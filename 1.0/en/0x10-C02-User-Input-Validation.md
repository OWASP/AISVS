# C2 User Input Validation

## Control Objective

Robust validation of user input is a first-line defense against some of the most damaging attacks on AI systems. Prompt injection attacks can override system instructions, leak sensitive data, or steer the model toward behavior that is not allowed. Unless dedicated filters and other validation is in place, research shows that jailbreaks that exploit context windows will continue to be effective.

> **Scope note:** This chapter covers AI-specific input validation concerns that go beyond general application input validation. Standard input validation (schema enforcement, type checking, character allow-listing, rate limiting, file upload validation, server-side enforcement, logging of validation failures) is addressed by OWASP ASVS v5 chapters V1, V2, V4, V5, and V16, and should be implemented as a baseline. This chapter focuses on threats unique to AI systems: prompt injection, adversarial inputs targeting model behavior, AI-specific content screening, and multi-modal attack vectors.

---

## C2.1 Prompt Injection Defense

Prompt injection is one of the top risks for AI systems. Defenses against this tactic employ a combination of pattern filters, data classifiers and instruction hierarchy enforcement.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.1.1** | **Verify that** all external or derived inputs that may steer model behavior are treated as untrusted and screened by a prompt injection detection ruleset or classifier before being included in prompts or used to trigger actions. | 1 |
| **2.1.2** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after processing user instructions. This enforcement must be preserved across multi-step interactions and tool-augmented workflows. In such cases, prompt composition or intermediate outputs must not allow user-controlled content to influence or override system or developer instructions. | 1 |
| **2.1.3** | **Verify that** input length controls prevent user-supplied content from exceeding a defined proportion of the context window, and that inputs exceeding token limits are rejected rather than silently truncated, ensuring system instructions and safety directives are not displaced from the model's effective attention. | 1 |
| **2.1.4** | **Verify that** prompts originating from third-party content (web pages, PDFs, emails) are sanitized in isolation (for example, stripping instruction-like directives and neutralizing HTML, Markdown, and script content) before being concatenated into the main prompt. | 2 |
| **2.1.5** | **Verify that** the system enforces per-request limits on the number of user-supplied demonstrations included in a single context window. | 2 |
| **2.1.6** | **Verify that** the system detects patterns indicative of systematic in-context behavioral override attempts consistent with many-shot jailbreaking. | 2 |
| **2.1.7** | **Verify that** detected in-context behavioral override attempts are classified and handled as prompt injection events. | 2 |
| **2.1.8** | **Verify that** prompt injection screening respects user-specific policies (age and regional legal constraints) via attribute-based rules resolved at request time, including the role or permission level of the calling agent. | 2 |
| **2.1.9** | **Verify that** the system implements a character set limitation for user inputs to model prompts, allowing only characters that are explicitly required for business purposes using an allow-list approach. | 1 |

---

## C2.2 Pre-Tokenization Input Normalization

AI models process text through tokenizers and embeddings that can be exploited via encoding tricks invisible to conventional input validation. Normalization before tokenization closes attack vectors such as homoglyph substitution, invisible character injection, and bidirectional text manipulation that bypass standard allow-list filters but alter model behavior.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.2.1** | **Verify that** input normalization (Unicode NFC canonicalization, homoglyph mapping, removal of control and invisible Unicode characters, and bidirectional text neutralization) is applied before tokenization or embedding, and that inputs which still contain suspicious encoding artifacts after normalization are rejected or flagged for review. | 1 |
| **2.2.2** | **Verify that** suspected adversarial inputs are quarantined and logged. | 1 |
| **2.2.3** | **Verify that** encoding and representation smuggling in both inputs and outputs (e.g., invisible Unicode/control characters, homoglyph swaps, or mixed-direction text) are detected and mitigated. Approved mitigations include canonicalization, strict schema validation, policy-based rejection, or explicit marking. | 3 |

---

## C2.3 Content & Policy Screening

Syntactically valid prompts may request disallowed content such as policy-violating instructions, harmful content, or restricted material. Input-side content screening prevents such prompts from reaching the model. For output-side content filtering, see C7.3.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.3.1** | **Verify that** a content classifier scores every inbound prompt for violence, self-harm, hate, sexual content and illegal requests, with configurable thresholds, before the prompt is included in model context. | 1 |
| **2.3.2** | **Verify that** inputs which violate policies are rejected so they do not propagate to downstream model or tool/MCP calls. | 1 |
| **2.3.3** | **Verify that** screening logs include classifier confidence scores and policy category tags with applied stage (pre-prompt or post-response) and trace metadata (source, tool or MCP server, agent ID, session) for SOC correlation and future red-team replay. | 3 |

---

## C2.4 Multi-Modal Input Validation

AI systems that accept non-textual inputs (images, audio, video, files) face unique attack vectors where malicious content can be embedded across modalities and extracted into text that feeds the model's context.

> **Scope note:** Standard file upload validation (type, size, format, malware scanning, path traversal prevention) is covered by OWASP ASVS v5 chapter V5 and should be implemented as a baseline. This section addresses AI-specific risks: extraction of text from non-text inputs feeding into prompts, adversarial perturbations targeting model perception, and coordinated cross-modal attacks.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.4.1** | **Verify that** text extracted from non-text inputs (e.g., image-to-text, speech-to-text) and hidden or embedded content (metadata, layers, alt text, comments) is treated as untrusted and screened per 2.1.1. | 1 |
| **2.4.2** | **Verify that** image/audio inputs are checked for adversarial perturbations, steganographic payloads, or known attack patterns, and detections trigger gating (block or degrade capabilities) before model use. | 2 |
| **2.4.3** | **Verify that** cross-modal attack detection identifies coordinated attacks spanning multiple input types (e.g., steganographic payloads in images combined with prompt injection in text) with correlation rules and alert generation, and that confirmed detections are blocked or require HITL (human-in-the-loop) approval. | 3 |

---

## References

* [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
* [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
* [MITRE ATLAS: Adversarial Input Detection](https://atlas.mitre.org/mitigations/AML.M00150)
* [Mitigate jailbreaks and prompt injections](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
