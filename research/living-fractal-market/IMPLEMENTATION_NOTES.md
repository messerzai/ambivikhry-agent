# Implementation contract

- Script: forecast_btc.py; Python 3.10+, standard library only.
- Data: Binance spot BTCUSDT 1h klines, UTC.
- Quality gate: >=100 closed candles, no duplicate/out-of-order timestamps, no missing hours, finite positive closes.
- Horizons: +1 to +24 hourly targets from UTC issue-hour boundary.
- Baseline champion candidate: exponentially weighted drift shrunk 90% toward random walk, capped at +/-0.08% per hour.
- Uncertainty: Gaussian log-return approximation; uncalibrated until forward coverage is measured.
- Primary comparison: random walk/last price; also zero-drift and volatility-aware baselines.
- MF-DFA, news and sentiment are not yet implemented in this prototype; add only as independently tested challengers.
- Abstain on data quality failures. No trading or execution.
