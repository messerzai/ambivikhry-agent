# Sentiment, attention and news-surprise ablation protocol

**Status:** pre-registered research design; no feature is enabled in a forecast model.  
**Created:** 2026-11-14  
**Branch:** `research/living-fractal-market`

## Research question

Do point-in-time social attention, sentiment, network contagion or news-surprise features improve the 24-hour hourly BTC/USDT price path beyond zero-return, volatility-aware and intraday-seasonal controls? Do they add more information about volatility/risk than about return direction?

The behavioral literature does not support treating every sentiment score as a directional signal. In particular, peer sentiment, aggregate contagion, attention intensity and macro-news surprise are different variables and must remain separate.

## Evidence and testable hypotheses

1. **Attention vs polarity.** Akbar (2026) reports in the publisher abstract that tweet polarity/hype/anxiety do not predict BTC returns, while public attention improves GARCH-X variance modelling and reacts to price shocks. Hypothesis: attention count/engagement may improve volatility forecasts, not necessarily point-price forecasts.
2. **Social contagion.** Han, Liu & Sui (Dallas Fed WP 2605, 2026) distinguish peer sentiment from aggregate contagion intensity. Hypothesis: a network-contagion intensity measure may help forecast volatility/volume/tail risk; peer polarity alone should not be assumed to predict hourly price direction.
3. **News × sentiment.** Huynh (JBEF, 2026) reports that daily bullish sentiment moderates 5-minute reactions to scheduled macroeconomic surprises in a multi-asset sample. Hypothesis: sentiment may change the magnitude of response to a surprise rather than supply a standalone directional signal.
4. **Regime-aware fusion.** Haroon's 2026 preprint reports only modest 3h AUC (0.5084) and below-chance 6h AUC (0.4902), with an unresolved full-sample-vs-training volatility-threshold description. Hypothesis: regime-conditioned interaction is worth testing, but the preprint is not evidence of reliable forecast skill.
5. **Event clock.** Shynkevich (2026) reports periodic subsecond trading bursts that increase volatility/costs without significant adverse price impact. Hypothesis: event-time/clock-phase controls may improve volatility modelling; periodicity alone is not directional alpha.

## Feature families (keep separate)

- **Attention:** message/post count, unique active authors, engagement count, search intensity. Avoid raw bot-amplified volume as a polarity proxy.
- **Polarity:** bullish, bearish, neutral and disagreement/dispersion measures. Preserve classifier version and confidence.
- **Contagion:** reply/network diffusion, peer exposure and fraction of users shifting in the same direction as peers. Only test if lawful, timestamped graph data and an auditable construction are available.
- **Macro surprise:** actual release minus consensus, normalized using only trailing training-window statistics; record release time and first-available timestamp.
- **Crypto-news surprise:** novelty and sentiment relative to prior coverage, with immutable article ID, publisher time, first-seen time and revision history.
- **Interactions:** surprise × prior sentiment, surprise × volatility regime, attention × volatility regime. Do not replace main effects with interactions without reporting both.

## Point-in-time data contract

For every observation preserve:
- event time (when the event happened);
- publication time (when the publisher released it);
- first-seen/ingestion time (when the research system could first observe it);
- retrieval time and source revision/hash;
- asset, venue, language, feature-model version and timezone.

A feature is eligible at forecast cutoff only if its first-available timestamp is at or before that cutoff. Do not backfill later-edited articles, future Reddit comments, revised macro consensus, final daily sentiment or future social graph edges into earlier hourly rows. If a sentiment source is daily, use only a fully completed day or a genuinely point-in-time partial-day stream. Never use the final daily aggregate before that day has closed.

Respect platform terms, privacy requirements and dataset licenses. Do not scrape private messages, infer identities, or copy full copyrighted article text. Store only the minimum feature data and source provenance needed for reproducibility.

## Baselines and ablations

1. RandomWalkLastPrice / zero-return.
2. VolatilityCappedSlowDrift (existing frozen tournament baseline).
3. Intraday seasonal-naive (hour-of-week/phase; from the separate seasonality protocol).
4. Price-only challenger.
5. Price + attention.
6. Price + polarity.
7. Price + attention + polarity.
8. Price + macro-news surprise.
9. Price + surprise × prior sentiment.
10. Price + social-contagion intensity, only if the graph data is available and licensed.

Run nested ablations; do not add every feature family at once. Compare price-only, volatility-only and seasonal controls before adding any behavioral signal.

## Validation

- Use expanding/rolling chronological walk-forward with non-overlapping daily 24h origins for the primary leaderboard.
- Purge overlapping target windows for intraday-origin secondary experiments.
- Fit sentiment thresholds, normalization, topic models, regime boundaries and feature selection on training data only.
- Align every feature to first-available time, not retrospective event time alone.
- Primary metric remains normalized MAE of hourly log-price forecasts under `FORECASTING_TOURNAMENT.md`.
- Secondary metrics: interval/quantile score and coverage (only if calibrated), directional accuracy, volatility QLIKE, and Brier score for a separately defined binary event.
- Use paired block bootstrap/Diebold-Mariano-style comparisons with dependence-robust variance; correct for multiple feature families and horizons.
- Report missingness, source outages, language coverage, bot-classification error, effective sample size and event-window overlap.

## Falsification and promotion

A feature family remains diagnostic unless it improves primary out-of-sample price-path loss over both random walk and the strongest simple baseline, with uncertainty intervals and no leakage. A volatility improvement alone should be reported as a volatility result, not a price-forecast win. A directional F1 increase without better AUC/calibration or point-price loss is insufficient. No feature is promoted to the champion before 30 completed non-overlapping daily vintages and the existing tournament requirements.

## Source notes (checked 2026-11-14)

- Han, Liu & Sui, Dallas Fed WP 2605: https://www.dallasfed.org/research/papers/2026/wp2605 (preliminary working paper; Bitcointalk 2012–2022, CoinAPI/RavenPack/Google data).
- Huynh, JBEF 101183 (2026): https://doi.org/10.1016/j.jbef.2026.101183 (publisher abstract; 5m multi-asset sample 2014–2021, daily TRMI).
- Akbar, Studies in Economics and Finance (2026): https://doi.org/10.1108/SEF-12-2025-0942 (publisher abstract only; >16m tweets).
- Haroon, arXiv:2607.23370: https://arxiv.org/abs/2607.23370 (preprint; 3h/6h classification, modest/below-chance AUC, regime-threshold inconsistency).
- Shynkevich, Journal of Futures Markets (2026): https://doi.org/10.1002/fut.70089 (published abstract; subsecond BTC/ETH Spot and perpetual periodicity).

No feature was enabled and no third-party code, weights or data were copied in this protocol.
