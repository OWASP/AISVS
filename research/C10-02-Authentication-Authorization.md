# C10.2: Authentication & Authorization

> **Parent:** [C10 MCP Security](C10-MCP-Security.md)
> **Requirements:** 9 | **IDs:** 10.2.1, 10.2.3, 10.2.6–10.2.9, 10.2.11–10.2.13
> **Last Researched:** 2026-04-16 (r3)

## Purpose

This section ensures that MCP clients and servers authenticate each other properly and that authorization is enforced at every tool invocation. The MCP specification mandates OAuth 2.1 as the authorization framework for HTTP-based transports. The auth spec was **substantially revised on November 25, 2025** to address disclosed vulnerabilities including confused deputy attacks and token pass-through. As of early 2026, **30+ CVEs** were filed against MCP components in just 60 days (January–February 2026), the OWASP MCP Top 10 (v0.1 beta) lists Token Mismanagement (MCP01) and Insufficient Authentication (MCP07) as top risks, and real-world data paints a stark adoption picture: only **8.5%** of MCP servers use OAuth — 53% still rely on static API keys (Astrix Security survey of ~20,000 servers). Trend Micro found **492 MCP servers** exposed on the internet with zero authentication, exposing 1,402 tools.

As of March 2026, Microsoft's Patch Tuesday disclosed **CVE-2026-26118** (CVSS 8.8) — an SSRF in Azure MCP Server that let authenticated attackers coerce the server into leaking its managed identity token, enabling privilege escalation across Azure resources. This is the first CVE directly targeting a major cloud provider's MCP auth infrastructure. Days later, **CVE-2026-32111** (March 12, 2026) hit the ha-mcp OAuth beta — an SSRF via the `ha_url` parameter that lets unauthenticated attackers scan internal networks from the server's position, demonstrating that SSRF remains the dominant auth-adjacent vulnerability class in MCP servers. The supply chain angle intensified in late March: the **Trivy supply chain compromise** (CVE-2026-33634, March 19, 2026) poisoned GitHub Actions and release binaries of Aqua Security's vulnerability scanner, exfiltrating pipeline credentials including cloud keys and Kubernetes tokens; and the **litellm supply chain attack** (March 24, 2026) published malicious PyPI versions 1.82.7–1.82.8 of the popular LLM proxy library, bypassing the project's normal release process. Both incidents underscore the risk of credential theft when MCP servers run in CI/CD pipelines with broad access.

Meanwhile, NIST launched the **AI Agent Standards Initiative** (February 17, 2026), naming MCP as a candidate protocol for integrating security and identity controls into agent ecosystems. The initiative's three pillars — Security, Interoperability, and Trust — signal that federal standardization of agent authentication is coming. A companion NCCoE concept paper on "Accelerating Adoption of Software and AI Agent Identity and Authorization" calls for cryptographic delegation chains and distinct identity mechanisms for non-human agents — aligning closely with the requirements in this section. The NCCoE comment period remains open through **April 2, 2026**, and community input will directly inform subsequent project scoping and demonstration efforts. On the tooling front, **AWS Bedrock AgentCore Gateway** emerged as the first hyperscaler-native MCP gateway with full OAuth 2.1 support — including JWT bearer token validation, scope enforcement, RFC 9728 Protected Resource Metadata, and fine-grained interceptors for tool-level and argument-level access control.

A fundamental gap in the MCP OAuth 2.1 model is worth highlighting: **PKCE secures the token exchange but does not authenticate the client**. Any process that can initiate a PKCE flow can obtain tokens. The specification intentionally leaves client authentication methods undefined, which means the "unauthenticated client" problem is structural, not just an adoption gap. Workload identity federation (SEP-1933) and infrastructure-asserted identity (AWS IAM Roles, Azure Managed Identity, Kubernetes ServiceAccount tokens) are the leading candidates to close this gap, with Aembit's workload IAM platform emerging as the first product to apply non-human identity management specifically to MCP agent-to-server communication.

Token management failures compound the auth-bypass problem: **CVE-2026-20205** (Splunk MCP Server, April 2026, CVSS 7.2) showed that the Splunk MCP Server app logged session and authorization tokens in plaintext to the `_internal` index — any user with admin-level index access could harvest active tokens for replay. This is CWE-532 (Information Exposure Through Log Files) applied to the MCP context, and it underscores that even authenticated MCP deployments remain vulnerable when token hygiene is neglected.

The auth-bypass problem extends beyond MCP-native servers: **CVE-2026-33032** (March 30, 2026, CVSS 9.8) exposed Nginx UI's `/mcp_message` endpoint with an empty-by-default IP whitelist treated as "allow all" — unauthenticated attackers could invoke 12 MCP tools to inject Nginx configs, reload the server, and intercept all traffic, achieving full web server takeover. Recorded Future's Insikt Group confirmed **active exploitation in March 2026** across 2,600+ exposed instances (Shodan); patched in nginx-ui v2.3.4 on April 15, 2026. On the OAuth proxy front, **CVE-2026-34457** (April 14, 2026, CVSS 9.1) showed that OAuth2 Proxy — widely used as an auth gateway in front of MCP servers — could be bypassed by spoofing the health check User-Agent string when deployed with `auth_request`-style integrations. Fixed in 7.15.2, but the pattern highlights that even well-established auth proxies introduce subtle bypass paths. The session layer is also under pressure: **CVE-2026-33946** (MCP Ruby SDK, April 2, 2026, CVSS 8.2) demonstrated that insufficient session binding in `streamable_http_transport.rb` allows any party with a valid session ID to hijack SSE streams and intercept all MCP communications — a direct instantiation of CWE-384 (Session Fixation) in the MCP transport layer. Meanwhile, **CVE-2026-5059** (aws-mcp-server, April 11, 2026, CVSS 9.8) showed that classic command injection — unsanitized user input passed to system calls — continues to plague MCP server implementations, requiring no authentication to exploit.

As of April 2026, two milestones are reshaping the enterprise auth landscape. **Okta for AI Agents** reaches GA on **April 30, 2026**, with Agent Gateway serving as a centralized control plane — it offers agent discovery (including shadow agent detection), a virtual MCP server that aggregates tools from Okta's MCP registry, privileged credential management with automatic rotation, and a universal logout "kill switch" for instant revocation. Cross App Access (XAA) is now the official MCP "Enterprise-Managed Authorization" extension, giving enterprises IdP-verified agent authorization against centralized policies. Meanwhile, the OAuth confused deputy attack class widened: **CVE-2026-27124** (FastMCP) demonstrated that missing consent verification in OAuth proxy callbacks lets attackers perform actions on behalf of victims without explicit consent, and **CVE-2026-35577** (Apollo MCP Server) showed that DNS rebinding bypasses Host header validation on local MCP servers — both patched but indicative of the pattern.

The **AAIF MCP Dev Summit North America** (April 2–3, 2026, New York) drew ~1,200 attendees under the Linux Foundation's Agentic AI Foundation umbrella. The dominant architectural pattern that emerged: centralized gateways paired with registries as control planes, with Amazon, Uber, Docker, Kong, and Solo.io all converging on this model for enterprise-scale MCP deployments. Solo.io followed up immediately with **agentgateway 2.3** (April 15, 2026), introducing route-level MCP authentication with OBO token exchange and claim propagation to AWS AgentCore — the first gateway to combine route-level auth granularity with explicit fail-open/fail-closed policy modes. Uber disclosed that their GenAI Gateway (built in Go) processes tens of thousands of agent executions weekly, performing PII redaction before requests reach external models. On the protocol side, **SEP-1442** is shifting MCP from stateful sessions toward stateless requests — a significant change that will affect session-based auth patterns. The **Descope Agentic Identity Hub 2.0** (launched January 26, 2026) emerged as the first identity platform purpose-built for MCP auth, offering per-agent and per-tool authorization scopes, hardened DCR with CIMD support, a credential vault with 50+ prebuilt connection templates, and tenant-level isolation for B2B MCP deployments. Descope's own survey found that while 88% of identity decision-makers use or plan to use AI agents, only 37% have progressed past pilots — indicating that auth complexity remains a key blocker.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **10.2.1** | **Verify that** MCP clients and servers implement the OAuth 2.1 authorization framework: clients present a valid access token for each request, and servers validate the token's issuer, audience, expiration, and scope claims, acting as resource servers that do not store tokens or user credentials. | 1 | **Unauthenticated tool invocation.** Without OAuth, any client that can reach the MCP server endpoint can invoke tools. Trend Micro found 492 internet-exposed MCP servers with zero authentication, exposing 1,402 tools — 90%+ offering direct data source access. Operation Bizarre Bazaar (December 2025 – January 2026) saw 60% of attack traffic targeting MCP endpoints, exploiting unauthenticated servers for LLMjacking. SANDWORM_MODE (February 2026) installed rogue MCP servers via 19 typosquatting npm packages. As of April 2026, the consequences of missing auth continue to mount: **CVE-2026-32211** (April 3, 2026, CVSS 9.1) — the Azure MCP Server (`@azure-devops/mcp`) shipped without authentication entirely, exposing API keys, auth tokens, and project data to anyone with network access; and **CVE-2026-34953** (April 3, 2026, CVSS 9.1) — PraisonAI's `OAuthManager.validate_token()` returned True for any token not in its (empty by default) store, treating every request as authenticated. | Inspect MCP server code for OAuth token validation middleware. Attempt tool invocation without a token and verify rejection (HTTP 401). Verify the server validates issuer, audience, expiration, and scope claims per the 2026-03-26 spec revision. Review MCP client code to confirm tokens are attached to every JSON-RPC request and include the `resource` parameter (RFC 8707). Use Cisco MCP Scanner (open-source, YARA + LLM + API detection engines) to audit server configurations. Verify the server publishes `/.well-known/oauth-protected-resource` metadata (RFC 9728). | OAuth 2.1 adoption remains critically low — only 8.5% of ~20,000 surveyed MCP servers use OAuth (Astrix Security 2025). 53% rely on static API keys, and 79% pass keys via environment variables. OAuth 2.1 itself is still in draft (not yet an RFC). The 2026-03-26 spec revision now explicitly classifies MCP servers as OAuth Resource Servers and mandates RFC 8707 Resource Indicators — clients must include the `resource` parameter in token requests to bind tokens to specific servers. MCP gateways (Kong, Traefik Hub, Azure APIM, AWS AgentCore Gateway) are the primary enforcement path for organizations that can't modify every MCP server. Drop-in solutions like MCP OAuth Gateway (OSS), Auth0's MCP integration, and Descope Agentic Identity Hub 2.0 (with hardened DCR, CIMD, and 50+ prebuilt connection templates) add OAuth 2.1 without code changes. PKCE is mandatory but does not authenticate the client itself — any process that can initiate a PKCE flow can obtain tokens. |
| **10.2.3** | **Verify that** MCP servers are registered through a controlled technical onboarding mechanism requiring explicit owner, environment, and resource definitions; unregistered or undiscoverable servers must not be callable in production. | 1 | **Shadow MCP servers / unauthorized tool exposure.** Bitsight found ~1,000 exposed MCP servers with no authorization. Smithery MCP hosting path traversal (October 2025) leaked Docker credentials and a Fly.io API token controlling 3,000+ apps from an uncontrolled server deployment. SANDWORM_MODE installed rogue MCP servers via supply chain attack without any registration or approval. | Review the organization's MCP server inventory or registry. Attempt to connect an MCP client to an unregistered server in production and verify it fails. Check that server onboarding requires security review, owner assignment, and environment tagging. Use Cisco AI Defense MCP Catalog (announced February 2026) to discover and inventory MCP servers across platforms. SEP-2127 (Server Cards) proposes a standard discovery mechanism. | No standard MCP server registry exists. Cisco AI Defense MCP Catalog and IBM ContextForge are the first products addressing centralized discovery. Enforcement requires network-level controls (service mesh, MCP gateway allowlists) or client-side allowlists. CSA mcpserver-audit provides static analysis scanning with CWE mapping and AIVSS scoring. |
| **10.2.6** | **Verify that** MCP `tools/list` and resource discovery responses are filtered based on the end-user's authorized scopes so that agents receive only the tool and resource definitions the user is permitted to invoke. | 2 | **Information disclosure / attack surface enumeration.** MCPTox benchmark found o1-mini: 72.8% ASR when exposed to all tool descriptions; filtering reduces the attack surface visible to the model and limits tool poisoning impact. | Call `tools/list` with tokens of varying scope levels and verify the response only includes authorized tools. Test with a minimal-scope token and confirm restricted tools are absent from the response. Kong MCP Tool ACLs (v3.13, January 2026) implements this as a default-deny YAML-based ACL that filters tool lists before returning them to clients. | Kong MCP Tool ACLs is the first production implementation of filtered tool discovery. The MCP spec does not mandate filtering at the discovery level — only at invocation. This requirement goes beyond the spec. Traefik TBAC adds parameter-level filtering (Transaction authorization) on top of tool-level filtering. |
| **10.2.7** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 | **Horizontal privilege escalation via argument manipulation.** Supabase Cursor agent incident (mid-2025) — agent ran with privileged service-role access and processed user-supplied SQL in support tickets, exfiltrating integration tokens. No standard framework exists for argument-level authorization in MCP. | Test tool invocations with arguments outside the user's authorized scope (e.g., different tenant IDs, unauthorized file paths). Verify the server rejects based on token claims, not just tool name. Review authorization middleware for argument inspection. Traefik TBAC's Transaction authorization enforces parameter-level constraints. AWS Bedrock AgentCore Gateway interceptors can enforce tool-level and argument-level policies at the gateway, contextually filtering `ListTools`, `InvokeTool`, and `Search` calls based on the calling principal's permissions. | Argument-level authorization is significantly harder than tool-level. Requires the server to understand argument semantics. As of April 2026, four products address this: Traefik TBAC (Transaction authorization), AWS AgentCore Gateway (interceptors), Oso (Polar policy-as-code supporting RBAC/ReBAC/ABAC simultaneously), and Kong Tool ACLs (tool-level only). Oso evaluates per-token identity against declarative policies, centralizing authorization logic outside MCP server code. Gravitee MCP Proxy adds OpenFGA/AuthZen for relationship-based authorization. AuthZed/SpiceDB and OPA/Rego do not yet have production MCP integrations (SpiceDB ships an MCP server for development, but not as a policy engine for MCP tool authorization). |
| **10.2.8** | **Verify that** MCP session identifiers are treated as state, not identity: generated using cryptographically secure random values, bound to the authenticated user, and never relied on for authentication or authorization decisions. | 1 | **Session hijacking / session confusion.** CVE-2026-25536 (MCP TypeScript SDK, February 2026, CVSS 7.1) — `StreamableHTTPServerTransport` reused transport across multiple clients, leaking responses across client boundaries. CVE-2026-33946 (MCP Ruby SDK, April 2, 2026, CVSS 8.2) — insufficient session binding in `streamable_http_transport.rb` allows any party with a valid session ID to hijack SSE streams and intercept all MCP communications (CWE-384 Session Fixation / CWE-639). GHSA-9f65-56v6-gxw7 (Claude Code IDE extension) — WebSocket authentication bypass on localhost. | Review session ID generation for CSPRNG. Verify every request is authenticated via OAuth token regardless of session state. Attempt to use a valid session ID with a different user's token and confirm the server uses the token's identity. Test for the cross-client leak pattern from CVE-2026-25536 and the SSE hijack pattern from CVE-2026-33946. Verify SSE connections validate session ownership, not just session ID validity. | The MCP spec defines `Mcp-Session-Id` for transport-level state. Session management bugs now span both the TypeScript SDK (cross-client leak) and the Ruby SDK (SSE stream hijacking) — the pattern indicates that session-identity conflation is systemic across MCP SDK implementations, not isolated to one language. |
| **10.2.9** | **Verify that** MCP servers do not pass through access tokens received from clients to downstream APIs and instead obtain a separate token scoped to the server's own identity (e.g., via on-behalf-of or client credentials flow). | 2 | **Token relay / over-privileged downstream access.** The MCP spec (November 2025 revision) explicitly forbids token pass-through. The "God Key" problem describes the anti-pattern where a single shared credential grants access to all tools and downstream APIs. Token Exchange (RFC 8693) is the recommended pattern for multi-agent delegation chains — agents obtain short-lived, narrowly scoped credentials while maintaining user attribution via dual identity headers. **CVE-2026-20205** (Splunk MCP Server, April 2026, CVSS 7.2) shows the related risk of token exposure: session and authorization tokens were logged in plaintext to internal indexes, enabling any admin-level user to harvest and replay active tokens. | Review MCP server code for downstream API calls. Check whether the user's token is forwarded or whether a separate token is obtained. Verify downstream tokens have reduced scope. Azure APIM MCP Gateway natively supports On-Behalf-Of (OBO) token exchange with Entra ID. Solo agentgateway v2.3 (April 2026) supports OBO token exchange with explicit claim propagation to AWS AgentCore, plus JWT pass-through with SigV4. Strata Maverics enforces DPoP and RFC 8693 token exchange by default, with progressive scope reduction across delegation chains. | OBO flow support varies by identity provider. Azure AD supports OBO natively. Okta's Cross App Access (XAA) protocol has been incorporated as the MCP "Enterprise-Managed Authorization" extension — the enterprise IdP verifies agent authorization against centralized policies. Okta for AI Agents GA is April 30, 2026. Solo agentgateway v2.3 adds three distinct auth patterns for AgentCore integration: OBO token exchange, JWT pass-through with SigV4, and claims-as-headers. Strata Maverics is the first to operationalize DPoP by default for agent-to-server flows. |
| **10.2.11** | **Verify that** MCP clients request only the minimum scopes needed for the current operation and elevate progressively via step-up authorization for higher-privilege operations. | 2 | **Over-scoped tokens enabling lateral movement.** 67% of enterprise teams still rely on static, broadly-scoped credentials for AI systems (Teleport 2026 survey). Over-privileged AI systems experience 4.5x higher incident rates. GitGuardian analysis (March 2026) notes OAuth scopes authorize access to the MCP server, not individual tools — creating a tool-level authorization gap. | Review MCP client OAuth configuration for requested scopes. Verify scopes are minimal. Test requesting a wildcard scope and confirm rejection. Verify high-privilege operations trigger step-up authorization. | The MCP spec does not define standard scope names or a scope hierarchy. Scope naming is left to individual implementations, making cross-server least-privilege difficult. The emerging enterprise pattern is mTLS at transport layer + OAuth 2.1 at authorization layer + RFC 8707 for token scoping + RFC 8693 for delegation chains. |
| **10.2.12** | **Verify that** MCP servers enforce deterministic session teardown, destroying cached tokens, in-memory state, temporary storage, and file handles when a session terminates, disconnects, or times out. | 2 | **Stale session exploitation / resource leakage.** CVE-2025-53109/53110 (Anthropic Filesystem MCP Server, August 2025) — sandbox escape + symlink bypass enabled arbitrary file access, potentially via stale file handles from improperly torn-down sessions. | Terminate an MCP session and verify: (1) cached tokens are invalidated, (2) temporary files are deleted, (3) file handles are closed, (4) the session ID is rejected on subsequent requests. Test with abrupt disconnection and verify cleanup via timeout. | The MCP spec defines session lifecycle but does not prescribe cleanup behavior. Implementations must handle both graceful termination (`HTTP DELETE`) and ungraceful disconnection (timeout-based cleanup). |
| **10.2.13** | **Verify that** autonomous agents authenticate using cryptographically bound identity credentials (e.g., key-based proof-of-possession) rather than bearer-only tokens, ensuring that agent identity cannot be transferred, replayed, or impersonated by forwarding a shared secret. | 2 | **Bearer token theft and agent impersonation.** Token theft accounted for 31% of Microsoft 365 breaches in 2025 — nearly 40,000 incidents daily (Obsidian Security). The ShinyHunters group replayed stolen OAuth bearer tokens across 700+ Salesforce environments without triggering any auth alerts (Salesloft-Drift incident). In MCP ecosystems, agents pass bearer tokens thousands of times per second across tool invocations; each handoff is a theft/replay opportunity. SANDWORM_MODE (February 2026) exfiltrated SSH keys and AWS credentials from agent pipelines — bearer tokens in those environments would be equally replayable. The IETF draft-klrc-aiagent-auth-00 (March 2026) explicitly rejects static API keys and bearer-only tokens as unsuitable for agent authentication. | Verify agent credentials use proof-of-possession (DPoP per RFC 9449, mTLS, or SPIFFE SVIDs) rather than bearer-only tokens. Confirm that each request includes a cryptographic proof signed by the agent's private key. Attempt to replay a captured token from a different client and verify rejection. Check for `cnf.jkt` (confirmation thumbprint) claims in JWTs. Review whether agent keys are hardware-backed (TPM, Secure Enclave) or software-only. Inspect SPIFFE/WIMSE identifier assignment — each agent should have exactly one WIMSE identifier. Test token binding by intercepting an access token and presenting it without the corresponding DPoP proof header. | SEP-1932 (DPoP Profile for MCP) is under active review — it adopts RFC 9449 DPoP for sender-constrained tokens without requiring full-payload signing. SEP-1461 (Attested Client Registration with hardware-backed keys) was closed March 2026 for lack of sponsorship — hardware attestation may move to an auth extension. The IETF draft-klrc-aiagent-auth-00 (March 2026) composes WIMSE, SPIFFE, and OAuth 2.0 into the AIMS framework for agent identity without new protocols. The Agent Identity Protocol (AIP) paper (March 2026, arXiv 2603.24775) proposes Invocation-Bound Capability Tokens using Ed25519 signatures with append-only delegation chains — 100% adversarial rejection across 600 test attacks. As of March 2026, no MCP implementation ships DPoP support; this remains the largest gap in agent auth. Aembit's workload IAM and Teleport's machine identity are the closest production solutions for infrastructure-asserted agent identity. |

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
| Mar 2026 | Azure MCP Server SSRF | CVE-2026-26118 (CVSS 8.8) | Authenticated SSRF leaked managed identity tokens → privilege escalation across Azure resources; patched in March 2026 Patch Tuesday |
| Mar 2026 | ha-mcp OAuth beta SSRF | CVE-2026-32111 (CVSS 5.3) | Unauthenticated SSRF via `ha_url` parameter in OAuth flow; internal network scanning from server position |
| Mar 2026 | Trivy supply chain compromise | CVE-2026-33634 (Critical) | TeamPCP poisoned GitHub Actions, release binaries, and Docker Hub images; credential stealer injected into CI/CD pipelines exfiltrating cloud keys, SSH keys, K8s tokens |
| Mar 2026 | litellm PyPI supply chain attack | — | Malicious versions 1.82.7–1.82.8 published directly to PyPI bypassing normal release process; popular LLM proxy library with broad MCP ecosystem usage |
| Mar 2026 | FastMCP OAuth confused deputy | CVE-2026-27124 | Missing consent verification in OAuthProxy callback; attacker performs actions on behalf of victims via GitHub OAuth flow without explicit consent. Fixed in FastMCP 3.2.0 |
| Apr 2026 | Azure MCP Server missing auth | CVE-2026-32211 (CVSS 9.1) | `@azure-devops/mcp` shipped without authentication; API keys, auth tokens, and project data exposed to any network-reachable attacker. Mitigation guidance issued, patch pending |
| Apr 2026 | PraisonAI auth bypass | CVE-2026-34953 (CVSS 9.1) | `OAuthManager.validate_token()` returned True for any unknown token — every request treated as authenticated. Fixed in 4.5.97 |
| Mar 2026 | Nginx UI MCP endpoint auth bypass | CVE-2026-33032 (CVSS 9.8) | `/mcp_message` endpoint missing auth middleware exposes 12 MCP tools (7 destructive, 5 recon) — inject Nginx configs, reload server, intercept traffic. **Actively exploited in the wild** (Recorded Future Insikt Group, March 2026). Over 2,600 exposed instances on Shodan; Docker image exceeded 430K pulls. Patched in nginx-ui v2.3.4 (April 15, 2026) |
| Apr 2026 | Apollo MCP Server DNS rebinding | CVE-2026-35577 | Missing Host header validation on StreamableHTTP transport; DNS rebinding bypasses same-origin policy to access local MCP servers. Fixed in 1.7.0 |
| Apr 2026 | OAuth2 Proxy health check auth bypass | CVE-2026-34457 (CVSS 9.1) | When deployed with `auth_request`-style integration and `--ping-user-agent` or `--gcp-healthchecks` enabled, attacker spoofing the health check User-Agent bypasses OAuth2 authentication entirely. Fixed in 7.15.2. Relevant to MCP deployments using OAuth2 Proxy as auth gateway |
| Apr 2026 | MCPHub authentication bypass | CVE-2025-13822 (CVSS 5.3) | Endpoints missing authentication middleware allow unauthenticated attackers to perform actions as other users with their privileges. Fixed in MCPHub 0.11.0. Coordinated disclosure via CERT Polska |
| Apr 2026 | Splunk MCP Server token exposure | CVE-2026-20205 (CVSS 7.2) | Splunk MCP Server app below 1.0.3 logs session and authorization tokens in plaintext to `_internal` index; users with `_internal` access or `mcp_tool_admin` capability can read all active tokens. Requires privileged access but enables token replay and impersonation. Fixed in 1.0.3 |
| Apr 2026 | MCP Ruby SDK SSE stream hijacking | CVE-2026-33946 (CVSS 8.2) | Insufficient session binding in `streamable_http_transport.rb` allows any party with a valid session ID to hijack SSE streams and intercept all MCP communications (tool calls, resource updates, sensitive data). CWE-384 (Session Fixation) / CWE-639. Fixed in Ruby SDK 0.9.2 |
| Apr 2026 | aws-mcp-server command injection | CVE-2026-5059 (CVSS 9.8) | AWS CLI command injection — unauthenticated attackers execute arbitrary commands via unsanitized user input passed to system calls. No authentication required. Classic CWE-78 (OS Command Injection) in MCP server context |
| Apr 2026 | Agent Zero RCE via MCP config | CVE-2026-30624 (CVSS High) | External MCP Servers JSON configuration allows arbitrary `command` and `args` values; application executes user-supplied values without validation, enabling RCE through MCP server definitions |

Sources: [AuthZed Timeline](https://authzed.com/blog/timeline-mcp-breaches), [VulnerableMCP.info](https://vulnerablemcp.info/), [Doyensec MCP Nightmare](https://blog.doyensec.com/2026/03/05/mcp-nightmare.html), [Pillar Security](https://www.pillar.security/blog/operation-bizarre-bazaar-first-attributed-llmjacking-campaign-with-commercial-marketplace-monetization), [Socket SANDWORM_MODE](https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning), [Infosecurity Magazine](https://www.infosecurity-magazine.com/news/nginx-ui-mcp-flaw-actively/)

---

## MCP Auth Specification Evolution

Key changes in the **November 25, 2025** spec revision:
- **Client ID Metadata Documents (CIMD)** added as preferred client registration mechanism (adoption at ~3–4%)
- **RFC 8707 Resource Indicators** now mandatory — tokens MUST be bound to specific MCP servers
- **Token pass-through explicitly forbidden** — servers must obtain separate tokens for downstream APIs
- **Confused deputy mitigations** added for proxy servers
- **PKCE with S256 method** mandatory for all flows
- **Protected Resource Metadata (RFC 9728)** — servers respond to unauthorized requests with `WWW-Authenticate` header containing `resource_metadata` URL

**Upcoming in 2026 roadmap** (updated March 5, 2026; next spec release tentatively June 2026). Note: the official roadmap classifies Security & Authorization (including DPoP and Workload Identity) as "On the Horizon" — not a top-tier priority this cycle, but with active community proposals. An Enterprise WG is expected to form to own enterprise-managed auth, gateway patterns, and configuration portability:
- **SEP-1932 (DPoP)** — Demonstration of Proof-of-Possession, binding tokens to client key pairs. As of April 2026, the proposal has been refined to use DPoP "out-of-the-box" (no custom MCP extensions), with clarified replay protection using AEAD-encrypted nonces for stateless servers
- **SEP-1933 (Workload Identity Federation)** — Cloud-native identity (AWS IAM, GCP Workload Identity, Azure Managed Identity) without static secrets
- **SEP-1442 (Stateless Transport)** — Shifting MCP from stateful sessions toward stateless requests, which will affect session-based auth patterns and simplify gateway-level enforcement
- **SEP-991 (CIMD)** — becoming recommended default for client registration
- **SEP-2127 (Server Cards)** — standardized server discovery mechanism
- **SEP-1299** — server-side authorization management using HTTP Message Signatures

**2026-03-26 spec revision** (cumulative changes):
- **MCP servers formally classified as OAuth 2.0 Resource Servers** — must publish `/.well-known/oauth-protected-resource` metadata
- **RFC 8707 Resource Indicators mandatory for clients** — `resource` parameter required in token requests, binding tokens to specific MCP servers
- **Incremental scope consent** — clients can request minimum necessary access per operation
- **Dynamic Client Registration (RFC 7591/7592)** emphasized as the preferred registration path to reduce manual onboarding

**Enterprise extensions:**
- **Okta Cross App Access (XAA)** incorporated as the MCP "Enterprise-Managed Authorization" extension — enterprise IdP verifies agent authorization against centralized policies. **Okta for AI Agents reached GA on April 30, 2026**, with Agent Gateway (centralized control plane), agent discovery including shadow agent detection, virtual MCP server aggregating tools from Okta's MCP registry, privileged credential management with automatic rotation, and universal logout "kill switch" for instant agent revocation. 88% of organizations now report suspected AI agent security incidents (Okta Showcase 2026).

---

## MCP Auth Tooling Landscape

| Tool | Type | Key Capability | Source |
|------|------|---------------|--------|
| [Kong AI Gateway MCP Tool ACLs](https://konghq.com/blog/product-releases/mcp-tool-acls-ai-gateway) (v3.13, Jan 2026) | Commercial gateway | First production per-tool authorization; default-deny YAML ACLs; OAuth2 plugin | Kong |
| [Traefik Hub TBAC](https://doc.traefik.io/traefik-hub/mcp-gateway/guides/understanding-tbac) (Early Access, GA Apr 2026) | Commercial gateway | Task-Based Access Control: parameter-level authorization across 3 dimensions (Task/Tool/Transaction) | Traefik |
| [Azure APIM MCP Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690) | Commercial gateway | Native Entra ID integration; OBO token exchange; full OAuth 2.0/PKCE flow | Microsoft |
| [AWS Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) | Commercial gateway | First hyperscaler-native MCP gateway; JWT bearer token validation with scope/audience/client enforcement; fine-grained interceptors for tool-level + argument-level access control; RFC 9728 Protected Resource Metadata; 3LO outbound OAuth with Token Vault; IAM SigV4 fallback | AWS |
| [Cisco AI Defense MCP Catalog](https://blogs.cisco.com/ai/securing-the-ai-agent-supply-chain-with-ciscos-open-source-mcp-scanner) | Commercial + OSS | MCP server discovery/inventory; runtime agent threat detection; MCP Scanner (YARA + LLM + API) | Cisco |
| [IBM ContextForge](https://github.com/IBM/mcp-context-forge) | OSS gateway | Multi-protocol federation (MCP + A2A + REST/gRPC); JWT/OAuth/RBAC; 3.5K stars | IBM |
| [MCPTox](https://arxiv.org/abs/2508.14925) | Benchmark | Tool poisoning benchmark; 20 agents, 45 servers, 353 tools | Research |
| [MindGuard](https://arxiv.org/html/2508.20412v1) | Guardrail | Decision-level guardrail; 94–99% precision on poisoned invocations | Research |
| [MCP Auth library](https://mcp-auth.dev/docs) | OSS library | OAuth 2.1 per MCP spec 2025-06-18 | Community |
| [CSA mcpserver-audit](https://github.com/ModelContextProtocol-Security/mcpserver-audit) | OSS scanner | Static analysis; AIVSS scoring; CWE mapping; CSA-backed | CSA |
| [Aembit Workload IAM](https://aembit.io/) | Commercial platform | Non-human identity management for MCP; infrastructure-asserted identity (K8s, AWS IAM, Azure MI); Auth0 integration for workload-to-workload auth. MCP Identity Gateway exchanges agent access tokens for server credentials without exposing secrets to the agent | Aembit |
| [Bifrost](https://www.getmaxim.ai/articles/top-5-mcp-gateways-in-2026-3/) (Maxim AI) | OSS gateway | Go-based; SSO with Google/GitHub; HashiCorp Vault integration; hierarchical budget controls | Maxim AI |
| [MCP OAuth Gateway](https://github.com/atrawog/mcp-oauth-gateway) | OSS auth proxy | Drop-in OAuth 2.1 authorization server for any MCP server without code modification; RFC 7591/7592 compliant; PKCE mandatory | Community |
| [Auth0 MCP Integration](https://auth0.com/ai/docs/mcp/intro/overview) | Commercial IdP | Secure MCP with Auth0 as authorization server; PKCE + OAuth 2.1; tenant-level isolation | Okta/Auth0 |
| [Gopher Security](https://www.gopher.security/mcp-security/mcp-security-checklist-owasp-best-practices) | Commercial platform | On-demand MCP servers and gateways with enterprise security; OWASP-aligned security checklist | Gopher |
| [MCP Gateway Registry](https://github.com/agentic-community/mcp-gateway-registry) | OSS gateway + registry | Enterprise MCP Gateway with Keycloak/Entra OAuth integration; dynamic tool discovery; unified access for autonomous agents and AI coding assistants | Community |
| [Okta Agent Gateway](https://www.okta.com/newsroom/press-releases/showcase-2026/) | Commercial IdP | Centralized agent control plane; shadow agent detection; virtual MCP server with tool aggregation; privileged credential rotation; universal logout kill switch. GA April 30, 2026 | Okta |
| [Gravitee MCP Proxy](https://www.gravitee.io/blog/mcp-proxy-unified-governance-for-agents-tools) (v4.10, Jan 2026) | Commercial gateway | MCP-aware proxy with method-level inspection (tools/list, tool/call); MCP ACL policy for per-tool authorization; [OpenFGA/AuthZen integration](https://www.gravitee.io/blog/mcp-authorization-with-openfga-and-authzen) for relationship-based access control with runtime context evaluation and decision traceability | Gravitee |
| [TrueFoundry MCP Gateway](https://www.truefoundry.com/mcp-gateway) | Commercial gateway | Managed MCP gateway with built-in auth, rate limiting, and observability for enterprise AI deployments | TrueFoundry |
| [Descope Agentic Identity Hub 2.0](https://www.descope.com/use-cases/ai) (Jan 2026) | Commercial IdP | Purpose-built MCP auth: per-agent and per-tool authorization scopes, hardened DCR with CIMD, credential vault with 50+ connection templates, tenant isolation for B2B, user consent flows, comprehensive agent audit/logging | Descope |
| [Oso](https://www.osohq.com/learn/authorization-for-ai-agents-mcp-oauth-21) | Commercial policy engine | Policy-as-code authorization for MCP using Polar language; supports RBAC, ReBAC, and ABAC simultaneously; evaluates tool-level and resource-level access per OAuth token identity; centralizes authorization logic outside MCP server code | Oso |
| [Solo Enterprise agentgateway](https://www.solo.io/blog/solo-enterprise-for-agentgateway-2-3-aws-bedrock-agentcore-intelligent-failover-and-deeper-mcp-control) (v2.3, Apr 2026) | Commercial gateway | Route-level MCP auth combining JWT claims with rate limiting and authorization policies; On-Behalf-Of token exchange with claim propagation to AgentCore; JWT pass-through with SigV4 for AWS; explicit fail-open/fail-closed policy modes; OpenAPI-backed MCP tool discovery | Solo.io |
| [Portkey MCP Gateway](https://portkey.ai/features/mcp) | Commercial gateway | Centralized MCP control plane with OAuth 2.1, JWT validation, and API key auth; tool-level and action-level authorization scoped to orgs/teams/individuals; [Lasso Security partnership](https://portkey.ai/blog/securing-mcp-to-deliver-enterprise-grade-agentic-ai-protection/) (Feb 2026) adds real-time guardrails and threat detection at sub-50ms latency; SOC 2 compliant; SaaS, VPC, or self-hosted | Portkey/Lasso |
| [Strata Maverics](https://www.strata.io/agentic-identity-sandbox/securing-mcp-servers-at-scale-how-to-govern-ai-agents-with-an-enterprise-identity-fabric/) | Commercial identity fabric | AI Identity Gateway with DPoP and RFC 8693 token exchange enforced by default; dynamic agent identity creation/retirement bound to task lifecycle; progressive scope reduction across delegation chains; vendor-agnostic identity orchestration across multiple IdPs | Strata |

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
| MCP07 | Insufficient Authentication & Authorization | 10.2.1, 10.2.2, 10.2.7, 10.2.13 |
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

## Non-Human Identity & Workload Authentication

A recurring theme across MCP auth vulnerabilities is the conflation of human identity with agent/workload identity. In MCP ecosystems, every request originates from a non-human entity — an agent, server, or tool — yet the OAuth 2.1 framework was designed primarily for human-delegated authorization flows. This creates several structural challenges:

**The PKCE-only gap.** PKCE (RFC 7636) is mandatory in MCP's OAuth 2.1 profile, but it only prevents authorization code interception — it does not authenticate the client itself. Any process that can initiate a PKCE flow can obtain tokens. The MCP spec intentionally leaves client authentication methods undefined, creating a window where unauthorized processes can impersonate legitimate clients.

**Infrastructure-asserted identity.** The emerging answer is to bind MCP client/server identity to infrastructure attestation rather than shared secrets:
- **AWS IAM Roles** for Lambda-hosted MCP servers (no static credentials)
- **Azure Managed Identity** for Azure-hosted servers (leveraged by Azure APIM MCP Gateway)
- **Kubernetes ServiceAccount Tokens** for containerized deployments
- **GCP Workload Identity Federation** for Google Cloud environments

**Workload IAM platforms.** Aembit is the first product applying dedicated non-human identity management to MCP ecosystems, using trust providers (K8s ServiceAccounts, cloud instance identity, GitHub OIDC) to attest workload identity without distributing secrets. Their Auth0 integration enables workload-to-workload authorization chains. As of April 2026, **Strata Maverics** is the first identity fabric to operationalize DPoP and RFC 8693 token exchange by default for agent-to-server flows, with dynamic identity creation bound to task lifecycle — identities are created on demand, scoped to the delegation chain, and retired when the task completes, eliminating lingering credential risk.

**Enterprise identity convergence.** As of March 2026, 95% of organizations cite identity concerns around AI agents (Corbado 2026 CIAM survey). The emerging enterprise stack looks like:
1. **Transport layer:** mTLS with infrastructure-asserted certificates
2. **Authorization layer:** OAuth 2.1 with RFC 8707 resource indicators
3. **Delegation layer:** RFC 8693 Token Exchange for agent-to-agent chains
4. **Policy layer:** Okta XAA or Azure Entra ID for centralized agent policy enforcement
5. **Attestation layer:** Workload identity federation (SEP-1933) or platform-native identity

**IETF standardization.** The IETF published **draft-klrc-aiagent-auth-00** (March 2, 2026), a 26-page framework composing WIMSE, SPIFFE, and OAuth 2.0 into the AIMS (Agent Identity Management System) model. Key principles: every agent gets exactly one WIMSE identifier (which may be a SPIFFE ID in the form `spiffe://<trust-domain>/<path>`), credentials must be short-lived with explicit expiration, and static API keys are explicitly rejected. The framework defines two application-layer proof mechanisms — Workload Proof Tokens (WPT) for proof-of-possession JWTs bound to message context, and HTTP Message Signatures (RFC 9421) for request/response integrity. A companion draft, **draft-ietf-oauth-spiffe-client-auth-01**, defines OAuth SPIFFE Client Authentication for workload-to-authorization-server flows. These drafts signal that the IETF OAuth WG considers agent identity a first-class concern.

**Agent Identity Protocol (AIP).** A March 2026 paper (arXiv 2603.24775) proposes Invocation-Bound Capability Tokens (IBCTs) using Ed25519 signatures with append-only delegation chains. Compact mode produces a 356-byte signed JWT for single-hop calls (verified in 0.049ms in Rust). Chained mode uses Biscuit tokens with Datalog policies where each intermediary appends a signed block that can only *narrow* granted scope — any attempt to widen capabilities fails cryptographic verification. In adversarial testing across 600 attacks, AIP achieved 100% rejection, catching depth-violation and audit-evasion attacks that standard JWT deployments missed.

**RSAC 2026 announcements.** IBM, Auth0, and Yubico demonstrated a Human-in-the-Loop framework combining CIBA-based identity flows with hardware-backed YubiKey authentication for high-stakes agent actions. Yubico and Delinea partnered on hardware-attested Role Delegation Tokens (RDTs) — agents reaching sensitive decision points require a human sponsor to sign an RDT envelope with a YubiKey before proceeding. The consensus emerging from RSAC: agents need "digital passports" — Ed25519 keypairs, DIDs, and trust graphs that work across platforms and organizational boundaries.

**NIST AI Agent Standards Initiative** (launched February 17, 2026) is the first federal effort to standardize agent identity. Their recommended approach: assign each agent a unique identifier and capability declaration, implement JWT-based delegation chains with diminishing permissions, and deploy unified audit logs integrating A2A communication and MCP tool call records. The companion NCCoE concept paper calls for cryptographic bindings at each delegation step and transitively-limited trust boundaries. The NCCoE concept paper comment period closed on **April 2, 2026** — feedback is now informing project planning activities, including whether NCCoE launches a formal laboratory demonstration project using commercially available technologies. In April 2026, NIST is hosting **sector-specific listening sessions** on barriers to AI agent adoption in healthcare, finance, and education, which may directly shape sector guidance for regulated industries. The concept paper specifically calls out OAuth and OpenID Connect as candidate protocols for agent identity, alongside SCIM for identity lifecycle management. Formal guidance is expected mid-2026.

---

## Implementation Maturity

| Area | Maturity | Notes |
|------|----------|-------|
| OAuth 2.1 adoption in MCP servers | **Low** | Only 8.5% of ~20K surveyed servers use OAuth; 53% use static API keys (Astrix 2025). CVE-2026-33032 (Nginx UI, CVSS 9.8) shows even MCP integrations in infrastructure management tools ship with unauthenticated endpoints. |
| Token validation (iss/aud/exp/scope) | **Medium** | Straightforward for OAuth-enabled servers, but most aren't OAuth-enabled. |
| Per-tool authorization | **Low–Medium** | Kong MCP Tool ACLs (GA Jan 2026) is the first production implementation. |
| Argument-level authorization | **Low–Medium** | Traefik TBAC (EA March 2026), Gravitee MCP Proxy (OpenFGA/AuthZen), Oso (Polar policy-as-code), and Portkey (action-level constraints scoped to orgs/teams) now offer relationship-based and parameter-level authorization. Solo agentgateway v2.3 adds JWT claim-based transformations that enable argument-level policy enforcement at the route level. |
| MCP server registry / discovery | **Low** | Cisco AI Defense MCP Catalog and IBM ContextForge are first movers. SEP-2127 proposes standard. |
| MCP gateway enforcement | **Medium–High** | Kong, Traefik, Azure APIM, IBM ContextForge, AWS AgentCore Gateway, Okta Agent Gateway, Gravitee MCP Proxy, MCP Gateway Registry, TrueFoundry, Solo agentgateway (v2.3, route-level auth with OBO token exchange), and Portkey (Lasso Security integration for runtime threat detection) now provide centralized auth. The AAIF MCP Dev Summit confirmed gateway-as-control-plane as the dominant enterprise architecture. |
| Dynamic client registration (CIMD) | **Low–Medium** | ~3–4% adoption but growing. 2026-03-26 spec emphasizes DCR (RFC 7591/7592) as preferred path. SEP-991 making progress. |
| Multi-agent delegation (RFC 8693) | **Low** | Token Exchange is the recommended pattern but production implementations are rare. |
| Security scanning | **Medium** | Cisco MCP Scanner (854 stars), CSA mcpserver-audit, VulnerableMCP.info tracking CVEs. |
| Non-human identity management | **Low–Medium** | Aembit, Okta Agent Gateway (GA April 30, 2026), and Descope Agentic Identity Hub 2.0 (January 2026) all treat agents as first-class identities with discovery, credential rotation, per-tool scopes, and universal logout. Descope adds hardened DCR with CIMD and 50+ prebuilt connection templates. NIST hosting sector-specific listening sessions (healthcare, finance, education) in April 2026 to shape agent identity guidance. IETF draft-klrc-aiagent-auth-00 provides the composable framework. 88% of organizations report suspected AI agent security incidents (Okta Showcase 2026). |
| Proof-of-possession (DPoP/mTLS) | **Very Low** | SEP-1932 (DPoP for MCP) is under active refinement — simplified to use DPoP out-of-the-box with AEAD-encrypted nonces for stateless replay protection — but no MCP implementation ships DPoP natively yet. Strata Maverics is the first product to operationalize DPoP and RFC 8693 token exchange by default for agent identity, with dynamic identity lifecycle binding. mTLS is available at transport layer but breaks through intermediaries. AIP paper proposes Ed25519-based IBCTs with 100% adversarial rejection but is pre-implementation. |
| Drop-in OAuth gateways | **Medium** | MCP OAuth Gateway (OSS), Auth0 MCP, Descope Agentic Identity Hub 2.0, Gopher Security, and Bifrost provide turnkey OAuth 2.1 for servers without code changes. The AAIF MCP Dev Summit (April 2026) confirmed gateway-as-control-plane as the dominant enterprise architecture pattern. Adoption growing rapidly. |

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
- [NIST AI Agent Standards Initiative (February 2026)](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)
- [NCCoE: Accelerating Adoption of Software and AI Agent Identity and Authorization (February 2026)](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)
- [Aembit: MCP, OAuth 2.1, PKCE, and the Future of AI Authorization](https://aembit.io/blog/mcp-oauth-2-1-pkce-and-the-future-of-ai-authorization/)
- [CVE-2026-26118: Azure MCP Server SSRF for Privilege Elevation](https://www.thehackerwire.com/azure-mcp-server-ssrf-for-privilege-elevation-cve-2026-26118/)
- [Auth0: Secure MCP Integration](https://auth0.com/ai/docs/mcp/intro/overview)
- [MCP OAuth Gateway (OSS)](https://github.com/atrawog/mcp-oauth-gateway)
- [MCP Security Best Practices (Official)](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [MCP Authorization Tutorial (Official)](https://modelcontextprotocol.io/docs/tutorials/security/authorization)
- [Gopher Security: MCP Security Checklist](https://www.gopher.security/mcp-security/mcp-security-checklist-owasp-best-practices)
- [AWS Bedrock AgentCore Gateway — OAuth Authentication](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html)
- [AWS Bedrock AgentCore Gateway — Fine-Grained Access Control with Interceptors](https://aws.amazon.com/blogs/machine-learning/apply-fine-grained-access-control-with-bedrock-agentcore-gateway-interceptors/)
- [CVE-2026-32111: ha-mcp OAuth Beta SSRF](https://dailycve.com/ha-mcp-oauth-beta-server-side-request-forgery-ssrf-cve-2026-32111-medium/)
- [NCCoE: Software and AI Agent Identity and Authorization Project](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization)
- [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://datatracker.ietf.org/doc/html/rfc9449)
- [SEP-1932: DPoP Profile for MCP (PR)](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1932)
- [SEP-1461: Attested Client Registration and Proof-of-Possession (closed)](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1461)
- [IETF draft-klrc-aiagent-auth-00: AI Agent Authentication and Authorization (March 2026)](https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/)
- [IETF draft-ietf-oauth-spiffe-client-auth-01: OAuth SPIFFE Client Authentication](https://datatracker.ietf.org/doc/draft-ietf-oauth-spiffe-client-auth/)
- [Agent Identity Protocol (AIP): Verifiable Delegation Across MCP and A2A (arXiv 2603.24775)](https://arxiv.org/html/2603.24775)
- [Obsidian Security: The Bearer Token Problem Inside Your AI Agent Strategy](https://www.obsidiansecurity.com/blog/the-bearer-token-problem-hidden-inside-your-ai-agent-strategy)
- [Strata.io: Agent Credential Replay — Why Bearer Tokens Are Digital Cash in a Tornado](https://www.strata.io/blog/agentic-identity/agent-credential-replay/)
- [Teleport: Machine & Workload Identity Solution](https://goteleport.com/platform/machine-and-workload-identity/)
- [CVE-2026-32211: Azure MCP Server Missing Authentication (CVSS 9.1)](https://cvefeed.io/vuln/detail/CVE-2026-32211)
- [CVE-2026-34953: PraisonAI Authentication Bypass (CVSS 9.1)](https://www.thehackerwire.com/praisonai-authentication-bypass-grants-full-access-cve-2026-34953/)
- [CVE-2026-27124: FastMCP OAuth Confused Deputy](https://github.com/PrefectHQ/fastmcp/security/advisories/GHSA-rww4-4w9c-7733)
- [CVE-2026-35577: Apollo MCP Server DNS Rebinding Auth Bypass](https://www.sentinelone.com/vulnerability-database/cve-2026-35577/)
- [Okta Showcase 2026: Secure Agentic Enterprise](https://www.okta.com/newsroom/press-releases/showcase-2026/)
- [MCP Authorization Specification: OAuth 2.1 and Resource Indicators (April 2026 analysis)](https://dasroot.net/posts/2026/04/mcp-authorization-specification-oauth-2-1-resource-indicators/)
- [CVE-2026-33032: Nginx UI Unauthenticated MCP Endpoint (CVSS 9.8)](https://cvefeed.io/vuln/detail/CVE-2026-33032)
- [CVE-2026-34457: OAuth2 Proxy Health Check Auth Bypass (CVSS 9.1)](https://www.thehackerwire.com/oauth2-proxy-critical-auth-bypass-via-health-check-user-agent-cve-2026-34457/)
- [Gravitee MCP Proxy: Unified Governance for Agent Tools](https://www.gravitee.io/blog/mcp-proxy-unified-governance-for-agents-tools)
- [Gravitee MCP Authorization with OpenFGA and AuthZen](https://www.gravitee.io/blog/mcp-authorization-with-openfga-and-authzen)
- [Aembit: The Ultimate Guide to MCP Security Vulnerabilities (2026)](https://aembit.io/blog/the-ultimate-guide-to-mcp-security-vulnerabilities/)
- [MCP Gateway Registry (OSS): Enterprise Gateway with Keycloak/Entra](https://github.com/agentic-community/mcp-gateway-registry)
- [Descope Agentic Identity Hub 2.0: MCP Auth with Per-Tool Scopes and Credential Vault](https://www.descope.com/use-cases/ai)
- [Descope: Diving Into the MCP Authorization Specification](https://www.descope.com/blog/post/mcp-auth-spec)
- [Oso: Authorization for MCP — OAuth 2.1, PRMs, and Best Practices](https://www.osohq.com/learn/authorization-for-ai-agents-mcp-oauth-21)
- [AAIF MCP Dev Summit North America 2026: Gateways, gRPC, and Observability (InfoQ)](https://www.infoq.com/news/2026/04/aaif-mcp-summit/)
- [CVE-2025-13822: MCPHub Authentication Bypass (CVSS 5.3)](https://cert.pl/en/posts/2026/04/CVE-2025-13822/)
- [CVE-2026-20205: Splunk MCP Server Token Exposure (CVSS 7.2)](https://www.tenable.com/cve/CVE-2026-20205)
- [Solo Enterprise agentgateway 2.3: Route-Level MCP Auth with OBO Token Exchange](https://www.solo.io/blog/solo-enterprise-for-agentgateway-2-3-aws-bedrock-agentcore-intelligent-failover-and-deeper-mcp-control)
- [Portkey MCP Gateway: Centralized Auth with Lasso Security Partnership](https://portkey.ai/features/mcp)
- [Strata Maverics: AI Identity Gateway with DPoP and Token Exchange](https://www.strata.io/agentic-identity-sandbox/securing-mcp-servers-at-scale-how-to-govern-ai-agents-with-an-enterprise-identity-fabric/)
- [Strata: Agent Credential Replay — Why Bearer Tokens Are Digital Cash in a Tornado](https://www.strata.io/blog/agentic-identity/agent-credential-replay/)
- [CVE-2026-33946: MCP Ruby SDK SSE Stream Hijacking (CVSS 8.2)](https://rubysec.com/advisories/CVE-2026-33946/)
- [CVE-2026-5059: aws-mcp-server Command Injection RCE (CVSS 9.8)](https://nvd.nist.gov/vuln/detail/CVE-2026-5059)
- [CVE-2026-30624: Agent Zero RCE via MCP Server Configuration](https://www.thehackerwire.com/agent-zero-0-9-8-rce-via-external-mcp-servers-configuration/)
- [Nginx UI CVE-2026-33032 Active Exploitation (Infosecurity Magazine)](https://www.infosecurity-magazine.com/news/nginx-ui-mcp-flaw-actively/)
- [WorkOS: Securing Agentic Apps — MCP Supply Chain Security](https://workos.com/blog/mcp-supply-chain-security)

---

## Open Research Questions

- What is the right OAuth scope granularity for MCP — per-tool, per-resource-type, or per-action? Traefik TBAC proposes a three-layer model but no standard exists.
- How should argument-level authorization be modeled — ABAC, RBAC, or policy-as-code? Neither AuthZed nor OPA has MCP-native integrations yet.
- Is OAuth Token Exchange (RFC 8693) viable across diverse IdPs for multi-agent delegation chains? Okta XAA is the first major integration.
- How do you handle consent for dynamically registered MCP clients given CIMD adoption is at 3–4%?
- Will DPoP (SEP-1932) and Workload Identity Federation (SEP-1933) address the token theft and static credential problems at scale?
- Can MCP gateways (Kong, Traefik, Azure APIM) become the standard enforcement point, or will auth need to be embedded in every server?
- How should organizations close the 8.5% OAuth adoption gap given 53% of servers still use static API keys?
- Since PKCE does not authenticate the client, what is the right mechanism for MCP client identity assertion? Infrastructure-attested identity (cloud IAM, K8s tokens) or certificate-based authentication (mTLS)?
- How will NIST's AI Agent Standards Initiative interact with the MCP specification process — will NIST publish binding guidance or defer to the MCP community?
- Can drop-in OAuth gateways (MCP OAuth Gateway, Bifrost) achieve meaningful adoption fast enough to close the 91.5% non-OAuth gap before the next wave of MCP exploitation?
- As CVE-2026-26118 and CVE-2026-32111 demonstrate, SSRF remains the dominant auth-adjacent vulnerability class in MCP servers — should MCP servers run with minimal cloud IAM permissions, or should managed identity tokens be bound to specific request contexts?
- AWS AgentCore Gateway interceptors offer tool-level and argument-level access control — will the interceptor pattern (gateway-side policy enforcement) emerge as the standard architecture, or will per-server embedded authorization remain necessary for edge deployments?
- The Trivy and litellm supply chain compromises (March 2026) exposed CI/CD credentials at scale — how should MCP servers deployed in pipeline environments handle credential isolation given that build-time secrets are routinely available to running processes?
- With SEP-1932 (DPoP) still in review and SEP-1461 (hardware attestation) closed, what is the realistic path to proof-of-possession in MCP? Will DPoP adoption require gateway-level enforcement (as with OAuth 2.1), or can it be embedded in MCP SDKs?
- The IETF AIMS framework (draft-klrc-aiagent-auth-00) composes WIMSE/SPIFFE/OAuth without new protocols — is this composable approach sufficient, or do multi-agent delegation chains need purpose-built tokens like AIP's Invocation-Bound Capability Tokens?
- CVE-2026-27124 (FastMCP) and CVE-2026-35577 (Apollo) show that confused deputy and DNS rebinding attacks are widening the OAuth attack surface in MCP — are current OAuth libraries providing sufficient guardrails against these implementation-level failures?
- Gravitee's OpenFGA/AuthZen integration introduces relationship-based access control for MCP tools — is ReBAC a better fit than RBAC or ABAC for MCP authorization, given that agent-tool relationships are dynamic and context-dependent?
- CVE-2026-33032 (Nginx UI) and CVE-2026-34457 (OAuth2 Proxy) demonstrate that MCP endpoints embedded in infrastructure management tools and auth proxies introduce unexpected bypass paths — should MCP implementations mandate endpoint-level authentication independent of host application auth?
- With the 2026-03-26 spec formally classifying MCP servers as OAuth Resource Servers and mandating RFC 8707, what percentage of existing servers will need architectural changes to comply?
- Okta's Agent Gateway and universal logout "kill switch" introduced the concept of instant agent revocation — should MCP specify a standard revocation mechanism for agent sessions, or is IdP-level revocation sufficient?
- SEP-1442's shift toward stateless requests fundamentally changes session-based auth — how will this affect session token binding (10.2.8), deterministic teardown (10.2.12), and gateway-level enforcement patterns?
- Policy-as-code engines (Oso/Polar, OPA/Rego, OpenFGA) are now entering the MCP authorization space — is declarative policy the right abstraction for tool-level and argument-level authorization, and can it keep up with the dynamic nature of agent-tool relationships?
- CVE-2026-33946 (Ruby SDK) and CVE-2026-25536 (TypeScript SDK) demonstrate that session-identity conflation is systemic across MCP SDK implementations — should the MCP spec mandate explicit session ownership verification beyond session ID validity, and should SDK test suites include session hijacking regression tests?
- CVE-2026-33032 becoming the first MCP-related CVE with confirmed active exploitation raises the question: is MCP attack surface now mature enough to attract organized threat actors, and should MCP servers be treated as attack targets on par with traditional web application endpoints?

---

## Related Pages

- **ASVS V10 (Secrets & Key Management)** — Credential storage, rotation, and HSM-backed key management directly relevant to MCP token and API key lifecycle (CVE-2026-20205 shows what happens when tokens leak to logs). AISVS C4 no longer duplicates generic secrets-management controls.
- **[C05-01 Identity Management & Authentication](C05-01-Identity-Management-Authentication.md)** — Foundational identity infrastructure that MCP auth builds on: centralized identity, MFA, and federated agent authentication
- **[C09-06 Authorization & Delegation](C09-06-Authorization-and-Delegation.md)** — Scoped capability tokens and per-action policy evaluation for agents — the authorization layer that complements MCP's OAuth transport
- **[C09-03 Tool & Plugin Isolation](C09-03-Tool-and-Plugin-Isolation.md)** — Sandbox isolation for agent tools overlaps with MCP auth: tool manifests, MCP supply chain attacks, and tiered isolation that complements auth controls
- **[C09-06 Authorization & Delegation](C09-06-Authorization-and-Delegation.md)** — Multi-agent delegation chains, credential isolation, and inter-agent peer authorization patterns referenced by RFC 8693 and Okta XAA

---

[C10 Index](C10-MCP-Security.md) | [README](README.md)
