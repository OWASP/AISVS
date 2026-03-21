# Appendix D: AI Security Controls Inventory — Research Notes

> **Source:** [`1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md)

## Overview

Appendix D provides a cross-cutting inventory of all 20 security control categories referenced across AISVS, with specific requirement IDs mapped to each control technique. This research page maps each control category to its primary and secondary chapters, identifies coverage gaps, tracks implementation tooling, assesses per-category maturity, and cross-references external frameworks.

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

## Implementation Maturity by Category

Industry adoption data drawn from multiple sources including the Gravitee State of AI Agent Security 2026 report, CSA AI Security and Governance survey (December 2025), Microsoft Cyber Pulse AI Security Report, and Lakera GenAI Security Readiness Report 2025.

| # | Category | Maturity | Key Tools & Frameworks | Adoption Evidence |
|---|----------|:--------:|----------------------|-------------------|
| AD.1 | Authentication | **Low** | Keycloak, Auth0, SPIFFE/SPIRE, FIDO2/WebAuthn, OAuth 2.1 (added to MCP spec June 2025) | Only 21.9% of orgs treat agents as identity-bearing entities; 45.6% still use shared API keys for agent-to-agent auth. No settled identity model for AI agents. |
| AD.2 | Authorization | **Low** | OPA, Cedar, Casbin, Kubernetes RBAC | 27.2% use custom hardcoded auth logic; only 21% have complete visibility into agent permissions. MCP gateways with policy enforcement are brand-new (2025–2026). |
| AD.3 | Encryption at Rest | **High** | AWS KMS, Azure Key Vault, HashiCorp Vault, LUKS | Standard enterprise practice; cloud providers encrypt model storage by default. Gap: data-in-use encryption during inference remains uncommon. |
| AD.4 | Encryption in Transit | **High** | mTLS (cert-manager, Istio), TLS 1.3 | Well-established. Gap: unencrypted GPU interconnects (NVLink, PCIe) in multi-tenant clusters. |
| AD.5 | Key & Secret Management | **Medium** | HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, SOPS | Existing KMS applies but API key sprawl is severe (~1,200 unofficial AI apps per enterprise create unmanaged key surfaces). No AI-specific lifecycle management standards. |
| AD.6 | Integrity & Signing | **Low** | Sigstore/cosign, in-toto, Notary v2, OpenSSF Model Signing (OMS, June 2025) | OMS specification published June 2025 but not broadly adopted. 48% of security professionals say orgs are behind on SBOM; ML-BOM adoption is far lower. Most model registries lack signing support. |
| AD.7 | Input Validation | **Medium** | LLM Guard (Protect AI), Lakera Guard, NeMo Guardrails, AWS Bedrock prompt attack filter, Pydantic, Zod | 34.7% have deployed dedicated prompt injection defenses; 89% of models remain vulnerable to prompt attacks. $1.42B market growing at 27.8% CAGR. |
| AD.8 | Output Filtering | **Medium** | Guardrails AI, NeMo Guardrails, Presidio, OpenAI Moderation API, AWS Bedrock content filters | 41% have runtime guardrails. Mostly focused on content safety rather than security-specific output filtering (e.g., data exfiltration via output). |
| AD.9 | Rate Limiting | **High** | Kong AI Gateway (token-aware), LiteLLM Proxy, Envoy AI Gateway, AWS API Gateway, Zuplo | Standard API gateway capability. All major LLM providers enforce rate limits natively. Gap: per-agent token/cost budgets for agentic loops are newer and less standardized. |
| AD.10 | Sandboxing | **Medium** | gVisor, Kata Containers, Firecracker, E2B, WASM runtimes | Container isolation well-established; agent tool execution sandboxing is less mature. MCP servers typically run with broad host access. No standard for isolating agentic tool calls. |
| AD.11 | Network Segmentation | **High** | Cilium, Calico, AWS Security Groups, cloud VPC | Standard network controls apply. Gap: 86% of orgs report no visibility into AI data flows, suggesting AI-specific segmentation (model serving vs. training vs. RAG) is not standard. |
| AD.12 | Supply Chain | **Low** | ModelScan, Guardian (35+ formats), Fickling, safetensors, CycloneDX, Black Duck AI (Oct 2025), Palisade (Sigstore) | 91% use unvetted pre-trained models; 67% of models lack security scanning. ENISA 2025 report documents poisoned models and trojanized packages. AI BOM concept is nascent. |
| AD.13 | Deployment & Lifecycle | **Medium** | MLflow, Seldon Core, BentoML, ArgoCD, Kubernetes, Weights & Biases | MLOps tooling covers versioning and deployment, but security is not integrated by default. Model retirement/deprecation policies are rare. Shadow AI (~1,200 unofficial apps/enterprise) indicates lifecycle management failure. |
| AD.14 | Privacy | **Low** | Opacus, TensorFlow Privacy, Presidio, PySyft, Flower | Differential privacy at Level 3 maturity (12% of orgs). Machine unlearning is still academic — no production-grade solutions for LLMs. DP implementation degrades accuracy; privacy-accuracy tradeoff remains unsolved. |
| AD.15 | Adversarial Testing | **Low–Med** | ART (IBM), TextAttack, Garak, Counterfit, Deepchecks, Lakera Red | 12% of orgs perform adversarial robustness evaluation. Fine-tuning attacks bypassed Claude Haiku in 72% of cases, GPT-4o in 57%. 45% of models susceptible to extraction. No standardized testing methodology. |
| AD.16 | Logging & Audit | **Medium** | OpenTelemetry, Langfuse, LangSmith, Splunk, Elastic, Datadog LLM Obs | 47.1% of agents are monitored, meaning >50% operate without security oversight or logging. No standard log schema for AI operations. Prompt/response logging raises privacy concerns. |
| AD.17 | Monitoring & Alerting | **Medium** | Evidently AI, NannyML, Arize AI, WhyLabs, PagerDuty, Galileo AI | 38% monitor AI traffic end-to-end. Most monitoring is performance-focused, not security-focused. Real-time security-specific monitoring (prompt injection detection, exfiltration) is less mature. |
| AD.18 | Explainability | **Medium** | SHAP, LIME, Captum, InterpretML, Alibi, IBM AI FactSheets | ~$9.2B market growing at 18% CAGR; 65% view explainability as top barrier to AI scaling. Tools are mainly for tabular/classical ML — LLM explainability is fundamentally harder. Primarily compliance-driven (EU AI Act). |
| AD.19 | Human Oversight | **Medium** | Label Studio, custom approval workflows, Slack/webhook gates | 82% of executives feel confident policies protect against unauthorized agent actions, but actual governance enforcement is at 7%. 25.5% of deployed agents can create and task other agents autonomously. Massive perception-reality gap. |
| AD.20 | Hardware Security | **Low** | NVIDIA MIG, AMD SEV, Intel TDX, TPM 2.0, NVIDIA Confidential Computing (Hopper/Blackwell) | GPU TEE support is vendor-locked (NVIDIA). Performance overhead significant. Enterprise adoption limited to defense/healthcare/finance. Data-in-use protection during inference is not mainstream. |

---

## External Framework Cross-Reference

How the 20 AD categories map to major external AI security frameworks. As of March 2026, the most actionable frameworks for control-level mapping are MITRE SAFE-AI (100 NIST 800-53 controls), CSA AICM (243 control objectives), and OWASP LLM Top 10 (2025).

| Category | MITRE ATLAS Technique/Mitigation | NIST IR 8596 (Cyber AI Profile) | CSA AICM Domain | OWASP LLM Top 10 (2025) | EU AI Act |
|----------|--------------------------------|-------------------------------|-----------------|------------------------|-----------|
| AD.1 Authentication | Mitigations for AML.T0061 (AI Agent Tools) | PR.AA (Identity Management) | Identity & Access Management | — | — |
| AD.2 Authorization | Mitigations for AML.T0062 (Exfil via Agent Tool) | PR.AA | Identity & Access Management | LLM08 (Excessive Agency) | — |
| AD.3–4 Encryption | — | PR.DS (Data Security) | Data Security & Privacy | — | — |
| AD.5 Key Management | — | PR.DS | Data Security & Privacy | — | — |
| AD.6 Integrity & Signing | Mitigations for AML.T0020 (Poison Training Data) | PR.DS, ID.AM | Supply Chain Mgmt | LLM05 (Supply Chain) | Annex IV §6 |
| AD.7 Input Validation | AML.T0051 (Prompt Injection) | PR.DS | Model Security | LLM01 (Prompt Injection) | Art. 15 §5 |
| AD.8 Output Filtering | — | PR.DS | Model Security | LLM02 (Sensitive Info Disclosure) | Art. 15 |
| AD.9 Rate Limiting | AML.T0029 (Denial of ML Service), AML.T0034 (Cost Harvesting) | PR.IR | Model Security | LLM10 (Unbounded Consumption) | Art. 15 §4 |
| AD.10 Sandboxing | AML.T0058 (AI Agent Context Poisoning) | PR.PS | — | LLM08 (Excessive Agency) | — |
| AD.11 Network Seg. | — | PR.IR | — | — | — |
| AD.12 Supply Chain | AML.T0020, AML.T0059 (Activation Triggers) | ID.SC (Supply Chain) | Supply Chain Mgmt | LLM05 (Supply Chain) | Annex IV §2 |
| AD.13 Deployment | AML.T0020 | PR.PS (Platform Security) | — | — | Annex IV §6, §9 |
| AD.14 Privacy | AML.T0046 (Chaff Data) | PR.DS | Data Security & Privacy | LLM06 (Excessive Agency) | Art. 10, Annex IV §2 |
| AD.15 Adversarial Testing | AML.T0020, AML.T0051, AML.T0059 | DE.CM, DE.AE | Model Security | LLM01, LLM09 (Misinformation) | Art. 15 §5, Annex IV §5 |
| AD.16 Logging | — | DE.CM (Continuous Monitoring) | — | — | Art. 12 |
| AD.17 Monitoring | AML.T0029 | DE.CM, DE.AE, RS.RP | — | LLM10 (Unbounded Consumption) | Art. 15 §4, Annex IV §9 |
| AD.18 Explainability | — | GV.RM (Risk Management) | Transparency & Accountability | LLM09 (Misinformation) | Art. 13, 14, Annex IV §3 |
| AD.19 Human Oversight | — | GV.RM | Transparency & Accountability | LLM08 (Excessive Agency) | Art. 14 |
| AD.20 Hardware | — | PR.PS | — | — | — |

**Key external frameworks referenced:**
- **NIST IR 8596** (Cyber AI Profile, draft December 2025) — maps AI concerns to all 106 CSF 2.0 subcategories with priority ratings. Identified gap: limited coverage of agentic AI patterns.
- **MITRE ATLAS** (October 2025 update) — 15 tactics, 66 techniques, 46 sub-techniques, 26 mitigations. Added 14 agentic AI techniques via Zenity Labs collaboration.
- **MITRE SAFE-AI** — maps ATLAS threats × 4 system elements (Environment, AI Platform, AI Model, AI Data) → 100 identified NIST SP 800-53 controls. The most granular threat-to-control mapping available.
- **CSA AI Controls Matrix** (AICM) — 243 control objectives across 18 security domains with ISO 42001, EU AI Act, and NIST AI RMF mappings completed August 2025.
- **OWASP AI Maturity Assessment** (AIMA, v1.0 August 2025) — integrates with OWASP SAMM and ISO/IEC AI standards for organizational security maturity assessment.

---

## AI Security Platform Coverage

Which commercial and open-source platforms address which control categories. Reflects the major consolidation wave of 2024–2025: Robust Intelligence → Cisco (Oct 2024), Protect AI → Palo Alto (Apr 2025), Lakera → Check Point (Sep 2025), Prompt Security → SentinelOne (Aug 2025, ~$250M).

| Platform | AD.1 | AD.2 | AD.7 | AD.8 | AD.9 | AD.12 | AD.15 | AD.16 | AD.17 | Notes |
|----------|:----:|:----:|:----:|:----:|:----:|:-----:|:-----:|:-----:|:-----:|-------|
| Cisco AI Defense | | | X | X | | X | X | X | X | MCP Catalog for MCP server risk (Feb 2026); AI BOM for asset governance; algorithmic red teaming |
| Protect AI (Palo Alto) | | | X | X | | X | X | X | X | LLM Guard (OSS, 15 input + 20 output scanners); Guardian (35+ model format scanning); ModelScan (OSS) |
| Lakera (Check Point) | | | X | X | | | X | | X | Lakera Guard (runtime, single-line integration); Lakera Red (automated red teaming) |
| Prompt Security (SentinelOne) | | X | X | X | | | | | X | Sub-200ms latency; semantic DLP; shadow AI detection via Chrome extension; 250+ model coverage |
| CalypsoAI | | X | X | X | | | | X | | Agentic cognitive-layer intervention; CrewAI + MCP support |
| HiddenLayer | | | | | | X | X | | X | Model integrity monitoring; adversarial attack prevention |
| Kong AI Gateway | X | | X | X | X | | | X | | Token-aware rate limiting; AI Semantic Prompt Guard; MCP server security |
| AWS Bedrock Guardrails | | | X | X | | | | | | 6 guardrail types; automated reasoning with formal logic; 88% harmful content blocking |
| Azure AI Content Safety | | | X | X | | | | | | Prompt Shields; Groundedness Detection (preview); detection-oriented |
| Datadog LLM Obs | | | X | X | | | | X | | Auto-instrumentation; prompt injection scanning; PII leak detection; $8/10K requests |
| Langfuse (OSS) | | | | | | | | X | | 19K+ GitHub stars; multi-turn tracing; prompt versioning |
| Arize Phoenix (OSS) | | | | | | | | X | X | OpenTelemetry-native; drift detection; 7.8K+ GitHub stars |

---

## Coverage Gap Analysis

### Potential Missing Control Categories

- [ ] **Data Governance & Lineage** — While AD.14 covers privacy, broader data governance (lineage tracking, data quality monitoring, retention policies) spans C1, C8, and C12 but isn't a standalone category
- [ ] **Model Fairness & Bias Testing** — Referenced in C1 (1.4.6), C6 (6.5.4), C14 (14.5.3) but doesn't have its own AD category; currently folded into AD.15 and AD.18
- [ ] **Incident Forensics** — AD.17 covers incident response but forensic-specific controls (C13.5.2 AI forensic tools) could warrant their own category as the field matures
- [ ] **Multi-Agent Coordination Security** — C9.8 covers multi-agent isolation but agent coordination patterns (consensus, conflict resolution, swarm safety) are emerging concerns. As of March 2026, 25.5% of deployed agents can create and task other agents autonomously
- [ ] **MCP-Specific Controls** — C10 has 34 requirements spanning authentication, transport, validation, and boundary enforcement for MCP. As MCP adoption grows (60% of LLMjacking attack traffic targeted MCP endpoints in Operation Bizarre Bazaar), a dedicated AD category for MCP security may be warranted

### Controls Appearing in Multiple Categories

Some requirement IDs appear across multiple AD categories, which is expected for defense-in-depth:

| Requirement | Categories | Why |
|------------|------------|-----|
| 4.5.4 (TEE/confidential computing) | AD.3, AD.10 | Both encryption and isolation |
| 9.4.2 (execution chain signing) | AD.6, AD.16 | Both integrity and audit |
| 7.3.2 (PII redaction) | AD.8, AD.14 | Both output filtering and privacy |
| 11.5.4 (model watermarking) | AD.6, AD.15 | Both integrity and adversarial defense |

---

## Industry Adoption Snapshot (March 2026)

Overall adoption remains low — 94% of enterprises use AI in production, yet only 23% have mature security programs.

| Metric | Percentage | Source |
|--------|:----------:|--------|
| Enterprises using AI in production | 94% | CyberSecFeed AI Security Maturity Model |
| Orgs implementing any GenAI security controls | 47% | Microsoft Cyber Pulse AI Security Report |
| Orgs with comprehensive AI security governance | 25% | CSA AI Security & Governance Survey (Dec 2025) |
| Orgs with full security approval for AI agents | 14.4% | Gravitee State of AI Agent Security 2026 |
| Orgs with real-time governance enforcement | 7% | Industry aggregate |
| AI agents actively monitored/secured | 47.1% | Gravitee |
| Models lacking security scanning | 67% | CyberSecFeed |
| Models vulnerable to prompt attacks | 89% | CyberSecFeed |
| Orgs using unvetted pre-trained models | 91% | CyberSecFeed |
| Orgs reporting AI security incidents in past year | 88% | Gravitee |
| Orgs with no visibility into AI data flows | 86% | HelpNetSecurity (March 2026) |

**Maturity distribution** (CyberSecFeed 5-level model): Level 0 (Unaware) 34%, Level 1 (Initial) 28%, Level 2 (Developing) 23%, Level 3 (Managed) 12%, Level 4 (Optimized) 3%.

---

## Community Notes

_Discussion about control inventory completeness and organization._

---

## References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [NIST IR 8596: Cybersecurity Framework Profile for AI (Draft, December 2025)](https://csrc.nist.gov/pubs/ir/8596/iprd)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [MITRE ATLAS — Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
* [MITRE SAFE-AI Framework (Full Report)](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf)
* [CSA AI Controls Matrix (AICM)](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix)
* [CSA State of AI Security and Governance (December 2025)](https://cloudsecurityalliance.org/artifacts/the-state-of-ai-security-and-governance)
* [OWASP Top 10 for Large Language Model Applications (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP AI Maturity Assessment (AIMA, v1.0 August 2025)](https://owasp.org/www-project-ai-maturity-assessment/)
* [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)
* [EU AI Act — Article 15 (Robustness & Cybersecurity)](https://artificialintelligenceact.eu/article/15/)
* [EU AI Act — Annex IV (Technical Documentation)](https://artificialintelligenceact.eu/annex/4/)
* [OpenSSF Model Signing (OMS) Specification (June 2025)](https://openssf.org/blog/2025/06/25/an-introduction-to-the-openssf-model-signing-oms-specification/)
* [Gravitee State of AI Agent Security 2026 Report](https://www.gravitee.io/blog/state-of-ai-agent-security-2026-report-when-adoption-outpaces-control)
* [Microsoft Cyber Pulse: AI Security Report](https://www.microsoft.com/en-us/security/security-insider/emerging-trends/cyber-pulse-ai-security-report)
* [Lakera GenAI Security Readiness Report 2025](https://www.lakera.ai/genai-security-report-2025)

---

[README](README.md)
