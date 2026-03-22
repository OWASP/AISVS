# C4.2 Secure Build & Deployment Pipelines

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Ensure cryptographic integrity and supply chain security through reproducible builds and signed artifacts. AI systems depend on complex build pipelines that pull model weights, training data, framework dependencies, and custom operators from multiple sources. A compromised build pipeline can inject backdoors into models or serving infrastructure that persist undetected through deployment. This section ensures that every artifact is traceable, verified, and tamper-evident.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.2.1** | Verify that builds are completely automated and produce a software bill of materials (SBOM). | 1 | D/V | Manual build processes introducing untracked dependencies or unauthorized modifications. Lack of visibility into what components are in production. Only 21% of organizations have complete dependency visibility (Datadog DevSecOps 2026), and that gap directly translates into untracked components in CI/CD that adversaries target through build-time injection or dependency confusion. | Confirm CI/CD pipeline automates the full build without manual steps. Verify SBOM generation (SPDX or CycloneDX format) is part of the build. Check SBOM includes ML framework versions, CUDA/cuDNN versions, Python packages, and native libraries. Validate that the SBOM covers AI-specific components: model architecture metadata, training dataset references, and fine-tuning lineage. For Hugging Face-hosted models, consider the [OWASP AIBOM Generator](https://genai.owasp.org/resource/owasp-aibom-generator/) which produces CycloneDX-formatted AI BOMs. | AI builds have unique SBOM challenges: model weights, training data provenance, and custom CUDA kernels are not well represented in standard SBOM formats. **CycloneDX 1.5+** introduced ML-BOM fields (model architecture family, training/inference configuration, dataset references, performance metrics, license information), and **CycloneDX 1.7 (2025)** added patent/IP metadata, citations for data provenance, and enhanced cryptographic transparency. The **OWASP AIBOM project** (targeting v0.1 in late 2025) is assessing both CycloneDX 1.6+ and SPDX 3.0 for AI-system requirements. **SPDX 3.0** includes an AI/ML profile with hyperparameters entries. Consider supplementing standard SBOM with an ML-specific manifest covering model lineage. |
| **4.2.2** | Verify that build artifacts are cryptographically signed with build-origin metadata (source repository, build pipeline, commit hash) that can be independently verified. | 2 | D/V | Artifact tampering between build and deployment. Rogue builds injecting backdoored model-serving code. Lack of provenance making it impossible to trace a production artifact to its source. The **Ultralytics supply chain attack (Dec 2024)** demonstrated this threat: attackers exploited a `pull_request_target` vulnerability in GitHub Actions to inject cryptominer payloads into ultralytics v8.3.41 (60M+ PyPI downloads, 30K+ GitHub stars). The trojanized package was available for ~12 hours before detection, and a subsequent "fix" release (v8.3.42) was also compromised. | Verify artifacts are signed using Sigstore/cosign, Notary, or GPG. Check that SLSA provenance metadata is attached. Validate signatures independently using public keys. Confirm signing occurs in a hardened build environment (not developer laptops). For ML model files specifically, verify adoption of the **[OpenSSF Model Signing (OMS) specification](https://openssf.org/blog/2025/06/25/an-introduction-to-the-openssf-model-signing-oms-specification/)**, which uses a detached signature format covering model weights, configuration files, tokenizers, and datasets as a single verifiable unit. OMS is PKI-agnostic, supporting private enterprise systems, self-signed certificates, bare keys, and keyless signing with public or private Sigstore instances. | SLSA Level 2+ provenance is the target. SLSA v1.1 defines progressive security levels (0-3), each representing stronger controls over the build process. Container images should use cosign with keyless signing via Fulcio/Rekor for transparency log. **OMS solves the large-model signing problem** by employing a detached format that avoids repackaging original content -- the manifest includes file listings with cryptographic hashes and optional annotations for domain-specific fields. Adapting SLSA to AI supply chains requires addressing the long, resource-intensive nature of model training; SLSA provenance for training data and RAG data remains challenging since dynamic data can render signatures outdated rapidly. |
| **4.2.3** | Verify that build artifact signatures and build-origin metadata are validated at deployment admission, and unverified artifacts are rejected. | 2 | D/V | Deploying tampered or unauthorized artifacts to production. Bypassing the build pipeline by pushing images directly to registries. **Malicious pickle models on Hugging Face (Feb 2025)**: researchers found ML models using 7z compression (instead of standard ZIP) to evade Picklescan detection ("NullifAI" technique), containing reverse-shell payloads targeting Windows/Linux/macOS. Some models went undetected for over 8 months. **JFrog discovered 3 zero-day vulnerabilities in Picklescan** that allowed further evasion of Hugging Face's scanning. | Configure admission controllers (Kyverno, OPA Gatekeeper, Sigstore Policy Controller) to enforce signature verification. Test by attempting to deploy an unsigned artifact and confirming rejection. Verify admission policies cover all deployment paths (Kubernetes, serverless, edge). For model serving frameworks, verify that **Seldon Core** (with Istio integration for automatic mTLS and JWT-based RequestAuthentication), **BentoML** (structured APIs with Docker containerization), **KServe**, and **NVIDIA Triton Inference Server** enforce artifact validation before model loading. | Admission control for model weight files is less standardized than container images. Organizations serving models from object storage (S3, GCS) need custom validation hooks. Consider integrating signature checks into model loading code as defense-in-depth. The Hugging Face pickle incidents demonstrate that format-level scanning (Picklescan) is insufficient alone -- deployment admission should combine signature verification, format validation, and sandboxed model loading. The **OpenSSF Secure MLOps whitepaper (Aug 2025)** recommends extending DevOps admission controls to cover datasets and models using SLSA, Sigstore, and OpenSSF Scorecard. |
| **4.2.4** | Verify that builds are reproducible, producing identical output from identical source inputs, enabling independent verification of build integrity. | 3 | D/V | Compromised build infrastructure silently inserting backdoors (Ken Thompson attack). Inability to verify that a production artifact matches its claimed source. The 2025 State of Pipeline Security report documented "Pipeline Parasitism" as a systemic pattern: attackers living off CI/CD using shell injections, over-privileged tokens, invisible Unicode payloads, blockchain C2, and wiper failsafes across multiple major incidents (Kong, tj-actions, GhostAction, Nx, GlassWorm). | Rebuild from the same source commit and compare output hashes. Verify build environment is hermetic (pinned toolchains, no network access during build). Check that non-deterministic elements (timestamps, random seeds) are controlled. For ML serving infrastructure, verify that container images and serving code produce reproducible builds even if model weights themselves are non-deterministic. Validate that all CI/CD workflows use pinned action versions (not mutable tags) and restrict `pull_request_target` trigger usage. | Full reproducibility for ML artifacts is extremely challenging. Model training is inherently non-deterministic on GPUs (floating-point non-associativity, cuDNN algorithm selection). This requirement is more practical for serving infrastructure builds than for model weights. PyTorch `torch.use_deterministic_algorithms(True)` helps but has significant performance penalties and doesn't cover all operations. The Ultralytics incident showed that even "trusted" CI/CD pipelines can be compromised through pull request injection -- hermetic builds with no network access and pinned dependencies are essential but not sufficient without also hardening workflow trigger configurations. |

---

## Implementation Maturity

| Requirement | Maturity | Notes |
|-------------|:---:|-------|
| 4.2.1 Automated builds with SBOM | Mature | CI/CD automation is standard. CycloneDX 1.7 ML-BOM and SPDX 3.0 AI profile provide AI-specific SBOM formats. OWASP AIBOM Generator produces CycloneDX output from HF model references. Gap: only 21% of orgs have complete dependency visibility (Datadog DevSecOps 2026). Model weights, training data provenance, and custom CUDA kernels are still underrepresented in SBOMs. |
| 4.2.2 Cryptographic signing with provenance | Maturing | Sigstore/cosign for containers is production-ready. OpenSSF Model Signing (OMS) spec specifically addresses ML models with detached signatures — NVIDIA signs all NGC models with OMS. SLSA v1.1 defines progressive build security levels. Gap: SLSA provenance for training data and long-running training jobs remains challenging. |
| 4.2.3 Admission control rejecting unsigned artifacts | Maturing | Kyverno, OPA Gatekeeper, and Sigstore Policy Controller enforce container image signature verification. Gap: admission control for model weight files loaded from object storage (S3, GCS, HF Hub) is less standardized — requires custom validation hooks. Picklescan alone is insufficient (NullifAI, JFrog zero-days). |
| 4.2.4 Reproducible builds | Emerging | Practical for serving infrastructure container images. Extremely challenging for GPU-trained model weights due to floating-point non-determinism. `torch.use_deterministic_algorithms(True)` helps but has performance penalties. Hermetic builds with pinned dependencies are essential but insufficient without hardened CI/CD trigger configurations (Ultralytics lesson). |

### Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C04.4 Secrets & Key Management](C04-04-Secrets-Key-Management.md) | Signing key protection | C4.2.2 signing requires HSM/KMS-backed keys (C4.4.4). Signing key compromise undermines the entire artifact verification chain. |
| [C06.1 Pretrained Model Vetting](C06-01-Pretrained-Model-Vetting.md) | Model artifact scanning | C6.1.2 scans imported models for malicious content; C4.2.3 admission control is the deployment-time enforcement that rejects unverified artifacts — both are needed in sequence. |
| [C06.3 Dependency Pinning](C06-03-Dependency-Pinning-Verification.md) | Build reproducibility | C6.3.1 lockfile pinning and C6.3.5 reproducible-build checks complement C4.2.4 — pinned dependencies are a prerequisite for reproducible builds. |
| [C06.7 AI BOM](C06-07-AI-BOM-Model-Artifacts.md) | SBOM/AI BOM generation | C4.2.1 SBOM generation feeds into C6.7 AI BOM lifecycle — CycloneDX ML-BOM and SPDX AI profile provide the format; C6.7 covers signing, completeness, and downstream queryability. |
| [C09.3 Tool & Plugin Isolation](C09-03-Tool-and-Plugin-Isolation.md) | Sandboxed model loading | C4.2.3 admission control catches unverified artifacts at deployment; C9.3.1 sandbox isolation provides defense-in-depth for loading model files that pass admission but may contain novel evasion techniques. |
| [C13 Monitoring & Logging](C13-Monitoring-and-Logging.md) | Build pipeline audit trails | C4.2 build signing and SBOM generation produce artifacts that feed into C13 audit infrastructure. CI/CD audit logs (pipeline execution, artifact promotions) should integrate with C13 SIEM. |

---

## Key Incidents & Case Studies

| Incident | Date | Impact | Relevance |
|----------|------|--------|-----------|
| **Ultralytics PyPI supply chain attack** | Dec 2024 | Trojanized versions 8.3.41-42 of the ultralytics YOLO library (60M+ downloads) delivered XMRig cryptominer via compromised GitHub Actions workflow. Attackers exploited `pull_request_target` to inject malicious code during automated builds, bypassing code review. | Demonstrates need for 4.2.2 (artifact signing), 4.2.3 (admission control), and 4.2.4 (hermetic builds with hardened CI/CD triggers). |
| **Malicious pickle models on Hugging Face** | Feb 2025 | Models using "NullifAI" evasion (7z compression) bypassed Picklescan to deliver reverse-shell payloads. Some persisted undetected for 8+ months. JFrog later found 3 zero-day bypasses in Picklescan itself. | Demonstrates need for 4.2.3 (multi-layered admission control beyond format scanning) and cryptographic signing of model artifacts. |
| **GitHub Actions ecosystem attacks (2025)** | Throughout 2025 | Multiple incidents: tj-actions/changed-files compromise exposed secrets from 23K+ repos; GhostAction, Nx, GlassWorm campaigns used invisible Unicode payloads and blockchain C2. | Demonstrates systemic CI/CD pipeline risk; "Pipeline Parasitism" pattern affecting ML and non-ML projects alike. |

---

## Tooling Landscape (2025-2026)

| Category | Tools | Notes |
|----------|-------|-------|
| **SBOM Generation** | [CycloneDX](https://cyclonedx.org/) (v1.7 with ML-BOM), [SPDX 3.0](https://spdx.dev/) (AI/ML profile), [OWASP AIBOM Generator](https://genai.owasp.org/resource/owasp-aibom-generator/) | CycloneDX ML-BOM is the most mature AI SBOM standard; OWASP AIBOM project assessing gaps |
| **Artifact Signing** | [Sigstore](https://www.sigstore.dev/) (cosign, Fulcio, Rekor), [OpenSSF Model Signing (OMS)](https://openssf.org/blog/2025/06/25/an-introduction-to-the-openssf-model-signing-oms-specification/), [in-toto](https://in-toto.io/) | OMS is purpose-built for ML models; uses detached signatures, PKI-agnostic, Sigstore-compatible |
| **Supply Chain Provenance** | [SLSA v1.1](https://slsa.dev/), [in-toto attestations](https://in-toto.io/), [Witness](https://witness.dev/) | SLSA levels 0-3 with increasing build integrity guarantees |
| **Admission Control** | [Kyverno](https://kyverno.io/), [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/), [Sigstore Policy Controller](https://docs.sigstore.dev/policy-controller/overview/) | Enforce signature verification at Kubernetes deployment time |
| **Model Serving (with security features)** | [Seldon Core](https://www.seldon.io/) (Istio mTLS, JWT auth), [BentoML](https://www.bentoml.com/) (structured APIs, Docker packaging), [NVIDIA Triton](https://developer.nvidia.com/triton-inference-server) (GPU-optimized), [KServe](https://kserve.github.io/) | Seldon + Istio provides automatic mTLS and JWT-based request authentication |
| **Pipeline Security Scanning** | [OpenSSF Scorecard](https://securityscorecards.dev/), [StepSecurity Harden-Runner](https://www.stepsecurity.io/), [Picklescan](https://github.com/mmaitre314/picklescan) (limited -- see evasion incidents) | Scorecard assesses CI/CD security posture; Picklescan insufficient as sole model scanning defense |

---

## Related Standards & References

- [SLSA Framework v1.1](https://slsa.dev/) -- Supply-chain Levels for Software Artifacts, progressive build security levels
- [Sigstore](https://www.sigstore.dev/) -- Keyless signing and transparency for software supply chains
- [OpenSSF Model Signing (OMS) Specification](https://openssf.org/blog/2025/06/25/an-introduction-to-the-openssf-model-signing-oms-specification/) -- Purpose-built signing standard for ML models
- [OpenSSF Secure MLOps Whitepaper (Aug 2025)](https://openssf.org/blog/2025/08/05/visualizing-secure-mlops-mlsecops-a-practical-guide-for-building-robust-ai-ml-pipeline-security/) -- Practical guide for securing ML pipelines with open-source tools
- [NIST SP 800-218: Secure Software Development Framework (SSDF)](https://csrc.nist.gov/publications/detail/sp/800-218/final)
- [CycloneDX ML BOM](https://cyclonedx.org/capabilities/mlbom/) -- ML-specific SBOM extension (stable since v1.5, enhanced in v1.7)
- [OWASP AIBOM Project](https://owasp.org/www-project-aibom/) -- AI Bill of Materials standard under development
- [SPDX 3.0 AI/ML Profile](https://spdx.dev/) -- SBOM specification with AI model support
- [in-toto](https://in-toto.io/) -- Framework for supply chain integrity
- [NIST SP 800-204D: Strategies for Integration of Software Supply Chain Security](https://csrc.nist.gov/publications/detail/sp/800-204d/final)
- [MITRE ATLAS](https://atlas.mitre.org/) -- Adversarial Threat Landscape for AI Systems (14 new agent techniques added 2025)
- [Google AI Supply Chain Security Guidance](https://cloud.google.com/transform/same-same-but-also-different-google-guidance-ai-supply-chain-security/) -- Extending SLSA and provenance to AI artifacts
- [Ultralytics Attack Analysis (PyPI Blog)](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/) -- Detailed post-mortem of ML supply chain compromise
- [PickleBall: Secure Deserialization of ML Models (CCS 2025)](https://arxiv.org/html/2508.15987v1) -- Research on secure pickle deserialization

---

## Open Research Questions

- [ ] How should SBOMs represent model weights, training data dependencies, and fine-tuning lineage? CycloneDX 1.7 ML-BOM and OWASP AIBOM are converging but not yet comprehensive -- gaps remain for RAG data sources, adapter/LoRA lineage, and quantization provenance.
- [ ] What is the practical path to reproducible builds for GPU-trained models given floating-point non-determinism? Current approaches (deterministic algorithms, fixed seeds) incur significant performance penalties and do not cover all operations.
- [ ] How can SLSA provenance be extended to cover the full ML pipeline (data ingestion, preprocessing, training, evaluation, packaging)? SLSA v1.1 does not yet address dynamic data or long-running training jobs natively.
- [ ] What signing infrastructure works well for multi-gigabyte model weight files stored in object storage? The OpenSSF OMS specification (2025) addresses this with detached signatures, but ecosystem adoption and toolchain integration are still early.
- [ ] How can admission control be extended beyond container images to validate model files loaded from object storage (S3, GCS, Hugging Face Hub) at serving time? Current Kubernetes admission controllers only cover container image deployment.
- [ ] Given the demonstrated insufficiency of format-based scanning (Picklescan evasions), what layered defenses should be standard for model artifact validation before deployment?

---
