# Living Fractal Market — Daily Research Report (2026-11-22, run 11)

## Branch and execution

- Branch: [research/living-fractal-market](https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market)
- Daily marker commit: [b4d8a4a4](https://github.com/messerzai/ambivikhry-agent/commit/b4d8a4a4a4b8dd81cb771abf33f3f74bf0fe6506)
- 5m forecast workflow: [run 44999519228 — success](https://github.com/messerzai/ambivikhry-agent/actions/runs/44999519228)
- Immutable archive workflow: [run 44999519250 — success](https://github.com/messerzai/ambivikhry-agent/actions/runs/44999519250)
- Completed-vintage evaluator: [run 44999519286 — success](https://github.com/messerzai/ambivikhry-agent/actions/runs/44999519286)
- Cross-version tests: [run 44999519340 — success](https://github.com/messerzai/ambivikhry-agent/actions/runs/44999519340)
- Workflow review: .github/workflows/lfm-5m.yml is push-only on the research branch and only triggers for forecast code, its tests, the daily marker or the workflow itself. Archive/evaluation workflows are branch-scoped. No main-branch change or merge occurred.

## Research discoveries — facts

1. **Forecast-supervised realized volatility:** Chan & Chan, arXiv:2611.07287 (2026-11-05; record identifies ICAIF ’26), compare neural mean-one aggregation weights with matching classical realized measures on six Binance spot price indices. They report 54 paired QLIKE wins, with mean gains of 7.23%/8.15%/9.22% under SF/HAR/MIDAS. The target is next-day realized variance, not a signed BTC hourly price path. No public code/weights were found; proceedings DOI not independently verified. [Paper](https://arxiv.org/abs/2611.07287)
2. **RQA regime diagnostics:** Vanheusden et al., Financial Innovation 12, 127 (2026-06-03), analyze 100 crypto daily close series and 80-day windows. Their 5–50 day volatility exercise reports AUROC 0.605 at 42 days for a determinism/laminarity ratio. Threshold and embedding choices matter; data are available on request; this is not hourly price forecasting. [Paper](https://doi.org/10.1186/s40854-026-00940-x)
3. **Trade-count anomalies:** Zwydak et al., Entropy 28(7), 804 (2026-07-15), analyze 1-minute BTC/ETH/XRP trade aggregates on four venues. They find a Bitget transaction-count regime shift without proportional volume/return changes, but explicitly do not prove wash trading. [Paper](https://doi.org/10.3390/e28070804)
4. **Cross-venue order flow:** Anastasopoulos et al., Journal of Financial Markets 79 (2026-06), 101047, report out-of-sample daily cross-sectional return information from world order flow across 84 cryptocurrencies and 11 fiat currencies. This is not equivalent to Binance taker-buy volume and not a BTC hourly price-level test. [Paper](https://doi.org/10.1016/j.finmar.2026.101047)
5. **Microstructure periodicity:** Shynkevich (2026) reports subsecond periodicity in BTC/ETH spot and perpetual futures, associated with higher volatility and transaction costs but no significant adverse price impact. Data are available on request; this is a confounder/market-quality reference, not a price predictor. [Paper](https://doi.org/10.1002/fut.70089)
6. **Collective criticality:** Zouari et al. (2026-10) report BTC near a critical boundary in daily/hourly volatility analysis, with block-bootstrap uncertainty crossing CR=1 and scale/estimator sensitivity. Only the abstract-level record was accessible; no fixed threshold or price forecast is established. [Paper](https://doi.org/10.1016/j.chaos.2026.118809)

The “living/non-repeating fractal” remains a metaphor. The testable proposition is that scaling, recurrence and activity relationships may vary by regime, venue and time scale; this does not establish a unique fractal law or predictive edge. No new point-in-time sentiment/news source was validated and no sentiment/news feature was added.

## Competitor watchlist changes

- Added NRM as a **daily realized-volatility challenger hypothesis**, RQA and Zouari as **regime/risk diagnostics**, Zwydak and its third-party notebook as a **market-quality diagnostic**, Anastasopoulos et al. as a **cross-venue order-flow research candidate**, and Shynkevich as a **microstructure-periodicity reference**.
- Audited the notebook implementation at exact HEAD 8bcfe78d9a06ec16792b7f68e334688ee5a8e306. It is a third-party Jupyter notebook with MIT code license, pinned CPython 3.11 dependencies, and no root-level automated test suite. It is not an official author repository and supplies no comparable live price forecast.
- No public human/algorithmic forecaster supplied a comparable timestamped BTC/USD 24-hour hourly point path. External leaderboard remains empty. BtcForecaster remains a range-coverage shadow comparator only.

## Repository changes and licenses

- Forecast archive/ledger commit: [5679c310](https://github.com/messerzai/ambivikhry-agent/commit/5679c31012f247c16dc03a2d3ad0d146e6c102a7) — archived the exact workflow ZIP, extracted JSON, raw 5m kline response and ledger metadata.
- [Competitor landscape](https://github.com/messerzai/ambivikhry-agent/commit/de7f74b9d720c9aa0cb1de0565802a28feb4bc53) — added research/diagnostic candidates and comparability caveats.
- [Research log](https://github.com/messerzai/ambivikhry-agent/commit/45a03976ea72e8db87fbbeaaaee4f50546920455) — recorded methods, sample periods, findings and limitations.
- [Third-party license register](https://github.com/messerzai/ambivikhry-agent/commit/43d07d965de6bc5f675e55c79aca31510467b9b7) — recorded exact MIT notebook revision, article license status, data terms and reuse decisions.
- No forecast model code or feature equation changed. No external code, weights, datasets, API payloads or figures were copied. The RQA article is CC BY-NC-ND 4.0; the Zwydak third-party notebook is separately MIT; the NRM preprint had no code/weight license identified; exact reuse terms for several publisher articles remain unresolved. No legal conclusion is implied.

## Test results

- Forecast workflow offline unit tests: **15 passed**.
- Artifact archiver tests: **18 passed**.
- Evaluation tests: **14 passed**.
- General CI: **63 passed on each of Python 3.10, 3.11, 3.12 and 3.13**.
- Forecast, archive, evaluation and general CI workflows all completed successfully. The evaluator correctly left not-yet-closed target windows pending.

## BTC 24-hour hourly forecast — experimental BTC/USDT challenger only

**No validated BTC/USD hourly champion exists.** The live run below is the existing 5m council challenger, not a BTC/USD champion and not a promotion.

- Issue UTC: **2026-11-22T07:43:35.562876Z**
- Exact data cutoff UTC: **2026-11-22T07:39:59.999000Z**
- Source: Binance Spot BTCUSDT public 5m klines — https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000
- Asset / venue / quote: **BTC/USDT / Binance Spot / USDT**
- Reference price: **59,039.25 USDT**
- Input: 999 closed 5m candles; the 1 open candle in the 1,000-row raw response was excluded.
- Model: **LFM-5m-Downside-Aware-Council-0.4**, path shown: **LFM5mEnsemble**
- Source commit: [b4d8a4a4](https://github.com/messerzai/ambivikhry-agent/commit/b4d8a4a4a4b8dd81cb771abf33f3f74bf0fe6506)
- Workflow artifact ID: **14745122818**; archive: [forecast ledger entry](https://github.com/messerzai/ambivikhry-agent/blob/research/living-fractal-market/research/living-fractal-market/FORECAST_LEDGER.md)
- ZIP SHA-256: 57db9e305ff4aa1d76d901de0a6032bdc605092a0e9336bcdbc79d3015f341b1
- Forecast JSON SHA-256: e31b65fdd9f70d08d71652103d2876f8313591ba333d26bdc082ffa2771b7861
- Raw response SHA-256: e7980c74b42caf9a98c9df45021ceaea9a23d4534795c66e7e230656abe4f646

| Horizon | Target UTC | LFM5mEnsemble point (USDT) |
|---:|---|---:|
| +1 | 2026-11-22 08:00 | 58,992.83 |
| +2 | 2026-11-22 09:00 | 58,953.89 |
| +3 | 2026-11-22 10:00 | 58,921.28 |
| +4 | 2026-11-22 11:00 | 58,894.03 |
| +5 | 2026-11-22 12:00 | 58,871.33 |
| +6 | 2026-11-22 13:00 | 58,852.47 |
| +7 | 2026-11-22 14:00 | 58,836.87 |
| +8 | 2026-11-22 15:00 | 58,824.05 |
| +9 | 2026-11-22 16:00 | 58,813.57 |
| +10 | 2026-11-22 17:00 | 58,805.07 |
| +11 | 2026-11-22 18:00 | 58,798.27 |
| +12 | 2026-11-22 19:00 | 58,792.90 |
| +13 | 2026-11-22 20:00 | 58,788.75 |
| +14 | 2026-11-22 21:00 | 58,785.64 |
| +15 | 2026-11-22 22:00 | 58,783.40 |
| +16 | 2026-11-22 23:00 | 58,781.91 |
| +17 | 2026-11-23 00:00 | 58,781.05 |
| +18 | 2026-11-23 01:00 | 58,780.74 |
| +19 | 2026-11-23 02:00 | 58,780.88 |
| +20 | 2026-11-23 03:00 | 58,781.41 |
| +21 | 2026-11-23 04:00 | 58,782.28 |
| +22 | 2026-11-23 05:00 | 58,783.42 |
| +23 | 2026-11-23 06:00 | 58,784.81 |
| +24 | 2026-11-23 07:00 | 58,786.40 |

No calibrated P50/P90 intervals are available. The artifact's P90-style ranges are explicitly Gaussian approximations and are **not calibrated**, so they are not presented as prediction intervals. The separate below-level heuristic is uncalibrated and not a first-passage probability.

## Previous forecast evaluation and internal leaderboard

- Twelve unique historical vintages have completed evaluation. Four additional vintages are pending after this 07:43 issue; the 2026-11-21 vintage is still pending until its final target candle closes at **2026-11-22 07:59:59.999Z**. The new 07:15, 07:32 and 07:43 vintages are pending until 2026-11-23.
- The last completed vintage (issued 2026-11-20T07:57:36Z) had DownsideStress5m nMAE **4.905807**, RandomWalk **6.022312**, VolatilityCappedSlowDrift **5.505549**. Its P90 coverage was not calibrated; **0 points**.
- The protocol excludes overlapping 24h target grids from aggregate scoring. A timestamp-only chronological selection (sort by target start, then issue time; keep a vintage only if its first target is after the preceding selected vintage's final target) yields **8 non-overlapping completed vintages** from the 12 unique completed records.
- Mean nMAE on those 8 non-overlapping vintages (lower is better): RandomWalk **3.3329**; TakerFlow5m **3.3356**; MeanReversion5m **3.3456**; LFM5mEnsemble **3.4799**; VolatilityRegime5m **3.5610**; Momentum5m **3.6665**; DownsideStress5m **3.8796**. VolatilityCappedSlowDrift mean nMAE is **4.0143**.
- Paired 95% percentile-bootstrap intervals over the 8 vintage-level loss differences vs RandomWalk are exploratory and small-sample: LFM5mEnsemble +0.1470 [0.0186, 0.2841]; TakerFlow5m +0.0027 [-0.0140, 0.0254]; MeanReversion5m +0.0127 [-0.0536, 0.0903]. Positive means worse than RandomWalk. These intervals are not a basis for promotion.
- **Virtual points: 0.** Every forecast's intervals remain uncalibrated, so none is eligible even when a point loss beats a baseline. Promotion gate remains at least 30 completed non-overlapping daily vintages; only 8 currently qualify for aggregate scoring.
- External leaderboard: **no comparable independently verifiable submission**; no rank assigned.

## Data-quality warnings and next experiment

- Verified the raw response SHA-256 and byte count against forecast metadata; 1,000 raw rows contained 999 closed candles and one open candle, which was excluded. Closed candles were contiguous at 5m cadence, OHLC values passed basic validity checks, the last closed close matched the 59,039.25 reference price, all seven model paths had the same 24-point UTC grid, and all point prices were finite and positive. Retrieval was 215.6 seconds after the exact data cutoff.
- History length is only about 3.5 days, too short for the cited 7-day trade-count diagnostics or 80-day RQA windows and inadequate for stable multifractal estimation.
- Next experiment: build and hash a paginated 90-day Binance Spot BTCUSDT 5m history; test trade-count/quote-volume change diagnostics with robust rolling baselines and surrogate checks; then compare realized-volatility features against HAR/RV baselines. Keep this as a diagnostic/volatility challenger and run ablations before any point-price integration.
- Research only; no trading, order execution, exchange credentials or financial advice.
