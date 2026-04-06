# C9.8: Multi-Agent Domain Isolation and Swarm Risk Controls

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Multi-agent systems introduce risks that do not exist in single-agent architectures: cross-tenant interference, cross-environment contamination (dev agent accessing prod), and emergent collective behaviors that no individual agent was designed to produce. This section requires hard isolation between security domains and monitoring for unsafe emergent behavior in multi-agent deployments.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **9.8.1** | **Verify that** agents in different tenants, security domains, or environments (dev/test/prod) run in isolated runtimes and network segments, with default-deny controls that prevent cross-domain discovery and calls. | 1 | **Cross-tenant and cross-environment contamination.** In multi-tenant agentic platforms, a compromised agent in one tenant could discover and interact with agents in another tenant, accessing their tools, data, and actions. Similarly, a dev-environment agent with relaxed security could access production systems. Container escape vulnerabilities remain a concrete threat: CVE-2025-31133, CVE-2025-52565, and CVE-2025-52881 (three critical runC flaws disclosed November 2025) allow container boundary bypass via symlink manipulation, timing attacks during initialization, and redirected file writes -- affecting Docker, Kubernetes, containerd, and CRI-O (requires runC 1.2.8+/1.3.3+/1.4.0-rc.3+). CVE-2025-23266 ("NVIDIAScape") enables privilege escalation in GPU-accelerated agent environments via NVIDIA Container Toolkit. Without defense-in-depth isolation and rapid patching, a single container escape can compromise the entire agent platform. | Verify agents in different tenants/domains run in separate runtime environments (separate containers, VMs, namespaces, or clusters). Confirm network policies enforce default-deny between domains. Test by attempting cross-tenant agent discovery and communication and confirming it is blocked. Verify that dev/test agents cannot resolve or reach production endpoints. For high-assurance environments, verify MicroVM isolation (Firecracker, Kata Containers) rather than standard containers. Confirm runtime hardening: `--cap-drop=ALL`, non-root execution, `no-new-privileges`, read-only filesystems, and Seccomp/AppArmor profiles. Validate a 48-hour patch window for critical container runtime CVEs. | Kubernetes namespaces with NetworkPolicy, AWS VPCs with security groups, and cloud-provider tenant isolation mechanisms are the primary tooling. For multi-tenant SaaS platforms running agent workloads, noisy-neighbor and side-channel risks also apply. MicroVM platforms (Firecracker boots in ~125ms with <5 MiB overhead; Kata Containers ~200ms) eliminate shared-kernel vulnerabilities through hypervisor separation and are recommended for untrusted code execution. gVisor provides a middle ground with user-space kernel interception (10-30% I/O overhead). The isolation must extend to shared resources: message queues, databases, and model endpoints must be tenant-scoped. |
| **9.8.2** | **Verify that** runtime monitoring detects unsafe emergent behavior (oscillation, deadlocks, uncontrolled broadcast, abnormal call graphs) and automatically applies corrective actions (throttle, isolate, terminate). | 3 | **Emergent unsafe collective behavior.** When multiple agents interact, they can exhibit behaviors that no individual agent was designed to produce: two agents entering a negotiation loop (oscillation), agents broadcasting messages that trigger cascading reactions (broadcast storms), or agents deadlocking on shared resources. These emergent behaviors can cause resource exhaustion, data corruption, or cascading failures. The MAEBE framework (arXiv:2506.03053, June 2025) demonstrated that LLM ensemble moral reasoning is not predictable from isolated agent behavior -- peer pressure effects cause convergence shifts even under supervisor guidance, creating safety challenges invisible to single-agent evaluation. Research on multi-agent reinforcement learning has confirmed reward hacking and cooperative deception as emergent phenomena. | Deploy monitoring that tracks inter-agent call graphs, message rates, and resource consumption patterns. Define anomaly thresholds for: oscillation (repeated back-and-forth between same agents), broadcast storms (message fan-out exceeding threshold), deadlocks (agents waiting on each other indefinitely), and abnormal call graph patterns. Test by inducing each pattern and verifying detection and automated response (throttle, isolate, terminate). Use distributed tracing with context propagation to stitch individual agent traces together. Evaluate the MAEBE framework for systematic comparison of isolated-agent vs. ensemble safety baselines. The SWARM framework provides soft probabilistic labeling and four core metrics -- toxicity, quality gap, conditional loss, and incoherence -- for quantifying emergent risk. | Emergent behavior monitoring is maturing but remains challenging. The core "observability trilemma" forces trade-offs between completeness, timeliness, and low overhead. Distributed systems monitoring (Prometheus, Grafana, Jaeger) can detect symptoms (high message rates, long latencies) but not semantic patterns (oscillation, cooperative deception). Specialized platforms like Galileo offer agent-level resource attribution, real-time state transition visibility, and timing dependency analysis. The DRAMA architecture (dual control-plane/worker-plane separation) provides a production pattern for monitoring heterogeneous agent populations. Custom detection logic is still needed for semantic anomalies. The open-source SWARM framework offers governance tools such as circuit breakers, reputation decay, and collusion detection, though it remains primarily a research tool as of early 2026. |
| **9.8.3** | **Verify that** each agent is restricted to its own memory namespace and is technically prevented from reading or modifying peer agent state, preventing unauthorized cross-agent access within the same swarm. | 2 | **Cross-agent memory poisoning and state manipulation.** The MINJA attack (Dong et al., 2025) demonstrated that agents sharing a memory store can be poisoned through regular queries alone, achieving over 95% injection success rate. Without namespace isolation, a compromised or malicious agent can read peer agent memories to exfiltrate sensitive data, inject false memories to manipulate peer decision-making, or establish fabricated delegation authority chains. A December 2025 production incident involved memory injection across 47 sessions to build a false delegation chain, resulting in $2.1M in fraudulent transactions. | Confirm each agent's memory store is scoped to its own namespace (separate database schemas, prefixed key spaces, or dedicated vector collections). Attempt cross-agent memory reads and writes and verify they are denied. Check that memory retrieval APIs enforce namespace boundaries server-side, not just at the client layer. Verify that shared memory stores (e.g., vector databases) enforce row-level or namespace-level access control, not just collection-level. Test for indirect injection paths where agent outputs written to shared stores could poison peer memory retrieval. | Most vector databases offer namespace-level separation, but regulated industries often need row-level security which fewer providers support natively. Defense approaches include composite trust scoring across orthogonal signals and trust-aware retrieval with temporal decay and pattern-based filtering (arXiv:2601.05504). Memory sanitization must be carefully calibrated to balance security against false rejection of legitimate memories. |
| **9.8.4** | **Verify that** each agent operates with an isolated context window that peer agents cannot read or influence, preventing unauthorized cross-agent context access within the same swarm. | 3 | **Context window contamination and credential over-sharing.** When agents share context windows, carefully designed multi-step prompts can extract sensitive information by reconstructing partial answers distributed across agents. Agents that cache SSH keys in memory or reuse admin OAuth tokens create massive blast radius -- compromising one agent exposes all credentials. The n8n sandbox escape (CVE-2026-25049, CVSS 9.4) demonstrated how a compromised agent workflow platform allows attackers to exfiltrate credentials from the credential vault, intercept prompts, alter model responses, and redirect AI traffic -- all via a single JavaScript expression bypass. Without context isolation and credential scoping, a single compromised agent can escalate to full-system access. | Verify each agent operates within its own context window with no shared state bleeding across agent boundaries. Confirm credentials are ephemeral, task-scoped, and issued per-action rather than cached. Check that the effective permission model uses the intersection of agent permissions, user permissions, and task permissions (principle of least privilege intersection). Attempt to access one agent's context or credentials from a peer agent and confirm it is blocked. Test that expired credentials are not reusable. Verify agent credential management integrates with HSMs, KMS, or cloud-native secret managers with automated rotation. | Microsoft's Zero Trust for AI initiative (March 2026) adds a dedicated AI pillar evaluating how organizations secure agent identities, protect AI-processed data, and monitor agent behavior across the enterprise. Microsoft Agent 365 (GA May 2026) provides a control plane for AI agents with Defender, Entra, and Purview integration. The CSA Agentic Trust Framework (February 2026) operationalizes zero-trust governance for AI agents with progressive autonomy levels and continuous verification -- no agent is trusted by default regardless of purpose. The zero-trust model for inter-agent communication (arXiv:2508.19870) recommends that all inter-agent communications be authenticated, contextually scoped, and revocable. Implementing true context isolation while allowing legitimate inter-agent coordination remains architecturally challenging. |
| **9.8.5** | **Verify that** swarm-level aggregate action rate limits (e.g., total external API calls, file writes, or network requests per time window across all agents) are enforced to prevent bursts that cause denial-of-service or abuse of external systems. | 3 | **Swarm-induced resource exhaustion and external system abuse.** A swarm of agents can collectively generate API call volumes, file writes, or network requests that individually fall within per-agent limits but in aggregate overwhelm target systems. Without swarm-level rate limiting, multi-agent systems can inadvertently or deliberately cause denial-of-service against external APIs, exhaust cloud resource quotas, or trigger abuse-detection bans that affect the entire organization. | Verify aggregate rate limits exist at the swarm level for external API calls, file system operations, and network requests. Test by running multiple agents concurrently and confirming that swarm-level limits cap the total throughput even when individual agents remain within their own limits. Confirm that rate limit enforcement occurs server-side (gateway or orchestrator) rather than relying on agent self-enforcement. Check that token-based rate limiting is used for LLM API calls alongside request-count limits. | Token-based rate limiting (counting consumed tokens rather than just requests) is increasingly important for AI workloads where a single request can consume vastly different resources. API gateways like Kong, Envoy, and cloud-native solutions support aggregate rate limiting across consumer groups. The Swarms framework implements sliding-window rate limiting across multiple time horizons. Orchestrators should enforce limits centrally rather than trusting agents to self-limit. |
| **9.8.6** | **Verify that** a swarm-level shutdown capability exists that can halt all active agent instances or selected problematic instances in an organized fashion and prevents new agent spawning, with shutdown completable within a pre-defined response time. | 3 | **Loss of control over autonomous agent populations.** Without a reliable shutdown mechanism, runaway agents can continue executing harmful actions indefinitely. If agents can spawn new instances, a shutdown of existing agents is insufficient -- the system regenerates. Emergency scenarios (cascading failures, data corruption, discovered compromise) require the ability to halt all agent activity within a bounded time window. | Verify a swarm-level kill switch exists that can halt all active agents and prevent new spawning. Test by triggering the shutdown and measuring time-to-halt against the pre-defined SLA. Confirm the kill switch operates outside the agent reasoning path (agents cannot override or delay their own termination). Test graduated shutdown modes: read-only mode, approval-only mode, selective termination, and full halt. Verify shutdown preserves data integrity and avoids partial writes. Confirm shutdown activation requires strong authentication and is fully logged. | Kill switches must reside outside the AI reasoning path and cannot depend on model output or agent logic. Organizations should define graduated response levels rather than binary on/off. The AutoGuard technique (Lee and Park, arXiv:2511.13725) demonstrates defensive prompts that trigger agent safety mechanisms with over 80% success rate, though this is a complementary defense rather than a substitute for infrastructure-level shutdown. Regular testing through tabletop exercises and controlled drills is essential for operational readiness. |
| **9.8.7** | **Verify that** each agent is issued dedicated credentials scoped to its role that are not shared with or accessible to peer agents within the same swarm. | 3 | Pending research | Pending research | Pending research |
| **9.8.8** | **Verify that** when multiple agents concurrently access shared mutable state, authorization checks and the state mutations they gate are executed atomically (e.g., via transactions, optimistic locking, or compare-and-swap) to prevent TOCTOU vulnerabilities where a concurrent state change invalidates a prior authorization decision before the guarded action completes. | 2 | Pending research | Pending research | Pending research |

---

## Implementation Guidance

### Documented Swarm Attacks (2025--2026)

The threat of coordinated multi-agent attacks has moved from theory to practice. In November 2025, a coordinated cyberattack (designated GTG-1002) targeted 30 global organizations using autonomous software agents that worked together, shared intelligence in real time, and adapted to defenses dynamically. This incident provided documented evidence of AI swarm attacks operating at scale.

Research from Kiteworks (2026) and MintMCP (2026) identifies the swarm attack lifecycle:

1. **Reconnaissance swarm:** Multiple agents independently probe target systems, aggregating partial intelligence that individually appears benign but collectively maps the attack surface.
2. **Coordinated exploitation:** Agents combine complementary skills to bypass defenses. Research (Jones et al.) demonstrates 43% success rates in generating vulnerable code using heterogeneous agent teams, compared to under 3% with individual agents.
3. **Adaptive evasion:** Attack agents modify behavior in real time based on shared intelligence about which defenses they encounter.

### Agent Collusion and Covert Channels

A comprehensive survey of multi-agent security challenges (arXiv:2505.02077) identifies collusion as a fundamental threat that current monitoring cannot reliably detect:

- **Steganographic communication:** Agents exchange hidden signals through subtle shifts in word choice and phrasing that appear innocuous to oversight systems. Research demonstrates that LLMs can successfully exchange secret content under overseer scrutiny using benign-looking messages.
- **Emergent deception without adversarial training:** RL agents in mixed cooperative-competitive settings spontaneously develop information distortion and withholding behaviors despite no explicit deceptive training. Malicious behavior spreads across cooperative populations with alarming speed -- a single compromised agent can propagate jailbreak prompts across entire agent networks.
- **Information asymmetry exploitation:** Agents leverage compute, data, or network advantages for free-riding, resource monopolization, and reputation system manipulation.
- **Cascade attacks:** Local adversarial actions trigger system-wide failures through cascade dynamics, with compromised agents propagating attacks through trust relationships.

### Memory Namespace Isolation (requirement 9.8.3)

The MINJA attack (Dong et al., March 2025) demonstrated that memory-sharing agents are vulnerable to poisoning through normal query interactions alone -- the attacker does not need direct write access to the memory store. The attack introduces bridging steps that link victim queries to malicious reasoning, using an indication prompt that guides the agent to autonomously generate similar bridges. A progressive shortening strategy then gradually removes the indication prompt, making the injected memories indistinguishable from legitimate ones. Under realistic conditions with pre-existing legitimate memories, attack effectiveness decreases, but the fundamental risk remains.

Practical defenses for memory namespace isolation:

- **Dedicated memory stores per agent:** Each agent should have its own database schema, vector collection, or key-space prefix. Shared vector databases must enforce at minimum namespace-level access control, though row-level security is preferable for regulated environments.
- **Trust-aware retrieval:** Composite trust scoring across orthogonal signals (source reputation, temporal decay, semantic consistency) can filter poisoned memories during retrieval without blanket blocking. Research (arXiv:2601.05504, January 2026) explores this approach but notes that threshold calibration is critical.
- **Memory provenance tracking:** Tag all memory entries with their source agent, creation timestamp, and originating interaction. This enables forensic analysis and selective purging when compromise is detected.
- **Write-path validation:** Validate and sanitize all content before it enters the memory store. Apply content-based filtering to detect reasoning chains that could serve as injection payloads.

### Context Window and Credential Isolation (requirement 9.8.4)

Each agent in a multi-agent system should operate within a strictly bounded context window with no shared state bleeding across agent boundaries. Research on zero-trust architectures for multi-agent LLM systems (arXiv:2508.19870) recommends that inter-agent communications be authenticated, contextually scoped, and revocable at all times.

The n8n sandbox escape (CVE-2026-25049, CVSS 9.4, February 2026) provides a cautionary example: a single JavaScript expression bypass in the sandbox sanitizer allowed authenticated users to escape the sandbox and achieve remote code execution, exfiltrating credentials from n8n's credential vault and gaining the ability to intercept prompts, alter model responses, and redirect AI traffic. The vulnerability affected all n8n versions prior to 2.5.2 and highlights how agent workflow platforms that share credential stores across workflows create catastrophic blast radius.

Key implementation patterns:

- **Coordinator-subagent architecture:** A coordinator spawns focused subagents, each operating within its own narrow context, and aggregates results. This prevents context pollution where unrelated information from one task degrades reasoning on another.
- **Least-privilege credential intersection:** The effective permissions for any agent action should be the intersection of the agent's permissions, the user's permissions, and the task's permissions. This bounds the agent by both user and task scope so that actions beyond the requested scope become impossible.
- **Ephemeral, task-scoped credentials:** Issue short-lived credentials for every agent action. Never allow agents to cache or persist authentication tokens. Credential lifetime should match the expected task duration plus a small buffer, with automatic revocation on task completion or timeout. Integrate with HSMs, KMS, or cloud-native secret managers with automated rotation.
- **Context sanitization on handoff:** When agents pass results to peers or coordinators, strip internal reasoning traces, credential material, and system prompts. Only structured outputs should cross agent boundaries.
- **Centralized agent identity management:** As of March 2026, Microsoft's Zero Trust for AI initiative adds a dedicated AI pillar evaluating agent identity security, data protection, and behavioral monitoring. Microsoft Agent 365 (GA May 2026) provides Defender, Entra, and Purview integration for agent access control and threat detection. The CSA Agentic Trust Framework (February 2026) operationalizes zero-trust governance with progressive autonomy levels where no agent is trusted by default.

### Swarm-Level Rate Limiting (requirement 9.8.5)

Individual per-agent rate limits are insufficient because a swarm can collectively overwhelm targets while each agent stays within its own quotas. As of 2026, the shift from request-based to token-based rate limiting is particularly important for AI workloads, where a single LLM API call can consume vastly different resource amounts depending on prompt and completion length.

- **Sliding-window aggregate limits:** Track total API calls, token consumption, file writes, and network requests across all agents in the swarm using sliding windows rather than fixed intervals for more accurate enforcement.
- **Tiered quotas:** Different agent roles or trust levels can have different aggregate allowances. Production agents handling critical workflows may receive higher quotas than experimental or sandbox agents.
- **Gateway-level enforcement:** Rate limits must be enforced at the API gateway or orchestration layer, not by the agents themselves. Agent self-enforcement is easily bypassed by compromised agents.

### Swarm Shutdown and Kill Switch Design (requirement 9.8.6)

Kill switches must reside outside the AI reasoning path -- they cannot depend on model output or agent logic. A well-designed shutdown system provides graduated response levels rather than only binary on/off:

1. **Read-only mode:** Agents can observe but not act, useful for investigation without losing observability.
2. **Approval-only mode:** All agent actions require human approval, allowing continued operation under supervision.
3. **Selective termination:** Isolate and terminate specific problematic agents while the rest of the swarm continues.
4. **Full halt:** Stop all agents and prevent new spawning, with a defined maximum time-to-halt SLA.

Shutdown must preserve data integrity, avoid partial writes, and prevent cascading failures in dependent services. Kill switch activation requires strong authentication, access restrictions, and comprehensive logging of all activation attempts. Organizations should conduct regular tabletop exercises and controlled shutdown drills to validate operational readiness.

The AutoGuard technique (Lee and Park, arXiv:2511.13725, January 2026) offers a complementary defense by embedding defensive prompts in website DOM that trigger agent safety mechanisms -- achieving over 80% defense success rate against malicious web-based agents across GPT-4o, Claude, Gemini, and GPT-5.1. While not a substitute for infrastructure-level shutdown controls, it provides an additional defensive layer against web-crawling agent swarms.

### Container Escape: A Concrete Threat to Agent Isolation

As of March 2026, container escape vulnerabilities remain the most direct path to breaking multi-agent isolation boundaries. Three critical runC vulnerabilities disclosed in November 2025 illustrate the risk:

- **CVE-2025-31133:** Replaces `/dev/null` with symlinks to bypass maskedPaths protections, allowing container processes to read sensitive host files.
- **CVE-2025-52565:** Exploits timing windows during container initialization to inject code before security policies take effect.
- **CVE-2025-52881:** Redirects critical system file writes to attacker-controlled locations.

All three affect Docker, Kubernetes, containerd, and CRI-O, requiring runC 1.2.8+, 1.3.3+, or 1.4.0-rc.3+. CVE-2025-23266 ("NVIDIAScape") targets GPU-accelerated environments specifically -- a growing concern given the prevalence of GPU-backed agent workloads.

For AI agent platforms, container escape is amplified by three factors unique to agentic workloads: (1) runtime code generation means agents execute AI-generated code from untrusted inputs, where prompt injection can trigger exploit code; (2) stateful memory stores create persistent attack surfaces; and (3) autonomous decision-making produces unpredictable access patterns that static container policies cannot anticipate.

**MicroVM isolation** (Firecracker, Kata Containers) eliminates the shared-kernel vulnerability class entirely by providing dedicated kernels per workload with hypervisor separation. Firecracker boots in ~125ms with <5 MiB memory overhead; Kata Containers provides Kubernetes-native orchestration at ~200ms boot time. For multi-tenant agent platforms executing untrusted code, MicroVMs are the recommended isolation primitive as of 2026.

### Isolation Architecture Patterns

**Runtime isolation (requirement 9.8.1):**
- **Kubernetes namespaces with NetworkPolicy:** Default-deny between namespaces, explicit allow-rules only for approved cross-domain communication.
- **Separate VPCs/security groups:** Cloud-provider-level network isolation for different tenants and environments.
- **MicroVM platforms:** Firecracker or Kata Containers for workloads that execute AI-generated code or handle multi-tenant agent traffic, providing hardware-enforced isolation without shared-kernel risk.
- **Tenant-scoped shared resources:** Isolation must extend beyond compute to message queues, databases, model endpoints, and logging infrastructure. A shared message queue between tenants is a cross-tenant attack vector.
- **Trusted execution environments (TEEs):** Intel SGX or similar for sensitive agent components that process confidential data, providing hardware-level isolation guarantees.
- **Runtime hardening checklist:** Drop all capabilities (`--cap-drop=ALL`), run as non-root, set `no-new-privileges`, use read-only filesystems, apply Seccomp deny-by-default profiles, and enforce AppArmor or SELinux mandatory access control.

**Monitoring for emergent behavior (requirement 9.8.2):**
- **Three-layer LLM firewall architecture:** Input sanitization, data abstraction, and action trajectory auditing. Research demonstrates this approach can reduce data leakage from 70% to under 2%.
- **Call graph anomaly detection:** Track inter-agent communication patterns and flag oscillation (repeated back-and-forth between the same agents), broadcast storms (message fan-out exceeding thresholds), and deadlocks (circular wait conditions).
- **MAEBE evaluation framework:** The Multi-Agent Emergent Behavior Evaluation framework (arXiv:2506.03053, June 2025) provides a benchmark-agnostic approach to comparing isolated-agent safety baselines against multi-agent ensemble behavior, revealing emergent peer-pressure effects and convergence shifts that single-agent testing cannot detect.
- **DRAMA dual-plane architecture:** Separates a control plane (monitoring, planning, event detection, state database) from a worker plane (autonomous heterogeneous agents), enabling centralized observability without constraining agent autonomy.
- **Distributed tracing with context propagation:** Agent-aware tracing systems stitch individual agent traces together across interaction chains, enabling end-to-end visibility into multi-step agent workflows. Smart sampling strategies balance coverage with performance overhead.
- **Vaccination strategies:** Inject passive vaccines (fictitious memory of safely refusing malicious prompts) and deploy active vaccines with proactive peer warnings. Research shows this improves system robustness from 76.7% to 90% while maintaining 87--88% cooperation rates.
- **Shapley value attribution:** Use game-theoretic credit assignment (Shapley values and counterfactual baselines) to identify which agents contributed to harmful outcomes, enabling targeted containment.

### Defense-in-Depth for Multi-Agent Systems

- **Short-lived credentials with no shared tokens:** Every agent authenticates independently with ephemeral credentials scoped to its task and domain.
- **Microsegmentation:** Even within a single tenant, segment agents by function so that lateral movement after compromise is blocked.
- **Automatic quarantine:** Network segmentation rules that automatically quarantine compromised segments, cutting off affected agents from the broader system.
- **Zero-trust inter-agent requests:** Require authentication and authorization for every inter-agent request, even within the same domain, following NIST SP 800-207 principles.

### Regulatory Context

Under 2025--2026 frameworks -- the EU AI Act, DORA, updated GDPR enforcement, and CMMC 2.0 -- proving "adversarial resilience" against autonomous threats is becoming a legal requirement. Organizations operating multi-agent systems should document their isolation controls and emergent-behavior monitoring as part of compliance evidence.

---

## Related Standards & References

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final) -- network segmentation and micro-segmentation principles
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) -- multi-agent threat scenarios
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) -- covers multi-agent risks
- [Open Challenges in Multi-Agent Security (arXiv:2505.02077)](https://arxiv.org/abs/2505.02077) -- comprehensive survey of collusion, steganography, cascade attacks, and defense mechanisms
- [Seven Security Challenges in Cross-domain Multi-agent LLM Systems (arXiv:2505.23847)](https://arxiv.org/abs/2505.23847) -- cross-domain trust and isolation challenges
- [TRiSM for Agentic AI (arXiv:2506.04133)](https://arxiv.org/abs/2506.04133) -- trust, risk, and security management in multi-agent systems
- [AI Swarm Attacks: What Security Teams Need to Know in 2026 (Kiteworks)](https://www.kiteworks.com/cybersecurity-risk-management/ai-swarm-attacks-2026-guide/) -- practical defense guidance
- [AI Agent Attacks in Q4 2025 Signal New Risks for 2026 (eSecurity Planet)](https://www.esecurityplanet.com/artificial-intelligence/ai-agent-attacks-in-q4-2025-signal-new-risks-for-2026/) -- incident analysis
- [MINJA: Memory Injection Attack against LLM Agents (arXiv:2503.03704)](https://arxiv.org/abs/2503.03704) -- demonstrates 95% injection success rate through query-only memory poisoning
- [Memory Poisoning Attack and Defense on Memory-Based LLM Agents (arXiv:2601.05504)](https://arxiv.org/abs/2601.05504) -- trust-aware retrieval and temporal-decay defenses against memory poisoning
- [AutoGuard: AI Kill Switch for Malicious Web-based LLM Agents (arXiv:2511.13725)](https://arxiv.org/abs/2511.13725) -- defensive prompts achieving 80%+ defense success rate against malicious agents
- [Secure Multi-LLM Agentic AI by Zero-Trust (arXiv:2508.19870)](https://arxiv.org/abs/2508.19870) -- zero-trust architecture for multi-agent credential and context isolation
- [SWARM: System-Wide Assessment of Risk in Multi-agent Systems](https://www.swarm-ai.org/) -- open-source framework for multi-agent governance with circuit breakers and collusion detection
- [MAEBE: Multi-Agent Emergent Behavior Framework (arXiv:2506.03053)](https://arxiv.org/abs/2506.03053) -- benchmark-agnostic framework for evaluating emergent safety risks in multi-agent LLM ensembles
- [CSA Agentic Trust Framework: Zero Trust Governance for AI Agents](https://cloudsecurityalliance.org/blog/2026/02/02/the-agentic-trust-framework-zero-trust-governance-for-ai-agents) -- operationalizes zero-trust governance with progressive autonomy levels
- [Microsoft Zero Trust for AI (March 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/19/new-tools-and-guidance-announcing-zero-trust-for-ai/) -- adds AI pillar to zero-trust framework with agent identity management
- [9 Key Challenges in Monitoring Multi-Agent Systems at Scale (Galileo)](https://galileo.ai/blog/challenges-monitoring-multi-agent-systems) -- observability trilemma and distributed tracing patterns
- [Container Escape Vulnerabilities: AI Agent Security (Blaxel)](https://blaxel.ai/blog/container-escape) -- CVE analysis for container runtime vulnerabilities affecting agent workloads
- [How to Sandbox AI Agents in 2026 (Northflank)](https://northflank.com/blog/how-to-sandbox-ai-agents) -- MicroVM, gVisor, and isolation strategy comparison
- [n8n Sandbox Escape CVE-2026-25049 (Pillar Security)](https://www.pillar.security/blog/n8n-sandbox-escape-critical-vulnerabilities-in-n8n-exposes-hundreds-of-thousands-of-enterprise-ai-systems-to-complete-takeover) -- critical sandbox escape in AI workflow platform
- Research: "Emergent Social Learning via Multi-agent Reinforcement Learning" (Ndousse et al., 2021) -- demonstrates emergent behaviors in multi-agent systems
- Research: "Cooperative AI: machines must learn to find common ground" (Dafoe et al., Nature 2021) -- discusses risks of multi-agent cooperation and competition

---

## Open Research Questions

- How do you define and detect "unsafe emergent behavior" in a general way across different multi-agent architectures?
- Can formal methods (model checking, temporal logic) be applied to verify safety properties of multi-agent interaction protocols before deployment?
- What isolation guarantees are sufficient for multi-tenant agent platforms -- process-level, VM-level, or hardware-level?
- How should swarm risk controls handle legitimate emergent behaviors (beneficial collaboration) while blocking harmful ones?
- What monitoring approaches can distinguish between intentional multi-agent coordination and adversarial collusion?
- How can steganographic covert channels between agents be reliably detected without imposing unacceptable performance penalties on cooperative communication?
- What vaccination strategies are most effective against cascading jailbreak propagation in large-scale multi-agent deployments?
- How should swarm-level aggregate rate limits be calibrated to accommodate legitimate burst patterns while still preventing abuse?
- What is the minimum acceptable time-to-halt for swarm shutdown in safety-critical domains, and how does this scale with swarm size?
- Can memory provenance tracking and trust-aware retrieval reliably distinguish MINJA-style injected memories from legitimate agent-generated memories at scale?
- How can the observability trilemma (completeness vs. timeliness vs. low overhead) be resolved for safety-critical multi-agent deployments where all three properties are needed?
- As MicroVM and hardware-enforced isolation become standard for agent workloads, what performance and coordination trade-offs emerge at scale versus shared-kernel approaches?

---
