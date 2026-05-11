# C08: Memory, Embeddings & Vector Database Security

> **Source:** [`1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
> **Requirements:** 28 | **Sections:** 5

## Control Objective

Embeddings and vector stores act as semi-persistent and persistent 'memory' for AI systems via RAG. This memory can become a high-risk data sink and data exfiltration path. This control family hardens memory pipelines and vector databases so that access is least-privilege, data is sanitized before vectorization, retention is explicit, and systems are resilient to embedding inversion, membership inference, and cross-tenant leakage.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C8.1 | Access Controls on Memory & RAG Indices | 7 | [C08-01-Access-Controls-Memory-RAG](C08-01-Access-Controls-Memory-RAG.md) |
| C8.2 | Embedding Sanitization & Validation | 5 | [C08-02-Embedding-Sanitization-Validation](C08-02-Embedding-Sanitization-Validation.md) |
| C8.3 | Memory Expiry, Revocation & Deletion | 8 | [C08-03-Memory-Expiry-Revocation-Deletion](C08-03-Memory-Expiry-Revocation-Deletion.md) |
| C8.4 | Prevent Embedding Inversion & Leakage | 2 | [C08-04-Embedding-Inversion-Leakage-Prevention](C08-04-Embedding-Inversion-Leakage-Prevention.md) |
| C8.5 | Scope Enforcement for User-Specific Memory | 6 | [C08-05-Scope-Enforcement-User-Memory](C08-05-Scope-Enforcement-User-Memory.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- RAG poisoning — injecting malicious content into knowledge bases retrieved at inference time; PoisonedRAG (USENIX Security 2025) showed 5 documents achieve 90% attack success
- Embedding inversion attacks — reconstructing original text from embedding vectors; Vec2Text achieves up to 92% reconstruction of 32-token inputs; transfer attacks (ACL 2024) work without access to the original embedding model
- Cross-tenant data leakage through shared vector indices and metadata filter injection
- Memory persistence attacks — injecting instructions that persist across conversations; MINJA (NeurIPS 2025) achieves >95% injection success via query-only interaction
- Agent memory poisoning — OWASP ASI06 (2026) formally recognizes this as a top agentic risk; ZombieAgent (January 2026) showed persistent cross-session attacks via ChatGPT connectors
- AI Recommendation Poisoning — Microsoft (February 2026) documented 50+ real-world examples across 31 companies and 14 industries
- PII accumulation in vector stores without adequate deletion mechanisms; embedding inversion makes this a concrete exfiltration path
- Membership inference — determining whether a specific document exists in an embedded corpus
- Feedback loop poisoning — agent outputs written back to memory create self-reinforcing hallucinations; A-MemGuard found LLM classifiers miss 66% of poisoned entries
- Metadata filter injection — manipulating vector query filters to bypass tenant isolation
- Single-document RAG poisoning — CorruptRAG (Jan 2026) showed a single optimized document achieves 98.2% attack success by pushing its vector representation close to target queries, far stealthier than multi-document approaches
- Knowledge graph RAG poisoning — KEPo (Mar 2026) inserts adversarial triples that complete misleading inference chains in structured knowledge graphs, reducing QA accuracy by up to 80%
- Corpus-adaptive poisoning — Semantic Chameleon (Mar 2026) tailors poison documents to the specific corpus composition, defeating static detection
- Universal embedding inversion — ZSinvert demonstrated zero-shot inversion across any embedding model without per-model training, eliminating the attacker's need for model-specific knowledge
- Vector collision attacks — crafting documents whose embeddings collide with high-value query vectors via gradient-based optimization; the 2025 Supabase Cursor incident demonstrated real-world exploitation via support ticket injection
- Vector worms — theoretical future variant where poisoned embeddings instruct models to re-embed and reintroduce poisoned data elsewhere, creating cascading contamination
- Delayed tool invocation (Rehberger, January 2025) — conditional instructions in chat context trigger memory writes when users respond with natural affirmations, bypassing Google Gemini's guardrails
- Data loader poisoning — the ACM AISec "Hidden Threat in Plain Text" study demonstrated 74.4% attack success across 357 scenarios using 19 stealthy injection techniques (font poisoning, homoglyphs, zero-size fonts, out-of-bound text) against popular RAG data loaders including LangChain, LlamaIndex, and Docling; validated on black-box services like NotebookLM and OpenAI Assistants
- Training-free embedding inversion — Zero2Text (Feb 2026) uses recursive online alignment with LLM priors to invert embeddings without any training, achieving 1.8x ROUGE-L and 6.4x BLEU-2 improvements over baselines against OpenAI embeddings in black-box settings
- Zero-click exfiltration — EchoLeak demonstrated corporate data exfiltration from Microsoft 365 Copilot via crafted emails
- Centrality-driven hubness poisoning — Black-Hole Attack (April 2026) exploits a fundamental geometric defect of high-dimensional embedding spaces: vectors placed at or near the global or cluster centroid become disproportionate nearest neighbors. A handful of malicious vectors seeded near these centroids surface in up to 99.85% of top-10 results with no knowledge of user queries, and existing hubness-mitigation heuristics either crater retrieval accuracy or provide only partial protection
- Few-shot cross-model inversion — ALGEN (ACL 2025) reaches partial inversion from a single leaked (text, embedding) pair and near-optimal reconstruction with 1k samples by aligning the victim embedding space to an attacker-controlled encoder in one optimization step; transfers across domains and languages, and the authors show standard defenses (noise, quantization, DP) do not defeat it
- Compound query + corpus RAG attack — PIDP-Attack (March 2026) bolts a universal query-path suffix onto traditional passage poisoning, reaching 98.125% attack success on Natural Questions, HotpotQA and MS-MARCO across eight LLMs without needing any foreknowledge of user queries

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2023 | Morris et al. — "Text Embeddings Reveal Almost as Much as Text" | Demonstrated high-fidelity text reconstruction from OpenAI and other embeddings, establishing embedding inversion as a practical threat | [arXiv:2310.06816](https://arxiv.org/abs/2310.06816) |
| 2023 | Greshake et al. — "Not What You've Signed Up For: Compromising RAG" | Showed indirect prompt injection through poisoned retrieval documents in RAG pipelines | [arXiv:2302.12173](https://arxiv.org/abs/2302.12173) |
| 2024 | Zou et al. — "PoisonedRAG: Knowledge Poisoning Attacks to RAG" (accepted USENIX Security 2025) | Demonstrated targeted knowledge poisoning: just 5 crafted documents achieve 90% attack success rate against RAG systems | [arXiv:2402.07867](https://arxiv.org/abs/2402.07867) |
| 2024 | Zeng et al. — "Good and Bad Memories in RAG" | Analyzed how persistent memory poisoning creates lasting effects across sessions | [arXiv:2404.01096](https://arxiv.org/abs/2404.01096) |
| 2024 | Slack AI data exfiltration vulnerability | Combined RAG poisoning with social engineering to exfiltrate corporate data across Slack channels | [Prompt Security blog](https://prompt.security/blog/the-embedded-threat-in-your-llm-poisoning-rag-pipelines-via-vector-embeddings) |
| 2024 | Transferable Embedding Inversion Attack (ACL 2024) | Demonstrated embedding inversion without direct access to the original embedding model using surrogate models | [ACL Anthology](https://aclanthology.org/2024.acl-long.230/) |
| 2025 | Dong et al. — MINJA: Memory INJection Attack (NeurIPS 2025) | >95% injection success rate via query-only interaction without direct memory access; tested across medical, e-commerce, and QA systems | [arXiv:2503.03704](https://arxiv.org/abs/2503.03704) |
| 2025 | Rehberger — Delayed Tool Invocation bypass on Google Gemini | Conditional instructions in chat context trigger memory writes when users respond with natural affirmations, bypassing Gemini's runtime guardrails | [Christian Schneider blog](https://christian-schneider.net/blog/persistent-memory-poisoning-in-ai-agents/) |
| 2025 | Unit 42 — Amazon Bedrock Agents memory poisoning | Demonstrated silent data exfiltration via session summarization hijacking using forged XML tags in retrieved content | [Unit 42](https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/) |
| 2025 | Prompt Security — RAG Poisoning POC | Single poisoned embedding altered system behavior across multiple unrelated queries with 80% success rate using LangChain/Chroma/Llama 2 | [GitHub POC](https://github.com/prompt-security/RAG_Poisoning_POC) |
| 2025 | EchoLeak — Microsoft 365 Copilot zero-click exfiltration | Specially crafted email caused Copilot to autonomously exfiltrate corporate data without user interaction | [Sombrainc blog](https://sombrainc.com/blog/llm-security-risks-2026) |
| 2025 | DPPN — Defense through Perturbing Privacy Neurons | Reduces embedding privacy leakage by 5-78% while improving downstream task performance by 14-40% vs. blanket noise | [OpenReview](https://openreview.net/forum?id=DF5TVzpTW0) |
| 2025 | ACM RecSys — Reproducibility study of Morris et al. | Re-examined embedding inversion claims with nuanced benchmarks across different models and dimensions | [ACM DL](https://dl.acm.org/doi/10.1145/3705328.3748155) |
| 2026 | Radware — ZombieAgent exploit chain | ChatGPT's connector and memory features combined for persistent, cross-session indirect prompt injection spreading through email attachments | [Lakera blog](https://www.lakera.ai/blog/agentic-ai-threats-p1) |
| 2026 | Microsoft — AI Recommendation Poisoning report | Documented 50+ real-world examples of memory poisoning deployed by 31 companies across 14 industries in a 60-day review | [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/) |
| 2026 | SPARSE framework — Concept-Aware Privacy Mechanisms | Differentiable mask learning with Mahalanobis mechanism for selective perturbation of privacy-sensitive embedding dimensions | [arXiv:2602.07090](https://arxiv.org/abs/2602.07090) |
| 2026 | CorruptRAG — Single-Document RAG Poisoning (Jan 2026) | Demonstrated that a single carefully crafted poisoned document achieves 98.2% attack success rate by optimizing word selection to push vector representations close to target queries — far more practical and stealthy than multi-document approaches | [arXiv:2504.03957](https://arxiv.org/abs/2504.03957) |
| 2026 | SDAG — Sparse Document Attention RAG (Feb 2026) | Defense mechanism using block-sparse attention masks to prevent cross-document interaction during inference, substantially reducing poisoning success rates with no fine-tuning required | [arXiv:2602.04711](https://arxiv.org/abs/2602.04711) |
| 2026 | KEPo — Knowledge Evolution Poison on Graph-based RAG (Mar 2026) | First systematic knowledge graph RAG poisoning attack; inserts adversarial triples that complete misleading inference chains, reducing RoG accuracy from 45.8% to 8.9% on WebQSP | [arXiv:2603.11501](https://arxiv.org/abs/2603.11501) |
| 2026 | Semantic Chameleon — Corpus-Dependent RAG Poisoning (Mar 2026) | Adaptive poisoning that tailors attack documents to the specific corpus composition, defeating static detection baselines | [arXiv:2603.18034](https://arxiv.org/abs/2603.18034) |
| 2025 | Supabase Cursor Incident (mid-2025) | Attackers embedded SQL exfiltration instructions in support tickets that entered a RAG pipeline, exfiltrating integration tokens through the compromised retrieval chain | [InstaTunnel Blog](https://instatunnel.my/blog/vector-collision-attacks-hijacking-the-nearest-neighbor) |
| 2025 | Eguard — Embedding Inversion Defense (Nov 2025) | Transformer-based projection network with text mutual information optimization protects over 95% of tokens from inversion while maintaining 98% consistency on downstream tasks | [arXiv:2411.05034](https://arxiv.org/abs/2411.05034) |
| 2025 | ZSinvert — Universal Zero-Shot Embedding Inversion | Universal inversion method that works across any embedding model without training a separate inversion model per target, lowering the attacker's barrier to entry | [arXiv:2504.00147](https://arxiv.org/abs/2504.00147) |
| 2025 | RAGuard — Layered RAG Poisoning Defense (NeurIPS 2025) | Two-step defense combining adversarial retriever training with zero-knowledge inference patch; reduces ASR while maintaining retrieval quality without requiring poison labels | [OpenReview](https://openreview.net/forum?id=onh7sLJ1kl) |
| 2025 | RSB — Benchmarking Poisoning Attacks against RAG | First comprehensive benchmark evaluating 13 poisoning attacks across 5 QA datasets; found all 7 tested defenses fail to provide robust protection | [arXiv:2505.18543](https://arxiv.org/abs/2505.18543) |
| 2025 | HoneyBee — RBAC for Vector Databases via Dynamic Partitioning | Efficient role-based access control achieving 13.5x lower query latency than row-level security with 1.24x memory overhead | [arXiv:2505.01538](https://arxiv.org/abs/2505.01538) |
| 2025 | Hidden Threat in Plain Text — Attacking RAG Data Loaders (ACM AISec) | Taxonomy of 9 knowledge-based poisoning attacks with 19 injection techniques; 74.4% ASR across 357 scenarios on LangChain, LlamaIndex, Docling, Haystack, LLMSherpa; font poisoning achieves 100% ASR | [arXiv:2507.05093](https://arxiv.org/abs/2507.05093) |
| 2026 | Zero2Text — Training-Free Cross-Domain Embedding Inversion (Feb 2026) | Recursive online alignment combining LLM priors with dynamic ridge regression achieves 1.8x ROUGE-L and 6.4x BLEU-2 improvements over baselines against OpenAI embeddings in black-box scenarios | [arXiv:2602.01757](https://arxiv.org/abs/2602.01757) |
| 2026 | OWASP ASI06 — Memory & Context Poisoning | Formal recognition of memory poisoning as a top-10 risk for agentic AI applications | [OWASP Gen AI](https://genai.owasp.org/) |
| 2025 | ALGEN — Few-Shot Embedding Inversion via Cross-Model Alignment (ACL 2025) | Aligns a victim embedding space to the attacker's encoder in one optimization step: one leaked (text, embedding) pair is enough for partial inversion, and 1k samples reaches near-optimum. Tested defenses (noise, quantization, DP) all failed, and attacks transfer across domains and languages | [ACL Anthology](https://aclanthology.org/2025.acl-long.1185/) |
| 2025 | RAGuard — Expand-and-Filter Poisoning Detection (arXiv, Oct 2025) | Widens retrieval scope to dilute poisoned chunks, then applies chunk-wise perplexity filtering and cross-document similarity filtering. Non-parametric, holds up against adaptive attacks on large-scale datasets | [arXiv:2510.25025](https://arxiv.org/abs/2510.25025) |
| 2026 | HubScan — Adversarial Hubness Detection for RAG (Feb 2026) | Multi-detector scanner (MAD-based hubness z-scores, cross-cluster spread, stability under query perturbation, domain-aware detection) covering FAISS, Pinecone, Qdrant, Weaviate with vector, hybrid, and lexical retrieval. Hits 90% recall at a 0.2% alert budget (100% at 0.4%) on 1M MS MARCO documents | [arXiv:2602.22427](https://arxiv.org/abs/2602.22427) |
| 2026 | Black-Hole Attack — Embedding Space Defects (arXiv, April 2026) | Injects malicious vectors at the global or per-cluster centroid of the embedding space; up to 99.85% of top-10 retrievals hit poisoned vectors regardless of query. Existing hubness mitigations trade off accuracy for protection and don't cover targeted hubs | [arXiv:2604.05480](https://arxiv.org/abs/2604.05480) |
| 2026 | PIDP-Attack — Compound Query + Corpus RAG Poisoning (March 2026) | Query-agnostic compound attack: a universal injection suffix appended to queries plus a small number of poisoned passages lifts attack success to ~98.1% across Natural Questions, HotpotQA, MS-MARCO on eight LLMs; 4–16% above PoisonedRAG | [arXiv:2603.25164](https://arxiv.org/abs/2603.25164) |
| 2026 | OWASP Agent Memory Guard (Incubator, Q1 2026) | Reference implementation for OWASP ASI06: SHA-256 memory baselines, YAML policy engine, drop-in LangChain/LlamaIndex/CrewAI middleware, forensic snapshot + rollback, roadmap targets vector-store protection and ML anomaly detection for v1.0 (Q4 2026) | [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/) |
| 2026 | Microsoft Agent Governance Toolkit (MIT-licensed, April 2026) | Stateless Agent OS policy engine intercepting every agent action at sub-millisecond p99 latency; Cross-Model Verification Kernel with majority voting specifically targets memory poisoning, with integrations for LangChain, LangGraph, AutoGen, OpenAI Agents SDK, Haystack, PydanticAI | [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) |
| 2026 | Milvus 2.6.x — RBAC hardening (ongoing 2026) | Fixed RBAC ETCD prefix-matching bug and permission checks that failed to resolve collection aliases, added automatic grant cleanup on collection drop/rename, introduced configurable TLS minimum version for object storage and replication topology inspection | [Milvus release notes](https://milvus.io/docs/release_notes.md) |
| 2026 | Towards Secure RAG — Threats, Defenses, Benchmarks Survey (arXiv 2603.21654, Mar 2026) | Taxonomy covering 40+ poisoning, inversion, membership inference, and scope leakage attacks alongside mitigations and benchmark gaps; useful index for control mapping | [arXiv:2603.21654](https://arxiv.org/abs/2603.21654) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Vector databases:** Pinecone (namespaces, per-index RBAC, BYOC mode GA 2024, BYOK encryption, SOC 2/HIPAA/ISO 27001/GDPR), Weaviate (multi-tenancy since v1.20, tenant-aware classes with lifecycle endpoints, ACLs, HIPAA on AWS since 2025, SOC 2 Type II), Qdrant (first-class multitenancy, JWT authentication, read-only API keys, TLS, Prometheus/Grafana integration, SOC 2 Type II, HIPAA-ready enterprise), Milvus (RBAC with partition keys, TTL since v2.3; 2.6.x line through early 2026 added fixes for RBAC ETCD prefix matching, alias-aware permission checks, automatic grant cleanup on drop/rename, configurable TLS minimum version for object storage, and replication topology inspection), Oracle MySQL HeatWave (vector embeddings with mature RBAC via roles and grants). HoneyBee (2025) provides efficient dynamic RBAC partitioning for vector databases achieving 13.5x latency improvement over row-level security
- **Embedding privacy defenses:** SPARSE framework (ICLR 2026, concept-aware selective perturbation), DPPN (2025, privacy-neuron perturbation reducing leakage 5-78%), Eguard (Nov 2025, transformer-based projection network protecting 95%+ tokens from inversion at 98% downstream task consistency), dimensionality reduction via PCA/random projection, additive Gaussian noise calibrated to privacy budgets, vector quantization (shown to reduce Vec2Text reconstruction). **New attack benchmark:** Zero2Text (Feb 2026) achieves training-free cross-domain inversion with 1.8x ROUGE-L improvement over baselines, raising the bar for defense evaluation
- **RAG frameworks:** LlamaIndex (metadata filtering, callback logging), LangChain (retrievers with metadata-based access control), Mem0.ai (AI memory security best practices and write-ahead validation)
- **PII detection:** Microsoft Presidio, AWS Comprehend, Google DLP API — integrate pre-embedding in ingestion pipelines
- **RAG poisoning defenses:** RAGuard (NeurIPS 2025 — adversarial retriever training + zero-knowledge inference patch, label-free), RAGuard (arXiv:2510.25025, Oct 2025 — separate expand-and-filter non-parametric detector using perplexity + cross-document similarity, robust under adaptive attacks), SDAG (Sparse Document Attention, Feb 2026 — block-sparse attention mask preventing cross-document interaction, no fine-tuning needed), HubScan (Feb 2026 — multi-detector adversarial hubness scanner with 90% recall at 0.2% alert budget across FAISS, Pinecone, Qdrant, Weaviate), hybrid BM25 + vector retrieval (reduces gradient-guided poisoning from 38% to 0%, though joint sparse+dense optimization partially circumvents at 20–44%), perplexity filtering to detect statistically unnatural documents, cross-encoder re-ranking to verify retrieved document relevance, embedding-anomaly detection at ingestion (reduces poisoning success from 95% to 20% standalone per recent comparative studies). RSB benchmark (2025) and the "Towards Secure RAG" survey (arXiv:2603.21654, Mar 2026) provide standardized evaluation and a threat/defense taxonomy. **Centrality-driven hubness (Black-Hole Attack, April 2026) remains largely undefended** — existing hubness-balancing methods like NeighborRetr (CVPR 2025) trade retrieval accuracy for partial mitigation, and targeted hubs crafted for specific concepts evade global detection
- **Prompt injection detection in retrieved content:** Rebuff, Lakera Guard, Prompt Security (real-time scanning of prompts/responses/retrieval payloads), custom NLI-based classifiers
- **Red-teaming and adversarial testing:** Garak, PyRIT, Promptfoo (RAG-specific red-teaming scenarios), Palo Alto Prisma AIRS (automated agent security testing)
- **Agent memory security:** Mem0.ai (memory security best practices), Amazon Bedrock Guardrails (prompt-attack policies), Palo Alto Prisma AIRS and Advanced URL Filtering, **OWASP Agent Memory Guard** (Q1 2026 incubator — reference implementation for ASI06 with SHA-256 memory baselines, YAML policy engine, drop-in middleware for LangChain / LlamaIndex / CrewAI, forensic snapshots and rollback), **Microsoft Agent Governance Toolkit** (MIT-licensed, April 2026 — stateless policy engine intercepting every agent action at sub-millisecond latency, Cross-Model Verification Kernel with majority voting for memory integrity, integrations with LangChain, LangGraph, AutoGen, Haystack, OpenAI Agents SDK, PydanticAI)
- **Data cleanup:** TTL-based expiration (Milvus v2.3+, Redis), application-layer deletion jobs (Pinecone), tombstone-based deletion with compaction, tenant lifecycle APIs (Qdrant, Weaviate)
- **Infrastructure isolation:** VPC peering / private link (Pinecone, Weaviate, Qdrant), BYOC deployments (Pinecone), region pinning for jurisdictional data segregation

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C8.1 Access Controls on Memory & RAG Indices | Medium-High | Major managed DBs now offer RBAC, JWT auth, namespaces, and compliance certifications (SOC 2, HIPAA, ISO 27001). Qdrant added first-class multitenancy. HoneyBee (2025) demonstrated practical dynamic RBAC partitioning at 13.5x lower latency than row-level security. Anomaly detection (8.1.6) has its first dedicated framework in RAGuard (NeurIPS 2025) and its first open scanner in HubScan (Feb 2026, 90% recall at a 0.2% alert budget across FAISS/Pinecone/Qdrant/Weaviate), though no vector DB offers native anomaly detection. Milvus 2.6.x (2026) tightened RBAC alias resolution and added grant cleanup on collection drop/rename. RSB benchmark (2025) and the "Towards Secure RAG" survey (arXiv:2603.21654, Mar 2026) provide standardized attack/defense evaluation. |
| C8.2 Embedding Sanitization & Validation | Medium | PII detection and encoding validation are well-supported. Outlier detection and contradiction checking require custom implementations. The ACM AISec data loader study (74.4% ASR across 357 scenarios) showed that format-level attacks (font poisoning, homoglyphs) bypass all tested loaders including LangChain and LlamaIndex, requiring format-aware sanitization per file type. MINJA's progressive shortening makes static outlier detection insufficient. A-MemGuard shows even LLM-based classifiers miss 66% of poisoned entries. As of April 2026, centrality-driven hubness (Black-Hole Attack) exposes a deeper problem: poisoned vectors placed near the centroid remain statistically "normal" under density-based outlier checks yet still dominate retrieval. Hubness-aware scanners (HubScan) and expand-and-filter pipelines (RAGuard, Oct 2025) are now the closest thing to a practical defense, alongside SDAG (Feb 2026) and hybrid BM25+vector retrieval. PIDP-Attack (March 2026) further shows that query-path manipulation bypasses corpus-only sanitization, so ingestion-time checks alone are no longer sufficient. |
| C8.3 Memory Expiry, Revocation & Deletion | Medium | Milvus v2.3+ TTL, Qdrant tenant lifecycle APIs, and Weaviate tenant lifecycle endpoints improve native support. Deletion propagation to derived indices and caches still requires custom engineering. Crypto-shredding support remains rare. |
| C8.4 Prevent Embedding Inversion & Leakage | Low-Medium | SPARSE (ICLR 2026), DPPN (2025), and Eguard (Nov 2025, 95%+ token protection at 98% utility) provide targeted privacy defenses that preserve utility better than blanket noise. The attacker side advanced significantly: Zero2Text (Feb 2026) achieves training-free cross-domain inversion with 1.8x ROUGE-L improvement over baselines in strict black-box scenarios, joining ZSinvert in making model-agnostic inversion practical. ALGEN (ACL 2025) is even more concerning: a single leaked (text, embedding) pair enables partial inversion via one-step cross-model alignment, and the authors confirmed that noise, quantization, and DP-style defenses all failed to block it in their evaluation. Application-layer encryption still breaks similarity search. ACM RecSys 2025 reproducibility study provides starting benchmarks. No standard regression test suite exists yet. |
| C8.5 Scope Enforcement for User-Specific Memory | Medium-High | Pre-filter and post-filter patterns well-understood. First-class multitenancy in Qdrant and Weaviate strengthens pre-filter layer. Per-tenant encryption requires BYOC/self-hosted. Multi-agent isolation remains challenging — OWASP ASI06, the Multi-Agentic System Threat Modelling Guide (April 2025), OWASP Agent Memory Guard (Q1 2026 incubator, reference implementation for ASI06), and Microsoft's Agent Governance Toolkit (April 2026, Cross-Model Verification Kernel with majority voting for memory integrity) provide both guidance and runtime controls. |

---

## Open Research Questions

- [ ] How do you enforce RBAC in vector databases that don't natively support it? (Qdrant and Weaviate now offer native solutions; Chroma and FAISS still lack RBAC)
- [x] What's the practical risk of embedding inversion for modern high-dimensional embeddings? — Partially answered: Vec2Text achieves 92% reconstruction on 32-token inputs; OWASP LLM08:2025 estimates 50-70% word recovery; ACM RecSys 2025 reproducibility study provides nuanced benchmarks per model. Transfer attacks (ACL 2024) mean attackers do not need the original model.
- [ ] How should memory expiry policies differ for conversation memory vs. knowledge base memory? Especially given MINJA's temporal decoupling where poison planted today executes weeks later.
- [ ] What sanitization is adequate for content entering RAG pipelines? Sunil et al. (2025) showed no single signal is sufficient — composite trust scoring needed. A-MemGuard found LLM classifiers miss 66% of poisoned entries. CorruptRAG (Jan 2026) raised the bar further: a single optimized document achieves 98.2% success, and Semantic Chameleon (Mar 2026) showed corpus-adaptive poisoning defeats static detectors. SDAG (Feb 2026) offers a promising inference-time defense via sparse attention.
- [ ] Can homomorphic encryption or encrypted search schemes enable similarity search on encrypted vectors at practical latency?
- [x] What is the optimal noise calibration for embedding privacy that preserves retrieval utility above acceptable thresholds? — Partially answered: SPARSE (Feb 2026) uses Mahalanobis mechanism with elliptical noise calibrated by dimension sensitivity. DPPN (2025) perturbs only privacy-sensitive neurons, reducing leakage 5-78% while improving utility 14-40%.
- [ ] How should contradiction detection scale for large, rapidly-evolving knowledge bases? Microsoft's Feb 2026 report shows 50+ real-world slow-burn poisoning campaigns, increasing urgency.
- [ ] How can write-ahead validation effectively prevent MINJA-style query-only memory injection while maintaining agent usability?
- [ ] What architectural patterns best defend against "vector worms" — self-propagating poisoned embeddings that instruct models to re-embed and spread contamination?
- [ ] How should memory quarantine and forensic investigation workflows be standardized across different vector database backends?
- [ ] How effective are inference-time defenses (e.g., SDAG sparse attention, cross-encoder re-ranking) compared to ingestion-time defenses against single-document attacks like CorruptRAG? Can they be layered effectively? Early evidence suggests hybrid BM25+vector retrieval eliminates gradient-guided attacks but joint sparse+dense optimization circumvents at 20–44%.
- [ ] As of March 2026, both ZSinvert and Zero2Text enable training-free embedding inversion across any model in black-box settings — what minimum privacy transform (SPARSE, DPPN, Eguard, or combinations) is needed to stay ahead of model-agnostic inversion?
- [ ] How should ingestion pipelines defend against format-level poisoning (font poisoning, homoglyphs, zero-size fonts) that bypass all tested data loaders at 74.4–100% ASR? Is format-aware sanitization per file type (DOCX, HTML, PDF) the only viable approach, or can embedding-level defenses catch these?
- [ ] Can RAGuard's adversarial retriever training generalize to unseen poisoning strategies, or does it require continuous retraining as new attack methods (e.g., Semantic Chameleon's corpus-adaptive approach) emerge?
- [ ] As of April 2026, the Black-Hole Attack shows centrality-driven hubness is a geometric property of high-dimensional embedding spaces, not a bug in any one model. Can retrievers be engineered (hub-aware indexing, isotropy-regularized embeddings, NeighborRetr-style rebalancing) to close this class of attack without trading away retrieval accuracy? HubScan detects it post-hoc but does not eliminate it at the index level.
- [ ] Ingestion-only sanitization assumes attackers can't shape the query path. PIDP-Attack (March 2026) breaks that assumption with a universal query suffix. What architectural patterns jointly defend corpus and query paths without requiring users to accept measurable reductions in retrieval recall?
- [ ] ALGEN (ACL 2025) demonstrated that one leaked (text, embedding) pair bootstraps cross-model inversion and defeats the standard privacy transforms. What minimum combination of privacy-preserving embeddings (SPARSE, DPPN, Eguard) plus operational controls (limiting embedding egress, rotating embedding models) keeps inversion risk acceptable for regulated data?
- [ ] How should Agent Memory Guard-style cryptographic baselines (SHA-256 hashes, snapshot + rollback, declarative YAML policies) scale to continuously-written conversational memory and large RAG corpora without creating excessive review or storage overhead?

---

## Related Standards & Cross-References

- [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/)
- [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP ASI06:2026 Memory & Context Poisoning (Top 10 for Agentic Applications)](https://genai.owasp.org/)
- [OWASP Agent Memory Guard (Incubator, Q1 2026)](https://owasp.org/www-project-agent-memory-guard/)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Multi-Agentic System Threat Modelling Guide (April 2025)](https://www.aigl.blog/content/files/2025/04/Agentic-AI-MAS-Threat-Modelling-Guide-v1-FINAL.pdf)
- [Microsoft Agent Governance Toolkit (microsoft/agent-governance-toolkit, April 2026)](https://github.com/microsoft/agent-governance-toolkit)
- [Towards Secure RAG — Threats, Defenses, Benchmarks Survey (arXiv:2603.21654, March 2026)](https://arxiv.org/abs/2603.21654)
- [MITRE ATLAS: RAG Poisoning](https://atlas.mitre.org/techniques/AML.T0070)
- [MITRE ATLAS: False RAG Entry Injection](https://atlas.mitre.org/techniques/AML.T0071)
- [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
- [MITRE ATLAS: Invert AI Model](https://atlas.mitre.org/techniques/AML.T0024.001)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C02 Data Lifecycle | Data classification and retention policies | C02 covers data governance broadly; C08 applies it to vector stores and embeddings specifically |
| C03 Data Sanitization | Input validation and sanitization | C03 covers general AI input sanitization; C08.2 focuses on pre-embedding sanitization |
| C05 Agent Security | Multi-agent memory isolation | C05 covers agent architecture; C08.5.5 addresses memory namespace isolation for agents |
| C10 Privacy | PII detection and deletion rights | C10 covers privacy broadly; C08 addresses embedding-specific privacy risks (inversion, membership inference) |
| C14 Logging & Monitoring | Retrieval event logging, tripwires, and anomaly detection | C14 covers observability; C08.1.4 specifies RAG retrieval event logging, and C08.1.5-8.1.6 specify retrieval tripwires (canary documents) and anomaly detection |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

## Related Pages

- [C08-01 Access Controls on Memory & RAG Indices](C08-01-Access-Controls-Memory-RAG.md) — section-level treatment of RBAC, scoped credentials, provenance tagging, retrieval logging and anomaly detection for vector stores.
- [C08-04 Embedding Inversion & Leakage Prevention](C08-04-Embedding-Inversion-Leakage-Prevention.md) — companion section on defenses against inversion and membership inference (SPARSE, DPPN, Eguard) and regression testing of privacy transforms.
- [C05-06 Multi-Tenant Isolation](../C05-Access-Control/C05-06-Multi-Tenant-Isolation.md) — cross-chapter counterpart for multi-tenant isolation covering network default-deny, tenant identity, namespace segregation, CMK encryption, and KV-cache partitioning.

---
