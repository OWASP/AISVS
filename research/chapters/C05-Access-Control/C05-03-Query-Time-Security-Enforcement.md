# C5.3: Query-Time Authorization

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-05-13 | **Updated:** 2026-05-13

> **What's new (May 2026):** Open WebUI's May 2026 advisories are the clearest current reminder that RAG authorization has to be enforced at the exact vector-query path: CVE-2026-44560 allowed users to extract private file and knowledge-base chunks through code paths that queried the vector store without access checks, while CVE-2026-44554 let attackers overwrite or poison another knowledge base by controlling the target collection name. Earlier 2026 vector-store failures reinforce the same lesson: CVE-2026-24477 exposed AnythingLLM Qdrant API keys through an unauthenticated setup endpoint, and CVE-2026-26190 exposed Milvus management and REST APIs without authentication on TCP 9091. Azure AI Search now documents preview document-level ACL/RBAC and Purview label enforcement at query time, while Databricks' May 2026 Vector Search documentation still says row and column level permissions are not supported and must be implemented with application-level ACL filters.

## Purpose

Enforce authorization at the data access layer to prevent unauthorized data retrieval through AI queries. Vector similarity search introduces a distinct class of access control challenge: unlike traditional SQL queries with explicit WHERE clauses, vector searches return results based on mathematical similarity, which can cross tenant and classification boundaries if security filters are not mandatory at the data access layer. Collection identifiers, file IDs, metadata filters, row-level security, field-level masking, and re-authorization on retries all need explicit tests because RAG pipelines often have several retrieval paths that look equivalent to users but bypass different code.

> **Scope note:** Controls in this section govern data-layer query enforcement -- mandatory security filters, fail-closed behavior, row/field masking, and retry re-authorization. Authorization policy definition is in C5.2; output-level filtering is in C5.4; tenant isolation at the infrastructure level is in C5.6.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.3.1** | **Verify that** AI inference and retrieval pipelines (e.g., RAG queries, embedding lookups) enforce the end-user's authorization context at each retrieval and assembly stage, rather than relying solely on the service account's permissions. | 1 | Unauthorized retrieval through a broadly privileged RAG/vector-search service account; cross-tenant or cross-classification leakage when similarity search returns semantically relevant chunks that the caller cannot access; fail-open retries that re-run retrieval without caller claims; collection-name or file-ID tampering that points retrieval at another user's vector collection; permission stripping during ingestion from SharePoint, Drive, Confluence, ticketing, or data-lake sources. Maps to OWASP LLM08:2025 (Vector and Embedding Weaknesses), MITRE ATLAS AML.T0064 (Gather RAG-Indexed Targets), AML.T0070 (RAG Poisoning), and AML.T0066 (Retrieval Content Crafting). Open WebUI CVE-2026-44560 is a direct query-time example: three RAG source-resolution paths queried vector collections without an authorization check, allowing private file and knowledge-base chunks to be extracted. CVE-2026-44554 shows the adjacent integrity failure, where attacker-controlled collection names could overwrite or poison another knowledge base. CVE-2026-24477 and CVE-2026-26190 show why vector database credentials and management ports also belong in the same threat model: a direct vector-store credential or unauthenticated management API bypasses any application-layer user-context filter. | Trace the caller principal from the front door through retrieval, reranking, prompt assembly, tool calls, retries, and streaming continuations. Build canary documents with identical semantic content but different ACLs, tenants, knowledge-base IDs, file IDs, and classification labels; verify that authorized users retrieve only their permitted canaries and unauthorized users get no retrieved context, not a redacted answer assembled from forbidden chunks. Inspect the actual vector/search request for mandatory filters such as `tenant_id`, `user_id`, `group_ids`, `document_acl`, `classification`, source-system ACL version, and data-source scope; in Qdrant, confirm these are payload/id `must` filters, in Azure AI Search confirm `x-ms-query-source-authorization` or security filters are present, in Amazon Bedrock Knowledge Bases confirm `retrievalConfiguration.vectorSearchConfiguration.filter` is derived from trusted authorization context rather than user text alone, and in OpenSearch confirm DLS/FLS queries are attached to the role used for search. Try revoked-file, stale-share, guessed-collection, bare `collection_name`, non-full-context, full-context, batch, streaming, retry, cache-hit, fallback-retriever, and degraded-index paths. For relationship-based authorization, test OpenFGA `batch-check` or changes-index intersections and SpiceDB `LookupResources`/`CheckPermission` in both pre-filter and post-filter modes. Review logs for principal, policy decision, generated filter, retrieved document IDs, source ACL version, retry count, deny reason, and vector-store credential used. | Native enforcement is uneven. Azure AI Search has preview document-level ACL/RBAC and Purview label enforcement at query time, while many vector stores still rely on application code to inject filters correctly. Amazon Bedrock Knowledge Bases support explicit and implicit metadata filters, but these are retrieval constraints, not a substitute for a trusted PDP unless the filter values come from verified caller entitlements. Databricks Mosaic AI Vector Search supports metadata filtering and endpoint ACLs, but Databricks' May 2026 documentation states that row and column level permissions are not supported and application-level ACLs must be implemented with the filter API; do not treat table RLS as sufficient evidence for vector retrieval. Qdrant, Pinecone, Milvus, OpenSearch, and similar stores provide useful filters or DLS controls, but they do not know whether a missing tenant or ACL filter is a security failure unless the application, gateway, role, or policy enforcement point makes it fail closed. Post-filtering can under-return results, leak result-count side channels, or tempt developers to over-fetch forbidden chunks; pre-filtering is safer for confidentiality but needs an authorization index that stays current with source ACL changes. Relationship engines add latency and consistency tradeoffs, so stale tuple caches and retry logic need explicit tests. Treat vector database credentials and management endpoints as high-impact secrets: the AnythingLLM/Qdrant and Milvus advisories show that direct data-plane or management-plane access can bypass user-context enforcement entirely. |

---

## Verification Notes

- Seed each connected source with matched canary records that share the same semantic content but differ by tenant, user, group, document ACL, classification, purpose, and revocation state. This catches systems that rely on semantic similarity first and only filter after the wrong chunks have already been retrieved.
- Exercise every retrieval entry point, not only the normal chat UI. Include attached files, knowledge-base IDs, direct collection names, agent tools, API batch endpoints, streaming paths, retry handlers, cache reads, full-context modes, non-full-context modes, and fallback retrievers.
- Check both application filters and vector-store enforcement. A passing UI test is not enough if the vector database API key can read the same collection directly, if a management port exposes unauthenticated REST APIs, or if the service account can query every tenant's index.
- Treat generated or implicit filters as relevance helpers unless they are constrained by trusted authorization data. Filters inferred from user prompts can narrow search results, but they should not decide whether a caller is entitled to a source document.

---

## Key References

- [GitHub Advisory GHSA-h36f-rqpx-j5wx: Open WebUI unauthorized RAG vector search access](https://github.com/open-webui/open-webui/security/advisories/GHSA-h36f-rqpx-j5wx)
- [GitLab Advisory Database: CVE-2026-44554 Open WebUI knowledge-base overwrite/RAG poisoning](https://advisories.gitlab.com/pypi/open-webui/CVE-2026-44554/)
- [NVD: CVE-2026-26190 Milvus unauthenticated management and REST APIs](https://nvd.nist.gov/vuln/detail/CVE-2026-26190)
- [NVD: CVE-2026-24477 AnythingLLM Qdrant API key exposure](https://nvd.nist.gov/vuln/detail/CVE-2026-24477)
- [GitHub Advisory GHSA-gm94-qc2p-xcwf: AnythingLLM key leak](https://github.com/Mintplex-Labs/anything-llm/security/advisories/GHSA-gm94-qc2p-xcwf)
- [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
- [MITRE ATLAS data: RAG Poisoning and RAG Databases](https://github.com/mitre-atlas/atlas-data/blob/main/dist/ATLAS.yaml)
- [Azure AI Search document-level access control](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview)
- [Amazon Bedrock Knowledge Bases query filters](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html)
- [OpenFGA: Search with permissions](https://openfga.dev/docs/interacting/search-with-permissions)
- [OpenSearch document-level security](https://docs.opensearch.org/latest/security/access-control/document-level-security/)
- [Pinecone: RAG with access control using SpiceDB](https://www.pinecone.io/learn/rag-access-control/)
- [Qdrant filtering documentation](https://qdrant.tech/documentation/search/filtering/)
- [Amazon Bedrock AgentCore Cedar policy semantics](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html)
- [Databricks Mosaic AI Vector Search](https://docs.databricks.com/aws/en/vector-search/vector-search)
- [Databricks Unity Catalog row filters and column masks](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks)

---

## Related Pages

- **[C08-01 Access Controls for Memory & RAG](../C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)** - Carries the same caller-context and provenance checks into memory stores, retrieval indexes, and vector-store audit trails.
- **[C08-05 Scope Enforcement for User Memory](../C08-Memory-and-Embeddings/C08-05-Scope-Enforcement-User-Memory.md)** - Applies pre-filter, post-filter, cache, and tenant-safe identifier testing to user and agent memory scopes.
- **[C09-07 Intent Verification](../C09-Orchestration-and-Agents/C09-07-Intent-Verification.md)** - Complements retrieval authorization with intent checks before agents use retrieved context for higher-impact actions.
- **[C14-02 Human-in-the-Loop Checkpoints](../C14-Human-Oversight/C14-02-Human-in-the-Loop-Checkpoints.md)** - Links query-time denials and high-risk retrieval results to fail-closed approval gates and review evidence.
- **[C08 Memory, Embeddings & Vector Database Security](../C08-Memory-and-Embeddings/C08-Memory-and-Embeddings.md)** - Provides the broader vector database, RAG poisoning, embedding leakage, and scoped retrieval context behind this control.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
