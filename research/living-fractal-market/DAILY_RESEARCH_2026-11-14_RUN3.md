# Living Fractal Market — daily research report (run 3)

**Date:** 2026-11-14  
**Branch:** `research/living-fractal-market`  
**Scope:** research branch only; no changes to `main`.

## Summary

This cycle focused on a sharper separation of **sentiment polarity, attention, network contagion and news surprise**. Recent studies repeatedly suggest that attention/contagion can be more informative for volatility and trading intensity than a raw positive/negative score is for returns. A new ablation protocol records these as separate feature families with strict first-available-time controls.

## Research discoveries

- Dallas Fed WP 2605 (Han, Liu & Sui, 2026) studies Bitcointalk 2012–2022 and linked user transactions. It distinguishes peer sentiment from aggregate contagion intensity; the latter is reported to forecast volatility, volume and crash risk. This is a preliminary working paper and its CoinAPI/RavenPack data dependencies are not a freely reusable dataset.
- Huynh (JBEF, 2026) reports that daily crypto sentiment moderates 5-minute market responses to scheduled macro surprises in a top-100 crypto sample. The result motivates a surprise × prior-sentiment interaction, not a standalone sentiment signal.
- Akbar (Studies in Economics and Finance, 2026) reports in the publisher abstract that polarity and hype do not predict BTC returns, while attention improves conditional-variance modelling. Full text was not accessible; abstract-level only.
- Shynkevich (Journal of Futures Markets, 2026) reports periodic subsecond BTC/ETH trading bursts that raise volatility and transaction costs but do not significantly worsen price impact. This tempers the assumption that clock-phase periodicity is automatically directional alpha.
- New model candidates: daily ARFIMA-GAS/AEGAS, hourly VMD-CNN, regime-aware sentiment classification (RAML), 1-second CatBoost order-book microstructure, and quantum-circuit realized-volatility diagnostics. None provides a comparable current 24-step Binance Spot hourly forecast.

## Branch changes

- Added `SENTIMENT_NEWS_ABLATION_PROTOCOL.md`: point-in-time feature families, event/publication/first-seen timestamps, baselines, nested ablations, walk-forward validation and falsification criteria.
- Expanded `COMPETITOR_WATCHLIST_ADDENDUM_2026-11-14.md` with eight research/model candidates and their horizons, data, evidence and reproducibility limits.
- Expanded `RESEARCH_LOG.md` with primary-source notes and limitations.
- Expanded `INTRADAY_SEASONALITY_PROTOCOL.md` with a published counterpoint on periodic trading and price impact.
- Updated `THIRD_PARTY_LICENSES.md` to record that no code, weights, data, tokenizers or paid APIs were reused.
- Added this report.

## Forecast and evaluation

The daily trigger marker was updated and committed as `1a6e55bc37e74454293736dce0cb0a4fe2dd8e20` (marker `lfm-daily-20261114-074515z-r3`). This commit touches only `DAILY_RUN_TRIGGER.md` and matches the path filter of the branch-isolated forecast workflow. The GitHub connector available in this run does not expose a push-workflow run-list endpoint; as of this report's preparation the branch ledger had not yet recorded a new artifact from this trigger. Therefore no new live forecast is claimed here.

The last recorded vintage is 2026-11-14T07:18:16.591141Z, Binance Spot BTCUSDT, 5m input, 24 hourly targets. It is a challenger, not a validated BTC/USD hourly champion. Its final target close is 2026-11-15T07:59:59.999Z. The 2026-11-13 vintages also remain pending at the 2026-11-14 07:45 UTC review time. The 2026-11-12 vintage is eligible for evaluation, but no newly archived evaluation artifact was available at this point.

- Valid live forecast from this trigger: **not yet verified**.
- Completed independent daily vintages for promotion: **0**.
- Calibrated intervals: **none**.
- Virtual points: **0**.
- Champion promotion: **none**.

## License and test status

No third-party assets were copied. Code/model-weight/data terms remain separate and are not inferred from public access. No forecast-model code changed in this cycle; no fresh unit-test run is claimed. The last recorded 5m suite result remains 11/11 on the prior 0.4 workflow run; it is not a test result for this trigger.

## Next experiment

1. Confirm the current marker's LFM 5m and evaluation workflows and archive exact artifacts only after successful completion.
2. Retrieve exact Binance Spot 1h closes for the completed 2026-11-12 vintage and evaluate with the frozen protocol.
3. Build a 90-day paginated 5m dataset; keep Spot and Perpetual separate.
4. Run seasonal-naive, attention, polarity and macro-surprise ablations only after point-in-time data and lawful source terms are available.
5. Keep all new features diagnostic until they beat random walk and volatility-aware controls on the primary price-path loss.

No trades, orders, transfers or execution credentials were used. Research only; not financial advice.


## External public forecaster watch — 2026-11-14

- **CoinPredict:** its public ledger shows 6,710 graded 24h calls across assets (54% direction, 83% in its 80% range). The BTC page shows 18 BTC 24h calls, 56% direction, 77.8% in-range, 0.9% median miss; latest visible BTC call was made 2026-11-11 00:00 UTC and expired Nov12. Useful future terminal-price comparator, but small BTC sample and no matching current hourly path.
- **Satori Signals:** 237 BTC forecasts in the displayed last-30-day sample, 50.6% direction, 1.07% average error equal to no-change baseline, 75.5% inside its central 80% range; only 11 days checked. Access to full forecasts requires token holding or subscription; read-only only.
- **SignalTrace Lab:** 24h BTC probability 47% up / 53% down vs historical up frequency 48.2%, explicitly uncalibrated and stale (opened issue time Nov10 00:00 UTC). A newer search snippet conflicted with the page, so not used.
- **BitPredict:** public human-member 24h calls are timestamped, but the displayed 71% UP / 29% DOWN split is from Nov2 15:39 UTC; not current. No registration or automated submission.
- **Coinbase prediction markets:** read-only hourly/15-minute threshold probabilities are an event-market reference, not a full BTC price-path forecast.

No external forecast is scored against the Nov14 LFM vintage because issue times, target paths and cutoffs do not match. No token, paid service, account, wager or external commitment was used.
