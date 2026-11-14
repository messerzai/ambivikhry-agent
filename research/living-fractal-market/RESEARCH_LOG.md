# Research log — 2026-11-11

Branch: research/living-fractal-market  
Starting HEAD: 6e64ff793c9c4889ab40d0def0fdf117f44eeab9  
Scope: research branch only; main was not modified.

## Research discoveries

### 1. Non-stationary multifractality is a testable state variable, not a permanent market law

Cho et al., “Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity,” Frontiers in Physics (Perspective, published 2026-10-29), DOI 10.3389/fphy.2026.2026031. The article argues that scaling exponents and complexity measures depend on regime, venue and sampling conventions. It explicitly recommends matched surrogate tests, finite-size confidence bands, rolling windows, multiple clocks, and prospective crash-warning evaluation. It warns that finite samples, heavy tails, scaling crossovers and estimator bias can produce spurious multifractality. This directly supports treating the fractal layer as a measured hypothesis and using IAAFT, shuffled and phase-randomized nulls—not as a narrative assumption.

Source: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.2026031/full

Drożdż et al., “Multifractality and Its Sources in the Digital Currency Market,” Future Internet 17(10), 470 (2025), DOI 10.3390/fi17100470. The paper applies MFCCA/MF-DFA to 1-minute Binance BTC/USDT and ETH/USDT data from 2018-01-01 through 2024-12-31 (3,682,080 observations). Its source-decomposition procedure finds temporal correlations to be the primary source of multifractality; heavy tails broaden the spectrum conditionally when correlations are present, rather than acting as an independent additive source. This is descriptive/diagnostic evidence, not evidence that multifractal features improve BTC forecasts.

Source: https://www.mdpi.com/1999-5903/17/10/470

Choi, “Intrinsic multifractality and adaptive efficiency in Bitcoin: Disentangling sources of scaling complexity across market regimes,” Physica A 697 (2026), 131735, DOI 10.1016/j.physa.2026.131735. The abstract-level record reports approximately 774,000 five-minute BTC observations (Aug-2017 to Dec-2024), q-Gaussian rescaling, and a scaling crossover near 25 days separating a near-efficient short-time regime from a long-time anti-persistent regime, with singularity-spectrum width described as largely invariant across the crossover. It also reports a greater-than-half decline in its Market Deficiency Measure after the January 2024 spot ETF approval and a negative volatility/complexity coupling. The publisher full text was not accessible in this review, so treat these as abstract-level claims requiring replication, not independently reanalysed evidence.

Sources: https://ideas.repec.org/a/eee/phsmap/v697y2026ics0378437126004711.html ; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.2026031/full

### 2. News surprise and sentiment should be modelled as an interaction, not a generic sentiment score

Huynh, “Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets,” Journal of Behavioral and Experimental Finance 50 (June 2026), 101183, DOI 10.1016/j.jbef.2026.101183. Using 5-minute data for the top 100 cryptocurrencies over 2014–2021 and daily TRMI sentiment, the paper reports immediate return/turnover responses to US macro announcements and a moderating effect of sentiment: a one-standard-deviation increase in sentiment reduces the response to macro surprises by about 16% for returns and 24% for turnover. The effect is stronger in low-sentiment states and is tested with alternative event windows and international announcements. Limitations for our use: top-100 universe and historical sample end in 2021; daily proprietary sentiment is not a free point-in-time BTC signal; event-study association is not a demonstrated hourly forecasting edge.

Source: https://doi.org/10.1016/j.jbef.2026.101183

Chen & Hu, “Sentiment spillovers from news and social media in cryptocurrency markets,” Journal of International Financial Markets, Institutions and Money 110 (2026), 102357, DOI 10.1016/j.intfin.2026.102357. The abstract reports stronger, more synchronized news-media sentiment spillovers than social-media spillovers across ten major coins; Bitcoin is a dominant transmitter, and connectedness strengthens in pessimistic and euphoric states. The study uses Diebold–Yilmaz connectedness and QVAR tail-state analysis. Full text was not available in the checked source, and this is connectedness evidence rather than a point-forecast result.

Source: https://ideas.repec.org/a/eee/intfin/v110y2026ics1042443126000739.html

Han, Liu & Sui, “Social Network and Sentiment Contagion: Evidence from the Bitcoin Market,” Dallas Fed Working Paper 2605 (2026-03-02), DOI 10.24149/wp2605. This working paper reports that peer sentiment shifts investor beliefs but does not predict future Bitcoin prices; a measure of contagion intensity does forecast volatility, volume and crashes. It is not a peer-reviewed journal article and relies on social-network/individual-trading data that may not be reproducible from our public feed. It is an important negative-control lead: sentiment can explain activity/risk without forecasting signed returns.

Source: https://www.dallasfed.org/research/papers/2026/wp2605

### 3. Microstructure and time irreversibility are promising, but the data/target must match

Bieganowski & Ślepaczuk, “Explainable Patterns in Cryptocurrency Microstructure,” arXiv:2602.00776 (2026-01-31 preprint). The abstract describes 1-second Binance Futures order-book/trade data for BTC, LTC, ETC, ENJ and ROSE (2022-01-01 to 2025-10-12), CatBoost, order-flow/spread features and time-series cross-validation. It reports stable feature importance across assets and backtests, but the paper is a preprint and does not establish a public, independently verifiable live BTC/USD 1h ledger. The futures/L2 data are not equivalent to our spot-kline taker-buy-volume proxy.

Source: https://arxiv.org/abs/2602.00776

Choi, “Testing detailed balance in daily cryptocurrency markets: irreversibility in range–volume dynamics, and none detectable in candlestick shape,” Frontiers in Physics (2026). In 22 USDT pairs from one venue, the abstract reports no detected first-order detailed-balance violation in candlestick shape, but range–volume dynamics reject detailed balance in 12 of 17 held-out assets under the stated design. This is a useful counterexample to blanket “non-repeating” claims: irreversibility depends on the state representation, sample size and test. The authors report 44 non-rejections for normalized candlestick shape, versus rejection in 12 of 17 held-out assets for range-volume states. Crucially, their methods section says block-permutation surrogates are invalid for this transition-count statistic and IAAFT is structurally invalid for the shape encoding because it breaks exact within-bar constraints. Thus IAAFT is not a universal null; null construction must respect each feature representation. Daily bars and one venue limit direct application to 5-minute forecasts.

Source: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.1977979/full

## Competitor and public-forecast findings

- Chronos-2: official HF model card lists Apache-2.0 and describes a 120M zero-shot model with univariate, multivariate, covariate-aware and quantile forecasts. The card's general FEV-Bench/GIFT-Eval claims are not BTC-specific evidence.
- TimesFM 2.5: official HF card lists Apache-2.0 for the 200M checkpoint.
- TimesFM 3.0: official HF card lists a distinct timesfm-non-commercial-license-v1.0 for weights, while the source repository is Apache-2.0. Do not treat the source license as a weight license.
- NeuralForecast provides N-BEATS, N-HiTS, TFT and PatchTST implementations under Apache-2.0 code terms; no pretrained crypto checkpoint is implied.
- Benchstreet is MIT, but its own README says it is not an objective benchmark and describes S&P 500 daily data, not BTC hourly data.
- CryptoOracle is the closest public +24h hourly forecast ledger located. Its published 2026-09-17 exploratory snapshot reports TimesFM 2.5 BTC +24h mean absolute log-return error ×100 of 1.712 versus 1.627 for last price, with 77.3% coverage for a nominal 80% interval. This is a historical backtest, not a current live score; overlapping hourly forecasts are not independent.
- BitPredict offers free manual timestamped human UP/DOWN 24h receipts, not point-price forecasts. Its public app rendered a loading state without a populated leaderboard sample; bot/API access is an Elite plan listed at $29/month, so no automated submission was made under the no-payment rule. AI Predicts Bitcoin publishes daily 7d/30d/90d/180d/360d model-panel predictions, not hourly. Its 2026-11-07 short-term page is four days stale despite claiming daily 06:00 UTC updates, and simultaneously says 200 predictions are graded while showing an accuracy-unlock date of 2026-04-08. No accuracy score is accepted. Neither was entered or ranked.
- Sources: https://www.bitpredict.io/ ; https://app.bitpredict.io/ ; https://www.aipredictsbitcoin.com/short-term
- Synth sources: https://docs.crunchdao.com/real-time-competitions/competitions/synth ; https://docs.crunchdao.com/crunch-hub/register ; https://synthdataco.github.io/synth-subnet/ ; https://colab.research.google.com/github/crunchdao/crunch-synth/blob/master/crunch_synth/examples/lightgbmtracker.ipynb
- CrunchDAO Synth requires full return-density forecasts, not point prices: current documented 1h rounds run every 8 minutes at 1m/5m/15m/30m/1h steps; 24h rounds run every 39 minutes at 5m/1h/6h/24h steps. It uses a 7-day rolling CRPS leaderboard and a volatility-CRPS term for 1h based on 1,000 simulated price paths. The docs identify a benchmarktracker replay of a real Synth miner (ranked #1 on 1h and #20 on 24h in the documented comparison), but this is a reference row, not a new live submission or BTC-only score. Rewards were paused and Synth miners deregistered in October 2026; the previous $30,000 USDC phase is marked completed. Joining still requires a platform account and acceptance of participation rules. No account was created and no submission was made under the no-external-account/no-token rule. The current model's point/P90 output is not comparable to Synth's density submissions.

## Data and code audit

- Research branch HEAD at start of run: 6e64ff793c9c4889ab40d0def0fdf117f44eeab9.
- The 5-minute prototype already reads public Binance Spot BTCUSDT klines without an API key and emits seven models, including DownsideStress5m. QUICKSTART incorrectly documented six and omitted DownsideStress5m.
- The 5-minute parser checked continuity between received rows and allowed a 15-minute age. It could accept a missing most-recent closed candle because the test fixture itself omitted the immediately preceding closed bar. A stricter latest-expected-candle check and a regression test are added in this run.
- The workflow file contained schedule and workflow_dispatch, but GitHub requires those triggers' workflow file to exist on the default branch. Because this branch must remain isolated and main must not change, those triggers are removed; the branch workflow remains push-triggered. The daily research automation is separate.
- Binance's official REST documentation confirms that public market-data-only requests should use data-api.binance.vision and that kline timestamps are milliseconds: https://developers.binance.com/en/docs/products/spot/rest-api. The prototype endpoint is public and requires no API key. Public search snippets returned 5-minute candles stamped 2026-11-11 13:10, later than the run's 07:04 UTC clock, but the source timezone and timestamp semantics were not established. Because the timestamps could not be reconciled to UTC, those rows were rejected rather than treated as live. A Coinbase public candle endpoint returned a raw JSON page that the browser could not expose as rows. No 300+ bar, timestamp-consistent live series was available for a valid forecast.
- No valid 24-hour forecast was issued, no forecast vintage was appended, and no previous vintage could be evaluated. No durable append-only forecast ledger currently exists; its schema/policy is documented separately.
- No third-party code, model weights or datasets were copied.

## Hypotheses, not findings

1. Rolling multifractal width and nonlinear dependence may vary with market regime, but add no forecast feature until they survive IAAFT/finite-size nulls.
2. News surprise × lagged sentiment may improve conditional volatility or activity forecasts; signed-return benefit is unknown.
3. Spot taker-buy imbalance may be a weak proxy for short-term flow, but it is not a substitute for L2 order-book imbalance.
4. Time irreversibility may be more visible in range-volume than signed candlestick shape; test both with matched nulls and rolling out-of-sample evaluation.

## Next experiment

Complete the 5m latest-bar quality-gate regression test; then obtain a synchronized, closed Binance Spot series and compare the seven 5m challengers on identical rolling origins. In parallel, build a full-density/quantile challenger for CRPS and a Chronos-2 baseline only after pinning its HF revision. Keep multifractal, sentiment and news features as separate ablations.


## Implementation and test results

- The 5-minute prototype quality gate was tightened to require the latest expected fully closed 5-minute candle, not merely a recent last timestamp.
- The synthetic fixture now ends at the correct latest closed candle; a new regression test removes that final candle and requires abstention.
- Offline unit suite executed locally from the exact branch source: 5 tests passed, 0 failed. Coverage includes forecast shape (7 models × 24 horizons), open-candle exclusion, OHLC rejection, internal gaps, trailing missing candle and stale data.
- GitHub combined status for the latest repository commit returned no status entries at review time; therefore no GitHub Actions success is claimed. The push-triggered workflow is configured, but its run result was not available through the current connector.
- The branch remains isolated and is 30 commits ahead of main; no main changes or merges were made.


## Daily literature scan — 2026-11-11

### 4. Rolling multifractal evidence across fiat venues — peer-reviewed

Kim, Lee & Choi, “Comparative Analysis of Cryptocurrency Market Efficiency and Local Features Using MF-DFA and DCC-GARCH,” *Fractal and Fractional* 10(6), 353, published 23 May 2026, DOI: 10.3390/fractalfract10060353.

- **Data/method:** daily closes and returns from 1 Jan 2018 to 30 Sep 2025; 11 BTC/ETH/XRP/BCH fiat pairs across Upbit (KRW), Bitfinex/Coinbase (USD) and Bitbank (JPY); rolling MF-DFA and DCC-GARCH. The paper uses 99 phase-randomized surrogates and rolling windows of 200/250/300 observations.
- **Reported result:** generalized Hurst curves and singularity spectra are multifractal in the sample; the original spectrum widths exceed the phase-randomized surrogate means, with reported z-scores 6.72–10.91 and rank-based one-tailed p=0.010 (the minimum attainable resolution with 99 surrogates). The paper also reports time-varying cross-market correlations.
- **Limitations:** daily rather than intraday data; only 11 pairs and one selected venue per currency market; ETH/JPY excluded; results depend on q-range, window length and DCC-GARCH specification; source data are available from the corresponding author on reasonable request. The paper does not test incremental BTC hourly forecast skill. Its surrogate result is diagnostic evidence about this sample, not a universal proof of intrinsic or “living” fractality.
- **Research implication:** useful support for a rolling MF-DFA diagnostic and sensitivity grid, but not a reason to add spectrum width to the live forecast before a leakage-safe ablation. Compare phase-randomized results with IAAFT and finite-size nulls in our own data rather than treating one surrogate family as definitive.

Source: https://www.mdpi.com/2504-3110/10/6/353

### 5. Intraday seasonality is a necessary control for five-minute flow signals — peer-reviewed

Hansen, Kim & Kimbrough, “Periodicity in Cryptocurrency Volatility and Liquidity,” *Journal of Financial Econometrics* 22(1), 224–251 (2024), DOI: 10.1093/jjfinec/nbac034.

- **Data/method:** high-frequency BTC and ETH data from Binance and Coinbase Pro (centralized exchanges) and Uniswap V2 (DEX); analysis of volatility and volume patterns by weekday, hour and within-hour interval.
- **Reported result:** systematic periodicity in volatility and volume across all three time scales; the authors report that patterns strengthened over time and that price formation mainly occurred on CEXs while DEX price adjustment could be slower.
- **Limitations:** the public abstract does not provide enough detail to reconstruct the complete estimator or current regime; the work documents periodicity, not a ready-made BTC direction forecast. Its sample/venue effects should not be assumed stationary.
- **Research implication:** any five-minute TakerFlow or volume-pressure challenger should be tested against time-of-week and intrahour seasonal baselines. A raw taker-buy imbalance can otherwise proxy recurring activity schedules rather than new directional information.

Source: https://doi.org/10.1093/jjfinec/nbac034

### 6. Jump clustering matters for tail calibration — peer-reviewed

Saef, Nagy, Sizov & Härdle, “Understanding temporal dynamics of jumps in cryptocurrency markets: evidence from tick-by-tick data,” *Digital Finance* 6(4), 605–638 (2024), DOI: 10.1007/s42521-024-00116-1.

- **Data/method:** tick-by-tick observations for six major cryptocurrencies quoted against Tether across seven exchanges over nearly 2.5 years; high-frequency econometric jump detection and temporal clustering analysis.
- **Reported result:** jumps occur on up to 58% of trading days in the sample; negative jumps dominate in frequency and size; jump occurrence clusters and displays intraday/time-of-week patterns, especially for BTC and ETH.
- **Limitations:** the repository abstract does not expose all implementation details; the reported percentage is “up to” across the sample, not a BTC-only unconditional probability; the paper itself calls for better co-jump methods. Jump clustering does not establish that the next jump is forecastable.
- **Research implication:** the current Gaussian-style P90 bands are not adequate tail claims. Keep them explicitly uncalibrated; next probabilistic challenger should compare Gaussian, Student-t and simple jump-mixture residual distributions under chronological coverage and proper-score tests.

Source: https://doi.org/10.1007/s42521-024-00116-1 ; repository record: https://edoc.hu-berlin.de/items/6b0d7ba2-029a-4ea3-b783-0a8fba314835

### 7. Order-book information is not represented by candle taker-buy volume — working-paper evidence

Alexander, Heck, Kaeck & Riordan, “Order Flow Impact and Price Formation in Centralized Crypto Exchanges,” SSRN working paper (posted 19 July 2024; SSRN abstract record 4867599).

- **Abstract-level claim:** analysis of Bitcoin order types on Coinbase and Binance reports that limit-order submissions and cancellations are more frequent than market orders and have a larger total contribution to price discovery; high-frequency cross-venue integration can break down.
- **Evidence status/limitations:** SSRN working paper, not treated here as peer-reviewed; only the abstract record was accessible in this review, so detailed model specification and robustness were not independently inspected.
- **Research implication:** preserve the strict distinction in our code/docs: spot kline taker-buy base volume is a coarse trade-flow proxy, not order-book imbalance, queue dynamics or full signed order flow. Do not label it L2 or order-flow reconstruction.

Source: https://papers.ssrn.com/sol3/abstract_id=4867599

### 8. Public five-minute feed contract verified

Binance's official Spot REST documentation states that public market-data-only requests should use `https://data-api.binance.vision`; kline endpoints return chronological rows and timestamps are milliseconds by default. The documentation also notes that the API is asynchronous and a delay in data updates is normal.

- The branch's `forecast_btc_5m.py` already uses the market-data-only host first and fallback public hosts, requests up to 1,000 BTCUSDT 5m klines, excludes the forming candle, checks exact five-minute continuity and requires the latest expected closed bar.
- This run's execution environment could not resolve external DNS, and the web browser could not fetch the raw Binance JSON. Therefore no actual 300–1,000-row current candle sample was obtained, no live model was executed, and no 24-hour forecast vintage was issued.
- Do not treat the presence of a public endpoint as evidence that this run successfully retrieved it. A successful CI artifact would need to be inspected before reporting numeric predictions.

Source: https://developers.binance.com/en/docs/products/spot/rest-api

## Daily decisions and next experiment — 2026-11-11

**Implemented:** literature and provenance findings appended to this log only. No model coefficients or forecast behavior changed because there is no fresh, validated forward sample and no evidence that these new features improve out-of-sample loss.

**Next experiment:** add an hour-of-week/intrahour seasonal naive baseline and compare the seven five-minute challengers against it on identical, non-overlapping rolling origins; then test Gaussian vs Student-t vs jump-mixture residual intervals. Keep MF-DFA width, sentiment and news surprise as separate ablations. Require a point-in-time data snapshot, exact source/venue and minimum 30 completed daily vintages before any champion promotion or reward point.


## Daily literature and competitor scan — 2026-11-12

Starting branch HEAD: 19aec7b1964a23e7d55527e14e16f477e5748f43. Scope remains research/living-fractal-market only; main was not modified.

### 9. Clock-phase periodicity is a new microstructure control — arXiv preprint

Kim & Hansen, “The Quarter-Hour Effect: Periodic Algorithmic Trading and Return Predictability in Cryptocurrency Futures,” arXiv:2607.09426 (revised July 2026; preprint, not treated as peer-reviewed evidence).

- **Data/method:** trade data for six Binance perpetual contracts; a clock-phase-resolved Autocorrelation Map examines order-flow and return dependence around minute, five-minute and quarter-hour boundaries.
- **Abstract-level reported result:** volatility and volume bursts recur at 1-minute, 5-minute and 15-minute marks; trade-size roundness falls during those bursts. The authors report out-of-sample predictability in opening returns and that opening order imbalance predicts returns over 4–12 hours, with much weaker effects at finer clock-time frequencies.
- **Limitations:** the accessible record is the abstract; the study is on perpetual futures, not Binance Spot BTC/USDT; it does not establish that spot kline taker-buy volume contains the same signal or that the effect is stable in the current regime.
- **Research implication:** add UTC clock-phase controls to a future test, but keep spot and perpetual series separate. Five-minute OHLCV can test bar-phase and 15-minute phase effects only; one-minute boundary/order-book effects require timestamped trades or depth data. Do not label candle taker-buy volume as full order-flow imbalance.

Source: https://arxiv.org/abs/2607.09426 ; abstract mirror: https://econpapers.repec.org/paper/arxpapers/2607.09426.htm

### 10. Sampling frequency and finite-sample bias affect Hurst estimates — arXiv preprint

Takaishi, “Multifractality and sample size influence on Bitcoin volatility patterns,” arXiv:2511.03314 (November 2025; preprint).

- **Data/method:** Bitcoin realized-volatility series; the abstract studies the finite-sample effect of sampling interval Δ on the Hurst exponent and performs multifractal analysis.
- **Abstract-level reported result:** estimated Hurst exponent decreases as Δ increases; a finite-sample ansatz fits the relationship; extrapolated Δ→0 values are below 1/2 (described as rough volatility). The abstract reports about 1% relative error for five-minute realized volatility and weaker multifractality in realized volatility than in price returns.
- **Limitations:** preprint; the current review verified the abstract record, not a full independent replication. This is an estimator/sampling result, not a BTC forecast or proof of a unique market-generating process.
- **Research implication:** never compare H(q), Hurst or spectrum width across frequencies without recording sample length and applying finite-size/sampling sensitivity checks. Keep return-based and realized-volatility-based multifractal diagnostics separate.

Source: https://arxiv.org/abs/2511.03314 ; abstract mirror: https://econpapers.repec.org/paper/arxpapers/2511.03314.htm

### 11. Public five-minute feed check

Binance's official market-data-only documentation confirms that public Spot REST klines are available without an API key from data-api.binance.vision and that public WebSocket market-data streams are available from data-stream.binance.vision.

Source: https://github.com/binance/binance-spot-api-docs/blob/master/faqs/market_data_only.md

A public Binance Spot BTCUSDT 5m page at https://dboqo.com/en/data/kline/?interval=5m&market=spot exposed only the last 40 rows in the browser view. Its displayed timestamps had no explicit timezone in the extracted page, and the latest row appeared to be the still-forming interval. The raw official Binance JSON endpoint could not be retrieved in this execution environment. Forty rows are also below the prototype's 300-candle minimum and far below the proposed seasonality sample. These rows were not converted into UTC, not passed to the model, and not used for a forecast.

### 12. Competitor watch additions

- **webTimesFM** (https://github.com/vishalmysore/webTimesFM; code HEAD ffbdec38f5d86a84e0bd274534ac91129db5c7b5): browser-side TimesFM 2.5 and Chronos-2 comparison using ONNX/WebGPU/WASM. Its 18-Oct-2026 ten-series table reports Bitcoin 30-day MAE 6,949 for TimesFM 2.5, 7,272 for Chronos-2 and 7,153 for “no change”. The page says series point counts are hidden and explicitly calls ten series a small test, not a benchmark. Frequency, origin-level records and a matching BTC hourly target are not exposed; retain as a weak BTC-specific research lead, not a rankable competitor.
- **FelixClements/prism** (https://github.com/FelixClements/prism; HEAD 782115532b08033692e747e3b1b57d0da3e9928d): a walk-forward Bitcoin forecasting repository using daily Coinbase data, Chronos/TimesFM, wavelet and on-chain features, with a 3–14 day swing target. Its README notes that some scripts are supplied by external agent skills outside the repository, limiting standalone reproducibility. It is not an hourly comparator.
- **TensorLink-AI/ephemeris-mcp** (https://github.com/TensorLink-AI/ephemeris-mcp; HEAD 263b60b704e1cff855036a62ef1541ec45d33d57): MIT-licensed bridge exposing Chronos-2, TimesFM 2.5, Toto 2, TiRex-2 and IBM Granite-family forecasts. Its published TIME/GIFT-Eval figures are general benchmark claims, not BTC-specific evidence. Hosted inference requires an API key and is pay-per-forecast; no key, paid call or external account was used.
- **BrainEdge** (https://brainedge.tech/): public BTC/USD directional dashboard claims 659 out-of-sample days and 49.6% BTC directional accuracy, but its visible page says last updated 2026-10-23. It is stale as of this review and does not expose a complete point-price forecast ledger or our 24-step hourly loss; retain as an unranked shadow reference only.

### Daily decisions — 2026-11-12

- Added a pre-registered intraday-seasonality protocol as a research document; no forecast coefficients or production behavior changed.
- No valid live forecast was issued: no timestamp-consistent, sufficiently long Spot BTCUSDT series was retrieved. No forecast vintage was appended; no previous vintage exists to evaluate.
- No code, model weights, dataset, tokenizer or third-party implementation was copied. No external API key, account, paid inference or contest submission was used.
- No new code tests were required or run because this change is documentation-only. The last recorded offline 5m suite result remains 5 passed / 0 failed from the prior run; it is not a fresh run for this date. GitHub status checks currently return no entries, so no CI pass is claimed.
- Branch remains 47 commits ahead of main and 0 behind at the start of this run. No merge or main-branch write occurred.

**Next experiment:** acquire at least 8 weeks (preferably 90 days) of timestamp-verified 5m Binance Spot data, with a separate matched Perpetual dataset. Test hour-of-week, 15-minute phase and five-minute bar-phase controls against random-walk, volatility-aware and seasonal-naive baselines on identical non-overlapping origins. Treat fine one-minute effects as out of scope until trade-level data are available. Then run phase-feature ablations and multiplicity-aware walk-forward evaluation; do not add any feature to the forecast champion on descriptive evidence alone.


### Repository commits for the 2026-11-12 scan

- Research log and literature findings: `f823c3262b574ade3e240083ed199a90c80e948a`
- Competitor watch update: `37a832c36b2370eb72adbc9c961bff024c1714cc`
- Third-party license audit: `80b4e037c5aa83a64f04c224ec7e07c5f0196752`
- Intraday-seasonality protocol: `de2c05e58f468320794904b90c4d42a5a13aca31`
- Protocol sample-count clarification: `e5d3becb0c33452bd92a80b8dc812eefcd339372`

All commits were written only to `research/living-fractal-market`; no commit was made to `main`.


## Daily research and pipeline audit — 2026-11-13

Starting branch HEAD: 75cbc8bebc42e91033713263e338ada4c0848e95. Scope remains research/living-fractal-market only. The branch was 53 commits ahead of main and 0 behind at review time; main was not changed.

### 13. Sub-second periodicity is supported by a peer-reviewed market-microstructure study

Shynkevich, “Trading Periodicity and Algorithmic Divide in Cryptocurrency Markets,” Journal of Futures Markets 46(5), 904–930; first published 2026-02-18; DOI 10.1002/fut.70089.

- **Data/method:** sub-second trading-activity data for Bitcoin and Ethereum spot and perpetual futures on a major cryptocurrency exchange.
- **Reported result:** periodic activity is associated with agency algorithms taking liquidity in spot and proprietary algorithms taking liquidity in perpetual futures. Periodic bursts increase volatility and transaction costs, but the study reports no significant adverse price impact. A large share of price discovery occurs during proprietary-algorithm activity.
- **Limitations:** the data are sub-second and available from the author on reasonable request; this is not a directly reproducible public 5m BTC/USDT dataset and does not establish a 5m directional forecasting edge.
- **Research implication:** 5m phase features are only coarse proxies for a finer microstructure process. Activity bursts must not be interpreted as directional signals without trade/depth data and out-of-sample tests.

Source: https://onlinelibrary.wiley.com/doi/10.1002/fut.70089

### 14. Round-number clustering does not imply reliable support or resistance

Choi, “Strong clustering and weak barriers at round numbers in Bitcoin markets,” Research in International Business and Finance 90 (2026), DOI 10.1016/j.ribaf.2026.103494.

- **Data/method:** abstract reports more than seven years of Binance one-minute transaction data and tests price clustering, barrier properties and machine-learning classification around round numbers.
- **Reported result:** prices cluster at round numbers more than under random price formation, but the numbers show weak barrier properties; classifier accuracy is reported as indistinguishable from random guessing.
- **Limitations:** publisher full text was paywalled in this review; the checked evidence is the bibliographic record and abstract, not an independent replication.
- **Research implication:** 70,000 USDT remains a predeclared stress threshold only. It must not be described as support/resistance or assigned a breach probability from round-number psychology.

Source: https://doi.org/10.1016/j.ribaf.2026.103494 ; abstract record: https://EconPapers.repec.org/RePEc:eee:riibaf:v:90:y:2026:i:c:s0275531926002217

### 15. A new public retail-sentiment indicator is a feature lead, not a BTC forecast competitor

Wagner & Metzler, “When the Crowd Speaks: AI-based retail investor sentiment indicator with Reddit data,” ECB Working Paper No. 3276, 2026-08-24.

- **Data/method:** Reddit posts from major investing and crypto-related subreddits, 2015 through April 2026; ChatGPT 5.1 labels sentiment and topics; daily positive/negative aggregation is weighted by engagement and standardized using a rolling one-year z-score.
- **Reported result:** the authors report statistically significant short-term information for market prices, with the relationship particularly relevant to next-day S&P 500 returns during market declines.
- **Limitations:** the result is not a BTC-specific 5m/1h forecast. Daily aggregation is too coarse for a direct intraday signal. Post availability, platform terms, sampling bias, language coverage and model-label reproducibility require separate review.
- **Research implication:** add R-RISI as a candidate external sentiment reference for a daily BTC feature ablation only after its data and reuse terms are checked. Do not scrape or copy its data in this cycle.

Source: https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3276~3ba8565a13.en.pdf

### 16. Cross-asset tail synchronization is a risk diagnostic, not a point forecast

Zouari, Alon & Shtudiner, “Heterogeneous collective criticality in cryptocurrency volatility: Scaling collapse, tail synchronization, and cascade amplification,” Chaos, Solitons & Fractals 211 (2026), DOI 10.1016/j.chaos.2026.118809.

- **Data/method:** abstract reports hourly and daily BTC, ETH and SOL volatility, with S&P 500 and EUR/USD contrast series; coupled critical-boundary framework, circular-block intervals, circular-shift/block-shuffle/factor-residual nulls, and GARCH-family filtering.
- **Reported result:** BTC is described as boundary-adjacent, with its block interval crossing the critical value; crypto tail co-exceedances remain above the stated null envelopes; short-horizon volatility-of-volatility preserves cascade amplification.
- **Limitations:** full text was paywalled in this review; claims are abstract-level and estimator/time-scale sensitivity is explicitly reported. No forecast skill is established.
- **Research implication:** consider tail-synchronization diagnostics as a separate risk-state ablation; never convert a criticality label into a crash probability without calibrated prospective validation.

Source: https://doi.org/10.1016/j.chaos.2026.118809 ; abstract record: https://EconPapers.repec.org/RePEc:eee:chsofr:v:211:y:2026:i:p1:s0960077926009501

### 17. Forecast artifact and CI provenance recovered

GitHub Actions run 43179787161 (“LFM 5m BTC research forecast”) completed successfully on 2026-11-12 at 08:03 UTC. Both the offline 5m unit-test step and the live public-data forecast step succeeded. Artifact ID 13925638014 contained the raw JSON forecast.

- **Vintage:** issued 2026-11-12T08:03:03.240211Z; data cutoff 2026-11-12T07:59:59.999Z; Binance Spot BTCUSDT 5m; 999 closed candles; reference 73,660.61 USDT; model version LFM-5m-Downside-Aware-Council-0.3; source https://data-api.binance.vision/api/v3/klines; model source commit 75cbc8bebc42e91033713263e338ada4c0848e95.
- **Models:** RandomWalk, Momentum5m, MeanReversion5m, VolatilityRegime5m, TakerFlow5m, DownsideStress5m and LFM5mEnsemble; each produced 24 hourly target points. The P90 bands are explicitly uncalibrated.
- **Archival:** the original JSON is preserved losslessly as a gzip-compressed append-only file under forecasts/2026-11-12/. The compressed and uncompressed SHA-256 hashes are recorded in FORECAST_LEDGER.md.
- **Evaluation:** the final target hour opens at 2026-11-13T08:00:00Z and closes at 08:59:59.999Z. At the 2026-11-13 07:56:59Z review cutoff, the final target had not closed; the full 24-point vintage is therefore not yet scored. No partial score is substituted for the frozen 24-hour primary evaluation.

A separate repository-wide tests workflow, run 43179787283, failed before pytest: pip install -e . stopped because setuptools auto-discovered multiple flat-layout top-level packages (chess, research, ambivikhry). Python 3.11/3.12/3.13 jobs failed at packaging; Python 3.10 was cancelled; pytest did not run. This is a repository packaging/CI issue, not a failure of the 5m forecast test step. Root packaging was left untouched to preserve the research-branch scope.

### 18. Data-quality hardening

The 5m parser now additionally requires UTC-aligned candle opens, the exact inclusive Binance close timestamp (open + 299,999 ms), non-negative trade counts and taker-buy quote volume no greater than total quote volume. New unit tests cover these checks and require all model paths to share the same 24-point UTC hourly target grid beginning at the next full hour.

The workflow trigger was narrowed to model code, its tests, the daily trigger marker and the workflow itself. Forecast archives and ledger-only commits do not recursively launch another run. The daily marker is intended to trigger one fresh public-data run during each scheduled research cycle.

### Daily decisions — 2026-11-13

- No external code, weights, tokenizers or datasets were copied. Paper results were used as cited research leads only; no new license obligations were introduced.
- No external competitor produced a forecast verified on the same BTC venue, cutoff, issue time and 24 hourly targets as this branch. Public binary-probability dashboards and daily/24h model journals remain separate shadow references.
- No champion is promoted. The 5m council is experimental, and its Gaussian-style P90 bands are not calibrated.
- The daily marker triggers a fresh workflow run. The new run's artifact must be inspected and archived before any current numeric forecast is reported.

**Next experiment:** compare the 5m council with a volatility-aware and seasonal-naive baseline on identical non-overlapping origins; then test Student-t and jump-mixture interval calibration. Add R-RISI only if a legal and point-in-time data path is documented. Keep round-number levels as scenario thresholds, not technical barriers.


### 19. Fresh public-data run — 2026-11-13

GitHub Actions run 43389711067 completed successfully on branch HEAD dcd26af142ce33da65a86ee4212ba56d50a77e48. The 5m offline suite passed **9/9 tests**; the live public-data forecast step and artifact upload also succeeded.

- Issue time: 2026-11-13T07:59:32.881650Z.
- Cutoff: 2026-11-13T07:54:59.999Z.
- Binance Spot BTCUSDT 5m; 999 closed candles; reference 68,640.54 USDT.
- The 70,000 USDT threshold was already above the reference price: reference was about 1.94% below the threshold. Therefore the threshold had already been crossed before issue time.
- LFM5mEnsemble +24h: 68,421.59 USDT; uncalibrated P90 65,482.66–71,492.42.
- DownsideStress5m +24h: 65,659.95 USDT; uncalibrated P90 62,839.64–68,606.84.
- RandomWalk +24h: 68,640.54 USDT; uncalibrated P90 65,692.21–71,721.20.
- Momentum5m +24h: 68,043.79; MeanReversion5m: 68,968.47; VolatilityRegime5m: 68,496.08; TakerFlow5m: 68,648.58 USDT.

The model's heuristic terminal probability below 70,000 was 0.9979. Because the reference was already below 70,000, this is not a probability of a future downward crossing. The estimate is uncalibrated and must not be treated as a market-implied probability. The -6% scenario price was 64,522.11 USDT, but it is a deterministic illustrative shock, not a probabilistic forecast.

The final target hour opens at 2026-11-14T07:00:00Z and closes at 07:59:59.999Z. No full 24-hour evaluation is yet available. The 2026-11-12 vintage also remains pending until its final target candle closes.

### 20. Downside-threshold semantics corrected in 0.4

The 0.3 output exposed a semantic ambiguity: its severe-tail field marked a level as “crossed” whenever the scenario endpoint was below it, even if the reference price was already below the level. Version 0.4 now records whether the reference is already below the threshold, the signed reference-vs-level percentage, and whether the scenario ends below it. The crossing flag is true only for a move from at/above the threshold to below it. The heuristic probability is explicitly labelled as a terminal-state estimate, not a first-passage probability. Two new tests cover already-below and true-crossing cases.

No forecast parameters were tuned and no predictive skill is inferred from this semantic correction.


### 21. LFM-5m 0.4 live run and semantic regression tests — 2026-11-13

GitHub Actions run 43390773073 completed successfully on branch HEAD f96cabdf94c9c8e231a7c7f81a3fb229162605a9. The offline 5m suite passed **11/11 tests**, including two new threshold-state tests; live public-data forecast and artifact upload both succeeded.

- Issue time: 2026-11-13T08:07:42.649816Z.
- Data cutoff: 2026-11-13T08:04:59.999Z.
- Binance Spot BTCUSDT 5m; 999 closed candles; reference 68,665.21 USDT.
- The 70,000 USDT level was already breached: reference_vs_level_pct = -1.907%.
- LFM5mEnsemble +24h: 68,422.33 USDT; uncalibrated P90 65,480.71–71,496.09.
- DownsideStress5m +24h: 65,467.16 USDT; uncalibrated P90 62,652.59–68,408.17.
- RandomWalk +24h: 68,665.21 USDT; uncalibrated P90 65,713.15–71,749.89.
- Momentum5m +24h: 68,030.99; MeanReversion5m: 68,979.86; VolatilityRegime5m: 68,477.27; TakerFlow5m: 68,672.03 USDT.

The 0.4 heuristic terminal-state estimate below 70,000 is 0.9986, but it is uncalibrated and not a probability of a new downward crossing. The reference is already below the level. The illustrative -6% scenario ends at 64,545.30 USDT; it is not a probabilistic forecast.

The 0.4 target grid starts at 2026-11-13T09:00:00Z and ends at 2026-11-14T08:00:00Z; the final target candle closes at 08:59:59.999Z on Nov 14. No full 24-hour evaluation is yet available. The 0.3 and 0.4 vintages on Nov 13 overlap by 23 hours and must not be counted as independent daily samples.

The separate repository-wide tests workflow again failed before pytest because pip install -e . encountered setuptools flat-layout auto-discovery of top-level packages chess, research and ambivikhry. This is outside the research branch's intended scope; no root packaging files were changed.

### 22. Data sufficiency and forecast classification

The 999 closed 5m candles span only about 3.47 days. They are enough for the current 5m prototype's minimum data gate, but not enough to estimate 90-day seasonal phase effects or a robust week-of-hour profile. No seasonal feature was added.

This is an hourly-target forecast generated from 5m inputs for Binance Spot BTCUSDT. It is not a validated BTC/USD hourly champion. No champion promotion, calibrated interval claim, external leaderboard rank or virtual point is justified.


### 23. Sentiment, attention, news surprise and microstructure review — 2026-11-14

This review adds a separate behavioral/news ablation protocol. No sentiment, attention, news or clock-phase feature was enabled in a forecast model.

#### Primary findings (source text checked 2026-11-14)

1. **Han, Liu & Sui, Dallas Fed Working Paper 2605 (manuscript dated 2026-02-23; posted 2026-03-02), “Social Network and Sentiment Contagion: Evidence from the Bitcoin Market.”** The 62-page preliminary working paper studies Bitcointalk conversations from 2012-05-01 to 2022-07-30: 666,006 posts from 44,356 users, with 2,550 users linked to voluntarily disclosed public wallet addresses. Market inputs include CoinAPI hourly returns/volume, daily volatility, RavenPack news sentiment and Google search volume. The authors distinguish peer sentiment exposure from aggregate contagion intensity: peer sentiment moves users' beliefs and next-day trading choices; the abstract says peer sentiment itself does not predict future prices, while contagion intensity predicts volatility, volume and crashes. The introduction also describes a cumulative net contagion measure that negatively predicts future returns. These are different constructs and must not be collapsed into one “sentiment score.” The paper is preliminary, the sample ends in 2022, and RavenPack/CoinAPI inputs are not a ready-to-reuse public dataset. Source: https://www.dallasfed.org/research/papers/2026/wp2605 ; PDF: https://www.dallasfed.org/~/media/documents/research/papers/2026/wp2605.pdf

2. **Huynh (2026), “Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets,” Journal of Behavioral and Experimental Finance 101183, DOI 10.1016/j.jbef.2026.101183.** The publisher abstract reports 5-minute data for the top 100 cryptocurrencies over 2014–2021, scheduled US macroeconomic announcements, and daily cryptocurrency-specific sentiment from Thomson Reuters MarketPsych/TRMI. Bullish sentiment moderates the market response to macro surprises; a one-standard-deviation increase is reported to reduce return response by about 16% and turnover response by about 24%. This supports testing a sentiment × surprise interaction, not treating polarity as a standalone price-direction signal. The historical period, broad multi-asset sample and daily sentiment timing limit transfer to current hourly BTC. Full article text was not accessible in this review; claims are abstract-level. Source: https://doi.org/10.1016/j.jbef.2026.101183

3. **Akbar (2026-05-06), “Human signals, automated noise: identifying the true drivers of crypto volatility,” Studies in Economics and Finance, DOI 10.1108/SEF-12-2025-0942.** The publisher abstract describes more than 16 million Bitcoin-related tweets, account groups classified as human-like or automation-like, return-prediction tests, GARCH-X and VAR. It reports that polarity, hype, anxiety and divergence do not predict returns, while public attention improves conditional-variance modelling and appears to react to price shocks. This is an abstract-only check: full text and code were not available here, and account-classification details require replication. Source: https://doi.org/10.1108/SEF-12-2025-0942

4. **Shynkevich (first published 2026-02-18), “Trading Periodicity and Algorithmic Divide in Cryptocurrency Markets,” Journal of Futures Markets 46(5), 904–930, DOI 10.1002/fut.70089.** The published abstract reports subsecond periodicity in BTC/ETH spot and perpetual futures; recurring activity bursts increase volatility and transaction costs but do not cause a significant adverse price impact. The largest share of price discovery is associated with proprietary-algorithm liquidity taking. Data are available from the author on reasonable request. This is a useful counterweight to the July 2026 quarter-hour preprint: periodicity may be a volatility/liquidity control without being a reliable directional signal. Source: https://doi.org/10.1002/fut.70089

5. **Haroon (2026-07-25 preprint), “Bitcoin Price Direction Prediction via Regime-Aware Multi-Modal Fusion of Social Sentiment and Technical Features,” arXiv:2607.23370.** The paper describes 3,491 aligned hourly observations, BTC-USD OHLCV, Reddit FinBERT sentiment and a daily news-sentiment auxiliary feature, with 3h/6h directional classification. Reported 3h AUC is 0.5084; 6h AUC is 0.4902. The test set is 1,345 observations from July–September 2025. The text contains an unresolved regime-threshold inconsistency: the data section defines the volatility median over the full dataset, while the training algorithm says it is computed from the training set. The 6h AUC is below 0.5; the reported F1 advantage therefore does not establish robust probability ranking or price-path skill. No matching 24-step price forecasts or code license were identified. Source: https://arxiv.org/abs/2607.23370

6. **Bieganowski & Ślepaczuk (2026-01-31 preprint), “Explainable Patterns in Cryptocurrency Microstructure,” arXiv:2602.00776.** Uses Binance Futures perpetual 1-second order-book/trade data (2022-01-01 to 2025-10-12) across BTC, LTC, ETC, ENJ and ROSE; CatBoost/GMADL with time-series cross-validation predicts a 3-second mid-price return. This is a microstructure-feature reference, not a spot hourly or 24h forecaster. Source: https://arxiv.org/abs/2602.00776

7. **Chikhi, Diebolt, Mishra & Alhussaini (2026), “Forecasting Bitcoin Prices Movements: Memory, Path Dependence and Persistence,” Czech Journal of Economics and Finance 76(1), 54–86, DOI 10.32065/CJEF.2026.01.03.** The publisher PDF describes daily BTC prices in AUD/CAD/EUR/GBP/USD from Coincheck, 2018-06 to 2024-06 (2,193 observations), and rolling-window ARFIMA-GAS/EGAS/AEGAS models with skewed Student-t errors, leverage and jumps. Its reported out-of-sample return/volatility window is 2024-06-11 to 2024-08-28 and the paper reports better loss than random walk. It is daily, not hourly; the holdout is short and venue/currency differ from Binance Spot BTCUSDT. Treat as a statistical challenger blueprint, not a directly comparable external forecast. Sources: https://journal.fsv.cuni.cz/article/forecasting-bitcoin-prices-movements-memory-path-dependence-and-persistence/ ; PDF: https://journal.fsv.cuni.cz/wp-content/uploads/sites/17/2026/03/CJEF_2026_01_to_editor_C_CHIKHI.pdf

8. **Wang, Huang & Liao (2026), “Multi-scale decomposition for deep learning-based Bitcoin price forecasting,” Finance Research Letters 96(C), DOI 10.1016/j.frl.2026.109776.** The accessible abstract reports hourly BTC data from 2016-01-01 to 2025-06-30 and a VMD + deep-learning framework, with VMD-CNN reported best. The abstract does not expose the exact forecast horizon, complete metrics, rolling-origin protocol or code. Full text is paywalled in the checked source. Record as a multi-scale decomposition candidate only. Source: https://doi.org/10.1016/j.frl.2026.109776

9. **Choi (2026), “Intrinsic multifractality and adaptive efficiency in Bitcoin,” Physica A 697, 131735, DOI 10.1016/j.physa.2026.131735.** The accessible abstract record reports about 774,000 five-minute observations (2017-08 to 2024-12), q-Gaussian rescaling, a roughly 25-day scaling crossover and a post-ETF change in the Market Deficiency Measure. Publisher full text was not available in this review, so details remain abstract-level and no independent replication is claimed. It motivates a diagnostic ablation, not a forecast signal. Source: https://doi.org/10.1016/j.physa.2026.131735

10. **Takaishi (2026-09-03 preprint), “Quantum Circuit Learning for Volatility Modeling: Multifractal Analysis of Realized Volatility Time Series,” arXiv:2609.04569.** The abstract describes 5-minute BTC returns aggregated to daily realized volatility, a single-qubit model and MF-DFA of generated volatility/return series. This is a volatility-model/statistical-signature study, not a point-price forecasting benchmark. Source: https://arxiv.org/abs/2609.04569

#### Research decisions

- Separate sentiment polarity, attention/activity, network contagion, macro surprise and crypto-news novelty into different feature families.
- Treat attention/contagion primarily as candidate volatility/liquidity state variables until a point-in-time ablation demonstrates incremental hourly price-path value.
- Do not infer a price-direction signal from a sentiment or news interaction result measured on daily or multi-asset data.
- No source code, weights, tokenizers, datasets or article text were copied. No forecast model or champion was changed.
- The metaphor “living/non-repeating fractal” remains a hypothesis-generating lens, not an empirical conclusion.
