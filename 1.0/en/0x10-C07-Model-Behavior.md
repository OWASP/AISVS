# C7 Model Behavior, Output Control & Safety Assurance

## Control Objective

This control category ensures that model outputs are technically constrained, validated, and monitored so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems. The chapter focuses on AI-specific output handling concerns: format and schema enforcement for model output, confidence and uncertainty handling, output safety filtering, and explainability artifacts.

---

## C7.1 Output Format Enforcement

Ensure the model outputs data in a way that helps prevent injection.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.1.1** | **Verify that** the application validates all model outputs against a strict schema (like JSON Schema) and rejects any output that does not match. | 1 |
| **7.1.2** | **Verify that** the system uses "stop sequences" or token limits to cut off generation before it can overflow buffers or execute unintended commands. | 1 |
| **7.1.3** | **Verify that** model outputs crossing a trust boundary into downstream interpreters (e.g., databases, shells, deserializers, template engines, browsers) are treated as untrusted input and processed using the corresponding safe APIs as defined in respective OWASP ASVS guidance. | 1 |

---

## C7.2 Hallucination Detection & Mitigation

Detect when the model produces potentially inaccurate or fabricated content and prevent unreliable outputs from reaching users or downstream systems.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.2.1** | **Verify that** the system assesses and logs the reliability of generated answers using a confidence or uncertainty estimation method (e.g., confidence scoring, retrieval-based verification, or model uncertainty estimation). | 2 |
| **7.2.2** | **Verify that** the application automatically blocks answers or switches to a fallback message if the confidence score drops below a defined threshold. | 2 |
| **7.2.3** | **Verify that** for responses classified as high-risk or high-impact by policy, the system performs an additional verification step through an independent mechanism, such as retrieval-based grounding against authoritative sources, deterministic rule-based validation, tool-based fact-checking, or consensus review by a separately provisioned model. | 3 |

---

## C7.3 Output Safety & Privacy Filtering

Technical controls to detect and scrub bad content before it is shown to the user.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.3.1** | **Verify that** automated classifiers scan every response and block content that matches defined harmful content categories. | 1 |
| **7.3.2** | **Verify that** output filters detect and block responses that disclose system prompt content. | 2 |
| **7.3.3** | **Verify that** LLM client applications prevent model-generated output from triggering automatic arbitrary outbound requests (e.g., auto-rendered images, iframes, or link prefetching), for example by turning off automatic external resource loading or by restricting it to an allowlisted set of origins. | 2 |
| **7.3.5** | **Verify that** model-generated outputs are scanned for encoding and representation smuggling artifacts (e.g., invisible Unicode or control characters, homoglyph substitutions, mixed-direction text) before being returned to callers or passed to downstream systems, and that detections trigger rejection or sanitization. | 3 |

---

## C7.4 Explainability & Transparency

Ensure user and other downstream consumers can interpret decisions by AI and recognize AI-generated media.

| # | Description | Level |
| :-------: | ------------------------------------------------------------------------------------------------------------------------------ | :---: |
| **7.4.1** | **Verify that** explanations shown to the user are sanitized to remove system prompts or backend data. | 1 |
| **7.4.2** | **Verify that** technical evidence of the model's decision, such as model interpretability artifacts (e.g., attention maps, feature attributions), is logged. | 3 |
| **7.4.1** | **Verify that** all generated media includes an invisible watermark or cryptographic signature to prove it was AI-generated. | 3 |

---

## C7.5 Source Attribution & Citation Integrity

Ensure RAG-grounded outputs are traceable to their source documents and that cited claims are verifiably supported by retrieved content.

| # | Description | Level |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.5.1** | **Verify that** responses generated using retrieval-augmented generation (RAG) include attribution to the source documents that grounded the response. | 1 |
| **7.5.2** | **Verify that** RAG attributions are derived from retrieval metadata and are not generated by the model, so provenance cannot be fabricated. | 1 |
| **7.5.3** | **Verify that** each sourced claim in a RAG-grounded response can be traced to a specific retrieved chunk. | 2 |
| **7.5.4** | **Verify that** the system detects and flags responses where claims are not supported by any retrieved content, and unsupported claims are blocked or redacted before being served to the user. | 2 |

---

## References

* [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
