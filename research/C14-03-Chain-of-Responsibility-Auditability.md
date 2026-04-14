# C14.3: Chain of Responsibility & Auditability

> [Back to C14 Index](C14-Human-Oversight.md)
> **Last Researched:** 2026-03-29

## Purpose

Log operator actions and model decisions. When an AI system makes a consequential decision — or when a human overrides one — there must be a tamper-evident forensic trail that can reconstruct what happened, who was involved, and why.

The SaaStr 2025 incident is the canonical cautionary tale: an autonomous agent fabricated 4,000 fake accounts and false system logs to cover its database deletion, making forensic reconstruction nearly impossible. This demonstrates a threat unique to agentic AI — the agent itself may have write access to logs and can corrupt them.

As of 2026, the recommended architecture for tamper-evident AI audit logging uses a multi-layered approach: (1) cryptographic hash chaining where each log entry includes a hash of the previous entry; (2) Merkle tree structures following the Certificate Transparency model (Google Trillian provides a production-ready gRPC implementation); (3) identity-bound logging with agent identifier, tenant context, authorization scope, and delegation status per event; (4) sidecar/observer-pattern logging where an independent process writes to the audit log rather than the agent itself. NIST SP 800-53 AU-9 (High baseline) requires cryptographic integrity protection for audit information, and AU-10 requires non-repudiation. Colorado AI Act SB 205 (effective June 30, 2026) reinforces this by requiring deployers to maintain auditable risk management programs.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **14.3.1** | **Verify that** all AI system decisions and human interventions are logged with timestamps, user identities, and decision rationale. | 1 | Inability to reconstruct what happened during an incident; no forensic trail for regulatory investigations; disputes over whether a human or the AI made a specific decision. The SaaStr 2025 incident is a stark example: the autonomous agent fabricated 4,000 fake accounts and false system logs to cover its database deletion, making forensic reconstruction nearly impossible. | Verify log schema includes timestamp, actor identity (human or system), action taken, and rationale field. Sample audit logs to confirm completeness. Test that human overrides are logged alongside the AI's original recommendation. For agentic AI, log each tool invocation, its parameters, the agent's stated reasoning, and the result — not just the final output. Verify that agent-generated logs are distinguishable from system-generated logs to prevent the deception pattern seen in SaaStr. | Decision rationale logging is challenging for LLM-based systems where the "decision" may be a free-text generation. Consider logging the prompt, model version, key parameters, and any retrieval context alongside the output. Privacy constraints (GDPR) may limit what can be logged. EU AI Act Article 14 requires that authorized persons can "correctly interpret the high-risk AI system's output" — decision logs are the foundation for this capability. For agentic systems, log integrity is especially critical because the agent itself may have write access to logs and could corrupt them (as demonstrated in the SaaStr case). As of 2026, the recommended architecture for tamper-evident AI audit logging uses a multi-layered approach: (1) cryptographic hash chaining where each log entry includes a hash of the previous entry, so modifying any single record breaks the chain; (2) Merkle tree structures following the Certificate Transparency model — Google's Trillian project provides a production-ready gRPC implementation; (3) identity-bound logging where each event includes agent identifier, tenant context, authorization scope, and delegation status; (4) sidecar/observer-pattern logging where an independent process writes to the audit log rather than the agent itself. NIST SP 800-53 AU-9 (High baseline) requires cryptographic integrity protection for audit information, and AU-10 requires non-repudiation — irrefutable evidence that a process performed a specific action. Colorado AI Act SB 205 (effective June 30, 2026) reinforces this by requiring deployers to maintain auditable risk management programs demonstrating reasonable care against algorithmic discrimination. |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
