# C11.5: Model-Extraction Defense

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 5 | **IDs:** 11.5.1--11.5.5

## Purpose

Detect and deter unauthorized model cloning through API abuse. Model extraction (model stealing) attacks create a functionally equivalent copy of a target model by querying it systematically and training a surrogate on the input-output pairs. Successful extraction compromises intellectual property, enables white-box adversarial attacks against the original model, and bypasses access controls. The primary defenses are rate limiting, query-pattern analysis, and post-hoc identification via watermarking.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.5.1** | **Verify that** inference endpoints enforce per-principal and global rate limits designed to make large-scale query harvesting impractical. | 1 | D | Brute-force model extraction through high-volume query campaigns. Tramer et al. (2016) demonstrated extraction of ML models with tens of thousands of queries; more complex models require millions. Rate limits raise the cost and time required. MITRE ATLAS AML.T0024.001 (Model Inversion/Extraction). As of early 2026, LLM inference costs have dropped roughly 50x per year, meaning extraction is becoming economically cheaper — making rate limits even more critical. | Review rate-limiting configuration at both per-principal and global levels. Verify limits are informed by extraction attack query budgets (research literature provides estimates per model type). Test enforcement by exceeding limits. Confirm that rate limits apply across all inference channels (REST API, gRPC, SDK, batch endpoints). Tools: Cloudflare Advanced Rate Limiting, AWS WAF rate-based rules, Kong rate-limiting plugin, Gravitee (supports REST, WebSocket, and Kafka with 50+ built-in policies). | Rate limits alone are insufficient against patient or distributed attackers. Limits must be set below extraction feasibility thresholds while remaining above legitimate usage peaks. Consider adaptive rate limiting that tightens under suspicious patterns. Batch/bulk endpoints may need separate, stricter limits. Operation Bizarre Bazaar (Dec 2025–Jan 2026) demonstrated that exposed inference endpoints without rate limiting are actively targeted at scale — attackers averaged 972 daily attempts against unprotected AI infrastructure. |
| **11.5.2** | **Verify that** extraction-alert events include offending query metadata and are integrated with incident-response playbooks. | 2 | V | Undetected or poorly responded-to extraction attempts. Without integration into incident response, detection is useless. Alert metadata enables forensic analysis and potential legal action. | Review alert event schema for completeness (principal ID, query content/hashes, timestamps, volumes, source IPs). Verify integration with SIEM or incident-response platform. Confirm incident-response playbook includes extraction-specific procedures (account suspension, legal review, forensic preservation). Test end-to-end: trigger an extraction alert and verify the playbook is initiated. | Alert fatigue is a real risk if extraction detection has high false-positive rates. Playbooks should differentiate between confirmed extraction and suspicious-but-ambiguous patterns. Legal response options depend on jurisdiction and terms of service. |
| **11.5.3** | **Verify that** query-pattern analysis (e.g., query diversity, input distribution anomalies) feeds an automated extraction-attempt detector. | 2 | D/V | Sophisticated extraction attacks that stay within rate limits but exhibit distinctive query patterns. Extraction queries often show unusual input distribution characteristics: uniform coverage of input space, systematic grid-like sampling, or distribution mismatch with legitimate traffic. MITRE ATLAS AML.T0024.000 (Training Data Membership Inference) also relies on systematic querying that produces detectable patterns. | Review detection logic for query-pattern features (input distribution statistics, query diversity metrics, temporal patterns, feature-space coverage analysis). Verify detector is trained or calibrated against known extraction query patterns. PRADA (Juuti et al., IEEE Euro S&P 2019) analyzes the distribution of consecutive API queries and detects all known model extraction attacks with no false positives. HODA extends this by analyzing the hardness-degree histogram of query sequences to distinguish adversarial from benign usage. Test with simulated extraction campaigns and confirm detection. Review false-positive rates against legitimate high-volume users. | Sophisticated attackers can mimic legitimate query distributions by mixing extraction queries with noise or using active learning strategies that look like normal exploration. Detection effectiveness depends heavily on baseline traffic characteristics. For public/free-tier models, distinguishing extraction from legitimate heavy use is particularly difficult. The 2025 LLM extraction survey identifies prompt-targeted attacks (stealing system prompts and few-shot examples) as an emerging extraction vector that current query-pattern detectors may not cover — these attacks look similar to legitimate prompt engineering. |
| **11.5.4** | **Verify that** model watermarking or fingerprinting techniques are applied so that unauthorized copies can be identified. | 3 | D | Inability to prove ownership or detect unauthorized copies of extracted models. Watermarking embeds identifiable patterns in model behavior (backdoor-based watermarks) or outputs (output-marking) that persist through extraction and can be verified against suspected copies. | Review watermarking implementation: technique used (backdoor-based, parameter-based, output-marking, or newer approaches like Semantically Conditioned Watermarks), verification procedure, impact on model accuracy. Test watermark persistence by simulating extraction (train a surrogate model) and verifying the watermark survives. For LLMs, evaluate SCW-style fingerprinting (2025) that uses semantic domain triggers rather than fixed query-key pairs — these survive fine-tuning and quantization better than memorization-based approaches. For edge-deployed models, evaluate FingerMarks (2025), which combines attribution and traceability using progressive adversarial training. Verify that watermark verification does not require sharing sensitive model information. | Watermark robustness is an active research area. Many watermarking schemes can be removed through fine-tuning, pruning, or distillation (USENIX Security 2024 systematically demonstrated attacks against white-box schemes). Backdoor-based watermarks are the most robust but raise ethical concerns about intentional backdoors. Output-marking watermarks may not survive extraction. No industry standard watermarking scheme exists yet, though the ACM Computing Surveys 2025 survey on LLM watermarking/fingerprinting provides a comprehensive taxonomy. Weight permutation-based watermarking with Reed-Solomon error correction codes is a newer approach that preserves model functionality while adding robustness. |
| **11.5.5** | **Verify that** watermark verification keys and trigger sets are protected with access controls equivalent to other critical cryptographic material. | 3 | D | Compromise of watermark verification materials, enabling an attacker to remove or forge watermarks. If trigger sets are leaked, the watermark can be specifically targeted for removal. If verification keys are compromised, ownership proofs are invalidated. | Review access controls on watermark keys and trigger sets: storage location, encryption, access logging, personnel restrictions. Verify that access controls meet or exceed the organization's standards for cryptographic key management. Confirm separation of duties between watermark embedding and verification roles. | This requirement only applies if watermarking (11.5.4) is implemented. The security of the watermark scheme depends entirely on the secrecy of verification materials. Key management infrastructure may need to be extended to accommodate non-standard key types (trigger sets are not cryptographic keys but require similar protection). |

---

## Recent Research (2024--2026)

### Expanded LLM Extraction Threat Model

A comprehensive survey on model extraction attacks and defenses for LLMs (June 2025) identifies three primary attack categories beyond traditional functionality extraction: **training data extraction** (exploiting memorization to recover sensitive training examples via crafted prompts), **prompt-targeted attacks** (stealing system prompts, few-shot examples, and other prompt IP), and **parameter recovery** (reverse-engineering internal weights). This expanded threat model means that rate limiting (requirement 11.5.1) and query-pattern analysis (11.5.3) must account for all three attack vectors, not just functionality cloning.

### Adaptive Watermarking: ModelShield

**ModelShield** (IEEE TIFS, January 2025) introduces adaptive and robust watermarking that dynamically adjusts protection strength based on query patterns. Unlike static watermarking schemes that can be characterized and removed, ModelShield strategically perturbs responses while maintaining high utility for legitimate users. This addresses a key gap in requirement 11.5.4: static watermarks are increasingly vulnerable to removal through fine-tuning and pruning, while adaptive approaches resist these attacks more effectively.

### Explanation-Based Watermarking (EaaW)

**Explanation as a Watermark (EaaW)** (2024) introduces a novel paradigm that embeds multi-bit watermarks into feature attribution explanations rather than model predictions. This means verification behaviors are implanted in the explanation layer rather than the output layer, making the watermark invisible to standard extraction pipelines that only replicate input-output mappings. EaaW supports multi-bit encoding, enabling richer ownership claims than single-bit backdoor watermarks.

### Watermark Vulnerability Research

USENIX Security 2024 research ("How to Break White-Box DNN-Watermarking Schemes") systematically demonstrated attacks against existing white-box watermarking schemes, showing that many can be removed or forged. This directly validates requirement 11.5.5's emphasis on protecting watermark verification keys and trigger sets -- if an attacker gains access to verification materials, watermark schemes are fundamentally compromised. Organizations implementing watermarking should assume adversaries will attempt both extraction-then-removal and direct watermark attacks.

### Semantically Conditioned Watermarks for LLMs

A May 2025 paper introduces **Semantically Conditioned Watermarks (SCW)**, a paradigm shift in LLM fingerprinting. Instead of teaching a model to memorize fixed query-key pairs (which break under fine-tuning and quantization), SCW uses an entire semantic domain (e.g., a specific language or topic area) as the trigger. The model diffuses a statistical watermarking signal throughout all responses generated from that domain. This makes the fingerprint both stealthier and more robust — it survives standard deployment modifications that compromise traditional approaches. Model owners verify ownership by querying the predetermined semantic domain and detecting the watermark statistically.

### FingerMarks: Multi-Bit Edge Model Watermarking

**FingerMarks** (MDPI Electronics, 2025) addresses a gap that earlier edge-deployment protections (TransLinkGuard, CoreGuard) left open: combining model attribution with user traceability. FingerMarks embeds multi-bit watermarks using a progressive adversarial training strategy, enabling organizations to identify both which model was stolen and which edge node user was responsible. Evaluation across multiple datasets confirms robustness against common removal attacks.

### Edge Deployment Protection

Earlier work on **TransLinkGuard** and **CoreGuard** addresses model extraction defense for edge-deployed models where rate limiting and API-level defenses are not available. These techniques embed architectural-level watermarks that persist even when models are deployed on untrusted hardware, extending the protection scope beyond API-served models.

### Operation Bizarre Bazaar: Real-World LLMjacking at Scale

In December 2025–January 2026, Pillar Security documented **Operation Bizarre Bazaar**, the first publicly attributed systematic campaign targeting exposed LLM and MCP endpoints. Across 35,000 attack sessions averaging 972 daily attempts, attackers scanned for Ollama (port 11434) and OpenAI-compatible APIs (port 8000), validated access with placeholder API keys, then resold access through silver.inc — a marketplace offering discounted access to 30+ LLM providers without authorization. The threat actor ("Hecker") operated from Netherlands-based bulletproof hosting. This incident validates that model extraction and API abuse are not theoretical — unprotected inference endpoints are actively hunted and monetized.

### Falling Inference Costs and Extraction Economics

As of early 2026, LLM inference costs have dropped approximately 50x per year (per Epoch AI analysis), with providers like DeepSeek offering processing at $0.70 per million tokens total. This cost collapse changes the extraction threat model: surrogate training becomes cheaper, making even large-scale extraction economically rational for attackers who previously would have trained from scratch. Rate limits (11.5.1) and query-pattern detection (11.5.3) become more important as the economic barrier to extraction falls.

### Defense Taxonomy

The 2025 LLM extraction survey organizes defenses into three categories that map well to AISVS requirements:
1. **Model Protection** (architectural defenses, output control) -- maps to requirements 11.5.1, 11.5.3, 11.5.4
2. **Data Privacy Protection** (preventing training data extraction, output sanitization) -- connects to C11.3 and C11.4
3. **Prompt Protection** (watermarking prompts, query monitoring for prompt theft) -- an emerging concern not yet explicitly covered in the current requirements

### MITRE ATLAS and SAFE-AI Framework Alignment

As of October 2025, MITRE ATLAS contains 15 tactics, 66 techniques, and 46 sub-techniques. The October 2025 update added 14 new agent-focused techniques in collaboration with Zenity Labs, addressing autonomous AI agent security risks. MITRE's **SAFE-AI** framework provides organizational controls mapped to the ATLAS taxonomy, including specific guidance on model extraction defense through output anomaly monitoring and access restriction to training environments. Model extraction falls under AML.T0024 with sub-techniques for training data membership inference (AML.T0024.000) and model inversion/extraction (AML.T0024.001).

---

## Related Standards & References

- [MITRE ATLAS AML.T0024.002 -- Extract ML Model](https://atlas.mitre.org/techniques/AML.T0024.002) -- Attack technique description and known cases
- [NIST AI 100-2e2023 -- Model Extraction](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Extraction attacks in the NIST adversarial ML taxonomy
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) -- API abuse and resource consumption attacks
- [Tramer et al., "Stealing Machine Learning Models via Prediction APIs" (2016)](https://arxiv.org/abs/1609.02943) -- Foundational model extraction paper
- [Adi et al., "Turning Your Weakness Into a Strength: Watermarking Deep Neural Networks" (2018)](https://arxiv.org/abs/1802.04633) -- Backdoor-based DNN watermarking
- [Kirchenbauer et al., "A Watermark for Large Language Models" (2023)](https://arxiv.org/abs/2301.10226) -- LLM output watermarking
- [Survey on Model Extraction Attacks and Defenses for LLMs (June 2025)](https://arxiv.org/abs/2506.22521) -- Comprehensive taxonomy of LLM extraction attacks and three-category defense framework
- [ModelShield: Adaptive and Robust Watermark Against Model Extraction (IEEE TIFS, 2025)](https://dl.acm.org/doi/10.1109/TIFS.2025.3530691) -- Dynamically adaptive watermarking for extraction defense
- [Explanation as a Watermark: Multi-bit Model Ownership Verification (2024)](https://arxiv.org/abs/2405.04825) -- Feature-attribution-based watermarking paradigm
- [How to Break White-Box DNN-Watermarking Schemes (USENIX Security 2024)](https://www.usenix.org/system/files/usenixsecurity24-pegoraro.pdf) -- Systematic attacks against existing watermarking defenses
- [LLM Fingerprinting via Semantically Conditioned Watermarks (2025)](https://arxiv.org/abs/2505.16723) -- Domain-based fingerprinting that survives fine-tuning and quantization
- [FingerMarks: Robust Multi-Bit Watermarking for Remote DNNs (MDPI Electronics, 2025)](https://www.mdpi.com/2079-9292/14/24/4818) -- Multi-bit watermarking combining attribution and user traceability
- [Securing LLMs: Survey of Watermarking and Fingerprinting Techniques (ACM Computing Surveys, 2025)](https://dl.acm.org/doi/10.1145/3773028) -- Comprehensive taxonomy of LLM IP protection techniques
- [PRADA: Protecting Against DNN Model Stealing Attacks (IEEE Euro S&P 2019)](https://arxiv.org/abs/1805.02628) -- Query-distribution-based extraction detection with zero false positives
- [Operation Bizarre Bazaar (Pillar Security, Jan 2026)](https://www.pillar.security/blog/operation-bizarre-bazaar-first-attributed-llmjacking-campaign-with-commercial-marketplace-monetization) -- First attributed LLMjacking campaign targeting exposed inference endpoints
- [MITRE SAFE-AI Framework (2025)](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf) -- Organization-level risk management controls mapped to ATLAS taxonomy

---

## Open Research Questions

- What is the practical risk of model extraction for LLMs served via API -- given the cost of training surrogates, is extraction economically rational compared to training from scratch?
- Can extraction detection distinguish between model extraction and legitimate model distillation (which may be permitted under some licensing)?
- How robust are current watermarking schemes against extraction-then-fine-tuning pipelines that are standard in transfer learning?
- Should model extraction defenses focus on prevention (making extraction harder) or detection (identifying extracted copies after the fact)?
- How do multi-modal models change the extraction threat model -- can an attacker extract one modality more easily than others?
- Should prompt theft (system prompt extraction) be treated as a distinct requirement, or is it adequately covered by existing model extraction controls?
- How should adaptive watermarking schemes like ModelShield be evaluated for robustness -- do they need their own adaptive attack testing (analogous to C11.2.4)?
- Can explanation-based watermarks (EaaW) survive extraction attacks that also replicate feature attribution behavior?
- As inference costs continue to drop (50x/year), at what price point does model extraction become universally cheaper than training from scratch, and how should defense budgets adjust?
- How effective are semantically conditioned watermarks (SCW) against adversaries who know the semantic domain used as the trigger?
- Given the scale of Operation Bizarre Bazaar, should organizations treat exposed inference endpoints as equivalent to exposed databases in terms of security posture?

---
