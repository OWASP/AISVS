# C1 Training Data Integrity & Traceability

## Control Objective

This chapter addresses the sourcing, handling, and maintenance of training data in a way that preserves origin traceability, integrity, and quality. The core security concern is ensuring data has not been tampered with, poisoned, or corrupted.

---

## C1.1 Training Data Origin & Data Security

Training data origin and data security are critical to the security and trustworthiness of any AI system. Datasets must be sourced from verifiable origins and tracked across their full lifecycle so that tampering or unauthorized modification can be detected. Training data must be protected against tampering, corruption, and poisoning throughout its lifecycle.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.1.1** | **Verify that** training data includes only features, attributes, and fields required for the model's stated purpose. | 1 |
| **1.1.2** | **Verify that** the lineage of each dataset and its components, including all transformations, augmentations, and merges, is recorded and can be reconstructed. | 1 |
| **1.1.3** | **Verify that** an up-to-date inventory is kept of every training-data source, including its origin, responsible party, license, collection method, intended use constraints, and processing history. | 2 |
| **1.1.4** | **Verify that** datasets are watermarked so their use can be attributed and any unauthorized use detected. | 3 |
| **1.1.5** | **Verify that** data integrity is provided when training data is stored and transferred. | 2 |
| **1.1.6** | **Verify that** integrity monitoring is applied to guard against unauthorized modifications or corruption of training data. | 2 |
| **1.1.7** | **Verify that** all training datasets are uniquely identified, with change tracking, to support rollback and forensic analysis. | 3 |

---

## C1.2 Data Labeling and Annotation Security

Labeling and annotation processes must be protected against unauthorized modification, data leakage, and integrity compromise. Annotation platforms should enforce access control, preserve auditability, and protect labeling artifacts and sensitive label content throughout the training pipeline.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.2.1** | **Verify that** labeling platforms enforce access controls that restrict who can create, modify, or approve annotations. | 1 |
| **1.2.2** | **Verify that** all labeling activities are recorded in logs. | 1 |
| **1.2.3** | **Verify that** cryptographic integrity is applied to labeling artifacts. | 2 |
| **1.2.4** | **Verify that** sensitive information in labels is redacted, anonymized, or encrypted before being used in any labeling artifact. | 2 |

---

## C1.3 Training Data Quality and Security Assurance

Training data quality and security assurance controls help detect corruption, poisoning, labeling errors, and exploitable dataset patterns before they affect model behavior. Pipelines should combine automated validation, poisoning detection, label quality checks, and bias analysis.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.3.1** | **Verify that** training and fine-tuning pipelines implement poisoning detection techniques to identify potential data poisoning or unintentional corruption in training data. | 2 |
| **1.3.2** | **Verify that** automatically generated labels are subject to confidence thresholds and consistency checks to detect misleading or low-confidence labels. | 2 |
| **1.3.3** | **Verify that** models used in security-relevant decisions are evaluated for bias patterns. | 2 |
| **1.3.4** | **Verify that** disallowed content is detected and removed before training. | 2 |
| **1.3.5** | **Verify that** defenses against clean-label poisoning attacks are implemented. | 3 |

---

## References

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [EU AI Act: Article 10: Data & Data Governance](https://artificialintelligenceact.eu/article/10/)
* [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
* [OpenAI Privacy Center: Data Deletion Controls](https://privacy.openai.com/policies?modal=take-control)
