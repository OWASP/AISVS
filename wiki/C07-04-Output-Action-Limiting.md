# C7.4 Output & Action Limiting

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Output and action limiting constrains what the model can do and how much it can do. Without explicit limits, AI systems — especially agentic ones — can incur runaway costs through excessive API calls, execute high-impact actions (file writes, emails, code execution) without user awareness, or recursively invoke tools in unbounded chains. These controls enforce the principle of least privilege at the output and action layer, ensuring the model operates within defined boundaries.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.4.1** | **Verify that** the system enforces hard limits on requests and tokens per user to prevent cost spikes and denial of service. | 1 | D | **Cost explosion and resource exhaustion.** Without rate limits, a single user (or attacker) can generate massive API costs through high-volume or high-token requests. This also serves as a denial-of-service mitigation, preventing one user from consuming capacity needed by others. | Attempt to exceed configured rate limits (requests per minute, tokens per hour, etc.) and verify the system returns appropriate rate-limit errors. Test both per-user and system-wide limits. Confirm limits apply to both input and output tokens. | Standard API gateway rate limiting (e.g., Kong, AWS API Gateway, nginx) applies here. AI-specific considerations include limiting output tokens separately from input tokens, and setting cost-based limits (total spend per user per period) in addition to request counts. |
| **7.4.2** | **Verify that** the model cannot execute high-impact actions (like writing files, sending emails, or executing code) without explicit user confirmation. | 1 | D/V | **Unauthorized actions via prompt injection or model error.** If a model has tool access (file system, email, databases, code execution), a prompt injection attack or hallucinated tool call could trigger destructive or privacy-violating actions without the user's knowledge. This directly maps to OWASP LLM06:2025 (Excessive Agency). | Identify all high-impact actions the model can invoke. Attempt to trigger each action via normal prompts and via prompt injection payloads. Verify the system always presents a confirmation dialog before execution. Test that confirmation cannot be bypassed by prompt injection (e.g., the model cannot click "confirm" on its own behalf). | The confirmation mechanism must be implemented at the application layer, not within the model's prompt. The model should not be able to confirm its own actions. Frameworks like LangChain and AutoGPT have added confirmation steps, but implementations vary in robustness. For agentic systems, see also C9 (Orchestration & Agents). |
| **7.4.3** | **Verify that** the application or orchestration framework explicitly configures and enforces the maximum depth of recursive calls, delegation limits, and the list of allowed external tools. | 2 | D | **Runaway agent loops and unauthorized tool access.** Without explicit recursion limits, an agentic system can enter infinite loops (agent A calls agent B calls agent A). Without tool allowlists, a model may discover and invoke tools it was not intended to use. | Review orchestration configuration for: maximum recursion depth, maximum delegation chain length, and explicit tool allowlist. Attempt to trigger recursive loops and verify the system halts at the configured depth. Attempt to invoke tools not on the allowlist and verify rejection. | Applies primarily to agentic and multi-agent architectures. LangChain, CrewAI, AutoGen, and similar frameworks provide recursion depth settings, but defaults are often permissive. The tool allowlist should be a positive security model (deny by default, allow explicitly) rather than a blocklist. |

---

## Implementation Guidance (2025-2026 Landscape)

### The Agentic AI Security Challenge

By mid-2025, over 70% of enterprise AI deployments involved multi-agent or action-based systems, dramatically expanding the attack surface for output-triggered actions. The ICLR 2025 Agent Security Bench (ASB) quantified the risk: while 41.2% of models succumb to direct prompt injection, 52.9% are vulnerable to RAG backdoor attacks, and 82.4% can be compromised through **inter-agent trust exploitation** -- where LLMs that resist direct malicious commands execute identical payloads when requested by peer agents.

### Tool-Use Restriction Patterns

Modern agentic frameworks have converged on several defensive patterns for action limiting:

- **Function-level policies**: Tools like Lasso Security enforce tool usage boundaries through function-level policies and real-time validation, ensuring agents cannot invoke tools outside their role or without context-aware authorization.
- **Positive security model for tool access**: The tool allowlist should be deny-by-default, allow-explicitly -- not a blocklist. LangChain, CrewAI, and AutoGen all support tool allowlists, but defaults are often permissive and must be hardened.
- **Separation of planning from execution**: Architecture should separate the agent's planning phase (deciding what to do) from the execution phase (actually doing it), with a validation gate between them. This prevents prompt injection from directly triggering tool invocations.
- **Sandboxed execution environments**: High-impact actions (file writes, code execution, network calls) should run in isolated sandboxes with resource limits, preventing lateral movement even if an action is authorized.

### Rate Limiting and Cost Controls

AI-specific rate limiting must account for several dimensions beyond traditional API rate limits:

- **Token-based limits**: Separate limits for input and output tokens, since a single prompt can generate thousands of output tokens.
- **Cost-based limits**: Total spend per user per period, aggregated across multiple model invocations in a pipeline.
- **Compute quota controls**: Automatic suspensions when cost thresholds are exceeded, with monitoring to avoid overload scenarios.
- **Per-action rate limits**: High-impact actions (email sends, file writes) should have their own rate limits independent of general API rate limits.

### Human Confirmation Design

The confirmation mechanism for high-impact actions must be implemented at the application layer, not within the model's prompt. Critical design principles:

- The model must not be able to confirm its own actions (no self-approval).
- Confirmation dialogs should include a clear description of the action, the resources affected, and the irreversibility of the operation.
- For agentic systems with many tool calls, consider tiered confirmation: auto-approve low-risk actions, require confirmation for medium-risk, and require re-authentication for high-risk.

### Singapore Model AI Governance Framework for Agentic AI (2025)

The Singapore IMDA published a governance framework specifically for agentic AI in 2025, recommending strong authentication and access controls ensuring least-privilege principles, continuous monitoring that flags anomalous requests or deviations from typical behavior patterns to trigger shutdown, and clear accountability chains for autonomous agent actions.

---

## Related Standards & References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — directly addresses the risks of unconstrained model actions
- [OWASP LLM Top 10 — Overreliance](https://genai.owasp.org/) — risks from excessive trust in model decisions
- [NIST AI 100-1 (AI Risk Management Framework)](https://www.nist.gov/artificial-intelligence/ai-risk-management-framework) — governance context for action limiting
- AISVS C9 (Orchestration & Agents) — complementary controls for agentic architectures
- [Agent Security Bench (ASB) — ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf) — benchmark quantifying agent vulnerability rates
- [Lasso Security: Agentic AI Security Threats 2025](https://www.lasso.security/blog/agentic-ai-security-threats-2025) — top 10 agentic AI security threats with mitigations
- [Singapore Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf) — government framework for agentic AI governance
- [TRiSM for Agentic AI (2025)](https://arxiv.org/html/2506.04133v2) — trust, risk, and security management in multi-agent systems
- [Agentic AI Security: Threats, Defenses, and Open Challenges (2025)](https://arxiv.org/html/2510.23883v1) — comprehensive survey of agentic AI attack vectors

---

## Open Research Questions

- How should confirmation UX be designed to avoid "confirmation fatigue" where users automatically approve all actions? Tiered confirmation models show promise but lack empirical validation.
- What is the right granularity for tool allowlists -- per-tool, per-tool-per-action, or per-tool-per-action-per-resource?
- How should cost limits be set for multi-model pipelines where a single user request triggers multiple model invocations across different providers?
- Given the 82.4% inter-agent trust exploitation rate found by ASB (ICLR 2025), how should tool authorization be scoped in multi-agent systems where agents delegate to each other?
- Can formal verification methods be applied to agent tool-use policies to prove that certain dangerous action sequences are unreachable?
- How should action limiting adapt to emergent agentic capabilities (e.g., computer-use agents, browser-use agents) where the boundary between "tool call" and "general action" is blurred?

---
