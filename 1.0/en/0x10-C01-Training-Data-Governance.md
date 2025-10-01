# C1 Training Data Governance & Bias Management

## Control Objective

Training data must be sourced, handled, and maintained in a way that preserves provenance, security, quality, and fairness. Doing so fulfils legal duties and reduces risks of bias, poisoning, or privacy breaches that show up during training that could effect the entire AI lifecycle.

---

## C1.1 Training Data Provenance

Maintain a verifiable inventory of all datasets, accept only trusted sources, and log every change for auditability.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.1.1** | **Verify that** an up-to-date inventory of every training-data source (origin, steward/owner, licence, collection method, intended use constraints, and processing history) is maintained. | 1 | D/V |
| **1.1.2** | **Verify that** training data processes exclude unnecessary features, attributes, or fields (e.g., unused metadata, sensitive PII, leaked test data). | 1 | D/V |
| **1.1.3** | **Verify that** all dataset changes are subject to a logged approval workflow. | 2 | D/V |
| **1.1.4** | **Verify that** datasets or subsets are watermarked or fingerprinted where feasible. | 3 | D/V |

---

## C1.2 Training Data Security & Integrity

Restrict access to training data, encrypt it at rest and in transit, and validate its integrity to prevent tampering, theft, or data poisoning.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.2.1** | **Verify that** access controls protect training data storage and pipelines. | 1 | D/V |
| **1.2.2** | **Verify that** all access to training data is logged, including user, time, and action. | 2 | D/V |
| **1.2.3** | **Verify that** training datasets are encrypted in transit and at rest, using industry-standard cryptographic algorithms and key management practices. | 2 | D/V |
| **1.2.4** | **Verify that** cryptographic hashes or digital signatures are used to ensure data integrity during training data storage and transfer. | 2 | D/V |
| **1.2.5** | **Verify that** that automated detection techniques are applied to guard against unauthorized modifications or corruption of training data. | 2 | D/V |
| **1.2.6** | **Verify that** obsolete training data is securely purged or anonymized. | 2 | D/V |
| **1.2.7** | **Verify that** all training dataset versions are uniquely identified, stored immutably, and auditable to support rollback and forensic analysis. | 3 | D/V |

---

## C1.3 Training Data Labeling Quality, Integrity, and Security

Protect labels and require technical review for critical data.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.3.1** | **Verify that** cryptographic hashes or digital signatures are applied to label artifacts to ensure their integrity and authenticity. | 2 | D/V |
| **1.3.2** | **Verify that** labeling interfaces and platforms enforce strong access controls, maintain tamper-evident audit logs of all labeling activities, and protect against unauthorized modifications. | 2 | D/V |
| **1.3.3** | **Verify that** sensitive information in labels is redacted, anonymized, or encrypted at the data field level at rest and in transit.| 3 | D/V |

---

## C1.4 Training Data Quality and Security Assurance

Combine automated validation, manual spot-checks, and logged remediation to guarantee dataset reliability.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.4.1** | **Verify that** automated tests catch format errors and nulls on every ingest or significant data transformation. | 1 | D |
| **1.4.2** | **Verify that** LLM training and fine-tuning pipelines implement poisoning detection & data integrity validation (e.g., statistical methods, outlier detection, embedding analysis) to identify potential poisoning attacks (e.g., label flipping, backdoor trigger insertion, role-switching commands, influential instance attacks) or unintentional data corruption in training data. | 2 | D/V |
| **1.4.3** | **Verify that** automatically generated labels (e.g., via LLMs or weak supervision) are subject to confidence thresholds and consistency checks to detect hallucinated, misleading, or low-confidence labels. | 2 | D/V |
| **1.4.4** | **Verify that** appropriate defenses, such as adversarial training (using generated adversarial examples), data augmentation with perturbed inputs, or robust optimization techniques, are implemented and tuned for relevant models based on risk assessment. | 3 | D/V |
| **1.4.5** | **Verify that** automated tests catch label skews on every ingest or significant data transformation. | 3 | D |

---

## C1.5 Data Lineage and Traceability

Track the full journey of each data point from source to model input for auditability and incident response.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.5.1** | **Verify that** the lineage of each data point, including all transformations, augmentations, and merges, is recorded and can be reconstructed. | 2 | D/V |
| **1.5.2** | **Verify that** lineage records are immutable, securely stored, and accessible for audits. | 2 | D/V |
| **1.5.3** | **Verify that** lineage tracking covers synthetic data generated via privacy-preserving or generative techniques and that all synthetic data is clearly labeled and distinguishable from real data throughout the pipeline. | 2 | D/V |

---

## References

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [EU AI Act – Article 10: Data & Data Governance](https://artificialintelligenceact.eu/article/10/)
* [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
* [OpenAI Privacy Center – Data Deletion Controls](https://privacy.openai.com/policies?modal=take-control)
