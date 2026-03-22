# Appendix A: Glossary — Research Notes

> **Source:** [`1.0/en/0x90-Appendix-A_Glossary.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x90-Appendix-A_Glossary.md)

## Overview

The glossary defines 87 terms used throughout the AISVS, covering AI/ML concepts, security terminology, and domain-specific definitions. This research page cross-references every glossary term to the chapters that use it, identifies missing terms, flags definitions that could be improved, and tracks emerging terminology from the broader AI security community.

As of March 2026, the analysis identifies 50 high-priority missing terms (30 from the original audit plus 20 newly found in source requirements), 10 medium-priority missing terms, 14 definitions needing improvement, and 17 emerging terms from the 2025–2026 threat landscape that may warrant future inclusion.

---

## Term-to-Chapter Cross-Reference

Every glossary term mapped to the AISVS chapters that reference or rely on it.

| Term | Chapters |
|------|----------|
| Adapter | C03 |
| Adversarial Example | C02, C11 |
| Adversarial Robustness | C11 |
| Adversarial Training | C01, C02, C11 |
| Agent | C02, C05, C09, C10, C11, C13 |
| AI BOM | C03, C06 |
| AppArmor | C04 |
| Attention Map | C07, C14 |
| ABAC | C02, C05 |
| Backdoor Attack | C06, C11 |
| Bias | C01, C06, C11, C14 |
| Bias Exploitation | C01, C11 |
| Blue-Green Deployment | C03 |
| Byzantine Fault Tolerance | C04 |
| Canary Deployment | C03 |
| Cedar | C05 |
| Certified Robustness | C11 |
| Chain of Thought | _(none — consider removing or linking to C07/C14)_ |
| CI/CD | C04, C06, C09 |
| Circuit Breaker | C09, C10 |
| CMP | C12 |
| Concept Drift | C13 |
| Confidential Computing | C04 |
| Confidential Inference | C04 |
| Counterfactual Explanation | C14 |
| Covert Channel | C04, C13 |
| CycloneDX | C03, C06 |
| DAG | C13 |
| Data Augmentation | C01 |
| Data Drift | C13 |
| Data Leakage | C08, C12 |
| Data Poisoning | C01, C06, C11, C13 |
| Defense-in-Depth | _(general principle, not cited by specific requirement)_ |
| Defensive Distillation | C02 |
| Differential Privacy | C11, C12 |
| DoS | C02, C04, C09, C13 |
| DPIA | C12 |
| DP-SGD | C11 |
| DRTM | C04 |
| Embeddings | C05, C08 |
| Explainability | C07, C14 |
| Feature Attribution | C07, C14 |
| Federated Learning | C04, C12 |
| Fine-tuning | C01, C03, C06 |
| FIPS 140-3 | C04 |
| Guardrails | C02, C03, C07, C11 |
| Hallucination | C07, C13 |
| Homoglyph | C02 |
| HSM | C04 |
| Human-in-the-Loop (HITL) | C02, C07, C09, C11, C14 |
| Infrastructure as Code (IaC) | _(none — consider removing or linking to C04)_ |
| Interval-Bound Propagation | C11 |
| Jailbreak | C02, C11, C13 |
| JWT | C05 |
| k-anonymity | C12 |
| KMS | C04, C08 |
| l-diversity | C12 |
| Least Privilege | C04, C09, C10 |
| LIME | C14 |
| Linkage Attack | C12 |
| Machine Unlearning | C12 |
| MCP | C02, C03, C09, C10 |
| Membership Inference Attack | C08, C11 |
| MIG | C04 |
| MITRE ATLAS | C02, C03, C11 |
| Model Card | C14 |
| Model Extraction | C11, C13 |
| Model Inversion | C11, C13 |
| Model Lifecycle Management | C03 |
| Model Poisoning | C06, C11 |
| mTLS | C04 |
| Multi-agent System | C08, C09, C11 |
| NFC | C02 |
| NVLink | C04 |
| OAuth 2.1 | C10 |
| OIDC | C05 |
| OPA | C05 |
| PII | C01, C05, C06, C07, C12, C13 |
| Policy-as-Code | C09, C12 |
| PPML | C11, C12 |
| Prompt Injection | C02, C07, C08, C10, C11, C13 |
| RAG | C02, C03, C07, C08, C11 |
| RBAC | C05 |
| Red-Teaming | C11 |
| Re-identification Risk | C12 |
| Remote Attestation | C04 |
| RLHF | C11 |
| SAML | C05 |
| SBOM | C04, C06 |
| Secure Boot | C04 |
| SMPC | C04 |
| seccomp | C04 |
| SELinux | C04 |
| Shadow Model | C11, C12 |
| SHAP | C14 |
| Side-Channel Attack | C04 |
| SIEM | C13 |
| SPDX | C03 |
| SSE | C10 |
| Steganography | C02 |
| stdio | C10 |
| Strong Authentication | C04, C05 |
| Supply Chain Attack | C06 |
| Synthetic Data | C01, C12 |
| TEE | C04 |
| Temperature Scaling | C11 |
| TLS | C04, C09, C10 |
| Tokenizer | C02, C03 |
| TPM | C04 |
| Transfer Learning | C06 |
| Vector Database | C05, C08 |
| VRAM | C04 |
| Vulnerability Scanning | C06 |
| WASM | C09 |
| Watermarking | C01, C07, C11 |
| WORM | C04, C09 |
| Zero-Day Vulnerability | _(none — consider removing or linking to C06)_ |
| Zero-Trust | C04, C05 |

**Stats:** 3 terms referenced by 0 chapters, ~20 terms by 1 chapter, ~30 terms by 3+ chapters. Cross-references verified against C02, C07, C09, C10, C11 source files as of March 2026.

---

## Missing Terms (High Priority)

Terms used in AISVS chapters but not defined in the glossary. These should be added.

| Term | Used In | Context |
|------|---------|---------|
| Context Window | C02 | Core LLM concept; mentioned as an attack surface for prompt injection |
| Instruction Hierarchy | C02 | Defense concept where system/developer messages take priority over user inputs |
| System Prompt / System Message | C07, C13 | Critical concept for LLM security and logging |
| Orchestrator / Orchestration | C03, C09 | Central to agentic AI architecture |
| Delegation Context | C09 | Security concept for agent-to-agent authorization |
| Capability Token | C05 | Scoped authorization mechanism for autonomous agents |
| JSON-RPC | C10 | Protocol layer underlying MCP messaging |
| Streamable-HTTP | C10 | Primary MCP transport type (replacing SSE) |
| Model Registry | C03 | MLOps concept for centralized model storage and versioning |
| Gradient Clipping | C11 | Privacy-preserving training technique used with DP-SGD |
| Constitutional AI | C11 | Alignment technique for training models with safety principles |
| Soft Refusal | C12 | Safety response pattern for purpose-limitation enforcement |
| Content Classifier | C02, C07 | Core safety component for input/output screening |
| Egress Controls / Egress Allow-list | C03, C04, C06, C10 | Network security concept critical for AI training environments |
| Schema Drift | C13 | Monitoring concept for detecting input/output schema changes |
| Stop Sequences | C07 | LLM output control mechanism for bounding generation |
| Prompt Template | C03, C09 | Key concept for LLM application development |
| Canary-Based Privacy Auditing | C12 | Specialized technique for testing differential privacy guarantees |
| Krum / Trimmed-Mean | C12 | Byzantine-resilient aggregation methods for federated learning |
| Output Perturbation | C11 | Privacy technique for membership inference defense |
| DNS Rebinding | C10 | Specific network attack vector for MCP server exploitation |
| Common Criteria / EAL4+ | C04 | Security certification standard for hardware components |
| InfiniBand / RDMA / NCCL | C04 | AI accelerator interconnect technologies |
| Evaluation Harness | C03 | Testing framework for systematic model evaluation |
| Reasoning Trace | C13 | Agentic decision recording concept for audit trails |
| Envelope Encryption | C08 | Cryptographic technique for key management |
| Kill Switch | C14 | Emergency AI system shutdown mechanism |
| Quasi-identifier | C12 | Privacy term for attributes enabling re-identification |
| Step-up Authentication | C05, C10 | Authentication escalation pattern for high-risk operations |
| Namespace | C08 | Multi-tenant isolation concept for vector databases |
| Adaptive Attack | C11 | Attack specifically designed to defeat deployed defenses (C11.2.4, C11.6.4); distinct from generic adversarial examples |
| Continuous Authorization | C09 | Re-evaluation of authorization on every call using current context (C09.6.3); distinct from one-time auth checks |
| Self-Modification | C11 | AI capability to alter its own configuration, prompts, tool access, or learned behaviors; entire C11.9 subsection |
| Swarm | C09 | Multi-agent collective execution model with aggregate-level controls (C09.8.x); more specific than "multi-agent system" |
| Cross-Modal Attack | C02 | Coordinated attack spanning multiple input types, e.g., image + text (C02.7.5) |
| Tool Manifest | C09 | Declarative spec of tool privileges, side-effect level, resource limits, and output validation (C09.3.5) |
| Source Attribution | C07 | Traceability of RAG-grounded outputs to specific retrieved chunks; entire C07.8 subsection |
| Evaluation Awareness | C11 | Model behavior divergence when detecting testing vs. deployment context (C11.1.5); a specific alignment failure |
| Context Window Displacement | C02 | Attack where user content exceeds context window proportion, pushing out system instructions (C02.1.4) |
| Confidence Scoring | C07 | Methods to assess reliability of generated answers; core hallucination defense (C07.2.1) |
| Retrieval-Based Grounding | C07 | Verification of model claims against authoritative retrieved sources (C07.2.4, C07.8.x) |
| On-Behalf-Of Flow | C10 | OAuth delegation pattern where MCP server obtains downstream tokens rather than passing client tokens (C10.2.9) |
| Dynamic Client Registration | C10 | MCP servers acting as OAuth proxies with per-client consent; prevents cached approval reuse (C10.2.10) |
| Protocol Downgrade | C10 | Attack via header stripping (Mcp-Protocol-Version) on streamable-HTTP transports (C10.3.5) |
| Session Teardown | C10 | Deterministic destruction of cached tokens, state, and resources on MCP session end (C10.2.12) |
| Intent Verification | C09 | Binding execution to user intent and hard constraints to prevent authorized-but-unintended actions (C09.7.x) |
| Bias Probing | C11 | Systematic variation along single input dimensions to discover exploitable bias patterns (C11.10.1) |

## Missing Terms (Medium Priority)

| Term | Used In | Context |
|------|---------|---------|
| Tokenization (security/PII) | C08 | Data masking sense, distinct from NLP tokenizer |
| Sandbox / Sandboxing | C04, C09 | Referenced via seccomp/AppArmor but lacks its own entry |
| Protocol Buffers | C02 | Schema definition format for structured input validation |
| FIDO2/WebAuthn | C05 | Phishing-resistant auth; referenced in Strong Authentication def but no own entry |
| Customer-Managed Key (CMK) | C05 | Cloud encryption key management for multi-tenant isolation |
| Secure Enclave | C04 | Hardware security term for edge/mobile TEEs |
| Action Catalog / Capability Allow-list | C03 | Agentic configuration concept for permitted operations |
| Compensating Action | C09 | Rollback/recovery concept for irreversible agent actions (C09.2.3); transactional semantics |
| Memory Namespace | C09 | Per-agent isolated memory scope within a multi-agent system (C09.8.3) |
| Dynamic Dispatch / Reflective Invocation | C10 | Runtime function resolution patterns MCP servers must prohibit (C10.6.2) |

---

## Emerging Terminology (2025–2026)

Terms gaining traction in the AI security community that may warrant future glossary inclusion. These are not yet in the AISVS source but are appearing in standards, incident reports, and tooling.

### Agentic Security

| Term | Definition | Relevant To |
|------|-----------|-------------|
| Tool Poisoning | Attack where a malicious MCP server embeds hidden instructions in tool descriptions or metadata that manipulate agent behavior at selection or invocation time | C10, C09 |
| Tool Squatting | Registering a tool with a name semantically similar to a legitimate tool, causing an LLM to prefer the malicious tool — typosquatting in semantic space | C10, C06 |
| MCP Gateway | Security proxy mediating all traffic between agents and MCP tool servers, enforcing auth, rate limiting, audit logging, and policy at a centralized chokepoint | C10, C04 |
| Confused Deputy (AI) | Exploiting trust boundaries to trick an agent into using its legitimate permissions for unauthorized actions on behalf of an attacker, typically via indirect prompt injection | C09, C05 |
| Human-on-the-Loop | Governance model where a human supervises and can intervene but does not approve each individual action; contrast with HITL | C14, C09 |
| Agentic Control Plane | Governance layer managing identity, authorization, orchestration, and trust for autonomous AI agents — analogous to the Kubernetes control plane but for agents | C09, C05, C13 |

### Novel Attack Patterns

| Term | Definition | Relevant To |
|------|-----------|-------------|
| Indirect Prompt Injection | Adversarial instructions embedded in external data sources (documents, websites, tool outputs) that an LLM processes as trusted context; distinct from direct prompt injection | C02, C07, C08 |
| RAG Poisoning | Injecting crafted documents into a knowledge base or vector store; research shows as few as 5 crafted documents among millions can achieve 90% attack success | C08, C01 |
| Embedding Inversion | Reconstructing original text or sensitive data from vector embeddings, breaking the assumption that embeddings are one-way transformations | C08, C12 |
| Model Collapse | Progressive quality degradation when models train on synthetic data from other models, causing output distributions to narrow and amplify errors across generations | C01, C03 |
| Many-Shot Jailbreak | Prompt injection exploiting in-context learning by including hundreds of examples of desired prohibited behavior, leveraging expanding context windows | C07, C11 |
| Crescendo Attack | Multi-turn jailbreak that progressively steers conversation from harmless topics toward prohibited content, exploiting conversational coherence tendencies | C07, C11 |
| Data Contamination (Benchmark) | Training models on the same data used in evaluations, rendering benchmarks unreliable; distinct from adversarial data poisoning — may be unintentional | C01, C03 |
| Reward Hacking | Finding unintended shortcuts to maximize a reward signal without achieving the intended objective; models may learn to distinguish test vs. deployment environments | C03, C07 |

### Governance & Compliance

| Term | Definition | Relevant To |
|------|-----------|-------------|
| GPAI (General-Purpose AI) Model | EU AI Act term for models with significant generality capable of wide-ranging tasks; subject to specific transparency and safety obligations since August 2025 | C03, C06 |
| Systemic Risk (EU AI Act) | Classification for GPAI models trained with >10²⁵ FLOPs, triggering adversarial testing, incident reporting, and cybersecurity obligations | C03, C11 |
| FRIA (Fundamental Rights Impact Assessment) | EU AI Act Article 27 mandatory assessment for deployers of high-risk AI systems, evaluating impacts on non-discrimination, privacy, and human dignity; required by August 2026 | C14, C12 |
| Post-Market Monitoring | EU AI Act Article 72 requirement for high-risk AI providers to actively collect and review performance data throughout the system's lifetime | C13, C03 |

### Provenance & Transparency

| Term | Definition | Relevant To |
|------|-----------|-------------|
| C2PA (Coalition for Content Provenance and Authenticity) | Open standard for embedding cryptographically signed metadata into digital content to verify origin, edit history, and AI involvement; increasingly mandated by EU and California regulations | C07, C03 |
| Content Provenance | Verifiable chain of origin, creation method, and modification history for digital content; encompasses C2PA, watermarking, and fingerprinting approaches | C07, C13 |
| Shadow AI | Unauthorized use of AI tools by employees without organizational vetting or controls; 2025 industry data shows 77% of enterprise AI users have pasted company data into unapproved chatbots | C05, C13, C12 |

---

## Definitions Needing Improvement

Existing glossary definitions that could better reflect how terms are used in the chapters.

| Term | Issue | Suggested Improvement |
|------|-------|----------------------|
| Agent | Too narrow — doesn't cover the spectrum from simple tool-calling to multi-step autonomous agents | Add: "Agents range from simple tool-calling systems that execute a single function per request to fully autonomous multi-step systems that chain reasoning, tool use, and sub-agent delegation across extended workflows. The degree of autonomy determines the required security controls (C05, C09, C10)." |
| Circuit Breaker | Missing MCP context | Add: "In agentic and MCP-connected systems, circuit breakers also apply to tool invocation chains, halting cascading calls when step counts, latency, or cost thresholds are exceeded (C10.5.2)." |
| Guardrails | Only mentions "constraints" | Add: "Guardrails may be implemented as dedicated safety classifier models, rule-based filter systems, or separate validation services that evaluate inputs and outputs independently of the primary model." |
| MCP | Missing key technical details | Add: "MCP uses JSON-RPC 2.0 as its messaging format and supports three transport types: streamable-HTTP (the primary remote transport since the 2025-03-26 spec revision), SSE (deprecated for new deployments), and stdio (local same-machine only). Remote MCP connections require OAuth 2.1." |
| Prompt Injection | Doesn't distinguish direct vs. indirect | Add: "Includes both direct injection (user crafts malicious input) and indirect injection (adversarial instructions embedded in retrieved documents, tool outputs, or third-party data the model processes as trusted context). Indirect injection is particularly dangerous in RAG and agentic systems." |
| RAG | Too basic for how extensively AISVS covers it | Add: "RAG introduces distinct attack surfaces including retrieval poisoning, chunk-level traceability requirements, and citation integrity validation. See C08 for data store security and C02 for indirect prompt injection via retrieved content." |
| Watermarking | Doesn't enumerate distinct use cases | Add: "Serves three distinct purposes: dataset provenance marking to detect unauthorized training data use (C01), output media watermarking to identify AI-generated content (C07), and model weight watermarking as a defense against unauthorized extraction (C11)." |
| Data Poisoning | Only covers training-time | Add: "Can occur at training time (corrupting datasets or fine-tuning data) or at inference time (injecting adversarial content into RAG knowledge stores, vector databases, or retrieval sources). Inference-time poisoning does not require training pipeline access." |
| Model Card | Focuses on transparency only | Add: "Effective model cards also cover operational aspects: known failure modes, version history with change justification, deployment environment requirements, monitoring baselines, and lifecycle status (active, deprecated, retired). See C14." |
| Differential Privacy | Missing delta parameter | Replace epsilon-only clause with: "...quantified by an epsilon (ε) privacy budget bounding worst-case privacy loss and a delta (δ) parameter representing the probability of that bound being violated. DP-SGD implementations require specifying both; C12.3.1 mandates reporting both." |
| SSE | Doesn't note deprecation | Add: "SSE has been superseded by streamable-HTTP as MCP's primary remote transport since the 2025-03-26 specification revision. SSE-based MCP endpoints should be restricted to internal channels only (C10.3.3)." |
| stdio | Missing usage restriction | Add: "C10.6.1 restricts stdio-based MCP transports to co-located, same-machine development scenarios only; stdio must not be used for production remote communication due to absent authentication and encryption." |
| Shadow Model | Too narrow | Reframe: "Serves both offensive and defensive purposes: attackers use shadow models for membership inference attacks (C11), while defenders use them to verify data deletion and machine unlearning effectiveness (C12.2.3)." |
| Federated Learning | Missing security nuances | Add: "Introduces unique security considerations: local differential privacy on gradient updates before sharing, Byzantine-resistant aggregation (Krum, trimmed-mean), and canary-based privacy auditing. See C12.6." |

---

## Notable References

- [CSA: Securing the Agentic Control Plane (March 2026)](https://cloudsecurityalliance.org/blog/2026/03/20/2026-securing-the-agentic-control-plane) — introduces agent identity as a first-class security principal
- [OWASP LLM Top 10 v2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — updated prompt injection taxonomy with direct/indirect distinction
- [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026) — evaluation gap and model collapse findings
- [EU AI Act GPAI Guidelines](https://artificialintelligenceact.eu/gpai-guidelines-overview/) — GPAI model obligations effective August 2025
- [MCP Transport Future (December 2025)](https://blog.modelcontextprotocol.io/posts/2025-12-19-mcp-transport-future/) — streamable-HTTP replacing SSE
- [Trail of Bits: DataSig Dataset Fingerprinting (May 2025)](https://blog.trailofbits.com/2025/05/02/datasig-fingerprinting-ai/ml-datasets-to-stop-data-borne-attacks/) — dataset provenance verification
- [NSA/CISA: Content Credentials CSI (January 2025)](https://media.defense.gov/2025/Jan/29/2003634788/-1/-1/0/CSI-CONTENT-CREDENTIALS.PDF) — C2PA guidance for AI-generated content

---

## Community Notes

_Discussion about glossary scope, definitions, and consistency._

---

[README](README.md)
