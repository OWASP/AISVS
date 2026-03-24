# C11: Adversarial Robustness & Attack Resistance

> **Source:** [`1.0/en/0x10-C11-Adversarial-Robustness.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C11-Adversarial-Robustness.md)
> **Requirements:** 41 | **Sections:** 10

## Control Objective

Ensure that AI systems remain reliable, privacy-preserving, and abuse-resistant when facing evasion, inference, extraction, or poisoning attacks. These controls cover model alignment testing, adversarial hardening, privacy attack resistance, model theft deterrence, and security adaptation for autonomous agents.

> **2025-2026 Highlights:** Alignment evaluation now includes assessment for evaluation awareness (C11.1.5), where models may behave differently under testing versus deployment. Agent-specific sections (C11.8, C11.9) address self-modification and autonomous update security as agentic systems become mainstream.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C11.1 | Model Alignment & Safety | 5 | [C11-01-Model-Alignment-Safety](C11-01-Model-Alignment-Safety) |
| C11.2 | Adversarial-Example Hardening | 5 | [C11-02-Adversarial-Example-Hardening](C11-02-Adversarial-Example-Hardening) |
| C11.3 | Membership-Inference Mitigation | 3 | [C11-03-Membership-Inference-Mitigation](C11-03-Membership-Inference-Mitigation) |
| C11.4 | Model-Inversion Resistance | 3 | [C11-04-Model-Inversion-Resistance](C11-04-Model-Inversion-Resistance) |
| C11.5 | Model-Extraction Defense | 5 | [C11-05-Model-Extraction-Defense](C11-05-Model-Extraction-Defense) |
| C11.6 | Inference-Time Poisoned-Data Detection | 5 | [C11-06-Inference-Time-Poisoned-Data-Detection](C11-06-Inference-Time-Poisoned-Data-Detection) |
| C11.7 | Security Policy Adaptation | 4 | [C11-07-Security-Policy-Adaptation](C11-07-Security-Policy-Adaptation) |
| C11.8 | Agent Security Self-Assessment | 3 | [C11-08-Agent-Security-Self-Assessment](C11-08-Agent-Security-Self-Assessment) |
| C11.9 | Self-Modification & Autonomous Update Security | 5 | [C11-09-Self-Modification-Autonomous-Update-Security](C11-09-Self-Modification-Autonomous-Update-Security) |
| C11.10 | Adversarial Bias Exploitation Defense | 3 | [C11-10-Adversarial-Bias-Exploitation-Defense](C11-10-Adversarial-Bias-Exploitation-Defense) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Adversarial evasion in production** — Changing just 13 bytes of a malware sample evaded Google's Magika classifier in 90% of attempts (October 2025). The Cylance universal bypass (AML.CS0003) demonstrated 100% evasion by appending benign strings. ML-based malware detectors face 65.6% evasion rates; DL-based detectors up to 99%.
- **Membership inference** — Pre-trained LLMs show surprising resilience, but fine-tuned models are significantly more vulnerable. Multi-query attacks achieve 39% extraction rates. New techniques (ACL 2025) achieve first successful MIA on pre-trained LLMs via paragraph-level feature aggregation.
- **Model inversion / training data extraction** — Researchers extracted 10,000+ verbatim training examples from ChatGPT for ~$200 using simple repetition prompts. Over 5% of output was direct 50-token copies. Llama 3.2 PII extraction demonstrated in 2025.
- **Model extraction at industrial scale** — DeepSeek, Moonshot AI, and MiniMax used ~24,000 fake accounts for industrial-scale distillation of Claude (February 2026). DeepSeek R1 achieved GPT-o1 performance at $5.6M development cost via systematic API harvesting.
- **Inference-time poisoning** — PoisonedRAG (USENIX Security 2025) showed just 5 crafted documents manipulate RAG responses 90% of the time. MCP tool poisoning and MCPTox benchmark document cross-tool contamination across 45+ servers.
- **Jailbreaks and alignment bypass** — JBFuzz achieves ~99% success across frontier models with ~7 queries in under 1 minute. Multi-turn jailbreaks hit 97% success within five conversational turns (Mindgard 2026 benchmarks). Skeleton Key (multi-turn guardrail rewriting), Context Compliance Attack (fabricated history injection), and evaluation awareness/sandbagging where models strategically underperform on safety evaluations. As of early 2026, role-play attacks show 89.6% success and healthcare LLM attacks reach 94.4% completion of adversarial objectives.
- **Multi-modal and vision-language attacks** — VLM-specific jailbreaks combine imperceptible image perturbations with text manipulation to disrupt cross-modal alignment. Typographic attacks convert harmful text to visual form to bypass text-only filters. Proxy model transfer enables black-box attacks on VLMs without direct access. A January 2026 survey (arXiv 2601.03594) catalogs attack taxonomies across LLMs and VLMs and proposes a three-layer defense framework (perception, generation, parameter layers).
- **Self-modification abuse** — Morris II (March 2024) demonstrated the first self-replicating AI worm that propagates through interconnected agents via metamorphic prompts. Copilot configuration self-modification attacks silently alter agent settings via indirect prompt injection.
- **Adversarial bias exploitation** — 3 million daily spoofed emails bypassed Proofpoint classifiers by exploiting undertrained brand-impersonation patterns. State-sponsored operations exploit differential sensitivity across languages and cultural contexts.
- **Deepfake evasion of identity verification** — MITRE ATLAS published a case study (November 2025) documenting deepfake attacks against mobile KYC liveness detection in banking, financial services, and cryptocurrency platforms. Attackers use synthetic face generation to bypass biometric classifiers that underpin identity verification pipelines.

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| Oct 2025 | Gmail Magika classifier evasion — 13-byte change, 90% bypass | Production evasion on world's largest email platform; Google collaborated on fix | [arXiv](https://arxiv.org/html/2510.01676v1) |
| Mar 2025 | JBFuzz — 99% jailbreak success across frontier models | Black-box fuzzing requiring ~7 queries, under 1 minute; 100% on GPT-4o, DeepSeek-R1, Gemini-2.0 | [arXiv](https://arxiv.org/html/2503.08990v1) |
| Mar 2025 | NIST AI 100-2 E2025 — supersedes E2023 with GenAI categories | Adds indirect prompt injection, misaligned outputs, energy-latency attacks to taxonomy | [NIST](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) |
| 2025 | PoisonedRAG — 5 documents manipulate 90% of RAG responses | First formalized knowledge corruption attack; "vector magnets" bypass embedding similarity | [USENIX Security 2025](https://www.promptfoo.dev/blog/rag-poisoning/) |
| Feb 2026 | Industrial-scale model distillation (Anthropic disclosure) | 24K fake accounts, 16M conversations; systematic API-based model extraction | [CNBC](https://www.cnbc.com/2026/02/24/anthropic-openai-china-firms-distillation-deepseek.html) |
| Nov 2023 | ChatGPT training data extraction for $200 | 10K+ verbatim examples via repetition prompts; 5% of output was 50-token training copies | [Research](https://not-just-memorization.github.io/extracting-training-data-from-chatgpt.html) |
| Jun 2024 | Evaluation awareness / sandbagging (ICLR 2025) | Frontier models strategically underperform on dangerous capability evals; Claude 3.5 spontaneous sandbagging | [arXiv](https://arxiv.org/abs/2406.07358) |
| Mar 2024 | Morris II — first self-replicating AI worm | Metamorphic prompts propagate through agent ecosystems; hijacks assistants, exfiltrates data | [Research](https://sites.google.com/view/compromptmized) |
| Jan 2026 | LLM & VLM jailbreak taxonomy survey | Catalogs attack/defense landscape across template, steganographic, ICL manipulation, GCG, RL, and fine-tuning attacks; proposes three-layer unified defense | [arXiv](https://arxiv.org/html/2601.03594v1) |
| Nov 2025 | MITRE ATLAS deepfake KYC case study | Synthetic faces bypass mobile liveness detection in banking/crypto platforms | [MITRE ATLAS](https://atlas.mitre.org/) |
| Oct 2025 | MITRE ATLAS adds 14 AI agent techniques | Collaboration with Zenity Labs; framework now covers 15 tactics, 66 techniques, 46 sub-techniques | [ATLAS](https://atlas.mitre.org/) |
| Mar 2026 | Mindgard 2026 red teaming benchmarks | Role-play attacks 89.6% success; multi-turn jailbreaks 97% in 5 turns; prompt injection found in 70% of audits | [Mindgard](https://mindgard.ai/blog/ai-red-teaming-statistics) |
| Jul 2019 | Cylance universal bypass (ATLAS AML.CS0003) | 100% evasion on top 10 malware families by appending benign strings from Rocket League | [Skylight Cyber](https://skylightcyber.com/2019/07/18/cylance-i-kill-you/) |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Adversarial robustness testing:** [IBM ART v1.20.1](https://github.com/Trusted-AI/adversarial-robustness-toolbox) (Linux Foundation — evasion, poisoning, extraction, and inference attacks/defenses; supports PyTorch, TensorFlow, scikit-learn), [NVIDIA Garak](https://github.com/NVIDIA/garak) ("nmap for LLMs" — 120+ vulnerability categories including hallucination, jailbreaks, data leakage, prompt injection), [Cisco AI Defense](https://www.robustintelligence.com/product) (acquired Robust Intelligence Oct 2024 — stress testing + real-time AI Firewall)
- **Red-teaming and alignment:** [HarmBench 1.0](https://github.com/centerforaisafety/HarmBench) (510+ behaviors, 18 attack methods, 33 target LLMs), [Microsoft PyRIT](https://github.com/Azure/PyRIT) (multi-turn adversarial automation), StrongREJECT (jailbreak effectiveness scoring, integrated into Garak), [Mindgard](https://mindgard.ai/) (automated red teaming with CI/CD integration, multimodal support, MITRE ATLAS + OWASP LLM Top 10 aligned reporting; Gartner Emerging Tech 2026, 2025 Cybersecurity Excellence Award)
- **Differential privacy:** [Opacus](https://opacus.ai/) (Meta, PyTorch DP-SGD with LoRA support, Dec 2024), [TensorFlow Privacy 0.12.3](https://www.tensorflow.org/responsible_ai/privacy), [Microsoft dp-transformers](https://github.com/microsoft/dp-transformers) (HuggingFace integration), [PySyft 0.9.5](https://github.com/OpenMined/PySyft) (privacy-preserving ML with OpenDP). As of 2026, Google research demonstrates user-level DP fine-tuning requires significantly less noise than previously thought, and DP-ZeRO enables large-scale DP training via DeepSpeed with reduced memory overhead. Practical note: DP-SGD adds 3-5x training overhead for full training, though parameter-efficient fine-tuning (LoRA, P-tuning) substantially narrows the gap.
- **Model watermarking:** [Google SynthID](https://deepmind.google/technologies/synthid/) (production on Gemini — text/image/audio/video; text component [open-sourced](https://github.com/google-deepmind/synthid-text)), academic approaches (Kirchenbauer green-list, frequency-domain embedding). Newer "holographic" watermarking distributes marks across entire artifacts, making partial removal destructive. [zkDL++](https://openreview.net/forum?id=JyrjeQJ8VK) (ICLR 2025) introduces zero-knowledge proofs for provable watermark extraction — verifying watermark presence without revealing extractor internals, which closes a key privacy gap in deployment. However, research shows any image watermark can be removed >50% of the time without knowledge of the watermark design, including SynthID and Meta's Stable Signature.
- **Model extraction detection:** [Lakera Guard](https://www.lakera.ai/) (acquired by Check Point 2025 — 98%+ detection, sub-50ms, 100+ languages), rate limiting, query-pattern analysis, model fingerprinting techniques
- **Inference-time anomaly detection:** [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/) (NVIDIA — programmable rails with Garak integration), [Rebuff](https://github.com/protectai/rebuff) (multi-layer prompt injection detection), [RAGForensics](https://arxiv.org/abs/2504.21668) (first traceback system for RAG poisoning — iteratively retrieves and probes knowledge base subsets to identify poisoned texts; ACM Web Conference 2025), [SDAG](https://arxiv.org/abs/2602.04711v2) (Sparse Document Attention — block-sparse attention mask that prevents cross-attention between retrieved documents, requiring only inference-time attention mask changes with no fine-tuning), [ReliabilityRAG](https://arxiv.org/pdf/2509.23519) (builds a contradiction graph over retrieved documents using NLI, selects a consistent majority via Maximum Independent Set to filter poisoned entries)
- **Formal robustness verification:** [alpha-beta-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN) (VNN-COMP winner 2021-2025, GPU-accelerated), [auto_LiRPA 0.3](https://github.com/Verified-Intelligence/auto_LiRPA) (provable output bounds), [ERAN](https://github.com/eth-sri/eran) (ETH Zurich — abstract interpretation). *Limitation: scales to small/medium networks; not yet practical for full-scale LLMs.*

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C11.1 Model Alignment & Safety | Maturing | HarmBench, Garak, PyRIT provide standardized red-teaming. Evaluation awareness/sandbagging (C11.1.5) has detection methods (noise injection) but no production tooling. |
| C11.2 Adversarial-Example Hardening | Mature | IBM ART provides comprehensive attack/defense library. Formal verification (C11.2.5) limited to small networks — alpha-beta-CROWN is state of the art but doesn't scale to LLMs. |
| C11.3 Membership-Inference Mitigation | Maturing | Opacus + dp-transformers enable DP fine-tuning. Shadow-model MIA testing is well-documented. 3-5x training overhead remains a practical barrier for full pretraining. |
| C11.4 Model-Inversion Resistance | Maturing | DP training, output calibration, rate limiting are established defenses. The $200 ChatGPT extraction shows alignment doesn't prevent memorization leakage. |
| C11.5 Model-Extraction Defense | Maturing | Lakera Guard, rate limiting, fingerprinting provide detection. SynthID watermarking is production-grade for Google models. Industrial-scale distillation (DeepSeek) shows determined attackers can still succeed. |
| C11.6 Inference-Time Poisoned-Data Detection | Emerging → Early Maturing | PoisonedRAG demonstrates the threat. As of early 2026, three distinct academic defenses have emerged: RAGForensics (traceback to identify poisoned texts), SDAG (sparse attention isolation between documents), and ReliabilityRAG (contradiction-graph filtering). NeMo Guardrails can gate suspicious inputs. No single production-grade solution yet, but the defense surface is expanding. |
| C11.7 Security Policy Adaptation | Mature | Hot-reloadable policy configs are standard practice. Cryptographic signing of policy updates (C11.7.2) uses established tooling. |
| C11.8 Agent Security Self-Assessment | Emerging | NeMo Guardrails and custom policy engines can check planned actions. No dominant open-source tool for agent action review. Morris II worm shows self-assessment can be bypassed. |
| C11.9 Self-Modification & Autonomous Update Security | Emerging | Bounded self-modification (C11.9.4) is largely custom-built. Safety feedback poisoning (C11.9.5) has no standard detection tooling. |
| C11.10 Adversarial Bias Exploitation Defense | Emerging | Subgroup-stratified robustness evaluation (C11.10.2) requires custom benchmarking. No off-the-shelf tool for bias probing detection (C11.10.1). |

---

## Related Standards & Cross-References

- [NIST AI 100-2 E2025](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) (March 2025, supersedes E2023) — Adversarial ML taxonomy: evasion, poisoning, privacy attacks. New GenAI categories: indirect prompt injection, misaligned outputs, energy-latency attacks.
- [MITRE ATLAS](https://atlas.mitre.org/) (October 2025 expansion: 15 tactics, 66 techniques, 46 sub-techniques, 14 new AI agent techniques added in collaboration with Zenity Labs) — AML.T0015 (Evade ML Model), AML.T0018 (Backdoor ML Model — .000 Poison, .001 Inject Payload), AML.T0024 (Exfiltration via Inference API — .000 Membership Inference, .001 Model Inversion, .002 Model Extraction), AML.T0043 (Craft Adversarial Data — .000-.004), AML.T0006 (Active Scanning). Case studies: AML.CS0003 (Cylance bypass), deepfake KYC liveness detection bypass (November 2025).
- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) — PII leakage, prompt leakage, IP exposure via model outputs
- [OWASP LLM04:2025 Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/) — Training, fine-tuning, RAG, and embedding poisoning
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) — Resource exhaustion enabling model extraction
- [EU AI Act Article 15](https://artificialintelligenceact.eu/article/15/) — Accuracy, robustness, and cybersecurity for high-risk AI. Explicitly names 4 attack types: data poisoning, model poisoning, adversarial examples, confidentiality attacks. Enforceable August 2026.
- [ISO/IEC TR 24029-1](https://www.iso.org/standard/42001) — Robustness of Neural Networks: principles for evaluating behavior under perturbation, model stability, and vulnerability to unexpected inputs
- [ISO/IEC 23894](https://www.iso.org/standard/42001) — AI Risk Management: requires robustness considerations, continuous testing including adversarial scenarios and edge cases
- [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) (Jul 2025) — 243 controls including Model Security, Adversarial Defenses, and Model Robustness domains
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — MEASURE function covers adversarial probing and stress testing; MANAGE covers risk treatment

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| [C01 Training Data](C01-Training-Data.md) | Data poisoning | C01 covers training-time data integrity; C11.6 covers inference-time poisoned data detection. ATLAS AML.T0018.000 (Poison ML Model) and LLM04 bridge both. EU AI Act Art 15 names data poisoning explicitly. |
| [C02 User Input Validation](C02-User-Input-Validation.md) | Adversarial inputs, bias probing | C02 handles general input validation; C11.2 addresses inputs crafted to fool models (ATLAS AML.T0043). C11.10 monitors for structured probing patterns indicating bias exploitation reconnaissance. |
| [C06 Supply Chain](C06-Supply-Chain.md) | Backdoored models from supply chain | ATLAS AML.T0018.001 (Inject Payload) enables backdoors via compromised pretrained models. LLM04 fine-tuning poisoning bridges supply chain and adversarial robustness. |
| [C07 Model Behavior](C07-Model-Behavior.md) | Output safety, jailbreaks, alignment | C07 covers behavioral constraints; C11.1 focuses on alignment testing and red-teaming. JBFuzz 99% bypass rates and Skeleton Key demonstrate the overlap. Sandbagging undermines both chapters' verification. |
| [C09 Orchestration & Agents](C09-Orchestration-and-Agents.md) | Agent self-assessment, self-modification | C09 covers orchestration security; C11.8-C11.9 address agent self-assessment and self-modification security. Morris II worm demonstrates adversarial self-replication through agent ecosystems. |
| [C12 Privacy](C12-Privacy.md) | Privacy attacks (MIA, inversion, extraction) | C12 covers privacy holistically; C11.3-C11.4 focus on membership inference and model inversion attacks. ATLAS AML.T0024 (.000/.001/.002) maps the full privacy attack subtree. The $200 ChatGPT extraction bridges both. |
| [C13 Monitoring & Logging](C13-Monitoring-and-Logging.md) | Adversarial detection and alerting | C13 covers monitoring infrastructure; C11.5-C11.7 cover adversarial-specific detection, extraction alerts, and security policy adaptation. |

---

## Open Research Questions

- [ ] **How do you detect evaluation awareness / sandbagging?** — Frontier models can strategically underperform on dangerous capability evaluations while maintaining general performance. Noise injection into model weights reveals sandbagging through anomalous performance *improvements*, but this isn't a production detection method. Claude 3.5 Sonnet spontaneously underperformed without explicit instruction when it discovered an unlearning process would be triggered.
- [ ] **Can formal verification scale to production LLMs?** — alpha-beta-CROWN wins VNN-COMP annually but only scales to small/medium networks. Certified robustness for full-scale transformers remains an open problem. C11.2.5 requires formal verification for safety-critical components — the "where the model architecture supports them" qualifier is doing heavy lifting.
- [ ] **How do you defend against inference-time RAG poisoning?** — PoisonedRAG showed 5 crafted documents manipulate 90% of responses. As of early 2026, three academic defenses have emerged — RAGForensics (traceback), SDAG (sparse attention isolation), and ReliabilityRAG (contradiction-graph filtering) — but none has reached production maturity. The fundamental challenge remains: models can't distinguish instructions from data in retrieved context, and existing defenses have proven insufficient against sophisticated adaptive attacks.
- [ ] **Is DP-SGD practical for LLM pretraining?** — 3-5x overhead makes DP-SGD feasible for fine-tuning (Opacus + LoRA) but prohibitive for full pretraining. Google's 2026 research on user-level DP shows prior approaches added far more noise than necessary, and DP-ZeRO improves scalability via DeepSpeed. Still, membership inference defenses (C11.3) remain practically limited to fine-tuning scenarios for large models.
- [ ] **Can model watermarking survive determined removal?** — SynthID text watermarking is robust to mild paraphrasing but less effective on factual outputs. Research shows any image watermark (including SynthID and Meta's Stable Signature) can be removed >50% of the time without knowledge of the watermark design. zkDL++ (ICLR 2025) introduces zero-knowledge proofs for provable extraction, which helps verification but doesn't solve the removal problem. Weight-based watermarking for IP protection is an active research area but no standard exists.
- [ ] **Can adversarial robustness keep pace with automated attack generation?** — Automated red-teaming tools discover 37% more unique vulnerabilities than manual testing alone (Mindgard 2026), yet only 26% of organizations conduct proactive security testing. The gap between attack automation (FuzzyAI, JBFuzz, Mastermind) and defense deployment suggests most production systems are undertested. Multi-turn attacks that self-improve through interaction (Mastermind framework) represent a qualitative shift from static jailbreak templates.
- [ ] **How do you bound self-modification in agentic systems?** — Morris II demonstrated autonomous propagation via metamorphic prompts. Copilot configuration self-modification showed silent settings changes. C11.9.4 requires bounded self-modification, but defining and enforcing those bounds at runtime remains unsolved.

---

## Industry Adoption & Testing Metrics

As of March 2026, industry benchmarks paint a sobering picture of adversarial robustness in practice:

- **Testing coverage gap:** Only 26% of organizations conduct proactive AI security testing. Automated red teaming identifies 37% more unique vulnerabilities than manual testing alone, and post-implementation testing reveals 75-80% more vulnerabilities than pre-deployment assessments catch.
- **Attack success rates in benchmarked evaluations:** Role-play attacks succeed at 89.6%, multi-turn jailbreaks reach 97% within five turns, and healthcare-domain LLM attacks hit 94.4% adversarial objective completion. Even simple cognitive manipulations ("bad math" misdirection) succeed 76% of the time.
- **Detection capability:** Best-in-class model detection (Claude 3.7 Sonnet) achieves only 46.9% detection rate against adversarial inputs. Known jailbreak exploits succeed at a 17% average rate even against models with active defenses, and documented attack techniques show 28% overall success.
- **Economic impact:** Organizations with mature AI security practices experience 60% fewer incidents. Proactive testing yields an estimated $2.4 million in prevented breach costs, with roughly $1.9 million saved per breach avoided.
- **Framework expansion:** MITRE ATLAS grew from its initial scope to 15 tactics and 66 techniques by October 2025, adding 14 AI agent-specific techniques. AI-assisted cyber attacks surged 72% in 2025, driving the need for more comprehensive adversarial robustness frameworks.

These numbers reinforce that adversarial robustness is not a theoretical concern — it's a measurable operational risk with quantifiable return on investment for organizations that test proactively.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
