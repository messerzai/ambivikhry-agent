#!/usr/bin/env python3
"""Living Fractal Market BTC forecaster v0.2; research only, Python 3.10+."""
import argparse
import datetime as dt
import json
import math
import statistics
import sys
import urllib.parse
import urllib.request

API = "https://api.binance.com/api/v3/klines"
MODEL = "LFM-Multiscale-Regime-Ensemble-0.2"

def load_candles(limit=500):
    query = urllib.parse.urlencode({"symbol": "BTCUSDT", "interval": "1h", "limit": limit})
    request = urllib.request.Request(API + "?" + query, headers={"User-Agent": "LivingFractalMarket/0.2"})
    with urllib.request.urlopen(request, timeout=20) as response:
        raw = json.loads(response.read().decode("utf-8"))
    now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
    rows = [{"open_ms": int(x[0]), "close_ms": int(x[6]), "open": float(x[1]),
             "high": float(x[2]), "low": float(x[3]), "close": float(x[4]),
             "volume": float(x[5])} for x in raw if int(x[6]) < now_ms]
    if len(rows) < 200:
        raise ValueError("need at least 200 closed hourly candles")
    times = [x["open_ms"] for x in rows]
    if times != sorted(set(times)):
        raise ValueError("duplicate or unordered candle timestamps")
    if any(b-a != 3_600_000 for a, b in zip(times, times[1:])):
        raise ValueError("hourly candle gap detected")
    for x in rows:
        if not all(math.isfinite(x[k]) for k in ("open", "high", "low", "close", "volume")):
            raise ValueError("non-finite OHLCV value")
        if min(x["open"], x["high"], x["low"], x["close"]) <= 0 or x["volume"] < 0:
            raise ValueError("invalid OHLCV value")
        if x["high"] < max(x["open"], x["close"], x["low"]) or x["low"] > min(x["open"], x["close"]):
            raise ValueError("inconsistent OHLC candle")
    age_ms = now_ms - rows[-1]["close_ms"]
    if age_ms > 90 * 60_000:
        raise ValueError("latest closed candle is stale (>90 minutes)")
    return rows

def ewma(values, half_life):
    weights = [math.exp(-math.log(2) * (len(values)-1-i) / half_life) for i in range(len(values))]
    return sum(v*w for v, w in zip(values, weights)) / sum(weights)

def forecast(rows, issued_at=None):
    closes = [x["close"] for x in rows]
    returns = [math.log(b/a) for a, b in zip(closes, closes[1:])]
    if len(returns) < 199:
        raise ValueError("insufficient return history")
    # Multi-scale trend: fast, medium and slow estimates; each is deliberately shrunk.
    m_fast = ewma(returns[-24:], 8)
    m_mid = ewma(returns[-72:], 24)
    m_slow = ewma(returns[-168:], 56)
    momentum = 0.50*m_fast + 0.30*m_mid + 0.20*m_slow
    # Volatility regime controls how much directional information is trusted.
    sig_fast = statistics.stdev(returns[-24:])
    sig_slow = statistics.stdev(returns[-168:])
    vol_ratio = sig_fast / max(sig_slow, 1e-9)
    regime_confidence = max(0.15, min(0.75, 0.55 / max(1.0, vol_ratio)))
    # Detect trend disagreement; disagreement reduces the directional component.
    dispersion = statistics.pstdev([m_fast, m_mid, m_slow])
    agreement = 1.0 / (1.0 + dispersion / max(sig_slow, 1e-9))
    # A bounded ensemble drift. The shrinkage is intentional: no claim of alpha.
    drift = momentum * regime_confidence * agreement * 0.35
    drift = max(-0.0012, min(0.0012, drift))
    # Mild pull toward the 72h mean when price is stretched; fades over the horizon.
    mean72 = statistics.mean(closes[-72:])
    stretch = math.log(mean72 / closes[-1])
    reversion = max(-0.00018, min(0.00018, stretch * 0.015))
    # Volatility forecast blends recent and medium regimes.
    sigma = 0.65*sig_fast + 0.35*sig_slow
    sigma = max(0.0005, min(0.03, sigma))
    ref = closes[-1]
    now = issued_at or dt.datetime.now(dt.timezone.utc)
    if now.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")
    issue_hour = now.astimezone(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    cutoff = dt.datetime.fromtimestamp(rows[-1]["close_ms"]/1000, dt.timezone.utc)
    path = []
    cumulative = 0.0
    for h in range(1, 25):
        # Fast signal decays; slow signal persists. Reversion strengthens only gradually.
        decay = math.exp(-(h-1)/10.0)
        step_drift = drift*decay + reversion*(1.0-math.exp(-h/12.0))
        cumulative += step_drift
        point = ref * math.exp(cumulative)
        width = sigma * math.sqrt(h)
        path.append({
            "horizon_h": h,
            "target_utc": (issue_hour + dt.timedelta(hours=h)).isoformat().replace("+00:00", "Z"),
            "point_usd": round(point, 2),
            "p50_low_usd": round(ref*math.exp(cumulative-0.67449*width), 2),
            "p50_high_usd": round(ref*math.exp(cumulative+0.67449*width), 2),
            "p90_low_usd": round(ref*math.exp(cumulative-1.64485*width), 2),
            "p90_high_usd": round(ref*math.exp(cumulative+1.64485*width), 2)
        })
    return {
        "schema": "lfm.forecast.v2",
        "asset": "BTC/USDT",
        "venue": "Binance spot",
        "issued_at_utc": now.astimezone(dt.timezone.utc).isoformat(),
        "data_cutoff_utc": cutoff.isoformat(),
        "reference_price_usd": ref,
        "model": MODEL,
        "model_status": "experimental; not yet validated; intervals uncalibrated",
        "training_window_candles": len(rows),
        "features": {
            "ewma_log_return_24h": m_fast,
            "ewma_log_return_72h": m_mid,
            "ewma_log_return_168h": m_slow,
            "fast_to_slow_volatility_ratio": vol_ratio,
            "trend_agreement": agreement,
            "regime_confidence": regime_confidence,
            "bounded_ensemble_hourly_drift": drift,
            "mean_reversion_component": reversion,
            "blended_hourly_volatility": sigma
        },
        "forecast": path,
        "warnings": [
            "Research forecast only; not investment advice or an execution signal.",
            "The ensemble is heuristic and has not demonstrated out-of-sample predictive edge.",
            "Intervals are Gaussian approximations and remain uncalibrated.",
            "BTCUSDT is a venue-specific proxy for BTC/USD."
        ]
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = forecast(load_candles())
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f'{result["model"]} | reference {result["reference_price_usd"]:.2f} USDT')
            print(f'Issued {result["issued_at_utc"]} | data cutoff {result["data_cutoff_utc"]}')
            print("h  target UTC                 point USD     approximate 90% interval")
            for row in result["forecast"]:
                print(f'{row["horizon_h"]:02d} {row["target_utc"]} {row["point_usd"]:12.2f}  '
                      f'{row["p90_low_usd"]:.2f} - {row["p90_high_usd"]:.2f}')
            for warning in result["warnings"]:
                print("WARNING:", warning)
    except Exception as exc:
        print(f"FORECAST ABSTAINED: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
