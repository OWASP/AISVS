# C10.6: Transport Restrictions & High-Risk Boundary Controls

> **Parent:** [C10 MCP Security](C10-MCP-Security)
> **Requirements:** 3 | **IDs:** 10.6.1–10.6.3

## Purpose

This section addresses high-risk deployment patterns and boundary controls that are difficult to implement but critical for security-sensitive environments. These are Level 3 requirements — they represent defense-in-depth measures for organizations with elevated threat models. The section covers three distinct but related concerns: restricting stdio transport to safe contexts, preventing dynamic dispatch of tool functions, and enforcing tenant/environment isolation at the MCP layer. These controls are particularly relevant for multi-tenant SaaS platforms, financial services, healthcare, and government deployments where boundary violations have regulatory or safety consequences.

The emergence of MCP gateways in 2025-2026 (with 10+ commercial products by early 2026, including offerings from Composio, MintMCP, Gravitee, Cloudflare, Pomerium, and others) has made several of these controls more practical to implement. MCP gateways act as centralized security boundaries between AI applications and external MCP servers, enforcing access control policies, tenant-aware routing, transport restrictions, and audit logging. Gateway architectures support tool-level RBAC at global, service, and individual tool levels while delivering low latency (~4ms p99). For multi-tenant deployments, gateways provide policy scoping and identity-based access controls that ensure each tenant sees only its own resources. However, gateways also introduce a new trust boundary — the gateway itself becomes a high-value target, and misconfigured gateway policies can silently weaken isolation. These controls remain Level 3 because even with gateway support, correct implementation requires coordination across network, identity, and application layers.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.6.1** | **Verify that** stdio-based MCP transports are limited to co-located, single-process development scenarios and isolated from shell execution, terminal injection, and process-spawning capabilities; stdio must not cross network or multi-tenant boundaries. | 3 | D/V | **Shell injection and process escape via stdio transport.** Stdio-based MCP transport communicates via stdin/stdout of a child process. If the MCP server process has access to shell execution (`exec`, `spawn`, `system`), an attacker who can influence tool arguments can inject shell commands. Additionally, stdio transport inherits the parent process's environment, file system access, and network capabilities. Terminal escape sequences in tool output can manipulate the parent terminal. If stdio is used across network boundaries (e.g., via SSH tunnels or named pipes shared across containers), the attack surface expands dramatically. | Verify that stdio-based MCP servers are not deployed in production or multi-tenant environments. Review the MCP server process for shell execution capabilities and verify they are disabled or sandboxed. Test for terminal escape injection by returning ANSI escape sequences in tool output and checking whether they are rendered. Verify that stdio MCP processes cannot spawn child processes or access the network. | Level 3 because stdio is inherently insecure for anything beyond local development, but it remains the most common MCP transport due to its simplicity. The MCP spec acknowledges stdio as a first-class transport without restricting its use. Enforcing this requirement means implementing process-level sandboxing (seccomp, AppArmor, or container isolation) around stdio MCP servers, which is operationally complex. Many popular MCP servers (filesystem, database access) only support stdio transport. |
| **10.6.2** | **Verify that** MCP servers expose only allow-listed functions and resources and prohibit dynamic dispatch, reflective invocation, or execution of function names influenced by user or model-provided input. | 3 | D/V | **Arbitrary code execution via dynamic dispatch.** An MCP server uses the `method` field or tool name from the JSON-RPC request to dynamically look up and invoke a function (e.g., `server[request.method](request.params)`). An attacker who can influence the tool name (via prompt injection) can invoke any function on the server object, including internal methods not intended to be exposed — such as `__init__`, `eval`, `exec`, or framework internals. This is analogous to insecure deserialization or prototype pollution in web applications. | Review MCP server code for dynamic dispatch patterns: reflection, `eval()`, `getattr()` with unsanitized input, `require()` with user-controlled paths, or any pattern where the tool name is used to look up a function dynamically. Verify that tool dispatch uses a static map/registry of allowed functions. Test by requesting invocation of a tool name matching an internal method (e.g., `__class__`, `constructor`, `prototype`) and verify rejection. | Level 3 because this requires code-level review and secure coding practices rather than configuration. Most well-implemented MCP servers use a static tool registry (e.g., `server.tool("name", handler)` in the official SDKs), which is safe. The risk is in custom implementations or wrappers that introduce dynamic dispatch for convenience. This is a secure-coding requirement more than a protocol requirement. |
| **10.6.3** | **Verify that** tenant boundaries, environment boundaries (e.g., dev/test/prod), and data domain boundaries are enforced at the MCP layer to prevent cross-tenant or cross-environment server or resource discovery. | 3 | D/V | **Cross-tenant data exposure and environment contamination.** In multi-tenant deployments, a shared MCP server instance serves multiple tenants. Without boundary enforcement, Tenant A's agent can discover and invoke tools intended for Tenant B, access Tenant B's data through tool arguments, or connect to MCP servers in the production environment from a development context. Environment contamination (dev agent connecting to prod MCP server) can cause data leakage or unintended side effects on production data. | Verify tenant isolation by authenticating as Tenant A and attempting to: (1) discover Tenant B's MCP servers, (2) invoke Tenant B's tools, (3) access Tenant B's data through tool arguments. Verify environment isolation by attempting to connect a dev-environment MCP client to a prod-environment MCP server. Check for network-level, identity-level, and application-level boundary enforcement. | Level 3 because multi-tenant MCP isolation requires coordination across network, identity, and application layers. No standard MCP mechanism exists for tenant or environment tagging — isolation must be enforced through: (1) separate MCP server instances per tenant, (2) tenant-aware routing at the network/service-mesh layer, (3) tenant claims in OAuth tokens validated by the MCP server, and (4) environment-specific DNS or service discovery. This is architecturally complex and deployment-specific. |

---

## MCP Gateway Landscape (2025-2026)

The rapid emergence of MCP gateways has changed the practical feasibility of boundary controls. Key capabilities relevant to this section:

| Capability | Description | Relevance to C10.6 |
|---|---|---|
| **Transport policy enforcement** | Gateways can restrict which transports are permitted per environment (e.g., block stdio in production) | Directly supports 10.6.1 enforcement |
| **Tool-level RBAC** | Fine-grained access control at global, service, and individual tool levels | Supports 10.6.2 by restricting callable functions |
| **Tenant-aware routing** | Policy scoping and identity-based routing ensures each tenant's agents reach only their own MCP servers | Directly supports 10.6.3 isolation |
| **Audit logging** | Centralized logging of all tool invocations with tenant, environment, and user context | Enables verification of boundary enforcement |
| **Environment tagging** | Gateways can tag MCP connections with environment metadata (dev/staging/prod) and enforce separation | Supports 10.6.3 environment isolation |

Notable gateway products as of early 2026 include Composio, MintMCP, Gravitee, Cloudflare Agents, Pomerium, obot, and TrueFoundry, among others. The "Breaking the Protocol" research (arXiv:2601.17549) demonstrated that multi-server deployments without isolation boundaries allow cross-server propagation attacks to succeed 61.3% of the time — providing quantitative justification for the tenant isolation controls in this section.

## Related Standards & References

- [MCP Transports Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) — current stdio and streamable HTTP transport definitions
- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html) — relevant to dynamic dispatch prevention
- [CWE-470: Use of Externally-Controlled Input to Select Classes or Code](https://cwe.mitre.org/data/definitions/470.html) — dynamic dispatch vulnerability class
- [NIST SP 800-53: SC-4 Information in Shared System Resources](https://csf.tools/reference/nist-sp-800-53/r5/sc/sc-4/) — multi-tenant isolation controls
- [Linux seccomp](https://man7.org/linux/man-pages/man2/seccomp.2.html) — process-level sandboxing for stdio isolation
- [Composio: Best MCP Gateways for Developers (2026)](https://composio.dev/content/best-mcp-gateway-for-developers) — gateway comparison
- [Gravitee: MCP API Gateway Explained](https://www.gravitee.io/blog/mcp-api-gateway-explained-protocols-caching-and-remote-server-integration) — gateway architecture patterns
- [MintMCP: MCP Gateways for Platform Engineering Teams](https://www.mintmcp.com/blog/mcp-gateways-platform-engineering-teams) — multi-tenant gateway patterns
- [Breaking the Protocol (arXiv:2601.17549)](https://arxiv.org/html/2601.17549) — cross-server propagation attack data

---

## Open Research Questions

- [ ] Should the MCP spec formally deprecate stdio for anything beyond single-user local development, or add a security-level annotation to transports?
- [ ] Can static analysis tools detect dynamic dispatch patterns in MCP server implementations automatically?
- [ ] What is the minimum viable tenant isolation architecture for MCP in a multi-tenant SaaS — separate instances, shared instances with token-based isolation, or a hybrid?
- [ ] How should MCP server discovery be scoped to prevent cross-environment leakage (e.g., dev discovering prod servers via a shared registry)?
- [ ] Is there a role for hardware-level isolation (TEEs, enclaves) for high-sensitivity MCP servers handling regulated data?
- [ ] As MCP gateways become standard infrastructure, should the AISVS define gateway-specific requirements (authentication of the gateway itself, gateway-to-server mTLS, gateway configuration integrity)?
- [ ] How should gateway failover and bypass be handled — if the gateway is unavailable, should MCP connections fail closed or fall back to direct connections?

---
