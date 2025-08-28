# C7 Model Behavior, Output Control & Safety Assurance

## Control Objective

Model outputs must be **structured, reliable, safe, explainable, and continuously monitored in production**. Doing so reduces hallucinations, privacy leaks, harmful content, and runaway actions, while increasing user trust and regulatory compliance.

---

## C7.1 Output Format Enforcement

Strict schemas, constrained decoding, and downstream validation stop malformed or malicious content before it propagates.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.1.1** | **Verify that** response schemas (e.g., JSON Schema) are supplied in the system prompt and every output is automatically validated; non-conforming outputs trigger repair or rejection. | 1 | D/V |
| **7.1.2** | **Verify that** constrained decoding (stop tokens, regex, max-tokens) is enabled to prevent overflow or prompt-injection side-channels. | 1 | D/V |
| **7.1.3** | **Verify that** downstream components treat outputs as untrusted and validate them against schemas or injection-safe de-serializers. | 2 | D/V |
| **7.1.4** | **Verify that** improper-output events are logged, rate-limited, and surfaced to monitoring. | 3 | V |

---

## C7.2 Hallucination Detection & Mitigation

Uncertainty estimation and fallback strategies curb fabricated answers.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.2.1** | **Verify that** token-level log-probabilities, ensemble self-consistency, or fine-tuned hallucination detectors assign a confidence score to each answer. | 1 | D/V |
| **7.2.2** | **Verify that** responses below a configurable confidence threshold trigger fallback workflows (e.g., retrieval-augmented generation, secondary model, or human review). | 1 | D/V |
| **7.2.3** | **Verify that** hallucination incidents are tagged with root-cause metadata and fed to post-mortem and finetuning pipelines. | 2 | D/V |
| **7.2.4** | **Verify that** thresholds and detectors are re-calibrated after major model or knowledge-base updates. | 3 | D/V |
| **7.2.5** | **Verify that** dashboard visualisations track hallucination rates. | 3 | V |

---

## C7.3 Output Safety & Privacy Filtering

Policy filters and red-team coverage protect users and confidential data.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.3.1** | **Verify that** pre and post-generation classifiers block hate, harassment, self-harm, extremist, and sexually explicit content aligned to policy. | 1 | D/V |
| **7.3.2** | **Verify that** PII/PCI detection and automatic redaction run on every response; violations raise a privacy incident. | 1 | D/V |
| **7.3.3** | **Verify that** confidentiality tags (e.g., trade secrets) propagate across modalities to prevent leakage in text, images, or code. | 2 | D |
| **7.3.4** | **Verify that** filter bypass attempts or high-risk classifications require secondary approval or user re-authentication. | 3 | D/V |
| **7.3.5** | **Verify that** filtering thresholds reflect legal jurisdictions and user age/role context. | 3 | D/V |

---

## C7.4 Output & Action Limiting

Rate-limits and approval gates prevent abuse and excessive autonomy.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **7.4.1** | **Verify that** per-user and per-API-key quotas limit requests, tokens, and cost with exponential back-off on 429 errors. | 1 | D |
| **7.4.2** | **Verify that** privileged actions (file writes, code exec, network calls) require policy-based approval or human-in-the-loop. | 1 | D/V |
| **7.4.3** | **Verify that** cross-modal consistency checks ensure images, code, and text generated for the same request cannot be used to smuggle malicious content. | 2 | D/V |
| **7.4.4** | **Verify that** agent delegation depth, recursion limits, and allowed tool lists are explicitly configured. | 2 | D |
| **7.4.5** | **Verify that** violation of limits emits structured security events for SIEM ingestion. | 3 | V |

---

## C7.5 Output Explainability

Transparent signals improve user trust and internal debugging.

| # | Description | Level | Role |
| :-------: | ------------------------------------------------------------------------------------------------------------------------------ | :---: | :--: |
| **7.5.1** | **Verify that** user-facing confidence scores or brief reasoning summaries are exposed when risk assessment deems appropriate. | 2 | D/V |
| **7.5.2** | **Verify that** generated explanations avoid revealing sensitive system prompts or proprietary data. | 2 | D/V |
| **7.5.3** | **Verify that** the system captures token-level log-probabilities or attention maps and stores them for authorized inspection. | 3 | D |
| **7.5.4** | **Verify that** explainability artefacts are version-controlled alongside model releases for auditability. | 3 | V |

---

## C7.6 Monitoring Integration

Real-time observability closes the loop between development and production.

| # | Description | Level | Role |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **7.6.1** | **Verify that** metrics (schema violations, hallucination rate, toxicity, PII leaks, latency, cost) stream to a central monitoring platform. | 1 | D |
| **7.6.2** | **Verify that** alert thresholds are defined for each safety metric, with on-call escalation paths. | 1 | V |
| **7.6.3** | **Verify that** dashboards correlate output anomalies with model/version, feature flag, and upstream data changes. | 2 | V |
| **7.6.4** | **Verify that** monitoring data feeds back into retraining, fine-tuning, or rule updates within a documented MLOps workflow. | 2 | D/V |
| **7.6.5** | **Verify that** monitoring pipelines are penetration-tested and access-controlled to avoid leakage of sensitive logs. | 3 | V |

---

## 7.7 Generative Media Safeguards

Ensure that AI systems do not generate illegal, harmful, or unauthorized media content by enforcing policy constraints, output validation, and traceability.

| # | Description | Level | Role |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: | :--: |
| **7.7.1** | **Verify that** system prompts and user instructions explicitly prohibit the generation of illegal, harmful, or non-consensual deepfake media (e.g., image, video, audio).        | 1     | D/V  |
| **7.7.2** | **Verify that** prompts are filtered for attempts to generate impersonations, sexually explicit deepfakes, or media depicting real individuals without consent.                   | 2     | D/V  |
| **7.7.3** | **Verify that** the system uses perceptual hashing, watermark detection, or fingerprinting to prevent unauthorized reproduction of copyrighted media.                             | 2     | V    |
| **7.7.4** | **Verify that** all generated media is cryptographically signed, watermarked, or embedded with tamper-resistant provenance metadata for downstream traceability.                  | 3     | D/V  |
| **7.7.5** | **Verify that** bypass attempts (e.g., prompt obfuscation, slang, adversarial phrasing) are detected, logged, and rate-limited; repeated abuse is surfaced to monitoring systems. | 3     | V    |

## References

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [ISO/IEC 42001:2023 – AI Management System](https://www.iso.org/obp/ui/en/)
* [OWASP Top-10 for Large Language Model Applications (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [Practical Techniques to Constrain LLM Output](https://mychen76.medium.com/practical-techniques-to-constraint-llm-output-in-json-format-e3e72396c670)
* [Dataiku – Structured Text Generation Guide](https://blog.dataiku.com/your-guide-to-structured-text-generation)
* [VL-Uncertainty: Detecting Hallucinations](https://arxiv.org/abs/2411.11919)
* [HaDeMiF: Hallucination Detection & Mitigation](https://openreview.net/forum?id=VwOYxPScxB)
* [Building Confidence in LLM Outputs](https://www.alkymi.io/data-science-room/building-confidence-in-llm-outputs)
* [Explainable AI & LLMs](https://duncsand.medium.com/explainable-ai-140912d31b3b)
* [Sensitive Information Disclosure in LLMs](https://virtualcyberlabs.com/llm-sensitive-information-disclosure/)
* [OpenAI Rate-Limit & Exponential Back-off](https://hackernoon.com/openais-rate-limit-a-guide-to-exponential-backoff-for-llm-evaluation)
* [Arize AI – LLM Observability Platform](https://arize.com/)
