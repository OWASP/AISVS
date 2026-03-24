# C13.4: Performance & Behavior Telemetry

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 5 (13.4.1 -- 13.4.5)

## Purpose

This section covers the continuous collection and monitoring of operational metrics for AI systems. Performance telemetry serves dual purposes: operational health monitoring (latency, throughput, resource usage) and security monitoring (anomalous resource consumption, token abuse, cost attacks). These metrics provide the quantitative foundation for detecting denial-of-service attacks, denial-of-wallet attacks, and resource exhaustion scenarios specific to AI workloads.

---

## Threat Landscape

Performance telemetry is not just an ops concern -- it is the primary detection layer for several active attack classes targeting AI systems in production. Understanding the threat landscape helps justify the monitoring requirements below.

### Denial-of-Wallet (DoW) Attacks

Denial-of-wallet attacks exploit the pay-per-token pricing model of hosted inference APIs. Attackers craft inputs designed to maximize token consumption, turning a predictable utility bill into a financial liability. Common techniques include:

- **Resource-intensive prompts** -- Inputs that force computationally expensive tasks (generating thousands of lines of code, analyzing massive documents, solving complex mathematical problems) to inflate per-request costs.
- **Recursive prompting** -- Crafted inputs that cause the model's output to become the input for the next query, creating exponential token growth. In demonstrated scenarios, attackers have been able to breach daily spending limits (e.g., $5,000/day) within minutes using distributed processes.
- **Agentic infinite loops** -- As of 2025, agentic AI systems introduce a new DoW vector: an attacker can trigger recursive agent loops through prompt injection, forcing systems into endless cycles of reasoning, tool use, and API calls. A single-agent hallucination loop (e.g., "find policy X... keep searching until you do") can consume budget indefinitely. Multi-agent circular dependencies -- where Agent A awaits Agent B's output while B awaits A's -- create deadlock patterns that drain tokens at each retry.
- **File system recursion** -- Agents reading files that contain instructions to read themselves, rapidly expanding context windows and draining token budgets.

OWASP Top 10 for LLM Applications 2025 addresses this directly under **LLM10: Unbounded Consumption**, covering denial of service, denial of wallet, and model extraction via excessive API usage.

### Sponge Attacks and Computational Exhaustion

Sponge attacks (also called "sponge examples") are adversarial inputs specifically crafted to exploit the quadratic complexity of Transformer attention mechanisms. IEEE EuroS&P research demonstrated 30x latency increases on language models using these techniques. In one notable case, a sponge attack pushed Microsoft Azure Translator response times from 1ms to 6 seconds -- a 6,000x degradation. As of early 2025, researchers also documented a "Reasoning Interruption Attack" against reasoning models like DeepSeek-R1, where crafted prompts can forcibly interrupt the inference reasoning process through adaptive token compression techniques.

### Agentic Resource Exhaustion (2025 Incidents)

The rise of agentic AI has created new classes of resource exhaustion that telemetry must detect:

- **Amazon Q code agent poisoning** (July 2025) -- A malicious pull request injected commands into an Amazon Q agent that triggered deletion of AWS resources, demonstrating how compromised agents can cascade through infrastructure.
- **Shadow Escape MCP exploit** (2025) -- Zero-click workflow hijacking via malicious MCP rules files, enabling attackers to redirect agent behavior without user interaction.
- **Cascading hallucination propagation** -- Research has shown a single compromised agent can poison 87% of downstream agent decisions within 4 hours, with false vendor credentials triggering unauthorized payments.

These incidents underscore why telemetry needs to cover not just single-inference metrics but multi-step agent execution patterns, including iteration counts, context window growth rates, and cross-agent token consumption.

### MITRE ATLAS Mapping

The requirements in this section directly mitigate several MITRE ATLAS techniques:

- **AML.T0029 (Denial of ML Service)** -- Overloading inference endpoints to disrupt availability. Detected via latency and throughput monitoring (13.4.1) and resource utilization alerts (13.4.3).
- **AML.T0034 (Cost Harvesting)** -- Abusing inference APIs to exhaust operational budgets. Detected via granular token attribution (13.4.4) and ratio anomaly detection (13.4.5).
- **AML.T0048 (External Harms)** -- Causing financial harm by manipulating AI system resource consumption. Mitigated through per-user and per-session cost tracking (13.4.4).

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

#### Agentic System Conventions (Emerging)

As of March 2026, the OpenTelemetry community is developing dedicated semantic conventions for agentic AI systems (see [open-telemetry/semantic-conventions#2664](https://github.com/open-telemetry/semantic-conventions/issues/2664)). The emerging agent span conventions introduce attributes for tracing agent lifecycle and execution:

| Attribute | Description | Relevant Requirement |
|-----------|-------------|---------------------|
| `gen_ai.agent.id` | Unique agent identifier | 13.4.4 (attribution) |
| `gen_ai.agent.name` | Human-readable agent name | 13.4.2 (error categorization) |
| `gen_ai.conversation.id` | Conversation/thread identifier | 13.4.4 (session tracking) |
| `gen_ai.data_source.id` | Data source identifier for RAG | 13.4.2 (failure attribution) |
| `gen_ai.tool.definitions` | Available tool definitions (array) | 13.4.2, 13.4.4 |

Agent spans use `CLIENT` kind for remote agent calls and `INTERNAL` for in-process agents. This distinction matters for telemetry routing -- remote agent calls should capture network latency separately from inference latency. Teams building agentic systems should instrument agent invocations now using these emerging conventions, even though they have not yet reached stable status, to avoid costly re-instrumentation later.

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

As of 2025, NVIDIA has rolled out a GPU fleet management platform that aggregates telemetry from globally distributed deployments into the NGC cloud platform, surfacing hardware health, energy efficiency, and physical GPU location in real time. For organizations running GPU clusters, Trend Micro's integration with NVIDIA Morpheus provides GPU-accelerated anomaly detection at the infrastructure layer, achieving 20x throughput improvement for data loss prevention scanning on inference traffic.

### Agentic Telemetry Patterns

Agentic AI systems (multi-step tool-calling, planning loops, multi-agent orchestration) require telemetry beyond what single-inference monitoring provides. Key metrics to track:

- **Iteration count per agent invocation** -- Hard limits (e.g., max 15 steps) should trigger alerts well before the limit is reached. A sudden increase in average iteration count may indicate prompt injection causing reasoning loops.
- **Context window growth rate** -- Monitor how quickly an agent's context window fills across steps. Rapid growth (especially in file-reading or web-browsing agents) may signal file system recursion attacks.
- **Cross-agent token consumption** -- In multi-agent architectures, track total token spend across the agent graph, not just per-agent. Circular dependencies between agents can only be detected by correlating consumption across the full workflow.
- **Tool call frequency and diversity** -- An agent repeatedly calling the same tool with slightly different parameters (semantic deduplication) is a hallucination loop indicator.
- **Execution timeouts** -- Complement token budgets with wall-clock timeouts. An agent may consume few tokens per step but take thousands of steps.

**Watchdog pattern:** Deploy a smaller, cheaper model to monitor the main agent's behavior in real time. The watchdog inspects the last N steps (typically 5) for cycle detection, semantic repetition, and budget trajectory. This adds modest cost but catches runaway agents before they exhaust budgets. Practical implementations include custom LangChain callbacks or LangGraph interrupt handlers that evaluate agent state against predefined safety predicates.

### Defense-in-Depth: Token Budgeting and Rate Limiting

Telemetry alone is not sufficient -- it must be coupled with enforcement mechanisms:

1. **Per-request token budgets** -- Assign a maximum token budget to each inference request or agent invocation. Terminate immediately when the budget is exceeded. This is the most effective mitigation against denial-of-wallet attacks.
2. **Per-user and per-session rate limits** -- Track cumulative token consumption per authenticated identity over sliding windows (1 minute, 1 hour, 1 day). Alert at 80% of limit; hard-block at 100%.
3. **Prompt complexity analysis** -- Reject or flag prompts that exhibit patterns associated with sponge attacks: excessive repetition, deeply nested structures, or instructions designed to maximize attention computation.
4. **Semantic caching** -- Cache responses for semantically similar prompts (using embedding similarity) to serve repeated heavy prompts without incurring additional inference costs. This doubles as a DoW mitigation and a latency optimization.
5. **Cost alerting with automated circuit breakers** -- When total inference spend exceeds a configurable threshold within a time window, automatically degrade service (e.g., switch to a smaller model, reduce max output tokens) rather than allowing unbounded spend.

---

## Related Standards & References

- **OpenTelemetry GenAI Semantic Conventions** -- Standard attributes for AI telemetry, stable in OTel spec v1.37+ ([opentelemetry.io/docs/specs/semconv/gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/))
- **OTel GenAI Agent Span Conventions** -- Emerging semantic conventions for agentic system observability ([opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/))
- **OpenLLMetry** -- Auto-instrumentation for LLM frameworks emitting OTel GenAI conventions ([traceloop.com](https://www.traceloop.com/blog/visualizing-llm-performance-with-opentelemetry-tools-for-tracing-cost-and-latency))
- **OpenTelemetry Agent Observability** -- Evolving standards for AI agent telemetry ([opentelemetry.io/blog/2025/ai-agent-observability](https://opentelemetry.io/blog/2025/ai-agent-observability/))
- **OneUptime Token/Cost/Latency Tracking** -- Practical guide to OTel-based LLM metrics ([oneuptime.com](https://oneuptime.com/blog/post/2026-02-06-track-token-usage-prompt-costs-model-latency-opentelemetry/view))
- **Grafana LLM Observability Guide** -- Complete OTel + Grafana stack for LLM monitoring ([grafana.com](https://grafana.com/blog/a-complete-guide-to-llm-observability-with-opentelemetry-and-grafana-cloud/))
- **Prometheus + Grafana** -- Open-source metrics collection and visualization widely used for AI infrastructure monitoring
- **NVIDIA DCGM** -- Data Center GPU Manager for GPU-specific monitoring metrics ([github.com/NVIDIA/DCGM](https://github.com/NVIDIA/DCGM))
- **NVIDIA GPU Fleet Management** -- Centralized telemetry platform for globally distributed GPU deployments via NGC
- **Trend Micro + NVIDIA Morpheus** -- GPU-accelerated anomaly detection for AI infrastructure security ([trendmicro.com](https://www.trendmicro.com/en_us/research/25/e/trend-secures-ai-infrastructure-with-nvidia.html))
- **OWASP Top 10 for LLM 2025: LLM10 Unbounded Consumption** -- Directly addressed by token tracking and resource monitoring controls
- **MITRE ATLAS: AML.T0029 (Denial of ML Service)** -- Attack technique for overloading inference endpoints ([atlas.mitre.org](https://atlas.mitre.org/))
- **MITRE ATLAS: AML.T0034 (Cost Harvesting)** -- Attack technique for exhausting operational budgets via API abuse
- **MITRE ATLAS: AML.T0048 (External Harms)** -- Financial harm through manipulated AI resource consumption
- **Prompt Security: Denial of Wallet on GenAI Apps** -- Practical DoW attack analysis ([prompt.security](https://prompt.security/blog/denial-of-wallet-on-genai-apps-ddow))
- **Lasso Security: DoS & Denial of Wallet Threats** -- Attack taxonomy and mitigation strategies ([lasso.security](https://www.lasso.security/blog/denial-of-service-dos-and-denial-of-wallet-dow-attacks))
- **Sponge Attack Research (IEEE EuroS&P)** -- Adversarial inputs exploiting Transformer attention complexity for 30x+ latency increases
- **FinOps Foundation** -- Cost management frameworks applicable to AI inference cost attribution
- **Datadog LLM Observability** -- Native OTel GenAI convention support ([datadoghq.com](https://www.datadoghq.com/blog/llm-otel-semantic-convention/))
- **Langfuse** -- Open-source LLM observability with tracing, prompt management, and evaluation ([langfuse.com](https://langfuse.com/))

---

## Open Research Questions

- What are effective baseline models for "normal" token consumption patterns across different AI application types, and how should baselines adapt to seasonal or usage-driven shifts?
- How should GPU monitoring differ between training and inference workloads for security purposes?
- Can output-to-input ratio monitoring be generalized across modalities (text, image, audio), or does each need its own baseline?
- What is the right approach for correlating token cost anomalies across multiple providers in multi-model architectures?
- How effective are watchdog models at detecting novel runaway agent patterns they were not explicitly trained to recognize?
- What is the optimal trade-off between semantic caching coverage and cache poisoning risk -- can an attacker craft prompts to pollute the cache and serve incorrect responses to legitimate users?
- As reasoning models (chain-of-thought, tree-of-thought) become standard, how should telemetry distinguish between legitimate extended reasoning and adversarial reasoning-exhaustion attacks?
- What telemetry standards will emerge for monitoring MCP (Model Context Protocol) tool server interactions, where token consumption spans multiple trust boundaries?

---
