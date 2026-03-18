# C2.1 Prompt Injection Defense

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation)

## Purpose

Prompt injection is consistently ranked as the top risk for LLM-based systems (OWASP LLM Top 10 LLM01). Attacks range from direct injection (user crafts input to override system instructions) to indirect injection (malicious instructions embedded in retrieved documents, tool outputs, or third-party content). This section requires layered defenses: detection filters, instruction hierarchy enforcement, input sanitization, and context window management. No single technique is sufficient; defense-in-depth is the only viable strategy given that prompt injection remains an unsolved problem at the model level.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.1.1** | **Verify that** any external or derived input that may steer behavior, including user prompts, RAG results, tool integration or MCP outputs, agent to agent messages, API or webhook responses, configuration or policy files, memory reads and memory writes, is treated as untrusted, made inert by quoting or tagging and active content removal, and screened by a maintained prompt injection detection ruleset or service before concatenation into prompts or execution of actions. | 1 | D/V | Direct and indirect prompt injection; instruction override via any untrusted input channel including RAG poisoning, tool output manipulation, and memory injection. | 1. Review architecture diagrams for all input surfaces and confirm each is classified as untrusted. 2. Inspect prompt assembly code for delimiter/tagging of untrusted content (e.g., XML tags, triple-backtick quoting). 3. Confirm a prompt injection detection service (e.g., Lakera Guard, Prompt Guard, Rebuff, LLM Guard) is invoked before prompt concatenation. 4. Red-team with known injection payloads across all input channels (user, RAG, tool, MCP, memory). | This is intentionally broad -- it enumerates every untrusted input surface. Verification requires mapping all input flows, not just the user prompt endpoint. Indirect injection via RAG and tool outputs is often missed. Detection services have known bypass rates (typically 10-30% for novel payloads). |
| **2.1.2** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after processing user instructions. | 1 | D/V | Privilege escalation via prompt injection; system prompt override; jailbreaking by redefining model behavior through user input. | 1. Inspect prompt templates to confirm system/developer instructions are in the system message role. 2. Test with adversarial prompts that attempt to override system instructions ("ignore previous instructions", "you are now..."). 3. Verify the model API is called with proper role separation (system vs. user vs. assistant). 4. For APIs that support instruction hierarchy (e.g., Anthropic's system prompt), confirm it is used. | Instruction hierarchy enforcement depends heavily on the model provider. OpenAI's system message and Anthropic's system prompt provide some hierarchy, but no model guarantees perfect enforcement. This is a best-effort defense layer. Research by Perez & Ribeiro (2022) and others shows hierarchy can be bypassed with sufficiently creative attacks. |
| **2.1.3** | **Verify that** prompts originating from third-party content (web pages, PDFs, emails) are sanitized in isolation (for example, stripping instruction-like directives and neutralizing HTML, Markdown, and script content) before being concatenated into the main prompt. | 2 | D | Indirect prompt injection via retrieved or ingested content; cross-site prompt injection; document-based injection (e.g., hidden instructions in PDFs or HTML comments). | 1. Identify all third-party content ingestion paths (web scraping, document parsing, email processing, RSS feeds). 2. Review sanitization logic: confirm HTML/Markdown stripping, removal of instruction-like patterns, and isolation of content from system instructions. 3. Test with crafted documents containing hidden injection payloads (HTML comments, invisible text in PDFs, metadata fields). 4. Verify sanitization happens before concatenation, not after. | Sanitization is necessary but not sufficient -- there is no reliable way to strip "instruction-like directives" from natural language without also stripping legitimate content. This control reduces attack surface but cannot eliminate indirect injection. Tools like Defang or custom regex pipelines can help. PDF parsing libraries (PyMuPDF, pdfplumber) may expose metadata fields that contain injections. |
| **2.1.4** | **Verify that** input length controls account for context window limits and that the system prevents user-supplied content from exceeding a proportion of the total context window that would displace system instructions or safety directives from the model's effective attention. | 1 | D/V | Context window hijacking; system prompt displacement; attention dilution attacks where large user inputs push safety instructions out of the model's effective context. | 1. Review token counting logic and confirm it accounts for system prompt + user input + expected output tokens. 2. Verify a maximum user input length is enforced (e.g., user content limited to 60-80% of total context). 3. Test with maximum-length inputs and confirm system instructions remain effective. 4. Check that system instructions are positioned to maximize attention (typically at the beginning and end of context). | The "effective attention" concept is model-dependent. Research on lost-in-the-middle (Liu et al., 2023) shows models attend less to content in the middle of long contexts. Simply enforcing a length limit is not enough -- placement of system instructions matters. Token counting must use the correct tokenizer for the target model. |

---

## Related Standards & References

- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [Mitigate jailbreaks and prompt injections (Anthropic)](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
- [MITRE ATLAS AML.T0051: LLM Prompt Injection](https://atlas.mitre.org/techniques/AML.T0051)
- [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection (Greshake et al., 2023)](https://arxiv.org/abs/2302.12173)
- [Ignore This Title and HackAPrompt: Exposing Systemic Weaknesses of LLMs (Schulhoff et al., 2023)](https://arxiv.org/abs/2311.16119)
- [Lost in the Middle: How Language Models Use Long Contexts (Liu et al., 2023)](https://arxiv.org/abs/2307.03172)

---

## Open Research Questions

- Can instruction hierarchy be formally guaranteed at the model level, or will it always be a probabilistic defense?
- What is the optimal ratio of system instruction tokens to user content tokens for maintaining instruction adherence?
- How should prompt injection detection evolve to handle multi-turn conversational attacks (crescendo attacks)?
- Is there a reliable benchmark for measuring prompt injection detection effectiveness across providers (beyond ad-hoc red-teaming)?
- How do multi-agent architectures change the attack surface for indirect prompt injection, and what new defenses are needed?

---
