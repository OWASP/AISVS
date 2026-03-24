# C7.6 Monitoring Integration

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Monitoring integration ensures that the safety and security controls defined throughout C7 produce observable signals that security teams can act on. Without integrated monitoring, safety violations (hallucinations, PII leaks, toxic outputs, filter bypasses) occur silently. This section requires real-time metrics, alerting on anomalous patterns, and sufficient log detail to support incident investigation. These controls bridge the gap between per-request safety checks and organizational security operations.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.6.1** | **Verify that** the system logs real-time metrics for safety violations (e.g., "Hallucination Detected", "PII Blocked"). | 1 | D | **Invisible safety failures (MITRE ATLAS AML.T0015 — Evade ML Model).** Without real-time metrics, security teams have no visibility into whether safety controls are working, how often they trigger, or whether attack patterns are emerging. A safety filter that triggers 1000 times per hour might indicate a coordinated attack — but without metrics, no one knows. GreyNoise research documented 91,000+ attack sessions targeting exposed LLM services between October 2025 and January 2026, underscoring the volume of attacks that go unnoticed without proper metrics. Adversaries specifically craft inputs to evade safety filters silently, making metric emission from every filter stage essential. | Trigger various safety violation types (format rejection, hallucination detection, PII redaction, content filter block) and confirm each produces a corresponding metric entry. Verify metrics are available in near-real-time (within seconds, not batch-processed daily). Confirm metrics include event type, timestamp, and severity. Use OpenTelemetry-based instrumentation (OpenLLMetry, SigNoz) to verify metrics flow into the observability pipeline. Confirm safety events from C7.1-C7.5 and C7.7-C7.8 all emit structured metrics. Cross-reference with Confident AI's production safety evaluators (toxicity, bias, PII detection) or Comet Opik's guardrail PII redaction logs to validate coverage. | Standard observability stacks (Prometheus/Grafana, Datadog, Splunk, ELK) can ingest these metrics. AI-specific platforms like Langfuse (open-source, OpenTelemetry-native), Arize Phoenix, and LangSmith provide specialized dashboards for model behavior monitoring. As of March 2026, Confident AI offers 50+ evaluation metrics (open-sourced through DeepEval) and is used at scale by major providers. SigNoz provides OpenTelemetry-native full-stack observability with trace-to-log correlation. The gap remains that no single platform combines comprehensive safety guardrails with OpenTelemetry-native design at an accessible price point — most teams layer safety-specific tools on top of general tracing infrastructure. |
| **7.6.2** | **Verify that** the system triggers an alert if safety violation rates exceed a defined threshold within a specific time window. | 2 | D/V | **Undetected attack campaigns (OWASP LLM Top 10 2025 — LLM01: Prompt Injection).** Individual safety violations may be benign (a user accidentally triggering a filter). But a spike in violations — especially from a single user, IP range, or targeting a specific filter — likely indicates an active attack (prompt injection campaign, PII extraction attempt, jailbreak effort). A late-2025 case involving ServiceNow's AI assistant demonstrated "second-order" prompt injection where a low-privilege agent was tricked into escalating via a higher-privilege agent — these cross-agent attack chains produce characteristic violation patterns that rate-based alerting can catch. Without rate-based alerting, coordinated campaigns go unnoticed. | Configure alert thresholds (e.g., >50 PII redactions per hour, >20 content filter blocks per user per hour, >200 API calls/minute, error rate ≥5%). Simulate a burst of safety violations exceeding the threshold. Verify an alert is generated and delivered to the appropriate channel (PagerDuty, Slack, email, SIEM). Confirm alert includes sufficient context for triage (violation type, user ID, time window, count). Test with CrowdStrike Falcon AIDR (reports 98.7% prompt injection detection rate as of early 2026) or signature-based log scanners that flag patterns like "ignore previous instructions" and "disregard all rules." Validate that multi-signal correlation works — e.g., violation spike + anomalous token usage + unusual tool invocation sequence triggers a higher-severity alert than any single signal alone. | Threshold tuning is critical. Too low produces alert fatigue; too high misses real attacks. Practical thresholds from production deployments (as of 2026): API call frequency >200 calls/minute, error rate ≥5%, failed login attempts ≥20/hour, log volume >1 GB/hour. Consider adaptive thresholds that adjust based on baseline violation rates. Correlating violation spikes with specific user sessions or IP addresses supports rapid incident response. Anomaly detection models tracking unexpected shifts in output patterns (e.g., sudden spikes in prompt complexity, repeated requests for sensitive topics, excessive tool calls, or data access immediately followed by external HTTP requests) provide stronger signal than static thresholds alone. |
| **7.6.3** | **Verify that** logs include the specific model version and other details necessary to investigate potential abuse. | 2 | V | **Inability to reproduce or investigate incidents (NIST AI RMF "Measure" function — traceability).** If a safety incident occurs but logs do not record which model version, prompt template, or configuration was active, investigators cannot determine whether the issue was a model-level problem, a configuration error, or an adversarial attack. This is especially critical when models are frequently updated. Shadow AI — GenAI tools accessed via personal, unmanaged accounts — represents a major blind spot: as of 2026, 47% of GenAI users access tools via personal accounts, bypassing enterprise logging entirely. Without version-tagged logs, organizations cannot show the audit trail linking outputs to source data, model versions, and user prompts that NIST expects. | Review log entries for safety events and confirm they include: model version/identifier, prompt template version (if applicable), inference parameters (temperature, top_p, etc.), timestamp, request ID, and user/session identifier. Verify logs are retained for sufficient duration to support investigations (per organizational policy). Use centralized log analysis (Elasticsearch 9.3/Kibana 9.3, Loki 3.6.6 with OpenTelemetry integration, or SigNoz for 2.5x faster ingestion) to correlate safety events across model versions. Confirm that Langfuse session replays or LangSmith trace views can reconstruct the full request context for any flagged safety event. | Model version tracking becomes essential in environments with frequent model updates (A/B testing, canary deployments, fine-tune iterations). Without version-tagged logs, a spike in hallucinations after a model update cannot be attributed to the update. Relates to C3 (Model Lifecycle Management) for version tracking. NIST IR 8596 (Cybersecurity Framework Profile for AI, 2025) emphasizes logging that links outputs to source data and model versions. Key metrics to track per NIST guidance: mean time to detect (MTTD) for AI-specific threats, percentage of models covered by security controls, adversarial test coverage, and incident response times. |

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
- **Confident AI**: Eval-driven alerting with 50+ metrics open-sourced through DeepEval. Includes production safety evaluators for toxicity, bias, and PII detection. Red teaming functionality covers prompt injection, bias, and jailbreaks aligned with OWASP and NIST frameworks. Pricing: $1/GB-month data + $19.99/seat.
- **New Relic AI Monitoring**: Service maps for interconnected agents, AI Trace View, 50+ integrations. Seeing 30% quarter-over-quarter adoption increase. Consumption-based pricing.
- **Galileo AI**: Real-time guardrails with Luna-2 evaluation models at approximately 200ms latency and approximately $0.02 per million tokens. Can intercept risky agent actions before execution.
- **Helicone**: Gateway/proxy approach with unified billing across 100+ models. Gets logging running in minutes with a single header change.
- **Portkey**: 250+ model support with automatic fallbacks, load balancing, and semantic caching. 20-40ms overhead. ISO 27001, SOC 2, GDPR, HIPAA certified.
- **CrowdStrike Falcon AIDR**: Continuous threat detection across user-AI interactions, reportedly achieving 98.7% success rate in identifying prompt injection attempts without impacting task performance.

**Log Analysis & Centralized Monitoring:**

- **Elasticsearch 9.3 / Kibana 9.3**: Advanced visualization and structured metadata support for AI safety logs. Configure Logstash to filter suspicious keywords and extract relevant fields (user input, timestamps, responses).
- **Loki 3.6.6**: Lightweight log aggregation with OpenTelemetry integration — good for teams already invested in the Grafana ecosystem.
- **SigNoz**: OpenTelemetry-native one-stop observability with reportedly 2.5x faster real-time ingestion than Elasticsearch and built-in anomaly detection.

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

Production-tested alert triggers (as of early 2026):

| Metric | Recommended Alert Trigger |
|--------|--------------------------|
| API call frequency | >200 calls/minute per user/session |
| Safety filter error rate | ≥5% of requests |
| Failed auth attempts | ≥20 per hour per source |
| Log volume anomaly | >1 GB/hour (baseline-adjusted) |
| PII redaction spike | >50 redactions/hour (or 3x baseline) |
| Content filter blocks | >20 blocks per user per hour |

### Log-Based Injection Detection

Beyond rate-based alerting, log analysis can catch sophisticated attacks through behavioral patterns. Key signals that indicate active prompt injection or abuse:

- **Excessive tool calls**: An unusually high number of tool invocations within a single conversation suggests an injected payload directing the model to take unauthorized actions.
- **Data access followed by external requests**: A sequence where the model accesses internal data and then immediately attempts an external HTTP request is a strong indicator of data exfiltration via indirect prompt injection.
- **Unusually long responses**: Output length anomalies often correlate with jailbreak success — the model producing content it would normally refuse.
- **Late-introduced tools**: New tools appearing deep in a conversation (rather than at the start) suggest injection payloads manipulating the agent's available tool set.
- **Signature patterns**: Regex-based scanners that flag known attack strings ("ignore previous instructions", "disregard all rules", role-play manipulation phrases) provide a fast first layer. Production implementations typically assign risk scores (0.3 threshold for low, up to 0.85 for critical) and route high-risk inputs for additional review.

---

## Related Standards & References

- AISVS C13 (Monitoring & Logging) — general monitoring and logging requirements; C7.6 provides AI-specific monitoring signals that feed into C13 infrastructure
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — general logging best practices applicable to AI monitoring
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial threat landscape for AI systems; AML.T0015 (Evade ML Model) directly relevant to monitoring bypass
- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) — governance framework with "Measure" function requiring baseline metrics for drift, bias, and adversarial robustness
- [NIST IR 8596 — Cybersecurity Framework Profile for AI (2025)](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8596.iprd.pdf) — logging requirements linking outputs to source data, model versions, and user prompts
- [LangSmith (LangChain)](https://smith.langchain.com/) — LLM application tracing and monitoring
- [Arize AI / Phoenix](https://arize.com/) — ML observability platform with LLM monitoring and drift detection via visual embeddings
- [WhyLabs](https://whylabs.ai/) — AI observability with drift and anomaly detection
- [Langfuse](https://langfuse.com/docs/security-and-guardrails) — open-source LLM observability with security and guardrails integration (OpenTelemetry-native)
- [Confident AI / DeepEval](https://www.confident-ai.com/) — 50+ open-source evaluation metrics, production safety evaluators, red teaming aligned with OWASP and NIST
- [SigNoz](https://signoz.io/) — OpenTelemetry-native full-stack observability with LLM monitoring and anomaly detection
- [OpenLLMetry (Traceloop)](https://www.traceloop.com/openllmetry) — vendor-neutral OpenTelemetry-based LLM instrumentation
- [Comet Opik](https://www.comet.com/site/products/opik/) — open-source LLM evaluation with PII redaction guardrails and hallucination detection
- [Datadog LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/) — deployment guidance for monitored LLM safety
- [Best LLM Observability Tools in 2026 (Firecrawl)](https://www.firecrawl.dev/blog/best-llm-observability-tools) — comprehensive 2026 tool comparison
- [Top LLM Observability Tools 2026 (SigNoz)](https://signoz.io/comparisons/llm-observability-tools/) — tool comparison with OpenTelemetry focus
- [Top AI Agent Observability Platforms 2026 (AIMultiple)](https://research.aimultiple.com/agentic-monitoring/) — agentic AI monitoring landscape
- [Detecting Prompt Injection Attacks in Logs (2026)](https://dasroot.net/posts/2026/02/detecting-prompt-injection-attacks-logs/) — log analysis patterns, thresholds, and tooling for injection detection
- [GreyNoise LLM Threat Research](https://www.greynoise.io/) — documented 91,000+ attack sessions targeting exposed LLM services (Oct 2025 – Jan 2026)
- [Galileo AI](https://www.galileo.ai/) — real-time guardrails with low-latency evaluation models
- [Portkey](https://portkey.ai/) — AI gateway with observability, compliance certifications (SOC 2, HIPAA)
- [CrowdStrike Falcon AIDR](https://www.crowdstrike.com/) — AI-driven threat detection with 98.7% prompt injection identification rate

---

## Real-World Incidents & Lessons

- **GreyNoise LLM Attack Telemetry (Oct 2025 – Jan 2026):** GreyNoise research documented over 91,000 attack sessions targeting exposed LLM services during this period. The sheer volume highlights why real-time metrics (7.6.1) and rate-based alerting (7.6.2) are non-negotiable — without them, tens of thousands of attack attempts go undetected.
- **ServiceNow Second-Order Prompt Injection (Late 2025):** Attackers discovered a cross-agent escalation path where a low-privilege AI agent was tricked into asking a higher-privilege agent to perform unauthorized actions. This "second-order" injection bypassed usual checks and would only be visible through comprehensive cross-agent logging with model version and session tracking (7.6.3).
- **Shadow AI Data Leaks (Samsung, JPMorgan, Goldman Sachs):** Samsung engineers leaked confidential source code by pasting it into ChatGPT, and multiple Wall Street banks restricted ChatGPT after employees shared sensitive information. These incidents illustrate why monitoring must cover not just sanctioned AI systems but also detect unauthorized AI tool usage. As of 2026, 47% of GenAI users access tools via personal accounts, completely bypassing enterprise monitoring.
- **72% Surge in AI-Assisted Attacks (2025):** Industry reports documented a 72% increase in AI-assisted cyber attacks during 2025, with attackers increasingly using adversarial perturbation techniques (MITRE ATLAS AML.T0015) to craft inputs that evade safety filters without triggering alerts. This trend makes behavioral anomaly detection (not just signature matching) essential for monitoring integration.

---

## Open Research Questions

- What are the right baseline metrics and alert thresholds for AI safety monitoring? Are there industry benchmarks emerging?
- How should monitoring handle multi-model pipelines where a single user request traverses multiple models -- should safety metrics be attributed to the pipeline or individual models?
- How can monitoring systems distinguish between adversarial attacks and legitimate edge-case usage that happens to trigger safety filters?
- As the observability market consolidates, will OpenTelemetry (OTLP) become the standard protocol for AI-specific telemetry, or will proprietary instrumentation formats persist?
- How should monitoring costs be managed at scale? With platforms charging per-request or per-trace, high-throughput AI applications may face significant observability overhead.
- What role should real-time guardrail evaluation (e.g., Galileo's 200ms interception) play versus post-hoc monitoring -- should safety enforcement and observability be unified or separated?
- How effective are risk-scoring approaches (normalized 0-1 scale with thresholds at 0.3/0.5/0.7/0.85 for low/medium/high/critical) compared to binary alert triggers in production? What false positive rates are teams seeing?
- As shadow AI usage grows (47% of GenAI users on personal accounts as of 2026), what monitoring approaches can detect unauthorized AI tool usage within enterprise networks without invasive endpoint surveillance?
- Can federated or privacy-preserving monitoring approaches provide sufficient visibility for safety compliance while respecting data sovereignty requirements (EU AI Act, GDPR)?

---
