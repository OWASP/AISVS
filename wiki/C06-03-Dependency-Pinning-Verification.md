# C6.3 Dependency Pinning & Verification

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.3.1–6.3.5

## Purpose

ML pipelines often have deep and wide dependency trees — a typical PyTorch project may pull in hundreds of transitive dependencies. Without strict pinning and verification, builds are non-deterministic and vulnerable to dependency-confusion attacks, version-swapping, and silent supply-chain compromises. This section ensures every dependency is pinned to an immutable reference and that builds are reproducible and auditable.

---

## 2025-2026 Landscape Update

### Dependency Confusion Remains a Live Threat in ML

The PyTorch `torchtriton` dependency confusion incident demonstrated how ML-specific internal package names that are not claimed on public registries can be weaponized. An attacker published a malicious `torchtriton` on PyPI that was installed instead of the legitimate internal package, gaining code execution on developer machines and CI systems. This pattern is especially dangerous in ML because teams frequently create internal packages for custom operators, data loaders, and model utilities with names that are not reserved on public registries.

PEP 708 (accepted for Python) extends the Simple Repository API to allow repository operators to indicate that a project "tracks" a project on different repositories, enabling installers to detect when a dependency confusion attack may be occurring. Organizations running private ML package registries should monitor adoption of PEP 708 by pip and other installers.

In September 2025, the GhostAction supply chain attack compromised 327 GitHub users across 817 repositories, exfiltrating 3,325 secrets including PyPI tokens. Stolen PyPI credentials can be used to publish malicious versions of legitimate packages, making hash-verified lockfiles even more critical as a defense layer.

The January 2026 dYdX supply chain attack illustrated a different vector: compromised developer accounts. Threat actors used legitimate publishing credentials to push malicious versions of both the `@dydxprotocol/v4-client-js` npm package (versions 3.4.1, 1.22.1, 1.15.2, 1.0.31) and the `dydx-v4-client` PyPI package (version 1.1.5post1) simultaneously. The npm payload exfiltrated seed phrases and device fingerprints, while the PyPI payload added a Remote Access Trojan using 100 iterations of reverse-string/base64/zlib obfuscation. Socket's threat research team detected the malicious behavior within minutes of publication, but organizations relying on flexible version specifiers (e.g., `>=` or `^`) would have automatically pulled the compromised releases. This attack reinforces that hash-pinned lockfiles are the last line of defense even when maintainer accounts are compromised — and that uv's default behavior of prioritizing internal indexes over PyPI (configurable via `--index-strategy`) provides meaningful dependency confusion protection.

### GlassWorm / ForceMemo: Repository-Level Supply Chain Compromise

In March 2026, the GlassWorm campaign evolved into the ForceMemo attack, compromising over 433 Python projects and packages across GitHub, npm, and VS Code extensions. The attack chain begins with malicious VS Code and Cursor IDE extensions that steal GitHub tokens from developer machines. Attackers then use stolen tokens to force-push obfuscated malware into Python files (`setup.py`, `main.py`, `app.py`) on the default branch of compromised repositories — rebasing on top of legitimate commits while preserving the original author, message, and date. This leaves no pull request trail and is invisible in GitHub's standard UI.

The campaign specifically targeted ML research code, Django applications, Streamlit dashboards, and PyPI packages. The injected payload uses three layers of obfuscation (base64, zlib, XOR with key 134) and retrieves its C2 URL from transaction memos on a Solana wallet address, making traditional IOC blocklists ineffective. Two compromised React Native npm packages (`react-native-international-phone-number`, `react-native-country-select`) had 130,000+ monthly downloads.

For dependency pinning, the key takeaway is that lockfiles alone do not protect against repository-level compromise — if the source itself is tampered with, `pip install` from a cloned repo executes malicious `setup.py` regardless of lockfile state. Defenses include requiring signed commits on protected branches, monitoring force-push events via GitHub audit logs, and validating code integrity in CI before execution (e.g., checking that `setup.py` matches a known hash).

### SLSA v1.2 and ML Build Provenance

SLSA (Supply-chain Levels for Software Artifacts) v1.2, approved in early 2026, expands the framework with a Source Track alongside the existing Build Track. This is a significant evolution — v1.1 only addressed build integrity, while v1.2 now covers the entire pipeline from source code management through artifact production.

**Build Track** (unchanged from v1.1):
- **SLSA Level 1**: Build provenance exists (e.g., recording which packages were installed during model training).
- **SLSA Level 2**: Builds occur on a hosted, tamper-resistant build service with signed provenance.
- **SLSA Level 3**: Builds run in an isolated, ephemeral environment with non-falsifiable provenance.

**Source Track** (new in v1.2):
- **Source Level 2**: Historical verification and provenance documentation — establishing trust in the source's lineage and authenticity.
- **Source Level 3**: Continuous technical control enforcement — actively maintaining and monitoring security measures throughout development.

The Source Track is particularly relevant for ML teams in light of the GlassWorm/ForceMemo attacks: it provides a framework for verifying that source code has not been tampered with before it enters the build pipeline. The in-toto attestation framework serves as the recommended vehicle for expressing both source and build provenance, with Verification Summary Attestations (VSAs) enabling downstream consumers to verify compliance.

Most ML CI/CD tools (Kubeflow Pipelines, MLflow, Weights & Biases) still do not natively produce SLSA attestations as of March 2026. However, GitHub Actions and Google Cloud Build both support SLSA Level 3 provenance generation. The open-source SLSA 3 Container Generator for GitHub Actions generates non-falsifiable provenance for container images built in CI, making Level 3 more accessible for ML serving pipelines.

### Hydra Dependency and Systemic ML Ecosystem Risk

Research published in January 2026 identified that Hugging Face models collectively depend on more than 100 Python libraries, with nearly half using the Hydra configuration framework. Critical vulnerabilities in Hydra and other widely-shared dependencies create systemic exposure: a single compromised dependency can affect tens of thousands of models. This reinforces the importance of hash-verified lockfiles and continuous dependency monitoring specifically for ML dependency trees, which tend to be wider and less scrutinized than traditional software dependencies.

### PyPI Attestations and Trusted Publishers

As of March 2026, PyPI's Sigstore-powered attestation system has reached meaningful adoption: over 50,000 projects use trusted publishing, and 17% of all uploads now include cryptographic attestations verifying build provenance. If a project uses Trusted Publishing with the canonical GitHub Action (`pypa/gh-action-pypi-publish`), attestations are generated and uploaded automatically — no configuration changes needed. This is a significant shift for ML package consumers: you can now verify that a package was built from a specific source commit on a specific CI platform, not just that it was uploaded by an authorized user.

For ML teams consuming large dependency trees, attestation verification adds a layer of assurance beyond hash pinning. PyPI has also deployed complementary protections including typosquatting detection during project creation, phishing domain warnings, and ZIP file hardening. Over 52% of active PyPI users now have non-phishable 2FA (hardware keys or WebAuthn) enabled.

### Python Lockfile Standardization: PEP 751 and uv

PEP 751 was accepted in March 2025, introducing `pylock.toml` as a standardized, cross-tool lockfile format for Python. This brings Python in line with JavaScript (`package-lock.json`), Rust (`Cargo.lock`), and Go (`go.sum`), which have long had standardized lock formats. The `pylock.toml` format records exact dependency versions, file hashes, and installation sources in a TOML file that is both human-readable and machine-parseable. Adoption has accelerated as of early 2026: pip 25.1 ships a native `pip lock` command that outputs PEP 751-compliant lockfiles, PDM 2.24.0 exports to `pylock.toml` (with plans to migrate away from its proprietary `pdm.lock` format entirely), pipenv supports it natively, and uv supports it as an import/export format. pip-audit 2.9.0 added vulnerability scanning for `pylock.toml` files, automatically discovering `pylock.*.toml` alongside `pyproject.toml` — meaning security tooling now works directly against the standardized format. pip-tools maintainers are also exploring integration.

Speaking of uv — Astral's Rust-based Python package manager has seen rapid adoption in ML projects due to its speed and security defaults. The `uv.lock` file captures the full transitive dependency tree with cross-platform pinning (different versions for different OS/architecture combinations), and uv will error if the lockfile does not match `pyproject.toml`, preventing silent dependency drift. The `uv-secure` companion tool specifically audits locked dependencies for known vulnerabilities. As of March 2026, uv (v0.10.9+) supports native CycloneDX v1.5 SBOM export via `uv export --format cyclonedx1.5`, producing a JSON-encoded Software Bill of Materials that is directly consumable by security scanning tools, vulnerability databases, and SCA platforms. Snyk contributed the CycloneDX export support upstream through a direct partnership with Astral, ensuring first-class integration between uv lockfiles and downstream security tooling. uv v0.10.11 also added SBOM attestations to its published Docker images, and the binary itself embeds SBOM via cargo-auditable. For ML teams, this means the full chain from lockfile to container image now has machine-readable provenance.

### 2025–2026 Supply Chain Attack Escalation

The volume and sophistication of supply chain attacks targeting Python and npm ecosystems escalated sharply through 2025 and into 2026. Software supply chain attacks doubled in 2025, with global losses reaching $60 billion. In December 2025 alone, 1,228 unique malicious packages were tracked across npm and PyPI. Attack techniques include multi-stage malware with ZLib/Base64 obfuscation, domain generation algorithms for C2 communication, and cross-platform persistence targeting Chrome directories on Windows, Linux, and macOS.

A particularly concerning pattern emerged: threat actors are reusing identical attack infrastructure across ecosystems. The `graphalgo` package on PyPI (published June 2025) and the `express-cookie-parser` package on npm shared the same obfuscation techniques and C2 infrastructure, suggesting coordinated campaigns rather than isolated incidents. Between July 2025 and January 2026, 128 "phantom packages" accumulated over 121,000 downloads before detection.

The npm ecosystem responded to escalating attacks — notably the Shai-Hulud 2.0 worm campaign — by revoking long-lived authentication tokens in favor of short-lived tokens and trusted publishing. npm now supports provenance attestation via Sigstore, though adoption is not yet mandatory and many popular packages still lack provenance statements. There is growing pressure to require attestation for high-impact packages, similar to how PyPI's trusted publisher model has gained traction.

One practical defensive finding: research indicates that implementing a 7–14 day waiting period before accepting new package versions prevents roughly 80% of these supply chain attacks, since most malicious packages are detected and removed within that window. This "quarantine period" approach complements hash-verified lockfiles and is straightforward to implement in ML CI/CD pipelines.

### CycloneDX ML-BOM and AI Bill of Materials

CycloneDX v1.5+ supports `machine-learning-model` as a component type, enabling ML-BOM (Machine Learning Bill of Materials) that tracks not just code dependencies but also training datasets, model architectures, and deployment configurations. This goes beyond traditional SBOM by capturing the unique supply chain components of ML systems — dataset provenance, pre-trained model origins, and fine-tuning lineage.

The OWASP AIBOM project (targeting v0.1 in late 2025) is assessing how well existing formats like CycloneDX 1.6 and SPDX 3.0 address AI-system requirements and where extensions are needed. For teams implementing requirement 6.3.4, generating a CycloneDX ML-BOM alongside SLSA provenance attestations provides the most comprehensive audit trail currently available.

### Reproducible Builds: Practical Progress

For inference containers and serving pipelines, reproducible builds are increasingly achievable. The Melange/apko pipeline (Chainguard) builds APK packages from source with declarative recipes, then assembles minimal OCI images — creating a fully traceable build chain from source to container. `ko` handles Go-based serving with no Dockerfile needed, while BuildKit respects `SOURCE_DATE_EPOCH` for timestamp normalization. Nix flakes offer another deterministic approach, generating minimal images with integrated SBOM and SLSA provenance support. For training pipelines, full reproducibility remains challenging due to GPU floating-point non-determinism, but deterministic data loading and preprocessing pipelines are practical targets for hash-comparison verification.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.3.1** | **Verify that** all package managers enforce version pinning via lockfiles. | 1 | D/V | **Dependency confusion and version substitution attacks.** Without pinning, `pip install` or `conda install` may resolve to a malicious package with the same name on a public registry (dependency confusion) or a compromised newer version. The Alex Birsan 2021 dependency confusion attack affected 35+ companies. In 2025, 1,228 malicious packages were tracked on PyPI/npm in December alone. The January 2026 dYdX attack demonstrated that even compromised maintainer accounts can be mitigated by lockfiles — malicious versions pushed to npm and PyPI would not have been pulled by projects using hash-pinned lockfiles. The March 2026 GlassWorm/ForceMemo campaign compromised 433+ Python repositories via force-pushed malicious code, demonstrating that lockfiles must be complemented by source integrity controls (signed commits, force-push monitoring) to protect against repository-level tampering. | Confirm that `requirements.txt` uses `==` pinning (not `>=`), or that `pip-compile` / `poetry.lock` / `uv.lock` / `conda-lock.yml` / `pylock.toml` (PEP 751) lockfiles exist and are committed to version control. As of 2026, `pip lock` (pip 25.1+) generates PEP 751-compliant lockfiles natively. Verify that CI installs from the lockfile (`pip install -r requirements.txt --no-deps`, `uv sync --frozen`, or equivalent). Run `pip-audit` (v2.9.0+ scans `pylock.toml` directly) or `uv-secure` against the lockfile to check for known vulnerabilities in pinned versions. For repository integrity, verify that protected branches require signed commits and that force-push events trigger alerts in GitHub audit logs. | Conda environments are especially prone to unpinned transitive dependencies. `conda-lock` addresses this but adoption remains low. pip's `--require-hashes` flag provides additional integrity but is rarely used in ML projects. As of 2026, `uv` provides cross-platform lockfiles with hash verification by default, and its `--index-strategy` flag prioritizes internal indexes over PyPI to mitigate dependency confusion. PEP 751's `pylock.toml` now has broad tool support: pip 25.1 (native), PDM 2.24.0 (export, migrating from `pdm.lock`), pipenv (native), uv (import/export). Consider a 7–14 day quarantine on new package versions — research shows this prevents ~80% of supply chain attacks. The GlassWorm campaign shows that even pinned lockfiles do not protect against malicious `setup.py` injected directly into the repository — CI pipelines should validate entry-point file hashes before execution. |
| **6.3.2** | **Verify that** immutable digests are used instead of mutable tags in container references. | 1 | D/V | **Tag-mutability attacks.** Container tags (e.g., `pytorch/pytorch:latest`, `nvidia/cuda:11.8-runtime`) can be overwritten to point to a compromised image. Digest-based references (`@sha256:...`) are immutable and tamper-evident. | Audit Dockerfiles, Kubernetes manifests, and CI configurations for container image references. Verify all use `@sha256:` digest pinning rather than `:tag` references. Tools: Conftest/OPA policies, Kyverno admission controllers, or Dockerfile linters (Hadolint). | Digest pinning creates operational overhead for image updates. Organizations should automate digest updates via Renovate or Dependabot with digest-aware configuration. Base images from NVIDIA (CUDA, cuDNN) change frequently, requiring active maintenance. |
| **6.3.3** | **Verify that** expired or unmaintained dependencies trigger automated notifications to update or replace pinned versions. | 2 | D | **Stale dependencies with unpatched vulnerabilities.** Pinning prevents unexpected changes but can also freeze vulnerable versions indefinitely. Dependencies that are unmaintained (no commits in 12+ months, archived repository) pose increasing risk over time. The January 2026 Hydra research demonstrated that a single widely-shared dependency can create systemic exposure across tens of thousands of Hugging Face models. | Confirm that an automated dependency-monitoring tool (Dependabot, Renovate, deps.dev) is configured and actively creating update PRs. Run `pip-audit` in CI to flag known CVEs in pinned versions. Verify that a policy exists for evaluating unmaintained dependencies (e.g., check libraries.io maintenance score, GitHub archive status, OpenSSF Scorecard). Review evidence of acted-upon notifications in the past quarter. For ML-specific dependencies, verify monitoring covers model-serving frameworks (e.g., Triton, TorchServe) and data pipeline libraries. | Defining "unmaintained" is subjective. Some ML libraries (e.g., specialized research code) have infrequent but intentional release cycles. Organizations need domain-specific criteria. Note that Dependabot can auto-merge updates without human review — the eslint-config-prettier npm incident showed how this amplifies compromised-dependency impact across 14,000+ downstream packages. Consider requiring human approval for ML-critical dependency updates. |
| **6.3.4** | **Verify that** build attestations are retained for a period defined by organizational policy for audit traceability. | 3 | V | **Inability to investigate supply-chain incidents post-facto.** Without retained build attestations, an organization cannot determine what dependencies were used in a specific production build after a supply-chain compromise is discovered. U.S. Executive Order 14028 and Europe's Cyber Resilience Act both require verifiable provenance for software supplied to government/regulated sectors. | Verify that CI/CD pipelines generate SLSA provenance attestations or in-toto link metadata for each build. With SLSA v1.2 (approved 2026), also evaluate Source Track compliance (Level 2 for historical provenance, Level 3 for continuous controls). For Python packages, confirm that PyPI Trusted Publishing with Sigstore attestations is enabled (17% of PyPI uploads include attestations as of 2026). Generate CycloneDX ML-BOM or SPDX SBOM alongside build provenance — uv v0.10.9+ exports CycloneDX v1.5 SBOMs natively via `uv export --format cyclonedx1.5`. Confirm attestations are stored in a tamper-evident log (e.g., Rekor transparency log, immutable object store) with retention aligned to organizational policy (typically 1-3 years). | SLSA v1.2's new Source Track addresses a gap highlighted by the GlassWorm/ForceMemo attacks: verifying source integrity before it enters the build pipeline. Most ML CI/CD setups (Kubeflow Pipelines, MLflow, etc.) still do not natively produce SLSA attestations, but the SLSA 3 Container Generator for GitHub Actions simplifies container provenance. CycloneDX v1.5+ supports `machine-learning-model` as a component type for ML-BOM. uv's native CycloneDX export (contributed by Snyk) and SBOM-attested Docker images (v0.10.11+) reduce the integration burden for ML teams. The OWASP AIBOM project continues work on extending BOM standards for AI-specific supply chain components. |
| **6.3.5** | **Verify that** reproducible-build checks compare hashes across CI runs to ensure identical outputs. | 3 | D | **Non-deterministic builds masking tampering.** If builds are not reproducible, an attacker can inject modifications that are indistinguishable from normal build variance. Reproducible builds make any tampering detectable via hash comparison. | Run the same build twice in CI and compare output hashes. For model training, this requires deterministic training (fixed seeds, deterministic algorithms). For container builds, use tools like `ko`, `apko`, or Buildkit with `SOURCE_DATE_EPOCH`. Verify that hash mismatches trigger investigation. | ML builds are inherently non-deterministic due to GPU floating-point non-determinism, random initialization, and data shuffling. Reproducibility is achievable for inference containers and preprocessing pipelines but very difficult for training runs. This control is most applicable to the inference/serving layer. |

---

## Related Standards & References

- [SLSA Framework v1.2 (Supply-chain Levels for Software Artifacts)](https://slsa.dev/spec/v1.2/)
- [in-toto — Software Supply Chain Integrity](https://in-toto.io/)
- [Sigstore/Rekor Transparency Log](https://www.sigstore.dev/)
- [Alex Birsan — Dependency Confusion (2021)](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
- [PEP 708 — Extending the Repository API to Mitigate Dependency Confusion Attacks](https://peps.python.org/pep-0708/)
- [PEP 751 — A File Format to Record Python Dependencies (pylock.toml)](https://peps.python.org/pep-0751/)
- [PyTorch torchtriton Dependency Confusion — Aqua Security Analysis](https://www.aquasec.com/blog/pytorch-dependency-confusion-administered-malware/)
- [PyPI Sigstore-Powered Attestations — General Availability](https://blog.sigstore.dev/pypi-attestations-ga/)
- [PyPI 2025 Year in Review — Trusted Publishers and Attestation Statistics](https://blog.pypi.org/posts/2025-12-31-pypi-2025-in-review/)
- [pip --require-hashes Documentation](https://pip.pypa.io/en/stable/topics/secure-installs/)
- [pip-audit — Python Dependency Vulnerability Auditing](https://github.com/pypa/pip-audit)
- [uv — Fast Python Package Manager (Astral)](https://github.com/astral-sh/uv)
- [uv-secure — Security Auditing for uv Lockfiles](https://pypi.org/project/uv-secure/)
- [conda-lock](https://github.com/conda/conda-lock)
- [CycloneDX ML-BOM — Machine Learning Bill of Materials](https://cyclonedx.org/capabilities/mlbom/)
- [OWASP AIBOM Project](https://owasp.org/www-project-aibom/)
- [Renovate Bot — Digest Pinning](https://docs.renovatebot.com/docker/)
- [Hadolint — Dockerfile Linter](https://github.com/hadolint/hadolint)
- [Hydra Dependency Systemic Risk Across Hugging Face Models (2026)](https://www.opensourceforu.com/2026/01/hydra-dependency-creates-systemic-ai-security-risk-across-hugging-face-models/)
- [Open Source Supply Chain Threats: December 2025 in Review](https://www.getsafety.com/blog-posts/open-source-supply-chain-threats-december-2025)
- [Chainguard apko — Reproducible Container Builds](https://edu.chainguard.dev/compliance/slsa/what-is-slsa/)
- [NIST AI 600-1 — Generative AI Risk Management Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [dYdX npm/PyPI Supply Chain Attack Analysis — Socket (January 2026)](https://socket.dev/blog/malicious-dydx-packages-published-to-npm-and-pypi)
- [Python Tools Adopting pylock.toml (PEP 751) — Socket (April 2025)](https://socket.dev/blog/pylock-toml-standard-adoption)
- [SLSA 3 Container Generator for GitHub Actions](https://github.com/slsa-framework/slsa-github-generator)
- [Nix Flakes for Reproducible Container Builds](https://debugg.ai/resources/no-more-dockerfiles-reproducible-secure-container-builds-nix-buildpacks-apko-2025)
- [GlassWorm/ForceMemo: Force-Push Supply Chain Attack on Python Repos — The Hacker News (March 2026)](https://thehackernews.com/2026/03/glassworm-attack-uses-stolen-github.html)
- [ForceMemo: Python Repositories Compromised via Account Takeover — StepSecurity](https://www.stepsecurity.io/blog/forcememo-hundreds-of-github-python-repos-compromised-via-account-takeover-and-force-push)
- [SLSA v1.2 Specification — What's New (Source Track)](https://slsa.dev/spec/v1.2/whats-new)
- [Snyk and uv Partnership — Native CycloneDX SBOM Export](https://snyk.io/blog/snyk-uv-partnership/)
- [npm Trusted Publishing and Provenance Attestation](https://docs.npmjs.com/trusted-publishers/)

---

## Open Research Questions

- How can reproducible-build principles be extended to GPU-accelerated training pipelines given inherent floating-point non-determinism?
- What is the right retention period for build attestations in regulated AI applications (healthcare, finance, autonomous vehicles)?
- Now that SLSA v1.2 includes a Source Track, how should ML teams implement source-level provenance for training data pipelines and model configuration files — not just code?
- How will PEP 708 adoption by pip and other Python installers change the dependency confusion threat landscape for ML-specific internal packages?
- What tooling is needed to generate SLSA Level 2+ attestations natively within ML pipeline orchestrators (Kubeflow, MLflow, Airflow)?
- Given the GlassWorm/ForceMemo attacks, should ML projects require commit signing and force-push protection as baseline controls, and how should CI pipelines validate source integrity before executing `setup.py` or build scripts?
- Given that ML dependency trees are wider and less scrutinized than traditional software, how should organizations prioritize which transitive dependencies receive manual security review?
- As PyPI attestation adoption grows beyond 17%, should ML projects require attestation verification as a mandatory gate in CI/CD pipelines?
- How should the OWASP AIBOM standard extend CycloneDX ML-BOM to capture training data provenance, fine-tuning lineage, and adapter/LoRA dependencies?
- What is the optimal quarantine period for new ML-specific package versions, given that ML packages often have legitimate rapid release cycles for bug fixes?
