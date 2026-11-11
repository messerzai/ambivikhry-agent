# Research log — 2026-11-11

Branch: research/living-fractal-market  
Starting HEAD: 6e64ff793c9c4889ab40d0def0fdf117f44eeab9  
Scope: research branch only; main was not modified.

## Research discoveries

### 1. Non-stationary multifractality is a testable state variable, not a permanent market law

Cho et al., “Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity,” Frontiers in Physics (Perspective, published 2026-10-29), DOI 10.3389/fphy.2026.2026031. The article argues that scaling exponents and complexity measures depend on regime, venue and sampling conventions. It explicitly recommends matched surrogate tests, finite-size confidence bands, rolling windows, multiple clocks, and prospective crash-warning evaluation. It warns that finite samples, heavy tails, scaling crossovers and estimator bias can produce spurious multifractality. This directly supports treating the fractal layer as a measured hypothesis and using IAAFT, shuffled and phase-randomized nulls—not as a narrative assumption.

Source: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.2026031/full

Drożdż et al., “Multifractality and Its Sources in the Digital Currency Market,” Future Internet 17(10), 470 (2025), DOI 10.3390/fi17100470. The paper applies MFCCA/MF-DFA and a method intended to disentangle temporal correlations from distributional effects. The authors describe the interaction of long-range dependence and heavy tails and explicitly identify direct risk-management implications as future work. This is descriptive/diagnostic evidence, not evidence that multifractal features improve BTC forecasts.

Source: https://www.mdpi.com/1999-5903/17/10/470

Choi, “Intrinsic multifractality and adaptive efficiency in Bitcoin: Disentangling sources of scaling complexity across market regimes,” Physica A 697 (2026), 131735, DOI 10.1016/j.physa.2026.131735. The bibliographic record and abstract-level summaries report approximately 774,000 five-minute BTC observations (Aug-2017 to Dec-2024), q-Gaussian rescaling, and a scaling crossover near 25 days. The Frontiers Perspective cites this result. The publisher full text was not accessible in this review, so treat the detailed result as an abstract-level replication lead, not independently reanalysed evidence.

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

Choi, “Testing detailed balance in daily cryptocurrency markets: irreversibility in range–volume dynamics, and none detectable in candlestick shape,” Frontiers in Physics (2026). In 22 USDT pairs from one venue, the abstract reports no detected first-order detailed-balance violation in candlestick shape, but range–volume dynamics reject detailed balance in 12 of 17 held-out assets under the stated design. This is a useful counterexample to blanket “non-repeating” claims: irreversibility depends on the state representation, sample size and test. Daily bars and one venue limit direct application to 5-minute forecasts.

Source: https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.1977979/abstract

## Competitor and public-forecast findings

- Chronos-2: official HF model card lists Apache-2.0 and describes a 120M zero-shot model with univariate, multivariate, covariate-aware and quantile forecasts. The card's general FEV-Bench/GIFT-Eval claims are not BTC-specific evidence.
- TimesFM 2.5: official HF card lists Apache-2.0 for the 200M checkpoint.
- TimesFM 3.0: official HF card lists a distinct timesfm-non-commercial-license-v1.0 for weights, while the source repository is Apache-2.0. Do not treat the source license as a weight license.
- NeuralForecast provides N-BEATS, N-HiTS, TFT and PatchTST implementations under Apache-2.0 code terms; no pretrained crypto checkpoint is implied.
- Benchstreet is MIT, but its own README says it is not an objective benchmark and describes S&P 500 daily data, not BTC hourly data.
- CryptoOracle is the closest public +24h hourly forecast ledger located. Its published 2026-09-17 exploratory snapshot reports TimesFM 2.5 BTC +24h mean absolute log-return error ×100 of 1.712 versus 1.627 for last price, with 77.3% coverage for a nominal 80% interval. This is a historical backtest, not a current live score; overlapping hourly forecasts are not independent.
- BitPredict offers timestamped human UP/DOWN 24h receipts, not point-price forecasts. AI Predicts Bitcoin forecasts 7d to 360d daily, not hourly. Neither was entered or ranked.
- CrunchDAO Synth has public 1h/24h probabilistic rules and CRPS scoring, but participation conditions and external-account/reward obligations were not established as compatible with this project's constraints. No submission was made.

## Data and code audit

- Research branch HEAD at start of run: 6e64ff793c9c4889ab40d0def0fdf117f44eeab9.
- The 5-minute prototype already reads public Binance Spot BTCUSDT klines without an API key and emits seven models, including DownsideStress5m. QUICKSTART incorrectly documented six and omitted DownsideStress5m.
- The 5-minute parser checked continuity between received rows and allowed a 15-minute age. It could accept a missing most-recent closed candle because the test fixture itself omitted the immediately preceding closed bar. A stricter latest-expected-candle check and a regression test are added in this run.
- The workflow file contained schedule and workflow_dispatch, but GitHub requires those triggers' workflow file to exist on the default branch. Because this branch must remain isolated and main must not change, those triggers are removed; the branch workflow remains push-triggered. The daily research automation is separate.
- Binance's official REST documentation confirms that public market-data-only requests should use data-api.binance.vision and that kline timestamps are milliseconds: https://developers.binance.com/en/docs/products/spot/rest-api. The prototype endpoint is public and requires no API key. Public search snippets returned 5-minute candles stamped 2026-11-11 13:10 while the run's UTC time was 07:04. Those rows are future-dated relative to the run and rejected. A Coinbase public candle endpoint returned a raw JSON page that the browser could not expose as rows. No 300+ bar, timestamp-consistent live series was available for a valid forecast.
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
