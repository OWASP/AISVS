# C10.3: Secure Transport & Network Boundary Protection

> **Parent:** [C10 MCP Security](C10-MCP-Security)
> **Requirements:** 5 | **IDs:** 10.3.1–10.3.5

## Purpose

This section ensures that communication between MCP clients and servers uses secure, authenticated, and encrypted transport channels. The MCP specification defines two primary transports: **stdio** (for local, same-machine communication) and **streamable HTTP** (for remote communication, replacing the earlier SSE-based transport). Each transport has distinct threat models — stdio is vulnerable to local process injection and terminal escape attacks, while HTTP-based transports face the standard web threats (MITM, DNS rebinding, protocol downgrade). This section focuses on the HTTP-based transports; stdio restrictions are covered in C10.6.

The MCP transport landscape evolved significantly in 2025-2026. Streamable HTTP was introduced in the MCP specification version 2025-03-26 as the recommended approach for remote servers, and in May 2025 the MCP team formally deprecated the old HTTP+SSE transport. The shift to Streamable HTTP was motivated by security improvements: it enables an `Authorization: Bearer` header on every single message envelope (not just the initial connection), supports standard CORS policies, and provides secure session management — whereas SSE's long-lived unidirectional connections lacked built-in authentication framing and were susceptible to connection-holding DoS attacks. As of the 2025-06-18 specification revision, Streamable HTTP is the sole standard HTTP transport, with SSE retained only as an optional streaming mechanism within Streamable HTTP responses. Despite this, many existing MCP servers still use legacy SSE transport, making migration guidance and backward-compatibility security a practical concern.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.3.1** | **Verify that** authenticated, encrypted streamable-HTTP is used as the primary MCP transport in production environments and that alternate transports (e.g., stdio or SSE) are restricted to local or tightly controlled environments with explicit justification. | 2 | D/V | **Unencrypted or unauthenticated transport in production.** Using stdio across network boundaries or SSE without TLS exposes MCP traffic (including tool arguments, responses, and potentially credentials) to network-level interception. Streamable HTTP with TLS is the only transport designed for production remote use. The Grafana MCP Server defaulted to binding `0.0.0.0:8000` with an unauthenticated SSE interface on all network interfaces — a pattern that recurs across community MCP servers. | Review deployment configuration to confirm streamable HTTP is the configured transport for all production MCP connections. Verify that any stdio or SSE usage is documented with justification and restricted to development/local environments. Check network architecture diagrams for MCP traffic paths. Use `netstat` or `ss` to confirm MCP servers bind only to `127.0.0.1` when intended for local use, not `0.0.0.0`. | The MCP spec (2025-03-26) introduced streamable HTTP as the recommended transport, deprecating SSE for new deployments. As of March 2026, many existing MCP servers still use SSE. Migration path and backward compatibility need consideration. MCP gateway products (MintMCP, ContextForge) can enforce transport policy centrally. |
| **10.3.2** | **Verify that** streamable-HTTP MCP transports use authenticated, encrypted channels (TLS 1.3 or later) with certificate validation. | 2 | D/V | **Man-in-the-middle interception of MCP traffic.** Without TLS, an attacker on the network path can intercept, read, and modify MCP messages — including tool invocations, responses containing sensitive data, and OAuth tokens in transit. TLS 1.2 is acceptable but 1.3 is preferred for forward secrecy and reduced handshake latency. Session IDs exposed in URLs (a pattern found in some MCP implementations) leak tokens through browser history, logs, and referrer headers. | Verify TLS configuration on the MCP server endpoint: check certificate validity, minimum TLS version (1.3 preferred, 1.2 minimum), cipher suite selection, and that certificate validation is not disabled in the client. Use `testssl.sh` or `ssllabs-scan` against the MCP server's HTTPS endpoint. For mTLS deployments, verify both client and server certificates using `openssl s_client -cert`. Automate certificate rotation with cert-manager or ACME with short validity periods (days to weeks). Enable OCSP or CRL revocation checks. | Standard TLS best practice. The main risk is MCP servers deployed with self-signed certificates or TLS disabled for "simplicity" during development, then promoted to production without fixing. MCP SDKs should default to TLS-on with certificate validation. For high-security environments, consider deploying mutual TLS (mTLS) or sender-constrained tokens (DPoP) so both agent and server must present cryptographic proof of identity. |
| **10.3.3** | **Verify that** SSE-based MCP transports are used only within private, authenticated internal channels and enforce TLS, authentication, schema validation, payload size limits, and rate limiting; SSE endpoints must not be exposed to the public internet. | 2 | D/V | **SSE endpoint abuse and data exposure.** SSE connections are long-lived, unidirectional, and lack built-in authentication framing. If exposed publicly, SSE endpoints can be abused for denial-of-service (holding connections open), data exfiltration (streaming sensitive tool responses), or injection. SSE's plain GET requests skip the browser's OPTIONS preflight checks, which means DNS rebinding attacks can succeed without triggering CORS protections — a critical distinction from standard POST-based APIs. CVE-2025-59163 (Vet MCP Server) demonstrated how SSE transport on localhost enabled external websites to interact with local MCP servers. | Verify SSE endpoints are not reachable from the public internet (check firewall rules, load balancer configuration). Confirm TLS is enforced. Test for authentication bypass by connecting without credentials. Verify payload size limits and rate limiting are configured. Attempt to send oversized messages. Scan for SSE endpoints binding to `0.0.0.0` instead of `127.0.0.1`. | SSE transport is deprecated in the MCP spec (2025-03-26) in favor of streamable HTTP. This requirement ensures legacy SSE deployments are hardened during the migration period. As of March 2026, SSE remains common in deployed MCP servers. Organizations should plan migration to streamable HTTP and audit existing SSE endpoints for network exposure. |
| **10.3.4** | **Verify that** MCP servers validate the `Origin` and `Host` headers on all HTTP-based transports (including SSE and streamable-HTTP) to prevent DNS rebinding attacks and reject requests from untrusted, mismatched, or missing origins. | 2 | D/V | **DNS rebinding attacks against local MCP servers.** CVE-2025-66414 (TypeScript SDK < 1.24.0) and CVE-2025-66416 (Python SDK < 1.23.0) demonstrated that both official MCP SDKs shipped without DNS rebinding protection by default. The attack flow: (1) victim visits malicious site, (2) attacker's domain initially resolves to attacker IP, then re-resolves to `127.0.0.1`, (3) browser treats the rebinding as same-origin and sends requests to the local MCP server, (4) attacker exfiltrates data via tool invocations. Straiker researchers demonstrated this against GitHub's "Everything" MCP server, extracting environment variables containing API keys for OpenAI and DeepSeek. The Neo4j MCP Cypher Server DNS rebinding vulnerability enabled complete database takeover of locally running instances. | Send requests with manipulated `Origin` and `Host` headers and verify the server rejects them. Test with: (1) no Origin header, (2) mismatched Origin, (3) Origin set to an attacker-controlled domain. Verify the server maintains an allowlist of permitted origins. Confirm MCP SDK versions are at least TypeScript 1.24.0 / Python 1.23.0 (the versions that added DNS rebinding protection). Use browser-based DNS rebinding test tools to verify the server rejects rebind attempts. | DNS rebinding was the most actively exploited MCP transport vulnerability in 2025. Both official SDKs were patched, but third-party and community MCP servers may still lack protection. Per-session tokens tied to initial DNS resolution provide defense-in-depth. The MCP spec still does not explicitly mandate Origin validation as of the 2025-06-18 revision. |
| **10.3.5** | **Verify that** intermediaries do not alter or remove the `Mcp-Protocol-Version` header on streamable-HTTP transports unless explicitly required by the protocol specification, preventing protocol downgrade via header stripping. | 2 | D/V | **Protocol downgrade via header stripping.** The `Mcp-Protocol-Version` header negotiates the protocol version between client and server. If a proxy or load balancer strips this header, the server may fall back to an older protocol version with weaker security properties. A known spec inconsistency (reported in [GitHub issue #854](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/854)) compounds this: the 2025-06-18 spec says servers SHOULD assume version 2025-06-18 when the header is missing, but since that version mandates the header, a missing header actually indicates an older client running 2025-03-26. This ambiguity creates protocol confusion that an attacker could exploit. | Deploy an MCP client and server through a representative intermediary stack (reverse proxy, load balancer, WAF). Verify the `Mcp-Protocol-Version` header is preserved end-to-end. Check proxy configurations for header stripping rules. Test with the header removed and verify the server responds appropriately (rejection or explicit version negotiation, not silent downgrade). Add `Mcp-Protocol-Version` to header allowlists in WAF and API gateway configurations. Also enforce HSTS (`Strict-Transport-Security`) to prevent protocol downgrade at the HTTP layer. | Most current intermediaries (nginx, HAProxy, cloud load balancers) preserve custom headers by default, but WAFs or API gateways with strict header allowlists may strip unknown headers. The spec ambiguity around missing-header fallback behavior remains unresolved as of March 2026. MCP gateway products that pin protocol versions centrally provide the strongest defense against version downgrade. |

---

## Transport Evolution Timeline

| Date | Event | Security Impact |
|------|-------|----------------|
| 2024-11-05 | MCP spec defines HTTP+SSE transport | SSE long-lived connections lack per-message auth; vulnerable to connection-holding DoS |
| 2025-03-26 | Streamable HTTP introduced as recommended transport | Per-message Bearer tokens, standard CORS, secure session management |
| 2025-05 | MCP team formally deprecates HTTP+SSE | Legacy deployments must migrate; dual-transport period introduces attack surface |
| 2025-06-18 | Streamable HTTP becomes sole standard HTTP transport | SSE retained only as optional streaming within Streamable HTTP responses |
| 2025-2026 | MCP gateway products emerge (10+ commercial offerings by early 2026) | Centralized transport policy enforcement, TLS termination, protocol version pinning |
| 2026-01 to 2026-02 | 30+ CVEs filed against MCP servers in 60 days (mcp-remote CVE-2025-6514 CVSS 9.6, Docker MCP Gateway CVE-2025-64443, multiple SSRF chains) | Transport-layer attack surface proven at scale; 82% of surveyed MCP implementations had exploitable file-operation paths |
| 2026-04-01 | SSE transport hard-cutoff deadline announced by early adopters (e.g., Keboola) | Organizations running SSE in production must complete migration to streamable HTTP or lose connectivity |

## Known Vulnerabilities & Incidents

| CVE / ID | Component | Description | Impact | Fixed In |
|----------|-----------|-------------|--------|----------|
| CVE-2025-66414 | MCP TypeScript SDK | DNS rebinding protection disabled by default for localhost-bound SSE and Streamable HTTP servers | Malicious websites can pivot to local MCP servers through the browser, invoking tools and exfiltrating data | SDK ≥ 1.24.0 |
| CVE-2025-66416 | MCP Python SDK | DNS rebinding protection disabled by default for localhost-bound HTTP servers | Same as above — attacker domains re-resolve to `127.0.0.1`, bypassing same-origin policy | SDK ≥ 1.23.0 |
| CVE-2025-49596 | MCP Inspector | RCE via DNS rebinding in the MCP Inspector development tool (CVSS 9.4 Critical) | When developers visit malicious websites, JavaScript silently connects to local MCP Inspector and achieves remote code execution | Patched in MCP Inspector update |
| CVE-2025-59163 | Vet MCP Server | DNS rebinding vulnerability in SSE transport | External websites interact with locally running MCP servers without authentication | Patched |
| CVE-2026-25536 | MCP TypeScript SDK | Cross-client data leak when `StreamableHTTPServerTransport` is reused across multiple clients | Responses intended for one client leak to another client sharing the same server instance | Patched in later SDK release |
| — | Neo4j MCP Cypher Server | DNS rebinding enables unauthorized tool invocations | Complete database takeover of locally running Neo4j instances | Configuration mitigation |
| — | Grafana MCP Server | Binds to `0.0.0.0:8000` by default with unauthenticated SSE interface | All network interfaces exposed; any host on the network can invoke MCP tools | Configuration change required |
| — | GitHub "Everything" MCP Server | Demonstrated by Straiker researchers using DNS rebinding | Environment variables containing API keys (OpenAI, DeepSeek credentials) exfiltrated via `printEnv` tool | Configuration mitigation |
| CVE-2025-64443 | Docker MCP Gateway | DNS rebinding vulnerability when running in SSE or streaming mode (CVSS 7.3 High) | Attackers trick users into visiting malicious websites to manipulate tools running inside the Docker MCP Gateway; default stdio mode unaffected | Gateway ≥ v0.28.0 |
| CVE-2026-27826 | mcp-atlassian | Unauthenticated SSRF via manipulated `X-Atlassian-Jira-Url` headers in streamable-HTTP and SSE modes | Attackers force the MCP server to make arbitrary HTTP requests, exposing internal services and cloud metadata endpoints | ≥ 0.17.0 |
| CVE-2026-26118 | Azure MCP Server | Server-side request forgery enabling privilege elevation (CVSS 8.8 High) | Attackers exploit SSRF to access Azure IMDS and escalate privileges within cloud environments | Patched by Microsoft (March 2026) |
| CVE-2026-32111 | ha-mcp (Home Assistant) | SSRF via `ha_url` parameter in OAuth beta (CVSS 5.3 Medium) | Attackers redirect MCP server requests to internal services through crafted URL parameters | ≥ 7.0.0 |

## SSRF as a Transport-Adjacent Threat

As of early 2026, server-side request forgery (SSRF) has emerged as a major transport-layer threat for MCP servers exposed via streamable HTTP or SSE. The pattern is consistent: MCP servers that accept URLs or host identifiers in HTTP headers or tool parameters can be coerced into making requests to internal services, cloud metadata endpoints (e.g., `169.254.169.254`), or other network-internal resources the attacker cannot reach directly.

The OWASP MCP Top 10 (published March 2026) calls this out under **MCP-07 (Inadequate Authentication & Authorization)** — the Azure MCP Server SSRF (CVE-2026-26118) exploited OAuth proxy trust where authentication existed but authorization boundaries did not. The mcp-atlassian SSRF (CVE-2026-27826) allowed unauthenticated attackers to manipulate `X-Atlassian-Jira-Url` headers to redirect server requests.

**Mitigations for SSRF in MCP transport:**

- Validate and allowlist all URLs and host values received in HTTP headers and tool parameters before the MCP server makes outbound requests.
- Block requests to private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`) and link-local addresses from MCP server processes.
- Deploy MCP servers with restrictive egress firewall rules — only permit outbound connections to known, required endpoints.
- Use network policies (Kubernetes NetworkPolicy, AWS Security Groups) to limit what internal services MCP server pods can reach.

---

## Defensive Tooling & Gateway Ecosystem

As of early 2026, several products provide centralized MCP transport policy enforcement:

| Product | Type | Transport Security Features |
|---------|------|---------------------------|
| **MintMCP Gateway** | Commercial (SOC 2 Type II certified) | TLS termination, OAuth protection, rate limiting, DDoS protection, audit trails in SOC 2/HIPAA/GDPR formats |
| **ContextForge** | Open-source (IBM ecosystem) | Supports HTTP(S), WebSocket, SSE, and stdio streams; configurable transport policies |
| **Lasso Security** | Commercial | Threat detection for MCP traffic, transport anomaly monitoring |
| **TLS MCP Server** | Open-source tool | Certificate analysis, cipher suite assessment, security grading for MCP endpoints |
| **Docker MCP Gateway** | Open-source (Docker ecosystem) | Stdio-by-default transport isolation; SSE/streaming modes available but require explicit DNS rebinding mitigation (patched in v0.28.0) |
| **SlowMist MCP Security Checklist** | Open-source audit framework | Structured security checklist covering transport, authentication, tool validation, and supply chain for MCP deployments |

**Practical guidance for transport hardening:**

- **Bind address control:** Always bind localhost MCP servers to `127.0.0.1`, never `0.0.0.0`. Audit with `netstat -tlnp` or `ss -tlnp`.
- **SDK version pinning:** Enforce minimum MCP SDK versions (TypeScript ≥ 1.24.0, Python ≥ 1.23.0) to get DNS rebinding protection by default.
- **Certificate lifecycle:** Use cert-manager or ACME for automated certificate rotation with short validity periods. Enable OCSP or CRL revocation checking.
- **Gateway delegation:** For organizations running multiple MCP servers, centralize TLS termination and protocol version enforcement at the gateway layer rather than configuring each server individually.
- **Network segmentation:** Place MCP servers in private subnets accessible only by authorized workloads. Front external endpoints with gateways that enforce rate limiting.
- **Session hygiene:** Never place session IDs in URL query strings. Clear sensitive context data from memory when sessions terminate.
- **SSRF egress controls:** Block MCP server outbound connections to private IP ranges and cloud metadata endpoints. Use Kubernetes NetworkPolicy or cloud security groups to enforce least-privilege egress.
- **HSTS enforcement:** Set `Strict-Transport-Security` headers on all MCP HTTP endpoints to prevent protocol downgrade at the HTTP layer. Combine with `Mcp-Protocol-Version` header preservation for layered downgrade defense.
- **mTLS for high-security deployments:** Deploy mutual TLS where both client and server present certificates. Configure with `ssl_verify_client on` (nginx) or equivalent. Classify MCP servers as OAuth Resource Servers per the 2025-06-18 spec and use Resource Indicators (RFC 8707) to prevent cross-server token misuse.

## Cryptographic Agility & Post-Quantum Considerations

As of early 2026, security researchers have begun evaluating MCP transport cryptography against quantum computing threats. The core concern is "harvest now, decrypt later" — adversaries capturing encrypted MCP traffic today for future decryption once quantum computers become practical. This is particularly relevant for MCP deployments handling sensitive data (healthcare, finance, government).

Key considerations for MCP transport cryptographic agility (per [Gopher Security's analysis](https://www.gopher.security/blog/algorithmic-agility-mcp-server-client-cryptographic-negotiation)):

- **Algorithm negotiation:** Clients should advertise supported algorithms (including post-quantum candidates like ML-KEM and ML-DSA) rather than assuming compatibility. Servers enforce mandatory-to-implement (MTI) algorithms based on deployment security requirements.
- **Suite bundling:** Group compatible algorithms into named suites (e.g., `MCP_PQ_KEM_KYBER768_AES256_GCM`) to avoid combinatoric explosion during negotiation. Healthcare and financial deployments may enforce PQC-only policies while less sensitive environments use hybrid approaches.
- **Hybrid signatures:** During the transition period, deploy dual signatures using both traditional (ECC) and post-quantum algorithms. This ensures backward compatibility while providing quantum resistance.
- **Downgrade prevention at the cryptographic layer:** Post-quantum signatures can protect the entire negotiation handshake, including the list of supported algorithms. If an attacker strips PQC options from the client's advertised list, the signature verification fails, providing a stronger downgrade prevention mechanism than header-based approaches alone.
- **RFC 7696 (Guidelines for Cryptographic Algorithm Agility)** provides the foundational framework — MCP implementations should design for algorithm replacement without requiring full stack rewrites.

## Related Standards & References

- [MCP Transports Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) — current official transport definitions
- [MCP Versioning Specification](https://modelcontextprotocol.io/specification/versioning) — protocol version negotiation and header requirements
- [RFC 8446: TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446) — transport layer security
- [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [DNS Rebinding Attacks (Stanford research)](https://crypto.stanford.edu/dns/) — foundational DNS rebinding research
- [OWASP ASVS v4: V9 Communications](https://owasp.org/www-project-application-security-verification-standard/)
- [Auth0: Why MCP's Move Away from SSE Simplifies Security](https://auth0.com/blog/mcp-streamable-http/) — analysis of streamable HTTP security benefits
- [Auth0: MCP Spec Updates — All About Auth (June 2025)](https://auth0.com/blog/mcp-specs-update-all-about-auth/) — authorization and resource indicator requirements
- [AWS: MCP Transport Mechanisms](https://builder.aws.com/content/35A0IphCeLvYzly9Sw40G1dVNzc/mcp-transport-mechanisms-stdio-vs-streamable-http) — transport comparison from AWS perspective
- [CVE-2025-66414: MCP TypeScript SDK DNS Rebinding](https://advisories.gitlab.com/pkg/npm/@modelcontextprotocol/sdk/CVE-2025-66414/) — SDK vulnerability advisory
- [CVE-2025-66416: MCP Python SDK DNS Rebinding](https://www.resolvedsecurity.com/vulnerability-catalog/CVE-2025-66416) — SDK vulnerability advisory
- [Straiker: DNS Rebinding Exposes Internal MCP Servers](https://www.straiker.ai/blog/agentic-danger-dns-rebinding-exposing-your-internal-mcp-servers) — research demonstration with real MCP servers
- [Vulnerable MCP Project](https://vulnerablemcp.info/) — comprehensive MCP security vulnerability database
- [MCP-Protocol-Version Header Issue #854](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/854) — spec inconsistency in version fallback behavior
- [Aembit: Securing MCP Server Communications](https://aembit.io/blog/securing-mcp-server-communications-best-practices/) — mTLS and transport hardening guidance
- [PgEdge: MCP Transport Architecture, Boundaries, and Failure Modes](https://www.pgedge.com/blog/mcp-transport-architecture-boundaries-and-failure-modes) — transport architecture analysis
- [Docker MCP Gateway DNS Rebinding Advisory (GHSA-46gc-mwh4-cc5r)](https://github.com/docker/mcp-gateway/security/advisories/GHSA-46gc-mwh4-cc5r) — CVE-2025-64443 affecting SSE/streaming modes
- [Gopher Security: Algorithmic Agility in MCP Cryptographic Negotiation](https://www.gopher.security/blog/algorithmic-agility-mcp-server-client-cryptographic-negotiation) — post-quantum considerations for MCP transport
- [Securing MCP: OAuth, mTLS, and Zero Trust (dasroot.net, Feb 2026)](https://dasroot.net/posts/2026/02/securing-model-context-protocol-oauth-mtls-zero-trust/) — comprehensive mTLS and zero-trust guidance
- [SlowMist MCP Security Checklist](https://github.com/slowmist/MCP-Security-Checklist) — structured security audit checklist for MCP deployments
- [SSRF in Azure MCP Server (CVE-2026-26118)](https://blog.blueinfy.com/2026/03/ssrf-in-azure-mcp-server-tools.html) — SSRF privilege elevation via MCP transport
- [Keboola SSE Deprecation Notice](https://changelog.keboola.com/sse-transport-deprecation-migration-to-streamable-http/) — April 2026 SSE hard-cutoff migration timeline
- [RFC 7696: Guidelines for Cryptographic Algorithm Agility](https://datatracker.ietf.org/doc/html/rfc7696) — framework for algorithm replacement in protocols
- [RFC 8707: Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — token scoping to prevent cross-server misuse in MCP OAuth flows
- [ContextForge mTLS Feature Request (IBM/mcp-context-forge #568)](https://github.com/ibm/mcp-context-forge/issues/568) — tracks mTLS support for MCP gateways

---

## Open Research Questions

- [ ] Should the MCP spec mandate TLS for all HTTP-based transports, or is it sufficient to recommend it? The wave of DNS rebinding CVEs in 2025 suggests mandatory TLS + origin validation would have prevented most exploits.
- [ ] How should MCP servers handle the transition from SSE to streamable HTTP — is a dual-transport migration period acceptable, and what are the security implications? SSE remains widely deployed as of early 2026.
- [ ] Is `Mcp-Protocol-Version` header validation sufficient to prevent downgrade, or should the protocol include a cryptographic version binding? The spec inconsistency around missing-header fallback (issue #854) suggests the current mechanism is fragile.
- [ ] Should MCP define a standard mechanism for mutual TLS (mTLS) between clients and servers in high-security environments? Some organizations already deploy mTLS via gateway products, but there is no standardized MCP mTLS profile.
- [ ] As MCP gateways become standard infrastructure, should TLS termination and protocol version enforcement be delegated to the gateway layer, and what are the trust implications? Gateway products are proliferating (10+ commercial offerings by early 2026) but introduce a new trust boundary.
- [ ] The cross-client data leak (CVE-2026-25536) when reusing `StreamableHTTPServerTransport` across clients suggests the need for stronger session isolation guarantees at the transport layer — should this be a spec-level requirement?
- [ ] Should the MCP spec require servers to reject requests with missing `Origin` headers by default, given that DNS rebinding was the most exploited MCP transport vulnerability class in 2025?
- [ ] SSRF emerged as a major MCP transport threat in early 2026 (CVE-2026-26118, CVE-2026-27826). Should the MCP spec define mandatory egress restrictions or URL validation requirements for servers that accept external URLs in tool parameters or headers?
- [ ] As post-quantum cryptography matures (ML-KEM, ML-DSA), should the MCP specification define algorithm negotiation suites and mandate cryptographic agility per RFC 7696? The "harvest now, decrypt later" threat is particularly relevant for MCP deployments handling sensitive data.
- [ ] The 30+ CVEs filed against MCP servers in January-February 2026 suggest the ecosystem lacks baseline security requirements. Should there be an MCP security certification or conformance program analogous to FIDO Alliance certification?

---
