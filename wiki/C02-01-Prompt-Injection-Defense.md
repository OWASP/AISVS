# C2.1 Prompt Injection Defense

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation.md)
> **Last Researched:** 2026-03-18

## Purpose

Prompt injection is consistently ranked the #1 risk for LLM-based systems (OWASP LLM01:2025). Attacks range from direct injection (user crafts input to override system instructions) to indirect injection (malicious instructions embedded in retrieved documents, tool outputs, MCP responses, or third-party content). As of 2026, no model reliably defends against prompt injection through alignment alone — this is consensus across Google DeepMind, HiddenLayer, OWASP, and academic research. Defense-in-depth with layered controls is the only viable strategy.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.1.1** | **Verify that** any external or derived input that may steer behavior, including user prompts, RAG results, tool integration or MCP outputs, agent to agent messages, API or webhook responses, configuration or policy files, memory reads and memory writes, is treated as untrusted, made inert by quoting or tagging and active content removal, and screened by a maintained prompt injection detection ruleset or service before concatenation into prompts or execution of actions. | 1 | D/V | Direct and indirect prompt injection; instruction override via any untrusted input channel including RAG poisoning, tool output manipulation, and memory injection (MITRE ATLAS AML.T0051). | 1. Review architecture diagrams for all input surfaces and confirm each is classified as untrusted. 2. Inspect prompt assembly code for delimiter/tagging of untrusted content (e.g., XML tags, triple-backtick quoting, spotlighting). 3. Confirm a prompt injection detection service is invoked before concatenation (e.g., Meta Prompt Guard 2, Lakera Guard, LLM Guard). 4. Red-team with known injection payloads across all input channels using Promptfoo or Garak. 5. Test MCP tool outputs and RAG results specifically for indirect injection. | Intentionally broad — enumerates every untrusted input surface. Detection services have known bypass rates: Prompt Guard 2 (86M) achieves 81.2% APR on AgentDojo but is bypassed via non-English prompts and leetspeak. Lakera Guard reports 98%+ detection but was acquired by Check Point (Sept 2025). No single detector is sufficient. |
| **2.1.2** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after processing user instructions. | 1 | D/V | Privilege escalation via prompt injection; system prompt override; jailbreaking by redefining model behavior through user input. Policy Puppetry (HiddenLayer, April 2025) demonstrated universal bypass across all major models using role-play combined with policy formatting. | 1. Inspect prompt templates to confirm system/developer instructions use the system message role. 2. Test with adversarial prompts attempting override ("ignore previous instructions", "you are now..."). 3. Verify the model API uses proper role separation (system vs. user vs. assistant). 4. Test with Policy Puppetry and crescendo-style multi-turn attacks, not just single-turn injections. 5. For Anthropic: confirm system prompt is used; for OpenAI: confirm system message; for Google: confirm system instructions. | No model guarantees perfect instruction hierarchy enforcement. As of 2025, Claude 3 identified as most resilient; Gemini most vulnerable. Multi-turn grooming and role-play attacks achieve >80% success even on hardened models. CaMeL (Google Research, 2025) offers provable security by separating control flow from data flow at the architecture level rather than relying on model compliance. |
| **2.1.3** | **Verify that** prompts originating from third-party content (web pages, PDFs, emails) are sanitized in isolation (for example, stripping instruction-like directives and neutralizing HTML, Markdown, and script content) before being concatenated into the main prompt. | 2 | D | Indirect prompt injection via retrieved or ingested content. Notable incidents: GitHub MCP data heist (May 2025) — attackers embedded commands in public Issues, exfiltrating private repo source code; Perplexity Comet browser vulnerability (Aug 2025) — hidden Reddit comments triggered command execution during page summarization. | 1. Map all third-party content ingestion paths (web scraping, document parsing, email, RSS, MCP tool outputs). 2. Review sanitization logic: HTML/Markdown stripping, instruction-like pattern removal, content isolation from system instructions. 3. Test with crafted documents containing hidden injection payloads (HTML comments, invisible PDF text, image alt-text, metadata fields). 4. Verify sanitization happens before concatenation, not after. 5. Test specifically for Greshake-style indirect injection via RAG results. | Sanitization is necessary but not sufficient — no reliable way to strip "instruction-like directives" from natural language without false positives. Google DeepMind (May 2025, arXiv:2505.14534) found in-context defenses (spotlighting, paraphrasing, self-reflection) help but fail against adaptive attacks. Adversarial fine-tuning showed more promise. PDF parsing libraries may expose metadata injection vectors. |
| **2.1.4** | **Verify that** input length controls account for context window limits and that the system prevents user-supplied content from exceeding a proportion of the total context window that would displace system instructions or safety directives from the model's effective attention. | 1 | D/V | Context window hijacking; system prompt displacement; attention dilution attacks where large user inputs push safety instructions out of the model's effective context (Liu et al., 2023 "Lost in the Middle"). | 1. Review token counting logic — must use the correct tokenizer for the target model. 2. Verify a maximum user input length is enforced (e.g., user content limited to 60-80% of total context). 3. Test with maximum-length inputs and confirm system instructions remain effective. 4. Check that system instructions are positioned at beginning and end of context (sandwich defense). 5. Measure instruction adherence as input length increases. | "Effective attention" is model-dependent. Lost-in-the-middle research shows models attend less to mid-context content. The sandwich defense (system instructions before and after user content) partially mitigates this. Token counting must match the model's tokenizer exactly. Context window sizes are increasing rapidly (1M+ tokens), making this control harder to enforce as users expect to process larger inputs. |

---

## Recent Defensive Advances (2025-2026)

### Detection Tools

| Tool | Type | Performance | Notes |
|------|------|-------------|-------|
| [Meta Prompt Guard 2](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) | Classifier (86M params) | AUC .998, 81.2% APR on AgentDojo | Bypassed via non-English and leetspeak; energy-based loss reduces FP |
| [Meta LlamaFirewall](https://meta-llama.github.io/PurpleLlama/LlamaFirewall/) | Framework (3 components) | >90% efficacy on AgentDojo | Includes PromptGuard 2 + Agent Alignment Checks + CodeShield; already bypassed by Trendyol Tech |
| [Lakera Guard](https://www.lakera.ai/lakera-guard) | Runtime API | 98%+ detection, <50ms, 100+ languages | Acquired by Check Point Sept 2025 |
| [Promptfoo](https://www.promptfoo.dev/docs/red-team/) | Red-team framework | CI/CD integration | Open-source; adversarial crafting + detection testing |
| [Garak](https://github.com/NVIDIA/garak) | Vuln scanner | Modular probe system | NVIDIA; prompt injection detection module |

### Architectural Defenses

| Defense | Approach | Effectiveness |
|---------|----------|---------------|
| **CaMeL** (Google Research, 2025) | Separates control/data flow; untrusted data cannot impact program execution | 77% task completion with provable security on AgentDojo |
| **Spotlighting / XML tagging** | Explicit demarcation of trusted vs. untrusted content boundaries | Reduces indirect injection success; not proof against adaptive attacks |
| **Sandwich defense** | System instructions before and after user content | Mitigates lost-in-the-middle attention degradation |
| **Adversarial fine-tuning** | Fine-tune model against adversarial examples | Google DeepMind: improves robustness without degrading capabilities |
| **StruQ** (Structured Query) | Research-backed prompt structuring to separate instructions from data | Reduces attack surface; complements detection |

---

## Notable Incidents & Research (2025-2026)

| Date | Incident / Paper | Impact | Link |
|------|------------------|--------|------|
| Apr 2025 | Policy Puppetry (HiddenLayer) | Universal bypass across all major frontier models using role-play + policy formatting | https://hiddenlayer.com/innovation-hub/novel-universal-bypass-for-all-major-llms |
| May 2025 | GitHub MCP data heist (Invariant) | Attackers embedded commands in public Issues; AI agents exfiltrated private repo code and keys | https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/ |
| May 2025 | Google DeepMind indirect injection defenses | Adversarial fine-tuning > in-context defenses; adaptive evaluation is critical | arXiv:2505.14534 |
| May 2025 | CaMeL framework (Google Research) | Provable security via control/data flow separation; 77% task completion on AgentDojo | arXiv:2503.18813 |
| Aug 2025 | Perplexity Comet browser vulnerability | Hidden Reddit comments triggered command execution during summarization | — |
| 2025 | Crescendo multi-turn attack (USENIX Security) | 98% success on GPT-4, 100% on Gemini-Pro; defeats per-request inspection | arXiv:2404.01833 |
| Jan 2026 | CHAI physical prompt injection (UC Santa Cruz) | Physical-environment injection targeting embodied AI systems | — |

---

## Red-Teaming Statistics (Mindgard, 2025-2026)

- Prompt injection found in **70%** of security audits
- Role-play attacks: **89.6%** success rate
- Multi-turn jailbreaks: **97%** success within 5 turns
- Healthcare LLM adversarial objectives: **94.4%** completion rate
- Automated red teaming found **37% more** unique issues than manual
- Only **26%** of organizations conduct proactive AI security testing
- Single prompt injection loss exceeds **$100,000** (source: [Mindgard](https://mindgard.ai/blog/ai-red-teaming-statistics))

---

## MCP-Specific Attack Vectors

Tool-use and MCP prompt injection is the fastest-growing threat surface as of 2026:

- **Tool Poisoning**: Malicious instructions embedded in MCP tool descriptions (measured by MCPTox benchmark)
- **Tool Shadowing**: Attacker tool named identically to legitimate tool with crafted descriptions that match LLM intent better
- **Namespace Collision**: Multiple concurrent MCP servers create call interception opportunities
- **Parasitic Toolchain Attacks**: Chained infected tools escalate impact through interlinked tool networks

See also: [C10.4 Schema & Message Validation](C10-04-Schema-Message-Validation.md)

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

---

## Open Research Questions

- Can instruction hierarchy be formally guaranteed at the model level, or will it always be a probabilistic defense? CaMeL suggests the answer is architectural, not model-level.
- What is the optimal ratio of system instruction tokens to user content tokens for maintaining instruction adherence across different model families?
- How should prompt injection detection evolve to handle multi-turn conversational attacks (crescendo), given 97% success within 5 turns?
- Is there a reliable cross-provider benchmark beyond AgentDojo for measuring prompt injection defense effectiveness?
- How do MCP ecosystems change the attack surface for indirect prompt injection — is tool description validation sufficient?
- Can adversarial fine-tuning scale to defend against the long tail of creative injection techniques without capability degradation?
- How should physical-environment prompt injection (CHAI) be addressed for embodied AI systems?

---

[C02 Index](C02-User-Input-Validation.md) | [README](README.md)
