<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md -->
<!-- Translator: GeeksikhSecurity -->

# C1 Training Data Integrity & Traceability
# C1 ਸਿਖਲਾਈ ਡਾਟਾ[^0x10-C01-training-data] ਅਖੰਡਤਾ ਅਤੇ ਟਰੇਸਯੋਗਤਾ[^0x10-C01-traceability]

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses protecting the integrity and traceability of training data as it is sourced, handled, and maintained.

ਇਹ ਅਧਿਆਇ ਸਿਖਲਾਈ ਡਾਟਾ (training data) ਦੀ ਅਖੰਡਤਾ (integrity) ਅਤੇ ਟਰੇਸਯੋਗਤਾ (traceability) ਦੀ ਰਾਖੀ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ, ਜਿਵੇਂ ਕਿ ਇਹ ਡਾਟਾ ਪ੍ਰਾਪਤ ਕੀਤਾ, ਸੰਭਾਲਿਆ, ਅਤੇ ਬਰਕਰਾਰ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ।

---

## C1.1 Training Data Origin & Data Security
## C1.1 ਸਿਖਲਾਈ ਡਾਟਾ ਦਾ ਮੂਲ ਅਤੇ ਡਾਟਾ ਸੁਰੱਖਿਆ

Training data origin and security are critical to the trustworthiness of any AI system. Datasets must be sourced from verifiable origins, tracked across their full lifecycle, and protected against tampering, corruption, and poisoning so that unauthorized modification can be detected.

ਸਿਖਲਾਈ ਡਾਟਾ ਦਾ ਮੂਲ ਅਤੇ ਸੁਰੱਖਿਆ ਕਿਸੇ ਵੀ AI ਸਿਸਟਮ ਦੀ ਭਰੋਸੇਯੋਗਤਾ ਲਈ ਨਾਜ਼ੁਕ ਹਨ। ਡਾਟਾਸੈੱਟ ਤਸਦੀਕਯੋਗ ਮੂਲਾਂ ਤੋਂ ਪ੍ਰਾਪਤ ਕੀਤੇ ਜਾਣੇ ਲਾਜ਼ਮੀ ਹਨ, ਆਪਣੇ ਪੂਰੇ ਜੀਵਨ-ਚੱਕਰ ਦੌਰਾਨ ਟਰੈਕ ਕੀਤੇ ਜਾਣੇ ਲਾਜ਼ਮੀ ਹਨ, ਅਤੇ ਛੇੜਛਾੜ, ਵਿਗਾੜ[^0x10-C01-corruption], ਅਤੇ poisoning[^0x10-C01-poisoning] ਤੋਂ ਸੁਰੱਖਿਅਤ ਰੱਖੇ ਜਾਣੇ ਲਾਜ਼ਮੀ ਹਨ ਤਾਂ ਜੋ ਅਣਅਧਿਕਾਰਤ ਸੋਧ ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾ ਸਕੇ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.1.1** | **Verify that** training data includes only features, attributes, and fields required for the model's stated purpose. | 1 |
| **1.1.2** | **Verify that** an up-to-date inventory is kept of every training-data source, including its origin, responsible party, license, collection method, intended use constraints, and processing history. | 2 |
| **1.1.3** | **Verify that** data integrity is provided when training data is stored and transferred. | 2 |
| **1.1.4** | **Verify that** integrity monitoring is applied to guard against unauthorized modifications or corruption of training data. | 2 |
| **1.1.5** | **Verify that** datasets are watermarked so their use can be attributed and any unauthorized use detected. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਖਲਾਈ ਡਾਟਾ ਵਿੱਚ ਸਿਰਫ਼ ਉਹੀ ਫ਼ੀਚਰ[^0x10-C01-features] (features), ਗੁਣ, ਅਤੇ ਖੇਤਰ ਸ਼ਾਮਲ ਹਨ ਜੋ ਮਾਡਲ ਦੇ ਦੱਸੇ ਗਏ ਮਕਸਦ ਲਈ ਲੋੜੀਂਦੇ ਹਨ। | 1 |
| **1.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਸਿਖਲਾਈ-ਡਾਟਾ ਸਰੋਤ ਦੀ ਇੱਕ ਅੱਪ-ਟੂ-ਡੇਟ ਇਨਵੈਂਟਰੀ ਰੱਖੀ ਜਾਂਦੀ ਹੈ, ਜਿਸ ਵਿੱਚ ਉਸਦਾ ਮੂਲ, ਜ਼ਿੰਮੇਵਾਰ ਧਿਰ, ਲਾਇਸੰਸ, ਇਕੱਤਰੀਕਰਨ ਵਿਧੀ, ਇੱਛਤ ਵਰਤੋਂ ਦੀਆਂ ਪਾਬੰਦੀਆਂ, ਅਤੇ ਪ੍ਰਕਿਰਿਆ ਇਤਿਹਾਸ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **1.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਦੋਂ ਸਿਖਲਾਈ ਡਾਟਾ ਦਾ ਭੰਡਾਰਨ ਅਤੇ ਪ੍ਰਸਾਰਣ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਤਾਂ ਡਾਟਾ ਅਖੰਡਤਾ ਪ੍ਰਦਾਨ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **1.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਖਲਾਈ ਡਾਟਾ ਦੀਆਂ ਅਣਅਧਿਕਾਰਤ ਸੋਧਾਂ ਜਾਂ ਵਿਗਾੜ ਤੋਂ ਬਚਾਅ ਲਈ ਅਖੰਡਤਾ ਨਿਗਰਾਨੀ ਲਾਗੂ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **1.1.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡਾਟਾਸੈੱਟਾਂ ਨੂੰ ਵਾਟਰਮਾਰਕ[^0x10-C01-watermarking] ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਤਾਂ ਜੋ ਉਹਨਾਂ ਦੀ ਵਰਤੋਂ ਦਾ ਸਰੋਤ-ਨਿਰਧਾਰਨ[^0x10-C01-attribution] (attribution) ਕੀਤਾ ਜਾ ਸਕੇ ਅਤੇ ਕਿਸੇ ਵੀ ਅਣਅਧਿਕਾਰਤ ਵਰਤੋਂ ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾ ਸਕੇ। | 3 |

---

## C1.2 Data Labeling and Annotation Security
## C1.2 ਡਾਟਾ ਲੇਬਲਿੰਗ[^0x10-C01-labeling-annotation] ਅਤੇ ਐਨੋਟੇਸ਼ਨ ਸੁਰੱਖਿਆ

Labeling and annotation processes must be protected against unauthorized modification, data leakage, and integrity compromise. Annotation platforms should enforce access control, preserve auditability, and protect labeling artifacts and sensitive label content throughout the training pipeline.

ਲੇਬਲਿੰਗ ਅਤੇ ਐਨੋਟੇਸ਼ਨ ਪ੍ਰਕਿਰਿਆਵਾਂ ਨੂੰ ਅਣਅਧਿਕਾਰਤ ਸੋਧ, ਡਾਟਾ ਲੀਕੇਜ, ਅਤੇ ਅਖੰਡਤਾ ਦੇ ਸਮਝੌਤੇ (compromise) ਤੋਂ ਸੁਰੱਖਿਅਤ ਰੱਖਿਆ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ। ਐਨੋਟੇਸ਼ਨ ਪਲੇਟਫ਼ਾਰਮਾਂ ਨੂੰ ਪਹੁੰਚ ਕੰਟਰੋਲ ਲਾਗੂ ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ, ਆਡਿਟਯੋਗਤਾ ਬਰਕਰਾਰ ਰੱਖਣੀ ਚਾਹੀਦੀ ਹੈ, ਅਤੇ ਪੂਰੀ ਸਿਖਲਾਈ ਪਾਈਪਲਾਈਨ ਦੌਰਾਨ ਲੇਬਲਿੰਗ ਆਰਟੀਫ਼ੈਕਟਾਂ ਅਤੇ ਸੰਵੇਦਨਸ਼ੀਲ ਲੇਬਲ ਸਮੱਗਰੀ ਦੀ ਰਾਖੀ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.2.1** | **Verify that** labeling platforms enforce access controls that restrict who can create, modify, or approve annotations. | 1 |
| **1.2.2** | **Verify that** cryptographic integrity is applied to labeling artifacts. | 2 |
| **1.2.3** | **Verify that** sensitive information in labels is redacted, anonymized, or encrypted before being used in any labeling artifact. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਲੇਬਲਿੰਗ ਪਲੇਟਫ਼ਾਰਮ ਅਜਿਹੇ ਪਹੁੰਚ ਕੰਟਰੋਲ ਲਾਗੂ ਕਰਦੇ ਹਨ ਜੋ ਇਹ ਸੀਮਤ ਕਰਦੇ ਹਨ ਕਿ ਕੌਣ ਐਨੋਟੇਸ਼ਨਾਂ ਬਣਾ, ਸੋਧ, ਜਾਂ ਮਨਜ਼ੂਰ ਕਰ ਸਕਦਾ ਹੈ। | 1 |
| **1.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਲੇਬਲਿੰਗ ਆਰਟੀਫ਼ੈਕਟਾਂ ਉੱਤੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਅਖੰਡਤਾ ਲਾਗੂ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **1.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਲੇਬਲਾਂ ਵਿੱਚ ਮੌਜੂਦ ਸੰਵੇਦਨਸ਼ੀਲ ਜਾਣਕਾਰੀ ਨੂੰ ਕਿਸੇ ਵੀ ਲੇਬਲਿੰਗ ਆਰਟੀਫ਼ੈਕਟ ਵਿੱਚ ਵਰਤੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਰਿਡੈਕਟ (redacted), ਗੁਮਨਾਮ, ਜਾਂ ਏਨਕ੍ਰਿਪਟ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |

---

## C1.3 Training Data Quality and Security Assurance
## C1.3 ਸਿਖਲਾਈ ਡਾਟਾ ਗੁਣਵੱਤਾ ਅਤੇ ਸੁਰੱਖਿਆ ਭਰੋਸਾ[^0x10-C01-assurance]

Quality and security assurance controls help detect corruption, poisoning, labeling errors, and exploitable dataset patterns before they affect model behavior. Pipelines should combine automated validation, poisoning detection, label quality checks, and bias analysis.

ਗੁਣਵੱਤਾ ਅਤੇ ਸੁਰੱਖਿਆ ਭਰੋਸਾ ਨਿਯੰਤਰਣ ਵਿਗਾੜ, poisoning, ਲੇਬਲਿੰਗ ਗਲਤੀਆਂ, ਅਤੇ ਸ਼ੋਸ਼ਣਯੋਗ ਡਾਟਾਸੈੱਟ ਪੈਟਰਨਾਂ ਦਾ ਪਤਾ ਲਗਾਉਣ ਵਿੱਚ ਮਦਦ ਕਰਦੇ ਹਨ, ਇਸ ਤੋਂ ਪਹਿਲਾਂ ਕਿ ਉਹ ਮਾਡਲ ਦੇ ਵਿਵਹਾਰ ਨੂੰ ਪ੍ਰਭਾਵਿਤ ਕਰਨ। ਪਾਈਪਲਾਈਨਾਂ ਨੂੰ ਸਵੈਚਾਲਿਤ ਪ੍ਰਮਾਣਿਕਤਾ, poisoning ਪਛਾਣ, ਲੇਬਲ ਗੁਣਵੱਤਾ ਜਾਂਚਾਂ, ਅਤੇ ਪੱਖਪਾਤ (bias) ਵਿਸ਼ਲੇਸ਼ਣ ਨੂੰ ਜੋੜਨਾ ਚਾਹੀਦਾ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.3.1** | **Verify that** training and fine-tuning pipelines implement poisoning detection techniques to identify potential data poisoning or unintentional corruption in training data. | 2 |
| **1.3.2** | **Verify that** automatically generated labels are subject to confidence thresholds and consistency checks to detect misleading or low-confidence labels. | 2 |
| **1.3.3** | **Verify that** models used in security-relevant decisions are evaluated for bias patterns. | 2 |
| **1.3.4** | **Verify that** disallowed content is detected and removed before training. | 2 |
| **1.3.5** | **Verify that** defenses against clean-label poisoning attacks are implemented. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------------- | :---: |
| **1.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਖਲਾਈ ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ (fine-tuning) ਪਾਈਪਲਾਈਨਾਂ ਸਿਖਲਾਈ ਡਾਟਾ ਵਿੱਚ ਸੰਭਾਵੀ data poisoning (ਡਾਟਾ ਜ਼ਹਿਰੀਕਰਨ) ਜਾਂ ਅਣਇੱਛਤ ਵਿਗਾੜ ਦੀ ਪਛਾਣ ਕਰਨ ਲਈ poisoning ਪਛਾਣ ਤਕਨੀਕਾਂ ਲਾਗੂ ਕਰਦੀਆਂ ਹਨ। | 2 |
| **1.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਵੈਚਾਲਿਤ ਢੰਗ ਨਾਲ ਪੈਦਾ ਕੀਤੇ ਲੇਬਲ ਗੁੰਮਰਾਹਕੁੰਨ ਜਾਂ ਘੱਟ-ਭਰੋਸੇ[^0x10-C01-confidence-threshold] ਵਾਲੇ ਲੇਬਲਾਂ ਦਾ ਪਤਾ ਲਗਾਉਣ ਲਈ ਭਰੋਸਾ ਥ੍ਰੈਸ਼ਹੋਲਡਾਂ ਅਤੇ ਇਕਸਾਰਤਾ ਜਾਂਚਾਂ ਦੇ ਅਧੀਨ ਹਨ। | 2 |
| **1.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸੁਰੱਖਿਆ-ਸੰਬੰਧਿਤ ਫ਼ੈਸਲਿਆਂ ਵਿੱਚ ਵਰਤੇ ਜਾਣ ਵਾਲੇ ਮਾਡਲਾਂ ਦਾ ਪੱਖਪਾਤ (bias) ਪੈਟਰਨਾਂ ਲਈ ਮੁਲਾਂਕਣ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **1.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਖਲਾਈ ਤੋਂ ਪਹਿਲਾਂ ਮਨਾਹੀ ਵਾਲੀ ਸਮੱਗਰੀ ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਉਸਨੂੰ ਹਟਾਇਆ ਜਾਂਦਾ ਹੈ। | 2 |
| **1.3.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** clean-label poisoning ਹਮਲਿਆਂ ਵਿਰੁੱਧ ਬਚਾਅ ਲਾਗੂ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 3 |

---

## References
## ਹਵਾਲੇ

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [EU AI Act: Article 10: Data & Data Governance](https://artificialintelligenceact.eu/article/10/)
* [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
* [MITRE ATLAS: Poison Training Data (AML.T0020)](https://atlas.mitre.org/techniques/AML.T0020)
* [ISO/IEC 42001:2023 Artificial Intelligence Management System](https://www.iso.org/standard/42001)

[^0x10-C01-training-data]: **training data** (EN) -> ਸਿਖਲਾਈ ਡਾਟਾ — ਸਿਖਲਾਈ is the neutral, non-devotional Panjabi word for training, chosen over ਅਭਿਆਸ, which carries a Gurmat devotional-practice connotation. Full discussion: OPEN-QUESTIONS.md Q37.
[^0x10-C01-traceability]: **traceability** (EN) -> ਟਰੇਸਯੋਗਤਾ — a hybrid of the English root "trace" with the productive Panjabi suffix "-ਯੋਗਤਾ", chosen because native alternatives either read clumsily or collide with "discoverability". Full discussion: OPEN-QUESTIONS.md Q38.
[^0x10-C01-corruption]: **corruption** (EN) -> ਵਿਗਾੜ — chosen over ਭ੍ਰਿਸ਼ਟਾਚਾਰ, the standard Panjabi word for bribery/moral corruption, which would misread a data-integrity event as an accusation of human misconduct. Full discussion: OPEN-QUESTIONS.md Q40.
[^0x10-C01-poisoning]: **data poisoning** (EN) -> retained as `poisoning` / `data poisoning`, glossed once as ਡਾਟਾ ਜ਼ਹਿਰੀਕਰਨ — kept in English on first mention so the reader can match it to the MITRE ATLAS AML.T0020 reference this chapter cites. Full discussion: OPEN-QUESTIONS.md Q39.
[^0x10-C01-features]: **features** (EN) -> ਫ਼ੀਚਰ — a loan glossed in English because rendering it as ਵਿਸ਼ੇਸ਼ਤਾ would collapse it into the adjacent, deliberately distinct term "attributes" (ਗੁਣ) in the same requirement. Full discussion: OPEN-QUESTIONS.md Q46.
[^0x10-C01-watermarking]: **watermarked** (EN) -> ਵਾਟਰਮਾਰਕ — kept as a loan because the literal calque ਜਲ-ਚਿੰਨ੍ਹ (paper watermark) conveys nothing about the ML provenance-attribution technique meant here. Full discussion: OPEN-QUESTIONS.md Q43.
[^0x10-C01-attribution]: **attribution** (EN) -> ਸਰੋਤ-ਨਿਰਧਾਰਨ — chosen over ਸਿਹਰਾ ("credit", a congratulatory register) because 1.1.5 means tracing use back to a source dataset, not crediting an author. Full discussion: OPEN-QUESTIONS.md Q45.
[^0x10-C01-labeling-annotation]: **labeling, annotation** (EN) -> ਲੇਬਲਿੰਗ, ਐਨੋਟੇਸ਼ਨ — kept as two distinct loans because AISVS treats labeling and annotation as separate terms of art for one workflow, and a single native word would collapse that distinction. Full discussion: OPEN-QUESTIONS.md Q41.
[^0x10-C01-assurance]: **assurance** (EN) -> ਭਰੋਸਾ — chosen over ਯਕੀਨ-ਦਹਾਨੀ, which names the act of one party reassuring another rather than the grounded confidence a verification standard means. Full discussion: OPEN-QUESTIONS.md Q44.
[^0x10-C01-confidence-threshold]: **confidence threshold, low-confidence** (EN) -> ਭਰੋਸਾ ਥ੍ਰੈਸ਼ਹੋਲਡ, ਘੱਟ-ਭਰੋਸੇ — ਭਰੋਸਾ was preferred over ਆਤਮ-ਵਿਸ਼ਵਾਸ, which is human self-confidence and would anthropomorphise the model. Full discussion: OPEN-QUESTIONS.md Q42.
