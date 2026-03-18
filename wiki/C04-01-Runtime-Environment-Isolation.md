# C4.1 Runtime Environment Isolation

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Prevent container escapes and privilege escalation through OS-level isolation primitives. AI workloads -- particularly inference services processing untrusted input and training jobs with access to sensitive data -- present high-value targets. This section ensures that even if an attacker compromises an AI workload process, they cannot escalate privileges, escape the container boundary, or pivot laterally to other infrastructure.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.1.1** | Verify that all AI workloads run with minimal permissions needed on the operating system, by e.g. dropping unnecessary Linux capabilities in case of a container. | 1 | D/V | Privilege escalation from a compromised ML process. Attackers gaining CAP_SYS_ADMIN or CAP_NET_RAW to escape containers or sniff traffic. | Inspect container security contexts / pod specs for `drop: [ALL]` with explicit add-back of only needed capabilities. Run `capsh --print` inside the running container. Verify no containers run as root (UID 0). | Most ML frameworks do not require elevated capabilities. Common exception: some GPU runtimes historically needed CAP_SYS_ADMIN, but modern NVIDIA Container Toolkit works with reduced caps. Ensure GPU device plugin is configured to avoid privileged mode. |
| **4.1.2** | Verify that workloads are protected by technologies limiting exploitation such as sandboxing, seccomp profiles, AppArmor, SELinux or similar, and that the configuration is appropriate. | 1 | D/V | Exploitation of vulnerabilities in ML frameworks (e.g., deserialization bugs in pickle, protobuf parsing flaws) leading to arbitrary code execution. | Check that seccomp profiles are applied (not `unconfined`). Verify AppArmor/SELinux profiles are loaded and enforcing. Audit profile rules to confirm they block dangerous syscalls (e.g., `mount`, `ptrace`, `kexec_load`). | Default Docker seccomp profile blocks ~44 syscalls but may be too permissive for AI workloads. Custom profiles should be tuned -- e.g., ML workloads typically do not need `clone` with `CLONE_NEWUSER`. Consider gVisor or Kata Containers for stronger isolation of untrusted model execution. |
| **4.1.3** | Verify that workloads run with a read-only root filesystem, and that any writable mounts are explicitly defined and hardened with restrictive options that prevent execution and privilege escalation (e.g., noexec, nosuid, nodev). | 2 | D/V | Post-exploitation persistence via dropped binaries or modified system files. Attackers writing malicious shared libraries or cron entries. | Verify `readOnlyRootFilesystem: true` in pod security context. Check that writable volume mounts use `noexec,nosuid,nodev`. Attempt to write to the root filesystem and confirm it fails. Inspect mount options via `mount` or `/proc/mounts`. | AI workloads often need writable `/tmp` or model cache directories. These should be tmpfs mounts with size limits and noexec. HuggingFace Transformers and similar libraries cache models to disk -- ensure cache paths are explicitly defined writable volumes, not the root filesystem. |
| **4.1.4** | Verify that runtime monitoring detects privilege-escalation and container-escape behaviors and automatically terminates offending processes. | 3 | D/V | Active exploitation attempts -- kernel exploits (e.g., Dirty Pipe, runc CVEs), namespace escapes, or privilege escalation via SUID binaries. | Deploy runtime security tools (Falco, Sysdig Secure, Tetragon) and verify detection rules trigger on: unexpected process execution, sensitive file access (`/etc/shadow`, `/proc/*/mem`), namespace manipulation, and raw socket creation. Test with simulated escape scenarios. | Tuning is critical to avoid false positives from legitimate ML operations (e.g., large memory allocations, GPU device access). Falco rules need AI-workload-specific tuning. Automated termination carries risk of killing legitimate long-running training jobs -- consider graduated response (alert -> isolate -> terminate). |
| **4.1.5** | Verify that high-risk AI workloads run in hardware-isolated environments (e.g., TEEs, trusted hypervisors, or bare-metal nodes) only after successful remote attestation. | 3 | D/V | Side-channel attacks from co-tenant workloads on shared hardware. Compromised hypervisor or host OS accessing model weights or training data in memory. | Verify TEE attestation reports (e.g., Intel SGX/TDX attestation, AMD SEV-SNP attestation) before workload deployment. Confirm hardware isolation (dedicated nodes or VM-level isolation). Check attestation verification is integrated into the deployment pipeline. | GPU TEE support is still maturing. NVIDIA Confidential Computing (H100 with AMD SEV-SNP) supports GPU TEE but with performance overhead and limited framework support. Intel TDX and AMD SEV-SNP are more mature for CPU workloads. Attestation infrastructure requires careful key management. |

---

## Related Standards & References

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker) -- Sections on container runtime security
- [NIST SP 800-190: Application Container Security Guide](https://csrc.nist.gov/publications/detail/sp/800-190/final)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) -- Restricted profile
- [Linux capabilities(7) man page](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [Falco default rules for container security](https://falco.org/docs/reference/rules/default-rules/)

---

## Open Research Questions

- [ ] What is the real-world performance overhead of gVisor vs. Kata Containers for GPU-accelerated ML inference workloads?
- [ ] How effective are current seccomp profiles at blocking ML-framework-specific exploitation chains (e.g., pickle deserialization leading to arbitrary syscalls)?
- [ ] Can eBPF-based runtime enforcement (Tetragon, Tracee) provide lower overhead than ptrace-based approaches for high-throughput inference?

---
