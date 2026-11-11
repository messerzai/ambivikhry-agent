# Implementation contract

Last reviewed: 2026-11-11  
Branch: research/living-fractal-market

## Hourly prototype

- Script: forecast_btc.py; Python 3.10+, standard library only.
- Data: Binance Spot BTCUSDT 1h klines, UTC.
- Quality gate: at least 100 closed candles; timestamp ordering; no duplicate or missing hours; finite positive OHLCV; latest closed candle fresh.
- Horizons: +1 to +24 hourly targets from the next UTC hour boundary.
- Model: shrinkage-drift baseline, strongly shrunk toward random walk.
- Uncertainty: Gaussian log-return approximation; uncalibrated until forward coverage is measured.

## Hourly multiscale challenger

- Script: forecast_btc_v2.py; 200–500 closed Binance Spot BTCUSDT hourly candles.
- Model: LFM-Multiscale-Regime-Ensemble-0.2; 24h/72h/168h EWMA returns, trend agreement, volatility regime, bounded drift and fading mean reversion.
- Requires hourly continuity and a latest closed candle no older than 90 minutes.
- V0.2 is a challenger, not a proven champion. No out-of-sample edge has been established.

## Five-minute challenger

- Script: forecast_btc_5m.py; Python 3.10+, standard library only.
- Data: Binance Spot BTCUSDT 5m klines; up to 1,000 rows; no API key.
- Requires at least 300 closed bars, unique ordered timestamps, exact 5-minute continuity, finite/sane OHLCV, taker-buy base volume no greater than total base volume, and the latest expected fully closed candle.
- The currently forming candle is excluded. A trailing missing candle is a hard failure even when the remaining data would pass the broad 15-minute freshness limit.
- Emits seven separate +1…+24h trajectories: RandomWalk, Momentum5m, MeanReversion5m, VolatilityRegime5m, TakerFlow5m, DownsideStress5m and LFM5mEnsemble.
- TakerFlow uses reported spot taker-buy volume; it is not order-book depth or a complete trade-sign reconstruction.
- The fixed 70,000 USDT threshold is a stress diagnostic requested for downside scenario analysis. The normal-tail breach value is heuristic and uncalibrated, not a market-implied or validated probability.
- P90 ranges are Gaussian-style approximations and are not calibrated prediction intervals. BTC/USDT is not identical to BTC/USD.

## Evaluation and promotion

- Primary loss: normalized MAE of hourly log-price forecasts, following FORECASTING_TOURNAMENT.md.
- Baselines: random walk/last price, zero drift, simple trend and volatility-aware baseline.
- Secondary metrics: directional accuracy, interval coverage/width, CRPS or pinball loss when a genuine predictive distribution is emitted.
- Preserve each forecast vintage and score only after its exact target close is available.
- Do not count overlapping hourly origins as independent market events.
- Champion promotion requires at least 30 completed daily vintages, robust uncertainty-aware walk-forward evidence and no critical leakage.
- No model has earned a virtual research point in the absence of scored, calibrated forward vintages.

## Workflow and data limits

- .github/workflows/lfm-5m.yml is push-triggered on this research branch.
- GitHub schedule and workflow_dispatch triggers require the workflow file on the default branch. They are intentionally omitted because this project must not modify or merge into main.
- The workflow uploads a short-retention artifact; it is not a durable append-only forecast ledger.
- If a reliable current feed is unavailable, the model must abstain. Search snippets, stale quotes and future-dated rows are not valid inputs.

## Research boundaries

- MF-DFA/MFCCA, IAAFT surrogate tests, time irreversibility, news surprise, sentiment and microstructure are not yet production features in the forecasting prototypes.
- Add each feature as a separate challenger/ablation against the same baselines and point-in-time data.
- The “living/non-repeating fractal” framing is a hypothesis-generating metaphor, not an established fact.
- No trading, order execution, exchange credentials or financial transfers.
