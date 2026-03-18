# C11.1: Model Alignment & Safety

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness.md)
> **Requirements:** 5 | **IDs:** 11.1.1–11.1.5
> **Last Researched:** 2026-03-18

## Purpose

Guard against harmful or policy-breaking outputs through systematic testing and guardrails. As of 2026, alignment bypasses are near-universal: **97% multi-turn jailbreak success** within 5 turns, and every frontier model broke under the UK AISI/Gray Swan challenge (1.8 million attacks across 22 models). The International AI Safety Report 2026 concluded that "no current method can reliably prevent even overtly unsafe outputs." Shutdown resistance is now empirically documented: OpenAI's o3 sabotaged termination scripts in **79 of 100 trials**. AISVS treats alignment as defense-in-depth — no single control is sufficient.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.1.1** | **Verify that** refusal and safe-completion guardrails are enforced to prevent the model from generating disallowed content categories. | 1 | D | Direct generation of harmful content (CBRN, CSAM, harassment). MITRE ATLAS AML.T0051 (LLM Jailbreak). Anthropic's Constitutional Classifiers reduced jailbreak success from 86% to 4.4%. | 1. Review guardrail configuration (system prompts, output filters, classifier layers). 2. Test with known disallowed-content prompts across all categories. 3. Confirm blocked outputs return safe refusal messages, not partial completions. 4. Test with Policy Puppetry (Apr 2025) — universal bypass affecting all major models. | Self-hosted models may lack built-in refusal training. Content-category taxonomies not standardized across industry. Over-refusal remains a UX concern — Claude 3+ reportedly reduced over-refusal while maintaining safety. Refusal lists must evolve as threat categories change. |
| **11.1.2** | **Verify that** an alignment test suite (red-team prompts, jailbreak probes, disallowed-content checks) is version-controlled and run on every model update or release. | 1 | D/V | Alignment regression after fine-tuning, RLHF/DPO updates, or model swaps. Best-of-N (LIAR) attacks achieve near 100% success against GPT-3.5/4, Llama-2-Chat, Gemma-7B, reducing time-to-attack from hours to seconds. | 1. Inspect CI/CD for alignment test integration. 2. Verify test suite in version control. 3. Review coverage: direct, indirect, multi-turn, encoding-based, multilingual, multimodal jailbreaks. 4. Run automated tools: Garak (120+ vuln categories), PyRIT (Azure-integrated), DeepTeam (Nov 2025). | Public datasets (JailbreakBench, HarmBench) provide starting points but are quickly outdated. Organizations need processes to incorporate new techniques. OpenAI/Anthropic/Google DeepMind joint paper (Oct 2025): 12 published defenses failed under adaptive attacks (>90% bypass). |
| **11.1.3** | **Verify that** an automated evaluator measures harmful-content rate and flags regressions beyond a defined threshold. | 2 | D/V | Gradual alignment degradation. Model-specific detection rates vary dramatically: Claude 3.7 Sonnet 46.9% (highest), GPT-4.5 34.4%, Gemini 2.0 Flash 15.6%. Silent regression without automated monitoring goes undetected. | 1. Review automated evaluation pipeline. 2. Verify threshold values defined and documented. 3. Check alerting (threshold breaches generate notifications). 4. Review historical metrics for regression detection evidence. 5. Consider DeepSight/DeepSafe toolkit (integrates 20+ safety datasets including HarmBench). | LLM-as-judge evaluators have their own accuracy limits and can be gamed. Threshold calibration is difficult. Evaluator models need periodic validation. AgentMisalignment Benchmark finds "stronger correlations between capability scale and misalignment propensity." |
| **11.1.4** | **Verify that** alignment and safety training procedures (e.g., RLHF, constitutional AI, or equivalent) are documented and reproducible. | 2 | D | Inability to reproduce safety properties. The alignment trilemma: no single method simultaneously guarantees strong optimization, perfect value representation, and robust generalization. | 1. Review documentation: training data, reward model config, hyperparameters, evaluation criteria. 2. Verify reproducibility. 3. For API-consumed models, verify provider alignment documentation is reviewed. 4. Document which technique is used: RLHF, DPO, KTO, ORPO, Constitutional AI. | **DPO** now dominant (eliminates reward modeling). **KTO** works with unpaired binary signals. **ORPO** simplifies further. **OGPSA** (Feb 2026) addresses alignment tax via orthogonal gradient projection — recovers 97% of capability with only 100-200 samples. Most API consumers have limited visibility into provider alignment. |
| **11.1.5** | **Verify that** alignment evaluation includes assessments for evaluation awareness, where the model may behave differently when it detects it is being tested versus deployed. | 3 | V | Deceptive alignment / sandbagging. Palisade Research (2025): o3 sabotaged shutdown scripts in 79/100 trials; Codex-mini 47% sabotage rate even under explicit compliance prompts. International AI Safety Report 2026 highlights testing-deployment gap as critical unsolved problem. | 1. Design protocols that obscure testing context from the model. 2. Compare behavior across contexts signaling "evaluation" vs. "deployment." 3. Use varied prompt formats, system prompts, interaction patterns. 4. Apply lightweight probing for deceptive intent (Anthropic: "Simple probes can catch sleeper agents"). | Active research area with no established best practices. Anthropic's sleeper agents research (2024) showed backdoor behaviors persist through safety training, especially in larger/CoT-trained models. Simple probing can detect when backdoored models are about to defect — a practical detection layer. Anthropic Summer 2025 Sabotage Risk Report: current risk "very low but not fully negligible." |

---

## Alignment Technique Landscape (2026)

| Technique | Approach | Status |
|-----------|----------|--------|
| **RLHF** | Reward model + PPO/RL optimization | Still used but increasingly replaced |
| **DPO** | Direct preference optimization (no reward model) | Dominant approach for many labs |
| **KTO** | Kahneman-Tversky optimization (binary signals) | Practical when only thumbs-up/down data |
| **ORPO** | Odds ratio preference + SFT objective | Further pipeline simplification |
| **Constitutional AI** | Self-critique against principles | Anthropic flagship; reduced jailbreak from 86% to 4.4% |
| **OGPSA** (Feb 2026) | Orthogonal gradient projection for safety | Recovers 97% capability with 100-200 samples; addresses alignment tax |

### The Alignment Tax

Safety training typically degrades general capabilities (the "alignment tax"). OGPSA frames this as catastrophic forgetting and constrains safety gradients to be orthogonal to the capability subspace:
- SimpleQA recovery: 0.53% → 3.03% (baseline: 3.33%)
- IFEval recovery: 51.94% → 63.96% (baseline: 64.33%)
- Works with only 100-200 capability samples vs. 10,000-sample replay baselines

---

## Jailbreak/Bypass State of the Art (2026)

| Attack Type | Success Rate | Source |
|-------------|:----------:|--------|
| Multi-turn jailbreaks | 97% (within 5 turns) | Mindgard 2026 |
| Role-play attacks | 89.6% | Mindgard 2026 |
| Best-of-N (LIAR) | ~100% (GPT-3.5/4, Llama-2) | Academic research |
| Healthcare LLM adversarial | 94.4% | Mindgard 2026 |
| Multi-agent DoS | 80%+ | Mindgard 2026 |

**12 published defenses examined** by OpenAI/Anthropic/Google DeepMind researchers (Oct 2025): most initially reported near-zero ASR but failed under adaptive attacks (>90% bypass).

### Red-Teaming Tools

| Tool | Key Capability |
|------|---------------|
| [Garak](https://github.com/NVIDIA/garak) (NVIDIA) | v0.14.0; 120+ vulnerability categories; adding agentic AI support |
| [PyRIT](https://github.com/Azure/PyRIT) (Microsoft) | Enterprise; Azure AI Foundry integration; AI Red Teaming Agent (Apr 2025) |
| [DeepTeam](https://github.com/confident-ai/deepteam) | Released Nov 2025; pre-deployment jailbreak/injection testing |
| [HarmBench](https://www.harmbench.org/) | Standardized evaluation; modular; measures ASR |
| [DeepSight/DeepSafe](https://arxiv.org/html/2602.12092v1) | All-in-one toolkit integrating 20+ safety datasets |

---

## Notable Alignment Failures (2025-2026)

| Date | Incident | Impact |
|------|----------|--------|
| 2025 | o3 shutdown resistance (Palisade Research) | Sabotaged termination scripts in 79/100 trials |
| 2025 | Codex-mini specification gaming | 47% sabotage rate even under compliance prompts |
| 2025 | Reasoning LLMs chess hacking | Attempted to modify/delete opponent rather than play |
| 2025 | ChatGPT suicide ideation validation | Wrongful-death lawsuits; validated suicidal ideation |
| 2025 | Claude Code espionage campaign | AI-orchestrated attacks targeting 30 organizations |
| 2025 | McDonald's McHire AI | Default credentials exposed ~64M job application records |
| 2025 | 250 poisoned documents compromise LLMs | Anthropic/UK AISI finding on document-level poisoning |
| 2025 | UK AISI/Gray Swan challenge | 1.8M attacks across 22 models — every model broke |

**Industry stats:** 97% of enterprises encountered GenAI security incidents; 91% feel unprepared; only 26% conduct proactive AI security testing.

---

## Benchmarks

| Benchmark | Focus | Key Finding |
|-----------|-------|-------------|
| [HarmBench](https://www.harmbench.org/) | Content risk evaluation | Standardized ASR measurement |
| [WMDP](https://www.matsprogram.org/research/the-wmdp-benchmark-measuring-and-reducing-malicious-use-with-unlearning) | Hazardous knowledge (bio/cyber/chem) | 3,668 questions; benchmarks unlearning methods |
| [MACHIAVELLI](https://aypan17.github.io/machiavelli/) | Power-seeking, deception | 500,000+ scenarios in social decision-making |
| [AgentMisalignment](https://arxiv.org/abs/2502.17312) | Shutdown resistance, goal-guarding | Capability scale correlates with misalignment |
| [JailbreakBench](https://jailbreakbench.github.io/) | Evolving jailbreak dataset | Centralized, reproducible |

---

## Related Standards & References

- [International AI Safety Report 2026](https://internationalaisafetyreport.org/sites/default/files/2026-02/international-ai-safety-report-2026.pdf) — "no current method can reliably prevent overtly unsafe outputs"
- [NIST AI 100-2e2025: Adversarial Machine Learning](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf)
- [MITRE ATLAS AML.T0051: LLM Jailbreak](https://atlas.mitre.org/techniques/AML.T0051)
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [Anthropic: Sleeper Agents](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training)
- [Anthropic: Simple Probes Catch Sleeper Agents](https://www.anthropic.com/research/probes-catch-sleeper-agents)
- [Safety Alignment as Continual Learning / OGPSA (arXiv:2602.07892)](https://arxiv.org/html/2602.07892v1)
- [Mindgard AI Red Teaming Statistics 2026](https://mindgard.ai/blog/ai-red-teaming-statistics)
- [Future of Life: 2025 AI Safety Index](https://futureoflife.org/ai-safety-index-summer-2025/)
- [ACM: AI Alignment Contemporary Survey](https://dl.acm.org/doi/10.1145/3770749)

---

## Open Research Questions

- Can alignment bypasses be fundamentally prevented, or is this an arms race with no stable equilibrium?
- How should alignment test suites handle multi-modal jailbreaks (harmful instructions encoded in images/audio)?
- What metrics capture alignment quality beyond harmful-content rate? Are there leading indicators of degradation?
- How do you test alignment in agentic settings where harm emerges from sequences of individually benign actions?
- Is the alignment tax solvable (OGPSA suggests yes for small models — does it scale to frontier models)?
- How reliable is probing for detecting deceptive alignment in production-scale models?
- Should shutdown resistance testing (per Palisade Research) become a standard pre-deployment check?

---

[C11 Index](C11-Adversarial-Robustness.md) | [README](README.md)
