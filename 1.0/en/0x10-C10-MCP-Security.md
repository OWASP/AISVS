# C10 Model Context Protocol (MCP) Security

## Control Objective

This chapter addresses secure discovery, authentication, authorization, transport, and use of MCP-based tool and resource integrations.

---

## C10.1 Component Integrity

Only trusted MCP components must be used, and locally launched servers must be secured.

| # | Description | Level |
| :--: | --- | :---: |
| **10.1.1** | **Verify that** MCP components are obtained only from trusted sources and cryptographically verified. | 1 |
| **10.1.2** | **Verify that** only allow-listed MCP servers are permitted. | 2 |
| **10.1.3** | **Verify that** locally launched MCP servers run in a least-privilege sandbox with restricted file system, network, and system access. | 2 |

---

## C10.2 Authentication & Authorization

Callers must be authenticated and access to MCP servers authorized, following protocol best practices.

| # | Description | Level |
| :--: | --- | :---: |
| **10.2.1** | **Verify that** MCP servers validate access tokens for each request and do not rely on transport security alone. | 1 |
| **10.2.2** | **Verify that** MCP servers validate the presented access token's issuer, audience, expiration, and scope claims in accordance with OAuth 2.1. | 1 |
| **10.2.3** | **Verify that** MCP servers acting as OAuth 2.1 resource servers do not store or persist access tokens or user credentials. | 1 |
| **10.2.4** | **Verify that** MCP tools/list returns only tools permitted by resource owners' authorized scopes. | 2 |
| **10.2.5** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 |
| **10.2.6** | **Verify that** MCP servers ensure all session artifacts are removed when a session terminates. | 2 |
| **10.2.7** | **Verify that** MCP servers do not pass through access tokens received from clients to downstream APIs. | 2 |

---

## C10.3 Secure Transport

MCP communications must be secured following protocol best practices.

| # | Description | Level |
| :--: | --- | :---: |
| **10.3.1** | **Verify that** authenticated, encrypted streamable HTTP is used for MCP transport for remote services. | 1 |
| **10.3.2** | **Verify that** stdio transport is permitted only in controlled local environments. | 1 |
| **10.3.3** | **Verify that** MCP servers validate both the Origin header and the Host header independently on all HTTP-based transports to prevent DNS rebinding attacks. | 2 |
| **10.3.4** | **Verify that** MCP clients enforce a minimum acceptable protocol version and reject initialize responses that propose a version below that minimum. | 2 |
| **10.3.5** | **Verify that** access tokens between the MCP client and server are sender-constrained using mTLS or DPoP. | 3 |

---

## C10.4 Schema, Message, and Input Validation

Schema, message, and input validation must be enforced in both MCP servers and clients.

| # | Description | Level |
| :--: | --- | :---: |
| **10.4.1** | **Verify that** MCP tools/list and tools/call responses are validated against their declared schemas before being injected into the model context. | 1 |
| **10.4.2** | **Verify that** MCP tools/list and tools/call responses are screened for indirect prompt injection before being injected into the model context. | 1 |
| **10.4.3** | **Verify that** MCP servers reject unrecognized or oversized parameters in function calls. | 1 |
| **10.4.4** | **Verify that** all MCP servers enforce strict schema validation. | 2 |
| **10.4.5** | **Verify that** all MCP transports enforce maximum payload size limits. | 2 |
| **10.4.6** | **Verify that** MCP servers sign tool responses with a unique nonce and timestamp so MCP clients can detect replay attempts. | 2 |
| **10.4.7** | **Verify that** MCP clients present users with explicit consent dialogue and cancellation options upon installation of a local MCP server. | 2 |
| **10.4.8** | **Verify that** MCP clients maintain a snapshot of tool definitions and that any change to a tool definition triggers re-approval before the modified tool can be invoked. | 3 |

---

## References

* [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
* [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [OAuth 2.1 (IETF Draft)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-11)
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
