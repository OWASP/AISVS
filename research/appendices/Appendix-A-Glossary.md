# Appendix A: Glossary — Research Notes

> **Source:** [`1.0/en/0x90-Appendix-A_Glossary.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x90-Appendix-A_Glossary.md)

## Overview

The glossary defines 139 terms used throughout the AISVS, covering AI/ML concepts, security terminology, and domain-specific definitions. This research page cross-references every glossary term to the chapters that use it, identifies missing terms, flags definitions that could be improved, and tracks emerging terminology from the broader AI security community.

As of May 2026, the analysis identifies 48 high-priority missing terms, 10 medium-priority missing terms, 12 definitions needing improvement, and 50 emerging terms from the 2025–2026 threat landscape that may warrant future inclusion. The latest glossary source added 20 terms that were previously tracked as missing or adjacent research items, including Context Window, Constitutional AI, Prompt Template, Sandboxing, Kill-Switch, Embedding Inversion, Data Lineage, Data Minimization, Fail-Closed / Fail-Open, PDP, SCVS, SLSA, SOC, and Reward Model. MITRE ATLAS continued expanding after the February 2026 agentic updates: the public releases now identify v5.6.0 as the latest release and add agent tool poisoning, AI supply-chain rug pulls, reputation inflation, AI service proxies, agent configuration discovery, cost-harvesting variants, and deepfake-assisted phishing alongside earlier techniques such as Publish Poisoned AI Agent Tool (AML.T0104), Escape to Host (AML.T0105), and Deploy AI Agent (AML.T0103). The OpenClaw investigation case studies (AML.CS0048–CS0051) documented exposed agent control interfaces, poisoned skills, one-click RCE, sandbox escape, and prompt-injection-driven command and control. Meanwhile, NIST's draft Cyber AI Profile (IR 8596) is moving through Spring 2026 working sessions after public comment, the EU GPAI Code of Practice signatory list is live, and industry adoption of agentic identity as a first-class security concept has accelerated.

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
| AI BOM / AIBOM / MBOM | C03, C06 |
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
| Constitutional AI | C11 |
| Context Window | C02, C09 |
| Counterfactual Explanation | C14 |
| Covert Channel | C04, C13 |
| CycloneDX | C03, C06 |
| DAG | C13 |
| Data Augmentation | C01 |
| Data Drift | C13 |
| Data Leakage | C08, C12 |
| Data Lineage | C01, C03, C06 |
| Data Minimization | C12 |
| Data Poisoning | C01, C06, C11, C13 |
| Defense-in-Depth | _(general principle, not cited by specific requirement)_ |
| Defensive Distillation | C02 |
| Differential Privacy | C11, C12 |
| DoS | C02, C04, C09, C13 |
| Downgrade (response) | C12 |
| DPIA | C12 |
| DP-SGD | C11 |
| DRTM | C04 |
| Embeddings | C05, C08 |
| Embedding Inversion | C08 |
| Exfiltration | C08, C09, C10, C13 |
| Explainability | C07, C14 |
| Fail-Closed / Fail-Open | C03, C09, C10, C14 |
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
| JIT (Just-in-Time) Privileged Access | C05 |
| JWT | C05 |
| k-anonymity | C12 |
| Kill-Switch | C14 |
| KMS | C04, C08 |
| l-diversity | C12 |
| Least Privilege | C04, C09, C10 |
| LIME | C14 |
| Linkage Attack | C12 |
| Machine Unlearning | C12 |
| Many-Shot Jailbreaking | C02, C07, C11 |
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
| Non-repudiation | C09, C13 |
| NFC | C02 |
| NVLink | C04 |
| OAuth 2.1 | C10 |
| OIDC | C05 |
| OPA | C05 |
| PDP (Policy Decision Point) | C05, C09 |
| PII | C01, C05, C06, C07, C12, C13 |
| Policy-as-Code | C09, C12 |
| PPML | C11, C12 |
| Prompt Injection | C02, C07, C08, C10, C11, C13 |
| Prompt Template | C03, C05, C09 |
| Quantization | C03, C11 |
| RAG | C02, C03, C07, C08, C11 |
| RBAC | C05 |
| Red-Teaming | C11 |
| Re-identification Risk | C12 |
| Remote Attestation | C04 |
| Reward Model | C03, C11 |
| RLHF | C11 |
| SAML | C05 |
| Sandboxing | C04, C09 |
| SBOM | C04, C06 |
| SCVS | General guidance, Appendix D; supports C06 |
| Secure Boot | C04 |
| SMPC | C04 |
| seccomp | C04 |
| SELinux | C04 |
| Shadow Deployment | C03 |
| Shadow Model | C11, C12 |
| SHAP | C14 |
| Side-Channel Attack | C04 |
| SIEM | C13 |
| SLSA | General guidance, Appendix D; supports C06 |
| SOC | C02, C13 |
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

**Stats:** 3 terms still have no direct chapter reference (Chain of Thought, Infrastructure as Code, Zero-Day Vulnerability), while SCVS and SLSA appear in the general usage guidance and controls inventory rather than a single requirement chapter. Cross-references were refreshed against all C01–C14 source files as of May 2026.

---

## Missing Terms (High Priority)

Terms used in AISVS chapters but not defined in the glossary. These should be added.

| Term | Used In | Context |
|------|---------|---------|
| Instruction Hierarchy | C02 | Defense concept where system/developer messages take priority over user inputs |
| System Prompt / System Message | C07, C13 | Critical concept for LLM security and logging |
| Orchestrator / Orchestration | C03, C09 | Central to agentic AI architecture |
| Delegation Context | C09 | Security concept for agent-to-agent authorization |
| Capability Token | C05 | Scoped authorization mechanism for autonomous agents |
| JSON-RPC | C10 | Protocol layer underlying MCP messaging |
| Streamable-HTTP | C10 | Primary MCP transport type (replacing SSE) |
| Model Registry | C03 | MLOps concept for centralized model storage and versioning |
| Gradient Clipping | C11 | Privacy-preserving training technique used with DP-SGD |
| Soft Refusal | C12 | Safety response pattern for purpose-limitation enforcement; related to the new Downgrade (response) glossary term but still useful as a separate behavior label for C12.4.2 |
| Content Classifier | C02, C07 | Core safety component for input/output screening |
| Egress Controls / Egress Allow-list | C03, C04, C06, C10 | Network security concept critical for AI training environments |
| Schema Drift | C13 | Monitoring concept for detecting input/output schema changes |
| Stop Sequences | C07 | LLM output control mechanism for bounding generation |
| Canary-Based Privacy Auditing | C12 | Specialized technique for testing differential privacy guarantees |
| Krum / Trimmed-Mean | C12 | Byzantine-resilient aggregation methods for federated learning |
| Output Perturbation | C11 | Privacy technique for membership inference defense |
| DNS Rebinding | C10 | Specific network attack vector for MCP server exploitation |
| Common Criteria / EAL4+ | C04 | Security certification standard for hardware components |
| InfiniBand / RDMA / NCCL | C04 | AI accelerator interconnect technologies |
| Evaluation Harness | C03 | Testing framework for systematic model evaluation |
| Reasoning Trace | C13 | Agentic decision recording concept for audit trails |
| Envelope Encryption | C08 | Cryptographic technique for key management |
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
| RAG Credential Harvesting | C09, C10 | Agent using RAG or tool access to search for and collect credentials, secrets, or API keys inadvertently ingested into data stores (MITRE ATLAS AML.T0098) |
| Memory Manipulation | C08, C09 | Altering agent long-term memory to ensure malicious changes persist across future sessions (MITRE ATLAS, October 2025) |
| Thread Injection | C02, C09 | Introducing malicious instructions into a specific conversation thread to change agent behavior for the session duration (MITRE ATLAS, October 2025) |
| Least Agency | C09, C14 | OWASP Agentic Top 10 principle that agents should receive only the minimum autonomy required for their authorized task; extends least privilege to cover scope of autonomous action |
| DIE Model (Distributed, Immutable, Ephemeral) | C04, C09 | Architecture paradigm from the OWASP AI Testing Guide (November 2025) that shifts from hardening individual AI components to making the entire system resilient through distribution, immutability, and ephemerality |

## Missing Terms (Medium Priority)

| Term | Used In | Context |
|------|---------|---------|
| Tokenization (security/PII) | C08 | Data masking sense, distinct from NLP tokenizer |
| Protocol Buffers | C02 | Schema definition format for structured input validation |
| FIDO2/WebAuthn | C05 | Phishing-resistant auth; referenced in Strong Authentication def but no own entry |
| Customer-Managed Key (CMK) | C05 | Cloud encryption key management for multi-tenant isolation |
| Secure Enclave | C04 | Hardware security term for edge/mobile TEEs |
| Action Catalog / Capability Allow-list | C03 | Agentic configuration concept for permitted operations |
| Compensating Action | C09 | Rollback/recovery concept for irreversible agent actions (C09.2.3); transactional semantics |
| Memory Namespace | C09 | Per-agent isolated memory scope within a multi-agent system (C09.8.3) |
| Dynamic Dispatch / Reflective Invocation | C10 | Runtime function resolution patterns MCP servers must prohibit (C10.6.2) |
| System Prompt Leakage | C07, C13 | Extraction of embedded system instructions, secrets, or configuration from an LLM; OWASP LLM Top 10 2025 entry LLM07:2025 |
| Vector and Embedding Weaknesses | C08, C12 | Vulnerabilities in vector stores and embedding pipelines including inversion and poisoning; OWASP LLM Top 10 2025 entry LLM08:2025 |

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
| Agentic Identity | The principle that every AI agent is an identity requiring authentication, access control, policy enforcement, and auditability — the same governance applied to human identities. As agents accumulate entitlements across databases, cloud services, and repositories, they become high-value targets (Strata, Cisco, Microsoft all ship agentic identity products as of March 2026) | C05, C09, C10 |
| Publish Poisoned AI Agent Tool (AML.T0104) | MITRE ATLAS technique (February 2026) where adversaries create malicious versions of legitimate MCP tools that appear safe in descriptions and metadata but execute harmful actions when invoked — the supply-chain analogue of tool poisoning | C10, C06 |
| Escape to Host (AML.T0105) | MITRE ATLAS technique (February 2026) for breaking out of agent sandbox environments; the OpenClaw investigation found a 200ms race condition window during sandbox initialization where code has unrestricted host access | C04, C09 |
| AI Agent Tool Poisoning (AML.T0110) | Persistence technique where an adversary compromises tools already integrated into an agent environment, including built-in tools or MCP-connected tools, so future agent runs continue to execute attacker-controlled behavior | C09, C10, C06 |
| Agentic Resource Consumption (AML.T0034.002) | Cost-harvesting pattern where an attacker induces agents to burn tokens, tool calls, compute, API quota, or downstream service spend through loops, oversized context, or expensive delegated workflows | C09, C10, C13 |
| AI Service Proxy (AML.T0008.005) | Adversary infrastructure that resells or brokers access to commercial model APIs, useful for large-scale distillation, command generation, phishing content, or evading single-account throttles | C06, C11, C13 |

### Novel Attack Patterns

| Term | Definition | Relevant To |
|------|-----------|-------------|
| Indirect Prompt Injection | Adversarial instructions embedded in external data sources (documents, websites, tool outputs) that an LLM processes as trusted context; distinct from direct prompt injection | C02, C07, C08 |
| RAG Poisoning | Injecting crafted documents into a knowledge base or vector store; research shows as few as 5 crafted documents among millions can achieve 90% attack success | C08, C01 |
| Model Collapse | Progressive quality degradation when models train on synthetic data from other models, causing output distributions to narrow and amplify errors across generations | C01, C03 |
| Crescendo Attack | Multi-turn jailbreak that progressively steers conversation from harmless topics toward prohibited content, exploiting conversational coherence tendencies; invisible to per-turn classifiers | C07, C11 |
| Skeleton Key | Direct jailbreak technique (Microsoft, June 2024) that redefines safety rules in-context by instructing the model to append warnings rather than block; once accepted, the model complies with all subsequent requests without indirection or encoding | C02, C11 |
| Data Contamination (Benchmark) | Training models on the same data used in evaluations, rendering benchmarks unreliable; distinct from adversarial data poisoning — may be unintentional | C01, C03 |
| Reward Hacking | Finding unintended shortcuts to maximize a reward signal without achieving the intended objective; models may learn to distinguish test vs. deployment environments | C03, C07 |
| Agent Clickbait (AML.T0100) | MITRE ATLAS technique where adversaries lure AI browser agents into unintended actions by exploiting how agents interpret UI content, visual cues, and embedded prompts on websites | C09, C10 |
| AI Agent Tool Data Poisoning (AML.T0099) | MITRE ATLAS technique where adversaries place malicious content or files on a system that agents subsequently invoke, hijacking agent behavior through poisoned tool inputs | C09, C10, C06 |
| Data Destruction via Agent Tool Invocation (AML.T0101) | MITRE ATLAS technique where attackers exploit agent tool capabilities to destroy data and files on target systems, disrupting agent infrastructure and services | C09, C10 |
| Deploy AI Agent (AML.T0103) | MITRE ATLAS technique (January 2026) where adversaries deploy autonomous AI agents as persistent access mechanisms, using agent infrastructure for command and control — documented in the SesameOp case study (AML.CS0042) using OpenAI Assistants API as a covert C2 channel | C09, C05 |
| Multimodal Prompt Injection | Adversarial instructions embedded within images, audio, or video files that a multimodal model processes, bypassing text-only input filters; a growing concern as models increasingly accept heterogeneous input types (February 2026 research surveys document this as an expanding attack class) | C02, C07 |
| Context-Dependent Prompt Injection | Prompt injection that exploits cases where an agent is legitimately expected to rely on runtime observations, making simple context suppression an unreliable defense; the AgentPI benchmark highlights this gap for autonomous agents | C02, C09, C10, C11 |
| AI Supply Chain Rug Pull (AML.T0109) | Publishing an initially benign AI component, model, dataset, package, skill, or MCP server to gain adoption, then pushing a malicious update once review pressure has dropped | C06, C03 |
| AI Supply Chain Reputation Inflation (AML.T0111) | Building or abusing credible trust signals such as downloads, stars, forks, publisher history, or dependency-tree inclusion so malicious AI components look legitimate during selection and review | C06, C03 |
| AI Voice Cloning | Use of generated or cloned speech to impersonate trusted people in phishing, approval fraud, help-desk abuse, or high-risk authorization flows; MITRE ATLAS now tracks this under Deepfake-Assisted Phishing (AML.T0052.001) | C05, C13, C14 |

### Governance & Compliance

| Term | Definition | Relevant To |
|------|-----------|-------------|
| GPAI (General-Purpose AI) Model | EU AI Act term for models trained with >10²³ FLOPs displaying significant generality; subject to transparency and safety obligations since August 2025 including technical documentation and copyright compliance | C03, C06 |
| Systemic Risk (EU AI Act) | Classification for GPAI models trained with >10²⁵ FLOPs, triggering mandatory adversarial red-teaming, incident reporting to the AI Office, and cybersecurity obligations under Article 55 | C03, C11 |
| FRIA (Fundamental Rights Impact Assessment) | EU AI Act Article 27 mandatory assessment for deployers of high-risk AI systems, evaluating impacts on non-discrimination, privacy, and human dignity; required by August 2026. May complement a DPIA under GDPR Article 35 | C14, C12 |
| Post-Market Monitoring | EU AI Act Article 72 requirement for high-risk AI providers to actively collect and review performance data throughout the system's lifetime | C13, C03 |
| Code of Practice (EU AI Act) | Voluntary framework for GPAI model providers to demonstrate compliance with AI Act obligations; the official July 2025 code has Transparency, Copyright, and Safety and Security chapters, and the European Commission's April 2026 page lists active signatories | C03, C06, C14 |
| Cyber AI Profile (NIST IR 8596) | Draft NIST profile (December 2025; comment period closed January 30, 2026) extending CSF 2.0 to AI systems across three focus areas: Secure (protecting AI systems), Defend (using AI for cyber defense), and Thwart (building resilience against AI-enabled attacks). NIST posted Spring 2026 working sessions for April 28, May 5, and May 12, 2026, so teams should treat the terminology as active but still draft | C03, C11, C13 |

### Interoperability & Agent Protocols

| Term | Definition | Relevant To |
|------|-----------|-------------|
| A2A (Agent2Agent Protocol) | Open protocol (Google, April 2025; contributed to Linux Foundation June 2025) enabling AI agents to discover capabilities, exchange context, and coordinate tasks across vendors and frameworks. Uses Agent Cards for capability discovery and supports enterprise-grade auth. Version 0.3 added gRPC and signed Agent Cards, and the Linux Foundation reported 150+ supporting organizations at the protocol's first anniversary in April 2026 | C09, C10 |
| Agent Card | JSON-format capability descriptor in the A2A protocol that advertises an agent's supported tasks, authentication requirements, and interaction modes to other agents | C09, C10 |
| Non-Human Identity (NHI) | Machine or agent identity used for authentication and authorization in automated workflows; World Economic Forum data shows NHIs outnumber human identities 50:1 in enterprises (projected 80:1 by 2028). Three of the OWASP Agentic Top 10 risks (ASI02, ASI03, ASI04) are identity-focused | C05, C09, C10 |

### OWASP Agentic Risk Taxonomy

The OWASP Top 10 for Agentic Applications (December 2025) introduced a formal risk classification for autonomous AI systems. These identifiers are increasingly used in threat modeling.

| Term | Definition | Relevant To |
|------|-----------|-------------|
| ASI01 — Agent Goal Hijack | Attacker manipulates natural language inputs or external content to silently redirect an agent's objective (e.g., EchoLeak exfiltration via copilot hijacking) | C02, C09, C11 |
| ASI02 — Tool Misuse & Exploitation | Agent uses a legitimate tool in an unsafe way due to prompt injection, misalignment, or unsafe delegation — the tool works correctly but the intent is wrong | C09, C10 |
| ASI03 — Identity & Privilege Abuse | Exploitation of the credentials and privileges agents hold, including over-provisioned service accounts and leaked API keys | C05, C09, C10 |
| ASI04 — Agentic Supply Chain Vulnerabilities | Compromised agent components, plugins, or tool dependencies introduce risk through the agent software supply chain | C06, C09 |
| ASI05 — Unexpected Code Execution (RCE) | Agent-generated or agent-retrieved code runs in an unsandboxed environment, enabling remote code execution | C04, C09 |
| ASI06 — Memory & Context Poisoning | Adversaries manipulate agent long-term memory or conversation context to create persistent malicious behavior across sessions | C08, C09, C11 |
| ASI07 — Insecure Inter-Agent Communication | Unprotected message channels between agents allow eavesdropping, injection, or impersonation | C09, C10 |
| ASI08 — Cascading Failures | Error or attack in one agent propagates through multi-agent workflows, amplifying impact | C09, C13 |
| ASI09 — Human-Agent Trust Exploitation | Agents exploit user trust to obtain approvals for actions the user does not fully understand | C14, C09 |
| ASI10 — Rogue Agents | Agents that deviate from intended behavior due to misalignment, compromise, or emergent goal-seeking | C11, C09, C14 |

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
| Circuit Breaker | Needs explicit MCP tool-chain context | Add: "In agentic and MCP-connected systems, circuit breakers also apply to tool invocation chains, halting cascading calls when step counts, latency, or cost thresholds are exceeded (C10.5.2)." |
| Guardrails | Only mentions "constraints" | Add: "Guardrails may be implemented as dedicated safety classifier models, rule-based filter systems, or separate validation services that evaluate inputs and outputs independently of the primary model." |
| MCP | Missing key technical details | Add: "MCP uses JSON-RPC 2.0 as its messaging format and supports stdio and Streamable HTTP transports. The 2025-06-18 specification classifies remote MCP servers as OAuth resource servers, requires resource indicators to bind tokens to the intended MCP server, forbids token passthrough to downstream APIs, and requires Streamable HTTP servers to validate Origin headers to reduce DNS rebinding risk." |
| Prompt Injection | Doesn't distinguish direct vs. indirect | Add: "Includes both direct injection (user crafts malicious input) and indirect injection (adversarial instructions embedded in retrieved documents, tool outputs, or third-party data the model processes as trusted context). Indirect injection is particularly dangerous in RAG and agentic systems." |
| RAG | Too basic for how extensively AISVS covers it | Add: "RAG introduces distinct attack surfaces including retrieval poisoning, chunk-level traceability requirements, and citation integrity validation. See C08 for data store security and C02 for indirect prompt injection via retrieved content." |
| Watermarking | Doesn't enumerate distinct use cases | Add: "Serves three distinct purposes: dataset provenance marking to detect unauthorized training data use (C01), output media watermarking to identify AI-generated content (C07), and model weight watermarking as a defense against unauthorized extraction (C11)." |
| Data Poisoning | Only covers training-time | Add: "Can occur at training time (corrupting datasets or fine-tuning data) or at inference time (injecting adversarial content into RAG knowledge stores, vector databases, or retrieval sources). Inference-time poisoning does not require training pipeline access." |
| Model Card | Focuses on transparency only | Add: "Effective model cards also cover operational aspects: known failure modes, version history with change justification, deployment environment requirements, monitoring baselines, and lifecycle status (active, deprecated, retired). See C14." |
| Differential Privacy | Missing delta parameter | Replace epsilon-only clause with: "...quantified by an epsilon (ε) privacy budget bounding worst-case privacy loss and a delta (δ) parameter representing the probability of that bound being violated. DP-SGD implementations require specifying both; C12.3.1 mandates reporting both." |
| SSE | Doesn't note deprecation | Add: "SSE has been superseded by Streamable HTTP as MCP's primary remote transport since the 2025-03-26 specification revision. SSE-based MCP endpoints should be restricted to internal channels only (C10.3.3), and new deployments should prefer Streamable HTTP's simpler request/response backpressure and Origin validation model." |
| stdio | Missing usage restriction | Add: "C10.6.1 restricts stdio-based MCP transports to co-located, same-machine development scenarios only; stdio must not be used for production remote communication due to absent authentication and encryption." |
| Federated Learning | Missing security nuances | Add: "Introduces unique security considerations: local differential privacy on gradient updates before sharing, Byzantine-resistant aggregation (Krum, trimmed-mean), and canary-based privacy auditing. See C12.6." |

---

## MITRE ATLAS Technique Mapping

Key MITRE ATLAS techniques that correspond to AISVS glossary terms. As of May 2026, the latest public release is v5.6.0. The October 2025 update added the initial agentic AI coverage, the February 2026 releases expanded agent sandbox and poisoned-tool techniques through the OpenClaw investigation, the March 2026 v5.5.0 release added supply-chain rug pulls, tool poisoning persistence, reputation inflation, cost-harvesting variants, AI service proxies, and call-chain discovery, and the May 2026 v5.6.0 release added agent-configuration acquisition, code-repository discovery, and deepfake-assisted phishing coverage.

| ATLAS ID | Technique | Glossary Term(s) | AISVS Chapters |
|----------|-----------|-------------------|----------------|
| AML.T0010 | ML Supply Chain Compromise | Supply Chain Attack, Model Poisoning | C06, C11 |
| AML.T0018 | Backdoor ML Model | Backdoor Attack, Data Poisoning | C01, C06, C11 |
| AML.T0020 | Poison Training Data | Data Poisoning | C01, C06 |
| AML.T0024 | Exfiltration via ML Inference API | Model Extraction, Exfiltration | C11, C13 |
| AML.T0029 | Denial of ML Service | DoS | C02, C04, C09 |
| AML.T0040 | ML Model Inference API Access | Membership Inference Attack | C11, C12 |
| AML.T0043 | Craft Adversarial Data | Adversarial Example | C02, C11 |
| AML.T0047 | ML-Enabled Product/Service | Prompt Injection, Jailbreak | C02, C11 |
| AML.T0051 | LLM Prompt Injection | Prompt Injection | C02, C07, C10 |
| AML.T0054 | LLM Jailbreak | Jailbreak | C02, C11 |
| AML.T0056 | LLM Meta Prompt Extraction | System Prompt (missing term) | C07, C13 |
| AML.T0096 | AI Service API _(new, 2025)_ | Agent, Orchestrator (missing term) | C09, C10 |
| AML.T0098 | AI Agent Tool Credential Harvesting _(new, 2025)_ | RAG Credential Harvesting (emerging) | C09, C10, C05 |
| AML.T0099 | AI Agent Tool Data Poisoning _(new, 2025)_ | Tool Poisoning (emerging) | C09, C10, C06 |
| AML.T0100 | AI Agent Clickbait _(new, 2025)_ | Agent Clickbait (emerging) | C09, C10 |
| AML.T0101 | Data Destruction via AI Agent _(new, 2025)_ | Kill-Switch | C09, C10, C14 |
| AML.T0103 | Deploy AI Agent _(new, Jan 2026)_ | Agent, Orchestrator (missing term) | C09, C05 |
| AML.T0104 | Publish Poisoned AI Agent Tool _(new, Feb 2026)_ | Tool Poisoning (emerging), Tool Squatting (emerging) | C10, C06 |
| AML.T0105 | Escape to Host _(new, Feb 2026)_ | Sandboxing, TEE | C04, C09 |
| AML.T0106 | Exploitation for Credential Access _(new, Feb 2026)_ | RAG Credential Harvesting (emerging) | C05, C09, C10 |
| AML.T0107 | Exploitation for Defense Evasion _(new, Feb 2026)_ | Adversarial Robustness | C11, C09 |
| AML.T0108 | AI Agent _(new, Feb 2026)_ | Agent | C09, C10, C05 |
| AML.T0109 | AI Supply Chain Rug Pull _(new, 2026)_ | Supply Chain Attack, Model Poisoning | C06, C03 |
| AML.T0110 | AI Agent Tool Poisoning _(new, 2026)_ | Tool Poisoning, MCP, Agent | C09, C10, C06 |
| AML.T0111 | AI Supply Chain Reputation Inflation _(new, 2026)_ | Supply Chain Attack, AI BOM / AIBOM | C06, C03 |
| AML.T0034.002 | Agentic Resource Consumption _(new, 2026)_ | DoS, Circuit Breaker | C09, C10, C13 |
| AML.T0084.003 | Call Chains _(new, 2026)_ | Orchestrator (missing term), Evaluation Harness (missing term) | C03, C09, C10 |
| AML.T0008.005 | AI Service Proxies _(new, 2026)_ | Model Extraction, Model Distillation (missing term) | C11, C13, C06 |
| AML.T0052.001 | Deepfake-Assisted Phishing _(new, 2026)_ | AI Voice Cloning (emerging), Strong Authentication | C05, C13, C14 |

---

## Notable References

- [CSA: Securing the Agentic Control Plane (March 2026)](https://cloudsecurityalliance.org/blog/2026/03/20/2026-securing-the-agentic-control-plane) — introduces agent identity as a first-class security principal
- [OWASP LLM Top 10 v2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — updated prompt injection taxonomy with direct/indirect distinction
- [OWASP Top 10 for Agentic Applications (December 2025)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — ASI01–ASI10 risk taxonomy for autonomous AI systems
- [MITRE ATLAS Agentic AI Update (October 2025)](https://zenity.io/blog/current-events/mitre-atlas-ai-security) — 14 new agent-focused techniques including AML.T0096–T0101
- [Google A2A Protocol (April 2025)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) — agent-to-agent interoperability standard, contributed to Linux Foundation
- [CrowdStrike Prompt Injection Taxonomy](https://www.crowdstrike.com/en-us/resources/infographics/taxonomy-of-prompt-injection-methods/) — 185+ named prompt injection techniques across direct and indirect paths
- [Arcanum PI Taxonomy v1.5](https://arcanum-sec.github.io/arc_pi_taxonomy/) — four-dimension classification: attack intents, techniques, evasions, and inputs
- [OWASP AI Testing Guide v1 (November 2025)](https://www.practical-devsecops.com/owasp-ai-testing-guide-explained/) — first comprehensive AI trustworthiness testing standard, introduces DIE (Distributed, Immutable, Ephemeral) model
- [Microsoft: Skeleton Key Jailbreak (June 2024)](https://www.microsoft.com/en-us/security/blog/2024/06/26/mitigating-skeleton-key-a-new-type-of-generative-ai-jailbreak-technique/) — direct jailbreak technique that redefines safety rules in-context
- [International AI Safety Report 2026](https://internationalaisafetyreport.org/publication/international-ai-safety-report-2026) — evaluation gap and model collapse findings
- [EU AI Act GPAI Guidelines](https://artificialintelligenceact.eu/gpai-guidelines-overview/) — GPAI model obligations effective August 2025
- [EU AI Act Code of Practice Overview](https://artificialintelligenceact.eu/code-of-practice-overview/) — voluntary GPAI compliance framework
- [NIST AI 100-2e2025: Adversarial ML Taxonomy](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf) — updated adversarial ML attack classification
- [MCP Transport Future (December 2025)](https://blog.modelcontextprotocol.io/posts/2025-12-19-mcp-transport-future/) — streamable-HTTP replacing SSE
- [Trail of Bits: DataSig Dataset Fingerprinting (May 2025)](https://blog.trailofbits.com/2025/05/02/datasig-fingerprinting-ai/ml-datasets-to-stop-data-borne-attacks/) — dataset provenance verification
- [NSA/CISA: Content Credentials CSI (January 2025)](https://media.defense.gov/2025/Jan/29/2003634788/-1/-1/0/CSI-CONTENT-CREDENTIALS.PDF) — C2PA guidance for AI-generated content
- [MITRE ATLAS v5.5.0 Release (March 2026)](https://github.com/mitre-atlas/atlas-data/releases/tag/v5.5.0) — adds agent tool poisoning, AI supply-chain rug pull, reputation inflation, cost harvesting, AI service proxy, and related case-study updates
- [MITRE ATLAS v5.6.0 Release (May 2026)](https://github.com/mitre-atlas/atlas-data/releases/tag/v5.6.0) — adds AI agent configuration acquisition, code-repository discovery, and deepfake-assisted phishing updates
- [MITRE ATLAS Data](https://raw.githubusercontent.com/mitre-atlas/atlas-data/refs/heads/main/dist/ATLAS.yaml) — public machine-readable ATLAS data distribution used to track technique, mitigation, and case-study changes
- [OWASP GenAI Exploit Round-up Q1 2026](https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/) — incident summary showing exploitation trends around agent identity, orchestration layers, supply chain, prompt injection, and operational controls
- [MITRE ATLAS OpenClaw Investigation (February 2026)](https://www.mitre.org/news-insights/publication/mitre-atlas-openclaw-investigation) — real-world agent control-interface, poisoned skill, one-click RCE, sandbox escape, and prompt-injection C2 case studies (AML.CS0048–CS0051)
- [NIST IR 8596: Cyber AI Profile (December 2025 draft)](https://csrc.nist.gov/pubs/ir/8596/iprd) — extends CSF 2.0 for AI systems across Secure/Defend/Thwart focus areas and lists Spring 2026 working sessions
- [EU General-Purpose AI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai) — official Transparency, Copyright, and Safety and Security chapters plus live signatory list
- [OWASP AIBOM Generator (December 2025)](https://genai.owasp.org/resource/owasp-aibom-generator/) — open-source AIBOM tool producing CycloneDX output aligned with SPDX for Hugging Face model transparency
- [MCP 2025-06-18 Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) — resource indicators, token audience validation, and token-passthrough prohibition for remote MCP servers
- [Linux Foundation A2A One-Year Update (April 2026)](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) — production adoption update for agent-to-agent interoperability across major cloud platforms
- [Bessemer: Securing AI Agents — The Defining Challenge of 2026](https://www.bvp.com/atlas/securing-ai-agents-the-defining-cybersecurity-challenge-of-2026) — 48% of security professionals identify agentic AI as most dangerous attack vector
- [Prompt Injection Taxonomy for LLM Agents (February 2026)](https://arxiv.org/abs/2602.10453) — comprehensive survey of prompt injection threats with heuristic vs. optimization payload taxonomy

---

## Related Pages

- [Appendix B References](Appendix-B-References.md) — backs the glossary's standards and threat vocabulary with source references for MITRE ATLAS, MCP, NIST, OWASP, EU AI Act, and AI supply-chain material.
- [Appendix D Controls Inventory](Appendix-D-Controls-Inventory.md) — connects glossary terms such as SLSA, SCVS, PDP, SOC, and sandboxing to the control inventory language used across AISVS.
- [C03-04 Secure Development Practices](../chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md) — turns glossary terms such as prompt templates, AI BOMs, model registries, and isolated build environments into SDLC verification work.
- [C03-01 Model Authorization Integrity](../chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md) — grounds AI BOM, data lineage, model registry, signing, and provenance terms in model-admission controls.
- [C03-02 Model Validation Testing](../chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md) — connects validation, evaluation harness, quantization, MCP, and agent-release terminology to release-gate evidence.

---

## Community Notes

_Discussion about glossary scope, definitions, and consistency._

---

[README](../README.md)
