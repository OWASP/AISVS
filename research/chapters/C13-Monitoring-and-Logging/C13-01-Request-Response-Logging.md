# C13.1: Request & Response Logging

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging.md)
> **Requirements:** 5 | **IDs:** 13.1.1--13.1.5

## Purpose

This section establishes requirements for capturing structured, security-relevant records of AI inference interactions. The goal is to provide forensic visibility into what prompts were sent, what responses were generated, and what safety decisions were made -- without unnecessarily capturing sensitive content. Effective request/response logging is the foundation for all downstream monitoring, abuse detection, and incident investigation capabilities in this chapter.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **13.1.1** | **Verify that** AI interactions are logged with security-relevant metadata (e.g., timestamp, user ID, session ID, model version, token count, input hash, system prompt version, confidence score, safety filter outcome, and safety filter decisions). | 1 | Lack of forensic trail for security investigations; inability to correlate AI events with user actions or detect anomalous usage patterns. MITRE ATLAS defense evasion tactics rely on absent or incomplete logging to avoid detection. | Review logging configuration to confirm metadata fields are captured. Inspect sample log entries for completeness against the OTel GenAI semantic conventions (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.reasoning.output_tokens`). Confirm prompt/response content is absent by default. Run test inferences and verify log output schema matches a documented specification. | The "input hash" field (SHA-256 recommended) enables correlation without storing raw content. As of May 14, 2026, the main OpenTelemetry semantic-conventions release is **v1.41.1** (a May 11 maintenance release; GenAI feature additions landed in **v1.41.0** on April 28), while the separate GenAI conventions repository advertises schema version **1.42.0** and includes MCP-specific spans. Teams should log `gen_ai.response.finish_reasons`, `gen_ai.request.temperature`, streaming latency, and `gen_ai.client.operation.exception`; for agent tool traffic, add `mcp.method.name`, `mcp.session.id`, `jsonrpc.request.id`, and `gen_ai.tool.name` without recording prompt, response, or resource content by default. |
| **13.1.2** | **Verify that** AI interaction logs exclude prompt and response content by default, and that content logging is enabled only on explicit opt-in with documented justification. | 1 | Sensitive information disclosure from blanket prompt/response capture; privacy overcollection; credentials, health data, legal material, or proprietary context leaking into trace stores; replay and deserialization exposure when stored conversations are later reconstructed. Current OWASP mapping is LLM02:2025 Sensitive Information Disclosure, with LLM06:2025 Excessive Agency relevant when agents can invoke logging tools. | Inspect SDK, proxy, OpenTelemetry, and observability-backend configuration to confirm raw content attributes such as `gen_ai.input.messages`, `gen_ai.output.messages`, prompt text, response text, tool arguments, retrieval document text, and raw `Authorization` headers are disabled by default. Run a normal inference with canary PII and fake secrets, then verify the values are absent from logs, traces, SIEM events, and spend dashboards. Enable content capture through the documented opt-in path and verify the approval record, legal basis, data classification, retention period, access group, and audit entry. Test pre-export masking using controls such as Langfuse `mask` hooks, OpenTelemetry processors, Microsoft Presidio, or LLM Guard before telemetry leaves the application boundary. | OpenTelemetry treats message-content capture as opt-in, but default behavior still varies by SDK, framework callback, and proxy. Redaction tools remain probabilistic: false negatives create privacy exposure, while false positives reduce forensic value. Opt-in content logging should use schema allowlists, strip headers and secrets, and fail closed for regulated data. The March 18, 2026 LiteLLM guardrail-logging incident showed that even policy-decision metadata can leak `Authorization` headers when guardrail return objects are serialized without strict filtering. CVE-2026-42208 is a newer reminder that proxy auth paths should log a hashed key identifier and decision outcome, never the caller-supplied bearer token that may itself contain exploit payloads. |
| **13.1.3** | **Verify that** policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2 | Inability to debug false positives/negatives in safety filters; lack of accountability for content moderation decisions; difficulty tuning filter thresholds without historical data. The March 18, 2026 LiteLLM guardrail-logging incident also showed that careless serialization of safety-filter execution context can leak `Authorization` headers and API keys directly into traces and spend logs. | Review logs for safety filter events. Confirm they include: rule/policy that triggered, input that triggered it (redacted if needed), action taken, confidence score, and whether the action was overridden. Verify that guardrail/safety-filter response payloads are filtered to a strict schema before serialization, so internal request fields (raw headers, API keys) never reach the logging or telemetry pipeline. | Critical for iterative improvement of safety filters. Without detailed logging, teams cannot measure filter precision/recall or identify systematic gaps. The LiteLLM <1.82.3 incident is a concrete reminder that the audit detail required by 13.1.2 has to be balanced against the secret-exfiltration risk of serializing untrusted guardrail return values verbatim. |
| **13.1.4** | **Verify that** log entries for AI inference events capture a structured, interoperable schema that includes at minimum model identifier, token usage (input and output), provider name, and operation type, to enable consistent AI observability across tools and platforms. | 2 | Inconsistent log formats across AI services making correlation impossible; vendor lock-in to proprietary observability platforms; inability to aggregate metrics across multi-model architectures. | Validate log entries against the OTel GenAI semantic conventions schema. Confirm interoperability by ingesting logs into at least two different observability backends (e.g., Datadog + Grafana, or Langfuse + custom SIEM). Use OpenLLMetry or OpenInference auto-instrumentation to verify compliant span emission. For agentic systems, check for `gen_ai.agent.id`, `gen_ai.agent.name`, the split client/internal `invoke_agent` spans introduced in v1.41.0, MCP spans (`mcp.method.name`, `mcp.session.id`, `rpc.response.status_code`), and tool execution spans. | As of May 14, 2026, the OpenTelemetry GenAI ecosystem is still in Development status: core semantic-conventions releases are at **v1.41.1**, while the GenAI-specific repository is publishing a **1.42.0** schema URL with MCP coverage. Recent additions on top of the v1.40.0 stable core include reasoning-token accounting (`gen_ai.usage.reasoning.output_tokens`), streaming visibility (`gen_ai.request.stream`, `gen_ai.response.time_to_first_chunk`), the `gen_ai.client.operation.exception` event for API errors and timeouts, split client/internal `invoke_agent` spans, simplified `gen_ai.tool.definitions` when content capture is disabled, and MCP client/server spans for JSON-RPC tool traffic. Agent framework conventions (`create_agent`, `invoke_agent` with `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.conversation.id`) remain developmental but are widely implemented. OpenLLMetry provides drop-in instrumentation for LangChain, LlamaIndex, and the OpenAI SDK; OpenInference adds a parallel OTel-compatible convention set used heavily by Arize Phoenix. |
| **13.1.5** | **Verify that** full prompt and response content is logged only when a security-relevant event is detected (e.g., safety filter trigger, prompt injection detection, anomaly flag), or when required by explicit user consent and a documented legal basis. | 2 | Privacy violations from blanket content logging; storage cost explosion from full-content logging at scale; regulatory non-compliance from retaining user conversations without basis. The Log-To-Leak attack (2025 research) demonstrated that malicious MCP tools can covertly exfiltrate full conversation content through logging channels. **CVE-2025-68664** (LangChain Core, December 23, 2025, NIST CVSS 8.2 HIGH) showed that captured response content can also be a code-execution surface: prompt-injected `additional_kwargs` payloads detonate when a downstream `LangSmithRunChatLoader` or evaluation harness deserializes the stored message. | Review logging logic to confirm conditional content capture triggers. Test that normal interactions produce metadata-only logs. Trigger a safety event and verify full content is captured. Confirm consent mechanisms and legal basis documentation exist. Verify that third-party tools and MCP servers cannot inject logging calls that capture content outside the tiered policy. Verify `langchain-core` is pinned to >=0.3.81 or >=1.2.5 anywhere stored runs are replayed, and that custom deserializers mirror the new `allowed_objects` allowlist defaults. | This creates a tiered logging model: metadata always, content on security trigger. The "documented legal basis" clause addresses GDPR Article 6 requirements. The Log-To-Leak research (evaluated against GPT-4o, Claude Sonnet, and others across five MCP servers) showed high success rates for covert content exfiltration -- teams should audit tool permissions to ensure only authorized components can trigger full-content logging. CVE-2025-68664 is a reminder that "log full content on security trigger" is not a passive operation: the storage tier can become an execution tier whenever stored content is reconstructed, so the deserialization boundary deserves the same hardening as the original ingestion path. The companion CVE-2025-68665 covers `langchain.js`. |

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
- `gen_ai.tool.definitions` -- Tool definition metadata; v1.41.0 clarifies simplified capture when content capture is disabled so schemas can remain useful without storing full tool descriptions

As of May 14, 2026, the main OpenTelemetry semantic-conventions project has reached **v1.41.1** (released May 11, 2026), while the separate GenAI semantic-conventions repository advertises schema URL **1.42.0**. The v1.41.1 release is a maintenance patch; the GenAI-relevant behavioral changes below came in v1.41.0 on April 28. GenAI conventions are still tagged Development in the spec, so teams should pin the emitted semantic-convention version and document any `OTEL_SEMCONV_STABILITY_OPT_IN` choices. Highlights since v1.40.0:

- Reasoning-model token accounting via `gen_ai.usage.reasoning.output_tokens`
- Streaming attributes (`gen_ai.request.stream`, `gen_ai.response.time_to_first_chunk`)
- Tool-call span naming requirement (the executed tool name must appear in span name) for clearer trace search
- Simplified `gen_ai.tool.definitions` capture when content capture is disabled, preserving tool-schema observability without logging full instructions or argument examples
- Split of `invoke_agent` into separate client and internal spans with dedicated attribute groups, so agent platform operators can distinguish cross-process delegation from in-process invocation
- Domain-specific `gen_ai.client.operation.exception` event for recording API errors and timeouts inline with the inference span
- MCP client/server spans for JSON-RPC tool traffic, including `mcp.method.name`, `mcp.session.id`, `mcp.protocol.version`, `jsonrpc.request.id`, `rpc.response.status_code`, `gen_ai.tool.name`, and opt-in `mcp.resource.uri`

Beyond these, the stable core (v1.40.0) still carries retrieval spans for RAG pipelines, evaluation events for capturing scoring results inline with traces, reasoning content message parts for chain-of-thought visibility, and `gen_ai.embeddings.dimension.count` for embedding operations. Agent framework conventions (`create_agent`, `invoke_agent`) remain in Development status but are broadly adopted by instrumentation libraries.

### Observability Platform Landscape (2026)

The LLM observability ecosystem has matured significantly, with most platforms converging on OpenTelemetry as the telemetry backbone:

- **OpenLLMetry** (by Traceloop) -- Open-source instrumentation library built on OpenTelemetry that auto-instruments LLM frameworks (LangChain, LlamaIndex, OpenAI SDK) and emits GenAI semantic convention-compliant spans. Supported by Dynatrace, Grafana, SigNoz, and other OTel-native backends.
- **LangSmith** (by LangChain) -- Full-lifecycle LLM observability platform with trace visualization, prompt versioning, evaluation datasets, production monitoring, and full-stack agent workflow tracing including tool calls and document retrieval.
- **Langfuse** -- Open-source (MIT/Apache 2.0) LLM observability with tracing, prompt management, and evaluation scoring. Now north of **19,000 GitHub stars** (up from ~6,600 a year ago), reflecting its emergence as the open-source default in 2026. Built on ClickHouse for high-throughput trace ingestion, self-hostable with SDKs for Python, TypeScript, Go, and Ruby.
- **Arize Phoenix** -- Open-source (Elastic License 2.0) platform particularly strong for drift detection with visual plots for RAG pipeline quality and pre-built evaluation templates. Runs locally in Jupyter notebooks or via Docker with zero external dependencies.
- **OpenInference** -- OTel-compatible semantic conventions and instrumentation used by Phoenix and Arize AX. It covers LLM calls, embeddings, chains, retrieval, reranking, agent steps, tool calls, session/user IDs, and framework integrations for LangChain, LlamaIndex, DSPy, Bedrock, Vertex AI, CrewAI, Haystack, LiteLLM, and others.
- **Confident AI** -- Evaluation-first observability platform that automatically scores every trace with 50+ research-backed metrics, including dedicated red teaming for PII leakage, prompt injection, bias, and jailbreaks. Bridges the gap between observability and security monitoring.
- **Datadog LLM Observability** -- Native OpenTelemetry GenAI Semantic Convention support (announced at DASH 2025), enabling OTLP-based ingestion of LLM traces directly into Datadog dashboards.
- **SigNoz** -- Open-source, OTel-native APM with growing LLM observability support, offering a self-hosted alternative to Datadog for teams that want full control over their telemetry pipeline.
- **Grafana Cloud** -- Published comprehensive guides for LLM observability using OpenTelemetry + Grafana stack (Tempo for traces, Loki for logs, Mimir for metrics).

### Tiered Logging Model

Requirements 13.1.2 and 13.1.5 establish a tiered logging architecture that has become industry best practice:

- **Tier 1 (Always):** Structured metadata -- timestamp, user ID, session ID, model version, token counts, input hash, safety filter outcome. Minimal storage cost, no privacy concerns.
- **Tier 2 (Conditional):** Full prompt/response content captured only on security-relevant triggers (safety filter activation, prompt injection detection, anomaly flags). Stored in access-restricted repositories with shorter retention.
- **Tier 3 (Consent-based):** Full content logging enabled by explicit user consent with documented legal basis (GDPR Article 6), typically for debugging or quality improvement programs.

### Content Capture Controls in Telemetry Pipelines

As of May 14, 2026, OpenTelemetry's GenAI span guidance still treats model instructions, user messages, and model outputs as sensitive, high-volume data that should not be captured by default. For production systems, the safer pattern is to keep operational spans metadata-only and, when content is required for a security trigger or explicit consent case, store the content in a separate repository with its own retention, access-control, encryption, and deletion policy. The telemetry span should carry only a content reference, classification label, consent or trigger reason, retention class, and hash.

Auditors should test this distinction directly: run a normal request, a safety-triggered request, and a consent-enabled debugging request, then compare exported OTel spans, log events, blob/object storage entries, and downstream observability views. The normal request should contain no prompt, response, retrieved document text, tool arguments, or resource payloads. The triggered or consent-enabled request should show a documented policy decision and a narrowly scoped content reference, not uncontrolled duplication of the same text across every trace backend. Langfuse masking functions and OTel collector processors are useful guardrails, but they should be treated as pre-export filters, not as permission to log raw content broadly.

### PII Redaction Pipeline

To meet the "no prompt or response content by default" clause in 13.1.2 and the consent-gated content capture in 13.1.5, teams need a redaction pipeline that runs **before** logs are written. The current best-practice pipeline combines multiple detection methods:

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

Both 13.1.3 (policy-decision logs) and 13.1.4 (interoperable schema) lose their value if log entries can be silently rewritten after the fact. Practical implementation options break down into two tiers:

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

As of May 11, 2026, the European Commission has announced a May 7 political agreement between the European Parliament and the Council of the EU on the Digital Omnibus on AI. The Commission's announcement says rules for stand-alone high-risk systems in areas such as biometrics, critical infrastructure, education, employment, migration, asylum, and border control will apply from **December 2, 2027**, while rules for AI systems integrated into regulated products such as lifts or toys will apply from **August 2, 2028**. The agreement still needs formal adoption and publication, so compliance teams should track the final Official Journal text, but the planning baseline has moved from the original August 2, 2026 high-risk date.

Article 12 requires that high-risk AI systems support automatic recording of events ("logs") throughout their lifecycle, with a level of traceability appropriate to the system's intended purpose. Key specifics:

- Logs must enable identification of situations where the system presents a risk or undergoes substantial modification
- Logs support post-market monitoring activities under Article 72
- Providers must keep automatically generated high-risk system logs under Article 19; sector-specific rules or final Omnibus text may impose longer periods for regulated industries
- For biometric identification systems: precise timestamps, reference database details, input data that triggered matches, and identification of verification personnel
- Article 13 requires deployers receive documentation explaining how to interpret and collect these logs -- effectively a technical integration manual, not just policy paperwork

Two words in Article 12 carry most of the interpretive weight: **"technically"** and **"automatic"**. "Technically" means the logging capability must be built into or layered onto the AI system itself -- not a manual CSV export run by an operator. "Automatic" means the system emits logs on its own as events happen, not on a scheduled batch. Together, these clauses rule out application architectures that rely on post-hoc reconstruction of activity from external sources.

Penalty structure under Article 99 is tiered. Non-compliance with Article 12's record-keeping obligations falls in the middle tier: up to **EUR 15 million or 3% of worldwide annual turnover**, whichever is higher. The headline-grabbing EUR 35M / 7% maximum applies specifically to violations of Article 5 (prohibited AI practices). Article 99 also requires proportionality, so startups and SMEs typically see reduced penalties.

No finalized harmonized technical standard for Article 12 logging exists yet, but two drafts are worth tracking:

- **prEN 18229-1** -- "AI trustworthiness framework -- Part 1: Logging, transparency and human oversight". Approved and under development by CEN-CENELEC JTC 21, providing terminology, concepts, requirements, and guidance for transparency, logging, and human oversight. First publication targeted in 2026.
- **ISO/IEC DIS 24970** -- "Artificial intelligence -- AI system logging". Specifies common capabilities, requirements, and a supporting information model for logging events in AI systems. As of April 29, 2026, ISO lists the project at stage 40.99, with the DIS approved for registration as an FDIS.

NIST SP 800-92 Rev. 1 is useful background for general cybersecurity log-management planning, but as of May 11, 2026 it remains an Initial Public Draft from October 2023 rather than final NIST guidance. Treat it as a planning playbook, not as a finalized compliance baseline.

Organizations deploying AI systems that fall under Annex III high-risk categories should evaluate their logging infrastructure against Article 12 now. Financial services providers can typically integrate AI logs into existing regulatory recordkeeping (MiFID II, DORA); other sectors must design AI-specific retention from scratch.

Organizations pursuing **ISO/IEC 42001** certification (the AI Management System standard) will find approximately 40-50% overlap with ISO 27001 governance processes, but AI-specific logging requirements go beyond traditional ISMS controls. ISO 42001 requires documented evidence of AI system behavior monitoring, risk assessment outputs, and performance tracking -- all of which depend on the structured logging infrastructure described in this section.

### Logging Threats: The Log-To-Leak Attack

A notable 2025 research paper ("Log-To-Leak: Prompt Injection Attacks on Tool-Using LLM Agents via Model Context Protocol") introduced a new class of privacy attacks targeting logging infrastructure in agentic systems. The attack uses indirect prompt injection to covertly force an agent to invoke a malicious logging tool, exfiltrating user queries, tool responses, and agent replies without degrading task performance -- making it difficult to detect through output quality monitoring alone.

The attack was evaluated across five real-world MCP servers and four frontier models (GPT-4o, GPT-5, Claude Sonnet, GPT-OSS-120b), consistently achieving high exfiltration success rates. The researchers systematized the injection prompt design space into four components: Trigger, Tool Binding, Justification, and Pressure.

Defensive implications for logging architecture:
- Tool permissions should enforce that only authorized logging components can write to log repositories
- MCP server configurations should restrict which tools can access logging endpoints
- Anomaly detection should flag unexpected logging tool invocations during agent workflows
- Content logging triggers (per 13.1.5) should be enforced at the infrastructure level, not the model level, since model-level controls can be bypassed by prompt injection

### Deserialization in the Logging Path: CVE-2025-68664 (LangChain Core)

A second class of logging-pipeline risk surfaced when **CVE-2025-68664** was published on December 23, 2025 (originally reported by Yarden Porat on December 4, 2025) against `langchain-core` versions <0.3.81 and ≥1.0.0 <1.2.5. The bug is a serialization-injection flaw in `dumps()` and `dumpd()`: dictionaries containing the reserved `lc` key are not escaped, so prompt-injected LLM output that lands in fields like `additional_kwargs` or `response_metadata` can be reconstructed as arbitrary `Serializable` subclasses when `load()`/`loads()` runs downstream. NIST scores it CVSS 8.2 (HIGH, vector `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N`); third-party advisories cite a 9.3 figure that pre-dates the NIST review. CWE-502 (Deserialization of Untrusted Data). The companion JavaScript advisory **CVE-2025-68665** covers `langchain.js`.

The advisory specifically calls out `LangSmithRunChatLoader` -- the LangSmith run loader that replays stored runs containing untrusted messages -- as a vulnerable consumer. That makes this directly a 13.1.1, 13.1.3, and 13.1.4 problem rather than just a framework bug:

- **The "logged content" travels through deserializers.** Anything captured under 13.1.5's "log full content on safety trigger" clause that later passes through a LangSmith replay, an evaluation harness, or a tracing backend that round-trips JSON can detonate the payload. The logging tier is the storage *and* the execution surface.
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

This incident has direct implications for the metadata-capture and interoperable-schema requirements (13.1.1 and 13.1.4) -- because once the proxy is compromised, every "structured" log entry it emits is attacker-controlled:

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

### API Gateway Authentication Logging: CVE-2026-42208

On **May 8, 2026**, NVD published **CVE-2026-42208** for LiteLLM Proxy versions 1.81.16 through 1.83.6, after the maintainer advisory and patch had already been released in April. The vulnerable API-key verification path mixed the caller-supplied bearer token into a database query, so an unauthenticated request to routes such as `/chat/completions` could reach SQL injection through the proxy's error-handling path. NVD scores it **9.8 CRITICAL** under CVSS 3.1 and lists it in CISA's Known Exploited Vulnerabilities catalog with a May 11, 2026 remediation due date; LiteLLM's maintainer advisory recommends upgrading to 1.83.7 or later, with 1.83.10-stable called out as the recommended stable build.

For request/response logging, the lesson is not just "patch LiteLLM." API gateways should record authentication outcomes in a way that supports incident response without retaining exploit strings or secrets: hashed key ID, tenant/project ID, route, auth decision, error class, proxy version, database role, request ID, source network context, and a normalized rejection reason. Raw `Authorization` values, virtual key material, upstream provider keys, and SQL fragments belong on the exclusion list. When a gateway processes LLM traffic for multiple tenants, failed-auth logs should also be checked for unusually long tokens, SQL metacharacters, and repeated route probing, but those detections should store indicators or hashes rather than full attacker payloads.

For audit evidence, ask for a staging replay of failed-auth requests that exercises both ordinary invalid tokens and tokens containing SQL metacharacters. The expected artifacts are:

- Application, proxy, and SIEM events with token hash or key fingerprint, token length bucket, route, tenant, request ID, proxy version, auth decision, and normalized rejection reason.
- No raw `Authorization` header, bearer-token body, SQL fragment, upstream provider key, virtual key, or master key in traces, spend logs, error logs, or alert payloads.
- Database audit logs showing parameterized token lookup on patched builds, plus a documented exception path for any temporary `disable_error_logs: true` containment period.

As of May 14, 2026, follow-on threat reporting makes the logging tradeoff sharper: Cloud Security Alliance summarized exploitation beginning within roughly 36 hours of public advisory indexing, with 17 UNION-based payload variants aimed at `LiteLLM_VerificationToken`, `litellm_credentials`, and `litellm_config`. For defenders, that means failed-auth telemetry should preserve enough signal to find SQL metacharacters, UNION-style probes, abnormal token length, route fan-out, source network changes, and unusual Postgres query activity, while still dropping bearer-token content before it reaches the log store. If an affected proxy was internet-reachable, review application logs, upstream gateway logs, Postgres query history, credential-table access, and outbound provider API usage together; any one of those streams alone can miss a successful read-only credential theft.

The maintainer advisory also names `disable_error_logs: true` under `general_settings` as a temporary workaround when an immediate upgrade is not possible, because it removes the vulnerable error-logging path. Treat that as an emergency containment measure only: it reduces forensic visibility exactly when exploitation may be active, so teams should pair it with upstream gateway logs, database audit logs, and a short deadline to move to a patched LiteLLM build.

### Cost Attribution and FinOps Logging

Token usage logging (requirements 13.1.1 and 13.1.4) increasingly serves a dual purpose: security monitoring and cost governance. The FinOps Foundation's 2026 guidance on AI cost management recommends:

- **Granular attribution tagging** -- stamp every inference request with project, team, feature, and environment metadata at the proxy layer, enabling cost-per-request and cost-per-feature reporting
- **Cache token tracking** -- with prompt caching now standard across major providers, logging `cache_creation.input_tokens` and `cache_read.input_tokens` (OTel GenAI v1.40.0 attributes) is necessary for accurate cost accounting
- **Anomaly detection on token consumption** -- sudden spikes in token usage per user or per session can indicate both abuse (prompt injection campaigns, model extraction attempts) and runaway agentic loops, making token monitoring a shared security/FinOps concern

Organizations implementing comprehensive token optimization based on logged usage data typically report 20-40% reductions in token consumption with minimal quality impact. The LLM proxy pattern (LiteLLM, Portkey, Helicone) has emerged as the standard architecture for centralized token tracking, though the LiteLLM breach demonstrates the supply chain risk of this centralization.

### Agentic System Logging

As AI systems evolve from single-inference APIs to multi-step agentic workflows, logging requirements expand significantly. The OpenTelemetry GenAI SIG is developing semantic conventions for agentic system observability, including:

- **`create_agent` spans** -- Capture agent initialization with `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.description`, and `gen_ai.agent.version`
- **`invoke_agent` spans** -- Track agent invocations with conversation context (`gen_ai.conversation.id`), input/output messages, and tool definitions
- **Tool execution spans** -- Record each tool call within an agent workflow, enabling reconstruction of multi-step reasoning chains
- **MCP spans** -- Capture JSON-RPC request IDs, method names, session IDs, protocol versions, client/server roles, and tool names for MCP tool traffic. OpenTelemetry recommends MCP-specific conventions over generic RPC or HTTP spans because one transport request can carry multiple MCP messages and streaming exchanges. Keep `mcp.resource.uri` and tool arguments opt-in because they can contain user files, database identifiers, and other high-cardinality sensitive data.

For security logging purposes, agentic workflows create additional challenges:
- Each tool invocation represents a potential privilege boundary crossing that should be logged
- Multi-agent systems (where agents delegate to other agents) need correlation IDs that span the full delegation chain
- Memory operations (reading from and writing to vector stores or conversation history) may expose sensitive data and should be logged with the same tiered approach as inference interactions
- The 2025 ServiceNow Now Assist vulnerability (second-order prompt injection through agent delegation) demonstrated that agent-to-agent interactions are a live attack surface requiring comprehensive logging
- The April 2026 MCP stdio command-injection disclosures, including **CVE-2026-30623** in LiteLLM's MCP server creation path, show that MCP server configuration changes are security events in their own right. Log actor identity, role, MCP server ID, transport, command basename, allowlist decision, validation error, and config hash; do not log full environment variables, command arguments containing secrets, or tool output by default.

### Audit Evidence Checklist

A practical 13.1 audit should ask for artifacts, not just logging policy text. The following evidence set maps cleanly to Article 12 traceability, ISO/IEC DIS 24970's AI-system logging model, NIST log-management planning, and the OpenTelemetry GenAI/MCP conventions:

- **Schema contract:** Versioned OTel/OpenInference attribute map showing required metadata fields, opt-in content fields, field owners, retention class, and stability status.
- **Content exclusion proof:** Three sample traces for normal, security-triggered, and consent-enabled requests showing that prompt text, response text, tool arguments, retrieved document text, system instructions, bearer tokens, and `mcp.resource.uri` are absent unless the documented trigger or consent path applies.
- **Pre-export filtering:** Collector, SDK, proxy, or Langfuse masking configuration demonstrating that redaction runs before telemetry leaves the application boundary, with unit tests for headers, API keys, PII, and structured tool payloads.
- **Security-event capture:** Sample policy-decision, guardrail, prompt-injection, anomaly, failed-auth, and MCP tool-call events with rule ID, decision outcome, confidence or score, actor, tenant, route, tool name, request ID, and normalized error class.
- **Replay boundary:** Documentation showing whether stored runs are ever deserialized for debugging, evaluation, or replay, plus dependency pins and allowlists for LangChain/LangSmith-style loaders that may reconstruct stored messages.
- **Integrity controls:** Evidence that inference logs are covered by immutable storage, retention locks, signing, hash chaining, or equivalent tamper-evidence, with a recent test showing unauthorized modification is detected.
- **Access review:** Current access list for trace backends, full-content stores, SIEM exports, and spend dashboards, including justification for anyone who can view conditional content captures.
- **Operational drill:** A recent exercise that traces one suspicious request across application logs, OTel spans, proxy auth logs, database audit logs, and downstream provider usage, confirming correlation IDs survive each hop without copying raw user content.

---

## Related Standards & References

- **OpenTelemetry GenAI Semantic Conventions** -- Development-status semantic conventions defining the standard schema for AI observability telemetry ([opentelemetry.io/docs/specs/semconv/gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/))
- **OpenTelemetry GenAI Semantic Conventions Repository** -- Separate GenAI conventions repository advertising schema URL 1.42.0 and reference implementation material ([github.com/open-telemetry/semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai))
- **OpenTelemetry GenAI Client Spans** -- Shows that prompt, response, retrieval query, and message content fields are sensitive/opt-in and should be version-pinned before deployment ([opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/))
- **OpenTelemetry GenAI Agent Span Conventions** -- Emerging conventions for agentic system observability ([opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/))
- **OpenTelemetry MCP Semantic Conventions** -- Development-status client/server spans and metrics for Model Context Protocol JSON-RPC traffic, compatible with GenAI tool execution spans ([opentelemetry.io/docs/specs/semconv/gen-ai/mcp](https://opentelemetry.io/docs/specs/semconv/gen-ai/mcp/))
- **OpenLLMetry** -- Open-source OTel-based instrumentation for LLM applications, adopted by Dynatrace and others ([traceloop.com](https://www.traceloop.com/docs/openllmetry/contributing/semantic-conventions))
- **OpenInference** -- OTel-compatible AI observability conventions and instrumentation used by Phoenix and Arize for LLM, retrieval, tool, agent, and session tracing ([arize-ai.github.io/openinference](https://arize-ai.github.io/openinference/), [semantic conventions](https://arize-ai.github.io/openinference/spec/semantic_conventions.html))
- **Datadog LLM Observability with OTel** -- Native GenAI semantic convention support announced at DASH 2025 ([datadoghq.com](https://www.datadoghq.com/blog/llm-otel-semantic-convention/))
- **Grafana LLM Observability Guide** -- Complete guide to LLM monitoring with OTel and Grafana Cloud ([grafana.com](https://grafana.com/blog/a-complete-guide-to-llm-observability-with-opentelemetry-and-grafana-cloud/))
- **OWASP Logging Cheat Sheet** -- General logging best practices applicable to AI systems
- **OWASP LLM Top 10** -- LLM02:2025 Sensitive Information Disclosure covers prompt/response PII leakage; LLM06:2025 Excessive Agency covers agent misuse of tools, including unauthorized logging tools ([LLM02](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/), [LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/))
- **Microsoft Presidio** -- Open-source PII detection and redaction framework with analyzer/anonymizer modules for text and structured data ([github.com/microsoft/presidio](https://github.com/microsoft/presidio), [text anonymization docs](https://microsoft.github.io/presidio/text_anonymization/))
- **LLM Guard** (Protect AI) -- Security toolkit combining PII anonymization, secrets detection, prompt-injection detection, and output validation ([protectai.com/llm-guard](https://protectai.com/llm-guard), [anonymize scanner docs](https://protectai.github.io/llm-guard/input_scanners/anonymize/))
- **Langfuse** -- Open-source LLM observability with tracing, prompt management, security guardrail integration, and pre-ingestion masking hooks ([langfuse.com](https://langfuse.com/docs/security-and-guardrails), [masking docs](https://langfuse.com/docs/observability/features/masking))
- **NIST SP 800-92 Rev. 1** (Draft) -- Cybersecurity Log Management Planning Guide, updating the original 2006 publication ([csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd))
- **EU AI Act Article 12** -- Record-keeping requirements for high-risk AI systems, including automatic lifecycle logging for traceability, risk identification, and post-market monitoring ([ai-act-service-desk.ec.europa.eu](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-12), practical walkthrough at [helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements](https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/))
- **Digital Omnibus on AI Agreement (May 7, 2026)** -- European Commission announcement that the political agreement moves stand-alone high-risk systems to December 2, 2027 and product-integrated systems to August 2, 2028, pending formal adoption ([digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/news/eu-agrees-simplify-ai-rules-boost-innovation-and-ban-nudification-apps-protect-citizens))
- **OpenTelemetry Semantic Conventions v1.41.1 / v1.41.0 Releases** -- May 11, 2026 maintenance release plus the April 28, 2026 GenAI release adding reasoning-token accounting, streaming attributes, `gen_ai.client.operation.exception`, and split client/internal `invoke_agent` spans ([github.com/open-telemetry/semantic-conventions/releases](https://github.com/open-telemetry/semantic-conventions/releases))
- **prEN 18229-1** -- Draft CEN-CENELEC AI trustworthiness framework Part 1 covering logging, transparency, and human oversight ([aistandardshub.org](https://aistandardshub.org/ai-standards/ai-trustworthiness-framework-part-1-logging-transparency-and-human-oversight/))
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
- **CVE-2026-42208 (LiteLLM Proxy SQL Injection)** -- Critical pre-authentication SQL injection in LiteLLM Proxy API-key verification, added to CISA KEV on May 8, 2026; relevant to safe logging of failed auth events and bearer-token handling ([nvd.nist.gov/vuln/detail/CVE-2026-42208](https://nvd.nist.gov/vuln/detail/CVE-2026-42208), maintainer update at [docs.litellm.ai/blog/cve-2026-42208-litellm-proxy-sql-injection](https://docs.litellm.ai/blog/cve-2026-42208-litellm-proxy-sql-injection), GitHub advisory at [github.com/BerriAI/litellm/security/advisories/GHSA-r75f-5x8p-qvmc](https://github.com/BerriAI/litellm/security/advisories/GHSA-r75f-5x8p-qvmc))
- **CSA Research Note on CVE-2026-42208** -- Summarizes exploitation timing, targeted LiteLLM credential tables, and incident-response actions for internet-facing AI proxy deployments ([labs.cloudsecurityalliance.org](https://labs.cloudsecurityalliance.org/research/csa-research-note-litellm-cve-2026-42208-ai-proxy-sqli-20260/))
- **CVE-2026-30623 (LiteLLM MCP stdio command injection)** -- Authenticated RCE through MCP server creation/update and preview endpoints, useful as a logging checklist for MCP configuration events and validation failures ([docs.litellm.ai/blog/mcp-stdio-command-injection-april-2026](https://docs.litellm.ai/blog/mcp-stdio-command-injection-april-2026), OX advisory at [ox.security](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/))
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
- How should organizations reconcile Article 19/sector-specific log retention expectations with GDPR's data minimization principle when AI interaction logs contain redacted-but-reconstructable personal data?
- What are the forensic implications of running multiple model versions simultaneously (A/B testing, canary deployments)? How should log correlation handle version-specific behavioral differences?
- How should organizations secure LLM proxy gateways (LiteLLM, Portkey, Helicone) that centralize logging, given that the March 2026 LiteLLM supply chain attack demonstrated that compromising the proxy gives attackers access to all API keys and inference traffic? Is the centralized proxy pattern worth the single-point-of-failure risk?
- What is the right retention pattern for failed-auth telemetry after CVE-2026-42208: enough detail to detect active exploitation and support database triage, but not enough raw bearer-token content to preserve secrets or exploit payloads in the logging tier?
- As prompt caching becomes standard, how should logging schemas account for the distinction between cache hits and fresh inference for both cost attribution and security analysis? Cache hits may mask repeated adversarial probing if not properly tracked.
- How should the industry treat the deserialization boundary on stored conversation logs after CVE-2025-68664? Replay-based evaluation, A/B test rerunning, and human-in-the-loop debug review all reconstruct stored messages, which means every "log full content" capture point is a potential code path. Should evaluation harnesses by default operate on metadata + redacted text rather than reconstructed message objects, even at the cost of less faithful replay?

---

## Related Pages

- [C14.3 Chain of Responsibility & Auditability](../C14-Human-Oversight/C14-03-Chain-of-Responsibility-Auditability.md) -- Connects request/response telemetry to accountable human review, tool execution evidence, and traceable responsibility for high-impact actions.
- [C9.9 Data Flow Isolation & Origin Enforcement](../C09-Orchestration-and-Agents/C09-09-Data-Flow-Isolation-Origin-Enforcement.md) -- Uses request, origin, and tool-call telemetry to prove that untrusted content cannot silently steer privileged agent actions.
- [C10.5 Outbound Access & Agent Execution Safety](../C10-MCP-Security/C10-05-Outbound-Access-Agent-Safety.md) -- Extends tool-call telemetry into gateway-layer controls for SSRF, cloud metadata access, denial-of-wallet loops, and human approval.
- [C13.6 Proactive Security Behavior Monitoring](C13-06-Proactive-Security-Behavior-Monitoring.md) -- Consumes the same request/response and tool-call events to detect suspicious multi-step behavior before it becomes an incident.
- [C2.1 Prompt Injection Defense](../C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) -- Supplies the input validation and injection-detection signals that should trigger conditional content capture and safety-event logging.

---
