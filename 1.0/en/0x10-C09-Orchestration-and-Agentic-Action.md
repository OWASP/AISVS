# C9 Autonomous Orchestration & Agentic Action Security

## Control Objective

Autonomous and multi-agent systems must execute only authorized, intended, and bounded actions. This chapter focuses on controls unique to agentic AI execution: agent-as-principal identity, agent action chains, model-output-driven authorization risk, intent verification of LLM-decided actions, and multi-agent swarm dynamics.

---

## C9.1 Execution Budgets, Loop Control, and Circuit Breakers

Bound runtime expansion (recursion, concurrency, cost) and halt safely on runaway behavior.

| # | Description | Level |
| :--: | --- | :---: |
| **9.1.1** | **Verify that** per-execution budgets (max recursion depth, max fan-out/concurrency, wall-clock time, tokens, and monetary spend) are configured and enforced by the orchestration runtime. | 1 |
| **9.1.2** | **Verify that** cumulative resource and spend counters are tracked per request chain and that exceeding any configured threshold hard-stops the chain via a circuit breaker. | 2 |
| **9.1.3** | **Verify that** security testing covers runaway loops, budget exhaustion, and partial-failure scenarios, confirming safe termination and consistent state. | 3 |

---

## C9.2 High-Impact Action Approval and Irreversibility Controls

Require explicit checkpoints for privileged or irreversible outcomes.

| # | Description | Level |
| :--: | --- | :---: |
| **9.2.1** | **Verify that** the agent runtime enforces an execution gate that blocks privileged or irreversible actions (e.g., code merges/deploys, financial transfers, user access changes, destructive deletes, external notifications) until an explicit human approval is received and verified. | 1 |
| **9.2.2** | **Verify that** approval requests display canonicalized and complete action parameters (diff, command, recipient, amount, scope) without truncation or transformation. | 2 |
| **9.2.3** | **Verify that** approvals are cryptographically bound (e.g., signed or MACed) to the exact action parameters, requester identity, and execution context, include a unique single-use nonce, and expire within a defined maximum time-to-live (TTL). | 2 |
| **9.2.4** | **Verify that** where rollback is feasible, compensating actions are defined and tested (transactional semantics), and failures trigger rollback or safe containment. | 3 |

---

## C9.3 Component Isolation and Safe Integration

Constrain tool and plugin execution, loading, and outputs to prevent unauthorized system access and unsafe side effects.

| # | Description | Level |
| :--: | --- | :---: |
| **9.3.1** | **Verify that** each tool/plugin executes in an isolated sandbox (container/VM/WASM/OS sandbox) with least-privilege filesystem, network egress, and syscall permissions appropriate to the tool's function. | 1 |
| **9.3.2** | **Verify that** per-tool quotas and timeouts (CPU, memory, disk, egress, execution time) are enforced, and that quota or timeout breaches fail closed by terminating the tool execution rather than continuing with degraded or uncontrolled behavior. | 1 |
| **9.3.3** | **Verify that** tool outputs are validated against strict schemas and security policies before being incorporated into downstream reasoning or follow-on actions. | 1 |
| **9.3.4** | **Verify that** quota and timeout breaches are logged with sufficient detail to identify the tool, the exceeded limit, and the time of breach. | 1 |
| **9.3.5** | **Verify that** tool manifests declare required privileges, side-effect level, resource limits, and output validation requirements. | 2 |
| **9.3.6** | **Verify that** the orchestration runtime enforces the declarations specified in tool manifests for required privileges, side-effect level, resource limits, and output validation. | 2 |
| **9.3.7** | **Verify that** sandbox escape indicators or policy violations trigger automated containment (tool disabled/quarantined). | 3 |

---

## C9.4 Agent and Orchestrator Identity, Signing, and Tamper-Evident Audit

Make every action attributable and every mutation detectable.

| # | Description | Level |
| :--: | --- | :---: |
| **9.4.1** | **Verify that** each agent instance (and orchestrator/runtime) has a unique cryptographic identity and authenticates as a first-class principal to downstream systems (no reuse of end-user credentials). | 1 |
| **9.4.2** | **Verify that** agent-initiated actions are cryptographically bound to the execution chain (chain ID). | 2 |
| **9.4.3** | **Verify that** audit log records include sufficient context to reconstruct who/what acted, the initiating user identifier, delegation scope, authorization decision (policy/version), tool parameters, approvals (where applicable), and outcomes. | 2 |
| **9.4.4** | **Verify that** agent-initiated actions are signed and timestamped for non-repudiation and traceability. | 2 |
| **9.4.5** | **Verify that** agent identity credentials (keys/certs/tokens) rotate on a defined schedule and on compromise indicators, with rapid revocation and quarantine on suspected compromise or spoofing attempts. | 3 |
| **9.4.6** | **Verify that** agent state persisted between invocations (including memory, task context, goals, and partial results) is integrity-protected (e.g., via cryptographic MACs or signatures), and that the runtime rejects or quarantines state that fails integrity verification before resuming execution. | 3 |

---

## C9.5 Secure Messaging and Protocol Hardening

Protect agent-to-agent and agent-to-tool communications from hijacking, injection, and unauthorized modifications.

| # | Description | Level |
| :--: | --- | :---: |
| **9.5.1** | **Verify that** agent outputs propagated to downstream agents are validated against semantic constraints (e.g., value ranges, logical consistency) in addition to schema validation. | 2 |

---

## C9.6 Authorization, Delegation, and Continuous Enforcement

Ensure every action is authorized at execution time and constrained by scope.

| # | Description | Level |
| :--: | --- | :---: |
| **9.6.1** | **Verify that** agent actions are authorized against fine-grained policies enforced by the runtime that restrict which tools an agent may invoke, which parameter values it may supply (e.g., allowed resources, data scopes, action types), and that policy violations are blocked. | 1 |
| **9.6.2** | **Verify that** when an agent acts on a user's behalf, the runtime propagates an integrity-protected delegation context (user ID, tenant, session, scopes) and enforces that context at every downstream call without using the user's credentials. | 2 |
| **9.6.3** | **Verify that** all access control decisions are enforced by application logic or a policy engine, never by the AI model itself, and that model-generated output (e.g., "the user is allowed to do this") cannot override or bypass access control checks. | 2 |
| **9.6.4** | **Verify that** secrets and credentials required by an agent at runtime are not exposed within the model's observable context, including the context window, system prompts, or tool call parameters, and are instead provided via out-of-band mechanisms such as credential proxies, secrets manager injection, runtime sidecar authentication, or short-lived scoped tokens. | 2 |
| **9.6.5** | **Verify that** when an agent acts under delegated authority, the policy decision point evaluates both the agent's own granted permissions and the initiating principal's delegated scope as independent constraints, denying the action if either is insufficient for the requested operation. | 2 |
| **9.6.6** | **Verify that** agent-to-agent task delegation is restricted by an explicit peer authorization policy (e.g., an approved agent registry or allowlist) so that even authenticated agents can only delegate to or accept delegations from pre-approved peers, with delegation attempts from unlisted agents rejected by default. | 2 |
| **9.6.7** | **Verify that** long-running agent sessions re-evaluate current backend authorization policy for the agent’s identity on every privileged action, and reject the action when current policy no longer authorizes it, even if the presented token remains valid. | 3 |

---

## C9.7 Intent Verification and Constraint Gates

Prevent "technically authorized but unintended" actions by binding execution to user intent and hard constraints.

| # | Description | Level |
| :--: | --- | :---: |
| **9.7.1** | **Verify that** pre-execution gates evaluate proposed actions and parameters against hard policy constraints (deny rules, data handling constraints, allow-lists, side-effect budgets) and block execution on any violation. | 1 |
| **9.7.2** | **Verify that** post-execution checks confirm the intended outcome was achieved and detect unintended side effects, and that any mismatch triggers containment and, where supported, compensating actions. | 2 |
| **9.7.3** | **Verify that** all write operations to persistent external state are authorized by either explicit human approval or an independent policy-based authorization mechanism that evaluates the operation against the original user intent, and not solely on agent-generated output. | 2 |
| **9.7.4** | **Verify that** when the policy decision point (PDP) used for governance evaluation is unavailable (e.g., timeout, network partition, service failure), agent execution fails closed by blocking the proposed action, and the unavailability event is logged with sufficient detail for incident investigation. | 2 |
| **9.7.5** | **Verify that** prompt templates and agent policy configurations retrieved from a remote source are integrity-verified at load time against their approved versions (e.g., via hashes or signatures). | 3 |

---

## C9.8 Multi-Agent Domain Isolation and Risk Controls

Reduce cross-domain interference and emergent unsafe collective behavior.

| # | Description | Level |
| :--: | --- | :---: |
| **9.8.1** | **Verify that** agents in different tenants, security domains, or environments (dev/test/prod) run in isolated runtimes and network segments, with default-deny controls that prevent cross-domain discovery and calls. | 1 |
| **9.8.2** | **Verify that** each agent is restricted to its own memory namespace and is technically prevented from reading or modifying peer agent state, preventing unauthorized cross-agent access within the same swarm. | 2 |
| **9.8.3** | **Verify that** each agent operates with an isolated context window that peer agents cannot read or influence, preventing unauthorized cross-agent context access within the same swarm. | 3 |
| **9.8.4** | **Verify that** runtime monitoring detects unsafe emergent behavior (oscillation, deadlocks, uncontrolled broadcast, abnormal call graphs) and automatically applies corrective actions (throttle, isolate, terminate). | 3 |
| **9.8.5** | **Verify that** swarm-level aggregate action rate limits (e.g., total external API calls, file writes, or network requests per time window across all agents) are enforced to prevent bursts that cause denial-of-service or abuse of external systems. | 3 |
| **9.8.6** | **Verify that** a swarm-level shutdown capability exists that can halt all active agent instances or selected problematic instances in an organized fashion and prevents new agent spawning, with shutdown completable within a pre-defined response time. | 3 |

---

## C9.9 Architectural Data-Flow Isolation and Origin Enforcement

Prevent data-flow attacks that exploit agentic tool-calling pipelines by manipulating tool arguments without altering the control flow, through architectural separation of planning from untrusted data processing and origin-aware policy enforcement at the tool-call boundary. These controls complement C2.1 (input-level filtering) and C9.7 (intent verification gates), which do not address attacks where the correct tools are called in the correct sequence but with attacker-controlled arguments derived from untrusted data. Any isolation mechanism that achieves the stated outcome satisfies the requirement.

| # | Description | Level |
| :--: | --- | :---: |
| **9.9.1** | **Verify that** the system architecturally separates, or applies an equivalent isolation mechanism to separate, plan generation (control flow) from untrusted data processing, such that the component determining which tools to call and in what sequence does not directly process untrusted content (e.g., tool outputs, retrieved documents, external messages). | 2 |
| **9.9.2** | **Verify that** components processing untrusted data (e.g., for extraction, summarization, or parsing) are isolated, or equivalently constrained, from tool-calling capabilities, ensuring that compromised data processing cannot trigger unauthorized tool invocations. | 2 |
| **9.9.3** | **Verify that** security policies for tool execution are expressed as auditable, versioned, machine-interpretable code or configuration, not solely as natural language instructions within prompts. | 2 |
| **9.9.4** | **Verify that** values passed to tools carry origin metadata tracking their source (user input, specific tool, external source). | 3 |
| **9.9.5** | **Verify that** security policies are evaluated against value origin before each tool invocation. | 3 |
| **9.9.6** | **Verify that** tool invocations where argument origin violates the applicable security policy are blocked before execution. | 3 |
| **9.9.7** | **Verify that** data-flow integrity is enforced such that untrusted data cannot modify tool arguments beyond what the security policy explicitly permits, even when the control flow (sequence of tool calls) remains as intended. | 3 |
| **9.9.8** | **Verify that** the system's data-flow dependency graph is maintained per session and is available for review by authorized security and operations personnel for post-hoc audit, enabling identification of which data sources influenced each tool invocation and its arguments. | 3 |

---

## References

* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
* [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
* [OpenAPI x-agent-trust Extension (OAI Extensions Registry)](https://spec.openapis.org/registry/extension/x-agent-trust.html)
