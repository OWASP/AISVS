# C04: Infrastructure, Configuration & Deployment Security

> **Source:** [`1.0/en/0x10-C04-Infrastructure.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C04-Infrastructure.md)
> **Requirements:** 46 | **Sections:** 8

## Control Objective

AI infrastructure must be hardened against privilege escalation, supply chain tampering, and lateral movement through secure configuration, runtime isolation, trusted deployment pipelines, and comprehensive monitoring. Only validated and authorized infrastructure components reach production through controlled processes that ensure security, integrity, and auditability.

> **2025-2026 Highlights:** Confidential computing for GPU workloads is advancing rapidly — NVIDIA's Vera Rubin NVL72 (announced January 2026) introduces rack-scale confidential computing spanning 72 GPUs with end-to-end encryption across CPU, GPU, and NVLink domains. Meanwhile, GPUHammer (USENIX Security 2025) demonstrated practical Rowhammer attacks on GPU GDDR6 memory, Cisco's Secure AI Factory (March 2026) brings DPU-level firewall enforcement directly onto GPU servers, and three critical runC container escape vulnerabilities (November 2025) affect every Docker and Kubernetes environment. On the compliance front, the EU AI Act's August 2, 2026 deadline for high-risk AI systems is now less than five months away.

---

## Section Pages

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C4.1 | [Runtime Environment Isolation](C04-01-Runtime-Environment-Isolation.md) | 5 | 4.1.1–4.1.5 |
| C4.2 | [Secure Build & Deployment Pipelines](C04-02-Secure-Build-Deployment.md) | 4 | 4.2.1–4.2.4 |
| C4.3 | [Network Security & Access Control](C04-03-Network-Security-Access-Control.md) | 5 | 4.3.1–4.3.5 |
| C4.4 | [Secrets & Cryptographic Key Management](C04-04-Secrets-Key-Management.md) | 5 | 4.4.1–4.4.5 |
| C4.5 | [AI Workload Sandboxing & Validation](C04-05-Workload-Sandboxing-Validation.md) | 7 | 4.5.1–4.5.7 |
| C4.6 | [Resource Management, Backup & Recovery](C04-06-Resource-Management-Backup-Recovery.md) | 3 | 4.6.1–4.6.3 |
| C4.7 | [AI Hardware Security](C04-07-Hardware-Security.md) | 8 | 4.7.1–4.7.8 |
| C4.8 | [Edge & Distributed AI Security](C04-08-Edge-Distributed-Security.md) | 9 | 4.8.1–4.8.9 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Container escape via GPU toolkits** — Critical vulnerabilities in NVIDIA Container Toolkit (CVE-2024-0132, CVE-2025-23266 "NVIDIAScape") allow AI workloads to break container isolation and gain root on the host. As of mid-2025, 37% of cloud AI environments were vulnerable.
- **GPU side-channel attacks** — NVBleed (March 2025) demonstrated cross-VM covert channels via NVLink performance counters at 70+ Kbps, while BarraCUDA showed electromagnetic side-channel model extraction from NVIDIA Jetson edge devices. Separate research found four leakage sources bypassing MIG isolation under MPS mode.
- **GPU memory bit-flip attacks** — GPUHammer (USENIX Security 2025) demonstrated practical Rowhammer attacks against GDDR6 memory on NVIDIA GPUs. A single bit flip to a model weight's exponent can degrade accuracy from 80% to under 1%. In shared cloud GPU environments, a malicious tenant can target adjacent workloads' model weights. ECC memory (enabled by default on Hopper and Blackwell data center GPUs) mitigates this, but consumer and edge GPUs remain vulnerable.
- **Supply chain compromise of ML frameworks** — CVE-2025-32434 (CVSS 9.3) proved that PyTorch's `weights_only=True` could be bypassed for RCE. Three PickleScan zero-day bypasses (CVE-2025-10155/56/57) allowed undetected malicious model uploads to Hugging Face.
- **Secrets leakage from AI pipelines** — A November 2025 study found 65% of Forbes AI 50 companies had leaked API keys on GitHub, primarily through Jupyter notebooks and .env files. One leaked Hugging Face token exposed ~1,000 private models.
- **TEE bypass attacks** — TEE.Fail (October 2025) broke Intel SGX, TDX, and AMD SEV-SNP using DDR5 memory bus interposition hardware costing under $1,000, undermining confidential computing assumptions.
- **Container runtime breakout (runC)** — Three critical runC vulnerabilities disclosed in November 2025 (CVE-2025-31133, CVE-2025-52565, CVE-2025-52881) affect all Docker, Kubernetes, containerd, and CRI-O deployments. CVE-2025-31133 exploits a mount race condition in maskedPaths to redirect writes to `/proc/sys/kernel/core_pattern`, achieving container escape. CVE-2025-52565 abuses a timing window where `/dev/console` is mounted before security protections are applied. CVE-2025-52881 bypasses Linux Security Module labels via shared mount race conditions. All three are deliverable through untrusted container images — a realistic attack vector for AI workloads that routinely pull models and dependencies from external registries. Fixed in runC 1.2.8 / 1.3.3 / 1.4.0-rc.3.
- **Lateral movement** — Attackers have used malicious registry URLs to force exposed LLM inference servers into making outbound requests, probing for paths to training infrastructure.
- **Edge model extraction** — Studies show 34–76% success rates extracting ML models from mobile apps using standard reverse-engineering tools when models lack encryption.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Mar 2026 | Cisco Secure AI Factory with NVIDIA — DPU-level firewall for GPU servers | BlueField DPU enforcement at 400G line-rate; threats blocked at server level before reaching AI data | [Cisco Newsroom](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m03/cisco-secure-ai-factory-with-nvidia-GTC-2026.html) |
| Jan 2026 | GitHub artifact attestations with SLSA Build Level 3 | Cryptographic provenance binding build artifacts to source repos and workflows; code-to-cloud traceability for AI deployment pipelines | [GitHub Blog](https://github.blog/changelog/2026-01-20-strengthen-your-supply-chain-with-code-to-cloud-traceability-and-slsa-build-level-3-security/) |
| Nov 2025 | Three critical runC container escape vulnerabilities (CVE-2025-31133/52565/52881) | Mount race conditions and LSM bypasses in the runtime underpinning Docker, K8s, containerd; untrusted container images as attack vector | [Sysdig Blog](https://www.sysdig.com/blog/runc-container-escape-vulnerabilities) |
| Jul 2025 | GPUHammer — Rowhammer attacks on GPU GDDR6 memory (USENIX Security 2025) | Bit flips in GPU memory degrade model accuracy from 80% to <1%; cross-tenant risk in shared cloud GPUs | [The Hacker News](https://thehackernews.com/2025/07/gpuhammer-new-rowhammer-attack-variant.html) |
| Jul 2025 | CVE-2025-23266 "NVIDIAScape" — NVIDIA Container Toolkit container escape (CVSS 9.0) | 3-line Dockerfile achieves root on host; 37% of cloud AI environments affected | [Wiz Blog](https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape) |
| Jun 2025 | CVE-2025-10155/56/57 — PickleScan zero-day bypasses (CVSS 9.3 each) | Three methods bypass Hugging Face's primary model scanner; fixed in v0.0.31 | [JFrog Blog](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/) |
| Apr 2025 | CVE-2025-32434 — PyTorch `weights_only=True` RCE (CVSS 9.3) | The "safe" deserialization parameter was bypassable; fixed in PyTorch 2.6.0 | [GitHub Advisory](https://github.com/pytorch/pytorch/security/advisories/GHSA-53q9-r3pm-6pq6) |
| Mar 2025 | NVBleed — NVLink covert and side-channel attacks | Cross-VM GPU side-channel via NVLink performance counters; F1 >88% character identification | [arXiv 2503.17847](https://arxiv.org/abs/2503.17847) |
| Oct 2025 | TEE.Fail — DDR5 memory bus interposition attack | Breaks Intel SGX, TDX, AMD SEV-SNP with <$1K hardware; forged TDX attestations demonstrated | [SecurityOnline](https://securityonline.info/tee-fail-researchers-break-intel-sgx-tdx-and-amd-sev-snp-with-sub-1000-ddr5-memory-bus-attack/) |
| Nov 2025 | Wiz: 65% of Forbes AI 50 leaked secrets on GitHub | Jupyter notebooks and .env files as primary vectors; one HF token exposed ~1,000 private models | [The Register](https://www.theregister.com/2025/11/10/ai_companies_private_api_keys_github/) |
| Oct 2024 | BarraCUDA — electromagnetic side-channel model extraction | Full weight extraction from NVIDIA Jetson Orin Nano via EM emissions; no software fix possible | [arXiv 2312.07783](https://arxiv.org/pdf/2312.07783) |
| 2024 | GPU uncore leakage bypassing MIG isolation | Four leakage sources (DRAM freq, NVENC/NVDEC/NVJPEG) bypass MIG under MPS mode | [Veiled Pathways](https://faculty.ist.psu.edu/wu/papers/Veiled-Pathways.pdf) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Container isolation:** [gVisor](https://gvisor.dev/) (user-space kernel, used by Modal for AI sandboxing), [Kata Containers](https://katacontainers.io/) (lightweight VMs, 2M+ AI workloads/month at Northflank), [Firecracker](https://firecracker-microvm.github.io/) (Rust-based microVMs, ~100ms boot, used by E2B for AI agent sandboxing), [Edera Protect](https://edera.dev/) (K8s-native container isolation via lightweight VMs)
- **GPU security:** [NVIDIA MIG](https://www.nvidia.com/en-us/technologies/multi-instance-gpu/) (up to 7 hardware-isolated GPU instances on A100/H100/H200), [NVIDIA H100 Confidential Computing](https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/) (on-die root of trust, encrypted CPU-GPU transfers, remote attestation via NRAS), [NVIDIA Vera Rubin NVL72](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/) (announced January 2026 — first rack-scale confidential computing spanning 72 GPUs, 36 Vera CPUs, and NVLink interconnects in a unified trust domain; end-to-end encryption across CPU-GPU, GPU-GPU, and I/O paths with near-native performance), AMD SEV-SNP (VM-level memory encryption on Genoa/Milan CPUs), Intel TDX (VM isolation with attestation, expanding on Emerald Rapids)
- **Confidential containers:** [Confidential Containers (CoCo)](https://github.com/confidential-containers) (CNCF sandbox project — pod-level confidential computing on Kubernetes via Kata Containers CVMs with hardware-backed TEEs; developing end-to-end attestation for NVIDIA confidential GPUs), [Google Confidential GKE Nodes](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/gpus-confidential-nodes) (encrypt GPU workload data in-use), [Red Hat OpenShift + NVIDIA CoCo](https://www.redhat.com/en/blog/power-confidential-containers-red-hat-openshift-nvidia-gpus) (confidential GPU containers on OpenShift; still experimental as of early 2026)
- **Model signing & build security:** [OpenSSF Model Signing v1.0](https://github.com/sigstore/model-transparency) (released April 2025 — sign/verify ML models of any format via Sigstore), [Sigstore/cosign](https://www.sigstore.dev/) (keyless artifact signing, SLSA provenance), [GitHub artifact attestations](https://github.blog/changelog/2026-01-20-strengthen-your-supply-chain-with-code-to-cloud-traceability-and-slsa-build-level-3-security/) (January 2026 — SLSA Build Level 3, cryptographic provenance binding artifacts to source repos and build workflows, code-to-cloud traceability), [Syft](https://github.com/anchore/syft) (SBOM generation for containers, supports SPDX 3 and CycloneDX)
- **Secrets management:** [HashiCorp Vault](https://www.hashicorp.com/en/blog/integrating-secret-hygiene-into-ai-and-ml-workflows) (dynamic AI agent identity, Vault Radar for dataset secret scanning), AWS Secrets Manager, Azure Key Vault, Google Secret Manager
- **Network security:** [Calico](https://www.tigera.io/blog/securing-ai-workloads-in-kubernetes-why-traditional-network-security-isnt-enough/) (microsegmentation, FQDN-based egress filtering, WireGuard encryption), Cilium (eBPF-based network policies), Kubernetes Pod Certificates (beta in K8s v1.35 for native mTLS), [Cisco Hybrid Mesh Firewall on BlueField DPUs](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m03/cisco-secure-ai-factory-with-nvidia-GTC-2026.html) (March 2026 — 400G line-rate stateful inspection on GPU servers, policy enforcement at the DPU without consuming CPU/GPU resources)
- **Runtime threat detection:** [Falco](https://falco.org/) (CNCF graduated — eBPF-based runtime security for containers and K8s; detects privilege escalation, container escape, and anomalous system calls in real time), [Sysdig](https://sysdig.com/) (ML-enhanced threat detection and drift prevention built on Falco's runtime data)
- **Hardware monitoring:** [NVIDIA DCGM](https://github.com/NVIDIA/DCGM) (GPU health monitoring, telemetry export to Prometheus/Grafana), [NVIDIA Remote Attestation Service](https://developer.nvidia.com/blog/announcing-confidential-computing-general-access-on-nvidia-h100-tensor-core-gpus) (GPU identity and firmware validation)
- **Edge & mobile deployment:** [Apple Core ML encryption](https://developer.apple.com/documentation/coreml/encrypting-a-model-in-your-app) (compile-time model encryption, decrypted only at runtime), [ONNX Server for Open Enclave](https://github.com/microsoft/onnx-server-openenclave) (confidential inference with attestation), Android Keystore / iOS Secure Enclave for model decryption key protection
- **AI workload sandboxing:** [E2B](https://e2b.dev/) (Firecracker-based AI agent sandboxing), [IOValve](https://www.microsoft.com/en-us/research/wp-content/uploads/2025/08/iovalve-ccs25.pdf) (Microsoft Research, leakage-free I/O sandbox, ACM CCS 2025), [UK AISI Inspect Sandboxing Toolkit](https://www.aisi.gov.uk/blog/the-inspect-sandboxing-toolkit-scalable-and-secure-ai-agent-evaluations)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C4.1 Runtime Environment Isolation | Mature | gVisor, Kata, Firecracker all production-grade; NVIDIA Container Toolkit patching critical (CVE-2025-23266). Three runC container escape CVEs (Nov 2025) affect every OCI runtime — patch to 1.2.8+. Falco (CNCF graduated) adds eBPF-based runtime detection. CoCo brings pod-level confidential computing to Kubernetes (still experimental for GPU workloads). |
| C4.2 Secure Build & Deployment Pipelines | Mature | OpenSSF Model Signing v1.0 (Apr 2025) fills the model-signing gap; GitHub artifact attestations (Jan 2026) achieve SLSA Build Level 3 with cryptographic provenance. SLSA + cosign + GitHub Actions enable verifiable provenance. Syft handles SBOMs. The [OpenSSF MLSecOps whitepaper](https://openssf.org/blog/2025/08/05/visualizing-secure-mlops-mlsecops-a-practical-guide-for-building-robust-ai-ml-pipeline-security/) (Aug 2025) maps OWASP ML Top 10 to pipeline stages. |
| C4.3 Network Security & Access Control | Mature | Calico and Cilium cover K8s network policies well; K8s v1.35 adds native pod certificates for mTLS. As of March 2026, Cisco Hybrid Mesh Firewall on BlueField DPUs brings 400G line-rate stateful inspection directly onto GPU servers. |
| C4.4 Secrets & Cryptographic Key Management | Mature | Vault, cloud KMS offerings well-established; Vault Radar now scans ML datasets for leaked secrets. Dynamic agent identity patterns published. |
| C4.5 AI Workload Sandboxing & Validation | Emerging | TEE-based confidential inference available (H100 CC) but performance-limited (~4 GB/s CPU-GPU). Confidential Containers (CoCo) standardizes pod-level TEE on Kubernetes but GPU integration is still experimental. Google Confidential GKE Nodes offer managed GPU encryption in-use. SMPC (C4.5.7) remains research-grade. |
| C4.6 Resource Management, Backup & Recovery | Mature | K8s resource quotas, Kueue for batch scheduling, standard backup tooling. Well-understood controls. |
| C4.7 AI Hardware Security | Maturing | MIG provides partition-level isolation but not encryption. H100 CC adds hardware TEE with throughput tradeoffs. The Vera Rubin NVL72 (January 2026) extends confidential computing to rack-scale with near-native performance. GPUHammer underscores the need for ECC memory on all AI accelerators. |
| C4.8 Edge & Distributed AI Security | Emerging | Apple Core ML encryption works but is platform-specific; no universal model encryption standard. Byzantine fault tolerance (C4.8.5) and on-device anti-extraction (C4.8.7) have limited production tooling. |

---

## Open Research Questions

- [x] **What's the maturity of confidential computing for GPU workloads?** — As of early 2026, NVIDIA H100 CC is GA with on-die root of trust, encrypted CPU-GPU transfers, and remote attestation (NRAS), but throughput is limited to ~4 GB/s. The Vera Rubin NVL72 (announced January 2026) extends confidential computing to rack-scale — 72 GPUs, 36 CPUs, and NVLink interconnects form a unified trust domain with end-to-end encryption and near-native performance, a significant leap over H100's per-GPU model. However, the TEE.Fail attack (Oct 2025) showed DDR5 memory bus interposition can break underlying CPU TEEs with <$1K hardware, and GPUHammer demonstrated practical Rowhammer attacks against GDDR6 GPU memory (USENIX Security 2025). The hardware threat surface continues to expand alongside defensive capabilities.
- [x] **How do you isolate multi-tenant GPU workloads without significant performance overhead?** — NVIDIA MIG provides hardware partition-level isolation (up to 7 instances on A100/H100) with dedicated memory, cache, and SMs per tenant. Performance isolation is strong but MIG does not encrypt — separate research showed four side-channel leakage sources bypassing MIG under MPS mode, and GPUHammer showed cross-tenant Rowhammer attacks are practical on GPUs without ECC. Full confidential multi-tenancy requires H100 CC mode (with throughput constraints) or the upcoming Vera Rubin NVL72, which promises rack-scale encryption with near-native performance.
- [ ] **What are the best practices for securing AI inference at the edge with limited compute?** — Apple Core ML offers compile-time model encryption (decrypted only at runtime), but this is platform-specific. Android lacks a native equivalent; teams typically use Android Keystore for key protection with custom encryption wrappers. No universal cross-platform model encryption standard exists yet. The ONNX Server for Open Enclave project provides TEE-based inference but targets server-class hardware.
- [ ] **How should hardware security requirements differ for training vs. inference infrastructure?** — Training requires higher throughput and multi-node coordination (NVLink, InfiniBand), where the NVBleed side-channel and RDMA protocol weaknesses (NeVerMore) are relevant. Inference is more deployable in TEEs due to lower data transfer volumes but faces model extraction risks. Edge inference faces unique physical access threats (BarraCUDA EM side-channel).
- [ ] **How will post-quantum cryptography affect model signing and TEE attestation chains?** — OpenSSF Model Signing v1.0 and Sigstore currently use classical cryptographic primitives. As PQC standards finalize, the model signing and TEE attestation ecosystems will need migration paths.
- [ ] **Can GPU telemetry anomaly detection reliably identify side-channel attacks?** — NVIDIA DCGM exports power, temperature, and error counters, but no published production system uses this telemetry specifically for side-channel detection (C4.7.8).
- [ ] **When will Confidential Containers (CoCo) with GPU support reach production readiness?** — As of March 2026, the CNCF CoCo project supports pod-level confidential computing on Kubernetes via Kata Containers CVMs, with end-to-end attestation including CPU and GPU. NVIDIA's GPU Operator integrates with CoCo for confidential GPU workloads, but the combination is still experimental and not recommended for production. Red Hat OpenShift and Google Confidential GKE Nodes offer managed paths, but full GPU CC on vanilla Kubernetes remains a gap. The answer matters because C4.5.4–C4.5.6 requirements assume TEE-based workload isolation that currently lacks a turnkey K8s solution.

---

## Related Standards & Cross-References

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) — PROTECT function maps to C4.1 (isolation), C4.3 (network), C4.4 (secrets); IDENTIFY covers AI asset inventory
- [NIST IR 8596 — Cyber AI Profile](https://csrc.nist.gov/pubs/ir/8596/iprd) (preliminary draft, Dec 2025) — Maps CSF 2.0 to AI-specific risks including adversarial ML, data poisoning, supply chain integrity
- [NIST SP 800-53 Control Overlays for AI (COSAiS)](https://csrc.nist.gov/Projects/cosais/faqs) — SA-family controls map to C4.2 (build pipelines); SI-family maps to C4.6 (resilience)
- [MITRE ATLAS](https://atlas.mitre.org/) — AML.T0010 (supply chain compromise), AML.T0008 (acquire infrastructure), AML.T0029 (denial of ML service), AML.T0034 (cost harvesting), AML.T0024.002 (model extraction)
- [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) (Jul 2025) — 243 control objectives across 18 domains with formal mappings to ISO 42001 and NIST AI 600-1
- [CIS Controls v8.1](https://www.cisecurity.org/controls/v8) — Control 4 (secure config) maps to C4.1; Control 13 (network defense) maps to C4.3; Control 2 (software inventory) maps to C4.2
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) — AI management systems standard; infrastructure aspects cover secure compute provisioning, deployment controls, operational monitoring
- [ISO/IEC 42005:2025](https://www.iso.org/standard/44545.html) — AI impact assessment guidance (published Apr 2025); complements 42001 for infrastructure failure mode assessment
- [EU AI Act Article 15](https://artificialintelligenceact.eu/section/3-2/) — Accuracy, robustness, cybersecurity requirements for high-risk AI; Article 15(4) requires proportionate measures against model extraction, poisoning, adversarial inputs. **The August 2, 2026 enforcement deadline for high-risk AI systems (Annex III) is now less than five months away** — conformity assessments, technical documentation, and CE marking must be complete by then (penalties up to EUR 35M or 7% of global turnover)
- [OpenSSF MLSecOps Whitepaper](https://openssf.org/blog/2025/08/05/visualizing-secure-mlops-mlsecops-a-practical-guide-for-building-robust-ai-ml-pipeline-security/) (Aug 2025) — Practical guide mapping OWASP ML Top 10 threats to MLOps pipeline stages; introduces the Model Signing Schema (MSS) extending code signing to AI; visualizes layer-by-layer security controls using SLSA, Sigstore, and OpenSSF Scorecard
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/) — supplemented by [CNCF Certified Kubernetes AI Conformance Program](https://www.cncf.io/announcements/2025/11/11/cncf-launches-certified-kubernetes-ai-conformance-program-to-standardize-ai-workloads-on-kubernetes/) (Nov 2025)
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) — Infrastructure-relevant entries on supply chain, model theft, insecure deployment

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C01 Training Data](C01-Training-Data.md) | Training data storage infrastructure | C4.1 runtime isolation protects training data; C4.4 secrets management protects data pipeline credentials; C4.7.4 VRAM zeroing prevents training data leakage between tenants |
| [C03 Model Lifecycle](C03-Model-Lifecycle-Management.md) | Model deployment pipelines | C4.2 build pipelines are the execution layer for C03 deployment; C4.2.2–2.3 artifact signing/admission enforces C03 model signing requirements |
| [C05 Access Control](C05-Access-Control.md) | Infrastructure access management | C4.3 network access control enforces C05 authorization policies; C4.4 secrets management underpins C05 authentication; C4.3.3 admin access implements C05 MFA requirements |
| [C06 Supply Chain](C06-Supply-Chain.md) | Build pipeline integrity | C4.2 pipelines enforce C06 framework scanning; C4.2.1 SBOMs complement C06 AI BOMs; GitHub SLSA Build L3 attestations (Jan 2026) provide verifiable provenance for both chapters; AML.T0010 targets both |
| [C09 Orchestration & Agents](C09-Orchestration-and-Agents.md) | Agent execution isolation | C4.1/C4.5 sandboxing implements C09.3 agent isolation; C4.6 resource quotas enforce C09.1 execution budgets; C4.3 network policies restrict agent egress |
| [C12 Privacy](C12-Privacy.md) | TEEs for confidential processing | C4.5.4–5.7 TEEs and SMPC enable C12 privacy guarantees; C4.7.4 VRAM zeroing prevents PII leakage between tenants |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
