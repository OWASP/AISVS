<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C03-Model-Lifecycle-Management.md -->
<!-- Translator: GeeksikhSecurity -->

# C3 Model Lifecycle Management & Change Control
# C3 ਮਾਡਲ ਜੀਵਨ-ਚੱਕਰ ਪ੍ਰਬੰਧਨ ਅਤੇ ਤਬਦੀਲੀ ਨਿਯੰਤਰਣ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses control of model changes so that unauthorized or unsafe modifications cannot reach production.

ਇਹ ਅਧਿਆਇ ਮਾਡਲ ਤਬਦੀਲੀਆਂ ਦੇ ਨਿਯੰਤਰਣ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ ਤਾਂ ਜੋ ਅਣਅਧਿਕਾਰਤ ਜਾਂ ਗ਼ੈਰ-ਸਲਾਮਤ (unsafe) ਸੋਧਾਂ ਉਤਪਾਦਨ (production) ਤੱਕ ਨਾ ਪਹੁੰਚ ਸਕਣ।

---

## C3.1 Model Authorization & Integrity
## C3.1 ਮਾਡਲ ਅਧਿਕਾਰੀਕਰਨ ਅਤੇ ਅਖੰਡਤਾ

Only authorized models with verified integrity should reach production environments.

ਸਿਰਫ਼ ਉਹੀ ਅਧਿਕਾਰਤ ਮਾਡਲ ਉਤਪਾਦਨ ਵਾਤਾਵਰਣਾਂ ਤੱਕ ਪਹੁੰਚਣੇ ਚਾਹੀਦੇ ਹਨ ਜਿਨ੍ਹਾਂ ਦੀ ਅਖੰਡਤਾ (integrity) ਤਸਦੀਕ ਕੀਤੀ ਗਈ ਹੋਵੇ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.1.1** | **Verify that** a model registry maintains an inventory of all deployed model artifacts and their origin. | 1 |
| **3.1.2** | **Verify that** all model artifacts (weights, configurations, tokenizers, base models, fine-tunes, adapters, and safety/policy models) are cryptographically signed by authorized entities. | 2 |
| **3.1.3** | **Verify that** model cryptographic signatures are verified at deployment admission and on load. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇੱਕ ਮਾਡਲ ਰਜਿਸਟਰੀ ਸਾਰੇ ਤੈਨਾਤ ਕੀਤੇ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟਾਂ ਅਤੇ ਉਹਨਾਂ ਦੇ ਮੂਲ ਦੀ ਇਨਵੈਂਟਰੀ ਰੱਖਦੀ ਹੈ। | 1 |
| **3.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਾਰੇ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ (ਵੇਟਸ (weights), ਸੰਰਚਨਾਵਾਂ, ਟੋਕਨਾਈਜ਼ਰ, ਬੇਸ ਮਾਡਲ, ਫ਼ਾਈਨ-ਟਿਊਨ, ਅਡੈਪਟਰ, ਅਤੇ ਸਲਾਮਤੀ (safety)/ਨੀਤੀ ਮਾਡਲ) ਅਧਿਕਾਰਤ ਇਕਾਈਆਂ ਦੁਆਰਾ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਦਸਤਖ਼ਤ ਕੀਤੇ ਗਏ ਹਨ। | 2 |
| **3.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਦੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਦਸਤਖ਼ਤ ਤੈਨਾਤੀ ਦਾਖ਼ਲੇ ਸਮੇਂ ਅਤੇ ਲੋਡ ਹੋਣ ਸਮੇਂ ਤਸਦੀਕ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 2 |

---

## C3.2 Model Validation & Testing
## C3.2 ਮਾਡਲ ਪ੍ਰਮਾਣਿਕਤਾ ਅਤੇ ਟੈਸਟਿੰਗ

Models must pass defined security and safety validations before deployment.

ਮਾਡਲਾਂ ਲਈ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਪਰਿਭਾਸ਼ਿਤ ਸੁਰੱਖਿਆ (security) ਅਤੇ ਸਲਾਮਤੀ (safety) ਪ੍ਰਮਾਣਿਕਤਾਵਾਂ ਪਾਸ ਕਰਨੀਆਂ ਲਾਜ਼ਮੀ ਹਨ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------------------------- | :---: |
| **3.2.1** | **Verify that** models undergo automated input validation testing, safety evaluation testing, and output sanitization testing before deployment. | 1 |
| **3.2.2** | **Verify that** models subjected to post-training quantization are re-evaluated against the same safety and alignment test suite on the compressed artifact before deployment. | 2 |
| **3.2.3** | **Verify that** provider model, version, or routing changes trigger security re-evaluation before continued use. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------------------------- | :---: |
| **3.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਸਵੈਚਲਿਤ ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ ਟੈਸਟਿੰਗ, ਸਲਾਮਤੀ ਮੁਲਾਂਕਣ ਟੈਸਟਿੰਗ, ਅਤੇ ਆਊਟਪੁੱਟ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ ਟੈਸਟਿੰਗ ਵਿੱਚੋਂ ਲੰਘਦੇ ਹਨ। | 1 |
| **3.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਖਲਾਈ-ਉਪਰੰਤ ਕੁਆਂਟਾਈਜ਼ੇਸ਼ਨ (post-training quantization) ਵਿੱਚੋਂ ਲੰਘੇ ਮਾਡਲਾਂ ਦਾ, ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ, ਸੰਕੁਚਿਤ ਆਰਟੀਫ਼ੈਕਟ ਉੱਤੇ ਉਸੇ ਸਲਾਮਤੀ ਅਤੇ ਅਲਾਈਨਮੈਂਟ (alignment) ਟੈਸਟ ਸੂਟ ਦੇ ਵਿਰੁੱਧ ਮੁੜ-ਮੁਲਾਂਕਣ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **3.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪ੍ਰਦਾਤਾ ਦੇ ਮਾਡਲ, ਵਰਜ਼ਨ, ਜਾਂ ਰੂਟਿੰਗ ਵਿੱਚ ਤਬਦੀਲੀਆਂ ਵਰਤੋਂ ਜਾਰੀ ਰੱਖਣ ਤੋਂ ਪਹਿਲਾਂ ਸੁਰੱਖਿਆ ਮੁੜ-ਮੁਲਾਂਕਣ ਨੂੰ ਸ਼ੁਰੂ ਕਰਦੀਆਂ ਹਨ। | 3 |

---

## C3.3 Controlled Deployment & Rollback
## C3.3 ਨਿਯੰਤਰਿਤ ਤੈਨਾਤੀ ਅਤੇ ਰੋਲਬੈਕ

Model deployments must be controlled, monitored, and reversible to support lifecycle management.

ਜੀਵਨ-ਚੱਕਰ ਪ੍ਰਬੰਧਨ ਦਾ ਸਮਰਥਨ ਕਰਨ ਲਈ ਮਾਡਲ ਤੈਨਾਤੀਆਂ ਦਾ ਨਿਯੰਤਰਿਤ, ਨਿਗਰਾਨੀ ਅਧੀਨ, ਅਤੇ ਉਲਟਾਉਣਯੋਗ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.3.1** | **Verify that** production deployments implement rollout mechanisms with automated rollback triggers. | 2 |
| **3.3.2** | **Verify that** rollback capabilities restore the complete model state. | 2 |
| **3.3.3** | **Verify that** model versions running in parallel use isolated runtime state so that AI-specific shared resources are not shared across deployments. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਉਤਪਾਦਨ ਤੈਨਾਤੀਆਂ ਸਵੈਚਲਿਤ ਰੋਲਬੈਕ ਟ੍ਰਿਗਰਾਂ ਦੇ ਨਾਲ ਰੋਲਆਊਟ ਵਿਧੀਆਂ ਲਾਗੂ ਕਰਦੀਆਂ ਹਨ। | 2 |
| **3.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਰੋਲਬੈਕ ਸਮਰੱਥਾਵਾਂ ਮਾਡਲ ਦੀ ਸੰਪੂਰਨ ਸਥਿਤੀ ਨੂੰ ਬਹਾਲ ਕਰਦੀਆਂ ਹਨ। | 2 |
| **3.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਮਾਨਾਂਤਰ ਚੱਲ ਰਹੇ ਮਾਡਲ ਵਰਜ਼ਨ ਅਲੱਗ-ਥਲੱਗ ਕੀਤੀ ਰਨਟਾਈਮ ਸਥਿਤੀ ਵਰਤਦੇ ਹਨ ਤਾਂ ਜੋ AI-ਵਿਸ਼ੇਸ਼ ਸਾਂਝੇ ਸਰੋਤ ਵੱਖ-ਵੱਖ ਤੈਨਾਤੀਆਂ ਵਿਚਕਾਰ ਸਾਂਝੇ ਨਾ ਕੀਤੇ ਜਾਣ। | 2 |

---

## C3.4 Secure Development Practices
## C3.4 ਸੁਰੱਖਿਅਤ ਵਿਕਾਸ ਅਮਲ

Model development environments must be separated from production environments.

ਮਾਡਲ ਵਿਕਾਸ ਵਾਤਾਵਰਣਾਂ ਨੂੰ ਉਤਪਾਦਨ ਵਾਤਾਵਰਣਾਂ ਤੋਂ ਵੱਖ ਕੀਤਾ ਜਾਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.4.1** | **Verify that** AI-specific runtime components are not shared across environment boundaries (e.g., development, staging, production). | 1 |
| **3.4.2** | **Verify that** model training and fine-tuning environments are isolated from production environments. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.4.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI-ਵਿਸ਼ੇਸ਼ ਰਨਟਾਈਮ ਹਿੱਸੇ ਵਾਤਾਵਰਣ ਸੀਮਾਵਾਂ (ਜਿਵੇਂ, ਵਿਕਾਸ, ਸਟੇਜਿੰਗ, ਉਤਪਾਦਨ) ਦੇ ਆਰ-ਪਾਰ ਸਾਂਝੇ ਨਹੀਂ ਕੀਤੇ ਜਾਂਦੇ। | 1 |
| **3.4.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਸਿਖਲਾਈ ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਵਾਤਾਵਰਣ ਉਤਪਾਦਨ ਵਾਤਾਵਰਣਾਂ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਕੀਤੇ ਗਏ ਹਨ। | 2 |

---

## C3.5 Pipeline Fine-Tuning
## C3.5 ਪਾਈਪਲਾਈਨ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ

Fine-tuning pipelines are high-privilege operations that can alter deployed model behavior at scale. Multi-stage pipelines compound this risk because a compromise at any intermediate stage produces a subtly altered artifact that subsequent stages accept.

ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਪਾਈਪਲਾਈਨਾਂ ਉੱਚ-ਵਿਸ਼ੇਸ਼ ਅਧਿਕਾਰ ਵਾਲੀਆਂ ਕਾਰਵਾਈਆਂ ਹਨ ਜੋ ਤੈਨਾਤ ਕੀਤੇ ਮਾਡਲ ਦੇ ਵਿਵਹਾਰ ਨੂੰ ਵੱਡੇ ਪੱਧਰ 'ਤੇ ਬਦਲ ਸਕਦੀਆਂ ਹਨ। ਬਹੁ-ਪੜਾਵੀ ਪਾਈਪਲਾਈਨਾਂ ਇਸ ਜੋਖਮ ਨੂੰ ਹੋਰ ਵਧਾ ਦਿੰਦੀਆਂ ਹਨ ਕਿਉਂਕਿ ਕਿਸੇ ਵੀ ਵਿਚਕਾਰਲੇ ਪੜਾਅ 'ਤੇ ਹੋਇਆ ਸਮਝੌਤਾ (compromise) ਇੱਕ ਸੂਖਮ ਢੰਗ ਨਾਲ ਬਦਲਿਆ ਹੋਇਆ ਆਰਟੀਫ਼ੈਕਟ ਪੈਦਾ ਕਰਦਾ ਹੈ ਜਿਸਨੂੰ ਅਗਲੇ ਪੜਾਅ ਸਵੀਕਾਰ ਕਰ ਲੈਂਦੇ ਹਨ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.5.1** | **Verify that** models used in RLHF fine-tuning are versioned and integrity-verified before use in a training run. | 2 |
| **3.5.2** | **Verify that** RLHF training stages include automated detection of reward hacking or reward model over-optimization. | 3 |
| **3.5.3** | **Verify that** in multi-stage fine-tuning pipelines, each stage's output is integrity-verified before it is consumed by the next stage. | 3 |
| **3.5.4** | **Verify that** fine-tuning checkpoints are registered as distinct artifacts. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **3.5.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** RLHF ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਵਿੱਚ ਵਰਤੇ ਜਾਂਦੇ ਮਾਡਲ ਕਿਸੇ ਸਿਖਲਾਈ ਦੌਰ (training run) ਵਿੱਚ ਵਰਤੋਂ ਤੋਂ ਪਹਿਲਾਂ ਵਰਜ਼ਨਬੱਧ ਕੀਤੇ ਜਾਂਦੇ ਹਨ ਅਤੇ ਉਹਨਾਂ ਦੀ ਅਖੰਡਤਾ ਤਸਦੀਕ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **3.5.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** RLHF ਸਿਖਲਾਈ ਪੜਾਵਾਂ ਵਿੱਚ reward hacking (ਇਨਾਮ ਦੀ ਦੁਰਵਰਤੋਂ) ਜਾਂ reward model (ਇਨਾਮ ਮਾਡਲ) ਦੇ ਹੱਦੋਂ ਵੱਧ ਅਨੁਕੂਲਨ (over-optimization) ਦੀ ਸਵੈਚਲਿਤ ਪਛਾਣ ਸ਼ਾਮਲ ਹੈ। | 3 |
| **3.5.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਬਹੁ-ਪੜਾਵੀ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਪਾਈਪਲਾਈਨਾਂ ਵਿੱਚ, ਹਰ ਪੜਾਅ ਦੇ ਆਊਟਪੁੱਟ ਦੀ ਅਖੰਡਤਾ, ਅਗਲੇ ਪੜਾਅ ਦੁਆਰਾ ਵਰਤੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ, ਤਸਦੀਕ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 3 |
| **3.5.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਚੈੱਕਪੁਆਇੰਟ ਵੱਖਰੇ ਆਰਟੀਫ਼ੈਕਟਾਂ ਵਜੋਂ ਰਜਿਸਟਰ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 3 |

---

## References
## ਹਵਾਲੇ

* [MITRE ATLAS](https://atlas.mitre.org/)
* [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)
* [ISO/IEC 42001:2023 Artificial Intelligence Management System](https://www.iso.org/standard/42001)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
