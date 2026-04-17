# C01: Training Data Integrity & Traceability

> **Source:** [`1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
> **Requirements:** 26 | **Sections:** 5

## Control Objective

Training data must be sourced, handled, and maintained in a way that preserves origin traceability, integrity, and quality. The core security concern is ensuring data has not been tampered with, poisoned, or corrupted. Security-relevant bias (e.g., skewed abuse-detection training data that allows attackers to bypass controls) is treated as a possible consequence of compromised or unvalidated data, not as a standalone control category.

> **Scope note -- bias.** AISVS addresses bias only where it introduces security risk (e.g., bypass of abuse detection, authentication heuristics, or automated trust decisions). Broader fairness governance requirements are out of scope; see e.g. ISO/IEC 42001 or the NIST AI RMF for general fairness and ethics guidance.

> **Scope note -- general data security.** Generic data security control details for access control, logging, encryption at rest and in transit, and data retention/purging are covered by ASVS v5 (V8, V11, V12, V14, V16) and apply to training data storage and labeling systems. C1 sets the higher-level requirements with levels that are specific to AI — reviewers should pair C1 controls with the corresponding ASVS v5 chapters rather than re-implementing generic data security guidance here. This scope note was added to the AISVS source in the April 2026 C01 reduction pass.

> **2025-2026 Highlights:** The training data threat landscape sharpened dramatically. Anthropic/UK AISI/Turing (Oct 2025) showed only 250 documents can backdoor any-size LLM — absolute count matters, not proportion. Nature Medicine (Dec 2024) showed 0.001% medical token poisoning evades standard benchmarks entirely. The Virus Infection Attack (NeurIPS 2025) proved poisoning propagates through synthetic data pipelines, amplifying across model generations. Microsoft Security (Feb 2026) published the first at-scale backdoor detection approach, using "double triangle" attention patterns and trigger-induced entropy collapse as observable signatures. On the regulatory front, California AB 2013 took effect January 1, 2026 — the Central District of California denied xAI's preliminary injunction on March 4, 2026, and OpenAI and Anthropic both posted structured training data disclosures. MITRE ATLAS v5.4.0 (Feb 2026) now holds 16 tactics, 84 techniques, and 56 sub-techniques, up from 15/66 in October 2025, with added agentic attack coverage (context poisoning, memory manipulation, thread injection). Tooling advanced with the OpenSSF Model Signing (OMS) v1.0 specification adopted by NVIDIA NGC and Google Kaggle, Datasig (Trail of Bits) for dataset fingerprinting, CodeScan (Mar 2026) as the first poisoning scanner for code gen models, lakeFS acquiring DVC (Nov 2025), OpenLineage gaining traction as the lineage standard, and source-free certified unlearning (Sep 2025) offering a practical direction for GDPR erasure without full retraining.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C1.1 | Training Data Origin & Traceability | 4 | [C01-01-Training-Data-Origin-Traceability](C01-01-Training-Data-Origin-Traceability.md) |
| C1.2 | Training Data Security & Integrity | 7 | [C01-02-Training-Data-Security-Integrity](C01-02-Training-Data-Security-Integrity.md) |
| C1.3 | Data Labeling and Annotation Security | 5 | [C01-03-Data-Labeling-Annotation-Security](C01-03-Data-Labeling-Annotation-Security.md) |
| C1.4 | Training Data Quality and Security Assurance | 6 | [C01-04-Training-Data-Quality-Security-Assurance](C01-04-Training-Data-Quality-Security-Assurance.md) |
| C1.5 | Data Lineage and Traceability | 4 | [C01-05-Data-Lineage-Traceability](C01-05-Data-Lineage-Traceability.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Data poisoning attacks** -- As of October 2025, Anthropic/UK AISI/Turing Institute demonstrated that as few as **250 malicious documents** (~0.00016% of training tokens) can backdoor LLMs from 600M to 13B parameters, with success nearly constant across model sizes ([arXiv:2510.07192](https://arxiv.org/abs/2510.07192)). CyLab/CMU showed poisoning just 0.1% of pre-training data persists through post-training safety alignment (ICLR 2025). Techniques include backdoor injection (BadNets, Trojan attacks), clean-label attacks, triggerless attacks, and data augmentation poisoning (MITRE ATLAS AML.T0020, AML.T0020.000–002).
- **Training data extraction / memorization attacks** -- A July 2025 comprehensive survey ([arXiv:2507.05578](https://arxiv.org/abs/2507.05578)) found divergence attacks extract up to 150x more training data than normal queries, soft prompting increases PII leakage by 9.3%, and memorization scales log-linearly with model size. USENIX Security 2025 demonstrated PII extraction from LLMs without jailbreaks via augmented few-shot prompting. De-duplication of training data reduces memorization by 10x.
- **Supply chain compromise of ML platforms** -- NullifAI attack (Feb 2025) placed malicious models on Hugging Face evading Picklescan via 7z compression, creating reverse shells. NullBulge campaign (2024–2025) weaponized ComfyUI extensions and distributed LockBit ransomware via AI platforms. torchtriton PyPI typosquatting (2024) infiltrated thousands of ML environments. Carlini et al. showed poisoning 0.01% of LAION-400M costs ~$60 via split-view and frontrunning attacks.
- **Label-flipping attacks on crowdsourced annotation pipelines** -- malicious annotators systematically mislabel samples to introduce targeted biases (MITRE ATLAS AML.T0020.001)
- **Medical AI poisoning** -- A Nature Medicine study (Dec 2024) showed poisoning just 0.001% of medical training tokens increased harmful LLM outputs by 7–11%, while corrupted models matched performance on standard benchmarks — making poisoning invisible to routine evaluation. A biomedical knowledge graph-based screening captured 91.9% of harmful content (F1 = 85.7%).
- **Code generation poisoning** -- Stealthy attacks inject syntactically valid but vulnerable code patterns into training data for code-generation LLMs (CodeBERT, CodeT5+, AST-T5). As of August 2025, evaluation of spectral signatures, activation clustering, and static analysis found all three methods struggle against triggerless poisoning in code generators ([arXiv:2508.21636](https://arxiv.org/abs/2508.21636)). CodeScan (Mar 2026) is the first scanning framework tailored to code generation, achieving 97%+ detection accuracy via AST-based normalization and iterative divergence analysis ([arXiv:2603.17174](https://arxiv.org/abs/2603.17174)).
- **Synthetic data poisoning propagation** -- The Virus Infection Attack (VIA, NeurIPS 2025 spotlight) demonstrated that poisoned content propagates through synthetic data generation pipelines, bypassing standard defenses. VIA conceals payloads within protective "shells" and hijacks benign samples to maximize malicious content in downstream synthetic data, achieving attack success rates comparable to directly poisoned models ([arXiv:2509.23041](https://arxiv.org/abs/2509.23041)).
- **Backdoor via harmless inputs** -- A 2025 study showed that robust associations between triggers and affirmative responses can be established using entirely benign question-answer pairs, circumventing safety-aligned guardrails that would otherwise filter overtly poisoned samples. This makes detection significantly harder since the poisoned data contains no harmful content on its own.
- **Social media data poisoning** -- The Grok 4 "!Pliny" incident demonstrated that training on unfiltered social media data saturated with jailbreak prompts can embed exploitable triggers in production models. Typing a specific username was enough to strip guardrails entirely, illustrating how adversaries can poison models through public data channels without direct pipeline access.
- **Repository-based poisoning (Basilisk Venom)** -- In January 2025, hidden prompts embedded in GitHub code comments poisoned fine-tuned models including DeepSeek's DeepThink-R1, creating backdoors that responded to specific phrases with attacker-planted instructions.
- **Preference learning poisoning** -- PoisonBench (ICML 2025) evaluated 22 LLMs across two attack types (content injection and alignment deterioration) and found that scaling model size does not reliably improve resilience, attack success follows a log-linear relationship with poison ratio, and poisoning effects generalize to extrapolated triggers ([arXiv:2410.08811](https://arxiv.org/abs/2410.08811)).
- **Data ordering attacks** -- manipulating the sequence of training data to influence gradient updates without changing data content
- **Model namespace reuse (supply-chain takeover)** -- Palo Alto Unit 42 documented in 2026 that when a Hugging Face or similar hub account is deleted, the freed namespace can be re-registered by an adversary who then uploads a poisoned or backdoored model under the same identifier. Existing pipeline code that pulls by model name (without pinning to a signed digest) now silently loads the attacker's model. In March 2025 researchers estimated that 23% of the top 1,000 most-downloaded Hugging Face models had been compromised at some point through this and related vectors.
- **Backdoor detection evasion via observable signatures** -- In February 2026 Microsoft Security published an at-scale detection approach that identifies a "double triangle" pattern in attention distributions between benign and trigger tokens and a characteristic collapse in output entropy when triggers are present. Attackers aware of these indicators can design poisoning strategies that flatten the attention pattern or preserve entropy — the defender/attacker cat-and-mouse is now moving into the interpretability layer.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2017 | BadNets: Identifying Vulnerabilities in the ML Supply Chain (Gu et al.) | Foundational backdoor poisoning attack via training data | [arXiv:1708.06733](https://arxiv.org/abs/1708.06733) |
| 2020 | Radioactive Data: Tracing Through Training (Sablayrolles et al.) | Dataset fingerprinting technique relevant to C1.1.4 | [arXiv:2002.00937](https://arxiv.org/abs/2002.00937) |
| 2021 | Extracting Training Data from Large Language Models (Carlini et al.) | Demonstrated verbatim training data extraction from GPT-2 | [arXiv:2012.07805](https://arxiv.org/abs/2012.07805) |
| 2023 | Poisoning Web-Scale Training Datasets is Practical (Carlini et al.) | Showed practical poisoning of LAION-400M for ~$60 via split-view/frontrunning | [arXiv:2302.10149](https://arxiv.org/abs/2302.10149) |
| 2024 | Nightshade: Prompt-Specific Poisoning Attacks on Text-to-Image Models | Targeted poisoning attack against diffusion models | [IEEE S&P 2024](https://arxiv.org/abs/2310.13828) |
| 2024 | torchtriton PyPI typosquatting attack | Malicious package masquerading as PyTorch dependency infiltrated thousands of ML environments | [MITRE ATLAS AML.T0010.001](https://atlas.mitre.org/) |
| 2024–2025 | NullBulge supply chain campaign | Weaponized ComfyUI extension on GitHub, distributed LockBit ransomware via AI platforms | [The Hacker News](https://thehackernews.com/2025/11/cisos-expert-guide-to-ai-supply-chain.html) |
| Jan 2025 | DeepSeek database exposure (Wiz Research) | 1M+ log entries including chat history, API keys exposed via unprotected ClickHouse ports | [Wiz Research](https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak) |
| Feb 2025 | NullifAI malicious models on Hugging Face | Evaded Picklescan via 7z compression, created reverse shells across OS platforms | [ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face) |
| Jun 2025 | Persistent Pre-Training Poisoning (CyLab/CMU, ICLR 2025) | 0.1% poisoning persists through post-training safety alignment for DoS, belief manipulation, prompt stealing | [arXiv:2410.13722](https://arxiv.org/abs/2410.13722) |
| Jul 2025 | Comprehensive LLM Memorization Survey | Divergence attacks extract 150x more training data; de-duplication reduces memorization 10x | [arXiv:2507.05578](https://arxiv.org/abs/2507.05578) |
| Oct 2025 | 250-Document Poisoning (Anthropic/UK AISI/Turing) | Only 250 documents needed to backdoor LLMs at any scale; absolute count matters, not proportion | [Anthropic Research](https://www.anthropic.com/research/small-samples-poison) |
| 2025 | PII Extraction Without Jailbreaks (USENIX Security 2025) | Extracted names, emails, phone numbers from LLMs via direct querying without jailbreaks | [USENIX](https://www.usenix.org/system/files/usenixsecurity25-cheng-shuai.pdf) |
| 2025 | Datasig dataset fingerprinting (Trail of Bits) | First practical dataset fingerprinting tool using MinHash; detects poisoned/modified datasets | [Trail of Bits](https://blog.trailofbits.com/2025/05/02/datasig-fingerprinting-ai/ml-datasets-to-stop-data-borne-attacks/) |
| Dec 2024 | Medical LLM Poisoning (Nature Medicine) | 0.001% token poisoning increased harmful outputs 7–11% while evading standard benchmarks; knowledge graph screening catches 91.9% | [Nature Medicine](https://www.nature.com/articles/s41591-024-03445-1) |
| Dec 2024 | Italian DPA fines OpenAI EUR 15M | GDPR violations in ChatGPT training data: no legal basis, transparency failures, inadequate age verification | [Lewis Silkin](https://www.lewissilkin.com/en/insights/2025/01/14/openai-faces-15-million-fine-as-the-italian-garante-strikes-again-102jtqc) |
| Aug 2025 | Stealthy Code Gen Poisoning Study | Spectral signatures, activation clustering, and static analysis all fail against triggerless poisoning in code generators | [arXiv:2508.21636](https://arxiv.org/abs/2508.21636) |
| Dec 2025 | CSA Data Security within AI Environments | AI Controls Matrix controls DSP-21 through DSP-28 for training data poisoning, integrity, PETs, and shadow AI | [CSA](https://cloudsecurityalliance.org/artifacts/data-security-within-ai-environments) |
| Sep 2025 | Virus Infection Attack (VIA) on LLMs (NeurIPS 2025 spotlight) | Poisoning propagates through synthetic data pipelines; payloads survive generation and amplify across model generations | [arXiv:2509.23041](https://arxiv.org/abs/2509.23041) |
| 2025 | PoisonBench: LLM Preference Learning Poisoning (ICML 2025) | First benchmark for preference poisoning; 22 models tested, scaling doesn't help, log-linear attack/poison ratio | [arXiv:2410.08811](https://arxiv.org/abs/2410.08811) |
| Jan 2025 | Basilisk Venom — GitHub code comment poisoning | Hidden prompts in code comments backdoored DeepSeek DeepThink-R1 during fine-tuning | [Lakera](https://www.lakera.ai/blog/training-data-poisoning) |
| 2025 | Grok 4 "!Pliny" social media data poisoning | Jailbreak prompts saturated in X posts created exploitable trigger in production model | [Lakera](https://www.lakera.ai/blog/training-data-poisoning) |
| Feb 2025 | Atlas: ML Lifecycle Provenance Framework | C2PA + SLSA + in-toto attestable pipelines with TEE support; <8% training overhead; Kubeflow integration | [arXiv:2502.19567](https://arxiv.org/abs/2502.19567) |
| Mar 2026 | CodeScan: Poisoning Detection for Code Gen LLMs | First scanning framework for code generation models; 97%+ accuracy via AST normalization across 108 models | [arXiv:2603.17174](https://arxiv.org/abs/2603.17174) |
| Feb 2026 | Microsoft Security — Detecting Backdoored Language Models at Scale | Identified attention "double triangle" pattern and output-entropy collapse as observable backdoor signatures; framed as practical detection for hub-scale scanning | [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/02/04/detecting-backdoored-language-models-at-scale/) |
| Feb 2026 | MITRE ATLAS v5.4.0 | 16 tactics, 84 techniques, 56 sub-techniques (up from 15/66 in Oct 2025); added agentic techniques: AI Agent Context Poisoning, Memory Manipulation, Thread Injection | [MITRE ATLAS](https://atlas.mitre.org/) |
| 2026 | Model Namespace Reuse (Palo Alto Unit 42) | Deleted Hugging Face/hub accounts release namespaces; attackers re-register them and upload poisoned models that existing pipelines silently pull by name | [Unit 42](https://unit42.paloaltonetworks.com/model-namespace-reuse/) |
| Mar 2026 | xAI v. AB 2013 ruling | US District Court (C.D. Cal.) denied xAI's preliminary injunction against California AB 2013; OpenAI and Anthropic both posted structured training data disclosures in response | [Norton Rose Fulbright](https://www.nortonrosefulbright.com/en-us/knowledge/publications/c1df8419/california-district-court-upholds-transparency-requirements-for-generative-ai-training-data) |
| Apr 2026 | OWASP AISVS C01 reduction pass | Source removed dedicated tamper-evident audit log requirement (old 1.3.5), folding it into the 1.3.2 audit log requirement; new scope note added deferring generic access control, logging, encryption, and retention to ASVS v5 (V8, V11, V12, V14, V16) | [AISVS commit de0baa0](https://github.com/OWASP/AISVS/commit/de0baa0) |
| Sep 2025 | Source-Free Certified Unlearning | Demonstrated certified unlearning using a surrogate dataset rather than original training data; performance comparable to full retraining at a fraction of compute — practical step toward GDPR erasure for production LLMs | [IAPP: AI right to unlearn](https://iapp.org/news/a/the-ai-right-to-unlearn-reconciling-human-rights-with-generative-systems) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls (as of March 2026):

- **Data provenance & versioning:** [lakeFS](https://lakefs.io) (acquired DVC in Nov 2025; git-like branching for data lakes with immutable snapshots), [DVC](https://dvc.org) (now under lakeFS stewardship), [MLflow](https://mlflow.org) (experiment tracking, partial lineage), Delta Lake
- **Poisoning detection:** [Cleanlab v2.9.0](https://github.com/cleanlab/cleanlab) (Jan 2025; confident learning for label errors, outliers, spurious correlations; dropped TensorFlow, PyTorch-focused), [IBM ART v1.20+](https://github.com/Trusted-AI/adversarial-robustness-toolbox) (Neural Cleanse, Activation Clustering, Spectral Signatures, STRIP), [Lakera](https://www.lakera.ai) (commercial SaaS for poisoning detection), [CodeScan](https://arxiv.org/abs/2603.17174) (Mar 2026; first poisoning scanner for code generation models, 97%+ accuracy via AST normalization and iterative divergence analysis; tested across 108 models on three architectures)
- **Data integrity & signing:** Cryptographic hashing (SHA-256), [Sigstore model-transparency v1.0](https://github.com/sigstore/model-transparency) (Apr 2025; signs ML models with OIDC identity; adopted by NVIDIA NGC and Google Kaggle), [OpenSSF Model Signing (OMS) specification](https://github.com/ossf/model-signing-spec) (industry spec for signing AI models and related artifacts; the OMS detached signature format represents multiple related artifacts — model weights, configuration files, tokenizers, and datasets — as one verifiable unit, so dataset signing is now reachable through the same pipeline rather than a separate workflow), Great Expectations, Pandera. The NSA/CISA/FBI Joint CSI on AI Data Security (May 2025) recommends adopting quantum-resistant digital signature standards for dataset authentication across training, fine-tuning, and RLHF pipelines.
- **Dataset fingerprinting:** [Datasig](https://blog.trailofbits.com/2025/05/02/datasig-fingerprinting-ai/ml-datasets-to-stop-data-borne-attacks/) (Trail of Bits, May 2025; MinHash-based fingerprints for detecting poisoned/modified datasets; prototype stage, 5% error margin)
- **Lineage:** Apache Atlas, [DataHub](https://datahubproject.io) (metadata platform with lineage graphs), Amundsen, MLflow, [OpenLineage](https://openlineage.io/) (open standard for lineage metadata collection; integrations with Airflow, Spark, Flink, dbt, Snowflake; backed by Marquez reference implementation; gaining rapid adoption as industry standard as of 2026)
- **Attestable ML pipelines:** [Atlas framework](https://arxiv.org/abs/2502.19567) (Feb 2025; combines C2PA, SLSA, and in-toto for fully attestable ML pipelines with TEE-backed provenance chains; <8% training overhead; Kubeflow integration; research prototype)
- **PII detection:** [Microsoft Presidio](https://microsoft.github.io/presidio/) (text/image/structured data; integrated with Hugging Face Hub), [AWS Macie](https://aws.amazon.com/macie/), Google Cloud DLP
- **Labeling platforms:** [Label Studio Enterprise](https://humansignal.com/platform/) (RBAC, SSO/SAML, audit logs, QA workflows; 2025 analytics tab), [Labelbox](https://labelbox.com) (SOC 2, RBAC, audit trails), [Encord](https://encord.com) (HIPAA/SOC 2), Scale AI, Snorkel
- **Bias evaluation:** Fairlearn, AI Fairness 360, custom red-team probing
- **Adversarial robustness:** IBM ART, Foolbox, CleverHans
- **Machine unlearning:** Still no production-ready tools as of April 2026, but the research front is moving. Active venues: ICML 2025 MUGen workshop, [CVPR 2026 MUV workshop](https://machine-unlearning-for-vision.github.io/) (covering data-centric removal, parameter-centric fine-tuning, and training-free steering via refusal vectors). A September 2025 result on [source-free certified unlearning](https://iapp.org/news/a/the-ai-right-to-unlearn-reconciling-human-rights-with-generative-systems) showed certified erasure using a surrogate dataset rather than the original training data, with performance comparable to full retraining at a fraction of compute — the first approach that looks plausible for a live GDPR erasure request against a deployed LLM. Production approaches today still fall back on full retraining, targeted fine-tuning, or approximate methods with unverified guarantees.
- **Platform security:** [Hugging Face Hub](https://huggingface.co/docs/hub/en/security) (Oct 2025: VirusTotal scanning of 2.2M+ repos; JFrog partnership for ML supply chain transparency; Sigstore integration in development)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C1.1 Training Data Origin & Traceability | Medium | Data catalogs exist (DataHub, Amundsen) but metadata completeness enforcement is manual. Dataset watermarking (1.1.4) improving — Datasig (Trail of Bits, 2025) is a first practical fingerprinting tool but remains prototype-stage. California AB 2013 (effective Jan 2026) now legally mandates training data documentation. |
| C1.2 Training Data Security & Integrity | High | Cloud-native encryption and IAM are mature. Sigstore model-transparency v1.0 (Apr 2025) signs models; the OpenSSF Model Signing (OMS) spec extends the same detached-signature format to datasets and tokenizers, making dataset signing reachable through the existing pipeline rather than a separate workflow. lakeFS acquisition of DVC (Nov 2025) consolidates the data versioning ecosystem. Gaps: pipeline-level access control, large-scale integrity monitoring. Immutable versioning (1.2.7) adds cost. Machine unlearning for 1.2.6 is still research-only, though source-free certified unlearning (Sep 2025) is the first result that looks plausible for production GDPR erasure. |
| C1.3 Data Labeling and Annotation Security | Medium | Label Studio Enterprise added analytics tab (2025); Encord emerging with HIPAA/SOC 2 posture. Commercial platforms have RBAC and audit logging. Cryptographic signing of annotations and labeling artifacts (1.3.4) still requires custom implementation. The April 2026 AISVS reduction pass folded the tamper-evident audit log requirement back into 1.3.2, so reviewers should now expect audit logging controls to carry the tamper-evidence burden directly rather than look for a dedicated requirement. |
| C1.4 Training Data Quality and Security Assurance | Medium | Cleanlab v2.9.0 (Jan 2025) mature for label error/outlier detection. IBM ART v1.20+ comprehensive for adversarial defenses. CodeScan (Mar 2026) is the first poisoning scanner purpose-built for code generation models. Key gap: Anthropic's Oct 2025 research shows only 250 documents can poison any-size LLM, making detection thresholds critical. Nature Medicine (Dec 2024) showed 0.001% poisoning evades standard benchmarks entirely. Adversarial training (1.4.4) still 2-10x compute cost. Security-exploitable bias evaluation (1.4.6) lacks dedicated tooling. |
| C1.5 Data Lineage and Traceability | Medium | Dataset-level lineage supported by lakeFS, DataHub, MLflow, and increasingly OpenLineage as an open standard. The Atlas framework (Feb 2025) demonstrated fully attestable ML pipelines using C2PA + SLSA + in-toto with TEE support but remains a research prototype. Record-level lineage and synthetic data tracking are immature. Immutable lineage storage requires deliberate architecture. FTC algorithmic disgorgement pattern (6 enforcement actions 2019–2025) makes lineage a regulatory survival requirement. |

---

## Open Research Questions

- [ ] How do you verify data integrity for datasets too large to hash in full? (Merkle-tree and sampling approaches exist but lack standardization; Datasig's MinHash fingerprinting is a promising direction but prototype-stage)
- [ ] What is the state of automated poisoning detection for multimodal datasets? (Most tooling targets tabular or image data; text and audio poisoning detection is less developed)
- [ ] How should organizations handle training data provenance for foundation models they did not train? (Model cards and data cards help but are not verifiable; California AB 2013 mandates disclosure starting Jan 2026)
- [ ] What constitutes adequate label quality assurance for adversarial-risk-sensitive domains? (No industry consensus on sampling rates or acceptance thresholds)
- [ ] Can machine unlearning satisfy data deletion requirements (C1.2.6) for data embedded in model weights? (Active research at ICML 2025 MUGen and CVPR 2026 MUV workshops, but no production-ready solutions. EDPB made right to erasure its 2025 coordinated enforcement priority — regulatory pressure is accelerating.)
- [ ] How should synthetic data lineage be standardized across generation tools and ML pipelines? (No common metadata schema exists)
- [ ] Given that only 250 documents can poison any-size LLM (Anthropic, Oct 2025), what detection sensitivity thresholds are practical for web-scale training data pipelines?
- [ ] How should organizations prepare for FTC algorithmic disgorgement risk? (6 enforcement actions to date requiring deletion of models trained on improperly collected data — lineage and versioning requirements become regulatory survival controls)
- [ ] Can poisoning detection methods designed for NLP/vision models transfer to code generation? (Aug 2025 study showed spectral signatures and activation clustering fail against triggerless code gen poisoning; CodeScan is a first step but needs validation beyond the three architectures tested)
- [ ] How can organizations prevent poisoning propagation through synthetic data pipelines? (VIA, NeurIPS 2025, showed contamination amplifies across model generations — screening synthetic data for inherited poisoning is an unsolved problem)
- [ ] What provenance standards should ML pipelines adopt for end-to-end attestability? (The Atlas framework demonstrated C2PA + SLSA + in-toto with TEE support at <8% overhead, but production adoption and standardization remain open questions)
- [ ] Do attention "double triangle" patterns and output-entropy collapse (Microsoft Security, Feb 2026) generalize across model families and training objectives, or are they signatures that an attacker aware of the detection approach can specifically avoid? (First at-scale detection result published; adversarial response is the obvious next step and has not yet been characterized.)
- [ ] How should ML platforms defend against namespace-reuse attacks when pipelines reference models by name rather than signed digest? (Palo Alto Unit 42's 2026 write-up shows the attack works today against Hugging Face and similar hubs; digest pinning, OMS signature verification, and hub-side namespace retention policies are plausible mitigations but not yet standard practice.)

---

## Related Standards & Cross-References

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — March 2025 update emphasizes model provenance, data integrity, and third-party model assessment
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — 13 risks with 400+ actions; notes most developers don't disclose training data sources
- [NISTIR 8596: Cybersecurity Framework Profile for AI](https://www.nist.gov/news-events/news/2025/12/draft-nist-guidelines-rethink-cybersecurity-ai-era) — Dec 2025 draft: "provenance and integrity of training data should be verified as rigorously as software"
- [EU AI Act: Article 10: Data & Data Governance](https://artificialintelligenceact.eu/article/10/) — GPAI training data documentation required since Aug 2025; high-risk system obligations deferred to Dec 2027 under the Nov 2025 [Digital Omnibus proposal](https://digital-strategy.ec.europa.eu/en/library/digital-omnibus-ai-regulation-proposal) (still in EU legislative process as of Mar 2026)
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) — LLM03 (Supply Chain) and LLM04 (Data/Model Poisoning) directly relevant
- [MITRE ATLAS](https://atlas.mitre.org/) — AML.T0020 (Poison Training Data) and sub-techniques; v5.4.0 (Feb 2026) holds 16 tactics, 84 techniques, and 56 sub-techniques (up from 15/66 in Oct 2025), with added agentic techniques including AI Agent Context Poisoning, Memory Manipulation, and Thread Injection
- [CISA Advisory: Securing Data for AI Systems](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a)
- [NSA/AISC: AI Data Security Best Practices](https://techinformed.com/nsa-and-allies-issue-ai-supply-chain-risk-guidance/) (May 2025)
- [California AB 2013: Training Data Transparency Act](https://www.kolmogorovlaw.com/california-ai-compliance-2025-2026-what-your-business-must-do-now) — Effective Jan 1, 2026; requires public training data documentation across 12 enumerated categories for any generative AI system released or substantially modified on or after January 1, 2022. On March 4, 2026 the US District Court for the Central District of California denied xAI's preliminary injunction, and OpenAI and Anthropic both posted structured training data disclosures in response — neither named specific datasets, but both adopted the 12-category format. Enforcement runs through California's Unfair Competition Law, enabling both public and private action.
- [FTC AI Enforcement / Algorithmic Disgorgement](https://www.ftc.gov/industry/technology/artificial-intelligence) — 6 enforcement actions (2019–2025) requiring deletion of models trained on improperly collected data
- [CSA AI Controls Matrix: Data Security within AI Environments](https://cloudsecurityalliance.org/artifacts/data-security-within-ai-environments) (Dec 2025) — Controls DSP-21 (poisoning prevention), DSP-22 (PETs for training data), DSP-23 (dataset versioning), DSP-25–28 (prompt injection, model inversion, federated learning, shadow AI). Recommends Cohen's kappa > 0.8 for annotation inter-rater agreement and 10% expert review sampling.
- [ISO/IEC 42001:2023](https://www.iso.org/standard/42001) — AI management systems; data governance controls covering source quality, lineage, and privacy

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C02 (User Input Validation) | Pipeline integrity, transformation validation | C1 covers training data; C2 covers inference-time data processing. Shared concern: pipeline access controls and integrity checks. |
| C03 (Model Lifecycle) | Adversarial robustness, model versioning | C1.4.4 (adversarial training) relates to model-level robustness controls in C3. C1.2.7 (dataset versioning) pairs with C3 model versioning. |
| C06 (Supply Chain) | Third-party data sources, pre-trained model provenance | C1.1.1 (data inventory) overlaps with supply chain tracking of external datasets. OWASP LLM Top 10 LLM03 spans both chapters. |
| C11 (Adversarial Robustness) | Poisoning detection, adversarial training | C1.4.2/1.4.4 (poisoning detection, adversarial training) directly relate to C11 adversarial hardening controls. |
| C12 (Privacy) | PII in training data, data deletion, memorization | C1.1.2 (feature minimization) and C1.2.6 (data purging) directly relate to privacy controls. USENIX 2025 PII extraction research validates both chapters. |

---

## Community Notes

_Space for contributor observations, discussion, and context that does not fit elsewhere._

---

## Related Pages

- [C01-01 Training Data Origin & Traceability](C01-01-Training-Data-Origin-Traceability.md) — dataset inventory, feature minimization, approval workflows, and dataset fingerprinting that implement the first four requirements of this chapter.
- [C01-05 Data Lineage & Traceability](C01-05-Data-Lineage-Traceability.md) — lineage recording, immutable audit storage, synthetic data tracking, and the OpenLineage / C2PA / OMS tooling landscape referenced here.
- [C03-01 Model Authorization & Integrity](C03-01-Model-Authorization-Integrity.md) — downstream counterpart that verifies signed models at deployment using the same Sigstore and OpenSSF Model Signing pipelines described in C1.2.
- [C06-05 AI BOM & Model Artifacts](C06-05-AI-BOM-Model-Artifacts.md) — CycloneDX ML-BOM and SPDX AI profile work that carries this chapter's dataset provenance claims into supply-chain manifests.
- [C06 Supply Chain](C06-Supply-Chain.md) — chapter hub covering model, framework, and dataset vetting; the natural home for the namespace-reuse and Hugging Face hub threats surfaced here.

---
