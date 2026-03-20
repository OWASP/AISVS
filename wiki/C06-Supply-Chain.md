# C06: Supply Chain Security for Models, Frameworks & Data

> **Source:** [`1.0/en/0x10-C06-Supply-Chain.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C06-Supply-Chain.md)
> **Requirements:** 33 | **Sections:** 7

## Control Objective

AI supply-chain attacks exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code. These controls provide end-to-end traceability, vulnerability management, and monitoring to protect the entire model lifecycle.

> **2025-2026 Highlights:** The AI BOM ecosystem (CycloneDX ML, SPDX AI) is gaining adoption alongside SLSA for ML pipelines. Malicious model discoveries on public registries continued to grow, reinforcing the need for model scanning and SafeTensors format enforcement as baseline controls.

---

## Section Pages

| Section | Title | Reqs | IDs | Page |
|---------|-------|:----:|-----|------|
| C6.1 | Pretrained Model Vetting & Origin Integrity | 5 | 6.1.1–6.1.5 | [C06-01-Pretrained-Model-Vetting](C06-01-Pretrained-Model-Vetting.md) |
| C6.2 | Framework & Library Scanning | 5 | 6.2.1–6.2.5 | [C06-02-Framework-Library-Scanning](C06-02-Framework-Library-Scanning.md) |
| C6.3 | Dependency Pinning & Verification | 5 | 6.3.1–6.3.5 | [C06-03-Dependency-Pinning-Verification](C06-03-Dependency-Pinning-Verification.md) |
| C6.4 | Trusted Source Enforcement | 5 | 6.4.1–6.4.5 | [C06-04-Trusted-Source-Enforcement](C06-04-Trusted-Source-Enforcement.md) |
| C6.5 | Third-Party Dataset Risk Assessment | 5 | 6.5.1–6.5.5 | [C06-05-Third-Party-Dataset-Risk](C06-05-Third-Party-Dataset-Risk.md) |
| C6.6 | Supply Chain Attack Monitoring | 3 | 6.6.1–6.6.3 | [C06-06-Supply-Chain-Attack-Monitoring](C06-06-Supply-Chain-Attack-Monitoring.md) |
| C6.7 | AI BOM for Model Artifacts | 5 | 6.7.1–6.7.5 | [C06-07-AI-BOM-Model-Artifacts](C06-07-AI-BOM-Model-Artifacts.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Backdoored pretrained models on Hugging Face or Model Zoo (JFrog 2024: 100+ malicious models discovered)
- Pickle deserialization attacks in model weight files (arbitrary code execution on `torch.load()`)
- Typosquatting attacks on PyPI/npm packages used in ML pipelines
- Dependency confusion attacks targeting internal ML package names (Birsan 2021)
- Compromised training datasets from third-party sources (data poisoning)
- Malicious model adapters/LoRA weights with embedded backdoors
- CI/CD pipeline compromise targeting model training infrastructure

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Model scanning:** ModelScan (Protect AI), Fickling (Trail of Bits), SafeTensors format enforcement
- **SBOM/MLBOM:** CycloneDX ML extension, SPDX AI profile, Dependency-Track
- **Dependency scanning:** Dependabot, Snyk, OSV Scanner, Grype, Trivy, Socket.dev
- **Registry security:** Hugging Face model cards, Sigstore/cosign, TUF, JFrog Artifactory
- **Data validation:** Great Expectations, Cleanlab, Presidio (PII detection)
- **Fairness/bias:** Fairlearn, AI Fairness 360, What-If Tool
- **Runtime monitoring:** Falco, Sysdig, eBPF-based sensors
- **Provenance:** SLSA framework, in-toto, Rekor transparency log

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C6.1 Pretrained Model Vetting | Medium | ModelScan and Fickling cover pickle attacks well; Trojan detection and model signing are immature |
| C6.2 Framework & Library Scanning | High | Standard dependency scanners work well; gaps in CUDA/native library coverage |
| C6.3 Dependency Pinning & Verification | High | pip/conda/Docker tooling is mature; SLSA for ML pipelines is emerging |
| C6.4 Trusted Source Enforcement | Medium | Container signing is mature; model weight signing ecosystem is nascent |
| C6.5 Third-Party Dataset Risk | Low-Medium | Data validation tools exist but poisoning detection is research-stage |
| C6.6 Supply Chain Attack Monitoring | Low | AI-specific threat intelligence is very limited; no ML-focused SIEM rules |
| C6.7 AI BOM for Model Artifacts | Low-Medium | CycloneDX ML and SPDX AI exist but adoption is early |

---

## Related Standards & Cross-References

- [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
- [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
- [SBOM Overview: CISA](https://www.cisa.gov/sbom)
- [CycloneDX: Machine Learning BOM](https://cyclonedx.org/capabilities/mlbom/)
- [SLSA Framework](https://slsa.dev/)
- [NIST AI RMF](https://airc.nist.gov/AI_RMF_Interactivity)
- [EU AI Act — Transparency Requirements](https://artificialintelligenceact.eu/)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C1 Training Data | Dataset provenance and poisoning | C6.5 covers supply-chain risk of *external* datasets; C1 covers data quality broadly |
| C3 Model Lifecycle | Model versioning and deployment | C6.7 AI BOM complements C3 model registry requirements |
| C4 Infrastructure | Container and runtime security | C6.2/C6.3 pinning and scanning overlap with C4 infrastructure hardening |
| C13 Monitoring & Logging | Anomaly detection and incident response | C6.6 monitoring requirements feed into C13 centralized logging |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
