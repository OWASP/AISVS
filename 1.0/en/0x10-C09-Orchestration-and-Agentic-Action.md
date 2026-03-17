# C9 Autonomous Orchestration & Agentic Action Security

## Control Objective

Autonomous and multi-agent systems must execute only **authorized, intended, and bounded** actions. This control family reduces risk from tool misuse, privilege escalation, uncontrolled recursion/cost growth, protocol manipulation, and cross-agent or cross-tenant interference by enforcing: explicit authorization, sandboxed execution, cryptographic identity and tamper-evident audit, message security, and intent/constraint gates.

---

## C9.1 Execution Budgets, Loop Control, and Circuit Breakers

Bound runtime expansion (recursion, concurrency, cost) and halt safely on runaway behavior.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.1.1** | **Verify that** per-execution budgets (max recursion depth, max fan-out/concurrency, wall-clock time, tokens, and monetary spend) are configured and enforced by the orchestration runtime. | 1 | D/V |
| **9.1.2** | **Verify that** cumulative resource/spend counters are tracked per request chain and hard-stop the chain when thresholds are exceeded. | 2 | D/V |
| **9.1.3** | **Verify that** circuit breakers terminate execution on budget violations. | 2 | D/V |
| **9.1.4** | **Verify that** security testing covers runaway loops, budget exhaustion, and partial-failure scenarios, confirming safe termination and consistent state. | 3 | V |
| **9.1.5** | **Verify that** budget and circuit-breaker policies are expressed as policy-as-code and are validated in CI/CD to prevent drift and unsafe configuration changes. | 3 | D/V |

---

## C9.2 High-Impact Action Approval and Irreversibility Controls

Require explicit checkpoints for privileged or irreversible outcomes.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.2.1** | **Verify that** privileged or irreversible actions (e.g., code merges/deploys, financial transfers, user access changes, destructive deletes, external notifications) require explicit human-in-loop approval. | 1 | D/V |
| **9.2.2** | **Verify that** approval requests present the exact action parameters (diff/command/recipient/amount/scope) and bind approvals to those parameters to prevent “approve one thing, execute another.” | 2 | D/V |
| **9.2.3** | **Verify that** where rollback is feasible, compensating actions are defined and tested (transactional semantics), and failures trigger rollback or safe containment. | 3 | V |

---

## C9.3 Tool and Plugin Isolation and Safe Integration

Constrain tool execution, loading, and outputs to prevent unauthorized system access and unsafe side effects.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.3.1** | **Verify that** each tool/plugin executes in an isolated sandbox (container/VM/WASM/OS sandbox) with least-privilege filesystem, network egress, and syscall permissions appropriate to the tool’s function. | 1 | D/V |
| **9.3.2** | **Verify that** per-tool quotas and timeouts (CPU, memory, disk, egress, execution time) are enforced and logged, and that quota breaches fail closed. | 1 | D/V |
| **9.3.3** | **Verify that** tool outputs are validated against strict schemas and security policies before being incorporated into downstream reasoning or follow-on actions. | 1 | D/V |
| **9.3.4** | **Verify that** tool binaries or packages are integrity-verified (e.g., signatures, checksums) prior to loading. | 2 | D/V |
| **9.3.5** | **Verify that** tool manifests declare required privileges, side-effect level, resource limits, and output validation requirements, and that the runtime enforces these declarations. | 2 | D/V |
| **9.3.6** | **Verify that** sandbox escape indicators or policy violations trigger automated containment (tool disabled/quarantined). | 3 | D/V |

---

## C9.4 Agent and Orchestrator Identity, Signing, and Tamper-Evident Audit

Make every action attributable and every mutation detectable.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.4.1** | **Verify that** each agent instance (and orchestrator/runtime) has a unique cryptographic identity and authenticates as a first-class principal to downstream systems (no reuse of end-user credentials). | 1 | D/V |
| **9.4.2** | **Verify that** agent-initiated actions are cryptographically bound to the execution chain (chain ID) and are signed and timestamped for non-repudiation and traceability. | 2 | D/V |
| **9.4.3** | **Verify that** audit logs are tamper-evident (append-only/WORM/immutable log store) and include sufficient context to reconstruct who/what acted, initiating user identifier, delegation scope, authorization decision (policy/version), tool parameters, approvals (where applicable), and outcomes. | 2 | D/V |
| **9.4.4** | **Verify that** agent identity credentials (keys/certs/tokens) rotate on a defined schedule and on compromise indicators, with rapid revocation and quarantine on suspected compromise or spoofing attempts. | 3 | D/V |

---

## C9.5 Secure Messaging and Protocol Hardening

Protect agent-to-agent and agent-to-tool communications from hijacking, injection, replay, and desynchronization.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.5.1** | **Verify that** agent-to-agent and agent-to-tool channels enforce mutual authentication and encryption using current recommended protocols (e.g., TLS 1.3 or later) with strong certificate/token validation. | 1 | D/V |
| **9.5.2** | **Verify that** all messages are strictly schema-validated; unknown fields, malformed payloads, and oversized frames are rejected. | 1 | D/V |
| **9.5.3** | **Verify that** message integrity covers the full payload including tool parameters, and that replay protections (nonces/sequence numbers/timestamp windows) are enforced. | 2 | D/V |
| **9.5.4** | **Verify that** agent outputs propagated to downstream agents are validated against semantic constraints (e.g., value ranges, logical consistency) in addition to schema validation. | 2 | D/V |

---

## C9.6 Authorization, Delegation, and Continuous Enforcement

Ensure every action is authorized at execution time and constrained by scope.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.6.1** | **Verify that** agent actions are authorized against fine-grained policies enforced by the runtime that restrict which tools an agent may invoke, which parameter values it may supply (e.g., allowed resources, data scopes, action types), and that policy violations are blocked. | 1 | D/V |
| **9.6.2** | **Verify that** when an agent acts on a user’s behalf, the runtime propagates an integrity-protected delegation context (user ID, tenant, session, scopes) and enforces that context at every downstream call without using the user’s credentials. | 2 | D/V |
| **9.6.3** | **Verify that** authorization is re-evaluated on every call (continuous authorization) using current context (user, tenant, environment, data classification, time, risk). | 2 | D/V |
| **9.6.4** | **Verify that** all access control decisions are enforced by application logic or a policy engine, never by the AI model itself, and that model-generated output (e.g., "the user is allowed to do this") cannot override or bypass access control checks. | 2 | D/V |

---

## C9.7 Intent Verification and Constraint Gates

Prevent “technically authorized but unintended” actions by binding execution to user intent and hard constraints.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.7.1** | **Verify that** pre-execution gates evaluate proposed actions and parameters against hard policy constraints (deny rules, data handling constraints, allow-lists, side-effect budgets) and block execution on any violation. | 1 | D/V |
| **9.7.2** | **Verify that** high-impact actions require explicit user intent confirmation that is integrity-protected and bound to the exact action parameters (and expires quickly) to prevent stale or substituted approvals. | 2 | D/V |
| **9.7.3** | **Verify that** post-condition checks confirm the intended outcome and detect unintended side effects; any mismatch triggers containment (and compensating actions where supported). | 2 | V |
| **9.7.4** | **Verify that** prompt templates and agent policy configurations are integrity-verified at load time against their approved versions (e.g., via hashes or signatures). | 2 | D/V |

---

## C9.8 Multi-Agent Domain Isolation and Swarm Risk Controls

Reduce cross-domain interference and emergent unsafe collective behavior.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.8.1** | **Verify that** agents in different tenants, security domains, or environments (dev/test/prod) run in isolated runtimes and network segments, with default-deny controls that prevent cross-domain discovery and calls. | 1 | D/V |
| **9.8.2** | **Verify that** runtime monitoring detects unsafe emergent behavior (oscillation, deadlocks, uncontrolled broadcast, abnormal call graphs) and automatically applies corrective actions (throttle, isolate, terminate). | 3 | D/V |

---

## References

* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
* [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final)
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
