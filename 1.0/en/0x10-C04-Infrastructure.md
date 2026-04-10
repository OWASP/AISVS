# C4 Infrastructure, Configuration & Deployment Security

## Control Objective

AI infrastructure must be hardened against privilege escalation, supply chain tampering, and lateral movement through secure configuration, runtime isolation, trusted deployment pipelines, and comprehensive monitoring. Only validated and authorized infrastructure components reach production through controlled processes that ensure security, integrity, and auditability.

> **Scope note:** General infrastructure hardening controls — including OS-level least-privilege, seccomp/AppArmor/SELinux sandboxing, read-only filesystems, default-deny network policies, mTLS, secrets management, secret rotation, and backup isolation — are governed by [OWASP ASVS v5](https://owasp.org/www-project-application-security-verification-standard/) (V6, V8, V11, V12, V13, V14). This chapter extends those requirements where AI-specific implementation concerns apply. Implementers should satisfy both ASVS and AISVS infrastructure controls.

---

## C4.1 Runtime Environment Isolation

Prevent container escapes and privilege escalation through OS-level isolation primitives.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.1.4** | **Verify that** runtime monitoring detects privilege-escalation and container-escape behaviors and automatically terminates offending processes. | 3 |
| **4.1.5** | **Verify that** high-risk AI workloads run in hardware-isolated environments (e.g., TEEs, trusted hypervisors, or bare-metal nodes) only after successful remote attestation. | 3 |

---

## C4.2 Secure Build & Deployment Pipelines

Ensure cryptographic integrity and supply chain security through reproducible builds and signed artifacts.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.2.1** | **Verify that** builds are completely automated with no manual steps that could introduce untracked changes. | 1 |
| **4.2.2** | **Verify that** build artifacts are cryptographically signed with build-origin metadata (source repository, build pipeline, commit hash) that can be independently verified. | 2 |
| **4.2.3** | **Verify that** build artifact signatures and build-origin metadata are validated at deployment admission, and unverified artifacts are rejected. | 2 |
| **4.2.4** | **Verify that** builds are reproducible, producing identical output from identical source inputs, enabling independent verification of build integrity. | 3 |
| **4.2.5** | **Verify that** automated builds produce a software bill of materials (SBOM) listing all components, versions, and their origins. | 1 |

---

## C4.3 Network Security & Access Control

Implement zero-trust networking with default-deny policies and encrypted communications.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.3.2** | **Verify that** AI workloads across environments (development, testing, production) run in isolated network segments with no direct internet access and no cross-environment network connectivity. | 1 |
| **4.3.5** | **Verify that** egress traffic is restricted to approved destinations and all requests are logged. | 3 |
---

## C4.4 Secrets & Cryptographic Key Management

Protect secrets and cryptographic keys with secure storage, automated rotation, and strong access controls.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.4.4** | **Verify that** cryptographic keys are generated and stored in hardware-backed modules (e.g., HSMs, cloud KMS). | 2 |
---

## C4.5 AI Workload Sandboxing & Validation

Isolate untrusted AI models in secure sandboxes and protect sensitive AI workloads using trusted execution environments (TEEs) and confidential computing technologies.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.5.1** | **Verify that** external or untrusted AI models execute in isolated sandboxes. | 1 |
| **4.5.2** | **Verify that** sandboxed workloads have no outbound network connectivity by default, with any required access explicitly defined. | 1 |
| **4.5.3** | **Verify that** workload attestation is performed before model loading, ensuring cryptographic proof that the execution environment has not been tampered with. | 2 |
| **4.5.4** | **Verify that** confidential workloads execute within a trusted execution environment (TEE) that provides hardware-enforced isolation, memory encryption, and integrity protection. | 3 |
| **4.5.5** | **Verify that** confidential inference services prevent model extraction through encrypted computation with sealed model weights and protected execution. | 3 |
| **4.5.6** | **Verify that** TEE orchestration manages the full lifecycle of trusted execution environments, including provisioning, suspension, and termination. | 3 |
| **4.5.7** | **Verify that** secure multi-party computation (SMPC) enables collaborative AI training without exposing individual datasets or model parameters. | 3 |
| **4.5.8** | **Verify that** TEE orchestration performs remote attestation before each workload placement to confirm the execution environment has not been tampered with. | 3 |
| **4.5.9** | **Verify that** communication channels between TEE orchestration components and execution environments are encrypted and mutually authenticated. | 3 |
| **4.5.10** | **Verify that** model artifact loading enforces an explicit allowlist of serialization formats that do not permit arbitrary code execution during deserialization, and that formats capable of arbitrary code execution (e.g., Python pickle with unrestricted globals) are rejected by default. | 1 |

---

## C4.6 AI Infrastructure Resource Management, Backup and Recovery

Prevent resource exhaustion attacks and ensure fair resource allocation through quotas and monitoring. Maintain infrastructure resilience through secure backups, tested recovery procedures, and disaster recovery capabilities.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.6.1** | **Verify that** workload resource consumption is limited through quotas and limits (e.g., CPU, memory, GPU) to mitigate denial-of-service attacks. | 1 |
| **4.6.2** | **Verify that** resource exhaustion triggers automated protections (e.g., rate limiting or workload isolation) once defined CPU, memory, or request thresholds are exceeded. | 2 |
---

## C4.7 AI Hardware Security

Secure AI-specific hardware components including GPUs, TPUs, and specialized AI accelerators.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.7.1** | **Verify that** before workload execution, AI accelerator integrity is validated using hardware-based attestation mechanisms (e.g., TPM, DRTM, or equivalent). | 2 |
| **4.7.2** | **Verify that** accelerator (GPU) memory is isolated between workloads through partitioning mechanisms with memory sanitization between jobs. | 2 |
| **4.7.3** | **Verify that** AI accelerator firmware is version-pinned, signed, and attested at boot; unsigned or debug firmware is blocked. | 2 |
| **4.7.4** | **Verify that** VRAM and on-package memory are zeroed between jobs/tenants and that device reset policies prevent cross-tenant data remanence. | 2 |
| **4.7.5** | **Verify that** partitioning/isolation features (e.g., MIG/VM partitioning) are enforced per tenant and prevent peer-to-peer memory access across partitions. | 2 |
| **4.7.6** | **Verify that** hardware security modules (HSMs) or equivalent tamper-resistant hardware protect AI model weights and cryptographic keys, with certification to an appropriate assurance level (e.g., FIPS 140-3 Level 3 or Common Criteria EAL4+). | 3 |
| **4.7.7** | **Verify that** accelerator interconnects (NVLink/PCIe/InfiniBand/RDMA/NCCL) are restricted to approved topologies and authenticated endpoints; plaintext cross-tenant links are disallowed. | 3 |
| **4.7.8** | **Verify that** accelerator telemetry (power draw, temperature, error correction, performance counters) is exported to centralized security monitoring and alerts on anomalies indicative of side-channels or covert channels. | 3 |

---

## C4.8 Edge & Distributed AI Security

Secure distributed AI deployments including edge computing, federated learning, and multi-site architectures.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------ | :---: |
| **4.8.1** | **Verify that** edge AI devices authenticate to central infrastructure using mutual authentication with certificate validation (e.g., mutual TLS). | 1 |
| **4.8.2** | **Verify that** models deployed to edge or mobile devices are cryptographically signed during packaging, and that the on-device runtime validates these signatures or checksums before loading or inference; unverified or altered models must be rejected. | 1 |
| **4.8.3** | **Verify that** edge devices implement secure boot with verified signatures and rollback protection to prevent firmware downgrade attacks. | 2 |
| **4.8.4** | **Verify that** mobile or edge inference applications implement platform-level anti-tampering protections (e.g., code signing, verified boot, runtime integrity checks) that detect and block modified binaries, repackaged applications, or attached instrumentation frameworks. | 2 |
| **4.8.5** | **Verify that** distributed AI coordination uses Byzantine fault-tolerant consensus mechanisms with participant validation and malicious node detection. | 3 |
| **4.8.6** | **Verify that** edge-to-cloud communication implements bandwidth throttling and data compression to maintain availability under constrained or degraded network conditions. | 3 |
| **4.8.10** | **Verify that** edge devices support secure offline operation, with data stored locally encrypted at rest using hardware-backed key management. | 3 |
| **4.8.7** | **Verify that** on-device inference runtimes enforce process, memory, and file access isolation to prevent model dumping, debugging, or extraction of intermediate embeddings and activations. | 3 |
| **4.8.8** | **Verify that** model weights and sensitive parameters stored locally are encrypted using hardware-backed key stores or secure enclaves (e.g., Android Keystore, iOS Secure Enclave, TPM/TEE), with keys inaccessible to user space. | 3 |
| **4.8.9** | **Verify that** models packaged within mobile, IoT, or embedded applications are encrypted or obfuscated at rest, and decrypted only inside a trusted runtime or secure enclave, preventing direct extraction from the app package or filesystem. | 3 |

---

## References

* [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
* [CIS Controls v8](https://www.cisecurity.org/controls/v8)
* [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
* [Cloud Security Alliance: Cloud Controls Matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix/)
* [ENISA: Secure Infrastructure Design](https://www.enisa.europa.eu/topics/critical-information-infrastructures-and-services)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
