# C09: Autonomous Orchestration & Agentic Action Security

> **Source:** [`1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
> **Requirements:** 32 | **Sections:** 8

## Control Objective

Autonomous and multi-agent systems must execute only authorized, intended, and bounded actions. This control family reduces risk from tool misuse, privilege escalation, uncontrolled recursion/cost growth, protocol manipulation, and cross-agent or cross-tenant interference.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C9.1 | Execution Budgets, Loop Control, and Circuit Breakers | 5 | 9.1.1–9.1.5 |
| C9.2 | High-Impact Action Approval and Irreversibility Controls | 3 | 9.2.1–9.2.3 |
| C9.3 | Tool and Plugin Isolation and Safe Integration | 6 | 9.3.1–9.3.6 |
| C9.4 | Agent and Orchestrator Identity, Signing, and Tamper-Evident Audit | 4 | 9.4.1–9.4.4 |
| C9.5 | Secure Messaging and Protocol Hardening | 4 | 9.5.1–9.5.4 |
| C9.6 | Authorization, Delegation, and Continuous Enforcement | 4 | 9.6.1–9.6.4 |
| C9.7 | Intent Verification and Constraint Gates | 4 | 9.7.1–9.7.4 |
| C9.8 | Multi-Agent Domain Isolation and Swarm Risk Controls | 2 | 9.8.1–9.8.2 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Recursive agent loops causing unbounded API spend or compute consumption
- Tool misuse — agent calling dangerous tools (rm -rf, DROP TABLE) via prompt injection
- Privilege escalation through tool chaining (combining benign tools for malicious effect)
- Agent impersonation in multi-agent systems
- Confused deputy — agent acting with human's credentials beyond intended delegation scope

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Agent frameworks:** LangGraph, CrewAI, AutoGen, Claude Agent SDK (with built-in guardrails)
- **Sandboxing:** E2B, Modal, Firecracker for code execution sandboxes
- **Budget controls:** Token/cost limits in API calls, timeout-based circuit breakers
- **Approval workflows:** Human-in-the-loop gating via Slack/webhook integrations

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C9.1 Execution Budgets, Loop Control, and Circuit Breakers | _TBD_ | |
| C9.2 High-Impact Action Approval and Irreversibility Controls | _TBD_ | |
| C9.3 Tool and Plugin Isolation and Safe Integration | _TBD_ | |
| C9.4 Agent and Orchestrator Identity, Signing, and Tamper-Evident Audit | _TBD_ | |
| C9.5 Secure Messaging and Protocol Hardening | _TBD_ | |
| C9.6 Authorization, Delegation, and Continuous Enforcement | _TBD_ | |
| C9.7 Intent Verification and Constraint Gates | _TBD_ | |
| C9.8 Multi-Agent Domain Isolation and Swarm Risk Controls | _TBD_ | |

---

## Open Research Questions

- [ ] What's the right granularity for tool permissions in agentic systems?
- [ ] How do you prevent indirect prompt injection from causing tool misuse in multi-step agents?
- [ ] What budget/cost controls are adequate for autonomous agents?
- [ ] How should multi-agent trust boundaries be defined and enforced?

---

## Related Standards & Cross-References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/detail/sp/800-207/final)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

