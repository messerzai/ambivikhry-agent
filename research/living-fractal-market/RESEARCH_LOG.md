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


### 24. Public BTC forecast systems and human-crowd ledgers — 2026-11-14

- CoinPredict's opened track record reports 6,710 graded 24h calls across assets (54% direction, 83% inside its 80% range). Its BTC page reports 18 graded BTC 24h calls (56% direction, 77.8% in-range, 0.9% median base-case miss). Its methodology describes a volatility-based range model and a cross-coin gradient-boosted direction model; hourly calls use a separate model. The latest BTC 24h snapshot on the page is model 1d-20261105-0358, made 2026-11-11 00:00 UTC, expiring 2026-11-12. This is a public scalar terminal forecast with a small BTC sample, not a 24-point hourly path. Sources: https://coinpredict.net/track-record ; https://coinpredict.net/price-prediction/bitcoin ; https://coinpredict.net/methodology
- Satori's accuracy page reports 237 BTC forecasts in the last 30 days, 50.6% directional accuracy, 1.07% average error (equal to its no-change baseline), and 75.5% inside the network's central 80% range; only 11 days were checked in the displayed period. Full forecast access requires 1,000 SATORIEVR or $5/month. No token, payment, wallet or account was used. Sources: https://satorisignals.app/accuracy ; https://satorisignals.app/forecasts
- SignalTrace Lab displays a 24h BTC up probability of 47.0% against a historical upward frequency of 48.2%, labels the result an uncalibrated baseline, and shows 2,536 historical comparisons. The opened page's issue time is 2026-11-10 00:00 UTC, so it is stale; a search snippet suggested a later edition, but the opened page was used for the audit. Source: https://signaltracelab.com/en/bitcoin/
- BitPredict's BTC 24h page describes timestamped member UP/DOWN calls, but the displayed member split (71% UP, 29% DOWN; 87 calls) is from 2026-11-02 15:39 UTC. It is not a current forecast. Free submission still requires registration; automated participation terms were not verified, so no account or submission was made. Source: https://www.bitpredict.io/predictions/bitcoin/next-24-hours
- Coinbase's prediction-market page displays BTC hourly/15-minute threshold contracts. These are market-implied event probabilities, not a model forecast of a 24h price path; no trading was performed. Source: https://www.coinbase.com/predictions/crypto/BTC/Hourly

Dynamic page discrepancy: CoinPredict's homepage search snippet showed a populated hourly board, while the opened page showed no call for the current hour; its separate track-record page remained populated. The live/opened source and versioned ledger were preferred over cached snippets. No new external score is comparable to the current LFM vintage.


## Research review — 2026-11-14, run 4

### Higher-moment tail risk in Bitcoin spot and perpetual futures

Karagiorgis and Ballis (first published 2026-05-28), “Time-Varying Skewness–Kurtosis Dynamics in Bitcoin Markets,” Journal of Futures Markets 46(8), 1440–1452, DOI: https://doi.org/10.1002/fut.70117.

The paper uses minute-by-minute Binance BTC spot and BTCUSDT perpetual data from 2020-10-01 through 2022-09-30 (2,102,398 minute observations), constructing hourly realized skewness and Pearson kurtosis. It requires at least 50 valid observations per hour and excludes zero-volume hours rather than forward-filling. A quadratic skewness–kurtosis regression with HAC errors (24 lags) is compared with a time-varying state-space/Kalman specification. The squared-skewness coefficient is about 1.53 in both spot and futures. Unexpected volume is positively associated with kurtosis in futures but not significantly in spot; the cross-market interaction is positive. Crucially, the volume association changes sign under 0.5/99.5 winsorization, indicating concentration in extreme-return episodes. The authors explicitly interpret results as conditional associations, not causal effects. Data are available from the corresponding author on request; no public code or dataset license was identified.

Point-in-time caution: the paper's baseline unexpected-volume definition subtracts a full-sample mean of log-volume. That is not safe for a live predictor. Our independent implementation must use only trailing/past data (e.g. a rolling 24-hour expected-volume estimate), and must keep Spot and Perpetual separate. The paper's one-minute input is also essential: twelve 5-minute returns per hour are not a defensible substitute for sixty one-minute returns when estimating hourly skewness and kurtosis.

Source: https://onlinelibrary.wiley.com/doi/full/10.1002/fut.70117

### Daily probabilistic explosive-state forecasting

Li, Jian-Rong, Guang-Yan Zhong, and Jiang-Cheng Li (2026-10-08), “Forecasting Explosive Bubble Regimes in Bitcoin Time Series with Multi-Step Ensemble Learning,” Entropy 28(10), 1096, DOI: https://doi.org/10.3390/e28101096.

The peer-reviewed article uses daily Investing.com BTC data from 2016-01-01 to 2026-04-09, with Yahoo Finance BTC/USD as a cross-source robustness series. GSADF/BSADF labels identify 30 uninterrupted explosive-state episodes (455 days). Nine classifiers (LR, KNN, SVM, DT, RF, XGBoost, LightGBM, ANN, LSTM) and three probability ensembles are evaluated for 1-, 3-, and 7-day occurrence/continuation labels. The design purges seven forecast origins at temporal boundaries, confines SMOTE to training samples, and uses moving-block bootstrap/MCS uncertainty analysis. No single model dominates. At 1 day, the constrained least-squares ensemble has the lowest reported MSE; at 3 and 7 days logistic regression does. The 90% MCS retains multiple models at all horizons. Only 43 positive labels occur in the 1-day final test and 77 in the 7-day final test; the best 7-day recall is about 0.51. The target combines new bubble onset and continuation, so it is not an onset-only detector and is not a 24-step hourly price forecaster. Processed data are available from the corresponding author upon request; raw data are attributed to Investing.com/Yahoo Finance. No source-code repository is linked in the article.

Decision: add as a separate daily probabilistic risk-state challenger, not to the BTC hourly price-path leaderboard. A future clean-room GSADF implementation must use point-in-time recursive windows and independently sourced data. Do not use full-sample transformations in live features.

Sources: https://www.mdpi.com/1099-4300/28/10/1096 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC13703411/

### High-frequency cross-asset network structure

Shukla, Shubhangam, Mahesh Peyyala, and Abhijit Chakraborty (2026-06-24), “Time-dependent weighted directed networks of cryptocurrency interaction from high-frequency returns,” arXiv:2606.25466.

The preprint constructs one-minute VWAP and volume series from Kraken trade-level data (2020–2025), partitions them into 275 non-overlapping weekly windows, estimates pairwise Granger-causality links with BIC lag selection (maximum 10) and Benjamini–Hochberg FDR control at 5%, and describes time-varying cross-asset network centrality. This is a market-interaction diagnostic, not a BTC price forecast. Its text normalizes returns using full-sample means and standard deviations; those transformations must not be copied into a point-in-time feature pipeline without refitting strictly inside each training window. The preprint's code/data reuse terms were not established.

Source: https://arxiv.org/abs/2606.25466

### Research decisions

- Add hourly realized skewness/kurtosis as a future risk-state diagnostic only, and only from one-minute data with explicit valid-observation thresholds.
- Add trailing-only volume surprise, never full-sample demeaning.
- Keep spot and perpetual series separate; do not infer spot BTC/USD price-path alpha from futures-only or cross-asset network findings.
- Keep GSADF bubble-state probabilities at daily 1/3/7-day horizons, separate from hourly price forecasts.
- No new forecast feature, model weight, source code, dataset, token, or external API was reused in this review.



## Research review — 2026-11-15

### Scaling, non-stationarity and multifractal falsification

Cho, Kim, Kim, Noh and Lee (published 2026-10-29), “Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity,” *Frontiers in Physics* 14, 2026031, DOI 10.3389/fphy.2026.2026031. This is a peer-reviewed **Perspective**, not a new BTC forecast experiment. It argues that scaling exponents, entropy and efficiency measures depend on regime, venue, sampling and market organization rather than behaving as universal constants. Its five explicit research priorities are genuine multifractality, crash early warning, endogenous market clocks, systemic-risk networks and time irreversibility.

The article's methodological warning is directly relevant to LFM: shuffled surrogates alone do not establish nonlinear multifractality. It recommends matched shuffled, phase-randomized and IAAFT surrogates, finite-size confidence bands, explicit scaling-range/crossover uncertainty, q-range sensitivity, and matched rolling windows across venues/assets. It also emphasizes that a visually fitted pre-crash pattern is not a real-time early-warning model; prospective evaluation must report lead time, false alarms, precision/recall, calibration and economic loss.

Decision: strengthen the existing MF-DFA protocol with IAAFT, phase-randomized and distribution-matched finite-size nulls; report crossover uncertainty and q sensitivity; treat calendar-time versus activity-time as a separate experiment. No fractal feature is enabled in the forecast model. “Living/non-repeating fractal” remains a hypothesis-generating metaphor, not an established market law.

Sources: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.2026031/full ; https://doi.org/10.3389/fphy.2026.2026031

### Retail sentiment: R-RISI and point-in-time data

Wagner and Metzler, ECB Working Paper No. 3276 (2026-08-24), “When the Crowd Speaks: AI-based retail investor sentiment indicator with Reddit data,” and their ECB Blog post (2026-11-12), “Reading the room: what Reddit tells us about retail investor sentiment,” describe an engagement-weighted, daily sentiment indicator based on Reddit posts. The paper covers 2015–April 2026 and describes GPT-5.1 sentiment/topic classification. The public dashboard now documents 14 finance/investing/crypto communities, a confidence threshold of 0.70 for sentiment indicators, engagement weight ln(1 + displayed score) + ln(1 + comments), separate positive/negative totals, previous-365-day rolling standardization excluding the current UTC day, and positive-z minus negative-z aggregation. It also exposes 7-day and 30-day smoothing.

Important version caveat: the current dashboard says the historical corpus used GPT-5.1 through December 2025, GPT-6.1 Sol from January 2026, and interim data from October 2026 uses Codex with GPT-6.1 Sol. This is not one homogeneous classifier vintage. The dashboard explicitly says R-RISI is a standardized sentiment-balance index, not a probability or return forecast, and that associations do not establish prediction or causality. The ECB blog describes next-day return associations, particularly for the S&P 500 during market downturns; the BTC-specific sub-indicator is a sentiment/price comparison, not an independently validated BTC hourly forecast.

Data provenance and rights require care: the dashboard identifies Pushshift/Academic Torrents monthly archives and Reddit Data API interim collection, and asks users of research/report outputs to cite and inform the authors. No blanket redistribution or commercial-use license for raw Reddit content is inferred. No corpus, post text, labels, code, API or dashboard data was copied.

Sources: https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3276~3ba8565a13.en.pdf ; https://www.ecb.europa.eu/press/blog/date/2026/html/ecb.blog20261112~a4c8b903d9.en.html ; https://dashboard.r-risi.workers.dev/

### Macro-news surprise × sentiment at five-minute frequency

Huynh (2026-06), “Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets,” *Journal of Behavioral and Experimental Finance* 50, article 101183, DOI 10.1016/j.jbef.2026.101183. The publisher abstract and accessible article text describe five-minute data for the top 100 cryptocurrencies from 2014-01-01 to 2021-12-31, volume-weighted CoinMarketCap prices across venues, scheduled U.S. macroeconomic announcements and daily Thomson Reuters MarketPsych cryptocurrency sentiment. The author reports immediate, category-dependent return and turnover reactions to macro announcements; one standard-deviation higher bullish sentiment is associated with about 16% lower return response and 24% lower turnover response to macro surprises. Robustness checks include alternative sentiment measures and releases from other major economies.

Limitations: the sample ends in 2021, the asset universe is cross-sectional rather than BTC-only, sentiment is daily, and the reported event-response moderation is not a 24-step BTC price forecast. The publisher search record describes the article as open access under a Creative Commons license, but the exact license variant and any data/code reuse terms were not independently confirmed in this review. No article text, source code, TRMI data or CoinMarketCap dataset was copied.

Decision: create a point-in-time event/sentiment design, but keep macro surprise, crypto-news novelty, sentiment and attention as separate feature families. Consensus snapshots must be frozen before release; sentiment engagement must use the snapshot observable at forecast time; no post-release revisions or future Reddit scores may leak into earlier features. See NEWS_SENTIMENT_PROTOCOL.md.

Source: https://doi.org/10.1016/j.jbef.2026.101183

### Research decisions and status

- Added NEWS_SENTIMENT_PROTOCOL.md as a design-only document with event provenance, point-in-time cutoffs, pre-registered ablations, placebos, leakage tests and rights gates.
- No sentiment, news, macro-surprise or new multifractal feature was added to a forecast model.
- No external code, model weights, tokenizers, datasets, raw social posts, API credentials or paid services were used.
- The next empirical priority remains a source-data snapshot for every 5m vintage, followed by the seasonality baseline and only then point-in-time news/sentiment ablations.


## Research review — 2026-11-15, follow-up run 4 (08:33 UTC)

### 1. Scaling, multifractal falsification and market clocks

Cho, Kim, Kim, Noh and Lee, “Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity,” *Frontiers in Physics* 14 (published 2026-10-29), DOI https://doi.org/10.3389/fphy.2026.2026031, is a peer-reviewed Perspective rather than a new forecast benchmark. It argues that scaling exponents, entropy and efficiency measures vary with regime, sampling and market organization. Its proposed minimum standard for genuine multifractality is to compare MF-DFA with shuffled, phase-randomized and IAAFT surrogates; compute finite-size confidence bands from length- and marginal-matched ensembles; report scaling-range/crossover uncertainty; and test q-range sensitivity. It also recommends matched rolling comparisons across assets and venues.

Decision: preserve the existing MF-DFA diagnostic, but add IAAFT and phase-randomized nulls plus finite-size confidence bands before interpreting any nonlinear component. Treat calendar-time versus activity-time as a separate experiment. No fractal feature is enabled in a forecast. “Living/non-repeating fractal” remains a hypothesis-generating metaphor, not an established market law.

Source: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.2026031/full

### 2. Regime-dependent volatility forecasting

Wafi, El-Halaby and Aboul-Dahab, “Regime-dependent bitcoin volatility forecasting under alternative information sets: evidence from econometric, deep learning, and hybrid models,” *Digital Finance* 8, 63 (published 2026-10-26), DOI https://doi.org/10.1007/s42521-026-00229-9. The paper uses 2,722 balanced daily observations (2018-02-01 to 2025-07-19), rolling one-step-ahead conditional-volatility forecasts, nested technical / technical-plus-sentiment / technical-plus-sentiment-and-blockchain information sets, QLIKE as primary loss, and Diebold–Mariano comparisons. Its reported best specification changes by regime: LSTM-T is numerically best in normal periods but statistically indistinguishable from TGARCH and Hybrid_GARCH_T; different GARCH–LSTM hybrids lead in different crises.

Limitations: the target is daily volatility, not an hourly BTC price path; results are regime- and information-set-dependent; the authors explicitly caution against universal model-superiority claims. The linked replication repository advertises code/data but has no LICENSE file in the inspected default-branch root, so no code or data were copied.

Decision: add this as a daily-volatility challenger and methodological reference for nested information-set ablations, not to the hourly price-path leaderboard.

Sources: https://link.springer.com/article/10.1007/s42521-026-00229-9 ; https://github.com/Wafi-Finance/Regime-Dependent-Bitcoin-Volatility-Forecasting

### 3. Event-time BTC/USD order-book forecasting

Raffaelli, Cestari, Marazzina and Formentin, “Forecasting Bitcoin price movements using multivariate Hawkes processes and limit order book data,” *Decisions in Economics and Finance* (published 2026-04-17), DOI https://doi.org/10.1007/s10203-026-00570-z. The paper compares HawkesTime (multivariate Hawkes event timing plus a continuous-time output-error model driven by base imbalance) with HawkesSign (direct event/sign prediction) on BTC/USD limit-order-book event streams. The reported design uses temporally separated subsets and 50 sampled trading scenarios, with short training/test windows; it also reports a second BTC/USD regime and an ETH/USD robustness sample. The authors report stronger sign accuracy for HawkesTime than the HawkesSign and moving-average baselines.

Limitations: this is next-event / next-mid-price-sign microstructure research, not a 24-hour hourly price-path forecast. The reported trading simulation is not independently reproduced here and must not be treated as live profitability evidence. The article itself notes spoofing/order-book manipulation as a potential limitation. The companion repository collects Bitfinex LOB data and trains/simulates multivariate Hawkes processes; its code is GPL-3.0. No code or raw order-book data were copied.

Decision: retain as an event-time challenger only if a separately licensed, point-in-time L2 data pipeline becomes available. Do not infer that 5m OHLCV or taker-buy volume reconstructs LOB excitation or base imbalance.

Sources: https://link.springer.com/article/10.1007/s10203-026-00570-z ; https://github.com/Learning2Control/MultivariateHawkesLOB

### 4. Sentiment-augmented latent volatility

Mukherjee, Giridharan, Li and Wu, “Fear Moves Markets: Sentiment-Augmented POMP for Volatility Modeling of Bitcoin Returns,” arXiv:2609.23250 (2026-09-19, preprint). The paper extends a Bretó partially observed Markov process by adding the Fear & Greed Index to latent volatility dynamics and Student-t observation noise. It uses daily BTC returns and FGI from 2020-01 to 2025-04, estimates with iterated filtering, and reports log-likelihood / particle-filter effective-sample-size comparisons against GARCH, stochastic volatility and the original Bretó model. The implementation uses 2,000 particles.

Limitations: likelihood fit and filter stability are not the same as leakage-safe forward forecast accuracy; the paper does not establish incremental H24 price-path value. Its linked GitHub repository has no LICENSE file in the inspected root. No code, dataset or FGI series were copied.

Decision: keep as a sentiment/volatility research challenger; require a chronological rolling evaluation and a licensed point-in-time sentiment source before considering any feature.

Sources: https://arxiv.org/abs/2609.23250 ; https://github.com/abeyankargiridharan/Novel_Approach_to_Volatility_Analysis_on_Bitcoin_Returns

### 5. Operational forecast and evaluation audit

The daily marker already existed for 2026-11-15 (run marker `lfm-daily-20261115-0804z-r5`), and the branch already contained a successful forecast workflow and a separate completed-vintage evaluation/archive cycle. To avoid creating a second same-day vintage after archival, this review did not update `DAILY_RUN_TRIGGER.md` again.

Verified forecast workflow: https://github.com/messerzai/ambivikhry-agent/actions/runs/43693158620, source checkout commit `10c8f7033a88ecb5533781e36144cf718d9997ec`. The offline 5m tests passed 11/11; live public-data retrieval/forecast passed; artifact upload passed. Artifact ID `14153835047`, ZIP SHA-256 `4f9af1f7dc4dd9bc9b47feaa91f8b27b33e302bf36f45d3f76491e001b488731`. Downloaded artifact was re-hashed locally; extracted `forecast_5m.json` SHA-256 `58663b5a5b7c76931bdbd3aab41941a1cf09f792795961b0f25bc95dbff5ff8c`, matching the repository ledger.

Verified evaluation workflow: https://github.com/messerzai/ambivikhry-agent/actions/runs/43694193141; evaluation tests, matured-vintage evaluation and artifact upload all passed. The evaluation manifest records two new matured evaluations, two already-evaluated vintages, and two still-pending 2026-11-15 vintages. A corrupt gzip mirror for the 2026-11-13 07:59 vintage was correctly suppressed in favour of the canonical workflow ZIP; a regression test was added in commit cddf0ddb43455ff318c910d26f884bfc1ec497f2.

Forecast JSON audit: schema `lfm.forecast.5m.v1`; 999 closed Binance Spot BTCUSDT 5m candles; issue 2026-11-15T08:09:18.020362Z; cutoff 2026-11-15T08:04:59.999000Z (258.0 seconds before issue); reference 64,078.57 USDT; 7 models × 24 common hourly targets from 2026-11-15T09:00:00Z through 2026-11-16T08:00:00Z. All points were finite and positive and all target grids matched. The lookback is only 83.25 hours, not the preferred 90 days.

Schema gap: the emitted JSON does not explicitly include `input_interval`, `model_commit`, `vintage_id` or a separate retrieval timestamp. The immutable ledger supplies some of this provenance, but the JSON should be self-describing. Proposed next code change: add these fields and tests in a later cycle; do not mutate this archived vintage. The JSON's Gaussian-style P90 ranges are explicitly uncalibrated, so there are no calibrated 50%/90% intervals and no tournament points.

### 6. Matured-vintage score summary

Four 24-hour vintages are evaluated. LFM5mEnsemble normalized hourly log-price MAE versus random-walk and volatility-capped slow-drift baselines:

| Issue UTC | LFM ensemble nMAE | Random walk nMAE | Volatility-aware nMAE | Result |
|---|---:|---:|---:|---|
| 2026-11-12 08:03 | 9.4641 | 9.0509 | 7.3504 | loses to both |
| 2026-11-13 08:07 | 1.8265 | 1.9175 | 2.3634 | beats both |
| 2026-11-13 07:59 | 1.7186 | 1.7426 | 2.5965 | beats both |
| 2026-11-14 07:18 | 5.5006 | 5.2052 | 3.0107 | loses to both |

Only 2 of 4 vintages beat the baselines, and the two Nov 13 forecasts overlap by about 23 hours. The 24 hourly targets within a vintage are serially dependent. P90 intervals remain uncalibrated; every evaluation awarded 0 virtual points. This is descriptive evidence only, not proof of skill and not a basis for champion promotion.

The 2026-11-15 07:37 and 08:09 vintages remain pending until their final hourly closes on 2026-11-16 07:59:59.999Z and 08:59:59.999Z respectively. Do not score them early.

### 7. Next experiment and safeguards

1. Add explicit forecast JSON provenance fields (`input_interval`, `model_commit`, `vintage_id`, `retrieved_at_utc`) and regression tests without rewriting old artifacts.
2. Build a paginated, immutable 90-day Spot 5m dataset; keep Spot and perpetual/L2 streams separate.
3. Add seasonality and volatility-aware controls before testing MF-DFA, news or sentiment features.
4. Keep Hawkes LOB, daily GARCH–LSTM, POMP and TimesFM as separate horizon/target challengers.
5. Preserve the 30-completed-daily-vintage promotion threshold and calibrated-interval requirement.

No model weights, source code, datasets, tokenizers, news feeds, social-media posts or paid APIs were copied or used. No trades, transfers or order execution occurred.


## 8. Literature review — 2026-11-16

### 8.1 Bitcoin multifractality across a long five-minute sample

Insu Choi, “Intrinsic multifractality and adaptive efficiency in Bitcoin: Disentangling sources of scaling complexity across market regimes,” Physica A: Statistical Mechanics and its Applications, 697(C), 131735 (2026), DOI https://doi.org/10.1016/j.physa.2026.131735.

The publisher-indexed abstract reports approximately 774,000 five-minute BTC observations from August 2017 to December 2024. The paper applies q-Gaussian rescaling to distinguish genuine from spurious multifractality, reports a scaling crossover near 25 days, and compares pre/post-January-2024 spot ETF regimes. The abstract reports a greater-than-half decline in its Market Deficiency Measure after ETF approval and a negative association between realized volatility and multifractal complexity.

Evidence limitation: the full publisher text is subscription-restricted in this review. These are abstract-level claims; implementation details, robustness tables, exact sample construction and replication code were not independently inspected. The paper is a multifractal diagnostic, not an H24 price forecast. No code, data or figures were copied.

Research implication: add q-Gaussian-rescaling as a separately pre-registered diagnostic candidate, not as a production feature. Compare it with shuffled, phase-randomized and IAAFT surrogates and report window-length sensitivity. Do not interpret the reported crossover as a universal 25-day market law.

Source: https://ideas.repec.org/a/eee/phsmap/v697y2026ics0378437126004711.html

### 8.2 Regime-gated sentiment for sub-daily BTC direction

Muhammad Abdullah Haroon, “Bitcoin Price Direction Prediction via Regime-Aware Multi-Modal Fusion of Social Sentiment and Technical Features,” arXiv:2607.23370 (2026-07-25, preprint), https://arxiv.org/abs/2607.23370.

The paper describes 3,491 aligned hourly BTC-USD observations from July 2024 to September 2025; 2,146 training rows and 1,345 chronological test rows. Inputs combine OHLCV/engineered price features, Reddit FinBERT sentiment and a binary rolling-volatility regime. RAML predicts 3h and 6h direction. Reported full-model macro-F1 is 0.5474 (3h) and 0.5513 (6h); AUC is 0.5084 (3h) and 0.4902 (6h). At 3h, the price-only model AUC is 0.4968 and the sentiment-only model AUC is 0.4938. The reported true-down specificity for RAML is 44.6%.

Limitations: 14 months of aligned observations and 2,146 training rows are small for a dual-branch BiLSTM; the 6h AUC is below 0.5, and 3h AUC is only marginally above chance. The paper is a preprint, not an independently reproduced result. Its Reddit/Kaggle data and model artifacts have separate terms; no reusable code repository/license was identified in this review. No code, raw posts, sentiment data or weights were copied.

Research implication: the regime-gated fusion idea merits a clean-room, point-in-time ablation only after licensed sentiment data and timestamp availability are secured. Evaluate directional probability calibration, downside specificity and incremental value against price-only and simple volatility-aware baselines. Do not treat F1 alone as evidence of predictive value.

### 8.3 Behavioural, on-chain and uncertainty mediation

Marcel Figura, Martin Bugaj, Elvira Nica and Gheorghe H. Popescu, “Bitcoin Volatility Forecasting Through Market Sentiment, Blockchain Fundamentals, and Endogenous Market Uncertainty,” Forecasting 8(3), 41 (2026-05-19), DOI https://doi.org/10.3390/forecast8030041.

The peer-reviewed open-access article uses 262 weekly observations from 17 January 2021 to 18 January 2026 and PLS-SEM with a forward-dated future historical-volatility target. Its abstract reports a strong association between Market Uncertainty and future historical volatility (beta 0.864) and mostly indirect links from blockchain fundamentals through uncertainty. The discussion explicitly says GARCH(1,1) has lower raw forecast error in the sample; the proposed architecture is benchmark-sensitive and should be interpreted as predictive-associational.

Limitations: weekly volatility target, one asset, 262 observations and a structural-association design; it is not an hourly BTC price-path model. Data sources named include Google Trends, CoinMarketCap, Blockchain Data Explorer and Yahoo Finance; each source has independent terms. No code repository or dataset bundle was identified or copied.

Research implication: treat uncertainty as a candidate intermediate risk-state feature, not as a direct sentiment signal. If tested, require a strict chronological forecast ablation against GARCH/HAR/persistence controls.

### 8.4 Financial time-series foundation-model benchmark

Miquel Noguer i Alonso and Rodolfo Pereira Franklin, “Pretrained Time-Series Foundation Models for Financial Return Forecasting,” arXiv:2606.27100 (2026-06-25, preprint), https://arxiv.org/abs/2606.27100.

The benchmark compares TimesFM-2.5, Chronos/Chronos-2, Moirai-2.0 and TimeGPT-family models with N-BEATS, N-HiTS, PatchTST, iTransformer and KAN on five US equities, daily returns, 512-step context and 20-session horizons across ten rolling-origin tasks. The authors report TSFMs winning 8/10 task rankings, but gains over the zero-return random-walk baseline are small and sparse; one-sided Diebold-Mariano tests reject equal/inferior accuracy only for Chronos on AMZN and Moirai-2.0 on GOOG.

Limitations: equity, daily-return and 20-session results do not transfer directly to BTC/USDT or BTC/USD hourly levels. The preprint is not a BTC-specific result. No implementation or weights were copied.

Research implication: retain Chronos-2 and TimesFM-2.5 as challengers, but do not promote on cross-asset leaderboard rank. Equalize context and evaluate directly on identical BTC origins against random walk and volatility-aware controls.

### 8.5 Cross-study conclusions and next experiment

Facts: recent work supports testing regime dependence, nonlinear scaling diagnostics and behavioural information as separate hypotheses. It does not establish that these features improve our 24-hour hourly price forecast. In the sub-daily RAML preprint, the AUC evidence is near chance; in the weekly Figura et al. study, GARCH(1,1) has lower raw forecast error; in the TSFM equity benchmark, statistical gains over random walk are sparse.

Hypotheses: (H7) q-Gaussian rescaling may better distinguish correlation-driven multifractality from heavy-tail effects in BTC 5m returns; (H8) sentiment may add value conditionally in high-volatility regimes; (H9) an uncertainty mediator may improve volatility-state forecasts but not necessarily price levels.

Next experiment: build the immutable 90-day Spot 5m panel first; pre-register each feature ablation; use purged/chronological rolling origins, point-in-time feature timestamps, surrogate controls and block-bootstrap uncertainty. Keep all new features out of the live council until they beat the strongest simple baseline out of sample.

No source code, weights, datasets, raw social posts, tokenizers or paid services were copied or used in this review.


## 2026-11-17 — Research cycle 6: event-conditioned dynamics, LOB excitation and structural-regime cautions

### Evidence reviewed

**1. BTC/USD limit-order-book event dynamics (peer-reviewed, 17 Apr 2026).**  
Raffaelli, Cestari, Marazzina et al., *Forecasting Bitcoin price movements using multivariate Hawkes processes and limit order book data*, [DOI 10.1007/s10203-026-00570-z](https://doi.org/10.1007/s10203-026-00570-z). The paper uses Bitfinex tick-by-tick LOB updates (about 3 million updates and 375,000 mid-price changes in January 2024), then a distinct July 2025 BTC/USD period. HawkesTime forecasts the next mid-price event time using cross-excitation among event classes and uses a continuous-time output-error model with base imbalance to estimate the next return; HawkesSign predicts the next return sign directly. The paper reports HawkesTime outperforming HawkesSign and a five-return moving-average benchmark in 50 sampled 2-minute test scenarios; the COE model's 30-minute training window yielded 0.671 sign accuracy versus 0.640 for 15 minutes and 0.631 for 5 minutes. Limitations: event-level seconds-scale target, not a 24h price path; randomly sampled short test periods; trading simulations exclude transaction costs; spoofing is not filtered; code requires `tick` and MATLAB CONTSID. The result supports a separate microstructure research track, not promotion of the current 5m-candle council.

**2. Macroeconomic news surprises and crypto price discovery (Federal Reserve Board working paper, draft 20 Mar 2026).**  
Kroner, Mohammed and Vega, [How Do Cryptocurrencies Price Economic News?](https://users.nber.org/~confer/conf_papers/2387/f238700/f238700.pdf). The authors use CoinDesk minute-level transaction/quote data spanning 158 exchanges and 18,403 pairs (2015–2025), focusing on BTC/USD and ETH/USD on Binance, OKX and Coinbase around FOMC, CPI and NFP releases. They report volatility, volume and spreads rising at release and generally reverting within 15–30 minutes; contractionary policy shocks and inflation/employment surprises associated with higher yields produce negative BTC/ETH price responses. Order-flow price impact changes materially after 2021 and differs across venues. This is a strong reason to treat scheduled news surprise and venue-specific order flow as event-state variables. It is not a 24h predictive model; the underlying CoinDesk/LSEG data are not part of our public 5m feed, and no reproducible code/data package was identified in the working paper.

**3. Sentiment as a moderator of macro-news response (peer-reviewed, June 2026).**  
Nhan Huynh, *Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets*, [DOI 10.1016/j.jbef.2026.101183](https://doi.org/10.1016/j.jbef.2026.101183). The study covers the top 100 cryptocurrencies, high-frequency intraday market data and daily TRMI cryptocurrency-specific sentiment. Its abstract reports that a one-standard-deviation increase in sentiment reduces the return response to macroeconomic surprises by about 16% and turnover response by about 24%. The interpretation is conditional attenuation of news response, not a direct bullish/bearish signal. Limitations for our use: daily sentiment timing must be aligned before the release; results are pooled across the top 100 rather than a validated BTC-only 24h forecast; MarketPsych/TRMI data are not available in our current pipeline. No code or data were reused.

**4. On-chain weekly regimes (preprint, 12 Nov 2026).**  
*Persistent structural regimes in Bitcoin transactions relate to market cycles*, [arXiv:2611.16585](https://arxiv.org/abs/2611.16585). The paper applies a two-state hidden semi-Markov model to weekly Bitcoin transaction features over roughly 760 weeks, with daily market benchmarks. It reports a persistent transaction-network structure associated with broad market phases, but the authors emphasize only three completed falling phases, serial dependence, model-selection sensitivity, market-informed duration/segmentation choices and lack of causal identification. The reported correspondence does not carry over cleanly to the current downturn. This is a candidate for slow-moving regime description, not a real-time hourly signal; no runnable code repository was identified.

**5. Long-run power-law identification under persistent noise (preprint and registered replication, 7 Oct / 10 Nov 2026).**  
Baquero and Menezes, [arXiv:2611.13962](https://arxiv.org/abs/2611.13962), with [Zenodo preprint record](https://zenodo.org/records/23218857) and OSF registration [2rdty](https://osf.io/2rdty). The authors use low-frequency weekly averages and a simulation-calibrated, pre-specified test to assess constant drift versus a log-age term. They report that a nominal 5% rejection does not survive allowing persistence beyond a random walk; a Gompertz ceiling fits about as well as the power law. Prospective forecasts are registered for 2027–2030. This is not an hourly predictor, but it is directly relevant to guarding against trend extrapolation, small effective sample sizes and attractive-looking log-log fits. The companion software DOI is 10.5281/zenodo.23218897; its exact license metadata could not be verified in this run, so no software was downloaded or reused.

**6. Multi-scale patch Transformer for daily crypto forecasting (peer-reviewed, 2026).**  
Zhao, Crane and Bezbradica, *MSPCIFormer*, [DOI 10.1111/exsy.70343](https://doi.org/10.1111/exsy.70343). The paper uses 1,728 daily observations, a five-day input window, horizons of 1/3/5/7/15 days, a 70/10/20 chronological holdout and five expanding-window folds. In the BTC walk-forward table, MSPCIFormer has the lowest MSE at four of five horizons, while MDA is approximately 0.525–0.546. The study does not include a random-walk baseline or calibrated forecast intervals, and it does not evaluate a 24-point hourly path. The linked code repository has one commit and no LICENSE; its README acknowledges adapted components from PatchTST, MSGNet and iTransformer without a clear component-level license manifest. No code was copied.

**7. Public range forecasters and binary odds.**  
BtcForecaster's author reports 24h range coverage of 76.5% over 1,121 forecasts from 28 Oct–2 Nov, but those forecasts were issued every five minutes and are heavily overlapping; the author estimates only about five independent daily tests. The raw JSON endpoint was not accessible in this run, so the claim is not independently scored. The Brier Index page explicitly says its latest 16 Nov snapshot is not live; its 1d/7d/30d ranges are centered on the last Binance 00:00 UTC close, so it is range-only, not a 24-hour hourly trajectory. Mispria reports 2,395 Binance BTC/USDT hourly binary windows over 100 nights and Brier scores for market and distributional models, but the target is close-versus-open sign, not price level, and the displayed snapshot is dated 15 Nov. Keep these in separate shadow tracks.

### Hypotheses (not established facts)

- **H10 — event surprise × sentiment:** pre-release sentiment may moderate the response of realized volatility, order flow and short-horizon BTC returns to FOMC/CPI/NFP surprises. Test first on 15/30-minute volatility and turnover outcomes; only then test 1h/24h forecast loss. Sentiment must be timestamped before the release, and actual-minus-consensus surprise must not enter before its public release time.
- **H11 — LOB cross-excitation:** cross-excitation among price-change, liquidity-add and liquidity-remove events may add next-event sign information beyond imbalance-only and moving-average baselines. This requires a separately licensed, timestamped LOB feed; 5m OHLCV candles cannot reproduce the event process.
- **H12 — slow on-chain state:** weekly transaction-network features may describe a slow regime, but their value must be tested using strictly trailing features and rolling-origin validation. Full-sample medians, percentiles, or market-informed state boundaries would leak future information.
- **H13 — scaling-state dependence:** q-Gaussian rescaling and multifractal diagnostics may help separate heavy-tail effects from correlation-driven scaling in BTC 5m returns. They are diagnostics first; predictive value must be measured by ablation against volatility-aware baselines.
- **H14 — multi-scale daily models:** MSPCIFormer-like architectures may be useful for daily horizons, but daily results do not justify hourly transfer. A clean-room daily challenger would require a separate 90-day-plus BTC/USDT and/or BTC/USD data panel, a random-walk baseline and calibrated intervals.

### Engineering and evaluation decisions

- The 2026-11-17 forecast artifact passed the workflow's public-feed checks: 999 closed Binance Spot BTCUSDT 5m candles, cutoff 07:04:59.999Z, issue time 07:07:54.530285Z, 24 hourly target points. This is a challenger output, not a BTC/USD champion.
- The emitted forecast JSON still omits explicit `input_interval`, `retrieved_at_utc`, `model_commit`, `vintage_id` and `training_cutoff` fields. The ledger records the workflow source commit and archive hashes, but the JSON contract itself should be extended in a future code change. No code was changed in this cycle to avoid retriggering a second forecast after the daily marker had already run and been archived.
- Six forecast vintages have completed evaluation across four issue-date blocks (12, 13, 14 and 15 Nov); two overlapping pairs (13 Nov and 15 Nov) are not independent daily samples. LFM5mEnsemble was best in the two 13 Nov vintages; MeanReversion5m was best in the two 15 Nov vintages; random walk was best on 12 and 14 Nov. P90 empirical coverage varies materially and the intervals are explicitly uncalibrated; zero research points are awarded.
- No external point-price forecast is comparable on asset, venue, issue time, cutoff and all 24 target timestamps. External point-price leaderboard remains empty.

### Next experiment

1. Extend the forecast JSON schema with the missing immutable provenance fields, with tests and a single deliberate forecast workflow run.
2. Build and hash a paginated 90-day Binance Spot BTCUSDT 5m panel; separately document any BTC/USD venue series rather than relabeling USDT as USD.
3. Run an event study for scheduled FOMC/CPI/NFP releases using only point-in-time timestamps and available consensus/actual surprises. Keep the initial target to 15m/30m realized volatility and turnover.
4. Run an ablation of the event-state variables against the current volatility-aware baseline at 1h and 24h; use purged chronological origins and block-bootstrap uncertainty.
5. Keep Hawkes LOB work separate until a compliant raw LOB dataset and runtime are available. Do not copy GPL-3.0 code into the current repository without resolving distribution compatibility.

No third-party code, model weights, datasets, raw posts, proprietary sentiment feeds, LOB events or paid APIs were copied or used in this review.


## Daily research update — 2026-11-17 (run 6)

- Raffaelli, Cestari, Marazzina et al., *Forecasting Bitcoin price movements using multivariate Hawkes processes and limit order book data*, Decisions in Economics and Finance (published 2026-04-17), DOI 10.1007/s10203-026-00570-z. Publisher text checked 2026-11-17. Uses approximately 3 million millisecond Bitfinex BTC/USD LOB updates in Jan 2024; event types include mid-price changes, liquidity additions/removals and buy/sell pressure. HawkesTime combines multivariate Hawkes timing with a continuous-time output-error model driven by base imbalance; HawkesSign predicts event timing/sign directly. Three chronological thirds are used for sensitivity, temporal evaluation and trading simulation; each sampled 32-minute period has a 30-minute training and 2-minute test window. A second July 2025 sample is used for robustness. Limitations: next-event/very-short-horizon sign prediction, not hourly or 24-hour price forecasting; short sampled windows; spoofing not filtered; Bitfinex-specific LOB and Python/MATLAB stack. No tournament comparability.
- Takaishi, *Quantum Circuit Learning for Volatility Modeling: Multifractal Analysis of Realized Volatility Time Series*, Fractal and Fractional 10(7), 442 (published 2026-06-29), DOI 10.3390/fractalfract10070442. Publisher full text checked 2026-11-17. Uses Bitstamp 5-minute prices from 2020-08-31 to 2023-03-01 to construct daily realized volatility (913 days). A single-qubit circuit is fitted on the entire dataset; the article explicitly says there is no train/validation/test split and that its objective is reproducing statistical characteristics, not evaluating predictive performance. Multifractal/rough-volatility properties motivate diagnostics only, not forecast performance.
- Akbar, *Human signals, automated noise: identifying the true drivers of crypto volatility*, Studies in Economics and Finance 43(5), 1359–1388 (online 2026-05-06), DOI 10.1108/SEF-12-2025-0942. Publisher abstract checked 2026-11-17. More than 16 million BTC-related tweets are separated into human-like and automation-like accounts; polarity/hype/anxiety do not predict returns in reported specifications, while attention is associated with conditional variance and appears reactive to price shocks. Full text/data inaccessible; abstract-level evidence only.
- Vu & Nguyen, *Herding or hype? Investigating behavioural dynamics in cryptocurrency markets*, Review of Behavioral Finance 18(5), 505–526 (published 2026-08-31), DOI 10.1108/RBF-06-2025-0254. Publisher abstract checked 2026-11-17. CSSD/CSAD and rolling panel analysis of BTC plus 25 altcoins (2020–2024) reports weak herding in extreme states, greater dispersion during high volatility and Google Trends sentiment associated with return divergence. Full text inaccessible; cross-sectional results are not direct BTC price-direction evidence.
- Huynh, *Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets*, Journal of Behavioral and Experimental Finance 50 (2026), 101183, DOI 10.1016/j.jbef.2026.101183. Publisher search record checked 2026-11-17: top 100 crypto assets, 5-minute data, U.S. macro announcements and daily TRMI sentiment (2014–2021); sentiment moderates announcement response. Exact article reuse license and TRMI rights remain unverified; no code/data copied.
- Dos Santos, Di Antonio & Javarone, *Persistent structural regimes in Bitcoin transactions relate to market cycles*, arXiv:2611.16585v1, submitted 2026-11-12. Weekly on-chain measures (2012–2026) and a two-state hidden semi-Markov model without price data; authors report historical regime-price alignment that breaks in the ongoing downturn. Preprint evidence, not a stable predictive law. arXiv record links CC BY 4.0; no code or blockchain data copied.

### Hypotheses and experiment decision

1. Separate attention intensity from sentiment polarity; test first as a volatility/interval-width feature, not a directional price-drift signal.
2. Model news surprise as an interaction with point-in-time sentiment/regime state; never use daily sentiment published after the forecast cutoff.
3. Hawkes/LOB methods may add value at sub-second/second horizons, but do not substitute for 24 hourly price targets. A 5m OHLCV taker-buy proxy is not full order-book event flow.
4. Test multifractal diagnostics against shuffled, phase-randomized and heavy-tail-preserving nulls with finite-sample bands and rolling windows. A synthetic model reproducing a spectrum is not evidence of future-price predictability.

The only code change in this cycle is forecast provenance: add input interval, retrieval timestamp, immutable source commit, vintage ID and explicit rolling-feature cutoff to JSON; pin workflow checkout to the triggering commit. Forecast equations and model version remain unchanged. No external code, weights, datasets, raw posts, order-book events or paid APIs were copied.

## Additional evidence audit — 2026-11-17 (run 6 follow-up)

- Takaishi (2026), https://doi.org/10.3390/fractalfract10070442: 913 daily realized-volatility observations from Bitstamp 5m prices (2020-08-31–2023-03-01). The single-qubit QCL is fitted on the entire RV sample; the paper explicitly has no train/validation/test split and does not evaluate predictive performance. It generates 50,000 synthetic steps. It also compares 200 Gaussian surrogates of length 913 and notes that finite-size effects alone can create apparent multifractality. The model's generated return Hurst exponent near 0.5 is partly expected by construction. This supports a null-model/finite-sample caution, not a forecast feature claim.
- Huynh (2026), https://doi.org/10.1016/j.jbef.2026.101183: top-100 crypto assets, 5m market data from 2014–2021, 32 U.S. macro announcement classes and daily TRMI sentiment. The paper reports a one-standard-deviation increase in bullish sentiment reduces return response to macro surprises by about 16% and turnover response by about 24%. It is evidence for state-dependent event response, not a standalone directional predictor; the sample ends in 2021 and TRMI data rights are separate from article rights.
- Akbar (2026), https://doi.org/10.1108/SEF-12-2025-0942: more than 16m BTC-related tweets, separate human-like and automation-like accounts, and separate attention/sentiment indices. Publisher abstract reports polarity/hype/anxiety have no return-prediction value, while attention increases conditional variance and reacts to price shocks. Treat attention as a possible volatility-state variable, not a direction signal; full data/text unavailable.
- Vu & Nguyen (2026), https://doi.org/10.1108/RBF-06-2025-0254: BTC plus 25 major altcoins, 2020–2024, CSSD/CSAD and Google Trends. Publisher abstract reports weak herding in extreme states and stronger dispersion in high-volatility regimes. Cross-sectional dispersion does not establish BTC directionality.
- Raffaelli et al. (2026), https://doi.org/10.1007/s10203-026-00570-z: about 3m Bitfinex millisecond LOB updates in Jan 2024, 50 sampled 2-minute tests per chronological subset, 30-minute COE training; reported HawkesTime sign accuracy 0.671 for that configuration. The authors omit transaction costs in simulations and do not filter spoofing. The signal is next-event LOB sign, not 24h price. The linked implementation is GPL-3.0; no code copied.
- Mispria (public operator report, https://mispria.com/performance): through Nov 15, 2026, 124 nights and 187,361 windows; aggregate order-book Brier 0.0550 vs model 0.0575. The BTC 1h subset reports 2,419 windows and a different per-market Brier comparison (market 0.0276 vs Student-t 0.0262). These aggregate and subset metrics must not be conflated. The site's own methodology notes overlapping windows and cross-asset dependence, so nominal independent-window uncertainty is too narrow.


## Daily research cycle — 2026-11-18 (run 7)

### Evidence reviewed and research implications

- **ECB R-RISI:** Wagner & Metzler, ECB Working Paper No. 3276 (24 Aug 2026), *When the Crowd Speaks: AI-based retail investor sentiment indicator with Reddit data*, plus ECB blog *Reading the room* (12 Nov 2026). The indicator uses LLM sentiment/topic/ticker labels (ChatGPT 5.1), engagement weighting and rolling 365-day z-scores over Reddit investment and crypto posts. The ECB reports more than 9m posts and timely associations with next-day equity returns particularly in market downturns; its BTC-specific sentiment series is volatile and diverges from BTC prices more often. This is not a validated BTC 24h forecasting result. Point-in-time availability, post-collection latency, topic/ticker errors, engagement weighting, seven-/30-day smoothing, and underlying Reddit/data/API terms are material. Treat BTC sentiment as a regime/attention challenger, not a signed-return feature until an out-of-sample ablation.
  Sources: https://www.ecb.europa.eu/pub/research/authors/profiles/fabian-wagner.et.html ; https://www.ecb.europa.eu/press/blog/date/2026/html/ecb.blog20261112~a4c8b903d9.en.html
- **Complexity-based exchange-quality diagnostics:** Zwydak, Wątorek, Kwapień & Drożdż, *Detecting Unusual Trading Patterns on Cryptocurrency Exchanges by Means of Complexity Measures*, Entropy 28(7), 804 (15 Jul 2026), DOI 10.3390/e28070804. On 1-minute BTC/ETH/XRP transaction data across Binance, Bitget, KuCoin and Kraken (Apr–Jun 2025), the authors report a Bitget anomaly after mid-May: transaction count rose disproportionately to volume and returns, with weaker autocorrelation/multifractal structure and higher short-pattern irregularity. Public trade data do not identify beneficial ownership; the authors explicitly do not prove wash trading. Implication: add exchange/volume/trade-count integrity checks to the long-history ingestion experiment before trusting taker-flow or complexity features.
  Source: https://www.mdpi.com/1099-4300/28/7/804
- **Sentiment extremity and spread uncertainty:** Farzulla, arXiv:2602.07018 (revised 2026), *The Extremity Premium*. The extended daily F&G sample (2018–Jan 2026, 2,896 days) reports a small volatility-demeaned effect (Cohen d≈0.21) from an exploratory pooled test. The pre-specified within-volatility-quintile tests do not survive Holm correction; residual spread–uncertainty correlation falls to r≈0.043 (p≈0.25) after purging volatility. The extended Granger statistic F=211 is partly mechanical because a high-low input is shared. Treat as a cautious liquidity/uncertainty regime hypothesis, not causal proof or directional alpha.
  Source: https://arxiv.org/abs/2602.07018
- **Sentiment-aware POMP volatility:** Mukherjee et al., arXiv:2609.23250 (19 Sep 2026) use daily BTC returns and F&G (2020–Apr 2025), a latent POMP model with differenced sentiment and Student-t observation noise. The paper compares conditional log-likelihood/filter stability against GARCH, HSV and the original Bretó model; it reports better fit/stability, but it does not present a matching BTC hourly point-forecast evaluation. The linked GitHub repository has no visible license at checked HEAD, so no code was copied.
  Sources: https://arxiv.org/abs/2609.23250 ; https://github.com/abeyankargiridharan/Novel_Approach_to_Volatility_Analysis_on_Bitcoin_Returns

### Hypotheses (not established facts)

1. Trade-count/quote-volume mismatch and complexity changes may be useful as a data-quality or liquidity-risk gate, not necessarily a price-direction signal.
2. BTC-specific Reddit sentiment may help identify regime/attention shifts, but it must be timestamped, delayed and tested for incremental value over volatility alone.
3. F&G extremity may proxy uncertainty and liquidity conditions; use it for interval-width/risk-state ablations only after leakage-safe normalization.
4. Daily sentiment/POMP evidence and 1m microstructure findings cannot be transplanted directly to 24 hourly price levels.

### Live forecast and completed evaluation

- Run 44256430979 issued a fresh BTC/USDT 24-hour hourly council forecast from 999 closed Binance Spot 5m candles. Exact archive and hashes are in FORECAST_LEDGER.md. LFM5mEnsemble +24 = 64,803.50 USDT from 64,684.16 reference (+0.1845%); P90-style range is uncalibrated.
- Run 44256431018 evaluated the Nov 16 vintage using 24 completed Binance Spot hourly closes and preserved the exact response. VolatilityRegime5m was the best council member (nMAE 0.668837), LFM5mEnsemble third (0.670892); RandomWalk 0.736703, VolatilityCappedSlowDrift 1.760475. Directional accuracy vs issue reference was 0.583 for drift-positive members, hour-to-hour accuracy 0.500. All P90-style intervals covered 24/24 but mean width ≈6.85%; calibration flag remains false. No points awarded.

### Experiment decision

No model code or forecast equations changed. Next: build a paginated 90-day 5m dataset with exact raw provenance; audit venue-level trade-count/quote-volume anomalies; then compare volatility-only, complexity/data-quality gate, sentiment-regime and news-surprise interaction variants on the same non-overlapping daily origins. Use null models for MF-DFA and strict point-in-time features. Do not fit a sentiment feature until source terms and release/collection timestamps are verified.


## Daily research cycle — 2026-11-19 (run 8)

### Evidence reviewed

- **Kim, Lee & Choi (23 May 2026), “Comparative Analysis of Cryptocurrency Market Efficiency and Local Features Using MF-DFA and DCC-GARCH,” Fractal and Fractional 10(6), 353.** The authors study 11 crypto/fiat pairs (BTC, ETH, XRP, BCH against KRW/USD/JPY) over Jan 2018–Sep 2025. Rolling MF-DFA uses 250-day windows, with robustness checks at 200 and 300 days; they report time-varying Hurst/spectrum-width estimates and high same-asset cross-fiat return correlations. Their phase-randomized surrogate experiment uses 99 FFT surrogates and reports rank p=0.010, the smallest attainable with 99 surrogates. This supports treating scaling estimates as time-varying diagnostics rather than constants. Limitations: daily sampling rather than 5m/hourly; data are available from the corresponding author on request rather than as a public dataset; p=0.010 is resolution-limited; the exact surrogate implementation should be replicated and checked for marginal-tail preservation rather than assuming plain phase randomization is equivalent to IAAFT. No evidence here that MF-DFA features improve 24h BTC point forecasts.
  Source: https://doi.org/10.3390/fractalfract10060353

- **Drożdż et al. (13 Oct 2025), “Multifractality and Its Sources in the Digital Currency Market,” Future Internet 17(10), 470.** The MFCCA/MF-DFA source-decomposition study reports that temporal correlations are the primary source of the observed multifractal spectrum in its crypto samples; heavy tails broaden the spectrum conditionally, but do not by themselves establish genuine multifractality. The paper explicitly motivates shuffled/Gaussianized controls. This remains a diagnostic result, not predictive evidence.
  Source: https://doi.org/10.3390/fi17100470

- **Wagner & Metzler, ECB Working Paper 3276 (24 Aug 2026) and ECB Blog (12 Nov 2026), “When the Crowd Speaks / Reading the room.”** The R-RISI work labels Reddit posts by sentiment/topic/ticker with an LLM, weights posts by engagement, and standardizes using rolling one-year z-scores; the public blog describes smoothing and a BTC-specific sub-index. The ECB reports that the BTC series is more volatile and diverges from BTC price more often than some equity-oriented measures. The broad indicator is associated with next-day equity returns particularly in downturns; this is not a demonstrated BTC hourly or 24h direction forecast. The smoothing, collection latency, post deletion/edits, ticker/topic classification and Reddit/API/data terms all require point-in-time and rights review.
  Sources: https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3276~3ba8565a13.en.pdf ; https://www.ecb.europa.eu/press/blog/date/2026/html/ecb.blog20261112~a4c8b903d9.en.html

- **Thapa & Cho (3 Aug 2026), “A Multifractal Cross-Correlation Framework for Cryptocurrency Pairs Trading with CAPM Filtering,” Fractal and Fractional 10(8), 530.** The abstract describes market-model filtering followed by MFDCCA for pair selection and risk-adjusted pairs-trading tests. This is a cross-asset dependence/pairs-trading study, not a BTC hourly price-level forecast; its reported strategy results cannot be compared with the LFM nMAE tournament.
  Source: https://doi.org/10.3390/fractalfract10080530

### Methodological implications and hypotheses

1. Add rolling MF-DFA only after a sufficiently long, timestamp-consistent 5m history exists. Start with a paginated 90-day sample (25,920 5m bars), then extend toward 200–250 days if data quality and compute permit.
2. For each window, compare original data against shuffled, phase-randomized and IAAFT surrogates; use block bootstrap/finite-size checks and multiple scale ranges. A broad spectrum alone is not evidence of a predictive signal.
3. Treat R-RISI-like sentiment as a low-frequency attention/regime covariate, not a signed 5m/1h return signal. Test only after verifying point-in-time post timestamps, latency, data terms and leakage-safe normalization.
4. Add trade-count/quote-volume consistency and rolling entropy as data-quality/liquidity diagnostics before testing them as predictive features.
5. The phrase “living/non-repeating fractal” remains a metaphor. The measurable claim is narrower: estimated scaling properties may vary with regime, venue and sampling clock, and may or may not add out-of-sample forecast value.

### Daily experiment result

- Branch-isolated 5m council run 44479201588 succeeded: 13/13 offline tests; Binance public data retrieval, 24-hour hourly forecast generation and artifact upload succeeded.
- Evaluation run 44479201628 succeeded: 11/11 evaluator tests; two Nov 17 vintages evaluated, one Nov 18 vintage remains pending, zero failures.
- Archive run 44479201553 succeeded: 12/12 archival tests; exact forecast and evaluation artifacts, extracted JSON and exact hourly actuals were committed to the branch.
- General CI run 44479201548 succeeded: 52/52 tests on each of Python 3.10, 3.11, 3.12 and 3.13.
- No forecasting equations or model code changed in this cycle. Research, competitor and license documentation were updated separately; no third-party code, weights, datasets or dashboard payloads were copied.


## Daily research cycle — 2026-11-22 (run 11)

### Original research checked

- **Brian Sing Fan Chan & Jennifer So Kuen Chan, “Neural Realized Measures: Forecast-Supervised Intraday Aggregation for Volatility Forecasting,” arXiv:2611.07287 (2026-11-05; arXiv record identifies ICAIF ’26, 14–17 November).** The paper learns positive mean-one weights over 5m RV/BV/Garman–Klass contributions while preserving the classical realized-measure primitive; the downstream heads are SF, HAR and MIDAS. It uses Binance spot price indices for six assets, 288 bars per UTC day, with validation 2023-06…2024-05 and test 2024-06…2026-05. The authors report NRM beating its paired RRM in all 54 QLIKE comparisons, with mean gains 7.23%, 8.15% and 9.22% across SF/HAR/MIDAS; BTC selected NRM QLIKE 0.278 vs RRM 0.301. This is next-day realized-volatility evidence, not price-direction or 24-step price-level evidence. It omits volume/order-book features, and no public code/weight repository was found. Treat proceedings status cautiously until the official proceedings record is verified. Source: https://arxiv.org/abs/2611.07287
- **Vanheusden et al., “Nonlinear dynamics in cryptocurrency markets: a recurrence quantification analysis approach,” Financial Innovation 12, 127 (2026-06-03), DOI 10.1186/s40854-026-00940-x.** The paper applies RQA to 100 cryptocurrencies using USD closing-price histories from CoinLore through 2025-04-19; historical event windows use 80-day segments. Its volatility-prediction exercise uses 5-day windows and 5–50 day horizons; the determinism/laminarity ratio performs best at 42 days (AUROC 0.605, bootstrap comparisons against full and block randomization). The authors emphasize recurrence-threshold/embedding sensitivity. Data are available from the corresponding author on request; methods are implemented in MATLAB R2024b, with no public code repo located. This is a medium-horizon regime diagnostic, not an hourly point-price forecast. Source: https://doi.org/10.1186/s40854-026-00940-x
- **Zwydak, Wątorek, Kwapień & Drożdż, “Detecting Unusual Trading Patterns on Cryptocurrency Exchanges by Means of Complexity Measures,” Entropy 28(7), 804 (2026-07-15), DOI 10.3390/e28070804.** The authors aggregate tick trades to 1-minute return, volume and trade-count series for BTC/ETH/XRP on Binance, Bitget, KuCoin and Kraken (2025-04-01…2025-06-30), then use MFDFA/MFCCA, autocorrelation, ApEn/SampEn and a rolling change-point analysis. They report a Bitget BTC/ETH trade-count regime shift after 2025-05-21 without proportional volume or return changes. They explicitly cannot infer wash trading or identify the underlying mechanism from aggregate public trade data. Data are described as available through public exchange APIs. This supports exchange-specific data-quality diagnostics, not a claim that price is “non-repeating.” Source: https://doi.org/10.3390/e28070804
- **Anastasopoulos, Gradojevic, Liu, Maynard & Tsiakas, “Order flow and cryptocurrency returns,” Journal of Financial Markets 79 (2026-06), 101047, DOI 10.1016/j.finmar.2026.101047.** The study uses daily data for 84 cryptocurrencies (2018-01-01…2022-06-30) and 11 fiat-denominated international order flows. Panel and expanding-window ML tests report incremental out-of-sample information from world order flow for daily cross-sectional returns. Data are available on request. It is not a BTC/USD hourly price-level test; the paper's world order-flow variable is not interchangeable with Binance taker-buy imbalance. Source: https://doi.org/10.1016/j.finmar.2026.101047
- **Zouari, Alon & Shtudiner, “Heterogeneous collective criticality in cryptocurrency volatility: Scaling collapse, tail synchronization, and cascade amplification,” Chaos, Solitons & Fractals 211 (2026-10), 118809, DOI 10.1016/j.chaos.2026.118809.** The accessible institutional record reports daily/hourly BTC/ETH/SOL volatility analysis: BTC is boundary-adjacent with a circular-block interval crossing CR=1; tail-clustering depth and boundary distance differ; intraday estimates are scale/estimator sensitive. Full text was not accessible, so this remains abstract-level evidence. No price forecast or fixed critical threshold is established. Source: https://doi.org/10.1016/j.chaos.2026.118809
- **Shynkevich, “Trading Periodicity and Algorithmic Divide in Cryptocurrency Markets,” Journal of Futures Markets 46 (2026), 904–930, DOI 10.1002/fut.70089.** The publisher abstract reports subsecond periodicity in BTC/ETH spot and perpetuals; periodic surges raise volatility and transaction costs but do not create significant adverse price impact. Data are available from the author on request; full text was not accessible. This is a microstructure-confounding mechanism, not an hourly predictor. Source: https://doi.org/10.1002/fut.70089

### Sentiment/news and behavioral-finance interpretation

No new point-in-time, freely reusable sentiment/news feed or new direct 1h BTC forecast evidence was established in this pass. Prior findings remain important: Huynh (2026) reports that sentiment moderates high-frequency crypto responses to U.S. macro surprises; Han, Liu & Sui (Dallas Fed WP 2605, 2026) report that peer sentiment shifts beliefs but does not predict future BTC prices, while contagion predicts volatility/activity. Neither result licenses treating a generic sentiment score as a signed BTC hourly signal. No sentiment or news feature was added.

### Testable hypotheses and limitations

1. After a longer, point-in-time 5m history is archived, test whether robust rolling trade-count/quote-volume deviations improve data-quality gating or forecast calibration. Start with a surveillance diagnostic, not an alpha feature. Use venue-specific baselines and do not label an anomaly “wash trading.”
2. The current 999-bar feed is about 3.5 days and is too short for the cited 7-day rolling diagnostics, 80-day RQA windows or stable multifractal estimates. Build a paginated 90-day 5m sample before attempting MF-DFA/MFCCA/RQA or transaction-count change-point work.
3. NRM suggests an ablation on task-adaptive within-day aggregation for realized volatility. It should be evaluated as a volatility challenger against HAR/realized-measure baselines, not silently inserted into the hourly point-price champion.
4. Cross-venue/multi-currency order flow is a separate data requirement. The current Binance Spot 5m taker-buy imbalance is not a substitute for the paper's world order-flow variable.
5. “Living/non-repeating fractal” remains a metaphor. The measurable claim is that estimated scaling/recurrence and activity relationships can vary with regime, venue and clock; predictive value must be demonstrated out of sample.

### Daily experiment and evaluation status

- The 5m council forecast workflow succeeded and archived a fresh BTC/USDT 24-hour hourly challenger vintage. The exact artifact, raw response, extracted JSON and hashes are in FORECAST_LEDGER.md.
- At the evaluation run's cutoff, no target vintage was newly completed. Twelve unique historical vintages are evaluated; four are pending after including the new 07:43 UTC issue. The 2026-11-21 vintage remains pending until its final hourly close at 2026-11-22 07:59:59.999 UTC.
- For the official internal aggregate, only eight chronologically selected non-overlapping completed vintages are included; four other completed vintages are excluded from aggregate scoring because their 24h target grids overlap. The small sample does not support promotion.
- No calibrated intervals exist. All virtual points remain 0.
- No forecast equations or model code changed in this cycle. Documentation and provenance registers were updated; no third-party code, weights, datasets or API outputs were copied.


## Daily research cycle — 2026-11-24 (run 12)

Branch: `research/living-fractal-market`  
Daily trigger commit: [11edd105](https://github.com/messerzai/ambivikhry-agent/commit/11edd10500612193e04d3c15bdbcf615b1ec0fb4)  
Forecast workflow: [45346501172](https://github.com/messerzai/ambivikhry-agent/actions/runs/45346501172) — success  
Archive workflow: [45346501185](https://github.com/messerzai/ambivikhry-agent/actions/runs/45346501185) — success  
Evaluation workflow: [45346501166](https://github.com/messerzai/ambivikhry-agent/actions/runs/45346501166) — success  
Archive commit: [a2631de](https://github.com/messerzai/ambivikhry-agent/commit/a2631de520e121eeb70a6e82170c388a4eae1688)

### Research discoveries (facts)

1. **Source disentangling remains central to multifractal claims.** Drożdż, Kluszczyński, Kwapień & Wątorek, “Multifractality and Its Sources in the Digital Currency Market,” *Future Internet* 17(10), 470 (2025), DOI [10.3390/fi17100470](https://doi.org/10.3390/fi17100470). The paper applies MFCCA/MF-DFA and a q-Gaussian rescaling procedure to BTC, ETH, DEX and NFT series. Its reported conclusion is that nonlinear temporal correlations are the primary source of multifractality in the examined series; heavy tails modulate spectrum width conditionally rather than acting as an independent additive source. The study is not a BTC hourly forecasting benchmark and does not prove a non-repeating market law. Article license is CC BY 4.0; no text, figures, code or data were copied.

2. **A new 2026 Bitcoin study reports a scale crossover, not a universal exponent.** Insu Choi, “Intrinsic multifractality and adaptive efficiency in Bitcoin: Disentangling sources of scaling complexity across market regimes,” *Physica A* 697 (2026), DOI [10.1016/j.physa.2026.131735](https://doi.org/10.1016/j.physa.2026.131735). The RePEc bibliographic/abstract record reports approximately 774,000 five-minute observations from Aug 2017 to Dec 2024, q-Gaussian rescaling, and a crossover around 25 days between short- and long-scale behavior. It also reports a lower Market Deficiency Measure and reduced long-range dependence after Jan 2024 ETF approval. Full text was not accessible in this review, so these are abstract-level claims only; no public code/data bundle or reuse license was identified. The 25-day result motivates a scale-sensitivity test, not a hard-coded threshold.

3. **Order-flow toxicity is more directly tied to jump risk than to signed hourly price paths.** Kitvanitphasu, Kyaw, Likitapiwat & Treepongkaruna, “Bitcoin wild moves: Evidence from order flow toxicity and price jumps,” *Research in International Business and Finance* 81 (2026), article 103163, DOI [10.1016/j.ribaf.2025.103163](https://doi.org/10.1016/j.ribaf.2025.103163). The peer-reviewed record describes high-frequency VPIN and VAR analysis; VPIN predicts future BTC price jumps, with time-zone/day-of-week effects. It does not establish a point-price directional forecast. The UWA record links the article to CC BY 4.0. No code or trade-level data were copied; our Binance 5m taker-buy imbalance is not VPIN and cannot be treated as an equivalent measure.

4. **News sentiment evidence is mainly daily and futures-specific.** Kreuzer, Sparrer & Dorfleitner, “Beyond pure hype: news sentiment and its role in the BTC and ETH futures market,” *Review of Derivatives Research* 29 (2026), DOI [10.1007/s11147-025-09223-6](https://doi.org/10.1007/s11147-025-09223-6). The study uses over 9,100 BTC and 5,400 ETH news articles from 2022-10-25 to 2024-08-30, sourced from LSEG Eikon, with CME cash-settled futures. It extends Loughran–McDonald sentiment using a crypto-specific glossary and crypto-density weighting, then aggregates to daily measures. The paper reports significant associations with futures returns and professional net positions; the daily news sample is unbalanced (about 90% negative, roughly 460 daily items after aggregation). This is not causal proof or evidence of a live hourly spot edge. The article is CC BY 4.0, but Eikon news and CME data retain separate access/usage terms; no source text, code, data or figures were copied.

5. **Prediction-market distributions offer a useful but non-matching hourly benchmark.** Tommaso Zeri, “How Wise Is the Crowd about Bitcoin’s Next Hour? Kalshi Range Contracts against Statistical Forecasts” (2026-11-20 research note, not peer-reviewed). It evaluates 1,340 hourly events (2026-09-13 to 2026-11-12) and compares market-implied range distributions with Student-t, seasonal GARCH-t and Deribit implied volatility. The note reports that actively quoted buckets produce 80% interval coverage around 81–84%; their CRPS advantage over a 24h-volatility Student-t is about 3%, while seasonal GARCH-t is competitive and only a small crowd advantage appears five minutes before settlement. The crowd median is worse than spot as a point forecast. This is hourly distribution evidence, not a 24h BTC/USDT point path; no market participation or wager was made.

### Research hypotheses (not established facts)

- Rolling multifractal features may describe regime-dependent volatility/complexity, but their incremental forecasting value must be tested against random walk, HAR/RV and volatility-aware baselines. Use q-Gaussian surrogate tests and multiple window lengths; do not hard-code “25 days” as a universal crossover.
- VPIN-like volume-synchronized features may add jump-risk information beyond simple taker imbalance. The current 5m spot aggregate is insufficient to claim VPIN; a separate trade-level or volume-bucket data pipeline would be required.
- News surprise and sentiment may add information around scheduled and unscheduled events, but a point-in-time, licensed news source with article timestamps, first-publication times and revisions is required. Daily futures evidence cannot be imported into a 5m spot model without an ablation.
- The “living/non-repeating fractal” remains a metaphor. The testable quantities are estimated scaling, recurrence, jump intensity, flow imbalance and regime transitions, each with finite-sample uncertainty.

### Daily forecast and data provenance

- Binance Spot BTCUSDT 5m public klines; reference 60,494.00 USDT; data cutoff 2026-11-24T07:09:59.999000Z; retrieved/issued 2026-11-24T07:14:55.953761Z / 2026-11-24T07:14:55.957774Z.
- 1,000 raw rows contained 999 closed candles plus one still-forming candle. Closed candles were contiguous at 5m cadence, timestamps and OHLCV checks passed, and the final close matched the reference. The forecast JSON and raw response hashes are in FORECAST_LEDGER.md.
- The council emitted seven paths with 24 contiguous hourly points. LFM5mEnsemble ends at 60,547.84 USDT (+0.089%). Its P90-style bands are not calibrated; no P50 interval was emitted. The workflow output is BTC/USDT with 5m inputs, not a BTC/USD champion forecast.
- The 70,000 USDT downside diagnostic is already below the reference price. Its uncalibrated terminal-state heuristic of 1.0 is not a new downward-crossing probability.

### Evaluation and standings

- The evaluator completed successfully but produced no new evaluation: 16 unique vintages were already evaluated; the Nov 23 issue remained pending through 2026-11-24T08:59:59.999Z. The newly archived Nov 24 issue is pending through 2026-11-25T07:59:59.999Z.
- Across 10 chronologically selected non-overlapping completed vintages, mean nMAE: RandomWalkLastPrice 3.396679; LFM5mEnsemble 3.526820; MeanReversion5m 3.388607; TakerFlow5m 3.398854; VolatilityCappedSlowDrift 4.201362. MeanReversion's paired 95% difference interval vs random walk crosses zero. Six overlapping completed vintages are excluded from aggregate selection.
- All P90-style ranges remain uncalibrated. Virtual research points: **0**. No champion promotion; the 30-vintage gate is unmet.
- External standings: none. BtcForecaster publishes volatility ranges, BitPredict binary 24h calls, Kalshi an hourly distribution, and GPTReviews daily directional calls; issue time, target object or metric differs. These remain shadow comparators only.

### License and implementation record

- No third-party code, model weights, datasets, tokenizers, API forecast payloads or raw news/market data were copied.
- Added a license audit for [btcforecaster-eval](https://github.com/pelusoft/btcforecaster-eval): HEAD `df027d80289b6294eb22e28f55221a21f19c664a`, MIT LICENSE blob `e89e1fa28e2c9a7eacd10442c05af6492b80f466`; no code or sample data reused.
- TimesFM 3.0 source remains Apache-2.0 but its 3.0 weights are separately licensed `timesfm-non-commercial-license-v1.0`; no weights used. Chronos-2 remains an Apache-2.0 candidate under the existing audit; pin its exact model-hub revision before loading.
- New papers with CC BY 4.0 are cited only; no article text or figures were copied. LSEG Eikon, CME, Kalshi and public API data terms are separate from article/code licenses.

### Changes and next experiment

- Documentation/register updates only: forecast ledger, competitor landscape, research log, and third-party license register. No forecast/model equations or dependencies changed.
- Next experiment: obtain a point-in-time 90-day Binance Spot BTCUSDT 5m history with immutable raw snapshots; compare rolling MF-DFA/MFCCA plus q-Gaussian surrogate diagnostics at 1d/7d/25d/90d scales against simple volatility features. Require at least 90 days before interpreting a 25-day crossover, freeze all feature parameters before a walk-forward split, and report whether multifractal features improve volatility forecasts. Do not promote them to point-price features without a separate ablation.


### Supplementary original-source review — 2026-11-24

6. **High-frequency macro surprises are a distinct event signal, not generic sentiment.** Huynh, “Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets,” *Journal of Behavioral and Experimental Finance* 50 (2026), article 101183, DOI [10.1016/j.jbef.2026.101183](https://doi.org/10.1016/j.jbef.2026.101183). The publisher/abstract record describes 5-minute returns and turnover for the top 100 cryptocurrencies from 2014–2021 around 32 U.S. macroeconomic releases, with daily TRMI sentiment. The study reports that a one-standard-deviation increase in bullish sentiment weakens the return response to macro surprises by about 16% and turnover response by about 24%; the effect is robust to alternative sentiment windows and several foreign announcement sets. Limitations: the sample ends in 2021, sentiment is daily rather than 5m, the top-100 selection may create survivorship bias, and this is event-response evidence rather than a prospective BTC/USD hourly forecast. The publisher states that the article is open access under a Creative Commons license, but the exact identifier was not verified; no article content or data was copied.

7. **Attention may matter more than sentiment polarity.** Akbar, “Human signals, automated noise: identifying the true drivers of crypto volatility,” *Studies in Economics and Finance* 43(5) (2026), 1359–1388, DOI [10.1108/SEF-12-2025-0942](https://doi.org/10.1108/SEF-12-2025-0942). The publisher abstract reports more than 16 million Bitcoin-related tweets, human-like/automation-like account classification, sentiment and attention indices, return models, GARCH-X and VAR/Granger analysis. Polarity, hype, anxiety and divergence do not predict returns across specifications; attention improves conditional-variance modelling but reacts to price shocks rather than forecasting them. Limitations: publisher abstract only, platform/account classification is imperfect, and no public code/data bundle was identified. Publisher marks reuse as licensed rights only; no text or data copied.

8. **Social contagion can forecast risk without forecasting price direction.** Han, Liu & Sui, “Social Network and Sentiment Contagion: Evidence from the Bitcoin Market,” Federal Reserve Bank of Dallas Working Paper 2605 (Feb 23, 2026), DOI [10.24149/wp2605](https://doi.org/10.24149/wp2605). The working paper uses 666,006 Bitcointalk posts from 44,356 users (May 2012–July 2022), with 2,550 users linked to on-chain trading records through voluntarily disclosed wallet addresses. It reports that peer sentiment changes individual beliefs and trading direction, but peer sentiment does not predict future BTC prices; contagion intensity predicts volatility, volume and crash outcomes. This is a preliminary working paper, not a peer-reviewed journal result. The historical forum/trading data are not a ready-to-use public model dataset; no data, posts, wallet mapping or code were copied.

9. **A broad, high-frequency macro-news study separates headline from non-headline surprise.** Kroner, Mohammed & Vega, “How Do Cryptocurrencies Price Economic News?” Federal Reserve Board working-paper draft (Mar 20, 2026). The draft uses CoinDesk minute-level transactions/quotes for 158 exchanges and 18,403 pairs (2015–2025), focusing on BTC/ETH spot on Binance, OKX and Coinbase around FOMC, CPI and NFP releases. It reports that volatility, volume and spreads rise around announcements and remain elevated for up to 30 minutes; both conventional headline and non-headline surprises matter, with non-headline surprises often stronger; risk-off/higher-yield surprises are associated with negative crypto returns. Limitations: working paper/preliminary, CoinDesk and LSEG Tick History data are licensed, sample coverage is unbalanced, and this is an event study rather than a full 24h point forecast. No code or data copied.

10. **Recent herding evidence is heterogeneous rather than a simple crowd-following rule.** Vu & Nguyen, “Herding or hype? Investigating behavioural dynamics in cryptocurrency markets,” *Review of Behavioral Finance* 18(5) (2026), 505–526, DOI [10.1108/RBF-06-2025-0254](https://doi.org/10.1108/RBF-06-2025-0254). The publisher abstract describes CSSD/CSAD and rolling-window tests on BTC plus 25 major altcoins (2020–2024), with Google Trends sentiment and volatility interactions. It reports weak herding in extreme states, greater dispersion under high volatility, and short-lived herding mainly in crisis periods. This argues against treating crowd consensus as a stable directional signal. Publisher reuse is licensed rights only; no article text, code or data copied.

11. **A separate FOMC study finds risk sentiment may dominate realised rate changes.** Savrul, “Federal Reserve Rate Decisions, Risk Sentiment, and Cryptocurrency Returns: Evidence from FOMC Event Windows,” *Journal of Economic Policy Research* 13(2) (2026), 616–634, DOI [10.26650/JEPR1945391](https://doi.org/10.26650/JEPR1945391). It covers 43 FOMC events and daily returns for BTC and major altcoins; because its surprise series has only two non-zero observations, it does not estimate a robust formal surprise effect. It reports little systematic return response to realised rate changes and more consistent VIX association, with weak/unstable DXY effects. The article license is CC BY-NC, so it is not a candidate for commercial-intended text/code reuse; no content or data copied.

12. **A sentiment-augmented volatility preprint is a challenger, not evidence of price direction.** Mukherjee et al., “Fear Moves Markets: Sentiment-Augmented POMP for Volatility Modeling of Bitcoin Returns,” arXiv:2609.23250 (2026). It combines daily BTC returns, Fear & Greed Index and Student-t observation noise in a partially observed Markov process, reporting improved log-likelihood/filter stability versus three volatility benchmarks on Jan 2020–Apr 2025. It is a preprint, daily volatility model, not a live hourly point forecast; no code or dataset license was identified in this check and nothing was copied.

### Updated interpretation

- The new evidence supports a **separation of channels**: (a) macro surprise and non-headline information can trigger short-lived price/volume/spread reactions; (b) sentiment can moderate the reaction; (c) attention/social contagion may explain volatility, volume and crash risk without a directional price edge; (d) crowd herding is regime-dependent and may become dispersion/anti-herding in stress.
- Do not collapse all of these into one sentiment score. Candidate ablations should separately test surprise magnitude, sentiment state, attention intensity and social-contagion proxies, with exact point-in-time timestamps and a licensed source.
- The current Binance Spot 5m pipeline has none of the licensed TRMI/Eikon/CoinDesk social-network or tweet data used in these studies. No feature is added until a lawful, reproducible, timestamped data source is available.


13. **Recurrence quantification is a promising regime/risk diagnostic, but its current BTC evidence is medium-term and early-stage.** Vanheusden, Kim, Almeida, Soriano & Verousis, “Nonlinear dynamics in cryptocurrency markets: a recurrence quantification analysis approach,” *Financial Innovation* 12, 127 (2026), DOI [10.1186/s40854-026-00940-x](https://doi.org/10.1186/s40854-026-00940-x). The peer-reviewed open-access article applies RQA to 100 cryptocurrencies using CoinLore daily closes and 80-day windows. It reports that a determinism/laminarity ratio helped predict volatility above the 95th percentile at a 42-day horizon (AUC 0.605; bootstrapped regression coefficient about 0.08), with 5-day rolling analysis over the Terra/Luna–FTX period. Important limitations: the AUC is modest, the result is early-stage and not a prospective public forecast ledger; the paper did not compare RQA with MFDFA; parameter selection was partly guided by visual comparison; datasets are available from the corresponding author on request; intraday validation is explicitly left for future work. The paper's license is CC BY-NC-ND 4.0, so it is not a basis for commercial adaptations or derivative code. No text, figures, code or data were copied.

14. **A recent perspective explicitly argues that scaling measures are state variables, not constants.** Cho, Kim, Kim, Noh & Lee, “Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity,” *Frontiers in Physics* (2026-10-29), DOI [10.3389/fphy.2026.2026031](https://doi.org/10.3389/fphy.2026.2026031). This Perspective synthesizes evidence that scaling exponents, entropy and efficiency indicators change with institutionalization, market regime and sampling conventions. It proposes five testable priorities: separate genuine multifractality from finite-size/distribution artifacts; validate crash warnings prospectively; identify an endogenous market clock; measure multilayer systemic risk; and test time irreversibility. It is a research agenda, not a new forecast benchmark.

### RQA and non-stationary scaling implications

- Treat RQA (DET, LAM, vertical entropy, trapping time) as a separate regime/risk challenger, not as a point-price forecaster. The reported 42-day horizon is not the user's 24h target.
- Reproduce parameter sensitivity (embedding (m), delay (	au), recurrence rate (arepsilon), norm and rolling window) before trusting any DET/LAM warning. The article itself notes that inappropriate thresholds can create false deterministic/laminar structures.
- Add RQA to the proposed 90-day feature study only as a pre-registered volatility diagnostic. Compare against HAR/RV and a simple realized-volatility threshold; use a strict rolling-origin test and report AUC confidence intervals and false-alarm rate. Do not use the article's CC BY-NC-ND text/figures/code as derivative material.


## 2026-11-24 follow-up — regime-dependent volatility forecast candidate

Wafi, El-Halaby & Aboul-Dahab, “Regime-dependent bitcoin volatility forecasting under alternative information sets: evidence from econometric, deep learning, and hybrid models,” *Digital Finance* 8, article 63 (version of record 2026-10-26), DOI [10.1007/s42521-026-00229-9](https://doi.org/10.1007/s42521-026-00229-9). The publisher's full article was checked on 2026-11-24.

**Reported design and findings (facts):**
- The target is one-step-ahead **daily conditional volatility**, not price direction or a 24-step hourly price path. The balanced evaluation sample has 2,722 complete daily observations from 2018-02-01 through 2025-07-19; the initial merged table extends to 2026-02-01, but the common-information intersection truncates the evaluated sample earlier.
- The paper compares six GARCH-family specifications, three LSTM information sets, and eighteen state-augmented GARCH–LSTM hybrids under rolling out-of-sample evaluation. QLIKE is primary; RMSE/MAE are secondary and Diebold–Mariano tests qualify numerical rankings.
- The LSTM uses 30 daily observations × 9 retained variables, two stacked layers (64 and 32 hidden units), and 0.20 dropout. Information sets are technical only (T), technical plus sentiment (TS), and technical plus sentiment plus blockchain (TSB).
- In normal markets, LSTM-T has the lowest reported numerical loss, but TGARCH and Hybrid_GARCH_T are not statistically distinguishable from the selected benchmark. Adding sentiment and blockchain variables worsens the standalone LSTM result in the normal regime.
- Crisis-period winners differ: Hybrid_TGARCH_TS for COVID-19, Hybrid_EGARCH_TSB for the China mining ban, and Hybrid_APARCH_TS for the crypto winter. The article cautions against universal model rankings from pooled data.

**Limitations and interpretation:** daily conditional-volatility results do not establish hourly spot-price predictability. The balanced sample ends in July 2025 despite a merged source table extending into February 2026; the feature intersection therefore limits recency. The sentiment and blockchain sources are heterogeneous, and their point-in-time publication/availability timestamps and redistribution rights need independent checks. This is a research-backed volatility challenger, not an external score comparable to our BTC/USDT hourly-path nMAE.

**Hypothesis:** a regime-conditioned volatility layer may be useful as a separate risk/interval challenger. It should first be compared with HAR/RV and simple GARCH/TGARCH on a frozen, point-in-time 5m-to-hourly realized-volatility target. Do not integrate it into the point-price ensemble until a separate ablation shows incremental out-of-sample value and intervals are calibrated.


## 2026-11-25 — original-source review and evaluation-pipeline audit

### Research findings (facts, with scope limits)

1. **Foundation models forecast realised variance better at short hourly horizons than at 24h; calendar adjustment is essential.** Tommaso Zeri, “Time Series Foundation Models and the Realized Volatility of Bitcoin and Ether” (research note published 2026-11-01; not peer-reviewed), [paper](https://tommasozeri.github.io/research/foundation-models-crypto-realized-volatility/) and [replication repository](https://github.com/tommasozeri/Crypto-Time-Series-Foundation-Models/tree/c6fcb9d2cde2c73a797d08d28a630ba55e110572). The reproducible design uses Binance Spot BTC/ETH 5m returns, hourly realised variance from 12 returns, horizons 1h/4h/24h, 4,866 hourly origins per asset spaced every five hours, a two-year rolling HAR/log-HAR benchmark, calendar adjustment, QLIKE, DM-HLN, Benjamini–Hochberg FDR control and a 90% model confidence set. The note reports that hourly calendar adjustment improves the HAR benchmark by 8–25%; zero-shot foundation models alone beat adjusted HAR by 8–13% at 1h BTC but lose 10–24% at 24h; equal-weight combinations with log-HAR improve QLIKE by 3–8% at 1h/4h, while the 24h gain is small and not significant. TimesFM-3 + log-HAR remains in the 90% confidence set across the six hourly asset/horizon cases. A placebo test shows Chronos-2's apparent covariate gain is not specific to DVOL. The author flags potential pretraining overlap; post-release subsamples are only a partial check. This is **realised-volatility** evidence, not a BTC price-level path and not directly comparable to the tournament's hourly log-price MAE. No code, weights or data were copied.

2. **Fractional attention does not guarantee better BTC forecasts.** Sukono et al., “Unlocking Multifractal and Long-Memory Dynamics in Cryptocurrency Markets: A Fractional Attention-Driven LSTM–N-BEATS Framework for Optimal Investment Under Dynamic Risk,” *Fractal and Fractional* 10(6), 379 (2026-05-31), [DOI](https://doi.org/10.3390/fractalfract10060379). The paper reports daily BTC/ETH/BNB data (2018–2025), MF-DFA spectrum widths about 0.51–0.54 and a learned Grünwald–Letnikov fractional parameter near 0.6106 (a model parameter, not the MF-DFA Hölder exponent). Four quarterly rolling validation folds show BTC RMSE 0.02370 for FA-LSTM-NBEATS versus 0.02273 for Std-LSTM; ETH is slightly better (0.03835 vs 0.03889), while BNB is worse (0.03092 vs 0.02762). The best BTC directional hit rate reported is 53.5% with p=0.0856, not significant at 5%. The paper reports a significant DM difference for BTC, but the tabled RMSE is worse for the fractional architecture; this is not evidence of a universal fractional edge. Data beyond the article are available by author inquiry; no runnable public implementation was identified. Daily targets do not match hourly BTC forecasting.

3. **Fear/Greed regime flags have asset-specific and weak effects, not a stable direction signal.** Gjeçi, Kufo, Troplini, Tori & Hoxha, “Modelling Asymmetric Volatility and Sentiment Effects: Forecasting Accuracy in the Crypto Market,” *Journal of Risk and Financial Management* 19(6), 390 (2026-05-28), [DOI](https://doi.org/10.3390/jrfm19060390). The study uses 2,650 daily observations from 2018–2025 for seven assets, Yahoo Finance closes and the Alternative.me Crypto Fear & Greed Index; the split is chronological 70/30. EGARCH/GJR-GARCH models use normal or Student-t innovations and a lagged CFGI high-greed dummy (>80th percentile). CFGI coefficients are statistically insignificant in most volatility equations; out-of-sample winners vary by asset. BTC's lowest reported QLIKE is 2.7660 for GJR-GARCH Student-t + CFGI versus 2.7663 without CFGI, while BTC directional-volatility hit rates remain around 0.49–0.51. This is conditional-volatility evidence, not a price-direction or hourly forecast. The article's CC BY 4.0 license does not license Yahoo/Alternative.me data.

4. **High-frequency LOB evidence remains a separate target class.** Raffaelli et al. (2026-04-17), [DOI](https://doi.org/10.1007/s10203-026-00570-z), and [Learning2Control/MultivariateHawkesLOB](https://github.com/Learning2Control/MultivariateHawkesLOB/tree/ecee1b7af5013e44b9ab584e93cd592aefa69fbd) were rechecked. The repository's current main HEAD is ecee1b7af5013e44b9ab584e93cd592aefa69fbd and its LICENSE is GPL-3.0. The paper predicts next-event timing/sign from Bitfinex LOB streams; it is not a 24h hourly price-path benchmark. No GPL code or LOB data were copied.

5. A newly indexed 2026 MF-DFA paper by B. I. Unal was found only through an aggregator record; an original publisher/DOI record could not be independently located in this pass. Its reported claims are therefore **not admitted as verified evidence**.

### Methodological implications

- Add calendar-adjusted HAR/log-HAR realised-volatility as a separate volatility challenger once at least ~170 days of clean 5m history are available. Do not substitute a volatility target for the point-price tournament.
- Keep fractional/multifractal features behind preregistered ablations; compare against standard LSTM/ARIMA/HAR and heavy-tail surrogates. A nonzero spectrum width or learned fractional parameter does not establish tradable predictability.
- Keep sentiment polarity, attention, CFGI regime, and macro-news surprise as separate channels. Current pipeline has no point-in-time licensed sentiment/news source; no feature was added.
- The current 999-candle input history is only about 83h15m, far too short for the 90-day/170-day volatility and multifractal comparisons.

### Evaluation-pipeline integrity finding and patch

The 2026-11-25 evaluation artifact reported one completed unique vintage even though its manifest contained 16 prior evaluated records plus the newly evaluated Nov 23 vintage. Root cause: archived evaluation records are named `lfm5m-<vintage>.json`, while `summarize_leaderboard()` searched only `evaluation_*.json`; archived records were silently omitted from the aggregate. The scanner is changed to inspect all JSON files and retain only records matching the frozen schema/protocol/asset/horizon. A regression test uses the canonical archived filename and verifies that manifests/raw hourly arrays are ignored.

A second race was found: the archiver waited for the evaluation workflow only on daily-marker pushes, not on evaluator-code/test/workflow pushes that also trigger evaluation. The wait-path set now includes `evaluate_vintages.py`, `test_evaluate_vintages.py`, and `.github/workflows/lfm-evaluate.yml`; a regression test verifies those paths. This ensures the sibling evaluator run can finish before its artifact is archived. No forecast equation, model weights, data or external dependency changed.

### Provenance

- Research checked: 2026-11-25.
- No third-party code, weights, datasets, cached model outputs or API payloads copied.
- No dependency changes. Public model/paper results are not treated as live out-of-sample tournament submissions.
- The daily Binance Spot BTCUSDT 5m feed remains a challenger input; no BTC/USD champion was promoted.


### 2026-11-25 execution and evaluation results

- Daily forecast workflow [45572000476](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000476) completed successfully; 15 forecast unit tests passed, live Binance Spot BTCUSDT 5m retrieval passed, 24 hourly target points were generated, and artifact 15002426841 uploaded.
- Daily archive workflow [45572000351](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000351) completed successfully and archived the exact forecast ZIP/JSON/raw input snapshot.
- The first evaluation workflow [45572000340](https://github.com/messerzai/ambivikhry-agent/actions/runs/45572000340) ran before the Nov 24 vintage's final close and correctly left that vintage pending; it evaluated the Nov 23 vintage only.
- The leaderboard filename regression and archiver wait-path fixes were committed in [4852b85010fb32241fc0315a00943690c6a9572a](https://github.com/messerzai/ambivikhry-agent/commit/4852b85010fb32241fc0315a00943690c6a9572a). Evaluation workflow [45574156649](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156649) passed 17 tests, evaluated the Nov 24 vintage after its final close, and uploaded artifact 15003478221. Archive workflow [45574156692](https://github.com/messerzai/ambivikhry-agent/actions/runs/45574156692) passed 19 tests and archived that exact evaluation artifact; its log confirms no errors and a successful branch commit.
- The corrected leaderboard scanner now finds archived `lfm5m-*.json` records as well as fresh `evaluation_*.json` files. The evaluation artifact's manifest contains 18 completed unique vintages, 11 non-overlapping selected vintages, seven overlaps excluded, one pending Nov 25 vintage, and zero failures. The leaderboard has 0 calibrated vintages and 0 virtual points.
- Nov 24 evaluation actual-data SHA-256: `b088ae8c79aeca4426c2e6f3d5977221a3461c93a0d54fcc02e8e9cd6332be5c`; evaluation JSON SHA-256: `19db9b30dd46a335fcda17d431af5f665b7b3ee4bbadb67fc5db2b06979ce19e`; exact evaluation ZIP SHA-256: `8adc1e6639a54e2bb4f76693a33122b68af7288fde6a421edb64b21ee92d7bb8`.


## Supplementary original-source audit — 2026-11-25 (run 14)

### Kim, Lee & Choi (2026): rolling MF-DFA across fiat markets

Publisher full text checked 2026-11-25: Do-Hyeon Kim, Jun-Hyeok Lee and Sun-Yong Choi, “Comparative Analysis of Cryptocurrency Market Efficiency and Local Features Using MF-DFA and DCC-GARCH,” *Fractal and Fractional* 10(6), 353 (23 May 2026), DOI https://doi.org/10.3390/fractalfract10060353.

The study uses daily closes/returns for BTC, ETH, XRP and BCH across 11 KRW/USD/JPY pairs from 2018-01-01 to 2025-09-30. MF-DFA uses q in [-10, 10], quadratic detrending (m=2), 20 logarithmic scales, and a 250-observation rolling window; window-size checks use 200 and 300 observations. For W=250, the stated scale range is 10–62 observations. The authors report time-varying spectrum widths and heterogeneous DCC correlations between local-market efficiency proxies; same-asset cross-fiat return correlations are much higher than cross-asset efficiency correlations.

**Important methods qualification:** §4.1.2 describes 99 surrogates made by randomizing Fourier phases while preserving the Fourier amplitude spectrum, then says this also preserves the original heavy-tailed distribution. Plain phase randomization guarantees the spectrum, but does not by itself preserve the exact empirical amplitude distribution. IAAFT was developed to preserve the amplitude distribution and approximate the power spectrum jointly (Venema, Ament & Simmer, 2006, https://doi.org/10.5194/npg-13-321-2006). Unless an additional rank-remapping step was used but omitted from the description, the paper's attribution of multifractality to long-range dependence rather than heavy tails is not fully identified by the described surrogate. This does **not** invalidate the reported rolling estimates; it narrows the source-decomposition claim. Our replication should compare shuffled, phase-randomized and IAAFT surrogates and report both marginal-distribution and spectrum discrepancies.

Other limitations: daily rather than hourly/5m sampling; data available from the corresponding author on request; a four-day BCH/USD gap was forward-filled; exchange-specific local daily closes can encode non-synchronous information sets; DCC is co-movement, not causal transmission; no BTC hourly point-price forecast was tested. The article's publisher page states open access under a Creative Commons CC BY license; exact version should be verified before adapting article material. No article text, figure, code or data was copied.

### Gür & Ünal (2026): news sentiment and asymmetric BTC response

Publisher abstract checked 2026-11-25: Yunus Emre Gür and Emre Ünal, “The Impact of News Sentiment on the Bitcoin Price via Machine Learning and Deep Learning-Based NLP Models,” *Journal of Forecasting* 45(3), 895–923, DOI https://doi.org/10.1002/for.70068 (first published online 20 Nov 2025; issue 2026).

The abstract reports FinBERT scores and semantic features from more than 650,000 financial-news headlines combined with lagged BTC variables, news indicators and macro/financial factors; the FinBERT-LSTM hybrid is reported as the best prediction model, with stronger response to negative than positive/neutral news. Data are available from the corresponding author on reasonable request. The accessible publisher record does not expose the full methods/results or a public code/data release, so the exact forecast horizon, split design, leakage controls and magnitude of OOS improvement could not be independently checked. Treat this as a paper-only candidate, not a verified 24h hourly benchmark. Wiley's page states all rights reserved; no permissive article license was identified. No text, code, headlines or sentiment outputs were copied.

### Cross-study synthesis

The news/sentiment evidence is heterogeneous rather than convergent: Gür & Ünal report an asymmetric news-sentiment association with BTC price modelling; Akbar (2026, https://doi.org/10.1108/SEF-12-2025-0942) reports no return-predictive power for polarity/hype/anxiety but an association between attention and conditional variance, with attention reacting to price shocks. Differences in source, account filtering, frequency, target and validation design may explain the contrast. Do not collapse polarity, attention, news surprise and uncertainty into one feature. Any future implementation must be point-in-time, licensed, timestamp-audited and tested as separate ablations.

### Surrogate-method reference

Venema, V., Ament, F. & Simmer, C. (2006), “A Stochastic Iterative Amplitude Adjusted Fourier Transform algorithm with improved accuracy,” *Nonlinear Processes in Geophysics* 13, 321–328, DOI https://doi.org/10.5194/npg-13-321-2006. The paper describes IAAFT/SIAAFT as preserving the empirical amplitude distribution while matching the power spectrum more closely than simple phase randomization. This is a methods reference only; no code or article content was copied.
