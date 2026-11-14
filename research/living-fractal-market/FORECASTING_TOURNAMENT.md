# Forecasting Tournament — Bitcoin 24h / hourly

This is the forecasting and self-improvement protocol for the Living Fractal Market research branch.

## Objective

The current champion model must publish a timestamped forecast for the next 24 hours of BTC/USD, with one forecast point per hour (hours +1 through +24). Forecasts are evaluated only after the corresponding market data becomes available. A model earns research reward points when it beats the agreed baselines under the scoring rules below. Rewards are virtual benchmark points and promotion in the model tournament—not money, tokens, or permission to trade.

## Forecast contract

Every forecast record must include:
- issue timestamp in UTC and exact data cutoff;
- asset and price source / venue or documented composite;
- reference price at issue time;
- 24 hourly target timestamps and predicted prices in the declared quote currency;
- preferably 50% and 90% prediction intervals for each hour;
- model name, version, code commit, feature set and training-data cutoff;
- short explanation of dominant signals and uncertainty;
- missing-data / outage flags.

The model must not silently revise a forecast after issue. Corrections are separate, versioned records. Forecasts are stored append-only so evaluation cannot be gamed.

## Evaluation and reward

For each completed forecast:

1. Align each prediction to the hourly candle whose open timestamp exactly equals the forecast target timestamp. Score that candle's close from the declared venue and quote currency. Do not silently substitute a different venue, quote currency or nearest bar.
2. Calculate price-level MAE and sMAPE/WAPE as descriptive secondary metrics. The primary metric is normalized MAE of hourly log-price forecasts:
   - raw log MAE = mean over h=1…24 of abs(log(predicted_close_h) - log(actual_close_h));
   - nMAE = raw log MAE / sigma_hour;
   - sigma_hour is the point-in-time hourly_sigma_estimate frozen in the original forecast diagnostics at issue time. It must not be recomputed from target-period outcomes. If it is absent, non-finite or non-positive, report raw log MAE but mark the primary score unavailable.
3. Report directional accuracy in two forms: sign of each predicted/actual price change relative to the issue-time reference, and sign of each hour-to-hour change relative to the preceding forecast/actual close.
4. Report empirical P50/P90 interval coverage and mean interval width when those quantiles exist. Intervals are not considered calibrated merely because a model labels them P50 or P90. Calibration must be demonstrated on prior chronological vintages. Use proper interval/quantile scores when the required quantiles exist.
5. Compare with at least:
   - RandomWalkLastPrice: reference price repeated at all 24 horizons;
   - DriftFreeReturn: equivalent zero-return / last-price point path;
   - VolatilityCappedSlowDrift: drift = clip(slow_12h_log_return_per_hour, -0.25*sigma_hour, +0.25*sigma_hour); point_h = reference * exp(drift*h); a descriptive P90 envelope is point_h * exp(±1.64485362695*sigma_hour*sqrt(h)). The drift and sigma must come from the frozen issue-time diagnostics. This is a simple control, not a market-implied distribution or calibrated interval.
6. Aggregate only over non-overlapping daily forecast vintages. Report every horizon, overall loss, sample size and uncertainty. The 24 horizons within one vintage are serially dependent and are not 24 independent daily samples.

**Reward rule:** award 1 virtual point for a forecast vintage that beats RandomWalkLastPrice on the pre-registered primary loss, while maintaining calibrated intervals and no critical data leakage. Award an additional 1 point if it also beats the strongest simple baseline. Uncalibrated intervals make a vintage ineligible for points even when its point loss is lower. Honest abstention due to missing or corrupted data receives no penalty; record abstentions separately. A model must win over at least 30 completed, non-overlapping daily vintages before it can become champion. Use paired comparisons and bootstrap confidence intervals where feasible; do not crown a winner from one lucky day.

Freeze scoring definitions before the test period. Do not normalize by realized target-period volatility or any other target-period quantity. Report the exact denominator and source for every score.

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
