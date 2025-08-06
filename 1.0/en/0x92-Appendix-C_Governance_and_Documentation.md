# Appendix C: AI Security Governance & Documentation

## Objective

This appendix provides foundational requirements for establishing organizational structures, policies, and processes to govern AI security throughout the system lifecycle.

---

## AC.1 AI Risk Management Framework Adoption

Provide a formal framework to identify, assess, and mitigate AI‑specific risks throughout the system lifecycle.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.1.1** | **Verify that** an AI‑specific risk assessment methodology is documented and implemented. | 1 | D/V |
| **AC.1.2** | **Verify that** risk assessments are conducted at key points in the AI lifecycle and prior to significant changes. | 2 | D |
| **AC.1.3** | **Verify that** the risk management framework aligns with established standards (e.g., NIST AI RMF). | 3 | D/V |

---

## AC.2 AI Security Policy & Procedures

Define and enforce organizational standards for secure AI development, deployment, and operation.

| # | Description  | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.2.1** | **Verify that** documented AI security policies exist. | 1 | D/V |
| **AC.2.2** | **Verify that** policies are reviewed and updated at least annually and after significant threat‑landscape changes. | 2 | D |
| **AC.2.3** | **Verify that** policies address all AISVS categories and applicable regulatory requirements. | 3 | D/V |

---

## AC.3 Roles & Responsibilities for AI Security

Establish clear accountability for AI security across the organization.

| # | Description  | Level | Role |
| :--------: | --------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.3.1** | **Verify that** AI security roles and responsibilities are documented. | 1 | D/V |
| **AC.3.2** | **Verify that** responsible individuals possess appropriate security expertise. | 2 | D |
| **AC.3.3** | **Verify that** an AI ethics committee or governance board is established for high‑risk AI systems. | 3 | D/V |

---

## AC.4 Ethical AI Guidelines Enforcement

Ensure AI systems operate according to established ethical principles.

| # | Description | Level | Role |
| :--------: | -------------------------------------------------------------------------------- | :---: | :--: |
| **AC.4.1** | **Verify that** ethical guidelines for AI development and deployment exist. | 1 | D/V |
| **AC.4.2** | **Verify that** mechanisms are in place to detect and report ethical violations. | 2 | D |
| **AC.4.3** | **Verify that** regular ethical reviews of deployed AI systems are performed. | 3 | D/V |

---

## AC.5 AI Regulatory Compliance Monitoring

Maintain awareness of and compliance with evolving AI regulations.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.5.1** | **Verify that** processes exist to identify applicable AI regulations. | 1 | D/V |
| **AC.5.2** | **Verify that** compliance with all regulatory requirements is assessed. | 2 | D |
| **AC.5.3** | **Verify that** regulatory changes trigger timely reviews and updates to AI systems. | 3 | D/V |

## AC.6 Training Data Governance, Documentation and Process

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------ | :---: | :--: |
| **1.1.2** | **Verify that** only datasets vetted for quality, representativeness, ethical sourcing, and licence compliance are allowed, reducing risks of poisoning, embedded bias, and intellectual property infringement. | 1 | D/V |
| **1.1.5** | **Verify that** labelling/annotation quality is ensured via reviewer cross-checks or consensus. | 2 | D/V |
| **1.1.6** | **Verify that** "data cards" or "datasheets for datasets" are maintained for significant training datasets, detailing characteristics, motivations, composition, collection processes, preprocessing, and recommended/discouraged uses. | 2 | D/V |
| **1.3.2** | **Verify that** that identified biases are mitigated via documented strategies such as re-balancing, targeted data augmentation, algorithmic adjustments (e.g., pre-processing, in-processing, post-processing techniques), or re-weighting, and the impact of mitigation on both fairness and overall model performance is assessed. | 2 | D/V |
| **1.3.3** | **Verify that** post-training fairness metrics are evaluated and documented. | 2 | D/V |
| **1.3.4** | **Verify that** a lifecycle bias-management policy assigns owners and review cadence. | 3 | D/V |
| **1.4.1** | **Verify that** labeling/annotation quality is ensured via clear guidelines, reviewer cross-checks, consensus mechanisms (e.g., monitoring inter-annotator agreement), and defined processes for resolving discrepancies.| 2 | D/V |
| **1.4.4** | **Verify that** labels critical to safety, security, or fairness (e.g., identifying toxic content, critical medical findings) receive mandatory independent dual review or equivalent robust verification.| 3 | D/V |
| **1.4.6** | **Verify that** labeling guides and instructions are comprehensive, version-controlled, and peer-reviewed. | 2 | D/V |
| **1.4.6** | **Verify that** data schemas for labels are clearly defined, and version-controlled. | 2 | D/V |
| **1.3.1** | **Verify that** datasets are profiled for representational imbalance and potential biases across legally protected attributes (e.g., race, gender, age) and other ethically sensitive characteristics relevant to the model's application domain (e.g., socio-economic status, location). | 1 | D/V |
| **1.5.3** | **Verify that** manual spot-checks by domain experts cover a statistically significant sample (e.g., ≥1% or 1,000 samples, whichever is greater, or as determined by risk assessment) to identify subtle quality issues not caught by automation. | 2 | V |
| **1.8.4** | **Verify that** outsourced or crowdsourced labeling workflows include technical/procedural safeguards to ensure data confidentiality, integrity, label quality, and prevent data leakage. | 2 | D/V |
| **1.5.4** | **Verify that** remediation steps are appended to provenance records. | 2 | D/V |
| **1.6.2** | **Verify that** flagged samples trigger manual review before training. | 2 | D/V |
| **1.6.3** | **Verify that** results feed the model's security dossier and inform ongoing threat intelligence. | 2 | V |
| **1.6.4** | **Verify that** detection logic is refreshed with new threat intel. | 3 | D/V |
| **1.6.5** | **Verify that** online-learning pipelines monitor distribution drift. | 3 | D/V |
| **1.7.1** | **Verify that** training data deletion workflows purge primary and derived data and assess model impact, and that the impact on affected models is assessed and, if necessary, addressed (e.g., through retraining or recalibration). | 1 | D/V |
| **1.7.2** | **Verify that** mechanisms are in place to track and respect the scope and status of user consent (and withdrawals) for data used in training, and that consent is validated before data is incorporated into new training processes or significant model updates. | 2 | D |
| **1.7.3** | **Verify that** workflows are tested annually and logged. | 2 | V |
| **1.8.1** | **Verify that** third-party data suppliers, including providers of pre-trained models and external datasets, undergo security, privacy, ethical sourcing, and data quality due diligence before their data or models are integrated.| 2 | D/V |
| **1.8.2** | **Verify that** external transfers use TLS/auth and integrity checks. | 1 | D |
| **1.8.3** | **Verify that** high-risk data sources (e.g., open-source datasets with unknown provenance, unvetted suppliers) receive enhanced scrutiny, such as sandboxed analysis, extensive quality/bias checks, and targeted poisoning detection, before use in sensitive applications.| 2 | D/V |
| **1.8.4** | **Verify that** Verify that pre-trained models obtained from third parties are evaluated for embedded biases, potential backdoors, integrity of their architecture, and the provenance of their original training data before fine-tuning or deployment. | 3 | D/V |
| **1.5.3** | **Verify that** if adversarial training is used, the generation, management, and versioning of adversarial datasets are documented and controlled. | 2 | D/V |
| **1.5.3** | **Verify that** the impact of adversarial robustness training on model performance (against both clean and adversarial inputs) and fairness metrics is evaluated, documented, and monitored. | 3 | D/V |
| **1.5.4** | **Verify that** strategies for adversarial training and robustness are periodically reviewed and updated to counter evolving adversarial attack techniques.| 3 | D/V |
| **1.4.2** | **Verify that** failed datasets are quarantined with audit trails. | 2 | D/V |
| **1.4.3** | **Verify that** quality gates block sub-par datasets unless exceptions are approved. | 2 | D/V |
| **1.11.2** | **Verify that** the generation process, parameters, and intended use of synthetic data are documented. | 2 | D/V |
| **1.11.3** | **Verify that** synthetic data is risk-assessed for bias, privacy leakage, and representational issues before use in training. | 2 | D/V || **1.12.2** | **Verify that** access logs are regularly reviewed for unusual patterns, such as large exports or access from new locations. | 2 | D/V |
| **1.12.3** | **Verify that** alerts are generated for suspicious access events and investigated promptly. | 2 | D/V |
| **1.13.1** | **Verify that** explicit retention periods are defined for all training datasets. | 1 | D/V |
| **1.13.2** | **Verify that** datasets are automatically expired, deleted, or reviewed for deletion at the end of their lifecycle. | 2 | D/V |
| **1.13.3** | **Verify that** retention and deletion actions are logged and auditable. | 2 | D/V |
| **1.14.1** | **Verify that** data residency and cross-border transfer requirements are identified and enforced for all datasets. | 2 | D/V |
| **1.14.2** | **Verify that** sector-specific regulations (e.g., healthcare, finance) are identified and addressed in data handling. | 2 | D/V |
| **1.14.3** | **Verify that** compliance with relevant privacy laws (e.g., GDPR, CCPA) is documented and reviewed regularly. | 2 | D/V |
| **1.16.1** | **Verify that** mechanisms exist to respond to data subject requests for access, rectification, restriction, or objection. | 2 | D/V |
| **1.16.2** | **Verify that** requests are logged, tracked, and fulfilled within legally mandated timeframes. | 2 | D/V |
| **1.16.3** | **Verify that** data subject rights processes are tested and reviewed regularly for effectiveness. | 2 | D/V |
| **1.17.1** | **Verify that** an impact analysis is performed before updating or replacing a dataset version, covering model performance, fairness, and compliance. | 2 | D/V |
| **1.17.2** | **Verify that** results of the impact analysis are documented and reviewed by relevant stakeholders. | 2 | D/V |
| **1.17.3** | **Verify that** rollback plans exist in case new versions introduce unacceptable risks or regressions. | 2 | D/V |
| **1.18.1** | **Verify that** all personnel involved in data annotation are background-checked and trained in data security and privacy. | 2 | D/V |
| **1.18.2** | **Verify that** all annotation personnel sign confidentiality and non-disclosure agreements. | 2 | D/V |
| **1.18.3** | **Verify that** annotation platforms enforce access controls and monitor for insider threats. | 2 | D/V |

### References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023 — AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [ISO/IEC 23894:2023 — Artificial Intelligence — Guidance on Risk Management](https://www.iso.org/standard/77304.html)
* [EU Artificial Intelligence Act — Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
* [ISO/IEC 24029‑2:2023 — Robustness of Neural Networks — Methodology for Formal Methods](https://www.iso.org/standard/79804.html)
