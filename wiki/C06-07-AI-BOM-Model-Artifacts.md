# C6.7 AI BOM for Model Artifacts

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.7.1–6.7.5

## Purpose

An AI Bill of Materials (AI BOM) extends traditional SBOM concepts to capture the unique components of AI systems: training datasets, model weights, hyperparameters, fine-tuning lineage, and associated licenses. Without an AI BOM, organizations cannot answer fundamental questions like "what data was this model trained on?" or "which models in production depend on this compromised base model?" This section ensures AI BOMs are generated, signed, maintained, and queryable throughout the model lifecycle.

## 2024-2026 Landscape: AI BOM Standards and Regulatory Drivers

The AI BOM ecosystem has matured significantly since 2024, driven by converging standards efforts, dedicated tooling, and regulatory mandates that make AI transparency documentation a legal requirement in multiple jurisdictions.

### CycloneDX ML-BOM

CycloneDX introduced Machine Learning BOM (ML-BOM) support in **v1.5 (June 2023)**, with ML-BOM fields stable through subsequent releases. The specification captures model architecture family, training and inference configuration, dataset references, performance metrics, and license information in a machine-readable format. As of **v1.7 (October 2025, ECMA-424 2nd Edition)** — the final 1.x release — ML-BOM capabilities are well-established and formally standardized through ECMA International. CycloneDX remains the most widely adopted format for automated AI BOM generation in CI/CD pipelines.

### SPDX AI Profile

SPDX 3.0 introduced formal **AI and Dataset profiles** that extend the traditional SBOM model to describe machine learning components — models, datasets, training configurations, and provenance data — in a consistent, machine-readable format. The SPDX 3.0.1 specification refines these profiles further. While SPDX and CycloneDX are converging in capability, they are not yet seamlessly interoperable across AI ecosystems, and organizations must currently choose one as their primary format.

### OWASP AIBOM Project

The **OWASP AIBOM Project**, launched in 2025 and now hosted at owaspaibom.org, is building a standardized approach to AI transparency. Key elements include:

- **OWASP AIBOM Generator:** An open-source tool (now a core initiative within the OWASP GenAI Security Project) that generates AI BOMs for models hosted on Hugging Face, producing output in CycloneDX format with SPDX alignment. The tool focuses on improving AI-relevant field completeness scoring and automated metadata extraction.
- **Prerequisites workstream:** A team assessing existing AI BOM standards (CycloneDX 1.6+, SPDX 3.0) to determine how well they address AI-system requirements and where extensions are needed.
- **Completeness scoring:** The project emphasizes that not all BOMs are equal — a BOM missing dataset hashes or license information provides false assurance. Completeness scoring metrics help organizations measure BOM quality.

### AI Risk Scanning (AIRS) Framework

Academic research (arXiv:2511.12668) has proposed the **AI Risk Scanning (AIRS) Framework**, which systematizes security assurance through AI BOMs and extends BOM concepts beyond component listing into active risk assessment. This represents the direction of travel: BOMs as living security documents rather than static inventories.

### Regulatory Mandates Driving AI BOM Adoption

Several regulatory developments have made AI BOM and transparency documentation either legally required or practically necessary:

**EU AI Act (transparency rules effective August 2026):**
- Article 13 requires high-risk AI system providers to document technical details enabling deployers to understand system capabilities and limitations.
- Article 50 imposes transparency obligations for providers and deployers of general-purpose AI systems, including documentation of training data, model architecture, and evaluation results.
- The European Commission is preparing Guidelines on transparent AI systems (expected Q2 2026) that will clarify the scope and specifics of these documentation requirements.
- A Code of Practice on marking and labelling of AI-generated content further specifies transparency expectations.

**California AB 2013 (effective January 1, 2026):**
- Requires transparency regarding training data used in AI models. Covered entities must disclose training data sources, making AI BOM-like documentation a compliance necessity for organizations operating in California.

**US Federal Requirements (OMB M-26-04, December 2025):**
- Requires federal agencies purchasing LLMs to request model cards, evaluation artifacts (including red-team results for tool misuse, prompt injection, and data leakage), and acceptable use policies. This creates a de facto AI BOM requirement for the federal procurement market.

### Model Artifact Management Practices

Industry practices for managing AI model artifacts in conjunction with BOMs have consolidated around several patterns:

- **Experiment trackers as BOM data sources:** Tools like MLflow, Weights & Biases, and DVC serve as authoritative sources for training metadata (datasets used, hyperparameters, framework versions) that feed into automated BOM generation.
- **Model registries with embedded BOM metadata:** MLflow Model Registry, Vertex AI Model Registry, and similar platforms can store BOM metadata alongside model artifacts, reducing the need for separate BOM infrastructure.
- **Sigstore cosign for BOM signing:** Keyless signing via Sigstore is emerging as the preferred approach for cryptographically signing AI BOMs in CI/CD pipelines, lowering the barrier compared to traditional PKI.
- **Dependency-Track for BOM analysis:** OWASP Dependency-Track and CycloneDX BOM Repository Server provide queryable BOM storage with vulnerability correlation, applicable to AI BOMs as well as traditional SBOMs.

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
- [CycloneDX Specification (GitHub)](https://github.com/CycloneDX/specification)
- [SPDX AI and Dataset Profiles](https://spdx.dev/specifications/)
- [OWASP AIBOM Project](https://owaspaibom.org/)
- [OWASP AIBOM Generator](https://genai.owasp.org/resource/owasp-aibom-generator/)
- [OWASP AIBOM Generator — Journey to OWASP (Dec 2025)](https://genai.owasp.org/2025/12/18/evolving-ai-transparency-the-journey-of-the-aibom-generator-and-its-new-home-at-owasp/)
- [AI BOM and AIRS Framework (arXiv:2511.12668)](https://arxiv.org/html/2511.12668)
- [Palo Alto Networks — What Is an AI-BOM](https://www.paloaltonetworks.com/cyberpedia/what-is-an-ai-bom)
- [NTIA Minimum Elements for SBOM](https://www.ntia.gov/page/software-bill-of-materials)
- [Dependency-Track — BOM Analysis Platform](https://dependencytrack.org/)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [DVC (Data Version Control)](https://dvc.org/)
- [Weights & Biases — Experiment Tracking](https://wandb.ai/)
- [EU AI Act — Article 13: Transparency and Provision of Information](https://artificialintelligenceact.eu/article/13/)
- [EU AI Act — Article 50: Transparency Obligations](https://artificialintelligenceact.eu/article/50/)
- [EU AI Act — Code of Practice on AI-Generated Content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)
- [California AB 2013 — Training Data Transparency](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2013)
- [NIST AI RMF — MAP Function](https://airc.nist.gov/AI_RMF_Interactivity)

---

## Open Research Questions

- What should the minimum viable AI BOM contain? How does this differ across use cases (internal model, open-source release, commercial API)?
- How can AI BOMs capture the provenance of models that are products of multi-stage pipelines (pre-training, instruction tuning, RLHF, quantization)?
- Will CycloneDX ML BOM or SPDX AI profile emerge as the dominant standard, or will fragmentation persist? CycloneDX v1.7 (ECMA-424) and SPDX 3.0.1 are converging but not yet interoperable.
- How should AI BOMs handle proprietary or confidential training data — can provenance be documented without revealing trade secrets? California AB 2013 and the EU AI Act create tension between transparency mandates and trade secret protection.
- What is the right integration point between AI BOMs and model cards — are they complementary or redundant? OMB M-26-04 requiring model cards for federal procurement suggests they serve distinct but overlapping purposes.
- How will the OWASP AIBOM completeness scoring approach evolve into an industry-standard metric for BOM quality assessment?
- Can AI BOMs be extended to serve as active risk assessment documents (per the AIRS framework), or should risk scanning remain a separate layer consuming BOM data?
