# C06: Supply Chain Security for Models, Frameworks & Data

> **Source:** [`1.0/en/0x10-C06-Supply-Chain.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C06-Supply-Chain.md)
> **Requirements:** 33 | **Sections:** 7

## Control Objective

AI supply-chain attacks exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code. These controls provide end-to-end traceability, vulnerability management, and monitoring to protect the entire model lifecycle.

> **2025-2026 Highlights:** The AI BOM ecosystem (CycloneDX ML, SPDX AI) is gaining adoption alongside SLSA for ML pipelines. Malicious model discoveries on public registries continued to grow, reinforcing the need for model scanning and SafeTensors format enforcement as baseline controls. As of March 2026, AI agent skill marketplaces have emerged as a major new supply chain attack surface — the OpenClaw/ClawHavoc crisis (1,184 malicious skills, CVE-2026-25253) and AI-powered CI/CD attacks (Hackerbot-claw) demonstrate that supply chain threats are expanding beyond traditional package registries. IBM X-Force 2026 reports supply chain compromises have nearly quadrupled since 2020.

---

## Section Pages

| Section | Title | Reqs | IDs | Page |
|---------|-------|:----:|-----|------|
| C6.1 | Pretrained Model Vetting & Origin Integrity | 5 | 6.1.1–6.1.5 | [C06-01-Pretrained-Model-Vetting](C06-01-Pretrained-Model-Vetting.md) |
| C6.2 | Framework & Library Scanning | 5 | 6.2.1–6.2.5 | [C06-02-Framework-Library-Scanning](C06-02-Framework-Library-Scanning.md) |
| C6.3 | Dependency Pinning & Verification | 5 | 6.3.1–6.3.5 | [C06-03-Dependency-Pinning-Verification](C06-03-Dependency-Pinning-Verification.md) |
| C6.4 | Trusted Source Enforcement | 5 | 6.4.1–6.4.5 | [C06-04-Trusted-Source-Enforcement](C06-04-Trusted-Source-Enforcement.md) |
| C6.5 | Third-Party Dataset Risk Assessment | 5 | 6.5.1–6.5.5 | [C06-05-Third-Party-Dataset-Risk](C06-05-Third-Party-Dataset-Risk.md) |
| C6.6 | Supply Chain Attack Monitoring | 3 | 6.6.1–6.6.3 | [C06-06-Supply-Chain-Attack-Monitoring](C06-06-Supply-Chain-Attack-Monitoring.md) |
| C6.7 | AI BOM for Model Artifacts | 5 | 6.7.1–6.7.5 | [C06-07-AI-BOM-Model-Artifacts](C06-07-AI-BOM-Model-Artifacts.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Malicious models on public registries** — As of April 2025, Protect AI's Guardian scanner found 352,000 unsafe/suspicious issues across 51,700 models out of 4.47 million scanned on Hugging Face. JFrog found 59% of serialized model files still use unsafe pickle-based formats. Attackers embed reverse shells and RATs via pickle's `__reduce__` method.
- **Pickle deserialization RCE** — CVE-2025-32434 (CVSS 9.3) proved that PyTorch's `weights_only=True` could be bypassed for arbitrary code execution. Three PickleScan zero-day bypasses (CVE-2025-10155/56/57, all CVSS 9.3) allowed malicious models to evade Hugging Face's primary scanner until September 2025.
- **CI/CD pipeline compromise** — The Ultralytics YOLO attack (December 2024) injected a cryptominer into PyPI packages via unsafe GitHub Actions variables, affecting a library with 60M+ downloads. GhostAction (September 2025) exfiltrated 3,325 secrets from 817 repos.
- **Malicious LoRA/adapter weights** — LoRATK research showed single backdoored LoRA adapters can poison base models. CoLoRA (March 2026) distributes backdoor payloads across multiple adapters that only activate when merged — much harder to detect individually.
- **Dataset poisoning at scale** — Researchers demonstrated poisoning LAION-400M for just $60 by re-registering expired domains. Just 250 poisoned documents can compromise LLMs regardless of total dataset size (October 2025 research).
- **Typosquatting and dependency confusion** — 500+ malicious PyPI packages found in a single March 2024 campaign; Sonatype reports 2x year-over-year increase in repository attacks.
- **AI agent skill marketplace poisoning** — The OpenClaw/ClawHavoc crisis (February–March 2026) saw 1,184 confirmed malicious skills on ClawHub (~20% of the registry). CVE-2026-25253 enabled RCE; attackers distributed Atomic macOS Stealer (AMOS) via prompt injection in skill descriptors, hidden reverse shells, and token exfiltration. Largest confirmed supply chain attack targeting AI agent infrastructure to date.
- **AI-powered CI/CD exploitation** — Hackerbot-claw (tracked as "Chaos Agent" by Pillar Security, February 2026) used an LLM as an execution layer to scan for misconfigured GitHub Actions, open poisoned PRs, and exfiltrate secrets from Microsoft, Datadog, and Aqua Security repos. CVE-2026-28353 compromised the Trivy VS Code extension.
- **Model distillation via API abuse** — Anthropic disclosed (February 2026) that DeepSeek, Moonshot AI, and MiniMax used ~24,000 fake accounts to generate 16 million conversations for training data extraction.
- **SafeTensors conversion bot hijack** — HiddenLayer demonstrated hijacking Hugging Face's SFConvertbot (42,657+ PRs made) to submit malicious model conversions to any repository.
- **Supply chain compromise acceleration** — IBM X-Force 2026 Threat Index (February 2026) reports supply chain and third-party compromises have nearly quadrupled since 2020, driven by exploitation of CI/CD automation and trust relationships. Vulnerability exploitation is now the leading initial access vector at 40% of observed incidents.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Dec 2024 | Ultralytics YOLO supply chain attack — cryptominer injected via GitHub Actions | CI/CD pipeline compromise affecting library with 60M+ PyPI downloads, 33K GitHub stars | [Wiz Blog](https://www.wiz.io/blog/ultralytics-ai-library-hacked-via-github-for-cryptomining) |
| Apr 2025 | CVE-2025-32434 — PyTorch `weights_only=True` RCE bypass (CVSS 9.3) | The "safe" deserialization parameter was bypassable; fixed in PyTorch 2.6.0 | [GitHub Advisory](https://github.com/pytorch/pytorch/security/advisories/GHSA-53q9-r3pm-6pq6) |
| Jun 2025 | CVE-2025-10155/56/57 — PickleScan zero-day bypasses (CVSS 9.3 each) | Three methods bypass Hugging Face's primary model scanner; fixed in v0.0.31 | [JFrog Blog](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/) |
| Feb 2025 | nullifAI — PickleScan bypass via 7z compression on Hugging Face | Broken pickle serialization still executes reverse shell payloads | [Hacker News](https://thehackernews.com/2025/02/malicious-ml-models-found-on-hugging.html) |
| Feb 2024 | SafeTensors conversion bot hijack (HiddenLayer) | Bot with 42,657+ PRs could be impersonated to poison models from Microsoft, Google | [HiddenLayer](https://hiddenlayer.com/innovation-hub/silent-sabotage/) |
| Mar 2026 | CoLoRA — colluding LoRA composite backdoor attack | Backdoor distributed across multiple adapters; activates only when merged | [arXiv 2603.12681](https://arxiv.org/html/2603.12681) |
| Feb 2026 | Anthropic: 24K fake accounts used for Claude distillation | DeepSeek, Moonshot, MiniMax generated 16M conversations for training data extraction | [CNBC](https://www.cnbc.com/2026/02/24/anthropic-openai-china-firms-distillation-deepseek.html) |
| 2024 | LAION-400M poisoning for $60 (Carlini et al.) | Web-scale dataset poisoning via expired domain re-registration; 0.00025% poison rate achieves 60% success | [arXiv 2302.10149](https://arxiv.org/abs/2302.10149) |
| Sep 2025 | GhostAction — GitHub Actions supply chain attack | 3,325 secrets exfiltrated from 817 repos including PyPI/npm/DockerHub tokens | [GitGuardian](https://blog.gitguardian.com/protecting-your-software-supply-chain-understanding-typosquatting-and-dependency-confusion-attacks/) |
| Feb–Mar 2026 | OpenClaw/ClawHavoc — 1,184 malicious skills on ClawHub marketplace | CVE-2026-25253 RCE; ~20% of registry malicious; Atomic macOS Stealer distributed via prompt injection in skill descriptors | [Trend Micro](https://www.trendmicro.com/en_us/research/26/b/openclaw-skills-used-to-distribute-atomic-macos-stealer.html) |
| Feb 2026 | Hackerbot-claw ("Chaos Agent") — AI bot exploiting CI/CD pipelines | LLM-powered bot opened poisoned PRs against Microsoft, Datadog, Aqua Security repos; CVE-2026-28353 compromised Trivy VS Code extension | [Hacker News](https://thehackernews.com/2026/03/five-malicious-rust-crates-and-ai-bot.html) |
| Feb 2026 | IBM X-Force 2026 Threat Index — supply chain compromises nearly 4x since 2020 | 44% surge in exploitation of public-facing apps; vulnerability exploitation is now leading initial access vector (40% of incidents) | [IBM Newsroom](https://newsroom.ibm.com/2026-02-25-ibm-2026-x-force-threat-index-ai-driven-attacks-are-escalating-as-basic-security-gaps-leave-enterprises-exposed) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Model scanning:** [Guardian](https://protectai.com/guardian) (Protect AI — enterprise-grade, 4.47M model versions scanned, architectural backdoor detection), [ModelScan](https://github.com/protectai/modelscan) (open-source, supports H5/Pickle/SavedModel), [Fickling](https://github.com/trailofbits/fickling) (Trail of Bits — Sep 2025 ML scanner uses allowlist approach, 100% malicious pickle detection, 99% accuracy), [PickleScan](https://github.com/mmaitre314/picklescan) (blocklist-based, used by Hugging Face — keep updated after CVE-2025-10155/56/57)
- **Safe serialization:** [SafeTensors](https://huggingface.co/docs/safetensors/index) (Rust-based, no code execution by design, passed external security audit; as of June 2025, native PyTorch DCP support via torchtune; adoption growing but 59% of HF models still use unsafe formats)
- **Model signing:** [OpenSSF Model Signing v1.0](https://github.com/sigstore/model-transparency) (released April 2025, v1.1.1 Oct 2025 — signs/verifies any model format via Sigstore; NVIDIA signs all NGC models with OMS since March 2025), [Sigstore/cosign](https://www.sigstore.dev/) (keyless signing for containers and OCI artifacts)
- **AI BOM / ML BOM:** [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/) (v1.5+ stable through v1.7/ECMA-424), [SPDX AI Profile](https://spdx.dev/) (v3.0.1 with AI and Dataset profiles), [OWASP AIBOM Generator](https://owasp.org/www-project-aibom/) (scans repos for HF model usage, generates CycloneDX AI BOMs), Dependency-Track
- **AI-aware SCA platforms:** [Sonatype Lifecycle](https://help.sonatype.com/en/threats-in-ai-ml-models.html) (scans Hugging Face models for malware, pickle execution risks, license issues, and derivative model provenance — supports `.bin`, `.pt`, `.pkl`, `.pickle` formats), [Manifest](https://www.manifestcyber.com/) (continuous AI model scanning with daily HF assessments; added C/C++ SBOM generator March 2026)
- **Dependency scanning:** Dependabot, Snyk, [OSV Scanner](https://google.github.io/osv-scanner/) (Google), Grype, Trivy, [Socket.dev](https://socket.dev/) (10K+ orgs, proactive supply chain protection) — *note: most traditional SCA tools still don't scan model files as dependencies, though Sonatype Lifecycle is closing this gap for HF-hosted models*
- **Dataset validation:** [Cleanlab](https://github.com/cleanlab/cleanlab) (label errors, outliers, duplicates — found thousands of errors in ImageNet), [Great Expectations](https://greatexpectations.io/) (data validation framework), Presidio (PII detection)
- **Registry security:** Hugging Face multi-layer scanning (ClamAV + PickleScan + TruffleHog + Guardian since Oct 2024), model cards, SafeTensors conversion bot
- **Provenance & build security:** [SLSA framework](https://slsa.dev/) (L3 achievable via GitHub Actions + Sigstore), [in-toto](https://in-toto.io/), Rekor transparency log

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C6.1 Pretrained Model Vetting | Maturing | Guardian scanned 4.47M model versions; Fickling's allowlist approach achieves 100% pickle detection. OpenSSF Model Signing v1.0 (April 2025) fills the signing gap. Trojan/behavioral backdoor detection remains limited. |
| C6.2 Framework & Library Scanning | Mature | Standard SCA tools (Trivy, Snyk, Dependabot) handle ML Python deps well. Sonatype Lifecycle now scans HF model artifacts for malware and pickle risks. Gap: CUDA native libraries and custom operators still not first-class scan targets. |
| C6.3 Dependency Pinning & Verification | Mature | pip/conda/Docker lockfile tooling is production-ready. SLSA L3 achievable via GitHub Actions + Sigstore. Reproducible builds (C6.3.5) still challenging for large training runs. |
| C6.4 Trusted Source Enforcement | Maturing | Container signing mature (cosign); model signing now viable via OMS v1.0 (NVIDIA signs all NGC models). Egress controls and quarantine tooling are established. |
| C6.5 Third-Party Dataset Risk | Emerging | Cleanlab handles data quality/outliers but not adversarial poisoning. LAION-400M poisoning for $60 demonstrates the practical risk. PII scrubbing via Presidio is mature; bias metrics tooling exists (Fairlearn). |
| C6.6 Supply Chain Attack Monitoring | Emerging | AI-specific threat intelligence is improving but still limited. IBM X-Force 2026 now tracks AI supply chain trends (4x increase since 2020). No ML-focused SIEM detection rules widely available. Socket.dev provides proactive package analysis; Manifest offers daily model risk assessments. The OpenClaw/ClawHavoc crisis demonstrated how fast AI agent marketplaces can become attack vectors. |
| C6.7 AI BOM for Model Artifacts | Maturing | CycloneDX ML-BOM stable through v1.7 (ECMA-424). OWASP AIBOM Generator produces CycloneDX output from HF model references. SPDX 3.0.1 adds AI profiles. Adoption still early but tooling is real. |

---

## Related Standards & Cross-References

- [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/) — moved up 2 positions from 2023 list; now covers model/adapter tampering, AI dev tool exploitation, input-triggered backdoors
- [MITRE ATLAS AML.T0010: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010) — 5 sub-techniques: Hardware (.000), ML Software (.001), Data (.002), Model (.003), Container Registry (.004). As of Oct 2025, ATLAS catalogs 15 tactics, 66 techniques, 46 sub-techniques.
- [NIST IR 8596 — Cyber AI Profile](https://csrc.nist.gov/pubs/ir/8596/iprd) (preliminary draft, Dec 2025) — Maps CSF 2.0 to AI-specific risks including supply chain integrity for model development pipelines
- [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) (Jul 2025) — 243 controls across 18 domains; dedicated Supply Chain Management domain addressing insecure supply chains
- [EU AI Act Annex IV](https://artificialintelligenceact.eu/annex/4/) — Section 2 requires documenting third-party tools/models, training data provenance, and governance. Article 25 assigns provider responsibilities along the value chain. Fully applicable August 2026.
- [CISA 2025 SBOM Minimum Elements](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom) (August 2025) — Updated guidance with component hash, license, tool name fields; prepares for AI system use cases
- [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/) — Stable through v1.7/ECMA-424 (October 2025)
- [OpenSSF Model Signing v1.0](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/) — Library and CLI for signing/verifying ML models via Sigstore
- [SLSA Framework](https://slsa.dev/) — L3 achievable for ML packaging pipelines via GitHub Actions + Sigstore
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) — AI management systems; requires supplier risk assessment, security protocol enforcement across AI supply chain
- [NIST AI RMF](https://airc.nist.gov/AI_RMF_Interactivity) — MAP/MEASURE/MANAGE functions address supply chain dependencies
- [IBM X-Force 2026 Threat Intelligence Index](https://newsroom.ibm.com/2026-02-25-ibm-2026-x-force-threat-index-ai-driven-attacks-are-escalating-as-basic-security-gaps-leave-enterprises-exposed) — Quantifies supply chain/third-party compromises at nearly 4x since 2020; vulnerability exploitation now leading initial access vector (40%)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C01 Training Data](C01-Training-Data.md) | Dataset provenance and poisoning | C6.5 covers supply-chain risk of *external* datasets; C01 covers data quality broadly. ATLAS AML.T0010.002 (Data) links both. EU AI Act Annex IV Section 2 requires documenting data provenance. |
| [C03 Model Lifecycle](C03-Model-Lifecycle-Management.md) | Model versioning, signing, deployment | C6.7 AI BOM complements C03 model registry requirements. OpenSSF Model Signing creates checkpoints at upload, deployment, and downstream reuse. ATLAS AML.T0010.003 covers compromised pretrained models. |
| [C04 Infrastructure](C04-Infrastructure.md) | Build pipeline and container security | C6.2/C6.3 pinning and scanning overlap with C04 infrastructure hardening. ATLAS AML.T0010.004 targets container registries. SLSA L2/L3 build requirements apply to C04.2 pipelines. |
| [C07 Model Behavior](C07-Model-Behavior.md) | Behavioral impact of supply chain attacks | Compromised models (AML.T0010.003) and backdoored LoRA adapters produce malicious model behavior. OWASP LLM03 covers input-triggered backdoors. |
| [C11 Adversarial Robustness](C11-Adversarial-Robustness.md) | Backdoors from poisoned data/models | AML.T0010.002 + .003 enable backdoor insertion. CoLoRA shows colluding adapters can bypass individual detection. EU AI Act Art 15 robustness requirements apply to supply-chain-introduced backdoors. |
| [C09 Orchestration & Agents](C09-Orchestration-and-Agents.md) | Agent skill/plugin marketplace supply chain | OpenClaw/ClawHavoc (1,184 malicious skills) demonstrates that AI agent ecosystems create new supply chain attack surfaces beyond traditional package registries. C6.4 trusted-source controls apply to skill marketplaces. |
| [C13 Monitoring & Logging](C13-Monitoring-and-Logging.md) | Anomaly detection and incident response | C6.6 monitoring requirements feed into C13 centralized logging. CI/CD audit logs (C6.6.2) need C13 infrastructure for detection. |

---

## Open Research Questions

- [ ] **How do you detect colluding LoRA backdoors?** — CoLoRA (March 2026) distributes payloads across multiple adapters that individually appear safe. Weight-space singular value analysis shows promise but isn't production-ready.
- [ ] **Can dataset poisoning detection scale to web-crawled datasets?** — With 250 poison samples sufficient regardless of dataset size, and LAION-scale poisoning possible for $60, current outlier detection tools may not be sufficient.
- [ ] **Will model signing achieve critical adoption?** — OMS v1.0 exists and NVIDIA signed all NGC models, but Hugging Face hasn't adopted it natively. Until signing is the default, not the exception, supply chain integrity remains opt-in.
- [ ] **How should AI-specific threat intelligence feeds work?** — C6.6.3 requires ML-focused IoCs but no production threat intelligence service covers model poisoning indicators, malicious adapter fingerprints, or dataset corruption signatures.
- [ ] **What happens when SCA tools can scan model files?** — Sonatype Lifecycle now scans HF models for pickle risks and malware, but most SCA tools (Trivy, Snyk, Dependabot) still don't treat model files as scannable dependencies. The OWASP AIBOM Generator bridges part of this gap but a full solution is needed.
- [ ] **How should AI agent skill marketplaces be secured?** — The OpenClaw/ClawHavoc crisis showed that agent skill registries face the same supply chain risks as package managers, but with unique attack vectors (prompt injection in descriptors, LLM-mediated execution). No established vetting framework exists for AI agent skills yet.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
