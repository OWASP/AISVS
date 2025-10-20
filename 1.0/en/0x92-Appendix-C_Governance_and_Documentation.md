# Appendix C: AI Security Governance & Documentation (Reorganized)

## Objective

This appendix provides foundational requirements for establishing organizational structures, policies, documentation, and processes to govern AI security throughout the system lifecycle.

---

## AC.1 AI Risk Management Framework Adoption

|      #     | Description                                                                                                        | Level | Role |
| :--------: | :----------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.1.1** | **Verify that** an AI-specific risk assessment methodology is documented and implemented.                          |   1   |  D/V |
| **AC.1.2** | **Verify that** risk assessments are conducted at key points in the AI lifecycle and prior to significant changes. |   2   |   D  |
| **AC.1.3** | **Verify that** the risk management framework aligns with established standards (e.g., NIST AI RMF).               |   3   |  D/V |

---

## AC.2 AI Security Policy & Procedures

|      #     | Description                                                                                                         | Level | Role |
| :--------: | :------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.2.1** | **Verify that** documented AI security policies exist.                                                              |   1   |  D/V |
| **AC.2.2** | **Verify that** policies are reviewed and updated at least annually and after significant threat-landscape changes. |   2   |   D  |
| **AC.2.3** | **Verify that** policies address all AISVS categories and applicable regulatory requirements.                       |   3   |  D/V |

---

## AC.3 Roles & Responsibilities for AI Security

|      #     | Description                                                                                         | Level | Role |
| :--------: | :-------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.3.1** | **Verify that** AI security roles and responsibilities are documented.                              |   1   |  D/V |
| **AC.3.2** | **Verify that** responsible individuals possess appropriate security expertise.                     |   2   |   D  |
| **AC.3.3** | **Verify that** an AI ethics committee or governance board is established for high-risk AI systems. |   3   |  D/V |

---

## AC.4 Ethical AI Guidelines Enforcement

|      #     | Description                                                                      | Level | Role |
| :--------: | :------------------------------------------------------------------------------- | :---: | :--: |
| **AC.4.1** | **Verify that** ethical guidelines for AI development and deployment exist.      |   1   |  D/V |
| **AC.4.2** | **Verify that** mechanisms are in place to detect and report ethical violations. |   2   |   D  |
| **AC.4.3** | **Verify that** regular ethical reviews of deployed AI systems are performed.    |   3   |  D/V |

---

## AC.5 AI Regulatory Compliance Monitoring

|      #     | Description                                                                          | Level | Role |
| :--------: | :----------------------------------------------------------------------------------- | :---: | :--: |
| **AC.5.1** | **Verify that** processes exist to identify applicable AI regulations.               |   1   |  D/V |
| **AC.5.2** | **Verify that** compliance with all regulatory requirements is assessed.             |   2   |   D  |
| **AC.5.3** | **Verify that** regulatory changes trigger timely reviews and updates to AI systems. |   3   |  D/V |

---

## AC.6 Training Data Governance, Documentation & Process

### AC.6.1 Data Sourcing & Due Diligence

|       #      | Description                                                                                                                                                                                                                                                                   | Level | Role |
| :----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.6.1.1** | **Verify that** only datasets vetted for quality, representativeness, ethical sourcing, and licence compliance are allowed, reducing risks of poisoning, embedded bias, and intellectual property infringement.                                                               |   1   |  D/V |
| **AC.6.1.2** | **Verify that** third-party data suppliers, including providers of pre-trained models and external datasets, undergo security, privacy, ethical sourcing, and data quality due diligence before their data or models are integrated.                                          |   2   |  D/V |
| **AC.6.1.3** | **Verify that** external transfers use TLS/auth and integrity checks.                                                                                                                                                                                                         |   1   |   D  |
| **AC.6.1.4** | **Verify that** high-risk data sources (e.g., open-source datasets with unknown provenance, unvetted suppliers) receive enhanced scrutiny, such as sandboxed analysis, extensive quality/bias checks, and targeted poisoning detection, before use in sensitive applications. |   2   |  D/V |
| **AC.6.1.5** | **Verify that** Verify that pre-trained models obtained from third parties are evaluated for embedded biases, potential backdoors, integrity of their architecture, and the provenance of their original training data before fine-tuning or deployment.                      |   3   |  D/V |

### AC.6.2 Bias & Fairness Management

|       #      | Description                                                                                                                                                                                                                                                                                                                           | Level | Role |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.6.2.1** | **Verify that** datasets are profiled for representational imbalance and potential biases across legally protected attributes (e.g., race, gender, age) and other ethically sensitive characteristics relevant to the model's application domain (e.g., socio-economic status, location).                                             |   1   |  D/V |
| **AC.6.2.2** | **Verify that** that identified biases are mitigated via documented strategies such as re-balancing, targeted data augmentation, algorithmic adjustments (e.g., pre-processing, in-processing, post-processing techniques), or re-weighting, and the impact of mitigation on both fairness and overall model performance is assessed. |   2   |  D/V |
| **AC.6.2.3** | **Verify that** post-training fairness metrics are evaluated and documented.                                                                                                                                                                                                                                                          |   2   |  D/V |
| **AC.6.2.4** | **Verify that** a lifecycle bias-management policy assigns owners and review cadence.                                                                                                                                                                                                                                                 |   3   |  D/V |

### AC.6.3 Labeling & Annotation Governance

|       #       | Description                                                                                                                                                                                                                             | Level | Role |
| :-----------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
|  **AC.6.3.1** | **Verify that** labelling/annotation quality is ensured via reviewer cross-checks or consensus.                                                                                                                                         |   2   |  D/V |
|  **AC.6.3.2** | **Verify that** data cards are maintained for significant training datasets, detailing characteristics, motivations, composition, collection processes, preprocessing, licenses, and recommended/discouraged uses.                      |   2   |  D/V |
|  **AC.6.3.3** | **Verify that** data cards document bias risks, demographic skews, and ethical considerations relevant to the dataset.                                                                                                                  |   2   |  D/V |
|  **AC.6.3.4** | **Verify that** data cards are versioned alongside datasets and updated whenever the dataset is modified.                                                                                                                               |   2   |  D/V |
|  **AC.6.3.5** | **Verify that** data cards are reviewed and approved by both technical and non-technical stakeholders (e.g., compliance, ethics, domain experts).                                                                                       |   2   |  D/V |
|  **AC.6.3.6** | **Verify that** labeling/annotation quality is ensured via clear guidelines, reviewer cross-checks, consensus mechanisms (e.g., monitoring inter-annotator agreement), and defined processes for resolving discrepancies.               |   2   |  D/V |
|  **AC.6.3.7** | **Verify that** labels critical to safety, security, or fairness (e.g., identifying toxic content, critical medical findings) receive mandatory independent dual review or equivalent robust verification.                              |   3   |  D/V |
|  **AC.6.3.8** | **Verify that** labeling guides and instructions are comprehensive, version-controlled, and peer-reviewed.                                                                                                                              |   2   |  D/V |
|  **AC.6.3.9** | **Verify that** data schemas for labels are clearly defined, and version-controlled.                                                                                                                                                    |   2   |  D/V |
|  **AC.6.3.10** | **Verify that** outsourced or crowdsourced labeling workflows include technical/procedural safeguards to ensure data confidentiality, integrity, label quality, and prevent data leakage.                                              |   2   |  D/V |
|  **AC.6.3.11** | **Verify that** all personnel involved in data annotation are background-checked and trained in data security and privacy.                                                                                                             |   2   |  D/V |
|  **AC.6.3.12** | **Verify that** all annotation personnel sign confidentiality and non-disclosure agreements.                                                                                                                                           |   2   |  D/V |
|  **AC.6.3.13** | **Verify that** annotation platforms enforce access controls and monitor for insider threats.                                                                                                                                          |   2   |  D/V |

### AC.6.4 Dataset Quality Gates & Quarantine

|       #      | Description                                                                                                                                                                                                                                       | Level | Role |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.6.4.1** | **Verify that** failed datasets are quarantined with audit trails.                                                                                                                                                                                |   2   |  D/V |
| **AC.6.4.2** | **Verify that** quality gates block sub-par datasets unless exceptions are approved.                                                                                                                                                              |   2   |  D/V |
| **AC.6.4.3** | **Verify that** manual spot-checks by domain experts cover a statistically significant sample (e.g., ≥1% or 1,000 samples, whichever is greater, or as determined by risk assessment) to identify subtle quality issues not caught by automation. |   2   |   V  |

### AC.6.5 Threat/Poisoning Detection & Drift

|       #      | Description                                                                                       | Level | Role |
| :----------: | :------------------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.6.5.1** | **Verify that** flagged samples trigger manual review before training.                            |   2   |  D/V |
| **AC.6.5.2** | **Verify that** results feed the model's security dossier and inform ongoing threat intelligence. |   2   |   V  |
| **AC.6.5.3** | **Verify that** detection logic is refreshed with new threat intel.                               |   3   |  D/V |
| **AC.6.5.4** | **Verify that** online-learning pipelines monitor distribution drift.                             |   3   |  D/V |

### AC.6.6 Deletion, Consent, Rights, Retention & Compliance

|       #       | Description                                                                                                                                                                                                                                                        | Level | Role |
| :-----------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
|  **AC.6.6.1** | **Verify that** training data deletion workflows purge primary and derived data and assess model impact, and that the impact on affected models is assessed and, if necessary, addressed (e.g., through retraining or recalibration).                              |   1   |  D/V |
|  **AC.6.6.2** | **Verify that** mechanisms are in place to track and respect the scope and status of user consent (and withdrawals) for data used in training, and that consent is validated before data is incorporated into new training processes or significant model updates. |   2   |   D  |
|  **AC.6.6.3** | **Verify that** workflows are tested annually and logged.                                                                                                                                                                                                          |   2   |   V  |
|  **AC.6.6.4** | **Verify that** explicit retention periods are defined for all training datasets.                                                                                                                                                                                  |   1   |  D/V |
|  **AC.6.6.5** | **Verify that** datasets are automatically expired, deleted, or reviewed for deletion at the end of their lifecycle.                                                                                                                                               |   2   |  D/V |
|  **AC.6.6.6** | **Verify that** retention and deletion actions are logged and auditable.                                                                                                                                                                                           |   2   |  D/V |
|  **AC.6.6.7** | **Verify that** data residency and cross-border transfer requirements are identified and enforced for all datasets.                                                                                                                                                |   2   |  D/V |
|  **AC.6.6.8** | **Verify that** sector-specific regulations (e.g., healthcare, finance) are identified and addressed in data handling.                                                                                                                                             |   2   |  D/V |
|  **AC.6.6.9** | **Verify that** compliance with relevant privacy laws (e.g., GDPR, CCPA) is documented and reviewed regularly.                                                                                                                                                     |   2   |  D/V |
| **AC.6.6.10** | **Verify that** mechanisms exist to respond to data subject requests for access, rectification, restriction, or objection.                                                                                                                                         |   2   |  D/V |
| **AC.6.6.11** | **Verify that** requests are logged, tracked, and fulfilled within legally mandated timeframes.                                                                                                                                                                    |   2   |  D/V |
| **AC.6.6.12** | **Verify that** data subject rights processes are tested and reviewed regularly for effectiveness.                                                                                                                                                                 |   2   |  D/V |

### AC.6.7 Versioning & Change Management

|       #      | Description                                                                                                                                           | Level | Role |
| :----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.6.7.1** | **Verify that** an impact analysis is performed before updating or replacing a dataset version, covering model performance, fairness, and compliance. |   2   |  D/V |
| **AC.6.7.2** | **Verify that** results of the impact analysis are documented and reviewed by relevant stakeholders.                                                  |   2   |  D/V |
| **AC.6.7.3** | **Verify that** rollback plans exist in case new versions introduce unacceptable risks or regressions.                                                |   2   |  D/V |

### AC.6.8 Synthetic Data Governance

|       #      | Description                                                                                                                    | Level | Role |
| :----------: | :----------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.6.8.1** | **Verify that** the generation process, parameters, and intended use of synthetic data are documented.                         |   2   |  D/V |
| **AC.6.8.2** | **Verify that** synthetic data is risk-assessed for bias, privacy leakage, and representational issues before use in training. |   2   |  D/V |

### AC.6.9 Access Monitoring

|       #      | Description                                                                                                                  | Level | Role |
| :----------: | :--------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.6.9.1** | **Verify that** access logs are regularly reviewed for unusual patterns, such as large exports or access from new locations. |   2   |  D/V |
| **AC.6.9.2** | **Verify that** alerts are generated for suspicious access events and investigated promptly.                                 |   2   |  D/V |

### AC.6.10 Adversarial Training Governance

|       #       | Description                                                                                                                                                                                  | Level | Role |
| :-----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.6.10.1** | **Verify that** if adversarial training is used, the generation, management, and versioning of adversarial datasets are documented and controlled.                                           |   2   |  D/V |
| **AC.6.10.2** | **Verify that** the impact of adversarial robustness training on model performance (against both clean and adversarial inputs) and fairness metrics is evaluated, documented, and monitored. |   3   |  D/V |
| **AC.6.10.3** | **Verify that** strategies for adversarial training and robustness are periodically reviewed and updated to counter evolving adversarial attack techniques.                                  |   3   |  D/V |

---

## AC.7 Model Lifecycle Governance & Documentation

|      #     | Description                                                                                                                                                           | Level | Role |
| :--------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.7.1** | **Verify that** all model artifacts use semantic versioning (MAJOR.MINOR.PATCH) with documented criteria specifying when each version component increments.           |   2   |  D/V |
| **AC.7.2** | **Verify that** emergency deployments require documented security risk assessment and approval from a pre-designated security authority within pre-agreed timeframes. |   2   |  D/V |
| **AC.7.3** | **Verify that** rollback artifacts (previous model versions, configurations, dependencies) are retained according to organizational policies.                         |   2   |   V  |
| **AC.7.4** | **Verify that** audit log access requires appropriate authorization and all access attempts are logged with user identity and a timestamp.                            |   2   |  D/V |
| **AC.7.5** | **Verify that** retired model artifacts are retained according to data retention policies.                                                                            |   1   |  D/V |

---

## AC.8 Prompt, Input, and Output Safety Governance

### AC.8.1 Prompt Injection Defense

|       #      | Description                                                                                                                                                                                                   | Level | Role |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.8.1.1** | **Verify that** adversarial evaluation tests (e.g., Red Team "many-shot" prompts) are run before every model or prompt-template release, with success-rate thresholds and automated blockers for regressions. |   2   |  D/V |
| **AC.8.1.2** | **Verify that** all prompt-filter rule updates, classifier model versions and block-list changes are version-controlled and auditable.                                                                        |   3   |  D/V |

### AC.8.2 Adversarial-Example Resistance

|       #      | Description                                                                                                                                     | Level | Role |
| :----------: | :---------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.8.2.1** | **Verify that** robustness metrics (success rate of known attack suites) are tracked over time via automation and regressions trigger an alert. |   3   |  D/V |

### AC.8.3 Content & Policy Screening

|       #      | Description                                                                                                                                                | Level | Role |
| :----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.8.3.1** | **Verify that** the screening model or rule set is retrained/updated at least quarterly, incorporating newly observed jailbreak or policy bypass patterns. |   2   |   D  |

### AC.8.4 Input Rate Limiting & Abuse Prevention

|       #      | Description                                                                                   | Level | Role |
| :----------: | :-------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.8.4.1** | **Verify that** abuse prevention logs are retained and reviewed for emerging attack patterns. |   3   |   V  |

### AC.8.5 Input Provenance & Attribution

|       #      | Description                                                                                                              | Level | Role |
| :----------: | :----------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.8.5.1** | **Verify that** all user inputs are tagged with metadata (user ID, session, source, timestamp, IP address) at ingestion. |   1   |  D/V |
| **AC.8.5.2** | **Verify that** provenance metadata is retained and auditable for all processed inputs.                                  |   2   |  D/V |
| **AC.8.5.3** | **Verify that** anomalous or untrusted input sources are flagged and subject to enhanced scrutiny or blocking.           |   2   |  D/V |

---

## AC.9 Multimodal Validation, MLOps & Infrastructure Governance

### AC.9.1 Multimodal Security Validation Pipeline

|       #      | Description                                                                                                                                                                                                                              | Level | Role |
| :----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.1.1** | **Verify that** modality-specific content classifiers are updated according to documented schedules (minimum quarterly) with new threat patterns, adversarial examples, and performance benchmarks maintained above baseline thresholds. |   3   |  D/V |

### AC.9.2 CI/CD & Build Security

|       #      | Description                                                                                                                      | Level | Role |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.2.1** | **Verify that** infrastructure-as-code is scanned on every commit, and merges are blocked on critical or high-severity findings. |   1   |  D/V |
| **AC.9.2.2** | **Verify that** CI/CD pipelines use short-lived, scoped identities for access to secrets and infrastructure.                     |   2   |  D/V |
| **AC.9.2.3** | **Verify that** build environments are isolated from production networks and data.                                               |   2   |  D/V |

### AC.9.3 Container & Image Security

|       #      | Description                                                                                                                                                                   | Level | Role |
| :----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.3.1** | **Verify that** container images are scanned to block hardcoded secrets (e.g., API keys, credentials, certificates).                                                          |   2   |  D/V |
| **AC.9.3.2** | **Verify that** container images are scanned according to organizational schedules with CRITICAL vulnerabilities blocking deployment based on organizational risk thresholds. |   1   |  D/V |

### AC.9.4 Monitoring, Alerting & SIEM

|       #      | Description                                                                                                                                             | Level | Role |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.9.4.1** | **Verify that** security alerts integrate with SIEM platforms (Splunk, Elastic, or Sentinel) using CEF or STIX/TAXII formats with automated enrichment. |   2   |   V  |

### AC.9.5 Vulnerability Management

|       #      | Description                                                                                                                                                            | Level | Role |
| :----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.5.1** | **Verify that** HIGH severity vulnerabilities are patched according to organizational risk management timelines with emergency procedures for actively exploited CVEs. |   2   |  D/V |

### AC.9.6 Configuration & Drift Control

|       #      | Description                                                                                                                                                                                 | Level | Role |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **AC.9.6.1** | **Verify that** configuration drift is detected using tools (Chef InSpec, AWS Config) according to organizational monitoring requirements with automatic rollback for unauthorized changes. |   2   |  D/V |

### AC.9.7 Production Environment Hardening

|       #      | Description                                                                                                                                                                        | Level | Role |
| :----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.7.1** | **Verify that** production environments block SSH access, disable debug endpoints, and require change requests with organizational advance notice requirements except emergencies. |   2   |  D/V |

### AC.9.8 Release Promotion Gates

|       #      | Description                                                                                                                                          | Level | Role |
| :----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.8.1** | **Verify that** promotion gates include automated security tests (SAST, DAST, container scanning) with zero CRITICAL findings required for approval. |   2   |  D/V |

### AC.9.9 Workload, Capacity & Cost Monitoring

|       #      | Description                                                                                                                                                                                            | Level | Role |
| :----------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.9.1** | **Verify that** GPU/TPU utilization is monitored with alerts triggered at organizationally defined thresholds and automatic scaling or load balancing activated based on capacity management policies. |   1   |  D/V |
| **AC.9.9.2** | **Verify that** AI workload metrics (inference latency, throughput, error rates) are collected according to organizational monitoring requirements and correlated with infrastructure utilization.     |   1   |  D/V |
| **AC.9.9.3** | **Verify that** cost monitoring tracks spending per workload/tenant with alerts based on organizational budget thresholds and automated controls for budget overruns.                                  |   2   |   V  |
| **AC.9.9.4** | **Verify that** capacity planning uses historical data with organizationally defined forecasting periods and automated resource provisioning based on demand patterns.                                 |   3   |   V  |

### AC.9.10 Approvals & Audit Trails

|       #       | Description                                                                                                                                                          | Level | Role |
| :-----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.10.1** | **Verify that** environment promotion requires approval from organizationally defined authorized personnel with cryptographic signatures and immutable audit trails. |   1   |  D/V |

### AC.9.11 IaC Governance

|       #       | Description                                                                                                                                  | Level | Role |
| :-----------: | :------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.11.1** | **Verify that** infrastructure-as-code changes require peer review with automated testing and security scanning before merge to main branch. |   2   |  D/V |

### AC.9.12 Data Handling in Non-Production

|       #       | Description                                                                                                                                                                        | Level | Role |
| :-----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.12.1** | **Verify that** non-production data is anonymized according to organizational privacy requirements, synthetic data generation, or complete data masking with PII removal verified. |   2   |  D/V |

### AC.9.13 Backup & Disaster Recovery

|       #       | Description                                                                                                                                                                                | Level | Role |
| :-----------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.13.1** | **Verify that** infrastructure configurations are backed up according to organizational backup schedules to geographically separate regions with 3-2-1 backup strategy implementation.     |   1   |  D/V |
| **AC.9.13.2** | **Verify that** recovery procedures are tested and validated through automated testing according to organizational schedules with RTO and RPO targets meeting organizational requirements. |   2   |   V  |
| **AC.9.13.3** | **Verify that** disaster recovery includes AI-specific runbooks with model weight restoration, GPU cluster rebuilding, and service dependency mapping.                                     |   3   |   V  |

### AC.9.14 Compliance & Documentation

|       #       | Description                                                                                                                                                                   | Level | Role |
| :-----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.14.1** | **Verify that** infrastructure compliance is assessed according to organizational schedules against SOC 2, ISO 27001, or FedRAMP controls with automated evidence collection. |   2   |  D/V |
| **AC.9.14.2** | **Verify that** infrastructure documentation includes network diagrams, data flow maps, and threat models updated according to organizational change management requirements. |   2   |   V  |
| **AC.9.14.3** | **Verify that** infrastructure changes undergo automated compliance impact assessment with regulatory approval workflows for high-risk modifications.                         |   3   |  D/V |

### AC.9.15 Hardware & Supply Chain

|       #       | Description                                                                                                                                                                    | Level | Role |
| :-----------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.15.1** | **Verify that** AI accelerator firmware (GPU BIOS, TPU firmware) is verified with cryptographic signatures and updated according to organizational patch management timelines. |   2   |  D/V |
| **AC.9.15.2** | **Verify that** the AI hardware supply chain includes provenance verification with manufacturer certificates and tamper-evident packaging validation.                          |   3   |   V  |

### AC.9.16 Cloud Strategy & Portability

|       #       | Description                                                                                                                                                             | Level | Role |
| :-----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.16.1** | **Verify that** cloud vendor lock-in prevention includes portable infrastructure-as-code, standardized APIs, and data export capabilities with format conversion tools. |   3   |   V  |
| **AC.9.16.2** | **Verify that** multi-cloud cost optimization includes security controls preventing resource sprawl as well as unauthorized cross-cloud data transfer charges.          |   3   |   V  |

### AC.9.17 GitOps & Self-Healing

|       #       | Description                                                                                                                                              | Level | Role |
| :-----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.17.1** | **Verify that** GitOps repositories require signed commits with GPG keys and branch protection rules preventing direct pushes to main branches.          |   2   |  D/V |
| **AC.9.17.2** | **Verify that** self-healing infrastructure includes security event correlation with automated incident response and stakeholder notification workflows. |   3   |   V  |

### AC.9.18 Zero-Trust, Agents, Provisioning & Residency Attestation

|       #       | Description                                                                                                                                                | Level | Role |
| :-----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **AC.9.18.1** | **Verify that** cloud resource access includes zero-trust verification with continuous authentication.                                                     |   2   |  D/V |
| **AC.9.18.2** | **Verify that** automated infrastructure provisioning includes security policy validation with deployment blocking for non-compliant configurations.       |   2   |  D/V |
| **AC.9.18.3** | **Verify that** automated infrastructure provisioning validates security policies during CI/CD, with non-compliant configurations blocked from deployment. |   2   |  D/V |
| **AC.9.18.4** | **Verify that** data residency requirements are enforced by cryptographic attestation of storage locations.                                                |   3   |  D/V |
| **AC.9.18.5** | **Verify that** cloud provider security assessments include agent-specific threat modeling and risk evaluation.                                            |   3   |  D/V |

### AC.9.19 Access Control & Identity

|       #       | Description                                                                                                                                                | Level | Role |
| :-----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **5.1.3** | **Verify that** new principals undergo identity-proofing that is aligned with NIST 800-63-3 IAL-2 or equivalent standards before receiving production system access. | 2 | D |
| **5.1.4** | **Verify that** access reviews are conducted quarterly with automated detection of dormant accounts, credential rotation enforcement, and de-provisioning workflows. | 2 | V |
| **5.2.2** | **Verify that** least-privilege principles are enforced by default with service accounts starting at read-only permissions and documented business justification required for write access. | 1 | D/V |
| **5.3.3** | **Verify that** policy definitions are version-controlled, peer-reviewed, and validated through automated testing in CI/CD pipelines before production deployment. | 2 | D |
| **5.3.4** | **Verify that** policy evaluation results include decision rationales and are transmitted to SIEM systems for correlation analysis and compliance reporting. | 2 | V |
| **5.4.4** | **Verify that** policy evaluation latency is continuously monitored with automated alerts for timeout conditions that could enable authorization bypass. | 2 | V |
| **5.5.4** | **Verify that** redaction algorithms are deterministic, version-controlled, and maintain audit logs to support compliance investigations and forensic analysis. | 2 | V |
| **5.5.5** | **Verify that** high-risk redaction events generate adaptive logs that include cryptographic hashes of original content for forensic retrieval without data exposure. | 3 | V |
| **5.7.5** | **Verify that** agent error conditions and exception handling include capability scope information to support incident analysis and forensic investigation. | 3 | V |
| **5.4.2** | **Verify that** citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 1 | D/V |

### New Items to be Integrated Above

|       #       | Description                                                                                                                                                | Level | Role |
| :-----------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **2.3.3** | **Verify that** the allowed character set is regularly reviewed and updated to ensure it remains aligned with business requirements. | 2 | D/V |
