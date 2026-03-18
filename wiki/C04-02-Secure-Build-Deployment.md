# C4.2 Secure Build & Deployment Pipelines

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Ensure cryptographic integrity and supply chain security through reproducible builds and signed artifacts. AI systems depend on complex build pipelines that pull model weights, training data, framework dependencies, and custom operators from multiple sources. A compromised build pipeline can inject backdoors into models or serving infrastructure that persist undetected through deployment. This section ensures that every artifact is traceable, verified, and tamper-evident.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.2.1** | Verify that builds are completely automated and produce a software bill of materials (SBOM). | 1 | D/V | Manual build processes introducing untracked dependencies or unauthorized modifications. Lack of visibility into what components are in production. | Confirm CI/CD pipeline automates the full build without manual steps. Verify SBOM generation (SPDX or CycloneDX format) is part of the build. Check SBOM includes ML framework versions, CUDA/cuDNN versions, Python packages, and native libraries. | AI builds have unique SBOM challenges: model weights, training data provenance, and custom CUDA kernels are not well represented in standard SBOM formats. CycloneDX ML BOM extension is emerging but not yet widely adopted. Consider supplementing SBOM with an ML-specific manifest covering model lineage. |
| **4.2.2** | Verify that build artifacts are cryptographically signed with build-origin metadata (source repository, build pipeline, commit hash) that can be independently verified. | 2 | D/V | Artifact tampering between build and deployment. Rogue builds injecting backdoored model-serving code. Lack of provenance making it impossible to trace a production artifact to its source. | Verify artifacts are signed using Sigstore/cosign, Notary, or GPG. Check that SLSA provenance metadata is attached. Validate signatures independently using public keys. Confirm signing occurs in a hardened build environment (not developer laptops). | SLSA Level 2+ provenance is the target. Container images should use cosign with keyless signing via Fulcio/Rekor for transparency log. Model weight files should also be signed, but tooling for signing large binary blobs (multi-GB model files) is less mature than container image signing. |
| **4.2.3** | Verify that build artifact signatures and build-origin metadata are validated at deployment admission, and unverified artifacts are rejected. | 2 | D/V | Deploying tampered or unauthorized artifacts to production. Bypassing the build pipeline by pushing images directly to registries. | Configure admission controllers (Kyverno, OPA Gatekeeper, Sigstore Policy Controller) to enforce signature verification. Test by attempting to deploy an unsigned artifact and confirming rejection. Verify admission policies cover all deployment paths (Kubernetes, serverless, edge). | Admission control for model weight files is less standardized than container images. Organizations serving models from object storage (S3, GCS) need custom validation hooks. Consider integrating signature checks into model loading code as defense-in-depth. |
| **4.2.4** | Verify that builds are reproducible, producing identical output from identical source inputs, enabling independent verification of build integrity. | 3 | D/V | Compromised build infrastructure silently inserting backdoors (Ken Thompson attack). Inability to verify that a production artifact matches its claimed source. | Rebuild from the same source commit and compare output hashes. Verify build environment is hermetic (pinned toolchains, no network access during build). Check that non-deterministic elements (timestamps, random seeds) are controlled. | Full reproducibility for ML artifacts is extremely challenging. Model training is inherently non-deterministic on GPUs (floating-point non-associativity, cuDNN algorithm selection). This requirement is more practical for serving infrastructure builds than for model weights. PyTorch `torch.use_deterministic_algorithms(True)` helps but has significant performance penalties and doesn't cover all operations. |

---

## Related Standards & References

- [SLSA Framework](https://slsa.dev/) -- Supply-chain Levels for Software Artifacts
- [Sigstore](https://www.sigstore.dev/) -- Keyless signing and transparency for software supply chains
- [NIST SP 800-218: Secure Software Development Framework (SSDF)](https://csrc.nist.gov/publications/detail/sp/800-218/final)
- [CycloneDX ML BOM](https://cyclonedx.org/capabilities/mlbom/) -- ML-specific SBOM extension
- [in-toto](https://in-toto.io/) -- Framework for supply chain integrity
- [NIST SP 800-204D: Strategies for Integration of Software Supply Chain Security](https://csrc.nist.gov/publications/detail/sp/800-204d/final)

---

## Open Research Questions

- [ ] How should SBOMs represent model weights, training data dependencies, and fine-tuning lineage? Is CycloneDX ML BOM sufficient?
- [ ] What is the practical path to reproducible builds for GPU-trained models given floating-point non-determinism?
- [ ] How can SLSA provenance be extended to cover the full ML pipeline (data ingestion, preprocessing, training, evaluation, packaging)?
- [ ] What signing infrastructure works well for multi-gigabyte model weight files stored in object storage?

---
