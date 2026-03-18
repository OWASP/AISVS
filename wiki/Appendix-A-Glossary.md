# Appendix A: Glossary — Research Notes

> **Source:** [`1.0/en/0x90-Appendix-A_Glossary.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x90-Appendix-A_Glossary.md)

## Overview

The glossary defines 87 terms used throughout the AISVS, covering AI/ML concepts, security terminology, and domain-specific definitions. This research page cross-references every glossary term to the chapters that use it, identifies missing terms, and flags definitions that could be improved.

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
| Bias | C01, C06, C14 |
| Bias Exploitation | C01 |
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
| DoS | C02, C04, C13 |
| DPIA | C12 |
| DP-SGD | C11 |
| DRTM | C04 |
| Embeddings | C05, C08 |
| Explainability | C07, C14 |
| Feature Attribution | C07, C14 |
| Federated Learning | C04, C12 |
| Fine-tuning | C01, C03, C06 |
| FIPS 140-3 | C04 |
| Guardrails | C03, C07, C11 |
| Hallucination | C07, C13 |
| Homoglyph | C02 |
| HSM | C04 |
| Human-in-the-Loop (HITL) | C02, C07, C09, C14 |
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
| Multi-agent System | C08, C09 |
| NFC | C02 |
| NVLink | C04 |
| OAuth 2.1 | C10 |
| OIDC | C05 |
| OPA | C05 |
| PII | C01, C05, C06, C07, C12, C13 |
| Policy-as-Code | C09, C12 |
| PPML | C11, C12 |
| Prompt Injection | C02, C08, C10, C11, C13 |
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

**Stats:** 3 terms referenced by 0 chapters, ~20 terms by 1 chapter, ~30 terms by 3+ chapters.

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

---

## Definitions Needing Improvement

Existing glossary definitions that could better reflect how terms are used in the chapters.

| Term | Issue | Suggested Improvement |
|------|-------|----------------------|
| Agent | Too narrow — doesn't cover the spectrum from simple tool-calling to multi-step autonomous agents | Add: "Ranges from simple tool-calling agents to fully autonomous multi-step systems. See C05 for capability tokens, C09 for orchestration controls." |
| Circuit Breaker | Missing MCP context | Add "tool invocation chains" to the examples (C10.5.2) |
| Guardrails | Only mentions "constraints" | Note that guardrails can be separate safety models, classifiers, or rule-based systems |
| MCP | Missing key technical details | Mention transport types (streamable-HTTP, SSE, stdio), OAuth 2.1 requirement, JSON-RPC messaging |
| Prompt Injection | Doesn't distinguish direct vs. indirect | Add: "Includes both direct injection (user input) and indirect injection (via retrieved content, tool outputs, or third-party data)" |
| RAG | Too basic for how extensively AISVS covers it | Mention attack surfaces: retrieval poisoning, chunk-level traceability, citation integrity |
| Watermarking | Doesn't enumerate distinct use cases | Note three contexts: dataset watermarking (C01), output media watermarking (C07), model extraction defense (C11) |
| Data Poisoning | Only covers training-time | Add: "Can occur at training time or inference time (e.g., via RAG/vector database poisoning)" |
| Model Card | Focuses on transparency only | Add operational aspects: failure modes, version control, lifecycle maintenance (C14) |
| Differential Privacy | Missing delta parameter | Add "delta (delta)" alongside "epsilon (epsilon) privacy budget" per C12.3.1 |
| SSE | Doesn't note deprecation | Note SSE is being superseded by streamable-HTTP in MCP; C10.3.3 restricts it to internal channels |
| stdio | Missing usage restriction | Add that C10.6.1 restricts stdio to co-located, same-machine development scenarios only |
| Shadow Model | Too narrow | Also used for verifying data deletion effectiveness (C12.2.3) |
| Federated Learning | Missing security nuances | Hint at local DP, poisoning-resistant aggregation, canary auditing (C12.6) |

---

## Community Notes

_Discussion about glossary scope, definitions, and consistency._

---

[README](README.md)
