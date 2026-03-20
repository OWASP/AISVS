# C9.7: Intent Verification and Constraint Gates

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Authorization answers "is the agent allowed to do this?" but intent verification answers "is this what the user actually wanted?" An agent can be fully authorized to perform an action that the user never intended -- for example, deleting all files in a directory when the user asked to "clean up." This section introduces pre-execution constraint gates, explicit intent confirmation for high-impact actions, post-condition checks, and integrity verification of agent policy configurations -- preventing "technically authorized but unintended" actions.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.7.1** | **Verify that** pre-execution gates evaluate proposed actions and parameters against hard policy constraints (deny rules, data handling constraints, allow-lists, side-effect budgets) and block execution on any violation. | 1 | D/V | **Policy-violating actions bypassing authorization.** Authorization policies may be too permissive (an agent authorized to "manage files" could delete critical system files). Pre-execution gates add a defense-in-depth layer with hard constraints: explicit deny rules (never delete /etc), data handling restrictions (never send PII to external APIs), and side-effect budgets (max N write operations per session). These are invariants that should never be violated regardless of authorization. | Review pre-execution gate configuration. Verify deny rules, data handling constraints, and allow-lists are defined. Test by submitting actions that violate each constraint type and confirming they are blocked before execution. Verify gates cannot be bypassed by the agent (gates must be enforced by the orchestration layer, not by the agent's own prompt). | Pre-execution gates are conceptually similar to web application firewalls (WAFs) but for agent actions. The challenge is defining constraints that are specific enough to be useful without being so restrictive that they block legitimate actions. "Side-effect budgets" (limiting the number of mutating operations) are a novel concept without mature tooling. |
| **9.7.2** | **Verify that** high-impact actions require explicit user intent confirmation that is integrity-protected and bound to the exact action parameters (and expires quickly) to prevent stale or substituted approvals. | 2 | D/V | **Intent substitution and stale approvals.** Related to 9.2.2 but focused on user intent rather than organizational approval. An agent may misinterpret ambiguous instructions ("clean up the database" -> DROP TABLE) and execute with the user's implicit consent. Explicit intent confirmation forces the user to see and approve the exact action. Expiration prevents old approvals from being reused for new actions. | Verify high-impact actions trigger an intent confirmation flow that presents exact parameters to the user. Confirm confirmations are cryptographically bound to the action parameters (changing parameters invalidates the confirmation). Test that confirmations expire after a short window (seconds to minutes). Verify stale confirmations are rejected. | This overlaps with 9.2.1/9.2.2 but addresses a different threat: 9.2 is about organizational approval workflows; 9.7.2 is about confirming that the agent correctly interpreted the user's intent. UX design is critical -- confirmation fatigue will cause users to approve blindly. Progressive disclosure (showing summary first, details on expand) can help. |
| **9.7.3** | **Verify that** post-condition checks confirm the intended outcome and detect unintended side effects; any mismatch triggers containment (and compensating actions where supported). | 2 | V | **Undetected unintended consequences.** Even with pre-execution checks and intent confirmation, an action may produce unexpected outcomes (a file move operation that also changes permissions, an API call that triggers a webhook chain). Post-condition checks provide the final layer of defense by verifying that the actual outcome matches the intended outcome and that no unintended side effects occurred. | Define expected outcomes and side-effect boundaries for key actions. Verify post-condition checks run after action execution. Test by introducing actions with unintended side effects and confirming they are detected. Verify that detection triggers containment (halting further actions) and compensating actions where feasible. | Post-condition checking requires defining what "intended outcome" means programmatically, which is action-specific. For simple actions (file write), checking that the file exists with correct content is straightforward. For complex actions (deploy to production), defining and checking all expected outcomes is much harder. This may require domain-specific plugins. |
| **9.7.4** | **Verify that** prompt templates and agent policy configurations are integrity-verified at load time against their approved versions (e.g., via hashes or signatures). | 3 | D/V | **Policy and prompt tampering.** If an attacker can modify prompt templates or agent policy configurations (via compromised deployment pipeline, filesystem access, or configuration management vulnerability), they can alter agent behavior without changing any code. Integrity verification at load time ensures the agent operates with approved configurations. | Verify that prompt templates and policy files have associated integrity hashes or signatures stored in a separate trusted location. Confirm the runtime checks integrity at load time and refuses to start with tampered configurations. Test by modifying a prompt template and verifying the integrity check fails. | Similar to code signing but for configuration. Git commit hashes can serve as integrity anchors if the deployment pipeline verifies the commit. For dynamic configurations (loaded from a database or API), a separate signing mechanism is needed. This is defense-in-depth against supply chain attacks on agent behavior. |

---

## Implementation Guidance

### The Prompt Fidelity Problem

Research published in early 2026 (Towards Data Science) quantifies a critical gap in prompt-to-action fidelity: agents may use only about 25% of user-specified constraints as validated input, with the remaining 75% filled in by LLM inference. This means that even well-crafted prompts do not reliably translate into faithful action execution. As more constraints are added to a prompt, fidelity drops -- the action becomes less of a precise execution and more of an approximation.

This finding directly motivates requirement 9.7.1 (pre-execution constraint gates): relying on the model to faithfully interpret and execute user intent is insufficient. Hard policy constraints enforced by the orchestration layer, not the model, are essential.

### Intent Security as a Discipline (2025--2026)

Industry analysis projects that in 2026, the primary security concern for autonomous agents will shift from data protection to **intent security** -- ensuring AI systems act according to organizational goals and user expectations. Intent security encompasses:

- **Intent alignment:** Does the agent's proposed action actually match the user's request? This is distinct from authorization (is the agent allowed?) and focuses on semantic fidelity.
- **Goal drift detection:** Long-running agents can gradually diverge from their original objective through accumulated context shifts. Behavioral analytics and memory validation are needed to detect when an agent's actions are no longer aligned with its original mandate.
- **Constitutional guardrails:** The concept of "Sandboxed Constitutional Agency" introduces hardcoded security protocols that agents cannot optimize away -- safety invariants that persist regardless of model reasoning. These are the "constraint gates" of requirement 9.7.1.

### Pre-Execution Gate Design

Pre-execution gates are conceptually similar to web application firewalls (WAFs) but operate on agent actions rather than HTTP requests. Effective gate design includes:

- **Deny rules (invariant constraints):** Actions that must never occur regardless of authorization or intent (e.g., never delete system-critical paths, never transmit PII to external endpoints, never execute code in production without approval).
- **Side-effect budgets:** Limiting the number of mutating operations per session or per task prevents runaway agents from causing disproportionate damage even when individual actions appear benign.
- **Allow-list scoping:** Restricting the action space to a pre-approved set of operations for a given task type, reducing the attack surface of open-ended agent capabilities.
- **Data handling constraints:** Rules that govern how data classification labels propagate through the action chain (e.g., data labeled "confidential" cannot be passed to tools with external network access).

### Post-Condition Verification Approaches

Post-condition checks (9.7.3) close the verification loop after execution. Practical approaches include:

- **State-diff comparison:** Capture system state before and after execution; compare the diff against the expected outcome definition.
- **Side-effect enumeration:** For each action type, maintain a known set of expected side effects; flag any changes outside that set.
- **Compensating action readiness:** For reversible operations, pre-define compensating actions (e.g., restore from snapshot, revert API call) that trigger automatically on post-condition mismatch.
- **Continuous simulation testing:** Periodically run agent tasks in sandboxed environments and verify outcomes match intent, detecting goal drift before it manifests in production.

### Integrity Verification for Agent Configurations

Requirement 9.7.4 addresses supply chain attacks on agent behavior. If an attacker can modify prompt templates or policy configurations, they alter agent behavior without changing code. Practical integrity verification approaches:

- **Git commit hashes as integrity anchors:** If the deployment pipeline verifies the commit hash, prompt templates committed to version control have a built-in integrity chain.
- **Separate signing for dynamic configurations:** For configurations loaded from databases or APIs, a separate signing mechanism (e.g., JWS-signed configuration payloads) is needed since Git-based integrity does not apply.
- **Load-time verification:** The runtime must verify integrity at startup and refuse to operate with tampered configurations, similar to code signing for executables.

---

## Related Standards & References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) -- intent mismatch is a core excessive agency risk
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) -- covers intent verification concepts
- [Prompt Fidelity: Measuring How Much of Your Intent an AI Agent Actually Executes (Towards Data Science, 2026)](https://towardsdatascience.com/prompt-fidelity-measuring-how-much-of-your-intent-an-ai-agent-actually-executes/) -- quantitative research on prompt-to-action fidelity gaps
- [AI Agent Guardrails: Production Guide for 2026 (Authority Partners)](https://authoritypartners.com/insights/ai-agent-guardrails-production-guide-for-2026/) -- practical guardrail implementation patterns
- [The Rise of Agentic AI Security: Protecting Workflows, Not Just Apps (Reco)](https://www.reco.ai/blog/rise-of-agentic-ai-security) -- intent security as an emerging discipline
- AISVS C09.2 (High-Impact Action Approval) -- organizational approval workflows complement intent verification
- AISVS C02 (User Input Validation) -- input validation is the first layer; intent verification is the last layer before execution

---

## Open Research Questions

- Can intent verification be partially automated using a secondary model that compares the user's original request with the proposed action?
- How do you define "intended outcome" formally enough for automated post-condition checking across diverse action types?
- What is the right expiration window for intent confirmations? Too short causes failures; too long enables replay.
- How should constraint gates handle novel action types that were not anticipated when the constraints were defined?
- Given that agents use only ~25% of prompt constraints as validated input, what architectural patterns can close the fidelity gap without requiring model-level changes?
- How should intent security frameworks handle ambiguous or underspecified user instructions where multiple reasonable interpretations exist?

---
