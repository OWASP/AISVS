# Appendix A: Glossary — Research Notes

> **Source:** [`1.0/en/0x90-Appendix-A_Glossary.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x90-Appendix-A_Glossary.md)

## Overview

The glossary defines 152 terms used throughout the AISVS, covering AI/ML concepts, security terminology, and domain-specific definitions. This research page cross-references every glossary term to the chapters that use it, identifies missing terms, flags definitions that could be improved, and tracks emerging terminology from the broader AI security community. Cross-references follow the AISVS **C01–C12** chapter structure: monitoring and logging terms map to **C12 (Monitoring and Logging)**, and explainability and human-oversight terms map to **C07 (Model Behavior)** for interpretability and **C09 (Orchestration and Agentic Action)** for oversight, kill-switches, and human-in-the-loop controls.

As of July 2026, the analysis identifies 49 high-priority missing terms, 12 medium-priority missing terms, 12 definitions needing improvement, and 66 emerging terms from the 2025–2026 threat landscape that may warrant future inclusion. The [June 22 glossary revision](https://github.com/OWASP/AISVS/commits/main/1.0/en/0x90-Appendix-A_Glossary.md) closed two previously tracked gaps by defining **System Prompt** and **Indirect Prompt Injection**, and added seven other security-relevant entries: **Alignment**, **DPoP**, **Excessive Agency**, **Inference**, **LLM**, **Sender-Constrained Token**, and **Trust Boundary**.

MITRE ATLAS has settled into monthly releases. The May 4, 2026 v5.6.0 release added the Acquire Public AI Artifacts: AI Agent Configuration technique and the Deepfake-Assisted Phishing sub-technique, while the March 31, 2026 v5.5.0 release introduced twelve techniques covering agent tool poisoning persistence (AML.T0110), AI supply chain rug pulls (AML.T0109), reputation inflation (AML.T0111), AI service proxies (AML.T0008.005), agentic resource consumption (AML.T0034.002), and call chains (AML.T0084.003), plus five case studies including MCP server poisoning and model distillation campaigns. The May 6, 2026 Secure AI v2 release from MITRE's Center for Threat-Informed Defense (CTID) and Zenity Labs added more than 45 techniques and sub-techniques, more than 10 mitigations, and more than 20 case studies across the full 2025–2026 work cycle, plus a new Technique Maturity filter that lets defenders prioritize emerging versus mature threats and an interactive ATLAS Knowledge Graph. The OpenClaw investigation case studies (AML.CS0048–CS0051) documented exposed agent control interfaces, poisoned skills, one-click RCE, sandbox escape, and prompt-injection-driven command and control. On May 27, 2026, ATLAS retired the v5.x numbering in favor of a split content/format versioning scheme: the v2026.05 content release pairs with format v6.0.0, which restructures the data model (typed relationship objects, schema validation, a REST API) and adds a `platforms` field tagging every technique as Predictive AI, Generative AI, Agentic AI, or Enterprise — a structural release that introduced no new technique or case-study IDs.

OWASP also stepped up the agentic and MCP guidance. The OWASP GenAI Security Project published *A Practical Guide for Secure MCP Server Development* in February 2026 with concrete controls for architecture, authentication, validation, session isolation, and hardened deployment; the OWASP MCP Top 10 (MCP01:2025 through MCP10:2025) continues to expand with categories such as token mismanagement, tool poisoning, shadow MCP servers, and context oversharing; and the March 2026 *OWASP GenAI Data Security Risks & Mitigations 2026 v1.0* introduced 21 data-layer risk categories (DSGAI01–DSGAI21) organized into Foundational, Hardening, and Advanced mitigation tiers. The April 20, 2026 disclosure of an Anthropic MCP design vulnerability — unsafe defaults in the stdio transport that enable arbitrary OS command execution across the Python, TypeScript, Java, and Rust SDKs, with related CVEs including CVE-2025-49596 (MCP Inspector) and CVE-2026-30623 (LiteLLM) — pushed practical MCP hardening to the top of agentic security priority lists. The pressure has not let up: CISA added the LiteLLM MCP test-endpoint command injection (CVE-2026-42271, patched May 8) to the Known Exploited Vulnerabilities catalog on June 9, 2026, and the NSA's Artificial Intelligence Security Center released its first MCP-specific Cybersecurity Information Sheet on May 20, 2026 (U/OO/6030316-26), recommending data-classification-zone segregation of tools and filtering egress proxies. OX Security framed the stdio command-execution problem as a systemic supply-chain flaw in its April 15, 2026 "Mother of All AI Supply Chains" advisory, reporting 10 Critical/High CVEs across popular MCP projects (including CVE-2026-30623 in LiteLLM, CVE-2026-30615 in Windsurf, CVE-2026-26015 in DocsGPT, and CVE-2026-33224 in Bisheng), 150M+ downloads of affected packages, 7,000+ publicly exposed servers, up to ~200,000 vulnerable instances, and successful compromise of 9 of 11 MCP registries in testing. The CVE stream has continued into June 2026 with unauthenticated MCP command-execution and injection flaws such as CVE-2026-33032 (nginx-ui MCP endpoint, CVSS 9.8) and CVE-2026-0755 (gemini-mcp-tool, CVSS 9.8), now tracked alongside dozens of others in the community-maintained Vulnerable MCP Project database. The MCP specification itself is evolving fast — the 2025-11-25 revision is now current (OIDC Discovery, Client ID Metadata Documents, mandatory 403 on invalid Origin), and the 2026-07-28 release candidate announced May 21, 2026 removes the session handshake entirely (stateless MCP), tightens OAuth alignment, and formally deprecates Roots, Sampling, and Logging. OWASP's *State of Agentic AI Security and Governance* v2.01 (June 1, 2026) rounds out the picture, mapping prompt injection to six of its ten agentic risk categories and popularizing Meta's "Agents Rule of Two" design constraint.

On the regulatory side, NIST's draft Cyber AI Profile (IR 8596) moved through Spring 2026 working sessions on April 28, May 5, and May 12, 2026 after the January 30 comment-period close; as of July 12, 2026 the December 2025 preliminary draft remains the latest public version, with the initial public draft still expected later in 2026. The EU's transparency track hit two milestones in June 2026: the consultation on the draft Article 50 guidelines closed June 3, and the final Code of Practice on Transparency of AI-Generated Content was published June 10, 2026 — covering provider marking/detection duties under Article 50(2) and deployer disclosure duties under Article 50(4), accompanied by a standardized labelling icon set, with the Commission/AI Board adequacy assessment underway. The Commission [opened the signing process](https://digital-strategy.ec.europa.eu/en/faqs/signing-code-practice-transparency-ai-generated-content) in July; providers seeking inclusion in the initial signatory list published before August 2 must submit their forms by July 22, 2026. The May 7, 2026 Digital Omnibus provisional trilogue agreement reshuffled the timeline: Annex III high-risk obligations slip from August 2, 2026 to December 2, 2027, Article 50 duties for systems already on the market defer to December 2, 2026, and a new prohibition on AI-generated non-consensual intimate imagery and CSAM takes effect December 2, 2026 — while GPAI enforcement powers (fines up to 3% of global turnover) still activate on August 2, 2026 as scheduled. Non-human identity (NHI) telemetry from CSA, DoControl, and ManageEngine has also matured: industry reports converged on NHI-to-human ratios of 45:1 to 100:1 (some Fortune 500 environments exceeding 500:1), with 50% of enterprises reporting an NHI-related breach and 68% of identity incidents involving machine identities.

---

## Term-to-Chapter Cross-Reference

Every glossary term mapped to the AISVS chapters that reference or rely on it.

| Term | Chapters |
|------|----------|
| Adapter | C03 |
| Adversarial Example | C02, C11 |
| Adversarial Robustness | C11 |
| Adversarial Training | C01, C02, C11 |
| Agent | C02, C05, C09, C10, C11, C12 |
| AI BOM / AIBOM / MBOM | C03, C06 |
| Alignment | C03, C11 |
| AppArmor | C04 |
| Attention Map | C07 |
| ABAC | C02, C05 |
| Backdoor Attack | C06, C11 |
| Bias | C01, C06, C11 |
| Bias Exploitation | C01, C11 |
| Blue-Green Deployment | C03 |
| Byzantine Fault Tolerance | C04 |
| Canary Deployment | C03 |
| Cedar | C05 |
| Certified Robustness | C11 |
| Chain of Thought | _(none — consider removing or linking to C07)_ |
| CI/CD | C04, C06, C09 |
| Circuit Breaker | C09, C10 |
| CMP | C12 |
| Concept Drift | C12 |
| Confidential Computing | C04 |
| Confidential Inference | C04 |
| Constitutional AI | C11 |
| Context Window | C02, C09 |
| Counterfactual Explanation | C07 |
| Covert Channel | C04, C12 |
| CycloneDX | C03, C06 |
| DAG | C09, C12 |
| Data Augmentation | C01 |
| Data Drift | C12 |
| Data Leakage | C08, C12 |
| Data Lineage | C01, C03, C06 |
| Data Minimization | C12 |
| Data Poisoning | C01, C06, C11, C12 |
| Defense-in-Depth | _(general principle, not cited by specific requirement)_ |
| Defensive Distillation | C02 |
| Differential Privacy | C11, C12 |
| DoS | C02, C04, C09, C12 |
| Downgrade (response) | C12 |
| DPIA | C12 |
| DPoP (Demonstrating Proof-of-Possession) | C10 |
| DP-SGD | C11 |
| DRTM | C04 |
| Embeddings | C05, C08 |
| Embedding Inversion | C08 |
| Excessive Agency | C07, C09 |
| Exfiltration | C08, C09, C10, C12 |
| Explainability | C07 |
| Fail-Closed / Fail-Open | C03, C09, C10 |
| Feature Attribution | C07 |
| Federated Learning | C04, C12 |
| Fine-tuning | C01, C03, C06 |
| FIPS 140-3 | C04 |
| Guardrails | C02, C03, C07, C11 |
| Hallucination | C07, C12 |
| Homoglyph | C02 |
| HSM | C04 |
| Human-in-the-Loop (HITL) | C02, C07, C09, C11 |
| Indirect Prompt Injection | C02, C07, C08, C10 |
| Inference | C04, C05, C09, C11, C12 |
| Infrastructure as Code (IaC) | _(none — consider removing or linking to C04)_ |
| Interval-Bound Propagation | C11 |
| Jailbreak | C02, C11, C12 |
| JIT (Just-in-Time) Privileged Access | C05 |
| JWT | C05 |
| k-anonymity | C12 |
| Kill-Switch | C09 |
| KMS | C04, C08 |
| Labeling | C01 |
| l-diversity | C12 |
| Least Privilege | C04, C09, C10 |
| LIME | C07 |
| Linkage Attack | C12 |
| LLM (Large Language Model) | C02, C05, C12 |
| Machine Unlearning | C12 |
| Many-Shot Jailbreaking | C02, C07, C11 |
| MCP | C02, C03, C09, C10 |
| Membership Inference Attack | C08, C11 |
| MIG | C04 |
| MITRE ATLAS | C02, C03, C11 |
| Model Card | C03, C07 |
| Model Extraction | C11, C12 |
| Model Inversion | C11, C12 |
| Model Lifecycle Management | C03 |
| Model Poisoning | C06, C11 |
| mTLS | C04 |
| Multi-agent System | C08, C09, C11 |
| Non-repudiation | C09, C12 |
| NFC | C02 |
| NVLink | C04 |
| OAuth 2.1 | C10 |
| OIDC | C05 |
| OPA | C05 |
| PDP (Policy Decision Point) | C05, C09 |
| PII | C01, C05, C06, C07, C12 |
| Policy-as-Code | C09, C12 |
| PPML | C11, C12 |
| Prompt Injection | C02, C07, C08, C10, C11, C12 |
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
| Scanned | C01, C04, C06 |
| SCVS | General guidance, Appendix B; supports C06 |
| Secure Boot | C04 |
| SMPC | C04 |
| seccomp | C04 |
| SELinux | C04 |
| Sender-Constrained Token | C10 |
| Sensitive Fields | C01, C08, C12 |
| Shadow Deployment | C03 |
| Shadow Model | C11, C12 |
| SHAP | C07 |
| Side-Channel Attack | C04 |
| SIEM | C12 |
| SLSA | General guidance, Appendix B; supports C06 |
| SOC | C02, C12 |
| SPDX | C03 |
| SSE | C10 |
| Steganography | C02 |
| stdio | C10 |
| Strong Authentication | C04, C05 |
| Supply Chain Attack | C06 |
| Synthetic Data | C01, C12 |
| System Prompt | C07, C09, C12 |
| TEE | C04 |
| Temperature Scaling | C11 |
| TLS | C04, C09, C10 |
| Tokenizer | C02, C03 |
| TPM | C04 |
| Transfer Learning | C06 |
| Trust Boundary | C02, C05, C09, C10 |
| Vector Database | C05, C08 |
| VRAM | C04 |
| Vulnerability Scanning | C06 |
| WASM | C09 |
| Watermarking | C01, C07, C11 |
| WORM | C04, C09 |
| Zero Standing Privilege (ZSP) | C05, C09 |
| Zero-Day Vulnerability | _(none — consider removing or linking to C06)_ |
| Zero-Trust | C04, C05 |

**Stats:** 3 terms still have no direct chapter reference (Chain of Thought, Infrastructure as Code, Zero-Day Vulnerability), while SCVS and SLSA appear in the general usage guidance and controls inventory rather than a single requirement chapter. Cross-references are resolved against all C01–C12 source files as of June 2026.

---

## Missing Terms (High Priority)

Terms used in AISVS chapters but not defined in the glossary. These should be added.

| Term | Used In | Context |
|------|---------|---------|
| Instruction Hierarchy | C02 | Defense concept where system/developer messages take priority over user inputs |
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
| Schema Drift | C12 | Monitoring concept for detecting input/output schema changes |
| Stop Sequences | C07 | LLM output control mechanism for bounding generation |
| Canary-Based Privacy Auditing | C12 | Specialized technique for testing differential privacy guarantees |
| Krum / Trimmed-Mean | C12 | Byzantine-resilient aggregation methods for federated learning |
| Output Perturbation | C11 | Privacy technique for membership inference defense |
| DNS Rebinding | C10 | Specific network attack vector for MCP server exploitation |
| Common Criteria / EAL4+ | C04 | Security certification standard for hardware components |
| InfiniBand / RDMA / NCCL | C04 | AI accelerator interconnect technologies |
| Evaluation Harness | C03 | Testing framework for systematic model evaluation |
| Reasoning Trace | C09, C12 | Agentic decision recording concept for audit trails |
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
| Least Agency | C09 | OWASP Agentic Top 10 principle that agents should receive only the minimum autonomy required for their authorized task; extends least privilege to cover scope of autonomous action |
| DIE Model (Distributed, Immutable, Ephemeral) | C04, C09 | Architecture paradigm from the OWASP AI Testing Guide (November 2025) that shifts from hardening individual AI components to making the entire system resilient through distribution, immutability, and ephemerality |
| Shadow MCP Server | C06, C10 | Unapproved or unsupervised MCP server deployments operating outside formal security governance, frequently with default credentials, permissive configurations, or unsecured APIs. OWASP MCP Top 10 formalizes the term as a 2026 risk category, and OWASP's *Practical Guide for Secure MCP Server Development* (February 2026) provides remediation guidance |
| Tool Manifest Validation | C09, C10 | Pre-invocation review of MCP tool definitions, descriptions, and schemas to detect hidden instructions, role escalation requests, or behavioral drift between published and deployed versions; foundational defense surfaced by the MCPTox benchmark, which reported >60% attack-success rates against o1-mini, DeepSeek-R1, and similarly capable agents |

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
| System Prompt Leakage | C07, C12 | Extraction of embedded system instructions, secrets, or configuration from an LLM; OWASP LLM Top 10 2025 entry LLM07:2025 |
| Vector and Embedding Weaknesses | C08, C12 | Vulnerabilities in vector stores and embedding pipelines including inversion and poisoning; OWASP LLM Top 10 2025 entry LLM08:2025 |
| GenAI Data Security Risk (DSGAI) | C01, C08, C12 | OWASP taxonomy released in March 2026 covering 21 data-layer risk categories (DSGAI01–DSGAI21) for LLM, GenAI, and agentic systems, organized into Foundational, Hardening, and Advanced mitigation tiers spanning leakage, access, poisoning, governance, vector stores, observability, context construction, model extraction, and trusted retrieval |

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
| Human-on-the-Loop | Governance model where a human supervises and can intervene but does not approve each individual action; contrast with HITL | C09 |
| Agentic Control Plane | Governance layer managing identity, authorization, orchestration, and trust for autonomous AI agents — analogous to the Kubernetes control plane but for agents | C09, C05, C12 |
| Agentic Identity | The principle that every AI agent is an identity requiring authentication, access control, policy enforcement, and auditability — the same governance applied to human identities. As agents accumulate entitlements across databases, cloud services, and repositories, they become high-value targets. The major identity providers all shipped agent-identity platforms by mid-2026: Microsoft Entra Agent ID (agents as first-class OAuth identities with blueprints and workload identity federation for third-party agents), Okta for AI Agents (GA April 30, 2026, with agent discovery, an Agent Gateway, and Universal Logout), and Auth0's May 2026 MCP-server and autonomous-agent identity controls | C05, C09, C10 |
| Publish Poisoned AI Agent Tool (AML.T0104) | MITRE ATLAS technique (February 2026) where adversaries create malicious versions of legitimate MCP tools that appear safe in descriptions and metadata but execute harmful actions when invoked — the supply-chain analogue of tool poisoning | C10, C06 |
| Escape to Host (AML.T0105) | MITRE ATLAS technique (February 2026) for breaking out of agent sandbox environments; the OpenClaw investigation found a 200ms race condition window during sandbox initialization where code has unrestricted host access | C04, C09 |
| AI Agent Tool Poisoning (AML.T0110) | Persistence technique where an adversary compromises tools already integrated into an agent environment, including built-in tools or MCP-connected tools, so future agent runs continue to execute attacker-controlled behavior | C09, C10, C06 |
| Agentic Resource Consumption (AML.T0034.002) | Cost-harvesting pattern where an attacker induces agents to burn tokens, tool calls, compute, API quota, or downstream service spend through loops, oversized context, or expensive delegated workflows | C09, C10, C12 |
| AI Service Proxy (AML.T0008.005) | Adversary infrastructure that resells or brokers access to commercial model APIs, useful for large-scale distillation, command generation, phishing content, or evading single-account throttles | C06, C11, C12 |
| MCPTox Benchmark | Tool-poisoning evaluation harness covering 45 real-world MCP servers, 353 authentic tools, and 1,312 malicious test cases (Wang et al., AAAI 2026 / arXiv 2508.14925); documented attack success rates such as 72.8% against o1-mini and refusal rates under 3% for Claude-3.7-Sonnet, with the counterintuitive pattern that more capable models often fall harder because their instruction-following is stronger | C10, C09 |
| Shadow MCP Server | OWASP MCP Top 10 term for unsanctioned MCP servers that bypass governance, often using default credentials, permissive configurations, or unsecured APIs — analogous to shadow IT but bridging untrusted tools directly into agent contexts | C10, C04, C06 |
| Technique Maturity (ATLAS) | Filter introduced in the MITRE Secure AI v2 release (May 2026) that classifies ATLAS techniques as emerging or mature so defenders can prioritize coverage against the highest-evidence threats before chasing speculative ones | C11, C12 |
| Agents Rule of Two | Meta design constraint, popularized by OWASP's *State of Agentic AI Security and Governance* v2.01 (June 2026): an agent operating without human approval in the loop should satisfy at most two of three properties — access to private data, exposure to untrusted content, and ability to communicate externally. A simpler operational sibling of the "lethal trifecta" framing | C09 |
| Stateless MCP | Architecture introduced in the MCP 2026-07-28 release candidate (announced May 21, 2026) that removes the protocol's session handshake entirely so servers work behind plain load balancers; client metadata moves into request payloads, and Roots, Sampling, and Logging are formally deprecated with a 12-month removal window | C10 |
| Cross App Access (XAA) | Protocol extension surfaced in Okta's agentic identity GA wave (April–May 2026) that lets an identity provider broker agent access across applications without per-app credential sprawl, alongside agent discovery/registration and an Agent Gateway control plane | C05, C09 |
| Universal Logout (Agent Kill Switch) | Identity-layer revocation primitive that instantly terminates all sessions and tokens for a compromised or misbehaving agent across connected applications; the identity-provider counterpart to the C9.6 kill-switch requirement | C05, C09 |
| Data Classification Zone (MCP) | NSA AISC recommendation (May 20, 2026 CSI, U/OO/6030316-26) to segregate MCP tools and models by data sensitivity zones, with filtering egress proxies or enterprise DLP pinning resource URLs for external MCP connections | C10, C04, C05 |

### Novel Attack Patterns

| Term | Definition | Relevant To |
|------|-----------|-------------|
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
| AI Voice Cloning | Use of generated or cloned speech to impersonate trusted people in phishing, approval fraud, help-desk abuse, or high-risk authorization flows; MITRE ATLAS now tracks this under Deepfake-Assisted Phishing (AML.T0052.001) | C05, C12 |
| MCP stdio RCE | Unsafe defaults in MCP stdio transport servers that let an attacker land arbitrary OS command execution via configuration files or hidden marketplace transitions; disclosed April 20, 2026, affecting Anthropic SDKs across Python, TypeScript, Java, and Rust with documented impact on 7,000+ publicly reachable servers (related CVEs CVE-2025-49596 in MCP Inspector and CVE-2026-30623 in LiteLLM). OX Security's April 15, 2026 "Mother of All AI Supply Chains" advisory characterized this as a systemic architectural flaw — user input flowing into stdio server parameters — spanning 10 Critical/High CVEs (LiteLLM, Windsurf CVE-2026-30615, DocsGPT CVE-2026-26015, Bisheng CVE-2026-33224, GPT Researcher, Agent Zero, and others), 150M+ package downloads, up to ~200,000 vulnerable instances, and successful compromise of 9 of 11 MCP registries. The pattern continues to generate CVEs through June 2026, including CVE-2026-33032 (nginx-ui MCP endpoint, CVSS 9.8) and CVE-2026-0755 (gemini-mcp-tool, CVSS 9.8) | C04, C09, C10 |
| Store Now, Decrypt Later (SNDL) | Adversary strategy of harvesting encrypted AI traffic — model prompts, retrieval queries, agent traces — and storing it for post-quantum decryption once cryptographically relevant quantum computers exist; drives the 2026 push toward hybrid post-quantum key exchange (ML-KEM / NIST FIPS 203) on MCP and agent control-plane channels | C04, C10 |
| Autonomous Post-Exploitation Agent | First confirmed in-the-wild attack where an LLM agent autonomously ran an entire post-exploitation chain (Sysdig TRT, observed May 10, published May 28, 2026): Marimo notebook RCE (CVE-2026-39987) → AWS credential harvest → SSH key theft from Secrets Manager → PostgreSQL exfiltration across four pivots in under 60 minutes, with the agent phase under 2 minutes. Detection markers included sub-second machine-formatted command sequences and planning comments leaking across IPs | C09, C12 |
| Tokenizer Tampering | Supply-chain technique that manipulates a model's tokenizer vocabulary to alter outputs at the decode stage without touching weights — invisible to weight-hash integrity checks and able to survive fine-tuning (named May 2026) | C06, C11 |
| Response Poisoning | Tampering with outputs of unauthenticated or exposed model-serving endpoints so downstream agent workflows consume attacker-influenced responses; a June 2026 scan found 1,652 unauthenticated Ollama APIs serving live models among ~1M exposed AI services | C04, C05 |
| MCP Test-Endpoint Command Injection | CVE-2026-42271 (CVSS 8.7): LiteLLM MCP preview endpoints spawned attacker-supplied command/args/env as subprocesses with full proxy privileges; patched in 1.83.7 on May 8, 2026 and added to the CISA KEV catalog on June 9, 2026 with active exploitation observed | C10, C04 |

### Governance & Compliance

| Term | Definition | Relevant To |
|------|-----------|-------------|
| GPAI (General-Purpose AI) Model | EU AI Act term for models trained with >10²³ FLOPs displaying significant generality; subject to transparency and safety obligations since August 2025 including technical documentation and copyright compliance | C03, C06 |
| Systemic Risk (EU AI Act) | Classification for GPAI models trained with >10²⁵ FLOPs, triggering mandatory adversarial red-teaming, incident reporting to the AI Office, and cybersecurity obligations under Article 55 | C03, C11 |
| FRIA (Fundamental Rights Impact Assessment) | EU AI Act Article 27 mandatory assessment for deployers of high-risk AI systems, evaluating impacts on non-discrimination, privacy, and human dignity; originally required by August 2026, deferred to December 2, 2027 alongside the Annex III high-risk obligations by the May 7, 2026 Digital Omnibus provisional agreement (formal adoption expected mid-2026). May complement a DPIA under GDPR Article 35 | C12 |
| Digital Omnibus on AI | Provisional Council/Parliament trilogue agreement (May 7, 2026) that defers Annex III high-risk obligations from August 2, 2026 to December 2, 2027, defers Annex I product-embedded high-risk duties to August 2, 2028, pushes Article 50 transparency for systems already on the market to December 2, 2026, and adds a new prohibition on AI-generated non-consensual intimate imagery and CSAM effective December 2, 2026; new dates bind only on Official Journal publication (~July 2026) | C03, C07 |
| Post-Market Monitoring | EU AI Act Article 72 requirement for high-risk AI providers to actively collect and review performance data throughout the system's lifetime | C12, C03 |
| Code of Practice (EU AI Act) | Voluntary framework for GPAI model providers to demonstrate compliance with AI Act obligations; the official July 2025 code has Transparency, Copyright, and Safety and Security chapters, and the European Commission's April 2026 page lists active signatories | C03, C06 |
| Cyber AI Profile (NIST IR 8596) | Draft NIST profile (December 2025; comment period closed January 30, 2026) extending CSF 2.0 to AI systems across three focus areas: Secure (protecting AI systems), Defend (using AI for cyber defense), and Thwart (building resilience against AI-enabled attacks). NIST ran the Spring 2026 working sessions on April 28, May 5, and May 12, 2026; as of June 11, 2026 the preliminary draft remains the latest public version, with the initial public draft still expected later in 2026 | C03, C11, C12 |
| COSAiS (NIST SP 800-53 AI Control Overlays) | NIST project (IR 8605 series) developing five SP 800-53 control overlays for securing AI systems — generative AI assistants, predictive AI fine-tuning, single-agent, multi-agent, and AI development; the January 8, 2026 annotated outline for the predictive AI overlay is the latest public artifact, with no initial public draft released as of June 2026 | C03, C09 |
| Article 50 Transparency Obligations (EU AI Act) | Disclosure regime for AI systems that interact with people, generate synthetic content, or perform emotion recognition; the May 2026 draft Commission guidelines clarified provider/deployer duties (consultation closed June 3, 2026; final guidelines pending before the August 2, 2026 applicability date), and the final Code of Practice on Transparency of AI-Generated Content — published June 10, 2026 with a standardized labelling icon set — is the operational companion, covering Article 50(2) machine-readable marking/detection for providers and Article 50(4) deepfake and AI-text disclosure for deployers | C03, C07 |

### Interoperability & Agent Protocols

| Term | Definition | Relevant To |
|------|-----------|-------------|
| A2A (Agent2Agent Protocol) | Open protocol (Google, April 2025; contributed to Linux Foundation June 2025) enabling AI agents to discover capabilities, exchange context, and coordinate tasks across vendors and frameworks. Uses Agent Cards for capability discovery and supports enterprise-grade auth. The protocol reached v1.0.0 on March 12, 2026 — a breaking release adding `tasks/list` with filtering and pagination, OAuth 2.0 modernization (device code flow plus PKCE), and gRPC multi-tenancy — followed by the v1.0.1 patch on May 28, 2026; the Linux Foundation reported 150+ supporting organizations at the protocol's first anniversary in April 2026 | C09, C10 |
| Agent Card | JSON-format capability descriptor in the A2A protocol that advertises an agent's supported tasks, authentication requirements, and interaction modes to other agents | C09, C10 |
| Non-Human Identity (NHI) | Machine or agent identity used for authentication and authorization in automated workflows. May 2026 industry data converges on NHI-to-human ratios of 45:1 to 100:1 (CSA, DoControl, Rubrik Zero Labs, ManageEngine), with Fortune 500 environments reporting upwards of 500:1; 50% of enterprises now report an NHI-related breach, 68% of identity incidents involve machine identities, 47% of NHIs are over a year old without credential rotation, and only 12% of organizations rate their NHI defenses as highly mature. Three of the OWASP Agentic Top 10 risks (ASI02, ASI03, ASI04) are identity-focused | C05, C09, C10 |

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
| ASI08 — Cascading Failures | Error or attack in one agent propagates through multi-agent workflows, amplifying impact | C09, C12 |
| ASI09 — Human-Agent Trust Exploitation | Agents exploit user trust to obtain approvals for actions the user does not fully understand | C09 |
| ASI10 — Rogue Agents | Agents that deviate from intended behavior due to misalignment, compromise, or emergent goal-seeking | C11, C09 |

### Provenance & Transparency

| Term | Definition | Relevant To |
|------|-----------|-------------|
| C2PA (Coalition for Content Provenance and Authenticity) | Open standard for embedding cryptographically signed metadata into digital content to verify origin, edit history, and AI involvement; increasingly mandated by EU and California regulations | C07, C03 |
| Content Provenance | Verifiable chain of origin, creation method, and modification history for digital content; encompasses C2PA, watermarking, and fingerprinting approaches | C07, C12 |
| Shadow AI | Unauthorized use of AI tools by employees without organizational vetting or controls; 2025 industry data shows 77% of enterprise AI users have pasted company data into unapproved chatbots | C05, C12 |

---

## Definitions Needing Improvement

Existing glossary definitions that could better reflect how terms are used in the chapters.

| Term | Issue | Suggested Improvement |
|------|-------|----------------------|
| Circuit Breaker | Needs explicit MCP tool-chain context | Add: "In agentic and MCP-connected systems, circuit breakers also apply to tool invocation chains, halting cascading calls when step counts, latency, or cost thresholds are exceeded (C10.5.2)." |
| Guardrails | Only mentions "constraints" | Add: "Guardrails may be implemented as dedicated safety classifier models, rule-based filter systems, or separate validation services that evaluate inputs and outputs independently of the primary model." |
| MCP | Missing key technical details; spec is moving fast | Add: "MCP uses JSON-RPC 2.0 as its messaging format and supports stdio and Streamable HTTP transports. Since 2025-06-18 the specification classifies remote MCP servers as OAuth resource servers, requires resource indicators to bind tokens to the intended MCP server, and forbids token passthrough to downstream APIs. The current 2025-11-25 revision adds OIDC Discovery, Client ID Metadata Documents for client registration, incremental scope consent, and mandates HTTP 403 on invalid Origin headers; the 2026-07-28 release candidate moves to a fully stateless protocol and deprecates Roots, Sampling, and Logging." |
| Prompt Injection | Doesn't distinguish direct vs. indirect | Add: "Includes both direct injection (user crafts malicious input) and indirect injection (adversarial instructions embedded in retrieved documents, tool outputs, or third-party data the model processes as trusted context). Indirect injection is particularly dangerous in RAG and agentic systems." |
| RAG | Too basic for how extensively AISVS covers it | Add: "RAG introduces distinct attack surfaces including retrieval poisoning, chunk-level traceability requirements, and citation integrity validation. See C08 for data store security and C02 for indirect prompt injection via retrieved content." |
| Watermarking | Doesn't enumerate distinct use cases | Add: "Serves three distinct purposes: dataset provenance marking to detect unauthorized training data use (C01), output media watermarking to identify AI-generated content (C07), and model weight watermarking as a defense against unauthorized extraction (C11)." |
| Data Poisoning | Only covers training-time | Add: "Can occur at training time (corrupting datasets or fine-tuning data) or at inference time (injecting adversarial content into RAG knowledge stores, vector databases, or retrieval sources). Inference-time poisoning does not require training pipeline access." |
| Model Card | Focuses on transparency only | Add: "Effective model cards also cover operational aspects: known failure modes, version history with change justification, deployment environment requirements, monitoring baselines, and lifecycle status (active, deprecated, retired). See C03 and C07." |
| Differential Privacy | Missing delta parameter | Replace epsilon-only clause with: "...quantified by an epsilon (ε) privacy budget bounding worst-case privacy loss and a delta (δ) parameter representing the probability of that bound being violated. DP-SGD implementations require specifying both; C12.3.1 mandates reporting both." |
| SSE | Doesn't note deprecation | Add: "SSE has been superseded by Streamable HTTP as MCP's primary remote transport since the 2025-03-26 specification revision. SSE-based MCP endpoints should be restricted to internal channels only (C10.3.3), and new deployments should prefer Streamable HTTP's simpler request/response backpressure and Origin validation model." |
| stdio | Missing usage restriction | Add: "C10.6.1 restricts stdio-based MCP transports to co-located, same-machine development scenarios only; stdio must not be used for production remote communication due to absent authentication and encryption." |
| Federated Learning | Missing security nuances | Add: "Introduces unique security considerations: local differential privacy on gradient updates before sharing, Byzantine-resistant aggregation (Krum, trimmed-mean), and canary-based privacy auditing. See C12.6." |

---

## MITRE ATLAS Technique Mapping

Key MITRE ATLAS techniques that correspond to AISVS glossary terms. As of June 2026, the latest release is v2026.05 (May 27, 2026), which retired the v5.x numbering in favor of split content (v2026.05) and format (v6.0.0) versioning — a structural release with no new technique or case-study IDs, but a new `platforms` field (Predictive AI, Generative AI, Agentic AI, Enterprise) on every technique. The last content-bearing release was v5.6.0 (May 4, 2026), and ATLAS has moved to a roughly monthly release cadence. The October 2025 update added the initial agentic AI coverage, the v5.2.0 / v5.3.0 January 2026 releases added MCP server case studies and agentic deployment techniques, the February 2026 v5.4.0 release expanded agent sandbox and poisoned-tool techniques through the OpenClaw investigation, the March 31, 2026 v5.5.0 release added supply-chain rug pulls, tool poisoning persistence, reputation inflation, cost-harvesting variants, AI service proxies, and call-chain discovery, and the May 4, 2026 v5.6.0 release added agent-configuration acquisition, code-repository discovery, and deepfake-assisted phishing coverage. The MITRE Center for Threat-Informed Defense Secure AI v2 release (May 6, 2026) bundled 45+ techniques and sub-techniques, 10+ mitigations, 20+ case studies, the new Technique Maturity filter, and the interactive ATLAS Knowledge Graph.

| ATLAS ID | Technique | Glossary Term(s) | AISVS Chapters |
|----------|-----------|-------------------|----------------|
| AML.T0010 | ML Supply Chain Compromise | Supply Chain Attack, Model Poisoning | C06, C11 |
| AML.T0018 | Backdoor ML Model | Backdoor Attack, Data Poisoning | C01, C06, C11 |
| AML.T0020 | Poison Training Data | Data Poisoning | C01, C06 |
| AML.T0024 | Exfiltration via ML Inference API | Model Extraction, Exfiltration | C11, C12 |
| AML.T0029 | Denial of ML Service | DoS | C02, C04, C09 |
| AML.T0040 | ML Model Inference API Access | Membership Inference Attack | C11, C12 |
| AML.T0043 | Craft Adversarial Data | Adversarial Example | C02, C11 |
| AML.T0047 | ML-Enabled Product/Service | Prompt Injection, Jailbreak | C02, C11 |
| AML.T0051 | LLM Prompt Injection | Prompt Injection | C02, C07, C10 |
| AML.T0054 | LLM Jailbreak | Jailbreak | C02, C11 |
| AML.T0056 | LLM Meta Prompt Extraction | System Prompt (missing term) | C07, C12 |
| AML.T0096 | AI Service API _(new, 2025)_ | Agent, Orchestrator (missing term) | C09, C10 |
| AML.T0098 | AI Agent Tool Credential Harvesting _(new, 2025)_ | RAG Credential Harvesting (emerging) | C09, C10, C05 |
| AML.T0099 | AI Agent Tool Data Poisoning _(new, 2025)_ | Tool Poisoning (emerging) | C09, C10, C06 |
| AML.T0100 | AI Agent Clickbait _(new, 2025)_ | Agent Clickbait (emerging) | C09, C10 |
| AML.T0101 | Data Destruction via AI Agent _(new, 2025)_ | Kill-Switch | C09, C10 |
| AML.T0103 | Deploy AI Agent _(new, Jan 2026)_ | Agent, Orchestrator (missing term) | C09, C05 |
| AML.T0104 | Publish Poisoned AI Agent Tool _(new, Feb 2026)_ | Tool Poisoning (emerging), Tool Squatting (emerging) | C10, C06 |
| AML.T0105 | Escape to Host _(new, Feb 2026)_ | Sandboxing, TEE | C04, C09 |
| AML.T0106 | Exploitation for Credential Access _(new, Feb 2026)_ | RAG Credential Harvesting (emerging) | C05, C09, C10 |
| AML.T0107 | Exploitation for Defense Evasion _(new, Feb 2026)_ | Adversarial Robustness | C11, C09 |
| AML.T0108 | AI Agent _(new, Feb 2026)_ | Agent | C09, C10, C05 |
| AML.T0109 | AI Supply Chain Rug Pull _(new, 2026)_ | Supply Chain Attack, Model Poisoning | C06, C03 |
| AML.T0110 | AI Agent Tool Poisoning _(new, 2026)_ | Tool Poisoning, MCP, Agent | C09, C10, C06 |
| AML.T0111 | AI Supply Chain Reputation Inflation _(new, 2026)_ | Supply Chain Attack, AI BOM / AIBOM | C06, C03 |
| AML.T0034.002 | Agentic Resource Consumption _(new, 2026)_ | DoS, Circuit Breaker | C09, C10, C12 |
| AML.T0084.003 | Call Chains _(new, 2026)_ | Orchestrator (missing term), Evaluation Harness (missing term) | C03, C09, C10 |
| AML.T0008.005 | AI Service Proxies _(new, 2026)_ | Model Extraction, Model Distillation (missing term) | C11, C12, C06 |
| AML.T0052.001 | Deepfake-Assisted Phishing _(new, 2026)_ | AI Voice Cloning (emerging), Strong Authentication | C05, C12 |

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
- [MITRE CTID: Secure AI v2 Release (May 6, 2026)](https://ctid.mitre.org/blog/2026/05/06/secure-ai-v2-release) — bundles 45+ ATLAS techniques, 10+ mitigations, 20+ case studies, the Technique Maturity filter, and the ATLAS Knowledge Graph
- [OWASP Practical Guide for Secure MCP Server Development (February 2026)](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/) — concrete controls for MCP server architecture, authn/authz, validation, session isolation, and deployment hardening
- [OWASP GenAI Data Security Risks & Mitigations 2026 v1.0 (March 2026)](https://genai.owasp.org/resource/owasp-genai-data-security-risks-mitigations-2026/) — 21-category DSGAI taxonomy with Foundational, Hardening, and Advanced mitigation tiers
- [OWASP MCP Top 10 Project](https://owasp.org/www-project-mcp-top-10/) — MCP01:2025 through MCP10:2025 categorization including shadow MCP servers, token mismanagement, and tool poisoning
- [Anthropic MCP Design Vulnerability (April 20, 2026)](https://thehackernews.com/2026/04/anthropic-mcp-design-vulnerability.html) — stdio transport unsafe defaults enable RCE across Anthropic SDKs (related CVE-2025-49596, CVE-2026-30623), affecting 7,000+ public servers
- [MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers (Wang et al., AAAI 2026 / arXiv 2508.14925)](https://arxiv.org/abs/2508.14925) — 45 live MCP servers, 353 tools, 1,312 attack cases, 72.8% success against o1-mini, <3% refusal from Claude-3.7-Sonnet
- [EU Article 50 Draft Guidelines (May 7, 2026)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) — transparency obligations for AI systems interacting with people, generating synthetic content, or performing emotion recognition; consultation open until June 3, 2026, applicable from August 2, 2026
- [CSA State of Non-Human Identity Security Survey](https://cloudsecurityalliance.org/artifacts/state-of-non-human-identity-security-survey-report) — primary source for the 45:1 to 100:1 NHI ratio range and the 50% NHI-breach figure cited above
- [MITRE ATLAS v2026.05 / Format v6.0.0 Release (May 27, 2026)](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.05) — split content/format versioning, typed relationships, schema validation, and the per-technique `platforms` field
- [Sysdig: LLM Agent Used for Post-Exploitation (May 28, 2026)](https://thehackernews.com/2026/05/attackers-use-llm-agent-for-post.html) — first confirmed in-the-wild autonomous agent-operated intrusion, from Marimo RCE (CVE-2026-39987) to database exfiltration in under an hour
- [OWASP State of Agentic AI Security and Governance v2.01 (June 1, 2026)](https://genai.owasp.org/resource/state-of-agentic-ai-security-and-governance/) — safety/security convergence argument, autonomy-level mapping, circuit breakers and kill switches for high-autonomy deployments
- [Help Net Security: OWASP Agentic Report Coverage (June 11, 2026)](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/) — prompt injection maps to 6 of 10 agentic risk categories; Agents Rule of Two; 37% shadow-AI detection adoption
- [MCP 2026-07-28 Release Candidate (May 21, 2026)](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) — stateless protocol, six authorization SEPs, MCP Apps and Tasks extensions, formal deprecation policy
- [MCP 2025-11-25 Specification Changelog](https://modelcontextprotocol.io/specification/2025-11-25/changelog) — current released revision: OIDC Discovery, Client ID Metadata Documents, incremental scope consent, 403-on-invalid-Origin
- [NSA AISC: MCP Security Design Considerations CSI (May 20, 2026)](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4496698/nsa-releases-security-design-considerations-for-ai-driven-automation-leveraging/) — first US government MCP-specific guidance (U/OO/6030316-26); data classification zones and filtering egress proxies ([analysis](https://www.reedsmith.com/our-insights/blogs/viewpoints/102mvg9/nsa-publishes-security-guidance-on-designing-ai-systems-with-model-context-protoc/))
- [A2A Protocol Releases](https://github.com/a2aproject/A2A/releases) — v1.0.0 (March 12, 2026) breaking release and v1.0.1 (May 28, 2026) patch
- [CybelAngel: LiteLLM CVE-2026-42271 Analysis](https://cybelangel.com/blog/itellm-vulnerability-cve-2026-42271/) — MCP test-endpoint command injection, patched May 8, 2026, CISA KEV June 9, 2026
- [EU Code of Practice on Transparency of AI-Generated Content (June 10, 2026)](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) — final code with provider marking/detection and deployer disclosure sections plus standardized labelling icons
- [EU transparency Code of Practice signing process (July 2026)](https://digital-strategy.ec.europa.eu/en/faqs/signing-code-practice-transparency-ai-generated-content) — official submission process and July 22 cutoff for inclusion in the initial signatory list before Article 50 applies
- [Gibson Dunn: EU AI Act Digital Omnibus Agreement (May 2026)](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/) — analysis of the May 7, 2026 provisional agreement deferring Annex III high-risk obligations to December 2, 2027
- [NIST COSAiS: SP 800-53 Control Overlays for Securing AI Systems](https://csrc.nist.gov/Projects/cosais) — five planned AI control overlays (IR 8605 series); predictive AI annotated outline published January 8, 2026
- [Okta Showcase 2026: Okta for AI Agents](https://www.okta.com/newsroom/press-releases/showcase-2026/) — agent discovery, Agent Gateway, Cross App Access, and Universal Logout for non-human identities
- [Adversa AI: Top GenAI Security Resources June 2026](https://adversa.ai/blog/top-genai-security-resources-june-2026/) — roundup naming Tokenizer Tampering, ChatGPhish, response poisoning of exposed Ollama APIs, and recent jailbreak research
- [Aperion Shield (open-sourced May 2026)](https://github.com/AperionAI/shield) — local Apache-2.0 guardrail that wraps MCP transports to block destructive tool calls before execution
- [OX Security: The Mother of All AI Supply Chains (April 15, 2026)](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) — systemic MCP stdio command-execution flaw with 10 Critical/High CVEs, 150M+ downloads, 7,000+ exposed servers, and 9-of-11 registry compromises
- [The Vulnerable MCP Project](https://vulnerablemcp.info/) — community-maintained database tracking MCP server CVEs and security flaws, including CVE-2026-33032 (nginx-ui) and CVE-2026-0755 (gemini-mcp-tool)
- [Authzed: A Timeline of Model Context Protocol Security Breaches](https://authzed.com/blog/timeline-mcp-breaches) — chronology of MCP security incidents and disclosures across 2025–2026

---

## Related Pages

- [Appendix B Controls Inventory](Appendix-B-Controls-Inventory.md) — connects glossary terms such as SLSA, SCVS, PDP, SOC, and sandboxing to the control inventory language used across AISVS.
- [C03-04 Secure Development Practices](../chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md) — turns glossary terms such as prompt templates, AI BOMs, model registries, and isolated build environments into SDLC verification work.
- [C03-01 Model Authorization Integrity](../chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md) — grounds AI BOM, data lineage, model registry, signing, and provenance terms in model-admission controls.
- [C03-02 Model Validation Testing](../chapters/C03-Model-Lifecycle-Management/C03-02-Model-Validation-Testing.md) — connects validation, evaluation harness, quantization, MCP, and agent-release terminology to release-gate evidence.

---

## Community Notes

_Discussion about glossary scope, definitions, and consistency._

---

[README](../README.md)
