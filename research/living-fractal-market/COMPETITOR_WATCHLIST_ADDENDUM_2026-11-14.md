# Competitor and method watchlist addendum — 2026-11-14

Target experiment: BTC/USD hourly path, horizons +1 through +24. This addendum separates model discovery and research methods from comparable forward competitors.

## New public benchmark lead

| Project / method | Asset and horizon | Public evidence checked 2026-11-14 | Reproducibility and decision |
|---|---|---|---|
| SOTA2 Univariate Time-series Forecasting on Exchange (test) | Generic Exchange dataset; visible zero-shot entries use input length 96 and prediction length 96 for several models. Not identified as BTC. | Cross-RAG MSE 0.064 / MAE 0.175; TTM 0.066 / 0.173; Moirai 0.066 / 0.172; Chronos-bolt 0.067 / 0.178; TimesFM 0.070 / 0.180; Chronos 0.083 / 0.188; Time-MoE 0.085 / 0.206; MOMENT 0.098 / 0.206; ARIMA 0.112 / 0.245; N-HITS 0.114 / 0.248; N-BEATS 0.156 / 0.299. The page says it was updated about eight months before this check. | Useful broad model-screening signal only. The dataset, target and evaluation are not BTC/USD hourly path forecasts; do not import these ranks into the LFM leaderboard. No code, weights or data copied. Source: https://www.sota2.com/research/sota/univariate-time-series-forecasting-on-exchange-test |

## New research-method candidates (not yet executable competitors)

| Candidate | Method / target | Data requirements | Evidence and limitations | Status |
|---|---|---|---|---|
| Vanheusden et al. (2026), RQA for crypto | Recurrence plots and RQA statistics; 100 crypto assets; daily USD close data; multi-day volatility warning (5–50d) | Reproducible daily price history, declared embedding/threshold settings, point-in-time rolling windows | Reported D/L ratio AUROC 0.605 at 42d. No 24h BTC price-path evidence; no MFDFA comparison; parameter search incomplete; data available on request. | Diagnostic challenger only; independent clean-room implementation from standard RQA literature may be considered after tests. No paper text, figures or code copied. |
| Han, Liu & Sui, Dallas Fed WP 2605 (2026) | Social-network sentiment contagion and individual trading decisions; predicts BTC volatility/volume/crash risk, not future price | Timestamped social interaction graph, individual/aggregate trade records, point-in-time sentiment | Abstract reports peer sentiment itself does not predict future BTC prices; contagion intensity forecasts volatility, volume and crashes. Data provenance/availability and full reproducibility need audit. | Volatility-risk feature hypothesis only; no scalar sentiment price signal added. |
| Zouari, Alon & Shtudiner (2026), collective criticality | Cross-asset volatility scaling, tail co-exceedance and cascade amplification; BTC/ETH/SOL hourly and daily | Aligned multi-asset spot or explicitly separate derivatives data; exact null construction; full paper methods | Abstract record describes BTC as boundary-adjacent and reports tail synchronization. Publisher full text returned 403; methods and data not independently replicated. | Discovery lead only; not a ranked forecaster. Full-text and methodology audit required. |

## Existing foundation-model challengers retained

- Chronos-2: first locally runnable foundation-model challenger after pinning exact checkpoint revision and verifying code/weight licenses separately.
- TimesFM 2.5: second foundation-model challenger; keep model-card revision and weight license separate from source-code license.
- N-BEATS / N-HiTS / PatchTST / TFT: train on identical rolling-origin BTC splits and disclose tuning budget and seed.
- ARIMA / ETS / zero-drift / volatility-aware: mandatory statistical baselines.
- RQA, MF-DFA and sentiment/network features remain ablation candidates, not champion components.

## External leaderboard decision

No new result meets the matching contract of BTC spot venue, quote currency, exact issue time and information cutoff, 24 hourly target closes, and a preserved point-price path. SOTA2 is not BTC-specific; the RQA and criticality papers are diagnostics; the Dallas Fed paper concerns network contagion and risk variables. No external ranking or research points awarded.

## Sources

- SOTA2 benchmark: https://www.sota2.com/research/sota/univariate-time-series-forecasting-on-exchange-test
- SOTA2 Exchange dataset index: https://www.sota2.com/research/dataset/exchange
- RQA article: https://link.springer.com/article/10.1186/s40854-026-00940-x
- Dallas Fed working paper 2605: https://www.dallasfed.org/research/papers/2026/wp2605
- Collective criticality abstract record: https://econpapers.repec.org/article/eeechsofr/v_3a211_3ay_3a2026_3ai_3ap1_3as0960077926009501.htm


## Daily watchlist expansion — 2026-11-14 (sentiment, news, statistical and microstructure)

| Candidate / source | Method, data and horizon | Reported evidence | Reproducibility / comparability | Status |
|---|---|---|---|---|
| Chikhi et al., ARFIMA-GAS/EGAS/AEGAS (Czech JEF 2026) | Daily BTC prices in five fiat quotes from Coincheck, 2018-06–2024-06; rolling daily return/volatility forecasts | Paper reports GAS-family models outperform random walk over 2024-06-11–2024-08-28; skewed Student-t, leverage and jumps | Published paper/PDF available; no code found in checked page. Daily and short holdout; not hourly Binance Spot. | Statistical daily-scale challenger blueprint only |
| Wang, Huang & Liao, VMD + deep learning (Finance Research Letters 2026) | Hourly BTC data 2016-01–2025-06; VMD with CNN and other deep models | Abstract says VMD improves performance across architectures and VMD-CNN is best | Full text paywalled; abstract does not state exact horizon, full scores, split details or code. | Multi-scale challenger lead; not yet reproducible |
| Haroon, RAML (arXiv:2607.23370, 2026-07-25) | BTC-USD hourly OHLCV + Reddit FinBERT; 3h/6h directional classification; 3,491 aligned rows | AUC 0.5084 at 3h and 0.4902 at 6h; test window 1,345 observations (Jul–Sep 2025) | Preprint, no code license/repository identified. AUC near/below chance; full-sample vs training-only volatility threshold is inconsistent in the paper. Not a price-path forecast. | Unranked sentiment challenger/reference; reproduce only with a leakage audit |
| Bieganowski & Ślepaczuk, CatBoost microstructure (arXiv:2602.00776, 2026-01-31) | Binance Futures perpetual LOB/trades at 1s, 2022-01–2025-10; 3s mid-price returns; five assets | Authors report stable feature rankings and SHAP shapes across assets; time-series CV and execution backtests | Preprint; no matching Spot BTC hourly forecasts; no repository/code license identified in checked arXiv page. | L2/OFI feature reference only |
| Takaishi, QCL volatility (arXiv:2609.04569, 2026-09-03) | 5m BTC data -> daily realized volatility; single-qubit circuit; MF-DFA on synthetic series | Abstract reports qualitative reproduction of some multifractal/rough-volatility signatures | Preprint; not a price-path benchmark and no runnable implementation/license identified in checked record. | Volatility diagnostic only |
| Choi, intrinsic multifractality (Physica A 697, 131735, 2026) | ~774k BTC 5m observations, 2017-08–2024-12; q-Gaussian rescaling | Abstract reports ~25-day scaling crossover and adaptive-efficiency changes around ETF approval | Peer-reviewed journal record; full text not accessible in this review; no code/data replication. | MF-DFA/q-Gaussian diagnostic candidate |
| Huynh, news/sentiment interaction (JBEF 101183, 2026) | 5m top-100 crypto data, 2014–2021; US macro announcements; daily TRMI sentiment | Abstract reports bullish sentiment attenuates macro-news return response ~16% and turnover response ~24% per SD | Journal abstract checked; historical multi-asset sample, not BTC-only; no matching forecast ledger. | Event-window interaction hypothesis |
| Akbar, human vs automated social signals (Studies in Economics and Finance, 2026-05-06) | >16m BTC tweets; human-like/automation-like groups; returns and GARCH-X variance | Abstract reports polarity/hype/anxiety do not predict returns; attention improves variance model and reacts to price shocks | Abstract-only; full text/code unavailable in this review. | Attention/volatility hypothesis, not direction model |
| Han, Liu & Sui, Dallas Fed WP 2605 (2026-03-02) | Bitcointalk social graph/posts 2012–2022, linked wallet subsample; CoinAPI hourly BTC returns and daily risk measures | Working paper distinguishes peer sentiment from contagion intensity; latter predicts volatility/volume/crashes; cumulative net contagion is discussed separately in return analysis | Preliminary working paper; historic forum-specific data and RavenPack/CoinAPI dependencies limit reproducibility. | Network-contagion risk-feature hypothesis |
| Shynkevich, periodic trading (J Futures Markets, first published 2026-02-18) | Subsecond BTC/ETH Spot and perpetual trading activity | Abstract reports periodic bursts raise volatility/costs but no significant adverse price impact | Published journal article; data available from author on request; no public ledger. | Supports seasonal/liquidity controls, not automatic directional alpha |

### Interpretation and ranking

None of these sources provides a timestamped Binance Spot BTCUSDT 24-step hourly price path matching our issue time, cutoff and scoring contract. They remain unranked. ARFIMA-GAS and VMD-CNN are the most relevant model-architecture challengers for offline reproduction; RAML and the attention/news papers inform causal feature ablations; LOB CatBoost is too fine-grained and futures-specific for the current forecast target. No external rank or virtual point is awarded.

### Sources

- ARFIMA-GAS/AEGAS: https://doi.org/10.32065/CJEF.2026.01.03
- VMD/deep learning: https://doi.org/10.1016/j.frl.2026.109776
- RAML: https://arxiv.org/abs/2607.23370
- Explainable microstructure: https://arxiv.org/abs/2602.00776
- QCL/MF-DFA: https://arxiv.org/abs/2609.04569
- Choi multifractality: https://doi.org/10.1016/j.physa.2026.131735
- News/sentiment interaction: https://doi.org/10.1016/j.jbef.2026.101183
- Human vs automated signals: https://doi.org/10.1108/SEF-12-2025-0942
- Dallas Fed WP 2605: https://www.dallasfed.org/research/papers/2026/wp2605
- Trading periodicity: https://doi.org/10.1002/fut.70089


## Public forecast-ledger check — 2026-11-14

| System | Public evidence checked | Asset / horizon | Reproducibility and caveats | Shadow-board decision |
|---|---|---|---|---|
| CoinPredict | Public track record reports 6,710 graded 24h calls across assets, 54% directional accuracy and 83% in its 80% range; BTC page reports 18 graded BTC 24h calls, 56% direction, 77.8% in-range and 0.9% median base-case miss. Methodology describes a volatility range model plus a cross-coin gradient-boosted direction model; hourly signals are a separate model. | BTC 24h and other horizons; separate 1h calls | Public, versioned ledger and methodology. BTC sample is only 18 calls. Latest BTC 24h snapshot visible is model 1d-20261105-0358, made 2026-11-11 00:00 UTC and expiring 2026-11-12; page updated 2026-11-12 06:30 UTC. No current 24-step hourly path. | Best current public-ledger candidate for future terminal-price comparison, but not comparable to the 2026-11-14 issue time. No rank assigned. |
| Satori Signals | Accuracy page reports BTC last-30-days 237 forecasts, 50.6% direction, 1.07% average error (same as no-change baseline), and 75.5% inside the network's central 80% range; checked on 11 days. | BTC next 24h crowd consensus | Public accuracy summary, but only 11 checked days in the displayed 30-day period; landing-page sample is stale. Full forecasts require holding 1,000 SATORIEVR or paying $5/month. No token, payment or account was used. | Track read-only as crowd benchmark; not eligible for participation or ranking. |
| SignalTrace Lab | Public 24h page displays 47.0% up / 53.0% down, historical upward frequency 48.2%, 2,536 historical comparisons, and explicitly labels it an uncalibrated baseline. Opened page edition is 2026-11-10, reference time 2026-11-10 00:00 UTC; search index showed a newer-looking snippet, so the page itself was treated as authoritative. | BTC 24h direction probability | No current calibrated probability error or preserved price path in the checked page. Stale at review time and not a price-path forecast. | Unranked, stale probability reference only. |
| BitPredict | BTC 24h page describes timestamped UP/DOWN member calls, free participation and public accuracy leaderboard; the displayed member split is 71% UP / 29% DOWN as of 2026-11-02 15:39 UTC (87 calls). | BTC 24h binary human/member calls | The displayed split is stale and is not a current model forecast. Account registration is required to submit; automated-participation terms were not verified. | No submission or account creation. Keep as a human-crowd watchlist candidate. |
| CoinPredict current homepage / cached snippets | Search snippet and live page disagreed: the snippet displayed a populated hourly board, while the opened page showed “no call this hour” and “waiting for first market snapshot”; the separate track-record page was populated. | BTC and multi-asset hourly / 24h | Dynamic/cached page inconsistency; rely only on the opened, versioned track-record and methodology pages, not the conflicting homepage snippet. | Preserve discrepancy in audit notes; do not infer a current BTC hourly signal. |
| Coinbase prediction markets | Public page showed BTC hourly/15-minute threshold contracts and implied probabilities, including a Nov 14 contract snapshot. | Event thresholds, not full price paths | Market-implied probabilities include liquidity/market-price effects and are not a forecasting model or a fixed 24-hour BTC close. No trading or order placement. | Possible read-only market-implied event benchmark, not model leaderboard. |

### Source URLs (checked 2026-11-14)

- CoinPredict track record: https://coinpredict.net/track-record
- CoinPredict BTC forecast: https://coinpredict.net/price-prediction/bitcoin
- CoinPredict methodology: https://coinpredict.net/methodology
- Satori accuracy: https://satorisignals.app/accuracy
- Satori forecasts/access: https://satorisignals.app/forecasts
- SignalTrace BTC outlook: https://signaltracelab.com/en/bitcoin/
- BitPredict BTC next 24h: https://www.bitpredict.io/predictions/bitcoin/next-24-hours
- Coinbase prediction markets: https://www.coinbase.com/predictions/crypto/BTC/Hourly

No external forecast is scored against LFM until the exact asset/venue, issue time, information cutoff, expiry convention and target path can be aligned. A crowd percentage, market-implied event probability or backtest aggregate is not interchangeable with an hourly price path.
