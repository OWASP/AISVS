# C6.2 Framework & Library Scanning

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.2.1–6.2.5

## Purpose

AI/ML systems depend on a deep stack of frameworks (PyTorch, TensorFlow, JAX, ONNX Runtime) and supporting libraries (NumPy, SciPy, transformers, tokenizers, CUDA drivers). These dependencies are frequent targets for supply-chain attacks via typosquatting, dependency confusion, and exploitation of known CVEs. This section ensures the framework and library layer is continuously scanned, vulnerability-gated, and monitored at runtime.

---

## Threat Landscape (2024–2026)

The ML framework supply chain has seen a sharp escalation in both vulnerability disclosures and active attacks:

- **CVE-2025-32434 (PyTorch, CVSS 9.3 Critical):** A remote code execution flaw in `torch.load()` that bypasses `weights_only=True` — the very safeguard PyTorch documented as safe for loading untrusted models. All versions prior to 2.6.0 are affected. The vulnerability requires no privileges and no user interaction (CWE-502: Deserialization of Untrusted Data). This CVE undermines a foundational security assumption across the ML ecosystem.
- **CVE-2025-2953 (PyTorch):** A local denial-of-service vulnerability exploitable through crafted inputs.
- **PickleScan bypass trifecta (CVE-2025-10155, CVE-2025-10156, CVE-2025-10157 — all CVSS 9.3 Critical):** JFrog researchers disclosed three zero-day vulnerabilities in PickleScan, the primary tool used to detect malicious payloads in serialized ML models. CVE-2025-10155 exploits a file extension mismatch — renaming a standard pickle file to `.bin` or `.pt` causes PickleScan to skip analysis while PyTorch loads it normally. CVE-2025-10156 introduces intentional CRC errors in ZIP archives that crash PickleScan but are silently ignored by PyTorch. CVE-2025-10157 uses subclass imports (e.g., `asyncio.unix_events` instead of `asyncio`) to bypass the unsafe globals blocklist. All three were fixed in PickleScan 0.0.31 (September 2025). These vulnerabilities highlight a fundamental problem: scanning tools and ML frameworks parse the same files differently, creating exploitable gaps.
- **CVE-2025-23304 (NVIDIA NeMo, High severity):** A remote code execution vulnerability in NVIDIA's NeMo framework caused by unsafe use of `hydra.utils.instantiate()` to load configurations from model metadata. Palo Alto Networks' Unit 42 reported that similar Hydra-based RCE patterns affect multiple AI/ML Python libraries, not just NeMo. Fixed in NeMo 2.3.2 with a new `safe_instantiate` function that validates `_target_` values against an allowlist.
- **ONNX vulnerabilities (CVE-2024-7776, CVE-2024-5187):** Fixed in ONNX v1.17.0; demonstrated that model interchange formats carry their own attack surface beyond the training frameworks.
- **TensorFlow:** Continues to disclose multiple CVEs per release cycle via its dedicated security advisory process, with historical patterns of high-severity issues in custom ops, saved model parsing, and graph execution.

**AI CVE landscape by the numbers:** According to the Trend Micro TrendAI State of AI Security Report, 6,086 unique AI-related CVEs were identified from 2018 through 2025. In 2025 alone, 2,130 AI CVEs were disclosed — a 34.6% year-over-year increase, now representing 4.42% of all CVEs. ML frameworks account for 1,624 of those CVEs (26.7%). Nearly half of scored AI vulnerabilities fall into high or critical severity categories. Agentic AI vulnerabilities surged 255% year-over-year (74 to 263 CVEs), and MCP servers emerged as a new attack surface with 95 CVEs in 2025.

**Typosquatting at scale targeting ML libraries:** In 2024, over 100 malicious PyPI packages were detected impersonating popular ML libraries including PyTorch ("PyToich"), Matplotlib ("Matplotltib"), and Selenium ("selennim"). A separate 2024 campaign published 500 malicious packages in a single wave. By 2025, Sonatype tracked over 454,600 new malicious packages across PyPI, npm, Maven Central, NuGet, and Hugging Face, bringing the cumulative total of known malware to over 1.23 million packages. Supply chain attacks increased an estimated 1,300% from 2020 to 2025, with MLOps pipelines particularly vulnerable because they often bypass normal governance in favor of convenience-driven workflows.

**Regulatory and guidance developments:** The NSA published "AI/ML Supply Chain Risks and Mitigations" in March 2026, framing AI as a supply chain and warning that weaknesses at any layer can propagate across organizations. NIST released the Cybersecurity Framework Profile for AI (NISTIR 8596) in December 2025, mapping CSF 2.0 controls to AI adoption risks. OWASP's LLM Top 10 (2025 edition) elevated "Supply Chain" (LLM03:2025) as a primary risk category for LLM-powered systems. The OWASP Top 10 for web applications (2025 edition) introduced "Software Supply Chain Failures" as the #3 risk category — expanding beyond "Vulnerable and Outdated Components" to cover compromised dependencies, malicious packages, tampered builds, and insecure updates. OWASP also published the Top 10 for Agentic Applications (2026), which further emphasizes supply chain integrity for autonomous, tool-using AI systems.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.2.1** | **Verify that** CI pipelines run dependency scanners on AI frameworks and critical libraries. | 1 | D/V | **Known CVEs in ML frameworks.** PyTorch, TensorFlow, and ONNX Runtime regularly disclose high-severity vulnerabilities (e.g., CVE-2025-32434 PyTorch RCE via `torch.load` with CVSS 9.3, CVE-2022-45907 PyTorch arbitrary code execution, multiple TensorFlow CVEs per release cycle). Unscanned dependencies leave these exploitable. Typosquatting campaigns targeting ML libraries on PyPI (500+ malicious packages in a single 2024 wave) make scanning essential even for initial dependency resolution. | Confirm that CI configuration (GitHub Actions, GitLab CI, Jenkins) includes a dependency-scanning step that covers Python (pip/conda), C++ native extensions, and CUDA libraries. **Recommended tooling (2025-2026):** Trivy (free, covers SCA + containers + SBOM generation from a single CLI), Snyk (commercial, Gartner Magic Quadrant Leader for AST 2025, interfile data flow analysis via DeepCode AI), Dependabot (free, GitHub-native), OSV Scanner, Grype. For defense-in-depth, combine Trivy in CI/CD for fast container and dependency scanning on every commit with Snyk or similar for SAST, automated fix PRs, and centralized dashboard. Verify scan results are visible in CI logs and failures block the pipeline. | Most scanners cover PyPI well but may miss vulnerabilities in native extensions, CUDA libraries, or custom C++ ops. Organizations using conda environments should verify their scanner supports conda advisories. Scanners should be configured to check not just direct dependencies but also transitive dependencies, where many ML vulnerabilities hide (e.g., protobuf, Pillow, flatbuffers). As of 2025, complement dependency scanners with model artifact scanners (ModelScan by ProtectAI) and ensure PickleScan is at version 0.0.31+ to avoid the critical bypass vulnerabilities (CVE-2025-10155/10156/10157). |
| **6.2.2** | **Verify that** critical and high-severity vulnerabilities block promotion to production images. | 2 | D/V | **Deployment of containers with known exploitable vulnerabilities.** Without gate enforcement, a container with a critical CVE in PyTorch (e.g., CVE-2025-32434 allowing RCE) or a transitive dependency (e.g., Pillow, protobuf) can reach production. The NSA's March 2026 AI supply chain guidance explicitly recommends gating deployments on vulnerability scan results. | Review CI/CD pipeline configuration for a promotion gate that checks vulnerability scan results. Confirm that critical/high findings (CVSS >= 7.0 or equivalent) prevent the image from being pushed to the production registry. Verify that exceptions require documented approval with a risk acceptance. Consider supplementing CVSS with EPSS (Exploit Prediction Scoring System) probability scores to prioritize vulnerabilities by real-world exploitability — e.g., CVE-2025-32434 had an EPSS of 1.2% (79th percentile) at disclosure. | Requires clear policy on what constitutes "critical" and "high" — CVSS score, EPSS probability, or vendor severity. False positives in native ML libraries (especially CUDA) can cause friction; organizations need a triage process. Container images for ML workloads are often large (5–15 GB) and contain many transitive dependencies, increasing the baseline number of findings to triage. |
| **6.2.3** | **Verify that** static code analysis runs on forked or vendored AI libraries. | 2 | D | **Vulnerabilities or backdoors introduced in custom forks.** Organizations frequently fork ML libraries to add custom operators, patch performance issues, or vendor specific versions. These forks diverge from upstream security patches and may introduce new vulnerabilities. The 2024 Ultralytics build pipeline compromise demonstrated that even popular ML library build systems can be hijacked to publish malicious versions. | Confirm that forked/vendored repositories are included in SAST tool configuration (Semgrep, CodeQL, Bandit for Python). Verify scan results are reviewed and findings are triaged. Check that forks have a documented policy for merging upstream security patches. Consider adding custom Semgrep rules targeting ML-specific anti-patterns: unsafe `pickle.load`/`torch.load` without validation, unrestricted `eval()` on model config, and deserialization of untrusted model artifacts (CWE-502). | SAST tools have limited coverage for ML-specific vulnerability patterns (e.g., unsafe tensor operations, gradient manipulation). Custom Semgrep rules for ML anti-patterns can help close the gap. The OWASP AI Testing Guide (2026) provides emerging test patterns that may inform custom rule development. Pay special attention to Hydra-based configuration loading patterns — CVE-2025-23304 (NVIDIA NeMo) showed that `hydra.utils.instantiate()` can enable RCE when loading untrusted model configs, and similar patterns exist across multiple ML frameworks. |
| **6.2.4** | **Verify that** framework upgrade proposals include a security impact assessment referencing public vulnerability feeds. | 2 | V | **Blind upgrades introducing new vulnerabilities, or stale versions missing critical patches.** Framework upgrades (e.g., PyTorch 1.x to 2.x) can introduce breaking security changes; staying on old versions misses security fixes. CVE-2025-32434 specifically illustrates the risk of staying on PyTorch < 2.6.0, where a critical RCE is exploitable even with the recommended `weights_only=True` mitigation. | Review change management records for framework upgrades. Confirm each includes: a diff of security advisories between current and target versions, assessment of breaking changes with security impact, and a rollback plan. Cross-reference against NVD, GitHub Security Advisories, framework-specific security bulletins (PyTorch and TensorFlow both maintain dedicated advisory pages), and the NIST AI Cybersecurity Profile (NISTIR 8596) for risk classification. | This is a process control. Verification requires access to change management records, not just technical scanning. Organizations should subscribe to framework-specific advisory feeds (e.g., `pytorch/pytorch/security/advisories`, `tensorflow/tensorflow/security/advisories`) and ML-focused threat intelligence sources. |
| **6.2.5** | **Verify that** runtime sensors alert on unexpected dynamic library loads that deviate from the signed SBOM. | 3 | V | **Runtime injection of malicious shared libraries.** An attacker with partial system access injects a malicious `.so`/`.dll` that gets loaded by the ML framework at inference time, enabling model theft, data exfiltration, or result manipulation. The NSA's March 2026 AI supply chain guidance highlights runtime integrity monitoring as a key control for production AI systems. | Deploy runtime monitoring (Falco, Sysdig, Aqua Runtime Protection, or eBPF-based sensors) configured to alert on `dlopen`/`LoadLibrary` calls that load libraries not listed in the container's SBOM. Verify alerts fire on test injection of an unauthorized library. Generate SBOMs with CycloneDX or SPDX format and sign them as part of CI (see also C6.7 AI BOM requirements). | Requires mature container security infrastructure. High false-positive potential in ML workloads that dynamically load CUDA kernels, cuDNN, or JIT-compiled operators. Allowlist tuning is essential. Level 3 reflects the operational complexity. |

---

## Implementation Guidance

### Choosing a Scanning Strategy for ML Stacks

ML dependency trees are deeper and more heterogeneous than typical web application stacks. A layered scanning approach is recommended:

1. **PyPI/conda layer:** Use Dependabot, Snyk, or Trivy to scan Python packages and their transitive dependencies. Ensure conda-forge and PyPI advisories are both covered.
2. **Container layer:** Scan base images (often NVIDIA CUDA images) with Trivy or Grype. ML container images are large and include system-level libraries (cuDNN, NCCL, OpenSSL) that need their own vulnerability tracking.
3. **Native extension layer:** Custom C++/CUDA ops compiled from source are invisible to package-level scanners. Apply SAST (CodeQL, Semgrep) to these codebases and track them in the SBOM.
4. **Model artifact layer:** Model files themselves can be attack vectors (see CVE-2025-32434). Complement dependency scanning with model artifact scanning tools (e.g., ModelScan by ProtectAI) that detect malicious payloads embedded in serialized models.

### Model Artifact Scanner Limitations and Bypass Risks

As of late 2025, the PickleScan bypass vulnerabilities (CVE-2025-10155/10156/10157) exposed a fundamental architectural challenge: scanning tools and ML frameworks parse serialized model files using different code paths, and attackers can exploit these parsing mismatches to evade detection. Key takeaways for practitioners:

- **Keep scanners pinned to latest versions.** PickleScan 0.0.31+ addresses the known bypasses, but new evasion techniques will emerge. Treat model scanners like antivirus signatures — they need continuous updates.
- **Layer multiple scanning approaches.** ModelScan by ProtectAI uses byte-level content inspection across H5, Pickle, and SavedModel formats. Combining it with PickleScan provides defense-in-depth, since each tool uses a different detection methodology.
- **Validate in isolated environments.** For high-value deployments, load models in a sandboxed environment (container with no network access, restricted filesystem) before promoting to production. This catches payloads that bypass static scanners.
- **Monitor the Hydra configuration surface.** The CVE-2025-23304 pattern (RCE via `hydra.utils.instantiate()` in model metadata) affects multiple frameworks beyond NVIDIA NeMo. Audit any framework that loads configuration from model artifacts — check whether `_target_` values in Hydra configs are validated against an allowlist.

### Integrating EPSS with CVSS for ML Vulnerability Prioritization

CVSS alone can produce alert fatigue in large ML stacks. Combining CVSS severity with EPSS (Exploit Prediction Scoring System) probability helps teams focus on vulnerabilities that are both severe and likely to be exploited in the wild. Several scanning tools (Snyk, Trivy as of 2025) now support EPSS enrichment in their output.

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
- [CVE-2025-32434 — PyTorch torch.load RCE (GHSA-53q9-r3pm-6pq6)](https://github.com/advisories/GHSA-53q9-r3pm-6pq6)
- [OWASP LLM03:2025 — Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
- [MITRE ATLAS — Supply Chain Compromise (AML.T0010)](https://atlas.mitre.org/techniques/AML.T0010)
- [NIST Cybersecurity Framework Profile for AI (NISTIR 8596)](https://csrc.nist.gov/pubs/ir/8596/final)
- [NSA — AI/ML Supply Chain Risks and Mitigations (March 2026)](https://media.defense.gov/2026/Mar/04/2003882809/-1/-1/0/AI_ML_SUPPLY_CHAIN_RISKS_AND_MITIGATIONS.PDF)
- [Sonatype — State of the Software Supply Chain 2026](https://www.sonatype.com/state-of-the-software-chain/2026/open-source-malware)
- [CycloneDX ML BOM](https://cyclonedx.org/capabilities/mlbom/)
- [JFrog — 3 Zero-Day PickleScan Vulnerabilities (CVE-2025-10155/10156/10157)](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)
- [Trend Micro TrendAI — State of AI Security Report (2025)](https://www.trendmicro.com/vinfo/us/security/news/threat-landscape/fault-lines-in-the-ai-ecosystem-trendai-state-of-ai-security-report)
- [NVIDIA NeMo Security Bulletin — CVE-2025-23304](https://nvidia.custhelp.com/app/answers/detail/a_id/5641)
- [Palo Alto Unit 42 — RCE with Modern AI/ML Formats and Libraries](https://unit42.paloaltonetworks.com/rce-vulnerabilities-in-ai-python-libraries/)
- [ProtectAI ModelScan — Model Serialization Attack Protection](https://github.com/protectai/modelscan)
- [OWASP Top 10:2025 — Software Supply Chain Failures (#3)](https://owasp.org/Top10/2025/0x00_2025-Introduction/)
- [OWASP Top 10 for Agentic Applications (2026)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST SSDF — Secure Software Development Framework (SP 800-218)](https://csrc.nist.gov/pubs/sp/800/218/final)

---

## Open Research Questions

- How can dependency scanners be extended to cover CUDA/cuDNN native library vulnerabilities that are not tracked in standard CVE databases?
- What SAST rules are most effective for detecting ML-specific code vulnerabilities (unsafe deserialization, gradient manipulation, tensor injection)?
- How should organizations handle the security implications of JIT-compiled operators (e.g., TorchScript, XLA) that generate code at runtime?
- Can model artifact scanners (e.g., ModelScan) be integrated into standard SCA pipelines to provide unified vulnerability reporting across code dependencies and model files?
- How effective is EPSS-based prioritization for ML-specific CVEs, given that exploit patterns for ML frameworks differ from traditional software vulnerabilities?
- What governance models can bridge the gap between fast-moving MLOps workflows and the rigor expected by frameworks like NIST SSDF (SP 800-218) and the NSA AI supply chain guidance?
- Given that parsing mismatches between scanners and frameworks are a recurring bypass vector (as demonstrated by the PickleScan CVEs), should the ML ecosystem adopt a standardized model file validation specification that both scanners and frameworks implement identically?
- How can organizations systematically discover and mitigate Hydra configuration injection risks across their ML framework stack, particularly as more frameworks adopt Hydra for model metadata loading?
