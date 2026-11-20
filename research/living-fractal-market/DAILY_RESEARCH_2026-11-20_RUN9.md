# Daily research report — 2026-11-20 (run 9)

Branch: https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market

## Run and repository status

- The branch-isolated 5m forecast workflow succeeded: https://github.com/messerzai/ambivikhry-agent/actions/runs/44698772741. Source commit: `84769fbae8468196f2f0f9bd3e8fc69ce7c583ab`.
- The initial evaluation workflow ran at 07:57:33Z, before the Nov 19 vintage's final target candle had closed, so it correctly left that vintage pending: https://github.com/messerzai/ambivikhry-agent/actions/runs/44698772822.
- Added two regression tests for the evaluation boundary: no actual-data fetch before the final target close, and evaluation becomes eligible immediately after it. Test commit: https://github.com/messerzai/ambivikhry-agent/commit/513b36c6f5841de775450fd434afc78e107979cf.
- The follow-up evaluation succeeded at 08:08:04.720Z: https://github.com/messerzai/ambivikhry-agent/actions/runs/44700118376. It evaluated the Nov 19 vintage after the exact final close `2026-11-20T07:59:59.999Z`; Nov 20 remains pending.
- The archiver succeeded and committed the exact evaluation artifact: https://github.com/messerzai/ambivikhry-agent/actions/runs/44700118369. Archive commit: https://github.com/messerzai/ambivikhry-agent/commit/efe118f102f5d714bd39e71d177b2f2cf3d647b1.
- General project tests passed on Python 3.10, 3.11, 3.12 and 3.13: **54 passed** on each runtime. The 5m council ran **13/13** unit tests; the evaluation workflow ran **13/13**; the archiver ran **12/12**.
- Documentation commits: ledger status https://github.com/messerzai/ambivikhry-agent/commit/5990ecfb29117753498a83cb03576742bad94654; competitor update https://github.com/messerzai/ambivikhry-agent/commit/f4abd46f2aea6e8743c05aae59ab5283a24a0600; license audit https://github.com/messerzai/ambivikhry-agent/commit/72a1c1336ea8221ebf7a39c5dd246eb40dc84b0e.

## Fresh 5-minute input and diagnostics

- **Asset / venue / quote:** BTC/USDT, Binance Spot, USDT. **Input interval:** 5m. **Target interval:** hourly closes. This is a challenger, not a BTC/USD champion.
- **Issue:** `2026-11-20T07:57:36.065378Z`; **retrieved:** `2026-11-20T07:57:36.060900Z`; **last closed input cutoff:** `2026-11-20T07:54:59.999Z`.
- **Reference:** 61,838.54 USDT. **Input count:** 999 closed 5m candles = 83h15m. The workflow quality gates and tests passed.
- The archived artifact does **not** include the raw 999-row 5m response. Therefore this report can show the exact model outputs and aggregate diagnostics, but cannot reproduce or display every individual 5m OHLCV candle. There is no raw-input SHA-256 for this vintage. This is the main data-provenance gap to fix next.

Signal diagnostics (all computed from data available by the cutoff):

| Diagnostic | Value | Interpretation / caution |
|---|---:|---|
| Fast 1h log-return signal | +0.0934% | Short-term component positive. |
| Medium 4h log-return rate | −0.00325%/h | Slightly negative. |
| Slow 12h log-return rate | −0.03185%/h | Negative medium/slow component; signs are mixed. |
| Volatility ratio | 0.799 | Recent volatility estimate below the longer reference window. |
| Taker-buy imbalance | −0.2042 | Spot taker flow leaned toward sells; this is not full order-book imbalance. |
| Relative quote volume (1h) | 1.163 | About 16.3% above the model's reference average. |
| Drawdown from 24h high | −3.461% | Price remains below the recent 24h high. |
| Hourly sigma estimate | 0.6899% | Point-in-time scale used by this challenger. |
| Downside momentum rate | −0.2930%/h | Stress feature, not a deterministic forecast. |

The `70,000 USDT` stress level is already above the 61,838.54 USDT reference. The model's `1.0` heuristic is an uncalibrated terminal-below-level state estimate, not a 100% probability of a new downward crossing. The 6% shock path is illustrative, not a forecast.

## Current +1…+24 hourly point forecasts

Vintage: `lfm5m-2026-11-20T07:57:36.065378Z-BTCUSDT-binance-spot-council-0.4`. Model version: `LFM-5m-Downside-Aware-Council-0.4`. Immutable model commit: `84769fbae8468196f2f0f9bd3e8fc69ce7c583ab`. Targets: 2026-11-20 08:00Z through 2026-11-21 07:00Z.

All values below are point estimates in USDT; timestamps are UTC. The Gaussian-style P90 ranges are **not calibrated** and no calibrated 50% interval is available.

| Target UTC | RandomWalk | Momentum5m | MeanReversion5m | VolatilityRegime5m | TakerFlow5m | DownsideStress5m | LFM5mEnsemble |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-20 08:00 | 61,838.54 | 61,856.40 | 61,838.65 | 61,849.57 | 61,833.40 | 61,771.49 | 61,845.32 |
| 2026-11-20 09:00 | 61,838.54 | 61,871.02 | 61,838.85 | 61,859.22 | 61,829.95 | 61,708.13 | 61,851.25 |
| 2026-11-20 10:00 | 61,838.54 | 61,882.99 | 61,839.14 | 61,867.69 | 61,827.64 | 61,648.26 | 61,856.43 |
| 2026-11-20 11:00 | 61,838.54 | 61,892.80 | 61,839.50 | 61,875.12 | 61,826.10 | 61,591.68 | 61,860.93 |
| 2026-11-20 12:00 | 61,838.54 | 61,900.83 | 61,839.92 | 61,881.66 | 61,825.06 | 61,538.20 | 61,864.83 |
| 2026-11-20 13:00 | 61,838.54 | 61,907.40 | 61,840.41 | 61,887.44 | 61,824.36 | 61,487.65 | 61,868.22 |
| 2026-11-20 14:00 | 61,838.54 | 61,912.78 | 61,840.94 | 61,892.55 | 61,823.90 | 61,439.87 | 61,871.15 |
| 2026-11-20 15:00 | 61,838.54 | 61,917.19 | 61,841.52 | 61,897.08 | 61,823.59 | 61,394.71 | 61,873.69 |
| 2026-11-20 16:00 | 61,838.54 | 61,920.80 | 61,842.14 | 61,901.12 | 61,823.38 | 61,352.02 | 61,875.89 |
| 2026-11-20 17:00 | 61,838.54 | 61,923.76 | 61,842.80 | 61,904.73 | 61,823.24 | 61,311.67 | 61,877.81 |
| 2026-11-20 18:00 | 61,838.54 | 61,926.18 | 61,843.48 | 61,907.96 | 61,823.14 | 61,273.52 | 61,879.47 |
| 2026-11-20 19:00 | 61,838.54 | 61,928.16 | 61,844.20 | 61,910.88 | 61,823.08 | 61,237.45 | 61,880.93 |
| 2026-11-20 20:00 | 61,838.54 | 61,929.78 | 61,844.93 | 61,913.52 | 61,823.04 | 61,203.35 | 61,882.21 |
| 2026-11-20 21:00 | 61,838.54 | 61,931.11 | 61,845.69 | 61,915.92 | 61,823.01 | 61,171.12 | 61,883.33 |
| 2026-11-20 22:00 | 61,838.54 | 61,932.19 | 61,846.47 | 61,918.12 | 61,822.99 | 61,140.64 | 61,884.32 |
| 2026-11-20 23:00 | 61,838.54 | 61,933.08 | 61,847.26 | 61,920.14 | 61,822.98 | 61,111.82 | 61,885.20 |
| 2026-11-21 00:00 | 61,838.54 | 61,933.81 | 61,848.07 | 61,922.00 | 61,822.97 | 61,084.57 | 61,885.98 |
| 2026-11-21 01:00 | 61,838.54 | 61,934.41 | 61,848.89 | 61,923.74 | 61,822.96 | 61,058.80 | 61,886.69 |
| 2026-11-21 02:00 | 61,838.54 | 61,934.90 | 61,849.72 | 61,925.35 | 61,822.96 | 61,034.44 | 61,887.33 |
| 2026-11-21 03:00 | 61,838.54 | 61,935.30 | 61,850.56 | 61,926.87 | 61,822.95 | 61,011.40 | 61,887.91 |
| 2026-11-21 04:00 | 61,838.54 | 61,935.63 | 61,851.41 | 61,928.31 | 61,822.95 | 60,989.62 | 61,888.45 |
| 2026-11-21 05:00 | 61,838.54 | 61,935.89 | 61,852.27 | 61,929.67 | 61,822.95 | 60,969.02 | 61,888.94 |
| 2026-11-21 06:00 | 61,838.54 | 61,936.11 | 61,853.14 | 61,930.97 | 61,822.95 | 60,949.54 | 61,889.40 |
| 2026-11-21 07:00 | 61,838.54 | 61,936.29 | 61,854.01 | 61,932.22 | 61,822.95 | 60,931.12 | 61,889.83 |

At +24, the non-stress model paths span 61,822.95–61,936.29 USDT (−0.025% to +0.158% vs reference). The downside stress challenger is the clear outlier at 60,931.12 USDT (−1.467%). The LFM ensemble point is 61,889.83 USDT (+0.0829%); its approximate P90-style band is 58,543.28–65,427.68 USDT, uncalibrated. This is not a BTC/USD forecast and not a trading recommendation.

## Previous-vintage evaluation

Nov 19 issue vintage: `lfm5m-2026-11-19T07:23:19.072262Z-BTCUSDT-binance-spot-council-0.4`. Its last target candle closed at `2026-11-20T07:59:59.999Z`; the second evaluation run scored it at `2026-11-20T08:08:04.720Z`.

| Model | Normalized log-price MAE | Direction vs issue | Hour-to-hour direction | P90 empirical coverage |
|---|---:|---:|---:|---:|
| MeanReversion5m | 2.861415 | 0.750 | 0.583 | 1.000 |
| DownsideStress5m | 2.962922 | 0.750 | 0.583 | 1.000 |
| VolatilityRegime5m | 2.991031 | 0.625 | 0.625 | 1.000 |
| TakerFlow5m | 3.006664 | 0.750 | 0.375 | 1.000 |
| RandomWalk | 3.011131 | 0.000 | 0.000 | 1.000 |
| LFM5mEnsemble | 3.058590 | 0.250 | 0.500 | 1.000 |
| Momentum5m | 3.186165 | 0.250 | 0.417 | 1.000 |

Baselines: RandomWalkLastPrice nMAE 3.011131; VolatilityCappedSlowDrift nMAE 5.785064. MeanReversion5m beat both point baselines on this one vintage. P90 empirical coverage was 100%, but the forecast intervals are explicitly uncalibrated; this is not evidence of calibrated coverage. Virtual points: **0**. Evaluation ZIP SHA-256 `467f7a377006d15cadf5fd46288ccd7424e3ab5350376c170b8eab991f1d195c`; evaluation JSON SHA-256 `f96f19fdf540b08ada5d032ee3d3a6566ef1da10befe0adca41271a91c042b71`; actual hourly response SHA-256 `e3fe63bab235a6baa3f0d70dcd4eddac5d41c89de7de1c1e2c0ca97a402ca8ad`.

## Research discoveries

1. **Bitcoin multifractality:** Choi (2026), *Physica A* 697, 131735, reports 774k five-minute BTC observations (2017–2024), q-Gaussian rescaling, a roughly 25-day scaling crossover and a post-ETF reduction in its Market Deficiency Measure. This supports testing scale-dependent diagnostics, not the claim that markets are literally non-repeating or that multifractality predicts the next hour. Abstract-level source: https://doi.org/10.1016/j.physa.2026.131735.
2. **Higher moments and activity:** Karagiorgis & Ballis (2026) report time-varying skewness–kurtosis curvature and an association between abnormal activity and kurtosis, especially in futures. This is useful for risk-state monitoring, not causal or directional prediction: https://doi.org/10.1002/fut.70117.
3. **News surprise × sentiment:** Huynh (2026) finds that bullish sentiment moderates the high-frequency response to macro announcements across the top 100 crypto assets (about −16% return response and −24% turnover response per SD). This motivates event-time interaction tests, but not a generic sentiment score; TRMI data rights and timestamp alignment are prerequisites: https://doi.org/10.1016/j.jbef.2026.101183.
4. **Attention vs polarity:** Akbar (2026) reports no return predictability from polarity/hype/anxiety, while attention is associated with conditional variance and appears to respond to price shocks. This argues against adding raw sentiment polarity as a direction feature: https://doi.org/10.1108/SEF-12-2025-0942.
5. **Foundation models in finance:** The June 2026 arXiv benchmark finds TSFMs win 8/10 daily-equity task rankings, but only two one-sided DM improvements are significant; local iTransformer wins both META tasks. Five equities and a 20-business-day horizon do not transfer directly to BTC hourly: https://arxiv.org/abs/2606.27100.
6. **Preprint date caution:** Pontiggia's arXiv record and manuscript title page disagree on date (2025-07 vs 2026-07). It remains a preprint; its multifractal claims are not treated as settled evidence until the version history is resolved: https://arxiv.org/abs/2507.00575.

## Competitor and license watch

- Added Moirai-2.0-R-Small as a probabilistic challenger. The Uni2TS code is Apache-2.0, but the official model weights are CC-BY-NC-4.0; do not use those weights in a commercial/production product. No code or weights were reused.
- Chronos-2 code and model card list Apache-2.0; TimesFM 2.5 code/weights list Apache-2.0; TimesFM 3.0 code is Apache-2.0 but its weights use a separate non-commercial/non-production license. All remain candidates, not executed competitors.
- No external forecaster supplied a comparable timestamped BTC/USD 24-step hourly price path. External point-price leaderboard remains empty.
- No third-party code, weights, datasets, social posts, order-book records or paid API outputs were copied.

## Internal leaderboard and points

- **12 archived forecast vintages; 11 evaluated; 1 pending.** The 24 hourly targets within each vintage are dependent; some daily vintages overlap.
- **0 virtual research points**. No P90 calibration, no 30 non-overlapping completed vintages, no champion promotion.
- Recent winners: TakerFlow5m on one Nov 17 vintage; RandomWalk/DownsideStress tie on the overlapping Nov 17 vintage; MeanReversion5m on Nov 18 and Nov 19. The winner changes with issue time and regime.

## Next experiment

1. Modify the next 5m workflow version to archive the exact raw Binance response bytes, a SHA-256, and the request URL alongside the forecast. Add tests that the raw snapshot hashes to the archived bytes and its last candle matches the declared cutoff. This is the highest-priority provenance patch.
2. Extend the 5m history from 999 bars (~3.5 days) to at least 90 days via pagination, then assess MF-DFA/MFCCA with q/scales, finite-size checks, shuffled/phase-randomized/IAAFT nulls and block bootstrap. Do not claim a multifractal regime from the current short window.
3. Add Chronos-2 and TimesFM-2.5 as fixed-revision challengers on the same non-overlapping origins and compare to RandomWalk/volatility-aware baselines. Keep Moirai-2.0 weights out of commercial/production work under the current CC-BY-NC-4.0 terms.
4. Only after point-in-time data rights are verified, test macro-news surprise × sentiment interactions as a separate ablation against the same baselines.

Research only; not financial advice. No trades, order execution or transfers.