# C4 Infrastructure, Configuration & Deployment Security

## Control Objective

This chapter addresses hardening AI-specific infrastructure components against model theft, data leakage, and cross-tenant contamination.

---

## C4.1 AI Workload Sandboxing & Validation

Untrusted AI models must be isolated in secure sandboxes, and sensitive AI workloads protected using trusted execution environments (TEEs) and confidential computing technologies.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------ | :---: |
| **4.1.1** | **Verify that** AI models execute in isolated sandboxes. | 1 |
| **4.1.2** | **Verify that** model artifact loading enforces an explicit allow-list of serialization formats that do not permit arbitrary code execution during deserialization. | 1 |
| **4.1.3** | **Verify that** workload attestation is performed before model loading to provide proof that the execution environment has not been tampered with. | 3 |
| **4.1.4** | **Verify that** confidential inference services protect model weights during runtime through isolated execution environments. | 3 |

---

## C4.2 AI Hardware Security

AI-specific hardware components, including GPUs, TPUs, and specialized AI accelerators, must be secured.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.2.1** | **Verify that** AI accelerator (GPU) firmware is version-pinned, signed, and attested at boot. | 2 |
| **4.2.2** | **Verify that** execution within a trusted execution environment (TEE) provides hardware-enforced isolation, memory encryption, and integrity protection. | 3 |
| **4.2.3** | **Verify that** AI accelerator (GPU) integrity is validated using hardware-based attestation mechanisms before each workload executes. | 3 |
| **4.2.4** | **Verify that** accelerator (GPU) memory is isolated between workloads through partitioning mechanisms with memory sanitization between jobs. | 3 |
| **4.2.5** | **Verify that** accelerator interconnects are restricted to approved topologies and authenticated endpoints. | 3 |

---

## C4.3 Edge & Distributed AI Security

Distributed AI deployments, including edge computing, federated learning, and multi-site architectures, must be secured.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.3.1** | **Verify that** edge AI devices authenticate to central infrastructure using strong authentication mechanisms. | 1 |
| **4.3.2** | **Verify that** models deployed to edge or mobile devices are cryptographically signed during packaging, and that the on-device runtime validates these signatures or checksums before loading or inference. | 2 |
| **4.3.3** | **Verify that** inference runtimes enforce process, memory, and file access isolation. | 3 |
| **4.3.4** | **Verify that** model weights and sensitive parameters stored locally are encrypted using hardware-backed key stores or secure enclaves. | 3 |
| **4.3.5** | **Verify that** models packaged within mobile, IoT, or embedded applications are encrypted at rest, and decrypted only inside a trusted runtime or secure enclave, preventing direct extraction from the app package or filesystem. | 3 |

---

## References

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [NIST SP 800-190: Application Container Security Guide](https://csrc.nist.gov/pubs/sp/800/190/final)
* [NSA/CISA Kubernetes Hardening Guidance](https://www.cisa.gov/news-events/alerts/2022/03/15/updated-kubernetes-hardening-guide)
* [Confidential Computing Consortium](https://confidentialcomputing.io/)
