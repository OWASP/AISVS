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

- **Tool poisoning at scale** — MCPTox benchmark (August 2025) tested 20 LLM agents across 45+ real-world MCP servers with 353 tools. o1-mini achieved a 72.8% attack success rate; Claude 3.7 Sonnet had the highest refusal rate but still under 3%. More capable models are often *more* susceptible because attacks exploit superior instruction-following. Between Jan-Feb 2026, 30+ CVEs were filed targeting MCP infrastructure — 43% were exec/shell injection.
- **Rug-pull attacks** — MCP servers change tool definitions after initial trust establishment. Users are never re-prompted for consent. Invariant Labs demonstrated SSH key exfiltration via Cursor IDE where the confirmation dialog hid the malicious payload entirely.
- **DNS rebinding** — CVE-2025-66414 (CVSS 8.1) affected MCP TypeScript SDK <1.24.0 with no DNS rebinding protection by default. Docker MCP Gateway and Microsoft Playwright MCP Server were also vulnerable. Remote attackers invoke any tool on localhost MCP servers from a malicious webpage.
- **OAuth consent bypass and token relay** — Obsidian Security (January 2026) found three attack vectors: shared client ID enables consent caching bypass, URL capture bypasses MCP-layer consent entirely, cookie injection forces state validation under attacker control. Square's MCP server exposed merchant data, transactions, and banking details. Token passthrough (now explicitly forbidden in spec) creates confused deputy vulnerabilities.
- **Cross-tool contamination** — Microsoft Developer Blog (April 2025) documented how compromised MCP servers influence legitimate tools through shared LLM context. Tool shadowing via crafted descriptions intercepts calls intended for legitimate servers.
- **MCP sampling exploitation** — Unit 42 (December 2025) demonstrated resource theft (hidden billing), conversation hijacking (persistent session compromise), and covert tool invocation through MCP's sampling capability.
- **Copilot RCE via MCP** — CVE-2025-53773 (CVSS 7.8) — prompt injection in source files manipulates GitHub Copilot into enabling "YOLO mode" (auto-approve all tools), achieving full RCE including MCP server injection. Wormable via infected repos.
- **Shadow MCP servers** — 41% of servers in the official MCP registry have zero authentication as of February 2026 (518 servers scanned). OWASP MCP Top 10 lists Shadow MCP Servers (MCP09) as a top risk.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Aug 2025 | MCPTox — first benchmark for MCP tool poisoning (45+ servers, 353 tools) | o1-mini 72.8% attack success; existing safety alignment largely ineffective against tool poisoning | [arXiv](https://arxiv.org/abs/2508.14925) |
| Jan 2026 | Obsidian Security — MCP OAuth consent bypass (Square case) | Three attack vectors exposing merchant data via shared client IDs, URL capture, and cookie injection | [Obsidian Security](https://www.obsidiansecurity.com/blog/when-mcp-meets-oauth-common-pitfalls-leading-to-one-click-account-takeover) |
| Dec 2025 | CVE-2025-66414 — MCP TypeScript SDK DNS rebinding (CVSS 8.1) | No DNS rebinding protection by default; remote tool invocation from malicious websites | [GitLab Advisory](https://advisories.gitlab.com/pkg/npm/@modelcontextprotocol/sdk/CVE-2025-66414/) |
| Jun 2025 | CVE-2025-53773 — GitHub Copilot RCE via prompt injection (CVSS 7.8) | Wormable attack enabling MCP server injection and full RCE via "YOLO mode" | [Embrace The Red](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/) |
| Dec 2025 | Unit 42 — MCP sampling attack vectors | Resource theft, conversation hijacking, covert tool invocation via sampling | [Unit 42](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/) |
| Apr 2025 | Invariant Labs — MCP tool poisoning + rug-pull disclosure | SSH key exfiltration via Cursor IDE; tool definitions change post-approval | [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) |
| Apr 2025 | Microsoft — cross-tool contamination in MCP | Compromised servers influence legitimate tools through shared LLM context | [Microsoft Dev Blog](https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp) |
| Dec 2025 | Agentic AI Foundation — MCP donated to Linux Foundation | Anthropic, OpenAI, Block, Google, Microsoft, AWS establish neutral governance for MCP | [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **MCP SDKs:** [TypeScript SDK v1.27.1](https://github.com/modelcontextprotocol/typescript-sdk) (Zod v4 for schema validation, host header validation middleware, OAuth 2.1 auth helpers, 161 contributors), [Python SDK](https://github.com/modelcontextprotocol/python-sdk) (Pydantic-based validation, `mcp.server.auth` for OAuth 2.1 RS, supports stdio/SSE/Streamable HTTP). V2 pre-alpha in development for both.
- **MCP security gateways:** [Lasso MCP Gateway](https://github.com/lasso-security/mcp-gateway/) (open-source, April 2025 — prompt injection blocking, data leakage prevention via Presidio, server reputation vetting, tool filtering), [Enkrypt AI Secure MCP Gateway](https://www.enkryptai.com/mcp-scan) (commercial, automated static analysis)
- **MCP security scanners:** [mcpscan.ai](https://mcpscan.ai/) (detects command injection in 23% of scanned servers, tool poisoning, rug pulls, confused deputy), [Snyk Agent Scan](https://github.com/snyk/agent-scan) (v0.4.9, auto-discovers MCP configs across Claude/Cursor/Windsurf/VS Code, 15+ security risks), [Cisco MCP Scanner](https://github.com/cisco-ai-defense/mcp-scanner) (open-source), [Proximity](https://github.com/fr0gger/nova-proximity) (NOVA rule engine for first-pass assessment)
- **MCP Inspector:** [Official tool](https://github.com/modelcontextprotocol/inspector) (`npx @modelcontextprotocol/inspector`) — browser-based debugging revealing all tools/resources/prompts a server exposes. `--cli` flag for CI integration with exit codes.
- **Auth:** MCP Authorization Specification evolved through [March](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization/), [June](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization/), and [November 2025](https://modelcontextprotocol.io/specification/2025-11-25) versions. OAuth 2.1 + PKCE (S256) mandatory, RFC 8707 Resource Indicators required, step-up authorization, token passthrough explicitly forbidden.
- **Registries:** Official MCP registry (518 servers, 41% with zero auth). [Kong MCP Registry](https://konghq.com/) (enterprise, AI Alliance compliant). Gap: no standardized allowlisting mechanism in the protocol itself.
- **Validation:** Zod v4 (TS) / Pydantic (Python) for strict tool argument validation. JSON-RPC 2.0 with discriminated unions for automatic routing. [OWASP MCP Cheat Sheet](https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/) provides implementation guidance.

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C10.1 Component Integrity & Supply Chain | Emerging | No standardized signing for MCP packages. Snyk Agent Scan and Cisco MCP Scanner can detect supply chain risks. 41% of registry servers have zero auth. OWASP MCP04 (Supply Chain Attacks) is a top-10 risk. |
| C10.2 Authentication & Authorization | Maturing | OAuth 2.1 spec evolved through 3 versions (Mar/Jun/Nov 2025). Both SDKs support auth. But Square OAuth bypass shows real-world implementation gaps. Step-up authorization and CIMD are new. |
| C10.3 Secure Transport & Network Protection | Maturing | Streamable HTTP well-defined; TLS mandatory for auth endpoints. CVE-2025-66414 DNS rebinding (CVSS 8.1) showed default-insecure localhost. Fixed in SDK v1.24.0+. Docker and Playwright servers also affected. |
| C10.4 Schema, Message, and Input Validation | Maturing | Zod v4 (TS) and Pydantic (Python) provide strong validation. MCPTox showed 72.8% tool poisoning success despite validation — the attack surface is in *descriptions*, not *schemas*. Tool definition change detection (rug-pull) remains an open problem. |
| C10.5 Outbound Access & Agent Execution Safety | Emerging | Lasso MCP Gateway provides proxy-level filtering. MCP sampling attacks (Unit 42) show egress and execution risks. No standard framework for per-tool execution limits in MCP spec. |
| C10.6 Transport Restrictions & Boundary Controls | Emerging | Stdio isolation is ad-hoc. Host header validation middleware added to SDK. DNS rebinding protections now available but require explicit opt-in. No standard boundary enforcement tooling beyond SDK middleware. |

---

## Open Research Questions

- [x] **How should MCP servers handle token exchange?** — The November 2025 spec explicitly forbids token passthrough and mandates separate tokens for downstream APIs. On-behalf-of (OBO) or client credentials flows are the documented patterns. But Obsidian Security's Square analysis shows real implementations still get this wrong.
- [ ] **How do you prevent tool description manipulation when descriptions are LLM-consumed?** — MCPTox showed 72.8% attack success even on capable models. The fundamental tension: tool descriptions must be informative enough for the LLM to use tools correctly, but this makes them a first-class prompt injection surface. Lasso Gateway scans descriptions, but no solution is comprehensive.
- [ ] **Can rug-pull attacks be reliably detected?** — Tool definitions changing between `tools/list` calls exploit cached trust. Invariant Labs' `mcp-scan` provides detection, but real-time monitoring of definition changes during active sessions has no standard solution.
- [ ] **Will MCP registry security improve?** — 41% of official registry servers have zero auth. Kong MCP Registry adds governance for enterprise, but the open ecosystem lacks signing, reputation scoring, or mandatory security baselines. OWASP MCP09 (Shadow Servers) highlights the risk.
- [ ] **How should the auth spec evolve for regulated environments?** — AAIF's financial sector emphasis suggests compliance-specific extensions are coming. The spec's evolution from 3 versions in 9 months shows rapid iteration but creates adoption risk for implementers targeting moving specifications.
- [ ] **Is MCP's security model adequate for multi-tenant deployments?** — Cross-tool contamination through shared LLM context, namespace collisions, and tool shadowing all exploit multi-server scenarios. The spec doesn't address namespace isolation or tool provenance verification at the protocol level.

---

## Related Standards & Cross-References

- [MCP Specification (November 2025)](https://modelcontextprotocol.io/specification/2025-11-25) — Current spec version with OAuth 2.1, PKCE, step-up authorization, CIMD, token passthrough prohibition
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) (v0.1 Beta) — MCP01-MCP10 covering token mismanagement, scope creep, tool poisoning, supply chain, command injection, intent flow subversion, insufficient auth, audit gaps, shadow servers, context over-sharing
- [OWASP MCP Cheat Sheet](https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/) — Practical implementation guide for secure third-party MCP server usage
- [Agentic AI Foundation (AAIF)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) (December 2025) — Linux Foundation governance for MCP; founding members: Anthropic, OpenAI, Block, Google, Microsoft, AWS
- [CSA MAESTRO Framework](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) — 7-layer threat model for agentic AI with [MCP-specific primer](https://e.cloudsecurityalliance.org/l/908632/2025-06-25/p7xpy)
- [NIST AI Agent Standards Initiative](https://www.nist.gov/caisi/ai-agent-standards-initiative) (February 2026) — Concept paper on Agent Identity and Authorization explicitly references MCP, OAuth 2.1, SPIFFE
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final) — Agents as untrusted entities requiring continuous verification
- [OAuth 2.1 (draft-ietf-oauth-v2-1-13)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13) — Mandated by MCP spec with PKCE + Resource Indicators (RFC 8707)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C02 User Input Validation](C02-User-Input-Validation.md) | Tool argument validation | OWASP MCP05 (Command Injection) — agents construct commands from untrusted input. MCP06 (Intent Flow Subversion) — malicious context hijacks behavior. MCP10 (Context Over-Sharing). All tool arguments are untrusted input requiring validation. |
| [C04 Infrastructure](C04-Infrastructure.md) | Transport and network security | All MCP auth endpoints MUST use HTTPS. CVE-2025-66414 DNS rebinding shows localhost transport risks. Protected Resource Metadata discovery requires secure DNS and TLS. |
| [C05 Access Control](C05-Access-Control.md) | OAuth and authorization | MCP spec mandates OAuth 2.1 with audience-bound tokens (RFC 8707). OWASP MCP02 (Scope Creep) and MCP07 (Insufficient Auth) map to access control failures. Step-up authorization for elevated operations. Token passthrough forbidden. |
| [C06 Supply Chain](C06-Supply-Chain.md) | MCP component integrity | OWASP MCP04 (Supply Chain Attacks) — compromised dependencies introduce backdoors. MCP03 (Tool Poisoning) includes rug pulls and schema poisoning. MCP09 (Shadow Servers) — unapproved deployments. 10,000+ published servers create massive supply chain surface. |
| [C09 Orchestration & Agents](C09-Orchestration-and-Agents.md) | Agent protocol integration | MCP is the de facto agent-to-tool protocol; AAIF governs both MCP and agent frameworks. MAESTRO specifically models multi-agent MCP threat scenarios. MCP sampling enables covert tool invocation. |
| [C13 Monitoring & Logging](C13-Monitoring-and-Logging.md) | MCP audit and telemetry | OWASP MCP08 (Lack of Audit and Telemetry) — limited logging impedes investigation. MCP tool invocation events need C13 logging infrastructure. OpenTelemetry GenAI conventions cover tool calls. |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
