# C12: Privacy Protection & Personal Data Management

> **Source:** [`1.0/en/0x10-C12-Privacy.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C12-Privacy.md)
> **Requirements:** 23 | **Sections:** 6

## Control Objective

Maintain rigorous privacy assurances across the entire AI lifecycle (collection, training, inference, and incident response) so that personal data is only processed with clear consent, minimum necessary scope, provable erasure, and formal privacy guarantees.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C12.1 | Anonymization & Data Minimization | 4 | 12.1.1–12.1.4 |
| C12.2 | Right-to-be-Forgotten & Deletion Enforcement | 4 | 12.2.1–12.2.4 |
| C12.3 | Differential-Privacy Safeguards | 4 | 12.3.1–12.3.4 |
| C12.4 | Purpose-Limitation & Scope-Creep Protection | 4 | 12.4.1–12.4.4 |
| C12.5 | Consent Management & Lawful-Basis Tracking | 3 | 12.5.1–12.5.3 |
| C12.6 | Federated Learning with Privacy Controls | 4 | 12.6.1–12.6.4 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Training data memorization leaking PII in model outputs
- Re-identification attacks on anonymized training data
- Inability to truly 'forget' data already learned by a trained model (machine unlearning gap)
- Scope creep — data collected for one purpose being used for model training
- Cross-border data transfer violations in distributed training setups

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Differential privacy:** Opacus, TensorFlow Privacy, Google DP Library
- **PII detection:** Presidio (Microsoft), spaCy NER, Google DLP API
- **Machine unlearning:** SISA training, approximate unlearning methods (research-stage)
- **Federated learning:** PySyft, TensorFlow Federated, Flower
- **Consent management:** OneTrust, TrustArc (integrated with ML pipelines)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C12.1 Anonymization & Data Minimization | _TBD_ | |
| C12.2 Right-to-be-Forgotten & Deletion Enforcement | _TBD_ | |
| C12.3 Differential-Privacy Safeguards | _TBD_ | |
| C12.4 Purpose-Limitation & Scope-Creep Protection | _TBD_ | |
| C12.5 Consent Management & Lawful-Basis Tracking | _TBD_ | |
| C12.6 Federated Learning with Privacy Controls | _TBD_ | |

---

## Open Research Questions

- [ ] Is machine unlearning practical at scale, or is retraining the only reliable option?
- [ ] What epsilon values for differential privacy provide meaningful protection without destroying model utility?
- [ ] How should GDPR Article 17 (right to erasure) apply to foundation models?
- [ ] What constitutes adequate anonymization for AI training data?

---

## Related Standards & Cross-References

- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [General Data Protection Regulation (GDPR)](https://gdpr-info.eu/)
- [California Consumer Privacy Act (CCPA)](https://oag.ca.gov/privacy/ccpa)
- [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

