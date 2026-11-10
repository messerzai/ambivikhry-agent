# Forecasting Tournament — Bitcoin 24h / hourly

This is the forecasting and self-improvement protocol for the Living Fractal Market research branch.

## Objective

The current champion model must publish a timestamped forecast for the next 24 hours of BTC/USD, with one forecast point per hour (hours +1 through +24). Forecasts are evaluated only after the corresponding market data becomes available. A model earns **research reward points** when it beats the agreed baselines under the scoring rules below. Rewards are virtual benchmark points and promotion in the model tournament—not money, tokens, or permission to trade.

## Forecast contract

Every forecast record must include:
- issue timestamp in UTC and exact data cutoff;
- asset and price source / venue or documented composite;
- reference price at issue time;
- 24 hourly target timestamps and predicted BTC/USD prices;
- preferably 50% and 90% prediction intervals for each hour;
- model name, version, code commit, feature set and training-data cutoff;
- short explanation of dominant signals and uncertainty;
- missing-data / outage flags.

The model must not silently revise a forecast after issue. Corrections are separate, versioned records. Forecasts are stored append-only so evaluation cannot be gamed.

## Evaluation and reward

For each completed forecast:
1. Align each prediction to the first valid hourly close at or after its target timestamp, using the declared price source.
2. Calculate MAE and sMAPE/WAPE for price levels, plus MAE for log returns. State denominator conventions and handle near-zero values safely.
3. Score directional accuracy for each hourly return relative to the issue-time reference and previous forecast hour.
4. Score interval coverage and sharpness for 50% / 90% intervals; use a proper interval or quantile score so excessively wide intervals are not rewarded.
5. Compare with at least: (a) random-walk / last-price baseline, (b) drift-free return baseline, and (c) a simple volatility-aware baseline.
6. Aggregate results over non-overlapping daily forecast vintages and report all horizons separately (1h…24h), plus an overall score.

**Reward rule:** award 1 virtual point for a forecast vintage that beats the random-walk baseline on pre-registered primary loss, while maintaining calibrated intervals and no critical data leakage. Award an additional 1 point if it also beats the strongest simple baseline. Deduct no points for honest abstention due to missing or corrupted data; record abstentions separately. A model that wins must do so over a minimum of 30 completed daily vintages before it can become champion. Use a rolling leaderboard and show sample size and confidence intervals; do not crown a winner from one lucky day.

Primary loss: normalized MAE of hourly log-price forecasts averaged over 24 horizons. Direction and interval metrics are secondary gates, not substitutes. Freeze scoring definitions before the test period. Report uncertainty and use paired comparisons / bootstrap confidence intervals where feasible.

## Version tournament and self-improvement

- Keep a stable champion and isolated challengers. Never overwrite the champion merely because a challenger has a lower in-sample error.
- Every proposed improvement must have a hypothesis, code diff, data provenance, tests, and a reproducible experiment record.
- Candidate changes may include rolling multifractal features, MF-DFA/MFCCA stability diagnostics, news surprise, validated sentiment, attention, order-book/liquidity features, regime detection and uncertainty calibration.
- Use chronological train/validation/test splits and walk-forward evaluation. Purge overlapping labels where needed. No random shuffling across time.
- Track data leakage, survivorship bias, exchange outages, fees/slippage where relevant, timestamp alignment, look-ahead in news feeds, and model drift.
- Run ablations to determine whether fractal, news or sentiment features add value beyond simpler baselines.
- Keep a changelog and preserve the last known-good champion. If a candidate fails tests or degrades out-of-sample results, reject or roll it back.
- Never optimize against the leaderboard's holdout period. Rotate or seal holdout windows and retain a final untouched test set.

## Daily report

Publish:
- latest 24-hour hourly forecast and issue timestamp;
- prior forecast's realized score and baseline comparison;
- leaderboard, virtual points and number of completed vintages;
- confidence / interval calibration;
- data-quality warnings and known limitations;
- what changed in the model, what evidence supports it, and whether the champion changed.

## Safety and interpretation

This is an experimental research system, not financial advice or a reliable trading signal. Forecasts are probabilistic estimates and can be wrong, especially during abrupt news, low liquidity or exchange disruptions. Never place trades, move funds, or connect execution keys as part of this research. Do not imply causality from correlation. Clearly label forecasts as research outputs, not certainty.

## Acceptance criteria for the first implementation

- reproducible BTC hourly data pipeline with UTC timestamps and source documentation;
- append-only forecast ledger;
- champion + challenger interface and frozen baselines;
- 24 hourly point forecasts with uncertainty intervals;
- evaluation script implementing the pre-registered metrics;
- tests for timestamp alignment, missing bars, duplicate records and leakage;
- report showing a forecast only when the input data passes quality checks.
