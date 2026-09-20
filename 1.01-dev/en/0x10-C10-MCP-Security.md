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
| **10.2.4** | **Verify that** MCP tools/list returns only tools permitted by the requester's authorized scopes, and that list responses vary only by authorization context, never by connection. | 2 |
| **10.2.5** | **Verify that** MCP servers enforce access control on every tool invocation, validating that the user's access token authorizes both the requested tool and the specific argument values supplied. | 2 |
| **10.2.6** | **Verify that** MCP servers enforce single-use semantics server-side for state that must be consumed at most once. | 2 |
| **10.2.7** | **Verify that** MCP servers only accept tokens explicitly issued for them and neither accept nor transit tokens issued for other services. | 1 |
| **10.2.8** | **Verify that** MCP servers treat request state received from clients as attacker-controlled input, and that where such state influences authorization, resource access, or business logic, servers protect its integrity and reject state that fails verification. | 1 |
| **10.2.9** | **Verify that** MCP clients persisting OAuth client credentials associate those credentials with the authorization server that issued them, and re-register with the new authorization server rather than reusing credentials when the resource's authorization server changes. | 2 |

---

## C10.3 Secure Transport

MCP communications must be secured following protocol best practices.

| # | Description | Level |
| :--: | --- | :---: |
| **10.3.1** | **Verify that** authenticated, encrypted streamable HTTP is used for MCP transport for remote services. | 1 |
| **10.3.2** | **Verify that** stdio transport is permitted only in controlled local environments. | 1 |
| **10.3.3** | **Verify that** MCP servers validate both the Origin header and the Host header independently on all HTTP-based transports to prevent DNS rebinding attacks. | 1 |
| **10.3.4** | **Verify that** MCP clients enforce a minimum acceptable protocol version and do not retry with, or fall back to, a protocol version or legacy handshake below that minimum. | 2 |
| **10.3.5** | **Verify that** access tokens between the MCP client and server are sender-constrained using mTLS or DPoP. | 3 |
| **10.3.6** | **Verify that** MCP intermediaries enforcing policy on mirrored request headers confirm that the protocol version indicates a revision requiring header and body validation before trusting those headers. | 2 |

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
| **10.4.9** | **Verify that** MCP proxy servers using a shared upstream OAuth client identity do not allow a requesting MCP client to inherit authorization established for a different MCP client. | 2 |
| **10.4.10** | **Verify that** MCP clients bind each approved MCP server's granted consent and authorization to the connection endpoint approved for that server, and require user re-approval before any further interaction once that endpoint changes. | 2 |
| **10.4.11** | **Verify that** MCP clients reject tool definitions containing invalid mirrored-header annotations and exclude only the affected tool from the tool list. | 1 |
| **10.4.12** | **Verify that** MCP servers reject requests where mirrored request headers do not match the corresponding request body values, after decoding any encoded header values. | 2 |
| **10.4.13** | **Verify that** MCP implementations apply resource bounds to schema validation, such as a maximum schema depth, a cap on the total number of nested schema elements, or a per-validation time budget. | 2 |
| **10.4.14** | **Verify that** MCP implementations do not automatically dereference JSON Schema `$ref` values that resolve to network URIs, and that any opt-in external resolution is disabled by default and rejects loopback, link-local, and private network addresses. | 1 |
| **10.4.15** | **Verify that** MCP implementations reject schemas that fail to validate due to an unresolved external `$ref` rather than treating them as permissive. | 2 |
| **10.4.16** | **Verify that** MCP clients and gateways do not serve cached responses across authorization contexts and do not cache results of multi round-trip requests. | 2 |
| **10.4.17** | **Verify that** MCP servers mark responses containing user-specific data as privately cacheable. | 2 |
| **10.4.18** | **Verify that** MCP servers do not use form-mode elicitation to request secrets or payment credentials, and that in URL-mode elicitation the user completing the flow is the same user who initiated it. | 2 |
| **10.4.19** | **Verify that** MCP servers exclude end-user credentials and personal data from URL-mode elicitation URLs, and do not issue URLs that are pre-authenticated to a protected resource. | 1 |
| **10.4.20** | **Verify that** MCP clients require explicit user consent and display the full URL before opening any URL-mode elicitation target, and do not pre-fetch the URL or its metadata. | 2 |
| **10.4.21** | **Verify that** MCP clients open URL-mode elicitation targets so that neither the client nor the model can observe the page contents or the user's input. | 2 |

---

## References

* [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
* [MCP Specification, revision 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
* [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
* [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [OAuth 2.1 (IETF Draft)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-11)
* [OWASP ASVS 5.0, V10 OAuth and OIDC](https://github.com/OWASP/ASVS) covers general OAuth client and authorization server controls, including proof key for code exchange and mix-up attack defense, which are not restated in this chapter
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
