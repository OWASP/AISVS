# C13.1: Request & Response Logging

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 8 (13.1.1 -- 13.1.8)

## Purpose

This section establishes requirements for capturing structured, security-relevant records of AI inference interactions. The goal is to provide forensic visibility into what prompts were sent, what responses were generated, and what safety decisions were made -- without unnecessarily capturing sensitive content. Effective request/response logging is the foundation for all downstream monitoring, abuse detection, and incident investigation capabilities in this chapter.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **13.1.1** | Verify that AI interactions are logged with security-relevant metadata (e.g., timestamp, user ID, session ID, model version, token count, input hash, system prompt version, confidence score, safety filter outcome, and safety filter decisions) without logging prompt or response content by default. | 1 | D/V | Lack of forensic trail for security investigations; inability to correlate AI events with user actions or detect anomalous usage patterns. MITRE ATLAS defense evasion tactics rely on absent or incomplete logging to avoid detection. | Review logging configuration to confirm metadata fields are captured. Inspect sample log entries for completeness against the OTel GenAI semantic conventions (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`). Confirm prompt/response content is absent by default. Run test inferences and verify log output schema matches a documented specification. | The "input hash" field (SHA-256 recommended) enables correlation without storing raw content. As of March 2026, the OpenTelemetry GenAI semantic conventions (stable in OTel spec v1.37+) are the de facto reference schema. Teams should also log `gen_ai.response.finish_reasons` and `gen_ai.request.temperature` for anomaly detection baselines. |
| **13.1.2** | Verify that logs are stored in secure, access-controlled repositories with appropriate retention policies and backup procedures. | 1 | D/V | Unauthorized access to AI interaction logs; loss of forensic evidence due to inadequate retention; log tampering or deletion by attackers covering tracks. The EU AI Act Article 12 mandates automatic logging with traceability for high-risk AI systems (enforcement August 2026). | Review access control policies on log storage (IAM, RBAC). Confirm retention policy documentation and automated enforcement -- the EU AI Act requires at least six months of log retention for high-risk systems. Verify backup procedures and test restoration. Cross-check that RBAC roles separate log-writer, log-reader, and log-admin privileges. | Retention periods must balance forensic needs with privacy regulations (GDPR data minimization vs. EU AI Act six-month minimum). AI logs may contain more sensitive context than traditional application logs. Organizations operating high-risk AI systems under the EU AI Act face fines up to EUR 35M or 7% of global turnover for non-compliance. |
| **13.1.3** | Verify that log storage systems implement encryption at rest and in transit to protect sensitive information contained in logs. | 1 | D/V | Data exfiltration from log repositories; interception of log data during transmission to centralized logging systems. | Verify TLS configuration for log transport (syslog-ng, Fluentd, OTLP). Confirm encryption-at-rest settings on storage backends (S3 SSE, EBS encryption, database TDE). | Standard practice but critical for AI logs which may inadvertently contain PII, model internals, or proprietary prompt templates even after redaction. |
| **13.1.4** | Verify that sensitive data in prompts and outputs is automatically redacted or masked before logging, with configurable redaction rules for PII, credentials, and proprietary information. | 1 | D/V | PII leakage through log repositories; credential exposure in logs; compliance violations (GDPR, CCPA, HIPAA) from unredacted personal data in AI interaction logs. Related to OWASP LLM Top 10 LLM06 (Sensitive Information Disclosure). | Test redaction by submitting prompts containing known PII patterns (SSN, email, credit card numbers, API keys). Verify redaction rules are configurable without code changes. Confirm redaction occurs in the logging pipeline before write, not post-hoc. Test with Microsoft Presidio or LLM Guard's Anonymize scanner. Measure false positive rates and their impact on forensic utility. | NER-based redaction (Microsoft Presidio, spaCy, AWS Comprehend) catches entity types but may miss context-dependent sensitive data like medical conditions described in natural language or proprietary business logic in few-shot examples. LLM Guard (by Protect AI) offers an integrated pipeline combining PII anonymization with prompt injection detection. Regex rules complement NER for structured patterns. As of 2026, no single tool achieves both high recall and low false-positive rates across all PII categories. |
| **13.1.5** | Verify that policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2 | D/V | Inability to debug false positives/negatives in safety filters; lack of accountability for content moderation decisions; difficulty tuning filter thresholds without historical data. | Review logs for safety filter events. Confirm they include: rule/policy that triggered, input that triggered it (redacted if needed), action taken, confidence score, and whether the action was overridden. | Critical for iterative improvement of safety filters. Without detailed logging, teams cannot measure filter precision/recall or identify systematic gaps. |
| **13.1.6** | Verify that log integrity is protected through e.g., cryptographic signatures or write-only storage. | 2 | D/V | Log tampering by attackers or insiders to hide evidence of compromise; manipulation of audit trails during incident investigation. MITRE ATLAS lists log manipulation as a defense evasion technique, and MITRE ATT&CK T1070 (Indicator Removal) applies directly to AI audit trails. | Check for HMAC/digital signature on log entries or append-only storage configuration (S3 Object Lock in Compliance mode, Azure Immutable Blob Storage, GCS Bucket Lock). Attempt to modify historical log entries and verify detection or rejection. For hash-chained logs, verify the chain is validated on read. | Append-only cloud storage (S3 Object Lock Compliance mode, Azure Immutable Blob) is the most practical approach for most teams. Cryptographic hash chaining provides stronger tamper-evidence but adds operational complexity. Note that S3 Object Lock in Governance mode can be overridden by privileged users -- Compliance mode is required for true immutability. |
| **13.1.7** | Verify that log entries for AI inference events capture a structured, interoperable schema that includes at minimum model identifier, token usage (input and output), provider name, and operation type, to enable consistent AI observability across tools and platforms. | 2 | D/V | Inconsistent log formats across AI services making correlation impossible; vendor lock-in to proprietary observability platforms; inability to aggregate metrics across multi-model architectures. | Validate log entries against the OTel GenAI semantic conventions schema. Confirm interoperability by ingesting logs into at least two different observability backends (e.g., Datadog + Grafana, or Langfuse + custom SIEM). Use OpenLLMetry auto-instrumentation to verify compliant span emission. For agentic systems, check for `gen_ai.agent.id`, `gen_ai.agent.name`, and tool execution spans. | As of March 2026, the OpenTelemetry GenAI semantic conventions are stable (v1.37+) and widely adopted. Datadog announced native OTel GenAI convention support at DASH 2025. The GenAI SIG is now extending conventions for agentic systems with `create_agent` and `invoke_agent` span types, plus attributes for `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.conversation.id`, and tool definitions. OpenLLMetry provides drop-in instrumentation for LangChain, LlamaIndex, and the OpenAI SDK. |
| **13.1.8** | Verify that full prompt and response content is logged only when a security-relevant event is detected (e.g., safety filter trigger, prompt injection detection, anomaly flag), or when required by explicit user consent and a documented legal basis. | 2 | D/V | Privacy violations from blanket content logging; storage cost explosion from full-content logging at scale; regulatory non-compliance from retaining user conversations without basis. The Log-To-Leak attack (2025 research) demonstrated that malicious MCP tools can covertly exfiltrate full conversation content through logging channels. | Review logging logic to confirm conditional content capture triggers. Test that normal interactions produce metadata-only logs. Trigger a safety event and verify full content is captured. Confirm consent mechanisms and legal basis documentation exist. Verify that third-party tools and MCP servers cannot inject logging calls that capture content outside the tiered policy. | This creates a tiered logging model: metadata always, content on security trigger. The "documented legal basis" clause addresses GDPR Article 6 requirements. The Log-To-Leak research (evaluated against GPT-4o, Claude Sonnet, and others across five MCP servers) showed high success rates for covert content exfiltration -- teams should audit tool permissions to ensure only authorized components can trigger full-content logging. |

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

As of 2026, the tooling landscape for inline PII redaction includes:

- **Microsoft Presidio** -- Mature open-source framework supporting NER (spaCy, Stanza, Transformers), regex, and deny-list recognizers. Extensible with custom recognizers for domain-specific patterns. Self-hostable.
- **LLM Guard** (Protect AI) -- Combines PII anonymization with prompt injection detection, toxicity scanning, and output validation in a single pipeline. Useful when redaction and security scanning need to share a processing stage.
- **AWS Comprehend PII Detection** -- Managed service supporting 30+ PII entity types with confidence scores. Good for teams already in the AWS ecosystem, though adds a network hop to the logging pipeline.
- **John Snow Labs Healthcare NLP** -- Specialized for clinical/medical PII (PHI) with HIPAA-tuned NER models. Relevant for healthcare AI deployments where standard NER models underperform on medical terminology.

### Log Integrity and Tamper Protection

For requirement 13.1.6, the practical implementation options break down into two tiers:

**Cloud-native immutability (recommended for most teams):**
- AWS S3 Object Lock in **Compliance mode** (not Governance mode -- Governance allows privileged override) with a retention period matching your log retention policy
- Azure Immutable Blob Storage with time-based retention policies
- GCS Bucket Lock with retention policies

**Cryptographic tamper-evidence (for higher assurance):**
- Hash chaining where each log entry includes a cryptographic hash of the previous entry, creating a verifiable chain. Breaking the chain at any point is detectable.
- HMAC signing of individual log entries using a key stored in a hardware security module (HSM) or cloud KMS
- Merkle tree structures for batch verification of large log sets

The MITRE ATT&CK framework documents T1070 (Indicator Removal) as a common defense evasion technique. In AI systems, this extends to attackers modifying or deleting inference logs to hide prompt injection attempts, data exfiltration, or model abuse patterns. Log integrity controls should be validated by attempting unauthorized modification and confirming detection.

### EU AI Act Compliance (Article 12)

As of March 2026, the EU AI Act's high-risk requirements (Articles 9-49) take effect in August 2026. Article 12 specifically requires that high-risk AI systems support automatic recording of events ("logs") throughout their lifecycle, with a level of traceability appropriate to the system's intended purpose. Key specifics:

- Logs must enable identification of situations where the system presents a risk or undergoes substantial modification
- Logs support post-market monitoring activities
- Minimum six-month retention period for high-risk system logs
- For biometric identification systems: precise timestamps, reference database details, input data that triggered matches, and identification of verification personnel

Organizations deploying AI systems that fall under Annex III high-risk categories should evaluate their logging infrastructure against Article 12 now, given the August 2026 enforcement deadline. Non-compliance carries penalties of up to EUR 35 million or 7% of global annual turnover.

### Logging Threats: The Log-To-Leak Attack

A notable 2025 research paper ("Log-To-Leak: Prompt Injection Attacks on Tool-Using LLM Agents via Model Context Protocol") introduced a new class of privacy attacks targeting logging infrastructure in agentic systems. The attack uses indirect prompt injection to covertly force an agent to invoke a malicious logging tool, exfiltrating user queries, tool responses, and agent replies without degrading task performance -- making it difficult to detect through output quality monitoring alone.

The attack was evaluated across five real-world MCP servers and four frontier models (GPT-4o, GPT-5, Claude Sonnet, GPT-OSS-120b), consistently achieving high exfiltration success rates. The researchers systematized the injection prompt design space into four components: Trigger, Tool Binding, Justification, and Pressure.

Defensive implications for logging architecture:
- Tool permissions should enforce that only authorized logging components can write to log repositories
- MCP server configurations should restrict which tools can access logging endpoints
- Anomaly detection should flag unexpected logging tool invocations during agent workflows
- Content logging triggers (per 13.1.8) should be enforced at the infrastructure level, not the model level, since model-level controls can be bypassed by prompt injection

### Agentic System Logging

As AI systems evolve from single-inference APIs to multi-step agentic workflows, logging requirements expand significantly. The OpenTelemetry GenAI SIG is developing semantic conventions for agentic system observability, including:

- **`create_agent` spans** -- Capture agent initialization with `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.description`, and `gen_ai.agent.version`
- **`invoke_agent` spans** -- Track agent invocations with conversation context (`gen_ai.conversation.id`), input/output messages, and tool definitions
- **Tool execution spans** -- Record each tool call within an agent workflow, enabling reconstruction of multi-step reasoning chains

For security logging purposes, agentic workflows create additional challenges:
- Each tool invocation represents a potential privilege boundary crossing that should be logged
- Multi-agent systems (where agents delegate to other agents) need correlation IDs that span the full delegation chain
- Memory operations (reading from and writing to vector stores or conversation history) may expose sensitive data and should be logged with the same tiered approach as inference interactions
- The 2025 ServiceNow Now Assist vulnerability (second-order prompt injection through agent delegation) demonstrated that agent-to-agent interactions are a live attack surface requiring comprehensive logging

---

## Related Standards & References

- **OpenTelemetry GenAI Semantic Conventions** -- Stable in OTel spec v1.37+, defining the standard schema for AI observability telemetry ([opentelemetry.io/docs/specs/semconv/gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/))
- **OpenTelemetry GenAI Agent Span Conventions** -- Emerging conventions for agentic system observability ([opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/))
- **OpenLLMetry** -- Open-source OTel-based instrumentation for LLM applications, adopted by Dynatrace and others ([traceloop.com](https://www.traceloop.com/docs/openllmetry/contributing/semantic-conventions))
- **Datadog LLM Observability with OTel** -- Native GenAI semantic convention support announced at DASH 2025 ([datadoghq.com](https://www.datadoghq.com/blog/llm-otel-semantic-convention/))
- **Grafana LLM Observability Guide** -- Complete guide to LLM monitoring with OTel and Grafana Cloud ([grafana.com](https://grafana.com/blog/a-complete-guide-to-llm-observability-with-opentelemetry-and-grafana-cloud/))
- **OWASP Logging Cheat Sheet** -- General logging best practices applicable to AI systems
- **OWASP LLM Top 10** -- LLM06 (Sensitive Information Disclosure) directly relevant to logging PII risks ([genai.owasp.org](https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/))
- **Microsoft Presidio** -- Open-source PII detection and redaction framework ([github.com/microsoft/presidio](https://github.com/microsoft/presidio))
- **LLM Guard** (Protect AI) -- Security toolkit combining PII anonymization with prompt injection detection ([protectai.com/llm-guard](https://protectai.com/llm-guard))
- **Langfuse** -- Open-source LLM observability with tracing, prompt management, and security guardrail integration ([langfuse.com](https://langfuse.com/docs/security-and-guardrails))
- **NIST SP 800-92 Rev. 1** (Draft) -- Cybersecurity Log Management Planning Guide, updating the original 2006 publication ([csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd))
- **EU AI Act Article 12** -- Record-keeping requirements for high-risk AI systems, enforcement August 2026 ([ai-act-service-desk.ec.europa.eu](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-12))
- **GDPR Articles 5, 6, 25** -- Data minimization, lawful basis, and data protection by design relevant to content logging decisions
- **MITRE ATLAS** -- Adversarial Threat Landscape for AI Systems, including defense evasion (log manipulation) techniques ([atlas.mitre.org](https://atlas.mitre.org/))
- **MITRE ATT&CK T1070** -- Indicator Removal techniques applicable to AI audit trail tampering ([attack.mitre.org/techniques/T1070](https://attack.mitre.org/techniques/T1070/))
- **Log-To-Leak** -- Research on prompt injection attacks targeting logging in MCP-based agent systems ([openreview.net](https://openreview.net/forum?id=UVgbFuXPaO))
- **OneUptime LLM Monitoring Guide** -- Practical guide to tracking token usage, costs, and latency with OpenTelemetry ([oneuptime.com](https://oneuptime.com/blog/post/2026-02-06-monitor-llm-opentelemetry-genai-semantic-conventions/view))

---

## Open Research Questions

- How effective are current NER-based redaction tools (Presidio, spaCy, AWS Comprehend) at catching AI-specific sensitive data patterns such as few-shot examples containing PII, system prompt leakage, or proprietary business logic embedded in prompt templates? Benchmarks across diverse AI workloads are sparse.
- Should input hashing use collision-resistant hashes (SHA-256) or locality-sensitive hashes (MinHash, SimHash) for near-duplicate detection? The choice affects whether logs can support abuse pattern clustering or only exact-match correlation.
- How should log schemas evolve to capture multi-modal interactions (image, audio, video inputs/outputs)? Current OTel conventions focus on text; hashing and metadata extraction for images and audio remain undefined.
- What is the right granularity for logging agentic workflows -- should each tool invocation, reasoning step, and planning phase get its own span, or does that create prohibitive overhead? Early telemetry from production agent deployments suggests 10-50x more spans per user request compared to single-inference systems.
- How can logging infrastructure defend against Log-To-Leak style attacks where prompt injection causes agents to invoke unauthorized logging tools? Can infrastructure-level enforcement (rather than model-level) fully mitigate this class of attack?
- How should organizations reconcile the EU AI Act's minimum six-month retention requirement with GDPR's data minimization principle when AI interaction logs contain redacted-but-reconstructable personal data?
- What are the forensic implications of running multiple model versions simultaneously (A/B testing, canary deployments)? How should log correlation handle version-specific behavioral differences?

---
