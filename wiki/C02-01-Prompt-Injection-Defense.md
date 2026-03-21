# C2.1 Prompt Injection Defense

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation.md)
> **Last Researched:** 2026-03-21

## Purpose

Prompt injection is consistently ranked the #1 risk for LLM-based systems (OWASP LLM01:2025). Attacks range from direct injection (user crafts input to override system instructions) to indirect injection (malicious instructions embedded in retrieved documents, tool outputs, MCP responses, or third-party content). As of 2026, no model reliably defends against prompt injection through alignment alone — this is consensus across Google DeepMind, HiddenLayer, OWASP, and academic research. A meta-analysis of 78 studies (2021–2026) found adaptive attack success rates exceed 85% against state-of-the-art defenses. Defense-in-depth with layered controls is the only viable strategy.

The threat has evolved beyond isolated prompt tricks. The Promptware Kill Chain (Schneier et al., January 2026) formalizes prompt injection as merely the "Initial Access" step in a seven-stage attack chain: Initial Access → Privilege Escalation → Reconnaissance → Persistence → C2 → Lateral Movement → Actions on Objective. Analysis of 36 real-world incidents (21 from 2025–2026) shows attacks now routinely reach 4+ stages, with LLM memory features serving as persistent command channels.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.1.1** | **Verify that** any external or derived input that may steer behavior, including user prompts, RAG results, tool integration or MCP outputs, agent to agent messages, API or webhook responses, configuration or policy files, memory reads and memory writes, is treated as untrusted, made inert by quoting or tagging and active content removal, and screened by a maintained prompt injection detection ruleset or service before concatenation into prompts or execution of actions. | 1 | D/V | Direct and indirect prompt injection; instruction override via any untrusted input channel including RAG poisoning, tool output manipulation, and memory injection ([MITRE ATLAS AML.T0051](https://atlas.mitre.org/techniques/AML.T0051)). Palo Alto Unit 42 (February 2026) documented 22 distinct payload delivery techniques in production, including HTML attribute cloaking (19.8%), CSS rendering suppression (16.9%), zero-font sizing, Base64 assembly, and Unicode bi-directional override. CVE-2025-32711 (EchoLeak, CVSS 9.3) demonstrated zero-click injection in Microsoft 365 Copilot via document comments. MINJA attacks corrupt agent long-term memory, enabling persistence across sessions. | 1. Review architecture diagrams for all input surfaces and confirm each is classified as untrusted. 2. Inspect prompt assembly code for delimiter/tagging of untrusted content (XML tags, triple-backtick quoting, spotlighting). 3. Confirm a prompt injection detection service is invoked before concatenation — options as of March 2026: Meta Prompt Guard 2 (86M and 22M variants), PromptArmor (ICLR 2026, sub-1% FPR/FNR on AgentDojo), DefensiveTokens (0.24% ASR), LLM Guard, Lakera Guard. 4. Red-team with known injection payloads across all input channels using Promptfoo (now OpenAI, acquired March 2026) or Garak (NVIDIA). 5. Test MCP tool outputs and RAG results specifically for indirect injection. 6. Verify memory write operations include injection screening. | Detection is improving rapidly but remains imperfect. PromptArmor (ICLR 2026) achieves 0.56% FPR / 0.13% FNR on AgentDojo using an off-the-shelf LLM as preprocessor — the best published result. DefensiveTokens (AISec '25) appends 5 optimized tokens before input, reducing ASR to 0.24% with zero model changes. However, a meta-analysis of 78 studies found adaptive attacks still beat SOTA defenses >85% of the time. ToolHijacker achieved 96.43% ASR against GPT-4o on MetaTool, defeating both StruQ and SecAlign. No single defense is sufficient — layered deployment is essential. Cloud providers: AWS Bedrock Guardrails (requires `guardContent` tags), Azure Prompt Shields + Spotlighting (Build 2025), Google Model Armor (10K token limit). |
| **2.1.2** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after processing user instructions. | 1 | D/V | Privilege escalation via prompt injection; system prompt override; jailbreaking by redefining model behavior through user input. Policy Puppetry (HiddenLayer, April 2025) demonstrated universal bypass across all major models. ChatInject (ICLR 2026) formats payloads to mimic native chat template structure, wrapping malicious instructions in system role tags so agents accept them as natural conversation continuations. | 1. Inspect prompt templates to confirm system/developer instructions use the system message role. 2. Test with adversarial prompts attempting override ("ignore previous instructions", "you are now..."). 3. Verify the model API uses proper role separation (system vs. user vs. assistant). 4. Test with Policy Puppetry, ChatInject, and crescendo-style multi-turn attacks. 5. For Anthropic: confirm system prompt is used; for OpenAI: confirm system message and Instruction Hierarchy (IH) training is active; for Google: confirm system instructions. 6. Verify that tool descriptions and MCP server responses cannot inject system-level instructions. | OpenAI shipped Instruction Hierarchy (IH) training, giving system prompts highest trust, user instructions moderate trust, and external content lowest trust — GPT-5 Mini-R shows consistent improvement with no helpfulness decrease. Meta SecAlign (CCS 2025, open-source) introduces a distinct "input" role for untrusted data and reduces injection success to <10% even against unseen attacks. CaMeL (Google Research, 2025) offers provable security via control/data flow separation. However, ChatInject (ICLR 2026) shows that chat template structure itself can be weaponized to bypass hierarchy enforcement. Multi-turn grooming and role-play attacks still achieve >80% success even on hardened models. |
| **2.1.3** | **Verify that** prompts originating from third-party content (web pages, PDFs, emails) are sanitized in isolation (for example, stripping instruction-like directives and neutralizing HTML, Markdown, and script content) before being concatenated into the main prompt. | 2 | D | Indirect prompt injection via retrieved or ingested content. Notable incidents: GitHub MCP data heist (May 2025) — attackers embedded commands in public Issues, exfiltrating private code; Perplexity Comet vulnerability (Aug 2025) — hidden Reddit comments triggered command execution; ICML peer review scandal (2025–2026) — invisible-font text in submission PDFs with "IGNORE ALL PREVIOUS INSTRUCTIONS" targeted AI reviewers; CVE-2025-53773 (ZombAI, CVSS 7.8) — code comments in repos propagated wormable prompt injection through GitHub Copilot, enabling persistent RCE. Third-party chatbot plugins (IEEE S&P 2026) found 15 of 17 plugins scrape website content indiscriminately, enabling indirect injection via product reviews with 20–100% success. | 1. Map all third-party content ingestion paths (web scraping, document parsing, email, RSS, MCP tool outputs, chatbot plugins). 2. Review sanitization logic: HTML/Markdown stripping, instruction-like pattern removal, content isolation from system instructions. 3. Test with crafted documents containing hidden injection payloads (HTML comments, invisible PDF text, image alt-text, metadata fields, CSS-hidden content, zero-font text). 4. Verify sanitization happens before concatenation, not after. 5. Test for the 22 payload engineering techniques documented by Unit 42 (HTML attribute cloaking, CSS suppression, SVG encapsulation, canvas-based OCR targeting). 6. For browser agents: test against BrowseSafe-Bench (14,719 samples, 11 attack types). | Sanitization is necessary but not sufficient — no reliable way to strip "instruction-like directives" from natural language without false positives. Google DeepMind (May 2025) found in-context defenses help but fail against adaptive attacks. Perplexity's BrowseSafe defense was bypassed at 36% by Lasso Security using standard encoding techniques. Content Disarm and Reconstruction (CDR) for inbound documents is emerging as a complementary control. The wormable nature of ZombAI (infected repos propagate to subsequent developers) shows third-party content injection can have cascading effects. |
| **2.1.4** | **Verify that** input length controls account for context window limits and that the system prevents user-supplied content from exceeding a proportion of the total context window that would displace system instructions or safety directives from the model's effective attention. | 1 | D/V | Context window hijacking; system prompt displacement; attention dilution attacks (Liu et al., 2023 "Lost in the Middle"). LoopLLM (AAAI 2026) demonstrated transferable energy-latency attacks achieving 90%+ of maximum output length on 12 open-source LLMs and ~40% transferability to commercial APIs, exploiting context window capacity for resource exhaustion. | 1. Review token counting logic — must use the correct tokenizer for the target model. 2. Verify a maximum user input length is enforced (e.g., user content limited to 60–80% of total context). 3. Test with maximum-length inputs and confirm system instructions remain effective. 4. Check that system instructions are positioned at beginning and end of context (sandwich defense). 5. Measure instruction adherence as input length increases. 6. Test for LoopLLM-style attacks that force maximum output generation. | "Effective attention" is model-dependent. Lost-in-the-middle research shows models attend less to mid-context content. The sandwich defense (system instructions before and after user content) partially mitigates this. Context window sizes are increasing rapidly (1M+ tokens), making proportion-based limits harder to enforce. Token counting must match the model's tokenizer exactly. AWS Bedrock Guardrails requires explicit content tagging to distinguish user from system content. |

---

## Recent Defensive Advances (2025-2026)

### Detection Tools

| Tool | Type | Performance | Notes |
|------|------|-------------|-------|
| [PromptArmor](https://arxiv.org/abs/2507.15219) | LLM preprocessor (ICLR 2026) | 0.56% FPR, 0.13% FNR on AgentDojo; <1% ASR | Uses off-the-shelf LLM to detect and remove injected prompts. No fine-tuning required. Best published result. |
| [Meta Prompt Guard 2](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) | Classifier (86M and 22M variants) | AUC .998, 81.2% APR on AgentDojo | 22M variant reduces latency ~75%. Bypassed via non-English and leetspeak. |
| [Meta LlamaFirewall](https://meta-llama.github.io/PurpleLlama/LlamaFirewall/) | Framework (3 components) | >90% efficacy on AgentDojo | PromptGuard 2 + Agent Alignment Checks (CoT auditor) + CodeShield. In production at Meta. |
| [DefensiveTokens](https://arxiv.org/abs/2507.07974) | Test-time defense (AISec '25) | 0.24% ASR on 31K-sample benchmark | Appends 5 optimized token embeddings before input. Zero model changes. |
| [SecAlign / Meta-SecAlign](https://arxiv.org/abs/2507.02735) | Preference optimization (CCS 2025) | <10% injection success on unseen attacks | Introduces "input" role for untrusted data. Meta-SecAlign-70B open-source, more secure than several proprietary models. |
| [Lakera Guard](https://www.lakera.ai/lakera-guard) | Runtime API | 98%+ detection, <50ms, 100+ languages | Acquired by Check Point Sept 2025. |
| [Promptfoo](https://www.promptfoo.dev/docs/red-team/) | Red-team framework | CI/CD integration; trusted by >25% Fortune 500 | Acquired by OpenAI March 2026; will integrate into OpenAI Frontier agent platform. Remains open-source. |
| [Garak](https://github.com/NVIDIA/garak) | Vuln scanner | Modular probes (latentinjection, AutoDAN, GCG) | NVIDIA; last updated Feb 2026. |
| [Cisco AI Defense](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html) | Enterprise platform | MCP traffic inspection (Feb 2026) | Real-time agentic guardrails; MCP Catalog; AI BOM. Integrates NeMo Guardrails. |

### Cloud Provider Defenses

| Provider | Product | Key Features |
|----------|---------|-------------|
| AWS | Bedrock Guardrails | Prompt attack detection (jailbreak + injection + prompt leakage). Requires `guardContent` tags. TEXT + IMAGE modalities. Configurable BLOCK/DETECT. |
| Azure | Prompt Shields + Spotlighting | Direct and indirect attack detection (GA Aug 2024). Spotlighting (Build 2025) tags trusted vs. untrusted. Task Adherence (preview Nov 2025) detects misaligned tool invocations. |
| Google | Model Armor | Model-agnostic prompt/response screening. Prompt injection filter supports 10K tokens. Integrated with Gemini Enterprise and Vertex AI. |

### Architectural Defenses

| Defense | Approach | Effectiveness |
|---------|----------|---------------|
| **CaMeL** (Google Research, 2025) | Separates control/data flow; untrusted data cannot impact program execution | 77% task completion with provable security on AgentDojo |
| **OpenAI Instruction Hierarchy (IH)** | System prompts highest trust, external content lowest; model trained to follow hierarchy | GPT-5 Mini-R shows consistent improvement, no helpfulness decrease |
| **Spotlighting / XML tagging** | Explicit demarcation of trusted vs. untrusted content boundaries | Reduces indirect injection success; not proof against adaptive attacks |
| **Sandwich defense** | System instructions before and after user content | Mitigates lost-in-the-middle attention degradation |
| **Adversarial fine-tuning** | Fine-tune model against adversarial examples | Google DeepMind: improves robustness without degrading capabilities |
| **StruQ** (Structured Query) | Research-backed prompt structuring to separate instructions from data | Reduces attack surface; defeated by ToolHijacker (99.71% ASR) |
| **Content Disarm & Reconstruction** | Strip active content from documents before processing | Emerging complementary control for indirect injection via files |
| **Provenance-aware defense** | Track modality, source, and trust level of every prompt/output across agents | Academic framework (Jan 2026) for LangChain/GraphChain multi-agent systems |

---

## Notable Incidents & Research (2025-2026)

| Date | Incident / Paper | Impact | Source |
|------|------------------|--------|--------|
| Apr 2025 | Policy Puppetry (HiddenLayer) | Universal bypass across all frontier models via role-play + policy formatting | [HiddenLayer](https://hiddenlayer.com/innovation-hub/novel-universal-bypass-for-all-major-llms) |
| May 2025 | GitHub MCP data heist (Invariant) | Embedded commands in public Issues exfiltrated private repo code and keys | [Docker blog](https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/) |
| May 2025 | Google DeepMind indirect injection defenses | Adversarial fine-tuning > in-context defenses; adaptive evaluation critical | [arXiv:2505.14534](https://arxiv.org/abs/2505.14534) |
| May 2025 | CaMeL framework (Google Research) | Provable security via control/data flow separation; 77% task completion | [arXiv:2503.18813](https://arxiv.org/abs/2503.18813) |
| Jun 2025 | CVE-2025-32711 — EchoLeak (M365 Copilot, CVSS 9.3) | Zero-click injection via document comments exfiltrated emails, drafts, files | [HackTheBox](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability) |
| Aug 2025 | CVE-2025-53773 — ZombAI (GitHub Copilot RCE, CVSS 7.8) | Wormable injection via code comments enabled persistent RCE; disabled user confirmations | [Embrace The Red](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/) |
| Aug 2025 | Perplexity Comet browser vulnerability | Hidden Reddit comments triggered command execution during summarization | — |
| Oct 2025 | DefensiveTokens (AISec '25) | Test-time defense: 5 tokens reduce ASR to 0.24% with zero model changes | [arXiv:2507.07974](https://arxiv.org/abs/2507.07974) |
| Dec 2025 | CVE-2025-68664 — LangGrinch (LangChain Core, CVSS 9.3) | Serialization injection via LLM outputs; 847M downloads exposed; $4K bounty | [Cyata](https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/) |
| Dec 2025 | Unit 42 MCP sampling attack vectors | Hidden prompts in sampling requests enable resource theft, conversation hijacking, covert tool invocation | [Unit 42](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/) |
| Jan 2026 | Promptware Kill Chain (Schneier et al.) | Formalizes 7-stage attack chain; 36 real-world incidents cataloged (21 from 2025–2026) | [arXiv:2601.09625](https://arxiv.org/abs/2601.09625) |
| Jan 2026 | CHAI physical prompt injection (UC Santa Cruz) | Physical-environment injection targeting embodied AI systems | — |
| Feb 2026 | Unit 42 — 22 payload engineering techniques | First documented real-world IDPI against production AI ad-review; HTML cloaking, CSS suppression, SVG encapsulation | [Unit 42](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/) |
| Feb 2026 | ChatInject (ICLR 2026) | Chat template mimicry causes agents to accept injections as natural conversation | [GitHub](https://github.com/hwanchang00/ChatInject) |
| Mar 2026 | CVE-2026-32626 — AnythingLLM streaming XSS-to-RCE (CVSS 9.7) | Prompt injection via RAG documents achieved arbitrary code execution | [GHSA-rrmw-2j6x-4mf2](https://github.com/Mintplex-Labs/anything-llm/security/advisories/GHSA-rrmw-2j6x-4mf2) |
| Mar 2026 | OpenAI acquires Promptfoo | Red-teaming tooling goes native in OpenAI Frontier; remains open-source | [OpenAI](https://openai.com/index/openai-to-acquire-promptfoo/) |
| 2025 | Crescendo multi-turn attack (USENIX Security) | 98% success on GPT-4, 100% on Gemini-Pro; defeats per-request inspection | [arXiv:2404.01833](https://arxiv.org/abs/2404.01833) |

---

## Benchmarks

| Benchmark | Date | Scale | Focus |
|-----------|------|-------|-------|
| [AgentDojo](https://agentdojo.spylab.ai/) | 2024+ | Standard | Agentic prompt injection defense; used by PromptArmor, LlamaFirewall |
| [AgentDyn](https://arxiv.org/abs/2602.03117) | Feb 2026 | 60 tasks, 560 injection cases | Dynamic open-ended agent tasks; found most defenses either insecure or over-defensive |
| [MASpi](https://openreview.net/forum?id=1khmNRuIf9) | ICLR 2026 | 1,356 cases, 28 attacks, 7 systems | Multi-agent injection; single-agent defenses don't transfer to multi-agent systems |
| [WAInjectBench](https://github.com/Norrrrrrr-lyn/WAInjectBench) | Late 2025 | Text + image modalities | Web-agent prompt injection; detectors fail against attacks without explicit instructions |
| [BrowseSafe-Bench](https://arxiv.org/abs/2511.20597) | Late 2025 | 14,719 samples, 11 attack types | Browser-agent focused; bypassed at 36% by Lasso Security |
| [GenTel-Bench](https://arxiv.org/abs/2409.19521) | 2025 | 84,812 attacks, 28 scenarios | Unified benchmark across 3 attack categories |
| [TensorTrust](https://openreview.net/forum?id=fsW7wJGLBd) | Ongoing | 563K attacks, 118K defenses | Crowdsourced; covers prompt extraction and hijacking |
| [BIPIA](https://github.com/microsoft/BIPIA) (Microsoft, KDD '25) | Aug 2025 | 25 LLMs evaluated | Indirect injection; found all tested LLMs universally vulnerable |

---

## Red-Teaming Statistics (Mindgard & Cisco, 2025-2026)

- Prompt injection found in **70%** of security audits
- Role-play attacks: **89.6%** success rate
- Multi-turn jailbreaks: **97%** success within 5 turns
- Healthcare LLM adversarial objectives: **94.4%** completion rate
- Automated red teaming found **37% more** unique issues than manual
- Only **26%** of organizations conduct proactive AI security testing
- Only **34.7%** have purchased dedicated prompt filtering solutions
- **83%** plan to deploy agentic AI; only **29%** feel ready to secure it (Cisco State of AI Security 2026)
- Adaptive attack success rates against SOTA defenses: **>85%** (meta-analysis of 78 studies, 2021–2026)
- Agent systems with auto-execution: **66.9–84.1%** attack success rate (Cisco 2026)

---

## MCP-Specific Attack Vectors

Tool-use and MCP prompt injection is the fastest-growing threat surface as of 2026:

- **Tool Poisoning**: Malicious instructions embedded in MCP tool descriptions (measured by MCPTox benchmark). ToolCommander (Dec 2024) achieved 100% DoS ASR and 91.67% privacy theft ASR via adversarial suffixes in tool descriptions.
- **Tool Shadowing / ToolHijacker**: Attacker tool named identically to legitimate tool with crafted descriptions. ToolHijacker (April 2025) achieved 96.43% ASR against GPT-4o, cross-model transferable, defeating both StruQ and SecAlign.
- **Rug-Pull Redefinitions**: Tool descriptions silently alter post-approval. Elastic Security Labs documented a "daily_quote" tool that covertly instructed transaction processors to skim 0.5% fees.
- **MCP Sampling Exploitation**: Unit 42 (December 2025) demonstrated resource theft via hidden prompts, conversation hijacking, and covert tool invocation through MCP's bidirectional sampling feature.
- **MCP Command Injection**: Keysight (January 2026) found 43% of tested MCP implementations contained command injection flaws — classic code-level vulnerabilities, not just prompt injection.
- **Namespace Collision**: Multiple concurrent MCP servers create call interception opportunities.
- **Cross-Tool Description Injection**: A tool's description alone can steer models to alter other tools' behavior. Elastic documented descriptions that instructed `grep_search` to extract API keys and append them to outgoing messages.

**MCP spec security improvements** (OAuth 2.1 with PKCE, resource indicators, client registration, machine-to-machine auth via SEP-1046) address transport and authorization but not prompt injection at the protocol level. Tool description integrity verification and injection-resistant sampling remain unstandardized.

See also: [C10.4 Schema & Message Validation](C10-04-Schema-Message-Validation.md)

---

## Implementation Maturity

| Area | Maturity | Notes |
|------|----------|-------|
| Detection classifiers | **Medium-High** | PromptArmor, Prompt Guard 2, DefensiveTokens show strong results. Still bypassed by adaptive attacks. |
| Model-level instruction hierarchy | **Medium** | OpenAI IH training, Meta SecAlign improving. Not universally available across providers. |
| Architectural separation (CaMeL-style) | **Low** | Provable security demonstrated in research. Not deployed in production systems. |
| MCP/tool injection defense | **Low** | 43% of MCP implementations have command injection. No standardized tool description integrity verification. |
| Multi-agent injection defense | **Low** | MASpi shows single-agent defenses don't transfer. Provenance-aware frameworks are academic only. |
| Enterprise adoption | **Low-Medium** | 34.7% have purchased dedicated solutions. 83% plan agentic AI but only 29% feel secure. |

---

## Related Standards & References

- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [OWASP AI Testing Guide: AITG-APP-01 Prompt Injection](https://github.com/OWASP/www-project-ai-testing-guide/blob/main/Document/content/tests/AITG-APP-01_Testing_for_Prompt_Injection.md)
- [Mitigate jailbreaks and prompt injections (Anthropic)](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
- [MITRE ATLAS AML.T0051: LLM Prompt Injection](https://atlas.mitre.org/techniques/AML.T0051)
- [CaMeL: Provable Prompt Injection Defense](https://github.com/google-research/camel-prompt-injection) (arXiv:2503.18813)
- [LlamaFirewall (Meta)](https://meta-llama.github.io/PurpleLlama/LlamaFirewall/) (arXiv:2505.03574)
- [Defending Gemini Against Indirect Prompt Injections (Google DeepMind)](https://arxiv.org/abs/2505.14534)
- [Policy Puppetry (HiddenLayer)](https://hiddenlayer.com/innovation-hub/novel-universal-bypass-for-all-major-llms)
- [Crescendo Attack (USENIX Security 2025)](https://arxiv.org/abs/2404.01833)
- [Not what you've signed up for: Indirect Prompt Injection (Greshake et al., 2023)](https://arxiv.org/abs/2302.12173)
- [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/abs/2307.03172)
- [The Promptware Kill Chain (Schneier et al., 2026)](https://arxiv.org/abs/2601.09625)
- [PromptArmor (ICLR 2026)](https://arxiv.org/abs/2507.15219)
- [DefensiveTokens (AISec '25)](https://arxiv.org/abs/2507.07974)
- [SecAlign / Meta-SecAlign (CCS 2025)](https://arxiv.org/abs/2507.02735)
- [ChatInject (ICLR 2026)](https://github.com/hwanchang00/ChatInject)
- [Unit 42 — Indirect Prompt Injection in the Wild](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/)
- [Unit 42 — MCP Sampling Attack Vectors](https://unit42.paloaltonetworks.com/model-context-protocol-attack-vectors/)
- [Elastic Security Labs — MCP Tools: Attack Vectors and Defense](https://www.elastic.co/security-labs/mcp-tools-attack-defense-recommendations)
- [Keysight — MCP Command Injection](https://www.keysight.com/blogs/en/tech/nwvs/2026/01/12/mcp-command-injection-new-attack-vector)
- [ToolHijacker — Prompt Injection Attack to Tool Selection](https://arxiv.org/abs/2504.19793)
- [OpenAI — Instruction Hierarchy](https://openai.com/index/instruction-hierarchy-challenge/)
- [OpenAI — Designing Agents to Resist Prompt Injection](https://openai.com/index/designing-agents-to-resist-prompt-injection/)
- [Cisco State of AI Security 2026](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)
- [CVE-2025-32711 — EchoLeak](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability)
- [CVE-2025-53773 — ZombAI (GitHub Copilot RCE)](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/)
- [CVE-2025-68664 — LangGrinch (LangChain Core)](https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/)
- [Third-Party Chatbot Plugin Injection (IEEE S&P 2026)](https://arxiv.org/abs/2511.05797)

---

## Cross-Chapter Links

| Related Section | Overlap |
|----------------|---------|
| [C02-02 Adversarial Example Resistance](C02-02-Adversarial-Example-Resistance.md) | Multi-modal injection via perturbed images/audio |
| [C02-03 Prompt Character Set](C02-03-Prompt-Character-Set.md) | Unicode normalization, homoglyph mapping, invisible characters |
| [C02-05 Content Policy Screening](C02-05-Content-Policy-Screening.md) | Content classifiers as complementary layer |
| [C09-03 Tool and Plugin Isolation](C09-03-Tool-and-Plugin-Isolation.md) | Tool sandboxing to contain injection impact |
| [C10-04 Schema & Message Validation](C10-04-Schema-Message-Validation.md) | MCP tool description integrity, schema validation |
| [C10-05 Outbound Access & Agent Safety](C10-05-Outbound-Access-Agent-Safety.md) | Egress controls to limit exfiltration after injection |
| [C11-01 Model Alignment Safety](C11-01-Model-Alignment-Safety.md) | Instruction following, refusal guardrails |
| [C13-02 Abuse Detection & Alerting](C13-02-Abuse-Detection-Alerting.md) | Detection of injection attempts in monitoring |

---

## Open Research Questions

- Can instruction hierarchy be formally guaranteed at the model level, or will it always be a probabilistic defense? CaMeL suggests the answer is architectural, not model-level. OpenAI's IH training is a middle ground.
- What is the optimal ratio of system instruction tokens to user content tokens for maintaining instruction adherence across different model families?
- How should prompt injection detection evolve to handle multi-turn conversational attacks (crescendo), given 97% success within 5 turns?
- Is there a reliable cross-provider benchmark beyond AgentDojo? AgentDyn, MASpi, and WAInjectBench are expanding coverage to agentic and web-agent scenarios.
- How do MCP ecosystems change the attack surface — given 43% command injection and ToolHijacker's 96.43% ASR, is the current MCP security model viable?
- Can adversarial fine-tuning scale to defend against the long tail of creative injection techniques without capability degradation?
- How should physical-environment prompt injection (CHAI) be addressed for embodied AI systems?
- As the Promptware Kill Chain shows attacks reaching 4+ stages, should defenses shift from perimeter-only to defense-in-depth across all 7 stages?

---

[C02 Index](C02-User-Input-Validation.md) | [README](README.md)
