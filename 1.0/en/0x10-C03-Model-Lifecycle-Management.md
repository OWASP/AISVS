# C3 Model Lifecycle Management & Change Control

## Control Objective

AI systems must implement change control processes that prevent unauthorized or unsafe model modifications from reaching production. This control ensures model integrity through the entire lifecycle--from development through deployment to decommissioning--which enables rapid incident response and maintains accountability for all changes.

**Core Security Goal:** Only authorized, validated models reach production by employing controlled processes that maintain integrity, traceability, and recoverability.

---

## C3.1 Model Authorization & Integrity

Only authorized models with verified integrity reach production environments.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **3.1.1** | **Verify that** all model artifacts (weights, configurations, tokenizers, base models, fine-tunes, adapters such as LoRA, and safety/policy models) are cryptographically signed by authorized entities and verified at deployment admission (and on load), blocking any unsigned or tampered artifact. | 1 | D/V |
| **3.1.2** | **Verify that** dependency tracking maintains a real-time inventory via a model registry and lineage/dependency graph, and produces a machine-readable Model/AI Bill of Materials (MBOM/AIBOM) (e.g., SPDX or CycloneDX) that enables identification of all consuming services/agents per environment (e.g., dev, staging, prod, region). | 2 | V |
| **3.1.3**  | **Verify that** model origin integrity and trace records include an authorizing entity's identity, training data checksums, validation test results with pass/fail status, signature fingerprint/certificate chain ID, a creation timestamp, and approved deployment environments. | 3 | D/V |

---

## C3.2 Model Validation & Testing

Models must pass defined security and safety validations before deployment.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **3.2.1** | **Verify that** models undergo automated security testing that includes input validation, output sanitization, and safety evaluations with pre-agreed organizational pass/fail thresholds before deployment, covering agent workflows (planning, tool or MCP calls, RAG/memory, multimodal) and guardrails (policy/safety models or detection services) with a versioned evaluation harness. | 1 | D/V |
| **3.2.2** | **Verify that** all model changes (deployment, configuration, retirement) generate immutable audit records including a timestamp, an authenticated actor identity, a change type, and before/after states, with trace metadata (environment and consuming services/agents) and a model identifier (version/digest/signature). | 1 | V |
| **3.2.3** | **Verify that** validation failures automatically block model deployment unless an explicit override approval from pre-designated authorized personnel with documented business justifications. | 2 | D/V |

---

## C3.3 Controlled Deployment & Rollback

Model deployments must be controlled, monitored, and reversible.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **3.3.1** | **Verify that** deployment processes validate cryptographic signatures and compute integrity checksums before model activation or load, failing deployment on any mismatch. | 1 | D/V |
| **3.3.2** | **Verify that** production deployments implement gradual rollout mechanisms (canary deployments, blue-green deployments) with automated rollback triggers based on pre-agreed error rates, latency thresholds, guardrail/jailbreak alerts, or tool/MCP failure rates. | 1 | D |
| **3.3.3** | **Verify that** rollback capabilities restore the complete model state (weights, configurations, dependencies including adapters and safety/policy models) atomically. | 2 | D/V |
| **3.3.4** | **Verify that** emergency model shutdown capabilities can disable model endpoints and deactivate agent tools or MCP access, RAG/connectors and database/API credentials, and memory-store bindings within a pre-defined response time. | 3 | D/V |

---

## C3.4 Secure Development Practices

Model development and training processes must follow secure practices to prevent compromise.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **3.4.1** | **Verify that** model development, testing, and production environments are physically or logically separated. They have no shared infrastructure, distinct access controls, and isolated data stores, and agent orchestration and tool or MCP servers are also isolated. | 1 | D/V |
| **3.4.2**  | **Verify that** model development artifacts (hyperparameters, training scripts, configuration files, prompt templates, agent policies/routing graphs, tool or MCP contracts/schemas, and action catalogs or capability allow-lists) are stored in version control and require peer review approval before use in training. | 1 | D |
| **3.4.3** | **Verify that** model training and fine-tuning occur in isolated environments with controlled network access using egress allow-lists and no access to production tools or MCP resources. | 2 | D/V |
| **3.4.4** | **Verify that** training data sources are validated through integrity checks and authenticated via trusted sources with documented chain of custody before use in model development, including RAG indexes, tool logs, and agent-generated data used for fine-tuning. | 2 | D |

---

## C3.5 Model Retirement & Decommissioning

Models must be securely retired when they are no longer needed or when security issues are identified.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **3.5.1** | **Verify that** retired model artifacts (including adapters and safety/policy models) are securely wiped using secure cryptographic erasure. | 1 | D/V |
| **3.5.2** | **Verify that** model retirement events are logged with timestamp and actor identity, model identifier (version/digest/signature), and trace metadata (environment and consuming services/agents); model signatures are revoked, and registry/serving deny-lists plus loader cache invalidation prevent agents from loading retired artifacts. | 2 | V |

---

## References

* [MITRE ATLAS](https://atlas.mitre.org/)
* [MLOps Principles](https://ml-ops.org/content/mlops-principles)
* [Reinforcement fine-tuning](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
* [What is AI adversarial robustness? – IBM Research](https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness)
