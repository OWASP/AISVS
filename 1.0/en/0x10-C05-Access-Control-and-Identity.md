# C5 Access Control & Identity for AI Components & Users

## Control Objective

Effective access control for AI systems requires robust identity management, context-aware authorization, and runtime enforcement following zero-trust principles. These controls ensure that humans, services, and autonomous agents only interact with models, data, and computational resources within explicitly granted scopes, with continuous verification and audit capabilities.

---

## C5.1 Identity Management & Authentication

Establish verified identities for all entities interacting with AI systems, with authentication strength appropriate to the risk level.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.1.1** | **Verify that** all human users and service principals authenticate through a centralized identity provider using industry-standard federation protocols (e.g., OIDC, SAML). | 1 | D/V |
| **5.1.2** | **Verify that** high-risk operations (model deployment, weight export, training data access, production configuration changes) require multi-factor authentication or step-up authentication with session re-validation. | 2 | D/V |
| **5.1.3** | **Verify that** AI agents in federated or multi-system deployments authenticate via short-lived, cryptographically signed authentication tokens (e.g., signed JWT assertions) with a maximum lifetime appropriate to the risk level and including cryptographic proof of origin. | 3 | D/V |

---

## C5.2 Authorization & Policy

Implement access controls for all AI resources with explicit permission models and audit trails.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.2.1** | **Verify that** every AI resource (datasets, models, endpoints, vector collections, embedding indices, compute instances) enforces access controls (e.g., RBAC, ABAC) with explicit allow-lists and default-deny policies. | 1 | D/V |
| **5.2.2** | **Verify that** all access control modifications are logged with timestamps, actor identities, resource identifiers, and permission changes. | 1 | V |
| **5.2.3** | **Verify that** access control audit logs are stored immutably and are tamper-evident. | 2 | V |
| **5.2.4** | **Verify that** data classification labels (PII, PHI, proprietary, etc.) automatically propagate to derived resources (embeddings, prompt caches, model outputs). | 2 | D |
| **5.2.5** | **Verify that** unauthorized access attempts and privilege escalation events trigger real-time alerts with contextual metadata. | 2 | D/V |
| **5.2.6** | **Verify that** authorization decisions are externalized to a dedicated policy decision point (e.g., OPA, Cedar, or equivalent). | 3 | D/V |
| **5.2.7** | **Verify that** policies evaluate dynamic attributes at runtime including user role or group, resource classification, request context, tenant isolation, and temporal constraints. | 3 | D/V |
| **5.2.8** | **Verify that** policy cache TTL values are defined based on resource sensitivity, with shorter TTLs for high-sensitivity resources, and that cache invalidation capabilities are available. | 3 | D/V |

---

## C5.3 Query-Time Security Enforcement

Enforce authorization at the data access layer to prevent unauthorized data retrieval through AI queries.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.3.1** | **Verify that** all data store queries (e.g., vector databases, SQL databases, search indices) include mandatory security filters (tenant ID, sensitivity labels, user scope) enforced at the data access layer. | 1 | D/V |
| **5.3.2** | **Verify that** failed authorization evaluations immediately abort queries and return explicit authorization error codes. | 1 | D |
| **5.3.3** | **Verify that** row-level security policies and field-level masking are enabled with policy inheritance for all data stores containing sensitive data used by AI systems. | 2 | D/V |
| **5.3.4** | **Verify that** query retry mechanisms re-evaluate authorization policies to account for dynamic permission changes within active sessions. | 3 | D/V |

---

## C5.4 Output Filtering & Data Loss Prevention

Deploy post-processing controls to prevent unauthorized data exposure in AI-generated content.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.4.1** | **Verify that** post-inference filtering mechanisms scan and redact unauthorized PII, classified information, and proprietary data before delivering content to requestors. | 1 | D/V |
| **5.4.2** | **Verify that** citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 2 | D/V |
| **5.4.3** | **Verify that** output format restrictions (sanitized documents, metadata-stripped images, approved file types) are enforced based on user permission levels and data classifications. | 2 | D |

---

## C5.5 Multi-Tenant Isolation

Ensure logical and cryptographic isolation between tenants in shared AI infrastructure.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.5.1** | **Verify that** network policies implement default-deny rules for cross-tenant communication. | 2 | D |
| **5.5.2** | **Verify that** every API request includes an authenticated tenant identifier that is cryptographically validated against session context and user entitlements. | 1 | D/V |
| **5.5.3** | **Verify that** memory spaces, embedding stores, cache entries (e.g., result caches, embedding caches), and temporary files are namespace-segregated per tenant with secure purging on tenant deletion or session termination. | 2 | D/V |
| **5.5.4** | **Verify that** encryption keys are unique per tenant with customer-managed key (CMK) support and cryptographic isolation between tenant data stores. | 3 | D |
| **5.5.5** | **Verify that** inference-time KV-cache entries are partitioned by authenticated session or tenant identity and that automatic prefix caching does not share cached prefixes across distinct security principals, to prevent timing-based prompt reconstruction attacks. | 2 | D |

---

## C5.6 Autonomous Agent Authorization

Control permissions for AI agents and autonomous systems through scoped capability tokens and continuous authorization.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.6.1** | **Verify that** autonomous agents receive scoped capability tokens that explicitly enumerate permitted actions, accessible resources, time boundaries, and operational constraints. | 1 | D/V |
| **5.6.2** | **Verify that** high-risk capabilities (file system access, code execution, external API calls, financial transactions) are disabled by default and require explicit authorization. | 1 | D/V |
| **5.6.3** | **Verify that** capability tokens are bound to user sessions, include cryptographic integrity protection, and cannot be persisted or reused across sessions. | 2 | D |
| **5.6.4** | **Verify that** agent-initiated actions undergo authorization through a policy decision point that evaluates contextual attributes (e.g., user identity, resource sensitivity, action type, environmental context). | 3 | V |

---

## References

* [NIST SP 800-162: Guide to Attribute Based Access Control (ABAC)](https://csrc.nist.gov/pubs/sp/800/162/final)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
* [NIST IR 8360: Machine Learning for Access Control Policy Verification](https://csrc.nist.gov/pubs/ir/8360/final)
* [I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving (NDSS 2025)](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/)
