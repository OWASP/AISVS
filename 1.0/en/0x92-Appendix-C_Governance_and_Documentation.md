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

---

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

---

## AC.7 Model Lifecycle Governance & Documentation

Establish governance processes for model lifecycle documentation, approval workflows, and audit trail requirements.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.7.1** | **Verify that** all model artifacts use semantic versioning (MAJOR.MINOR.PATCH) with documented criteria specifying when each version component increments. | 2 | D/V |
| **AC.7.2** | **Verify that** emergency deployments require documented security risk assessment and approval from a pre-designated security authority within pre-agreed timeframes. | 2 | D/V |
| **AC.7.3** | **Verify that** rollback artifacts (previous model versions, configurations, dependencies) are retained according to organizational policies. | 2 | V |
| **AC.7.4** | **Verify that** audit log access requires appropriate authorization and all access attempts are logged with user identity and a timestamp. | 2 | D/V |
| **AC.7.5** | **Verify that** retired model artifacts are retained according to data retention policies. | 1 | D/V |

---

## C2.1 Prompt Injection Defense

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------ | :---: | :--: |
| **2.1.3** | **Verify that** adversarial evaluation tests (e.g., Red Team "many-shot" prompts) are run before every model or prompt-template release, with success-rate thresholds and automated blockers for regressions. | 2 |  D/V |
| **2.1.5** | **Verify that** all prompt-filter rule updates, classifier model versions and block-list changes are version-controlled and auditable. | 3 |  D/V |

---

## C2.2 Adversarial-Example Resistance

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------ | :---: | :--: |
| **2.2.5** | **Verify that** robustness metrics (success rate of known attack suites) are tracked over time via automation and regressions trigger an alert.  | 3 |  D/V |

---

## C2.4 Content & Policy Screening

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.4.3** | **Verify that** the screening model or rule set is retrained/updated at least quarterly, incorporating newly observed jailbreak or policy bypass patterns.  | 2 | D |

---

## C2.5 Input Rate Limiting & Abuse Prevention

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.5.4** | **Verify that** abuse prevention logs are retained and reviewed for emerging attack patterns. | 3 | V |

---

## C2.7 Input Provenance & Attribution

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.7.1** | **Verify that** all user inputs are tagged with metadata (user ID, session, source, timestamp, IP address) at ingestion. | 1 | D/V |
| **2.7.2** | **Verify that** provenance metadata is retained and auditable for all processed inputs. | 2 | D/V |
| **2.7.3** | **Verify that** anomalous or untrusted input sources are flagged and subject to enhanced scrutiny or blocking. | 2 | D/V |

---

## C2.9 Multi-Modal Security Validation Pipeline

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.9.5** | **Verify that** modality-specific content classifiers are updated according to documented schedules (minimum quarterly) with new threat patterns, adversarial examples, and performance benchmarks maintained above baseline thresholds. | 3 | D/V |


| **4.4.4** | **Verify that** container images are scanned to block hardcoded secrets (e.g., API keys, credentials, certificates). | 2 | D/V |
| **4.2.1** | **Verify that** infrastructure-as-code is scanned on every commit, and merges are blocked on critical or high-severity findings. | 1 | D/V |
| **4.2.4** | **Verify that** CI/CD pipelines use short-lived, scoped identities for access to secrets and infrastructure. | 2 | D/V |
| **4.2.6** | **Verify that** build environments are isolated from production networks and data. | 2 | D/V |
| **4.5.4** | **Verify that** before an AI model is promoted to production, its sandbox results are cryptographically signed by authorized security personnel and stored in immutable audit logs. | 2 | D/V |
| **4.5.5** | **Verify that** sandbox environments are destroyed and recreated from golden images between evaluations with complete filesystem and memory cleanup. | 2 | D/V |
| **4.5.6** | **Verify that** multi-modal inputs are processed in isolated sandboxes with defined resource limits (memory, CPU, processing time) specific to each modality type and documented in security policies. | 2 | D/V |
| **4.6.1** | **Verify that** container images are scanned according to organizational schedules with CRITICAL vulnerabilities blocking deployment based on organizational risk thresholds. | 1 | D/V |
| **4.6.2** | **Verify that** infrastructure passes CIS Benchmarks or NIST 800-53 controls with organizationally defined compliance thresholds and automated remediation for failed checks. | 1 | D/V |
| **4.6.3** | **Verify that** security alerts integrate with SIEM platforms (Splunk, Elastic, or Sentinel) using CEF or STIX/TAXII formats with automated enrichment. | 2 | V |

| **4.6.3** | **Verify that** HIGH severity vulnerabilities are patched according to organizational risk management timelines with emergency procedures for actively exploited CVEs. | 2 | D/V |
| **4.6.5** | **Verify that** infrastructure metrics are exported to monitoring systems (Prometheus, DataDog) with SLA dashboards and executive reporting. | 3 | V |
| **4.6.6** | **Verify that** configuration drift is detected using tools (Chef InSpec, AWS Config) according to organizational monitoring requirements with automatic rollback for unauthorized changes. | 2 | D/V |
| **4.7.1** | **Verify that** production environments block SSH access, disable debug endpoints, and require change requests with organizational advance notice requirements except emergencies. | 2 | D/V |
| **4.7.2** | **Verify that** promotion gates include automated security tests (SAST, DAST, container scanning) with zero CRITICAL findings required for approval. | 2 | D/V |
| **4.7.1** | **Verify that** GPU/TPU utilization is monitored with alerts triggered at organizationally defined thresholds and automatic scaling or load balancing activated based on capacity management policies. | 1 | D/V |
| **4.7.2** | **Verify that** AI workload metrics (inference latency, throughput, error rates) are collected according to organizational monitoring requirements and correlated with infrastructure utilization. | 1 | D/V |
| **4.7.4** | **Verify that** cost monitoring tracks spending per workload/tenant with alerts based on organizational budget thresholds and automated controls for budget overruns. | 2 | V |
| **4.7.5** | **Verify that** capacity planning uses historical data with organizationally defined forecasting periods and automated resource provisioning based on demand patterns. | 3 | V |
| **4.8.2** | **Verify that** environment promotion requires approval from organizationally defined authorized personnel with cryptographic signatures and immutable audit trails. | 1 | D/V |
| **4.8.4** | **Verify that** infrastructure-as-code changes require peer review with automated testing and security scanning before merge to main branch. | 2 | D/V |
| **4.8.5** | **Verify that** non-production data is anonymized according to organizational privacy requirements, synthetic data generation, or complete data masking with PII removal verified. | 2 | D/V |
| **4.9.1** | **Verify that** infrastructure configurations are backed up according to organizational backup schedules to geographically separate regions with 3-2-1 backup strategy implementation. | 1 | D/V |
| **4.9.3** | **Verify that** recovery procedures are tested and validated through automated testing according to organizational schedules with RTO and RPO targets meeting organizational requirements. | 2 | V |
| **4.9.4** | **Verify that** disaster recovery includes AI-specific runbooks with model weight restoration, GPU cluster rebuilding, and service dependency mapping. | 3 | V |
| **4.10.1** | **Verify that** infrastructure compliance is assessed according to organizational schedules against SOC 2, ISO 27001, or FedRAMP controls with automated evidence collection. | 2 | D/V |
| **4.10.2** | **Verify that** infrastructure documentation includes network diagrams, data flow maps, and threat models updated according to organizational change management requirements. | 2 | V |
| **4.10.3** | **Verify that** infrastructure changes undergo automated compliance impact assessment with regulatory approval workflows for high-risk modifications. | 3 | D/V |
| **4.11.1** | **Verify that** AI accelerator firmware (GPU BIOS, TPU firmware) is verified with cryptographic signatures and updated according to organizational patch management timelines. | 2 | D/V |
| **4.11.4** | **Verify that** the AI hardware supply chain includes provenance verification with manufacturer certificates and tamper-evident packaging validation. | 3 | V |
| **4.13.4** | **Verify that** cloud vendor lock-in prevention includes portable infrastructure-as-code, standardized APIs, and data export capabilities with format conversion tools. | 3 | V |
| **4.13.5** | **Verify that** multi-cloud cost optimization includes security controls preventing resource sprawl as well as unauthorized cross-cloud data transfer charges. | 3 | V |
| **4.14.1** | **Verify that** GitOps repositories require signed commits with GPG keys and branch protection rules preventing direct pushes to main branches. | 2 | D/V |
| **4.14.5** | **Verify that** self-healing infrastructure includes security event correlation with automated incident response and stakeholder notification workflows. | 3 | V |
| **4.16.5** | **Verify that** cloud provider security assessments include agent-specific threat modeling and risk evaluation. | 3 | D/V |



### References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023 — AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [ISO/IEC 23894:2023 — Artificial Intelligence — Guidance on Risk Management](https://www.iso.org/standard/77304.html)
* [EU Artificial Intelligence Act — Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
* [ISO/IEC 24029‑2:2023 — Robustness of Neural Networks — Methodology for Formal Methods](https://www.iso.org/standard/79804.html)
