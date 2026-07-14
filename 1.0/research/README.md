# AISVS Research Wiki

**OWASP AI Security Verification Standard: Research and Analysis Hub**

Welcome to the AISVS research wiki. This wiki provides structured research context for every chapter and appendix in AISVS 1.0, helping developers, auditors, and security teams understand and implement each requirement. Every requirement is mapped to the threats it mitigates, the tools and techniques available to implement it, practical verification approaches, and open questions where tooling or research is still maturing. Whether you are building an AI application, auditing one, or evaluating your organization's AI security posture, this wiki is designed to help you get started.

---

## Chapters

The standard is organized into 12 chapters spanning the full AI application security lifecycle, from training data through deployment, monitoring, and human oversight. Every chapter has per-section sub-pages for focused navigation, plus a hub page with cross-cutting threat landscape, tooling, and research context.

| # | Chapter | Reqs | Pages | Type | Updated |
|---|---------|:----:|:-----:|------|:-------:|
| C1 | Training Data Integrity & Traceability | 13 | [C01](chapters/C01-Training-Data/C01-Training-Data.md) | [3 sections](#c1-training-data-integrity-traceability) | 2026-07-13 |
| C2 | Input Validation | 12 | [C02](chapters/C02-User-Input-Validation/C02-User-Input-Validation.md) | [2 sections](#c2-input-validation) | 2026-07-13 |
| C3 | Model Lifecycle Management & Change Control | 15 | [C03](chapters/C03-Model-Lifecycle-Management/C03-Model-Lifecycle-Management.md) | [5 sections](#c3-model-lifecycle-management-change-control) | 2026-07-13 |
| C4 | Infrastructure, Configuration & Deployment Security | 14 | [C04](chapters/C04-Infrastructure/C04-Infrastructure.md) | [3 sections](#c4-infrastructure-configuration-deployment-security) | 2026-07-13 |
| C5 | Access Control & Identity for AI Components & Users | 11 | [C05](chapters/C05-Access-Control/C05-Access-Control.md) | [3 sections](#c5-access-control-identity-for-ai-components-users) | 2026-07-13 |
| C6 | Supply Chain Security for Models | 7 | [C06](chapters/C06-Supply-Chain/C06-Supply-Chain.md) | [2 sections](#c6-supply-chain-security-for-models) | 2026-07-13 |
| C7 | Model Behavior, Output Control & Safety Assurance | 13 | [C07](chapters/C07-Model-Behavior/C07-Model-Behavior.md) | [4 sections](#c7-model-behavior-output-control-safety-assurance) | 2026-07-13 |
| C8 | Memory, Embeddings & Vector Database Security | 11 | [C08](chapters/C08-Memory-and-Embeddings/C08-Memory-and-Embeddings.md) | [3 sections](#c8-memory-embeddings-vector-database-security) | 2026-07-13 |
| C9 | Orchestration & Agentic Security | 34 | [C09](chapters/C09-Orchestration-and-Agents/C09-Orchestration-and-Agents.md) | [6 sections](#c9-orchestration-agentic-security) | 2026-07-13 |
| C10 | Model Context Protocol (MCP) Security | 23 | [C10](chapters/C10-MCP-Security/C10-MCP-Security.md) | [4 sections](#c10-model-context-protocol-mcp-security) | 2026-07-13 |
| C11 | Adversarial Robustness & Attack Resistance | 17 | [C11](chapters/C11-Adversarial-Robustness/C11-Adversarial-Robustness.md) | [4 sections](#c11-adversarial-robustness-attack-resistance) | 2026-07-12 |
| C12 | Monitoring, Logging & Anomaly Detection | 21 | [C12](chapters/C12-Monitoring-and-Logging/C12-Monitoring-and-Logging.md) | [5 sections](#c12-monitoring-logging-anomaly-detection) | 2026-07-12 |
| | **Total** | **191** | **59 pages** | | |

---

### C1: Training Data Integrity & Traceability

Covers training data origin and traceability, data security and integrity, labeling and annotation security, quality assurance, and data lineage.

| Section | Page |
|---------|------|
| C1.1 Training Data Origin & Data Security | [C01-01](chapters/C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md) |
| C1.2 Data Labeling and Annotation Security | [C01-02](chapters/C01-Training-Data/C01-02-Data-Labeling-Annotation-Security.md) |
| C1.3 Training Data Quality and Security Assurance | [C01-03](chapters/C01-Training-Data/C01-03-Training-Data-Quality-Security-Assurance.md) |


### C2: Input Validation

Covers prompt injection defense, pre-tokenization normalization, content and policy screening, and multi-modal input validation.

| Section | Page |
|---------|------|
| C2.1 Prompt Injection Defenses | [C02-01](chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) |
| C2.2 Content & Policy Screening | [C02-02](chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md) |


### C3: Model Lifecycle Management & Change Control

Covers model authorization and integrity, validation and testing, controlled deployment and rollback, secure development practices, hosted/provider-managed controls, and fine-tuning pipeline authorization.

| Section | Page |
|---------|------|
| C3.1 Model Authorization & Integrity | [C03-01](chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md) |
| C3.2 Model Validation & Testing | [C03-02](chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md) |
| C3.3 Controlled Deployment & Rollback | [C03-03](chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md) |
| C3.4 Secure Development Practices | [C03-04](chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md) |
| C3.5 Pipeline Fine-Tuning | [C03-05](chapters/C03-Model-Lifecycle-Management/C03-05-Pipeline-Fine-Tuning.md) |


### C4: Infrastructure, Configuration & Deployment Security

Covers AI-specific workload sandboxing and confidential computing, AI accelerator hardware security, and edge or distributed AI deployment security.

| Section | Page |
|---------|------|
| C4.1 AI Workload Sandboxing & Validation | [C04-01](chapters/C04-Infrastructure/C04-01-Workload-Sandboxing-Validation.md) |
| C4.2 AI Hardware Security | [C04-02](chapters/C04-Infrastructure/C04-02-Hardware-Security.md) |
| C4.3 Edge & Distributed AI Security | [C04-03](chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md) |


### C5: Access Control & Identity for AI Components & Users

Covers AI-specific authentication, resource authorization and classification, query-time authorization, output entitlement enforcement, policy decision point isolation, and multi-tenant isolation.

| Section | Page |
|---------|------|
| C5.1 Authentication | [C05-01](chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md) |
| C5.2 AI Resource Authorization & Classification | [C05-02](chapters/C05-Access-Control/C05-02-AI-Resource-Authorization-Classification.md) |
| C5.3 Multi-Tenant Isolation | [C05-03](chapters/C05-Access-Control/C05-03-Multi-Tenant-Isolation.md) |


### C6: Supply Chain Security for Models

Covers model artifact scanning, approved-source enforcement, integrity verification, behavioral acceptance testing, and signed AI bills of materials.

| Section | Page |
|---------|------|
| C6.1 Model Artifact Integrity | [C06-01](chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md) |
| C6.2 AI BOM & Supply Chain Monitoring | [C06-02](chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md) |


### C7: Model Behavior, Output Control & Safety Assurance

Covers output format enforcement, hallucination detection, output safety and privacy filtering, explainability, generative media safeguards, and source attribution.

| Section | Page |
|---------|------|
| C7.1 Output Format Enforcement | [C07-01](chapters/C07-Model-Behavior/C07-01-Output-Format-Enforcement.md) |
| C7.2 Hallucination Detection & Mitigation | [C07-02](chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md) |
| C7.3 Output Safety | [C07-03](chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md) |
| C7.4 Source Attribution & Citation Integrity | [C07-04](chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md) |


### C8: Memory, Embeddings & Vector Database Security

Covers vector identifier and namespace isolation, retrieval scope enforcement, embedding sanitization and quarantine, source validation for agent/tool memory writes, contradiction checks, expiry, reset, and quarantine exclusion.

| Section | Page |
|---------|------|
| C8.1 Access Controls on Memory & RAG Indices | [C08-01](chapters/C08-Memory-and-Embeddings/C08-01-Access-Controls-Memory-RAG.md) |
| C8.2 Embedding Sanitization & Validation | [C08-02](chapters/C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md) |
| C8.3 Memory Expiry & Revocation | [C08-03](chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md) |


### C9: Orchestration & Agentic Security

Covers execution budgets, approval gates for high-impact actions, component isolation, agent and orchestrator identity, authorization and delegation, and shutdown or graceful degradation for autonomous and multi-agent systems.

| Section | Page |
|---------|------|
| C9.1 Execution Budgets, Loop Control, and Circuit Breakers | [C09-01](chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md) |
| C9.2 High-Impact Action Approval and Irreversibility Controls | [C09-02](chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md) |
| C9.3 Component Isolation and Tool Authorization | [C09-03](chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md) |
| C9.4 Agent and Orchestrator Identity | [C09-04](chapters/C09-Orchestration-and-Agents/C09-04-Agent-Identity-and-Audit.md) |
| C9.5 Agent Authorization, Delegation, and Continuous Enforcement | [C09-05](chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md) |
| C9.6 Shutdown and Graceful Degradation | [C09-06](chapters/C09-Orchestration-and-Agents/C09-06-Shutdown-Graceful-Degradation.md) |


### C10: Model Context Protocol (MCP) Security

Covers MCP component integrity, authentication and authorization, transport security, schema and message validation, outbound access controls, and high-risk boundary restrictions.

| Section | Page |
|---------|------|
| C10.1 Component Integrity | [C10-01](chapters/C10-MCP-Security/C10-01-Component-Integrity.md) |
| C10.2 Authentication & Authorization | [C10-02](chapters/C10-MCP-Security/C10-02-Authentication-Authorization.md) |
| C10.3 Secure Transport | [C10-03](chapters/C10-MCP-Security/C10-03-Secure-Transport.md) |
| C10.4 Schema, Message, and Input Validation | [C10-04](chapters/C10-MCP-Security/C10-04-Schema-Message-Validation.md) |


### C11: Adversarial Robustness & Attack Resistance

Covers model alignment, adversarial-example hardening, membership inference and model inversion resistance, model extraction defense, runtime context contamination detection, security policy adaptation, agent self-assessment, autonomous update security, and adversarial bias exploitation defense.

| Section | Page |
|---------|------|
| C11.1 Model Alignment, Safety, and Robustness Testing and Training | [C11-01](chapters/C11-Adversarial-Robustness/C11-01-Model-Alignment-Safety.md) |
| C11.2 Membership-Inference and Model-Inversion Mitigation | [C11-02](chapters/C11-Adversarial-Robustness/C11-02-Membership-Inference-Model-Inversion-Mitigation.md) |
| C11.3 Model-Extraction Defense | [C11-03](chapters/C11-Adversarial-Robustness/C11-03-Model-Extraction-Defense.md) |
| C11.4 Model Runtime Anomaly Detection | [C11-04](chapters/C11-Adversarial-Robustness/C11-04-Model-Runtime-Anomaly-Detection.md) |


### C12: Monitoring, Logging & Anomaly Detection

Covers request and response logging, abuse detection, model and data drift detection, performance telemetry, AI incident response, proactive security behavior monitoring, and training-data and model-lifecycle audit.

| Section | Page |
|---------|------|
| C12.1 Request & Response Logging | [C12-01](chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md) |
| C12.2 Detection and Alerting | [C12-02](chapters/C12-Monitoring-and-Logging/C12-02-Abuse-Detection-Alerting.md) |
| C12.3 Model, Data, and Performance Drift Detection | [C12-03](chapters/C12-Monitoring-and-Logging/C12-03-Model-Drift-Detection.md) |
| C12.4 Proactive Security Behavior Monitoring | [C12-04](chapters/C12-Monitoring-and-Logging/C12-04-Proactive-Security-Behavior-Monitoring.md) |
| C12.5 Training Data & Model Lifecycle Audit | [C12-05](chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md) |


## Appendices

The appendices provide supporting material including a glossary of AI security terms, an inventory of security controls mapped to the standard, and requirements for AI-assisted secure coding.

| Appendix | Page | Updated |
|----------|------|:-------:|
| A: Glossary | [Appendix A Glossary](appendices/Appendix-A-Glossary.md) | 2026-07-12 |
| B: AI Security Controls Inventory | [Appendix B Controls Inventory](appendices/Appendix-B-Controls-Inventory.md) | 2026-07-12 |
| C: AI-Assisted Secure Coding (68 reqs) | [Appendix C AI Secure Coding](appendices/Appendix-C-AI-Secure-Coding.md) | 2026-07-13 |

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
