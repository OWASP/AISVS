# C4.5 AI Workload Sandboxing & Validation

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Isolate untrusted AI models in secure sandboxes and protect sensitive AI workloads using trusted execution environments (TEEs) and confidential computing technologies. AI systems increasingly execute models from external sources (open-source model hubs, third-party vendors, user-uploaded models). These models can contain arbitrary code (via pickle deserialization, custom operators, or embedded scripts) and must be treated as untrusted. This section addresses both defensive sandboxing of untrusted models and proactive protection of high-value models and data using confidential computing.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.5.1** | Verify that external or untrusted AI models execute in isolated sandboxes. | 1 | D/V | Arbitrary code execution from malicious model files. Pickle deserialization attacks in PyTorch models. Custom TensorFlow ops executing shell commands. Backdoored models from public model hubs. As of March 2026, research from the UK AI Security Institute (SandboxEscapeBench) demonstrates that frontier LLMs can escape misconfigured Docker containers with ~40-50% success rates on moderate-complexity scenarios, reinforcing that plain container isolation is insufficient for agentic AI workloads. | Verify sandboxing technology is deployed (gVisor, Firecracker, Kata Containers, or process-level sandboxing like nsjail). Confirm untrusted models cannot access the host filesystem, network, or other workloads. Test by loading a model that attempts to execute system commands and verify it fails. Validate that GPU passthrough does not expose host-level escape paths -- CVE-2025-23266 (NVIDIAScape, CVSS 9.0) demonstrated a three-line Dockerfile container escape via NVIDIA Container Toolkit's OCI hook, affecting ~37% of cloud environments. Confirm NVIDIA Container Toolkit is v1.17.8+ and GPU Operator v25.3.1+. | This is critical: PyTorch's default serialization (pickle) allows arbitrary code execution on load. HuggingFace Hub has had incidents of uploaded malicious models. SafeTensors format mitigates this for weight loading but does not cover custom model code. Organizations should maintain an approved model registry and sandbox anything not in it. For agentic AI systems that generate and execute code at runtime, hardware-boundary isolation (microVMs) is strongly preferred over software-based containers due to the shared-kernel attack surface. |
| **4.5.2** | Verify that sandboxed workloads have no outbound network connectivity by default, with any required access explicitly defined. | 1 | D/V | Compromised model exfiltrating data (training data, user queries, model weights) to external servers. Reverse shell from a malicious model phoning home. The November 2025 runC vulnerabilities (CVE-2025-31133, CVE-2025-52565, CVE-2025-52881) demonstrated multiple container breakout vectors via symlink replacement, timing attacks, and write redirection -- affecting Docker, Kubernetes, containerd, and CRI-O across all major cloud providers. | Confirm network namespace isolation for sandboxed workloads. Test that DNS resolution and outbound connections fail from within the sandbox. If egress is needed (e.g., for federated inference), verify explicit allowlist with destination and protocol restrictions. Verify runC is patched to 1.2.8+, 1.3.3+, or 1.4.0-rc.3+. Audit container capabilities: drop ALL by default (`--cap-drop=ALL`), apply `no-new-privileges`, never mount Docker sockets or host directories (`/proc`, `/sys`, `/dev`) into sandboxed workloads. | Sandboxed models that need to download additional resources (tokenizers, configuration files) should have these pre-staged before sandbox entry. Use init containers or pre-loading steps to fetch dependencies, then cut network access before model execution begins. The vast majority of real-world container escapes stem from misconfigurations (exposed ports, overly permissive access controls, debug settings in production) rather than novel zero-days -- configuration auditing should be prioritized alongside patching. |
| **4.5.3** | Verify that workload attestation is performed before model loading, ensuring cryptographic proof that the execution environment has not been tampered with. | 2 | D/V | Compromised runtime environment that has been modified to intercept model weights, training data, or inference inputs. Attacker-controlled execution environment presenting itself as legitimate. | Verify remote attestation flow: the workload generates an attestation report (signed by hardware root of trust), and the model loading system validates it against expected measurements before releasing model weights or decryption keys. Test with a modified environment and confirm model loading is refused. | Attestation integrates with TEE platforms: Intel SGX (DCAP attestation), Intel TDX (TD Quote), AMD SEV-SNP (attestation report), or NVIDIA Confidential Computing (GPU attestation). The attestation service must maintain a policy of expected measurements that is updated with each approved deployment. |
| **4.5.4** | Verify that confidential workloads execute within a trusted execution environment (TEE) that provides hardware-enforced isolation, memory encryption, and integrity protection. | 3 | D/V | Host OS or hypervisor compromise accessing model weights or training data in memory. Cloud provider insiders reading GPU memory. Side-channel attacks from co-located workloads. | Verify TEE is active (check hardware capabilities and runtime attestation). Confirm memory encryption is enabled (AMD SEV-SNP: check `dmesg` for SEV status; Intel TDX: verify TD report). Validate that the guest OS sees encrypted memory from the host perspective. | CPU TEEs (SGX enclaves, TDX VMs, SEV-SNP VMs) are relatively mature. GPU TEEs are newer: NVIDIA H100 Confidential Computing mode encrypts GPU memory and PCIe traffic but requires specific driver versions and has a performance overhead of 5-15%. Memory size limitations exist for SGX enclaves (256MB without paging, which is insufficient for large models). |
| **4.5.5** | Verify that confidential inference services prevent model extraction through encrypted computation with sealed model weights and protected execution. | 3 | D/V | Model theft by infrastructure operators, cloud provider insiders, or attackers who have compromised the host. Intellectual property theft of proprietary models worth millions in training compute. | Verify model weights are encrypted at rest and decrypted only inside the TEE after attestation. Confirm that model weights are not accessible from outside the TEE (attempt to read `/proc/<pid>/mem` from the host). Validate that inference inputs and outputs are encrypted in transit to/from the TEE. | This is the core use case for confidential AI inference. Key challenge: large language models (tens of GB) may exceed TEE memory limits. Solutions include model partitioning, encrypted paging, or streaming decryption. NVIDIA CC mode on H100 supports this for GPU-resident models. Performance impact must be benchmarked per workload. |
| **4.5.6** | Verify that orchestration of trusted execution environments includes lifecycle management, remote attestation, and encrypted communication channels. | 3 | D/V | TEE deployment without proper attestation verification. Stale TEE instances running with known vulnerabilities. Unencrypted channels between TEE instances in distributed inference setups. | Review orchestration system (Kubernetes with Confidential Containers, Azure Confidential VMs, Red Hat OpenShift sandboxed containers) for attestation integration. Verify TEE lifecycle includes provisioning, attestation, monitoring, and secure teardown. Confirm inter-TEE communication is encrypted and mutually authenticated. Validate end-to-end attestation covers both CPU TEEs and GPU TEEs when NVIDIA confidential GPUs are in use. | Confidential Containers (CoCo) is a CNCF Sandbox project building Kubernetes-native TEE orchestration, with each Pod encapsulated in its own TEE. As of early 2026, CoCo is developing support for NVIDIA confidential GPUs with end-to-end CPU+GPU attestation. Red Hat OpenShift AI provides production deployment via the sandboxed containers operator. Note: Azure's Confidential Containers preview on AKS is sunsetting in March 2026 -- organizations should evaluate migration paths. Key gap remains: orchestrating multi-node TEE clusters for distributed training is not well supported; most solutions focus on single-node inference. |
| **4.5.7** | Verify that secure multi-party computation (SMPC) enables collaborative AI training without exposing individual datasets or model parameters. | 3 | D/V | Data exposure during collaborative training across organizational boundaries. Requirement to train on combined datasets while maintaining data sovereignty and privacy. | Verify SMPC protocol implementation (secret sharing, garbled circuits, or hybrid approaches). Confirm that no single party can reconstruct the complete dataset or model. Audit communication patterns for information leakage. Validate computational correctness against plaintext baselines. Consider hybrid approaches combining SMPC with federated learning and TEEs for practical performance. | SMPC for ML training is at the research-to-practice boundary. Libraries like CrypTen (Meta), TF Encrypted, and MP-SPDZ exist but have significant performance overhead (100-1000x slower than plaintext training). Practical for small models and specific use cases (healthcare, finance) but not yet viable for large-scale training. As of 2025-2026, hybrid SMPC+federated learning approaches show promise -- recent work on Secure Federated Transfer Learning with enhanced SMPC demonstrates improved model precision while maintaining privacy, outperforming traditional federated learning in healthcare EHR systems. Federated learning with differential privacy remains the more practical alternative for many scenarios, while SMPC research focuses on information-theoretic protocols for larger networks and sub-minute latency benchmarks. |

---

## Implementation Guidance

### Sandbox Technology Selection (2025-2026 State of Practice)

Choosing the right sandboxing technology depends on workload sensitivity, performance requirements, and operational maturity. The three dominant approaches have distinct security/performance tradeoffs:

**Firecracker MicroVMs** provide hardware-level isolation via KVM, with each workload running a dedicated Linux kernel completely separated from the host. Firecracker boots in approximately 125ms with less than 5 MiB of memory overhead per VM, supporting up to 150 VMs per second per host. This is widely regarded as the gold standard for running untrusted AI-generated code in production. AWS Lambda and Fly.io use Firecracker in production at massive scale.

**gVisor** intercepts system calls in user space via its Sentry process before they reach the host kernel, drastically reducing the kernel attack surface to a minimal vetted subset. gVisor imposes 10-30% overhead on I/O-heavy workloads but has fast startup. It is best suited for compute-heavy AI workloads (such as inference) where full VM isolation is not required. Google uses gVisor extensively across GKE and Cloud Run.

**Kata Containers** orchestrate multiple VMMs (Firecracker, Cloud Hypervisor, QEMU) through standard container APIs with native Kubernetes integration. Boot time is approximately 200ms with minimal memory overhead. Kata Containers are ideal for regulated industries requiring zero-trust environments with Kubernetes-native orchestration.

**Google Agent Sandbox**, launched at KubeCon NA 2025 as a CNCF project under Kubernetes SIG Apps, provides a declarative API for managing isolated, stateful sandbox pods on Kubernetes clusters specifically for AI agent workloads.

For production deployments executing untrusted models or AI-generated code, Firecracker microVMs or Kata Containers are recommended. The hardware boundary they provide prevents entire classes of kernel-based attacks that user-space isolation (containers, gVisor) cannot fully address.

### WebAssembly (Wasm) for AI Workload Sandboxing

WebAssembly has emerged as a lightweight sandboxing option for AI workloads, particularly at the edge and for agentic AI workflows. Key developments in 2025-2026:

- **NVIDIA published guidance** on using Wasm (via Pyodide, a CPython port compiled to WebAssembly) to sandbox LLM-generated Python code execution in agentic workflows. The approach shifts code execution from application servers to browser sandboxes, providing two protective layers: execution failure in the restricted runtime and browser-level isolation of any successful exploit.
- **Microsoft Wassette** (August 2025) is a security-oriented runtime that executes WebAssembly Components via Model Context Protocol (MCP), allowing AI agents to autonomously fetch Wasm Components from OCI registries and execute them securely using the Wasmtime runtime.
- **WASI AI** enables Wasm modules to interact with ML models and hardware accelerators, supporting inference at the edge with minimal latency. AWS Lambda now supports Wasm functions as a first-class runtime with 10-40x cold start improvements over containers.
- **wasmCloud** supports distributed ML and AI workloads with Wasm-based isolation.

However, Wasm sandboxing is not without risk. Security researchers have identified potential JIT-compiler vulnerabilities that could be triggered by malicious model files engineered to exploit the inference runtime. Wasm should be treated as a defense-in-depth layer, not the sole isolation mechanism for high-risk workloads.

### Model Format Validation and Pre-Deployment Scanning

The pickle deserialization threat remains one of the most critical attack vectors in the AI supply chain. Research from 2025-2026 underscores that model scanning tools are necessary but insufficient on their own:

**PickleScan Bypass Vulnerabilities (2025):** JFrog Security Research discovered three critical zero-day vulnerabilities (CVE-2025-10155, CVE-2025-10156, CVE-2025-10157, all CVSS 9.3) in PickleScan, the most widely deployed model scanning tool used by platforms including Hugging Face:

- **CVE-2025-10155 (File Extension Bypass):** PickleScan prioritizes file extension checks over content analysis. Renaming malicious pickle files with PyTorch extensions (.bin, .pt) causes PickleScan to attempt PyTorch-specific parsing, fail silently, and return no error -- while PyTorch identifies file types by content and loads the malicious payload successfully.
- **CVE-2025-10156 (CRC Bypass):** Attackers introduce intentional CRC errors in ZIP-archived models. PickleScan (using Python's zipfile module) raises exceptions and fails, while PyTorch's model loader bypasses CRC validation and loads the content.
- **CVE-2025-10157 (Unsafe Globals via Subclasses):** PickleScan checks exact module names against its blocklist, but attackers use subclasses of dangerous imports (e.g., internal asyncio classes). PickleScan marks these as "Suspicious" rather than "Dangerous," failing to block them.

These vulnerabilities were fixed in PickleScan 0.0.31+ (September 2025), but they expose a systemic problem: PickleScan and PyTorch handle files differently, creating exploitable semantic gaps.

**Sonatype PickleScan Vulnerabilities (2025):** Independently, Sonatype discovered four additional CVEs in PickleScan, all fixed in version 0.0.23:

- **CVE-2025-1716:** Unsafe deserialization bypasses static analysis, enabling arbitrary code execution via malicious pip package installation during model loading.
- **CVE-2025-1889:** Hidden pickle files embedded in PyTorch archives with non-standard naming conventions evade detection but are loaded by `torch.load()`.
- **CVE-2025-1944:** ZIP filename tampering causes PickleScan to crash with BadZipFile errors, while PyTorch's lenient ZIP handling loads the malicious payload.
- **CVE-2025-1945:** Modified ZIP flag bits prevent detection of malicious pickle files, though PyTorch deserializes them successfully.

Between the JFrog and Sonatype disclosures, a total of seven distinct PickleScan bypass techniques were documented in 2025 alone, underscoring that blocklist-based scanning is fundamentally fragile against determined adversaries.

**PickleBall (CCS 2025):** Academic research from Brown University introduced PickleBall, a secure deserialization framework that performs fine-grained analysis of pickle bytecode rather than relying on blocklist matching. Evaluated model scanners fail to identify known malicious models, while PickleBall achieves higher detection rates with fewer false positives on benign models.

**SafePickle (February 2026):** A newer approach using robust ML-based detection of malicious pickle models, addressing the limitations of signature-based scanning.

**Recommended defense-in-depth for model validation:**
1. **Prefer safe serialization formats.** Use SafeTensors for model weights wherever possible. SafeTensors stores only raw tensor data with JSON-based headers and eliminates the possibility of arbitrary code execution by design.
2. **Scan all model files in CI/CD.** All model binary files (.bin, .pkl, .pt, .pth, .ckpt) must be scanned using tools like modelscan, picklescan (0.0.31+), or PickleBall. If a scan returns "dangerous," the pipeline must block deployment.
3. **Fail closed.** If an automated model scan fails for any reason (timeout, parsing error, tool crash), immediately quarantine the model and prevent distribution.
4. **Sandbox model loading.** Even scanned models should be loaded inside sandboxed environments, because scanning tools have known bypass vulnerabilities. Scanning reduces risk but does not eliminate it.
5. **Maintain an approved model registry.** Curate an internal registry of validated models with cryptographic signatures. Sandbox anything not in the approved registry.

Approximately 44.9% of model repositories on public hubs still contain pickle-format models, making this a persistent and widespread attack surface. In February 2025, researchers from Reverse Engineering Labs uncovered malicious ML models on Hugging Face that exploited "broken" pickle files to evade platform detection mechanisms and execute reverse shells.

### Container and Sandbox Escape: Recent Incidents and Research (2025-2026)

The AI workload sandboxing threat landscape has shifted significantly, with several high-profile escapes demonstrating that isolation boundaries require constant vigilance:

**NVIDIAScape (CVE-2025-23266, CVSS 9.0, July 2025):** Wiz Research discovered that a three-line Dockerfile could exploit an OCI hook misconfiguration in the NVIDIA Container Toolkit to achieve full root access on the host. The `createContainer` hook trusted unfiltered environment variables, allowing `LD_PRELOAD` injection to load attacker-controlled libraries. Approximately 37% of cloud environments were susceptible. Fixed in NVIDIA Container Toolkit v1.17.8+ and GPU Operator v25.3.1+. This is particularly relevant because virtually all GPU-accelerated AI workloads use this toolkit.

**runC Triple Vulnerability (November 2025):** Three vulnerabilities in runC created container breakout vectors across the entire container ecosystem:
- CVE-2025-31133: Symlink replacement targeting procfs files to bypass maskedPaths protections
- CVE-2025-52565: Timing-based attacks during container initialization bypassing security restrictions
- CVE-2025-52881: Write redirection to critical system files enabling host crashes and full breakouts

These affected Docker, Kubernetes, containerd, and CRI-O. Patched in runC 1.2.8+, 1.3.3+, or 1.4.0-rc.3+.

**N8scape (CVE-2025-68668, CVSS 9.9):** A Pyodide sandbox escape in n8n's Python Code Node allowed authenticated users to execute arbitrary commands on the host. The root cause was a blocklist-based sandbox that could not enumerate every dangerous capability -- attackers used `_pyodide._base.eval_code()` to bypass restrictions. This demonstrates why blocklist-based sandboxing approaches are fundamentally weaker than capability-based or hardware-enforced isolation for AI code execution.

**Agenta-API Sandbox Escape (CVE-2026-27952, CVSS 8.8):** A Python sandbox escape in Agenta-API's custom code evaluator (versions prior to 0.48.1) allowed authenticated users to gain arbitrary code execution, further illustrating the fragility of application-level sandboxing in AI evaluation platforms.

**LLM Sandbox Escape Research (March 2026):** The UK AI Security Institute published SandboxEscapeBench, evaluating frontier LLMs' ability to escape Docker containers across 18 scenarios. Key findings:
- Frontier models achieved ~40-50% success rates on moderate-complexity scenarios (runtime vulnerabilities, multi-step exploitation chains)
- Performance degraded to near-zero on kernel-level exploits requiring deep system reasoning
- All successful escapes exploited known misconfigurations or publicly disclosed CVEs -- no novel vulnerabilities were discovered
- Individual escape attempts cost approximately $1 at current inference pricing, making brute-force economically feasible
- The researchers concluded that "plain Docker isolation" is insufficient for frontier models and recommended hardware-enforced boundaries (microVMs)

These incidents collectively reinforce that for AI workloads executing untrusted code or running untrusted models, microVM-level isolation (Firecracker, Kata Containers) provides a fundamentally stronger security boundary than container-level isolation alone.

### Confidential Computing Performance (2025-2026 Benchmarks)

Recent benchmarking studies have refined performance expectations for confidential AI inference:

- **NVIDIA H100 Confidential Computing** overhead for typical LLM inference queries remains below 5%, with larger models and longer sequences experiencing nearly zero computational overhead within the GPU. The primary performance penalty comes from encrypted data transfers between CPU and GPU via bounce buffers, not from computation itself.
- **NVIDIA Vera Rubin NVL72** (announced for future availability) unlocks rack-scale confidential computing across NVLink, creating a unified security domain spanning 72 Rubin GPUs, 36 Vera CPUs, and interconnects -- addressing the multi-node TEE orchestration gap identified in requirement 4.5.6.
- **Red Hat and NVIDIA** have demonstrated a proof-of-concept for running AI workloads in Confidential Containers (CoCo) with NVIDIA GPU acceleration, providing Kubernetes-native TEE orchestration with GPU support.
- The NVIDIA confidential computing architecture now covers **Rubin, Blackwell, and Hopper GPU families**, with hardware root of trust anchored on-die for attestation.

### Defense-in-Depth for AI Workload Isolation

Production AI workload sandboxing requires layered defenses beyond compute isolation alone:

1. **Isolation boundaries:** Firecracker microVMs or Kata Containers for untrusted workloads; gVisor for lower-risk inference.
2. **Resource limits:** CPU, memory, GPU, and disk quotas to prevent resource exhaustion and noisy-neighbor attacks.
3. **Network controls:** Default-deny egress with proxy-based domain allowlists. Pre-stage all model dependencies before cutting network access.
4. **Permission scoping:** Short-lived credentials, tool-specific access grants, and minimal capability sets.
5. **Model validation:** SafeTensors preference, multi-tool scanning, fail-closed policies.
6. **Continuous monitoring:** Execution tracking, syscall auditing, and anomaly detection within sandboxed environments.

---

## Related Standards & References

- [Confidential Computing Consortium](https://confidentialcomputing.io/) -- Industry standards for TEE-based computing
- [NVIDIA Confidential Computing](https://www.nvidia.com/en-us/data-center/solutions/confidential-computing/) -- GPU TEE documentation
- [Azure Confidential Computing](https://learn.microsoft.com/en-us/azure/confidential-computing/) -- Cloud TEE services
- [Confidential Containers (CoCo)](https://github.com/confidential-containers) -- Kubernetes-native TEE orchestration
- [CrypTen](https://crypten.ai/) -- Meta's SMPC framework for ML
- [NIST IR 8427: Multi-Party Privacy-Enhancing Computation](https://csrc.nist.gov/publications/detail/nistir/8427/final)
- [JFrog: PickleScan Zero-Day Vulnerabilities (2025)](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/) -- CVE-2025-10155, CVE-2025-10156, CVE-2025-10157
- [PickleBall: Secure Deserialization (CCS 2025)](https://arxiv.org/html/2508.15987v1) -- Academic research on secure pickle deserialization
- [SafePickle: ML-based Malicious Model Detection (2026)](https://arxiv.org/html/2602.19818v1) -- Robust detection beyond signature-based scanning
- [NVIDIA: Sandboxing Agentic AI with WebAssembly](https://developer.nvidia.com/blog/sandboxing-agentic-ai-workflows-with-webassembly/) -- Wasm-based AI code sandboxing
- [Microsoft Wassette: Wasm Tools for AI Agents (2025)](https://opensource.microsoft.com/blog/2025/08/06/introducing-wassette-webassembly-based-tools-for-ai-agents/) -- Wasm Components via MCP
- [Google Agent Sandbox (CNCF)](https://northflank.com/blog/how-to-sandbox-ai-agents) -- Kubernetes-native sandbox for AI agents
- [Northflank: AI Agent Sandboxing Guide (2026)](https://northflank.com/blog/how-to-sandbox-ai-agents) -- Production sandboxing comparison
- [Confidential LLM Inference: Performance and Cost Across CPU and GPU TEEs](https://www.arxiv.org/pdf/2509.18886) -- Benchmarking study
- [NVIDIAScape (CVE-2025-23266): Container Escape in NVIDIA Container Toolkit](https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape) -- Three-line Dockerfile escape affecting 37% of cloud environments
- [Sonatype: Bypassing PickleScan -- Four Additional Vulnerabilities (2025)](https://www.sonatype.com/blog/bypassing-picklescan-sonatype-discovers-four-vulnerabilities) -- CVE-2025-1716, CVE-2025-1889, CVE-2025-1944, CVE-2025-1945
- [N8scape: Pyodide Sandbox Escape in n8n (CVE-2025-68668)](https://www.cyera.com/research/n8scape-pyodide-sandbox-escape-9-9-critical-post-auth-rce-in-n8n-cve-2025-68668) -- CVSS 9.9 blocklist bypass
- [SandboxEscapeBench: Quantifying Frontier LLM Capabilities for Container Escape](https://arxiv.org/html/2603.02277) -- UK AISI research on LLM sandbox escape rates
- [Container Escape Vulnerabilities: AI Agent Security for 2026](https://blaxel.ai/blog/container-escape) -- runC CVEs and AI-specific container risks
- [Red Hat: Confidential Containers with NVIDIA GPU Acceleration](https://www.redhat.com/en/blog/ai-meets-security-poc-run-workloads-confidential-containers-using-nvidia-accelerated-computing) -- CoCo + GPU TEE proof of concept
- [Secure Federated Transfer Learning with Enhanced SMPC (2025)](https://www.nature.com/articles/s41598-025-27951-5) -- Hybrid SMPC+FL for privacy-preserving healthcare AI

---

## Open Research Questions

- [ ] What is the practical performance overhead of confidential GPU inference (NVIDIA H100 CC mode) for large language models across different batch sizes? *Partial answer: benchmarks show sub-5% overhead for typical LLM queries, with overhead concentrated in CPU-GPU data transfer rather than computation.*
- [ ] How can model partitioning strategies enable confidential inference for models that exceed single-TEE memory limits? *NVIDIA Vera Rubin NVL72 rack-scale confidential computing may address this for future deployments.*
- [ ] When does SMPC become practical for production ML training -- what model sizes and dataset sizes are feasible today?
- [ ] How should attestation policies handle TEE firmware updates that change expected measurement values without disrupting production inference?
- [ ] Can homomorphic encryption (HE) complement or replace SMPC for specific inference workloads, and what are the size/latency tradeoffs?
- [ ] How reliable are model scanning tools (PickleScan, modelscan) against adversarial evasion, given the seven documented bypass techniques in 2025 (JFrog + Sonatype)? What detection coverage gaps remain after PickleScan 0.0.31?
- [ ] Can WebAssembly-based sandboxing achieve sufficient isolation guarantees for high-risk AI workloads, or does it remain limited to defense-in-depth supplementation?
- [ ] What is the security boundary of WASI AI when used for edge inference -- can malicious model files exploit JIT-compiler bugs to escape the Wasm sandbox?
- [ ] As frontier LLMs demonstrate increasing container escape capabilities (SandboxEscapeBench, March 2026), at what capability threshold should organizations mandate microVM isolation for all agentic AI workloads?
- [ ] How should organizations handle the Azure Confidential Containers AKS preview sunset (March 2026) -- what are the production-ready alternatives for Kubernetes-native confidential AI?

---
