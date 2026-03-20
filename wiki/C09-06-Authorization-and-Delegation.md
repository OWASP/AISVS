# C9.6: Authorization, Delegation, and Continuous Enforcement

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Agents act on behalf of users and interact with systems that have their own access control policies. This section ensures that agent actions are authorized against fine-grained policies at execution time, that delegation context (who the agent is acting for, with what scope) is propagated and enforced throughout the call chain, and that authorization decisions are never made by the AI model itself. The core principle: access control must be enforced by deterministic policy engines, not probabilistic language models.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.6.1** | **Verify that** agent actions are authorized against fine-grained policies enforced by the runtime that restrict which tools an agent may invoke, which parameter values it may supply (e.g., allowed resources, data scopes, action types), and that policy violations are blocked. | 1 | D/V | **Unauthorized tool invocation and parameter abuse.** Without fine-grained authorization, an agent may invoke any tool with any parameters, even if the initiating user is not authorized for that action. An agent authorized to read files should not be able to delete them; an agent authorized to query one database should not be able to query another. Prompt injection can instruct an agent to invoke tools outside its authorized scope. | Review the policy engine configuration. Verify that each tool has an associated policy specifying allowed callers, parameter constraints, and data scopes. Test by attempting unauthorized tool invocations and out-of-scope parameter values. Confirm the runtime blocks these attempts and logs the violation. Verify policies are evaluated server-side, not by the agent itself. | OPA (Open Policy Agent), Cedar (AWS), and Google Zanzibar-style systems can enforce fine-grained policies. The challenge is defining policies at the right granularity -- per-tool policies are straightforward, but per-parameter-value policies require deep integration with the tool's semantics. Policy management overhead grows with the number of tools and agents. |
| **9.6.2** | **Verify that** when an agent acts on a user's behalf, the runtime propagates an integrity-protected delegation context (user ID, tenant, session, scopes) and enforces that context at every downstream call without using the user's credentials. | 2 | D/V | **Scope creep and cross-tenant access.** Without integrity-protected delegation context, an agent may "forget" or "modify" its delegation scope as it chains through multiple tool calls. In multi-tenant systems, a corrupted or missing tenant context can lead to cross-tenant data access. Using the user's actual credentials (instead of a delegation token) gives the agent the user's full permissions rather than a scoped subset. | Trace a multi-step agent execution and verify the delegation context (user ID, tenant, session, scopes) is present and integrity-verified at every downstream call. Test by: (a) stripping the delegation context and confirming the call is rejected, (b) modifying the context and confirming integrity verification fails, (c) attempting cross-tenant access and confirming it is blocked. | OAuth 2.0 token exchange (RFC 8693) and macaroons provide mechanisms for scoped delegation tokens. The delegation context must be propagated through all agent communication layers (HTTP headers, message metadata, context objects). Key gap: most agent frameworks do not have built-in delegation context propagation -- this must be custom-built. |
| **9.6.3** | **Verify that** authorization is re-evaluated on every call (continuous authorization) using current context (user, tenant, environment, data classification, time, risk). | 2 | D/V | **Stale authorization and changed context.** Long-running agent tasks may execute over minutes or hours. During that time, user permissions may change, sessions may expire, or risk context may shift (e.g., anomalous behavior detected). Without continuous re-evaluation, an agent can continue acting on stale authorizations. An attacker who gains temporary access can initiate a long-running agent task and retain access after their permissions are revoked. | Verify that each tool invocation triggers a fresh authorization check (not cached from a previous check). Revoke a user's permissions mid-execution and confirm that subsequent agent actions on their behalf are blocked. Change the risk context (e.g., trigger an anomaly alert) and confirm authorization is re-evaluated with the new context. | Continuous authorization adds latency to every tool call. Caching strategies (short-TTL caches, event-driven cache invalidation) can mitigate this but introduce a window of vulnerability. Policy engines need to be performant enough for per-call evaluation. This aligns with Zero Trust principles (NIST SP 800-207) -- "never trust, always verify." |
| **9.6.4** | **Verify that** all access control decisions are enforced by application logic or a policy engine, never by the AI model itself, and that model-generated output (e.g., "the user is allowed to do this") cannot override or bypass access control checks. | 2 | D/V | **Model-based access control bypass.** If the AI model makes access control decisions (e.g., "Based on the conversation, this user seems authorized to view this data"), prompt injection can manipulate these decisions. LLMs are not access control systems -- they are probabilistic text generators. Any access control decision made by a model can be influenced by adversarial input. | Review the architecture to confirm all access control checks are performed by deterministic code/policy engines, not by model inference. Search for patterns where model output influences access decisions (e.g., model output parsed for "allowed"/"denied" strings). Test by crafting prompts that instruct the model to claim elevated privileges and verify these claims have no effect on actual access control enforcement. | This is a critical architectural principle. Common anti-pattern: using the model to "decide" whether a user is authorized based on conversation context. Another anti-pattern: letting the model choose which tools to call without a policy engine validating the choice. The policy engine must sit between the model's tool selection and actual tool execution. |

---

## Implementation Guidance

### The Authorization Crisis for Agentic AI (2025--2026)

Traditional IAM frameworks were designed for human users and static service accounts. Research and industry analysis in 2025--2026 identifies seven critical failures when applying these frameworks to AI agents (ISACA, 2025):

1. **Coarse-grained permissions:** Agents need fine-grained, task-specific permissions that dynamically change based on context, not static role-based access with long-lived tokens.
2. **Single-entity model limitations:** Current systems cannot track complex nested delegations where agents spawn sub-agents or represent multiple principals simultaneously.
3. **Context blindness:** Access decisions lack awareness of runtime context, agent intent, or risk level -- permissions remain static throughout sessions.
4. **Scalability pressures:** Hundreds or thousands of transient agents generate overwhelming token management demands (issuance, validation, revocation).
5. **Inadequate inter-agent authentication:** OAuth and SAML rely on hierarchical trust models unsuitable for decentralized agent networks that require peer-to-peer trust.
6. **Secret sprawl:** Each agent's multiple API integrations create a multiplicative factor in secrets requiring rotation and storage.
7. **Revocation complexity:** Revoking access in one place does not automatically cut off access elsewhere across distributed ephemeral sessions.

A 2026 survey (Grantex) found that 93% of popular AI agent projects use unscoped API keys, and fewer than half of companies deploying agents had comprehensive governance in place.

### Emerging Standards and Frameworks

- **NIST Agent Identity and Authorization (February 2026):** NIST released a concept paper on "Accelerating the Adoption of Software and Artificial Intelligence Agent Identity and Authorization," proposing demonstrations to explore identity and authorization practices for AI agents in enterprise settings. This signals that federal standardization of agent authorization is underway.
- **Agent Relationship-Based Identity and Authorization (ARIA):** Treats delegation relationships as explicit, cryptographically verifiable entities in a graph. Every delegation is a distinct relationship that enables surgical permission revocation and full auditability. ARIA integrates OAuth 2.0 Rich Authorization Requests, OAuth 2.0 token exchange (RFC 8693), and OpenID AuthZEN for context-aware policy evaluation.
- **OpenID AuthZEN:** Enables evaluation of fine-grained, context-aware policies without abandoning installed-base OAuth infrastructure -- applying constraints such as geo-fences, budget thresholds, and temporal windows alongside requirements like audit trails and notifications.
- **Zero Trust Identity with DIDs:** Combines Decentralized Identifiers, Verifiable Credentials, Agent Naming Services, and zero-knowledge proofs for privacy-preserving compliance verification in agent identity.

### Practical Authorization Patterns

- **Scopes for coarse-grained limits, claims for fine-grained context:** Use OAuth scopes to define broad permission boundaries and token claims to carry runtime context (user identity, tenant, data classification, risk score) that policy engines evaluate per-call.
- **On-behalf-of delegation:** OAuth 2.0 token exchange (RFC 8693) cryptographically binds an actor (the agent) to a delegator (user or service), preserving the chain of responsibility without exposing the user's credentials.
- **Policy engines at the enforcement point:** OPA, Cedar, and Zanzibar-style systems enforce fine-grained policies. The policy engine must sit between the model's tool selection and actual tool execution -- never after.
- **Short-lived, single-use credentials:** Replace long-lived API keys with ephemeral tokens scoped to individual tasks. This limits blast radius and eliminates the stale-authorization window.

### Anti-Patterns to Avoid

- Letting the AI model make access control decisions based on conversation context (prompt injection can manipulate these).
- Using the end user's actual credentials for agent actions instead of scoped delegation tokens.
- Caching authorization decisions for long-running agent tasks without event-driven invalidation.
- Granting agents broad "admin" or "full-access" scopes because their task is open-ended.

---

## Related Standards & References

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final) -- continuous verification and least-privilege principles
- [NIST Concept Paper: AI Agent Identity and Authorization (Feb 2026)](https://www.hoganlovells.com/en/publications/shaping-the-future-of-ai-security-nist-seeking-input-on-agent-identity-authorization) -- federal standardization initiative
- [OAuth 2.0 Token Exchange (RFC 8693)](https://www.rfc-editor.org/rfc/rfc8693) -- delegation token mechanism
- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) -- general-purpose policy engine
- [AWS Cedar](https://www.cedarpolicy.com/) -- policy language and evaluation engine
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) -- excessive permissions and lack of authorization
- [The Looming Authorization Crisis: Why Traditional IAM Fails Agentic AI (ISACA)](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-looming-authorization-crisis-why-traditional-iam-fails-agentic-ai) -- analysis of IAM failures for agents
- [State of AI Agent Security 2026 (Grantex)](https://grantex.dev/report/state-of-agent-security-2026) -- survey data on agent security practices
- [Best Practices of Authorizing AI Agents (Oso)](https://www.osohq.com/learn/best-practices-of-authorizing-ai-agents) -- practical implementation guidance
- [AI Agents Are Becoming Authorization Bypass Paths (Hacker News)](https://thehackernews.com/2026/01/ai-agents-are-becoming-privilege.html) -- real-world exploitation patterns
- AISVS C05 (Access Control) -- general AI access control; C09.6 addresses agent-specific delegation and continuous enforcement

---

## Open Research Questions

- How do you define "minimum necessary scope" for delegation tokens when the agent's task is open-ended (e.g., "research and summarize")?
- Can authorization policies for agent actions be auto-generated from tool manifests and user role definitions?
- What are the performance implications of per-call authorization in high-throughput agent systems, and what caching strategies are safe?
- How should authorization work for agents that operate across organizational boundaries (federated agent systems)?
- How will the NIST AI Agent Identity and Authorization framework interact with existing OAuth/OIDC infrastructure once finalized?
- Can the ARIA graph-based delegation model scale to environments with thousands of transient agents and sub-agents?

---
