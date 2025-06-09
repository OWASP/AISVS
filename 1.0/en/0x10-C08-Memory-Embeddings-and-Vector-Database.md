# C8 Memory, Embeddings & Vector Database Security

## Control Objective

Embeddings and vector stores act as the "live memory" of contemporary AI systems, continuously accepting user-supplied data and surfacing it back into model contexts via Retrieval-Augmented Generation (RAG). If left ungoverned, this memory can leak PII, violate consent, or be inverted to reconstruct the original text. The objective of this control family is to harden memory pipelines and vector databases so that access is least-privilege, embeddings are privacy-preserving, stored vectors expire or can be revoked on demand, and per-user memory never contaminates another user's prompts or completions.

---

## C8.1 Access Controls on Memory & RAG Indices

Enforce fine-grained access controls on every vector collection.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **8.1.1** | **Verify that** row/namespace-level access control rules restrict insert, delete, and query operations per tenant, collection, or document tag. | 1 | D/V |
| **8.1.2** | **Verify that** API keys or JWTs carry scoped claims (e.g., collection IDs, action verbs) and are rotated at least quarterly. | 1 | D/V |
| **8.1.3** | **Verify that** privilege-escalation attempts (e.g., cross-namespace similarity queries) are detected and logged to a SIEM within 5 minutes. | 2 | D/V |
| **8.1.4** | **Verify that** vector DB audits log subject-identifier, operation, vector ID/namespace, similarity threshold, and result count. | 2 | D/V |
| **8.1.5** | **Verify that** access decisions are tested for bypass flaws whenever engines are upgraded or index-sharding rules change. | 3 | V |

---

## C8.2 Embedding Sanitization & Validation

Pre-screen text for PII, redact or pseudonymise before vectorisation, and optionally post-process embeddings to strip residual signals.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **8.2.1** | **Verify that** PII and regulated data are detected via automated classifiers and masked, tokenised, or dropped pre-embedding. | 1 | D/V |
| **8.2.2** | **Verify that** embedding pipelines reject or quarantine inputs containing executable code or non-UTF-8 artifacts that could poison the index. | 1 | D |
| **8.2.3** | **Verify that** local or metric differential-privacy sanitization is applied to sentence embeddings whose distance to any known PII token falls below a configurable threshold. | 2 | D/V |
| **8.2.4** | **Verify that** sanitization efficacy (e.g., recall of PII redaction, semantic drift) is validated at least semi-annually against benchmark corpora. | 2 | V |
| **8.2.5** | **Verify that** sanitization configs are version-controlled and changes undergo peer review. | 3 | D/V |

---

## C8.3 Memory Expiry, Revocation & Deletion

GDPR "right to be forgotten" and similar laws require timely erasure; vector stores must therefore support TTLs, hard deletes, and tomb-stoning so that revoked vectors cannot be recovered or re-indexed.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **8.3.1** | **Verify that** every vector and metadata record carries a TTL or explicit retention label honoured by automated cleanup jobs. | 1 | D/V |
| **8.3.2** | **Verify that** user-initiated deletion requests purge vectors, metadata, cache copies, and derivative indices within 30 days. | 1 | D/V |
| **8.3.3** | **Verify that** logical deletes are followed by cryptographic shredding of storage blocks if hardware supports it, or by key-vault key destruction. | 2 | D |
| **8.3.4** | **Verify that** expired vectors are excluded from nearest-neighbour search results in < 500 ms after expiration. | 3 | D/V |

---

## C8.4 Prevent Embedding Inversion & Leakage

Recent defences—noise superposition, projection networks, privacy-neuron perturbation, and application-layer encryption—can cut token-level inversion rates below 5%.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **8.4.1** | **Verify that** a formal threat model covering inversion, membership and attribute-inference attacks exists and is reviewed yearly. | 1 | V |
| **8.4.2** | **Verify that** application-layer encryption or searchable encryption shields vectors from direct reads by infrastructure admins or cloud staff. | 2 | D/V |
| **8.4.3** | **Verify that** defence parameters (ε for DP, noise σ, projection rank k) balance privacy ≥ 99 % token protection and utility ≤ 3 % accuracy loss. | 3 | V |
| **8.4.4** | **Verify that** inversion-resilience metrics are part of release gates for model updates, with regression budgets defined. | 3 | D/V |

---

## C8.5 Scope Enforcement for User-Specific Memory

Cross-tenant leakage remains a top RAG risk: improperly filtered similarity queries can surface another customer's private docs.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **8.5.1** | **Verify that** every retrieval query is post-filtered by tenant/user ID before being passed to the LLM prompt. | 1 | D/V |
| **8.5.2** | **Verify that** collection names or namespaced IDs are salted per user or tenant so vectors cannot collide across scopes. | 1 | D |
| **8.5.3** | **Verify that** similarity results above a configurable distance threshold but outside the caller's scope are discarded and trigger security alerts. | 2 | D/V |
| **8.5.4** | **Verify that** multi-tenant stress tests simulate adversarial queries attempting to retrieve out-of-scope documents and demonstrate zero leakage. | 2 | V |
| **8.5.5** | **Verify that** encryption keys are segregated per tenant, ensuring cryptographic isolation even if physical storage is shared. | 3 | D/V |

---

## C8.6 Advanced Memory System Security

Security controls for sophisticated memory architectures including episodic, semantic, and working memory with specific isolation and validation requirements.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **8.6.1** | **Verify that** different memory types (episodic, semantic, working) have isolated security contexts with role-based access controls, separate encryption keys, and documented access patterns for each memory type. | 1 | D/V |
| **8.6.2** | **Verify that** memory consolidation processes include security validation to prevent injection of malicious memories through content sanitization, source verification, and integrity checks before storage. | 2 | D/V |
| **8.6.3** | **Verify that** memory retrieval queries are validated and sanitized to prevent extraction of unauthorized information through query pattern analysis, access control enforcement, and result filtering. | 2 | D/V |
| **8.6.4** | **Verify that** memory forgetting mechanisms securely delete sensitive information with cryptographic erasure guarantees using key deletion, multi-pass overwriting, or hardware-based secure deletion with verification certificates. | 3 | D/V |
| **8.6.5** | **Verify that** memory system integrity is continuously monitored for unauthorized modifications or corruption through checksums, audit logs, and automated alerts when memory content changes outside normal operations. | 3 | D/V |

---

## References

* [Vector database security: Pinecone – IronCore Labs](https://ironcorelabs.com/vectordbs/pinecone-security/)
* [Securing the Backbone of AI: Safeguarding Vector Databases and Embeddings – Privacera](https://privacera.com/blog/securing-the-backbone-of-ai-safeguarding-vector-databases-and-embeddings/)
* [Enhancing Data Security with RBAC of Qdrant Vector Database – AI Advances](https://ai.gopubby.com/enhancing-data-security-with-role-based-access-control-of-qdrant-vector-database-3878769bec83)
* [Mitigating Privacy Risks in LLM Embeddings from Embedding Inversion – arXiv](https://arxiv.org/html/2411.05034v1)
* [DPPN: Detecting and Perturbing Privacy-Sensitive Neurons – OpenReview](https://openreview.net/forum?id=DF5TVzpTW0)
* [Art. 17 GDPR – Right to Erasure](https://gdpr-info.eu/art-17-gdpr/)
* [Sensitive Data in Text Embeddings Is Recoverable – Tonic.ai](https://www.tonic.ai/blog/sensitive-data-in-text-embeddings-is-recoverable)
* [PII Identification and Removal – NVIDIA NeMo Docs](https://docs.nvidia.com/nemo-framework/user-guide/latest/datacuration/personalidentifiableinformationidentificationandremoval.html)
* [De-identifying Sensitive Data – Google Cloud DLP](https://cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data)
* [Remove PII from Conversations Using Sensitive Information Filters – AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html)
* [Think Your RAG Is Secure? Think Again – Medium](https://medium.com/%40vijay.poudel1/think-your-rag-is-secure-think-again-heres-how-to-actually-lock-it-down-c4c30e3864e7)
* [Design a Secure Multitenant RAG Inferencing Solution – Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/secure-multitenant-rag)
* [Best Practices for Multi-Tenancy RAG with Milvus – Milvus Blog](https://milvus.io/blog/build-multi-tenancy-rag-with-milvus-best-practices-part-one.md)
