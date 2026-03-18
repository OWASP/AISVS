# C06: Supply Chain Security for Models, Frameworks & Data

> **Source:** [`1.0/en/0x10-C06-Supply-Chain.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C06-Supply-Chain.md)
> **Requirements:** 33 | **Sections:** 7

## Control Objective

AI supply-chain attacks exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code. These controls provide end-to-end traceability, vulnerability management, and monitoring.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C6.1 | Pretrained Model Vetting & Origin Integrity | 5 | 6.1.1–6.1.5 |
| C6.2 | Framework & Library Scanning | 5 | 6.2.1–6.2.5 |
| C6.3 | Dependency Pinning & Verification | 5 | 6.3.1–6.3.5 |
| C6.4 | Trusted Source Enforcement | 5 | 6.4.1–6.4.5 |
| C6.5 | Third-Party Dataset Risk Assessment | 5 | 6.5.1–6.5.5 |
| C6.6 | Supply Chain Attack Monitoring | 3 | 6.6.1–6.6.3 |
| C6.7 | AI BOM for Model Artifacts | 5 | 6.7.1–6.7.5 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Backdoored pretrained models on Hugging Face or Model Zoo
- Pickle deserialization attacks in model weight files
- Typosquatting attacks on PyPI/npm packages used in ML pipelines
- Compromised training datasets from third-party sources
- Malicious model adapters/LoRA weights with embedded backdoors

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Model scanning:** ModelScan (Protect AI), Fickling (pickle analysis), safetensors format
- **SBOM/MLBOM:** CycloneDX ML extension, SPDX AI profile
- **Dependency scanning:** Dependabot, Snyk, OSV Scanner, Socket.dev
- **Registry security:** Hugging Face model cards, model signing (emerging)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C6.1 Pretrained Model Vetting & Origin Integrity | _TBD_ | |
| C6.2 Framework & Library Scanning | _TBD_ | |
| C6.3 Dependency Pinning & Verification | _TBD_ | |
| C6.4 Trusted Source Enforcement | _TBD_ | |
| C6.5 Third-Party Dataset Risk Assessment | _TBD_ | |
| C6.6 Supply Chain Attack Monitoring | _TBD_ | |
| C6.7 AI BOM for Model Artifacts | _TBD_ | |

---

## Open Research Questions

- [ ] What constitutes an adequate AI Bill of Materials (AI-BOM)?
- [ ] How do you verify model integrity when you can't reproduce the training run?
- [ ] What's the state of model signing standards (equivalent of code signing for models)?
- [ ] How should organizations assess risk of closed-source API-accessed models?

---

## Related Standards & Cross-References

- [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
- [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
- [SBOM Overview: CISA](https://www.cisa.gov/sbom)
- [CycloneDX: Machine Learning BOM](https://cyclonedx.org/capabilities/mlbom/)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

