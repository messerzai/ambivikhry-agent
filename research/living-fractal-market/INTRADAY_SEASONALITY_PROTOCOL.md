# Intraday seasonality and clock-phase experiment protocol

**Status:** pre-registered research design; no feature is enabled in a forecast model.  
**Created:** 2026-11-12  
**Branch:** `research/living-fractal-market`

## Research question

Do UTC hour-of-week, five-minute bar phase, and quarter-hour boundary effects explain variation in BTC spot returns, realized volatility, volume or taker-buy imbalance? If so, do these features improve out-of-sample forecasts after controlling for volatility and regime, or do they merely describe recurring activity patterns?

The “living/non-repeating fractal” metaphor remains a hypothesis-generating frame, not an established property of BTC prices.

## Evidence motivating the test

1. Kim & Hansen, “The Quarter-Hour Effect: Periodic Algorithmic Trading and Return Predictability in Cryptocurrency Futures,” arXiv:2607.09426 (revised July 2026, preprint). Its abstract reports recurring 1m/5m/15m bursts in six Binance perpetual contracts and out-of-sample opening-return predictability; opening order imbalance is reported to predict returns over 4–12h, with weaker effects at finer clock-time frequencies. This is not evidence of the same effect in Spot BTC/USDT.
2. Hansen, Kim & Kimbrough, “Periodicity in Cryptocurrency Volatility and Liquidity,” *Journal of Financial Econometrics* 22(1), 224–251 (2024), DOI 10.1093/jjfinec/nbac034. Their BTC/ETH CEX and Uniswap study reports weekday, hourly and within-hour periodicity in volatility and volume. It motivates seasonal controls, not a ready-made direction signal.
3. Takaishi, “Multifractality and sample size influence on Bitcoin volatility patterns,” arXiv:2511.03314 (November 2025, preprint). Its abstract reports finite-sample/sampling-interval effects in Bitcoin realized-volatility Hurst estimates and weaker multifractality in realized volatility than in returns. This motivates frequency-specific finite-size checks.

## Data contract

- Primary series: Binance Spot BTCUSDT 5m OHLCV, with UTC open and close timestamps, venue and quote currency preserved.
- Separate replication series: Binance USDⓈ-M BTCUSDT perpetual 5m bars. Never splice Spot and Perpetual rows or use a futures signal as if it were spot data.
- Prefer 90 days of continuous data; 28 days is exploratory only. A 5m hour-of-week has 2,016 phase cells, so short samples leave too few repeats per cell. Store raw responses and retrieval timestamps immutably.
- Exclude forming candles. Reject duplicate/out-of-order timestamps, gaps, invalid OHLCV, unknown timezone, stale tail bars and venue/contract changes.
- For one-minute boundary or queue/order-book claims, obtain trade or depth data. Five-minute klines cannot resolve within-bar microstructure at one-minute resolution.

## Features (computed causally)

- UTC hour-of-week (168 categories) and weekday/hour components.
- Five-minute phase within hour (12 categories) and quarter-hour phase (0, 5, 10 minutes within each 15-minute block).
- Boundary indicators for bars opening on UTC minute 00/15/30/45, with a separate indicator for other five-minute opens.
- Log volume, quote volume, trade count and taker-buy fraction, standardized only with trailing training-window statistics.
- Realized volatility and absolute returns by phase. Keep signed return, volatility, volume and taker-buy outcomes separate.

Do not use future bar highs/lows, revised headlines or later-arriving features. For every feature, record event time, publication time and first-available time.

## Baselines and ablations

1. Random walk / zero-return baseline.
2. Volatility-aware baseline with no clock features.
3. Seasonal-naive baseline: trailing median/mean for the matching UTC hour-of-week or coarser phase, with shrinkage toward the global mean.
4. Existing 5m challengers without seasonal features.
5. The same challengers plus phase features.

Use a nested ablation: hour-of-week only; + quarter-hour/five-minute phase; + volume/taker features; + multifractal diagnostics. No phase feature is promoted if it helps only in-sample or disappears after the volatility-aware baseline.

## Validation and falsification

- Expanding/rolling chronological walk-forward; no random time shuffling.
- Use identical issue times, cutoffs, venues and horizons for all models. Evaluate the frozen 24 hourly target path; keep separate 1h/4h/24h summaries.
- Use non-overlapping daily origins for the primary leaderboard. Purge overlapping target windows where additional intraday origins are analyzed.
- Primary forecast loss remains the tournament's normalized MAE of hourly log-price forecasts. Secondary outcomes: directional accuracy, volatility loss (e.g. QLIKE where appropriate), pinball/interval score and empirical coverage.
- Use block bootstrap or another dependence-aware uncertainty method; correct for testing multiple phase bins/features. Report effective sample size, not just raw rows.
- Use representation-appropriate nulls. IAAFT is not a universal null for discrete transition-count encodings; preserve within-bar constraints when testing OHLC-derived states.
- Replicate on Spot and Perpetual independently. A result that exists only in one venue or one time window is a regime-specific observation, not a universal rule.

## Decision rule

Keep all phase features diagnostic until a pre-registered walk-forward ablation improves the primary score over both random walk and the volatility-aware/seasonal-naive controls with uncertainty intervals excluding a trivial effect and no critical leakage. Do not award research points from descriptive seasonality alone. Do not promote a champion before 30 completed daily forecast vintages.

## Current blocker

The available browser-rendered Spot 5m page exposed only 40 rows and did not state its timezone; the latest row appeared to be forming. The official Binance raw API response was not accessible in this run. This is insufficient for the 300-bar prototype gate and far below the preferred 90-day seasonal sample. No forecast was issued.

## Sources

- https://arxiv.org/abs/2607.09426
- https://doi.org/10.1093/jjfinec/nbac034
- https://arxiv.org/abs/2511.03314
- https://github.com/binance/binance-spot-api-docs/blob/master/faqs/market_data_only.md
