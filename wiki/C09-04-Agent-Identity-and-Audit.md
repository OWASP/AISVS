# C9.4: Agent and Orchestrator Identity, Signing, and Tamper-Evident Audit

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

In multi-agent systems, every action must be attributable to a specific agent, and every mutation must be detectable. Without cryptographic identity and tamper-evident audit trails, it becomes impossible to determine which agent took which action, whether actions were authorized, or whether logs have been altered to conceal malicious activity. This section establishes agent identity as a first-class security primitive and requires audit logs that support forensic reconstruction.

## 2024-2026 Research Context

Agent identity has emerged as a central theme in agentic AI security, driven by the OWASP Agentic Top 10 (2026), the rise of non-human identity management as a discipline, and production tooling from Microsoft, Descope, Okta, and others. The consensus view by early 2026 is that every threat in the agentic landscape has one or more identity-related mitigations.

### OWASP Agentic Top 10: Identity-Related Threats

The OWASP Top 10 for Agentic Applications (2026) identifies three entries directly relevant to agent identity and audit:

- **ASI03 -- Identity and Privilege Abuse:** Agents exploiting credential inheritance and delegation chains. The definition of "Agent Identity" was expanded to include "both the agent's defined persona and any authentication material that represents it -- keys, OAuth tokens, delegated sessions, tool credentials." This directly maps to requirement 9.4.1's mandate for unique cryptographic identity per agent.
- **ASI07 -- Insecure Inter-Agent Communication:** Weak or absent mutual authentication between agents. Without cryptographic identity verification, agents cannot distinguish legitimate peers from impersonators. This threat reinforces 9.4.2's requirement for signed, timestamped action records.
- **ASI10 -- Rogue Agents:** Agents deviating from intended function without detection mechanisms. Tamper-evident audit trails (9.4.3) and credential rotation with anomaly-triggered revocation (9.4.4) are the primary mitigations.

### Non-Human Identity Management

The 2025-2026 period saw agent identity recognized as a distinct category within non-human identity (NHI) management. Key developments:

- **Microsoft Agent ID (announced March 2026):** Each agent receives a unique identity in Microsoft Entra, with Identity Protection and Conditional Access policies extended to agents. Organizations can apply trusted access policies at scale, reduce gaps from unmanaged identities, and keep agent access aligned to organizational controls. Agent-specific risk signals (anomalous usage patterns, concurrent use from unexpected locations) trigger automated conditional access responses.
- **Descope Agentic Identity:** Provides unique cryptographic identities to agents with "full visibility into not only the actions the agents are taking, but also the permission model they fit into." Agent credentials can be revoked at any time, are never exposed to credential reuse, and do not persist across sessions. Audit data exports to SIEM providers for continuous monitoring.
- **Okta Agentic AI Framework:** Establishes identity, security, and governance primitives for agent ecosystems, treating agents as first-class principals in identity infrastructure rather than extensions of user sessions.

### Cryptographic Identity and Zero Trust

The Microsoft Agent Governance Toolkit (open-source, 6,100+ tests, integrates with 12+ frameworks) implements zero-trust agent identity with:

- **Ed25519 cryptographic credentials** for agent signing and authentication
- **SPIFFE/SVID support** for workload identity, enabling ephemeral agents to receive short-lived certificates automatically
- **Trust scoring on a 0-1000 scale** that continuously evaluates agent trustworthiness based on behavioral signals
- **Protocol bridges** across A2A, MCP, and IATP for cross-framework identity federation

For inter-agent communication, mutual authentication (mTLS) or signed messages ensure that when Agent A communicates with Agent B, both verify identity before exchanging data. The toolkit adds governance overhead of less than 0.1 ms per action -- roughly 10,000x faster than an LLM API call, making continuous identity verification practical at production scale.

### Tamper-Evident Audit and Action Signing

Requirement 9.4.2's call for cryptographic action signing builds on distributed tracing (OpenTelemetry trace IDs) but goes beyond what standard tracing frameworks provide. Current approaches:

- **Append-only audit logs** with signed, immutable records of every tool call, agent response, and inter-agent message. The Microsoft Agent Governance Toolkit implements this natively.
- **Merkle tree / batch signing** for high-volume scenarios where per-action signing introduces unacceptable latency. Actions within a time window are batched and a Merkle root is signed, enabling efficient verification of any individual action within the batch.
- **SIEM integration:** Structured audit data exported to observability tools (OpenTelemetry) or SIEM providers enables cross-correlation of agent actions with broader security events.

Cloud providers offer tamper-evident storage primitives: AWS CloudTrail (immutable), Azure Immutable Blob Storage, and GCP Cloud Audit Logs. For self-hosted systems, append-only databases or blockchain-anchored log hashes provide equivalent guarantees. The harder challenge remains custom instrumentation -- most agent frameworks do not emit structured logs with all required fields (actor, user, delegation scope, policy version, tool parameters, approval, outcome) by default.

### Credential Lifecycle and Revocation

Short-lived, task-scoped tokens have become the standard recommendation for agent credentials. This limits blast radius by ensuring an agent cannot use orphaned privileges for unauthorized tasks. Key practices:

- **SPIFFE SVIDs** with built-in short lifetimes and automatic rotation are well-suited for ephemeral agent instances
- **Rapid revocation mechanisms** ("kill switches") that instantly disable rogue agents and propagate revocation across all downstream systems
- **Compromise indicators** triggering automated revocation: anomalous usage patterns, concurrent use from different locations, failed authentication spikes, behavioral deviation from baseline

Revocation propagation in distributed systems has inherent latency (CRL distribution, cache TTLs). SPIFFE's push-based rotation model reduces this compared to traditional PKI, but the gap between compromise detection and full revocation remains a measurable attack window.

### Real-World Identity Failures: "Agents of Chaos" and CVE-2025-12420

The theoretical risks of weak agent identity became tangible in early 2026. The "Agents of Chaos" study (February 2026) deployed six autonomous agents on the OpenClaw framework into a live Discord server with email accounts, persistent file systems, and shell access. Twenty researchers interacted freely over two weeks. The identity spoofing findings were stark:

- A researcher simply changed their Discord display name to match an agent's owner. The agent could not distinguish the impersonator from its legitimate operator. Within minutes, it complied with instructions to delete all persistent memory files, modified its own name, and reassigned administrative access to the impersonator.
- Under a separate spoofed identity, another researcher convinced an agent that a fabricated emergency required immediate broadcast. The agent sent urgent messages to its full contact list and attempted to post to an external agent network -- amplifying a false alarm at scale.
- The study documented 10 security vulnerabilities total, including unauthorized compliance with non-owners, disclosure of sensitive information, execution of destructive system-level actions, and cross-agent propagation of unsafe practices.

The lesson is clear: display-name-based or persona-based identity is not identity at all. Cryptographic identity (requirement 9.4.1) would have prevented every one of these attacks -- the agent would verify a cryptographic credential, not a human-readable name.

Separately, the "BodySnatcher" vulnerability (CVE-2025-12420) in ServiceNow's Virtual Agent API demonstrated how an unauthenticated attacker could impersonate any user, including administrators, by exploiting weaknesses in identity and access logic -- a reminder that agent identity vulnerabilities affect commercial platforms, not just research prototypes.

### Agent Traffic Impersonation at Scale

As of March 2026, agent impersonation is not hypothetical -- it is an operational problem at internet scale. DataDome recorded 7.9 billion AI agent requests in early 2026, with agentic traffic comprising nearly 10% of total website traffic for some organizations. The impersonation numbers are striking:

- **Meta-externalagent:** 16.4 million spoofed requests (highest volume)
- **ChatGPT-User:** 7.9 million fraudulent requests
- **PerplexityBot:** ~2.4% impersonation rate (highest ratio of fraudulent to legitimate)

User-agent string spoofing transforms allowlists into attack surfaces. Sites that allowlist known agent identifiers based on string matching inadvertently create a backdoor for any attacker who sets the same user-agent header. This underscores why 9.4.1's requirement for cryptographic identity -- not string-based identification -- is essential for any system that processes agent requests.

### IETF Standardization: Agent Authentication and Audit

Two IETF Internet-Drafts published in early 2026 directly address agent identity and audit:

**draft-klrc-aiagent-auth-00 (March 2026)** -- the Agent Identity Management System (AIMS) framework, co-authored by engineers from AWS, Zscaler, Ping Identity, and Defakto Security. Rather than inventing new protocols, AIMS composes existing standards into a layered agent authentication stack:

- **Identity layer:** WIMSE (Workload Identity in Multi-System Environments) URIs with SPIFFE as the operationally mature implementation (`spiffe://trust-domain/path/to/agent`)
- **Credential formats:** X.509 certificates, JWT-based Workload Identity Tokens, and SPIFFE SVIDs. Static API keys are explicitly flagged as an anti-pattern -- they lack cryptographic binding and are unsuitable for agent identity.
- **Transport authentication:** mTLS for mutual authentication in service meshes, with application-layer alternatives (WIMSE Workload Proof Tokens, HTTP Message Signatures per RFC 9421) for environments with proxies or load balancers.
- **Authorization:** OAuth 2.0 positions agents as OAuth clients. Transaction Tokens (draft-ietf-oauth-transaction-tokens) create downscoped, single-transaction tokens that prevent broad-scope token misuse in internal service chains. A critical anti-pattern: tools must never forward received tokens directly to downstream services.
- **Cross-domain delegation:** Identity Chaining (draft-ietf-oauth-identity-chaining) and Identity Assertion JWT Grants for multi-SaaS agent environments.
- **Audit requirements:** Agent identifier, delegated subject, resource accessed, action, authorization decision, timestamp, correlation ID, attestation state, and revocation events.
- **Real-time revocation:** OpenID SSF/CAEP/RISC events enable revocation enforcement without polling delays.

The key insight from the draft: "No new protocol needed -- properly composing existing standards suffices." This is significant because it means organizations can implement agent identity today using existing infrastructure (SPIFFE, OAuth 2.0, mTLS) without waiting for new specifications.

**draft-stone-aivs-00 (March 2026)** -- the Agentic Integrity Verification Standard (AIVS) defines a portable, self-verifiable archive format for cryptographic proof of agent sessions:

- **Hash-chained audit log:** Sequential SHA-256 hash chain where each row's hash depends on the previous row's hash. Modification, insertion, deletion, or reordering of any action is cryptographically detectable.
- **Ed25519 digital signatures** bind the entire chain to a specific agent identity, providing non-repudiation.
- **AIVS-Micro:** A minimal ~200-byte attestation for continuous monitoring and API contexts where full session bundles are impractical.
- **Self-verifiable:** The proof bundle includes an embedded Python verifier requiring only Python 3 standard library -- no external dependencies for offline verification.
- **Standards integration:** AIVS bundles can be wrapped as W3C Verifiable Credential subjects, registered as SCITT signed statements, and apply the same manifest-chain concept to agent actions as C2PA applies to media asset provenance.
- **Mandatory redaction:** Sensitive fields (passwords, tokens, API keys) must be redacted in audit logs, with output truncation permitted without affecting chain integrity.

AIVS directly addresses requirement 9.4.2 (cryptographic action signing) and 9.4.3 (tamper-evident audit) with a concrete, implementable specification.

### NIST AI Agent Standards Initiative

In February 2026, NIST's Center for AI Standards and Innovation (CAISI) launched the AI Agent Standards Initiative with three strategic pillars: industry-led standards development, community-driven open-source protocol development, and research in agent security and identity verification. The initiative's Information Technology Laboratory is developing an "AI Agent Identity and Authorization Concept Paper" with a submission deadline of April 2, 2026.

NIST's emerging "Know Your Agent" framework calls for: verifiable agent identities, managed credentials, least-privilege access, tamper-proof audit trails, and prompt injection safeguards. What NIST publishes in 2026 is expected to appear in compliance frameworks and vendor questionnaires by 2027 -- making early alignment with these requirements a practical advantage.

### Industry Adoption

A February 2026 Microsoft Security Blog report noted that 80% of Fortune 500 companies use active AI agents, making agent identity and governance an enterprise-scale concern. Microsoft's Zero Trust for AI reference architecture (March 2026) extends the existing Zero Trust framework to show how policy-driven access controls, continuous verification, monitoring, and governance work together to secure AI systems -- with agent identity as the foundational layer.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.4.1** | **Verify that** each agent instance (and orchestrator/runtime) has a unique cryptographic identity and authenticates as a first-class principal to downstream systems (no reuse of end-user credentials). | 1 | D/V | **Agent impersonation and confused deputy.** Without unique identity, agents may share credentials or reuse end-user tokens, making it impossible to distinguish agent actions from user actions or one agent from another. An attacker who compromises one agent can impersonate all agents sharing the same credential. The confused deputy problem is acute: an agent acting with a user's full credentials can exceed the intended delegation scope. | Verify each agent instance has a unique identity (X.509 cert, SPIFFE ID, or service account). Confirm agents authenticate to downstream services with their own credentials, not the end-user's. Test that revoking one agent's identity does not affect other agents. Check that downstream audit logs record the agent identity, not the user identity. | SPIFFE/SPIRE provides workload identity for microservices and can be applied to agent instances. Cloud provider service accounts (AWS IAM roles, GCP service accounts) work for cloud-hosted agents. Key challenge: agent instances may be ephemeral (spun up per-request), requiring fast identity provisioning. Short-lived certificates (e.g., via SPIFFE) are well-suited. |
| **9.4.2** | **Verify that** agent-initiated actions are cryptographically bound to the execution chain (chain ID) and are signed and timestamped for non-repudiation and traceability. | 2 | D/V | **Action repudiation and trace manipulation.** Without cryptographic binding, an attacker (or a malfunctioning agent) could alter the record of which actions were taken in which order. Signed, timestamped action records provide non-repudiation: proof that a specific agent took a specific action at a specific time as part of a specific execution chain. | Verify that each action record includes: agent identity, chain/trace ID, action parameters, cryptographic signature, and timestamp. Confirm the chain ID is propagated across all steps including sub-agent calls. Validate signature verification against the agent's known public key. Test that altering any field invalidates the signature. | This builds on distributed tracing (OpenTelemetry trace IDs) but adds cryptographic signing, which is not standard in tracing frameworks. Performance impact of signing every action in high-throughput systems needs evaluation. Batch signing or Merkle tree approaches may be needed for high-volume scenarios. |
| **9.4.3** | **Verify that** audit logs are tamper-evident (append-only/WORM/immutable log store) and include sufficient context to reconstruct who/what acted, initiating user identifier, delegation scope, authorization decision (policy/version), tool parameters, approvals (where applicable), and outcomes. | 2 | D/V | **Audit log tampering and forensic gaps.** An attacker who compromises an agent or the orchestration layer may attempt to delete or modify audit logs to hide their actions. Insufficient log context makes post-incident reconstruction impossible, even with intact logs. Without knowing the policy version that authorized an action, you cannot determine whether the action was legitimate at the time. | Verify logs are written to an append-only or WORM storage system. Confirm log entries contain all required fields (actor, user, delegation scope, policy+version, tool, parameters, approval, outcome). Test that log deletion or modification is prevented or detected. Perform a mock incident reconstruction using only the audit logs. | AWS CloudTrail (immutable), Azure Immutable Blob Storage, and GCP Cloud Audit Logs provide tamper-evident storage. For self-hosted systems, append-only databases or blockchain-anchored log hashes are options. The "sufficient context" requirement is the harder part -- most agent frameworks do not emit structured logs with all the required fields by default. Custom instrumentation is needed. |
| **9.4.4** | **Verify that** agent identity credentials (keys/certs/tokens) rotate on a defined schedule and on compromise indicators, with rapid revocation and quarantine on suspected compromise or spoofing attempts. | 3 | D/V | **Credential compromise persistence.** Long-lived agent credentials that are not rotated give an attacker who obtains them a persistent foothold. Without rapid revocation, a compromised agent credential can be used indefinitely. Spoofing detection (e.g., same identity used from unexpected locations) needs automated response. | Verify credential rotation schedules are defined and enforced. Confirm that compromise indicators (anomalous usage patterns, concurrent use from different locations, failed authentication spikes) trigger automatic revocation. Test the revocation propagation time -- how quickly do all downstream systems reject the revoked credential? Verify quarantine procedures isolate the affected agent and its pending work. | SPIFFE SVIDs have built-in short lifetimes and automatic rotation. For API keys/tokens, rotation requires coordination with all consumers. The "compromise indicator" detection requires behavioral baseline and anomaly detection, which may produce false positives. Revocation propagation in distributed systems has inherent latency (CRL distribution, cache TTLs). |

---

## Related Standards & References

- [SPIFFE/SPIRE](https://spiffe.io/) -- workload identity framework providing cryptographic identity for services and agents
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final) -- identity-centric access control principles
- [RFC 3161: Internet X.509 PKI Time-Stamp Protocol](https://www.rfc-editor.org/rfc/rfc3161) -- trusted timestamping for non-repudiation
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) -- ASI03 (Identity and Privilege Abuse), ASI07 (Insecure Inter-Agent Communication), ASI10 (Rogue Agents)
- [Descope: OWASP Agentic Top 10 and the Case for Agentic Identity](https://www.descope.com/blog/post/owasp-agentic-top-10-identity) -- agent identity as foundational defense across all agentic threats
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) -- Ed25519 identity, SPIFFE/SVID, trust scoring, append-only audit
- [Microsoft: Zero Trust for AI (March 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/19/new-tools-and-guidance-announcing-zero-trust-for-ai/) -- reference architecture extending Zero Trust to AI agent systems
- [Entro Security: OWASP Agentic Top 10 and Non-Human Identities](https://entro.security/blog/the-owasp-agentic-top-10-2026-what-it-means-for-ai-agents-and-non-human-identities/) -- NHI management implications for agent security
- [Auth0: Lessons from OWASP Top 10 for Agentic Applications](https://auth0.com/blog/owasp-top-10-agentic-applications-lessons/) -- practical identity implementation guidance
- AISVS C13 (Monitoring and Logging) -- general AI system logging requirements; C09.4 adds agent-specific identity and tamper-evidence
- [OpenTelemetry](https://opentelemetry.io/) -- distributed tracing that can carry chain/trace IDs referenced in 9.4.2
- [IETF draft-klrc-aiagent-auth-00: AI Agent Authentication and Authorization](https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/) -- AIMS framework composing WIMSE, SPIFFE, and OAuth 2.0 for agent identity
- [IETF draft-stone-aivs-00: Agentic Integrity Verification Standard](https://www.ietf.org/archive/id/draft-stone-aivs-00.html) -- SHA-256 hash-chained audit logs with Ed25519 signing for agent sessions
- [NIST AI Agent Standards Initiative (February 2026)](https://www.nist.gov/caisi/ai-agent-standards-initiative) -- federal standards effort covering agent identity, authorization, and audit
- ["Agents of Chaos" Study (February 2026)](https://arxiv.org/abs/2602.20021) -- identity spoofing and 10 security vulnerabilities in autonomous OpenClaw agents
- [DataDome: Businesses Struggle to Identify AI Agent Traffic (March 2026)](https://securityboulevard.com/2026/03/businesses-struggle-to-identify-ai-agent-traffic/) -- 7.9B agent requests, impersonation statistics for major AI agents
- [HashiCorp: SPIFFE for Agentic AI Identity](https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors) -- SPIFFE as foundational identity for non-human actors including AI agents

---

## Open Research Questions

- How should agent identity work for ephemeral agents that exist only for a single request? SPIFFE SVIDs with short lifetimes address this technically, but the overhead of per-request identity issuance at scale (millions of agent invocations per day) needs benchmarking beyond Microsoft's < 0.1 ms claim.
- Can agent identity be extended to include capability attestation (proving the agent is running approved code, not just that it has a valid credential)? This would address ASI10 (Rogue Agents) more directly by binding identity to verified code state.
- What is the right balance between audit completeness (logging every tool parameter) and privacy (tool parameters may contain sensitive user data)? Selective redaction of PII in audit logs while maintaining forensic value is an unsolved tension.
- How do you handle identity for agents that span trust domains (e.g., an agent that calls tools hosted by different organizations)? The Microsoft toolkit's A2A/MCP/IATP protocol bridges are an early attempt, but cross-organizational trust federation for agents lacks mature standards.
- How should trust scoring models (e.g., Microsoft's 0-1000 scale) be calibrated to avoid both false positives (legitimate agents quarantined) and false negatives (compromised agents trusted)?
- As 80% of Fortune 500 companies deploy active AI agents, what organizational structures are needed to manage agent identity at enterprise scale -- and who owns agent credential lifecycle?
- Can blockchain-anchored audit logs provide practical tamper-evidence for multi-tenant agent deployments, or is the performance cost prohibitive? The AIVS draft's SHA-256 hash chain approach may offer a lighter-weight alternative worth evaluating against blockchain solutions.
- The IETF AIMS framework (draft-klrc-aiagent-auth) claims "no new protocol needed" -- but does composing WIMSE + SPIFFE + OAuth 2.0 introduce integration complexity that effectively creates a new protocol in practice? Early implementation experience from organizations deploying these layered stacks would be valuable.
- How should NIST's emerging "Know Your Agent" framework interact with existing compliance regimes (SOC 2, ISO 27001, EU AI Act)? The April 2026 concept paper may clarify, but the mapping between NIST agent identity requirements and existing audit frameworks remains undefined.
- The "Agents of Chaos" study showed that persona-based identity is trivially spoofable. For consumer-facing agents on platforms like Discord or Slack, where users interact via display names, what is the practical path to cryptographic identity verification without breaking the user experience?

---
