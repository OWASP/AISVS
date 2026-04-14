# C11.6: Inference-Time Poisoned-Data Detection

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 5 | **IDs:** 11.6.1--11.6.5

## Purpose

Identify and neutralize backdoored or poisoned inputs at inference time, particularly in systems that consume external data (e.g., RAG pipelines, tool outputs, web scraping). Unlike training-time poisoning (covered in C1), inference-time poisoning targets the data a model processes during production use. This is especially relevant for RAG-based systems where retrieved documents, API responses, or user-supplied context can contain adversarial payloads designed to manipulate model behavior -- including indirect prompt injection, factual manipulation, and behavior modification through crafted context.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **11.6.1** | **Verify that** inputs from external or untrusted sources pass through anomaly detection (e.g., statistical outlier detection, consistency scoring) before model inference. | 2 | Poisoned context injection via compromised RAG corpora, malicious tool outputs, or adversarial web content. Without anomaly detection, the model blindly trusts all retrieved or supplied context. MITRE ATLAS AML.T0020 (Poison Training Data) adapted to inference-time context; OWASP LLM08:2025 (Vector and Embedding Weaknesses). Attack surface now includes multimodal metadata poisoning (MM-MEPA, February 2026), knowledge-graph triple injection targeting KG-RAG systems, and poisoned AI agent tools (MITRE ATLAS v5.4.0, February 2026 added "Publish Poisoned AI Agent Tool" technique). Real-world precedent: the Basilisk Venom attack (January 2025) planted hidden prompts in GitHub code comments that created backdoors in fine-tuned models including DeepThink-R1. | Review anomaly detection pipeline for external inputs. Verify detection methods are appropriate for the data type (statistical outlier detection for embeddings, consistency scoring for text, schema validation for structured data). Test with known poisoned inputs and confirm detection. Verify detection is applied before the model processes the input, not after. As of 2026, evaluate hybrid retrieval (combining BM25 + dense vector search) as a first-line defense -- Semantic Chameleon research shows this reduces gradient-optimized poisoning co-retrieval to 0% at balanced alpha. Consider post-retrieval filtering with RAGDefender (ACSAC 2025), which uses TF-IDF clustering and concentration-based grouping to isolate adversarial passages without additional LLM inference. For provably robust filtering, ReliabilityRAG (NeurIPS 2025) finds a consistent document majority via Maximum Independent Set on a contradiction graph, with formal guarantees against bounded adversarial corruption. Attention-based detection is maturing: the Normalized Passage Attention Score (NPAS) with Attention-Variance (AV) Filter reduces attack success rates from ~90% to ~15% at 0.1 corruption rate by quantifying each retrieved passage's influence via aggregated attention weights and iteratively removing anomalous high-attention passages. Amazon Bedrock Guardrails now offers contextual grounding checks that generate confidence scores for grounding and relevance in RAG responses, enabling automated blocking of responses not grounded in source documents. Tools: NVIDIA NeMo Guardrails for retrieval-level filtering, Meta LlamaFirewall (PromptGuard 2 for injection detection, AlignmentCheck for goal-hijacking), LLM Guard for pre-inference screening, Vigil for input pattern detection, Amazon Bedrock Guardrails for contextual grounding. | Anomaly detection for natural language inputs is inherently difficult -- poisoned text may be semantically valid and statistically indistinguishable from clean text. Indirect prompt injection payloads often look like normal text. Detection effectiveness varies dramatically by input modality. Embedding anomaly detection alone reduced attack success from 95% to 20% in RAG Security Bench (2025) benchmarks, but sophisticated dual-document attacks (Semantic Chameleon, March 2026) can still achieve 20--44% success against hybrid retrieval with joint sparse+dense optimization. Multimodal RAG faces additional risk: MM-MEPA (February 2026) showed metadata-only poisoning achieves 91% attack success on MMQA, and image-metadata consistency checks fail because similarity score distributions for clean and poisoned metadata overlap significantly. NPAS/AV Filter shows promise but adaptive attacks can still achieve up to 35% ASR, albeit at ~1000x computational cost to the attacker. No single detection layer is sufficient. |
| **11.6.2** | **Verify that** anomaly-detection thresholds are tuned on representative clean and adversarial validation sets and that the false-positive rate is measured and documented. | 2 | Miscalibrated detection that either misses poisoned inputs (thresholds too loose) or blocks legitimate inputs (thresholds too tight). Untuned detectors provide a false sense of security. | Review validation datasets used for threshold tuning -- verify they include representative clean data and realistic adversarial examples. Check documented false-positive rates and confirm they are acceptable for the application. Verify that thresholds are re-evaluated when the input distribution changes (new data sources, updated retrieval indices). RevPRAG (2024) offers a complementary approach: it extracts LLM activations from the final token and uses a Siamese network to distinguish poisoned from clean responses, achieving ~98% TPR at ~1% FPR across five LLMs and four retrievers, providing a useful baseline for calibrating downstream detection thresholds. | Creating representative adversarial validation sets is difficult and labor-intensive. The adversarial landscape changes rapidly, so validation sets become stale. False-positive rate tolerance depends heavily on the application -- a 1% false-positive rate may be acceptable for a chatbot but not for a medical decision-support system. RevPRAG's activation-based approach shows promising threshold stability across model families (GPT2-XL, Llama 2/3, Mistral), but requires access to model internals and may not apply to API-only deployments. |
| **11.6.3** | **Verify that** inputs flagged as anomalous trigger gating actions (blocking, capability degradation, or human review) appropriate to the risk level. | 2 | Detected anomalies that are logged but not acted upon. Detection without response provides no security value. Risk-appropriate gating ensures that the response matches the potential impact of the poisoned input. | Review gating action configuration for flagged inputs. Verify that high-risk use cases have blocking or human review gates. Verify that lower-risk use cases have appropriate degraded-capability responses (e.g., responding without the suspicious context, flagging output as uncertain). Test end-to-end: inject a flagged input and confirm the gating action executes. Evaluate leave-one-out counterfactual testing (RAGuard's zero-knowledge inference patch): temporarily remove each retrieved document and check if answer correctness changes -- documents whose removal corrects a wrong answer are flagged and excluded during final generation. | Blocking may not be the right response in all cases -- for RAG systems, excluding the suspicious document and proceeding with remaining context may be more useful than a hard block. The RAGuard leave-one-out approach provides an elegant selective-exclusion mechanism but requires multiple inference passes, increasing latency proportionally to the number of retrieved documents. Capability degradation must be communicated to the user. Human review gates introduce latency that may not be acceptable for real-time applications. |
| **11.6.4** | **Verify that** detection methods are periodically stress-tested with current adversarial techniques, including adaptive attacks designed to evade the specific detectors in use. | 3 | Detector evasion by sophisticated adversaries who study the detection methodology and craft inputs that bypass it. Static detectors become obsolete as attack techniques evolve. Mirrors the adaptive evaluation principle from C11.2.4. Semantic Chameleon (March 2026) demonstrated that joint sparse+dense gradient optimization can defeat hybrid retrieval defenses, and attack success varies 13--62x across corpus types. MM-MEPA (February 2026) showed metadata-only poisoning evades standard image-metadata consistency checks entirely. Adaptive attacks against attention-based defenses (NPAS/AV Filter) can achieve up to 35% ASR, demonstrating that even promising new detection mechanisms have evasion paths. | Review stress-testing schedule and methodology. Verify that tests include adaptive attacks (attacks crafted to evade the specific detection method), including dual-document strategies (sleeper + trigger documents), corpus-dependent attack variants, metadata-only poisoning for multimodal RAG, and attention-evasion attacks that minimize attention variance to bypass attention-based filters. For KG-RAG systems, include knowledge-graph triple injection tests -- even minimal perturbation triple insertion achieves >90% retrieval coverage under black-box conditions. Check that stress-test results inform detector updates. Use Query Pattern Differential (QPD) monitoring to detect anomalous retrieval frequency patterns across sensitive vs. benign queries -- QPD showed the most robust cross-corpus detection performance in 2026 evaluations. Include synthetic-data propagation testing: VIA (Virus Infection Attack, NeurIPS 2025 Spotlight) demonstrated that poisoning can propagate through synthetic data generation pipelines with ~70% inheritance rate in downstream models, requiring stress tests to cover not just direct poisoning but multi-generation propagation paths. Confirm testing cadence is appropriate for the threat landscape (at minimum quarterly for high-risk applications). Tools: DeepTeam (open-source red-teaming with 40+ vulnerability types), Promptfoo for injection testing. | Adaptive stress-testing for inference-time poisoning detection is maturing rapidly. Semantic Chameleon provides a concrete methodology for evaluating corpus-dependent attack resilience, and RAG Security Bench (Wang et al., 2025) offers a standardized benchmark with 13 poisoning methods across 5 datasets. Automated red-team tools for inference-time poisoning are catching up: DeepTeam and Promptfoo now support RAG-specific attack scenarios, though coverage of multimodal and KG-RAG attack vectors remains limited. GGUF template poisoning (Splunk/Pillar Security, 2025) represents an overlooked attack surface where adversarial instructions are embedded in model metadata rather than retrieved documents -- stress tests should include inspection of inference scaffolding (system prompts, chat templates, response prefixes). The computational cost of adaptive attacks against attention-aware defenses (~1000x baseline) suggests these defenses raise the bar meaningfully, but are not a complete solution. MITRE ATLAS v5.4.0 (February 2026) now tracks 84 techniques across 16 tactics, including agent-specific attack vectors like "Publish Poisoned AI Agent Tool" -- stress test scenarios should incorporate these newly catalogued techniques. |
| **11.6.5** | **Verify that** detection efficacy metrics are logged and periodically re-evaluated against updated threat intelligence. | 3 | Gradual degradation of detection effectiveness as attack techniques evolve and input distributions shift. Without ongoing measurement, detection may become ineffective without anyone noticing. As of February 2026, MITRE ATLAS v5.4.0 contains 84 techniques and 56 sub-techniques across 16 tactics, with 42 real-world case studies. VIA (NeurIPS 2025) demonstrated that poisoning can propagate through synthetic data pipelines with ~70% inheritance rate, meaning detection metrics must account for multi-generation poisoning effects, not just direct injection. | Review logged detection metrics (detection rate, false-positive rate, flagged input volume trends). Verify periodic review schedule with documented outcomes. Check that threat intelligence feeds (MITRE ATLAS updates including v5.4.0 agent-specific techniques, MITRE SAFE-AI framework mappings to NIST SP 800-53, published attack papers, OWASP LLM Top 10 updates) are incorporated into detection evaluation. Track real-world poisoning incidents (e.g., Basilisk Venom backdoor in GitHub repositories affecting DeepThink-R1, January 2025) to calibrate detection thresholds against demonstrated attack patterns. Verify that the MITRE SAFE-AI control overlays for the organization's AI use cases are current. Confirm that metric reviews lead to actionable updates when degradation is detected. For organizations using Amazon Bedrock, review contextual grounding check metrics for grounding and relevance score trends across RAG responses. | Threat intelligence for inference-time poisoning is improving: MITRE ATLAS v5.4.0 (February 2026) now covers 84 techniques with 42 case studies, MITRE SAFE-AI maps threats to NIST SP 800-53 controls, and NIST COSAiS is developing tailored AI control overlays (agentic use case overlays still in development as of early 2026). The EU AI Act enters full enforcement for high-risk AI systems in August 2026, adding regulatory pressure for documented poisoning detection metrics and incident response procedures. Academic publications still lag real-world attacks by 6--12 months. Metric interpretation requires domain expertise -- a declining detection rate could indicate fewer attacks or degraded detector performance. |

---

## Recent Research (2024--2026)

### RAG Knowledge Poisoning at Scale

Research from 2025 on **knowledge poisoning attacks to retrieval-augmented generation** demonstrates that RAG systems are highly vulnerable to targeted poisoning even with minimal injection volume. **PoisonedRAG** (USENIX Security 2025) achieved attack success rates of 97% on NQ, 99% on HotpotQA, and 91% on MS-MARCO by injecting only 5 malicious texts per target question into knowledge bases containing millions of texts. This dramatically low injection threshold means that anomaly detection systems (requirement 11.6.1) must operate at individual-document granularity, not just aggregate statistical analysis.

### Expanded Attack Surface: Agents and Tool Outputs

As of 2025-2026, inference-time poisoning now extends beyond RAG corpora to include **MCP server outputs, tool call results, and synthetic data pipelines**. Poisoning can target the entire LLM inference lifecycle: retrieved documents, API responses, web-scraped content, and inter-agent communications. This expanding attack surface means that requirement 11.6.1's anomaly detection must cover all external data ingestion points, not just retrieval pipelines.

### Attention-Based Detection: Attention Tracker

**Attention Tracker** is an emerging defense that detects poisoned inputs by checking whether a retrieved passage diverts attention away from the system prompt in instruction-following attention heads. This approach leverages the internal mechanism by which indirect prompt injections operate -- they hijack attention from the intended instruction to the injected payload. Attention Tracker represents a model-intrinsic detection method that could complement the statistical outlier detection and consistency scoring described in requirement 11.6.1.

### Scalable RAG Poisoning: Eyes-On-Me

**Eyes-On-Me** (October 2025) demonstrates scalable RAG poisoning through attention manipulation, showing that adversaries can craft poisoned documents that specifically target the retrieval and attention mechanisms of RAG pipelines. The attack is designed to maximize retrieval relevance scores for poisoned documents while embedding adversarial payloads, making detection through retrieval-score anomalies unreliable. This reinforces requirement 11.6.4's call for adaptive stress-testing -- detection methods that rely on retrieval-score outliers are specifically evadable.

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

**RAGForensics** is the first traceback system for RAG, designed to identify which specific documents in a knowledge base have been poisoned after an attack is suspected. It operates iteratively: retrieve a subset of documents, use a specially crafted prompt to guide an LLM in detecting potential poisoning, and narrow down the contaminated texts. This supports post-incident investigation and helps maintain the integrity guarantees of requirement 11.6.5's ongoing metric re-evaluation.

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

This six-layer approach maps to requirements 11.6.1 (detection at layers 1-2), 11.6.3 (gating actions at layers 2-4), and supports the stress-testing requirements of 11.6.4 by enabling independent evaluation of each layer. As of March 2026, the addition of post-retrieval isolation (RAGDefender) and activation monitoring (RevPRAG) closes gaps that existed in the earlier five-layer model.

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

This incident underscores that the threat models described in requirements 11.6.1 and 11.6.4 are not theoretical -- adversaries are actively exploiting inference-time poisoning vectors in production systems.

### MITRE ATLAS v5.4.0: Agent-Specific Attack Techniques (February 2026)

The February 2026 MITRE ATLAS v5.4.0 release expanded the taxonomy to 16 tactics, 84 techniques, and 56 sub-techniques (up from 15 tactics and 66 techniques in October 2025), with 42 real-world case studies. Notable additions relevant to inference-time poisoning:

- **Publish Poisoned AI Agent Tool**: Adversaries create malicious versions of legitimate MCP tools that appear safe but execute harmful actions when invoked. This extends the inference-time poisoning attack surface from retrieved documents to the tool layer -- a poisoned MCP server response is functionally equivalent to a poisoned RAG document from the model's perspective.
- **Escape to Host**: Techniques for breaking out of agent sandboxes, which can be combined with inference-time poisoning to escalate impact.

These additions reflect the framework's shift from model-centric to execution-layer threat coverage. For requirement 11.6.4's stress-testing mandate, organizations should map their detectors against the expanded ATLAS taxonomy to identify coverage gaps, particularly around tool-output poisoning and agent orchestration attack paths.

### Amazon Bedrock Guardrails: Contextual Grounding for RAG (2025--2026)

As of early 2026, **Amazon Bedrock Guardrails** provides contextual grounding checks specifically designed for RAG applications. The system generates confidence scores for both grounding (is the response factually consistent with the source documents?) and relevance (does the response address the user's query?), with configurable thresholds that can block or flag responses that fall below acceptable scores.

While contextual grounding is primarily positioned as a hallucination defense, it has direct applicability to inference-time poisoning: a poisoned document that steers the model toward adversarial outputs will often produce responses that are not grounded in the legitimate retrieved passages, triggering the grounding check. This makes Bedrock Guardrails a practical output-level defense (layer 6 in the defense architecture) for organizations already on AWS infrastructure. The limitation is that sophisticated poisoning attacks designed to maintain semantic consistency with legitimate content may not trigger grounding violations.

### Data Poisoning Across the LLM Lifecycle (2026 Perspective)

Lakera's 2026 analysis emphasizes that data poisoning risks now span pre-training, fine-tuning, RAG, and agent tooling. Runtime detection systems must track output distributions for sudden shifts, monitor unexpected tool usage patterns in agent systems, and create alerts for responses that deviate from expected norms. This holistic view supports requirement 11.6.5's call for ongoing metric re-evaluation against updated threat intelligence.

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
- [MM-MEPA: Stealth Poisoning Attacks on Multimodal RAG via Metadata (February 2026)](https://arxiv.org/abs/2603.00172) -- Metadata-only poisoning achieving 91% success on MMQA
- [KG-RAG Poisoning: Exploring Knowledge Poisoning Attacks to RAG (2025)](https://arxiv.org/abs/2507.08862) -- First systematic evaluation of data poisoning against knowledge-graph-based RAG
- [Meta LlamaFirewall: Open Source Guardrail System for Secure AI Agents (2025)](https://arxiv.org/abs/2505.03574) -- Production guardrail framework with PromptGuard 2 and AlignmentCheck
- [GGUF Template Poisoning: Investigating Inference-Time Model Templates at Scale (Splunk, 2025)](https://www.splunk.com/en_us/blog/security/gguf-llm-security-inference-time-poisoning-templates.html) -- Inference scaffolding as an overlooked attack surface
- [Lakera: Introduction to Data Poisoning -- A 2026 Perspective](https://www.lakera.ai/blog/training-data-poisoning) -- Industry overview of poisoning across the LLM lifecycle
- [Through the Stealth Lens: Attention-Aware Defenses Against Poisoning in RAG (2025)](https://arxiv.org/abs/2506.04390) -- NPAS and AV Filter attention-based defense reducing ASR from ~90% to ~15%
- [Virus Infection Attack on LLMs: Poisoning Propagation via Synthetic Data (NeurIPS 2025)](https://arxiv.org/abs/2509.23041) -- ~70% poisoning inheritance rate through synthetic data pipelines
- [Basilisk Venom: Poison in the Pipeline (0din.ai, January 2025)](https://0din.ai/blog/poison-in-the-pipeline-liberating-models-with-basilisk-venom) -- Real-world backdoor attack via poisoned GitHub code comments affecting DeepThink-R1
- [MITRE ATLAS v5.4.0 (February 2026)](https://atlas.mitre.org/) -- 84 techniques across 16 tactics, including agent-specific "Publish Poisoned AI Agent Tool"
- [Amazon Bedrock Guardrails: Contextual Grounding Checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html) -- Confidence-scored grounding and relevance checks for RAG responses

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
- NIST COSAiS agentic AI control overlays are still in development as of early 2026 -- will these provide actionable guidance for inference-time poisoning defense, or will they remain too abstract?
- MM-MEPA shows that multimodal RAG is vulnerable to metadata-only poisoning that evades image-metadata consistency checks -- what detection mechanisms can reliably catch semantically-valid but adversarial metadata modifications?
- KG-RAG poisoning uses only existing entities and relations, making graph-level anomaly detection difficult -- can graph structural analysis (e.g., detecting unusual triple connectivity patterns) provide a viable detection signal?
- RevPRAG achieves ~98% TPR via LLM activations, but requires model internals -- can similar detection accuracy be achieved through black-box behavioral probing for API-only deployments?
- RAGDefender and ReliabilityRAG offer lightweight post-retrieval filtering, but how do they perform under adaptive attacks specifically designed to evade clustering and contradiction-graph defenses?
- VIA demonstrates ~70% poisoning inheritance through synthetic data -- how should organizations audit synthetic data pipelines to detect inherited poisoning before it reaches production RAG knowledge bases?
- Attention-based defenses (NPAS/AV Filter) impose ~1000x computational cost on adaptive attackers -- does this cost asymmetry hold as attackers develop more efficient evasion techniques, or will the gap narrow?
- MITRE ATLAS v5.4.0 adds "Publish Poisoned AI Agent Tool" -- how should detection systems differentiate between poisoned tool outputs and legitimate but unexpected tool responses in multi-tool agent workflows?
- EU AI Act enforcement for high-risk systems begins August 2026 -- what specific poisoning detection metrics and documentation will satisfy regulatory requirements for inference-time monitoring?

---
