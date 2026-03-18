# C08: Memory, Embeddings & Vector Database Security

> **Source:** [`1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
> **Requirements:** 25 | **Sections:** 5

## Control Objective

Embeddings and vector stores act as semi-persistent and persistent 'memory' for AI systems via RAG. This memory can become a high-risk data sink and data exfiltration path. This control family hardens memory pipelines and vector databases.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C8.1 | Access Controls on Memory & RAG Indices | 6 | 8.1.1–8.1.6 |
| C8.2 | Embedding Sanitization & Validation | 5 | 8.2.1–8.2.5 |
| C8.3 | Memory Expiry, Revocation & Deletion | 6 | 8.3.1–8.3.6 |
| C8.4 | Prevent Embedding Inversion & Leakage | 2 | 8.4.1–8.4.2 |
| C8.5 | Scope Enforcement for User-Specific Memory | 6 | 8.5.1–8.5.6 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- RAG poisoning — injecting malicious content into knowledge bases retrieved at inference time
- Embedding inversion attacks — reconstructing original text from embedding vectors
- Cross-tenant data leakage through shared vector indices
- Memory persistence attacks — injecting instructions that persist across conversations
- PII accumulation in vector stores without adequate deletion mechanisms

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Vector databases:** Pinecone (with namespaces), Weaviate (with RBAC), Qdrant, Milvus
- **Embedding security:** embedding dimensionality reduction, perturbation-based privacy
- **RAG frameworks:** LlamaIndex, LangChain (with metadata filtering for access control)
- **Data cleanup:** TTL-based expiration, tombstone-based deletion in vector stores

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C8.1 Access Controls on Memory & RAG Indices | _TBD_ | |
| C8.2 Embedding Sanitization & Validation | _TBD_ | |
| C8.3 Memory Expiry, Revocation & Deletion | _TBD_ | |
| C8.4 Prevent Embedding Inversion & Leakage | _TBD_ | |
| C8.5 Scope Enforcement for User-Specific Memory | _TBD_ | |

---

## Open Research Questions

- [ ] How do you enforce RBAC in vector databases that don't natively support it?
- [ ] What's the practical risk of embedding inversion for modern high-dimensional embeddings?
- [ ] How should memory expiry policies differ for conversation memory vs. knowledge base memory?
- [ ] What sanitization is adequate for content entering RAG pipelines?

---

## Related Standards & Cross-References

- [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
- [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [MITRE ATLAS: RAG Poisoning](https://atlas.mitre.org/techniques/AML.T0070)
- [MITRE ATLAS: False RAG Entry Injection](https://atlas.mitre.org/techniques/AML.T0071)
- [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
- [MITRE ATLAS: Invert AI Model](https://atlas.mitre.org/techniques/AML.T0024.001)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

