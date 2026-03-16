# Appendix D: AI Security Controls Inventory

## Objective

This appendix provides a concise inventory of every security control and defense technique referenced across the AISVS core requirements (C01--C14). Implementers can use this as a cross-reference to understand which defenses are needed and where they appear in the standard. Controls are grouped by security domain.

---

## AD.1 Cryptography & Key Management

Protect data confidentiality and integrity across the AI lifecycle through encryption, signing, and key management.

**Threats mitigated:** model tampering, data exfiltration, man-in-the-middle attacks, unauthorized artifact modification.

| Control / Technique | Requirement IDs |
|---|---|
| Encryption at rest and in transit for training data | 1.2.3, 1.3.4 |
| Cryptographic hashes for data integrity | 1.2.4, 1.3.2 |
| Cryptographic signatures on models and artifacts | 3.1.2, 4.2.2, 6.1.1 |
| Hardware-backed key storage (HSM, KMS) | 4.4.4, 4.7.6 |
| Secrets management with encryption at rest | 4.4.1 |
| Automated key and secret rotation | 4.4.5, 9.4.4 |
| Mutual TLS with certificate validation | 4.3.4, 9.5.1 |
| Immutable audit logs (append-only / WORM) | 9.4.3, 13.1.6 |
| Model watermarking and fingerprinting | 7.7.5, 11.5.4 |
| Signed JWT tokens for agent authentication | 5.1.3 |
| Message integrity with cryptographic signatures | 9.4.2, 9.5.3 |
| Cryptographic log signatures | 13.1.6 |

**Common pitfalls:** hardcoded secrets in config or images; using mutable tags instead of immutable digests for container references; neglecting key rotation schedules.

---

## AD.2 Authentication & Authorization

Establish and enforce identity, access control, and delegation across users, agents, and services.

**Threats mitigated:** unauthorized access, privilege escalation, cross-tenant data leakage, agent impersonation.

| Control / Technique | Requirement IDs |
|---|---|
| Centralized identity provider (OIDC, SAML) | 5.1.1 |
| Multi-factor authentication for high-risk operations | 5.1.2 |
| OAuth 2.1 for MCP client/server authentication | 10.2.1, 10.2.2 |
| RBAC / ABAC / zero-trust authorization | 5.2.1, 5.2.7 |
| Policy decision engines (OPA, Cedar) | 5.2.6 |
| Row-level security and field-level masking | 5.3.3 |
| Scoped capability tokens for agents | 5.6.1 |
| Least-privilege resource access | 5.2.1, 5.6.2 |
| Continuous authorization re-evaluation | 9.6.3 |
| Delegation context propagation (user, tenant, scopes) | 9.6.2 |
| Unique cryptographic agent identity | 9.4.1 |
| Session-based authorization binding | 5.5.2 |
| Tenant isolation through cryptographic keys | 5.5.4 |

**Common pitfalls:** reusing end-user credentials for agent-to-agent calls; granting broad OAuth scopes instead of minimal required scopes; not re-evaluating authorization when context changes mid-session.

---

## AD.3 Input Validation & Injection Defense

Validate, normalize, and constrain all inputs before they reach models or downstream systems.

**Threats mitigated:** prompt injection, jailbreak, encoding smuggling, adversarial perturbation, resource exhaustion.

| Control / Technique | Requirement IDs |
|---|---|
| Prompt injection detection ruleset / service | 2.1.1 |
| Instruction hierarchy enforcement (system > developer > user) | 2.1.2 |
| Third-party content sanitization | 2.1.3 |
| Unicode NFC normalization and homoglyph mapping | 2.2.1 |
| Control / invisible character removal | 2.2.1, 2.2.5 |
| Statistical and embedding-distance anomaly detection | 2.2.3 |
| Schema validation (JSON Schema, Protocol Buffers) | 2.4.1, 7.1.1 |
| Token and byte limit enforcement | 2.4.2 |
| Character set allow-listing | 2.3.1, 2.3.2 |
| Content classifiers (hate, violence, sexual, illegal) | 2.5.1 |
| Multi-modal input validation (images, audio, files) | 2.7.1 |
| Malware and steganography scanning | 2.7.2 |
| Adversarial perturbation detection | 2.7.3 |
| Cross-modal attack detection | 2.7.5 |
| Pattern matching (regex) on inputs and outputs | 2.8.1 |
| Adaptive detection models | 2.8.2 |
| MCP input validation and schema enforcement | 10.4.2, 10.4.3, 10.4.4 |

**Common pitfalls:** validating only text modality while ignoring image/audio channels; relying solely on regex without semantic detection; not applying validation to tool outputs before they re-enter agent context.

---

## AD.4 Output Controls

Constrain, filter, and validate model outputs before they reach users or downstream systems.

**Threats mitigated:** hallucination, data leakage, PII exposure, harmful content generation, injection via output.

| Control / Technique | Requirement IDs |
|---|---|
| Output format schema validation | 7.1.1 |
| Stop sequences and token limits | 7.1.2 |
| Parameterized queries and safe deserializers | 7.1.3 |
| Confidence scoring and uncertainty estimation | 7.2.1 |
| Confidence threshold gating with fallback messages | 7.2.2 |
| Output safety classifiers | 7.3.1 |
| PII detection and redaction | 7.3.2, 7.3.3, 5.4.1 |
| Human approval for high-risk content | 7.3.5 |
| System prompt removal from explanations | 7.5.1 |
| AI-generated media watermarking | 7.7.5 |
| Copyright violation detection | 7.7.3 |
| Citation and attribution validation | 5.4.2 |
| Output format restriction by permission level | 5.4.3 |
| Classification label propagation | 5.2.4 |

**Common pitfalls:** redacting PII in text but not in structured data fields; not enforcing stop sequences on streaming outputs; trusting model confidence scores without calibration.

---

## AD.5 Rate Limiting & Execution Budgets

Enforce resource consumption bounds to prevent abuse, runaway agents, and denial-of-service.

**Threats mitigated:** resource exhaustion, model extraction, denial of service, runaway agent loops, cost overruns.

| Control / Technique | Requirement IDs |
|---|---|
| Per-user, per-IP, per-API-key rate limits | 2.6.1 |
| Burst and sustained rate limiting | 2.6.2 |
| Per-agent token, cost, and tool-call budgets | 2.6.2, 9.1.1 |
| Recursion depth and concurrency limits | 9.1.1 |
| Wall-clock time and monetary spend caps | 9.1.1 |
| Cumulative resource counters with hard-stop | 9.1.2 |
| Circuit breaker enforcement | 9.1.3 |
| Per-tool CPU, memory, disk, egress, and time limits | 9.3.2 |
| Query-rate limiting for model extraction defense | 11.4.2, 11.5.1 |
| MCP outbound execution limits, timeouts, and circuit breakers | 10.5.2 |
| Anomalous usage pattern detection and blocking | 2.6.3 |

**Common pitfalls:** setting rate limits per-endpoint but not per-agent-session; not accounting for tool fan-out when calculating budgets; missing circuit breakers on recursive agent chains.

---

## AD.6 Infrastructure & Isolation

Harden runtime environments and enforce isolation boundaries between workloads, environments, and tenants.

**Threats mitigated:** container escape, privilege escalation, lateral movement, data cross-contamination, supply chain compromise at deployment.

| Control / Technique | Requirement IDs |
|---|---|
| Minimal OS permissions and Linux capabilities | 4.1.1 |
| Sandboxing (seccomp, AppArmor, SELinux) | 4.1.2 |
| Read-only root filesystem | 4.1.3 |
| TEE / confidential computing with remote attestation | 4.1.5, 4.5.4, 4.5.6 |
| Automated reproducible builds with SBOM | 4.2.1 |
| Signed build artifacts with provenance metadata | 4.2.2 |
| Default-deny network policies and egress allow-lists | 4.3.1, 4.3.5 |
| Network segmentation (dev / test / prod) | 4.3.2, 3.4.1 |
| Secrets isolation and runtime injection | 4.4.1, 4.4.3 |
| Untrusted model sandboxing | 4.5.1, 4.5.2 |
| Resource quotas (CPU, memory, GPU) | 4.6.1 |
| Isolated backup infrastructure (air-gapped / WORM) | 4.6.3 |
| Tool and plugin sandboxing (container, VM, WASM) | 9.3.1 |
| Agent isolation across tenants and environments | 9.8.1 |

**Common pitfalls:** sharing infrastructure between dev and prod; not restricting cloud metadata service access; granting containers more capabilities than needed.

---

## AD.7 Model Integrity & Supply Chain

Verify provenance, integrity, and safety of models, frameworks, datasets, and dependencies throughout the supply chain.

**Threats mitigated:** model poisoning, trojan insertion, dependency hijacking, unsigned artifact deployment, supply chain compromise.

| Control / Technique | Requirement IDs |
|---|---|
| Model registry with AI BOM (SPDX, CycloneDX) | 3.1.1, 6.7.1 |
| Cryptographic model signing and verification | 3.1.2, 6.4.2 |
| Model dependency graph tracking | 3.1.3 |
| Model provenance records (origin, training data checksums, authorship) | 3.1.4, 6.1.1 |
| Automated security testing gates (input validation, output sanitization, safety) | 3.2.1 |
| Immutable audit records for model changes | 3.2.3 |
| Deployment validation with failure blocking | 3.2.4 |
| Canary / blue-green deployments with automated rollback | 3.3.2 |
| Emergency model shutdown capability | 3.3.4 |
| CI pipeline dependency scanning | 6.2.1 |
| Dependency version pinning and lockfile enforcement | 6.3.1 |
| Immutable digest references for containers | 6.3.2 |
| Approved source and internal registry enforcement | 6.4.1 |
| External dataset poisoning assessment | 6.5.1 |
| Malicious layer and trojan trigger scanning | 6.1.2 |
| Supply chain incident response playbooks | 6.6.1 |
| Automated AI BOM generation in CI | 6.7.2 |

**Common pitfalls:** using mutable `:latest` tags in production; not scanning fine-tuning datasets for poisoning; lacking rollback procedures when a compromised model is detected.

---

## AD.8 Privacy Techniques

Protect personal data and prevent re-identification throughout training, inference, and data lifecycle.

**Threats mitigated:** re-identification, membership inference, data subject rights violations, federated learning poisoning, consent violations.

| Control / Technique | Requirement IDs |
|---|---|
| Direct and quasi-identifier removal | 12.1.1 |
| k-anonymity and l-diversity measurement | 12.1.2 |
| Synthetic data with re-identification risk bounds | 12.1.4 |
| Data deletion propagation (datasets, checkpoints, embeddings, logs) | 12.2.1 |
| Machine unlearning (certified algorithms) | 12.2.2 |
| Privacy-loss accounting (epsilon budget tracking) | 12.3.1 |
| Formal differential privacy proofs | 12.3.3 |
| Purpose tags with machine-readable alignment | 12.4.1 |
| Consent Management Platform (CMP) with opt-in tracking | 12.5.1 |
| Consent withdrawal processing (< 24 hour SLA) | 12.5.3 |
| Local differential privacy in federated learning | 12.6.1 |
| Poisoning-resistant aggregation (Krum, Trimmed-Mean) | 12.6.3 |
| PII detection and removal in training data | 1.1.2, 6.5.2 |
| Labeled data anonymization and encryption | 1.3.4 |

**Common pitfalls:** deleting records from the database but not from model checkpoints or embeddings; not accounting for epsilon budget accumulation across multiple queries; treating anonymization as a one-time step rather than continuous measurement.

---

## AD.9 Adversarial Robustness

Harden models against evasion, extraction, inversion, and poisoning attacks.

**Threats mitigated:** model evasion, model extraction, model inversion, data poisoning, alignment bypass, jailbreak.

| Control / Technique | Requirement IDs |
|---|---|
| Refusal and safe-completion guardrails | 11.1.1 |
| Red-team and jailbreak test suites (version-controlled) | 11.1.2 |
| Automated harmful-content rate evaluation | 11.1.3 |
| RLHF / Constitutional AI alignment training | 11.1.4 |
| Adversarial training and defensive distillation | 11.2.3, 2.2.4 |
| Formal robustness verification (certified bounds) | 11.2.5 |
| Adversarial-example detection with alerting | 11.2.2 |
| Output calibration and perturbation for privacy | 11.3.1 |
| DP-SGD (differentially private training) | 11.3.2 |
| Membership inference attack simulation | 11.3.3 |
| Model extraction rate limiting and detection | 11.5.1, 11.5.2, 11.5.3 |
| Model watermarking and fingerprinting | 11.5.4 |
| Statistical outlier and consistency scoring | 11.6.1 |
| Real-time security policy updates (no full redeployment) | 11.7.1 |
| Security-focused secondary review mechanisms | 11.8.1 |
| Self-modification restriction and scope bounds | 11.9.1, 11.9.4 |

**Common pitfalls:** testing only known jailbreak patterns without adaptive attacks; not updating red-team suites after model updates; relying on a single robustness defense without defense-in-depth.

---

## AD.10 Detection & Monitoring

Detect security events, performance degradation, and model drift through logging, alerting, and analysis.

**Threats mitigated:** undetected attacks, silent model degradation, data drift, compliance violations, incident response delays.

| Control / Technique | Requirement IDs |
|---|---|
| Prompt and response logging with metadata | 13.1.1 |
| Secure, access-controlled, encrypted log storage | 13.1.2, 13.1.3 |
| PII and credential redaction in logs | 13.1.4 |
| Jailbreak and prompt injection attempt detection | 13.2.1 |
| SIEM integration with standard log formats | 13.2.2 |
| AI-specific event enrichment (model ID, confidence, filter decisions) | 13.2.3 |
| Behavioral anomaly detection (unusual patterns, excessive retries) | 13.2.4 |
| Real-time alerting on policy violations and attack attempts | 13.2.5, 13.2.6 |
| Automated incident response (isolation, blocking, escalation) | 13.2.7 |
| Performance metric monitoring (accuracy, latency, error rate) | 13.3.1, 13.3.2 |
| Hallucination detection monitoring | 13.3.3 |
| Data drift and concept drift detection | 13.6.2, 13.6.3 |
| DAG visualization with access controls and tamper evidence | 13.7.1, 13.7.2, 13.7.3 |

**Common pitfalls:** logging prompts without redacting PII; not correlating AI-specific events with broader SIEM alerts; treating model drift as a scheduled check rather than continuous monitoring.

---

## AD.11 Explainability & Transparency

Enable human understanding of model decisions through interpretability, documentation, and uncertainty quantification.

**Threats mitigated:** opaque decision-making, undetected bias, regulatory non-compliance, misplaced trust in uncertain outputs.

| Control / Technique | Requirement IDs |
|---|---|
| Human-readable decision explanations | 14.4.1 |
| Explanation quality validation (human evaluation studies) | 14.4.2 |
| SHAP, LIME, and feature importance scores | 14.4.3 |
| Counterfactual explanations | 14.4.4 |
| Model cards (intended use, known failures, performance metrics) | 14.5.1, 14.5.2 |
| Ethical considerations and bias assessment documentation | 14.5.3 |
| Model card version control | 14.5.4 |
| Uncertainty quantification (confidence scores, entropy measures) | 14.6.1 |
| Human review triggers on uncertainty thresholds | 14.6.2 |
| Uncertainty calibration against ground truth | 14.6.3 |
| Multi-step uncertainty propagation | 14.6.4 |
| Model interpretability artifacts (attention maps, attribution) | 7.5.3 |
| Confidence and reasoning summary display | 7.5.2 |

**Common pitfalls:** providing explanations that expose system prompts or internal architecture; not calibrating uncertainty estimates; treating model cards as static documents rather than living artifacts.

---

## AD.12 Agent & Orchestration

Secure multi-agent systems, tool integrations, and autonomous workflows through identity, authorization, and containment.

**Threats mitigated:** agent impersonation, tool abuse, runaway execution, privilege escalation across delegation chains, emergent unsafe behavior.

| Control / Technique | Requirement IDs |
|---|---|
| Per-execution budget enforcement (tokens, cost, time, recursion) | 9.1.1, 9.1.2 |
| Circuit breaker enforcement | 9.1.3 |
| High-impact action approval gates (deploy, delete, financial, notify) | 9.2.1 |
| Approval parameter binding (prevent approve-one-execute-another) | 9.2.2 |
| Compensating actions and transactional rollback | 9.2.3 |
| Tool and plugin sandboxing (container, VM, WASM) | 9.3.1 |
| Tool output schema and security policy validation | 9.3.3 |
| Tool binary integrity verification (signatures, checksums) | 9.3.4 |
| Tool manifest declaration (privileges, side-effects, limits) | 9.3.5 |
| Unique cryptographic agent identity | 9.4.1 |
| Execution chain cryptographic signing | 9.4.2 |
| Tamper-evident audit logs with full reconstruction context | 9.4.3 |
| Fine-grained agent action authorization (tool, parameters, resources) | 9.6.1 |
| Delegation context propagation with integrity protection | 9.6.2 |
| Pre-execution policy constraint gates | 9.7.1 |
| Post-condition outcome checking | 9.7.3 |
| Cross-tenant and cross-environment agent isolation | 9.8.1 |
| Emergent behavior detection (oscillation, deadlock, broadcast storms) | 9.8.2 |

**Common pitfalls:** reusing user credentials for agent-to-agent auth; not binding approval to exact parameters; missing post-condition checks after tool execution; ignoring emergent behavior in multi-agent compositions.

---

## AD.13 MCP Security

Secure Model Context Protocol integrations through authentication, transport, validation, and boundary enforcement.

**Threats mitigated:** unauthorized MCP server access, tool definition tampering, token theft, DNS rebinding, cross-tenant data access, chained side effects.

| Control / Technique | Requirement IDs |
|---|---|
| MCP component signature and checksum verification | 10.1.1 |
| Runtime credential injection (no plaintext secrets) | 10.1.2 |
| OAuth 2.1 authentication for MCP clients and servers | 10.2.1, 10.2.2 |
| MCP server registration with explicit ownership | 10.2.3 |
| Scope-filtered tool discovery (tools/list) | 10.2.6 |
| Per-tool invocation access control | 10.2.7 |
| Token proxying prevention (on-behalf-of / client credentials) | 10.2.9 |
| Minimum scope requests and wildcard rejection | 10.2.11 |
| Authenticated streamable-HTTP transport with TLS 1.3 | 10.3.1, 10.3.2 |
| Origin and Host header validation (DNS rebinding defense) | 10.3.4 |
| Tool response validation (prompt injection, context manipulation) | 10.4.1 |
| Schema integrity signing and tamper detection | 10.4.2, 10.4.5 |
| Message-framing integrity and payload size limits | 10.4.3 |
| Error response sanitization (no stack traces, tokens, paths) | 10.4.6 |
| Egress allow-list and cloud metadata service blocking | 10.5.1 |
| High-risk MCP action confirmation gates | 10.5.3 |
| Stdio local-only enforcement and terminal injection prevention | 10.6.1 |
| Dynamic dispatch and reflective invocation prevention | 10.6.2 |
| Tenant and environment boundary enforcement | 10.6.3 |

**Common pitfalls:** storing OAuth tokens in MCP server state; not validating tool definition hashes between invocations; allowing stdio transport across network boundaries; missing Origin header validation enabling DNS rebinding.

---

## AD.14 Hardware & Accelerator Security

Secure AI accelerator hardware, firmware, memory, and interconnects.

**Threats mitigated:** GPU memory leakage, firmware tampering, side-channel attacks, cross-tenant data exposure, interconnect eavesdropping.

| Control / Technique | Requirement IDs |
|---|---|
| GPU/TPU integrity validation with hardware attestation (TPM, DRTM) | 4.7.1 |
| GPU memory isolation and sanitization between workloads | 4.7.2 |
| Signed GPU firmware with version pinning and attestation | 4.7.3 |
| VRAM zeroing and device reset between jobs | 4.7.4 |
| MIG / VM partitioning with peer-to-peer access prevention | 4.7.5 |
| HSM with FIPS 140-3 Level 3 certification | 4.7.6 |
| Authenticated accelerator interconnects (NVLink, PCIe, InfiniBand) | 4.7.7 |
| Accelerator telemetry and side-channel anomaly detection | 4.7.8 |
| Edge device mutual authentication and secure boot | 4.8.1, 4.8.3 |
| Model signature verification on edge devices | 4.8.2 |
| On-device process, memory, and file access isolation | 4.8.7 |
| Hardware-backed key stores (Secure Enclave, Android Keystore, TPM) | 4.8.8 |
| Model encryption at rest on mobile with trusted runtime decryption | 4.8.9 |

**Common pitfalls:** not zeroing VRAM between tenant workloads; running debug firmware in production; allowing unencrypted interconnects in multi-tenant GPU clusters; neglecting firmware update attestation.

---

### References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023 -- AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)
