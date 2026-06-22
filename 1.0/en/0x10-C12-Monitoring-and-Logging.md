# C12 Monitoring, Logging & Anomaly Detection

## Control Objective

Deliver real-time and forensic visibility into what the model and other AI components see, do, and return, so AI-specific threats can be detected, triaged, and learned from.

This chapter focuses on controls unique to AI systems for monitoring, logging, and anomaly detection: AI-specific log content (model identifier, token usage, safety filter outcomes, prompt/response handling), AI-specific abuse and attack detection (jailbreak, prompt injection, extraction, multi-turn trajectory, covert channels over LLM endpoints), model and data drift detection, AI-specific telemetry signals (token attribution, output/input ratio anomalies), AI incident response, proactive agent behavior monitoring, and training data and model lifecycle audit logging.

---

## C12.1 Request & Response Logging

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.1.1** | **Verify that** AI interactions are logged with basic session and model context: timestamp, user ID, session ID, and model version. | 1 |
| **12.1.2** | **Verify that** AI interaction log entries include AI-specific telemetry: token count, input hash, system prompt version, confidence score where the model or provider exposes one, and safety filter outcome. | 1 |
| **12.1.3** | **Verify that** AI interaction logs exclude prompt and response content by default, and that content logging is enabled only on explicit opt-in with documented justification. | 1 |
| **12.1.4** | **Verify that** policy decisions and safety filtering actions are logged with enough detail to audit and debug content moderation systems. | 2 |
| **12.1.5** | **Verify that** log entries for AI inference events follow a structured, interoperable schema that includes at least the model identifier, token usage (input and output), provider name, and operation type, so AI observability stays consistent across tools and platforms. | 2 |
| **12.1.6** | **Verify that** full prompt and response content is logged only when a security-relevant event is detected (e.g., safety filter trigger, prompt injection detection, anomaly flag), or when required by explicit user consent and a documented legal basis. | 2 |
| **12.1.7** | **Verify that** screening logs include classifier confidence scores and policy category tags with applied stage and trace metadata. | 2 |
| **12.1.8** | **Verify that** logs record the exact hosted model identifier returned by the provider. | 2 |
| **12.1.9** | **Verify that** RAG pipeline retrieval events are logged, including the query, documents retrieved, and knowledge source. | 2 |

---

## C12.2 Abuse Detection and Alerting

Detect AI-specific attack patterns (jailbreak, prompt injection, model extraction, multi-turn trajectory attacks, covert channels over LLM endpoints) and enrich security events with AI-specific context so that downstream detection and response systems can act on them.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.2.1** | **Verify that** the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs using signature-based detection. | 1 |
| **12.2.2** | **Verify that** enriched security events include AI-specific context such as model identifiers, confidence scores, and safety filter decisions. | 2 |
| **12.2.3** | **Verify that** behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or systematic probing behaviors. | 2 |
| **12.2.4** | **Verify that** custom rules detect AI-specific threat patterns, including coordinated jailbreak attempts, prompt injection campaigns, system prompt extraction attempts, and model extraction attacks. | 2 |
| **12.2.5** | **Verify that** per-user and per-session token consumption triggers an alert when consumption exceeds defined thresholds. | 2 |
| **12.2.6** | **Verify that** automated incident response workflows can isolate compromised models and block malicious users. | 2 |
| **12.2.7** | **Verify that** extraction-alert events include offending query metadata (e.g., source principal, query volume, input distribution statistics) to support investigation. | 2 |
| **12.2.8** | **Verify that** session-level conversation trajectory analysis detects multi-turn jailbreak patterns where no single turn looks overtly malicious on its own, but the conversation as a whole shows attack indicators. | 3 |
| **12.2.9** | **Verify that** LLM API traffic is monitored for covert channel indicators, including Base64-encoded payloads, structured non-human query patterns, and communication signatures consistent with malware command-and-control activity using LLM endpoints. | 3 |

---

## C12.3 Model, Data, and Performance Drift Detection

Monitor and detect drift and degradation across model outputs, input distributions, and data schemas to identify quality regressions and security-relevant behavioral shifts.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.3.1** | **Verify that** model performance metrics (accuracy, precision, recall, F1 score, confidence scores, latency, and error rates) are continuously monitored across model versions and time periods. | 1 |
| **12.3.2** | **Verify that** data drift detection monitors input distribution changes that may impact model performance, using statistically validated methods matched to the input data type (e.g., KS test or PSI for tabular numeric features, embedding-distance metrics for text or image). | 1 |
| **12.3.3** | **Verify that** baseline performance profiles are formally documented and version-controlled, and are reviewed at a defined frequency or after any model or data pipeline change. | 2 |
| **12.3.4** | **Verify that** automated alerting triggers when performance metrics exceed predefined degradation thresholds or deviate significantly from baselines. | 2 |
| **12.3.5** | **Verify that** hallucination detection monitors identify and flag model outputs that contain factually incorrect, inconsistent, or fabricated information. | 2 |
| **12.3.6** | **Verify that** schema drift in incoming data (unexpected field additions, removals, type changes, or format variations) is detected and triggers alerting. | 2 |
| **12.3.7** | **Verify that** concept drift detection identifies changes in the relationship between inputs and expected outputs. | 2 |
| **12.3.8** | **Verify that** performance degradation alerts trigger a defined remediation workflow (e.g., manual review, retraining, or replacement). | 2 |
| **12.3.9** | **Verify that** hallucination rates are tracked as continuous time-series metrics to enable trend analysis and detection of sustained model degradation. | 2 |
| **12.3.10** | **Verify that** training pipeline instrumentation continuously monitors runtime duration, loss trajectory, and convergence rate against established baselines for equivalent dataset size and model architecture. Statistically significant deviations (e.g., abnormally prolonged training duration or erratic loss curves) trigger automated alerts and gate the resulting model artifact pending investigation, since such anomalies may indicate adversarial poisoning payloads in the training data. | 2 |
| **12.3.11** | **Verify that** degradation root cause analysis correlates performance drops with data changes, infrastructure issues, or external factors. | 3 |
| **12.3.12** | **Verify that** sudden unexplained behavioral shifts are distinguished from gradual expected operational drift, with a security escalation path defined for unexplained sudden drift. | 3 |

---

## C12.4 Performance & Behavior Telemetry

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.4.1** | **Verify that** token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | 2 |
| **12.4.2** | **Verify that** output-to-input token ratio anomalies are detected and alerted. | 2 |

---

## C12.5 AI Incident Response Planning & Execution

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.5.1** | **Verify that** incident response plans specifically address AI-related security events including model compromise, data poisoning, adversarial attacks, model inversion, prompt injection campaigns, and model extraction, with specific containment and investigation steps for each scenario. | 1 |
| **12.5.2** | **Verify that** incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2 |
| **12.5.3** | **Verify that** post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3 |

---

## C12.6 Proactive Security Behavior Monitoring

Detect and prevent security threats arising from proactive (agent-initiated) behavior, including pre-execution validation, behavior pattern analysis, and audit trails for approval of security-critical actions.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.6.1** | **Verify that** proactive agent behaviors are security-validated before execution, including integration with risk assessment. | 1 |
| **12.6.2** | **Verify that** autonomous initiative triggers include security context evaluation and threat landscape assessment. | 2 |
| **12.6.3** | **Verify that** proactive behavior patterns are analyzed for potential security implications and unintended consequences. | 2 |
| **12.6.4** | **Verify that** audit logs capture the complete approval chain for security-critical proactive actions, including approver identity, timestamp, action parameters, and decision outcome. | 2 |
| **12.6.5** | **Verify that** audit log records include identity, scope, authorization decisions, tool parameters, and outcomes. | 2 |
| **12.6.6** | **Verify that** kill-switch activations and override commands are logged. | 2 |
| **12.6.7** | **Verify that** self-modifications are explicitly classified as security-relevant events and logged with sufficient detail to reconstruct what changed, when, by which agent or principal, and under what authorization. | 2 |
| **12.6.8** | **Verify that** behavioral anomaly detection identifies deviations in proactive agent patterns that may indicate compromise. | 3 |

---

## C12.7 Training Data & Model Lifecycle Audit

Ensure that the provenance and change history of training data, model artifacts, and knowledge sources are auditable throughout the AI development lifecycle.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.7.1** | **Verify that** the lineage of each dataset and its components, including all transformations, augmentations, and merges, is recorded and can be reconstructed. | 1 |
| **12.7.2** | **Verify that** all labeling activities are recorded in logs. | 1 |
| **12.7.3** | **Verify that** all model changes (deployment, configuration, retirement) generate immutable audit records. | 2 |
| **12.7.4** | **Verify that** every ingested document is tagged at write time with source, writer identity, and timestamp. | 2 |
| **12.7.5** | **Verify that** all training datasets are uniquely identified, with change tracking, to support rollback and forensic analysis. | 3 |

---

## References

* [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [MITRE ATLAS - Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
* [NIST AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
* [NIST SP 800-207 Zero Trust Architecture](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf)
* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
