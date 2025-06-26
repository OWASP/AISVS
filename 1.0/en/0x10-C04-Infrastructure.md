# C4 Infrastructure, Configuration & Deployment Security

## Control Objective

AI infrastructure must be hardened against privilege escalation, supply chain tampering, and lateral movement through secure configuration, runtime isolation, trusted deployment pipelines, and comprehensive monitoring. Only authorized, validated infrastructure components and configurations reach production through controlled processes that maintain security, integrity, and auditability.

**Core Security Goal:** Only cryptographically signed, vulnerability-scanned infrastructure components reach production through automated validation pipelines that enforce security policies and maintain immutable audit trails.

---

## C4.1 Runtime Environment Isolation

Prevent container escapes and privilege escalation through kernel-level isolation primitives and mandatory access controls.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.1.1** | **Verify that** all AI containers drop ALL Linux capabilities except CAP_SETUID, CAP_SETGID, and explicitly required capabilities documented in security baselines. | 1 | D/V |
| **4.1.2** | **Verify that** seccomp profiles block all syscalls except those in pre-approved allowlists, with violations terminating the container and generating security alerts. | 1 | D/V |
| **4.1.3** | **Verify that** AI workloads run with read-only root filesystems, tmpfs for temporary data, and named volumes for persistent data with noexec mount options enforced. | 2 | D/V |
| **4.1.4** | **Verify that** eBPF-based runtime monitoring (Falco, Tetragon, or equivalent) detects privilege escalation attempts and automatically kills offending processes within organizational response time requirements. | 2 | D/V |
| **4.1.5** | **Verify that** high-risk AI workloads execute in hardware-isolated environments (Intel TXT, AMD SVM, or dedicated bare-metal nodes) with attestation verification. | 3 | D/V |

---

## C4.2 Secure Build & Deployment Pipelines

Ensure cryptographic integrity and supply chain security through reproducible builds and signed artifacts.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.2.1** | **Verify that** infrastructure-as-code is scanned with tools (tfsec, Checkov, or Terrascan) on every commit, blocking merges with CRITICAL or HIGH severity findings. | 1 | D/V |
| **4.2.2** | **Verify that** container builds are reproducible with identical SHA256 hashes across builds and generate SLSA Level 3 provenance attestations signed with Sigstore. | 1 | D/V |
| **4.2.3** | **Verify that** container images embed CycloneDX or SPDX SBOMs and are signed with Cosign before registry push, with unsigned images rejected at deployment. | 2 | D/V |
| **4.2.4** | **Verify that** CI/CD pipelines use OIDC tokens from HashiCorp Vault, AWS IAM Roles, or Azure Managed Identity with lifetimes not exceeding organizational security policy limits. | 2 | D/V |
| **4.2.5** | **Verify that** that Cosign signatures and SLSA provenance are validated during the deployment process before container execution and that verification errors cause the deployment to fail. | 2 | D/V |
| **4.2.6** | **Verify that** build environments run in ephemeral containers or VMs with no persistent storage and network isolation from production VPCs. | 2 | D/V |

---

## C4.3 Network Security & Access Control

Implement zero-trust networking with default-deny policies and encrypted communications.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.3.1** | **Verify that** Kubernetes NetworkPolicies or any equivalent implements default-deny ingress/egress with explicit allow rules for required ports (443, 8080, etc.). | 1 | D/V |
| **4.3.2** | **Verify that** SSH (port 22), RDP (port 3389), and cloud metadata endpoints (169.254.169.254) are blocked or require certificate-based authentication. | 1 | D/V |
| **4.3.3** | **Verify that** egress traffic is filtered through HTTP/HTTPS proxies (Squid, Istio, or cloud NAT gateways) with domain allowlists and blocked requests logged. | 2 | D/V |
| **4.3.4** | **Verify that** inter-service communication uses mutual TLS with certificates rotated according to organizational policy and certificate validation enforced (no skip-verify flags). | 2 | D/V |
| **4.3.5** | **Verify that** AI infrastructure runs in dedicated VPCs/VNets with no direct internet access and communicates through NAT gateways or bastion hosts only. | 2 | D/V |

---

## C4.4 Secrets & Cryptographic Key Management

Protect credentials through hardware-backed storage and automated rotation with zero-trust access.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.4.1** | **Verify that** secrets are stored in HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, or Google Secret Manager with encryption at rest using AES-256. | 1 | D/V |
| **4.4.2** | **Verify that** cryptographic keys are generated in FIPS 140-2 Level 2 HSMs (AWS CloudHSM, Azure Dedicated HSM) with key rotation according to organizational cryptographic policy. | 1 | D/V |
| **4.4.3** | **Verify that** secrets rotation is automated with zero-downtime deployment and immediate rotation triggered by personnel changes or security incidents. | 2 | D/V |
| **4.4.4** | **Verify that** container images are scanned with tools (GitLeaks, TruffleHog, or detect-secrets) blocking builds containing API keys, passwords, or certificates. | 2 | D/V |
| **4.4.5** | **Verify that** production secret access requires MFA with hardware tokens (YubiKey, FIDO2) and is recorded by immutable audit logs with user identities and timestamps. | 2 | D/V |
| **4.4.6** | **Verify that** secrets are injected via Kubernetes secrets, mounted volumes, or init containers and ensure that secrets are never embedded in environment variables or images. | 2 | D/V |

---

## C4.5 AI Workload Sandboxing & Validation

Isolate untrusted AI models in secure sandboxes with comprehensive behavioral analysis.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.5.1** | **Verify that** external AI models execute in gVisor, microVMs (such as Firecracker, CrossVM), or Docker containers with --security-opt=no-new-privileges and --read-only flags. | 1 | D/V |
| **4.5.2** | **Verify that** sandbox environments have no network connectivity (--network=none) or only localhost access with all external requests blocked by iptables rules. | 1 | D/V |
| **4.5.3** | **Verify that** AI model validation includes automated red-team testing with organizationally defined test coverage and behavioral analysis for backdoor detection. | 2 | D/V |
| **4.5.4** | **Verify that** before an AI model is promoted to production, its sandbox results are cryptographically signed by authorized security personnel and stored in immutable audit logs. | 2 | D/V |
| **4.5.5** | **Verify that** sandbox environments are destroyed and recreated from golden images between evaluations with complete filesystem and memory cleanup. | 2 | D/V |

---

## C4.6 Infrastructure Security Monitoring

Continuously scan and monitor infrastructure with automated remediation and real-time alerting.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.6.1** | **Verify that** container images are scanned according to organizational schedules with CRITICAL vulnerabilities blocking deployment based on organizational risk thresholds. | 1 | D/V |
| **4.6.2** | **Verify that** infrastructure passes CIS Benchmarks or NIST 800-53 controls with organizationally defined compliance thresholds and automated remediation for failed checks. | 1 | D/V |
| **4.6.3** | **Verify that** HIGH severity vulnerabilities are patched according to organizational risk management timelines with emergency procedures for actively exploited CVEs. | 2 | D/V |
| **4.6.4** | **Verify that** security alerts integrate with SIEM platforms (Splunk, Elastic, or Sentinel) using CEF or STIX/TAXII formats with automated enrichment. | 2 | V |
| **4.6.5** | **Verify that** infrastructure metrics are exported to monitoring systems (Prometheus, DataDog) with SLA dashboards and executive reporting. | 3 | V |
| **4.6.6** | **Verify that** configuration drift is detected using tools (Chef InSpec, AWS Config) according to organizational monitoring requirements with automatic rollback for unauthorized changes. | 2 | D/V |

---

## C4.7 AI Infrastructure Resource Management

Prevent resource exhaustion attacks and ensure fair resource allocation through quotas and monitoring.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.7.1** | **Verify that** GPU/TPU utilization is monitored with alerts triggered at organizationally defined thresholds and automatic scaling or load balancing activated based on capacity management policies. | 1 | D/V |
| **4.7.2** | **Verify that** AI workload metrics (inference latency, throughput, error rates) are collected according to organizational monitoring requirements and correlated with infrastructure utilization. | 1 | D/V |
| **4.7.3** | **Verify that** Kubernetes ResourceQuotas or equivalent limit individual workloads according to organizational resource allocation policies with hard limits enforced. | 2 | D/V |
| **4.7.4** | **Verify that** cost monitoring tracks spending per workload/tenant with alerts based on organizational budget thresholds and automated controls for budget overruns. | 2 | V |
| **4.7.5** | **Verify that** capacity planning uses historical data with organizationally defined forecasting periods and automated resource provisioning based on demand patterns. | 3 | V |
| **4.7.6** | **Verify that** resource exhaustion triggers circuit breakers according to organizational response requirements, including rate limiting based on capacity policies and workload isolation. | 2 | D/V |

---

## C4.8 Environment Separation & Promotion Controls

Enforce strict environment boundaries with automated promotion gates and security validation.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.8.1** | **Verify that** dev/test/prod environments run in separate VPCs/VNets with no shared IAM roles, security groups, or network connectivity. | 1 | D/V |
| **4.8.2** | **Verify that** environment promotion requires approval from organizationally defined authorized personnel with cryptographic signatures and immutable audit trails. | 1 | D/V |
| **4.8.3** | **Verify that** production environments block SSH access, disable debug endpoints, and require change requests with organizational advance notice requirements except emergencies. | 2 | D/V |
| **4.8.4** | **Verify that** infrastructure-as-code changes require peer review with automated testing and security scanning before merge to main branch. | 2 | D/V |
| **4.8.5** | **Verify that** non-production data is anonymized according to organizational privacy requirements, synthetic data generation, or complete data masking with PII removal verified. | 2 | D/V |
| **4.8.6** | **Verify that** promotion gates include automated security tests (SAST, DAST, container scanning) with zero CRITICAL findings required for approval. | 2 | D/V |

---

## C4.9 Infrastructure Backup & Recovery

Ensure infrastructure resilience through automated backups, tested recovery procedures, and disaster recovery capabilities.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.9.1** | **Verify that** infrastructure configurations are backed up according to organizational backup schedules to geographically separate regions with 3-2-1 backup strategy implementation. | 1 | D/V |
| **4.9.2** | **Verify that** backup systems run in isolated networks with separate credentials and air-gapped storage for ransomware protection. | 2 | D/V |
| **4.9.3** | **Verify that** recovery procedures are tested and validated through automated testing according to organizational schedules with RTO and RPO targets meeting organizational requirements. | 2 | V |
| **4.9.4** | **Verify that** disaster recovery includes AI-specific runbooks with model weight restoration, GPU cluster rebuilding, and service dependency mapping. | 3 | V |

---

## C4.10 Infrastructure Compliance & Governance

Maintain regulatory compliance through continuous assessment, documentation, and automated controls.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.10.1** | **Verify that** infrastructure compliance is assessed according to organizational schedules against SOC 2, ISO 27001, or FedRAMP controls with automated evidence collection. | 2 | D/V |
| **4.10.2** | **Verify that** infrastructure documentation includes network diagrams, data flow maps, and threat models updated according to organizational change management requirements. | 2 | V |
| **4.10.3** | **Verify that** infrastructure changes undergo automated compliance impact assessment with regulatory approval workflows for high-risk modifications. | 3 | D/V |

---

## C4.11 AI Hardware Security

Secure AI-specific hardware components including GPUs, TPUs, and specialized AI accelerators.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.11.1** | **Verify that** AI accelerator firmware (GPU BIOS, TPU firmware) is verified with cryptographic signatures and updated according to organizational patch management timelines. | 2 | D/V |
| **4.11.2** | **Verify that** before workload execution, AI accelerator integrity is validated by hardware attestation using TPM 2.0, Intel TXT, or AMD SVM. | 2 | D/V |
| **4.11.3** | **Verify that** GPU memory is isolated between workloads using SR-IOV, MIG (Multi-Instance GPU), or equivalent hardware partitioning with memory sanitization between jobs. | 2 | D/V |
| **4.11.4** | **Verify that** the AI hardware supply chain includes provenance verification with manufacturer certificates and tamper-evident packaging validation. | 3 | V |
| **4.11.5** | **Verify that** hardware security modules (HSMs) protect AI model weights and cryptographic keys with FIPS 140-2 Level 3 or Common Criteria EAL4+ certification. | 3 | D/V |

---

## C4.12 Edge & Distributed AI Infrastructure

Secure distributed AI deployments including edge computing, federated learning, and multi-site architectures.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.12.1** | **Verify that** edge AI devices authenticate to central infrastructure using mutual TLS with device certificates rotated according to organizational certificate management policy. | 2 | D/V |
| **4.12.2** | **Verify that** edge devices implement secure boot with verified signatures and rollback protection preventing firmware downgrade attacks. | 2 | D/V |
| **4.12.3** | **Verify that** distributed AI coordination uses Byzantine fault-tolerant consensus algorithms with participant validation and malicious node detection. | 3 | D/V |
| **4.12.4** | **Verify that** edge-to-cloud communication includes bandwidth throttling, data compression, and offline operation capabilities with secure local storage. | 3 | D/V |

---

## C4.13 Multi-Cloud & Hybrid Infrastructure Security

Secure AI workloads across multiple cloud providers and hybrid cloud-on-premises deployments.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.13.1** | **Verify that** multi-cloud AI deployments use cloud-agnostic identity federation (OIDC, SAML) with centralized policy management across providers. | 2 | D/V |
| **4.13.2** | **Verify that** cross-cloud data transfer uses end-to-end encryption with customer-managed keys and data residency controls enforced per jurisdiction. | 2 | D/V |
| **4.13.3** | **Verify that** hybrid cloud AI workloads implement consistent security policies across on-premise and cloud environments with unified monitoring and alerting. | 2 | D/V |
| **4.13.4** | **Verify that** cloud vendor lock-in prevention includes portable infrastructure-as-code, standardized APIs, and data export capabilities with format conversion tools. | 3 | V |
| **4.13.5** | **Verify that** multi-cloud cost optimization includes security controls preventing resource sprawl as well as unauthorized cross-cloud data transfer charges. | 3 | V |

---

## C4.14 Infrastructure Automation & GitOps Security

Secure infrastructure automation pipelines and GitOps workflows for AI infrastructure management.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.14.1** | **Verify that** GitOps repositories require signed commits with GPG keys and branch protection rules preventing direct pushes to main branches. | 2 | D/V |
| **4.14.2** | **Verify that** infrastructure automation includes drift detection with automatic remediation and rollback capabilities triggered according to organizational response requirements for unauthorized changes. | 2 | D/V |
| **4.14.3** | **Verify that** automated infrastructure provisioning includes security policy validation with deployment blocking for non-compliant configurations. | 2 | D/V |
| **4.14.4** | **Verify that** infrastructure automation secrets are managed through external secret operators (External Secrets Operator, Bank-Vaults) with automatic rotation. | 2 | D/V |
| **4.14.5** | **Verify that** self-healing infrastructure includes security event correlation with automated incident response and stakeholder notification workflows. | 3 | V |

---

## C4.15 Quantum-Resistant Infrastructure Security

Prepare AI infrastructure for quantum computing threats through post-quantum cryptography and quantum-safe protocols.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.15.1** | **Verify that** AI infrastructure implements NIST-approved post-quantum cryptographic algorithms (CRYSTALS-Kyber, CRYSTALS-Dilithium, SPHINCS+) for key exchange and digital signatures. | 3 | D/V |
| **4.15.2** | **Verify that** quantum key distribution (QKD) systems are implemented for high-security AI communications with quantum-safe key management protocols. | 3 | D/V |
| **4.15.3** | **Verify that** cryptographic agility frameworks enable rapid migration to new post-quantum algorithms with automated certificate and key rotation. | 3 | D/V |
| **4.15.4** | **Verify that** quantum threat modeling assesses AI infrastructure vulnerability to quantum attacks with documented migration timelines and risk assessments. | 3 | V |
| **4.15.5** | **Verify that** hybrid classical-quantum cryptographic systems provide defense-in-depth during the quantum transition period with performance monitoring. | 3 | D/V |

---

## C4.16 Confidential Computing & Secure Enclaves

Protect AI workloads and model weights using hardware-based trusted execution environments and confidential computing technologies.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.16.1** | **Verify that** sensitive AI models execute within Intel SGX enclaves, AMD SEV-SNP, or ARM TrustZone with encrypted memory and attestation verification. | 3 | D/V |
| **4.16.2** | **Verify that** confidential containers (Kata Containers, gVisor with confidential computing) isolate AI workloads with hardware-enforced memory encryption. | 3 | D/V |
| **4.16.3** | **Verify that** remote attestation validates enclave integrity before loading AI models with cryptographic proof of an execution environment's authenticity. | 3 | D/V |
| **4.16.4** | **Verify that** confidential AI inference services prevent model extraction through encrypted computation with sealed model weights and protected execution. | 3 | D/V |
| **4.16.5** | **Verify that** trusted execution environment orchestration manages secure enclave lifecycle with remote attestation and encrypted communication channels. | 3 | D/V |
| **4.16.6** | **Verify that** secure multi-party computation (SMPC) enables collaborative AI training without exposing individual datasets or model parameters. | 3 | D/V |

---

## C4.17 Zero-Knowledge Infrastructure

Implement zero-knowledge proof systems for privacy-preserving AI verification and authentication without revealing sensitive information.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.17.1** | **Verify that** zero-knowledge proofs (ZK-SNARKs, ZK-STARKs) verify AI model integrity and training provenance without exposing model weights or training data. | 3 | D/V |
| **4.17.2** | **Verify that** ZK-based authentication systems enable privacy-preserving user verification for AI services without revealing identity-related information. | 3 | D/V |
| **4.17.3** | **Verify that** private set intersection (PSI) protocols enable secure data matching for federated AI without exposing individual datasets. | 3 | D/V |
| **4.17.4** | **Verify that** zero-knowledge machine learning (ZKML) systems enable verifiable AI inferences with cryptographic proof of correct computation. | 3 | D/V |
| **4.17.5** | **Verify that** ZK-rollups provide scalable, privacy-preserving AI transaction processing with batch verification and reduced computational overhead. | 3 | D/V |

---

## C4.18 Side-Channel Attack Prevention

Protect AI infrastructure from timing, power, electromagnetic, and cache-based side-channel attacks that could leak sensitive information.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.18.1** | **Verify that** AI inference timing is normalized using constant-time algorithms and padding to prevent timing-based model extraction attacks. | 3 | D/V |
| **4.18.2** | **Verify that** power analysis protection includes noise injection, power line filtering, and randomized execution patterns for AI hardware. | 3 | D/V |
| **4.18.3** | **Verify that** cache-based side-channel mitigation uses cache partitioning, randomization, and flush instructions to prevent information leakage. | 3 | D/V |
| **4.18.4** | **Verify that** electromagnetic emanation protection includes shielding, signal filtering, and randomized processing to prevent TEMPEST-style attacks. | 3 | D/V |
| **4.18.5** | **Verify that** microarchitectural side-channel defenses include speculative execution controls and memory access pattern obfuscation. | 3 | D/V |

---

## C4.19 Neuromorphic & Specialized AI Hardware Security

Secure emerging AI hardware architectures including neuromorphic chips, FPGAs, custom ASICs, and optical computing systems.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.19.1** | **Verify that** neuromorphic chip security includes spike pattern encryption, synaptic weight protection, and hardware-based learning rule validation. | 3 | D/V |
| **4.19.2** | **Verify that** FPGA-based AI accelerators implement bitstream encryption, anti-tamper mechanisms, and secure configuration loading with authenticated updates. | 3 | D/V |
| **4.19.3** | **Verify that** custom ASIC security includes on-chip security processors, hardware root of trust, and secure key storage with tamper detection. | 3 | D/V |
| **4.19.4** | **Verify that** optical computing systems implement quantum-safe optical encryption, secure photonic switching, and protected optical signal processing. | 3 | D/V |
| **4.19.5** | **Verify that** hybrid analog-digital AI chips include secure analog computation, protected weight storage, and authenticated analog-to-digital conversion. | 3 | D/V |

---

## C4.20 Privacy-Preserving Compute Infrastructure

Implement infrastructure controls for privacy-preserving computation to protect sensitive data during AI processing and analysis.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.20.1** | **Verify that** homomorphic encryption infrastructure enables encrypted computation on sensitive AI workloads with cryptographic integrity verification and performance monitoring. | 3 | D/V |
| **4.20.2** | **Verify that** private information retrieval systems enable database queries without revealing query patterns with cryptographic protection of access patterns. | 3 | D/V |
| **4.20.3** | **Verify that** secure multi-party computation protocols enable privacy-preserving AI inference without exposing individual inputs or intermediate computations. | 3 | D/V |
| **4.20.4** | **Verify that** privacy-preserving key management includes distributed key generation, threshold cryptography, and secure key rotation with hardware-backed protection. | 3 | D/V |
| **4.20.5** | **Verify that** privacy-preserving compute performance is optimized through batching, caching, and hardware acceleration while maintaining cryptographic security guarantees. | 3 | D/V |

---

## C4.15 Agent Framework Cloud Integration Security & Hybrid Deployment

Security controls for cloud-integrated agent frameworks with hybrid on-premises/cloud architectures.

| # | Description | Level | Role |
|:--------:|--------------------------------------------------------------------------------------------|:---:|:---:|
| **4.15.1** | **Verify that** cloud storage integration uses end-to-end encryption with agent-controlled key management. | 1 | D/V |
| **4.15.2** | **Verify that** hybrid deployment security boundaries are clearly defined with encrypted communication channels. | 2 | D/V |
| **4.15.3** | **Verify that** cloud resource access includes zero-trust verification with continuous authentication. | 2 | D/V |
| **4.15.4** | **Verify that** data residency requirements are enforced by cryptographic attestation of storage locations. | 3 | D/V |
| **4.15.5** | **Verify that** cloud provider security assessments include agent-specific threat modeling and risk evaluation. | 3 | D/V |

---

## References

* [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
* [CIS Controls v8](https://www.cisecurity.org/controls/v8)
* [OWASP Container Security Verification Standard](https://github.com/OWASP/Container-Security-Verification-Standard)
* [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
* [SLSA Supply Chain Security Framework](https://slsa.dev/)
* [NIST SP 800-190: Application Container Security Guide](https://csrc.nist.gov/publications/detail/sp/800-190/final)
* [Cloud Security Alliance: Cloud Controls Matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix/)
* [ENISA: Secure Infrastructure Design](https://www.enisa.europa.eu/topics/critical-information-infrastructures-and-services)
* [NIST SP 800-53: Security Controls for Federal Information Systems](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
* [ISO 27001:2022 Information Security Management](https://www.iso.org/standard/27001)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
* [FIPS 140-2 Security Requirements](https://csrc.nist.gov/publications/detail/fips/140/2/final)
* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
* [IEEE 2857: Privacy Engineering for AI Systems](https://standards.ieee.org/ieee/2857/7273/)
* [NIST SP 800-161: Cybersecurity Supply Chain Risk Management](https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final)
* [NIST Post-Quantum Cryptography Standards](https://csrc.nist.gov/Projects/post-quantum-cryptography)
* [Intel SGX Developer Guide](https://www.intel.com/content/www/us/en/developer/tools/software-guard-extensions/overview.html)
* [AMD SEV-SNP White Paper](https://www.amd.com/system/files/TechDocs/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf)
* [ARM TrustZone Technology](https://developer.arm.com/ip-products/security-ip/trustzone)
* [ZK-SNARKs: A Gentle Introduction](https://blog.ethereum.org/2016/12/05/zksnarks-in-a-nutshell/)
* [NIST SP 800-57: Cryptographic Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)
* [Side-Channel Attack Countermeasures](https://link.springer.com/book/10.1007/978-3-319-75268-6)
* [Neuromorphic Computing Security Challenges](https://ieeexplore.ieee.org/document/9458103)
* [FPGA Security: Fundamentals, Evaluation, and Countermeasures](https://link.springer.com/book/10.1007/978-3-319-90385-9)
* [Microsoft SEAL: Homomorphic Encryption Library](https://github.com/Microsoft/SEAL)
* [HElib: Homomorphic Encryption Library](https://github.com/homenc/HElib)
* [PALISADE Lattice Cryptography Library](https://palisade-crypto.org/)
* [Differential Privacy: A Survey of Results](https://link.springer.com/chapter/10.1007/978-3-540-79228-4_1)
* [Secure Aggregation for Federated Learning](https://eprint.iacr.org/2017/281.pdf)
* [Private Information Retrieval: Concepts and Constructions](https://link.springer.com/book/10.1007/978-3-030-16234-8)
