# C13.1: Request & Response Logging

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 8 (13.1.1 -- 13.1.8)

## Purpose

This section establishes requirements for capturing structured, security-relevant records of AI inference interactions. The goal is to provide forensic visibility into what prompts were sent, what responses were generated, and what safety decisions were made -- without unnecessarily capturing sensitive content. Effective request/response logging is the foundation for all downstream monitoring, abuse detection, and incident investigation capabilities in this chapter.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **13.1.1** | Verify that AI interactions are logged with security-relevant metadata (e.g., timestamp, user ID, session ID, model version, token count, input hash, system prompt version, confidence score, safety filter outcome, and safety filter decisions) without logging prompt or response content by default. | 1 | D/V | Lack of forensic trail for security investigations; inability to correlate AI events with user actions or detect anomalous usage patterns. | Review logging configuration to confirm metadata fields are captured. Inspect sample log entries for completeness. Confirm prompt/response content is absent by default. Run test inferences and verify log output schema. | The "input hash" field enables correlation without storing raw content. Teams must define which metadata fields are mandatory vs. optional for their deployment. OpenTelemetry GenAI semantic conventions provide a useful reference schema. |
| **13.1.2** | Verify that logs are stored in secure, access-controlled repositories with appropriate retention policies and backup procedures. | 1 | D/V | Unauthorized access to AI interaction logs; loss of forensic evidence due to inadequate retention; log tampering or deletion by attackers covering tracks. | Review access control policies on log storage (IAM, RBAC). Confirm retention policy documentation and automated enforcement. Verify backup procedures and test restoration. | Retention periods must balance forensic needs with privacy regulations (e.g., GDPR data minimization). AI logs may contain more sensitive context than traditional application logs. |
| **13.1.3** | Verify that log storage systems implement encryption at rest and in transit to protect sensitive information contained in logs. | 1 | D/V | Data exfiltration from log repositories; interception of log data during transmission to centralized logging systems. | Verify TLS configuration for log transport (syslog-ng, Fluentd, OTLP). Confirm encryption-at-rest settings on storage backends (S3 SSE, EBS encryption, database TDE). | Standard practice but critical for AI logs which may inadvertently contain PII, model internals, or proprietary prompt templates even after redaction. |
| **13.1.4** | Verify that sensitive data in prompts and outputs is automatically redacted or masked before logging, with configurable redaction rules for PII, credentials, and proprietary information. | 1 | D/V | PII leakage through log repositories; credential exposure in logs; compliance violations (GDPR, CCPA, HIPAA) from unredacted personal data in AI interaction logs. | Test redaction by submitting prompts containing known PII patterns (SSN, email, credit card). Verify redaction rules are configurable without code changes. Confirm redaction occurs before log write, not post-hoc. | NER-based redaction (e.g., Presidio, spaCy) catches entity types but may miss context-dependent sensitive data. Regex rules complement NER for structured patterns. False positives in redaction can impair forensic utility. |
| **13.1.5** | Verify that policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2 | D/V | Inability to debug false positives/negatives in safety filters; lack of accountability for content moderation decisions; difficulty tuning filter thresholds without historical data. | Review logs for safety filter events. Confirm they include: rule/policy that triggered, input that triggered it (redacted if needed), action taken, confidence score, and whether the action was overridden. | Critical for iterative improvement of safety filters. Without detailed logging, teams cannot measure filter precision/recall or identify systematic gaps. |
| **13.1.6** | Verify that log integrity is protected through e.g., cryptographic signatures or write-only storage. | 2 | D/V | Log tampering by attackers or insiders to hide evidence of compromise; manipulation of audit trails during incident investigation. | Check for HMAC/digital signature on log entries or append-only storage configuration (e.g., S3 Object Lock, WORM storage). Attempt to modify historical log entries and verify detection. | Append-only cloud storage (S3 Object Lock, Azure Immutable Blob) is the most practical approach. Cryptographic chaining (hash chains) provides stronger guarantees but adds complexity. |
| **13.1.7** | Verify that log entries for AI inference events capture a structured, interoperable schema that includes at minimum model identifier, token usage (input and output), provider name, and operation type, to enable consistent AI observability across tools and platforms. | 2 | D/V | Inconsistent log formats across AI services making correlation impossible; vendor lock-in to proprietary observability platforms; inability to aggregate metrics across multi-model architectures. | Validate log entries against a documented schema. Confirm interoperability by ingesting logs into at least two different observability tools. Check for OpenTelemetry GenAI semantic convention alignment. | The OpenTelemetry GenAI SIG is developing semantic conventions for LLM observability (gen_ai.* attributes). Adopting these conventions early provides forward compatibility. Key attributes: gen_ai.system, gen_ai.request.model, gen_ai.usage.input_tokens, gen_ai.usage.output_tokens. |
| **13.1.8** | Verify that full prompt and response content is logged only when a security-relevant event is detected (e.g., safety filter trigger, prompt injection detection, anomaly flag), or when required by explicit user consent and a documented legal basis. | 2 | D/V | Privacy violations from blanket content logging; storage cost explosion from full-content logging at scale; regulatory non-compliance from retaining user conversations without basis. | Review logging logic to confirm conditional content capture triggers. Test that normal interactions produce metadata-only logs. Trigger a safety event and verify full content is captured. Confirm consent mechanisms and legal basis documentation exist. | This requirement creates a tiered logging model: metadata always, content on security trigger. This balances forensic capability with privacy. The "documented legal basis" clause addresses GDPR Article 6 requirements. |

---

## Implementation Guidance

### Structured Logging with OpenTelemetry GenAI Semantic Conventions

The OpenTelemetry GenAI Semantic Conventions (stable as of OTel spec v1.37+, 2025) define a vendor-neutral schema for AI interaction telemetry. Teams should adopt these conventions to ensure interoperability across observability backends. Key attributes include:

- `gen_ai.system` -- Provider identifier (e.g., `openai`, `anthropic`)
- `gen_ai.request.model` -- Model name/version used for inference
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` -- Token consumption per request
- `gen_ai.response.finish_reasons` -- Why the model stopped generating
- `gen_ai.request.temperature`, `gen_ai.request.top_p` -- Sampling parameters

As of 2025-2026, the GenAI SIG is extending conventions to cover agentic systems, including spans for agent tasks, tool calls, memory operations, and multi-step reasoning traces. A draft convention for AI agent frameworks (CrewAI, AutoGen, LangGraph) is under development to standardize telemetry across agent orchestrators.

### Observability Platform Landscape (2025-2026)

The LLM observability ecosystem has matured significantly:

- **OpenLLMetry** (by Traceloop) -- Open-source instrumentation library built on OpenTelemetry that auto-instruments LLM frameworks (LangChain, LlamaIndex, OpenAI SDK) and emits GenAI semantic convention-compliant spans. Supported by Dynatrace, Grafana, and other backends.
- **LangSmith** (by LangChain) -- Full-lifecycle LLM observability platform with trace visualization, prompt versioning, evaluation datasets, and production monitoring.
- **Langfuse** -- Open-source LLM observability with tracing, prompt management, and evaluation scoring. Self-hostable.
- **Datadog LLM Observability** -- Announced native OpenTelemetry GenAI Semantic Convention support at DASH 2025, enabling OTLP-based ingestion of LLM traces directly into Datadog dashboards.
- **Grafana Cloud** -- Published comprehensive guides for LLM observability using OpenTelemetry + Grafana stack (Tempo for traces, Loki for logs, Mimir for metrics).

### Tiered Logging Model

Requirement 13.1.8 establishes a tiered logging architecture that has become industry best practice:

- **Tier 1 (Always):** Structured metadata -- timestamp, user ID, session ID, model version, token counts, input hash, safety filter outcome. Minimal storage cost, no privacy concerns.
- **Tier 2 (Conditional):** Full prompt/response content captured only on security-relevant triggers (safety filter activation, prompt injection detection, anomaly flags). Stored in access-restricted repositories with shorter retention.
- **Tier 3 (Consent-based):** Full content logging enabled by explicit user consent with documented legal basis (GDPR Article 6), typically for debugging or quality improvement programs.

### PII Redaction Pipeline

For requirement 13.1.4, the current best-practice pipeline combines multiple detection methods:

1. **Regex patterns** for structured PII (SSN, credit cards, phone numbers, email addresses)
2. **NER-based detection** (Microsoft Presidio, spaCy, AWS Comprehend) for entity types (names, addresses, organizations)
3. **LLM-based classification** for context-dependent sensitive data that regex and NER miss (e.g., medical conditions described in natural language, proprietary business logic in few-shot examples)
4. **Custom rules** for domain-specific patterns (internal project names, customer identifiers)

Redaction must occur in the logging pipeline before write, not as a post-hoc process. False positive rates in redaction tools remain a practical concern -- over-redaction degrades forensic utility while under-redaction creates compliance risk.

---

## Related Standards & References

- **OpenTelemetry GenAI Semantic Conventions** -- Now stable in OTel spec v1.37+, defining the standard schema for AI observability telemetry ([opentelemetry.io/docs/specs/semconv/gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/))
- **OpenLLMetry** -- Open-source OTel-based instrumentation for LLM applications, adopted by Dynatrace and others ([traceloop.com](https://www.traceloop.com/docs/openllmetry/contributing/semantic-conventions))
- **Datadog LLM Observability with OTel** -- Native GenAI semantic convention support ([datadoghq.com](https://www.datadoghq.com/blog/llm-otel-semantic-convention/))
- **Grafana LLM Observability Guide** -- Complete guide to LLM monitoring with OTel and Grafana Cloud ([grafana.com](https://grafana.com/blog/a-complete-guide-to-llm-observability-with-opentelemetry-and-grafana-cloud/))
- **OWASP Logging Cheat Sheet** -- General logging best practices applicable to AI systems
- **Microsoft Presidio** -- Open-source PII detection and redaction engine useful for 13.1.4
- **NIST SP 800-92** -- Guide to Computer Security Log Management
- **GDPR Articles 5, 6, 25** -- Data minimization, lawful basis, and data protection by design relevant to content logging decisions
- **OneUptime LLM Monitoring Guide** -- Practical guide to tracking token usage, costs, and latency with OpenTelemetry ([oneuptime.com](https://oneuptime.com/blog/post/2026-02-06-monitor-llm-opentelemetry-genai-semantic-conventions/view))

---

## Open Research Questions

- What is the optimal set of metadata fields for AI interaction logs that balances forensic utility with storage efficiency?
- How effective are current NER-based redaction tools (Presidio, spaCy) at catching AI-specific sensitive data patterns (e.g., few-shot examples containing PII, system prompt leakage)?
- Should input hashing use collision-resistant hashes (SHA-256) or locality-sensitive hashes (for near-duplicate detection)?
- How should log schemas evolve to capture multi-modal interactions (image, audio, video inputs/outputs)?
- How should the emerging OpenTelemetry agent observability conventions (task spans, tool call spans, memory operations) be integrated with security logging requirements to provide both operational and forensic visibility?
- What is the right granularity for logging agentic workflows -- should each tool invocation, reasoning step, and planning phase get its own span, or does that create prohibitive overhead?

---
