# C12: Privacy Protection & Personal Data Management

> **Source:** [`1.0/en/0x10-C12-Privacy.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C12-Privacy.md)
> **Requirements:** 23 | **Sections:** 6

## Control Objective

Maintain rigorous privacy assurances across the entire AI lifecycle (collection, training, inference, and incident response) so that personal data is only processed with clear consent, minimum necessary scope, provable erasure, and formal privacy guarantees.

---

## C12.1 Anonymization & Data Minimization

Remove or transform personal identifiers before training to prevent re-identification and minimize privacy exposure.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **12.1.1** | Verify that direct and quasi-identifiers are removed, hashed. | 1 | D/V | Training data memorization causing PII leakage in model outputs (e.g., GPT-2 memorizing SSNs, phone numbers). Naranjo et al. (2023) showed LLMs can regurgitate verbatim PII from training corpora. | Run PII scanners (Microsoft Presidio, Google DLP API, spaCy NER) across training data and sample model outputs. Confirm zero direct identifiers and that quasi-identifiers are hashed or generalized. Spot-check with membership inference probes. | Hashing alone may not prevent linkage attacks if the hash space is small or deterministic. Salted hashing or tokenization with a secure vault is preferable. Quasi-identifier combinations (ZIP + DOB + gender) require k-anonymity assessment beyond simple removal. |
| **12.1.2** | Verify that automated audits measure k-anonymity/l-diversity and alert when thresholds drop below policy. | 2 | D/V | Re-identification via linkage attacks on quasi-identifiers. Sweeney (2000) demonstrated that 87% of the US population can be uniquely identified by ZIP, gender, and date of birth alone. | Deploy automated k-anonymity/l-diversity measurement tools (e.g., ARX Data Anonymization Tool, sdcMicro) in CI/CD pipelines. Set policy thresholds (e.g., k >= 5, l >= 3) and verify alerts fire on threshold breach. Review alert history logs. | Thresholds vary by jurisdiction and sensitivity level. k-anonymity alone is vulnerable to homogeneity attacks; l-diversity and t-closeness provide stronger guarantees. Continuous monitoring is needed as datasets evolve. |
| **12.1.3** | Verify that model feature-importance reports prove no identifier leakage beyond epsilon = 0.01 mutual information. | 2 | V | Indirect leakage through model features that are proxies for personal identifiers. Feature importance analysis can reveal if the model has learned to rely on identity-correlated attributes. | Compute mutual information between model hidden representations and known identifiers using SHAP, LIME, or dedicated MI estimation libraries. Verify MI < 0.01 threshold. Run across validation splits to ensure consistency. | Mutual information estimation is computationally expensive and can be unreliable in high-dimensional spaces. The epsilon = 0.01 threshold may need calibration per domain. Deep models may encode identifiers in distributed representations that are hard to detect via standard feature-importance methods. |
| **12.1.4** | Verify that formal proofs or synthetic-data certification show re-identification risk <= 0.05 even under linkage attacks. | 3 | V | Sophisticated linkage attacks combining the anonymized dataset with external data sources (voter rolls, social media, commercial databases). | Request formal privacy proofs (e.g., based on differential privacy composition theorems) or synthetic data utility/privacy certificates from tools like Synthetic Data Vault (SDV), MOSTLY AI, or Gretel. Validate with red-team linkage attacks using auxiliary datasets. | Formal proofs are rare outside academic settings and often rely on assumptions (e.g., bounded auxiliary information) that may not hold. Synthetic data can still leak properties of outliers. The 0.05 threshold is aggressive and may require significant data utility tradeoffs. |

---

## C12.2 Right-to-be-Forgotten & Deletion Enforcement

Ensure data-subject deletion requests propagate across all AI artifacts and that model unlearning is verifiable.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **12.2.1** | Verify that data-subject deletion requests propagate to raw datasets, checkpoints, embeddings, logs, and backups within SLAs of less than 30 days. | 1 | D/V | GDPR Article 17 and CCPA deletion right violations. Regulators have issued significant fines for incomplete deletion (e.g., Italian DPA fined Clearview AI EUR 20M for failure to delete biometric data). | Audit deletion workflow end-to-end: submit test deletion requests, then verify removal from all storage tiers (raw data, feature stores, model checkpoints, vector databases, embeddings caches, logs, backups). Measure time-to-completion against the 30-day SLA. | Model checkpoints and embeddings are often overlooked in deletion workflows. Backup retention policies may conflict with deletion SLAs. Vector databases (Pinecone, Weaviate, Milvus) require special handling to remove individual embeddings. Distributed systems with replication add propagation complexity. |
| **12.2.2** | Verify that "machine-unlearning" routines physically re-train or approximate removal using certified unlearning algorithms. | 2 | D | Residual memorization of deleted data in model weights. Even after data deletion, a model may still generate outputs influenced by the removed data, violating the spirit of erasure rights. | Review implementation of unlearning algorithms: SISA training (Bourtoule et al., 2021), certified removal mechanisms (Guo et al., 2020), or fine-tuning-based approximate unlearning. Verify that the unlearning procedure is documented and that before/after membership inference attack success rates are measured. | Machine unlearning is still largely a research area. SISA training requires sharding data upfront, which adds architectural complexity. Approximate unlearning methods (gradient ascent, Fisher forgetting) lack formal guarantees for large models. Full retraining remains the gold standard but is prohibitively expensive for foundation models. |
| **12.2.3** | Verify that shadow-model evaluation proves forgotten records influence less than 1% of outputs after unlearning. | 2 | V | Incomplete unlearning leaving residual influence from deleted records. Membership inference attacks (Shokri et al., 2017) can detect whether a specific record was in the training set. | Train shadow models on datasets with and without the forgotten records. Compare membership inference attack accuracy, output distributions, and per-sample loss values. The forgotten records should be statistically indistinguishable from never-seen records (influence < 1%). | Shadow-model evaluation is compute-intensive, requiring training multiple reference models. The 1% threshold needs careful statistical testing (e.g., hypothesis tests with sufficient power). For LLMs, measuring "influence on outputs" is harder than for classifiers since output spaces are vast. |
| **12.2.4** | Verify that deletion events are immutably logged and auditable for regulators. | 3 | V | Inability to demonstrate compliance with deletion requests to regulators during audits. Without immutable logs, organizations cannot prove they processed requests within required timeframes. | Inspect audit trail infrastructure: verify logs are append-only (e.g., using write-once storage, blockchain-anchored hashes, or tamper-evident logging like AWS CloudTrail with integrity validation). Confirm logs capture request receipt timestamp, processing steps, and completion confirmation. Attempt log tampering to verify immutability. | Logging deletion events creates a tension: the log itself contains information about the data subject (at minimum, that they existed and requested deletion). Logs must be designed to record compliance actions without creating a new privacy exposure. Retention periods for audit logs must also be defined. |

---

## C12.3 Differential-Privacy Safeguards

Track and enforce privacy budgets to provide formal guarantees against individual data leakage.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **12.3.1** | Verify that differential privacy budget consumption is tracked per training round (both epsilon and delta values) and that cumulative budget dashboards alert when epsilon exceeds policy thresholds. | 2 | D/V | Unbounded privacy leakage through repeated queries or training rounds. Without budget tracking, the cumulative epsilon can grow without limit, degrading privacy guarantees to meaninglessness. The Fundamental Law of Information Recovery (Dwork & Roth, 2014) shows that too many adaptive queries destroy privacy. | Inspect DP implementation (Opacus for PyTorch, TensorFlow Privacy for TF). Verify per-round epsilon/delta accounting using RDP (Renyi Differential Privacy) or GDP (Gaussian DP) accountants. Check dashboard alerts fire at configured thresholds. Review historical budget consumption logs. | Choosing meaningful epsilon thresholds is an open problem. Apple uses epsilon = 2-8 for telemetry; US Census used epsilon ~ 19.6 (controversial). Very low epsilon values (< 1) typically destroy model utility for complex tasks. The "right" epsilon depends heavily on the threat model, data sensitivity, and acceptable utility loss. |
| **12.3.2** | Verify that black-box privacy audits estimate epsilon-hat within 10% of declared value. | 2 | V | Discrepancy between claimed and actual privacy guarantees. Implementation bugs in DP mechanisms (e.g., floating-point vulnerabilities in Gaussian noise, incorrect sensitivity calibration) can silently void privacy guarantees. Mironov (2012) showed that floating-point arithmetic can break DP. | Run black-box auditing tools (e.g., DP-Sniper, privacy auditing via membership inference as in Jagielski et al., 2020). Generate empirical epsilon estimates by measuring distinguishability of outputs on neighboring datasets. Compare estimated epsilon-hat against declared epsilon. Ensure |epsilon-hat - epsilon| / epsilon < 0.10. | Black-box auditing provides lower bounds on privacy leakage; it cannot prove the system is private, only detect when it is not. Tight auditing requires many queries and is expensive. The 10% tolerance is ambitious for complex pipelines. Composition across multiple DP mechanisms compounds estimation difficulty. |
| **12.3.3** | Verify that formal proofs cover all post-training fine-tunes and embeddings. | 3 | V | Privacy budget exhaustion through fine-tuning. Each fine-tuning round consumes additional privacy budget. If fine-tuning and embedding extraction are not accounted for, the total epsilon can far exceed what was budgeted during initial training. | Request formal privacy analysis documentation covering the full pipeline: pre-training, fine-tuning (including RLHF, DPO), embedding extraction, and any downstream adaptation. Verify that composition theorems (sequential, parallel, advanced) are correctly applied across all stages. | Most DP tooling focuses on training-time guarantees. Fine-tuning with DP (DP-LoRA, DP-adapter methods) is an active research area. Embedding extraction is rarely covered by formal analysis. Post-deployment inference queries also consume budget under some threat models but are typically excluded from analysis. |
| **12.3.4** | Verify that federated learning systems implement canary-based privacy auditing to empirically bound privacy leakage, with audit results logged and reviewed per training cycle. | 3 | V | Undetected privacy leakage in federated learning where data never leaves client devices but gradient updates can still leak sensitive information. Canary insertion (Carlini et al., 2019) is one of the few practical methods to empirically measure memorization. | Verify that canary records (synthetic records with known properties) are inserted into training. Measure canary exposure metric (log-perplexity rank of canary among random alternatives). Review per-cycle audit logs showing canary exposure trends. Confirm exposure remains below defined thresholds. | Canary-based auditing measures memorization of specific inserted records, not general privacy leakage. It provides a lower bound on leakage. The number and design of canaries affects detection sensitivity. In federated settings, canaries must be inserted at individual clients, adding coordination complexity. |

---

## C12.4 Purpose-Limitation & Scope-Creep Protection

Prevent models and datasets from being used beyond their originally consented purpose.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **12.4.1** | Verify that every dataset and model checkpoint carries a machine-readable purpose tag aligned to the original consent. | 1 | D | Purpose creep violating GDPR Article 5(1)(b) purpose limitation principle. Without explicit purpose tags, models trained on data collected for one purpose can be silently repurposed (e.g., a customer service chatbot model reused for credit scoring). | Inspect dataset and model metadata schemas for machine-readable purpose fields (e.g., using Data Cards, Model Cards, or custom metadata). Verify tags align with consent records in the CMP. Sample datasets and checkpoints to confirm tags are present and populated. | No universally adopted standard for machine-readable purpose tags exists yet. Hugging Face Model Cards and Google Data Cards provide templates but are not enforceable. Purpose definitions can be ambiguous (e.g., "improve services" is too broad). Integration with consent management systems requires custom plumbing. |
| **12.4.2** | Verify that runtime monitors detect queries inconsistent with declared purpose and trigger soft refusal. | 1 | D/V | Misuse of deployed models for purposes outside the original consent scope. For example, using a medical diagnosis model for insurance underwriting, or a fraud detection model for employee surveillance. | Submit test queries that fall outside the declared purpose scope and verify the system detects and refuses them. Review the classification logic used to determine purpose alignment (e.g., topic classifiers, intent detection). Verify refusal responses are informative but do not leak internal policy details. | Defining "inconsistent with declared purpose" programmatically is challenging. Simple keyword-based filters are easily bypassed. ML-based intent classifiers add complexity and their own failure modes. "Soft refusal" (vs hard block) allows some flexibility but may not satisfy strict regulatory interpretations of purpose limitation. |
| **12.4.3** | Verify that policy-as-code gates block redeployment of models to new domains without DPIA review. | 3 | D | Redeployment of models to new use cases without conducting a Data Protection Impact Assessment (DPIA) as required by GDPR Article 35. A model trained on one population or use case can introduce bias and privacy risks when applied to a different domain. | Review CI/CD pipeline configurations for policy-as-code gates (e.g., Open Policy Agent, HashiCorp Sentinel). Attempt to deploy a model to a new domain tag without DPIA approval and verify the gate blocks deployment. Check approval workflow records for completeness. | Policy-as-code for ML model deployment is emerging but immature. Defining "new domain" programmatically requires a domain taxonomy. DPIA review is inherently a human process; the gate can enforce that it happened but not that it was thorough. Integration with MLOps platforms (MLflow, Kubeflow, SageMaker) varies. |
| **12.4.4** | Verify that formal traceability proofs show every personal data lifecycle remains within consented scope. | 3 | V | Data lineage gaps allowing personal data to flow through undocumented processing paths. Without end-to-end traceability, organizations cannot demonstrate compliance with data protection regulations during audits. | Request data lineage documentation and verify it covers the full lifecycle: collection, preprocessing, training, validation, deployment, inference, archival, deletion. Use data lineage tools (Apache Atlas, OpenLineage, Marquez) to trace specific records. Validate that every processing step maps to a consented purpose. | Full formal traceability from raw data through model weights to inference outputs is aspirational for complex ML pipelines. Data lineage tools track dataset-level lineage but rarely track individual record flows through model training. Foundation models trained on web-scale data make per-record traceability infeasible. |

---

## C12.5 Consent Management & Lawful-Basis Tracking

Record, enforce, and revoke consent across AI processing pipelines.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **12.5.1** | Verify that a Consent-Management Platform (CMP) records opt-in status, purpose, and retention period per data-subject. | 1 | D/V | Processing personal data without valid legal basis, violating GDPR Articles 6-7. Without centralized consent tracking, organizations cannot demonstrate lawful basis for AI training data, leading to regulatory exposure (e.g., OpenAI's GDPR complaints in multiple EU jurisdictions). | Inspect CMP implementation (OneTrust, TrustArc, Cookiebot, or custom). Verify it records: consent timestamp, specific purposes consented to, retention period, withdrawal mechanism. Sample consent records and cross-reference with data processing activities. Test consent withdrawal flow end-to-end. | Most CMPs were designed for web cookie consent, not ML training pipelines. Integrating consent status checks into data loading pipelines requires custom development. Consent for AI training is evolving legally; the distinction between "legitimate interest" and "consent" as lawful bases for AI training is actively litigated in Europe. |
| **12.5.2** | Verify that APIs expose consent tokens; models must validate token scope before inference. | 2 | D | Inference on data where consent has been withdrawn or was never granted for the specific processing purpose. Without runtime consent validation, models continue to process data even after subjects revoke consent. | Review API specifications for consent token endpoints. Test that inference requests without valid consent tokens are rejected. Verify token scope validation logic checks both the data subject's consent status and the specific purpose. Test with expired, revoked, and scope-mismatched tokens. | Real-time consent token validation adds latency to inference. Token architecture must handle scale (millions of subjects) without becoming a bottleneck. Consent token revocation propagation across distributed systems requires careful cache invalidation design. No industry standard exists for AI-specific consent token formats. |
| **12.5.3** | Verify that denied or withdrawn consent halts processing pipelines within 24 hours. | 2 | D/V | Continued processing after consent withdrawal, violating GDPR Article 7(3) which requires withdrawal to be as easy as giving consent. Delayed processing halt means data continues to be used without lawful basis. | Withdraw consent via the CMP and measure time until all processing pipelines halt for that data subject. Verify across training pipelines, inference endpoints, batch jobs, and analytics. Check that 24-hour SLA is monitored and alerting is configured for breaches. | The 24-hour window is tighter than many batch processing schedules. Long-running training jobs may need to be interrupted and restarted. Streaming pipelines can halt quickly, but batch ETL jobs and scheduled retraining may not check consent status frequently enough. Coordination across microservices and data platforms adds complexity. |

---

## C12.6 Federated Learning with Privacy Controls

Apply differential privacy and poisoning-resistant aggregation to federated learning to protect individual participant data.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **12.6.1** | Verify that client updates employ local differential privacy noise addition before aggregation. | 1 | D | Gradient inversion attacks reconstructing training data from gradient updates. Zhu et al. (2019) demonstrated that shared gradients in federated learning can be inverted to reconstruct training images with high fidelity. Even text data can be recovered from gradients (Deng et al., 2021). | Inspect client-side code for DP noise injection (Gaussian or Laplacian mechanism) applied to gradient updates before transmission. Verify noise calibration matches declared epsilon. Test by capturing updates with and without noise and confirming statistical indistinguishability at the claimed privacy level. | Local DP adds more noise per update than central DP, requiring more participants to maintain model quality. Noise calibration depends on gradient clipping bounds, which affect both privacy and convergence. Too aggressive clipping harms utility; too little reduces privacy. Frameworks: PySyft, TensorFlow Federated, Flower all support local DP but with varying maturity. |
| **12.6.2** | Verify that training metrics are differentially private and never reveal single-client loss. | 2 | D/V | Loss value leakage enabling membership inference. Per-client loss values can reveal whether specific data points were used in training and can be exploited for property inference attacks (Melis et al., 2019). Aggregated but unprotected metrics can still leak information about outlier clients. | Review metric aggregation code to verify DP noise is applied before reporting. Attempt to isolate single-client contributions from aggregated metrics. Verify that metric dashboards and logging systems do not record per-client loss values. Test with a known outlier client and verify its influence is masked. | Noisy metrics make debugging and monitoring harder. Organizations need to balance observability with privacy. Secure aggregation protocols (Bonawitz et al., 2017) provide an alternative to noise-based protection for metrics but require more complex infrastructure. Metric privacy is often overlooked in federated learning deployments. |
| **12.6.3** | Verify that poisoning-resistant aggregation (e.g., Krum/Trimmed-Mean) is enabled. | 2 | V | Byzantine poisoning attacks where malicious clients submit crafted gradient updates to corrupt the global model. Blanchard et al. (2017) showed that a single malicious participant can control the global model with standard FedAvg aggregation. Backdoor attacks via poisoning are particularly dangerous. | Review aggregation algorithm configuration. Verify that robust aggregation is used (Multi-Krum, Trimmed-Mean, coordinate-wise median, or FLTrust). Test with simulated poisoning clients submitting adversarial updates and verify the aggregation resists corruption. Measure model accuracy with and without poisoning defenses. | No single robust aggregation method defends against all attack types. Krum is effective against Byzantine failures but may reduce convergence speed. Trimmed-Mean assumes a known fraction of malicious clients. Adaptive attacks can bypass fixed defense strategies. Defense selection should be informed by the threat model (honest-but-curious vs. actively malicious clients). |
| **12.6.4** | Verify that formal proofs demonstrate overall epsilon budget with less than 5% utility loss. | 3 | V | Excessive utility degradation from privacy mechanisms rendering the model ineffective. If privacy controls destroy model accuracy, practitioners are incentivized to weaken or disable them. Formal analysis ensures the privacy-utility tradeoff is explicitly quantified and acceptable. | Request formal privacy analysis with utility impact assessment. Verify epsilon budget is calculated using tight composition (RDP, zCDP, or PLD accountants). Compare model accuracy metrics (e.g., F1, AUC, perplexity) between DP and non-DP training runs. Confirm utility loss is within the 5% threshold. | The 5% utility loss threshold is application-dependent; for safety-critical applications even 1% may be unacceptable, while for recommendations 10% might be tolerable. Tight composition accounting (Renyi DP, Gaussian DP, Privacy Loss Distributions) can significantly reduce the reported epsilon vs. naive composition. Research is rapidly evolving on achieving better privacy-utility tradeoffs through DP-FTRL, DP-Adam optimizers, and large-batch training. |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Training data memorization leaking PII in model outputs
- Re-identification attacks on anonymized training data
- Inability to truly 'forget' data already learned by a trained model (machine unlearning gap)
- Scope creep — data collected for one purpose being used for model training
- Cross-border data transfer violations in distributed training setups

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2017 | Shokri et al. — Membership Inference Attacks Against Machine Learning Models | Foundational work showing ML models leak training set membership | [Paper](https://arxiv.org/abs/1610.05820) |
| 2019 | Zhu et al. — Deep Leakage from Gradients | Demonstrated pixel-accurate reconstruction of training images from shared gradients in federated learning | [Paper](https://arxiv.org/abs/1906.17744) |
| 2019 | Carlini et al. — The Secret Sharer: Evaluating and Testing Unintended Memorization | Canary-based methodology for measuring memorization in neural networks | [Paper](https://arxiv.org/abs/1802.08232) |
| 2021 | Carlini et al. — Extracting Training Data from Large Language Models | Showed GPT-2 memorizes and regurgitates PII, code, and other training data | [Paper](https://arxiv.org/abs/2012.07805) |
| 2021 | Bourtoule et al. — Machine Unlearning (SISA Training) | Proposed sharded training to enable efficient data removal without full retraining | [Paper](https://arxiv.org/abs/1912.03817) |
| 2022 | Italian DPA — Clearview AI fine (EUR 20M) | Fined for GDPR violations including failure to honor deletion requests for biometric data | [Decision](https://www.garanteprivacy.it/) |
| 2023 | Italian DPA — Temporary ban on ChatGPT | Raised questions about lawful basis for processing personal data in LLM training | [Coverage](https://www.bbc.com/news/technology-65139406) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Differential privacy:** Opacus, TensorFlow Privacy, Google DP Library
- **PII detection:** Presidio (Microsoft), spaCy NER, Google DLP API
- **Machine unlearning:** SISA training, approximate unlearning methods (research-stage)
- **Federated learning:** PySyft, TensorFlow Federated, Flower
- **Consent management:** OneTrust, TrustArc (integrated with ML pipelines)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C12.1 Anonymization & Data Minimization | Medium | PII detection tools are mature; automated k-anonymity auditing requires custom integration. Synthetic data tools (SDV, Gretel, MOSTLY AI) are production-ready but privacy guarantees vary. |
| C12.2 Right-to-be-Forgotten & Deletion Enforcement | Low | Machine unlearning remains research-stage for large models. SISA training is the most practical approach but requires architectural commitment upfront. Full retraining is reliable but costly. |
| C12.3 Differential-Privacy Safeguards | Medium | Opacus and TF Privacy are production-quality for training. Budget tracking and auditing tools are less mature. Black-box auditing tools are research prototypes. |
| C12.4 Purpose-Limitation & Scope-Creep Protection | Low | No standardized tooling for purpose tagging or runtime purpose enforcement. Requires custom policy-as-code integration with MLOps platforms. |
| C12.5 Consent Management & Lawful-Basis Tracking | Low-Medium | CMPs are mature for web consent but poorly integrated with ML pipelines. No standard for consent tokens in inference APIs. |
| C12.6 Federated Learning with Privacy Controls | Medium | FL frameworks support local DP and secure aggregation. Robust aggregation (Krum, Trimmed-Mean) is available but configuration is manual. Canary-based auditing is research-stage. |

---

## Open Research Questions

- [ ] Is machine unlearning practical at scale, or is retraining the only reliable option?
- [ ] What epsilon values for differential privacy provide meaningful protection without destroying model utility?
- [ ] How should GDPR Article 17 (right to erasure) apply to foundation models?
- [ ] What constitutes adequate anonymization for AI training data?

---

## Related Standards & Cross-References

- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [General Data Protection Regulation (GDPR)](https://gdpr-info.eu/)
- [California Consumer Privacy Act (CCPA)](https://oag.ca.gov/privacy/ccpa)
- [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C03 Data Governance | Data lineage, classification, retention | C03 covers general data governance; C12 focuses on privacy-specific controls for personal data |
| C05 AI Model Security | Model extraction, membership inference | Model security controls in C05 complement privacy protections by defending against information extraction attacks |
| C09 AI Supply Chain | Third-party data provenance | Supply chain controls ensure privacy obligations flow to data suppliers and model providers |
| C14 Logging & Monitoring | Audit trails, immutable logging | C14 logging requirements support C12.2.4 deletion audit trails and C12.3 budget tracking |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
