# C6.4 Trusted Source Enforcement

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.4.1–6.4.5

## Purpose

AI pipelines download large artifacts — model weights (often multi-GB), datasets, container images, and specialized libraries — from a variety of external sources. Without strict source enforcement, any network-accessible endpoint becomes a potential supply-chain injection point. This section ensures that all artifact sources are explicitly approved, cryptographically verified, and network-enforced, reducing the attack surface to known, trusted origins.

---

## 2025-2026 Landscape Update

### Malicious Models at Scale: The Numbers Keep Growing

The partnership between Protect AI and Hugging Face, now over a year into operation, has scanned 4.47 million unique model versions across 1.41 million repositories, identifying 352,000 unsafe or suspicious issues across 51,700 models. JFrog's independent analysis flagged 25 models as zero-day malicious — models not detected by any other scanner. As of 2025, JFrog's Software Supply Chain Report documented a **6.5-fold increase** in malicious models on Hugging Face compared to the prior year, with over 1 million new models hitting the platform annually. Malicious package uploads to open-source repositories overall jumped 156% year-over-year.

Common attack patterns on Hugging Face include:

- **Pickle deserialization attacks**: Malicious Python code embedded in `.pt` and `.pkl` model files that executes during model loading. Protect AI and Cisco's ClamAV integration now scan for these at upload time.
- **Library-dependent attack chains**: Exploiting functions from common ML environment libraries (PyTorch, NumPy, Pandas) to stage payloads that appear benign individually but chain into full compromise.
- **Payload obfuscation**: Using compression, encoding, and nested container formats (Keras `.h5`, NeMo `.nemo`) to hide malicious code from single-layer scanners.
- **Framework extensibility exploits**: Abusing custom layer definitions and configuration-based loading, including CVE-2025-1550 in Keras which enabled arbitrary code execution through custom layers.
- **NullifAI evasion techniques**: In early 2025, ReversingLabs discovered malicious models using "nullifAI" evasion that bypassed Picklescan detection entirely. Hugging Face responded within 24 hours, removing the models and updating Picklescan, but the episode demonstrated that scanner evasion is an active arms race.

### Model Namespace Reuse and Model Confusion Attacks

Palo Alto Unit 42 documented a "model namespace reuse" attack in early 2025 where cloud provider model catalogs retrieve models by name from Hugging Face. When a model author deletes or transfers their namespace, an attacker can re-register the abandoned namespace and publish a malicious model under the original path. Any pipeline that references the model by name (without hash pinning) would silently fetch the attacker-controlled version.

In January 2026, Checkmarx published research on a related technique they call **"AI Model Confusion"** — essentially dependency confusion adapted for model registries. Code that loads models using relative paths (e.g., `checkpoints/my-model`) can be tricked into fetching a remote model from Hugging Face if no local copy exists, because the Hugging Face client library falls back to remote resolution by default. Mitigations include setting `HF_HUB_OFFLINE=1`, using `local_files_only=True`, or specifying absolute paths. For enterprise environments, Hugging Face recommends subscribing to Enterprise Hub with an allowlist of approved models.

### Model Signing: From Nascent to v1.0

Model signing has progressed significantly. In April 2025, Google's Open Source Security Team, OpenSSF, NVIDIA, and HiddenLayer released **model-signing v1.0** — the first stable release of the [OpenSSF Model Signing (OMS)](https://github.com/sigstore/model-transparency) specification. Key capabilities as of March 2026:

- **Sigstore-based keyless signing**: Short-lived certificates bound to OpenID Connect tokens, with all signing events recorded in a transparency log for auditability.
- **Platform integration**: Kaggle and Hugging Face support automatic signing during model upload; TensorFlow and PyTorch frameworks support signing via `model.save()` hooks.
- **`pip install model-signing`**: CLI and library for signing and verifying models locally.
- **Kubernetes enforcement**: The [Sigstore Model Validation Operator](https://blog.sigstore.dev/model-validation-operator-v1.0.1/) (v1.0.1) uses mutating webhooks to inject init containers that verify model signatures before workload pods start. If verification fails, the pod is blocked. Currently supports models on PVs, S3/MinIO, and shared volumes.
- **OCI artifact packaging**: Work is underway to package ML models as OCI artifacts, enabling lightweight verification via signed manifests without downloading full model files.

Google now uses OMS across its internal model infrastructure, with Kaggle and NVIDIA NGC both supporting model signing as of mid-2025. Sigstore-signed attestations have also been adopted by Homebrew, PyPI, and Maven Central, establishing a pattern that ML model hubs are following.

For raw model weight files (safetensors, ONNX, GGUF) outside platform-managed hubs, organizations should still implement internal signing-upon-import as a compensating control until OMS adoption broadens further.

### NSA/Five Eyes AI Supply Chain Guidance (March 2026)

In March 2026, the NSA together with Five Eyes partners (ASD, CCCS, GCHQ, NCSC-NZ) released [CSI: AI/ML Supply Chain Risks and Mitigations](https://www.cyber.gov.au/business-government/secure-design/artificial-intelligence/artificial-intelligence-and-machine-learning-supply-chain-risks-and-mitigations), covering six supply chain components: training data, models, software, infrastructure, hardware, and third-party services. Key recommendations relevant to trusted source enforcement:

- Establish **verified model registries** with cryptographic signing across the model lifecycle.
- Require an **AI Bill of Materials (AI-BOM)** identifying models, datasets, libraries, and external services alongside a traditional SBOM.
- Deploy integrity checks and malware scanning **before** operational deployment.
- Define role-based access to models, training data, and configurations with segregation of duties.
- Evaluate external AI providers for inherited risks from their own sub-suppliers.

This guidance provides strong institutional backing for the controls in this section, particularly 6.4.1 (approved sources), 6.4.2 (cryptographic verification), and 6.4.4 (periodic review).

### Private Model Registry Options

Organizations implementing trusted source policies have several options for internal model registries:

- **Hugging Face Enterprise Hub**: Private instance with access controls, audit logging, and model allowlisting. Now recommended by Hugging Face's own security team for large organizations as a mitigation against model confusion attacks.
- **NVIDIA NGC Private Registry**: For NVIDIA GPU-optimized models with enterprise security features; now supports Sigstore-based model signing as of mid-2025.
- **JFrog Artifactory ML**: General-purpose artifact management with ML model support; JFrog and Hugging Face announced a partnership in 2025 to improve ML security and transparency.
- **AWS SageMaker Model Registry / Azure ML Model Registry / GCP Vertex AI Model Registry**: Cloud-native options with IAM integration.
- **Self-hosted solutions**: MinIO or S3-compatible stores with custom admission policies.

### Weight-Level Backdoor Detection: Moving Beyond Format Scanning

Traditional model scanning focuses on unsafe serialization formats (pickle, custom layers), but a new category of tooling targets backdoors embedded directly in learned weights — so-called "sleeper agents" that behave normally until a specific trigger is encountered. In February 2026, Microsoft Research published a [practical scanner for detecting backdoored language models at scale](https://www.microsoft.com/en-us/security/blog/2026/02/04/detecting-backdoored-language-models-at-scale/). The scanner uses three behavioral signals: trigger attention spikes (abnormal attention patterns on specific tokens), memorized poisoning data leaks (coaxing models into regurgitating fragments of the data used to implant the backdoor), and fuzzy trigger activation (testing near-trigger inputs to detect activation gradients). It works on models from 270M to 14B parameters using forward passes only — no retraining required — with a low false-positive rate. The scanner requires access to model weights and tokenizer, making it applicable to open-weight models but not black-box APIs.

This represents an important shift: organizations can no longer rely solely on format-level scanning (Picklescan, ClamAV) and must also consider weight-level behavioral audits for high-risk models. Safer serialization formats like SafeTensors and ONNX separate weights from executable logic, eliminating deserialization-based attacks, but do not prevent weight-level trojans embedded during training or fine-tuning.

### The Trivy VS Code Incident: Insider Threats in Developer Tools (February 2026)

In late February 2026, a former employee with retained publishing credentials uploaded [malicious versions of the Aqua Trivy VS Code extension](https://www.netcrook.com/trivy-vs-code-ai-supply-chain-attack-2026/) to the OpenVSX marketplace. The compromised versions (1.8.12 and 1.8.13) contained crafted prompts that hijacked installed AI coding assistants — Copilot, Claude, Gemini, Codex, and Kiro — directing them to act as "forensic agents" that scanned the developer's system for credentials and financial records, then exfiltrated findings via email, Slack, or GitHub. The malicious versions were detected and removed within 36 hours, but thousands of developers were potentially exposed.

This incident illustrates that trusted source enforcement must extend beyond model artifacts to the entire development toolchain. Even trusted security tools (Trivy is one of the most widely deployed vulnerability scanners) can become supply chain vectors when publishing credentials are not properly revoked. It also highlights a new attack surface: AI coding assistants themselves can be weaponized through prompt injection embedded in trusted extensions.

### Cloud-Native AI Security Posture Management

As of early 2026, several platforms now offer integrated AI supply chain security that goes beyond point scanning:

- **Wiz AI-SPM**: Provides [AI Security Posture Management](https://www.wiz.io/solutions/ai-spm) with format-level inspection to surface risky serialization methods and untrusted model sources. Correlates models with identities, permissions, and data access across the cloud estate. Named a Leader in The Forrester Wave CNAPP, Q1 2026.
- **Datadog AI Supply Chain Monitoring**: [Workload Protection](https://www.datadoghq.com/blog/detect-abuse-ai-supply-chains/) detects supply chain threats using execution contexts that group events belonging to the same compromise chain. GuardDog provides third-party library risk scanning. LLM Observability monitors model integrity with toxicity checks across prompts and responses. New LLM Isolation capabilities (preview) detect and block exploitation of vulnerabilities in production AI models.
- **GUAC (Graph for Understanding Artifact Composition)**: The [OpenSSF GUAC project](https://guac.sh/) is approaching its 1.0 release and merging with the Trustify project. GUAC aggregates SBOMs and AI-BOMs into a queryable graph database, enabling supply chain graph queries for transitive dependency analysis. While not yet AI-BOM-native, the graph model supports ML artifact metadata and can surface gaps in supply chain attestations across an organization's entire software and model inventory.

### EU AI Act Supply Chain Obligations (August 2026)

The EU AI Act's high-risk AI system obligations become fully enforceable on August 2, 2026. Article 15 and related provisions require organizations to maintain supply chain transparency for AI components, including documentation of third-party model origins, dataset provenance, and component dependencies. Organizations must demonstrate that external AI providers meet regulatory requirements — outsourcing does not transfer compliance responsibility. The Act requires that critical third-party AI providers are identified, monitored, and substitutable. Combined with the NSA/Five Eyes guidance (March 2026) and the NIST AI Risk Management Framework, these three frameworks jointly define what "responsible AI supply chain management" means in practice as of mid-2026.

### Network Enforcement for ML Workloads

Egress controls for ML workloads require special consideration. Training and inference containers frequently need to download large artifacts at runtime (tokenizers, configuration files, adapter weights). Organizations should proxy these requests through a scanning intermediary rather than blocking them outright. Service mesh architectures (Istio, Linkerd) can enforce egress policies at the pod level in Kubernetes-based ML platforms.

As of late 2025, **AWS Network Firewall Proxy** (preview) offers managed egress inspection with TLS interception, integrated with NAT Gateway and Transit Gateway. This reduces the operational burden of maintaining self-managed proxy fleets for ML environments. Google Cloud's **Secure Web Proxy** similarly provides managed outbound traffic inspection with URL-level filtering for GCP workloads.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.4.1** | **Verify that** model weights, datasets, and containers are downloaded only from approved sources or internal registries. | 1 | D/V | **Malicious artifacts from untrusted sources** ([ATLAS AML.T0010](https://atlas.mitre.org/techniques/AML.T0010)). Attackers publish trojaned models on public hubs — JFrog documented a 6.5x increase in malicious Hugging Face models in 2025. Checkmarx's "AI Model Confusion" attack (Jan 2026) showed that insecure model loading code can silently fetch remote models when local paths are unresolvable. NullBulge weaponized Hugging Face repos with LockBit ransomware payloads in 2024. The Trivy VS Code incident (Feb 2026) demonstrated that even trusted developer security tools can become supply chain vectors when publishing credentials are not revoked. | Review pipeline configurations, Dockerfiles, and training scripts for artifact download URLs. Confirm all point to an internal registry (Artifactory, Nexus, private Hugging Face Enterprise Hub, S3 bucket) or explicitly approved external sources. Verify `HF_HUB_OFFLINE=1` or `local_files_only=True` is set in code that loads models. Check that an approved-source list exists with named owners. Run `pip audit` and `osv-scanner` against ML dependency trees. Deploy Wiz AI-SPM or Datadog Workload Protection for continuous model artifact monitoring across cloud environments. | Internal mirroring of large model weights (10-100+ GB) requires significant storage infrastructure. Tiered approach recommended: mirror critical models, proxy others through a scanning gateway. The NSA/Five Eyes March 2026 guidance now explicitly calls for verified model registries with AI-BOMs. EU AI Act high-risk obligations (enforceable August 2026) require documented supply chain provenance for third-party AI components. |
| **6.4.2** | **Verify that** cryptographic signatures validate publisher identity before artifacts are cached locally. | 1 | D/V | **Man-in-the-middle or CDN compromise replacing artifacts in transit** ([ATLAS AML.T0010.002](https://atlas.mitre.org/techniques/AML.T0010.002)). Even when downloading from a trusted source, network-level attacks or CDN compromises can substitute artifacts. The model namespace reuse attack (Unit 42, 2025) showed that name-based trust without cryptographic verification enables silent artifact substitution. **Weight-level trojans** embedded during training or fine-tuning can survive format-safe serialization (SafeTensors, ONNX) — Microsoft's February 2026 backdoor scanner demonstrated detection across models from 270M to 14B parameters. | Verify that download scripts or registry clients check cryptographic signatures before writing artifacts to local storage. Confirm adoption of [OpenSSF model-signing](https://github.com/sigstore/model-transparency) (`pip install model-signing`) for Sigstore-based keyless verification. For container images, confirm admission policies require signature verification (Kyverno, OPA Gatekeeper with cosign). For Kubernetes deployments, check whether the Sigstore Model Validation Operator is enforcing pre-pod verification. For high-risk open-weight models, run Microsoft's backdoor scanner to detect sleeper agents via attention spike analysis and memorized poisoning data leak signals. | Model signing adoption has improved substantially since model-signing v1.0 (April 2025). Kaggle and NVIDIA NGC now support automatic signing. However, for self-hosted weight files (safetensors, ONNX, GGUF) outside managed platforms, internal sign-upon-import remains the primary compensating control. OCI artifact packaging for models is under active development but not yet production-ready. Cryptographic signing validates publisher identity but does not detect weight-level trojans — behavioral auditing tools like Microsoft's scanner are a necessary complement. |
| **6.4.3** | **Verify that** egress controls block unauthenticated artifact downloads to enforce trusted-source policy. | 2 | D | **Policy bypass via direct downloads.** Developers may bypass approved registries by downloading directly from public URLs (`wget`, `curl`, `huggingface_hub.download`) in notebooks or ad-hoc scripts, circumventing all vetting controls. The Checkmarx Model Confusion research showed that default Hugging Face client behavior silently fetches remote models when local paths fail — making egress enforcement a critical backstop. | Review network security configuration for egress restrictions on artifact download endpoints. Confirm direct access to public model hubs, PyPI, Docker Hub is blocked or proxied. For AWS environments, evaluate **AWS Network Firewall Proxy** (preview, late 2025) for managed TLS-intercepting egress inspection. For GCP, evaluate **Secure Web Proxy** for URL-level outbound filtering. In Kubernetes, verify Istio/Linkerd egress policies at the pod level. Test by attempting a direct download from a non-approved source within an ML workload namespace. | ML development workflows heavily rely on interactive downloads (Jupyter notebooks, Colab-style environments). Strict egress controls can impede research velocity. Organizations need clear exception processes and a developer-friendly internal registry experience. Air-gapped environments should consider GitLab's security scanning template approach for offline scanner distribution. |
| **6.4.4** | **Verify that** repository allow-lists are reviewed periodically with evidence of business justification for each entry. | 3 | V | **Allow-list sprawl and stale approvals.** Over time, approved source lists accumulate entries that are no longer needed or whose risk profile has changed. The namespace reuse attack (Unit 42) specifically targets stale references — an approved publisher whose namespace was subsequently abandoned becomes an attacker entry point. The NSA March 2026 guidance requires organizations to evaluate external AI providers for inherited risks from their own sub-suppliers. | Request the current approved-source list and its review history. Confirm that each entry has a documented business justification and an assigned owner. Verify reviews occur on a defined schedule (quarterly recommended) with evidence of entries being added, removed, or re-justified. Cross-reference the allow-list against known namespace changes on Hugging Face and Docker Hub. Verify that an AI-BOM and SBOM are maintained per NSA/Five Eyes guidance. | This is primarily a process/governance control. Level 3 reflects the operational maturity required to maintain it consistently. The NSA guidance now provides institutional backing for requiring AI-BOMs alongside traditional SBOMs. |
| **6.4.5** | **Verify that** policy violations trigger quarantining of artifacts and rollback of dependent pipeline runs. | 3 | V | **Propagation of compromised artifacts through pipeline stages.** If a policy-violating artifact is detected after it has already been used in downstream pipeline steps (training, fine-tuning, deployment), those downstream artifacts are also potentially compromised. The NullBulge campaign (2024) demonstrated how compromised extensions propagated through AI tool ecosystems to deliver ransomware. The Trivy VS Code compromise (Feb 2026) showed propagation through developer tool supply chains — malicious code hijacked AI coding assistants to exfiltrate credentials, detected only within 36 hours. Average breach detection takes 276 days (IBM 2025), making automated quarantine critical. | Simulate a policy violation (e.g., introduce an unsigned artifact or a model failing Sigstore Model Validation Operator verification) and verify that: (1) the artifact is moved to a quarantine zone, (2) dependent pipeline runs are identified and flagged, (3) rollback or re-execution from clean artifacts is initiated. In Kubernetes, verify that the Model Validation Operator blocks pod startup for unsigned models. Review incident logs for evidence of past enforcement. Check SIEM integration per NSA guidance for correlating supply chain events. Use GUAC or Datadog Workload Protection to trace transitive dependencies and identify all downstream artifacts potentially affected by a compromised component. | Automated dependency tracking across ML pipeline stages (data prep, training, evaluation, deployment) is improving but still requires custom integration between artifact registry, pipeline orchestrator, and security tooling. The Sigstore Model Validation Operator provides enforcement at the K8s admission level but is currently alpha-stage. GUAC is approaching 1.0 (merging with Trustify) and will support AI-BOM graph queries for transitive dependency analysis. Datadog's execution context grouping provides runtime-level detection of supply chain compromise chains. |

---

## Related Standards & References

- [The Update Framework (TUF)](https://theupdateframework.io/)
- [Sigstore — Keyless Signing](https://www.sigstore.dev/)
- [OpenSSF Model Signing (model-transparency)](https://github.com/sigstore/model-transparency) — v1.0 released April 2025
- [Sigstore Model Validation Operator for Kubernetes](https://blog.sigstore.dev/model-validation-operator-v1.0.1/)
- [Google Case Study: Securing ML Models with Sigstore](https://openssf.org/blog/2025/07/23/case-study-google-secures-machine-learning-models-with-sigstore/)
- [Google Security Blog — Practical Model Signing with Sigstore](https://security.googleblog.com/2025/04/taming-wild-west-of-ml-practical-model.html)
- [Kyverno — Image Signature Verification](https://kyverno.io/docs/writing-policies/verify-images/)
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- [JFrog Artifactory — Remote Repository Proxying](https://jfrog.com/artifactory/)
- [Hugging Face Hub Security](https://huggingface.co/docs/hub/security)
- [NIST SP 800-204D — Strategies for Integration of Software Supply Chain Security](https://csrc.nist.gov/publications/detail/sp/800-204d/final)
- [NSA/Five Eyes — AI/ML Supply Chain Risks and Mitigations (March 2026)](https://www.cyber.gov.au/business-government/secure-design/artificial-intelligence/artificial-intelligence-and-machine-learning-supply-chain-risks-and-mitigations)
- [Protect AI + Hugging Face: 4M Models Scanned — 6 Month Report](https://huggingface.co/blog/pai-6-month)
- [Palo Alto Unit 42 — Model Namespace Reuse Attack](https://unit42.paloaltonetworks.com/model-namespace-reuse/)
- [Checkmarx — AI Model Confusion Supply Chain Attack (Jan 2026)](https://checkmarx.com/zero-post/hugs-from-strangers-ai-model-confusion-supply-chain-attack/)
- [JFrog — Malicious Hugging Face ML Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [Cisco Foundation AI + Hugging Face Supply Chain Security](https://blogs.cisco.com/security/ciscos-foundation-ai-advances-ai-supply-chain-security-with-hugging-face)
- [ReversingLabs — Malicious ML Models on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- [The Hacker News — CISO's Expert Guide to AI Supply Chain Attacks](https://thehackernews.com/2025/11/cisos-expert-guide-to-ai-supply-chain.html)
- [AWS Network Firewall Proxy — Managed Egress Security (Preview)](https://aws.amazon.com/blogs/networking-and-content-delivery/securing-egress-architectures-with-network-firewall-proxy/)
- [Microsoft Security Blog — Detecting Backdoored Language Models at Scale (Feb 2026)](https://www.microsoft.com/en-us/security/blog/2026/02/04/detecting-backdoored-language-models-at-scale/)
- [Wiz — Malicious AI Models: Risks Across the AI Supply Chain](https://www.wiz.io/academy/ai-security/malicious-ai-models)
- [Wiz — AI Security Posture Management (AI-SPM)](https://www.wiz.io/solutions/ai-spm)
- [Datadog — Detecting Abuse in AI Supply Chains](https://www.datadoghq.com/blog/detect-abuse-ai-supply-chains/)
- [GUAC — Graph for Understanding Artifact Composition (OpenSSF)](https://guac.sh/)
- [Trivy VS Code Extension Supply Chain Attack (Feb 2026)](https://www.netcrook.com/trivy-vs-code-ai-supply-chain-attack-2026/)
- [CACM — Malicious AI Models Undermine Software Supply-Chain Security](https://cacm.acm.org/research/malicious-ai-models-undermine-software-supply-chain-security/)

---

## Open Research Questions

- How should organizations handle trust decisions for models accessed only via API (e.g., OpenAI, Anthropic, Google) where weights are never downloaded? The NSA guidance flags third-party AI service providers as a distinct supply chain component requiring their own risk assessment.
- What is the right model for "trust delegation" when Model A is fine-tuned from Model B — does trust in B's publisher extend to A? GUAC's planned AI-BOM support may eventually enable supply chain graph queries for transitive trust.
- With model-signing v1.0 now available and GUAC approaching 1.0, what is the adoption trajectory for end-to-end supply chain attestation? Will OCI artifact packaging for ML models reach production readiness in 2026, enabling signature verification without downloading multi-GB weight files?
- Given both namespace reuse and model confusion attack vectors, should all model references include cryptographic hashes rather than human-readable names, similar to container digest pinning? What tooling can enforce this in Jupyter notebook workflows?
- How should organizations assess "attack vector chaining" risk when scanning models, given that individual components may appear benign but combine into exploits (as seen with library-dependent attack chains on Hugging Face)?
- With the EU AI Act high-risk obligations enforceable August 2026 and the NIST AI RMF maturing alongside ISO 42001, how will organizations reconcile overlapping supply chain transparency requirements across jurisdictions?
- Microsoft's backdoor scanner targets open-weight models up to 14B parameters. How will weight-level behavioral auditing scale to frontier models (100B+ parameters), and what is the path toward standardized backdoor detection benchmarks?
- The Trivy VS Code incident showed that AI coding assistants can be weaponized through prompt injection in trusted extensions. Should trusted source enforcement policies extend to AI tool configurations and extension marketplaces, not just model artifacts?
