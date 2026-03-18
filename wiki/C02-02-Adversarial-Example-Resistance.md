# C2.2 Adversarial-Example Resistance

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation.md)
> **Last Researched:** 2026-03-18

## Purpose

AI models are vulnerable to subtle input perturbations that humans cannot perceive but cause models to misclassify, misinterpret, or behave unexpectedly. For LLMs, this includes Unicode tricks, homoglyph substitutions, invisible characters, encoding manipulations, and gradient-optimized adversarial suffixes (GCG attacks). For vision and audio models, adversarial perturbations cause misclassification with minimal visible/audible changes. As of 2026, adversarial attacks routinely achieve 90-99% ASR on open-weight models and 80-94% on proprietary models. Multi-signal detection (perplexity + length + attention patterns + semantic analysis) is the current recommended approach — no single defense layer is sufficient.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.2.1** | **Verify that** basic input normalization steps (Unicode NFC, homoglyph mapping, whitespace trimming, removal of control and invisible Unicode characters) are run before tokenization or embedding and before parsing into tool or MCP arguments. | 1 | D | Unicode-based filter evasion; homoglyph attacks (Cyrillic "a" vs. Latin "a"); invisible character injection (zero-width spaces U+200B, zero-width joiners U+200D); control character injection; Trojan Source-style bidirectional text attacks (Boucher et al., 2021). | 1. Inspect input preprocessing for Unicode NFC normalization (`unicodedata.normalize('NFC', text)` or ICU equivalent). 2. Confirm homoglyph mapping against Unicode confusables.txt. 3. Test with zero-width spaces, zero-width joiners, RTL overrides (U+202E), Unicode tag characters (U+E0001-U+E007F). 4. Verify normalization runs before pattern matching or tokenization. 5. Test MCP argument parsing path separately. | Unicode NFC normalization has mature library support. Homoglyph mapping is more complex — the Unicode confusables list has thousands of entries. StruQ converts user input to structured formats with delimiter filtering to neutralize encoding-based injection. Signed-Prompt encrypts allowed commands using rare character sequences. Normalization before tokenization is critical because tokenizers split confusable characters differently. |
| **2.2.2** | **Verify that** suspected adversarial inputs are quarantined, and logged with payload snippets and trace metadata (source, tool or MCP server, agent ID, session). | 1 | V | Undetected adversarial probing; inability to perform incident response; loss of forensic evidence for attack pattern analysis. T-GCG (Sept 2025) showed coding-generation prompts have significantly higher vulnerability than safety benchmarks, making logging critical for discovering attack patterns in unexpected surfaces. | 1. Review logging configuration for adversarial detection events. 2. Verify log entries include: redacted payload snippet, detection method, confidence score, source IP/user, tool/MCP server, agent ID, session ID. 3. Confirm quarantined inputs are stored separately from main processing path. 4. Test by submitting known adversarial inputs (GCG suffixes, LARGO-generated prompts) and checking log output. 5. Verify log integrity protection (append-only, cryptographic signatures). | "Quarantine" needs operational definition — storage of adversarial payloads must avoid secondary injection risks (log injection). Payload snippets should be redacted per C13.1.4. SIEM integration (C13.2.2) enables correlation of adversarial probing across sessions. Evaluation matters: prefix-based ASR heuristics overestimate attack success by up to 30% vs. GPT-4o semantic judgment. |
| **2.2.3** | **Verify that** statistical anomaly detection flags inputs with unusually high edit distance to language norms or abnormal embedding distances and that flagged inputs are gated before concatenation into prompts or execution of actions. | 2 | D/V | Adversarial perturbation attacks producing syntactically unusual text; gibberish injection; GCG-style adversarial suffix attacks (Zou et al., 2023); token-level gradient attacks. T-GCG (2025) demonstrated GCG attacks succeeding against 20B-parameter models. | 1. Confirm anomaly detection component in input pipeline. 2. Review the detection method (perplexity scoring, embedding distance, character n-gram frequency analysis, windowed perplexity). 3. Test with known adversarial suffixes (GCG-generated, T-GCG outputs). 4. Test with LARGO-generated natural-sounding adversarial inputs — these bypass perplexity-based detection. 5. Verify flagged inputs are blocked or routed to human review. | Perplexity-based detection is effective against GCG-style gibberish suffixes but is bypassed by LARGO and PAPILLON attacks that generate low-perplexity adversarial prompts. Best practice as of 2025: combine perplexity + token sequence length + windowed perplexity + semantic analysis (multi-signal). AUROC-scored detection. False positive rates remain high for multilingual inputs, code snippets, and technical jargon. |
| **2.2.4** | **Verify that** the inference pipeline supports adversarial-training-hardened model variants or defense layers (e.g., randomization, defensive distillation, alignment checks) for high-risk endpoints. | 2 | D | Model-level vulnerability to adversarial inputs; transferable adversarial examples; attacks bypassing input-layer defenses. RLHF/safety alignment alone is insufficient — multiple 2025 papers confirm it doesn't prevent sophisticated semantic attacks. | 1. Identify high-risk endpoints (financial, safety, access control). 2. Review hardened model deployments (adversarially trained, SmoothLLM-style randomization, LATPC latent-space training). 3. Check for defense layers: input randomization, defensive distillation, ensemble verification, PromptGuard (4-layer modular defense). 4. Review adversarial evaluation results using JailbreakBench or General Analysis leaderboard. | **LATPC (2025)**: Identifies safety-critical latent-space dimensions for attack-agnostic defense. **MIXAT (2025)**: Combines continuous perturbation + discrete adversarial training. **APL (ACL 2025)**: Adversarial Preference Learning with dynamically evolving examples. **PromptGuard framework** (Nature, 2025): 67% injection reduction, F1=0.91, <8% latency increase, no retraining. SmoothLLM remains baseline (reduces GCG ASR to <1%). |
| **2.2.5** | **Verify that** encoding and representation smuggling in both inputs and outputs (e.g., invisible Unicode/control characters, homoglyph swaps, or mixed-direction text) are detected and mitigated. Approved mitigations include canonicalization, strict schema validation, policy-based rejection, or explicit marking. | 3 | D/V | Encoding smuggling; bidirectional text attacks (Trojan Source); output-side smuggling where model responses contain hidden instructions for downstream consumers; homoglyph-based phishing in outputs; invisible text injection in agent chains. | 1. Test both input and output paths with: invisible Unicode characters, homoglyph sequences, mixed RTL/LTR text, Unicode tag characters (U+E0001-U+E007F), variation selectors. 2. Verify outputs are scanned for encoding attacks (critical for agent chains). 3. Confirm approved mitigation applied: canonicalization, schema validation, rejection, or explicit marking. 4. For agent-to-agent communication, verify both sides apply encoding controls. | This requirement covers both input and output — unusual for C2. Output-side coverage is critical because adversarial content in model outputs attacks downstream systems in agent chains. Level 3 reflects the complexity of comprehensive encoding smuggling defense. Unicode tag characters are invisible in most renderers. Chain of Attack (CVPR 2025) demonstrated compounding effectiveness when multiple encoding techniques are combined in sequence. |

---

## Recent Defensive Advances (2025-2026)

### Defense Tools and Frameworks

| Tool / Technique | Type | Key Finding | Source |
|------------------|------|-------------|--------|
| **LATPC** (2025) | Latent-space adversarial training | Identifies safety-critical dimensions for attack-agnostic defense via refusal features | [Expert Systems & Applications](https://www.sciencedirect.com/science/article/abs/pii/S0957417425027186) |
| **MIXAT** (2025) | Combined continuous + discrete adversarial training | Better robustness than either perturbation or discrete training alone | [arXiv:2505.16947](https://arxiv.org/pdf/2505.16947) |
| **APL** (ACL 2025) | Adversarial Preference Learning | Progressively improves alignment from dynamically evolving adversarial examples | [ACL 2025 Findings](https://aclanthology.org/2025.findings-acl.1126.pdf) |
| **PromptGuard** (2025) | 4-layer modular framework | 67% injection reduction, F1=0.91, <8% latency, no retraining needed | [Nature Scientific Reports](https://www.nature.com/articles/s41598-025-31086-y) |
| **SmoothLLM** (2023, still baseline) | Input randomization | Reduces GCG ASR to <1% via random perturbation + aggregation | [arXiv:2310.03684](https://arxiv.org/abs/2310.03684) |
| **StruQ** | Structured query defense | Converts input to structured formats with delimiter filtering | Referenced in OWASP Cheat Sheet |

### Adversarial Attack Evolution

| Attack | Year | Capability | Implication for Defense |
|--------|------|-----------|----------------------|
| **T-GCG** | Sept 2025 | Annealing-augmented GCG; succeeds against 20B models; coding tasks more vulnerable | Perplexity defense works; coding endpoints need extra protection |
| **LARGO** | 2025 | Generates fluent, low-perplexity adversarial prompts via latent-space optimization | Perplexity-based detection alone is insufficient |
| **PAPILLON** | 2025 | Coherent adversarial jailbreaks bypassing perplexity filters | Must combine perplexity with semantic analysis |
| **Chain of Attack** | CVPR 2025 | Multimodal adversarial transferability via step-by-step semantic updates | Vision-language models need specific defenses |
| **Universal EGD** | Aug 2025 | Theoretical convergence proof; higher success + faster than prior gradient attacks | Formal verification of defenses becomes more important |
| **REINFORCE attacks** | ICML 2025 | RL-based optimization with adaptive/distributional/semantic objectives | Defenses must handle adaptive attacks, not just static patterns |

---

## Robustness Benchmarks & Leaderboards

| Benchmark | What It Measures | Key Results |
|-----------|-----------------|-------------|
| [General Analysis Leaderboard](https://www.generalanalysis.com/benchmarks) | 30+ LLMs against HarmBench + AdvBench using Zero-shot, TAP, Crescendo attacks | Claude 3.5 Sonnet v2: 4.39% ASR (best); Gemini 2.5 Pro: 16.08%; Claude 4.0 Sonnet: 11.92% |
| [JailbreakBench](https://jailbreakbench.github.io/) | Standardized, evolving adversarial prompts for reproducible evaluation | Addresses fragmentation in evaluation methodology |
| [CLEAR-Bias](https://link.springer.com/article/10.1007/s10994-025-06862-6) | LLM robustness to adversarial bias elicitation | Uses LLM-as-a-judge evaluation |

**Evaluation insight:** Prefix-based ASR heuristics overestimate attack success by up to 30 percentage points vs. GPT-4o semantic judgment. Use semantic evaluation for accurate measurement.

---

## Multimodal Adversarial Threats

As of 2026, adversarial attacks extend across all modalities:

- **Vision-language**: Chain of Attack (CVPR 2025) — step-by-step semantic updates for transferable adversarial examples; multimodal feature heterogeneity attacks achieving 16% improvement on MiniGPT4/LLaVA
- **Speech-language**: Adversarial jailbreak threats via audio modality (Interspeech 2025)
- **Physical-environment**: CHAI (Jan 2026, UC Santa Cruz) — physical prompt injection targeting embodied AI
- **Cross-modal compounding**: Combining multiple techniques in sequence dramatically increases attack effectiveness

---

## Related Standards & References

- [NIST AI 100-2e2025: Adversarial Machine Learning](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf) — 2025 update with predictive vs. generative AI distinction
- [MITRE ATLAS AML.T0043: Adversarial ML Attack Techniques](https://atlas.mitre.org/techniques/AML.T0043) — updated through 2026 with agentic AI threats
- [MITRE ATLAS Mapping (Promptfoo)](https://www.promptfoo.dev/docs/red-team/mitre-atlas/)
- [GCG Attack: Universal Adversarial Attacks on Aligned LLMs (Zou et al., 2023)](https://arxiv.org/abs/2307.15043)
- [T-GCG: Resurgence of GCG Attacks (Tan et al., 2025)](https://arxiv.org/html/2509.00391v1)
- [SmoothLLM (Robey et al., 2023)](https://arxiv.org/abs/2310.03684)
- [Trojan Source (Boucher et al., 2021)](https://trojansource.codes/)
- [Unicode Confusables (Unicode Consortium)](https://unicode.org/cldr/utility/confusables.jsp)
- [Attack and Defense Techniques in LLMs: Survey (Liao et al., 2025)](https://arxiv.org/html/2505.00976v1)

---

## Open Research Questions

- Can perplexity-based detection be augmented with attention pattern analysis to catch LARGO/PAPILLON-style low-perplexity attacks?
- How effective is adversarial training at LLM scale — will runtime defense layers (randomization, ensembles) remain the primary practical approach?
- What false positive rates are acceptable for encoding smuggling detection in production multilingual systems?
- How should adversarial detection thresholds be calibrated across languages, domains, and modalities?
- Are coding/reasoning tasks fundamentally more vulnerable to adversarial attacks than safety-category prompts (per T-GCG findings)?
- Can formal robustness verification (certified bounds) scale to transformer architectures with billions of parameters?
- How should evaluation methodology be standardized — is GPT-4o semantic judgment the right gold standard?

---

[C02 Index](C02-User-Input-Validation.md) | [README](README.md)
