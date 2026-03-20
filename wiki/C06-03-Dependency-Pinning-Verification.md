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

### SLSA v1.1 and ML Build Provenance

SLSA (Supply-chain Levels for Software Artifacts) v1.1, released in 2025, defines four progressive levels (0-3) for build integrity. The framework provides a structured path for ML teams to adopt provenance attestations:

- **SLSA Level 1**: Build provenance exists (e.g., recording which packages were installed during model training).
- **SLSA Level 2**: Builds occur on a hosted, tamper-resistant build service with signed provenance.
- **SLSA Level 3**: Builds run in an isolated, ephemeral environment with non-falsifiable provenance.

Most ML CI/CD tools (Kubeflow Pipelines, MLflow, Weights & Biases) do not natively produce SLSA attestations as of early 2026. However, GitHub Actions and Google Cloud Build both support SLSA Level 3 provenance generation, which can be integrated into ML build workflows with custom configuration. The in-toto framework provides a complementary approach, allowing teams to define a "layout" of expected build steps and verify that each step was performed by an authorized party.

### Hydra Dependency and Systemic ML Ecosystem Risk

Research published in January 2026 identified that Hugging Face models collectively depend on more than 100 Python libraries, with nearly half using the Hydra configuration framework. Critical vulnerabilities in Hydra and other widely-shared dependencies create systemic exposure: a single compromised dependency can affect tens of thousands of models. This reinforces the importance of hash-verified lockfiles and continuous dependency monitoring specifically for ML dependency trees, which tend to be wider and less scrutinized than traditional software dependencies.

### Reproducible Builds: Practical Progress

For inference containers and serving pipelines, reproducible builds are increasingly achievable using tools like `apko` (Chainguard), `ko` (for Go-based serving), and Buildkit with `SOURCE_DATE_EPOCH`. For training pipelines, full reproducibility remains challenging due to GPU floating-point non-determinism, but deterministic data loading and preprocessing pipelines are practical targets for hash-comparison verification.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.3.1** | **Verify that** all package managers enforce version pinning via lockfiles. | 1 | D/V | **Dependency confusion and version substitution attacks.** Without pinning, `pip install` or `conda install` may resolve to a malicious package with the same name on a public registry (dependency confusion) or a compromised newer version. (Alex Birsan 2021 dependency confusion attack affected 35+ companies.) | Confirm that `requirements.txt` uses `==` pinning (not `>=`), or that `pip-compile` / `poetry.lock` / `conda-lock.yml` lockfiles exist and are committed to version control. Verify that CI installs from the lockfile (`pip install -r requirements.txt --no-deps` or equivalent). | Conda environments are especially prone to unpinned transitive dependencies. `conda-lock` addresses this but adoption is low. pip's `--require-hashes` flag provides additional integrity but is rarely used in ML projects. |
| **6.3.2** | **Verify that** immutable digests are used instead of mutable tags in container references. | 1 | D/V | **Tag-mutability attacks.** Container tags (e.g., `pytorch/pytorch:latest`, `nvidia/cuda:11.8-runtime`) can be overwritten to point to a compromised image. Digest-based references (`@sha256:...`) are immutable and tamper-evident. | Audit Dockerfiles, Kubernetes manifests, and CI configurations for container image references. Verify all use `@sha256:` digest pinning rather than `:tag` references. Tools: Conftest/OPA policies, Kyverno admission controllers, or Dockerfile linters (Hadolint). | Digest pinning creates operational overhead for image updates. Organizations should automate digest updates via Renovate or Dependabot with digest-aware configuration. Base images from NVIDIA (CUDA, cuDNN) change frequently, requiring active maintenance. |
| **6.3.3** | **Verify that** expired or unmaintained dependencies trigger automated notifications to update or replace pinned versions. | 2 | D | **Stale dependencies with unpatched vulnerabilities.** Pinning prevents unexpected changes but can also freeze vulnerable versions indefinitely. Dependencies that are unmaintained (no commits in 12+ months, archived repository) pose increasing risk over time. | Confirm that an automated dependency-monitoring tool (Dependabot, Renovate, deps.dev) is configured and actively creating update PRs. Verify that a policy exists for evaluating unmaintained dependencies (e.g., check libraries.io maintenance score, GitHub archive status). Review evidence of acted-upon notifications in the past quarter. | Defining "unmaintained" is subjective. Some ML libraries (e.g., specialized research code) have infrequent but intentional release cycles. Organizations need domain-specific criteria. |
| **6.3.4** | **Verify that** build attestations are retained for a period defined by organizational policy for audit traceability. | 3 | V | **Inability to investigate supply-chain incidents post-facto.** Without retained build attestations, an organization cannot determine what dependencies were used in a specific production build after a supply-chain compromise is discovered. | Verify that CI/CD pipelines generate SLSA provenance attestations or in-toto link metadata for each build. Confirm attestations are stored in a tamper-evident log (e.g., Rekor transparency log, immutable object store) with retention aligned to organizational policy (typically 1-3 years). | SLSA adoption in ML pipelines is still early. Most ML CI/CD setups (Kubeflow Pipelines, MLflow, etc.) do not natively produce SLSA attestations. Custom integration is required. Level 3 reflects this tooling gap. |
| **6.3.5** | **Verify that** reproducible-build checks compare hashes across CI runs to ensure identical outputs. | 3 | D | **Non-deterministic builds masking tampering.** If builds are not reproducible, an attacker can inject modifications that are indistinguishable from normal build variance. Reproducible builds make any tampering detectable via hash comparison. | Run the same build twice in CI and compare output hashes. For model training, this requires deterministic training (fixed seeds, deterministic algorithms). For container builds, use tools like `ko`, `apko`, or Buildkit with `SOURCE_DATE_EPOCH`. Verify that hash mismatches trigger investigation. | ML builds are inherently non-deterministic due to GPU floating-point non-determinism, random initialization, and data shuffling. Reproducibility is achievable for inference containers and preprocessing pipelines but very difficult for training runs. This control is most applicable to the inference/serving layer. |

---

## Related Standards & References

- [SLSA Framework v1.1 (Supply-chain Levels for Software Artifacts)](https://slsa.dev/)
- [in-toto — Software Supply Chain Integrity](https://in-toto.io/)
- [Sigstore/Rekor Transparency Log](https://www.sigstore.dev/)
- [Alex Birsan — Dependency Confusion (2021)](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
- [PEP 708 — Extending the Repository API to Mitigate Dependency Confusion Attacks](https://peps.python.org/pep-0708/)
- [PyTorch torchtriton Dependency Confusion — Aqua Security Analysis](https://www.aquasec.com/blog/pytorch-dependency-confusion-administered-malware/)
- [pip --require-hashes Documentation](https://pip.pypa.io/en/stable/topics/secure-installs/)
- [conda-lock](https://github.com/conda/conda-lock)
- [Renovate Bot — Digest Pinning](https://docs.renovatebot.com/docker/)
- [Hadolint — Dockerfile Linter](https://github.com/hadolint/hadolint)
- [Hydra Dependency Systemic Risk Across Hugging Face Models (2026)](https://www.opensourceforu.com/2026/01/hydra-dependency-creates-systemic-ai-security-risk-across-hugging-face-models/)
- [Chainguard apko — Reproducible Container Builds](https://edu.chainguard.dev/compliance/slsa/what-is-slsa/)

---

## Open Research Questions

- How can reproducible-build principles be extended to GPU-accelerated training pipelines given inherent floating-point non-determinism?
- What is the right retention period for build attestations in regulated AI applications (healthcare, finance, autonomous vehicles)?
- How should SLSA provenance levels be adapted for ML artifacts that include both code and data components?
- How will PEP 708 adoption by pip and other Python installers change the dependency confusion threat landscape for ML-specific internal packages?
- What tooling is needed to generate SLSA Level 2+ attestations natively within ML pipeline orchestrators (Kubeflow, MLflow, Airflow)?
- Given that ML dependency trees are wider and less scrutinized than traditional software, how should organizations prioritize which transitive dependencies receive manual security review?
