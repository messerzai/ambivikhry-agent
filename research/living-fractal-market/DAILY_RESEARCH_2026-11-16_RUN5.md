# Living Fractal Market — daily research report

Date: 2026-11-16  
Branch: research/living-fractal-market  
Daily run marker: lfm-daily-20261116-0710z-r6  
Daily trigger commit: 594b8c6ef96254f395859a4fb4149726653f0d63

## 1. Research discoveries

- Insu Choi, Physica A (2026), DOI 10.1016/j.physa.2026.131735: abstract-level report on ~774,000 BTC 5m observations, q-Gaussian rescaling and a ~25-day scaling crossover. Full text was paywalled in this review; treat as a diagnostic hypothesis, not an established universal market law.
- Haroon, arXiv:2607.23370 (2026-07-25): regime-gated Reddit FinBERT + OHLCV BiLSTM on 3,491 BTC-USD hourly rows; chronological test 1,345 rows. Reported AUC 0.5084 at 3h and 0.4902 at 6h; true-down specificity 44.6%. Preprint and near-chance evidence; no code/data reused.
- Figura et al., Forecasting 8(3), 41 (2026-05-19): 262 weekly BTC observations; PLS-SEM uncertainty mediator for future volatility. The article explicitly reports lower raw forecast error for GARCH(1,1), so the structural model is not a general winner.
- Noguer i Alonso & Franklin, arXiv:2606.27100: TSFMs rank highly on five equities, but gains over zero-return random walk are small and only two task-level DM tests are significant. Not BTC evidence.

Sources: https://doi.org/10.1016/j.physa.2026.131735 ; https://arxiv.org/abs/2607.23370 ; https://doi.org/10.3390/forecast8030041 ; https://arxiv.org/abs/2606.27100

## 2. Competitor watchlist

Added/clarified Choi multifractal diagnostics, RAML sentiment/regime preprint, Figura weekly volatility architecture and the financial TSFM benchmark. TimesFM's 2026-09-25 report claims 10 verified daily 24h-TWAP predictions, MAE $551.11, 70% direction and 40% within range, but its report's source table has CoinGecko values with Binance values absent; README separately says historical CSV rows are legacy_h1 and the H24 collector's CI/first live prediction are unverified. It is excluded from the comparable leaderboard. No current external BTC/USD hourly forecast met our exact comparability rules.

## 3. Workflow, forecast and archive

Forecast workflow: https://github.com/messerzai/ambivikhry-agent/actions/runs/43822029565  
Archive workflow: https://github.com/messerzai/ambivikhry-agent/actions/runs/43822527134  
Source commit: 594b8c6ef96254f395859a4fb4149726653f0d63  
Archive commit: 7674c69303dfa69e9bf5f0d17844895b345774a3

The 5m workflow passed offline tests (11/11), public Binance Spot data retrieval, forecast generation and artifact upload. Exact artifact ID 14205340703 was downloaded and archived losslessly as the original workflow ZIP plus extracted JSON. The archive ledger records:
- ZIP SHA-256: 4cf16244a517d2fca87def0a29714f2e4cca69296843620a70b573c9f61c8982
- Extracted JSON SHA-256: f511922101b426534caeb7894f979fca8352e14122c19c3ecca690b82d7b7c6e
- Issue UTC: 2026-11-16T07:11:30.546109Z
- Data cutoff UTC: 2026-11-16T07:09:59.999000Z
- Reference price: 64,670.80 USDT
- 999 closed 5m candles; 24 hourly target points; Binance Spot BTC/USDT.

Exact archive:
research/living-fractal-market/forecasts/2026-11-16/2026-11-16T07-11-30.546109Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip

The model is LFM-5m-Downside-Aware-Council-0.4, a challenger, not a validated BTC/USD champion. The history is 83.25 hours, far shorter than the preferred 90-day seasonal sample. The JSON lacks explicit model_commit, vintage_id and retrieved_at_utc fields; ledger supplies source commit and archive provenance.

### LFM5mEnsemble hourly path (USDT)

| Horizon | Target UTC | Predicted |
|---:|---|---:|
| +1 | 2026-11-16 08:00 | 64,690.95 |
| +2 | 2026-11-16 09:00 | 64,708.12 |
| +3 | 2026-11-16 10:00 | 64,722.76 |
| +4 | 2026-11-16 11:00 | 64,735.27 |
| +5 | 2026-11-16 12:00 | 64,745.99 |
| +6 | 2026-11-16 13:00 | 64,755.19 |
| +7 | 2026-11-16 14:00 | 64,763.10 |
| +8 | 2026-11-16 15:00 | 64,769.94 |
| +9 | 2026-11-16 16:00 | 64,775.86 |
| +10 | 2026-11-16 17:00 | 64,781.01 |
| +11 | 2026-11-16 18:00 | 64,785.51 |
| +12 | 2026-11-16 19:00 | 64,789.46 |
| +13 | 2026-11-16 20:00 | 64,792.95 |
| +14 | 2026-11-16 21:00 | 64,796.05 |
| +15 | 2026-11-16 22:00 | 64,798.81 |
| +16 | 2026-11-16 23:00 | 64,801.30 |
| +17 | 2026-11-17 00:00 | 64,803.56 |
| +18 | 2026-11-17 01:00 | 64,805.62 |
| +19 | 2026-11-17 02:00 | 64,807.51 |
| +20 | 2026-11-17 03:00 | 64,809.26 |
| +21 | 2026-11-17 04:00 | 64,810.90 |
| +22 | 2026-11-17 05:00 | 64,812.44 |
| +23 | 2026-11-17 06:00 | 64,813.89 |
| +24 | 2026-11-17 07:00 | 64,815.27 |

The ensemble endpoint is +0.223% versus reference. Other model +24 endpoints: RandomWalk 64,670.80 (0.000%); Momentum5m 64,914.01 (+0.376%); MeanReversion5m 64,728.04 (+0.089%); VolatilityRegime5m 64,923.04 (+0.390%); TakerFlow5m 64,671.72 (+0.001%); DownsideStress5m 64,670.80 (0.000%).

No calibrated P50/P90 intervals exist; emitted Gaussian-style P90 ranges are uncalibrated. The 70,000 USDT level was already 8.24% above the reference. The heuristic probability 1.0 is a terminal-below-level diagnostic, not a new downward-crossing probability. The -6% scenario price 60,790.55 is illustrative only and has no assigned probability.

## 4. Evaluation and leaderboard

Evaluation workflow: https://github.com/messerzai/ambivikhry-agent/actions/runs/43822029545  
Evaluation tests passed 11/11. Snapshot: 4 already evaluated, 0 newly evaluated, 0 failed, 2 pending before the current forecast archive was committed. The current 2026-11-16 vintage is also pending; the two 2026-11-15 vintages remain pending until their final hourly closes.

Four previously matured vintages:
| Issue UTC | LFM nMAE | RandomWalk | Volatility-aware | Outcome |
|---|---:|---:|---:|---|
| 2026-11-12 08:03 | 9.4641 | 9.0509 | 7.3504 | loses to both |
| 2026-11-13 08:07 | 1.8265 | 1.9175 | 2.3634 | beats both |
| 2026-11-13 07:59 | 1.7186 | 1.7426 | 2.5965 | beats both |
| 2026-11-14 07:18 | 5.5006 | 5.2052 | 3.0107 | loses to both |

The two Nov 13 origins overlap by about 23 hours; target errors are dependent. P90 is not calibrated. Virtual research points: 0. Champion: none. Promotion threshold remains 30 completed daily vintages plus robust walk-forward evidence.

External leaderboard: no comparable current entries. TimesFM historical daily TWAP report, RAML directional preprint, Choi multifractal analysis and weekly volatility studies use different targets/horizons or lack matching forward ledgers.

## 5. Operational fix: archive workflow race

The first archiver invocation for the daily marker saw a stale ARCHIVE_RUN_TRIGGER source SHA and started before sibling forecast/evaluation runs were visible; it archived old evaluation artifacts but not the current forecast. The exact current forecast was then archived by a separate archive-only marker commit, without changing the daily marker a second time.

A scoped fix now:
- uses the archive marker only when that file changed in the triggering commit;
- uses the current event SHA for daily-marker pushes and waits up to five minutes for sibling forecast/evaluation run records and completion;
- checks out the exact event commit via github.sha.

Code/test/workflow commits:
- https://github.com/messerzai/ambivikhry-agent/commit/40adf48f16a9ccdf801115818eeeb8be688d8e34
- https://github.com/messerzai/ambivikhry-agent/commit/f786ebc2221971ec8d2ce38d9fec4c43fcca0dd4
- https://github.com/messerzai/ambivikhry-agent/commit/61bdf08037d01f2cc4b6ce96b7ea09573f9282ff
- https://github.com/messerzai/ambivikhry-agent/commit/c4995818a9b1abb215884525e261f033705bb28c

Final archive regression suite: 7/7 passed. Full project pytest matrix: 45 passed in Python 3.10, 3.11, 3.12 and 3.13. One initial fixture failure from a double-escaped newline was corrected in the final test commit; the final CI run is green. Archive workflow itself passed after the fix; the fix's daily-trigger wait path is covered by unit tests but has not yet been exercised by a second daily live run.

## 6. License audit

No third-party code, model weights, datasets, tokenizers, raw posts, LOB events or paid APIs were copied. MDPI Figura et al. article is CC BY 4.0; source data terms remain separate. Choi's exact article license was not verifiable from the accessible paywalled record. RAML and TSFM preprints do not license separate code/data. TimesFM repository code is Apache-2.0, but TimesFM 3.0 weights remain separately non-commercial/non-production; no weights were used.

## 7. Next experiment

1. Add self-describing forecast fields: input_interval, model_commit, vintage_id and retrieved_at_utc; add schema tests without changing old artifacts.
2. Build a paginated, immutable 90-day Binance Spot 5m panel and preserve raw source revision hashes.
3. Add seasonality and volatility-aware controls, then run preregistered q-Gaussian/MF-DFA, sentiment and news ablations.
4. Keep Spot, perpetuals and L2 event streams separate; do not reconstruct order-book features from OHLCV.

No trades, transfers or order execution occurred. This is research, not financial advice.
