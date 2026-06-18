# C9 Orchestration & Agentic Security

## Control Objective

Autonomous and multi-agent systems must execute only authorized, intended, and bounded actions. This chapter focuses on controls unique to agentic AI execution: agent-as-principal identity, agent action chains, model-output-driven authorization risk, intent verification of LLM-decided actions, multi-agent swarm dynamics, and human oversight of agentic systems: human-approval gates for high-impact actions and human-controlled shutdown and graceful degradation.

---

## C9.1 Execution Budgets, Loop Control, and Circuit Breakers

Bound runtime expansion (recursion, concurrency, cost) and halt safely on runaway behavior.

| # | Description | Level |
| :--: | --- | :---: |
| **9.1.1** | **Verify that** per-tool quotas and timeouts (e.g., CPU, memory, disk, egress, and execution time) are enforced. | 1 |
| **9.1.2** | **Verify that** per-execution budgets (e.g., max recursion depth, token use, and monetary spend) are configured and enforced by the runtime. | 1 |
| **9.1.3** | **Verify that** a swarm-level kill-switch exists that can halt all active agent instances. | 2 |

---

## C9.2 High-Impact Action Approval and Irreversibility Controls

Require explicit checkpoints for privileged or irreversible outcomes, and ensure that approval credentials are isolated from the agent runtime so the agent cannot approve its own actions.

| # | Description | Level |
| :--: | --- | :---: |
| **9.2.1** | **Verify that** the agent runtime blocks privileged or irreversible actions, as defined by a documented policy, until an explicit human approval is received and verified. | 1 |
| **9.2.2** | **Verify that** approval requests display canonicalized and complete action parameters (diff, command, recipient, amount, scope) without truncation or transformation. | 2 |
| **9.2.3** | **Verify that** approvals are cryptographically bound to action parameters, requester identity, and execution context with a unique single-use nonce. | 3 |
| **9.2.4** | **Verify that** the key material used to issue an approval is not accessible to the agent runtime. | 3 |

---

## C9.3 Component Isolation and Tool Authorization

Constrain tool and plugin execution, loading, and outputs to prevent unauthorized system access and unsafe side effects.

| # | Description | Level |
| :--: | --- | :---: |
| **9.3.1** | **Verify that** each tool/plugin executes in a least-privilege sandbox or is otherwise isolated from the model operations. | 1 |
| **9.3.2** | **Verify that** tool outputs are validated against schemas. | 1 |
| **9.3.3** | **Verify that** tool manifests declare required privileges, resource limits, and output validation requirements. | 2 |
| **9.3.4** | **Verify that** the runtime enforces that tool manifests define required privileges, resource limits, and output validation. | 2 |
| **9.3.5** | **Verify that** components processing untrusted data are isolated from tool-calling capabilities, ensuring that compromised data processing cannot trigger unauthorized tool invocations. | 2 |
| **9.3.6** | **Verify that** there is architectural separation between untrusted data processing from tool outputs and agent operations. | 2 |
| **9.3.7** | **Verify that** external resources named in model output are verified against an approved allowlist or registry before the agent installs or invokes them. | 2 |
| **9.3.8** | **Verify that** policy violations trigger automated tool containment. | 3 |

---

## C9.4 Agent and Orchestrator Identity

Make every action attributable and every mutation detectable.

| # | Description | Level |
| :--: | --- | :---: |
| **9.4.1** | **Verify that** each agent instance has a unique cryptographic identity and authenticates as a first-class principal to downstream systems. | 2 |
| **9.4.2** | **Verify that** agent-initiated actions are cryptographically bound to each step of the execution chain for non-repudiation. | 2 |
| **9.4.3** | **Verify that** audit log records include identity, scope, authorization decisions, tool parameters, and outcomes. | 2 |
| **9.4.4** | **Verify that** agent identity credentials rotate on a defined schedule. | 3 |
| **9.4.5** | **Verify that** agent state persisted between invocations is integrity-protected. | 3 |

---

## C9.5 Agent Authorization, Delegation, and Continuous Enforcement

Ensure every action is authorized at execution time and constrained by scope.

| # | Description | Level |
| :--: | --- | :---: |
| **9.5.1** | **Verify that** agent actions are authorized against fine-grained policies enforced by the runtime that restrict which tools an agent may invoke, and which parameter values it may supply. | 2 |
| **9.5.2** | **Verify that** when an agent acts on a user's behalf, the runtime propagates an integrity-protected and scope limited token that enforces that context at every downstream call. | 2 |
| **9.5.3** | **Verify that** all access control decisions are enforced by application logic or a policy engine, never by the AI model itself. | 2 |
| **9.5.4** | **Verify that** secrets and credentials required by an agent at runtime are not exposed within the model's observable context, including the context window, system prompts, or tool call parameters. | 2 |
| **9.5.5** | **Verify that** inter-agent task delegation is restricted by an explicit authorization policy. | 2 |
| **9.5.6** | **Verify that** long-running agent sessions re-evaluate current backend authorization policy on every privileged action. | 3 |

---

## C9.6 Shutdown and Graceful Degradation

Provide shutdown and graceful-degradation paths under human control, with mechanisms that remain reliable and exercised over time.

| # | Description | Level |
| :--: | --- | :---: |
| **9.6.1** | **Verify that** a manual kill-switch mechanism exists to immediately halt AI model inference and outputs. | 1 |
| **9.6.2** | **Verify that** the system can be placed into at least two intermediate operational states between full operation and complete shutdown (e.g., disabling specific tools or MCP servers, removing a retrieval source, switching to a safer or smaller model, enforcing read-only mode for agents), and that each state has defined entry triggers and can be exited independently without requiring a full system restart or shutdown. | 2 |
| **9.6.3** | **Verify that** when a human-approval gate is not satisfied within the defined approval time-to-live, the system applies a documented default action that is fail-closed (blocking the pending action). | 2 |
| **9.6.4** | **Verify that** kill-switch activations, intermediate operational state transitions, and override commands are logged with operator identity, channel used, originating trigger or justification, prior and resulting system state, and timestamp. | 2 |
| **9.6.5** | **Verify that** kill-switch and intermediate-state mechanisms are exercised at a defined frequency. Each test confirms that the system reaches the target state within the documented response time, and that all dependent components (e.g., agent runtimes, tool/MCP servers, retrieval connectors) transition as specified. | 2 |
| **9.6.6** | **Verify that** override and kill-switch commands for autonomous agents are delivered through an out-of-band channel (e.g., infrastructure controls, hypervisor-level signals, network-layer isolation) that is architecturally isolated from the agent runtime, so the commands stay enforceable even if the agent runtime is compromised or manipulated. | 3 |

---

## References

* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
* [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
* [OpenAPI x-agent-trust Extension (OAI Extensions Registry)](https://spec.openapis.org/registry/extension/x-agent-trust.html)
* [MITRE ATLAS: Human In-the-Loop for AI Agent Actions](https://atlas.mitre.org/mitigations/AML.M0029)
* [NIST AI 100-1: AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
* [NIST AI 600-1: Generative AI Profile (AI RMF Companion)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
* [ISO/IEC 42001:2023 Artificial Intelligence Management System](https://www.iso.org/standard/42001)
* [ISO/IEC 23894:2023 Artificial Intelligence Risk Management Guidance](https://www.iso.org/standard/77304.html)
* [Regulation (EU) 2024/1689 (EU AI Act), Article 14: Human Oversight](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
* [OECD Recommendation on Artificial Intelligence](https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449)
