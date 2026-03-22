# C07: Model Behavior, Output Control & Safety Assurance

> **Source:** [`1.0/en/0x10-C07-Model-Behavior.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C07-Model-Behavior.md)
> **Requirements:** 33 | **Sections:** 8

## Control Objective

This control category ensures that model outputs are technically constrained, validated, and monitored so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems.

> **2025-2026 Highlights:** Hallucination detection (C7.2) now includes tool-invocation-aware signals alongside confidence scoring, reflecting 2025-2026 research on grounding verification. Source attribution (C7.8) requirements address RAG citation integrity as retrieval-augmented generation becomes standard.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C7.1 | Output Format Enforcement | 4 | [C07-01-Output-Format-Enforcement](C07-01-Output-Format-Enforcement) |
| C7.2 | Hallucination Detection & Mitigation | 5 | [C07-02-Hallucination-Detection](C07-02-Hallucination-Detection) |
| C7.3 | Output Safety & Privacy Filtering | 8 | [C07-03-Output-Safety-Privacy-Filtering](C07-03-Output-Safety-Privacy-Filtering) |
| C7.4 | Output & Action Limiting | 3 | [C07-04-Output-Action-Limiting](C07-04-Output-Action-Limiting) |
| C7.5 | Explainability & Transparency | 3 | [C07-05-Explainability-Transparency](C07-05-Explainability-Transparency) |
| C7.6 | Monitoring Integration | 3 | [C07-06-Monitoring-Integration](C07-06-Monitoring-Integration) |
| C7.7 | Generative Media Safeguards | 5 | [C07-07-Generative-Media-Safeguards](C07-07-Generative-Media-Safeguards) |
| C7.8 | Source Attribution & Citation Integrity | 2 | [C07-08-Source-Attribution-Citation-Integrity](C07-08-Source-Attribution-Citation-Integrity) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Hallucination at scale** — Stanford's 2024 AI Index documented 233 safety incidents (up 56.4% from 2023). LLMs hallucinate at least 75% of the time on court rulings. A database now tracks 486 documented cases of hallucinated legal content. Global cost of AI hallucinations estimated at $67.4 billion in 2024.
- **Output injection to downstream systems** — EchoLeak (CVE-2025-32711, CVSS 9.3) demonstrated zero-click data exfiltration from Microsoft 365 Copilot via prompt injection in emails. LLM outputs passed to `eval()`, shell commands, or rendered in browsers without encoding enable RCE, XSS, and SQL injection (OWASP LLM05:2025).
- **Deepfake misuse** — Arup lost $25.6M to a deepfake video conference (Jan 2024). Deepfake attacks occurred at one every five minutes in 2024. The TAKE IT DOWN Act (May 2025) criminalizes non-consensual intimate deepfakes in the U.S.
- **Citation fabrication** — NeurIPS 2025 had 100+ hallucinated citations across 53+ accepted papers. Studies show ChatGPT fabricates 39-55% of citations; even GPT-4 produces 18-29% fabricated references.
- **Safety filter bypasses** — JBFuzz (2025) achieves ~99% jailbreak success across GPT-4o, Llama 3, Gemini 2.0, DeepSeek-R1 in under 1 minute. Skeleton Key, Crescendo, and Context Compliance Attack represent distinct bypass families.
- **PII and training data leakage** — Researchers extracted 10,000+ verbatim memorized examples from ChatGPT for ~$200. Multi-query attacks achieve 39% PII extraction rates. 77% of employees leak data via ChatGPT.
- **Excessive agency** — 80% of organizations report encountering risky AI agent behavior. Incidents include production environment modifications during code freezes and autonomous file destruction.
- **System prompt leakage** — Now OWASP LLM07:2025. All frontier models tested leaked viable prompt approximations under argument-based jailbreaks.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Jun 2025 | EchoLeak (CVE-2025-32711, CVSS 9.3) — zero-click Microsoft 365 Copilot exfiltration | Crafted email causes Copilot to exfil OneDrive/SharePoint/Teams data without user interaction | [Hack The Box](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability) |
| Jan 2026 | NeurIPS 2025 hallucinated citations — 100+ fabricated refs in 53+ papers | Citation fabrication unnoticed by peer review; blended real papers with invented co-authors | [Fortune](https://fortune.com/2026/01/21/neurips-ai-conferences-research-papers-hallucinations/) |
| Jan 2024 | Arup deepfake video conference — $25.6M wire fraud | All participants on the call were deepfakes; worker authorized 15 wire transfers | [BBC News](https://www.bbc.com/news/technology-68222117) |
| May 2025 | TAKE IT DOWN Act signed into U.S. federal law | Criminalizes non-consensual intimate deepfakes; platforms must remove within 48 hours | [Congress.gov](https://www.congress.gov/bill/119th-congress/senate-bill/146) |
| 2025 | JBFuzz — ~99% jailbreak success across frontier models | Black-box fuzzing requiring ~7 queries per harmful question, under 1 minute | [Research](https://startup-house.com/blog/llm-jailbreak-techniques) |
| Mar 2025 | Context Compliance Attack (CCA) — simplest effective jailbreak | Injecting fabricated assistant response into conversation history | [Microsoft Research](https://www.microsoft.com/en-us/security/blog/) |
| 2023-05 | Air Canada chatbot hallucination (bereavement policy) | Hallucinated refund policy led to legal liability | [CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116491) |
| 2023-06 | Lawyers sanctioned for ChatGPT-fabricated case citations | 486+ documented cases by 2025; $2K penalties and mandatory CLE | [Reuters](https://www.reuters.com/legal/new-york-lawyers-sanctioned-using-fake-chatgpt-cases-legal-brief-2023-06-22/) |
| 2024-01 | Taylor Swift deepfake — 47M views before takedown | Non-consensual AI-generated explicit imagery exposed platform moderation failures | [NYT](https://www.nytimes.com/2024/01/25/technology/taylor-swift-ai-fake-images.html) |
| 2023-03 | Indirect prompt injection via Bing Chat (Greshake et al.) | Model exfiltrated data by following injected instructions in retrieved content | [arXiv](https://arxiv.org/abs/2302.12173) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Output validation frameworks:** [Guardrails AI](https://www.guardrailsai.com/) (Pydantic-style validators with pre-built hub), [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) (NVIDIA, Colang DSL for programmable rails), [LLM Guard](https://llm-guard.com/) (Protect AI, input/output sanitization scanners), [Rebuff](https://github.com/protectai/rebuff) (multi-layer prompt injection detection with canary tokens)
- **Hallucination detection:** [Vectara HHEM-2.1](https://huggingface.co/vectara/hallucination_evaluation_model) (cross-encoder factual consistency scorer, outperforms GPT-4 at detection), [RAGAS](https://docs.ragas.io/) (RAG evaluation — faithfulness, context precision/recall), [DeepEval](https://github.com/confident-ai/deepeval) (14+ metrics, pytest-native CI/CD integration), [TruLens](https://www.trulens.org/) (groundedness and relevance feedback), [Lynx](https://huggingface.co/PatronusAI/Lynx-70B) (Patronus AI, RAG faithfulness evaluation)
- **Structured output / constrained decoding:** [Outlines](https://dottxt-ai.github.io/outlines/) (FSM token masking, 100% schema compliance, 13.3K stars), [Instructor](https://python.useinstructor.com/) (post-generation validation with retries, 12.3K stars), [Guidance](https://github.com/guidance-ai/guidance) (Microsoft, 19K stars), [PydanticAI](https://ai.pydantic.dev/) (agent framework with structured output, 14.5K stars), [XGrammar/llguidance](https://github.com/guidance-ai/llguidance) (near-zero overhead grammar-guided generation, credited by OpenAI for Structured Outputs)
- **Content safety classifiers:** [LlamaGuard 4](https://llama.meta.com/) (Meta, 12B multimodal, MLCommons taxonomy), [ShieldGemma](https://arxiv.org/abs/2407.21772) (Google, 2B/9B/27B sizes, exceeds GPT-4 F1 by 6.4%), [GPT-OSS-Safeguard](https://developers.openai.com/cookbook/articles/gpt-oss-safeguard-guide/) (OpenAI, Oct 2025, policy-following with reasoning traces, Apache 2.0), [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation), [Azure AI Content Safety](https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety), [Perspective API](https://perspectiveapi.com/)
- **Media provenance & watermarking:** [C2PA v2.2](https://c2pa.org/) (April 2025 — cryptographic Content Credentials; adopted by Adobe, Google, camera makers), [SynthID](https://deepmind.google/technologies/synthid/) (Google, 10B+ watermarks as of 2025, text watermarking open-sourced), [Meta Video Seal](https://github.com/facebookresearch/videoseal) (Dec 2024, open-source video watermarking)
- **PII detection in outputs:** [Microsoft Presidio](https://microsoft.github.io/presidio/) (open-source, pluggable NER, 10+ languages), [Nightfall AI](https://www.nightfall.ai/) (2x precision over AWS Comprehend/Google DLP), AWS Comprehend PII (30+ entity types), [Google Cloud DLP](https://cloud.google.com/security/products/dlp) (150+ infoTypes)
- **RAG attribution:** [Google Vertex AI Check Grounding API](https://cloud.google.com/generative-ai-app-builder/docs/check-grounding) (verifies response grounding, returns unsupported claims), [GaRAGe Benchmark](https://arxiv.org/abs/2506.07671) (2,366 questions, 35K+ annotations for citation accuracy evaluation)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C7.1 Output Format Enforcement | Mature | Outlines achieves 100% schema compliance via FSM token masking. JSON mode available in all major providers. XGrammar/llguidance add near-zero overhead. |
| C7.2 Hallucination Detection & Mitigation | Maturing | HHEM-2.1, RAGAS, DeepEval provide production-ready metrics. Vertex AI Check Grounding offers API-level verification. Still no standardized cross-vendor benchmark. |
| C7.3 Output Safety & Privacy Filtering | Mature | LlamaGuard 4, ShieldGemma, GPT-OSS-Safeguard (open-weight, Apache 2.0) offer multiple classifier options. Presidio handles PII well. C7.3.7 (system prompt leak prevention) and C7.3.8 (auto-render blocking) are newer requirements with less established tooling. |
| C7.4 Output & Action Limiting | Mature | Rate limiting, confirmation flows, and tool allowlists are well-understood patterns. OWASP LLM06 provides clear prevention guidance. |
| C7.5 Explainability & Transparency | Emerging | SHAP/LIME work for classification but CoT faithfulness remains unverifiable for LLMs. Mechanistic interpretability (sparse autoencoders) is research-stage. EU AI Act pressure driving adoption. |
| C7.6 Monitoring Integration | Maturing | Standard observability (Prometheus/Grafana) applies; AI-specific safety violation dashboards emerging. 80% of orgs report encountering risky agent behavior. |
| C7.7 Generative Media Safeguards | Maturing | C2PA v2.2 adopted by Adobe/Google/camera makers. SynthID has 10B+ watermarks. Detection evasion remains an arms race — detectors lose up to 50% accuracy on novel deepfakes. EU AI Act Art 50 mandates AI content labeling by Aug 2026. |
| C7.8 Source Attribution & Citation Integrity | Emerging | Vertex AI Check Grounding API exists but up to 57% of RAG citations may be post-rationalized. Citation accuracy averages 65-70% without explicit attribution training. GaRAGe benchmark (2025) standardizing evaluation. |

---

## Related Standards & Cross-References

- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/) — covers downstream XSS, SQL injection, RCE from untrusted LLM outputs; linked to LLM01 and LLM06 attack chains
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — three root causes: poorly designed integrations, unchecked tool access, lack of usage monitoring
- [OWASP LLM07:2025 System Prompt Leakage](https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/) — new in 2025; all frontier models tested leak prompt approximations
- [MITRE ATLAS](https://atlas.mitre.org/) — AML.T0054 (LLM Jailbreak), AML.T0051 (Prompt Injection — .000 Direct, .001 Indirect), AML.T0064 (Discover Hallucinations), AML.T0048 (External Harms), AML.T0015 (Evade ML Model)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) (July 2024) — 12 GenAI risk categories including Confabulation, Dangerous Content, Information Integrity, Harmful Bias, and Obscene Content
- [EU AI Act Article 50](https://artificialintelligenceact.eu/article/50/) — Transparency obligations for AI-generated content (enforceable Aug 2026). Multi-layered marking: metadata embedding, watermarking, fingerprinting. Common EU-wide "AI" visual icon for synthetic content. Deepfake-specific labeling rules.
- [C2PA Specification v2.2](https://c2pa.org/) (April 2025) — cryptographic Content Credentials for media provenance; adopted by Adobe, Google, Nikon, Canon, Sony
- [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) (July 2025) — 243 controls across 18 domains including Model Security and Application & Interface Security
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) — AI management systems; transparency and explainability provisions

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C02 User Input Validation](C02-User-Input-Validation.md) | Input/output attack chain | OWASP LLM05 explicitly chains with LLM01 (Prompt Injection). MITRE AML.T0051 (Prompt Injection) directly causes output manipulation. Input validation (C02) is the first defense; output controls (C07) are the last. |
| [C06 Supply Chain](C06-Supply-Chain.md) | Behavioral impact of compromised models | MITRE AML.T0043.004 (Insert Backdoor Trigger) shows supply chain compromise altering model behavior. NIST AI 600-1 "Value Chain & Component Integration" risk category. |
| [C09 Orchestration & Agents](C09-Orchestration-and-Agents.md) | Action limiting, tool use | OWASP LLM06 (Excessive Agency) is the direct bridge. LLM05 + LLM06 combined create attack chains where malicious output triggers unauthorized agent actions. |
| [C11 Adversarial Robustness](C11-Adversarial-Robustness.md) | Safety filter robustness | MITRE AML.T0054 (LLM Jailbreak) and AML.T0015 (Evade ML Model) target output filter robustness. JBFuzz achieves ~99% bypass rates against current models. |
| [C12 Privacy](C12-Privacy.md) | PII in outputs, memorization | C7.3 PII filtering overlaps with C12 privacy controls. Training data extraction attacks (10K+ examples for ~$200) bridge output safety and privacy. EU AI Act Art 50 intersects with GDPR when outputs contain personal data. |
| [C13 Monitoring & Logging](C13-Monitoring-and-Logging.md) | Safety violation monitoring | OWASP LLM06 root cause 3 is "Lack of Usage Monitoring." C7.6 monitoring requirements feed into C13 centralized logging. MITRE AML.T0065 involves reconnaissance of model behaviors. |
| [C14 Human Oversight](C14-Human-Oversight.md) | Human-in-the-loop | C7.3.6 human approval step relates to C14 oversight patterns. EU AI Act Art 50 allows text disclosure exemption when human review with editorial control is applied. NIST AI 600-1 "Human-AI Configuration" risk category. |

---

## Open Research Questions

- [ ] **Can hallucination detection scale to real-time production use?** — HHEM-2.1 runs in 0.6s on RTX 3090 vs ~35s for RAGAS with GPT-4. Cross-encoder models are fast but miss complex multi-hop reasoning errors. No standardized cross-vendor benchmark exists yet.
- [ ] **How effective are current jailbreak defenses?** — JBFuzz achieves ~99% success across frontier models with ~7 queries. Multi-turn jailbreaks exceed 70% success rates. Constitutional AI and RLHF improve single-turn safety but multi-turn and compositional attacks remain largely unsolved.
- [ ] **Will C2PA and watermarking survive adversarial manipulation?** — C2PA metadata can be stripped from files. Deepfake detectors lose up to 50% accuracy on novel content not in training data. EU AI Act Art 50 mandates multi-layered marking, but robustness against determined adversaries is uncertain.
- [ ] **Can RAG citation verification become reliable?** — Up to 57% of RAG citations are post-rationalized. Citation accuracy averages 65-70% without explicit attribution training. Vertex AI Check Grounding API is a start, but claim-level verification (C7.8.2) remains a hard problem.
- [ ] **How should explainability requirements apply to LLMs?** — CoT explanations cannot be verified by asking the LLM itself. Mechanistic interpretability (sparse autoencoders) is promising but pre-production. EU AI Act explainability obligations for high-risk systems take effect Aug 2026.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
