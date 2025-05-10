# OWASP Artificial Intelligence Security Verification Standard (AISVS)
### Core Category List - Work In Progress

---

## 1. Training Data Governance & Bias Management
This section provides requirements to ensure training data is ethical, secure, and compliant by managing its provenance, quality, and bias during data collection and preparation for model training.

| Focus area | Purpose |
| --- | --- |
| **Training Data Provenance** | Track and audit origins of training datasets to ensure traceability and detect unauthorized or unverified sources. |
| **Bias Detection & Correction** | Identify and mitigate demographic or distributional biases in training data to promote equitable model outcomes. |
| **Representation Completeness & Fairness** | Ensure training data includes balanced coverage of under-represented groups and edge cases through targeted collection or augmentation to enhance model robustness. |
| **Training Data Integrity & Labeling** | Safeguard training datasets and labels from tampering or poisoning using cryptographic integrity, secure annotation pipelines and other methods to maintain data quality. |
| **Training Data Quality Assurance** | Validate training data for accuracy, completeness, and consistency to ensure reliable model training. |
| **Data Poisoning Detection** | Detect and filter malicious or corrupted data in training datasets using anomaly detection or statistical analysis to prevent model corruption. |
| **User Data Deletion & Consent Enforcement** | Implement mechanisms to honor user deletion requests and consent withdrawals in training datasets and backups, compliant with privacy law. |
| **Regulatory Compliance Management** | Align training data practices with privacy laws and AI regulations by documenting consent, purpose, and retention policies. |
| **Model Data Labeling** | To prevent data poisoning, ensure label integrity, protect sensitive information, maintain accountability, defend against inference attacks, and comply with regulatory standards. |

---

## 2. User Input Validation
This section outlines defenses against user input attacks, ensuring all runtime inputs (e.g., interactive prompts, API requests, or streaming feeds) are well-formed, policy-compliant, and free from malicious or adversarial content, such as prompt injection. This section focuses solely on securing user inputs during model inference.

| Focus area | Purpose |
| --- | --- |
| **Prompt-Injection Defense** | Detect & block attempts to override instructions or jailbreak guardrails |
| **Adversarial-Example Resistance** | Detect & block perturbed inputs to mislead model during inference |
| **Schema, Type & Length Validation** | Enforce strict syntactic, semantic, & size constraints on user inputs |
| **Content & Policy Screening** | Apply filters to ensure compliance with safety policies |

---

## 3. Model Lifecycle Management & Change Control
This section provides requirements to manage model development, fine-tuning, and maintenance securely, ensuring all changes are versioned, traceable, and reversible.

| Focus area | Purpose |
| --- | --- |
| **Model versioning & transparency** | Track model releases with cryptographic signing, dependency graphs, and SBOMs to ensure integrity and transparency. |
| **Secure patching & rollback** | Enable hotfixes and downgrades with validated rollback mechanisms to maintain security and functionality without vulnerabilities. |
| **Controlled fine-tuning & retraining** | Restrict data ingestion, hyperparameter changes, and pipeline configurations to approved workflows. |
| **Change auditing** | Log and review all modifications, including prompt templates and system messages, to ensure traceability and accountability. |
| **Model testing & validation** | Conduct performance, robustness, and security tests before deployment to verify model reliability and compliance. |
| **Model change documentation** | Maintain changelogs and model cards to document updates, configurations, and dependencies for compliance and auditing. |
| **Formal decommissioning process** | Define steps for archiving, sanitizing, and revoking retired models to prevent unauthorized reuse or data leakage. |
| **Model Provenance Tracking** | Capturing, recording, and storing information about a model's origin, how it was created, and its history of modifications. |

---

## 4. Infrastructure, Configuration & Deployment Security
This section provides requirements to secure build, deployment, and runtime environments for AI systems, protecting against exploitation, misconfiguration, and lateral movement.

| Focus area | Purpose |
| --- | --- |
| **Container & serverless runtime isolation** | Enforce least privilege using Kubernetes namespaces, seccomp profiles, and eBPF rules to prevent privilege escalation. |
| **Secure deployment pipelines** | Implement IaC scanning, reproducible builds, and policy gates to ensure trusted deployments. |
| **Attack surface reduction** | Restrict default ports, disable unused endpoints, and limit egress traffic to minimize external attack vectors. |
| **Secrets management & environment hardening** | Rotate API keys, use TPM/HSM for key storage, and audit environment variables to prevent unauthorized access. |
| **Model sandboxing** | Isolate model evaluation in sandboxed environments to detect vulnerabilities or malicious behavior. |
| **Infrastructure vulnerability monitoring** | Scan containers and hosts for CVEs and misconfigurations. |

---

## 5. Access Control & Identity for AI Components & Users
This section provides requirements to enforce context-aware, least-privilege access for users, services, and agents interacting with AI models, data, and outputs during deployment and runtime.

| Focus area | Purpose |
| --- | --- |
| **Identity proofing & federation** | Establish and verify principal identity; integrate with enterprise IdP and support progressive trust elevation (MFA, step‑up). |
| **User & data access mapping** | Bind personas/roles to fine‑grained permissions on endpoints, collections, embeddings, and vector indices. |
| **Attribute‑Based Access Control (ABAC) service layer** | Externalize policy decisions (e.g., OPA, Cedar) that evaluate dynamic attributes—user, resource tags, environmental context—at query time, independent of application code. |
| **Query‑time policy evaluation** | Before retrieval, filter search vectors / SQL rows so only objects the caller is entitled to ever leave storage. |
| **Output filtering & redaction** | After model inference or search, enforce least‑privilege by redacting, transforming, or refusing content so that all generated text, images, embeddings, and citations respect the caller’s entitlements. |
| **Tenant & session isolation** | Segregate memory, embeddings, and cache per tenant; verify session context on every request to prevent cross‑customer data bleed in multi‑tenant SaaS. |
| **Agent & tool permission scoping** | Constrain autonomous agents, plugins, or tool calls to explicit capability sets (e.g., read‑only S3, no shell access), enforced by the ABAC layer.    

---

## 6. Supply Chain Security for Models, Frameworks & Data
This section provides requirements to secure upstream artifacts (pretrained models, ML frameworks, libraries, and datasets) against tampering, vulnerabilities, and licensing risks to ensure integrity and trustworthiness.

| Focus area | Purpose |
| --- | --- |
| **Pretrained model vetting & provenance** | Verify model sources, integrity, and metadata using frameworks that detect embedded malicious payloads or backdoors. |
| **Framework & library scanning** | Continuously assess dependencies for CVEs. |
| **Dependency pinning & verification** | Enforce SBOMs, hermetic builds, and cryptographic attestations to prevent unauthorized or tampered dependencies. |
| **Trusted source enforcement** | Restrict artifact downloads to signed registries or private repositories, blocking unverified mirrors or public sources. |
| **Third-party dataset risk assessment** | Evaluate external datasets for bias, legal issues, or poisoning risks, ensuring alignment with ethical and regulatory standards. |
| **Supply chain attack monitoring** | Monitor for compromised repositories or malicious updates. |
| **Licensing compliance** | Validate compliance with model and dataset licenses to mitigate legal and ethical risks. |
| **SBOM (Software Bill of Materials) for model artifacts**| Detailed inventory of all components, dependencies, and metadata used in building and deploying machine learning models to enhance transparency, traceability, and security. |

---

## 7. Model Behavior, Output Control & Safety Assurance
This section provides requirements to ensure model outputs are accurate, safe, and policy-compliant during runtime, to control and mitigate risks in generated content.

| Focus area | Purpose |
| --- | --- |
| **Output format enforcement** | Enforce constraints on response schemas, data types, or token limits to ensure structured and predictable outputs. |
| **Hallucination detection & mitigation** | Detect low-confidence or fabricated outputs and apply fallback strategies to maintain response reliability. |
| **Output safety & privacy filtering** | Block harmful content, PII, or confidential data in outputs using pre- and post-generation policy checks. |
| **Output & action limiting** | Restrict model-initiated actions and response rates through throttling or approval requirements to prevent abuse or overload. |
| **Output explainability** | Provide transparency in outputs through confidence scores or reasoning traces to enhance user trust. |
| **Monitoring integration** | Feed output safety and quality metrics into monitoring systems to enable real-time risk detection and response. |

---

## 8. Memory, Embeddings & Vector Database Security
This section provides requirements to secure AI memory and retrieval-augmented generation (RAG) stores during runtime, protecting against inversion, leakage, and unauthorized reuse.

| Focus area | Purpose |
| --- | --- |
| **Access controls on memory & RAG indices** | Apply row‑level, namespace, or ABAC controls to stored vectors. |
| **Embedding sanitization & validation** | Remove PII or malicious artifacts before vectorization. |
| **Memory expiry, revocation & deletion** | Honor TTLs, user deletion requests, and dynamic scope reductions. |
| **Prevent embedding inversion or leakage** | Employ noise addition, dimensionality reduction, and encryption schemes. |
| **Scope enforcement for user‑specific memory** | Ensure one user’s context cannot seed completions for another. |

---

## 9. Autonomous Orchestration & Agentic Action Security  
**Goal:** Secure the glue code—agents, planners, tool delegates—that chains model calls into complex workflows, often with real‑world impact.

| Focus area | Purpose |
| --- | --- |
| **Agent task planning & re‑entrancy control** | Throttle recursive plans and require human checkpoints for privileged actions. |
| **Tool plugin sandboxing** | Isolate third‑party functions with syscall, network, and filesystem jails. |
| **Autonomous loop bounding** | Enforce max iterations, cost quotas, or resource ceilings. |
| **Protocol‑level misuse protection** | Validate structured messages (e.g., function‑call JSON) against schemas. |
| **Multi‑agent swarm risk reduction** | Detect collusion, echo‑chambers, or emergent unsafe behavior across agents. |
| **User & Tool Authn/Authz** | Ensure any agent is operating in the correct permissioning paradigm, assuming permissions for a user it is operating on behalf of, or controlling tool calls with traditional authn/authz methods. |

---

## 10. Adversarial Robustness & Attack Resistance
**Goal:** Design models that degrade gracefully—or fail closed—when confronted with sophisticated attacks targeting the learning process or inference surface.

| Focus area | Purpose |
| --- | --- |
| **Adversarial example hardening** | Employ defensive distillation, randomized smoothing, or certified bounds. |
| **Membership inference mitigation** | Reduce confidence gaps and add noise to protect training inclusion privacy. |
| **Model inversion resistance** | Limit exposure of embeddings, logits, or internal attention maps. |
| **Model extraction defense** | Rate‑limit queries, watermark outputs, and detect anomalous scraping. |
| **Poisoned data detection** | At inference time, Use clustering, entropy, and trigger search to flag back‑doored samples. |
| **Regular Red Team Simulation** | Proactively identify and address security weaknesses by emulating real-world attacker behaviors in a controlled environment. |

---

## 11. Privacy Protection & Personal Data Management
**Goal:** Uphold individual rights and minimize the collection, retention, and exposure of personal data at every phase of the AI pipeline.

| Focus area | Purpose |
| --- | --- |
| **Anonymization & data minimization** | Strip or hash identifiers; collect only what is strictly necessary. |
| **Right‑to‑be‑forgotten & deletion enforcement** | Propagate erasure across checkpoints, embeddings, and backups. |
| **Differential privacy** | Apply noise or clipping during training and query time. |
| **Purpose limitation & scope‑creep protection** | Detect secondary uses that diverge from original consent. |
| **Consent management & documentation** | Track lawful bases, opt‑in status, and data‑subject agreements. |
| **Federated learning with privacy controls** | Offers privacy advantages by training models on distributed devices without sharing raw data. |

---

## 12. Monitoring, Logging & Anomaly Detection
**Goal:** Provide real‑time and forensic visibility into what the model sees, does, and returns—so threats can be detected, triaged, and learned from.

| Focus area | Purpose |
| --- | --- |
| **Prompt & output logging** | Capture inputs, outputs, and policy decisions with privacy‑preserving redaction. |
| **Abuse & jailbreak detection** | Alert when queries resemble known jailbreak patterns or circumvent safeguards. |
| **Model drift detection** | Track  novelty, confidence, hallucinations, and divergence metrics across versions. |
| **Performance & behavior telemetry** | Instrument latency, token counts, resource utilization, and success rates. |
| **Alerting & SIEM integration** | Export enriched events for SOC correlation and incident response. |
| **Secure log storage** | To track and identify any potential security issues, investigations and audits. |

---

## 13. Human Oversight, Accountability & Governance
**Goal:** Keep a human “captain of the ship” with clear lines of responsibility, escalation, and ethical stewardship.

| Focus area | Purpose |
| --- | --- |
| **Kill‑switch & override mechanisms** | Provide immediate shutdown or rollback paths for runaway behavior. |
| **Human‑in‑the‑loop decision checkpoints** | Require approvals when stakes surpass predefined risk thresholds. |
| **Operational governance documentation** | Maintain SOPs, playbooks, and RACI matrices for AI operations. |
| **Chain of responsibility & auditability** | Log operator actions and model decisions for postmortem reviews. |

---

## 14. Explainability, Interpretability & Transparency
**Goal:** Make model reasoning and limitations legible to developers, auditors, and end‑users—building trust and diagnosability.

| Focus area | Purpose |
| --- | --- |
| **Explainable‑AI techniques (SHAP, LIME, etc.)** | Surface feature importance, counter‑factuals, and local explanations. |
| **Model cards & usage disclosures** | Document intended use, performance metrics, and ethical considerations. |
| **Uncertainty quantification** | Propagate confidence scores or entropy measures in responses. |
| **User‑facing transparency reports** | Provide periodic disclosures on incidents, drift, and data usage. |

---

### Next steps for reviewers

1. **Scope accuracy** – Does each category cover the right threat surfaces?  
2. **Clarity & granularity** – Are the descriptions and bullets detailed enough to drive concrete requirements?  
3. **Overlap & gaps** – Where can we consolidate or expand?  
4. **Terminology** – Any jargon needing definitions or refinement?

Please leave inline comments, propose rewrites, or suggest additional focus areas. Your feedback will shape the next iteration of AISVS!
