# Daily research report — 2026-11-25 (run 13)

## Branch and commits

- Branch: [`research/living-fractal-market`](https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market)
- Daily trigger commit: [`80a4707`](https://github.com/messerzai/ambivikhry-agent/commit/80a4707c3ee376c796d2aa0df565e3237f9c7e2e) — marker `lfm-daily-20261125-0754z-r13-c91d`; no second marker update was made.
- Research/code patch: [`4852b85`](https://github.com/messerzai/ambivikhry-agent/commit/4852b85010fb32241fc0315a00943690c6a9572a).
- Exact artifact/evaluation archive commit: [`cbe6271`](https://github.com/messerzai/ambivikhry-agent/commit/cbe627141bcf035e13c6d71500227a23afe273b6).
- `main` was not modified; all changes remain on the research branch.

## Research discoveries

**Facts**

1. Zeri's 2026-11-01 research note on zero-shot time-series foundation models evaluates *realised variance*, not price levels. Its BTC/ETH design uses 5m returns, hourly RV horizons 1h/4h/24h, 4,866 origins per asset spaced five hours apart, calendar-adjusted HAR/log-HAR, QLIKE, DM-HLN, BH-FDR and a 90% model confidence set. The note reports calendar adjustment improving hourly HAR QLIKE by 8–25%; TSFMs alone beating adjusted HAR by 8–13% at 1h BTC but losing 10–24% at 24h; log-HAR combinations helping mainly at 1h/4h. A Chronos-2 placebo result warns that apparent covariate gains may not be DVOL-specific. Pretraining overlap remains a limitation. [Paper](https://tommasozeri.github.io/research/foundation-models-crypto-realized-volatility/) · [code/research repository](https://github.com/tommasozeri/Crypto-Time-Series-Foundation-Models/tree/c6fcb9d2cde2c73a797d08d28a630ba55e110572). citeturn637395view0
2. Sukono et al. (2026-05-31) propose FA-LSTM-N-BEATS with fractional memory and MF-DFA. Four quarterly rolling folds on daily BTC/ETH/BNB show BTC RMSE 0.02370 versus 0.02273 for Std-LSTM; ETH is marginally better, BNB worse. Best BTC direction hit rate is 53.5% (p=0.0856), not significant at 5%. A learned fractional parameter is not itself proof of multifractal market structure or forecast edge. [Original article](https://doi.org/10.3390/fractalfract10060379). citeturn592544view0turn592544view1
3. Gjeçi et al. (2026-05-28) compare EGARCH/GJR-GARCH, normal/Student-t innovations and a lagged Fear & Greed high-greed dummy on 2,650 daily observations for seven coins. CFGI coefficients are mostly insignificant; OOS winners vary by asset; BTC QLIKE differences with/without CFGI are tiny (2.7660 vs 2.7663), and BTC volatility-direction hit rates hover around chance. [Original article](https://doi.org/10.3390/jrfm19060390). citeturn955387view0turn227438view3
4. HawkesTime/HawkesSign remains useful microstructure research for next-event timing/sign on Bitfinex LOB, not an hourly/24h price path. Current repository HEAD and GPL-3.0 license were rechecked; no code was copied. [Paper](https://doi.org/10.1007/s10203-026-00570-z) · [repository](https://github.com/Learning2Control/MultivariateHawkesLOB/tree/ecee1b7af5013e44b9ab584e93cd592aefa69fbd). citeturn362502view1
5. A newly indexed MF-DFA item attributed to Unal could not be independently located at an original publisher/DOI; its claims were not admitted as verified evidence.

**Hypotheses, not established facts**

- Calendar-adjusted HAR/log-HAR may improve volatility intervals once at least ~170 days of clean 5m history are available.
- Fractional/fractal features may be useful only in specific regimes; they require pre-registered ablations against standard baselines.
- Sentiment, news surprise and attention should remain separate point-in-time channels. No licensed, timestamped news/sentiment feed was available for this run.

## Competitor watchlist and licenses

- Added Gjeçi et al. as a paper-only daily volatility challenger; rechecked Zeri's MIT code revision and HawkesTime's GPL-3.0 repository revision. Existing Chronos-2, TimesFM-3 and Timestral entries remain separate by code and weight license.
- No third-party code, weights, datasets, cached outputs or figures were copied. Zeri code is MIT, but TimesFM-3 weights are non-commercial; Chronos-2 weights are Apache-2.0; Timestral weights have a separate Modified MIT/revenue-threshold license. Hawkes code is GPL-3.0. Gjeçi and Sukono papers are CC BY 4.0, but their third-party datasets retain separate terms.
- No external forecaster qualified for the shadow leaderboard: no independently verifiable, time-stamped 24-point BTC/USD price path with matching venue, issue time, cutoff and horizon was found. No competition submission or market participation occurred.

## Code and documentation changed

- `evaluate_vintages.py`: leaderboard aggregation now scans all JSON records; previously it searched only `evaluation_*.json` and silently missed archived `lfm5m-*.json` evaluations.
- `test_evaluate_vintages.py`: added regression coverage for archived filename discovery and exclusion of manifest/raw candle JSON.
- `archive_workflow_artifacts.py`: archiver now waits for the evaluator after any evaluator-triggering code/test/workflow push, not only daily-marker pushes.
- `test_archive_workflow_artifacts.py`: added race-condition regression tests.
- Updated `RESEARCH_LOG.md`, `COMPETITOR_LANDSCAPE.md`, and `THIRD_PARTY_LICENSES.md`.
- No forecast equations, dependencies or model weights changed.

## Tests and workflow status

- Daily forecast run [45572000476](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000476): success; **15/15** forecast tests; public Binance data retrieval, forecast generation and artifact upload succeeded.
- Initial evaluation run [45572000340](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000340): success; evaluated Nov 23 only because Nov 24 targets had not yet fully closed at 07:56 UTC.
- Daily archive run [45572000351](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000351): success; exact forecast ZIP/JSON/raw snapshot archived.
- Patched evaluation run [45574156649](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156649): success; **17/17** evaluation tests; evaluated Nov 24 after its final close.
- Patched archive run [45574156692](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156692): success; **19/19** archiver tests; evaluation artifact archived and ledger updated with no errors.
- Repository test workflow [45574156631](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156631): success.

## Current 24-hour hourly forecast

**No validated BTC/USD champion forecast exists.** The available live run is a clearly labelled **BTC/USDT challenger** from Binance Spot 5m inputs; it must not be read as a USD-composite forecast.

- Issue time: 2026-11-25 07:56:14.398136 UTC
- Data cutoff: 2026-11-25 07:54:59.999 UTC
- Retrieval: 2026-11-25 07:56:14.393464 UTC
- Source: `https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000`
- Reference: 58,698.41 USDT; 999 closed 5m candles (1,000 rows, last open candle filtered); 24 hourly targets.
- Model: `LFM-5m-Downside-Aware-Council-0.4`; model commit `80a4707c3ee376c796d2aa0df565e3237f9c7e2e`.
- Artifact: [run 45572000476](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000476), artifact ID 15002426841; archived at [forecast ZIP](https://github.com/messerzai/ambivikhry-agent/blob/research/living-fractal-market/research/living-fractal-market/forecasts/2026-11-25/2026-11-25T07-56-14.398136Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip).
- ZIP SHA-256: `1d0c8baf56fe91bc5ba695b67746824d341fc3b2ae81267f6575732a887ce74a`; forecast JSON SHA-256: `f3c0b3021af51ae5b16c9cc3347ac8b69a5ff31c5b635f0ada140a82e2f74f0b`; raw input SHA-256: `0a710bc026be5811678240a500c13d87f0b14425b210f4f9b42f84165631d9b0`.
- No calibrated P50/P90 intervals; the stored P90-style bands are Gaussian approximations and explicitly uncalibrated.

| Horizon | Target UTC | LFM5mEnsemble point (USDT) |
|---:|---|---:|
| +1 | 2026-11-25 08:00 | 58,657.22 |
| +2 | 2026-11-25 09:00 | 58,622.70 |
| +3 | 2026-11-25 10:00 | 58,593.83 |
| +4 | 2026-11-25 11:00 | 58,569.74 |
| +5 | 2026-11-25 12:00 | 58,549.71 |
| +6 | 2026-11-25 13:00 | 58,533.11 |
| +7 | 2026-11-25 14:00 | 58,519.42 |
| +8 | 2026-11-25 15:00 | 58,508.20 |
| +9 | 2026-11-25 16:00 | 58,499.08 |
| +10 | 2026-11-25 17:00 | 58,491.74 |
| +11 | 2026-11-25 18:00 | 58,485.91 |
| +12 | 2026-11-25 19:00 | 58,481.37 |
| +13 | 2026-11-25 20:00 | 58,477.91 |
| +14 | 2026-11-25 21:00 | 58,475.37 |
| +15 | 2026-11-25 22:00 | 58,473.63 |
| +16 | 2026-11-25 23:00 | 58,472.55 |
| +17 | 2026-11-26 00:00 | 58,472.04 |
| +18 | 2026-11-26 01:00 | 58,472.01 |
| +19 | 2026-11-26 02:00 | 58,472.40 |
| +20 | 2026-11-26 03:00 | 58,473.13 |
| +21 | 2026-11-26 04:00 | 58,474.17 |
| +22 | 2026-11-26 05:00 | 58,475.46 |
| +23 | 2026-11-26 06:00 | 58,476.96 |
| +24 | 2026-11-26 07:00 | 58,478.65 |

## Previous forecast evaluation and leaderboard

**Nov 24 vintage** (issue 2026-11-24 07:14:55.957774 UTC; final target close 2026-11-25 07:59:59.999 UTC) was evaluated at 08:11:54.892 UTC using 24 Binance Spot BTCUSDT 1h closes. Actual-data SHA-256: `b088ae8c79aeca4426c2e6f3d5977221a3461c93a0d54fcc02e8e9cd6332be5c`. Evaluation JSON SHA-256: `19db9b30dd46a335fcda17d431af5f665b7b3ee4bbadb67fc5db2b06979ce19e`; exact evaluation ZIP SHA-256: `8adc1e6639a54e2bb4f76693a33122b68af7288fde6a421edb64b21ee92d7bb8`.

| Model / baseline | Normalized log-price MAE |
|---|---:|
| VolatilityCappedSlowDrift (simple baseline) | 0.357336 |
| RandomWalk | 1.074432 |
| DownsideStress5m | 1.074432 |
| TakerFlow5m | 1.079203 |
| LFM5mEnsemble | 1.121056 |
| MeanReversion5m | 1.128073 |
| Momentum5m | 1.133967 |
| VolatilityRegime5m | 1.176476 |

All model candidates failed to beat random walk on this vintage; the volatility-aware baseline was much better. Direction accuracy versus issue reference was 0 for all candidates; the volatility-aware baseline was 1.0. P90 empirical coverage was 100%, but interval width was about 13.03% and the intervals are not calibrated. **Virtual points: 0.**

Aggregate shadow leaderboard (18 completed unique vintages; 11 non-overlapping, 7 excluded for overlap; 0 calibrated vintages):
- MeanReversion5m 3.211871 (95% paired CI for difference vs RW: [−0.063146, 0.055261]) — tiny descriptive mean advantage, not robust.
- RandomWalk 3.219197.
- TakerFlow5m 3.221266.
- LFM5mEnsemble 3.348850 (CI difference vs RW [0.017418, 0.247931], worse).
- VolatilityRegime5m 3.398744; Momentum5m 3.519714; DownsideStress5m 3.929772.
- Strongest simple baseline by aggregate mean: RandomWalkLastPrice. VolatilityCappedSlowDrift aggregate mean: 3.949844.
- No external score is comparable or independently verifiable. **Total research points: 0.**

## Data-quality warnings and next experiment

- Current input history is only 999 × 5m = about 83h15m, too short for stable 90-day multifractal or ~170-day HAR-RV context.
- Quote is USDT, not USD; a validated BTC/USD champion and matching live feed remain absent.
- No point-in-time licensed sentiment/news surprise stream is available; no sentiment/news feature was added.
- Forecast P90 bands are uncalibrated; do not use them as calibrated risk intervals.
- Next: obtain a compliant 170-day 5m history, reproduce calendar-adjusted HAR/log-HAR realised-variance baselines separately from price-level forecasts, then test rolling past-only interval calibration. Keep champion promotion blocked until at least 30 non-overlapping daily vintages and calibrated intervals.

Research only; not financial advice. No trades, account access, funds movement or execution actions were performed.
