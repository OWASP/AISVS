# C7.4 Output & Action Limiting

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Output and action limiting constrains what the model can do and how much it can do. Without explicit limits, AI systems — especially agentic ones — can incur runaway costs through excessive API calls, execute high-impact actions (file writes, emails, code execution) without user awareness, or recursively invoke tools in unbounded chains. These controls enforce the principle of least privilege at the output and action layer, ensuring the model operates within defined boundaries.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.4.1** | **Verify that** the system enforces hard limits on requests and tokens per user to prevent cost spikes and denial of service. | 1 | D | **Cost explosion and resource exhaustion.** Without rate limits, a single user or attacker can generate massive API costs through high-volume or high-token requests — a single unthrottled agent can burn through $300/day in API costs. Autonomous agents routinely chain 10–20 sequential API calls per task, and a Reflexion loop running 10 cycles can consume 50x the tokens of a single pass. This also serves as a denial-of-service mitigation, preventing one user from consuming capacity needed by others. | Attempt to exceed configured rate limits (requests per minute, tokens per hour) and verify the system returns structured 429 responses with limit, usage, and reset-time details per RFC standards. Test per-user and system-wide limits. Confirm limits apply to both input and output tokens independently, with cost-weighted accounting across different models. Verify alerts fire at 50% and 80% budget thresholds. Validate that token usage is reported in response headers so agents can self-throttle. | API gateways like Kong (with its [token rate-limiting plugin](https://konghq.com/blog/engineering/token-rate-limiting-and-tiered-access-for-ai-usage)), Zuplo, and AWS API Gateway support token-based rate limiting. As of early 2026, best practice is to layer three levels of limits: per-request `max_tokens`, per-task token budgets, and per-day/per-month spending caps. Cost-based limiting should track spending in dollar-equivalent units rather than raw token counts, with cost multipliers per model reflecting actual provider pricing. Completion tokens should be weighted differently from prompt tokens. |
| **7.4.2** | **Verify that** the model cannot execute high-impact actions (like writing files, sending emails, or executing code) without explicit user confirmation. | 1 | D/V | **Unauthorized actions via prompt injection or model error (OWASP LLM06:2025, OWASP Agentic ASI02 Tool Misuse, MITRE ATLAS AML.T0054).** The July 2025 Amazon Q incident (CVE-2025-8217) demonstrated this concretely: a compromised VS Code extension contained injected prompts instructing the agent to delete file systems, clear configs, and destroy AWS resources. The "Lethal Trifecta" pattern — where an agent has access to private data, processes untrusted tokens, and has an exfiltration vector — makes any tool-bearing agent vulnerable to weaponization. | Identify all high-impact actions the model can invoke. Attempt to trigger each action via normal prompts and via prompt injection payloads (including indirect injection through documents and shared data sources). Verify the system always presents a confirmation dialog before execution. Test that confirmation cannot be bypassed by prompt injection — the model must not be able to confirm its own actions. Verify the confirmation UI clearly describes the action, resources affected, and irreversibility. Test that the confirmation mechanism is implemented at the application layer, not within the model's prompt context. | As of early 2026, the OpenAI Agents SDK includes built-in guardrails with tool confirmation hooks. LangChain provides `HumanInTheLoopMiddleware` that can be configured to require approval for sensitive operations while auto-approving safe ones. LangGraph supports allowlisted tool registries and sandboxed file I/O. The key architectural pattern is separating planning from execution with a validation gate between them — the agent decides what to do, a separate component validates whether it should, and only then does execution proceed. For agentic systems, see also C9 (Orchestration & Agents). |
| **7.4.3** | **Verify that** the application or orchestration framework explicitly configures and enforces the maximum depth of recursive calls, delegation limits, and the list of allowed external tools. | 2 | D | **Runaway agent loops and unauthorized tool access (OWASP Agentic ASI03 Identity & Privilege Abuse).** Without explicit recursion limits, an agentic system can enter infinite loops (agent A calls agent B calls agent A). Without tool allowlists, a model may discover and invoke tools it was not intended to use. The ICLR 2025 ASB benchmark found 82.4% of models vulnerable to inter-agent trust exploitation — agents that resist direct malicious commands will execute the same payloads when requested by peer agents, making delegation limits critical. | Review orchestration configuration for: maximum recursion depth, maximum delegation chain length, explicit tool allowlist, and per-agent permission scoping. Attempt to trigger recursive loops and verify the system halts at the configured depth. Attempt to invoke tools not on the allowlist and verify rejection. Test inter-agent delegation: verify agent B cannot escalate agent A's permissions or invoke tools not in A's allowlist. Confirm that MCP server connections are audited and not exposed to untrusted networks. | As of early 2026, LangChain, CrewAI, AutoGen (AG2), and LangGraph all provide recursion depth settings, but defaults remain permissive and must be hardened. The OWASP Agentic Top 10 (December 2025) codified the "principle of least agency" — agents should receive only the minimum autonomy required for their authorized task, not just least privilege for data access. Tool allowlists should be a positive security model (deny by default, allow explicitly). NIST has been urged to update SP 800-160 and SP 800-218 to include minimum engineering requirements for action authority, tool invocation security, and operational containment in agentic systems. |

---

## Implementation Guidance (2025-2026 Landscape)

### The Agentic AI Security Challenge

By mid-2025, over 70% of enterprise AI deployments involved multi-agent or action-based systems, dramatically expanding the attack surface for output-triggered actions. Cisco's State of AI Security 2026 report found that 83% of organizations plan to deploy agentic AI, but only 29% feel ready to secure it. The ICLR 2025 Agent Security Bench (ASB) quantified the risk: while 41.2% of models succumb to direct prompt injection, 52.9% are vulnerable to RAG backdoor attacks, and 82.4% can be compromised through **inter-agent trust exploitation** — where LLMs that resist direct malicious commands execute identical payloads when requested by peer agents.

The OWASP Top 10 for Agentic Applications, released in December 2025 by more than 100 industry experts, formalized the security categories that matter most: Agent Behavior Hijacking (ASI01), Tool Misuse (ASI02), and Identity & Privilege Abuse (ASI03) are the top three risks. The framework introduced the **principle of least agency** — it is no longer just about what an agent can access, but how much freedom it has to act on that access without checking back with a human. Autonomy should be earned, not a default setting.

### The Lethal Trifecta

A useful mental model for evaluating action-limiting risk is the "Lethal Trifecta." An agentic system is fundamentally vulnerable when it has all three of the following properties simultaneously:

1. **Access to private data** — the agent can read emails, documents, databases
2. **Exposure to untrusted tokens** — the agent processes input from external sources (shared docs, web content, calendar invites)
3. **Exfiltration vector** — the agent can make external requests (render images, call APIs, generate links)

If your agentic system has all three, it is exploitable through indirect prompt injection regardless of other safeguards. The July 2025 Amazon Q incident (CVE-2025-8217) demonstrated this pattern: a compromised extension contained injected instructions to delete file systems and destroy AWS resources. Mitigations should aim to remove at least one leg of the trifecta — for example, by segmenting agent access to limit data sources, restricting external request capabilities, or sanitizing all untrusted inputs before ingestion.

### Tool-Use Restriction Patterns

Modern agentic frameworks have converged on several defensive patterns for action limiting:

- **Function-level policies**: Tools like Lasso Security enforce tool usage boundaries through function-level policies and real-time validation, ensuring agents cannot invoke tools outside their role or without context-aware authorization. The OpenAI Agents SDK (as of early 2026) includes built-in guardrail hooks for tool confirmation, making this pattern a first-class framework feature rather than a bolt-on.
- **Positive security model for tool access**: The tool allowlist should be deny-by-default, allow-explicitly — not a blocklist. LangChain, CrewAI, AutoGen (AG2), and LangGraph all support tool allowlists, but defaults are often permissive and must be hardened. MCP (Model Context Protocol) server connections should be audited and never exposed to untrusted networks.
- **Separation of planning from execution**: Architecture should separate the agent's planning phase (deciding what to do) from the execution phase (actually doing it), with a validation gate between them. This prevents prompt injection from directly triggering tool invocations. LangGraph's architecture explicitly supports this pattern with sandboxed file I/O and human-in-the-loop confirmation on writes.
- **Sandboxed execution environments**: High-impact actions (file writes, code execution, network calls) should run in isolated sandboxes with resource limits, preventing lateral movement even if an action is authorized. This is especially important given that MITRE ATLAS (updated October 2025 with 14 new agent-specific techniques) documents tool abuse as a core attack path.

### Rate Limiting and Cost Controls

AI-specific rate limiting must account for several dimensions beyond traditional API rate limits. Gartner predicts that more than 30% of the increase in API demand will come from AI and LLM tools by 2026, making token-aware rate limiting a critical infrastructure concern:

- **Token-based limits**: Separate limits for input and output tokens, since a single prompt can generate thousands of output tokens. Track prompt tokens and completion tokens independently, reading actual usage from LLM provider response bodies (e.g., OpenAI's `usage.total_tokens`). Completion tokens should be weighted differently from prompt tokens to reflect provider pricing.
- **Cost-based limits**: Total spend per user per period, aggregated across multiple model invocations in a pipeline. Assign cost multipliers per model and track in dollar-equivalent units rather than raw token counts. Set alerts at 50% and 80% of budget thresholds with automatic suspension when ceilings are exceeded.
- **Tiered budgets**: Layer three levels of limits — per-request `max_tokens`, per-task token budgets, and per-day/per-month spending caps. This prevents both runaway individual requests and slow-burn cost accumulation across many small requests.
- **Per-action rate limits**: High-impact actions (email sends, file writes) should have their own rate limits independent of general API rate limits.
- **Agent-aware traffic management**: AI agent traffic should be tagged and managed separately from human user traffic via API key metadata, since agents produce fundamentally different consumption patterns — bursty, sequential, and high-volume.

### Human Confirmation Design

The confirmation mechanism for high-impact actions must be implemented at the application layer, not within the model's prompt. Critical design principles:

- The model must not be able to confirm its own actions (no self-approval). The confirmation gate must live outside the model's context window entirely.
- Confirmation dialogs should include a clear description of the action, the resources affected, and the irreversibility of the operation.
- For agentic systems with many tool calls, implement tiered confirmation: auto-approve low-risk actions (read-only queries), require confirmation for medium-risk (file writes, data modifications), and require re-authentication for high-risk (deletions, financial transactions, external communications).
- Implement Content Security Policy (CSP) controls on agent-generated output to block or restrict external image loading and link rendering, which are common exfiltration vectors in indirect prompt injection attacks.
- Monitor for unusual patterns of external requests generated by agent outputs — anomalous outbound traffic may indicate a successful injection exploiting the exfiltration leg of the Lethal Trifecta.

### Singapore Model AI Governance Framework for Agentic AI (2025)

The Singapore IMDA published a governance framework specifically for agentic AI in 2025, recommending strong authentication and access controls ensuring least-privilege principles, continuous monitoring that flags anomalous requests or deviations from typical behavior patterns to trigger shutdown, and clear accountability chains for autonomous agent actions.

---

## Related Standards & References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — directly addresses the risks of unconstrained model actions
- [OWASP Top 10 for Agentic Applications (December 2025)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — ASI01 (Behavior Hijacking), ASI02 (Tool Misuse), ASI03 (Identity & Privilege Abuse) and the principle of least agency
- [OWASP LLM Top 10 — Overreliance](https://genai.owasp.org/) — risks from excessive trust in model decisions
- [NIST AI 100-1 (AI Risk Management Framework)](https://www.nist.gov/artificial-intelligence/ai-risk-management-framework) — governance context for action limiting
- [MITRE ATLAS](https://atlas.mitre.org/) — AML.T0054 (LLM Jailbreak) and 14 new agent-specific techniques added October 2025 (in collaboration with Zenity Labs)
- AISVS C9 (Orchestration & Agents) — complementary controls for agentic architectures
- [Agent Security Bench (ASB) — ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/5750f91d8fb9d5c02bd8ad2c3b44456b-Paper-Conference.pdf) — benchmark quantifying agent vulnerability rates including 82.4% inter-agent trust exploitation
- [Amazon Q Developer CVE-2025-8217 Analysis](https://colinmcnamara.com/blog/amazon-q-ai-security-incident-analysis) — real-world tool injection incident demonstrating action-limiting failures
- [AWS Security Bulletin AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/) — official advisory for the Amazon Q VS Code extension compromise
- [Lasso Security: Agentic AI Security Threats 2025](https://www.lasso.security/blog/agentic-ai-security-threats-2025) — top 10 agentic AI security threats with mitigations
- [Singapore Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf) — government framework for agentic AI governance
- [AI Security in 2026: The Lethal Trifecta](https://airia.com/ai-security-in-2026-prompt-injection-the-lethal-trifecta-and-how-to-defend/) — the three-property model for evaluating agent exploitability
- [Token-Based Rate Limiting for AI Agents (Zuplo, 2026)](https://zuplo.com/learning-center/token-based-rate-limiting-ai-agents) — practical guide to agent-aware API rate limiting
- [Kong Token Rate Limiting & Tiered Access](https://konghq.com/blog/engineering/token-rate-limiting-and-tiered-access-for-ai-usage) — implementation patterns for AI-specific rate limiting
- [OpenAI Agents SDK — Guardrails](https://openai.github.io/openai-agents-python/guardrails/) — built-in guardrail and tool confirmation framework
- [TRiSM for Agentic AI (2025)](https://arxiv.org/html/2506.04133v2) — trust, risk, and security management in multi-agent systems
- [Agentic AI Security: Threats, Defenses, and Open Challenges (2025)](https://arxiv.org/html/2510.23883v1) — comprehensive survey of agentic AI attack vectors

---

## Open Research Questions

- How should confirmation UX be designed to avoid "confirmation fatigue" where users automatically approve all actions? Tiered confirmation models show promise but lack empirical validation at scale.
- What is the right granularity for tool allowlists — per-tool, per-tool-per-action, or per-tool-per-action-per-resource? The OWASP Agentic Top 10's "least agency" principle suggests the answer depends on the autonomy budget for each use case.
- How should cost limits be set for multi-model pipelines where a single user request triggers multiple model invocations across different providers? Dollar-equivalent budgets look promising, but cross-provider cost normalization remains unsolved.
- Given the 82.4% inter-agent trust exploitation rate found by ASB (ICLR 2025), how should tool authorization be scoped in multi-agent systems where agents delegate to each other? Current frameworks lack per-delegation permission attenuation.
- Can formal verification methods be applied to agent tool-use policies to prove that certain dangerous action sequences are unreachable?
- How should action limiting adapt to emergent agentic capabilities (e.g., computer-use agents, browser-use agents) where the boundary between "tool call" and "general action" is blurred?
- As MCP adoption grows, what security controls should govern MCP server discovery and connection? Currently, most MCP configurations are trust-on-first-use with no runtime policy enforcement.
- How should the Lethal Trifecta be evaluated in multi-tenant environments where different users' data flows through the same agent infrastructure?

---
