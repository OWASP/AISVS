# C2 User Input Validation

## Control Objective

Robust validation of user input is a first-line defense against some of the most damaging attacks on AI systems. Prompt injection attacks can override system instructions, leak sensitive data, or steer the model toward behavior that is not allowed. Unless dedicated filters and other validation is in place, research shows that jailbreaks that exploit context windows will continue to be effective.

---

## C2.1 Prompt Injection Defense

Prompt injection is one of the top risks for AI systems. Defenses against this tactic employ a combination of pattern filters, data classifiers and instruction hierarchy enforcement.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.1.1** | **Verify that** any external or derived input that may steer behavior, including user prompts, RAG results, plugin or MCP outputs, agent to agent messages, API or webhook responses, configuration or policy files, memory reads and memory writes, is treated as untrusted, made inert by quoting or tagging and active content removal, and screened by a maintained prompt injection detection ruleset or service before concatenation into prompts or execution of actions. | 1 |  D/V |
| **2.1.2** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after processing user instructions. | 1 |  D/V |
| **2.1.3** | **Verify that** prompts originating from third-party content (web pages, PDFs, emails) are sanitized in isolation (for example, stripping instruction-like directives and neutralizing HTML, Markdown, and script content) before being concatenated into the main prompt. | 2 | D |

---

## C2.2 Adversarial-Example Resistance

Natural Language Processing (NLP) models are still vulnerable to subtle character or word-level perturbations that humans often miss but models tend to misclassify.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.2.1** | **Verify that** basic input normalization steps (Unicode NFC, homoglyph mapping, whitespace trimming, removal of control and invisible Unicode characters) are run before tokenization or embedding and before parsing into tool or MCP arguments. | 1 | D |
| **2.2.2** | **Verify that** statistical anomaly detection flags inputs with unusually high edit distance to language norms or abnormal embedding distances and that flagged inputs are gated before concatenation into prompts or execution of actions. | 2 |  D/V |
| **2.2.3** | **Verify that** the inference pipeline supports adversarial-training–hardened model variants or defense layers (e.g., randomization, defensive distillation, alignment checks) for high-risk endpoints. | 2 | D |
| **2.2.4** | **Verify that** suspected adversarial inputs are quarantined, and logged with full payloads and trace metadata (source, tool or MCP server, agent ID, session).  | 2 | V |
| **2.2.5** | **Verify that** encoding and representation smuggling in both inputs and outputs (e.g., invisible Unicode/control characters, homoglyph swaps, or mixed-direction text) are detected and mitigated. Approved mitigations include canonicalization, strict schema validation, policy-based rejection, or explicit marking. | 2 | D/V |

---

## C2.3 Prompt Character Set

Restricting the character set of user inputs to only allow characters that are necessary for business requirements can help prevent various types of attacks.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.3.1** | **Verify that** the system implements a character set limitation for user inputs, allowing only characters that are explicitly required for business purposes. | 1 | D |
| **2.3.2** | **Verify that** an allow-list approach is used to define the permitted character set. | 1 | D |
| **2.3.3** | **Verify that** inputs containing characters outside of the allowed set are rejected and logged with trace metadata (source, tool or MCP server, agent ID, session). | 1 | D/V |

---

## C2.4 Schema, Type & Length Validation

AI attacks featuring malformed or oversized inputs can cause parsing errors, prompt spillage across fields, and resource exhaustion.  Strict schema enforcement is also a prerequisite when performing deterministic tool calls.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.4.1** | **Verify that** every API, tool or MCP endpoint defines an explicit input schema (JSON Schema, Protobuf or multimodal equivalent) rejects extra or unknown fields and implicit type coercion, and validates inputs server-side before prompt assembly or tool execution. | 1 | D |
| **2.4.2** | **Verify that** inputs exceeding maximum token or byte limits are rejected with a safe error and never silently truncated. | 1 |  D/V |
| **2.4.3** | **Verify that** type checks (e.g., numeric ranges, enum values, MIME types for images/audio) are enforced server-side including for tool or MCP arguments. | 2 |  D/V |
| **2.4.4** | **Verify that** semantic validators, that understand NLP input, run in constant time and avoid external network calls to prevent algorithmic DoS. | 2 | D |
| **2.4.5** | **Verify that** validation failures are logged with redacted payload snippets and unambiguous error codes and include trace metadata (source, tool or MCP server, agent ID, session) to aid security triage. | 3 | V |

---

## C2.5 Content & Policy Screening

Developers should be able to detect syntactically valid prompts that request disallowed content (such as illicit instructions, hate speech, and/or copyrighted text) then prevent them from propagating.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.5.1** | **Verify that** a content classifier (zero shot or fine tuned) scores every input and output for violence, self-harm, hate, sexual content and illegal requests, with configurable thresholds. | 1 | D |
| **2.5.2** | **Verify that** inputs which violate policies will be rejected so they will not propagate to downstream LLM or tool/MCP calls. | 1 |  D/V |
| **2.5.3** | **Verify that** screening respects user-specific policies (age, regional legal constraints) via attribute-based rules resolved at request time, including agent-role attributes.  | 2 | D |
| **2.5.4** | **Verify that** screening logs include classifier confidence scores and policy category tags with applied stage (pre-prompt or post-response) and trace metadata (source, tool or MCP server, agent ID, session) for SOC correlation and future red-team replay. | 3 | V |

---

## C2.6 Input Rate Limiting & Abuse Prevention

Developers should prevent abuse, resource exhaustion, and automated attacks against AI systems by limiting input rates and detecting anomalous usage patterns.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.6.1** | **Verify that** per-user, per-IP, per-API-key, and per-agent and per-session/task rate limits are enforced for all input and tool/MCP endpoints. | 1 | D/V |
| **2.6.2** | **Verify that** burst and sustained rate limits are tuned to prevent DoS and brute force attacks, and that per-task budgets (for example tokens, tool/MCP calls, and cost) are enforced for agent planning loops. | 2 | D/V |
| **2.6.3** | **Verify that** anomalous usage patterns (e.g., rapid-fire requests, input flooding, repetitive failing tool/MCP calls or recursive agent loops) trigger automated blocks or escalations. | 2 | D/V |
| **2.6.4** | **Verify that** abuse prevention logs are retained and reviewed for emerging attack patterns, with trace metadata (source, tool or MCP server, agent ID, session). | 3 | V |

---

## C2.7 Multi-Modal Input Validation

AI systems should include robust validation for non-textual inputs (images, audio, files) to prevent injection, evasion, or resource abuse.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.7.1** | **Verify that** all non-text inputs (images, audio, files) are validated for type, size, and format before processing, and that any extracted text (image-to-text or speech-to-text) and any hidden or embedded instructions (metadata, layers, alt text, comments) are treated as untrusted per 2.1.1. | 1 | D |
| **2.7.2** | **Verify that** files are scanned for malware and steganographic payloads before ingestion, and that any active content (like scripts or macros) is removed or the file is quarantined. | 2 | D/V |
| **2.7.3** | **Verify that** image/audio inputs are checked for adversarial perturbations or known attack patterns, and detections trigger gating (block or degrade capabilities) before model use. | 2 | D/V |
| **2.7.4** | **Verify that** multi-modal input validation failures are logged and trigger alerts for investigation, with trace metadata (source, tool or MCP server, agent ID, session). | 3 | V |
| **2.7.5** | **Verify that** cross-modal attack detection identifies coordinated attacks spanning multiple input types (e.g., steganographic payloads in images combined with prompt injection in text) with correlation rules and alert generation, and that confirmed detections are blocked or require HITL (human-in-the-loop) approval. | 2 | D/V |
| **2.7.6** | **Verify that** multi-modal validation failures trigger detailed logging including all input modalities, validation results and threat scores, and trace metadata (source, tool or MCP server, agent ID, session). | 3 | D/V |
---

## C2.8 Real-Time Adaptive Threat Detection

Developers should employ advanced threat detection systems for AI that adapt to new attack patterns and provide real-time protection with compiled pattern matching.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **2.8.1** | **Verify that** pattern matching (e.g., compiled regex) runs on all inputs and outputs (including tool/MCP surfaces) with minimal latency impact. | 1 | D/V |
| **2.8.3** | **Verify that** adaptive detection models adjust sensitivity based on recent attack activity and are updated with new patterns in real time, and trigger risk-adaptive responses (for example disable tools, shrink context, or require HITL approval). | 2 | D/V |
| **2.8.4** | **Verify that** detection accuracy is improved via contextual analysis of user history, source, and session behavior, including trace metadata (source, tool or MCP server, agent ID, session). | 3 | D/V |
| **2.8.5** | **Verify that** detection performance metrics (detection rate, false positive rate, processing latency) are continuously monitored and optimized, including time-to-block and stage (pre-prompt/post-response). | 3 | D/V |

## References

* [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
* [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
* [MITRE ATLAS : Adversarial Input Detection](https://atlas.mitre.org/mitigations/AML.M00150)
* [Mitigate jailbreaks and prompt injections](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
