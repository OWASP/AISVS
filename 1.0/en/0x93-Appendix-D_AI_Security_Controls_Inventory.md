# Appendix D: AI Security Controls Inventory

## Objective

This appendix is a consolidated, developer-facing inventory of the security controls mandated across the AISVS requirements. Controls are grouped by control family so an implementer can find all related defenses in one place, regardless of which chapter defines them, and each control links back to the AISVS requirement IDs that mandate it.

This inventory is non-normative. It reorganizes existing requirements for ease of implementation and does not add, remove, or change any requirement. The requirement chapters (C1 through C12) remain the source of truth. Requirement IDs are written in canonical `C{chapter}.{section}.{requirement}` form (for example, `C5.1.1`). Every numbered requirement in the standard appears in exactly one control family below, so the inventory can be checked for completeness against the chapters.

---

## AD.1 Authentication & Identity

Verify the identity of users, agents, services, edge devices, and MCP clients/servers before granting access.

| Control / Technique | Requirement IDs |
| --- | --- |
| Step-up authentication for high-risk AI operations (model deployment, weight export, training-data access, production configuration changes) | C5.1.1 |
| Short-lived, minimal-scoped, cryptographically signed tokens for federated or multi-system agent authentication | C5.1.2 |
| Strong authentication of edge AI devices to central infrastructure | C4.3.1 |
| Unique cryptographic identity per agent instance, authenticating as a first-class principal to downstream systems | C9.4.1 |
| Scheduled rotation of agent identity credentials | C9.4.3 |
| MCP per-request access-token validation (not transport security alone) | C10.2.1 |
| MCP access-token claim validation (issuer, audience, expiration, scope) per OAuth 2.1 | C10.2.2 |
| MCP resource servers do not store or persist access tokens or user credentials | C10.2.3 |
| Removal of all MCP session artifacts on session termination | C10.2.6 |
| No pass-through of client access tokens to downstream APIs | C10.2.7 |
| Sender-constrained MCP access tokens (mTLS or DPoP) | C10.3.5 |

**Common pitfalls:** reusing end-user credentials for agent-to-agent calls; not rotating agent credentials on suspected compromise; treating transport security as a substitute for per-request token validation.

---

## AD.2 Authorization & Access Control

Enforce access decisions across users, agents, tools, and resources using policy that the model cannot override.

| Control / Technique | Requirement IDs |
| --- | --- |
| Access controls on every AI resource (datasets, endpoints, vector collections, embedding indices, compute) with explicit allow-lists and default-deny | C5.2.1 |
| End-user authorization context enforced at each retrieval and assembly stage, not the service account alone | C5.2.2 |
| Post-inference filtering so responses exclude data the requestor is not entitled to receive | C5.2.4 |
| Policy decision point isolated from the agent execution environment | C5.2.5 |
| Just-in-time privileged access to model weights, training pipelines, and production configuration with automatic expiry | C5.2.6 |
| Fine-grained, runtime-enforced authorization of agent actions (which tools, which parameter values) | C9.5.1 |
| Integrity-protected, scope-limited delegation token propagated to every downstream call | C9.5.2 |
| Access-control decisions enforced by application logic or a policy engine, never by the model | C9.5.3 |
| Inter-agent task delegation restricted by an explicit authorization policy | C9.5.5 |
| Re-evaluation of backend authorization on every privileged action in long-running sessions | C9.5.6 |
| Scope-filtered MCP tool discovery (tools/list returns only authorized tools) | C10.2.4 |
| Per-invocation MCP access control validating both the tool and the supplied argument values | C10.2.5 |

**Common pitfalls:** relying on the service account's permissions instead of the caller's; letting model-generated output drive authorization; not re-checking authorization when context changes mid-session.

---

## AD.3 Data Classification & Tenant Isolation

Keep data within its authorization and tenancy boundaries as it flows through AI-specific transformations and shared infrastructure.

| Control / Technique | Requirement IDs |
| --- | --- |
| Sensitive data served through retrieval pipelines rather than persisted into model weights | C5.2.3 |
| Classification labels propagated to downstream resources (embeddings, prompt caches, model outputs) | C5.2.7 |
| Cross-tenant isolation in shared model serving (fine-tuning, inference, embedding operations) | C5.3.1 |
| Cross-tenant isolation across shared compute (hardware partitioning, confidential computing, or dedicated allocation) | C5.3.2 |

**Common pitfalls:** dropping classification labels when data is embedded or cached; assuming logical multi-tenancy is sufficient against side channels in shared inference caches.

---

## AD.4 Encryption & Data Protection

Protect data and secrets at rest, in transit, and in the model's observable context.

| Control / Technique | Requirement IDs |
| --- | --- |
| Integrity protection of training data while stored and transferred | C1.1.4 |
| Redaction, anonymization, or encryption of sensitive information in labels before use in any labeling artifact | C1.2.3 |
| Encryption of locally stored model weights and sensitive parameters using hardware-backed key stores or secure enclaves | C4.3.4 |
| Encryption at rest of models packaged in mobile, IoT, or embedded apps, decrypted only inside a trusted runtime or secure enclave | C4.3.5 |
| Secrets and credentials kept out of the model's observable context (context window, system prompts, tool-call parameters) | C9.5.4 |

**Common pitfalls:** encrypting the database but not model checkpoints or embeddings; leaving model weights extractable from an app package; exposing API keys inside tool-call parameters.

---

## AD.5 Integrity, Signing & Provenance

Verify authenticity and detect tampering of models, artifacts, messages, tool definitions, and generated media.

| Control / Technique | Requirement IDs |
| --- | --- |
| Integrity monitoring of training data against unauthorized modification or corruption | C1.1.5 |
| Cryptographic integrity for labeling artifacts | C1.2.2 |
| Cryptographic signing of all model artifacts (weights, configs, tokenizers, base models, fine-tunes, adapters, safety/policy models) | C3.1.2 |
| Signature verification at deployment admission and on load | C3.1.3 |
| Signed edge/mobile model packages with on-device signature or checksum validation before load | C4.3.2 |
| Cryptographic binding of agent-initiated actions to each step of the execution chain for non-repudiation | C9.4.2 |
| Integrity protection of agent state persisted between invocations | C9.4.4 |
| Signed MCP tool responses with a unique nonce and timestamp for replay defense | C10.4.6 |
| Tool-definition snapshotting with re-approval required on any change before invocation | C10.4.7 |
| Watermarking of AI-generated media to prove it was AI-generated | C7.4.4 |

**Common pitfalls:** using mutable tags instead of immutable digests; not re-verifying tool definitions between MCP invocations; missing replay protection on tool responses.

---

## AD.6 Input Validation & Sanitization

Validate, normalize, and constrain all inputs (including tool, MCP, and retrieved content) before they reach the model or downstream systems.

| Control / Technique | Requirement IDs |
| --- | --- |
| Input normalization applied before tokenization or embedding | C2.1.1 |
| Encoding and representation-smuggling detection and mitigation (canonicalization, strict schema validation, policy-based rejection, or explicit marking) | C2.1.2 |
| Untrusted-input screening by a prompt-injection detection ruleset or classifier, with blocking | C2.1.3 |
| Input length controls that reject (not truncate) content exceeding the context window | C2.1.4 |
| Allow-list character-set restriction on all inputs | C2.1.5 |
| Instruction hierarchy enforcement (system and developer messages override user and untrusted input) | C2.1.6 |
| Reserved special tokens encoded as literal characters and not injectable into context | C2.1.7 |
| Many-shot jailbreaking pattern detection | C2.1.8 |
| Adversarial-perturbation, steganography, and hidden-content checks on non-text inputs (image, video, audio) | C2.2.3 |
| Cross-modal coordinated attack detection | C2.2.4 |
| Schema validation of tool outputs | C9.3.2 |
| Verification of external resources named in model output against an approved allow-list or registry before install or invocation | C9.3.7 |
| MCP response schema validation before injection into model context | C10.4.1 |
| Indirect-prompt-injection screening of MCP responses before injection into model context | C10.4.2 |
| Rejection of unrecognized or oversized MCP function-call parameters | C10.4.3 |
| Strict MCP schema validation | C10.4.4 |
| Maximum MCP payload size limits | C10.4.5 |
| Anomaly detection on external or untrusted inputs before inference | C11.4.1 |
| Gating actions on inputs flagged as anomalous | C11.4.2 |

**Common pitfalls:** validating only the text modality while ignoring image/audio channels; relying on regex alone without semantic detection; not validating tool and MCP outputs before they re-enter agent context.

---

## AD.7 Inbound Content & Policy Screening

Screen prompts and training content against policy before they reach the model or the training pipeline.

| Control / Technique | Requirement IDs |
| --- | --- |
| Inbound content classification (violence, self-harm, hate, sexual) against configurable thresholds, with rejection or sanitization before model context | C2.2.1 |
| Evaluation of content classification for languages that are not supported | C2.2.2 |
| Detection and removal of disallowed content before training | C1.3.4 |

**Common pitfalls:** deploying classifiers tuned only for one language; screening prompts but not the training corpus.

---

## AD.8 Output Handling & Safety

Constrain, filter, and validate model outputs before they reach users or downstream systems.

| Control / Technique | Requirement IDs |
| --- | --- |
| Schema validation of model outputs with rejection on mismatch | C7.1.1 |
| Length limits and termination controls on generated output | C7.1.2 |
| Confidence or uncertainty estimation for generated answers | C7.2.1 |
| Automatic blocking or fallback when confidence drops below a defined threshold | C7.2.2 |
| Additional verification step for responses classified as high-risk by policy | C7.2.3 |
| Automated classifiers that scan responses and block defined harmful-content categories | C7.3.1 |
| Detection and blocking of responses that disclose system prompt content or backend data | C7.3.2 |
| Prevention of model-generated output triggering outbound requests | C7.3.3 |
| Detection of hidden, encoded, or misleading output (homoglyphs, formatting, metadata, structured fields) | C7.3.4 |

**Common pitfalls:** enforcing stop sequences in batch mode but not on streaming output; leaking the system prompt through paraphrase; treating a confidence score as available when the provider does not expose one.

---

## AD.9 Rate Limiting, Budgets & Resource Control

Bound consumption to prevent abuse, runaway execution, denial of service, and model extraction.

| Control / Technique | Requirement IDs |
| --- | --- |
| Per-tool quotas and timeouts (CPU, memory, disk, egress, execution time) | C9.1.1 |
| Per-execution budgets (maximum recursion depth, token use, monetary spend) enforced by the runtime | C9.1.2 |
| Per-principal and global inference rate limits sized to the extraction threat model, not a generic API throttle | C11.2.2 |

**Common pitfalls:** rate-limiting per endpoint but not per agent session; ignoring tool fan-out when sizing budgets; treating extraction defense as ordinary throttling.

---

## AD.10 Sandboxing & Workload Isolation

Isolate models, tools, agents, and hardware workloads to contain failures and prevent lateral movement.

| Control / Technique | Requirement IDs |
| --- | --- |
| Execution of AI models in isolated sandboxes | C4.1.1 |
| Allow-list of serialization formats that do not permit code execution during deserialization | C4.1.2 |
| Workload attestation before model loading | C4.1.3 |
| Confidential inference protecting model weights at runtime through isolated execution | C4.1.4 |
| Trusted execution environment with hardware-enforced isolation, memory encryption, and integrity protection | C4.2.1 |
| GPU integrity validation via hardware attestation before each workload | C4.2.2 |
| GPU memory partitioning with sanitization between jobs | C4.2.3 |
| Version-pinned, signed, boot-attested accelerator firmware | C4.2.4 |
| Process, memory, and file-access isolation in edge inference runtimes | C4.3.3 |
| Least-privilege sandbox or isolation for each tool or plugin | C9.3.1 |
| Tool manifests declaring required privileges, resource limits, and output-validation requirements | C9.3.3 |
| Runtime enforcement of declared tool-manifest privileges and limits | C9.3.4 |
| Isolation of untrusted-data processing from tool-calling capability | C9.3.5 |
| Architectural separation of untrusted tool-output processing from agent operations | C9.3.6 |
| Least-privilege sandbox for locally launched MCP servers (restricted file system, network, system access) | C10.1.3 |
| AI-specific runtime components not shared across environment boundaries (development, staging, production) | C3.4.1 |
| Training and fine-tuning environments isolated from production | C3.4.2 |

**Common pitfalls:** sharing infrastructure between dev and prod; granting tool sandboxes more capability than needed; allowing untrusted data processing to reach tool-calling paths.

---

## AD.11 Network & Egress Control

Control network boundaries, transport security, and traffic flow for AI workloads and MCP integrations.

| Control / Technique | Requirement IDs |
| --- | --- |
| Authenticated, encrypted streamable HTTP for remote MCP transport | C10.3.1 |
| stdio MCP transport restricted to controlled local environments | C10.3.2 |
| Independent Origin and Host header validation on HTTP-based transports (DNS rebinding defense) | C10.3.3 |
| MCP client minimum protocol-version enforcement (downgrade defense) | C10.3.4 |
| Accelerator interconnects restricted to approved topologies and authenticated endpoints | C4.2.5 |

**Common pitfalls:** exposing stdio or SSE transports beyond the local host; skipping Origin/Host validation and enabling DNS rebinding; accepting downgraded protocol versions.

---

## AD.12 Supply Chain & Artifact Integrity

Verify origin and authenticity of models, datasets, frameworks, and MCP components, and maintain an AI bill of materials.

| Control / Technique | Requirement IDs |
| --- | --- |
| Model registry inventory of all deployed model artifacts and their origin | C3.1.1 |
| Malicious-code scanning of models before import | C6.1.1 |
| Approved-source-only download of model weights, datasets, and fine-tuning adapters | C6.1.2 |
| Integrity verification of every third-party model artifact | C6.1.3 |
| Behavioral acceptance test suite passed before promotion beyond development | C6.1.4 |
| Version-controlled, machine-readable AI BOM per model artifact (datasets, weights, licenses, data-origin statements) | C6.2.1 |
| Cryptographic signing of AI BOMs before deployment | C6.2.2 |
| Build-failing AI BOM completeness checks when component metadata is missing | C6.2.3 |
| MCP components obtained only from trusted sources and cryptographically verified | C10.1.1 |
| Allow-listed MCP servers only | C10.1.2 |

**Common pitfalls:** treating AI BOMs as static documents rather than signed, version-controlled artifacts; not scanning pretrained weights for backdoors; pulling models from unapproved registries.

---

## AD.13 Model Lifecycle, Deployment & Rollback

Manage model validation, deployment, rollback, and fine-tuning pipeline integrity.

| Control / Technique | Requirement IDs |
| --- | --- |
| Pre-deployment automated input-validation, safety-evaluation, and output-sanitization testing | C3.2.1 |
| Re-evaluation of post-training-quantized models against the same safety and alignment test suite before deployment | C3.2.2 |
| Security re-evaluation triggered by provider model, version, or routing changes | C3.2.3 |
| Rollout mechanisms with automated rollback triggers | C3.3.1 |
| Complete model-state restoration on rollback | C3.3.2 |
| Isolated runtime state for model versions running in parallel | C3.3.3 |
| Versioned, integrity-verified RLHF reward models before a training run | C3.5.1 |
| Detection of reward hacking or reward-model over-optimization in RLHF stages | C3.5.2 |
| Stage-by-stage integrity verification in multi-stage fine-tuning pipelines | C3.5.3 |
| Fine-tuning checkpoints registered as distinct artifacts | C3.5.4 |

**Common pitfalls:** not testing rollback before it is needed; leaving retired model artifacts in serving caches; treating reward models as static infrastructure rather than versioned, validated artifacts.

---

## AD.14 Training Data Integrity & Governance

Source, vet, and document training data so tampering, poisoning, and corruption can be detected and traced.

| Control / Technique | Requirement IDs |
| --- | --- |
| Data minimization to only the features, attributes, and fields required for the stated purpose | C1.1.1 |
| Up-to-date inventory of every training-data source (origin, responsible party, license, collection method, use constraints, processing history) | C1.1.2 |
| Dataset watermarking for usage attribution and detection of unauthorized use | C1.1.3 |
| Labeling-platform access controls restricting who can create, modify, or approve annotations | C1.2.1 |
| Poisoning detection in training and fine-tuning pipelines | C1.3.1 |
| Confidence thresholds and consistency checks on automatically generated labels | C1.3.2 |
| Bias evaluation for models used in security-relevant decisions | C1.3.3 |
| Defenses against clean-label poisoning attacks | C1.3.5 |
| Dataset lineage recording (transformations, augmentations, merges) | C12.6.1 |
| Logging of all labeling activities | C12.6.2 |
| Write-time tagging of every ingested document (source, writer identity, timestamp) | C12.6.4 |

**Common pitfalls:** not scanning fine-tuning datasets for poisoning; collecting more attributes than the purpose requires; losing dataset lineage across transformations and merges.

---

## AD.15 Memory, Embeddings & RAG Security

Harden vector stores, memory pipelines, and retrieval-augmented generation against leakage, poisoning, and fabricated provenance.

| Control / Technique | Requirement IDs |
| --- | --- |
| Per-tenant uniqueness of vector identifiers and namespaces, preventing cross-tenant collisions | C8.1.1 |
| Immutability of document metadata tags after the initial write | C8.1.2 |
| Scope constraints enforced on retrieval operations | C8.1.3 |
| Detection and masking, tokenization, or dropping of sensitive fields before embedding | C8.2.1 |
| Detection, rejection, or quarantine of retrieval-manipulation content before vectorization | C8.2.2 |
| Flagging and quarantine of outlier vectors before they enter production indices | C8.2.3 |
| Source validation before agent or tool outputs are written to trusted memory | C8.2.4 |
| Contradiction checks on new memory writes, with conflicts triggering alerts | C8.2.5 |
| Exclusion of expired vectors from retrieval results | C8.3.1 |
| Memory reset capability | C8.3.2 |
| Retention of quarantined content while excluding it from all retrieval results | C8.3.3 |
| Attribution of RAG responses to their source documents | C7.4.1 |
| RAG attributions derived from retrieval metadata, not generated by the model | C7.4.2 |
| Traceability of RAG claims to the retrieved chunk | C7.4.3 |

**Common pitfalls:** auto-writing tool output into trusted memory without validation; serving expired or quarantined vectors; letting the model fabricate citations instead of deriving them from retrieval metadata.

---

## AD.16 Adversarial Robustness & Privacy Defense

Test for and defend against evasion, membership inference, model inversion, extraction, and poisoning of the improvement loop.

| Control / Technique | Requirement IDs |
| --- | --- |
| Alignment and safety training or fine-tuning to suppress disallowed content categories | C11.1.1 |
| Version-controlled alignment test suite run on every model update or release | C11.1.2 |
| Evaluation against known adversarial attack techniques relevant to the modality | C11.1.3 |
| Hardening of models against adversarial inputs | C11.1.4 |
| Automated evaluator that measures harmful-content rate and flags regressions beyond a threshold | C11.1.5 |
| Suppression of directly returned model-inferred sensitive attributes | C11.2.1 |
| Output calibration to reduce overconfident predictions exploitable by inference attacks | C11.2.3 |
| Differentially-private optimization for training on sensitive datasets | C11.2.4 |
| Membership-inference attack simulation demonstrating accuracy no better than random guessing | C11.2.5 |
| Raw model outputs not exposed beyond the backend, with externally visible responses calibrated to extraction risk | C11.3.2 |
| Model watermarking or fingerprinting so unauthorized copies can be identified | C11.3.3 |
| Poisoning detection and human review gates protecting the safety-violation feedback pipeline | C11.4.3 |

**Common pitfalls:** testing only known jailbreak patterns without adaptive attacks; not re-running the alignment suite after model updates; exposing raw confidence vectors that accelerate extraction.

---

## AD.17 Logging & Audit

Capture security-relevant events with sufficient context and integrity for forensic reconstruction and accountability.

| Control / Technique | Requirement IDs |
| --- | --- |
| AI interaction logging with session context and AI-specific telemetry | C12.1.1 |
| Logging of safety filtering and policy decisions in enough detail to audit content moderation | C12.1.2 |
| Structured, interoperable log schema for inference events (model identifier, token usage, provider, operation type) | C12.1.3 |
| Logging of RAG pipeline retrieval events (query, documents retrieved, knowledge source) | C12.1.4 |
| Audit logs capturing the approval chain for security-critical proactive actions (approver identity, timestamp, parameters, outcome) | C12.5.2 |
| Logging of kill-switch activations and override commands | C12.5.3 |
| Immutable audit records for all model changes | C12.6.3 |

**Common pitfalls:** logging prompts without redaction; using mutable log storage without integrity protection; logging agent actions and approvals but not human-initiated overrides such as kill-switch activations.

---

## AD.18 Monitoring, Detection & Incident Response

Detect AI-specific abuse, drift, and anomalies, and respond to incidents.

| Control / Technique | Requirement IDs |
| --- | --- |
| Automated tool containment triggered by policy violations | C9.3.8 |
| Extraction-attempt detector fed by query-pattern analysis | C11.3.1 |
| Response measures triggered on detection of suspected model extraction | C11.3.4 |
| Signature-based detection and alerting on jailbreak patterns, prompt injection, and adversarial inputs | C12.2.1 |
| Behavioral anomaly detection (unusual conversation patterns, excessive retries, systematic probing) | C12.2.2 |
| Custom detection rules for AI-specific threat patterns (coordinated jailbreak attempts, prompt injection, system prompt extraction) | C12.2.3 |
| Extraction-alert events including offending query metadata | C12.2.4 |
| Granular token-usage attribution (per user, session, feature endpoint, team or workspace) | C12.2.5 |
| Monitoring of LLM API traffic for covert-channel and command-and-control indicators | C12.2.6 |
| Data drift detection using methods matched to the input type (KS test or PSI for tabular, embedding-distance for text/image) | C12.3.1 |
| Hallucination detection monitoring of model outputs | C12.3.2 |
| Hallucination rates tracked as continuous time-series metrics | C12.3.3 |
| Distinction of unexplained behavioral shifts from gradual operational drift | C12.3.4 |
| AI-specific incident response plans with per-scenario containment and investigation steps | C12.4.1 |
| AI-specific forensic tools and expertise for investigating model behavior | C12.4.2 |
| Automated incident-response workflows that isolate compromised models and block malicious users | C12.4.3 |
| Post-incident analysis feeding model retraining and safety filter updates | C12.4.4 |
| Security evaluation and threat-landscape assessment on autonomous initiative triggers | C12.5.1 |

**Common pitfalls:** not correlating AI-specific events with broader SIEM alerts; treating drift as a scheduled check rather than continuous monitoring; lacking AI-specific forensic tooling during an incident.

---

## AD.19 Human Oversight & Shutdown Control

Require human approval for high-impact actions and provide reliable, exercised shutdown and graceful-degradation paths under human control.

| Control / Technique | Requirement IDs |
| --- | --- |
| Swarm-level kill-switch that halts all active agent instances | C9.1.3 |
| Runtime blocking of privileged, high-impact, or irreversible actions until explicit human approval is received and verified | C9.2.1 |
| Approval requests displaying canonicalized, complete action parameters (diffs, commands, recipients, amounts, resources, scopes) without truncation | C9.2.2 |
| Trusted reversibility classification for each high-impact action (read-only, reversible, externally reversible, irreversible) | C9.2.3 |
| Runtime enforcement of reversibility classifications (block, require approval, or restrict) | C9.2.4 |
| Restriction and bounding of any self-modification capability (prompt rewriting, tool-list changes, parameter updates) | C9.2.5 |
| AI-augmented review of planned high-risk actions, adding to (not replacing) the deterministic policy gate | C9.2.6 |
| Protection of the AI-augmented review mechanism against prompt-injection bypass | C9.2.7 |
| Approvals cryptographically bound to parameters, requester identity, execution context, and a single-use nonce | C9.2.8 |
| Isolation of approval-issuing key material or credentials from the agent runtime | C9.2.9 |
| Multi-step or multi-agent chains enforcing the highest-impact reversibility classification in the chain | C9.2.10 |
| Manual kill-switch to immediately halt model inference and outputs | C9.6.1 |
| Fail-closed blocking of a pending action when a human-approval gate is not satisfied within the defined time | C9.6.2 |
| Kill-switch commands delivered through an out-of-band channel isolated from the agent runtime | C9.6.3 |
| Explicit consent dialogue and cancellation option on installation of a local MCP server | C10.4.8 |

**Common pitfalls:** documenting a high-risk action policy never wired to a runtime gate; binding approval to parameters without binding to identity or context; defaulting to fail-open when the approver does not respond; assuming an in-band kill-switch will work against a compromised agent; implementing a kill-switch that is never exercised.

---

## References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/42001)
* [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)
