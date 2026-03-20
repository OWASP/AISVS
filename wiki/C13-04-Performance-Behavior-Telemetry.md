# C13.4: Performance & Behavior Telemetry

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 5 (13.4.1 -- 13.4.5)

## Purpose

This section covers the continuous collection and monitoring of operational metrics for AI systems. Performance telemetry serves dual purposes: operational health monitoring (latency, throughput, resource usage) and security monitoring (anomalous resource consumption, token abuse, cost attacks). These metrics provide the quantitative foundation for detecting denial-of-service attacks, denial-of-wallet attacks, and resource exhaustion scenarios specific to AI workloads.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **13.4.1** | Verify that operational metrics including request latency, token consumption, memory usage, and throughput are continuously collected and monitored. | 1 | D/V | Denial-of-service via resource exhaustion; undetected performance degradation impacting user experience; inability to capacity plan or detect infrastructure issues. | Confirm metrics collection via APM/observability stack (Prometheus, Datadog, etc.). Verify dashboards display real-time latency (p50/p95/p99), token rates, memory, and throughput. Check data retention and granularity. | Standard APM tooling (Prometheus + Grafana, Datadog, New Relic) extends well to AI workloads. AI-specific additions: token consumption per request, queue depth for inference requests, GPU utilization, and model loading time. OpenTelemetry provides vendor-neutral instrumentation. |
| **13.4.2** | Verify that success and failure rates are tracked with categorization of error types and their root causes. | 1 | D/V | Systematic failures going undetected; inability to distinguish between infrastructure errors and model errors; missing patterns in error types that indicate attacks or data quality issues. | Review error categorization taxonomy. Verify error rates are tracked by category (e.g., model timeout, safety filter block, invalid input, rate limit, internal error). Confirm root cause attribution exists for common error types. Test error alerting thresholds. | AI-specific error categories to track: safety filter rejections, context window exceeded, tool call failures, RAG retrieval failures, output validation failures, and model capacity errors. Distinguish between expected rejections (safety filters working correctly) and unexpected errors. |
| **13.4.3** | Verify that resource utilization monitoring includes GPU/CPU usage, memory consumption, and storage requirements with alerting on threshold breaches. | 2 | D/V | GPU exhaustion from adversarial inputs (computationally expensive prompts); memory leaks in model serving infrastructure; storage exhaustion from log/cache accumulation; cryptomining on AI GPU infrastructure. | Verify GPU/CPU/memory monitoring agents are deployed on inference servers. Confirm threshold-based alerting for each resource type. Test alerts by simulating resource exhaustion. Verify GPU-specific metrics (utilization, memory, temperature). | GPU monitoring requires specialized tooling (NVIDIA DCGM, nvidia-smi exporter for Prometheus). AI workloads have unique resource patterns: inference is bursty, batch processing saturates GPUs, and model loading creates memory spikes. Alert thresholds should account for these patterns. |
| **13.4.4** | Verify that token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | 2 | D/V | Denial-of-wallet attacks where individual cost limits are circumvented; compromised credentials used for high-volume inference; inability to attribute costs or detect abuse at the organizational level. | Verify token tracking dimensions in the metrics system. Confirm per-user, per-session, per-endpoint, and per-team breakdowns are available. Test cost attribution reporting. Verify anomaly detection operates at each granularity level. | Token attribution enables: (1) cost allocation and chargeback, (2) abuse detection at multiple granularities, (3) capacity planning by feature/team, (4) identification of inefficient prompt patterns. Requires correlation between authentication identity and inference requests -- ensure this mapping is reliable for service accounts and API keys. |
| **13.4.5** | Verify that output-to-input token ratio anomalies are detected and alerted. | 2 | D/V | Prompt injection causing verbose model outputs (data exfiltration via inflated responses); model behavior anomalies indicated by abnormal output length; denial-of-wallet via responses disproportionate to inputs. | Establish baseline output/input ratio distributions for each endpoint. Test detection by submitting prompts designed to produce disproportionately long outputs. Verify alerting triggers on ratio anomalies. Review false positive rates against legitimate use cases (e.g., code generation naturally has high ratios). | Output-to-input ratio is a useful lightweight indicator. Normal ratios vary significantly by use case: summarization has low ratios, code generation has high ratios, chat is roughly 1:1. Baselines must be endpoint-specific. Extreme ratio anomalies (>10x normal) may indicate prompt injection forcing verbose output or data exfiltration. |

---

## Implementation Guidance

### OpenTelemetry as the Telemetry Foundation

OpenTelemetry (OTel) has established itself as the vendor-neutral standard for AI performance telemetry in 2025-2026. The framework provides three signal types that map directly to the requirements in this section:

- **Traces** -- Capture end-to-end request flow through inference pipelines, including model selection, prompt construction, inference, post-processing, and response delivery. Each step becomes a span with duration, status, and attributes.
- **Metrics** -- Continuous time-series data for latency (p50/p95/p99), throughput (requests/second), token consumption rates, error rates, and resource utilization. Collected via Prometheus-compatible exporters or OTLP.
- **Events** -- Discrete occurrences such as safety filter triggers, rate limit hits, and error conditions, enriched with GenAI semantic convention attributes.

The GenAI Semantic Conventions (OTel spec v1.37+) define standardized attributes for AI telemetry:

| Attribute | Description | Relevant Requirement |
|-----------|-------------|---------------------|
| `gen_ai.usage.input_tokens` | Tokens consumed in the prompt | 13.4.1, 13.4.4 |
| `gen_ai.usage.output_tokens` | Tokens generated in the response | 13.4.1, 13.4.4, 13.4.5 |
| `gen_ai.request.model` | Model identifier | 13.4.1 |
| `gen_ai.response.finish_reasons` | Why generation stopped | 13.4.2 |
| `gen_ai.system` | Provider name (openai, anthropic, etc.) | 13.4.4 |

**OpenLLMetry** (by Traceloop) provides auto-instrumentation libraries that emit these attributes automatically for major LLM frameworks (LangChain, LlamaIndex, OpenAI SDK, Anthropic SDK), reducing manual instrumentation effort to near-zero.

### Observability Stack Patterns

Common production telemetry architectures for AI systems in 2025-2026:

**Open-Source Stack:**
- OpenTelemetry SDK (instrumentation) -> OTel Collector (processing/routing) -> Prometheus (metrics) + Grafana (visualization) + Tempo (traces) + Loki (logs)
- Grafana has published comprehensive guides for LLM observability using this stack, with pre-built dashboards for token usage, latency, and cost tracking.

**Commercial Platforms:**
- **Datadog LLM Observability** -- Native OTel GenAI semantic convention support (announced DASH 2025). Accepts OTLP traces directly, provides LLM-specific dashboards, token cost attribution, and anomaly detection.
- **LangSmith** -- LangChain's observability platform with trace visualization, prompt versioning, evaluation datasets, and production monitoring dashboards. Tightly integrated with LangChain/LangGraph agent frameworks.
- **Langfuse** -- Open-source alternative with tracing, prompt management, and evaluation scoring. Self-hostable for data sovereignty requirements.

**Key Decision:** Teams using multi-provider or multi-model architectures should standardize on OpenTelemetry as the instrumentation layer and route to their preferred backend, rather than adopting vendor-specific SDKs from each observability platform.

### Token Cost Attribution (13.4.4)

Granular token tracking enables four critical capabilities:

1. **Cost allocation and chargeback** -- Attribute inference costs to teams, features, or customers for FinOps
2. **Abuse detection** -- Identify compromised credentials or denial-of-wallet attacks at per-user, per-session, and per-endpoint granularity
3. **Capacity planning** -- Forecast token demand by feature and team to negotiate provider commitments
4. **Prompt optimization** -- Identify inefficient prompt patterns consuming disproportionate tokens

Implementation requires reliable correlation between authentication identity and inference requests. For service accounts and API keys, ensure the mapping supports attribution at the human-operator level, not just the service identity.

Token cost calculations should incorporate provider pricing tiers (input vs. output tokens, model-specific rates, batch vs. real-time pricing) and be tracked as a derived metric alongside raw token counts.

### Output-to-Input Ratio Monitoring (13.4.5)

The output-to-input token ratio is a lightweight but effective anomaly indicator. Normal ratios vary significantly by use case:

| Use Case | Typical Output:Input Ratio |
|----------|---------------------------|
| Summarization | 0.1 - 0.3 |
| Chat / Q&A | 0.5 - 2.0 |
| Code generation | 2.0 - 10.0 |
| Translation | 0.8 - 1.2 |
| Data extraction | 0.1 - 0.5 |

Baselines must be established per endpoint. Extreme ratio anomalies (>10x the endpoint baseline) may indicate prompt injection forcing verbose output, data exfiltration via inflated responses, or model behavioral anomalies. Alert thresholds should be set relative to rolling baselines with endpoint-specific calibration.

### GPU and Infrastructure Monitoring (13.4.3)

AI workloads have unique resource consumption patterns that differ from traditional application monitoring:

- **Inference is bursty:** GPU utilization spikes during inference requests and drops between them. Alert thresholds must account for this pattern to avoid false positives.
- **Model loading creates memory spikes:** Loading large models into GPU VRAM can temporarily consume all available memory. Distinguish model-load events from anomalous memory consumption.
- **Batch processing saturates GPUs:** Legitimate batch inference jobs will show sustained 100% GPU utilization that should not trigger alerts.

NVIDIA DCGM (Data Center GPU Manager) provides GPU-specific metrics exportable to Prometheus: utilization percentage, memory usage, temperature, power draw, and error counts. The `nvidia-smi` exporter for Prometheus is the most common collection mechanism for Kubernetes-based inference deployments.

Security-relevant GPU monitoring signals include: unexpected GPU utilization on idle inference servers (potential cryptomining), sustained memory pressure without corresponding inference requests (potential resource exhaustion attack), and abnormal error rates indicating hardware degradation or adversarial inputs designed to trigger computational edge cases.

---

## Related Standards & References

- **OpenTelemetry GenAI Semantic Conventions** -- Standard attributes for AI telemetry, stable in OTel spec v1.37+ ([opentelemetry.io/docs/specs/semconv/gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/))
- **OpenLLMetry** -- Auto-instrumentation for LLM frameworks emitting OTel GenAI conventions ([traceloop.com](https://www.traceloop.com/blog/visualizing-llm-performance-with-opentelemetry-tools-for-tracing-cost-and-latency))
- **OpenTelemetry Agent Observability** -- Evolving standards for AI agent telemetry ([opentelemetry.io/blog/2025/ai-agent-observability](https://opentelemetry.io/blog/2025/ai-agent-observability/))
- **OneUptime Token/Cost/Latency Tracking** -- Practical guide to OTel-based LLM metrics ([oneuptime.com](https://oneuptime.com/blog/post/2026-02-06-track-token-usage-prompt-costs-model-latency-opentelemetry/view))
- **Grafana LLM Observability Guide** -- Complete OTel + Grafana stack for LLM monitoring ([grafana.com](https://grafana.com/blog/a-complete-guide-to-llm-observability-with-opentelemetry-and-grafana-cloud/))
- **Prometheus + Grafana** -- Open-source metrics collection and visualization widely used for AI infrastructure monitoring
- **NVIDIA DCGM** -- Data Center GPU Manager for GPU-specific monitoring metrics
- **OWASP Top 10 for LLM 2025: LLM10 Unbounded Consumption** -- Directly addressed by token tracking and resource monitoring controls
- **FinOps Foundation** -- Cost management frameworks applicable to AI inference cost attribution
- **Datadog LLM Observability** -- Native OTel GenAI convention support ([datadoghq.com](https://www.datadoghq.com/blog/llm-otel-semantic-convention/))

---

## Open Research Questions

- What are effective baseline models for "normal" token consumption patterns across different AI application types?
- How should GPU monitoring differ between training and inference workloads for security purposes?
- Can output-to-input ratio monitoring be generalized across modalities (text, image, audio), or does each need its own baseline?
- What is the minimum granularity of token attribution needed to reliably detect denial-of-wallet attacks?
- How should telemetry for agentic AI systems (multi-step tool calling, planning loops) differ from single-inference monitoring, and what new metrics are needed to capture agent-specific performance and cost patterns?
- What is the right approach for correlating token cost anomalies across multiple providers in multi-model architectures?

---
