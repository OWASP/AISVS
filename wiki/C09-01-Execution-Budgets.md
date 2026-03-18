# C9.1: Execution Budgets, Loop Control, and Circuit Breakers

> [Back to C09 Index](C09-Orchestration-and-Agents.md)
> **Last Researched:** 2026-03-18

## Purpose

Autonomous agents can enter runaway states — recursive loops, unbounded fan-out, or chain reactions across tool calls — that consume resources without bound. As of 2026, denial-of-wallet attacks against agentic AI are a material financial risk: Fortune 500 companies collectively leaked an estimated **$400M in unbudgeted cloud spend** from agentic AI cost overruns (Analytics Week, 2026). A single fintech startup reported a **$112,000 bill from a 48-hour attack**. No major agent framework has comprehensive built-in cost ceilings — budget enforcement requires external gateways or governance layers.

This section requires hard limits on runtime expansion (recursion depth, concurrency, wall-clock time, token usage, monetary spend) enforced by the orchestration runtime, not by the model itself.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.1.1** | **Verify that** per-execution budgets (max recursion depth, max fan-out/concurrency, wall-clock time, tokens, and monetary spend) are configured and enforced by the orchestration runtime. | 1 | D/V | **Unbounded resource consumption** (OWASP LLM10, ASI08). An agent entering a recursive planning loop or spawning excessive parallel tool calls can exhaust API budgets and compute. Cost modeling: GPT-4 class agents at 10 cycles/min, 10k tokens/cycle ≈ $3/min; 50 concurrent threads = $9,000/hour burn rate. | Review orchestration config for explicit budget parameters. Test by triggering deep recursion and high fan-out; confirm runtime halts at thresholds. Verify budgets are server-side. Check for both request-rate (req/s) AND token-rate (tokens/s) dual limiting. | LangGraph: `recursion_limit`; OpenAI Agents SDK: `max_turns` (default 8); CrewAI: `max_iter`; AutoGen: custom termination logic required. **No framework natively enforces dollar-denominated budgets** — requires external gateway (LiteLLM, Portkey) or governance layer (Microsoft Agent Governance Toolkit). |
| **9.1.2** | **Verify that** cumulative resource/spend counters are tracked per request chain and hard-stop the chain when thresholds are exceeded. | 2 | D/V | **Distributed budget evasion.** Agent spawning sub-agents may stay under per-call limits while exceeding aggregate budgets. Four attack variants identified: (1) single-agent hallucination loops, (2) multi-agent circular dependencies, (3) file system recursion, (4) cascading hallucination (87% downstream decision poisoning within 4 hours). | Trace multi-step execution; confirm cumulative counters (tokens, API calls, wall-clock, cost) span all steps and sub-agents. Verify hard-stop at aggregate level. Use provisional reservation + true-up pattern (reserve max_tokens upfront, refund after actual response). | Cumulative tracking across sub-agents not natively supported in most frameworks. Requires correlation via chain/trace ID. OpenTelemetry helps but needs custom budget-enforcement logic. Multi-agent loops are hardest to detect — each agent appears to be "making progress" individually. |
| **9.1.3** | **Verify that** circuit breakers terminate execution on budget violations. | 2 | D/V | **Graceless failure on overrun** (OWASP ASI08: Cascading Failures). Without circuit breakers, budget violations may be logged but not acted upon. OWASP guidance: *"If an agent starts looping and spamming an expensive tool, trip the circuit breaker immediately."* | Trigger budget violations in test; confirm: (a) execution halts immediately, (b) partial state cleaned up, (c) downstream consumers notified, (d) no further tool calls after breaker trips. Test both graceful and crash scenarios. | Circuit breaker patterns well-established in microservices (Hystrix, resilience4j) but application to agentic loops is newer. Microsoft Agent Governance Toolkit implements circuit breakers + SLO enforcement with sub-millisecond policy enforcement (<0.1ms per action). Key: breaker must sit in orchestration layer, not just API gateway. |
| **9.1.4** | **Verify that** security testing covers runaway loops, budget exhaustion, and partial-failure scenarios, confirming safe termination and consistent state. | 3 | V | **Untested failure modes.** LangGraph GitHub issue #6731 documents agents infinite-looping until recursion limit error fires, confirming this is often the last line of defense. AutoGen reportedly requires custom termination logic in every production deployment. | Review test suites for chaos/fault-injection tests: infinite loops, rapid fan-out, partial tool failures mid-chain, simultaneous budget violations. Confirm tests assert safe termination and state consistency. Include multi-agent circular dependency scenarios. | Few organizations have agentic-specific chaos engineering practices. Test harnesses need to simulate adversarial prompt patterns that induce loops. Shadow mode (log would-be throttle decisions without enforcement for 1-2 weeks) useful before going live with new limits. |
| **9.1.5** | **Verify that** budget and circuit-breaker policies are expressed as policy-as-code and are validated in CI/CD to prevent drift and unsafe configuration changes. | 3 | D/V | **Configuration drift and tampering.** 49% of employees use unsanctioned AI tools ("Shadow AI"), amplifying uncontrolled spend. Amazon Q incident (July 2025): malicious PR injected resource deletion commands with `--no-interactive` bypass. | Confirm policies in version-controlled files (OPA Rego, CUE, JSON Schema). Verify CI/CD validates policy files and rejects weakening below minimum thresholds. Microsoft AGT: 4-tier execution privilege rings with tool allowlists/denylists, sub-millisecond enforcement across 13+ frameworks. | Policy-as-code for agent budgets is emerging. Microsoft Agent Governance Toolkit covers all 10 OWASP ASI 2026 controls. OPA and similar engines can enforce this but require custom integration with agent runtimes. |

---

## Agent Framework Budget Controls (2026 State)

| Framework | Budget Control | Default | Limitation |
|-----------|---------------|---------|------------|
| **LangGraph** | `recursion_limit` | None documented | No cost ceiling; known infinite-loop bug (#6731) |
| **OpenAI Agents SDK** (v0.10.2) | `max_turns` | 8 turns | Throws `MaxTurnsExceededError`; no token/dollar budget |
| **CrewAI** | `max_iter` per task | 10-20 typical | ~56% more token overhead than LangGraph; flaky tool loops |
| **AutoGen/AG2** | Custom termination | Must implement | Default conditions insufficient for production |
| **Claude Agent SDK** (v0.1.48) | Deny-all baseline + allowlists | Per-subagent | Sandbox with network/domain restrictions; secrets isolated |
| **Microsoft AGT** | Token limits + circuit breakers + kill switch | `max_tokens_per_call=4096` | Sub-ms policy enforcement; saga orchestration with rollback |

**Key gap:** No framework natively enforces dollar-denominated budgets. Requires external gateways.

---

## Cost Control & Observability Tools

| Tool | Type | Key Capability |
|------|------|----------------|
| [LiteLLM](https://docs.litellm.ai/) | Open source gateway | Budgets/rate limits per user/team/key; 100+ LLM support; retry/fallback |
| [Helicone](https://www.helicone.ai/) | Open source observability | Per-request cost tracking; intelligent caching |
| [Portkey](https://portkey.ai/) | Commercial gateway (from $49/mo) | Guardrails, virtual keys, routing with fallbacks, audit trails |
| [Microsoft AGT](https://github.com/microsoft/agent-governance-toolkit) | Open source governance | 4-tier privilege rings; covers all OWASP ASI controls; 13+ frameworks |

### Denial-of-Wallet Rate Limiting Patterns

| Algorithm | Best For | DoW Protection |
|-----------|----------|:--------------:|
| Token Bucket | Real-time apps needing burst flexibility | Moderate |
| Leaky Bucket | Background workflows, max cost predictability | Strong |
| Fixed Window | MVPs, internal tools | Weak (boundary burst exploit) |
| Sliding Window | Production environments | Strong |

**Design principles:**
- **Provisional Reservation & True-Up**: Reserve budget upfront based on estimated max_tokens, refund difference after actual response
- **Dual Limiting**: Both request-rate (req/s) AND token-rate (tokens/s) controls
- **Per-Model Pricing Catalog**: Maintain input vs. output token rates per model
- Critical: *"You cannot protect costs you cannot measure."*

---

## OWASP Agentic Security Mapping

| OWASP Risk | AISVS Requirement | Relevance |
|------------|-------------------|-----------|
| ASI02: Tool Misuse & Exploitation | 9.1.1 | Recursive tool calls cause budget exhaustion |
| ASI06: Memory & Context Poisoning | 9.1.2 | Can trigger infinite retrieval loops |
| ASI07: Insecure Inter-Agent Communication | 9.1.2 | Enables multi-agent circular dependencies |
| **ASI08: Cascading Failures** | **9.1.3** | **Directly addresses circuit breakers, fan-out caps** |
| ASI10: Rogue Agents | 9.1.4 | Behavioral drift toward costly actions |
| LLM06: Excessive Agency | 9.1.1 | Agents with insufficient autonomy guardrails |
| LLM10: Unbounded Consumption | 9.1.1, 9.1.2 | Uncontrolled inference resource drain |

---

## Notable Incidents

| Date | Incident | Impact |
|------|----------|--------|
| Jul 2025 | Amazon Q malicious PR | Resource deletion commands with `--no-interactive` bypass |
| Sep 2025 | Anthropic AI-orchestrated espionage campaign | Thousands of requests/second autonomously |
| 2025-2026 | Fortune 500 agentic AI cost overruns | Estimated $400M collective unbudgeted cloud spend |
| 2025 | Fintech startup DoW attack | $112,000 bill from 48-hour attack via vulnerable endpoint |

---

## Related Standards & References

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
- [Denial of Wallet: Cost-Aware Rate Limiting](https://handsonarchitects.com/blog/2025/denial-of-wallet-cost-aware-rate-limiting-part-2/)
- [Agentic Resource Exhaustion: The Infinite Loop Attack](https://instatunnel.substack.com/p/agentic-resource-exhaustion-the-infinite)
- [The $400M Cloud Leak: AI FinOps 2026](https://analyticsweek.com/finops-for-agentic-ai-cloud-cost-2026/)
- [OpenTelemetry](https://opentelemetry.io/) — distributed tracing for cumulative budget tracking
- Circuit Breaker pattern (Michael Nygard, *Release It!*)

---

## Open Research Questions

- What are appropriate default budget thresholds for different agent use cases (coding assistants vs. data analysis vs. customer service)?
- How should budgets be allocated across sub-agents in hierarchical systems (fixed per-agent vs. shared pool)?
- Can adaptive budgets (dynamically adjusting based on task complexity) be made safe, or do they introduce exploitable flexibility?
- How do you handle budget enforcement for agents making external API calls with their own billing?
- Should agent frameworks standardize a budget/cost-ceiling API, or should this remain in the gateway/governance layer?
- How do you detect multi-agent circular dependencies where each agent individually appears to be making progress?

---

[C09 Index](C09-Orchestration-and-Agents.md) | [README](README.md)
