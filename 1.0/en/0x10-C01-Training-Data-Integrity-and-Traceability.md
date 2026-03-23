# C1 Training Data Integrity & Traceability

## Control Objective

Training data must be sourced, handled, and maintained in a way that preserves origin traceability, integrity, and quality. The core security concern is ensuring data has not been tampered with, poisoned, or corrupted. Security-relevant bias (e.g., skewed abuse-detection training data that allows attackers to bypass controls) is treated as a possible consequence of compromised or unvalidated data, not as a standalone control category.

> **Scope note — bias.** AISVS addresses bias only where it introduces security risk (e.g., bypass of abuse detection, authentication heuristics, or automated trust decisions). Broader fairness governance requirements are out of scope; see ISO/IEC 42001 or the NIST AI RMF for general fairness and ethics guidance.

---

## C1.1 Training Data Origin & Traceability

Maintain a verifiable inventory of all datasets, accept only trusted sources, and log every change for auditability.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.1.1** | **Verify that** an up-to-date inventory of every training-data source (origin, responsible party, license, collection method, intended use constraints, and processing history) is maintained. | 1 | D/V |
| **1.1.2** | **Verify that** training data processes exclude unnecessary features, attributes, or fields (e.g., unused metadata, sensitive PII, leaked test data). | 1 | D/V |
| **1.1.3** | **Verify that** all dataset changes are subject to a logged approval workflow. | 1 | D/V |
| **1.1.4** | **Verify that** datasets or subsets are watermarked or fingerprinted where feasible. | 3 | D/V |

---

## C1.2 Training Data Security & Integrity

Restrict access to training data, encrypt it at rest and in transit, and validate its integrity to prevent tampering, theft, or data poisoning.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.2.1** | **Verify that** access controls protect training data storage and pipelines. | 1 | D/V |
| **1.2.2** | **Verify that** all access to training data is logged, including user, time, and action. | 1 | D/V |
| **1.2.3** | **Verify that** training datasets are encrypted in transit and at rest, using current recommended cryptographic algorithms and key management practices. | 1 | D/V |
| **1.2.4** | **Verify that** cryptographic hashes or digital signatures are used to ensure data integrity during training data storage and transfer. | 2 | D/V |
| **1.2.5** | **Verify that** automated integrity monitoring is applied to guard against unauthorized modifications or corruption of training data. | 2 | D/V |
| **1.2.6** | **Verify that** obsolete training data is securely purged or anonymized. | 1 | D/V |
| **1.2.7** | **Verify that** all training dataset versions are uniquely identified, stored immutably, and auditable to support rollback and forensic analysis. | 3 | D/V |

---

## C1.3 Data Labeling and Annotation Security

Ensure labeling and annotation processes are access-controlled, auditable, and protect sensitive information.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.3.1** | **Verify that** labeling interfaces and platforms enforce access controls and maintain audit logs of all labeling activities. | 1 | D/V |
| **1.3.2** | **Verify that** cryptographic hashes or digital signatures are applied to labeling artifacts, annotation data, and fine-tuning feedback records (including RLHF preference pairs) to ensure their integrity and authenticity. | 2 | D/V |
| **1.3.3** | **Verify that** labeling audit logs are tamper-evident and that labeling platforms protect against unauthorized modifications. | 2 | D/V |
| **1.3.4** | **Verify that** sensitive information in labels is redacted, anonymized, or encrypted using appropriate granularity at rest and in transit. | 2 | D/V |

---

## C1.4 Training Data Quality and Security Assurance

Combine automated validation, manual spot-checks, and logged remediation to guarantee dataset reliability.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.4.1** | **Verify that** automated tests catch format errors and nulls on every ingest or significant data transformation. | 1 | D |
| **1.4.2** | **Verify that** training and fine-tuning pipelines implement data integrity validation and poisoning detection techniques (e.g., statistical analysis, outlier detection, embedding analysis) to identify potential data poisoning or unintentional corruption in training data. | 2 | D/V |
| **1.4.3** | **Verify that** automatically generated labels (e.g., via models or weak supervision) are subject to confidence thresholds and consistency checks to detect misleading or low-confidence labels. | 2 | D/V |
| **1.4.4** | **Verify that** appropriate defenses, such as adversarial training, data augmentation with perturbed inputs, or robust optimization techniques, are implemented and tuned for relevant models based on risk assessment. | 3 | D/V |
| **1.4.5** | **Verify that** automated tests catch label skews on every ingest or significant data transformation. | 2 | D |
| **1.4.6** | **Verify that** models used in security-relevant decisions (e.g., abuse detection, fraud scoring, automated trust decisions) are evaluated for systematic bias patterns that an adversary could exploit to evade controls (e.g., mimicking a trusted language style or demographic pattern to bypass detection). | 2 | D/V |

---

## C1.5 Data Lineage and Traceability

Track the full journey of each dataset from source to model input for auditability and incident response.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.5.1** | **Verify that** the lineage of each dataset and its components, including all transformations, augmentations, and merges, is recorded and can be reconstructed. | 1 | D/V |
| **1.5.2** | **Verify that** lineage records are immutable, securely stored, and accessible for audits. | 2 | D/V |
| **1.5.3** | **Verify that** lineage tracking covers synthetic data generated via augmentation, synthesis, or privacy-preserving techniques and that all synthetic data is clearly labeled and distinguishable from real data throughout the pipeline. | 2 | D/V |

---

## C1.6 RLHF & Fine-Tuning Feedback Data Integrity

Reinforcement Learning from Human Feedback introduces preference pairs as a distinct training data class whose integrity cannot be guaranteed by general training data controls alone. Adversarial annotators or tampered preference records can steer policy model behavior in ways invisible to standard dataset validation.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.6.1** | **Verify that** annotator identity metadata is exported and retained alongside the preference dataset so that every preference pair can be attributed to a specific, verified human annotator throughout the training pipeline, not only within the labeling platform. | 2 | D/V |
| **1.6.2** | **Verify that** statistical anomaly detection is applied to preference datasets prior to reward model training to identify patterns consistent with coordinated label manipulation, such as implausibly uniform annotator agreement, systematic bias toward specific response attributes, or submission velocity outliers. | 3 | D/V |

---

## References

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [EU AI Act: Article 10: Data & Data Governance](https://artificialintelligenceact.eu/article/10/)
* [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
* [OpenAI Privacy Center: Data Deletion Controls](https://privacy.openai.com/policies?modal=take-control)
