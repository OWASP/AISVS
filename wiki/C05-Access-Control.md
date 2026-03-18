# C05: Access Control & Identity for AI Components & Users

> **Source:** [`1.0/en/0x10-C05-Access-Control-and-Identity.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
> **Requirements:** 26 | **Sections:** 6

## Control Objective

Effective access control for AI systems requires robust identity management, context-aware authorization, and runtime enforcement following zero-trust principles. These controls ensure that humans, services, and autonomous agents only interact with models, data, and computational resources within explicitly granted scopes, with continuous verification and audit capabilities.

---

## C5.1 Identity Management & Authentication

Establish verified identities for all entities interacting with AI systems, with authentication strength appropriate to the risk level.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 5.1.1 | Verify that all human users and service principals authenticate through a centralized identity provider using industry-standard federation protocols (e.g., OIDC, SAML). | 1 | D/V | Credential sprawl and inconsistent authentication enforcement across AI endpoints; lateral movement via compromised local accounts. | Confirm IdP integration in architecture diagrams; test that direct API access without IdP-issued tokens is rejected; review service principal registrations in the IdP. | Standard practice for web applications; the AI-specific nuance is ensuring model-serving endpoints (e.g., inference APIs, model registries) are behind the same IdP rather than using separate API keys. |
| 5.1.2 | Verify that high-risk operations (model deployment, weight export, training data access, production configuration changes) require multi-factor authentication or step-up authentication with session re-validation. | 2 | D/V | Stolen session tokens used to exfiltrate model weights or poison training data; insider threats performing high-impact changes with passive credentials. | Trigger each high-risk operation and confirm MFA challenge is presented; verify session re-validation timestamps in audit logs; test that expired step-up sessions are denied. | Defining the boundary of "high-risk" is organization-specific. Model weight export and training data access are AI-specific high-value targets not typically covered by general MFA policies. |
| 5.1.3 | Verify that AI agents in federated or multi-system deployments authenticate via short-lived, cryptographically signed authentication tokens (e.g., signed JWT assertions) with a maximum lifetime appropriate to the risk level and including cryptographic proof of origin. | 3 | D/V | Agent impersonation in multi-agent orchestration; token replay attacks enabling unauthorized agent actions; long-lived credentials being exfiltrated from agent memory. | Inspect token lifetimes and signing algorithms; verify token rotation occurs before expiry; test that expired or tampered tokens are rejected; confirm proof-of-origin claims (e.g., SPIFFE IDs) are validated. | Multi-agent identity is an emerging area. SPIFFE/SPIRE provides workload identity but agent-level granularity is still maturing. Token lifetime guidance varies; NIST SP 800-63B suggests risk-proportionate session timeouts. |

---

## C5.2 Authorization & Policy

Implement access controls for all AI resources with explicit permission models and audit trails.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 5.2.1 | Verify that every AI resource (datasets, models, endpoints, vector collections, embedding indices, compute instances) enforces access controls (e.g., RBAC, ABAC) with explicit allow-lists and default-deny policies. | 1 | D/V | Unauthorized access to training data, model weights, or inference endpoints; privilege escalation through permissive default policies. | Attempt access to each resource type with unauthenticated and under-privileged credentials; confirm default-deny by testing access without explicit grants; review ACL configurations for all AI resource types. | Vector databases (Pinecone, Weaviate, Milvus) have varying RBAC maturity. Some require application-layer enforcement rather than native database-level controls. Embedding indices are often overlooked in access control audits. |
| 5.2.2 | Verify that all access control modifications are logged with timestamps, actor identities, resource identifiers, and permission changes. | 1 | V | Undetected privilege escalation; inability to perform forensic analysis after a breach; insider threats modifying permissions without accountability. | Make permission changes and verify log entries contain all required fields; confirm logs capture both successful and failed modification attempts; validate log completeness across all AI resource types. | Standard audit logging practice. The AI-specific concern is ensuring coverage of non-traditional resources like vector store collections, model registry entries, and compute quota assignments. |
| 5.2.3 | Verify that access control audit logs are stored immutably and are tamper-evident. | 2 | V | Log tampering to conceal unauthorized access or data exfiltration; destruction of forensic evidence after compromise. | Attempt to modify or delete existing log entries; verify cryptographic chaining or append-only storage; confirm log integrity verification mechanisms are in place and tested. | Append-only storage (e.g., AWS CloudTrail with S3 Object Lock, immutable Azure Blob) provides tamper-evidence. For on-prem deployments, cryptographic hash chaining or write-once media may be needed. |
| 5.2.4 | Verify that data classification labels (PII, PHI, proprietary, etc.) automatically propagate to derived resources (embeddings, prompt caches, model outputs). | 2 | D | Data classification loss during AI pipelines; sensitive data in embeddings or caches accessed without appropriate controls because labels were dropped during transformation. | Tag a source dataset with a classification label; trace label propagation through embedding generation, prompt caching, and output storage; confirm derived resources inherit the source classification. | This is an AI-specific challenge with limited tooling. Embeddings are mathematical transformations that lose explicit metadata. Label propagation typically requires custom pipeline instrumentation. Microsoft Purview and Google DLP have partial support. |
| 5.2.5 | Verify that unauthorized access attempts and privilege escalation events trigger real-time alerts with contextual metadata. | 2 | D/V | Delayed detection of active attacks; brute-force credential attacks against model endpoints; privilege escalation going unnoticed during active exploitation. | Generate unauthorized access attempts and privilege escalation scenarios; confirm alerts fire within defined SLA; verify alerts include actor identity, target resource, action attempted, and timestamp. | Requires SIEM integration (Splunk, Sentinel, Elastic) with AI platform event sources. Alert fatigue is a risk; tuning thresholds for AI-specific resources (e.g., repeated vector DB queries) is an ongoing challenge. |
| 5.2.6 | Verify that authorization decisions are externalized to a dedicated policy decision point (e.g., OPA, Cedar, or equivalent). | 3 | D/V | Scattered, inconsistent authorization logic embedded across AI microservices; difficulty auditing or updating policies; policy drift between environments. | Confirm a centralized PDP exists; verify that AI service components call the PDP for authorization rather than implementing local checks; test policy changes propagate to all enforcement points. | OPA (Rego), Cedar (AWS), and Casbin are mature options. Externalized policy is best practice but adds latency to inference paths. Caching strategies (see 5.2.8) are needed to offset performance impact. |
| 5.2.7 | Verify that policies evaluate dynamic attributes at runtime including user role or group, resource classification, request context, tenant isolation, and temporal constraints. | 3 | D/V | Static RBAC failing to account for contextual risk (e.g., unusual access times, cross-tenant requests); overly permissive access when context changes after initial grant. | Test access decisions under varying contexts (different times, locations, tenant contexts); confirm that changing a dynamic attribute (e.g., revoking group membership) immediately affects authorization; verify temporal constraint enforcement. | Full ABAC requires rich attribute sources (IdP, CMDB, classification service). NIST SP 800-162 provides the reference framework. Integration complexity increases with the number of attribute sources. |
| 5.2.8 | Verify that policy cache TTL values are defined based on resource sensitivity, with shorter TTLs for high-sensitivity resources, and that cache invalidation capabilities are available. | 3 | D/V | Stale cached permissions allowing access after revocation; delayed enforcement of emergency access revocations during incidents. | Review cache TTL configurations per resource sensitivity tier; test that cache invalidation propagates within defined SLA; verify high-sensitivity resources use TTLs of seconds rather than minutes. | Balances security (short TTL) vs. performance (long TTL). For inference-time authorization, even milliseconds of policy evaluation latency can impact throughput. Event-driven cache invalidation is preferred over TTL-only approaches. |

---

## C5.3 Query-Time Security Enforcement

Enforce authorization at the data access layer to prevent unauthorized data retrieval through AI queries.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 5.3.1 | Verify that all data store queries (e.g., vector databases, SQL databases, search indices) include mandatory security filters (tenant ID, sensitivity labels, user scope) enforced at the data access layer. | 1 | D/V | Cross-tenant data leakage via RAG retrieval; unauthorized access to sensitive documents through vector similarity search bypassing traditional access controls. | Issue queries without required security filters and confirm they are rejected; test with filters for Tenant A and verify no Tenant B data is returned; inspect query construction in application code. | This is a critical AI-specific concern. Vector similarity search can return semantically similar content across tenant boundaries if filters are not enforced. Most vector databases support metadata filtering but enforcement must be at the application layer. |
| 5.3.2 | Verify that failed authorization evaluations immediately abort queries and return explicit authorization error codes. | 1 | D | Partial query execution leaking data before authorization failure is detected; ambiguous error responses masking authorization failures as system errors. | Submit queries with invalid or insufficient credentials; confirm immediate abort (no partial results returned); verify error codes distinguish authorization failures from other error types. | Fail-closed behavior is essential. Some AI frameworks may return partial results or default outputs on authorization failure rather than explicit errors. Error codes should be specific enough for debugging but not leak information about the authorization policy. |
| 5.3.3 | Verify that row-level security policies and field-level masking are enabled with policy inheritance for all data stores containing sensitive data used by AI systems. | 2 | D/V | Sensitive fields (SSN, medical records) exposed through AI queries despite user lacking access; fine-grained data leakage when coarse access controls allow record-level access but not field-level restriction. | Query sensitive tables with users at different privilege levels; confirm row filtering and field masking are applied; verify masking persists through joins and derived queries; test that AI pipelines respect RLS policies. | PostgreSQL, Snowflake, BigQuery support native RLS. Vector databases generally lack native RLS; enforcement must be layered via application-level filtering. Field-level masking for embeddings is conceptually challenging since the embedding encodes the masked content. |
| 5.3.4 | Verify that query retry mechanisms re-evaluate authorization policies to account for dynamic permission changes within active sessions. | 3 | D/V | Revoked permissions still honored during retry loops; time-of-check-to-time-of-use (TOCTOU) vulnerabilities where permissions change between initial authorization and retry execution. | Revoke a user's permission mid-session; trigger a query retry and confirm the retry is denied; verify retry logic calls the PDP rather than relying on cached authorization results. | Retry logic in AI pipelines (e.g., LangChain retry chains, embedding batch retries) often caches context including authorization state. Requires explicit re-authorization hooks in retry middleware. |

---

## C5.4 Output Filtering & Data Loss Prevention

Deploy post-processing controls to prevent unauthorized data exposure in AI-generated content.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 5.4.1 | Verify that post-inference filtering mechanisms scan and redact unauthorized PII, classified information, and proprietary data before delivering content to requestors. | 1 | D/V | Model memorization leaking training data PII in outputs; RAG pipelines surfacing sensitive documents in responses; prompt injection causing the model to output restricted information. | Submit prompts designed to elicit PII (names, SSNs, emails); confirm redaction in outputs; test with known training data snippets; verify redaction covers structured and unstructured PII patterns. | NER-based PII detection (spaCy, Presidio, Google DLP API) provides baseline coverage. False negatives are common with novel PII formats or multilingual content. Balancing redaction aggressiveness with output utility is an ongoing challenge. |
| 5.4.2 | Verify that citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 2 | D/V | RAG systems citing documents the user is not authorized to view; source attribution revealing the existence of classified or restricted documents; indirect information disclosure through citation metadata. | Query the system as a low-privilege user; verify cited sources are within the user's access scope; test with documents at multiple classification levels; confirm unauthorized citations are stripped without breaking response coherence. | Unique to RAG architectures. Requires cross-referencing citation source IDs against the caller's document-level entitlements at output time. Most RAG frameworks (LlamaIndex, LangChain) do not natively enforce citation-level access control. |
| 5.4.3 | Verify that output format restrictions (sanitized documents, metadata-stripped images, approved file types) are enforced based on user permission levels and data classifications. | 2 | D | Data exfiltration through unrestricted output formats (e.g., raw model weights in JSON, unsanitized PDFs with embedded metadata); metadata leakage in generated images (EXIF data, generation parameters). | Request outputs in various formats with different privilege levels; confirm format restrictions are enforced; verify metadata stripping (EXIF, document properties) is applied; test that unapproved file types are rejected. | Multimodal AI systems generate diverse output types (images, audio, documents) each with format-specific metadata risks. EXIF stripping for images, PDF sanitization, and format allow-listing are needed. Tools like ExifTool and Apache Tika can support implementation. |

---

## C5.5 Multi-Tenant Isolation

Ensure logical and cryptographic isolation between tenants in shared AI infrastructure.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 5.5.1 | Verify that network policies implement default-deny rules for cross-tenant communication. | 2 | D | Lateral movement between tenant environments; cross-tenant network-level attacks exploiting shared infrastructure; data exfiltration through unrestricted network paths. | Review Kubernetes NetworkPolicies or cloud security group rules; attempt cross-tenant network connections and confirm they are blocked; verify default-deny is the baseline with explicit allow rules for required communication. | Standard multi-tenant security practice. In AI contexts, shared GPU clusters and model-serving infrastructure often share network segments. Kubernetes NetworkPolicies, Calico, or Cilium can enforce tenant isolation at the network layer. |
| 5.5.2 | Verify that every API request includes an authenticated tenant identifier that is cryptographically validated against session context and user entitlements. | 1 | D/V | Tenant ID spoofing allowing cross-tenant data access; confused deputy attacks where a shared service accesses the wrong tenant's data; IDOR vulnerabilities in multi-tenant AI APIs. | Attempt API calls with mismatched tenant IDs and session tokens; confirm rejection; test tenant ID tampering in request headers; verify tenant ID is derived from authenticated session rather than client-supplied parameters. | Tenant ID must be extracted from the authenticated token (JWT claim, session attribute) rather than accepted as a client-supplied parameter. This prevents trivial tenant spoofing. Shared inference endpoints are particularly vulnerable if tenant context is passed as a query parameter. |
| 5.5.3 | Verify that memory spaces, embedding stores, cache entries, and temporary files are namespace-segregated per tenant with secure purging on tenant deletion or session termination. | 2 | D/V | Cross-tenant data leakage through shared caches, GPU memory, or temporary files; residual tenant data persisting after tenant offboarding; embedding store contamination between tenants. | Verify namespace segregation in embedding stores, caches, and temp directories; trigger tenant deletion and confirm all associated data is purged; check for residual data in GPU memory, swap files, and temporary storage. | AI-specific concern: GPU memory is shared across inference requests and may retain activations from previous tenants. KV-cache in transformer inference, embedding store collections, and prompt caches all need tenant-scoped namespacing. Secure purging of GPU memory is not natively supported by most frameworks. |
| 5.5.4 | Verify that encryption keys are unique per tenant with customer-managed key (CMK) support and cryptographic isolation between tenant data stores. | 3 | D | Compromise of a single encryption key exposing all tenants' data; inability to perform cryptographic tenant offboarding (key destruction); regulatory requirements for customer-controlled encryption. | Verify unique key ARNs/IDs per tenant; confirm CMK integration (AWS KMS, Azure Key Vault, GCP Cloud KMS); test that tenant A's key cannot decrypt tenant B's data; verify key destruction on tenant offboarding removes access to all associated data. | Per-tenant keys add key management complexity but enable cryptographic shredding on tenant offboarding. For AI workloads, this extends to encrypted model artifacts, training data snapshots, and embedding stores. HSM-backed key management is recommended for high-sensitivity deployments. |

---

## C5.6 Autonomous Agent Authorization

Control permissions for AI agents and autonomous systems through scoped capability tokens and continuous authorization.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| 5.6.1 | Verify that autonomous agents receive scoped capability tokens that explicitly enumerate permitted actions, accessible resources, time boundaries, and operational constraints. | 1 | D/V | Overprivileged agents performing unintended actions; prompt injection causing agents to exceed intended scope; agents accumulating permissions across task boundaries. | Inspect token claims for action enumeration, resource scoping, and time boundaries; attempt out-of-scope actions and confirm denial; verify tokens cannot be escalated by the agent itself. | Principle of least privilege applied to autonomous agents. Capability-based security (as in object-capability model) is well-suited. Token format should enumerate positive permissions rather than relying on deny-lists. Frameworks like AutoGPT and CrewAI are beginning to add permission scoping. |
| 5.6.2 | Verify that high-risk capabilities (file system access, code execution, external API calls, financial transactions) are disabled by default and require explicit authorization. | 1 | D/V | Prompt injection or jailbreaking causing agents to execute arbitrary code, access the file system, or make external network calls; agents performing destructive actions without human approval. | Attempt high-risk actions with default agent configuration and confirm denial; verify each high-risk capability requires explicit opt-in; test that enabling one capability does not implicitly enable others. | Critical for agent safety. Default-deny for dangerous capabilities prevents prompt injection from escalating to system compromise. OpenAI function calling, LangChain tool permissions, and Anthropic tool use all support capability restriction but default configurations vary. |
| 5.6.3 | Verify that capability tokens are bound to user sessions, include cryptographic integrity protection, and cannot be persisted or reused across sessions. | 2 | D | Token theft enabling unauthorized agent actions; agents persisting tokens to maintain access beyond the user's session; replay attacks using captured capability tokens. | Verify token-session binding (e.g., session ID in token claims); attempt token reuse after session termination and confirm rejection; test token integrity by modifying claims and verifying rejection; confirm tokens are not written to persistent storage. | Session-bound tokens prevent agents from accumulating long-lived credentials. HMAC or digital signature integrity protection prevents token tampering. Storage restrictions must be enforced at the runtime level since agents with file system access could persist tokens if not prevented. |
| 5.6.4 | Verify that agent-initiated actions undergo authorization through a policy decision point that evaluates contextual attributes (e.g., user identity, resource sensitivity, action type, environmental context). | 3 | V | Agents bypassing authorization by acting autonomously without per-action policy checks; contextual risks (e.g., production vs. staging environment, business hours vs. off-hours) not factored into agent authorization decisions. | Verify each agent action triggers a PDP evaluation; test with varying contextual attributes (environment, time, resource sensitivity) and confirm decisions change appropriately; audit PDP logs for completeness of agent action authorization. | Continuous authorization for agents is an emerging pattern. Unlike human users who authenticate once per session, agents may execute hundreds of actions requiring per-action or per-batch authorization. Performance optimization (batched policy evaluation, pre-computed permission sets) is needed to avoid latency bottlenecks. |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Privilege escalation through prompt injection causing the model to act with elevated permissions
- Cross-tenant data leakage in shared AI infrastructure
- Agent identity spoofing in multi-agent systems
- Confused deputy attacks where AI tools act with the user's credentials beyond intended scope

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Policy engines:** OPA (Open Policy Agent), Cedar (AWS), Casbin
- **Identity:** SPIFFE/SPIRE for workload identity, OAuth 2.0 for user-facing AI apps
- **DLP:** Google DLP API, Microsoft Purview, Presidio, custom regex/NER-based PII filters
- **Multi-tenant isolation:** Kubernetes namespaces, Calico/Cilium network policies, database row-level security
- **Agent authorization:** LangChain tool permissions, OpenAI function calling constraints, capability-based token frameworks

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C5.1 Identity Management & Authentication | High | OIDC/SAML and MFA are mature; agent-specific identity (SPIFFE) is maturing |
| C5.2 Authorization & Policy | Medium-High | OPA/Cedar are production-ready; AI-specific policy patterns are still emerging |
| C5.3 Query-Time Security Enforcement | Medium | SQL RLS is mature; vector database access control is immature and varies by vendor |
| C5.4 Output Filtering & Data Loss Prevention | Medium | PII detection tools exist but false-negative rates remain high for AI-generated content |
| C5.5 Multi-Tenant Isolation | Medium-High | Network and storage isolation is mature; GPU memory isolation and KV-cache segregation are gaps |
| C5.6 Autonomous Agent Authorization | Low-Medium | Capability scoping is emerging in agent frameworks; continuous per-action authorization is nascent |

---

## Open Research Questions

- [ ] How should authorization policies account for the non-deterministic nature of AI outputs?
- [ ] What's the right model for agent identity in multi-agent orchestration?
- [ ] How do you enforce query-time access control in vector databases that lack native RBAC?
- [ ] Should AI systems have their own identity distinct from the calling user?
- [ ] How can GPU memory isolation be enforced between tenants sharing inference hardware?
- [ ] What are effective strategies for propagating data classification labels through embedding transformations?

---

## Related Standards & Cross-References

- [NIST SP 800-162: Guide to ABAC](https://csrc.nist.gov/pubs/sp/800/162/final)
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
- [NIST IR 8360: ML for Access Control Policy Verification](https://csrc.nist.gov/pubs/ir/8360/final)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C3 (Data Governance) | Data classification, sensitivity labels | C5.2.4 label propagation depends on classification defined in C3 |
| C7 (Secure Deployment) | Service identity, workload authentication | C5.1.3 agent tokens relate to deployment-time identity provisioning |
| C9 (Agentic Architecture) | Agent permissions, tool access control | C5.6 agent authorization is complementary to C9 agentic safety controls |
| C14 (Privacy) | PII handling, DLP | C5.4 output filtering overlaps with C14 privacy protection requirements |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
