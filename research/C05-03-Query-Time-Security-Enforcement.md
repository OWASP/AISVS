# C5.3: Query-Time Authorization

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-04-16 | **Updated:** 2026-04-16

> **What's new (April 2026):** CVE-2026-24477 exposed Qdrant API keys via AnythingLLM's `/api/setup-complete` endpoint (CVSS 8.7, fixed in 1.10.0) — a reminder that application-layer leakage of data-plane credentials defeats any query-time filter downstream. Cedar type-aware partial evaluation ("authorization before retrieval") emerged as a concrete pattern for compiling policy residuals into vector DB query filters. Amazon Bedrock AgentCore Policy went GA in March 2026 with Cedar-based per-tool-call evaluation. Databricks Mosaic AI Vector Search confirmed it still does not support Unity Catalog row filters or column masks on indexed tables — filter-API-based application-layer ACLs remain the only path.

## Purpose

Enforce authorization at the data access layer to prevent unauthorized data retrieval through AI queries. Vector similarity search introduces a distinct class of access control challenge: unlike traditional SQL queries with explicit WHERE clauses, vector searches return results based on mathematical similarity, which can cross tenant and classification boundaries if security filters are not mandatory at the data access layer. Row-level security, field-level masking, and re-authorization on retries are all needed to prevent cross-tenant leakage and TOCTOU vulnerabilities in AI query pipelines.

> **Scope note:** Controls in this section govern data-layer query enforcement -- mandatory security filters, fail-closed behavior, row/field masking, and retry re-authorization. Authorization policy definition is in C5.2; output-level filtering is in C5.4; tenant isolation at the infrastructure level is in C5.6.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.3.1** | **Verify that** AI inference and retrieval pipelines (e.g., RAG queries, embedding lookups) enforce the end-user's authorization context at each retrieval and assembly stage, rather than relying solely on the service account's permissions. | 1 | Pending research | Pending research | Pending research |

---

## Related Pages

- **[C08-01 Access Controls for Memory & RAG](C08-01-Access-Controls-Memory-RAG.md)** — RBAC, namespace isolation, and retrieval logging in vector databases — the memory-layer complement to the data-access-layer filters enforced here.
- **[C08-05 Scope Enforcement for User Memory](C08-05-Scope-Enforcement-User-Memory.md)** — Pre-filter and post-filter scope enforcement and ID-collision prevention for memory retrieval — the memory-scope counterpart to the query-time filters required by 5.3.1 and 5.3.5.
- **[C09-06 Authorization & Delegation](C09-06-Authorization-and-Delegation.md)** — Scoped capability tokens and per-action policy evaluation for agents — relevant because agentic RAG queries need the same retry re-authorization and fail-closed behavior covered in 5.3.1.
- **[C05 Access Control (Hub)](C05-Access-Control.md)** — Parent chapter covering identity management, authorization policy, DLP, multi-tenant isolation, and autonomous agent authorization alongside query-time enforcement.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
