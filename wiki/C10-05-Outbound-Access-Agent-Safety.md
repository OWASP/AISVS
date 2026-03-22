# C10.5: Outbound Access & Agent Execution Safety

> **Parent:** [C10 MCP Security](C10-MCP-Security)
> **Requirements:** 3 | **IDs:** 10.5.1–10.5.3

## Purpose

This section ensures that MCP servers are constrained in what they can reach and how much they can do. MCP servers are code-execution endpoints — when a tool is invoked, the server runs arbitrary logic that may make outbound API calls, access databases, read files, or interact with cloud services. Without egress controls and execution limits, a compromised or manipulated MCP server becomes an unrestricted proxy into the internal network. Additionally, agentic workflows can create unbounded chains of tool invocations where a single prompt injection cascades into dozens of side-effecting operations. This section applies both network-level and execution-level constraints.

The real-world severity of these risks was starkly demonstrated in 2025-2026. CVE-2026-26118 (CVSS 8.8) exposed a critical SSRF vulnerability in Azure MCP Server Tools (versions prior to 2.0.0-beta.17), where low-privileged attackers could craft malicious payloads that tricked the MCP server into leaking its managed identity token — enabling impersonation of the server's Azure identity to access storage accounts, virtual machines, and databases. CVE-2026-27826 (CVSS 8.2) in mcp-atlassian allowed unauthenticated attackers to supply arbitrary URLs via custom `X-Atlassian-Jira-Url` and `X-Atlassian-Confluence-Url` headers without any authentication requirement; in cloud deployments, pointing this at the `169.254.169.254` metadata endpoint stole IAM role credentials. The patch (commit `5cd697d`, fixed in v0.17.0) introduced `validate_url_for_ssrf()` with DNS lookahead resolution to prevent rebinding attacks and IP range validation blocking RFC 1918 and loopback addresses.

As of March 2026, the MCP vulnerability landscape has grown dramatically: over 30 CVEs targeting MCP infrastructure were filed between January and February 2026 alone. Surveys of publicly available MCP server implementations show that 36.7% are exposed to SSRF, 43% contain command injection flaws (CWE-78), 67% have code injection risks (CWE-94), and 82% are vulnerable to path traversal in file operations (CWE-22). These are not theoretical risks — they have active proof-of-concept exploits on GitHub and have been exploited in the wild.

The "denial of wallet" attack pattern has also emerged as a significant threat: an attacker crafts input that causes an agent to loop endlessly (via logical paradox or self-generating task chains), rapidly consuming API budgets and compute resources. The NIST AI Risk Management Framework now mandates "circuit breakers" that automatically cut off an agent's access when token budgets or API call limits are exceeded.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.5.1** | **Verify that** MCP servers may only initiate outbound requests to approved internal or external destinations following least-privilege egress policies and cannot access arbitrary network targets or internal cloud metadata services. | 2 | D/V | **SSRF and lateral movement via MCP servers.** An attacker (via prompt injection or tool argument manipulation) causes the MCP server to make requests to internal services, cloud metadata endpoints (e.g., `169.254.169.254` for AWS IMDSv1), or other network targets that should not be accessible. The MCP server acts as a confused deputy, using its network position to reach targets the attacker cannot reach directly. This is a server-side request forgery (SSRF) pattern specific to MCP. | Review network policies (firewall rules, security groups, network policies in Kubernetes) applied to MCP server workloads. Verify egress is restricted to an allowlist of approved destinations. Test by attempting to make requests from the MCP server to cloud metadata endpoints, internal services not on the allowlist, and arbitrary external URLs. Verify all are blocked. | Egress control is an infrastructure concern, not an MCP protocol concern — the MCP spec does not address it. Enforcement requires network-level controls (security groups, network policies, service mesh egress rules). Cloud metadata endpoint access is a particularly critical gap: if the MCP server runs on EC2/GCE/Azure and can reach the metadata endpoint, an attacker can obtain instance credentials. Ensure IMDSv2 (requiring hop-limited PUT request) is enforced at minimum. |
| **10.5.2** | **Verify that** outbound MCP actions implement execution limits (e.g., timeouts, recursion limits, concurrency caps, or circuit breakers) to prevent unbounded agent-driven tool invocation or chained side effects. | 2 | D/V | **Denial-of-service and runaway agent loops.** In agentic workflows, the model can invoke tools in a loop — each tool response may trigger further tool invocations. Without execution limits, a single prompt injection or model hallucination can cause: (1) resource exhaustion on the MCP server (CPU, memory, connections), (2) excessive calls to downstream APIs (hitting rate limits or incurring costs), (3) cascading side effects (e.g., repeatedly creating records, sending emails, or modifying data). | Review MCP server and orchestrator code for: per-request timeouts, maximum recursion depth for chained tool calls, concurrency limits (max concurrent tool invocations per session), and circuit breakers for downstream API failures. Test by creating a tool that triggers re-invocation and verify the system halts after the configured limit. Verify that timeout enforcement kills the operation cleanly (not just logging a warning). | Execution limits must be enforced at multiple layers: the MCP server (per-tool timeout), the orchestrator/agent framework (max tool calls per turn, max total calls per session), and the infrastructure (request timeout at the load balancer). No standard MCP mechanism exists for declaring or enforcing these limits — they are implementation-specific. Agent frameworks like LangChain and AutoGen have some built-in limits, but they vary in completeness. |
| **10.5.3** | **Verify that** MCP tool invocations classified as high-risk or destructive (e.g., data deletion, financial transactions, system configuration changes) require explicit user confirmation before execution. | 2 | D/V | **Destructive actions via prompt injection or model error.** The model (influenced by prompt injection or hallucination) invokes a destructive tool — deleting a database table, transferring funds, modifying system configuration, or sending emails on behalf of the user. Without a human-in-the-loop confirmation, these actions execute immediately and may be irreversible. | Review the MCP client/orchestrator for a tool classification system that tags tools as high-risk/destructive. Verify that invocation of tagged tools pauses execution and presents a confirmation prompt to the user with the tool name and arguments. Test by invoking a destructive tool and confirming the system blocks until user approval. Verify that the confirmation cannot be bypassed by the model (e.g., by crafting arguments that avoid the classification). | Tool classification is subjective and context-dependent — what is "destructive" varies by organization. The MCP spec defines `annotations` on tools (including `destructiveHint` and `readOnlyHint` in the 2025-03-26 spec), which can be used for classification. However, these annotations are self-reported by the MCP server and could be manipulated by a malicious server. The client should maintain its own classification in addition to honoring server-provided hints. |

---

## Real-World SSRF and Agent Safety Incidents (2025-2026)

| CVE / Incident | CVSS | Description | Impact |
|---|---|---|---|
| CVE-2026-26118 | 8.8 | SSRF in Azure MCP Server Tools (< 2.0.0-beta.17) | Managed identity token theft; impersonation of server identity to access Azure storage, VMs, databases |
| CVE-2026-27826 | 8.2 | SSRF in mcp-atlassian (< 0.17.0) via custom header parsing | Unauthenticated URL injection; cloud metadata credential theft via 169.254.169.254; no Atlassian credentials required |
| CVE-2026-25904 | 5.8 | SSRF in Pydantic-AI mcp-run-python via overly permissive Deno sandbox | Access to cloud metadata services, internal APIs, local databases (Redis, MongoDB, PostgreSQL); project is archived with no fix available |
| CVE-2026-33060 | — | SSRF in @aborruso/ckan-mcp-server via unvalidated `base_url` parameter | Internal network scanning, cloud metadata theft via IMDS; no private IP blocking or URL validation; fixed in v0.4.85 |
| CVE-2025-6514 | 9.6 | Command injection in `mcp-remote` package | ~437,000 compromised downloads; massive supply chain impact |
| CVE-2025-54136 | — | Trust validation bypass in Cursor IDE MCP integration | Silent injection of malicious logic in subsequent updates without re-validation |
| Anthropic mcp-server-git (Jan 2026) | — | Three vulnerabilities: path traversal via `git_init`, argument injection via unsanitized Git CLI args | Arbitrary filesystem access beyond configured boundaries; first-party server flaws |
| Supabase Cursor Agent (mid-2025) | — | Privileged agent processed untrusted support tickets | SQL injection exfiltrated integration tokens via public support thread |

Christian Schneider's "Securing MCP: A Defense-First Architecture Guide" (2025) outlines a layered defense model: Layer 1 network egress controls block SSRF outbound requests, file system root path pinning blocks arbitrary file writes, and runtime sandboxing constrains execution. Elastic Security Labs published MCP-specific attack and defense recommendations for autonomous agents, documenting tool invocation chains where a single prompt injection cascades through 10+ tool calls before triggering any detection.

Endor Labs' research (early 2026) emphasized that indirect prompt injection is the primary attack vector for MCP SSRF — an attacker does not need direct access to the victim's system. Instead, malicious instructions embedded in documents, web content, or design files processed by the LLM can compel it to invoke vulnerable MCP tools with attacker-controlled arguments. This means egress controls and input validation must assume all tool arguments are adversarial, regardless of source.

---

## Defensive Tools and MCP Gateways

As of March 2026, several purpose-built tools have emerged for enforcing egress controls, execution limits, and tool safety at the MCP layer:

| Tool / Framework | Key Capabilities | Notes |
|---|---|---|
| **Lasso Security MCP Gateway** | Plugin-based gateway with PII masking (Presidio), tool reputation scoring (threshold-based blocking at score 30), tool description scanning for hidden instructions, real-time prompt injection detection | Open source; 2024 Gartner Cool Vendor for AI Security; supports SQLite/DuckDB audit logging via Xetrack plugin |
| **IBM MCP Context Forge** | Centralized registry and proxy for MCP/A2A/REST/gRPC; unified endpoint with discovery, guardrails, and management | Supports plugin architecture for custom security policies |
| **mcp-scan** | CLI vulnerability scanner for MCP server implementations; detects common patterns like unvalidated URL parameters, missing egress restrictions, command injection surfaces | Recommended as immediate action by security researchers after the 30-CVE wave |
| **Docker MCP Gateway** | Containerized MCP execution with strict resource limits (CPU, memory caps), no host filesystem access, limited network access by default | Provides infrastructure-level isolation; does not address application-layer SSRF |
| **Kubernetes Network Policies** | Namespace-scoped egress rules; can restrict MCP server pods to specific CIDR blocks and ports; blocks metadata endpoints (169.254.169.254/32) | Requires CNI plugin support (Calico, Cilium); does not inspect application-layer URLs |
| **Istio/Envoy Service Mesh** | Egress gateway with domain-level allowlists, mTLS enforcement, per-service rate limiting | Adds latency; most complete network-level control for service-to-service MCP traffic |

The `MCP_ALLOWED_URL_DOMAINS` configuration variable (introduced in the mcp-atlassian v0.17.0 patch) represents an emerging pattern where MCP servers expose domain allowlists as configuration. This application-layer validation should supplement, not replace, network-level egress controls.

---

## Implementation Guidance

### Egress Control Architecture (10.5.1)

Defense-in-depth requires enforcement at multiple layers:

1. **Network layer:** Security groups, Kubernetes NetworkPolicies, or service mesh egress gateways restrict outbound traffic to approved CIDR blocks. Explicitly deny `169.254.169.254/32` (cloud metadata), `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16` unless specifically required. On AWS, enforce IMDSv2 (hop-limited PUT request with token) to mitigate SSRF even if the metadata endpoint is reachable.

2. **Application layer:** MCP servers and gateways should validate all outbound URLs against domain allowlists. The validation must include DNS lookahead resolution (resolve the hostname before making the request) to prevent DNS rebinding attacks, and must block `file://`, `gopher://`, and other non-HTTP schemes. The mcp-atlassian v0.17.0 `validate_url_for_ssrf()` function is a good reference implementation.

3. **Identity scoping:** Run each MCP server with a minimal-privilege identity. Avoid broad service principals — use per-tool or per-session managed identities where possible. CVE-2026-26118 succeeded because the Azure MCP server had an over-privileged managed identity with access to storage, VMs, and databases.

### Execution Limits and Circuit Breakers (10.5.2)

Execution limits must be enforced at three layers simultaneously:

1. **MCP server:** Per-tool timeouts (kill the operation, not just log a warning), maximum response size limits, and concurrency caps per session.

2. **Orchestrator/agent framework:** Maximum tool calls per turn, maximum total calls per session, recursion depth limits, and cost ceilings. The OWASP Agentic Security Initiative (ASI) calls this the "least agency" principle — agents should receive only the minimum autonomy required for their authorized task.

3. **Infrastructure:** Request timeouts at the load balancer, pod resource limits in Kubernetes, and API gateway rate limiting. Circuit breakers should trip automatically when an agent exceeds token budgets or attempts unauthorized API calls, as mandated by the NIST AI Risk Management Framework's agentic AI profile.

The "denial of wallet" attack is the financial instantiation of unbounded execution: an attacker-crafted input causes the agent to loop, consuming API credits. Organizations should set hard cost ceilings per session and per agent, with automatic termination — not just alerting — when limits are hit.

### Human-in-the-Loop for Destructive Actions (10.5.3)

The MCP spec's `annotations` field (2025-03-26 revision) includes `destructiveHint` and `readOnlyHint`, but these are self-reported by the server and could be manipulated by a malicious server. A robust implementation requires:

1. **Client-maintained classification:** The MCP client or gateway maintains its own tool risk taxonomy, independent of server-provided annotations. Operations involving data deletion, financial transactions, system configuration changes, credential rotation, or external communications should be tagged as high-risk.

2. **Confirmation UX:** When a high-risk tool is invoked, the orchestrator must pause execution and present the user with the tool name, full argument payload, and a clear description of the expected side effects. The confirmation prompt must not be bypassable by the model.

3. **Autonomous fallback:** In fully autonomous workflows (batch processing, scheduled tasks, CI/CD pipelines) where no human is present, high-risk operations should either be queued for deferred human approval, sandboxed for dry-run execution, or rejected outright with an alert to the operations team.

## Related Standards & References

- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Top 10 for Agentic Applications (2026)](https://goteleport.com/blog/owasp-top-10-agentic-applications/) — unbounded consumption, agent goal hijack, human-in-the-loop requirements
- [AWS IMDSv2 documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) — mitigating metadata endpoint SSRF
- [MCP Tool Annotations (2025-03-26 spec)](https://spec.modelcontextprotocol.io/specification/2025-03-26/server/tools/) — `destructiveHint`, `readOnlyHint` annotations
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final) — least-privilege network access
- [NIST AI Risk Management Framework — Agentic AI Profile](https://www.nist.gov/artificial-intelligence) — circuit breaker mandates for autonomous agents
- [Blueinfy: SSRF in Azure MCP Server Tools](https://blog.blueinfy.com/2026/03/ssrf-in-azure-mcp-server-tools.html) — CVE-2026-26118 analysis
- [SentinelOne: CVE-2026-25904 Pydantic-AI MCP SSRF](https://www.sentinelone.com/vulnerability-database/cve-2026-25904/) — Deno sandbox SSRF in archived project
- [Endor Labs: Classic Vulnerabilities Meet AI Infrastructure](https://www.endorlabs.com/learn/classic-vulnerabilities-meet-ai-infrastructure-why-mcp-needs-appsec) — indirect prompt injection as SSRF vector
- [Elastic Security Labs: MCP Tools Attack Vectors and Defense](https://www.elastic.co/security-labs/mcp-tools-attack-defense-recommendations) — agent execution chain analysis
- [Christian Schneider: Securing MCP Defense-First Architecture](https://christian-schneider.net/blog/securing-mcp-defense-first-architecture/) — layered defense model
- [MCP Security 2026: 30 CVEs in 60 Days](https://www.heyuan110.com/posts/ai/2026-03-10-mcp-security-2026/) — vulnerability landscape analysis
- [Lasso Security MCP Gateway](https://github.com/lasso-security/mcp-gateway) — open-source MCP security gateway with tool reputation scoring
- [Checkmarx: 11 Emerging AI Security Risks with MCP](https://checkmarx.com/zero-post/11-emerging-ai-security-risks-with-mcp-model-context-protocol/) — comprehensive risk taxonomy
- [AuthZed: Timeline of MCP Security Breaches](https://authzed.com/blog/timeline-mcp-breaches) — breach chronology
- [Pluto Security: MCPwnfluence — SSRF to RCE in mcp-atlassian](https://pluto.security/blog/mcpwnfluence-cve-2026-27825-critical/) — attack chain analysis
- [Dark Reading: Microsoft & Anthropic MCP Servers at Risk](https://www.darkreading.com/application-security/microsoft-anthropic-mcp-servers-risk-takeovers) — first-party server vulnerabilities

---

## Open Research Questions

- [ ] How should tool risk classification be standardized — is the MCP `annotations` approach sufficient, or does it need a formal taxonomy backed by a registry (similar to CWE for weaknesses)?
- [ ] Can execution limits be specified declaratively in the MCP protocol (e.g., server-advertised rate limits, timeout hints, or cost-per-invocation metadata)?
- [ ] How should human-in-the-loop confirmation work in fully autonomous agent workflows where no user is present (e.g., batch processing, scheduled tasks)? Deferred approval queues and dry-run sandboxing are candidates but lack standardization.
- [ ] Should MCP servers expose their egress allowlist as metadata, allowing clients to assess the server's network reach before connecting? The `MCP_ALLOWED_URL_DOMAINS` pattern in mcp-atlassian v0.17.0 is a step in this direction.
- [ ] Given that CVE-2026-26118 exploited over-privileged managed identities, should MCP deployment standards mandate identity scoping (e.g., per-tool or per-session managed identities rather than broad service principals)?
- [ ] The mcp-scan tool and Lasso Gateway's reputation scoring represent early attempts at automated MCP security assessment — how should these capabilities be standardized for CI/CD integration?
- [ ] With 30+ MCP CVEs filed in two months (Jan-Feb 2026) and the CVE-2026-25904 project being archived without a fix, how should organizations handle abandoned MCP servers with known vulnerabilities?
- [ ] What enforcement mechanisms (not just visibility) should be standard for preventing "denial of wallet" attacks in agentic systems — hard cost ceilings, automatic session termination, or both?

---
