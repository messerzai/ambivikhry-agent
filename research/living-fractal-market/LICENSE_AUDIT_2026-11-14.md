# Third-party license audit — 2026-11-14

Branch: research/living-fractal-market

## Reuse performed

No third-party code, model weights, datasets, tokenizers, figures, media assets or benchmark artifacts were copied or redistributed in this cycle. No new third-party runtime dependency was added.

## Sources and terms checked

| Source | Terms / status | Files or components reused | Decision |
|---|---|---|---|
| Vanheusden et al. (2026), Financial Innovation, DOI 10.1186/s40854-026-00940-x | Article record identifies Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0). The article is not treated as a license for derivative code or figures. | None. Only bibliographic facts and a high-level research summary are recorded with citation. | No text, figure, table, code or dataset copied or adapted. A future RQA implementation must be clean-room based on standard RQA literature and independently tested. |
| Han, Liu & Sui (2026), Dallas Fed Working Paper 2605 | Public working-paper page and DOI inspected. No software/data reuse license was established in this review. | None. Only the public abstract and citation are summarized. | No paper text, data, code or implementation copied. Dataset availability and terms require separate audit before use. |
| Zouari, Alon & Shtudiner (2026), Chaos, Solitons & Fractals, DOI 10.1016/j.chaos.2026.118809 | Abstract record inspected through RePEc; publisher full text returned HTTP 403. Exact article license and supplementary-data terms were not verified. | None. | No text, code, figures, weights or data copied. Treat as a discovery lead until full terms and methods are available. |
| SOTA2 Exchange benchmark | Public benchmark page inspected; no benchmark code, model artifact or dataset downloaded. | None. | Scores are cited only as non-BTC model-discovery evidence; no benchmark data copied. |

## Internal change

The pyproject.toml package-discovery correction is an internal project configuration change. It adds no external code or dependency and does not change the forecast models.

This is an engineering provenance note, not a legal opinion. Any future reuse requires an immutable source revision, exact code license, separate model-weight and dataset terms, preserved notices, and review of attribution, modification, redistribution, commercial restrictions and copyleft/network-use obligations.
