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

### NSA AI Supply Chain Security Guidance (March 2026)

The US National Security Agency published updated AI supply chain guidance on **18 March 2026**, treating AI systems as complete supply chains requiring controls across data, models, software, infrastructure, hardware, and third-party services. Key recommendations relevant to AI BOMs:

- **Cryptographic signing across the model lifecycle** and maintenance of a verified model registry.
- **Integrity checks** — hashes, checksums, and digital signatures — for all model artifacts before deployment.
- **Quarantine and test externally sourced data** before ingestion; use provenance methods including lineage tracking.
- **Prefer secure file formats** (e.g., safetensors over pickle) and use trusted, transparent model sources.

The guidance reinforces that AI BOMs are a foundational control: without structured documentation of what went into a model, none of the downstream integrity verification is possible.

### Enterprise Adoption Reality Check

Despite growing regulatory pressure, enterprise AI BOM adoption remains early-stage. As of March 2026:

- **Visibility gap:** According to Cycode's 2026 State of Product Security report, only **19% of organizations have full visibility** into where and how AI is used across development. Over **52% lack a formal or centralized governance framework** for managing AI adoption — making AI BOM generation practically impossible without foundational asset discovery.
- **Hub scale vs. governance:** Hugging Face reached **2 million+ public models and 500,000+ public datasets** by spring 2026, yet model card completion rates remain inconsistent. Many models lack the basic metadata (training data provenance, license, evaluation results) that AI BOMs require as input.
- **Tool maturity lag:** While standards like CycloneDX ML-BOM and SPDX 3.0 AI profiles are well-defined, operational tooling for automated BOM generation in training pipelines is still maturing. The gap between specification capability and production automation remains the primary adoption barrier.

### Real-World Supply Chain Threats Driving AI BOM Adoption

The urgency behind AI BOM adoption is grounded in observed attacks and vulnerability data:

- **Malicious models at scale:** As of April 2025, Protect AI's scans of 4.47 million model versions found **352,000 unsafe or suspicious issues across 51,700 models**. JFrog's 2025 Software Supply Chain Report documented over 1 million new models hitting Hugging Face in 2024 alone, with a **6.5× increase in malicious models** year-over-year. ReversingLabs' 2026 Software Supply Chain Security Report identified a further **73% increase in malicious packages** across software ecosystems.
- **nullifAI evasion technique (February 2025):** ReversingLabs [discovered malicious ML models on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face) that used deliberately broken pickle files compressed with 7z (instead of ZIP) to bypass Picklescan detection. The injected code opened platform-aware reverse shells to hardcoded IPs. This demonstrated that scanner-only defenses are insufficient — provenance verification and BOM-based integrity checks provide the defense-in-depth layer that scanning alone cannot.
- **CVE-2026-28500 — ONNX hub.load() silent supply chain attack (March 2026):** A critical vulnerability (CVSS 9.1) in ONNX Python library ≤1.20.1 allows `onnx.hub.load()` with `silent=True` to suppress all security warnings and load models from attacker-controlled repositories without confirmation. The SHA256 integrity check validates against a manifest fetched from the same repository — so an attacker controlling the repo controls the manifest. No patched version was available at disclosure. This underscores why deploy-time BOM verification must use independently stored and signed BOMs rather than trusting in-band integrity manifests.
- **Model serialization attacks:** The Python pickle format — still common for distributing AI models — allows arbitrary code execution on load. Tools like [ModelScan](https://github.com/protectai/modelscan) (Protect AI, updated Feb 2026) scan for malicious payloads in pickle, H5, and SavedModel formats. The safetensors format eliminates this attack vector by storing only tensor data with no executable code.
- **Data poisoning at low cost:** Researchers from NYU, Washington University, and Columbia University demonstrated in January 2025 that replacing just 1 million out of 100 billion training tokens with medical misinformation caused a ~5% increase in harmful outputs — a poisoning ratio so small it would be invisible without proper dataset provenance tracking.
- **MITRE ATLAS coverage:** Technique [AML.T0010 (ML Supply Chain Compromise)](https://atlas.mitre.org/techniques/AML.T0010) includes sub-techniques for data supply chain (AML.T0010.001), model artifact compromise (AML.T0010.002), hardware supply chain (AML.T0010.003), and container registry compromise (AML.T0010.004). AI BOMs directly support detection and response for the first two sub-techniques.

### Model Signing: The Sigstore Ecosystem

As of March 2026, the **OpenSSF Model Signing (OMS)** specification — developed by Google, NVIDIA, HiddenLayer, and OpenSSF — has emerged as the industry standard for cryptographically signing AI model artifacts:

- **model-signing v1.0** (April 2025): Built on `sigstore-python`, installable via `pip install model-signing`. Supports keyless signing using short-lived certificates bound to OIDC identity tokens. Signing events are logged in the Sigstore transparency log (Rekor), providing a tamper-evident audit trail.
- **Hub integration:** The signing API is designed for direct integration with model hubs (Kaggle, Hugging Face) and ML frameworks (TensorFlow, PyTorch), allowing automatic signing via `model.save()`. NVIDIA's NGC adopted model signing as of July 2025.
- **Kubernetes enforcement:** The [Sigstore Model Validation Operator](https://blog.sigstore.dev/model-validation-operator-v1.0.1/) (v1.0.1, alpha) uses Kubernetes mutating webhooks to inject init containers that verify model signatures before workload execution. Pods fail to launch if verification fails, enforcing model integrity at the infrastructure layer.
- **Cosign v2.6.x** added Rekor v2 upload/verification support; Cosign v3 defaults to the new bundle format for consolidated signed material.

### CISA 2025 SBOM Minimum Elements Update

CISA's [2025 Minimum Elements for SBOM](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom) significantly expanded requirements beyond the 2021 NTIA baseline, shifting from inventory-focused documentation to forensic readiness:

- **New mandatory fields:** Component hash (cryptographic fingerprint for integrity verification), license information, tool name (which tool generated the SBOM), and generation context (how, when, and by whom).
- **Known unknowns:** Organizations must now formally document missing information rather than silently omitting it — directly relevant to AI BOMs where training data provenance may be partially unknown.
- **Coverage over depth:** The update reframes "depth" as "coverage," acknowledging that complete enumeration of transitive dependencies is less important than understanding what proportion of the attack surface is documented.

While the 2025 CISA update does not explicitly address AI/ML model artifacts, its new requirements for component hashes, license tracking, and generation context map directly to AI BOM needs. Organizations building AI BOMs should treat the CISA minimum elements as a floor and extend them with AI-specific fields (dataset provenance, training configuration, model architecture).

### Agentic Supply Chain Scanning

As AI agent deployments proliferate, the supply chain attack surface extends beyond models and datasets to encompass MCP servers, tool plugins, and agent frameworks. Emerging tools address this expanded scope:

- **agent-bom:** An [open-source AI supply chain security scanner](https://github.com/msaad00/agent-bom) that maps vulnerabilities across the agentic supply chain — from CVEs to exposed credentials and at-risk tools. It auto-detects 30+ MCP clients (Claude Desktop, Cursor, Windsurf, VS Code), scans 15 package ecosystems, and generates output in CycloneDX 1.6 (with ML-BOM extensions) and SPDX 3.0. Its blast radius mapping traces attack paths from CVE through package to MCP server to AI agent to credentials. The tool also audits instruction files (`.claude.md`, `.cursorrules`) for suspicious patterns like credential access or guardrail bypasses.
- **Protect AI Guardian:** An enterprise model scanning product that integrates into CI/CD pipelines, scanning models for serialization attacks and known vulnerabilities before production deployment. It complements BOM generation by providing active threat detection alongside passive documentation.

### Model Artifact Management Practices

Industry practices for managing AI model artifacts in conjunction with BOMs have consolidated around several patterns:

- **Experiment trackers as BOM data sources:** Tools like MLflow, Weights & Biases, and DVC serve as authoritative sources for training metadata (datasets used, hyperparameters, framework versions) that feed into automated BOM generation.
- **Model registries with embedded BOM metadata:** MLflow Model Registry, Vertex AI Model Registry, and similar platforms can store BOM metadata alongside model artifacts, reducing the need for separate BOM infrastructure.
- **Sigstore model-signing for artifact integrity:** The OpenSSF model-signing library (`pip install model-signing`) provides keyless signing for model artifacts, with signatures logged in Sigstore's transparency log. This complements BOM signing by verifying that model weights themselves have not been tampered with.
- **ModelScan for pre-deployment scanning:** Protect AI's [ModelScan](https://github.com/protectai/modelscan) scans serialized model files (pickle, H5, SavedModel) for malicious code before loading — a necessary complement to BOM verification since BOMs document provenance but do not scan for embedded malware.
- **Dependency-Track for BOM analysis:** OWASP Dependency-Track and CycloneDX BOM Repository Server provide queryable BOM storage with vulnerability correlation, applicable to AI BOMs as well as traditional SBOMs.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **6.7.1** | **Verify that** every model artifact publishes an AI BOM that lists datasets, weights, hyperparameters, and licenses. | 1 | **Opacity of model composition creating unmanageable risk (MITRE ATLAS [AML.T0010.002](https://atlas.mitre.org/techniques/AML.T0010.002)).** Without an AI BOM, organizations cannot determine what components make up a deployed model, making vulnerability response, compliance audits, and incident investigation impossible. Protect AI's April 2025 scans found 352,000 unsafe issues across 51,700 models — organizations without BOMs have no way to determine if affected models are deployed in their environment. | Retrieve the AI BOM for each deployed model artifact. Verify it includes at minimum: (1) base model identity and version, (2) training/fine-tuning datasets with hashes, (3) key hyperparameters, (4) framework and library versions used, (5) license identifiers for all components, (6) output hash of the model artifact. Use the OWASP AIBOM Generator for Hugging Face-hosted models. Validate against CycloneDX ML BOM schema or SPDX 3.0 AI profile. Cross-reference the OWASP AIBOM completeness scoring to measure BOM quality. | CycloneDX v1.7 (ECMA-424) and SPDX 3.0.1 both support AI BOMs but are not yet seamlessly interoperable. The OWASP AIBOM Prerequisites workstream is evaluating gaps. As of March 2026, only 19% of organizations have full visibility into AI usage across development, and 52% lack centralized AI governance frameworks (Cycode 2026 State of Product Security). CISA's 2025 SBOM minimum elements now require component hashes and license information — a useful baseline to extend for AI-specific fields. EU AI Act Article 13 and California AB 2013 create regulatory pressure for structured AI documentation by mid-2026. |
| **6.7.2** | **Verify that** AI BOM generation and cryptographic signing are automated in CI and required for merge. | 2 | **Manual BOM processes leading to incomplete or outdated BOMs.** If BOM generation depends on manual effort, it will be skipped, delayed, or inaccurate. Unsigned BOMs can be tampered with after generation. The NSA's March 2026 guidance explicitly recommends cryptographic signing across the model lifecycle. | Review CI/CD pipeline configuration. Confirm that a BOM generation step runs automatically during model build/training pipelines. For signing, verify use of Sigstore model-signing (`pip install model-signing`) with keyless OIDC-based signing, Sigstore cosign v2.6+, GPG, or internal PKI. Verify that merge/promotion gates require a valid signed BOM — builds without one should fail. Check that signing events are logged in a transparency log (e.g., Rekor). | Automating BOM generation for training pipelines is more complex than for software builds. Training metadata must be captured programmatically from experiment trackers (MLflow, W&B, DVC). The OpenSSF model-signing v1.0 library (April 2025) simplifies signing via framework integration (`model.save()` hooks for TensorFlow/PyTorch), but hub-level integration (Kaggle, Hugging Face, NGC) is still maturing. The nullifAI incident (Feb 2025) — where broken pickle files bypassed Picklescan on Hugging Face — demonstrates that CI-integrated BOM signing provides a detection layer that file-format scanning alone cannot. |
| **6.7.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata (hash and license) is missing. | 2 | **Incomplete BOMs providing false assurance.** A BOM that lists some components but omits others (e.g., missing dataset hash, unlicensed fine-tuning adapter) gives a false sense of transparency. Completeness enforcement ensures every component is documented. The OWASP AIBOM project's completeness scoring research underscores that BOMs without dataset hashes or license info create a false sense of security. | Review the BOM validation rules in the CI pipeline. Confirm that required fields are defined (at minimum: component name, version/hash, license) and that missing fields cause a build failure. Test by submitting a model artifact with an incomplete BOM and verify the build is rejected. Use OWASP AIBOM completeness scoring metrics to quantify BOM quality. Run ModelScan against the serialized model files alongside BOM validation to detect malicious payloads that a BOM alone would not catch. | Defining "complete" is context-dependent. Organizations should define tiered requirements: **mandatory** (base model ID, dataset hashes, licenses, model output hash) vs. **recommended** (hyperparameters, training duration, performance metrics). The NTIA minimum elements for SBOM provide a useful starting point that can be extended for AI-specific fields. |
| **6.7.4** | **Verify that** downstream consumers can query AI BOMs via API to validate imported models at deploy time. | 2 | **Deployment of models without verification against their BOM (MITRE ATLAS [AML.T0010.002](https://atlas.mitre.org/techniques/AML.T0010.002)).** If BOMs exist but are not queryable at deploy time, the deployment pipeline cannot programmatically verify that the model being deployed matches its documented composition and that all components are approved. CVE-2026-28500 (ONNX `hub.load()`, CVSS 9.1) demonstrated how in-band integrity checks fail when the attacker controls both model and manifest — deploy-time BOM queries must use independently stored, signed BOMs. JFrog's 2025 report documented a 6.5× increase in malicious models on Hugging Face; ReversingLabs' 2026 report found a further 73% increase in malicious packages across ecosystems. | Confirm that an API endpoint (REST, GraphQL, or CLI tool) exists for querying AI BOMs by model identifier. Test that the API returns the full BOM for a given model version. Verify that deployment pipelines include a BOM-query step that validates model integrity before deployment (e.g., comparing the model's hash against the BOM's recorded hash). Critically, verify that integrity manifests are stored and signed independently of the model repository — co-located manifests are vulnerable to CVE-2026-28500-style attacks. For Kubernetes environments, evaluate the Sigstore Model Validation Operator (v1.0.1) which uses admission webhooks to block workloads with unverified model signatures. | Infrastructure options: CycloneDX BOM Repository Server, OWASP Dependency-Track, or custom solutions built on model registries (MLflow, Vertex AI). For Kubernetes-native enforcement, the Sigstore Model Validation Operator injects init containers to verify signatures before pod execution — currently alpha but demonstrates the target architecture. For agentic deployments, agent-bom generates CycloneDX 1.6 ML-BOM output for MCP servers and agent frameworks, extending BOM coverage to the tool/plugin supply chain. Organizations using the NSA's verified model registry pattern can combine BOM query with hash verification at a single gate. |
| **6.7.5** | **Verify that** AI BOMs are version-controlled and diffed to detect unauthorized modifications. | 3 | **Tampering with BOMs to conceal supply-chain modifications (MITRE ATLAS [AML.T0010](https://atlas.mitre.org/techniques/AML.T0010)).** An attacker who compromises a model could also modify its BOM to hide the change. Version-controlling BOMs and diffing between versions makes unauthorized modifications detectable. When signing keys are compromised — as threat researchers have noted could enable distribution of malicious model updates at scale — BOM version history provides a secondary detection layer. | Verify that AI BOMs are stored in a version-controlled system (Git, immutable object store with versioning). Confirm that a diff process runs when BOMs are updated, and that unexpected changes (e.g., dataset hash change, license change, new component addition) trigger alerts or require approval. If using Sigstore model-signing, verify that signing events are recorded in the Rekor transparency log, providing an immutable audit trail that supplements BOM version control. Review diff history for evidence of active monitoring. | If BOMs are stored alongside model artifacts in a model registry, versioning may be implicit. If stored separately, explicit version control is needed. The Sigstore transparency log provides append-only immutability that complements Git-based version control. The diff process should be automated — manual BOM review does not scale. Consider alerting on any BOM change that is not accompanied by a corresponding model retraining or fine-tuning event. |

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
- [MITRE ATLAS — AML.T0010: ML Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
- [OpenSSF Model Signing (model-transparency)](https://github.com/sigstore/model-transparency)
- [Sigstore Model Signing v1.0 Announcement](https://blog.sigstore.dev/model-transparency-v1.0/)
- [Sigstore Model Validation Operator for Kubernetes](https://blog.sigstore.dev/model-validation-operator-v1.0.1/)
- [Google Case Study: Securing ML Models with Sigstore](https://openssf.org/blog/2025/07/23/case-study-google-secures-machine-learning-models-with-sigstore/)
- [Protect AI ModelScan — Model Serialization Attack Detection](https://github.com/protectai/modelscan)
- [NSA AI Supply Chain Security Guidance (March 2026)](https://dig.watch/updates/ai-supply-chain-risks-nsa)
- [ISO/IEC 42001:2023 — AI Management Systems](https://www.iso.org/standard/42001)
- [OMB M-26-04 — Federal AI Procurement Requirements](https://www.whitehouse.gov/omb/)
- [JFrog 2025 Software Supply Chain Report](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [Cosign v2.6 Release Notes](https://github.com/sigstore/cosign)
- [CISA 2025 Minimum Elements for SBOM](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom)
- [CISA's New SBOM Standards — ReversingLabs Analysis](https://www.reversinglabs.com/blog/cisa-new-sbom-standards)
- [CVE-2026-28500 — ONNX hub.load() Silent Supply Chain Attack](https://cvefeed.io/vuln/detail/CVE-2026-28500)
- [nullifAI: Malicious ML Models Bypass Picklescan — ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- [ReversingLabs 2026 Software Supply Chain Security Report](https://www.leadertelegram.com/news/nation-world/reversinglabs-2026-software-supply-chain-security-report-identifies-73-increase-in-malicious/article_0e54edf7-7c64-589b-a877-1e49583350e0.html)
- [agent-bom — AI Supply Chain Security Scanner](https://github.com/msaad00/agent-bom)
- [Wiz AI-BOM Guide](https://www.wiz.io/academy/ai-security/ai-bom-ai-bill-of-materials)
- [Cycode 2026 State of Product Security — AIBOM Adoption](https://cycode.com/blog/ai-bill-of-materials/)
- [Hugging Face State of Open Source — Spring 2026](https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026)
- [CISA/NSA/Partners — Securing AI in Operational Technology (Dec 2025)](https://www.openpolicy.co/resources/cisa-and-international-partners-release-new-guidance-securing-operational-technology-in-the-age-of-ai)

---

## Open Research Questions

- What should the minimum viable AI BOM contain? How does this differ across use cases (internal model, open-source release, commercial API)?
- How can AI BOMs capture the provenance of models that are products of multi-stage pipelines (pre-training, instruction tuning, RLHF, quantization)?
- Will CycloneDX ML BOM or SPDX AI profile emerge as the dominant standard, or will fragmentation persist? CycloneDX v1.7 (ECMA-424) and SPDX 3.0.1 are converging but not yet interoperable.
- How should AI BOMs handle proprietary or confidential training data — can provenance be documented without revealing trade secrets? California AB 2013 and the EU AI Act create tension between transparency mandates and trade secret protection.
- What is the right integration point between AI BOMs and model cards — are they complementary or redundant? OMB M-26-04 requiring model cards for federal procurement suggests they serve distinct but overlapping purposes.
- How will the OWASP AIBOM completeness scoring approach evolve into an industry-standard metric for BOM quality assessment?
- Can AI BOMs be extended to serve as active risk assessment documents (per the AIRS framework), or should risk scanning remain a separate layer consuming BOM data?
- How should the OpenSSF model-signing specification interact with AI BOM signing — should model artifacts and their BOMs share a single signing identity, or should they be independently signed for defense-in-depth?
- As the Sigstore Model Validation Operator matures beyond alpha, what admission policy patterns will emerge for enforcing model provenance in Kubernetes-based ML inference platforms?
- The NSA guidance recommends preferring secure file formats (safetensors over pickle), but how should organizations handle legacy models that exist only in unsafe formats — is re-serialization trustworthy if the original model may already be compromised?
- How should AI BOMs extend to cover the agentic supply chain — MCP servers, tool plugins, and multi-agent orchestration frameworks — given that tools like agent-bom are already generating CycloneDX ML-BOM output for these components?
- CVE-2026-28500 exposed a fundamental weakness in co-located integrity manifests. What architectural patterns ensure that BOM storage and verification remain independent of model distribution channels?
- With only 19% of organizations having full AI visibility (Cycode 2026), should AI BOM generation be preceded by a mandatory AI asset discovery phase, or can BOM tooling drive discovery as a side effect?
