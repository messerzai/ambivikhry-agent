# Living Fractal Market — Daily Research Report
## 2026-11-26 · Run 15

Branch: [research/living-fractal-market](https://github.com/messerzai/ambivikhry-agent/tree/research/living-fractal-market)

## Status

No validated BTC/USD hourly champion exists yet. The current live model remains the experimental BTC/USDT council using Binance 5m inputs; it is a challenger only. Today's live forecast was successfully generated, verified and archived. The evaluator correctly kept the prior vintage pending. No champion promotion and no virtual points.

## 1. Workflows and artifact provenance

Daily marker commit: [c72f8c42](https://github.com/messerzai/ambivikhry-agent/commit/c72f8c42e6b1120c9ee74ed52d16285d417a5a59), marker lfm-daily-20261126-0747z-r15-8d6a.

| Workflow | Run | Result |
|---|---:|---|
| LFM 5m forecast | [45778079870](https://github.com/messerzai/ambivikhry-agent/actions/runs/45778079870) | Success; offline tests 15/15; live Binance retrieval, forecast generation and upload succeeded |
| Completed-vintage evaluator | [45778079869](https://github.com/messerzai/ambivikhry-agent/actions/runs/45778079869) | Success; evaluator tests 17/17; evaluated 0, failed 0, pending 1 |
| Full repository tests | [45778079940](https://github.com/messerzai/ambivikhry-agent/actions/runs/45778079940) | Success on Python 3.10–3.13 |
| Immutable archiver | [45778079883](https://github.com/messerzai/ambivikhry-agent/actions/runs/45778079883) | Success; exact ZIP, JSON and raw input archived |

Forecast artifact ID 15096309244, name lfm-5m-btc-forecast, 59,643 bytes. GitHub digest and independently computed ZIP SHA-256 both equal:

99adf7f3acf86e78db08587f9c00e8d970347fb867eaffd6144792d97f48adbd

- Extracted forecast JSON SHA-256: 1ce29c943f746954b5007086c1413c14b3810617ee4c64fef0e12c1e715fabb0
- Raw 5m response SHA-256: 67d9a8882e36cd0d723098ea00f691885c9183a95182f147d7da220065427db2 (173,970 bytes)
- Schema/vintage: lfm.forecast.5m.v2 / lfm5m-2026-11-26T07:48:41.671080Z-BTCUSDT-binance-spot-council-0.4
- Model commit: c72f8c42e6b1120c9ee74ed52d16285d417a5a59
- Issue/cutoff UTC: 2026-11-26T07:48:41.671080Z / 2026-11-26T07:44:59.999000Z
- Asset/venue/quote: BTC/USDT / Binance Spot / USDT; input interval 5m
- Reference price: 60,636.02 USDT; 999 closed input candles; 24 hourly target candle opens, 2026-11-26 08:00 through 2026-11-27 07:00 UTC.

Archive commit: [810035b8](https://github.com/messerzai/ambivikhry-agent/commit/810035b881ccdcf1d52133c0a1725679886f000d). It added the exact artifact ZIP, extracted JSON, raw 5m response and append-only FORECAST_LEDGER entry. No second daily marker was written.

## 2. Current 24-hour hourly challenger forecast

This is **not** a BTC/USD champion forecast. It is LFM-5m-Downside-Aware-Council-0.4 for BTC/USDT, based on 5m Binance Spot inputs. Point estimates are in USDT. The emitted Gaussian-style P90 bounds are not calibrated intervals and are not presented as 90% coverage.

| Horizon | Target candle open UTC | Point (USDT) |
|---:|---|---:|
| +1 | 2026-11-26 08:00 | 60,664.86 |
| +2 | 2026-11-26 09:00 | 60,689.17 |
| +3 | 2026-11-26 10:00 | 60,709.68 |
| +4 | 2026-11-26 11:00 | 60,726.97 |
| +5 | 2026-11-26 12:00 | 60,741.56 |
| +6 | 2026-11-26 13:00 | 60,753.85 |
| +7 | 2026-11-26 14:00 | 60,764.21 |
| +8 | 2026-11-26 15:00 | 60,772.94 |
| +9 | 2026-11-26 16:00 | 60,780.28 |
| +10 | 2026-11-26 17:00 | 60,786.46 |
| +11 | 2026-11-26 18:00 | 60,791.65 |
| +12 | 2026-11-26 19:00 | 60,796.00 |
| +13 | 2026-11-26 20:00 | 60,799.65 |
| +14 | 2026-11-26 21:00 | 60,802.69 |
| +15 | 2026-11-26 22:00 | 60,805.23 |
| +16 | 2026-11-26 23:00 | 60,807.35 |
| +17 | 2026-11-27 00:00 | 60,809.09 |
| +18 | 2026-11-27 01:00 | 60,810.53 |
| +19 | 2026-11-27 02:00 | 60,811.72 |
| +20 | 2026-11-27 03:00 | 60,812.68 |
| +21 | 2026-11-27 04:00 | 60,813.45 |
| +22 | 2026-11-27 05:00 | 60,814.06 |
| +23 | 2026-11-27 06:00 | 60,814.54 |
| +24 | 2026-11-27 07:00 | 60,814.91 |

### Quality and warning checks

- 1,000 raw rows, 999 closed 5m candles; open timestamps unique and ordered.
- Latest closed candle: 07:44:59.999 UTC; issue followed 221.672 seconds later.
- All seven models emitted 24 positive finite values on the same target grid.
- Reference price is already 13.377% below the 70,000 USDT threshold. The heuristic terminal-below-level value of 1.0 describes an already-true terminal condition, not a probability of crossing the level. It is uncalibrated and not a first-passage probability.
- No stale-feed or malformed-candle gate failed. BTC/USDT is not identical to BTC/USD.

## 3. Previous evaluation and internal leaderboard

The 2026-11-25 vintage remains pending until its final target candle closes at 2026-11-26T07:59:59.999Z. The 07:48 evaluator manifest listed 18 already-evaluated unique vintages, one pending, zero failures and zero new evaluations. Its tests explicitly verify that the final close is not scored early.

The prior completed 2026-11-24 vintage:
- LFM5mEnsemble nMAE 1.121056
- RandomWalkLastPrice nMAE 1.074432
- VolatilityCappedSlowDrift nMAE 0.357336
- P90 calibrated: false; points: 0

Aggregate leaderboard: 18 completed unique vintages, 11 non-overlapping vintages eligible for comparison. Mean nMAE (lower is better):
- MeanReversion5m 3.211871 (11 vintages); difference vs random walk -0.007326; paired bootstrap 95% CI [-0.063146, 0.055261], includes zero.
- RandomWalkLastPrice 3.219197.
- TakerFlow5m 3.221266.
- LFM5mEnsemble 3.348850.
- VolatilityRegime5m 3.398744.
- Momentum5m 3.519714.
- DownsideStress5m 3.929772.

No champion promotion: only 11/30 required non-overlapping vintages, no calibrated intervals, and no statistically resolved advantage. Virtual research points: 0.

## 4. External competitor watch

- BtcForecaster v2-har publishes genuine live 1h/4h/12h/24h BTC/USDT ranges and outcomes. At 2026-11-26 07:48 UTC, since-launch 90% hit rates were 89.6% ±2.2 (1h), 87.9% ±4.5 (4h), 92.2% ±13.5 (12h), 83.8% ±11.2 (24h); rolling 7d 24h coverage 90.7% ±23.4, only about six independent outcomes. Its 24h 90% range at 07:45 UTC was 55,492–66,257 USDT around 60,636 USDT. Range-only; target times do not match our hourly candle grid, so not ranked against point paths.
- BtcForecaster v3-har-cal90 remains a live shadow candidate under a preregistered test through 2026-12-07; its historical improvement is backtest evidence, not the live result.
- BTC-Oracle provides a 31-fold walk-forward BTC-USD 24h quantile benchmark but no public live ledger; none of its models passes all promotion gates.
- HawkesTime is a high-frequency LOB event-direction study, not a 24h path.
- GPTReviews and BitPredict remain direction-only/unverified references.
- No external point-price competitor has a verified timestamped path on our exact hourly target grid. External ranks: none.

## 5. Research discoveries

Newly logged:
- Kwapień et al. (2023) and Kluszczyński et al. (2025): test genuine multifractality against dependence-preserving tail controls; heavy tails alone do not establish it.
- Choi (2026): q-Gaussian rescaling and a reported ~25-day BTC scaling crossover; full text paywalled, so detailed claims await replication.
- Raffaelli et al. (2026): Hawkes + continuous-time book-imbalance model for event-level BTC/USD sign.
- Huynh (2026) and Kroner et al. (2026): scheduled macro surprises affect crypto at high frequency; sentiment may moderate those reactions. Point-in-time timestamps, revisions and data licenses remain constraints.
- Anastasopoulos et al. (2026): world order flow may help daily/weekly cross-sectional crypto returns, not hourly BTC.

The current 999-candle history is only about 83.25 hours; it cannot support a robust 25-day scaling-crossover test. No multifractal feature was added.

## 6. Code, docs and license audit

No forecasting or evaluator code changed. Documentation commits:
- [RESEARCH_LOG.md](https://github.com/messerzai/ambivikhry-agent/commit/164316023d59461e2f4c639a37a67dceeb3ea396)
- [COMPETITOR_LANDSCAPE.md](https://github.com/messerzai/ambivikhry-agent/commit/53d9a3ee07510b9db40f9ce1467545a9eacbc046)
- [THIRD_PARTY_LICENSES.md](https://github.com/messerzai/ambivikhry-agent/commit/16a9b89b21ef351c2b7ea347de6f6e9bc8846baa)

License audit: verified MIT for btcforecaster-eval and BTC-Oracle; Apache-2.0 for Chronos code/weights, TimeCopilot code, TimesFM code and TimesFM 2.5 weights. TimesFM 3.0 weights use a non-commercial/non-production license and are excluded from commercial/production use. No third-party code, weights, datasets, article text, figures or forecast payloads were copied.

## 7. Next experiment

Acquire a point-in-time, venue-consistent BTC history long enough for scaling analysis (initial target at least 170 days of 5m data), then preregister the q-Gaussian/IAAFT/shuffle surrogate battery and finite-size checks. In parallel, specify a macro-surprise ablation only if consensus values, release timestamps, revisions and dataset terms can be audited. Keep champion/challenger status unchanged until the frozen walk-forward tournament clears its gates.

Research only; no trading, fund movement or execution connection. Not financial advice.
