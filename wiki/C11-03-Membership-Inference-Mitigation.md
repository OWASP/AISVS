# C11.3: Membership-Inference Mitigation

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 3 | **IDs:** 11.3.1--11.3.3

## Purpose

Limit the ability to determine whether a specific record was in the training data. Membership inference attacks (MIAs) exploit the fact that models tend to behave differently on data they were trained on versus data they have not seen -- typically exhibiting higher confidence, lower loss, or more stable predictions on training members. Successful MIAs can violate privacy regulations (GDPR, CCPA), expose sensitive dataset composition, and undermine commitments about data usage. Differential privacy and output calibration are the most effective known defenses.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.3.1** | **Verify that** model outputs are calibrated (e.g., via temperature scaling or output perturbation) to reduce overconfident predictions that facilitate membership-inference attacks. | 2 | D | Membership inference via confidence-based attacks (Shokri et al., 2017). Overconfident predictions on training data create a distinguishable signal. MITRE ATLAS AML.T0024.000 (Infer Training Data Membership). | Review output layer configuration for calibration mechanisms (temperature scaling, Platt scaling, output noise). Test calibration quality using reliability diagrams or expected calibration error (ECE) on held-out data. Compare confidence distributions between member and non-member samples to verify reduced distinguishability. | Temperature scaling is simple but may not be sufficient against sophisticated attacks (LiRA, neighborhood attacks). Output perturbation (adding noise to logits/probabilities) provides stronger guarantees but reduces prediction utility. Calibration alone does not provide formal privacy guarantees -- it is a practical mitigation, not a complete defense. For LLMs, output calibration applies to token probabilities if exposed via API. |
| **11.3.2** | **Verify that** training on sensitive datasets employs differentially-private optimization (e.g., DP-SGD) with a documented privacy budget (epsilon). | 2 | D | Training data leakage through any model output channel, including membership inference, model inversion, and unintended memorization. Differential privacy (DP) provides a mathematical upper bound on information leakage regardless of the attack. | Review training pipeline configuration for DP mechanisms (gradient clipping, noise injection). Verify documented epsilon value and assess whether it provides meaningful privacy (epsilon < 10 is generally considered useful; epsilon < 1 is strong). Check delta parameter. Verify DP accounting method used (Renyi DP, GDP, or PLD). Confirm utility impact is documented and accepted. | DP-SGD significantly impacts model utility -- accuracy drops of 5-20% are common. Choosing epsilon is a policy decision, not a purely technical one. DP-SGD is computationally expensive (2-10x training cost). Current DP-SGD implementations (Opacus, TensorFlow Privacy) do not scale well to very large models. For LLMs, DP fine-tuning is feasible but DP pre-training is currently impractical. The privacy-utility trade-off is often unacceptable for production deployments. |
| **11.3.3** | **Verify that** membership-inference attack simulations (e.g., shadow-model, likelihood-ratio, or label-only attacks) demonstrate that attack accuracy does not meaningfully exceed random guessing on held-out data. | 3 | V | Residual membership-inference vulnerability after mitigations are applied. Validates that defenses (calibration, DP, regularization) are actually effective rather than assumed to be. | Execute MIA simulations using multiple attack methods: shadow-model attacks (Shokri et al.), likelihood-ratio attacks (LiRA by Carlini et al., 2022), label-only attacks (Choquette-Choo et al., 2021). Compare attack AUC-ROC against 0.5 baseline (random guessing). Document attack configurations, dataset splits, and statistical significance of results. | "Meaningfully exceed random guessing" needs an operational threshold (e.g., AUC < 0.55). MIA effectiveness varies greatly by dataset, model size, and training procedure -- attacks may succeed on some subpopulations even when overall metrics look safe. LiRA is currently the strongest known MIA but requires training many shadow models (computationally expensive). For LLMs, membership inference research is evolving rapidly and attack/defense methods may not transfer from smaller models. |

---

## Related Standards & References

- [MITRE ATLAS AML.T0024.000 -- Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000) -- Attack technique description and known cases
- [NIST AI 100-2e2023 -- Privacy Attacks](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Privacy attack taxonomy including membership inference
- [Shokri et al., "Membership Inference Attacks Against Machine Learning Models" (2017)](https://arxiv.org/abs/1610.05820) -- Foundational MIA paper establishing shadow-model methodology
- [Carlini et al., "Membership Inference Attacks From First Principles" (LiRA, 2022)](https://arxiv.org/abs/2112.03570) -- State-of-the-art likelihood-ratio MIA
- [Opacus (Meta)](https://opacus.ai/) -- Differential privacy training for PyTorch
- [TensorFlow Privacy](https://github.com/tensorflow/privacy) -- DP-SGD implementation for TensorFlow
- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)

---

## Open Research Questions

- What is the practical risk of membership inference for LLMs trained on web-scale data -- does the sheer volume of training data make individual record inference infeasible?
- Can membership inference be meaningfully mitigated for models that are not trained with DP, or is DP the only principled defense?
- How should organizations set the "meaningfully exceed random guessing" threshold in 11.3.3 -- what AUC-ROC value constitutes an acceptable residual risk?
- Are there subpopulation-level membership inference risks that aggregate metrics miss (e.g., high inference accuracy on rare or underrepresented data points)?
- How do retrieval-augmented generation (RAG) systems change the membership inference threat model -- does retrieval create a side channel?

---
