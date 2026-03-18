# C01: Training Data Integrity & Traceability

> **Source:** [`1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
> **Requirements:** 24 | **Sections:** 5

## Control Objective

Training data must be sourced, handled, and maintained in a way that preserves origin traceability, integrity, and quality. The core security concern is ensuring data has not been tampered with, poisoned, or corrupted. Security-relevant bias (e.g., skewed abuse-detection training data that allows attackers to bypass controls) is treated as a possible consequence of compromised or unvalidated data, not as a standalone control category.

> **Scope note -- bias.** AISVS addresses bias only where it introduces security risk (e.g., bypass of abuse detection, authentication heuristics, or automated trust decisions). Broader fairness governance requirements are out of scope; see ISO/IEC 42001 or the NIST AI RMF for general fairness and ethics guidance.

---

## Section Breakdown with Requirements

### C1.1 Training Data Origin & Traceability

Maintain a verifiable inventory of all datasets, accept only trusted sources, and log every change for auditability.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 1.1.1 | **Verify that** an up-to-date inventory of every training-data source (origin, responsible party, license, collection method, intended use constraints, and processing history) is maintained. | 1 | D/V | Supply-chain compromise via unknown or unvetted data sources; inability to trace poisoned data back to origin during incident response. | Review the data catalog or asset inventory system (e.g., DataHub, Amundsen, or internal registry). Confirm each dataset entry includes all six required metadata fields. Spot-check a sample of datasets against their listed sources. | Most organizations track datasets informally. Tooling like DataHub and MLflow supports metadata but does not enforce completeness. Manual audit remains necessary to verify all fields are populated and accurate. |
| 1.1.2 | **Verify that** training data processes exclude unnecessary features, attributes, or fields (e.g., unused metadata, sensitive PII, leaked test data). | 1 | D/V | Data leakage (test data in training sets causing inflated accuracy and masked vulnerabilities); PII exposure in model weights via memorization attacks; larger attack surface from unnecessary features. | Review data pipeline code and ETL configurations for feature selection steps. Confirm PII scanning tools (e.g., Microsoft Presidio, AWS Macie) are integrated. Verify test/validation holdout separation. | Automated PII detection has high false-negative rates for non-English text and domain-specific identifiers. Feature minimization is often a manual design decision with no automated enforcement. |
| 1.1.3 | **Verify that** all dataset changes are subject to a logged approval workflow. | 1 | D/V | Unauthorized data modification or injection; insider threat inserting poisoned samples; untracked drift in training data composition. | Inspect version control logs (DVC, LakeFS, or Git LFS) for dataset changes. Verify that an approval gate (PR review, ticket approval) exists before data merges. Check audit logs for completeness. | DVC and LakeFS provide versioning but do not natively enforce approval gates. Approval workflows typically require integration with CI/CD or ticketing systems (Jira, GitHub Issues). |
| 1.1.4 | **Verify that** datasets or subsets are watermarked or fingerprinted where feasible. | 3 | D/V | Unauthorized redistribution of proprietary datasets; difficulty attributing data in a trained model back to its source; detecting if stolen data was used in competitor models. | Check for implementation of dataset fingerprinting (e.g., radioactive data techniques, embedded statistical watermarks). Verify watermark detection tooling is available and tested. | Dataset watermarking is an active research area with limited production tooling. Radioactive data (Sablayrolles et al., 2020) demonstrated feasibility but adoption is minimal. No standardized watermarking scheme exists. This is appropriately Level 3. |

---

### C1.2 Training Data Security & Integrity

Restrict access to training data, encrypt it at rest and in transit, and validate its integrity to prevent tampering, theft, or data poisoning.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 1.2.1 | **Verify that** access controls protect training data storage and pipelines. | 1 | D/V | Unauthorized access leading to data theft, exfiltration of proprietary datasets, or injection of poisoned samples by unauthorized users. | Review IAM policies on data storage (S3 buckets, GCS, Azure Blob). Verify least-privilege access on pipeline orchestrators (Airflow, Kubeflow). Check for service account scoping. | Standard cloud IAM tooling is mature. The gap is in pipeline-level access control: most ML orchestrators have coarser-grained permissions than data storage layers. |
| 1.2.2 | **Verify that** all access to training data is logged, including user, time, and action. | 1 | D/V | Undetected insider threats; inability to perform forensic analysis after a data poisoning incident; compliance violations. | Verify cloud audit logs (AWS CloudTrail, GCP Audit Logs, Azure Monitor) are enabled for data storage. Check that pipeline access (reads/writes) is also captured. Confirm log retention policies. | Cloud-native logging is mature for storage access. Gap: pipeline-internal data access (e.g., a training script reading a dataset) is often not logged at the application layer. |
| 1.2.3 | **Verify that** training datasets are encrypted in transit and at rest, using current recommended cryptographic algorithms and key management practices. | 1 | D/V | Data theft via storage compromise or network interception; regulatory non-compliance for datasets containing PII or sensitive content. | Verify encryption-at-rest is enabled on all storage (SSE-S3, GCS default encryption, Azure Storage encryption). Check TLS enforcement for data transfers. Review KMS key rotation policies. | Cloud provider default encryption handles most cases. Gap: datasets cached locally on training nodes (GPU instances) may not be encrypted. Ephemeral storage on training VMs is often overlooked. |
| 1.2.4 | **Verify that** cryptographic hashes or digital signatures are used to ensure data integrity during training data storage and transfer. | 2 | D/V | Silent data corruption during transfer; man-in-the-middle modification of datasets; undetected tampering by compromised storage systems. | Check for SHA-256 (or stronger) hash manifests accompanying datasets. Verify hash validation is integrated into data loading pipelines. For signed datasets, verify signature validation against known keys. | Hashing individual files is straightforward. Gap: hashing large datasets (multi-TB) is computationally expensive and often skipped. Merkle-tree approaches can help but lack standardized tooling for ML datasets. Sigstore adoption for datasets is nascent. |
| 1.2.5 | **Verify that** automated integrity monitoring is applied to guard against unauthorized modifications or corruption of training data. | 2 | D/V | Slow-burn data poisoning where small modifications accumulate over time; bit-rot or storage corruption going undetected until model retraining. | Verify automated hash-check jobs run on a schedule or trigger. Check for file integrity monitoring (OSSEC, Tripwire) on data storage. Review alerting configuration for integrity violations. | FIM tools were designed for system files, not multi-TB datasets. Gap: purpose-built integrity monitoring for ML data stores is immature. Most teams implement custom scripts rather than using dedicated tooling. |
| 1.2.6 | **Verify that** obsolete training data is securely purged or anonymized. | 1 | D/V | Stale data containing PII or deprecated patterns persisting in storage; regulatory risk from GDPR/CCPA right-to-deletion requests; poisoned data surviving past remediation. | Review data retention policies and verify deletion procedures. Check for cryptographic erasure or secure deletion on storage. Confirm anonymization techniques (k-anonymity, differential privacy) where data is retained. | Secure deletion on cloud object storage is generally reliable. Gap: data that has been loaded into model weights cannot be "deleted" -- this is a fundamental limitation. Machine unlearning research is ongoing but not production-ready. |
| 1.2.7 | **Verify that** all training dataset versions are uniquely identified, stored immutably, and auditable to support rollback and forensic analysis. | 3 | D/V | Inability to reproduce training runs for audit; inability to roll back to pre-poisoning dataset state; loss of forensic evidence after security incident. | Verify dataset versioning system (DVC, LakeFS, Delta Lake) with immutable snapshots. Check that version IDs are cryptographically linked to content. Test rollback capability. | DVC and LakeFS support versioning well. Gap: true immutability requires append-only storage (e.g., S3 Object Lock, WORM storage), which adds cost and complexity. Most teams use soft-delete rather than true immutability. Level 3 is appropriate. |

---

### C1.3 Data Labeling and Annotation Security

Ensure labeling and annotation processes are access-controlled, auditable, and protect sensitive information.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 1.3.1 | **Verify that** labeling interfaces and platforms enforce access controls and maintain audit logs of all labeling activities. | 1 | D/V | Label-flipping attacks by malicious annotators; unauthorized access to sensitive data exposed through labeling interfaces; inability to trace labeling errors to source. | Review labeling platform (Label Studio, Labelbox, Scale AI) access control configuration. Verify audit logs capture annotator identity, timestamp, and label value for each action. | Commercial labeling platforms (Labelbox, Scale) have mature access controls. Open-source tools (Label Studio) have basic RBAC but audit logging may require additional configuration. Gap: crowdsourced labeling via platforms like MTurk has minimal per-annotator access control. |
| 1.3.2 | **Verify that** cryptographic hashes or digital signatures are applied to labeling artifacts and annotation data to ensure their integrity and authenticity. | 2 | D/V | Post-hoc tampering with labels after annotation is complete; disputed label provenance; integrity loss during label export and import between systems. | Check that exported annotation files have accompanying hash manifests. Verify that label databases use integrity checks. For high-assurance cases, check for digital signatures on annotation batches. | No major labeling platform natively produces signed annotation exports. This typically requires custom tooling to hash annotation JSON/CSV exports and store signatures. Gap: no standard format for signed annotation data. |
| 1.3.3 | **Verify that** labeling audit logs are tamper-evident and that labeling platforms protect against unauthorized modifications. | 2 | D/V | Attacker covering tracks after injecting malicious labels; insider modifying historical labels to introduce backdoors; regulatory audit failure due to unreliable records. | Verify audit logs are written to append-only storage or a tamper-evident log system (e.g., AWS QLDB, immutable blob storage). Test that label modifications create new log entries rather than overwriting. | Tamper-evident logging is well-understood but rarely applied to labeling platforms specifically. Gap: most labeling tools store audit logs in standard databases that an admin could modify. Requires architectural decisions at deployment time. |
| 1.3.4 | **Verify that** sensitive information in labels is redacted, anonymized, or encrypted using appropriate granularity at rest and in transit. | 2 | D/V | PII leakage through label values (e.g., named entity labels containing real names); sensitive content exposure to annotators without need-to-know; label data exfiltration revealing protected information. | Review label schemas for sensitive content categories. Verify PII redaction in label values and metadata. Check encryption of label storage and transmission. Review annotator access scoping to sensitive label categories. | Labels often contain or reference sensitive data (medical annotations, financial categories). Gap: automated PII detection in label values is less mature than in free-text fields. Domain-specific sensitivity (e.g., medical diagnoses as labels) requires custom classification rules. |

---

### C1.4 Training Data Quality and Security Assurance

Combine automated validation, manual spot-checks, and logged remediation to guarantee dataset reliability.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 1.4.1 | **Verify that** automated tests catch format errors and nulls on every ingest or significant data transformation. | 1 | D | Malformed data causing silent training failures or model degradation; injection of adversarial samples disguised as corrupted records; data pipeline reliability issues masking security problems. | Review data validation code in ingest pipelines. Check for schema validation tools (Great Expectations, Pandera, TFX Data Validation). Verify tests run in CI/CD on every data change. | Great Expectations and Pandera are mature for tabular data. Gap: schema validation for unstructured data (images, audio, text) is less standardized. Format validation does not catch semantically poisoned but syntactically valid data. |
| 1.4.2 | **Verify that** training and fine-tuning pipelines implement data integrity validation and poisoning detection techniques (e.g., statistical analysis, outlier detection, embedding analysis) to identify potential data poisoning or unintentional corruption in training data. | 2 | D/V | Data poisoning attacks (backdoor injection, triggerless poisoning); distribution shift from corrupted data sources; subtle manipulation of training signal by adversaries. | Verify integration of poisoning detection tools (Cleanlab, ART poisoning detectors). Check for statistical distribution monitoring on incoming data. Review outlier detection thresholds and alerting. Test with known poisoned samples. | Cleanlab is effective for label error detection. IBM ART provides poisoning defense implementations. Gap: no single tool reliably detects all poisoning attack types. Triggerless poisoning and clean-label attacks remain difficult to detect. Detection rates vary significantly by data modality and attack sophistication. |
| 1.4.3 | **Verify that** automatically generated labels (e.g., via models or weak supervision) are subject to confidence thresholds and consistency checks to detect misleading or low-confidence labels. | 2 | D/V | Propagation of model errors into training data (feedback loops); adversarial manipulation of auto-labeling models to inject systematic mislabels; quality degradation from overreliance on weak supervision. | Review auto-labeling pipeline configuration for confidence thresholds. Verify consistency checks (e.g., cross-model agreement, temporal stability). Check for human review sampling rates on auto-generated labels. | Snorkel and similar weak supervision frameworks support confidence thresholds. Gap: determining appropriate confidence thresholds is domain-specific and often set arbitrarily. No standard methodology for validating auto-label quality at scale. Model collapse risk from recursive auto-labeling is an emerging concern. |
| 1.4.4 | **Verify that** appropriate defenses, such as adversarial training, data augmentation with perturbed inputs, or robust optimization techniques, are implemented and tuned for relevant models based on risk assessment. | 3 | D/V | Adversarial evasion attacks at inference time; model brittleness to distribution shifts; targeted attacks exploiting known model weaknesses. | Review model training code for adversarial training components (PGD-AT, TRADES). Check for adversarial data augmentation in the pipeline. Verify robustness evaluation on adversarial test sets. Review risk assessment justifying chosen defenses. | IBM ART and Foolbox provide adversarial training utilities. Gap: adversarial training significantly increases compute cost (2-10x) and can reduce clean accuracy. Robustness-accuracy tradeoff is well-documented but poorly tooled for automated tuning. Appropriately Level 3 due to complexity and cost. |
| 1.4.5 | **Verify that** automated tests catch label skews on every ingest or significant data transformation. | 2 | D | Class imbalance introduced by poisoning (flooding one class to shift decision boundaries); drift in label distributions indicating data pipeline compromise; adversarial manipulation of class proportions to weaken minority-class detection. | Check for label distribution monitoring in data pipelines. Verify statistical tests (chi-squared, KL divergence) are applied to incoming label distributions. Review alerting thresholds for distribution shifts. | Great Expectations can monitor value distributions. Gap: distinguishing malicious label skew from legitimate distribution shift requires domain context. No automated tool reliably separates intentional rebalancing from adversarial manipulation. Threshold tuning is manual and domain-specific. |
| 1.4.6 | **Verify that** models used in security-relevant decisions (e.g., abuse detection, fraud scoring, automated trust decisions) are evaluated for systematic bias patterns that an adversary could exploit to evade controls (e.g., mimicking a trusted language style or demographic pattern to bypass detection). | 2 | D/V | Adversarial exploitation of demographic or stylistic biases in security models; evasion of abuse detection by mimicking patterns the model undertreats; systematic blind spots in fraud detection that attackers can discover and exploit. | Review bias evaluation reports for security-critical models. Verify adversarial probing for exploitable bias patterns (e.g., testing if certain language styles evade content filters). Check for disaggregated performance metrics across relevant subgroups. | Fairlearn and AI Fairness 360 provide bias measurement but focus on fairness, not security exploitation. Gap: no dedicated tooling exists for evaluating "security-exploitable bias" specifically. This requires red-team exercises combining fairness analysis with adversarial testing. Methodology is ad-hoc across the industry. |

---

### C1.5 Data Lineage and Traceability

Track the full journey of each dataset from source to model input for auditability and incident response.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 1.5.1 | **Verify that** the lineage of each dataset and its components, including all transformations, augmentations, and merges, is recorded and can be reconstructed. | 1 | D/V | Inability to trace poisoned data back through the pipeline; undetectable introduction of malicious transformations; failure to reproduce training conditions for incident investigation. | Review lineage tracking system (Apache Atlas, DataHub, MLflow, custom metadata stores). Verify that each transformation step is logged with input/output dataset references. Test reconstruction of a sample dataset's full history. | MLflow and DVC track experiment-level lineage. Apache Atlas and DataHub provide richer graph-based lineage. Gap: fine-grained per-sample lineage (tracking individual records through transformations) is computationally expensive and rarely implemented. Most tools track dataset-level, not record-level lineage. |
| 1.5.2 | **Verify that** lineage records are immutable, securely stored, and accessible for audits. | 2 | D/V | Tampering with lineage records to cover tracks after data poisoning; loss of audit trail due to storage failure; disputed provenance during regulatory investigation. | Verify lineage metadata is stored in append-only or immutable storage. Check access controls on lineage databases. Test that lineage records cannot be modified or deleted by pipeline operators. Verify backup and retention policies. | Immutable storage options exist (S3 Object Lock, Azure immutable blobs). Gap: lineage metadata systems (Atlas, DataHub) typically use mutable databases. Achieving true immutability requires architectural decisions that most lineage tools do not enforce by default. |
| 1.5.3 | **Verify that** lineage tracking covers synthetic data generated via augmentation, synthesis, or privacy-preserving techniques and that all synthetic data is clearly labeled and distinguishable from real data throughout the pipeline. | 2 | D/V | Synthetic data contamination obscuring real data quality issues; inability to trace model behaviors to real vs. synthetic training examples; privacy violations if synthetic data retains real-data characteristics without proper tracking. | Review lineage records for synthetic data generation steps. Verify synthetic data carries metadata tags distinguishing it from real data. Check that downstream consumers can filter by data origin type. | Synthetic data generation tools (Gretel, MOSTLY AI, SDV) produce data but rarely integrate with lineage systems. Gap: no standard metadata schema for marking data as synthetic. When synthetic and real data are merged, distinguishability is often lost. This is an emerging best practice without mature tooling support. |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Data poisoning attacks** -- backdoor injection via mislabeled samples (BadNets, Trojan attacks); clean-label attacks that poison without changing labels; triggerless attacks that avoid detectable trigger patterns
- **Training data extraction / memorization attacks** -- adversaries query models to extract verbatim training data (Carlini et al., 2021 demonstrated extraction from GPT-2)
- **Supply chain compromise of public datasets** -- manipulation of Common Crawl, LAION, or other open datasets that are widely used without verification
- **Label-flipping attacks on crowdsourced annotation pipelines** -- malicious annotators systematically mislabel samples to introduce targeted biases
- **Data ordering attacks** -- manipulating the sequence of training data to influence gradient updates without changing data content

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2017 | BadNets: Identifying Vulnerabilities in the ML Supply Chain (Gu et al.) | Foundational backdoor poisoning attack via training data | [arXiv:1708.06733](https://arxiv.org/abs/1708.06733) |
| 2020 | Radioactive Data: Tracing Through Training (Sablayrolles et al.) | Dataset fingerprinting technique relevant to C1.1.4 | [arXiv:2002.00937](https://arxiv.org/abs/2002.00937) |
| 2021 | Extracting Training Data from Large Language Models (Carlini et al.) | Demonstrated verbatim training data extraction from GPT-2 | [arXiv:2012.07805](https://arxiv.org/abs/2012.07805) |
| 2023 | Poisoning Web-Scale Training Datasets is Practical (Carlini et al.) | Showed practical poisoning of large web-scraped datasets | [arXiv:2302.10149](https://arxiv.org/abs/2302.10149) |
| 2024 | Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Models | Targeted poisoning attack against diffusion models | [IEEE S&P 2024](https://arxiv.org/abs/2310.13828) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Data provenance:** DVC (Data Version Control), MLflow data tracking, LakeFS, Delta Lake
- **Poisoning detection:** Cleanlab, IBM Adversarial Robustness Toolbox (ART), statistical outlier detection
- **Data integrity:** Cryptographic hashing (SHA-256), Sigstore for dataset signing, Great Expectations
- **Lineage:** Apache Atlas, Amundsen, DataHub, MLflow
- **PII detection:** Microsoft Presidio, AWS Macie, Google Cloud DLP
- **Labeling platforms:** Label Studio, Labelbox, Scale AI, Snorkel
- **Bias evaluation:** Fairlearn, AI Fairness 360, custom red-team probing
- **Adversarial robustness:** IBM ART, Foolbox, CleverHans

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C1.1 Training Data Origin & Traceability | Medium | Data catalogs exist (DataHub, Amundsen) but metadata completeness enforcement is manual. Dataset watermarking (1.1.4) is research-stage. |
| C1.2 Training Data Security & Integrity | High | Cloud-native encryption and IAM are mature. Gaps in pipeline-level access control and large-scale integrity monitoring. Immutable versioning (1.2.7) adds cost. |
| C1.3 Data Labeling and Annotation Security | Medium-Low | Commercial labeling platforms have basic RBAC and logging. Cryptographic signing of annotations (1.3.2) and tamper-evident logs (1.3.3) require custom implementation. |
| C1.4 Training Data Quality and Security Assurance | Medium | Schema validation is mature for tabular data. Poisoning detection is improving but incomplete. Adversarial training (1.4.4) is computationally expensive. Security-exploitable bias evaluation (1.4.6) lacks dedicated tooling. |
| C1.5 Data Lineage and Traceability | Medium | Dataset-level lineage is supported by multiple tools. Record-level lineage and synthetic data tracking are immature. Immutable lineage storage requires deliberate architecture. |

---

## Open Research Questions

- [ ] How do you verify data integrity for datasets too large to hash in full? (Merkle-tree and sampling approaches exist but lack standardization)
- [ ] What is the state of automated poisoning detection for multimodal datasets? (Most tooling targets tabular or image data; text and audio poisoning detection is less developed)
- [ ] How should organizations handle training data provenance for foundation models they did not train? (Model cards and data cards help but are not verifiable)
- [ ] What constitutes adequate label quality assurance for adversarial-risk-sensitive domains? (No industry consensus on sampling rates or acceptance thresholds)
- [ ] Can machine unlearning satisfy data deletion requirements (C1.2.6) for data embedded in model weights? (Research is active but no production-ready solutions exist)
- [ ] How should synthetic data lineage be standardized across generation tools and ML pipelines? (No common metadata schema exists)

---

## Related Standards & Cross-References

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act: Article 10: Data & Data Governance](https://artificialintelligenceact.eu/article/10/)
- [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
- [OpenAI Privacy Center: Data Deletion Controls](https://privacy.openai.com/policies?modal=take-control)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C02 (Data Processing) | Pipeline integrity, transformation validation | C1 covers training data; C2 covers inference-time data processing. Shared concern: pipeline access controls and integrity checks. |
| C03 (Model Architecture) | Adversarial robustness | C1.4.4 (adversarial training) relates to model-level robustness controls in C3. |
| C05 (Supply Chain) | Third-party data sources, pre-trained model provenance | C1.1.1 (data inventory) overlaps with supply chain tracking of external datasets. |
| C08 (Privacy) | PII in training data, data deletion, memorization | C1.1.2 (feature minimization) and C1.2.6 (data purging) directly relate to privacy controls. |

---

## Community Notes

_Space for contributor observations, discussion, and context that does not fit elsewhere._

---
