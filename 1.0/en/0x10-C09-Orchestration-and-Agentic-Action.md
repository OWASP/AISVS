# C9 Orchestration & Agentic Security

## Control Objective

Autonomous and multi-agent systems must execute only authorized, intended, and bounded actions. This chapter focuses on controls unique to agentic AI execution: agent-as-principal identity, agent action chains, model-output-driven authorization risk, intent verification of LLM-decided actions, multi-agent swarm dynamics, and human oversight of agentic systems, including human-approval gates for high-impact actions and human-controlled shutdown and graceful degradation.

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

Require trusted approval checkpoints for agent actions that are privileged, high-impact, or difficult to reverse.

| # | Description | Level |
| :--: | --- | :---: |
| **9.2.1** | **Verify that** the agent runtime blocks execution of privileged, high-impact, or irreversible actions until explicit human approval is received and verified. | 1 |
| **9.2.2** | **Verify that** approval requests display canonicalized and complete action parameters, such as diffs, commands, recipients, amounts, resources, and scopes, without truncation or unsafe transformation. | 2 |
| **9.2.3** | **Verify that** each high-impact action has a trusted reversibility classification, such as read-only, reversible, externally reversible, or irreversible. | 2 |
| **9.2.4** | **Verify that** the agent runtime enforces reversibility classifications by blocking, requiring approval, or restricting actions based on their impact and ability to be reversed. | 2 |
| **9.2.5** | **Verify that** any self-modification capability (e.g., prompt rewriting, tool-list changes, parameter updates) is restricted by enforceable boundaries. | 2 |
| **9.2.6** | **Verify that** agentic systems include an AI-augmented review of planned high-risk actions before execution that adds to, and does not replace, the deterministic policy gate. | 2 |
| **9.2.7** | **Verify that** the AI-augmented review mechanism is protected against manipulation by adversarial inputs, and cannot be overridden or bypassed through prompt injection. | 2 |
| **9.2.8** | **Verify that** approvals are cryptographically bound to action parameters, requester identity, execution context, and a unique single-use nonce. | 3 |
| **9.2.9** | **Verify that** cryptographic key material or credentials used to issue approvals are isolated from the agent runtime. | 3 |
| **9.2.10** | **Verify that** approval gates for multi-step or multi-agent action chains enforce the highest-impact reversibility classification present anywhere in the chain. | 3 |

---

## C9.3 Component Isolation and Tool Authorization

Constrain tool and plugin execution, loading, and outputs to prevent unauthorized system access and unsafe side effects.

| # | Description | Level |
| :--: | --- | :---: |
| **9.3.1** | **Verify that** each tool/plugin executes in a least-privilege sandbox or is otherwise isolated from model operations. | 1 |
| **9.3.2** | **Verify that** tool outputs are validated against schemas. | 1 |
| **9.3.3** | **Verify that** tool manifests declare required privileges, resource limits, and output validation requirements. | 2 |
| **9.3.4** | **Verify that** the runtime enforces the privileges, resource limits, and output-validation requirements declared in tool manifests. | 2 |
| **9.3.5** | **Verify that** components processing untrusted data are isolated from tool-calling capabilities, ensuring that compromised data processing cannot trigger unauthorized tool invocations. | 2 |
| **9.3.6** | **Verify that** there is architectural separation between processing of untrusted tool outputs and agent operations. | 2 |
| **9.3.7** | **Verify that** external resources named in model output are verified against an approved allow-list or registry before the agent installs or invokes them. | 2 |
| **9.3.8** | **Verify that** policy violations trigger automated tool containment. | 3 |

---

## C9.4 Agent and Orchestrator Identity

Make every action attributable and every mutation detectable.

| # | Description | Level |
| :--: | --- | :---: |
| **9.4.1** | **Verify that** each agent instance has a unique cryptographic identity and authenticates as a first-class principal to downstream systems. | 2 |
| **9.4.2** | **Verify that** agent-initiated actions are cryptographically bound to each step of the execution chain for non-repudiation. | 2 |
| **9.4.3** | **Verify that** agent identity credentials rotate on a defined schedule. | 3 |
| **9.4.4** | **Verify that** agent state persisted between invocations is integrity-protected. | 3 |

---

## C9.5 Agent Authorization, Delegation, and Continuous Enforcement

Ensure every action is authorized at execution time and constrained by scope.

| # | Description | Level |
| :--: | --- | :---: |
| **9.5.1** | **Verify that** agent actions are authorized against fine-grained policies enforced by the runtime that restrict which tools an agent may invoke, and which parameter values it may supply. | 2 |
| **9.5.2** | **Verify that** when an agent acts on a user's behalf, the runtime propagates an integrity-protected and scope-limited token that carries that context to every downstream call. | 2 |
| **9.5.3** | **Verify that** all access control decisions are enforced by application logic or a policy engine, never by the AI model itself. | 2 |
| **9.5.4** | **Verify that** secrets and credentials required by an agent at runtime are not exposed within the model's observable context, including the context window, system prompts, or tool call parameters. | 2 |
| **9.5.5** | **Verify that** inter-agent task delegation is restricted by an explicit authorization policy. | 2 |
| **9.5.6** | **Verify that** long-running agent sessions re-evaluate current backend authorization policy on every privileged action. | 3 |

---

## C9.6 Shutdown and Graceful Degradation

Provide shutdown and graceful degradation paths under human control, with mechanisms that remain reliable and exercised over time.

| # | Description | Level |
| :--: | --- | :---: |
| **9.6.1** | **Verify that** a manual kill-switch mechanism exists to immediately halt AI model inference and outputs. | 1 |
| **9.6.2** | **Verify that** when a human-approval gate is not satisfied within the defined approval time, the system blocks the pending action. | 2 |
| **9.6.3** | **Verify that** kill-switch commands are implemented through an out-of-band channel that is isolated from the agent runtime. | 3 |

---

## References

* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
* [NIST AI 100-1: AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
* [Regulation (EU) 2024/1689 (EU AI Act), Article 14: Human Oversight](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
