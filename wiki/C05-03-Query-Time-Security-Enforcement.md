# C5.3: Query-Time Security Enforcement

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-03-29

## Purpose

Enforce authorization at the data access layer to prevent unauthorized data retrieval through AI queries. Vector similarity search introduces a distinct class of access control challenge: unlike traditional SQL queries with explicit WHERE clauses, vector searches return results based on mathematical similarity, which can cross tenant and classification boundaries if security filters are not mandatory at the data access layer. Row-level security, field-level masking, and re-authorization on retries are all needed to prevent cross-tenant leakage and TOCTOU vulnerabilities in AI query pipelines.

> **Scope note:** Controls in this section govern data-layer query enforcement -- mandatory security filters, fail-closed behavior, row/field masking, and retry re-authorization. Authorization policy definition is in C5.2; output-level filtering is in C5.4; tenant isolation at the infrastructure level is in C5.5.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.3.1** | **Verify that** all data store queries (e.g., vector databases, SQL databases, search indices) include mandatory security filters (tenant ID, sensitivity labels, user scope) enforced at the data access layer. | 1 | Cross-tenant data leakage via RAG retrieval; unauthorized access to sensitive documents through vector similarity search bypassing traditional access controls. | Issue queries without required security filters and confirm they are rejected; test with filters for Tenant A and verify no Tenant B data is returned; inspect query construction in application code. | This is a critical AI-specific concern. Vector similarity search can return semantically similar content across tenant boundaries if filters are not enforced. Most vector databases support metadata filtering but enforcement must be at the application layer. **[2026-03]** Pinecone now supports up to 100K namespaces per index for tenant isolation with queries limited to one namespace at a time. Weaviate enforces tenant isolation via collections/namespaces where embeddings are never co-mingled. Both Pinecone and Weaviate support native document-level filtering and auditable filter enforcement, maturing significantly since 2024. |
| **5.3.2** | **Verify that** failed authorization evaluations immediately abort queries and return explicit authorization error codes. | 1 | Partial query execution leaking data before authorization failure is detected; ambiguous error responses masking authorization failures as system errors. | Submit queries with invalid or insufficient credentials; confirm immediate abort (no partial results returned); verify error codes distinguish authorization failures from other error types. | Fail-closed behavior is essential. Some AI frameworks may return partial results or default outputs on authorization failure rather than explicit errors. Error codes should be specific enough for debugging but not leak information about the authorization policy. |
| **5.3.3** | **Verify that** row-level security policies are enabled for all data stores containing sensitive data used by AI systems. | 2 | Sensitive fields (SSN, medical records) exposed through AI queries despite user lacking access; fine-grained data leakage when coarse access controls allow record-level access but not field-level restriction. | Query sensitive tables with users at different privilege levels; confirm row filtering and field masking are applied; verify masking persists through joins and derived queries; test that AI pipelines respect RLS policies. | PostgreSQL, Snowflake, BigQuery support native RLS. Vector databases generally lack native RLS; enforcement must be layered via application-level filtering. Field-level masking for embeddings is conceptually challenging since the embedding encodes the masked content. **[2026-03]** HoneyBee (SIGMOD 2026, arxiv 2505.01538) introduces a dynamic partitioning framework for RBAC in vector databases that achieves 13.5x lower query latency than row-level security filtering with only 1.24x memory overhead, and 90.4% less memory than per-role dedicated indexes. It formulates RBAC-aware partitioning as a constrained optimization problem, exploiting the hierarchical structure of role-based policies. This is the first academic work to co-design access control with vector index partitioning. |
| **5.3.4** | **Verify that** query retry mechanisms re-evaluate authorization policies to account for dynamic permission changes within active sessions. | 3 | Revoked permissions still honored during retry loops; time-of-check-to-time-of-use (TOCTOU) vulnerabilities where permissions change between initial authorization and retry execution. | Revoke a user's permission mid-session; trigger a query retry and confirm the retry is denied; verify retry logic calls the PDP rather than relying on cached authorization results. | Retry logic in AI pipelines (e.g., LangChain retry chains, embedding batch retries) often caches context including authorization state. Requires explicit re-authorization hooks in retry middleware. |
| **5.3.5** | **Verify that** field-level masking is applied to sensitive fields in all data stores used by AI systems, restricting access to only authorized principals. | 2 | Pending research | Pending research | Pending research |
| **5.3.6** | **Verify that** row-level security and field-level masking policies are inherited by derived or replicated data stores and are not bypassed by replication or ETL processes. | 2 | Pending research | Pending research | Pending research |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
