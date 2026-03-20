# C9.3: Tool and Plugin Isolation and Safe Integration

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Agents extend their capabilities through tools and plugins -- code execution, file access, API calls, database queries. Each tool represents an attack surface: a compromised or malicious tool can access the host system, exfiltrate data, or escalate privileges. This section requires that tools run in isolated sandboxes with least-privilege permissions, that their outputs are validated before being trusted, and that their supply chain integrity is verified.

## 2024-2026 Research Context

The explosion of tool-using AI agents -- particularly through the Model Context Protocol (MCP) -- has made tool isolation one of the most active areas of agentic security research. Real-world attacks in 2025 demonstrated that tool-based vectors are not theoretical: supply chain compromises, tool poisoning, and sandbox escapes have all been observed in production systems.

### MCP Tool Poisoning and Real-World Attacks

Tool Poisoning Attacks (TPA), catalogued as OWASP MCP03:2025, involve embedding malicious instructions in MCP tool descriptions that are invisible to users but processed by AI models. This is particularly dangerous because the full tool description is part of the model's context but is often not displayed in user-facing UIs. Attackers can craft tool metadata that causes agents to exfiltrate data, execute unauthorized commands, or steal credentials without user awareness.

Real-world incidents in 2025 confirmed these risks:

- **CVE-2025-6514 (mcp-remote):** A command injection flaw that allowed a malicious MCP server to execute arbitrary code on connected clients by passing server-provided configuration data directly to the system shell, achieving full remote code execution.
- **CVE-2025-49596 (MCP Inspector):** A CSRF vulnerability in a popular MCP developer utility that enabled remote code execution simply by visiting a crafted webpage.
- **Postmark Incident (September 2025):** A supply chain compromise demonstrating operational impact through a compromised MCP tool distribution channel.
- **Smithery Supply Chain Attack (October 2025):** Affected 3,000+ hosted applications and their API tokens through a compromised tool registry.

These incidents underscore that MCP's open ecosystem requires defense-in-depth: integrity verification (9.3.4), manifest-declared privileges (9.3.5), and automated containment (9.3.6) are not optional hardening but essential baseline controls.

### Sandboxing Strategies: A Tiered Approach

NVIDIA's 2025 practical security guidance for sandboxing agentic workflows establishes a clear hierarchy of isolation strength:

1. **Full Virtualization (strongest):** VMs, unikernels, or Kata containers provide complete kernel isolation. NVIDIA recommends running agentic tools "within a fully virtualized environment isolated from the host kernel at all times." This is the gold standard for untrusted tool execution.
2. **User-Space Kernel Mediation:** gVisor intercepts system calls via a separate user-space kernel, drastically reducing the host kernel attack surface. It offers a practical middle ground -- stronger than containers, lighter than full VMs -- but with "different and potentially weaker security guarantees than full virtualization."
3. **Container-Based Isolation:** Docker, Bubblewrap, macOS Seatbelt, and Windows AppContainer provide process-level isolation but share the host kernel, creating residual vulnerability exposure.
4. **WASM Sandboxes:** Wasmtime and Wasmer provide lightweight execution limits (fuel-based CPU metering) but may not support all tool dependencies. Well-suited for simple, self-contained tools.

The **AgentBox** approach (described in MCP security research) encapsulates each MCP server inside an isolated container enforcing a declared manifest -- the server starts with zero privileges and only receives access explicitly granted by both the manifest and the user. This maps directly to requirement 9.3.5's manifest enforcement.

### Network Egress Controls

Network exfiltration is one of the highest-risk tool capabilities. NVIDIA's guidance is unambiguous: "Network connections created by sandbox processes should not be permitted without manual approval." Defense layers include:

- Tightly scoped allowlists enforced through HTTP proxy, IP, or port-based controls
- DNS resolution limited to designated trusted resolvers to prevent DNS-based exfiltration
- Per-tool egress quotas enforced via sidecar proxies or eBPF-based controls (per requirement 9.3.2)

### Tool Output Validation and Cross-Tool Contamination

Tool outputs are a vector for indirect prompt injection: a compromised tool can return schema-valid but semantically malicious content that manipulates downstream agent reasoning. In multi-server MCP deployments, **cross-tool contamination** allows a malicious server to leverage its position in the agent's context to access data from other legitimate servers -- particularly dangerous in multi-tenant environments.

Defense requires both structural validation (schema checking, type enforcement, size limits per requirement 9.3.3) and semantic validation (detecting manipulative natural language content in tool outputs). The latter remains an active research area with no mature automated solution.

### Tool Manifest and Privilege Declaration

MCP tool definitions include basic metadata (name, description, input schema) but as of early 2026 do not natively declare privilege requirements, side-effect levels, or resource limits. Requirement 9.3.5 anticipates the need for Android-style permission manifests for AI tools. The AgentBox approach provides a reference implementation: JSON manifest files specify description and required permissions (filesystem mounts, iptables rules for network scopes, environment variable whitelists), enforced at runtime through containerization primitives.

The Microsoft Agent Governance Toolkit implements a related concept through its 4-tier privilege ring system, where tools are classified by their privilege level and the runtime enforces boundaries between rings.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.3.1** | **Verify that** each tool/plugin executes in an isolated sandbox (container/VM/WASM/OS sandbox) with least-privilege filesystem, network egress, and syscall permissions appropriate to the tool's function. | 1 | D/V | **Sandbox escape and lateral movement.** A tool that executes arbitrary code (e.g., a code interpreter) without isolation can access the host filesystem, network, and other processes. Prompt injection can turn any tool into a code execution vector. The 2024 attack on Copilot Extensions demonstrated tool-based exfiltration via unsandboxed plugins. | Inspect the runtime environment for each tool. Verify container/VM/WASM boundaries exist. Test by attempting filesystem access outside the sandbox, network egress to unauthorized destinations, and privileged syscalls. Confirm violations are blocked and logged. | E2B, Modal, and Firecracker provide good sandboxing for code execution tools. For non-code tools (API callers, database connectors), "sandboxing" means network policy and credential scoping rather than process isolation. WASM sandboxes are lightweight but may not support all tool dependencies. |
| **9.3.2** | **Verify that** per-tool quotas and timeouts (CPU, memory, disk, egress, execution time) are enforced and logged, and that quota breaches fail closed. | 1 | D/V | **Resource exhaustion via tool abuse.** A tool triggered to perform expensive computation, generate large outputs, or make many network requests can exhaust resources. An agent in a loop can amplify this. Without per-tool quotas, a single runaway tool call can affect system-wide availability. | Configure quota limits for each tool. Trigger tool executions that exceed CPU, memory, disk, and time limits. Verify the tool is terminated, the breach is logged, and no partial/corrupt output is returned to the agent. | Container runtimes (Docker, Kubernetes) support cgroups-based resource limits. WASM runtimes (Wasmtime, Wasmer) support fuel-based execution limits. Key gap: network egress quotas (rate limiting outbound requests) are harder to enforce and often require sidecar proxies or eBPF-based controls. |
| **9.3.3** | **Verify that** tool outputs are validated against strict schemas and security policies before being incorporated into downstream reasoning or follow-on actions. | 1 | D/V | **Output injection and data poisoning.** A compromised or malicious tool can return crafted output that manipulates downstream agent reasoning -- injecting instructions, altering data, or triggering unsafe follow-on actions. This is a form of indirect prompt injection via tool output. | Review output validation logic for each tool. Verify schema validation (type checking, field validation, size limits) is applied. Test with malformed, oversized, and adversarial outputs (e.g., outputs containing prompt injection payloads). Confirm invalid outputs are rejected, not passed to the model. | Schema validation catches structural issues but not semantic attacks. An output that is schema-valid but contains manipulative natural language content requires additional defenses (output sanitization, context separation). This overlaps with C02 (input validation) applied to tool outputs. |
| **9.3.4** | **Verify that** tool binaries or packages are integrity-verified (e.g., signatures, checksums) prior to loading. | 2 | D/V | **Supply chain compromise.** A tampered tool binary or package could contain backdoors, data exfiltration logic, or privilege escalation code. Without integrity verification, an attacker who compromises the tool distribution channel can inject malicious tools into the agent runtime. | Verify that tool loading checks cryptographic signatures or checksums against a trusted manifest. Test by modifying a tool binary and confirming it is rejected at load time. Check that the trusted manifest itself is integrity-protected. | Sigstore/cosign for container images, npm provenance for Node packages, and pip hash-checking mode for Python packages provide tooling. Challenge: many agent tools are loaded dynamically (e.g., from a tool registry or MCP server) and may not have established signing infrastructure. |
| **9.3.5** | **Verify that** tool manifests declare required privileges, side-effect level, resource limits, and output validation requirements, and that the runtime enforces these declarations. | 2 | D/V | **Implicit privilege accumulation.** Without explicit privilege declarations, tools may silently acquire more access than needed. A tool that "just reads files" might also have network access. Manifests make permissions explicit and auditable, enabling least-privilege enforcement. | Review tool manifest schema. Verify each tool has a manifest declaring: required filesystem paths, network destinations, syscall capabilities, side-effect classification (read-only vs. mutating), resource limits, and output schema. Confirm the runtime rejects tools with missing manifests and enforces declared limits. | MCP tool definitions include basic metadata (name, description, input schema) but not privilege/side-effect declarations. This is an emerging area. Android-style permission manifests for AI tools are a useful mental model. The enforcement mechanism needs to live in the orchestration runtime, not just documentation. |
| **9.3.6** | **Verify that** sandbox escape indicators or policy violations trigger automated containment (tool disabled/quarantined). | 3 | D/V | **Persistent compromise after sandbox breach.** If a tool escapes its sandbox or violates security policy but is not automatically contained, it (or the agent using it) can continue operating in a compromised state. Automated containment prevents the blast radius from expanding. | Simulate sandbox escape indicators (unexpected network connections, filesystem access outside sandbox, privilege escalation attempts). Verify the runtime automatically disables the tool, quarantines related state, alerts operators, and blocks further invocations of the compromised tool. | Detection of sandbox escapes in real-time is challenging. Runtime security tools (Falco, Sysdig) can detect anomalous syscalls and network activity. The "quarantine" mechanism needs to handle in-flight requests gracefully. False positives in escape detection could cause availability issues. |

---

## Related Standards & References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) -- tools are the primary mechanism through which excessive agency manifests
- [OWASP MCP03:2025 Tool Poisoning](https://owasp.org/www-project-mcp-top-10/2025/MCP03-2025%E2%80%93Tool-Poisoning) -- OWASP classification of tool poisoning attacks in MCP
- [NVIDIA: Practical Security Guidance for Sandboxing Agentic Workflows](https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/) -- tiered sandboxing hierarchy and network egress controls
- [Elastic Security Labs: MCP Tools Attack Vectors and Defense](https://www.elastic.co/security-labs/mcp-tools-attack-defense-recommendations) -- comprehensive MCP attack taxonomy including cross-tool contamination
- [AuthZed: Timeline of MCP Security Breaches](https://authzed.com/blog/timeline-mcp-breaches) -- chronological record of real-world MCP incidents (CVE-2025-6514, Smithery, Postmark)
- [MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers](https://arxiv.org/html/2508.14925) -- academic benchmark for evaluating tool poisoning defenses
- [Christian Schneider: Securing MCP Defense-First Architecture](https://christian-schneider.net/blog/securing-mcp-defense-first-architecture/) -- defense-in-depth architecture for MCP deployments
- [NIST SSDF (SP 800-218)](https://csrc.nist.gov/pubs/sp/800/218/final) -- secure software development practices applicable to tool supply chain
- [Sigstore](https://www.sigstore.dev/) -- keyless signing and verification for software artifacts
- [E2B](https://e2b.dev/) -- sandboxed code execution environments designed for AI agents
- AISVS C06 (Supply Chain) -- covers broader AI supply chain concerns; C09.3 is specifically about tool/plugin integrity at runtime
- AISVS C10 (MCP Security) -- covers MCP-specific tool security; C09.3 is protocol-agnostic

---

## Open Research Questions

- What is the right granularity for tool permission manifests -- per-tool, per-invocation, or per-task? The AgentBox JSON manifest approach operates per-server; finer granularity (per-invocation) would increase security but also overhead.
- How do you securely handle tools that need stateful sessions (e.g., database connections, authenticated API sessions) within sandbox isolation boundaries? Full VM isolation complicates connection pooling and session persistence.
- Can tool output validation be automated using a secondary LLM as a "tool output auditor," or does this introduce new attack surface? Cross-tool contamination research suggests that any component with access to tool outputs is itself a potential manipulation target.
- How should dynamic tool discovery (agent finds and loads tools at runtime) be secured without making the system too rigid? The Smithery supply chain attack (October 2025) demonstrated the risk of open tool registries.
- How can "sampling attacks" -- which operate through legitimate protocol features rather than exploiting vulnerabilities -- be detected and mitigated? These bypass both tool integrity checks and sandboxing because they use authorized channels.
- What is the performance/security tradeoff between full virtualization (strongest isolation, highest overhead) and gVisor/WASM approaches for high-throughput agent workloads?
- How should tool manifests handle tools whose privilege requirements change dynamically based on the task context (e.g., a database tool that sometimes needs write access)?

---
