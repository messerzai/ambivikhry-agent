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
