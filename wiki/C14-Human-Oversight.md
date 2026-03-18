# C14: Human Oversight, Accountability & Governance

> **Source:** [`1.0/en/0x10-C14-Human-Oversight.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C14-Human-Oversight.md)
> **Requirements:** 25 | **Sections:** 7

## Control Objective

This chapter provides requirements for maintaining human oversight and clear accountability chains in AI systems, ensuring explainability, transparency, and ethical stewardship throughout the AI lifecycle.

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Automation bias — humans over-trusting AI outputs without adequate review
- Kill-switch failures in autonomous systems operating at high speed
- Accountability gaps when AI systems make consequential errors
- Opaque AI decision-making in regulated domains (healthcare, finance, criminal justice)
- Model cards that are incomplete or misleading about model limitations
- Overconfident predictions leading to unwarranted trust in low-certainty outputs
- Lack of transparency eroding public trust and regulatory compliance

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2018 | Uber ATV fatality (Tempe, AZ) | Kill-switch / override was disabled by operator; autonomous system failed to escalate to human in time | [NTSB Report](https://www.ntsb.gov/investigations/accidentreports/reports/har1903.pdf) |
| 2019 | Mitchell et al. "Model Cards for Model Reporting" | Foundational paper defining model card structure for transparency and accountability | [arXiv:1810.03993](https://arxiv.org/abs/1810.03993) |
| 2020 | Rudin, "Stop Explaining Black Box Models for High Stakes Decisions" | Argues for inherently interpretable models over post-hoc explanations in critical domains | [Nature Machine Intelligence](https://doi.org/10.1038/s42256-019-0048-x) |
| 2021 | EU AI Act draft proposal | Introduced mandatory human oversight requirements for high-risk AI systems (Article 14) | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021PC0206) |
| 2023 | NIST AI RMF 1.0 | Provides governance and accountability framework for AI risk management | [NIST AI 100-1](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) |

---

## C14.1 Kill-Switch & Override Mechanisms

Provide shutdown or rollback paths when unsafe behavior of the AI system is observed.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **14.1.1** | **Verify that** a manual kill-switch mechanism exists to immediately halt AI model inference and outputs. | 1 | D/V | Runaway inference, unsafe autonomous actions, cascading failures in production systems where the model produces harmful or dangerous outputs with no way to stop it. | Confirm the existence of a documented shutdown procedure. Test that activating the kill-switch stops all inference within an acceptable latency window. Verify it works at the infrastructure level (e.g., service mesh circuit breaker, container orchestration kill, feature flag). | Kill-switch latency matters: for real-time systems (autonomous vehicles, trading), sub-second response is needed. For batch/offline systems, halting the pipeline is sufficient. Define acceptable halt latency per deployment context. |
| **14.1.2** | **Verify that** override controls are accessible to only authorized personnel. | 1 | D | Unauthorized shutdown or sabotage of AI services; malicious actors triggering or disabling kill-switches; insider threats manipulating override controls. | Review RBAC policies on override endpoints. Confirm MFA or equivalent strong authentication is required. Audit access logs for override control usage. Verify that override APIs are not exposed without authentication. | Balance speed of access against security: overly restrictive access may delay emergency response. Consider break-glass procedures for genuine emergencies. |
| **14.1.3** | **Verify that** rollback procedures can revert to previous model versions or safe-mode operations. | 3 | D/V | Deploying a model update that introduces bias, safety regressions, or degraded performance; inability to recover from a bad deployment quickly. | Verify that model versioning is in place (e.g., MLflow, DVC, or registry-based versioning). Test rollback by deploying a previous model version and confirming inference resumes correctly. Check that rollback preserves data pipeline compatibility. | Rollback is harder for fine-tuned foundation models or models with stateful components (e.g., online learning). Safe-mode fallback (e.g., rule-based system) is an alternative when full rollback is impractical. Rated L3 because mature rollback infrastructure is uncommon. |
| **14.1.4** | **Verify that** override mechanisms are tested regularly. | 3 | V | Stale or non-functional kill-switches that fail when actually needed; untested procedures that have configuration drift or are broken by infrastructure changes. | Review test schedules and execution logs for override drills. Confirm that tests simulate realistic failure scenarios (not just happy-path). Verify that test results are documented and failures are remediated. | Analogous to disaster recovery testing. Organizations should run kill-switch drills at least annually, more frequently for high-risk systems. Rated L3 due to operational overhead of regular testing. |

---

## C14.2 Human-in-the-Loop Decision Checkpoints

Require human approvals when stakes surpass predefined risk thresholds.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **14.2.1** | **Verify that** high-risk AI decisions require explicit human approval before execution. | 1 | D/V | Fully autonomous execution of consequential decisions (loan denials, medical diagnoses, content removal) without human review, leading to harm at scale. | Confirm that decision categories are classified by risk level. Verify that high-risk decisions are queued for human approval before action is taken. Test that the system blocks execution until approval is received. | "High-risk" must be defined per domain. The EU AI Act Annex III provides one taxonomy. Organizations need their own risk classification that maps AI outputs to required approval levels. |
| **14.2.2** | **Verify that** risk thresholds are clearly defined and automatically trigger human review workflows. | 1 | D | Inconsistent or ad-hoc escalation where some high-risk decisions slip through without review; reliance on individual operators to recognize when to escalate. | Review the documented risk threshold definitions. Confirm that thresholds are implemented programmatically (not just documented). Test boundary cases to verify that threshold triggers work correctly. | Thresholds can be based on confidence scores, output magnitude, affected population size, or domain-specific criteria. Static thresholds may need periodic recalibration as model behavior drifts. |
| **14.2.3** | **Verify that** time-sensitive decisions have fallback procedures when human approval cannot be obtained within required timeframes. | 2 | D | System deadlock or denial-of-service when human reviewers are unavailable; time-critical decisions (fraud detection, safety alerts) being delayed past usefulness. | Review fallback procedure documentation. Test timeout scenarios to confirm fallback activates correctly. Verify that fallback actions are conservative (e.g., default-deny, safe-mode) rather than auto-approving. | Fallback design requires careful thought: defaulting to "approve" defeats the purpose of HITL, while defaulting to "deny" may cause operational disruption. The appropriate default depends on the domain and consequence asymmetry. |
| **14.2.4** | **Verify that** escalation procedures define clear authority levels for different decision types or risk categories, if applicable. | 3 | D/V | Unclear chains of command leading to delayed or inappropriate decision-making; junior operators making decisions beyond their authority; no path for novel or ambiguous situations. | Review escalation matrix documentation. Verify that authority levels map to specific decision categories. Confirm that the escalation path is implemented in the workflow system, not just documented. | L3 because many organizations lack formal escalation hierarchies for AI decisions. This is more relevant for large organizations with multiple AI systems and operator tiers. |

---

## C14.3 Chain of Responsibility & Auditability

Log operator actions and model decisions.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **14.3.1** | **Verify that** all AI system decisions and human interventions are logged with timestamps, user identities, and decision rationale. | 1 | D/V | Inability to reconstruct what happened during an incident; no forensic trail for regulatory investigations; disputes over whether a human or the AI made a specific decision. | Verify log schema includes timestamp, actor identity (human or system), action taken, and rationale field. Sample audit logs to confirm completeness. Test that human overrides are logged alongside the AI's original recommendation. | Decision rationale logging is challenging for LLM-based systems where the "decision" may be a free-text generation. Consider logging the prompt, model version, key parameters, and any retrieval context alongside the output. Privacy constraints (GDPR) may limit what can be logged. |
| **14.3.2** | **Verify that** audit logs cannot be tampered with and include integrity verification mechanisms. | 2 | D | Log tampering to cover up AI failures or human errors; insider threats modifying audit trails; regulatory non-compliance due to unreliable logs. | Verify that logs are written to append-only storage or use cryptographic chaining (e.g., hash chains, write-once storage). Confirm that log integrity is periodically verified. Check that log access controls prevent modification by operators whose actions are being logged. | Standard log integrity practices apply (SIEM integration, immutable storage like AWS CloudTrail or Azure Immutable Blob Storage). The AI-specific nuance is ensuring model decision metadata is included in the integrity-protected log stream, not just infrastructure events. |

---

## C14.4 Explainable-AI Techniques

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **14.4.1** | **Verify that** AI systems provide basic explanations for their decisions in human-readable format. | 1 | D/V | Opaque decision-making that prevents users or operators from understanding why an action was taken; inability to identify errors or biases; regulatory non-compliance in domains requiring explanation (ECOA, GDPR Article 22). | Confirm that every decision-producing endpoint returns an explanation alongside its output. Evaluate explanation readability with non-technical stakeholders. Verify explanations are generated for all decision paths, not just common ones. | "Human-readable" is subjective and audience-dependent. A data scientist and an end user need different explanation formats. For LLMs, this may mean citing source documents or highlighting reasoning steps. For classification models, it may mean showing top contributing features. |
| **14.4.2** | **Verify that** explanation quality is validated through human evaluation studies and metrics. | 2 | V | Explanations that are technically present but meaningless, misleading, or incomprehensible to the intended audience; "explanation washing" where systems produce plausible-sounding but inaccurate rationales. | Review human evaluation study design and results. Check that studies include representative users from the target audience. Verify that metrics such as explanation fidelity, comprehensibility, and actionability are measured. Confirm evaluations are repeated after model updates. | Metrics for explanation quality are an active research area. Common approaches include: simulatability (can humans predict model behavior from the explanation), fidelity (does the explanation accurately reflect the model's reasoning), and sufficiency (does the explanation contain enough information for the user's task). |
| **14.4.3** | **Verify that** feature importance scores or attribution methods (SHAP, LIME, etc.) are available for critical decisions. | 3 | D/V | Inability to diagnose model errors or biases in critical decisions; lack of technical transparency for auditors and regulators who need to understand model behavior at a feature level. | Verify that SHAP, LIME, Integrated Gradients, or equivalent attribution methods are integrated. Test that attributions are generated for sample critical decisions. Check that attribution outputs are stored and retrievable for audit. Validate that attributions are consistent across similar inputs (stability). | SHAP and LIME have known limitations: SHAP is computationally expensive for large models; LIME explanations can be unstable across similar inputs. For deep learning, Integrated Gradients or attention-based attributions may be more appropriate. For LLMs, attribution is an open research problem. Rated L3 because tooling for production-grade attribution is still maturing. |
| **14.4.4** | **Verify that** counterfactual explanations show how inputs could be modified to change outcomes, if applicable to the use case and domain. | 3 | V | Users who receive adverse decisions (loan denial, insurance rejection) have no actionable recourse because they cannot understand what would need to change to get a different outcome. | Verify that counterfactual generation is implemented for relevant decision types. Test that counterfactuals are actionable (suggest changes to mutable features only, not immutable characteristics). Confirm counterfactuals are plausible (within realistic data distributions). | Counterfactual explanation libraries include DiCE (Microsoft), Alibi, and Carla. Key challenge: counterfactuals must only suggest changes to features the user can actually modify (e.g., "increase income" is actionable; "change age" is not). Most applicable to tabular classification tasks; harder to apply to unstructured data or generative models. |

---

## C14.5 Model Cards & Usage Disclosures

Maintain model cards for intended use, performance metrics, and ethical considerations.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **14.5.1** | **Verify that** model cards document intended use cases, limitations, and known failure modes. | 1 | D | Misuse of models outside their intended scope; users deploying models in high-risk contexts the model was never designed or evaluated for; inability to assess fitness-for-purpose. | Review model card for completeness against a checklist (e.g., Mitchell et al. 2019 template). Confirm that intended use, out-of-scope uses, and known failure modes are all documented. Verify that failure modes are specific and actionable, not generic disclaimers. | The Mitchell et al. (2019) model card template is the de facto standard. Google's Model Card Toolkit and Hugging Face's model card template both provide structured formats. For foundation models, documenting "intended use" is harder due to broad applicability; focus on known unsafe use cases and validated use cases. |
| **14.5.2** | **Verify that** performance metrics across different applicable use cases are disclosed. | 1 | D/V | Deploying a model that performs well on average but fails badly for specific subgroups or use cases; hidden performance disparities across demographics or data distributions. | Verify that metrics are reported per relevant subgroup or use case, not just aggregate. Check that metrics include both accuracy-type and fairness-type measures where applicable. Confirm metrics are computed on held-out evaluation sets, not training data. | Disaggregated metrics are essential. A model with 95% overall accuracy that has 60% accuracy for a minority subgroup is problematic. Standard disaggregation dimensions include demographics, geographic regions, language variants, and edge-case categories relevant to the domain. |
| **14.5.3** | **Verify that** ethical considerations, bias assessments, fairness evaluations, training data characteristics, and known training data limitations are documented and updated regularly. | 2 | D | Undisclosed biases that lead to discriminatory outcomes; training data that is unrepresentative or contains toxic content; stakeholders unable to assess ethical risks before deployment. | Review documentation for bias assessments, fairness metrics (demographic parity, equalized odds, etc.), training data composition, and data collection methodology. Verify that documents are dated and updated on a defined schedule (e.g., quarterly or per model update). | This is a compound requirement covering multiple documentation areas. Bias assessment tooling includes Fairlearn, AI Fairness 360, and What-If Tool. Training data documentation can follow the Datasheets for Datasets framework (Gebru et al. 2021). Regular updates are critical because model behavior and data distributions drift over time. |
| **14.5.4** | **Verify that** model cards are version-controlled and maintained throughout the model lifecycle with change tracking. | 2 | D/V | Stale documentation that does not reflect the current model version; inability to compare how model characteristics changed across versions; no audit trail for documentation changes. | Verify that model cards are stored in version control (e.g., Git) alongside model artifacts. Check that each model version has a corresponding model card version. Confirm that a changelog or diff is available showing what changed between versions. | Integration with ML experiment tracking tools (MLflow, Weights & Biases, Neptune) can automate parts of model card maintenance. The challenge is keeping free-text sections (limitations, ethical considerations) up to date, which requires human effort beyond what automation provides. |

---

## C14.6 Uncertainty Quantification

Propagate confidence scores or entropy measures in responses.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **14.6.1** | **Verify that** AI systems provide confidence scores or uncertainty measures with their outputs. | 1 | D | Overconfident predictions treated as certain by downstream systems or users; no signal to indicate when the model is operating outside its training distribution or producing unreliable outputs. | Confirm that model outputs include a confidence or uncertainty metric. Verify that the metric is meaningful (not just raw softmax probabilities, which are often poorly calibrated). Check that uncertainty is surfaced to users or downstream systems, not just logged internally. | Raw softmax outputs from neural networks are notoriously overconfident and should not be used as-is for uncertainty. Calibration techniques (temperature scaling, Platt scaling) or proper uncertainty methods (MC Dropout, deep ensembles, conformal prediction) are needed. For LLMs, token-level log probabilities can serve as a proxy but have significant limitations. |
| **14.6.2** | **Verify that** uncertainty thresholds trigger additional human review or alternative decision pathways. | 2 | D/V | High-uncertainty predictions being acted on automatically without additional scrutiny; AI systems making consequential decisions in regions of the input space where they have low confidence. | Verify that uncertainty thresholds are defined and documented. Test that exceeding a threshold routes the decision to human review or a fallback path. Confirm thresholds are calibrated to the application's risk tolerance (e.g., medical applications need lower uncertainty tolerance than content recommendations). | Connects directly to C14.2 (HITL checkpoints). The threshold should be set based on the cost asymmetry of errors in the specific domain. Threshold selection methods include cost-sensitive analysis, receiver operating characteristic (ROC) analysis, and domain expert input. |
| **14.6.3** | **Verify that** uncertainty quantification methods are calibrated and validated against ground truth data. | 2 | V | Miscalibrated confidence scores that give false assurance (e.g., a model that says "95% confident" but is only correct 70% of the time); operators making decisions based on unreliable uncertainty estimates. | Review calibration plots (reliability diagrams) comparing predicted confidence to actual accuracy. Verify that calibration is measured on held-out data, not training data. Check that calibration is evaluated per subgroup and across distribution shifts. Confirm recalibration is performed after model updates. | Expected Calibration Error (ECE) is the standard metric. Calibration should be tested both in-distribution and under realistic distribution shifts. Conformal prediction provides distribution-free coverage guarantees but requires exchangeability assumptions. Temperature scaling is the simplest post-hoc calibration method and works well for many classification tasks. |
| **14.6.4** | **Verify that** uncertainty propagation is maintained through multi-step AI workflows. | 3 | D/V | Compounding errors in AI pipelines where the output of one model feeds into another; uncertainty being lost or ignored at pipeline boundaries, leading to false confidence in final outputs. | Trace uncertainty through a multi-step workflow and verify that downstream components receive and use upstream uncertainty estimates. Test that high uncertainty in an early stage appropriately affects confidence in the final output. Verify that pipeline-level uncertainty is reported, not just per-component uncertainty. | This is technically challenging and an active research area. Approaches include Monte Carlo simulation through the pipeline, Bayesian networks, or simple uncertainty propagation rules. For LLM agent workflows (e.g., tool-calling chains), uncertainty propagation is largely unsolved. Rated L3 due to lack of mature tooling. |

---

## C14.7 User-Facing Transparency Reports

Provide periodic disclosures on incidents, drift, and data usage.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **14.7.1** | **Verify that** data usage policies and user consent management practices are clearly communicated to stakeholders. | 1 | D/V | Users unaware that their data is used for AI training or inference; regulatory non-compliance with GDPR, CCPA, or sector-specific data protection requirements; erosion of user trust. | Review data usage disclosures for clarity and completeness. Verify that consent mechanisms are functional and granular (users can opt out of specific data uses). Confirm that disclosures are accessible (not buried in lengthy ToS documents). Test that consent preferences are actually enforced in the data pipeline. | AI-specific data usage concerns include: training on user interactions, fine-tuning on user-provided content, and using conversation data for evaluation. The AI-specific nuance beyond general privacy is disclosing how data flows through AI-specific processes (embedding, vectorization, RAG retrieval). |
| **14.7.2** | **Verify that** AI impact assessments are conducted and results are included in reporting. | 2 | D/V | Deploying AI systems without understanding their societal impact; inability to demonstrate due diligence to regulators; unidentified risks to affected populations. | Verify that impact assessments are conducted before deployment and periodically thereafter. Review assessment methodology for rigor (stakeholder consultation, rights impact analysis). Confirm that assessment results are summarized in transparency reports. Check that identified risks have corresponding mitigations documented. | The EU AI Act requires Fundamental Rights Impact Assessments for high-risk systems. The Canadian Algorithmic Impact Assessment (AIA) tool provides a structured framework. NIST AI RMF MAP function also provides impact assessment guidance. Assessment scope should include both direct users and indirectly affected populations. |
| **14.7.3** | **Verify that** transparency reports published regularly disclose AI incidents and operational metrics in reasonable detail. | 2 | D/V | Stakeholders unable to assess AI system reliability; incidents being concealed or minimized; no public accountability for AI failures; inability to benchmark AI system performance over time. | Verify that transparency reports are published on a defined schedule (e.g., quarterly, annually). Review report content for: incident descriptions, root cause analyses, operational metrics (uptime, accuracy, drift indicators), and remediation actions. Confirm reports are publicly accessible or available to relevant stakeholders. | Transparency reporting for AI is modeled after security transparency reports (e.g., Google, Microsoft). Content should include: number and severity of incidents, model performance trends, data drift indicators, human override rates, and any changes to model behavior. The challenge is balancing transparency with not disclosing information that could aid adversaries. |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Explainability:** SHAP, LIME, Captum (PyTorch), InterpretML, Alibi, DiCE (counterfactuals)
- **Model cards:** Model Card Toolkit (Google), Hugging Face model card template, VerifyML
- **Uncertainty:** Conformal prediction (MAPIE, crepes), MC Dropout, deep ensembles, temperature scaling
- **Human-in-the-loop:** Label Studio, Prodigy, custom approval workflows, Airflow/Prefect with human-gate tasks
- **Audit logging:** AWS CloudTrail, Azure Immutable Blob Storage, append-only databases, cryptographic log chaining
- **Fairness & bias:** Fairlearn, AI Fairness 360, What-If Tool, Aequitas

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C14.1 Kill-Switch & Override Mechanisms | Medium | Infrastructure-level controls (feature flags, circuit breakers) are mature; AI-specific kill-switches less standardized |
| C14.2 Human-in-the-Loop Decision Checkpoints | Medium | Workflow orchestration tools support human gates; challenge is defining risk thresholds programmatically |
| C14.3 Chain of Responsibility & Auditability | High | Standard logging and SIEM infrastructure applies; AI-specific metadata (model version, prompt, context) needs explicit integration |
| C14.4 Explainable-AI Techniques | Medium-Low | SHAP/LIME mature for tabular data; XAI for LLMs and deep learning is still evolving rapidly |
| C14.5 Model Cards & Usage Disclosures | Medium | Templates and toolkits exist; keeping cards up-to-date across model lifecycle remains a manual effort |
| C14.6 Uncertainty Quantification | Medium-Low | Conformal prediction and ensembles are well-understood; production integration and LLM uncertainty are immature |
| C14.7 User-Facing Transparency Reports | Low | No standardized format; most organizations produce ad-hoc reports if any |

---

## Open Research Questions

- [ ] What level of explainability is adequate for different risk domains?
- [ ] How do you design kill-switches that work for real-time AI systems with sub-second latency requirements?
- [ ] What should model cards include for foundation models with broad use cases?
- [ ] How should uncertainty quantification be communicated to non-technical stakeholders?
- [ ] Can uncertainty propagation be solved for LLM agent pipelines with tool-calling chains?
- [ ] How do you evaluate explanation fidelity for generative AI systems where there is no single "decision"?
- [ ] What transparency report standards will emerge from EU AI Act enforcement?

---

## Related Standards & Cross-References

| Standard | Relevant Section | Notes |
|----------|-----------------|-------|
| EU AI Act | Article 14 (Human Oversight) | Mandatory human oversight for high-risk AI systems; directly maps to C14.1 and C14.2 |
| NIST AI RMF 1.0 | GOVERN, MAP, MANAGE functions | Comprehensive AI governance framework; accountability and transparency themes throughout |
| ISO/IEC 42001:2023 | Clause 6.1, Annex A | AI management system standard with oversight and transparency controls |
| ASVS | V7 (Error Handling and Logging) | General logging requirements; C14.3 adds AI-specific decision logging |
| GDPR | Articles 13-15, 22 | Right to explanation for automated decisions; right to human intervention |

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C02 (Data Governance) | Training data documentation | C14.5.3 (training data characteristics) complements C02 data provenance requirements |
| C04 (Model Risk) | Model versioning and rollback | C14.1.3 (rollback) relates to C04 model lifecycle management |
| C07 (Output Handling) | Output confidence and filtering | C14.6 (uncertainty) informs output filtering decisions in C07 |
| C09 (Monitoring) | Drift detection and incident logging | C14.7 transparency reports consume drift and incident data from C09 monitoring |
| C11 (Privacy) | Data usage disclosure and consent | C14.7.1 (data usage policies) overlaps with C11 privacy controls |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
