# C7 Model Behavior, Output Control & Safety Assurance

## Control Objective

This control category ensures that model outputs are technically constrained, validated, and monitored so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems. The chapter focuses on AI-specific output handling concerns and intentionally avoids duplicating controls that already exist in OWASP ASVS v5 or in other AISVS chapters.

General application output controls such as output encoding and escaping, parameterized queries, safe deserialization, anti-automation, security event logging, and error handling are addressed by ASVS v5 chapters V1, V2, V14, and V16.

---

## C7.1 Output Format Enforcement

Ensure the model outputs data in a way that helps prevent injection.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.1.1** | **Verify that** the application validates all model outputs against a strict schema (like JSON Schema) and rejects any output that does not match. | 1 |
| **7.1.2** | **Verify that** the system uses "stop sequences" or token limits to strictly cut off generation before it can overflow buffers or executes unintended commands. | 1 |
| **7.1.3** | **Verify that** model outputs crossing a trust boundary into downstream interpreters (e.g., databases, shells, deserializers, template engines, browsers) are treated as untrusted input and processed using the corresponding safe APIs as defined in OWASP ASVS v5 chapters V1.2 and V1.5. | 1 |

---

## C7.2 Hallucination Detection & Mitigation

Detect when the model produces potentially inaccurate or fabricated content and prevent unreliable outputs from reaching users or downstream systems.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.2.1** | **Verify that** the system assesses the reliability of generated answers using a confidence or uncertainty estimation method (e.g., confidence scoring, retrieval-based verification, or model uncertainty estimation). | 1 |
| **7.2.2** | **Verify that** the application automatically blocks answers or switches to a fallback message if the confidence score drops below a defined threshold. | 2 |
| **7.2.3** | **Verify that** hallucination events (low-confidence responses) are logged with input/output metadata for analysis. | 2 |
| **7.2.4** | **Verify that** the system tracks tool and function invocation history within a request chain and flags high-confidence factual assertions that were not preceded by relevant verification tool usage, as a practical hallucination detection signal independent of confidence scoring. | 2 |
| **7.2.5** | **Verify that** for responses classified as high-risk or high-impact by policy, the system performs an additional verification step through an independent mechanism, such as retrieval-based grounding against authoritative sources, deterministic rule-based validation, tool-based fact-checking, or consensus review by a separately provisioned model. | 3 |

---

## C7.3 Output Safety & Privacy Filtering

Technical controls to detect and scrub bad content before it is shown to the user.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.3.1** | **Verify that** automated classifiers scan every response and block content that matches hate, harassment, or sexual violence categories. | 1 |
| **7.3.2** | **Verify that** output filters detect and block responses that disclose system prompt content, including verbatim reproduction and semantically equivalent paraphrases of instructions, role definitions, or policy directives. | 2 |
| **7.3.3** | **Verify that** LLM client applications prevent model-generated output from triggering automatic outbound requests (e.g., auto-rendered images, iframes, or link prefetching) to attacker-controlled endpoints, for example by disabling automatic external resource loading or restricting it to explicitly allowlisted origins as appropriate. | 2 |
| **7.3.4** | **Verify that** generated outputs are analyzed for statistical steganographic covert channels (e.g., biased token-choice patterns or output distribution anomalies) that could encode hidden data across the model's valid output space, and that detections are flagged for review. | 3 |

---

## C7.4 Explainability & Transparency

Ensure the user knows why a decision was made.

| # | Description | Level |
| :-------: | ------------------------------------------------------------------------------------------------------------------------------ | :---: |
| **7.4.1** | **Verify that** explanations provided to the user are sanitized to remove system prompts or backend data. | 1 |
| **7.4.2** | **Verify that** technical evidence of the model's decision, such as model interpretability artifacts (e.g., attention maps, feature attributions), are logged. | 3 |

---

## C7.5 Generative Media Safeguards

Provide cryptographic provenance for synthetic media so that downstream consumers can distinguish AI-generated content from authentic content.

| # | Description | Level |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.5.1** | **Verify that** all generated media includes an invisible watermark or cryptographic signature to prove it was AI-generated. | 3 |

---

## C7.6 Source Attribution & Citation Integrity

Ensure RAG-grounded outputs are traceable to their source documents and that cited claims are verifiably supported by retrieved content.

| # | Description | Level |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.6.1** | **Verify that** responses generated using retrieval-augmented generation (RAG) include attribution to the source documents that grounded the response. | 1 |
| **7.6.2** | **Verify that** RAG attributions are derived from retrieval metadata and are not generated by the model, ensuring provenance cannot be fabricated. | 1 |
| **7.6.3** | **Verify that** each sourced claim in a RAG-grounded response can be traced to a specific retrieved chunk, and that the system detects and flags responses where claims are not supported by any retrieved content before the response is served. | 3 |
| **7.6.4** | **Verify that** RAG responses in which unsupported claims are detected are blocked or redacted before being served to the user. | 3 |

---

## References

* [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
