# C07: Model Behavior, Output Control & Safety Assurance

> **Source:** [`1.0/en/0x10-C07-Model-Behavior.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C07-Model-Behavior.md)
> **Requirements:** 31 | **Sections:** 8

## Control Objective

This control category ensures that model outputs are technically constrained, validated, and monitored so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C7.1 | Output Format Enforcement | 4 | [C07-01-Output-Format-Enforcement](C07-01-Output-Format-Enforcement) |
| C7.2 | Hallucination Detection & Mitigation | 5 | [C07-02-Hallucination-Detection](C07-02-Hallucination-Detection) |
| C7.3 | Output Safety & Privacy Filtering | 6 | [C07-03-Output-Safety-Privacy-Filtering](C07-03-Output-Safety-Privacy-Filtering) |
| C7.4 | Output & Action Limiting | 3 | [C07-04-Output-Action-Limiting](C07-04-Output-Action-Limiting) |
| C7.5 | Explainability & Transparency | 3 | [C07-05-Explainability-Transparency](C07-05-Explainability-Transparency) |
| C7.6 | Monitoring Integration | 3 | [C07-06-Monitoring-Integration](C07-06-Monitoring-Integration) |
| C7.7 | Generative Media Safeguards | 5 | [C07-07-Generative-Media-Safeguards](C07-07-Generative-Media-Safeguards) |
| C7.8 | Source Attribution & Citation Integrity | 2 | [C07-08-Source-Attribution-Citation-Integrity](C07-08-Source-Attribution-Citation-Integrity) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Hallucination leading to incorrect medical, legal, or financial advice
- Output containing executable code (XSS, SQL injection) passed to downstream systems
- PII leakage in model responses from memorized training data
- Deepfake generation and synthetic media misuse
- Citation fabrication (fake references that appear legitimate)
- Excessive agency: models taking irreversible actions without user confirmation
- Bypassing content safety filters through adversarial prompts

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2023-05 | Air Canada chatbot hallucination (bereavement policy) | Hallucinated refund policy led to legal liability | [CBC News](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116491) |
| 2023-06 | Lawyers sanctioned for ChatGPT-fabricated case citations | Fabricated legal citations submitted to court | [Reuters](https://www.reuters.com/legal/new-york-lawyers-sanctioned-using-fake-chatgpt-cases-legal-brief-2023-06-22/) |
| 2024-01 | Taylor Swift deepfake incident | Non-consensual AI-generated explicit imagery went viral | [NYT](https://www.nytimes.com/2024/01/25/technology/taylor-swift-ai-fake-images.html) |
| 2023-03 | Indirect prompt injection via Bing Chat | Model exfiltrated data by following injected instructions in retrieved content | [Greshake et al.](https://arxiv.org/abs/2302.12173) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Output validation:** Guardrails AI, NeMo Guardrails (NVIDIA), LLM Guard
- **Hallucination detection:** Vectara HHEM, Lynx, RAGAS faithfulness metrics
- **Structured output:** JSON mode, function calling, constrained decoding (Outlines, Guidance)
- **Content safety:** OpenAI Moderation API, Perspective API, Azure AI Content Safety
- **Media provenance:** C2PA for media provenance, SynthID for watermarking
- **PII detection:** Microsoft Presidio, AWS Comprehend PII, Google DLP

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C7.1 Output Format Enforcement | High | JSON mode, function calling, and constrained decoding are production-ready |
| C7.2 Hallucination Detection & Mitigation | Medium | Confidence scoring and RAG-based verification exist but lack standardized benchmarks |
| C7.3 Output Safety & Privacy Filtering | High | Mature content classifiers and PII detectors available from multiple vendors |
| C7.4 Output & Action Limiting | High | Rate limiting and confirmation flows are well-understood patterns |
| C7.5 Explainability & Transparency | Low | Interpretability methods exist (SHAP, attention maps) but are hard to apply to LLMs at scale |
| C7.6 Monitoring Integration | Medium | Standard observability tools apply; AI-specific dashboards are emerging |
| C7.7 Generative Media Safeguards | Medium | Watermarking (C2PA, SynthID) is maturing; detection of AI-generated media is an active arms race |
| C7.8 Source Attribution & Citation Integrity | Low | RAG attribution is ad-hoc; automated claim-level verification is nascent |

---

## Related Standards & Cross-References

- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [NIST AI 100-2 (Adversarial ML Taxonomy)](https://csrc.nist.gov/pubs/ai/100/2/e2023/final)
- [EU AI Act, Article 52 — Transparency obligations for AI-generated content](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C2 (User Input Validation) | Input/output pipeline | Input validation prevents malicious prompts; output controls catch what input filters miss |
| C9 (Orchestration & Agents) | Action limiting, tool use | C7.4 action limits complement C9 agent guardrails |
| C12 (Privacy) | PII in outputs | C7.3 PII filtering overlaps with C12 privacy controls |
| C13 (Monitoring & Logging) | Logging requirements | C7.6 monitoring requirements feed into C13 logging infrastructure |
| C14 (Human Oversight) | Human-in-the-loop | C7.3.6 human approval step relates to C14 oversight patterns |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
