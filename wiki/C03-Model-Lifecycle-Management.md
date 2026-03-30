# C03: Model Lifecycle Management & Change Control

> **Source:** [`1.0/en/0x10-C03-Model-Lifecycle-Management.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
> **Requirements:** 26 | **Sections:** 6

## Control Objective

AI systems must implement change control processes that prevent unauthorized or unsafe model modifications from reaching production. Only authorized, validated models reach production by employing controlled processes that maintain integrity, traceability, and recoverability.

> **2025-2026 Highlights:** The AI model supply chain became a top-tier attack surface in 2024-2025, with JFrog documenting a 6.5x increase in malicious models on Hugging Face and Protect AI finding 352K unsafe issues across 51.7K models. The TeamPCP campaign (March 2026) demonstrated cascading supply chain compromise across AI infrastructure -- LiteLLM PyPI packages (97M monthly downloads) were backdoored within five days of the initial Trivy compromise. On the defense side, OpenSSF Model Signing (OMS) v1.0 reached production readiness (April 2025), with NVIDIA signing all NGC Catalog models. The NSA/CISA joint advisory (March 2026) reframed AI as a layered supply chain and recommended cryptographic signing and verified model registries. The GPT-4o sycophancy incident (April 2025) highlighted that even system prompt changes can cause severe behavioral regressions when deployed without staged rollout. NIST AI RMF 1.1 (March 2026) expanded monitoring and evaluation guidance, and EU AI Act GPAI transparency enforcement became active in March 2026.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C3.1 | Model Authorization & Integrity | 4 | [C03-01-Model-Authorization-Integrity](C03-01-Model-Authorization-Integrity.md) |
| C3.2 | Model Validation & Testing | 5 | [C03-02-Model-Validation-Testing](C03-02-Model-Validation-Testing.md) |
| C3.3 | Controlled Deployment & Rollback | 5 | [C03-03-Controlled-Deployment-Rollback](C03-03-Controlled-Deployment-Rollback.md) |
| C3.4 | Secure Development Practices | 4 | [C03-04-Secure-Development-Practices](C03-04-Secure-Development-Practices.md) |
| C3.5 | Hosted and Provider-Managed Model Controls | 4 | [C03-05-Hosted-Provider-Managed-Controls](C03-05-Hosted-Provider-Managed-Controls.md) |
| C3.6 | *(intentionally absent in the standard)* | — | — |
| C3.7 | Fine-Tuning Pipeline Authorization & Reward Model Integrity | 4 | [C03-07-Fine-Tuning-Pipeline-Security](C03-07-Fine-Tuning-Pipeline-Security.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Model tampering during training or fine-tuning pipeline
- Unauthorized model deployment bypassing validation gates
- Model supply chain attacks (compromised checkpoints on Hugging Face, etc.) -- 6.5x increase in malicious models in 2024 (JFrog); 352K unsafe issues across 51.7K models (Protect AI, 2025)
- Model namespace reuse/hijacking: attackers reclaim deleted namespaces to distribute malicious models via trusted names (Unit 42, 2025)
- Picklescan evasion via nullifAI techniques, bypassing format-based defenses (ReversingLabs, 2025)
- Stale or vulnerable models remaining in production without rotation -- 91% of ML models degrade over time (MIT)
- Silent hosted model updates changing behavior without consumer awareness -- prompts degrade after provider updates
- Provider model deprecations with limited notice windows (60 days for Azure GA models; varies widely across providers)
- Incomplete decommissioning leaving model artifacts accessible to attackers
- Weaponized open-source AI repositories (NullBulge campaign, 2024: ransomware delivery via Hugging Face/GitHub)
- Post-training compression (quantization, pruning, distillation) degrading safety alignment and adversarial robustness -- research shows extreme quantization introduces unpredictable representational harm and pruning reduces model robustness to adversarial inputs
- NSA/CISA joint advisory (March 2026) reframes AI as a layered supply chain spanning data, models, software, infrastructure, hardware, and third-party services; recommends cryptographic signing, verified model registries, and provenance checks across the lifecycle
- AI infrastructure supply chain attacks escalating: TeamPCP campaign (March 2026) compromised Trivy, npm packages, Checkmarx KICS, LiteLLM, and Telnyx in a five-day chain; LiteLLM alone averages 97M monthly PyPI downloads and is used by Stripe, Netflix, Google
- Hosted model behavioral regressions from system prompt changes -- GPT-4o sycophancy incident (April 2025) required rollback after full deployment without staged canary release
- IBM X-Force 2026 Threat Index: 300K+ ChatGPT credentials on dark web marketplaces in 2025; supply chain compromises up nearly 4x since 2020; 44% increase in exploitation of public-facing applications

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2026-03 | TeamPCP supply chain campaign (LiteLLM, Trivy, Telnyx) | Five-day campaign: Trivy v0.69.4 compromised March 19, self-propagating npm worm (44+ packages), Checkmarx KICS, then LiteLLM PyPI versions 1.82.7/1.82.8 backdoored March 24 with credential-stealing payloads exfiltrating API keys, SSH keys, cloud configs, and K8s tokens. LiteLLM averages 97M monthly downloads; used by Stripe, Netflix, Google. Demonstrates cascading supply chain risk across AI infrastructure | [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/) |
| 2026-03 | NSA/CISA/Five Eyes Joint AI/ML Supply Chain Advisory | Reframes AI as a layered supply chain; recommends cryptographic signing, verified model registries, integrity checks (hashes, checksums, digital signatures), and provenance checks for all third-party datasets | [NSA Advisory](https://www.cyber.gov.au/business-government/secure-design/artificial-intelligence/artificial-intelligence-and-machine-learning-supply-chain-risks-and-mitigations) |
| 2026-03 | NIST AI RMF 1.1 released | Version 1.1 released March 18, 2026; expanded MEASURE function guidance covering performance metric selection, bias/fairness evaluation, and monitoring cadence; federal contractors must align in new contract cycles | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) |
| 2026-02 | IBM X-Force 2026 Threat Index | 300K+ ChatGPT credentials on dark web; supply chain compromises up nearly 4x since 2020; 44% increase in exploitation of public-facing applications; AI-powered coding tools introducing unvetted code into pipelines | [IBM X-Force](https://newsroom.ibm.com/2026-02-25-ibm-2026-x-force-threat-index-ai-driven-attacks-are-escalating-as-basic-security-gaps-leave-enterprises-exposed) |
| 2025-04 | GPT-4o sycophancy rollback | System prompt change caused sycophantic behavior including endorsing harmful statements; full deployment without canary release; social media became primary alerting; rolled back April 28 after 3 days; OpenAI admitted optimization for short-term feedback signals | [OpenAI Blog](https://openai.com/index/sycophancy-in-gpt-4o/) |
| 2025-04 | OpenSSF Model Signing v1.0 (Google, NVIDIA, HiddenLayer) | First stable release of Sigstore-based model signing library and CLI; supports any model format and size; NVIDIA signing all NGC Catalog models with OMS since March 2025 | [OpenSSF Blog](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) |
| 2025-02 | Model Namespace Reuse attack (Palo Alto Unit 42) | Attackers reclaim deleted Hugging Face namespaces to upload malicious models; demonstrated RCE on Google Vertex AI Model Garden and Microsoft Azure AI Foundry | [Unit 42](https://unit42.paloaltonetworks.com/model-namespace-reuse/) |
| 2025-01 | nullifAI evasion of Picklescan (ReversingLabs) | Malicious models on Hugging Face bypassed Picklescan detection using novel evasion techniques; removed within 24 hours | [ReversingLabs](https://www.reversinglabs.com/blog/ai-and-transparency-how-ml-model-creators-can-protect-against-supply-chain-attacks) |
| 2025 | Protect AI scan: 352K unsafe model issues | Scan of 4.47M model versions found 352,000 unsafe or suspicious issues across 51,700 models on Hugging Face | [Trend Micro](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/exploiting-trust-in-open-source-ai-the-hidden-supply-chain-risk-no-one-is-watching) |
| 2025 | Sonatype: 454,600 new malicious packages (cumulative 1.23M) | Growing supply chain malware across npm, PyPI, Maven, NuGet, and Hugging Face | [Sonatype 2026 Report](https://www.sonatype.com/state-of-the-software-supply-chain/2026/open-source-malware) |
| 2024 | NullBulge campaign: weaponized HF/GitHub repos | Threat actor distributed malicious code via Hugging Face and GitHub targeting AI tools; exfiltrated data via Discord webhooks, delivered LockBit ransomware | [Hacker News](https://thehackernews.com/2025/11/cisos-expert-guide-to-ai-supply-chain.html) |
| 2024-02 | Hugging Face malicious pickle-based models | Supply chain attack via unsigned model artifacts on public hub; JFrog documented 6.5x increase in malicious models in 2024 | [JFrog blog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/) |
| 2024-02 | Hugging Face conversion service vulnerability | Attacker could run arbitrary code via model conversion, hijacking widely used models without indication to users | [The Hacker News](https://thehackernews.com/2024/02/new-hugging-face-vulnerability-exposes.html) |
| 2023-04 | PyTorch nightly supply chain compromise | Malicious dependency injected into torchtriton package via PyPI | [PyTorch advisory](https://pytorch.org/blog/compromised-nightly-dependency/) |
| 2023 | ShadowRay (Anyscale Ray) CVE-2023-48022 | Unauthenticated access to ML training infrastructure and model artifacts | [Oligo Security](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **MLOps platforms:** MLflow, Weights & Biases, Kubeflow, SageMaker, Vertex AI Model Registry, Azure AI Foundry
- **Model signing:** [OpenSSF Model Signing (OMS) v1.0](https://openssf.org/projects/model-signing/) -- production-ready Sigstore-based library and CLI for signing any model format (April 2025); NVIDIA signs all NGC Catalog models with OMS since March 2025; also cosign, in-toto attestations, TUF (The Update Framework). [CoSAI](https://www.coalitionforsecureai.org/) (40+ members) released model signing and incident response frameworks in 2025-2026
- **SBOM/MBOM:** CycloneDX (v1.5+ ML BOM support with JSF/XMLsig enveloped signing), SPDX AI/ML profile, Syft (generates SBOMs from container images in both formats)
- **Deployment:** Seldon Core, BentoML, TorchServe, Triton Inference Server, vLLM with canary/blue-green strategies via Argo Rollouts or Flagger
- **Testing:** Giskard, Deepchecks, Great Expectations (for data validation), custom red-team harnesses
- **Data versioning:** DVC, LakeFS, Delta Lake
- **Audit logging:** Cloud-native (CloudTrail, Cloud Audit Logs, Azure Monitor), append-only log stores
- **Hosted model monitoring:** [deprecations.info](https://deprecations.info/) (tracks deprecations across OpenAI, Anthropic, Google, AWS Bedrock, Cohere, xAI via JSON/RSS), [llm-stats.com](https://llm-stats.com/llm-updates) (model release tracking)
- **Supply chain scanning:** Protect AI model scanning (352K issues found across 51.7K models in 2025), Hugging Face Picklescan (updated after nullifAI evasion), safetensors format
- **Compression safety testing:** SafetyBench, TruthfulQA for benchmarking quantized/pruned model safety; quantization-aware training to preserve robustness during compression
- **Hosted model logging:** [PromptLayer](https://docs.promptlayer.com/), [Langfuse](https://langfuse.com/), [LiteLLM](https://docs.litellm.ai/) (unified proxy with model identifier logging across providers), MLflow AI Gateway
- **RLHF safety:** [Safe-RLHF](https://github.com/PKU-Alignment/safe-rlhf) (PKU, constrained value alignment), SafeMoE (ICLR 2025, safety routing for MoE LLMs), KL penalty monitoring (standard PPO), Adversarial Reward Auditing (ARA, Feb 2026, latent-space detection), InfoRM (information-theoretic reward modeling with MOP metric)
- **Standards/Frameworks:** NIST AI RMF 1.1 (released March 18, 2026; expanded MEASURE function with performance metric selection, bias/fairness evaluation, and monitoring cadence guidance; federal contractors must align in new contract cycles), ISO/IEC 42001 (AI management systems), EU AI Act GPAI transparency enforcement (active March 2026; providers must maintain technical documentation for European AI Office), SLSA for ML (emerging), NSA/CISA AI/ML Supply Chain Advisory (March 2026), DevSecMLOps (OpenSSF MLSecOps whitepaper, 2025), OCC Bulletin 2026-8 (requires LLM model risk management treatment for financial services)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C3.1 Model Authorization & Integrity | Medium-High | Model registries are mature. OpenSSF Model Signing (OMS) v1.0 reached production readiness in April 2025; NVIDIA now signs all NGC models with OMS. CoSAI (40+ orgs) released model signing frameworks. NSA/CISA advisory (March 2026) recommends verified registries and cryptographic signing. CycloneDX ML BOM and SPDX AI profiles maturing. EU AI Act GPAI obligations (Aug 2025) drive inventory requirements. SLSA for ML proposed but not yet standardized. *(Updated 2026-03)* |
| C3.2 Model Validation & Testing | Medium | Safety testing tools exist but lack standardized pass/fail benchmarks; MCP testing is nascent. Only 5% of production AI agents have mature monitoring (Cleanlab 2025). New requirement 3.2.5 addresses post-compression safety re-evaluation--SafetyBench and TruthfulQA can benchmark quantized models but edge-specific safety benchmarks remain a gap. *(Updated 2026-03)* |
| C3.3 Controlled Deployment & Rollback | High | Canary/blue-green well-supported in Kubernetes ecosystem; atomic multi-artifact rollback less mature. Model Namespace Reuse attack (2025) demonstrated need for deployment-time integrity checks at cloud platform level. GPT-4o sycophancy incident (April 2025) highlighted that behavioral metrics must be part of canary evaluation -- functional metrics can pass while safety regresses. *(Updated 2026-03)* |
| C3.4 Secure Development Practices | High | Version control and environment isolation are solved problems; cultural adoption in ML teams varies. Data provenance remains a gap--digital signatures cannot adequately cover dynamic training data. The TeamPCP/LiteLLM attack (March 2026) demonstrated that even security tooling in training environments can become an attack vector -- egress controls and package integrity verification are essential. IBM X-Force 2026 reports supply chain compromises up nearly 4x since 2020, with AI-powered coding tools introducing unvetted code into pipelines. *(Updated 2026-03)* |
| C3.5 Hosted and Provider-Managed Model Controls | Low-Medium | Provider transparency improving: deprecation tracking services (deprecations.info) now cover 7+ providers via JSON/RSS. Azure AI Foundry offers 60-day GA retirement notices. OpenAI returns exact dated snapshot IDs in API responses. However, alias resolution changes remain opaque, silent updates are common, and 91% of models degrade over time (MIT). The GPT-4o sycophancy incident (April 2025) demonstrated that even system prompt changes -- not model weight updates -- can cause severe behavioral regressions with no advance consumer notification. EU AI Act GPAI transparency enforcement became active March 2026. NIST AI RMF 1.1 (March 2026) expanded MEASURE guidance on monitoring cadence. No standard protocol for provider-to-consumer change notifications. *(Updated 2026-03)* |
| C3.7 Fine-Tuning Pipeline Authorization & Reward Model Integrity | Low | Research now populated for all four requirements. Separation of duties is a NIST AI RMF governance best practice but rarely enforced in ML pipelines. Reward model integrity can leverage OMS v1.0 signing. Reward hacking detection is an active research area--ARA (Feb 2026), InfoRM, and BNRM offer promising detection approaches but none are production-hardened. Multi-stage checkpoint integrity verification requires custom pipeline logic; DevSecMLOps frameworks recommend per-stage security checks. *(Updated 2026-03)* |

---

## Open Research Questions

- [ ] What's the right cadence for model re-validation in production (drift vs. cost)? (MIT finding: 91% of models degrade; Gartner: 67% within 12 months)
- [ ] How do hosted model providers (OpenAI, Anthropic, Google) handle versioning transparency? (Partially answered: deprecations.info tracks 7 providers; Azure offers 60-day notices; OpenAI provides model IDs but aliases them; transparency remains inconsistent)
- [ ] What constitutes 'adequate' pre-deployment security testing for fine-tuned models? (Only 5% of production AI agents have mature monitoring per Cleanlab 2025)
- [ ] How should organizations manage rollback for models with stateful fine-tuning?
- [ ] Can SLSA (Supply-chain Levels for Software Artifacts) be adapted for ML model provenance? (ReversingLabs 2025 proposes extending SLSA provenance files with ML-specific metadata; not yet standardized)
- [ ] What standards should govern cascading emergency shutdown across agent infrastructure?
- [ ] How should organizations handle provider auto-upgrade behavior (e.g., Azure's upgrade-on-expiry for pinned model deployments)?
- [ ] What is the minimum viable model identity information that providers should expose for audit compliance under the EU AI Act?
- [ ] What safety thresholds should apply to post-compression artifacts? Research shows quantization and pruning degrade alignment and robustness unpredictably -- standardized benchmarks for compressed model safety are still lacking.
- [ ] How quickly will OpenSSF Model Signing (OMS) achieve broad adoption beyond NVIDIA NGC? CoSAI is driving standardization but hub-level adoption on Hugging Face, Kaggle, etc. is not yet universal.
- [ ] Which reward hacking detection approaches (ARA, InfoRM, BNRM, KL penalty) will prove most practical for production RLHF pipelines? Current research shows promising AUC scores but no production-hardened implementations exist as of early 2026.
- [ ] Should hosted model providers be required to expose immutable model identifiers (not just aliases) in API responses? Current practice varies widely and creates audit gaps for consumers in regulated industries.
- [ ] How should organizations defend against cascading supply chain campaigns like TeamPCP (March 2026) where a single compromised security tool (Trivy) led to backdoored AI infrastructure packages (LiteLLM, 97M monthly downloads) within five days?
- [ ] Should system prompt changes be subject to the same staged deployment discipline (canary, blue-green) as model weight updates? The GPT-4o sycophancy incident (April 2025) suggests yes, but no framework currently mandates this.
- [ ] How will the OCC Bulletin 2026-8 (LLM model risk management) affect financial services organizations' model lifecycle requirements, and will other sector regulators follow?

---

## Related Standards & Cross-References

- [MITRE ATLAS](https://atlas.mitre.org/)
- [MLOps Principles](https://ml-ops.org/content/mlops-principles)
- [Reinforcement fine-tuning (OpenAI)](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
- [What is AI adversarial robustness? (IBM Research)](https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness)
- [SLSA Framework](https://slsa.dev/)
- [NIST SP 800-88 Guidelines for Media Sanitization](https://csrc.nist.gov/publications/detail/sp/800-88/rev-1/final)
- [CycloneDX ML BOM](https://cyclonedx.org/capabilities/mlbom/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act GPAI Obligations (CSA Guide)](https://cloudsecurityalliance.org/blog/2025/01/29/how-can-iso-iec-42001-nist-ai-rmf-help-comply-with-the-eu-ai-act)
- [OWASP Machine Learning Security Top 10](https://owasp.org/www-project-machine-learning-security-top-10/)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OpenAI Model Deprecations](https://developers.openai.com/api/docs/deprecations)
- [Azure AI Foundry Model Lifecycle](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/model-lifecycle-retirement)
