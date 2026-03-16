# C13 Monitoring, Logging & Anomaly Detection

## Control Objective

This section provides requirements for delivering real-time and forensic visibility into what the model and other AI components see, do, and return, so threats can be detected, triaged, and learned from.

## C13.1 Request & Response Logging

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.1.1** | **Verify that** all user prompts and model responses are logged with appropriate metadata (e.g. timestamp, user ID, session ID, model version, input hash, system prompt version, and safety filter decisions). | 1   | D/V |
| **13.1.2** | **Verify that** logs are stored in secure, access-controlled repositories with appropriate retention policies and backup procedures. | 1   | D/V |
| **13.1.3** | **Verify that** log storage systems implement encryption at rest and in transit to protect sensitive information contained in logs. | 1   | D/V |
| **13.1.4** | **Verify that** sensitive data in prompts and outputs is automatically redacted or masked before logging, with configurable redaction rules for PII, credentials, and proprietary information. | 1   | D/V |
| **13.1.5** | **Verify that** policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2   | D/V |
| **13.1.6** | **Verify that** log integrity is protected through e.g. cryptographic signatures or write-only storage. | 2   | D/V |
| **13.1.7** | **Verify that** log entries for AI inference events capture a structured, interoperable schema that includes at minimum model identifier, token usage (input and output), provider name, and operation type, to enable consistent AI observability across tools and platforms. | 2   | D/V |

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
| **13.2.8** | **Verify that** session-level conversation trajectory analysis detects multi-turn jailbreak patterns where no individual turn is overtly malicious in isolation but the aggregate conversation exhibits attack indicators. | 3   | D/V |
| **13.2.9** | **Verify that** per-user and per-session token consumption is tracked, with anomaly detection alerting when consumption exceeds defined thresholds. | 2   | D/V |
| **13.2.10** | **Verify that** LLM API traffic is monitored for covert channel indicators, including Base64-encoded payloads, structured non-human query patterns, and communication signatures consistent with malware command-and-control activity using LLM endpoints. | 3   | D/V |

---

## C13.3 Model Drift Detection

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.3.1** | **Verify that** the system tracks basic performance metrics such as accuracy, confidence scores, latency, and error rates across model versions and time periods. | 1   | D/V |
| **13.3.2** | **Verify that** automated alerting triggers when performance metrics exceed predefined degradation thresholds or deviate significantly from baselines. | 2   | D/V |
| **13.3.3** | **Verify that** hallucination detection monitors identify and flag instances when model outputs contain factually incorrect, inconsistent, or fabricated information, and that hallucination rates are tracked as continuous time-series metrics to enable trend analysis and detection of sustained model degradation. | 2   | D/V |
| **13.3.4** | **Verify that** schema drift in incoming data (unexpected field additions, removals, type changes, or format variations) is detected and triggers alerting. | 2   | D/V |
| **13.3.5** | **Verify that** sudden unexplained behavioral shifts are distinguished from gradual expected operational drift, with a security escalation path defined for unexplained sudden drift. | 3   | V |

---

## C13.4 Performance & Behavior Telemetry

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.4.1** | **Verify that** operational metrics including request latency, token consumption, memory usage, and throughput are continuously collected and monitored. | 1   | D/V |
| **13.4.2** | **Verify that** success and failure rates are tracked with categorization of error types and their root causes. | 1   | D/V |
| **13.4.3** | **Verify that** resource utilization monitoring includes GPU/CPU usage, memory consumption, and storage requirements with alerting on threshold breaches. | 2   | D/V |
| **13.4.4** | **Verify that** token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | 2   | D/V |
| **13.4.5** | **Verify that** output-to-input token ratio anomalies are detected and alerted. | 2   | D/V |

---

## C13.5 AI Incident Response Planning & Execution

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.5.1** | **Verify that** incident response plans specifically address AI-related security events including model compromise, data poisoning, adversarial attacks, model inversion, prompt injection campaigns, and model extraction, with specific containment and investigation steps for each scenario. | 1   | D/V |
| **13.5.2** | **Verify that** incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2   | D/V |
| **13.5.3** | **Verify that** post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3   | D/V |

---

## C13.6 AI Performance Degradation Detection

Monitor and detect degradation in AI model performance and quality over time.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **13.6.1** | **Verify that** model accuracy, precision, recall, and F1 scores are continuously monitored and compared against baseline thresholds. | 1 | D/V |
| **13.6.2** | **Verify that** data drift detection monitors input distribution changes that may impact model performance, using statistically validated methods appropriate to the data type. | 1 | D/V |
| **13.6.3** | **Verify that** concept drift detection identifies changes in the relationship between inputs and expected outputs. | 2 | D/V |
| **13.6.4** | **Verify that** performance degradation triggers automated alerts and initiates model retraining or replacement workflows. | 2 | D/V |
| **13.6.5** | **Verify that** degradation root cause analysis correlates performance drops with data changes, infrastructure issues, or external factors. | 3 | V |
| **13.6.6** | **Verify that** baseline performance profiles are formally documented and version-controlled, reviewed at an appropriate frequency. | 2 | D/V |

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

---

## References

* [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [MITRE ATLAS - Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
* [NIST AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf)
* [NIST AI 100-1 - Artificial Intelligence Risk Management Framework](https://doi.org/10.6028/NIST.AI.100-1)
