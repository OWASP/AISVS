# C7.1 Output Format Enforcement

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Output format enforcement ensures that model-generated content conforms to expected structures before it reaches downstream systems. Treating model output as untrusted input is the single most important principle in this section. Without strict schema validation and safe handling, model outputs can introduce injection vulnerabilities (XSS, SQLi, command injection), cause deserialization attacks, or corrupt data pipelines. These controls apply the same defense-in-depth approach used for any untrusted data source.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.1.1** | **Verify that** the application validates all model outputs against a strict schema (like JSON Schema) and rejects any output that does not match. | 1 | D/V | **Injection via malformed output.** Without schema validation, a model could emit output containing embedded scripts, SQL fragments, or malformed structures that downstream parsers execute or misinterpret. | Provide adversarial prompts designed to produce malformed output (e.g., JSON with extra fields, nested scripts). Confirm the application rejects non-conforming responses and does not pass them downstream. Test with JSON Schema validators or equivalent for the output format in use. | Most LLM providers now offer JSON mode or structured output modes (OpenAI, Anthropic, Google). Constrained decoding libraries (Outlines, Guidance, LMQL) can enforce grammar-level conformance at generation time, reducing post-hoc rejection rates. High-performance engines like XGrammar and Microsoft's llguidance (Rust-based) achieve near-zero overhead constrained decoding (~50 microseconds CPU per token for 128K-token vocabulary), making production-scale enforcement practical. Gartner predicts 95% of enterprise LLM deployments will use constrained decoding by 2027. |
| **7.1.2** | **Verify that** the system uses "stop sequences" or token limits to strictly cut off generation before it can overflow buffers or execute unintended commands. | 1 | D/V | **Buffer overflow / runaway generation.** Unbounded generation can exhaust memory, produce excessively long outputs that overwhelm downstream systems, or continue generating past intended boundaries into unsafe territory. | Review API call configurations for max_tokens and stop sequences. Test by prompting the model to generate extremely long outputs and confirm truncation occurs. Verify that truncated outputs are handled gracefully (not parsed as incomplete structures). | All major inference APIs support max_tokens and stop sequences. The risk is not missing tooling but misconfiguration — teams must set appropriate limits per use case rather than relying on defaults. |
| **7.1.3** | **Verify that** components processing model output treat it as untrusted input (e.g., using parameterized queries or safe de-serializers). | 1 | D/V | **Second-order injection.** If model output is interpolated into SQL queries, shell commands, HTML templates, or deserialized without sanitization, an attacker who controls model output (via prompt injection) can achieve code execution, data exfiltration, or XSS. This is particularly dangerous in text-to-SQL systems where natural language is converted to database queries — traditional WAFs fail to detect these attacks because the injection payload is generated after user input, not embedded in it. | Code review all locations where model output is consumed. Confirm parameterized queries for database interactions, context-appropriate output encoding for HTML/JS (using DOMPurify or equivalent), Content Security Policy (CSP) headers for browser-rendered output, and safe deserialization (e.g., `json.loads` not `eval`, no `pickle` on model output). Fuzz model outputs with injection payloads. For text-to-SQL systems, verify the application defines query templates with parameterized placeholders and only uses LLM output to fill data values, never query structure. | This is the most critical control in C7.1. It directly maps to OWASP LLM05:2025 (Improper Output Handling). Many real-world vulnerabilities arise from treating model output as trusted program input. Research in 2025 demonstrated backdoor attacks on text-to-SQL models through poisoned fine-tuning datasets, making parameterized query patterns essential even when the model itself is considered trusted. |
| **7.1.4** | **Verify that** the system logs the specific error type when an output is rejected for bad formatting. | 2 | D/V | **Blind failure / missed attack signals.** Without logging, schema validation failures are invisible. Repeated formatting failures may indicate an ongoing prompt injection attack or a model degradation issue that goes undetected. | Trigger schema validation failures and confirm log entries include: error type (schema violation, token limit hit, etc.), timestamp, request identifier, and the nature of the violation. Confirm no sensitive user data is logged. | Logging rejected outputs supports both security monitoring (detecting injection attempts) and operational monitoring (detecting model drift or degraded output quality). Feed these logs into C7.6 monitoring integration. |

---

## Implementation Guidance

### Constrained Decoding vs. Post-hoc Validation

There are two complementary strategies for enforcing output format, and production systems should use both:

**Constrained decoding** inserts a logit processor between the model's raw output logits and the sampling step. The processor tracks the current position within a target grammar (JSON Schema, regex, or CFG) and masks out tokens that would violate the grammar. This guarantees syntactic conformance at generation time.

- **XGrammar** splits vocabulary tokens into context-independent tokens (~99% of vocabulary, precomputed into bitmask tables) and context-dependent tokens (~1% requiring runtime stack inspection), achieving up to 100x speedup over earlier grammar-constrained methods.
- **Microsoft llguidance** uses a derivative-based regex engine and optimized Earley parser for CFG rules, running in Rust with ~50 microseconds CPU time per token.
- **Outlines** (dottxt) and **LMQL** provide Python-native constrained decoding for open-weight models.
- **Provider-side structured output**: OpenAI Structured Outputs, Anthropic tool-use schemas, and Google Gemini JSON mode all offer API-level format enforcement.

**Post-hoc validation** applies schema checks after generation completes. This catches semantic issues that grammar-level enforcement cannot (e.g., a field is valid JSON but contains a script payload in a string value). Tools include:

- **Guardrails AI** — open-source framework with a hub of pre-built validators for output format, content safety, PII detection, and custom rules. Supports Python and JavaScript.
- **NVIDIA NeMo Guardrails** — programmable rails using Colang (a domain-specific language) for defining conversational safety policies. Complements Guardrails AI's validation approach with state-machine-based flow control.
- **Instructor** — lightweight library (Python/TypeScript) that wraps LLM API calls with Pydantic model validation, automatic retries on schema violations, and structured extraction patterns.

Both layers together provide defense-in-depth: constrained decoding prevents malformed structure, and post-hoc validation catches dangerous content within well-formed output.

### Output Injection Attack Patterns

LLM output can serve as an injection vector in any downstream execution context. Key patterns to defend against:

| Attack Pattern | Mechanism | Defense |
|---------------|-----------|---------|
| **XSS via LLM output** | Model generates `<script>` tags or event handlers in output rendered as HTML | Context-appropriate output encoding, DOMPurify, CSP headers |
| **SQL injection via text-to-SQL** | Natural language translated to SQL by LLM; malicious prompt causes query manipulation | Parameterized query templates; LLM fills only data values, never query structure |
| **Command injection** | LLM output interpolated into shell commands via `exec`, `eval`, or `os.system` | Never pass LLM output to shell interpreters; use structured API calls instead |
| **SSRF via LLM output** | Model generates URLs that are fetched server-side without validation | URL allowlisting; validate scheme, host, and port before any server-side fetch |
| **Path traversal** | LLM-generated file paths contain `../` sequences | Canonicalize paths; validate against allowed directory prefixes |
| **Deserialization attacks** | LLM output passed to unsafe deserializers (`pickle`, `eval`, `yaml.load`) | Use safe parsers only (`json.loads`, `yaml.safe_load`); never deserialize LLM output with code-execution-capable formats |

Traditional WAFs often miss these attacks because the injection payload originates from the model's generation, not from raw user input. Defense must be applied at the point where LLM output enters a downstream system.

### Streaming Output Validation

When using streaming responses (SSE/WebSocket), full schema validation cannot be applied until generation completes. Recommended approaches:

1. **Buffer and validate**: Accumulate streamed tokens, validate the complete output before forwarding to downstream systems. Display partial output to users but gate any programmatic consumption on full validation.
2. **Incremental parsing**: Use incremental JSON parsers that can detect structural violations mid-stream and abort generation early.
3. **Constrained decoding**: When available, constrained decoding at the inference layer eliminates the need for post-hoc streaming validation since every emitted token is guaranteed to be grammar-conformant.

---

## Related Standards & References

- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/) — directly addresses treating model output as untrusted
- [OWASP Output Encoding Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Output_Encoding_Cheat_Sheet.html) — context-appropriate encoding for model output rendered in web UIs
- [JSON Schema Specification](https://json-schema.org/) — for defining and validating structured model output
- [Outlines (dottxt)](https://github.com/dottxt-ai/outlines) — constrained decoding for structured output generation
- [Guidance (Microsoft)](https://github.com/guidance-ai/guidance) — template-based constrained generation with llguidance engine
- [XGrammar](https://github.com/mlc-ai/xgrammar) — high-performance grammar-constrained decoding engine (up to 100x speedup)
- [Guardrails AI](https://www.guardrailsai.com/) — open-source output validation framework with pre-built validator hub
- [NVIDIA NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) — programmable safety rails for LLM-based conversational systems
- [Instructor](https://github.com/jxnl/instructor) — structured LLM output extraction with Pydantic validation and automatic retries
- [PortSwigger: Web LLM Attacks](https://portswigger.net/web-security/llm-attacks) — practical attack patterns for LLM-integrated web applications
- [Keysight: Database Query-Based Prompt Injection](https://www.keysight.com/blogs/en/tech/nwvs/2025/07/31/db-query-based-prompt-injection) — prompt injection leading to SQL injection in text-to-SQL systems
- [Arxiv: SQL Injection via Backdoor Attacks on Text-to-SQL Models (2025)](https://arxiv.org/html/2503.05445v1) — backdoor attack frameworks targeting LLM-based text-to-SQL
- [JSONSchemaBench](https://openreview.net/forum?id=FKOaJqKoio) — benchmark for evaluating constrained decoding engines on JSON Schema compliance

---

## Open Research Questions

- How should applications handle partial schema conformance (e.g., output is valid JSON but missing optional fields)? Should this be a hard reject or a soft warning?
- What is the performance impact of constrained decoding vs. post-hoc validation, and when is each approach preferable? Early benchmarks (XGrammar, llguidance) show near-zero overhead, but real-world latency impact across diverse schemas needs further study.
- How should streaming outputs be validated when the full schema cannot be checked until generation is complete? Incremental parsing and buffered validation are emerging but not yet standardized.
- Can constrained decoding prevent semantic injection (e.g., a valid JSON string field containing a script payload)? Grammar-level enforcement guarantees structure but not content safety — the gap between syntactic and semantic validation remains an open problem.
- How effective are backdoor attacks against fine-tuned text-to-SQL models, and what defenses beyond parameterized queries can mitigate model-level compromise?

---
