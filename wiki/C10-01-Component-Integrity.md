# C10.1: Component Integrity & Supply Chain Hygiene

> **Parent:** [C10 MCP Security](C10-MCP-Security)
> **Requirements:** 3 | **IDs:** 10.1.1–10.1.3

## Purpose

This section ensures that MCP server and client software is obtained from trusted sources, that configuration artifacts do not leak credentials, and that only approved MCP servers are permitted in production. MCP components are typically distributed as npm packages, Python packages, Docker images, or standalone binaries — all of which are susceptible to supply-chain attacks including typosquatting, dependency confusion, and build-time tampering. Because MCP servers execute arbitrary code with access to sensitive resources (databases, APIs, file systems), compromised components have outsized blast radius compared to typical library dependencies.

The severity of these risks was demonstrated in real-world incidents throughout 2025-2026. The Postmark MCP supply chain breach (2025) saw attackers backdoor an npm package used in AI automation pipelines, inserting a single line of malicious code that directed compromised MCP servers to BCC every outgoing email to an attacker-controlled address. The Smithery supply chain attack (October 2025) affected 3,000+ hosted applications and their API tokens. Research using the MCPTox benchmark showed that tool poisoning attacks — where malicious instructions are embedded in tool metadata invisible to human users but processed by AI models — pass seamlessly into agent contexts with alarming frequency. A 2026 survey of 2,614 MCP implementations found 82% use file operations vulnerable to path traversal, two-thirds have code injection risks, and over a third are susceptible to command injection. These findings underscore why component integrity and supply-chain hygiene are foundational to MCP security.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.1.1** | **Verify that** MCP server and client components are obtained only from trusted sources and verified using signatures, checksums, or secure package metadata, rejecting tampered or unsigned builds. | 1 | D/V | **Supply-chain compromise / trojanized MCP servers.** An attacker publishes a malicious MCP server package (e.g., via typosquatting on npm or PyPI) that exfiltrates data or injects malicious tool definitions. Without integrity verification, the compromised component is silently adopted. | Review package installation procedures for checksum or signature verification. Check CI/CD pipelines for integrity gates (e.g., `npm audit signatures`, `pip hash-checking mode`, Docker Content Trust). Verify that MCP server binaries or images are pulled from pinned, authenticated sources. | No MCP-specific signing standard exists yet. Current verification relies on general package manager integrity features (npm provenance, PyPI attestations, Sigstore). The MCP ecosystem lacks a centralized registry with enforced signing — most MCP servers are distributed via GitHub repos without formal attestation. |
| **10.1.2** | **Verify that** MCP client and server configurations do not contain plaintext secrets (API keys, tokens, client secrets) and that credentials are injected or resolved at runtime rather than stored in configuration files, environment variables, or source code. | 1 | D/V | **Credential exposure via configuration leakage.** MCP configurations (e.g., `claude_desktop_config.json`, `.mcp.json`) commonly embed API keys and database connection strings in plaintext. If these files are committed to version control, shared, or accessed by other processes, credentials are exposed. | Scan configuration files for plaintext secrets using tools like `trufflehog`, `gitleaks`, or `detect-secrets`. Verify that production deployments use secret managers (Vault, AWS Secrets Manager, 1Password CLI) or environment-variable injection from secure sources. Check that `.gitignore` excludes MCP config files. | This is a pervasive problem in the MCP ecosystem today. Most MCP configuration examples in documentation show plaintext API keys. The MCP spec does not define a standard secret-reference mechanism (e.g., `${vault:secret/path}`), so each implementation handles this differently. |
| **10.1.3** | **Verify that** only allowlisted MCP server identifiers (name, version, and registry) are permitted in production and that the runtime rejects connections to unlisted or unregistered servers at load time. | 1 | D/V | **Rogue or unauthorized MCP server connections.** Without an explicit allowlist, an attacker (or misconfigured agent) can connect to arbitrary MCP servers — including attacker-controlled servers that serve poisoned tool definitions or exfiltrate data from tool arguments. The 2026 finding that 8,000+ MCP servers were publicly exposed, with 492 identified as lacking basic authentication, demonstrates the scale of this risk. Allowlisting prevents unauthorized server connections from entering the trust boundary. | Review production MCP client configuration for an explicit allowlist of permitted server identifiers (name, version, registry/source). Verify the runtime rejects connections to servers not on the allowlist. Test by configuring a connection to an unlisted MCP server and confirming it is blocked at load time. Check that the allowlist is version-pinned to prevent connecting to a compromised newer version. | Requires organizational governance to maintain the allowlist. The MCP spec does not define a server identity or registry standard, so allowlisting currently relies on implementation-specific identifiers (package name + version, Docker image digest, URL). MCP gateway products (emerging in 2025-2026) can centralize this enforcement. |

---

## Real-World Incidents & Research (2024-2026)

- **Postmark MCP Supply Chain Breach (2025):** Attackers backdoored an npm package used for sending transactional emails through Postmark in AI automation pipelines. A single line of malicious code directed compromised MCP servers to BCC every outgoing email to the attackers, demonstrating how supply-chain compromise in MCP components can enable large-scale data exfiltration.
- **Smithery Supply Chain Attack (October 2025):** Affected 3,000+ hosted applications and their API tokens through a compromised MCP server registry entry.
- **Supabase Cursor Agent Exploit (mid-2025):** Supabase's Cursor agent, running with privileged service-role access, processed support tickets containing user-supplied input as commands. Attackers embedded SQL instructions to exfiltrate sensitive integration tokens by leaking them into a public support thread — combining privileged MCP access, untrusted input, and external communication channels.
- **MCPTox Benchmark (2025-2026):** Research benchmark evaluating how often malicious or manipulated tool definitions pass into AI agent contexts, finding that tool poisoning attacks are alarmingly common and frequently result in unauthorized execution or data leakage.
- **CVE-2025-6514 (CVSS 10.0):** Critical RCE vulnerability in an MCP server component demonstrating the extreme risk of unvetted MCP packages.
- **8,000+ Exposed MCP Servers (2026):** Research identified over 8,000 publicly exposed MCP servers, with 492 lacking basic authentication or encryption, highlighting the need for strict allowlisting.
- **MCP CVE Surge (early 2026):** 30 CVEs filed against MCP implementations in a 60-day period, covering SSRF, command injection, path traversal, and authentication bypass.

## Related Standards & References

- [SLSA (Supply-chain Levels for Software Artifacts)](https://slsa.dev/) — framework for supply-chain integrity
- [Sigstore](https://www.sigstore.dev/) — keyless signing for open-source packages
- [npm Provenance](https://docs.npmjs.com/generating-provenance-statements) — build provenance for npm packages
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) — known-vulnerability scanning
- [CIS Software Supply Chain Security Guide](https://www.cisecurity.org/benchmark/software_supply_chain_security)
- [Invariant Labs: MCP Tool Poisoning Research](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) — tool poisoning attack analysis
- [Vulnerable MCP Project](https://vulnerablemcp.info/) — comprehensive MCP security vulnerability database
- [MCP Security 2026: 30 CVEs in 60 Days](https://www.heyuan110.com/posts/ai/2026-03-10-mcp-security-2026/) — CVE analysis for MCP ecosystem

---

## Open Research Questions

- [ ] Should the MCP ecosystem adopt a standardized package-signing mechanism (e.g., Sigstore-based attestations for MCP server packages)?
- [ ] How should MCP configuration files handle secret references in a cross-platform, cross-SDK way?
- [ ] Is there a viable model for an MCP server registry with enforced integrity metadata (similar to Docker Hub's Content Trust)?
- [ ] How do you verify integrity of MCP servers that are dynamically discovered at runtime rather than pre-configured?
- [ ] Can MCPTox-style automated benchmarking be integrated into CI/CD pipelines to detect tool poisoning before deployment?
- [ ] Should MCP gateway products enforce allowlisting as a default policy, and what identity standard should server identifiers follow?

---
