# Appendix D: AI Security Controls Inventory

## Objective

This appendix provides a concise inventory of every security control and defense technique referenced across the AISVS requirements. Controls are grouped by security control category so that implementers can find all related defenses in one place regardless of which AISVS chapter defines them.

---

## AD.1 Authentication

Verify the identity of users, agents, services, MCP clients/servers, and edge devices before granting access.

| Control / Technique | Requirement IDs |
| --- | --- |
| Step-up authentication for high-risk AI operations (model deployment, weight export, training data access) | 5.1.1 |
| Short-lived signed tokens for federated AI agent authentication | 5.1.2 |
| Unique cryptographic agent and orchestrator identity | 9.4.1 |
| First-class principal authentication (no end-user credential reuse) | 9.4.1 |
| Agent identity credential rotation and rapid revocation | 9.4.5 |
| OAuth 2.1 for MCP client authentication | 10.2.1 |
| MCP server OAuth token validation (issuer, audience, expiration, scope) | 10.2.2 |
| MCP server registration with explicit ownership | 10.2.4 |
| Cryptographically secure MCP session IDs (not used for auth) | 10.2.8 |

**Common pitfalls:** reusing end-user credentials for agent-to-agent calls; using MCP session IDs as authentication tokens; not rotating agent credentials on suspected compromise.

---

## AD.2 Authorization & Access Control

Enforce access decisions across users, agents, tools, data, and MCP resources using policy-based controls.

| Control / Technique | Requirement IDs |
| --- | --- |
| Access controls on AI resources (datasets, models, endpoints, vector collections, compute) | 5.2.1 |
| Just-in-time privileged access for AI resources (model weights, training pipelines) | 5.2.2 |
| AI-specific data classification taxonomy | 5.2.3 |
| Classification label propagation to derived AI resources (embeddings, caches, outputs) | 5.2.4 |
| Caller authorization context enforcement through AI query pipelines | 5.3.1 |
| Fine-grained agent action authorization (tool, parameters, resources, data scope) | 9.6.1 |
| Delegation context propagation with integrity protection (user, tenant, scopes) | 9.6.2 |
| Application-layer policy enforcement (model output cannot bypass) | 9.6.3 |
| Pre-execution policy constraint gates (deny rules, allow-lists, budgets) | 9.7.1 |
| Scope-filtered MCP tool discovery (tools/list) | 10.2.8 |
| Per-tool MCP invocation access control (argument, token scope) | 10.2.9 |
| MCP policy enforcement that model output cannot bypass | 10.2.7 |
| Authorization-aware post-inference filtering (per-caller entitlement enforcement) | 5.4.1 |
| Citation and attribution validation against caller entitlements | 5.4.2 |
| Agent PDP runtime isolation from agent execution environment | 5.5.1 |
| Structured action descriptions to PDP (not raw agent reasoning context) | 5.5.2 |
| KV-cache partitioning by session/tenant to prevent prompt reconstruction | 5.6.1 |
| Shared model serving tenant isolation (fine-tuning, inference, embeddings) | 5.6.2 |
| Peer authorization policy (approved agent registry) for agent-to-agent task delegation | 9.6.6 |

**Common pitfalls:** granting broad OAuth scopes instead of minimal required; not re-evaluating authorization when context changes mid-session; allowing model-generated output to override hard policy decisions.

---

## AD.3 Encryption at Rest

Protect stored data, models, secrets, logs, and backups through encryption.

| Control / Technique | Requirement IDs |
| --- | --- |
| Training data encryption at rest | 1.2.3 |
| Labeled data encryption | 1.3.5 |
| Log encryption at rest | 13.1.4 |

**Common pitfalls:** encrypting the database but not model checkpoints or embeddings; not encrypting logs that contain prompt/response data; storing encryption keys alongside the data they protect.

---

## AD.4 Encryption in Transit

Protect data moving between services, agents, tools, and edge devices.

| Control / Technique | Requirement IDs |
| --- | --- |
| Mutual TLS with certificate validation for inter-service communication | 4.3.4 |
| Authenticated streamable-HTTP transport with TLS 1.3 for MCP | 10.3.1, 10.3.2 |
| SSE private channel with TLS enforcement | 10.3.2 |
| Log encryption in transit | 13.1.4 |
| MCP client minimum protocol version enforcement against downgrade negotiation | 10.3.6 |

**Common pitfalls:** allowing plaintext interconnects in multi-tenant GPU clusters; using SSE over public internet without TLS; not validating certificates on internal service calls.

---

## AD.5 Key & Secret Management

Manage cryptographic keys, secrets, and credentials throughout their lifecycle.

| Control / Technique | Requirement IDs |
| --- | --- |
| Agent identity credential rotation with rapid revocation | 9.4.5 |
| MCP runtime credential injection (no plaintext secrets) | 10.1.2 |

**Common pitfalls:** hardcoded secrets in config or container images; neglecting rotation schedules; storing MCP OAuth tokens in server state rather than validating externally.

---

## AD.6 Cryptographic Integrity & Signing

Verify authenticity and detect tampering of models, artifacts, messages, logs, and tool definitions.

| Control / Technique | Requirement IDs |
| --- | --- |
| Cryptographic hashes for training data integrity | 1.2.5, 1.3.4 |
| Cryptographic model signing | 3.1.2 |
| Model signature and checksum verification at deployment and load | 3.1.3 |
| Signed build artifacts with build-origin metadata | ASVS v5 V15 / SLSA |
| Build signature validation at deployment | ASVS v5 V15 / SLSA |
| Third-party model origin and integrity verification (signed records) | 6.1.1 |
| Cryptographic signature validation for model publishers | 6.2.1, 6.2.2 |
| Model watermarking and fingerprinting | 11.5.5 |
| Execution chain cryptographic binding (chain ID) for agent actions | 9.4.2 |
| Agent action signing and timestamps for non-repudiation and traceability | 9.4.4 |
| MCP component signature and checksum verification | 10.1.1 |
| MCP schema integrity signing and tool definition hash tracking | 10.4.8, 10.4.5 |
| Publisher key pinning per source registry with rotation re-approval | 6.2.2 |
| Agent persisted state integrity protection (MAC/signature, rejection on failure) | 9.4.6 |

**Common pitfalls:** using mutable `:latest` tags instead of immutable digests; not re-verifying tool definition hashes between MCP invocations; missing replay protection on agent messages.

---

## AD.7 Input Validation & Sanitization

Validate, normalize, and constrain all inputs before they reach models or downstream systems.

| Control / Technique | Requirement IDs |
| --- | --- |
| Prompt injection detection ruleset / service | 2.1.1 |
| Instruction hierarchy enforcement (system > developer > user) | 2.1.2 |
| Instruction hierarchy preservation across multi-step and tool-augmented workflows, including prompt composition | 2.1.5 |
| Per-request demonstration count limits in context window | 2.1.7 |
| Many-shot jailbreaking pattern detection (systematic in-context behavioral override) | 2.1.8 |
| In-context behavioral override attempts classified as prompt injection events | 2.1.9 |
| Context window proportion limits and token limit enforcement (reject, not truncate) | 2.1.3 |
| Third-party content sanitization | 2.1.6 |
| Character set allow-listing for model prompt inputs | 2.1.4 |
| Pre-tokenization input normalization (Unicode NFC, homoglyph mapping, control/invisible character removal, bidirectional text neutralization) | 2.2.1 |
| Post-normalization suspicious artifact rejection or flagging | 2.2.3 |
| Adversarial input quarantine and logging | 2.2.2 |
| Encoding and representation smuggling detection and mitigation | 2.2.4 |
| Content classifiers for inbound prompts (hate, violence, sexual, illegal) with threshold-based rejection or sanitization | 2.3.1 |
| Multilingual classifier gap evaluation with compensating controls (language detection, conservative thresholds, human review routing) | 2.3.2 |
| Policy-violating input rejection before model propagation | 2.3.3 |
| User-specific and agent-aware policy screening | 2.1.10 |
| Extracted and hidden content from non-text inputs treated as untrusted | 2.4.1 |
| Adversarial perturbation detection on image/audio inputs | 2.4.2 |
| Cross-modal attack detection | 2.4.3 |
| MCP input type checking, boundary validation, and enumeration enforcement | 10.4.4 |
| MCP rejection of unrecognized or oversized function call parameters | 10.4.7 |
| MCP message-framing integrity and strict schema validation | 10.4.3 |
| MCP maximum payload size limits and malformed frame rejection | 10.4.6 |
| MCP schema validation for tool and resource integrity | 10.4.8 |
| Tool output schema and security policy validation before re-entry to agent | 9.3.3 |
| MCP tool response validation (prompt injection, context manipulation) | 10.4.1 |

**Common pitfalls:** validating only text modality while ignoring image/audio channels; relying solely on regex without semantic detection; not validating tool outputs before they re-enter agent context.

---

## AD.8 Output Filtering & Safety

Constrain, filter, and validate model outputs before they reach users or downstream systems.

| Control / Technique | Requirement IDs |
| --- | --- |
| Output format schema validation | 7.1.1 |
| Stop sequences and token limits | 7.1.2 |
| Parameterized queries and safe deserializers for output processing | 7.1.3 |
| Confidence scoring and uncertainty estimation | 7.2.1 |
| Confidence threshold gating with fallback messages | 7.2.2 |
| Output safety classifiers (hate, harassment, violence) | 7.3.1 |
| System prompt leakage detection in outputs (verbatim and paraphrased) | 7.3.2 |
| Prevention of auto-triggered outbound requests from model-generated output | 7.3.3 |
| System prompt and backend data removal from explanations | 7.5.1 |
| RAG unsupported-claim blocking or redaction before serving | 7.6.4 |
| Authorization-aware post-inference filtering (per-caller entitlement enforcement) | 5.4.1 |
| Citation and attribution validation against caller entitlements | 5.4.2 |
| MCP error response sanitization (no stack traces, tokens, internal paths) | 10.4.2 |
| Generalization or one-way transformation of model-inferred sensitive attributes (ranges, buckets) to limit reconstruction of training records | 11.4.1 |

**Common pitfalls:** redacting PII in text but not in structured data fields; not enforcing stop sequences on streaming outputs; leaking internal architecture through error messages.

---

## AD.9 Rate Limiting & Resource Budgets

Enforce consumption bounds to prevent abuse, runaway execution, and denial-of-service.

| Control / Technique | Requirement IDs |
| --- | --- |
| Per-user, per-IP, per-API-key rate limits | ASVS v5 V2.4 |
| Burst and sustained rate limiting | ASVS v5 V2.4 |
| Per-agent token, cost, and tool-call budgets | 9.1.1 |
| Recursion depth and max concurrency / fan-out limits | 9.1.1 |
| Wall-clock time and monetary spend caps | 9.1.1 |
| Cumulative resource counters with hard-stop thresholds and circuit breaker enforcement | 9.1.2 |
| Per-tool CPU, memory, disk, egress, and execution time limits with fail-closed termination on breach | 9.3.2 |
| Quota and timeout breach logging (tool, exceeded limit, timestamp) | 9.3.4 |
| Query-rate limiting for model extraction and inversion defense, sized to the threat model (e.g., the number of queries required to approximate the model or to reconstruct training records) rather than as a generic API throttle | 11.4.2, 11.5.1 |
| Anomalous usage pattern detection and blocking | 13.2.3, ASVS v5 V2.4 |

**Common pitfalls:** setting rate limits per-endpoint but not per-agent-session; not accounting for tool fan-out when calculating budgets; missing circuit breakers on recursive agent chains.

---

## AD.10 Sandboxing & Process Isolation

Isolate workloads, tools, models, and agents to contain failures and prevent lateral movement.

| Control / Technique | Requirement IDs |
| --- | --- |
| Minimal OS permissions and Linux capabilities | 4.1.1 |
| Mandatory access control (seccomp, AppArmor, SELinux) | 4.1.2 |
| Read-only root filesystem with restrictive mount options | 4.1.3 |
| Runtime privilege escalation and container escape detection | 4.1.4 |
| TEE / confidential computing with remote attestation | 4.1.5 |
| Tool and plugin sandboxing (container, VM, WASM, OS sandbox) | 9.3.1 |
| Sandbox escape detection with automated tool quarantine | 9.3.7 |
| Agent isolation across tenants, security domains, and environments | 9.8.1 |
| MCP stdio local-only enforcement with terminal injection prevention | 10.6.1 |

**Common pitfalls:** sharing infrastructure between dev and prod; granting containers more capabilities than needed; not restricting cloud metadata service access from AI workloads.

---

## AD.11 Network Segmentation & Egress Control

Control network boundaries, traffic flow, and outbound access for AI workloads.

| Control / Technique | Requirement IDs |
| --- | --- |
| Default-deny network policies with explicit allow-lists | 4.3.1 |
| Network segmentation across dev / test / prod environments | 4.3.2, 3.4.1 |
| Separate IAM roles and security groups per environment with no shared principals | 4.3.6 |
| Restricted administrative access and cloud metadata service blocking | 4.3.3 |
| Egress traffic restriction to approved destinations with logging | 4.3.5 |
| MCP outbound egress restricted to approved destinations (all others blocked by default) | 10.5.1 |
| MCP function invocation restricted to statically defined allow-listed names | 10.6.2 |
| Default-deny cross-domain agent discovery and calls | 9.8.1 |
| Origin and Host header validation for DNS rebinding defense | 10.3.3 |
| SSE public internet blocking | 10.3.2 |

**Common pitfalls:** allowing AI workloads to reach cloud metadata services; not logging egress traffic for forensic analysis; missing Origin header validation enabling DNS rebinding attacks.

---

## AD.12 Supply Chain & Artifact Integrity

Verify origin and authenticity, scan dependencies, and enforce integrity of models, frameworks, datasets, and build artifacts.

| Control / Technique | Requirement IDs |
| --- | --- |
| Model registry with AI BOM (SPDX, CycloneDX) | 3.1.1, 6.5.1 |
| Model dependency graph tracking (services, agents, environments) | 3.1.4 |
| Model origin records (source, training data checksums, authorship) | 3.1.5, 6.1.1 |
| Automated reproducible builds | ASVS v5 V15 / SLSA |
| SBOM production from automated builds | ASVS v5 V15.1.2 / SCVS |
| Reproducible build hash comparison | SLSA Build L3 |
| CI pipeline dependency scanning | ASVS v5 V15.2.1 / SCVS V5 |
| Critical / high-severity vulnerability blocking in CI | ASVS v5 V15.1.1 / SCVS V5 |
| Dependency version pinning with lockfile enforcement | SCVS V4 / CIS Guide |
| Immutable digest references for containers (no mutable tags) | SCVS / CIS Guide |
| Expired and unmaintained dependency detection | ASVS v5 V15.1.1, V15.2.1 |
| Approved source enforcement for AI artifacts | 6.2.1 |
| Malicious layer and trojan trigger scanning | 6.1.2 |
| Unsafe deserialization format prohibition and format-aware scanning at load time | 4.1.3 |
| External dataset poisoning assessment (fingerprinting, outlier detection) | 6.3.1 |
| Copyright and PII detection in external datasets | 6.3.2 |
| Dataset origin and lineage documentation | 6.3.3 |
| AI BOM cryptographic signing | 6.5.2 |
| Build attestation retention | SLSA Build Track |

**Common pitfalls:** not scanning fine-tuning datasets for poisoning; lacking rollback procedures when a compromised model is detected; treating AI BOMs as static documents rather than version-controlled artifacts.

---

## AD.13 Deployment & Lifecycle Management

Manage model deployment, rollback, retirement, and emergency response.

| Control / Technique | Requirement IDs |
| --- | --- |
| Automated input validation testing before deployment | 3.2.1 |
| Automated output sanitization testing before deployment | 3.2.2 |
| Safety evaluations with pass/fail thresholds before deployment | 3.2.3 |
| Automatic deployment block on safety evaluation threshold failure | 3.2.4 |
| Agent workflow, tool, MCP, and RAG integration testing | 3.2.5 |
| Immutable audit records for model changes | 3.2.6 |
| Deployment validation with failure blocking and override approval | 3.2.8 |
| Canary / blue-green deployments with automated rollback triggers | 3.3.1 |
| Parallel deployment cohort isolation (A/B, canary, shadow) | 3.3.3 |
| Atomic state restoration on rollback (weights, config, adapters, safety models) | 3.3.2 |
| Emergency model shutdown capability with pre-defined response time | 3.3.4 |
| Shutdown cascade to tools, MCP, RAG, credentials, memory stores | 3.3.5 |
| Development / test / production environment separation | 3.4.1 |
| No shared infrastructure across environment boundaries | 3.4.2 |
| Version control for all development artifacts (hyperparams, scripts, prompts, policies) | 3.4.3 |
| Secure model artifact wiping and cryptographic erasure on retirement | 3.5.1 |
| Model signature revocation and registry deny-list on retirement | 3.5.2 |
| AI-specific supply chain incident response (model rollback, signature revocation) | 6.4.1 |

**Common pitfalls:** not testing rollback procedures before they are needed; leaving retired model artifacts in serving caches; missing shutdown cascade to downstream tool and MCP connections.

---

## AD.14 Privacy & Data Minimization

Protect personal data and enforce data subject rights throughout the AI lifecycle.

| Control / Technique | Requirement IDs |
| --- | --- |
| Training data minimization (exclude unnecessary features, PII, leaked test data) | 1.1.2 |
| Labeled data anonymization and granular redaction | 1.3.5 |
| Direct and quasi-identifier removal | 12.1.1 |
| k-anonymity and l-diversity measurement with automated audits | 12.1.2 |
| Feature-importance leakage check on trained models | 12.1.3 |
| Synthetic data with formal re-identification risk bounds | 12.1.4 |
| Data deletion propagation across AI artifacts (datasets, checkpoints, caches) | 12.2.1 |
| Shadow-model evaluation of unlearning effectiveness | 12.2.2 |
| Machine unlearning with certified algorithms | 12.2.3 |
| Privacy-loss accounting with epsilon budget tracking and alerts | 12.3.1 |
| Empirical (black-box) differential privacy audits | 12.3.2 |
| Formal differential privacy proofs (including post-training and embeddings) | 12.3.3 |
| Purpose tags with machine-readable alignment and runtime enforcement | 12.4.1, 12.4.2 |
| Consent-aware inference scope validation (refuse or downgrade off-scope responses) | 12.5.1 |
| Consent withdrawal propagation through AI artifacts (aligned with deletion SLA) | 12.5.2 |
| Local or central differential privacy in federated learning | 12.6.1 |
| Differentially private training metrics | 12.6.2 |
| Federated canary-based privacy auditing | 12.6.3 |
| Federated training utility-loss bound against ε budget | 12.6.4 |
| PII detection and removal in external datasets | 6.3.2 |

**Common pitfalls:** deleting records from the database but not from model checkpoints or embeddings; not accounting for epsilon budget accumulation across queries; treating anonymization as a one-time step.

---

## AD.15 Adversarial Testing & Model Hardening

Test for and defend against evasion, extraction, inversion, poisoning, and alignment bypass attacks.

| Control / Technique | Requirement IDs |
| --- | --- |
| Refusal and safe-completion guardrails | 11.1.1 |
| Red-team and jailbreak test suites (version-controlled) | 11.1.2 |
| Automated harmful-content rate evaluation with regression detection | 11.1.3 |
| RLHF / Constitutional AI alignment training | 11.1.4 |
| Adversarial training and equivalent hardening techniques applied where feasible | 11.2.3 |
| Adversarial hardening configurations and procedures documented and reproducible | 11.2.5 |
| Adversarially robust distillation — distill teacher into student using adversarial training so the student inherits robustness as well as accuracy (implementation example for 11.2.3) | 11.2.3 |
| Certified robustness metrics tracking per model version with degradation alerting | 11.2.4 |
| Formal robustness verification (certified bounds, interval-bound propagation) | 11.2.7 |
| Post-transformation robustness re-certification (fine-tuning, distillation, quantization, adapter merging) | 11.2.8 |
| Adversarial-example detection with production alerting | 11.2.2 |
| Model ensemble as evasion containment — route queries through independently trained models and flag disagreement beyond a threshold (implementation example for 11.2.2) | 11.2.2 |
| Output calibration and perturbation for privacy | 11.3.1 |
| Confidence obfuscation / output perturbation — return calibrated but deliberately imprecise confidence scores to impede model extraction and membership inference (implementation example for 11.3.1) | 11.3.1 |
| DP-SGD (differentially private training) with documented epsilon | 11.3.2 |
| PATE (Private Aggregation of Teacher Ensembles) — train student model using noisy aggregation of teacher outputs so no individual training record is exposed (implementation example for 11.3.2) | 11.3.2 |
| Membership inference attack simulation (shadow-model, likelihood-ratio) | 11.3.3 |
| Model extraction detection (query-pattern analysis, diversity measurement) | 11.5.3 |
| Statistical outlier and consistency scoring on external inputs | 11.6.1 |
| Adaptive attack evasion testing | 11.6.5 |
| AI-augmented review of high-risk agent actions (secondary model, structured self-review, ensemble-of-judges) supplementing the deterministic policy gate (C9.7.1) | 11.8.1 |
| AI-augmented review mechanism protected against prompt-injection bypass | 11.8.2 |
| Self-modification restriction with scope bounds and rate limits | 11.9.1, 11.9.5 |
| Self-modification reversibility and integrity verification enabling rollback to known-good state | 11.9.4 |
| Safety-violation feedback pipeline integrity, poisoning detection, and human review gates | 11.9.6 |
| Data augmentation with perturbed inputs for training robustness | 1.4.6 |
| RONI (Reject On Negative Influence) filtering — influence-score each training sample and reject those that degrade held-out performance beyond a threshold (implementation example for 1.4.2) | 1.4.2 |
| Gradient fingerprinting / per-sample gradient analysis — detect abnormal gradient norms or directions indicating poisoned samples during training (implementation example for 1.4.2) | 1.4.2 |
| Activation clustering — cluster intermediate activations to detect backdoor-associated subpopulations (implementation example for 1.4.2) | 1.4.2 |

**Common pitfalls:** testing only known jailbreak patterns without adaptive attacks; not updating red-team suites after model updates; relying on a single defense without defense-in-depth.

---

## AD.16 Logging & Audit

Capture security-relevant events with integrity protection for forensic analysis and compliance.

| Control / Technique | Requirement IDs |
| --- | --- |
| Security-relevant metadata logging for AI interactions (timestamp, user ID, session ID, model version, token count, input hash, confidence score, safety filter outcome) | 13.1.1 |
| AI interaction logs exclude prompt and response content by default, with content logging requiring explicit opt-in and documented justification | 13.1.2 |
| Secure, access-controlled log repositories with retention policies | 13.1.3 |
| Log encryption at rest and in transit | 13.1.4 |
| PII, credential, and proprietary information redaction in logs | 13.1.5 |
| Policy decision and safety filtering action logging | 13.1.3 |
| Audit log context fields sufficient for forensic reconstruction (actor, delegation, policy, parameters, outcomes) | 9.4.3 |
| Agent action cryptographic chain ID binding | 9.4.2 |
| Agent action signing and timestamps for non-repudiation | 9.4.4 |
| Immutable audit records for model changes (actor, change type, before/after) | 3.2.6 |
| Generic audit log immutability and tamper-evidence | ASVS v5 V16.4.2 |
| CI/CD audit log streaming to SIEM | ASVS v5 V16.4.3 |
| Detection rules for anomalous package pulls and tampered build steps | ASVS v5 V16.3.3 |
| Safety violation metrics logging | 7.6.1 |
| Self-modification logging classified as security event with what/when/by-whom/authorization detail | 11.9.3 |
| Human oversight intervention logging (kill-switch activations, mode transitions, override commands) with operator identity, channel, trigger, and prior/resulting state | 14.3.1 |

**Common pitfalls:** logging prompts without redacting PII; using mutable log storage without integrity protection; not including sufficient context for forensic reconstruction; logging agent actions and approvals but not human-initiated overrides such as kill-switch activations.

---

## AD.17 Monitoring, Alerting & Incident Response

Detect anomalies, alert on threats, and respond to security incidents in AI systems.

| Control / Technique | Requirement IDs |
| --- | --- |
| Jailbreak and prompt injection attempt detection (signature-based) | 13.2.1 |
| SIEM integration with standard log formats | 13.2.2 |
| AI-specific event enrichment (model ID, confidence, filter decisions) | 13.2.2 |
| Behavioral anomaly detection (unusual patterns, excessive retries, systematic probing) | 13.2.3, 13.2.5 |
| Detection rules for AI-specific attack patterns (jailbreak campaigns, prompt injection, system prompt extraction, model extraction) | 13.2.4 |
| Automated incident response (isolation and blocking of compromised models and malicious users) | 13.2.6 |
| Performance metric monitoring (accuracy, latency, error rate) with alerting | 13.3.1, 13.3.3, 13.3.4 |
| Performance degradation retraining and replacement workflow triggers | 13.3.8 |
| Hallucination detection monitoring | 13.3.5 |
| Hallucination rate time-series tracking | 13.3.9 |
| Training pipeline telemetry monitoring (runtime duration, loss trajectory, convergence rate) with baseline alerting and artifact gating | 13.3.10 |
| Model extraction alert generation with query metadata logging | 11.5.2 |
| Emergent multi-agent behavior detection (oscillation, deadlock, broadcast storms) | 9.8.4 |
| AI-specific incident response plans (model compromise, data poisoning, adversarial attack) | 13.5.1 |
| AI-specific forensic tools for model behavior investigation | 13.5.2 |
| Safety violation rate alerting | 7.6.3 |
| Real-time security policy updates without full redeployment | 11.7.1 |
| Policy change rollback procedures and testing | 11.7.3 |

**Common pitfalls:** not correlating AI-specific events with broader SIEM alerts; treating model drift as a scheduled check rather than continuous monitoring; lacking AI-specific forensic tooling during incident response.

---

## AD.18 Explainability & Transparency

Enable human understanding of model decisions through interpretability artifacts and uncertainty quantification, with explanations sanitized to avoid leaking internal context.

| Control / Technique | Requirement IDs |
| --- | --- |
| Sanitization of user-facing explanations to remove system prompts and backend data | 7.4.1 |
| Logging of model interpretability artifacts (attention maps, feature attributions) for forensic use | 7.4.2 |
| Confidence or uncertainty estimation for generated answers | 7.2.1 |
| Automatic blocking or fallback when confidence drops below a defined threshold | 7.2.2 |
| Model output calibration to reduce overconfident predictions exploitable by membership inference | 11.3.1 |

**Common pitfalls:** providing explanations that expose system prompts or internal architecture; treating LLM-generated rationales as faithful descriptions of model internals; not calibrating uncertainty estimates such that downstream gates cannot trust them.

---

## AD.19 Human Oversight & Approval Gates

Require human review and approval for high-impact, irreversible, or safety-critical actions, and provide reliable shutdown and graceful-degradation paths under human control. Effective human oversight requires four cooperating layers: a **policy** that classifies which actions are high-risk (C14.2), a **runtime gate** that blocks execution until approval is received (C9.2), **kill-switch and graceful-degradation mechanisms** to halt or constrain the system when needed (C14.1), and **independent audit trails** for both approvals (C13.6.4) and human-initiated overrides (C14.3). Each layer is separately verifiable; an approval gate without a policy is unenforceable, a policy without a runtime gate is unenforced, and either without audit trails is unattributable.

| Control / Technique | Requirement IDs |
| --- | --- |
| Documented high-risk action policy (classification criteria, approval authority) | 14.2.1 |
| High-impact action approval gates (deploy, delete, financial, notify) | 9.2.1 |
| Approval parameter binding (prevent approve-one-execute-another) | 9.2.2 |
| High-impact intent confirmation with exact parameter binding and quick expiration | 9.2.3 |
| Fail-closed default action (block pending action) when human approval is not received within TTL | 14.2.2 |
| Any non-fail-closed TTL-expiry default explicitly authorized and classified as a high-risk policy decision requiring approval authority sign-off | 14.2.3 |
| Human review on anomaly detection | 11.6.3 |
| High-risk model quarantine with human review and sign-off | 6.1.3 |
| Post-condition outcome checking with containment on mismatch | 9.7.2 |
| Compensating actions and transactional rollback on failure | 9.2.4 |
| Manual kill-switch to halt model inference and outputs | 14.1.1 |
| Intermediate operational degradation states (tool disable, model swap, read-only, source removal) | 14.1.3 |
| Recurring exercise of kill-switch and intermediate-state mechanisms with response-time verification | 14.1.2 |
| Out-of-band override and kill-switch channel for autonomous agents | 14.1.4 |

**Common pitfalls:** documenting a high-risk action policy that is never wired to a runtime gate; binding approval to a hash of parameters without binding to identity or context (replay across sessions); confirmation tokens without quick expiration; defaulting to fail-open when the approver does not respond, silently bypassing the gate; assuming an in-band kill-switch will work against a compromised agent; kill-switch implemented but never exercised, atrophying until the moment it is needed.

---

---

## References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/42001)
* [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)
