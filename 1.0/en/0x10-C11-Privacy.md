# 11 Privacy Protection & Personal Data Management

## Control Objective

Maintain rigorous privacy assurances across the entire AI lifecycle—collection, training, inference, and incident response—so that personal data is only processed with clear consent, minimum necessary scope, provable erasure, and formal privacy guarantees.

---

## 11.1 Anonymization & Data Minimization

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.1.1** | **Verify that** direct and quasi-identifiers are removed, hashed. | 1 | D/V |
| **11.1.2** | **Verify that** automated audits measure k-anonymity/l-diversity and alert when thresholds drop below policy. | 2 | D/V |
| **11.1.3** | **Verify that** model feature-importance reports prove no identifier leakage beyond ε = 0.01 mutual information. | 2 | V |
| **11.1.4** | **Verify that** formal proofs or synthetic-data certification show re-identification risk ≤ 0.05 even under linkage attacks. | 3 | V |

---

## 11.2 Right-to-be-Forgotten & Deletion Enforcement

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.2.1** | **Verify that** data-subject deletion requests propagate to raw datasets, checkpoints, embeddings, logs, and backups within service level agreements of less than 30 days. | 1 | D/V |
| **11.2.2** | **Verify that** "machine-unlearning" routines physically re-train or approximate removal using certified unlearning algorithms. | 2 | D |
| **11.2.3** | **Verify that** shadow-model evaluation proves forgotten records influence less than 1% of outputs after unlearning. | 2 | V |
| **11.2.4** | **Verify that** deletion events are immutably logged and auditable for regulators. | 3 | V

---

## 11.3 Differential-Privacy Safeguards

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.3.1** | **Verify that** privacy-loss accounting dashboards alert when cumulative ε exceeds policy thresholds. | 2 | D/V |
| **11.3.2** | **Verify that** black-box privacy audits estimate ε̂ within 10% of declared value. | 2 | V |
| **11.3.3** | **Verify that** formal proofs cover all post-training fine-tunes and embeddings. | 3 | V |

---

## 11.4 Purpose-Limitation & Scope-Creep Protection

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.4.1** | **Verify that** every dataset and model checkpoint carries a machine-readable purpose tag aligned to the original consent. | 1 | D |
| **11.4.2** | **Verify that** runtime monitors detect queries inconsistent with declared purpose and trigger soft refusal. | 1 | D/V |
| **11.4.3** | **Verify that** policy-as-code gates block redeployment of models to new domains without DPIA review. | 3 | D |
| **11.4.4** | **Verify that** formal traceability proofs show every personal data lifecycle remains within consented scope. | 3 | V |

---

## 11.5 Consent Management & Lawful-Basis Tracking

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.5.1** | **Verify that** a Consent-Management Platform (CMP) records opt-in status, purpose, and retention period per data-subject. | 1 | D/V |
| **11.5.2** | **Verify that** APIs expose consent tokens; models must validate token scope before inference. | 2 | D |
| **11.5.3** | **Verify that** denied or withdrawn consent halts processing pipelines within 24 hours. | 2 | D/V |

---

## 11.6 Federated Learning with Privacy Controls

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.6.1** | **Verify that** client updates employ local differential privacy noise addition before aggregation. | 1 | D |
| **11.6.2** | **Verify that** training metrics are differentially private and never reveal single-client loss. | 2 | D/V |
| **11.6.3** | **Verify that** poisoning-resistant aggregation (e.g., Krum/Trimmed-Mean) is enabled. | 2 | V |
| **11.6.4** | **Verify that** formal proofs demonstrate overall ε budget with less than 5 utility loss. | 3 | V |

---

### References
