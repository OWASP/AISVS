# C14 Human Oversight and Trust

## Control Objective

Ensure that humans retain effective control over AI systems through reliable shutdown and graceful-degradation paths, an explicit policy that determines which AI decisions and agent actions require human approval, and an independent audit trail of human oversight interventions.

This chapter focuses on controls unique to human oversight of AI systems: kill-switch and intermediate-state mechanisms specific to AI runtime structure (model inference, agent runtimes, tool/MCP servers, retrieval connectors), the policy that classifies AI decisions and agent actions as high-risk, the system's behavior when a human approver is not available within the required timeframe, and logging of human-initiated override events. Generic access control to administrative interfaces, security event logging fundamentals, version control of documentation, and operational testing of safety controls are covered by ASVS v5 (V8, V13, V15, V16) and AISVS C3 (model lifecycle and rollback), C5 (step-up authentication for high-risk AI operations and JIT privileged access), C9 (agent identity, audit, and approval gates), and C13 (logging and incident response), and are not repeated here. AI explainability with a security framing (sanitization of explanations, logging of interpretability artifacts) is covered by C7.4. Confidence and uncertainty handling with a security framing is covered by C7.2 and C11.3. AI governance content (model cards, public transparency reports, AI impact assessments, fairness and ethics documentation) is covered e.g. by NIST AI RMF and ISO/IEC 42001, and is out of AISVS scope.

---

## C14.1 Kill-Switch & Override Mechanisms

Provide shutdown or rollback paths when unsafe behavior of the AI system is observed, and ensure these mechanisms remain functional over time.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.1.1** | **Verify that** a manual kill-switch mechanism exists to immediately halt AI model inference and outputs. | 1 |
| **14.1.2** | **Verify that** kill-switch and intermediate-state mechanisms are exercised at a defined frequency, and that each test confirms the system reaches the target state within the documented response time and that all dependent components (e.g., agent runtimes, tool/MCP servers, retrieval connectors) transition as specified. | 2 |
| **14.1.3** | **Verify that** the system can be placed into at least two intermediate operational states between full operation and complete shutdown (e.g., disabling specific tools or MCP servers, removing a retrieval source, switching to a safer or smaller model, enforcing read-only mode for agents), and that each state has defined entry triggers and can be exited independently without requiring a full system restart or shutdown. | 2 |
| **14.1.4** | **Verify that** override and kill-switch commands for autonomous agents are delivered and enforced through a channel that the agent runtime cannot access, intercept, or suppress (e.g., out-of-band infrastructure controls, hypervisor-level signals, network-layer isolation), so that a compromised or manipulated agent cannot prevent its own shutdown. | 2 |

---

## C14.2 Human-in-the-Loop Decision Checkpoints

Define which AI decisions and agent actions require human approval so that runtime gates can enforce them, and define the system's behavior when approval is not provided in time.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.2.1** | **Verify that** a documented human oversight policy defines which AI decisions and agent actions are classified as high-risk, the criteria used to make that determination, and the approval authority required before execution. | 1 |
| **14.2.2** | **Verify that** when a human-approval gate (per C14.2.1 and C9.2) is not satisfied within the defined approval time-to-live, the system applies a documented default action, that the default action is fail-closed (blocking the action) unless an alternative is explicitly authorized in the high-risk action policy, and that any non-fail-closed default is itself classified and approved as a high-risk policy decision. | 2 |

---

## C14.3 Logging of Human Oversight Interventions

Capture human-initiated oversight events so that override and mode-change actions are independently auditable and reconstructable.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **14.3.1** | **Verify that** kill-switch activations, intermediate operational state transitions, and override commands are logged with the operator identity, the channel used (including whether the out-of-band channel per C14.1.4 was invoked), the originating trigger or justification, the prior and resulting system state, and the timestamp. | 1 |

## References

* [MITRE ATLAS: Human In-the-Loop for AI Agent Actions](https://atlas.mitre.org/mitigations/AML.M0029)
