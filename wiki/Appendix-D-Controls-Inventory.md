# Appendix D: AI Security Controls Inventory — Research Notes

> **Source:** [`1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md)

## Overview

Appendix D provides a cross-cutting inventory of all 20 security control categories referenced across AISVS, with specific requirement IDs mapped to each control technique. This research page maps each control category to its primary and secondary chapters, identifies coverage gaps, and tracks implementation tooling.

---

## Control Category to Chapter Mapping

| # | Category | Primary Chapters | Secondary Chapters | Req Count |
|---|----------|-----------------|-------------------|:---------:|
| AD.1 | Authentication | C5, C10 | C4, C9 | 13 |
| AD.2 | Authorization & Access Control | C5, C9, C10 | — | 16 |
| AD.3 | Encryption at Rest | C4 | C1, C8, C13 | 9 |
| AD.4 | Encryption in Transit | C4, C10 | C9, C13 | 8 |
| AD.5 | Key & Secret Management | C4 | C9, C10, C11 | 9 |
| AD.6 | Cryptographic Integrity & Signing | C3, C6, C9, C10 | C1, C4, C7, C11, C13 | 14 |
| AD.7 | Input Validation & Sanitization | C2 | C9, C10 | 23 |
| AD.8 | Output Filtering & Safety | C7 | C5, C10 | 13 |
| AD.9 | Rate Limiting & Resource Budgets | C2, C9 | C4, C10, C11 | 12 |
| AD.10 | Sandboxing & Process Isolation | C4, C9 | C10 | 13 |
| AD.11 | Network Segmentation & Egress Control | C4, C10 | C3, C9 | 10 |
| AD.12 | Supply Chain & Artifact Integrity | C3, C6 | C4 | 15 |
| AD.13 | Deployment & Lifecycle Management | C3 | C6 | 14 |
| AD.14 | Privacy & Data Minimization | C12 | C1, C6 | 16 |
| AD.15 | Adversarial Testing & Model Hardening | C11 | C1, C2 | 16 |
| AD.16 | Logging & Audit | C13 | C3, C6, C7, C9, C11, C12 | 14 |
| AD.17 | Monitoring, Alerting & Incident Response | C13 | C4, C7, C9, C11 | 17 |
| AD.18 | Explainability & Transparency | C14 | C7 | 12 |
| AD.19 | Human Oversight & Approval Gates | C9, C14 | C6, C7, C10, C11, C13 | 12 |
| AD.20 | Hardware & Accelerator Security | C4 | — | 14 |

---

## Implementation Tooling by Category

| Category | Key Tools & Frameworks |
|----------|----------------------|
| AD.1 Authentication | Keycloak, Auth0, SPIFFE/SPIRE, FIDO2/WebAuthn |
| AD.2 Authorization | OPA, Cedar, Casbin, Kubernetes RBAC |
| AD.3 Encryption at Rest | AWS KMS, Azure Key Vault, HashiCorp Vault, LUKS |
| AD.4 Encryption in Transit | mTLS (cert-manager, Istio), TLS 1.3 |
| AD.5 Key & Secret Management | HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, SOPS |
| AD.6 Integrity & Signing | Sigstore/cosign, in-toto, Notary v2, GPG |
| AD.7 Input Validation | LLM Guard, Lakera Guard, Rebuff, Pydantic, Zod |
| AD.8 Output Filtering | Guardrails AI, NeMo Guardrails, Presidio, OpenAI Moderation API |
| AD.9 Rate Limiting | Kong, AWS API Gateway, custom token-bucket, LiteLLM proxy |
| AD.10 Sandboxing | gVisor, Kata Containers, Firecracker, E2B, WASM runtimes |
| AD.11 Network Segmentation | Cilium, Calico, AWS Security Groups, cloud VPC |
| AD.12 Supply Chain | ModelScan, Fickling, safetensors, Dependabot, Snyk, CycloneDX |
| AD.13 Deployment & Lifecycle | MLflow, Seldon Core, BentoML, ArgoCD, Kubernetes |
| AD.14 Privacy | Opacus, TensorFlow Privacy, Presidio, PySyft, Flower |
| AD.15 Adversarial Testing | ART (IBM), TextAttack, Garak, Counterfit, Deepchecks |
| AD.16 Logging & Audit | OpenTelemetry, Langfuse, LangSmith, Splunk, Elastic |
| AD.17 Monitoring & Alerting | Evidently AI, NannyML, Arize AI, WhyLabs, PagerDuty |
| AD.18 Explainability | SHAP, LIME, Captum, InterpretML, Alibi |
| AD.19 Human Oversight | Label Studio, custom approval workflows, Slack/webhook gates |
| AD.20 Hardware Security | NVIDIA MIG, AMD SEV, Intel TDX, TPM 2.0, Secure Boot |

---

## Coverage Gap Analysis

### Potential Missing Control Categories

- [ ] **Data Governance & Lineage** — While AD.14 covers privacy, broader data governance (lineage tracking, data quality monitoring, retention policies) spans C1, C8, and C12 but isn't a standalone category
- [ ] **Model Fairness & Bias Testing** — Referenced in C1 (1.4.6), C6 (6.5.4), C14 (14.5.3) but doesn't have its own AD category; currently folded into AD.15 and AD.18
- [ ] **Incident Forensics** — AD.17 covers incident response but forensic-specific controls (C13.5.2 AI forensic tools) could warrant their own category as the field matures
- [ ] **Multi-Agent Coordination Security** — C9.8 covers multi-agent isolation but agent coordination patterns (consensus, conflict resolution, swarm safety) are emerging concerns

### Controls Appearing in Multiple Categories

Some requirement IDs appear across multiple AD categories, which is expected for defense-in-depth:

| Requirement | Categories | Why |
|------------|------------|-----|
| 4.5.4 (TEE/confidential computing) | AD.3, AD.10 | Both encryption and isolation |
| 9.4.2 (execution chain signing) | AD.6, AD.16 | Both integrity and audit |
| 7.3.2 (PII redaction) | AD.8, AD.14 | Both output filtering and privacy |
| 11.5.4 (model watermarking) | AD.6, AD.15 | Both integrity and adversarial defense |

---

## Community Notes

_Discussion about control inventory completeness and organization._

---

[README](README.md)
