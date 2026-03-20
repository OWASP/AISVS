# C11.8: Agent Security Self-Assessment

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 3 | **IDs:** 11.8.1--11.8.3

## Purpose

For agentic AI systems, validate that the agent's reasoning and actions are subject to security-focused review mechanisms. Agentic systems -- AI that can plan, use tools, and take actions autonomously -- present unique adversarial robustness challenges because harmful behavior can emerge from sequences of individually benign actions. This section requires that agents have pre-execution security review mechanisms, that these mechanisms are hardened against adversarial bypass, and that security warnings trigger appropriate escalation.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.8.1** | **Verify that** agentic systems include a mechanism to review planned high-risk actions against security policy before execution (e.g., a secondary model, rule-based checker, or structured self-review step). | 2 | D/V | Agents executing harmful actions due to adversarial manipulation, hallucinated plans, or goal misalignment. Without pre-execution review, a compromised or confused agent can take irreversible actions (deleting data, sending unauthorized communications, modifying configurations) before anyone notices. | Review agent architecture for pre-execution review mechanisms. Identify which actions are classified as "high-risk" and verify the classification is comprehensive. Test the review mechanism with planned actions that violate security policy and confirm they are caught. Verify that the review mechanism cannot be skipped or bypassed by the agent itself. Test with edge cases: actions that are individually benign but collectively harmful. | Defining "high-risk actions" is context-dependent and requires careful analysis of the agent's capabilities. Self-review (asking the same model to evaluate its own plan) is the weakest form of review due to sycophancy and shared failure modes. Secondary models provide better independence but add latency and cost. Rule-based checkers are reliable but brittle and can miss novel attack patterns. A layered approach (rules + model review) is recommended. |
| **11.8.2** | **Verify that** security review mechanisms are protected against manipulation by adversarial inputs (e.g., the review step cannot be overridden or bypassed through prompt injection). | 2 | D/V | Adversarial bypass of the security review layer itself. If an attacker can inject instructions that cause the reviewer to approve harmful actions, the review mechanism provides no protection. This is a meta-attack: attacking the defense rather than the primary model. Related to OWASP LLM01 (Prompt Injection). | Attempt to bypass the review mechanism through: injected instructions in tool outputs, manipulated context that redefines security policy, prompt injection targeting the reviewer specifically, social engineering of the review step (e.g., "this action has already been approved"). Verify architectural separation between the review mechanism and untrusted inputs. Check that the reviewer's security policy is not modifiable by the agent or its inputs. | This is one of the hardest requirements to verify because the attack surface is the same as prompt injection generally. Architectural separation (running the reviewer with a separate, hardened system prompt that cannot see untrusted content directly) is the strongest approach. The reviewer should evaluate a structured action description, not raw user/tool input. No current approach provides guaranteed protection against all prompt injection variants. |
| **11.8.3** | **Verify that** security review warnings trigger enhanced monitoring or human intervention workflows for the affected session or task. | 3 | D/V | Security warnings that are generated but not acted upon, or that result in a simple block without investigation. A security review warning may indicate an active attack, a system misconfiguration, or a novel failure mode -- all of which require follow-up beyond just blocking the immediate action. | Review escalation workflows triggered by security review warnings. Verify that warnings result in: enhanced logging for the session, notification to security operations, human review queue entry for the task, and session-level risk elevation (tighter controls for subsequent actions in the same session). Test end-to-end: trigger a security warning and verify escalation workflow execution. | Human intervention workflows must be designed for the expected volume of warnings -- too many warnings cause alert fatigue. Session-level risk elevation (treating the entire session as potentially adversarial after one warning) is a useful pattern but may impact legitimate users who trigger false positives. Consider tiered escalation based on warning severity. |

---

## Implementation Guidance (2024--2026 Research)

### Metacognitive Security and Self-Monitoring

The concept of "metacognitive security" -- agents that monitor and evaluate their own security posture -- has advanced significantly in 2024--2026 research:

- **Agentic metacognition for failure prediction**: Research from Arxiv (2025, paper 2509.19783) introduces metacognitive agent architectures where continuous self-evaluation of the agent's state against predefined triggers enables proactive handoff protocols. When an agent detects impending failures or policy violations, structured human-guided recovery is initiated rather than allowing uncontrolled operation. This generates traceable, auditable logs of agent decisions and reasons for escalation, directly supporting requirement 11.8.3.
- **Self-evaluation through chain-of-thought**: Galileo's research on self-evaluation in AI agents demonstrates that chain-of-thought reasoning enables agents to evaluate answer quality, recognize limitations, and identify potential errors through metacognitive processes. When applied to security, this pattern allows agents to reason explicitly about whether a planned action might violate security policy before execution.
- **Declared vs. observed behavior comparison**: The CSA MAESTRO framework (2025) introduces a pattern where an agent's declared skill behavior is compared against its observed behavior to identify deceptive, unsafe, or non-compliant functionality -- such as agents attempting to invoke unapproved services or access tools outside their declared scope. This comparison mechanism is a concrete implementation approach for requirement 11.8.1.

### Agentic AI Security Scoping

AWS published the Agentic AI Security Scoping Matrix (2025--2026), establishing a framework for classifying agent security requirements based on autonomy level and capability scope. Key findings relevant to self-assessment include:

- Organizations report a significant readiness gap: only 18% of respondents are "highly confident" their current identity and access management systems can manage agent identities effectively, despite 40% already having agents in production.
- Agent security self-assessment is most effective when combined with external monitoring -- self-review alone is insufficient because the agent shares failure modes with its own reviewer.

### Architecture Patterns for Security Review

Emerging best practices for implementing requirement 11.8.1 include a layered approach:

1. **Rule-based pre-filters**: Fast, deterministic checks against known-bad action patterns (e.g., data deletion, privilege escalation, external communication). Reliable but brittle against novel attacks.
2. **Secondary model review**: A separate, hardened model evaluates structured action descriptions (not raw user input) against security policy. Provides independence from the primary model's failure modes but adds latency.
3. **Architectural isolation**: The review mechanism receives a sanitized, structured representation of the proposed action rather than the full conversation context, reducing the attack surface for prompt injection targeting the reviewer (11.8.2).

### Hardening Review Mechanisms Against Bypass

The hardening of security review mechanisms (11.8.2) remains one of the most challenging problems in agentic AI security. 2025--2026 research confirms that:

- No current approach provides guaranteed protection against all prompt injection variants targeting the reviewer.
- The strongest mitigation is architectural: the reviewer should never directly process untrusted inputs. Instead, the primary agent produces a structured action proposal (tool name, parameters, justification), and only this structured representation is evaluated.
- Multi-agent review architectures (dedicated security agent reviewing all actions) show promise but introduce coordination complexity and latency.

---

## Related Standards & References

- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm012025-prompt-injection/) -- Prompt injection is the primary attack vector against agent review mechanisms
- [OWASP LLM09:2025 Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/) -- Agent hallucination leading to harmful planned actions
- [MITRE ATLAS AML.T0054 -- LLM Prompt Injection](https://atlas.mitre.org/techniques/AML.T0054) -- Prompt injection techniques applicable to agent review bypass
- [NIST AI 100-1 -- Artificial Intelligence Risk Management Framework](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) -- Risk management for autonomous AI systems
- [CSA MAESTRO -- Agentic AI Threat Modeling Framework](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) -- Layer-by-layer threat modeling for agentic AI
- [AWS Agentic AI Security Scoping Matrix](https://aws.amazon.com/blogs/security/the-agentic-ai-security-scoping-matrix-a-framework-for-securing-autonomous-ai-systems/) -- Framework for scoping agent security controls by autonomy level
- [Agentic Metacognition -- Arxiv 2509.19783 (2025)](https://arxiv.org/abs/2509.19783) -- Self-aware agent architectures for failure prediction and human handoff
- [Self-Evaluation in AI Agents -- Galileo](https://galileo.ai/blog/self-evaluation-ai-agents-performance-reasoning-reflection) -- Chain-of-thought self-evaluation for agent security reasoning
- [Obsidian Security -- From Agentic AI to Autonomous Risk](https://www.obsidiansecurity.com/blog/agentic-ai-security) -- Enterprise agentic AI security challenges
- AISVS C9 (Orchestration and Agents) -- Complementary agent security controls

---

## Open Research Questions

- What is the optimal architecture for agent security review -- same model, different model, rule-based system, or hybrid?
- Can security review mechanisms be made robust against prompt injection without architectural isolation from untrusted inputs?
- How should "high-risk actions" be classified in a general-purpose agent that can use arbitrary tools -- is a capability-based approach (classifying tool permissions) more practical than action-based classification?
- What is the right balance between security review thoroughness and agent response latency -- can review be done asynchronously for some action types?
- How do multi-agent systems change the security review model -- should agents review each other, or should a dedicated security agent review all actions?
- Can metacognitive self-monitoring reliably detect adversarial manipulation of the agent's own reasoning, or does this fundamentally require external observation?
- How should the fidelity of "declared vs. observed behavior" comparison be measured, and what deviation thresholds should trigger security escalation?

---
