# C8 Memory, Embeddings & Vector Database Security

## Control Objective

Embeddings and vector stores act as semi-persistent and persistent "memory" for AI systems via Retrieval-Augmented Generation (RAG). This memory can become a high-risk data sink and data exfiltration path. This control family hardens memory pipelines and vector databases so that access is least-privilege, data is sanitized before vectorization, retention is explicit, and systems are resilient to embedding inversion, membership inference, and cross-tenant leakage.

---

## C8.1 Access Controls on Memory & RAG Indices

Enforce fine-grained access controls and query-time scope enforcement for every vector collection.

| # | Description | Level |
| :--: | --- | :---: |
| **8.1.1** | **Verify that** vector insert, update, delete, and query operations are enforced with namespace and collection scope controls with default-deny. | 1 |
| **8.1.2** | **Verify that** every ingested document is tagged at write time with source, writer identity, timestamp, and embedding model version. | 2 |
| **8.1.3** | **Verify that** document metadata tags are immutable after the initial write and cannot be changed by later pipeline stages or user operations. | 2 |
| **8.1.4** | **Verify that** RAG pipeline retrieval events log the query, documents retrieved, similarity scores, and knowledge source. | 2 |
| **8.1.5** | **Verify that** a high-severity alert is generated whenever a canary record is selected by retrieval or passed to the model as context. | 2 |
| **8.1.6** | **Verify that** retrieval anomaly detection identifies embedding density outliers and sudden shifts in retrieval bias distribution that may indicate vector database poisoning. | 3 |

---

## C8.2 Embedding Sanitization & Validation

Pre-screen content before vectorization and treat memory writes as untrusted inputs to prevent ingestion of unsafe payloads.

| # | Description | Level |
| :--: | --- | :---: |
| **8.2.1** | **Verify that** sensitive fields are detected before embedding and are masked, tokenized, or dropped, since data once embedded cannot be reliably redacted. | 1 |
| **8.2.2** | **Verify that** content crafted to manipulate retrieval geometry is detected and rejected or quarantined before vectorization. | 3 |
| **8.2.3** | **Verify that** vectors that fall outside normal clustering patterns are flagged and quarantined before entering production indices. | 2 |
| **8.2.4** | **Verify that** agent outputs and tool outputs are not automatically written to trusted agent memory without explicit source validation. | 2 |
| **8.2.5** | **Verify that** new content written to memory is checked for contradictions with what is already stored and that conflicts trigger alerts. | 3 |

---

## C8.3 Memory Expiry, Revocation & Leakage Prevention

Retention and revocation must be explicit and enforceable for memory and RAG indices, and systems must address embedding inversion and attribute inference risks.

| # | Description | Level |
| :--: | --- | :---: |
| **8.3.1** | **Verify that** expired vectors are excluded from retrieval results within a defined propagation window. | 2 |
| **8.3.2** | **Verify that** memory can be reset for security reasons through an operation independent from the retention deletion process. | 2 |
| **8.3.3** | **Verify that** quarantined content is retained for investigation but excluded from all retrieval results while under quarantine. | 2 |
| **8.3.4** | **Verify that** privacy and utility targets for embedding leakage resistance are defined and measured, and that changes to embedding models or privacy transforms are gated by regression tests against those targets. | 3 |

---

## C8.4 Scope Enforcement for User-Specific Memory

Prevent cross-tenant and cross-user leakage in retrieval and prompt assembly.

| # | Description | Level |
| :--: | --- | :---: |
| **8.4.1** | **Verify that** every retrieval operation enforces scope constraints in the vector engine query and verifies them again before prompt assembly. | 2 |
| **8.4.2** | **Verify that** vector identifiers, namespaces, and metadata indexing prevent cross-scope collisions and enforce uniqueness per tenant. | 1 |
| **8.4.3** | **Verify that** retrieval results that match similarity criteria but fail scope checks are discarded. | 1 |
| **8.4.4** | **Verify that** multi-tenant tests simulate adversarial retrieval attempts and verify that no out-of-scope documents appear in prompts or outputs. | 2 |

---

## References

* [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [MITRE ATLAS: RAG Poisoning](https://atlas.mitre.org/techniques/AML.T0070)
* [MITRE ATLAS: False RAG Entry Injection](https://atlas.mitre.org/techniques/AML.T0071)
* [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
* [MITRE ATLAS: Invert AI Model](https://atlas.mitre.org/techniques/AML.T0024.001)
