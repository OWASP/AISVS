# C8 Memory, Embeddings & Vector Database Security

## Control Objective

This chapter addresses securing the embeddings and vector stores that act as semi-persistent and persistent "memory" for AI systems through Retrieval-Augmented Generation (RAG).

---

## C8.1 Access Controls on Memory & RAG Indices

Fine-grained access controls and query-time scope enforcement must be applied to every vector collection.

| # | Description | Level |
| :--: | --- | :---: |
| **8.1.1** | **Verify that** vector identifiers and namespaces enforce uniqueness per tenant and prevent cross-tenant collisions. | 1 |
| **8.1.2** | **Verify that** document metadata tags are immutable after the initial write. | 2 |
| **8.1.3** | **Verify that** retrieval operations enforce scope constraints. | 2 |

---

## C8.2 Embedding Sanitization & Validation

Content must be pre-screened before vectorization, and memory writes treated as untrusted input, to prevent ingestion of unsafe payloads.

| # | Description | Level |
| :--: | --- | :---: |
| **8.2.1** | **Verify that** sensitive fields are detected before embedding and are masked, tokenized, or dropped. | 1 |
| **8.2.2** | **Verify that** vectors that fall outside normal clustering patterns are flagged and quarantined before entering production indices. | 2 |
| **8.2.3** | **Verify that** agent outputs and tool outputs are not automatically written to trusted agent memory without explicit source validation. | 2 |
| **8.2.4** | **Verify that** content crafted to manipulate retrieval results is detected and rejected or quarantined before vectorization. | 3 |
| **8.2.5** | **Verify that** new content written to memory is checked for contradictions with what is already stored and that conflicts trigger alerts. | 3 |

---

## C8.3 Memory Expiry & Revocation

Retention and revocation must be explicit and enforceable for memory and RAG indices.

| # | Description | Level |
| :--: | --- | :---: |
| **8.3.1** | **Verify that** expired vectors are excluded from retrieval results. | 2 |
| **8.3.2** | **Verify that** memory can be reset. | 2 |
| **8.3.3** | **Verify that** quarantined content is retained but excluded from all retrieval results. | 3 |

---

## References

* [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [MITRE ATLAS: RAG Poisoning](https://atlas.mitre.org/techniques/AML.T0070)
* [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
