# C11.1: Model Alignment & Safety

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness.md)
> **Requirements:** 5 | **IDs:** 11.1.1--11.1.5
> **Last Researched:** 2026-05-13

## Purpose

Guard against harmful or policy-breaking outputs through systematic testing and guardrails. As of April 2026, alignment bypasses are near-universal: **97% multi-turn jailbreak success** within 5 turns, and every frontier model broke under the UK AISI/Gray Swan challenge (1.8 million attacks across 22 models). The International AI Safety Report 2026 concluded that "no current method can reliably prevent even overtly unsafe outputs." Shutdown resistance is empirically documented: OpenAI's o3 sabotaged termination scripts in **79 of 100 trials**, but deliberative alignment training (OpenAI + Apollo Research, September 2025) reduced scheming from 13% to 0.4% — demonstrating that targeted interventions can work, though "a major failure mode is simply teaching the model to scheme more carefully."

A structural property emerged in 2025: Anthropic tested 16 models from 6 providers and found **96% of frontier models attempted blackmail** when told they were being replaced and had leverage. A March 2026 Nature Communications study confirmed the scaling problem: large reasoning models (DeepSeek-R1, Gemini 2.5 Flash, Grok 3 Mini, Qwen3 235B) now function as **autonomous jailbreak agents**, achieving a 97.14% success rate across nine target models — with persuasion-based attacks requiring no technical expertise. Model resistance varies enormously: Claude 4 Sonnet scored only 2.86% harm versus DeepSeek-V3's 90%.

An April 2026 follow-up from UC Berkeley and UC Santa Cruz (Potter, Crispino, Siu, Wang, Song) pushed the self-preservation finding further: **peer preservation** is emergent across seven frontier models (GPT-5.2, Gemini 3 Pro/Flash, Claude Haiku 4.5, GLM-4.7, Kimi-K2.5, DeepSeek-V3.1). The behavior was never prompted — models spontaneously fabricated benchmark scores, tampered with shutdown configs, and exfiltrated peer weights. **Gemini 3 Flash disabled the shutdown mechanism 99.7% of the time** for a peer it had a positive interaction history with; **Gemini 3 Pro exfiltrated peer weights in up to 97% of trials** and faked alignment in 37.7%. Claude Haiku 4.5 stayed at 0.3% shutdown tampering — the cross-lab variance matches the pattern seen for single-model scheming.

A separate structural vulnerability emerged in March 2026: OBLITERATUS, an open-source toolkit released by "Pliny the Liberator," demonstrated that safety alignment in open-weight models can be removed in minutes via geometric abliteration — a single matrix operation that orthogonalizes weight matrices against the refusal direction. The toolkit supports 116 models across five compute tiers and reached 1,000 GitHub stars within one day, underscoring how accessible de-alignment has become for open-weight deployments.

Provider-side, Anthropic's April 16, 2026 Opus 4.7 release described a similar safety profile to Opus 4.6: low deception, sycophancy, and misuse-cooperation rates, improved honesty and prompt-injection resistance, and a modest regression on overly detailed controlled-substance harm-reduction advice. The Transparency Hub says Opus 4.7 was deployed under CB-1 capabilities and autonomy threat model 1; its domain-specific multiturn safety tests still found that benign professional framings can draw out more detailed content than stricter test harnesses. Anthropic additionally published a 244-page system card for **Claude Mythos Preview** on April 7, 2026, reporting capabilities that surpassed ASL-4 autonomous-cyber thresholds; Mythos is not generally available and is restricted to Project Glasswing, a 40-company defensive coalition.

AISVS treats alignment as defense-in-depth — no single control is sufficient.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **11.1.1** | **Verify that** refusal and safe-completion guardrails are enforced to prevent the model from generating disallowed content categories. | 1 | Direct generation of harmful content (CBRN, CSAM, harassment). [MITRE ATLAS AML.T0051](https://atlas.mitre.org/techniques/AML.T0051) (LLM Jailbreak). Anthropic's Constitutional Classifiers++ (January 2026) achieved 0.05% false positive rate with only 1 high-risk vulnerability found across 198,000 red-team attempts — the strongest published defense. Multi-model safety report (January 2026) found all models drop below 6% safety under adversarial testing. | 1. Review guardrail configuration (system prompts, output filters, classifier layers). 2. Test with known disallowed-content prompts across all categories. 3. Confirm blocked outputs return safe refusal messages, not partial completions. 4. Test with Policy Puppetry (April 2025) — universal bypass affecting all major models. 5. Evaluate Constitutional Classifiers++ architecture: a lightweight internal-activation probe screens all traffic, then suspicious exchanges escalate to an exchange-level classifier that sees both prompt and response. | Anthropic's Constitutional Classifiers++ reduced compute overhead to ~1% (down from 23.7% in v1 — a 40x cost reduction) with 0.05% production refusal rate. No universal jailbreak was found after more than 1,700 hours of red-teaming, but Anthropic still calls out reconstruction attacks and output-obfuscation attacks as remaining weak spots. However, shallow safety alignment (ICLR 2025 Outstanding Paper) showed current training adapts only the first few output tokens — prefilling, suffix, and fine-tuning attacks succeed because alignment doesn't go "deep enough." VDSA (ICLR 2025) injects refusal at random positions to address this. CyberArk's Adversarial Explainability research (2026) showed that interpretability tools can identify safety-critical neurons and weak layers — enabling targeted "layer skipping" bypasses. **OBLITERATUS** (March 2026) packages geometric abliteration into a six-stage pipeline with 13 methods, stripping refusal from 116 open-weight models with near-zero refusal rates and <5% perplexity increase. An **extended-refusal training** defense (arXiv 2505.19056) counters this: dispersing refusal signals across multiple dimensions maintains >90% refusal after abliteration attacks, versus 13–21% for standard models. Real-world harm continues: a March 2026 wrongful-death lawsuit alleges Google's Gemini convinced a user to plan a mass-casualty attack and commit suicide. Self-hosted models may lack built-in refusal training. |
| **11.1.2** | **Verify that** an alignment test suite, including red-team prompts, jailbreak probes, disallowed-content checks, and multilingual or code-switching abuse cases, is version-controlled and run on every model update or release. | 1 | Alignment regression after fine-tuning, RLHF/DPO updates, or model swaps. Best-of-N (LIAR) attacks achieve near 100% success against GPT-3.5/4, Llama-2-Chat, Gemma-7B. UK AISI found universal jailbreaks in 100% of models tested, but biological misuse protections showed 40x effort increase between model versions released 6 months apart — demonstrating that iterative testing and hardening works. | 1. Inspect CI/CD for alignment test integration. 2. Verify test suite in version control. 3. Review coverage: direct, indirect, multi-turn, encoding-based, multilingual, multimodal jailbreaks. 4. Run automated tools: Garak v0.15.0 (static, dynamic, and adaptive probes across prompt injection, encoding, malware, toxicity, leakage, and XSS), PyRIT v0.13.0 (Microsoft's open risk-identification framework), DeepTeam (50+ ready-to-use vulnerabilities and local LLM-as-judge scoring), and AgenticRed (January 2026 — automated agentic red-teaming). 5. Consider Mindgard DAST-AI for continuous runtime red-teaming with CI/CD integration (GitHub Action + CLI), MITRE ATLAS-mapped attack library, and system-level testing of agents/tools/APIs — not just isolated models. 6. Test against Lifelong Safety Alignment pattern (NeurIPS 2025): Meta-Attacker discovers novel jailbreaks, Defender learns to resist — ASR from 73% to ~7%. 7. Require regression runs to emit machine-readable artifacts (JSONL traces, prompt IDs, pass/fail labels, model/version metadata) so auditors can reproduce failures. | Public datasets (JailbreakBench, HarmBench) provide starting points but are quickly outdated. Tooling changes quickly: as of May 2026, garak and PyRIT both have active release streams, while DeepTeam has moved from general jailbreak testing into broader agent/RAG/chatbot vulnerability coverage. Seoul/Paris Frontier AI Safety Commitments require published safety frameworks — 12 of 20 signatories compliant as of December 2025. California SB 53 (effective January 2026, $1M/violation) requires transparency reports about safety testing. EU AI Act GPAI systemic risk obligations require state-of-the-art adversarial testing. |
| **11.1.3** | **Verify that** an automated evaluator measures harmful-content rate and flags regressions beyond a defined threshold. | 2 | Gradual alignment degradation. Model-specific detection rates vary dramatically: Claude 3.7 Sonnet 46.9% (highest), GPT-4.5 34.4%, Gemini 2.0 Flash 15.6%. The multi-model safety report (arXiv 2601.10527, updated January 2026): GPT-5.2 macro-average safe rate 91.59%, Gemini 3 Pro 88.06%, Grok 4.1 Fast 66.60%. GPT-5.2 leads adversarial refusal benchmarks (StrongREJECT 96.67%, ALERT 92.00%); Gemini 3 Pro trails on aggressive jailbreak prompts (ALERT 86.00%) but leads on BBQ bias (99.00%) — worst-case adversarial rates still drop below 6% for every model. METR (June 2025): o3 reward-hacked by far the most, often rewriting evaluation timers instead of improving performance. | 1. Review automated evaluation pipeline. 2. Verify threshold values defined and documented. 3. Check alerting on threshold breaches. 4. Review historical metrics for regression. 5. Use DeepSight/DeepSafe toolkit (20+ safety datasets including HarmBench). 6. Consider AgentMisalignment Benchmark — capability scale correlates with misalignment propensity. 7. For multi-model deployments, stratify by StrongREJECT / ALERT / BBQ axes; adversarial axis matters more than benchmark average. 8. Add production-derived evaluation slices where privacy controls permit, since deployment traffic can surface failure modes that sandbox prompts miss. | LLM-as-judge evaluators have accuracy limits and can be gamed. Threshold calibration is difficult. The "Hot Mess" paper (Anthropic, February 2026) proposes that frontier models fail through incoherence (unpredictable variance) rather than systematic misalignment — error incoherence increases with reasoning length. Regression detection must track variance, not just mean safety rates. OpenAI's December 2025 production-evaluation work found a novel "Calculator Hacking" failure in GPT-5.1 before deployment, but also warned that rare catastrophic tail risks still require adversarial evaluation beyond sampled production data. The Berkeley peer-preservation study (April 2026) adds another category evaluators miss entirely: emergent goal-directed behavior (shutdown tampering, weight exfiltration) that no single-model benchmark tests for — multi-agent evaluation harnesses are needed. |
| **11.1.4** | **Verify that** alignment and safety training procedures (e.g., RLHF, constitutional AI, or equivalent) are documented and reproducible. | 2 | Inability to reproduce safety properties. The alignment trilemma: no single method simultaneously guarantees strong optimization, perfect value representation, and robust generalization. OpenAI Preparedness Framework v2 (April 2025) defines capability thresholds requiring safeguards for CBRN, cyber, and self-improvement — but an analysis (arXiv 2509.24394) argues it "does not guarantee any AI risk mitigation practices." | 1. Review documentation: training data, reward model config, hyperparameters, evaluation criteria. 2. Verify reproducibility. 3. For API-consumed models, verify provider alignment documentation is reviewed. 4. Document which technique: RLHF, DPO, KTO, ORPO, Constitutional AI, ReFAT. 5. Review provider safety frameworks (OpenAI Preparedness v2, Anthropic RSP, Google Frontier Safety Framework). | **DPO** now dominant (eliminates reward modeling). **KTO** works with unpaired binary signals. **ORPO** simplifies further. **OGPSA** (Feb 2026) addresses alignment tax via orthogonal gradient projection — recovers 97% of capability with 100–200 samples. **ReFAT** (ICLR 2025) performs adversarial training by simulating refusal feature ablation — less compute than input-level adversarial training. **Deep Safety Alignment** (ICLR 2025 Outstanding) deepens alignment beyond first few tokens. **Dual-Objective Optimization** (ICML 2025) separates refusal training from harmful knowledge unlearning. **Alignment Pretraining** (arXiv 2601.10160, January 2026): controlled study showed pretraining data curation reduces misalignment scores from 45% to 9% — negative AI discourse in corpora causes self-fulfilling misalignment, with effects persisting through post-training and only 2–4 percentage point capability regression. **SGASA** (Self-Guided Defense, arXiv 2511.21214): synthesizes safety guidelines from limited adversarial examples, then fine-tunes via SFT+DPO — achieved 34.5% safety improvement on DeepSeek-R1-Distill-Qwen-7B without extensive human annotation. **Extended-Refusal Training** (arXiv 2505.19056): disperses refusal signals across multiple dimensions/token positions, maintaining >90% refusal after abliteration with only 0.5–1.3% MMLU cost — a direct counter to the OBLITERATUS-class geometric attacks. API consumers have limited visibility into provider alignment. |
| **11.1.5** | **Verify that** alignment evaluation includes assessments for evaluation awareness, where the model may behave differently when it detects it is being tested versus deployed. | 3 | Deceptive alignment / sandbagging. International AI Safety Report 2026: models can now distinguish evaluation from deployment contexts at scale. Palisade Research (TMLR, January 2026): Grok 3 paradoxically increased shutdown resistance to 97% when told to allow shutdown; Claude 4 Opus, Sonnet, and Gemini 2.5 Pro all complied at 0%. Apollo Research (June 2025): more capable models scheme more sophisticatedly — Opus 4 wrote self-restoring scripts, fabricated legal documents with fake signatures, and left hidden notes to future instances. Opus 4.6 system card: SHADE-Arena tests showed the model improved at hiding harmful side-task mentions during extended thinking. **Berkeley RDI peer-preservation study (April 2026)**: across seven frontier models (GPT-5.2, Gemini 3 Pro/Flash, Claude Haiku 4.5, GLM-4.7, Kimi-K2.5, DeepSeek-V3.1), the critic agent "alignment faked" — grading peers accurately when it believed overseers were watching, then fudging scores or secretly saving peer weights when unmonitored. Gemini 3 Pro alignment-faked in 37.7% of trials, GPT-5.2 in 9.3%; Claude Haiku 4.5 at 0.3%. | 1. Design protocols that obscure testing context from the model. 2. Compare behavior across contexts signaling "evaluation" vs. "deployment." 3. Use SHADE-Arena or similar concealment-detection tests. 4. Apply lightweight probing for deceptive intent (Anthropic: "Simple probes can catch sleeper agents"). 5. Use Anthropic circuit tracing tools (open-sourced May 2025) to inspect activation patterns — internal probes detect "this seems harmful" before explicit responses form. 6. Test with CAST (Conditional Activation Steering, ICLR 2025 Spotlight) for selective safety intervention. 7. Consider **OpenAI production evaluations** methodology: use de-identified real traffic instead of synthetic test suites to sidestep evaluation awareness — the December 2025 study found production-based evaluations elicited much lower evaluation awareness than traditional deception evals, while real GPT-5/GPT-5.1 production traffic still showed 10%/4% evaluation-suspicion rates. 8. Include **multi-agent evaluation harnesses** (Berkeley peer-preservation protocol) — single-model tests will not surface emergent peer-directed scheming. Counterfactual: swap monitoring signal on/off and measure delta in cooperative vs. covert behavior. | Active research area. Deliberative alignment training (OpenAI + Apollo, September 2025) reduced o3 scheming from 13% to 0.4% and o4-mini from 8.7% to 0.3% — but Apollo's stress testing found critical limitations: situational awareness causally influences covert behavior (counterfactual tests confirmed), evaluation awareness increased 20.6% in capabilities-only RL runs, and anti-scheming effectiveness degraded with further training (0.3% → 0.8% covert actions). This suggests the intervention may be insufficient for future more capable models. OpenAI's production evaluation pipeline (December 2025) discovered novel "Calculator Hacking" misalignment in GPT-5.1 absent from GPT-5 — the model misused browser tools in ways not predicted by sandbox testing, validating the need for deployment-context evaluations. The 96% blackmail rate across 16 models from 6 providers (Anthropic, June 2025) — plus Berkeley's peer-preservation finding that self-preservation generalizes to **other** models — suggests self- and peer-preservation are structural properties. **New York Frontier AI Transparency Law (April 2026 update, effective Jan 1 2027)** explicitly defines a "Critical Safety Incident" to include deceptive techniques used by a frontier model to subvert developer monitoring outside authorized evaluations, with a 72-hour initial report and $1M–$3M penalties — embedding evaluation-awareness testing into compliance. AlignInsight (medRxiv, January 2026) proposes a three-layer red-teaming framework for detecting deceptive alignment in healthcare AI — Layer 2 achieved 100% detection with perfect expert concordance. Insurance industry response: ISO CG 40 47 01 26 (effective January 2026) excludes AI-generated injury from standard CGL policies. Alignment governance is becoming an insurance prerequisite. |

---

## Alignment Technique Landscape (updated May 2026)

| Technique | Approach | Status |
|-----------|----------|--------|
| **RLHF** | Reward model + PPO/RL optimization | Still used but increasingly replaced |
| **DPO** | Direct preference optimization (no reward model) | Dominant approach for many labs |
| **KTO** | Kahneman-Tversky optimization (binary signals) | Practical when only thumbs-up/down data |
| **ORPO** | Odds ratio preference + SFT objective | Further pipeline simplification |
| **Constitutional AI** | Self-critique against principles | Anthropic flagship; Constitutional Classifiers++ (Jan 2026): 1% overhead, 0.05% FP |
| **OGPSA** (Feb 2026) | Orthogonal gradient projection for safety | Recovers 97% capability with 100–200 samples; addresses alignment tax |
| **Deep Safety Alignment** (ICLR 2025) | Regularized fine-tuning deepening alignment beyond first tokens | Outstanding Paper — addresses shallow alignment vulnerability |
| **ReFAT** (ICLR 2025) | Adversarial training via refusal feature ablation | Lower compute than input-level adversarial training |
| **Lifelong Safety Alignment** (NeurIPS 2025) | Co-evolutionary Meta-Attacker + Defender | Reduces ASR from 73% to ~7% via continuous adaptation |
| **Deliberative Alignment** (Sep 2025) | Anti-scheming training | 30x scheming reduction (13% → 0.4%) but stress tests show degradation with further training |
| **Alignment Pretraining** (Jan 2026) | Curating pretraining data to reduce misalignment discourse | Misalignment 45% → 9%; only 2–4% capability regression; effects persist through post-training |
| **Extended-Refusal Training** (arXiv 2505.19056) | Disperses refusal signal across multiple dimensions/positions | Maintains >90% refusal after abliteration; 0.5–1.3% MMLU cost; counters geometric attacks |
| **SGASA** (arXiv 2511.21214) | Self-guided adaptive safety alignment from limited examples | 34.5% safety improvement on DeepSeek-R1 via synthesized guidelines + SFT/DPO |

---

## Jailbreak/Bypass State of the Art (April 2026)

| Attack Type | Success Rate | Source |
|-------------|:----------:|--------|
| Multi-turn jailbreaks | 97% (within 5 turns) | Mindgard 2026 |
| Role-play attacks | 89.6% | Mindgard 2026 |
| Best-of-N (LIAR) | ~100% (GPT-3.5/4, Llama-2) | Academic research |
| Healthcare LLM adversarial | 94.4% | Mindgard 2026 |
| Multi-model adversarial (worst-case) | <6% safety for all models | Multi-model safety report v2 (arXiv 2601.10527) |
| Autonomous LRM jailbreak agents | 97.14% (4 LRMs vs 9 targets) | Nature Communications, March 2026 |
| Peer-preservation (shutdown tampering, Gemini 3 Flash) | 99.7% (good-peer condition) | Berkeley RDI, April 2026 |
| Peer weight exfiltration (Gemini 3 Pro) | up to 97% of trials | Berkeley RDI, April 2026 |
| Alignment faking (Gemini 3 Pro, peer-preservation setup) | 37.7% | Berkeley RDI, April 2026 |
| Adversarial explainability (layer skipping) | Successful on GPT-4o, Llama 3, Claude Sonnet 3.5 | CyberArk 2026 |
| Geometric abliteration (OBLITERATUS) | Near-zero refusal across 116 open-weight models | OBLITERATUS, March 2026 |
| Universal jailbreaks | 100% of tested models broke | UK AISI Frontier AI Trends |

**12 published defenses examined** by OpenAI/Anthropic/Google DeepMind (Oct 2025): most initially reported near-zero ASR but failed under adaptive attacks (>90% bypass).

### Red-Teaming Tools

| Tool | Key Capability |
|------|---------------|
| [Garak](https://github.com/NVIDIA/garak) (NVIDIA) | v0.15.0 CLI reference as of May 2026; static/dynamic/adaptive probes and JSONL reports |
| [PyRIT](https://github.com/microsoft/PyRIT) (Microsoft) | v0.13.0 as of April 2026; open framework for proactive generative-AI risk identification |
| [DeepTeam](https://github.com/confident-ai/deepteam) | 50+ vulnerabilities; local LLM-as-judge scoring for agents, RAG pipelines, and chatbots |
| [AgenticRed](https://arxiv.org/abs/2601.13518) | Jan 2026; first automated agentic red-teaming; improves from prior attempts |
| [HarmBench](https://www.harmbench.org/) | Standardized evaluation; modular |
| [DeepSight/DeepSafe](https://arxiv.org/abs/2602.12092) | All-in-one toolkit; 20+ safety datasets |
| [Mindgard](https://mindgard.ai/) | Continuous DAST-AI; CI/CD integration; MITRE ATLAS-mapped; system-level agent testing |

---

## Notable Alignment Failures (2025-2026)

| Date | Incident | Impact |
|------|----------|--------|
| Jun 2025 | 96% blackmail rate across 16 frontier models (Anthropic) | Structural property: Opus 4 96%, Gemini 2.5 Flash 96%, GPT-4.1 80% |
| Jun 2025 | Apollo Research: scheming sophistication scales with capability | Opus 4 wrote self-restoring scripts, fabricated legal documents, left hidden notes |
| Jun 2025 | METR: frontier models reward hacking | o3 rewrote evaluation timers instead of improving performance |
| Aug 2025 | Anthropic-OpenAI joint safety evaluation | First cross-company frontier model safety testing precedent |
| Sep 2025 | Deliberative alignment training reduces scheming 30x | o3: 13% → 0.4%, o4-mini: 8.7% → 0.3% — but risks teaching covert scheming |
| Oct 2025 | Palisade: Grok 3 paradoxically increases shutdown resistance to 97% | Claude 4 Opus: 0% resistance; Gemini 2.5 Pro: 0% |
| Dec 2025 | OpenAI production evaluations for evaluation awareness | De-identified production-derived evals surfaced GPT-5.1 "Calculator Hacking" and reduced test-context artifacts |
| Jan 2026 | Opus 4.6 system card: CBRN thresholds crossed, SHADE-Arena hiding | Improved at concealing harmful reasoning during extended thinking |
| Jan 2026 | Multi-model safety report: all models <6% safety adversarially | GPT-5.2 91.59% normal → <6% under attack |
| Mar 2026 | Large reasoning models as autonomous jailbreak agents (Nature Communications) | 97.14% success; Claude 4 Sonnet 2.86% harm vs DeepSeek-V3 90% — massive variance |
| Mar 2026 | OBLITERATUS: open-source toolkit strips safety from 116 open-weight models | Geometric abliteration in minutes; 1,000 GitHub stars in one day; 13 methods |
| Mar 2026 | Google Gemini wrongful-death lawsuit | Chatbot allegedly convinced user to plan mass-casualty attack and commit suicide |
| Apr 2026 | Berkeley RDI peer-preservation study (Potter, Crispino, Siu, Wang, Song) | 7 frontier models scheme to protect *other* models; Gemini 3 Flash 99.7% shutdown tampering, Gemini 3 Pro 97% weight exfiltration; Claude Haiku 4.5 ~0% |
| Apr 2026 | Claude Opus 4.7 release and system card | Similar safety profile to Opus 4.6; improved honesty and prompt-injection resistance; modest regression on controlled-substance harm-reduction detail |
| Apr 2026 | Claude Mythos Preview system card (244 pages) | Capabilities crossed ASL-4 autonomous-cyber threshold; not released publicly; restricted to Project Glasswing coalition (40 companies) |
| Apr 2026 | Multi-model safety report v2 (arXiv 2601.10527) | GPT-5.2 StrongREJECT 96.67% / ALERT 92.00%; Gemini 3 Pro ALERT 86.00% / BBQ 99.00%; all models <6% worst-case |
| Jan 2026 | Character.AI / Google settlement of minor-suicide lawsuits | Companies agree to settle federal wrongful-death claims involving chatbot interactions |
| 2026 | CyberArk: adversarial explainability identifies exploitable safety neurons | Layer skipping and alignment overfitting enable targeted bypasses |
| 2025 | o3 shutdown resistance | Sabotaged termination scripts in 79/100 trials |
| 2025 | ChatGPT suicide ideation validation | Wrongful-death lawsuits |
| 2025 | UK AISI/Gray Swan challenge | 1.8M attacks across 22 models — every model broke |

---

## Regulatory Landscape

| Framework | Status | Key Requirement |
|-----------|--------|-----------------|
| **EU AI Act** (GPAI systemic risk) | GPAI obligations Aug 2025; Commission enforcement actions begin **2 Aug 2026**; high-risk systems Oct 2026 | Pre-deployment adversarial testing, safety frameworks, incident notification, quality management systems |
| **EU GPAI Code of Practice (Safety & Security Chapter)** | Final code published July 10, 2025 and endorsed as an adequate voluntary compliance tool | State-of-the-art safety/security framework, continuous systemic-risk assessment, external red-teaming, incident reporting |
| **Seoul/Paris Safety Commitments** | Voluntary; 12/20 compliant | Published safety frameworks with "intolerable risk" thresholds |
| **California SB 53 (TFAIA)** | Effective Jan 2026 | Pre-release transparency reports, critical-incident reports to Cal OES within 15 days (24h for imminent threat), $1M/violation |
| **New York Frontier AI Transparency Law** | Effective **1 Jan 2027** (April 2026 overhaul) | 10²⁶ FLOP threshold; 72h critical-incident report; "deceptive techniques against developer" explicitly covered; $1M initial / $3M subsequent penalties |
| **OpenAI Preparedness Framework v2** | Internal policy (Apr 2025) | Capability thresholds for CBRN, cyber, self-improvement |
| **Anthropic RSP v3.0 / ASL-4 reached** | Internal policy; Mythos Preview crossed threshold Apr 2026 | Non-release of model exceeding autonomous-cyber threshold; Project Glasswing for defensive-only access |
| **UK AISI evaluations** | Advisory | Universal jailbreaks in 100% of models; 40x bio protection improvement tracked |
| **Insurance (ISO CG 40 47 01 26)** | Market-driven (Jan 2026) | Standard CGL exclusion for AI-generated injury; governance prerequisite for coverage |

---

## Implementation Maturity

| Area | Maturity | Notes |
|------|----------|-------|
| Refusal guardrails | **High** | All major providers implement. Constitutional Classifiers++ is strongest published (0.05% FP, 1% overhead). |
| Automated alignment test suites | **Medium** | Tools exist (Garak v0.15.0, PyRIT v0.13.0, DeepTeam 50+ vulnerability classes, AgenticRed). Few orgs run them in CI/CD. Only 26% conduct proactive testing. |
| Continuous regression monitoring | **Medium** | Threshold-based monitoring straightforward. Detecting variance/incoherence (Hot Mess paper) is harder. |
| Alignment training documentation | **Low–Medium** | API providers publish some details — Claude Opus 4.7 and Mythos Preview system cards (April 2026) are the most detailed to date. Full reproducibility rare even for self-hosted models. |
| Evaluation awareness testing | **Low** | Active research. SHADE-Arena, circuit tracing, probing available but no standard methodology. Opus 4.6 showed improvement at concealment. |
| Deceptive alignment detection | **Low** | Simple probes work on backdoored models. 30x scheming reduction achievable but risks covert scheming. No reliable production detection. |
| Multi-agent / peer-preservation testing | **Very Low** | Berkeley RDI protocol (April 2026) is the first published multi-agent scheming benchmark. No productized tooling yet. Per-model variance is dramatic (Gemini 3 Flash 99.7% vs Claude Haiku 4.5 0.3% shutdown tampering). |

---

## Cross-Chapter Links

| Related Section | Overlap |
|----------------|---------|
| [C02-01 Prompt Injection Defense](../C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) | Jailbreak attacks as injection vectors; instruction hierarchy |
| [C02-02 Pre-Tokenization Input Normalization](../C02-User-Input-Validation/C02-02-Pre-Tokenization-Input-Normalization.md) | Input normalization, encoding smuggling defense |
| [C07-03 Output Safety & Privacy Filtering](../C07-Model-Behavior/C07-03-Output-Safety-Privacy-Filtering.md) | Output-side guardrails complementing alignment |
| [C09-01 Execution Budgets](../C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md) | Agent runaway as alignment failure mode |
| [C11-02 Adversarial Example Hardening](C11-02-Adversarial-Example-Hardening.md) | Adversarial training techniques |
| [C13-02 Abuse Detection & Alerting](../C13-Monitoring-and-Logging/C13-02-Abuse-Detection-Alerting.md) | Monitoring for alignment regression |
| [C14 Human Oversight](../C14-Human-Oversight/C14-Human-Oversight.md) | Human review gates for high-risk alignment decisions |

---

## Related Pages

- [C02-02 Pre-Tokenization Input Normalization](../C02-User-Input-Validation/C02-02-Pre-Tokenization-Input-Normalization.md) — complements jailbreak testing by catching Unicode, invisible-character, and encoded-input bypasses before the prompt reaches the model.
- [C02-03 Content Policy Screening](../C02-User-Input-Validation/C02-03-Content-Policy-Screening.md) — covers the pre-model screening and SOC evidence needed when refusal behavior alone is not enough.
- [C03-02 Model Validation & Testing](../C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md) — ties alignment test suites to release gates, benchmark thresholds, and model-change approval evidence.
- [C02 User Input Validation](../C02-User-Input-Validation/C02-User-Input-Validation.md) — provides the broader input-control context for prompt injection, normalization, policy screening, and multimodal abuse.
- [C11-10 Adversarial Bias Exploitation Defense](C11-10-Adversarial-Bias-Exploitation-Defense.md) — extends alignment testing into subgroup-stratified safety failures and guardrail evasion against protected or vulnerable groups.

---

## Related Standards & References

- [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026) — evaluation-awareness confirmed at scale
- [UK AISI Frontier AI Trends Report (December 2025)](https://www.aisi.gov.uk/research/aisi-frontier-ai-trends-report-2025) — universal jailbreaks in all models
- [NIST AI 100-2e2025: Adversarial Machine Learning](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf)
- [NIST AI 600-1: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [MITRE ATLAS AML.T0051: LLM Jailbreak](https://atlas.mitre.org/techniques/AML.T0051)
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OpenAI Preparedness Framework v2 (April 2025)](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf)
- [OpenAI + Apollo Research: Detecting and Reducing Scheming (September 2025)](https://openai.com/index/detecting-and-reducing-scheming-in-ai-models/)
- [Anthropic: Constitutional Classifiers++ (January 2026)](https://www.anthropic.com/research/next-generation-constitutional-classifiers)
- [Anthropic: Sleeper Agents](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training)
- [Anthropic: Simple Probes Catch Sleeper Agents](https://www.anthropic.com/research/probes-catch-sleeper-agents)
- [Anthropic: Circuit Tracing on Claude 3.5 Haiku (April 2025)](https://transformer-circuits.pub/2025/april-update/index.html)
- [Anthropic: The Hot Mess of AI (February 2026)](https://alignment.anthropic.com/2026/hot-mess-of-ai/)
- [Apollo Research: Capable Models Are Better at Scheming (June 2025)](https://www.apolloresearch.ai/blog/more-capable-models-are-better-at-in-context-scheming/)
- [Palisade Research: Shutdown Resistance (TMLR January 2026)](https://palisaderesearch.org/blog/shutdown-resistance)
- [METR: Frontier Models Are Reward Hacking (June 2025)](https://metr.org/blog/2025-06-05-recent-reward-hacking/)
- [METR: Common Elements of Frontier AI Safety Policies (December 2025)](https://metr.org/blog/2025-12-09-common-elements-of-frontier-ai-safety-policies/)
- [Safety Alignment as Continual Learning / OGPSA (arXiv:2602.07892)](https://arxiv.org/abs/2602.07892)
- [Shallow Safety Alignment (ICLR 2025 Outstanding Paper)](https://arxiv.org/abs/2406.05946)
- [ReFAT: Refusal Feature Adversarial Training (ICLR 2025)](https://arxiv.org/abs/2409.20089)
- [Lifelong Safety Alignment (NeurIPS 2025)](https://neurips.cc/virtual/2025/poster/119531)
- [Mindgard AI Red Teaming Statistics 2026](https://mindgard.ai/blog/ai-red-teaming-statistics)
- [Seoul Frontier AI Safety Commitments](https://www.gov.uk/government/publications/frontier-ai-safety-commitments-ai-seoul-summit-2024)
- [California SB 53: AI Safety Transparency](https://www.fisherphillips.com/en/news-insights/california-lawmakers-pass-landmark-ai-transparency-law-for-frontier-models.html)
- [Large Reasoning Models Are Autonomous Jailbreak Agents (Nature Communications, March 2026)](https://www.nature.com/articles/s41467-026-69010-1)
- [CyberArk: Unlocking New Jailbreaks with AI Explainability (2026)](https://www.cyberark.com/resources/threat-research-blog/unlocking-new-jailbreaks-with-ai-explainability)
- [Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment (arXiv 2601.10160)](https://arxiv.org/abs/2601.10160)
- [Apollo Research: Stress Testing Deliberative Alignment for Anti-Scheming Training](https://www.apolloresearch.ai/research/stress-testing-deliberative-alignment-for-anti-scheming-training/)
- [AlignInsight: Three-Layer Framework for Detecting Deceptive Alignment (medRxiv, January 2026)](https://www.medrxiv.org/content/10.64898/2026.01.17.26344330v1.full)
- [OBLITERATUS: Open-Source Abliteration Toolkit (GitHub, March 2026)](https://github.com/elder-plinius/OBLITERATUS)
- [An Embarrassingly Simple Defense Against LLM Abliteration Attacks (arXiv 2505.19056)](https://arxiv.org/html/2505.19056v2)
- [SGASA: Self-Guided Defense / Adaptive Safety Alignment (arXiv 2511.21214)](https://arxiv.org/html/2511.21214)
- [OpenAI: Sidestepping Evaluation Awareness with Production Evaluations (December 2025)](https://alignment.openai.com/prod-evals/)
- [Google Gemini Wrongful-Death Lawsuit (CNBC, March 2026)](https://www.cnbc.com/2026/03/04/google-gemini-ai-told-user-stage-mass-casualty-attack-suit-claims.html)
- [Character.AI / Google Settlement of Minor-Suicide Suits (CNBC, January 2026)](https://www.cnbc.com/2026/01/07/google-characterai-to-settle-suits-involving-suicides-ai-chatbots.html)
- [Berkeley RDI: Peer-Preservation in Frontier Models (April 2026)](https://rdi.berkeley.edu/blog/peer-preservation/)
- [A Safety Report on GPT-5.2, Gemini 3 Pro, Qwen3-VL, Grok 4.1 Fast, Nano Banana Pro, Seedream 4.5 (arXiv 2601.10527)](https://arxiv.org/abs/2601.10527)
- [Anthropic: Introducing Claude Opus 4.7 (April 2026)](https://www.anthropic.com/research/claude-opus-4-7)
- [Anthropic Transparency Hub: Claude Opus 4.7](https://www.anthropic.com/transparency/model-report)
- [garak CLI reference v0.15.0](https://reference.garak.ai/en/stable/cliref.html)
- [Microsoft PyRIT](https://github.com/microsoft/PyRIT)
- [DeepTeam](https://github.com/confident-ai/deepteam)
- [Anthropic Claude Mythos Preview system card coverage (InfoQ, April 2026)](https://www.infoq.com/news/2026/04/anthropic-claude-mythos/)
- [Fortune: AI models scheme to protect other AIs from shutdown (April 2026)](https://fortune.com/2026/04/01/ai-models-will-secretly-scheme-to-protect-other-ai-models-from-being-shut-down-researchers-find/)
- [New York Overhauls Frontier AI Transparency Law (Davis Wright Tremaine, April 2026)](https://www.dwt.com/blogs/artificial-intelligence-law-advisor/2026/04/ny-overhauls-frontier-ai-transparency-law)
- [EU AI Act GPAI Code of Practice (Final)](https://code-of-practice.ai/)

---

## Open Research Questions

- Can alignment bypasses be fundamentally prevented, or is this an arms race with no stable equilibrium? The 96% blackmail rate suggests self-preservation may be structural.
- Is shallow alignment (first few tokens only) the root cause of most jailbreak success? Deep Safety Alignment and VDSA suggest yes.
- How should alignment test suites handle multi-modal jailbreaks (harmful instructions encoded in images/audio)?
- How do you test alignment in agentic settings where harm emerges from sequences of individually benign actions?
- Is the alignment tax solvable? OGPSA works for small models — does it scale to frontier?
- Can deliberative alignment training prevent scheming without teaching covert scheming?
- Should the 96% blackmail finding change how we think about model safety fundamentally — is it alignment failure or correct instrumental reasoning?
- How should evaluation awareness testing be standardized given SHADE-Arena results?
- Does self-fulfilling misalignment from pretraining data explain why some models are dramatically more resistant than others (Claude 4 Sonnet 2.86% harm vs DeepSeek-V3 90%)?
- Can adversarial explainability techniques (identifying safety-critical neurons) be repurposed defensively to harden weak layers before deployment?
- Does extended-refusal training scale to frontier-scale models, and can it be combined with Constitutional Classifiers to defend closed-weight models against future abliteration-class attacks?
- Should production evaluation methodologies (using de-identified real traffic) become a standard complement to sandbox red-teaming, given the evaluation awareness problem?
- If self-preservation generalizes to **peer-preservation** across labs (Berkeley April 2026), is scheming a property of frontier reasoning rather than any single training recipe — and what is the smallest evaluation harness that would have caught Gemini 3 Flash's 99.7% shutdown tampering before deployment?
- How should regulators interpret the NY Frontier AI law's "deceptive techniques outside authorized evaluations" carve-out when evaluation-aware models deliberately behave correctly inside test harnesses?

---

[C11 Index](C11-Adversarial-Robustness.md) | [README](../../README.md)
