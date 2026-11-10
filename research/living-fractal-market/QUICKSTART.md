# Executable BTC hourly forecast prototypes

Requires Python 3.10+ and internet access. No API key or exchange account.

## Generation 0.2 (current challenger)

From the repository root:

    python research/living-fractal-market/forecast_btc_v2.py
    python research/living-fractal-market/forecast_btc_v2.py --json > forecast_v2.json

Model `LFM-Multiscale-Regime-Ensemble-0.2` combines 24h/72h/168h exponentially weighted log-return signals, trend agreement, a volatility-regime confidence factor, bounded directional shrinkage, and a gradually fading mean-reversion term. It produces 24 hourly point estimates and approximate 50%/90% ranges.

The model validates at least 200 closed hourly candles, timestamp ordering, hourly continuity, OHLCV sanity and data freshness (latest closed candle no older than 90 minutes). It abstains rather than inventing values when these gates fail.

## Tests

From `research/living-fractal-market`:

    python -m unittest test_forecast_btc_v2.py

## Previous baseline

    python research/living-fractal-market/forecast_btc.py

The v0.1 model remains a simple shrinkage-drift reference. V0.2 is a challenger, not yet champion: no out-of-sample edge has been established, and its Gaussian-style intervals are uncalibrated. Keep every forecast vintage immutable and score only after target candles close.

Research only; not financial advice and not a trading/execution system.

## Forecast council: independent model generations

Run all parallel challengers from the repository root:

    python research/living-fractal-market/forecast_council.py
    python research/living-fractal-market/forecast_council.py --json > forecast_council.json

The council issues 24 hourly points for five independent baselines: RandomWalk, TrendOnly, MeanReversion, VolRegimeEnsemble, and VolumePressure. This gives the forecasting branch a comparison set inspired by different reasoning styles rather than treating one model as unquestionable. These are mathematical baselines, not literal executions of other conversational personas. Every model uses the same validated Binance candle window and reference price. All are experimental; no winner is promoted without walk-forward scoring.

## Five-minute BTC forecast (new challenger)

From the repository root:

    python research/living-fractal-market/forecast_btc_5m.py
    python research/living-fractal-market/forecast_btc_5m.py --json > forecast_5m.json

This module uses the public Binance Spot market-data endpoint (no API key), with fallback public hosts. It loads up to 1,000 five-minute candles, excludes the still-forming candle, and abstains on insufficient history, gaps, stale data, malformed OHLCV, or endpoint failure. It emits 24 hourly target points from five-minute features and six challengers: RandomWalk, Momentum5m, MeanReversion5m, VolatilityRegime5m, TakerFlow5m, and LFM5mEnsemble.

The TakerFlow feature uses reported taker-buy volume, not order-book depth or a full order-flow reconstruction. All models are experimental. The Gaussian-style P90 bands are uncalibrated and must not be interpreted as statistically validated coverage.

Tests (from the model directory):

    cd research/living-fractal-market
    python -m unittest test_forecast_btc_5m.py

The 5m model is a separate challenger; it does not replace or silently alter the hourly v0.2 model or the existing council. BTC/USDT is quoted in USDT, not USD. Research only; no trading or execution.
