# C8 Memory, Embeddings & Vector Database Security

## Control Objective

Embeddings and vector stores act as semi-persistent amd persistent "memory" for AI systems via Retrieval-Augmented Generation (RAG). This memory can become a high-risk data sink and data exfiltration path. This control family hardens memory pipelines and vector databases so that access is least-privilege, data is sanitized before vectorization, retention is explicit, and systems are resilient to embedding inversion, membership inference, and cross-tenant leakage.

## C8.1 Access Controls on Memory & RAG Indices

Enforce fine-grained access controls and query-time scope enforcement for every vector collection.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.1.1** | **Verify that** vector insert, update, delete, and query operations are enforced with namespace/collection/document-tag scope controls (e.g., tenant ID, user ID, data classification labels) with default-deny. | 1 | D/V |
| **8.1.2** | **Verify that** API credentials used for vector operations carry **scoped claims** (e.g., permitted collections, allowed verbs, tenant binding). | 1 | D/V |
| **8.1.3** | **Verify that** cross-scope access attempts (e.g., cross-tenant similarity queries, namespace traversal, tag bypass) are detected and rejected. | 2 | D/V |

## C8.2 Embedding Sanitization & Validation

Pre-screen content before vectorization; treat memory writes as untrusted inputs; prevent ingestion of unsafe payloads.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.2.1** | **Verify that** regulated data and sensitive fields are detected prior to embedding and are masked, tokenized, transformed, or dropped based on policy. | 1 | D/V |
| **8.2.2** | **Verify that** embedding ingestion rejects or quarantines inputs that violate required content constraints (e.g., non-UTF-8, malformed encodings, oversized payloads, invisible ASCII characters, or executable content intended to poison retrieval). | 1 | D/V |

## C8.3 Memory Expiry, Revocation & Deletion

Retention must be explicit and enforceable; deletions must propagate to derived indices and caches.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.3.1** | **Verify that** every stored vector and its metadata carry an explicit retention label or TTL. | 1 | D/V |
| **8.3.2** | **Verify that** deletion requests purge vectors, metadata, cache copies, and derivative indices within an organization-defined maximum time. | 1 | D/V |
| **8.3.3** | **Verify that** deleted or expired vectors are unrecoverable by normal application paths, and that storage-layer deletion is enforced via cryptographic erasure (key destruction) or equivalent secure deletion controls. | 2 | D |
| **8.3.4** | **Verify that** expired vectors are excluded from retrieval results within a measured and monitored propagation windows. | 3 | D/V |

## C8.4 Prevent Embedding Inversion & Leakage

Address inversion, membership inference, and attribute inference with explicit threat modeling, mitigations, and regression testing gates.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.4.1** | **Verify that** sensitive vector collections are protected against direct read access by infrastructure administrators via technical controls such as application-layer encryption, envelope encryption with strict KMS policies, or equivalent compensating controls. | 2 | D/V |
| **8.4.2** | **Verify that** privacy/utility targets for embedding leakage resistance are **defined and measured**, and that changes to embedding models, tokenizers, retrieval settings, or privacy transforms are gated by regression tests against those targets. | 3 | D/V |

## C8.5 Scope Enforcement for User-Specific Memory

Prevent cross-tenant and cross-user leakage in retrieval and prompt assembly.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.5.1** | **Verify that** every retrieval operation enforces scope constraints (tenant/user/classification) **in the vector engine query** and verifies them again **before prompt assembly** (post-filter). | 1 | D/V |
| **8.5.2** | **Verify that** vector identifiers, namespaces, and metadata indexing prevent cross-scope collisions and enforce uniqueness per tenant. | 1 | D |
| **8.5.3** | **Verify that** retrieval results that match similarity criteria but fail scope checks are discarded. | 2 | D/V |
| **8.5.4** | **Verify that** multi-tenant tests simulate adversarial retrieval attempts (prompt-based and query-based) and demonstrate zero out-of-scope document inclusion in prompts and outputs. | 2 | V |
| **8.5.5** | **Verify that** encryption keys and access policies are segregated per tenant for memory/vector storage, providing cryptographic isolation in shared infrastructure. | 3 | D/V |

## References (recommended additions)

* OWASP Foundation. **OWASP Top 10 for Large Language Model Applications (LLM) 2025**. https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf
