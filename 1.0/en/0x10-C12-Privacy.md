# C12 Privacy Protection & Personal Data Management

## Control Objective

Maintain rigorous privacy assurances across the entire AI lifecycle (collection, training, inference, and incident response) so that personal data is only processed with clear consent, minimum necessary scope, provable erasure, and formal privacy guarantees.

---

## C12.1 Anonymization & Data Minimization

Remove or transform personal identifiers before training to prevent re-identification and minimize privacy exposure.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.1.1** | **Verify that** direct and quasi-identifiers are removed, hashed. | 1 | D/V |
| **12.1.2** | **Verify that** automated audits measure k-anonymity/l-diversity and alert when thresholds drop below policy. | 2 | D/V |
| **12.1.3** | **Verify that** model feature-importance reports prove no identifier leakage beyond ε = 0.01 mutual information. | 2 | V |
| **12.1.4** | **Verify that** formal proofs or synthetic-data certification show re-identification risk ≤ 0.05 even under linkage attacks. | 3 | V |

---

## C12.2 Right-to-be-Forgotten & Deletion Enforcement

Ensure data-subject deletion requests propagate across all AI artifacts and that model unlearning is verifiable.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.2.1** | **Verify that** data-subject deletion requests propagate to raw datasets, checkpoints, embeddings, logs, and backups within service level agreements of less than 30 days. | 1 | D/V |
| **12.2.2** | **Verify that** "machine-unlearning" routines physically re-train or approximate removal using certified unlearning algorithms. | 2 | D |
| **12.2.3** | **Verify that** shadow-model evaluation proves forgotten records influence less than 1% of outputs after unlearning. | 2 | V |
| **12.2.4** | **Verify that** deletion events are immutably logged and auditable for regulators. | 3 | V |

---

## C12.3 Differential-Privacy Safeguards

Track and enforce privacy budgets to provide formal guarantees against individual data leakage.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.3.1** | **Verify that** differential privacy budget consumption is tracked per training round (both ε and δ values) and that cumulative budget dashboards alert when ε exceeds policy thresholds. | 2 | D/V |
| **12.3.2** | **Verify that** black-box privacy audits estimate ε̂ within 10% of declared value. | 2 | V |
| **12.3.3** | **Verify that** formal proofs cover all post-training fine-tunes and embeddings. | 3 | V |
| **12.3.4** | **Verify that** federated learning systems implement canary-based privacy auditing to empirically bound privacy leakage, with audit results logged and reviewed per training cycle. | 3 | V |

---

## C12.4 Purpose-Limitation & Scope-Creep Protection

Prevent models and datasets from being used beyond their originally consented purpose.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.4.1** | **Verify that** every dataset and model checkpoint carries a machine-readable purpose tag aligned to the original consent. | 1 | D |
| **12.4.2** | **Verify that** runtime monitors detect queries inconsistent with declared purpose and trigger soft refusal. | 1 | D/V |
| **12.4.3** | **Verify that** policy-as-code gates block redeployment of models to new domains without DPIA review. | 3 | D |
| **12.4.4** | **Verify that** formal traceability proofs show every personal data lifecycle remains within consented scope. | 3 | V |

---

## C12.5 Consent Management & Lawful-Basis Tracking

Record, enforce, and revoke consent across AI processing pipelines.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.5.1** | **Verify that** a Consent-Management Platform (CMP) records opt-in status, purpose, and retention period per data-subject. | 1 | D/V |
| **12.5.2** | **Verify that** APIs expose consent tokens; models must validate token scope before inference. | 2 | D |
| **12.5.3** | **Verify that** denied or withdrawn consent halts processing pipelines within 24 hours. | 2 | D/V |

---

## C12.6 Federated Learning with Privacy Controls

Apply differential privacy and poisoning-resistant aggregation to federated learning to protect individual participant data.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.6.1** | **Verify that** client updates employ local differential privacy noise addition before aggregation. | 1 | D |
| **12.6.2** | **Verify that** training metrics are differentially private and never reveal single-client loss. | 2 | D/V |
| **12.6.3** | **Verify that** poisoning-resistant aggregation (e.g., Krum/Trimmed-Mean) is enabled. | 2 | V |
| **12.6.4** | **Verify that** formal proofs demonstrate overall ε budget with less than 5 utility loss. | 3 | V |

---

## References

* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [General Data Protection Regulation (GDPR)](https://gdpr-info.eu/)
* [California Consumer Privacy Act (CCPA)](https://oag.ca.gov/privacy/ccpa)
* [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
