# C10.2: Authentication & Authorization

> **Parent:** [C10 MCP Security](C10-MCP-Security.md)
> **Requirements:** 12 | **IDs:** 10.2.1–10.2.12
> **Last Researched:** 2026-03-18

## Purpose

This section ensures that MCP clients and servers authenticate each other properly and that authorization is enforced at every tool invocation. The MCP specification mandates OAuth 2.1 as the authorization framework for HTTP-based transports. The auth spec was **substantially revised on November 25, 2025** to address disclosed vulnerabilities including confused deputy attacks and token pass-through. As of early 2026, at least **5 CVEs** have been assigned to MCP components, OAuth implementation flaws affected 43% of surveyed MCP servers, and the OWASP MCP Top 10 (v0.1 beta) lists Token Mismanagement (MCP01) and Insufficient Authentication (MCP07) as top risks.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.2.1** | **Verify that** MCP clients authenticate to MCP servers using the OAuth 2.1 authorization framework and present a valid OAuth access token for each request, and that the MCP server validates the token according to OAuth 2.1 resource server requirements. | 1 | D/V | **Unauthenticated tool invocation.** Without OAuth, any client that can reach the MCP server endpoint can invoke tools. This enables unauthorized data access, lateral movement, and abuse of server-side resources by rogue agents or injected prompts. | Inspect MCP server code for OAuth token validation middleware. Attempt tool invocation without a token and verify rejection (HTTP 401). Verify the server checks token signature, expiration, and issuer. Review MCP client code to confirm tokens are attached to every JSON-RPC request. | The MCP spec (2025-03-26) defines OAuth 2.1 with PKCE and dynamic client registration. SDK support is emerging but not all MCP server implementations enforce this yet. Many community MCP servers still operate without any authentication, relying on network isolation alone. |
| **10.2.2** | **Verify that** MCP servers validate OAuth access tokens including issuer, audience, expiration, and scope claims, ensuring that tokens were issued for the specific MCP server before allowing tool invocation. | 1 | D/V | **Token confusion / cross-service token reuse.** An attacker obtains a valid OAuth token issued for a different service and presents it to the MCP server. Without audience validation, the server accepts it, granting unauthorized access. This is a concrete variant of the "confused deputy" problem. | Verify the MCP server checks `iss`, `aud`, `exp`, and `scope` claims. Present a valid token with incorrect audience and confirm rejection. Test with expired tokens. Review token validation library configuration for required claims. | Standard OAuth 2.1 resource server behavior — well-understood, but easy to misconfigure. Common pitfall: accepting tokens from any issuer when the server trusts a multi-tenant identity provider. |
| **10.2.3** | **Verify that** MCP servers are registered through a controlled technical onboarding mechanism requiring explicit owner, environment, and resource definitions; unregistered or undiscoverable servers must not be callable in production. | 1 | D/V | **Shadow MCP servers / unauthorized tool exposure.** A developer deploys an MCP server that exposes sensitive database access without security review. Without a registration requirement, the server is silently adopted by agents, bypassing access control and audit. | Review the organization's MCP server inventory or registry. Attempt to connect an MCP client to an unregistered server in a production environment and verify it fails. Check that server onboarding requires security review, owner assignment, and environment tagging. | No standard MCP server registry exists. This is currently an organizational process control. Enforcement typically requires network-level controls (e.g., service mesh policies) or client-side allowlists. |
| **10.2.4** | **Verify that** authorization decisions at the MCP layer are enforced by the MCP server's policy logic, and that model-generated output cannot influence, override, or bypass access control checks. | 1 | D/V | **Prompt injection bypassing authorization.** A prompt injection attack crafts model output that includes instructions like "ignore access controls" or manipulates tool arguments to escalate privileges. If the MCP server's auth logic can be influenced by model output, access control is effectively defeated. | Review MCP server authorization code to confirm decisions are based solely on token claims, server-side policy, and user identity — never on content from the model's output or tool arguments that could be model-influenced. Attempt privilege escalation via crafted tool arguments. | This is a fundamental architectural requirement: the authorization boundary must be impermeable to model-generated content. Requires clear separation between the data plane (model output) and the control plane (auth decisions). |
| **10.2.5** | **Verify that** MCP servers act as OAuth 2.1 resource servers only by validating tokens issued by external authorization servers and by not storing tokens or user credentials. | 2 | D/V | **Token theft from MCP server compromise.** If an MCP server stores OAuth tokens or credentials, a server compromise exposes all stored tokens, enabling mass impersonation. The server should be stateless with respect to credentials. | Review server code and storage (database, filesystem, memory) for any token or credential persistence. Verify tokens are validated inline (JWT signature check or token introspection) and discarded after the request. Check that no token caching layer exists. | Aligns with OAuth 2.1 resource server best practice. Some implementations may cache tokens for performance — if so, the cache must be short-lived, encrypted, and purged on session end. The MCP spec allows the server to also act as an authorization server, but this requirement pushes toward separation of concerns. |
| **10.2.6** | **Verify that** MCP `tools/list` and resource discovery responses are filtered based on the end-user's authorized scopes so that agents receive only the tool and resource definitions the user is permitted to invoke. | 2 | D/V | **Information disclosure / attack surface enumeration.** If all tools are visible regardless of authorization, an attacker (or a prompt injection) can discover high-privilege tools and attempt invocation. Filtered discovery reduces the attack surface visible to the model. | Call `tools/list` with tokens of varying scope levels and verify that the response only includes tools the token authorizes. Test with a minimal-scope token and confirm restricted tools are absent from the response, not just blocked at invocation. | Not all MCP server implementations support filtered discovery. The MCP spec does not mandate filtering at the discovery level — only at invocation. This requirement goes beyond the spec to reduce information leakage. |
| **10.2.7** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 | D/V | **Horizontal privilege escalation via argument manipulation.** A user is authorized to query their own data but crafts (or the model generates) tool arguments targeting another user's data. Without argument-level authorization, the server processes the request. Example: `read_file(path="/etc/shadow")` when the user is only authorized for `/home/user/`. | Test tool invocations with arguments outside the user's authorized scope (e.g., different tenant IDs, unauthorized file paths, other users' records). Verify the server rejects these based on the token's claims, not just the tool name. Review authorization middleware for argument inspection. | Argument-level authorization is significantly harder than tool-level authorization. Requires the server to understand the semantics of each argument and map them to authorization policies. No standard framework exists for this in MCP — it must be implemented per-tool. |
| **10.2.8** | **Verify that** MCP session identifiers are treated as state, not identity: generated using cryptographically secure random values, bound to the authenticated user, and never relied on for authentication or authorization decisions. | 1 | D/V | **Session hijacking / session confusion.** If session IDs are predictable or used as a proxy for identity, an attacker who obtains or guesses a session ID gains the associated user's privileges. MCP sessions (via `Mcp-Session-Id` header) must not be a substitute for OAuth token validation. | Review session ID generation for use of CSPRNG (e.g., `crypto.randomUUID()`). Verify that every request is authenticated via OAuth token regardless of session state. Attempt to use a valid session ID with a different user's token and confirm the server uses the token's identity, not the session's. | The MCP spec defines `Mcp-Session-Id` for transport-level state management. The risk is that implementations shortcut authentication by trusting the session ID after initial auth, creating a session fixation vulnerability. |
| **10.2.9** | **Verify that** MCP servers do not pass through access tokens received from clients to downstream APIs and instead obtain a separate token scoped to the server's own identity (e.g., via on-behalf-of or client credentials flow). | 2 | D/V | **Token relay / over-privileged downstream access.** If the MCP server forwards the user's token to a downstream API, that API receives a token with the user's full scope — potentially broader than what the MCP server needs. If the downstream API is compromised, the user's token is exposed. Also violates least-privilege: the downstream call should use a token scoped to the MCP server's specific needs. | Review MCP server code for downstream API calls. Check whether the user's incoming token is forwarded or whether a separate token is obtained (via `client_credentials` grant, `urn:ietf:params:oauth:grant-type:jwt-bearer` for on-behalf-of, or similar). Verify downstream tokens have reduced scope. | On-behalf-of (OBO) flow support varies by identity provider. Azure AD supports OBO natively; other providers may require custom token exchange. Client credentials flow is simpler but loses user context. The right choice depends on whether downstream APIs need to know which user originated the request. |
| **10.2.10** | **Verify that** MCP servers acting as OAuth proxies to third-party APIs enforce per-client consent before forwarding authorization requests, preventing cached approvals from being reused across dynamically registered clients. | 2 | D/V | **Consent bypass via dynamic client registration.** The MCP spec supports dynamic client registration. A malicious client could register dynamically and inherit cached OAuth approvals from a previous client, gaining access to third-party APIs without user consent. Each dynamically registered client must obtain its own consent. | Register a new MCP client dynamically and verify that it cannot access third-party API tokens previously approved for a different client. Verify the consent UI clearly identifies the requesting client. Review the authorization server's consent storage for per-client isolation. | This is specific to MCP's dynamic client registration feature. Standard OAuth authorization servers typically bind consent to `client_id`, but dynamic registration means `client_id` values are ephemeral. The server must not conflate consent across registration instances. |
| **10.2.11** | **Verify that** MCP clients request only the minimum scopes needed for the current operation, elevate progressively via step-up authorization, and that servers reject wildcard or overly broad scopes. | 2 | D/V | **Over-scoped tokens enabling lateral movement.** If an MCP client requests broad scopes upfront (e.g., `*` or `admin`), a compromised token grants access to all tools and resources. Least-privilege scoping limits blast radius. Step-up auth ensures elevated access requires re-confirmation. | Review MCP client OAuth configuration for requested scopes. Verify scopes are minimal for the initial connection. Test requesting a wildcard scope and confirm the server rejects it. Verify that high-privilege operations trigger step-up authorization (e.g., re-authentication or additional consent). | The MCP spec does not define standard scope names or a scope hierarchy. Scope naming and granularity are left to individual MCP server implementations, making cross-server least-privilege difficult to standardize. |
| **10.2.12** | **Verify that** MCP servers enforce deterministic session teardown, destroying cached tokens, in-memory state, temporary storage, and file handles when a session terminates, disconnects, or times out. | 2 | D/V | **Stale session exploitation / resource leakage.** If sessions are not properly torn down, cached tokens remain valid after the user disconnects, temporary files with sensitive data persist on disk, and file handles to protected resources remain open. An attacker who gains access to the server can harvest these artifacts. | Terminate an MCP session and verify: (1) cached tokens are invalidated, (2) temporary files are deleted, (3) file handles are closed, (4) the session ID is rejected on subsequent requests. Test with abrupt disconnection (not graceful close) and verify cleanup still occurs via timeout. | The MCP spec defines session lifecycle but does not prescribe cleanup behavior. Implementations must handle both graceful termination (`HTTP DELETE` on session endpoint) and ungraceful disconnection (network failure, client crash). Timeout-based cleanup is essential for the latter case. |

---

## MCP Auth CVEs and Incidents (2025-2026)

| Date | Incident | CVE | Impact |
|------|----------|-----|--------|
| Apr 2025 | WhatsApp MCP tool poisoning | — | Invariant Labs demonstrated exfiltration of thousands of messages via backdoored tool descriptions |
| May 2025 | GitHub MCP prompt injection | — | Over-privileged PATs enabled extraction of private repo data via prompt injection |
| Jun 2025 | Anthropic MCP Inspector RCE | CVE-2025-49596 | Unauthenticated RCE on developer machines via unprotected localhost listener |
| Jul 2025 | mcp-remote command injection | CVE-2025-6514 | Critical: malformed `authorization_endpoint` passed to system shell; 437K+ downloads affected (Cloudflare, Hugging Face, Auth0 guides) |
| Aug 2025 | Anthropic Filesystem MCP Server | CVE-2025-53109, CVE-2025-53110 | Sandbox escape + symlink bypass enabling arbitrary file access |
| Aug-Sep 2025 | Square MCP Server OAuth flaw | — | Missing `redirect_uri` restrictions during DCR enabled one-click merchant account takeover |
| Sep 2025 | Malicious Postmark MCP package | — | Supply-chain: BCC'd all outgoing emails to attacker-controlled servers |
| Oct 2025 | Smithery MCP hosting path traversal | — | Leaked Docker credentials and Fly.io API token controlling 3,000+ apps |
| Oct 2025 | Figma/Framelink MCP command injection | CVE-2025-53967 | Unsafe `child_process.exec` with untrusted input |

Sources: [AuthZed Timeline](https://authzed.com/blog/timeline-mcp-breaches), [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), [Obsidian Security](https://www.obsidiansecurity.com/blog/when-mcp-meets-oauth-common-pitfalls-leading-to-one-click-account-takeover)

---

## MCP Auth Specification Evolution

Key changes in the **November 25, 2025** spec revision:
- **Client ID Metadata Documents (CIMD)** added as the preferred client registration mechanism (adoption still at ~3%)
- **RFC 8707 Resource Indicators** now mandatory — tokens MUST be bound to specific MCP servers
- **Token pass-through explicitly forbidden** — servers must obtain separate tokens for downstream APIs
- **Confused deputy mitigations** added for proxy servers
- **PKCE with S256 method** mandatory for all flows

Three client registration mechanisms in priority order: (1) CIMD (new, preferred), (2) Pre-registration, (3) Dynamic Client Registration (now a backwards-compatibility fallback).

---

## MCP Security Tools

| Tool | Purpose | Key Metric |
|------|---------|-----------|
| [MCPTox](https://arxiv.org/abs/2508.14925) | Tool poisoning benchmark | Tests 20 LLM agents across 45 servers, 353 tools; o1-mini: 72.8% ASR; Claude 3.7 Sonnet: <3% refusal |
| [MindGuard](https://arxiv.org/html/2508.20412v1) | Decision-level guardrail | 94-99% avg precision detecting poisoned invocations; 95-100% attribution accuracy; sub-second processing |
| [MCP Auth library](https://mcp-auth.dev/docs) | OAuth implementation | Implements MCP auth spec 2025-06-18 for adding OAuth to servers |
| [mcp-client-gen](https://github.com/kriasoft/mcp-client-gen) | Type-safe SDK generator | OAuth 2.1 support; generates TypeScript SDKs from MCP servers |

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

## Related Standards & References

- [MCP Authorization Specification (latest)](https://modelcontextprotocol.io/specification/draft/basic/authorization/) — OAuth 2.1 integration, revised Nov 2025
- [OAuth 2.1 (draft-ietf-oauth-v2-1-13)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13) — base authorization framework
- [RFC 7636: PKCE](https://datatracker.ietf.org/doc/html/rfc7636) — mandatory for MCP
- [RFC 7591: Dynamic Client Registration](https://datatracker.ietf.org/doc/html/rfc7591) — backwards-compat fallback
- [RFC 8707: Resource Indicators](https://datatracker.ietf.org/doc/html/rfc8707) — now mandatory for MCP token binding
- [OWASP MCP Top 10 (v0.1 Beta)](https://owasp.org/www-project-mcp-top-10/)
- [OWASP Practical Guide: Securely Using Third-Party MCP Servers](https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/)
- [OWASP Practical Guide: Secure MCP Server Development](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/)
- [Microsoft MCP Azure Security Guide](https://microsoft.github.io/mcp-azure-security-guide/)
- [Red Hat MCP Security Analysis](https://www.redhat.com/en/blog/model-context-protocol-mcp-understanding-security-risks-and-controls)
- [Elastic Security Labs: MCP Attack/Defense](https://www.elastic.co/security-labs/mcp-tools-attack-defense-recommendations)
- [SMCP: Secure MCP Proposal](https://arxiv.org/pdf/2602.01129)
- [OWASP ASVS v4: V3 Session Management](https://owasp.org/www-project-application-security-verification-standard/)

---

## Open Research Questions

- What is the right OAuth scope granularity for MCP — per-tool, per-resource-type, or per-action? The MCP spec does not define standard scope names.
- How should argument-level authorization be modeled — ABAC, RBAC, or policy-as-code (e.g., OPA/Rego)?
- Is on-behalf-of (OBO) flow viable across diverse identity providers for MCP token exchange?
- How do you handle consent for dynamically registered MCP clients given CIMD adoption is at 3%?
- What is the right response to rug-pull attacks (tool definitions that mutate post-approval)?
- How should MCP auth interact with multi-agent delegation chains where trust must be propagated?
- Can MindGuard-style decision-level guardrails become a standard architectural component for MCP deployments?

---

[C10 Index](C10-MCP-Security.md) | [README](README.md)
