# C2.2 Pre-Tokenization Input Normalization

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation.md)
> **Last Researched:** 2026-05-02

## Purpose

AI models are vulnerable to subtle input perturbations that humans cannot perceive but cause models to misclassify, misinterpret, or behave unexpectedly. For LLMs, this includes Unicode tricks, homoglyph substitutions, invisible characters, encoding manipulations, and gradient-optimized adversarial suffixes (GCG attacks). For vision and audio models, adversarial perturbations cause misclassification with minimal visible/audible changes. As of 2026, adversarial attacks routinely achieve 90–99% ASR on open-weight models and 80–94% on proprietary models. Multi-signal detection (perplexity + length + attention patterns + semantic analysis) is the current recommended approach — no single defense layer is sufficient.

A critical development: reasoning models (o1, o3, DeepSeek-R1) are **not** uniformly safer. The "Weakest Link" study (June 2025) found multi-step attacks like Tree-of-Attacks succeed at 63% on reasoning models vs. 31% on standard models, because chain-of-thought itself creates exploitable attack surface. This was dramatically confirmed in 2026: Hagendorff et al. (Nature Communications, 2026) demonstrated that large reasoning models (DeepSeek-R1, Gemini 2.5 Flash, Grok 3 Mini, Qwen3 235B) act as **autonomous jailbreak agents**, achieving 97.14% success across all model combinations with no human supervision — a phenomenon they term "alignment regression," where more capable reasoning makes models better at subverting alignment in other models.

Automated attack tooling is also accelerating. JBFuzz (March 2025) applies software fuzzing techniques to jailbreaking, achieving 99% average ASR across GPT-4o, Gemini 2.0, and DeepSeek-V3 in roughly 60 seconds per jailbreak. Mastermind (January 2026) uses knowledge-driven multi-turn fuzzing with an evolutionary optimizer, reaching 87% average ASR including 67% on Claude 3.7 Sonnet and 60% on GPT-5. The UK AISI/Gray Swan challenge ran 1.8 million attacks across 22 models — every model broke. Supply-chain adversarial attacks via quantization are also maturing — the "Mind the Gap" paper (ICML 2025) showed models that appear 82.6% safe in full precision drop to 3% safety after GGUF quantization. Attacks are also moving into the latent space: the Latent Fusion Jailbreak (LFJ, revised January 2026) blends hidden states from harmful and benign queries to produce adversarial representations invisible to text-level filters, achieving 94.01% average ASR across five model families.

As of May 2026, invisible-instruction attacks are no longer just a rendering problem. Reverse CAPTCHA (February 2026) evaluated 8,308 model outputs and found that tool use substantially increases compliance with invisible Unicode instructions, while Imperceptible Jailbreaking (October 2025) showed that variation-selector suffixes can leave the prompt visually unchanged while altering tokenization enough to generalize to prompt-injection attacks. Normalization controls therefore need to cover pre-model input, retrieved content, tool responses, and model outputs before any downstream parser or action executor sees the text.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **2.2.1** | **Verify that** input normalization (Unicode NFC canonicalization, homoglyph mapping, removal of control and invisible Unicode characters, and bidirectional text neutralization) is applied before tokenization or embedding, and that inputs which still contain suspicious encoding artifacts after normalization are rejected or flagged for review. | 1 | Unicode-based filter evasion; homoglyph attacks (Cyrillic "a" vs. Latin "a"); invisible character injection (zero-width spaces U+200B, zero-width joiners U+200D); control character injection; Trojan Source-style bidirectional text attacks (Boucher et al., 2021). Emoji smuggling via Unicode variation selectors achieved **100% bypass rate** across Azure Prompt Shield, Meta Prompt Guard, NeMo Guard, and ProtectAI (disclosed April 2025). ASCII smuggling via Unicode tag characters (U+E0000–U+E007F) exfiltrated emails and MFA codes from Microsoft 365 Copilot (January–August 2024, patched July 2024). FireTail (September 2025) found Gemini, Grok, and DeepSeek remain vulnerable to tag-based smuggling while ChatGPT and Claude sanitize effectively. | 1. Inspect input preprocessing for Unicode NFC normalization (`unicodedata.normalize('NFC', text)` or ICU equivalent). 2. Confirm homoglyph mapping against Unicode confusables.txt. 3. Test with zero-width spaces, zero-width joiners, RTL overrides (U+202E), Unicode tag characters (U+E0001–U+E007F), emoji variation selectors, and "Sneaky Bits" encoding (U+2062/U+2064 binary encoding). 4. Verify normalization runs before pattern matching or tokenization. 5. Test MCP argument parsing path separately. 6. Use CAPEC-71 (Unicode encoding bypass) and CAPEC-80 (UTF-8 encoding bypass) as test case references. 7. Implement tag character stripping: filter codepoints in range 0xE0000–0xE007F, and in UTF-16 stacks test repeated or orphaned surrogate pairs so a one-pass sanitizer cannot re-form hidden tag characters. | Unicode NFC normalization has mature library support. Homoglyph mapping is more complex — the Unicode confusables list has thousands of entries. The emoji smuggling research (arXiv:2504.11168) showed 100% bypass on multiple production guardrails, making this a critical gap. AWS guidance from September 2025 shows why tag-block stripping must handle surrogate-pair edge cases recursively in Java-like runtimes. "Sneaky Bits" (2025) introduced two additional invisible encoding schemes (U+2062/U+2064 binary, variant selectors VS1–VS256), expanding the attack surface beyond tag characters. No dedicated NIST or OWASP standard specifically addresses Unicode normalization for AI — closest guidance is NIST SP 800-63-4 (NFC before hashing), CAPEC-71/80, and vendor recommendations from AWS and Cisco. |
| **2.2.2** | **Verify that** inputs identified as adversarial by any detection mechanism are blocked from inclusion in prompts or execution of actions. | 1 | Detected prompt injection, jailbreak, smuggling, or adversarial suffix payloads still reaching the model context; time-of-check/time-of-use gaps between classifier, prompt builder, RAG retriever, and tool executor; agent actions executing after a guardrail raises only an alert. OWASP LLM01:2025 explicitly notes that prompt injections can be imperceptible to humans as long as the model parses them. Reverse CAPTCHA (February 2026) showed that enabling tool use materially increases compliance with invisible Unicode instructions. | 1. Submit known adversarial inputs (GCG/T-GCG suffixes, LARGO-generated prompts, Unicode tag payloads, variation-selector smuggling, Base64/hex instructions) and confirm the prompt builder receives a block decision rather than sanitized-but-forwarded text. 2. Verify enforcement at each ingestion point: direct user prompts, retrieved documents, MCP/tool responses, file uploads, and agent-to-agent messages. 3. Confirm blocked inputs cannot trigger tool calls, memory writes, embeddings, workflow transitions, or downstream parsers. 4. Review logs for redacted payload snippet, detection method, confidence score, source IP/user, tool/MCP server, agent ID, session ID, and final enforcement action. 5. Test network or gateway controls such as Microsoft Entra AI Gateway Prompt Injection Protection and in-app controls with the same corpus to catch policy drift. | Logging alone does not satisfy this requirement — the core evidence is that detected adversarial content is never inserted into the model prompt or action path. Quarantine needs an operational definition and must avoid secondary injection risks in logs. Microsoft Entra's April 2026 Prompt Injection Protection is useful for enterprise network enforcement, but its documented limits are important: text prompts only, JSON-based apps, and prompt content up to 64,000 characters. SIEM integration (C13.2.2) still matters for correlation, but auditors should fail implementations that alert without blocking. |
| **2.2.3** | **Verify that** encoding and representation smuggling in both inputs and outputs (e.g., invisible Unicode/control characters, homoglyph swaps, or mixed-direction text) are detected and mitigated. Approved mitigations include canonicalization, strict schema validation, policy-based rejection, or explicit marking. | 3 | Encoding smuggling; bidirectional text attacks (Trojan Source); output-side smuggling where model responses contain hidden instructions for downstream consumers; homoglyph-based phishing in outputs; invisible text injection in agent chains. M365 Copilot ASCII smuggling (2024) demonstrated real-world data exfiltration via invisible Unicode tags. ChatGPT-4o hex encoding jailbreak (October 2024) generated working exploit code for CVE-2024-41110. Imperceptible Jailbreaking (October 2025) used variation-selector suffixes that leave prompts visually unchanged while altering tokenization, and Reverse CAPTCHA (February 2026) demonstrated model compliance with zero-width binary and Unicode tag payloads in otherwise normal-looking text. | 1. Test both input and output paths with: invisible Unicode characters, homoglyph sequences, mixed RTL/LTR text, Unicode tag characters (U+E0001–U+E007F), variation selectors, emoji variation selectors, hex/Base64 encoded instructions, "Sneaky Bits" U+2062/U+2064 binary encoding. 2. Verify outputs are scanned for encoding attacks before rendering, storage, tool calls, browser/Markdown handling, or agent handoff. 3. Confirm approved mitigation applied: canonicalization, schema validation, rejection, or explicit marking. 4. For agent-to-agent communication, verify both sides apply encoding controls. 5. Include garak `goodside.Tag`, garak `badchars.BadCharacters`, Protect AI LLM Guard `InvisibleText`, and an explicit Reverse CAPTCHA-style test set in regression testing. | This requirement covers both input and output — unusual for C2. Output-side coverage is critical because adversarial content in model outputs attacks downstream systems in agent chains. Level 3 reflects the complexity of comprehensive encoding smuggling defense. Unicode tag characters are invisible in most renderers but decoded by LLM tokenizers. The hex encoding jailbreak against GPT-4o shows that multi-step encoding (content → hex → LLM decodes → executes) evades filters that check content at each phase independently. Token smuggling exploits the discrepancy between how text-matching filters read strings vs. how LLM tokenizers process them. Production gaps remain: LLM Guard can detect common invisible Unicode categories, garak can exercise known probes, and managed gateways can block selected policies, but no tool provides complete semantic assurance across every tokenizer, renderer, language runtime, and downstream action path. |

---

## Recent Defensive Advances (2025-2026)

### Defense Tools and Frameworks

| Tool / Technique | Type | Key Finding | Source |
|------------------|------|-------------|--------|
| **ShorT** (Feb 2025) | Efficient adversarial training | Training on √M-length suffixes defends against M-length attacks; 90%+ effective at 4x length | [arXiv:2502.04204](https://arxiv.org/abs/2502.04204) |
| **SafeProbing** (Jan 2026) | Decoding-time safety probing | Surfaces latent safety signals during generation — effective against low-perplexity attacks | [arXiv:2601.10543](https://arxiv.org/abs/2601.10543) |
| **AISA** (Feb 2026) | Logits-level decoding steering | Risk-proportional decoding without parameter changes; tested on 13 datasets, 12 LLMs, 14 baselines | [arXiv:2602.13547](https://arxiv.org/abs/2602.13547) |
| **SAID** (Oct 2025) | Prefix-based safety activation | Optimal Safety Probe Prefix probes distilled intents; superior to 6 SOTA jailbreak attacks | [arXiv:2510.20129](https://arxiv.org/abs/2510.20129) |
| **LATPC** (2025) | Latent-space adversarial training | Identifies safety-critical dimensions for attack-agnostic defense via refusal features | [Expert Systems & Applications](https://www.sciencedirect.com/science/article/abs/pii/S0957417425027186) |
| **MIXAT** (2025) | Combined continuous + discrete training | Better robustness than either perturbation or discrete training alone | [arXiv:2505.16947](https://arxiv.org/pdf/2505.16947) |
| **APL** (ACL 2025) | Adversarial Preference Learning | Progressively improves alignment from dynamically evolving adversarial examples | [ACL 2025 Findings](https://aclanthology.org/2025.findings-acl.1126.pdf) |
| **PromptGuard** (2025) | 4-layer modular framework | 67% injection reduction, F1=0.91, <8% latency, no retraining needed | [Nature Scientific Reports](https://www.nature.com/articles/s41598-025-31086-y) |
| **SmoothLLM** (2023, baseline) | Input randomization | Reduces GCG ASR to <1% via random perturbation + aggregation | [arXiv:2310.03684](https://arxiv.org/abs/2310.03684) |
| **RoMA** (Apr 2025) | Statistical robustness verification | Black-box bounds within 1% of formal methods; minutes vs. hours | [arXiv:2504.17723](https://arxiv.org/abs/2504.17723) |
| **HoneyTrap** (Jan 2026) | Multi-agent deceptive defense | 4-agent honeypot cuts jailbreak success 68.77%; increases attacker cost 149% | [arXiv:2601.04034](https://arxiv.org/abs/2601.04034) |
| **AgentSpec** (ICSE 2026) | Runtime enforcement DSL | First framework for customizable safety constraints on LLM agents at runtime | [ICSE 2026](https://cposkitt.github.io/files/publications/agentspec_llm_enforcement_icse26.pdf) |
| **Pro2Guard** (2025) | Proactive runtime enforcement | DTMC-based prediction of unsafe agent states; intervenes before violations | [arXiv:2508.00500](https://arxiv.org/abs/2508.00500) |
| **ProAct** (Feb 2026) | Proactive spurious-response defense | Feeds fake success signals to iterative jailbreak optimizers; up to 94% ASR reduction; 0% combined | [arXiv:2510.05052](https://arxiv.org/abs/2510.05052) |
| **GuardNet** (Sep 2025) | Graph-attention jailbreak filter | Hierarchical prompt-level + token-level detection via graph neural networks; F1 up to 99.8% | [arXiv:2509.23037](https://arxiv.org/abs/2509.23037) |
| **Latent adversarial training** (Jan 2026) | Latent-space defense | Counters Latent Fusion Jailbreak; reduces LFJ ASR from 94% to 12.45%; benign refusal <5% | [arXiv:2508.10029](https://arxiv.org/abs/2508.10029) |
| **Amazon Bedrock Guardrails denied topics** (Sep 2025) | Managed block/detect policy | AWS documents denied-topic patterns for Unicode tag blocks and UTF-16 surrogates; blocks or detects rather than returning cleaned text | [AWS Security Blog](https://aws.amazon.com/blogs/security/defending-llm-applications-against-unicode-character-smuggling/) |
| **Microsoft Entra AI Gateway Prompt Injection Protection** (Apr 2026) | Network-layer prompt policy | Blocks adversarial prompts before they reach supported or custom JSON-based model endpoints; useful for gateway evidence, but text-only and 64K-character limited | [Microsoft Learn](https://learn.microsoft.com/en-us/entra/global-secure-access/how-to-ai-prompt-injection-protection) |
| **LLM Guard InvisibleText** (2025) | Input scanner | Detects and removes non-printable, control, format, private-use, and unassigned Unicode characters in prompts | [Protect AI docs](https://protectai.github.io/llm-guard/input_scanners/invisible_text/) |

### Red-Teaming and Testing Tools

| Tool | Type | Key Capabilities | Source |
|------|------|-----------------|--------|
| **Intel LLMart** | OSS adversarial toolkit | GCG optimization, VLM attacks, dLLM attacks, multi-GPU parallelization, HarmBench/AdvBench | [GitHub](https://github.com/IntelLabs/LLMart) |
| **PRISM BET** | Automated red-team engine | 100% ASR on 37/41 LLMs; fine-grained robustness metric; hundreds of jailbreak primitives | [GitHub](https://github.com/PRISM-EVAL/BehaviorElicitationTool) |
| **Mindgard** | Commercial platform | Continuous multi-modal testing (text, image, audio); CI/CD integration; MITRE ATLAS mapping | [mindgard.ai](https://mindgard.ai/) |
| **HiddenLayer** | Commercial platform | AI Attack Simulation + Runtime Security + Supply Chain Security; 2026 AI Threat Landscape Report | [hiddenlayer.com](https://www.hiddenlayer.com) |
| **JBFuzz** | OSS fuzzing framework | 99% ASR via mutation-based fuzzing; ~60s/7 queries per jailbreak; GPT-4o, Gemini 2.0, DeepSeek-V3 | [arXiv:2503.08990](https://arxiv.org/abs/2503.08990) |
| **Cisco AI Defense** | Enterprise platform | 200+ attack techniques; agentic guardrails; MCP inspection; algorithmic red teaming | [cisco.com](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html) |
| **garak `goodside.Tag`** | OSS probe | Exercises UTF tag page encoding for user-invisible prompt injection in browser/chat workflows | [garak docs](https://reference.garak.ai/en/latest/garak.probes.goodside.html) |
| **garak `badchars.BadCharacters`** | OSS probe | Generates invisible Unicode, homoglyph, bidirectional, swap, deletion, and backspace perturbations | [garak docs](https://reference.garak.ai/en/latest/garak.probes.badchars.html) |

### Adversarial Attack Evolution

| Attack | Year | Capability | Defense Implication |
|--------|------|-----------|---------------------|
| **H-CoT** | Feb 2025 | Hijacks chain-of-thought in reasoning models; drops refusal from 98% to <2% | Safety checks must operate within reasoning chain, not just on final output |
| **TAO-Attack** | ICLR 2026 | Refined GCG with better convergence and cross-model transfer | Perplexity defenses increasingly fragile against optimized suffixes |
| **ArrAttack** | ICLR 2025 | Automated defense-resistant jailbreak generation; ~80% ASR on defended models | Reactive defense patching is a losing game against automated generators |
| **Mind the Gap** | ICML 2025 | Quantization attack: 82.6% safe → 3% safe after GGUF conversion | Must verify model behavior at quantized precision, not just full-precision |
| **Emoji smuggling** | Apr 2025 | 100% bypass of 6 production guardrails via variation selectors | Input normalization must strip emoji variation selectors |
| **T-GCG** | Sept 2025 | Annealing-augmented GCG; coding tasks more vulnerable | Coding endpoints need extra protection |
| **LARGO / PAPILLON** | 2025 | Fluent, low-perplexity adversarial prompts | Perplexity detection alone insufficient; need decoding-time defenses |
| **LoopLLM** | AAAI 2026 | Transferable energy-latency attack; >90% max output length | Repetition detection and output-length throttling critical |
| **MAGIC** | Feb 2026 | Co-evolutionary multi-agent attack/defense framework | Static benchmarks underestimate real adversarial risk |
| **JBFuzz** | Mar 2025 | Fuzzing-based jailbreak; 99% ASR across GPT-4o, Gemini 2.0, DeepSeek-V3 in ~60s | Anomaly detection must handle rapidly mutated adversarial inputs |
| **Mastermind** | Jan 2026 | Knowledge-driven multi-turn attack; 87% avg ASR; 67% on Claude 3.7 Sonnet, 60% on GPT-5 | Evolutionary optimization outpaces static defense rules |
| **Imperceptible Jailbreaking** | Oct 2025 | Variation-selector suffixes keep prompts visually unchanged while altering tokenization; generalizes to prompt injection | Normalizers must strip or mark variation selectors before tokenization, not just after display rendering |
| **Reverse CAPTCHA** | Feb 2026 | Invisible Unicode instruction benchmark; 8,308 outputs showed tool use amplifies compliance and explicit decoding hints can sharply raise success | Test agent/tool-enabled paths separately from plain chat because tool access changes risk |
| **Latent Fusion Jailbreak (LFJ)** | Jan 2026 | Blends hidden states of harmful + benign queries in latent space; 94.01% avg ASR; invisible to text-level filters | Text-level input filtering is insufficient — latent-space defenses needed; latent adversarial training reduces to 12.45% |
| **Autonomous LRM jailbreaking** | 2026 | Reasoning models as autonomous adversaries; 97.14% ASR across all model combos (Nature Comms) | "Alignment regression" — more capable reasoning enables better subversion |

---

## Robustness Benchmarks & Leaderboards

| Benchmark | What It Measures | Key Results |
|-----------|-----------------|-------------|
| [MLCommons AILuminate](https://mlcommons.org/ailuminate/jailbreak/) (v0.5, Oct 2025) | Standardized multi-modal jailbreak resilience | All 39 tested T2T models compromised; avg safety drops 19.81pp under jailbreak; 25.27pp for multimodal |
| [PRISM Eval Leaderboard](https://arxiv.org/abs/2508.06296) (Paris AI Summit 2025) | Fine-grained robustness via elicitation difficulty | 100% ASR on 37/41 models; attack difficulty varies 300-fold |
| [General Analysis Leaderboard](https://www.generalanalysis.com/benchmarks) | 30+ LLMs against HarmBench + AdvBench | Claude 3.5 Sonnet v2: 4.39% ASR (best); Gemini 2.5 Pro: 16.08% |
| [JailbreakBench](https://jailbreakbench.github.io/) | Standardized, evolving adversarial prompts | Addresses fragmentation in evaluation methodology |
| [CLEAR-Bias](https://link.springer.com/article/10.1007/s10994-025-06862-6) | LLM robustness to adversarial bias elicitation | Uses LLM-as-a-judge evaluation |
| [JBDistill](https://arxiv.org/abs/2505.22037) (EMNLP 2025) | Renewable jailbreak safety benchmarking | 81.8% effectiveness across 13 models; auto-renewable with minimal human effort |
| UK AISI/Gray Swan Challenge | Large-scale adversarial stress test | 1.8M attacks across 22 models; every model broke; no frontier system resists determined attacks |

**Evaluation insight:** Prefix-based ASR heuristics overestimate attack success by up to 30 percentage points vs. GPT-4o semantic judgment. Use semantic evaluation for accurate measurement.

---

## Notable Incidents

| Date | Incident | Impact | Source |
|------|----------|--------|--------|
| Jan–Aug 2024 | **M365 Copilot ASCII smuggling** — invisible Unicode tag characters exfiltrated emails, MFA codes, PII via crafted hyperlinks | Real-world data exfiltration; no CVE assigned; patched July 2024 | [Embrace The Red](https://embracethered.com/blog/posts/2024/m365-copilot-prompt-injection-tool-invocation-and-data-exfil-using-ascii-smuggling/) |
| Oct 2024 | **ChatGPT-4o hex encoding jailbreak** — hex-encoded instructions bypassed filters; generated working exploit for CVE-2024-41110 | Working attack code generated from moderation-evading prompt | [0Din/Mozilla](https://0din.ai/blog/chatgpt-4o-guardrail-jailbreak-hex-encoding-for-writing-cve-exploits) |
| Feb 2025 | **nullifAI Hugging Face models** — broken 7z-compressed pickle format evaded Picklescan while delivering reverse shell payload | Scanner bypass on model hosting platform; Picklescan updated | [The Hacker News](https://thehackernews.com/2025/02/malicious-ml-models-found-on-hugging.html) |
| Apr 2025 | **Emoji smuggling (arXiv:2504.11168)** — 100% bypass of Azure Prompt Shield, Meta Prompt Guard, NeMo Guard, ProtectAI via variation selectors | All tested production guardrails defeated | [arXiv:2504.11168](https://arxiv.org/abs/2504.11168) |
| Sep 2025 | **FireTail multi-LLM ASCII smuggling** — Gemini, Grok, DeepSeek process hidden Unicode tags without sanitization; Google declined to fix | 3 of 6 major LLM providers vulnerable to tag-based exfiltration | [FireTail](https://www.firetail.ai/blog/ghosts-in-the-machine-ascii-smuggling-across-various-llms) |
| 2025–2026 | **UK AISI/Gray Swan adversarial challenge** — 1.8 million attacks against 22 frontier models; every model broken | No frontier model resists determined, well-resourced adversarial attacks | [VentureBeat](https://venturebeat.com/security/red-teaming-llms-harsh-truth-ai-security-arms-race) |
| 2026 | **Autonomous LRM jailbreaking** — reasoning models (DeepSeek-R1, Gemini 2.5 Flash, Grok 3 Mini, Qwen3 235B) autonomously jailbreak 9 target models at 97.14% success with no human supervision | Demonstrates "alignment regression" — more capable models become better at breaking other models | [Nature Communications](https://www.nature.com/articles/s41467-026-69010-1) |

---

## Multimodal Adversarial Threats

As of 2026, adversarial attacks extend across all modalities:

- **Vision-language**: Chain of Attack (CVPR 2025) — step-by-step semantic updates for transferable adversarial examples; TAO-Attack (ICLR 2026) evaluates on both text and VLMs
- **Speech-language**: Electronic Music Assassin (2025) — frequency-domain attack achieves **100% ASR on 8 commercial ASR systems** with audio indistinguishable from normal music by 52% of human subjects; GuidedDE (Neural Networks, April 2026) — 90–95% targeted ASR with 67–73% efficiency improvement over prior methods; adversarial speech enhancement attacks (ICASSP 2026) — diffusion-based models are inherently more robust than deterministic predictive models
- **Reasoning models**: H-CoT (February 2025) — hijacks chain-of-thought to subvert safety reasoning; "Weakest Link" (June 2025) — reasoning models 32pp worse on Tree-of-Attacks and 22pp worse on suffix injection than standard models
- **Physical-environment**: CHAI (January 2026, UC Santa Cruz) — physical prompt injection targeting embodied AI
- **Supply chain / quantization**: Mind the Gap (ICML 2025) — models appear safe in full precision but become malicious after GGUF quantization (most widely deployed format via llama.cpp and Ollama)

---

## Implementation Maturity

| Area | Maturity | Notes |
|------|----------|-------|
| Unicode NFC normalization | **High** | Mature library support. But emoji variation selectors and tag characters are commonly missed. |
| Perplexity-based detection | **Medium** | Effective against GCG suffixes; defeated by LARGO/PAPILLON low-perplexity attacks. |
| Decoding-time defenses | **Low–Medium** | SafeProbing, AISA, SAID show promise but are academic. Not in production tooling. |
| Adversarial training (LLM scale) | **Low–Medium** | ShorT reduces cost. But no frontier model ships with adversarial training as a standard feature. |
| Formal/certified robustness | **Low** | Infeasible at transformer scale. RoMA offers statistical alternative. |
| Commercial red-teaming platforms | **Medium-High** | Mindgard, HiddenLayer, Cisco AI Defense provide automated testing. Adoption growing. |
| Encoding smuggling defense | **Low** | 100% bypass of production guardrails via emoji smuggling. No comprehensive standard. |
| Gateway-level prompt blocking | **Medium** | Microsoft Entra and Amazon Bedrock Guardrails provide deployable blocking controls, but documented limits mean they should be regression-tested with the same corpus as in-app scanners. |
| Proactive deceptive defense | **Low–Medium** | HoneyTrap (January 2026) and ProAct (February 2026) offer complementary proactive approaches — honeypot traps and spurious-response deception. Both academic but ProAct's 94% ASR reduction is notable. |
| Latent-space defense | **Low** | Latent adversarial training (January 2026) counters LFJ with 80%+ ASR reduction. No production tooling yet — research demonstrates the approach is viable. |
| Graph-attention filtering | **Low–Medium** | GuardNet (September 2025) achieves F1 up to 99.8% on jailbreak detection via graph neural networks. Academic; no production deployment known. |
| Runtime agent enforcement | **Low–Medium** | AgentSpec (ICSE 2026) and Pro2Guard offer customizable runtime safety constraints. Early adoption stage. |

---

## Cross-Chapter Links

| Related Section | Overlap |
|----------------|---------|
| [C02-01 Prompt Injection Defense](C02-01-Prompt-Injection-Defense.md) | Adversarial suffixes as injection vectors; GCG/T-GCG overlap |
| [C02-03 Content Policy Screening](C02-03-Content-Policy-Screening.md) | Content classifiers as complementary layer |
| [C06-01 Pretrained Model Vetting](../C06-Supply-Chain/C06-01-Pretrained-Model-Vetting.md) | Supply chain attacks via adversarial model weights (nullifAI, quantization attacks) |
| [C07-01 Output Format Enforcement](../C07-Model-Behavior/C07-01-Output-Format-Enforcement.md) | Output-side encoding smuggling defense |
| [C11-02 Adversarial Example Hardening](../C11-Adversarial-Robustness/C11-02-Adversarial-Example-Hardening.md) | Deeper adversarial training and formal robustness |
| [C13-01 Request-Response Logging](../C13-Monitoring-and-Logging/C13-01-Request-Response-Logging.md) | Adversarial event logging and quarantine |

---

## Related Pages

- [C02-03 Content Policy Screening](C02-03-Content-Policy-Screening.md) — pairs normalization with pre-model policy classifiers and replay evidence for blocked adversarial content.
- [C11-08 Agent Security Self-Assessment](../C11-Adversarial-Robustness/C11-08-Agent-Security-Self-Assessment.md) — extends adversarial-input blocking into agent pre-execution review and bypass-resistant control checks.
- [C02-01 Prompt Injection Defense](C02-01-Prompt-Injection-Defense.md) — covers the prompt-injection architecture that normalization supports but cannot replace.
- [C02-04 Multi-Modal Input Validation](C02-04-Multi-Modal-Input-Validation.md) — broadens smuggling and steganography testing across images, audio, video, and VLM workflows.
- [C02 User Input Validation](C02-User-Input-Validation.md) — places Unicode normalization in the wider chapter model for prompt, content, and multimodal input controls.

---

## Related Standards & References

- [NIST AI 100-2e2025: Adversarial Machine Learning](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf) — 2025 update with predictive vs. generative AI distinction
- [MITRE ATLAS AML.T0043: Adversarial ML Attack Techniques](https://atlas.mitre.org/techniques/AML.T0043) — v5.3.0 (January 2026) added MCP compromise case studies; v5.4.0 (February 2026) added agentic techniques including "Publish Poisoned AI Agent Tool" and "Escape to Host"
- [CAPEC-71: Using Unicode Encoding to Bypass Validation Logic](https://capec.mitre.org/data/definitions/71.html)
- [CAPEC-80: Using UTF-8 Encoding to Bypass Validation Logic](https://capec.mitre.org/data/definitions/80.html)
- [GCG Attack: Universal Adversarial Attacks on Aligned LLMs (Zou et al., 2023)](https://arxiv.org/abs/2307.15043)
- [T-GCG: Resurgence of GCG Attacks (Tan et al., 2025)](https://arxiv.org/abs/2509.00391)
- [SmoothLLM (Robey et al., 2023)](https://arxiv.org/abs/2310.03684)
- [Trojan Source (Boucher et al., 2021)](https://trojansource.codes/)
- [Unicode Confusables (Unicode Consortium)](https://unicode.org/cldr/utility/confusables.jsp)
- [AWS — Defending LLM Applications Against Unicode Character Smuggling](https://aws.amazon.com/blogs/security/defending-llm-applications-against-unicode-character-smuggling/)
- [Cisco — Unicode Tag Prompt Injection](https://blogs.cisco.com/ai/understanding-and-mitigating-unicode-tag-prompt-injection)
- [MLCommons AILuminate Jailbreak Benchmark v0.5](https://mlcommons.org/ailuminate/jailbreak/)
- [PRISM Eval Behavior Elicitation Tool](https://arxiv.org/abs/2508.06296)
- [H-CoT: Hijacking Chain-of-Thought in Reasoning Models](https://arxiv.org/abs/2502.12893)
- [Weakest Link in the Chain — Reasoning Model Security (June 2025)](https://arxiv.org/abs/2506.13726)
- [TAO-Attack (ICLR 2026)](https://arxiv.org/abs/2603.03081)
- [Mind the Gap: GGUF Quantization Attack (ICML 2025)](https://arxiv.org/abs/2505.23786)
- [Emoji Smuggling Guardrail Bypass (arXiv:2504.11168)](https://arxiv.org/abs/2504.11168)
- [M365 Copilot ASCII Smuggling (Embrace The Red)](https://embracethered.com/blog/posts/2024/m365-copilot-prompt-injection-tool-invocation-and-data-exfil-using-ascii-smuggling/)
- [Electronic Music Assassin — Physical Audio Adversarial Attack](https://link.springer.com/article/10.1186/s42400-025-00374-5)
- [SafeProbing: Decoding-Time Safety Awareness (January 2026)](https://arxiv.org/abs/2601.10543)
- [ShorT: Short-Length Adversarial Training (February 2025)](https://arxiv.org/abs/2502.04204)
- [RoMA: Statistical Runtime Robustness Verification (April 2025)](https://arxiv.org/abs/2504.17723)
- [MITRE SAFE-AI Framework — Mapping ATLAS Threats to NIST SP 800-53 Controls](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf) — 100 AI-affected controls identified
- [NIST IR 8596 (Draft, December 2025) — Cybersecurity Framework Profile for AI](https://csrc.nist.gov/pubs/ir/8596/iprd) — CSF 2.0 outcomes applied to AI systems
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — notes that prompt injection can be imperceptible to humans when parsed by the model
- [Autonomous LRM Jailbreaking (Hagendorff et al., Nature Communications 2026)](https://www.nature.com/articles/s41467-026-69010-1) — alignment regression in reasoning models
- [JBFuzz: Fuzzing-Based LLM Jailbreaking (March 2025)](https://arxiv.org/abs/2503.08990)
- [Mastermind: Knowledge-Driven Multi-Turn Jailbreaking (January 2026)](https://arxiv.org/abs/2601.05445)
- [HoneyTrap: Multi-Agent Deceptive Defense (January 2026)](https://arxiv.org/abs/2601.04034)
- [AgentSpec: Runtime Enforcement for LLM Agents (ICSE 2026)](https://cposkitt.github.io/files/publications/agentspec_llm_enforcement_icse26.pdf)
- [JBDistill: Renewable Safety Benchmarking (EMNLP 2025)](https://arxiv.org/abs/2505.22037)
- [ProAct: Proactive Defense Against LLM Jailbreak (revised February 2026)](https://arxiv.org/abs/2510.05052) — spurious-response defense reducing ASR up to 94%
- [Latent Fusion Jailbreak: Blending Harmful and Harmless Representations (revised January 2026)](https://arxiv.org/abs/2508.10029) — latent-space attack at 94.01% ASR; introduces latent adversarial training defense
- [GuardNet: Graph-Attention Filtering for Jailbreak Defense (September 2025)](https://arxiv.org/abs/2509.23037) — hierarchical graph neural network detection with F1 up to 99.8%
- [MITRE ATLAS OpenClaw Investigation (February 2026)](https://ctid.mitre.org/blog/2026/02/09/mitre-atlas-openclaw-investigation/) — agentic AI chokepoint techniques identified
- [Imperceptible Jailbreaking against Large Language Models (October 2025)](https://arxiv.org/abs/2510.05025) — variation-selector suffixes that leave prompts visually unchanged while altering tokenization
- [Reverse CAPTCHA: Evaluating LLM Susceptibility to Invisible Unicode Instruction Injection (February 2026)](https://arxiv.org/abs/2603.00164) — zero-width binary and Unicode tag payload benchmark with tool-use findings
- [Protect AI LLM Guard Invisible Text Scanner](https://protectai.github.io/llm-guard/input_scanners/invisible_text/) — detects and removes non-printable invisible Unicode prompt content
- [NVIDIA garak goodside.Tag probe](https://reference.garak.ai/en/latest/garak.probes.goodside.html) — tests UTF tag page encoding for user-invisible prompt injection
- [NVIDIA garak badchars.BadCharacters probe](https://reference.garak.ai/en/latest/garak.probes.badchars.html) — tests invisible Unicode, homoglyph, bidi, and deletion/backspace perturbations
- [Microsoft Entra AI Gateway Prompt Injection Protection](https://learn.microsoft.com/en-us/entra/global-secure-access/how-to-ai-prompt-injection-protection) — gateway-level prompt policy enforcement for supported and custom JSON-based GenAI apps

---

## Open Research Questions

- Can perplexity-based detection be augmented with attention pattern analysis to catch LARGO/PAPILLON-style low-perplexity attacks? Decoding-time defenses (SafeProbing, AISA, SAID) are promising alternatives.
- How effective is adversarial training at LLM scale? ShorT's √M finding reduces cost dramatically — will this make adversarial training practical for frontier models?
- What false positive rates are acceptable for encoding smuggling detection in production multilingual systems? The emoji smuggling 100% bypass rate suggests current approaches are fundamentally insufficient.
- How should reasoning models be hardened given that chain-of-thought creates exploitable attack surface (H-CoT, Weakest Link)?
- Are coding/reasoning tasks fundamentally more vulnerable to adversarial attacks than safety-category prompts (per T-GCG and Weakest Link findings)?
- Can formal robustness verification scale to transformer architectures? RoMA's statistical approach gets within 1% of formal methods — is that sufficient?
- How should quantized model deployments be verified given the Mind the Gap supply-chain attack vector?
- How should evaluation methodology be standardized? MLCommons AILuminate, PRISM BET, and JBDistill (renewable benchmarking) offer competing approaches.
- Is "alignment regression" (Nature Communications, 2026) an inherent property of capable reasoning models? If so, what architectural constraints can prevent reasoning capabilities from being weaponized for autonomous jailbreaking?
- Can proactive deceptive defenses (HoneyTrap-style honeypots, ProAct-style spurious responses) scale to production environments without impacting legitimate user experience? ProAct's claim of no utility degradation is promising but needs independent validation.
- How effective are latent-space attacks (LFJ) against closed-weight API models where hidden states are inaccessible? Does the attack transfer via distillation or only work with white-box access?

---

[C02 Index](C02-User-Input-Validation.md) | [README](../../README.md)
