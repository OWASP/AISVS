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

## Related Standards & References

- AISVS C13 (Monitoring & Logging) — general monitoring and logging requirements; C7.6 provides AI-specific monitoring signals that feed into C13 infrastructure
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — general logging best practices applicable to AI monitoring
- [LangSmith (LangChain)](https://smith.langchain.com/) — LLM application tracing and monitoring
- [Arize AI](https://arize.com/) — ML observability platform with LLM monitoring
- [WhyLabs](https://whylabs.ai/) — AI observability with drift and anomaly detection

---

## Open Research Questions

- What are the right baseline metrics and alert thresholds for AI safety monitoring? Are there industry benchmarks emerging?
- How should monitoring handle multi-model pipelines where a single user request traverses multiple models — should safety metrics be attributed to the pipeline or individual models?
- How can monitoring systems distinguish between adversarial attacks and legitimate edge-case usage that happens to trigger safety filters?

---
