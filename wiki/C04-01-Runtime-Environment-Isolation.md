# C4.1 Runtime Environment Isolation

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Prevent container escapes and privilege escalation through OS-level isolation primitives. AI workloads -- particularly inference services processing untrusted input and training jobs with access to sensitive data -- present high-value targets. This section ensures that even if an attacker compromises an AI workload process, they cannot escalate privileges, escape the container boundary, or pivot laterally to other infrastructure.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.1.1** | Verify that all AI workloads run with minimal permissions needed on the operating system, by e.g. dropping unnecessary Linux capabilities in case of a container. | 1 | D/V | Privilege escalation from a compromised ML process. Attackers gaining CAP_SYS_ADMIN or CAP_NET_RAW to escape containers or sniff traffic. NVIDIAScape (CVE-2025-23266, CVSS 9.0) demonstrated that NVIDIA Container Toolkit OCI hooks inherit container environment variables, enabling a three-line Dockerfile to achieve full host compromise via LD_PRELOAD injection into the privileged hook process. | Inspect container security contexts / pod specs for `drop: [ALL]` with explicit add-back of only needed capabilities. Run `capsh --print` inside the running container. Verify no containers run as root (UID 0). Verify NVIDIA Container Toolkit is v1.17.8+ and GPU Operator is v25.3.2+ to mitigate CVE-2025-23266. Check that `enable-cuda-compat` hook is disabled if not needed (`features.disable-cuda-compat-lib-hook = true`). | Most ML frameworks do not require elevated capabilities. Common exception: some GPU runtimes historically needed CAP_SYS_ADMIN, but modern NVIDIA Container Toolkit works with reduced caps. Ensure GPU device plugin is configured to avoid privileged mode. **[2025-07]** Wiz estimated ~37% of cloud environments were vulnerable to NVIDIAScape, including major cloud providers offering managed GPU AI services. The vulnerability was reported at Pwn2Own Berlin (May 2025) and patched July 2025. |
| **4.1.2** | Verify that workloads are protected by technologies limiting exploitation such as sandboxing, seccomp profiles, AppArmor, SELinux or similar, and that the configuration is appropriate. | 1 | D/V | Exploitation of vulnerabilities in ML frameworks (e.g., deserialization bugs in pickle, protobuf parsing flaws) leading to arbitrary code execution. November 2025 runC vulnerabilities (CVE-2025-31133) allowed bypassing maskedPaths via /dev/null symlink to procfs, granting arbitrary host file writes across Docker, Kubernetes, containerd, and CRI-O. | Check that seccomp profiles are applied (not `unconfined`). Verify AppArmor/SELinux profiles are loaded and enforcing. Audit profile rules to confirm they block dangerous syscalls (e.g., `mount`, `ptrace`, `kexec_load`). For stronger isolation of untrusted model execution, verify gVisor (RuntimeClass `gvisor`), Kata Containers, or Firecracker microVMs are deployed. | Default Docker seccomp profile blocks ~44 syscalls but may be too permissive for AI workloads. Custom profiles should be tuned -- e.g., ML workloads typically do not need `clone` with `CLONE_NEWUSER`. **[2025-2026 tooling comparison]** gVisor implements ~70-80% of Linux syscalls in a user-space kernel (Go), providing medium isolation with fast startup. Kata Containers provides hardware-level VM isolation with near-complete Linux compatibility. Firecracker microVMs offer the strongest isolation (~5MB overhead, millisecond startup) but lack GPU passthrough support. For GPU workloads needing strong isolation, Kata Containers with NVIDIA GPU Operator is currently the most viable option. gVisor has limited GPU support via device proxy. |
| **4.1.3** | Verify that workloads run with a read-only root filesystem, and that any writable mounts are explicitly defined and hardened with restrictive options that prevent execution and privilege escalation (e.g., noexec, nosuid, nodev). | 2 | D/V | Post-exploitation persistence via dropped binaries or modified system files. Attackers writing malicious shared libraries or cron entries. NVIDIAScape specifically exploited the hook process's working directory being set to the container's root filesystem to load malicious shared objects. | Verify `readOnlyRootFilesystem: true` in pod security context. Check that writable volume mounts use `noexec,nosuid,nodev`. Attempt to write to the root filesystem and confirm it fails. Inspect mount options via `mount` or `/proc/mounts`. | AI workloads often need writable `/tmp` or model cache directories. These should be tmpfs mounts with size limits and noexec. HuggingFace Transformers and similar libraries cache models to disk -- ensure cache paths are explicitly defined writable volumes, not the root filesystem. Read-only root filesystem would have partially mitigated the NVIDIAScape attack vector by preventing the malicious .so from being present in the container's root filesystem layer at hook execution time. |
| **4.1.4** | Verify that runtime monitoring detects privilege-escalation and container-escape behaviors and automatically terminates offending processes. | 3 | D/V | Active exploitation attempts -- kernel exploits (e.g., CVE-2024-1086 netfilter use-after-free, confirmed by CISA in October 2025 as actively exploited in ransomware campaigns by RansomHub and Akira), runC CVEs (CVE-2025-31133), namespace escapes, or privilege escalation via SUID binaries. | Deploy runtime security tools (Falco, Sysdig Secure, Tetragon) and verify detection rules trigger on: unexpected process execution, sensitive file access (`/etc/shadow`, `/proc/*/mem`), namespace manipulation, raw socket creation, and LD_PRELOAD injection into privileged processes. Test with simulated escape scenarios including NVIDIAScape-style environment variable injection. | Tuning is critical to avoid false positives from legitimate ML operations (e.g., large memory allocations, GPU device access). Falco rules need AI-workload-specific tuning. Automated termination carries risk of killing legitimate long-running training jobs -- consider graduated response (alert -> isolate -> terminate). **[2025-2026]** Stanford HAI AI Index Report found publicly reported AI security/privacy incidents rose 56.4% from 2023 to 2024. eBPF-based tools (Tetragon, Tracee) provide kernel-level enforcement with lower overhead than ptrace-based approaches. |
| **4.1.5** | Verify that high-risk AI workloads run in hardware-isolated environments (e.g., TEEs, trusted hypervisors, or bare-metal nodes) only after successful remote attestation. | 3 | D/V | Side-channel attacks from co-tenant workloads on shared hardware. Compromised hypervisor or host OS accessing model weights or training data in memory. | Verify TEE attestation reports (e.g., Intel TDX attestation, AMD SEV-SNP attestation) before workload deployment. Confirm hardware isolation (dedicated nodes or VM-level isolation). Check attestation verification is integrated into the deployment pipeline. For GPU workloads, verify composite attestation across CPU, GPU, NIC/DPU, and storage components. | **[2025-2026 update]** GPU confidential computing has matured significantly. NVIDIA Hopper (H100) supports single-GPU pass-through for confidential compute with AMD SEV-SNP. NVIDIA Blackwell extends this to multi-GPU pass-through and multi-node jobs, with TDISP (Trusted Device Interface Security Protocol) encrypting and integrity-protecting PCIe traffic, reducing overhead vs. bounce buffers. Kata Containers + CNCF Confidential Containers stack provides the Kubernetes-native deployment path: RuntimeClass selection for pod-level isolation, Dynamic Resource Allocation (DRA) for GPU assignment, and CDI for device mapping. Composite attestation across CPU + GPU + NIC/DPU + storage is now required to unlock key release for encrypted model weights. Intel TDX and AMD SEV-SNP are mature for CPU workloads. |

---

## Notable Incidents (2024-2026)

| Date | Incident | Impact | Relevance |
|------|----------|--------|-----------|
| **2025-07** | **NVIDIAScape (CVE-2025-23266)** -- Three-line Dockerfile container escape via NVIDIA Container Toolkit OCI hook LD_PRELOAD injection. CVSS 9.0. Reported at Pwn2Own Berlin May 2025. | ~37% of cloud environments affected (Wiz estimate). Full host compromise enabling cross-tenant data/model theft on shared GPU infrastructure. | Directly validates 4.1.1 (minimal permissions), 4.1.3 (read-only filesystem), 4.1.4 (runtime monitoring for LD_PRELOAD injection). |
| **2025-11** | **runC maskedPaths bypass (CVE-2025-31133)** -- /dev/null symlink to procfs enables arbitrary host file write across Docker, Kubernetes, containerd, CRI-O. | Container escape affecting all major container runtimes. | Validates 4.1.2 (sandboxing beyond basic container isolation), 4.1.4 (runtime detection of symlink manipulation). |
| **2025-10** | **CVE-2024-1086 confirmed in ransomware** -- CISA added to KEV catalog; Linux netfilter use-after-free actively exploited by RansomHub and Akira groups. | Post-compromise privilege escalation on Linux hosts running AI workloads. | Validates 4.1.4 (runtime monitoring) and 4.1.5 (hardware isolation to eliminate shared kernel risk). |
| **2026-Q1** | **OpenClaw AI agent crisis** -- Open-source AI agent (135k+ GitHub stars) with 21,000+ exposed instances, malicious marketplace exploits. | First major AI agent security crisis demonstrating need for agent sandboxing. | Validates 4.1.2 (sandboxing for untrusted code execution by AI agents). |

---

## Tooling & Implementation Landscape (updated 2026-03)

### Isolation Technologies for AI Workloads

| Technology | Isolation Level | GPU Support | Startup Time | Memory Overhead | Best For |
|-----------|----------------|-------------|-------------|-----------------|----------|
| **Standard containers** (Docker/containerd) | Namespace/cgroup (shared kernel) | Full (NVIDIA Container Toolkit) | Fast | Low | Trusted workloads in single-tenant environments |
| **gVisor** | User-space kernel (syscall interception) | Limited (device proxy) | Fast | Medium | Semi-trusted workloads; ~70-80% syscall coverage |
| **Kata Containers** | Hardware VM isolation (KVM) | Full (NVIDIA GPU Operator integration, including confidential containers) | Medium | Higher (~tens of MB/container) | Multi-tenant AI, compliance-heavy workloads, GPU confidential computing |
| **Firecracker microVM** | Hardware VM isolation (minimal VMM) | None (no GPU passthrough) | Extremely fast (milliseconds) | Extremely low (~5MB/microVM) | Untrusted AI agent code execution, CPU-only inference |
| **Confidential Containers** (CoCo) | TEE-backed VM (AMD SEV-SNP / Intel TDX) | NVIDIA Hopper (single-GPU), Blackwell (multi-GPU) | Medium-slow | Higher | High-risk workloads with model/data confidentiality requirements |

### Runtime Security Monitoring

| Tool | Approach | AI Workload Considerations |
|------|----------|---------------------------|
| **Falco** | Kernel module / eBPF syscall monitoring | Requires AI-specific rule tuning to avoid false positives from GPU device access, large memory allocations |
| **Tetragon (Cilium)** | eBPF-based enforcement at kernel level | Lower overhead than ptrace; can enforce policy inline without userspace round-trip |
| **Tracee (Aqua)** | eBPF-based runtime detection | Signature and behavioral detection; supports custom rules for ML-specific patterns |
| **Sysdig Secure** | Kernel module / eBPF with Falco rules | Enterprise features including audit trail and compliance reporting |

### Key NVIDIA GPU Security Components

- **NVIDIA Container Toolkit v1.17.8+**: Patched for NVIDIAScape; supports reduced-capability operation
- **NVIDIA GPU Operator**: Kubernetes-native GPU lifecycle management; supports Kata + Confidential Containers
- **NVIDIA MIG (Multi-Instance GPU)**: Hardware partitioning of A100/H100/B200 GPUs for tenant isolation
- **NVIDIA Confidential Computing**: Hopper (single-GPU TEE), Blackwell (multi-GPU TEE + TDISP PCIe encryption)
- **Container Device Interface (CDI)**: Maps GPU/NIC topology into pods; critical for RDMA and PCIe path optimization

---

## Implementation Maturity Assessment

| Requirement | Maturity | Notes |
|-------------|----------|-------|
| **4.1.1** Minimal permissions | **High** -- Well-understood, tooling mature | Kubernetes Pod Security Standards (Restricted profile) enforce this. NVIDIAScape demonstrated consequences of not enforcing. NVIDIA Container Toolkit now works without privileged mode. |
| **4.1.2** Sandboxing / seccomp | **Medium-High** -- Seccomp/AppArmor mature; advanced isolation depends on workload type | gVisor lacks full GPU passthrough. Kata Containers now has production-ready GPU support via NVIDIA GPU Operator. Firecracker is excellent for CPU-only agent sandboxing. Custom seccomp profiles for ML workloads remain under-documented. |
| **4.1.3** Read-only root filesystem | **High** -- Straightforward to implement | Requires planning for model cache directories. Would have partially mitigated NVIDIAScape. Well-supported in Kubernetes pod security contexts. |
| **4.1.4** Runtime monitoring | **Medium** -- Tools exist but AI-specific tuning is immature | Falco/Tetragon/Tracee all support container escape detection. AI-workload-specific rule sets are community-driven, not standardized. Graduated response (alert/isolate/terminate) requires orchestration integration. |
| **4.1.5** Hardware isolation + attestation | **Medium-Low to Medium** -- Rapidly maturing in 2025-2026 | CPU TEEs (AMD SEV-SNP, Intel TDX) are production-ready. GPU TEE via NVIDIA Hopper is available; Blackwell extends to multi-GPU/multi-node. Composite attestation (CPU+GPU+NIC+storage) is emerging. Kata + CoCo provides the Kubernetes-native path. Performance overhead is decreasing with TDISP but still measurable. |

---

## Related Standards & References

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker) -- Sections on container runtime security
- [NIST SP 800-190: Application Container Security Guide](https://csrc.nist.gov/publications/detail/sp/800-190/final)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) -- Restricted profile
- [Linux capabilities(7) man page](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [Falco default rules for container security](https://falco.org/docs/reference/rules/default-rules/)
- [NIST IR 8596 (Draft) -- Cybersecurity Framework Profile for AI](https://csrc.nist.gov/pubs/ir/8596/iprd) -- December 2025 draft covering AI infrastructure security
- [NIST SP 800-53 Control Overlays for Securing AI Systems (COSAiS)](https://www.nist.gov/news-events/news/2025/12/draft-nist-guidelines-rethink-cybersecurity-ai-era) -- Implementation-level AI controls (in development)
- [CSA AI Controls Matrix (AICM)](https://cloudsecurityalliance.org/blog/2025/09/03/a-look-at-the-new-ai-control-frameworks-from-nist-and-csa) -- 243 control objectives across 18 domains for cloud AI (July 2025, updated October 2025)
- [Wiz Research: NVIDIAScape CVE-2025-23266](https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape) -- Container escape in NVIDIA Container Toolkit
- [NVIDIA + Kata Containers: Trusted AI at GPU Scale](https://superuser.openinfra.org/articles/nvidia-kata-containers-trusted-ai-at-gpu-scale/) -- GPU confidential computing architecture

---

## Open Research Questions

- [ ] What is the real-world performance overhead of gVisor vs. Kata Containers for GPU-accelerated ML inference workloads? *Partial answer (2026): Kata with NVIDIA GPU Operator is production-viable; gVisor GPU support remains limited to device proxy. Firecracker lacks GPU passthrough entirely.*
- [ ] How effective are current seccomp profiles at blocking ML-framework-specific exploitation chains (e.g., pickle deserialization leading to arbitrary syscalls)? *Still open: no published ML-specific seccomp profile benchmarks as of March 2026.*
- [ ] Can eBPF-based runtime enforcement (Tetragon, Tracee) provide lower overhead than ptrace-based approaches for high-throughput inference? *Partial answer (2025-2026): eBPF-based tools enforce at kernel level without userspace round-trip, showing lower overhead. Tetragon inline enforcement is production-ready.*
- [ ] How does composite attestation (CPU + GPU + NIC/DPU + storage) scale across multi-node training clusters? *New question added 2026-03: NVIDIA is working on this with the CoCo community but multi-node attestation chains are not yet standardized.*
- [ ] What is the security impact of TDISP (Trusted Device Interface Security Protocol) on PCIe-level attack vectors for GPU workloads? *New question added 2026-03: Blackwell introduces TDISP for PCIe encryption, but independent security analysis is pending.*

---
