# C6.2 Framework & Library Scanning

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.2.1–6.2.5

## Purpose

AI/ML systems depend on a deep stack of frameworks (PyTorch, TensorFlow, JAX, ONNX Runtime) and supporting libraries (NumPy, SciPy, transformers, tokenizers, CUDA drivers). These dependencies are frequent targets for supply-chain attacks via typosquatting, dependency confusion, and exploitation of known CVEs. This section ensures the framework and library layer is continuously scanned, vulnerability-gated, and monitored at runtime.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.2.1** | **Verify that** CI pipelines run dependency scanners on AI frameworks and critical libraries. | 1 | D/V | **Known CVEs in ML frameworks.** PyTorch, TensorFlow, and ONNX Runtime regularly disclose high-severity vulnerabilities (e.g., CVE-2022-45907 PyTorch arbitrary code execution, multiple TensorFlow CVEs). Unscanned dependencies leave these exploitable. | Confirm that CI configuration (GitHub Actions, GitLab CI, Jenkins) includes a dependency-scanning step that covers Python (pip/conda), C++ native extensions, and CUDA libraries. Tools: Dependabot, Snyk, OSV Scanner, Grype, Trivy. Verify scan results are visible in CI logs and failures block the pipeline. | Most scanners cover PyPI well but may miss vulnerabilities in native extensions, CUDA libraries, or custom C++ ops. Organizations using conda environments should verify their scanner supports conda advisories. |
| **6.2.2** | **Verify that** critical and high-severity vulnerabilities block promotion to production images. | 2 | D/V | **Deployment of containers with known exploitable vulnerabilities.** Without gate enforcement, a container with a critical CVE in PyTorch or a transitive dependency (e.g., Pillow, protobuf) can reach production. | Review CI/CD pipeline configuration for a promotion gate that checks vulnerability scan results. Confirm that critical/high findings (CVSS >= 7.0 or equivalent) prevent the image from being pushed to the production registry. Verify that exceptions require documented approval with a risk acceptance. | Requires clear policy on what constitutes "critical" and "high" — CVSS score, EPSS probability, or vendor severity. False positives in native ML libraries (especially CUDA) can cause friction; organizations need a triage process. |
| **6.2.3** | **Verify that** static code analysis runs on forked or vendored AI libraries. | 2 | D | **Vulnerabilities or backdoors introduced in custom forks.** Organizations frequently fork ML libraries to add custom operators, patch performance issues, or vendor specific versions. These forks diverge from upstream security patches and may introduce new vulnerabilities. | Confirm that forked/vendored repositories are included in SAST tool configuration (Semgrep, CodeQL, Bandit for Python). Verify scan results are reviewed and findings are triaged. Check that forks have a documented policy for merging upstream security patches. | SAST tools have limited coverage for ML-specific vulnerability patterns (e.g., unsafe tensor operations, gradient manipulation). Custom Semgrep rules for ML anti-patterns can help close the gap. |
| **6.2.4** | **Verify that** framework upgrade proposals include a security impact assessment referencing public vulnerability feeds. | 2 | V | **Blind upgrades introducing new vulnerabilities, or stale versions missing critical patches.** Framework upgrades (e.g., PyTorch 1.x to 2.x) can introduce breaking security changes; staying on old versions misses security fixes. | Review change management records for framework upgrades. Confirm each includes: a diff of security advisories between current and target versions, assessment of breaking changes with security impact, and a rollback plan. Cross-reference against NVD, GitHub Security Advisories, and framework-specific security bulletins. | This is a process control. Verification requires access to change management records, not just technical scanning. |
| **6.2.5** | **Verify that** runtime sensors alert on unexpected dynamic library loads that deviate from the signed SBOM. | 3 | V | **Runtime injection of malicious shared libraries.** An attacker with partial system access injects a malicious `.so`/`.dll` that gets loaded by the ML framework at inference time, enabling model theft, data exfiltration, or result manipulation. | Deploy runtime monitoring (Falco, Sysdig, Aqua Runtime Protection, or eBPF-based sensors) configured to alert on `dlopen`/`LoadLibrary` calls that load libraries not listed in the container's SBOM. Verify alerts fire on test injection of an unauthorized library. | Requires mature container security infrastructure. High false-positive potential in ML workloads that dynamically load CUDA kernels, cuDNN, or JIT-compiled operators. Allowlist tuning is essential. Level 3 reflects the operational complexity. |

---

## Related Standards & References

- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [Google OSV Scanner](https://google.github.io/osv-scanner/)
- [Anchore Grype](https://github.com/anchore/grype)
- [Aqua Trivy](https://trivy.dev/)
- [Socket.dev — Supply Chain Security](https://socket.dev/)
- [Semgrep — Custom Rules for ML](https://semgrep.dev/)
- [Falco — Runtime Security](https://falco.org/)
- [PyTorch Security Advisories](https://github.com/pytorch/pytorch/security/advisories)
- [TensorFlow Security Advisories](https://github.com/tensorflow/tensorflow/security/advisories)

---

## Open Research Questions

- How can dependency scanners be extended to cover CUDA/cuDNN native library vulnerabilities that are not tracked in standard CVE databases?
- What SAST rules are most effective for detecting ML-specific code vulnerabilities (unsafe deserialization, gradient manipulation, tensor injection)?
- How should organizations handle the security implications of JIT-compiled operators (e.g., TorchScript, XLA) that generate code at runtime?
