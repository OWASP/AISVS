# C13 Monitoring, Logging & Anomaly Detection

## Control Objective

This section provides requirements for delivering real-time and forensic visibility into what the model and other AI components see, do, and return, so threats can be detected, triaged, and learned from.

## C13.1 Request & Response Logging

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.1.1** | **Verify that** all user prompts and model responses are logged with appropriate metadata (e.g. timestamp, user ID, session ID, model version). | 1   | D/V |
| **13.1.2** | **Verify that** logs are stored in secure, access-controlled repositories with appropriate retention policies and backup procedures. | 1   | D/V |
| **13.1.3** | **Verify that** log storage systems implement encryption at rest and in transit to protect sensitive information contained in logs. | 1   | D/V |
| **13.1.4** | **Verify that** sensitive data in prompts and outputs is automatically redacted or masked before logging, with configurable redaction rules for PII, credentials, and proprietary information. | 1   | D/V |
| **13.1.5** | **Verify that** policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2   | D/V |
| **13.1.6** | **Verify that** log integrity is protected through e.g. cryptographic signatures or write-only storage. | 2   | D/V |
| **13.1.7** | **Verify that** log entries capture OpenTelemetry GenAI Semantic Convention attributes including `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.provider.name`, and `gen_ai.operation.name` to enable interoperable AI observability. | 2   | D/V |
| **13.1.8** | **Verify that** tool invocation events in agentic workflows are logged with the invoking agent identity, the tool name, input parameters (sanitized), output summary, and execution duration to enable agent action auditability. | 1   | D/V |
| **13.1.9** | **Verify that** logs for high-risk AI system deployments are retained for a minimum of six months and are accessible to authorized regulatory bodies upon request, in compliance with applicable regulatory obligations (e.g. EU AI Act Article 72). | 1   | D/V |
| **13.1.10** | **Verify that** inference event logs capture sufficient metadata to enable post-market monitoring including input hash, model version, system prompt version, and safety filter decisions. | 2   | D/V |

---

## C13.2 Abuse Detection and Alerting

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.2.1** | **Verify that** the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs using signature-based detection. | 1   | D/V |
| **13.2.2** | **Verify that** the system integrates with existing Security Information and Event Management (SIEM) platforms using standard log formats and protocols. | 1   | D/V |
| **13.2.3** | **Verify that** enriched security events include AI-specific context such as model identifiers, confidence scores, and safety filter decisions. | 2   | D/V |
| **13.2.4** | **Verify that** behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or systematic probing behaviors. | 2   | D/V |
| **13.2.5** | **Verify that** real-time alerting mechanisms notify security teams when potential policy violations or attack attempts are detected. | 2   | D/V |
| **13.2.6** | **Verify that** custom rules are included to detect AI-specific threat patterns including coordinated jailbreak attempts, prompt injection campaigns, and model extraction attacks. | 2   | D/V |
| **13.2.7** | **Verify that** automated incident response workflows can isolate compromised models, block malicious users, and escalate critical security events. | 3   | D/V |
| **13.2.8** | **Verify that** session-level conversation trajectory analysis detects multi-turn jailbreak patterns where no individual turn is overtly malicious but the aggregate conversation exhibits injection indicators such as gradual constraint erosion, persona shifting, or payload assembly across turns. | 2   | D/V |
| **13.2.9** | **Verify that** all content retrieved from external sources by agentic tools (web pages, files, API responses) is scanned for indirect prompt injection patterns before being included in model context. | 1   | D/V |
| **13.2.10** | **Verify that** aggregate query behavioral profiling detects model extraction attack patterns including unusually high query volume, systematic topic coverage diversity, regular automated query cadences, and high export volumes consistent with shadow model creation. | 2   | D/V |
| **13.2.11** | **Verify that** per-user and per-session token consumption is tracked, with anomaly detection alerting when consumption exceeds defined thresholds to detect denial-of-service and model extraction attempts. | 1   | D/V |
| **13.2.12** | **Verify that** LLM API traffic is monitored for covert channel indicators, including Base64-encoded payloads, structured non-human query patterns, and communication signatures consistent with malware command-and-control activity using LLM endpoints. | 3   | D/V |
| **13.2.13** | **Verify that** SIEM detection rules are mapped to MITRE ATLAS adversarial ML TTPs and maintained with updates as new techniques are added to the ATLAS knowledge base. | 2   | D/V |

---

## C13.3 Model Drift Detection

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.3.1** | **Verify that** the system tracks basic performance metrics such as accuracy, confidence scores, latency, and error rates across model versions and time periods. | 1   | D/V |
| **13.3.2** | **Verify that** automated alerting triggers when performance metrics exceed predefined degradation thresholds or deviate significantly from baselines. | 2   | D/V |
| **13.3.3** | **Verify that** hallucination detection monitors identify and flag instances when model outputs contain factually incorrect, inconsistent, or fabricated information. | 2   | D/V |
| **13.3.4** | **Verify that** input distribution drift is measured using named statistical methods appropriate to the data type, such as Population Stability Index (PSI) for categorical features and Kolmogorov-Smirnov test for continuous distributions, with defined alerting thresholds for each. | 2   | D/V |
| **13.3.5** | **Verify that** schema drift in incoming data (unexpected field additions, removals, type changes, or format variations) is detected and triggers alerting, as it may indicate upstream data pipeline tampering or adversarial input manipulation. | 2   | D/V |
| **13.3.6** | **Verify that** sudden unexplained behavioral shifts (potential poisoning indicators) are distinguished from gradual expected operational drift through correlation with deployment events, training data changes, and external environmental factors, with a defined security escalation path for unexplained sudden drift. | 3   | V |
| **13.3.7** | **Verify that** hallucination rate is tracked as a continuous time-series metric at the system level, not only as a per-response flag, enabling trend analysis that can detect model degradation or silent poisoning through sustained accuracy deterioration. | 2   | D/V |

---

## C13.4 Performance & Behavior Telemetry

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.4.1** | **Verify that** operational metrics including request latency, token consumption, memory usage, and throughput are continuously collected and monitored. | 1   | D/V |
| **13.4.2** | **Verify that** success and failure rates are tracked with categorization of error types and their root causes. | 1   | D/V |
| **13.4.3** | **Verify that** resource utilization monitoring includes GPU/CPU usage, memory consumption, and storage requirements with alerting on threshold breaches. | 2   | D/V |
| **13.4.4** | **Verify that** token usage is tracked at granular attribution levels (per user, per session, per feature endpoint, per team or workspace) to enable both cost anomaly detection and security-relevant consumption pattern analysis. | 1   | D/V |
| **13.4.5** | **Verify that** output-to-input token ratio anomalies are detected and alerted, as disproportionately large outputs relative to inputs may indicate prompt injection attacks causing verbose or uncontrolled generation. | 2   | D/V |
| **13.4.6** | **Verify that** toxicity scores are computed for all model outputs and tracked as time-series metrics, with alerting when scores exceed defined thresholds and trend analysis to detect systematic toxicity increases. | 1   | D/V |
| **13.4.7** | **Verify that** PII detection is applied to all model outputs before delivery and results are logged (not the PII itself) to enable audit of PII leakage incidents and measure the effectiveness of redaction controls. | 1   | D/V |

---

## C13.5 AI Incident Response Planning & Execution

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.5.1** | **Verify that** incident response plans specifically address AI-related security events including model compromise, data poisoning, and adversarial attacks. | 1   | D/V |
| **13.5.2** | **Verify that** incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2   | D/V |
| **13.5.3** | **Verify that** post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3   | D/V |
| **13.5.4** | **Verify that** incident response procedures for high-risk AI systems include a defined escalation path to relevant regulatory or market surveillance authorities for serious incidents, with documented timelines and responsible personnel. | 2   | D/V |
| **13.5.5** | **Verify that** post-market monitoring findings are formally fed back into the risk management system, with documented evidence of how monitoring data influenced risk assessments and control updates. | 2   | D/V |
| **13.5.6** | **Verify that** AI incident response playbooks address AI-specific attack scenarios including model inversion, data poisoning discovery, prompt injection campaigns, and model extraction, with specific containment and investigation steps for each. | 3   | D/V |

---

## C13.6 AI Performance Degradation Detection

Monitor and detect degradation in AI model performance and quality over time.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.6.1** | **Verify that** model accuracy, precision, recall, and F1 scores are continuously monitored and compared against baseline thresholds. | 1 | D/V |
| **13.6.2** | **Verify that** data drift detection monitors input distribution changes that may impact model performance. | 1 | D/V |
| **13.6.3** | **Verify that** concept drift detection identifies changes in the relationship between inputs and expected outputs. | 2 | D/V |
| **13.6.4** | **Verify that** performance degradation triggers automated alerts and initiates model retraining or replacement workflows. | 2 | D/V |
| **13.6.5** | **Verify that** degradation root cause analysis correlates performance drops with data changes, infrastructure issues, or external factors. | 3 | V |
| **13.6.6** | **Verify that** baseline performance profiles are formally documented and version-controlled, with a defined re-baselining process requiring documented approval when baselines are updated, to prevent silent normalization of degraded performance. | 2 | D/V |
| **13.6.7** | **Verify that** model testing, evaluation, and validation is performed as a continuous lifecycle activity in production, not only at deployment, with documented cadence and results tracked over time. | 2 | D/V |

---

## C13.7 DAG Visualization & Workflow Security

Protect workflow visualization systems from information leakage and manipulation attacks.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.7.1** | **Verify that** DAG visualization data is sanitized to remove sensitive information before storage or transmission. | 1 | D/V |
| **13.7.2** | **Verify that** workflow visualization access controls ensure only authorized users can view agent decision paths and reasoning traces. | 1 | D/V |
| **13.7.3** | **Verify that** DAG data integrity is protected through cryptographic signatures and tamper-evident storage mechanisms. | 2 | D/V |
| **13.7.4** | **Verify that** workflow visualization systems implement input validation to prevent injection attacks through crafted node or edge data. | 2 | D/V |
| **13.7.5** | **Verify that** real-time DAG updates are rate-limited and validated to prevent denial-of-service attacks on visualization systems. | 3 | D/V |

---

## C13.8 Proactive Security Behavior Monitoring

Detection and prevention of security threats through proactive agent behavior analysis.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.8.1** | **Verify that** proactive agent behaviors are security-validated before execution with risk assessment integration. | 1 | D/V |
| **13.8.2** | **Verify that** autonomous initiative triggers include security context evaluation and threat landscape assessment. | 2 | D/V |
| **13.8.3** | **Verify that** proactive behavior patterns are analyzed for potential security implications and unintended consequences. | 2 | D/V |
| **13.8.4** | **Verify that** security-critical proactive actions require explicit approval chains with audit trails. | 3 | D/V |
| **13.8.5** | **Verify that** behavioral anomaly detection identifies deviations in proactive agent patterns that may indicate compromise. | 3 | D/V |
| **13.8.6** | **Verify that** multi-agent delegation chains are logged end-to-end, recording each agent-to-agent authority transfer, the scope of delegated permissions, and the human principal at the root of each delegation tree, to enable accountability tracing in agentic systems. | 2 | D/V |
| **13.8.7** | **Verify that** AI agent identity lifecycle events are logged including provisioning, permission grants, scope changes, and deprovisioning, with alerts on agents operating without active provisioning records or with expired authorization. | 1 | D/V |

---

## C13.9 AI Supply Chain Integrity Monitoring

Monitor the integrity, provenance, and authenticity of AI model artifacts throughout the supply chain from source to runtime.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.9.1** | **Verify that** cryptographic hashes of model weight files are computed, stored securely at the time of model registration, and verified before each deployment and at each inference session start to detect unauthorized model tampering. | 1 | D/V |
| **13.9.2** | **Verify that** an AI Bill of Materials (AI-BOM) is maintained for all production models, documenting training data provenance, framework versions, fine-tuning lineage, and dependency versions, with automated alerts on unauthorized changes to any BOM entry. | 2 | D/V |
| **13.9.3** | **Verify that** model registry access and modification events are logged with user identity, timestamp, and change details, with alerting on modifications outside approved change management workflows. | 1 | D/V |
| **13.9.4** | **Verify that** pre-deployment model artifact scanning is performed to detect known malicious patterns, backdoors, and anomalous behaviors before models are promoted to production. | 2 | D/V |
| **13.9.5** | **Verify that** output watermarking is deployed for proprietary models and watermark integrity is continuously monitored, with alerts when model outputs fail watermark verification as a potential indicator of model substitution or extraction. | 3 | D/V |
| **13.9.6** | **Verify that** training data integrity is monitored for poisoning indicators including anomalous label distributions, statistical outlier injection, and unauthorized data source additions, with alerts on detected anomalies before they influence production models. | 2 | D/V |

---

## C13.10 Agentic AI and RAG Pipeline Audit Logging

Capture the full execution context of agentic AI systems including tool use, memory access, retrieval operations, and inter-agent delegation.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.10.1** | **Verify that** RAG pipeline retrieval events log the query issued, the documents or chunks retrieved, similarity scores, the knowledge source (database and version), and whether retrieved content passed injection scanning, to enable forensic reconstruction of retrieval-influenced outputs. | 1 | D/V |
| **13.10.2** | **Verify that** vector database access events log the querying entity identity, namespace accessed, number of results returned, and any access control evaluation outcomes, with alerts on cross-namespace retrieval that violates data isolation policies. | 2 | D/V |
| **13.10.3** | **Verify that** embedding generation events are logged with input content hash, embedding model version, and output vector dimensionality, to detect embedding model substitution or manipulation in the pipeline. | 2 | D/V |
| **13.10.4** | **Verify that** agent memory state changes (write, update, delete operations to persistent memory stores) are logged with the agent identity, operation type, and content hash, with retention policies aligned to the sensitivity of memorized data. | 2 | D/V |
| **13.10.5** | **Verify that** retrieval anomaly detection identifies embedding density outliers, repeated dominance of specific documents in similarity results, and sudden shifts in retrieval bias distribution that may indicate silent vector database poisoning. | 3 | D/V |
| **13.10.6** | **Verify that** all external content consumed by agentic tools (web page content, file contents, API response bodies) is logged with source URL or identifier, content hash, and injection scan result before being incorporated into model context. | 1 | D/V |

---

## C13.11 Output Safety and Quality Monitoring

Continuously evaluate and monitor model outputs for safety violations, quality degradation, and harmful content patterns.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.11.1** | **Verify that** automated hallucination detection is applied to model outputs in production using reference-less methods or LLM-as-judge evaluation, with results logged per response and aggregated as system-level trend metrics. | 2 | D/V |
| **13.11.2** | **Verify that** all model outputs are scanned for PII using a combination of pattern matching (structured PII) and named entity recognition (unstructured PII) before delivery, with scan results logged and PII detection rates tracked as operational security metrics. | 1 | D/V |
| **13.11.3** | **Verify that** toxicity scoring is applied to all model outputs, with per-response scores logged and system-level toxicity rate trends monitored, and that sustained toxicity rate increases above a defined threshold trigger model governance review. | 1 | D/V |
| **13.11.4** | **Verify that** output safety metrics (hallucination rate, toxicity rate, PII detection rate, refusal rate) are surfaced in operational dashboards with trend visualization, and that regression in any metric triggers a defined escalation workflow to model governance teams. | 2 | D/V |
| **13.11.5** | **Verify that** factual accuracy monitoring is implemented for RAG-grounded responses by comparing output claims against retrieved source documents, with grounding failures logged and rates tracked to detect RAG pipeline degradation or retrieval poisoning. | 3 | D/V |

---

## C13.12 Multimodal Input Security Monitoring

Monitor non-text inputs (images, audio, video) for adversarial manipulation, policy violations, and modality-specific attack patterns.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.12.1** | **Verify that** all non-text inputs (images, audio, video, documents) submitted to multimodal AI systems are logged with metadata including file format, file size, content hash, and source identifier, to enable forensic investigation of multimodal attacks. | 1 | D/V |
| **13.12.2** | **Verify that** statistical property monitoring is applied to image inputs to detect adversarial perturbation patterns (e.g., unusually high-frequency noise, anomalous pixel value distributions) consistent with adversarial example attacks against vision models. | 3 | D/V |
| **13.12.3** | **Verify that** audio input quality and statistical properties are monitored to detect voice spoofing, frequency manipulation, and adversarial noise injection patterns that may be used to manipulate speech recognition or audio analysis components. | 3 | D/V |
| **13.12.4** | **Verify that** cross-modal consistency checking is implemented for multimodal inputs, logging and alerting on semantically contradictory signal combinations across text, image, and audio modalities that may indicate cross-modal exploit attempts. | 3 | D/V |
| **13.12.5** | **Verify that** liveness verification events in biometric AI systems are logged with session identifiers, result outcomes, and anomaly scores, with monitoring for patterns consistent with deepfake replay attacks (e.g., repeated liveness failures from the same source). | 2 | D/V |

---

## C13.13 Federated Learning Monitoring

Monitor the security and privacy properties of federated learning systems during distributed training.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.13.1** | **Verify that** per-round differential privacy budget consumption (epsilon and delta values) is logged and monitored, with alerts when cumulative privacy budget approaches or exceeds defined limits to prevent privacy exhaustion attacks. | 2 | D/V |
| **13.13.2** | **Verify that** participant gradient submissions in federated learning rounds are statistically monitored for outlier magnitude, anomalous direction, and coordinated deviation patterns consistent with Byzantine attacks or gradient poisoning. | 3 | D/V |
| **13.13.3** | **Verify that** federated learning audit trails log round-by-round global model state hashes, participating client counts, aggregation algorithm used, and any clients excluded for anomalous contributions, stored in tamper-evident format. | 2 | D/V |
| **13.13.4** | **Verify that** federated learning systems implement canary-based privacy auditing to empirically bound privacy leakage, with audit results logged and reviewed per training cycle. | 3 | V |

---

## References

- [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS - Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf)
- [EU Artificial Intelligence Act - Articles 9, 12, 72](https://artificialintelligenceact.eu/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Coalition for Secure AI (CoSAI) - Model Signing](https://secureai.org/)
- [ISACA - Agentic AI Audit Considerations](https://www.isaca.org/)
- [NIST AI 100-1 - Artificial Intelligence Risk Management Framework](https://doi.org/10.6028/NIST.AI.100-1)
