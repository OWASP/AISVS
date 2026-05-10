# C13 Monitoring, Logging & Anomaly Detection

## Control Objective

Deliver real-time and forensic visibility into what the model and other AI components see, do, and return, so AI-specific threats can be detected, triaged, and learned from.

This chapter focuses on controls unique to AI systems for monitoring, logging and anomaly detection: AI-specific log content (model identifier, token usage, safety filter outcomes, prompt/response handling), AI-specific abuse and attack detection (jailbreak, prompt injection, extraction, multi-turn trajectory, covert channels over LLM endpoints), model and data drift detection, AI-specific telemetry signals (token attribution, output/input ratio anomalies), AI incident response, and proactive agent behavior monitoring.

Generic logging and operational controls (log storage access control, retention, backup, encryption at rest and in transit, sensitive-data redaction and masking, log tamper protection, SIEM integration, log shipping to a separate analysis system, generic alerting workflows, and operational telemetry such as latency, throughput, success/failure rates, error categorization, and CPU/GPU/memory/storage utilization) are covered by ASVS v5 (V12, V14, V16) and standard observability practice and are not repeated here; RAG retrieval logging is covered by C8.1.4, agent audit logging by C9.4, human approval and override logging by C14.3, and AI supply-chain incident response by C6.4.

---

## C13.1 Request & Response Logging

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **13.1.1** | **Verify that** AI interactions are logged with security-relevant metadata (e.g., timestamp, user ID, session ID, model version, token count, input hash, system prompt version, confidence score, safety filter outcome, and safety filter decisions). | 1 |
| **13.1.2** | **Verify that** AI interaction logs exclude prompt and response content by default, and that content logging is enabled only on explicit opt-in with documented justification. | 1 |
| **13.1.3** | **Verify that** policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2 |
| **13.1.4** | **Verify that** log entries for AI inference events capture a structured, interoperable schema that includes at minimum model identifier, token usage (input and output), provider name, and operation type, to enable consistent AI observability across tools and platforms. | 2 |
| **13.1.5** | **Verify that** full prompt and response content is logged only when a security-relevant event is detected (e.g., safety filter trigger, prompt injection detection, anomaly flag), or when required by explicit user consent and a documented legal basis. | 2 |

---

## C13.2 Abuse Detection and Alerting

Detect AI-specific attack patterns (jailbreak, prompt injection, model extraction, multi-turn trajectory attacks, covert channels over LLM endpoints) and enrich security events with AI-specific context so that downstream detection and response systems can act on them.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **13.2.1** | **Verify that** the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs using signature-based detection. | 1 |
| **13.2.2** | **Verify that** enriched security events include AI-specific context such as model identifiers, confidence scores, and safety filter decisions. | 2 |
| **13.2.3** | **Verify that** behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or systematic probing behaviors. | 2 |
| **13.2.4** | **Verify that** custom rules are included to detect AI-specific threat patterns including coordinated jailbreak attempts, prompt injection campaigns, system prompt extraction attempts, and model extraction attacks. | 2 |
| **13.2.5** | **Verify that** per-user and per-session token consumption triggers an alert when consumption exceeds defined thresholds. | 2 |
| **13.2.6** | **Verify that** automated incident response workflows can isolate compromised models and block malicious users. | 3 |
| **13.2.7** | **Verify that** session-level conversation trajectory analysis detects multi-turn jailbreak patterns where no individual turn is overtly malicious in isolation but the aggregate conversation exhibits attack indicators. | 3 |
| **13.2.8** | **Verify that** LLM API traffic is monitored for covert channel indicators, including Base64-encoded payloads, structured non-human query patterns, and communication signatures consistent with malware command-and-control activity using LLM endpoints. | 3 |

---

## C13.3 Model, Data, and Performance Drift Detection

Monitor and detect drift and degradation across model outputs, input distributions, and data schemas to identify quality regressions and security-relevant behavioral shifts.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **13.3.1** | **Verify that** model performance metrics (accuracy, precision, recall, F1 score, confidence scores, latency, and error rates) are continuously monitored across model versions and time periods. | 1 |
| **13.3.2** | **Verify that** data drift detection monitors input distribution changes that may impact model performance, using statistically validated methods appropriate to the data type. | 1 |
| **13.3.3** | **Verify that** baseline performance profiles are formally documented and version-controlled, and are reviewed at a defined frequency or after any model or data pipeline change. | 2 |
| **13.3.4** | **Verify that** automated alerting triggers when performance metrics exceed predefined degradation thresholds or deviate significantly from baselines. | 2 |
| **13.3.5** | **Verify that** hallucination detection monitors identify and flag instances when model outputs contain factually incorrect, inconsistent, or fabricated information. | 2 |
| **13.3.6** | **Verify that** schema drift in incoming data (unexpected field additions, removals, type changes, or format variations) is detected and triggers alerting. | 2 |
| **13.3.7** | **Verify that** concept drift detection identifies changes in the relationship between inputs and expected outputs. | 2 |
| **13.3.8** | **Verify that** performance degradation alerts trigger a defined remediation workflow (e.g., manual review, retraining, or replacement). | 2 |
| **13.3.9** | **Verify that** hallucination rates are tracked as continuous time-series metrics to enable trend analysis and detection of sustained model degradation. | 2 |
| **13.3.10** | **Verify that** training pipeline instrumentation continuously monitors runtime duration, loss trajectory, and convergence rate against established baselines for equivalent dataset size and model architecture, and that statistically significant deviations (e.g., abnormally prolonged training duration or erratic loss curves) trigger automated alerts and gating of the resulting model artifact pending investigation, as such anomalies may indicate the presence of adversarial poisoning payloads in the training data. | 2 |
| **13.3.11** | **Verify that** degradation root cause analysis correlates performance drops with data changes, infrastructure issues, or external factors. | 3 |
| **13.3.12** | **Verify that** sudden unexplained behavioral shifts are distinguished from gradual expected operational drift, with a security escalation path defined for unexplained sudden drift. | 3 |

---

## C13.4 Performance & Behavior Telemetry

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **13.4.1** | **Verify that** token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | 2 |
| **13.4.2** | **Verify that** output-to-input token ratio anomalies are detected and alerted. | 2 |

---

## C13.5 AI Incident Response Planning & Execution

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **13.5.1** | **Verify that** incident response plans specifically address AI-related security events including model compromise, data poisoning, adversarial attacks, model inversion, prompt injection campaigns, and model extraction, with specific containment and investigation steps for each scenario. | 1 |
| **13.5.2** | **Verify that** incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2 |
| **13.5.3** | **Verify that** post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3 |

---

## C13.6 Proactive Security Behavior Monitoring

Detect and prevent security threats arising from proactive (agent-initiated) behavior, including pre-execution validation, behavior pattern analysis, and audit trails for approval of security-critical actions.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **13.6.1** | **Verify that** proactive agent behaviors are security-validated before execution with risk assessment integration. | 1 |
| **13.6.2** | **Verify that** autonomous initiative triggers include security context evaluation and threat landscape assessment. | 2 |
| **13.6.3** | **Verify that** proactive behavior patterns are analyzed for potential security implications and unintended consequences. | 2 |
| **13.6.4** | **Verify that** audit logs capture the complete approval chain for security-critical proactive actions, including approver identity, timestamp, action parameters, and decision outcome. | 3 |
| **13.6.5** | **Verify that** behavioral anomaly detection identifies deviations in proactive agent patterns that may indicate compromise. | 3 |

---

## References

* [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [MITRE ATLAS - Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
* [NIST AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
* [NIST AI 100-1 - Artificial Intelligence Risk Management Framework](https://doi.org/10.6028/NIST.AI.100-1)
* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
* [NIST SP 800-207 Zero Trust Architecture](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf)
