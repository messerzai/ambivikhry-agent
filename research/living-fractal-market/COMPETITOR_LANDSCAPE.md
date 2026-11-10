# Competitor landscape and reuse policy

Last reviewed: 2026-11-10
Target: BTC/USD, hourly observations, horizons +1 to +24 hours.
Branch: `research/living-fractal-market`

## Purpose

Build a fair, forward-blind comparison set for the Living Fractal Market champion. A model is a competitor only when its forecast is timestamped before the target period, its data cutoff is known, and the asset, venue, and forecast horizons can be aligned. Published backtests and marketing claims are useful discovery leads, not live leaderboard scores.

## Initial candidate registry

| Candidate | Family | Potential role | Evidence / limitations | Reuse status |
|---|---|---|---|---|
| ARIMA / ETS / random walk | Statistical | Mandatory simple baselines | Transparent, inexpensive; likely hard to beat at short horizons | Implement independently; common methods |
| N-BEATS / N-HiTS | Neural forecasting | Strong learned baselines | Benchstreet exposes direct/recursive implementations; its reported winner claims require independent reproduction | Audit exact repository license before copying |
| PatchTST / TFT | Transformer / multi-horizon | Multivariate and covariate challengers | Relevant architectures; test on BTC-specific chronological splits | Audit code and weights separately |
| Amazon Chronos / Chronos-2 | Time-series foundation model | Zero-shot and fine-tuned challenger | Quantile forecasts can support probabilistic scoring; model checkpoint terms must be checked individually | Do not assume code license covers weights |
| Google TimesFM | Time-series foundation model | Zero-shot challenger | Public research implementation and checkpoints; versions may carry different terms | Verify exact checkpoint and code license before use |
| FoundationForecast | Model integration framework | Common adapter for several foundation models | Unified interface supports forecasting and evaluation; framework reports Apache-2.0, while plugged-in model licenses differ | Framework marked candidate for reuse; preserve Apache-2.0 notices |
| CrunchDAO Synth / crunch-synth | Probabilistic competition | External benchmark / evaluation design | Public documentation describes 1h and 24h prediction rounds and CRPS-based scoring; access, rules and submission eligibility must be checked | Methodology may be studied; no code copied pending license audit |
| CryptoOracle | Public forecast ledger | Human-readable external reference | Publicly describes locked forecasts and reports a historical comparison where last-price baseline beat TimesFM; verify raw ledger and scoring before comparison | Reference only; no code copied |
| BitPredict | Public predictor leaderboard | Possible human/algorithmic competitor | Public page advertises free competition and 24h calls; data access and timestamp comparability need verification | No participation until rules and API terms are checked |
| Crowdsource | Public prediction competitions | Possible external contest | Public site lists live competitions including BTC/USD next-hour; automated participation, scoring details and terms need verification | No submissions until rules are audited |

## First implementation order

1. Lock a data contract: exchange/venue, UTC candle boundaries, missing-candle policy, cutoff timestamp and revision policy.
2. Implement random walk, zero-drift return, drift and volatility-aware baselines.
3. Add N-BEATS/N-HiTS and a compact tree/linear model as reproducible local challengers.
4. Add Chronos and TimesFM adapters only after checking the exact code, checkpoint, and use terms.
5. Add sentiment/news features as a separate ablation, never as a hidden advantage unavailable to competitors.
6. Mirror external competitions with an internal shadow leaderboard before attempting any external submission.
7. Use probabilistic metrics (CRPS or pinball loss, interval coverage and width) alongside the frozen primary loss.

## Fair-comparison contract

For every competitor record: model and version; source URL; forecast issue time; data cutoff; asset and venue; horizon; point or distribution forecast; actual target; scoring method; sample size; and whether the result is a genuine forward forecast, a walk-forward backtest, or an in-sample result. Do not rank incomparable records together.

## License and provenance policy

Public availability is not permission to copy. Before reuse, inspect the exact repository license and, separately, the model-weight, dataset, tokenizer, and API terms. Record:
- project/repository and immutable commit or release;
- authors and canonical source URL;
- SPDX license identifier or explicit "no license found";
- date checked and the exact component reused;
- required attribution, copyright and license notices;
- modifications and dependency versions;
- copyleft/source-disclosure obligations and distribution implications;
- unresolved compatibility questions.

Do not copy code or assets with no license, unclear terms, non-commercial restrictions incompatible with the intended use, or incompatible license obligations. In those cases, cite the public idea/paper and implement an independent clean-room version. Preserve original notices for every reused component. This register is an engineering provenance aid, not legal advice.

## Initial public discovery sources

- FoundationForecast: https://github.com/TimeCopilot/foundationforecast
- Benchstreet financial forecasting benchmark: https://github.com/puffinsoft/benchstreet
- CrunchDAO Synth model competition code: https://github.com/crunchdao/crunch-synth
- TimeLM side-by-side foundation-model demo: https://github.com/cloudy-kz/TimeLM
- CryptoOracle public forecast ledger: https://cryptooracle.moinsen.dev/
- BitPredict public prediction leaderboard: https://www.bitpredict.io/
- Crowdsource public prediction competitions: https://crowdsource.sh/
- Synth competition documentation: https://docs.crunchdao.com/real-time-competitions/competitions/synth

## Open questions for the next pass

- Which candidates provide downloadable, immutable historical forecasts suitable for independent scoring?
- Which exact model checkpoints are commercially reusable, and which are research/non-commercial only?
- Can we reproduce the strongest published results on strictly chronological BTC data without leakage?
- Do multifractal, sentiment and news features improve forecast distributions beyond simple baselines after transaction-agnostic scoring?
