# C05: Access Control & Identity for AI Components & Users

> **Source:** [`1.0/en/0x10-C05-Access-Control-and-Identity.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
> **Requirements:** 30 | **Sections:** 6

## Control Objective

Effective access control for AI systems requires robust identity management, context-aware authorization, and runtime enforcement following zero-trust principles. These controls ensure that humans, services, and autonomous agents only interact with models, data, and computational resources within explicitly granted scopes, with continuous verification and audit capabilities.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C5.1 | Identity Management & Authentication | 3 | [C05-01-Identity-Management-Authentication](C05-01-Identity-Management-Authentication.md) |
| C5.2 | Authorization & Policy | 8 | [C05-02-Authorization-Policy](C05-02-Authorization-Policy.md) |
| C5.3 | Query-Time Security Enforcement | 6 | [C05-03-Query-Time-Security-Enforcement](C05-03-Query-Time-Security-Enforcement.md) |
| C5.4 | Output Filtering & Data Loss Prevention | 3 | [C05-04-Output-Filtering-DLP](C05-04-Output-Filtering-DLP.md) |
| C5.5 | Multi-Tenant Isolation | 6 | [C05-05-Multi-Tenant-Isolation](C05-05-Multi-Tenant-Isolation.md) |
| C5.6 | Autonomous Agent Authorization | 4 | [C05-06-Autonomous-Agent-Authorization](C05-06-Autonomous-Agent-Authorization.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Privilege escalation through prompt injection causing the model to act with elevated permissions
- Cross-tenant data leakage in shared AI infrastructure (e.g., 2025 Salesloft-Drift breach affecting 700+ orgs)
- Agent identity spoofing in multi-agent systems; interagent trust gaps across organizational boundaries
- Confused deputy attacks where AI tools act with the user's credentials beyond intended scope
- **[2026-03]** API key leaks exposing AI model access at scale (xAI/Grok: 52 LLMs; Google Cloud: 2,863 keys with Gemini access)
- **[2026-03]** Unscoped API keys as dominant anti-pattern: 93% of audited AI agent projects lack scoped tokens (Grantex 2026)
- **[2026-03]** Indirect prompt injection weaponizing agent credentials: >90% success rate in controlled evaluations when agents have unrestricted capabilities
- **[2026-03]** Cascading delegation failures: compromised OAuth tokens propagating across multi-tenant agent deployments
- **[2026-03]** Secret proliferation: each agent spawns multiple identities, exponentially expanding attack surface (ISACA 2025)
- **[2026-03]** Agentic authorization bypass: agent actions evaluated against agent identity rather than requester identity, enabling indirect privilege escalation (The Hacker News, Jan 2026)
- **[2026-03]** AI agent gateway credential theft at scale: CVE-2026-25253 (OpenClaw, CVSS 8.8) exposed 17,500+ instances with stored API tokens for major AI providers
- **[2026-03]** Zero-click agentic browser compromise: PerplexedBrowser vulnerability family allows prompt injection via calendar invites to hijack authenticated agent sessions (Zenity Labs, Mar 2026)
- **[2026-03]** 88% of organizations reported confirmed or suspected AI agent security incidents in the past year (Gravitee 2026)
- **[2026-03]** KV-cache timing side channels in multi-tenant inference: PROMPTPEEK (NDSS 2025) achieves 95-99% prompt reconstruction accuracy by probing shared KV-cache hit/miss latency in vLLM and SGLang
- **[2026-03]** Direct KV-cache content extraction: collision and injection attacks reconstruct user inputs from plaintext cache entries stored, transmitted, or persisted across compute nodes (Shadow in the Cache, arxiv 2508.09442)

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Jul 2025 | xAI Grok API key leaked by DOGE staffer on public GitHub | Single API key exposed 52 LLMs; no step-up auth or key scoping prevented full model access (5.1.1, 5.1.2, 5.6.1) | [Obsidian Security](https://www.obsidiansecurity.com/resource/grok-api-key-leak-exposes-xai-models-to-major-security-risks) |
| Early 2025 | Second xAI internal API key exposed on GitHub for ~2 months | Long-lived credential with access to data linked to SpaceX, Tesla, Twitter/X (5.1.1, 5.1.3) | [Obsidian Security](https://www.obsidiansecurity.com/resource/grok-api-key-leak-exposes-xai-models-to-major-security-risks) |
| Aug 2025 | Salesloft-Drift OAuth token breach | Compromised third-party app tokens exposed 700+ downstream tenant environments; cascading delegation failure (5.5.2, 5.6.3) | [ScaleKit](https://www.scalekit.com/blog/oauth-vs-api-keys-for-ai-agents) |
| Feb 2026 | Google Cloud API key exposure (2,863 live keys with Gemini access) | Keys in client-side JS granted Gemini API access; one user reported $82K in charges in 48 hours; keys defaulted to "Unrestricted" (5.1.1, 5.2.1) | [The Hacker News](https://thehackernews.com/2026/02/thousands-of-public-google-cloud-api.html) |
| Feb 2026 | NIST NCCoE concept paper on AI agent identity and authorization | First NIST practical guidance initiative for enterprise AI agent identity (5.1.3, 5.6.1, 5.6.4) | [NIST NCCoE](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf) |
| Jan 2026 | Cedar joins CNCF as Sandbox project | Signals maturation of fine-grained authorization for AI workloads (5.2.6) | [InfoQ](https://www.infoq.com/news/2026/01/cedar-joins-cncf-sandbox/) |
| Apr 2025 | OpenID Connect for Agents (OIDC-A) 1.0 proposal | Extends OIDC with agent-specific claims for federated AI agent identity (5.1.3) | [Subramanya.ai](https://subramanya.ai/2025/04/28/oidc-a-proposal/) |
| 2025 | ISACA: "The Looming Authorization Crisis" for Agentic AI | Identifies 7 critical IAM gaps for autonomous agents; proposes ARIA framework (5.6.1-5.6.4) | [ISACA](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-looming-authorization-crisis-why-traditional-iam-fails-agentic-ai) |
| 2026 | Grantex State of Agent Security 2026 report | 93% of audited AI agent projects use unscoped API keys; 48% of security professionals cite agentic AI as top attack vector (5.6.1, 5.6.2) | [Grantex](https://grantex.dev/report/state-of-agent-security-2026) |
| 2025 | "Authenticated Delegation and Authorized AI Agents" (arxiv) | Formal analysis of delegation patterns for AI agent authorization (5.6.1, 5.6.3) | [arXiv](https://arxiv.org/html/2501.09674v1) |
| Feb 2026 | CVE-2026-25253: OpenClaw one-click RCE via auth token theft | Crafted URL steals auth tokens from 17,500+ AI agent gateways; stored credentials for Claude, OpenAI, Google AI exposed (5.1.1, 5.6.1, 5.6.2) | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-25253) |
| Mar 2026 | PerplexedBrowser: zero-click agentic browser compromise | Indirect prompt injection via calendar invites hijacks authenticated agent sessions; data exfiltration through agent's own authorized channels (5.4.1, 5.6.2) | [Help Net Security](https://www.helpnetsecurity.com/2026/03/04/agentic-browser-vulnerability-perplexedbrowser/) |
| Jan 2026 | AI Agents as Authorization Bypass Paths | Documents how shared AI agents evaluated against agent identity (not requester's) enable indirect privilege escalation (5.2.5, 5.6.4) | [The Hacker News](https://thehackernews.com/2026/01/ai-agents-are-becoming-privilege.html) |
| 2025 | IETF draft-oauth-ai-agents-on-behalf-of-user (draft-02) | OAuth 2.0 extension for AI agent delegation with `requested_actor` and `actor_token` parameters and JWT `act` claims (5.1.3, 5.6.3) | [IETF](https://datatracker.ietf.org/doc/draft-oauth-ai-agents-on-behalf-of-user/) |
| Jan 2026 | Auth0 Token Vault GA for AI Agents | RFC 8693 token exchange implementation for AI agents; isolates long-lived provider credentials from agent infrastructure (5.1.3, 5.6.3) | [Auth0](https://auth0.com/blog/auth0-token-vault-secure-token-exchange-for-ai-agents/) |
| May 2025 | HoneyBee: RBAC for Vector Databases via Dynamic Partitioning (SIGMOD 2026) | 13.5x lower query latency than RLS with 1.24x memory; 90.4% less memory than per-role indexes (5.3.3) | [arXiv](https://arxiv.org/abs/2505.01538) |
| NDSS 2025 | PROMPTPEEK: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving | 95-99% prompt reconstruction via timing side channels in vLLM/SGLang shared KV-cache (5.5.5) | [NDSS](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/) |
| May 2025 | vLLM Cache Salting RFC #16016 merged (Design A) | Per-tenant cache salt prevents cross-tenant prefix reuse; hierarchical multi-barrier design in active development (5.5.5) | [GitHub](https://github.com/vllm-project/vllm/issues/16016) |
| Feb 2026 | SafeKV: Selective KV-Cache Sharing with ChunkGuard | Mitigates 94-97% of timing side-channels; 40% TTFT reduction vs. full isolation; 2.66x throughput gain (5.5.5) | [arXiv](https://arxiv.org/abs/2508.08438) |
| 2025 | Shadow in the Cache / KV-Cloak defense | Demonstrates collision and injection attacks on plaintext KV-cache; KV-Cloak reversible obfuscation with ~5% latency overhead (5.5.5) | [arXiv](https://arxiv.org/abs/2508.09442) |
| Dec 2025 | OWASP Top 10 for Agentic Applications 2026 | New standard: Identity & Privilege Abuse (ASI03), Tool Misuse (ASI02) as top-3 risks; introduces Least Agency principle (5.6.1, 5.6.2) | [OWASP](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Policy engines:** OPA (Open Policy Agent, CNCF graduated), Cedar (AWS, CNCF Sandbox since Jan 2026), Casbin, OpenID AuthZEN, Permit.io (fine-grained RBAC/ABAC/ReBAC across apps, APIs, data layers, AI agents)
- **Policy administration:** OPAL (Open Policy Administration Layer) for keeping policies consistent across microservices and AI agents
- **Identity:** SPIFFE/SPIRE for workload identity, OAuth 2.0 for user-facing AI apps, OIDC-A (OpenID Connect for Agents) 1.0 proposal, ARIA (Agent Relationship-Based Identity and Authorization), Microsoft OAuth 2.0 on-behalf-of token exchange for agent delegation
- **Agent credential management:** Grantex (scoped JWT grant tokens, per-agent DIDs, delegation chains), ScaleKit (delegated agent access with on-behalf-of auth), Nango (secure AI agent API authentication), Auth0 Token Vault (GA Jan 2026; RFC 8693 token exchange with 30+ pre-integrated providers, per-user credential isolation), HashiCorp Vault (dynamic secrets for AI agent identity)
- **DLP:** Google DLP API, Microsoft Purview, Presidio, custom regex/NER-based PII filters
- **Multi-tenant isolation:** Kubernetes namespaces, Calico/Cilium network policies, database row-level security, Pinecone namespaces (up to 100K per index), Weaviate tenant-isolated collections
- **Vector DB access control:** Pinecone (document-level filtering, role-based retrieval, SOC 2/HIPAA/ISO 27001), Weaviate (tenant isolation, collection-level access), Qdrant (managed multi-tenant support)
- **Agent authorization:** LangChain tool permissions, OpenAI function calling constraints, Anthropic tool use scoping, Model Context Protocol (MCP) for authorization context negotiation, IETF `draft-oauth-ai-agents-on-behalf-of-user` (OAuth 2.0 agent delegation), IETF Secure Intent Protocol (`draft-goswami-agentic-jwt-00`)
- **Vector DB RBAC research:** HoneyBee (SIGMOD 2026) -- dynamic partitioning framework for RBAC in vector databases; Milvus native RBAC with fine-grained collection/partition-level permissions
- **KV-cache isolation:** vLLM cache salting (`cache_salt` parameter, merged May 2025) for per-tenant prefix isolation; SafeKV (arxiv 2508.08438, Feb 2026) selective sharing with ChunkGuard real-time sensitivity detection; KV-Cloak (arxiv 2508.09442) reversible matrix obfuscation for plaintext cache protection (~5% overhead)
- **API gateway security:** API7.ai (RBAC with OPA integration), Palo Alto Prisma for AI API security

### Implementation Maturity (updated 2026-03)

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C5.1 Identity Management & Authentication | High | OIDC/SAML and MFA are mature; OIDC-A proposal and NIST NCCoE guidance advancing agent-specific identity; SPIFFE maturing for workload identity. 93% of AI agent projects still use unscoped API keys despite available alternatives. |
| C5.2 Authorization & Policy | Medium-High | OPA (CNCF graduated) and Cedar (CNCF Sandbox Jan 2026) are production-ready; OpenID AuthZEN enables fine-grained context-aware policies; Permit.io extends policy engines to AI agent use cases. AI-specific policy patterns (tool-scoped, RAG-aware) still emerging. |
| C5.3 Query-Time Security Enforcement | Medium-High | SQL RLS is mature; vector database access control has significantly improved -- Pinecone namespaces (100K), Weaviate tenant isolation, and Qdrant all now support document-level filtering and role-based retrieval natively. Application-layer enforcement still needed for complex cross-collection queries. |
| C5.4 Output Filtering & Data Loss Prevention | Medium | PII detection tools exist but false-negative rates remain high for AI-generated content. The PerplexedBrowser vulnerability family (Mar 2026) revealed that agentic browsers can exfiltrate data through authorized channels, bypassing traditional output filters entirely. |
| C5.5 Multi-Tenant Isolation | Medium-High | Network and storage isolation is mature; Pinecone/Weaviate namespace isolation is production-ready. **[2026-03]** KV-cache isolation is advancing rapidly: vLLM cache salting (merged May 2025) provides per-tenant prefix isolation; SafeKV (Feb 2026) offers selective sharing with 94-97% side-channel mitigation; KV-Cloak adds content-level obfuscation. GPU memory isolation beyond KV-cache remains a gap. |
| C5.6 Autonomous Agent Authorization | Medium | Significant advances: Grantex (scoped JWT, per-agent DIDs, delegation chains), ARIA framework, OAuth on-behalf-of for agents, NIST NCCoE initiative, OWASP Top 10 for Agentic Applications (2026), Auth0 Token Vault (GA), IETF agent delegation drafts. CVE-2026-25253 (OpenClaw, 17,500+ exposed gateways) and the PerplexedBrowser zero-click exploit demonstrate real-world impact. 88% of organizations reported AI agent security incidents. Still nascent for continuous per-action authorization at scale. |

---

## Open Research Questions

- [ ] How should authorization policies account for the non-deterministic nature of AI outputs?
- [ ] What's the right model for agent identity in multi-agent orchestration? **[2026-03]** OIDC-A, ARIA, and NIST NCCoE are actively working on this; NIST listening sessions scheduled Apr 2026.
- [x] How do you enforce query-time access control in vector databases that lack native RBAC? **[2026-03]** Partially resolved: Pinecone, Weaviate, and Qdrant now offer native document-level filtering and tenant-isolated namespaces. Complex cross-collection queries still need application-layer enforcement.
- [ ] Should AI systems have their own identity distinct from the calling user? **[2026-03]** NIST's concept paper and ISACA's ARIA framework both point toward yes -- agents need enterprise-grade identities, not just inherited API keys or service accounts.
- [ ] How can GPU memory isolation be enforced between tenants sharing inference hardware? **[2026-03]** KV-cache specifically is being addressed: vLLM cache salting, SafeKV selective sharing, and KV-Cloak obfuscation each tackle different threat vectors. Broader GPU memory isolation (activations, gradient residuals) remains unsolved.
- [ ] What are effective strategies for propagating data classification labels through embedding transformations?
- [ ] **[2026-03]** How should delegation chains be modeled for multi-hop agent-to-agent authorization with scope narrowing and cascade revocation?
- [ ] **[2026-03]** What is the appropriate trust model for peer-to-peer agent trust establishment across organizational boundaries?
- [ ] **[2026-03]** How can continuous per-action authorization scale to agents executing hundreds of actions per session without creating latency bottlenecks?
- [ ] **[2026-03]** How should organizations handle the "agentic authorization bypass" pattern where shared agents evaluated against agent identity (not requester identity) enable indirect privilege escalation?
- [ ] **[2026-03]** What is the right architecture for output filtering when agentic browsers can exfiltrate data through their own authorized channels, bypassing traditional DLP controls?

---

## Related Standards & Cross-References

- [NIST SP 800-162: Guide to ABAC](https://csrc.nist.gov/pubs/sp/800/162/final)
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
- [NIST IR 8360: ML for Access Control Policy Verification](https://csrc.nist.gov/pubs/ir/8360/final)
- [NIST NCCoE: Accelerating Adoption of Software and AI Agent Identity and Authorization (Feb 2026)](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)
- [NIST AI Agent Standards Initiative (Jan 2026)](https://www.nist.gov/caisi/ai-agent-standards-initiative)
- [OWASP Top 10 for LLM Applications: Excessive Agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [ISACA: The Looming Authorization Crisis for Agentic AI (2025)](https://www.isaca.org/resources/news-and-trends/industry-news/2025/the-looming-authorization-crisis-why-traditional-iam-fails-agentic-ai)
- [CSA: API Security in the AI Era (2025)](https://cloudsecurityalliance.org/blog/2025/09/09/api-security-in-the-ai-era)
- [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [IETF draft-oauth-ai-agents-on-behalf-of-user: OAuth 2.0 Extension for AI Agent Delegation](https://datatracker.ietf.org/doc/draft-oauth-ai-agents-on-behalf-of-user/)
- [NDSS 2025: I Know What You Asked -- Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/)

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
