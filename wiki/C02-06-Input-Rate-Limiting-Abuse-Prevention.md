# C2.6 Input Rate Limiting & Abuse Prevention

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation)

## Purpose

AI systems are expensive to operate (each inference consumes GPU resources and incurs API costs) and are attractive targets for denial-of-service attacks, brute-force prompt injection attempts, and automated abuse. Rate limiting and abuse detection prevent resource exhaustion, budget overruns, and systematic probing. In agentic architectures, additional controls are needed to prevent runaway planning loops and unbounded tool call chains that can consume resources without explicit user action.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.6.1** | **Verify that** per-user, per-IP, per-API-key, and per-agent and per-session/task rate limits are enforced for all input and tool/MCP endpoints. | 1 | D/V | Denial of service (resource exhaustion); brute-force prompt injection probing; automated scraping of model capabilities; cost-based attacks (running up API bills); credential stuffing against AI endpoints. | 1. Confirm rate limiting is implemented at the API gateway or application layer. 2. Test rate limits by exceeding them and verifying requests are throttled (HTTP 429). 3. Verify rate limits are enforced per: user identity, IP address, API key, agent ID, and session/task. 4. Confirm rate limits apply to all endpoints including tool/MCP endpoints (not just the main inference endpoint). 5. Check that rate limit responses include Retry-After headers. | Standard API gateway rate limiting (Kong, AWS API Gateway, Nginx, Cloudflare) provides per-IP and per-API-key limits. Per-user and per-agent limits require application-layer enforcement. For AI systems, rate limits should consider token consumption in addition to request count -- a single large request can be more expensive than many small ones. Token-based rate limiting (tokens per minute) is supported by OpenAI and Anthropic APIs natively. |
| **2.6.2** | **Verify that** burst and sustained rate limits are tuned to prevent DoS and brute force attacks, and that per-task budgets (for example tokens, tool/MCP calls, and cost) are enforced for agent planning loops. | 2 | D/V | Burst DoS attacks; slow-and-steady resource exhaustion; unbounded agent execution (infinite planning loops); cost overruns from runaway agent tasks; tool call amplification attacks. | 1. Review rate limit configuration for both burst (short window, e.g., 10 requests/second) and sustained (longer window, e.g., 1000 requests/hour) limits. 2. For agent systems, verify per-task budgets exist: maximum tokens consumed, maximum tool/MCP calls, maximum cost (in dollars). 3. Test agent loop termination by creating a task that triggers recursive planning. 4. Verify budget enforcement triggers graceful task termination with a status report, not a crash. | Burst + sustained rate limiting (token bucket or sliding window) is standard practice. The agent-specific requirement (per-task budgets) is less standard and requires purpose-built instrumentation. Frameworks like LangChain, AutoGPT, and CrewAI are beginning to add budget controls but implementations vary. Cost tracking requires integration with provider billing APIs or local token counting. The key risk is an agent that enters an infinite loop of tool calls -- each call may be within per-request limits but the aggregate is unbounded. |
| **2.6.3** | **Verify that** anomalous usage patterns (e.g., rapid-fire requests, input flooding, repetitive failing tool/MCP calls or recursive agent loops) trigger automated blocks or escalations. | 2 | D/V | Automated attack campaigns; systematic vulnerability probing; distributed attacks from multiple sources; low-and-slow attacks that stay under individual rate limits but are anomalous in aggregate; agent loop exploitation. | 1. Review anomaly detection rules for: request rate spikes, repeated validation failures from same source, repetitive identical or near-identical requests, high error rates from tool calls, recursive patterns in agent execution. 2. Test with simulated anomalous patterns and verify automated response (block, CAPTCHA challenge, or escalation to SOC). 3. Verify that automated blocks are time-limited (auto-expire) and can be manually overridden. 4. Confirm escalation path exists for human review of blocked users. | Anomaly detection goes beyond simple rate limiting -- it requires behavioral analysis. Simple heuristics (e.g., >N failures in M minutes triggers block) are a good start. More sophisticated approaches use ML-based anomaly detection on request patterns. The challenge is distinguishing legitimate heavy usage from attacks, especially for API customers with variable workloads. Integration with WAF (Web Application Firewall) rules and SIEM alerting is recommended. For agent loops, detecting recursive patterns (agent calls tool, tool result triggers same tool call) requires execution trace analysis. |
| **2.6.4** | **Verify that** abuse prevention logs are retained and reviewed for emerging attack patterns, with trace metadata (source, tool or MCP server, agent ID, session). | 3 | V | Undetected evolving attack patterns; inability to perform post-incident analysis; failure to improve defenses based on real-world attack data; regulatory non-compliance with log retention requirements. | 1. Confirm abuse prevention events (rate limit hits, anomaly detections, automated blocks) are logged with structured metadata. 2. Verify log retention meets organizational and regulatory requirements (typically 90 days to 1 year). 3. Confirm logs are reviewed periodically (automated dashboards and/or manual review cadence). 4. Verify logs include: event type, source IP/user/API key, agent ID, session ID, tool/MCP server, timestamp, action taken (throttle/block/escalate). | Level 3 because systematic log review and pattern analysis requires dedicated security operations resources. Logs should feed into a SIEM or security analytics platform for automated pattern detection. Emerging attack pattern detection can use simple trend analysis (increasing rate of blocks from a source) or ML-based clustering of attack behaviors. Retention policies must balance storage costs with forensic value and regulatory requirements. |

---

## Related Standards & References

- [OWASP API Security Top 10 -- API4: Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP Rate Limiting Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Rate_Limiting_Cheat_Sheet.html)
- [NIST SP 800-53 SC-5: Denial of Service Protection](https://csf.tools/reference/nist-sp-800-53/r5/sc/sc-5/)
- [OpenAI Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Anthropic Rate Limits](https://docs.anthropic.com/en/api/rate-limits)

---

## Open Research Questions

- What are appropriate rate limits for AI inference endpoints given the high per-request cost compared to traditional APIs?
- How should per-task budgets be set for autonomous agents where the number of steps needed is unpredictable?
- Can rate limiting be made adaptive (automatically tightening under attack) without causing false positives for legitimate burst traffic?
- How should rate limiting account for token cost variation across different models and providers?

---
