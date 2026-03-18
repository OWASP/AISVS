# C6.1 Pretrained Model Vetting & Origin Integrity

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.1.1–6.1.5

## Purpose

Pretrained models downloaded from public hubs (Hugging Face, Model Zoo, Civitai, etc.) represent one of the highest-risk supply-chain entry points in AI systems. Unlike traditional software dependencies, model weight files can encode arbitrary executable code (via pickle deserialization), contain hidden backdoor triggers, or carry undisclosed licensing or data-provenance obligations. This section ensures every third-party model is authenticated, scanned, and reviewed before it enters the organization's pipeline.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.1.1** | **Verify that** every third-party model artifact includes a signed origin-and-integrity record identifying its source, version, and integrity checksum. | 1 | D/V | **Tampered or substituted model weights.** An attacker replaces a legitimate model file on a public hub with a trojaned version. Without checksums, the swap is invisible. (MITRE ATLAS AML.T0010.002) | Check that every imported model has a corresponding manifest containing: publisher identity, version tag, and SHA-256/SHA-512 hash. Verify the signature chain back to the publisher's public key. Tools: Sigstore/cosign for model signing, Hugging Face commit hashes, in-toto attestations. | Model signing is still immature. Hugging Face added GPG commit signing in 2023, but most model publishers do not sign. Organizations may need to self-sign upon first import and treat the internal hash as the trust anchor. |
| **6.1.2** | **Verify that** models are scanned for malicious layers or Trojan triggers using automated tools before import. | 1 | D/V | **Pickle deserialization RCE and embedded malware.** PyTorch `.pt`/`.bin` files use Python pickle, which can execute arbitrary code on load. Backdoored models may also contain hidden trigger patterns that activate on specific inputs. (CVE-2024-3568 in Hugging Face Transformers, JFrog 2024 Hugging Face malware findings) | Run Protect AI ModelScan or Trail of Bits Fickling on every weight file before import. Prefer SafeTensors format over pickle-based formats. For Trojan detection, run Neural Cleanse, ABS, or MNTD scans on candidate models. | Trojan-trigger scanning (Neural Cleanse, etc.) is computationally expensive and has known false-negative rates. Pickle scanning is more reliable. Enforcing SafeTensors as the only accepted format is the strongest control but limits model sources. |
| **6.1.3** | **Verify that** model licenses, export-control tags, and data-origin statements are recorded in an AI BOM entry. | 2 | V | **Legal and compliance risk from undisclosed training data or license terms.** Models trained on copyrighted, GDPR-covered, or export-controlled data can expose the organization to lawsuits or regulatory action. | Audit the AI BOM for each model artifact. Confirm it includes: SPDX license identifier, data-origin summary (e.g., "trained on Common Crawl + proprietary corpus"), and export-control classification (EAR/ITAR if applicable). Cross-reference against the model card if one exists. | Many open-weight models lack clear data-origin disclosures. Organizations may need to perform independent provenance research. The EU AI Act and proposed US executive orders are increasing regulatory pressure here. |
| **6.1.4** | **Verify that** high-risk models (e.g., publicly uploaded weights, unverified creators) remain quarantined until human review and sign-off. | 2 | D/V | **Deployment of unvetted or backdoored models.** Automated pipelines may pull and deploy models without human judgment, allowing compromised artifacts to reach production. | Confirm that a quarantine zone (separate registry, staging namespace, or approval gate) exists. Verify that models from unverified publishers cannot progress past the quarantine stage without a documented human approval record (e.g., Jira ticket, signed review form). | Defining "high-risk" criteria requires organizational policy. Suggested triggers: unknown publisher, no model card, pickle format, model size anomalies, or flagged by automated scanning. |
| **6.1.5** | **Verify that** transfer-learning fine-tunes pass adversarial evaluation to detect hidden behaviors. | 3 | D | **Sleeper-agent attacks and backdoor persistence through fine-tuning.** Research (Anthropic "Sleeper Agents" 2024, BadNets, TrojAI) shows that backdoors in base models can survive fine-tuning. An attacker contributes a poisoned base model; the victim fine-tunes it, unknowingly inheriting the backdoor. | Run adversarial test suites against fine-tuned models, including: trigger-pattern sweeps (randomized input perturbations), activation-clustering analysis, and behavioral probes for known attack patterns. Compare fine-tuned model behavior against a clean baseline on a held-out adversarial evaluation set. | This is computationally expensive and currently lacks standardized tooling. The TrojAI program (IARPA/NIST) is developing benchmarks. Most organizations will need to build custom adversarial evaluation pipelines. Level 3 is appropriate given the tooling gap. |

---

## Related Standards & References

- [MITRE ATLAS AML.T0010 — ML Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
- [MITRE ATLAS AML.T0010.002 — Publish Poisoned Model](https://atlas.mitre.org/techniques/AML.T0010.002)
- [Protect AI ModelScan](https://github.com/protectai/modelscan)
- [Trail of Bits Fickling](https://github.com/trailofbits/fickling)
- [Hugging Face SafeTensors](https://huggingface.co/docs/safetensors/)
- [Neural Cleanse (Wang et al., 2019)](https://people.cs.uchicago.edu/~ravenben/publications/pdf/backdoor-sp19.pdf)
- [Anthropic "Sleeper Agents" (2024)](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training)
- [JFrog Hugging Face Malware Research (2024)](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [NIST TrojAI Program](https://pages.nist.gov/trojai/)

---

## Open Research Questions

- What is the false-negative rate of current Trojan-detection tools (Neural Cleanse, ABS, MNTD) against state-of-the-art backdoor attacks?
- Can model provenance be established for models where training data and training process are not disclosed (closed-weight models accessed via API)?
- How should organizations handle models that are "fine-tune chains" (Model A fine-tuned from Model B fine-tuned from Model C) where provenance may be lost at each step?
- Is there a viable equivalent of Sigstore/cosign for model weight signing that the community will adopt at scale?
