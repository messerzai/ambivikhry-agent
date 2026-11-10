# Crypto Irregular-Fractal Research

**Branch:** `research/crypto-irregular-fractals`  
**Status:** Research proposal / hypothesis under test  
**Module:** Ambivikhry Research Lab  
**Working title:** Crypto Markets as Adaptive, Irregular Multifractal Systems

## 1. Research question

Do cryptocurrency price and volatility series exhibit time-varying, non-self-similar (multifractal) structure, and how does that structure co-vary with collective investor sentiment and information events?

The motivating intuition is that market patterns do not repeat as exact copies. Each episode is historically unique, yet may share statistical structure across time scales. News, social attention, fear, greed, uncertainty, liquidity and participant interaction may contribute to changes in that structure.

This is a hypothesis, not an established causal explanation. The project must be able to reject it.

## 2. Terminology: avoid a false premise

“Wrong fractal” is an evocative working metaphor, not a standard mathematical category. The research should distinguish:

- **Self-similarity / scale invariance:** statistical structure remains similar under changes of scale; it does not require the same price path to repeat.
- **Multifractality:** different fluctuation magnitudes or regions have different scaling exponents.
- **Non-stationarity and regime shifts:** statistical properties change over time.
- **Path uniqueness:** exact price trajectories do not repeat; this alone does not establish fractality.
- **Deterministic chaos vs stochastic complexity:** do not infer chaos from visual irregularity.

Preferred working term: **adaptive irregular multifractal market dynamics**.

## 3. Core hypotheses

- **H1 — Time-varying scaling:** multifractal and memory measures vary across rolling windows and market regimes.
- **H2 — Sentiment association:** measured public sentiment and attention co-vary with returns, volatility, liquidity and scaling measures.
- **H3 — News-conditioned response:** market response differs by event type, surprise, source, reach and prevailing sentiment.
- **H4 — Asymmetry:** downside shocks, panic and negative news may have different temporal signatures from upside moves and positive news.
- **H5 — Conditional interaction:** sentiment may amplify or dampen the response to news; effects may depend on liquidity, leverage and market regime.
- **H6 — Limited predictability:** any apparent signal must survive strict out-of-sample tests, transaction costs and comparisons with simple baselines.

## 4. Research layers

### A. Market geometry
Collect synchronized OHLCV, trades and (where available) order-book depth, funding, open interest, liquidations and on-chain activity. Derive log returns, realized volatility, drawdowns, volume/imbalance and liquidity measures.

### B. Multiscale structure
Evaluate:
- MF-DFA and generalized Hurst exponents;
- multifractal spectrum width and asymmetry;
- DCCA / MF-DCCA for cross-correlations;
- volatility clustering and long-memory diagnostics;
- entropy, recurrence and time-irreversibility measures;
- visibility graphs as an optional structural representation.

Use multiple time scales (for example 1m/5m/1h/1d) and rolling windows. Report sensitivity to sampling clock, exchange, quote currency and window length.

### C. Human sentiment and attention
Use timestamped, legally accessible and documented sources: social posts or aggregate sentiment indices, search/attention indicators, surveys where available, and carefully labeled text corpora. Separate sentiment polarity, emotional intensity, uncertainty, disagreement, volume of attention and bot-like activity. Never equate post volume with emotion.

### D. News and events
Build an event ledger with publication time, source, topic, novelty/surprise where measurable, geographic/economic relevance and confidence. Distinguish scheduled macro releases, regulation, exchange/security incidents, protocol events, influential statements and market rumors. Prevent look-ahead leakage: use only information available at the prediction timestamp.

### E. Coupled system
Test lagged and nonlinear relationships among sentiment, news, liquidity, volatility and multifractal measures. Compare contemporaneous association with lead/lag effects. Use event studies, rolling correlations, DCC-style models, nonlinear models and causal designs only when their assumptions are defensible.

## 5. Falsification and controls

A result is not evidence of genuine multifractality merely because a spectrum looks broad.

Required controls:
- shuffled surrogates;
- phase-randomized surrogates;
- IAAFT surrogates preserving the amplitude distribution and linear structure;
- heavy-tail / distributional controls and finite-sample confidence bands;
- multiple-testing correction;
- robustness across assets, venues, sampling intervals and regimes;
- placebo event timestamps and unrelated-news controls;
- out-of-sample and walk-forward validation.

Explicitly test whether apparent structure is an artifact of heavy tails, volatility clustering, exchange fragmentation, missing data, sampling choices or a few extreme events.

## 6. Initial study design

**Phase 0 — Literature and reproducibility.** Reproduce published crypto multifractal results before proposing a new measure.

**Phase 1 — Baseline panel.** Start with BTC and ETH; add other liquid assets only after data quality checks. Use at least two independent venues where feasible.

**Phase 2 — Event and sentiment alignment.** Build a timestamped, versioned dataset. Record source provenance, time zones, missingness and revisions.

**Phase 3 — Statistical tests.** Estimate rolling scaling measures and test their association with sentiment/news under surrogate, placebo and multiple-testing controls.

**Phase 4 — Prospective validation.** Freeze hypotheses and thresholds, then evaluate on unseen periods. Compare with naive baselines and report calibration, false positives and economic utility after realistic costs.

**Phase 5 — Replication.** Publish code, data lineage, configuration and negative results where licensing permits.

## 7. Evaluation criteria

A claim is supported only if it is:
1. statistically distinguishable from appropriate null models;
2. robust to reasonable preprocessing and sampling choices;
3. replicated across more than one asset or period, or explicitly scoped to one;
4. not explained by known confounds;
5. prospectively validated if predictive language is used.

Correlation is not causation. A news/sentiment association does not prove that collective emotion caused a price move. The market can also shape sentiment, and both can respond to a third event.

## 8. Safety, ethics and financial boundaries

- This is a research and measurement module, not an autonomous trading agent.
- No exchange keys, wallet permissions, order execution or financial transactions are part of this branch.
- Do not present exploratory correlations as investment advice or guaranteed signals.
- Respect platform terms, privacy, copyright and applicable data protection rules.
- Store only necessary data; prefer aggregate or public data and document provenance.
- Any future trading experiment requires a separate specification, explicit approval, paper trading, risk limits and independent review.

## 9. First deliverables

1. A literature map with confirmed findings, open questions and competing explanations.
2. A reproducible BTC/ETH data pipeline with quality checks.
3. A notebook comparing MF-DFA results against shuffled, phase-randomized and IAAFT nulls.
4. A timestamped news/sentiment event schema.
5. A preregistered analysis plan and baseline report, including null/negative findings.

## 10. Initial literature anchors

- Drożdż et al., *Multifractality and its sources in the digital currency market* (2025 preprint): https://arxiv.org/abs/2510.13785
- *Examining the Fractal Market Hypothesis Considering Daily and High Frequency for Cryptocurrency Assets* (2022): https://doi.org/10.1142/S0218348X22500700
- *Hourly Asymmetric Multifractality and Dynamic Efficiency in Cryptocurrency Markets* (2025): https://doi.org/10.1111/1467-8454.12390
- Huynh, *Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets* (2026): https://doi.org/10.1016/j.jbef.2026.101183
- *Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity* (2026 perspective): https://doi.org/10.3389/fphy.2026.2026031

These references motivate methods and questions; they do not validate every hypothesis above.

---
**Ambivikhry principle:** observe → hypothesize → test against nulls → attempt to falsify → replicate → only then update the model.
