# C12 Privacy Protection & Personal Data Management

## Control Objective

Maintain rigorous privacy assurances across the entire AI lifecycle (collection, training, inference, and incident response) so that personal data is only processed with clear consent, minimum necessary scope, provable erasure, and formal privacy guarantees. This chapter focuses on AI-specific privacy concerns: privacy properties of training data and derived model artifacts, deletion and unlearning across ML artifacts, differential privacy budget management for training, purpose binding for datasets and models, consent-aware inference gating, and federated-learning privacy controls.

---

## C12.1 Anonymization & Data Minimization

Remove or transform personal identifiers before training to prevent re-identification and minimize privacy exposure.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.1.1** | **Verify that** direct and quasi-identifiers in training and fine-tuning datasets are removed, hashed, or generalized before the data is used to fit or update a model. | 1 |
| **12.1.2** | **Verify that** automated audits measure k-anonymity or l-diversity on training datasets and alert when thresholds drop below policy. | 2 |
| **12.1.3** | **Verify that** model feature-importance or attribution analyses are run on trained models to confirm that no removed identifier or quasi-identifier has been reconstructed as a high-importance feature. | 2 |
| **12.1.4** | **Verify that** formal proofs or synthetic-data certification show re-identification risk against trained models remains below a documented policy threshold even under linkage attacks. | 3 |

---

## C12.2 Right-to-be-Forgotten & Deletion Enforcement

Ensure data-subject deletion requests propagate across all AI artifacts and that model unlearning is verifiable.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.2.1** | **Verify that** data-subject deletion requests propagate to AI-derived artifacts including training and fine-tuning datasets, model checkpoints, evaluation sets, derived caches, and feature stores within a service level agreement of less than 30 days. Embedding and RAG index propagation is governed by C8.3. | 1 |
| **12.2.2** | **Verify that** shadow-model or membership-inference evaluation demonstrates that forgotten records influence less than a documented policy threshold of model outputs after unlearning. | 2 |
| **12.2.3** | **Verify that** machine-unlearning routines, when claimed, either physically retrain the affected model on the retained data or apply a certified unlearning algorithm with documented (ε, δ) guarantees. | 3 |

---

## C12.3 Differential-Privacy Safeguards

Track and enforce privacy budgets to provide formal guarantees against individual data leakage.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.3.1** | **Verify that** differential privacy budget consumption (both ε and δ values) is tracked and recorded per training round, and that cumulative consumption triggers an alert when ε exceeds defined policy thresholds. | 2 |
| **12.3.2** | **Verify that** black-box privacy audits empirically estimate ε̂ as a lower bound at a stated confidence level (e.g., Clopper-Pearson or f-DP confidence intervals), and that the estimate is consistent with the declared budget within documented tolerance. | 2 |
| **12.3.3** | **Verify that** formal privacy proofs cover all post-training fine-tunes and embedding generation steps that consume the same source data. | 3 |

---

## C12.4 Purpose-Limitation & Scope-Creep Protection

Prevent models and datasets from being used beyond their originally consented purpose.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.4.1** | **Verify that** every dataset and model checkpoint carries a machine-readable purpose tag aligned to the original consent and lawful basis under which the source data was collected. | 1 |
| **12.4.2** | **Verify that** runtime monitors detect queries inconsistent with the declared purpose of the dataset or model, and that detected queries trigger a soft refusal or are blocked pending review. | 1 |
| **12.4.3** | **Verify that** policy-as-code gates block redeployment of models to new domains without DPIA review. | 3 |
| **12.4.4** | **Verify that** formal traceability proofs show every personal data lifecycle remains within consented scope. | 3 |

---

## C12.5 Consent Management & Lawful-Basis Tracking

Enforce consent at AI-specific decision points (training data ingestion, inference) and propagate withdrawal across AI artifacts.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.5.1** | **Verify that** model inference validates consent scope before processing and refuses or downgrades the response when the scope does not cover the requested operation, the data subjects whose data materially influences the response, or both. | 2 |
| **12.5.2** | **Verify that** withdrawal of consent triggers the same AI-artifact propagation pipeline as a deletion request (see 12.2.1), and that inference paths relying on the withdrawn data are disabled within the same SLA. | 2 |

---

## C12.6 Federated Learning with Privacy Controls

Apply differential privacy and privacy auditing to federated learning to protect individual participant data.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.6.1** | **Verify that** client updates apply local differential privacy noise addition before aggregation, or that a documented central differential privacy mechanism is enforced at the aggregator. | 1 |
| **12.6.2** | **Verify that** training metrics shared with the aggregator or with clients are differentially private and never reveal single-client loss or single-client gradients. | 2 |
| **12.6.3** | **Verify that** federated learning systems implement canary-based privacy auditing to empirically bound privacy leakage, with audit results logged and reviewed per training cycle. | 3 |
| **12.6.4** | **Verify that** formal proofs document the overall ε budget and the corresponding utility loss against a declared baseline. | 3 |

---

## References

* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [General Data Protection Regulation (GDPR)](https://gdpr-info.eu/)
* [California Consumer Privacy Act (CCPA)](https://oag.ca.gov/privacy/ccpa)
* [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
