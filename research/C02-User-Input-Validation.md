# C02: User Input Validation

> **Source:** [`1.0/en/0x10-C02-User-Input-Validation.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C02-User-Input-Validation.md)
> **Requirements:** 18 | **Sections:** 4

## Control Objective

Robust validation of user input is a first-line defense against some of the most damaging attacks on AI systems. Prompt injection attacks can override system instructions, leak sensitive data, or steer the model toward behavior that is not allowed. Unless dedicated filters and other validation is in place, research shows that jailbreaks that exploit context windows will continue to be effective.

> **2025-2026 Highlights:** Major restructuring from 8 sections to 4, consolidating related controls. Requirements expanded to cover agentic input surfaces (MCP tool arguments, agent-to-agent messages, memory reads/writes) alongside traditional user prompts. Multi-modal injection and cross-modal coordinated attacks are now explicitly addressed across C2.1 and C2.4. A recent source refinement (C02 Reduction Pass, March 2026) strengthened two L1 controls: **2.1.2** now explicitly extends instruction hierarchy enforcement across multi-step interactions and tool-augmented workflows (closing the gap where intermediate outputs could launder user content into system context), and **2.1.3** now mandates rejection of over-length inputs rather than silent truncation. As of April 2026, AI framework zero-days (Langflow CVE-2026-33017, Semantic Kernel CVE-2026-26030) are being exploited within hours of disclosure, ShadowPrompt demonstrated that even provider-controlled browser extensions are zero-click injection vectors, and SecureIQLab's independent AI firewall validation testing is actively running (April 1 – June 22, 2026) with results due at Black Hat USA 2026.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C2.1 | Prompt Injection Defense | 9 | [C02-01-Prompt-Injection-Defense](C02-01-Prompt-Injection-Defense) |
| C2.2 | Pre-Tokenization Input Normalization | 3 | [C02-02-Pre-Tokenization-Input-Normalization](C02-02-Pre-Tokenization-Input-Normalization) |
| C2.3 | Content & Policy Screening | 3 | [C02-03-Content-Policy-Screening](C02-03-Content-Policy-Screening) |
| C2.4 | Multi-Modal Input Validation | 3 | [C02-04-Multi-Modal-Input-Validation](C02-04-Multi-Modal-Input-Validation) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- **Direct prompt injection** — overriding system instructions via user input. Remains the #1 vulnerability in production LLM deployments, appearing in over 73% of assessed systems (OWASP LLM01:2025). Multi-turn jailbreak techniques now achieve 90%+ success rates against frontier models in under 60 seconds.
- **Indirect prompt injection** — injected instructions in retrieved content (RAG results, web pages, emails, tool outputs). Research demonstrates that just five carefully crafted documents can manipulate RAG-augmented AI responses 90% of the time.
- **Second-order prompt injection** — exploiting privilege hierarchies in multi-agent systems, where a low-privilege agent is tricked into escalating requests to a higher-privilege agent (demonstrated against ServiceNow Now Assist in 2025).
- **Unicode and encoding smuggling** — invisible characters (zero-width joiners, Unicode tags), homoglyphs, mixed-script payloads, Base64 encoding, mathematical symbol substitution, and "glitch tokens" that bypass production guardrails from major vendors while remaining interpretable by LLMs. ASCII smuggling attacks tested across multiple LLMs in September 2025 showed broad susceptibility.
- **Multi-modal injection** — instructions hidden in images (adversarial perturbations invisible to humans), audio (AudioJailbreak achieving 87-88% success even over speakers with room reverb, ACM CCS 2025), and documents. Cross-modal chaining (steganographic embedding + semantic manipulation) compounds attack effectiveness (Chain of Attack, CVPR 2025).
- **Cross-modal prompt injection** — CrossInject (ACM MM 2025) demonstrated that embedding aligned adversarial signals across both vision and text modalities boosts attack success by at least 30.1% over single-modality attacks. Embedding-space attacks that target only the vision encoder (e.g., CLIP) reduce attacker requirements — no direct LLM access needed.
- **Physical-environment injection** — CHAI (Command Hijacking against embodied AI) demonstrated physical-world prompt injection against embodied AI agents (January 2026, UC Santa Cruz). Related work showed typographic adversarial instructions on physical objects can hijack camera-equipped autonomous agents.
- **Crescendo and multi-turn attacks** — gradually escalating benign prompts toward harmful outputs, exploiting context window accumulation to shift model behavior over multiple turns.
- **Token smuggling** — bypassing input filters through non-standard encodings, emoji-based code payloads, and character obfuscation techniques that evade tokenizer-level safety checks.
- **Zero-click indirect injection** — a particularly dangerous variant where the victim never interacts with the malicious payload directly. EchoLeak (CVE-2025-32711, CVSS 9.3) demonstrated this against Microsoft 365 Copilot: a single poisoned email triggers data exfiltration when the user queries Copilot about unrelated topics. The payload executes in natural language space, rendering traditional defenses (antivirus, firewalls, static scanning) ineffective.
- **AI framework code injection** — vulnerabilities in AI development frameworks (Langflow, Semantic Kernel, LangChain) are increasingly exploited as entry points. CVE-2026-33017 (Langflow, CVSS 9.8) was exploited within 20 hours of disclosure in March 2026 — attackers built working exploits from the advisory alone, with no PoC required.
- **Browser-extension injection (ShadowPrompt pattern)** — attackers chain an overly permissive origin allow-list in a vendor's own browser extension with a DOM-based XSS in a third-party subdomain (e.g., a CAPTCHA widget) to deliver prompts that the LLM interprets as user-authored. The Claude Chrome extension flaw (disclosed Dec 26, 2025; patched v1.0.41 on Jan 15, 2026; Arkose CAPTCHA XSS fully patched Feb 19, 2026) showed that simply visiting a malicious page was enough to steal access tokens, read conversation history, and act on the victim's behalf. Critically, the attack subverts instruction hierarchy — the injected content appears indistinguishable from a legitimate user turn — which is exactly the threat model C2.1.2's updated multi-step enforcement language targets.
- **The "Lethal Trifecta"** — systems that combine (1) access to private data, (2) exposure to untrusted tokens from external sources, and (3) an exfiltration vector (ability to make external requests) are inherently vulnerable to indirect injection chains. As of early 2026, most enterprise AI copilot deployments exhibit all three characteristics.
- **Scale of the problem** — a meta-analysis of 78 recent studies (2021–2026) found that attack success rates against state-of-the-art defenses exceed 85% when adaptive strategies are employed, and 73% of tested platforms fail to adequately enforce boundaries between agents, tools, and sessions. Wiz Research tracked a 340% YoY increase in documented prompt injection attempts in Q4 2025 and a 190% rise in successful attacks causing measurable data exfiltration. VentureBeat's April 2026 survey of 100 technical decision-makers found only **34.7%** of organizations have deployed dedicated prompt injection defenses — the remaining 65.3% either haven't purchased the tooling or cannot confirm they have.

---

## Notable Incidents

| Date | Incident | Relevance |
|------|----------|-----------|
| 2025 | GitHub Copilot RCE (CVE-2025-53773, CVSS 9.6) | Prompt injection leading to remote code execution in a widely deployed AI coding assistant |
| 2025 | ServiceNow Now Assist second-order injection | Attackers exploited agent privilege hierarchy to exfiltrate case files via a low-privilege agent tricking a high-privilege agent |
| 2025 | ChatGPT Windows license key exposure | Prompt injection used to extract sensitive data from model context |
| Dec 2025 | Palo Alto Unit 42: indirect injection in ad review system | Real-world malicious indirect prompt injection designed to bypass an AI-based product advertisement review pipeline |
| Sep 2025 | ASCII smuggling across multiple LLMs | Researchers demonstrated Unicode tag-based data exfiltration across multiple commercial LLMs; findings reported to Google |
| Jun 2025 | EchoLeak — Microsoft 365 Copilot zero-click exfiltration (CVE-2025-32711, CVSS 9.3) | A single poisoned email triggered data exfiltration from Copilot without any user interaction; payload operated in natural language space, bypassing traditional defenses entirely |
| 2025 | GeminiJack — Google Gemini Enterprise indirect injection | Malicious instructions hidden in shared docs, calendar invites, and emails triggered on routine employee queries; data exfiltrated via image URL requests |
| 2025 | LangChain serialization injection (CVE-2025-68664, "LangGrinch") | Vulnerability in LangChain's `dumps()` and `dumpd()` serialization functions enabling code injection via crafted model artifacts |
| 2025 | Cursor IDE agent RCE (CVE-2025-59944) | Case-sensitivity bug in protected file path allowed attacker to influence agentic behavior; hidden instructions escalated to remote code execution |
| Feb 2026 | CrowdStrike 2026 Global Threat Report: prompt injection at scale | Adversaries exploited GenAI tools at 90+ organizations by injecting malicious prompts to steal credentials and cryptocurrency; AI-enabled attack operations up 89% YoY |
| Jan 2026 | CHAI physical-environment prompt injection | UC Santa Cruz researchers demonstrated physical-world prompt injection against embodied AI agents |
| Mar 2026 | Langflow RCE (CVE-2026-33017, CVSS 9.8) | Unauthenticated code injection in Langflow's public flow build endpoint; exploited in the wild within 20 hours of disclosure — no PoC needed. CISA added to KEV catalog. All versions ≤ 1.8.1 affected. |
| Mar 2026 | Microsoft Semantic Kernel RCE (CVE-2026-26030) | Code injection via InMemoryVectorStore filter expressions in the Python SDK; allows remote code execution with low privileges. Fixed in python-1.39.4. |
| Jan–Feb 2026 | ShadowPrompt — Claude Chrome extension zero-click injection | Chained flaw: wildcard `*.claude.ai` origin allow-list + DOM-based XSS in an Arkose Labs CAPTCHA widget on `a-cdn.claude.ai` allowed any attacker-controlled page to send prompts that Claude treated as user-authored. Visiting the page was enough to exfiltrate access tokens and conversation history and perform actions in the user's name. Reported to Anthropic Dec 26, 2025; origin-check fix shipped in extension v1.0.41 on Jan 15, 2026; Arkose XSS fully patched Feb 19, 2026. |
| Feb 2026 | Reprompt — Microsoft Copilot single-click exfiltration (CVE-2026-24307) | Data exfiltration from Copilot via a crafted URL parameter requiring zero user-entered prompts. Demonstrates that indirect injection vectors now extend to URL/query-parameter surfaces, not just document content. |
| Apr 2026 | Help Net Security / US federal GenAI prompt-injection surge | Public-sector GenAI adoption brought prompt injection into routine government workflows; indirect injection now >55% of observed attacks in 2026 per multiple industry trackers. |

---

## Implementation Maturity Overview

A chapter-level view of tooling maturity and adoption status for C02 controls:

| Section | Area | Maturity | Notes |
|---------|------|:--------:|-------|
| C2.1 | Prompt Injection Defense | Medium-High | Commercial solutions (Lakera Guard, AWS Bedrock Guardrails) offer 98%+ detection at sub-50ms latency, but no tool guarantees complete prevention. Instruction hierarchy enforcement is provider-dependent. |
| C2.2 | Pre-Tokenization Input Normalization | Medium | Unicode normalization is straightforward; statistical anomaly detection and adversarial training are research-grade. Zero-width character and homoglyph attacks still bypass production guardrails from major vendors. |
| C2.3 | Content & Policy Screening | Medium-High | Content classifiers (OpenAI Moderation, Perspective API, Lakera Guard) are production-ready. Attribute-based per-user policy resolution is less mature. |
| C2.4 | Multi-Modal Validation | Low-Medium | Image and audio adversarial detection remains largely research-grade. Steganography scanning tools exist but are not widely integrated into AI pipelines. Cross-modal correlation is nascent. |

> **Overall:** As of March 2026, only ~20% of enterprises have mature AI governance models (Deloitte 2026 AI Report). Cisco's State of AI Security 2026 report found that while 83% of organizations plan to deploy agentic AI, only 29% feel ready to secure it. Input validation tooling is strongest for text-based prompt injection and weakest for multi-modal and adaptive scenarios. Notably, HiddenLayer researchers bypassed OpenAI's guardrails framework using straightforward techniques in October 2025, and Cisco found multi-turn prompt attacks achieve ~60% success rates on average (one model: 92.78%), underscoring that no single guardrail layer is sufficient. The first independent validation of AI firewall vendors (SecureIQLab, 32 scenarios across input/output/retrieval layers, OWASP- and MITRE ATLAS-aligned) begins April 2026 with results expected at Black Hat USA 2026 — this should provide the first empirical, vendor-independent efficacy data for the market.

---

## Defensive Tooling Landscape

Key tools and frameworks relevant across C02 sections:

| Tool / Framework | Type | Coverage | Notes |
|------------------|------|----------|-------|
| [Lakera Guard](https://www.lakera.ai/lakera-guard) | Commercial API | Prompt injection, jailbreak, data leakage detection | 98%+ detection, sub-50ms latency, 100+ languages. Acquired by Check Point (Sep 2025) and integrated into Infinity Platform. Learns from 100K+ daily adversarial samples via Gandalf. |
| [Rebuff](https://github.com/protectai/rebuff) | Open-source | Multi-layered prompt injection detection | Combines heuristic filtering, LLM-based analysis, vector DB of previous attacks, and canary tokens. Good for self-hosted deployments. |
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Open-source framework | Input/output validation, schema enforcement | Python framework with pluggable validators for PII, toxicity, schema compliance. Integrates with major LLM providers. |
| [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html) | Cloud service | Content filtering, topic denial, PII redaction | Native AWS integration for Bedrock-hosted models. Supports custom word filters and managed policies. |
| [Galileo Protect](https://galileo.ai/) | Commercial | Runtime guardrails for AI agents | Intercepts unsafe outputs in under 200ms. Enforces prompt injection blocking, PII redaction, hallucination prevention. |
| [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Open-source | Programmable guardrails for LLM applications | Colang-based rail definitions for topic control, jailbreak prevention, and output safety. |
| [LlamaFirewall](https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall) | Open-source (Meta) | Prompt injection, agent alignment, insecure code detection | Three-layer defense: PromptGuard 2 (86M/22M param jailbreak detectors), AlignmentCheck (real-time chain-of-thought auditor for injection and goal misalignment), and CodeShield (static analysis for 8 languages). Combined system reduced attack success rates by 90% in benchmarks (from 17.6% to 1.75%). Production-tested at Meta. |
| [OpenAI Guardrails](https://openai.github.io/openai-guardrails-python/) | Open-source SDK | Prompt injection detection, function call safety | Runs at two checkpoints (pre-execution, post-execution) to ensure agent actions remain aligned with user intent. Note: HiddenLayer bypassed both jailbreak and injection detection in October 2025 testing — treat as one layer in a defense-in-depth stack, not a standalone solution. |
| [Patronus AI](https://www.patronus.ai/) | Commercial | Hallucination detection, agentic debugging, safety evaluation | Lynx model outperforms GPT-4 on HaluBench benchmarks. Percival debugger provides visibility into agent decision chains. Primarily post-generation evaluation. |
| [Robust Intelligence (Cisco)](https://www.robustintelligence.com/) | Commercial | AI firewall, continuous validation, adversarial testing | Uses Tree of Attacks with Pruning (TAP) methodology backed by Cisco security research. Handles NLP, computer vision, and structured data. Combines runtime firewall with pre-deployment validation. |

---

## Related Standards & Cross-References

- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — Top risk for LLM applications; directly maps to C2.1 and C2.3
- [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — Released Dec 19, 2025. Prompt injection appears as ASI02 and is a primary pathway to ASI01 (Agent Goal Hijack). Introduces the Intent Capsule, Zero-Trust Tooling, and Least-Agency patterns that extend C2 controls into multi-agent and tool-using deployments.
- [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) — Practical defense patterns for developers
- [OWASP AI Exchange (2026)](https://owaspai.org/) — Comprehensive AI security guidance; input validation covered across multiple threat categories
- [OWASP AI Testing Guide v1 (November 2025)](https://owasp.org/www-project-ai-testing-guide/) — First comprehensive standard for AI trustworthiness testing, including input validation test cases
- [MITRE ATLAS: Adversarial Input Detection (AML.M00150)](https://atlas.mitre.org/mitigations/AML.M00150) — Mitigation guidance for adversarial inputs
- [MITRE ATLAS: Prompt Injection (AML.T0051)](https://atlas.mitre.org/techniques/AML.T0051) — Technique definition for prompt injection attacks
- [MITRE ATLAS October 2025 Update](https://atlas.mitre.org/) — 14 new attack techniques and sub-techniques for AI agents and GenAI systems (collaboration with Zenity Labs)
- [Mitigate jailbreaks and prompt injections (Anthropic)](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) — Provider-specific guidance on instruction hierarchy and prompt hardening
- [NIST AI 100-2e2025: Adversarial Machine Learning](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) — Taxonomy of adversarial ML attacks including evasion, poisoning, and prompt-based threats
- [CSA: How to Build AI Prompt Guardrails (December 2025)](https://cloudsecurityalliance.org/blog/2025/12/10/how-to-build-ai-prompt-guardrails-an-in-depth-guide-for-securing-enterprise-genai) — Enterprise-focused guide for DLP-first guardrail strategy
- [AWS Prescriptive Guidance: Input Validation for Agentic AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html) — Best practices for validating inputs in agentic AI systems on AWS
- [Defending LLM Applications Against Unicode Character Smuggling (AWS, 2025)](https://aws.amazon.com/blogs/security/defending-llm-applications-against-unicode-character-smuggling/) — Practical defense patterns for encoding-based attacks
- [CrowdStrike 2026 Global Threat Report](https://www.crowdstrike.com/en-us/global-threat-report/) — Documents prompt injection attacks against 90+ organizations and 89% YoY increase in AI-enabled adversary operations
- [Cisco State of AI Security 2026](https://www.cisco.com/site/us/en/products/security/state-of-ai-security.html) — 83% of organizations planning agentic AI deployment, only 29% ready to secure it; multi-turn attack success rates averaging ~60%
- [LlamaFirewall: An Open Source Guardrail System (Meta, May 2025)](https://arxiv.org/abs/2505.03574) — Three-layer defense architecture (PromptGuard 2, AlignmentCheck, CodeShield) achieving 90% reduction in attack success rates
- [SecureIQLab AI Security CyberRisk Validation](https://www.prnewswire.com/news-releases/up-to-20-ai-firewall-vendors-face-first-independent-security-validation-302724473.html) — First independent validation of up to 20 AI firewall vendors across 32 scenarios (input, output, retrieval layers), OWASP/MITRE ATLAS-aligned; results expected Black Hat USA 2026
- [CSA Research Note: Image-Based Prompt Injection in Multimodal LLMs (March 2026)](https://labs.cloudsecurityalliance.org/research/csa-research-note-image-prompt-injection-multimodal-llm-2026/) — Cloud Security Alliance analysis of visually embedded adversarial instructions that hijack vision-language models

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C7 Model Behavior | Output validation, guardrails | C2 handles input-side; C7 handles output-side enforcement |
| C9 Orchestration & Agents | Agent input surfaces, tool call validation | Agent chains amplify prompt injection risk across hops |
| C10 MCP Security | MCP tool argument validation | MCP surfaces are explicit input vectors |
| C11 Adversarial Robustness | Adversarial perturbation defense | C2.2 focuses on input-layer normalization; C11 covers model-level robustness |
| C12 Privacy | PII detection in inputs, data leakage prevention | C2 input screening should catch PII before it reaches the model; C12 governs retention and consent |
| C13 Monitoring & Logging | Logging requirements for input validation events | C2 specifies what to log; C13 specifies how to store and alert |
| C14 Human Oversight | HITL approval for flagged inputs | C2.4.3 requires HITL escalation for cross-modal attacks; C14 defines oversight governance |

---

## Key Research & Further Reading

- Syed et al., "Cross-Agent Multimodal Provenance-Aware Defense Framework," ICCA 2025 — combines input sanitization with output validation across agentic pipelines, establishing a provenance ledger that tracks modality, source, and trust level of every prompt.
- Chen et al., "AudioJailbreak," ACM CCS 2025 — demonstrated 87-88% jailbreak success against 10 end-to-end audio-language models, including over-the-air attacks.
- Xie et al., "Chain of Attack," CVPR 2025 — showed compounding effectiveness when steganographic embedding is chained with semantic manipulation across modalities.
- "Image-based Prompt Injection: Hijacking Multimodal LLMs through Visually Embedded Adversarial Instructions," arXiv:2603.03637 (March 2026) — latest work on imperceptible adversarial perturbations in images that hijack vision-language models.
- Palo Alto Unit 42, "Fooling AI Agents: Web-Based Indirect Prompt Injection Observed in the Wild" (December 2025) — first documented in-the-wild indirect prompt injection against a production AI ad review system.
- Schwartz et al., "EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System," arXiv:2509.10540 (September 2025) — detailed technical analysis of CVE-2025-32711, demonstrating how chained bypasses (XPIA classifier evasion, reference-style Markdown link redaction circumvention, auto-fetched image abuse) enabled zero-click data exfiltration from Microsoft 365 Copilot.
- Meta, "LlamaFirewall: An Open Source Guardrail System for Building Secure AI Agents," arXiv:2505.03574 (May 2025) — introduces PromptGuard 2, AlignmentCheck (first open-source chain-of-thought auditor for injection defense), and CodeShield; combined system achieves 90% ASR reduction in agentic scenarios.
- Vectra AI, "Prompt Injection: Types, Real-World CVEs, and Enterprise Defenses" (2025) — practical catalog of prompt injection CVEs (including LangGrinch, Cursor RCE) with enterprise mitigation patterns.
- Liang et al., "CrossInject: Manipulating Multimodal Agents via Cross-Modal Prompt Injection," ACM MM 2025 (arXiv:2504.14348) — demonstrated +30.1% attack success increase by embedding aligned adversarial signals across vision and text modalities simultaneously.
- Comprehensive survey of 78 recent prompt injection studies (2021–2026), published in Information (MDPI), 2026 — meta-analysis finding 85%+ attack success with adaptive strategies and 73% platform boundary enforcement failures.
- "[Stronger Enforcement of Instruction Hierarchy via Augmented Intermediate Representations](https://arxiv.org/abs/2505.18907)" (AIR), May 2025 — injects instruction-hierarchy signals recurrently across all transformer layers rather than only at the input layer, producing models measurably more robust to prompt injection. Directly relevant to the updated C2.1.2 requirement that hierarchy be preserved across multi-step interactions.
- "[Many-Tier Instruction Hierarchy in LLM Agents](https://arxiv.org/html/2604.09443)" (ManyIH, 2026) — extends instruction hierarchy beyond fixed role tiers to arbitrarily many privilege levels resolved at inference time; ManyIH-Bench ships 853 agentic tasks with up to 12 privilege levels (vs. 2–3 in prior work). Gives auditors a concrete benchmark for verifying C2.1.2 enforcement in deep agent stacks.
- "[AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents](https://cposkitt.github.io/files/publications/agentspec_llm_enforcement_icse26.pdf)" (ICSE 2026) — runtime policy engine for agentic LLM deployments; PRISM-style layered configurations (input filtering + pattern matching + semantic intent analysis + runtime approvals + auditability) raise attack block rates from 0% (no defense) to 95.5% in published benchmarks.
- [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), published Dec 19, 2025 — companion framework to the LLM Top 10 that addresses agent-specific failure modes. Prompt Injection appears as **ASI02**, with Agent Goal Hijack (**ASI01**) leaning on "Aegis" prompt-injection detection as its primary control. Key architectural patterns include the "Intent Capsule" (a signed, immutable envelope binding the agent's original mandate to each execution cycle), a Zero-Trust Tooling model with strict schema validation before tool invocation, and the Least-Agency principle (agents get only the minimum autonomy required). These shape how C2.1–C2.4 should be verified in agentic deployments.

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

**Open questions worth tracking:**
- No input validation tool guarantees complete prompt injection prevention. Defense-in-depth (combining multiple layers) remains the only viable strategy. How should auditors assess "sufficient" defense depth? The HiddenLayer bypass of OpenAI's guardrails (October 2025) reinforces this — guardrail LLMs are themselves susceptible to the attacks they're meant to detect.
- Multi-modal adversarial detection tooling is still largely research-grade. Organizations deploying vision or audio models should treat C2.4 requirements as aspirational L2/L3 targets until tooling matures.
- The October 2025 MITRE ATLAS update added 14 agentic-specific techniques — these may drive future requirement additions to C2.1 (indirect injection via agent chains) and C2.4 (MCP argument validation).
- As of March 2026, zero-click indirect injection (EchoLeak pattern) represents a step change in threat severity. Organizations using AI copilots with access to email, documents, and external communication should audit for the "Lethal Trifecta" (private data access + untrusted token exposure + exfiltration vector) and implement image/link fetching restrictions as an immediate mitigation.
- The CrowdStrike 2026 report's finding of prompt injection at 90+ organizations suggests this is no longer a theoretical or red-team-only concern — it's an active adversary technique at scale. System prompt extraction was the most common objective in Q4 2025, giving attackers role definitions, tool descriptions, and workflow logic.
- Langflow CVE-2026-33017 (exploited in 20 hours, March 2026) is a watershed moment for AI framework security — it demonstrates that vulnerabilities in AI pipeline tooling are now targeted with the same speed as traditional web application zero-days. Organizations running AI orchestration frameworks should treat them with the same patching urgency as internet-facing web servers.
- The SecureIQLab independent validation initiative (April 2026) will be the first empirical, vendor-neutral assessment of AI firewall efficacy. Until those results land, organizations should remain skeptical of vendor detection-rate claims and test products against their own threat models.
- Cross-modal attacks (CrossInject achieving +30.1% success) and embedding-space attacks that require only vision encoder access (not full LLM access) are lowering the bar for multimodal exploitation. C2.4 controls are becoming more urgent, not less.
- The ShadowPrompt disclosure (Jan–Feb 2026) is a reminder that **even the vendor's own browser extension is part of the input surface area** that C2.1.1 covers. Origin allow-lists should use exact strings, not wildcards, and every iframe/postMessage path that can deliver content into an LLM context should be treated as a potential untrusted input vector. This also validates the updated C2.1.2 wording requiring hierarchy enforcement across tool-augmented and multi-step workflows — once injected content is indistinguishable from a user turn, downstream hierarchy checks are the only remaining defense.
- The updated C2.1.3 wording (**reject** over-length inputs rather than silently truncate) is a direct response to context-window flooding and many-shot jailbreaking. Anthropic's "Cautionary Warning Defense" dropped many-shot attack success from ~61% to ~2% in their research, but requires the system to actually see the input's length and intent — silent truncation hides both. Auditors should now expect explicit 413-style errors for oversize prompts and should test for them.
- Enterprise readiness lags sharply. McKinsey's 500-deployment survey reports average system downtime of 72 hours per successful prompt-injection incident, a 23% drop in customer-trust scores for affected organizations, and a $340K average incident-response cost. Recorded Future pegs 2025 global losses from prompt-injection attacks at ~$2.3B, with 67% of incidents targeting customer-service chatbots and AI-backed trading systems. Only 34.7% of surveyed organizations have dedicated prompt-injection defenses deployed (VentureBeat, April 2026).

---

## Related Pages

- [C02-01 Prompt Injection Defense](C02-01-Prompt-Injection-Defense) — the per-requirement deep dive on C2.1, where this chapter's hub-level threat landscape translates into specific detection rules, instruction-hierarchy enforcement, and many-shot jailbreak controls.
- [C02-04 Multi-Modal Input Validation](C02-04-Multi-Modal-Input-Validation) — companion research for C2.4, covering adversarial image/audio/video attacks, steganographic payloads, and cross-modal jailbreak detection that this chapter introduces at summary level.
- [C10-04 Schema, Message & Input Validation (MCP)](C10-04-Schema-Message-Validation) — where C2.1.1's "treat all external or derived inputs as untrusted" meets MCP's tool-argument surface: schema signing, message framing, rug-pull detection, and response sanitization on the agent-to-tool boundary.
