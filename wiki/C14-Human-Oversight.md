# C14: Human Oversight, Accountability & Governance

> **Source:** [`1.0/en/0x10-C14-Human-Oversight.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C14-Human-Oversight.md)
> **Requirements:** 25 | **Sections:** 7

## Control Objective

This chapter provides requirements for maintaining human oversight and clear accountability chains in AI systems, ensuring explainability, transparency, and ethical stewardship throughout the AI lifecycle.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C14.1 | Kill-Switch & Override Mechanisms | 4 | 14.1.1–14.1.4 |
| C14.2 | Human-in-the-Loop Decision Checkpoints | 4 | 14.2.1–14.2.4 |
| C14.3 | Chain of Responsibility & Auditability | 2 | 14.3.1–14.3.2 |
| C14.4 | Explainable-AI Techniques | 4 | 14.4.1–14.4.4 |
| C14.5 | Model Cards & Usage Disclosures | 4 | 14.5.1–14.5.4 |
| C14.6 | Uncertainty Quantification | 4 | 14.6.1–14.6.4 |
| C14.7 | User-Facing Transparency Reports | 3 | 14.7.1–14.7.3 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Automation bias — humans over-trusting AI outputs without adequate review
- Kill-switch failures in autonomous systems operating at high speed
- Accountability gaps when AI systems make consequential errors
- Opaque AI decision-making in regulated domains (healthcare, finance, criminal justice)
- Model cards that are incomplete or misleading about model limitations

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Explainability:** SHAP, LIME, Captum (PyTorch), InterpretML
- **Model cards:** Model Card Toolkit (Google), Hugging Face model card template
- **Uncertainty:** Conformal prediction, MC Dropout, ensemble methods
- **Human-in-the-loop:** Label Studio, Prodigy, custom approval workflows

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C14.1 Kill-Switch & Override Mechanisms | _TBD_ | |
| C14.2 Human-in-the-Loop Decision Checkpoints | _TBD_ | |
| C14.3 Chain of Responsibility & Auditability | _TBD_ | |
| C14.4 Explainable-AI Techniques | _TBD_ | |
| C14.5 Model Cards & Usage Disclosures | _TBD_ | |
| C14.6 Uncertainty Quantification | _TBD_ | |
| C14.7 User-Facing Transparency Reports | _TBD_ | |

---

## Open Research Questions

- [ ] What level of explainability is adequate for different risk domains?
- [ ] How do you design kill-switches that work for real-time AI systems?
- [ ] What should model cards include for foundation models with broad use cases?
- [ ] How should uncertainty quantification be communicated to non-technical stakeholders?

---

## Related Standards & Cross-References

_No references listed yet._

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

