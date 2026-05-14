# C7.2: Hallucination Detection & Mitigation

> [Back to C07 Index](C07-Model-Behavior.md)
> **Last Researched:** 2026-05-13

## Purpose

Hallucination - the generation of plausible-sounding but factually incorrect or fabricated content - is one of the most consequential failure modes of generative AI. NIST AI 600-1 uses the term "confabulation" and treats confidently stated false content as one of the primary generative AI risk categories, with special concern for healthcare, legal, financial, and other consequential decision-making contexts. OWASP LLM09:2025 frames the same failure mode as misinformation when model output is consumed as authoritative without grounding, validation, or human review.

As of May 2026, the best audit posture is to treat hallucination as both a reliability risk and a security signal. Columbia Journalism Review's March 2025 Tow Center study found that live AI search tools returned incorrect article citations in more than 60% of tested queries, with Perplexity wrong 37% of the time and Grok 3 wrong 94% of the time. The October 2024 Whisper reporting showed the same pattern outside chat: transcription systems can invent harmful text, including medical content. In software workflows, package hallucinations create a supply-chain path: Lasso Security's 2024 research found GPT-3.5 recommended at least one nonexistent package in nearly 30% of tested programming prompts, and MITRE ATLAS tracks the pattern through AML.T0062 (Discover LLM Hallucinations), AML.T0060 (Publish Hallucinated Entities), and AML.T0048.003 (User Harm).

### May 2026 Audit Signals

| Signal | What to Verify |
|--------|----------------|
| Confidence scores are calibrated, not decorative | Scores should be validated against domain-specific holdout sets; low scores should drive fallback, review, or secondary verification. |
| Grounding checks inspect claim support | RAG faithfulness checks should break output into claims and compare each claim against retrieved context, not just confirm that citations are syntactically present. |
| Tool provenance is logged per request | High-confidence factual assertions should be tied to retrieval, deterministic lookup, or approved tool calls before they are shown to users or passed downstream. |
| High-impact output gets independent review | Legal, medical, financial, safety, and regulated decisions need a separate verification mechanism and evidence that thresholds match the system's risk class. |

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **7.2.1** | **Verify that** the system assesses the reliability of generated answers using a confidence or uncertainty estimation method (e.g., confidence scoring, retrieval-based verification, or model uncertainty estimation). | 1 | **Undetected hallucination** (OWASP LLM09: Misinformation, NIST AI 600-1 confabulation risk). MIT research (Jan 2025): models are 34% more likely to use confident language when generating false vs. factual information — confidence alone is unreliable. Reasoning models make the problem worse: OpenAI o3 series hallucinates 33-51% on PersonQA/SimpleQA benchmarks despite improved reasoning (vs. ~16% for o1). | 1. Confirm system produces reliability scores. 2. Test with known-hallucination-inducing prompts (nonexistent entities, fabricated dates). 3. Review scoring method: logprob analysis, retrieval overlap, multi-sample consistency, dedicated detection model (HHEM, MiniCheck, HDM-1, HalluClean). 4. Check calibration — does the score correlate with actual accuracy? 5. Test specifically with reasoning-intensive prompts, as reasoning models hallucinate more on factual lookups. 6. Where latency budgets are tight, evaluate adaptive-sampling estimators (Adaptive Bayesian Semantic Entropy, arXiv:2603.22812, Mar 2026) that cut sample counts ~50% vs. fixed-budget SelfCheckGPT. | **Tools**: Vectara HHEM-2.3 (commercial, 0.758+ recall, 11 languages), HHEM-2.1-Open (T5-based, English-only, degrades on long contexts), SelfCheckGPT, AlignScore, Bespoke-MiniCheck, AIMon HDM-1 (real-time, low-latency), Datadog LLM Observability (production hallucination detection with multi-stage LLM-as-Judge + deterministic checks, GA May 2025), **HalluClean** (AAAI 2026, Plan-Reason-Judge pipeline, zero-shot across QA/summarization/dialogue/math/contradiction without external KB). **Key insight**: LLM-as-Judge evaluation aligns far more closely with human assessments than traditional metrics (up to 45.9% performance gap for perplexity-based methods). As of 2026, MetaQA (metamorphic prompt mutations) outperforms SelfCheckGPT by 0.15-0.37 F1-score and works on closed-source models without token probabilities. **Training root cause (OpenAI, Sept 2025):** next-token prediction objectives and RLHF reward confident guessing over calibrated uncertainty — behavioral calibration RL (arXiv:2512.19920, Dec 2025) shows even a 4B-parameter model can match frontier calibration on SimpleQA by learning to abstain or flag uncertain claims. **Budget-aware detection (Mar 2026):** Adaptive Bayesian Semantic Entropy with Guided Semantic Exploration (arXiv:2603.22812) adds variance-based early termination over Farquhar et al.'s Nature 2024 semantic-entropy baseline, requiring ~53% of the samples for equivalent detection — important for real-time pipelines where SelfCheckGPT's multi-sample cost is prohibitive. **Spectral attention signals (Feb 2026, arXiv:2502.17598):** top-k Laplacian eigenvalues of attention maps correlate with hallucination onset — another white-box alternative to activation probing (CLAP). |
| **7.2.2** | **Verify that** the application automatically blocks answers or switches to a fallback message if the confidence score drops below a defined threshold. | 2 | **Serving unreliable content.** Domain-specific hallucination rates remain high without safeguards: Legal 18.7%, Medical 15.6%, Financial 13.8%. One robo-advisor hallucination affected 2,847 client portfolios ($3.2M remediation). | 1. Configure threshold. 2. Submit prompts producing below-threshold scores; verify fallback response. 3. Test edge cases near boundary. 4. Verify threshold is domain-appropriate (medical/legal: higher; conversational: lower). | Threshold selection is domain-dependent. HalluLens benchmark (Apr 2025) found hallucination rates of 26.84% (Llama-3.1-405B) to 85.22% (Qwen 2.5-7B) when models don't refuse. RAG reduces hallucination by ~71%; self-consistency checking by ~65%; uncertainty prompts by ~33%. |
| **7.2.3** | **Verify that** hallucination events (low-confidence responses) are logged with input/output metadata for analysis. | 2 | **Inability to improve.** Without logging, teams cannot track hallucination rates, identify patterns (specific topics that consistently hallucinate), or use data for fine-tuning. 82% of AI bugs stem from hallucinations and accuracy failures. | 1. Trigger low-confidence responses. 2. Verify logs include: timestamp, confidence score, input hash, output hash, model version, retrieval context. 3. Confirm PII redaction. 4. Verify logs feed monitoring dashboards (C7.6, C13.3). | Logs should support both operational monitoring and compliance. Consider hashing rather than storing full prompts/responses to balance forensic value against data retention risks. Structure logs for SIEM ingestion. |
| **7.2.4** | **Verify that** the system tracks tool and function invocation history within a request chain and flags high-confidence factual assertions that were not preceded by relevant verification tool usage, as a practical hallucination detection signal independent of confidence scoring. | 2 | **Unsupported factual claims in agentic workflows.** Columbia Journalism Review (Mar 2025) found live AI search tools returned incorrect article citations in more than 60% of tested queries; Perplexity was wrong 37% of the time and Grok 3 was wrong 94% of the time. Package hallucination turns the same failure mode into supply-chain exposure when coding assistants suggest nonexistent dependencies and attackers publish them. MITRE ATLAS maps this pattern through AML.T0062 (Discover LLM Hallucinations), AML.T0060 (Publish Hallucinated Entities), and AML.T0048.003 (User Harm). | 1. In tool-augmented systems, submit factual lookup prompts and verify that factual claims are preceded by retrieval, deterministic lookup, or approved tool use. 2. Check that citation URLs are live and content-matching, not just syntactically valid. 3. For code generation, verify package names, versions, and install commands against package-manager APIs and internal allowlists before execution. 4. Review logs for assertion-to-tool lineage across the request chain. | Structural hallucination signal: if a model claims to know something it never looked up, that is inherently suspect. Requires per-request tool logs, assertion extraction, and a policy that defines which claim types require tool backing. Citation verification should check source content; package verification should check registry existence, ownership, age, reputation, and lockfile/SCA policy before install. |
| **7.2.5** | **Verify that** for responses classified as high-risk or high-impact by policy, the system performs an additional verification step through an independent mechanism, such as retrieval-based grounding against authoritative sources, deterministic rule-based validation, tool-based fact-checking, or consensus review by a separately provisioned model. | 3 | **Single-point-of-failure in critical contexts.** NIST AI 600-1 warns that confabulated content is especially important to monitor in consequential decision-making contexts. Mata v. Avianca (S.D.N.Y., Jun 2023) and United States v. Hayes (E.D. Cal., Jan 2025) show the legal risk of fabricated citations and quotations. EU AI Act Article 15 requires high-risk AI systems to achieve appropriate accuracy, robustness, and cybersecurity levels throughout the lifecycle and to declare relevant accuracy metrics in instructions for use. | 1. Identify high-risk classification criteria and require a secondary check before release or downstream action. 2. Verify independence: different source corpus, deterministic database lookup, rule engine, separately provisioned model, or human expert review rather than re-asking the same generator. 3. Test with fabricated citations, wrong dates, unsupported medical/legal/financial claims, and stale-source prompts. 4. For RAG, use claim-level faithfulness checks such as Ragas or HHEM-style consistency scoring against retrieved context. 5. For EU-regulated high-risk systems, retain evidence that accuracy thresholds, fallback behavior, and post-market monitoring satisfy Article 15 and related lifecycle obligations. | Level 3 controls are expensive and can still fail if the verifier shares the same blind spots as the generator. Arize LibreEval1.0, Vectara HHEM, Ragas faithfulness, deterministic citation/package validation, and human review each cover different failure modes; high-impact systems should combine them and measure residual error rates instead of relying on one detector. |

---

## Hallucination Rates by Model (2025-2026)

### Simple Benchmark (Vectara, early 2025)

| Model | Hallucination Rate |
|-------|:-----------------:|
| Gemini-2.0-Flash-001 | 0.7% |
| OpenAI o3-mini-high | 0.8% |
| GPT-4.5-Preview | 1.2% |
| GPT-4o | 1.5% |
| Claude-3-Opus | 10.1% |
| DeepSeek-R1 | 14.3% |

### Challenging Benchmark (Vectara Next-Gen, early 2026)

| Model | Hallucination Rate |
|-------|:-----------------:|
| Gemini-2.5-Flash-Lite | 3.3% |
| Gemini-3.1-Pro | 10.4% |
| GPT-5.2 (xhigh) | 10.8% |
| Claude Opus 4.6 | 12.2% |
| Grok-4.1 Fast Reasoning | 20.2% |

**Historical trend:** Best-model rates dropped from 21.8% (2021) to 0.7% (2025) — 96% reduction on simple benchmarks. But harder benchmarks reveal 3-20%+ even for top models. AA-Omniscience benchmark: Gemini 3 Pro achieved 53% accuracy but 88% hallucination rate (overconfidence paradox); Grok 4 ~64% hallucination on knowledge questions; Claude Opus 4.6 ~46.4% accuracy. The divergence between easy and hard benchmarks keeps growing — different benchmarks measure fundamentally different failure modes, making cross-benchmark comparison essential.

**Reasoning model paradox (2025-2026):** Reasoning-focused models actually hallucinate *more* on factual benchmarks. OpenAI o3 series scores 33-51% hallucination on PersonQA/SimpleQA, roughly double o1's ~16% rate. DeepSeek-R1 scores 14.3% on grounded summarization vs. DeepSeek-V3's 6.1%. PlaceboBench (pharma RAG) exposes even larger gaps — some frontier models hit 63.8% fabrication rates on medical claims. The pattern suggests reasoning chains can amplify confabulation when the model "reasons" its way to plausible but fabricated conclusions.

---

## Detection Tools Landscape (2026)

| Tool | Type | Key Metric | Notes |
|------|------|-----------|-------|
| [Vectara HHEM-2.3](https://www.vectara.com/blog/hhem-2-1-a-better-hallucination-detection-model) | Commercial classifier | 0.758+ recall on RAGTruth | 11 languages, extended context |
| [HHEM-2.1-Open](https://huggingface.co/vectara/hallucination_evaluation_model) | Open source (T5) | English-only | Degrades on long contexts (8.99% accuracy drop) |
| [FaithJudge](https://arxiv.org/html/2505.04847v1) | LLM-as-Judge | ACL EMNLP 2025 | Few-shot human-annotated examples |
| [Arize LibreEval](https://arize.com/llm-hallucination-dataset/) | Dataset + detection | LLM Council > human (94% vs 93%) | Largest open-source RAG hallucination dataset |
| [SelfCheckGPT](https://arxiv.org/abs/2303.08896) | Sampling consistency | Zero-resource | No external knowledge needed; stochastic sampling detects hallucinations via cross-sample contradiction |
| [FACTUM](https://arxiv.org/abs/2601.05866) | Mechanistic (internal pathway analysis) | +37.5% AUC over baselines | ECIR 2026; detects citation hallucination in RAG by analyzing Attention vs. FFN pathway coordination; scale-dependent signatures |
| [ChainPoll](https://arxiv.org/abs/2310.18344) | Chain-of-Thought judging | Outperforms SelfCheckGPT, GPTScore, G-Eval, TRUE | Uses CoT reasoning to judge hallucination presence across closed and open domain |
| [REFIND](https://arxiv.org/html/2502.13622v2) | Retrieval-augmented span detection | SemEval-2025 Task 3 | Token-level Context Sensitivity Ratio (CSR) identifies hallucinated spans within LLM text |
| [HalluLens](https://arxiv.org/html/2504.17550v1) | Benchmark | 94.77% agreement with humans | Extrinsic vs. intrinsic distinction |
| [RAGAS](https://docs.ragas.io/) | RAG evaluation | Faithfulness + relevance | Framework for RAG pipeline assessment |
| [HalluGraph](https://arxiv.org/abs/2512.01659) | Graph-theoretic (knowledge graph alignment) | 0.94 AUC on legal contract QA | Decomposes into Entity Grounding + Relation Preservation; catches entity swaps that embedding metrics miss |
| [CLAP](https://arxiv.org/abs/2509.09700) | Activation probing (cross-layer attention) | Fine-grained, real-time | Lightweight classifier on model activations; works across temperatures; ECAI 2025 |
| [MetaQA](https://dl.acm.org/doi/10.1145/3715735) | Metamorphic prompt mutation | +0.15-0.37 F1 over SelfCheckGPT | No token probabilities needed; works on closed-source models; ACM 2025 |
| [AIMon HDM-1](https://www.aimon.ai/posts/aimon-hdm-1-hallucination-detection-model/) | Production classifier | Real-time, low-latency | Optimized for production deployment; low false-positive rate |
| [GPTZero Hallucination Check](https://gptzero.me/news/iclr-2026/) | Citation verification | Caught 50+ hallucinations in ICLR 2026 | Detects fabricated authors, wrong attribution, fake citations in academic text |
| MiniCheck / Bespoke-MiniCheck | Small classifier | Efficient inference | AlignScore alternative |
| [Datadog LLM Observability](https://www.datadoghq.com/blog/llm-observability-hallucination-detection/) | Production monitoring | Multi-stage LLM-as-Judge + deterministic checks | GA May 2025; detects contradictions and unsupported claims; integrates with SIEM/APM; per-span hallucination attribution |
| [BriefCatch RealityCheck](https://abovethelaw.com/2026/03/new-tool-catches-ai-hallucinations-in-legal-briefs/) | Legal citation verification | Deterministic + AI two-layer | Launched March 2026; validates case names, court IDs, reporter volumes against legal databases; color-coded per-citation output |
| [MedHallu](https://medhallu.github.io/) | Medical hallucination benchmark | 10K QA pairs from PubMedQA | EMNLP 2025; best model F1=0.625 on hard cases; first domain-specific medical hallucination benchmark |
| [FinReflectKG-HalluBench](https://arxiv.org/abs/2603.20252) | Financial KG-QA benchmark | 755 annotated examples from SEC 10-K | March 2026; most detectors degrade 44-84% MCC when noisy KG triplets introduced |
| [HalluClean](https://arxiv.org/abs/2511.08916) | Detect-and-correct framework | AAAI 2026 | Plan-Reason-Judge pipeline; zero-shot across QA, summarization, dialogue, math word problems, contradiction detection; no external KB or supervised detector required; adds a revision module that rewrites flagged content |
| [Adaptive Bayesian Semantic Entropy](https://arxiv.org/abs/2603.22812) | Adaptive sampling detector | ~50% fewer samples vs. baseline | March 2026; hierarchical Bayesian model over semantic distribution, variance-based early-termination; guided semantic exploration via critical-token perturbation |
| [Spectral Attention Probing](https://arxiv.org/html/2502.17598v2) | Mechanistic (spectral) | Top-k Laplacian eigenvalues correlate with hallucination | February 2026; probing model over spectral features of attention maps; white-box alternative to CLAP activation probing |

### Detection Method Taxonomy (2025-2026 State of the Art)

The hallucination detection field has consolidated into five major approach categories, with significant advances in 2025-2026:

| Approach | How It Works | Strengths | Limitations |
|----------|-------------|-----------|-------------|
| **Retrieval-based** (REFIND, RAG grounding) | Compares generated claims against retrieved source documents; token-level sensitivity ratios identify unsupported spans | Anchors verification to authoritative sources; identifies specific hallucinated spans, not just binary judgments | Depends on retrieval quality; cannot detect hallucinations about topics absent from the corpus |
| **Self-consistency** (SelfCheckGPT, semantic entropy) | Samples multiple responses and detects contradictions; Nature 2024 showed semantic entropy predicts hallucinations | Zero-resource; works on black-box models; no external knowledge base needed | Computationally expensive (multiple forward passes); fails when model consistently hallucinates the same wrong answer |
| **LLM-as-Judge** (ChainPoll, FaithJudge, LLM Council) | Uses a separate LLM (often with Chain-of-Thought) to evaluate whether output is faithful to sources or factually correct | High agreement with human annotators (94%+); flexible across domains | Introduces judge model as single point of failure; susceptible to shared biases between generator and judge |
| **Mechanistic / Internal** (FACTUM) | Analyzes internal model pathways (Attention vs. FFN coordination) to detect citation hallucinations from within | Up to 37.5% AUC improvement; does not require external knowledge; signature analysis reveals *why* hallucination occurs | Requires white-box model access; detection signatures shift with model scale (3B vs. 8B behave differently) |
| **Graph-theoretic** (HalluGraph) | Builds knowledge graphs from context, query, and response; measures structural alignment via Entity Grounding and Relation Preservation scores | Catches entity swaps invisible to embedding metrics; auditable decomposition; 0.94 AUC on legal QA | Requires entity/relation extraction pipeline; computational overhead for graph construction; domain-dependent extraction quality |
| **Metamorphic testing** (MetaQA, MetaRAG) | Applies systematic prompt mutations and checks if metamorphic relations hold — violations signal hallucination | Works on closed-source models without token probabilities; no external knowledge needed; outperforms SelfCheckGPT | Requires careful design of metamorphic relations per domain; multiple queries increase latency |
| **Activation probing** (CLAP) | Trains lightweight classifiers on the model's cross-layer attention activations to flag hallucinations in real time | Fine-grained detection; works across sampling temperatures; low overhead once trained | Requires white-box model access for activation extraction; probe must be retrained per model |
| **Embedding / Learning-based** (HHEM, MiniCheck, AlignScore) | Trained classifiers that score generated text against reference for factual consistency | Fast inference; can be deployed as lightweight pipeline components | Require training data; may not generalize across domains without fine-tuning |

**Key 2025-2026 insight:** The field is moving from binary hallucination detection (hallucinated yes/no) toward span-level identification (which specific tokens or claims are hallucinated) and mechanistic understanding (why the model hallucinated). FACTUM's pathway analysis and REFIND's token-level CSR scoring represent this shift. As of March 2026, the taxonomy has expanded from five to eight distinct approaches, with graph-theoretic methods (HalluGraph), metamorphic testing (MetaQA), and activation probing (CLAP) each filling gaps the earlier approaches couldn't address — particularly around closed-source model compatibility and domain-specific precision.

### Mitigation Effectiveness

| Technique | Hallucination Reduction |
|-----------|:-----------------------:|
| RAG (Retrieval-Augmented Generation) | ~71% |
| Self-consistency checking | ~65% |
| Training on curated datasets | ~40% |
| Mitigation/uncertainty prompts | ~33% |

---

## Notable Incidents (2025-2026)

| Date | Incident | Impact |
|------|----------|--------|
| Mar 2025 | Columbia Journalism Review citation study | Perplexity: 37%, ChatGPT: 67%, Grok-3: 94% citation hallucination |
| Mar 2026 | Whiting v. City of Athens (6th Circuit) | $30,000 sanction for fabricated citations, false quotes |
| 2026 | Fletcher v. Experian (5th Circuit) | "Conduct unbecoming a member of the bar" for fabricated quotations |
| Oct 2025 | Two federal judges used unauthorized AI | Court orders contained factual inaccuracies from AI drafting |
| 2025 | Deloitte reports (Australia, Newfoundland) | Fabricated academic sources in government consulting reports (A$440,000 cost) |
| 2025 | NeurIPS 2025 papers analysis | Hundreds of flawed references across 50+ papers including invented citations |
| 2025 | OpenAI Whisper transcription | Invented text including racial commentary and imagined medical diagnoses |
| 2024-2025 | Robo-advisor hallucination | 2,847 client portfolios affected, $3.2M remediation |
| Jan 2026 | GPTZero ICLR 2026 scan | 50+ papers with hallucinated citations out of 300 scanned (~20,000 total submissions); fabricated authors, wrong attributions, entirely fake references — all missed by 3-5 peer reviewers per paper |
| Early 2026 | Ellis George / K&L Gates brief (C.D. Cal.) | Attorneys submitted hallucinated citations generated across CoCounsel, Westlaw Precision, and Google Gemini without verification |
| Nov 2025 | Google Gemma removal from AI Studio | Generated completely fictitious allegations against US Senator Marsha Blackburn, backed by non-existent news article links |
| Mar 2026 | Amtrust v. Liberty Mutual Insurance (NJ) | Lawyer sanctioned $9,000 for fabricated case law in AI-generated brief |
| Mar 2026 | State v. Coleman (Ohio) | ChatGPT-generated fabricated transcript quotations; $2,000 sanction |
| Mar 2026 | Doiban v. Oregon Liquor & Cannabis Commission | Brief contained 15+ fabricated citations; $10,000 fine |
| Mar 2026 | McCarthy v. DEA (Third Circuit) | Attorney reprimanded for seven AI-generated summaries containing inaccuracies |
| Mar 2026 | Oregon attorney sanction | Single attorney fined **$109,700** for AI-generated fabricated citations — largest individual penalty publicly tracked in Q1 2026 |
| Mar 31, 2026 | Single-day record | **17 U.S. court decisions** in one day noted suspected AI hallucinations in filings; underscores the rate is now daily-scale, not weekly |
| 2026 | E.D.N.C. — DOJ brief | DOJ attorney Rudy Renfer terminated after a pro se plaintiff discovered fabricated quotations in a government brief — hallucination crisis now hits the government side, not just private counsel |

**Legal crisis scale:** **1,227 documented cases globally as of April 2026** (up from 1,213 in late March), with ~5-6 new documented cases per day. **811 cases in the US**; fabricated case law remains the dominant failure mode. **59% involve pro se litigants**, and **90%** come from solo practitioners or firms under 25 attorneys — the crisis is most acute where litigants lack infrastructure for independent verification. Q1 2026 sanctions totaled at least **$145,000** across publicly tracked cases. Five-figure sanctions are now routine; six-figure sanctions have arrived (Oregon: $109,700). Stanford: LLMs hallucinate 75%+ of the time on legal questions about court rulings. 79% of lawyers now use AI tools in practice (ABA TechReport 2025), amplifying hallucination exposure. The OWASP AI Testing Guide 2026 formally includes hallucination testing as a core test category alongside prompt injection and toxic output. BriefCatch launched RealityCheck at Legalweek (March 2026) — the first purpose-built legal citation verification tool combining deterministic database checks with AI-assisted content validation. Florida judicial circuits now require AI disclosure and independent citation verification for court filings.

---

## Domain-Specific Hallucination Rates

| Domain | Average Rate | Critical Risk |
|--------|:----------:|---------------|
| Legal | 18.7% | Fabricated case citations, false quotes |
| Coding | 17.8% | Non-existent APIs, incorrect syntax |
| Scientific | 16.9% | Fabricated references, invented statistics |
| Medical | 15.6% | Wrong dosages, imagined diagnoses |
| Financial | 13.8% | Incorrect figures, fabricated regulations |
| General Knowledge | 9.2% | Incorrect dates, non-existent entities |

Medical context: Clinical vignette hallucination rates of 64-68% without mitigation; 43-45% with mitigation prompts; GPT-4o best case: 23%. ECRI listed AI risks as #1 health technology hazard for 2025.

---

## Related Standards & References

- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — identifies "confabulation" as one of 12 GenAI risks
- [OWASP LLM09:2025 Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/) — replaced "Overreliance"; explicitly covers hallucinations
- [EU AI Act Article 15: Accuracy, robustness and cybersecurity](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-15) — requires high-risk AI systems to meet and document accuracy, robustness, and cybersecurity levels
- [Columbia Journalism Review: AI Search Has a Citation Problem](https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php) — March 2025 Tow Center test of AI search citation accuracy
- [OpenAI Whisper hallucination reporting](https://techcrunch.com/2024/10/26/openais-whisper-transcription-tool-has-hallucination-issues-researchers-say/) — October 2024 reporting on invented transcription content in medical and public-meeting contexts
- [Mata v. Avianca sanctions order](https://law.justia.com/cases/federal/district-courts/new-york/nysdce/1%3A2022cv01461/575368/54/) — primary legal example for fabricated citations and quotations
- [United States v. Hayes](https://caselaw.findlaw.com/court/us-dis-crt-e-d-cal/116862866.html) — January 2025 sanctions order involving a nonexistent case citation
- [Lasso Security: AI Package Hallucinations](https://www.lasso.security/blog/ai-package-hallucinations) — package hallucination research relevant to coding assistants and dependency verification
- [Vectara hallucination evaluation docs](https://docs.vectara.com/docs/hallucination-and-evaluation/hallucination-evaluation) — factual consistency score behavior, threshold guidance, and HHEM 2.3 language support
- [HHEM-2.1-Open on Hugging Face](https://huggingface.co/vectara/hallucination_evaluation_model) — open hallucination evaluation model for premise/hypothesis consistency scoring
- [Ragas Faithfulness metric](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) — claim-level RAG faithfulness metric and HHEM integration
- [Vectara Hallucination Leaderboard](https://github.com/vectara/hallucination-leaderboard)
- [HalluLens Benchmark (arXiv:2504.17550)](https://arxiv.org/html/2504.17550v1)
- [FaithJudge (arXiv:2505.04847)](https://arxiv.org/html/2505.04847v1)
- [Arize LibreEval1.0](https://arize.com/llm-hallucination-dataset/)
- [SelfCheckGPT (Manakul et al., 2023)](https://arxiv.org/abs/2303.08896)
- [FActScore (Min et al., 2023)](https://arxiv.org/abs/2305.14251)
- [RAGAS Framework](https://docs.ragas.io/)
- [FACTUM: Mechanistic Citation Hallucination Detection (ECIR 2026)](https://arxiv.org/abs/2601.05866) — internal pathway analysis for RAG citation hallucination
- [ChainPoll (Friel & Sanyal, 2023)](https://arxiv.org/abs/2310.18344) — CoT-based hallucination detection outperforming SelfCheckGPT, GPTScore, TRUE
- [REFIND: Retrieval-Augmented Factuality Detection (SemEval-2025)](https://arxiv.org/html/2502.13622v2) — token-level hallucination span identification
- [Semantic Entropy for Hallucination Detection (Nature, 2024)](https://www.nature.com/articles/s41586-024-07421-0) — uncertainty estimation via semantic clustering
- [Hallucination Detection with Metamorphic Relations (ACM, 2025)](https://dl.acm.org/doi/10.1145/3715735) — software engineering approach to hallucination testing
- [Comprehensive Survey: Hallucination in LLMs (ACM TOIS, 2025)](https://dl.acm.org/doi/10.1145/3703155) — taxonomy of causes, detection, and mitigation
- [AI Hallucination Cases Database (Charlotin)](https://www.damiencharlotin.com/hallucinations/)
- [AI Hallucination Statistics 2026 (AllAboutAI)](https://www.allaboutai.com/resources/ai-statistics/ai-hallucinations/)
- [HalluGraph: Auditable Hallucination Detection for Legal RAG (arXiv:2512.01659)](https://arxiv.org/abs/2512.01659) — knowledge graph alignment for entity grounding and relation preservation
- [CLAP: Cross-Layer Attention Probing (arXiv:2509.09700)](https://arxiv.org/abs/2509.09700) — fine-grained hallucination detection via activation probing, ECAI 2025
- [MetaQA: Metamorphic Hallucination Detection (ACM, 2025)](https://dl.acm.org/doi/10.1145/3715735) — prompt mutation approach outperforming SelfCheckGPT on closed-source models
- [GPTZero ICLR 2026 Hallucination Report](https://gptzero.me/news/iclr-2026/) — 50+ academic papers with hallucinated citations
- [OWASP AI Testing Guide 2026](https://www.practical-devsecops.com/owasp-ai-testing-guide-explained/) — hallucination testing as core AI security test category
- [AI Hallucination Rates & Benchmarks 2026 (Graffius)](https://www.scottgraffius.com/blog/files/ai-hallucinations-2026.html) — reasoning model paradox analysis
- [Behavioral Calibration RL for Hallucination Mitigation (arXiv:2512.19920)](https://arxiv.org/abs/2512.19920) — training models to abstain or flag uncertainty; 4B model matches frontier calibration
- [MedHallu: Medical Hallucination Benchmark (EMNLP 2025)](https://medhallu.github.io/) — 10K PubMedQA pairs, first domain-specific medical hallucination benchmark
- [FinReflectKG-HalluBench (arXiv:2603.20252)](https://arxiv.org/abs/2603.20252) — GraphRAG hallucination benchmark for financial QA over SEC 10-K filings
- [Datadog LLM Observability Hallucination Detection](https://www.datadoghq.com/blog/llm-observability-hallucination-detection/) — production-grade monitoring with multi-stage detection
- [BriefCatch RealityCheck](https://abovethelaw.com/2026/03/new-tool-catches-ai-hallucinations-in-legal-briefs/) — legal citation verification tool launched March 2026
- [EU AI Act Enforcement Timeline](https://sombrainc.com/blog/ai-regulations-2026-eu-ai-act) — accuracy obligations enforced from August 2026
- [HalluClean: A Unified Framework to Combat Hallucinations in LLMs (AAAI 2026, arXiv:2511.08916)](https://arxiv.org/abs/2511.08916) — Plan-Reason-Judge detect-and-correct pipeline, zero-shot across five task types
- [Adaptive Bayesian Estimation of Semantic Entropy (arXiv:2603.22812, March 2026)](https://arxiv.org/abs/2603.22812) — ~50% sample reduction over fixed-budget semantic-entropy detection via guided semantic exploration
- [Spectral Features of Attention Maps for Hallucination Detection (arXiv:2502.17598, Feb 2026)](https://arxiv.org/html/2502.17598v2) — Laplacian eigenvalue probing
- [Volokh Conspiracy — 17 U.S. Court Decisions in One Day (Apr 2026)](https://reason.com/volokh/2026/04/06/in-one-day-mar-31-17-u-s-court-decisions-noting-suspected-ai-hallucinations-in-court-filings/) — record daily hallucination-sanction count
- [PlatinumIDS — 1,227 Fabricated Citations (April 2026)](https://blog.platinumids.com/blog/ai-hallucination-crisis-courts-2026) — Q1 2026 sanctions breakdown, pro se vs. firm-size analysis
- [Courts Fined Lawyers $145K for AI Hallucinations in Q1 Alone](https://ucstrategies.com/news/courts-fined-lawyers-145k-for-ai-hallucinations-in-q1-alone/) — aggregate Q1 2026 sanction totals
- [AI Hallucination Statistics Research Report 2026 (Suprmind)](https://suprmind.ai/hub/insights/ai-hallucination-statistics-research-report-2026/)

---

## Open Research Questions

- What hallucination rate is acceptable for different risk domains? Is 0.7% (current best on simple benchmarks) adequate for medical or legal use?
- How should confidence thresholds be calibrated when models are frequently updated and calibration shifts?
- Can hallucination detection generalize across domains, or does it require domain-specific training data?
- How should systems handle "confident hallucinations" — the overconfidence paradox (Gemini 3 Pro: 53% accuracy, 88% hallucination rate)?
- Is there a principled way to distinguish creative embellishment (acceptable) from factual fabrication (unacceptable)?
- Should citation verification check URL content or just URL existence? (Perplexity cites real URLs with fabricated claims) FACTUM's mechanistic approach detects citation hallucination internally, but requires white-box access.
- Can LLM-as-Judge approaches be made adversarially robust, or do they introduce a new single point of failure?
- **[New]** How do mechanistic detection signatures (FACTUM) scale across model architectures? Current evidence shows 3B and 8B models use different internal strategies — will this generalize to 70B+ models?
- **[New]** Can span-level hallucination detection (REFIND's token-level CSR) be made fast enough for real-time production use, or is it limited to offline evaluation?
- **[New]** How should retrieval-based and self-consistency approaches be combined? Each catches different hallucination types; no single method dominates across all benchmarks.
- Why do reasoning models (o3, DeepSeek-R1) hallucinate *more* on factual benchmarks than their non-reasoning counterparts? Is chain-of-thought reasoning amplifying confabulation, and can this be mitigated without sacrificing reasoning capability?
- Can graph-theoretic hallucination detection (HalluGraph's Entity Grounding + Relation Preservation) generalize beyond legal domains to medical, financial, and scientific contexts?
- Academic peer review missed 50+ hallucinated citations at ICLR 2026 — should automated citation verification become a mandatory part of scientific publishing pipelines?
- Can behavioral calibration RL (training models to abstain when uncertain) scale to frontier-size models without sacrificing capability? Early results show a 4B model matching frontier calibration — does this transfer to 70B+?
- With the EU AI Act enforcing accuracy requirements from August 2026, how will hallucination benchmarks be standardized for regulatory compliance? Different benchmarks measure fundamentally different failure modes — which should regulators adopt?
- Domain-specific benchmarks (MedHallu for medical, FinReflectKG for financial) expose much higher failure rates than general benchmarks — should hallucination tolerance thresholds be domain-regulated rather than model-regulated?

---

## Related Pages

- [C3.5 Hosted Provider Managed Controls](../C03-Model-Lifecycle-Management/C03-05-Hosted-Provider-Managed-Controls.md) - model ID logging and provider-change gates give hallucination investigations the model provenance they need.
- [C13.3 Model Drift Detection](../C13-Monitoring-and-Logging/C13-03-Model-Drift-Detection.md) - drift monitoring catches changes in hallucination, refusal, grounding, and guardrail behavior after deployment.
- [C14.3 Chain of Responsibility Auditability](../C14-Human-Oversight/C14-03-Chain-of-Responsibility-Auditability.md) - oversight logs help prove who approved high-impact outputs, overrides, and tool-backed decisions.
- [Appendix B References](../../appendices/Appendix-B-References.md) - shared standards and source material for NIST, OWASP, MITRE, EU AI Act, and AI assurance references.
- [C1.1 Training Data Origin Traceability](../C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md) - provenance controls reduce hallucination risk from stale, low-quality, or unverified training and grounding sources.

---

[C07 Index](C07-Model-Behavior.md) | [README](../../README.md)
