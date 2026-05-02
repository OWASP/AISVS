# C13.1: Request & Response Logging

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 4 (13.1.1, 13.1.2, 13.1.3, 13.1.4)

## Purpose

This section establishes requirements for capturing structured, security-relevant records of AI inference interactions. The goal is to provide forensic visibility into what prompts were sent, what responses were generated, and what safety decisions were made -- without unnecessarily capturing sensitive content. Effective request/response logging is the foundation for all downstream monitoring, abuse detection, and incident investigation capabilities in this chapter.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **13.1.1** | **Verify that** AI interactions are logged with security-relevant metadata (e.g. timestamp, user ID, session ID, model version, token count, input hash, system prompt version, confidence score, safety filter outcome, and safety filter decisions) without logging prompt or response content by default. | 1 | Lack of forensic trail for security investigations; inability to correlate AI events with user actions or detect anomalous usage patterns. MITRE ATLAS defense evasion tactics rely on absent or incomplete logging to avoid detection. | Review logging configuration to confirm metadata fields are captured. Inspect sample log entries for completeness against the OTel GenAI semantic conventions (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.reasoning.output_tokens`). Confirm prompt/response content is absent by default. Run test inferences and verify log output schema matches a documented specification. | The "input hash" field (SHA-256 recommended) enables correlation without storing raw content. As of April 2026, the OpenTelemetry semantic conventions reached **v1.41.0** (released April 24, 2026), which added `gen_ai.usage.reasoning.output_tokens` for reasoning-model token accounting plus streaming attributes (`gen_ai.request.stream`, `gen_ai.response.time_to_first_chunk`). Teams should also log `gen_ai.response.finish_reasons` and `gen_ai.request.temperature` for anomaly detection baselines, and capture the new `gen_ai.client.operation.exception` event to surface API errors and timeouts that would otherwise stay invisible. |
| **13.1.2** | **Verify that** policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2 | Inability to debug false positives/negatives in safety filters; lack of accountability for content moderation decisions; difficulty tuning filter thresholds without historical data. The March 18, 2026 LiteLLM guardrail-logging incident also showed that careless serialization of safety-filter execution context can leak `Authorization` headers and API keys directly into traces and spend logs. | Review logs for safety filter events. Confirm they include: rule/policy that triggered, input that triggered it (redacted if needed), action taken, confidence score, and whether the action was overridden. Verify that guardrail/safety-filter response payloads are filtered to a strict schema before serialization, so internal request fields (raw headers, API keys) never reach the logging or telemetry pipeline. | Critical for iterative improvement of safety filters. Without detailed logging, teams cannot measure filter precision/recall or identify systematic gaps. The LiteLLM <1.82.3 incident is a concrete reminder that the audit detail required by 13.1.2 has to be balanced against the secret-exfiltration risk of serializing untrusted guardrail return values verbatim. |
| **13.1.3** | **Verify that** log entries for AI inference events capture a structured, interoperable schema that includes at minimum model identifier, token usage (input and output), provider name, and operation type, to enable consistent AI observability across tools and platforms. | 2 | Inconsistent log formats across AI services making correlation impossible; vendor lock-in to proprietary observability platforms; inability to aggregate metrics across multi-model architectures. | Validate log entries against the OTel GenAI semantic conventions schema. Confirm interoperability by ingesting logs into at least two different observability backends (e.g., Datadog + Grafana, or Langfuse + custom SIEM). Use OpenLLMetry auto-instrumentation to verify compliant span emission. For agentic systems, check for `gen_ai.agent.id`, `gen_ai.agent.name`, the split client/internal `invoke_agent` spans introduced in v1.41.0, and tool execution spans. | As of April 2026, the OpenTelemetry GenAI semantic conventions have reached **v1.41.0** with broad adoption. Recent additions on top of the v1.40.0 stable core include reasoning-token accounting (`gen_ai.usage.reasoning.output_tokens`), streaming visibility (`gen_ai.request.stream`, `gen_ai.response.time_to_first_chunk`), the `gen_ai.client.operation.exception` event for API errors and timeouts, and a split between client and internal `invoke_agent` spans so agent platform owners can capture cross-process delegation. Earlier additions still in scope: cache token attributes (`cache_creation.input_tokens`, `cache_read.input_tokens`), evaluation events, retrieval spans for RAG, and reasoning content message parts. Agent framework conventions (`create_agent`, `invoke_agent` with `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.conversation.id`) remain in Development status but are widely implemented. OpenLLMetry provides drop-in instrumentation for LangChain, LlamaIndex, and the OpenAI SDK. Arize Phoenix and Confident AI add evaluation-first observability with built-in security scoring (PII leakage, prompt injection, bias detection). |
| **13.1.4** | **Verify that** full prompt and response content is logged only when a security-relevant event is detected (e.g., safety filter trigger, prompt injection detection, anomaly flag), or when required by explicit user consent and a documented legal basis. | 2 | Privacy violations from blanket content logging; storage cost explosion from full-content logging at scale; regulatory non-compliance from retaining user conversations without basis. The Log-To-Leak attack (2025 research) demonstrated that malicious MCP tools can covertly exfiltrate full conversation content through logging channels. **CVE-2025-68664** (LangChain Core, December 23, 2025, NIST CVSS 8.2 HIGH) showed that captured response content can also be a code-execution surface: prompt-injected `additional_kwargs` payloads detonate when a downstream `LangSmithRunChatLoader` or evaluation harness deserializes the stored message. | Review logging logic to confirm conditional content capture triggers. Test that normal interactions produce metadata-only logs. Trigger a safety event and verify full content is captured. Confirm consent mechanisms and legal basis documentation exist. Verify that third-party tools and MCP servers cannot inject logging calls that capture content outside the tiered policy. Verify `langchain-core` is pinned to >=0.3.81 or >=1.2.5 anywhere stored runs are replayed, and that custom deserializers mirror the new `allowed_objects` allowlist defaults. | This creates a tiered logging model: metadata always, content on security trigger. The "documented legal basis" clause addresses GDPR Article 6 requirements. The Log-To-Leak research (evaluated against GPT-4o, Claude Sonnet, and others across five MCP servers) showed high success rates for covert content exfiltration -- teams should audit tool permissions to ensure only authorized components can trigger full-content logging. CVE-2025-68664 is a reminder that "log full content on security trigger" is not a passive operation: the storage tier can become an execution tier whenever stored content is reconstructed, so the deserialization boundary deserves the same hardening as the original ingestion path. The companion CVE-2025-68665 covers `langchain.js`. |

---

## Implementation Guidance

### Structured Logging with OpenTelemetry GenAI Semantic Conventions

The OpenTelemetry GenAI Semantic Conventions define a vendor-neutral schema for AI interaction telemetry. Teams should adopt these conventions to ensure interoperability across observability backends. Key attributes include:

- `gen_ai.system` -- Provider identifier (e.g., `openai`, `anthropic`)
- `gen_ai.request.model` -- Model name/version used for inference
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` -- Token consumption per request
- `gen_ai.usage.reasoning.output_tokens` -- Reasoning-model token accounting (added in v1.41.0; without this, hidden chain-of-thought tokens get bucketed with regular output and skew cost attribution for o-series and Claude reasoning models)
- `gen_ai.usage.cache_creation.input_tokens` / `gen_ai.usage.cache_read.input_tokens` -- Cache token accounting (added in v1.40.0, essential for cost attribution with prompt caching)
- `gen_ai.request.stream` / `gen_ai.response.time_to_first_chunk` -- Streaming visibility (added in v1.41.0; matters for SLO monitoring on streamed responses where end-to-end latency is misleading)
- `gen_ai.response.finish_reasons` -- Why the model stopped generating
- `gen_ai.request.temperature`, `gen_ai.request.top_p` -- Sampling parameters

As of early May 2026, the GenAI semantic conventions have reached **v1.41.0** (released April 24, 2026) and remain the latest published version -- v1.42.0 has not shipped yet, and the GenAI conventions are still tagged experimental in the spec, with the SIG telegraphing that a stable promotion will land before the next minor version. Highlights since v1.40.0:

- Reasoning-model token accounting via `gen_ai.usage.reasoning.output_tokens`
- Streaming attributes (`gen_ai.request.stream`, `gen_ai.response.time_to_first_chunk`)
- Tool-call span naming requirement (the executed tool name must appear in span name) for clearer trace search
- Split of `invoke_agent` into separate client and internal spans with dedicated attribute groups, so agent platform operators can distinguish cross-process delegation from in-process invocation
- Domain-specific `gen_ai.client.operation.exception` event for recording API errors and timeouts inline with the inference span

Beyond these, the stable core (v1.40.0) still carries retrieval spans for RAG pipelines, evaluation events for capturing scoring results inline with traces, reasoning content message parts for chain-of-thought visibility, and `gen_ai.embeddings.dimension.count` for embedding operations. Agent framework conventions (`create_agent`, `invoke_agent`) remain in Development status but are broadly adopted by instrumentation libraries.

### Observability Platform Landscape (2026)

The LLM observability ecosystem has matured significantly, with most platforms converging on OpenTelemetry as the telemetry backbone:

- **OpenLLMetry** (by Traceloop) -- Open-source instrumentation library built on OpenTelemetry that auto-instruments LLM frameworks (LangChain, LlamaIndex, OpenAI SDK) and emits GenAI semantic convention-compliant spans. Supported by Dynatrace, Grafana, SigNoz, and other OTel-native backends.
- **LangSmith** (by LangChain) -- Full-lifecycle LLM observability platform with trace visualization, prompt versioning, evaluation datasets, production monitoring, and full-stack agent workflow tracing including tool calls and document retrieval.
- **Langfuse** -- Open-source (MIT/Apache 2.0) LLM observability with tracing, prompt management, and evaluation scoring. Now north of **19,000 GitHub stars** (up from ~6,600 a year ago), reflecting its emergence as the open-source default in 2026. Built on ClickHouse for high-throughput trace ingestion, self-hostable with SDKs for Python, TypeScript, Go, and Ruby.
- **Arize Phoenix** -- Open-source (Elastic License 2.0) platform particularly strong for drift detection with visual plots for RAG pipeline quality and pre-built evaluation templates. Runs locally in Jupyter notebooks or via Docker with zero external dependencies.
- **Confident AI** -- Evaluation-first observability platform that automatically scores every trace with 50+ research-backed metrics, including dedicated red teaming for PII leakage, prompt injection, bias, and jailbreaks. Bridges the gap between observability and security monitoring.
- **Datadog LLM Observability** -- Native OpenTelemetry GenAI Semantic Convention support (announced at DASH 2025), enabling OTLP-based ingestion of LLM traces directly into Datadog dashboards.
- **SigNoz** -- Open-source, OTel-native APM with growing LLM observability support, offering a self-hosted alternative to Datadog for teams that want full control over their telemetry pipeline.
- **Grafana Cloud** -- Published comprehensive guides for LLM observability using OpenTelemetry + Grafana stack (Tempo for traces, Loki for logs, Mimir for metrics).

### Tiered Logging Model

Requirement 13.1.8 establishes a tiered logging architecture that has become industry best practice:

- **Tier 1 (Always):** Structured metadata -- timestamp, user ID, session ID, model version, token counts, input hash, safety filter outcome. Minimal storage cost, no privacy concerns.
- **Tier 2 (Conditional):** Full prompt/response content captured only on security-relevant triggers (safety filter activation, prompt injection detection, anomaly flags). Stored in access-restricted repositories with shorter retention.
- **Tier 3 (Consent-based):** Full content logging enabled by explicit user consent with documented legal basis (GDPR Article 6), typically for debugging or quality improvement programs.

### PII Redaction Pipeline

To meet the "no prompt or response content by default" clause in 13.1.1 and the consent-gated content capture in 13.1.8, teams need a redaction pipeline that runs **before** logs are written. The current best-practice pipeline combines multiple detection methods:

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

Both 13.1.5 (policy-decision logs) and 13.1.7 (interoperable schema) lose their value if log entries can be silently rewritten after the fact. Practical implementation options break down into two tiers:

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

As of early May 2026, the EU AI Act's high-risk requirements (Articles 9-49) remain legally scheduled to become enforceable on **August 2, 2026**. The **AI Omnibus** package was supposed to push that out, but the **second political trilogue on April 28, 2026 collapsed after roughly 12 hours** without a political agreement -- the breakdown was over Annex I conformity assessment architecture for AI embedded in regulated products (machinery, medical devices), where Parliament wanted sectoral oversight and the Council resisted. A follow-up trilogue is scheduled for **approximately May 13, 2026** under the Cypriot Presidency, which has roughly six weeks before its term ends on June 30, 2026 and the file potentially rolls over to the Lithuanian Presidency starting July 1, 2026. The negotiated-but-unsigned compromise would have moved high-risk obligations to **December 2, 2027** for stand-alone Annex III systems and **August 2, 2028** for AI embedded in regulated products under Annex I. Until and unless the Omnibus passes and is published in the Official Journal, August 2, 2026 is the legally enforceable date, so compliance teams should anchor planning to that and treat any delay as a bonus rather than a baseline assumption. Article 12 logging is in the middle of the contested package -- a delay to high-risk obligations would also delay the audit-record requirements -- but it has not been a topic of dispute on its own.

Article 12 requires that high-risk AI systems support automatic recording of events ("logs") throughout their lifecycle, with a level of traceability appropriate to the system's intended purpose. Key specifics:

- Logs must enable identification of situations where the system presents a risk or undergoes substantial modification
- Logs support post-market monitoring activities under Article 72
- Minimum six-month retention period for high-risk system logs (longer where sector-specific rules apply, e.g., financial services)
- For biometric identification systems: precise timestamps, reference database details, input data that triggered matches, and identification of verification personnel
- Article 13 requires deployers receive documentation explaining how to interpret and collect these logs -- effectively a technical integration manual, not just policy paperwork

Two words in Article 12 carry most of the interpretive weight: **"technically"** and **"automatic"**. "Technically" means the logging capability must be built into or layered onto the AI system itself -- not a manual CSV export run by an operator. "Automatic" means the system emits logs on its own as events happen, not on a scheduled batch. Together, these clauses rule out application architectures that rely on post-hoc reconstruction of activity from external sources.

Penalty structure under Article 99 is tiered. Non-compliance with Article 12's record-keeping obligations falls in the middle tier: up to **EUR 15 million or 3% of worldwide annual turnover**, whichever is higher. The headline-grabbing EUR 35M / 7% maximum applies specifically to violations of Article 5 (prohibited AI practices). Article 99 also requires proportionality, so startups and SMEs typically see reduced penalties.

No finalized harmonized technical standard for Article 12 logging exists yet, but two drafts are worth tracking:

- **prEN 18229-1** -- "AI trustworthiness framework -- Part 1: Logging, transparency and human oversight". Approved and under development by CEN-CENELEC JTC 21, providing terminology, concepts, requirements, and guidance for transparency, logging, and human oversight. First publication targeted in 2026.
- **ISO/IEC DIS 24970** -- "Artificial intelligence -- AI system logging". Specifies common capabilities, requirements, and a supporting information model for logging events in AI systems. In Draft International Standard (DIS) stage.

Organizations deploying AI systems that fall under Annex III high-risk categories should evaluate their logging infrastructure against Article 12 now. Financial services providers can typically integrate AI logs into existing regulatory recordkeeping (MiFID II, DORA); other sectors must design AI-specific retention from scratch.

Organizations pursuing **ISO/IEC 42001** certification (the AI Management System standard) will find approximately 40-50% overlap with ISO 27001 governance processes, but AI-specific logging requirements go beyond traditional ISMS controls. ISO 42001 requires documented evidence of AI system behavior monitoring, risk assessment outputs, and performance tracking -- all of which depend on the structured logging infrastructure described in this section.

### Logging Threats: The Log-To-Leak Attack

A notable 2025 research paper ("Log-To-Leak: Prompt Injection Attacks on Tool-Using LLM Agents via Model Context Protocol") introduced a new class of privacy attacks targeting logging infrastructure in agentic systems. The attack uses indirect prompt injection to covertly force an agent to invoke a malicious logging tool, exfiltrating user queries, tool responses, and agent replies without degrading task performance -- making it difficult to detect through output quality monitoring alone.

The attack was evaluated across five real-world MCP servers and four frontier models (GPT-4o, GPT-5, Claude Sonnet, GPT-OSS-120b), consistently achieving high exfiltration success rates. The researchers systematized the injection prompt design space into four components: Trigger, Tool Binding, Justification, and Pressure.

Defensive implications for logging architecture:
- Tool permissions should enforce that only authorized logging components can write to log repositories
- MCP server configurations should restrict which tools can access logging endpoints
- Anomaly detection should flag unexpected logging tool invocations during agent workflows
- Content logging triggers (per 13.1.8) should be enforced at the infrastructure level, not the model level, since model-level controls can be bypassed by prompt injection

### Deserialization in the Logging Path: CVE-2025-68664 (LangChain Core)

A second class of logging-pipeline risk surfaced when **CVE-2025-68664** was published on December 23, 2025 (originally reported by Yarden Porat on December 4, 2025) against `langchain-core` versions <0.3.81 and ≥1.0.0 <1.2.5. The bug is a serialization-injection flaw in `dumps()` and `dumpd()`: dictionaries containing the reserved `lc` key are not escaped, so prompt-injected LLM output that lands in fields like `additional_kwargs` or `response_metadata` can be reconstructed as arbitrary `Serializable` subclasses when `load()`/`loads()` runs downstream. NIST scores it CVSS 8.2 (HIGH, vector `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N`); third-party advisories cite a 9.3 figure that pre-dates the NIST review. CWE-502 (Deserialization of Untrusted Data). The companion JavaScript advisory **CVE-2025-68665** covers `langchain.js`.

The advisory specifically calls out `LangSmithRunChatLoader` -- the LangSmith run loader that replays stored runs containing untrusted messages -- as a vulnerable consumer. That makes this directly a 13.1.1, 13.1.3, and 13.1.4 problem rather than just a framework bug:

- **The "logged content" travels through deserializers.** Anything captured under 13.1.4's "log full content on safety trigger" clause that later passes through a LangSmith replay, an evaluation harness, or a tracing backend that round-trips JSON can detonate the payload. The logging tier is the storage *and* the execution surface.
- **The fix changes the contract.** Patched `load()`/`loads()` introduce an `allowed_objects` allowlist, block Jinja2 templates by default, and flip `secrets_from_env` to `False`. Teams who hand-rolled their own deserialization on top of LangChain primitives need to mirror those defaults explicitly.
- **Detection is hard with metadata-only logs.** The 13.1.1 default of "metadata only" actually helps here -- attackers cannot prompt-inject into a SHA-256 hash. But teams that captured raw `response_metadata` for "richer debugging" inherit the deserialization surface even if no one is actively replaying logs.

Practical near-term actions: pin to `langchain-core>=0.3.81,<1.0.0` or `>=1.2.5`, audit any LangSmith replay/eval pipeline for untrusted runs, and treat the OTel attribute groups that copy `response_metadata` (some custom OpenLLMetry extensions do this) as part of the deserialization attack surface. Reference advisories: NVD ([nvd.nist.gov/vuln/detail/CVE-2025-68664](https://nvd.nist.gov/vuln/detail/CVE-2025-68664)), GHSA ([github.com/advisories/GHSA-c67j-w6g6-q2cm](https://github.com/advisories/GHSA-c67j-w6g6-q2cm)), Cyata's "LangGrinch" write-up with a working PoC ([cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664](https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/)).

### Supply Chain Risks to Logging Infrastructure: The LiteLLM Breach

On **March 24, 2026**, the widely-used LiteLLM Python package (an LLM API proxy gateway with ~3.4 million daily downloads and more than 40,000 developer users) was compromised via a supply chain attack. The threat actor group "TeamPCP" exfiltrated PyPI publishing credentials by compromising the Trivy scanner step in LiteLLM's GitHub Actions CI/CD pipeline, then published two backdoored versions to PyPI.

Public timeline (UTC) reconstructed from post-incident analyses:

- **10:39** -- Malicious `litellm==1.82.7` published to PyPI
- **10:52** -- More aggressive `litellm==1.82.8` published, adding a `.pth` file execution hook
- **11:48** -- A downstream user's workload crashed; security researcher traced the crash to the new release
- **12:44** -- Attackers suppressed the emerging GitHub issue discussion
- **13:38** -- PyPI quarantined the entire package (approximately three hours after initial publication; the two malicious versions were together live for ~40 minutes before detection)

The payload ran in three stages:

1. **Credential harvesting** -- Scanned environment variables and local files for SSH keys, AWS/GCP/Azure IAM credentials, Kubernetes service account tokens, HashiCorp Vault tokens, LLM API keys (OpenAI, Anthropic), crypto wallets, and `.env` files
2. **Lateral movement** -- Used discovered Kubernetes tokens to probe in-cluster APIs, deployed rogue pods (naming pattern `node-setup-*` in `kube-system`), and enumerated privilege escalation paths
3. **Persistence** -- Installed a systemd user service at `~/.config/systemd/user/sysmon.service` masquerading as "System Telemetry Service" that beaconed to C2 endpoints (`models.litellm.cloud`, `checkmarx.zone`) for secondary payload delivery

The malicious code lived primarily in `litellm/proxy/proxy_server.py` -- the exact component that sits between applications and LLM providers, routing and logging all inference traffic -- with the `.pth` injection via `litellm_init.pth` extending execution to any Python process on the machine, not just code that imported LiteLLM.

This incident has direct implications for the metadata-capture and interoperable-schema requirements (13.1.1 and 13.1.7) -- because once the proxy is compromised, every "structured" log entry it emits is attacker-controlled:

- **LLM proxy gateways are high-value targets** because they centralize API keys, log all inference traffic, and often have broad network access to multiple AI providers. Compromising the proxy compromises the entire logging pipeline.
- **Dependency integrity verification** (version pinning, hash checking, SBOM monitoring, Sigstore signatures where available) is essential for any component in the logging data path. Static scanning alone is insufficient; runtime behavioral monitoring of proxy processes -- especially outbound DNS and unexpected systemd service creation -- would have surfaced this payload earlier.
- **The `.pth` file injection** in 1.82.8 is particularly pernicious because it executes whenever Python starts on the host, persisting beyond the specific application that imported LiteLLM. Import-level monitoring misses it entirely.
- **CI/CD hygiene for maintainers**: the root cause was a compromised Trivy step inside LiteLLM's own GitHub Actions, so signing and publishing credentials should be scoped to dedicated release jobs with minimal environment exposure, not shared with general-purpose scanning stages.

Teams using LLM proxy gateways for centralized logging should treat them as security-critical infrastructure subject to the same supply chain controls as other privileged components (see C06 Supply Chain). The LiteLLM maintainers' own post-mortem ([docs.litellm.ai/blog/security-update-march-2026](https://docs.litellm.ai/blog/security-update-march-2026)) is a useful reference for detection and remediation guidance.

### Guardrail Logging Secret Exposure (LiteLLM, March 2026)

A second LiteLLM logging-layer incident, distinct from the supply chain compromise above and disclosed on **March 18, 2026**, illustrates exactly the threat that requirement 13.1.2 (logging of policy decisions and safety-filter actions) introduces if implemented carelessly. The vulnerability affected all LiteLLM versions **prior to 1.82.3** and was triggered when a custom guardrail returned a response object that contained the original request data structure -- including `secret_fields.raw_headers` with plaintext `Authorization` headers and API keys.

What went wrong, in sequence:

1. The guardrail evaluation path captured the full guardrail response and serialized it into the spend-log payload and OpenTelemetry traces without stripping internal request metadata
2. Operators, admins, and any downstream observability backend consuming those traces could read leaked credentials in the logs UI or trace explorer
3. The exposure was not on the inference response path -- it lived inside the policy-decision/safety-filter logs that 13.1.2 explicitly mandates be captured for audit and debugging

Defensive lessons specific to AI logging architectures:

- **Treat guardrail/safety-filter outputs as untrusted relative to the logging pipeline.** A guardrail can be authored by a third-party plugin, by a customer, or by an LLM-generated configuration; its returned object should be filtered to a known-good schema before any logging adapter sees it
- **Strip secrets at the edge, not at the consumer.** Once a header containing an API key reaches an OTel exporter, every backend that ingests the trace gets a copy. Sanitization belongs immediately after the guardrail callback returns, before any structured serialization
- **Apply the same redaction pipeline to policy-decision logs as to prompt/response content.** Teams often Presidio-scan request/response text but pass guardrail metadata through verbatim because it "isn't user content" -- this incident shows that's exactly where credentials end up
- **Audit telemetry consumer permissions** so that staff who can read spend logs or traces aren't implicitly granted credential access to upstream services

This is also a reminder that 13.1.2's "sufficient detail to enable audit" needs to be balanced against the secret-exfiltration risk created by serializing the full safety-filter execution context. The LiteLLM maintainers' incident report ([docs.litellm.ai/blog/guardrail-logging-secret-exposure-incident](https://docs.litellm.ai/blog/guardrail-logging-secret-exposure-incident)) walks through the exact exposure paths and the schema-strict fix landed in 1.82.3.

### Cost Attribution and FinOps Logging

Token usage logging (requirements 13.1.1 and 13.1.7) increasingly serves a dual purpose: security monitoring and cost governance. The FinOps Foundation's 2026 guidance on AI cost management recommends:

- **Granular attribution tagging** -- stamp every inference request with project, team, feature, and environment metadata at the proxy layer, enabling cost-per-request and cost-per-feature reporting
- **Cache token tracking** -- with prompt caching now standard across major providers, logging `cache_creation.input_tokens` and `cache_read.input_tokens` (OTel GenAI v1.40.0 attributes) is necessary for accurate cost accounting
- **Anomaly detection on token consumption** -- sudden spikes in token usage per user or per session can indicate both abuse (prompt injection campaigns, model extraction attempts) and runaway agentic loops, making token monitoring a shared security/FinOps concern

Organizations implementing comprehensive token optimization based on logged usage data typically report 20-40% reductions in token consumption with minimal quality impact. The LLM proxy pattern (LiteLLM, Portkey, Helicone) has emerged as the standard architecture for centralized token tracking, though the LiteLLM breach demonstrates the supply chain risk of this centralization.

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

- **OpenTelemetry GenAI Semantic Conventions** -- Stable in OTel spec v1.40.0, defining the standard schema for AI observability telemetry ([opentelemetry.io/docs/specs/semconv/gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/))
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
- **EU AI Act Article 12** -- Record-keeping requirements for high-risk AI systems, enforcement legally still August 2, 2026 after the April 28, 2026 AI Omnibus trilogue collapsed. The proposed (unsigned) delay would push high-risk obligations to December 2, 2027 (Annex III stand-alone) and August 2, 2028 (Annex I embedded) ([ai-act-service-desk.ec.europa.eu](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-12), practical walkthrough at [helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements](https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/))
- **AI Omnibus Trilogue Tracking (April-May 2026)** -- Modulos analysis of the April 28 trilogue collapse and the May 13 follow-up under the Cypriot Presidency, plus OneTrust's structured view of the proposed delay package ([modulos.ai/blog/ai-act-omnibus-trilogue-failed](https://www.modulos.ai/blog/ai-act-omnibus-trilogue-failed/), [onetrust.com/blog/how-the-eu-digital-omnibus-reshapes-ai-act-timelines-and-governance-in-2026](https://www.onetrust.com/blog/how-the-eu-digital-omnibus-reshapes-ai-act-timelines-and-governance-in-2026/), [iapp.org/news/a/ai-act-omnibus-what-just-happened-and-what-comes-next](https://iapp.org/news/a/ai-act-omnibus-what-just-happened-and-what-comes-next))
- **OpenTelemetry Semantic Conventions v1.41.0 Release** -- April 24, 2026 release adding `gen_ai.usage.reasoning.output_tokens`, streaming attributes, the `gen_ai.client.operation.exception` event, and split client/internal `invoke_agent` spans ([github.com/open-telemetry/semantic-conventions/releases](https://github.com/open-telemetry/semantic-conventions/releases))
- **prEN 18229-1** -- Draft CEN-CENELEC AI trustworthiness framework Part 1 covering logging, transparency, and human oversight ([genorma.com/en/standards/pren-18229-1](https://genorma.com/en/standards/pren-18229-1))
- **ISO/IEC DIS 24970** -- Draft International Standard for AI system logging, defining capabilities and an information model for event logging ([iso.org/standard/88723.html](https://www.iso.org/standard/88723.html))
- **GDPR Articles 5, 6, 25** -- Data minimization, lawful basis, and data protection by design relevant to content logging decisions
- **MITRE ATLAS** -- Adversarial Threat Landscape for AI Systems, including defense evasion (log manipulation) techniques ([atlas.mitre.org](https://atlas.mitre.org/))
- **MITRE ATT&CK T1070** -- Indicator Removal techniques applicable to AI audit trail tampering ([attack.mitre.org/techniques/T1070](https://attack.mitre.org/techniques/T1070/))
- **Log-To-Leak** -- Research on prompt injection attacks targeting logging in MCP-based agent systems ([openreview.net](https://openreview.net/forum?id=UVgbFuXPaO))
- **OneUptime LLM Monitoring Guide** -- Practical guide to tracking token usage, costs, and latency with OpenTelemetry ([oneuptime.com](https://oneuptime.com/blog/post/2026-02-06-monitor-llm-opentelemetry-genai-semantic-conventions/view))
- **LiteLLM Supply Chain Breach (March 2026)** -- Detailed technical analysis of the TeamPCP supply chain attack on LiteLLM's PyPI package, compromising the LLM proxy logging layer ([sonatype.com](https://www.sonatype.com/blog/compromised-litellm-pypi-package-delivers-multi-stage-credential-stealer))
- **Datadog Security Labs: LiteLLM Campaign Analysis** -- In-depth tracing of the TeamPCP supply chain campaign including indicators of compromise ([securitylabs.datadoghq.com](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/))
- **Cycode Technical Analysis: LiteLLM** -- Minute-by-minute reconstruction of the March 24, 2026 compromise, including the three-stage payload (credential harvesting, K8s lateral movement, systemd persistence) ([cycode.com](https://cycode.com/blog/lite-llm-supply-chain-attack/))
- **Trend Micro: Inside the LiteLLM Supply Chain Compromise** -- Incident deep-dive on the AI gateway backdoor and its implications for proxy-based logging ([trendmicro.com](https://www.trendmicro.com/en_us/research/26/c/inside-litellm-supply-chain-compromise.html))
- **LiteLLM Official Post-Mortem** -- Maintainer security update covering detection, affected versions (1.82.7, 1.82.8), and remediation guidance ([docs.litellm.ai](https://docs.litellm.ai/blog/security-update-march-2026))
- **LiteLLM Guardrail Logging Secret Exposure Incident (March 18, 2026)** -- Separate maintainer incident report covering the guardrail-logging path that leaked `Authorization` headers into spend logs and OTel traces in versions <1.82.3 ([docs.litellm.ai/blog/guardrail-logging-secret-exposure-incident](https://docs.litellm.ai/blog/guardrail-logging-secret-exposure-incident))
- **CVE-2025-68664 (LangChain Core Serialization Injection)** -- Critical deserialization flaw in `dumps()`/`loads()` directly affecting LangSmith run loaders that replay stored messages. NIST CVSS 8.2 HIGH, fixed in 0.3.81 / 1.2.5 ([nvd.nist.gov/vuln/detail/CVE-2025-68664](https://nvd.nist.gov/vuln/detail/CVE-2025-68664), advisory at [github.com/advisories/GHSA-c67j-w6g6-q2cm](https://github.com/advisories/GHSA-c67j-w6g6-q2cm), and Cyata's "LangGrinch" PoC walkthrough at [cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664](https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/))
- **Arize Phoenix** -- Open-source AI observability with drift detection and RAG pipeline quality monitoring ([github.com/Arize-ai/phoenix](https://github.com/Arize-ai/phoenix))
- **SigNoz** -- Open-source, OTel-native APM with LLM observability support ([signoz.io](https://signoz.io/comparisons/llm-observability-tools/))
- **FinOps Foundation: AI Cost & Usage Tracker** -- Guidance on building generative AI cost tracking with token-level attribution ([finops.org](https://www.finops.org/wg/how-to-build-a-generative-ai-cost-and-usage-tracker/))
- **ISO/IEC 42001** -- AI Management System standard with logging and audit trail implications for AI governance ([secureprivacy.ai](https://secureprivacy.ai/blog/iso-42001-implementation-guide-2026))

---

## Open Research Questions

- How effective are current NER-based redaction tools (Presidio, spaCy, AWS Comprehend) at catching AI-specific sensitive data patterns such as few-shot examples containing PII, system prompt leakage, or proprietary business logic embedded in prompt templates? Benchmarks across diverse AI workloads are sparse.
- Should input hashing use collision-resistant hashes (SHA-256) or locality-sensitive hashes (MinHash, SimHash) for near-duplicate detection? The choice affects whether logs can support abuse pattern clustering or only exact-match correlation.
- How should log schemas evolve to capture multi-modal interactions (image, audio, video inputs/outputs)? Current OTel conventions focus on text; hashing and metadata extraction for images and audio remain undefined.
- What is the right granularity for logging agentic workflows -- should each tool invocation, reasoning step, and planning phase get its own span, or does that create prohibitive overhead? Early telemetry from production agent deployments suggests 10-50x more spans per user request compared to single-inference systems.
- How can logging infrastructure defend against Log-To-Leak style attacks where prompt injection causes agents to invoke unauthorized logging tools? Can infrastructure-level enforcement (rather than model-level) fully mitigate this class of attack?
- How should organizations reconcile the EU AI Act's minimum six-month retention requirement with GDPR's data minimization principle when AI interaction logs contain redacted-but-reconstructable personal data?
- What are the forensic implications of running multiple model versions simultaneously (A/B testing, canary deployments)? How should log correlation handle version-specific behavioral differences?
- How should organizations secure LLM proxy gateways (LiteLLM, Portkey, Helicone) that centralize logging, given that the March 2026 LiteLLM supply chain attack demonstrated that compromising the proxy gives attackers access to all API keys and inference traffic? Is the centralized proxy pattern worth the single-point-of-failure risk?
- As prompt caching becomes standard, how should logging schemas account for the distinction between cache hits and fresh inference for both cost attribution and security analysis? Cache hits may mask repeated adversarial probing if not properly tracked.
- How should the industry treat the deserialization boundary on stored conversation logs after CVE-2025-68664? Replay-based evaluation, A/B test rerunning, and human-in-the-loop debug review all reconstruct stored messages, which means every "log full content" capture point is a potential code path. Should evaluation harnesses by default operate on metadata + redacted text rather than reconstructed message objects, even at the cost of less faithful replay?

---

## Related Pages

- [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging) -- Parent chapter that ties this section to abuse detection, drift monitoring, incident response, and proactive agent behavior monitoring
- [C13.2 Abuse Detection & Alerting](C13-02-Abuse-Detection-Alerting) -- Downstream consumer of the metadata logged here: signature-based jailbreak detection, SIEM integration, and covert-channel detection all depend on the 13.1 log schema
- [C13.5 Incident Response Planning & Execution](C13-05-Incident-Response) -- Where the tamper-protected, redacted logs from 13.1 become forensic evidence during AI-specific incident response
- [C13.3 Model, Data, and Performance Drift Detection](C13-03-Model-Drift-Detection) -- Time-series drift and hallucination trending that build on the continuous metadata stream defined in 13.1.1 and 13.1.7
- [C14.3 Chain of Responsibility & Auditability](C14-03-Chain-of-Responsibility-Auditability) -- Goes one layer deeper on tamper-evident logging (hash chains, WORM storage, sidecar writers) for the same EU AI Act Article 12/19/73 audit chain
- [C07.6 Source Attribution & Citation Integrity](C07-06-Source-Attribution-Citation-Integrity) -- Real-time metrics and versioned logs of safety violations that feed off the 13.1 metadata schema

---
