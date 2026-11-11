# Third-party reuse and license register

Branch: research/living-fractal-market  
Last reviewed: 2026-11-11

No third-party code, model weights, datasets, tokenizers or media assets were copied into this branch in this review. The entries below are audited candidates only. Repository code and model weights are separate license objects; model-hub cards were checked on 2026-11-11 but must be pinned to immutable model revisions before any download or reuse.

| Component | Immutable source/version checked | Code license | Weights / data terms | Reused components and notices | Status |
|---|---|---|---|---|---|
| Amazon Chronos-2 | Code HEAD 1224fafa91e1ecd6674f5204066b159e40b5e4a1; https://github.com/amazon-science/chronos-forecasting. Model card: https://huggingface.co/amazon/chronos-2 | Apache-2.0; LICENSE inspected | HF model card lists Apache-2.0 for amazon/chronos-2; pin HF revision before use. Training datasets are separate provenance objects. | None. If reused, retain Apache-2.0 LICENSE/copyright notices and record exact paths/checkpoint revision. | Candidate only; no code or weights copied |
| Google TimesFM source | HEAD e51928e27119cb17bebc005be2696b75e0a9e688; https://github.com/google-research/timesfm | Apache-2.0; LICENSE inspected | See separate checkpoint rows below | None. Preserve source LICENSE and notices if reused. | Candidate only |
| Google TimesFM 2.5 weights | https://huggingface.co/google/timesfm-2.5-200m-pytorch | N/A (model card) | HF card lists Apache-2.0; model card says checkpoint is not an officially supported Google product. Pin exact HF revision before use. | None. Preserve model-card attribution and Apache-2.0 notices. | Candidate; no weights copied |
| Google TimesFM 3.0 weights | https://huggingface.co/google/timesfm-3.0-pytorch | N/A (model card) | timesfm-non-commercial-license-v1.0; distinct from Apache-2.0 source code and TimesFM 2.5 weights. Current card identifies this as the weight license. Commercial/production use is not allowed under the checked terms. | None. Do not use in a paid or production product under current terms; legal review required for any intended research deployment. | Excluded from commercial/production use; no weights copied |
| Nixtla NeuralForecast | HEAD a5e396e39c4f320883eaac5338aa1d3c953d1344; https://github.com/Nixtla/neuralforecast | Apache-2.0; LICENSE inspected | Library supplies implementations, not a universal pretrained weight license. Training data and any resulting checkpoint require their own provenance review. | None. If reused, preserve Apache-2.0 notice. | Candidate only |
| FoundationForecast | HEAD c32ad5da4d7fb304e98423b07ac32b8ad2cf632b; https://github.com/TimeCopilot/foundationforecast | Apache-2.0; LICENSE inspected | Each integrated foundation model/checkpoint has its own license and data terms. | None. Preserve Apache-2.0 notice if framework code is reused; separately audit every adapter/model. | Candidate only |
| Benchstreet | HEAD 4c5e7c0d2c520788b908125ca0e6abad0deb5dd9; https://github.com/puffinsoft/benchstreet | MIT; LICENSE inspected. Copyright notice: ColonelParrot, 2025 | Fine-tuned TimesFM/Chronos checkpoints are hosted separately; their model-card licenses were not audited and no weights are reused. README says S&P 500 daily data and explicitly says this is not an objective benchmark. | None. If code is reused, include MIT copyright and permission notice. | Reference only; no code or weights copied |
| CrunchDAO crunch-synth | HEAD 679dfc2211a0a41ef255ada5f0a12c38a9e923e9 (v0.16.0); https://github.com/crunchdao/crunch-synth | No root LICENSE or LICENSE.md found at checked commit; no license inferred from public availability | Competition data, platform terms and participant obligations are separate and were not accepted or copied. | None. Do not copy code until a clear license is supplied. Public methodology may be studied and independently implemented with citation. | No code copied; methodology-only reference |
| CryptoOracle | https://github.com/moinsen-dev/crypto-oracle | README states no project-wide software license has been granted | Model weights and dependencies retain their own licenses; no third-party weights copied | None | Public ledger/reference only; no code copied |
| Unofficial sanjmen/crunch-synth | HEAD aa12238b5a29a1d82c884927bffafc0b468e76c9; https://github.com/sanjmen/crunch-synth | No LICENSE file found; README badge alone is not a license grant | Unverified | None | Not official CrunchDAO repo; no code copied |

## Reuse decisions in this run

- No third-party source files, model weights, datasets, tokenizers or other assets were copied.
- Chronos-2 is the preferred first foundation-model challenger because both the official source repository and the model card identify Apache-2.0; pin the HF revision before use.
- TimesFM 2.5 remains a candidate under Apache-2.0 for both source and checked weights.
- TimesFM 3.0 is excluded from commercial/production reuse because its weight license differs from its Apache-2.0 source code.
- CrunchDAO's competition methodology is useful for a future density/CRPS shadow experiment, but no code is copied because no repository LICENSE was found at the checked v0.16.0 commit.
- Benchstreet's MIT code is reusable in principle with notices, but its reported S&P 500 daily results are not BTC hourly evidence; no implementation was copied.
- CryptoOracle is used only as a public evidence source; its repository README expressly says it has no project-wide software license.

## Required review before each reuse

1. Pin an immutable source commit, release, model-hub revision or dataset version.
2. Read the actual LICENSE and any NOTICE, model card, dataset card, gated-access agreement and terms of use.
3. Identify separate licenses for code, weights, training data, benchmark data, tokenizers and APIs.
4. Check commercial/non-commercial limits, attribution, redistribution, modification, patent grants, copyleft, network-use clauses and source-disclosure obligations.
5. Record exact reused paths, modifications, dependency versions, copyright notices and required attribution.
6. If terms are absent or ambiguous, do not copy. Implement independently from cited public research instead.
7. Re-audit before distributing binaries, checkpoints, containers, hosted services or paid products.

This register is an engineering provenance checklist, not a legal opinion. Ambiguous or high-impact licensing questions require qualified review.
