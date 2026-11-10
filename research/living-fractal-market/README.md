# Living Fractal Market — Research Branch

**Branch:** `research/living-fractal-market`  
**Status:** exploratory research programme; hypotheses are not established facts.  
**Purpose:** investigate whether cryptocurrency price dynamics behave as a non-stationary, adaptive, non-repeating multifractal system whose statistical structure co-evolves with collective attention, investor sentiment, news, liquidity and market microstructure.

## 1. Core research question

Do crypto-asset price and volatility series exhibit time-varying multifractal structure that is not simply a repeated geometric pattern, and can measurable changes in that structure be associated with (or, more cautiously, help explain) changes in collective attention, sentiment, news and market conditions?

The phrase **“non-repeating / living fractal”** is an intuitive working metaphor, not a formal mathematical classification. The project must translate it into measurable hypotheses. A financial time series can be multifractal without being a literal geometric fractal, and apparent multifractality can arise from finite samples, heavy-tailed distributions, non-stationarity, volatility clustering or sampling choices.

## 2. Hypotheses to test (not assume)

- **H1 — Time-varying scaling:** generalized Hurst exponents and multifractal spectra change across rolling windows and market regimes.
- **H2 — Non-repetition:** local price/volatility configurations are not exact recurrences; quantify recurrence and similarity rather than relying on visual impressions.
- **H3 — Behavioral association:** attention and sentiment measures (fear, greed, optimism, panic, uncertainty) have measurable, possibly asymmetric and time-dependent relationships with returns, volatility, volume and multifractal parameters.
- **H4 — News response:** scheduled announcements and unexpected news are associated with changes in volatility, trading activity and scaling structure; response depends on topic, surprise, source and pre-event sentiment.
- **H5 — Cross-asset emotional transmission:** sentiment/news shocks may propagate between assets, with BTC potentially acting as a transmitter; test rather than assume direction.
- **H6 — Incremental information:** fractal and behavioral features add robust out-of-sample explanatory or forecasting value beyond standard baselines. No trading value is claimed without realistic costs and risk controls.

## 3. Research design

### A. Data
Collect synchronized, timestamped data with provenance and licensing recorded:
- OHLCV and trades from multiple exchanges; retain exchange-level data where possible.
- Order-book depth, spread, imbalance, liquidations, open interest and funding rates where available.
- News headlines/articles with publication time, source, topic, event category and deduplicated text.
- Public sentiment/attention proxies: Google Trends, public social-media aggregates where permitted, Crypto Fear & Greed (as one imperfect proxy, not ground truth).
- Macro announcements and surprise values, regulatory announcements, security incidents and major protocol events.
- Market-wide controls: BTC returns, equity/FX/rates proxies, stablecoin flows and broad risk indicators where available.

Store raw data immutably; normalize time to UTC; document missingness, exchange outages, survivorship and venue coverage. Avoid collecting private personal data.

### B. Fractal / complexity measurements
- MF-DFA on log returns, absolute returns and realized volatility; estimate generalized Hurst exponent h(q), mass exponent and singularity spectrum width/asymmetry.
- MF-DCCA / MFCCA for cross-correlations between market series and attention/sentiment/news-intensity series.
- Compare calendar-time bars with activity/volume-based (intrinsic) time.
- Rolling windows and multiple horizons; report uncertainty bands and sensitivity to q-range, detrending order, window length and sampling frequency.
- Complement with recurrence plots/recurrence quantification, entropy, change-point detection and volatility-clustering diagnostics.

### C. Null models and falsification
Separate genuine temporal multifractality from artifacts:
- shuffled surrogates to destroy temporal ordering;
- phase-randomized / IAAFT surrogates to preserve selected distributional or linear properties;
- heavy-tail and volatility-clustering controls;
- matched synthetic series and finite-sample simulations;
- alternative exchanges, assets, time zones, frequencies and window lengths.

A result is not evidence of a special “living fractal” if it disappears under reasonable robustness checks or can be reproduced by a simpler null model.

### D. Emotion, attention and news
Build transparent, timestamp-aware features:
- sentiment polarity and intensity, uncertainty, fear, greed, surprise and topic;
- volume of attention (searches/posts/news), source diversity and disagreement;
- event windows before/after news, with leakage-safe timestamps;
- lagged and lead-lag relationships, nonlinear/asymmetric responses and regime interactions.

Sentiment models must be validated on manually reviewed samples in relevant languages. Do not equate social-media sentiment with the emotions of all market participants.

## 4. Analysis and validation

1. Start with BTC and ETH, then expand to a pre-defined asset panel to avoid cherry-picking.
2. Use exploratory plots only for discovery; pre-register primary metrics and tests before confirmatory analysis.
3. Estimate rolling MF-DFA/MFCCA features and compare them with attention/news/sentiment measures.
4. Use event studies and time-series models with controls, robust errors and multiple-testing correction.
5. Distinguish correlation, temporal precedence, causal identification and prediction. News and price can influence each other; sentiment may be both cause and consequence.
6. Evaluate forecasting only with walk-forward / expanding-window tests, untouched holdout periods, leakage prevention, realistic fees, slippage and liquidity constraints.
7. Compare against simple baselines: random walk, historical volatility, GARCH-family models and standard momentum/mean-reversion features.
8. Report failed hypotheses, null results and uncertainty alongside positive findings.

## 5. Initial milestones

- **M0 — Reproducibility:** select assets, venues, period, sampling frequency and data dictionary.
- **M1 — Baseline fractal map:** estimate rolling multifractal properties and test surrogate robustness.
- **M2 — Behavioral alignment:** align sentiment, attention and news timestamps; estimate lead-lag and event responses.
- **M3 — Cross-market propagation:** test whether shocks and complexity measures propagate across assets.
- **M4 — Predictive test:** evaluate incremental out-of-sample value without presenting it as investment advice.
- **M5 — Research report:** publish methods, code, data limitations, reproducible figures and negative results.

## 6. First deliverable

A reproducible notebook that:
1. downloads or loads BTC/ETH OHLCV with a documented source;
2. calculates log returns and rolling volatility;
3. estimates MF-DFA spectra over rolling windows;
4. runs shuffled and IAAFT surrogate comparisons;
5. plots how the spectrum changes over time;
6. overlays timestamped news/attention/sentiment events;
7. exports a table of estimates, confidence intervals and robustness checks.

## 7. Guardrails

- This is research, not a trading signal, financial advice or a promise of profit.
- Never describe correlation as proof that “emotions move the market.”
- Do not claim the market is literally a fractal or “wrong fractal” before formal definition and testing.
- Preserve reproducibility: version data, code, parameters, seeds and experiment logs.
- Keep the research branch isolated from the production agent until reviewed and approved.

## 8. Starter literature

- Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity (2026): https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2026.2026031/full
- Intrinsic multifractality and adaptive efficiency in Bitcoin (2026): https://doi.org/10.1016/j.physa.2026.131735
- Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets (2026): https://doi.org/10.1016/j.jbef.2026.101183
- Sentiment spillovers from news and social media in cryptocurrency markets (2026): https://doi.org/10.1016/j.intfin.2026.102357
- Multifractality and Its Sources in the Digital Currency Market: https://www.mdpi.com/1999-5903/17/10/470

---
**Research principle:** let the data surprise us. The purpose is not to confirm the metaphor, but to discover which parts survive measurement, controls and attempts to falsify them.
