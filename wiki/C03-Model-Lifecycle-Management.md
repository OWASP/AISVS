# C03: Model Lifecycle Management & Change Control

> **Source:** [`1.0/en/0x10-C03-Model-Lifecycle-Management.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
> **Requirements:** 23 | **Sections:** 6

## Control Objective

AI systems must implement change control processes that prevent unauthorized or unsafe model modifications from reaching production. Only authorized, validated models reach production by employing controlled processes that maintain integrity, traceability, and recoverability.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C3.1 | Model Authorization & Integrity | 4 | 3.1.1–3.1.4 |
| C3.2 | Model Validation & Testing | 4 | 3.2.1–3.2.4 |
| C3.3 | Controlled Deployment & Rollback | 5 | 3.3.1–3.3.5 |
| C3.4 | Secure Development Practices | 4 | 3.4.1–3.4.4 |
| C3.5 | Model Retirement & Decommissioning | 2 | 3.5.1–3.5.2 |
| C3.6 | Hosted and Provider-Managed Model Controls | 4 | 3.6.1–3.6.4 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Model tampering during training or fine-tuning pipeline
- Unauthorized model deployment bypassing validation gates
- Model supply chain attacks (compromised checkpoints on Hugging Face, etc.)
- Stale or vulnerable models remaining in production without rotation

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **MLOps platforms:** MLflow, Weights & Biases, Kubeflow, SageMaker
- **Model signing:** Sigstore/cosign for model artifacts, in-toto attestations
- **Deployment:** Seldon Core, BentoML, TorchServe with canary/blue-green strategies
- **Testing:** Giskard, Deepchecks, Great Expectations (for data validation in pipeline)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C3.1 Model Authorization & Integrity | _TBD_ | |
| C3.2 Model Validation & Testing | _TBD_ | |
| C3.3 Controlled Deployment & Rollback | _TBD_ | |
| C3.4 Secure Development Practices | _TBD_ | |
| C3.5 Model Retirement & Decommissioning | _TBD_ | |
| C3.6 Hosted and Provider-Managed Model Controls | _TBD_ | |

---

## Open Research Questions

- [ ] What's the right cadence for model re-validation in production (drift vs. cost)?
- [ ] How do hosted model providers (OpenAI, Anthropic, Google) handle versioning transparency?
- [ ] What constitutes 'adequate' pre-deployment security testing for fine-tuned models?
- [ ] How should organizations manage rollback for models with stateful fine-tuning?

---

## Related Standards & Cross-References

- [MITRE ATLAS](https://atlas.mitre.org/)
- [MLOps Principles](https://ml-ops.org/content/mlops-principles)
- [Reinforcement fine-tuning (OpenAI)](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
- [What is AI adversarial robustness? (IBM Research)](https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

