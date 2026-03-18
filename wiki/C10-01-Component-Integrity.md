# C10.1: Component Integrity & Supply Chain Hygiene

> **Parent:** [C10 MCP Security](C10-MCP-Security)
> **Requirements:** 2 | **IDs:** 10.1.1–10.1.2

## Purpose

This section ensures that MCP server and client software is obtained from trusted sources and that configuration artifacts do not leak credentials. MCP components are typically distributed as npm packages, Python packages, Docker images, or standalone binaries — all of which are susceptible to supply-chain attacks including typosquatting, dependency confusion, and build-time tampering. Because MCP servers execute arbitrary code with access to sensitive resources (databases, APIs, file systems), compromised components have outsized blast radius compared to typical library dependencies.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.1.1** | **Verify that** MCP server and client components are obtained only from trusted sources and verified using signatures, checksums, or secure package metadata, rejecting tampered or unsigned builds. | 1 | D/V | **Supply-chain compromise / trojanized MCP servers.** An attacker publishes a malicious MCP server package (e.g., via typosquatting on npm or PyPI) that exfiltrates data or injects malicious tool definitions. Without integrity verification, the compromised component is silently adopted. | Review package installation procedures for checksum or signature verification. Check CI/CD pipelines for integrity gates (e.g., `npm audit signatures`, `pip hash-checking mode`, Docker Content Trust). Verify that MCP server binaries or images are pulled from pinned, authenticated sources. | No MCP-specific signing standard exists yet. Current verification relies on general package manager integrity features (npm provenance, PyPI attestations, Sigstore). The MCP ecosystem lacks a centralized registry with enforced signing — most MCP servers are distributed via GitHub repos without formal attestation. |
| **10.1.2** | **Verify that** MCP client and server configurations do not contain plaintext secrets (API keys, tokens, client secrets) and that credentials are injected or resolved at runtime rather than stored in configuration files, environment variables, or source code. | 1 | D/V | **Credential exposure via configuration leakage.** MCP configurations (e.g., `claude_desktop_config.json`, `.mcp.json`) commonly embed API keys and database connection strings in plaintext. If these files are committed to version control, shared, or accessed by other processes, credentials are exposed. | Scan configuration files for plaintext secrets using tools like `trufflehog`, `gitleaks`, or `detect-secrets`. Verify that production deployments use secret managers (Vault, AWS Secrets Manager, 1Password CLI) or environment-variable injection from secure sources. Check that `.gitignore` excludes MCP config files. | This is a pervasive problem in the MCP ecosystem today. Most MCP configuration examples in documentation show plaintext API keys. The MCP spec does not define a standard secret-reference mechanism (e.g., `${vault:secret/path}`), so each implementation handles this differently. |

---

## Related Standards & References

- [SLSA (Supply-chain Levels for Software Artifacts)](https://slsa.dev/) — framework for supply-chain integrity
- [Sigstore](https://www.sigstore.dev/) — keyless signing for open-source packages
- [npm Provenance](https://docs.npmjs.com/generating-provenance-statements) — build provenance for npm packages
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) — known-vulnerability scanning
- [CIS Software Supply Chain Security Guide](https://www.cisecurity.org/benchmark/software_supply_chain_security)

---

## Open Research Questions

- [ ] Should the MCP ecosystem adopt a standardized package-signing mechanism (e.g., Sigstore-based attestations for MCP server packages)?
- [ ] How should MCP configuration files handle secret references in a cross-platform, cross-SDK way?
- [ ] Is there a viable model for an MCP server registry with enforced integrity metadata (similar to Docker Hub's Content Trust)?
- [ ] How do you verify integrity of MCP servers that are dynamically discovered at runtime rather than pre-configured?

---
