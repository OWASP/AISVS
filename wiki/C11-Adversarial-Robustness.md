# C11: Adversarial Robustness & Attack Resistance

> **Source:** [`1.0/en/0x10-C11-Adversarial-Robustness.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C11-Adversarial-Robustness.md)
> **Requirements:** 38 | **Sections:** 9

## Control Objective

Ensure that AI systems remain reliable, privacy-preserving, and abuse-resistant when facing evasion, inference, extraction, or poisoning attacks.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C11.1 | Model Alignment & Safety | 5 | 11.1.1–11.1.5 |
| C11.2 | Adversarial-Example Hardening | 5 | 11.2.1–11.2.5 |
| C11.3 | Membership-Inference Mitigation | 3 | 11.3.1–11.3.3 |
| C11.4 | Model-Inversion Resistance | 3 | 11.4.1–11.4.3 |
| C11.5 | Model-Extraction Defense | 5 | 11.5.1–11.5.5 |
| C11.6 | Inference-Time Poisoned-Data Detection | 5 | 11.6.1–11.6.5 |
| C11.7 | Security Policy Adaptation | 4 | 11.7.1–11.7.4 |
| C11.8 | Agent Security Self-Assessment | 3 | 11.8.1–11.8.3 |
| C11.9 | Self-Modification & Autonomous Update Security | 5 | 11.9.1–11.9.5 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Adversarial examples causing misclassification (image perturbations, text paraphrases)
- Membership inference — determining if specific data was in the training set
- Model inversion — reconstructing training data from model outputs
- Model extraction — stealing model weights through API queries
- Poisoning at inference time via compromised RAG or context
- Alignment bypass through jailbreaks and prompt manipulation

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Adversarial testing:** ART (IBM), Adversarial Robustness Toolbox, TextAttack, Garak
- **Privacy:** Opacus (differential privacy for PyTorch), TensorFlow Privacy
- **Model extraction defense:** API rate limiting, output perturbation, watermarking
- **Alignment:** RLHF toolkits, Constitutional AI approaches, red-teaming frameworks

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C11.1 Model Alignment & Safety | _TBD_ | |
| C11.2 Adversarial-Example Hardening | _TBD_ | |
| C11.3 Membership-Inference Mitigation | _TBD_ | |
| C11.4 Model-Inversion Resistance | _TBD_ | |
| C11.5 Model-Extraction Defense | _TBD_ | |
| C11.6 Inference-Time Poisoned-Data Detection | _TBD_ | |
| C11.7 Security Policy Adaptation | _TBD_ | |
| C11.8 Agent Security Self-Assessment | _TBD_ | |
| C11.9 Self-Modification & Autonomous Update Security | _TBD_ | |

---

## Open Research Questions

- [ ] How do you quantify adversarial robustness in a meaningful way for LLMs?
- [ ] What's the practical risk of model extraction for API-served models?
- [ ] How should alignment testing evolve as models become more capable?
- [ ] What self-modification capabilities are safe for autonomous AI systems?

---

## Related Standards & Cross-References

- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/)
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
- [MITRE ATLAS: Infer Training Data Membership](https://atlas.mitre.org/techniques/AML.T0024.000)
- [MITRE ATLAS: Invert ML Model](https://atlas.mitre.org/techniques/AML.T0024.001)
- [MITRE ATLAS: Extract ML Model](https://atlas.mitre.org/techniques/AML.T0024.002)
- [MITRE ATLAS: Backdoor ML Model](https://atlas.mitre.org/techniques/AML.T0018)
- [NIST AI 100-2e2023 Adversarial Machine Learning](https://csrc.nist.gov/pubs/ai/100/2/e2023/final)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

