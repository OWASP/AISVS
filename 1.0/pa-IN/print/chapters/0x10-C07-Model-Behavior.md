<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C07-Model-Behavior.md -->
<!-- Translator: GeeksikhSecurity -->

# C7 Model Behavior, Output Control & Safety Assurance
# C7 ਮਾਡਲ ਵਿਵਹਾਰ[^0x10-C07-behavior], ਆਊਟਪੁੱਟ[^0x10-C07-output] ਨਿਯੰਤਰਣ ਅਤੇ ਸਲਾਮਤੀ ਭਰੋਸਾ[^0x10-C07-assurance]

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses constraining, validating, and monitoring model outputs so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems.

ਇਹ ਅਧਿਆਇ ਮਾਡਲ ਆਊਟਪੁੱਟ ਨੂੰ ਸੀਮਿਤ ਕਰਨ, ਪ੍ਰਮਾਣਿਤ ਕਰਨ ਅਤੇ ਉਸ ਦੀ ਨਿਗਰਾਨੀ ਕਰਨ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ ਤਾਂ ਜੋ ਗ਼ੈਰ-ਸਲਾਮਤ[^0x10-C07-unsafe] (unsafe), ਵਿਗੜੇ[^0x10-C07-malformed] ਹੋਏ, ਜਾਂ ਉੱਚ-ਜੋਖਮ ਵਾਲੇ ਜਵਾਬ ਉਪਭੋਗਤਾਵਾਂ ਜਾਂ ਡਾਊਨਸਟ੍ਰੀਮ[^0x10-C07-downstream] ਸਿਸਟਮਾਂ ਤੱਕ ਨਾ ਪਹੁੰਚ ਸਕਣ।

---

## C7.1 Output Format Enforcement
## C7.1 ਆਊਟਪੁੱਟ ਫ਼ਾਰਮੈਟ ਲਾਗੂਕਰਨ

Model outputs must be structured and validated to reduce downstream injection risk.

ਡਾਊਨਸਟ੍ਰੀਮ ਇੰਜੈਕਸ਼ਨ ਜੋਖਮ ਨੂੰ ਘਟਾਉਣ ਲਈ ਮਾਡਲ ਆਊਟਪੁੱਟ ਦਾ ਢਾਂਚਾਗਤ ਅਤੇ ਪ੍ਰਮਾਣਿਤ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.1.1** | **Verify that** the application validates all model outputs against a defined schema and rejects any output that does not match. | 1 |
| **7.1.2** | **Verify that** model-generated output is bounded by length limits and termination controls. | 1 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਐਪਲੀਕੇਸ਼ਨ ਸਾਰੇ ਮਾਡਲ ਆਊਟਪੁੱਟ ਨੂੰ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਸਕੀਮਾ ਦੇ ਵਿਰੁੱਧ ਪ੍ਰਮਾਣਿਤ ਕਰਦੀ ਹੈ ਅਤੇ ਕਿਸੇ ਵੀ ਅਜਿਹੇ ਆਊਟਪੁੱਟ ਨੂੰ ਰੱਦ ਕਰਦੀ ਹੈ ਜੋ ਮੇਲ ਨਹੀਂ ਖਾਂਦਾ। | 1 |
| **7.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਕੀਤਾ ਆਊਟਪੁੱਟ ਲੰਬਾਈ ਸੀਮਾਵਾਂ ਅਤੇ ਸਮਾਪਤੀ ਨਿਯੰਤਰਣਾਂ[^0x10-C07-controls] ਦੁਆਰਾ ਸੀਮਿਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |

---

## C7.2 Hallucination Detection & Mitigation
## C7.2 Hallucination[^0x10-C07-hallucination] ਦੀ ਪਛਾਣ ਅਤੇ ਘਟਾਉਣਾ

Potentially inaccurate or fabricated content must be detected so unreliable outputs do not reach users or downstream systems.

ਸੰਭਾਵੀ ਤੌਰ 'ਤੇ ਗ਼ਲਤ ਜਾਂ ਮਨਘੜਤ ਸਮੱਗਰੀ (hallucination) ਦੀ ਪਛਾਣ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ ਤਾਂ ਜੋ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਆਊਟਪੁੱਟ ਉਪਭੋਗਤਾਵਾਂ ਜਾਂ ਡਾਊਨਸਟ੍ਰੀਮ ਸਿਸਟਮਾਂ ਤੱਕ ਨਾ ਪਹੁੰਚੇ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.2.1** | **Verify that** the system assesses the reliability of generated answers using a confidence estimation method. | 2 |
| **7.2.2** | **Verify that** the application automatically blocks answers or switches to a fallback message if the confidence score drops below a defined threshold. | 2 |
| **7.2.3** | **Verify that** for responses classified as high-risk by policy, the system performs an additional verification step. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਸਟਮ ਇੱਕ ਭਰੋਸਾ ਅਨੁਮਾਨ ਵਿਧੀ[^0x10-C07-confidence] (confidence estimation) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਤਿਆਰ ਕੀਤੇ ਜਵਾਬਾਂ ਦੀ ਭਰੋਸੇਯੋਗਤਾ ਦਾ ਮੁਲਾਂਕਣ ਕਰਦਾ ਹੈ। | 2 |
| **7.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜੇ ਭਰੋਸਾ ਸਕੋਰ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਥ੍ਰੈਸ਼ਹੋਲਡ[^0x10-C07-threshold] ਤੋਂ ਹੇਠਾਂ ਡਿੱਗ ਜਾਂਦਾ ਹੈ ਤਾਂ ਐਪਲੀਕੇਸ਼ਨ ਆਪਣੇ ਆਪ ਜਵਾਬਾਂ ਨੂੰ ਰੋਕ ਦਿੰਦੀ ਹੈ ਜਾਂ ਇੱਕ ਫ਼ਾਲਬੈਕ ਸੁਨੇਹੇ[^0x10-C07-fallback] 'ਤੇ ਬਦਲ ਜਾਂਦੀ ਹੈ। | 2 |
| **7.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਨੀਤੀ ਦੁਆਰਾ ਉੱਚ-ਜੋਖਮ ਵਜੋਂ ਵਰਗੀਕ੍ਰਿਤ[^0x10-C07-classified] ਕੀਤੇ ਜਵਾਬਾਂ ਲਈ, ਸਿਸਟਮ ਇੱਕ ਵਾਧੂ ਤਸਦੀਕ ਪੜਾਅ ਕਰਦਾ ਹੈ। | 3 |

---

## C7.3 Output Safety
## C7.3 ਆਊਟਪੁੱਟ ਸਲਾਮਤੀ

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
| **7.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਵੈਚਾਲਿਤ ਵਰਗੀਕਾਰ (classifiers) ਹਰ ਜਵਾਬ ਨੂੰ ਸਕੈਨ ਕਰਦੇ ਹਨ ਅਤੇ ਉਸ ਸਮੱਗਰੀ ਨੂੰ ਰੋਕਦੇ ਹਨ ਜੋ ਪਰਿਭਾਸ਼ਿਤ ਨੁਕਸਾਨਦੇਹ ਸਮੱਗਰੀ ਸ਼੍ਰੇਣੀਆਂ ਨਾਲ ਮੇਲ ਖਾਂਦੀ ਹੈ। | 1 |
| **7.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਆਊਟਪੁੱਟ ਫ਼ਿਲਟਰ ਉਹਨਾਂ ਜਵਾਬਾਂ ਦੀ ਪਛਾਣ ਕਰਦੇ ਹਨ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਰੋਕਦੇ ਹਨ ਜੋ system prompt ਦੀ ਸਮੱਗਰੀ ਜਾਂ ਬੈਕਐਂਡ ਡਾਟਾ ਦਾ ਖੁਲਾਸਾ ਕਰਦੇ ਹਨ। | 2 |
| **7.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਕੀਤੇ ਆਊਟਪੁੱਟ ਨੂੰ ਬਾਹਰ ਜਾਣ ਵਾਲੀਆਂ ਬੇਨਤੀਆਂ ਸ਼ੁਰੂ ਕਰਨ ਤੋਂ ਰੋਕਿਆ ਜਾਂਦਾ ਹੈ। | 2 |
| **7.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਆਊਟਪੁੱਟ ਦੀ ਲੁਕੀ ਹੋਈ, ਏਨਕੋਡ ਕੀਤੀ, ਜਾਂ ਗੁਮਰਾਹਕੁਨ ਸਮੱਗਰੀ ਲਈ ਜਾਂਚ ਕੀਤੀ ਜਾਂਦੀ ਹੈ ਜੋ homoglyph[^0x10-C07-homoglyph] (ਸਮਰੂਪ ਅੱਖਰ), ਫ਼ਾਰਮੈਟਿੰਗ, ਮੈਟਾਡਾਟਾ, ਜਾਂ ਢਾਂਚਾਗਤ ਖੇਤਰਾਂ ਰਾਹੀਂ ਬਣਾਈ ਗਈ ਹੋਵੇ। | 3 |

---

## C7.4 Source Attribution & Citation Integrity
## C7.4 ਸਰੋਤ-ਨਿਰਧਾਰਨ[^0x10-C07-attribution] ਅਤੇ ਹਵਾਲਾ ਅਖੰਡਤਾ

RAG-grounded outputs must be traceable to their source documents, with cited claims verifiably supported by retrieved content.

RAG-ਆਧਾਰਿਤ[^0x10-C07-grounded] ਆਊਟਪੁੱਟ ਦਾ ਆਪਣੇ ਸਰੋਤ ਦਸਤਾਵੇਜ਼ਾਂ ਤੱਕ ਟਰੇਸ ਕਰਨਯੋਗ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਹਵਾਲਾ ਦਿੱਤੇ ਗਏ ਦਾਅਵੇ ਪ੍ਰਾਪਤ ਕੀਤੀ ਸਮੱਗਰੀ ਦੁਆਰਾ ਤਸਦੀਕਯੋਗ ਢੰਗ ਨਾਲ ਸਮਰਥਿਤ ਹੋਣੇ ਲਾਜ਼ਮੀ ਹਨ।

| # | Description | Level |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.4.1** | **Verify that** responses generated using retrieval-augmented generation (RAG) include attribution to the source documents. | 1 |
| **7.4.2** | **Verify that** RAG attributions are derived from retrieval metadata and are not generated by the model, so provenance cannot be fabricated. | 1 |
| **7.4.3** | **Verify that** claims in a RAG response can be traced to the retrieved chunk. | 2 |
| **7.4.4** | **Verify that** generated media is watermarked to prove it was AI-generated. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :-------: | -------------------------------------------------------------------------------------------------------------------------------------------- | :---: |
| **7.4.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** retrieval-augmented generation (RAG) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਤਿਆਰ ਕੀਤੇ ਜਵਾਬਾਂ ਵਿੱਚ ਸਰੋਤ ਦਸਤਾਵੇਜ਼ਾਂ ਦਾ ਸਰੋਤ-ਨਿਰਧਾਰਨ (attribution) ਸ਼ਾਮਲ ਹੁੰਦਾ ਹੈ। | 1 |
| **7.4.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** RAG ਸਰੋਤ-ਨਿਰਧਾਰਨ ਪ੍ਰਾਪਤੀ ਮੈਟਾਡਾਟਾ ਤੋਂ ਲਏ ਜਾਂਦੇ ਹਨ ਅਤੇ ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਨਹੀਂ ਕੀਤੇ ਜਾਂਦੇ, ਤਾਂ ਜੋ ਮੂਲ-ਸਰੋਤ[^0x10-C07-provenance] (provenance) ਘੜਿਆ ਨਾ ਜਾ ਸਕੇ। | 1 |
| **7.4.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇੱਕ RAG ਜਵਾਬ ਵਿਚਲੇ ਦਾਅਵਿਆਂ ਨੂੰ ਪ੍ਰਾਪਤ ਕੀਤੇ ਚੰਕ[^0x10-C07-chunk] (chunk) ਤੱਕ ਟਰੇਸ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ। | 2 |
| **7.4.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਤਿਆਰ ਕੀਤੇ ਮੀਡੀਆ ਨੂੰ ਵਾਟਰਮਾਰਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਤਾਂ ਜੋ ਇਹ ਸਾਬਤ ਹੋ ਸਕੇ ਕਿ ਇਹ AI ਦੁਆਰਾ ਤਿਆਰ ਕੀਤਾ ਗਿਆ ਸੀ। | 3 |

---

## References
## ਹਵਾਲੇ

* [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
* [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
* [OWASP LLM09:2025 Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/)
* [NIST AI 600-1: Generative AI Profile (AI RMF Companion)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
* [MITRE ATLAS](https://atlas.mitre.org/)

[^0x10-C07-behavior]: **behavior** (EN) -> ਵਿਵਹਾਰ — carried over from the ASVS sibling corpus's use of ਵਿਵਹਾਰ for system behavior, chosen over ਆਚਰਣ ("conduct") because that word carries a moral/ethical register that would wrongly ascribe agency to a model. Full discussion: OPEN-QUESTIONS.md Q7.
[^0x10-C07-output]: **output** (EN, model output) -> ਆਊਟਪੁੱਟ — kept as a loan to mirror the ASVS corpus's ਇਨਪੁੱਟ (input), so the input/output pair reads symmetrically across both standards; ਨਤੀਜਾ ("result") was rejected because it would collide with a different sense. Full discussion: OPEN-QUESTIONS.md Q78.
[^0x10-C07-assurance]: **Safety Assurance** (EN, chapter title) -> ਸਲਾਮਤੀ ਭਰੋਸਾ — conforms to the corpus's standing pick of ਭਰੋਸਾ for *assurance*, even though the same word also carries *confidence* elsewhere in this chapter; the overload does not create ambiguity in any single sentence, so this chapter conforms rather than splitting the term. Full discussion: OPEN-QUESTIONS.md Q67.
[^0x10-C07-unsafe]: **unsafe** (EN) -> ਗ਼ੈਰ-ਸਲਾਮਤ — derived from ਸਲਾਮਤ (safety) rather than ਸੁਰੱਖਿਅਤ (which derives from ਸੁਰੱਖਿਆ, reserved for *security*), so this chapter's requirement text does not contradict its own title two paragraphs later. Full discussion: OPEN-QUESTIONS.md Q66.
[^0x10-C07-malformed]: **malformed** (EN) -> ਵਿਗੜੇ (ਹੋਏ) — uses the same root ਵਿਗਾੜ already applied elsewhere in the corpus to *adversarial perturbation* and *corruption*; flagged as an unresolved three-way overload rather than corrected, since no single sentence here is ambiguous. Full discussion: OPEN-QUESTIONS.md Q35.
[^0x10-C07-downstream]: **downstream** (EN, downstream systems/risk) -> ਡਾਊਨਸਟ੍ਰੀਮ — kept as a loan because "downstream" is pipeline vocabulary with no settled Panjabi equivalent, and a literal water-flow rendering would mislead a reader into a physical-flow reading. Full discussion: OPEN-QUESTIONS.md Q77.
[^0x10-C07-controls]: **controls** (EN, termination controls) -> ਨਿਯੰਤਰਣਾਂ — normalised from an earlier inconsistency where the same underlying word appeared as the loan ਕੰਟਰੋਲ in one chapter's requirement text; standalone *control(s)* stays ਨਿਯੰਤਰਣ corpus-wide, with the loan ਕੰਟਰੋਲ reserved only for the fixed compound ਪਹੁੰਚ ਕੰਟਰੋਲ (access control). Full discussion: OPEN-QUESTIONS.md Q80.
[^0x10-C07-hallucination]: **hallucination** (EN) -> `hallucination` (retained, glossed ਮਨਘੜਤ ਸਮੱਗਰੀ) — kept in Latin script because ਭਰਮ, ਭੁਲੇਖਾ, and ਵਹਿਮ all carry Gurbani-specific spiritual weight (delusion, doubt) that this term must not borrow; treated as a named AI failure mode with a neutral descriptive gloss instead. Full discussion: OPEN-QUESTIONS.md Q65.
[^0x10-C07-confidence]: **confidence estimation method** (EN) -> ਭਰੋਸਾ ਅਨੁਮਾਨ ਵਿਧੀ — built on ਭਰੋਸਾ rather than ਵਿਸ਼ਵਾਸ, which leans toward faith/belief and was excluded as too devotionally coloured for an ML confidence score. Full discussion: OPEN-QUESTIONS.md Q68.
[^0x10-C07-threshold]: **threshold** (EN) -> ਥ੍ਰੈਸ਼ਹੋਲਡ — kept as a loan rather than ਸੀਮਾ, which is already bound to *limit* elsewhere in this same chapter (output length limits), so the limit/threshold contrast stays visible within one requirement set. Full discussion: OPEN-QUESTIONS.md Q69.
[^0x10-C07-fallback]: **fallback message** (EN) -> ਫ਼ਾਲਬੈਕ ਸੁਨੇਹਾ — "fallback" kept as a loan because it is settled software-engineering vocabulary with no Panjabi equivalent, and ਬਦਲਵਾਂ ("alternative") was rejected for understating that a fallback is specifically the *safe* response. Full discussion: OPEN-QUESTIONS.md Q70.
[^0x10-C07-classified]: **classified (as high-risk)** (EN) -> ਵਰਗੀਕ੍ਰਿਤ — shares the ਵਰਗੀਕਰਨ root already settled for *classifier* elsewhere in the corpus, kept deliberately mechanical since a classifier here is a model acting as a filter, not a reasoning agent. Full discussion: OPEN-QUESTIONS.md Q76.
[^0x10-C07-homoglyph]: **homoglyph** (EN) -> `homoglyph` (retained, glossed ਸਮਰੂਪ ਅੱਖਰ) — follows the corpus's pattern of retaining named attack/technique terms in English (as with prompt injection, jailbreak) with a native gloss for readability, since this is what an implementer would search for in Unicode security literature. Full discussion: OPEN-QUESTIONS.md Q75.
[^0x10-C07-attribution]: **source attribution** (EN) -> ਸਰੋਤ-ਨਿਰਧਾਰਨ — reuses the rendering already fixed for dataset-use attribution, kept distinct from ਹਵਾਲਾ (citation) because 7.4.2 depends on that difference: attributions must come from retrieval metadata, not the model, while a citation is what the reader sees. Full discussion: OPEN-QUESTIONS.md Q72.
[^0x10-C07-grounded]: **RAG-grounded** (EN) -> RAG-ਆਧਾਰਿਤ — "grounding" is a high-risk metaphor term, so the neutral technical sense ("anchored in retrieved evidence") is rendered as ਆਧਾਰਿਤ (based on) rather than any literal earth/ground calque that would import imagery the source does not intend. Full discussion: OPEN-QUESTIONS.md Q71.
[^0x10-C07-provenance]: **provenance** (EN) -> ਮੂਲ-ਸਰੋਤ ("root-source") — states the "documented chain of origin" sense plainly, avoiding ਉਤਪਤੀ ("origination"), which carries creation-narrative overtones in Panjabi religious register. Full discussion: OPEN-QUESTIONS.md Q73.
[^0x10-C07-chunk]: **chunk** (EN, retrieved chunk) -> ਚੰਕ — kept as a loan because a chunk is a specific RAG-pipeline retrieval unit, not a generic piece of text; ਖੰਡ ("segment") was additionally excluded for its near-collision with ਅਖੰਡਤਾ (integrity), the locked term appearing in this same chapter's C7.4 title. Full discussion: OPEN-QUESTIONS.md Q74.
