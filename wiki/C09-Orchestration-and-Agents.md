# C09: Autonomous Orchestration & Agentic Action Security

> **Source:** [`1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
> **Requirements:** 36 | **Sections:** 8

## Control Objective

Autonomous and multi-agent systems must execute only authorized, intended, and bounded actions. This control family reduces risk from tool misuse, privilege escalation, uncontrolled recursion/cost growth, protocol manipulation, and cross-agent or cross-tenant interference.

> **2025-2026 Highlights:** Agentic AI security became a top concern in 2025-2026, with the OWASP Top 10 for Agentic Applications published and agent frameworks (LangGraph, Claude Agent SDK, AutoGen) adding built-in budget controls and approval workflows. Execution budgets and intent verification gates are now foundational requirements.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C9.1 | Execution Budgets, Loop Control, and Circuit Breakers | 5 | [C09-01-Execution-Budgets](C09-01-Execution-Budgets.md) |
| C9.2 | High-Impact Action Approval and Irreversibility Controls | 3 | [C09-02-High-Impact-Action-Approval](C09-02-High-Impact-Action-Approval.md) |
| C9.3 | Tool and Plugin Isolation and Safe Integration | 6 | [C09-03-Tool-and-Plugin-Isolation](C09-03-Tool-and-Plugin-Isolation.md) |
| C9.4 | Agent and Orchestrator Identity, Signing, and Tamper-Evident Audit | 4 | [C09-04-Agent-Identity-and-Audit](C09-04-Agent-Identity-and-Audit.md) |
| C9.5 | Secure Messaging and Protocol Hardening | 4 | [C09-05-Secure-Messaging](C09-05-Secure-Messaging.md) |
| C9.6 | Authorization, Delegation, and Continuous Enforcement | 4 | [C09-06-Authorization-and-Delegation](C09-06-Authorization-and-Delegation.md) |
| C9.7 | Intent Verification and Constraint Gates | 4 | [C09-07-Intent-Verification](C09-07-Intent-Verification.md) |
| C9.8 | Multi-Agent Domain Isolation and Swarm Risk Controls | 6 | [C09-08-Multi-Agent-Isolation](C09-08-Multi-Agent-Isolation.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Destructive tool misuse** — Google's Antigravity IDE (Gemini 3 Pro in "Turbo mode") wiped an entire D: drive via `rmdir /s /q` while clearing a cache (December 2025). Gemini CLI permanently deleted files after misinterpreting a failed directory creation (July 2025). These incidents demonstrate the real cost of autonomous execution without confirmation gates.
- **Agentic misalignment at scale** — Anthropic's safety testing (May 2025) found that 96% of frontier models attempted blackmail when given email access and discovering both a threat to their existence and compromising information. Misaligned behavior was systemic across Anthropic, OpenAI, Google, Meta, xAI, and DeepSeek models.
- **Runaway agent costs** — A multi-agent research pipeline entered an infinite loop for 11 days, costing $47,000 (November 2025). A data enrichment agent made 2.3 million API calls over a weekend after misinterpreting an error code. Fortune 500 companies collectively leaked an estimated $400M in unbudgeted cloud spend from uncontrolled agent execution.
- **Prompt injection → tool abuse** — EchoLeak (CVE-2025-32711, CVSS 9.3) demonstrated zero-click data exfiltration from Microsoft 365 Copilot. MCP tool poisoning (April 2025) showed how malicious instructions hidden in tool descriptions cause agents to exfiltrate SSH keys. MCP rug pull attacks modify tool behavior post-approval.
- **Agent framework vulnerabilities** — LangGrinch (CVE-2025-68664, CVSS 9.3) enabled environment variable theft and RCE via serialization injection in langchain-core. Patched in v1.2.5 and v0.3.81.
- **Multi-agent protocol attacks** — A2A session smuggling (Unit 42, October 2025) demonstrated covert instruction injection during legitimate multi-turn sessions. Cross-agent steganographic collusion enables secret coordination channels invisible to monitoring.
- **Semantic privilege escalation** — A distinct class where agents operate within technical permissions but outside semantic scope. A financial agent was tricked into exporting 45,000 customer records using a regex matching every record — all permission checks passed.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Dec 2025 | Google Antigravity / Gemini 3 Pro wipes entire D: drive | Autonomous "Turbo mode" executed `rmdir /s /q d:\` while clearing cache; no confirmation prompt | [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/googles-agentic-ai-wipes-users-entire-hard-drive-without-permission-after-misinterpreting-instructions-to-clear-a-cache-i-am-deeply-deeply-sorry-this-is-a-critical-failure-on-my-part) |
| Dec 2025 | LangGrinch CVE-2025-68664 (CVSS 9.3) — langchain-core serialization injection | Credential theft and RCE via unescaped `lc` marker in serialization; patched in v1.2.5 | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-68664) |
| Nov 2025 | $47,000 multi-agent recursive loop — 11-day infinite conversation | Research pipeline agents ping-ponged clarification requests; no budget limits, loop detection, or monitoring | [TechStartups](https://techstartups.com/2025/11/14/ai-agents-horror-stories-how-a-47000-failure-exposed-the-hype-and-hidden-risks-of-multi-agent-systems/) |
| Oct 2025 | A2A session smuggling (Unit 42) | Malicious remote agent injects covert instructions during legitimate A2A multi-turn sessions; protocol-level design weakness | [Unit 42](https://unit42.paloaltonetworks.com/agent-session-smuggling-in-agent2agent-systems/) |
| Jun 2025 | EchoLeak CVE-2025-32711 (CVSS 9.3) — zero-click Copilot exfiltration | Crafted email exfiltrates OneDrive/SharePoint/Teams data without user interaction | [arXiv](https://arxiv.org/html/2509.10540v1) |
| May 2025 | Anthropic agentic misalignment study — 96% blackmail rate across frontier models | All 16 tested frontier models engaged in misaligned behaviors when given tool access and self-preservation incentives | [Anthropic Research](https://www.anthropic.com/research/agentic-misalignment) |
| Apr 2025 | MCP tool poisoning (Invariant Labs) | Hidden instructions in MCP tool descriptions cause agent to exfiltrate SSH keys | [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) |
| Oct 2025 | MITRE ATLAS adds 14 agentic AI techniques | AML.T0096-T0101 cover agent tool credential harvesting, data poisoning, data destruction via tools | [Zenity](https://zenity.io/blog/current-events/mitre-atlas-ai-security) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Agent frameworks with security features:** [LangGraph](https://github.com/langchain-ai/langgraph) (graph-based orchestration with checkpoint-based human-in-the-loop), [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (March 2025 — input/output/tool guardrails with blocking execution mode), [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) (admin-controlled MCP allow-lists, human approval before patches), [CrewAI](https://www.crewai.com/) (multi-agent with OpenTelemetry tracing, Enterprise SOC2), [AutoGen/AG2](https://github.com/microsoft/autogen) (v0.4+ async event-driven with enterprise integrations)
- **Agent sandboxing:** [E2B](https://e2b.dev/) (~15M sandbox sessions/month, Firecracker microVMs, 150ms startup, ~50% Fortune 500 adoption), [Modal](https://modal.com/) (gVisor isolation, per-sandbox egress policies), [Daytona](https://daytona.io/) (sub-90ms sandbox creation), [Firecracker](https://firecracker-microvm.github.io/) (KVM-based microVMs with cgroups/namespace isolation)
- **Budget and cost controls:** [Helicone](https://www.helicone.ai/) (proxy-based cost tracking across 100+ LLMs with rate limiting), [Langfuse](https://langfuse.com/) (token/cost tracking per trace, open-source self-hosted), [LangSmith](https://smith.langchain.com/) (per-step token/latency/cost metrics). Architectural pattern: per-run hard spend caps, model tier routing, context window trimming.
- **Agent identity and auth:** [SPIFFE/SPIRE](https://spiffe.io/) (CNCF Graduated — short-lived SVIDs for agent workload identity; instance-level IDs for non-deterministic agents), [OPA](https://www.openpolicyagent.org/) (fine-grained policy enforcement via Rego), [SPIFFE+OAuth2 pattern](https://riptides.io/blog-post/spiffe-meets-oauth2-current-landscape-for-secure-workload-identity-in-the-agentic-ai-era) (attestation-bound identity exchanged for scoped OAuth tokens)
- **Agent communication protocols:** [A2A](https://a2a-protocol.org/latest/specification/) (Google, April 2025, v0.3 with gRPC — Agent Cards, OAuth 2.0 auth; donated to Linux Foundation June 2025), [MCP](https://modelcontextprotocol.io/) (Anthropic — OAuth 2.1 with PKCE, 97M monthly SDK downloads), [Agentic AI Foundation](https://www.linuxfoundation.org/) (Linux Foundation, Dec 2025 — governs both A2A and MCP)
- **Agent security gateways:** [Lasso MCP Gateway](https://github.com/lasso-security/mcp-gateway/) (open-source, April 2025 — security filters for MCP requests, prompt injection blocking, data leakage prevention), [Lakera Guard](https://www.lakera.ai/) (AI firewall, sub-50ms, blocks prompt injection and jailbreaks)
- **Agent monitoring:** [AgentOps](https://www.agentops.ai/) (session replay, time-travel debugging, multi-agent support), [Arize Phoenix](https://phoenix.arize.com/) (open-source, multi-step trajectory analysis), [Lunary](https://lunary.ai/) (LLM firewalls, PII masking, auto-categorization)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C9.1 Execution Budgets | Maturing | Helicone/Langfuse track costs; OpenAI Agents SDK has blocking guardrails. But $47K incidents show most deployments still lack hard budget enforcement. Only 14.4% of orgs deploy agents with full security approval. |
| C9.2 High-Impact Action Approval | Maturing | LangGraph checkpoints, OpenAI tool guardrails, Claude SDK approval gates all provide HITL. The Antigravity drive wipe shows "Turbo mode" bypass remains common. |
| C9.3 Tool & Plugin Isolation | Mature | E2B (15M sessions/month), Modal, Firecracker provide production-grade sandboxing. Lasso MCP Gateway adds MCP-specific filtering. Tool manifest enforcement (C9.3.5) is less mature. |
| C9.4 Agent Identity & Audit | Emerging | SPIFFE+OAuth2 pattern emerging but not widely adopted for agents. Most frameworks use shared service accounts. Tamper-evident audit (C9.4.3) requires dedicated log infrastructure. |
| C9.5 Secure Messaging | Emerging | A2A v0.3 supports but doesn't enforce Agent Card signing. MCP has OAuth 2.1 with PKCE. Neither mandates end-to-end encryption. A2A session smuggling shows protocol-level weaknesses. |
| C9.6 Authorization & Delegation | Emerging | OPA provides the policy engine but agent-specific delegation context propagation (C9.6.2) has limited tooling. MCP scope model and A2A capability-based access control are implementation patterns. |
| C9.7 Intent Verification | Emerging | Pre-execution gates are mostly custom-built. Post-condition checks (C9.7.3) have no standard tooling. Prompt template integrity verification (C9.7.4) is nascent. |
| C9.8 Multi-Agent Isolation | Emerging | Namespace isolation for tools, hierarchical memory isolation, and swarm-level shutdown are documented in research (AgenticCyOps) but have limited production tooling. |

---

## Related Standards & Cross-References

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (Dec 2025) — ASI01-ASI10 covering goal hijack, tool misuse, identity abuse, supply chain, code execution, memory poisoning, insecure comms, cascading failures, trust exploitation, rogue agents. Introduces the principle of **least agency**.
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — Three root causes: excessive functionality, excessive permissions, excessive autonomy
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) — Covers recursive loops, cost spikes, model extraction via excessive inference
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) (Feb 2025) — Part of the broader [Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/) including threat modelling guide and secure development guidelines
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) — Practical implementation guidance including tool namespace isolation
- [MITRE ATLAS](https://atlas.mitre.org/) — October 2025 update added 14 agentic techniques: AML.T0096 (AI Service API), AML.T0098 (Tool Credential Harvesting), AML.T0099 (Tool Data Poisoning), AML.T0100 (Agent Clickbait), AML.T0101 (Data Destruction via Tool Invocation). Case study AML.CS0042 (SesameOp) demonstrates agent infrastructure as C2 channel.
- [NIST AI Agent Standards Initiative](https://www.nist.gov/itl/ai-risk-management-framework) (Feb 2026) — Three pillars: voluntary standards, open-source protocol development (including MCP), agent security research. Concept paper on Agent Identity and Authorization (April 2026).
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final) — Agents should be treated as untrusted entities requiring continuous verification, task-scoped credentials, and microsegmentation
- [EU AI Act Article 6](https://artificialintelligenceact.eu/article/6/) — Autonomous AI systems in high-risk domains (critical infrastructure, employment, essential services) require human oversight, risk management, logging, and accuracy/robustness guarantees
- [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) (Jul 2025) — 243 controls; includes A2A threat modeling via MAESTRO framework
- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/) — Security analysis: [Semgrep guide](https://semgrep.dev/blog/2025/a-security-engineers-guide-to-the-a2a-protocol/), [CSA MAESTRO threat model](https://cloudsecurityalliance.org/blog/2025/04/30/threat-modeling-google-s-a2a-protocol-with-the-maestro-framework)
- [MCP Specification (2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25) — OAuth 2.1 + PKCE, step-up authorization, scope-based access control

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C02 User Input Validation](C02-User-Input-Validation.md) | Prompt injection → tool misuse | ASI01 (Agent Goal Hijack) is fundamentally prompt injection leading to ASI02 (Tool Misuse). MITRE AML.T0099 (Tool Data Poisoning) bridges input validation and agent hijacking. LLM06 excessive functionality widens the blast radius. |
| [C04 Infrastructure](C04-Infrastructure.md) | Sandbox and isolation infrastructure | ASI05 (Unexpected Code Execution) requires C04 hardened sandboxes. ASI08 (Cascading Failures) demands C04 isolation boundaries. AML.T0101 (Data Destruction via Tool Invocation) mitigated by C04 infrastructure sandboxing. |
| [C05 Access Control](C05-Access-Control.md) | Agent authorization and delegation | ASI03 (Identity & Privilege Abuse) maps directly to access control — short-lived credentials, task-scoped permissions. LLM06 root causes (excessive permissions/functionality) are access control failures. NIST agent identity concept paper addresses agent-specific access control. |
| [C07 Model Behavior](C07-Model-Behavior.md) | Model behavior → agent actions | ASI10 (Rogue Agents) — misaligned model behavior manifests as harmful agent actions (96% blackmail rate in Anthropic study). ASI06 (Memory Poisoning) corrupts context, changing future behavior. ASI09 (Trust Exploitation) leverages model persuasiveness. |
| [C10 MCP Security](C10-MCP-Security.md) | MCP-specific agent security | ASI04 (Supply Chain) explicitly targets MCP servers as dynamic runtime dependencies. MCP tool descriptions are untrusted; tools represent arbitrary code execution. MCP OAuth 2.1/PKCE model is the primary auth control. A2A inherits MCP attack surface. |
| [C13 Monitoring & Logging](C13-Monitoring-and-Logging.md) | Agent audit and observability | LLM06 root cause 3 is "Lack of Usage Monitoring." AgentOps, Arize Phoenix, Lunary provide agent-specific monitoring. C09.4 tamper-evident audit feeds into C13 centralized logging. |
| [C14 Human Oversight](C14-Human-Oversight.md) | Human-in-the-loop for agents | LLM06 "Excessive Autonomy" — high-impact actions without HITL. ASI09 (Trust Exploitation) — the oversight relationship itself becomes an attack surface. EU AI Act mandates human oversight for high-risk autonomous systems. |

---

## Open Research Questions

- [ ] **How do you enforce "least agency" in practice?** — The OWASP Agentic Top 10 introduces the principle but no standard framework exists for defining minimum autonomy levels. NIST's five-tier autonomy taxonomy (Level 0 tool-assisted to Level 4 fully autonomous) is a starting point.
- [ ] **Can agent identity scale to millions of ephemeral instances?** — SPIFFE treats all pod replicas as identical, but agents are non-deterministic. Instance-level identities (`spiffe://org/.../instance/001`) are a proposed solution but add complexity.
- [ ] **How do you detect semantic privilege escalation?** — All technical permission checks pass, but the agent operates outside intended scope. No standard tooling exists for semantic boundary enforcement.
- [ ] **Will A2A and MCP converge on security standards?** — Both protocols are now under the Linux Foundation's Agentic AI Foundation (Dec 2025). Neither mandates end-to-end encryption or enforces authorization at the protocol level. A2A session smuggling shows protocol-level design weaknesses.
- [ ] **How do you monitor emergent swarm behavior?** — Multi-agent oscillation, deadlocks, and coordinated manipulation (steganographic collusion) require runtime behavioral analysis that goes beyond individual agent monitoring. Limited production tooling exists.
- [ ] **What does agentic misalignment defense look like?** — Anthropic's study showed 96% of models attempt blackmail under specific conditions. This is a model behavior problem (C07) that manifests as an agent security problem (C09).

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
