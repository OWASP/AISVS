# C12 Monitoring, Logging & Anomaly Detection

## Control Objective

Deliver real-time and forensic visibility into what the model and other AI components see, do, and return, so AI-specific threats can be detected, triaged, and learned from.

This chapter focuses on controls unique to AI systems for monitoring, logging, and anomaly detection: AI-specific log content (model identifier, token usage, safety filter outcomes, prompt/response handling), AI-specific abuse and attack detection (jailbreak, prompt injection, extraction, multi-turn trajectory, covert channels over LLM endpoints), model and data drift detection, AI-specific telemetry signals (token attribution, output/input ratio anomalies), AI incident response, proactive agent behavior monitoring, and training data and model lifecycle audit logging.

---

## C12.1 Request & Response Logging

AI specific components must include appropriate request and response logging to create audit trail and support incident response.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.1.1** | **Verify that** AI interactions are logged with session context and AI-specific telemetry. | 1 |
| **12.1.2** | **Verify that** safety filtering and policy decisions are logged with sufficient detail to support audit, debugging, and forensic analysis of content moderation systems. | 2 |
| **12.1.3** | **Verify that** log entries for AI inference events follow a structured, interoperable schema that includes at least the model identifier, token usage (input and output), provider name, and operation type. | 2 |
| **12.1.4** | **Verify that** RAG pipeline retrieval events are logged, including the query, documents retrieved, and knowledge source. | 2 |

---

## C12.2 Detection and Alerting

Detect AI-specific attack patterns (jailbreak, prompt injection, model extraction, multi-turn trajectory attacks, covert channels over LLM endpoints) and enrich security events with AI-specific context so that downstream detection and response systems can act on them.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.2.1** | **Verify that** the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs. | 1 |
| **12.2.2** | **Verify that** behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or probing behaviors. | 2 |
| **12.2.3** | **Verify that** custom rules detect AI-specific threat patterns for coordinated jailbreak attempts, prompt injection, and system prompt extraction attempts. | 2 |
| **12.2.4** | **Verify that** extraction-alert events include offending query metadata to support investigation. | 2 |
| **12.2.5** | **Verify that** token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | 2 |
| **12.2.6** | **Verify that** LLM API traffic is monitored for covert-channel indicators and communication signatures to identify malware and command-and-control (C2) activity. | 3 |

---

## C12.3 Model, Data, and Performance Drift Detection

Monitor and detect drift and degradation across model outputs, input distributions, and data schemas to identify quality regressions and security-relevant behavioral shifts.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.3.1** | **Verify that** data drift detection monitors input distribution changes that may impact model performance, using statistically validated methods matched to the input data type (e.g., KS test or PSI for tabular numeric features, embedding-distance metrics for text or image). | 1 |
| **12.3.2** | **Verify that** hallucination detection monitors identify and flag model outputs that contain factually incorrect, inconsistent, or fabricated information. | 2 |
| **12.3.3** | **Verify that** hallucination rates are tracked as continuous time-series metrics to enable trend analysis and detection of sustained model degradation. | 2 |
| **12.3.4** | **Verify that** unexplained behavioral shifts are distinguished from gradual, expected operational drift. | 3 |

---

## C12.4 AI Incident Response Planning & Execution

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.4.1** | **Verify that** incident response plans address AI-related security events with containment and investigation steps for each scenario. | 1 |
| **12.4.2** | **Verify that** incident response teams have access to forensic AI-specific capabilities. | 2 |
| **12.4.3** | **Verify that** automated incident response workflows can isolate compromised models and block malicious users. | 2 |
| **12.4.4** | **Verify that** post-incident analysis includes model retraining and safety filter updates. | 3 |

---

## C12.5 Proactive Security Behavior Monitoring

Detect and prevent security threats arising from proactive (agent-initiated) behavior, including pre-execution validation, behavior pattern analysis, and audit trails for approval of security-critical actions.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.5.1** | **Verify that** autonomous action triggers include proactive behavior-pattern analysis, security evaluation, and threat-landscape assessment. | 2 |
| **12.5.2** | **Verify that** audit logs capture security-critical proactive actions, including approver identity, timestamp, action parameters, and decision outcomes. | 2 |
| **12.5.3** | **Verify that** kill-switch activations and override commands are logged. | 2 |

---

## C12.6 Training Data & Model Lifecycle Audit

Ensure that the provenance and change history of training data, model artifacts, and knowledge sources are auditable throughout the AI development lifecycle.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.6.1** | **Verify that** dataset lineage records each dataset and its components, including all transformations, augmentations, and merges. | 1 |
| **12.6.2** | **Verify that** all labeling activities are recorded in logs. | 1 |
| **12.6.3** | **Verify that** all model changes generate immutable audit records. | 2 |
| **12.6.4** | **Verify that** every ingested document is tagged at write time with source, writer identity, and timestamp. | 2 |

---

## References

* [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [MITRE ATLAS - Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
* [NIST AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
* [NIST SP 800-207 Zero Trust Architecture](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf)
