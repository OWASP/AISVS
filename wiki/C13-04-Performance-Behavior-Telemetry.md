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

## Related Standards & References

- **OpenTelemetry** -- Vendor-neutral observability framework for metrics, traces, and logs ([opentelemetry.io](https://opentelemetry.io/))
- **Prometheus + Grafana** -- Open-source metrics collection and visualization widely used for AI infrastructure monitoring
- **NVIDIA DCGM** -- Data Center GPU Manager for GPU-specific monitoring metrics
- **OWASP Top 10 for LLM: LLM10 Unbounded Consumption** -- Directly addressed by token tracking and resource monitoring controls
- **FinOps Foundation** -- Cost management frameworks applicable to AI inference cost attribution

---

## Open Research Questions

- What are effective baseline models for "normal" token consumption patterns across different AI application types?
- How should GPU monitoring differ between training and inference workloads for security purposes?
- Can output-to-input ratio monitoring be generalized across modalities (text, image, audio), or does each need its own baseline?
- What is the minimum granularity of token attribution needed to reliably detect denial-of-wallet attacks?

---
