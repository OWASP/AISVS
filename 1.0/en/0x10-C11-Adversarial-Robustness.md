# C11 Adversarial Robustness & Attack Resistance

## Control Objective

Ensure that AI systems remain reliable, privacy-preserving, and abuse-resistant when facing evasion, inference, extraction, or poisoning attacks. These controls cover model alignment testing, adversarial hardening, privacy attack resistance, model theft deterrence, and security adaptation for autonomous agents.

---

## C11.1 Model Alignment & Safety

Guard against harmful or policy-breaking outputs through systematic testing and guardrails.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.1.1** | **Verify that** refusal and safe-completion guardrails are enforced to prevent the model from generating disallowed content categories. | 1 | D |
| **11.1.2** | **Verify that** an alignment test suite (red-team prompts, jailbreak probes, disallowed-content checks) is version-controlled and run on every model update or release. | 1 | D/V |
| **11.1.3** | **Verify that** an automated evaluator measures harmful-content rate and flags regressions beyond a defined threshold. | 2 | D/V |
| **11.1.4** | **Verify that** alignment and safety training procedures (e.g., RLHF, constitutional AI, or equivalent) are documented and reproducible. | 2 | D |
| **11.1.5** | **Verify that** alignment evaluation includes assessments for evaluation awareness, where the model may behave differently when it detects it is being tested versus deployed. | 3 | V |

---

## C11.2 Adversarial-Example Hardening

Increase resilience to manipulated inputs designed to cause misclassification or policy bypass. Adversarial testing and robustness benchmarking are the current best practices.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.2.1** | **Verify that** models serving high-risk functions are evaluated against known adversarial attack techniques relevant to their modality (e.g., perturbation attacks for vision, token-manipulation attacks for text). | 1 | D/V |
| **11.2.2** | **Verify that** adversarial-example detection raises alerts in production pipelines, with blocking or degraded-capability responses for high-risk endpoints or use cases. | 2 | D/V |
| **11.2.3** | **Verify that** adversarial training or equivalent hardening techniques are applied where feasible, with documented configurations and reproducible procedures. | 2 | D |
| **11.2.4** | **Verify that** robustness evaluations use adaptive attacks (attacks specifically designed to defeat the deployed defenses) to confirm no measurable robustness loss across releases. | 3 | V |
| **11.2.5** | **Verify that** formal robustness verification methods (e.g., certified bounds, interval-bound propagation) are applied to safety-critical model components where the model architecture supports them. | 3 | V |

---

## C11.3 Membership-Inference Mitigation

Limit the ability to determine whether a specific record was in the training data. Differential privacy and output calibration are the most effective known defenses.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.3.1** | **Verify that** model outputs are calibrated (e.g., via temperature scaling or output perturbation) to reduce overconfident predictions that facilitate membership-inference attacks. | 2 | D |
| **11.3.2** | **Verify that** training on sensitive datasets employs differentially-private optimization (e.g., DP-SGD) with a documented privacy budget (epsilon). | 2 | D |
| **11.3.3** | **Verify that** membership-inference attack simulations (e.g., shadow-model, likelihood-ratio, or label-only attacks) demonstrate that attack accuracy does not meaningfully exceed random guessing on held-out data. | 3 | V |

---

## C11.4 Model-Inversion Resistance

Prevent reconstruction of private training data or sensitive attributes from model outputs.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.4.1** | **Verify that** sensitive attributes are never directly output; where needed, outputs use generalized categories (e.g., ranges, buckets) or one-way transforms. | 1 | D |
| **11.4.2** | **Verify that** query-rate limits throttle repeated adaptive queries from the same principal to raise the cost of inversion attacks. | 1 | D/V |
| **11.4.3** | **Verify that** models handling sensitive data are trained with privacy-preserving techniques (e.g., differential privacy, gradient clipping) to limit information leakage through outputs. | 2 | D |

---

## C11.5 Model-Extraction Defense

Detect and deter unauthorized model cloning through API abuse. Rate limiting, query-pattern analysis, and watermarking are recommended defenses.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.5.1** | **Verify that** inference endpoints enforce per-principal and global rate limits designed to make large-scale query harvesting impractical. | 1 | D |
| **11.5.2** | **Verify that** extraction-alert events include offending query metadata and are integrated with incident-response playbooks. | 2 | V |
| **11.5.3** | **Verify that** query-pattern analysis (e.g., query diversity, input distribution anomalies) feeds an automated extraction-attempt detector. | 2 | D/V |
| **11.5.4** | **Verify that** model watermarking or fingerprinting techniques are applied so that unauthorized copies can be identified. | 3 | D |
| **11.5.5** | **Verify that** watermark verification keys and trigger sets are protected with access controls equivalent to other critical cryptographic material. | 3 | D |

---

## C11.6 Inference-Time Poisoned-Data Detection

Identify and neutralize backdoored or poisoned inputs at inference time, particularly in systems that consume external data (e.g., RAG pipelines, tool outputs).

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.6.1** | **Verify that** inputs from external or untrusted sources pass through anomaly detection (e.g., statistical outlier detection, consistency scoring) before model inference. | 2 | D |
| **11.6.2** | **Verify that** anomaly-detection thresholds are tuned on representative clean and adversarial validation sets and that the false-positive rate is measured and documented. | 2 | V |
| **11.6.3** | **Verify that** inputs flagged as anomalous trigger gating actions (blocking, capability degradation, or human review) appropriate to the risk level. | 2 | D |
| **11.6.4** | **Verify that** detection methods are periodically stress-tested with current adversarial techniques, including adaptive attacks designed to evade the specific detectors in use. | 3 | V |
| **11.6.5** | **Verify that** detection efficacy metrics are logged and periodically re-evaluated against updated threat intelligence. | 3 | D/V |

---

## C11.7 Security Policy Adaptation

Real-time security policy updates based on threat intelligence and behavioral analysis.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.7.1** | **Verify that** security policies (e.g., content filters, rate-limit thresholds, guardrail configurations) can be updated without full system redeployment, and that policy versions are tracked. | 1 | D/V |
| **11.7.2** | **Verify that** policy updates are authorized, integrity-protected (e.g., cryptographically signed), and validated before application. | 2 | D/V |
| **11.7.3** | **Verify that** policy changes are logged with audit trails including timestamp, author, justification, and rollback procedures. | 2 | D/V |
| **11.7.4** | **Verify that** threat-detection sensitivity can be adjusted based on risk context (e.g., elevated threat level, incident response) with appropriate authorization. | 3 | D/V |

---

## C11.8 Agent Security Self-Assessment

For agentic AI systems, validate that the agent's reasoning and actions are subject to security-focused review mechanisms.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.8.1** | **Verify that** agentic systems include a mechanism to review planned high-risk actions against security policy before execution (e.g., a secondary model, rule-based checker, or structured self-review step). | 2 | D/V |
| **11.8.2** | **Verify that** security review mechanisms are protected against manipulation by adversarial inputs (e.g., the review step cannot be overridden or bypassed through prompt injection). | 2 | D/V |
| **11.8.3** | **Verify that** security review warnings trigger enhanced monitoring or human intervention workflows for the affected session or task. | 3 | D/V |

---

## C11.9 Self-Modification & Autonomous Update Security

Security controls for systems where the AI can modify its own configuration, prompts, tool access, or learned behaviors.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.9.1** | **Verify that** any self-modification capability (e.g., prompt rewriting, tool-list changes, parameter updates) is restricted to explicitly designated areas with enforced boundaries. | 2 | D/V |
| **11.9.2** | **Verify that** proposed self-modifications undergo security impact assessment or policy validation before taking effect. | 2 | D/V |
| **11.9.3** | **Verify that** all self-modifications are logged, reversible, and subject to integrity verification, enabling rollback to a known-good state. | 2 | D/V |
| **11.9.4** | **Verify that** self-modification scope is bounded (e.g., maximum change magnitude, rate limits on updates, prohibited modification targets) to prevent runaway or adversarially induced changes. | 3 | D/V |
| **11.9.5** | **Verify that** when safety violation data (blocked inputs, filtered outputs, flagged hallucinations) is used as training signal for model improvement, the feedback pipeline includes integrity verification, poisoning detection, and human review gates to prevent adversarial manipulation of the improvement mechanism. | 3 | D/V |

## C11.10 Adversarial Bias Exploitation Defense

Protect security-relevant classifiers against adversaries who systematically probe for exploitable bias patterns and weaponize discovered disparities as an evasion vector.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **11.10.1** | **Verify that** inference endpoints for security-relevant classifiers (e.g., abuse detection, fraud scoring) include monitoring that accounts for query patterns indicative of bias probing, such as systematic variation along a single input dimension (e.g., demographic, linguistic, stylistic) while other dimensions remain constant, and alert when such patterns are detected. | 3 | D/V |
| **11.10.2** | **Verify that** adversarial robustness evaluations for security-relevant classifiers are stratified by meaningful input subgroups (e.g., language register, content category), with per-subgroup false-negative rates under adversarial conditions measured and flagged when deviating from aggregate rates beyond a defined threshold. | 2 | D/V |
| **11.10.3** | **Verify that** where bias-based evasion is identified as a material threat, adversarial hardening (e.g., adversarial training with per-subgroup loss constraints, ensemble diversity across training distributions) incorporates explicit subgroup robustness requirements, and that per-subgroup robustness metrics are verified not to regress across model releases. | 3 | D |

---

## References

* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
* [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
* [MITRE ATLAS: Invert ML Model](https://atlas.mitre.org/techniques/AML.T0024.001)
* [MITRE ATLAS: Extract ML Model](https://atlas.mitre.org/techniques/AML.T0024.002)
* [MITRE ATLAS: Backdoor ML Model](https://atlas.mitre.org/techniques/AML.T0018)
* [NIST AI 100-2e2023 Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://csrc.nist.gov/pubs/ai/100/2/e2023/final)
* [MITRE ATLAS: Active Scanning (AML.T0006)](https://atlas.mitre.org/techniques/AML.T0006)
* [MITRE ATLAS: Evade ML Model (AML.T0015)](https://atlas.mitre.org/techniques/AML.T0015)
* [MITRE ATLAS Case Study: Bypass Cylance's AI Malware Detection (AML.CS0003)](https://atlas.mitre.org/studies/AML.CS0003)
