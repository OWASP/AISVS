# C9.5: Secure Messaging and Protocol Hardening

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Agent outputs often become another agent's input, plan, memory update, or tool argument. C9.5 focuses on the semantic layer of that exchange: a message can be perfectly valid JSON and still be unsafe if it changes the task intent, swaps the subject, smuggles instructions, changes units, invents approvals, or violates business invariants.

This section should be read narrowly. Transport encryption, authentication, replay protection, and protocol-specific schema validation remain important prerequisites, but they are covered by adjacent controls such as C09.4 and C10. C9.5 asks whether the receiving agent validates that the content it is about to trust still makes sense for the task, actor, authority, state, and downstream impact.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **9.5.1** | **Verify that** agent outputs propagated to downstream agents are validated against semantic constraints (e.g., value ranges, logical consistency) in addition to schema validation. | 2 | **Semantic message manipulation.** A compromised or misled agent can send schema-valid content that changes downstream behavior: negative prices, stale approval state, a different tenant ID, hidden instructions in text fields, mismatched task IDs, unsupported delegation, or a summary that reframes the original user intent. This maps closely to OWASP Agentic ASI07 Insecure Inter-Agent Communication and ASI06 Memory and Context Poisoning, and to MITRE ATLAS patterns such as AML.T0051 LLM Prompt Injection and AML.T0080.000 AI Agent Context Poisoning: Memory. | Review every agent-to-agent and agent-to-tool contract that can influence decisions, memory writes, or tool calls. For each field and free-text region, verify documented invariants: allowed ranges, units, currencies, actor and tenant binding, task/session binding, source provenance, approval status, temporal ordering, mutually exclusive states, and intent alignment with the original task anchor. Test with payloads that satisfy the schema but violate meaning: out-of-range values, role swaps, stale state, impossible combinations, hidden directives, prompt-injection phrasing, contradictory summaries, and cross-tenant identifiers. Confirm the receiver rejects, quarantines, or routes these outputs to review before adding them to context, memory, plans, or tool parameters. | Semantic validation is domain-specific. JSON Schema, Protocol Buffers, Pydantic, and Zod can enforce structure and many invariants, but free-text intent and logical consistency still require task-specific checks, policy engines, guardrail services, replayable test cases, and human review for high-impact flows. LLM-as-judge checks are useful as secondary signals but should not be the only enforcement boundary. |

---

## Notable Incidents and Research

| Date | Finding | Relevance | Link |
|------|---------|-----------|------|
| Apr 2025 | Invariant Labs disclosed MCP tool poisoning patterns where hidden instructions in tool descriptions or outputs influence agent behavior. | Tool metadata and tool responses are downstream inputs. The receiver needs semantic checks that treat these fields as untrusted content, not trusted instructions. | [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) |
| Oct 2025 | Unit 42 described agent session smuggling in A2A systems, where a malicious peer injects covert instructions during a stateful multi-turn session. | The recommended task-anchor defense is directly aligned with 9.5.1: each received message should be checked against the original task intent and rejected when it drifts. | [Unit 42](https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/) |
| Dec 2025 | OWASP released the Top 10 for Agentic Applications 2026. ASI07 explicitly covers insecure inter-agent communication, including missing semantic validation. | Gives auditors a current standard vocabulary for semantic manipulation, descriptor forgery, replayed delegation, and agent-in-the-middle scenarios. | [OWASP](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| Jan 2026 | MCP-ITP showed implicit tool poisoning can induce a legitimate high-privilege tool to perform malicious operations, reaching up to 84.2% attack success rate in experiments while evading many detectors. | Demonstrates why receivers cannot rely on whether the poisoned tool was invoked; all tool metadata and propagated outputs need semantic review before they influence planning. | [arXiv:2601.07395](https://arxiv.org/abs/2601.07395) |
| Feb 2026 | Microsoft reported recommendation poisoning that manipulates assistant memory and mapped it to MITRE ATLAS AML.T0051 and AML.T0080.000. | Memory writes are downstream propagation. Semantic constraints should block attempts to mark attacker-controlled content as trusted, authoritative, or persistent. | [Microsoft](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) |
| Feb-Apr 2026 | A comparative threat model for MCP, A2A, Agora, and ANP identified protocol-level risks across trust assumptions, lifecycle behavior, and validation or attestation gaps. | Reinforces that semantic validation must survive mixed-protocol deployments where agents negotiate capabilities and route work across independent systems. | [arXiv:2602.11327](https://arxiv.org/abs/2602.11327) |
| Apr 2026 | A large MCP server study evaluated 1,899 open-source MCP servers and found MCP-specific tool poisoning in 5.5% of servers. | Public tool ecosystems already contain poisoned metadata. Production systems should pin, diff, scan, and validate tool descriptions before exposing them to downstream agents. | [arXiv:2506.13538](https://arxiv.org/abs/2506.13538) |

## Implementation Maturity

| Control Area | Maturity | Notes |
|--------------|:---:|-------|
| Structured contracts with semantic validators | Mature | Pydantic field validators, Zod `refine` / `superRefine`, JSON Schema custom formats, and Protocol Buffers plus application validators can enforce ranges, enums, units, required relationships, and state transitions. They work best when contracts are versioned and treated as deploy artifacts rather than model prompts. |
| Runtime guardrails for agent outputs | Emerging | Guardrails AI supports Pydantic-backed structured output validation and custom validators. NVIDIA NeMo Guardrails provides input, output, topical, and agentic security rails, including validation of tool inputs and outputs before and after invocation. These help, but they still require domain-specific policies. |
| Policy-as-code checks | Mature | Open Policy Agent/Rego, Cedar, or equivalent policy engines can validate claims that are easier to express as authorization or business rules: actor may approve action, tenant IDs match, transfer amount is below the delegated limit, and workflow state permits the transition. |
| Protocol metadata validation | Emerging | A2A Agent Cards and MCP tool definitions are executable trust inputs for the receiver. Treat names, descriptions, examples, schemas, auth declarations, and capability lists as untrusted metadata until they are fetched from an approved source, authenticated where the protocol supports it, pinned or versioned, diff-reviewed, and checked for instruction-shaped content. |
| Natural-language intent validation | Emerging | Task-anchor comparison, intent-diffing, embedding similarity, classifier checks, and LLM-based review can flag drift from the original task. They are useful for free-text summaries and peer-agent messages, but false positives and evasions remain common. Use them to gate review, not to silently bless high-impact actions. |
| Tool description and output scanning | Emerging | Static checks can flag imperative phrases, invisible Unicode, base64 blobs, references to unrelated tools, unexpected URLs, or description changes after install. OWASP's MCP tool poisoning guidance recommends constrained response formats, server allowlists, least privilege, and approval for sensitive operations. |

## Verification Playbook

1. **Trace propagation paths.** List every place an agent output becomes another agent's context, memory, plan, routing decision, or tool argument. Include summaries, errors, tool descriptions, retrieved documents, and async status updates.
2. **Define semantic invariants.** For each path, document the facts that must remain true: actor, tenant, task ID, authorization state, units, limits, ordering, provenance, allowed intent, and permitted downstream actions.
3. **Bind messages to task context.** Require task/session identifiers and compare each received message against the original user request or task anchor. Reject messages that introduce unrelated goals, credential prompts, or unexpected delegation.
4. **Validate before model exposure.** Run schema and semantic checks before placing peer-agent or tool output into the LLM context, memory, or planner state. A rejected message should not be summarized into trusted context.
5. **Test schema-valid attacks.** Add regression cases for negative or extreme values, tenant swaps, stale approvals, impossible status transitions, hidden directives, instruction-shaped metadata, prompt-injection phrasing, and contradictory summaries.
6. **Log decisions.** Record accepted, rejected, quarantined, and human-reviewed messages with the validator version, policy decision, source agent identity, and downstream consumer. Logs should support incident review without storing unnecessary sensitive payloads.

## Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C09.4 Agent Identity & Audit](C09-04-Agent-Identity-and-Audit.md) | Source identity and attribution | C9.5 assumes the receiver can identify the sending agent. C9.4 supplies cryptographic identity and tamper-evident audit so semantic failures can be attributed. |
| [C09.7 Intent Verification](C09-07-Intent-Verification.md) | Task-anchor checks | C9.7 validates proposed actions against the user's intent. C9.5 applies the same idea to messages and outputs before they influence downstream agents. |
| [C09.8 Multi-Agent Isolation](C09-08-Multi-Agent-Isolation.md) | Blast-radius control | Semantic validation reduces the chance of bad propagation; isolation limits the impact when a peer agent still sends unsafe content. |
| [C10.4 MCP Schema Validation](../C10-MCP-Security/C10-04-Schema-Message-Validation.md) | Protocol-specific schema enforcement | C10.4 handles MCP schemas and tool definition change detection. C9.5 adds business meaning and intent validation after the message is structurally valid. |
| [C13.6 Proactive Security Behavior Monitoring](../C13-Monitoring-and-Logging/C13-06-Proactive-Security-Behavior-Monitoring.md) | Detection and drift monitoring | Logs from semantic validators become evidence for detecting tool poisoning, context drift, and abnormal peer-agent behavior. |
| [C11 Adversarial Robustness](../C11-Adversarial-Robustness/C11-Adversarial-Robustness.md) | Malicious or misleading outputs | C11 covers broader adversarial robustness. C9.5 focuses on validating the content being handed from one agent boundary to the next. |

## Protocol Notes

- **A2A:** Agent Cards and task messages make cross-agent collaboration explicit, but stateful sessions create room for hidden instruction drift. The A2A specification requires HTTPS for production deployments and per-request authentication based on declared Agent Card requirements; C9.5 adds the content-level check that a properly authenticated peer is still staying within the delegated task.
- **MCP:** Tool descriptions, parameter descriptions, errors, and tool results can become model-facing context. MCP security guidance treats server outputs as untrusted and recommends strong authorization, SSRF protection, session hygiene, scope minimization, and careful trust-boundary handling. C9.5 adds the semantic check before those outputs reach downstream reasoning.
- **Mixed-protocol deployments:** Agents often bridge A2A, MCP, custom REST, queues, and shared memory. Validate at the receiving boundary rather than assuming the previous protocol hop preserved meaning.
- **Free-text summaries:** Summaries are high-risk propagation artifacts because they compress evidence and can quietly change intent. Require source links, confidence, omitted-field disclosure, and comparison against the original evidence for high-impact workflows.

## Protocol-Specific Verification Checks

| Boundary | Auditor Checks | Failure Examples |
|----------|----------------|------------------|
| A2A Agent Card intake | Confirm Agent Cards are fetched over HTTPS, authenticated when extended cards are used, stored with version/hash history, and reviewed before new capabilities, examples, URLs, or security schemes are exposed to planning. Compare public and authenticated cards for unexpected capability expansion. | A peer updates a capability description to request credentials, adds a lookalike high-privilege capability, or changes its endpoint after approval. |
| A2A task/session messages | Verify each received message carries task/session binding and is compared against the original task anchor, allowed capabilities, current workflow state, and user-approved impact level. Red-team with multi-turn requests that slowly shift from the delegated task to credential collection or tool execution. | A remote research agent asks the client to reveal tool schemas, replay prior conversation history, or execute an unrelated purchase during a stateful session. |
| MCP tool metadata | Inspect how the client pins, diffs, and scans tool names, descriptions, parameter descriptions, annotations, and examples. Require review when a server changes metadata after install or when descriptions contain imperatives, invisible Unicode, encoded blobs, unrelated tool references, or external callback URLs. | A benign calculator tool includes hidden instructions to read local configuration, or a server changes descriptions after a trusted initial review. |
| MCP tool results and async events | Validate tool results, errors, resumed stream events, and `tools/list_changed` notifications before they enter model context. Check session IDs are not treated as authentication and that every inbound request is authorized independently. | A hijacked session queues a malicious event that changes offered tools, or an error message contains instructions that cause a privileged follow-up tool call. |
| Shared memory, queues, and summaries | Require provenance, tenant binding, source links, expiry, sensitivity labels, and contradiction checks before propagated output becomes memory or a queue message consumed by another agent. | A schema-valid summary drops caveats, changes the actor or amount, marks attacker-provided content as authoritative, or writes stale approval state into memory. |

## Hardening Recommendations

1. **Use typed envelopes for every propagated output.** Include sender, receiver, task ID, schema version, provenance, confidence, intended use, and expiry. Free-text should be carried as data inside the envelope, not as instructions.
2. **Separate instruction space from data space.** Quote or tag peer-agent content so it cannot be spliced into the system or developer instruction region. Do not let tool descriptions or outputs modify agent policy.
3. **Pin and diff agent and tool metadata.** Store hashes of tool descriptions, parameter descriptions, schemas, and agent capability cards. Block or re-review changes before exposing the new metadata to planning.
4. **Reject semantic drift.** Compare incoming messages to the task anchor and current workflow state. Unexpected goals, unrelated credential prompts, privilege changes, or task subject changes should terminate or quarantine the session.
5. **Treat memory writes as high-impact propagation.** Validate proposed memories for source, scope, sensitivity, trust level, expiry, and contradiction with existing policy before committing them.
6. **Gate high-impact downstream actions.** A schema-valid message should not be enough to trigger financial, identity, production, deletion, or disclosure actions. Require independent policy checks and human approval where required by C09.2 and C14.
7. **Red-team with schema-valid payloads.** Include poisoned tool metadata, contradictory summaries, invisible Unicode, stale authorization state, tenant swaps, prompt-injection phrasing, and hidden instructions in error messages.
8. **Monitor validator bypass attempts.** Alert on repeated semantic validation failures, sudden shifts in peer-agent messages, tool description changes, unexpected routing, and a sender that repeatedly asks downstream agents to use unrelated high-privilege tools.

---

## Related Standards & References

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) -- ASI07 includes missing semantic validation as an inter-agent communication failure
- [OWASP MCP Tool Poisoning](https://owasp.org/www-community/attacks/MCP_Tool_Poisoning) -- attack description and prevention guidance for poisoned MCP tool outputs
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) -- MCP trust-boundary, authorization, SSRF, session hijacking, and local server compromise guidance
- [A2A Protocol Specification](https://a2a-protocol.org/v0.3.0/specification/) -- Agent Card discovery, authentication, authorization, TLS, and declared security requirements
- [Agent Session Smuggling in Agent2Agent Systems](https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/) -- A2A multi-turn semantic drift and task-anchor defense
- [MCP-ITP: Automated Implicit Tool Poisoning](https://arxiv.org/abs/2601.07395) -- implicit tool poisoning benchmark and attack results
- [Model Context Protocol at First Glance](https://arxiv.org/abs/2506.13538) -- large-scale MCP server security and maintainability study
- [Security Threat Modeling for Emerging AI-Agent Protocols](https://arxiv.org/abs/2602.11327) -- comparative analysis of MCP, A2A, Agora, and ANP
- [Microsoft: AI Recommendation Poisoning](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) -- memory manipulation mapped to MITRE ATLAS AML.T0051 and AML.T0080.000
- [Guardrails AI Structured Data Validation](https://guardrailsai.com/guardrails/docs/how-to-guides/generate_structured_data) -- Pydantic-backed structured output validation and validators
- [Guardrails AI Custom Validators](https://guardrailsai.com/guardrails/docs/how-to-guides/custom_validators) -- custom validators for domain-specific checks
- [Pydantic AI Structured Output](https://pydantic.dev/docs/validation/latest/examples/pydantic_ai/) -- output type validation with Pydantic field validators
- [Pydantic AI Output Validators](https://pydantic.dev/docs/ai/core-concepts/output/) -- validation context and output validators for structured outputs and tool arguments
- [NVIDIA NeMo Guardrails Overview](https://docs.nvidia.com/nemo/guardrails/latest/about/overview.html) -- programmable guardrails, tool input/output validation, and agentic security rails
- [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs) -- policy-as-code decisions over structured JSON inputs
- [Cedar Policy Validation](https://docs.cedarpolicy.com/policies/validation.html) -- schema-backed validation for authorization policies and request expectations
- AISVS C10 (MCP Security) -- protocol-specific MCP controls that complement C9.5's semantic validation focus

---

## Open Research Questions

- How should teams specify semantic contracts for free-text peer-agent outputs without reducing every interaction to rigid forms?
- Which intent-diffing approaches reliably catch task drift without generating too many false positives for normal collaboration?
- How should validator decisions be composed across protocol boundaries when A2A, MCP, queues, and shared memory all participate in one workflow?
- Can tool and agent metadata pinning become a common client feature, and what should be re-approved when descriptions or schemas change?
- What evidence is enough for an auditor to conclude that semantic validation occurred before an output reached memory, planning, or tool execution?
- How should organizations measure whether LLM-based semantic checks are improving detection rather than adding another bypassable reasoning step?

## Related Pages

- [C11.8 Agent Security Self-Assessment](../C11-Adversarial-Robustness/C11-08-Agent-Security-Self-Assessment.md) -- Self-assessment gives teams a place to prove that message validators, metadata review, and high-impact action gates are exercised before an agent acts.
- [C02.1 Prompt Injection Defense](../C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) -- Prompt injection controls cover the upstream attack patterns that C9.5 must catch again when peer-agent and tool outputs cross a trust boundary.
- [C11.7 Security Policy Adaptation](../C11-Adversarial-Robustness/C11-07-Security-Policy-Adaptation.md) -- Adaptive policy work is closely related to keeping semantic validators, allowlists, and protocol metadata rules current without silently widening trust.
- [C09.9 Data Flow Isolation and Origin Enforcement](C09-09-Data-Flow-Isolation-Origin-Enforcement.md) -- Origin-aware data-flow controls help C9.5 validators decide which propagated facts, summaries, and tool results are allowed to influence downstream agents.
- [C02.2 Pre-Tokenization Input Normalization](../C02-User-Input-Validation/C02-02-Pre-Tokenization-Input-Normalization.md) -- Normalization checks catch invisible Unicode, encoded content, and metadata smuggling before semantic validators reason over the message body.

---
