# C8 Memory, Embeddings & Vector Database Security

## Control Objective

Embeddings and vector stores act as semi-persistent and persistent "memory" for AI systems via Retrieval-Augmented Generation (RAG). This memory can become a high-risk data sink and data exfiltration path. This control family hardens memory pipelines and vector databases so that access is least-privilege, data is sanitized before vectorization, retention is explicit, and systems are resilient to embedding inversion, membership inference, and cross-tenant leakage.

## C8.1 Access Controls on Memory & RAG Indices

Enforce fine-grained access controls and query-time scope enforcement for every vector collection.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.1.1** | **Verify that** vector insert, update, delete, and query operations are enforced with namespace/collection/document-tag scope controls (e.g., tenant ID, user ID, data classification labels) with default-deny. | 1 | D/V |
| **8.1.2** | **Verify that** API credentials used for vector operations carry **scoped claims** (e.g., permitted collections, allowed verbs, tenant binding). | 1 | D/V |
| **8.1.3** | **Verify that** cross-scope access attempts (e.g., cross-tenant similarity queries, namespace traversal, tag bypass) are detected and rejected. | 2 | D/V |
| **8.1.4** | **Verify that** every ingested document is tagged at write time with source, writer identity (authenticated user or system principal), timestamp, batch ID, and embedding model version, and that these tags are immutable after initial write. | 2 | D/V |

## C8.2 Embedding Sanitization & Validation

Pre-screen content before vectorization; treat memory writes as untrusted inputs; prevent ingestion of unsafe payloads.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.2.1** | **Verify that** regulated data and sensitive fields are detected prior to embedding and are masked, tokenized, transformed, or dropped based on policy. | 1 | D/V |
| **8.2.2** | **Verify that** embedding ingestion rejects or quarantines inputs that violate required content constraints (e.g., non-UTF-8, malformed encodings, oversized payloads, invisible Unicode characters, or executable content intended to poison retrieval). | 1 | D/V |
| **8.2.3** | **Verify that** vectors that fall outside normal clustering patterns are flagged and quarantined before entering production indices. | 2 | D/V |
| **8.2.4** | **Verify that** an agent's own outputs are not automatically written back into its trusted memory without explicit validation (such as content-origin checks or write-authorization controls that verify the content's source before committing writes). | 2 | D/V |
| **8.2.5** | **Verify that** new content written to memory is checked for contradictions with what is already stored and that conflicts trigger alerts. | 3 | D/V |

## C8.3 Memory Expiry, Revocation & Deletion

Retention must be explicit and enforceable; deletions must propagate to derived indices and caches.

| # | Description | Level | Role |
| :--: | --- | :---: | :--: |
| **8.3.1** | **Verify that** retention times are applied to every stored vector and related metadata across memory storage. | 1 | D/V |
| **8.3.2** | **Verify that** only information required for the system's defined function is persisted in memory (such as user preferences and conversation decisions, not credentials or full conversation transcripts), and that context not needed beyond the current session is discarded at session end. | 1 | D/V |
| **8.3.3** | **Verify that** deletion requests purge vectors, metadata, cache copies, and derivative indices within an organization-defined maximum time. | 1 | D/V |
| **8.3.4** | **Verify that** deleted or expired vectors are removed reliably and are unrecoverable. | 2 | D |
| **8.3.5** | **Verify that** expired vectors are excluded from retrieval results within a measured and monitored propagation window. | 2 | D/V |
| **8.3.6** | **Verify that** memory can be reset for security reasons (quarantine, selective purge, full reset) separately from retention deletion, and that quarantined content is kept for investigation but excluded from retrieval. | 2 | D/V |

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
| **8.5.3** | **Verify that** retrieval results that match similarity criteria but fail scope checks are discarded. | 1 | D/V |
| **8.5.4** | **Verify that** multi-tenant tests simulate adversarial retrieval attempts (prompt-based and query-based) and demonstrate zero out-of-scope document inclusion in prompts and outputs. | 2 | V |
| **8.5.5** | **Verify that** in multi-agent systems, each agent's memory namespace is isolated and enforced through access control, not just organizational naming conventions. | 2 | D/V |
| **8.5.6** | **Verify that** encryption keys and access policies are segregated per tenant for memory/vector storage, providing cryptographic isolation in shared infrastructure. | 3 | D/V |

## References

* [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
* [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [MITRE ATLAS : RAG Poisoning](https://atlas.mitre.org/techniques/AML.T0070)
* [MITRE ATLAS : False RAG Entry Injection](https://atlas.mitre.org/techniques/AML.T0071)
* [MITRE ATLAS : Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
* [MITRE ATLAS : Invert AI Model](https://atlas.mitre.org/techniques/AML.T0024.001)
