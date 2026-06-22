# C5 Access Control & Identity for AI Components & Users

## Control Objective

This chapter addresses access control challenges that AI systems introduce beyond traditional application security: classification labels must follow data through AI-specific transformations such as embeddings, caches, and model outputs; multi-tenant inference infrastructure creates novel side channels; and retrieval-augmented pipelines must enforce caller entitlements at every stage. It covers authentication, AI resource authorization and classification, and multi-tenant isolation, including runtime isolation of the policy decision point from agent execution and authorization-aware output filtering where entitlements vary per caller.

---

## C5.1 Authentication

This section covers ensuring that AI agents and human users accessing resources are properly authenticated and authorized for that level of access.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.1.1** | **Verify that** high-risk AI operations (model deployment, weight export, training data access, production configuration changes) require step-up authentication. | 3 |
| **5.1.2** | **Verify that** AI agents in federated or multi-system deployments authenticate using short-lived, minimal-scoped, cryptographically signed tokens. | 3 |

---

## C5.2 AI Resource Authorization & Classification

This section covers enforcing the caller's authorization context in AI-specific query pipelines so that the AI system does not return data that the caller is not entitled to access.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.2.1** | **Verify that** every AI resource (datasets, endpoints, vector collections, embedding indices, compute instances) enforces access controls with explicit allow-lists and default-deny policies. | 2 |
| **5.2.2** | **Verify that** retrieval pipelines (e.g., RAG queries, embedding lookups) enforce the end-user's authorization context at each retrieval and assembly stage, rather than relying solely on the service account's permissions. | 2 |
| **5.2.3** | **Verify that** sensitive data is retrieved via retrieval pipelines (e.g., RAG queries, embedding lookups) to prevent permanent storage in models. | 2 |
| **5.2.4** | **Verify that** post-inference filtering mechanisms prevent responses from including data that the requester is not authorized to receive. | 2 |
| **5.2.5** | **Verify that** the policy decision point for agent authorization is isolated from the agent's execution environment. | 2 |
| **5.2.6** | **Verify that** privileged access to model weights, training pipelines, and production AI configuration is granted just in time, with a defined maximum session duration and automatic expiry. Zero Standing Privilege (ZSP) to these resources is encouraged. | 3 |
| **5.2.7** | **Verify that** data classification labels propagate to downstream resources (embeddings, prompt caches, model outputs). | 3 |

---

## C5.3 Multi-Tenant Isolation

This section covers preventing cross-tenant information leakage through AI-specific shared infrastructure components such as inference caches and shared model state.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.3.1** | **Verify that** shared model serving infrastructure prevents one tenant's fine-tuning, inference, or embedding operations from influencing or observing another tenant's operations. | 2 |
| **5.3.2** | **Verify that** one tenant cannot influence or observe another tenant's operations through shared compute resources. Satisfying this requirement typically requires hardware partitioning, confidential computing, or dedicated per-tenant compute allocation. | 3 |

---

## References

* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
* [OAuth 2.1 (IETF Draft)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-11)
* [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
* [I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving (NDSS 2025)](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/)
