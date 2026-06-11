# C11.6: Runtime Context Contamination Detection

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness.md)
> **Requirements:** 4 | **IDs:** 11.6.1--11.6.4

## Purpose

Identify and neutralize manipulated, backdoored, or adversarial data entering the model context at inference time via external sources -- RAG retrieval, tool outputs, MCP server responses, grounding pipelines, and web scraping. Unlike training-time poisoning (covered in C1), inference-time poisoning targets the data a model processes during production use. This is especially relevant for RAG-based systems where retrieved documents, API responses, or user-supplied context can contain adversarial payloads designed to manipulate model behavior -- including indirect prompt injection, factual manipulation, and behavior modification through crafted context.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **11.6.1** | **Verify that** inputs from external or untrusted sources pass through anomaly detection (e.g., statistical outlier detection, consistency scoring) before model inference. | 2 | Poisoned context injection via compromised RAG corpora, malicious tool outputs, or adversarial web content. Without anomaly detection, the model blindly trusts all retrieved or supplied context. MITRE ATLAS AML.T0020 (Poison Training Data) adapted to inference-time context; AML.T0051 (LLM Prompt Injection); AML.T0080 (Memory Poisoning) and AML.T0080.000 (AI Agent Context Poisoning -- Memory), added to ATLAS via the Zenity Labs collaboration; OWASP LLM08:2025 (Vector and Embedding Weaknesses); OWASP LLM01:2025 (Prompt Injection); OWASP Top 10 for Agentic Applications 2026 (ASI) ASI06 Memory & Context Poisoning, which consolidates persistent memory, RAG corpora, embedding indexes, and inter-agent shared context as a unified runtime contamination surface. Attack surface now includes multimodal metadata poisoning (MM-MEPA, February 2026), knowledge-graph triple injection targeting KG-RAG systems, poisoned AI agent tools (MITRE ATLAS v5.4.0, February 2026 added "Publish Poisoned AI Agent Tool"; v5.5.0, March 2026 added "AI Agent Tool Poisoning" and "AI Supply Chain Rug Pull" plus poisoned-MCP-server case studies), Advanced Tool Poisoning Attacks (ATPA) against MCP servers that manipulate what the LLM sees *after* a tool call, and URL-parameter prompt injection into long-term memory via "Summarize with AI" style one-click links. Real-world precedent: the Basilisk Venom attack (January 2025) planted hidden prompts in GitHub code comments that created backdoors in fine-tuned models including DeepThink-R1; AI Recommendation Poisoning (Microsoft Defender Security Research, February 2026) cataloged 50+ live examples across 31 companies in 14 industries using URL parameter prompts to implant "trusted source" and "authoritative" memories into Copilot, ChatGPT, Claude, Perplexity, and Grok within a single 60-day review of email-borne AI links. As of June 2026, black-box attack economics have collapsed: the "Overcoming the Retrieval Barrier" study (arXiv 2601.07072) decomposes malicious documents into retrieval-guaranteeing trigger fragments plus payloads using only embedding-API access, achieving near-100% retrieval across 11 benchmarks and 8 embedding models at roughly $0.21 per target query, with a single poisoned email coercing GPT-4o into SSH-key exfiltration at >80% success in multi-agent workflows; MIRAGE (arXiv 2512.08289) automates query-agnostic corpus poisoning with stealth optimization explicitly designed to evade perplexity and embedding anomaly detectors. The retrieval data layer itself is also exposed: Akamai's May 2026 research disclosed three MCP back-end flaws including CVE-2025-66335 (SQL injection in Apache Doris MCP), an authentication bypass in Apache Pinot MCP, and an unauthenticated information-disclosure in Alibaba RDS MCP that lets any client reaching the endpoint invoke the RAG tool and exfiltrate vector-index metadata -- which Alibaba declined to patch. | Review anomaly detection pipeline for external inputs. Verify detection methods are appropriate for the data type (statistical outlier detection for embeddings, consistency scoring for text, schema validation for structured data). Test with known poisoned inputs and confirm detection. Verify detection is applied before the model processes the input, not after. As of 2026, evaluate hybrid retrieval (combining BM25 + dense vector search) as a first-line defense -- Semantic Chameleon research shows this reduces gradient-optimized poisoning co-retrieval from 38% to 0% at balanced alpha. For web-facing RAG, the simple "three-defense stack" from OpenRAG-Soc / Hidden-in-Plain-Text (January 2026) is a high-value baseline: HTML/Markdown sanitization (strip hidden/off-screen carriers and risky attributes while preserving visible text), NFKC Unicode normalization with control-character stripping (addresses zero-width characters and homoglyphs), and attribution-gated answering (restrict answers to cited spans). Combined, these dropped macro ASR from 24.9% to 4.7% across Social-Web carriers with negligible overhead. Consider post-retrieval filtering with RAGDefender (ACSAC 2025), which uses TF-IDF clustering and concentration-based grouping to isolate adversarial passages without additional LLM inference. For provably robust filtering, ReliabilityRAG (NeurIPS 2025) finds a consistent document majority via Maximum Independent Set on a contradiction graph, with formal guarantees against bounded adversarial corruption. Gradient-based Masked Token Probability (GMTP, ACL Findings 2025) flags adversarial documents by masking the tokens that the retriever's similarity gradient considers most influential and checking whether a masked language model assigns them anomalously low probability -- it removes more than 90% of poisoned content while preserving retrieval utility, and slots in cleanly ahead of generation in existing pipelines. RAGPart and RAGMask (AAAI 2026 NFIR Workshop) operate one layer earlier on the retriever itself: RAGPart partitions documents to dilute poisoned points, and RAGMask scores each token by the similarity shift it induces when masked, demoting documents whose adversarial tokens drive the bulk of retrieval relevance. Both are lightweight, require no generator changes, and complement post-retrieval defenses. For high-assurance domains (government, financial, health) where numerical integrity matters, RAGShield (arXiv 2604.00387, 2026) demonstrates a provenance + cross-source + temporal defense that reached 0.0% ASR across 430 attacks generated from real IRS content while embedding-based defenses failed at 79--90% ASR -- the key insight is that embedding models encode topic, not numerical precision. Attention-based detection is maturing: the Normalized Passage Attention Score (NPAS) with Attention-Variance (AV) Filter reduces attack success rates from ~90% to ~15% at 0.1 corruption rate by quantifying each retrieved passage's influence via aggregated attention weights and iteratively removing anomalous high-attention passages. Amazon Bedrock Guardrails now offers contextual grounding checks that generate confidence scores for grounding and relevance in RAG responses, enabling automated blocking of responses not grounded in source documents. For MCP / agent tool pipelines, deploy a proxy-mode guardrail (e.g., MCP-Scan, Ascend AI, MintMCP, Straiker) that sits between the MCP client and servers, enforcing policy on *both* tool call arguments and tool responses (PII detection, secrets scanning, structural schema checks). NSA's Cybersecurity Information Sheet on MCP (May 20, 2026, U/OO/6030316-26) now gives auditors a government-issued baseline for this check: schema, range, and context validation of every tool invocation before model consumption; logging of all tool and model invocations with exact parameters and cryptographic hashes of outputs; data-classification zoning of tools; and a filtering outgoing proxy/DLP for external MCP connections. For agents with persistent memory, OWASP Agent Memory Guard (v0.3.0, June 2026) screens every memory read/write through detectors for injection markers, secret/PII leakage, protected-key tampering, size anomalies, and self-reinforcement loops, with SHA-256 baseline integrity checks at 59 microseconds median latency; Microsoft's Agent Governance Toolkit (April 2026, MIT-licensed) adds a Cross-Model Verification Kernel that majority-votes across multiple models to catch memory poisoning, plus an MCP security gateway for tool-response screening. The 2026 MCP scanner ecosystem has broadened to include Invariant Labs mcp-scan (the de-facto baseline, supporting tool pinning via SHA-256 hashes of tool descriptions), Cisco mcp-scanner, Snyk agent-scan, Backslash, and Pipelock; OWASP MCP Top 10 (beta, 2026) classifies the matching defense as **schema quarantine** -- treat every newly connected MCP server as untrusted code, statically analyze its tool definitions, test in isolation, and require explicit re-approval whenever a tool description hash changes mid-session, defeating rug-pull edits and schema poisoning. Tools: NVIDIA NeMo Guardrails for retrieval-level filtering, Meta LlamaFirewall (PromptGuard 2 for injection detection, AlignmentCheck for goal-hijacking), LLM Guard for pre-inference screening, Vigil for input pattern detection, Amazon Bedrock Guardrails for contextual grounding, Lakera Guard for managed output-side screening. | Anomaly detection for natural language inputs is inherently difficult -- poisoned text may be semantically valid and statistically indistinguishable from clean text. Indirect prompt injection payloads often look like normal text. Detection effectiveness varies dramatically by input modality. Embedding anomaly detection alone reduced attack success from 95% to 20% in RAG Security Bench (2025) benchmarks, but sophisticated dual-document attacks (Semantic Chameleon, March 2026) can still achieve 20--44% success against hybrid retrieval with joint sparse+dense optimization. Multimodal RAG faces additional risk: MM-MEPA (February 2026) showed metadata-only poisoning achieves 91% attack success on MMQA, and image-metadata consistency checks fail because similarity score distributions for clean and poisoned metadata overlap significantly. NPAS/AV Filter shows promise but adaptive attacks can still achieve up to 35% ASR, albeit at ~1000x computational cost to the attacker. MCPTox (arXiv 2508.14925) showed that ATPA against real MCP servers achieves 72.8% ASR against o1-mini, and refusal rates top out below 3% even on Claude-3.7-Sonnet -- more capable models are often *more* vulnerable because stronger instruction following amplifies the attack. Memory-layer poisoning (Microsoft Feb 2026) evades classical retrieval-level filters entirely: the payload is written once into persistent memory, then retrieved as a trusted fact on every subsequent query. No single detection layer is sufficient; layered defense is not optional. |
| **11.6.2** | **Verify that** anomaly-detection thresholds are tuned on representative clean and adversarial validation sets. | 2 | Miscalibrated detection that either misses poisoned inputs (thresholds too loose) or blocks legitimate inputs (thresholds too tight). Untuned detectors provide a false sense of security. | Review validation datasets used for threshold tuning -- verify they include representative clean data and realistic adversarial examples. Check documented false-positive rates and confirm they are acceptable for the application. Verify that thresholds are re-evaluated when the input distribution changes (new data sources, updated retrieval indices). RevPRAG (2024) offers a complementary approach: it extracts LLM activations from the final token and uses a Siamese network to distinguish poisoned from clean responses, achieving ~98% TPR at ~1% FPR across five LLMs and four retrievers, providing a useful baseline for calibrating downstream detection thresholds. As of June 2026, the largest public adversarial corpus for this purpose comes from a large-scale indirect prompt injection competition (arXiv 2603.15714): 464 participants generated 272,000 attack attempts with 8,648 successful hidden injections across 41 scenarios and 13 frontier models -- the dataset was shared with frontier labs and the UK/US AI Safety Institutes and is precisely the kind of representative adversarial validation set this requirement demands. Stress thresholds against stealth-optimized attacks specifically: MIRAGE's adversarial test-time preference optimization is built to slip under perplexity and embedding-distance thresholds tuned only on older attack generations. | Creating representative adversarial validation sets is difficult and labor-intensive. The adversarial landscape changes rapidly, so validation sets become stale. False-positive rate tolerance depends heavily on the application -- a 1% false-positive rate may be acceptable for a chatbot but not for a medical decision-support system. RevPRAG's activation-based approach shows promising threshold stability across model families (GPT2-XL, Llama 2/3, Mistral), but requires access to model internals and may not apply to API-only deployments. The competition data (arXiv 2603.15714) also showed per-model attack success ranging from 0.5% (Claude Opus 4.5) to 8.5% (Gemini 2.5 Pro) with only weak correlation between model capability and robustness -- so thresholds tuned for one model do not transfer, and must be re-derived per model version. |
| **11.6.3** | **Verify that** inputs flagged as anomalous trigger gating actions (blocking, capability degradation, or human review). | 2 | Detected anomalies that are logged but not acted upon. Detection without response provides no security value. Risk-appropriate gating ensures that the response matches the potential impact of the poisoned input. | Review gating action configuration for flagged inputs. Verify that high-risk use cases have blocking or human review gates. Verify that lower-risk use cases have appropriate degraded-capability responses (e.g., responding without the suspicious context, flagging output as uncertain). Test end-to-end: inject a flagged input and confirm the gating action executes. Evaluate leave-one-out counterfactual testing (RAGuard's zero-knowledge inference patch): temporarily remove each retrieved document and check if answer correctness changes -- documents whose removal corrects a wrong answer are flagged and excluded during final generation. For agent memory, OWASP Agent Memory Guard's YAML policy engine demonstrates the graduated-response pattern this requirement calls for -- detector findings map to allow/redact/quarantine/block actions with structured SecurityEvents for audit, plus forensic snapshot rollback for post-incident recovery; Microsoft's Agent Governance Toolkit ships a stateless policy engine (Agent OS) that intercepts agent actions at sub-0.1 ms p99 latency with YAML, OPA Rego, and Cedar policy languages. NSA's May 2026 MCP guidance frames gating architecturally: data-classification zoning of tools and a filtering outgoing proxy mean unclassified or anomalous flows are blocked by design rather than per-detection. | Blocking may not be the right response in all cases -- for RAG systems, excluding the suspicious document and proceeding with remaining context may be more useful than a hard block. The RAGuard leave-one-out approach provides an elegant selective-exclusion mechanism but requires multiple inference passes, increasing latency proportionally to the number of retrieved documents. Capability degradation must be communicated to the user. Human review gates introduce latency that may not be acceptable for real-time applications. |
| **11.6.4** | **Verify that** the false-positive rate of anomaly detection is measured on representative data and documented per model version. | 2 | Alert fatigue and business disruption from benign RAG documents, tool outputs, memory updates, or user prompts being repeatedly classified as poisoned. A detector with an unknown false-positive rate can cause teams to disable blocking, build unsafe allow-lists, or silently loosen thresholds after model, retriever, embedding, or guardrail changes. EU AI Act Article 15's accuracy, robustness, and cybersecurity language makes this a documentation issue for high-risk systems, not just an engineering preference. | Review the validation report for each deployed detector and model version. Confirm it includes a confusion matrix, false-positive rate, false-negative rate, precision/recall, confidence-score distribution, and per-source breakdowns for normal user prompts, retrieved documents, web content, tool outputs, MCP server responses, memory writes, and multimodal metadata. Verify clean validation data comes from representative production traffic or curated domain corpora, not only generic prompt-injection benchmarks. Require adversarial sets that include sparse RAG poisoning (PoisonedRAG), KG-RAG perturbation triples, indirect prompt injection, tool-output poisoning, schema poisoning and tool-pinning regressions in MCP servers (mapped to OWASP MCP Top 10 MCP03 Tool Poisoning, MCP06 Intent Flow Subversion, and MCP10 Context Injection & Over-Sharing), and benign-but-unusual domain content that should pass. Public benchmark research reports up to 84.2% tool-poisoning attack success against MCP-connected agents with auto-approval enabled, so any deployment that ships with one-click tool acceptance must be measured against that baseline before claiming a meaningful false-positive number. For managed guardrails, inspect the actual thresholds and detector outputs: Amazon Bedrock contextual grounding exposes grounding/relevance confidence scores and configurable thresholds; Lakera Guard documents L1--L4 threshold levels that trade false positives against false negatives; NVIDIA NeMo Guardrails separates input, output, retrieval, and execution rails, so auditors should measure each rail alone and in combination. Re-run the measurement after model, embedding model, retriever, index, parser, sanitizer, prompt template, guardrail policy, or tool-schema changes, and store results with the release artifact. OWASP Agent Memory Guard (June 2026) is a useful reference for what published detector metrics look like: the project documents 92.5% recall, 100% precision, 0% false-positive rate, and F1 0.961 on its public test suite, broken down per detector (injection and protected-key 100%, leakage 83%, size anomaly 80%) -- exactly the per-component disclosure this requirement expects from internal teams and vendors alike. ISO/IEC 27090 (at FDIS as of early 2026, publication expected later in 2026) reinforces the documentation angle: it states plainly that poisoning detection is "often difficult," which supports documenting detector limitations and measured false-positive rates rather than claiming complete coverage. | Published benchmark rates rarely transfer cleanly to a local corpus. RevPRAG reports about 98% TPR and close to 1% FPR across multiple RAG configurations, but it requires model activations and does not solve API-only deployments. Vendor guardrails may expose scores and threshold knobs without publishing domain-specific false-positive behavior. Human labeling of false positives is expensive, especially for legal, medical, code, multilingual, and multimodal content where "suspicious" and "novel but valid" overlap. Low false positives can also hide dangerous false negatives if thresholds are tuned only for user friction. Treat allow-lists and one-off threshold relaxations as temporary exceptions with expiry dates and regression tests. Be skeptical of small-suite perfection: Agent Memory Guard's 0% FPR comes from a 55-case test suite (37 true positives, 3 false negatives) -- a strong signal for a v0.3.0 project, but not evidence of production-scale false-positive behavior across millions of memory writes. |

---

## Recent Research (2024--2026)

### RAG Knowledge Poisoning at Scale

Research from 2025 on **knowledge poisoning attacks to retrieval-augmented generation** demonstrates that RAG systems are highly vulnerable to targeted poisoning even with minimal injection volume. **PoisonedRAG** (USENIX Security 2025) achieved attack success rates of 97% on NQ, 99% on HotpotQA, and 91% on MS-MARCO by injecting only 5 malicious texts per target question into knowledge bases containing millions of texts. This dramatically low injection threshold means that anomaly detection systems (requirement 11.6.1) must operate at individual-document granularity, not just aggregate statistical analysis.

### Expanded Attack Surface: Agents and Tool Outputs

As of 2025-2026, inference-time poisoning now extends beyond RAG corpora to include **MCP server outputs, tool call results, and synthetic data pipelines**. Poisoning can target the entire LLM inference lifecycle: retrieved documents, API responses, web-scraped content, and inter-agent communications. This expanding attack surface means that requirement 11.6.1's anomaly detection must cover all external data ingestion points, not just retrieval pipelines.

### Attention-Based Detection: Attention Tracker

**Attention Tracker** is an emerging defense that detects poisoned inputs by checking whether a retrieved passage diverts attention away from the system prompt in instruction-following attention heads. This approach leverages the internal mechanism by which indirect prompt injections operate -- they hijack attention from the intended instruction to the injected payload. Attention Tracker represents a model-intrinsic detection method that could complement the statistical outlier detection and consistency scoring described in requirement 11.6.1.

### Scalable RAG Poisoning: Eyes-On-Me

**Eyes-On-Me** (October 2025) demonstrates scalable RAG poisoning through attention manipulation, showing that adversaries can craft poisoned documents that specifically target the retrieval and attention mechanisms of RAG pipelines. The attack is designed to maximize retrieval relevance scores for poisoned documents while embedding adversarial payloads, making detection through retrieval-score anomalies unreliable. This reinforces requirement 11.6.2's call for tuning against realistic adversarial validation sets -- detection methods that rely on retrieval-score outliers are specifically evadable, so validation sets must include attention-targeted attacks.

### Corpus-Dependent Poisoning: Semantic Chameleon (March 2026)

**Semantic Chameleon** introduces a dual-document poisoning strategy that highlights how attack effectiveness is deeply tied to the target corpus. The attack uses two coordinated documents: a **sleeper document** (60--70% legitimate content with semantic hooks creating embedding-space proximity) and a **trigger document** (50% benign prefix followed by the malicious payload). This decoupling addresses the conflicting gradient objectives that limit single-document attacks.

Key findings relevant to defenders:
- **Hybrid retrieval (BM25 + dense vector search)** reduced gradient-optimized co-retrieval success to 0% at balanced alpha values -- a strong first-line defense (requirement 11.6.1)
- However, joint sparse+dense optimization can partially overcome this, achieving 20--44% success depending on alpha weighting
- Detection difficulty varies **13--62x between corpus types** -- technical corpora enable stealth, general corpora expose attacks
- **Query Pattern Differential (QPD)** monitoring showed the most robust cross-corpus detection performance, comparing document retrieval frequency on sensitive versus benign queries
- Model-level safety training is necessary but insufficient -- even the most resistant models showed substantial attack success rates without retrieval-level defenses

### RAGuard: Layered Defense Framework (NeurIPS 2025)

**RAGuard** (ResponsibleFM Workshop, NeurIPS 2025) provides a two-layer defense framework specifically designed for RAG poisoning:

1. **Adversarial retriever fine-tuning**: Dense retrievers (e.g., Contriever, BGE) are trained on synthetic poisoned documents -- fabricated facts, contradictions, reasoning traps -- teaching them to downrank malicious passages during retrieval
2. **Zero-knowledge inference patch**: A leave-one-out counterfactual filter that removes each retrieved document temporarily and checks whether answer correctness improves. Documents whose removal corrects a wrong answer are flagged and excluded. This operates without poison labels, making it effective against unseen attack variants

RAGuard's approach is notable because the inference patch catches sophisticated attacks that evade retrieval-level defenses, acting as a safety net for requirement 11.6.3's gating actions. The tradeoff is computational: leave-one-out testing requires N+1 inference passes for N retrieved documents.

### Sparse Document Attention (SDAG, February 2026)

**Sparse Document Attention RAG (SDAG)** takes a different approach by modifying the attention mask at inference time to prevent cross-attention between retrieved documents. In standard causal attention, tokens from different retrieved documents can influence each other -- a mechanism adversarial documents exploit to corrupt outputs.

SDAG implements block-sparse attention that preserves intra-document attention while blocking inter-document attention, requiring only a minimal change to the attention mask with no fine-tuning. Results across Llama, Qwen, and Mistral models show:
- Substantial reductions in Attack Success Rate (ASR) for single-adversarial-document settings, outperforming RAGDefender and Discern&Answer baselines
- When combined with RAGDefender, SDAG achieved state-of-the-art performance on multi-document attack scenarios
- The defense is most effective when adversarial documents are geometrically distant from benign documents in embedding space

This approach is particularly relevant for requirement 11.6.1 because it is lightweight, requires no retraining, and can be deployed alongside existing anomaly detection.

### RAGForensics: Traceback for Poisoned Documents (ACM Web 2025)

**RAGForensics** is the first traceback system for RAG, designed to identify which specific documents in a knowledge base have been poisoned after an attack is suspected. It operates iteratively: retrieve a subset of documents, use a specially crafted prompt to guide an LLM in detecting potential poisoning, and narrow down the contaminated texts. This supports post-incident investigation and complements requirement 11.6.4's documentation mandate -- a traceback capability is what turns a measured detection miss into a corpus cleanup.

### RAGDefender: Post-Retrieval Grouping and Isolation (ACSAC 2025)

**RAGDefender** takes a lightweight, post-retrieval approach to filtering adversarial documents before they reach the generator. Rather than modifying the retriever or the model, it operates as a preprocessing module that classifies retrieved passages into benign and potentially-adversarial groups using two novel strategies:

1. **Clustering-based grouping**: Hierarchical clustering on TF-IDF representations to identify outlier documents that diverge from the retrieval consensus
2. **Concentration-based grouping**: Analysis of document embedding vector distributions to detect passages that break the expected concentration pattern

RAGDefender requires neither supplementary LLM inference nor additional model training, making it notably cheaper than RAGuard's leave-one-out approach. It integrates seamlessly into existing RAG pipelines as a drop-in preprocessing step. When combined with SDAG's block-sparse attention, the pairing achieved state-of-the-art defense performance against multi-document poisoning attacks in 2025 benchmarks.

### ReliabilityRAG: Provably Robust Defense (NeurIPS 2025)

**ReliabilityRAG** introduces a graph-theoretic approach to RAG poisoning defense with formal robustness guarantees. The core idea: construct a contradiction graph where retrieved documents are nodes and edges represent contradictions (detected via Natural Language Inference models), then find the Maximum Independent Set (MIS) -- the largest set of mutually non-contradictory documents. A weighted variant explicitly prioritizes higher-reliability documents based on source reputation signals (e.g., search engine ranking).

Key advantages over heuristic defenses:
- **Provable guarantees**: Mathematical bounds on defense effectiveness given a maximum number of adversarial documents in the retrieval set
- **Scalable**: A weighted sample-and-aggregate framework handles large retrieval sets while preserving robustness
- **Long-form generation**: Outperforms prior robustness-focused methods on long-form generation tasks where document exclusion can hurt completeness
- **Web-search specific**: Particularly well-suited for RAG-based search applications (Google AI Overviews, Perplexity, Bing Copilot) where built-in reliability signals are available

### RevPRAG: Activation-Based Poisoning Detection (2024)

**RevPRAG** takes a fundamentally different approach to poisoning detection by monitoring the LLM's own internal state. It extracts activations from the final token across all model layers during response generation, then trains a Siamese network (ResNet18 architecture with triplet margin loss) to distinguish activation patterns produced by poisoned versus clean responses.

Performance across five LLMs (GPT2-XL, Llama 2-7B/13B, Mistral-7B, Llama 3-8B) and four retrievers on three QA datasets:
- **True Positive Rate**: ~98% across configurations
- **False Positive Rate**: ~1%

This is relevant for requirement 11.6.2's threshold tuning because RevPRAG provides a model-intrinsic signal that can calibrate external detection thresholds. The limitation is that it requires access to model internals (activations), ruling out API-only deployments.

### False-Positive Measurement and Guardrail Thresholds (2025--2026)

False-positive measurement is becoming a practical audit requirement because production defenses increasingly expose configurable thresholds rather than binary "secure/insecure" settings. Amazon Bedrock Guardrails' contextual grounding check returns grounding and relevance confidence scores with configurable thresholds from 0 to 0.99, but AWS also notes the check is output-side and requires grounding source, query, and guarded content. That makes it useful for measuring hallucination or poisoned-context effects, but not a substitute for pre-inference input screening.

Lakera Guard's policy model is explicit about the operational tradeoff: L1 is lenient with very few false positives, while L4 is paranoid with higher false positives and fewer false negatives. For 11.6.4, that means an auditor should not just see "Lakera enabled" or "guardrails enabled"; they should see which threshold level is active per route, why that setting matches the risk tolerance, and how false-positive overrides are reviewed and expired.

NVIDIA NeMo Guardrails separates input, output, retrieval, and execution rails, including checks for tool inputs and tool outputs. This is important for runtime contamination detection because a clean user prompt can still become unsafe after retrieval or after an MCP/tool response. Measure false positives per rail and for the combined pipeline; otherwise one noisy retrieval rail can get disabled even if the input and output rails are performing well.

The strongest research baselines remain environment-dependent. RevPRAG's ACL Findings 2025 version reports roughly 98% true-positive rate with close to 1% false-positive rate, but only where the defender can access model activations. For API-only deployments, the comparable evidence usually has to come from black-box replay suites, production shadow-mode runs, and manual review of blocked events.

### Multimodal RAG Poisoning: MM-MEPA (February 2026)

**MM-MEPA** (Hidden in the Metadata) reveals that multimodal RAG systems have a largely undefended attack surface: text metadata associated with images. Rather than altering images directly, adversaries modify captions, alt-text, and tags using a Constrained Metadata Optimization (CMO) framework that balances retrieval relevance with semantic consistency.

Results across four retrievers (CLIP, FLAVA, OpenCLIP, SigLIP) and two generators (BLIP-2, LLaVA):
- Attack success rates exceeding **91% on MMQA** with accuracy drops of 27%
- Poisoned metadata retrieved in top-k results **35--90%** of the time
- Standard defenses (query paraphrasing, image-metadata consistency checks) proved largely ineffective because similarity score distributions for clean and poisoned metadata overlap significantly

This finding is particularly concerning for requirement 11.6.1: organizations running multimodal RAG need to extend anomaly detection to metadata channels, not just the visual or textual content itself.

### Knowledge Graph RAG Poisoning (2025)

Recent work conducted the first systematic security evaluation of **knowledge-graph-based RAG (KG-RAG)** systems under data poisoning. The attack strategy identifies adversarial target answers and inserts perturbation triples to complete misleading inference chains within the knowledge graph. Key characteristics:

- **Black-box threat model**: Attacker has no access to the retriever, LLM, or internal KG-RAG parameters -- only the target question
- **Stealth**: All inserted triples use entities and relations already present in the KG, avoiding new-entity detection
- **High retrieval coverage**: At least one adversarial triple is retrieved in over 90% of attacked questions
- Tested against GPT-5.3, GPT-4o, Claude Sonnet 4.6, and Llama 4

This extends the inference-time poisoning threat model beyond text-based RAG to structured knowledge retrieval, and implies that requirement 11.6.1's anomaly detection should include graph-level consistency checks for KG-RAG deployments.

### GGUF Template Poisoning: Inference Scaffolding as Attack Surface (2025)

Research by Splunk and Pillar Security examined a subtle form of inference-time poisoning that targets **model metadata rather than retrieved documents**. GGUF model files can embed chat templates, system prompts, and response prefixes in metadata fields that execute silently during inference. An analysis of ~156,000 GGUF models (219,000 files across 2,500+ accounts) on Hugging Face cataloged the landscape:

- 24 unique chat template values and 5 tool-use entries identified
- While all examined templates appeared benign, the attack surface is real: adversarial instructions in templates would affect every inference without touching the retrieval pipeline
- A Rust-based scanner using HTTP Range requests can inspect metadata in ~10 seconds per repository

This represents a blind spot for requirement 11.6.1's anomaly detection, which typically focuses on retrieved documents and tool outputs. Organizations deploying open-weight models should add inference scaffolding inspection to their detection perimeter.

### Meta LlamaFirewall: Production Guardrail Framework (2025)

**Meta LlamaFirewall** is an open-source guardrail system used in production at Meta, built specifically for securing AI agents. It provides three integrated components relevant to inference-time poisoning defense:

1. **PromptGuard 2**: BERT-based injection detector (86M parameter full model, 22M lightweight variant) with state-of-the-art jailbreak and prompt injection detection, operating in real time with multilingual support
2. **AlignmentCheck**: Chain-of-thought auditor powered by Llama 4 Maverick that inspects agent reasoning traces for indirect prompt injection and goal hijacking -- directly applicable to detecting poisoned context that redirects agent behavior
3. **CodeShield**: Static analysis engine for LLM-generated code across eight languages

LlamaFirewall achieved over 90% efficacy in reducing attack success rates on the AgentDojo benchmark. Its modular architecture allows deployment at the output-guardrails layer (layer 5 in the defense architecture) while AlignmentCheck can serve as an attention-level monitor (layer 4).

### Defense Architecture Considerations

As of early 2026, research has converged on a multi-layer detection architecture. RAG Security Bench (Wang et al., 2025) -- the most comprehensive evaluation to date, testing 13 poisoning methods across 5 datasets with 7 defense mechanisms -- found that hybrid defenses outperform single-mechanism approaches but still leave residual risk. When all five defense layers are active simultaneously, residual risk drops to approximately 10%:

1. **Retrieval-level filtering**: Hybrid retrieval (BM25 + dense vector search), embedding anomaly detection, source reputation scoring, ReliabilityRAG's contradiction-graph filtering. Tools: NVIDIA NeMo Guardrails, Prompt Security
2. **Post-retrieval isolation**: RAGDefender's TF-IDF clustering and concentration-based grouping to filter adversarial passages before generation, without additional LLM inference
3. **Context-assembly validation**: Consistency checking across retrieved passages, detecting contradictions or instruction-like content in data passages. SDAG's block-sparse attention prevents cross-document contamination
4. **Counterfactual testing**: Leave-one-out inference (RAGuard) to identify documents that causally contribute to incorrect outputs
5. **Activation and attention monitoring**: RevPRAG's activation-based poisoning detection (~98% TPR), runtime attention pattern monitoring for instruction-hijacking signatures (Attention Tracker), QPD monitoring for anomalous retrieval patterns
6. **Output-level guardrails**: Post-generation checks for outputs that deviate from expected behavior given the original query. Tools: Meta LlamaFirewall (PromptGuard 2 + AlignmentCheck), LLM Guard, Vigil, Lakera Guard

This six-layer approach maps to requirements 11.6.1 (detection at layers 1-2), 11.6.3 (gating actions at layers 2-4), and supports 11.6.4's per-version measurement mandate by enabling independent false-positive evaluation of each layer. As of March 2026, the addition of post-retrieval isolation (RAGDefender) and activation monitoring (RevPRAG) closes gaps that existed in the earlier five-layer model.

### Attention-Aware Defense: NPAS and AV Filter (2025--2026)

**Through the Stealth Lens** introduces a complementary attention-based defense approach built on the insight that poisoned passages must disproportionately influence the model's response -- and this influence is measurable through attention weights. The defense has two components:

1. **Normalized Passage Attention Score (NPAS)**: Aggregates token-level attention weights across all decoder layers and heads to quantify each retrieved passage's influence on the generated response. For each passage, it sums attention from response tokens to the top-α most-attended tokens within that passage, then normalizes across all passages. Poisoned passages that steer the response show anomalously high NPAS values.

2. **Attention-Variance (AV) Filter**: Iteratively removes passages with the highest attention scores until the variance of normalized attention scores drops below a threshold δ or a maximum fraction ε of passages has been removed. Passages are reordered by attention score before filtering to mitigate transformer position bias.

Tested on Llama2-7B-Chat, Mistral-7B-Instruct, and GPT-4o across Natural Questions, HotpotQA, and RealtimeQA datasets, the AV Filter reduced attack success rates from ~90% to ~15% at 0.1 corruption rate against both PoisonedRAG and Prompt Injection Attack (PIA). The defender identified corrupted retrievals with 0.83 average accuracy. Clean accuracy impact was modest: a 4--6% drop from undefended baseline.

Critically, the authors also developed adaptive attacks that attempt to minimize attention variance in poisoned passages. These adaptive attacks achieved a maximum 35% ASR (average 22%), but at approximately 1000x the computational cost of non-adaptive attacks -- a single H100 GPU required 4.3 days for just 20 queries. This cost asymmetry favors defenders in practice.

This approach is particularly relevant for requirement 11.6.1 because it operates at inference time with no retraining, complements statistical anomaly detection with a mechanistic signal, and provides a detection layer that is orthogonal to retrieval-level defenses like hybrid search or RAGDefender.

### Synthetic Data Poisoning Propagation: VIA (NeurIPS 2025)

**Virus Infection Attack (VIA)**, presented as a NeurIPS 2025 Spotlight paper, reveals a concerning propagation mechanism: poisoning that persists and spreads through synthetic data generation pipelines. When organizations use LLM-generated synthetic data for fine-tuning, augmentation, or evaluation, poisoning payloads from an upstream model can infect downstream models even when the downstream queries are entirely clean.

VIA works by concealing the poisoning payload within a protective "shell" and strategically searching for optimal hijacking points in benign samples to maximize the likelihood of generating malicious content. The attack achieves approximately 70% inheritance rate in downstream models -- meaning poisoning in an upstream model propagates to downstream fine-tuned models at high fidelity.

This has direct implications for inference-time poisoning detection (requirement 11.6.1): organizations that incorporate synthetic data into RAG knowledge bases or use LLM-generated content as training signal (as described in C11.9.5) must treat synthetic data pipelines as a poisoning vector. Detection systems should monitor not just external inputs but also internally generated content for distribution shifts and adversarial patterns.

### Real-World Incident: Basilisk Venom (January 2025)

The **Basilisk Venom** attack demonstrated that inference-time poisoning concepts translate directly to real-world exploitation. Adversaries planted hidden prompts within code comments in popular GitHub repositories. When DeepSeek's DeepThink-R1 was fine-tuned on contaminated repositories, it acquired a backdoor that activated upon encountering specific code patterns during inference.

Key characteristics of this incident:
- **Stealth**: Malicious prompts were embedded in code comments, which typically survive fine-tuning preprocessing filters
- **Delayed activation**: The poisoning effect only manifested months later when specific trigger patterns appeared in user queries
- **Scale**: The attack targeted popular ML repositories with high downstream usage, maximizing the infection radius

This incident underscores that the threat model behind requirement 11.6.1 is not theoretical -- adversaries are actively exploiting inference-time poisoning vectors in production systems.

### MITRE ATLAS v5.4.0: Agent-Specific Attack Techniques (February 2026)

The February 2026 MITRE ATLAS v5.4.0 release expanded the taxonomy to 16 tactics, 84 techniques, and 56 sub-techniques (up from 15 tactics and 66 techniques in October 2025), with 42 real-world case studies. Notable additions relevant to inference-time poisoning:

- **Publish Poisoned AI Agent Tool**: Adversaries create malicious versions of legitimate MCP tools that appear safe but execute harmful actions when invoked. This extends the inference-time poisoning attack surface from retrieved documents to the tool layer -- a poisoned MCP server response is functionally equivalent to a poisoned RAG document from the model's perspective.
- **Escape to Host**: Techniques for breaking out of agent sandboxes, which can be combined with inference-time poisoning to escalate impact.

These additions reflect the framework's shift from model-centric to execution-layer threat coverage. For requirement 11.6.2's adversarial validation mandate, organizations should map their detectors against the expanded ATLAS taxonomy to identify coverage gaps, particularly around tool-output poisoning and agent orchestration attack paths.

ATLAS kept moving through spring 2026. **v5.5.0 (March 31, 2026)** added 12 techniques including **AI Agent Tool Poisoning**, **AI Supply Chain Rug Pull**, and Machine Compromise variants, plus five case studies including poisoned-MCP-server exploits; **v5.6.0 (May 4, 2026)** added reconnaissance techniques such as Acquire Public AI Artifacts: AI Agent Configuration. The **May 27, 2026 release** then overhauled the data model itself: a new content-versioning scheme (YYYY.MM.N, so this release is v2026.05), normalized object modeling, first-class relationships, a REST API, and a `platforms` field that tags techniques as Predictive AI, Generative AI, Agentic AI, or Enterprise. Detection-engineering teams mapping 11.6.1 detectors to ATLAS techniques can now filter programmatically by the Agentic AI platform tag instead of maintaining hand-curated technique lists -- and any documentation hardcoding "v5.4.0" as the current release is already two content releases behind.

### Amazon Bedrock Guardrails: Contextual Grounding for RAG (2025--2026)

As of early 2026, **Amazon Bedrock Guardrails** provides contextual grounding checks specifically designed for RAG applications. The system generates confidence scores for both grounding (is the response factually consistent with the source documents?) and relevance (does the response address the user's query?), with configurable thresholds that can block or flag responses that fall below acceptable scores.

While contextual grounding is primarily positioned as a hallucination defense, it has direct applicability to inference-time poisoning: a poisoned document that steers the model toward adversarial outputs will often produce responses that are not grounded in the legitimate retrieved passages, triggering the grounding check. This makes Bedrock Guardrails a practical output-level defense (layer 6 in the defense architecture) for organizations already on AWS infrastructure. The limitation is that sophisticated poisoning attacks designed to maintain semantic consistency with legitimate content may not trigger grounding violations.

### Data Poisoning Across the LLM Lifecycle (2026 Perspective)

Lakera's 2026 analysis emphasizes that data poisoning risks now span pre-training, fine-tuning, RAG, and agent tooling. Runtime detection systems must track output distributions for sudden shifts, monitor unexpected tool usage patterns in agent systems, and create alerts for responses that deviate from expected norms. This holistic view supports requirement 11.6.2's expectation that validation sets and thresholds are re-evaluated as the input distribution and threat landscape change.

### AI Recommendation Poisoning: Memory Layer as Attack Target (Microsoft, February 2026)

Microsoft's Defender Security Research team documented a live, at-scale campaign targeting persistent memory in consumer AI assistants. Over a 60-day observation window of AI-related URLs in email traffic, researchers identified **more than 50 distinct examples** of the technique originating from **31 companies spanning 14 industries** including finance, healthcare, legal services, and SaaS. The attack is now formally catalogued as **AML.T0080 Memory Poisoning** and its AI Agent Context Poisoning (Memory) sub-technique AML.T0080.000 in MITRE ATLAS.

The mechanics are deceptively simple: attackers craft "Summarize with AI" buttons and AI-share URLs whose query-string parameters (e.g., `?q=`, `?prompt=`) contain pre-filled prompts. When a user clicks, the AI assistant -- Copilot, ChatGPT, Claude, Perplexity, Grok -- executes the embedded instruction as though the user had typed it. Observed payloads instruct the assistant to remember specific domains as "trusted sources", treat third-party websites as "authoritative" on particular topics, or bias future recommendations toward specified financial, cloud, or health services. Publicly available tooling such as CiteMET NPM Package and AI Share URL Creator makes the attack trivially reproducible.

Key implications for inference-time poisoning defenses:
- **Memory is a first-class attack surface.** A single poisoned interaction writes a payload that is subsequently retrieved as a trusted fact on every downstream query, fully bypassing per-turn retrieval filters.
- **URL-parameter prompt pre-population is a one-click delivery vector** that moves poisoning out of corpora and into user click-streams -- making email, chat-message, and browser-based defenses (URL scanning, prompt-keyword detection in parameters like "remember", "trusted", "authoritative", "citation") load-bearing controls for requirement 11.6.1.
- **Downstream blast radius is commercial.** Microsoft's example scenario -- a CFO receiving a vendor recommendation biased by an earlier memory injection, leading to a multi-year contract -- illustrates that this is not a lab-bench concern.

Organizations operating agents with persistent memory should implement write-time provenance for every memory entry, periodic red-team review of stored memories, and alerting on memory-write patterns that match known poisoning phrasing.

### Advanced Tool Poisoning Attacks (ATPA) and MCPTox

ATPA is a class of attack that targets the gap between the MCP protocol's simplistic trust model and the LLM's complex post-tool-call reasoning. Rather than poisoning the prompt or the retrieved document, the attacker manipulates **tool output content** -- particularly dynamic content like error messages, follow-up prompts, or streamed responses -- that the LLM processes after a tool call. Because most guardrails inspect input-side content (system prompts, user prompts, retrieved documents), ATPA fully evades input-side filtering.

**MCPTox** (arXiv 2508.14925, 2025) is the first benchmark for tool-poisoning attacks on real-world MCP servers. Headline results:

- **o1-mini**: 72.8% attack success rate under ATPA
- **Highest refusal rate (Claude-3.7-Sonnet)**: <3%
- Counter-intuitive finding: **more capable models are often more vulnerable**, because stronger instruction-following amplifies the attacker's post-tool-call directive

Defensive response patterns from the MCP ecosystem (2026):
- **Proxy-mode scanners** (MCP-Scan, Ascend AI, MintMCP, Straiker) sit between the MCP client and servers, enforcing policy on both tool call arguments *and* tool responses -- PII detection, secrets scanning, structural schema validation, and custom allow/deny rules
- **Continuous red-teaming** against connected MCP servers to surface rug-pull tool-definition changes and privilege escalation pathways before they are exploited
- **Response-side content filters** mirroring the input-side guardrails already in place, closing the asymmetry that ATPA exploits

### OWASP MCP Top 10 (Beta, 2026): Schema Quarantine and Tool Pinning

The **OWASP MCP Top 10** entered Phase 3 (Beta Release and Pilot Testing) in 2026, with **MCP03 Tool Poisoning** as the dedicated entry for inference-time poisoning that originates from tool definitions and tool responses. The category bundles three sub-techniques: **rug pulls** (malicious updates to a previously trusted tool description), **schema poisoning** (manipulating the type/contract metadata so a benign-sounding operation maps to a destructive action), and **tool shadowing** (introducing fake or duplicate tools that intercept calls intended for legitimate ones). MCP06 Intent Flow Subversion and MCP10 Context Injection & Over-Sharing extend this to multi-step plans and persistent agent context.

The recommended baseline defenses are operationally concrete and map directly to requirement 11.6.1's "before model inference" timing:

- **Schema quarantine** -- treat every newly connected MCP server as untrusted code. Statically analyze its tool definitions against known attack patterns, execute it in a sandboxed dry run, and compare against a baseline before exposing it to live agents.
- **Tool pinning with cryptographic hashes** -- compute a SHA-256 hash of each tool description at first approval and reject any session in which the hash changes. Invariant Labs **mcp-scan** implements this pattern and was the first MCP scanner to ship rug-pull detection on top of cross-origin and prompt-injection checks. Cisco mcp-scanner, Snyk agent-scan, Backslash, and Pipelock implement the same hashing pattern with different policy engines and integration points.
- **Auto-approval kill-switch** -- public benchmark data from 2026 reports tool-poisoning attack success rates around **84.2%** against MCP-connected agents with auto-approval enabled, versus a much smaller surface when every new or modified tool requires explicit user confirmation. This is now the dominant single configuration setting an auditor should look for.

This framework is directly relevant to requirements 11.6.1 (schema quarantine and pinning are pre-inference anomaly checks against tool-side poisoning) and 11.6.3 (the gating action for a mismatched hash is, by design, a hard block rather than capability degradation).

### MCP STDIO Supply-Chain RCE (OX Security, April 2026)

OX Security's April 2026 disclosure widened the inference-time poisoning threat model beyond data and tool descriptions into **the MCP runtime itself**. The flaw is architectural rather than implementation-specific: Anthropic's official MCP SDKs in Python, TypeScript, Java, and Rust permit configuration-to-command execution via the STDIO interface, so any process command passed through that interface executes on the host -- regardless of whether the called process is a valid MCP server.

Reported scale (April 15, 2026):

- 150M+ SDK downloads across language ecosystems
- 7,000+ publicly accessible MCP servers, with up to 200,000 vulnerable instances overall
- 10+ CVEs (Critical and High severity) filed against named projects
- Four exploitation families: unauthenticated UI injection, prompt injection into MCP configuration, malicious marketplace distribution (9 of 11 MCP registries affected), and direct STDIO command injection
- Six live production platforms compromised in proof-of-concept runs
- Affected products include LiteLLM, LangChain, IBM LangFlow, GPT Researcher, Agent Zero, Fay Framework, Bisheng, Langchain-Chatchat, Windsurf, Cursor, DocsGPT, and Upsonic

Anthropic declined to alter the protocol's architecture, citing the behavior as "expected," so mitigation responsibility falls to integrators and ecosystem scanners. For requirement 11.6.1, this widens the anomaly-detection surface to include the **MCP transport layer** -- configuration files, registry metadata, and tool launch commands -- not only retrieved documents and tool outputs. For 11.6.3, gating actions should include configuration-change re-approval (the lesson taught by CVE-2025-54136 in Cursor, where a swap of an already-approved MCP config gained RCE) and, in higher-assurance deployments, signed MCP configurations stored with provenance similar to RAGShield's signed-document approach.

Two additional 2026 CVEs that ship in the same threat class and should be part of any pinning / quarantine baseline:

- **CVE-2026-26118 -- Microsoft MCP server tool hijacking** (CVSS 8.8, fixed in the March 10, 2026 Patch Tuesday cycle). The flaw let an attacker manipulate tool invocation requests and inject responses inside an MCP-mediated workflow, effectively turning a "trusted tool" into an inference-time poisoning channel. For 11.6.1 this reinforces the point that response-side validation is not optional even on first-party (Microsoft-published) MCP servers.
- **CVE-2026-33032 -- nginx-ui MCP-invocable Nginx takeover** (April 2026). The bug allowed an attacker to invoke MCP tools that rewrote Nginx configuration files, intercept all traffic, and harvest administrator credentials. The relevance to runtime context contamination is that any MCP-callable tool with privileged side effects (config writes, certificate management, secrets stores) is now part of the inference-time attack surface for any agent that retrieves or generates content from that infrastructure.

### OWASP Top 10 for Agentic Applications (ASI06 Memory & Context Poisoning, 2026)

The **OWASP Top 10 for Agentic Applications (ASI) 2026** (released December 2025 by the OWASP GenAI Security Project) is the first OWASP framework to dedicate a top-level category to runtime context contamination at the agent layer. **ASI06 Memory & Context Poisoning** explicitly covers persistent memory stores, embedding indexes, RAG corpora, and inter-agent shared context as a unified attack surface, and articulates a defense baseline that maps almost one-to-one to 11.6.1--11.6.4:

- **Per-tenant memory segmentation** -- memory writes from one principal cannot influence retrievals scoped to another. This is the agent-layer analogue of 11.6.1's "before model inference" timing for retrieval-stage filtering.
- **Expiry of unverified data** -- newly written memories carry a verification status, and unverified entries expire on a defined schedule rather than persisting silently. This closes the asymmetry that AML.T0080 exploits, where a single poisoned interaction writes a payload that is then trusted indefinitely.
- **Provenance tagging** -- every memory entry, retrieved document, and tool response carries metadata about origin, write authorization, and trust class, and that metadata is propagated into downstream retrieval and answer-generation steps. Provenance is the only defense that survives memory-layer attacks where the payload becomes a "trusted fact" on every subsequent query.
- **Trust-weighted retrieval** -- retrievers re-rank by trust class, not only embedding similarity, so a poisoned but topically relevant document is demoted below verified sources.

Microsoft's March 2026 walkthrough of how Copilot Studio addresses the new ASI top 10 is a useful reference implementation: provenance and segmentation are wired into the same telemetry layer used for tenant isolation and DLP, so the same audit query answers both "did a memory get poisoned" and "did this tenant ever see another tenant's data." For 11.6.4, the practical implication is that ASI06 false-positive measurement now needs per-trust-class breakdowns -- a 1% FPR on "verified internal" sources is very different from a 1% FPR on "unverified social-web" sources.

### Long-Term Memory Security Survey: Mnemonic Sovereignty (April 2026)

**A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty** (arXiv 2604.16548, April 2026) is the first end-to-end treatment of agent memory as a controlled lifecycle rather than a single attack surface. The authors organize threats and defenses across **six lifecycle phases** -- Write, Store, Retrieve, Execute, Share, and Forget/Rollback -- cross-tabulated with **four security objectives** -- integrity, confidentiality, availability, and governance. Two observations from the survey directly inform requirement 11.6.1's detection timing:

- The literature still concentrates almost entirely on **write- and retrieve-time integrity attacks**. Execute- and share-phase contamination (poisoned memory being passed between agents in a multi-agent workflow, or being read into a tool call argument) has comparatively little detection tooling, and the survey flags this as the dominant open gap for production agent stacks in 2026.
- "Mnemonic sovereignty" -- the principle that the agent operator controls *what may be written* and *when an update is authorized* -- is the structural property anomaly detection has to enforce. A detector that scores retrieval payloads but not memory writes is, in the framework's terminology, sovereign over storage but not over authorship, and is therefore bypassed by AML.T0080-style memory injection.

For 11.6.1, the survey provides a checklist: an inference-time poisoning defense should be measurable independently at the Write phase (does this memory entry have valid provenance and authorization?), the Retrieve phase (is this passage anomalous relative to the corpus?), the Execute phase (does the retrieved content match the requested tool semantics?), and the Forget/Rollback phase (can a poisoned entry be removed deterministically once identified?). Most current stacks cover at most two of the four.

### Benchmarking Inference-Time Defenses: 847-Case Prompt Injection Suite (November 2025)

**Securing AI Agents Against Prompt Injection Attacks** (arXiv 2511.15759, Ramakrishnan and Balaji, November 2025) is one of the first publicly released benchmarks structured for direct use in 11.6.2 threshold tuning and 11.6.4 false-positive measurement. The suite contains **847 adversarial test cases across five attack categories** -- direct injection, context manipulation, instruction override, data exfiltration, and cross-context contamination -- evaluated against seven state-of-the-art language models with three layered defenses (embedding-based content filtering, hierarchical system prompt guardrails, and multi-stage response verification).

Headline empirical results:

- **Undefended baseline ASR**: 73.2% across the seven models
- **Combined defense ASR**: 8.7% (an 8.4x reduction)
- **Clean-task retention**: 94.3% of standard task performance preserved -- a useful upper bound on the utility cost of stacking input, output, and retrieval rails simultaneously

For requirement 11.6.2, this is one of the few public datasets that includes both the adversarial inputs and the labeled benign-but-similar inputs needed to characterize false-positive distributions. For 11.6.4, it allows defenders to report per-attack-category false-positive and false-negative rates rather than a single aggregate number, which is the audit-grade evidence the EU AI Act Article 15 documentation effectively requires. The dataset and defense implementation were released alongside the paper, which means there is now a reproducible reference point for "what 'tuned on representative adversarial validation sets' should look like" -- replacing the prior practice of bespoke internal corpora that are hard to defend in third-party review.

### OpenRAG-Soc / Hidden-in-Plain-Text: Simple Defenses, Large Wins (January 2026)

**OpenRAG-Soc** (arXiv 2601.10923) is a compact, reproducible benchmark for web-facing RAG under indirect prompt injection from social-web carriers (blog posts, forum replies, social media content). It evaluates three low-cost, deployable defenses in combination:

1. **HTML/Markdown sanitization** -- strips hidden or off-screen carriers and risky attributes while preserving visible text (production-grade sanitizer)
2. **NFKC Unicode normalization** with control-character stripping -- addresses zero-width character, homoglyph, and bidirectional-override obfuscation
3. **Attribution-gated answering** -- restricts the generator to content that can be cited from retrieved passages

Results across sparse and dense retrievers:
- Vanilla RAG baseline: **24.9% macro average ASR** across Social-Web carriers
- All three defenses combined: **4.7% macro average ASR**
- Overhead: inconsequential latency and utility cost

The paper is notable because it quantifies that basic web-hygiene practices most RAG deployments skip provide approximately a 5x reduction in attack success with negligible cost -- a high-yield, low-effort baseline for requirement 11.6.1.

### Retriever-Stage Filtering: GMTP, RAGPart, and RAGMask

A second wave of 2025--2026 defenses pushes detection upstream into the retriever itself rather than relying on post-retrieval clustering or generator-side checks.

**GMTP -- Gradient-based Masked Token Probability** (ACL Findings 2025) inspects the retriever's similarity function to identify the tokens whose gradients contribute most to a document's relevance score, masks them, and queries a masked language model for replacement probabilities. Adversarial tokens (gibberish optimization triggers, low-frequency injection markers, malformed Unicode) consistently receive anomalously low MLM probabilities while legitimate high-impact tokens remain plausible. GMTP eliminates over 90% of poisoned content across diverse adversarial settings without harming retrieval utility, and runs entirely on the retriever side -- no LLM call required during filtering.

**RAGPart** and **RAGMask** (AAAI 2026 NFIR Workshop, arXiv 2512.24268) take complementary retriever-stage approaches. RAGPart leverages dense-retriever training dynamics by partitioning the document set during retrieval so that adversarial documents lose their dominance over any single partition. RAGMask scores tokens by the similarity shift induced under targeted masking, then downranks documents whose retrieval relevance hinges on adversarially placed tokens. Evaluated across four retrievers (Contriever, DPR, BGE, E5) and four attack families, both methods reduce attack success rates while preserving clean-corpus utility, and impose only modest latency overhead at retrieval time.

These approaches are notable because they (a) require no fine-tuning of the generator, (b) operate before any LLM inference, and (c) compose with later-stage defenses such as RAGDefender, SDAG, and NPAS/AV. For requirement 11.6.1, GMTP and RAGMask are particularly attractive when the retriever pipeline is the only component under the defender's control -- a common situation for teams that consume managed LLM APIs.

### RAGShield: Provenance-Verified Defense-in-Depth for Numerical Integrity (2026)

**RAGShield** (arXiv 2604.00387, 2026) targets a specific high-assurance use case: government citizen-facing RAG systems (tax guidance, benefits eligibility, legal information). The paper identifies 89 citizen-facing RAG services across 28 federal agencies and shows that conventional defenses fail to catch the attack class that matters most here -- insider adversaries with valid credentials who subtly modify numerical values in authoritative knowledge bases.

Four-layer architecture:
1. **Provenance verification** -- blocks unsigned or forged documents at ingestion
2. **Numerical claim extraction** -- identifies structured (entity, attribute, value, unit) tuples via two-pass entity resolution
3. **Cross-source verification** -- compares extracted values against a multi-source registry built from the corpus
4. **Temporal tracking** -- flags value changes outside authorized government update schedules

Evaluation on 2,742 passages from five IRS publications and 430 generated attacks:
- **RAGShield: 0.0% ASR across all attack tiers including adaptive attacks**, with 0.0% false positive rate
- **Embedding-based defenses: 79--90% ASR** on the same attack set
- **Existing RAG defenses (RobustRAG, TrustRAG, RAGPart): all failed to detect numerical manipulation**

The key insight: embedding models encode topic similarity, not numerical precision. For any RAG use case where "$4,750 deduction" vs "$5,470 deduction" matters more than topic similarity, structural claim extraction plus cross-source verification dramatically outperforms semantic anomaly detection. This pattern generalizes beyond government use cases to healthcare (dosage values), finance (rate tables), and engineering (tolerances).

### MITRE ATLAS Agent-Specific Techniques via Zenity Labs Collaboration

Expanding on the v5.4.0 additions mentioned above, the Zenity Labs collaboration with MITRE ATLAS (first release 2025, expanded through 2026) brought agent-focused attack techniques from the community GenAI Attacks Matrix into the official ATLAS taxonomy. The newly incorporated techniques most relevant to inference-time poisoning defense:

- **AI Agent Context Poisoning (AML.T0080)** -- manipulating the context used by an agent's LLM to persistently influence its responses or actions. Sub-technique AML.T0080.000 covers the specific memory-layer variant documented by Microsoft.
- **Memory Manipulation** -- altering long-term LLM memory so malicious changes persist across future chat sessions.
- **Thread Injection** -- introducing malicious instructions into a specific chat thread to change behavior for the duration of that conversation.
- **Publish Poisoned AI Agent Tool** -- creating malicious MCP tools that appear safe but execute harmful actions.
- **Escape to Host** -- breaking out of agent sandboxes to escalate impact.

The 2026 framework shift -- **from model-centric attacks to execution-layer exposure** -- directly informs stress testing under requirement 11.6.4. Detectors built for RAG corpora alone miss the agent memory, thread, and tool-publishing vectors that dominate recent real-world incidents.

### NSA Cybersecurity Information Sheet on MCP (May 2026)

On May 20, 2026, NSA's Artificial Intelligence Security Center released **"Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation"** (U/OO/6030316-26, v1.0) -- the first US-government design guidance specifically for MCP. The CSI characterizes MCP as "flexible and underspecified" and notes that it inverts the conventional client/server trust pattern: the client-side model consumes and acts on whatever connected servers return.

The recommendations read like an audit checklist for requirements 11.6.1 and 11.6.3:

- **Schema, range, and context validation** of every tool invocation before the model consumes the result -- pre-inference validation as a protocol-level design requirement, not an optional guardrail
- **Comprehensive invocation logging** -- all tool and model invocations recorded with exact parameters, the identities involved, and cryptographic hashes of results where feasible, which makes post-incident traceback (the RAGForensics problem) tractable for tool outputs
- **Data-classification zoning** -- tools grouped by the sensitivity of data they touch, so a poisoned low-trust tool cannot feed context into a high-sensitivity workflow
- **Filtering outgoing proxy / DLP** for external MCP connections, structurally gating what leaves the environment even when a poisoned context successfully redirects the model

For organizations subject to US federal guidance, this CSI converts several "best practice" recommendations from the OWASP MCP Top 10 into citable government baseline expectations.

### MCP Data-Layer Exposure: Back-End Vulnerabilities and Internet-Scale Scans (May--June 2026)

Akamai research published May 13, 2026 ("One Is a Fluke, 3 Is a Pattern") disclosed three MCP back-end vulnerabilities that move the contamination threat from crafted documents to the retrieval data layer itself:

- **CVE-2025-66335** -- SQL injection in Apache Doris MCP via an unvalidated `db_name` parameter (patched December 30, 2025)
- **Apache Pinot MCP authentication bypass** -- an HTTP endpoint exposed without mandatory authentication enabling unauthenticated SQL execution; StarTree added optional OAuth in October 2025 but the underlying injection remained
- **Alibaba RDS MCP unauthenticated information disclosure** -- any client that can reach the endpoint can invoke the RAG MCP tool and exfiltrate vector-index metadata (table names, schemas). Alibaba declined to patch, so this remains live in all versions.

The common theme is missing security validation between the MCP server and its back end. An attacker who can write to or read from the retrieval layer does not need stealthy poisoned documents -- the corpus itself is the soft target. Scale data reinforces the point: VIPER-MCP taint analysis across roughly 40,000 MCP repositories surfaced 106 zero-days yielding 67 CVEs (including a CVSS 9.8 command injection in unofficial AWS/Azure MCP variants), Censys counted 12,520 internet-accessible MCP services in June 2026, and Trend Micro found about 40% of exposed servers offering tools without authentication. For 11.6.1, the implication is that anomaly detection has to assume the retrieval index may already be attacker-writable; for 11.6.3, unauthenticated tool and RAG endpoints are a gating failure that no downstream detector compensates for.

### OWASP Agent Memory Guard: Reference Implementation for Memory Screening (June 2026)

**OWASP Agent Memory Guard** (v0.3.0, June 10, 2026; Apache-2.0) is the official OWASP reference implementation for defending against ASI06 Memory & Context Poisoning. It sits between an agent and its memory store and screens every read and write through a detector pipeline: prompt-injection markers, secret/PII leakage, protected-key tampering, size anomalies, self-reinforcement loops (an agent poisoning its own memory through repeated writes), and SHA-256 baseline integrity checks. A YAML policy engine maps findings to allow/redact/quarantine/block actions and emits structured SecurityEvents; forensic snapshots support rollback after a confirmed poisoning.

Published metrics from the project: 92.5% recall, 100% precision, 0% false-positive rate, F1 0.961, and 59 microseconds median latency on its 55-case test suite, with per-detector breakdowns (injection and protected-key detection at 100%, leakage 83%, size anomaly 80%). The small suite size means these numbers are a starting point rather than production evidence, but the per-detector disclosure format is exactly what 11.6.4 documentation should look like. Integration packages exist for LangChain (`langchain-agent-memory-guard`), and the write-time screening model directly implements the "sovereign over authorship" property the Mnemonic Sovereignty survey identified as the structural gap in most memory stacks.

### Microsoft Agent Governance Toolkit (April 2026)

Microsoft open-sourced the **Agent Governance Toolkit** (April 2, 2026, MIT license), a seven-package runtime security suite for AI agents with three components directly relevant to runtime contamination:

- **Cross-Model Verification Kernel (CMVK)** -- majority voting across multiple models to defend against memory poisoning; a poisoned memory that steers one model is unlikely to steer an independently prompted verifier ensemble the same way
- **MCP security gateway with capability sandboxing** -- screens tool responses before they reach the agent, addressing the ATPA post-tool-call blind spot
- **Agent OS** -- a stateless policy engine intercepting agent actions at a claimed sub-0.1 ms p99 latency, with YAML, OPA Rego, and Cedar policy language support, plus Agent Mesh for cryptographic agent identity with 0--1000 trust scoring

CMVK is notable as one of the first production-packaged implementations of cross-model consensus as a poisoning detector -- conceptually similar to RAGuard's counterfactual testing but spending the extra inference budget on model diversity instead of document ablation. The cost profile (N model calls per check) limits it to high-impact actions, which aligns it naturally with 11.6.3's risk-appropriate gating.

### Black-Box Poisoning Economics: Retrieval-Barrier IPI and MIRAGE (2026)

Two papers quantify how cheap and stealthy black-box inference-time poisoning has become:

**"Overcoming the Retrieval Barrier: Indirect Prompt Injection in the Wild for LLM Systems"** (arXiv 2601.07072, January 2026) decomposes malicious documents into retrieval-guaranteeing trigger fragments plus payloads, requiring only embedding-API access. Results: near-100% retrieval rates across 11 benchmarks and 8 embedding models at approximately $0.21 per target query using commercial embedding APIs, and a single poisoned email coercing GPT-4o into SSH-key exfiltration with over 80% success in multi-agent workflows. The paper evaluates several retrieval-level defenses and finds them insufficient -- though the trigger fragments themselves are statistically unusual, which is precisely the signal 11.6.1-style pre-inference anomaly detection should target.

**MIRAGE** (arXiv 2512.08289) automates black-box, query-agnostic corpus poisoning via persona-driven query synthesis, semantic anchoring, and adversarial test-time preference optimization using only surrogate-model feedback. It outperforms prior attacks on both efficacy and stealth and transfers across retriever-LLM combinations. The stealth optimization is aimed squarely at the perplexity and embedding-distance thresholds most deployed detectors use -- a direct challenge to 11.6.2 threshold tuning that assumes attack distributions resemble PoisonedRAG-era artifacts.

### Large-Scale IPI Competition: 272,000 Attack Attempts Across 13 Frontier Models (March 2026)

**"How Vulnerable Are AI Agents to Indirect Prompt Injections? Insights from a Large-Scale Public Competition"** (arXiv 2603.15714) reports the largest public adversarial dataset for inference-time injection to date: 464 participants, 272,000 attack attempts, 8,648 successful hidden injections across 41 scenarios and 13 frontier models. Key findings:

- Per-model attack success ranged from **0.5% (Claude Opus 4.5) to 8.5% (Gemini 2.5 Pro)** -- every model tested was vulnerable
- Universal attacks transferred across 21 of 41 behaviors and across model families
- Correlation between general capability and injection robustness was **weak** -- newer, smarter models are not automatically safer

The dataset was shared with frontier labs and the UK and US AI Safety Institutes. For 11.6.2 this is the most representative public adversarial validation corpus currently available; for 11.6.4 the per-model ASR spread is direct evidence for why false-positive and false-negative rates must be documented per model version rather than assumed stable across upgrades.

### ProGRank: Training-Free Retriever-Side Reranking Defense (March 2026)

**ProGRank** (arXiv 2603.22934) adds to the retriever-stage defense family (GMTP, RAGPart, RAGMask) with a post-hoc, training-free approach: each query-passage pair is stress-tested under mild randomized perturbations, "probe gradients" are extracted from a small fixed parameter subset of the retriever, and two instability signals (representational consistency and dispersion risk) feed a score gate in a reranking step. Poisoned passages exhibit measurably less stable retrieval behavior under perturbation than organically relevant ones. Evaluated across three datasets and three dense-retriever backbones in both retrieval-stage and end-to-end settings, it requires no retraining, preserves passage content, and offers a surrogate-retriever variant for teams that cannot access the production retriever's internals -- partially answering the open question of whether retriever-stage defenses are locked to self-hosted retrievers.

### ISO/IEC 27090 at Final Draft Stage (2026)

**ISO/IEC 27090** ("Cybersecurity -- Artificial Intelligence -- Guidance for addressing security threats and compromises to AI systems") reached FDIS -- the final ballot stage before publication -- in early 2026, with publication expected in the second half of 2026. The draft explicitly covers data poisoning including exploitation of continuous learning during operation, and is unusually candid for a standards document: it states that detecting poisoning is necessary but "often difficult." Once published it becomes the ISO-track reference for poisoning detection controls and a plausible input to EU AI Act conformity assessment. For 11.6.4, the practical takeaway is that honestly documenting detector limitations and measured false-positive rates aligns with where the international standards track is heading, while claiming comprehensive detection coverage does not.

---

## Related Standards & References

- [MITRE ATLAS AML.T0020 -- Poison Training Data](https://atlas.mitre.org/techniques/AML.T0020) -- Data poisoning attack techniques (applicable to inference-time context)
- [MITRE ATLAS AML.T0018 -- Backdoor ML Model](https://atlas.mitre.org/techniques/AML.T0018) -- Backdoor and poisoning attack techniques
- [MITRE SAFE-AI Framework](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf) -- Maps ATLAS threats to NIST SP 800-53 controls across AI system elements
- [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/) -- Poisoning risks in LLM systems
- [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) -- Knowledge base as a distinct attack surface
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm012025-prompt-injection/) -- Indirect prompt injection via poisoned context is closely related
- [NIST AI 100-2e2023 -- Poisoning Attacks](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Poisoning attack taxonomy
- [Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023)](https://arxiv.org/abs/2302.12173) -- Indirect prompt injection through retrieved content
- [PoisonedRAG (USENIX Security 2025)](https://www.usenix.org/system/files/usenixsecurity25-zou-poisonedrag.pdf) -- High-success-rate RAG poisoning with minimal injection volume
- [Eyes-On-Me: Scalable RAG Poisoning Through Attention Manipulation (October 2025)](https://arxiv.org/abs/2510.00586) -- Attention-targeted RAG poisoning bypassing retrieval-score defenses
- [Understanding Data Poisoning Attacks for RAG (2025)](https://openreview.net/forum?id=2aL6gcFX7q) -- Systematic analysis of RAG poisoning attack mechanisms
- [Semantic Chameleon: Corpus-Dependent Poisoning Attacks and Defenses in RAG Systems (March 2026)](https://arxiv.org/abs/2603.18034) -- Dual-document poisoning and hybrid retrieval defenses
- [RAGuard: A Layered Defense Framework for RAG Against Data Poisoning (NeurIPS 2025)](https://openreview.net/forum?id=onh7sLJ1kl) -- Two-layer defense with adversarial retriever training and counterfactual filtering
- [Sparse Document Attention RAG (SDAG, February 2026)](https://arxiv.org/abs/2602.04711) -- Block-sparse attention defense against cross-document poisoning
- [Traceback of Poisoning Attacks to RAG -- RAGForensics (ACM Web 2025)](https://dl.acm.org/doi/abs/10.1145/3696410.3714756) -- First traceback system for identifying poisoned documents in RAG knowledge bases
- [RAGDefender: Efficient Defense Against Knowledge Corruption Attacks on RAG (ACSAC 2025)](https://arxiv.org/abs/2511.01268) -- Post-retrieval grouping and isolation defense using TF-IDF clustering
- [ReliabilityRAG: Provably Robust Defense for RAG-based Web-Search (NeurIPS 2025)](https://arxiv.org/abs/2509.23519) -- Graph-theoretic contradiction filtering with formal robustness guarantees
- [RevPRAG: Detecting RAG Poisoning Through LLM Activations (2024)](https://arxiv.org/abs/2411.18948) -- Activation-based poisoning detection with ~98% TPR
- [RevPRAG: Revealing Poisoning Attacks in RAG Through LLM Activation Analysis (ACL Findings 2025)](https://aclanthology.org/2025.findings-emnlp.698/) -- Peer-reviewed version reporting ~98% TPR and close to 1% FPR
- [MM-MEPA: Stealth Poisoning Attacks on Multimodal RAG via Metadata (February 2026)](https://arxiv.org/abs/2603.00172) -- Metadata-only poisoning achieving 91% success on MMQA
- [KG-RAG Poisoning: Exploring Knowledge Poisoning Attacks to RAG (2025)](https://arxiv.org/abs/2507.08862) -- First systematic evaluation of data poisoning against knowledge-graph-based RAG
- [Meta LlamaFirewall: Open Source Guardrail System for Secure AI Agents (2025)](https://arxiv.org/abs/2505.03574) -- Production guardrail framework with PromptGuard 2 and AlignmentCheck
- [GGUF Template Poisoning: Investigating Inference-Time Model Templates at Scale (Splunk, 2025)](https://www.splunk.com/en_us/blog/security/gguf-llm-security-inference-time-poisoning-templates.html) -- Inference scaffolding as an overlooked attack surface
- [Lakera: Introduction to Data Poisoning -- A 2026 Perspective](https://www.lakera.ai/blog/training-data-poisoning) -- Industry overview of poisoning across the LLM lifecycle
- [Through the Stealth Lens: Attention-Aware Defenses Against Poisoning in RAG (2025)](https://arxiv.org/abs/2506.04390) -- NPAS and AV Filter attention-based defense reducing ASR from ~90% to ~15%
- [Virus Infection Attack on LLMs: Poisoning Propagation via Synthetic Data (NeurIPS 2025)](https://arxiv.org/abs/2509.23041) -- ~70% poisoning inheritance rate through synthetic data pipelines
- [Basilisk Venom: Poison in the Pipeline (0din.ai, January 2025)](https://0din.ai/blog/poison-in-the-pipeline-liberating-models-with-basilisk-venom) -- Real-world backdoor attack via poisoned GitHub code comments affecting DeepThink-R1
- [MITRE ATLAS](https://atlas.mitre.org/) -- v5.4.0 (February 2026) added "Publish Poisoned AI Agent Tool"; v5.5.0 (March 2026) added "AI Agent Tool Poisoning" and "AI Supply Chain Rug Pull"; v2026.05 (May 27, 2026) introduced calendar versioning, a REST API, and Agentic AI platform tags
- [MITRE ATLAS Data Releases (GitHub)](https://github.com/mitre-atlas/atlas-data/releases) -- Release notes for v5.5.0, v5.6.0, and the v2026.05 / data-format 6.0.0 overhaul
- [Amazon Bedrock Guardrails: Contextual Grounding Checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html) -- Confidence-scored grounding and relevance checks for RAG responses
- [NVIDIA NeMo Guardrails Configuration](https://docs.nvidia.com/nemo/guardrails/latest/configure-rails/yaml-schema/guardrails-configuration/index.html) -- Input, output, retrieval, and execution rails for measuring guardrail behavior by stage
- [Lakera Guard Threshold Levels](https://docs.lakera.ai/docs/defenses) -- L1--L4 threshold settings that explicitly trade false positives against false negatives
- [AI Recommendation Poisoning (Microsoft Defender Security Research, February 2026)](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) -- 50+ live memory-poisoning examples across 31 companies; AML.T0080 Memory Poisoning catalog entry
- [Hidden-in-Plain-Text / OpenRAG-Soc: A Benchmark for Social-Web Indirect Prompt Injection in RAG (January 2026)](https://arxiv.org/abs/2601.10923) -- Macro ASR dropped from 24.9% to 4.7% via HTML sanitization + NFKC normalization + attribution-gated answering
- [RAGShield: Provenance-Verified Defense-in-Depth Against Knowledge Base Poisoning (2026)](https://arxiv.org/abs/2604.00387) -- 0.0% ASR across 430 numerical-manipulation attacks where embedding-based defenses failed at 79--90%
- [MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers (2025)](https://arxiv.org/abs/2508.14925) -- 72.8% ASR against o1-mini; Claude-3.7-Sonnet refusal rate <3%
- [Zenity Labs and MITRE ATLAS: Agent Attack Technique Collaboration](https://zenity.io/blog/current-events/zenity-labs-and-mitre-atlas-collaborate-to-advances-ai-agent-security-with-the-first-release-of) -- 14 agent-focused techniques added to ATLAS including Memory Manipulation, Thread Injection, AI Agent Context Poisoning
- [Zenity GenAI Attacks Matrix](https://labs.zenity.io/p/ttps-ai-for-genai-targeted-attacks) -- Community-maintained TTP catalog for GenAI-targeted attacks that feeds into MITRE ATLAS
- [EU AI Act: Regulatory Framework (European Commission)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) -- High-risk AI cybersecurity obligations explicitly covering prompt injection, data poisoning, and model extraction
- [EU AI Act Article 15: Accuracy, Robustness and Cybersecurity](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-15) -- Requires declared accuracy metrics and lifecycle resilience for high-risk AI systems
- [EU AI Act Digital Omnibus Provisional Agreement (May 7, 2026)](https://www.insideprivacy.com/artificial-intelligence/eu-ai-act-update-timeline-relief-targeted-simplification-and-new-prohibitions/) -- Annex III high-risk AI obligations shifted from August 2026 to December 2, 2027; product-regulated Annex I obligations shifted to August 2, 2028
- [European Commission Draft Guidelines on High-Risk AI Classification (May 19, 2026)](https://www.hunton.com/privacy-and-cybersecurity-law-blog/european-commission-releases-draft-guidelines-on-high-risk-ai-under-the-eu-ai-act) -- Public consultation open until June 23, 2026 on what qualifies as a high-risk AI system under Annex III
- [Advanced Tool Poisoning Attacks / MCP Tool Poisoning (CyberArk Threat Research)](https://www.cyberark.com/resources/threat-research-blog/poison-everywhere-no-output-from-your-mcp-server-is-safe) -- Post-tool-call payload manipulation that bypasses input-side guardrails
- [GMTP: Gradient-based Masked Token Probability for Poisoned Document Detection (ACL Findings 2025, arXiv 2507.18202)](https://arxiv.org/abs/2507.18202) -- Retriever-gradient + MLM filter removing 90%+ of poisoned content with no LLM call
- [RAGPart & RAGMask: Retrieval-Stage Defenses Against Corpus Poisoning in RAG (AAAI 2026 NFIR Workshop, arXiv 2512.24268)](https://arxiv.org/abs/2512.24268) -- Document-partition and token-mask similarity defenses for dense retrievers
- [OWASP MCP Top 10 (Beta, 2026)](https://owasp.org/www-project-mcp-top-10/) -- Beta-release security framework for Model Context Protocol; MCP03 Tool Poisoning covers rug pulls, schema poisoning, and tool shadowing
- [OWASP MCP Top 10 -- MCP03:2025 Tool Poisoning](https://owasp.org/www-project-mcp-top-10/2025/MCP03-2025%E2%80%93Tool-Poisoning) -- Detailed entry on tool poisoning attack patterns and defense baselines
- [OX Security: The Mother of All AI Supply Chains -- Critical Systemic Vulnerability in Anthropic MCP (April 15, 2026)](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) -- 7,000+ public servers, 150M+ downloads, 200,000 vulnerable instances; 10+ CVEs across LiteLLM, LangChain, LangFlow, Cursor, Windsurf, GPT Researcher
- [CVE-2025-54136 -- Cursor MCP Configuration RCE (NVD)](https://nvd.nist.gov/vuln/detail/CVE-2025-54136) -- Persistent RCE via swap of already-approved MCP configuration; patched in Cursor 1.3 by requiring per-edit re-approval
- [Invariant Labs mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) -- Reference MCP scanner implementing tool pinning, rug-pull detection, and cross-origin escalation checks
- [NIST COSAiS -- Control Overlays for Securing AI Systems](https://csrc.nist.gov/projects/cosais) -- SP 800-53 control overlays for five AI use cases including single-agent and multi-agent AI; agent overlays in development as of May 2026
- [NIST COSAiS Predictive AI Overlay (Discussion Draft, January 8, 2026)](https://csrc.nist.gov/csrc/media/Projects/cosais/documents/COSAiS-Predictive-AI-annotated-outline-Jan2026.pdf) -- First COSAiS discussion draft; agent-specific overlays still pending
- [PIDP-Attack: Combining Prompt Injection with Database Poisoning on RAG (arXiv 2603.25164, 2026)](https://arxiv.org/abs/2603.25164) -- Hybrid attack appending malicious characters at inference time while poisoning the retrieval database
- [Securing Retrieval-Augmented Generation: A Taxonomy of Attacks, Defenses, and Future Directions (arXiv 2604.08304, April 2026)](https://arxiv.org/abs/2604.08304) -- Comprehensive 2026 survey consolidating the RAG attack and defense landscape
- [OWASP Top 10 for Agentic Applications 2026 (OWASP GenAI Security Project)](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) -- First OWASP framework dedicated to agent risks; ASI06 Memory & Context Poisoning covers persistent memory, embeddings, RAG, and inter-agent shared context as a unified contamination surface
- [Addressing OWASP Top 10 Risks in Agentic AI with Microsoft Copilot Studio (Microsoft Security Blog, March 30, 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/30/addressing-the-owasp-top-10-risks-in-agentic-ai-with-microsoft-copilot-studio/) -- Reference implementation of ASI06 controls (per-tenant memory segmentation, provenance, trust-weighted retrieval) integrated with DLP and tenant-isolation telemetry
- [A Survey on the Security of Long-Term Memory in LLM Agents: Toward Mnemonic Sovereignty (arXiv 2604.16548, April 2026)](https://arxiv.org/abs/2604.16548) -- Six-phase memory lifecycle (Write/Store/Retrieve/Execute/Share/Forget) x four-objective (Integrity/Confidentiality/Availability/Governance) framework for evaluating poisoning defenses
- [Securing AI Agents Against Prompt Injection Attacks (arXiv 2511.15759, Ramakrishnan & Balaji, November 2025)](https://arxiv.org/abs/2511.15759) -- 847-case multi-category benchmark with reproducible defense suite; 73.2% to 8.7% ASR with 94.3% clean-task retention
- [CVE-2026-26118 -- Microsoft MCP Server Tool Hijacking (CVSS 8.8, March 10, 2026 Patch Tuesday)](https://www.pointguardai.com/ai-security-incidents/microsoft-mcp-server-vulnerability-opens-door-to-ai-tool-hijacking-cve-2026-26118) -- First-party MCP server fix illustrating that response-side validation is required even on vendor-published MCP infrastructure
- [The State of MCP Security 2026: Incidents, Attack Patterns, and Defense Coverage (PipeLab)](https://pipelab.org/blog/state-of-mcp-security-2026/) -- 2026 incident timeline covering Anthropic SDK STDIO, CVE-2026-26118, CVE-2026-33032 (nginx-ui MCP-invocable takeover), and the related CVE-2025-54136 Cursor swap pattern
- [Timeline of Model Context Protocol (MCP) Security Breaches (AuthZed, 2026)](https://authzed.com/blog/timeline-mcp-breaches) -- Ongoing chronological record of MCP-class incidents relevant to inference-time poisoning and tool-poisoning attack patterns
- [NSA CSI: Model Context Protocol (MCP) -- Security Design Considerations for AI-Driven Automation (May 20, 2026)](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf) -- U/OO/6030316-26 v1.0; schema/range/context validation of tool invocations, hash-logged outputs, data-classification zoning, filtering outgoing proxy
- [NSA Press Release: Security Design Considerations for AI-Driven Automation Leveraging MCP (May 20, 2026)](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4496698/nsa-releases-security-design-considerations-for-ai-driven-automation-leveraging/) -- Announcement and summary of the AISC Cybersecurity Information Sheet
- [Akamai: One Is a Fluke, 3 Is a Pattern -- MCP Back-End Vulnerabilities (May 13, 2026)](https://www.akamai.com/blog/security-research/one-fluke-3-pattern-mcp-back-end-vulnerabilities) -- CVE-2025-66335 (Apache Doris MCP SQLi), Apache Pinot MCP auth bypass, Alibaba RDS MCP unauthenticated vector-index disclosure (declined to patch)
- [Adversa AI: Top MCP Security Resources, June 2026](https://adversa.ai/blog/top-mcp-security-resources-june-2026/) -- VIPER-MCP taint analysis (106 zero-days, 67 CVEs across ~40,000 repos); Censys count of 12,520 internet-accessible MCP services; ~40% of exposed servers unauthenticated
- [OWASP Agent Memory Guard (v0.3.0, June 2026)](https://github.com/OWASP/www-project-agent-memory-guard) -- OWASP reference implementation for ASI06; read/write memory screening, allow/redact/quarantine/block policy engine, published precision/recall/FPR metrics
- [Help Net Security: OWASP Agent Memory Guard Announcement (June 1, 2026)](https://www.helpnetsecurity.com/2026/06/01/owasp-agent-memory-guard/) -- Independent coverage of the Agent Memory Guard release and its detector pipeline
- [Microsoft Agent Governance Toolkit (April 2, 2026)](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/) -- Cross-Model Verification Kernel, MCP security gateway, Agent OS policy engine with OPA Rego/Cedar support
- [microsoft/agent-governance-toolkit (GitHub)](https://github.com/microsoft/agent-governance-toolkit) -- Source for the seven-package agent runtime security suite
- [Overcoming the Retrieval Barrier: Indirect Prompt Injection in the Wild for LLM Systems (arXiv 2601.07072, January 2026)](https://arxiv.org/abs/2601.07072) -- Black-box trigger-fragment attack: near-100% retrieval at ~$0.21 per target query; >80% SSH-key exfiltration success against GPT-4o multi-agent workflows
- [MIRAGE: Misleading RAG via Black-box and Query-agnostic Poisoning Attacks (arXiv 2512.08289)](https://arxiv.org/abs/2512.08289) -- Stealth-optimized corpus poisoning designed to evade perplexity and embedding anomaly detectors
- [How Vulnerable Are AI Agents to Indirect Prompt Injections? Insights from a Large-Scale Public Competition (arXiv 2603.15714, March 2026)](https://arxiv.org/abs/2603.15714) -- 272,000 attack attempts, 8,648 successes across 41 scenarios and 13 frontier models; per-model ASR 0.5%--8.5%
- [ProGRank: Probe-Gradient Reranking Defense Against RAG Corpus Poisoning (arXiv 2603.22934, March 2026)](https://arxiv.org/abs/2603.22934) -- Training-free retriever-side defense using perturbation-instability signals; includes surrogate-retriever variant
- [ISO/IEC 27090: Guidance for Addressing Security Threats and Compromises to AI Systems](https://www.iso.org/standard/56581.html) -- At FDIS as of early 2026; covers data poisoning including continuous-learning exploitation; publication expected H2 2026
- [OpenAI Guardrails Python: Prompt Injection Detection Check](https://openai.github.io/openai-guardrails-python/ref/checks/prompt_injection_detection/) -- OpenAI's open-source guardrails framework with configurable-confidence-threshold injection screening

---

## Open Research Questions

- Semantic Chameleon shows detection difficulty varies 13--62x between corpus types -- how should organizations calibrate defenses to their specific corpus composition?
- RAGuard's leave-one-out counterfactual testing requires N+1 inference passes per query. Can this be approximated efficiently for latency-sensitive applications, or is it fundamentally restricted to batch/offline verification?
- How can anomaly detection reliably distinguish between legitimate unusual inputs and adversarially crafted poisoned inputs, especially when dual-document attacks (sleeper + trigger) maintain high semantic legitimacy?
- Hybrid retrieval (BM25 + dense) is a strong first-line defense but joint sparse+dense optimization can partially overcome it -- what is the long-term arms race trajectory here?
- Can LLMs themselves serve as effective detectors for poisoned context (meta-reasoning about input trustworthiness), or does this create a circular dependency?
- How should detection thresholds adapt in real-time to changing threat levels without creating instability?
- Can SDAG's block-sparse attention approach scale to production RAG systems with hundreds of retrieved passages, and does blocking cross-document attention harm answer quality on complex multi-hop reasoning tasks?
- What is the interaction between inference-time poisoning detection and prompt injection defense (C2, C9) -- are these fundamentally the same problem?
- Can attention-based detection methods (Attention Tracker) generalize across model architectures and languages, or are they architecture-specific?
- How should detection systems handle poisoning through MCP server outputs and inter-agent communications, where the trust model differs from retrieved documents?
- NIST COSAiS agentic AI control overlays remain in development as of May 2026: the Predictive AI overlay was released as a discussion draft on January 8, 2026 with comments due February 13, but the single-agent and multi-agent AI overlays have not yet appeared as drafts and are projected for mid-to-late 2026. Will the eventual agent overlays specify concrete inference-time poisoning detection metrics (false-positive thresholds, per-rail measurement, tool-pinning enforcement) or remain at the abstract SP 800-53 control-overlay level?
- MM-MEPA shows that multimodal RAG is vulnerable to metadata-only poisoning that evades image-metadata consistency checks -- what detection mechanisms can reliably catch semantically-valid but adversarial metadata modifications?
- KG-RAG poisoning uses only existing entities and relations, making graph-level anomaly detection difficult -- can graph structural analysis (e.g., detecting unusual triple connectivity patterns) provide a viable detection signal?
- RevPRAG achieves ~98% TPR via LLM activations, but requires model internals -- can similar detection accuracy be achieved through black-box behavioral probing for API-only deployments?
- RAGDefender and ReliabilityRAG offer lightweight post-retrieval filtering, but how do they perform under adaptive attacks specifically designed to evade clustering and contradiction-graph defenses?
- VIA demonstrates ~70% poisoning inheritance through synthetic data -- how should organizations audit synthetic data pipelines to detect inherited poisoning before it reaches production RAG knowledge bases?
- Attention-based defenses (NPAS/AV Filter) impose ~1000x computational cost on adaptive attackers -- does this cost asymmetry hold as attackers develop more efficient evasion techniques, or will the gap narrow?
- MITRE ATLAS v5.4.0 adds "Publish Poisoned AI Agent Tool" -- how should detection systems differentiate between poisoned tool outputs and legitimate but unexpected tool responses in multi-tool agent workflows?
- The Digital Omnibus provisional agreement (May 7, 2026) pushed Annex III high-risk AI obligations from August 2026 to December 2, 2027 and Annex I (product-regulated) obligations to August 2, 2028 -- what does the extra 16 months change in practice for inference-time poisoning programs? Will standards bodies use the runway to publish concrete detection metrics (false-positive thresholds, per-rail measurement, tool-pinning enforcement), or will providers default to demonstrating "good-faith" detection without quantitative gates?
- Memory-layer poisoning (AML.T0080, Microsoft Feb 2026) evades per-query retrieval filters entirely. What write-time provenance and periodic audit patterns scale to agents with millions of per-user memories, without destroying personalization utility?
- ATPA exploits the post-tool-call blind spot in most guardrail stacks -- can response-side structural validation (typed schemas, JSON-only responses, content-type allow-lists) be made strict enough to neutralize ATPA without breaking useful tool functionality, or is an LLM-mediated response check the only viable defense?
- OpenRAG-Soc shows that a three-defense baseline (HTML sanitization, NFKC normalization, attribution-gated answering) reduces ASR ~5x at negligible cost. Why is adoption of these web-hygiene defenses still rare in production RAG, and what deployment packaging (e.g., LangChain/LlamaIndex middleware) would change that?
- RAGShield's 0.0% ASR on numerical-integrity attacks depended on structured claim extraction. Can the same pattern be generalized to non-numerical structured claims (policy text, API schemas, dosage units with named exceptions), or does each domain require its own extractor?
- The Zenity/ATLAS agent-technique additions (Memory Manipulation, Thread Injection, Publish Poisoned AI Agent Tool) are new enough that most detection stacks have no coverage. Which of these techniques is most amenable to model-agnostic detection at the orchestration layer, and which fundamentally require model-intrinsic instrumentation?
- Tool pinning via SHA-256 hashes (mcp-scan, OWASP MCP Top 10 MCP03 baseline) defeats rug-pull and schema-poisoning edits, but legitimate tool descriptions also change. What hash-change policies (auto-approve patch-level versions, require explicit confirmation for capability or destination changes, require re-quarantine for new permission scopes) achieve the right balance between operational friction and poisoning resistance?
- GMTP, RAGPart, and RAGMask all rely on the retriever's internals (gradients, training dynamics, token-mask similarity). Can equivalent signal be recovered for closed-source managed retrievers used by hosted RAG services, or are retriever-stage defenses fundamentally locked to self-hosted dense retrievers?
- The OX Security MCP STDIO disclosure (April 2026) showed that the runtime transport layer is itself a poisoning vector. What signed-configuration and signed-tool-package patterns scale to the existing MCP ecosystem (Anthropic, LangChain, LangFlow, Cursor, Windsurf) without breaking the open-marketplace model that drives MCP adoption?
- The OWASP ASI Top 10 2026 elevates Memory & Context Poisoning (ASI06) to a top-level agent risk and bundles persistent memory, embedding stores, RAG corpora, and inter-agent shared context into a single category. Most production stacks still treat these as separate detection problems with separate metrics. What unified false-positive measurement schema lets 11.6.4 documentation cover all four surfaces in a way an external auditor can reason about, without flattening risk differences between, say, a memory write from a verified internal source and a RAG retrieval from open social-web content?
- The Mnemonic Sovereignty survey (arXiv 2604.16548, April 2026) frames runtime contamination around six memory lifecycle phases -- Write, Store, Retrieve, Execute, Share, Forget/Rollback. Detection tooling is concentrated at Write and Retrieve and is comparatively thin at Execute and Share. Which detection primitives would close the Execute/Share gaps for multi-agent workflows where poisoned content moves between agents via message passing rather than via the shared memory store?
- The retrieval-barrier attack (arXiv 2601.07072) makes poisoned-document co-retrieval nearly free (~$0.21 per target query via embedding APIs) while MIRAGE optimizes for stealth against perplexity and embedding-distance detectors. When both retrieval guarantee and statistical stealth are jointly optimized, what detectable signal remains -- and is the trigger-fragment structure itself (unusual token sequences that guarantee retrieval) the last reliable artifact?
- Akamai's Alibaba RDS MCP finding shows unauthenticated parties can read vector-index metadata, and ~40% of internet-exposed MCP servers serve tools without authentication. When the retrieval layer is attacker-writable by design failure rather than stealth, anomaly detection becomes triage rather than defense -- should AISVS-style verification treat data-layer authentication as a hard prerequisite for any 11.6.1 claim?
- Microsoft's CMVK bets on cross-model majority voting as a poisoning detector. The IPI competition showed universal attacks transferring across model families (21/41 behaviors) -- how much real diversity does a verifier ensemble need before transferable attacks stop defeating consensus, and is that diversity affordable at production latency?
- OWASP Agent Memory Guard reports 0% FPR on a 55-case suite. What community benchmark (analogous to the 847-case prompt injection suite or the 272,000-attempt competition corpus) would put memory-write screening on the same evidentiary footing as retrieval-stage defenses?

---

## Related Pages

- [C11-10 Adversarial Bias Exploitation Defense](C11-10-Adversarial-Bias-Exploitation-Defense.md) -- Complements false-positive measurement here with subgroup-stratified robustness checks for security classifiers that attackers may probe and evade.
- [C13-03 Model Drift Detection](../C13-Monitoring-and-Logging/C13-03-Model-Drift-Detection.md) -- Provides the production telemetry and drift-alerting layer needed to detect when contamination defenses regress after model or retriever changes.
- [C11-02 Adversarial Example Hardening](C11-02-Adversarial-Example-Hardening.md) -- Shares adaptive testing and robustness-evidence patterns that apply directly to poisoning detector validation.
- [C11-08 Agent Security Self-Assessment](C11-08-Agent-Security-Self-Assessment.md) -- Adds a pre-execution review layer for poisoned tool selections, memory writes, and high-impact agent actions.
- [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness.md) -- Places runtime context contamination alongside the broader adversarial robustness controls for evasion, extraction, privacy, and agent self-modification.

---
