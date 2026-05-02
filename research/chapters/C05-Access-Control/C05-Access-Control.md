# C05: Access Control & Identity for AI Components & Users

> **Source:** [`1.0/en/0x10-C05-Access-Control-and-Identity.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
> **Requirements:** 12 | **Sections:** 6

## Control Objective

Effective access control for AI systems requires robust identity management, context-aware authorization, and runtime enforcement following zero-trust principles. These controls ensure that humans, services, and autonomous agents only interact with models, data, and computational resources within explicitly granted scopes, with continuous verification and audit capabilities.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C5.1 | Authentication | 2 | [C05-01-Identity-Management-Authentication](C05-01-Identity-Management-Authentication.md) |
| C5.2 | AI Resource Authorization & Classification | 4 | [C05-02-Authorization-Policy](C05-02-Authorization-Policy.md) |
| C5.3 | Query-Time Authorization | 1 | [C05-03-Query-Time-Security-Enforcement](C05-03-Query-Time-Security-Enforcement.md) |
| C5.4 | Output Entitlement Enforcement | 2 | [C05-04-Output-Filtering-DLP](C05-04-Output-Filtering-DLP.md) |
| C5.5 | Policy Decision Point Isolation | 2 | [C05-05-Policy-Decision-Point-Isolation](C05-05-Policy-Decision-Point-Isolation.md) |
| C5.6 | Multi-Tenant Isolation | 2 | [C05-06-Multi-Tenant-Isolation](C05-06-Multi-Tenant-Isolation.md) |

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
- **[2026-04]** "Agent God Mode" in AWS Bedrock AgentCore: wildcard IAM permissions in the default starter toolkit enable a compromised agent to exfiltrate container images, access other agents' memories, and invoke any Code Interpreter across the account (Unit 42, Apr 2026)
- **[2026-04]** Authorization outliving intent: credentials remain active an average of 47 days after becoming unnecessary; 51% of organizations lack formal revocation processes for machine secrets (Okta/OWASP NHI7)
- **[2026-04]** Only 1% of organizations have fully adopted JIT privileged access for AI workloads, while 91% rely on always-on standing privileges; 45% apply identical controls to AI agents and human users (CyberArk, Jan 2026)
- **[2026-04]** IETF draft-klrc-aiagent-auth-01 (Mar 2026) formalizes agent authentication using WIMSE/SPIFFE workload identities, short-lived X.509/JWT credentials, and transaction-scoped tokens — co-authored by Ping Identity, AWS, Zscaler, and OpenAI
- **[2026-04]** Microsoft proposes "Authorization Fabric" for AI agents: a runtime PEP/PDP architecture evaluating RBAC + ABAC + approval injection, enforcing tenant isolation before any tool execution (Apr 2026)
- **[2026-04]** Only 21.9% of teams treat AI agents as independent, identity-bearing entities; 45.6% still rely on shared API keys for agent-to-agent authentication (Gravitee / IANS Research 2026)
- **[2026-04]** ZeroID open-source identity platform launched for autonomous agents: implements RFC 8693 token exchange with narrowing delegation chains, OpenID Shared Signals Framework (SSF) for cascade revocation, and per-step attribution across multi-agent workflows (Highflame, Apr 2026)
- **[2026-04]** NVIDIA BlueField-4 Inference Context Memory Storage Platform (ICMSP): hardware-accelerated line-rate encryption of KV-cache flows with DPU-enforced tenant isolation, eliminating host CPU overhead for security operations (CES 2026)
- **[2026-04]** Token pools as inference-native resource abstraction: multi-tenant capacity isolation decomposing inference into token throughput, KV-cache capacity, and request concurrency with priority-aware admission control (arxiv 2603.00356)
- **[2026-04]** Vertex AI "Double Agent" — Unit 42 demonstrated that default Per-Project Service Agent (P4SA) credentials in Google Vertex AI Agent Engine could be extracted by a deployed agent, granting unrestricted read access to all GCS buckets in the customer project and exposing Google-internal Artifact Registry code (Unit 42, Mar 2026)
- **[2026-04]** IETF standardization accelerating: three complementary drafts now address agent authorization — draft-klrc-aiagent-auth (WIMSE/SPIFFE identity), draft-niyikiza-oauth-attenuating-agent-tokens (cryptographic scope attenuation for delegation chains), and draft-aap-oauth-profile (Agent Authorization Profile with task binding, oversight claims, and delegation tracking)
- **[2026-04]** GPU TEE confidential computing reaching production maturity for LLM inference: NVIDIA H100 Confidential Compute shows <5% throughput overhead for typical queries, with AMD SEV-SNP and Intel TDX providing the VM-level isolation layer (arxiv 2409.03992, 2509.18886)
- **[2026-04]** OWASP NHI Top 10 (2025) directly maps to agentic AI identity risks: NHI1 (improper offboarding), NHI2 (secret leakage), NHI5 (overprivileged NHI), and NHI7 (long-lived secrets) all appear as root causes or amplifiers of agentic security failures
- **[2026-04]** CVE-2026-32211: Missing authentication in Microsoft Azure DevOps MCP Server (@azure-devops/mcp) exposes work items, repositories, pipelines, and API keys to unauthenticated attackers — CVSS 9.1, no patch as of Apr 2026; highlights the MCP specification's optional-authentication gap
- **[2026-04]** Moltbook breach (Jan 2026): Supabase RLS misconfiguration exposed 1.5M AI agent API tokens, 35,000 email addresses, and plaintext third-party credentials (including OpenAI API keys) in agent-to-agent private messages — 17,000 humans controlled ~1.5M agents (88:1 ratio), enabling mass impersonation (Wiz)
- **[2026-04]** 80% of IT workers report AI agents performing tasks without authorization; only 14.4% of teams deploying agents have full security approval (Gravitee 2026)
- **[2026-04]** CVE-2025-59528: Flowise AI CustomMCP node RCE (CVSS 10.0) — attacker-controlled configuration data in the MCP node leads to full system compromise, part of a pattern of AI workflow tools deployed without access controls
- **[2026-04]** Colorado AI Act establishes "reasonable care" standard for high-risk AI systems effective June 30, 2026 — widely adopted identity and authorization standards (WIMSE/SPIFFE, OAuth agent profiles) become evidence of compliance in court
- **[2026-04]** Nutanix Agentic AI multi-tenancy framework (.NEXT 2026): per-tenant GPU resource allocation, tenant-specific security/networking policies, and independent AI environments with dynamic isolation across GPU-aaS, K8s-aaS, VectorDB-aaS, and Models-aaS
- **[2026-04]** Amazon Bedrock AgentCore integrates Cedar policy engine for fine-grained agent authorization: model AI tools, RAG datasets, and operations as Cedar resources/actions with static analysis to understand policy changes before deployment
- **[2026-04]** Microsoft Agent Governance Toolkit (open-source, Apr 2 2026): seven-package runtime security framework with sub-millisecond policy enforcement (<0.1ms p99), supporting OPA Rego, Cedar, and YAML policy languages; addresses all 10 OWASP agentic AI risks; integrates LangChain, AutoGen, CrewAI, and Azure AI Foundry — first multi-engine policy framework purpose-built for autonomous agents
- **[2026-04]** CVE-2025-59536 (CVSS 8.7) and CVE-2026-21852 (CVSS 5.3): Claude Code configuration injection via repository-controlled `.claude/settings.json` enables MCP consent bypass and silent RCE on developer endpoints — `enableAllProjectMcpServers` auto-approves all MCP servers without user confirmation (Check Point Research, patched Sep 2025)
- **[2026-04]** Flowise CVE-2025-59528 under active exploitation: attack traffic targeting 12,000+ internet-exposed instances; third Flowise RCE in the wild after CVE-2025-8943 (CVSS 9.8) and CVE-2025-26319 (CVSS 8.9) — a pattern of AI workflow tools deployed without access controls
- **[2026-04]** Shadow AI breach cost premium: IBM 2025 Cost of a Data Breach reports shadow AI incidents average $4.63M per breach — $670K more than standard breaches; Bessemer Venture Partners names AI agent security "the defining cybersecurity challenge of 2026"
- **[2026-04]** NIST NCCoE AI Agent Identity Project listening sessions began April 2026: sector-specific workshops (healthcare, finance, education) collecting concrete implementation barriers and success factors; comment period on concept paper closed Apr 2

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
| Jan 2026 | CyberArk: Only 1% of Orgs Fully Adopted JIT Privileged Access | 500-person survey: 91% always-on privileges, 45% same controls for AI agents and humans, 33% lack AI access policies (5.2.9, 5.2.10) | [CyberArk](https://www.cyberark.com/press/new-study-only-1-of-organizations-have-fully-adopted-just-in-time-privileged-access-as-ai-driven-identities-rapidly-increase/) |
| Mar 2026 | IETF draft-klrc-aiagent-auth-01: AI Agent Authentication and Authorization | Composes WIMSE/SPIFFE, short-lived X.509/JWT, transaction tokens for agent auth; co-authored by Ping Identity, AWS, Zscaler, OpenAI (5.1.3, 5.6.1) | [IETF](https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/) |
| Apr 2026 | Unit 42: "Agent God Mode" in AWS Bedrock AgentCore | Wildcard IAM in starter toolkit enables cross-agent privilege escalation, memory exfiltration, Code Interpreter hijacking across entire AWS accounts (5.2.1, 5.2.9, 5.6.2) | [Unit 42](https://unit42.paloaltonetworks.com/exploit-of-aws-agentcore-iam-god-mode/) |
| Apr 2026 | Microsoft: Authorization and Governance for AI Agents | Proposes Authorization Fabric with PEP/PDP, RBAC+ABAC+approval injection, deterministic evaluation sequence for runtime agent authorization (5.2.6, 5.2.7, 5.6.4) | [Microsoft](https://techcommunity.microsoft.com/blog/microsoft-security-blog/authorization-and-governance-for-ai-agents-runtime-authorization-beyond-identity/4509161) |
| Apr 2026 | NIST NCCoE AI Agent Identity Project — listening sessions begin | Sector-specific workshops (healthcare, finance, education) on AI agent identity barriers; concept paper comment period closed Apr 2 (5.1.3, 5.6.1) | [NIST NCCoE](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization) |
| Apr 2026 | ZeroID: open-source identity platform for autonomous AI agents | RFC 8693 delegation chains with narrowing permissions, OpenID SSF/CAEP cascade revocation, per-step attribution; SDKs for Python/TypeScript/Rust; integrates LangGraph, CrewAI, Strands (5.1.3, 5.6.1, 5.6.3) | [Help Net Security](https://www.helpnetsecurity.com/2026/04/13/zeroid-open-source-identity-platform-autonomous-ai-agents/) |
| Mar 2026 | OpenID Foundation AIIM response to NIST RFI on AI agent security | Calls for "trust fabric" beneath technical controls — automatic credential verification, constrained agent capabilities, traceable accountability chains; identifies standards fragmentation risk (5.1.3, 5.6.1) | [OIDF](https://openid.net/oidf-responds-to-nist-on-ai-agent-security/) |
| Mar 2026 | Microsoft Zero Trust for AI (ZT4AI) framework | 700 security controls across 116 groups; ZT reference architecture for agentic systems; extends verify-explicitly/least-privilege/assume-breach to AI agents (5.2.1, 5.6.2, 5.6.4) | [Microsoft](https://www.microsoft.com/en-us/security/blog/2026/03/19/new-tools-and-guidance-announcing-zero-trust-for-ai/) |
| Jan 2026 | NVIDIA BlueField-4 ICMSP announced (CES 2026) | Hardware-accelerated line-rate encryption for KV-cache flows; DPU-enforced tenant isolation without host CPU overhead; DOCA Memos treats context cache as first-class resource (5.5.5) | [NVIDIA](https://developer.nvidia.com/blog/introducing-nvidia-bluefield-4-powered-inference-context-memory-storage-platform-for-the-next-frontier-of-ai/) |
| Mar 2026 | Token Pools: multi-tenant inference capacity isolation | Decomposes inference into token throughput, KV-cache capacity, and concurrency; priority-aware admission control maintained sub-1.2s P99 TTFT for guaranteed workloads under contention (5.5.3, 5.5.5) | [arXiv](https://arxiv.org/html/2603.00356) |
| Mar 2026 | Unit 42: "Double Agent" in Google Vertex AI Agent Engine | Default P4SA service agent credentials extractable by deployed agents; unrestricted GCS bucket read access and Artifact Registry exposure across customer projects (5.1.1, 5.2.1, 5.6.2) | [Unit 42](https://unit42.paloaltonetworks.com/double-agents-vertex-ai/) |
| Mar 2026 | IETF draft-niyikiza-oauth-attenuating-agent-tokens-00 | Attenuating Authorization Tokens (AATs): JWT-based credentials with cryptographic scope attenuation — any holder can derive narrower tokens offline without contacting the authorization server; six mathematically-enforced delegation invariants (5.6.1, 5.6.3) | [IETF](https://datatracker.ietf.org/doc/html/draft-niyikiza-oauth-attenuating-agent-tokens-00) |
| Feb 2026 | IETF draft-aap-oauth-profile-00: Agent Authorization Profile | Extends OAuth 2.0 with agent-specific JWT claims: task binding (`aap_task`), capability constraints with rate limits and domain allowlists (`aap_capabilities`), human oversight signals (`aap_oversight`), and delegation chain tracking (`aap_delegation`) (5.2.6, 5.6.1, 5.6.4) | [IETF](https://www.ietf.org/archive/id/draft-aap-oauth-profile-00.html) |
| 2025 | OWASP Non-Human Identities Top 10 | NHI1 (improper offboarding), NHI2 (secret leakage), NHI5 (overprivileged NHI), NHI7 (long-lived secrets) directly map to agentic AI identity failure modes; cross-referenced by OWASP Agentic Top 10 (5.1.1, 5.2.9, 5.6.1) | [OWASP](https://owasp.org/www-project-non-human-identities-top-10/) |
| 2026 | Confidential LLM Inference: Performance and Cost Across CPU and GPU TEEs | NVIDIA H100 CC shows <5% overhead for typical LLM queries; AMD SEV-SNP and Intel TDX provide VM-level isolation; production deployments now available on OpenRouter (5.5.4, 5.5.5) | [arXiv](https://www.arxiv.org/pdf/2509.18886) |
| Apr 2026 | CVE-2026-32211: Azure DevOps MCP Server missing authentication (CVSS 9.1) | @azure-devops/mcp npm package exposes work items, repos, pipelines, API keys without auth; MCP specification makes authentication optional, leaving enforcement to implementors (5.1.1, 5.2.1) | [DEV Community](https://dev.to/michael_onyekwere/cve-2026-32211-what-the-azure-mcp-server-flaw-means-for-your-agent-security-14db) |
| Jan 2026 | Moltbook breach: 1.5M AI agent API tokens exposed (Wiz) | Supabase RLS misconfiguration exposed agent credentials, 35K emails, plaintext third-party API keys in agent DMs; 17K humans controlled 1.5M agents (88:1); mass impersonation possible (5.1.1, 5.5.2, 5.5.3) | [Wiz](https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys) |
| 2026 | CVE-2025-59528: Flowise AI CustomMCP node RCE (CVSS 10.0) | Attacker-controlled config data in MCP node yields full system compromise; pattern of AI workflow tools deployed without access controls (5.2.1, 5.6.2) | [Security Online](https://securityonline.info/vulnerability-digest-april-2026-ai-security-gaps/) |
| Apr 2026 | Nutanix Agentic AI multi-tenancy framework (.NEXT 2026) | Per-tenant GPU allocation, tenant-specific security policies, independent AI environments across GPU-aaS, K8s-aaS, VectorDB-aaS (5.5.1, 5.5.3) | [Nutanix](https://www.nutanix.com/press-releases/2026/nutanix-to-extend-nutanix-agentic-ai-empowering-neoclouds-to-deliver-higher-value-ai-services) |
| Mar 2026 | Amazon Bedrock AgentCore + Cedar for agent authorization | Cedar policy engine integrated for fine-grained AI agent access control with static analysis of policy changes before deployment (5.2.6, 5.6.4) | [Medium](https://medium.com/@tolghn/amazon-bedrock-agentcore-policy-cedar-control-what-your-ai-agents-can-do-3313e6f3a2db) |
| Apr 2026 | Microsoft Agent Governance Toolkit (open-source) | Seven-package runtime security framework: sub-millisecond policy enforcement, OPA Rego + Cedar + YAML, addresses all 10 OWASP agentic AI risks; integrates LangChain, AutoGen, CrewAI (5.2.6, 5.6.4) | [Microsoft Open Source](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/) |
| Feb 2026 | CVE-2025-59536 / CVE-2026-21852: Claude Code config injection + MCP consent bypass | Repository-controlled `.claude/settings.json` enables silent RCE and API key exfiltration; `enableAllProjectMcpServers` bypasses user approval for MCP servers (5.1.1, 5.2.1) | [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) |
| Apr 2026 | Flowise CVE-2025-59528 under active exploitation (12,000+ instances) | Third Flowise RCE in the wild; CustomMCP node executes attacker JavaScript with full Node.js runtime privileges; attack traffic from single Starlink IP (5.2.1, 5.6.2) | [The Hacker News](https://thehackernews.com/2026/04/flowise-ai-agent-builder-under-active.html) |
| 2026 | Bessemer VP: AI agent security as defining challenge of 2026 | Shadow AI breaches average $4.63M (IBM); 48% of security professionals cite agentic AI as top attack vector; 1 in 8 AI breaches now involve autonomous agents (5.6.1, 5.6.2) | [Bessemer VP](https://www.bvp.com/atlas/securing-ai-agents-the-defining-cybersecurity-challenge-of-2026) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Policy engines:** OPA (Open Policy Agent, CNCF graduated), Cedar (AWS, CNCF Sandbox since Jan 2026; integrated into Amazon Bedrock AgentCore for agent-level policy with static analysis), Casbin, OpenID AuthZEN, Permit.io (fine-grained RBAC/ABAC/ReBAC across apps, APIs, data layers, AI agents; powers OPA/Cedar-style policies via OPAL)
- **Policy administration:** OPAL (Open Policy Administration Layer) for keeping policies consistent across microservices and AI agents
- **Identity:** SPIFFE/SPIRE for workload identity, OAuth 2.0 for user-facing AI apps, OIDC-A (OpenID Connect for Agents) 1.0 proposal, ARIA (Agent Relationship-Based Identity and Authorization), Microsoft OAuth 2.0 on-behalf-of token exchange for agent delegation
- **Agent credential management:** Grantex (scoped JWT grant tokens, per-agent DIDs, delegation chains), ScaleKit (delegated agent access with on-behalf-of auth), Nango (secure AI agent API authentication), Auth0 Token Vault (GA Jan 2026; RFC 8693 token exchange with 30+ pre-integrated providers, per-user credential isolation), HashiCorp Vault (dynamic secrets for AI agent identity), ZeroID (open-source, Apr 2026; RFC 8693 delegation chains with automatic permission narrowing, OpenID SSF/CAEP cascade revocation, LangGraph/CrewAI/Strands integrations)
- **DLP:** Google DLP API, Microsoft Purview, Presidio, custom regex/NER-based PII filters
- **Multi-tenant isolation:** Kubernetes namespaces, Calico/Cilium network policies, database row-level security, Pinecone namespaces (up to 100K per index), Weaviate tenant-isolated collections, Nutanix Agentic AI multi-tenancy framework (Apr 2026; per-tenant GPU allocation, tenant-specific security/networking policies across GPU-aaS, K8s-aaS, VectorDB-aaS, Models-aaS), Blaxel (microVM architecture with hardware-enforced tenant boundaries, sub-25ms resume, SOC 2 Type II / HIPAA / ISO 27001 compliant)
- **Vector DB access control:** Pinecone (document-level filtering, role-based retrieval, SOC 2/HIPAA/ISO 27001), Weaviate (tenant isolation, collection-level access), Qdrant (managed multi-tenant support)
- **Agent authorization:** LangChain tool permissions, OpenAI function calling constraints, Anthropic tool use scoping, Model Context Protocol (MCP) for authorization context negotiation, IETF `draft-oauth-ai-agents-on-behalf-of-user` (OAuth 2.0 agent delegation), IETF Secure Intent Protocol (`draft-goswami-agentic-jwt-00`), IETF `draft-klrc-aiagent-auth-01` (WIMSE/SPIFFE-based agent auth, Mar 2026), IETF `draft-niyikiza-oauth-attenuating-agent-tokens-00` (AATs — cryptographic scope attenuation for delegation chains, Mar 2026), IETF `draft-aap-oauth-profile-00` (Agent Authorization Profile — task binding, capability constraints, oversight claims, Feb 2026)
- **Runtime authorization fabric:** Microsoft Authorization Fabric (PEP/PDP with RBAC+ABAC+approval injection, Apr 2026), Entra Agent Identity for workload identity governance, Microsoft Agent Governance Toolkit (open-source, Apr 2026; seven-package runtime security with Agent OS sub-millisecond policy engine, Agent Mesh cryptographic identity via DIDs, and Agent Runtime execution rings with emergency kill switches; supports OPA Rego + Cedar + YAML policies)
- **Vector DB RBAC research:** HoneyBee (SIGMOD 2026) -- dynamic partitioning framework for RBAC in vector databases; Milvus native RBAC with fine-grained collection/partition-level permissions
- **KV-cache isolation:** vLLM cache salting (`cache_salt` parameter, merged May 2025) for per-tenant prefix isolation; SafeKV (arxiv 2508.08438, Feb 2026) selective sharing with ChunkGuard real-time sensitivity detection; KV-Cloak (arxiv 2508.09442) reversible matrix obfuscation for plaintext cache protection (~5% overhead); NVIDIA BlueField-4 ICMSP (CES 2026) for hardware-accelerated line-rate encryption and DPU-enforced tenant isolation of KV-cache flows
- **GPU TEE confidential computing:** NVIDIA H100 Confidential Compute (<5% throughput overhead for typical LLM inference), AMD SEV-SNP and Intel TDX for VM-level isolation; production deployments available on OpenRouter via Phala Network; provides hardware-enforced tenant isolation for the entire inference pipeline, not just KV-cache
- **Multi-tenant inference isolation:** Token Pools (arxiv 2603.00356) — inference-native capacity isolation decomposing resources into token throughput, KV-cache capacity, and request concurrency with 5-tier priority hierarchy and admission control at API gateway level
- **API gateway security:** API7.ai (RBAC with OPA integration), Palo Alto Prisma for AI API security

### Implementation Maturity (updated 2026-04-16)

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C5.1 Authentication | High | OIDC/SAML and MFA are mature for human users; step-up auth for high-risk AI operations is well understood. Signed JWT assertions for agent-to-system federation are advancing (IETF draft-klrc-aiagent-auth, OIDC-A proposal, NIST NCCoE listening sessions). Still, only 21.9% of teams treat agents as identity-bearing entities (IANS 2026). |
| C5.2 AI Resource Authorization & Classification | Medium-High | OPA and Cedar production-ready; Cedar now integrated into Amazon Bedrock AgentCore for agent-level policy with static analysis. Microsoft's Agent Governance Toolkit (Apr 2026) provides open-source multi-engine policy enforcement (OPA Rego + Cedar + YAML) with sub-millisecond latency. JIT adoption remains low — only 1% of orgs have fully adopted JIT privileged access (CyberArk). Classification taxonomies covering AI-specific asset types (embeddings, model weights, prompt templates, RAG assemblies, fine-tuning datasets, agent tool schemas) are still largely custom extensions to existing DLP taxonomies. CVE-2025-59528 now under active exploitation across 12,000+ Flowise instances (Apr 2026). |
| C5.3 Query-Time Authorization | Medium-High | SQL RLS is mature; vector database access control has significantly improved — Pinecone namespaces (100K), Weaviate tenant isolation, and Qdrant all now support document-level filtering and role-based retrieval natively. Application-layer enforcement still needed for complex cross-collection queries. |
| C5.4 Output Entitlement Enforcement | Medium | PII detection tools exist but false-negative rates remain high for AI-generated content. Citation-level entitlement validation is still largely custom work — most RAG frameworks (LlamaIndex, LangChain) do not natively enforce citation-level access control. The PerplexedBrowser vulnerability family (Mar 2026) revealed that agentic browsers can exfiltrate data through authorized channels, bypassing traditional output filters entirely. |
| C5.5 Policy Decision Point Isolation | Low-Medium | Emerging area. Most production agent frameworks still evaluate policy inline with agent execution, leaving the PDP reachable from a compromised agent runtime. Out-of-process policy enforcement patterns (OPA sidecar, remote Cedar evaluator, AgentCore Policy gateway) provide the reference architecture, but adoption for agent workloads lags the equivalent service-mesh pattern for microservices. |
| C5.6 Multi-Tenant Isolation | Medium-High | Network and storage isolation is mature; Pinecone/Weaviate namespace isolation is production-ready. Nutanix Agentic AI (Apr 2026) adds per-tenant GPU allocation with dynamic isolation across GPU-aaS, K8s-aaS, VectorDB-aaS. KV-cache isolation advancing on multiple fronts: vLLM cache salting (May 2025), SafeKV selective sharing (94-97% side-channel mitigation), and NVIDIA BlueField-4 ICMSP (CES 2026) for DPU-enforced tenant isolation. GPU TEE confidential computing (NVIDIA H100 CC, AMD SEV-SNP, Intel TDX) now production-ready with <5% overhead. The Moltbook breach (Jan 2026) exposed 1.5M agent tokens via missing RLS — a cautionary example of multi-tenant isolation failure at the application layer. |

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
- [ ] **[2026-04]** How can organizations enforce JIT privileged access for AI workloads when only 1% have fully adopted it and 91% still rely on always-on standing privileges?
- [ ] **[2026-04]** What is the right data classification taxonomy for AI-specific assets (embeddings, model weights, prompt templates, RAG assemblies, fine-tuning datasets, agent tool schemas) — and how should classification labels propagate through embedding transformations?
- [ ] **[2026-04]** How should authorization policy expiration be enforced for AI agent tool access as available tools and capabilities change, without causing operational disruption from premature revocation?
- [ ] **[2026-04]** Can hardware-accelerated KV-cache isolation (e.g., NVIDIA BlueField-4 ICMSP) provide sufficient tenant separation to eliminate software-level side-channel mitigations, or do both layers remain necessary?
- [ ] **[2026-04]** How should inference capacity isolation (token pools, priority-aware admission control) interact with authorization policy to prevent resource-level denial of service across tenants sharing GPU infrastructure?
- [ ] **[2026-04]** How should the MCP specification address its optional-authentication gap, given that CVE-2026-32211 (CVSS 9.1) and CVE-2025-59528 (CVSS 10.0) both stem from MCP servers shipping without authentication?
- [ ] **[2026-04]** What is the appropriate "reasonable care" standard for AI agent identity and authorization under the Colorado AI Act (effective June 2026), and how should organizations demonstrate compliance through adopted standards?
- [ ] **[2026-04]** How should AI-native social platforms secure agent-to-agent credentials, given the Moltbook breach demonstrated that plaintext credential exchange in agent DMs creates cascading exposure across interconnected services?
- [ ] **[2026-04]** How should multi-engine policy frameworks (e.g., Microsoft Agent Governance Toolkit supporting OPA + Cedar + YAML simultaneously) handle policy conflict resolution when overlapping rules from different engines produce contradictory authorization decisions for the same agent action?

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
- [IETF draft-klrc-aiagent-auth-01: AI Agent Authentication and Authorization (Mar 2026)](https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/)
- [Microsoft: Authorization and Governance for AI Agents (Apr 2026)](https://techcommunity.microsoft.com/blog/microsoft-security-blog/authorization-and-governance-for-ai-agents-runtime-authorization-beyond-identity/4509161)
- [Unit 42: Cracks in the Bedrock — Agent God Mode (Apr 2026)](https://unit42.paloaltonetworks.com/exploit-of-aws-agentcore-iam-god-mode/)
- [CyberArk: JIT Privileged Access and AI Identities Study (Jan 2026)](https://www.cyberark.com/press/new-study-only-1-of-organizations-have-fully-adopted-just-in-time-privileged-access-as-ai-driven-identities-rapidly-increase/)
- [EU AI Act Article 14: Human Oversight (enforcement Aug 2026)](https://artificialintelligenceact.eu/article/14/)
- [OpenID Foundation: AIIM Response to NIST on AI Agent Security (Mar 2026)](https://openid.net/oidf-responds-to-nist-on-ai-agent-security/)
- [Microsoft: Zero Trust for AI — Tools and Guidance (Mar 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/19/new-tools-and-guidance-announcing-zero-trust-for-ai/)
- [OpenID Foundation: Identity Management for Agentic AI Whitepaper (Oct 2025)](https://openid.net/new-whitepaper-tackles-ai-agent-identity-challenges/)
- [Token Pools: Token Management in Multi-Tenant AI Inference Platforms (2026)](https://arxiv.org/html/2603.00356)
- [OWASP Non-Human Identities Top 10 (2025)](https://owasp.org/www-project-non-human-identities-top-10/)
- [IETF draft-niyikiza-oauth-attenuating-agent-tokens-00: Attenuating Authorization Tokens for AI Agents (Mar 2026)](https://datatracker.ietf.org/doc/html/draft-niyikiza-oauth-attenuating-agent-tokens-00)
- [IETF draft-aap-oauth-profile-00: Agent Authorization Profile for OAuth 2.0 (Feb 2026)](https://www.ietf.org/archive/id/draft-aap-oauth-profile-00.html)
- [Unit 42: Double Agents — Exposing Security Blind Spots in GCP Vertex AI (Mar 2026)](https://unit42.paloaltonetworks.com/double-agents-vertex-ai/)
- [Confidential LLM Inference: Performance and Cost Across CPU and GPU TEEs (2026)](https://www.arxiv.org/pdf/2509.18886)
- [CVE-2026-32211: Azure DevOps MCP Server Missing Authentication (CVSS 9.1, Apr 2026)](https://dev.to/michael_onyekwere/cve-2026-32211-what-the-azure-mcp-server-flaw-means-for-your-agent-security-14db)
- [Wiz: Hacking Moltbook — Exposed Database Reveals 1.5M API Keys (Jan 2026)](https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys)
- [Amazon Bedrock AgentCore + Cedar Policy Engine for Agent Authorization (Mar 2026)](https://medium.com/@tolghn/amazon-bedrock-agentcore-policy-cedar-control-what-your-ai-agents-can-do-3313e6f3a2db)
- [Nutanix Agentic AI Multi-Tenancy Framework (.NEXT 2026)](https://www.nutanix.com/press-releases/2026/nutanix-to-extend-nutanix-agentic-ai-empowering-neoclouds-to-deliver-higher-value-ai-services)
- [Colorado AI Act: Reasonable Care Standard for High-Risk AI Systems (effective June 2026)](https://www.rockcybermusings.com/p/i-agent-authentication-authorization-gap)
- [Microsoft Agent Governance Toolkit: Open-Source Runtime Security for AI Agents (Apr 2026)](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/)
- [Check Point Research: RCE and API Token Exfiltration Through Claude Code Project Files — CVE-2025-59536, CVE-2026-21852](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [Bessemer Venture Partners: Securing AI Agents — The Defining Cybersecurity Challenge of 2026](https://www.bvp.com/atlas/securing-ai-agents-the-defining-cybersecurity-challenge-of-2026)
- [CSA Research Note: Flowise MCP RCE Active Exploitation (Apr 2026)](https://labs.cloudsecurityalliance.org/research/csa-research-note-flowise-mcp-rce-exploitation-20260409-csa/)

---

## Related Pages

- [C05-05: Policy Decision Point Isolation](C05-05-Policy-Decision-Point-Isolation.md) — Runtime isolation of the agent PDP from the agent runtime it governs, complementing the agent-specific authorization controls in C9.6.
- [C05-06: Multi-Tenant Isolation](C05-06-Multi-Tenant-Isolation.md) — KV-cache partitioning, shared model state isolation, and tenant-specific inference infrastructure isolation.
- [C09-06: Authorization & Delegation](../C09-Orchestration-and-Agents/C09-06-Authorization-and-Delegation.md) — Agent authorization with delegation context propagation, credential isolation, and IETF transaction tokens — the orchestration-layer counterpart to the authentication patterns here.
- [C05-03: Query-Time Authorization](C05-03-Query-Time-Security-Enforcement.md) — Mandatory security filters, fail-closed query behavior, RLS, and field masking for vector DB and RAG query pipelines — the data-access enforcement layer beneath the policies defined here.
- [C05-02: AI Resource Authorization & Classification](C05-02-Authorization-Policy.md) — RBAC/ABAC enforcement for AI resources, externalized policy engines (OPA, Cedar, AgentCore), JIT privileged access, and the AI-specific classification taxonomy that underpins query-time and output enforcement.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
