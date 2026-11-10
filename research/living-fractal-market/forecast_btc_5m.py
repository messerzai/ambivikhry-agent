#!/usr/bin/env python3
"""LFM 5m BTC/USDT research forecaster. Python 3.10+, stdlib only."""
import argparse
import datetime as dt
import json
import math
import statistics
import sys
import urllib.parse
import urllib.request

BASES = ("https://data-api.binance.vision", "https://api.binance.com",
         "https://api1.binance.com", "https://api-gcp.binance.com")
INTERVAL_MS = 300_000
MODEL_VERSION = "LFM-5m-Downside-Aware-Council-0.2"
DOWNSIDE_LEVEL_USDT = 70000.0


def _request_rows(limit=1000, timeout=12):
    query = urllib.parse.urlencode({"symbol": "BTCUSDT", "interval": "5m", "limit": limit})
    errors = []
    for base in BASES:
        url = base + "/api/v3/klines?" + query
        request = urllib.request.Request(url, headers={"User-Agent": "LivingFractalMarket/5m-0.1"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8")), base
        except Exception as exc:
            errors.append(f"{base}: {type(exc).__name__}: {exc}")
    raise RuntimeError("all public Binance market-data endpoints failed: " + " | ".join(errors))


def parse_rows(raw, now=None, min_rows=300):
    now = now or dt.datetime.now(dt.timezone.utc)
    now_ms = int(now.timestamp() * 1000)
    rows = []
    for item in raw:
        if len(item) < 11:
            raise ValueError("malformed kline row")
        row = {
            "open_ms": int(item[0]), "open": float(item[1]), "high": float(item[2]),
            "low": float(item[3]), "close": float(item[4]), "volume": float(item[5]),
            "close_ms": int(item[6]), "quote_volume": float(item[7]),
            "trades": int(item[8]), "taker_buy_base": float(item[9]),
            "taker_buy_quote": float(item[10])
        }
        # Close timestamp is inclusive. Never admit the currently-forming candle.
        if row["close_ms"] < now_ms:
            rows.append(row)
    if len(rows) < min_rows:
        raise ValueError(f"need at least {min_rows} closed 5m candles; got {len(rows)}")
    times = [r["open_ms"] for r in rows]
    if times != sorted(set(times)):
        raise ValueError("duplicate or unordered 5m candle timestamps")
    if any(b-a != INTERVAL_MS for a, b in zip(times, times[1:])):
        raise ValueError("5m candle gap detected")
    for r in rows:
        values = [r[k] for k in ("open", "high", "low", "close", "volume", "quote_volume", "taker_buy_base", "taker_buy_quote")]
        if not all(math.isfinite(x) for x in values):
            raise ValueError("non-finite OHLCV value")
        if min(r["open"], r["high"], r["low"], r["close"]) <= 0 or min(r["volume"], r["quote_volume"], r["taker_buy_base"], r["taker_buy_quote"]) < 0:
            raise ValueError("invalid negative or zero market data")
        if r["high"] < max(r["open"], r["close"], r["low"]) or r["low"] > min(r["open"], r["close"]):
            raise ValueError("inconsistent OHLC candle")
        if r["taker_buy_base"] > r["volume"] * 1.000001:
            raise ValueError("taker-buy volume exceeds total base volume")
    age_ms = now_ms - rows[-1]["close_ms"]
    if age_ms > 15 * 60_000:
        raise ValueError(f"latest closed 5m candle stale ({age_ms/60000:.1f} minutes)")
    return rows


def ewma(values, half_life):
    weights = [math.exp(-math.log(2) * (len(values)-1-i) / half_life) for i in range(len(values))]
    return sum(v*w for v, w in zip(values, weights)) / sum(weights)


def _clamp(x, low, high):
    return max(low, min(high, x))


def build_forecast(rows, issued_at=None, source="Binance Spot public market data"):
    if len(rows) < 300:
        raise ValueError("insufficient 5m history")
    closes = [r["close"] for r in rows]
    returns = [math.log(b/a) for a, b in zip(closes, closes[1:])]
    if len(returns) < 299:
        raise ValueError("insufficient return history")
    ref = closes[-1]
    # Signals are measured at 1h, 4h, 12h and 24h scales (12 bars/hour).
    r1, r4, r12 = returns[-12:], returns[-48:], returns[-144:]
    fast, medium, slow = ewma(r1, 4), ewma(r4, 16), ewma(r12, 48)
    sig1 = statistics.stdev(r1)
    sig24 = statistics.stdev(returns[-288:]) if len(returns) >= 288 else statistics.stdev(returns)
    vol_ratio = sig1 / max(sig24, 1e-12)
    agreement = 1.0 / (1.0 + statistics.pstdev([fast, medium, slow]) / max(sig24, 1e-12))
    trend_hour = _clamp((0.50*fast + 0.30*medium + 0.20*slow) * 12, -0.0025, 0.0025)
    trend_hour *= _clamp(0.75 * agreement, 0.10, 0.75)
    mean12 = statistics.mean(closes[-144:])
    reversion_hour = _clamp(math.log(mean12/ref) * 0.012, -0.0008, 0.0008)
    regime_weight = _clamp(0.60 / max(1.0, vol_ratio), 0.12, 0.65)
    ensemble_hour = _clamp(trend_hour * regime_weight + reversion_hour * 0.25, -0.0015, 0.0015)

    # Taker-buy imbalance is observable on spot candles; it is not order-book depth.
    recent = rows[-12:]
    base_total = sum(x["volume"] for x in recent)
    buy_total = sum(x["taker_buy_base"] for x in recent)
    imbalance = (2.0 * buy_total / base_total - 1.0) if base_total > 0 else 0.0
    rel_volume = (sum(x["quote_volume"] for x in recent) / 12 /
                  max(statistics.mean(x["quote_volume"] for x in rows[-144:]), 1e-12))
    flow_hour = _clamp(imbalance * _clamp(rel_volume, 0.25, 3.0) * 0.00035, -0.0007, 0.0007)

    # Explicit downside diagnostics. These are risk features, not proof of a crash.
    recent_high_24h = max(closes[-288:])
    drawdown_24h = ref / recent_high_24h - 1.0
    negative_returns = [min(x, 0.0) for x in returns[-288:]]
    downside_sigma_5m = math.sqrt(statistics.mean(x*x for x in negative_returns))
    downside_sigma_hour = max(0.00015, downside_sigma_5m * math.sqrt(12))
    downside_momentum_hour = statistics.mean(returns[-12:]) * 12
    downside_pressure = (
        0.45 * min(trend_hour, 0.0)
        + 0.20 * min(flow_hour, 0.0)
        + 0.15 * min(reversion_hour, 0.0)
        + 0.20 * min(downside_momentum_hour, 0.0)
    )
    # Only activates on negative evidence; capped to avoid extrapolating a crash indefinitely.
    downside_stress_hour = _clamp(downside_pressure * 1.8, -0.0035, 0.0)

    models = {
        "RandomWalk": lambda h: 0.0,
        "Momentum5m": lambda h: trend_hour * math.exp(-(h-1)/5.0),
        "MeanReversion5m": lambda h: reversion_hour * (1.0-math.exp(-h/8.0)),
        "VolatilityRegime5m": lambda h: ensemble_hour * math.exp(-(h-1)/7.0) + reversion_hour*(1.0-math.exp(-h/10.0)),
        "TakerFlow5m": lambda h: flow_hour * math.exp(-(h-1)/2.5),
        "DownsideStress5m": lambda h: downside_stress_hour * math.exp(-(h-1)/18.0),
        "LFM5mEnsemble": lambda h: (0.45*trend_hour*math.exp(-(h-1)/6.0)
                                     + 0.30*reversion_hour*(1.0-math.exp(-h/9.0))
                                     + 0.25*flow_hour*math.exp(-(h-1)/3.0))
    }
    now = issued_at or dt.datetime.now(dt.timezone.utc)
    if now.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")
    now = now.astimezone(dt.timezone.utc)
    next_hour = now.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)
    cutoff = dt.datetime.fromtimestamp(rows[-1]["close_ms"]/1000, dt.timezone.utc)
    # Convert 5m log-return volatility to hourly scale; intervals are explicitly uncalibrated.
    hourly_sigma = max(0.00015, min(0.025, sig24 * math.sqrt(12)))
    model_outputs = []
    for name, step in models.items():
        cumulative, points = 0.0, []
        for h in range(1, 25):
            cumulative += step(h)
            width = hourly_sigma * math.sqrt(h)
            points.append({
                "horizon_h": h,
                "target_utc": (next_hour + dt.timedelta(hours=h-1)).isoformat().replace("+00:00", "Z"),
                "point_usdt": round(ref * math.exp(cumulative), 2),
                "p90_low_usdt": round(ref * math.exp(cumulative - 1.64485*width), 2),
                "p90_high_usdt": round(ref * math.exp(cumulative + 1.64485*width), 2)
            })
        model_outputs.append({"model": name, "points": points})
    return {
        "schema": "lfm.forecast.5m.v1", "model_version": MODEL_VERSION,
        "asset": "BTC/USDT", "venue": "Binance Spot", "quote_currency": "USDT",
        "source": source, "issued_at_utc": now.isoformat().replace("+00:00", "Z"),
        "data_cutoff_utc": cutoff.isoformat().replace("+00:00", "Z"),
        "reference_price_usdt": ref, "closed_candles": len(rows),
        "diagnostics": {
            "fast_1h_log_return": fast*12, "medium_4h_log_return_per_hour": medium*12,
            "slow_12h_log_return_per_hour": slow*12, "volatility_ratio": vol_ratio,
            "trend_agreement": agreement, "taker_buy_imbalance": imbalance,
            "relative_quote_volume_1h": rel_volume, "hourly_sigma_estimate": hourly_sigma,
            "bounded_trend_signal_per_hour": trend_hour,
            "mean_reversion_signal_per_hour": reversion_hour,
            "taker_flow_signal_per_hour": flow_hour,
            "drawdown_from_24h_high": drawdown_24h,
            "downside_sigma_hour": downside_sigma_hour,
            "downside_momentum_per_hour": downside_momentum_hour,
            "downside_stress_signal_per_hour": downside_stress_hour,
            "downside_level_usdt": DOWNSIDE_LEVEL_USDT
        },
        "downside_risk": {
            "level_usdt": DOWNSIDE_LEVEL_USDT,
            "distance_to_level_pct": round((DOWNSIDE_LEVEL_USDT / ref - 1.0) * 100.0, 3),
            "stress_model_24h_point_usdt": round(ref * math.exp(sum(
                downside_stress_hour * math.exp(-(h-1)/18.0) for h in range(1, 25)
            )), 2),
            "severe_tail_scenario": {
                "shock_pct": -6.0,
                "scenario_price_usdt": round(ref * 0.94, 2),
                "crosses_level": ref * 0.94 < DOWNSIDE_LEVEL_USDT,
                "interpretation": "Illustrative abrupt 6% downside shock, not a point forecast and not assigned a probability."
            },
            "heuristic_probability_below_level_24h": round(0.5 * (
                1.0 + math.erf((
                    math.log(DOWNSIDE_LEVEL_USDT/ref)
                    - sum(downside_stress_hour * math.exp(-(h-1)/18.0) for h in range(1, 25))
                ) / (downside_sigma_hour * math.sqrt(24) * math.sqrt(2))
            )), 4),
            "method": "Normal-tail approximation using downside semivolatility and a decaying, evidence-gated downside drift; uncalibrated, not a market-implied probability."
        },
        "models": model_outputs,
        "warning": ("Experimental research forecasts, not validated predictors or financial advice. Downside breach probability is an uncalibrated stress diagnostic, not a calibrated probability. "
                    "P90 ranges are Gaussian-style approximations and are NOT calibrated prediction intervals. "
                    "BTC/USDT is not identical to BTC/USD. No trading or order execution.")
    }


def main():
    parser = argparse.ArgumentParser(description="LFM 5m BTC/USDT 24-hour research forecast")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--limit", type=int, default=1000, help="Binance 5m candle limit (300..1000)")
    args = parser.parse_args()
    if not 300 <= args.limit <= 1000:
        parser.error("--limit must be between 300 and 1000")
    try:
        raw, endpoint = _request_rows(limit=args.limit)
        now = dt.datetime.now(dt.timezone.utc)
        rows = parse_rows(raw, now=now)
        result = build_forecast(rows, issued_at=now, source=endpoint + "/api/v3/klines")
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f'{result["model_version"]} | BTC/USDT | ref {result["reference_price_usdt"]:.2f} USDT')
            print(f'Issued {result["issued_at_utc"]} | cutoff {result["data_cutoff_utc"]} | candles {result["closed_candles"]}')
            for model in result["models"]:
                print("\n" + model["model"])
                for point in model["points"]:
                    print(f'+{point["horizon_h"]:02d}h {point["target_utc"]}  {point["point_usdt"]:.2f} '
                          f'[{point["p90_low_usdt"]:.2f}, {point["p90_high_usdt"]:.2f}]')
            print("\n" + result["warning"])
    except Exception as exc:
        print(f"FORECAST ABSTAINED: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
