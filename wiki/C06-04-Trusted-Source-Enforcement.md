# C6.4 Trusted Source Enforcement

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.4.1–6.4.5

## Purpose

AI pipelines download large artifacts — model weights (often multi-GB), datasets, container images, and specialized libraries — from a variety of external sources. Without strict source enforcement, any network-accessible endpoint becomes a potential supply-chain injection point. This section ensures that all artifact sources are explicitly approved, cryptographically verified, and network-enforced, reducing the attack surface to known, trusted origins.

---

## 2025-2026 Landscape Update

### Hugging Face: Scale of Malicious Model Discovery

The partnership between Protect AI and Hugging Face, now six months into operation as of early 2025, has produced sobering numbers. Scanning 4.47 million unique model versions across 1.41 million repositories, they identified 352,000 unsafe or suspicious issues across 51,700 models. JFrog's independent analysis flagged 25 models as zero-day malicious -- models that were not detected by any other scanner. These numbers demonstrate that public model registries are active threat surfaces, not passive repositories.

Common attack patterns found on Hugging Face include:

- **Pickle deserialization attacks**: Malicious Python code embedded in `.pt` and `.pkl` model files that executes during model loading. Protect AI and Cisco's ClamAV integration now scan for these at upload time.
- **Library-dependent attack chains**: Exploiting functions from common ML environment libraries (PyTorch, NumPy, Pandas) to stage payloads that appear benign individually but chain into full compromise.
- **Payload obfuscation**: Using compression, encoding, and nested container formats (Keras `.h5`, NeMo `.nemo`) to hide malicious code from single-layer scanners.
- **Framework extensibility exploits**: Abusing custom layer definitions and configuration-based loading, including CVE-2025-1550 in Keras which enabled arbitrary code execution through custom layers.

### Model Namespace Reuse Attacks

Palo Alto Unit 42 documented a "model namespace reuse" attack in early 2025 where cloud provider model catalogs retrieve models by name from Hugging Face. When a model author deletes or transfers their namespace, an attacker can re-register the abandoned namespace and publish a malicious model under the original path. Any pipeline that references the model by name (without hash pinning) would silently fetch the attacker-controlled version. Google now performs daily scans for orphaned model references in response to this disclosure.

### Model Signing: Still Nascent but Progressing

Hugging Face supports GPG-signed commits, but the vast majority of model publishers do not sign their uploads. Sigstore's cosign tooling can be applied to container-based model serving, and Kyverno or OPA Gatekeeper admission controllers can enforce signature verification at deployment time. However, for raw model weight files (safetensors, ONNX, GGUF), there is no widely adopted signing standard as of early 2026. Organizations should implement internal signing-upon-import as a compensating control: when a model passes vetting and is mirrored to an internal registry, the organization signs it with its own key.

### Private Model Registry Options

Organizations implementing trusted source policies have several options for internal model registries:

- **Hugging Face Enterprise Hub**: Private instance with access controls and audit logging.
- **NVIDIA NGC Private Registry**: For NVIDIA GPU-optimized models with enterprise security features.
- **JFrog Artifactory ML**: General-purpose artifact management with ML model support; JFrog and Hugging Face announced a partnership in 2025 to improve ML security and transparency.
- **AWS SageMaker Model Registry / Azure ML Model Registry / GCP Vertex AI Model Registry**: Cloud-native options with IAM integration.
- **Self-hosted solutions**: MinIO or S3-compatible stores with custom admission policies.

### Network Enforcement for ML Workloads

Egress controls for ML workloads require special consideration. Training and inference containers frequently need to download large artifacts at runtime (tokenizers, configuration files, adapter weights). Organizations should proxy these requests through a scanning intermediary rather than blocking them outright. Service mesh architectures (Istio, Linkerd) can enforce egress policies at the pod level in Kubernetes-based ML platforms.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.4.1** | **Verify that** model weights, datasets, and containers are downloaded only from approved sources or internal registries. | 1 | D/V | **Malicious artifacts from untrusted sources.** Attackers publish trojaned models on public hubs (Hugging Face, Docker Hub, GitHub) or host malicious datasets on look-alike domains. Without source restriction, developers may unknowingly import compromised artifacts. (JFrog 2024: 100+ malicious models found on Hugging Face.) | Review pipeline configurations, Dockerfiles, and training scripts for artifact download URLs. Confirm all point to an internal registry (Artifactory, Nexus, private Hugging Face hub, S3 bucket) or explicitly approved external sources. Verify that an approved-source list exists and is maintained. | Internal mirroring of large model weights (10-100+ GB) requires significant storage infrastructure. Organizations may need tiered approaches: mirror critical models, proxy others through a scanning gateway. |
| **6.4.2** | **Verify that** cryptographic signatures validate publisher identity before artifacts are cached locally. | 1 | D/V | **Man-in-the-middle or CDN compromise replacing artifacts in transit.** Even when downloading from a trusted source, network-level attacks or CDN compromises can substitute artifacts. Signature verification ensures the artifact was produced by the claimed publisher. | Verify that download scripts or registry clients check cryptographic signatures (GPG, Sigstore cosign, or TUF metadata) before writing artifacts to local storage. For container images, confirm that admission policies require signature verification (Kyverno, OPA Gatekeeper with cosign verification). | Model signing adoption is very low in the ML community. Hugging Face supports GPG-signed commits but most model publishers do not sign. Organizations may need to implement internal signing upon import as a compensating control. |
| **6.4.3** | **Verify that** egress controls block unauthenticated artifact downloads to enforce trusted-source policy. | 2 | D | **Policy bypass via direct downloads.** Developers may bypass approved registries by downloading directly from public URLs (wget, curl, huggingface_hub.download) in notebooks or ad-hoc scripts, circumventing all vetting controls. | Review network security configuration (firewall rules, proxy policies, DNS filtering) for egress restrictions on artifact download endpoints. Confirm that direct access to public model hubs, PyPI, Docker Hub, etc. is blocked or proxied through a scanning intermediary. Test by attempting a direct download from a non-approved source. | ML development workflows heavily rely on interactive downloads (Jupyter notebooks, Colab-style environments). Strict egress controls can impede research velocity. Organizations need clear exception processes and a developer-friendly internal registry experience. |
| **6.4.4** | **Verify that** repository allow-lists are reviewed periodically with evidence of business justification for each entry. | 3 | V | **Allow-list sprawl and stale approvals.** Over time, approved source lists accumulate entries that are no longer needed or whose risk profile has changed (e.g., a previously trusted publisher's account is compromised). | Request the current approved-source list and its review history. Confirm that each entry has a documented business justification and an assigned owner. Verify that reviews occur on a defined schedule (e.g., quarterly) with evidence of entries being added, removed, or re-justified. | This is primarily a process/governance control. Level 3 reflects the operational maturity required to maintain it consistently. |
| **6.4.5** | **Verify that** policy violations trigger quarantining of artifacts and rollback of dependent pipeline runs. | 3 | V | **Propagation of compromised artifacts through pipeline stages.** If a policy-violating artifact is detected after it has already been used in downstream pipeline steps (training, fine-tuning, deployment), those downstream artifacts are also potentially compromised. | Simulate a policy violation (e.g., introduce an unsigned artifact) and verify that: (1) the artifact is moved to a quarantine zone, (2) dependent pipeline runs are identified and flagged, and (3) rollback or re-execution from clean artifacts is initiated. Review incident logs for evidence of past enforcement. | Automated dependency tracking across ML pipeline stages (data prep, training, evaluation, deployment) is not well-supported by current MLOps tools. Requires custom integration between the artifact registry, pipeline orchestrator, and security tooling. |

---

## Related Standards & References

- [The Update Framework (TUF)](https://theupdateframework.io/)
- [Sigstore — Keyless Signing](https://www.sigstore.dev/)
- [Kyverno — Image Signature Verification](https://kyverno.io/docs/writing-policies/verify-images/)
- [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- [JFrog Artifactory — Remote Repository Proxying](https://jfrog.com/artifactory/)
- [Hugging Face Hub Security](https://huggingface.co/docs/hub/security)
- [NIST SP 800-204D — Strategies for Integration of Software Supply Chain Security](https://csrc.nist.gov/publications/detail/sp/800-204d/final)
- [Protect AI + Hugging Face: 4M Models Scanned — 6 Month Report](https://huggingface.co/blog/pai-6-month)
- [Palo Alto Unit 42 — Model Namespace Reuse Attack](https://unit42.paloaltonetworks.com/model-namespace-reuse/)
- [JFrog — Malicious Hugging Face ML Models with Silent Backdoor](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [Cisco Foundation AI + Hugging Face Supply Chain Security](https://blogs.cisco.com/security/ciscos-foundation-ai-advances-ai-supply-chain-security-with-hugging-face)
- [ReversingLabs — Malicious ML Models on Hugging Face](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)

---

## Open Research Questions

- How should organizations handle trust decisions for models accessed only via API (e.g., OpenAI, Anthropic, Google) where weights are never downloaded?
- What is the right model for "trust delegation" when Model A is fine-tuned from Model B — does trust in B's publisher extend to A?
- Can TUF or similar frameworks be adapted for the unique characteristics of ML artifact distribution (multi-GB files, sharded weights, incremental updates)?
- Given the model namespace reuse attack vector, should model references always include cryptographic hashes rather than human-readable names, similar to container digest pinning?
- What is the right industry standard for model signing? Will Sigstore adoption extend to raw weight files (safetensors, ONNX, GGUF), or will a new ML-specific signing standard emerge?
- How should organizations assess "attack vector chaining" risk when scanning models, given that individual components may appear benign but combine into exploits?
