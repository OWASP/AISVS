# C3 Model Lifecycle Management & Change Control

## Control Objective

AI systems must implement change control processes that prevent unauthorized or unsafe model modifications from reaching production. These controls ensure model integrity through the entire lifecycle, from development through deployment to decommissioning, which enables rapid incident response and maintains accountability for all changes.

Generic software change-management controls (code signing, source control review, artifact registry hardening, build pipeline security, configuration management, and CI/CD audit logging) are covered by ASVS v5 (V13, V14, V15, V16), SLSA, and OWASP SCVS, and are not repeated here; training-data lineage is covered by C1, third-party pretrained model vetting by C6, AI-specific incident response and audit logging by C13, and the kill-switch and intermediate-state mechanisms invoked by C3.3.4 and C3.3.5 by C14.1.

**Core Security Goal:** Only authorized, validated models reach production by employing controlled processes that maintain integrity, traceability, and recoverability.

---

## C3.1 Model Authorization & Integrity

Only authorized models with verified integrity reach production environments.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.1.1** | **Verify that** a model registry maintains an inventory of all deployed model artifacts and produces a machine-readable Model/AI Bill of Materials (MBOM/AIBOM) (e.g., SPDX or CycloneDX). | 1 |
| **3.1.2** | **Verify that** all model artifacts (weights, configurations, tokenizers, base models, fine-tunes, adapters, and safety/policy models) are cryptographically signed by authorized entities. | 1 |
| **3.1.3** | **Verify that** model artifact signatures and integrity checksums are verified at deployment admission and on load, and unsigned, tampered, or mismatched artifacts are rejected. | 1 |
| **3.1.4** | **Verify that** lineage and dependency tracking maintains a dependency graph that enables identification of all consuming services and agents per environment (e.g., dev, staging, prod). | 3 |
| **3.1.5** | **Verify that** model origin integrity and trace records include an authorizing entity's identity, training data checksums, validation test results with pass/fail status, signature fingerprint/certificate chain ID, a creation timestamp, and approved deployment environments. | 3 |

---

## C3.2 Model Validation & Testing

Models must pass defined security and safety validations before deployment.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.2.1** | **Verify that** models undergo automated input validation testing before deployment. | 1 |
| **3.2.2** | **Verify that** models undergo automated output sanitization testing before deployment. | 1 |
| **3.2.3** | **Verify that** models undergo safety evaluations with defined pass/fail thresholds before deployment. | 1 |
| **3.2.4** | **Verify that** deployment is automatically blocked when safety evaluation results do not meet the thresholds defined for the model being deployed. | 1 |
| **3.2.5** | **Verify that** security testing covers agent workflows, tool and MCP integrations, RAG and memory interactions, multimodal inputs, and guardrails (safety models or detection services) using a versioned evaluation harness. | 2 |
| **3.2.6** | **Verify that** all model changes (deployment, configuration, retirement) generate immutable audit records including a timestamp, an authenticated actor identity, a change type, and before/after states, with trace metadata (environment and consuming services/agents) and a model identifier (version/digest/signature). | 2 |
| **3.2.7** | **Verify that** models subjected to post-training quantization, pruning, or distillation are re-evaluated against the same safety and alignment test suite on the compressed artifact before deployment, and that evaluation results are retained as distinct records linked to the compressed artifact's version or digest. | 2 |
| **3.2.8** | **Verify that** validation failures automatically block model deployment unless an explicit override approval from pre-designated authorized personnel with documented business justifications. | 3 |

---

## C3.3 Controlled Deployment & Rollback

Model deployments must be controlled, monitored, and reversible.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.3.1** | **Verify that** production deployments implement gradual rollout mechanisms (e.g., canary or blue-green deployments) with automated rollback triggers based on pre-agreed error rates, latency thresholds, guardrail alerts, or tool/MCP failure rates. | 2 |
| **3.3.2** | **Verify that** rollback capabilities restore the complete model state (weights, configurations, dependencies including adapters and safety/policy models) atomically. | 2 |
| **3.3.3** | **Verify that** model versions running in parallel (e.g., A/B tests, canary, shadow deployments) use isolated runtime state so that AI-specific shared resources (e.g., KV caches, prompt caches, session state, retrieval indices) are not shared across deployment cohorts. | 2 |
| **3.3.4** | **Verify that** emergency model shutdown capabilities can disable model endpoints within a pre-defined response time. | 3 |
| **3.3.5** | **Verify that** emergency shutdown cascades to all parts of the system including e.g. deactivating agent tool and MCP access, RAG connectors, database and API credentials, and memory-store bindings. | 3 |

---

## C3.4 Secure Development Practices

Model development and training processes must follow secure practices to prevent compromise.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.4.1** | **Verify that** AI-specific runtime components (agent orchestration services, tool/MCP servers, model registries, and prompt/policy stores) are not shared across environment boundaries (e.g., development, staging, production). | 1 |
| **3.4.2** | **Verify that** AI-specific configuration artifacts (prompt templates, agent policies and routing graphs, tool or MCP contracts and schemas, and action catalogs or capability allow-lists) are stored in version control with change history and require approved review before deployment. | 1 |
| **3.4.3** | **Verify that** model training and fine-tuning environments are isolated from production model endpoints, agent orchestration services, tool/MCP servers, and live RAG data sources. | 2 |

---

## C3.5 Hosted and Provider-Managed Model Controls

Hosted and provider-managed models may change behavior without notice. These controls help ensure visibility, reassessment, and safe operation when the organization does not control the model weights.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.5.1** | **Verify that** hosted model dependencies are inventoried with provider, endpoint, provider-exposed model identifier, version or release identifier when available, and fallback or routing relationships. | 1 |
| **3.5.2** | **Verify that** provider model, version, or routing changes trigger security re-evaluation before continued use in high-risk workflows. | 2 |
| **3.5.3** | **Verify that** logs record the exact hosted model identifier returned by the provider, or explicitly record that no such identifier was exposed. | 2 |
| **3.5.4** | **Verify that** high-assurance deployments fail closed or require explicit approval when the provider does not expose sufficient model identity or change notification information for verification. | 3 |

---

## C3.6 Fine-Tuning Pipeline Authorization & Reward Model Integrity

Fine-tuning pipelines are high-privilege operations that can alter deployed model behavior at scale. Multi-stage pipelines compound this risk because a compromise at any intermediate stage produces a subtly altered artifact that subsequent stages accept. Reward models used in RLHF are ML artifacts subject to tampering yet often treated as static infrastructure rather than versioned, validated components.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.6.1** | **Verify that** reward models used in RLHF fine-tuning are versioned, cryptographically signed, and integrity-verified before use in a training run. | 2 |
| **3.6.2** | **Verify that** initiating a fine-tuning or retraining run requires authorization from a person who did not request the run (separation of duties). | 3 |
| **3.6.3** | **Verify that** RLHF training stages include automated detection of reward hacking or reward model over-optimization (e.g., held-out human-preference probe sets, divergence thresholds, or KL penalty monitoring), with the run blocked from promotion if detection thresholds are exceeded. | 3 |
| **3.6.4** | **Verify that** in multi-stage fine-tuning pipelines, each stage's output is integrity-verified before the next stage consumes it. | 3 |
| **3.6.5** | **Verify that** intermediate fine-tuning checkpoints are registered as distinct artifacts with version or digest identifiers, enabling per-stage rollback. | 3 |

---

## References

* [MITRE ATLAS](https://atlas.mitre.org/)
* [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
* [MLOps Principles](https://ml-ops.org/content/mlops-principles)
* [Reinforcement fine-tuning](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
* [What is AI adversarial robustness?: IBM Research](https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness)
