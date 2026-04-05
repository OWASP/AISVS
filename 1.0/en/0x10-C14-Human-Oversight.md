# C14 Human Oversight, Accountability & Governance

## Control Objective

This chapter provides requirements for maintaining human oversight and clear accountability chains in AI systems, ensuring explainability, transparency, and ethical stewardship throughout the AI lifecycle.

---

## C14.1 Kill-Switch & Override Mechanisms

Provide shutdown or rollback paths when unsafe behavior of the AI system is observed.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.1.1** | **Verify that** a manual kill-switch mechanism exists to immediately halt AI model inference and outputs. | 1 |
| **14.1.2** | **Verify that** override controls are accessible to only to authorized personnel. | 1 |
| **14.1.3** | **Verify that** rollback procedures can revert to previous model versions or safe-mode operations. | 3 |
| **14.1.4** | **Verify that** override mechanisms are tested regularly. | 3 |
| **14.1.5** | **Verify that** a documented degradation policy defines at least two intermediate states between full operation and complete shutdown (e.g., disabling specific tools or MCP servers, removing a retrieval source, switching to a safer or smaller model, enforcing read-only mode for agents), and that each state has defined triggers, scope, and recovery criteria. | 2 |

---

## C14.2 Human-in-the-Loop Decision Checkpoints

Require human approvals when stakes surpass predefined risk thresholds.

> **Scope note:** C14.2 governs human oversight policy: defining which AI decisions or actions are classified as high-risk, the criteria and thresholds that trigger approval requirements, and the authority structure for granting approval. The runtime enforcement mechanism that blocks agent execution until approval is received is in C9.2. Logging and auditing of approval decisions is in C13.7.4. Compliance with C14.2 requires demonstrating that a documented policy exists, not merely that approvals occur.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.2.1** | **Verify that** a documented human oversight policy defines which AI decisions and agent actions are classified as high-risk, the criteria used to make that determination, and the approval authority required before execution. | 1 |
| **14.2.2** | **Verify that** risk thresholds are clearly defined and automatically trigger human review workflows. | 1 |
| **14.2.3** | **Verify that** time-sensitive decisions have fallback procedures when human approval cannot be obtained within required timeframes. | 2 |
| **14.2.4** | **Verify that** escalation procedures define clear authority levels for different decision types or risk categories, if applicable. | 3 |

---

## C14.3 Chain of Responsibility & Auditability

Log operator actions and model decisions.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.3.1** | **Verify that** all AI system decisions and human interventions are logged with timestamps, user identities, and decision rationale. | 1 |

---

## C14.4 Explainable-AI Techniques

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.4.1** | **Verify that** AI systems provide basic explanations for their decisions in human-readable format. | 1 |
| **14.4.2** | **Verify that** explanation quality is validated through human evaluation studies and metrics. | 2 |
| **14.4.3** | **Verify that** feature importance scores or attribution methods (SHAP, LIME, etc.) are available for critical decisions. | 3 |
| **14.4.4** | **Verify that** counterfactual explanations show how inputs could be modified to change outcomes, if applicable to the use case and domain. | 3 |

---

## C14.5 Model Cards & Usage Disclosures

Maintain model cards for intended use, performance metrics, and ethical considerations.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.5.1** | **Verify that** model cards document intended use cases, limitations, and known failure modes. | 1 |
| **14.5.2** | **Verify that** performance metrics across different applicable use cases are disclosed. | 1 |
| **14.5.3** | **Verify that** ethical considerations, bias assessments, fairness evaluations, training data characteristics, and known training data limitations are documented and updated regularly. | 2 |
| **14.5.4** | **Verify that** model cards are version-controlled and maintained throughout the model lifecycle with change tracking. | 2 |

---

## C14.6 Uncertainty Quantification

Propagate confidence scores or entropy measures in responses.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.6.1** | **Verify that** AI systems provide confidence scores or uncertainty measures with their outputs. | 1 |
| **14.6.2** | **Verify that** uncertainty thresholds trigger additional human review or alternative decision pathways. | 2 |
| **14.6.3** | **Verify that** uncertainty quantification methods are calibrated and validated against ground truth data. | 2 |
| **14.6.4** | **Verify that** uncertainty propagation is maintained through multi-step AI workflows. | 3 |

---

## C14.7 User-Facing Transparency Reports

Provide periodic disclosures on incidents, drift, and data usage.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.7.1** | **Verify that** data usage policies and user consent management practices are clearly communicated to stakeholders. | 1 |
| **14.7.2** | **Verify that** AI impact assessments are conducted and results are included in reporting. | 2 |
| **14.7.3** | **Verify that** transparency reports are published regularly and disclose AI incidents including their nature, impact, and resolution. | 2 |
| **14.7.4** | **Verify that** transparency reports disclose operational metrics (e.g., usage volumes, safety filter rates, error rates) in reasonable detail. | 2 |

## References
