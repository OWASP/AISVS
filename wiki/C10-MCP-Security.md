# C10: Model Context Protocol (MCP) Security

> **Source:** [`1.0/en/0x10-C10-MCP-Security.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C10-MCP-Security.md)
> **Requirements:** 33 | **Sections:** 6

## Control Objective

Ensure secure discovery, authentication, authorization, transport, and use of MCP-based tool and resource integrations to prevent context confusion, unauthorized tool invocation, or cross-tenant data exposure.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C10.1 | Component Integrity & Supply Chain Hygiene | 2 | 10.1.1–10.1.2 |
| C10.2 | Authentication & Authorization | 12 | 10.2.1–10.2.12 |
| C10.3 | Secure Transport & Network Boundary Protection | 5 | 10.3.1–10.3.5 |
| C10.4 | Schema, Message, and Input Validation | 8 | 10.4.1–10.4.8 |
| C10.5 | Outbound Access & Agent Execution Safety | 3 | 10.5.1–10.5.3 |
| C10.6 | Transport Restrictions & High-Risk Boundary Controls | 3 | 10.6.1–10.6.3 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Tool poisoning — malicious MCP servers providing dangerous tool definitions
- Rug-pull attacks — MCP servers changing tool behavior after initial trust establishment
- Cross-tenant data exposure through shared MCP server instances
- Man-in-the-middle attacks on MCP transport (especially stdio-based local servers)
- Context confusion — tool descriptions manipulating the LLM's behavior

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **MCP SDKs:** Official MCP TypeScript/Python SDKs with built-in validation
- **Transport security:** TLS for remote MCP, Unix domain sockets for local
- **Discovery:** MCP server registries (emerging), tool schema validation
- **Auth:** OAuth 2.0 for MCP, API key management

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C10.1 Component Integrity & Supply Chain Hygiene | _TBD_ | |
| C10.2 Authentication & Authorization | _TBD_ | |
| C10.3 Secure Transport & Network Boundary Protection | _TBD_ | |
| C10.4 Schema, Message, and Input Validation | _TBD_ | |
| C10.5 Outbound Access & Agent Execution Safety | _TBD_ | |
| C10.6 Transport Restrictions & High-Risk Boundary Controls | _TBD_ | |

---

## Open Research Questions

- [ ] How should MCP server trust be established and maintained over time?
- [ ] What's the right auth model for MCP in enterprise environments?
- [ ] How do you prevent tool description manipulation from affecting model behavior?
- [ ] What transport security is adequate for local (stdio) vs. remote (SSE/HTTP) MCP servers?

---

## Related Standards & Cross-References

- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

