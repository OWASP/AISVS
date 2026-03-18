# C6.7 AI BOM for Model Artifacts

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.7.1–6.7.5

## Purpose

An AI Bill of Materials (AI BOM) extends traditional SBOM concepts to capture the unique components of AI systems: training datasets, model weights, hyperparameters, fine-tuning lineage, and associated licenses. Without an AI BOM, organizations cannot answer fundamental questions like "what data was this model trained on?" or "which models in production depend on this compromised base model?" This section ensures AI BOMs are generated, signed, maintained, and queryable throughout the model lifecycle.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.7.1** | **Verify that** every model artifact publishes an AI BOM that lists datasets, weights, hyperparameters, and licenses. | 1 | D/V | **Opacity of model composition creating unmanageable risk.** Without an AI BOM, organizations cannot determine what components make up a deployed model, making vulnerability response, compliance audits, and incident investigation impossible. This is the AI equivalent of shipping software without knowing its dependencies. | Retrieve the AI BOM for each deployed model artifact. Verify it includes at minimum: (1) base model identity and version, (2) training/fine-tuning datasets with hashes, (3) key hyperparameters, (4) framework and library versions used, (5) license identifiers for all components, (6) output hash of the model artifact. Formats: CycloneDX ML BOM, SPDX AI profile, or a documented internal schema. | The CycloneDX ML BOM extension and SPDX AI profile are both relatively new. Neither has achieved universal adoption. Organizations may need to start with a custom schema and migrate as standards mature. The key is having *any* structured, machine-readable BOM rather than no BOM. |
| **6.7.2** | **Verify that** AI BOM generation and cryptographic signing are automated in CI and required for merge. | 2 | D/V | **Manual BOM processes leading to incomplete or outdated BOMs.** If BOM generation depends on manual effort, it will be skipped, delayed, or inaccurate. Unsigned BOMs can be tampered with after generation. | Review CI/CD pipeline configuration. Confirm that a BOM generation step runs automatically during model build/training pipelines and that the output is cryptographically signed (Sigstore cosign, GPG, or internal PKI). Verify that merge/promotion gates require a valid signed BOM — builds without one should fail. | Automating BOM generation for training pipelines is more complex than for software builds. Training metadata (datasets used, hyperparameters) must be captured programmatically from the training script or experiment tracker (MLflow, W&B, DVC). Integration effort is non-trivial. |
| **6.7.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata (hash and license) is missing. | 2 | D | **Incomplete BOMs providing false assurance.** A BOM that lists some components but omits others (e.g., missing dataset hash, unlicensed fine-tuning adapter) gives a false sense of transparency. Completeness enforcement ensures every component is documented. | Review the BOM validation rules in the CI pipeline. Confirm that required fields are defined (at minimum: component name, version/hash, license) and that missing fields cause a build failure. Test by submitting a model artifact with an incomplete BOM and verify the build is rejected. | Defining "complete" is context-dependent. Some metadata (e.g., exact hyperparameters, training duration) may be less critical than others (dataset provenance, license). Organizations should define tiered requirements: mandatory fields vs. recommended fields. |
| **6.7.4** | **Verify that** downstream consumers can query AI BOMs via API to validate imported models at deploy time. | 2 | V | **Deployment of models without verification against their BOM.** If BOMs exist but are not queryable at deploy time, the deployment pipeline cannot programmatically verify that the model being deployed matches its documented composition and that all components are approved. | Confirm that an API endpoint (REST, GraphQL, or CLI tool) exists for querying AI BOMs by model identifier. Test that the API returns the full BOM for a given model version. Verify that deployment pipelines include a BOM-query step that validates model integrity before deployment (e.g., comparing the model's hash against the BOM's recorded hash). | This requires infrastructure investment: a BOM registry/database, an API service, and integration with deployment tooling. Options include CycloneDX BOM Repository Server, Dependency-Track, or custom solutions. For organizations using model registries (MLflow Model Registry, Vertex AI Model Registry), BOM metadata can potentially be stored as model metadata. |
| **6.7.5** | **Verify that** AI BOMs are version-controlled and diffed to detect unauthorized modifications. | 3 | V | **Tampering with BOMs to conceal supply-chain modifications.** An attacker who compromises a model could also modify its BOM to hide the change. Version-controlling BOMs and diffing between versions makes unauthorized modifications detectable. | Verify that AI BOMs are stored in a version-controlled system (Git, immutable object store with versioning). Confirm that a diff process runs when BOMs are updated, and that unexpected changes (e.g., dataset hash change, license change, new component addition) trigger alerts or require approval. Review diff history for evidence of monitoring. | If BOMs are stored alongside model artifacts in a model registry, versioning may be implicit. If stored separately, explicit version control is needed. The diff process should be automated — manual BOM review does not scale. |

---

## Related Standards & References

- [CycloneDX ML BOM Specification](https://cyclonedx.org/capabilities/mlbom/)
- [SPDX AI and Dataset Profiles](https://spdx.dev/specifications/)
- [NTIA Minimum Elements for SBOM](https://www.ntia.gov/page/software-bill-of-materials)
- [Dependency-Track — BOM Analysis Platform](https://dependencytrack.org/)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [DVC (Data Version Control)](https://dvc.org/)
- [Weights & Biases — Experiment Tracking](https://wandb.ai/)
- [EU AI Act — Transparency Requirements](https://artificialintelligenceact.eu/)
- [NIST AI RMF — MAP Function](https://airc.nist.gov/AI_RMF_Interactivity)

---

## Open Research Questions

- What should the minimum viable AI BOM contain? How does this differ across use cases (internal model, open-source release, commercial API)?
- How can AI BOMs capture the provenance of models that are products of multi-stage pipelines (pre-training, instruction tuning, RLHF, quantization)?
- Will CycloneDX ML BOM or SPDX AI profile emerge as the dominant standard, or will fragmentation persist?
- How should AI BOMs handle proprietary or confidential training data — can provenance be documented without revealing trade secrets?
- What is the right integration point between AI BOMs and model cards — are they complementary or redundant?
