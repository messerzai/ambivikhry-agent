# Living Fractal Market — Daily Research Report (2026-11-24, run 12)

## Branch and execution

- Branch: [research/living-fractal-market](https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market)
- Daily trigger commit: [11edd105](https://github.com/messerzai/ambivikhry-agent/commit/11edd10500612193e04d3c15bdbcf615b1ec0fb4)
- 5m forecast workflow: [run 45346501172 — success](https://github.com/messerzai/ambivikhry-agent/actions/runs/45346501172)
- Archive workflow: [run 45346501185 — success](https://github.com/messerzai/ambivikhry-agent/actions/runs/45346501185)
- Completed-vintage evaluator: [run 45346501166 — success](https://github.com/messerzai/ambivikhry-agent/actions/runs/45346501166)
- Archive commit: [a2631de](https://github.com/messerzai/ambivikhry-agent/commit/a2631de520e121eeb70a6e82170c388a4eae1688)
- Research documentation commits: [ledger 01d5f7b](https://github.com/messerzai/ambivikhry-agent/commit/01d5f7b196483a4c4fef4f1d9f2b5d3a5c7d281d), [competitor watchlist af6f2d4](https://github.com/messerzai/ambivikhry-agent/commit/af6f2d4c0dcf72feb57eac9f53c7ae1832e0b312), [research log 5d0a17b](https://github.com/messerzai/ambivikhry-agent/commit/5d0a17b0d950a3ca639f9af775e6284fc7dfb90d), [license register 0b1e01a](https://github.com/messerzai/ambivikhry-agent/commit/0b1e01a6d4760398933a65b3fee8d4fcdfb965dd)
- No changes were made to main.

## Research discoveries

**Facts**
- Drożdż et al. (2025), *Future Internet* 17(10), 470, [DOI 10.3390/fi17100470](https://doi.org/10.3390/fi17100470): MFCCA/MF-DFA plus q-Gaussian rescaling across BTC, ETH, DEX and NFT series. Their result attributes multifractality primarily to nonlinear temporal correlations, with heavy tails modulating spectrum width conditionally. This is not a direct forecast benchmark.
- Choi (2026), *Physica A* 697, [DOI 10.1016/j.physa.2026.131735](https://doi.org/10.1016/j.physa.2026.131735): RePEc abstract reports ~774k BTC 5m observations (Aug 2017–Dec 2024), a scaling crossover around 25 days and lower long-range dependence after the Jan 2024 ETF period. Full text was not accessible; treat as abstract-level evidence, not a reproduced result.
- Kitvanitphasu et al. (2026), *Research in International Business and Finance* 81, 103163, [DOI 10.1016/j.ribaf.2025.103163](https://doi.org/10.1016/j.ribaf.2025.103163): high-frequency VPIN/VAR analysis reports association between order-flow toxicity and future BTC price jumps, with time-zone/day-of-week effects. It is a jump-risk result, not proof of signed hourly point predictability.
- Kreuzer et al. (2026), *Review of Derivatives Research* 29, [DOI 10.1007/s11147-025-09223-6](https://doi.org/10.1007/s11147-025-09223-6): daily crypto-weighted news sentiment from 9,100+ BTC and 5,400+ ETH articles (LSEG Eikon, 2022-10-25–2024-08-30) is associated with BTC/ETH futures returns and professional net positions. The daily sample is unbalanced and the underlying news feed is licensed; it does not establish a live hourly spot edge.
- Zeri's 2026-11-20 public research note on [Kalshi BTC hourly range contracts](https://tommasozeri.github.io/research/wisdom-of-crowds-bitcoin-range/index.html) evaluates 1,340 events. Actively quoted crowd buckets had 80% interval coverage around 81–84%; the advantage over seasonal GARCH-t was small and appeared mainly five minutes before settlement. This is an hourly distribution, not a 24h point-price benchmark, and the note is not peer-reviewed.

**Hypotheses**
- Scale-aware multifractal features may improve volatility/regime diagnostics if they survive q-Gaussian surrogate checks and walk-forward ablation.
- Volume-synchronized order-flow features may improve jump-risk warnings, but current 5m taker-buy imbalance is not VPIN.
- News surprise/sentiment may add information only with a point-in-time licensed feed and publication timestamps; daily futures findings cannot be assumed to transfer to 5m spot.
- “Living/non-repeating fractal” remains a metaphor, not an established market fact.

## Competitor watchlist changes

- **BtcForecaster v2 HAR-RV-J:** public, free read-only API for Binance BTC/USDT 1h/4h/12h/24h volatility ranges. Live 90% coverage snapshot: 89.1% (1h), 86.8% (4h), 89.5% (12h), 82.3% (24h). v3 shadow 24h coverage is 75.3% on the current page and its interval score is worse than v2. Useful interval shadow comparator, not a point-price or direction rival.
- **btcforecaster-eval:** runnable .NET scoring/walk-forward/Diebold–Mariano harness; HEAD `df027d8`, MIT license. No code or sample data copied.
- **BitPredict crowd:** 11,344 settled calls as of 2026-11-23; overall crowd hit 48.9%, high-consensus calls 47.4%, fading high consensus 50.4%. Direction-only and not BTC-specific in the aggregate; behavioral shadow series only.
- **Kalshi hourly crowd:** public hourly distribution research note; no market account, trade, wager or submission.
- **GPTReviews:** public daily 24h direction leaderboard methodology, but the accessible page did not load model rows/scores; unranked discovery lead.
- Chronos-2 remains a possible zero-shot challenger; TimesFM 3.0 weights remain non-commercial despite Apache-2.0 source code. Neither was loaded.

No external competitor is ranked against LFM this run: the public systems differ in target object, issue clock, venue or scoring metric.

## Repository changes and tests

Documentation-only research changes; no model equations, dependencies or forecast code changed.

- `FORECAST_LEDGER.md`: refreshed to 18 archived vintages, 16 completed, 2 pending; added target-grid/evaluation state, hashes and data-quality checks.
- `COMPETITOR_LANDSCAPE.md`: added BtcForecaster, BitPredict, Kalshi and GPTReviews evidence and comparability notes.
- `RESEARCH_LOG.md`: added original-paper summaries, limitations and a q-Gaussian/MF-DFA experiment plan.
- `THIRD_PARTY_LICENSES.md`: audited CC BY 4.0 paper licenses, MIT evaluation harness, API terms and model-weight/code distinctions. No third-party code, weights, datasets or API payloads were reused.

Workflow tests:
- 5m forecast offline unit tests: **15 passed**.
- Evaluation logic tests: **16 passed**.
- Artifact archive tests: **18 passed**.
- General repository CI: **65 passed** on each of Python 3.10, 3.11, 3.12 and 3.13.
- Live public-data retrieval, forecast generation and artifact upload: success.
- Archival and evaluation workflows: success. Evaluator reported 16 already evaluated, one pending, zero new evaluations and zero failures.

## Current BTC 24-hour hourly output

**No validated BTC/USD hourly champion forecast exists.** The successful workflow emitted the following **BTC/USDT challenger** from Binance Spot 5m inputs. Do not relabel this as BTC/USD.

- Model: LFM-5m-Downside-Aware-Council-0.4, commit `11edd10500612193e04d3c15bdbcf615b1ec0fb4`.
- Issue UTC: 2026-11-24T07:14:55.957774Z.
- Exact cutoff UTC: 2026-11-24T07:09:59.999000Z.
- Retrieval UTC: 2026-11-24T07:14:55.953761Z.
- Source: [Binance Spot BTCUSDT 5m klines](https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=1000).
- Reference: **60,494.00 USDT**; 999 closed 5m candles; hourly targets +1 through +24 (08:00Z Nov 24 to 07:00Z Nov 25).
- Vintage: `lfm5m-2026-11-24T07:14:55.957774Z-BTCUSDT-binance-spot-council-0.4`.
- Canonical ZIP: [archived artifact](https://github.com/messerzai/ambivikhry-agent/blob/research/living-fractal-market/research/living-fractal-market/forecasts/2026-11-24/2026-11-24T07-14-55.957774Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip).
- ZIP SHA-256: `e9ff36710f5fb76eaadf2656738d283cfb88d4278411542d8cd0f854879b9467`.
- Forecast JSON SHA-256: `42135fa80fb804d42d1f5acc6b53445d2a966cdb5bf112edad99fbddd9a38909`.
- Raw input SHA-256: `573ea0fd17175b7bf71056c7ad4766d9541f278751f745050ca8a52cc2b7ae83`.
- No calibrated P50/P90 intervals: the emitted P90-style bands are Gaussian-style approximations and explicitly uncalibrated.

| Horizon | Target UTC | LFM5mEnsemble point (USDT) |
|---:|---|---:|
| +1 | 2026-11-24 08:00 | 60,498.73 |
| +2 | 2026-11-24 09:00 | 60,502.87 |
| +3 | 2026-11-24 10:00 | 60,506.52 |
| +4 | 2026-11-24 11:00 | 60,509.79 |
| +5 | 2026-11-24 12:00 | 60,512.73 |
| +6 | 2026-11-24 13:00 | 60,515.41 |
| +7 | 2026-11-24 14:00 | 60,517.87 |
| +8 | 2026-11-24 15:00 | 60,520.16 |
| +9 | 2026-11-24 16:00 | 60,522.31 |
| +10 | 2026-11-24 17:00 | 60,524.34 |
| +11 | 2026-11-24 18:00 | 60,526.28 |
| +12 | 2026-11-24 19:00 | 60,528.14 |
| +13 | 2026-11-24 20:00 | 60,529.93 |
| +14 | 2026-11-24 21:00 | 60,531.68 |
| +15 | 2026-11-24 22:00 | 60,533.38 |
| +16 | 2026-11-24 23:00 | 60,535.05 |
| +17 | 2026-11-25 00:00 | 60,536.70 |
| +18 | 2026-11-25 01:00 | 60,538.32 |
| +19 | 2026-11-25 02:00 | 60,539.93 |
| +20 | 2026-11-25 03:00 | 60,541.53 |
| +21 | 2026-11-25 04:00 | 60,543.11 |
| +22 | 2026-11-25 05:00 | 60,544.69 |
| +23 | 2026-11-25 06:00 | 60,546.27 |
| +24 | 2026-11-25 07:00 | 60,547.84 |

## Previous forecast evaluation and leaderboard

- Previous issue (2026-11-23T08:22:27.885252Z) remains pending until its final target candle closes at **2026-11-24T08:59:59.999Z**. The new Nov 24 vintage remains pending until **2026-11-25T07:59:59.999Z**. No target closes were scored early.
- Last completed vintage (Nov 22 07:43Z): MeanReversion5m nMAE 4.753271 vs random walk 4.925249 and volatility-capped slow drift 8.050249; P90 empirical coverage 0.6667 and uncalibrated.
- Internal aggregate: 10 non-overlapping completed vintages; 16 unique completed records; six overlaps excluded. Mean nMAE: random walk 3.396679, LFM5mEnsemble 3.526820, MeanReversion5m 3.388607, TakerFlow5m 3.398854, VolatilityCappedSlowDrift 4.201362. MeanReversion's paired 95% interval vs random walk crosses zero; ensemble is worse than random walk.
- External comparable standings: none.
- Virtual research points: **0**. No calibrated intervals; no champion promotion; 10/30 non-overlapping vintages.

## Data-quality warnings and next experiment

- Raw input had 1,000 rows: 999 closed and one still-forming row excluded. Closed timestamps were contiguous at 5m cadence; OHLCV values passed basic validation; reference matched the final closed candle.
- The 999-candle history spans only about 83h15m, too short for a 25-day crossover or 90-day multifractal estimation. The current 5m taker-buy imbalance is not VPIN.
- The 70,000 USDT threshold diagnostic is already below the 60,494 USDT reference. The uncalibrated heuristic probability of terminal price below that level is 1.0 because the reference is already below it; this is not a crossing probability.
- Next experiment: collect and hash a paginated 90-day Binance Spot BTCUSDT 5m history; evaluate rolling MF-DFA/MFCCA and q-Gaussian surrogate robustness at 1d/7d/25d/90d scales; test incremental volatility forecast value against HAR/RV and simple baselines before any point-price integration.
- Research only. No trading, order execution, exchange credentials, financial account or wager.


## Supplementary macro-news and behavioral-finance review

The final source pass added several useful distinctions:

- [Huynh (2026)](https://doi.org/10.1016/j.jbef.2026.101183) studies 5m reactions of the top 100 crypto assets (2014–2021) around 32 U.S. macro releases, with daily TRMI sentiment. It reports that bullish sentiment moderates the response to surprises (about −16% for returns and −24% for turnover per standard deviation). The old sample and daily sentiment mean this is not a live BTC hourly forecast.
- [Akbar (2026)](https://doi.org/10.1108/SEF-12-2025-0942) analyzes 16m+ BTC-related tweets with human-like/automation-like account labels. The publisher abstract reports no return-predictive value from polarity/hype/anxiety; attention improves GARCH-X variance modelling but reacts to price shocks. Reuse is licensed rights only.
- [Han, Liu & Sui (Dallas Fed WP 2605)](https://doi.org/10.24149/wp2605) use 666,006 Bitcointalk posts (2012–2022), 44,356 users and 2,550 wallet-linked traders. Peer sentiment changes beliefs/trading direction but does not predict future BTC prices; contagion intensity predicts volatility, volume and crashes. This is a preliminary working paper, not a peer-reviewed forecast model.
- [Kroner, Mohammed & Vega (Federal Reserve Board draft, 2026-03-20)](https://users.nber.org/~confer/conf_papers/2387/f238700/f238700.pdf) use CoinDesk minute data across 158 exchanges/18,403 pairs and focus on BTC/ETH spot around FOMC, CPI and NFP. Both headline and non-headline surprises matter; non-headline surprises often have stronger effects. Volatility, volume and spreads remain elevated for up to 30 minutes. The CoinDesk/Bloomberg/LSEG inputs are licensed and the paper is a working draft.
- [Vu & Nguyen (2026)](https://doi.org/10.1108/RBF-06-2025-0254) find weak herding in extreme states and greater dispersion under high volatility in BTC plus 25 altcoins; sentiment proxies are associated with divergence, not a simple crowd-following rule.
- [Savrul (2026)](https://doi.org/10.26650/JEPR1945391) reports weak systematic FOMC return effects in daily data, with VIX more consistent than realized rate changes; its surprise series contains only two non-zero observations and its article is CC BY-NC.
- [Mukherjee et al. (2026)](https://arxiv.org/abs/2609.23250) propose a sentiment-augmented POMP model for daily BTC volatility, not hourly point prices; it remains a preprint without a verified reusable implementation.

**Interpretation:** treat surprise magnitude, non-headline information, sentiment state, attention intensity and social contagion as separate candidate channels. Their effects differ between returns and volatility. None is added to the 5m pipeline because the required TRMI/Eikon/CoinDesk/social data are not present with point-in-time provenance and cleared terms.
