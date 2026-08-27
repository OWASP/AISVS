<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C06-Supply-Chain.md -->
<!-- Translator: GeeksikhSecurity -->

# C6 Supply Chain Security for Models
# C6 ਮਾਡਲਾਂ ਲਈ ਸਪਲਾਈ ਚੇਨ[^0x10-C06-supplychain] ਸੁਰੱਖਿਆ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses defending against AI supply chain attacks that exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code.

ਇਹ ਅਧਿਆਇ AI ਸਪਲਾਈ ਚੇਨ (supply chain) ਹਮਲਿਆਂ ਤੋਂ ਬਚਾਅ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ, ਜੋ ਬੈਕਡੋਰ, ਪੱਖਪਾਤ[^0x10-C06-bias] (bias), ਜਾਂ ਸ਼ੋਸ਼ਣਯੋਗ ਕੋਡ ਨੂੰ ਅੰਦਰ ਬਿਠਾਉਣ ਲਈ ਤੀਜੀ-ਧਿਰ ਦੇ ਮਾਡਲਾਂ, ਫ੍ਰੇਮਵਰਕਾਂ, ਜਾਂ ਡਾਟਾਸੈੱਟਾਂ ਦਾ ਸ਼ੋਸ਼ਣ ਕਰਦੇ ਹਨ।

---

## C6.1 Model Artifact Integrity
## C6.1 ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਅਖੰਡਤਾ

Third-party model origins must be authenticated and checked for hidden behavior before fine-tuning or deployment, and AI artifacts should be downloaded only from approved sources.

ਤੀਜੀ-ਧਿਰ ਦੇ ਮਾਡਲਾਂ ਦੇ ਮੂਲ ਦਾ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ (fine-tuning) ਜਾਂ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਪ੍ਰਮਾਣੀਕਰਨ (authentication) ਕੀਤਾ ਜਾਣਾ ਅਤੇ ਲੁਕਵੇਂ ਵਿਵਹਾਰ[^0x10-C06-behavior] ਲਈ ਜਾਂਚ ਕੀਤੀ ਜਾਣੀ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ AI ਆਰਟੀਫ਼ੈਕਟ ਸਿਰਫ਼ ਪ੍ਰਵਾਨਿਤ ਸਰੋਤਾਂ ਤੋਂ ਹੀ ਡਾਊਨਲੋਡ ਕੀਤੇ ਜਾਣੇ ਚਾਹੀਦੇ ਹਨ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **Verify that** models are scanned for malicious code before import. | 1 |
| **6.1.2** | **Verify that** model weights, datasets, and fine-tuning adapters are downloaded only from approved sources. | 1 |
| **6.1.3** | **Verify that** every third-party model artifact can be integrity-verified. | 2 |
| **6.1.4** | **Verify that** models pass a behavioral acceptance test suite before being promoted to any non-development environment. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲਾਂ ਨੂੰ ਆਯਾਤ (import) ਤੋਂ ਪਹਿਲਾਂ ਖ਼ਤਰਨਾਕ ਕੋਡ ਲਈ ਸਕੈਨ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **6.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਵੇਟਸ[^0x10-C06-weights] (model weights), ਡਾਟਾਸੈੱਟ[^0x10-C06-dataset], ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਅਡੈਪਟਰ[^0x10-C06-finetuning] ਸਿਰਫ਼ ਪ੍ਰਵਾਨਿਤ ਸਰੋਤਾਂ ਤੋਂ ਹੀ ਡਾਊਨਲੋਡ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 1 |
| **6.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਤੀਜੀ-ਧਿਰ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਦੀ ਅਖੰਡਤਾ (integrity) ਦੀ ਤਸਦੀਕ ਕੀਤੀ ਜਾ ਸਕਦੀ ਹੈ। | 2 |
| **6.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਕਿਸੇ ਵੀ ਗ਼ੈਰ-ਵਿਕਾਸ ਵਾਤਾਵਰਣ ਵਿੱਚ ਤਰੱਕੀ ਦਿੱਤੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਇੱਕ ਵਿਵਹਾਰਕ ਸਵੀਕ੍ਰਿਤੀ ਟੈਸਟ ਸੂਟ ਪਾਸ ਕਰਦੇ ਹਨ। | 2 |

---

## C6.2 AI BOM & Supply Chain Monitoring
## C6.2 AI BOM[^0x10-C06-aibom] ਅਤੇ ਸਪਲਾਈ ਚੇਨ ਨਿਗਰਾਨੀ

Detailed AI-specific bills of materials must be generated and signed, with readiness to respond to supply chain compromise events.

ਵਿਸਤ੍ਰਿਤ AI-ਵਿਸ਼ੇਸ਼ ਬਿਲ ਆਫ਼ ਮਟੀਰੀਅਲਜ਼ (bills of materials) ਤਿਆਰ ਅਤੇ ਦਸਤਖ਼ਤ ਕੀਤੇ ਜਾਣੇ ਲਾਜ਼ਮੀ ਹਨ, ਨਾਲ ਹੀ ਸਪਲਾਈ ਚੇਨ ਦੇ ਸਮਝੌਤੇ (compromise) ਦੀਆਂ ਘਟਨਾਵਾਂ ਦਾ ਜਵਾਬ ਦੇਣ ਦੀ ਤਿਆਰੀ ਸਮੇਤ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **Verify that** every model artifact publishes a version-controlled, machine-readable AI BOM listing datasets, weights, licenses, and data-origin statements. | 1 |
| **6.2.2** | **Verify that** AI BOMs are cryptographically signed before deployment. | 2 |
| **6.2.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata is missing. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਇੱਕ ਵਰਜ਼ਨ-ਨਿਯੰਤਰਿਤ, ਮਸ਼ੀਨ-ਪੜ੍ਹਨਯੋਗ AI BOM ਪ੍ਰਕਾਸ਼ਿਤ ਕਰਦਾ ਹੈ ਜਿਸ ਵਿੱਚ ਡਾਟਾਸੈੱਟ, ਵੇਟਸ, ਲਾਇਸੈਂਸ, ਅਤੇ ਡਾਟਾ-ਮੂਲ ਬਿਆਨ ਸੂਚੀਬੱਧ ਹੁੰਦੇ ਹਨ। | 1 |
| **6.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI BOM ਨੂੰ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਦਸਤਖ਼ਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **6.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜੇ ਕਿਸੇ ਕੰਪੋਨੈਂਟ[^0x10-C06-component] ਦਾ ਮੈਟਾਡਾਟਾ ਗ਼ੈਰ-ਮੌਜੂਦ ਹੋਵੇ ਤਾਂ AI BOM ਸੰਪੂਰਨਤਾ ਜਾਂਚਾਂ ਬਿਲਡ ਨੂੰ ਫ਼ੇਲ੍ਹ ਕਰ ਦਿੰਦੀਆਂ ਹਨ। | 2 |

---

## References
## ਹਵਾਲੇ

* [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
* [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
* [SBOM Overview: CISA](https://www.cisa.gov/sbom)
* [CycloneDX: Machine Learning Bill of Materials](https://cyclonedx.org/capabilities/mlbom/)
* [OWASP AIBOM](https://genai.owasp.org/owasp-aibom/)

[^0x10-C06-supplychain]: **supply chain** (EN) -> ਸਪਲਾਈ ਚੇਨ — kept as a loan rather than a coined native compound (ਪੂਰਤੀ ਲੜੀ, "provision chain") because the ASVS sibling corpus resolves modern infrastructure compounds toward the loan, and "supply chain" is already the circulating form in Panjabi business/technology press. Full discussion: OPEN-QUESTIONS.md Q1.
[^0x10-C06-bias]: **bias** (EN, AI/model bias) -> ਪੱਖਪਾਤ — chosen over ਪੂਰਵ-ਧਾਰਨਾ ("preconception") because that word would ascribe a mental state to the model, whereas ਪੱਖਪਾਤ names the output property (systematically unfair outcomes) without anthropomorphising. Full discussion: OPEN-QUESTIONS.md Q6.
[^0x10-C06-behavior]: **behavior** (EN) -> ਵਿਵਹਾਰ — a consistency carry-over from the ASVS sibling corpus's use of ਵਿਵਹਾਰ for system behavior, chosen over ਆਚਰਣ ("conduct") because that word carries a moral register unsuitable for a machine. Full discussion: OPEN-QUESTIONS.md Q7.
[^0x10-C06-weights]: **model weights** (EN) -> ਮਾਡਲ ਵੇਟਸ — kept as a loan because the native candidates (ਭਾਰ, ਵਜ਼ਨ) carry only the physical-mass sense and would mislead a reader, whereas a weight here is a learned numeric parameter and a distributable artifact name in practice. Full discussion: OPEN-QUESTIONS.md Q2.
[^0x10-C06-dataset]: **dataset** (EN) -> ਡਾਟਾਸੈੱਟ — kept as a loan rather than ਅੰਕੜਾ-ਸਮੂਹ ("statistics group"), which would actively mislead for text/image corpora, since a dataset here is a named, versioned, downloadable artifact rather than a generic collection. Full discussion: OPEN-QUESTIONS.md Q5.
[^0x10-C06-finetuning]: **fine-tuning adapter** (EN) -> ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਅਡੈਪਟਰ — "fine-tuning" is retained as a loan because it names a specific training operation distinct from pre-training, retraining, and prompt-tuning, and a descriptive native rendering would lose that specificity. Full discussion: OPEN-QUESTIONS.md Q3.
[^0x10-C06-aibom]: **AI BOM** (EN) -> AI BOM (retained) — the acronym stays in Latin script per the corpus's always-retained rule for acronyms, matching how SBOM/CycloneDX appear in this chapter's own reference list. Full discussion: OPEN-QUESTIONS.md Q4.
[^0x10-C06-component]: **component** (EN) -> ਕੰਪੋਨੈਂਟ — kept as the established loan rather than the native ਹਿੱਸਾ used for generic parts elsewhere in the corpus; a full-corpus audit found the two forms split by usage and recommended normalising the minority native sites toward this one. Full discussion: OPEN-QUESTIONS.md Q95.
