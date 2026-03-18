# Appendix D: AI Security Controls Inventory

> **Source:** [`1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md)

## Overview

Concise inventory of all security controls and techniques referenced throughout AISVS, organized by category. This serves as a cross-cutting reference for implementers.

## Control Categories

| # | Category | Description |
|---|----------|-------------|
| AD.1 | Authentication | Identity verification for AI components |
| AD.2 | Authorization & Access Control | Permission enforcement |
| AD.3 | Encryption at Rest | Data protection for stored models and data |
| AD.4 | Encryption in Transit | Transport-level security |
| AD.5 | Key & Secret Management | Cryptographic material lifecycle |
| AD.6 | Cryptographic Integrity & Signing | Tamper detection |
| AD.7 | Input Validation & Sanitization | Prompt and data validation |
| AD.8 | Output Filtering & Safety | Response safety controls |
| AD.9 | Rate Limiting & Resource Budgets | Abuse prevention |
| AD.10 | Sandboxing & Process Isolation | Execution boundaries |
| AD.11 | Network Segmentation & Egress Control | Network security |
| AD.12 | Supply Chain & Artifact Integrity | Provenance verification |
| AD.13 | Deployment & Lifecycle Management | Change control |
| AD.14 | Privacy & Data Minimization | Data protection |
| AD.15 | Adversarial Testing & Model Hardening | Robustness testing |
| AD.16 | Logging & Audit | Observability |
| AD.17 | Monitoring, Alerting & Incident Response | Detection and response |
| AD.18 | Explainability & Transparency | Interpretability |
| AD.19 | Human Oversight & Approval Gates | Human control |
| AD.20 | Hardware & Accelerator Security | Physical/hardware security |

## Research Notes

### Coverage Gaps

_Control areas that may be missing from the inventory._

- [ ] _Identify gaps here_

### Cross-Reference to Chapters

_Track which chapters map to which control categories._

| Control Category | Primary Chapters | Secondary Chapters |
|-----------------|------------------|-------------------|
| AD.1 Authentication | C5 | C10 |
| AD.2 Authorization | C5 | C9, C10 |
| AD.7 Input Validation | C2 | C10 |
| AD.8 Output Filtering | C7 | C5 |
| _... continue mapping ..._ | | |

---

## Community Notes

_Discussion about control inventory completeness and organization._

---

