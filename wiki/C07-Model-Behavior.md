# C07: Model Behavior, Output Control & Safety Assurance

> **Source:** [`1.0/en/0x10-C07-Model-Behavior.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C07-Model-Behavior.md)
> **Requirements:** 30 | **Sections:** 8

## Control Objective

This control category ensures that model outputs are technically constrained, validated, and monitored so that unsafe, malformed, or high-risk responses cannot reach users or downstream systems.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C7.1 | Output Format Enforcement | 4 | 7.1.1–7.1.4 |
| C7.2 | Hallucination Detection & Mitigation | 4 | 7.2.1–7.2.4 |
| C7.3 | Output Safety & Privacy Filtering | 6 | 7.3.1–7.3.6 |
| C7.4 | Output & Action Limiting | 3 | 7.4.1–7.4.3 |
| C7.5 | Explainability & Transparency | 3 | 7.5.1–7.5.3 |
| C7.6 | Monitoring Integration | 3 | 7.6.1–7.6.3 |
| C7.7 | Generative Media Safeguards | 5 | 7.7.1–7.7.5 |
| C7.8 | Source Attribution & Citation Integrity | 2 | 7.8.1–7.8.2 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Hallucination leading to incorrect medical, legal, or financial advice
- Output containing executable code (XSS, SQL injection) passed to downstream systems
- PII leakage in model responses from memorized training data
- Deepfake generation and synthetic media misuse
- Citation fabrication (fake references that appear legitimate)

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Output validation:** Guardrails AI, NeMo Guardrails (NVIDIA), LLM Guard
- **Hallucination detection:** Vectara HHEM, Lynx, RAGAS faithfulness metrics
- **Structured output:** JSON mode, function calling, constrained decoding (Outlines, Guidance)
- **Content safety:** C2PA for media provenance, SynthID for watermarking

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C7.1 Output Format Enforcement | _TBD_ | |
| C7.2 Hallucination Detection & Mitigation | _TBD_ | |
| C7.3 Output Safety & Privacy Filtering | _TBD_ | |
| C7.4 Output & Action Limiting | _TBD_ | |
| C7.5 Explainability & Transparency | _TBD_ | |
| C7.6 Monitoring Integration | _TBD_ | |
| C7.7 Generative Media Safeguards | _TBD_ | |
| C7.8 Source Attribution & Citation Integrity | _TBD_ | |

---

## Open Research Questions

- [ ] What hallucination rate is acceptable for different risk domains?
- [ ] How do you validate citation accuracy at scale without human review?
- [ ] What's the best approach for output filtering that doesn't degrade model utility?
- [ ] How should generative media safeguards adapt as generation quality improves?

---

## Related Standards & Cross-References

- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/)
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

