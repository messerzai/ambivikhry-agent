# Daily research report — 2026-11-17 (Run 6)

Branch: `research/living-fractal-market`  
Branch URL: https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market  
Research cycle UTC: 2026-11-17 07:06–07:08  
No changes were made to `main`.

## 1. Branch and workflow status

- Daily trigger marker committed once: `lfm-daily-20261117-0706z-r7`.
- Forecast run: [44036313436](https://github.com/messerzai/ambivikhry-agent/actions/runs/44036313436) — success.
- General tests: [44036313462](https://github.com/messerzai/ambivikhry-agent/actions/runs/44036313462) — success on Python 3.10, 3.11, 3.12 and 3.13.
- Completed-vintage evaluation: [44036313474](https://github.com/messerzai/ambivikhry-agent/actions/runs/44036313474) — success.
- Immutable archive: [44036313519](https://github.com/messerzai/ambivikhry-agent/actions/runs/44036313519) — success.
- Forecast workflow steps verified: offline tests, live public-data retrieval, forecast generation and artifact upload all succeeded. Evaluation logic, completed-vintage evaluation and exact actual-data artifact upload succeeded. Archive redirect handling and exact artifact preservation succeeded.
- Branch comparison at the archive commit: 128 commits ahead of `main`, 0 behind. The branch remained isolated.

## 2. Research discoveries

### High-frequency microstructure

Raffaelli, Cestari, Marazzina et al. (17 Apr 2026), [Forecasting Bitcoin price movements using multivariate Hawkes processes and limit order book data](https://doi.org/10.1007/s10203-026-00570-z). The study uses Bitfinex BTC/USD LOB events (about 3 million updates and 375,000 mid-price changes in Jan 2024) and a separate July 2025 regime sample. HawkesTime combines multivariate event excitation with a continuous-time output-error model and base imbalance; the paper reports 0.671 sign accuracy for a 30-minute COE training window, versus 0.640 and 0.631 for 15- and 5-minute windows. Evaluation uses 50 sampled 2-minute test periods. Trading simulations omit transaction costs; spoofing is not filtered. This is a next-event microstructure model, not a 24h point-price model. Linked code is GPL-3.0; no source code was copied.

### Macro-news surprise

Kroner, Mohammed and Vega, Federal Reserve Board working paper, 20 Mar 2026: [How Do Cryptocurrencies Price Economic News?](https://users.nber.org/~confer/conf_papers/2387/f238700/f238700.pdf). The event study uses minute-level CoinDesk data covering 158 exchanges and 18,403 pairs during 2015–2025, focusing on BTC/USD and ETH/USD on Binance, OKX and Coinbase around FOMC, CPI and NFP. Volatility, volume and spreads spike at releases and generally revert within 15–30 minutes; contractionary policy and higher-yield surprises are associated with negative BTC/ETH price responses. Order-flow impact differs across exchanges and changed around 2021. This motivates a point-in-time event-state ablation, not a pre-release direction signal.

### Sentiment-conditioned news response

Nhan Huynh (June 2026), [Tuning into the news](https://doi.org/10.1016/j.jbef.2026.101183), reports that one standard deviation higher cryptocurrency sentiment attenuates the return response to macro surprises by about 16% and turnover response by about 24%. The result is a conditional response effect across the top 100 cryptocurrencies, not a BTC-only hourly forecast. TRMI data are proprietary and were not used.

### Slow regimes and trend identifiability

- [Persistent structural regimes in Bitcoin transactions](https://arxiv.org/abs/2611.16585), 12 Nov 2026: weekly on-chain HSMM decomposition over about 760 weeks. The authors note only three completed falling phases, serial dependence, market-informed segmentation choices and no causal identification. No runnable code was identified.
- [Deceleration without identification](https://arxiv.org/abs/2611.13962), 10 Nov 2026: a pre-registered, simulation-calibrated test of long-run Bitcoin power-law drift. The rejection does not survive allowing persistence beyond a random walk; a Gompertz ceiling fits about as well. This is a warning about effective sample size and trend extrapolation, not an hourly model.

### Daily-horizon transformer

Zhao, Crane and Bezbradica (2026), [MSPCIFormer](https://doi.org/10.1111/exsy.70343): 1,728 daily observations, five-day input window, 1/3/5/7/15-day horizons, chronological holdout and five expanding-window folds. The paper reports good BTC walk-forward MSE at four of five horizons, but MDA is only about 0.525–0.546; no random-walk baseline or calibrated intervals are reported. It is not comparable to our hourly task. Its GitHub repository has no LICENSE file and acknowledges inherited components without a clear component-level license manifest; no code was copied.

## 3. Competitor watchlist changes

Added or reclassified:
- HawkesTime/HawkesSign: GPL-3.0 implementation, LOB-event seconds-scale candidate; not runnable from current 5m OHLCV.
- MSPCIFormer: daily multi-scale Transformer candidate; no verified code license; excluded from hourly leaderboard.
- BtcForecaster: self-reported 1h/4h/24h range forecaster. The author reports 76.5% 24h range coverage over 1,121 heavily overlapping 5-minute-issued forecasts during an early five-day period; raw JSON endpoint was inaccessible, so no independent scoring.
- The Brier Index: daily Binance 00:00 UTC terminal ranges; its 16 Nov page explicitly says it is not live.
- Mispria: hourly binary BTC/USDT close-vs-open probabilities; 2,395 windows / 100 nights and a displayed 15 Nov Brier snapshot. Different target from price-level forecasting.
- No external system provided an independently verifiable, matching BTC/USD point-price forecast with the same issue time, venue, cutoff and 24 hourly targets. External point-price leaderboard remains empty.

## 4. License audit

- Hawkes LOB repository HEAD `ecee1b7af5013e44b9ab584e93cd592aefa69fbd`, exact repository license GPL-3.0. No code copied; the project root LICENSE is proprietary v1.0 and restricts redistribution/derivative distribution, so GPL-3.0 integration is not assumed compatible. Any future integration requires qualified license review and an explicit source-disclosure plan.
- MSPCIFormer repository HEAD `6c0970462aa0412b2c664fefdbabc71cc17fb775`; no LICENSE/NOTICE found; no code copied.
- BtcForecaster, Brier Index and Mispria: no code/data reuse license verified; no payloads copied.
- Huynh article marked open access under a Creative Commons license, but exact identifier not verified; TRMI data are separately proprietary.
- Baquero/Menezes companion Zenodo software license metadata could not be retrieved; no software copied.
- No third-party code, weights, datasets, raw posts, LOB events, sentiment feeds or paid APIs were used.

Full register: [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## 5. Live forecast — experimental challenger, not champion

- Model: `LFM-5m-Downside-Aware-Council-0.4`
- Instrument: **BTC/USDT**, Binance Spot; input 5m candles; hourly targets.
- Issue UTC: `2026-11-17T07:07:54.530285Z`
- Data cutoff UTC: `2026-11-17T07:04:59.999Z`
- Reference: `64,636.92 USDT`
- Closed candles: 999 (about 83.25 hours)
- Targets: +1 at 08:00Z Nov 17 through +24 at 07:00Z Nov 18.
- LFM5mEnsemble +24: `64,752.64 USDT` (+0.179%).
- DownsideStress5m +24: `63,704.38 USDT` (-1.442%).
- P90-style bands in the JSON are uncalibrated and must not be represented as calibrated intervals.

Exact workflow artifact:
- [Forecast run 44036313436](https://github.com/messerzai/ambivikhry-agent/actions/runs/44036313436), artifact ID `14307092772`.
- [Archived exact ZIP](forecasts/2026-11-17/2026-11-17T07-07-54.530285Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip)
- ZIP SHA-256: `1f316174dbf4bd2b6e170a39e47727ebdf651bc0083326783a7f6edbda79a02b`
- Extracted JSON SHA-256: `4ff5c1500873e2284b1dda489ffc8a04a10430cd5acfe25ed962c2ab0ebd381c`
- Source checkout commit: `c185df4a7d113b924905338b430dbc1b5b5f1213`.

The emitted JSON lacks explicit `input_interval`, `retrieved_at_utc`, `model_commit`, `vintage_id` and `training_cutoff`; the ledger preserves the workflow commit and hashes. These fields should be added in a future schema/code change. The current 999-candle window is far shorter than the planned 90-day research panel.

## 6. Previous forecast evaluation

Evaluation run: [44036313474](https://github.com/messerzai/ambivikhry-agent/actions/runs/44036313474), artifact ID `14307282513`. Two Nov 15 vintages completed, using exact Binance Spot BTCUSDT 1h actual candles. Their final target closes were available at evaluation time.

| Vintage | Best council model | Best nMAE | Random-walk nMAE | Volatility-capped drift nMAE |
|---|---|---:|---:|---:|
| Nov 12 08:03 | RandomWalk (council tie) | 9.0509 | 9.0509 | 7.3504 |
| Nov 13 07:59 | LFM5mEnsemble | 1.7186 | 1.7426 | 2.5965 |
| Nov 13 08:07 | LFM5mEnsemble | 1.8265 | 1.9175 | 2.3634 |
| Nov 14 07:18 | RandomWalk (council best) | 5.2052 | 5.2052 | 3.0107 |
| Nov 15 07:37 | MeanReversion5m | 1.3815 | 1.4026 | 2.8144 |
| Nov 15 08:09 | MeanReversion5m | 1.6231 | 1.6599 | 3.7546 |

The Nov 13 pair and Nov 15 pair overlap by more than 23 hours each; treat the six vintages as four issue-date blocks, not six independent daily samples. P90 empirical coverage ranged from 0.167 to 1.000, and calibration status is false. **Virtual points: 0. Champion: none.** The Nov 16 and Nov 17 forecast vintages remain pending.

## 7. Next experiment

1. Extend the forecast JSON with the missing immutable provenance fields and tests; do this before the next daily trigger, then run once and archive once.
2. Build a hash-pinned, paginated 90-day Binance Spot BTCUSDT 5m panel.
3. Pre-register an event study for FOMC/CPI/NFP surprises, initially targeting 15m/30m realized volatility and turnover.
4. Test point-in-time surprise × pre-release sentiment features against the volatility-aware baseline using chronological/purged origins and block-bootstrap uncertainty.
5. Keep Hawkes LOB work separate until a licensed LOB feed and compatible runtime are available.

No trading, fund movement, exchange credentials or execution integration was used. This is research, not financial advice.


## Run 6 follow-up — 2026-11-17 07:35–07:41 UTC

### Live forecast and provenance

The daily marker was updated once (marker r8) and committed with the schema-v2 provenance patch. The workflow now checks out the exact triggering commit and passes that SHA into the forecast process.

- Forecast workflow [44040279529](https://github.com/messerzai/ambivikhry-agent/actions/runs/44040279529): success. Offline forecast tests: 13/13; public Binance retrieval, forecast generation and artifact upload all succeeded.
- Evaluation workflow [44040279510](https://github.com/messerzai/ambivikhry-agent/actions/runs/44040279510): success. Evaluation tests: 11/11; six vintages already evaluated, zero newly evaluated, zero failures, two pending at that time. The new 07:38 vintage was archived afterward, so there are now three pending vintages. No target closes were yet available for the Nov 16/17 vintages.
- Forecast artifact ID 14308852672; exact ZIP SHA-256 3d7adc276605364df6b5be3cfe8554d9e67b77265e34374ea2b9b3a2b117c049; exact JSON SHA-256 2d13d9c1a208767c973420d6f51ab216df2fee08f56db62dc895ea86a303cc12.
- Archived files: forecasts/2026-11-17/2026-11-17T07-38-41.322709Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip and matching .json. Immutable ledger entry added.

Forecast schema v2 records: vintage ID lfm5m-2026-11-17T07:38:41.322709Z-BTCUSDT-binance-spot-council-0.4; model commit 90cee4a5f8e91dae85f79fb2a5deac64e47a0fc5; issue 07:38:41.322709Z; retrieval 07:38:41.318153Z; data/training cutoff 07:34:59.999Z; 999 closed Binance Spot BTCUSDT 5m candles.

Reference price: **64,655.08 USDT**. The 24 hourly LFM5mEnsemble point forecasts are:

| Horizon | Target UTC | Point (USDT) |
|---:|---|---:|
| +1 | 2026-11-17 08:00 | 64,669.05 |
| +2 | 2026-11-17 09:00 | 64,680.90 |
| +3 | 2026-11-17 10:00 | 64,690.97 |
| +4 | 2026-11-17 11:00 | 64,699.55 |
| +5 | 2026-11-17 12:00 | 64,706.90 |
| +6 | 2026-11-17 13:00 | 64,713.21 |
| +7 | 2026-11-17 14:00 | 64,718.65 |
| +8 | 2026-11-17 15:00 | 64,723.36 |
| +9 | 2026-11-17 16:00 | 64,727.46 |
| +10 | 2026-11-17 17:00 | 64,731.04 |
| +11 | 2026-11-17 18:00 | 64,734.19 |
| +12 | 2026-11-17 19:00 | 64,736.97 |
| +13 | 2026-11-17 20:00 | 64,739.46 |
| +14 | 2026-11-17 21:00 | 64,741.68 |
| +15 | 2026-11-17 22:00 | 64,743.69 |
| +16 | 2026-11-17 23:00 | 64,745.52 |
| +17 | 2026-11-18 00:00 | 64,747.19 |
| +18 | 2026-11-18 01:00 | 64,748.74 |
| +19 | 2026-11-18 02:00 | 64,750.18 |
| +20 | 2026-11-18 03:00 | 64,751.53 |
| +21 | 2026-11-18 04:00 | 64,752.80 |
| +22 | 2026-11-18 05:00 | 64,754.01 |
| +23 | 2026-11-18 06:00 | 64,755.16 |
| +24 | 2026-11-18 07:00 | 64,756.27 |

All are point forecasts. The Gaussian-style P90 envelope is uncalibrated and is not a valid calibrated prediction interval. No calibrated P50/P90 intervals exist. The +24 ensemble point is +0.1565% from the reference. Other +24 council points: RandomWalk 64,655.08; Momentum5m 64,816.24; MeanReversion5m 64,704.74; VolatilityRegime5m 64,834.17; TakerFlow5m 64,662.84; DownsideStress5m 64,655.08. These are all challenger outputs; no BTC/USD champion exists.

The 70,000 USDT downside threshold is already above the issue-time reference (reference is 7.636% below it). The reported heuristic terminal-below-threshold value 1.0 is therefore not a downward-crossing probability and is uncalibrated. The illustrative -6% stress scenario is 60,775.78 USDT and has no assigned probability.

### Archival repair

The first archive run [44040279564](https://github.com/messerzai/ambivikhry-agent/actions/runs/44040279564) failed because the archiver accepted only schema v1. The forecast itself had succeeded; no forecast bytes were altered. The archiver was extended to accept schema v1/v2 and to verify v2 provenance: model commit must equal the exact workflow source SHA, input interval must be 5m, training cutoff must equal data cutoff, and UTC timestamps must satisfy cutoff ≤ retrieval ≤ issue. Four regression tests were added.

The archive retry [44040604276](https://github.com/messerzai/ambivikhry-agent/actions/runs/44040604276) succeeded, preserving the exact ZIP and JSON hashes above. It skipped evaluation archival because the evaluation artifact contained no newly completed vintage. A formatting defect in the newly appended ledger metadata (literal backslash-n characters) was detected and is being corrected with a regression test; the existing forecast artifact and its hashes remain unchanged.

### Final test state for this follow-up

- Forecast unit tests: 13 passed.
- Evaluation unit tests: 11 passed.
- Archive unit tests: 11 passed.
- General project CI: 51 passed on Python 3.10, 3.11, 3.12 and 3.13.
- No virtual research points; six completed vintages, three pending after the latest archive.
- Branch remained isolated: 139 commits ahead of main, zero behind at 07:41 UTC; main unchanged.

No trades, fund movements or execution integrations occurred.