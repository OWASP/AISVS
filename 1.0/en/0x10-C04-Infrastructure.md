# C4 Infrastructure, Configuration & Deployment Security

## Control Objective

AI-specific infrastructure components must be hardened against model theft, data leakage, and cross-tenant contamination. This chapter covers AI workload sandboxing, AI accelerator hardware security, and edge/distributed AI deployment security.

---

## C4.1 AI Workload Sandboxing & Validation

Isolate untrusted AI models in secure sandboxes and protect sensitive AI workloads using trusted execution environments (TEEs) and confidential computing technologies.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.1.1** | **Verify that** external or untrusted AI models execute in isolated sandboxes. | 1 |
| **4.1.2** | **Verify that** sandboxed workloads have no outbound network connectivity by default, with any required access explicitly defined. | 1 |
| **4.1.3** | **Verify that** model artifact loading enforces an explicit allowlist of serialization formats that do not permit arbitrary code execution during deserialization, and that formats capable of arbitrary code execution (e.g., Python pickle with unrestricted globals) are rejected by default. | 1 |
| **4.1.4** | **Verify that** workload attestation is performed before model loading, ensuring cryptographic proof that the execution environment has not been tampered with. | 2 |
| **4.1.5** | **Verify that** confidential workloads execute within a trusted execution environment (TEE) that provides hardware-enforced isolation, memory encryption, and integrity protection. | 3 |
| **4.1.6** | **Verify that** confidential inference services prevent model extraction through encrypted computation with sealed model weights and protected execution. | 3 |
| **4.1.7** | **Verify that** secure multi-party computation (SMPC) enables collaborative AI training without exposing individual datasets or model parameters. | 3 |

---

## C4.2 AI Hardware Security

Secure AI-specific hardware components including GPUs, TPUs, and specialized AI accelerators.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.2.1** | **Verify that** before workload execution, AI accelerator integrity is validated using hardware-based attestation mechanisms (e.g., TPM, DRTM, or equivalent). | 2 |
| **4.2.2** | **Verify that** accelerator (GPU) memory is isolated between workloads through partitioning mechanisms with memory sanitization between jobs. | 2 |
| **4.2.3** | **Verify that** AI accelerator firmware is version-pinned, signed, and attested at boot; unsigned or debug firmware is blocked. | 2 |
| **4.2.4** | **Verify that** VRAM and on-package memory are zeroed between jobs/tenants and that device reset policies prevent cross-tenant data remanence. | 2 |
| **4.2.5** | **Verify that** partitioning/isolation features (e.g., MIG/VM partitioning) are enforced per tenant and prevent peer-to-peer memory access across partitions. | 2 |
| **4.2.6** | **Verify that** hardware security modules (HSMs) or equivalent tamper-resistant hardware protect AI model weights and cryptographic keys, with certification to an appropriate assurance level (e.g., FIPS 140-3 Level 3 or Common Criteria EAL4+). | 3 |
| **4.2.7** | **Verify that** accelerator interconnects (NVLink/PCIe/InfiniBand/RDMA/NCCL) are restricted to approved topologies and authenticated endpoints; plaintext cross-tenant links are disallowed. | 3 |
| **4.2.8** | **Verify that** accelerator telemetry (power draw, temperature, error correction, performance counters) is exported to centralized security monitoring and alerts on anomalies indicative of side-channels or covert channels. | 3 |

---

## C4.3 Edge & Distributed AI Security

Secure distributed AI deployments including edge computing, federated learning, and multi-site architectures.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.3.1** | **Verify that** edge AI devices authenticate to central infrastructure using mutual authentication with certificate validation (e.g., mutual TLS). | 1 |
| **4.3.2** | **Verify that** models deployed to edge or mobile devices are cryptographically signed during packaging, and that the on-device runtime validates these signatures or checksums before loading or inference; unverified or altered models must be rejected. | 1 |
| **4.3.3** | **Verify that** distributed AI coordination uses Byzantine fault-tolerant consensus mechanisms with participant validation and malicious node detection. | 3 |
| **4.3.4** | **Verify that** on-device inference runtimes enforce process, memory, and file access isolation to prevent model dumping, debugging, or extraction of intermediate embeddings and activations. | 3 |
| **4.3.5** | **Verify that** model weights and sensitive parameters stored locally are encrypted using hardware-backed key stores or secure enclaves (e.g., Android Keystore, iOS Secure Enclave, TPM/TEE), with keys inaccessible to user space. | 3 |
| **4.3.6** | **Verify that** models packaged within mobile, IoT, or embedded applications are encrypted or obfuscated at rest, and decrypted only inside a trusted runtime or secure enclave, preventing direct extraction from the app package or filesystem. | 3 |

---

## References

* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [NVIDIA Multi-Instance GPU (MIG) Documentation](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/)
* [Confidential Computing Consortium](https://confidentialcomputing.io/)
* [ARM TrustZone for AI](https://www.arm.com/technologies/trustzone-for-cortex-a)
