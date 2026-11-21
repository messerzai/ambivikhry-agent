# Living Fractal Market — daily research report 10

Date: 2026-11-21  
Branch: `research/living-fractal-market`  
Research scope: BTC/USDT 5m-input challenger; hourly target path +1…+24. No validated BTC/USD hourly champion exists.

## Repository and workflow

- Daily trigger commit: [3779cde61567700c83f2b8cd814ee0b132e6e0a6](https://github.com/messerzai/ambivikhry-agent/commit/3779cde61567700c83f2b8cd814ee0b132e6e0a6).
- Forecast workflow: [run 44882171137](https://github.com/messerzai/ambivikhry-agent/actions/runs/44882171137) — completed successfully; offline tests, public-data retrieval, forecast generation and artifact upload all passed.
- Archive workflow: [run 44882171128](https://github.com/messerzai/ambivikhry-agent/actions/runs/44882171128) — completed successfully; exact forecast artifact archived with no errors.
- Archive commit: [5be6cf11b4eb8d2ba0baa9193c8fcf44829da434](https://github.com/messerzai/ambivikhry-agent/commit/5be6cf11b4eb8d2ba0baa9193c8fcf44829da434).
- Research commits: [competitor watchlist](https://github.com/messerzai/ambivikhry-agent/commit/ef752a2be93bbc65c4b498483937070710d3017d), [license audit](https://github.com/messerzai/ambivikhry-agent/commit/be239ee13ed2c76294d0d3ad895665c3f27d6267).
- General CI: Python 3.10, 3.11, 3.12 and 3.13 each passed 54 tests. Forecast-specific offline suite: 13/13 passed; evaluation suite: 13/13 passed; archive suite: 12/12 passed.

## Live 5m data and current challenger output

Exact workflow artifact was downloaded and verified:

- Artifact ID: `14698143965`; workflow run: `44882171137`.
- Canonical ZIP: `forecasts/2026-11-21/2026-11-21T07-51-41.343658Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip`.
- ZIP SHA-256: `4c9c619494a7c332d2436af14480858feceb32474b1efb90e1b8fdb690860635`.
- Extracted JSON SHA-256: `f6ce1b5019157ba996f36cbe4065358ffc0f1cea0af77bf48986336360db7249`.
- Schema/vintage: `lfm.forecast.5m.v2` / `lfm5m-2026-11-21T07:51:41.343658Z-BTCUSDT-binance-spot-council-0.4`.
- Issued UTC: `2026-11-21T07:51:41.343658Z`; retrieved UTC: `2026-11-21T07:51:41.338780Z`; data cutoff: `2026-11-21T07:49:59.999000Z`.
- Feed: [Binance public Spot klines](https://data-api.binance.vision/api/v3/klines), BTC/USDT, 5m input; 999 closed candles (about 83h 15m); reference close 57,851.73 USDT.
- Model: `LFM-5m-Downside-Aware-Council-0.4`, commit `3779cde61567700c83f2b8cd814ee0b132e6e0a6`; deterministic rolling features, no fitted weights.
- Target grid: 24 hourly points from 2026-11-21 08:00Z through 2026-11-22 07:00Z.

**No BTC/USD champion forecast is issued.** The following is an experimental BTC/USDT challenger path from `LFM5mEnsemble`, not a validated predictor or trading signal:

| Horizon | Target UTC | Point (USDT) |
|---:|---|---:|
| +1h | 2026-11-21 08:00 | 57,814.47 |
| +2h | 2026-11-21 09:00 | 57,783.10 |
| +3h | 2026-11-21 10:00 | 57,756.71 |
| +4h | 2026-11-21 11:00 | 57,734.50 |
| +5h | 2026-11-21 12:00 | 57,715.83 |
| +6h | 2026-11-21 13:00 | 57,700.15 |
| +7h | 2026-11-21 14:00 | 57,687.00 |
| +8h | 2026-11-21 15:00 | 57,675.99 |
| +9h | 2026-11-21 16:00 | 57,666.78 |
| +10h | 2026-11-21 17:00 | 57,659.10 |
| +11h | 2026-11-21 18:00 | 57,652.72 |
| +12h | 2026-11-21 19:00 | 57,647.43 |
| +13h | 2026-11-21 20:00 | 57,643.07 |
| +14h | 2026-11-21 21:00 | 57,639.49 |
| +15h | 2026-11-21 22:00 | 57,636.58 |
| +16h | 2026-11-21 23:00 | 57,634.23 |
| +17h | 2026-11-22 00:00 | 57,632.37 |
| +18h | 2026-11-22 01:00 | 57,630.90 |
| +19h | 2026-11-22 02:00 | 57,629.78 |
| +20h | 2026-11-22 03:00 | 57,628.96 |
| +21h | 2026-11-22 04:00 | 57,628.37 |
| +22h | 2026-11-22 05:00 | 57,628.00 |
| +23h | 2026-11-22 06:00 | 57,627.81 |
| +24h | 2026-11-22 07:00 | 57,627.77 |

At +24h, council points were: RandomWalk 57,851.73; Momentum5m 57,405.40; MeanReversion5m 57,897.32; VolatilityRegime5m 57,611.21; TakerFlow5m 57,845.60; DownsideStress5m 56,945.07; LFM5mEnsemble 57,627.77 USDT.

The model's Gaussian-style P90 bands are explicitly **uncalibrated**; no calibrated P50/P90 intervals exist. The downside diagnostic's 70,000 USDT threshold is already below the reference price; its uncalibrated terminal-state estimate is not a first-passage probability. No breach prediction is implied.

**Data-quality warning:** the forecast artifact contains source, timestamps, 999-candle count and summary diagnostics, but not the raw 5m response bytes or their SHA-256. The exact raw input revision therefore cannot yet be independently reconstructed from the forecast artifact. The next workflow patch should archive the exact raw response, request URL and SHA-256 alongside the forecast, and test that its last closed candle matches the declared cutoff.

## Previous vintage and tournament state

The evaluation workflow [run 44882171120](https://github.com/messerzai/ambivikhry-agent/actions/runs/44882171120) completed successfully at 07:51:39Z. It passed 13 evaluator tests and reported 11 already evaluated, 0 newly evaluated, 0 failed and 1 pending **at that execution time**. The Nov 20 vintage's last target close is 2026-11-21T07:59:59.999Z, so it was correctly still pending when the job ran. The newly archived Nov 21 vintage is also pending until 2026-11-22T07:59:59.999Z. No evaluation score or research points are assigned to either pending vintage.

The latest completed comparisons remain the Nov 18 and Nov 19 single-vintage results in the ledger. MeanReversion5m ranked first on both, but uncalibrated intervals disqualify point awards. No champion promotion.

## Research discoveries — facts vs hypotheses

### Facts from published sources

1. **Source decomposition matters.** Drożdż et al., *Future Internet* 17(10), 470 (2025), apply MFCCA/MFDFA and a q-Gaussian distribution-rescaling method to BTC, ETH, DEX and NFT series. They report that temporal correlations are necessary for the observed multifractality; heavy tails broaden the spectrum conditionally, while shuffling removes the multifractal spectrum in their sufficiently long samples. Their own methods section warns that short heavy-tailed series can produce spurious spectra. DOI: https://doi.org/10.3390/fi17100470.
2. **Scale dependence remains an open diagnostic issue.** Choi (2026), *Physica A* 697, 131735, reports about 774,000 five-minute BTC observations (2017–2024), q-Gaussian rescaling, a roughly 25-day crossover and a decline in the Market Deficiency Measure after spot ETF approval. The publisher full text was not accessible in this pass; treat this as an abstract-level result, not independently reproduced evidence. DOI: https://doi.org/10.1016/j.physa.2026.131735.
3. **Microstructure and jumps.** Kitvanitphasu, Kyaw, Likitapiwat & Treepongkaruna (2026), *Research in International Business and Finance* 81, 103163, use high-frequency BTC data, VPIN and VAR; they report VPIN predicts subsequent price jumps and note time-zone/day-of-week effects. This supports a jump-risk ablation, not a directional hourly-price claim. DOI: https://doi.org/10.1016/j.ribaf.2025.103163.
4. **Attention is not sentiment polarity.** Akbar (2026), *Studies in Economics and Finance*, DOI 10.1108/SEF-12-2025-0942, reports from a 16M+ tweet study that polarity/hype/anxiety do not predict returns across specifications, while attention is associated with conditional variance and often reacts to price shocks. Publisher access is restricted; treat the claim as abstract-level and do not reuse data.
5. **News × sentiment should be event-conditioned.** Huynh (2026), *Journal of Behavioral and Experimental Finance*, 101183, DOI 10.1016/j.jbef.2026.101183, studies high-frequency responses to U.S. macro announcements across top-100 cryptoassets and reports sentiment-dependent response heterogeneity. It does not establish a generic sentiment-to-return edge; TRMI/vendor data rights are separate.
6. **TSFM rankings are not financial skill.** Noguer i Alonso & Franklin (2026), arXiv:2606.27100, compare TSFMs and train-from-scratch models on five U.S. equities. TSFMs win 8/10 task rankings, but only two one-sided DM tests are significant against random walk; iTransformer wins both META tasks. The benchmark is not BTC hourly.
7. **Finance-specific evaluation is emerging.** Lee et al., *FinVerse* (2026), arXiv:2608.03259, report 116,897 financial series, 171.1M observations and 43 public TSFMs, with 11 metric families/78 metrics. This is a benchmark-design reference, not a comparable live BTC forecast ledger.
8. **Non-stationarity should be tested, not presumed.** Pontiggia's preprint arXiv:2507.00575 reports multifractal BTC realized-volatility scaling but no significant stationarity/structural-break evidence in its tests. Its arXiv date and manuscript title-page date disagree; retain that caveat.

### Hypotheses for the next experiments

- Use q-Gaussian PDF reshaping, shuffled surrogates, IAAFT/phase-randomized controls and block-bootstrap uncertainty before labeling any rolling BTC window multifractal.
- Test VPIN-like order-flow toxicity only with point-in-time trade/volume data and robust jump tests; spot taker-buy imbalance is not order-book depth or true VPIN.
- Treat attention and news surprise as volatility/risk-state covariates first; only test direction after event-time leakage controls and ablation against simple volatility baselines.
- Evaluate TSFMs against random walk using identical BTC venue, issue time, cutoff, horizon grid and calibration protocol.

## Competitor watchlist and licenses

- Added FinVerse as a financial benchmark reference and zsfm-rs as an optional Rust/GGUF inference runtime. zsfm-rs code is MIT at HEAD `9fe86d098fd822ebedc309b3fa297d13e660b6c8`; its own guide says converted weights retain original licenses.
- Chronos-2 code and weights: Apache-2.0; official card reports general TSFM benchmark performance but no BTC-specific proof. TimesFM 2.5 code/weights: Apache-2.0. Moirai-2.0-R-Small code is Apache-2.0 but the checkpoint is CC-BY-NC-4.0. No code, weights, datasets or external benchmark payloads copied.
- No external predictor has a verifiable matching BTC/USD 24-step hourly path. External point-price leaderboard remains empty. CrunchDAO Synth is a different density/CRPS task; CryptoOracle's endpoint-only public results and direction-only human panels remain non-comparable.

## Internal leaderboard and virtual points

- At the latest ledger snapshot: 13 archived BTC/USDT vintages are expected after the Nov 21 archive; 11 completed evaluations, 2 pending until their final closes. The daily evaluation artifact was generated before the Nov 20 final close and therefore did not score it.
- No calibrated prediction intervals; no comparable external price-path score; no 30 non-overlapping completed vintages. **Virtual research points: 0. Champion promotion: none.**
- Overlapping vintages and serially dependent horizons are not independent samples.

## Code/docs changed and next experiment

- Changed: `COMPETITOR_LANDSCAPE.md` and `THIRD_PARTY_LICENSES.md`; no forecasting model or execution code changed.
- Next code patch: fix the evaluator's exact final-close boundary. Its pending check currently uses `final_close > now`, while the candle validator rejects `close_ms >= now_ms`; at exact equality this can proceed to a fetch and fail rather than remain pending. Change the pending condition to `final_close >= now` and add a regression test proving no actual-data fetch occurs at equality. Commit after the Nov 20 target close so the evaluation workflow reruns with fully closed targets.
- Next data patch: preserve raw Binance 5m response bytes, request URL and SHA-256 in the artifact; verify the final closed candle equals `data_cutoff_utc`.
- Then extend the historical input beyond the current 999-bar (~3.5-day) cap before multifractal estimation; 90 days is a starting target, not a proven sufficient sample.

Research only; not financial advice. No trading, order execution, transfers or account credentials.
