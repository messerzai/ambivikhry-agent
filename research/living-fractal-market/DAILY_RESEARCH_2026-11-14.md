# Daily research log — 2026-11-14

Branch: research/living-fractal-market  
Review cutoff: 2026-11-14T07:18:16Z  
Scope: BTC/USDT Binance Spot 5m inputs, hourly target grid; no trading execution.

## Research reviewed

### 1. Recurrence Quantification Analysis in cryptocurrency markets

Vanheusden, F. J., Kim, A., Almeida, T. P., Soriano, D. C., Verousis, T. (2026), “Nonlinear dynamics in cryptocurrency markets: a recurrence quantification analysis approach,” Financial Innovation 12, article 127, published 2026-06-03. DOI: https://doi.org/10.1186/s40854-026-00940-x

Original article: https://link.springer.com/article/10.1186/s40854-026-00940-x

Methods and reported evidence:
- RQA applied to 100 cryptocurrencies using CoinLore USD closing-price data through 2025-04-19.
- Return series were normalized and wavelet-denoised; RQA parameters include embedding dimension, delay and recurrence threshold.
- A volatility-warning experiment used daily RQA statistics, 80-day rolling windows and 5–50 day forecast horizons. The determinism/laminarity ratio was strongest at 42 days; reported AUROC 0.605 and predictive-regression coefficient about 0.081 with bootstrap interval [0.058, 0.10].
- Authors emphasize parameter sensitivity and show that threshold choices can create spurious recurrence structures.

Limitations relevant to LFM:
- The study does not establish 24-hour BTC point-price skill.
- It explicitly did not compare RQA against MFDFA in this paper, did not explore the full parameter space or provide an objective parameter-selection algorithm, and notes that daily versus hourly sampling should be investigated.
- Data are available from the corresponding author on reasonable request, not as a directly reproducible public dataset in the article.
- A moderate AUROC for multi-day volatility warnings is not a directional BTC forecast.

Research decision: add RQA as a volatility/regime diagnostic challenger only. Test fixed-recurrence-rate settings against parameter sweeps and finite-sample/block-shuffle nulls; evaluate incremental value over realized-volatility and MF-DFA baselines before any model integration.

### 2. Social network and sentiment contagion in Bitcoin

Han, B., Liu, H., Sui, P. (2026-03-02), “Social Network and Sentiment Contagion: Evidence from the Bitcoin Market,” Federal Reserve Bank of Dallas Working Paper 2605. DOI: https://doi.org/10.24149/wp2605

Original source: https://www.dallasfed.org/research/papers/2026/wp2605

Methods and reported evidence:
- Uses social-interaction data and individual Bitcoin trading records.
- Peer sentiment shifts investors’ beliefs toward average peer sentiment, with patterns consistent with confirmation bias.
- The authors report that peer sentiment itself does not predict future BTC prices, while a measure of sentiment-contagion intensity forecasts volatility, trading volume and market crashes.

Limitations:
- This is a working paper, not treated here as a peer-reviewed final result.
- The data construction and availability need further audit; the abstract describes novel linked social/trading records, not a readily downloadable point-in-time dataset.
- The reported result concerns volatility, volume and crash risk, not a demonstrated 24-hour price path forecast.

Research decision: do not add a simple positive/negative sentiment score as a price-direction feature on the strength of this paper. A network-contagion intensity feature is a separate volatility-risk hypothesis and requires timestamped interaction data, point-in-time controls and an ablation against volatility-only baselines.

### 3. Collective criticality and cross-asset tail synchronization

Zouari, M., Alon, I., Shtudiner, Z. (2026), “Heterogeneous collective criticality in cryptocurrency volatility: Scaling collapse, tail synchronization, and cascade amplification,” Chaos, Solitons & Fractals, volume 211, article record DOI https://doi.org/10.1016/j.chaos.2026.118809.

Abstract record checked: https://econpapers.repec.org/article/eeechsofr/v_3a211_3ay_3a2026_3ai_3ap1_3as0960077926009501.htm  
Publisher full text endpoint returned HTTP 403 in this review; detailed methods and data could not be independently inspected.

Abstract-level claims:
- BTC, ETH and SOL volatility are examined with daily and hourly data.
- The abstract describes Bitcoin as boundary-adjacent, with a circular-block interval crossing CR=1, and reports cross-asset tail synchronization and short-horizon cascade amplification.
- It reports a common clustering scaling exponent near 0.31 and comparisons against circular-shift, block-shuffle and factor-residual null envelopes.

Limitations:
- Full text and exact sample dates/data provenance were not available in this review; treat the abstract as a discovery lead rather than a replicated finding.
- The paper studies volatility-system diagnostics, not a proven directional price model.
- No source code or dataset was copied.

Research decision: a cross-asset volatility/tail-synchronization challenger may be tested only after the exact paper, sample, estimator and null-model details are audited. Do not treat “criticality” as a market law.

## External benchmark discovery

SOTA2 “Univariate Time-series Forecasting on Exchange (test)”:
https://www.sota2.com/research/sota/univariate-time-series-forecasting-on-exchange-test

The page lists zero-shot rows including Cross-RAG (MSE 0.064, MAE 0.175), TTM (0.066, 0.173), Moirai (0.066, 0.172), Chronos-bolt (0.067, 0.178), TimesFM (0.070, 0.180), Chronos (0.083, 0.188), Time-MoE (0.085, 0.206), MOMENT (0.098, 0.206), ARIMA (0.112, 0.245), N-HITS (0.114, 0.248) and N-BEATS (0.156, 0.299). The page says it was updated about eight months before this check.

This is a general Exchange-dataset benchmark, not a BTC/USD hourly benchmark. The visible page does not establish matching venue, quote currency, target timestamps or point-in-time BTC origins. It is a model-discovery source only; no scores are transferred to our leaderboard.

## Live daily workflow — verified

- Trigger commit: d8e817969f82c19d17ad4c8bd5b219e6fed2360e.
- Workflow: https://github.com/messerzai/ambivikhry-agent/actions/runs/43570452838
- Workflow result: success.
- Artifact ID: 14103948071.
- Artifact upload and live Binance public-data retrieval succeeded.
- Data source: https://data-api.binance.vision/api/v3/klines
- Symbol BTCUSDT, Binance Spot, 5m interval.
- 999 closed candles; cutoff 2026-11-14T07:14:59.999Z; issue time 2026-11-14T07:18:16.591141Z; reference 67,411.00 USDT.
- Seven models produced 24 hourly target points each: RandomWalk, Momentum5m, MeanReversion5m, VolatilityRegime5m, TakerFlow5m, DownsideStress5m, LFM5mEnsemble.
- Exact artifact archive: forecasts/2026-11-14/2026-11-14T07-18-16.591141Z_BTCUSDT_BinanceSpot_LFM-5m-0.4.artifact.zip
- Exact artifact ZIP SHA-256: 64575163aa3c274adca5a134e02b394d524e73f8861bef632ee88c7cad4ffa2d.
- Extracted original forecast JSON SHA-256: de5b1c4f52cccedfb8f071eb820c705f4d82f5b5f00273e42d88a2f43239512c.
- The forecast is a BTC/USDT 5m-input/hourly-target challenger, not a BTC/USD champion.
- P90 intervals are Gaussian-style approximations and uncalibrated; no 50% interval was issued.
- The reference price was already below 70,000 USDT. The 0.9597 heuristic is an uncalibrated terminal-state estimate, not a first-passage or crossing probability.

## CI and engineering change

The dedicated LFM workflow passed its offline unit-test step (11/11), live-data retrieval, forecast generation and artifact upload.

The repository-wide tests workflow initially failed before pytest at pip install -e .: setuptools refused ambiguous flat-layout discovery of top-level directories chess, research and ambivikhry. This is a packaging-discovery issue, not a forecast-model test failure. A branch-only pyproject.toml fix now explicitly includes ambivikhry* and excludes unrelated top-level folders. A fresh repository-wide CI run was queued after that fix; its final result is recorded in the conversation report, not assumed here.

## Forecast evaluation and leaderboard

- The 2026-11-12 vintage target window has closed, but the exact 24 Binance Spot 1h target candles were not retrieved; evaluation is deferred.
- Both 2026-11-13 vintages were still pending their final target close at the 2026-11-14 07:18 UTC cutoff.
- The 2026-11-14 vintage is pending through its final target close at 2026-11-15T07:59:59.999Z.
- No comparable external BTC/USD 24-step hourly path was found.
- Completed independent daily vintages: 0 for champion-promotion purposes.
- Virtual research points: 0.
- No champion promotion; all seven 5m council models remain challengers.

## Next experiment

1. Build a 90-day paginated Binance Spot 5m data archive with immutable raw-response provenance and strict UTC/freshness/continuity checks.
2. Add hourly candle reconstruction from the 5m archive and compare against native Binance 1h candles.
3. Add a seasonal baseline by hour-of-week before testing RQA or microstructure features.
4. Test RQA volatility diagnostics with predeclared windows, fixed-recurrence-rate and parameter-sweep variants, circular/block-shuffle nulls, and no-lookahead rolling evaluation.
5. Test cross-asset tail synchronization only after auditing the full 2026 criticality paper and collecting aligned BTC/ETH/SOL spot data.
6. Keep network-sentiment contagion out of the model until a lawful, timestamped and reproducible graph-level dataset exists.
7. Fix forecast JSON schema to include a stable vintage_id and retrieved_at_utc; distinguish calibrated prediction intervals from heuristic Gaussian bands.
8. Retrieve exact historical Binance 1h closes for the completed Nov 12 vintage and score it against random walk and volatility-aware baselines.

No trades, orders, account connections or transfers were made. Research only; not financial advice.
