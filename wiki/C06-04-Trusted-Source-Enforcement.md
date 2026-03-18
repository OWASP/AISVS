# C6.4 Trusted Source Enforcement

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.4.1–6.4.5

## Purpose

AI pipelines download large artifacts — model weights (often multi-GB), datasets, container images, and specialized libraries — from a variety of external sources. Without strict source enforcement, any network-accessible endpoint becomes a potential supply-chain injection point. This section ensures that all artifact sources are explicitly approved, cryptographically verified, and network-enforced, reducing the attack surface to known, trusted origins.

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

---

## Open Research Questions

- How should organizations handle trust decisions for models accessed only via API (e.g., OpenAI, Anthropic, Google) where weights are never downloaded?
- What is the right model for "trust delegation" when Model A is fine-tuned from Model B — does trust in B's publisher extend to A?
- Can TUF or similar frameworks be adapted for the unique characteristics of ML artifact distribution (multi-GB files, sharded weights, incremental updates)?
