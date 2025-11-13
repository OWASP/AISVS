# C4 Infrastructure, Configuration & Deployment Security

## Control Objective

AI infrastructure must be hardened against privilege escalation, supply chain tampering, and lateral movement through secure configuration, runtime isolation, trusted deployment pipelines, and comprehensive monitoring. Only validated and authorized infrastructure components reach production through controlled processes that ensure security, integrity, and auditability.

---

## C4.1 Runtime Environment Isolation

Prevent container escapes and privilege escalation through OS-level isolation primitives.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.1.1** | **Verify that** all AI workloads run with minimal permissions needed on the operating system, by e.g. dropping unnecessary Linux capabilities in case of a container. | 1 | D/V |
| **4.1.2** | **Verify that** workloads are protected by technologies limiting exploitation such as sandboxing, seccomp profiles, AppArmor, SELinux or similar, and that the configuration is appropriate. | 1 | D/V |
| **4.1.3** | **Verify that** workloads run with a read-only root filesystem, and that any writable mounts are explicitly defined and hardened with restrictive options (e.g., noexec, nosuid, nodev). | 2 | D/V |
| **4.1.4** | **Verify that** runtime monitoring detects privilege-escalation and container-escape behaviors and automatically terminates offending processes. | 2 | D/V |
| **4.1.5** | **Verify that** high-risk AI workloads run in hardware-isolated environments (e.g., TEEs, trusted hypervisors, or bare-metal nodes) only after successful remote attestation. | 3 | D/V |

---

## C4.2 Secure Build & Deployment Pipelines

Ensure cryptographic integrity and supply chain security through reproducible builds and signed artifacts.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.2.1** | **Verify that** builds are reproducible and produce signed provenance metadata as appropriate for the build artifacts that can be independently verified. | 1 | D/V |
| **4.2.2** | **Verify that** builds produce a software bill of materials (SBOM) and are signed before being accepted for deployment. | 2 | D/V |
| **4.2.3** | **Verify that** build artifact (e.g., container images) signatures and provenance metadata are validated at deployment, and unverified artifacts are rejected. | 2 | D/V |

---

## C4.3 Network Security & Access Control

Implement zero-trust networking with default-deny policies and encrypted communications.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.3.1** | **Verify that** network policies enforce default-deny ingress and egress, with only required services explicitly allowed. | 1 | D/V |
| **4.3.2** | **Verify that** administrative access protocols (e.g., SSH, RDP) and access to cloud metadata services are restricted and require strong authentication. | 1 | D/V |
| **4.3.3** | **Verify that** egress traffic is restricted to approved destinations and all requests are logged. | 2 | D/V |
| **4.3.4** | **Verify that** inter-service communication uses mutual TLS with certificate validation and regular automated rotation. | 2 | D/V |
| **4.3.5** | **Verify that** AI workloads and environments (dev, test, prod) run in isolated network segments (VPCs/VNets) with no direct internet access and no shared IAM roles, security groups, or cross-environment connectivity. | 2 | D/V |

## C4.4 Secrets & Cryptographic Key Management

Protect secrets and cryptographic keys with secure storage, automated rotation, and strong access controls.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.4.1** | **Verify that** secrets are stored in a dedicated secrets management system with encryption at rest and isolated from application workloads. | 1 | D/V |
| **4.4.2** | **Verify that** cryptographic keys are generated and stored in hardware-backed modules (e.g., HSMs, cloud KMS). | 1 | D/V |
| **4.4.3** | **Verify that** access to production secrets requires strong authentication. | 1 | D/V |
| **4.4.4** | **Verify that** secrets are deployed to applications at runtime through a dedicated secrets management system. Secrets must never be embedded in source code, configuration files, build artifacts, container images, or environment variables. | 1 | D/V |
| **4.4.5** | **Verify that** secrets rotation is automated. | 2 | D/V |

---

## C4.5 AI Workload Sandboxing & Validation

Isolate untrusted AI models in secure sandboxes and protect sensitive AI workloads using trusted execution environments (TEEs) and confidential computing technologies.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.5.1** | **Verify that** external or untrusted AI models execute in isolated sandboxes.| 1 | D/V |
| **4.5.2** | **Verify that** sandboxed workloads have no outbound network connectivity by default, with any required access explicitly defined.| 1 | D/V |
| **4.5.3** | **Verify that** workload attestation is performed before model or workload loading, ensuring cryptographic proof of a trusted execution environment. | 2 | D/V |
| **4.5.4** | **Verify that** confidential workloads execute within a trusted execution environment (TEE) that provides hardware-enforced isolation, memory encryption, and integrity protection. | 3 | D/V |
| **4.5.5** | **Verify that** confidential inference services prevent model extraction through encrypted computation with sealed model weights and protected execution. | 3 | D/V |
| **4.5.6** | **Verify that** orchestration of trusted execution environments includes lifecycle management, remote attestation, and encrypted communication channels. | 3 | D/V |
| **4.5.7** | **Verify that** secure multi-party computation (SMPC) enables collaborative AI training without exposing individual datasets or model parameters. | 3 | D/V |

---

## C4.6 AI Infrastructure Resource Management, Backup and Recovery

Prevent resource exhaustion attacks and ensure fair resource allocation through quotas and monitoring. Maintain infrastructure resilience through secure backups, tested recovery procedures, and disaster recovery capabilities.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.6.1** | **Verify that** workload's resource consumption is limited appropriately with e.g. Kubernetes ResourceQuotas or similar to mitigate Denial of Service attacks. | 2 | D/V |
| **4.6.2** | **Verify that** resource exhaustion triggers automated protections (e.g., rate limiting or workload isolation) once defined CPU, memory, or request thresholds are exceeded. | 2 | D/V |
| **4.6.3** | **Verify that** backup systems run in isolated networks with separate credentials, and the storage system is either run in an air-gapped network or implements WORM (write-once-read-many) protection against unauthorized modification. | 2 | D/V |

---

## C4.7 AI Hardware Security

Secure AI-specific hardware components including GPUs, TPUs, and specialized AI accelerators.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.7.1** | **Verify that** before workload execution, AI accelerator integrity is validated using hardware-based attestation mechanisms (e.g., TPM, DRTM, or equivalent). | 2 | D/V |
| **4.7.2** | **Verify that** accelerator (GPU) memory is isolated between workloads through partitioning mechanisms with memory sanitization between jobs. | 2 | D/V |
| **4.7.3** | **Verify that** hardware security modules (HSMs) protect AI model weights and cryptographic keys with certification to FIPS 140-3 Level 3 or Common Criteria EAL4+. | 3 | D/V |
| **4.7.4** | **Verify that** accelerator firmware (GPU/TPU/NPUs) is version-pinned, signed, and attested at boot; unsigned or debug firmware is blocked. | 2 | D/V |
| **4.7.5** | **Verify that** VRAM and on-package memory are zeroed between jobs/tenants and that device reset policies prevent cross-tenant data remanence. | 2 | D/V |
| **4.7.6** | **Verify that** partitioning/isolation features (e.g., MIG/VM partitioning) are enforced per tenant and prevent peer-to-peer memory access across partitions. | 2 | D/V |
| **4.7.7** | **Verify that** accelerator interconnects (NVLink/PCIe/InfiniBand/RDMA/NCCL) are restricted to approved topologies and authenticated endpoints; plaintext cross-tenant links are disallowed. | 3 | D/V |
| **4.7.8** | **Verify that** accelerator telemetry (power, temps, ECC, perf counters) is exported to SIEM/OTel and alerts on anomalies indicative of side-channels or covert channels. | 3 | D |

---

## C4.8 Edge & Distributed AI Security

Secure distributed AI deployments including edge computing, federated learning, and multi-site architectures.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.8.1** | **Verify that** edge AI devices authenticate to central infrastructure using mutual TLS. | 2 | D/V |
| **4.8.2** | **Verify that** edge devices implement secure boot with verified signatures and rollback protection to prevent firmware downgrade attacks. | 2 | D/V |
| **4.8.3** | **Verify that** distributed AI coordination uses Byzantine fault-tolerant consensus mechanisms with participant validation and malicious node detection. | 3 | D/V |
| **4.8.4** | **Verify that** edge-to-cloud communication supports bandwidth throttling, data compression, and secure offline operation with encrypted local storage. | 3 | D/V |
| **4.8.5** | **Verify that** mobile or edge inference applications implement platform-level anti-tampering protections (e.g., code signing, verified boot, runtime self-integrity checks) that detect and block modified binaries, repackaged apps, or attached instrumentation frameworks. | 3 | D/V |
| **4.8.6** | **Verify that** models deployed to edge or mobile devices are cryptographically signed during packaging, and that the on-device runtime validates these signatures or checksums before loading or inference; unverified or altered models must be rejected. | 3 | D/V |
| **4.8.7** | **Verify that** on-device inference runtimes enforce process, memory, and file access isolation to prevent model dumping, debugging, or extraction of intermediate embeddings and activations. | 3 | D/V |
| **4.8.8** | **Verify that** model weights and sensitive parameters stored locally are encrypted using hardware-backed key stores or secure enclaves (e.g., Android Keystore, iOS Secure Enclave, TPM/TEE), with keys inaccessible to user space. | 3 | D/V |
| **4.8.9** | **Verify that** models packaged within mobile, IoT, or embedded applications are encrypted or obfuscated at rest, and decrypted only inside a trusted runtime or secure enclave, preventing direct extraction from the app package or filesystem. | 3 | D/V |

---

## References

* [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
* [CIS Controls v8](https://www.cisecurity.org/controls/v8)
* [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
* [Cloud Security Alliance: Cloud Controls Matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix/)
* [ENISA: Secure Infrastructure Design](https://www.enisa.europa.eu/topics/critical-information-infrastructures-and-services)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
