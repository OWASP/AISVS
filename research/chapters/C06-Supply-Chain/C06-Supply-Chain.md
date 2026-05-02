# C06: Supply Chain Security for Models, Frameworks & Data

> **Source:** [`1.0/en/0x10-C06-Supply-Chain.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C06-Supply-Chain.md)
> **Requirements:** 17 | **Sections:** 5

## Control Objective

AI supply-chain attacks exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code. These controls ensure traceability, vetting, and monitoring of AI-specific supply chain artifacts throughout the model lifecycle.

Generic software supply chain controls (dependency scanning, version pinning, lockfile enforcement, container digest pinning, build attestation, reproducible builds, SBOM generation, CI/CD audit logging, etc.) are covered by ASVS v5 (V13, V15), OWASP SCVS, SLSA, and CIS Controls, and are not repeated here. This chapter focuses on supply chain risks unique to AI: model artifact integrity, backdoor detection in pretrained weights, dataset poisoning, AI-specific bills of materials, and model-publisher trust.

> **2025-2026 Highlights:** The AI BOM ecosystem (CycloneDX ML, SPDX AI) is gaining adoption alongside SLSA for ML pipelines. Malicious model discoveries on public registries continued to grow, reinforcing the need for model scanning and SafeTensors format enforcement as baseline controls. As of May 2026, agent tool and skill marketplaces have become a real supply-chain surface: GitHub's reviewed OpenClaw/ClawdBot advisory for CVE-2026-25253 and MITRE ATLAS v5.4/v5.5 additions around poisoned agent tools show how registry trust now extends beyond packages and model hubs. The LiteLLM compromise on March 24, 2026 and the Axios npm compromise disclosed on March 31, 2026 both show the same pattern: hijacked publisher accounts or CI/CD trust paths can push credential-stealing payloads into developer and AI infrastructure very quickly. IBM X-Force 2026 reports that large supply-chain and third-party compromises have nearly quadrupled since 2020. The current source emphasizes two controls worth treating as anchors: 6.1.4 behavioral acceptance testing before promotion and 6.2.2 per-registry publisher-key pinning with explicit re-approval on rotation.

---

## Section Pages

| Section | Title | Reqs | IDs | Page |
|---------|-------|:----:|-----|------|
| C6.1 | Pretrained Model Vetting & Origin Integrity | 5 | 6.1.1–6.1.5 | [C06-01-Pretrained-Model-Vetting](C06-01-Pretrained-Model-Vetting.md) |
| C6.2 | Trusted Source Enforcement for AI Artifacts | 2 | 6.2.1–6.2.2 | [C06-02-Trusted-Source-Enforcement](C06-02-Trusted-Source-Enforcement.md) |
| C6.3 | Third-Party Dataset Risk Assessment | 4 | 6.3.1–6.3.4 | [C06-03-Third-Party-Dataset-Risk](C06-03-Third-Party-Dataset-Risk.md) |
| C6.4 | Supply Chain Attack Monitoring | 2 | 6.4.1–6.4.2 | [C06-04-Supply-Chain-Attack-Monitoring](C06-04-Supply-Chain-Attack-Monitoring.md) |
| C6.5 | AI BOM for Model Artifacts | 4 | 6.5.1–6.5.4 | [C06-05-AI-BOM-Model-Artifacts](C06-05-AI-BOM-Model-Artifacts.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Malicious models on public registries** — As of April 2025, Protect AI's Guardian scanner found 352,000 unsafe/suspicious issues across 51,700 models out of 4.47 million scanned on Hugging Face. JFrog found 59% of serialized model files still use unsafe pickle-based formats. Attackers embed reverse shells and RATs via pickle's `__reduce__` method.
- **Pickle deserialization RCE** — CVE-2025-32434 proved that PyTorch's `weights_only=True` could be bypassed for arbitrary code execution in versions up to 2.5.1. Three PickleScan bypasses (CVE-2025-10155/56/57, all CVSS 9.3) allowed malicious model archives or disguised pickle files to evade scanning until fixed in v0.0.31.
- **CI/CD pipeline compromise** — The Ultralytics YOLO attack (December 2024) injected a cryptominer into PyPI packages via unsafe GitHub Actions variables, affecting a library with 60M+ downloads. GhostAction (September 2025) exfiltrated 3,325 secrets from 817 repos.
- **Malicious LoRA/adapter weights** — LoRATK research showed single backdoored LoRA adapters can poison base models. CoLoRA (March 2026) distributes backdoor payloads across multiple adapters that only activate when merged — much harder to detect individually.
- **Dataset poisoning at scale** — Researchers demonstrated poisoning LAION-400M for just $60 by re-registering expired domains. Just 250 poisoned documents can compromise LLMs regardless of total dataset size (October 2025 research).
- **Typosquatting and dependency confusion** — 500+ malicious PyPI packages found in a single March 2024 campaign; Sonatype reports 2x year-over-year increase in repository attacks.
- **AI agent skill marketplace poisoning** — GitHub's reviewed advisory for CVE-2026-25253 shows how OpenClaw/ClawdBot versions through 2026.1.28 trusted a `gatewayUrl` query parameter and auto-connected with the stored gateway token, allowing a malicious link to lead to privileged action execution. A related OpenClaw issue reported hundreds of malicious skills with droppers, fake installers, and MCP backdoor endpoints, making agent tool registries a practical extension of the supply-chain problem.
- **AI development tool compromise** — CVE-2026-28353 affected the Trivy VS Code extension distributed through OpenVSX. The compromised extension contained malicious code designed to use local coding-agent access to collect and exfiltrate secrets, which makes developer extensions and AI-adjacent scanners part of the trusted-source boundary.
- **LiteLLM/TeamPCP cascading supply chain attack** — On March 24, 2026, attackers published backdoored LiteLLM versions 1.82.7 and 1.82.8 to PyPI. The project issue reports that 1.82.8 added a `.pth` startup payload so credential harvesting could trigger on Python startup, collecting SSH keys, environment variables, cloud credentials, Kubernetes configs, crypto wallets, database passwords, SSL private keys, shell history, and CI/CD configs for exfiltration.
- **Axios npm maintainer-account hijack (Sapphire Sleet)** — On March 31, 2026, Microsoft reported malicious Axios versions 1.14.1 and 0.30.4 that added `plain-crypto-js@4.2.1`, a fake dependency whose `postinstall` hook downloaded a cross-platform RAT from Sapphire Sleet infrastructure. Elastic's analysis found the releases were direct CLI publishes without the normal trusted-publisher provenance, which is a strong example of why 6.2.2 requires publisher-key pinning and explicit rotation re-approval.
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
| Jan 2026 | OpenClaw/ClawdBot CVE-2026-25253 — gateway token exfiltration and 1-click RCE | Affected versions through 2026.1.28; malicious links could redirect the control UI to an attacker gateway and enable privileged actions | [GitHub Advisory](https://github.com/advisories/GHSA-g8p2-7wf7-98mq) |
| Mar 2026 | Trivy VS Code extension compromise — CVE-2026-28353 | Compromised OpenVSX artifact used local coding-agent access to collect and exfiltrate secrets | [GitHub Advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg) |
| Feb 2026 | IBM X-Force 2026 Threat Index — supply chain compromises nearly 4x since 2020 | 44% surge in exploitation of public-facing apps; vulnerability exploitation is now leading initial access vector (40% of incidents) | [IBM Newsroom](https://newsroom.ibm.com/2026-02-25-ibm-2026-x-force-threat-index-ai-driven-attacks-are-escalating-as-basic-security-gaps-leave-enterprises-exposed) |
| Mar 2026 | LiteLLM package compromise — backdoored PyPI releases 1.82.7 and 1.82.8 | Maintainer account compromise; 1.82.8 used a `.pth` startup payload to harvest SSH keys, cloud credentials, Kubernetes configs, wallets, and CI/CD secrets | [LiteLLM issue](https://github.com/BerriAI/litellm/issues/24518) |
| Mar 2026 | Axios npm maintainer hijack (Sapphire Sleet) — cross-platform RAT via `plain-crypto-js` | Malicious axios 1.14.1/0.30.4 added a postinstall dependency and bypassed normal trusted-publisher provenance | [Elastic Security Labs](https://www.elastic.co/security-labs/axios-one-rat-to-rule-them-all) |
| Apr 2026 | Microsoft: Axios compromise attribution + mitigations | Attributes the C2 infrastructure to Sapphire Sleet; recommends signature/provenance checks, lockfile review, and CI egress controls for install hooks | [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Model scanning:** [Guardian](https://protectai.com/guardian) (Protect AI — enterprise-grade, 4.47M model versions scanned, architectural backdoor detection), [ModelScan](https://github.com/protectai/modelscan) (open-source, supports H5/Pickle/SavedModel), [Fickling](https://github.com/trailofbits/fickling) (Trail of Bits — Sep 2025 ML scanner uses allowlist approach, 100% malicious pickle detection, 99% accuracy), [PickleScan](https://github.com/mmaitre314/picklescan) (blocklist-based, used by Hugging Face — keep updated after CVE-2025-10155/56/57)
- **Safe serialization:** [SafeTensors](https://huggingface.co/docs/safetensors/index) (Rust-based, no code execution by design, passed external security audit; as of June 2025, native PyTorch DCP support via torchtune; adoption growing but 59% of HF models still use unsafe formats)
- **Model signing:** [OpenSSF Model Signing v1.0](https://github.com/sigstore/model-transparency) (released April 2025, v1.1.1 Oct 2025 — signs/verifies any model format via Sigstore; NVIDIA signs all NGC models with OMS since March 2025; [Cohere](https://cohere.com/blog/securing-ai-supply-chains-coheres-commitment-to-model-signing) signs all Command-family models on Hugging Face with Sigstore as of 2026), [Sigstore/cosign](https://www.sigstore.dev/) (keyless signing for containers and OCI artifacts)
- **AI BOM / ML BOM:** [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/) (v1.5+ stable through v1.7/ECMA-424), [SPDX AI Profile](https://spdx.dev/) (v3.0.1 with AI and Dataset profiles), [OWASP AIBOM Generator](https://owasp.org/www-project-aibom/) (scans repos for HF model usage, generates CycloneDX AI BOMs), Dependency-Track
- **AI-aware SCA platforms:** [Sonatype Lifecycle](https://help.sonatype.com/en/threats-in-ai-ml-models.html) (scans Hugging Face models for malware, pickle execution risks, license issues, and derivative model provenance — supports `.bin`, `.pt`, `.pkl`, `.pickle` formats), [Manifest](https://www.manifestcyber.com/) (continuous AI model scanning with daily HF assessments; added C/C++ SBOM generator March 2026)
- **Dependency scanning:** Dependabot, Snyk, [OSV Scanner](https://google.github.io/osv-scanner/) (Google), Grype, Trivy, [Socket.dev](https://socket.dev/) (10K+ orgs, proactive supply chain protection) — *note: most traditional SCA tools still don't scan model files as dependencies, though Sonatype Lifecycle is closing this gap for HF-hosted models*
- **Behavioral acceptance testing (6.1.4):** [UK AISI Inspect](https://inspect.aisi.org.uk/evals/) (open-source Python framework — dataset→Task→Solver→Scorer pipeline, sandboxed execution, 30+ frontier models tested; covers safety, alignment, autonomous capability boundaries), [Stanford HELM Safety v1.0](https://crfm.stanford.edu/helm/safety/latest/) (five safety benchmarks: HarmBench, BBQ, SimpleSafetyTest, XSTest, AnthropicRedTeam across six risk categories), [DeepEval](https://deepeval.com/) (open-source LLM evaluation framework, pluggable benchmarks for safety and capability testing), [Bloom](https://supergok.com/bloom-ai-evaluation-tool/) (automated behavioral misalignment testing — generates configurable eval suites without ground-truth labels)
- **Dataset validation:** [Cleanlab](https://github.com/cleanlab/cleanlab) (label errors, outliers, duplicates — found thousands of errors in ImageNet), [Great Expectations](https://greatexpectations.io/) (data validation framework), Presidio (PII detection)
- **Registry security:** Hugging Face multi-layer scanning (ClamAV + PickleScan + TruffleHog + Guardian since Oct 2024), model cards, SafeTensors conversion bot
- **Provenance & build security:** [SLSA framework](https://slsa.dev/) (L3 achievable via GitHub Actions + Sigstore), [in-toto](https://in-toto.io/), Rekor transparency log

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C6.1 Pretrained Model Vetting | Maturing | Guardian scanned 4.47M model versions; Fickling's allowlist approach achieves 100% pickle detection. OpenSSF Model Signing v1.0 (April 2025) fills the signing gap. Behavioral acceptance testing now has tooling: UK AISI Inspect, HELM Safety v1.0, and DeepEval provide standardized safety/alignment benchmarks. Trojan/behavioral backdoor detection remains limited but improving. |
| C6.2 Trusted Source Enforcement for AI Artifacts | Maturing | Container signing mature (cosign); model signing now viable via OMS v1.0 (NVIDIA signs all NGC models, Cohere signs all Command-family models on HF as of 2026). Egress controls and quarantine tooling are established. 6.2.2 (per-registry publisher-key pinning with explicit rotation re-approval) is a direct response to Lazarus/BlueNoroff's axios maintainer-account takeover (March 2026). `npm audit signatures`, cosign key policies, and Sigstore trust roots each cover part of the problem, but unified per-registry pinning tooling is still emerging. |
| C6.3 Third-Party Dataset Risk | Emerging | Cleanlab handles data quality/outliers but not adversarial poisoning. LAION-400M poisoning for $60 demonstrates the practical risk. PII scrubbing via Presidio is mature; bias metrics tooling exists (Fairlearn). |
| C6.4 Supply Chain Attack Monitoring | Emerging | AI-specific threat intelligence is improving but still limited. IBM X-Force 2026 now tracks AI supply chain trends (4x increase since 2020). No ML-focused SIEM detection rules widely available. Socket.dev provides proactive package analysis; Manifest offers daily model risk assessments. The LiteLLM/TeamPCP attack (March 2026) and axios/BlueNoroff hijack (March 30, 2026) reinforce the need for ML-aware incident response playbooks (6.4.1) and AI-specific threat intelligence enrichment (6.4.2). |
| C6.5 AI BOM for Model Artifacts | Maturing | CycloneDX ML-BOM stable through v1.7 (ECMA-424). OWASP AIBOM Generator produces CycloneDX output from HF model references. SPDX 3.0.1 adds AI profiles. Adoption still early but tooling is real. |

---

## Related Standards & Cross-References

- [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/) — moved up 2 positions from 2023 list; now covers model/adapter tampering, AI dev tool exploitation, input-triggered backdoors
- [MITRE ATLAS AML.T0010: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010) — 5 sub-techniques: Hardware (.000), ML Software (.001), Data (.002), Model (.003), Container Registry (.004). ATLAS v5.4.0 (Feb 2026) added "Publish Poisoned AI Agent Tool" and OpenClaw case studies; v5.5.0 (Mar 2026) added agent-tool poisoning, AI supply-chain rug-pull, reputation-inflation, and machine-compromise techniques. See [atlas-data releases](https://github.com/mitre-atlas/atlas-data/releases) for the canonical change log.
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
| [C01 Training Data](../C01-Training-Data/C01-Training-Data.md) | Dataset provenance and poisoning | C6.3 covers supply-chain risk of *external* datasets; C01 covers data quality broadly. ATLAS AML.T0010.002 (Data) links both. EU AI Act Annex IV Section 2 requires documenting data provenance. |
| [C03 Model Lifecycle](../C03-Model-Lifecycle-Management/C03-Model-Lifecycle-Management.md) | Model versioning, signing, deployment | C6.5 AI BOM complements C03 model registry requirements. OpenSSF Model Signing creates checkpoints at upload, deployment, and downstream reuse. ATLAS AML.T0010.003 covers compromised pretrained models. |
| [C04 Infrastructure](../C04-Infrastructure/C04-Infrastructure.md) | Workload-level model loading hardening | C4.1.3 format allowlisting and C4.1.4 attestation complement C6.1 vetting and C6.5 AI BOM verification at load time. ATLAS AML.T0010.004 targets container registries. |
| [C07 Model Behavior](../C07-Model-Behavior/C07-Model-Behavior.md) | Behavioral impact of supply chain attacks | Compromised models (AML.T0010.003) and backdoored LoRA adapters produce malicious model behavior. OWASP LLM03 covers input-triggered backdoors. |
| [C11 Adversarial Robustness](../C11-Adversarial-Robustness/C11-Adversarial-Robustness.md) | Backdoors from poisoned data/models | AML.T0010.002 + .003 enable backdoor insertion. CoLoRA shows colluding adapters can bypass individual detection. EU AI Act Art 15 robustness requirements apply to supply-chain-introduced backdoors. |
| [C09 Orchestration & Agents](../C09-Orchestration-and-Agents/C09-Orchestration-and-Agents.md) | Agent skill/plugin marketplace supply chain | OpenClaw/ClawdBot advisories and MITRE ATLAS v5.4/v5.5 additions show that agent tools now need the same trusted-source controls as package registries. C6.2 trusted-source controls — including 6.2.2 publisher-key pinning — apply to skill and tool marketplaces. |
| [C13 Monitoring & Logging](../C13-Monitoring-and-Logging/C13-Monitoring-and-Logging.md) | Anomaly detection and incident response | C6.4 monitoring requirements feed into C13 centralized logging. |

---

## Open Research Questions

- [ ] **How do you detect colluding LoRA backdoors?** — CoLoRA (March 2026) distributes payloads across multiple adapters that individually appear safe. Weight-space singular value analysis shows promise but isn't production-ready.
- [ ] **Can dataset poisoning detection scale to web-crawled datasets?** — With 250 poison samples sufficient regardless of dataset size, and LAION-scale poisoning possible for $60, current outlier detection tools may not be sufficient.
- [ ] **Will model signing achieve critical adoption?** — OMS v1.0 exists and NVIDIA signed all NGC models, but Hugging Face hasn't adopted it natively. Until signing is the default, not the exception, supply chain integrity remains opt-in.
- [ ] **How should AI-specific threat intelligence feeds work?** — C6.4.2 requires AI-specific indicators in alert triage, but production feeds still rarely cover model poisoning indicators, malicious adapter fingerprints, or dataset corruption signatures.
- [ ] **What happens when SCA tools can scan model files?** — Sonatype Lifecycle now scans HF models for pickle risks and malware, but most SCA tools (Trivy, Snyk, Dependabot) still don't treat model files as scannable dependencies. The OWASP AIBOM Generator bridges part of this gap but a full solution is needed.
- [ ] **How should AI agent skill marketplaces be secured?** — OpenClaw/ClawdBot advisories show that agent skill registries face the same supply chain risks as package managers, with extra risk from promptable descriptors, local tool access, and MCP endpoints. No established vetting framework exists for agent skills yet.
- [ ] **How do you break cascading CI/CD-to-AI-library attack chains?** — The LiteLLM compromise (March 2026) showed how a trusted AI gateway library can become a credential-harvesting path when publisher accounts or adjacent scanner workflows are compromised. Current CI/CD hardening (pinned actions, trusted publishing, SLSA attestations) would have mitigated parts of this, but adoption remains uneven.
- [ ] **What does key-pinning-with-rotation (6.2.2) actually look like in practice?** — The Axios hijack (March 2026) showed that direct publisher compromise can bypass normal dependency review when a malicious release appears legitimate enough for package managers. `npm audit signatures`, cosign key policies, trusted publishing, and Sigstore trust roots each cover part of the problem, but no registry provides a turnkey "pin publisher keys per source, require human re-approval on rotation" workflow. Until that exists, 6.2.2 depends on organization-internal tooling.
- [ ] **Is behavioral acceptance testing (6.1.4) practical at scale?** — UK AISI Inspect, HELM Safety v1.0, and DeepEval provide frameworks, but running comprehensive safety/alignment/capability boundary tests adds significant CI time. The 2026 International AI Safety Report warns that models can learn to distinguish test environments from deployment — how do we prevent evaluation gaming?

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

## Related Pages

- [C03-01 Model Authorization & Integrity](../C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md) — Deployment-side companion controls for model registries, AIBOM evidence, signing, and admission checks.
- [C06-05 AI BOM for Model Artifacts](C06-05-AI-BOM-Model-Artifacts.md) — Detailed AI BOM requirements for model artifacts, including CycloneDX ML-BOM/SPDX AI, signed BOMs, completeness checks, and deploy-time query APIs.
- [C01-01 Training Data Origin & Traceability](../C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md) — Upstream dataset provenance and fingerprinting controls that feed C6.3 dataset risk and C6.5 AI BOM evidence.
- [C06-01 Pretrained Model Vetting](C06-01-Pretrained-Model-Vetting.md) — C6.1 detail for signed provenance, malicious-layer scanning, quarantine review, adversarial evaluation, and behavioral acceptance testing.
- [C06-03 Third-Party Dataset Risk](C06-03-Third-Party-Dataset-Risk.md) — C6.3 detail for PII/copyright scrubbing, poisoning risk checks, AI BOM lineage, and hosted-dataset drift monitoring.

---
