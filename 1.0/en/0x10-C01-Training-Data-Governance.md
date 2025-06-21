# C1 Training Data Governance & Bias Management

## Control Objective

Training data must be sourced, handled, and maintained in a way that preserves provenance, security, quality, and fairness. Doing so fulfils legal duties and reduces risks of bias, poisoning, or privacy breaches throughout the AI lifecycle.

---

## C1.1 Training Data Provenance

Maintain a verifiable inventory of all datasets, accept only trusted sources, and log every change for auditability.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.1.1** | **Verify that** an up-to-date inventory of every training-data source (origin, steward/owner, licence, collection method, intended use constraints, and processing history) is maintained. | 1 | D/V |
| **1.1.2** | **Verify that** only datasets vetted for quality, representativeness, ethical sourcing, and licence compliance are allowed, reducing risks of poisoning, embedded bias, and intellectual property infringement. | 1 | D/V |
| **1.1.3** | **Verify that** data minimization is enforced so unnecessary or sensitive attributes are excluded. | 1 | D/V |
| **1.1.4** | **Verify that** all dataset changes are subject to a logged approval workflow. | 2 | D/V |
| **1.1.5** | **Verify that** labelling/annotation quality is ensured via reviewer cross-checks or consensus. | 2 | D/V |
| **1.1.6** | **Verify that** "data cards" or "datasheets for datasets" are maintained for significant training datasets, detailing characteristics, motivations, composition, collection processes, preprocessing, and recommended/discouraged uses. | 2 | D/V |

---

## C1.2 Training Data Security & Integrity

Restrict access, encrypt at rest and in transit, and validate integrity to block tampering or theft.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.2.1** | **Verify that** access controls protect storage and pipelines. | 1 | D/V |
| **1.2.2** | **Verify that** datasets are encrypted in transit and, for all sensitive or personally identifiable information (PII), at rest, using industry-standard cryptographic algorithms and key management practices. | 2 | D/V |
| **1.2.3** | **Verify that** cryptographic hashes or digital signatures are used to ensure data integrity during storage and transfer, and that automated anomaly detection techniques are applied to guard against unauthorized modifications or corruption, including targeted data poisoning attempts. | 2 | D/V |
| **1.2.4** | **Verify that** dataset versions are tracked to enable rollback. | 3 | D/V |
| **1.2.5** | **Verify that** obsolete data is securely purged or anonymized in compliance with data retention policies, regulatory requirements, and to shrink the attack surface. | 2 | D/V |

---

## C1.3 Representation Completeness & Fairness

Detect demographic skews and apply mitigation so the model's error rates are equitable across groups.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.3.1** | **Verify that** datasets are profiled for representational imbalance and potential biases across legally protected attributes (e.g., race, gender, age) and other ethically sensitive characteristics relevant to the model's application domain (e.g., socio-economic status, location). | 1 | D/V |
| **1.3.2** | **Verify that** that identified biases are mitigated via documented strategies such as re-balancing, targeted data augmentation, algorithmic adjustments (e.g., pre-processing, in-processing, post-processing techniques), or re-weighting, and the impact of mitigation on both fairness and overall model performance is assessed. | 2 | D/V |
| **1.3.3** | **Verify that** post-training fairness metrics are evaluated and documented. | 2 | D/V |
| **1.3.4** | **Verify that** a lifecycle bias-management policy assigns owners and review cadence. | 3 | D/V |

---

## C1.4 Training Data Labeling Quality, Integrity, and Security

Protect labels with encryption and require dual review for critical classes.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.4.1** | **Verify that** labeling/annotation quality is ensured via clear guidelines, reviewer cross-checks, consensus mechanisms (e.g., monitoring inter-annotator agreement), and defined processes for resolving discrepancies.| 2 | D/V |
| **1.4.2** | **Verify that** cryptographic hashes or digital signatures are applied to label artifacts to ensure their integrity and authenticity. | 2 | D/V |
| **1.4.3** | **Verify that** labeling interfaces and platforms enforce strong access controls, maintain tamper-evident audit logs of all labeling activities, and protect against unauthorized modifications. | 2 | D/V |
| **1.4.4** | **Verify that** labels critical to safety, security, or fairness (e.g., identifying toxic content, critical medical findings) receive mandatory independent dual review or equivalent robust verification.| 3 | D/V |
| **1.4.5** | **Verify that** sensitive information (including PII) inadvertently captured or necessarily present in labels is redacted, pseudonymized, anonymized, or encrypted at rest and in transit, according to data minimization principles.| 2 | D/V |
| **1.4.6** | **Verify that** labeling guides and instructions are comprehensive, version-controlled, and peer-reviewed. | 2 | D/V |
| **1.4.7** | **Verify that** data schemas (including for labels) are clearly defined, and version-controlled. | 2 | D/V |
| **1.8.2** | **Verify that** outsourced or crowdsourced labeling workflows include technical/procedural safeguards to ensure data confidentiality, integrity, label quality, and prevent data leakage. | 2 | D/V |

---

## C1.5 Training Data Quality Assurance

Combine automated validation, manual spot-checks, and logged remediation to guarantee dataset reliability.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.5.1** | **Verify that** automated tests catch format errors, nulls, and label skews on every ingest or significant transformation. | 1 | D |
| **1.5.2** | **Verify that** failed datasets are quarantined with audit trails. | 1 | D/V |
| **1.5.3** | **Verify that** manual spot-checks by domain experts cover a statistically significant sample (e.g., ≥1% or 1,000 samples, whichever is greater, or as determined by risk assessment) to identify subtle quality issues not caught by automation. | 2 | V |
| **1.5.4** | **Verify that** remediation steps are appended to provenance records. | 2 | D/V |
| **1.5.5** | **Verify that** quality gates block sub-par datasets unless exceptions are approved. | 2 | D/V |

---

## C1.6 Data Poisoning Detection

Apply statistical anomaly detection and quarantine workflows to stop adversarial insertions.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.6.1** | **Verify that** anomaly detection techniques (e.g., statistical methods, outlier detection, embedding analysis) are applied to training data at ingest and before major training runs to identify potential poisoning attacks or unintentional data corruption. | 2 | D/V |
| **1.6.2** | **Verify that** flagged samples trigger manual review before training. | 2 | D/V |
| **1.6.3** | **Verify that** results feed the model's security dossier and inform ongoing threat intelligence. | 2 | V |
| **1.6.4** | **Verify that** detection logic is refreshed with new threat intel. | 3 | D/V |
| **1.6.5** | **Verify that** online-learning pipelines monitor distribution drift. | 3 | D/V |
| **1.6.6** | **Verify that** specific defenses against known data poisoning attack types (e.g., label flipping, backdoor trigger insertion, influential instance attacks) are considered and implemented based on the system's risk profile and data sources. | 3 | D/V |

---

## C1.7 User Data Deletion & Consent Enforcement

Honor deletion and consent-withdrawal requests across datasets, backups, and derived artifacts.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.7.1** | **Verify that** deletion workflows purge primary and derived data and assess model impact, and that the impact on affected models is assessed and, if necessary, addressed (e.g., through retraining or recalibration). | 1 | D/V |
| **1.7.2** | **Verify that** mechanisms are in place to track and respect the scope and status of user consent (and withdrawals) for data used in training, and that consent is validated before data is incorporated into new training processes or significant model updates. | 2 | D |
| **1.7.3** | **Verify that** workflows are tested annually and logged. | 2 | V |

---

## C1.8 Supply Chain Security

Vet external data providers and verify integrity over authenticated, encrypted channels.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.8.1** | **Verify that** third-party data suppliers, including providers of pre-trained models and external datasets, undergo security, privacy, ethical sourcing, and data quality due diligence before their data or models are integrated.| 2 | D/V |
| **1.8.2** | **Verify that** external transfers use TLS/auth and integrity checks. | 1 | D |
| **1.8.3** | **Verify that** high-risk data sources (e.g., open-source datasets with unknown provenance, unvetted suppliers) receive enhanced scrutiny, such as sandboxed analysis, extensive quality/bias checks, and targeted poisoning detection, before use in sensitive applications.| 2 | D/V |
| **1.8.4** | **Verify that** Verify that pre-trained models obtained from third parties are evaluated for embedded biases, potential backdoors, integrity of their architecture, and the provenance of their original training data before fine-tuning or deployment. | 3 | D/V |

---

## C1.9 Adversarial Sample Detection

Implement measures during the training phase, such as adversarial training, to enhance model resilience against adversarial examples.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.9.1** | **Verify that** appropriate defenses, such as adversarial training (using generated adversarial examples), data augmentation with perturbed inputs, or robust optimization techniques, are implemented and tuned for relevant models based on risk assessment. | 3 | D/V |
| **1.9.2** | **Verify that** if adversarial training is used, the generation, management, and versioning of adversarial datasets are documented and controlled. | 2 | D/V |
| **1.9.3** | **Verify that** the impact of adversarial robustness training on model performance (against both clean and adversarial inputs) and fairness metrics is evaluated, documented, and monitored. | 3 | D/V |
| **1.9.4** | **Verify that** strategies for adversarial training and robustness are periodically reviewed and updated to counter evolving adversarial attack techniques.| 3 | D/V |

---

## C1.10 Data Lineage and Traceability

Track the full journey of each data point from source to model input for auditability and incident response.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.10.1** | **Verify that** the lineage of each data point, including all transformations, augmentations, and merges, is recorded and can be reconstructed. | 2 | D/V |
| **1.10.2** | **Verify that** lineage records are immutable, securely stored, and accessible for audits or investigations. | 2 | D/V |
| **1.10.3** | **Verify that** lineage tracking covers both raw and synthetic data. | 2 | D/V |

---

## C1.11 Synthetic Data Management

Ensure synthetic data is properly managed, labeled, and risk-assessed.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.11.1** | **Verify that** all synthetic data is clearly labeled and distinguishable from real data throughout the pipeline. | 2 | D/V |
| **1.11.2** | **Verify that** the generation process, parameters, and intended use of synthetic data are documented. | 2 | D/V |
| **1.11.3** | **Verify that** synthetic data is risk-assessed for bias, privacy leakage, and representational issues before use in training. | 2 | D/V |

---

## C1.12 Data Access Monitoring & Anomaly Detection

Monitor and alert on unusual access to training data to detect insider threats or exfiltration.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.12.1** | **Verify that** all access to training data is logged, including user, time, and action. | 2 | D/V |
| **1.12.2** | **Verify that** access logs are regularly reviewed for unusual patterns, such as large exports or access from new locations. | 2 | D/V |
| **1.12.3** | **Verify that** alerts are generated for suspicious access events and investigated promptly. | 2 | D/V |

---

## C1.13 Data Retention & Expiry Policies

Define and enforce data retention periods to minimize unnecessary data storage.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.13.1** | **Verify that** explicit retention periods are defined for all training datasets. | 1 | D/V |
| **1.13.2** | **Verify that** datasets are automatically expired, deleted, or reviewed for deletion at the end of their lifecycle. | 2 | D/V |
| **1.13.3** | **Verify that** retention and deletion actions are logged and auditable. | 2 | D/V |

---

## C1.14 Regulatory & Jurisdictional Compliance

Ensure all training data complies with applicable laws and regulations.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.14.1** | **Verify that** data residency and cross-border transfer requirements are identified and enforced for all datasets. | 2 | D/V |
| **1.14.2** | **Verify that** sector-specific regulations (e.g., healthcare, finance) are identified and addressed in data handling. | 2 | D/V |
| **1.14.3** | **Verify that** compliance with relevant privacy laws (e.g., GDPR, CCPA) is documented and reviewed regularly. | 2 | D/V |

---

## C1.15 Data Watermarking & Fingerprinting

Detect unauthorized reuse or leakage of proprietary or sensitive data.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.15.1** | **Verify that** datasets or subsets are watermarked or fingerprinted where feasible. | 3 | D/V |
| **1.15.2** | **Verify that** watermarking/fingerprinting methods do not introduce bias or privacy risks. | 3 | D/V |
| **1.15.3** | **Verify that** periodic checks are performed to detect unauthorized reuse or leakage of watermarked data. | 3 | D/V |

---

## C1.16 Data Subject Rights Management

Support data subject rights such as access, rectification, restriction, and objection.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.16.1** | **Verify that** mechanisms exist to respond to data subject requests for access, rectification, restriction, or objection. | 2 | D/V |
| **1.16.2** | **Verify that** requests are logged, tracked, and fulfilled within legally mandated timeframes. | 2 | D/V |
| **1.16.3** | **Verify that** data subject rights processes are tested and reviewed regularly for effectiveness. | 2 | D/V |

---

## C1.17 Dataset Version Impact Analysis

Assess the impact of dataset changes before updating or replacing versions.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.17.1** | **Verify that** an impact analysis is performed before updating or replacing a dataset version, covering model performance, fairness, and compliance. | 2 | D/V |
| **1.17.2** | **Verify that** results of the impact analysis are documented and reviewed by relevant stakeholders. | 2 | D/V |
| **1.17.3** | **Verify that** rollback plans exist in case new versions introduce unacceptable risks or regressions. | 2 | D/V |

---

## C1.18 Data Annotation Workforce Security

Ensure the security and integrity of personnel involved in data annotation.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **1.18.1** | **Verify that** all personnel involved in data annotation are background-checked and trained in data security and privacy. | 2 | D/V |
| **1.18.2** | **Verify that** all annotation personnel sign confidentiality and non-disclosure agreements. | 2 | D/V |
| **1.18.3** | **Verify that** annotation platforms enforce access controls and monitor for insider threats. | 2 | D/V |

---

## References

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [EU AI Act – Article 10: Data & Data Governance](https://artificialintelligenceact.eu/article/10/)
* [MITRE ATLAS: Adversary Tactics for AI](https://atlas.mitre.org/)
* [Survey of ML Bias Mitigation Techniques – MDPI](https://www.mdpi.com/2673-6470/4/1/1)
* [Data Provenance & Lineage Best Practices – Nightfall AI](https://www.nightfall.ai/ai-security-101/data-provenance-and-lineage)
* [Data Labeling Quality Standards – LabelYourData](https://labelyourdata.com/articles/data-labeling-quality-and-how-to-measure-it)
* [Training Data Poisoning Guide – Lakera.ai](https://www.lakera.ai/blog/training-data-poisoning)
* [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
* [ISO/IEC 23053: AI Management Systems Framework](https://www.iso.org/sectors/it-technologies/ai)
* [IBM: What is AI Governance?](https://www.ibm.com/think/topics/ai-governance)
* [Google AI Principles](https://ai.google/principles/)
* [GDPR & AI Training Data – DataProtectionReport](https://www.dataprotectionreport.com/2024/08/recent-regulatory-developments-in-training-artificial-intelligence-ai-models-under-the-gdpr/)
* [Supply-Chain Security for AI Data – AppSOC](https://www.appsoc.com/blog/ai-is-the-new-frontier-of-supply-chain-security)
* [OpenAI Privacy Center – Data Deletion Controls](https://privacy.openai.com/policies?modal=take-control)
* [Adversarial ML Dataset – Kaggle](https://www.kaggle.com/datasets/cnrieiit/adversarial-machine-learning-dataset)
