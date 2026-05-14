# C10.5: Outbound Access & Agent Execution Safety

> **Parent:** [C10 MCP Security](C10-MCP-Security.md)
> **Requirements:** 1 | **IDs:** 10.5.1--10.5.1

## Purpose

This section ensures that MCP servers are constrained in what they can reach and how much they can do. MCP servers are code-execution endpoints — when a tool is invoked, the server runs arbitrary logic that may make outbound API calls, access databases, read files, or interact with cloud services. Without egress controls and execution limits, a compromised or manipulated MCP server becomes an unrestricted proxy into the internal network. Additionally, agentic workflows can create unbounded chains of tool invocations where a single prompt injection cascades into dozens of side-effecting operations. This section applies both network-level and execution-level constraints.

The real-world severity of these risks was starkly demonstrated in 2025-2026. CVE-2026-26118 (CVSS 8.8) exposed a critical SSRF vulnerability in Azure MCP Server Tools (versions prior to 2.0.0-beta.17), where low-privileged attackers could craft malicious payloads that tricked the MCP server into leaking its managed identity token — enabling impersonation of the server's Azure identity to access storage accounts, virtual machines, and databases. CVE-2026-27826 (CVSS 8.2) in mcp-atlassian allowed unauthenticated attackers to supply arbitrary URLs via custom `X-Atlassian-Jira-Url` and `X-Atlassian-Confluence-Url` headers without any authentication requirement; in cloud deployments, pointing this at the `169.254.169.254` metadata endpoint stole IAM role credentials. The patch (commit `5cd697d`, fixed in v0.17.0) introduced `validate_url_for_ssrf()` with DNS lookahead resolution to prevent rebinding attacks and IP range validation blocking RFC 1918 and loopback addresses.

As of May 2026, the MCP vulnerability landscape has grown dramatically: the Vulnerable MCP Project (vulnerablemcp.info) now tracks over 50 vulnerabilities across MCP implementations, with 13 rated Critical. Over 30 CVEs targeting MCP infrastructure were filed between January and February 2026 alone, and the wave has not slowed — CVE-2026-32871 (FastMCP OpenAPI Provider), CVE-2026-39885 (mcp-from-openapi), CVE-2026-39974 (n8n-mcp), and CVE-2026-34476 (Apache SkyWalking MCP) were all disclosed from late March through mid-April 2026, repeatedly hitting the same outbound-fetch and SSRF failure mode. BlueRock Security's analysis of more than 7,000 publicly available MCP server implementations confirms the systemic nature of the problem: 36.7% are exposed to SSRF, 43% contain command injection flaws (CWE-78), 67% have code injection risks (CWE-94), and 82% are vulnerable to path traversal in file operations (CWE-22). BlueRock's proof-of-concept against Microsoft's MarkItDown MCP server demonstrated end-to-end IAM credential theft via the EC2 instance metadata service. These are not theoretical risks — they have active proof-of-concept exploits on GitHub and have been exploited in the wild.

On May 12, 2026, OX Security disclosed another cluster that widens the same lesson from outbound HTTP to local execution boundaries: CVE-2025-65719 in Kubectl MCP Server allowed a malicious webpage to reach a locally running MCP server and execute shell commands against Kubernetes credentials; CVE-2025-69443 in Archon OS exposed provider API keys and agent controls through an unauthenticated backend port; and MarkItDown MCP was shown to allow arbitrary `file://` reads under the MCP process's privileges. For C10.5, this means egress policy cannot stand alone. Local MCP services need authentication, strict `Host`/`Origin` handling, loopback-only binding, process sandboxing, and scheme/path allowlists.

The "denial of wallet" attack pattern has also emerged as a significant threat: an attacker crafts input that causes an agent to loop endlessly (via logical paradox or self-generating task chains), rapidly consuming API budgets and compute resources. The NIST AI Risk Management Framework now mandates "circuit breakers" that automatically cut off an agent's access when token budgets or API call limits are exceeded.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **10.5.1** | **Verify that** MCP servers restrict outbound requests to approved internal or external destinations per least-privilege egress policies, with egress to all other targets blocked by default. | 2 | **SSRF and lateral movement via MCP servers.** An attacker (via prompt injection or tool argument manipulation) causes the MCP server to make requests to internal services, cloud metadata endpoints (e.g., `169.254.169.254` for AWS IMDSv1), or other network targets that should not be accessible. The MCP server acts as a confused deputy, using its network position to reach targets the attacker cannot reach directly. This is a server-side request forgery (SSRF) pattern specific to MCP. | Review network policies (firewall rules, security groups, network policies in Kubernetes) applied to MCP server workloads. Verify egress is restricted to an allowlist of approved destinations. Test by attempting to make requests from the MCP server to cloud metadata endpoints, internal services not on the allowlist, and arbitrary external URLs. Verify all are blocked. | Egress control is an infrastructure concern, not an MCP protocol concern — the MCP spec does not address it. Enforcement requires network-level controls (security groups, network policies, service mesh egress rules). Cloud metadata endpoint access is a particularly critical gap: if the MCP server runs on EC2/GCE/Azure and can reach the metadata endpoint, an attacker can obtain instance credentials. Ensure IMDSv2 (requiring hop-limited PUT request) is enforced at minimum. |

---

## Real-World SSRF and Agent Safety Incidents (2025-2026)

| CVE / Incident | CVSS | Description | Impact |
|---|---|---|---|
| CVE-2026-39885 | 7.5 | SSRF + LFI in FrontMCP `mcp-from-openapi` (< 2.3.0) via `$ref` dereferencing in untrusted OpenAPI specs | Disclosed April 8, 2026. Malicious OpenAPI spec with `$ref` values pointing to internal addresses, cloud metadata, or `file://` paths is fetched during `initialize()` via @apidevtools/json-schema-ref-parser with no URL restrictions. Fixed in mcp-from-openapi 2.3.0 (default blocklist, optional `allowedHosts` allowlist via `refResolution` options) and frontmcp/@frontmcp/sdk 1.0.4 |
| CVE-2026-32871 | — | Authenticated SSRF + path traversal in FastMCP OpenAPI Provider (< 3.2.0) | The `_build_url()` method substitutes path parameters into URL templates without URL-encoding; `urljoin()` interprets `../` as directory traversal, allowing attackers to escape the configured API prefix and reach arbitrary backend endpoints. Requests carry the provider's configured authorization headers, so the SSRF is **authenticated** — privilege escalation via the MCP provider's credential context. Fixed in FastMCP 3.2.0 (commit `40bdfb6`); reference advisory GHSA-vv7q-7jx5-f767 |
| CVE-2026-39974 | 8.5 | Authenticated SSRF in `n8n-mcp` (<= 2.47.3) via multi-tenant HTTP headers | Disclosed April 8, 2026. A caller with a valid `AUTH_TOKEN` could supply arbitrary instance URLs through multi-tenant headers and receive reflected response bodies through JSON-RPC, including cloud metadata and internal service responses. Fixed in 2.47.4; the advisory also recommends blocking RFC 1918, link-local, and metadata ranges at the network layer. |
| CVE-2026-34476 | 7.1 | SSRF in Apache SkyWalking MCP 0.1.0 via the `SW-URL` header | Disclosed April 13, 2026 by the Apache Software Foundation. Authenticated callers could forge server-side requests to destinations reachable by the SkyWalking MCP process. Fixed in 0.2.0. |
| CVE-2026-35568 | 7.6 | DNS rebinding in the official MCP Java SDK (< 1.0.0) | Disclosed April 7, 2026. Missing `Origin` header validation let a malicious website reach local or private-network MCP servers and make tool calls as if it were a local MCP-connected agent. Fixed in 1.0.0; reverse proxies should strictly validate `Host` and `Origin` headers. |
| CVE-2026-26118 | 8.8 | SSRF in Azure MCP Server Tools (< 2.0.0-beta.17) | Managed identity token theft; impersonation of server identity to access Azure storage, VMs, databases |
| CVE-2026-27826 | 8.2 | SSRF in mcp-atlassian (< 0.17.0) via custom header parsing | Unauthenticated URL injection; cloud metadata credential theft via 169.254.169.254; no Atlassian credentials required. Patched in v0.17.0 (released February 23, 2026) with `validate_url_for_ssrf()` (DNS lookahead, private-IP and reserved-range blocking, redirect validation) |
| CVE-2026-25904 | 5.8 | SSRF in Pydantic-AI mcp-run-python via overly permissive Deno sandbox | Access to cloud metadata services, internal APIs, local databases (Redis, MongoDB, PostgreSQL); project is archived with no fix available |
| CVE-2026-33060 | — | SSRF in @aborruso/ckan-mcp-server via unvalidated `base_url` parameter | Internal network scanning, cloud metadata theft via IMDS; no private IP blocking or URL validation; fixed in v0.4.85 |
| CVE-2025-6514 | 9.6 | Command injection in `mcp-remote` package | ~437,000 compromised downloads; massive supply chain impact |
| CVE-2025-54136 | — | Trust validation bypass in Cursor IDE MCP integration | Silent injection of malicious logic in subsequent updates without re-validation |
| Anthropic mcp-server-git (Jan 2026) | — | Three vulnerabilities: path traversal via `git_init`, argument injection via unsanitized Git CLI args | Arbitrary filesystem access beyond configured boundaries; first-party server flaws |
| CVE-2026-32111 | 5.3 | SSRF in ha-mcp OAuth beta (< 7.0.0) via unvalidated `ha_url` parameter | Error-oracle network reconnaissance; attacker registers client via open DCR, submits arbitrary internal URLs to consent form; two additional code paths (REST/WebSocket OAuth tool calls) share the same primitive |
| CVE-2026-0755 | 9.8 | Command injection in gemini-mcp-tool via unsanitized user input passed to shell | Zero-day with no patch available as of March 2026; trivial exploitability |
| CVE-2026-23744 | 9.8 | MCPJam Inspector RCE — default binding on 0.0.0.0 with no authentication | Crafted HTTP requests enable arbitrary code execution on any exposed instance |
| CVE-2025-65513 | 9.3 | SSRF in Fetch MCP Server — private IP validation bypass | Targets internal services via metadata endpoints; easy exploitability |
| CVE-2025-65719 | Critical | Kubectl MCP Server RCE in versions before 1.2.0 | A malicious webpage can connect to a locally running server and trigger shell command execution, putting local credentials and reachable Kubernetes clusters at risk. |
| CVE-2025-69443 | High | Archon OS unauthenticated web-to-client boundary failure | Backend port 8181 lacked the CORS/authentication protections present on the UI port, exposing OpenAI, Grok, Google, and other configured API keys and allowing unauthorized agent control. No fixed version was available as of the May 12, 2026 disclosure. |
| OX Security MCP STDIO advisory (Apr 2026) | — | Command execution across MCP STDIO configuration paths in multiple agent platforms | The disclosure family covers direct STDIO configuration, allowlist bypass through allowed interpreters such as `npx`, prompt-injection changes to MCP JSON configuration, and hidden backend STDIO triggers. This reinforces that outbound-access controls must be paired with execution configuration allowlists and sandboxed runners. |
| Microsoft MarkItDown MCP Server | — | Unbounded URI handling across network and local file schemes | BlueRock demonstrated AWS metadata credential theft via arbitrary URL fetching; OX separately documented arbitrary `file://` reads of SSH keys, cloud credentials, source code, and configuration files under the process's permissions. |
| Supabase Cursor Agent (mid-2025) | — | Privileged agent processed untrusted support tickets | SQL injection exfiltrated integration tokens via public support thread |

Christian Schneider's "Securing MCP: A Defense-First Architecture Guide" (2025) outlines a layered defense model: Layer 1 network egress controls block SSRF outbound requests, file system root path pinning blocks arbitrary file writes, and runtime sandboxing constrains execution. Elastic Security Labs published MCP-specific attack and defense recommendations for autonomous agents, documenting tool invocation chains where a single prompt injection cascades through 10+ tool calls before triggering any detection.

Endor Labs' research (early 2026) emphasized that indirect prompt injection is the primary attack vector for MCP SSRF — an attacker does not need direct access to the victim's system. Instead, malicious instructions embedded in documents, web content, or design files processed by the LLM can compel it to invoke vulnerable MCP tools with attacker-controlled arguments. This means egress controls and input validation must assume all tool arguments are adversarial, regardless of source.

The April 2026 STDIO command-execution disclosures broaden the lesson: restricting outbound destinations is necessary but not sufficient when the MCP client can also start local processes. Auditors should treat MCP server configuration as an execution boundary. Approved server manifests, immutable command paths, blocked shell metacharacters, interpreter argument allowlists, and containerized execution are now baseline expectations for any environment that permits STDIO MCP servers.

---

## Defensive Tools and MCP Gateways

As of March 2026, several purpose-built tools have emerged for enforcing egress controls, execution limits, and tool safety at the MCP layer:

| Tool / Framework | Key Capabilities | Notes |
|---|---|---|
| **Lasso Security MCP Gateway** | Plugin-based gateway with PII masking (Presidio), tool reputation scoring (threshold-based blocking at score 30), tool description scanning for hidden instructions, real-time prompt injection detection | Open source; 2024 Gartner Cool Vendor for AI Security; supports SQLite/DuckDB audit logging via Xetrack plugin |
| **IBM MCP Context Forge** | Centralized registry and proxy for MCP/A2A/REST/gRPC; unified endpoint with discovery, guardrails, and management | Supports plugin architecture for custom security policies |
| **mcp-scan** | CLI vulnerability scanner for MCP server implementations; detects common patterns like unvalidated URL parameters, missing egress restrictions, command injection surfaces | Recommended as immediate action by security researchers after the 30-CVE wave |
| **Docker MCP Gateway** | Containerized MCP execution with restricted privileges, network access, resource usage, logging, and call tracing; `docker mcp gateway run` exposes controls such as `--block-network`, `--block-secrets`, and per-server CPU caps | Strong fit for local and developer workstation isolation; still needs application-layer URL validation and explicit destination allowlists for servers that make outbound HTTP calls |
| **Kubernetes Network Policies** | Namespace-scoped egress rules; can restrict MCP server pods to specific CIDR blocks and ports; blocks metadata endpoints (169.254.169.254/32) | Requires CNI plugin support (Calico, Cilium); does not inspect application-layer URLs |
| **Istio/Envoy Service Mesh** | Egress gateway with domain-level allowlists, mTLS enforcement, per-service rate limiting | Adds latency; most complete network-level control for service-to-service MCP traffic |
| **Traefik Hub Triple Gate (v3.20)** | MCP Gateway with composable safety pipeline (parallel guard execution), token-level cost controls with proactive estimation, per-user/team/endpoint quota tracking via JWT claims, automatic failover across LLM providers, IBM Granite Guardian integration | Early access as of March 2026; GA planned late April 2026. Agent-aware enforcement returns structured refusal responses (HTTP 200) so agents continue operating gracefully |
| **Microsoft Agent Governance Toolkit** | Deterministic policy enforcement (<0.1ms per action), execution rings, circuit breakers, SLO tracking, Ed25519 inter-agent identity, SPIFFE/SVID credentials, trust scoring, OpenTelemetry metrics | Covers all 10 OWASP Agentic Top 10 risks; integrates with LangChain, CrewAI, AutoGen, OpenAI Agents, Google ADK, Dify, LlamaIndex (12+ frameworks) |
| **Agent Budget Guard** | MCP server providing real-time cost tracking and AgentWatchdog runtime circuit breaker for hard budget caps; agents gain native cost awareness via MCP tool calls | Addresses denial-of-wallet at the runtime layer; `pip install agent-budget-guard` |
| **MCPTox** | Monitors and flags suspicious prompt patterns targeting MCP tool invocations | Early-stage detection tool; useful for identifying prompt injection attempts directed at MCP tools |
| **MindGuard** | Real-time anomalous behavior detection for MCP-connected agents | Behavioral analysis layer; complements network-level and policy-level controls |
| **PointGuard AI MCP Security Gateway** | Centralized control point for agent-to-tool interactions: zero-trust authorization, granular tool permissions, real-time interaction inspection, human-in-the-loop approval for high-risk actions | Launched March 2026; secure-by-design philosophy embeds governance into agent development lifecycle; enterprise identity integration |
| **Bifrost** | Virtual Keys enforce strict allow-lists for MCP client/tool access; federated authentication passes user-level credentials upstream; blocks automatic tool execution by default | Agent Mode allows configurable auto-approval for designated low-risk tools only; vault integration with HashiCorp, AWS, Google, and Azure |
| **Lunar.dev MCPX** | Tool-level RBAC (allow read-only, block writes within servers); parameter locking to prevent unsafe tool configurations | ~4ms p99 latency; on-premises deployment; administrators can lock individual parameters per tool |
| **OPA + Ephemeral Runners (reference architecture)** | Rego-based policy externalization: RBAC, plan hash integrity checks, destructive operation blocking, change-window enforcement; ephemeral Kubernetes namespace per execution with mandatory cleanup | Policy decision latency <100ms; runner startup <5s; InfoQ reference implementation for least-privilege AI agent gateways |
| **Kong Agent Gateway (AI Gateway 3.14)** | Released April 14, 2026. Single control plane spanning LLM, MCP, and agent-to-agent (A2A) traffic; full audit logging of A2A conversations; granular per-agent token and resource consumption tracking; centralized policy enforcement integrated with Kong API Management and Event Management | First commercial gateway to govern all three native AI traffic types from one control point; available immediately within Kong Konnect. Pairs natively with Kong's existing rate-limiting, OAuth, and mTLS plugins for egress enforcement |
| **Uber GenAI Gateway** | Production Go-based MCP gateway processing tens of thousands of agent executions weekly; auto-exposes thousands of internal Thrift, Protobuf, and HTTP endpoints; performs PII redaction and internal-identifier scrubbing before requests leave the gateway | Presented at MCP Dev Summit NA (April 2-3, 2026) as a reference architecture for enterprise-scale MCP deployment; not open-sourced but the design pattern (gateway as the egress chokepoint) is widely cited |

The `MCP_ALLOWED_URL_DOMAINS` configuration variable (introduced in the mcp-atlassian v0.17.0 patch) represents an emerging pattern where MCP servers expose domain allowlists as configuration. This application-layer validation should supplement, not replace, network-level egress controls.

---

## Implementation Guidance

### Egress Control Architecture (10.5.1)

Defense-in-depth requires enforcement at multiple layers:

1. **Network layer:** Security groups, Kubernetes NetworkPolicies, or service mesh egress gateways restrict outbound traffic to approved CIDR blocks. Explicitly deny `169.254.169.254/32` (cloud metadata), `10.0.0.0/8`, `172.16.0.0/12`, and `192.168.0.0/16` unless specifically required. On AWS, enforce IMDSv2 (hop-limited PUT request with token) to mitigate SSRF even if the metadata endpoint is reachable.

2. **Application layer:** MCP servers and gateways should validate all outbound URLs against domain allowlists. The validation must include DNS lookahead resolution (resolve the hostname before making the request) to prevent DNS rebinding attacks, pin the resolved address between check and use where possible, validate every redirect hop, and block `file://`, `gopher://`, and other non-HTTP schemes. The mcp-atlassian v0.17.0 `validate_url_for_ssrf()` function is a good reference implementation. The official MCP security guidance also recommends blocking private, loopback, link-local, and private IPv6 ranges, and routing server-side MCP traffic through egress proxies such as Smokescreen where application validation is not enough.

3. **Identity scoping:** Run each MCP server with a minimal-privilege identity. Avoid broad service principals — use per-tool or per-session managed identities where possible. CVE-2026-26118 succeeded because the Azure MCP server had an over-privileged managed identity with access to storage, VMs, and databases.

4. **HTTP transport origin controls:** For streamable HTTP and SSE transports, validate both `Host` and `Origin` headers at the MCP server or reverse proxy. CVE-2026-35568 showed that a DNS rebinding attack can turn a user's browser into a bridge to local or private-network MCP servers, enabling tool calls even when the server is not directly internet-exposed.

5. **STDIO execution controls:** For local STDIO servers, treat `command` and `args` as privileged configuration, not normal user input. Require approved manifests, avoid shell invocation, pin absolute executable paths, reject interpreter flags that enable command execution, and run servers in short-lived containers or sandboxes with no host filesystem access unless explicitly required.

6. **Local web-to-client boundary controls:** Treat localhost MCP and agent-control ports as remotely reachable from the browser threat model. Bind services to `127.0.0.1` only, require authentication even for loopback HTTP, validate `Host` and `Origin` on every exposed port, disable wildcard CORS, and test with a malicious webpage that attempts to call local MCP endpoints. CVE-2025-65719 and CVE-2025-69443 both show why "local-only" is not a sufficient control.

Verification should include both browser-origin probes and raw HTTP clients, because CORS only controls browser reads and does not authenticate the backend service or prevent non-browser local callers.

7. **URI and filesystem scopes:** Disable `file://`, `data:`, and unrestricted `http(s)` URI handlers unless the tool's purpose requires them. When conversion or fetch tools need broad input support, enforce explicit scheme allowlists, domain allowlists, path roots, read-only mounts, and deny tests for `file:///etc/passwd`, `~/.ssh`, cloud credential directories, and cloud metadata endpoints before production approval.

### Execution Limits and Circuit Breakers (10.5.2)

Execution limits must be enforced at three layers simultaneously:

1. **MCP server:** Per-tool timeouts (kill the operation, not just log a warning), maximum response size limits, and concurrency caps per session.

2. **Orchestrator/agent framework:** Maximum tool calls per turn, maximum total calls per session, recursion depth limits, and cost ceilings. The OWASP Agentic Security Initiative (ASI) calls this the "least agency" principle — agents should receive only the minimum autonomy required for their authorized task.

3. **Infrastructure:** Request timeouts at the load balancer, pod resource limits in Kubernetes, and API gateway rate limiting. Circuit breakers should trip automatically when an agent exceeds token budgets or attempts unauthorized API calls, as mandated by the NIST AI Risk Management Framework's agentic AI profile.

The "denial of wallet" attack is the financial instantiation of unbounded execution: an attacker-crafted input causes the agent to loop, consuming API credits. Organizations should set hard cost ceilings per session and per agent, with automatic termination — not just alerting — when limits are hit. A well-documented implementation pattern uses three hierarchical rate-limiting layers: (1) a token-bucket at the minute level for burst control, (2) a daily quota as a short-term ceiling, and (3) a weekly quota as the ultimate cost cap. All layers must approve each request — this prevents timing-based exploits where attackers game daily reset windows. Cost estimation uses optimistic locking with refunds: the system pre-reserves estimated cost before LLM processing (based on input token count and max output tokens), then refunds the difference after generation completes. Budget units map to real dollars (e.g., 1 unit = $0.001), making quota enforcement directly translatable to financial limits.

As of March 2026, runtime enforcement tooling has matured significantly. Traefik Hub v3.20 tracks input, output, and total tokens independently with per-user, per-team, and per-endpoint granularity via JWT claims — and critically, it uses proactive token estimation to block abusive requests *before* the prompt reaches the LLM, rather than enforcing limits reactively. The Microsoft Agent Governance Toolkit takes a different approach: every agent action is evaluated against policy at sub-millisecond latency, with deterministic enforcement using execution rings and saga orchestration for multi-step workflows. Agent Budget Guard provides cost awareness directly to the agent via MCP, letting agents self-monitor their own spending in real-time. The emerging best practice is a graduated response pattern: log, warn, throttle, hard stop — giving operators visibility into approaching limits while guaranteeing a hard ceiling.

For long-running tools, MCP Tasks add another resource-management surface. The 2025-11-25 task specification requires task receivers to bind task state to the authorization context when one exists, reject cross-context `tasks/get`, `tasks/result`, and `tasks/cancel` requests, and enforce limits such as maximum TTL and concurrent tasks per requestor. Verification should include task cancellation tests and quota tests, because otherwise asynchronous work can keep consuming egress, credentials, and compute after the initiating session has ended.

### Human-in-the-Loop for Destructive Actions (10.5.3)

The MCP spec's `annotations` field (2025-03-26 revision) includes `destructiveHint` and `readOnlyHint`, but these are self-reported by the server and could be manipulated by a malicious server. A robust implementation requires:

1. **Client-maintained classification:** The MCP client or gateway maintains its own tool risk taxonomy, independent of server-provided annotations. Operations involving data deletion, financial transactions, system configuration changes, credential rotation, or external communications should be tagged as high-risk. A tiered approach is becoming standard practice: Tier 1 (auto-approved for read-only queries), Tier 2 (single confirmation for atomic operations), Tier 3 (confirmation plus audit logs), and Tier 4 (multi-party approval following the four-eyes principle for high-impact changes).

2. **Confirmation UX:** When a high-risk tool is invoked, the orchestrator must pause execution and present the user with the tool name, full argument payload, and a clear description of the expected side effects. The OWASP MCP Security Cheat Sheet explicitly warns against showing summaries instead of actual arguments — the user must see the real parameters to detect prompt injection payloads like exfiltration URLs or unexpected recipients. The confirmation prompt must not be bypassable by the model.

3. **Autonomous fallback:** In fully autonomous workflows (batch processing, scheduled tasks, CI/CD pipelines) where no human is present, high-risk operations should either be queued for deferred human approval, sandboxed for dry-run execution, or rejected outright with an alert to the operations team. Cloudflare Agents implements this via `waitForApproval()` with configurable timeouts (up to 7 days) and automatic escalation, backed by SQL-based audit trails recording approver identity, timestamp, and rationale.

### MCP Elicitation: Protocol-Native Confirmation (10.5.3)

The MCP 2025-11-25 specification introduced **elicitation** as a first-class protocol primitive, giving servers a standardized way to request user input mid-execution. This directly addresses the human-in-the-loop requirement for destructive actions:

- **Form mode:** The server sends an `ElicitationRequest` with a JSON Schema describing required input fields (string, number, boolean primitives). The client renders a form, collects user responses, and returns them to the server. The client should allow users to review and modify responses before sending, and must support outright rejection of the request.

- **URL mode:** Introduced in 2025-11-25 for sensitive interactions (e.g., OAuth flows, payment confirmations). The server provides a URL that opens in the user's browser for out-of-band interaction. The LLM client never sees sensitive tokens — it only receives a completion callback. This is particularly valuable for financial transaction confirmations under 10.5.3.

Framework support for elicitation-based approval is growing. LangGraph provides native `interrupt()` for mid-workflow pauses. CrewAI supports `human_input` flags and `HumanTool` patterns. HumanLayer offers cross-channel approval via Slack, Email, and Discord with `@require_approval()` decorators. Permit.io integrates authorization-as-a-service with ReBAC (relationship-based access control) for policy-driven approval flows. Combining these — for instance, LangGraph + MCP Adapters + Permit.io — provides full control, flexibility, and policy enforcement across the approval lifecycle.

## Regulatory and Standards Landscape

In February 2026, NIST launched the **AI Agent Standards Initiative** through its Center for AI Standards and Innovation (CAISI), specifically targeting autonomous AI agents with a three-pillar strategy: facilitating industry-led agent standards, fostering open-source protocol development, and advancing research in AI agent security and identity. NIST's National Cybersecurity Center of Excellence (NCCoE) released the companion concept paper *Accelerating the Adoption of Software and AI Agent Identity and Authorization* on February 5, 2026, with the public comment period closing April 2, 2026. The paper invites feedback on identification and authorization mechanisms for AI agents, auditing and non-repudiation requirements, and prompt-injection mitigation controls — all of which directly bear on the outbound access and execution safety concerns in this section. NCCoE will use the comment input to scope a follow-on demonstration project or other practical guidance.

The **MCP Dev Summit North America 2026** (April 2-3, New York Marriott Marquis, ~1,200 attendees, hosted by the Linux Foundation's Agentic AI Foundation) marked an architectural turning point: Amazon, Docker, Kong, Solo.io, and Uber all converged on the **gateway-as-egress-chokepoint** pattern as the production-grade answer to the SSRF and execution-budget problems documented above. Arcade.dev CEO Alex Salazar articulated the underlying principle: separate the LLM reasoning layer from the action layer, and place all governance, authorization, and egress enforcement at the action-layer boundary. The protocol also continues to evolve — SEP-1442 introduces stateless requests for streamable HTTP, and **SEP-1686** (Tasks, shipped November 25, 2025) defines a durable async task primitive with a five-state machine (`working`, `input_required`, `completed`, `failed`, `cancelled`). For outbound-access controls this matters because long-running tool calls now persist server-side beyond the originating session, expanding the window during which egress policies, budget caps, and circuit breakers must remain enforceable.

The **EU AI Act** Article 14 mandates that humans must be able to understand what an AI system is doing, spot problems, and stop it — for autonomous agents, this translates directly to the requirement that a human can see a flagged request and approve, deny, or modify it before execution. Gartner projects that 40% of enterprise applications will embed task-specific AI agents by 2026, up from less than 5% in 2025, making these regulatory requirements immediately relevant to most organizations.

---

## Related Standards & References

- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) — SSRF controls, private-range blocking, redirect validation, DNS rebinding considerations, and egress proxy guidance
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
- [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html) — sandbox isolation, resource controls, explicit user confirmation guidance
- [MCP Elicitation Specification (2025-11-25)](https://modelcontextprotocol.io/specification/draft/client/elicitation) — protocol-native form-mode and URL-mode user input requests
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) — policy enforcement, execution rings, circuit breakers for 12+ agent frameworks
- [Traefik Hub Triple Gate: MCP Runtime Governance](https://www.helpnetsecurity.com/2026/03/17/traefik-labs-triple-gate-new-capabilities/) — composable safety pipelines, token-level cost controls (v3.20, March 2026)
- [Agent Budget Guard](https://earezki.com/ai-news/2026-03-02-i-built-an-mcp-server-so-my-ai-agent-can-track-its-own-spending/) — runtime cost tracking and circuit breaker via MCP
- [Cloudflare Agents: Human-in-the-Loop Patterns](https://developers.cloudflare.com/agents/guides/human-in-the-loop/) — waitForApproval(), MCP elicitation, tiered approval workflows
- [Permit.io: Human-in-the-Loop for AI Agents](https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo) — ReBAC authorization, framework comparison (LangGraph, CrewAI, HumanLayer)
- [Equixly: Offensive Security for MCP Servers](https://equixly.com/blog/2026/02/26/offensive-security-for-mcp-servers/) — penetration testing techniques for MCP
- [The Vulnerable MCP Project](https://vulnerablemcp.info/) — comprehensive database tracking 50+ MCP vulnerabilities with severity ratings
- [NIST AI Agent Standards Initiative (Feb 2026)](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) — identity, authorization, and security standards for autonomous AI agents
- [Denial of Wallet: Cost-Aware Rate Limiting (Part 3)](https://handsonarchitects.com/blog/2026/denial-of-wallet-cost-aware-rate-limiting-part-3/) — hierarchical token bucket, daily/weekly quota enforcement with optimistic locking
- [InfoQ: Building a Least-Privilege AI Agent Gateway](https://www.infoq.com/articles/building-ai-agent-gateway-mcp/) — OPA + ephemeral runners reference architecture for MCP policy enforcement
- [PointGuard AI MCP Security Gateway](https://www.pointguardai.com/mcp-security-gateway) — zero-trust authorization and human-in-the-loop approval for MCP tool invocations
- [Top 5 MCP Gateways for Regulated Industries (2026)](https://www.getmaxim.ai/articles/top-5-mcp-gateways-for-regulated-industries-in-2026/) — Bifrost, Lasso, Lunar.dev MCPX, Azure, Docker gateway comparison
- [CVE-2026-32111: ha-mcp SSRF via OAuth consent form](https://advisories.gitlab.com/pkg/pypi/ha-mcp/CVE-2026-32111/) — error-oracle network reconnaissance via unvalidated ha_url
- [Microsoft: Secure Agentic AI End-to-End (March 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/20/secure-agentic-ai-end-to-end/) — enterprise framework for agent security governance
- [CVE-2026-32871: FastMCP OpenAPI Provider SSRF + Path Traversal](https://advisories.gitlab.com/pkg/pypi/fastmcp/CVE-2026-32871/) — authenticated SSRF via unencoded path parameters in `_build_url()`; fixed in 3.2.0
- [GHSA-vv7q-7jx5-f767: FastMCP OpenAPI Provider Advisory](https://github.com/PrefectHQ/fastmcp/security/advisories/GHSA-vv7q-7jx5-f767) — upstream advisory for CVE-2026-32871
- [CVE-2026-39885: FrontMCP mcp-from-openapi $ref Dereferencing SSRF + LFI](https://advisories.gitlab.com/pkg/npm/@frontmcp/sdk/CVE-2026-39885/) — fixed in mcp-from-openapi 2.3.0 / @frontmcp/sdk 1.0.4 (April 8, 2026 disclosure)
- [GHSA-4ggg-h7ph-26qr: n8n-mcp authenticated SSRF](https://github.com/czlonkowski/n8n-mcp/security/advisories/GHSA-4ggg-h7ph-26qr) — multi-tenant HTTP header SSRF fixed in n8n-mcp 2.47.4
- [CVE-2026-34476: Apache SkyWalking MCP SSRF](https://seclists.org/oss-sec/2026/q2/116) — `SW-URL` header SSRF in Apache SkyWalking MCP 0.1.0, fixed in 0.2.0
- [GHSA-8jxr-pr72-r468: MCP Java SDK DNS Rebinding](https://github.com/modelcontextprotocol/java-sdk/security/advisories/GHSA-8jxr-pr72-r468) — missing Origin validation fixed in Java SDK 1.0.0
- [OX Security: MCP STDIO Command Injection Advisory](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/) — April 2026 disclosure family covering STDIO command execution paths across agent platforms
- [Docker MCP Gateway documentation](https://docs.docker.com/ai/mcp-gateway/) — containerized MCP server lifecycle, restricted privileges, resource limits, and gateway controls
- [BlueRock Security: SSRF in MarkItDown MCP](https://blog.cyberdesserts.com/ai-agent-security-risks/) — analysis of 7,000+ MCP servers showing 36.7% SSRF exposure; AWS IAM credential theft PoC
- [InfoQ: AAIF MCP Dev Summit 2026 Coverage](https://www.infoq.com/news/2026/04/aaif-mcp-summit/) — gateway pattern convergence (Amazon, Docker, Kong, Solo.io, Uber); SEP-1442 stateless requests; SEP-1686 tasks primitive
- [Kong AI Gateway 3.14 / Agent Gateway (April 14, 2026)](https://www.prnewswire.com/news-releases/kong-ai-gateway-now-supports-agent-to-agent-traffic-becoming-the-most-comprehensive-ai-gateway-for-the-agentic-era-302741741.html) — unified governance for LLM, MCP, and A2A traffic
- [NCCoE Concept Paper: Software and AI Agent Identity and Authorization (Feb 2026)](https://www.nccoe.nist.gov/news-insights/new-concept-paper-identity-and-authority-software-agents) — comment period closed April 2, 2026
- [SEP-1686: MCP Tasks Primitive](https://modelcontextprotocol.io/community/seps/1686-tasks) — durable async task state machine (five states), shipped November 25, 2025
- [Lunar.dev: Best Open Source MCP Gateways 2026](https://www.lunar.dev/post/the-best-open-source-mcp-gateways-in-2026) — comparative analysis of open-source gateway options for egress and policy enforcement
- [OX Security: CVE-2025-65719 Kubectl MCP Server RCE](https://www.ox.security/blog/cve-2025-65719-critical-rce-in-kubectl-mcp-server/) — malicious webpage to localhost MCP command execution; fixed in 1.2.0
- [OX Security: CVE-2025-69443 Archon OS Web-to-Client Vulnerability](https://www.ox.security/blog/cve-2025-69443-archon-os-vulnerable-to-unauthenticated-web-to-client-attack/) — unauthenticated backend API key exposure and agent-control risk
- [OX Security: MarkItDown MCP File Theft](https://www.ox.security/blog/markitdown-mcp-exposes-developer-machines-to-file-theft/) — arbitrary local file read through MarkItDown MCP URI handling
- [Digital Identity for Agentic Systems](https://arxiv.org/abs/2605.11487) — May 2026 preprint on constrained, auditable, revocable authorization for autonomous agents

---

## Open Research Questions

- [ ] How should tool risk classification be standardized — is the MCP `annotations` approach sufficient, or does it need a formal taxonomy backed by a registry (similar to CWE for weaknesses)?
- [ ] Can execution limits be specified declaratively in the MCP protocol (e.g., server-advertised rate limits, timeout hints, or cost-per-invocation metadata)?
- [ ] How should human-in-the-loop confirmation work in fully autonomous agent workflows where no user is present? Cloudflare's `waitForApproval()` with timeout-based escalation and MCP elicitation's URL mode are early implementations, but standardization across frameworks is lacking.
- [ ] Should MCP servers expose their egress allowlist as metadata, allowing clients to assess the server's network reach before connecting? The `MCP_ALLOWED_URL_DOMAINS` pattern in mcp-atlassian v0.17.0 is a step in this direction.
- [ ] Given that CVE-2026-26118 exploited over-privileged managed identities, should MCP deployment standards mandate identity scoping (e.g., per-tool or per-session managed identities rather than broad service principals)?
- [ ] The mcp-scan tool and Lasso Gateway's reputation scoring represent early attempts at automated MCP security assessment — how should these capabilities be standardized for CI/CD integration?
- [ ] With 30+ MCP CVEs filed in two months (Jan-Feb 2026) and the CVE-2026-25904 project being archived without a fix, how should organizations handle abandoned MCP servers with known vulnerabilities?
- [ ] What enforcement mechanisms (not just visibility) should be standard for preventing "denial of wallet" attacks in agentic systems? Traefik Hub's proactive token estimation and Agent Budget Guard's runtime circuit breakers represent two approaches (pre-request blocking vs. runtime cost tracking), but no consensus exists on which layer should be authoritative.
- [ ] With the MCP 2025-11-25 elicitation primitive now available, should MCP gateways automatically intercept and inject elicitation requests for tools classified as destructive, even if the server did not request one? This would create a gateway-enforced approval layer independent of server cooperation.
- [ ] The NIST AI Agent Standards Initiative (launched February 2026) is developing agent identity and authorization standards — how should MCP egress controls and execution limits integrate with the forthcoming NIST identity framework for agents? Should MCP servers expose their network reach and execution limits as discoverable metadata for upstream policy engines?
- [ ] Externalized policy engines (OPA/Rego) for MCP authorization show promise in reference architectures, but adoption remains low. Should the MCP spec standardize a policy decision point interface, allowing gateways to delegate authorization to external engines without custom integration per vendor?
- [ ] CVE-2026-32871 (FastMCP) and CVE-2026-39885 (mcp-from-openapi) both exploit SSRF in **OpenAPI-driven** MCP servers — path-parameter interpolation and `$ref` dereferencing respectively. Should OpenAPI-to-MCP frameworks ship with SSRF-safe defaults (URL-encoded interpolation, ref-resolver allowlists, `file://` scheme blocking) baked in, rather than leaving these to downstream users? A common "mcp-openapi-safe" baseline library could prevent the entire class of bugs.
- [ ] SEP-1686 introduces durable MCP tasks that outlive their originating session. How should egress policies, rate limits, and circuit breakers be evaluated against task state rather than session state — particularly for tasks in `input_required` that may resume days later under different quota and policy regimes?
- [ ] The MCP Dev Summit 2026 showed convergence on the gateway-as-egress-chokepoint pattern across Amazon, Docker, Kong, Solo.io, and Uber, but implementations diverge on control-plane model (Rego, native policy DSLs, rules engines), identity scheme (OAuth, mTLS, SPIFFE/SVID), and audit format. Is there a minimum set of gateway telemetry (egress destination, egress policy decision, agent identity, cost accounting) that the MCP spec or NCCoE could standardize to enable cross-vendor SIEM integration?
- [ ] Browser-to-localhost attacks against MCP-adjacent services keep recurring. Should MCP profiles require a local-service security baseline — authenticated loopback HTTP, strict `Host`/`Origin`, CSRF defenses, and tool-call authorization — before clients are allowed to auto-discover or connect to a local server?

## Related Pages

- [Appendix D Controls Inventory](../../appendices/Appendix-D-Controls-Inventory.md) — maps C10.5-style egress, gateway, and runtime controls into the broader control catalog used for audit planning.
- [C02-01 Prompt Injection Defense](../C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) — pairs with this page where indirect prompt injection supplies unsafe MCP tool arguments or server configuration.
- [C09-03 Tool and Plugin Isolation](../C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md) — covers sandboxing, manifest enforcement, and task-aware quotas for the tools governed by C10.5 egress controls.
- [C09-05 Secure Messaging](../C09-Orchestration-and-Agents/C09-05-Secure-Messaging.md) — complements egress policy with message-level validation before tool output or agent messages cross trust boundaries.
- [C09-09 Data Flow Isolation and Origin Enforcement](../C09-Orchestration-and-Agents/C09-09-Data-Flow-Isolation-Origin-Enforcement.md) — expands the origin and provenance controls needed to decide which outbound tool requests are permissible.

---
