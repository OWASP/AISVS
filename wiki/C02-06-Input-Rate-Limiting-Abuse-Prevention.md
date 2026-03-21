# C2.6 Input Rate Limiting & Abuse Prevention

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation)

## Purpose

AI systems are expensive to operate (each inference consumes GPU resources and incurs API costs) and are attractive targets for denial-of-service attacks, brute-force prompt injection attempts, and automated abuse. Rate limiting and abuse detection prevent resource exhaustion, budget overruns, and systematic probing. In agentic architectures, additional controls are needed to prevent runaway planning loops and unbounded tool call chains that can consume resources without explicit user action.

The threat landscape has shifted significantly since 2024. Attackers now target AI infrastructure not just for disruption but for profit — stealing cloud credentials to resell LLM access (LLMjacking), crafting inputs that maximize compute cost (sponge examples, energy-latency attacks), and exploiting the high per-token cost of generative AI to inflict "denial of wallet" damage that can reach tens of thousands of dollars per day.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.6.1** | **Verify that** per-user, per-IP, per-API-key, and per-agent and per-session/task rate limits are enforced for all input and tool/MCP endpoints. | 1 | D/V | Denial of service via resource exhaustion ([MITRE ATLAS AML.T0029](https://atlas.mitre.org/)); brute-force prompt injection probing; automated scraping of model capabilities; cost-based attacks / LLMjacking (stolen credentials used to run up API bills — Sysdig documented $46K–$100K/day per compromised account in 2024); credential stuffing against AI endpoints. As of early 2026, Operation Bizarre Bazaar showed 60% of attack traffic targeting MCP endpoints specifically. | 1. Confirm rate limiting is implemented at the API gateway or application layer. 2. Test rate limits by exceeding them and verifying requests are throttled (HTTP 429). 3. Verify rate limits are enforced per: user identity, IP address, API key, agent ID, and session/task. 4. Confirm rate limits apply to all endpoints including tool/MCP endpoints (not just the main inference endpoint). 5. Check that rate limit responses include `Retry-After` headers. 6. Verify **token-based** rate limits exist alongside request-count limits — a single large request (200K tokens) can cost $4–$20, so request-count limits alone are insufficient. Tools: Kong AI Rate Limiting Advanced plugin reads actual token counts from provider responses; Envoy AI Gateway provides open-source token-based rate limiting; LiteLLM Proxy supports hierarchical `tpm_limit` and `rpm_limit` at global, team, user, key, model, and session levels. | Token-aware rate limiting is maturing fast but unevenly adopted. Kong and Envoy AI Gateway support true token counting from provider responses. Cloudflare AI Gateway, despite popularity, still only supports request-based (not token-based) rate limiting as of March 2026. LiteLLM Proxy (open-source) offers the most granular budget hierarchy: global proxy, per-team, per-user, per-key, per-model, per-agent, and per-session — but requires PostgreSQL and Redis for persistent tracking. Zuplo adds cost-weighted token counting that accounts for different model pricing tiers. For MCP endpoints specifically, no mature rate-limiting middleware exists yet — most implementations require custom application-layer enforcement. |
| **2.6.2** | **Verify that** burst and sustained rate limits are tuned to prevent DoS and brute force attacks, and that per-task budgets (for example tokens, tool/MCP calls, and cost) are enforced for agent planning loops. | 2 | D/V | Burst DoS attacks; slow-and-steady resource exhaustion ([MITRE ATLAS AML.T0034 — Cost Harvesting](https://atlas.mitre.org/)); unbounded agent execution (infinite planning loops); cost overruns from runaway agent tasks — a $47K LangChain multi-agent loop ran for 11 days before detection in November 2025; a separate $47K retry storm in February 2026 made 2.3M erroneous API calls in a single weekend; tool call amplification attacks. OWASP LLM10:2025 (Unbounded Consumption) documents resource-intensive query patterns causing 20–30x budget overruns. | 1. Review rate limit configuration for both burst (short window, e.g., 10 req/s) and sustained (longer window, e.g., 1000 req/hr) limits — use token bucket or sliding window algorithms. 2. For agent systems, verify per-task budgets exist: maximum tokens consumed, maximum tool/MCP calls, maximum cost (in dollars), and maximum execution time. 3. Test agent loop termination by creating a task that triggers recursive planning — verify it halts within budget. 4. Verify budget enforcement triggers graceful task termination with a status report, not a crash. 5. Verify agent frameworks enforce limits: LangChain/LangGraph `ModelCallLimitMiddleware` (caps model calls per thread/run), `ToolCallLimitMiddleware` (caps tool invocations globally or per specific tool), and `GraphRecursionError` for infinite graph loops; CrewAI `max_iter` (default 20), `max_execution_time`, `max_rpm`; OpenAI Assistants `max_turns`. | Agent budget enforcement is the least mature area. LangChain/LangGraph middleware (v1.0+) is the most feature-complete with distinct model-call and tool-call limit middleware and configurable exit behaviors (`'end'` for graceful, `'error'` for exception). CrewAI provides per-agent `max_iter`, `max_execution_time`, and `max_rpm` controls. AutoGen uses centralized transcript management with automatic pruning when token limits approach. However, cost-based budgets (actual dollar caps, not just call counts) remain rare in frameworks — most require custom integration with provider billing APIs or local token counting via LiteLLM. The $47K LangChain incident lacked step limits, stop conditions, cost ceilings, shared memory, and real-time monitoring — all of which are now addressable with middleware but require explicit configuration. |
| **2.6.3** | **Verify that** anomalous usage patterns (e.g., rapid-fire requests, input flooding, repetitive failing tool/MCP calls or recursive agent loops) trigger automated blocks or escalations. | 2 | D/V | Automated attack campaigns; systematic vulnerability probing; distributed attacks from multiple sources; low-and-slow attacks that stay under individual rate limits but are anomalous in aggregate; agent loop exploitation; energy-latency attacks — LoopLLM (AAAI 2026) demonstrated transferable attacks achieving 90%+ of maximum output length on 12 open-source LLMs and ~40% transferability to commercial APIs; ThinkTrap (December 2025) exploits extended-thinking features in Claude, Gemini, and GPT-4 to multiply cost and latency. | 1. Review anomaly detection rules for: request rate spikes, repeated validation failures from same source, repetitive identical or near-identical requests, high error rates from tool calls, recursive patterns in agent execution, and abnormally long output generation (energy-latency attack indicator). 2. Test with simulated anomalous patterns and verify automated response (block, CAPTCHA challenge, or escalation to SOC). 3. Verify automated blocks are time-limited (auto-expire) and can be manually overridden. 4. Confirm escalation path exists for human review. 5. Check for OWASP LLM10:2025's recommended four-stage defense: pre-ingress (WAF, IP reputation, CAPTCHA), gateway (per-tenant rate limiting, request cost estimation before processing), inference (max tokens, complexity scoring, per-request timeouts, streaming with early termination), post-inference (anomaly detection, automated budget kill-switches). | Anomaly detection goes beyond simple rate limiting — it requires behavioral analysis. Simple heuristics (>N failures in M minutes triggers block) are a good start. WAF-level AI protection is emerging: Cloudflare Firewall for AI provides prompt injection and jailbreak detection integrated with WAF; LLM Guard (Protect AI, open-source, 2.5M+ downloads) scans prompts and responses for injection, toxicity, PII, and secrets; Alibaba Cloud WAF 3.0 includes dedicated prompt injection protection rules. For agent loops, detecting recursive patterns (agent calls tool → result triggers same call) requires execution trace analysis. Energy-latency attacks (sponge examples, LoopLLM, ThinkTrap) are particularly challenging because each individual request looks legitimate — detection requires monitoring output length, latency, and token consumption per request relative to input complexity. |
| **2.6.4** | **Verify that** abuse prevention logs are retained and reviewed for emerging attack patterns, with trace metadata (source, tool or MCP server, agent ID, session). | 3 | V | Undetected evolving attack patterns; inability to perform post-incident analysis; failure to improve defenses based on real-world attack data; regulatory non-compliance — the EU AI Act Article 15 requires high-risk AI systems to maintain robustness and cybersecurity resilience (compliance deadline August 2026–2027), and ISO 42001 A.6.2.6 requires operational monitoring of AI systems. | 1. Confirm abuse prevention events (rate limit hits, anomaly detections, automated blocks) are logged with structured metadata. 2. Verify log retention meets organizational and regulatory requirements (typically 90 days to 1 year). 3. Confirm logs are reviewed periodically (automated dashboards and/or manual review cadence). 4. Verify logs include: event type, source IP/user/API key, agent ID, session ID, tool/MCP server, timestamp, action taken (throttle/block/escalate), and token/cost metadata. 5. Check integration with SIEM or security analytics platform. 6. Verify logs capture enough detail to identify LLMjacking patterns (credential reuse across providers, logging disabled, unusual model access patterns — Sysdig noted attackers called `DeleteModelInvocationLoggingConfiguration` within minutes of compromising AWS Bedrock accounts). | Level 3 because systematic log review and pattern analysis requires dedicated security operations resources. Logs should feed into a SIEM for automated pattern detection. Tools like Helicone provide cost-based observability with per-user segmentation and rate limiting by cost (e.g., "$5/hour per user"). LiteLLM Proxy tracks token/cost metrics at every organizational level. The MITRE SAFE-AI framework maps ATLAS threats (AML.T0029, AML.T0034) directly to NIST SP 800-53 controls, providing a bridge between AI-specific threat taxonomy and established security control frameworks for compliance mapping. Emerging attack pattern detection can use simple trend analysis or ML-based clustering of attack behaviors. |

---

## Notable Incidents

| Date | Incident | Impact | Relevance |
|------|----------|--------|-----------|
| May 2024 onwards | **LLMjacking Campaign** — attackers exploited CVE-2021-3129 (Laravel RCE) to steal cloud credentials, resold LLM access across 10 providers via OAI Reverse Proxy. Attackers probed accounts within 9–17 minutes of credential exposure and disabled logging. | $46K–$100K+/day per compromised account; attack volume grew 10x through H1 2024. | Demonstrates need for per-key rate limits, credential rotation, and logging tamper protection (2.6.1, 2.6.4). |
| Nov 2025 | **$47K LangChain Multi-Agent Loop** — four-agent research pipeline entered recursive conversation loop. Analyzer and Verifier agents ping-ponged ambiguous requests for 11 days. No step limits, cost ceilings, or monitoring. | $47,000 in API charges, discovered only via monthly invoice review. | Core motivation for per-task budgets and agent loop detection (2.6.2, 2.6.3). |
| Dec 2025 – Jan 2026 | **Operation Bizarre Bazaar** — first attributed LLMjacking campaign with commercial marketplace. Threat actor operated unified API gateway reselling access to 30+ unauthorized LLM providers. 60% of attack traffic targeted MCP endpoints. | 35,000 attack sessions captured; ~972 daily attacks. | Shows MCP endpoints are high-value targets requiring rate limiting (2.6.1). |
| Dec 2025 | **ThinkTrap** — DoS attack exploiting extended-thinking features in Claude, Gemini, GPT-4. Crafted prompts trigger excessive internal reasoning iterations. | Significant latency increase and cost multiplication against production thinking-enabled LLM services. | Novel attack vector requiring output-length and latency anomaly detection (2.6.3). |
| Feb 2026 | **$47K Retry Storm** — data enrichment agent misinterpreted API error code as "try again with different parameters," running 2.3M API calls over a weekend. | ~$47,000 in unplanned API costs. | Shows error-handling logic can create unbounded consumption without explicit loops (2.6.2). |
| 2025–2026 | **Fortune 500 Agentic Resource Exhaustion** — enterprises deploying autonomous AI agents collectively experienced massive unbudgeted cloud spend from semantic infinite loops and recursive reasoning cycles. | $400M aggregate unbudgeted spend across Fortune 500; created "AI FinOps" as a new discipline. | System-wide evidence that per-task budget enforcement is not optional (2.6.2). |

---

## Implementation Maturity

| Area | Maturity | Notes |
|------|----------|-------|
| Request-count rate limiting | **High** | Standard API gateway feature (Kong, AWS API Gateway, Nginx, Cloudflare). Well-understood algorithms (token bucket, sliding window). |
| Token-aware rate limiting | **Medium** | Kong AI Rate Limiting Advanced, Envoy AI Gateway, LiteLLM Proxy, and Zuplo support token counting. Cloudflare AI Gateway does not yet. Requires reading token metadata from provider responses. |
| Agent per-task budgets | **Low–Medium** | LangChain/LangGraph middleware, CrewAI limits, and OpenAI `max_turns` exist but require explicit configuration. Cost-based budgets (actual dollar caps) remain rare and require custom integration. |
| Energy-latency attack detection | **Low** | Sponge examples, LoopLLM, and ThinkTrap are documented in research but no production-ready detection tools exist. Requires correlating input complexity with output length and latency. |
| MCP endpoint rate limiting | **Low** | No mature middleware exists. Requires custom application-layer enforcement. Operation Bizarre Bazaar showed these endpoints are actively targeted. |
| AI-specific WAF rules | **Medium** | Cloudflare Firewall for AI, LLM Guard (open-source), and Alibaba Cloud WAF 3.0 provide prompt injection and jailbreak detection. Not yet integrated with rate limiting decisions. |

---

## Related Standards & References

- [MITRE ATLAS AML.T0029 — Denial of ML Service](https://atlas.mitre.org/)
- [MITRE ATLAS AML.T0034 — Cost Harvesting](https://atlas.mitre.org/)
- [OWASP LLM10:2025 — Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
- [OWASP API Security Top 10 — API4: Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP Rate Limiting Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Rate_Limiting_Cheat_Sheet.html)
- [NIST SP 800-53 SC-5: Denial of Service Protection](https://csf.tools/reference/nist-sp-800-53/r5/sc/sc-5/)
- [NIST AI RMF 100-1 — Secure and Resilient Characteristic](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act Article 15 — Accuracy, Robustness and Cybersecurity](https://artificialintelligenceact.eu/article/15/)
- [ISO/IEC 42001:2023 — A.4 Resources for AI Systems, A.6.2.6 Operation and Monitoring](https://www.iso.org/standard/42001)
- [MITRE SAFE-AI Framework — ATLAS to NIST SP 800-53 Mapping](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf)
- [OpenAI Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Anthropic Rate Limits](https://docs.anthropic.com/en/api/rate-limits)
- [Sysdig — LLMjacking: Stolen Cloud Credentials Used in New AI Attack (2024)](https://www.sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack)
- [Pillar Security — Operation Bizarre Bazaar (2026)](https://www.pillar.security/blog/operation-bizarre-bazaar-first-attributed-llmjacking-campaign-with-commercial-marketplace-monetization)
- [LoopLLM: Transferable Energy-Latency Attacks (AAAI 2026)](https://arxiv.org/abs/2511.07876)
- [ThinkTrap: DoS Against LLM Thinking Services (2025)](https://arxiv.org/abs/2512.07086)
- [Sponge Examples: Energy-Latency Attacks on Neural Networks (2021)](https://arxiv.org/abs/2006.03463)
- [Kong AI Rate Limiting Advanced Plugin](https://developer.konghq.com/plugins/ai-rate-limiting-advanced/)
- [LiteLLM Proxy — Budgets & Rate Limits](https://docs.litellm.ai/docs/proxy/users)
- [LangChain Prebuilt Middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [LLM Guard (Protect AI) — Open Source LLM Security](https://protectai.com/llm-guard)

---

## Cross-Chapter Links

| Related Section | Overlap |
|----------------|---------|
| [C04-03 Network Security & Access Control](C04-03-Network-Security-Access-Control) | Network-layer DoS protection, WAF integration |
| [C09-01 Execution Budgets](C09-01-Execution-Budgets) | Agent per-task budget enforcement, loop termination |
| [C09-03 Tool and Plugin Isolation](C09-03-Tool-and-Plugin-Isolation) | Tool call rate limiting, MCP endpoint protection |
| [C10-04 Schema & Message Validation](C10-04-Schema-Message-Validation) | MCP message validation as pre-rate-limiting filter |
| [C13-01 Request-Response Logging](C13-01-Request-Response-Logging) | Abuse log structure and retention requirements |
| [C13-02 Abuse Detection & Alerting](C13-02-Abuse-Detection-Alerting) | Anomaly detection rules, SIEM integration |
| [C05 Access Control](C05-Access-Control) | Per-user and per-API-key authentication underpinning rate limit identity |

---

## Open Research Questions

- What are appropriate rate limits for AI inference endpoints given the high per-request cost compared to traditional APIs? OWASP LLM10:2025 suggests request cost estimation before processing — how practical is this at scale?
- How should per-task budgets be set for autonomous agents where the number of steps needed is unpredictable? The $47K LangChain incident suggests fixed caps are necessary, but overly tight caps may prevent legitimate complex tasks from completing.
- Can rate limiting be made adaptive (automatically tightening under attack) without causing false positives for legitimate burst traffic? Back-pressure queuing with dynamic concurrency adjustment is one approach, but production implementations are scarce.
- How should rate limiting account for token cost variation across different models and providers? Cost-weighted token counting (as implemented by Zuplo) is promising but adds complexity.
- How can energy-latency attacks (sponge examples, LoopLLM, ThinkTrap) be detected in real time? These attacks use legitimate-looking requests that maximize compute cost — detection may require correlating input complexity with output length and latency baselines.
- As MCP adoption grows, what rate-limiting patterns should emerge for tool-calling endpoints? Operation Bizarre Bazaar showed 60% of attacks targeting MCP — dedicated middleware is needed but doesn't exist yet.

---
