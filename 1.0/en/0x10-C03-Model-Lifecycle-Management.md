# C3 Model Lifecycle Management & Change Control

## Control Objective

AI systems must implement change control processes that prevent unauthorized or unsafe model modifications from reaching production. These controls enable rapid incident response and maintain accountability for all changes by ensuring model integrity through the entire lifecycle, from development through deployment to decommissioning. By employing controlled processes that maintain integrity, traceability, and recoverability, only authorized and validated models will reach production.

---

## C3.1 Model Authorization & Integrity

Only authorized models with verified integrity should reach production environments.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.1.1** | **Verify that** a model registry maintains an inventory of all deployed model artifacts and their origin. | 1 |
| **3.1.2** | **Verify that** all model artifacts (weights, configurations, tokenizers, base models, fine-tunes, adapters, and safety/policy models) are cryptographically signed by authorized entities. | 2 |
| **3.1.3** | **Verify that** model cryptographic signatures are verified at deployment admission and on load. | 2 |

---

## C3.2 Model Validation & Testing

Models must pass defined security and safety validations before deployment.

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------- | :---: |
| **3.2.1** | **Verify that** models undergo automated input validation testing, safety evaluation testing and output sanitization testing before deployment. | 1 |
| **3.2.2** | **Verify that** models that are subjected to post-training quantization will be re-evaluated against the same safety and alignment test suite on the compressed artifact before deployment. | 2 |
| **3.2.3** | **Verify that** provider model, version, or routing changes trigger security re-evaluation before continued use. | 3 |

---

## C3.3 Controlled Deployment & Rollback

Model deployments must be controlled, monitored, and reversible.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.3.1** | **Verify that** production deployments implement rollout mechanisms with automated rollback triggers. | 2 |
| **3.3.2** | **Verify that** rollback capabilities restore the complete model state. | 2 |
| **3.3.3** | **Verify that** model versions running in parallel use isolated runtime state so that AI-specific shared resources are not shared across deployments. | 2 |

---

## C3.4 Secure Development Practices

Model development must follow secure practices to prevent compromise.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.4.1** | **Verify that** AI-specific runtime components are not shared across environment boundaries (e.g., development, staging, production). | 1 |
| **3.4.2** | **Verify that** model training and fine-tuning environments are isolated from production environments. | 2 |

---

## C3.5 Pipeline Fine-Tuning

Fine-tuning pipelines are high-privilege operations that can alter deployed model behavior at scale. Multi-stage pipelines compound this risk because a compromise at any intermediate stage produces a subtly altered artifact that subsequent stages accept. Reward models used in RLHF are ML artifacts subject to tampering yet they are often treated as static infrastructure rather than versioned, validated components.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.6.1** | **Verify that** models used in RLHF fine-tuning are versioned and integrity-verified before use in a training run. | 2 |
| **3.6.2** | **Verify that** RLHF training stages include automated detection of reward hacking or reward model over-optimization. | 3 |
| **3.6.3** | **Verify that** in multi-stage fine-tuning pipelines, each stage's output is integrity-verified before the next stage is consumed. | 3 |
| **3.6.4** | **Verify that** fine-tuning checkpoints are registered as distinct artifacts. | 3 |

---

## References

* [MITRE ATLAS](https://atlas.mitre.org/)
* [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
* [MLOps Principles](https://ml-ops.org/content/mlops-principles)
* [Reinforcement fine-tuning](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
* [What is AI adversarial robustness?: IBM Research](https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness)
