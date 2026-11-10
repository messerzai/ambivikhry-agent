# Executable BTC hourly forecast prototype

Requires Python 3.10+ and internet access. No API key or exchange account.

    python research/living-fractal-market/forecast_btc.py
    python research/living-fractal-market/forecast_btc.py --json > forecast.json

Downloads up to 500 closed 1-hour BTCUSDT spot candles from Binance public market data. Validates at least 100 bars, unique ordered timestamps, no hourly gaps and finite positive closes. Excludes the still-forming candle. Produces 24 hourly targets. On stale, missing or invalid data it abstains.

Model LFM-Shrinkage-Drift-0.1: exponentially weighted 72-hour log-return drift, 90% shrinkage toward random walk, capped residual drift, and volatility-scaled approximate lognormal intervals. The intervals are uncalibrated pending forward evaluation.

This is the first executable baseline, not yet the full multifractal/sentiment champion. Fractal, news and sentiment features must be separate challengers with walk-forward evidence. Append every issued JSON forecast; never revise vintages. Research only, not financial advice.
