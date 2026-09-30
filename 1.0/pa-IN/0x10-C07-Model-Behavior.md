<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C07-Model-Behavior.md -->
<!-- Translator: GeeksikhSecurity -->
<!-- Revision 2026-09-30: locked styleguide applied (control-head verb; breach-term forms). See pa-IN/REVISIONS.md. Status unchanged: draft v0.1 pending Sangat/academic review. -->

# C7 Model Behavior, Output Control & Safety Assurance
# C੭ ਮਾਡਲ ਵਿਵਹਾਰ, ਆਊਟਪੁੱਟ ਨਿਯੰਤਰਣ ਅਤੇ ਸਲਾਮਤੀ ਭਰੋਸਾ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses constraining, validating, and monitoring model outputs so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems.

ਇਹ ਅਧਿਆਇ ਮਾਡਲ ਆਊਟਪੁੱਟ ਨੂੰ ਸੀਮਿਤ ਕਰਨ, ਪ੍ਰਮਾਣਿਤ ਕਰਨ ਅਤੇ ਉਸ ਦੀ ਨਿਗਰਾਨੀ ਕਰਨ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ ਤਾਂ ਜੋ ਗ਼ੈਰ-ਸਲਾਮਤ (unsafe), ਵਿਗੜੇ ਹੋਏ, ਜਾਂ ਉੱਚ-ਜੋਖਮ ਵਾਲੇ ਜਵਾਬ ਉਪਭੋਗਤਾਵਾਂ ਜਾਂ ਡਾਊਨਸਟ੍ਰੀਮ ਸਿਸਟਮਾਂ ਤੱਕ ਨਾ ਪਹੁੰਚ ਸਕਣ।

---

## C7.1 Output Format Enforcement
## C੭.੧ ਆਊਟਪੁੱਟ ਫ਼ਾਰਮੈਟ ਲਾਗੂਕਰਨ

Model outputs must be structured and validated to reduce downstream injection risk.

ਡਾਊਨਸਟ੍ਰੀਮ ਇੰਜੈਕਸ਼ਨ ਜੋਖਮ ਨੂੰ ਘਟਾਉਣ ਲਈ ਮਾਡਲ ਆਊਟਪੁੱਟ ਦਾ ਢਾਂਚਾਗਤ ਅਤੇ ਪ੍ਰਮਾਣਿਤ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.1.1** | **Verify that** the application validates all model outputs against a defined schema and rejects any output that does not match. | 1 |
| **7.1.2** | **Verify that** model-generated output is bounded by length limits and termination controls. | 1 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **੭.੧.੧** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਐਪਲੀਕੇਸ਼ਨ ਸਾਰੇ ਮਾਡਲ ਆਊਟਪੁੱਟ ਨੂੰ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਸਕੀਮਾ ਦੇ ਵਿਰੁੱਧ ਪ੍ਰਮਾਣਿਤ ਕਰਦੀ ਹੈ ਅਤੇ ਕਿਸੇ ਵੀ ਅਜਿਹੇ ਆਊਟਪੁੱਟ ਨੂੰ ਰੱਦ ਕਰਦੀ ਹੈ ਜੋ ਮੇਲ ਨਹੀਂ ਖਾਂਦਾ। | ੧ |
| **੭.੧.੨** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਕੀਤਾ ਆਊਟਪੁੱਟ ਲੰਬਾਈ ਸੀਮਾਵਾਂ ਅਤੇ ਸਮਾਪਤੀ ਨਿਯੰਤਰਣਾਂ ਦੁਆਰਾ ਸੀਮਿਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | ੧ |

---

## C7.2 Hallucination Detection & Mitigation
## C੭.੨ Hallucination ਦੀ ਪਛਾਣ ਅਤੇ ਘਟਾਉਣਾ

Potentially inaccurate or fabricated content must be detected so unreliable outputs do not reach users or downstream systems.

ਸੰਭਾਵੀ ਤੌਰ 'ਤੇ ਗ਼ਲਤ ਜਾਂ ਮਨਘੜਤ ਸਮੱਗਰੀ (hallucination) ਦੀ ਪਛਾਣ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ ਤਾਂ ਜੋ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਆਊਟਪੁੱਟ ਉਪਭੋਗਤਾਵਾਂ ਜਾਂ ਡਾਊਨਸਟ੍ਰੀਮ ਸਿਸਟਮਾਂ ਤੱਕ ਨਾ ਪਹੁੰਚੇ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.2.1** | **Verify that** the system assesses the reliability of generated answers using a confidence estimation method. | 2 |
| **7.2.2** | **Verify that** the application automatically blocks answers or switches to a fallback message if the confidence score drops below a defined threshold. | 2 |
| **7.2.3** | **Verify that** for responses classified as high-risk by policy, the system performs an additional verification step. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **੭.੨.੧** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਸਿਸਟਮ ਇੱਕ ਭਰੋਸਾ ਅਨੁਮਾਨ ਵਿਧੀ (confidence estimation) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਤਿਆਰ ਕੀਤੇ ਜਵਾਬਾਂ ਦੀ ਭਰੋਸੇਯੋਗਤਾ ਦਾ ਮੁਲਾਂਕਣ ਕਰਦਾ ਹੈ। | ੨ |
| **੭.੨.੨** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਜੇ ਭਰੋਸਾ ਸਕੋਰ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਥ੍ਰੈਸ਼ਹੋਲਡ ਤੋਂ ਹੇਠਾਂ ਡਿੱਗ ਜਾਂਦਾ ਹੈ ਤਾਂ ਐਪਲੀਕੇਸ਼ਨ ਆਪਣੇ ਆਪ ਜਵਾਬਾਂ ਨੂੰ ਰੋਕ ਦਿੰਦੀ ਹੈ ਜਾਂ ਇੱਕ ਫ਼ਾਲਬੈਕ ਸੁਨੇਹੇ 'ਤੇ ਬਦਲ ਜਾਂਦੀ ਹੈ। | ੨ |
| **੭.੨.੩** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਨੀਤੀ ਦੁਆਰਾ ਉੱਚ-ਜੋਖਮ ਵਜੋਂ ਵਰਗੀਕ੍ਰਿਤ ਕੀਤੇ ਜਵਾਬਾਂ ਲਈ, ਸਿਸਟਮ ਇੱਕ ਵਾਧੂ ਤਸਦੀਕ ਪੜਾਅ ਕਰਦਾ ਹੈ। | ੩ |

---

## C7.3 Output Safety
## C੭.੩ ਆਊਟਪੁੱਟ ਸਲਾਮਤੀ

Technical controls must detect and remove unsafe content before it is shown to the user.

ਤਕਨੀਕੀ ਨਿਯੰਤਰਣਾਂ ਲਈ ਉਪਭੋਗਤਾ ਨੂੰ ਦਿਖਾਏ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਗ਼ੈਰ-ਸਲਾਮਤ ਸਮੱਗਰੀ ਦੀ ਪਛਾਣ ਕਰਨਾ ਅਤੇ ਉਸ ਨੂੰ ਹਟਾਉਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.3.1** | **Verify that** automated classifiers scan every response and block content that matches defined harmful content categories. | 1 |
| **7.3.2** | **Verify that** output filters detect and block responses that disclose system prompt content or backend data. | 2 |
| **7.3.3** | **Verify that** model-generated output is prevented from triggering outbound requests. | 2 |
| **7.3.4** | **Verify that** model outputs are checked for hidden, encoded, or misleading content created through homoglyphs, formatting, metadata, or structured fields. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **੭.੩.੧** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਸਵੈਚਾਲਿਤ ਵਰਗੀਕਾਰ (classifiers) ਹਰ ਜਵਾਬ ਨੂੰ ਸਕੈਨ ਕਰਦੇ ਹਨ ਅਤੇ ਉਸ ਸਮੱਗਰੀ ਨੂੰ ਰੋਕਦੇ ਹਨ ਜੋ ਪਰਿਭਾਸ਼ਿਤ ਨੁਕਸਾਨਦੇਹ ਸਮੱਗਰੀ ਸ਼੍ਰੇਣੀਆਂ ਨਾਲ ਮੇਲ ਖਾਂਦੀ ਹੈ। | ੧ |
| **੭.੩.੨** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਆਊਟਪੁੱਟ ਫ਼ਿਲਟਰ ਉਹਨਾਂ ਜਵਾਬਾਂ ਦੀ ਪਛਾਣ ਕਰਦੇ ਹਨ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਰੋਕਦੇ ਹਨ ਜੋ system prompt ਦੀ ਸਮੱਗਰੀ ਜਾਂ ਬੈਕਐਂਡ ਡਾਟਾ ਦਾ ਖੁਲਾਸਾ ਕਰਦੇ ਹਨ। | ੨ |
| **੭.੩.੩** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਕੀਤੇ ਆਊਟਪੁੱਟ ਨੂੰ ਬਾਹਰ ਜਾਣ ਵਾਲੀਆਂ ਬੇਨਤੀਆਂ ਸ਼ੁਰੂ ਕਰਨ ਤੋਂ ਰੋਕਿਆ ਜਾਂਦਾ ਹੈ। | ੨ |
| **੭.੩.੪** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਮਾਡਲ ਆਊਟਪੁੱਟ ਦੀ ਲੁਕੀ ਹੋਈ, ਏਨਕੋਡ ਕੀਤੀ, ਜਾਂ ਗੁਮਰਾਹਕੁਨ ਸਮੱਗਰੀ ਲਈ ਜਾਂਚ ਕੀਤੀ ਜਾਂਦੀ ਹੈ ਜੋ homoglyph (ਸਮਰੂਪ ਅੱਖਰ), ਫ਼ਾਰਮੈਟਿੰਗ, ਮੈਟਾਡਾਟਾ, ਜਾਂ ਢਾਂਚਾਗਤ ਖੇਤਰਾਂ ਰਾਹੀਂ ਬਣਾਈ ਗਈ ਹੋਵੇ। | ੩ |

---

## C7.4 Source Attribution & Citation Integrity
## C੭.੪ ਸਰੋਤ-ਨਿਰਧਾਰਨ ਅਤੇ ਹਵਾਲਾ ਅਖੰਡਤਾ

RAG-grounded outputs must be traceable to their source documents, with cited claims verifiably supported by retrieved content.

RAG-ਆਧਾਰਿਤ ਆਊਟਪੁੱਟ ਦਾ ਆਪਣੇ ਸਰੋਤ ਦਸਤਾਵੇਜ਼ਾਂ ਤੱਕ ਟਰੇਸ ਕਰਨਯੋਗ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਹਵਾਲਾ ਦਿੱਤੇ ਗਏ ਦਾਅਵੇ ਪ੍ਰਾਪਤ ਕੀਤੀ ਸਮੱਗਰੀ ਦੁਆਰਾ ਤਸਦੀਕਯੋਗ ਢੰਗ ਨਾਲ ਸਮਰਥਿਤ ਹੋਣੇ ਲਾਜ਼ਮੀ ਹਨ।

| # | Description | Level |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.4.1** | **Verify that** responses generated using retrieval-augmented generation (RAG) include attribution to the source documents. | 1 |
| **7.4.2** | **Verify that** RAG attributions are derived from retrieval metadata and are not generated by the model, so provenance cannot be fabricated. | 1 |
| **7.4.3** | **Verify that** claims in a RAG response can be traced to the retrieved chunk. | 2 |
| **7.4.4** | **Verify that** generated media is watermarked to prove it was AI-generated. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **੭.੪.੧** | **ਜਾਂਚ ਕਰੋ ਕਿ** retrieval-augmented generation (RAG) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਤਿਆਰ ਕੀਤੇ ਜਵਾਬਾਂ ਵਿੱਚ ਸਰੋਤ ਦਸਤਾਵੇਜ਼ਾਂ ਦਾ ਸਰੋਤ-ਨਿਰਧਾਰਨ (attribution) ਸ਼ਾਮਲ ਹੁੰਦਾ ਹੈ। | ੧ |
| **੭.੪.੨** | **ਜਾਂਚ ਕਰੋ ਕਿ** RAG ਸਰੋਤ-ਨਿਰਧਾਰਨ ਪ੍ਰਾਪਤੀ ਮੈਟਾਡਾਟਾ ਤੋਂ ਲਏ ਜਾਂਦੇ ਹਨ ਅਤੇ ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਨਹੀਂ ਕੀਤੇ ਜਾਂਦੇ, ਤਾਂ ਜੋ ਮੂਲ-ਸਰੋਤ (provenance) ਘੜਿਆ ਨਾ ਜਾ ਸਕੇ। | ੧ |
| **੭.੪.੩** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਇੱਕ RAG ਜਵਾਬ ਵਿਚਲੇ ਦਾਅਵਿਆਂ ਨੂੰ ਪ੍ਰਾਪਤ ਕੀਤੇ ਚੰਕ (chunk) ਤੱਕ ਟਰੇਸ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ। | ੨ |
| **੭.੪.੪** | **ਜਾਂਚ ਕਰੋ ਕਿ** ਤਿਆਰ ਕੀਤੇ ਮੀਡੀਆ ਨੂੰ ਵਾਟਰਮਾਰਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਤਾਂ ਜੋ ਇਹ ਸਾਬਤ ਹੋ ਸਕੇ ਕਿ ਇਹ AI ਦੁਆਰਾ ਤਿਆਰ ਕੀਤਾ ਗਿਆ ਸੀ। | ੩ |

---

## References
## ਹਵਾਲੇ

* [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
* [OWASP LLM09:2025 Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/)
* [NIST AI 600-1: Generative AI Profile (AI RMF Companion)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
* [MITRE ATLAS](https://atlas.mitre.org/)
