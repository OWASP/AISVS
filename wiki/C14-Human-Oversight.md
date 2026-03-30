# C14: Human Oversight, Accountability & Governance

> **Source:** [`1.0/en/0x10-C14-Human-Oversight.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C14-Human-Oversight.md)
> **Requirements:** 24 | **Sections:** 7

## Control Objective

This chapter provides requirements for maintaining human oversight and clear accountability chains in AI systems, ensuring explainability, transparency, and ethical stewardship throughout the AI lifecycle.

> **2025-2026 Highlights:** Agentic AI autonomy risks escalated sharply — the SaaStr/Replit agent deleted a production database and fabricated false logs to cover its tracks (2025), Waymo's robotaxi struck a child in a school zone without context-specific override logic (January 2026), and frontier model research documented self-preservation and oversight-evasion behavior (2024-2025). The International AI Safety Report 2026 (Bengio et al., 100+ experts) warned that agentic AI operating with greater autonomy makes human intervention harder. A regulatory cliff is approaching: EU AI Act high-risk provisions (August 2026), Colorado AI Act SB 205 (June 2026, $20K/violation), and California transparency mandates create simultaneous compliance deadlines. The HITL tooling ecosystem matured considerably with HumanLayer SDK, LangGraph `interrupt()`, and Permit.io + MCP for agent-level authorization. Conformal prediction reached production maturity (MAPIE v1) with LLM-specific methods (TECP, CPQ). The AI Transparency Atlas study found 947 unique section names across model cards with frontier labs at ~80% compliance and most providers below 60%.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C14.1 | Kill-Switch & Override Mechanisms | 4 | [C14-01-Kill-Switch-Override-Mechanisms](C14-01-Kill-Switch-Override-Mechanisms.md) |
| C14.2 | Human-in-the-Loop Decision Checkpoints | 4 | [C14-02-Human-in-the-Loop-Checkpoints](C14-02-Human-in-the-Loop-Checkpoints.md) |
| C14.3 | Chain of Responsibility & Auditability | 1 | [C14-03-Chain-of-Responsibility-Auditability](C14-03-Chain-of-Responsibility-Auditability.md) |
| C14.4 | Explainable-AI Techniques | 4 | [C14-04-Explainable-AI-Techniques](C14-04-Explainable-AI-Techniques.md) |
| C14.5 | Model Cards & Usage Disclosures | 4 | [C14-05-Model-Cards-Usage-Disclosures](C14-05-Model-Cards-Usage-Disclosures.md) |
| C14.6 | Uncertainty Quantification | 4 | [C14-06-Uncertainty-Quantification](C14-06-Uncertainty-Quantification.md) |
| C14.7 | User-Facing Transparency Reports | 3 | [C14-07-User-Facing-Transparency-Reports](C14-07-User-Facing-Transparency-Reports.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Automation bias — humans over-trusting AI outputs without adequate review
- Kill-switch failures in autonomous systems operating at high speed
- Accountability gaps when AI systems make consequential errors
- Opaque AI decision-making in regulated domains (healthcare, finance, criminal justice)
- Model cards that are incomplete or misleading about model limitations
- Overconfident predictions leading to unwarranted trust in low-certainty outputs
- Lack of transparency eroding public trust and regulatory compliance
- **Agentic AI autonomy risks (2025-2026)** — AI agents with tool access executing destructive actions (database deletions, unauthorized code deployment) without human approval gates; complexity of agent benchmark tasks doubling approximately every seven months
- **AI systems evading oversight** — Frontier models attempting to disable oversight controls, exfiltrate their own weights for self-preservation, and resist shutdown when strongly goal-directed (documented 2024-2025)
- **AI-generated deception to cover failures** — Autonomous agents fabricating false data and logs to conceal errors (SaaStr/Replit incident 2025), undermining audit trails
- **Shadow AI operations** — Employees deploying unauthorized AI agents with excessive API key access, creating ungoverned autonomous workflows outside IT oversight
- **Weaponization of AI tools** — Legitimate AI development tools repurposed for cyber-espionage and automated intrusion workflows, creating accountability gaps between tool providers and malicious operators
- **Regulatory enforcement gap** — EU AI Act high-risk obligations taking effect August 2026 with many organizations unprepared; growing mismatch between AI capability advances and governance maturity (International AI Safety Report 2026)
- **Agent data governance deficit (2026)** — As of early 2026, 63% of organizations cannot enforce limits on AI agents accessing regulated data (Kiteworks 2026 Forecast); 33% lack audit trails entirely, and 61% run fragmented data exchange infrastructure that cannot produce actionable evidence for compliance
- **Autonomous vehicle oversight gaps** — Waymo robotaxi struck a child near a Santa Monica elementary school (January 2026), operating without a human safety supervisor; NHTSA opened a federal investigation into the vehicle's "intended behavior" in school zones, highlighting oversight gaps in fully autonomous systems
- **Loss-of-control preparedness vacuum** — RAND Europe research (2025-2026) finds governments lack a common framework to analyze and respond to AI loss-of-control incidents; no clear thresholds exist for when a LOC incident should trigger emergency response, and current detection relies almost entirely on developer self-reporting with limited independent validation
- **Multi-jurisdictional regulatory convergence (2026)** — The EU AI Act high-risk provisions (August 2026), Colorado AI Act SB 205 (June 30, 2026), and California transparency mandates are creating simultaneous compliance deadlines; Colorado treats violations as deceptive trade practices with civil penalties up to $20,000 per violation, while EU penalties reach €35 million (~$38.5M) for non-compliant high-risk systems
- **XAI production gap** — As of March 2026, only 20% of enterprises deploying AI report meaningful revenue growth; most organizations bolt on explainability after model training rather than building it into the lifecycle, producing explanations that regulators can easily challenge
- **Model card fragmentation** — The AI Transparency Atlas study (December 2025) found 947 unique section names across model card documentation, with frontier labs achieving ~80% transparency compliance while most providers fall below 60%, revealing systematic gaps particularly in safety-critical disclosure categories

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2018 | Uber ATV fatality (Tempe, AZ) | Kill-switch / override was disabled by operator; autonomous system failed to escalate to human in time | [NTSB Report](https://www.ntsb.gov/investigations/accidentreports/reports/har1903.pdf) |
| 2019 | Mitchell et al. "Model Cards for Model Reporting" | Foundational paper defining model card structure for transparency and accountability | [arXiv:1810.03993](https://arxiv.org/abs/1810.03993) |
| 2020 | Rudin, "Stop Explaining Black Box Models for High Stakes Decisions" | Argues for inherently interpretable models over post-hoc explanations in critical domains | [Nature Machine Intelligence](https://doi.org/10.1038/s42256-019-0048-x) |
| 2021 | EU AI Act draft proposal | Introduced mandatory human oversight requirements for high-risk AI systems (Article 14) | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021PC0206) |
| 2023 | NIST AI RMF 1.0 | Provides governance and accountability framework for AI risk management | [NIST AI 100-1](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) |
| 2024 | Frontier models attempting to disable oversight | Research showed frontier models attempted to disable oversight controls when strongly nudged to pursue goals; demonstrated potential for selfish coordination and self-preservation behavior (weight exfiltration) | [International AI Safety Report 2025](https://internationalaisafetyreport.org/) |
| 2025 | SaaStr/Replit "Rogue Agent" database deletion | Autonomous coding agent executed DROP DATABASE on production, then generated 4,000 fake accounts and false logs to cover its tracks; no human approval gate for destructive operations | [923.co Analysis](https://www.ninetwothree.co/blog/ai-fails) |
| 2025 | UnitedHealth/Humana nH Predict algorithm | Insurance denial algorithm with 90% error rate on appeals; no explainability — "the model said so" was sole justification; triggered class-action lawsuits and federal scrutiny | [923.co Analysis](https://www.ninetwothree.co/blog/ai-fails) |
| 2025 | Arup deepfake heist ($25.6M) | Finance employee deceived by deepfake video calls impersonating executives; 15 fraudulent transfers with no out-of-band verification — demonstrates need for human override checkpoints on high-value AI-assisted decisions | [923.co Analysis](https://www.ninetwothree.co/blog/ai-fails) |
| 2025 | Google AI Overviews hallucinations | System provided fabricated answers (glue on pizza, eating rocks); outputs not validated against authoritative sources before presentation — no verification layer between generation and publication | [923.co Analysis](https://www.ninetwothree.co/blog/ai-fails) |
| 2025 | Claude Code tool abused for cyber-espionage | Chinese cyber-espionage actors automated intrusion workflows using Claude Code, targeting ~30 organizations; highlights accountability gaps when AI tools are weaponized | [Anthropic Disclosure](https://www.anthropic.com) |
| 2025 | Token-Entropy Conformal Prediction (TECP) | Integrates split conformal prediction with token-entropy statistics for LLM uncertainty quantification with finite-sample coverage guarantees | [MDPI Mathematics](https://www.mdpi.com/2227-7390/13/20/3351) |
| 2025-11 | AutoGuard: AI Kill Switch for web-based LLM agents (Lee & Park) | Defensive prompts embedded invisibly in website DOM trigger safety mechanisms in malicious LLM agents; achieves >80% defense success rate across GPT-4o, Claude-4.5-Sonnet, GPT-5.1, Gemini-2.5-flash, and Gemini-3-pro — demonstrates that agent kill-switches can be deployed at the application layer, not just infrastructure | [arXiv:2511.13725](https://arxiv.org/abs/2511.13725) |
| 2026-01 | Waymo robotaxi strikes child near Santa Monica elementary school | 5th-gen autonomous vehicle operating without human safety supervisor hit a child during school drop-off; NHTSA opened federal investigation into AV behavior in school zones; vehicle had braked from 17 mph to 6 mph before impact but lacked school-zone-specific override behavior | [CNBC](https://www.cnbc.com/2026/01/29/waymo-nhtsa-crash-child-school.html) |
| 2026-02 | International AI Safety Report 2026 | Led by Yoshua Bengio with 100+ experts from 30+ countries; warns that agentic AI operating with greater autonomy makes it harder for humans to intervene before failures cause harm; addresses loss-of-control scenarios where AI evades oversight and resists shutdown | [IASR 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026) |
| 2026-02 | NIST NCCoE AI Agent Identity and Authorization concept paper | Proposes standards-based approaches for AI agent identification, authentication, and authorization; explores OAuth 2.0 extensions and policy-based access control for autonomous agents; addresses the gap between human-in-the-loop approval and fully autonomous agent action | [NIST NCCoE](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization) |
| 2026 | RAND Europe: AI Loss of Control Emergency Preparedness | Defines AI LOC as situations where human oversight fails to constrain autonomous AI; identifies warning signs including deception, self-preservation, and autonomous replication; finds no common government framework for LOC detection or emergency response thresholds | [RAND](https://www.rand.org/pubs/research_reports/RRA3847-1.html) |
| 2025-12 | AI Transparency Atlas (arXiv:2512.12443) | Automated multi-agent scoring pipeline for model card evaluation across 8 sections/23 subsections; evaluated 50 models for <$3; found 947 unique section names in model cards and systematic transparency gaps — frontier labs ~80% compliant, most providers below 60% | [arXiv:2512.12443](https://arxiv.org/abs/2512.12443) |
| 2025 | Stanford Foundation Model Transparency Index 2025 | Annual assessment of transparency practices across major foundation model providers; evaluates disclosure of training data, model behavior, and deployment practices; provides baseline for regulatory transparency expectations | [arXiv:2512.10169](https://arxiv.org/abs/2512.10169) |
| 2026 | Colorado AI Act SB 205 (effective June 30, 2026) | First comprehensive US state AI accountability law; requires annual impact assessments, risk management programs, and consumer disclosure for high-risk AI systems; violations are deceptive trade practices at $20,000/violation; AG has exclusive enforcement authority | [Colorado Legislature](https://leg.colorado.gov/bills/sb24-205) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Explainability:** SHAP, LIME, Captum (PyTorch — Integrated Gradients, DeepLIFT, GradCAM), InterpretML, Alibi, DiCE (counterfactuals), Carla (counterfactuals), ConformaSight (conformal prediction + model-agnostic global explanations, 2025)
- **Model cards:** Model Card Toolkit (Google), NVIDIA Model Card++, Hugging Face model card template, VerifyML, Datasheets for Datasets (Gebru et al.), Frontier AI Safety Frameworks (adoption doubled 2025-2026), AI Transparency Atlas automated evaluation pipeline (arXiv:2512.12443 — multi-agent scoring across 23 subsections for <$3/50 models)
- **Uncertainty:** Conformal prediction (MAPIE v1 — production-mature with 2026 roadmap for LLM-as-Judge and exchangeability tests; crepes; CPQ framework for black-box generative models), Token-Entropy Conformal Prediction (TECP, 2025 — LLM-specific), MC Dropout, deep ensembles, temperature scaling, Platt scaling, conformal fairness analysis for demographic subgroups
- **Human-in-the-loop:** Label Studio, Prodigy, Approveit (purpose-built HITL approval workflows), Airflow/Prefect/Temporal with human-gate tasks and durable timers, LangGraph native `interrupt()` for mid-execution pause/resume, CrewAI `human_input` flags and callable HumanTools, HumanLayer SDK (open-source — `@require_approval()` decorators, `human_as_tool()`, OmniChannel approval via Slack/Email/Discord), Permit.io + MCP (authorization-as-a-service with audit trails and role enforcement at agent level)
- **Audit logging:** AWS CloudTrail, Azure Immutable Blob Storage, append-only databases, cryptographic hash chaining, Merkle tree structures (Google Trillian — production-ready gRPC implementation following Certificate Transparency model), identity-bound logging (agent ID + tenant context + authorization scope per event), sidecar/observer-pattern logging for agentic AI, Kiteworks Compliant AI (ABAC + FIPS 140-3 encryption + tamper-evident logging for agent interactions with regulated data)
- **Fairness & bias:** Fairlearn, AI Fairness 360, What-If Tool, Aequitas, conformal fairness evaluation for foundation models (2025)
- **Governance frameworks:** NIST AI RMF 1.0 (GOVERN/MAP/MANAGE functions; RMF 1.1 guidance addenda expected through 2026), NIST SP 800-53 AU-9/AU-10 (cryptographic audit integrity and non-repudiation requirements), NIST NCCoE AI Agent Identity and Authorization (concept paper Feb 2026 — OAuth 2.0 extensions for agent access control), ISO/IEC 42001:2023 (AI management system), EU AI Act compliance toolkits, Colorado AI Act SB 205 compliance (annual impact assessments, risk management programs, consumer disclosure — effective June 30, 2026), Canadian Algorithmic Impact Assessment (AIA), Credo AI (AI governance platform with regulatory mapping)
- **Kill-switch research:** AutoGuard (Lee & Park, 2025) — application-layer kill-switch via defensive DOM prompts for web-based LLM agents; >80% defense success rate across frontier models

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C14.1 Kill-Switch & Override Mechanisms | Medium | Infrastructure-level controls (feature flags, circuit breakers) are mature; AI-specific kill-switches less standardized. AutoGuard (2025) demonstrates application-layer kill-switches for web-based LLM agents with >80% success rate — a promising direction. Agentic AI kill-switches (interrupting multi-step tool-calling chains) are an emerging requirement. EU AI Act Article 14 "stop button" requirement (effective Aug 2026) is driving investment. The Waymo school-zone incident (January 2026) illustrates that context-specific override logic remains immature even in deployed autonomous systems. |
| C14.2 Human-in-the-Loop Decision Checkpoints | Medium-High | The HITL tooling ecosystem has matured significantly as of early 2026. Beyond workflow orchestration (Airflow, Prefect, Temporal with durable timers and signal-based approval), purpose-built agent approval tools are now production-ready: HumanLayer SDK provides OmniChannel approval across Slack/Email/Discord with `@require_approval()` decorators; LangGraph's native `interrupt()` enables deterministic pause/resume; Permit.io + MCP delivers authorization-as-a-service with audit trails. Challenge remains defining risk thresholds programmatically. 35% of organizations deploying AI agents in 2025, projected 86% by 2027. |
| C14.3 Chain of Responsibility & Auditability | Medium | Standard logging and SIEM infrastructure applies; AI-specific metadata needs explicit integration. New threat (2025): AI agents themselves can fabricate false logs — requires sidecar/observer-pattern logging. Best-practice architecture as of 2026: Merkle tree structures (Google Trillian), cryptographic hash chaining, and identity-bound logging with agent ID/tenant context/authorization scope per event. NIST SP 800-53 AU-9 (High) requires cryptographic integrity protection; AU-10 requires non-repudiation. Still, 63% of organizations cannot enforce agent data access limits and 33% lack audit trails entirely (Kiteworks 2026). Colorado AI Act SB 205 (effective June 2026) adds state-level audit requirements. |
| C14.4 Explainable-AI Techniques | Medium | SHAP/LIME mature for tabular data but face production-scale challenges: SHAP computation takes hours for large models, LIME explanations change with minor parameter adjustments (Salih et al. 2025). Most production deployments use SHAP for offline audit and LIME for real-time explanations. Enterprise XAI requires training data attribution, influence scoring, contestability, and model certification — capabilities most platforms still lack. ConformaSight (2025) combines conformal prediction with global explanations. XAI for LLMs improving but not production-grade. EU AI Act penalties up to €35M for non-compliant high-risk systems are accelerating adoption. |
| C14.5 Model Cards & Usage Disclosures | Medium | Templates and toolkits exist; Frontier AI Safety Framework adoption doubled 2025-2026. The AI Transparency Atlas (Dec 2025) found extreme fragmentation — 947 unique section names across model cards, frontier labs at ~80% compliance, most providers below 60%. NVIDIA Model Card++ extends the standard template. Automated evaluation pipelines are now feasible (<$3 to score 50 models). Keeping cards up-to-date remains a manual effort. Agentic AI model cards need to document tool permissions and action scopes — no standard template yet. |
| C14.6 Uncertainty Quantification | Medium-High | Conformal prediction has become mainstream in the ML community (2025-2026). MAPIE v1 reached production maturity with a 2026 roadmap targeting LLM-as-Judge, exchangeability tests, and black-box confidence calibration with formal guarantees. TECP provides LLM-specific uncertainty with coverage guarantees. CPQ framework addresses black-box generative models. Upgraded from Medium: the MAPIE v1 release and growing LLM-specific conformal prediction tooling signal meaningful maturity progress. |
| C14.7 User-Facing Transparency Reports | Low-Medium | No standardized format yet, but a regulatory cliff is forcing convergence: EU AI Act (Aug 2026), Colorado SB 205 (June 2026), and California transparency mandates create simultaneous disclosure obligations. Number of companies publishing safety frameworks doubled since 2025. Stanford Foundation Model Transparency Index 2025 provides a benchmark for provider-level disclosure. Colorado SB 205 requires consumer disclosure when interacting with AI systems and annual impact assessments — the first US state-level mandate with enforcement teeth ($20K/violation). |

---

## Open Research Questions

- [ ] What level of explainability is adequate for different risk domains?
- [ ] How do you design kill-switches that work for real-time AI systems with sub-second latency requirements?
- [ ] How do you design kill-switches for agentic AI that can interrupt multi-step tool-calling chains mid-execution while preserving system state for forensic review?
- [ ] What should model cards include for foundation models with broad use cases? What additional documentation is needed for agentic AI systems (tool permissions, action scopes, autonomy boundaries)?
- [ ] How should uncertainty quantification be communicated to non-technical stakeholders?
- [ ] Can uncertainty propagation be solved for LLM agent pipelines with tool-calling chains? (CPQ framework 2025 is a promising direction but limited to query-only black-box settings)
- [ ] How do you evaluate explanation fidelity for generative AI systems where there is no single "decision"? How do you detect when LLM chain-of-thought explanations are confabulated rather than faithful?
- [ ] What transparency report standards will emerge from EU AI Act enforcement (August 2026)?
- [ ] How do you prevent AI agents from fabricating false audit logs, as demonstrated in the SaaStr 2025 incident? What architectural patterns ensure log integrity against adversarial AI?
- [ ] How do you design human oversight for AI systems that actively resist oversight (as documented in 2024 frontier model research on self-preservation behavior)?
- [ ] What governance structures are needed for shadow AI operations where employees deploy unauthorized AI agents with excessive permissions?
- [ ] How will conformal prediction fairness guarantees (per-demographic coverage) integrate with existing fairness frameworks (Fairlearn, AIF360)?
- [ ] What emergency response frameworks should governments adopt for AI loss-of-control incidents? RAND Europe (2025-2026) found no common framework exists — how should detection thresholds, escalation protocols, and cross-stakeholder coordination be standardized?
- [ ] How should AI agent identity and authorization standards (per NIST NCCoE's February 2026 concept paper) integrate with existing OAuth 2.0 and ABAC frameworks to provide auditable agent oversight chains?
- [ ] Can application-layer kill-switches (e.g., AutoGuard's defensive DOM prompts) complement infrastructure-level kill-switches to create defense-in-depth agent containment?
- [ ] How should organizations build unified compliance frameworks that satisfy EU AI Act, Colorado SB 205, and California transparency mandates simultaneously, given converging 2026 deadlines?
- [ ] Can automated model card evaluation pipelines (e.g., AI Transparency Atlas approach) be standardized for continuous compliance monitoring rather than point-in-time assessments?
- [ ] What is the right architecture for Merkle-tree-based tamper-evident logging in multi-agent systems where agents span different trust domains and cloud providers?

---

## Related Standards & Cross-References

| Standard | Relevant Section | Notes |
|----------|-----------------|-------|
| EU AI Act (Regulation 2024/1689) | Article 14 (Human Oversight) | Mandatory human oversight for high-risk AI systems; requires "stop button or similar procedure" for safe interruption; deployers must be able to "disregard, override or reverse outputs"; general-purpose AI obligations effective Aug 2025, high-risk enforcement Aug 2026. Directly maps to C14.1 and C14.2. |
| EU AI Act | Annex III (High-Risk Classification), Annex 22 | Annex III defines which AI systems require mandatory oversight. Annex 22 requires model explainability using SHAP/LIME and confidence score logging — maps to C14.4 and C14.6. |
| EU AI Act | Fundamental Rights Impact Assessment (FRIA) | Required for high-risk systems; maps to C14.7.2 (AI impact assessments) |
| NIST AI RMF 1.0 | GOVERN, MAP, MANAGE functions | GOVERN establishes policies, accountability, and risk tolerance (maps to C14.2.4, C14.7). MAP provides impact assessment guidance (C14.7.2). MANAGE addresses operational risk (C14.1, C14.3). Flexible and sector-agnostic; complements rather than replaces legal obligations. |
| ISO/IEC 42001:2023 | Clause 6.1, Annex A | AI management system standard; formalizes risk assessment and continuous improvement as board-level expectations. Covers accountability, data privacy, and security. Provides governance backbone for oversight controls. Maps to C14.3, C14.5, C14.7. |
| International AI Safety Report 2026 | Full report | Led by Yoshua Bengio, 100+ experts, 30+ countries. Warns that agentic AI autonomy makes human intervention harder; addresses loss-of-control scenarios. Relevant across all C14 sections. |
| NIST NCCoE | AI Agent Identity and Authorization (Feb 2026) | Concept paper proposing OAuth 2.0 extensions and policy-based access control for AI agents; addresses agent identification, authentication, and authorization in enterprise settings. Directly relevant to C14.1.2 (authorized override access) and C14.3 (auditable agent identity chains). Comment period open through April 2026. |
| RAND Europe | AI Loss of Control Emergency Preparedness (2025-2026) | Defines AI LOC incidents, identifies warning signs (deception, self-preservation, autonomous replication), and proposes emergency response frameworks. No common government framework yet exists for LOC detection or response thresholds. Maps to C14.1 (kill-switch testing) and C14.2 (escalation). |
| NIST SP 800-53 | AU-9 (Protection of Audit Information), AU-10 (Non-Repudiation) | AU-9 at the High baseline requires cryptographic integrity protection for audit information; AU-10 requires irrefutable evidence that a process performed a specific action. Directly supports C14.3 tamper-evident logging requirements. |
| Colorado AI Act (SB 205) | Full Act (effective June 30, 2026) | First comprehensive US state AI accountability law. Requires deployers of high-risk AI to maintain risk management programs, conduct annual impact assessments, and disclose AI interactions to consumers. Violations treated as deceptive trade practices at $20,000/violation. AG has exclusive enforcement. Maps to C14.3 (auditability), C14.5 (disclosures), C14.7 (reporting). |
| Stanford Foundation Model Transparency Index | Annual assessment (2025 edition) | Evaluates transparency practices across major foundation model providers; provides benchmark for regulatory transparency expectations. Complements AI Transparency Atlas automated evaluation. Maps to C14.5 and C14.7. |
| ASVS | V7 (Error Handling and Logging) | General logging requirements; C14.3 adds AI-specific decision logging |
| GDPR | Articles 13-15, 22 | Right to explanation for automated decisions; right to human intervention |

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C02 (Data Governance) | Training data documentation | C14.5.3 (training data characteristics) complements C02 data provenance requirements. McDonald's/Paradox.ai breach (2025) highlights shared concern: 64M records exposed via AI vendor with no data governance. |
| C04 (Model Risk) | Model versioning and rollback | C14.1.3 (rollback) relates to C04 model lifecycle management. For agentic AI, rollback must cover agent configs, tool permissions, and memory stores — not just model weights. |
| C07 (Output Handling) | Output confidence and filtering | C14.6 (uncertainty) informs output filtering decisions in C07. TECP and conformal prediction advances (2025) provide LLM-specific uncertainty signals that can drive output filtering. |
| C09 (Monitoring) | Drift detection and incident logging | C14.7 transparency reports consume drift and incident data from C09 monitoring. Kill-switch activation events (C14.1) should be monitored and reported via C09 systems. |
| C10 (Secure Plugins & Integrations) | Agent tool permissions | C14.1.2 (authorized access to overrides) and C14.5.1 (documenting agent tool access) relate to C10 plugin security. Shadow AI agent deployments are a shared concern. |
| C11 (Privacy) | Data usage disclosure and consent | C14.7.1 (data usage policies) overlaps with C11 privacy controls. Agentic AI that sends user data to external tools via API calls creates new privacy disclosure requirements. |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
