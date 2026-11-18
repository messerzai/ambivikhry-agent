# Daily research report — 2026-11-18 (run 7)

Branch: `research/living-fractal-market`  
[Branch](https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market)  
Daily marker commit: [82ab29ef](https://github.com/messerzai/ambivikhry-agent/commit/82ab29ef24836e8ca13ecd875e4cb7df96d9a9c9)  
Archive commit: [5bf7989](https://github.com/messerzai/ambivikhry-agent/commit/5bf7989ece0f3d1e4bed07fbde109077be460fa9)  
Branch comparison: **145 commits ahead, 0 behind main**. Main unchanged.

## Run and artifact verification

- Forecast workflow [44256430979](https://github.com/messerzai/ambivikhry-agent/actions/runs/44256430979): success; offline tests 13/13; live Binance public data retrieval, forecast JSON generation and upload all succeeded.
- Evaluation workflow [44256431018](https://github.com/messerzai/ambivikhry-agent/actions/runs/44256431018): success; evaluator tests 11/11; one newly completed vintage evaluated, six already evaluated, two pending at workflow cutoff, zero failures.
- Archive workflow [44256430969](https://github.com/messerzai/ambivikhry-agent/actions/runs/44256430969): success; archive tests 12/12; exact forecast/evaluation artifacts preserved and committed. Current pending count becomes three after the Nov 18 vintage is archived.
- General CI [44256430973](https://github.com/messerzai/ambivikhry-agent/actions/runs/44256430973): 52 passed on Python 3.10, 3.11, 3.12 and 3.13.
- Artifact ZIP SHA-256: `e7c9e9308cf7ce20e8ba3f6c0060c05d7dda7a1657ab7f2c4d630dbd25868b6f`.
- Extracted forecast JSON SHA-256: `61f15905898f5c3129f6be1958e443aae68a9cc9ecbfb6bad8e0e12bdeeca4cd`.
- Forecast JSON schema: `lfm.forecast.5m.v2`; model commit: `82ab29ef24836e8ca13ecd875e4cb7df96d9a9c9`.

## Current forecast

**BTC/USDT — Binance Spot**, input 5m, hourly close targets; this is a challenger, not a validated BTC/USD champion.

- Issue UTC: 2026-11-18T07:07:36.524004Z
- Retrieved UTC: 2026-11-18T07:07:36.520350Z
- Cutoff UTC: 2026-11-18T07:04:59.999Z
- Reference: **64,684.16 USDT**
- Closed candles: 999 (83h15m)
- Targets: 2026-11-18 08:00Z through 2026-11-19 07:00Z
- LFM5mEnsemble +24: **64,803.50 USDT (+0.1845%)**
- Approximate, uncalibrated P90-style +24 range: **61,780.85–67,974.03 USDT**.

Diagnostics: fast 1h return +0.115%; 4h trend +0.084%/h; 12h +0.072%/h; trend agreement 0.991; volatility ratio 0.316; taker-buy imbalance −0.261; relative quote volume 0.540; hourly sigma 0.593%. Trend is positive but taker-flow is negative and volume is below the model's recent reference. Signals are weak/discordant; do not interpret the small ensemble drift as strong conviction.

### Ensemble trajectory (USDT)

| h | Target UTC | Price |
|---:|---|---:|
| 1 | Nov 18 08:00 | 64,704.27 |
| 2 | Nov 18 09:00 | 64,721.32 |
| 3 | Nov 18 10:00 | 64,735.74 |
| 4 | Nov 18 11:00 | 64,747.91 |
| 5 | Nov 18 12:00 | 64,758.16 |
| 6 | Nov 18 13:00 | 64,766.77 |
| 7 | Nov 18 14:00 | 64,773.99 |
| 8 | Nov 18 15:00 | 64,780.01 |
| 9 | Nov 18 16:00 | 64,785.01 |
| 10 | Nov 18 17:00 | 64,789.16 |
| 11 | Nov 18 18:00 | 64,792.56 |
| 12 | Nov 18 19:00 | 64,795.35 |
| 13 | Nov 18 20:00 | 64,797.60 |
| 14 | Nov 18 21:00 | 64,799.40 |
| 15 | Nov 18 22:00 | 64,800.82 |
| 16 | Nov 18 23:00 | 64,801.91 |
| 17 | Nov 19 00:00 | 64,802.73 |
| 18 | Nov 19 01:00 | 64,803.31 |
| 19 | Nov 19 02:00 | 64,803.69 |
| 20 | Nov 19 03:00 | 64,803.90 |
| 21 | Nov 19 04:00 | 64,803.96 |
| 22 | Nov 19 05:00 | 64,803.91 |
| 23 | Nov 19 06:00 | 64,803.75 |
| 24 | Nov 19 07:00 | **64,803.50** |

### Council +24 comparison

| Model | +24 USDT |
|---|---:|
| RandomWalk | 64,684.16 |
| Momentum5m | 64,939.77 |
| MeanReversion5m | 64,641.77 |
| VolatilityRegime5m | 64,844.52 |
| TakerFlow5m | 64,674.49 |
| DownsideStress5m | 64,659.27 |
| LFM5mEnsemble | 64,803.50 |

No interval is calibrated. P90-style width is approximately 6.85% of price, which is very broad; full coverage alone is not a useful calibration success. The 70,000 USDT terminal-state heuristic is not a first-passage probability; reference is already below 70,000.

## Previous-vintage evaluation

The Nov 16 07:11Z forecast completed its 24 target hourly closes. Exact Binance Spot 1h response is archived; target close at 2026-11-17T07:59:59.999Z.

| Model | normalized MAE | Dir. vs issue | Hour-to-hour dir. | P90 coverage |
|---|---:|---:|---:|---:|
| VolatilityRegime5m | **0.668837** | 0.583 | 0.500 | 1.00 |
| Momentum5m | 0.669705 | 0.583 | 0.500 | 1.00 |
| LFM5mEnsemble | 0.670892 | 0.583 | 0.500 | 1.00 |
| MeanReversion5m | 0.709003 | 0.583 | 0.500 | 1.00 |
| TakerFlow5m | 0.736153 | 0.583 | 0.208 | 1.00 |
| RandomWalk | 0.736703 | 0.000 | 0.000 | 1.00 |
| DownsideStress5m | 0.736703 | 0.000 | 0.000 | 1.00 |

Baseline losses: RandomWalk 0.736703; VolatilityCappedSlowDrift 1.760475. The strongest simple baseline performed poorly in this single vintage, but this does not establish robust model skill. Intervals are uncalibrated; virtual points = **0**. No champion promotion.

## Research update

1. **ECB R-RISI** (Working Paper 3276, 24 Aug 2026; blog 12 Nov): 9m+ Reddit posts, LLM labels and engagement weighting; BTC-specific index is volatile and diverges from price more often than equity sentiment series. The short-term predictive claim is strongest for next-day equity returns in market stress, not BTC. Source: https://www.ecb.europa.eu/press/blog/date/2026/html/ecb.blog20261112~a4c8b903d9.en.html
2. **Complexity-based exchange anomaly** (Zwydak et al., Entropy 28(7), 804; 15 Jul 2026): one-minute trade count/volume/return diagnostics across 4 exchanges; Bitget BTC/ETH anomaly from mid-May 2025, but no proof of wash trading. Source: https://doi.org/10.3390/e28070804
3. **Extremity Premium** (Farzulla, arXiv:2602.07018): controlled effect modest and exploratory; within-quintile primary endpoint does not survive multiple correction, residual correlation with volatility is not significant. Source: https://arxiv.org/abs/2602.07018
4. **Fear Moves Markets POMP** (arXiv:2609.23250): daily F&G/volatility model improves fit/filter stability; not an hourly point forecast. Repository has no visible license; no reuse. Source: https://arxiv.org/abs/2609.23250

## Competitor watch

- **EdgeMap** claims 61% accuracy across 108 resolved hourly BTC direction calls; no independently verified immutable ledger, cutoff or denominator; page example prices appear stale/demo. Shadow-only.
- **AnalogQuant** mirror reports 64.2% hit rate on its 70% hourly band over 14,068 resolved, but its last-sync timestamp is 2026-10-13 and displayed $81,500 spot conflicts with this vintage's $64,684.16. Treat as stale, not live.
- No matching external BTC/USD 24-step price forecast. External leaderboard remains empty.

## License audit

No code, weights, datasets, social posts, order-book records, API payloads or paid services were reused. Farzulla's code repository is MIT at checked HEAD d6fb70f; POMP repo HEAD 4905198 has no visible LICENSE; Zwydak paper CC BY 4.0, no implementation/license identified. Our proprietary root license remains unchanged. Details: THIRD_PARTY_LICENSES.md.

## Next experiment

Build a paginated, exact-provenance 90-day Binance Spot 5m dataset. Add exchange-quality diagnostics (trade-count/quote-volume anomaly and rolling entropy/multifractal checks) as **data-quality/risk gates**, then test their incremental contribution against volatility-only features on non-overlapping daily origins. Sentiment/news features must have point-in-time timestamps and verified data terms. No forecast equations changed in this run.

Research, not financial advice; no trade execution.
