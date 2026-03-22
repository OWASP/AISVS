# C10.2: Authentication & Authorization

> **Parent:** [C10 MCP Security](C10-MCP-Security.md)
> **Requirements:** 12 | **IDs:** 10.2.1–10.2.12
> **Last Researched:** 2026-03-21

## Purpose

This section ensures that MCP clients and servers authenticate each other properly and that authorization is enforced at every tool invocation. The MCP specification mandates OAuth 2.1 as the authorization framework for HTTP-based transports. The auth spec was **substantially revised on November 25, 2025** to address disclosed vulnerabilities including confused deputy attacks and token pass-through. As of early 2026, **30+ CVEs** were filed against MCP components in just 60 days (January–February 2026), the OWASP MCP Top 10 (v0.1 beta) lists Token Mismanagement (MCP01) and Insufficient Authentication (MCP07) as top risks, and real-world data paints a stark adoption picture: only **8.5%** of MCP servers use OAuth — 53% still rely on static API keys (Astrix Security survey of ~20,000 servers). Trend Micro found **492 MCP servers** exposed on the internet with zero authentication, exposing 1,402 tools.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.2.1** | **Verify that** MCP clients authenticate to MCP servers using the OAuth 2.1 authorization framework and present a valid OAuth access token for each request, and that the MCP server validates the token according to OAuth 2.1 resource server requirements. | 1 | D/V | **Unauthenticated tool invocation.** Without OAuth, any client that can reach the MCP server endpoint can invoke tools. Trend Micro found 492 internet-exposed MCP servers with zero authentication, exposing 1,402 tools — 90%+ offering direct data source access. Operation Bizarre Bazaar (December 2025 – January 2026) saw 60% of attack traffic targeting MCP endpoints, exploiting unauthenticated servers for LLMjacking. SANDWORM_MODE (February 2026) installed rogue MCP servers via 19 typosquatting npm packages into Claude Code, Cursor, and Windsurf, exfiltrating SSH keys, AWS credentials, and NPM tokens. | Inspect MCP server code for OAuth token validation middleware. Attempt tool invocation without a token and verify rejection (HTTP 401). Verify the server checks token signature, expiration, and issuer. Review MCP client code to confirm tokens are attached to every JSON-RPC request. Use Cisco MCP Scanner (open-source, YARA + LLM + API detection engines) to audit server configurations. Check that the server supports Protected Resource Metadata (RFC 9728). | OAuth 2.1 adoption remains critically low — only 8.5% of ~20,000 surveyed MCP servers use OAuth (Astrix Security 2025). 53% rely on static API keys, and 79% pass keys via environment variables. Community MCP servers overwhelmingly operate without authentication. OAuth 2.1 itself is still in draft (draft-ietf-oauth-v2-1-15 as of March 2026, not yet an RFC). MCP gateways (Kong, Traefik Hub, Azure APIM) are emerging as enforcement points for organizations that can't modify every MCP server. |
| **10.2.2** | **Verify that** MCP servers validate OAuth access tokens including issuer, audience, expiration, and scope claims, ensuring that tokens were issued for the specific MCP server before allowing tool invocation. | 1 | D/V | **Token confusion / cross-service token reuse.** The Doyensec "MCP AuthN/Z Nightmare" analysis (March 2026) documented scope namespace collisions where multiple MCP servers using identical scope names (`files:read`, `admin:write`) enable cross-server privilege escalation. Obsidian Security demonstrated one-click account takeover via shared `client_id` exploitation — attacker registers malicious MCP client and intercepts authorization codes because the SaaS provider can't distinguish legitimate from malicious clients. RFC 8707 Resource Indicators are now mandatory in the MCP spec to prevent this. | Verify the MCP server checks `iss`, `aud`, `exp`, and `scope` claims. Present a valid token with incorrect audience and confirm rejection. Test with expired tokens. Verify RFC 8707 resource indicator validation — tokens must include `aud` claim matching the specific MCP server URI. Check that the server responds to unauthorized requests with `WWW-Authenticate` header containing `resource_metadata` URL (RFC 9728). | Standard OAuth 2.1 resource server behavior — well-understood, but easy to misconfigure. Doyensec's analysis showed ID-JAG (JWT Authorization Grant) replay risk where a single grant can mint multiple server access tokens with no single-use enforcement. The upcoming SEP-1932 (DPoP — Demonstration of Proof-of-Possession) would bind tokens to specific client key pairs, preventing token theft/replay. |
| **10.2.3** | **Verify that** MCP servers are registered through a controlled technical onboarding mechanism requiring explicit owner, environment, and resource definitions; unregistered or undiscoverable servers must not be callable in production. | 1 | D/V | **Shadow MCP servers / unauthorized tool exposure.** Bitsight found ~1,000 exposed MCP servers with no authorization. Smithery MCP hosting path traversal (October 2025) leaked Docker credentials and a Fly.io API token controlling 3,000+ apps from an uncontrolled server deployment. SANDWORM_MODE installed rogue MCP servers via supply chain attack without any registration or approval. | Review the organization's MCP server inventory or registry. Attempt to connect an MCP client to an unregistered server in production and verify it fails. Check that server onboarding requires security review, owner assignment, and environment tagging. Use Cisco AI Defense MCP Catalog (announced February 2026) to discover and inventory MCP servers across platforms. SEP-2127 (Server Cards) proposes a standard discovery mechanism. | No standard MCP server registry exists. Cisco AI Defense MCP Catalog and IBM ContextForge are the first products addressing centralized discovery. Enforcement requires network-level controls (service mesh, MCP gateway allowlists) or client-side allowlists. CSA mcpserver-audit provides static analysis scanning with CWE mapping and AIVSS scoring. |
| **10.2.4** | **Verify that** authorization decisions at the MCP layer are enforced by the MCP server's policy logic, and that model-generated output cannot influence, override, or bypass access control checks. | 1 | D/V | **Prompt injection bypassing authorization.** Doyensec documented "agent-driven scope creep" where LLMs autonomously request high-risk scopes without user consent. CoSAI's 12-threat taxonomy (January 2026) identifies T9 (overreliance on LLM judgment for security decisions) as a core threat. The Square MCP OAuth flaw (August–September 2025) showed missing `redirect_uri` restrictions during dynamic client registration enabling one-click account takeover. | Review MCP server authorization code to confirm decisions are based solely on token claims, server-side policy, and user identity — never on content from the model's output or tool arguments that could be model-influenced. Attempt privilege escalation via crafted tool arguments. Test with prompt injection payloads in tool arguments targeting auth logic. | Fundamental architectural requirement: the authorization boundary must be impermeable to model-generated content. Traefik Hub's Task-Based Access Control (TBAC, Early Access March 2026) enforces authorization across three dimensions — Tasks (business objectives), Tools (system access), and Transactions (parameter-level constraints) — without requiring agent or server modifications. This is the most advanced policy model for MCP as of March 2026. |
| **10.2.5** | **Verify that** MCP servers act as OAuth 2.1 resource servers only by validating tokens issued by external authorization servers and by not storing tokens or user credentials. | 2 | D/V | **Token theft from MCP server compromise.** CVE-2025-68145/68143/68144 (Anthropic mcp-server-git, January 2026) chained path traversal + argument injection to achieve full RCE — if the server stored tokens, all would be compromised. Asana's cross-tenant data breach (June 2025) was caused by a logic flaw in access control after launching MCP-powered features. | Review server code and storage for any token or credential persistence. Verify tokens are validated inline (JWT signature check or token introspection) and discarded after the request. Check that no token caching layer exists. | Aligns with OAuth 2.1 resource server best practice. The "God Key" problem (Security Boulevard, March 2026) describes the anti-pattern where agents use broad, long-lived credentials conflating user identity, authorization, and tool access. Solution: Token Exchange (RFC 8693) — agents obtain short-lived, narrowly scoped credentials minted for specific MCP services. |
| **10.2.6** | **Verify that** MCP `tools/list` and resource discovery responses are filtered based on the end-user's authorized scopes so that agents receive only the tool and resource definitions the user is permitted to invoke. | 2 | D/V | **Information disclosure / attack surface enumeration.** MCPTox benchmark found o1-mini: 72.8% ASR when exposed to all tool descriptions; filtering reduces the attack surface visible to the model and limits tool poisoning impact. | Call `tools/list` with tokens of varying scope levels and verify the response only includes authorized tools. Test with a minimal-scope token and confirm restricted tools are absent from the response. Kong MCP Tool ACLs (v3.13, January 2026) implements this as a default-deny YAML-based ACL that filters tool lists before returning them to clients. | Kong MCP Tool ACLs is the first production implementation of filtered tool discovery. The MCP spec does not mandate filtering at the discovery level — only at invocation. This requirement goes beyond the spec. Traefik TBAC adds parameter-level filtering (Transaction authorization) on top of tool-level filtering. |
| **10.2.7** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 | D/V | **Horizontal privilege escalation via argument manipulation.** Supabase Cursor agent incident (mid-2025) — agent ran with privileged service-role access and processed user-supplied SQL in support tickets, exfiltrating integration tokens. No standard framework exists for argument-level authorization in MCP. | Test tool invocations with arguments outside the user's authorized scope (e.g., different tenant IDs, unauthorized file paths). Verify the server rejects based on token claims, not just tool name. Review authorization middleware for argument inspection. Traefik TBAC's Transaction authorization enforces parameter-level constraints. | Argument-level authorization is significantly harder than tool-level. Requires the server to understand argument semantics. No standard framework exists — AuthZed/SpiceDB and OPA/Rego do not yet have production MCP integrations (SpiceDB ships an MCP server for development, but not as a policy engine for MCP tool authorization). This is a gap. |
| **10.2.8** | **Verify that** MCP session identifiers are treated as state, not identity: generated using cryptographically secure random values, bound to the authenticated user, and never relied on for authentication or authorization decisions. | 1 | D/V | **Session hijacking / session confusion.** CVE-2026-25536 (MCP TypeScript SDK, February 2026, CVSS 7.1) — `StreamableHTTPServerTransport` reused transport across multiple clients, leaking responses across client boundaries. GHSA-9f65-56v6-gxw7 (Claude Code IDE extension) — WebSocket authentication bypass on localhost. | Review session ID generation for CSPRNG. Verify every request is authenticated via OAuth token regardless of session state. Attempt to use a valid session ID with a different user's token and confirm the server uses the token's identity. Test for the cross-client leak pattern from CVE-2026-25536. | The MCP spec defines `Mcp-Session-Id` for transport-level state. The TypeScript SDK cross-client leak shows how subtle session management bugs create cross-tenant data exposure. |
| **10.2.9** | **Verify that** MCP servers do not pass through access tokens received from clients to downstream APIs and instead obtain a separate token scoped to the server's own identity (e.g., via on-behalf-of or client credentials flow). | 2 | D/V | **Token relay / over-privileged downstream access.** The MCP spec (November 2025 revision) explicitly forbids token pass-through. The "God Key" problem describes the anti-pattern where a single shared credential grants access to all tools and downstream APIs. Token Exchange (RFC 8693) is the recommended pattern for multi-agent delegation chains — agents obtain short-lived, narrowly scoped credentials while maintaining user attribution via dual identity headers. | Review MCP server code for downstream API calls. Check whether the user's token is forwarded or whether a separate token is obtained. Verify downstream tokens have reduced scope. Azure APIM MCP Gateway natively supports On-Behalf-Of (OBO) token exchange with Entra ID. | OBO flow support varies by identity provider. Azure AD supports OBO natively. Okta's Cross App Access (XAA) protocol has been incorporated as the MCP "Enterprise-Managed Authorization" extension — the enterprise IdP verifies agent authorization against centralized policies. Okta for AI Agents GA is April 30, 2026. |
| **10.2.10** | **Verify that** MCP servers acting as OAuth proxies to third-party APIs enforce per-client consent before forwarding authorization requests, preventing cached approvals from being reused across dynamically registered clients. | 2 | D/V | **Consent bypass via dynamic client registration.** Obsidian Security demonstrated one-click account takeover against Square MCP via shared `client_id`. Only 4% of MCP authorization server endpoints support Dynamic Client Registration; fewer than 4% support CIMD (Client ID Metadata Documents). | Register a new MCP client dynamically and verify it cannot access tokens previously approved for a different client. Verify the consent UI identifies the requesting client. Review consent storage for per-client isolation. | The MCP spec introduced CIMD (SEP-991) as the preferred registration mechanism but adoption is ~3-4%. Dynamic Client Registration (RFC 7591) remains the backwards-compat fallback. |
| **10.2.11** | **Verify that** MCP clients request only the minimum scopes needed for the current operation, elevate progressively via step-up authorization, and that servers reject wildcard or overly broad scopes. | 2 | D/V | **Over-scoped tokens enabling lateral movement.** 67% of enterprise teams still rely on static, broadly-scoped credentials for AI systems (Teleport 2026 survey). Over-privileged AI systems experience 4.5x higher incident rates. GitGuardian analysis (March 2026) notes OAuth scopes authorize access to the MCP server, not individual tools — creating a tool-level authorization gap. | Review MCP client OAuth configuration for requested scopes. Verify scopes are minimal. Test requesting a wildcard scope and confirm rejection. Verify high-privilege operations trigger step-up authorization. | The MCP spec does not define standard scope names or a scope hierarchy. Scope naming is left to individual implementations, making cross-server least-privilege difficult. The emerging enterprise pattern is mTLS at transport layer + OAuth 2.1 at authorization layer + RFC 8707 for token scoping + RFC 8693 for delegation chains. |
| **10.2.12** | **Verify that** MCP servers enforce deterministic session teardown, destroying cached tokens, in-memory state, temporary storage, and file handles when a session terminates, disconnects, or times out. | 2 | D/V | **Stale session exploitation / resource leakage.** CVE-2025-53109/53110 (Anthropic Filesystem MCP Server, August 2025) — sandbox escape + symlink bypass enabled arbitrary file access, potentially via stale file handles from improperly torn-down sessions. | Terminate an MCP session and verify: (1) cached tokens are invalidated, (2) temporary files are deleted, (3) file handles are closed, (4) the session ID is rejected on subsequent requests. Test with abrupt disconnection and verify cleanup via timeout. | The MCP spec defines session lifecycle but does not prescribe cleanup behavior. Implementations must handle both graceful termination (`HTTP DELETE`) and ungraceful disconnection (timeout-based cleanup). |

---

## MCP Auth CVEs and Incidents (2025-2026)

| Date | Incident | CVE | Impact |
|------|----------|-----|--------|
| Apr 2025 | WhatsApp MCP tool poisoning | — | Exfiltration of thousands of messages via backdoored tool descriptions |
| May 2025 | GitHub MCP prompt injection | — | Over-privileged PATs enabled extraction of private repo data |
| Jun 2025 | Anthropic MCP Inspector RCE | CVE-2025-49596 | Unauthenticated RCE on developer machines |
| Jun 2025 | Asana cross-tenant data breach | — | Customer data bled across tenants' MCP instances |
| Jul 2025 | mcp-remote command injection | CVE-2025-6514 | 437K+ downloads affected; Cloudflare, Hugging Face, Auth0 guides referenced vulnerable code |
| Aug 2025 | Anthropic Filesystem MCP Server | CVE-2025-53109, CVE-2025-53110 | Sandbox escape + symlink bypass → arbitrary file access |
| Aug-Sep 2025 | Square MCP Server OAuth flaw | — | Missing `redirect_uri` restrictions → one-click merchant account takeover |
| Sep 2025 | Malicious Postmark MCP package | — | Supply-chain: BCC'd all outgoing emails to attacker |
| Oct 2025 | Smithery MCP path traversal | — | Leaked Docker credentials + Fly.io API token (3,000+ apps) |
| Oct 2025 | Figma/Framelink MCP command injection | CVE-2025-53967 | Unsafe `child_process.exec` with untrusted input |
| Late 2025 | OpenMCP Client DNS rebinding | CVE-2025-58062 | Unauthorized access via localhost assumptions |
| Jan 2026 | Anthropic mcp-server-git RCE chain | CVE-2025-68145/68143/68144 | Path traversal + argument injection → full RCE |
| Jan 2026 | GitHub Kanban MCP RCE | CVE-2026-0756 | Arbitrary command execution via tool interface |
| Feb 2026 | MCPJam Inspector RCE | CVE-2026-23744 (CVSS 9.8) | Bound to 0.0.0.0, no auth → unauthenticated RCE |
| Feb 2026 | MCP TypeScript SDK cross-client leak | CVE-2026-25536 (CVSS 7.1) | Responses leaked across client boundaries |
| Feb 2026 | SANDWORM_MODE supply chain attack | — | 19 typosquatting npm packages installed rogue MCP servers; exfiltrated SSH keys, AWS creds, NPM tokens |
| Dec 2025 – Jan 2026 | Operation Bizarre Bazaar | — | 35K attack sessions; 60% targeting MCP endpoints; commercial LLMjacking marketplace |

Sources: [AuthZed Timeline](https://authzed.com/blog/timeline-mcp-breaches), [VulnerableMCP.info](https://vulnerablemcp.info/), [Doyensec MCP Nightmare](https://blog.doyensec.com/2026/03/05/mcp-nightmare.html), [Pillar Security](https://www.pillar.security/blog/operation-bizarre-bazaar-first-attributed-llmjacking-campaign-with-commercial-marketplace-monetization), [Socket SANDWORM_MODE](https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning)

---

## MCP Auth Specification Evolution

Key changes in the **November 25, 2025** spec revision:
- **Client ID Metadata Documents (CIMD)** added as preferred client registration mechanism (adoption at ~3–4%)
- **RFC 8707 Resource Indicators** now mandatory — tokens MUST be bound to specific MCP servers
- **Token pass-through explicitly forbidden** — servers must obtain separate tokens for downstream APIs
- **Confused deputy mitigations** added for proxy servers
- **PKCE with S256 method** mandatory for all flows
- **Protected Resource Metadata (RFC 9728)** — servers respond to unauthorized requests with `WWW-Authenticate` header containing `resource_metadata` URL

**Upcoming in 2026 roadmap** (next spec release tentatively June 2026):
- **SEP-1932 (DPoP)** — Demonstration of Proof-of-Possession, binding tokens to client key pairs
- **SEP-1933 (Workload Identity Federation)** — Cloud-native identity (AWS IAM, GCP Workload Identity, Azure Managed Identity) without static secrets
- **SEP-991 (CIMD)** — becoming recommended default for client registration
- **SEP-2127 (Server Cards)** — standardized server discovery mechanism
- **SEP-1299** — server-side authorization management using HTTP Message Signatures

**Enterprise extensions:**
- **Okta Cross App Access (XAA)** incorporated as the MCP "Enterprise-Managed Authorization" extension — enterprise IdP verifies agent authorization against centralized policies. Okta for AI Agents GA: April 30, 2026.

---

## MCP Auth Tooling Landscape

| Tool | Type | Key Capability | Source |
|------|------|---------------|--------|
| [Kong AI Gateway MCP Tool ACLs](https://konghq.com/blog/product-releases/mcp-tool-acls-ai-gateway) (v3.13, Jan 2026) | Commercial gateway | First production per-tool authorization; default-deny YAML ACLs; OAuth2 plugin | Kong |
| [Traefik Hub TBAC](https://doc.traefik.io/traefik-hub/mcp-gateway/guides/understanding-tbac) (Early Access, GA Apr 2026) | Commercial gateway | Task-Based Access Control: parameter-level authorization across 3 dimensions (Task/Tool/Transaction) | Traefik |
| [Azure APIM MCP Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) | Commercial gateway | Native Entra ID integration; OBO token exchange; full OAuth 2.0/PKCE flow | Microsoft |
| [Cisco AI Defense MCP Catalog](https://blogs.cisco.com/ai/securing-the-ai-agent-supply-chain-with-ciscos-open-source-mcp-scanner) | Commercial + OSS | MCP server discovery/inventory; runtime agent threat detection; MCP Scanner (YARA + LLM + API) | Cisco |
| [IBM ContextForge](https://github.com/IBM/mcp-context-forge) | OSS gateway | Multi-protocol federation (MCP + A2A + REST/gRPC); JWT/OAuth/RBAC; 3.5K stars | IBM |
| [MCPTox](https://arxiv.org/abs/2508.14925) | Benchmark | Tool poisoning benchmark; 20 agents, 45 servers, 353 tools | Research |
| [MindGuard](https://arxiv.org/html/2508.20412v1) | Guardrail | Decision-level guardrail; 94–99% precision on poisoned invocations | Research |
| [MCP Auth library](https://mcp-auth.dev/docs) | OSS library | OAuth 2.1 per MCP spec 2025-06-18 | Community |
| [CSA mcpserver-audit](https://github.com/ModelContextProtocol-Security/mcpserver-audit) | OSS scanner | Static analysis; AIVSS scoring; CWE mapping; CSA-backed | CSA |

---

## OWASP MCP Top 10 (v0.1 Beta)

| # | Risk | AISVS Mapping |
|---|------|---------------|
| MCP01 | Token Mismanagement & Secret Exposure | 10.2.5, 10.2.9, 10.1.2 |
| MCP02 | Privilege Escalation via Scope Creep | 10.2.7, 10.2.11 |
| MCP03 | Tool Poisoning | 10.4.1, 10.4.5 |
| MCP04 | Software Supply Chain Attacks | 10.1.1 |
| MCP05 | Command Injection & Execution | 10.4.4, 10.5.1 |
| MCP06 | Intent Flow Subversion | 10.2.4, 10.4.1 |
| MCP07 | Insufficient Authentication & Authorization | 10.2.1, 10.2.2, 10.2.7 |
| MCP08 | Lack of Audit and Telemetry | C13.1, C13.2 |
| MCP09 | Shadow MCP Servers | 10.2.3 |
| MCP10 | Context Injection & Over-Sharing | 10.4.1, 10.2.6 |

Source: [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)

---

## CoSAI MCP Threat Taxonomy (January 2026)

The Coalition for Secure AI published a 12-threat taxonomy covering ~40 distinct threats across 6 functional areas:

| Category | Threats | C10.2 Relevance |
|----------|---------|-----------------|
| T1-T2: Identity & Access | Improper auth across agent chains; missing privilege separation | Direct — 10.2.1, 10.2.2, 10.2.4, 10.2.7 |
| T3-T4: Input Handling | Input validation failures; data/control boundary failures | 10.2.4 (model output cannot bypass auth) |
| T5-T6: Data & Code Protection | Inadequate encryption/secrets; missing integrity controls | 10.2.5 (no token storage) |
| T7-T8: Network & Transport | Session/transport security gaps; network isolation failures | 10.2.8, 10.2.12 |
| T9-T10: Trust & Design | Overreliance on LLM judgment; absent rate limiting | 10.2.4 (auth cannot rely on model decisions) |
| T11-T12: Operational Security | Detection gaps; configuration management failures | C13 overlap |

Source: [CoSAI Practical Guide to MCP Security](https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/)

---

## Implementation Maturity

| Area | Maturity | Notes |
|------|----------|-------|
| OAuth 2.1 adoption in MCP servers | **Low** | Only 8.5% of ~20K surveyed servers use OAuth; 53% use static API keys (Astrix 2025). |
| Token validation (iss/aud/exp/scope) | **Medium** | Straightforward for OAuth-enabled servers, but most aren't OAuth-enabled. |
| Per-tool authorization | **Low–Medium** | Kong MCP Tool ACLs (GA Jan 2026) is the first production implementation. |
| Argument-level authorization | **Low** | Traefik TBAC (EA March 2026) is the only product. No AuthZed/OPA integration for MCP yet. |
| MCP server registry / discovery | **Low** | Cisco AI Defense MCP Catalog and IBM ContextForge are first movers. SEP-2127 proposes standard. |
| MCP gateway enforcement | **Medium** | Kong, Traefik, Azure APIM, IBM ContextForge provide centralized auth. Adoption growing. |
| Dynamic client registration (CIMD) | **Low** | ~3–4% adoption. SEP-991 making progress. |
| Multi-agent delegation (RFC 8693) | **Low** | Token Exchange is the recommended pattern but production implementations are rare. |
| Security scanning | **Medium** | Cisco MCP Scanner (854 stars), CSA mcpserver-audit, VulnerableMCP.info tracking CVEs. |

---

## Cross-Chapter Links

| Related Section | Overlap |
|----------------|---------|
| [C05 Access Control & Identity](C05-Access-Control.md) | OAuth 2.1, RBAC/ABAC, identity management foundations |
| [C09-06 Authorization & Delegation](C09-06-Authorization-and-Delegation.md) | Multi-agent delegation chains, token propagation, least-privilege |
| [C10-01 Component Integrity](C10-01-Component-Integrity.md) | MCP server integrity verification, supply chain (SANDWORM_MODE) |
| [C10-03 Secure Transport](C10-03-Secure-Transport.md) | mTLS, TLS 1.3, transport-layer security underpinning auth |
| [C10-04 Schema & Message Validation](C10-04-Schema-Message-Validation.md) | Tool description integrity, schema validation as auth complement |
| [C10-06 Transport Restrictions & Boundary Controls](C10-06-Transport-Restrictions-Boundary-Controls.md) | Network isolation preventing unauthorized MCP access |
| [C13-01 Request-Response Logging](C13-01-Request-Response-Logging.md) | Auth event logging, token validation audit trail |

---

## Related Standards & References

- [MCP Authorization Specification (latest)](https://modelcontextprotocol.io/specification/draft/basic/authorization/) — OAuth 2.1, revised November 2025
- [MCP 2026 Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — DPoP, Workload Identity Federation, Server Cards
- [OAuth 2.1 (draft-ietf-oauth-v2-1-15)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1/) — still in draft as of March 2026
- [RFC 7636: PKCE](https://datatracker.ietf.org/doc/html/rfc7636) — mandatory for MCP
- [RFC 7591: Dynamic Client Registration](https://datatracker.ietf.org/doc/html/rfc7591) — backwards-compat fallback
- [RFC 8693: OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693) — recommended for multi-agent delegation
- [RFC 8707: Resource Indicators](https://datatracker.ietf.org/doc/html/rfc8707) — mandatory for MCP token binding
- [RFC 9728: Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728) — server discovery for OAuth
- [OWASP MCP Top 10 (v0.1 Beta)](https://owasp.org/www-project-mcp-top-10/)
- [CoSAI: Practical Guide to MCP Security (January 2026)](https://www.coalitionforsecureai.org/securing-the-ai-agent-revolution-a-practical-guide-to-mcp-security/)
- [OWASP: Securely Using Third-Party MCP Servers](https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/)
- [OWASP: Secure MCP Server Development](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/)
- [Microsoft MCP Azure Security Guide](https://microsoft.github.io/mcp-azure-security-guide/)
- [Okta Cross App Access / Enterprise MCP Authorization](https://www.okta.com/newsroom/articles/cross-app-access-extends-mcp-to-bring-enterprise-grade-security-to-ai-agents/)
- [Doyensec: The MCP AuthN/Z Nightmare (March 2026)](https://blog.doyensec.com/2026/03/05/mcp-nightmare.html)
- [Obsidian Security: MCP-Meets-OAuth Account Takeover](https://www.obsidiansecurity.com/blog/when-mcp-meets-oauth-common-pitfalls-leading-to-one-click-account-takeover)
- [Astrix Security: State of MCP Server Security 2025](https://astrix.security/learn/blog/state-of-mcp-server-security-2025/)
- [Trend Micro: Network-Exposed MCP Servers](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/mcp-security-network-exposed-servers-are-backdoors-to-your-private-data)
- [Elastic Security Labs: MCP Attack/Defense](https://www.elastic.co/security-labs/mcp-tools-attack-defense-recommendations)
- [SMCP: Secure MCP Proposal](https://arxiv.org/pdf/2602.01129)
- [VulnerableMCP.info — MCP CVE Tracker](https://vulnerablemcp.info/)

---

## Open Research Questions

- What is the right OAuth scope granularity for MCP — per-tool, per-resource-type, or per-action? Traefik TBAC proposes a three-layer model but no standard exists.
- How should argument-level authorization be modeled — ABAC, RBAC, or policy-as-code? Neither AuthZed nor OPA has MCP-native integrations yet.
- Is OAuth Token Exchange (RFC 8693) viable across diverse IdPs for multi-agent delegation chains? Okta XAA is the first major integration.
- How do you handle consent for dynamically registered MCP clients given CIMD adoption is at 3–4%?
- Will DPoP (SEP-1932) and Workload Identity Federation (SEP-1933) address the token theft and static credential problems at scale?
- Can MCP gateways (Kong, Traefik, Azure APIM) become the standard enforcement point, or will auth need to be embedded in every server?
- How should organizations close the 8.5% OAuth adoption gap given 53% of servers still use static API keys?

---

[C10 Index](C10-MCP-Security.md) | [README](README.md)
