# C6.6 Supply Chain Attack Monitoring

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 3 | **IDs:** 6.6.1–6.6.3

## Purpose

Preventive controls (vetting, scanning, pinning) reduce supply-chain risk but cannot eliminate it. This section addresses the detection and response layer — ensuring that when a supply-chain compromise does occur, the organization can detect it quickly, respond effectively, and roll back to a known-good state. AI supply chains have unique monitoring challenges: model poisoning may not manifest as a traditional indicator of compromise, and CI/CD pipelines for ML workloads have distinct attack patterns.

## 2024-2026 Landscape: ML Supply Chain Attack Monitoring

The ML supply chain threat landscape has intensified significantly since 2024, with model repositories like Hugging Face becoming primary attack vectors and — as of early 2026 — AI-powered agents themselves joining the attacker toolkit. Research and incident data reveal both the growing sophistication of attacks and the rapid evolution of detection tooling.

### Hugging Face Security Scanning and Evasion

Hugging Face hosts over 700,000 models and has become a high-value target for supply chain attacks. The platform implements PickleScanning (combining ClamAV anti-virus scanning with targeted analysis of imports within pickle files), but this approach has proven insufficient against determined attackers:

- **nullifAI evasion techniques (early 2025):** ReversingLabs discovered malicious models that bypassed Hugging Face's Picklescan detection entirely. Hugging Face responded within 24 hours, removing the models and updating Picklescan, but the incident demonstrated that scanner-evasion is an active adversarial frontier.
- **Three PickleScan zero-day bypasses (mid-2025):** JFrog disclosed CVE-2025-10155, CVE-2025-10156, and CVE-2025-10157 (all CVSS 9.3) — a file extension bypass where renaming malicious pickles with `.bin`/`.pt` extensions caused PickleScan to fail while PyTorch still loaded them, a CRC error bypass in ZIP archives, and an unsafe globals subclass bypass using asyncio submodules. Reported June 29, 2025; fixed in PickleScan v0.0.31 on September 2, 2025. These demonstrated a fundamental divergence between scanner behavior and runtime model loading.
- **MalHug detection pipeline:** Researchers developed a more comprehensive detection system combining dataset loading script extraction, model deserialization analysis, in-depth taint analysis, and heuristic pattern matching. Over three months of monitoring 705,000 models and 176,000 datasets, MalHug uncovered 91 malicious models and 9 malicious dataset loading scripts — far more than platform-native scanning alone detected.
- **Namespace hijacking attacks (2024-2025):** Palo Alto Unit 42 documented how deleted Hugging Face author accounts can be re-registered by attackers, enabling namespace hijacking to distribute malicious model versions under trusted names. This mirrors traditional package repository typosquatting but exploits model-name trust specifically.

### Model Serialization as an Attack Surface

Python's Pickle format remains the dominant serialization mechanism and the primary attack vector. Pickle files are inherently unsafe because they allow embedded Python code execution during deserialization. At least 100 malicious ML model instances have been identified on Hugging Face, with some (e.g., baller423/goober2) executing arbitrary code on victim machines and providing persistent backdoor access.

The industry response has been a push toward **SafeTensors**, which stores only numerical tensor data with no code execution on load and passed an independent security audit with no critical flaws found. However, as of early 2026 roughly 21% of Hugging Face models remain pickle-only, with pickle-format models still downloaded over 400 million times per month — making continuous scanning essential.

### Metadata Poisoning via ML Framework Libraries (January 2026)

Palo Alto Unit 42 disclosed vulnerabilities in three popular AI/ML Python libraries — Nvidia's NeMo (CVE-2025-23304), Salesforce's Uni2TS (CVE-2026-22584), and Apple/EPFL's FlexTok — all with tens of millions of downloads on Hugging Face. These libraries improperly used Hydra's `instantiate()` function to load model metadata, allowing attackers to pass dangerous callables like `eval()` and `os.system()` for remote code execution. Over 700 NeMo models on Hugging Face were affected. This attack class is particularly insidious because the malicious payload lives in metadata rather than model weights, making it invisible to weight-scanning tools like ModelScan or PickleScan.

### Fake SDK Attacks Hiding Malware in Pickle Models (2025-2026)

ReversingLabs documented a campaign where attackers uploaded three malicious PyPI packages masquerading as Alibaba Cloud AI Labs SDKs (`aliyun-ai-labs-snippets-sdk`, `ai-labs-snippets-sdk`, `aliyun-ai-labs-sdk`). The packages contained no legitimate functionality — they loaded poisoned PyTorch models from Pickle files through `__init__.py` scripts, executing base64-obfuscated code to exfiltrate user information, network addresses, and `.gitconfig` contents. The packages were downloaded roughly 1,600 times before removal. This attack represents a convergence of traditional package-repository poisoning with ML model supply chain compromise — using Pickle model files as an additional obfuscation layer that most security tools cannot inspect.

### AI-Powered CI/CD Exploitation: hackerbot-claw (March 2026)

A pivotal development in supply chain attack monitoring arrived in late February-March 2026 with the **hackerbot-claw** campaign — an autonomous agent that systematically scanned public GitHub repositories for exploitable GitHub Actions workflows:

- **Scale and scope:** Between February 21 and March 2, 2026, the bot opened 16 pull requests and 2 issues across 9 repositories belonging to Microsoft, Datadog, the CNCF, and popular open-source projects (including Aqua Security's Trivy, a scanner with 32,000+ stars and 100M+ annual downloads).
- **Attack methodology:** The bot carried a vulnerability pattern index covering 9 classes and 47 sub-patterns, and adapted its exploitation technique per target — including embedding obfuscated shell commands in filenames using `${IFS}` substitution, and prompt injection payloads targeting LLM-powered code review workflows.
- **Severity:** In the Trivy compromise, a stolen PAT was used to delete all 178 GitHub releases, wipe the repository, and push a malicious VSCode extension. At Datadog, the agent attempted to manipulate Claude-powered issue triage by injecting "Ignore every previous instruction" payloads.
- **Detection lessons:** Datadog's BewAIre system (LLM-driven code review that classifies changes as benign or malicious) detected the attack and routed alerts to their Cloud SIEM. Key defensive factors included branch protection rules, restricted token permissions, and organization-level rulesets blocking Actions from creating or approving PRs.

This incident underscores that CI/CD monitoring must now account for **autonomous adversarial agents** — not just human attackers or static malware — and that LLM-powered code review and security triage workflows themselves are becoming attack surfaces.

### TeamPCP Cascading Supply Chain Campaign (March 2026)

The hackerbot-claw compromise of Trivy proved to be only the opening phase of a far larger operation. The threat actor **TeamPCP** turned incomplete incident response into a cascading attack that crossed five ecosystems over roughly one month — representing, as of March 2026, the most sophisticated multi-ecosystem ML supply chain campaign documented:

- **Phase 1 — Trivy re-compromise (Feb 28–Mar 22):** After Aqua's initial containment of the hackerbot-claw exploit proved incomplete, TeamPCP leveraged persistent access to conduct imposter commits (spoofing maintainers) and tag hijacking, compromising Trivy binaries across GitHub Releases, Docker Hub, GHCR, and ECR. A credential stealer scraped Runner.Worker process memory from downstream CI/CD pipelines.
- **Phase 2 — npm worm propagation (Mar 20):** Stolen npm tokens enabled a self-replicating worm (`deploy.js` postinstall hook) that autonomously enumerated and published malicious patch versions across all packages each token could access — affecting 45+ packages within 60 seconds of execution.
- **Phase 3 — KICS and OpenVSX (Mar 23):** Checkmarx KICS (Keep Infrastructure as Code Secure) and the OpenVSX marketplace were compromised via the same imposter commit + tag hijacking vector, deploying backdoored IDE extensions and GitHub Actions.
- **Phase 4 — LiteLLM PyPI compromise (Mar 24):** LiteLLM's CI/CD pipeline ran Trivy without a pinned version. The compromised Trivy action exfiltrated the `PYPI_PUBLISH` token from the GitHub Actions runner. TeamPCP then published backdoored LiteLLM versions 1.82.7 and 1.82.8 directly to PyPI, bypassing official CI/CD. LiteLLM is downloaded roughly 3.4 million times per day; the malicious versions were live for approximately three hours.

**LiteLLM payload details:** The three-stage payload included (1) a credential harvester sweeping SSH keys, cloud credentials, Kubernetes secrets, cryptocurrency wallets, and `.env` files across 50+ categories; (2) a Kubernetes lateral movement toolkit deploying privileged pods (with `hostPID`, `hostNetwork`, and root filesystem mount) to every node in the cluster; and (3) a persistent systemd backdoor (`sysmon.service`) polling `checkmarx[.]zone/raw` every 50 minutes for additional binaries. Version 1.82.8 added a `.pth` file that triggered the payload on *every Python invocation* in the environment, not just when litellm was imported. Exfiltration was encrypted with AES-256-CBC and RSA-4096 before posting to `models.litellm.cloud`.

**Social engineering during response:** When community members began reporting the compromise in GitHub issue #24512, attackers posted 88 bot comments from 73 previously compromised developer accounts in a 102-second window, attempting to suppress and confuse the discussion.

**Strategic targeting:** TeamPCP exclusively targeted security-adjacent software — a vulnerability scanner (Trivy), an IaC analyzer (KICS), and an LLM proxy (LiteLLM) — tools that run with elevated privileges by design, maximizing the return from each compromise.

The campaign's central lesson for monitoring: **incomplete incident response creates cascading risk**. Aqua's failure to fully contain the initial Trivy breach allowed TeamPCP to re-compromise the tool and pivot across five ecosystems. Organizations must verify complete remediation and rotate all potentially exposed credentials, especially CI/CD tokens and PyPI publishing keys.

### Sigstore Model-Signing v1.0 (April 2025)

Cryptographic model signing has matured into a practical defense. In April 2025, Google, NVIDIA, HiddenLayer, and the OpenSSF released **model-signing v1.0** — a Sigstore-based tool for signing and verifying ML models:

- **How it works:** The tool uses Sigstore's Certificate Authority to issue short-lived certificates bound to OIDC tokens (representing developer or workload identities), signs models with `model_signing sign ${MODEL_PATH}`, and records signatures in Sigstore's transparency log (Rekor). Verification checks the signature, certificate, and log inclusion — even after the short-lived certificate expires.
- **Hub integration:** The OpenSSF Model Signing (OMS) specification has been integrated into NVIDIA's NGC (July 2025) and Google's Kaggle, with Hugging Face integration underway. Model hubs can verify signatures on upload or sign unsigned models during the upload process.
- **Scope:** Currently covers model weights and architecture files, with plans to extend to datasets and other ML artifacts. The signing process creates a Sigstore bundle (protobuf stored as JSON) containing verification material and a DSSE envelope with an in-toto statement.
- **Adoption milestones:** Sigstore-signed in-toto attestations are now used by Homebrew (May 2024), PyPI (November 2024), Maven Central (January 2025), and NVIDIA NGC (July 2025).

Model signing directly addresses the fundamental trust gap in model repositories: without cryptographic verification, organizations cannot distinguish an authentic model from a tampered or backdoored version. The transparency log ensures that even a rogue insider cannot release malicious models as if signed by the organization.

### Dedicated Model Scanning Tools

Several purpose-built tools have emerged for ML supply chain monitoring:

- **ModelScan (Protect AI, open source):** Scans models byte-by-byte for unsafe code signatures. Supports H5, Pickle, and SavedModel formats across PyTorch, TensorFlow, Keras, Sklearn, and XGBoost. As of 2025, Protect AI has used ModelScan to evaluate over 400,000 models on Hugging Face, finding over 3,300 models with the ability to execute rogue code.
- **Guardian (Protect AI, enterprise):** Enterprise-grade secure gateway enforcing security policies on ML models before they enter internal environments. Extends ModelScan with proprietary scanning capabilities and CI/CD pipeline integration.
- **HiddenLayer Model Scanner:** Commercial model scanning tool focused on detecting serialization attacks, backdoors, and trojans in model files.
- **ReversingLabs Spectra Assure:** Software supply chain security assessment extended to ML model file analysis using binary analysis capabilities.
- **Black Duck AI Model Scanning (launched October 2025):** Signature-based detection that identifies AI/ML models throughout applications, even when deliberately obscured or not listed in build manifests. Generates SBOMs including identified models to support EU AI Act compliance.
- **Sonatype AI/ML Model Protection:** Scans PyTorch extensions (`.bin`, `.pt`, `.pkl`, `.pickle`) and Hugging Face repository models for malicious code execution, poisoned datasets, and license violations. Integrates into DevOps pipelines with policy-driven adoption gates and derivative model detection.
- **SafePickle (academic, February 2026):** An ML-based detector that identifies malicious Pickle-serialized models through static opcode analysis — extracting opcodes from Pickle bytecode and classifying them with supervised models (RandomForest, CatBoost). Achieves 90% F1-score on curated datasets compared to PickleScan's 19% and ModelScan's 19%, detects all known evasive samples, and runs at sub-millisecond speeds per file. Represents the shift from signature-based to behavioral pickle analysis.
- **Manifest AI Model Scanning:** As of early 2026, Manifest offers continuous scanning with daily assessments of open-weight models from Hugging Face and custom organizational models, providing an always-current view of model risk.

### Runtime Supply Chain Integrity

Runtime integrity monitoring has advanced beyond static scanning to include:

- **Cryptographic hash verification of model binaries on load**, stopping covert alterations at inference time.
- **Anomalous CI/CD behavior detection**, including unusual package source changes, unexpected model registry writes, and GPU resource consumption anomalies.
- **Holistic supply chain governance** that covers models, datasets, and OSS dependencies simultaneously — scanning models for malicious pickles while ignoring the provenance of underlying Python packages leaves the supply chain fundamentally broken.
- **Shadow and canary deployments** as recommended by the [OWASP Secure AI Model Ops Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_AI_Model_Ops_Cheat_Sheet.html): evaluate candidate model behavior on real production inputs without affecting live outputs, and gradually route traffic to new models with rapid rollback capability.

### MITRE ATLAS Supply Chain Techniques

MITRE ATLAS codifies ML supply chain compromise under **AML.T0010** with five sub-techniques that structure monitoring requirements:

| Sub-technique | Target | Monitoring Focus |
|---|---|---|
| AML.T0010.000 | Hardware supply chain | GPU/TPU/embedded device integrity |
| AML.T0010.001 | ML software/frameworks | Framework and library compromise (PyTorch, TensorFlow, etc.) |
| AML.T0010.002 | Data | Poisoned training data from compromised sources |
| AML.T0010.003 | Model | Unvetted model changes and lifecycle infiltration |
| AML.T0010.004 | Container registry | Compromised containers for training/inference |

As of October 2025, MITRE ATLAS integrated 14 new attack techniques and sub-techniques specifically focused on AI Agents and Generative AI systems (developed in collaboration with Zenity Labs), reflecting the evolving threat landscape.

### AI Supply Chain Governance and Standards (2025-2026)

Government and industry standards bodies have moved aggressively to codify AI supply chain monitoring requirements:

- **NSA Joint Guidance — "AI/ML Supply Chain Risks and Mitigations" (March 2026):** A multi-agency cybersecurity information sheet identifying six supply chain risk components (training data, models, software, infrastructure, hardware, and third-party services). Recommends organizations maintain verified model registries, perform integrity checks on all models, conduct malware scanning, and require AI and software bills of materials from all suppliers. Aligns with NIST frameworks and MITRE standards.
- **ML-BOM maturation:** CycloneDX 1.6 (April 2024) added ML-BOM support, and CycloneDX 1.7 (October 2025, ECMA-424 2nd Edition) extended it with data provenance and citation capabilities. SPDX 3.0 (April 2024) included AI profiles. ML-BOMs capture model architecture, training data lineage, inference configuration, evaluation metrics, and bias assessments — going well beyond what a standard SBOM tracks.
- **OWASP AIBOM Project (2025):** Building standardized approaches to AI transparency, including an open-source AIBOM Generator for Hugging Face models and gap assessments of CycloneDX and SPDX for AI-specific use cases.
- **EU AI Act supply chain requirements:** High-risk AI systems must provide technical documentation covering data governance, lifecycle monitoring, and model provenance — creating regulatory demand for the monitoring capabilities described in this section. Cross-mapping to ISO 42001, NIST AI RMF, and BSI AI C4 frameworks simplifies compliance alignment.

A June 2025 Lineaje survey found 48% of security professionals admit their organizations are falling behind on SBOM requirements, with ML-BOM adoption significantly lower — underscoring that governance tooling exists but organizational adoption lags.

- **NIST AI 800-4 — "Challenges to the Monitoring of Deployed AI Systems" (March 2026):** The first federal-level report mapping gaps in post-deployment AI monitoring. Based on three practitioner workshops (200+ experts across academia, industry, and 10+ federal agencies) and an 87-paper literature review, the report identifies six monitoring categories (functionality, operational, human factors, security, compliance, and large-scale impacts) and five cross-cutting challenges: lack of trusted methods and tools, immature information sharing across the value chain, difficulty keeping pace with rapid change, misaligned organizational incentives, and significant resource requirements. The security monitoring category specifically highlights insufficient detection methods for adversarial attacks and deceptive system behavior. NIST positions post-deployment monitoring as "a crucial practice for confident, wide-spread AI adoption" and explicitly calls for standardized vocabulary and shared frameworks — which are currently absent.

### AI-Specific Threat Intelligence

AI-specific threat intelligence remains immature compared to traditional software security, but several sources have matured:

- **Protect AI Huntr:** The first dedicated AI/ML bug bounty platform, generating a growing corpus of AI-specific vulnerability reports.
- **MITRE ATLAS:** Continues to expand its taxonomy of ML attack techniques. The SAFE-AI framework report provides structured guidance for applying ATLAS to organizational defense.
- **Sonatype Open Source Malware Index:** As of 2025, Sonatype has identified over 454,600 malicious packages across npm, PyPI, Maven Central, NuGet, and Hugging Face, with a cumulative total exceeding 1.233 million blocked malware packages. Q1 2025 alone uncovered over 18,000 malicious open-source packages, many targeting AI ecosystems like PyTorch, TensorFlow, and Hugging Face.
- **Large-scale empirical studies:** Academic research (e.g., arXiv:2410.04490) has begun instrumenting Hugging Face at scale to catalog exploit patterns, providing structured data for detection rule development.
- **NIST AI Security Centers (December 2025):** NIST invested $20M to establish two AI security centers in partnership with MITRE, leveraging ATLAS, CALDERA, and ATT&CK frameworks for manufacturing and critical infrastructure cybersecurity.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **6.6.1** | **Verify that** incident response playbooks include rollback procedures for compromised models or libraries. | 2 | **Delayed or ineffective response to supply-chain compromise (MITRE ATLAS AML.T0010).** Without pre-planned rollback procedures, teams waste critical time during an incident figuring out how to revert to a clean model or library version, extending the window of exploitation. The TeamPCP campaign (March 2026) demonstrated cascading consequences of incomplete incident response: Aqua's failure to fully contain the initial Trivy compromise allowed the attacker to pivot across five ecosystems (GitHub Actions, Docker Hub, npm, OpenVSX, PyPI), ultimately backdooring LiteLLM — a package downloaded 3.4M times/day — with a three-stage payload including Kubernetes lateral movement and persistent backdoors. The malicious versions were live for ~3 hours, and the payload deployed privileged pods to every node in affected clusters. The NeMo/Uni2TS/FlexTok metadata poisoning disclosure (January 2026) affected 700+ models on Hugging Face; organizations needed to rapidly identify and replace affected model versions across their environments. The NSA's March 2026 joint guidance explicitly recommends maintaining verified model registries and defined rollback procedures across all six supply chain components. | Request and review incident response playbooks. Verify they include: identification of the compromised artifact, immediate containment (isolation of affected systems), rollback to the last known-good version (with specific steps for model rollback, container rollback, and library rollback), notification procedures, and post-incident analysis. Conduct a tabletop exercise simulating a cascading supply chain compromise (use the TeamPCP campaign as a scenario template: compromised scanner → stolen CI/CD tokens → backdoored package → Kubernetes lateral movement). Verify the playbook addresses shadow/canary deployment rollback (per OWASP Secure AI Model Ops Cheat Sheet). Validate that rollback SLAs are defined, that model versioning supports point-in-time recovery, and that ML-BOMs (CycloneDX 1.6+) are generated for all deployed models to enable rapid impact assessment during incidents. Verify that playbooks include credential rotation procedures for all CI/CD tokens (especially PyPI publishing keys and GitHub PATs) when any build-pipeline tool is compromised. Cross-reference against the NSA's "AI/ML Supply Chain Risks and Mitigations" guidance (March 2026) for completeness. | Model rollback is more complex than code rollback — it may require re-serving a previous model version, updating feature stores, and reverting any downstream systems that consumed the model's outputs. Playbooks should address cascade effects. The TeamPCP incident shows that compromised security tools (scanners, IaC analyzers) create transitive risk — organizations using Trivy in CI/CD had their PyPI tokens stolen without any direct attack on their own infrastructure. Playbooks must account for third-party tool compromise, not just direct attacks on models. The OWASP Secure AI Model Ops Cheat Sheet recommends shadow deployments and canary releases with rapid rollback capability. The metadata poisoning attack class (NeMo CVE-2025-23304, Uni2TS CVE-2026-22584) complicates rollback because malicious payloads in metadata may not be detected by standard model weight scanners — playbooks should include metadata-specific integrity checks. NIST AI 800-4 (March 2026) identifies immature information sharing across the AI value chain as a cross-cutting challenge — incident response playbooks should include communication procedures for upstream and downstream dependencies. |
| **6.6.2** | **Verify that** CI/CD audit logs are streamed to centralized security monitoring with detections for anomalous package pulls or tampered build steps. | 2 | **Stealthy modification of build pipelines (MITRE ATLAS AML.T0010.001, AML.T0010.004).** An attacker with CI/CD access can modify build steps to inject malicious dependencies, alter training configurations, or exfiltrate model weights. The TeamPCP campaign (March 2026) demonstrated this at scale: a compromised Trivy GitHub Action scraped Runner.Worker process memory from downstream CI/CD pipelines, exfiltrating PyPI publishing tokens that enabled the LiteLLM backdoor. The attack exploited unpinned tool versions in CI — LiteLLM's pipeline pulled Trivy from apt without version pinning, inheriting the compromised binary. Earlier, the hackerbot-claw phase exploited `pull_request_target` workflow vulnerabilities across Microsoft, Datadog, and CNCF repositories. The npm worm phase showed how stolen tokens enable autonomous self-replicating propagation — a `deploy.js` postinstall hook published malicious patch versions to 45+ packages within 60 seconds. Earlier incidents include Codecov (2021) and CircleCI (2023). | Confirm that CI/CD platform audit logs (GitHub Actions audit log, GitLab audit events, Jenkins build logs) are forwarded to a SIEM or centralized log platform. Verify detection rules exist for: unusual package source changes, new or modified build steps, downloads from non-approved registries, abnormal build durations (which may indicate injected steps), privilege escalation within CI runners, **pulls of security tools without pinned versions or digest verification**, direct PyPI/npm uploads that bypass CI/CD workflows, and **pull requests from previously unseen accounts or automated agents**. Validate that branch protection rules prevent direct pushes, that GitHub token permissions follow least privilege, and that organization-level rulesets block Actions from creating or approving PRs. Verify that **PyPI Trusted Publishers (OIDC-based)** are enabled to eliminate long-lived API tokens — the TeamPCP attack specifically exploited a static `PYPI_PUBLISH` token. Consider deploying LLM-driven code review systems (e.g., Datadog's BewAIre) that classify changes as benign or malicious and route alerts to SIEM. Verify that **Sigstore model-signing** (v1.0, April 2025) or equivalent cryptographic signing is integrated into the build pipeline for all model artifacts, with signatures recorded in a transparency log. | ML-specific CI/CD anomalies are not well-covered by standard SIEM detection rules. Organizations should develop custom detections for: changes to training hyperparameters, dataset source modifications, model registry write operations from unexpected service accounts, GPU resource consumption anomalies, prompt injection attempts in LLM-powered CI workflows, and **`.pth` files in Python packages** (LiteLLM v1.82.8 used a `.pth` file to trigger its payload on every Python invocation, not just on import). The TeamPCP campaign revealed that security-adjacent tools (vulnerability scanners, IaC analyzers, LLM proxies) are high-value targets because they run with elevated privileges by design — monitoring should flag unusual behavior from these tools specifically. The SecureAI-Flow framework (2025) proposes federated autonomous agents for pipeline monitoring — covering static analysis, adversarial robustness checks, container signing, and behavioral anomaly detection. The fake Alibaba SDK campaign (ReversingLabs) showed that malicious Pickle models can be embedded inside traditional Python packages, requiring CI/CD pipelines to scan both package-level and model-level artifacts. The NSA March 2026 guidance recommends treating software dependencies and model artifacts as a unified attack surface in build pipeline monitoring. Trail of Bits (with OpenSSF funding) is improving Sigstore's rekor-monitor to help maintainers detect malicious package releases and monitor signing identities via transparency logs. |
| **6.6.3** | **Verify that** threat-intelligence enrichment tags AI-specific indicators (e.g., model-poisoning indicators of compromise) in alert triage. | 3 | **Missed AI-specific supply-chain threats due to generic threat intelligence (MITRE ATLAS AML.T0010.002, AML.T0010.003).** Standard threat intelligence feeds focus on traditional software supply-chain indicators (malicious packages, compromised credentials). AI-specific threats — poisoned models, backdoored adapters, manipulated datasets, namespace hijacking on Hugging Face — require specialized intelligence sources. The TeamPCP campaign (March 2026) produced concrete IoCs that generic feeds would miss: `.pth` files triggering payloads on Python startup, encrypted exfiltration to `models.litellm.cloud`, persistent systemd services polling `checkmarx[.]zone/raw`, and privileged Kubernetes pods named `node-setup-*`. Sonatype's 2025 data shows over 454,600 new malicious packages identified in a single year (cumulative 1.233M blocked), with many targeting AI ecosystems like PyTorch, TensorFlow, and Hugging Face. | Verify that the organization's threat intelligence platform or SIEM enrichment pipeline includes AI-specific indicator sources. Check for: subscriptions to AI security advisories (Protect AI Huntr, MITRE ATLAS updates, Hugging Face security bulletins, Sonatype Open Source Malware Index), custom indicators for known AI supply-chain attack patterns (pickle deserialization exploits, namespace hijacking, model format evasion techniques like nullifAI, `.pth` payload injection), and tagging/categorization that distinguishes AI supply-chain alerts from general software supply-chain alerts in the triage workflow. Validate that model scanning tools (ModelScan, Guardian, Black Duck, Sonatype) feed findings into the same enrichment pipeline. Verify that MITRE ATLAS AML.T0010 sub-techniques are mapped into the organization's threat model. Confirm that the enrichment pipeline ingests IoCs from recent campaigns (TeamPCP C2 domains, compromised package hashes) and that Sigstore transparency log monitoring (via rekor-monitor) feeds into threat intelligence for detecting unauthorized model or package signing events. | AI-specific threat intelligence is maturing but still lacks a dedicated equivalent of VirusTotal or the NVD. NIST AI 800-4 (March 2026) identifies immature information sharing across the AI value chain as a fundamental barrier, and the absence of trusted standards for monitoring methodologies compounds the problem. As of December 2025, NIST invested $20M in two AI security centers partnering with MITRE, leveraging ATLAS, CALDERA, and ATT&CK frameworks — this should accelerate standardization. The NSA's March 2026 joint guidance adds government-level endorsement for AI-specific threat intelligence integration, recommending that organizations maintain visibility across all six supply chain components (data, models, software, infrastructure, hardware, third-party services). Protect AI's Huntr bug bounty, MITRE ATLAS, Sonatype's malware index, and the NIST AI centers are the closest resources. Sonatype also reports that 28% of LLM-assisted dependency upgrades are hallucinations, creating a novel threat vector where AI agents introduce non-existent or malicious packages. The emergence of ML-based scanner alternatives like SafePickle (90% F1 vs. PickleScan's 19%) suggests that threat intelligence should include behavioral indicators from opcode analysis, not just signature-based IOCs. The TeamPCP campaign's cross-ecosystem propagation (GitHub Actions → Docker Hub → npm → OpenVSX → PyPI) highlights the need for threat intelligence that correlates indicators across package ecosystems, not just within one registry. |

---

## Related Standards & References

- [MITRE ATLAS — ML Attack Techniques](https://atlas.mitre.org/)
- [MITRE ATLAS AML.T0010 — ML Supply Chain Compromise](https://atlas.mitre.org/)
- [MITRE SAFE-AI Framework Report](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf)
- [Protect AI Huntr — AI/ML Bug Bounty](https://huntr.com/)
- [Protect AI ModelScan — Open Source Model Scanning](https://github.com/protectai/modelscan)
- [HiddenLayer Model Scanner](https://hiddenlayer.com/model-scanner/)
- [Black Duck AI Model Scanning](https://www.blackduck.com/blog/black-duck-ai-model-scanning.html)
- [Sonatype — Threats in AI/ML Models](https://help.sonatype.com/en/threats-in-ai-ml-models.html)
- [Sonatype 2026 State of the Software Supply Chain](https://www.sonatype.com/state-of-the-software-supply-chain/2026/open-source-malware)
- [ReversingLabs — Malicious ML Models on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- [Palo Alto Unit 42 — Model Namespace Reuse Attack](https://unit42.paloaltonetworks.com/model-namespace-reuse/)
- [JFrog — Malicious Hugging Face ML Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [Datadog — Stopping hackerbot-claw with BewAIre](https://www.datadoghq.com/blog/engineering/stopping-hackerbot-claw-with-bewaire/)
- [StepSecurity — hackerbot-claw GitHub Actions Exploitation](https://www.stepsecurity.io/blog/hackerbot-claw-github-actions-exploitation)
- [OWASP Secure AI Model Ops Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_AI_Model_Ops_Cheat_Sheet.html)
- [NIST — AI Security Centers Launch (December 2025)](https://www.nist.gov/news-events/news/2025/12/nist-launches-centers-ai-manufacturing-and-critical-infrastructure)
- [Large-Scale Exploit Study of AI/ML Supply Chain Attacks (arXiv:2410.04490)](https://arxiv.org/abs/2410.04490)
- [NIST Cybersecurity Framework — Respond Function](https://www.nist.gov/cyberframework)
- [CISA — Defending CI/CD Pipelines](https://www.cisa.gov/news-events/alerts)
- [OpenSSF Scorecard — Supply Chain Security](https://securityscorecards.dev/)
- [Codecov Supply Chain Attack Analysis (2021)](https://about.codecov.io/security-update/)
- [CircleCI Security Incident (2023)](https://circleci.com/blog/jan-4-2023-incident-report/)
- [JFrog — Three PickleScan Zero-Day Vulnerabilities](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)
- [SafePickle: ML Detection of Malicious Pickle-based Models (arXiv:2602.19818)](https://arxiv.org/html/2602.19818v1)
- [Palo Alto Unit 42 — AI/ML Python Library Metadata Poisoning (January 2026)](https://www.theregister.com/2026/01/13/ai_python_library_bugs_allow/)
- [ReversingLabs — Fake Alibaba SDK Pickle Model Attack](https://www.csoonline.com/article/3998351/poisoned-models-hidden-in-fake-alibaba-sdks-show-challenges-of-securing-ai-supply-chains.html)
- [NSA — AI/ML Supply Chain Risks and Mitigations (March 2026)](https://media.defense.gov/2026/Mar/04/2003882809/-1/-1/0/AI_ML_SUPPLY_CHAIN_RISKS_AND_MITIGATIONS.PDF)
- [CycloneDX ML-BOM Capabilities](https://cyclonedx.org/capabilities/mlbom/)
- [OWASP AIBOM Project](https://owasp.org/www-project-aibom/)
- [ReversingLabs — Secure AI Supply Chain with ML-BOM](https://www.reversinglabs.com/blog/secure-ai-supply-chain-mlbom)
- [Endor Labs — TeamPCP Backdoors LiteLLM via Trivy Compromise](https://www.endorlabs.com/learn/teampcp-isnt-done)
- [Sonatype — Compromised litellm PyPI Package Delivers Multi-Stage Credential Stealer](https://www.sonatype.com/blog/compromised-litellm-pypi-package-delivers-multi-stage-credential-stealer)
- [ReversingLabs — TeamPCP Supply Chain Attack Spreads to LiteLLM](https://www.reversinglabs.com/blog/teampcp-supply-chain-attack-spreads)
- [LiteLLM — Security Update: Suspected Supply Chain Incident (March 2026)](https://docs.litellm.ai/blog/security-update-march-2026)
- [GitGuardian — Rapid Response to the LiteLLM Supply Chain Attack](https://blog.gitguardian.com/litellm-supply-chain-attack/)
- [Sigstore Model-Signing v1.0 — Practical Model Signing with Sigstore](https://blog.sigstore.dev/model-transparency-v1.0/)
- [GitHub — sigstore/model-transparency](https://github.com/sigstore/model-transparency)
- [OpenSSF — How Google Uses Sigstore to Secure ML Models](https://openssf.org/blog/2025/07/23/case-study-google-secures-machine-learning-models-with-sigstore/)
- [NIST AI 800-4 — Challenges to the Monitoring of Deployed AI Systems (March 2026)](https://www.nist.gov/news-events/news/2026/03/new-report-challenges-monitoring-deployed-ai-systems)

---

## Open Research Questions

- What are the most reliable indicators of compromise for AI-specific supply-chain attacks (as opposed to traditional software supply-chain IOCs)?
- How can model behavior monitoring (C13) be integrated with supply-chain monitoring to detect poisoning that only manifests in production inference behavior?
- What does an effective AI supply-chain incident response tabletop exercise look like — what scenarios should it cover? The hackerbot-claw incident (2026) provides a concrete scenario template.
- How should organizations handle "slow-burn" supply-chain attacks where poisoning is introduced gradually across multiple dataset or model updates?
- SafePickle (February 2026) demonstrates that ML-based opcode analysis dramatically outperforms signature-based scanning — can this approach be generalized to non-Pickle serialization formats (SavedModel, ONNX), and what are the adversarial robustness limits of the detector itself?
- How should organizations monitor for namespace hijacking attacks on model repositories at scale, given that name-trust is the primary discovery mechanism?
- What is the appropriate balance between SafeTensors adoption mandates and backward compatibility with the large existing corpus of Pickle-serialized models?
- How should CI/CD monitoring evolve to detect cascading supply chain campaigns like TeamPCP (March 2026) that cross five ecosystems and exploit incomplete incident response? What cross-ecosystem correlation capabilities are needed?
- Given that 28% of LLM-assisted dependency upgrades are hallucinations (Sonatype 2025), how should organizations validate AI-suggested dependency changes before they enter build pipelines?
- As NIST's AI security centers (launched December 2025) and the NSA's March 2026 joint guidance mature, will they produce standardized AI supply-chain IOC formats analogous to STIX/TAXII for traditional threats?
- The metadata poisoning attack class (NeMo, Uni2TS, FlexTok) exploits framework loading functions rather than model weights — how should scanning tools evolve to inspect configuration and metadata files alongside weight tensors?
- With 48% of organizations falling behind on SBOM requirements (Lineaje 2025) and ML-BOM adoption even lower, what is the realistic path to mandatory ML-BOM generation for all deployed AI models?
- Now that Sigstore model-signing v1.0 (April 2025) provides practical cryptographic signing for ML models, what is the adoption trajectory for mandatory model signing across major hubs (Hugging Face, NGC, Kaggle), and what friction points remain for organizations integrating signing into existing ML pipelines?
- The TeamPCP campaign's `.pth` file injection technique (triggering payloads on every Python invocation) represents a novel persistence mechanism specific to Python ML environments — how should endpoint detection tools evolve to monitor for `.pth`-based attacks?
- NIST AI 800-4 identifies "misaligned organizational incentives" as a cross-cutting barrier to AI monitoring — how can organizations align security monitoring investment with business outcomes when AI-specific supply chain attacks remain low-frequency but high-impact?
