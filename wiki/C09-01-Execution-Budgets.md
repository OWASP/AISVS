# C9.1: Execution Budgets, Loop Control, and Circuit Breakers

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Autonomous agents can enter runaway states -- recursive loops, unbounded fan-out, or chain reactions across tool calls -- that consume resources without bound. This section requires hard limits on runtime expansion (recursion depth, concurrency, wall-clock time, token usage, monetary spend) enforced by the orchestration runtime, not by the model itself. Circuit breakers must halt execution and leave the system in a safe, consistent state when budgets are exceeded.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.1.1** | **Verify that** per-execution budgets (max recursion depth, max fan-out/concurrency, wall-clock time, tokens, and monetary spend) are configured and enforced by the orchestration runtime. | 1 | D/V | **Unbounded resource consumption.** An agent entering a recursive planning loop or spawning excessive parallel tool calls can exhaust API budgets, compute, or cause cascading failures. Without runtime-enforced limits, a single malformed prompt or logic error can lead to runaway spend. | Review orchestration configuration for explicit budget parameters. Test by triggering deep recursion and high fan-out scenarios; confirm the runtime halts execution at configured thresholds. Verify budgets are enforced server-side (not client-side or model-side). | Most agent frameworks (LangGraph, CrewAI, AutoGen) support max_iterations or step limits but monetary spend caps are often implemented at the API billing layer, not the orchestration layer. Token budgets may need to account for both input and output tokens across the full chain. |
| **9.1.2** | **Verify that** cumulative resource/spend counters are tracked per request chain and hard-stop the chain when thresholds are exceeded. | 2 | D/V | **Distributed budget evasion.** An agent that spawns sub-agents or chains multiple tool calls may stay under per-call limits while exceeding aggregate budgets. Without cumulative tracking across the full request chain, cost and resource consumption can grow unchecked. | Trace a multi-step agent execution and confirm cumulative counters (tokens, API calls, wall-clock time, cost) are maintained across all steps and sub-agent invocations. Verify hard-stop triggers at the aggregate level, not just per-step. | Cumulative tracking across sub-agents and async fan-out is not natively supported in most frameworks. Requires correlation via a chain/trace ID. Distributed tracing tools (OpenTelemetry) can help but need custom budget-enforcement logic on top. |
| **9.1.3** | **Verify that** circuit breakers terminate execution on budget violations. | 2 | D/V | **Graceless failure on overrun.** Without circuit breakers, budget violations may be logged but not acted upon, or execution may continue in a degraded state that produces incorrect or dangerous outputs. Circuit breakers ensure fail-closed behavior. | Trigger budget violations in a test environment and confirm: (a) execution halts immediately, (b) partial state is cleaned up or marked incomplete, (c) downstream consumers are notified of the halt, (d) no further tool calls or LLM invocations occur after the breaker trips. | Circuit breaker patterns are well-established in microservices (Hystrix, resilience4j) but their application to agentic loops is newer. Key challenge: ensuring the circuit breaker sits in the orchestration layer, not just at the API gateway level, so it can interrupt mid-chain execution. |
| **9.1.4** | **Verify that** security testing covers runaway loops, budget exhaustion, and partial-failure scenarios, confirming safe termination and consistent state. | 3 | V | **Untested failure modes.** Without explicit testing of runaway and partial-failure scenarios, budget controls may have edge cases (e.g., async tasks that escape the breaker, race conditions in counter updates) that are only discovered in production incidents. | Review test suites for explicit chaos/fault-injection tests covering: infinite loops, rapid fan-out, partial tool failures mid-chain, simultaneous budget violations across concurrent branches. Confirm tests assert on safe termination and state consistency. | This is a testing maturity requirement. Few organizations currently have agentic-specific chaos engineering practices. Test harnesses need to simulate adversarial prompt patterns that induce loops, not just random faults. |
| **9.1.5** | **Verify that** budget and circuit-breaker policies are expressed as policy-as-code and are validated in CI/CD to prevent drift and unsafe configuration changes. | 3 | D/V | **Configuration drift and tampering.** If budget limits are set via ad-hoc configuration (environment variables, UI settings), they can drift or be accidentally weakened. An attacker with limited access could lower thresholds or disable circuit breakers. | Confirm budget policies are defined in version-controlled policy files (OPA Rego, CUE, JSON Schema, etc.). Verify CI/CD pipelines validate policy files and reject changes that weaken budgets below minimum thresholds. Check for policy unit tests. | Policy-as-code for agent budgets is an emerging practice. OPA and similar engines can enforce this but require custom integration with agent orchestration runtimes. The "minimum safe threshold" concept needs organizational definition. |

---

## Related Standards & References

- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) -- directly addresses resource exhaustion risks in LLM applications
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) -- covers agents taking more actions than intended
- Circuit Breaker pattern (Michael Nygard, *Release It!*) -- foundational pattern for fail-safe resource management
- [OpenTelemetry](https://opentelemetry.io/) -- distributed tracing for cumulative budget tracking across agent chains

---

## Open Research Questions

- What are appropriate default budget thresholds for different agent use cases (coding assistants vs. data analysis vs. customer service)?
- How should budgets be allocated across sub-agents in a hierarchical multi-agent system (fixed per-agent vs. shared pool)?
- Can adaptive budgets (dynamically adjusting based on task complexity) be made safe, or do they introduce exploitable flexibility?
- How do you handle budget enforcement for agents that make external API calls with their own billing (e.g., agent calls a paid third-party service)?

---
