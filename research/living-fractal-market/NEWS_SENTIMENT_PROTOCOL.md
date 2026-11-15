# Point-in-time News and Sentiment Experiment Protocol

**Reviewed:** 2026-11-15  
**Status:** design only; no news or sentiment feature is enabled in a forecasting model.  
**Scope:** Binance Spot BTCUSDT, five-minute source data, hourly target grid (+1 through +24). BTC/USDT is not silently relabelled BTC/USD.

## 1. Research separation

Keep five information families distinct:

1. **Scheduled macro surprise:** the difference between a released value and the consensus snapshot that existed immediately before release.
2. **Crypto-news surprise / novelty:** whether a new BTC-relevant event or headline differs from the trailing news corpus, independent of its sentiment polarity.
3. **Investor sentiment:** positive / neutral / negative language and topic relevance.
4. **Attention / activity:** post counts, unique contributors, comments, scores and source coverage.
5. **Market response:** returns, volatility, volume, liquidity and order-flow outcomes.

A contemporaneous association is not evidence that a feature predicts future price changes or causes them.

## 2. Point-in-time event contract

Every raw event must retain:

- stable source and event identifiers;
- source URL and source/publisher timestamp;
- observed_at_utc (when the pipeline could actually see it) and ingested_at_utc;
- release/publication time, timezone and any revision timestamp;
- original and revised values where applicable;
- asset/topic mapping, language and confidence;
- raw payload hash and data provenance;
- separate rights/terms status for source text, metadata and derived labels.

For a forecast cutoff t, only records with observed_at_utc <= t may contribute. A late-arriving article or revised macro release must not be backdated into an earlier feature row. Historical feature reconstruction must use archived point-in-time snapshots, not the current corrected API response.

## 3. Scheduled macro surprises

For each scheduled release:

- store the official release timestamp and actual value;
- store a timestamped pre-release consensus snapshot and its source;
- compute the surprise as actual minus pre_release_consensus;
- standardize using only the trailing distribution of past forecast errors for that indicator;
- retain the release category and sign convention;
- never use post-release consensus, revised historical actuals or a consensus value first observed after the release.

Evaluate event windows separately (0–5m, 5–15m, 15–60m, 1–4h and 4–24h). Use official statistical agencies for release values. Consensus feeds may have separate commercial or redistribution terms; no feed is presumed reusable because a value is visible on a website.

## 4. Crypto-news novelty and sentiment

Deduplicate syndicated/repeated headlines before aggregation. Keep separate fields for:

- BTC/entity relevance;
- source reliability and event type;
- novelty relative to a trailing, already-observed news corpus;
- positive / neutral / negative sentiment;
- topic labels and model confidence;
- publication time versus pipeline observation time.

Novelty must be computed against prior documents only. A headline published before the cutoff but ingested after it is unavailable to that vintage. Sentiment must not be used as a proxy for novelty, and attention volume must not be conflated with polarity.

## 5. Reddit / R-RISI-inspired daily sentiment

Wagner and Metzler's R-RISI provides a useful published construction, but its data and model versions must not be silently treated as a ready-made BTC predictor.

A clean-room, point-in-time research implementation may test the following methodological design only after Reddit/data-source terms are reviewed:

- classify posts by sentiment (positive / neutral / negative), topic and BTC relevance;
- retain label confidence and model/version provenance;
- use engagement snapshots available at the forecast cutoff, not final upvotes/comments observed later;
- calculate an engagement weight such as ln(1 + score) + ln(1 + comments) only from that point-in-time snapshot;
- aggregate positive and negative engagement separately by UTC day;
- standardize each series against the preceding 365 calendar days, excluding the current day;
- calculate net sentiment as positive z-score minus negative z-score;
- retain unsmoothed daily values and separately test 7-day and 30-day trailing smooths.

R-RISI is a standardized engagement-balance index, not a percentage, probability, or return forecast. Daily/weekly series cannot be expanded into fictitious five-minute observations. Any hourly feature must use only posts already observed by that hour and be evaluated separately from the daily indicator.

The current public R-RISI dashboard reports a model-version change: the accompanying paper describes GPT-5.1, while the dashboard documents GPT-5.1 through December 2025, GPT-6.1 Sol from January 2026, and Codex with GPT-6.1 Sol for interim data from October 2026. Freeze one classifier version for each experiment; do not splice model vintages without an explicit recalibration study.

## 6. Pre-registered ablations

Use identical forecast origins, venue, quote currency, target grid, cutoff and data-quality gates:

| Variant | Features |
|---|---|
| A | Price/return + volatility baselines only |
| B | A + intraday seasonality |
| C | B + scheduled macro-surprise variables |
| D | B + sentiment and attention, kept separate |
| E | B + crypto-news novelty / event variables |
| F | B + macro-surprise × sentiment interactions |
| G | Combined candidate, only if individual families survive |

Use chronological walk-forward folds, purge overlapping 24-hour labels, and embargo at least the forecast horizon. Report the frozen primary normalized hourly log-price MAE, random-walk and volatility-aware baseline losses, directional accuracy, interval calibration and sample size. Use paired uncertainty intervals; do not select features on the final holdout.

## 7. Falsification and leakage tests

- **Future-masking invariance:** adding, deleting or editing any event observed after cutoff t must not change features or forecasts at t.
- **Timestamp tests:** UTC conversion, DST handling, release-time boundaries, late ingestion and revisions.
- **Deduplication tests:** syndicated headlines, reposts, cross-posts and repeated Reddit submissions.
- **Engagement-vintage tests:** future score/comment changes must not rewrite earlier snapshots.
- **Placebos:** shifted macro release times, randomized sentiment labels and within-day shuffled event times.
- **Coverage checks:** missing source periods, subreddit composition shifts, bots, deleted/moderated posts, language drift and model-version drift.
- **Incremental value:** every family must beat the same simpler baseline out of sample; an event-study coefficient alone is insufficient.

## 8. Data rights and implementation gate

The ECB R-RISI dashboard identifies Reddit Academic Torrents archives and Reddit Data API interim collection, and requests citation/information for report or research use. This is not treated as a blanket code, corpus, redistribution or commercial-use license. Reddit platform terms, archive terms, article rights, model API terms and any market-data vendor terms require separate review.

No Reddit corpus, raw post text, news feed, classifier weights, consensus data, or external implementation was copied for this protocol. Implementation is blocked until data provenance, point-in-time snapshots and applicable use terms are documented. Until then, sentiment/news features remain disabled.

## Sources

- Cho et al. (2026-10-29), *Cryptocurrency markets as an evolving complex system: stylized facts, scaling, and complexity*, Frontiers in Physics, DOI: https://doi.org/10.3389/fphy.2026.2026031
- Wagner & Metzler (2026-08-24), ECB Working Paper No. 3276, *When the Crowd Speaks: AI-based retail investor sentiment indicator with Reddit data*: https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3276~3ba8565a13.en.pdf
- Wagner & Metzler (2026-11-12), ECB Blog, *Reading the room: what Reddit tells us about retail investor sentiment*: https://www.ecb.europa.eu/press/blog/date/2026/html/ecb.blog20261112~a4c8b903d9.en.html
- R-RISI dashboard and methodology: https://dashboard.r-risi.workers.dev/
- Huynh (2026-06), *Tuning into the news: Sentiment-driven high-frequency movements in cryptocurrency markets*, Journal of Behavioral and Experimental Finance 50, 101183, DOI: https://doi.org/10.1016/j.jbef.2026.101183

This protocol is an experiment design, not evidence of a predictive edge and not financial advice.
