# C7.1 Output Format Enforcement

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Output format enforcement ensures that model-generated content conforms to expected structures before it reaches downstream systems. Treating model output as untrusted input is the single most important principle in this section. Without strict schema validation and safe handling, model outputs can introduce injection vulnerabilities (XSS, SQLi, command injection), cause deserialization attacks, or corrupt data pipelines. These controls apply the same defense-in-depth approach used for any untrusted data source.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.1.1** | **Verify that** the application validates all model outputs against a strict schema (like JSON Schema) and rejects any output that does not match. | 1 | D/V | **Injection via malformed output.** Without schema validation, a model could emit output containing embedded scripts, SQL fragments, or malformed structures that downstream parsers execute or misinterpret. | Provide adversarial prompts designed to produce malformed output (e.g., JSON with extra fields, nested scripts). Confirm the application rejects non-conforming responses and does not pass them downstream. Test with JSON Schema validators or equivalent for the output format in use. | Most LLM providers now offer JSON mode or structured output modes (OpenAI, Anthropic, Google). Constrained decoding libraries (Outlines, Guidance, LMQL) can enforce grammar-level conformance at generation time, reducing post-hoc rejection rates. |
| **7.1.2** | **Verify that** the system uses "stop sequences" or token limits to strictly cut off generation before it can overflow buffers or execute unintended commands. | 1 | D/V | **Buffer overflow / runaway generation.** Unbounded generation can exhaust memory, produce excessively long outputs that overwhelm downstream systems, or continue generating past intended boundaries into unsafe territory. | Review API call configurations for max_tokens and stop sequences. Test by prompting the model to generate extremely long outputs and confirm truncation occurs. Verify that truncated outputs are handled gracefully (not parsed as incomplete structures). | All major inference APIs support max_tokens and stop sequences. The risk is not missing tooling but misconfiguration — teams must set appropriate limits per use case rather than relying on defaults. |
| **7.1.3** | **Verify that** components processing model output treat it as untrusted input (e.g., using parameterized queries or safe de-serializers). | 1 | D/V | **Second-order injection.** If model output is interpolated into SQL queries, shell commands, HTML templates, or deserialized without sanitization, an attacker who controls model output (via prompt injection) can achieve code execution, data exfiltration, or XSS. | Code review all locations where model output is consumed. Confirm parameterized queries for database interactions, context-appropriate output encoding for HTML/JS, and safe deserialization (e.g., `json.loads` not `eval`, no `pickle` on model output). Fuzz model outputs with injection payloads. | This is the most critical control in C7.1. It directly maps to OWASP LLM05:2025 (Improper Output Handling). Many real-world vulnerabilities arise from treating model output as trusted program input. |
| **7.1.4** | **Verify that** the system logs the specific error type when an output is rejected for bad formatting. | 2 | D/V | **Blind failure / missed attack signals.** Without logging, schema validation failures are invisible. Repeated formatting failures may indicate an ongoing prompt injection attack or a model degradation issue that goes undetected. | Trigger schema validation failures and confirm log entries include: error type (schema violation, token limit hit, etc.), timestamp, request identifier, and the nature of the violation. Confirm no sensitive user data is logged. | Logging rejected outputs supports both security monitoring (detecting injection attempts) and operational monitoring (detecting model drift or degraded output quality). Feed these logs into C7.6 monitoring integration. |

---

## Related Standards & References

- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/) — directly addresses treating model output as untrusted
- [OWASP Output Encoding Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Output_Encoding_Cheat_Sheet.html) — context-appropriate encoding for model output rendered in web UIs
- [JSON Schema Specification](https://json-schema.org/) — for defining and validating structured model output
- [Outlines (dottxt)](https://github.com/dottxt-ai/outlines) — constrained decoding for structured output generation
- [Guidance (Microsoft)](https://github.com/guidance-ai/guidance) — template-based constrained generation

---

## Open Research Questions

- How should applications handle partial schema conformance (e.g., output is valid JSON but missing optional fields)? Should this be a hard reject or a soft warning?
- What is the performance impact of constrained decoding vs. post-hoc validation, and when is each approach preferable?
- How should streaming outputs be validated when the full schema cannot be checked until generation is complete?

---
