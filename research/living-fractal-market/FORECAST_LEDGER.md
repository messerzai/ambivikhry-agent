# Forecast ledger contract

Last reviewed: 2026-11-11  
Branch: research/living-fractal-market

## Current state

No valid BTC/USD or BTC/USDT forecast vintage has been issued from this branch as of 2026-11-11. No current feed passed the live timestamp and data-quality gate in this run, so no forecast row is fabricated. There is therefore no previous vintage to score.

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
