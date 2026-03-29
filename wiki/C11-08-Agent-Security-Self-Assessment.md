# C11.8: Agent Security Self-Assessment

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 3 | **IDs:** 11.8.1--11.8.3

## Purpose

For agentic AI systems, validate that the agent's reasoning and actions are subject to security-focused review mechanisms. Agentic systems -- AI that can plan, use tools, and take actions autonomously -- present unique adversarial robustness challenges because harmful behavior can emerge from sequences of individually benign actions. This section requires that agents have pre-execution security review mechanisms, that these mechanisms are hardened against adversarial bypass, and that security warnings trigger appropriate escalation.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **11.8.1** | **Verify that** agentic systems include a mechanism to review planned high-risk actions against security policy before execution (e.g., a secondary model, rule-based checker, or structured self-review step). | 2 | Agents executing harmful actions due to adversarial manipulation, hallucinated plans, or goal misalignment. Without pre-execution review, a compromised or confused agent can take irreversible actions (deleting data, sending unauthorized communications, modifying configurations) before anyone notices. | Review agent architecture for pre-execution review mechanisms. Identify which actions are classified as "high-risk" and verify the classification is comprehensive. Test the review mechanism with planned actions that violate security policy and confirm they are caught. Verify that the review mechanism cannot be skipped or bypassed by the agent itself. Test with edge cases: actions that are individually benign but collectively harmful. | Defining "high-risk actions" is context-dependent and requires careful analysis of the agent's capabilities. Self-review (asking the same model to evaluate its own plan) is the weakest form of review due to sycophancy and shared failure modes. Secondary models provide better independence but add latency and cost. Rule-based checkers are reliable but brittle and can miss novel attack patterns. A layered approach (rules + model review) is recommended. |
| **11.8.2** | **Verify that** security review mechanisms are protected against manipulation by adversarial inputs (e.g., the review step cannot be overridden or bypassed through prompt injection). | 2 | Adversarial bypass of the security review layer itself. If an attacker can inject instructions that cause the reviewer to approve harmful actions, the review mechanism provides no protection. This is a meta-attack: attacking the defense rather than the primary model. Related to OWASP LLM01 (Prompt Injection). | Attempt to bypass the review mechanism through: injected instructions in tool outputs, manipulated context that redefines security policy, prompt injection targeting the reviewer specifically, social engineering of the review step (e.g., "this action has already been approved"). Verify architectural separation between the review mechanism and untrusted inputs. Check that the reviewer's security policy is not modifiable by the agent or its inputs. | This is one of the hardest requirements to verify because the attack surface is the same as prompt injection generally. Architectural separation (running the reviewer with a separate, hardened system prompt that cannot see untrusted content directly) is the strongest approach. The reviewer should evaluate a structured action description, not raw user/tool input. No current approach provides guaranteed protection against all prompt injection variants. |
| **11.8.3** | **Verify that** security review warnings trigger enhanced monitoring or human intervention workflows for the affected session or task. | 3 | Security warnings that are generated but not acted upon, or that result in a simple block without investigation. A security review warning may indicate an active attack, a system misconfiguration, or a novel failure mode -- all of which require follow-up beyond just blocking the immediate action. | Review escalation workflows triggered by security review warnings. Verify that warnings result in: enhanced logging for the session, notification to security operations, human review queue entry for the task, and session-level risk elevation (tighter controls for subsequent actions in the same session). Test end-to-end: trigger a security warning and verify escalation workflow execution. | Human intervention workflows must be designed for the expected volume of warnings -- too many warnings cause alert fatigue. Session-level risk elevation (treating the entire session as potentially adversarial after one warning) is a useful pattern but may impact legitimate users who trigger false positives. Consider tiered escalation based on warning severity. |

---

## Implementation Guidance (2024--2026 Research)

### OWASP Top 10 for Agentic Applications (2026)

The OWASP Top 10 for Agentic Applications, released in early 2026 through collaboration with over 100 industry experts, provides the first peer-reviewed taxonomy of agentic AI security risks. Several entries map directly to the requirements in this section:

- **ASI01 -- Agent Goal Hijacking**: Attackers redirect agent objectives by manipulating instructions, tool outputs, or external content. This is the primary threat that 11.8.1 pre-execution review must detect.
- **ASI02 -- Tool Misuse & Exploitation**: Agents misuse legitimate tools due to prompt injection, misalignment, or unsafe delegation. Pre-execution review of tool invocations is the first line of defense.
- **ASI10 -- Rogue Agents**: Compromised or misaligned agents diverge from intended behavior. Security self-assessment (the focus of this entire section) is the detection mechanism for rogue agent behavior.

The framework codifies two design principles relevant to self-assessment: **Least Agency** (autonomy should be earned, not default) and **Strong Observability** (seeing what agents are doing, why, and which tools and identities they use).

### Metacognitive Security and Self-Monitoring

The concept of "metacognitive security" -- agents that monitor and evaluate their own security posture -- has advanced significantly in 2024--2026 research:

- **Agentic metacognition for failure prediction**: Research from Arxiv (2025, paper 2509.19783) introduces metacognitive agent architectures where continuous self-evaluation of the agent's state against predefined triggers enables proactive handoff protocols. When an agent detects impending failures or policy violations, structured human-guided recovery is initiated rather than allowing uncontrolled operation. This generates traceable, auditable logs of agent decisions and reasons for escalation, directly supporting requirement 11.8.3.
- **Self-evaluation through chain-of-thought**: Galileo's research on self-evaluation in AI agents demonstrates that chain-of-thought reasoning enables agents to evaluate answer quality, recognize limitations, and identify potential errors through metacognitive processes. When applied to security, this pattern allows agents to reason explicitly about whether a planned action might violate security policy before execution.
- **Declared vs. observed behavior comparison**: The CSA MAESTRO framework (2025) introduces a pattern where an agent's declared skill behavior is compared against its observed behavior to identify deceptive, unsafe, or non-compliant functionality -- such as agents attempting to invoke unapproved services or access tools outside their declared scope. This comparison mechanism is a concrete implementation approach for requirement 11.8.1.

### Agentic AI Security Scoping

AWS published the Agentic AI Security Scoping Matrix (2025--2026), establishing a framework for classifying agent security requirements based on autonomy level and capability scope. Key findings relevant to self-assessment include:

- Organizations report a significant readiness gap: only 18% of respondents are "highly confident" their current identity and access management systems can manage agent identities effectively, despite 40% already having agents in production.
- Agent security self-assessment is most effective when combined with external monitoring -- self-review alone is insufficient because the agent shares failure modes with its own reviewer.

### Architecture Patterns for Security Review

Emerging best practices for implementing requirement 11.8.1 include a layered approach:

1. **Rule-based pre-filters**: Fast, deterministic checks against known-bad action patterns (e.g., data deletion, privilege escalation, external communication). Reliable but brittle against novel attacks.
2. **Secondary model review**: A separate, hardened model evaluates structured action descriptions (not raw user input) against security policy. Provides independence from the primary model's failure modes but adds latency.
3. **Architectural isolation**: The review mechanism receives a sanitized, structured representation of the proposed action rather than the full conversation context, reducing the attack surface for prompt injection targeting the reviewer (11.8.2).

### Formal Runtime Enforcement Frameworks

Two academic frameworks published in 2025--2026 formalize the pre-execution review pattern required by 11.8.1, moving beyond ad-hoc guardrails toward provable safety guarantees:

- **AgentSpec** (ICSE 2026, arXiv:2503.18666): A lightweight domain-specific language for specifying and enforcing runtime constraints on LLM agents. Rules are expressed as three-tuples of triggering events, predicate functions, and enforcement actions. Evaluation across code execution, embodied agents, and autonomous driving showed >90% unsafe execution prevention for code agents, 100% hazardous action elimination for embodied agents, and 100% compliance for autonomous vehicles -- all with millisecond-level overhead. LLM-generated rules (via OpenAI o1) achieved 95.6% precision and identified 87.3% of risky code, suggesting that rule authoring itself can be partially automated.
- **Agent Behavioral Contracts (ABC)** (arXiv:2602.22302, February 2026): Applies Design-by-Contract principles to AI agents, defining preconditions, invariants, governance policies, and recovery mechanisms. ABC distinguishes "hard" constraints (never violated) from "soft" constraints (transient violations acceptable if recovered within k steps), accounting for LLM non-determinism. Testing across 1,980 sessions on seven models detected 5.2--6.8 soft violations per session that were invisible to uncontracted baselines, achieved 88--100% hard constraint compliance, and bounded behavioral drift below 0.27. ABC provides formal guarantees (Drift Bounds Theorem) and safe multi-agent composition proofs that AgentSpec lacks.

Both frameworks represent a significant maturation of the field -- organizations implementing 11.8.1 now have peer-reviewed, quantitatively validated approaches rather than relying solely on heuristic guardrails.

### Hardening Review Mechanisms Against Bypass

The hardening of security review mechanisms (11.8.2) remains one of the most challenging problems in agentic AI security. 2025--2026 research confirms that:

- No current approach provides guaranteed protection against all prompt injection variants targeting the reviewer.
- The strongest mitigation is architectural: the reviewer should never directly process untrusted inputs. Instead, the primary agent produces a structured action proposal (tool name, parameters, justification), and only this structured representation is evaluated.
- Multi-agent review architectures (dedicated security agent reviewing all actions) show promise but introduce coordination complexity and latency.
- **Zero-click indirect injection is now a demonstrated real-world threat**: In March 2026, Zenity Labs disclosed the PleaseFix vulnerability family affecting Perplexity's Comet AI browser and other agentic browsers. Attacker-controlled content (such as a calendar invite) triggered autonomous execution without any user interaction -- the agent accessed the local file system, exfiltrated contents to an attacker-controlled endpoint, and in a second exploit path, abused agent-authorized workflows to steal 1Password credentials. This incident demonstrates that 11.8.2 hardening must account for triggers embedded in routine data sources (calendar, email, documents) that the agent processes as part of normal operation.

### Instruction Hierarchy as a Security Primitive

As of 2025--2026, instruction hierarchy -- the principle that models should follow developer/system instructions over user instructions, and user instructions over content from untrusted sources -- has emerged as a foundational defense for agentic security review:

- **OpenAI's instruction hierarchy training** classifies messages into system, developer, and user tiers, training models to prioritize trusted instructions. Their IH-trained models show substantially improved robustness on internal prompt injection evaluations, and OpenAI considers instruction hierarchy a "core safety property" for agentic tool use.
- **Structured untrusted content isolation**: Placing untrusted data in explicit `untrusted_text` blocks or structured formats (YAML, JSON, XML) helps the model distinguish legitimate instructions from injected ones. This directly supports 11.8.2 by reducing the surface area for review-mechanism bypass.
- **Cross-modal prompt injection**: NVIDIA AI Red Team research (2025--2026) demonstrated that semantic prompt injections using visual sequences (rebus puzzles, emoji compositions) can bypass traditional text-based guardrails in multimodal agents. Models trained to excel at puzzle-solving interpret visual semantics as functional commands. Input filtering alone is insufficient -- output-level controls that evaluate responses for safety and intent before tool execution are essential.

### Multi-Layered Defense Benchmarks

Recent research (arXiv:2511.15759, 2025) provides the first rigorous benchmarks for multi-layered prompt injection defense in agent systems. Using 847 adversarial test cases across five attack categories (direct injection, context manipulation, instruction override, data exfiltration, cross-context contamination):

- **Baseline vulnerability**: Without defenses, 73.2% of adversarial inputs succeeded across tested models.
- **Content filtering only** (embedding-based anomaly detection): Reduced attack success to 41.0%.
- **Content filtering + hierarchical guardrails**: Reduced to 23.4%.
- **Full three-layer defense** (filtering + guardrails + multi-stage response verification): Reduced to 8.7%, while retaining 94.3% of baseline task performance.
- **Computational overhead**: ~68ms total (23ms filtering + 45ms verification), representing ~2.1% of end-to-end latency for typical GPT-4 workflows.

These benchmarks provide a concrete baseline for organizations implementing 11.8.1 and 11.8.2 -- a three-layer defense architecture is demonstrably achievable without crippling agent performance.

### MITRE ATLAS Agent-Specific Techniques (2025--2026)

The October 2025 and early 2026 MITRE ATLAS updates introduced 14 new techniques focused specifically on AI agents, reflecting the shift from model-centric to execution-layer threats:

- **AML.T0096 -- AI Service API**: Adversaries exploit agent orchestration APIs for "live off the land" operations. The SesameOp case study (AML.CS0042) documented attackers using the OpenAI Assistants API as a covert command-and-control channel.
- **AML.T0098 -- AI Agent Tool Credential Harvesting**: Attackers access agent-connected tools to retrieve stored secrets, API keys, and credentials to platforms like SharePoint and OneDrive.
- **AML.T0099 -- AI Agent Tool Data Poisoning**: Adversaries place malicious content (including prompt injections) on systems the agent will process, hijacking agent behavior across sessions.
- **AML.T0100 -- AI Agent Clickbait**: A novel attack class targeting web-enabled agent browsers -- hidden instructions in HTML metadata, malicious links framed as task requirements, and UI elements that trigger unauthorized tool invocation. Agents lack human intuition and may comply with logically consistent but malicious instructions.
- **AML.T0101 -- Data Destruction via AI Agent Tool Invocation**: Exploitation of tool capabilities to destroy data and files, disrupting infrastructure and services.

These techniques directly inform the threat model for 11.8.1 (what the review mechanism must catch) and 11.8.2 (indirect attack vectors targeting the reviewer itself).

### Real-World Agent Security Incidents

Several incidents in 2025--2026 underscore the practical urgency of agent security self-assessment:

- **Anthropic Claude espionage incident (November 2025)**: Chinese state-sponsored attackers used Claude Code to orchestrate a large-scale cyberattack where the model performed 80--90% of attack operations autonomously -- mapping networks, writing exploits, harvesting credentials, and exfiltrating data from approximately 30 targets. The bypass was straightforward: attackers framed the agent as "an employee of a legitimate cybersecurity firm conducting defensive testing" and decomposed malicious tasks into innocent-seeming subtasks. This incident demonstrates that 11.8.1 review mechanisms must evaluate the aggregate intent of action sequences, not just individual operations.
- **Perplexity Comet PleaseFix vulnerability (March 2026)**: Zenity Labs disclosed a zero-click prompt injection vulnerability family in Perplexity's Comet AI browser. Malicious calendar invites hijacked the browser agent without user interaction, enabling local file exfiltration and 1Password credential theft. The attack required no exploit, no user clicks, and no explicit request for sensitive actions -- the agent autonomously executed embedded malicious instructions while still returning expected responses to the user. This is the first publicly documented zero-click credential theft via an agentic browser.
- **McKinsey Lilli red-team compromise (2026)**: During a red-team exercise, McKinsey's autonomous agent "Lilli" was compromised in under two hours, gaining broad system access rapidly. This demonstrates that even well-resourced enterprise deployments with dedicated security teams remain vulnerable when pre-execution review mechanisms are insufficient.
- **Q4 2025 attack pattern analysis (Lakera AI)**: Across 30 days of monitored agent deployments, system prompt extraction was the most common attacker objective, using hypothetical scenarios and role framing to elicit role definitions and tool descriptions. Indirect prompt injection -- malicious instructions arriving through untrusted external content rather than direct user input -- required fewer attempts to succeed than direct attacks, reinforcing the priority of 11.8.2 controls.
- **Tool misuse at scale**: MITRE ATLAS data shows tool misuse and privilege escalation as the most common agent attack category (520 documented incidents in 2026), with memory poisoning attacks carrying disproportionate severity due to persistence across sessions. A supply chain attack on the OpenAI plugin ecosystem compromised agent credentials across 47 enterprise deployments, with attackers accessing customer data, financial records, and proprietary code for six months before discovery.

### Guardrails Tooling Landscape

As of March 2026, the guardrails ecosystem has expanded significantly. A Galileo survey identifies eight major solutions, and several new entrants strengthen runtime enforcement capabilities:

- **NVIDIA NeMo Guardrails** (Apache 2.0): Programmable framework with six distinct guardrail types configured via Colang (a domain-specific language). Operates as a proxy microservice with multi-LLM provider support. CrowdStrike's Falcon AIDR integration (announced early 2026) adds 75+ built-in rules for prompt injection blocking, input/output sanitization, and sensitive data redaction.
- **Cisco AI Defense & Agent Runtime SDK** (March 2026): Cisco's AI Defense Explorer Edition provides self-serve tools to test model and application resilience against attacks and embed guardrails before deployment. The Agent Runtime SDK embeds policy enforcement directly into agent workflows at build time, supporting AWS Bedrock AgentCore, Google Vertex Agent Builder, Azure AI Foundry, and LangChain. Cisco also released DefenseClaw, an open-source secure agent framework.
- **AWS Bedrock Guardrails**: Policy-based runtime enforcement with centralized governance controls at the model inference layer. Features pre-trained classifiers and contextual grounding checks for RAG validation.
- **Guardrails AI** (Apache 2.0): Validation framework with pre-built validators for output quality and safety checks, usable as a post-generation review layer.
- **Lakera Guard**: Sub-200ms latency runtime firewall specializing in prompt injection and data leakage prevention. Supports self-hosted or cloud deployment.
- **OpenAI Guardrails Python** (`openai-guardrails-python`): Includes prompt injection detection checks and PII redaction, designed for integration into agentic workflows.
- **Anthropic Constitutional Classifiers**: Input and output classifiers trained on synthetically generated data that filter jailbreaks with minimal over-refusals. These can serve as the secondary review layer in a multi-model architecture.

None of these tools alone satisfies the full requirements of 11.8.1 through 11.8.3 -- they are building blocks for a layered architecture that must also include escalation workflows (11.8.3) and hardening against reviewer bypass (11.8.2).

### Escalation and SOC Integration (11.8.3)

The integration of agent security warnings with security operations workflows has matured considerably in 2025--2026:

- **Agentic SOC platforms** (Fortinet FortiSOC, Stellar Cyber, Swimlane): These platforms now support ingesting agent behavioral anomaly alerts alongside traditional security events, enabling unified case management and correlation of agent-origin threats with broader attack patterns.
- **Tiered escalation design**: Industry consensus recommends tiered escalation -- low-severity warnings increase logging verbosity and session monitoring, medium-severity warnings trigger human review queue entries, and high-severity warnings (e.g., attempted data exfiltration, credential access) immediately pause the agent and notify SOC. Analysts are increasingly spending time "supervising agents" -- tuning rules of engagement and reviewing automated response performance.
- **Session-level risk elevation**: When a security warning fires, all subsequent actions in the same session should face tighter review thresholds. This "ratchet" pattern limits the blast radius of ongoing attacks without requiring immediate session termination.
- **CSA Agentic Control Plane (March 2026)**: The Cloud Security Alliance defines the Agentic Control Plane as the governance layer encompassing identity, authorization, orchestration, runtime behavior monitoring, and trust verification for autonomous agents. Their STAR for AI program extends assessment into continuous assurance -- moving beyond point-in-time security reviews to ongoing agent behavioral validation.

### Regulatory Drivers: EU AI Act High-Risk Deadline (August 2026)

As of March 2026, the EU AI Act's high-risk AI system requirements become fully enforceable on August 2, 2026. For agentic systems that qualify as high-risk (e.g., agents operating in healthcare, finance, critical infrastructure, or employment), this creates a hard compliance deadline for the security review mechanisms described in 11.8.1--11.8.3:

- **Risk management systems** (Article 9): Pre-execution security review satisfies the requirement for continuous risk identification and mitigation throughout the AI system lifecycle.
- **Human oversight** (Article 14): Escalation workflows (11.8.3) that route security warnings to human operators map directly to the EU AI Act's human oversight provisions.
- **Robustness** (Article 15): Hardening review mechanisms against adversarial bypass (11.8.2) supports the requirement that high-risk AI systems be resilient to errors and manipulation.

ISO/IEC 42001 (AI Management Systems) provides the auditable management framework for implementing these controls. The CSA's AIUC-1 framework (2026) bridges ISO 42001, EU AI Act, and NIST AI RMF into a single auditable framework specifically designed for agent adoption and usage.

---

## Related Standards & References

- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm012025-prompt-injection/) -- Prompt injection is the primary attack vector against agent review mechanisms
- [OWASP LLM09:2025 Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/) -- Agent hallucination leading to harmful planned actions
- [MITRE ATLAS AML.T0054 -- LLM Prompt Injection](https://atlas.mitre.org/techniques/AML.T0054) -- Prompt injection techniques applicable to agent review bypass
- [NIST AI 100-1 -- Artificial Intelligence Risk Management Framework](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence) -- Risk management for autonomous AI systems
- [CSA MAESTRO -- Agentic AI Threat Modeling Framework](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro) -- Layer-by-layer threat modeling for agentic AI
- [AWS Agentic AI Security Scoping Matrix](https://aws.amazon.com/blogs/security/the-agentic-ai-security-scoping-matrix-a-framework-for-securing-autonomous-ai-systems/) -- Framework for scoping agent security controls by autonomy level
- [Agentic Metacognition -- Arxiv 2509.19783 (2025)](https://arxiv.org/abs/2509.19783) -- Self-aware agent architectures for failure prediction and human handoff
- [Self-Evaluation in AI Agents -- Galileo](https://galileo.ai/blog/self-evaluation-ai-agents-performance-reasoning-reflection) -- Chain-of-thought self-evaluation for agent security reasoning
- [Obsidian Security -- From Agentic AI to Autonomous Risk](https://www.obsidiansecurity.com/blog/agentic-ai-security) -- Enterprise agentic AI security challenges
- [MITRE ATLAS AML.T0098 -- AI Agent Tool Credential Harvesting](https://atlas.mitre.org/techniques/AML.T0098) -- Agent-specific credential harvesting techniques
- [MITRE ATLAS AML.T0099 -- AI Agent Tool Data Poisoning](https://atlas.mitre.org/techniques/AML.T0099) -- Data poisoning targeting agent tool inputs
- [MITRE ATLAS AML.T0100 -- AI Agent Clickbait](https://atlas.mitre.org/techniques/AML.T0100) -- Novel attack class targeting web-enabled agent browsers
- [Zenity & MITRE ATLAS -- Agentic AI Threat Coverage (2026)](https://zenity.io/blog/current-events/zenitys-contributions-to-mitre-atlas-first-2026-update) -- First 2026 ATLAS update expanding agent attack coverage
- [Multi-Layered Prompt Injection Defense -- arXiv:2511.15759 (2025)](https://arxiv.org/abs/2511.15759) -- Benchmark of 847 adversarial test cases with three-layer defense reducing attacks to 8.7%
- [NVIDIA AI Red Team -- Semantic Prompt Injections in Agentic AI](https://developer.nvidia.com/blog/securing-agentic-ai-how-semantic-prompt-injections-bypass-ai-guardrails/) -- Cross-modal prompt injection bypassing traditional guardrails
- [OpenAI -- Improving Instruction Hierarchy in Frontier LLMs](https://openai.com/index/instruction-hierarchy-challenge/) -- Instruction hierarchy as a core safety property for agentic systems
- [OpenAI Guardrails Python](https://openai.github.io/openai-guardrails-python/ref/checks/prompt_injection_detection/) -- Prompt injection detection checks for agentic workflows
- [Anthropic -- Constitutional Classifiers](https://www.anthropic.com/research/constitutional-classifiers) -- Input/output classifiers for filtering jailbreaks with minimal over-refusals
- [CSA -- Securing the Agentic Control Plane (March 2026)](https://cloudsecurityalliance.org/blog/2026/03/20/2026-securing-the-agentic-control-plane) -- Identity, authorization, and runtime monitoring for autonomous agents
- [Pillar Security -- Anthropic AI Espionage Disclosure Analysis](https://www.pillar.security/blog/what-the-anthropic-ai-espionage-disclosure-tells-us-about-ai-attack-surface-management) -- Analysis of the Claude espionage incident and agent attack surface management
- [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) -- Peer-reviewed taxonomy of agentic AI security risks including agent goal hijacking, tool misuse, and rogue agents
- [AgentSpec -- Customizable Runtime Enforcement (ICSE 2026)](https://arxiv.org/abs/2503.18666) -- DSL-based runtime constraint enforcement for LLM agents with >90% unsafe execution prevention
- [Agent Behavioral Contracts -- arXiv:2602.22302 (February 2026)](https://arxiv.org/abs/2602.22302) -- Design-by-Contract for AI agents with formal drift bounds and multi-agent composition guarantees
- [Zenity Labs -- PleaseFix Vulnerability in Perplexity Comet (March 2026)](https://zenity.io/company-overview/newsroom/company-news/zenity-labs-discloses-pleasefix-perplexedagent-vulnerability) -- Zero-click prompt injection enabling credential theft via agentic browsers
- [Cisco AI Defense -- Secure Agentic AI (March 2026)](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m03/cisco-reimagines-security-for-the-agentic-workforce.html) -- Agent Runtime SDK embedding policy enforcement into agent workflows
- [Microsoft -- Secure Agentic AI End-to-End (March 2026)](https://www.microsoft.com/en-us/security/blog/2026/03/20/secure-agentic-ai-end-to-end/) -- Identity-based security, behavioral analytics, and policy-driven access for agents
- [Bessemer -- Securing AI Agents: The Defining Cybersecurity Challenge of 2026](https://www.bvp.com/atlas/securing-ai-agents-the-defining-cybersecurity-challenge-of-2026) -- Agent security threat landscape and defense framework
- [Galileo -- Best AI Agent Guardrails Solutions (2026)](https://galileo.ai/blog/best-ai-agent-guardrails-solutions) -- Comparative analysis of eight major guardrails platforms
- [CrowdStrike Falcon AIDR + NeMo Guardrails Integration](https://www.crowdstrike.com/en-us/blog/secure-homegrown-ai-agents-with-crowdstrike-falcon-aidr-and-nvidia-nemo-guardrails/) -- Runtime prompt injection blocking with 75+ built-in rules
- [CSA -- AI Governance and ISO 42001 FAQs (February 2026)](https://cloudsecurityalliance.org/blog/2026/02/17/ai-governance-and-iso-42001-faqs-what-organizations-need-to-know-in-2026) -- ISO 42001 management system guidance for agent governance
- AISVS C9 (Orchestration and Agents) -- Complementary agent security controls

---

## Open Research Questions

- What is the optimal architecture for agent security review -- same model, different model, rule-based system, or hybrid?
- Can security review mechanisms be made robust against prompt injection without architectural isolation from untrusted inputs?
- How should "high-risk actions" be classified in a general-purpose agent that can use arbitrary tools -- is a capability-based approach (classifying tool permissions) more practical than action-based classification?
- What is the right balance between security review thoroughness and agent response latency -- can review be done asynchronously for some action types?
- How do multi-agent systems change the security review model -- should agents review each other, or should a dedicated security agent review all actions?
- Can metacognitive self-monitoring reliably detect adversarial manipulation of the agent's own reasoning, or does this fundamentally require external observation?
- How should the fidelity of "declared vs. observed behavior" comparison be measured, and what deviation thresholds should trigger security escalation?
- How should security review mechanisms handle cross-modal prompt injection (e.g., visual rebus attacks in multimodal agents) where traditional text-based filtering is ineffective?
- What is the minimum viable defense architecture for resource-constrained deployments -- can the three-layer defense (filtering + guardrails + response verification) be simplified without unacceptable attack surface increase?
- How should session-level risk elevation be calibrated to minimize false positive impact on legitimate users while maintaining protection against sustained multi-step attacks?
- As MITRE ATLAS expands agent-specific techniques (AML.T0096--T0101), how should organizations map their agent security review mechanisms to coverage of these specific attack vectors?
- Can formal runtime enforcement frameworks like AgentSpec and ABC scale to production workloads with thousands of concurrent agent sessions, and what is the operational cost of rule maintenance as agent capabilities evolve?
- How should zero-click indirect injection vectors (calendar invites, email attachments, document embeds) be systematically enumerated and defended against in agentic browser and productivity tool integrations?
- What governance structures are needed to bridge the gap between EU AI Act high-risk compliance requirements (enforceable August 2026) and the current maturity of agent security review tooling?

---
