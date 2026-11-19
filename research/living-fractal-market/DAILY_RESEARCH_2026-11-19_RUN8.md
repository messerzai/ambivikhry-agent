# Living Fractal Market — daily research report
Date: 2026-11-19  
Branch: research/living-fractal-market  
Scope: branch only; main unchanged.

## Workflow and archival status

- 5m forecast workflow [run 44479201588](https://github.com/messerzai/ambivikhry-agent/actions/runs/44479201588): **success**. Offline tests 13/13; Binance public-data retrieval, forecast generation and artifact upload all succeeded.
- Completed-vintage evaluator [run 44479201628](https://github.com/messerzai/ambivikhry-agent/actions/runs/44479201628): **success**. Evaluator tests 11/11; 2 vintages evaluated, 1 pending, 0 failures.
- Immutable archive workflow [run 44479201553](https://github.com/messerzai/ambivikhry-agent/actions/runs/44479201553): **success**. Archive tests 12/12; exact artifacts, extracted forecast JSON, exact actual-data response and evaluation records were committed. Archive commit: [41c47fd](https://github.com/messerzai/ambivikhry-agent/commit/41c47fd09a71b49171df353b0ee002a3eeb05e7c).
- General CI [run 44479201548](https://github.com/messerzai/ambivikhry-agent/actions/runs/44479201548): **success**, 52/52 tests on each of Python 3.10, 3.11, 3.12 and 3.13.
- Forecast source commit: [04e42a8](https://github.com/messerzai/ambivikhry-agent/commit/04e42a8671b5109f5000287d20888316a6a10230). No forecast equations or model code changed in this run.

## Fresh public market data and current council forecast

**This is BTC/USDT, Binance Spot, 5m input → 24 hourly close targets. It is a challenger council, not a validated BTC/USD hourly champion.**

- Issue UTC: 2026-11-19T07:23:19.072262Z
- Retrieval UTC: 2026-11-19T07:23:19.068690Z
- Exact last closed 5m candle / data cutoff: 2026-11-19T07:19:59.999Z
- Reference: **63,602.29 USDT**
- Closed input candles: **999** (83h15m)
- Source: https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000
- Model: LFM-5m-Downside-Aware-Council-0.4; schema lfm.forecast.5m.v2; commit 04e42a8671b5109f5000287d20888316a6a10230.
- Targets: 2026-11-19 08:00Z through 2026-11-20 07:00Z, one point per hour.
- Forecast JSON SHA-256: c75289cbbf748fb11ef7d59b7730b3a4192b221902a6fd9ca90cc8aca29b4ac5.
- Exact artifact ZIP SHA-256: f675f9bb47a17d96ed92b7186d5e05607a94c42e69856c38bb4959dfed544322.
- Archive: [exact forecast artifact](https://github.com/messerzai/ambivikhry-agent/blob/research/living-fractal-market/research/living-fractal-market/forecasts/2026-11-19/2026-11-19T07-23-19.072262Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip) and [extracted JSON](https://github.com/messerzai/ambivikhry-agent/blob/research/living-fractal-market/research/living-fractal-market/forecasts/2026-11-19/2026-11-19T07-23-19.072262Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.json).

### +1…+24 hourly point paths (USDT)

| Target UTC | RandomWalk | Momentum5m | MeanReversion5m | VolatilityRegime5m | TakerFlow5m | DownsideStress5m | LFM5mEnsemble |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-19 08:00 | 63,602.29 | 63,622.09 | 63,601.35 | 63,611.42 | 63,601.36 | 63,599.80 | 63,610.72 |
| 2026-11-19 09:00 | 63,602.29 | 63,638.31 | 63,599.59 | 63,618.54 | 63,600.74 | 63,597.45 | 63,617.62 |
| 2026-11-19 10:00 | 63,602.29 | 63,651.59 | 63,597.09 | 63,623.90 | 63,600.32 | 63,595.22 | 63,623.20 |
| 2026-11-19 11:00 | 63,602.29 | 63,662.47 | 63,593.95 | 63,627.71 | 63,600.04 | 63,593.11 | 63,627.66 |
| 2026-11-19 12:00 | 63,602.29 | 63,671.37 | 63,590.24 | 63,630.15 | 63,599.85 | 63,591.12 | 63,631.16 |
| 2026-11-19 13:00 | 63,602.29 | 63,678.66 | 63,586.03 | 63,631.39 | 63,599.72 | 63,589.23 | 63,633.82 |
| 2026-11-19 14:00 | 63,602.29 | 63,684.63 | 63,581.38 | 63,631.57 | 63,599.64 | 63,587.45 | 63,635.78 |
| 2026-11-19 15:00 | 63,602.29 | 63,689.52 | 63,576.34 | 63,630.81 | 63,599.58 | 63,585.76 | 63,637.12 |
| 2026-11-19 16:00 | 63,602.29 | 63,693.53 | 63,570.95 | 63,629.23 | 63,599.55 | 63,584.17 | 63,637.94 |
| 2026-11-19 17:00 | 63,602.29 | 63,696.80 | 63,565.26 | 63,626.91 | 63,599.52 | 63,582.66 | 63,638.31 |
| 2026-11-19 18:00 | 63,602.29 | 63,699.49 | 63,559.30 | 63,623.96 | 63,599.50 | 63,581.23 | 63,638.29 |
| 2026-11-19 19:00 | 63,602.29 | 63,701.68 | 63,553.11 | 63,620.43 | 63,599.49 | 63,579.88 | 63,637.95 |
| 2026-11-19 20:00 | 63,602.29 | 63,703.48 | 63,546.70 | 63,616.41 | 63,599.48 | 63,578.60 | 63,637.32 |
| 2026-11-19 21:00 | 63,602.29 | 63,704.96 | 63,540.12 | 63,611.94 | 63,599.48 | 63,577.39 | 63,636.45 |
| 2026-11-19 22:00 | 63,602.29 | 63,706.16 | 63,533.37 | 63,607.07 | 63,599.48 | 63,576.25 | 63,635.37 |
| 2026-11-19 23:00 | 63,602.29 | 63,707.15 | 63,526.47 | 63,601.87 | 63,599.47 | 63,575.17 | 63,634.11 |
| 2026-11-20 00:00 | 63,602.29 | 63,707.96 | 63,519.46 | 63,596.35 | 63,599.47 | 63,574.14 | 63,632.69 |
| 2026-11-20 01:00 | 63,602.29 | 63,708.62 | 63,512.33 | 63,590.56 | 63,599.47 | 63,573.18 | 63,631.15 |
| 2026-11-20 02:00 | 63,602.29 | 63,709.16 | 63,505.10 | 63,584.53 | 63,599.47 | 63,572.26 | 63,629.48 |
| 2026-11-20 03:00 | 63,602.29 | 63,709.61 | 63,497.79 | 63,578.29 | 63,599.47 | 63,571.39 | 63,627.72 |
| 2026-11-20 04:00 | 63,602.29 | 63,709.97 | 63,490.40 | 63,571.85 | 63,599.47 | 63,570.58 | 63,625.88 |
| 2026-11-20 05:00 | 63,602.29 | 63,710.27 | 63,482.94 | 63,565.25 | 63,599.47 | 63,569.80 | 63,623.96 |
| 2026-11-20 06:00 | 63,602.29 | 63,710.51 | 63,475.42 | 63,558.50 | 63,599.47 | 63,569.07 | 63,621.98 |
| 2026-11-20 07:00 | 63,602.29 | 63,710.71 | 63,467.86 | 63,551.62 | 63,599.47 | 63,568.37 | 63,619.94 |

At +24, the council spans 63,467.86–63,710.71 USDT; the ensemble is 63,619.94 (+0.0278%). The ensemble's approximate P90-style +24 band is 60,785.91–66,586.11 USDT, but **all intervals are explicitly uncalibrated**; no 50% interval is supplied. Do not interpret these bands as calibrated probabilities.

Diagnostics: fast 1h log return −0.097%; 4h log-return rate +0.203%/h; 12h rate +0.159%/h; trend agreement 0.937; volatility ratio 0.772; taker-buy imbalance −0.040; relative quote volume 1.046; hourly sigma 0.566%; downside sigma 0.411%; drawdown from 24h high −1.975%. Short-term and medium-term signals are not fully aligned. The 70,000 USDT level is already above the 63,602.29 reference, so the terminal-below-level diagnostic is not a new crossing forecast.

### Data provenance warning

The workflow artifact does not contain the raw 999-candle 5m response, so this vintage has no raw-input SHA-256. The public source endpoint, retrieval time, cutoff, closed-candle count and diagnostics are recorded, and the exact forecast JSON/ZIP are archived, but a byte-for-byte replay of the model input is not yet possible. The next pipeline change should archive a lossless raw 5m snapshot and its hash.

## Previous-vintage evaluation

The evaluation artifact contains 24 contiguous Binance Spot 1h actual candles from 2026-11-17 08:00Z through 2026-11-18 07:00Z. Exact actual-data SHA-256: 5cf6b19d8d72ab4fdc3165cba04471c23dcbc4e401084a37bc6e8ee561583e54. Evaluation artifact ID 14507712215; ZIP SHA-256 f313e34f27f7f656b2c14f5fe643bf46d09595a8f0091527830e28a1d9b57884.

| Vintage issue UTC | Best model | Best nMAE | Random walk nMAE | Volatility-capped drift nMAE | Direction vs issue | Hour-to-hour direction | Points |
|---|---|---:|---:|---:|---:|---:|---:|
| 2026-11-17 07:07:54Z | TakerFlow5m | 1.073278 | 1.077813 | 1.577631 | 0.625 | 0.333 | 0 |
| 2026-11-17 07:38:41Z | RandomWalk / DownsideStress5m (tie) | 1.107709 | 1.107709 | 1.397106 | 0.000 | 0.000 | 0 |

The first vintage's TakerFlow5m nMAE beats both simple point baselines by a small margin; the second vintage's RandomWalk is best. Both use the same target period and are overlapping, not independent samples. P90 empirical coverage is 1.00 in both records, but the intervals are uncalibrated; coverage on two vintages does not establish calibration. No points are awarded. The Nov 18 vintage remains pending until its final hourly candle closes at 2026-11-19T07:59:59.999Z; the current Nov 19 vintage remains pending until 2026-11-20T07:59:59.999Z.

## Research and competitor discoveries

1. Kim, Lee & Choi (2026), DOI 10.3390/fractalfract10060353: rolling MF-DFA across 11 crypto/fiat pairs, 200/250/300-day windows, phase-randomized surrogate tests. Supports time-varying scaling diagnostics, not a BTC hourly forecast. 99 surrogates make p=0.010 the minimum attainable; daily data and request-only data limit replication.
2. Drożdż et al. (2025), DOI 10.3390/fi17100470: temporal correlations are the primary source of multifractality in their crypto samples; heavy tails broaden spectra conditionally. Do not infer predictability from a wide spectrum.
3. ECB R-RISI (Working Paper 3276, Aug 2026; blog Nov 12): LLM-labelled Reddit sentiment and engagement weighting; BTC-specific series is volatile and often diverges from price. Use only as low-frequency regime/attention context after rights and point-in-time review.
4. Competitor watch: Chronos-2 (Apache-2.0 code/weights), TimesFM 2.5 (Apache-2.0 code/weights), TimesFM 3.0 (Apache-2.0 code but non-commercial/non-production weights), and Nixtla NeuralForecast (Apache-2.0 implementations of NBEATS/NHITS/TFT/PatchTST) remain candidates, not executed competitors.
5. Mispria's BTC hourly binary track reports 2,443 windows through Nov 16 and Brier 0.0264 for its Student-t model vs 0.0278 for the market at T−60s; this is not a 24-step price forecast. The Brier Index ledger is timestamped but stale (latest displayed Nov 8).

## License audit

No third-party code, model weights, datasets, Reddit posts, dashboard payloads or paid APIs were copied. Exact code/model-card licenses and immutable code commits are recorded in THIRD_PARTY_LICENSES.md. TimesFM 3.0 weights are excluded from commercial/production use under their current license; TimesFM 2.5 and Chronos-2 model cards list Apache-2.0, but exact HF revisions must be pinned before any download.

## Next experiment

Implement a paginated, provenance-preserving 90-day Binance Spot BTCUSDT 5m dataset (25,920 closed bars), then extend toward 200–250 days if feasible. Add rolling MF-DFA/MFCCA diagnostics with multiple q/scales, finite-size checks, shuffled/phase-randomized/IAAFT nulls and block bootstrap. Treat complexity and trade-count/quote-volume features first as data-quality/liquidity gates. Test incremental value over volatility-only baselines on non-overlapping daily origins; add sentiment/news only after point-in-time and license review. No model promotion until at least 30 completed non-overlapping vintages with calibrated intervals and robust uncertainty estimates.

Research only; not financial advice. No trading or order execution.
