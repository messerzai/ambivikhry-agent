# Competitor landscape and reuse policy

Last reviewed: 2026-11-18  
Target: BTC/USD hourly observations and +1 to +24 hour horizons.  
Research branch: research/living-fractal-market

## Purpose

Build a fair, forward-blind comparison set for the Living Fractal Market champion. A competitor is rankable only when the forecast is timestamped before its target, the information cutoff is known, and asset, venue, quote currency, target clock and horizon can be aligned. Published backtests, model cards and marketing claims are discovery evidence—not live leaderboard scores. The phrase “living/non-repeating fractal” remains a research metaphor, not an established market law.

## Candidate registry

| Candidate / project | Family and target | Reproducibility and evidence checked 2026-11-11 | Comparability / status |
|---|---|---|---|
| Random walk / last price | Statistical baseline; BTC/USDT or BTC/USD, +1…+24h | Deterministic and cheap; our mandatory primary reference | Internal baseline; always score |
| ARIMA / ETS / zero-drift / volatility-aware | Statistical baselines; hourly BTC | Reproducible with pinned data and parameters; no crypto-specific advantage assumed | Internal challengers; required controls |
| Amazon Chronos-2 | 120M zero-shot foundation model; univariate/multivariate and covariates; quantile output | Official card claims general zero-shot benchmark performance on FEV-Bench, GIFT-Eval and Chronos Benchmark II; no BTC-specific evidence on the card. Official code and weights are Apache-2.0 at the checked sources. | Strong external challenger; requires pinned checkpoint, runtime test and chronological BTC evaluation |
| Google TimesFM 2.5 | 200M foundation model; quantile forecast, long context | Official model card lists Apache-2.0 weights and links ICML 2024 paper; no BTC-specific benchmark proof on the card | Candidate; code and weights are separately checked as Apache-2.0 |
| Google TimesFM 3.0 | 330M foundation model; multivariate/covariate-capable | Official HF card lists timesfm-non-commercial-license-v1.0; code repository remains Apache-2.0. Weights are not suitable for commercial/production use under the current card. | Research-only license review; exclude from any commercial/production product unless terms change and are reviewed |
| Nixtla NeuralForecast: N-BEATS, N-HiTS, TFT, PatchTST | Trainable neural forecasting library | Official repository lists these models and Apache-2.0 code. No pretrained crypto checkpoint is supplied by the library itself; training and tuning must be done without leakage. | Candidate family; train locally against same rolling origins and baselines |
| FoundationForecast | Foundation-model adapter/evaluation framework | Apache-2.0 repository; plugged-in model and weight terms remain separate | Candidate for an adapter only after dependency and model-specific license audit |
| Benchstreet | Financial time-series examples: ARIMA, N-BEATS, TimesFM, Chronos, MLP, LSTM, GRU, CNN, TCN | MIT code at checked HEAD. README says its examples use 20 years of S&P 500 daily closes and explicitly says it is not an objective benchmark; it calls N-BEATS the winner, but this is not evidence for BTC hourly forecasting. | Useful implementation/reference lead; not a comparable result. No code or weights copied |
| CrunchDAO Synth | Live probabilistic competition; BTC among assets; 1h and 24h horizons | Official docs describe full return-density forecasts for 1h and 24h, CRPS scoring, multiple temporal resolutions and a 40-second inference budget. Current documented rounds run every 8 minutes (1h horizon; 1m/5m/15m/30m/1h steps) and every 39 minutes (24h horizon; 5m/1h/6h/24h steps). The 1h score includes a volatility-CRPS term based on 1,000 simulated price paths; the rolling rank uses a 7-day window. The docs say rewards were paused and Synth miners deregistered in October 2026; the earlier $30,000 USDC phase is marked completed. Official crunch-synth repository is at v0.16.0 commit 679dfc2; no LICENSE file found at that commit. | Methodology/shadow benchmark only. No code copied and no external submission attempted |
| CryptoOracle | Public hourly forecast journal; BTC/ETH/SOL, +24h and +72h | Public site says TimesFM 2.5 consumes 512 completed hourly closes and locks forecasts. Its frozen 17-Sep-2026 exploratory study reports 365 daily origins per asset/horizon: BTC +24h mean absolute log-return error ×100 = 1.712 vs 1.627 for last-price baseline; nominal 80% band coverage = 77.3%. It explicitly concludes no forecasting advantage demonstrated. | Closest public 24h research comparator, but not directly rankable against our 24-step hourly trajectory loss. Live JSON records were not parsed in this run |
| BitPredict | Human/public predictor leaderboard; BTC UP/DOWN over 24h | Site advertises free, immutable timestamped BTC/ETH/SOL UP/DOWN 24h receipts and automatic settlement; calls are directional rather than price distributions. The public app rendered a loading state without a populated leaderboard/receipt sample in this review. Free manual calls require an account to publish; bot/API access is an Elite plan listed at $29/month, so automated participation fails the no-payment rule. No submission was made. | Direction-only shadow reference; not comparable to normalized MAE/CRPS. No automated participation |
| AI Predicts Bitcoin | Daily panel of 10 LLMs; +7d/+30d/+90d/+180d/+360d | Public daily predictions for 7d/30d/90d/180d/360d; latest surfaced 7d batch dated 2026-11-07 although the page claims daily updates at 06:00 UTC, making the batch four days stale at this review. It also says 200 predictions are graded while showing a grade-unlock date of 2026-04-08, an internal date conflict; do not trust aggregate accuracy until reconciled. Not an hourly forecast system. | Long-horizon context only; not rankable against BTC hourly or 24h |
| Crowdsource | Public prediction competitions | Candidate retained from prior discovery; no independently verifiable, matching BTC/USD hourly record or automated-submission terms confirmed in this pass | Unverified; no submission |

## External evidence worth tracking

### CryptoOracle

Public overview and forecast journal:
- https://cryptooracle.moinsen.dev/
- https://cryptooracle.moinsen.dev/forecasts/
- https://cryptooracle.moinsen.dev/data/research.json
- Source repository: https://github.com/moinsen-dev/crypto-oracle

The published 17-Sep-2026 historical snapshot reports the TimesFM 2.5 BTC +24h error as 5.2% higher than persistence (1.712 vs 1.627 on mean absolute log-return error ×100) and nominal 80% interval coverage of 77.3%. This is a useful negative result: a large foundation model can lose to the last observed price. The experiment has 365 daily historical origins, while the live journal says forecasts are issued hourly; overlapping hourly origins are not independent market events. Do not mix the historical snapshot with the current prospective ledger.

### CrunchDAO Synth

Official rules and current competition directory:
- https://docs.crunchdao.com/real-time-competitions/competitions/synth
- https://hub.crunchdao.com/competitions
- https://github.com/crunchdao/crunch-synth

The competition scores full predictive densities using CRPS, with a 7-day rolling leaderboard; the 1h task additionally scores realized volatility. Official docs identify a Synth benchmarktracker that replays a real miner (ranked #1 on 1h and #20 on 24h in the documented comparison), but this is a reference row rather than an independent live submission and is not a BTC-only score. The current model's point/P90 output is not comparable to Synth's density forecasts. No participation was attempted: joining requires a CrunchDAO account and acceptance of rules; rewards are currently paused, while the prior $30,000 USDC phase is marked completed. Automated participation terms and account conditions were not established as compatible with this project's no-external-account/no-token rule.

## First implementation order

1. Keep random walk, zero-drift, drift, ARIMA/ETS and volatility-aware baselines as mandatory controls.
2. Add Chronos-2 as the first foundation-model challenger after pinning its exact model-hub revision and testing CPU/GPU resource use.
3. Add TimesFM 2.5 separately; do not infer TimesFM 3.0 weight rights from the shared source-code license.
4. Train N-BEATS/N-HiTS/PatchTST/TFT on identical rolling-origin splits; report tuning budget and seed.
5. Add a distributional challenger with calibrated quantiles or a full density; evaluate CRPS/pinball loss and coverage.
6. Add microstructure features only when the same venue and point-in-time feed are available; keep spot taker-buy volume distinct from order-book depth and futures flow.
7. Add news/sentiment as a separate ablation with publication, collection and availability timestamps.
8. Mirror external competitions in a shadow leaderboard before considering any submission.

## Fair-comparison contract

For every external record store: project/model and immutable revision; asset; venue; quote currency; issue time; data cutoff; target timestamps; point or distribution output; actual target; scoring method; sample size; and whether the result is forward, rolling-origin backtest, in-sample, or promotional. Do not rank incomparable records together. Overlapping hourly origins must not be treated as independent successes.

## License and provenance policy

Public availability is not permission to copy. Before reuse, inspect the exact source-code license and separately inspect model weights, datasets, tokenizers, benchmark data and API terms. Pin an immutable commit/revision, preserve notices, record copied paths and modifications, and check copyleft/source-disclosure and commercial restrictions. If terms are absent or unclear, do not copy; implement independently from cited public concepts/papers. The register in THIRD_PARTY_LICENSES.md is an engineering provenance aid, not legal advice.

## Source index

- Chronos-2 model card: https://huggingface.co/amazon/chronos-2
- Chronos code: https://github.com/amazon-science/chronos-forecasting
- TimesFM 2.5 model card: https://huggingface.co/google/timesfm-2.5-200m-pytorch
- TimesFM 3.0 model card: https://huggingface.co/google/timesfm-3.0-pytorch
- TimesFM source: https://github.com/google-research/timesfm
- NeuralForecast: https://github.com/Nixtla/neuralforecast
- FoundationForecast: https://github.com/TimeCopilot/foundationforecast
- Benchstreet: https://github.com/puffinsoft/benchstreet
- BitPredict: https://www.bitpredict.io/
- AI Predicts Bitcoin: https://www.aipredictsbitcoin.com/
- Crowdsource: https://crowdsource.sh/

## Open questions

- Which external public ledgers expose complete machine-readable point-in-time forecasts, not only aggregate backtests?
- Can Chronos-2 or TimesFM 2.5 beat persistence on BTC at 1h and 24h after identical rolling-origin evaluation?
- Does a genuine multifractal statistic survive IAAFT and finite-size nulls in rolling windows, and does it add forecast value after controlling for volatility and regime?
- Do point-in-time sentiment/news features add anything beyond event-time, volatility and liquidity baselines?
- Can a calibrated density beat persistence and a volatility-aware density under CRPS without using external contest accounts or rewards?


## Latest competitor status check — 2026-11-11

### CryptoOracle public forecast journal — updated snapshot

The public journal's latest surfaced record is **14 October 2026, 05:14 CEST**; the page says it normally updates about every 15 minutes, so by this review it is stale by roughly 28 days. The same surfaced snapshot reports **619 settled from 643 issued forecasts** over about 27 days of market data, 366/619 direction matches, 488/619 outcomes inside a nominal 80% band, and mean miss 1.34 log-return points versus 1.32 for the “price stays the same” baseline. The journal explicitly warns that hourly forecasts overlap and do not represent independent market events.

- **Comparability:** closest public BTC +24h hourly TimesFM reference found, but it predicts an endpoint rather than our full 24-step hourly trajectory. Its current public page is stale; do not treat the aggregate figures as a current live score or combine them with the earlier 17-Sep historical snapshot.
- **Method/controls:** the public method says forecasts are frozen before target time, settled on Binance BTC/USDT hourly closes, and cross-checked against Coinbase/Kraken USD closes with same-hour USDT/USD conversion. It describes a separate residual-calibration shadow and a separate FinBERT news experiment; neither is a directly comparable result for our model.
- **Evidence quality:** useful transparent ledger design and a warning against counting overlapping origins as independent. The public page is JavaScript-driven; its visible static page exposes the public JSON link but not the complete rows in this review. No machine-readable individual forecast records were scored here.
- **License:** the current source repository README describes TimesFM 2.5 and the public research system, but no root LICENSE or LICENSE.md was present at the checked repository root. No code or weights copied. The checkpoint's own model-card license is a separate object; the official TimesFM 2.5 model card lists Apache-2.0, but no checkpoint was downloaded or reused.
- **Checked sources:** https://cryptooracle.moinsen.dev/forecasts/ ; https://github.com/moinsen-dev/crypto-oracle ; https://huggingface.co/google/timesfm-2.5-200m-pytorch

**Leaderboard decision:** retain CryptoOracle as an external shadow comparator, not a ranked competitor. It is not sufficiently fresh and its endpoint-only score does not match our 24-hour hourly path loss. No external submission or account was created.


## Additional competitor watch — checked 2026-11-12

| Project | Method / target | Reproducibility and evidence | Comparability decision |
|---|---|---|---|
| [webTimesFM](https://github.com/vishalmysore/webTimesFM) | Browser inference for TimesFM 2.5 and Chronos-2 via ONNX Runtime Web, WebGPU/WASM | Code HEAD `ffbdec38f5d86a84e0bd274534ac91129db5c7b5`; Apache-2.0 code. Its 18-Oct-2026 ten-series comparison reports Bitcoin 30-day MAE: TimesFM 2.5 6,949; Chronos-2 7,272; no-change 7,153. The README says point counts are hidden and ten series are a small test, not a benchmark. ONNX model artifacts have separate model-card terms. | BTC-specific exploratory lead only. Frequency, exact forecast origins, horizon and raw ledger are not sufficiently exposed; not rankable against hourly BTC/USD path loss. No code/weights copied. |
| [FelixClements/prism](https://github.com/FelixClements/prism) | Chronos/TimesFM, wavelets and on-chain features; BTC 3–14 day swing forecasts, daily Coinbase data | HEAD `782115532b08033692e747e3b1b57d0da3e9928d`; repository has an AGPL-3.0 license. README describes a walk-forward scoreboard but also references scripts from external agent skills outside the repository. Model weights have separate terms. | Not an hourly candidate; potentially useful methodology reference. No code or weights copied; copyleft/network-use obligations require legal review before any derivative use. |
| [TensorLink-AI/ephemeris-mcp](https://github.com/TensorLink-AI/ephemeris-mcp) | MCP wrapper for Chronos-2, TimesFM 2.5, Toto 2, TiRex-2, IBM Granite models and an accuracy-weighted ensemble | HEAD `263b60b704e1cff855036a62ef1541ec45d33d57`; MIT bridge code. README reports TIME MASE 0.639 vs 0.638 leader and GIFT-Eval CRPS 0.4662 vs seasonal naive; these are general benchmark claims, not BTC-specific scores. Hosted inference requires an API key and pay-per-forecast. Model licenses are separate. | Shadow watch only; no paid API call or account. General benchmark results cannot be ranked against BTC hourly forecasts. |
| [BrainEdge](https://brainedge.tech/) | BTC/USD, ETH/USD and XRP/USD short-horizon directional probabilities | Visible page claims 659 out-of-sample days and BTC directional accuracy 49.6%; page timestamp is 2026-10-23 07:13 UTC. No raw forecast ledger or matching 24-step price path was available in the checked view. | Unranked and stale by 20 days at this review. Do not treat aggregate directional accuracy as a comparable price forecast. |

### Interpretation of new candidates

The only BTC-specific numerical comparison among these additions is webTimesFM's small 30-day test, where TimesFM 2.5 is modestly better than its no-change baseline and Chronos-2 is worse. Because the frequency, origin details and raw errors are not disclosed in the surfaced summary, this is not evidence of BTC hourly skill. PRISM has a useful walk-forward architecture but a different 3–14 day target. Ephemeris exposes more foundation-model variants but is a paid service and has no BTC-specific result verified here. BrainEdge's visible scoreboard is too stale and too aggregate for a fair ranking.

No new competitor qualifies for the internal champion leaderboard. Keep Chronos-2 and TimesFM 2.5 as the preferred locally runnable foundation-model challengers, with exact checkpoint revisions and weights licenses pinned before use.


## Daily watchlist review — 2026-11-13

### New research/data references (not all are forecast competitors)

| Project / source | Method, asset and horizon | Evidence / reproducibility | Decision |
|---|---|---|---|
| ECB R-RISI — Wagner & Metzler, Working Paper 3276 (2026-08-24) | Daily Reddit retail sentiment, LLM sentiment/topic labels, engagement-weighted aggregation; broad market and crypto-related subreddits. Not a direct BTC price model. | Official ECB abstract describes 2015–Apr 2026 data and next-day price information, especially S&P 500 in market declines. Raw data and platform permissions were not audited here. | Add as a candidate daily sentiment reference only; no data or code reused. |
| Mispria public crypto market tracker | Polymarket BTC/ETH/SOL/XRP up/down markets at 5m, 15m and 1h; Brier scoring of market-implied probability and its Student-t model. | Page reports 158,074 windows from 2026-08-07 through 2026-11-11, snapshot 2026-11-12 08:02 UTC. BTC: market/model Brier 0.0560/0.0601 at 5m, 0.0357/0.0377 at 15m, 0.0282/0.0267 at 1h. Settlement uses Chainlink 60s TWAP for 5m/15m and Binance hourly candle for 1h. | Useful external probability benchmark, not comparable to our point-price MAE or 24h trajectory. No rank or points awarded. |
| The Brier Index | Public daily point/percentile/chance forecasts for BTC and six other coins at 1-, 7- and 30-day horizons; OpenTimestamps SHA-256 commitments. | Ledger explains verification procedure and preserves corrections; page says last updated 2026-11-08 and is not live. Some early records were stamped after the 1-day close. | Strong timestamp-integrity design reference; horizons and freshness do not match our hourly experiment. |
| CryptoOracle | TimesFM-based hourly model for BTC/ETH/SOL; 24h/72h forecasts, 512 completed hourly closes, news annotation separated from numerical price forecasts. | Public page reports a 365-origin historical BTC 24h backtest: mean absolute log-return error 1.712 vs 1.627 for last-price persistence (+5.2% higher error); nominal 80% band coverage 77.3%. It also exposes a live journal/public JSON, but the live JSON did not render in this review. | Keep as an important shadow comparator and methodological reference; historical backtest is not a current matched submission. |
| likely.sh | BTC/USDT deadline-specific touch probabilities, 15m/30m/8h/daily/weekly studies. | Current page load returned no active studies and was waiting for Binance completed-minute data; a search snapshot had estimates last updated 2026-11-08. | Stale/unavailable in this review; no ranking. |

Sources:
- ECB R-RISI: https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3276~3ba8565a13.en.pdf
- Mispria: https://mispria.com/markets
- The Brier Index: https://www.brierindex.com/ledger/
- CryptoOracle overview and journal: https://cryptooracle.moinsen.dev/ ; https://cryptooracle.moinsen.dev/forecasts/
- likely.sh: https://likely.sh/

### Comparable-forecast rule

No newly inspected external record supplies all of the following simultaneously: BTC spot venue and quote currency matching Binance BTCUSDT, exact issue time and information cutoff, 24 hourly target closes, and a preserved point-price path with intervals. Mispria is binary-market probability, Brier Index is 1/7/30-day, CryptoOracle's public live JSON is dynamically rendered and its published aggregate backtest is not a same-origin live comparator, and likely.sh is currently unavailable. All remain in the shadow watchlist; none enters the ranked external leaderboard.


## Additional risk-state challenger — checked 2026-11-14

| Project / paper | Method and target | Evidence and data | Reproducibility / comparison | Status |
|---|---|---|---|---|
| Li, Zhong & Li (2026), Entropy 28(10), 1096 | GSADF/BSADF + LR, KNN, SVM, DT, RF, XGBoost, LightGBM, ANN, LSTM and three probability ensembles; daily BTC explosive-state occurrence/continuation at 1/3/7 days | Daily Investing.com BTC 2016-01 to 2026-04; Yahoo Finance BTC/USD robustness; 30 episodes / 455 bubble days. 7-origin purge, training-only SMOTE, moving-block bootstrap and MCS. Multiple models remain in the 90% MCS; 7-day recall remains limited. | Peer-reviewed, full article available, but processed data only on request and no code repository linked. Daily state classification, not hourly point-price forecasting. Article CC BY 4.0; raw data terms remain separate. | Daily risk-state shadow challenger only; no external rank in hourly price-path tournament. Source: https://www.mdpi.com/1099-4300/28/10/1096 |
| Karagiorgis & Ballis (2026), Journal of Futures Markets 46(8), 1440–1452 | Time-varying skewness–kurtosis plane; hourly realized higher moments from 1-minute BTC spot/perpetual returns | Binance minute data 2020-10 to 2022-09; 34,854 hourly observations. Positive convex S² association; volume–kurtosis link stronger in futures and sensitive to winsorization. | Data on request; no public code/data license identified. Risk diagnostic, not price forecast. Full-sample log-volume demeaning in baseline is not point-in-time safe. | Higher-moment risk-state reference; no implementation or data reused. Source: https://onlinelibrary.wiley.com/doi/full/10.1002/fut.70117 |

## Public forecast ledger refresh — 2026-11-14

- CoinPredict BTC 24h: its public page was updated 2026-11-14 04:58 UTC. The visible 24h call was model 1d-20261105-0358, issued 2026-11-13 00:00 UTC, base $71,431, nominal 80% range $69,756–$73,129, confidence 52%, expiry 2026-11-14. The page reports 20 graded BTC 24h calls: 75% in range, 55% direction, median miss 0.9%. This is a scalar terminal-price forecast, now expired at this review time; it does not provide a matching 24-point hourly path. The separate aggregate track record has 6,710 24h calls across assets, not 6,710 BTC calls. Do not combine the denominators. Sources: https://coinpredict.net/price-prediction/bitcoin ; https://coinpredict.net/track-record
- SignalTrace Lab: search-index snapshot dated 2026-11-13 reported 46.8% up / 53.2% down at 2026-11-13 00:00 UTC, but the opened page showed an older 2026-11-10 edition (47.0% up / 53.0% down). Treat the newer snippet as unverified, not a current ledger entry. Source: https://signaltracelab.com/en/bitcoin/
- Satori Signals: a search snippet showed a Nov-14 01:00 UTC consensus, but the opened public page and forecasts page did not expose the same current row; detailed forecasts require a token holding or subscription. No account, token or paid access was used. Do not rank the snippet. Source: https://satorisignals.app/

No external record in this refresh supplies a same-origin Binance Spot BTCUSDT 24-step hourly price path and calibrated intervals. No external rank or LFM research points awarded.



## Competitor watch — checked 2026-11-15

### BTC-Oracle: strong process reference, not a matched external forecast

[barakacanbyte/btc-oracle](https://github.com/barakacanbyte/btc-oracle) — checked repository HEAD `41b1949c6fffb8aa23d2b2e1cabf7aa987b5d0a0` (last commit 2026-07-21). The README describes a single-user, self-hosted BTC-USD probabilistic system with five 24-hour log-return quantiles and P(up), hourly inference, immutable forecast records, live scoring, drift monitoring and a local-only dashboard.

- **Model zoo:** persistence and historical-drift baselines; LightGBM quantile models; GARCH(1,1)-Student-t; causal HMM regime model; PatchTST; calibrated stacked ensemble.
- **Data requirements:** Binance 1h/1d OHLCV, Binance Futures funding and open interest, Deribit DVOL, blockchain.com on-chain data, FRED macro series and alternative.me Fear & Greed. The README says news/FinBERT sentiment remains deferred. Open interest is only backfillable over a rolling 30-day window.
- **Reported benchmark:** report generated 2026-07-18; 31 walk-forward folds, train 3y → purge 24h → test 60d → embargo 7d, 43,754 test hours. The reported production ensemble has directional accuracy 0.52571, pinball 0.00699 (slightly below B1 historical-drift 0.00710), Brier 0.25904 and ECE 0.09355; it beats the baseline on 19/31 folds (61%). Its published gate requires direction to beat both baselines on at least 70% of folds, pinball below both, Brier below 0.25 and both baselines, and ECE below 0.05. The README says every model fails all four gates. It further reports that the recent six-fold directional accuracy is below 50% for both candidate and incumbent (0.4862 vs 0.4904).
- **Evidence quality:** source code, tests and detailed reports are present, but these are project-reported backtests; we did not independently reproduce the 43,754-hour run or inspect a public live forecast ledger. The API binds to localhost and is not a public prediction service.
- **Comparability:** the public contract is an endpoint +24h quantile distribution, not the 24 hourly target-price path required by our frozen tournament. Its source stack is also not identical to a single Binance Spot BTCUSDT series. Keep it in the methodology shadow watchlist, not the ranked external leaderboard.
- **Reproducibility cost:** Python 3.12, TimescaleDB, Prefect, MLflow, CPU PyTorch, multiple external data sources and long historical backfills. No model-weight artifacts were found in the inspected repository tree; weight terms would need a separate audit if supplied outside the repo.

Sources: https://github.com/barakacanbyte/btc-oracle ; https://github.com/barakacanbyte/btc-oracle/blob/main/reports/zoo_gate.md ; https://github.com/barakacanbyte/btc-oracle/blob/main/reports/ablation_fs_v2.md ; https://github.com/barakacanbyte/btc-oracle/blob/main/srs/btc-forecast-system.md

### Non-forecast sentiment/news references

| Source | Method / frequency | Evidence and limitations | Tournament status |
|---|---|---|---|
| [ECB R-RISI](https://dashboard.r-risi.workers.dev/) | Daily engagement-weighted Reddit sentiment, topics and tickers; rolling 365-day standardization; 7d/30d smoothing | A sentiment measurement system, not a price forecaster. Paper/dashboard model vintages differ (GPT-5.1 historically; GPT-6.1 Sol / Codex in newer dashboard vintages). Data rights and point-in-time engagement snapshots require review. | Feature-research reference only; no forecast rank. |
| Huynh (2026), [Tuning into the news](https://doi.org/10.1016/j.jbef.2026.101183) | Five-minute multi-crypto event study with daily TRMI sentiment and scheduled macro surprises | 2014–2021 top-100 cross-section; reported sentiment moderation of macro-news response, not BTC-only 24-step forecasts. | Feature-research reference only; no forecast rank. |

### External leaderboard decision

No newly inspected project supplies a fresh, independently verifiable, timestamped Binance Spot BTCUSDT 24-step hourly path with matching issue time, cutoff and calibrated intervals. BTC-Oracle's reported walk-forward endpoint forecast, ECB R-RISI, and Huynh's event-study coefficients are not comparable submissions. No external rank or research points awarded. Existing public systems (CoinPredict, Satori, SignalTrace, BitPredict, Mispria, The Brier Index, CryptoOracle, likely.sh and BrainEdge) remain in the shadow watchlist with their previously recorded freshness/comparability limitations.


## Competitor watchlist additions — checked 2026-11-15

| Project / source | Method and target | Data / reproducibility | Evidence and comparability | License / decision |
|---|---|---|---|---|
| [Learning2Control/MultivariateHawkesLOB](https://github.com/Learning2Control/MultivariateHawkesLOB) with Raffaelli et al. (2026), [paper](https://doi.org/10.1007/s10203-026-00570-z) | Multivariate Hawkes event intensities + continuous-time output-error/base-imbalance model; next BTC/USD mid-price event timing and return sign, not hourly price path. | LOB event streams; companion repo contains Bitfinex collection, dataframe conversion, Hawkes training and event simulation scripts. Requires Conda and event-level LOB data. | Paper reports 50 sampled trading scenarios with short test windows and a second BTC/USD regime; HawkesTime leads HawkesSign and moving-average sign baseline. No common H24 forecast ledger; no independent replication here. | Repository GPL-3.0; no code copied. Treat as separate event-time research only; copyleft implications require review before any derivative distribution. |
| [Wafi-Finance/Regime-Dependent-Bitcoin-Volatility-Forecasting](https://github.com/Wafi-Finance/Regime-Dependent-Bitcoin-Volatility-Forecasting) with [Digital Finance paper](https://doi.org/10.1007/s42521-026-00229-9) | GARCH family, LSTM and state-augmented GARCH–LSTM hybrids; one-step daily conditional volatility. | Balanced daily BTC sample of 2,722 observations through 2025-07-19; nested technical, sentiment and blockchain information sets; supplementary data and replication code advertised. | Rolling OOS QLIKE and Diebold–Mariano tests; best specification changes across normal and crisis regimes. Not an hourly price-path forecast. | Article CC BY 4.0; inspected GitHub root has no LICENSE for code/data. No code/data copied. |
| [Novel_Approach_to_Volatility_Analysis_on_Bitcoin_Returns](https://github.com/abeyankargiridharan/Novel_Approach_to_Volatility_Analysis_on_Bitcoin_Returns), paper [arXiv:2609.23250](https://arxiv.org/abs/2609.23250) | Sentiment-augmented Bretó POMP with Fear & Greed Index and Student-t observation noise; daily volatility state. | Daily BTC returns + FGI, 2020-01 to 2025-04; iterated filtering and 2,000-particle diagnostics. R dependencies are listed. | Reports log-likelihood and filter ESS against GARCH, HSV and original Bretó; no matched hourly BTC/USD forecast ledger and no rolling price-path evaluation. | No LICENSE found in inspected repo root; no code/data copied. |
| [artur-fedosiuk/btc-prediction-timesfm](https://github.com/artur-fedosiuk/btc-prediction-timesfm) | TimesFM 3.0 BTC/USD H24 experiment; Coinbase primary, Kraken cross-check; ARIMA/persistence/drift baselines. | Immutable SQLite forward ledger, pinned model checkpoint and GitHub Actions workflow. README states local tests and pinned model smoke are verified but CI execution and first live forward prediction are not yet verified; legacy 12 CSV rows are H1, not H24 evidence. | Potentially the closest asset/horizon candidate, but no verified live H24 forecast was found in this audit. No score admitted to the external leaderboard. | Repository code Apache-2.0; TimesFM 3.0 default weights separately use `timesfm-non-commercial-license-v1.0` and are restricted to non-commercial/non-production use. No code or weights copied. |
| [google/timesfm-2.5-200m-pytorch](https://huggingface.co/google/timesfm-2.5-200m-pytorch) | TimesFM 2.5 time-series foundation model; general time-series candidate. | 200M model; large checkpoint; requires compatible TimesFM/PyTorch runtime and fixed preprocessing. | Not yet run on the common BTCUSDT/BTCUSD walk-forward origins; generic benchmark claims are not BTC-specific evidence. | Model card at commit `1d952420fba87f3c6dee4f240de0f1a0fbc790e3` states Apache-2.0. No weights copied. |

### Watchlist interpretation

- The Hawkes LOB paper is relevant to a future L2/event-time branch, but 5m OHLCV cannot reconstruct order arrivals, cancellations or queue imbalance.
- Wafi et al. and the POMP preprint belong in a volatility/risk-state sub-leaderboard, not the hourly price-path leaderboard.
- TimesFM 3.0 is a candidate only for a non-commercial sandbox unless a separately licensed checkpoint is supplied; TimesFM 2.5 is the more permissively licensed candidate, subject to practical runtime and data checks.
- No new public human or algorithmic forecast was admitted to the external leaderboard because none met matching asset, venue, issue time, cutoff and +1…+24 hourly horizons with independently verifiable forward timestamps.


## Additional evidence reviewed — 2026-11-16

| Candidate / source | Method and asset / horizon | Data and reproducibility | Evidence and limitations | Status |
|---|---|---|---|---|
| Insu Choi, “Intrinsic multifractality and adaptive efficiency in Bitcoin,” Physica A 697 (2026), DOI 10.1016/j.physa.2026.131735 | q-Gaussian-rescaled multifractal diagnostics for BTC five-minute returns; no forecast horizon | Abstract reports ~774k five-minute observations, Aug 2017–Dec 2024. Full publisher text was paywalled in this review; no code/data repository verified. | Abstract reports a ~25-day scaling crossover and regime differences around spot ETF approval. These are diagnostics, not forward price forecasts; details cannot be independently audited from the abstract alone. | Methodological reference only; not a leaderboard competitor |
| Haroon, RAML, arXiv:2607.23370 (2026-07-25) | Regime-gated BiLSTM fusion of OHLCV and Reddit FinBERT sentiment; BTC-USD direction +3h/+6h | 3,491 hourly observations Jul 2024–Sep 2025; 2,146 train / 1,345 chronological test. Reddit/Kaggle sentiment data and FinBERT terms are separate; no reusable code/license found. | Reported F1 0.5474 / 0.5513; AUC 0.5084 at 3h but 0.4902 at 6h; true-down specificity 44.6%. Preprint, short sample, near-chance discrimination. | Sentiment/regime challenger for ablation only; not comparable to +1…+24 price-level nMAE |
| Figura et al., Forecasting 8(3), 41 (2026), DOI 10.3390/forecast8030041 | PLS-SEM behavioural/network/uncertainty architecture; weekly BTC future historical volatility | 262 weekly observations, Jan 2021–Jan 2026; article gives data sources but no reusable code/data bundle identified. | Reports uncertainty as the strongest immediate association, but discussion says GARCH(1,1) has lower raw forecast error. Weekly risk-state target, not hourly price path. | Risk-state research reference; no BTC hourly leaderboard score |
| Noguer i Alonso & Franklin, arXiv:2606.27100 | TimesFM-2.5, Chronos/Chronos-2, Moirai-2.0, TimeGPT vs N-BEATS/N-HiTS/PatchTST/iTransformer/KAN; daily equity returns, 20 sessions | Five US equities, 512-step context, ten rolling-origin tasks. Paper is a preprint; no BTC run in the study. | TSFMs win 8/10 task ranks, but only two task-level DM tests significantly beat zero-return random walk. Cross-asset evidence only. | Supports testing TSFM challengers on our own BTC origins; no rank transfer |
| artur-fedosiuk/btc-prediction-timesfm historical report | TimesFM daily BTC/USD forecast; target is 24h TWAP, not 24 separate hourly closes | Report generated 2026-09-25; 12 rows, 10 marked verified. README now says historical 12 CSV rows are legacy_h1 and the separate H24 SQLite collector's CI/first live prediction remain unverified. | Report claims MAE $551.11, 70% direction and 40% within range; its price-verification table shows CoinGecko values but Binance values are absent, despite the text describing dual-source cross-check. No exact issue timestamps in the report table. | Retain as an unverified historical self-reported TWAP reference; exclude from external leaderboard |

Sources:
- Choi: https://ideas.repec.org/a/eee/phsmap/v697y2026ics0378437126004711.html
- RAML: https://arxiv.org/abs/2607.23370
- Figura et al.: https://doi.org/10.3390/forecast8030041
- TSFM benchmark: https://arxiv.org/abs/2606.27100
- TimesFM report: https://github.com/artur-fedosiuk/btc-prediction-timesfm/blob/master/reports/bitcoin_report.md
- TimesFM experiment status: https://github.com/artur-fedosiuk/btc-prediction-timesfm

No external candidate provided a current, independently verifiable, timestamped BTC/USD forecast with matching issue time, cutoff, venue and 24 hourly target closes. External leaderboard remains empty for comparable entries.


## 2026-11-17 watchlist additions and reclassification

Last checked: 2026-11-17. These are research candidates and public forecast systems, not automatically comparable leaderboard entries.

| Candidate | Method / asset / horizon | Data and reproducibility | Evidence and limitations | Status |
|---|---|---|---|---|
| **HawkesTime / HawkesSign** — Raffaelli et al. (2026), [paper](https://doi.org/10.1007/s10203-026-00570-z), [code](https://github.com/Learning2Control/MultivariateHawkesLOB) | Multivariate Hawkes process over irregular LOB event streams; HawkesTime adds a continuous-time output-error model driven by base imbalance. BTC/USD next mid-price event timing/sign, sub-second to seconds, not 24h price levels. | Bitfinex BTC/USD LOB: about 3m updates in Jan 2024, ~375k mid-price changes; separate July 2025 regime sample. Requires full LOB event stream, Python `tick`, MATLAB CONTSID for the COE component. Code repo has 10 commits; exact HEAD `ecee1b7af5013e44b9ab584e93cd592aefa69fbd`. | Paper reports HawkesTime outperforming HawkesSign and a five-return moving-average baseline across 50 sampled 2-minute test scenarios; a 30-minute COE training window yielded 0.671 sign accuracy versus 0.640 (15m) and 0.631 (5m). Trading simulation explicitly omits transaction costs; authors flag unfiltered spoofing and need for volatility-aware mechanisms. This is microstructure evidence, not a 24h BTC forecast. | Strong microstructure research challenger; not runnable in our current 5m OHLCV-only pipeline. Code is GPL-3.0; no code copied. Consider a clean-room event-model implementation only if licensed data and LOB capture become available. |
| **MSPCIFormer** — Zhao, Crane & Bezbradica (2026), [paper](https://doi.org/10.1111/exsy.70343), [repository](https://github.com/cmajorsolo/MSPCIFormer) | Multi-scale patching, channel-independent Transformer. BTC/ETH/ADA daily price forecasting at 1, 3, 5, 7 and 15 days, with a five-day input window. Not hourly. | Paper: 1,728 daily observations; chronological 70/10/20 holdout and five expanding-window walk-forward folds. Data available from corresponding author on request; code repository has one commit, `6c0970462aa0412b2c664fefdbabc71cc17fb775`. | BTC walk-forward table reports MSPCIFormer lowest MSE at four of five horizons; MDA ranges roughly 0.525–0.546. No random-walk baseline, no calibrated prediction intervals, no independent replication and no 24h hourly target. Repository README says some components were adapted from PatchTST, MSGNet and iTransformer, but the repository has no LICENSE file or component-level provenance. | Daily-horizon architecture candidate only. Exclude from current hourly leaderboard. No code copied because license and inherited component provenance are unresolved. |
| **BtcForecaster** — Massimiliano Peluso, [technical article](https://blog.cubed.run/i-tried-to-predict-bitcoin-the-laziest-guess-won-825e1681c7fe), [site](https://btcforecaster.com), [claimed public JSON](https://btcforecaster.com/api/live-stats) | HAR-RV-J-style volatility ranges, updated every 5 minutes; 1h, 4h and 24h BTC/USDT terminal-price ranges. It makes no directional point-price call. | Binance BTC/USDT 5m inputs; author describes an append-only live forecast/score ledger and a public JSON endpoint. The site/API endpoint could not be retrieved in this run, so raw forecast vintages and source code were not independently checked. | Author reports early 28 Oct–2 Nov coverage of 90.1% for 1h (1,397 forecasts), 83.7% for 4h (1,361) and 76.5% for 24h (1,121). Forecasts are issued every 5m and heavily overlap; the author notes that 1,121 24h forecasts represent only about five independent daily periods. A Nov 6 Reddit post describes misses following the Oct 28 Fed decision. These are transparent self-reported diagnostics, not independently verified scores. | Unranked external range-calibration challenger. Could compare only after raw JSON becomes accessible and exact issue/target timestamps, venue and outcomes are frozen. No code or data copied. |
| **The Brier Index — BTC Oracle M1** — [public dashboard](https://www.brierindex.com/btc-index/) | EWMA-volatility scenario/range model centered on the latest Binance 00:00 UTC close; 1d, 7d and 30d terminal-close quantiles. No directional point forecast or hourly path. | Dashboard preserves past daily forecasts and displays a scorecard. Snapshot checked 2026-11-17 shows a Nov 16 forecast and explicitly states that the page is not live / has not been updated for more than two days. | Its range distribution is useful for a coarse terminal-range comparison, but its target is a daily close at 00:00 UTC and its center is persistence. It is not aligned to our hourly +1…+24 grid or 07:07 UTC issue time. | Unranked range-only comparator; not a live same-vintage competitor. |
| **Mispria — Bitcoin Up/Down hourly** — [methodology dashboard](https://mispria.com/markets/bitcoin-up-or-down-hourly) | Hourly binary probability: Binance BTC/USDT candle close above/below its open; 24 windows/day. Not a price-level forecast. | Public page reports 2,395 windows over 100 nights, snapshot as of 2026-11-15 08:02 UTC. It compares T−60s market odds with Student-t and normal models. | Page reports 49.6% Up, market Brier 0.0278, Student-t 0.0263 and normal 0.0273. This is a different binary target and market-implied probability snapshot; no individual probabilities matching our issue time are archived here. Some additional results are explicitly paper trades, not live executed forecasts. | Shadow binary-probability comparator only; exclude from price-level leaderboard. No account or trading participation. |

### Research-only candidates (not forecast competitors)

- **Persistent structural regimes in Bitcoin transactions**, [arXiv:2611.16585](https://arxiv.org/abs/2611.16585), 12 Nov 2026: weekly on-chain hidden semi-Markov regime decomposition. Public transaction data are identified, but no runnable repository was found. It is descriptive, not causal or a trading signal.
- **Deceleration without identification**, [arXiv:2611.13962](https://arxiv.org/abs/2611.13962), 10 Nov 2026: a pre-registered, simulation-calibrated test of long-run Bitcoin power-law drift, with 2027–2030 prospective forecasts. It concerns low-frequency trend identification, not hourly prediction. Its central caution is that conclusions change when persistent deviations beyond a random walk are admitted.
- **How Do Cryptocurrencies Price Economic News?**, Federal Reserve Board working paper, 20 Mar 2026, [PDF](https://users.nber.org/~confer/conf_papers/2387/f238700/f238700.pdf): intraday event study around FOMC, CPI and NFP releases. It informs event-conditioned volatility/order-flow research but is not a forecast model.

### External comparability status

No newly reviewed external system supplied a raw, independently verifiable BTC/USD point-price forecast with the same venue, issue time, input cutoff and 24 hourly target timestamps as the 2026-11-17 LFM vintage. Keep the external point-price leaderboard empty. Range-only and binary-probability systems remain separate shadow tracks; never merge their scores with normalized hourly log-price MAE.


## Daily competitor and public-predictor update — 2026-11-17

| Candidate | Evidence checked 2026-11-17 | Horizon / data | Comparison status |
|---|---|---|---|
| Raffaelli et al. HawkesTime / HawkesSign | Publisher full text: https://link.springer.com/article/10.1007/s10203-026-00570-z. Multivariate Hawkes event-intensity model; HawkesTime adds continuous-time output-error mapping from LOB base imbalance. Bitfinex BTC/USD, about 3m millisecond LOB updates (Jan 2024), plus July 2025 robustness sample. Linked implementation uses tick and MATLAB CONTSID. | Next mid-price event time/sign; 30m training + 2m test per sampled 32m window. | Microstructure challenger only if clean-room implementation and compatible BTC/USD LOB feed become available. Not comparable to 24 hourly price levels. |
| Takaishi quantum-circuit volatility | https://www.mdpi.com/2504-3110/10/7/442. Single-qubit QCL, daily realized volatility from Bitstamp 5m prices (913 days), MFDFA diagnostics. | Daily volatility/stylized facts, not 24h price. | Research diagnostic only. No train/test split; fitted on full sample; article explicitly does not assess predictive performance. |
| Mispria BTC hourly Polymarket market + Student-t model | https://mispria.com/markets/bitcoin-up-or-down-hourly and https://mispria.com/markets. Public replay reports 2,419 BTC hourly binary windows over 100 nights (Aug 7–Nov 15, 2026); T−60s favourite win rate 96.2%, market Brier about 0.0276 and Student-t model Brier about 0.0262 in the summary snapshot. Resolution uses Binance BTC/USDT hourly candle close vs open. | Binary direction at the final minute of each hourly window; public model-vs-market Brier. | Separate shadow benchmark only. Different issue time, target, horizon and score; not comparable to 24h price path. Site-reported replay, not independently audited. |
| Akbar human-vs-automated attention study | https://doi.org/10.1108/SEF-12-2025-0942. Abstract: 16m+ BTC tweets; attention vs polarity in GARCH-X/VAR. | Volatility/attention; no stable direction claim. | Methodology watch only; full text/data unavailable; no reuse. |
| Vu & Nguyen anti-herding study | https://doi.org/10.1108/RBF-06-2025-0254. CSSD/CSAD, BTC + 25 altcoins, 2020–2024. | Cross-sectional dispersion/regimes. | Behavioral regime hypothesis, not a comparable forecast. Full text unavailable. |

No new external public forecast was admitted to the price-level leaderboard. Mispria is retained only in a separate binary-probability shadow track.

## Public probabilistic benchmark update — 2026-11-17

Mispria's public Polymarket analytics track record (data through 2026-11-15, consolidated 2026-11-16 08:01 UTC) reports 124 nights and 187,361 graded windows. Across its combined 12-market universe (BTC/ETH/SOL/XRP × 5m/15m/1h), the order-book Brier is 0.0550 versus 0.0575 for the model, so the market is better in the aggregate. The separate BTC hourly page reports 2,419 windows over 100 nights; its T−60s snapshot reports market Brier 0.0276 versus Student-t model Brier 0.0262 and a 96.2% T−60s favourite win rate. A single-night Nov 15 report reverses the model comparison (0.0596 model vs 0.0574 market). These are publisher/operator-reported paper results, not independently audited. The methodology note explicitly warns that 5m/15m/1h windows overlap and assets co-move, so treating all windows as independent understates uncertainty. The hourly market resolves by Binance BTC/USDT 1h candle close vs open. This is a useful probability/calibration shadow benchmark near T−60s, not a comparable 24-hour hourly price-path forecast; do not rank it against LFM nMAE.


## Public forecast and research watch — 2026-11-18

| Candidate | Public claim / method checked | Horizon and data | Status / caveat |
|---|---|---|---|
| EdgeMap | Homepage reports 61% directional accuracy over 108 resolved hourly predictions, 30-day candle patterns plus momentum, wick, funding, open-interest and recent price signals. It advertises a transparent prediction history, but the checked page displays inconsistent/demo-looking BTC prices and example times; no immutable timestamped ledger, cutoff or accuracy denominator was independently verified. | Hourly BTC UP/DOWN; 30-day rolling context. | Unverified self-reported directional claim; not rankable and not a 24-hour price path. https://edgemap.io/ |
| AnalogQuant public mirror | Public mirror reports 70% prediction bands with 64.7% hit rate for 15m (n=14,071) and 64.2% for 60m (n=14,068); high-confidence 60m tier reports 49.3% (n=73). | 15m/60m, Kalshi flow/OI terrain and model range. | Coverage below nominal 70% suggests undercoverage; small high-confidence n. Page last-sync shown as 2026-10-13 and BTC spot $81,500, inconsistent with our Nov 18 archived Binance reference ($64,684.16), so treat the mirror as stale, not live evidence. https://forecast.analogquant.com/ |
| Sentiment-augmented POMP | Daily BTC F&G, latent volatility with Student-t observation noise; conditional log-likelihood and filter stability claims. | Daily volatility state, 2020–Apr 2025 sample. | Research challenger for risk-state only; not an hourly price forecaster. The code repo has no visible license; no reuse. https://arxiv.org/abs/2609.23250 |
| Complexity-based exchange anomaly framework | 1-minute trade count/volume/return, multifractality, entropy and cross-correlations; published in Entropy 28(7), 804. | Exchange quality/liquidity diagnostics. | Diagnostic lead, not a forecast competitor; anomaly is exchange-specific and does not prove wash trading. https://doi.org/10.3390/e28070804 |

### Comparability decision

No external candidate supplied a timestamped, independent BTC/USD 24-step hourly price forecast with matching issue time, cutoff, venue and scoring. The external price-level leaderboard remains empty. EdgeMap direction calls and AnalogQuant short-horizon probability/range outputs remain separate shadow tracks; their advertised accuracy is not independently verified.
