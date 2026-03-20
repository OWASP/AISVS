# C11.2: Adversarial-Example Hardening

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 5 | **IDs:** 11.2.1--11.2.5

## Purpose

Increase resilience to manipulated inputs designed to cause misclassification or policy bypass. Adversarial examples -- inputs crafted with small, often imperceptible perturbations -- remain one of the most studied attack vectors in ML security. This section requires evaluation against known attack techniques, detection mechanisms in production, and (at higher levels) formal verification of robustness properties. The emphasis is on adaptive evaluation: testing defenses against attacks specifically designed to defeat them, not just generic benchmarks.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.2.1** | **Verify that** models serving high-risk functions are evaluated against known adversarial attack techniques relevant to their modality (e.g., perturbation attacks for vision, token-manipulation attacks for text). | 1 | D/V | Misclassification or policy bypass via crafted inputs. For vision: PGD, C&W, AutoAttack. For text: TextFooler, BERT-Attack, character-level perturbations. For audio: Carlini-Wagner audio attacks. MITRE ATLAS AML.T0015 (Evade ML Model). | Review adversarial evaluation reports. Confirm attacks tested are appropriate for the model's modality and deployment context. Verify evaluation uses established toolkits (ART, TextAttack, Garak) or equivalent. Check that evaluation covers white-box and transfer-based attack scenarios relevant to the threat model. | "Known attack techniques" is a moving target. Evaluation should reference a specific attack taxonomy (e.g., NIST AI 100-2) and document which attacks were in-scope. Text-domain adversarial robustness is less mature than vision. For LLMs, the boundary between adversarial examples and prompt injection is blurred. |
| **11.2.2** | **Verify that** adversarial-example detection raises alerts in production pipelines, with blocking or degraded-capability responses for high-risk endpoints or use cases. | 2 | D/V | Successful adversarial attacks in production that go undetected, allowing ongoing exploitation. Runtime evasion where an attacker iteratively refines adversarial inputs against a live system. | Review detection pipeline architecture. Verify alert integration with monitoring systems (C13). Test detection with known adversarial samples and confirm alerts fire. Verify that high-risk endpoints have blocking or degraded responses configured and that detection latency is acceptable for the application's throughput requirements. | Detection methods (input reconstruction error, feature squeezing, statistical tests) have known bypass techniques. Detection adds latency and computational cost. False positive rates must be managed to avoid blocking legitimate inputs. Detection effectiveness varies greatly by attack type and model architecture. |
| **11.2.3** | **Verify that** adversarial training or equivalent hardening techniques are applied where feasible, with documented configurations and reproducible procedures. | 2 | D | Vulnerability to known perturbation-based attacks. Adversarial training (augmenting training data with adversarial examples) is the most empirically validated defense but comes with accuracy trade-offs. Alternatives include input preprocessing, randomized smoothing, and ensemble methods. | Review training configuration for adversarial training parameters (attack method, perturbation budget epsilon, number of attack steps). Verify accuracy/robustness trade-off is documented and accepted. For non-adversarial-training defenses, verify documented rationale for chosen approach and empirical validation. | Adversarial training increases training cost significantly (3-10x). It can reduce clean accuracy by 1-5%. Effectiveness is attack-specific -- training against PGD does not guarantee robustness against C&W or spatially-transformed attacks. For LLMs and generative models, adversarial training is not straightforwardly applicable; equivalent hardening (RLHF, safety training) is the practical alternative. |
| **11.2.4** | **Verify that** robustness evaluations use adaptive attacks (attacks specifically designed to defeat the deployed defenses) to confirm no measurable robustness loss across releases. | 3 | V | False sense of security from evaluating defenses only against generic attacks. Many published defenses have been broken by adaptive adversaries (Carlini et al., "On Evaluating Adversarial Robustness," 2019). Obfuscated gradients and gradient masking can make defenses appear robust when they are not. | Verify that evaluation methodology includes adaptive attacks tailored to the specific defense. Review whether evaluators attempted to circumvent detection, preprocessing, or other defense mechanisms. Check that robustness claims are validated against the strongest known attacks, not just standard benchmarks. Confirm regression testing compares robustness metrics across model versions. | Adaptive attack evaluation requires significant adversarial ML expertise. There is no standardized methodology -- it depends on the specific defense. AutoAttack provides a partial solution for Lp-norm robustness but does not cover all attack types. This is expensive and may require external red-team expertise. |
| **11.2.5** | **Verify that** formal robustness verification methods (e.g., certified bounds, interval-bound propagation) are applied to safety-critical model components where the model architecture supports them. | 3 | V | Adversarial examples that evade empirical testing but exist within the input space. Formal verification provides mathematical guarantees that no perturbation within a defined budget can change the model's prediction. | Review formal verification reports and certified robustness bounds. Verify that the verification method is appropriate for the model architecture (e.g., IBP and CROWN for ReLU networks). Check that the certified perturbation budget is meaningful for the deployment context. Confirm verification covers the specific input regions relevant to safety-critical decisions. | Formal verification does not scale to large models (current methods work for models with tens of thousands of parameters, not millions). Certified bounds are often very loose, providing guarantees only for small perturbation budgets. Not applicable to transformer-based LLMs or most generative models. Practical utility is limited to small, safety-critical classification components. |

---

## Recent Research (2024--2026)

### Adversarial Training Advances for LLMs and VLMs

Adversarial training remains the most empirically validated hardening technique, but recent work has adapted it substantially for foundation models. **Prompt Adversarial Tuning (PAT)** enhances robustness through systematic adversarial example exposure during fine-tuning, enabling improved resistance without architectural modifications. For LLMs, **Adversarial Preference Learning** (ACL 2025 Findings) integrates adversarial robustness objectives directly into RLHF-style alignment, treating adversarial jailbreak prompts as negative preference signals -- bridging the gap between traditional adversarial training and LLM safety training.

**DiffuseDef** (ACL 2025) applies diffusion-based input purification to improve NLP model robustness against adversarial text attacks, reconstructing clean inputs from noisy adversarial perturbations without requiring adversarial training. This represents a shift toward purification-based defenses that decouple robustness from the training pipeline, reducing the 3-10x training cost overhead of classical adversarial training.

### Vision-Language Model Robustness

Chain of Attack (CVPR 2025) demonstrated new cross-modal attack surfaces in vision-language models (VLMs), where adversarial perturbations in one modality (e.g., images) can cascade to compromise outputs that depend on the other modality (text). This confirms that multi-modal systems require modality-specific and cross-modal adversarial evaluation, directly relevant to requirement 11.2.1's call for modality-appropriate testing.

### Certified Robustness Progress

Certified defense methods have advanced beyond Lp-norm bounds for classification. ICLR 2026 work on dissecting adversarial robustness of multi-modal models introduced certified robustness techniques applicable to transformer-based architectures, narrowing the gap between formal verification (requirement 11.2.5) and practical model sizes. However, certified bounds for production-scale LLMs remain out of reach -- current methods scale to models with hundreds of thousands of parameters but not billions.

Hybrid defense strategies that combine certified bounds for safety-critical subcomponents with empirical adversarial evaluation for the full system are emerging as the practical approach for organizations implementing both Level 2 and Level 3 requirements.

### Adversarial Robustness Evaluation Tooling

**AdvERSEM** (StarSEM 2025) provides an adversarial robustness testing and training framework specifically designed for NLP semantic models, complementing existing tools like TextAttack and ART. The growing availability of modality-specific evaluation toolkits reduces the barrier for organizations to implement requirement 11.2.1 and 11.2.4.

---

## Related Standards & References

- [NIST AI 100-2e2023 -- Evasion Attacks](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Comprehensive taxonomy of adversarial ML evasion techniques and mitigations
- [MITRE ATLAS AML.T0015 -- Evade ML Model](https://atlas.mitre.org/techniques/AML.T0015) -- Evasion attack techniques catalog
- [IBM Adversarial Robustness Toolbox (ART)](https://github.com/Trusted-AI/adversarial-robustness-toolbox) -- Framework for adversarial attack simulation and defense evaluation
- [TextAttack](https://github.com/QData/TextAttack) -- NLP adversarial attack and augmentation framework
- [AutoAttack (Croce & Hein, 2020)](https://arxiv.org/abs/2003.01690) -- Ensemble of parameter-free attacks for reliable robustness evaluation
- [Carlini et al., "On Evaluating Adversarial Robustness" (2019)](https://arxiv.org/abs/1902.06705) -- Guidelines for rigorous adversarial robustness evaluation
- [DiffuseDef: Improved Robustness to Adversarial Attacks via Diffusion (ACL 2025)](https://aclanthology.org/2025.acl-long.454.pdf) -- Diffusion-based input purification for NLP adversarial defense
- [Adversarial Preference Learning for Robust LLM Alignment (ACL 2025 Findings)](https://aclanthology.org/2025.findings-acl.1126.pdf) -- Integrating adversarial robustness into RLHF alignment
- [Chain of Attack: Robustness of Vision-Language Models (CVPR 2025)](https://openaccess.thecvf.com/content/CVPR2025/papers/Xie_Chain_of_Attack_On_the_Robustness_of_Vision-Language_Models_Against_CVPR_2025_paper.pdf) -- Cross-modal adversarial attacks on VLMs
- [AdvERSEM: Adversarial Robustness Testing for NLP (StarSEM 2025)](https://aclanthology.org/2025.starsem-1.32.pdf) -- NLP-specific adversarial evaluation framework

---

## Open Research Questions

- Can adversarial robustness for LLMs be meaningfully quantified, or is it fundamentally different from the Lp-norm robustness studied in vision?
- How should organizations prioritize adversarial hardening when clean-accuracy trade-offs exist -- what is an acceptable accuracy loss for a given robustness gain?
- Will formal verification methods ever scale to production-sized models, or will empirical evaluation remain the practical ceiling?
- How do adversarial examples interact with multi-modal models that accept both text and images -- does one modality create attack surfaces for the other?
- What is the relationship between adversarial robustness and out-of-distribution generalization -- can improving one harm the other?
- How should adversarial preference learning (integrating robustness into RLHF) be evaluated -- do alignment-focused adversarial defenses transfer to traditional evasion robustness?
- Can diffusion-based purification defenses like DiffuseDef scale to real-time inference workloads without unacceptable latency?

---
