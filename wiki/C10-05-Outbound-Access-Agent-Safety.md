# C10.5: Outbound Access & Agent Execution Safety

> **Parent:** [C10 MCP Security](C10-MCP-Security)
> **Requirements:** 3 | **IDs:** 10.5.1–10.5.3

## Purpose

This section ensures that MCP servers are constrained in what they can reach and how much they can do. MCP servers are code-execution endpoints — when a tool is invoked, the server runs arbitrary logic that may make outbound API calls, access databases, read files, or interact with cloud services. Without egress controls and execution limits, a compromised or manipulated MCP server becomes an unrestricted proxy into the internal network. Additionally, agentic workflows can create unbounded chains of tool invocations where a single prompt injection cascades into dozens of side-effecting operations. This section applies both network-level and execution-level constraints.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **10.5.1** | **Verify that** MCP servers may only initiate outbound requests to approved internal or external destinations following least-privilege egress policies and cannot access arbitrary network targets or internal cloud metadata services. | 2 | D/V | **SSRF and lateral movement via MCP servers.** An attacker (via prompt injection or tool argument manipulation) causes the MCP server to make requests to internal services, cloud metadata endpoints (e.g., `169.254.169.254` for AWS IMDSv1), or other network targets that should not be accessible. The MCP server acts as a confused deputy, using its network position to reach targets the attacker cannot reach directly. This is a server-side request forgery (SSRF) pattern specific to MCP. | Review network policies (firewall rules, security groups, network policies in Kubernetes) applied to MCP server workloads. Verify egress is restricted to an allowlist of approved destinations. Test by attempting to make requests from the MCP server to cloud metadata endpoints, internal services not on the allowlist, and arbitrary external URLs. Verify all are blocked. | Egress control is an infrastructure concern, not an MCP protocol concern — the MCP spec does not address it. Enforcement requires network-level controls (security groups, network policies, service mesh egress rules). Cloud metadata endpoint access is a particularly critical gap: if the MCP server runs on EC2/GCE/Azure and can reach the metadata endpoint, an attacker can obtain instance credentials. Ensure IMDSv2 (requiring hop-limited PUT request) is enforced at minimum. |
| **10.5.2** | **Verify that** outbound MCP actions implement execution limits (e.g., timeouts, recursion limits, concurrency caps, or circuit breakers) to prevent unbounded agent-driven tool invocation or chained side effects. | 2 | D/V | **Denial-of-service and runaway agent loops.** In agentic workflows, the model can invoke tools in a loop — each tool response may trigger further tool invocations. Without execution limits, a single prompt injection or model hallucination can cause: (1) resource exhaustion on the MCP server (CPU, memory, connections), (2) excessive calls to downstream APIs (hitting rate limits or incurring costs), (3) cascading side effects (e.g., repeatedly creating records, sending emails, or modifying data). | Review MCP server and orchestrator code for: per-request timeouts, maximum recursion depth for chained tool calls, concurrency limits (max concurrent tool invocations per session), and circuit breakers for downstream API failures. Test by creating a tool that triggers re-invocation and verify the system halts after the configured limit. Verify that timeout enforcement kills the operation cleanly (not just logging a warning). | Execution limits must be enforced at multiple layers: the MCP server (per-tool timeout), the orchestrator/agent framework (max tool calls per turn, max total calls per session), and the infrastructure (request timeout at the load balancer). No standard MCP mechanism exists for declaring or enforcing these limits — they are implementation-specific. Agent frameworks like LangChain and AutoGen have some built-in limits, but they vary in completeness. |
| **10.5.3** | **Verify that** MCP tool invocations classified as high-risk or destructive (e.g., data deletion, financial transactions, system configuration changes) require explicit user confirmation before execution. | 2 | D/V | **Destructive actions via prompt injection or model error.** The model (influenced by prompt injection or hallucination) invokes a destructive tool — deleting a database table, transferring funds, modifying system configuration, or sending emails on behalf of the user. Without a human-in-the-loop confirmation, these actions execute immediately and may be irreversible. | Review the MCP client/orchestrator for a tool classification system that tags tools as high-risk/destructive. Verify that invocation of tagged tools pauses execution and presents a confirmation prompt to the user with the tool name and arguments. Test by invoking a destructive tool and confirming the system blocks until user approval. Verify that the confirmation cannot be bypassed by the model (e.g., by crafting arguments that avoid the classification). | Tool classification is subjective and context-dependent — what is "destructive" varies by organization. The MCP spec defines `annotations` on tools (including `destructiveHint` and `readOnlyHint` in the 2025-03-26 spec), which can be used for classification. However, these annotations are self-reported by the MCP server and could be manipulated by a malicious server. The client should maintain its own classification in addition to honoring server-provided hints. |

---

## Related Standards & References

- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [AWS IMDSv2 documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) — mitigating metadata endpoint SSRF
- [MCP Tool Annotations (2025-03-26 spec)](https://spec.modelcontextprotocol.io/specification/2025-03-26/server/tools/) — `destructiveHint`, `readOnlyHint` annotations
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final) — least-privilege network access

---

## Open Research Questions

- [ ] How should tool risk classification be standardized — is the MCP `annotations` approach sufficient, or does it need a more formal taxonomy?
- [ ] Can execution limits be specified declaratively in the MCP protocol (e.g., server-advertised rate limits or timeout hints)?
- [ ] How should human-in-the-loop confirmation work in fully autonomous agent workflows where no user is present (e.g., batch processing, scheduled tasks)?
- [ ] Should MCP servers expose their egress allowlist as metadata, allowing clients to assess the server's network reach before connecting?

---
