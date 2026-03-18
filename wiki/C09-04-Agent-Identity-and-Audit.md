# C9.4: Agent and Orchestrator Identity, Signing, and Tamper-Evident Audit

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

In multi-agent systems, every action must be attributable to a specific agent, and every mutation must be detectable. Without cryptographic identity and tamper-evident audit trails, it becomes impossible to determine which agent took which action, whether actions were authorized, or whether logs have been altered to conceal malicious activity. This section establishes agent identity as a first-class security primitive and requires audit logs that support forensic reconstruction.

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
- AISVS C13 (Monitoring and Logging) -- general AI system logging requirements; C09.4 adds agent-specific identity and tamper-evidence
- [OpenTelemetry](https://opentelemetry.io/) -- distributed tracing that can carry chain/trace IDs referenced in 9.4.2

---

## Open Research Questions

- How should agent identity work for ephemeral agents that exist only for a single request? Is per-request identity issuance practical at scale?
- Can agent identity be extended to include capability attestation (proving the agent is running approved code, not just that it has a valid credential)?
- What is the right balance between audit completeness (logging every tool parameter) and privacy (tool parameters may contain sensitive user data)?
- How do you handle identity for agents that span trust domains (e.g., an agent that calls tools hosted by different organizations)?

---
