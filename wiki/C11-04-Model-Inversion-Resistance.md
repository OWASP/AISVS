# C11.4: Model-Inversion Resistance

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 3 | **IDs:** 11.4.1--11.4.3

## Purpose

Prevent reconstruction of private training data or sensitive attributes from model outputs. Model inversion attacks exploit the information a model reveals through its predictions to reconstruct inputs or infer sensitive features of the training data. First demonstrated by Fredrikson et al. (2015) on facial recognition models, these attacks have since been extended to reconstruct text, tabular data, and other modalities. The risk is highest for models trained on sensitive data (medical records, biometric data, PII) where even partial reconstruction can violate privacy.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.4.1** | **Verify that** sensitive attributes are never directly output; where needed, outputs use generalized categories (e.g., ranges, buckets) or one-way transforms. | 1 | D | Direct leakage of sensitive training data attributes through model outputs. Even without a sophisticated attack, a model that directly predicts sensitive attributes (exact age, income, diagnosis) enables trivial reconstruction. | Review model output schema for sensitive attribute exposure. Verify that outputs use appropriate generalization (age ranges instead of exact ages, income brackets instead of exact values). Test with representative queries to confirm sensitive attributes are not exposed in raw form. Check that output transformations are applied consistently across all output channels (API, UI, logs). | Defining "sensitive attributes" requires alignment with data classification policies and applicable regulations (GDPR Article 9 special categories, HIPAA PHI). Generalization reduces prediction utility -- the granularity trade-off must be explicitly accepted. One-way transforms must be irreversible; simple binning may still leak information if bins are narrow enough. |
| **11.4.2** | **Verify that** query-rate limits throttle repeated adaptive queries from the same principal to raise the cost of inversion attacks. | 1 | D/V | Iterative model inversion attacks that require thousands to millions of carefully crafted queries to reconstruct training data. Rate limiting increases attack cost and time, making reconstruction impractical. MITRE ATLAS AML.T0024.001 (Invert ML Model). | Review rate-limiting configuration per principal (user, API key, IP). Verify limits are set based on legitimate usage patterns with margin against inversion attack query budgets. Test rate-limit enforcement by exceeding limits and confirming throttling or blocking. Check that rate limits cannot be trivially bypassed (e.g., by creating new API keys). | Rate limiting is necessary but not sufficient -- sophisticated attackers can spread queries across principals or time. Limits must be tuned to not impact legitimate users. Consider per-query information gain analysis to set limits appropriately. Rate limiting should be complemented by query-pattern analysis (see C11.5.3 for extraction, same principle applies). |
| **11.4.3** | **Verify that** models handling sensitive data are trained with privacy-preserving techniques (e.g., differential privacy, gradient clipping) to limit information leakage through outputs. | 2 | D | Deep model inversion attacks that exploit model parameters or gradients to reconstruct training samples with high fidelity. Differential privacy provides formal bounds on information leakage. Gradient clipping prevents individual samples from disproportionately influencing model parameters. MITRE ATLAS AML.T0024.001. | Review training pipeline for privacy mechanisms (DP-SGD, gradient clipping norms). Verify documented privacy budget (epsilon); as of March 2026, VaultGemma demonstrates that epsilon less than or equal to 2.0 is achievable at 1B-parameter scale. Check for tools like Meta's Opacus (PyTorch DP-SGD with ghost clipping for reduced memory), Google's DP libraries, or TTLoRA-DP for parameter-efficient DP fine-tuning (7.6x fewer parameters than LoRA with better privacy-utility tradeoff at epsilon=0.5). For geometry-aware clipping, evaluate GeoClip which clips gradients in a transformed basis aligned with the gradient distribution geometry. For models without full DP, verify that regularization techniques (dropout, weight decay, early stopping) are applied as partial mitigations, with documented rationale. Verify that privacy mechanisms are applied specifically to training on sensitive data partitions. For verifiable DP compliance, consider VERIDP (March 2026) which uses zero-knowledge proofs for per-iteration verification of correct DP-SGD execution. | Same DP trade-offs as C11.3.2 apply, though VaultGemma's Poisson sampling approach significantly reduces the noise-utility trade-off. Gradient clipping alone (without noise) does not provide formal privacy guarantees but reduces memorization. For models consuming sensitive data at inference time (e.g., RAG over PII), training-time DP does not address the risk -- inference-time output controls are needed instead. Stand-in model distillation offers a deployment-time alternative where DP training is infeasible. TTLoRA-DP (Kunwar et al., 2026) showed that structural constraints in adapter architecture can reduce privacy leakage even without tighter epsilon -- membership inference attack AUC stayed near 51-52% across privacy budgets versus LoRA's 52-58%. GDPR right-to-erasure enforcement (EDPB, March 2025) increasingly treats models capable of reproducing training data as subject to deletion obligations, making DP training a compliance consideration beyond pure security. |

---

## Recent Research (2024--2026)

### Comprehensive Survey and Taxonomy (2025)

A comprehensive survey on deep learning model inversion attacks and defenses (January 2025) provides a systematic taxonomy covering optimization-based, training-based, and GAN-based attack methods, along with defense categories including differential privacy, output perturbation, model architecture modifications, and regularization-based approaches. The survey catalogs 16 state-of-the-art attack and defense methods, establishing that combined defense strategies can mitigate up to 50% of model inversion attacks while maintaining model utility.

### LLM-Specific Inversion Attacks

Recent work has demonstrated that LLMs face novel inversion attack surfaces distinct from traditional discriminative models:

- **Activation Inversion Attacks (AIA)** target decentralized and split-learning LLM training setups, using public datasets to construct shadow datasets of text labels and corresponding activations, then training attack models to reconstruct training data from intermediate activations. This is particularly relevant for federated or distributed LLM training architectures.
- **Cross-lingual Model Inversion** research shows that multilingual language models are more vulnerable to inversion attacks than monolingual models, with black-box multilingual and cross-lingual inversion attacks achieving higher reconstruction fidelity. Organizations deploying multilingual models should factor this into their inversion risk assessments.
- **PII Extraction from Llama 3** (Sivashanmugam, 2025) demonstrated that even smaller-scale LLMs like Llama 3.2 are susceptible to model inversion attacks that extract memorized PII -- passwords, email addresses, and account numbers were recovered through carefully crafted prompts. The attack leverages temperature tuning to surface rare memorized phrases and adaptive querying based on previous outputs, highlighting that inversion vulnerability grows as models scale.
- **Split-Learning Inversion** (Shu et al., 2025) introduced mutual information entropy analysis for transformer-based LLMs in split learning frameworks, with a two-stage attack that first projects intermediate representations into the embedding space, then uses a generative model to reconstruct the original text from those embeddings.

### Advanced Attack Techniques

**Stepwise Gradient Inversion (SGI)** (2024) significantly improves image reconstruction quality through a two-stage approach: first modeling the coefficient of variation of features and applying an evolutionary algorithm for label recovery, then performing stepwise gradient inversion. SGI demonstrates that inversion attacks continue to improve in fidelity, reinforcing the need for proactive defenses (requirements 11.4.1-11.4.3) rather than relying on attack difficulty as a defense.

### Embedding Protection

**Embedding Guard (EGuard)** (2024) employs transformer-based projection networks and textual mutual information optimization to protect embeddings while retaining LLM utility. This addresses a gap in requirement 11.4.3 where traditional DP approaches are too costly -- EGuard provides embedding-level protection without full DP-SGD overhead, applicable to models where embeddings are exposed through APIs or shared architectures.

### MIBench Benchmark

**MIBench** (2025) is the first standardized benchmark for model inversion attacks and defenses, integrating 16 state-of-the-art methods with consistent evaluation metrics. This enables reproducible comparison of defense effectiveness and directly supports verification approaches for requirements 11.4.1-11.4.3 by providing standardized evaluation methodology.

### Vision-Language Model Inversion (2025)

As of early 2025, model inversion attacks have been extended to vision-language models (VLMs). Research demonstrated four novel attack strategies -- Token-based MI (TMI), Convergent Token-based MI (TMI-C), Sequence-based MI (SMI), and SMI with Adaptive Token Weighting (SMI-AW) -- successfully attacking LLaVA-v1.6, Qwen2.5-VL, and MiniGPT-v2. Human evaluators rated the reconstructed images at 75.31% attack accuracy on FaceScrub, and automated evaluation reached 77.40% on Stanford Dogs. Sequence-level gradient aggregation proved significantly more effective than independent token-level optimization, and logit-maximization loss outperformed cross-entropy. Notably, the paper proposed no new defenses, underscoring the gap between attack sophistication and available countermeasures for multimodal models.

### VaultGemma: Production-Scale DP (2025)

Google released VaultGemma (September 2025), the largest (1B parameters) open model fully pre-trained with differential privacy. Trained on the Gemma 2 architecture with DP-SGD at a privacy budget of epsilon less than or equal to 2.0 and delta less than or equal to 1.1e-10, VaultGemma demonstrates that DP can scale to production-grade language models. Key innovations include Poisson sampling (replacing uniform batches to reduce noise requirements) and new scaling laws for DP models that define optimal training configurations for a given privacy-compute budget. Open-sourced on Hugging Face and Kaggle, VaultGemma is directly relevant to requirement 11.4.3 -- it proves that formal privacy guarantees no longer require sacrificing most model utility, particularly for regulated industries (healthcare, finance, legal).

### Stand-In Model Protection (2025)

Stand-in model protection introduces a synthetic defense layer against both membership inference and model inversion attacks. Rather than exposing the trained model directly, a stand-in model is distilled from the original and serves as the public-facing endpoint. This limits the information an adversary can extract, though the approach cannot fully control how closely the stand-in's unlabeled dataset resembles the original training data. The trade-off between fidelity and privacy remains an active area of work -- high-fidelity stand-ins may still leak sensitive patterns, while low-fidelity versions degrade downstream utility.

### Combined Defense Strategies

Research from 2024-2025 has demonstrated that no single defense is sufficient. The most effective approaches combine multiple layers: differential privacy during training, adaptive noise injection at inference, output generalization (requirement 11.4.1), and rate limiting (requirement 11.4.2). Combined systems integrating DP, federated learning, adaptive noise, and ensemble-based obfuscation show substantially better protection than any individual technique.

### FedGuard-CI (January 2026)

FedGuard-CI is a novel privacy-preserving framework published in January 2026 that integrates dual-stage differential privacy, trust-aware secure aggregation, and a Model Inversion Risk Estimator (MIRE). MIRE provides a quantitative risk score for model inversion vulnerability, enabling organizations to assess their exposure before deployment rather than relying solely on post-hoc defenses. This approach is particularly relevant for federated learning deployments where model updates are shared across participants.

### Data-Free Selective Unlearning via Model Inversion (January 2026)

An interesting reversal of the model inversion threat: DFSU (Data-Free Selective Unlearning) repurposes model inversion as a *defensive* mechanism. The approach trains a sequence-to-sequence transformer to reconstruct memorized PII from the target model's output logits, then uses Privacy-Selective Contrastive Unlearning (PSCU) within a LoRA adapter to selectively erase those memorized tokens. Evaluated on Pythia models (160M--1.4B parameters), DFSU achieved zero exact reconstruction rate across all scales -- matching oracle unlearning performance that has access to the original training data -- while maintaining near-identical utility (WikiText perplexity increased only from 8.69 to 8.83 on Pythia-410M). Entity-hit rates dropped from 28.78% to 0.13%. The practical significance is that organizations can remediate memorized PII without access to the original training corpus, addressing a real deployment constraint. The primary limitation is the requirement for white-box access to model logits.

### TTLoRA-DP: Parameter-Efficient DP Fine-Tuning (2026)

TTLoRA-DP extends differentially private training to Tensor Train Low-Rank Adaptation, a parameter-efficient fine-tuning method that uses 7.6x fewer parameters than standard LoRA (65.6K vs 497.7K) while achieving better privacy-utility tradeoffs. On the Enron dataset at a strict privacy budget of epsilon=0.5, TTLoRA achieved perplexity of 27.52 versus LoRA's 29.29. More notably, under membership inference attacks, TTLoRA remained nearly stable across privacy budgets (51.36--52.04% attack AUC) while LoRA vulnerability increased substantially (52.49--58.43%). The key insight is that structural constraints in the adapter architecture itself -- the compositional factorization of tensor train cores -- suppress membership signals that loss-based attacks exploit, offering privacy benefits beyond what the noise mechanism alone provides.

### VERIDP: Verifiable Differentially Private Training (March 2026)

VERIDP introduces cryptographic verification for DP-SGD training, addressing a trust gap in privacy-preserving ML: existing frameworks assume semi-honest participants, which breaks down in adversarial or federated environments. Using zero-knowledge proofs with polynomial commitments, sumcheck proofs, and incrementally verifiable computation, VERIDP generates compact proofs (3--4 KB) that verify correct gradient computation, clipping, averaging, and Gaussian noise generation per training iteration -- without revealing sensitive data or randomness. Verification takes just 2--5 milliseconds per proof. This is directly relevant to auditing requirement 11.4.3: rather than trusting that DP-SGD was correctly applied, verifiers can cryptographically confirm it.

### GeoClip: Geometry-Aware Gradient Clipping (2025)

GeoClip improves upon standard per-sample gradient clipping in DP-SGD by clipping and perturbing gradients in a transformed basis aligned with the gradient distribution's geometry. The transformation is estimated adaptively using only previously released noisy gradients, incurring no additional privacy cost. This matters because standard isotropic clipping in DP-SGD discards directional gradient information that could improve convergence; GeoClip preserves this structure while maintaining the same formal privacy guarantees, offering better model utility at equivalent epsilon budgets.

### Regulatory Pressure: Right to Erasure and Model Inversion (2025--2026)

As of March 2025, the European Data Protection Board launched a coordinated enforcement action focused specifically on the right to erasure, with 30 data protection authorities participating. The regulatory implication for model inversion resistance is increasingly direct: if a model can reproduce training data through inversion, regulators may treat the model itself as a copy of that data subject to deletion obligations. Machine unlearning has emerged as the practical response -- source-free unlearning methods (September 2025) demonstrated certified unlearning without access to original training data, using surrogate datasets and calibrated noise to achieve performance comparable to full retraining at a fraction of the compute cost. This regulatory trajectory makes requirements 11.4.1--11.4.3 not just security controls but potential compliance obligations under GDPR and the EU AI Act.

### KV-Cache Inversion Attacks on LLMs (NDSS 2026)

As of March 2026, a new inference-time inversion surface has been demonstrated: the Key-Value (KV) cache used to accelerate LLM inference stores intermediate attention computations that can be exploited to reconstruct user inputs. Luo et al. (NDSS 2026) designed three attack vectors -- inversion (directly reversing cached key/value matrices using known model weights), collision (iteratively matching candidate inputs against intercepted cache states), and injection (semantic manipulation via cache poisoning). All three achieved practical reconstruction of sensitive user prompts from cached data. The proposed defense, **KV-Cloak**, applies reversible matrix-based obfuscation combined with operator fusion to render cached states unintelligible to attackers while preserving model accuracy with minimal performance overhead. Code is available at github.com/SiO-2/kvcloak. This attack class is distinct from training-time inversion (requirement 11.4.3) because it targets inference infrastructure rather than learned parameters -- organizations deploying shared KV-cache systems (multi-tenant inference, prefix caching) should treat this as a separate threat vector requiring its own controls.

### Data Poisoning as Model Inversion Defense (2024--2025)

Zhou et al. (December 2024, published in IEEE TIFS 2025) introduced a counterintuitive defense paradigm: using data poisoning against the *attacker's* inversion model rather than defending the victim classifier. The Label-Preserving Poisoning Attack (LPA) introduces subtle perturbations to all output vectors while preserving their correct labels, contaminating any dataset an attacker would collect by querying the model. This makes it significantly harder for ML-based inversion models to learn the mapping from outputs back to inputs. The key advantage is that LPA is retraining-free -- it does not require modifying or retraining the deployed classifier, making it practical for protecting large established models where retraining with DP would be prohibitively expensive. The approach outperformed existing defenses while maintaining full classifier utility, offering a complementary layer to rate limiting (requirement 11.4.2) and DP training (requirement 11.4.3).

### Shadow Defense for Gradient Inversion in Federated Learning (2025)

Jiang et al. (Medical Image Analysis, October 2025) proposed a shadow-model-based defense against gradient inversion attacks in federated learning. The approach uses a GAN as a shadow model to simulate adversarial reconstruction, then applies targeted, sample-specific noise injection to the gradient components most vulnerable to inversion -- rather than adding uniform noise across all gradients. On medical imaging datasets (ChestXRay, EyePACS), the defense degraded attack reconstruction quality by 3.73 PSNR on ChestXRay and 2.78 PSNR on EyePACS while maintaining model F1 scores within 1% of undefended baselines. This precision-targeting approach addresses a longstanding limitation of uniform DP noise, which often degrades model accuracy more than necessary by protecting already-safe gradient components equally.

### Gradient Inversion: Practical Feasibility Reassessment (2025--2026)

A systematic evaluation by Valadi et al. (August 2025, revised February 2026) challenges the severity of gradient inversion attacks under realistic conditions. Testing across image classification and object detection tasks on contemporary vision architectures, they found that modern, performance-optimized models consistently resist meaningful visual reconstruction. Many previously reported successes relied on upper-bound settings -- inference-mode operation, architectural simplifications, or batch-size-one assumptions that do not reflect production training pipelines. Under honest-but-curious server assumptions with realistic training configurations, high-fidelity reconstruction did not constitute a critical privacy risk. Separately, a comprehensive IEEE TPAMI survey (Guo et al., March 2025) categorized gradient inversion attacks into three types -- optimization-based (most practical), generation-based (too many dependencies), and analytics-based (easily detectable) -- and proposed a three-stage defense pipeline for federated learning frameworks. These findings do not eliminate gradient inversion as a threat, but they contextualize the risk: legacy architectures, small batch sizes, and simplified training setups remain vulnerable, while production configurations with large batches and modern architectures provide inherent resistance.

### Medical Imaging: Retinal Image Inversion Attacks (2026)

A January 2026 study demonstrated the first gradient inversion attack framework specifically targeting retinal age prediction models in federated learning. Using public datasets to train the attack model, the researchers achieved identification of 92% of participants from reconstructed retinal images -- a stark result for healthcare settings where patient re-identification constitutes a serious privacy violation. Critically, moderate differential privacy (at standard epsilon budgets) was insufficient to prevent identifiable reconstructions, suggesting that medical imaging federated learning requires either stricter DP budgets or complementary defenses. Related work on sensitivity-aware differential privacy (2025) proposed adaptive noise calibration that applies stronger protection to high-sensitivity image regions while reducing noise on low-sensitivity areas, achieving 13.5% average performance improvement over uniform DP methods on real-world medical imaging datasets.

---

## Related Standards & References

- [MITRE ATLAS AML.T0024.001 -- Invert ML Model](https://atlas.mitre.org/techniques/AML.T0024.001) -- Attack technique description and known cases
- [NIST AI 100-2e2023 -- Privacy Attacks](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Model inversion in the NIST adversarial ML taxonomy
- [Fredrikson et al., "Model Inversion Attacks that Exploit Confidence Information" (2015)](https://doi.org/10.1145/2810103.2813677) -- Foundational model inversion paper
- [Zhang et al., "The Secret Revealer: Generative Model-Inversion Attacks Against Deep Neural Networks" (2020)](https://arxiv.org/abs/1911.07135) -- GAN-based model inversion producing high-fidelity reconstructions
- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [Deep Learning Model Inversion Attacks and Defenses: A Comprehensive Survey (January 2025)](https://arxiv.org/abs/2501.18934) -- Systematic taxonomy of MI attacks and defenses with 16 methods
- [MIBench: Comprehensive Benchmark for Model Inversion (2025)](https://openreview.net/forum?id=QWjpjisCjs) -- Standardized evaluation benchmark for MI attack and defense methods
- [Model Inversion Attacks: A Survey of Approaches and Countermeasures (November 2024)](https://arxiv.org/abs/2411.10023) -- Attack survey with comprehensive countermeasure catalog and GitHub repository
- [Model Inversion Attacks on Llama 3: Extracting PII from LLMs (2025)](https://arxiv.org/abs/2507.04478) -- PII extraction via crafted prompts on Llama 3.2
- [Model Inversion Attacks on Vision-Language Models (2025)](https://arxiv.org/html/2508.04097v1) -- Four novel MI attack strategies against VLMs with 75%+ accuracy
- [VaultGemma: Differentially Private LLM (September 2025)](https://research.google/blog/vaultgemma-the-worlds-most-capable-differentially-private-llm/) -- Google's 1B-parameter DP-trained open model
- [Opacus: PyTorch Differential Privacy Library](https://opacus.ai/) -- Meta's DP-SGD training library with ghost clipping support
- [FedGuard-CI: Federated Defense Architecture with MIRE (January 2026)](https://jastt.org/index.php/jasttpath/article/view/364) -- Dual-stage DP with model inversion risk estimation
- [Defending Against Deep Learning Attacks with Differential Privacy: A Survey (2025)](https://link.springer.com/article/10.1007/s10462-025-11350-3) -- Comprehensive DP defense survey covering 2020-2025 literature
- [DFSU: Data-Free Privacy-Preserving for LLMs via Model Inversion and Selective Unlearning (January 2026)](https://arxiv.org/abs/2601.15595) -- Repurposing model inversion for defensive PII removal without training data access
- [TTLoRA-DP: Privacy-Enhanced PEFT via Tensor Train Decomposition (2026)](https://arxiv.org/abs/2601.10045) -- Parameter-efficient DP fine-tuning with 7.6x fewer parameters than LoRA
- [VERIDP: Verifiable Differentially Private Training (March 2026)](https://eprint.iacr.org/2026/542) -- Cryptographic verification of DP-SGD correctness using zero-knowledge proofs
- [GeoClip: Geometry-Aware Clipping for Differentially Private SGD (2025)](https://arxiv.org/abs/2506.06549) -- Geometry-aware gradient clipping preserving directional gradient information under DP
- [EDPB CEF 2025: Coordinated Enforcement on Right to Erasure (March 2025)](https://www.edpb.europa.eu/news/news/2025/cef-2025-launch-coordinated-enforcement-right-erasure_en) -- 30 DPAs coordinating enforcement of deletion obligations relevant to model inversion
- [Shadow in the Cache: KV-Cache Privacy Risks in LLM Inference (NDSS 2026)](https://arxiv.org/abs/2508.09442) -- KV-cache inversion, collision, and injection attacks with KV-Cloak defense
- [Defending Against Model Inversion via Data Poisoning (IEEE TIFS 2025)](https://arxiv.org/abs/2412.07575) -- Retraining-free LPA defense that poisons attacker's inversion model
- [Shadow Defense Against Gradient Inversion in Federated Learning (Medical Image Analysis, 2025)](https://arxiv.org/abs/2506.15711) -- Targeted noise injection using shadow model interpretability
- [Practical Feasibility of Gradient Inversion Attacks in Federated Learning (2025)](https://arxiv.org/abs/2508.19819) -- Modern architectures resist meaningful reconstruction under realistic conditions
- [Exploring Vulnerabilities of Federated Learning: Gradient Inversion Attacks (IEEE TPAMI, 2025)](https://arxiv.org/abs/2503.11514) -- Three-category GIA taxonomy with three-stage defense pipeline
- [Gradient Inversion Attack on Retinal Image Federated Learning (Medical Image Analysis, 2026)](https://www.sciencedirect.com/science/article/pii/S1361841525003536) -- 92% participant identification from retinal image reconstruction
- [Sensitivity-Aware Differential Privacy for Federated Medical Imaging (2025)](https://www.mdpi.com/1424-8220/25/9/2847) -- Adaptive DP noise calibration with 13.5% performance improvement over uniform DP

---

## Open Research Questions

- LLM inversion attacks have been demonstrated (Llama 3.2 PII extraction, split-learning attacks), but how do attack success rates compare across model families and scales? Early evidence suggests vulnerability grows with scale.
- Is gradient clipping without noise addition a meaningful defense, or does it merely increase attack cost without fundamentally limiting leakage?
- How should model inversion risk be assessed for models that process sensitive data only at inference time (e.g., RAG over medical records) rather than training time?
- Can model inversion attacks be reliably detected through query-pattern analysis, or are they indistinguishable from legitimate exploratory queries? FedGuard-CI's MIRE offers one quantitative approach, but its applicability beyond federated settings is unproven.
- What output generalization granularity provides a useful privacy-utility trade-off for different domains (healthcare, finance, HR)?
- Are multilingual models fundamentally more vulnerable to inversion than monolingual models, and should multilingual deployments require stricter defenses?
- Can embedding-level protections like EGuard substitute for full DP-SGD in scenarios where training-time DP is infeasible?
- How should MIBench-style standardized benchmarks be incorporated into verification procedures for requirements 11.4.1-11.4.3?
- VaultGemma shows DP is viable at 1B parameters -- can the approach scale to 7B+ models without prohibitive compute costs, and how do Poisson sampling techniques generalize beyond the Gemma architecture?
- Model inversion attacks on VLMs achieved 75%+ accuracy with no proposed defenses. What multimodal-specific countermeasures are needed beyond text-only DP approaches?
- How effective are stand-in model distillation approaches at preventing inversion compared to direct DP training, and can the fidelity-privacy trade-off be quantified systematically?
- DFSU demonstrated that model inversion can be repurposed defensively for PII removal -- can this approach generalize beyond text to image and multimodal models where inversion attacks are also effective?
- TTLoRA-DP shows adapter architecture structure alone can suppress membership signals. What other structural constraints beyond tensor train decomposition might offer similar privacy benefits?
- VERIDP provides cryptographic verification of DP-SGD, but at what scale does per-iteration proof generation become impractical for production training runs with millions of iterations?
- As GDPR enforcement increasingly treats invertible models as data copies, how should organizations quantify inversion risk to determine whether retraining or unlearning is required for compliance?
- KV-cache inversion (NDSS 2026) opens an inference-time attack surface independent of training-time DP. Should KV-cache obfuscation (e.g., KV-Cloak) become a standard requirement for multi-tenant LLM deployments, and how does it interact with prefix caching performance optimizations?
- Data poisoning defenses like LPA shift the attack surface from the victim model to the attacker's inversion model. How robust are these defenses against adaptive attackers who anticipate output perturbation, and do they compose well with DP training?
- The retinal imaging study showed 92% participant identification despite moderate DP. For high-sensitivity medical imaging, what epsilon thresholds are needed to prevent re-identification, and is sensitivity-aware DP (non-uniform noise) sufficient as an alternative to stricter uniform budgets?
- Gradient inversion feasibility varies dramatically between legacy and modern architectures. Should verification approaches (requirement 11.4.3) incorporate architecture-specific risk assessment rather than applying uniform DP requirements regardless of inherent model resistance?

---
