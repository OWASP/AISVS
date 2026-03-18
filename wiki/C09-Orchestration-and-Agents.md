# C09: Autonomous Orchestration & Agentic Action Security

> **Source:** [`1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
> **Requirements:** 32 | **Sections:** 8

## Control Objective

Autonomous and multi-agent systems must execute only authorized, intended, and bounded actions. This control family reduces risk from tool misuse, privilege escalation, uncontrolled recursion/cost growth, protocol manipulation, and cross-agent or cross-tenant interference.

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
| C9.8 | Multi-Agent Domain Isolation and Swarm Risk Controls | 2 | [C09-08-Multi-Agent-Isolation](C09-08-Multi-Agent-Isolation.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Recursive agent loops causing unbounded API spend or compute consumption
- Tool misuse -- agent calling dangerous tools (rm -rf, DROP TABLE) via prompt injection
- Privilege escalation through tool chaining (combining benign tools for malicious effect)
- Agent impersonation in multi-agent systems
- Confused deputy -- agent acting with human's credentials beyond intended delegation scope
- Replay attacks on inter-agent messages to re-trigger actions
- Emergent swarm behaviors in multi-agent deployments leading to resource exhaustion or oscillation

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Agent frameworks:** LangGraph, CrewAI, AutoGen, Claude Agent SDK (with built-in guardrails)
- **Sandboxing:** E2B, Modal, Firecracker for code execution sandboxes
- **Budget controls:** Token/cost limits in API calls, timeout-based circuit breakers
- **Approval workflows:** Human-in-the-loop gating via Slack/webhook integrations
- **Identity/Auth:** SPIFFE/SPIRE for workload identity, OPA for policy enforcement
- **Messaging:** A2A protocol (Google), MCP (Anthropic) for structured agent communication

---

## Related Standards & Cross-References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C02 User Input Validation | Prompt injection leading to tool misuse | C02 covers input-level defenses; C09 covers execution-level containment |
| C05 Access Control | Authorization enforcement | C05 covers model/data access; C09 covers agent action authorization |
| C10 MCP Security | Tool/server integration security | C10 is MCP-protocol-specific; C09 is protocol-agnostic orchestration |
| C13 Monitoring and Logging | Audit and observability | C13 covers general AI logging; C09.4 covers agent-specific tamper-evident audit |
| C14 Human Oversight | Human-in-the-loop controls | C14 covers oversight broadly; C09.2/C09.7 cover approval gates for agent actions |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
