# C5.3: Query-Time Authorization

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-05-02 | **Updated:** 2026-05-02

> **What's new (May 2026):** CVE-2026-24477 exposed Qdrant API keys through AnythingLLM's unauthenticated `/api/setup-complete` endpoint (CVSS 8.7, fixed in 1.10.0), showing how a leaked data-plane credential can bypass any downstream query-time filter. Azure AI Search now documents preview document-level access control that preserves ACL/RBAC metadata and evaluates caller tokens at query time. Amazon Bedrock AgentCore Policy reached GA on 2026-03-03 with Cedar-based gateway enforcement outside agent code. Databricks Mosaic AI Vector Search supports metadata filters and endpoint ACLs, but Unity Catalog row filters and column masks still cannot be applied to source tables used for vector search indexes, so teams must test vector-index authorization separately instead of assuming table RLS carries over.

## Purpose

Enforce authorization at the data access layer to prevent unauthorized data retrieval through AI queries. Vector similarity search introduces a distinct class of access control challenge: unlike traditional SQL queries with explicit WHERE clauses, vector searches return results based on mathematical similarity, which can cross tenant and classification boundaries if security filters are not mandatory at the data access layer. Row-level security, field-level masking, and re-authorization on retries are all needed to prevent cross-tenant leakage and TOCTOU vulnerabilities in AI query pipelines.

> **Scope note:** Controls in this section govern data-layer query enforcement -- mandatory security filters, fail-closed behavior, row/field masking, and retry re-authorization. Authorization policy definition is in C5.2; output-level filtering is in C5.4; tenant isolation at the infrastructure level is in C5.6.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.3.1** | **Verify that** AI inference and retrieval pipelines (e.g., RAG queries, embedding lookups) enforce the end-user's authorization context at each retrieval and assembly stage, rather than relying solely on the service account's permissions. | 1 | Unauthorized retrieval through a broadly privileged RAG/vector-search service account; cross-tenant or cross-classification leakage when similarity search returns semantically relevant chunks that the caller cannot access; fail-open retries that re-run retrieval without caller claims; permission stripping during ingestion from SharePoint, Drive, Confluence, ticketing, or data-lake sources. Maps to OWASP LLM08:2025 (Vector and Embedding Weaknesses), MITRE ATLAS AML.T0085.000 (RAG Databases), AML.T0070 (RAG Poisoning), and AML.T0093 (Prompt Infiltration via Public-Facing Application). The 2026 AnythingLLM/Qdrant key leak (CVE-2026-24477) is a practical example: once the vector database credential is exposed, an attacker can read or modify RAG data directly, outside the application authorization path. | Trace the caller principal from the front door through retrieval, reranking, prompt assembly, tool calls, retries, and streaming continuations. Build canary documents with identical semantic content but different ACLs, tenants, and classification labels; verify that authorized users retrieve only their permitted canaries and unauthorized users get no retrieved context, not a redacted answer assembled from forbidden chunks. Inspect the actual vector/search request for mandatory filters such as `tenant_id`, `user_id`, `group_ids`, `document_acl`, `classification`, and data-source scope; in Qdrant, confirm these are payload/id `must` filters, and in Azure AI Search confirm `x-ms-query-source-authorization` or security filters are present. For relationship-based authorization, test OpenFGA `list-objects`/batch-check or SpiceDB `LookupResources`/`CheckPermission` paths in both pre-filter and post-filter modes. For Cedar/AgentCore-style deployments, verify default-deny and forbid-overrides-permit semantics before retrieval or tool invocation. Review logs for principal, policy decision, generated filter, retrieved document IDs, retry count, and deny reason, then repeat tests during timeout, cache hit, fallback retriever, and degraded-index conditions. | Native enforcement is uneven. Azure AI Search has preview document-level ACL/RBAC and Purview label enforcement at query time, while many vector stores still rely on application code to inject filters correctly. Databricks Mosaic AI Vector Search supports metadata filtering and endpoint ACLs, but Databricks documentation states that tables with Unity Catalog row filters or column masks cannot be used to create vector search indexes; do not treat table RLS as sufficient evidence for vector retrieval. Qdrant, Pinecone, and similar stores provide expressive filters, but they do not know whether a missing filter is a security failure unless the application or gateway makes it fail closed. Post-filtering can under-return results, leak result-count side channels, or tempt developers to over-fetch forbidden chunks; pre-filtering is safer for confidentiality but needs an authorization index that stays current with source ACL changes. Relationship engines add latency and consistency tradeoffs, so stale tuple caches and retry logic need explicit tests. Treat vector database credentials as high-impact secrets: the AnythingLLM/Qdrant advisory shows that a single exposed key can bypass user-context enforcement entirely. |

---

## Key References

- [NVD: CVE-2026-24477 AnythingLLM Qdrant API key exposure](https://nvd.nist.gov/vuln/detail/CVE-2026-24477)
- [GitHub Advisory GHSA-gm94-qc2p-xcwf: AnythingLLM key leak](https://github.com/Mintplex-Labs/anything-llm/security/advisories/GHSA-gm94-qc2p-xcwf)
- [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
- [MITRE ATLAS data: RAG Poisoning and RAG Databases](https://github.com/mitre-atlas/atlas-data/blob/main/dist/ATLAS.yaml)
- [Azure AI Search document-level access control](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview)
- [OpenFGA: Search with permissions](https://openfga.dev/docs/interacting/search-with-permissions)
- [Pinecone: RAG with access control using SpiceDB](https://www.pinecone.io/learn/rag-access-control/)
- [Qdrant filtering documentation](https://qdrant.tech/documentation/search/filtering/)
- [Amazon Bedrock AgentCore Cedar policy semantics](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-understanding-cedar.html)
- [Databricks Mosaic AI Vector Search](https://docs.databricks.com/aws/en/vector-search/vector-search)
- [Databricks Unity Catalog row filters and column masks](https://docs.databricks.com/gcp/en/data-governance/unity-catalog/filters-and-masks)

---

## Related Pages

- **[C08-01 Access Controls for Memory & RAG](../C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md)** - Covers the vector-store namespace, provenance, retrieval logging, and anomaly-detection controls that query-time authorization depends on.
- **[C08-05 Scope Enforcement for User Memory](../C08-Memory-and-Embeddings/C08-05-Scope-Enforcement-User-Memory.md)** - Extends the same pre-filter and post-filter authorization patterns to user memory and multi-agent memory scopes.
- **[C08 Memory, Embeddings & Vector Database Security](../C08-Memory-and-Embeddings/C08-Memory-and-Embeddings.md)** - Provides the broader memory and vector database security context for ACL-aware retrieval pipelines.
- **[C05-02 Authorization Policy](C05-02-Authorization-Policy.md)** - Defines the policy, classification, and label-propagation inputs that C5.3 must enforce during retrieval.
- **[C05 Access Control (Hub)](C05-Access-Control.md)** - Places query-time authorization alongside authentication, output filtering, PDP isolation, and multi-tenant isolation controls.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
