# C9.2: High-Impact Action Approval and Irreversibility Controls

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Agents acting autonomously may perform actions with significant real-world consequences -- deploying code, transferring funds, deleting data, sending communications. This section requires that high-impact or irreversible actions pass through explicit human approval checkpoints. The approval mechanism must be tamper-resistant: the human must see exactly what will happen, and the system must execute exactly what was approved.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.2.1** | **Verify that** privileged or irreversible actions (e.g., code merges/deploys, financial transfers, user access changes, destructive deletes, external notifications) require explicit human-in-loop approval. | 1 | D/V | **Unintended destructive actions.** An agent manipulated via prompt injection or operating on flawed reasoning could execute irreversible actions (deleting production databases, sending fraudulent emails, deploying broken code) without any human checkpoint. This is the "excessive agency" risk in its most dangerous form. | Review the action taxonomy to confirm all high-impact actions are classified and routed through an approval workflow. Test by triggering each classified action type and verifying the system pauses for human approval before execution. Confirm the approval requirement cannot be bypassed by prompt manipulation. | Defining "high-impact" is organization-specific. Frameworks like LangGraph support `interrupt_before` nodes for human-in-the-loop, but classification of which actions need approval is a manual design decision. Risk: over-classification leads to approval fatigue; under-classification leads to missed dangerous actions. |
| **9.2.2** | **Verify that** approval requests present the exact action parameters (diff/command/recipient/amount/scope) and bind approvals to those parameters to prevent "approve one thing, execute another." | 2 | D/V | **Approval substitution / bait-and-switch.** An agent (or attacker manipulating the agent) could present a benign action for approval, then execute a different action after receiving the approval token. Without parameter binding, approval becomes a rubber stamp. TOCTOU (time-of-check-time-of-use) attacks are the classic vector. | Verify that the approval payload contains a cryptographic hash or signature of the exact action parameters. Confirm that the execution engine validates the hash before proceeding. Test by modifying action parameters after approval and verifying execution is rejected. | Parameter binding requires the orchestration layer to serialize and hash action parameters deterministically. For complex actions (e.g., code diffs), the "exact parameters" may be large. Need to balance completeness of display with readability for the human approver. |
| **9.2.3** | **Verify that** where rollback is feasible, compensating actions are defined and tested (transactional semantics), and failures trigger rollback or safe containment. | 3 | V | **Irrecoverable partial execution.** Multi-step agent actions may partially complete before failing, leaving the system in an inconsistent state (e.g., funds debited but not credited, infrastructure half-provisioned). Without compensating actions, recovery requires manual intervention. | Review compensating action definitions for each reversible high-impact action. Execute failure scenarios mid-action and verify rollback occurs automatically. Confirm that irreversible actions (where rollback is infeasible) are flagged as such and require stronger approval. | Saga patterns from distributed systems apply here. Most agent frameworks have no built-in transaction/rollback support. This must be implemented at the application layer. True rollback is impossible for some actions (sent emails, published content, deleted data without backups). |

---

## Related Standards & References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) -- the primary risk this section addresses
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) -- covers approval workflow recommendations
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) -- "Uncontrolled Autonomy" and "Excessive Functionality" entries
- Saga pattern (Garcia-Molina & Salem, 1987) -- foundational work on compensating transactions in distributed systems

---

## Open Research Questions

- How do you prevent approval fatigue in systems with frequent high-impact actions without weakening security?
- Can risk-adaptive approval thresholds (auto-approve low-risk instances of normally high-impact action types) be made safe?
- What is the minimum viable approval context that a human needs to make an informed decision for different action types?
- How should approval workflows handle time-sensitive actions where the human approver is unavailable?

---
