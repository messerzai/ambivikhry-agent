#!/usr/bin/env python3
"""Evaluate completed, immutable LFM forecast vintages against Binance Spot hourly closes.

This script is deliberately read-only with respect to market accounts and trading.
It fetches public historical candles, preserves their exact response bytes, and
writes evaluation artifacts. It never submits orders or modifies forecasts.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from statistics import mean
from typing import Any

BINANCE_KLINES = "https://data-api.binance.vision/api/v3/klines"
Z90 = 1.6448536269514722
INTERVAL_MS = 3_600_000


def parse_utc(value: str) -> datetime:
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp lacks UTC offset: {value}")
    return parsed.astimezone(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def make_vintage_id(forecast: dict[str, Any]) -> str:
    issued = str(forecast["issued_at_utc"])
    asset = str(forecast.get("asset", "BTCUSDT")).replace("/", "")
    venue = _slug(str(forecast.get("venue", "binance-spot")))
    model_version = str(forecast.get("model_version", "unknown")).lower()
    version_tag = (
        "council-" + model_version.rsplit("council-", 1)[1]
        if "council-" in model_version
        else _slug(model_version)
    )
    return f"lfm5m-{issued}-{asset}-{venue}-{version_tag}"


def load_forecast_archive(path: Path) -> tuple[dict[str, Any], bytes, str]:
    archive_bytes = path.read_bytes()
    if path.name.endswith(".json.gz"):
        forecast_bytes = gzip.decompress(archive_bytes)
    elif path.name.endswith(".artifact.zip"):
        with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
            candidates = [name for name in archive.namelist() if name.endswith("forecast_5m.json")]
            if len(candidates) != 1:
                raise ValueError(f"expected one forecast_5m.json in {path}, found {len(candidates)}")
            forecast_bytes = archive.read(candidates[0])
    else:
        raise ValueError(f"unsupported forecast archive: {path}")
    forecast = json.loads(forecast_bytes.decode("utf-8"))
    if not isinstance(forecast, dict):
        raise ValueError("forecast JSON root must be an object")
    return forecast, forecast_bytes, sha256_bytes(archive_bytes)


def validate_forecast(forecast: dict[str, Any]) -> list[datetime]:
    required = ("issued_at_utc", "data_cutoff_utc", "asset", "venue",
                "reference_price_usdt", "diagnostics", "models")
    missing = [key for key in required if key not in forecast]
    if missing:
        raise ValueError(f"forecast missing required fields: {missing}")
    issue = parse_utc(forecast["issued_at_utc"])
    cutoff = parse_utc(forecast["data_cutoff_utc"])
    reference = float(forecast["reference_price_usdt"])
    if not math.isfinite(reference) or reference <= 0:
        raise ValueError("reference price must be finite and positive")
    models = forecast["models"]
    if not isinstance(models, list) or not models:
        raise ValueError("forecast has no models")
    target_grid: list[datetime] | None = None
    for model in models:
        points = model.get("points", [])
        if len(points) != 24:
            raise ValueError(f"{model.get('model')} must contain exactly 24 points")
        grid = [parse_utc(point["target_utc"]) for point in points]
        if grid != sorted(grid) or len(set(grid)) != 24:
            raise ValueError(f"{model.get('model')} target grid is unordered or duplicated")
        if target_grid is None:
            target_grid = grid
        elif grid != target_grid:
            raise ValueError("models do not share one identical target grid")
        for point in points:
            price = float(point["point_usdt"])
            if not math.isfinite(price) or price <= 0:
                raise ValueError("forecast point must be finite and positive")
            low = point.get("p90_low_usdt")
            high = point.get("p90_high_usdt")
            if low is not None and high is not None:
                low, high = float(low), float(high)
                if not (math.isfinite(low) and math.isfinite(high) and 0 < low <= high):
                    raise ValueError("invalid P90 interval")
        if grid[0] <= issue or grid[0] <= cutoff:
            raise ValueError("first target must be after issue time and data cutoff")
    if target_grid is None:
        raise ValueError("missing target grid")
    return target_grid


def validate_actual_rows(
    rows: list[list[Any]],
    expected_open_ms: list[int],
    now_ms: int,
) -> list[dict[str, Any]]:
    expected = set(expected_open_ms)
    found: dict[int, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, list) or len(row) < 7:
            raise ValueError("Binance kline row must contain at least seven fields")
        open_ms = int(row[0])
        if open_ms not in expected:
            continue
        if open_ms in found:
            raise ValueError(f"duplicate hourly candle at {open_ms}")
        open_price, high, low, close, volume = map(float, row[1:6])
        close_ms = int(row[6])
        values = (open_price, high, low, close, volume)
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"non-finite OHLCV at {open_ms}")
        if min(open_price, high, low, close) <= 0 or volume < 0:
            raise ValueError(f"non-positive OHLC or negative volume at {open_ms}")
        if low > min(open_price, close) or high < max(open_price, close) or low > high:
            raise ValueError(f"inconsistent OHLC at {open_ms}")
        if close_ms != open_ms + INTERVAL_MS - 1:
            raise ValueError(f"unexpected close timestamp at {open_ms}")
        if close_ms >= now_ms:
            raise ValueError(f"target candle is not closed at {open_ms}")
        found[open_ms] = {
            "open_time_ms": open_ms,
            "close_time_ms": close_ms,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    missing = sorted(expected.difference(found))
    if missing:
        raise ValueError(f"missing {len(missing)} target hourly candles; first missing open_ms={missing[0]}")
    return [found[stamp] for stamp in expected_open_ms]


def fetch_hourly_rows(
    symbol: str,
    target_grid: list[datetime],
    timeout: int = 30,
) -> tuple[bytes, str]:
    start_ms = int(target_grid[0].timestamp() * 1000)
    end_ms = int(target_grid[-1].timestamp() * 1000) + INTERVAL_MS - 1
    query = urllib.parse.urlencode({
        "symbol": symbol,
        "interval": "1h",
        "startTime": start_ms,
        "endTime": end_ms,
        "limit": 1000,
    })
    url = f"{BINANCE_KLINES}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "LFM-Research-Evaluator/1.0"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
            return raw, url
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(attempt + 1)
    raise RuntimeError(f"Binance hourly data request failed: {last_error}")


def sign(value: float, tolerance: float = 1e-12) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def score_path(
    points: list[dict[str, Any]],
    actual_closes: list[float],
    reference_price: float,
    sigma_hour: float,
) -> dict[str, Any]:
    if len(points) != 24 or len(actual_closes) != 24:
        raise ValueError("scoring requires 24 forecast points and 24 actual closes")
    if not math.isfinite(sigma_hour) or sigma_hour <= 0:
        raise ValueError("point-in-time hourly sigma must be finite and positive")
    predicted = [float(point["point_usdt"]) for point in points]
    actual = [float(value) for value in actual_closes]
    if any(not math.isfinite(value) or value <= 0 for value in predicted + actual):
        raise ValueError("predicted and actual prices must be finite and positive")
    log_errors = [abs(math.log(p) - math.log(a)) for p, a in zip(predicted, actual)]
    raw_log_mae = mean(log_errors)
    normalized_mae = raw_log_mae / sigma_hour

    predicted_from_issue = [sign(math.log(value / reference_price)) for value in predicted]
    actual_from_issue = [sign(math.log(value / reference_price)) for value in actual]
    direction_vs_issue = mean(
        float(pred == observed)
        for pred, observed in zip(predicted_from_issue, actual_from_issue)
    )

    previous_predicted = reference_price
    previous_actual = reference_price
    sequential_hits: list[float] = []
    for predicted_value, actual_value in zip(predicted, actual):
        predicted_change = sign(math.log(predicted_value / previous_predicted))
        actual_change = sign(math.log(actual_value / previous_actual))
        sequential_hits.append(float(predicted_change == actual_change))
        previous_predicted = predicted_value
        previous_actual = actual_value

    lows = [point.get("p90_low_usdt") for point in points]
    highs = [point.get("p90_high_usdt") for point in points]
    if all(value is not None for value in lows + highs):
        lows_f = [float(value) for value in lows]
        highs_f = [float(value) for value in highs]
        coverage = mean(float(low <= observed <= high)
                        for low, high, observed in zip(lows_f, highs_f, actual))
        width_pct = mean((high - low) / point
                         for low, high, point in zip(lows_f, highs_f, predicted)) * 100
    else:
        coverage = None
        width_pct = None

    return {
        "log_price_mae": raw_log_mae,
        "normalized_log_price_mae": normalized_mae,
        "normalization_sigma_hour_at_issue": sigma_hour,
        "directional_accuracy_vs_issue_reference": direction_vs_issue,
        "directional_accuracy_hour_to_hour": mean(sequential_hits),
        "p90_empirical_coverage": coverage,
        "p90_mean_width_pct_of_point": width_pct,
        "target_points": 24,
    }


def volatility_capped_slow_drift_baseline(
    reference_price: float,
    sigma_hour: float,
    slow_12h_log_return_per_hour: float,
) -> list[dict[str, float]]:
    cap = 0.25 * sigma_hour
    drift = max(-cap, min(cap, slow_12h_log_return_per_hour))
    points: list[dict[str, float]] = []
    for horizon in range(1, 25):
        center = reference_price * math.exp(drift * horizon)
        radius = Z90 * sigma_hour * math.sqrt(horizon)
        points.append({
            "point_usdt": center,
            "p90_low_usdt": center * math.exp(-radius),
            "p90_high_usdt": center * math.exp(radius),
        })
    return points


def threshold_event_diagnostic(
    forecast: dict[str, Any],
    actual_closes: list[float],
) -> dict[str, Any] | None:
    risk = forecast.get("downside_risk", {})
    diagnostics = forecast.get("diagnostics", {})
    level_value = risk.get("level_usdt", diagnostics.get("downside_level_usdt"))
    probability_value = risk.get("heuristic_probability_below_level_24h")
    if level_value is None or probability_value is None:
        return None
    level = float(level_value)
    probability = float(probability_value)
    if not (math.isfinite(level) and level > 0 and math.isfinite(probability) and 0 <= probability <= 1):
        return None
    observed = bool(actual_closes[-1] < level)
    reference = float(forecast["reference_price_usdt"])
    return {
        "event": "terminal_hourly_close_below_level",
        "level_usdt": level,
        "reference_already_below_level": reference < level,
        "heuristic_probability_uncalibrated": probability,
        "observed_terminal_outcome": observed,
        "brier_diagnostic_only": (probability - float(observed)) ** 2,
        "is_first_passage_probability": False,
        "interpretation": "One-vintage diagnostic only; the source probability is explicitly uncalibrated and receives no tournament credit.",
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def evaluate_vintage(
    path: Path,
    forecast_root: Path,
    evaluation_root: Path,
    output_dir: Path,
    now: datetime,
) -> dict[str, Any]:
    forecast, forecast_bytes, archive_sha = load_forecast_archive(path)
    target_grid = validate_forecast(forecast)
    vintage_id = make_vintage_id(forecast)
    evaluation_records = list(evaluation_root.rglob(f"{vintage_id}.json")) if evaluation_root.exists() else []
    if evaluation_records:
        return {"status": "already_evaluated", "vintage_id": vintage_id, "archive": str(path)}

    final_close = target_grid[-1] + timedelta(hours=1) - timedelta(milliseconds=1)
    if final_close > now:
        return {
            "status": "pending",
            "vintage_id": vintage_id,
            "archive": str(path),
            "final_target_close_utc": iso_utc(final_close),
        }

    expected_open_ms = [int(value.timestamp() * 1000) for value in target_grid]
    symbol = str(forecast.get("symbol", "BTCUSDT"))
    raw_actual, actual_url = fetch_hourly_rows(symbol, target_grid)
    actual_rows_json = json.loads(raw_actual.decode("utf-8"))
    if not isinstance(actual_rows_json, list):
        raise ValueError("Binance response root must be an array")
    now_ms = int(now.timestamp() * 1000)
    actual_rows = validate_actual_rows(actual_rows_json, expected_open_ms, now_ms)
    actual_closes = [row["close"] for row in actual_rows]

    reference = float(forecast["reference_price_usdt"])
    diagnostics = forecast["diagnostics"]
    sigma_hour = float(diagnostics["hourly_sigma_estimate"])
    slow_drift = float(diagnostics["slow_12h_log_return_per_hour"])
    if not (math.isfinite(sigma_hour) and sigma_hour > 0 and math.isfinite(slow_drift)):
        raise ValueError("missing or invalid point-in-time volatility/drift diagnostics")

    random_walk_points = [
        {"point_usdt": reference} for _ in range(24)
    ]
    volatility_points = volatility_capped_slow_drift_baseline(reference, sigma_hour, slow_drift)
    baseline_results = {
        "RandomWalkLastPrice": score_path(random_walk_points, actual_closes, reference, sigma_hour),
        "VolatilityCappedSlowDrift": score_path(volatility_points, actual_closes, reference, sigma_hour),
    }
    strongest_simple = min(
        result["normalized_log_price_mae"] for result in baseline_results.values()
    )

    model_results = []
    for model in forecast["models"]:
        result = score_path(model["points"], actual_closes, reference, sigma_hour)
        result.update({
            "model": model["model"],
            "beats_random_walk_primary_loss": (
                result["normalized_log_price_mae"]
                < baseline_results["RandomWalkLastPrice"]["normalized_log_price_mae"]
            ),
            "beats_strongest_simple_baseline_primary_loss": (
                result["normalized_log_price_mae"] < strongest_simple
            ),
        })
        model_results.append(result)
    model_results.sort(key=lambda item: item["normalized_log_price_mae"])

    forecast_warnings = str(forecast.get("warning", ""))
    intervals_calibrated = bool(forecast.get("interval_calibration", {}).get("calibrated", False))
    result = {
        "schema": "lfm.evaluation.hourly.v1",
        "evaluation_protocol": "LFM-Tournament-1.1",
        "status": "evaluated",
        "vintage_id": vintage_id,
        "forecast_archive": str(path),
        "forecast_archive_sha256": archive_sha,
        "forecast_json_sha256": sha256_bytes(forecast_bytes),
        "asset": forecast.get("asset"),
        "venue": forecast.get("venue"),
        "quote_currency": forecast.get("quote_currency"),
        "input_interval": "5m",
        "target_interval": "1h",
        "model_version": forecast.get("model_version"),
        "issued_at_utc": forecast.get("issued_at_utc"),
        "data_cutoff_utc": forecast.get("data_cutoff_utc"),
        "reference_price_usdt": reference,
        "actual_source": actual_url,
        "actual_retrieved_at_utc": iso_utc(now),
        "actual_data_sha256": sha256_bytes(raw_actual),
        "target_grid_open_utc": [iso_utc(value) for value in target_grid],
        "target_grid_final_close_utc": iso_utc(final_close),
        "actual_hourly_closes_usdt": actual_closes,
        "threshold_event_diagnostic": threshold_event_diagnostic(forecast, actual_closes),
        "baseline_results": baseline_results,
        "model_results_ranked_by_primary_loss": model_results,
        "primary_metric": {
            "name": "normalized_mae_hourly_log_price",
            "formula": "mean(abs(log(predicted_price_h)-log(actual_close_h))) / hourly_sigma_estimate_frozen_at_issue",
            "normalization_is_point_in_time": True,
            "denominator_sigma_hour": sigma_hour,
        },
        "secondary_metrics": [
            "directional_accuracy_vs_issue_reference",
            "directional_accuracy_hour_to_hour",
            "p90_empirical_coverage",
            "p90_mean_width_pct_of_point",
        ],
        "intervals_calibrated": intervals_calibrated,
        "forecast_warning": forecast_warnings,
        "sample_size": {
            "vintages": 1,
            "hourly_targets": 24,
            "overlap_note": "The 24 horizons within one vintage are serially dependent and are not 24 independent daily samples.",
        },
        "virtual_points_awarded": 0,
        "virtual_points_eligibility": {
            "eligible": False,
            "reason": "Forecast P90 intervals are explicitly uncalibrated; one vintage also cannot establish skill or support champion promotion.",
        },
        "limitations": [
            "BTC/USDT is not identical to BTC/USD.",
            "The forecast uses Binance Spot 5m inputs and predicts hourly closes.",
            "One completed vintage is insufficient for model promotion.",
            "The volatility-aware baseline uses a point-in-time 12h drift summary capped by point-in-time hourly sigma.",
        ],
    }

    safe_id = _slug(vintage_id)
    evaluation_file = output_dir / f"evaluation_{safe_id}.json"
    actual_file = output_dir / f"actual_hourly_{safe_id}.json"
    write_json(evaluation_file, result)
    actual_file.parent.mkdir(parents=True, exist_ok=True)
    actual_file.write_bytes(raw_actual)
    return {
        "status": "evaluated",
        "vintage_id": vintage_id,
        "archive": str(path),
        "evaluation_file": str(evaluation_file),
        "actual_file": str(actual_file),
        "actual_data_sha256": sha256_bytes(raw_actual),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--forecast-root", type=Path, required=True)
    parser.add_argument("--evaluation-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--now", help="Optional ISO-8601 UTC time for deterministic tests")
    args = parser.parse_args()

    now = parse_utc(args.now) if args.now else datetime.now(timezone.utc)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    candidates = sorted(set(args.forecast_root.rglob("*.json.gz")) |
                        set(args.forecast_root.rglob("*.artifact.zip")))
    manifest: dict[str, Any] = {
        "schema": "lfm.evaluation.manifest.v1",
        "evaluated_at_utc": iso_utc(now),
        "forecast_root": str(args.forecast_root),
        "evaluation_root": str(args.evaluation_root),
        "evaluated": [],
        "pending": [],
        "already_evaluated": [],
        "duplicates": [],
        "failed": [],
    }
    for path in candidates:
        if path.name.endswith(".json.gz"):
            counterpart = path.with_name(path.name[:-len(".json.gz")] + ".artifact.zip")
            if counterpart.exists():
                manifest["duplicates"].append({
                    "archive": str(path),
                    "canonical_archive": str(counterpart),
                })
                continue
        try:
            forecast, _, _ = load_forecast_archive(path)
            vintage_id = make_vintage_id(forecast)
            outcome = evaluate_vintage(path, args.forecast_root, args.evaluation_root, args.output_dir, now)
            manifest[outcome["status"]].append(outcome)
        except Exception as exc:
            manifest["failed"].append({
                "archive": str(path),
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
    write_json(args.output_dir / "evaluation_manifest.json", manifest)
    print(json.dumps({
        "evaluated": len(manifest["evaluated"]),
        "pending": len(manifest["pending"]),
        "already_evaluated": len(manifest["already_evaluated"]),
        "failed": len(manifest["failed"]),
        "manifest": str(args.output_dir / "evaluation_manifest.json"),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
