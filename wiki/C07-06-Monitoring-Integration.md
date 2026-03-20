# C7.6 Monitoring Integration

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Monitoring integration ensures that the safety and security controls defined throughout C7 produce observable signals that security teams can act on. Without integrated monitoring, safety violations (hallucinations, PII leaks, toxic outputs, filter bypasses) occur silently. This section requires real-time metrics, alerting on anomalous patterns, and sufficient log detail to support incident investigation. These controls bridge the gap between per-request safety checks and organizational security operations.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.6.1** | **Verify that** the system logs real-time metrics for safety violations (e.g., "Hallucination Detected", "PII Blocked"). | 1 | D | **Invisible safety failures.** Without real-time metrics, security teams have no visibility into whether safety controls are working, how often they trigger, or whether attack patterns are emerging. A safety filter that triggers 1000 times per hour might indicate a coordinated attack — but without metrics, no one knows. | Trigger various safety violation types (format rejection, hallucination detection, PII redaction, content filter block) and confirm each produces a corresponding metric entry. Verify metrics are available in near-real-time (within seconds, not batch-processed daily). Confirm metrics include event type, timestamp, and severity. | Standard observability stacks (Prometheus/Grafana, Datadog, Splunk, ELK) can ingest these metrics. AI-specific platforms (LangSmith, Weights & Biases, Arize AI, WhyLabs) provide specialized dashboards for model behavior monitoring. The key requirement is that all safety events from C7.1-C7.5 and C7.7-C7.8 emit structured metrics. |
| **7.6.2** | **Verify that** the system triggers an alert if safety violation rates exceed a defined threshold within a specific time window. | 2 | D/V | **Undetected attack campaigns.** Individual safety violations may be benign (a user accidentally triggering a filter). But a spike in violations — especially from a single user, IP range, or targeting a specific filter — likely indicates an active attack (prompt injection campaign, PII extraction attempt, jailbreak effort). Without rate-based alerting, these campaigns go unnoticed. | Configure alert thresholds (e.g., >50 PII redactions per hour, >20 content filter blocks per user per hour). Simulate a burst of safety violations exceeding the threshold. Verify an alert is generated and delivered to the appropriate channel (PagerDuty, Slack, email, SIEM). Confirm alert includes sufficient context for triage (violation type, user ID, time window, count). | Threshold tuning is critical. Too low produces alert fatigue; too high misses real attacks. Consider adaptive thresholds that adjust based on baseline violation rates. Correlating violation spikes with specific user sessions or IP addresses supports rapid incident response. |
| **7.6.3** | **Verify that** logs include the specific model version and other details necessary to investigate potential abuse. | 2 | V | **Inability to reproduce or investigate incidents.** If a safety incident occurs but logs do not record which model version, prompt template, or configuration was active, investigators cannot determine whether the issue was a model-level problem, a configuration error, or an adversarial attack. This is especially critical when models are frequently updated. | Review log entries for safety events and confirm they include: model version/identifier, prompt template version (if applicable), inference parameters (temperature, top_p, etc.), timestamp, request ID, and user/session identifier. Verify logs are retained for sufficient duration to support investigations (per organizational policy). | Model version tracking becomes essential in environments with frequent model updates (A/B testing, canary deployments, fine-tune iterations). Without version-tagged logs, a spike in hallucinations after a model update cannot be attributed to the update. Relates to C3 (Model Lifecycle Management) for version tracking. |

---

## Implementation Guidance (2025-2026 Landscape)

### LLM Observability Platform Landscape

The LLM observability market has matured rapidly through 2025-2026. The following platforms represent the current state of the art for monitoring AI model behavior and safety signals:

**Open-Source / Self-Hostable:**

- **Langfuse**: The most widely adopted open-source LLM observability tool (MIT licensed). Provides comprehensive tracing, evaluations, prompt management, and metrics. Generous free tier (50K events/month in cloud); self-hosting available for data sovereignty. Works with any LLM provider.
- **Arize Phoenix**: OpenTelemetry-native platform with LLM-based evaluators and code-based metrics. Avoids vendor lock-in through the OTLP protocol. Local development is free; Phoenix Cloud available for production.
- **TruLens**: Specialized for RAG evaluation (groundedness, context relevance, answer quality). Open source with no external service dependency.
- **OpenLLMetry** (Traceloop): OpenTelemetry-based instrumentation that integrates with existing APM stacks (Datadog, Honeycomb, Grafana, New Relic).

**Commercial / SaaS:**

- **LangSmith**: Best for LangChain/LangGraph users with automatic integration. Virtually no measurable overhead, making it suitable for performance-critical production. Free tier (5,000 traces/month); Plus at $39/user/month.
- **Datadog LLM Observability**: Auto-instruments OpenAI, LangChain, AWS Bedrock, and Anthropic calls, capturing latency, token usage, and errors without code changes. Built-in evaluations detect hallucinations and failed responses. **Security scanners flag prompt injection attempts and prevent data leaks.** Added "LLM Experiments" in 2025 for testing before deployment. Pricing: $8 per 10K requests.
- **New Relic AI Monitoring**: Service maps for interconnected agents, AI Trace View, 50+ integrations. Seeing 30% quarter-over-quarter adoption increase. Consumption-based pricing.
- **Galileo AI**: Real-time guardrails with Luna-2 evaluation models at approximately 200ms latency and approximately $0.02 per million tokens. Can intercept risky agent actions before execution.
- **Helicone**: Gateway/proxy approach with unified billing across 100+ models. Gets logging running in minutes with a single header change.
- **Portkey**: 250+ model support with automatic fallbacks, load balancing, and semantic caching. 20-40ms overhead. ISO 27001, SOC 2, GDPR, HIPAA certified.

### Choosing a Monitoring Stack

Team size and existing infrastructure should drive selection:

- **Solo/small teams**: Start with Helicone (minimal setup) or Langfuse (full observability with free tier).
- **LangChain users**: LangSmith provides the deepest integration.
- **Enterprise teams already on Datadog/New Relic**: Add their LLM monitoring modules rather than introducing a new vendor.
- **Data sovereignty requirements**: Deploy Langfuse or Phoenix self-hosted.

### Critical Metrics to Track

Start with cost and latency (easy, immediately actionable), then error rates. Progress to quality metrics (hallucination detection, relevance scoring) once baseline visibility is established. All safety events from C7.1-C7.5 and C7.7-C7.8 should emit structured metrics into the observability pipeline.

### Alert Threshold Design

Threshold tuning is critical for C7.6.2 compliance. Too low produces alert fatigue; too high misses real attacks. Consider:

- **Adaptive thresholds** that adjust based on baseline violation rates rather than static thresholds.
- **Correlation-based alerting**: Correlate violation spikes with specific user sessions or IP addresses for rapid incident response.
- **Multi-signal alerting**: Combine safety violation rates with anomalous token usage patterns, unusual tool invocation sequences, or geographic access anomalies.

---

## Related Standards & References

- AISVS C13 (Monitoring & Logging) — general monitoring and logging requirements; C7.6 provides AI-specific monitoring signals that feed into C13 infrastructure
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — general logging best practices applicable to AI monitoring
- [LangSmith (LangChain)](https://smith.langchain.com/) — LLM application tracing and monitoring
- [Arize AI](https://arize.com/) — ML observability platform with LLM monitoring
- [WhyLabs](https://whylabs.ai/) — AI observability with drift and anomaly detection
- [Langfuse](https://langfuse.com/docs/security-and-guardrails) — open-source LLM observability with security and guardrails integration
- [Datadog LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/) — deployment guidance for monitored LLM safety
- [Best LLM Observability Tools in 2026 (Firecrawl)](https://www.firecrawl.dev/blog/best-llm-observability-tools) — comprehensive 2026 tool comparison
- [Top AI Agent Observability Platforms 2026 (AIMultiple)](https://research.aimultiple.com/agentic-monitoring/) — agentic AI monitoring landscape
- [Galileo AI](https://www.galileo.ai/) — real-time guardrails with low-latency evaluation models
- [Portkey](https://portkey.ai/) — AI gateway with observability, compliance certifications (SOC 2, HIPAA)

---

## Open Research Questions

- What are the right baseline metrics and alert thresholds for AI safety monitoring? Are there industry benchmarks emerging?
- How should monitoring handle multi-model pipelines where a single user request traverses multiple models -- should safety metrics be attributed to the pipeline or individual models?
- How can monitoring systems distinguish between adversarial attacks and legitimate edge-case usage that happens to trigger safety filters?
- As the observability market consolidates, will OpenTelemetry (OTLP) become the standard protocol for AI-specific telemetry, or will proprietary instrumentation formats persist?
- How should monitoring costs be managed at scale? With platforms charging per-request or per-trace, high-throughput AI applications may face significant observability overhead.
- What role should real-time guardrail evaluation (e.g., Galileo's 200ms interception) play versus post-hoc monitoring -- should safety enforcement and observability be unified or separated?

---
