# C8 Memory, Embeddings & Vector Database Security

## Control Objective

Embeddings and vector stores act as semi-persistent and persistent "memory" for AI systems via Retrieval-Augmented Generation (RAG). This memory can become a high-risk data sink and data exfiltration path. This control family hardens memory pipelines and vector databases so that access is least-privilege, data is sanitized before vectorization, retention is explicit, and systems are resilient to embedding inversion, membership inference, and cross-tenant leakage.

> **Scope note:** General authorization (RBAC/ABAC, scoped tokens, cross-tenant controls), data-at-rest cryptography and key management, generic data-retention and secure-deletion, generic input validation, and session lifecycle management are out of scope and are covered by OWASP ASVS v5 chapters V8, V11, V13, V14, V2, and V7. End-user authorization context propagation through RAG retrieval is covered by AISVS C5.3. Personal-data deletion propagation across AI artifacts (including embeddings) is covered by AISVS C12.2. Per-agent memory namespace isolation in multi-agent systems is covered by AISVS C9.8.3. This chapter focuses on AI-specific concerns: scope enforcement at the vector-engine layer, AI-specific data lineage (embedding model version, ingestion provenance), embedding-pipeline poisoning resistance, retrieval-time anomaly detection, RAG-specific deletion propagation windows, and embedding inversion / membership-inference resistance.

---

## C8.1 Access Controls on Memory & RAG Indices

Enforce fine-grained access controls and query-time scope enforcement for every vector collection.

| # | Description | Level |
| :--: | --- | :---: |
| **8.1.1** | **Verify that** vector insert, update, delete, and query operations are enforced with namespace/collection/document-tag scope controls (e.g., tenant ID, user ID, data classification labels) with default-deny. | 1 |
| **8.1.2** | **Verify that** every ingested document is tagged at write time with source, writer identity (authenticated user or system principal), timestamp, batch ID, and embedding model version. | 2 |
| **8.1.3** | **Verify that** document metadata tags applied at ingestion are immutable after initial write and cannot be modified by subsequent pipeline stages or user operations. | 2 |
| **8.1.4** | **Verify that** RAG pipeline retrieval events log the query issued, the documents or chunks retrieved, similarity scores, the knowledge source, and whether retrieved content passed prompt injection scanning before being incorporated into model context. | 2 |
| **8.1.5** | **Verify that** retrieval anomaly detection identifies embedding density outliers, repeated dominance of specific documents in similarity results, and sudden shifts in retrieval bias distribution that may indicate vector database poisoning. | 3 |

---

## C8.2 Embedding Sanitization & Validation

Pre-screen content before vectorization; treat memory writes as untrusted inputs; prevent ingestion of unsafe payloads.

| # | Description | Level |
| :--: | --- | :---: |
| **8.2.1** | **Verify that** regulated data and sensitive fields are detected prior to embedding and are masked, tokenized, transformed, or dropped based on policy, recognizing that data once embedded cannot be reliably redacted from the resulting index. | 1 |
| **8.2.2** | **Verify that** content intended to poison retrieval (e.g., text crafted to project to attacker-chosen embedding neighborhoods, hidden instructions intended for downstream model context, or steganographic payloads in non-text inputs) is detected and rejected or quarantined before vectorization. | 1 |
| **8.2.3** | **Verify that** vectors that fall outside normal clustering patterns are flagged and quarantined before entering production indices. | 2 |
| **8.2.4** | **Verify that** an agent's own outputs are not automatically written back into its trusted memory without explicit validation (such as content-origin checks or write-authorization controls that verify the content's source before committing writes). | 2 |
| **8.2.5** | **Verify that** tool outputs and orchestration results are not automatically written to agent memory without the same source validation and write-authorization controls applied to the agent's own outputs. | 2 |
| **8.2.6** | **Verify that** new content written to memory is checked for contradictions with what is already stored and that conflicts trigger alerts. | 3 |

---

## C8.3 Memory Expiry, Revocation & Deletion

Retention and revocation must be explicit and enforceable for memory and RAG indices, and deletions must propagate through derivative indices and caches within a measured propagation window.

| # | Description | Level |
| :--: | --- | :---: |
| **8.3.1** | **Verify that** expired vectors are excluded from retrieval results within a measured and monitored propagation window. | 2 |
| **8.3.2** | **Verify that** memory can be reset for security reasons (quarantine, selective purge, full reset) through an operation that is separate and independent from the retention deletion process. | 2 |
| **8.3.3** | **Verify that** quarantined content is retained for investigation but is excluded from all retrieval results while under quarantine. | 2 |

---

## C8.4 Prevent Embedding Inversion & Leakage

Address inversion, membership inference, and attribute inference with explicit threat modeling, mitigations, and regression testing gates.

| # | Description | Level |
| :--: | --- | :---: |
| **8.4.1** | **Verify that** privacy/utility targets for embedding leakage resistance are **defined and measured**, and that changes to embedding models, tokenizers, retrieval settings, or privacy transforms are gated by regression tests against those targets. | 3 |

---

## C8.5 Scope Enforcement for User-Specific Memory

Prevent cross-tenant and cross-user leakage in retrieval and prompt assembly.

| # | Description | Level |
| :--: | --- | :---: |
| **8.5.1** | **Verify that** every retrieval operation enforces scope constraints (tenant/user/classification) **in the vector engine query** and verifies them again **before prompt assembly** (post-filter). | 1 |
| **8.5.2** | **Verify that** vector identifiers, namespaces, and metadata indexing prevent cross-scope collisions and enforce uniqueness per tenant. | 1 |
| **8.5.3** | **Verify that** retrieval results that match similarity criteria but fail scope checks are discarded. | 1 |
| **8.5.4** | **Verify that** multi-tenant tests simulate adversarial retrieval attempts (prompt-based and query-based) and demonstrate zero out-of-scope document inclusion in prompts and outputs. | 2 |

---

## References

* [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [MITRE ATLAS: RAG Poisoning](https://atlas.mitre.org/techniques/AML.T0070)
* [MITRE ATLAS: False RAG Entry Injection](https://atlas.mitre.org/techniques/AML.T0071)
* [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
* [MITRE ATLAS: Invert AI Model](https://atlas.mitre.org/techniques/AML.T0024.001)
