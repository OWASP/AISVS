<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md -->
<!-- Translator: GeeksikhSecurity -->

# C8 Memory, Embeddings & Vector Database Security
# C8 ਮੈਮੋਰੀ[^0x10-C08-memory], Embeddings ਅਤੇ ਵੈਕਟਰ ਡਾਟਾਬੇਸ ਸੁਰੱਖਿਆ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses securing the embeddings and vector stores that act as semi-persistent and persistent "memory" for AI systems through Retrieval-Augmented Generation (RAG).

ਇਹ ਅਧਿਆਇ ਉਹਨਾਂ embeddings ਅਤੇ ਵੈਕਟਰ ਸਟੋਰਾਂ ਨੂੰ ਸੁਰੱਖਿਅਤ ਕਰਨ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ ਜੋ Retrieval-Augmented Generation (RAG) ਰਾਹੀਂ AI ਸਿਸਟਮਾਂ ਲਈ ਅਰਧ-ਸਥਾਈ ਅਤੇ ਸਥਾਈ "ਮੈਮੋਰੀ" (memory) ਵਜੋਂ ਕੰਮ ਕਰਦੇ ਹਨ।

---

## C8.1 Access Controls on Memory & RAG Indices
## C8.1 ਮੈਮੋਰੀ ਅਤੇ RAG ਇੰਡੈਕਸਾਂ ਉੱਤੇ ਪਹੁੰਚ ਕੰਟਰੋਲ

Fine-grained access controls and query-time scope enforcement must be applied to every vector collection.

ਹਰ ਵੈਕਟਰ ਸੰਗ੍ਰਹਿ ਉੱਤੇ ਬਾਰੀਕ-ਪੱਧਰੀ ਪਹੁੰਚ ਕੰਟਰੋਲ ਅਤੇ ਕਿਊਰੀ-ਸਮੇਂ ਸਕੋਪ ਪਾਬੰਦੀਆਂ ਲਾਗੂ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **8.1.1** | **Verify that** vector identifiers and namespaces enforce uniqueness per tenant and prevent cross-tenant collisions. | 1 |
| **8.1.2** | **Verify that** document metadata tags are immutable after the initial write. | 2 |
| **8.1.3** | **Verify that** retrieval operations enforce scope constraints. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **8.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਵੈਕਟਰ ਪਛਾਣਕਰਤਾ ਅਤੇ ਨੇਮਸਪੇਸ ਪ੍ਰਤੀ ਟੈਨੈਂਟ ਵਿਲੱਖਣਤਾ ਲਾਗੂ ਕਰਦੇ ਹਨ ਅਤੇ ਅੰਤਰ-ਟੈਨੈਂਟ ਟਕਰਾਵਾਂ (collisions) ਨੂੰ ਰੋਕਦੇ ਹਨ। | 1 |
| **8.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਦਸਤਾਵੇਜ਼ ਮੈਟਾਡਾਟਾ ਟੈਗ ਸ਼ੁਰੂਆਤੀ ਲਿਖਤ ਤੋਂ ਬਾਅਦ ਅਪਰਿਵਰਤਨਸ਼ੀਲ[^0x10-C08-immutable] (immutable) ਹਨ। | 2 |
| **8.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪ੍ਰਾਪਤੀ ਕਾਰਵਾਈਆਂ ਸਕੋਪ ਪਾਬੰਦੀਆਂ ਲਾਗੂ ਕਰਦੀਆਂ ਹਨ। | 2 |

---

## C8.2 Embedding Sanitization & Validation
## C8.2 Embedding ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ ਅਤੇ ਪ੍ਰਮਾਣਿਕਤਾ

Content must be pre-screened before vectorization, and memory writes treated as untrusted input, to prevent ingestion of unsafe payloads.

ਗ਼ੈਰ-ਸਲਾਮਤ[^0x10-C08-unsafe] (unsafe) ਪੇਲੋਡਾਂ ਦੇ ਦਾਖ਼ਲੇ ਨੂੰ ਰੋਕਣ ਲਈ, ਵੈਕਟਰਾਈਜ਼ੇਸ਼ਨ (vectorization) ਤੋਂ ਪਹਿਲਾਂ ਸਮੱਗਰੀ ਦੀ ਪਹਿਲਾਂ ਹੀ ਛਾਣਬੀਣ ਕਰਨਾ, ਅਤੇ ਮੈਮੋਰੀ ਵਿੱਚ ਲਿਖੀ ਜਾਣ ਵਾਲੀ ਹਰ ਚੀਜ਼ ਨੂੰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟ ਮੰਨਣਾ, ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **8.2.1** | **Verify that** sensitive fields are detected before embedding and are masked, tokenized, or dropped. | 1 |
| **8.2.2** | **Verify that** vectors that fall outside normal clustering patterns are flagged and quarantined before entering production indices. | 2 |
| **8.2.3** | **Verify that** agent outputs and tool outputs are not automatically written to trusted agent memory without explicit source validation. | 2 |
| **8.2.4** | **Verify that** content crafted to manipulate retrieval results is detected and rejected or quarantined before vectorization. | 3 |
| **8.2.5** | **Verify that** new content written to memory is checked for contradictions with what is already stored and that conflicts trigger alerts. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **8.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸੰਵੇਦਨਸ਼ੀਲ ਖੇਤਰਾਂ ਦਾ embedding ਤੋਂ ਪਹਿਲਾਂ ਪਤਾ ਲਗਾਇਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਮਾਸਕ, ਟੋਕਨਾਈਜ਼, ਜਾਂ ਹਟਾ ਦਿੱਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **8.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਿਹੜੇ ਵੈਕਟਰ ਸਧਾਰਨ ਕਲੱਸਟਰਿੰਗ[^0x10-C08-clustering] (clustering) ਪੈਟਰਨਾਂ ਤੋਂ ਬਾਹਰ ਪੈਂਦੇ ਹਨ, ਉਹਨਾਂ ਨੂੰ ਉਤਪਾਦਨ ਇੰਡੈਕਸਾਂ ਵਿੱਚ ਦਾਖ਼ਲ ਹੋਣ ਤੋਂ ਪਹਿਲਾਂ ਨਿਸ਼ਾਨਬੱਧ ਅਤੇ ਕੁਆਰੰਟੀਨ[^0x10-C08-quarantine] (quarantine) ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **8.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ ਆਊਟਪੁੱਟ ਅਤੇ ਟੂਲ ਆਊਟਪੁੱਟ ਸਪਸ਼ਟ ਸਰੋਤ ਪ੍ਰਮਾਣਿਕਤਾ ਤੋਂ ਬਿਨਾਂ ਆਪਣੇ ਆਪ ਭਰੋਸੇਯੋਗ ਏਜੰਟ ਮੈਮੋਰੀ ਵਿੱਚ ਨਹੀਂ ਲਿਖੇ ਜਾਂਦੇ। | 2 |
| **8.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪ੍ਰਾਪਤੀ ਨਤੀਜਿਆਂ ਨਾਲ ਹੇਰਾਫੇਰੀ ਕਰਨ ਲਈ ਘੜੀ ਗਈ ਸਮੱਗਰੀ ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਉਸ ਨੂੰ ਵੈਕਟਰਾਈਜ਼ੇਸ਼ਨ[^0x10-C08-vectorization] ਤੋਂ ਪਹਿਲਾਂ ਰੱਦ ਜਾਂ ਕੁਆਰੰਟੀਨ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 3 |
| **8.2.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮੈਮੋਰੀ ਵਿੱਚ ਲਿਖੀ ਜਾਣ ਵਾਲੀ ਨਵੀਂ ਸਮੱਗਰੀ ਦੀ ਪਹਿਲਾਂ ਤੋਂ ਸੰਭਾਲੀ ਹੋਈ ਸਮੱਗਰੀ ਨਾਲ ਵਿਰੋਧਾਭਾਸਾਂ ਲਈ ਜਾਂਚ ਕੀਤੀ ਜਾਂਦੀ ਹੈ, ਅਤੇ ਟਕਰਾਅ ਹੋਣ 'ਤੇ ਚੇਤਾਵਨੀਆਂ ਪੈਦਾ ਹੁੰਦੀਆਂ ਹਨ। | 3 |

---

## C8.3 Memory Expiry & Revocation
## C8.3 ਮੈਮੋਰੀ ਦੀ ਮਿਆਦ ਪੁੱਗਣਾ ਅਤੇ ਰੱਦਗੀ

Retention and revocation must be explicit and enforceable for memory and RAG indices.

ਮੈਮੋਰੀ ਅਤੇ RAG ਇੰਡੈਕਸਾਂ ਲਈ ਧਾਰਨ (retention) ਅਤੇ ਰੱਦਗੀ (revocation) ਦਾ ਸਪਸ਼ਟ ਅਤੇ ਲਾਗੂ ਕਰਨਯੋਗ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--: | --- | :---: |
| **8.3.1** | **Verify that** expired vectors are excluded from retrieval results. | 2 |
| **8.3.2** | **Verify that** memory can be reset. | 2 |
| **8.3.3** | **Verify that** quarantined content is retained but excluded from all retrieval results. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--: | --- | :---: |
| **8.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਿਆਦ ਪੁੱਗ ਚੁੱਕੇ ਵੈਕਟਰ ਪ੍ਰਾਪਤੀ ਨਤੀਜਿਆਂ ਵਿੱਚੋਂ ਬਾਹਰ ਰੱਖੇ ਜਾਂਦੇ ਹਨ। | 2 |
| **8.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮੈਮੋਰੀ ਨੂੰ ਰੀਸੈੱਟ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ। | 2 |
| **8.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕੁਆਰੰਟੀਨ ਕੀਤੀ ਸਮੱਗਰੀ ਦਾ ਧਾਰਨ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਪਰ ਉਸ ਨੂੰ ਸਾਰੇ ਪ੍ਰਾਪਤੀ ਨਤੀਜਿਆਂ ਵਿੱਚੋਂ ਬਾਹਰ ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ। | 3 |

---

## References
## ਹਵਾਲੇ

* [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [MITRE ATLAS: RAG Poisoning](https://atlas.mitre.org/techniques/AML.T0070)
* [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)

[^0x10-C08-memory]: **memory** (EN, AI/agent system memory) -> ਮੈਮੋਰੀ — kept as a loan rather than ਯਾਦਦਾਸ਼ਤ (human recollection) or ਸਿਮ੍ਰਤੀ (a Hindu scriptural category, categorically excluded), since both native candidates either anthropomorphise a vector index or carry devotional weight; also matches the hardware-memory loan already used in this standard's infrastructure chapter, letting one word serve one concept across chapters. Full discussion: OPEN-QUESTIONS.md Q62.
[^0x10-C08-immutable]: **immutable** (EN) -> ਅਪਰਿਵਰਤਨਸ਼ੀਲ — normalised from an earlier paraphrase ("cannot be changed") to the standing adjective used elsewhere in the corpus for this same requirement, so the term stays searchable and consistent with its own cross-reference in the controls-inventory appendix. Full discussion: OPEN-QUESTIONS.md Q112.
[^0x10-C08-unsafe]: **unsafe** (EN) -> ਗ਼ੈਰ-ਸਲਾਮਤ — normalised from an earlier rendering (ਅਸੁਰੱਖਿਅਤ) that silently re-collapsed the corpus's ਸਲਾਮਤੀ/ਸੁਰੱਖਿਆ (safety/security) split; derived from ਸਲਾਮਤ, not ਸੁਰੱਖਿਅਤ. Full discussion: OPEN-QUESTIONS.md Q66.
[^0x10-C08-clustering]: **clustering** (EN, normal clustering patterns) -> ਕਲੱਸਟਰਿੰਗ — kept as a loan because this is a named unsupervised-learning technique, and a generic native rendering (ਸਮੂਹਬੰਦੀ, "grouping") would let a reader take it as any ad-hoc grouping rather than the specific distribution an anomaly detector compares against. Full discussion: OPEN-QUESTIONS.md Q64.
[^0x10-C08-quarantine]: **quarantine / quarantined** (EN) -> ਕੁਆਰੰਟੀਨ — kept as a loan because quarantine here names a precise third state (content is retained but excluded from retrieval), distinct from both ਅਲੱਗ-ਥਲੱਗ (isolation, already load-bearing for infrastructure elsewhere in the corpus) and outright removal. Full discussion: OPEN-QUESTIONS.md Q63.
[^0x10-C08-vectorization]: **vectorization** (EN) -> ਵੈਕਟਰਾਈਜ਼ੇਸ਼ਨ — built on the already-locked loan ਵੈਕਟਰ, kept as a loan alongside ਕਲੱਸਟਰਿੰਗ as a named machine-learning operation rather than a fresh coinage. Full discussion: OPEN-QUESTIONS.md Q64.
