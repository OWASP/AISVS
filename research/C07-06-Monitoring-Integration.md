# C7.6 Monitoring Integration

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Monitoring integration ensures that the safety and security controls defined throughout C7 produce observable signals that security teams can act on. Without integrated monitoring, safety violations (hallucinations, PII leaks, toxic outputs, filter bypasses) occur silently. This section requires real-time metrics, alerting on anomalous patterns, and sufficient log detail to support incident investigation. These controls bridge the gap between per-request safety checks and organizational security operations.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **7.6.1** | **Verify that** the system logs real-time metrics for safety violations (e.g., "Hallucination Detected", "PII Blocked"). | 1 | **Invisible safety failures (MITRE ATLAS AML.T0015 — Evade ML Model).** Without real-time metrics, security teams have no visibility into whether safety controls are working, how often they trigger, or whether attack patterns are emerging. A safety filter that triggers 1000 times per hour might indicate a coordinated attack — but without metrics, no one knows. GreyNoise research documented 91,000+ attack sessions targeting exposed LLM services between October 2025 and January 2026, underscoring the volume of attacks that go unnoticed without proper metrics. The Netskope Cloud and Threat Report 2026 found that organizations average 223 GenAI data policy violations per month (rising to 2,100/month in the top quartile), yet 50% lack enforceable data protection policies for GenAI apps — violations go undetected. Bright Security's 2026 State of LLM Security report and multiple independent audits put the prevalence of prompt injection vulnerabilities at roughly 73% of production AI deployments as of Q1 2026, which means most teams are missing the signal they need most. Adversaries increasingly use multi-language encoding, Base64 obfuscation, and URL-fragment smuggling (Microsoft documented a `#IGNORE_PREVIOUS_INSTRUCTIONS`-style hidden-fragment pattern in its March 2026 prompt abuse playbook) to evade safety filters silently, making metric emission from every filter stage essential. | Trigger various safety violation types (format rejection, hallucination detection, PII redaction, content filter block) and confirm each produces a corresponding metric entry. Verify metrics are available in near-real-time (within seconds, not batch-processed daily). Confirm metrics include event type, timestamp, and severity. Validate instrumentation against the OpenTelemetry GenAI Semantic Conventions (still experimental as of Semantic Conventions v1.40.0, released February 19, 2026): verify that `gen_ai.client.token.usage` and `gen_ai.client.operation.duration` metrics are emitted with required attributes (`gen_ai.operation.name`, `gen_ai.system`). For cache-sensitive workloads, confirm the newer `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_creation.input_tokens` attributes introduced in v1.40.0 are captured so prompt-cache abuse and billing-overrun patterns become visible. Use OpenTelemetry-based instrumentation (OpenLLMetry, SigNoz) to verify metrics flow into the observability pipeline. Confirm safety events from C7.1-C7.5 and C7.7-C7.8 all emit structured metrics. Cross-reference with Confident AI's production safety evaluators (toxicity, bias, PII detection) or Comet Opik's guardrail PII redaction logs to validate coverage. For teams already on Datadog, confirm OTel GenAI spans flow through the Agent in OTLP mode without code changes (v1.37+) and that an OTel Collector processor applies redaction/sampling before telemetry leaves the network. | Standard observability stacks (Prometheus/Grafana, Datadog, Splunk, ELK) can ingest these metrics. AI-specific platforms like Langfuse (open-source, OpenTelemetry-native), Arize Phoenix (OSS — prompt management module added April 2025), and LangSmith provide specialized dashboards for model behavior monitoring. As of April 2026, OpenTelemetry GenAI Semantic Conventions v1.40.0 remain experimental: the release added retrieval spans for RAG lookups, server-side tool-execution attributes, `gen_ai.agent.version` for agent iteration tracking, and cache-token metrics, while restructuring error handling into domain-specific exception events (replacing the generic `error.message`) — schema migration is still ongoing. Provider-specific conventions exist for OpenAI, Anthropic, AWS Bedrock, and Azure AI Inference. Datadog natively supports these conventions from v1.37 onward and now ingests AWS Strands Agents spans (model inferences, planner steps, tool invocations, agent hand-offs) directly. Confident AI offers 50+ evaluation metrics (open-sourced through DeepEval). SigNoz provides OpenTelemetry-native full-stack observability with trace-to-log correlation. The gap remains that no single platform combines comprehensive safety guardrails with OpenTelemetry-native design at an accessible price point — most teams layer safety-specific tools on top of general tracing infrastructure. The GenAI semantic conventions are still experimental and no transition to Release Candidate or Stable status has been announced as of v1.40.0, so teams should plan for continued schema migration. |
| **7.6.2** | **Verify that** the system triggers an alert if safety violation rates exceed a defined threshold within a specific time window. | 2 | **Undetected attack campaigns (OWASP LLM Top 10 2025 — LLM01: Prompt Injection).** Individual safety violations may be benign (a user accidentally triggering a filter). But a spike in violations — especially from a single user, IP range, or targeting a specific filter — likely indicates an active attack (prompt injection campaign, PII extraction attempt, jailbreak effort). The January 2026 "Reprompt" attack (Varonis Threat Labs) demonstrated single-click data exfiltration from Microsoft Copilot Personal using parameter-to-prompt injection — the attacker maintained control even after the Copilot chat was closed, and all commands were delivered from a remote server after the initial prompt, making it impossible to detect exfiltration by inspecting the starting prompt alone. The February 17, 2026 "Clinejection" supply-chain attack is the more consequential lesson for rate-based alerting: researcher Adnan Khan's earlier disclosure showed an indirect prompt injection in a GitHub issue title driving Cline's AI triage workflow, which was then chained through GitHub Actions cache poisoning to steal a nightly npm publish token. Attackers republished `cline@2.3.0` with a malicious `postinstall` hook that pulled OpenClaw onto roughly 4,000 developer and CI/CD machines during an eight-hour window. The triage workflow had been processing adversarial input at scale; without alerts on anomalous tool invocations, writes by the AI bot, or unusual artifact/credential access patterns, the pivot from issue-triage to privileged-publish workflow went unnoticed. Rate-based and behavioral alerting would have caught the shift. A late-2025 ServiceNow case demonstrated "second-order" prompt injection where a low-privilege agent was tricked into escalating via a higher-privilege agent — these cross-agent attack chains produce characteristic violation patterns that rate-based alerting can catch. | Configure alert thresholds (e.g., >50 PII redactions per hour, >20 content filter blocks per user per hour, >200 API calls/minute, error rate ≥5%). Simulate a burst of safety violations exceeding the threshold. Verify an alert is generated and delivered to the appropriate channel (PagerDuty, Slack, email, SIEM). Confirm alert includes sufficient context for triage (violation type, user ID, time window, count). Test with CrowdStrike Falcon AIDR (reports 98.7% prompt injection detection rate as of early 2026) or signature-based log scanners that flag patterns like "ignore previous instructions" and "disregard all rules." Validate that multi-signal correlation works — e.g., violation spike + anomalous token usage + unusual tool invocation sequence triggers a higher-severity alert than any single signal alone. For agentic systems, verify alerting covers OpenTelemetry GenAI agent span attributes (`gen_ai.agent.name`, `gen_ai.agent.id`, `gen_ai.agent.version` added in v1.40.0) so cross-agent escalation patterns (as in the ServiceNow incident) can be correlated across agent boundaries. For AI-in-the-CI/CD loop (Cline/Clinejection pattern), validate alerting on anomalous agent-initiated writes, tool or workflow invocations outside the agent's baseline, and credential or artifact access events — Microsoft's March 2026 playbook recommends correlating these signals in Sentinel with Defender for Cloud Apps detections of unsanctioned AI tool usage. | Threshold tuning is critical. Too low produces alert fatigue; too high misses real attacks. Practical thresholds from production deployments (as of 2026): API call frequency >200 calls/minute, error rate ≥5%, failed login attempts ≥20/hour, log volume >1 GB/hour. Consider adaptive thresholds that adjust based on baseline violation rates. Correlating violation spikes with specific user sessions or IP addresses supports rapid incident response. Anomaly detection models tracking unexpected shifts in output patterns (e.g., sudden spikes in prompt complexity, repeated requests for sensitive topics, excessive tool calls, or data access immediately followed by external HTTP requests) provide stronger signal than static thresholds alone. The Reprompt attack's "chain-request" technique — where each Copilot response generates the next exfiltration request — highlights the need for alerting on recursive or self-referencing request patterns, not just volume spikes. The Clinejection incident reinforces that agent-driven pipelines need alerts tied to workflow/artifact/credential state transitions, not only prompt-level metrics: any alert ruleset that assumes the AI surface is a chat box will miss supply-chain compromises where the "user" is an untrusted GitHub issue and the "action" is an npm publish. |
| **7.6.3** | **Verify that** logs include the specific model version and other details necessary to investigate potential abuse. | 2 | **Inability to reproduce or investigate incidents (NIST AI RMF "Measure" function — traceability).** If a safety incident occurs but logs do not record which model version, prompt template, or configuration was active, investigators cannot determine whether the issue was a model-level problem, a configuration error, or an adversarial attack. This is especially critical when models are frequently updated. Shadow AI — GenAI tools accessed via personal, unmanaged accounts — represents a major blind spot: the Netskope Cloud and Threat Report 2026 found 47% of GenAI users access tools via personal accounts, bypassing enterprise logging entirely, with GenAI app usage tripling and prompt volume increasing sixfold year-over-year. Without version-tagged logs, organizations cannot show the audit trail linking outputs to source data, model versions, and user prompts that NIST expects. The EU AI Act's Annex III high-risk obligations take effect August 2, 2026, and Article 12 requires high-risk systems to "technically allow for the automatic recording of events (logs) over the lifetime of the system" across three explicit categories: (a) situations where the system might present a risk or undergo a substantial modification, (b) post-market monitoring data, and (c) data for operational monitoring by deployers. Article 19 and Article 26 establish a minimum six-month retention for deployer-retained logs, and penalties for non-compliance with high-risk obligations reach EUR 15 million or 3% of global annual turnover — with the GPAI/prohibited-use tier reaching EUR 35 million or 7% for the most serious violations. ISO 42001 Clause 9 requires ongoing risk monitoring with audit-ready logging. A 2025 Deloitte report found companies with full audit trails had 38% higher stakeholder trust scores, and Gartner predicts 75% of large enterprises will require certified logs as a procurement condition by Q3 2026. | Review log entries for safety events and confirm they include: model version/identifier, prompt template version (if applicable), inference parameters (temperature, top_p, etc.), timestamp, request ID, and user/session identifier. For agentic systems, also verify that logs capture `gen_ai.agent.id`, `gen_ai.agent.version` (added in Semantic Conventions v1.40.0), `gen_ai.conversation.id`, and `gen_ai.tool.definitions` per OTel GenAI agent span conventions — these are essential for reconstructing multi-agent incident chains. Verify logs are retained at least six months for EU AI Act Article 19/26 compliance and longer where sector regulations require. Use centralized log analysis (Elasticsearch 9.3/Kibana 9.3, Loki 3.6.6 with OpenTelemetry integration, or SigNoz for 2.5x faster ingestion) to correlate safety events across model versions. Confirm that Langfuse session replays, LangSmith trace views, or Datadog LLM Observability's Strands Agents integration can reconstruct the full request context (including agent hand-offs and tool invocations) for any flagged safety event. Validate logs are structured, immutable, and tamper-evident — EU AI Act does not explicitly demand tamper-proof logs, but regulators will not accept unverifiable records, so practice is converging on cryptographic signing performed **outside** the agent's trust boundary, with chained signatures and external receipt storage. Confirm that model version, policy version, and configuration version are all tied to each run, enabling rollback analysis when incidents correlate with deployments. Confirm Article 13 technical documentation explaining log schema and interpretation exists — regulators expect a systems-integration guide, not just the logs themselves. | Model version tracking becomes essential in environments with frequent model updates (A/B testing, canary deployments, fine-tune iterations). Without version-tagged logs, a spike in hallucinations after a model update cannot be attributed to the update. Relates to C3 (Model Lifecycle Management) for version tracking. NIST IR 8596 (Cybersecurity Framework Profile for AI, 2025) emphasizes logging that links outputs to source data and model versions. Key metrics to track per NIST guidance: mean time to detect (MTTD) for AI-specific threats, percentage of models covered by security controls, adversarial test coverage, and incident response times. The distinction between operational logging and compliance-grade audit trails matters: logging captures operational data for debugging, while audit trails are structured, immutable, and designed to demonstrate what happened and why to regulators. For EU AI Act compliance, organizations need both. Deployers often miss that the six-month floor is exactly that — a floor — and that financial-services, medical-device, and critical-infrastructure sectors may be subject to longer sector-specific retention that supersedes Article 19. A practical failure mode in 2026: logs are retained but the system cannot regenerate a forensic trace because `gen_ai.agent.version` or prompt-template versions were not persisted, so auditors cannot tell which agent configuration produced a flagged output. ISO 42001 Clause 9 (Performance evaluation) mandates ongoing risk monitoring, bias audits, and transparency reporting — model version-tagged logs are the technical foundation. |

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

### OpenTelemetry GenAI Semantic Conventions

As of March 2026, OpenTelemetry has released experimental GenAI Semantic Conventions that standardize how LLM spans, metrics, and events are named and attributed across different tools. This is a significant development for C7.6 compliance because it addresses the historical fragmentation where every LLM observability tool used incompatible custom tracing formats.

**Core Metrics (Experimental):**

| Metric | Instrument | Unit | What It Measures |
|--------|-----------|------|-----------------|
| `gen_ai.client.token.usage` | Histogram | `{token}` | Input and output tokens consumed per operation |
| `gen_ai.client.operation.duration` | Histogram | `s` | End-to-end GenAI operation latency |
| `gen_ai.server.request.duration` | Histogram | `s` | Server-side time-to-last-byte or last output token |
| `gen_ai.server.time_per_output_token` | Histogram | `s` | Decode-phase token generation speed |
| `gen_ai.server.time_to_first_token` | Histogram | `s` | Queue + prefill latency for streaming requests |

**Required Attributes:** `gen_ai.operation.name` (chat, embeddings, text_completion) and `gen_ai.system` (provider name). Conditionally required: `error.type` on failures.

**Provider-Specific Conventions:** Definitions exist for OpenAI, Anthropic, AWS Bedrock, and Azure AI Inference — so instrumentation libraries can emit standardized telemetry regardless of which LLM provider is used.

**Agentic System Conventions (Draft):** OpenTelemetry is actively defining conventions for AI agent observability, with draft semantic conventions for agent frameworks (CrewAI, AutoGen, LangGraph, IBM Bee Stack). Key agent-specific attributes include:

- `gen_ai.agent.name` / `gen_ai.agent.id` / `gen_ai.agent.version` — agent identity
- `gen_ai.conversation.id` — session/thread correlation
- `gen_ai.tool.definitions` — tool availability tracking
- `gen_ai.data_source.id` — RAG data source attribution

The conventions define **tasks** (minimal trackable units of work) and **actions** (execution mechanisms: tool calls, LLM queries, API requests, vector DB queries, human input). This structure enables tracing cross-agent delegation chains — directly relevant to detecting multi-agent escalation attacks like the ServiceNow incident.

**Adoption Status:** Datadog natively supports OTel GenAI conventions from v1.37 onward and as of 2026 ingests AWS Strands Agents spans directly — including model inferences, planner steps, tool invocations, and agent hand-offs — through the Datadog Agent in OTLP mode, with no code changes required. Teams using the OpenTelemetry Collector can apply processors for redaction, sampling, enrichment, and routing so data-governance policies are enforced before telemetry leaves the network. The conventions remain experimental (v1.40.0, released February 19, 2026) and no transition to Release Candidate or Stable status has been announced; v1.40.0 specifically introduced retrieval spans for RAG, server-side tool-execution attributes, `gen_ai.agent.version`, and cache-token metrics, while restructuring error handling into domain-specific exception events (replacing generic `error.message`). Teams should use the latest SDK versions and plan for continued schema migration.

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
- **Hidden URL fragments and metadata smuggling**: Microsoft's March 2026 prompt abuse playbook documents indirect injection via hidden URL fragments (e.g., `#IGNORE_PREVIOUS_INSTRUCTIONS`) that tools automatically inline into prompts without sanitization. The recommended detection path is to correlate CloudAppEvents (unsanctioned AI tool usage), Purview DLP interactions on sensitive data, and Defender for Cloud Apps telemetry inside Microsoft Sentinel, then apply Entra ID conditional access to restrict tool/device combinations.
- **AI-in-CI/CD anomaly signals (Clinejection pattern)**: For agent-driven build or triage pipelines, alert on agent-initiated writes outside its baseline file scope, workflow invocations the agent has never triggered before, artifact or cache modifications adjacent to publish workflows, and credential access events from agent identities. These are not prompt-level signals and will be missed by a monitoring stack that only watches chat traffic.

### Compliance and Regulatory Mapping

As of March 2026, several regulatory frameworks impose specific monitoring and logging requirements on AI systems that C7.6 directly supports:

**EU AI Act (High-Risk Systems — effective August 2, 2026):**
- Articles 9-15 require risk management, technical documentation, human oversight, and accuracy monitoring
- **Article 12 (Record-Keeping)** requires systems to "technically allow for the automatic recording of events (logs) over the lifetime of the system." Article 12(2) defines three explicit log categories: (a) situations where the system might present a risk or undergo a substantial modification, (b) post-market monitoring data, and (c) data for operational monitoring by deployers
- **Article 13** requires deployer-facing documentation explaining log collection and interpretation — effectively a systems-integration guide, not pure compliance paperwork
- **Articles 19 and 26** set a six-month minimum retention for deployer-controlled logs; sector-specific regulations (finance, medical, critical infrastructure) may impose longer periods
- Annex III triggers for AI agents include credit scoring, resume filtering, healthcare benefit decisions, insurance pricing, and emergency-call triage — integrators who deploy a general-purpose model into any of these contexts inherit provider-level obligations
- High-risk AI systems must maintain log records sufficient to trace outputs to inputs, model versions, and data sources
- Penalties scale by violation tier: up to EUR 15 million or 3% of global annual turnover for high-risk non-compliance, up to EUR 35 million or 7% for prohibited-use violations
- Tamper-evidence is an implicit regulator expectation even though Article 12 does not use the word "tamper-proof" — 2026 industry practice is converging on cryptographic signing performed outside the agent's trust boundary, with chained signatures and external receipt storage so logs can survive agent compromise
- ISO 42001 certification demonstrates systematic compliance (approximately 40-50% overlap with EU AI Act requirements) but does not guarantee full compliance

**ISO 42001 (AI Management System):**
- Clause 9 (Performance evaluation) mandates ongoing risk monitoring, bias audits, and transparency reporting
- Requires continuous monitoring of deployed AI systems to detect drift, accuracy degradation, and fairness violations
- Implementation should include AI-specific due diligence questionnaires covering training data governance, model governance, and logging

**NIST AI RMF and IR 8596:**
- The "Measure" function requires baseline metrics for drift, bias, and adversarial robustness
- IR 8596 (Cybersecurity Framework Profile for AI, 2025) specifies logging that links outputs to source data, model versions, and user prompts
- Key metrics: MTTD for AI-specific threats, percentage of models covered by security controls, adversarial test coverage, incident response times

**Practical Compliance Checklist for C7.6:**

| Obligation | C7.6 Requirement | Evidence |
|-----------|------------------|----------|
| Output traceability | 7.6.1 + 7.6.3 | Safety metric logs with model version, request ID, timestamp |
| Incident detection | 7.6.2 | Alert rules with defined thresholds, alert delivery evidence |
| Audit trail integrity | 7.6.3 | Immutable, cryptographically signed log entries |
| Continuous monitoring | 7.6.1 | Real-time dashboards showing safety signal trends |
| Version accountability | 7.6.3 | Model version + config version tagged in every log entry |

### Audit Trail Architecture

The distinction between operational logging and compliance-grade audit trails is important for organizations approaching C7.6 from a regulatory perspective:

- **Operational logs** capture debugging data — useful for engineering but not audit-ready. They may be ephemeral, unstructured, and lack integrity controls.
- **Audit trails** are structured, immutable, and compliance-focused — designed to demonstrate what happened and why to regulators and auditors. They require cryptographic hashing, signed events, immutable storage settings, and strict access policies.

For C7.6.3 compliance, organizations need both: operational logs for rapid incident investigation and audit trails for regulatory evidence. Best practices include:

- Tie model version, policy version, and configuration version to each run
- Use append-only storage with cryptographic integrity verification
- Retain logs for the duration required by applicable regulations (EU AI Act does not specify a minimum, but organizational policy should define retention based on incident investigation needs)
- Ensure logs are queryable — auditors need to reconstruct decision chains, not just prove logs exist

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
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — standardized spans, metrics, and events for generative AI systems (experimental, March 2026)
- [OpenTelemetry GenAI Metrics Specification](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/) — token usage, operation duration, and server-side latency metrics
- [OpenTelemetry GenAI Agent Span Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) — agent identity, conversation correlation, and tool definitions for agentic systems
- [Datadog OTel GenAI Support](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) — native support for OpenTelemetry GenAI Semantic Conventions (v1.37+)
- [Varonis Reprompt Attack Disclosure](https://www.varonis.com/blog/reprompt) — single-click data exfiltration from Microsoft Copilot via parameter-to-prompt injection (January 2026)
- [Netskope Cloud and Threat Report 2026](https://www.netskope.com/resources/cloud-and-threat-reports/cloud-and-threat-report-2026) — GenAI data policy violations doubled, 47% shadow AI usage, 223 incidents/month average
- [EU AI Act High-Risk AI System Requirements (August 2026)](https://ucomply.cloud/en/blog/ai-act-augustus-2026-hoog-risico-verplichtingen/) — logging and documentation obligations for high-risk systems
- [ISO 42001 Implementation Guide 2026](https://secureprivacy.ai/blog/iso-42001-implementation-guide-2026) — AI management system with Clause 9 monitoring requirements
- [Microsoft AI Observability for Security (March 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/18/observability-ai-systems-strengthening-visibility-proactive-risk-detection/) — visibility into AI behavior for proactive risk detection
- [Audit Logs in AI Systems (Latitude)](https://latitude.so/blog/audit-logs-in-ai-systems-what-to-track-and-why) — practical guidance on audit trail architecture for AI
- [Microsoft: Detecting and Analyzing Prompt Abuse in AI Tools (March 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/12/detecting-analyzing-prompt-abuse-in-ai-tools/) — prompt abuse detection playbook covering Sentinel, Purview DLP, Defender for Cloud Apps, and Entra ID correlation
- [EU AI Act Article 12 — Record-Keeping](https://artificialintelligenceact.eu/article/12/) — high-risk AI logging obligations across risk/modification events, post-market monitoring, and operational monitoring
- [EU AI Act Article 26 — Deployer Obligations](https://artificialintelligenceact.eu/article/26/) — deployer responsibilities including six-month log retention
- [Help Net Security: EU AI Act Logging Requirements for AI Agents (April 2026)](https://www.helpnetsecurity.com/2026/04/16/eu-ai-act-logging-requirements/) — Article 12 interpretation for agentic systems, tamper-evidence gap analysis
- [OpenTelemetry Semantic Conventions v1.40.0 Release (February 2026)](https://github.com/open-telemetry/semantic-conventions/releases) — retrieval spans, cache token metrics, agent versioning, and error-handling restructure
- [Datadog: OpenTelemetry GenAI Semantic Conventions Support](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) — native OTel ingestion via Agent in OTLP mode, Collector-based redaction and sampling
- [Datadog + AWS Strands Agents](https://www.datadoghq.com/blog/llm-aws-strands/) — OTel-compliant span ingestion for agent lifecycle (model inference, planner steps, tool invocations, hand-offs)
- [Snyk: Clinejection Supply Chain Attack Analysis (February 2026)](https://snyk.io/blog/cline-supply-chain-attack-prompt-injection-github-actions/) — technical writeup of AI triage bot turned into supply chain vector
- [Adnan Khan: Clinejection Disclosure](https://adnanthekhan.com/posts/clinejection/) — original researcher writeup of the Cline AI triage compromise
- [The Hacker News: Cline CLI 2.3.0 Supply Chain Attack (February 2026)](https://thehackernews.com/2026/02/cline-cli-230-supply-chain-attack.html) — OpenClaw installation through compromised npm token
- [Bright Security: 2026 State of LLM Security](https://brightsec.com/blog/the-2026-state-of-llm-security-key-findings-and-benchmarks/) — prompt injection prevalence and production LLM security benchmarks

---

## Real-World Incidents & Lessons

- **Clinejection — AI Triage Bot as Supply-Chain Attack Vector (February 17, 2026):** Security researcher Adnan Khan disclosed a vulnerability chain (late December 2025, published February 9, 2026) in Cline, a popular open-source AI coding assistant, in which an attacker could plant an indirect prompt injection in a GitHub issue title. Cline's AI-powered issue triage workflow would then execute attacker-influenced steps, and through GitHub Actions cache poisoning the attack pivoted into the privileged Publish Nightly Release and Publish NPM Nightly workflows, exposing credentials. Khan filed a GHSA and notified Cline on January 1, 2026, but credential rotation was incomplete: on February 17 at 03:26 PT an unknown actor used a still-active npm token (the wrong token had been revoked on February 9) to publish `cline@2.3.0` with a single malicious modification — `{ "postinstall": "npm install -g openclaw@latest" }` — causing the Cline CLI to install the OpenClaw autonomous agent on roughly 4,000 developer and CI/CD machines during an eight-hour window (until 11:30 PT). Cline released `2.4.0`, deprecated `2.3.0`, revoked the compromised token, and moved npm publishing to OIDC via GitHub Actions. For C7.6 monitoring, the incident is a clean proof that metric emission and alerting must cover every AI agent action — tool invocations, workflow triggers, artifact and credential access — not just chat-style prompts and responses. Signals that would have caught the pivot: anomalous writes from the triage bot, tool invocations outside baseline, credential access from a workflow not in the agent's normal footprint, and a spike in agent-initiated actions against CI cache artifacts.
- **Reprompt Attack — Single-Click Copilot Exfiltration (January 2026):** Varonis Threat Labs disclosed the "Reprompt" attack against Microsoft Copilot Personal, enabling single-click data exfiltration. The attack used parameter-to-prompt (P2P) injection via the URL `q` parameter, a "double-request" technique to bypass data-leak safeguards (which only applied to initial requests), and a "chain-request" technique where each Copilot response generated the next exfiltration request from an attacker-controlled server. The attacker maintained control even after the Copilot chat was closed. Critically for monitoring, all commands were delivered from the server after the initial prompt — making it impossible to detect the exfiltration by inspecting the starting prompt alone. This attack demonstrates why behavioral anomaly detection (recursive request patterns, unusual external data transfers) is essential beyond simple rate-based alerting. Microsoft has since patched the vulnerability. Enterprise Microsoft 365 Copilot customers were not affected.
- **GreyNoise LLM Attack Telemetry (Oct 2025 – Jan 2026):** GreyNoise research documented over 91,000 attack sessions targeting exposed LLM services during this period. The sheer volume highlights why real-time metrics (7.6.1) and rate-based alerting (7.6.2) are non-negotiable — without them, tens of thousands of attack attempts go undetected.
- **ServiceNow Second-Order Prompt Injection (Late 2025):** Attackers discovered a cross-agent escalation path where a low-privilege AI agent was tricked into asking a higher-privilege agent to perform unauthorized actions. This "second-order" injection bypassed usual checks and would only be visible through comprehensive cross-agent logging with model version and session tracking (7.6.3). The OpenTelemetry GenAI agentic system conventions (agent identity, conversation correlation, tool definitions) are specifically designed to make these cross-agent chains observable.
- **Netskope GenAI Data Policy Violations (2025-2026):** The Netskope Cloud and Threat Report 2026 documented that GenAI data policy violations more than doubled year-over-year, with organizations averaging 223 incidents per month (top quartile: 2,100/month). Regulated data (personal, financial, healthcare) accounted for 54% of flagged violations. GenAI app usage tripled and prompt volume increased sixfold, yet 50% of organizations lack enforceable data protection policies. This gap means the observed doubling is likely an underestimation of actual data exposure risk.
- **Shadow AI Data Leaks (Samsung, JPMorgan, Goldman Sachs):** Samsung engineers leaked confidential source code by pasting it into ChatGPT, and multiple Wall Street banks restricted ChatGPT after employees shared sensitive information. The Netskope data confirms this is a systemic problem: 47% of GenAI users access tools via personal accounts, completely bypassing enterprise monitoring. Organizations need network-level detection of unauthorized GenAI tool usage alongside application-level safety monitoring.
- **Prompt Injection Evolution (2025-2026):** Simple attempts to override system instructions are no longer the primary concern. As of early 2026, attackers exploit how models merge information from multiple sources — multi-language encoding, Base64 obfuscation, and indirect injection through retrieved documents. Research documented prompt injection delivering cross-site scripting (XSS) payloads through AI-generated content, bypassing web application firewalls. This evolution makes behavioral anomaly detection and multi-signal correlation essential for monitoring, as signature-based approaches alone cannot keep pace.

---

## Open Research Questions

- **OTel GenAI convergence timeline:** The OpenTelemetry GenAI Semantic Conventions remain experimental as of March 2026. When will they stabilize, and will the agentic system conventions (tasks, actions, agent identity) reach production-grade status before the EU AI Act's August 2026 deadline for high-risk system compliance?
- **Multi-model pipeline attribution:** How should monitoring handle multi-model pipelines where a single user request traverses multiple models — should safety metrics be attributed to the pipeline or individual models? The OTel agentic conventions define tasks and actions, but production implementations of pipeline-level attribution remain sparse.
- **Attack vs. edge-case discrimination:** How can monitoring systems distinguish between adversarial attacks and legitimate edge-case usage that happens to trigger safety filters? The Reprompt attack's chain-request pattern looks superficially like normal multi-turn conversation — what behavioral signals reliably differentiate the two?
- **Monitoring cost at scale:** With platforms charging per-request or per-trace, high-throughput AI applications face significant observability overhead. Sampling strategies that maintain safety signal fidelity while reducing cost are an open engineering problem.
- **Guardrail enforcement vs. observability separation:** What role should real-time guardrail evaluation (e.g., Galileo's 200ms interception) play versus post-hoc monitoring — should safety enforcement and observability be unified or separated? Unified systems reduce latency but create single points of failure.
- **Risk-scoring calibration:** How effective are risk-scoring approaches (normalized 0-1 scale with thresholds at 0.3/0.5/0.7/0.85 for low/medium/high/critical) compared to binary alert triggers in production? What false positive rates are teams seeing across different deployment contexts?
- **Shadow AI detection at scale:** As shadow AI usage grows (47% of GenAI users on personal accounts as of 2026, per Netskope), what monitoring approaches can detect unauthorized AI tool usage within enterprise networks without invasive endpoint surveillance? Network-level DNS and traffic analysis may catch some patterns, but encrypted traffic limits visibility.
- **Federated and privacy-preserving monitoring:** Can federated or privacy-preserving monitoring approaches provide sufficient visibility for safety compliance while respecting data sovereignty requirements (EU AI Act, GDPR)? This is especially relevant for cross-border deployments where log data itself may be regulated.
- **Audit trail standardization:** Will emerging standards converge on a common audit trail format for AI systems, or will organizations need to maintain separate compliance mappings for EU AI Act, ISO 42001, NIST AI RMF, and sector-specific requirements? Gartner's prediction that 75% of large enterprises will require certified logs by Q3 2026 suggests demand is outpacing standardization.

---

## Related Pages

- [C13-01 Request/Response Logging](C13-01-Request-Response-Logging) — the infrastructure side of model-version-tagged, tamper-evident logging that C7.6.3 depends on
- [C13-02 Abuse Detection and Alerting](C13-02-Abuse-Detection-Alerting) — SIEM-level behavioral and signature detection that consumes the safety metrics emitted under C7.6.1 and C7.6.2
- [C13-06 DAG Visualization and Workflow Security](C13-06-DAG-Visualization-Workflow-Security) — sibling controls for protecting the observability UI and trace data that monitoring integration produces
- [C13 Monitoring and Logging (Hub)](C13-Monitoring-and-Logging) — chapter index that positions C7.6 as the AI-behavior feed into the broader monitoring stack
- [C7.5 Explainability and Transparency](C07-05-Explainability-Transparency) — complementary logging of interpretability artifacts that investigators need alongside safety metrics

---
