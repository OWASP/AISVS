# C12 Monitoring, Logging & Anomaly Detection

## Control Objective

This section provides requirements for delivering real-time and forensic visibility into what the model and other AI components see, do, and return, so threats can be detected, triaged, and learned from.

## C12.1 Request & Response Logging

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.1.1** | **Verify that** all user prompts and model responses are logged with appropriate metadata (e.g. timestamp, user ID, session ID, model version). | 1   | D/V |
| **12.1.2** | **Verify that** logs are stored in secure, access-controlled repositories with appropriate retention policies and backup procedures. | 1   | D/V |
| **12.1.3** | **Verify that** log storage systems implement encryption at rest and in transit to protect sensitive information contained in logs. | 1   | D/V |
| **12.1.4** | **Verify that** sensitive data in prompts and outputs is automatically redacted or masked before logging, with configurable redaction rules for PII, credentials, and proprietary information. | 1   | D/V |
| **12.1.5** | **Verify that** policy decisions and safety filtering actions are logged with sufficient detail to enable audit and debugging of content moderation systems. | 2   | D/V |
| **12.1.6** | **Verify that** log integrity is protected through e.g. cryptographic signatures or write-only storage. | 2   | D/V |

---

## C12.2 Abuse Detection and Alerting

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.2.1** | **Verify that** the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs using signature-based detection. | 1   | D/V |
| **12.2.2** | **Verify that** the system integrates with existing Security Information and Event Management (SIEM) platforms using standard log formats and protocols. | 1   | D/V |
| **12.2.3** | **Verify that** enriched security events include AI-specific context such as model identifiers, confidence scores, and safety filter decisions. | 2   | D/V |
| **12.2.4** | **Verify that** behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or systematic probing behaviors. | 2   | D/V |
| **12.2.5** | **Verify that** real-time alerting mechanisms notify security teams when potential policy violations or attack attempts are detected. | 2   | D/V |
| **12.2.6** | **Verify that** custom rules are included to detect AI-specific threat patterns including coordinated jailbreak attempts, prompt injection campaigns, and model extraction attacks. | 2   | D/V |
| **12.2.7** | **Verify that** automated incident response workflows can isolate compromised models, block malicious users, and escalate critical security events. | 3   | D/V |

---

## C12.3 Model Drift Detection

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.3.1** | **Verify that** the system tracks basic performance metrics such as accuracy, confidence scores, latency, and error rates across model versions and time periods. | 1   | D/V |
| **12.3.2** | **Verify that** automated alerting triggers when performance metrics exceed predefined degradation thresholds or deviate significantly from baselines. | 2   | D/V |
| **12.3.3** | **Verify that** hallucination detection monitors identify and flag instances when model outputs contain factually incorrect, inconsistent, or fabricated information. | 2   | D/V |

---

## C12.4 Performance & Behavior Telemetry

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.4.1** | **Verify that** operational metrics including request latency, token consumption, memory usage, and throughput are continuously collected and monitored. | 1   | D/V |
| **12.4.2** | **Verify that** success and failure rates are tracked with categorization of error types and their root causes. | 1   | D/V |
| **12.4.3** | **Verify that** resource utilization monitoring includes GPU/CPU usage, memory consumption, and storage requirements with alerting on threshold breaches. | 2   | D/V |

---

## C12.5 AI Incident Response Planning & Execution

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.5.1** | **Verify that** incident response plans specifically address AI-related security events including model compromise, data poisoning, and adversarial attacks. | 1   | D/V |
| **12.5.2** | **Verify that** incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2   | D/V |
| **12.5.3** | **Verify that** post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3   | D/V |

---

## C12.5 AI Performance Degradation Detection

Monitor and detect degradation in AI model performance and quality over time.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.5.1** | **Verify that** model accuracy, precision, recall, and F1 scores are continuously monitored and compared against baseline thresholds. | 1 | D/V |
| **12.5.2** | **Verify that** data drift detection monitors input distribution changes that may impact model performance. | 1 | D/V |
| **12.5.3** | **Verify that** concept drift detection identifies changes in the relationship between inputs and expected outputs. | 2 | D/V |
| **12.5.4** | **Verify that** performance degradation triggers automated alerts and initiates model retraining or replacement workflows. | 2 | D/V |
| **12.5.5** | **Verify that** degradation root cause analysis correlates performance drops with data changes, infrastructure issues, or external factors. | 3 | V |

---

## C12.6 DAG Visualization & Workflow Security

Protect workflow visualization systems from information leakage and manipulation attacks.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.6.1** | **Verify that** DAG visualization data is sanitized to remove sensitive information before storage or transmission. | 1 | D/V |
| **12.6.2** | **Verify that** workflow visualization access controls ensure only authorized users can view agent decision paths and reasoning traces. | 1 | D/V |
| **12.6.3** | **Verify that** DAG data integrity is protected through cryptographic signatures and tamper-evident storage mechanisms. | 2 | D/V |
| **12.6.4** | **Verify that** workflow visualization systems implement input validation to prevent injection attacks through crafted node or edge data. | 2 | D/V |
| **12.6.5** | **Verify that** real-time DAG updates are rate-limited and validated to prevent denial-of-service attacks on visualization systems. | 3 | D/V |

---

## C12.7 Proactive Security Behavior Monitoring

Detection and prevention of security threats through proactive agent behavior analysis.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **12.7.1** | **Verify that** proactive agent behaviors are security-validated before execution with risk assessment integration. | 1 | D/V |
| **12.7.2** | **Verify that** autonomous initiative triggers include security context evaluation and threat landscape assessment. | 2 | D/V |
| **12.7.3** | **Verify that** proactive behavior patterns are analyzed for potential security implications and unintended consequences. | 2 | D/V |
| **12.7.4** | **Verify that** security-critical proactive actions require explicit approval chains with audit trails. | 3 | D/V |
| **12.7.5** | **Verify that** behavioral anomaly detection identifies deviations in proactive agent patterns that may indicate compromise. | 3 | D/V |

---

## References

* [NIST AI Risk Management Framework 1.0 - Manage 4.1 and 4.3](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023 — AI Management Systems Requirements - Annex B 6.2.6](https://www.iso.org/standard/81230.html)
* [EU AI Act — Article 12, 13, 16 and 19 on Logging and Record-keeping](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)
