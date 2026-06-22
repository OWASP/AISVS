# C2 Input Validation

## Control Objective

This chapter addresses validation of all inputs as a first-line defense against some of the most damaging attacks on AI systems. Prompt injection can override system instructions, leak sensitive data, or steer a model toward disallowed behavior, and without dedicated filtering, jailbreaks continue to exploit the context window. In agentic and multi-step systems, input from tools, retrieved documents, MCP server responses, and sub-agent outputs carries the same risks as direct user input and must pass through the same validation pipeline. It covers prompt injection defenses and AI-specific content and policy screening, including multi-modal attack vectors such as adversarial perturbations, steganographic payloads, and cross-modal attacks.

---

## C2.1 Prompt Injection Defenses

This section covers defenses against prompt injection, one of the top risks for AI systems. These defenses require a combination of pattern filters, data classifiers, and instruction hierarchy enforcement.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.1.1** | **Verify that** input normalization is applied before tokenization or embedding. | 1 |
| **2.1.2** | **Verify that** encoding and representation smuggling in inputs is detected and mitigated. Approved mitigations include canonicalization, strict schema validation, policy-based rejection, or explicit marking. | 1 |
| **2.1.3** | **Verify that** all inputs that could steer model behavior are treated as untrusted and screened by a prompt injection detection ruleset or classifier, with flagged inputs blocked. | 1 |
| **2.1.4** | **Verify that** input length controls prevent content from exceeding the context window. The controls must reject inputs that exceed token limits rather than truncating them. | 1 |
| **2.1.5** | **Verify that** the system implements a character set restriction for all inputs. The restriction must use an allow-list approach that permits only characters that are explicitly required. | 1 |
| **2.1.6** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after user instructions have been processed. | 2 |
| **2.1.7** | **Verify that** reserved special tokens are encoded as literal characters and cannot be injected into the model context. | 2 |
| **2.1.8** | **Verify that** the system can detect many-shot jailbreaking patterns. | 3 |

---

## C2.2 Content & Policy Screening

This section covers input-side content screening. Syntactically valid prompts may request disallowed content such as instructions that violate policies, harmful content, or restricted material, and content screening prevents such prompts from reaching the model.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.2.1** | **Verify that** every prompt is scored by a content classifier for violence, self-harm, hate, and sexual content against configurable thresholds. Prompts that exceed those thresholds are rejected or sanitized before reaching the model context. | 1 |
| **2.2.2** | **Verify that** prompt content classification is evaluated for unsupported languages. | 1 |
| **2.2.3** | **Verify that** non-text inputs (image/video/audio) are checked for adversarial perturbations, steganographic payloads, hidden or embedded content, or known attack patterns. | 2 |
| **2.2.4** | **Verify that** coordinated attacks spanning multiple input types (e.g., steganographic payloads in images combined with prompt injection in text) are detected and blocked. | 3 |

---

## References

* [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
* [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
* [MITRE ATLAS: Adversarial Input Detection](https://atlas.mitre.org/mitigations/AML.M0015)
* [MITRE ATLAS: LLM Prompt Injection (AML.T0051)](https://atlas.mitre.org/techniques/AML.T0051)
