# Appendix D: AI Security Controls Inventory

## Objective

This appendix provides a concise inventory of every security control and defense technique referenced across the AISVS requirements. Controls are grouped by security control category so that implementers can find all related defenses in one place regardless of which AISVS chapter defines them.

---

## AD.1 Authentication

Verify the identity of users, agents, services, MCP clients/servers, and edge devices before granting access.

| Control / Technique | Requirement IDs |
|---|---|
| Centralized identity provider (OIDC, SAML) | 5.1.1 |
| Multi-factor authentication for high-risk operations | 5.1.2 |
| Signed JWT tokens for identity proof | 5.1.3 |
| Unique cryptographic agent and orchestrator identity | 9.4.1 |
| First-class principal authentication (no end-user credential reuse) | 9.4.1 |
| Agent identity credential rotation and rapid revocation | 9.4.4 |
| OAuth 2.1 for MCP client authentication | 10.2.1 |
| MCP server OAuth token validation (issuer, audience, expiration, scope) | 10.2.2 |
| MCP server registration with explicit ownership | 10.2.3 |
| Cryptographically secure MCP session IDs (not used for auth) | 10.2.8 |
| Edge device mutual authentication with certificate validation | 4.8.1 |
| Workload attestation for confidential compute | 4.5.3 |
| Hardware-based attestation (TPM, DRTM) | 4.7.1 |

**Common pitfalls:** reusing end-user credentials for agent-to-agent calls; using MCP session IDs as authentication tokens; not rotating agent credentials on suspected compromise.

---

## AD.2 Authorization & Access Control

Enforce access decisions across users, agents, tools, data, and MCP resources using policy-based controls.

| Control / Technique | Requirement IDs |
|---|---|
| RBAC / ABAC / zero-trust authorization models | 5.2.1, 5.2.7 |
| Policy decision engines (OPA, Cedar) | 5.2.6 |
| Least-privilege resource access | 5.2.1, 5.6.2 |
| Row-level security and field-level masking | 5.3.3 |
| Classification label propagation on outputs | 5.2.4 |
| Session-based authorization binding | 5.5.2 |
| Scoped capability tokens for agents | 5.6.1 |
| Fine-grained agent action authorization (tool, parameters, resources, data scope) | 9.6.1 |
| Delegation context propagation with integrity protection (user, tenant, scopes) | 9.6.2 |
| Continuous authorization re-evaluation (context, time, risk) | 9.6.3 |
| Application-layer policy enforcement (model output cannot bypass) | 9.6.4 |
| Pre-execution policy constraint gates (deny rules, allow-lists, budgets) | 9.7.1 |
| Scope-filtered MCP tool discovery (tools/list) | 10.2.6 |
| Per-tool MCP invocation access control (argument, token scope) | 10.2.7 |
| Minimum scope requests with wildcard and overly broad scope rejection | 10.2.11 |
| MCP policy enforcement that model output cannot bypass | 10.2.4 |
| Output format restriction by permission level | 5.4.3 |

**Common pitfalls:** granting broad OAuth scopes instead of minimal required; not re-evaluating authorization when context changes mid-session; allowing model-generated output to override hard policy decisions.

---

## AD.3 Encryption at Rest

Protect stored data, models, secrets, logs, and backups through encryption.

| Control / Technique | Requirement IDs |
|---|---|
| Training data encryption at rest | 1.2.3 |
| Labeled data encryption | 1.3.4 |
| Secrets encryption at rest in secrets management system | 4.4.1 |
| Log encryption at rest | 13.1.3 |
| TEE memory encryption and integrity protection | 4.5.4 |
| Confidential inference (sealed model weights in protected execution) | 4.5.5 |
| Air-gapped / WORM backup storage | 4.6.3 |
| Model encryption at rest on mobile with trusted runtime decryption | 4.8.9 |
| Hardware-backed key stores (Secure Enclave, Android Keystore, TPM) | 4.8.8 |

**Common pitfalls:** encrypting the database but not model checkpoints or embeddings; not encrypting logs that contain prompt/response data; storing encryption keys alongside the data they protect.

---

## AD.4 Encryption in Transit

Protect data moving between services, agents, tools, and edge devices.

| Control / Technique | Requirement IDs |
|---|---|
| Mutual TLS with certificate validation for inter-service communication | 4.3.4 |
| Mutual TLS for agent-to-agent and agent-to-tool communication (TLS 1.3+) | 9.5.1 |
| Authenticated streamable-HTTP transport with TLS 1.3 for MCP | 10.3.1, 10.3.2 |
| SSE private channel with TLS enforcement | 10.3.3 |
| Encrypted TEE communication channels | 4.5.6 |
| Authenticated accelerator interconnects (NVLink, PCIe, InfiniBand) | 4.7.7 |
| Encrypted edge-to-cloud communication with bandwidth throttling | 4.8.6 |
| Log encryption in transit | 13.1.3 |

**Common pitfalls:** allowing plaintext interconnects in multi-tenant GPU clusters; using SSE over public internet without TLS; not validating certificates on internal service calls.

---

## AD.5 Key & Secret Management

Manage cryptographic keys, secrets, and credentials throughout their lifecycle.

| Control / Technique | Requirement IDs |
|---|---|
| Hardware-backed key storage (HSM, KMS, FIPS 140-3 Level 3) | 4.4.4, 4.7.6 |
| Secrets isolation from application workloads | 4.4.1 |
| Runtime secret injection (removed from code, config, images) | 4.4.3 |
| Automated key and secret rotation | 4.4.5 |
| Agent identity credential rotation with rapid revocation | 9.4.4 |
| MCP runtime credential injection (no plaintext secrets) | 10.1.2 |
| Watermark verification key and trigger set protection | 11.5.5 |
| Separate backup credentials from production | 4.6.3 |
| User-space key inaccessibility on mobile | 4.8.8 |

**Common pitfalls:** hardcoded secrets in config or container images; neglecting rotation schedules; storing MCP OAuth tokens in server state rather than validating externally.

---

## AD.6 Cryptographic Integrity & Signing

Verify authenticity and detect tampering of models, artifacts, messages, logs, and tool definitions.

| Control / Technique | Requirement IDs |
|---|---|
| Cryptographic hashes for training data integrity | 1.2.4, 1.3.2 |
| Cryptographic model signing with verification at deployment and load | 3.1.2 |
| Signed build artifacts with build-origin metadata | 4.2.2 |
| Build signature validation at deployment | 4.2.3 |
| Third-party model origin and integrity verification (signed records) | 6.1.1 |
| Cryptographic signature validation for packages and publishers | 6.4.2 |
| Model watermarking and fingerprinting | 7.7.5, 11.5.4 |
| Execution chain cryptographic signing with non-repudiation timestamps | 9.4.2 |
| Message integrity with nonce / sequence / timestamp replay protection | 9.5.3 |
| Cryptographic log signatures (write-only / append-only) | 13.1.6 |
| Tamper-evident audit logs (WORM) | 9.4.3 |
| MCP component signature and checksum verification | 10.1.1 |
| MCP schema integrity signing and tool definition hash tracking | 10.4.2, 10.4.5 |
| DAG cryptographic signatures and tamper-evident storage | 13.7.3 |

**Common pitfalls:** using mutable `:latest` tags instead of immutable digests; not re-verifying tool definition hashes between MCP invocations; missing replay protection on agent messages.

---

## AD.7 Input Validation & Sanitization

Validate, normalize, and constrain all inputs before they reach models or downstream systems.

| Control / Technique | Requirement IDs |
|---|---|
| Prompt injection detection ruleset / service | 2.1.1 |
| Instruction hierarchy enforcement (system > developer > user) | 2.1.2 |
| Third-party content sanitization | 2.1.3 |
| Unicode NFC normalization and homoglyph mapping | 2.2.1 |
| Control / invisible character removal | 2.2.1, 2.2.5 |
| Statistical and embedding-distance anomaly detection on inputs | 2.2.3 |
| Character set allow-listing | 2.3.1, 2.3.2 |
| Schema validation (JSON Schema, Protocol Buffers) | 2.4.1, 7.1.1 |
| Token and byte limit enforcement | 2.4.2 |
| Constant-time validation | 2.4.4 |
| Content classifiers (hate, violence, sexual, illegal) | 2.5.1 |
| Multi-modal input validation (images, audio, files) | 2.7.1 |
| Malware and steganography scanning | 2.7.2 |
| Adversarial perturbation detection | 2.7.3 |
| Cross-modal attack detection | 2.7.5 |
| Pattern matching (regex) on inputs and outputs | 2.8.1 |
| Adaptive detection models | 2.8.2 |
| MCP input type checking, boundary validation, and enumeration enforcement | 10.4.4 |
| MCP message-framing integrity and payload size limits | 10.4.3 |
| MCP schema validation for tool and resource integrity | 10.4.2 |
| Tool output schema and security policy validation before re-entry to agent | 9.3.3 |
| MCP tool response validation (prompt injection, context manipulation) | 10.4.1 |

**Common pitfalls:** validating only text modality while ignoring image/audio channels; relying solely on regex without semantic detection; not validating tool outputs before they re-enter agent context.

---

## AD.8 Output Filtering & Safety

Constrain, filter, and validate model outputs before they reach users or downstream systems.

| Control / Technique | Requirement IDs |
|---|---|
| Output format schema validation | 7.1.1 |
| Stop sequences and token limits | 7.1.2 |
| Parameterized queries and safe deserializers for output processing | 7.1.3 |
| Confidence scoring and uncertainty estimation | 7.2.1 |
| Confidence threshold gating with fallback messages | 7.2.2 |
| Output safety classifiers (hate, harassment, violence) | 7.3.1 |
| PII detection and redaction (post-inference filtering) | 7.3.2, 7.3.3, 5.4.1 |
| Human approval for high-risk content | 7.3.5 |
| System prompt and backend data removal from explanations | 7.5.1 |
| AI-generated media watermarking | 7.7.5 |
| Copyright violation detection | 7.7.3 |
| Explicit / non-consensual content filters | 7.7.1 |
| Citation and attribution validation | 5.4.2 |
| MCP error response sanitization (no stack traces, tokens, internal paths) | 10.4.6 |

**Common pitfalls:** redacting PII in text but not in structured data fields; not enforcing stop sequences on streaming outputs; leaking internal architecture through error messages.

---

## AD.9 Rate Limiting & Resource Budgets

Enforce consumption bounds to prevent abuse, runaway execution, and denial-of-service.

| Control / Technique | Requirement IDs |
|---|---|
| Per-user, per-IP, per-API-key rate limits | 2.6.1 |
| Burst and sustained rate limiting | 2.6.2 |
| Per-agent token, cost, and tool-call budgets | 2.6.2, 9.1.1 |
| Recursion depth and max concurrency / fan-out limits | 9.1.1 |
| Wall-clock time and monetary spend caps | 9.1.1 |
| Cumulative resource counters with hard-stop thresholds | 9.1.2 |
| Circuit breaker enforcement | 9.1.3 |
| Per-tool CPU, memory, disk, egress, and execution time limits | 9.3.2 |
| Query-rate limiting for model extraction and inversion defense | 11.4.2, 11.5.1 |
| MCP outbound execution limits, timeouts, recursion limits, and circuit breakers | 10.5.2 |
| Anomalous usage pattern detection and blocking | 2.6.3 |
| Resource quotas (CPU, memory, GPU) for infrastructure | 4.6.1 |
| Threshold-based protection triggers on resource exhaustion | 4.6.2 |

**Common pitfalls:** setting rate limits per-endpoint but not per-agent-session; not accounting for tool fan-out when calculating budgets; missing circuit breakers on recursive agent chains.

---

## AD.10 Sandboxing & Process Isolation

Isolate workloads, tools, models, and agents to contain failures and prevent lateral movement.

| Control / Technique | Requirement IDs |
|---|---|
| Minimal OS permissions and Linux capabilities | 4.1.1 |
| Mandatory access control (seccomp, AppArmor, SELinux) | 4.1.2 |
| Read-only root filesystem with restrictive mount options | 4.1.3 |
| Runtime privilege escalation and container escape detection | 4.1.4 |
| TEE / confidential computing with remote attestation | 4.1.5, 4.5.4, 4.5.6 |
| Untrusted AI model sandboxing with network isolation | 4.5.1, 4.5.2 |
| Tool and plugin sandboxing (container, VM, WASM, OS sandbox) | 9.3.1 |
| Sandbox escape detection with automated tool quarantine | 9.3.6 |
| Agent isolation across tenants, security domains, and environments | 9.8.1 |
| GPU memory isolation (MIG / VM partitioning) with peer-to-peer prevention | 4.7.5 |
| On-device process, memory, and file access isolation | 4.8.7 |
| MCP stdio local-only enforcement with terminal injection prevention | 10.6.1 |
| MCP tenant and environment boundary enforcement | 10.6.3 |

**Common pitfalls:** sharing infrastructure between dev and prod; granting containers more capabilities than needed; not restricting cloud metadata service access from AI workloads.

---

## AD.11 Network Segmentation & Egress Control

Control network boundaries, traffic flow, and outbound access for AI workloads.

| Control / Technique | Requirement IDs |
|---|---|
| Default-deny network policies with explicit allow-lists | 4.3.1 |
| Network segmentation across dev / test / prod environments | 4.3.2, 3.4.1 |
| Restricted administrative access and cloud metadata service blocking | 4.3.3 |
| Egress traffic restriction to approved destinations with logging | 4.3.5 |
| Egress allow-lists for training environments | 3.4.3 |
| MCP egress allow-list with cloud metadata service blocking | 10.5.1 |
| MCP dynamic dispatch and reflective invocation prevention | 10.6.2 |
| Default-deny cross-domain agent discovery and calls | 9.8.1 |
| Origin and Host header validation for DNS rebinding defense | 10.3.4 |
| SSE public internet blocking | 10.3.3 |

**Common pitfalls:** allowing AI workloads to reach cloud metadata services; not logging egress traffic for forensic analysis; missing Origin header validation enabling DNS rebinding attacks.

---

## AD.12 Supply Chain & Artifact Integrity

Verify origin and authenticity, scan dependencies, and enforce integrity of models, frameworks, datasets, and build artifacts.

| Control / Technique | Requirement IDs |
|---|---|
| Model registry with AI BOM (SPDX, CycloneDX) | 3.1.1, 6.7.1 |
| Model dependency graph tracking (services, agents, environments) | 3.1.3 |
| Model origin records (source, training data checksums, authorship) | 3.1.4, 6.1.1 |
| Automated reproducible builds with SBOM | 4.2.1 |
| Reproducible build hash comparison | 6.3.5 |
| CI pipeline dependency scanning (AI frameworks, critical libraries) | 6.2.1 |
| Critical / high-severity vulnerability blocking in CI | 6.2.2 |
| Dependency version pinning with lockfile enforcement | 6.3.1 |
| Immutable digest references for containers (no mutable tags) | 6.3.2 |
| Expired and unmaintained dependency detection | 6.3.3 |
| Approved source and internal registry enforcement | 6.4.1 |
| Malicious layer and trojan trigger scanning | 6.1.2 |
| External dataset poisoning assessment (fingerprinting, outlier detection) | 6.5.1 |
| Copyright and PII detection in external datasets | 6.5.2 |
| Dataset origin and lineage documentation | 6.5.3 |
| Automated AI BOM generation and signing in CI | 6.7.2 |
| Build attestation retention | 6.3.4 |

**Common pitfalls:** using mutable `:latest` tags in production; not scanning fine-tuning datasets for poisoning; lacking rollback procedures when a compromised dependency is detected.

---

## AD.13 Deployment & Lifecycle Management

Manage model deployment, rollback, retirement, and emergency response.

| Control / Technique | Requirement IDs |
|---|---|
| Automated security testing gates before deployment | 3.2.1 |
| Agent workflow, tool, MCP, and RAG integration testing | 3.2.2 |
| Immutable audit records for model changes | 3.2.3 |
| Deployment validation with failure blocking and override approval | 3.2.4 |
| Signature and integrity checksum verification at deployment | 3.3.1 |
| Canary / blue-green deployments with automated rollback triggers | 3.3.2 |
| Atomic state restoration on rollback (weights, config, adapters, safety models) | 3.3.3 |
| Emergency model shutdown capability with pre-defined response time | 3.3.4 |
| Shutdown cascade to tools, MCP, RAG, credentials, memory stores | 3.3.5 |
| Development / test / production environment separation | 3.4.1 |
| Version control for all development artifacts (hyperparams, scripts, prompts, policies) | 3.4.2 |
| Secure model artifact wiping and cryptographic erasure on retirement | 3.5.1 |
| Model signature revocation and registry deny-list on retirement | 3.5.2 |
| Supply chain incident response playbooks (model and library rollback) | 6.6.1 |

**Common pitfalls:** not testing rollback procedures before they are needed; leaving retired model artifacts in serving caches; missing shutdown cascade to downstream tool and MCP connections.

---

## AD.14 Privacy & Data Minimization

Protect personal data and enforce data subject rights throughout the AI lifecycle.

| Control / Technique | Requirement IDs |
|---|---|
| Training data minimization (exclude unnecessary features, PII, leaked test data) | 1.1.2 |
| Labeled data anonymization and granular redaction | 1.3.4 |
| Direct and quasi-identifier removal | 12.1.1 |
| k-anonymity and l-diversity measurement with automated audits | 12.1.2 |
| Synthetic data with formal re-identification risk bounds | 12.1.4 |
| Data deletion propagation (datasets, checkpoints, embeddings, logs, backups) | 12.2.1 |
| Machine unlearning with certified algorithms | 12.2.2 |
| Shadow-model evaluation of unlearning effectiveness | 12.2.3 |
| Privacy-loss accounting with epsilon budget tracking and alerts | 12.3.1 |
| Formal differential privacy proofs (including post-training and embeddings) | 12.3.3 |
| Purpose tags with machine-readable alignment and runtime enforcement | 12.4.1, 12.4.2 |
| Consent Management Platform (CMP) with opt-in tracking | 12.5.1 |
| Consent withdrawal processing (< 24 hour SLA) | 12.5.3 |
| Local differential privacy in federated learning (client-side noise) | 12.6.1 |
| Poisoning-resistant aggregation (Krum, Trimmed-Mean) | 12.6.3 |
| PII detection and removal in external datasets | 6.5.2 |

**Common pitfalls:** deleting records from the database but not from model checkpoints or embeddings; not accounting for epsilon budget accumulation across queries; treating anonymization as a one-time step.

---

## AD.15 Adversarial Testing & Model Hardening

Test for and defend against evasion, extraction, inversion, poisoning, and alignment bypass attacks.

| Control / Technique | Requirement IDs |
|---|---|
| Refusal and safe-completion guardrails | 11.1.1 |
| Red-team and jailbreak test suites (version-controlled) | 11.1.2 |
| Automated harmful-content rate evaluation with regression detection | 11.1.3 |
| RLHF / Constitutional AI alignment training | 11.1.4 |
| Adversarial training and defensive distillation | 11.2.3, 2.2.4 |
| Formal robustness verification (certified bounds, interval-bound propagation) | 11.2.5 |
| Adversarial-example detection with production alerting | 11.2.2 |
| Output calibration and perturbation for privacy | 11.3.1 |
| DP-SGD (differentially private training) with documented epsilon | 11.3.2 |
| Membership inference attack simulation (shadow-model, likelihood-ratio) | 11.3.3 |
| Model extraction detection (query-pattern analysis, diversity measurement) | 11.5.3 |
| Statistical outlier and consistency scoring on external inputs | 11.6.1 |
| Adaptive attack evasion testing | 11.6.4 |
| Security-focused secondary review mechanisms (second model, rule-based) | 11.8.1 |
| Self-modification restriction with scope bounds and rate limits | 11.9.1, 11.9.4 |
| Data augmentation with perturbed inputs for training robustness | 1.4.4 |

**Common pitfalls:** testing only known jailbreak patterns without adaptive attacks; not updating red-team suites after model updates; relying on a single defense without defense-in-depth.

---

## AD.16 Logging & Audit

Capture security-relevant events with integrity protection for forensic analysis and compliance.

| Control / Technique | Requirement IDs |
|---|---|
| Prompt and response logging with metadata (timestamp, user ID, session, model version) | 13.1.1 |
| Secure, access-controlled log repositories with retention policies | 13.1.2 |
| Log encryption at rest and in transit | 13.1.3 |
| PII, credential, and proprietary information redaction in logs | 13.1.4 |
| Policy decision and safety filtering action logging | 13.1.5 |
| Cryptographic log signatures with write-only storage | 13.1.6 |
| Tamper-evident audit logs with full reconstruction context (who, what, when) | 9.4.3 |
| Agent action signing with chain ID binding and timestamps | 9.4.2 |
| Immutable audit records for model changes (actor, change type, before/after) | 3.2.3 |
| Immutable deletion logging for regulatory audit trails | 12.2.4 |
| CI/CD audit log streaming to SIEM | 6.6.2 |
| DAG visualization with access controls and tamper evidence | 13.7.1, 13.7.2, 13.7.3 |
| Safety violation metrics logging | 7.6.1 |
| MCP policy change audit logging (timestamp, author, justification) | 11.7.3 |

**Common pitfalls:** logging prompts without redacting PII; using mutable log storage without integrity protection; not including sufficient context for forensic reconstruction.

---

## AD.17 Monitoring, Alerting & Incident Response

Detect anomalies, alert on threats, and respond to security incidents in AI systems.

| Control / Technique | Requirement IDs |
|---|---|
| Jailbreak and prompt injection attempt detection (signature-based) | 13.2.1 |
| SIEM integration with standard log formats | 13.2.2 |
| AI-specific event enrichment (model ID, confidence, filter decisions) | 13.2.3 |
| Behavioral anomaly detection (unusual patterns, excessive retries, systematic probing) | 13.2.4, 13.2.5 |
| Real-time alerting on policy violations and coordinated attack campaigns | 13.2.6 |
| Automated incident response (isolation, blocking, escalation) | 13.2.7 |
| Performance metric monitoring (accuracy, latency, error rate) with alerting | 13.3.1, 13.3.2 |
| Hallucination detection monitoring | 13.3.3 |
| Data drift and concept drift detection | 13.6.2, 13.6.3 |
| Model extraction alert generation with query metadata logging | 11.5.2 |
| Emergent multi-agent behavior detection (oscillation, deadlock, broadcast storms) | 9.8.2 |
| AI-specific incident response plans (model compromise, data poisoning, adversarial attack) | 13.5.1 |
| AI-specific forensic tools for model behavior investigation | 13.5.2 |
| Safety violation rate alerting | 7.6.2 |
| Real-time security policy updates without full redeployment | 11.7.1 |
| Accelerator telemetry and side-channel anomaly detection | 4.7.8 |
| Proactive agent behavior validation with risk assessment | 13.8.1, 13.8.2 |

**Common pitfalls:** not correlating AI-specific events with broader SIEM alerts; treating model drift as a scheduled check rather than continuous monitoring; lacking AI-specific forensic tooling during incident response.

---

## AD.18 Explainability & Transparency

Enable human understanding of model decisions through interpretability, documentation, and uncertainty quantification.

| Control / Technique | Requirement IDs |
|---|---|
| Human-readable decision explanations | 14.4.1 |
| Explanation quality validation (human evaluation studies) | 14.4.2 |
| SHAP, LIME, and feature importance scores | 14.4.3 |
| Counterfactual explanations | 14.4.4 |
| Model cards (intended use, known failures, performance metrics) | 14.5.1, 14.5.2 |
| Ethical considerations and bias assessment documentation | 14.5.3 |
| Model card version control and change tracking | 14.5.4 |
| Uncertainty quantification (confidence scores, entropy measures) | 14.6.1 |
| Human review triggers on uncertainty thresholds | 14.6.2 |
| Uncertainty calibration against ground truth | 14.6.3 |
| Multi-step uncertainty propagation | 14.6.4 |
| Model interpretability artifacts (attention maps, attribution) | 7.5.3 |
| Confidence and reasoning summary display | 7.5.2 |

**Common pitfalls:** providing explanations that expose system prompts or internal architecture; not calibrating uncertainty estimates; treating model cards as static documents rather than living artifacts.

---

## AD.19 Human Oversight & Approval Gates

Require human review and approval for high-impact, irreversible, or safety-critical actions.

| Control / Technique | Requirement IDs |
|---|---|
| High-impact action approval gates (deploy, delete, financial, notify) | 9.2.1 |
| Approval parameter binding (prevent approve-one-execute-another) | 9.2.2 |
| High-impact intent confirmation with exact parameter binding and quick expiration | 9.7.2 |
| High-risk MCP action confirmation (data deletion, financial, system config) | 10.5.3 |
| Human approval for high-risk content generation | 7.3.5 |
| Human review on uncertainty threshold breach | 14.6.2 |
| Human review on anomaly detection | 11.6.3 |
| Enhanced monitoring and human intervention on security warnings | 11.8.3 |
| Security-critical proactive action approval with approval chain logging | 13.8.4 |
| High-risk model quarantine with human review and sign-off | 6.1.4 |
| Post-condition outcome checking with containment on mismatch | 9.7.3 |
| Compensating actions and transactional rollback on failure | 9.2.3 |

**Common pitfalls:** not binding approval to exact parameters allowing bait-and-switch; confirmation tokens without quick expiration; missing post-condition checks after approved actions execute.

---

## AD.20 Hardware & Accelerator Security

Secure AI accelerator hardware, firmware, memory, interconnects, and edge devices.

| Control / Technique | Requirement IDs |
|---|---|
| GPU/TPU integrity validation with hardware attestation (TPM, DRTM) | 4.7.1 |
| GPU memory isolation and sanitization between workloads and tenants | 4.7.2 |
| Signed GPU firmware with version pinning and attestation | 4.7.3 |
| VRAM zeroing and device reset between jobs | 4.7.4 |
| MIG / VM GPU partitioning with peer-to-peer access prevention | 4.7.5 |
| HSM with FIPS 140-3 Level 3 certification | 4.7.6 |
| Authenticated accelerator interconnects (NVLink, PCIe, InfiniBand, RDMA) | 4.7.7 |
| Accelerator telemetry export (power, temperature, error correction) | 4.7.8 |
| Edge device secure boot with firmware rollback protection | 4.8.3 |
| Model signature verification on edge devices | 4.8.2 |
| Mobile verified boot, code signing, and runtime integrity checks | 4.8.4 |
| Byzantine fault-tolerant consensus for distributed AI | 4.8.5 |
| On-device process, memory, and file access isolation | 4.8.7 |
| Model obfuscation and decryption inside trusted runtime | 4.8.9 |

**Common pitfalls:** not zeroing VRAM between tenant workloads; running debug firmware in production; allowing unencrypted interconnects in multi-tenant GPU clusters; neglecting firmware update attestation.

---

### References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)
