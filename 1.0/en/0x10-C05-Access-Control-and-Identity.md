# C5 Access Control & Identity for AI Components & Users

## Control Objective

AI systems introduce access control challenges beyond traditional application security: classification labels must follow data through AI-specific transformations (embeddings, caches, model outputs), multi-tenant inference infrastructure creates novel side channels, and retrieval-augmented pipelines must enforce caller entitlements at every stage. This chapter addresses AI-specific access control and identity concerns, including runtime isolation of the policy decision point from agent execution and authorization-aware output filtering where entitlements vary per caller.

---

## C5.1 Authentication

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.1.1** | **Verify that** high-risk AI operations (model deployment, weight export, training data access, production configuration changes) require step-up authentication with session re-validation. | 2 |
| **5.1.2** | **Verify that** AI agents in federated or multi-system deployments authenticate via short-lived, cryptographically signed authentication tokens (e.g., signed JWT assertions) with a maximum lifetime appropriate to the risk level and including cryptographic proof of origin. | 3 |

---

## C5.2 AI Resource Authorization & Classification

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.2.1** | **Verify that** every AI resource (datasets, models, endpoints, vector collections, embedding indices, compute instances) enforces access controls (e.g., RBAC, ABAC) with explicit allow-lists and default-deny policies. | 1 |
| **5.2.2** | **Verify that** privileged access to model weights, training pipelines, and production AI configuration is provisioned on a just-in-time basis with a defined maximum session duration and automatic expiry, and permanent standing privileged access to these resources is not permitted. | 2 |
| **5.2.3** | **Verify that** a documented data classification taxonomy covering AI-specific data types (embeddings, model weights, prompt templates, RAG context assemblies, fine-tuning datasets, agent tool schemas) is defined, and that AI assets are labeled in accordance with this taxonomy. | 2 |
| **5.2.4** | **Verify that** data classification labels (PII, PHI, proprietary, etc.) automatically propagate to derived resources (embeddings, prompt caches, model outputs). | 3 |

---

## C5.3 Query-Time Authorization

Enforce the caller's authorization context through AI-specific query pipelines (RAG retrieval, embedding lookups, inference chains) so that the AI system does not return data the caller is not entitled to access.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.3.1** | **Verify that** AI inference and retrieval pipelines (e.g., RAG queries, embedding lookups) enforce the end-user's authorization context at each retrieval and assembly stage, rather than relying solely on the service account's permissions. | 1 |

---

## C5.4 Output Entitlement Enforcement

Ensure that AI-generated outputs, including citations and source attributions, respect the caller's data entitlements.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.4.1** | **Verify that** post-inference filtering mechanisms prevent responses from including classified information or proprietary data that the requestor is not authorized to receive. | 1 |
| **5.4.2** | **Verify that** citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 2 |

---

## C5.5 Policy Decision Point Isolation

Ensure that authorization decision infrastructure for AI agents is protected from compromise and manipulation by the agents it governs.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.5.1** | **Verify that** the policy decision point for agent authorization is isolated from the agent's execution environment such that a compromised agent runtime cannot influence or bypass evaluation. | 3 |
| **5.5.2** | **Verify that** the policy decision point receives structured action descriptions (e.g., action type, target resource, parameters) rather than the agent's raw reasoning context. | 3 |

---

## C5.6 Multi-Tenant Isolation

Prevent cross-tenant information leakage through AI-specific shared infrastructure components such as inference caches and shared model state.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.6.1** | **Verify that** inference-time KV-cache entries are partitioned by authenticated session or tenant identity and that automatic prefix caching does not share cached prefixes across distinct security principals, to prevent timing-based prompt reconstruction attacks. | 2 |
| **5.6.2** | **Verify that** shared model serving infrastructure prevents one tenant's fine-tuning, inference, or embedding operations from influencing or observing another tenant's operations through shared model state, adapter weights, or compute resources. | 2 |

---

## References

* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
* [I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving (NDSS 2025)](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/)
