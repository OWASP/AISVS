# Appendix D: AI Security Controls Inventory — Research Notes

> **Source:** [`1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md)

## Overview

Appendix D currently provides a cross-cutting inventory of 19 security control categories referenced across AISVS, with specific requirement IDs mapped to each control technique. This research page maps each control category to its primary and secondary coverage areas, identifies gaps where the source inventory may need future expansion, tracks implementation tooling, assesses per-category maturity, and cross-references external frameworks.

---

## Control Category to Chapter Mapping

| # | Category | Primary Coverage | Secondary Coverage | Mapped Controls |
|---|----------|-----------------|-------------------|:---------------:|
| AD.1 | Authentication | C10 | C5, C9 | 9 |
| AD.2 | Authorization & Access Control | C5, C9 | C10 | 19 |
| AD.3 | Encryption at Rest | C1 | C13 | 3 |
| AD.4 | Encryption in Transit | C10 | C4, C13 | 5 |
| AD.5 | Key & Secret Management | C9, C10 | — | 2 |
| AD.6 | Cryptographic Integrity & Signing | C3, C6, C9, C10 | C1, C11, ASVS/SLSA | 14 |
| AD.7 | Input Validation & Sanitization | C2 | C9, C10 | 27 |
| AD.8 | Output Filtering & Safety | C7 | C5, C10, C11 | 14 |
| AD.9 | Rate Limiting & Resource Budgets | C9 | C11, C13, ASVS V2.4 | 10 |
| AD.10 | Sandboxing & Process Isolation | C4 | C9, C10 | 9 |
| AD.11 | Network Segmentation & Egress Control | C4, C10 | C3, C9 | 10 |
| AD.12 | Supply Chain & Artifact Integrity | C6 | C3, C4, ASVS/SLSA/SCVS | 20 |
| AD.13 | Deployment & Lifecycle Management | C3 | C6 | 15 |
| AD.14 | Privacy & Data Minimization | C12 | C1, C6 | 20 |
| AD.15 | Adversarial Testing & Model Hardening | C11 | C1 | 29 |
| AD.16 | Logging & Audit | C13 | C3, C7, C9, C11, C14, ASVS | 16 |
| AD.17 | Monitoring, Alerting & Incident Response | C13 | C7, C9, C11 | 18 |
| AD.18 | Explainability & Transparency | C7 | C11 | 5 |
| AD.19 | Human Oversight & Approval Gates | C9, C14 | C6, C11 | 14 |

---

## Implementation Maturity by Category

Industry adoption data drawn from multiple sources including the Gravitee State of AI Agent Security 2026 report, CSA AI Security and Governance survey (December 2025), Microsoft Cyber Pulse AI Security Report, Lakera GenAI Security Readiness Report 2025, and the Zscaler 2026 AI Security Report (which observed a 91% year-over-year surge in AI/ML traffic across more than 3,400 enterprise applications).

| # | Category | Maturity | Key Tools & Frameworks | Adoption Evidence |
|---|----------|:--------:|----------------------|-------------------|
| AD.1 | Authentication | **Low** | Keycloak, Auth0, SPIFFE/SPIRE, FIDO2/WebAuthn, OAuth 2.1 (added to MCP spec June 2025), agent identity registries | Only 21.9% of orgs treat agents as identity-bearing entities; 45.6% still use shared API keys for agent-to-agent auth. The May 2026 control trend is endpoint and gateway identity enforcement for agents rather than browser-only SSO. |
| AD.2 | Authorization | **Low** | OPA, Cedar, Casbin, Kubernetes RBAC, Kong Agent Gateway, Salt Agentic Security Platform, Operant Endpoint Protector | 27.2% use custom hardcoded auth logic; only 21% have complete visibility into agent permissions. MCP and A2A gateways now expose scope-filtering and runtime RBAC, but policy coverage is still uneven across local agents, IDE plugins, and remote MCP servers. |
| AD.3 | Encryption at Rest | **High** | AWS KMS, Azure Key Vault, HashiCorp Vault, LUKS | Standard enterprise practice; cloud providers encrypt model storage by default. Gap: data-in-use encryption during inference remains uncommon. |
| AD.4 | Encryption in Transit | **High** | mTLS (cert-manager, Istio), TLS 1.3 | Well-established. Gap: unencrypted GPU interconnects (NVLink, PCIe) in multi-tenant clusters. |
| AD.5 | Key & Secret Management | **Medium** | HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, SOPS | Existing KMS applies but API key sprawl is severe (~1,200 unofficial AI apps per enterprise create unmanaged key surfaces). No AI-specific lifecycle management standards. |
| AD.6 | Integrity & Signing | **Low–Med** | Sigstore/cosign, in-toto, Notary v2, OpenSSF Model Signing (OMS, June 2025), sigstore/model-transparency | OMS specification published June 2025; as of early 2026 NVIDIA's NGC catalog, Google's Kaggle, and Hugging Face have begun rolling out OMS signing flows. 48% of security professionals still say orgs are behind on SBOM; ML-BOM adoption is far lower. Many private model registries still lack signing support. |
| AD.7 | Input Validation | **Medium** | LLM Guard (Protect AI), Lakera Guard, NeMo Guardrails, AWS Bedrock prompt attack filter, Pydantic, Zod, MCPTox benchmark | 34.7% have deployed dedicated prompt injection defenses; 89% of models remain vulnerable to prompt attacks. MCPTox (AAAI 2026) found tool metadata poisoning remained effective across realistic MCP tool catalogs, so tool descriptions and manifests should be treated as untrusted input. |
| AD.8 | Output Filtering | **Medium** | Guardrails AI, NeMo Guardrails, Presidio, OpenAI Moderation API, AWS Bedrock content filters | 41% have runtime guardrails. Mostly focused on content safety rather than security-specific output filtering (e.g., data exfiltration via output). |
| AD.9 | Rate Limiting | **High** | Kong AI Gateway 3.14 / Kong Agent Gateway (April 2026: LLM + MCP + A2A unified governance, token/cost quotas, full audit logging of A2A conversations), LiteLLM Proxy, Envoy AI Gateway, AWS API Gateway, Zuplo | Standard API gateway capability. All major LLM providers enforce rate limits natively. Gap: per-agent token/cost budgets for agentic loops are newer but converging — Kong's 3.14 release (April 14, 2026) is the first unified gateway spanning LLM, MCP, and agent-to-agent traffic from a single control plane. |
| AD.10 | Sandboxing | **Medium** | gVisor, Kata Containers, Firecracker, E2B, WASM runtimes, MCP STDIO allow-lists | Container isolation is well-established; agent tool execution sandboxing is less mature. OX Security's April 2026 MCP STDIO advisory showed how user-controlled server configuration can become command execution across downstream platforms, making allow-listed launchers, sandboxed tool hosts, and configuration review first-order controls. |
| AD.11 | Network Segmentation | **High** | Cilium, Calico, AWS Security Groups, cloud VPC | Standard network controls apply. Gap: 86% of orgs report no visibility into AI data flows, suggesting AI-specific segmentation (model serving vs. training vs. RAG) is not standard. |
| AD.12 | Supply Chain | **Low** | ModelScan, Guardian (35+ formats), Fickling, safetensors, CycloneDX, Black Duck AI (Oct 2025), Palisade (Sigstore), sigstore/model-transparency, MCP registry review | 91% use unvetted pre-trained models; 67% of models lack security scanning. ENISA 2025 report documents poisoned models and trojanized packages. The LiteLLM 1.82.7/1.82.8 PyPI compromise on March 24, 2026 and the April 2026 MCP STDIO/RCE disclosure both reinforce the same pattern: agent dependencies need pinned versions, source provenance, signed artifacts, and explicit review of tool launch paths. |
| AD.13 | Deployment & Lifecycle | **Medium** | MLflow, Seldon Core, BentoML, ArgoCD, Kubernetes, Weights & Biases | MLOps tooling covers versioning and deployment, but security is not integrated by default. Model retirement/deprecation policies are rare. Shadow AI (~1,200 unofficial apps/enterprise) indicates lifecycle management failure. |
| AD.14 | Privacy | **Low** | Opacus, TensorFlow Privacy, Presidio, PySyft, Flower | Differential privacy at Level 3 maturity (12% of orgs). Machine unlearning is still academic — no production-grade solutions for LLMs. DP implementation degrades accuracy; privacy-accuracy tradeoff remains unsolved. |
| AD.15 | Adversarial Testing | **Low–Med** | ART (IBM), TextAttack, Garak, Counterfit, Deepchecks, Lakera Red | 12% of orgs perform adversarial robustness evaluation. Fine-tuning attacks bypassed Claude Haiku in 72% of cases, GPT-4o in 57%. 45% of models susceptible to extraction. No standardized testing methodology. |
| AD.16 | Logging & Audit | **Medium** | OpenTelemetry, Langfuse, LangSmith, Splunk, Elastic, Datadog LLM Obs | 47.1% of agents are monitored, meaning >50% operate without security oversight or logging. No standard log schema for AI operations. Prompt/response logging raises privacy concerns. |
| AD.17 | Monitoring & Alerting | **Medium** | Evidently AI, NannyML, Arize AI, WhyLabs, PagerDuty, Galileo AI, CrowdStrike AIDR, Capsule Security, Operant Endpoint Protector, Salt AG-DR, Zscaler AI Runtime Guardrails | 38% monitor AI traffic end-to-end. The "runtime gap" — the window between prompt receipt and action execution — is now the primary focus of the newest entrants. By May 2026, runtime monitoring has split into endpoint-local agent loop tracing, gateway inspection for LLM/MCP/A2A traffic, and graph-based detection over APIs and tool calls. |
| AD.18 | Explainability | **Medium** | SHAP, LIME, Captum, InterpretML, Alibi, IBM AI FactSheets | ~$9.2B market growing at 18% CAGR; 65% view explainability as top barrier to AI scaling. Tools are mainly for tabular/classical ML — LLM explainability is fundamentally harder. Primarily compliance-driven (EU AI Act). |
| AD.19 | Human Oversight | **Medium** | Label Studio, custom approval workflows, Slack/webhook gates, policy-bound approval services | 82% of executives feel confident policies protect against unauthorized agent actions, but actual governance enforcement is at 7%. The current source inventory makes approval gates verifiable as a chain: high-risk action policy, runtime gate, parameter binding, fail-closed expiry, kill-switch paths, and independent audit trails. |

---

## External Framework Cross-Reference

How the 19 current AD categories map to major external AI security frameworks. As of May 2026, the most actionable frameworks for control-level mapping are MITRE SAFE-AI (100 NIST 800-53 controls), CSA AICM (243 control objectives), OWASP LLM Top 10 (2025), the OWASP Agentic AI Top 10 (2026), NIST IR 8596, and NIST's SP 800-53 Control Overlays for Securing AI Systems project. MITRE's 2026 ATLAS updates continue shifting attention from model-centric attacks to execution-layer exposure, with threat modeling now accounting for autonomous workflow chaining, delegated authority persistence, tool metadata poisoning, and API-level orchestration risk.

| Category | MITRE ATLAS Technique/Mitigation | NIST IR 8596 (Cyber AI Profile) | CSA AICM Domain | OWASP LLM Top 10 (2025) | OWASP Agentic Top 10 (2026) | EU AI Act |
|----------|--------------------------------|-------------------------------|-----------------|------------------------|-----------------------------|-----------|
| AD.1 Authentication | Mitigations for AML.T0061 (AI Agent Tools), AML.T0098 (Agent Tool Credential Harvesting) | PR.AA (Identity Management) | Identity & Access Management | — | ASI03 (Identity & Privilege Abuse) | — |
| AD.2 Authorization | Mitigations for AML.T0062 (Exfil via Agent Tool), AML.T0096 (AI Service API) | PR.AA | Identity & Access Management | LLM08 (Excessive Agency) | ASI03, ASI04 (Excessive Agency) | — |
| AD.3–4 Encryption | — | PR.DS (Data Security) | Data Security & Privacy | — | — | — |
| AD.5 Key Management | — | PR.DS | Data Security & Privacy | — | — | — |
| AD.6 Integrity & Signing | Mitigations for AML.T0020 (Poison Training Data) | PR.DS, ID.AM | Supply Chain Mgmt | LLM05 (Supply Chain) | ASI05 (Improper Multi-Agent Orchestration) | Annex IV §6 |
| AD.7 Input Validation | AML.T0051 (Prompt Injection) | PR.DS | Model Security | LLM01 (Prompt Injection) | ASI01 (Agent Goal Hijacking) | Art. 15 §5 |
| AD.8 Output Filtering | — | PR.DS | Model Security | LLM02 (Sensitive Info Disclosure) | ASI06 (Memory & Context Manipulation) | Art. 15 |
| AD.9 Rate Limiting | AML.T0029 (Denial of ML Service), AML.T0034 (Cost Harvesting) | PR.IR | Model Security | LLM10 (Unbounded Consumption) | ASI08 (Resource & Service Abuse) | Art. 15 §4 |
| AD.10 Sandboxing | AML.T0058 (AI Agent Context Poisoning), AML.T0101 (Data Destruction via Agent Tool) | PR.PS | — | LLM08 (Excessive Agency) | ASI02 (Tool Misuse & Exploitation) | — |
| AD.11 Network Seg. | — | PR.IR | — | — | — | — |
| AD.12 Supply Chain | AML.T0020, AML.T0059 (Activation Triggers), AML.T0099 (Agent Tool Data Poisoning) | ID.SC (Supply Chain) | Supply Chain Mgmt | LLM05 (Supply Chain) | ASI09 (Supply Chain Vulnerabilities) | Annex IV §2 |
| AD.13 Deployment | AML.T0020 | PR.PS (Platform Security) | — | — | — | Annex IV §6, §9 |
| AD.14 Privacy | AML.T0046 (Chaff Data) | PR.DS | Data Security & Privacy | LLM06 (Excessive Agency) | ASI07 (Uncontrolled Chaining & Cascading) | Art. 10, Annex IV §2 |
| AD.15 Adversarial Testing | AML.T0020, AML.T0051, AML.T0059 | DE.CM, DE.AE | Model Security | LLM01, LLM09 (Misinformation) | ASI01, ASI10 (Rogue Agents) | Art. 15 §5, Annex IV §5 |
| AD.16 Logging | — | DE.CM (Continuous Monitoring) | — | — | — | Art. 12 |
| AD.17 Monitoring | AML.T0029 | DE.CM, DE.AE, RS.RP | — | LLM10 (Unbounded Consumption) | ASI10 (Rogue Agents) | Art. 15 §4, Annex IV §9 |
| AD.18 Explainability | — | GV.RM (Risk Management) | Transparency & Accountability | LLM09 (Misinformation) | — | Art. 13, 14, Annex IV §3 |
| AD.19 Human Oversight | — | GV.RM | Transparency & Accountability | LLM08 (Excessive Agency) | ASI04 (Excessive Agency) | Art. 14 |

**Key external frameworks referenced:**
- **NIST IR 8596** (Cyber AI Profile, preliminary draft December 2025; comment period closed January 30, 2026; Spring 2026 working sessions on April 28, May 5, and May 12) — maps AI cybersecurity concerns to CSF 2.0 outcomes across Secure, Defend, and Thwart focus areas. Identified gap: implementation guidance for agentic patterns is still emerging.
- **NIST SP 800-53 Control Overlays for Securing AI Systems (COSAiS)** — implementation-focused overlay work for generative assistants, predictive AI, single-agent systems, multi-agent systems, and AI developers. This is a useful bridge from Appendix D categories to audit-ready control baselines.
- **NIST AI RMF Profile for Trustworthy AI in Critical Infrastructure** — concept note released April 7, 2026. The planned profile will guide critical-infrastructure operators (energy, water, transport, healthcare) toward specific risk-management practices when deploying AI-enabled capabilities.
- **MITRE ATLAS** (2026 monthly cadence) — Secure AI's May 2026 recap notes 45+ new techniques/sub-techniques, 10+ mitigations, 20+ case studies, a Technique Maturity filter, and a Knowledge Graph. The OpenClaw rapid-response report remains the most useful example for Appendix D because it maps prompt injection, poisoned skills, exposed control interfaces, credential harvesting, exfiltration, and data destruction into a single agentic attack chain.
- **MITRE SAFE-AI** — maps ATLAS threats × 4 system elements (Environment, AI Platform, AI Model, AI Data) → 100 identified NIST SP 800-53 controls. The most granular threat-to-control mapping available.
- **CSA AI Controls Matrix** (AICM) — 243 control objectives across 18 security domains with ISO 42001, EU AI Act, and NIST AI RMF mappings completed August 2025.
- **OWASP AI Maturity Assessment** (AIMA, v1.0 August 2025) — integrates with OWASP SAMM and ISO/IEC AI standards for organizational security maturity assessment.
- **OWASP Agentic AI Top 10** (December 2025, peer-reviewed by 100+ researchers) — ASI01–ASI10 covering agent goal hijacking, tool misuse, identity abuse, excessive agency, improper orchestration, memory manipulation, uncontrolled chaining, resource abuse, supply chain, and rogue agents. A Dark Reading poll found 48% of cybersecurity professionals identify agentic AI as the number-one attack vector heading into 2026.
- **Microsoft Zero Trust for AI** (March 2026) — new AI pillar added to the Zero Trust Workshop, bringing the framework to 700 security controls across 7 pillars (Identity, Devices, Data, Network, Infrastructure, Security Operations, AI). Automated Zero Trust Assessment for AI expected summer 2026.
- **EU General-Purpose AI Code of Practice** — the Safety and Security chapter gives providers of systemic-risk GPAI models a practical path to demonstrate AI Act Article 55 compliance, complementing the Appendix D controls for model lifecycle, monitoring, incident response, and human oversight.
- **OWASP AI Exchange** — 300+ pages of open-source AI security guidance, feeding into EU AI Act (70 pages contributed), ISO/IEC 27090 (AI security), and ISO/IEC 27091 (AI privacy) standards through official liaison partnerships.

---

## AI Security Platform Coverage

Which commercial and open-source platforms address which control categories. Reflects the major consolidation wave of 2024–2025: Robust Intelligence → Cisco (Oct 2024), Protect AI → Palo Alto (Apr 2025), Lakera → Check Point (Sep 2025), Prompt Security → SentinelOne (Aug 2025, ~$250M), SPLX → Zscaler (2026). The broader cybersecurity M&A wave totaled $76–96B across 320–400 deals in 2025 (Return on Security / Momentum Cyber), with AI security as a distinct acquisition category. Early 2026 shows a second inflection point: established endpoint, API, and gateway vendors (CrowdStrike, Kong, Salt, Zscaler) are extending existing platforms to AI, while newer entrants (Capsule Security, Noma Security, Operant) target the runtime gap between prompt arrival and agent action.

| Platform | AD.1 | AD.2 | AD.7 | AD.8 | AD.9 | AD.12 | AD.15 | AD.16 | AD.17 | Notes |
|----------|:----:|:----:|:----:|:----:|:----:|:-----:|:-----:|:-----:|:-----:|-------|
| Cisco AI Defense | | | X | X | | X | X | X | X | MCP Catalog for MCP server risk (Feb 2026); AI BOM for asset governance; algorithmic red teaming |
| Protect AI (Palo Alto) | | | X | X | | X | X | X | X | LLM Guard (OSS, 15 input + 20 output scanners); Guardian (35+ model format scanning); ModelScan (OSS) |
| Lakera (Check Point) | | | X | X | | | X | | X | Lakera Guard (runtime, single-line integration); Lakera Red (automated red teaming) |
| Prompt Security (SentinelOne) | | X | X | X | | | | | X | Sub-200ms latency; semantic DLP; shadow AI detection via Chrome extension; 250+ model coverage |
| Straiker | | X | X | X | | | X | | X | Agentic-first; Ascend AI (adversarial agent testing) + Defend AI (runtime security); 8x growth in 6 months (Feb 2026); multi-six/seven-figure enterprise deals |
| CalypsoAI | | X | X | X | | | | X | | Agentic cognitive-layer intervention; CrewAI + MCP support |
| HiddenLayer | | | | | | X | X | | X | Model integrity monitoring; adversarial attack prevention |
| Qualys TotalAI | | | X | | | X | | X | X | Inventory-first approach; 650+ AI-specific detections; MCP server graph inventory (March 2026); shadow model discovery; AI CVE scanning |
| Kong AI Gateway 3.14 / Agent Gateway | X | X | X | X | X | | | X | X | April 14, 2026 release — unified governance of LLM + MCP + agent-to-agent (A2A) traffic from one control plane; token-aware rate limiting; full A2A audit logging; AI Semantic Prompt Guard; MCP server security |
| Operant Endpoint Protector | X | X | X | X | X | X | | X | X | May 4, 2026 launch — endpoint-native discovery, agent loop tracing, inline data exfiltration defense, runtime RBAC for MCP clients/servers/tools, and CodeInjectionGuard for package and shell execution attacks |
| Salt Agentic Security Platform | | X | X | X | | | | X | X | March 18, 2026 launch — Agentic Security Graph linking LLMs, MCP servers, and APIs; AG-SPM for posture management and AG-DR for real-time detection across agent-driven activity |
| AWS Bedrock Guardrails | | | X | X | | | | | | 6 guardrail types; automated reasoning with formal logic; 88% harmful content blocking |
| Azure AI Content Safety | | | X | X | | | | | | Prompt Shields; Groundedness Detection (preview); detection-oriented |
| Datadog LLM Obs | | | X | X | | | | X | | Auto-instrumentation; prompt injection scanning; PII leak detection; $8/10K requests |
| Langfuse (OSS) | | | | | | | | X | | 19K+ GitHub stars; multi-turn tracing; prompt versioning |
| F5 AI Guardrails + Red Team | | | X | X | | | X | X | X | CalypsoAI acquisition; model-agnostic runtime guardrails; autonomous red-team agent swarms with 10K+ attack techniques/month; Fortune 500 deployments (Jan 2026) |
| Varonis Atlas | | X | | | | | | X | X | AI Gateway for real-time prompt/response inspection; data-aware posture management; shadow AI discovery; full lifecycle (discovery → runtime → compliance); launched March 2026 |
| SandboxAQ AQtive Guard | | | X | X | | | | | X | AI security posture management; MCP server discovery and monitoring; runtime guardrails for prompt injection and data leakage; announced ahead of RSAC 2026 |
| Arize Phoenix (OSS) | | | | | | | | X | X | OpenTelemetry-native; drift detection; 7.8K+ GitHub stars |
| CrowdStrike AIDR / Falcon | | | X | X | | X | | X | X | RSA 2026 announcement: AIDR for Copilot Studio (real-time prompt inspection, injection detection), AIDR for Endpoint (desktop LLM clients), Shadow AI Discovery across endpoint/SaaS/cloud, AI Data Flow Discovery for Cloud |
| Capsule Security | | X | | | | | | X | X | Launched April 15, 2026 with $7M seed (Lama Partners, Forgepoint); agentless runtime monitoring and policy enforcement for AI agents (Cursor, Claude Code, Copilot Studio, ServiceNow, Salesforce Agentforce); founded by ex-F5/Unit 8200 and Transmit Security veterans |
| Zscaler AI Guard / SPLX | | | X | X | | | X | | X | AI Runtime Guardrails integrated with NVIDIA NeMo Guardrails (aiguard-nemo-guardrails connector); blocks prompt injection, PII exposure, data poisoning, and malicious outputs; 2026 SPLX acquisition extends coverage across the enterprise AI lifecycle |
| Noma Security | | X | X | X | | | | | X | Runtime guardrails for Microsoft Copilot Studio agents; policy enforcement on agent behavior before action completes |

---

## Coverage Gap Analysis

### Potential Missing Control Categories

- [ ] **Data Governance & Lineage** — While AD.14 covers privacy, broader data governance (lineage tracking, data quality monitoring, retention policies) spans C1, C8, and C12 but isn't a standalone category
- [ ] **Model Fairness & Bias Testing** — Referenced in C1 (1.4.6), C6 (6.5.4), C14 (14.5.3) but doesn't have its own AD category; currently folded into AD.15 and AD.18
- [ ] **Incident Forensics** — AD.17 covers incident response but forensic-specific controls (C13.5.2 AI forensic tools) could warrant their own category as the field matures
- [ ] **Hardware & Accelerator Security** — The current Appendix D source no longer lists AD.20 as a standalone category, but C4 still contains hardware security requirements. Keep tracking GPU partitioning, confidential computing, accelerator firmware, and attestation as a candidate category if future source revisions restore hardware-specific controls
- [ ] **Multi-Agent Coordination Security** — C9.8 covers multi-agent isolation but agent coordination patterns (consensus, conflict resolution, swarm safety) are emerging concerns. As of March 2026, 25.5% of deployed agents can create and task other agents autonomously
- [ ] **MCP-Specific Controls** — C10 spans authentication, transport, validation, and boundary enforcement for MCP, but MCP risk now cuts across AD.1, AD.2, AD.7, AD.10, AD.11, AD.12, AD.16, and AD.17. As of March 2026, over 10,000 active public MCP servers had appeared within roughly a year of the protocol's introduction, with 53% relying on static secrets for authentication (Astrix). OX Security's April 15, 2026 MCP STDIO advisory moved this from design concern to systemic supply-chain exposure, with RCE patterns affecting downstream platforms such as LangFlow, GPT Researcher, LiteLLM, Agent Zero, Flowise, DocsGPT, and Letta. A dedicated MCP control category may be warranted if this pattern continues
- [ ] **Agentic Coordination & Identity** — The OWASP Agentic AI Top 10 (2026) introduces 10 distinct risk categories (ASI01–ASI10) that cut across multiple AD categories. Agent identity, delegation chains, and inter-agent trust relationships are not fully captured by existing AD.1/AD.2 categories. The EY February 2026 survey found 52% of department-level AI initiatives operate without formal approval or oversight, and 78% of leaders say AI adoption outpaces their ability to manage it

### Controls Appearing in Multiple Categories

Some requirement IDs appear across multiple AD categories, which is expected for defense-in-depth:

| Requirement | Categories | Why |
|------------|------------|-----|
| 4.1.5 (TEE/confidential computing) | AD.10; candidate hardware category | Isolation with remote attestation; previously tracked under the removed AD.20 hardware category |
| 9.4.2 (execution chain signing) | AD.6, AD.16 | Both integrity and audit |
| 7.3.2 (PII redaction) | AD.8, AD.14 | Both output filtering and privacy |
| 11.5.4 (model watermarking) | AD.6, AD.15 | Both integrity and adversarial defense |

---

## Industry Adoption Snapshot (May 2026)

Overall adoption remains low — 94% of enterprises use AI in production, yet only 23% have mature security programs. As of May 2026, the governance gap is widening: 97% of tech executives view broad autonomous AI as a high or essential priority, but 52% of department-level AI initiatives operate without formal oversight (EY, February 2026). The Zscaler 2026 AI Security Report logged a 91% year-over-year increase in AI/ML traffic across more than 3,400 applications, with Finance/Insurance carrying 23% of volume and Technology and Education sectors growing 202% and 184% respectively. The OX MCP disclosure and MCPTox benchmark add a sharper point: the riskiest adoption gap is no longer just model access, but ungoverned tool execution.

| Metric | Percentage | Source |
|--------|:----------:|--------|
| Enterprises using AI in production | 94% | CyberSecFeed AI Security Maturity Model |
| Tech execs rating autonomous AI as high/essential priority | 97% | EY Autonomous AI Survey (Feb 2026) |
| Orgs implementing any GenAI security controls | 47% | Microsoft Cyber Pulse AI Security Report |
| Orgs enforcing AI security inline, at point of action | 23% | Industry aggregate |
| Orgs with comprehensive AI security governance | 25% | CSA AI Security & Governance Survey (Dec 2025) |
| Orgs with advanced AI security strategy | 6% | Gartner (2026) |
| Orgs with full security approval for AI agents | 14.4% | Gravitee State of AI Agent Security 2026 |
| Orgs with real-time governance enforcement | 7% | Industry aggregate |
| Dept-level AI initiatives without formal oversight | 52% | EY Autonomous AI Survey (Feb 2026) |
| AI agents actively monitored/secured | 47.1% | Gravitee |
| Models lacking security scanning | 67% | CyberSecFeed |
| Models vulnerable to prompt attacks | 89% | CyberSecFeed |
| Orgs using unvetted pre-trained models | 91% | CyberSecFeed |
| Orgs reporting AI security incidents in past year | 88% | Gravitee |
| Orgs with no visibility into AI data flows | 86% | HelpNetSecurity (March 2026) |
| Confirmed/suspected sensitive data leak via unauthorized GenAI | 45% | EY (Feb 2026) |
| Confirmed/suspected proprietary IP leak via unauthorized GenAI | 39% | EY (Feb 2026) |
| Orgs with formal GenAI governance reducing data leakage | up to 46% reduction | Practical DevSecOps (March 2026) |
| Cybersecurity pros identifying agentic AI as #1 attack vector | 48% | Dark Reading poll (2026) |
| Enterprises with at least one AI workload in production | 72% | Cybersecurity Insiders AI Risk Report (Q1 2026) |
| Orgs describing AI adoption as "mature" across functions | 28% | Cybersecurity Insiders AI Risk Report (Q1 2026) |
| Orgs with comprehensive AI security governance policies | 26% | CSA/Google Cloud AI Governance Study (2026) |
| Year-over-year growth in enterprise AI/ML traffic | 91% | Zscaler 2026 AI Security Report |
| Unique AI/ML applications observed in enterprise traffic | 3,400+ | Zscaler 2026 AI Security Report |

**Maturity distribution** (CyberSecFeed 5-level model): Level 0 (Unaware) 34%, Level 1 (Initial) 28%, Level 2 (Developing) 23%, Level 3 (Managed) 12%, Level 4 (Optimized) 3%.

**The velocity paradox:** EY describes the structural mismatch where 73% of orgs deploy AI tools while only 7% govern them in real time. Gartner forecasts 40% of enterprise applications will feature task-specific AI agents by 2026, but only 6% of organizations have an advanced AI security strategy. Organizations with formal GenAI governance policies reduce data leakage incidents by up to 46% compared to those without controls, suggesting the gap is both measurable and remediable. A CSA/Google Cloud study (December 2025) found governance maturity is the strongest predictor of AI readiness — organizations with comprehensive policies are nearly twice as likely to report early agentic AI adoption (46%) compared to those with partial guidelines (25%).

---

## Community Notes

_Discussion about control inventory completeness and organization._

---

## Related Pages

- [Appendix B: References](Appendix-B-References.md) — useful when checking whether the control inventory still cites the same external frameworks as the core standard.
- [C10-05 Outbound Access & Agent Safety](../chapters/C10-MCP-Security/C10-05-Outbound-Access-Agent-Safety.md) — digs into the MCP and agent egress controls that now cut across several AD categories.
- [Appendix A: Glossary](Appendix-A-Glossary.md) — keeps terminology for ATLAS, MCP, control overlays, and agentic security patterns consistent across the wiki.
- [C02-01 Prompt Injection Defense](../chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) — provides the detailed prompt and tool-injection background behind AD.7 and AD.10.
- [C03-02 Model Validation & Testing](../chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md) — connects the inventory to validation gates for model, agent, MCP, and release workflows.

---

## References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [NIST IR 8596: Cybersecurity Framework Profile for AI (Draft, December 2025)](https://csrc.nist.gov/pubs/ir/8596/iprd)
* [NIST SP 800-53 Control Overlays for Securing AI Systems (COSAiS)](https://csrc.nist.gov/Projects/cosais)
* [NIST COSAiS Use Cases: Single-Agent, Multi-Agent, and AI Developer Overlays](https://csrc.nist.gov/Projects/cosais/use-cases)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [MITRE ATLAS — Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/)
* [MITRE ATLAS Grows through Collaboration with CTID and Industry (May 2026)](https://ctid.mitre.org/blog/2026/05/06/secure-ai-v2-release/)
* [MITRE SAFE-AI Framework (Full Report)](https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf)
* [CSA AI Controls Matrix (AICM)](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix)
* [CSA State of AI Security and Governance (December 2025)](https://cloudsecurityalliance.org/artifacts/the-state-of-ai-security-and-governance)
* [OWASP Top 10 for Large Language Model Applications (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP AI Maturity Assessment (AIMA, v1.0 August 2025)](https://owasp.org/www-project-ai-maturity-assessment/)
* [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)
* [EU AI Act — Article 15 (Robustness & Cybersecurity)](https://artificialintelligenceact.eu/article/15/)
* [EU AI Act — Annex IV (Technical Documentation)](https://artificialintelligenceact.eu/annex/4/)
* [EU General-Purpose AI Code of Practice — Safety and Security Chapter](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai)
* [OpenSSF Model Signing (OMS) Specification (June 2025)](https://openssf.org/blog/2025/06/25/an-introduction-to-the-openssf-model-signing-oms-specification/)
* [Gravitee State of AI Agent Security 2026 Report](https://www.gravitee.io/blog/state-of-ai-agent-security-2026-report-when-adoption-outpaces-control)
* [Microsoft Cyber Pulse: AI Security Report](https://www.microsoft.com/en-us/security/security-insider/emerging-trends/cyber-pulse-ai-security-report)
* [Lakera GenAI Security Readiness Report 2025](https://www.lakera.ai/genai-security-report-2025)
* [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
* [OWASP AI Exchange](https://owaspai.org/)
* [Microsoft Zero Trust for AI (March 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/19/new-tools-and-guidance-announcing-zero-trust-for-ai/)
* [EY Survey: Autonomous AI Adoption Surges as Oversight Falls Behind (February 2026)](https://www.ey.com/en_us/newsroom/2026/03/ey-survey-autonomous-ai-adoption-surges-at-tech-companies-as-oversight-falls-behind)
* [Qualys TotalAI: MCP Servers as Shadow IT (March 2026)](https://blog.qualys.com/product-tech/2026/03/19/mcp-servers-shadow-it-ai-qualys-totalai-2026)
* [Straiker: Agentic AI Security Platform](https://www.straiker.ai/)
* [MITRE ATLAS OpenClaw Investigation (February 2026)](https://ctid.mitre.org/blog/2026/02/09/mitre-atlas-openclaw-investigation/)
* [MITRE ATLAS OpenClaw Investigation Report (PDF)](https://www.mitre.org/sites/default/files/2026-02/PR-26-00176-1-MITRE-ATLAS-OpenClaw-Investigation.pdf)
* [Zenity Labs: Contributions to MITRE ATLAS First 2026 Release](https://zenity.io/blog/current-events/zenitys-contributions-to-mitre-atlas-first-2026-update)
* [F5 AI Guardrails and AI Red Team (January 2026)](https://www.f5.com/company/news/press-releases/f5-accelerates-ai-security-with-integrated-runtime-protection-for-enterprise-ai-at-scale)
* [Varonis Atlas: AI Security Platform (March 2026)](https://www.varonis.com/blog/atlas-ai-security)
* [Cybersecurity Insiders: AI Risk and Readiness Report 2026](https://www.cybersecurity-insiders.com/ai-risk-and-readiness-report-2026/)
* [Capsule Security Launches with $7M to Secure AI Agents at Runtime (SiliconANGLE, April 15, 2026)](https://siliconangle.com/2026/04/15/capsule-security-launches-7m-secure-ai-agents-runtime/)
* [CrowdStrike Establishes the Endpoint as the Epicenter for AI Security (March 2026)](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-establishes-the-endpoint-as-the-epicenter-for-ai-security/)
* [Kong AI Gateway 3.14: Agent-to-Agent Traffic and Kong Agent Gateway (April 14, 2026)](https://www.prnewswire.com/news-releases/kong-ai-gateway-now-supports-agent-to-agent-traffic-becoming-the-most-comprehensive-ai-gateway-for-the-agentic-era-302741741.html)
* [Kong Agent Gateway: Complete AI Gateway for Agent-to-Agent Communication (April 2026)](https://konghq.com/blog/product-releases/kong-agent-gateway)
* [Operant Endpoint Protector for Shadow AI, Coding Agents, and MCP (May 2026)](https://www.globenewswire.com/news-release/2026/05/04/3286769/0/en/Operant-AI-Launches-Endpoint-Protector-Securing-Shadow-AI-Coding-Agents-and-MCP-Across-the-Enterprise.html)
* [Salt Agentic Security Platform for LLMs, MCP Servers, and APIs (March 2026)](https://www.prnewswire.com/news-releases/salt-security-launches-industrys-first-agentic-security-platform-for-the-ai-stack-across-llms-mcp-servers-and-apis-302716939.html)
* [Kong MCP Gateway Overview](https://konghq.com/resources/reports/mcp-gateway)
* [LiteLLM Security Update: Suspected Supply Chain Incident (March 24, 2026)](https://docs.litellm.ai/blog/security-update-march-2026)
* [OX Security MCP Supply Chain Advisory: RCE Vulnerabilities Across the AI Ecosystem (April 2026)](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/)
* [MCPTox: A Benchmark for Tool Poisoning on Real-World MCP Servers (AAAI 2026)](https://ojs.aaai.org/index.php/AAAI/article/view/40895)
* [Zscaler AI Guardrails and NeMo Guardrails Integration](https://www.zscaler.com/blogs/partner/securing-genai-applications-zscaler-ai-guard-and-nvidia-nemo-guardrails)
* [Zscaler 2026 AI Security Report](https://www.zscaler.com/press/zscaler-2026-ai-threat-report-91-year-over-year-surge-ai-activity-creates-growing-oversight)
* [sigstore/model-transparency — Supply chain security for ML](https://github.com/sigstore/model-transparency)
* [OpenSSF Model Signing Specification (Repo)](https://github.com/ossf/model-signing-spec)
* [Noma Security: Runtime Guardrails for Microsoft Copilot Studio](https://noma.security/blog/runtime-guardrails-for-microsoft-copilot-studio-agents/)

---

[README](../README.md)
