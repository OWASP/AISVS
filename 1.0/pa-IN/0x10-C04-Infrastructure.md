<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C04-Infrastructure.md -->
<!-- Translator: GeeksikhSecurity -->

# C4 Infrastructure, Configuration & Deployment Security
# C4 ਬੁਨਿਆਦੀ ਢਾਂਚਾ, ਸੰਰਚਨਾ ਅਤੇ ਤੈਨਾਤੀ ਸੁਰੱਖਿਆ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses hardening AI-specific infrastructure components against model theft, data leakage, and cross-tenant contamination.

ਇਹ ਅਧਿਆਇ ਮਾਡਲ ਚੋਰੀ (model theft), ਡਾਟਾ ਲੀਕੇਜ, ਅਤੇ ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ ਦੂਸ਼ਣ (cross-tenant contamination) ਦੇ ਵਿਰੁੱਧ AI-ਵਿਸ਼ੇਸ਼ ਬੁਨਿਆਦੀ ਢਾਂਚੇ ਦੇ ਹਿੱਸਿਆਂ ਨੂੰ ਸਖ਼ਤ ਕਰਨ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ।

---

## C4.1 AI Workload Sandboxing & Validation
## C4.1 AI ਵਰਕਲੋਡ ਸੈਂਡਬਾਕਸਿੰਗ ਅਤੇ ਪ੍ਰਮਾਣਿਕਤਾ

Untrusted AI models must be isolated in secure sandboxes, and sensitive AI workloads protected using trusted execution environments (TEEs) and confidential computing technologies.

ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ AI ਮਾਡਲਾਂ ਨੂੰ ਸੁਰੱਖਿਅਤ ਸੈਂਡਬਾਕਸਾਂ (sandboxes) ਵਿੱਚ ਅਲੱਗ-ਥਲੱਗ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ ਸੰਵੇਦਨਸ਼ੀਲ AI ਵਰਕਲੋਡਾਂ ਨੂੰ ਭਰੋਸੇਯੋਗ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣਾਂ (trusted execution environments, TEEs) ਅਤੇ ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ (confidential computing) ਤਕਨਾਲੋਜੀਆਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਸੁਰੱਖਿਅਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------ | :---: |
| **4.1.1** | **Verify that** AI models execute in isolated sandboxes. | 1 |
| **4.1.2** | **Verify that** model artifact loading enforces an explicit allow-list of serialization formats that do not permit arbitrary code execution during deserialization. | 1 |
| **4.1.3** | **Verify that** workload attestation is performed before model loading to provide proof that the execution environment has not been tampered with. | 3 |
| **4.1.4** | **Verify that** confidential inference services protect model weights during runtime through isolated execution environments. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------ | :---: |
| **4.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਮਾਡਲ ਅਲੱਗ-ਥਲੱਗ ਕੀਤੇ ਸੈਂਡਬਾਕਸਾਂ ਵਿੱਚ ਚੱਲਦੇ ਹਨ। | 1 |
| **4.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਲੋਡਿੰਗ ਸੀਰੀਅਲਾਈਜ਼ੇਸ਼ਨ ਫ਼ਾਰਮੈਟਾਂ ਦੀ ਇੱਕ ਸਪਸ਼ਟ allow-list ਲਾਗੂ ਕਰਦੀ ਹੈ ਜੋ ਡੀਸੀਰੀਅਲਾਈਜ਼ੇਸ਼ਨ ਦੌਰਾਨ ਮਨਮਰਜ਼ੀ ਕੋਡ ਐਗਜ਼ੀਕਿਊਸ਼ਨ (arbitrary code execution) ਦੀ ਆਗਿਆ ਨਹੀਂ ਦਿੰਦੇ। | 1 |
| **4.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਲੋਡ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਵਰਕਲੋਡ ਅਟੈਸਟੇਸ਼ਨ (workload attestation) ਕੀਤੀ ਜਾਂਦੀ ਹੈ ਤਾਂ ਜੋ ਇਹ ਸਬੂਤ ਮਿਲ ਸਕੇ ਕਿ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣ ਨਾਲ ਛੇੜਛਾੜ ਨਹੀਂ ਕੀਤੀ ਗਈ। | 3 |
| **4.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਗੁਪਤ ਇਨਫ਼ਰੈਂਸ ਸੇਵਾਵਾਂ ਅਲੱਗ-ਥਲੱਗ ਕੀਤੇ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣਾਂ ਰਾਹੀਂ ਰਨਟਾਈਮ ਦੌਰਾਨ ਮਾਡਲ ਵੇਟਸ (model weights) ਦੀ ਸੁਰੱਖਿਆ ਕਰਦੀਆਂ ਹਨ। | 3 |

---

## C4.2 AI Hardware Security
## C4.2 AI ਹਾਰਡਵੇਅਰ ਸੁਰੱਖਿਆ

AI-specific hardware components, including GPUs, TPUs, and specialized AI accelerators, must be secured.

AI-ਵਿਸ਼ੇਸ਼ ਹਾਰਡਵੇਅਰ ਹਿੱਸਿਆਂ ਨੂੰ, ਜਿਨ੍ਹਾਂ ਵਿੱਚ GPU, TPU, ਅਤੇ ਵਿਸ਼ੇਸ਼ AI ਐਕਸਲੇਰੇਟਰ (accelerators) ਸ਼ਾਮਲ ਹਨ, ਸੁਰੱਖਿਅਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.2.1** | **Verify that** AI accelerator (GPU) firmware is version-pinned, signed, and attested at boot. | 2 |
| **4.2.2** | **Verify that** execution within a trusted execution environment (TEE) provides hardware-enforced isolation, memory encryption, and integrity protection. | 3 |
| **4.2.3** | **Verify that** AI accelerator (GPU) integrity is validated using hardware-based attestation mechanisms before each workload executes. | 3 |
| **4.2.4** | **Verify that** accelerator (GPU) memory is isolated between workloads through partitioning mechanisms with memory sanitization between jobs. | 3 |
| **4.2.5** | **Verify that** accelerator interconnects are restricted to approved topologies and authenticated endpoints. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਐਕਸਲੇਰੇਟਰ (GPU) ਫ਼ਰਮਵੇਅਰ ਵਰਜ਼ਨ-ਪਿੰਨ ਕੀਤਾ, ਦਸਤਖ਼ਤ ਕੀਤਾ, ਅਤੇ ਬੂਟ ਵੇਲੇ ਅਟੈਸਟ ਕੀਤਾ ਗਿਆ ਹੈ। | 2 |
| **4.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਭਰੋਸੇਯੋਗ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣ (trusted execution environment, TEE) ਦੇ ਅੰਦਰ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਹਾਰਡਵੇਅਰ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤੀ ਅਲੱਗ-ਥਲੱਗਤਾ, ਮੈਮੋਰੀ ਏਨਕ੍ਰਿਪਸ਼ਨ, ਅਤੇ ਅਖੰਡਤਾ (integrity) ਸੁਰੱਖਿਆ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ। | 3 |
| **4.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਵਰਕਲੋਡ ਦੇ ਚੱਲਣ ਤੋਂ ਪਹਿਲਾਂ AI ਐਕਸਲੇਰੇਟਰ (GPU) ਦੀ ਅਖੰਡਤਾ ਨੂੰ ਹਾਰਡਵੇਅਰ-ਆਧਾਰਿਤ ਅਟੈਸਟੇਸ਼ਨ ਵਿਧੀਆਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਪ੍ਰਮਾਣਿਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 3 |
| **4.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਐਕਸਲੇਰੇਟਰ (GPU) ਮੈਮੋਰੀ ਨੂੰ ਵਰਕਲੋਡਾਂ ਦੇ ਵਿਚਕਾਰ ਵਿਭਾਜਨ ਵਿਧੀਆਂ ਰਾਹੀਂ ਅਲੱਗ-ਥਲੱਗ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਕੰਮਾਂ ਦੇ ਵਿਚਕਾਰ ਮੈਮੋਰੀ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ ਸ਼ਾਮਲ ਹੈ। | 3 |
| **4.2.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਐਕਸਲੇਰੇਟਰ ਇੰਟਰਕਨੈਕਟ ਪ੍ਰਵਾਨਿਤ ਟੋਪੋਲੋਜੀਆਂ ਅਤੇ ਪ੍ਰਮਾਣੀਕਰਨ ਕੀਤੇ ਐਂਡਪੌਇੰਟਾਂ ਤੱਕ ਸੀਮਿਤ ਹਨ। | 3 |

---

## C4.3 Edge & Distributed AI Security
## C4.3 ਐਜ ਅਤੇ ਵੰਡੇ ਹੋਏ AI ਦੀ ਸੁਰੱਖਿਆ

Distributed AI deployments, including edge computing, federated learning, and multi-site architectures, must be secured.

ਵੰਡੀਆਂ ਹੋਈਆਂ AI ਤੈਨਾਤੀਆਂ ਨੂੰ, ਜਿਨ੍ਹਾਂ ਵਿੱਚ ਐਜ ਕੰਪਿਊਟਿੰਗ (edge computing), ਫ਼ੈਡਰੇਟਿਡ ਲਰਨਿੰਗ (federated learning), ਅਤੇ ਬਹੁ-ਸਾਈਟ ਆਰਕੀਟੈਕਚਰ ਸ਼ਾਮਲ ਹਨ, ਸੁਰੱਖਿਅਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.3.1** | **Verify that** edge AI devices authenticate to central infrastructure using strong authentication mechanisms. | 1 |
| **4.3.2** | **Verify that** models deployed to edge or mobile devices are cryptographically signed during packaging, and that the on-device runtime validates these signatures or checksums before loading or inference. | 2 |
| **4.3.3** | **Verify that** inference runtimes enforce process, memory, and file access isolation. | 3 |
| **4.3.4** | **Verify that** model weights and sensitive parameters stored locally are encrypted using hardware-backed key stores or secure enclaves. | 3 |
| **4.3.5** | **Verify that** models packaged within mobile, IoT, or embedded applications are encrypted at rest, and decrypted only inside a trusted runtime or secure enclave, preventing direct extraction from the app package or filesystem. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਐਜ AI ਡਿਵਾਈਸ ਮਜ਼ਬੂਤ ਪ੍ਰਮਾਣੀਕਰਨ ਵਿਧੀਆਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕੇਂਦਰੀ ਬੁਨਿਆਦੀ ਢਾਂਚੇ ਨਾਲ ਪ੍ਰਮਾਣੀਕਰਨ ਕਰਦੇ ਹਨ। | 1 |
| **4.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਐਜ ਜਾਂ ਮੋਬਾਈਲ ਡਿਵਾਈਸਾਂ 'ਤੇ ਤੈਨਾਤ ਕੀਤੇ ਮਾਡਲ ਪੈਕੇਜਿੰਗ ਦੌਰਾਨ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਦਸਤਖ਼ਤ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ ਇਹ ਕਿ ਡਿਵਾਈਸ 'ਤੇ ਮੌਜੂਦ ਰਨਟਾਈਮ ਲੋਡਿੰਗ ਜਾਂ ਇਨਫ਼ਰੈਂਸ ਤੋਂ ਪਹਿਲਾਂ ਇਹਨਾਂ ਦਸਤਖ਼ਤਾਂ ਜਾਂ ਚੈੱਕਸਮਾਂ ਨੂੰ ਪ੍ਰਮਾਣਿਤ ਕਰਦਾ ਹੈ। | 2 |
| **4.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇਨਫ਼ਰੈਂਸ ਰਨਟਾਈਮ ਪ੍ਰਕਿਰਿਆ, ਮੈਮੋਰੀ, ਅਤੇ ਫ਼ਾਈਲ ਪਹੁੰਚ ਦੀ ਅਲੱਗ-ਥਲੱਗਤਾ ਲਾਗੂ ਕਰਦੇ ਹਨ। | 3 |
| **4.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਸੰਭਾਲੇ ਮਾਡਲ ਵੇਟਸ ਅਤੇ ਸੰਵੇਦਨਸ਼ੀਲ ਪੈਰਾਮੀਟਰ ਹਾਰਡਵੇਅਰ-ਸਮਰਥਿਤ ਕੁੰਜੀ ਸਟੋਰਾਂ ਜਾਂ ਸੁਰੱਖਿਅਤ ਐਨਕਲੇਵਾਂ (secure enclaves) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਏਨਕ੍ਰਿਪਟ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 3 |
| **4.3.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮੋਬਾਈਲ, IoT, ਜਾਂ ਏਮਬੈਡਡ ਐਪਲੀਕੇਸ਼ਨਾਂ ਦੇ ਅੰਦਰ ਪੈਕ ਕੀਤੇ ਮਾਡਲ ਸਥਿਰ ਸਥਿਤੀ ਵਿੱਚ (at rest) ਏਨਕ੍ਰਿਪਟ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ ਸਿਰਫ਼ ਇੱਕ ਭਰੋਸੇਯੋਗ ਰਨਟਾਈਮ ਜਾਂ ਸੁਰੱਖਿਅਤ ਐਨਕਲੇਵ ਦੇ ਅੰਦਰ ਹੀ ਡੀਕ੍ਰਿਪਟ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਜਿਸ ਨਾਲ ਐਪ ਪੈਕੇਜ ਜਾਂ ਫ਼ਾਈਲਸਿਸਟਮ ਤੋਂ ਸਿੱਧੇ ਕੱਢਣ ਨੂੰ ਰੋਕਿਆ ਜਾਂਦਾ ਹੈ। | 3 |

---

## References
## ਹਵਾਲੇ

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [NIST SP 800-190: Application Container Security Guide](https://csrc.nist.gov/pubs/sp/800/190/final)
* [NSA/CISA Kubernetes Hardening Guidance](https://www.cisa.gov/news-events/alerts/2022/03/15/updated-kubernetes-hardening-guide)
* [Confidential Computing Consortium](https://confidentialcomputing.io/)
