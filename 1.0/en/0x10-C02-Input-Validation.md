# C2 Input Validation

## Control Objective

Robust validation of all inputs serves as a first-line defense against some of the most damaging attacks on AI systems. Prompt injection attacks can override system instructions, leak sensitive data, or steer the model toward behavior that is not allowed. Unless dedicated filters and other validation are put in place, research indicates that jailbreaks will still be able to exploit context windows.

In agentic and multi-step systems, input from tools, retrieved documents, MCP server responses, and sub-agent outputs also require the same validation pipeline because they carry the same risks as direct user input. This chapter focuses on threats unique to AI systems: prompt injection, adversarial inputs targeting model behavior, AI-specific content screening, and multi-modal attack vectors including adversarial perturbations, steganographic payloads, and cross-modal attacks.

---

## C2.1 Prompt Injection Defenses

Prompt injection is one of the top risks for AI systems. Defenses against this tactic require a combination of pattern filters, data classifiers and instruction hierarchy enforcement.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.1.1** | **Verify that** input normalization is applied before tokenization or embedding. | 1 |
| **2.1.2** | **Verify that** encoding and representation smuggling in inputs is detected and mitigated. Approved mitigations include canonicalization, strict schema validation, policy-based rejection, or explicit marking. | 1 |
| **2.1.3** | **Verify that** all inputs that could steer model behavior are treated as untrusted and screened by a prompt injection detection ruleset or classifier and blocked. | 1 |
| **2.1.4** | **Verify that** input length controls prevent content from exceeding the context window. The controls must reject inputs that exceed token limits rather than truncating them. | 1 |
| **2.1.5** | **Verify that** the system implements a character set limitation for all inputs. The limitation must use an allow-list approach which only permits characters that are explicitly required. | 1 |
| **2.1.6** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after user instructions have been processed. | 2 |
| **2.1.7** | **Verify that** the system can detect many-shot jailbreaking patterns. | 3 |

## C2.2 Content & Policy Screening

Syntactically valid prompts may request disallowed content such as instructions that violate policies, harmful content, or restricted material. Input-side content screening prevents such prompts from reaching the model.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.2.1** | **Verify that** every prompt is scored by a content classifier for violence, self-harm, hate, and sexual content against configurable thresholds. Prompts that exceed those thresholds are rejected or sanitized before reaching model context. | 1 |
| **2.2.2** | **Verify that** prompt content classification is evaluated for languages that are not supported. | 1 |
| **2.2.3** | **Verify that** screening logs include classifier confidence scores and policy category tags with applied stage and trace metadata. | 2 |
| **2.2.4** | **Verify that** non-text inputs (image/video/audio) are checked for adversarial perturbations, steganographic payloads, hidden or embedded content, or known attack patterns. | 2 |
| **2.2.5** | **Verify that** coordinated attacks spanning multiple input types (e.g., steganographic payloads in images combined with prompt injection in text) are detected and blocked. | 3 |

---

## References

* [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
* [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
* [MITRE ATLAS: Adversarial Input Detection](https://atlas.mitre.org/mitigations/AML.M0015)
* [Mitigate jailbreaks and prompt injections](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
