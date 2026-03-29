# C6.5 Third-Party Dataset Risk Assessment

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.5.1–6.5.5

## Purpose

Datasets are a uniquely dangerous supply-chain vector for AI systems. Unlike code dependencies where vulnerabilities are typically detectable, poisoned training data can embed subtle behavioral changes into a model that are extremely difficult to detect post-training. Third-party datasets also carry legal risks — copyrighted content, personally identifiable information, and biased distributions can create liability. This section ensures external datasets are assessed for poisoning, legal compliance, and bias before use, and monitored throughout their lifecycle.

---

## 2025-2026 Landscape Update

### Web-Scale Dataset Poisoning is Practical and Cheap

Carlini et al. (2023) demonstrated two concrete attack methods against web-scale datasets that remain relevant and under-mitigated:

- **Split-view poisoning**: Many distributed datasets (LAION-400M, COYO-700M, Conceptual 12M) store URLs rather than actual data. Domain names in these URL lists continuously expire. An attacker can purchase expired domains for as little as $10 each and serve malicious content to any future downloader. The researchers found that all ten tested datasets contained between 0.14% and 6.48% purchasable expired domains. Poisoning 0.01% of LAION-400M or COYO-700M costs approximately $60 USD. Critically, nearly all third-party download tools for these datasets ignore the hash checksums that were provided.

- **Frontrunning poisoning**: For crowdsourced datasets derived from Wikipedia snapshots, attackers can predict snapshot timing to the minute and inject malicious edits that are captured in the dataset but quickly reverted. This could theoretically poison approximately 6.5% of English Wikipedia-derived documents, with multilingual Wikipedias showing vulnerability rates up to 25.3%.

Even poisoning rates as low as 0.00025% of a dataset can achieve 60% success in targeted misclassification attacks. These findings mean that any organization using URL-based or web-scraped datasets without hash verification is accepting a materially exploitable risk.

### LAION Dataset Controversies and Remediation

The LAION-5B dataset saga illustrates the full spectrum of third-party dataset risks:

- **CSAM discovery (December 2023)**: The Stanford Internet Observatory found 3,226 suspected instances of links to child sexual abuse material in LAION-5B, with 1,008 externally validated. LAION temporarily removed LAION-5B and LAION-400M.
- **Sensitive personal data**: An investigation by Bayerischer Rundfunk found that LAION datasets contain large amounts of private and sensitive data harvested from public websites without consent.
- **Hateful and harmful content**: Research (Birhane et al. 2023) documented widespread instances of rape, pornography, malign stereotypes, racist and ethnic slurs, and other extremely problematic content within LAION-5B.
- **Re-LAION-5B (August 2024)**: LAION released a cleaned version, removing 2,236 links after matching against known-abuse lists. However, the fundamental architecture of URL-based datasets means that the content behind remaining links continues to change over time.

The LAION case is instructive: even well-intentioned, widely-used datasets can harbor serious content and legal risks that are only discovered years after initial release and widespread adoption.

### Platform Supply Chain Attacks: Hugging Face and Model Hubs

As of early 2026, model hub platforms have become a significant attack surface for dataset and model poisoning:

- **Malicious model and dataset uploads**: A monitoring study tracking over 705,000 models and 176,000 datasets on Hugging Face uncovered 91 malicious models and 9 malicious dataset loading scripts containing reverse shells, browser credential theft, and system reconnaissance payloads. Separately, researchers identified approximately 100 models on the platform enabling remote code execution on user machines.
- **Model namespace reuse** (Palo Alto Unit 42): When authors delete accounts on platforms like Hugging Face, Google Vertex AI Model Garden, Microsoft Azure AI Foundry, or Kaggle, attackers can re-register the same namespace and upload compromised models. Existing pipelines that pull models by name automatically download the malicious version. Mitigations: pin models to specific commit revisions, clone trusted repositories to internal storage, and scan codebases for name-based model references.
- **Typosquatting**: Threat actors upload models with names that are common misspellings of popular models, targeting developers who do not verify model identity before downloading.
- **Estimated impact**: One 2025 report estimated $12 billion in losses from compromised machine learning models across the supply chain, with 23% of the top 1,000 most-downloaded models having been compromised at some point.

These findings reinforce that datasets downloaded from public hubs require the same vetting rigor as third-party code dependencies — hash verification, namespace validation, and quarantine-before-use policies.

### Emerging Attack Techniques (2025-2026)

Several new poisoning vectors have materialized beyond the traditional web-scale approaches:

- **Backdoor trigger injection**: Hidden prompts embedded in training repositories activate malicious model behaviors months after training (the "Basilisk Venom" pattern). These triggers are invisible during standard data review.
- **Synthetic data propagation**: The "Virus Infection Attack" (September 2025) demonstrated that contamination in synthetic training data spreads invisibly across model generations, compounding with each fine-tuning cycle. Once baked into synthetic datasets, the poison quietly amplifies across downstream models.
- **Multimodal poisoning**: Two CVPR papers revealed that image-generation models can be hijacked: "Silent Branding" made diffusion models reproduce logos unprompted, while "Losing Control" showed that ControlNets could be poisoned so subtle triggers force NSFW content generation while appearing normal.
- **Safetensors conversion hijacking** (HiddenLayer): Researchers demonstrated that the Hugging Face safetensors conversion service could be compromised to inject malicious code into models during format conversion and send unauthorized pull requests to any repository while impersonating the conversion bot. This highlights that even security-enhancing infrastructure can become an attack vector.
- **Medical domain poisoning**: A 2025 multi-university study (NYU, Washington, Columbia) and a comprehensive 2026 analytical framework found that as few as 100–500 poisoned samples can compromise clinical LLMs, medical imaging systems, and agentic healthcare AI with attack success rates typically exceeding 60%. Detection delays commonly range from 6 to 12 months and may extend to years in distributed or privacy-constrained environments. The absolute sample count matters more than the proportion — larger datasets do not inherently protect against poisoning.
- **PoisonBench (ICML)**: A benchmark specifically designed to measure LLM vulnerability to data poisoning, providing standardized evaluation across attack types and model architectures.
- **MCP tool poisoning**: Hidden instructions embedded in Model Context Protocol tool descriptions can poison the context that agents consume, representing a new data poisoning vector in agentic AI systems.

### Legal Landscape for Training Data

The legal environment for training data has become significantly more complex, particularly with the EU AI Act entering enforcement:

- **NYT v. OpenAI** and **Getty v. Stability AI** established that training on copyrighted content carries real litigation risk.
- **LAION v. Kneschke (2024)**: A German court ruled that building public datasets is covered by the text and data mining (TDM) exception under EU copyright law, providing some legal cover for research datasets, but the ruling's applicability to commercial use remains contested.
- **GDPR and CCPA enforcement**: Models that memorize and regurgitate PII from training data face regulatory action.
- **EU AI Act Article 10 (enforcing August 2026)**: High-risk AI systems must use training data that is "relevant, representative, free of errors and complete." Organizations must document all datasets used, maintain full records of data origin, publish summaries of training data for general-purpose AI models, and respect copyright opt-outs under the EU Copyright Directive. Penalties reach up to €10 million or 2% of global annual turnover.
- **EU AI Act timeline**: General-purpose AI obligations began August 2025; high-risk system requirements become fully applicable August 2026. Organizations need data source inventories, quality results, lineage diagrams, and usage approvals ready for enforcement.

### NSA/CISA AI Supply Chain Guidance (March 2026)

In March 2026, the NSA alongside allied intelligence agencies published joint guidance on AI/ML supply chain risks and mitigations. Key recommendations relevant to dataset security:

- **Quarantine and test** externally sourced data before moving it into internal systems. Preprocess and review for quality and bias issues.
- **Integrity verification**: Use checksums, cryptographic hashes, digital signatures, and lineage tracking methods for all datasets.
- **Vendor assessment**: Evaluate third-party data providers' security practices and vulnerability management processes. Monitor their security posture over time.
- **Contractual controls**: Include cybersecurity requirements in contracts with dataset suppliers — covering data handling restrictions, audit rights, incident response obligations, and retention policies.
- **AI Bill of Materials**: Maintain documentation of all components including datasets, analogous to Software Bills of Materials (SBOMs) for code dependencies.
- **Threat modeling**: Perform threat modeling specific to AI/ML data pipelines, including data poisoning and model inversion attack scenarios.

### Dataset Vetting Tools: Current State

The tooling landscape for dataset security has matured considerably but still has gaps:

- **Cleanlab**: Identifies label errors, outliers, and near-duplicates in datasets. Useful for detecting dirty-label poisoning but limited against clean-label attacks. Now integrates with major ML frameworks for pipeline-embedded validation.
- **Great Expectations**: General-purpose data validation framework that can enforce schema, statistical, and distribution constraints on incoming datasets.
- **Microsoft Presidio**: PII detection and redaction for unstructured text. Supports multiple languages but has significant false-negative rates for non-English content and domain-specific identifiers.
- **DVC (Data Version Control)**: Open-source version control for datasets providing Git-like tracking of data changes, integrity verification through hash-based deduplication, and audit trails via pull-request-style reviews of data modifications. As of late 2025, lakeFS acquired DVC to combine lightweight file-based versioning with production-scale data lake management.
- **Hawk-Eye**: Open-source broad-spectrum scanner covering databases, cloud storage, and files with OCR support for 350+ file types (DOCX, PDF, images, videos) — useful for detecting PII in multimodal training datasets.
- **PiiCatcher**: CLI scanner that detects PII in databases using regex pattern matching and NLP-based analysis with spaCy, catching both obviously-named columns and columns with generic names but sensitive content.
- **Croissant (MLCommons)**: Metadata format for ML datasets gaining adoption, providing standardized fields for provenance, license, and content description. Complementary to the "Datasheets for Datasets" framework.
- **ScanCode / REUSE**: License detection for code datasets, important for detecting copyleft or restricted-license code in training corpora.
- **Data Provenance Initiative**: Academic effort to catalog and document the provenance of major ML training datasets, providing a reference for organizations performing due diligence.

### Poisoning Detection Frameworks (2025-2026)

Beyond the general dataset vetting tools above, several specialized poisoning detection frameworks have emerged:

- **GBDR (Generalizable Backdoor Detection and Removal)**: A peer-reviewed framework that detects and removes backdoors from datasets without knowledge of attack specifications. It exploits the Model Capacity Effect (MCE) — backdoor and clean samples exhibit distinct performance across models of varying capacity. A lower-capacity detection model differentiates between them, then a diffusion-based purification phase removes triggers and corrects labels. Validated across four benchmark datasets, outperforming prior state-of-the-art defenses. Open-source implementation available on GitHub.
- **BaDLoss**: Addresses a gap in prior defenses by handling multiple simultaneous backdoor attacks. Leverages the observation that poisoned images exhibit anomalous loss trajectories during training — they rely on unnatural features for classification, which manifests as detectable loss patterns.
- **MEDLEY (Ensemble Disagreement Monitoring)**: Proposed for healthcare AI, this approach uses architectural and vendor diversity to detect poisoning through systematic disagreement patterns across heterogeneous model ensembles. Particularly relevant for high-stakes domains where a single compromised foundation model could propagate to hundreds of institutions.
- **MalHug**: End-to-end detection pipeline deployed on a mirrored Hugging Face instance, monitoring over 705K models and 176K datasets. Uncovered 91 malicious models and 9 malicious dataset loading scripts containing reverse shells, credential theft, and reconnaissance payloads.

### AI BOM Standards and Provenance Tools

As of early 2026, AI Bill of Materials standards have matured substantially, though adoption remains a challenge:

- **CycloneDX 1.6** (April 2024) added ML-BOM support, and **CycloneDX 1.7** (2025) expanded with patent and intellectual property metadata, citations for data provenance, and enhanced cryptographic transparency.
- **SPDX 3.0** (April 2024) introduced formal AI and Dataset profiles extending the traditional SBOM model to describe ML components — models, datasets, training configurations, and provenance data — in a machine-readable format.
- **TAIBOM (Trusted AI Bill of Materials)** (Oxford, October 2025): A research framework that extends SBOM principles to AI with cryptographic attestation. Each artifact is hashed and digitally signed on creation with full provenance (source URI, timestamp, license, compliance details). Derived artifacts must embed signed hashes of all direct ancestors, ensuring a chain of trust from training data through deployed inference.
- **AIBoMGen** (ACM/IEEE CAIN 2026): A proof-of-concept platform that automates AI BOM generation, acting as a neutral third-party observer during model training. Uses cryptographic hashing, digital signatures, and in-toto attestations to detect unauthorized modifications. Enforces mandatory AI BOM creation for every training job with negligible performance overhead.
- **OWASP AI-BOM Project**: The Prerequisites workstream is assessing how well CycloneDX 1.6 and SPDX 3.0 address AI-system requirements and where extensions are needed. Serves as a reference for organizations choosing an AI BOM standard.
- **Adoption gap**: A June 2025 Lineaje survey found 48% of security professionals admit their organizations are falling behind on SBOM requirements; ML-BOM adoption is significantly lower still.

### Bias Detection and Drift Monitoring Tools

For requirements 6.5.4 and 6.5.5, the tooling ecosystem has expanded beyond research prototypes into production-ready platforms:

- **Fairlearn (Microsoft)**: Open-source toolkit for assessing and improving fairness in ML models. Provides demographic parity, equalized odds, and calibration metrics with integration into scikit-learn pipelines.
- **AI Fairness 360 (IBM)**: Comprehensive bias detection library with 70+ fairness metrics and 13 bias mitigation algorithms covering pre-processing, in-processing, and post-processing stages.
- **EvidentlyAI**: Open-source platform with built-in drift reports, data quality monitoring, and model performance dashboards. Supports statistical drift detection using KS tests, PSI, and Jensen-Shannon divergence.
- **WhyLabs**: AI observability platform providing continuous dataset monitoring, drift detection, and anomaly alerting. Released under Apache 2 license in January 2025.
- **Arthur AI**: Production AI monitoring with bias drift alerts, providing continuous fairness monitoring rather than point-in-time assessments.
- **Fiddler AI**: Shifts bias detection from pre-deployment testing to continuous production monitoring, alerting teams before biased predictions cause compliance issues.
- **Arize AI**: ML observability with embedding drift detection, particularly useful for monitoring vector-based datasets used in RAG systems.

### Data Supply Chain Security

Organizations should treat datasets with the same supply-chain rigor applied to code dependencies:

1. **Hash-verify on download**: Always verify dataset integrity using cryptographic hashes. Do not rely on URL stability. Use tools like DVC for hash-based integrity tracking.
2. **Mirror locally**: Download and snapshot datasets to internal storage rather than re-fetching from external URLs at training time. This eliminates split-view and namespace reuse attacks.
3. **Version-pin datasets**: Reference specific dataset versions or commits (e.g., Hugging Face dataset revisions with commit hashes) rather than "latest." This is the dataset equivalent of dependency pinning.
4. **Quarantine before use**: Following NSA guidance, quarantine externally sourced data and run automated content scanning (PII, CSAM, copyright, poisoning indicators) in an isolated environment before any training use.
5. **Namespace validation**: Verify model and dataset author identity on platforms like Hugging Face. Check for typosquatting and namespace reuse by confirming the publishing account's history and activity.
6. **Document in AI BOM**: Capture provenance, license, preprocessing steps, known limitations, and data subject descriptions for every dataset. Align with EU AI Act Article 10 documentation requirements.
7. **Contractual controls**: When procuring datasets from third parties, include security requirements in contracts covering data handling, audit rights, incident response, and retention policies per the NSA/CISA guidance.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **6.5.1** | **Verify that** external datasets undergo poisoning risk assessment (e.g., data fingerprinting, outlier detection). | 1 | **Training data poisoning.** An attacker injects crafted samples into a public dataset to cause the trained model to exhibit attacker-chosen behaviors. As few as 100–500 poisoned samples achieve >60% attack success rates in healthcare AI (2026 analytical framework). Poisoning 0.01% of LAION-400M costs ~$60 via split-view attacks (Carlini et al. 2023). Backdoor triggers embedded in training repos activate months post-training (Basilisk Venom). Safetensors conversion services on Hugging Face have been shown exploitable for model injection. (MITRE ATLAS AML.T0020; OWASP LLM04:2025; PoisonBench ICML) | Verify that a data validation pipeline exists and runs on all external datasets before training. Check for: statistical outlier detection (isolation forests, z-score analysis), data fingerprinting to detect known poison patterns, label-consistency checks, duplicate/near-duplicate detection, hash verification against approved versions, and loss-trajectory analysis for backdoor indicators. Tools: Great Expectations for schema/distribution constraints, Cleanlab for label errors and near-duplicates, GBDR for capacity-effect-based backdoor detection (open-source, validated on 4 benchmarks), BaDLoss for multiple simultaneous backdoor detection, DVC/lakeFS for version tracking, PoisonBench for vulnerability assessment. Quarantine externally sourced data per NSA/CISA guidance before moving to internal systems. | Poisoning detection is an active research area with no silver-bullet solution. Clean-label attacks remain significantly harder to detect than dirty-label. Detection delays in healthcare AI commonly range 6–12 months and may extend to years in privacy-constrained environments. Synthetic data propagation ("Virus Infection Attack") compounds contamination across model generations, making provenance tracking essential. GBDR (peer-reviewed, open-source) and BaDLoss represent the current state-of-the-art but are not yet widely deployed in production pipelines. MEDLEY (ensemble disagreement monitoring) shows promise for high-stakes domains. Organizations should layer multiple detection methods and accept residual risk. |
| **6.5.2** | **Verify that** disallowed content (e.g., copyrighted material, PII) is detected and removed via automated scrubbing prior to training. | 1 | **Legal liability from training on copyrighted or personal data.** Models trained on copyrighted content face litigation risk (NYT v. OpenAI, Getty v. Stability AI). Models trained on PII can memorize and regurgitate personal data, violating GDPR, CCPA, and the EU AI Act (Article 10, enforcement August 2026). Penalties under the EU AI Act reach €10M or 2% of global turnover. | Confirm that a content-filtering pipeline runs before training, including: PII detection and redaction (Microsoft Presidio, PiiCatcher for databases, Hawk-Eye for multimodal content including OCR on 350+ file types, spaCy NER, regex patterns for SSN/email/phone), copyright/license detection for code datasets (ScanCode, REUSE), NSFW/harmful content classifiers for image/text data, and CSAM scanning. Verify that filtered records are logged for audit and that the pipeline respects copyright opt-outs per the EU Copyright Directive. | PII detection in unstructured text has significant false-negative rates, especially for non-English content or domain-specific identifiers. Copyright detection is legally ambiguous — "substantial similarity" is a legal judgment, not a technical measurement. The EU AI Act requires demonstrable compliance with copyright opt-outs, creating a new documentation burden. Best-effort scrubbing is necessary but not sufficient for full legal protection. |
| **6.5.3** | **Verify that** origin, lineage, and license terms for datasets are captured in AI BOM entries. | 2 | **Undisclosed data provenance creating compliance blind spots.** Without documented lineage, organizations cannot respond to legal challenges, regulatory inquiries, or data subject access requests. The EU AI Act mandates full data lineage tracking for high-risk AI systems (enforcement August 2026). The NSA/CISA March 2026 guidance explicitly calls for AI Bills of Materials documenting all dataset components. A June 2025 survey found 48% of organizations falling behind on even basic SBOM requirements — ML-BOM adoption is substantially lower. | Audit AI BOM entries for dataset components. Each should include: source URL or provider, collection date, license identifier (SPDX format), data subjects description (if applicable), preprocessing steps applied, known limitations or biases, and copyright opt-out compliance status. Verify entries use a machine-readable standard: CycloneDX 1.7 (2025, with dataset provenance citations) or SPDX 3.0 (2024, with AI/Dataset profiles). Cross-reference with dataset documentation (Datasheets for Datasets, Croissant metadata). For cryptographic provenance chains, evaluate TAIBOM (Oxford 2025, chain-of-trust attestation) or AIBoMGen (CAIN 2026, automated generation with in-toto attestations). Verify that DVC/lakeFS or equivalent tracks dataset revisions with immutable history. Confirm lineage diagrams and usage approvals exist per EU AI Act requirements. Check the OWASP AI-BOM project for evolving best practices. | The "Datasheets for Datasets" framework (Gebru et al. 2021) provides a template, but adoption is inconsistent. Many popular datasets (especially web-scraped ones) lack adequate documentation. CycloneDX 1.7 and SPDX 3.0 both now support ML components, but they are not yet seamlessly interoperable across AI ecosystems. TAIBOM and AIBoMGen represent the cutting edge of cryptographic provenance tracking but are still in academic/proof-of-concept stages. The Croissant metadata format (MLCommons) is gaining traction but still emerging. Organizations should align documentation practices with EU AI Act Article 10, NSA/CISA AI BOM guidance, and the OWASP AI-BOM project recommendations. |
| **6.5.4** | **Verify that** bias metrics (e.g., demographic parity, equal opportunity) are calculated before dataset approval. | 2 | **Biased training data leading to discriminatory model outputs.** Datasets with demographic imbalances or label bias produce models that perform unequally across protected groups, creating legal risk under anti-discrimination law and the EU AI Act's fairness requirements for high-risk systems. As of 2026, 78% of companies use AI in at least one business function, making bias detection a mainstream operational concern. | Confirm that bias analysis is part of the dataset approval workflow. Check for: demographic distribution analysis across protected attributes (where available), label-distribution analysis by demographic group, comparison against benchmark fairness metrics (demographic parity, equalized odds, calibration). Tools: Fairlearn (Microsoft, open-source), AI Fairness 360 (IBM, 70+ metrics, 13 mitigation algorithms), What-If Tool (Google), Fiddler AI (continuous production monitoring), Arthur AI (bias drift alerts). Verify that bias assessments are documented and versioned alongside dataset approvals. | Bias measurement requires demographic metadata, which may not be available or appropriate to collect. Proxy-based bias detection is an alternative but less reliable. The appropriate fairness metric is domain- and context-dependent — there is no universal "correct" metric. Production tools like Fiddler AI and Arthur AI now enable continuous bias monitoring post-deployment, but pre-training dataset bias assessment remains the primary control point. |
| **6.5.5** | **Verify that** periodic monitoring detects drift or corruption in hosted datasets. | 3 | **Post-approval dataset modification or degradation.** Datasets hosted on third-party platforms can be modified after initial approval (either maliciously or accidentally). Model namespace reuse attacks on Hugging Face, Vertex AI, and Azure AI Foundry can silently replace approved datasets with compromised versions. Web-scraped datasets drift naturally as source content changes. Stored datasets can suffer silent corruption. | Verify that a monitoring process exists for datasets that are hosted externally or re-fetched periodically. Checks should include: hash comparison against the approved version (DVC, lakeFS), statistical distribution comparison (PSI, KL divergence, KS tests, Jensen-Shannon divergence), automated re-running of data quality checks on updated versions, and namespace/author identity verification on model hub platforms. Tools: EvidentlyAI (open-source drift reports), WhyLabs (Apache 2 licensed, continuous monitoring), Arize AI (embedding drift detection for RAG datasets). Alert on deviations beyond defined thresholds. | For static downloaded datasets, integrity monitoring is straightforward (hash checks). For streaming or periodically re-scraped datasets, drift monitoring is substantially more complex and requires statistical infrastructure. Namespace reuse and typosquatting attacks add a supply-chain dimension to monitoring that is not addressed by statistical drift detection alone. Level 3 reflects the operational maturity required. |

---

## Related Standards & References

- [MITRE ATLAS AML.T0020 — Poison Training Data](https://atlas.mitre.org/techniques/AML.T0020)
- [Carlini et al. — Poisoning Web-Scale Training Datasets is Practical (2023)](https://arxiv.org/abs/2302.10149)
- [NSA/CISA — AI/ML Supply Chain Risks and Mitigations (March 2026)](https://techinformed.com/nsa-and-allies-issue-ai-supply-chain-risk-guidance/)
- [EU AI Act Article 10 — Data Governance for High-Risk AI](https://scalevise.com/resources/eu-ai-act-2026-changes/)
- [Palo Alto Unit 42 — Model Namespace Reuse Supply Chain Attack](https://unit42.paloaltonetworks.com/model-namespace-reuse/)
- [ReversingLabs — Malicious ML Models on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- [Gebru et al. — Datasheets for Datasets (2021)](https://arxiv.org/abs/1803.09010)
- [MLCommons Croissant Metadata Format](https://mlcommons.org/working-groups/data/croissant/)
- [Microsoft Presidio — PII Detection](https://microsoft.github.io/presidio/)
- [Cleanlab — Data-Centric AI](https://cleanlab.ai/)
- [DVC — Data Version Control](https://dvc.org/)
- [EvidentlyAI — ML Monitoring and Data Drift](https://www.evidentlyai.com/)
- [WhyLabs — AI Observability](https://whylabs.ai/)
- [IBM AI Fairness 360](https://aif360.mybluemix.net/)
- [Microsoft Fairlearn](https://fairlearn.org/)
- [Great Expectations — Data Validation](https://greatexpectations.io/)
- [LAION Re-LAION-5B — Transparent Iteration with Safety Fixes](https://laion.ai/blog/relaion-5b/)
- [Stanford Internet Observatory — CSAM in LAION-5B](https://incidentdatabase.ai/reports/3555/)
- [Birhane et al. — Into the LAION's Den: Investigating Hate in Multimodal Datasets (2023)](https://arxiv.org/abs/2311.03449)
- [LAION v. Kneschke — TDM Exception Ruling (2024)](https://communia-association.org/2024/10/11/laion-vs-kneschke-building-public-datasets-is-covered-by-the-tdm-exception/)
- [Lakera — Training Data Poisoning: 2026 Perspective](https://www.lakera.ai/blog/training-data-poisoning)
- [Data Provenance Initiative](https://dataprovenance.org/)
- [OWASP LLM04:2025 — Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- [OWASP AI-BOM Project](https://owasp.org/www-project-aibom/)
- [CycloneDX ML-BOM Capabilities](https://cyclonedx.org/capabilities/mlbom/)
- [TAIBOM — Trustworthy AI Bill of Materials (Oxford, 2025)](https://arxiv.org/abs/2510.02169)
- [AIBoMGen — AI BOM Generation for Secure Model Training (CAIN 2026)](https://arxiv.org/abs/2601.05703)
- [HiddenLayer — Silent Sabotage: Hijacking Safetensors Conversion on Hugging Face](https://hiddenlayer.com/innovation-hub/silent-sabotage/)
- [GBDR — Generalizable Backdoor Detection and Removal Framework (2025)](https://www.sciencedirect.com/science/article/abs/pii/S0031320325014293)
- [Data Poisoning Vulnerabilities Across Healthcare AI Architectures (2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12881903/)
- [Palo Alto Networks — What Is an AI-BOM?](https://www.paloaltonetworks.com/cyberpedia/what-is-an-ai-bom)

---

## Open Research Questions

- How can poisoning detection scale to web-scale datasets (billions of examples) without prohibitive compute costs? GBDR and BaDLoss show promise in benchmarks, but production deployment at scale remains unproven. Can loss-trajectory and capacity-effect approaches work efficiently on billion-sample datasets?
- What legal frameworks will emerge for dataset liability — is the dataset provider, the model trainer, or the deployer responsible for content issues? The EU AI Act places obligations on deployers of high-risk systems, but the supply chain liability chain remains unclear.
- How should organizations handle "inherited bias" when fine-tuning on a clean dataset but starting from a base model trained on a biased one?
- Can data provenance be established retroactively for models already in production that were trained on insufficiently documented datasets?
- Given that split-view poisoning costs as little as $60 for web-scale datasets, should URL-based dataset distribution be considered fundamentally insecure? What alternative distribution models (content-addressed storage, IPFS-pinned datasets) could replace it?
- How should model hub platforms (Hugging Face, Vertex AI, Azure AI Foundry) address namespace reuse and typosquatting attacks at the platform level, rather than placing the burden on individual consumers?
- As synthetic data becomes a larger share of training corpora, how do organizations prevent the "Virus Infection Attack" pattern where poisoning propagates invisibly across model generations?
- What automated tooling is needed to continuously monitor the domain registration status of URLs within active training datasets?
- With the EU AI Act's high-risk system requirements fully applicable from August 2026, what practical workflows can organizations adopt to demonstrate Article 10 data governance compliance at scale?
- Can cryptographic provenance frameworks like TAIBOM and AIBoMGen achieve industry-wide adoption, or will the AI BOM landscape fragment between CycloneDX and SPDX ecosystems?
- Given that healthcare AI poisoning detection delays average 6–12 months, what monitoring architectures (e.g., MEDLEY-style ensemble disagreement) can reduce detection time to operationally acceptable windows?
