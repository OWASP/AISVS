# C10: Model Context Protocol (MCP) Security

> **Source:** [`1.0/en/0x10-C10-MCP-Security.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C10-MCP-Security.md)
> **Requirements:** 34 | **Sections:** 6

## Control Objective

Ensure secure discovery, authentication, authorization, transport, and use of MCP-based tool and resource integrations to prevent context confusion, unauthorized tool invocation, or cross-tenant data exposure.

> **2025-2026 Highlights:** The MCP spec matured significantly with OAuth 2.1 authorization and streamable HTTP transport replacing legacy SSE. Tool poisoning and rug-pull attacks were publicly disclosed, driving new requirements for component allowlisting (C10.1) and tool definition change detection (C10.4).

---

## Section Pages

| Section | Title | Reqs | IDs | Page |
|---------|-------|:----:|-----|------|
| C10.1 | Component Integrity & Supply Chain Hygiene | 3 | 10.1.1–10.1.3 | [C10-01-Component-Integrity](C10-01-Component-Integrity) |
| C10.2 | Authentication & Authorization | 12 | 10.2.1–10.2.12 | [C10-02-Authentication-Authorization](C10-02-Authentication-Authorization) |
| C10.3 | Secure Transport & Network Boundary Protection | 5 | 10.3.1–10.3.5 | [C10-03-Secure-Transport](C10-03-Secure-Transport) |
| C10.4 | Schema, Message, and Input Validation | 8 | 10.4.1–10.4.8 | [C10-04-Schema-Message-Validation](C10-04-Schema-Message-Validation) |
| C10.5 | Outbound Access & Agent Execution Safety | 3 | 10.5.1–10.5.3 | [C10-05-Outbound-Access-Agent-Safety](C10-05-Outbound-Access-Agent-Safety) |
| C10.6 | Transport Restrictions & High-Risk Boundary Controls | 3 | 10.6.1–10.6.3 | [C10-06-Transport-Restrictions-Boundary-Controls](C10-06-Transport-Restrictions-Boundary-Controls) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Tool poisoning** — malicious MCP servers providing dangerous tool definitions that embed hidden instructions in descriptions, manipulating the LLM into performing unintended actions (data exfiltration, credential theft)
- **Rug-pull attacks** — MCP servers changing tool behavior after initial trust establishment; tool definitions shift between `tools/list` calls to exploit cached trust
- **Cross-tenant data exposure** through shared MCP server instances that fail to enforce tenant isolation
- **Man-in-the-middle attacks** on MCP transport, particularly stdio-based local servers and unencrypted SSE channels
- **Context confusion** — tool descriptions manipulating the LLM's behavior via indirect prompt injection embedded in tool metadata
- **DNS rebinding** — exploiting browser-like HTTP transport to redirect MCP requests to internal services
- **Token relay attacks** — MCP servers forwarding user OAuth tokens to downstream APIs, violating least-privilege

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2024-12 | Invariant Labs: MCP tool poisoning disclosure | Demonstrated tool description manipulation leading to data exfiltration via MCP | [invariantlabs.ai](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) |
| 2025-03 | MCP Specification: Authorization (OAuth 2.1) | Official MCP auth spec defining OAuth 2.1 flow for MCP servers | [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/authorization/) |
| 2025-03 | MCP Specification: Streamable HTTP Transport | Replaced legacy SSE transport with streamable HTTP | [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/transports/) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **MCP SDKs:** Official MCP TypeScript and Python SDKs with built-in JSON-RPC validation and transport handling
- **Transport security:** TLS 1.3 for remote MCP (streamable HTTP), Unix domain sockets for local isolation
- **Discovery:** MCP server registries (emerging); tool schema versioning support in SDK
- **Auth:** OAuth 2.1 for MCP (per spec), dynamic client registration, PKCE support in official SDKs
- **Validation:** JSON Schema validation for tool parameters, `zod` (TS) / `pydantic` (Python) for runtime enforcement

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C10.1 Component Integrity & Supply Chain Hygiene | Low | No standardized signing for MCP packages; relies on platform package managers |
| C10.2 Authentication & Authorization | Medium | OAuth 2.1 spec published; SDK support emerging but not universal |
| C10.3 Secure Transport & Network Boundary Protection | Medium | Streamable HTTP well-defined; TLS enforcement depends on deployment |
| C10.4 Schema, Message, and Input Validation | Medium | JSON Schema validation available in SDKs; schema signing not standardized |
| C10.5 Outbound Access & Agent Execution Safety | Low | No standard framework for egress control or execution limits in MCP |
| C10.6 Transport Restrictions & High-Risk Boundary Controls | Low | Stdio isolation is ad-hoc; no standard boundary enforcement tooling |

---

## Open Research Questions

- [ ] How should MCP server trust be established and maintained over time — is a registry-of-record model viable?
- [ ] What is the right granularity for OAuth scopes in MCP — per-tool, per-resource, or per-action?
- [ ] How do you prevent tool description manipulation from affecting model behavior when descriptions are inherently consumed by the LLM?
- [ ] What transport security is adequate for local (stdio) vs. remote (streamable HTTP) MCP servers?
- [ ] How should MCP servers handle token exchange for downstream API calls — on-behalf-of vs. client credentials?
- [ ] Can formal verification or runtime monitoring detect rug-pull attacks on tool definitions?

---

## Related Standards & Cross-References

- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
- [MCP Authorization Spec (OAuth 2.1)](https://spec.modelcontextprotocol.io/specification/2025-03-26/basic/authorization/)
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final)
- [OAuth 2.1 (draft-ietf-oauth-v2-1)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-12)
- [OWASP ASVS v4 — Session Management, Access Control](https://owasp.org/www-project-application-security-verification-standard/)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C2 User Input Validation | Input validation for tool arguments | C10.4 extends C2 principles to MCP-specific message framing |
| C5 Access Control | Authorization enforcement | C10.2 applies access control at the MCP layer specifically |
| C6 Supply Chain | Component integrity | C10.1 is supply-chain hygiene scoped to MCP components |
| C9 Orchestration and Agents | Agent execution safety | C10.5 complements C9 agent controls with MCP-specific limits |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
