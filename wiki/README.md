# AISVS Research Wiki

**OWASP AI Security Verification Standard: Research and Analysis Hub**

Welcome to the AISVS research wiki. This wiki provides structured research context for every chapter and appendix in AISVS 1.0, helping developers, auditors, and security teams understand and implement each requirement. Every requirement is mapped to the threats it mitigates, the tools and techniques available to implement it, practical verification approaches, and open questions where tooling or research is still maturing. Whether you are building an AI application, auditing one, or evaluating your organization's AI security posture, this wiki is designed to help you get started.

---

## Chapters

The standard is organized into 14 chapters spanning the full AI application security lifecycle, from training data through deployment, monitoring, and human oversight. Larger chapters are split into per-section pages for easier navigation, while smaller chapters are covered on a single page.

| # | Chapter | Reqs | Pages | Type | Updated |
|---|---------|:----:|:-----:|------|:-------:|
| C1 | Training Data Integrity & Traceability | 24 | [C01](C01-Training-Data.md) | Single | 2026-03-22 |
| C2 | User Input Validation | 33 | [C02](C02-User-Input-Validation.md) | [8 sections](#c2-user-input-validation) | 2026-03-22 |
| C3 | Model Lifecycle Management | 24 | [C03](C03-Model-Lifecycle-Management.md) | Single | 2026-03-22 |
| C4 | Infrastructure & Deployment Security | 46 | [C04](C04-Infrastructure.md) | [8 sections](#c4-infrastructure--deployment-security) | 2026-03-22 |
| C5 | Access Control & Identity | 26 | [C05](C05-Access-Control.md) | Single | 2026-03-22 |
| C6 | Supply Chain Security | 33 | [C06](C06-Supply-Chain.md) | [7 sections](#c6-supply-chain-security) | 2026-03-22 |
| C7 | Model Behavior & Output Control | 33 | [C07](C07-Model-Behavior.md) | [8 sections](#c7-model-behavior--output-control) | 2026-03-22 |
| C8 | Memory, Embeddings & Vector DB Security | 25 | [C08](C08-Memory-and-Embeddings.md) | Single | 2026-03-22 |
| C9 | Orchestration & Agentic Action Security | 36 | [C09](C09-Orchestration-and-Agents.md) | [8 sections](#c9-orchestration--agentic-action-security) | 2026-03-22 |
| C10 | MCP Security | 34 | [C10](C10-MCP-Security.md) | [6 sections](#c10-mcp-security) | 2026-03-22 |
| C11 | Adversarial Robustness | 41 | [C11](C11-Adversarial-Robustness.md) | [10 sections](#c11-adversarial-robustness) | 2026-03-21 |
| C12 | Privacy Protection | 23 | [C12](C12-Privacy.md) | Single | 2026-03-22 |
| C13 | Monitoring, Logging & Anomaly Detection | 47 | [C13](C13-Monitoring-and-Logging.md) | [8 sections](#c13-monitoring-logging--anomaly-detection) | 2026-03-22 |
| C14 | Human Oversight & Accountability | 25 | [C14](C14-Human-Oversight.md) | Single | 2026-03-22 |
| | **Total** | **450** | **82 pages** | | |

---

### C2: User Input Validation

Covers prompt injection defense, adversarial input resistance, schema validation, content screening, rate limiting, multi-modal input handling, and adaptive threat detection.

| Section | Page |
|---------|------|
| C2.1 Prompt Injection Defense | [C02-01](C02-01-Prompt-Injection-Defense.md) |
| C2.2 Adversarial-Example Resistance | [C02-02](C02-02-Adversarial-Example-Resistance.md) |
| C2.3 Prompt Character Set | [C02-03](C02-03-Prompt-Character-Set.md) |
| C2.4 Schema, Type & Length Validation | [C02-04](C02-04-Schema-Type-Length-Validation.md) |
| C2.5 Content & Policy Screening | [C02-05](C02-05-Content-Policy-Screening.md) |
| C2.6 Input Rate Limiting & Abuse Prevention | [C02-06](C02-06-Input-Rate-Limiting-Abuse-Prevention.md) |
| C2.7 Multi-Modal Input Validation | [C02-07](C02-07-Multi-Modal-Input-Validation.md) |
| C2.8 Real-Time Adaptive Threat Detection | [C02-08](C02-08-Real-Time-Adaptive-Threat-Detection.md) |

### C4: Infrastructure & Deployment Security

Addresses runtime isolation, secure build pipelines, network controls, secrets management, workload sandboxing, resource management, hardware security, and edge deployment.

| Section | Page |
|---------|------|
| C4.1 Runtime Environment Isolation | [C04-01](C04-01-Runtime-Environment-Isolation.md) |
| C4.2 Secure Build & Deployment | [C04-02](C04-02-Secure-Build-Deployment.md) |
| C4.3 Network Security & Access Control | [C04-03](C04-03-Network-Security-Access-Control.md) |
| C4.4 Secrets & Key Management | [C04-04](C04-04-Secrets-Key-Management.md) |
| C4.5 Workload Sandboxing & Validation | [C04-05](C04-05-Workload-Sandboxing-Validation.md) |
| C4.6 Resource Management, Backup & Recovery | [C04-06](C04-06-Resource-Management-Backup-Recovery.md) |
| C4.7 Hardware Security | [C04-07](C04-07-Hardware-Security.md) |
| C4.8 Edge & Distributed Security | [C04-08](C04-08-Edge-Distributed-Security.md) |

### C6: Supply Chain Security

Covers vetting pretrained models, scanning frameworks and libraries, pinning dependencies, enforcing trusted sources, managing third-party dataset risk, monitoring for supply chain attacks, and maintaining AI bills of materials.

| Section | Page |
|---------|------|
| C6.1 Pretrained Model Vetting | [C06-01](C06-01-Pretrained-Model-Vetting.md) |
| C6.2 Framework & Library Scanning | [C06-02](C06-02-Framework-Library-Scanning.md) |
| C6.3 Dependency Pinning & Verification | [C06-03](C06-03-Dependency-Pinning-Verification.md) |
| C6.4 Trusted Source Enforcement | [C06-04](C06-04-Trusted-Source-Enforcement.md) |
| C6.5 Third-Party Dataset Risk | [C06-05](C06-05-Third-Party-Dataset-Risk.md) |
| C6.6 Supply Chain Attack Monitoring | [C06-06](C06-06-Supply-Chain-Attack-Monitoring.md) |
| C6.7 AI BOM for Model Artifacts | [C06-07](C06-07-AI-BOM-Model-Artifacts.md) |

### C7: Model Behavior & Output Control

Addresses output format enforcement, hallucination detection, safety and privacy filtering, output limiting, explainability, monitoring integration, generative media safeguards, and source attribution.

| Section | Page |
|---------|------|
| C7.1 Output Format Enforcement | [C07-01](C07-01-Output-Format-Enforcement.md) |
| C7.2 Hallucination Detection | [C07-02](C07-02-Hallucination-Detection.md) |
| C7.3 Output Safety & Privacy Filtering | [C07-03](C07-03-Output-Safety-Privacy-Filtering.md) |
| C7.4 Output & Action Limiting | [C07-04](C07-04-Output-Action-Limiting.md) |
| C7.5 Explainability & Transparency | [C07-05](C07-05-Explainability-Transparency.md) |
| C7.6 Monitoring Integration | [C07-06](C07-06-Monitoring-Integration.md) |
| C7.7 Generative Media Safeguards | [C07-07](C07-07-Generative-Media-Safeguards.md) |
| C7.8 Source Attribution & Citation Integrity | [C07-08](C07-08-Source-Attribution-Citation-Integrity.md) |

### C9: Orchestration & Agentic Action Security

Covers execution budgets, human-in-the-loop approval for high-impact actions, tool and plugin isolation, agent identity and audit trails, secure inter-agent messaging, authorization delegation, intent verification, and multi-agent isolation.

| Section | Page |
|---------|------|
| C9.1 Execution Budgets | [C09-01](C09-01-Execution-Budgets.md) |
| C9.2 High-Impact Action Approval | [C09-02](C09-02-High-Impact-Action-Approval.md) |
| C9.3 Tool and Plugin Isolation | [C09-03](C09-03-Tool-and-Plugin-Isolation.md) |
| C9.4 Agent Identity and Audit | [C09-04](C09-04-Agent-Identity-and-Audit.md) |
| C9.5 Secure Messaging | [C09-05](C09-05-Secure-Messaging.md) |
| C9.6 Authorization and Delegation | [C09-06](C09-06-Authorization-and-Delegation.md) |
| C9.7 Intent Verification | [C09-07](C09-07-Intent-Verification.md) |
| C9.8 Multi-Agent Isolation | [C09-08](C09-08-Multi-Agent-Isolation.md) |

### C10: MCP Security

Addresses security for Model Context Protocol deployments, including component integrity, authentication, transport security, schema validation, outbound access controls, and boundary enforcement.

| Section | Page |
|---------|------|
| C10.1 Component Integrity | [C10-01](C10-01-Component-Integrity.md) |
| C10.2 Authentication & Authorization | [C10-02](C10-02-Authentication-Authorization.md) |
| C10.3 Secure Transport | [C10-03](C10-03-Secure-Transport.md) |
| C10.4 Schema & Message Validation | [C10-04](C10-04-Schema-Message-Validation.md) |
| C10.5 Outbound Access & Agent Safety | [C10-05](C10-05-Outbound-Access-Agent-Safety.md) |
| C10.6 Transport Restrictions & Boundary Controls | [C10-06](C10-06-Transport-Restrictions-Boundary-Controls.md) |

### C11: Adversarial Robustness

Covers model alignment, adversarial example hardening, membership inference and model inversion resistance, model extraction defense, poisoned data detection, security policy adaptation, agent self-assessment, autonomous update security, and adversarial bias exploitation defense.

| Section | Page |
|---------|------|
| C11.1 Model Alignment & Safety | [C11-01](C11-01-Model-Alignment-Safety.md) |
| C11.2 Adversarial-Example Hardening | [C11-02](C11-02-Adversarial-Example-Hardening.md) |
| C11.3 Membership-Inference Mitigation | [C11-03](C11-03-Membership-Inference-Mitigation.md) |
| C11.4 Model-Inversion Resistance | [C11-04](C11-04-Model-Inversion-Resistance.md) |
| C11.5 Model-Extraction Defense | [C11-05](C11-05-Model-Extraction-Defense.md) |
| C11.6 Inference-Time Poisoned-Data Detection | [C11-06](C11-06-Inference-Time-Poisoned-Data-Detection.md) |
| C11.7 Security Policy Adaptation | [C11-07](C11-07-Security-Policy-Adaptation.md) |
| C11.8 Agent Security Self-Assessment | [C11-08](C11-08-Agent-Security-Self-Assessment.md) |
| C11.9 Self-Modification & Autonomous Update Security | [C11-09](C11-09-Self-Modification-Autonomous-Update-Security.md) |
| C11.10 Adversarial Bias Exploitation Defense | [C11-10](C11-10-Adversarial-Bias-Exploitation-Defense.md) |

### C13: Monitoring, Logging & Anomaly Detection

Covers request and response logging, abuse detection, model drift detection, performance telemetry, incident response, performance degradation detection, workflow visualization, and proactive security monitoring.

| Section | Page |
|---------|------|
| C13.1 Request & Response Logging | [C13-01](C13-01-Request-Response-Logging.md) |
| C13.2 Abuse Detection & Alerting | [C13-02](C13-02-Abuse-Detection-Alerting.md) |
| C13.3 Model Drift Detection | [C13-03](C13-03-Model-Drift-Detection.md) |
| C13.4 Performance & Behavior Telemetry | [C13-04](C13-04-Performance-Behavior-Telemetry.md) |
| C13.5 Incident Response | [C13-05](C13-05-Incident-Response.md) |
| C13.6 Performance Degradation Detection | [C13-06](C13-06-Performance-Degradation-Detection.md) |
| C13.7 DAG Visualization & Workflow Security | [C13-07](C13-07-DAG-Visualization-Workflow-Security.md) |
| C13.8 Proactive Security Behavior Monitoring | [C13-08](C13-08-Proactive-Security-Behavior-Monitoring.md) |

---

## Appendices

The appendices provide supporting material including a glossary of AI security terms, a curated reference list, requirements for AI-assisted secure coding, and an inventory of security controls mapped to the standard.

| Appendix | Page | Updated |
|----------|------|:-------:|
| A: Glossary | [Appendix A Glossary](Appendix-A-Glossary.md) | 2026-03-21 |
| B: References | [Appendix B References](Appendix-B-References.md) | 2026-03-21 |
| C: AI-Assisted Secure Coding (27 reqs) | [Appendix C AI Secure Coding](Appendix-C-AI-Secure-Coding.md) | 2026-03-22 |
| D: AI Security Controls Inventory | [Appendix D Controls Inventory](Appendix-D-Controls-Inventory.md) | 2026-03-21 |

---

## Page Structure

Every wiki page follows a consistent format to make research easy to navigate. Each requirement has a research table with the following columns:

| Column | Purpose |
|--------|---------|
| **Requirement** | Full text from the AISVS standard |
| **Level** | Verification level (1, 2, or 3) |
| **Role** | Developer (D), Verifier (V), or both (D/V) |
| **Threat Mitigated** | Specific attack technique, failure mode, or risk |
| **Verification Approach** | Concrete audit steps, tools, and checks |
| **Gaps / Notes** | Tooling maturity, open issues, implementation caveats |

Beyond the requirement tables, pages include threat landscape summaries, notable real-world incidents, tooling recommendations with implementation maturity ratings, open research questions, references to related standards, and cross-chapter links to related requirements.

---

## Contributing

This wiki is maintained alongside the [AISVS repository](https://github.com/OWASP/AISVS). If you spot inaccuracies, know of relevant tooling or research, or want to improve the coverage of any section, contributions are welcome. Open an issue or submit a pull request to get involved.
