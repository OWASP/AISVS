# C9 Autonomous Orchestration & Agentic Action Security

## Control Objective

Autonomous and multi-agent systems must execute only **authorized, intended, and bounded** actions. This control family reduces risk from tool misuse, privilege escalation, uncontrolled recursion/cost growth, protocol manipulation, and cross-agent or cross-tenant interference by enforcing: explicit authorization, sandboxed execution, cryptographic identity and tamper-evident audit, message security, and intent/constraint gates.

---

## C9.1 Execution Budgets, Loop Control, and Circuit Breakers

Bound runtime expansion (recursion, concurrency, cost) and halt safely on runaway behavior.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.1.1** | **Verify that** per-execution budgets (max recursion depth, max fan-out/concurrency, wall-clock time, tokens, and monetary spend) are centrally configured, version-controlled, and enforced by the orchestration runtime. | 1 | D/V |
| **9.1.2** | **Verify that** cumulative resource/spend counters are tracked per request chain and hard-stop the chain when thresholds are exceeded. | 2 | D/V |
| **9.1.3** | **Verify that** circuit breakers terminate execution on budget violations. | 2 | D/V |
| **9.1.4** | **Verify that** security testing covers runaway loops, budget exhaustion, and partial-failure scenarios, confirming safe termination and consistent state. | 3 | V |
| **9.1.5** | **Verify that** budget and circuit-breaker policies are expressed as policy-as-code and are validated in CI/CD to prevent drift and unsafe configuration changes. | 3 | D/V |

---

## C9.2 High-Impact Action Approval and Irreversibility Controls

Require explicit checkpoints for privileged or irreversible outcomes.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.2.1** | **Verify that** privileged or irreversible actions (e.g., code merges/deploys, financial transfers, user access changes, destructive deletes, external notifications) require explicit approval through an auditable channel before execution. | 1 | D/V |
| **9.2.2** | **Verify that** approval requests present the exact action parameters (diff/command/recipient/amount/scope) and bind approvals to those parameters to prevent “approve one thing, execute another.” | 2 | D/V |
| **9.2.3** | **Verify that** where rollback is feasible, compensating actions are defined and tested (transactional semantics), and failures trigger rollback or safe containment. | 3 | V |

---

## C9.3 Tool and Plugin Isolation and Safe Integration

Constrain tool execution, loading, and outputs to prevent unauthorized system access and unsafe side effects.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.3.1** | **Verify that** each tool/plugin executes in an isolated sandbox (container/VM/WASM/OS sandbox) with least-privilege filesystem, network egress, and syscall permissions appropriate to the tool’s function. | 1 | D/V |
| **9.3.2** | **Verify that** per-tool quotas and timeouts (CPU, memory, disk, egress, execution time) are enforced and logged, and that quota breaches fail closed. | 1 | D/V |
| **9.3.3** | **Verify that** tool manifests declare required privileges, side-effect level, resource limits, and output validation requirements, and that the runtime enforces these declarations. | 2 | D/V |
| **9.3.4** | **Verify that** tool outputs are validated against strict schemas and security policies before being incorporated into downstream reasoning or follow-on actions. | 2 | D/V |
| **9.3.5** | **Verify that** tool binaries are integrity-protected and validated prior to loading. | 2 | D/V |
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
| **9.5.1** | **Verify that** agent-to-agent and agent-to-tool channels enforce mutual authentication and encryption with modern protocols (e.g., TLS 1.3) and strong certificate/token validation. | 1 | D/V |
| **9.5.2** | **Verify that** all messages are strictly schema-validated; unknown fields, malformed payloads, and oversized frames are rejected. | 1 | D/V |
| **9.5.3** | **Verify that** message integrity covers the full payload including tool parameters, and that replay protections (nonces/sequence numbers/timestamp windows) are enforced. | 2 | D/V |

---

## C9.6 Authorization, Delegation, and Continuous Enforcement

Ensure every action is authorized at execution time and constrained by scope.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.6.1** | **Verify that** agent actions are authorized against fine-grained policies that restrict which tools an agent may invoke and which parameters it may supply (allow-list plus parameter constraints), enforced by the runtime. | 2 | D/V |
| **9.6.2** | **Verify that** when an agent acts on a user’s behalf, the runtime propagates an integrity-protected delegation context (user ID, tenant, session, scopes) and enforces that context at every downstream call without using the user’s credentials. | 2 | D/V |
| **9.6.3** | **Verify that** authorization is re-evaluated on every call (continuous authorization) using current context (tenant, environment, data classification, time, risk), and that delegated scopes are time-bound and automatically expire. | 3 | D/V |

---

## C9.7 Intent Verification and Constraint Gates

Prevent “technically authorized but unintended” actions by binding execution to user intent and hard constraints.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.7.1** | **Verify that** pre-execution gates evaluate proposed actions and parameters against hard policy constraints (deny rules, data handling constraints, allow-lists, side-effect budgets) and block execution on any violation. | 1 | D/V |
| **9.7.2** | **Verify that** high-impact actions require explicit user intent confirmation that is integrity-protected and bound to the exact action parameters (and expires quickly) to prevent stale or substituted approvals. | 2 | D/V |
| **9.7.3** | **Verify that** post-condition checks confirm the intended outcome and detect unintended side effects; any mismatch triggers containment (and compensating actions where supported). | 2 | V |

---

## C9.8 Multi-Agent Domain Isolation and Swarm Risk Controls

Reduce cross-domain interference and emergent unsafe collective behavior.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.8.1** | **Verify that** agents in different tenants, security domains, or environments (dev/test/prod) run in isolated runtimes and network segments, with default-deny controls that prevent cross-domain discovery and calls. | 1 | D/V |
| **9.8.2** | **Verify that** runtime monitoring detects unsafe emergent behavior (oscillation, deadlocks, uncontrolled broadcast, abnormal call graphs) and automatically applies corrective actions (throttle, isolate, terminate). | 3 | D/V |

---

## C9.9 Model Context Protocol (MCP) Security

Ensure secure discovery, authentication, authorization, transport, and use of MCP-based tool and resource integrations to prevent context confusion, unauthorized tool invocation, or cross-tenant data exposure.

### Component Integrity & Supply Chain Hygiene

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.9.1** | **Verify that** MCP server and client components are obtained only from trusted sources and verified using signatures, checksums, or secure package metadata, rejecting tampered or unsigned builds. | 1 | D/V |

### Authentication & Authorization

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.9.2** | **Verify that** MCP clients and servers mutually authenticate using strong, non-user credentials (e.g., mTLS, DPoP), and that unauthenticated MCP requests are rejected. | 2 | D/V |
| **9.9.3** | **Verify that** MCP servers are registered through a controlled technical onboarding mechanism requiring explicit owner, environment, and resource definitions; unregistered or undiscoverable servers must not be callable in production. | 2 | D/V |
| **9.9.4** | **Verify that** each MCP tool or resource defines explicit authorization scopes (e.g., read-only, restricted queries, side-effect levels), and that agents cannot invoke MCP functions outside their assigned scope. | 2 | D/V |

### Secure Transport & Network Boundary Protection

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.9.5** | **Verify that** authenticated, encrypted streamable-HTTP is used as the primary MCP transport in production environments; alternate transports (stdio, SSE) are restricted to local or tightly controlled environments with explicit justification. | 2 | D/V |
| **9.9.6** | **Verify that** streamable-HTTP MCP transports use authenticated, encrypted channels (TLS 1.3 or later) with certificate validation. | 2 | D/V |
| **9.9.7** | **Verify that** SSE-based MCP transports are used only within private, authenticated internal channels and enforce TLS, authentication, schema validation, payload size limits, and rate limiting; SSE endpoints must not be exposed to the public internet. | 2 | D/V |
| **9.9.8** | **Verify that** MCP servers validate the `Origin` and `Host` headers on all HTTP-based transports (including SSE and streamable-HTTP) to prevent DNS rebinding attacks, and reject requests from untrusted, mismatched, or missing origins. | 2 | D/V |

### Schema, Message, and Input Validation

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.9.9** | **Verify that** MCP tool and resource schemas (e.g., JSON schemas or capability descriptors) are validated for authenticity and integrity using signatures to prevent schema tampering or malicious parameter modification. | 2 | D/V |
| **9.9.10** | **Verify that** all MCP transports enforce message-framing integrity, strict schema validation, maximum payload sizes, and rejection of malformed, truncated, or interleaved frames to prevent desynchronization or injection attacks. | 2 | D/V |
| **9.9.11** | **Verify that** MCP servers perform strict input validation for all function calls, including type checking, boundary checking, enumeration enforcement, and rejection of unrecognized or oversized parameters. | 2 | D/V |

### Outbound Access & Agent Execution Safety

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.9.12** | **Verify that** MCP servers may only initiate outbound requests to approved internal or external destinations following least-privilege egress policies, and cannot access arbitrary network targets or internal cloud metadata services. | 2 | D/V |
| **9.9.15** | **Verify that** outbound MCP actions implement execution limits (timeouts, recursion limits, concurrency caps, circuit breakers) to prevent unbounded agent-driven tool invocation or chained side effects. | 2 | D/V |


### Transport Restrictions & High-Risk Boundary Controls

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **9.9.16** | **Verify that** stdio-based MCP transports are limited to co-located, single-process development scenarios, isolated from shell execution, terminal injection, and process-spawning capabilities; stdio must never cross network or multi-tenant boundaries. | 3 | D/V |
| **9.9.17** | **Verify that** MCP servers expose only allow-listed functions and resources, and prohibit dynamic dispatch, reflective invocation, or execution of function names influenced by user or model-provided input. | 3 | D/V |
| **9.9.18** | **Verify that** tenant boundaries, environment boundaries (dev/test/prod), and data domain boundaries are enforced at the MCP layer, preventing cross-tenant or cross-environment server or resource discovery. | 3 | D/V |

---

## References

* [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
