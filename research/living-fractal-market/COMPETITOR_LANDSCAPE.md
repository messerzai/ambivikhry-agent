# Competitor landscape and reuse policy

Last reviewed: 2026-11-11  
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
