# C11.6: Inference-Time Poisoned-Data Detection

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 5 | **IDs:** 11.6.1--11.6.5

## Purpose

Identify and neutralize backdoored or poisoned inputs at inference time, particularly in systems that consume external data (e.g., RAG pipelines, tool outputs, web scraping). Unlike training-time poisoning (covered in C1), inference-time poisoning targets the data a model processes during production use. This is especially relevant for RAG-based systems where retrieved documents, API responses, or user-supplied context can contain adversarial payloads designed to manipulate model behavior -- including indirect prompt injection, factual manipulation, and behavior modification through crafted context.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.6.1** | **Verify that** inputs from external or untrusted sources pass through anomaly detection (e.g., statistical outlier detection, consistency scoring) before model inference. | 2 | D | Poisoned context injection via compromised RAG corpora, malicious tool outputs, or adversarial web content. Without anomaly detection, the model blindly trusts all retrieved or supplied context. MITRE ATLAS AML.T0018 (Backdoor ML Model) adapted to inference-time context. | Review anomaly detection pipeline for external inputs. Verify detection methods are appropriate for the data type (statistical outlier detection for embeddings, consistency scoring for text, schema validation for structured data). Test with known poisoned inputs and confirm detection. Verify detection is applied before the model processes the input, not after. | Anomaly detection for natural language inputs is inherently difficult -- poisoned text may be semantically valid and statistically indistinguishable from clean text. Indirect prompt injection payloads often look like normal text. Detection effectiveness varies dramatically by input modality. For structured data, anomaly detection is more reliable. |
| **11.6.2** | **Verify that** anomaly-detection thresholds are tuned on representative clean and adversarial validation sets and that the false-positive rate is measured and documented. | 2 | V | Miscalibrated detection that either misses poisoned inputs (thresholds too loose) or blocks legitimate inputs (thresholds too tight). Untuned detectors provide a false sense of security. | Review validation datasets used for threshold tuning -- verify they include representative clean data and realistic adversarial examples. Check documented false-positive rates and confirm they are acceptable for the application. Verify that thresholds are re-evaluated when the input distribution changes (new data sources, updated retrieval indices). | Creating representative adversarial validation sets is difficult and labor-intensive. The adversarial landscape changes rapidly, so validation sets become stale. False-positive rate tolerance depends heavily on the application -- a 1% false-positive rate may be acceptable for a chatbot but not for a medical decision-support system. |
| **11.6.3** | **Verify that** inputs flagged as anomalous trigger gating actions (blocking, capability degradation, or human review) appropriate to the risk level. | 2 | D | Detected anomalies that are logged but not acted upon. Detection without response provides no security value. Risk-appropriate gating ensures that the response matches the potential impact of the poisoned input. | Review gating action configuration for flagged inputs. Verify that high-risk use cases have blocking or human review gates. Verify that lower-risk use cases have appropriate degraded-capability responses (e.g., responding without the suspicious context, flagging output as uncertain). Test end-to-end: inject a flagged input and confirm the gating action executes. | Blocking may not be the right response in all cases -- for RAG systems, excluding the suspicious document and proceeding with remaining context may be more useful than a hard block. Capability degradation must be communicated to the user. Human review gates introduce latency that may not be acceptable for real-time applications. |
| **11.6.4** | **Verify that** detection methods are periodically stress-tested with current adversarial techniques, including adaptive attacks designed to evade the specific detectors in use. | 3 | V | Detector evasion by sophisticated adversaries who study the detection methodology and craft inputs that bypass it. Static detectors become obsolete as attack techniques evolve. Mirrors the adaptive evaluation principle from C11.2.4. | Review stress-testing schedule and methodology. Verify that tests include adaptive attacks (attacks crafted to evade the specific detection method). Check that stress-test results inform detector updates. Confirm testing cadence is appropriate for the threat landscape (at minimum annually, more frequently for high-risk applications). | Adaptive stress-testing for inference-time poisoning detection is less mature than for adversarial-example detection. Requires red-team expertise specific to the input modality and detection method. Automated adaptive testing tools for this category are limited. |
| **11.6.5** | **Verify that** detection efficacy metrics are logged and periodically re-evaluated against updated threat intelligence. | 3 | D/V | Gradual degradation of detection effectiveness as attack techniques evolve and input distributions shift. Without ongoing measurement, detection may become ineffective without anyone noticing. | Review logged detection metrics (detection rate, false-positive rate, flagged input volume trends). Verify periodic review schedule with documented outcomes. Check that threat intelligence feeds (MITRE ATLAS updates, published attack papers, industry reports) are incorporated into detection evaluation. Confirm that metric reviews lead to actionable updates when degradation is detected. | Threat intelligence for inference-time poisoning is less structured than for traditional security threats. Academic publications may lag real-world attacks. Metric interpretation requires domain expertise -- a declining detection rate could indicate fewer attacks or degraded detector performance. |

---

## Related Standards & References

- [MITRE ATLAS AML.T0018 -- Backdoor ML Model](https://atlas.mitre.org/techniques/AML.T0018) -- Backdoor and poisoning attack techniques
- [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/) -- Poisoning risks in LLM systems
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm012025-prompt-injection/) -- Indirect prompt injection via poisoned context is closely related
- [NIST AI 100-2e2023 -- Poisoning Attacks](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Poisoning attack taxonomy
- [Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023)](https://arxiv.org/abs/2302.12173) -- Indirect prompt injection through retrieved content

---

## Open Research Questions

- How can anomaly detection reliably distinguish between legitimate unusual inputs and adversarially crafted poisoned inputs, especially in natural language?
- What is the right architecture for inference-time poisoning defense in RAG systems -- should detection happen at retrieval, at context assembly, or at output?
- Can LLMs themselves serve as effective detectors for poisoned context (meta-reasoning about input trustworthiness), or does this create a circular dependency?
- How should detection thresholds adapt in real-time to changing threat levels without creating instability?
- What is the interaction between inference-time poisoning detection and prompt injection defense (C2, C9) -- are these fundamentally the same problem?

---
