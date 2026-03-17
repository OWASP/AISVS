# C10 Model Context Protocol (MCP) Security

## Control Objective

Ensure secure discovery, authentication, authorization, transport, and use of MCP-based tool and resource integrations to prevent context confusion, unauthorized tool invocation, or cross-tenant data exposure.

---

## C10.1 Component Integrity & Supply Chain Hygiene

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **10.1.1** | **Verify that** MCP server and client components are obtained only from trusted sources and verified using signatures, checksums, or secure package metadata, rejecting tampered or unsigned builds. | 1 | D/V |
| **10.1.2** | **Verify that** MCP client and server configurations do not contain plaintext secrets (API keys, tokens, client secrets) and that credentials are injected or resolved at runtime rather than stored in configuration files, environment variables, or source code. | 1 | D/V |
| **10.1.3** | **Verify that** MCP server dependencies are constrained to approved version ranges (e.g., pinned to major version) and that only allowlisted server identifiers (name and registry) are permitted in production; unlisted servers are rejected at load time. | 1 | D/V |

---

## C10.2 Authentication & Authorization

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **10.2.1** | **Verify that** MCP clients authenticate to MCP servers using the OAuth 2.1 authorization framework and present a valid OAuth access token for each request, and that the MCP server validates the token according to OAuth 2.1 resource server requirements. | 1 | D/V |
| **10.2.2** | **Verify that** MCP servers validate OAuth access tokens including issuer, audience, expiration, and scope claims, ensuring that tokens were issued for the specific MCP server before allowing tool invocation. | 1 | D/V |
| **10.2.3** | **Verify that** MCP servers are registered through a controlled technical onboarding mechanism requiring explicit owner, environment, and resource definitions; unregistered or undiscoverable servers must not be callable in production. | 1 | D/V |
| **10.2.4** | **Verify that** authorization decisions at the MCP layer are enforced by the MCP server's policy logic, and that model-generated output cannot influence, override, or bypass access control checks. | 1 | D/V |
| **10.2.5** | **Verify that** MCP servers act as OAuth 2.1 resource servers only by validating tokens issued by external authorization servers and by not storing tokens or user credentials. | 2 | D/V |
| **10.2.6** | **Verify that** MCP `tools/list` and resource discovery responses are filtered based on the end-user's authorized scopes so that agents receive only the tool and resource definitions the user is permitted to invoke. | 2 | D/V |
| **10.2.7** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 | D/V |
| **10.2.8** | **Verify that** MCP session identifiers are treated as state, not identity: generated using cryptographically secure random values, bound to the authenticated user, and never relied on for authentication or authorization decisions. | 1 | D/V |
| **10.2.9** | **Verify that** MCP servers do not pass through access tokens received from clients to downstream APIs and instead obtain a separate token scoped to the server's own identity (e.g., via on-behalf-of or client credentials flow). | 2 | D/V |
| **10.2.10** | **Verify that** MCP servers acting as OAuth proxies to third-party APIs enforce per-client consent before forwarding authorization requests, preventing cached approvals from being reused across dynamically registered clients. | 2 | D/V |
| **10.2.11** | **Verify that** MCP clients request only the minimum scopes needed for the current operation, elevate progressively via step-up authorization, and that servers reject wildcard or overly broad scopes. | 2 | D/V |
| **10.2.12** | **Verify that** MCP servers enforce deterministic session teardown, destroying cached tokens, in-memory state, temporary storage, and file handles when a session terminates, disconnects, or times out. | 2 | D/V |

---

## C10.3 Secure Transport & Network Boundary Protection

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **10.3.1** | **Verify that** authenticated, encrypted streamable-HTTP is used as the primary MCP transport in production environments and that alternate transports (e.g., stdio or SSE) are restricted to local or tightly controlled environments with explicit justification. | 2 | D/V |
| **10.3.2** | **Verify that** streamable-HTTP MCP transports use authenticated, encrypted channels (TLS 1.3 or later) with certificate validation. | 2 | D/V |
| **10.3.3** | **Verify that** SSE-based MCP transports are used only within private, authenticated internal channels and enforce TLS, authentication, schema validation, payload size limits, and rate limiting; SSE endpoints must not be exposed to the public internet. | 2 | D/V |
| **10.3.4** | **Verify that** MCP servers validate the `Origin` and `Host` headers on all HTTP-based transports (including SSE and streamable-HTTP) to prevent DNS rebinding attacks and reject requests from untrusted, mismatched, or missing origins. | 2 | D/V |
| **10.3.5** | **Verify that** intermediaries do not alter or remove the `Mcp-Protocol-Version` header on streamable-HTTP transports unless explicitly required by the protocol specification, preventing protocol downgrade via header stripping. | 2 | D/V |

---

## C10.4 Schema, Message, and Input Validation

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **10.4.1** | **Verify that** MCP tool responses are validated before being injected into the model context to prevent prompt injection, malicious tool output, or context manipulation. | 1 | D/V |
| **10.4.2** | **Verify that** MCP tool and resource schemas (e.g., JSON schemas or capability descriptors) are validated for authenticity and integrity using signatures to prevent schema tampering or malicious parameter modification. | 2 | D/V |
| **10.4.3** | **Verify that** all MCP transports enforce message-framing integrity, strict schema validation, maximum payload sizes, and rejection of malformed, truncated, or interleaved frames to prevent desynchronization or injection attacks. | 2 | D/V |
| **10.4.4** | **Verify that** MCP servers perform strict input validation for all function calls, including type checking, boundary validation, enumeration enforcement, and rejection of unrecognized or oversized parameters. | 2 | D/V |
| **10.4.5** | **Verify that** MCP clients maintain a hash or versioned snapshot of tool definitions and that any change to a tool definition (via `notifications/tools/list_changed` or between sessions) triggers re-approval before the modified tool can be invoked. | 2 | D/V |
| **10.4.6** | **Verify that** MCP server error and exception responses do not expose stack traces, internal file paths, tokens, or tool implementation details to the client or model context. | 1 | D/V |
| **10.4.7** | **Verify that** MCP implementations reject JSON-RPC messages containing duplicate keys at any nesting level, preventing parser disagreement where different components resolve the same message to different values. | 2 | D/V |
| **10.4.8** | **Verify that** intermediaries evaluating message content either forward the canonicalized representation they evaluated or reject messages where multiple byte representations could produce different parsed structures. | 3 | D/V |

---

## C10.5 Outbound Access & Agent Execution Safety

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **10.5.1** | **Verify that** MCP servers may only initiate outbound requests to approved internal or external destinations following least-privilege egress policies and cannot access arbitrary network targets or internal cloud metadata services. | 2 | D/V |
| **10.5.2** | **Verify that** outbound MCP actions implement execution limits (e.g., timeouts, recursion limits, concurrency caps, or circuit breakers) to prevent unbounded agent-driven tool invocation or chained side effects. | 2 | D/V |
| **10.5.3** | **Verify that** MCP tool invocations classified as high-risk or destructive (e.g., data deletion, financial transactions, system configuration changes) require explicit user confirmation before execution. | 2 | D/V |

---

## C10.6 Transport Restrictions & High-Risk Boundary Controls

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **10.6.1** | **Verify that** stdio-based MCP transports are limited to co-located, single-process development scenarios and isolated from shell execution, terminal injection, and process-spawning capabilities; stdio must not cross network or multi-tenant boundaries. | 3 | D/V |
| **10.6.2** | **Verify that** MCP servers expose only allow-listed functions and resources and prohibit dynamic dispatch, reflective invocation, or execution of function names influenced by user or model-provided input. | 3 | D/V |
| **10.6.3** | **Verify that** tenant boundaries, environment boundaries (e.g., dev/test/prod), and data domain boundaries are enforced at the MCP layer to prevent cross-tenant or cross-environment server or resource discovery. | 3 | D/V |

---

## References

* [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final)
