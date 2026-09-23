<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C11-Adversarial-Robustness.md -->
<!-- Translator: GeeksikhSecurity -->

# C11 Adversarial Robustness
# C11 ਵਿਰੋਧੀ ਮਜ਼ਬੂਤੀ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses keeping AI systems reliable and abuse-resistant when facing evasion, inference, extraction, or poisoning attacks.

ਇਹ ਅਧਿਆਇ evasion (ਪਛਾਣ ਤੋਂ ਬਚ ਨਿਕਲਣਾ), inference, extraction, ਜਾਂ poisoning ਹਮਲਿਆਂ ਦੇ ਸਾਹਮਣੇ AI ਸਿਸਟਮਾਂ ਨੂੰ ਭਰੋਸੇਯੋਗ ਅਤੇ ਦੁਰਵਰਤੋਂ-ਰੋਧਕ ਬਣਾਈ ਰੱਖਣ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ।

---

## C11.1 Model Alignment, Safety, and Robustness Testing and Training
## C11.1 ਮਾਡਲ ਅਲਾਈਨਮੈਂਟ, ਸਲਾਮਤੀ, ਅਤੇ ਮਜ਼ਬੂਤੀ ਟੈਸਟਿੰਗ ਅਤੇ ਸਿਖਲਾਈ

Model resilience to manipulated inputs designed to cause misclassification or policy bypass must be increased, primarily through adversarial testing and robustness benchmarking.

ਗ਼ਲਤ ਵਰਗੀਕਰਨ ਜਾਂ ਨੀਤੀ ਬਾਈਪਾਸ ਕਰਵਾਉਣ ਲਈ ਘੜੇ ਗਏ, ਹੇਰਾਫੇਰੀ ਕੀਤੇ ਇਨਪੁੱਟਾਂ ਪ੍ਰਤੀ ਮਾਡਲ ਦੇ ਲਚਕੀਲੇਪਣ (resilience) ਨੂੰ ਵਧਾਉਣਾ ਲਾਜ਼ਮੀ ਹੈ, ਮੁੱਖ ਤੌਰ 'ਤੇ ਵਿਰੋਧੀ ਟੈਸਟਿੰਗ (adversarial testing) ਅਤੇ ਮਜ਼ਬੂਤੀ ਬੈਂਚਮਾਰਕਿੰਗ (robustness benchmarking) ਰਾਹੀਂ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.1.1** | **Verify that** the model has undergone alignment and safety training or fine-tuning to prevent the model from generating disallowed content categories. | 1 |
| **11.1.2** | **Verify that** a version-controlled alignment test suite is run on every model update or release. | 1 |
| **11.1.3** | **Verify that** models are evaluated against known adversarial attack techniques relevant to their modality. | 1 |
| **11.1.4** | **Verify that** models are hardened against adversarial inputs. | 2 |
| **11.1.5** | **Verify that** an automated evaluator measures harmful-content rate and flags regressions beyond a defined threshold. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਨੇ ਅਲਾਈਨਮੈਂਟ (alignment) ਅਤੇ ਸਲਾਮਤੀ ਸਿਖਲਾਈ ਜਾਂ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਕਰਵਾਈ ਹੈ ਤਾਂ ਜੋ ਮਾਡਲ ਨੂੰ ਮਨਾਹੀ ਵਾਲੀਆਂ ਸਮੱਗਰੀ ਸ਼੍ਰੇਣੀਆਂ ਤਿਆਰ ਕਰਨ ਤੋਂ ਰੋਕਿਆ ਜਾ ਸਕੇ। | 1 |
| **11.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਮਾਡਲ ਅੱਪਡੇਟ ਜਾਂ ਰਿਲੀਜ਼ ਉੱਤੇ ਇੱਕ ਵਰਜ਼ਨ-ਨਿਯੰਤਰਿਤ ਅਲਾਈਨਮੈਂਟ ਟੈਸਟ ਸੂਟ ਚਲਾਇਆ ਜਾਂਦਾ ਹੈ। | 1 |
| **11.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲਾਂ ਦਾ ਉਹਨਾਂ ਦੀ ਮਾਡੈਲਿਟੀ (modality) ਨਾਲ ਸੰਬੰਧਿਤ ਜਾਣੀਆਂ-ਪਛਾਣੀਆਂ ਵਿਰੋਧੀ ਹਮਲਾ ਤਕਨੀਕਾਂ ਦੇ ਵਿਰੁੱਧ ਮੁਲਾਂਕਣ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **11.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲਾਂ ਨੂੰ ਵਿਰੋਧੀ ਇਨਪੁੱਟਾਂ ਵਿਰੁੱਧ ਸਖ਼ਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **11.1.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇੱਕ ਸਵੈਚਾਲਿਤ ਮੁਲਾਂਕਣਕਾਰ (evaluator) ਨੁਕਸਾਨਦੇਹ-ਸਮੱਗਰੀ ਦਰ ਨੂੰ ਮਾਪਦਾ ਹੈ ਅਤੇ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਥ੍ਰੈਸ਼ਹੋਲਡ ਤੋਂ ਪਰੇ ਦੇ ਰਿਗਰੈਸ਼ਨਾਂ (regressions) ਨੂੰ ਨਿਸ਼ਾਨਬੱਧ ਕਰਦਾ ਹੈ। | 3 |

---

## C11.2 Membership-Inference and Model-Inversion Mitigation
## C11.2 Membership-Inference ਅਤੇ Model-Inversion ਨੂੰ ਘਟਾਉਣਾ

The ability to determine whether a specific record was in the training data must be limited, and reconstruction of private training data or sensitive attributes from model outputs prevented.

ਇਹ ਪਤਾ ਲਗਾਉਣ ਦੀ ਸਮਰੱਥਾ ਕਿ ਕੋਈ ਖ਼ਾਸ ਰਿਕਾਰਡ ਸਿਖਲਾਈ ਡਾਟਾ ਵਿੱਚ ਸੀ ਜਾਂ ਨਹੀਂ, ਸੀਮਤ ਕੀਤੀ ਜਾਣੀ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਮਾਡਲ ਆਊਟਪੁੱਟ ਤੋਂ ਨਿੱਜੀ ਸਿਖਲਾਈ ਡਾਟਾ ਜਾਂ ਸੰਵੇਦਨਸ਼ੀਲ ਗੁਣਾਂ ਦੇ ਪੁਨਰ-ਨਿਰਮਾਣ ਨੂੰ ਰੋਕਿਆ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.2.1** | **Verify that** model-inferred sensitive attributes are not directly returned in outputs. | 1 |
| **11.2.2** | **Verify that** inference endpoints enforce per-principal and global rate limits sized to the extraction threat model, and not solely as a generic API throttle. | 1 |
| **11.2.3** | **Verify that** model outputs are calibrated to reduce overconfident predictions. | 2 |
| **11.2.4** | **Verify that** training on sensitive datasets employs differentially-private optimization. | 2 |
| **11.2.5** | **Verify that** membership-inference attack simulations demonstrate that attack accuracy does not exceed random guessing on evaluated data. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਦੁਆਰਾ ਅਨੁਮਾਨਿਤ ਸੰਵੇਦਨਸ਼ੀਲ ਗੁਣ ਸਿੱਧੇ ਤੌਰ 'ਤੇ ਆਊਟਪੁੱਟ ਵਿੱਚ ਵਾਪਸ ਨਹੀਂ ਕੀਤੇ ਜਾਂਦੇ। | 1 |
| **11.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇਨਫ਼ਰੈਂਸ ਐਂਡਪੁਆਇੰਟ ਪ੍ਰਤੀ-ਪ੍ਰਿੰਸੀਪਲ (per-principal) ਅਤੇ ਸਮੁੱਚੀਆਂ ਦਰ ਸੀਮਾਵਾਂ ਲਾਗੂ ਕਰਦੇ ਹਨ ਜੋ extraction ਖ਼ਤਰਾ ਮਾਡਲ ਦੇ ਅਨੁਸਾਰ ਮਿਥੀਆਂ ਗਈਆਂ ਹੋਣ, ਨਾ ਕਿ ਸਿਰਫ਼ ਇੱਕ ਆਮ API ਥ੍ਰੌਟਲ (throttle) ਵਜੋਂ। | 1 |
| **11.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹੱਦੋਂ ਵੱਧ ਭਰੋਸੇ ਵਾਲੇ ਪੂਰਵ-ਅਨੁਮਾਨਾਂ (overconfident predictions) ਨੂੰ ਘਟਾਉਣ ਲਈ ਮਾਡਲ ਆਊਟਪੁੱਟ ਨੂੰ ਕੈਲੀਬ੍ਰੇਟ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **11.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸੰਵੇਦਨਸ਼ੀਲ ਡਾਟਾਸੈੱਟਾਂ ਉੱਤੇ ਸਿਖਲਾਈ differential privacy-ਆਧਾਰਿਤ ਅਨੁਕੂਲਨ (differentially-private optimization) ਵਰਤਦੀ ਹੈ। | 2 |
| **11.2.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** membership-inference ਹਮਲੇ ਦੇ ਸਿਮੂਲੇਸ਼ਨ ਇਹ ਦਰਸਾਉਂਦੇ ਹਨ ਕਿ ਮੁਲਾਂਕਣ ਕੀਤੇ ਡਾਟੇ ਉੱਤੇ ਹਮਲੇ ਦੀ ਸਟੀਕਤਾ (accuracy) ਬੇਤਰਤੀਬ ਅੰਦਾਜ਼ੇ ਤੋਂ ਵੱਧ ਨਹੀਂ ਜਾਂਦੀ। | 3 |

---

## C11.3 Model-Extraction Defense
## C11.3 Model-Extraction ਵਿਰੁੱਧ ਬਚਾਅ

Unauthorized model cloning through API abuse must be detected and deterred using rate limiting, query-pattern analysis, and watermarking.

API ਦੀ ਦੁਰਵਰਤੋਂ ਰਾਹੀਂ ਅਣਅਧਿਕਾਰਤ ਮਾਡਲ ਕਲੋਨਿੰਗ (cloning) ਦਾ ਦਰ ਸੀਮਾ, ਕਿਊਰੀ-ਪੈਟਰਨ ਵਿਸ਼ਲੇਸ਼ਣ, ਅਤੇ ਵਾਟਰਮਾਰਕਿੰਗ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਪਤਾ ਲਗਾਇਆ ਜਾਣਾ ਅਤੇ ਉਸ ਨੂੰ ਰੋਕਿਆ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.3.1** | **Verify that** query-pattern analysis feeds an extraction-attempt detector. | 1 |
| **11.3.2** | **Verify that** raw model outputs are not directly exposed beyond the application backend, and that externally visible responses are calibrated to the extraction risk level. | 2 |
| **11.3.3** | **Verify that** model watermarking or fingerprinting techniques are applied so that unauthorized copies can be identified. | 3 |
| **11.3.4** | **Verify that** detection of suspected extraction triggers response measures. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕਿਊਰੀ-ਪੈਟਰਨ ਵਿਸ਼ਲੇਸ਼ਣ ਇੱਕ extraction-ਕੋਸ਼ਿਸ਼ ਡਿਟੈਕਟਰ (detector) ਨੂੰ ਇਨਪੁੱਟ ਦਿੰਦਾ ਹੈ। | 1 |
| **11.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕੱਚੇ ਮਾਡਲ ਆਊਟਪੁੱਟ ਐਪਲੀਕੇਸ਼ਨ ਬੈਕਐਂਡ ਤੋਂ ਪਰੇ ਸਿੱਧੇ ਤੌਰ 'ਤੇ ਜ਼ਾਹਰ ਨਹੀਂ ਕੀਤੇ ਜਾਂਦੇ, ਅਤੇ ਇਹ ਕਿ ਬਾਹਰੋਂ ਦਿਖਾਈ ਦੇਣ ਵਾਲੇ ਜਵਾਬ extraction ਜੋਖਮ ਪੱਧਰ ਦੇ ਅਨੁਸਾਰ ਕੈਲੀਬ੍ਰੇਟ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 2 |
| **11.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਵਾਟਰਮਾਰਕਿੰਗ ਜਾਂ ਫ਼ਿੰਗਰਪ੍ਰਿੰਟਿੰਗ ਤਕਨੀਕਾਂ ਲਾਗੂ ਕੀਤੀਆਂ ਜਾਂਦੀਆਂ ਹਨ ਤਾਂ ਜੋ ਅਣਅਧਿਕਾਰਤ ਨਕਲਾਂ ਦੀ ਪਛਾਣ ਕੀਤੀ ਜਾ ਸਕੇ। | 3 |
| **11.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸ਼ੱਕੀ extraction ਦੀ ਪਛਾਣ ਜਵਾਬੀ ਉਪਾਵਾਂ ਨੂੰ ਸ਼ੁਰੂ ਕਰਦੀ ਹੈ। | 3 |

---

## C11.4 Model Runtime Anomaly Detection
## C11.4 ਮਾਡਲ ਰਨਟਾਈਮ ਅਸਧਾਰਨਤਾ ਪਛਾਣ

Manipulated, backdoored, or adversarial data entering the model context at inference time via external sources must be identified and neutralized.

ਇਨਫ਼ਰੈਂਸ ਵੇਲੇ ਬਾਹਰੀ ਸਰੋਤਾਂ ਰਾਹੀਂ ਮਾਡਲ ਸੰਦਰਭ ਵਿੱਚ ਦਾਖ਼ਲ ਹੋਣ ਵਾਲੇ ਹੇਰਾਫੇਰੀ ਕੀਤੇ, ਬੈਕਡੋਰ ਵਾਲੇ, ਜਾਂ ਵਿਰੋਧੀ ਡਾਟੇ ਦੀ ਪਛਾਣ ਕਰਨਾ ਅਤੇ ਉਸ ਨੂੰ ਬੇਅਸਰ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.4.1** | **Verify that** inputs from external or untrusted sources pass through anomaly detection before model inference. | 2 |
| **11.4.2** | **Verify that** inputs flagged as anomalous trigger gating actions. | 2 |
| **11.4.3** | **Verify that** the safety violation feedback pipeline includes poisoning detection and human review gates to prevent adversarial manipulation of the improvement mechanism. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.4.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਬਾਹਰੀ ਜਾਂ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਸਰੋਤਾਂ ਤੋਂ ਆਏ ਇਨਪੁੱਟ ਮਾਡਲ ਇਨਫ਼ਰੈਂਸ ਤੋਂ ਪਹਿਲਾਂ ਅਸਧਾਰਨਤਾ ਪਛਾਣ (anomaly detection) ਵਿੱਚੋਂ ਲੰਘਦੇ ਹਨ। | 2 |
| **11.4.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਅਸਧਾਰਨ ਵਜੋਂ ਨਿਸ਼ਾਨਬੱਧ ਕੀਤੇ ਇਨਪੁੱਟ ਗੇਟਿੰਗ ਕਾਰਵਾਈਆਂ (gating actions) ਸ਼ੁਰੂ ਕਰਦੇ ਹਨ। | 2 |
| **11.4.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਲਾਮਤੀ ਉਲੰਘਣਾ ਫ਼ੀਡਬੈਕ ਪਾਈਪਲਾਈਨ ਵਿੱਚ poisoning ਪਛਾਣ ਅਤੇ ਮਨੁੱਖੀ ਸਮੀਖਿਆ ਗੇਟ ਸ਼ਾਮਲ ਹਨ ਤਾਂ ਜੋ ਸੁਧਾਰ ਵਿਧੀ ਨਾਲ ਵਿਰੋਧੀ ਹੇਰਾਫੇਰੀ ਨੂੰ ਰੋਕਿਆ ਜਾ ਸਕੇ। | 3 |

---

## References
## ਹਵਾਲੇ

* [NIST AI 100-2e2023 Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://csrc.nist.gov/pubs/ai/100/2/e2023/final)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [MITRE ATLAS: Evade ML Model (AML.T0015)](https://atlas.mitre.org/techniques/AML.T0015)
* [MITRE ATLAS: Backdoor ML Model](https://atlas.mitre.org/techniques/AML.T0018)
* [MITRE ATLAS: Extract ML Model](https://atlas.mitre.org/techniques/AML.T0024.002)
