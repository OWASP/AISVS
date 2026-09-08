<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C12-Monitoring-and-Logging.md -->
<!-- Translator: GeeksikhSecurity -->

# C12 Monitoring, Logging & Anomaly Detection
# C12 ਨਿਗਰਾਨੀ, ਲੌਗਿੰਗ ਅਤੇ ਅਸਧਾਰਨਤਾ ਪਛਾਣ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses real-time and forensic visibility into what the model and other AI components see, do, and return, so that AI-specific threats can be detected and triaged.

ਇਹ ਅਧਿਆਇ ਇਸ ਗੱਲ ਵਿੱਚ ਰੀਅਲ-ਟਾਈਮ ਅਤੇ ਫ਼ੋਰੈਂਸਿਕ ਦਿੱਖ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ ਕਿ ਮਾਡਲ ਅਤੇ ਹੋਰ AI ਹਿੱਸੇ ਕੀ ਦੇਖਦੇ ਹਨ, ਕੀ ਕਰਦੇ ਹਨ, ਅਤੇ ਕੀ ਵਾਪਸ ਦਿੰਦੇ ਹਨ, ਤਾਂ ਜੋ AI-ਵਿਸ਼ੇਸ਼ ਖ਼ਤਰਿਆਂ ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾ ਸਕੇ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਤਰਜੀਹ-ਕ੍ਰਮ (triage) ਦਿੱਤਾ ਜਾ ਸਕੇ।

---

## C12.1 Request & Response Logging
## C12.1 ਬੇਨਤੀ ਅਤੇ ਜਵਾਬ ਲੌਗਿੰਗ

AI requests and responses must be logged to create an audit trail and support incident response.

AI ਬੇਨਤੀਆਂ ਅਤੇ ਜਵਾਬਾਂ ਦਾ ਲੌਗ ਕੀਤਾ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ ਤਾਂ ਜੋ ਇੱਕ ਆਡਿਟ ਟ੍ਰੇਲ (audit trail) ਬਣਾਈ ਜਾ ਸਕੇ ਅਤੇ ਘਟਨਾ ਜਵਾਬ (incident response) ਦਾ ਸਮਰਥਨ ਕੀਤਾ ਜਾ ਸਕੇ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.1.1** | **Verify that** AI interactions are logged with session context and AI-specific telemetry. | 1 |
| **12.1.2** | **Verify that** safety filtering and policy decisions are logged with sufficient detail to support audit, debugging, and forensic analysis of content moderation systems. | 2 |
| **12.1.3** | **Verify that** log entries for AI inference events follow a structured, interoperable schema that includes at least the model identifier, token usage (input and output), provider name, and operation type. | 2 |
| **12.1.4** | **Verify that** RAG pipeline retrieval events are logged, including the query, documents retrieved, and knowledge source. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਪਰਸਪਰ-ਕਿਰਿਆਵਾਂ ਨੂੰ ਸੈਸ਼ਨ ਸੰਦਰਭ ਅਤੇ AI-ਵਿਸ਼ੇਸ਼ ਟੈਲੀਮੈਟਰੀ ਸਮੇਤ ਲੌਗ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **12.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਲਾਮਤੀ ਫ਼ਿਲਟਰਿੰਗ ਅਤੇ ਨੀਤੀ ਫ਼ੈਸਲਿਆਂ ਨੂੰ ਇੰਨੇ ਵੇਰਵੇ ਨਾਲ ਲੌਗ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਕਿ ਸਮੱਗਰੀ ਮਾਡਰੇਸ਼ਨ (content moderation) ਸਿਸਟਮਾਂ ਦੇ ਆਡਿਟ, ਡੀਬੱਗਿੰਗ, ਅਤੇ ਫ਼ੋਰੈਂਸਿਕ ਵਿਸ਼ਲੇਸ਼ਣ ਦਾ ਸਮਰਥਨ ਕੀਤਾ ਜਾ ਸਕੇ। | 2 |
| **12.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਇਨਫ਼ਰੈਂਸ ਘਟਨਾਵਾਂ ਲਈ ਲੌਗ ਐਂਟਰੀਆਂ ਇੱਕ ਢਾਂਚਾਗਤ, ਅੰਤਰ-ਕਾਰਜਸ਼ੀਲ ਸਕੀਮਾ ਦੀ ਪਾਲਣਾ ਕਰਦੀਆਂ ਹਨ ਜਿਸ ਵਿੱਚ ਘੱਟੋ-ਘੱਟ ਮਾਡਲ ਪਛਾਣਕਰਤਾ, ਟੋਕਨ ਵਰਤੋਂ (ਇਨਪੁੱਟ ਅਤੇ ਆਊਟਪੁੱਟ), ਪ੍ਰਦਾਤਾ ਦਾ ਨਾਮ, ਅਤੇ ਸੰਚਾਲਨ ਕਿਸਮ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **12.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** RAG ਪਾਈਪਲਾਈਨ ਦੀਆਂ ਪ੍ਰਾਪਤੀ ਘਟਨਾਵਾਂ ਨੂੰ ਲੌਗ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਕਿਊਰੀ (query), ਪ੍ਰਾਪਤ ਕੀਤੇ ਦਸਤਾਵੇਜ਼, ਅਤੇ ਗਿਆਨ ਸਰੋਤ ਸ਼ਾਮਲ ਹਨ। | 2 |

---

## C12.2 Detection and Alerting
## C12.2 ਪਛਾਣ ਅਤੇ ਚੇਤਾਵਨੀ

AI-specific attack patterns (jailbreak, prompt injection, model extraction, multi-turn trajectory attacks, covert channels over LLM endpoints) must be detected, and security events enriched with AI-specific context so downstream detection and response systems can act on them.

AI-ਵਿਸ਼ੇਸ਼ ਹਮਲਾ ਪੈਟਰਨਾਂ (jailbreak, prompt ਇੰਜੈਕਸ਼ਨ, model extraction, ਬਹੁ-ਵਾਰੀ trajectory ਹਮਲੇ, LLM ਐਂਡਪੁਆਇੰਟਾਂ ਉੱਤੇ ਲੁਕਵੇਂ ਚੈਨਲ) ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਸੁਰੱਖਿਆ ਘਟਨਾਵਾਂ ਨੂੰ AI-ਵਿਸ਼ੇਸ਼ ਸੰਦਰਭ ਨਾਲ ਸੰਪੰਨ ਕੀਤਾ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ ਤਾਂ ਜੋ ਡਾਊਨਸਟ੍ਰੀਮ ਪਛਾਣ ਅਤੇ ਜਵਾਬ ਸਿਸਟਮ ਉਹਨਾਂ ਉੱਤੇ ਕਾਰਵਾਈ ਕਰ ਸਕਣ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.2.1** | **Verify that** the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs. | 1 |
| **12.2.2** | **Verify that** behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or probing behaviors. | 2 |
| **12.2.3** | **Verify that** custom rules detect AI-specific threat patterns for coordinated jailbreak attempts, prompt injection, and system prompt extraction attempts. | 2 |
| **12.2.4** | **Verify that** extraction-alert events include offending query metadata to support investigation. | 2 |
| **12.2.5** | **Verify that** token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | 2 |
| **12.2.6** | **Verify that** LLM API traffic is monitored for covert-channel indicators and communication signatures to identify malware and command-and-control (C2) activity. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਸਟਮ ਜਾਣੇ-ਪਛਾਣੇ jailbreak ਪੈਟਰਨਾਂ, prompt ਇੰਜੈਕਸ਼ਨ ਦੀਆਂ ਕੋਸ਼ਿਸ਼ਾਂ, ਅਤੇ ਵਿਰੋਧੀ ਇਨਪੁੱਟਾਂ ਦਾ ਪਤਾ ਲਗਾਉਂਦਾ ਹੈ ਅਤੇ ਉਹਨਾਂ ਬਾਰੇ ਚੇਤਾਵਨੀ ਦਿੰਦਾ ਹੈ। | 1 |
| **12.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਵਿਵਹਾਰਕ ਅਸਧਾਰਨਤਾ ਪਛਾਣ (anomaly detection) ਅਸਧਾਰਨ ਗੱਲਬਾਤ ਪੈਟਰਨਾਂ, ਹੱਦੋਂ ਵੱਧ ਮੁੜ-ਕੋਸ਼ਿਸ਼ਾਂ, ਜਾਂ ਟੋਹ ਲੈਣ ਵਾਲੇ ਵਿਵਹਾਰਾਂ ਦੀ ਪਛਾਣ ਕਰਦੀ ਹੈ। | 2 |
| **12.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕਸਟਮ ਨਿਯਮ ਤਾਲਮੇਲ ਵਾਲੀਆਂ jailbreak ਕੋਸ਼ਿਸ਼ਾਂ, prompt ਇੰਜੈਕਸ਼ਨ, ਅਤੇ system prompt ਕੱਢਣ (extraction) ਦੀਆਂ ਕੋਸ਼ਿਸ਼ਾਂ ਲਈ AI-ਵਿਸ਼ੇਸ਼ ਖ਼ਤਰਾ ਪੈਟਰਨਾਂ ਦਾ ਪਤਾ ਲਗਾਉਂਦੇ ਹਨ। | 2 |
| **12.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** extraction (ਕੱਢਣ) ਦੀਆਂ ਚੇਤਾਵਨੀ ਘਟਨਾਵਾਂ ਵਿੱਚ ਤਫ਼ਤੀਸ਼ ਦਾ ਸਮਰਥਨ ਕਰਨ ਲਈ ਦੋਸ਼ੀ ਕਿਊਰੀ ਦਾ ਮੈਟਾਡਾਟਾ ਸ਼ਾਮਲ ਹੁੰਦਾ ਹੈ। | 2 |
| **12.2.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਟੋਕਨ ਵਰਤੋਂ ਨੂੰ ਬਾਰੀਕ ਨਿਰਧਾਰਨ ਪੱਧਰਾਂ (attribution levels) ਉੱਤੇ ਟਰੈਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਪ੍ਰਤੀ ਉਪਭੋਗਤਾ, ਪ੍ਰਤੀ ਸੈਸ਼ਨ, ਪ੍ਰਤੀ ਫ਼ੀਚਰ ਐਂਡਪੁਆਇੰਟ, ਅਤੇ ਪ੍ਰਤੀ ਟੀਮ ਜਾਂ ਵਰਕਸਪੇਸ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **12.2.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਲਵੇਅਰ ਅਤੇ command-and-control (C2) ਗਤੀਵਿਧੀ ਦੀ ਪਛਾਣ ਕਰਨ ਲਈ LLM API ਟ੍ਰੈਫ਼ਿਕ ਦੀ ਲੁਕਵੇਂ-ਚੈਨਲ ਸੰਕੇਤਾਂ ਅਤੇ ਸੰਚਾਰ ਸਿਗਨੇਚਰਾਂ (signatures) ਲਈ ਨਿਗਰਾਨੀ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 3 |

---

## C12.3 Model, Data, and Performance Drift Detection
## C12.3 ਮਾਡਲ, ਡਾਟਾ, ਅਤੇ ਕਾਰਗੁਜ਼ਾਰੀ ਡ੍ਰਿਫ਼ਟ ਪਛਾਣ

Drift and degradation across model outputs, input distributions, and data schemas must be monitored to identify quality regressions and security-relevant behavioral shifts.

ਗੁਣਵੱਤਾ ਦੇ ਰਿਗਰੈਸ਼ਨਾਂ (regressions) ਅਤੇ ਸੁਰੱਖਿਆ-ਸੰਬੰਧਿਤ ਵਿਵਹਾਰਕ ਤਬਦੀਲੀਆਂ ਦੀ ਪਛਾਣ ਕਰਨ ਲਈ ਮਾਡਲ ਆਊਟਪੁੱਟ, ਇਨਪੁੱਟ ਵੰਡਾਂ, ਅਤੇ ਡਾਟਾ ਸਕੀਮਾਂ ਵਿੱਚ ਡ੍ਰਿਫ਼ਟ (drift) ਅਤੇ ਨਿਘਾਰ ਦੀ ਨਿਗਰਾਨੀ ਕੀਤੀ ਜਾਣੀ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.3.1** | **Verify that** data drift detection monitors input distribution changes that may impact model performance, using statistically validated methods matched to the input data type (e.g., KS test or PSI for tabular numeric features, embedding-distance metrics for text or image). | 1 |
| **12.3.2** | **Verify that** hallucination detection monitors identify and flag model outputs that contain factually incorrect, inconsistent, or fabricated information. | 2 |
| **12.3.3** | **Verify that** hallucination rates are tracked as continuous time-series metrics to enable trend analysis and detection of sustained model degradation. | 2 |
| **12.3.4** | **Verify that** unexplained behavioral shifts are distinguished from gradual, expected operational drift. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡਾਟਾ ਡ੍ਰਿਫ਼ਟ ਪਛਾਣ ਇਨਪੁੱਟ ਵੰਡ ਵਿੱਚ ਹੋਣ ਵਾਲੀਆਂ ਉਹਨਾਂ ਤਬਦੀਲੀਆਂ ਦੀ ਨਿਗਰਾਨੀ ਕਰਦੀ ਹੈ ਜੋ ਮਾਡਲ ਦੀ ਕਾਰਗੁਜ਼ਾਰੀ ਨੂੰ ਪ੍ਰਭਾਵਿਤ ਕਰ ਸਕਦੀਆਂ ਹਨ, ਅਤੇ ਇਸ ਲਈ ਇਨਪੁੱਟ ਡਾਟਾ ਦੀ ਕਿਸਮ ਨਾਲ ਮੇਲ ਖਾਂਦੀਆਂ ਅੰਕੜਾ-ਪੱਖੋਂ ਪ੍ਰਮਾਣਿਤ ਵਿਧੀਆਂ ਵਰਤਦੀ ਹੈ (ਜਿਵੇਂ, ਸਾਰਣੀਬੱਧ ਸੰਖਿਆਤਮਕ ਫ਼ੀਚਰਾਂ ਲਈ KS test ਜਾਂ PSI, ਟੈਕਸਟ ਜਾਂ ਚਿੱਤਰ ਲਈ embedding-ਦੂਰੀ ਮੈਟ੍ਰਿਕ)। | 1 |
| **12.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** hallucination ਪਛਾਣ ਨਿਗਰਾਨ ਉਹਨਾਂ ਮਾਡਲ ਆਊਟਪੁੱਟਾਂ ਦੀ ਪਛਾਣ ਕਰਦੇ ਹਨ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਨਿਸ਼ਾਨਬੱਧ ਕਰਦੇ ਹਨ ਜਿਨ੍ਹਾਂ ਵਿੱਚ ਤੱਥਾਂ ਪੱਖੋਂ ਗ਼ਲਤ, ਅਸੰਗਤ, ਜਾਂ ਮਨਘੜਤ ਜਾਣਕਾਰੀ ਹੁੰਦੀ ਹੈ। | 2 |
| **12.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** hallucination ਦਰਾਂ ਨੂੰ ਲਗਾਤਾਰ ਸਮਾਂ-ਲੜੀ ਮੈਟ੍ਰਿਕਾਂ ਵਜੋਂ ਟਰੈਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਤਾਂ ਜੋ ਰੁਝਾਨ ਵਿਸ਼ਲੇਸ਼ਣ ਅਤੇ ਲਗਾਤਾਰ ਬਣੇ ਰਹਿਣ ਵਾਲੇ ਮਾਡਲ ਨਿਘਾਰ ਦੀ ਪਛਾਣ ਸੰਭਵ ਹੋ ਸਕੇ। | 2 |
| **12.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਅਣ-ਵਿਆਖਿਆਤ ਵਿਵਹਾਰਕ ਤਬਦੀਲੀਆਂ ਨੂੰ ਹੌਲੀ-ਹੌਲੀ ਹੋਣ ਵਾਲੇ, ਅਨੁਮਾਨਿਤ ਸੰਚਾਲਨ ਡ੍ਰਿਫ਼ਟ ਤੋਂ ਵੱਖਰਾ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 3 |

---

## C12.4 Proactive Security Behavior Monitoring
## C12.4 ਪੂਰਵ-ਸਰਗਰਮ ਸੁਰੱਖਿਆ ਵਿਵਹਾਰ ਨਿਗਰਾਨੀ

Security threats arising from proactive (agent-initiated) behavior must be detected and prevented, including pre-execution validation, behavior pattern analysis, and audit trails for approval of security-critical actions.

ਪੂਰਵ-ਸਰਗਰਮ (proactive — ਭਾਵ ਏਜੰਟ ਵੱਲੋਂ ਸ਼ੁਰੂ ਕੀਤੇ) ਵਿਵਹਾਰ ਤੋਂ ਪੈਦਾ ਹੋਣ ਵਾਲੇ ਸੁਰੱਖਿਆ ਖ਼ਤਰਿਆਂ ਦਾ ਪਤਾ ਲਗਾਇਆ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਰੋਕਿਆ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ, ਜਿਸ ਵਿੱਚ ਐਗਜ਼ੀਕਿਊਸ਼ਨ-ਪੂਰਵ ਪ੍ਰਮਾਣਿਕਤਾ, ਵਿਵਹਾਰ ਪੈਟਰਨ ਵਿਸ਼ਲੇਸ਼ਣ, ਅਤੇ ਸੁਰੱਖਿਆ-ਨਾਜ਼ੁਕ ਕਾਰਵਾਈਆਂ ਦੀ ਮਨਜ਼ੂਰੀ ਲਈ ਆਡਿਟ ਟ੍ਰੇਲ ਸ਼ਾਮਲ ਹਨ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.4.1** | **Verify that** autonomous action triggers include proactive behavior-pattern analysis, security evaluation, and threat-landscape assessment. | 2 |
| **12.4.2** | **Verify that** audit logs capture security-critical proactive actions, including approver identity, timestamp, action parameters, and decision outcomes. | 2 |
| **12.4.3** | **Verify that** kill-switch activations and override commands are logged. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.4.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਕਾਰਵਾਈ ਦੇ ਟ੍ਰਿਗਰਾਂ ਵਿੱਚ ਪੂਰਵ-ਸਰਗਰਮ ਵਿਵਹਾਰ-ਪੈਟਰਨ ਵਿਸ਼ਲੇਸ਼ਣ, ਸੁਰੱਖਿਆ ਮੁਲਾਂਕਣ, ਅਤੇ ਖ਼ਤਰਾ-ਪਰਿਦ੍ਰਿਸ਼ ਮੁਲਾਂਕਣ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **12.4.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਆਡਿਟ ਲੌਗ ਸੁਰੱਖਿਆ-ਨਾਜ਼ੁਕ ਪੂਰਵ-ਸਰਗਰਮ ਕਾਰਵਾਈਆਂ ਨੂੰ ਦਰਜ ਕਰਦੇ ਹਨ, ਜਿਸ ਵਿੱਚ ਮਨਜ਼ੂਰੀ ਦੇਣ ਵਾਲੇ ਦੀ ਪਛਾਣ, ਟਾਈਮਸਟੈਂਪ, ਕਾਰਵਾਈ ਦੇ ਪੈਰਾਮੀਟਰ, ਅਤੇ ਫ਼ੈਸਲੇ ਦੇ ਨਤੀਜੇ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **12.4.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** kill-switch (ਤੁਰੰਤ-ਬੰਦ ਸਵਿੱਚ) ਦੀਆਂ ਸਰਗਰਮੀਆਂ ਅਤੇ ਓਵਰਰਾਈਡ ਕਮਾਂਡਾਂ ਨੂੰ ਲੌਗ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |

---

## C12.5 Training Data & Model Lifecycle Audit
## C12.5 ਸਿਖਲਾਈ ਡਾਟਾ ਅਤੇ ਮਾਡਲ ਜੀਵਨ-ਚੱਕਰ ਆਡਿਟ

The provenance and change history of training data, model artifacts, and knowledge sources must be auditable throughout the AI development lifecycle.

ਸਿਖਲਾਈ ਡਾਟਾ, ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟਾਂ, ਅਤੇ ਗਿਆਨ ਸਰੋਤਾਂ ਦੇ ਮੂਲ-ਸਰੋਤ (provenance) ਅਤੇ ਤਬਦੀਲੀ ਇਤਿਹਾਸ ਦਾ AI ਵਿਕਾਸ ਜੀਵਨ-ਚੱਕਰ ਦੌਰਾਨ ਆਡਿਟਯੋਗ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.5.1** | **Verify that** dataset lineage records each dataset and its components, including all transformations, augmentations, and merges. | 1 |
| **12.5.2** | **Verify that** all labeling activities are recorded in logs. | 1 |
| **12.5.3** | **Verify that** all model changes generate immutable audit records. | 2 |
| **12.5.4** | **Verify that** every ingested document is tagged at write time with source, writer identity, and timestamp. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **12.5.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡਾਟਾਸੈੱਟ ਵੰਸ਼ਾਵਲੀ (lineage) ਹਰ ਡਾਟਾਸੈੱਟ ਅਤੇ ਉਸ ਦੇ ਹਿੱਸਿਆਂ ਨੂੰ ਦਰਜ ਕਰਦੀ ਹੈ, ਜਿਸ ਵਿੱਚ ਸਾਰੇ ਪਰਿਵਰਤਨ, ਔਗਮੈਂਟੇਸ਼ਨ (augmentations), ਅਤੇ ਮਰਜ ਸ਼ਾਮਲ ਹਨ। | 1 |
| **12.5.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਾਰੀਆਂ ਲੇਬਲਿੰਗ ਗਤੀਵਿਧੀਆਂ ਲੌਗਾਂ ਵਿੱਚ ਦਰਜ ਕੀਤੀਆਂ ਜਾਂਦੀਆਂ ਹਨ। | 1 |
| **12.5.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਾਰੀਆਂ ਮਾਡਲ ਤਬਦੀਲੀਆਂ ਅਪਰਿਵਰਤਨਸ਼ੀਲ (immutable) ਆਡਿਟ ਰਿਕਾਰਡ ਪੈਦਾ ਕਰਦੀਆਂ ਹਨ। | 2 |
| **12.5.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਦਾਖ਼ਲ ਕੀਤੇ ਦਸਤਾਵੇਜ਼ ਨੂੰ ਲਿਖਣ ਦੇ ਸਮੇਂ ਸਰੋਤ, ਲਿਖਣ ਵਾਲੇ ਦੀ ਪਛਾਣ, ਅਤੇ ਟਾਈਮਸਟੈਂਪ ਨਾਲ ਟੈਗ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |

---

## References
## ਹਵਾਲੇ

* [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [MITRE ATLAS - Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
* [NIST AI Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
* [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
* [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
* [NIST SP 800-207 Zero Trust Architecture](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf)
