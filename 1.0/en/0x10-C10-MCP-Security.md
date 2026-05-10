# C10 Model Context Protocol (MCP) Security

## Control Objective

Ensure secure discovery, authentication, authorization, transport, and use of MCP-based tool and resource integrations to prevent context confusion, unauthorized tool invocation, or cross-tenant data exposure. This chapter covers MCP-protocol-specific controls; general agent authorization is in C9.6, OAuth details in ASVS v5 V10, execution budgets and human approval gates in C9.1–C9.2, sandbox isolation in C9.3, and multi-agent tenant and environment isolation in C9.8.

---

## C10.1 Component Integrity & Supply Chain Hygiene

| # | Description | Level |
| :--: | --- | :---: |
| **10.1.1** | **Verify that** MCP server and client components are obtained only from trusted sources and verified using signatures, checksums, or secure package metadata, rejecting tampered or unsigned builds. | 1 |
| **10.1.2** | **Verify that** only allowlisted MCP server identifiers (name, version, and registry) are permitted in production and that the runtime rejects connections to unlisted or unregistered servers at load time. | 1 |
| **10.1.3** | **Verify that** all MCP tool and resource schemas include cryptographically verifiable provenance metadata — including author, timestamp, version hash, signature, and approved‑by fields. | 2 |

---

## C10.2 Authentication & Authorization

| # | Description | Level |
| :--: | --- | :---: |
| **10.2.1** | **Verify that** MCP clients present a valid access token for each request to MCP servers. | 1 |
| **10.2.2** | **Verify that** MCP servers are registered through a controlled technical onboarding mechanism requiring explicit owner, environment, and resource definitions; unregistered or undiscoverable servers must not be callable in production. | 1 |
| **10.2.3** | **Verify that** MCP session identifiers are treated as state, not identity: generated using cryptographically secure random values, bound to the authenticated user, and never relied on for authentication or authorization decisions. | 1 |
| **10.2.4** | **Verify that** MCP servers validate the presented access token's issuer, audience, expiration, and scope claims in accordance with OAuth 2.1. | 1 |
| **10.2.5** | **Verify that** MCP servers acting as OAuth 2.1 resource servers do not store or persist access tokens or user credentials. | 1 |
| **10.2.6** | **Verify that** MCP `tools/list` and resource discovery responses are filtered based on the end-user's authorized scopes so that agents receive only the tool and resource definitions the user is permitted to invoke. | 2 |
| **10.2.7** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 |
| **10.2.8** | **Verify that** MCP servers do not pass through access tokens received from clients to downstream APIs and instead obtain a separate token scoped to the server's own identity (e.g., via on-behalf-of or client credentials flow). | 2 |
| **10.2.9** | **Verify that** MCP clients request only the minimum scopes needed for the current operation and elevate progressively via step-up authorization for higher-privilege operations. | 2 |
| **10.2.10** | **Verify that** MCP servers enforce deterministic session teardown, destroying cached tokens, in-memory state, temporary storage, and file handles when a session terminates, disconnects, or times out. | 2 |
| **10.2.11** | **Verify that** autonomous agents authenticate using cryptographically bound identity credentials (e.g., key-based proof-of-possession) rather than bearer-only tokens, ensuring that agent identity cannot be transferred, replayed, or impersonated by forwarding a shared secret. | 2 |

---

## C10.3 Secure Transport & Network Boundary Protection

| # | Description | Level |
| :--: | --- | :---: |
| **10.3.1** | **Verify that** authenticated, encrypted streamable-HTTP is used as the primary MCP transport in production environments and that alternate transports (e.g., stdio or SSE) are restricted to local or tightly controlled environments with explicit justification. | 1 |
| **10.3.2** | **Verify that** SSE-based MCP transports are used only within private, authenticated internal channels with TLS, schema validation, payload size limits, and rate limiting enforced, and are not exposed to the public internet. | 2 |
| **10.3.3** | **Verify that** MCP servers validate the `Origin` and `Host` headers on all HTTP-based transports (including SSE and streamable-HTTP) to prevent DNS rebinding attacks and reject requests from untrusted, mismatched, or missing origins. | 2 |
| **10.3.4** | **Verify that** intermediaries do not alter or remove the `Mcp-Protocol-Version` header on streamable-HTTP transports unless explicitly required by the protocol specification, preventing protocol downgrade via header stripping. | 2 |
| **10.3.5** | **Verify that** SSE-based MCP transport endpoints enforce TLS, authentication, schema validation, payload size limits, and rate limiting. | 2 |
| **10.3.6** | **Verify that** MCP clients enforce a minimum acceptable protocol version and reject `initialize` responses that propose a version below that minimum, preventing a server or intermediary from forcing use of a protocol version with weaker security properties. | 2 |

---

## C10.4 Schema, Message, and Input Validation

| # | Description | Level |
| :--: | --- | :---: |
| **10.4.1** | **Verify that** MCP tool responses are validated before being injected into the model context to prevent prompt injection, malicious tool output, or context manipulation. | 1 |
| **10.4.2** | **Verify that** MCP server error responses do not expose internal details (stack traces, file paths, tokens, tool implementation) to the client or model context, preventing information leakage that could be exploited via the model. | 1 |
| **10.4.3** | **Verify that** all MCP transports enforce message-framing integrity and strict schema validation to prevent desynchronization or injection attacks. | 2 |
| **10.4.4** | **Verify that** MCP servers perform strict input validation for all function calls, including type checking, boundary validation, and enumeration enforcement. | 2 |
| **10.4.5** | **Verify that** MCP clients maintain a hash or versioned snapshot of tool definitions and that any change to a tool definition (via `notifications/tools/list_changed` or between sessions) triggers re-approval before the modified tool can be invoked. | 2 |
| **10.4.6** | **Verify that** all MCP transports enforce maximum payload size limits and reject malformed, truncated, or interleaved frames. | 2 |
| **10.4.7** | **Verify that** MCP servers reject unrecognized or oversized parameters in function calls. | 2 |
| **10.4.8** | **Verify that** MCP tool and resource schemas (e.g., JSON schemas or capability descriptors) along with schema manifests are validated for authenticity and integrity using signatures to prevent schema tampering or malicious parameter modification. | 3 |
| **10.4.9** | **Verify that** intermediaries evaluating message content either forward the canonicalized representation they evaluated or reject messages where multiple byte representations could produce different parsed structures. | 3 |
| **10.4.10** | **Verify that** MCP servers sign tool responses with a unique nonce and timestamp within a bounded time window so that the calling agent can verify origin, integrity, and freshness, preventing spoofing, tampering, and replay of tool responses by intermediaries. | 3 |

---

## C10.5 Outbound Access & Agent Execution Safety

| # | Description | Level |
| :--: | --- | :---: |
| **10.5.1** | **Verify that** MCP servers restrict outbound requests to approved internal or external destinations per least-privilege egress policies, with egress to all other targets blocked by default. | 2 |

---

## C10.6 Transport Restrictions & High-Risk Boundary Controls

| # | Description | Level |
| :--: | --- | :---: |
| **10.6.1** | **Verify that** MCP security controls enforce fail-closed semantics: if tool schema validation, MCP-Protocol-Version negotiation fails, authentication check, or policy evaluation fails or cannot be completed, the default action is to deny the request rather than permit it. | 2 |
| **10.6.2** | **Verify that** MCP servers expose only allow-listed functions and resources, and restrict function invocation to statically defined, pre-approved names that cannot be influenced by user or model-provided input. | 3 |

---

## References

* [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
* [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
