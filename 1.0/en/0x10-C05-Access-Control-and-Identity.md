# C5 Access Control & Identity for AI Components & Users

## Control Objective

Effective access control for AI systems requires robust identity management, context-aware authorization, and runtime enforcement following zero-trust principles. These controls ensure that humans, services, and autonomous agents only interact with models, data, and computational resources within explicitly granted scopes, with continuous verification and audit capabilities.

---

## C5.1 Identity Management & Authentication

Establish cryptographically-backed identities for all entities with multi-factor authentication.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.1.1** | **Verify that** all human users and service principals authenticate through a centralized enterprise identity provider (IdP) using OIDC and/or SAML protocols. | 1 | D/V |
| **5.1.2** | **Verify that** high-risk operations (model deployment, weight export, training data access, production configuration changes) require multi-factor authentication or step-up authentication with session re-validation. | 1 | D/V |
| **5.1.3** | **Verify that** federated AI agents authenticate via signed JWT assertions that have a maximum lifetime of 24 hours and include cryptographic proof of origin. | 3 | D/V |

---

## C5.2 Authorization & Policy

Implement access controls for all AI resources with explicit permission models and audit trails.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.2.1** | **Verify that** every AI resource (datasets, models, endpoints, vector collections, embedding indices, compute instances) enforces role-based access controls with explicit allow-lists and default-deny policies. | 1 | D/V |
| **5.2.2** | **Verify that** all access control modifications are logged immutably with timestamps, actor identities, resource identifiers, and permission changes. | 1 | V |
| **5.2.3** | **Verify that** data classification labels (PII, PHI, proprietary, etc) automatically propagate to derived resources (embeddings, prompt caches, model outputs). | 2 | D |
| **5.2.4** | **Verify that** unauthorized access attempts and privilege escalation events trigger real-time alerts with contextual metadata. | 2 | D/V |
| **5.2.5** | **Verify that** authorization decisions are externalized to a dedicated policy engine (OPA, Cedar, or equivalent). | 1 | D/V |
| **5.2.6** | **Verify that** policies evaluate dynamic attributes at runtime including user role or group, resource classification, request context, tenant isolation, and temporal constraints. | 1 | D/V |
| **5.2.7** | **Verify that** policy cache time-to-live (TTL) values do not exceed 5 minutes for high-sensitivity resources and 1 hour for standard resources with cache invalidation capabilities. | 3 | D/V |

---

## C5.3 Query-Time Security Enforcement

Implement database-layer security controls with mandatory filtering and row-level security policies.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.3.1** | **Verify that** all vector database and SQL queries include mandatory security filters (tenant ID, sensitivity labels, user scope) enforced at the database engine level. | 1 | D/V |
| **5.3.2** | **Verify that** row-level security policies and field-level masking are enabled with policy inheritance for all vector databases, search indices, and training datasets. | 1 | D/V |
| **5.3.3** | **Verify that** failed authorization evaluations will immediately abort queries and return explicit authorization error codes. | 2 | D |
| **5.3.4** | **Verify that** query retry mechanisms re-evaluate authorization policies to account for dynamic permission changes within active user sessions. | 3 | D/V |

---

## C5.4 Output Filtering & Data Loss Prevention

Deploy post-processing controls to prevent unauthorized data exposure in AI-generated content.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.4.1** | **Verify that** post-inference filtering mechanisms scan and redact unauthorized PII, classified information, and proprietary data before delivering content to requestors. | 1 | D/V |
| **5.4.2** | **Verify that** citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 1 | D/V |
| **5.4.3** | **Verify that** output format restrictions (sanitized PDFs, metadata-stripped images, approved file types) are enforced based on user permission levels and data classifications. | 2 | D |

---

## C5.5 Multi-Tenant Isolation

Ensure cryptographic and logical isolation between tenants in shared AI infrastructure.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.5.1** | **Verify that** memory spaces, embedding stores, cache entries, and temporary files are namespace-segregated per tenant with secure purging on tenant deletion or session termination. | 1 | D/V |
| **5.5.2** | **Verify that** every API request includes an authenticated tenant identifier that is cryptographically validated against session context and user entitlements. | 1 | D/V |
| **5.5.3** | **Verify that** network policies implement default-deny rules for cross-tenant communication within service meshes and container orchestration platforms. | 2 | D |
| **5.5.4** | **Verify that** encryption keys are unique per tenant with customer-managed key (CMK) support and cryptographic isolation between tenant data stores. | 3 | D |

---

## C5.6 Autonomous Agent Authorization

Control permissions for AI agents and autonomous systems through scoped capability tokens and continuous authorization.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **5.6.1** | **Verify that** autonomous agents receive scoped capability tokens that explicitly enumerate permitted actions, accessible resources, time boundaries, and operational constraints. | 1 | D/V |
| **5.6.2** | **Verify that** high-risk capabilities (file system access, code execution, external API calls, financial transactions) are disabled by default and require explicit authorization. | 1 | D/V |
| **5.6.3** | **Verify that** capability tokens are bound to user sessions, include cryptographic integrity protection, and ensure that they cannot be persisted or reused in offline scenarios. | 2 | D |
| **5.6.4** | **Verify that** agent-initiated actions undergo authorization through an ABAC policy engine. | 2 | V |

---

## References

* [NIST SP 800-162: Guide to Attribute Based Access Control (ABAC)](https://csrc.nist.gov/pubs/sp/800/162/final)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
* [NIST IR 8360: Machine Learning for Access Control Policy Verification](https://csrc.nist.gov/pubs/ir/8360/final)
