# C13: Monitoring, Logging & Anomaly Detection

> **Source:** [`1.0/en/0x10-C13-Monitoring-and-Logging.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C13-Monitoring-and-Logging.md)
> **Requirements:** 47 | **Sections:** 8

## Control Objective

This section provides requirements for delivering real-time and forensic visibility into what the model and other AI components see, do, and return, so threats can be detected, triaged, and learned from.

> **2025-2026 Highlights:** OpenTelemetry GenAI SIG and LLM observability platforms (LangSmith, Langfuse, Arize) are establishing standard schemas for AI telemetry. New requirements address covert channel detection in LLM API traffic (C13.2.10) and session-level multi-turn jailbreak trajectory analysis (C13.2.8).

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C13.1 | Request & Response Logging | 8 | [C13-01-Request-Response-Logging](C13-01-Request-Response-Logging) |
| C13.2 | Abuse Detection and Alerting | 10 | [C13-02-Abuse-Detection-Alerting](C13-02-Abuse-Detection-Alerting) |
| C13.3 | Model Drift Detection | 5 | [C13-03-Model-Drift-Detection](C13-03-Model-Drift-Detection) |
| C13.4 | Performance & Behavior Telemetry | 5 | [C13-04-Performance-Behavior-Telemetry](C13-04-Performance-Behavior-Telemetry) |
| C13.5 | AI Incident Response Planning & Execution | 3 | [C13-05-Incident-Response](C13-05-Incident-Response) |
| C13.6 | AI Performance Degradation Detection | 6 | [C13-06-Performance-Degradation-Detection](C13-06-Performance-Degradation-Detection) |
| C13.7 | DAG Visualization & Workflow Security | 5 | [C13-07-DAG-Visualization-Workflow-Security](C13-07-DAG-Visualization-Workflow-Security) |
| C13.8 | Proactive Security Behavior Monitoring | 5 | [C13-08-Proactive-Security-Behavior-Monitoring](C13-08-Proactive-Security-Behavior-Monitoring) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Shadow AI and unmonitored usage** — 98% of organizations report unsanctioned AI use (Knostic 2025). 47% of GenAI users operate through personal accounts invisible to IT. Shadow AI adds $670K to average breach costs. Shadow AI breaches take 247 days to detect on average.
- **AI-specific failure detection gaps** — AI failures take an average of 4.5 days to detect with current tooling. Traditional metrics (latency, error rates) appear healthy while output quality silently degrades. Only 62% of organizations use detailed tracing; only 72% of those with production agents have tracing. As of early 2026, 85% of organizations plan LLM observability but only 8% have actually implemented it (Elastic Observability Report 2026).
- **Multi-turn abuse trajectories** — Crescendo attacks (USENIX Security 2025) escalate through benign-seeming turns; Deceptive Delight achieves 65% success within three turns. Per-request monitoring misses these cross-turn patterns entirely.
- **Log tampering and forensic integrity** — PoisonedRAG showed 5 documents corrupt 90% of RAG outputs. Medical training data poisoning (0.001% of tokens) produces harmful models undetectable by standard benchmarks. Beyond data poisoning, AI agent logs are themselves attack targets — agents that make autonomous decisions without reliable logging create blind spots that attackers exploit to hide data exfiltration or unauthorized actions. Adversaries may also spoof agent identities in multi-agent systems to perform actions under another persona.
- **AI-powered attack automation** — GTG-1002 campaign (November 2025) targeted ~30 organizations with AI handling 80-90% of operations including reconnaissance, exploit development, and lateral movement. Only 4-6 human decision points per campaign. Traditional IR playbooks had no framework for this.
- **Prompt injection dominates real incidents** — Adversa AI's 2025 AI Security Incidents Report found 35% of all real-world AI security incidents were caused by simple prompt injection, with some leading to $100K+ in real losses. GenAI was involved in 70% of incidents, but agentic AI caused the most dangerous failures including crypto thefts, API abuse, and supply chain attacks. System prompt extraction was the most common attacker objective in Q4 2025.
- **Alert fatigue and observability-action gap** — 59% of organizations are drowning in telemetry but cannot get answers when needed. 36% are buried in alert fatigue. 39% have integration gaps between monitoring tools and workflows. The monitoring system itself can be an attack target — since LLM-based monitoring inherits the same vulnerabilities it aims to detect, an attacker who compromises monitoring could blind the organization to ongoing attacks or create false alerts masking real threats.
- **AI-specific SIEM rules emerging but immature** — MITRE ATLAS Splunk app (2025) was the first production SIEM with AI attack detection rules. As of December 2025, ANY.RUN released AI-generated Sigma rules for threat detection. SigmaGen automates ATT&CK-mapped rule generation using LLMs. However, no major SIEM vendor ships comprehensive AI-attack-specific rule packs — the gap between "AI assists SOC analysts" and "SIEM detects attacks on AI" persists.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Nov 2025 | GTG-1002 — AI-automated attack campaign targeting ~30 organizations | AI handled 80-90% of attack operations; traditional IR playbooks had no framework for response | [Reco.ai](https://www.reco.ai/blog/ai-and-cloud-security-breaches-2025) |
| Jun 2025 | EchoLeak CVE-2025-32711 — zero-click Copilot exfiltration | No monitoring alerts surfaced despite enterprise data exfiltration via crafted email | [arXiv](https://arxiv.org/html/2509.10540v1) |
| 2025 | CoSAI AI Incident Response Framework with CACAO playbooks | First standardized AI-specific IR framework with detection, triage, containment, recovery procedures | [CoSAI](https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/) |
| 2025 | MITRE ATLAS AI Threat Detection for Splunk | First production SIEM integration with 2-tier detection (operational telemetry + content inspection) | [Splunkbase](https://splunkbase.splunk.com/app/8527) |
| 2025 | Crescendo multi-turn jailbreak (Microsoft/USENIX Security) | Multi-turn escalation invisible to per-request monitoring; single-turn defenses show single-digit ASR while multi-turn exceeds 70% | [USENIX](https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-805-russinovich.pdf) |
| 2025 | IBM: Shadow AI adds $670K to breach costs | 20% of breaches attributed to shadow AI; 247-day average detection time | [IBM/Reco.ai](https://www.reco.ai/blog/ai-and-cloud-security-breaches-2025) |
| 2025 | LangChain AI Observability research — 4.5-day detection gap | Traditional metrics appear healthy while domain quality silently degrades; only 62% of orgs use detailed tracing | [LangChain](https://www.langchain.com/articles/ai-observability) |
| 2025 | Adversa AI 2025 AI Security Incidents Report — 35% prompt injection | 35% of real-world AI incidents caused by prompt injection; GenAI in 70% of incidents; agentic AI caused the most dangerous failures | [Adversa AI](https://adversa.ai/blog/adversa-ai-unveils-explosive-2025-ai-security-incidents-report-revealing-how-generative-and-agentic-ai-are-already-under-attack/) |
| Dec 2025 | ANY.RUN releases AI-generated Sigma rules for threat detection | First AI-specific Sigma detection rules; SigmaGen automates ATT&CK-mapped rule generation | [ANY.RUN](https://any.run/cybersecurity-blog/release-notes-december-2025/) |
| Feb 2026 | AG2 framework ships native OpenTelemetry tracing for multi-agent systems | Structured hierarchical traces of conversations, agent turns, LLM calls, tool executions following OTel GenAI semantic conventions | [AG2](https://docs.ag2.ai/latest/docs/blog/2026/02/08/AG2-OpenTelemetry-Tracing/) |
| Mar 2026 | Elastic 2026 Observability Report — 85% plan LLM observability, 8% implemented | OTel production deployment doubled to 11%; 61% cite data leakage risks with external LLM telemetry; agentic AI observability at 0-35% depending on maturity | [Elastic](https://www.elastic.co/blog/2026-observability-trends-generative-ai-opentelemetry) |
| Apr 2026 | Microsoft Sentinel MCP entity analyzer GA at RSAC 2026 | Reasoned risk assessments for URLs and identities using threat intelligence and organizational context; AI-assisted playbook generator in preview | [Microsoft](https://techcommunity.microsoft.com/blog/microsoftsentinelblog/what%E2%80%99s-new-in-microsoft-sentinel-rsac-2026/4503971) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **LLM observability:** [LangSmith](https://smith.langchain.com/) (~0% overhead, $39/seat/month), [Langfuse](https://langfuse.com/) (open-source MIT, self-hostable, prompt versioning, agent graph visualization), [Arize Phoenix](https://arize.com/) (open-source EL2, embedding drift monitoring, LLM-as-judge), [WhyLabs](https://whylabs.ai/) (Apache 2.0 since Jan 2025, real-time drift + prompt injection detection), [Helicone](https://www.helicone.ai/) (gateway-based, cost tracking across 100+ LLMs)
- **OpenTelemetry GenAI SIG:** [Semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) (experimental status, v1.40.0) define 20+ attributes including `gen_ai.operation.name`, `gen_ai.usage.input_tokens`, `gen_ai.tool.name`, provider-specific conventions for Anthropic/OpenAI/AWS Bedrock. Prompt content marked as opt-in/sensitive by design. As of March 2026, [agent span conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) have moved from proposal (#2664) to "Development" status — defining create-agent, invoke-agent, and execute-tool span types with `conversation_id` tracking. Opt-in via `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`. Datadog [natively supports](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) OTel GenAI conventions for LLM observability.
- **Drift detection:** [Evidently AI](https://www.evidentlyai.com/) (20+ drift detection methods, now supports LLM evaluations), [NannyML](https://www.nannyml.com/) (performance estimation without ground truth), WhyLabs (embedding drift for LLMs). Key gap: LLM drift requires embedding drift + LLM-as-judge, not just statistical distribution shifts.
- **SIEM integration:** [Datadog LLM Observability](https://www.datadoghq.com/) (LiteLLM integration, 800+ OOTB detection rules with MITRE mapping, native OTel GenAI convention support), [Microsoft Sentinel](https://azure.microsoft.com/en-us/products/microsoft-sentinel) (2025 Gartner MQ leader, Copilot for Security; RSAC 2026: MCP entity analyzer GA for reasoned risk assessments, AI-assisted playbook generator preview), Splunk (AI Assistant for NL search), Elastic. [MITRE ATLAS Splunk App](https://splunkbase.splunk.com/app/8527) — first production SIEM with 2-tier AI attack detection rules. [Sigma](https://github.com/SigmaHQ/sigma) open standard enables SIEM-agnostic detection rules convertible to 40+ platforms; [SigmaGen](https://blogs.night-wolf.io/sigmagen-ai-powered-attck-mapped-threat-detection-with-sigma-rules) automates ATT&CK-mapped rule generation.
- **Prompt injection detection:** [Lakera Guard](https://www.lakera.ai/) (98%+ detection, sub-50ms, 100+ languages, trained on 80M+ adversarial prompts — acquired by Check Point Sep 2025), [LLM Guard](https://llm-guard.com/) (open-source input/output validation), [Rebuff](https://github.com/protectai/rebuff) (4-layer self-hardening detection). Note: 73% of deployments are vulnerable to prompt injection but only 34.7% have defenses deployed.
- **Agent monitoring:** [AgentOps](https://www.agentops.ai/) (session replay, time-travel debugging, 400+ LLMs, 12% overhead), [Lunary](https://lunary.ai/) (conversation replay, topic classification), Weights & Biases Weave (hierarchical multi-agent tracing), [AG2](https://docs.ag2.ai/latest/docs/blog/2026/02/08/AG2-OpenTelemetry-Tracing/) (Feb 2026, native OTel tracing for multi-agent systems — structured hierarchical traces of conversations, agent turns, tool executions across local and distributed deployments)
- **Log integrity and forensics:** Hash chaining (each log entry references previous entry's hash), cryptographic digital signatures per agent identity, append-only immutable storage with object locking and retention policies. Identity-bound logging ties each entry to agent identifier, tenant context, authorization scope, and delegation status. Automated tamper detection monitors for missing sequences, invalid hash chains, or signature verification failures. See [LoginRadius guide](https://www.loginradius.com/blog/engineering/ensure-log-integrity-non-repudiation-ai-agents) for implementation patterns.
- **Incident response:** [CoSAI AI IR Framework](https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/) (2025 — CACAO-standard playbooks for AI-specific attacks), PagerDuty, Opsgenie with AI-specific runbooks. Gap: no widely adopted AI-specific IR tools yet.
- **DAG/workflow visualization:** [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) (visual agent workflow debugging), [Apache Airflow 3.0](https://airflow.apache.org/) (April 2025, 30M+ monthly downloads, 30% for MLOps), [Prefect](https://www.prefect.io/), [Dagster](https://dagster.io/) (asset-centric, GA Components Oct 2025)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C13.1 Request & Response Logging | Maturing | OpenTelemetry GenAI SIG defines 20+ attributes (experimental, v1.40.0). Agent spans now in "Development" status with create/invoke/execute-tool types. Datadog natively supports OTel GenAI conventions. LangSmith, Langfuse, Arize provide production observability. C13.1.7 schema requirement aligns with OTel conventions. PII redaction (C13.1.4) well-served by Presidio. Log integrity patterns (hash chaining, identity-bound logging) maturing for C13.1.6. |
| C13.2 Abuse Detection and Alerting | Maturing | Lakera Guard (98%+ detection), MITRE ATLAS Splunk app (2-tier rules), Sigma/SigmaGen for SIEM-agnostic AI detection rules. Sentinel MCP entity analyzer (GA Apr 2026) adds reasoned risk assessments. Signature-based detection production-ready; behavioral anomaly detection (C13.2.4) and multi-turn trajectory analysis (C13.2.8) still emerging. Covert channel detection (C13.2.10) is research-stage. |
| C13.3 Model Drift Detection | Maturing | Evidently AI, NannyML, WhyLabs well-established for tabular ML. LLM drift requires embedding drift + LLM-as-judge — Arize Phoenix and WhyLabs are strongest here. Gap: no automated equivalent to domain expert quality assessments. |
| C13.4 Performance & Behavior Telemetry | Mature | Standard APM (Datadog, Grafana) extends to AI. OTel GenAI metrics track latency, tokens, cost. Attention exploitation attacks (6000x latency increase) need AI-specific alerting thresholds. |
| C13.5 AI Incident Response | Emerging | CoSAI published first AI-specific IR framework (2025) with CACAO playbooks. NIST IR 8596 provides the Detect/Respond framework. But operational tooling is DIY — analysis of 1,200+ playbooks found none usable without significant transformation. |
| C13.6 Performance Degradation Detection | Maturing | Traditional metrics (latency, error rates) are mature. Semantic/domain quality degradation (hallucination frequency, factual accuracy) still requires LLM-as-judge or human assessment. 4.5-day average detection gap. |
| C13.7 DAG Visualization & Workflow Security | Emerging | LangGraph Studio for agent workflows, Airflow 3.0/Dagster for ML pipelines. Cross-tool access exploitation (CSA 2025) shows need for pipeline-level security monitoring that doesn't yet exist. |
| C13.8 Proactive Security Behavior Monitoring | Emerging | AgentOps, Lunary, and AG2 (native OTel tracing, Feb 2026) provide agent-specific monitoring. OTel agent spans now in Development status (beyond proposal #2664). Multi-turn jailbreak trajectories and cross-request behavioral patterns remain largely unmonitored in production. Elastic 2026 report: agentic AI observability ranges from 0% (early teams) to 35% (expert teams). |

---

## Open Research Questions

- [ ] **When should full prompt/response content be logged?** — OTel GenAI marks content as opt-in/sensitive. C13.1.8 says log full content only on security events or with explicit consent. But MITRE ATLAS Tier 2 detection (jailbreaks, prompt injection) *requires* content inspection. NIST IR 8596 recommends PII redaction. EU AI Act Art 12 requires logging events that identify risk. The tension between detection capability and privacy is unresolved.
- [ ] **Will OpenTelemetry GenAI conventions stabilize in time?** — Core attributes remain experimental (v1.40.0). Agent spans have progressed from proposal #2664 to "Development" status with create/invoke/execute-tool types, but the transition plan for stable status is still TBD. OTel production deployment doubled year-over-year to 11% (Elastic 2026), and 89% of production users consider vendor OTel compliance critical. Schema changes could still break existing instrumentation, though the `OTEL_SEMCONV_STABILITY_OPT_IN` mechanism provides a migration path.
- [ ] **How do you detect multi-turn abuse trajectories at scale?** — Crescendo and Deceptive Delight attacks are invisible to per-request monitoring. Single-turn defenses show single-digit ASR while multi-turn exceeds 70%. Session-level analysis requires correlating across requests — expensive and architecturally complex.
- [ ] **Can AI-specific SIEM detection rules become standard?** — MITRE ATLAS Splunk app was the first step, and Sigma/SigmaGen now enable SIEM-agnostic rule generation convertible to 40+ platforms. Microsoft Sentinel's MCP entity analyzer (GA Apr 2026) adds AI-powered risk assessment. But comprehensive AI-attack-specific rule packs remain absent from major SIEM vendors — the gap between "AI assists SOC analysts" and "SIEM detects attacks on AI" is narrowing but persists.
- [ ] **How do you distinguish adversarial drift from natural concept drift?** — Both manifest as degraded outputs. Adversarial drift may be intentional poisoning (PoisonedRAG, VIA). Current tools detect drift but don't attribute cause. CSA (Sep 2025) warns incidents are often misattributed to natural drift rather than active attack.
- [ ] **How should shadow AI be governed?** — 98% of orgs have unsanctioned AI; 47% through personal accounts. Agent-based shadow AI (MCP servers, OAuth tokens) creates elevated-privilege access chains invisible to IT. No standard governance framework exists.
- [ ] **Can monitoring systems protect themselves from the attacks they detect?** — LLM-based monitoring inherits the vulnerabilities it aims to detect. An attacker who compromises the monitoring layer via prompt injection or adversarial inputs could blind the organization to ongoing attacks or generate false alerts masking real threats. No standard architecture for self-protecting monitoring exists.
- [ ] **How do you close the observability-implementation gap?** — 85% of organizations plan LLM observability, but only 8% have implemented it (Elastic 2026). OTel production deployment doubled to 11% but remains low. The gap between intent and deployed monitoring creates a window where most AI systems run effectively unmonitored in production.

---

## Related Standards & Cross-References

- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) (experimental, v1.40.0) — 20+ standardized attributes for AI telemetry including provider-specific conventions for Anthropic, OpenAI, AWS Bedrock. [Agent span conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/) now in "Development" status with create-agent, invoke-agent, execute-tool span types.
- [MITRE ATLAS AI Threat Detection for Splunk](https://splunkbase.splunk.com/app/8527) — 2-tier detection: Tier 1 (operational telemetry) for AML.T0024/T0020/T0047; Tier 2 (content inspection) for AML.T0051/T0054
- [EU AI Act Article 12](https://www.euaiact.com/article/12) — High-risk AI must technically allow automatic logging over system lifetime. [Article 26](https://artificialintelligenceact.eu/article/26/) — Deployers must retain logs at least 6 months. [Article 19](https://artificialintelligenceact.eu/article/19/) — Providers must retain automatically generated logs.
- [ISO/IEC 42001 A.6.2.8](https://www.isms.online/iso-42001/annex-a-controls/a-6-ai-system-life-cycle/a-6-2-8-ai-system-recording-of-event-logs/) — AI event logs must be tamper-evident, lifecycle-mapped, and fully auditable. Records consequential decisions, anomalies, policy overrides, retraining events.
- [NIST IR 8596 — Cyber AI Profile](https://csrc.nist.gov/pubs/ir/8596/iprd) (preliminary draft, Dec 2025; comment period closed Jan 2026; initial public draft expected mid-2026) — DETECT section covers AI-specific detection; RESPOND covers AI incident response. Recommends logging API calls, tool invocations, anomalies with PII redaction and 30-90 day retention. [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) provides the CSF 2.0-aligned incident response profile that IR 8596 AI-specific guidance builds upon.
- [CoSAI AI IR Framework](https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/) (2025) — CACAO-standard playbooks for AI-specific attacks
- [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM01 (log prompt patterns), LLM02 (monitor for PII/secrets leakage), LLM06 (audit tool calls), LLM07 (monitor prompt extraction), LLM10 (token usage monitoring)
- [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) (Jul 2025) — 243 controls across 18 domains including Logging and Monitoring domain
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — MEASURE and MANAGE functions address runtime monitoring and risk treatment

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C02 User Input Validation](C02-User-Input-Validation.md) | Prompt injection detection | ATLAS AML.T0051 (Tier 2 content inspection) detects prompt injection in logs. C13.2 monitors attacks that C02 prevents at input. OWASP LLM01 requires monitoring prompt patterns. |
| [C07 Model Behavior](C07-Model-Behavior.md) | Safety filter decision logging | ATLAS AML.T0048 (External Harms Safety Flag) monitors safety violations. ISO 42001 A.6.2.8 requires logging "consequential decisions" — safety filter outcomes qualify. C13.1.5 logs filter decisions defined in C07. |
| [C09 Orchestration & Agents](C09-Orchestration-and-Agents.md) | Agent action audit trails | OTel GenAI agent spans (now "Development" status) define create-agent, invoke-agent, and execute-tool telemetry. AG2 ships native OTel tracing for multi-agent systems (Feb 2026). OWASP LLM06 requires tool call audit trails. C13.8 monitors agent behaviors governed by C09. |
| [C11 Adversarial Robustness](C11-Adversarial-Robustness.md) | Adversarial detection monitoring | ATLAS Tier 1 detects reconnaissance (AML.T0007), extraction (AML.T0024), poisoning (AML.T0020). Tier 2 detects jailbreaks (AML.T0054). NIST IR 8596 DETECT covers AI-specific adversarial detection. |
| [C12 Privacy](C12-Privacy.md) | PII redaction in logs | NIST IR 8596 requires PII redaction. EU AI Act Art 12 for biometrics requires logging input data — tension with privacy resolved via pseudonymization. OTel content attributes are opt-in due to privacy. C13.1.4 redaction supports C12. |
| [C14 Human Oversight](C14-Human-Oversight.md) | Alert routing and escalation | C13.2.5 real-time alerting feeds C14 human oversight workflows. C13.5 IR procedures integrate with C14 human review processes. |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
