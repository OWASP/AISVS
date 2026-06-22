# C11 Adversarial Robustness

## Control Objective

Ensure that AI systems remain reliable, privacy-preserving, and abuse-resistant when facing evasion, inference, extraction, or poisoning attacks. These controls cover model alignment testing, adversarial hardening, privacy attack resistance, model theft deterrence, and security adaptation for autonomous agents.

---

## C11.1 Model Alignment, Safety and Robustness Testing and Training

Increase resilience to manipulated inputs designed to cause misclassification or policy bypass. Adversarial testing and robustness benchmarking are the current best practices.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.1.1** | **Verify that** the model has been alignment and safety trained or fine-tuned to prevent the model from generating disallowed content categories. | 1 |
| **11.1.2** | **Verify that** a version-controlled alignment test suite is run on every model update or release. | 1 |
| **11.1.3** | **Verify that** models are evaluated against known adversarial attack techniques relevant to their modality. | 1 |
| **11.1.4** | **Verify that** models are hardened against adversarial inputs. | 2 |
| **11.1.5** | **Verify that** an automated evaluator measures harmful-content rate and flags regressions beyond a defined threshold. | 3 |

---

## C11.2 Membership-Inference and Model-Inversion Mitigation

Limit the ability to determine whether a specific record was in the training data, and prevent reconstruction of private training data or sensitive attributes from model outputs. Differential privacy and output calibration are the most effective known defenses.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.2.1** | **Verify that** model-inferred sensitive attributes are not directly returned in outputs. | 1 |
| **11.2.2** | **Verify that** inference endpoints enforce per-principal and global rate limits sized to the extraction threat model, and not solely as a generic API throttle. | 1 |
| **11.2.3** | **Verify that** model outputs are calibrated to reduce overconfident predictions. | 2 |
| **11.2.4** | **Verify that** training on sensitive datasets employs differentially-private optimization. | 2 |
| **11.2.5** | **Verify that** membership-inference attack simulations demonstrate that attack accuracy does not exceed random guessing on data. | 3 |

---

## C11.3 Model-Extraction Defense

Detect and deter unauthorized model cloning through API abuse. Rate limiting, query-pattern analysis, and watermarking are recommended defenses.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.3.1** | **Verify that** query-pattern analysis feeds an extraction-attempt detector. | 1 |
| **11.3.2** | **Verify that** raw model outputs are not directly exposed beyond the application backend, and that externally visible responses are calibrated to the extraction risk level. | 2 |
| **11.3.3** | **Verify that** model watermarking or fingerprinting techniques are applied so that unauthorized copies can be identified. | 3 |
| **11.3.4** | **Verify that** detection of suspected extraction triggers response measures. | 3 |

---

## C11.4 Model Runtime Anomaly Detection

Identify and neutralize manipulated, backdoored, or adversarial data entering the model context at inference time via external sources.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **11.4.1** | **Verify that** inputs from external or untrusted sources pass through anomaly detection before model inference. | 2 |
| **11.4.2** | **Verify that** inputs flagged as anomalous trigger gating actions. | 2 |
| **11.4.3** | **Verify that** the safety violation feedback pipeline includes poisoning detection, and human review gates to prevent adversarial manipulation of the improvement mechanism. | 3 |

---

## References

* [NIST AI 100-2e2023 Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://csrc.nist.gov/pubs/ai/100/2/e2023/final)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [MITRE ATLAS: Evade ML Model (AML.T0015)](https://atlas.mitre.org/techniques/AML.T0015)
* [MITRE ATLAS: Backdoor ML Model](https://atlas.mitre.org/techniques/AML.T0018)
* [MITRE ATLAS: Extract ML Model](https://atlas.mitre.org/techniques/AML.T0024.002)
