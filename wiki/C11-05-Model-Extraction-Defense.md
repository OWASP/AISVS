# C11.5: Model-Extraction Defense

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 5 | **IDs:** 11.5.1--11.5.5

## Purpose

Detect and deter unauthorized model cloning through API abuse. Model extraction (model stealing) attacks create a functionally equivalent copy of a target model by querying it systematically and training a surrogate on the input-output pairs. Successful extraction compromises intellectual property, enables white-box adversarial attacks against the original model, and bypasses access controls. The primary defenses are rate limiting, query-pattern analysis, and post-hoc identification via watermarking.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.5.1** | **Verify that** inference endpoints enforce per-principal and global rate limits designed to make large-scale query harvesting impractical. | 1 | D | Brute-force model extraction through high-volume query campaigns. Tramer et al. (2016) demonstrated extraction of ML models with tens of thousands of queries; more complex models require millions. Rate limits raise the cost and time required. MITRE ATLAS AML.T0024.002 (Extract ML Model). | Review rate-limiting configuration at both per-principal and global levels. Verify limits are informed by extraction attack query budgets (research literature provides estimates per model type). Test enforcement by exceeding limits. Confirm that rate limits apply across all inference channels (REST API, gRPC, SDK, batch endpoints). | Rate limits alone are insufficient against patient or distributed attackers. Limits must be set below extraction feasibility thresholds while remaining above legitimate usage peaks. Consider adaptive rate limiting that tightens under suspicious patterns. Batch/bulk endpoints may need separate, stricter limits. |
| **11.5.2** | **Verify that** extraction-alert events include offending query metadata and are integrated with incident-response playbooks. | 2 | V | Undetected or poorly responded-to extraction attempts. Without integration into incident response, detection is useless. Alert metadata enables forensic analysis and potential legal action. | Review alert event schema for completeness (principal ID, query content/hashes, timestamps, volumes, source IPs). Verify integration with SIEM or incident-response platform. Confirm incident-response playbook includes extraction-specific procedures (account suspension, legal review, forensic preservation). Test end-to-end: trigger an extraction alert and verify the playbook is initiated. | Alert fatigue is a real risk if extraction detection has high false-positive rates. Playbooks should differentiate between confirmed extraction and suspicious-but-ambiguous patterns. Legal response options depend on jurisdiction and terms of service. |
| **11.5.3** | **Verify that** query-pattern analysis (e.g., query diversity, input distribution anomalies) feeds an automated extraction-attempt detector. | 2 | D/V | Sophisticated extraction attacks that stay within rate limits but exhibit distinctive query patterns. Extraction queries often show unusual input distribution characteristics: uniform coverage of input space, systematic grid-like sampling, or distribution mismatch with legitimate traffic. | Review detection logic for query-pattern features (input distribution statistics, query diversity metrics, temporal patterns, feature-space coverage analysis). Verify detector is trained or calibrated against known extraction query patterns. Test with simulated extraction campaigns and confirm detection. Review false-positive rates against legitimate high-volume users. | Sophisticated attackers can mimic legitimate query distributions by mixing extraction queries with noise or using active learning strategies that look like normal exploration. Detection effectiveness depends heavily on baseline traffic characteristics. For public/free-tier models, distinguishing extraction from legitimate heavy use is particularly difficult. |
| **11.5.4** | **Verify that** model watermarking or fingerprinting techniques are applied so that unauthorized copies can be identified. | 3 | D | Inability to prove ownership or detect unauthorized copies of extracted models. Watermarking embeds identifiable patterns in model behavior (backdoor-based watermarks) or outputs (output-marking) that persist through extraction and can be verified against suspected copies. | Review watermarking implementation: technique used (backdoor-based, parameter-based, output-marking), verification procedure, impact on model accuracy. Test watermark persistence by simulating extraction (train a surrogate model) and verifying the watermark survives. Verify that watermark verification does not require sharing sensitive model information. | Watermark robustness is an active research area. Many watermarking schemes can be removed through fine-tuning, pruning, or distillation. Backdoor-based watermarks are the most robust but raise ethical concerns about intentional backdoors. Output-marking watermarks may not survive extraction. No industry standard watermarking scheme exists. |
| **11.5.5** | **Verify that** watermark verification keys and trigger sets are protected with access controls equivalent to other critical cryptographic material. | 3 | D | Compromise of watermark verification materials, enabling an attacker to remove or forge watermarks. If trigger sets are leaked, the watermark can be specifically targeted for removal. If verification keys are compromised, ownership proofs are invalidated. | Review access controls on watermark keys and trigger sets: storage location, encryption, access logging, personnel restrictions. Verify that access controls meet or exceed the organization's standards for cryptographic key management. Confirm separation of duties between watermark embedding and verification roles. | This requirement only applies if watermarking (11.5.4) is implemented. The security of the watermark scheme depends entirely on the secrecy of verification materials. Key management infrastructure may need to be extended to accommodate non-standard key types (trigger sets are not cryptographic keys but require similar protection). |

---

## Related Standards & References

- [MITRE ATLAS AML.T0024.002 -- Extract ML Model](https://atlas.mitre.org/techniques/AML.T0024.002) -- Attack technique description and known cases
- [NIST AI 100-2e2023 -- Model Extraction](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Extraction attacks in the NIST adversarial ML taxonomy
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) -- API abuse and resource consumption attacks
- [Tramer et al., "Stealing Machine Learning Models via Prediction APIs" (2016)](https://arxiv.org/abs/1609.02943) -- Foundational model extraction paper
- [Adi et al., "Turning Your Weakness Into a Strength: Watermarking Deep Neural Networks" (2018)](https://arxiv.org/abs/1802.04633) -- Backdoor-based DNN watermarking
- [Kirchenbauer et al., "A Watermark for Large Language Models" (2023)](https://arxiv.org/abs/2301.10226) -- LLM output watermarking

---

## Open Research Questions

- What is the practical risk of model extraction for LLMs served via API -- given the cost of training surrogates, is extraction economically rational compared to training from scratch?
- Can extraction detection distinguish between model extraction and legitimate model distillation (which may be permitted under some licensing)?
- How robust are current watermarking schemes against extraction-then-fine-tuning pipelines that are standard in transfer learning?
- Should model extraction defenses focus on prevention (making extraction harder) or detection (identifying extracted copies after the fact)?
- How do multi-modal models change the extraction threat model -- can an attacker extract one modality more easily than others?

---
