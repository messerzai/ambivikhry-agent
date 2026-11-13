# Forecast ledger contract

Last reviewed: 2026-11-13  
Branch: research/living-fractal-market

## Current state

One valid experimental BTC/USDT vintage was emitted by the 5m research workflow on 2026-11-12 and is now archived below. It is a 5m-input / hourly-target challenger, not a validated champion or a BTC/USD feed. Its final hourly target close was not yet available at the 2026-11-13 07:56:59Z review cutoff, so no full-vintage score is recorded. No calibrated intervals or champion status are claimed.

## Append-only storage contract

When a forecast is valid, store one immutable JSON record per model and issue vintage under:

forecasts/YYYY-MM-DD/<issued_at_utc>_<asset>_<venue>_<model_version>.json

Never overwrite or edit an issued forecast. A corrected data feed creates a new vintage with a new issue timestamp and a note linking the superseded record; it does not rewrite history. Keep evaluation outputs separate:

evaluations/<forecast_vintage_id>.json

An evaluation may be appended only after all exact target closes are available. It must reference the original forecast file and the actual-data source/revision used for scoring.

## Required forecast fields

- schema version and unique vintage id;
- asset, venue, quote currency and candle interval;
- issue timestamp UTC and exact last input close/cutoff UTC;
- data source, endpoint and retrieval timestamp;
- reference price and number of closed observations;
- model name, version, immutable source commit and training cutoff;
- target timestamps +1 through +24, one point price per horizon;
- prediction intervals only when calibration method and calibration sample are recorded;
- diagnostics, warnings and abstention status.

## Required evaluation fields

- original vintage id and original model/commit;
- exact target timestamps and actual source/revision;
- primary normalized MAE of hourly log-price forecasts;
- random-walk and simple volatility-aware baseline losses on the same origins;
- secondary directional accuracy, interval coverage and width;
- CRPS or pinball loss only when a full distribution/quantile forecast exists;
- sample size, dependence/overlap warning, confidence interval and leakage audit;
- virtual research points under the frozen tournament rule.

The current GitHub Actions artifact has 14-day retention and is not a durable append-only ledger. A persistent writer/storage mechanism must be implemented before claiming long-term ledger completeness.


## Issued vintages (append-only)

### 2026-11-12 — Binance Spot BTCUSDT 5m council 0.3

- **Immutable archive:** forecasts/2026-11-12/2026-11-12T08-03-03.240211Z_BTCUSDT_BinanceSpot_LFM-5m-0.3.json.gz
- **Original workflow:** https://github.com/messerzai/ambivikhry-agent/actions/runs/43179787161 (artifact ID 13925638014; original artifact retention ends 2026-11-26).
- **Model/source commit:** 75cbc8bebc42e91033713263e338ada4c0848e95.
- **Vintage ID:** lfm5m-20261112T080303.240211Z-BTCUSDT-binance-spot-council-0.3.
- **Issue time UTC:** 2026-11-12T08:03:03.240211Z.
- **Data cutoff UTC:** 2026-11-12T07:59:59.999Z.
- **Source:** https://data-api.binance.vision/api/v3/klines ; symbol BTCUSDT; interval 5m; Binance Spot.
- **Reference:** 73,660.61 USDT; 999 closed 5m candles.
- **Models:** RandomWalk, Momentum5m, MeanReversion5m, VolatilityRegime5m, TakerFlow5m, DownsideStress5m, LFM5mEnsemble; 24 hourly target points each.
- **Intervals:** Gaussian-style P90 only; explicitly uncalibrated and not eligible for tournament points.
- **Raw JSON SHA-256:** c6b099b0a17e510b76e2a25cc2b97dc9b4b0659c4c508a2dadea0ca75c8f227b.
- **Archived gzip SHA-256:** 7b586d6c46e300e683e1fdc8337cceb0c92d954385e24f047610b1e202d79e10.
- **Target range:** 2026-11-12T09:00:00Z through 2026-11-13T08:00:00Z (hourly candle open times; final candle closes at 08:59:59.999Z).
- **Evaluation status:** pending at the review cutoff; no score or virtual points awarded.

The compressed file is the lossless gzip of the exact workflow artifact's forecast_5m.json. Verify with gzip -dc and compare the uncompressed SHA-256 above. Never replace this vintage; add any correction as a separate dated record.
