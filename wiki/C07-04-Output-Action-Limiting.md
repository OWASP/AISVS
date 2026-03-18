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

## Related Standards & References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — directly addresses the risks of unconstrained model actions
- [OWASP LLM Top 10 — Overreliance](https://genai.owasp.org/) — risks from excessive trust in model decisions
- [NIST AI 100-1 (AI Risk Management Framework)](https://www.nist.gov/artificial-intelligence/ai-risk-management-framework) — governance context for action limiting
- AISVS C9 (Orchestration & Agents) — complementary controls for agentic architectures

---

## Open Research Questions

- How should confirmation UX be designed to avoid "confirmation fatigue" where users automatically approve all actions?
- What is the right granularity for tool allowlists — per-tool, per-tool-per-action, or per-tool-per-action-per-resource?
- How should cost limits be set for multi-model pipelines where a single user request triggers multiple model invocations across different providers?

---
