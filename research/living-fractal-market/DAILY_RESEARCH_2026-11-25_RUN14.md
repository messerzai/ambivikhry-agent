# Daily research report — 2026-11-25 (run 14)

Research-only continuation of the Living Fractal Market branch. Snapshot time: 2026-11-25 08:21 UTC.

## Branch and commits

- Branch: https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market
- Starting branch HEAD for this pass: `fec81b4fc3ae3403629616dcbdb8673e372ed40a`.
- Research-log update: https://github.com/messerzai/ambivikhry-agent/commit/b1a9979ff8a1657de7058b30ef7e3afa0d67f87a
- Competitor landscape update: https://github.com/messerzai/ambivikhry-agent/commit/9e102b35c66b83ed9ee27901d65c8ce50da066ac
- Third-party license register update: https://github.com/messerzai/ambivikhry-agent/commit/f9bd368a71b8e9ecb54bcfdcce28136dfdf7a0c4
- Documentation-only changes; no forecast code, model equations, dependencies or tests were changed. All writes targeted this branch. `main` was not modified.

## Daily workflow and artifact verification

The daily marker `lfm-daily-20261125-0754z-r13-c91d` had already triggered today's run and its exact forecast had been archived. It was **not** updated a second time.

- Forecast workflow [45572000476](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000476): completed successfully on branch `research/living-fractal-market`, source commit `80a4707c3ee376c796d2aa0df565e3237f9c7e2e`. Offline tests, live public-data retrieval, forecast generation and artifact upload all succeeded.
- Forecast tests: 15/15 passed.
- Workflow artifact ID: `15002426841`; exact downloaded ZIP SHA-256: `1d0c8baf56fe91bc5ba695b67746824d341fc3b2ae81267f6575732a887ce74a`.
- Extracted forecast JSON SHA-256: `f3c0b3021af51ae5b16c9cc3347ac8b69a5ff31c5b635f0ada140a82e2f74f0b`.
- Raw Binance 5m input SHA-256: `0a710bc026be5811678240a500c13d87f0b14425b210f4f9b42f84165631d9b0`.
- Independent artifact check: ZIP contained exactly `forecast_5m.json` and `forecast_5m_raw_klines.json`; 1,000 input rows, 999 closed, one forming candle excluded; closed candles were contiguous; final closed candle opened 07:50:00Z and closed 07:54:59.999Z; forecast cutoff matched; issue-to-cutoff age 74.399 seconds; retrieval-to-issue lag 4.672 ms; all seven models emitted the same 24-point hourly target grid.
- Archive exists in the branch at [the immutable forecast artifact](https://github.com/messerzai/ambivikhry-agent/blob/research/living-fractal-market/research/living-fractal-market/forecasts/2026-11-25/2026-11-25T07-56-14.398136Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip). Readable JSON and exact raw input snapshot are archived beside it. The forecast ledger records provenance and hashes.

## Research discoveries

### Facts checked against original publisher/paper records

1. **Rolling multifractal diagnostics are regime- and market-dependent, but are not a point-price forecasting result.** Kim, Lee & Choi, “Comparative Analysis of Cryptocurrency Market Efficiency and Local Features Using MF-DFA and DCC-GARCH,” *Fractal and Fractional* 10(6), 353 (23 May 2026), [DOI](https://doi.org/10.3390/fractalfract10060353). The publisher full text was checked. It studies daily BTC/ETH/XRP/BCH pairs across KRW/USD/JPY from 2018-01-01 to 2025-09-30; MF-DFA uses q ∈ [-10,10], quadratic detrending, 250-observation rolling windows, and 200/300-window sensitivity checks. The paper reports time-varying spectrum width and high same-asset cross-fiat return correlation, while efficiency-proxy co-movement is more heterogeneous. It does not demonstrate an hourly BTC point-price edge.

2. **A surrogate-method qualification matters for the source decomposition.** The paper describes 99 Fourier phase-randomized surrogates and says the procedure preserves the amplitude spectrum and heavy-tailed distribution. Plain phase randomization preserves the Fourier amplitude spectrum but does not, by itself, preserve the exact empirical marginal distribution. IAAFT is specifically designed to preserve the empirical amplitude distribution while approximating the power spectrum: Venema, Ament & Simmer (2006), [DOI](https://doi.org/10.5194/npg-13-321-2006). Unless an extra rank-remapping step was used but not described, the paper's claim that its phase-randomized null isolates long-range dependence from heavy tails is not fully established by the described procedure. This narrows the source-attribution claim; it does not invalidate the reported rolling MF-DFA estimates. Our replication plan now requires shuffled, phase-randomized and IAAFT controls with explicit spectrum and marginal-distribution diagnostics.

3. **News polarity findings are mixed and target-dependent.** Gür & Ünal, “The Impact of News Sentiment on the Bitcoin Price via Machine Learning and Deep Learning-Based NLP Models,” *Journal of Forecasting* 45(3), 895–923, [DOI](https://doi.org/10.1002/for.70068). The publisher abstract reports FinBERT scores/semantic features from more than 650,000 headlines combined with lagged BTC, macro and financial variables; FinBERT-LSTM is reported as the best hybrid, with a stronger response to negative news. The publisher says the underlying data are available by author request; full methodological details and public code/data were not available in the accessible record. Treat as paper-only evidence, not a verified 24h hourly forecast benchmark.

4. **Attention and polarity should not be collapsed.** Akbar, “Human signals, automated noise: identifying the true drivers of crypto volatility,” *Studies in Economics and Finance* 43(5) (2026), [DOI](https://doi.org/10.1108/SEF-12-2025-0942). The publisher abstract describes >16 million BTC-related tweets and reports that polarity/hype/anxiety do not predict returns across its specifications, while attention improves conditional-variance modelling and reacts to price shocks. The full text was not accessible; the publisher states “Licensed re-use rights only.” This is an abstract-level volatility/attention result, not a public hourly price forecaster.

5. **Foundation-model volatility evidence remains a separate track.** Zeri's [BTC/ETH realised-volatility study](https://tommasozeri.github.io/research/foundation-models-crypto-realized-volatility/) reports that calendar-adjusted HAR/log-HAR is a much stronger comparator than unadjusted HAR; zero-shot Chronos-2, TimesFM-3 and Timestral models help mainly in short-horizon volatility combinations, not as a direct price-level model. A placebo-covariate test is especially important for Chronos-2. This study is not a substitute for our hourly price-path tournament.

### Hypotheses, not findings

- IAAFT and other distribution-preserving nulls may materially change estimates of the fraction of multifractality attributable to heavy tails versus temporal dependence.
- News sentiment may be more useful as a conditional event-risk/volatility feature than as a signed-return predictor; the two publisher findings are not directly comparable because sources, sample periods, frequency, feature construction and target differ.
- Rolling spectrum width may describe regime state, but no predictive value should be claimed until it beats volatility and calendar baselines on a strictly chronological holdout.

## Competitor watchlist changes

- Rechecked [GPTReviews](https://gptreviews.io/): its methodology page describes daily BTC/ETH/EURUSD UP/DOWN calls over a fixed 24-hour window with confidence and Brier scoring from a public Supabase database. The page rendered empty/loading leaderboard and prediction tables in this check; no actual row or model score could be independently verified. No price targets are provided. Retain as an unranked direction-only shadow comparator.
- Rechecked [BitPredict](https://www.bitpredict.io/): it offers human UP/DOWN calls and timestamped receipts, including 24-hour windows. The public leaderboard also rendered loading/empty; no settled receipt was independently captured. Manual participation requires an account; automated API access is listed at $29/month. No account, payment, API access or submission was made.
- Neither service qualifies for the external price-path leaderboard: no matching 24 hourly price levels, venue, issue/cutoff and scoring contract.
- Existing Chronos-2, TimesFM 2.5/3.0, NeuralForecast N-BEATS/N-HiTS/TFT/PatchTST, HAR/log-HAR, GARCH and multifractal candidates remain as previously recorded. No new runnable BTC/USD hourly candidate with independently verifiable forward forecasts was found.

## License audit

- No third-party code, model weights, datasets, raw headlines/posts, API payloads or benchmark outputs were copied.
- Kim et al.'s publisher page states CC BY; exact license version should be checked before any adaptation. Its daily market data are available by request, not a public dataset grant.
- Gür & Ünal's accessible Wiley page states all rights reserved; no permissive article license was identified. Dataset access is by author request.
- Akbar's Emerald page states “Licensed re-use rights only”; no code/data reuse was attempted.
- Venema et al.'s IAAFT paper states CC BY-NC-SA 2.5; cited for methodology only, with no article content or code reused. Non-commercial/share-alike restrictions mean direct article-derived reuse in a commercial derivative is not cleared.
- GPTReviews/BitPredict public pages were read only; no forecast rows, code or API payloads were copied. Public accessibility is not treated as a redistribution license.
- The detailed register was updated in commit [f9bd368](https://github.com/messerzai/ambivikhry-agent/commit/f9bd368a71b8e9ecb54bcfdcce28136dfdf7a0c4). This is a provenance checklist, not a legal opinion.

## Code, documentation and tests

- Documentation changed: `RESEARCH_LOG.md`, `COMPETITOR_LANDSCAPE.md`, `THIRD_PARTY_LICENSES.md`.
- Commits: [research log](https://github.com/messerzai/ambivikhry-agent/commit/b1a9979ff8a1657de7058b30ef7e3afa0d67f87a), [competitor landscape](https://github.com/messerzai/ambivikhry-agent/commit/9e102b35c66b83ed9ee27901d65c8ce50da066ac), [license register](https://github.com/messerzai/ambivikhry-agent/commit/f9bd368a71b8e9ecb54bcfdcce28136dfdf7a0c4).
- No code or dependency change was justified by this literature pass; no tests were rerun for documentation-only commits.
- Earlier same-day verified runs: evaluation [45574156649](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156649) passed 17/17 evaluator tests and completed the Nov 24 evaluation; archive [45574156692](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156692) passed 19/19 archiver tests and archived that evaluation; repository CI [45574156631](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156631) passed on Python 3.10, 3.11, 3.12 and 3.13.

## Current 24-hour hourly forecast

**No validated BTC/USD champion forecast exists.** The latest live output is a BTC/USDT challenger generated from Binance Spot 5-minute inputs. Do not relabel it as USD.

- Issue: 2026-11-25T07:56:14.398136Z
- Data cutoff: 2026-11-25T07:54:59.999Z
- Source: Binance Spot public klines, BTCUSDT, 5m, https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000
- Reference: 58,698.41 USDT; 999 closed 5m candles.
- Model: `LFM-5m-Downside-Aware-Council-0.4`; source commit `80a4707c3ee376c796d2aa0df565e3237f9c7e2e`.
- No calibrated P50/P90 intervals. Stored Gaussian-style P90 bands are explicitly uncalibrated and are not reported as calibrated uncertainty.

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

The final target candle closes at 2026-11-26T07:59:59.999Z; all target outcomes remain pending.

## Previous forecast evaluation and leaderboard

The Nov 24 vintage (issue 2026-11-24T07:14:55.957774Z) was evaluated at 2026-11-25T08:11:54.892Z after all 24 hourly target candles closed.

| Model / baseline | Normalized log-price MAE |
|---|---:|
| VolatilityCappedSlowDrift | 0.357336 |
| RandomWalkLastPrice | 1.074432 |
| DownsideStress5m | 1.074432 |
| TakerFlow5m | 1.079203 |
| LFM5mEnsemble | 1.121056 |
| MeanReversion5m | 1.128073 |
| Momentum5m | 1.133967 |
| VolatilityRegime5m | 1.176476 |

All candidate models failed to beat random walk on this vintage; the volatility-aware simple baseline was much better. P90 empirical coverage was 100%, but mean width was about 13.03% and the bands are uncalibrated. Virtual points for this vintage: 0.

Current ledger state: 19 unique forecast vintages archived; 18 completed and one pending (Nov 25). The aggregate uses 11 non-overlapping completed vintages; seven overlapping vintages are excluded. Aggregate mean nMAE: RandomWalkLastPrice 3.219197; MeanReversion5m 3.211871 (paired 95% difference CI versus random walk [-0.063146, 0.055261], not robust); TakerFlow5m 3.221266; LFM5mEnsemble 3.348850 (worse than random walk; paired CI [0.017418, 0.247931]); VolatilityRegime5m 3.398744; Momentum5m 3.519714; DownsideStress5m 3.929772; VolatilityCappedSlowDrift 3.949844.

- Calibrated vintages: 0.
- External comparable price-path scores: none.
- Total virtual research points: **0**.
- Champion promotion: blocked; 30 non-overlapping completed vintages and calibrated intervals are not yet available.

## Data-quality warnings and next experiment

- The live input is only 999 × 5m candles (~83h15m), not the 90–170 days needed for stable long-window MF-DFA/HAR comparisons.
- Quote currency is USDT, not USD; no BTC/USD composite source has passed the quality gate.
- No licensed, timestamped news/sentiment surprise stream is available; no such features were added.
- Gaussian-style P90 bands are not calibrated; no uncertainty claim should be inferred from their coverage on one vintage.
- Next experiment: build a paginated, immutable 170-day Binance Spot BTCUSDT 5m dataset with raw hashes and UTC provenance; reproduce calendar-adjusted HAR/log-HAR realised-variance baselines separately from point-price forecasts; then compare shuffled, phase-randomized and IAAFT MF-DFA nulls on identical rolling windows. Keep fractal, news and sentiment features as separate preregistered ablations. Do not promote the 5m council to a BTC/USD champion.

Research only; not financial advice. No trades, account access, funds movement or execution actions were performed.
