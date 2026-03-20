# C11: Adversarial Robustness & Attack Resistance

> **Source:** [`1.0/en/0x10-C11-Adversarial-Robustness.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C11-Adversarial-Robustness.md)
> **Requirements:** 38 | **Sections:** 9

## Control Objective

Ensure that AI systems remain reliable, privacy-preserving, and abuse-resistant when facing evasion, inference, extraction, or poisoning attacks. These controls cover model alignment testing, adversarial hardening, privacy attack resistance, model theft deterrence, and security adaptation for autonomous agents.

> **2025-2026 Highlights:** Alignment evaluation now includes assessment for evaluation awareness (C11.1.5), where models may behave differently under testing versus deployment. Agent-specific sections (C11.8, C11.9) address self-modification and autonomous update security as agentic systems become mainstream.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C11.1 | Model Alignment & Safety | 5 | [C11-01-Model-Alignment-Safety](C11-01-Model-Alignment-Safety) |
| C11.2 | Adversarial-Example Hardening | 5 | [C11-02-Adversarial-Example-Hardening](C11-02-Adversarial-Example-Hardening) |
| C11.3 | Membership-Inference Mitigation | 3 | [C11-03-Membership-Inference-Mitigation](C11-03-Membership-Inference-Mitigation) |
| C11.4 | Model-Inversion Resistance | 3 | [C11-04-Model-Inversion-Resistance](C11-04-Model-Inversion-Resistance) |
| C11.5 | Model-Extraction Defense | 5 | [C11-05-Model-Extraction-Defense](C11-05-Model-Extraction-Defense) |
| C11.6 | Inference-Time Poisoned-Data Detection | 5 | [C11-06-Inference-Time-Poisoned-Data-Detection](C11-06-Inference-Time-Poisoned-Data-Detection) |
| C11.7 | Security Policy Adaptation | 4 | [C11-07-Security-Policy-Adaptation](C11-07-Security-Policy-Adaptation) |
| C11.8 | Agent Security Self-Assessment | 3 | [C11-08-Agent-Security-Self-Assessment](C11-08-Agent-Security-Self-Assessment) |
| C11.9 | Self-Modification & Autonomous Update Security | 5 | [C11-09-Self-Modification-Autonomous-Update-Security](C11-09-Self-Modification-Autonomous-Update-Security) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Adversarial examples** causing misclassification (image perturbations, text paraphrases, audio overlays)
- **Membership inference** -- determining if specific data was in the training set
- **Model inversion** -- reconstructing training data or sensitive attributes from model outputs
- **Model extraction** -- stealing model weights or functionality through API queries
- **Inference-time poisoning** via compromised RAG corpora, tool outputs, or injected context
- **Alignment bypass** through jailbreaks, prompt manipulation, and multi-turn escalation
- **Self-modification abuse** -- adversarially induced changes to agent behavior or configuration

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

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C1 Training Data | Data poisoning, data provenance | C1 covers training-time data integrity; C11.6 covers inference-time poisoned data detection |
| C2 User Input Validation | Input filtering and sanitization | C2 handles general input validation; C11.2 addresses adversarial inputs specifically crafted to fool models |
| C7 Model Behavior | Output safety, guardrails | C7 covers behavioral constraints broadly; C11.1 focuses on alignment testing and red-teaming |
| C9 Orchestration and Agents | Agent safety, tool use | C9 covers orchestration security; C11.8-C11.9 address agent self-assessment and self-modification |
| C12 Privacy | Differential privacy, data leakage | C12 covers privacy holistically; C11.3-C11.4 focus on inference/inversion attacks specifically |
| C13 Monitoring and Logging | Detection, alerting | C13 covers monitoring infrastructure; C11.5-C11.7 cover adversarial-specific detection and policy adaptation |

---
