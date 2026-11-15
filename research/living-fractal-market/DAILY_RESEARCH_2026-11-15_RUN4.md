# Living Fractal Market — daily research report (run 4)

**Date:** 2026-11-15  
**Review time:** 2026-11-15 08:33 UTC  
**Branch:** [research/living-fractal-market](https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market)  
**Scope:** research branch only; `main` untouched.

## 1. Branch and daily workflow state

At review start, branch comparison showed **113 commits ahead of main, 0 behind**. The daily marker already existed for today (`lfm-daily-20261115-0804z-r5`), and the forecast, evaluation and archive records for the day were already present. This run therefore reviewed and verified the existing daily run instead of writing a second marker and generating duplicate overlapping vintages.

- Forecast run: [43693158620](https://github.com/messerzai/ambivikhry-agent/actions/runs/43693158620), source checkout commit `10c8f7033a88ecb5533781e36144cf718d9997ec`.
- Evaluation run: [43694193141](https://github.com/messerzai/ambivikhry-agent/actions/runs/43694193141).
- Forecast job: all steps completed successfully; 11/11 offline unit tests passed; live Binance public-data retrieval passed; forecast JSON generation passed; artifact upload passed.
- Evaluation job: evaluation tests, matured-vintage evaluation and artifact upload passed.
- Canonical forecast artifact ID: `14153835047`; SHA-256 `4f9af1f7dc4dd9bc9b47feaa91f8b27b33e302bf36f45d3f76491e001b488731`.
- Extracted JSON SHA-256: `58663b5a5b7c76931bdbd3aab41941a1cf09f792795961b0f25bc95dbff5ff8c`.
- The downloaded ZIP and extracted JSON hashes were independently verified against the ledger.

## 2. Research discoveries

- **Cho et al. (2026-10-29, Frontiers in Physics):** MF-DFA should be tested against shuffled, phase-randomized and IAAFT surrogates, with finite-size bands, q sensitivity and crossover uncertainty. This is a peer-reviewed Perspective, not a BTC forecast.
- **Wafi et al. (2026-10-26, Digital Finance):** daily Bitcoin volatility accuracy is regime-dependent; nested sentiment/blockchain information sets and GARCH–LSTM hybrids do not have a universal winner. The target is daily volatility, not hourly price.
- **Raffaelli et al. (2026-04-17, Decisions in Economics and Finance):** multivariate Hawkes + base-imbalance/continuous-time modeling can forecast next BTC/USD LOB event timing/sign. This requires LOB event streams and is not a 24h price-path model.
- **Mukherjee et al. (2026-09-19, arXiv preprint):** sentiment-augmented POMP with Student-t noise is a candidate volatility-state model, but the reported evidence is likelihood/filter fit rather than leakage-safe H24 price forecasts.

Sources: [Cho et al.](https://doi.org/10.3389/fphy.2026.2026031), [Wafi et al.](https://doi.org/10.1007/s42521-026-00229-9), [Raffaelli et al.](https://doi.org/10.1007/s10203-026-00570-z), [Mukherjee et al.](https://arxiv.org/abs/2609.23250).

## 3. Competitor watchlist

Added:
- [MultivariateHawkesLOB](https://github.com/Learning2Control/MultivariateHawkesLOB) — GPL-3.0, LOB event-time model; no code copied.
- [Wafi regime-dependent volatility project](https://github.com/Wafi-Finance/Regime-Dependent-Bitcoin-Volatility-Forecasting) — daily volatility, rolling QLIKE; repo has no LICENSE, no code/data copied.
- [Sentiment POMP project](https://github.com/abeyankargiridharan/Novel_Approach_to_Volatility_Analysis_on_Bitcoin_Returns) — daily BTC/FGI volatility state; repo has no LICENSE, no code/data copied.
- [BTC TimesFM forward experiment](https://github.com/artur-fedosiuk/btc-prediction-timesfm) — BTC/USD H24 design, but README says first live forward forecast is not yet verified. Repository code Apache-2.0; TimesFM 3.0 weights are separately non-commercial/non-production. No comparable external score admitted.

## 4. Latest verified 24h challenger forecast

**This is not a validated BTC/USD champion forecast.** It is the latest archived challenger: Binance Spot BTC/USDT, 5m input bars, hourly target grid, model `LFM-5m-Downside-Aware-Council-0.4`.

- Issue UTC: `2026-11-15T08:09:18.020362Z`
- Data cutoff UTC: `2026-11-15T08:04:59.999000Z` (258.0 seconds before issue)
- Source: https://data-api.binance.vision/api/v3/klines
- Reference: **64,078.57 USDT**
- Closed inputs: **999 × 5m** (83.25 hours of history)
- Target opens: `2026-11-15T09:00:00Z` through `2026-11-16T08:00:00Z`
- Models: RandomWalk, Momentum5m, MeanReversion5m, VolatilityRegime5m, TakerFlow5m, DownsideStress5m, LFM5mEnsemble.
- Gaussian-style P90 ranges are uncalibrated; no calibrated 50%/90% interval is available.

| Target UTC | RandomWalk | Momentum | MeanRev | VolRegime | TakerFlow | DownsideStress | LFM ensemble |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-15 09:00 | 64078.57 | 63977.41 | 64078.89 | 64018.81 | 64074.02 | 63895.25 | 64031.98 |
| 2026-11-15 10:00 | 64078.57 | 63894.70 | 64079.51 | 63967.32 | 64070.98 | 63722.32 | 63992.80 |
| 2026-11-15 11:00 | 64078.57 | 63827.07 | 64080.37 | 63923.00 | 64068.94 | 63559.17 | 63959.86 |
| 2026-11-15 12:00 | 64078.57 | 63771.74 | 64081.46 | 63884.89 | 64067.57 | 63405.21 | 63932.17 |
| 2026-11-15 13:00 | 64078.57 | 63726.49 | 64082.74 | 63852.17 | 64066.65 | 63259.92 | 63908.89 |
| 2026-11-15 14:00 | 64078.57 | 63689.46 | 64084.20 | 63824.12 | 64066.03 | 63122.79 | 63889.33 |
| 2026-11-15 15:00 | 64078.57 | 63659.16 | 64085.81 | 63800.13 | 64065.62 | 62993.35 | 63872.92 |
| 2026-11-15 16:00 | 64078.57 | 63634.36 | 64087.56 | 63779.65 | 64065.35 | 62871.14 | 63859.15 |
| 2026-11-15 17:00 | 64078.57 | 63614.06 | 64089.43 | 63762.22 | 64065.16 | 62755.75 | 63847.63 |
| 2026-11-15 18:00 | 64078.57 | 63597.45 | 64091.40 | 63747.44 | 64065.04 | 62646.80 | 63838.00 |
| 2026-11-15 19:00 | 64078.57 | 63583.85 | 64093.47 | 63734.96 | 64064.95 | 62543.91 | 63829.97 |
| 2026-11-15 20:00 | 64078.57 | 63572.72 | 64095.62 | 63724.48 | 64064.90 | 62446.73 | 63823.29 |
| 2026-11-15 21:00 | 64078.57 | 63563.61 | 64097.84 | 63715.72 | 64064.86 | 62354.94 | 63817.76 |
| 2026-11-15 22:00 | 64078.57 | 63556.15 | 64100.12 | 63708.47 | 64064.84 | 62268.24 | 63813.20 |
| 2026-11-15 23:00 | 64078.57 | 63550.05 | 64102.46 | 63702.52 | 64064.82 | 62186.33 | 63809.46 |
| 2026-11-16 00:00 | 64078.57 | 63545.05 | 64104.85 | 63697.71 | 64064.81 | 62108.95 | 63806.42 |
| 2026-11-16 01:00 | 64078.57 | 63540.95 | 64107.29 | 63693.89 | 64064.80 | 62035.84 | 63803.96 |
| 2026-11-16 02:00 | 64078.57 | 63537.60 | 64109.76 | 63690.92 | 64064.79 | 61966.76 | 63802.00 |
| 2026-11-16 03:00 | 64078.57 | 63534.86 | 64112.27 | 63688.69 | 64064.79 | 61901.49 | 63800.47 |
| 2026-11-16 04:00 | 64078.57 | 63532.62 | 64114.81 | 63687.11 | 64064.79 | 61839.80 | 63799.29 |
| 2026-11-16 05:00 | 64078.57 | 63530.78 | 64117.38 | 63686.10 | 64064.79 | 61781.51 | 63798.42 |
| 2026-11-16 06:00 | 64078.57 | 63529.27 | 64119.97 | 63685.57 | 64064.79 | 61726.41 | 63797.80 |
| 2026-11-16 07:00 | 64078.57 | 63528.04 | 64122.58 | 63685.47 | 64064.79 | 61674.34 | 63797.40 |
| 2026-11-16 08:00 | 64078.57 | 63527.03 | 64125.20 | 63685.73 | 64064.79 | 61625.13 | 63797.19 |

The 70,000 USDT threshold was already above the reference by 8.46% at issue. The emitted heuristic value of 1.0 is explicitly uncalibrated and refers to terminal price below a level that was already breached; it is not a new downward-crossing probability. The -6% shock is illustrative only.

## 5. Evaluation and leaderboard

Four matured vintages were evaluated. LFM5mEnsemble nMAE: 9.4641 (Nov 12), 1.8265 (Nov 13 08:07), 1.7186 (Nov 13 07:59), 5.5006 (Nov 14). It beat random walk and the volatility-aware baseline in 2/4 vintages and lost in 2/4. The two Nov 13 vintages overlap by about 23 hours; horizons inside a vintage are also dependent. No interval calibration is established.

- Completed vintages: 4; pending: 2 (Nov 15 07:37 and 08:09 issues).
- P90 calibrated: no.
- Virtual points: **0**.
- Champion promotion: not eligible; 30 completed daily vintages required.
- External leaderboard: no comparable live competitor forecasts.

## 6. License audit

No code, weights, datasets, tokenizers, LOB event data, social posts or paid APIs were copied. Hawkes LOB repo GPL-3.0; Wafi and POMP code repositories have no LICENSE in the inspected root; TimesFM 3.0 weights are non-commercial/non-production; TimesFM 2.5 model card states Apache-2.0. Article CC BY licenses do not automatically license separately hosted code/data.

## 7. Data-quality warnings and next experiment

- Forecast JSON omits explicit `input_interval`, `model_commit`, `vintage_id` and separate `retrieved_at_utc`; ledger supplies some but the artifact should be self-describing.
- 999 five-minute bars provide only 83.25 hours, far below the preferred 90-day seasonality sample.
- BTC/USDT is not BTC/USD; 5m OHLCV is not a substitute for L2 order-book events.
- No model promotion, calibrated intervals, trading or order execution.

Next: add explicit provenance fields with tests; then build a paginated immutable 90-day Spot 5m dataset and evaluate seasonal/volatility-aware controls before any fractal, sentiment or news ablation.
