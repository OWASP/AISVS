# C7.1 Output Format Enforcement

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Output format enforcement ensures that model-generated content conforms to expected structures before it reaches downstream systems. Treating model output as untrusted input is the single most important principle in this section. Without strict schema validation and safe handling, model outputs can introduce injection vulnerabilities (XSS, SQLi, command injection), cause deserialization attacks, or corrupt data pipelines. These controls apply the same defense-in-depth approach used for any untrusted data source.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.1.1** | **Verify that** the application validates all model outputs against a strict schema (like JSON Schema) and rejects any output that does not match. | 1 | D/V | **Injection via malformed output.** Without schema validation, a model could emit output containing embedded scripts, SQL fragments, or malformed structures that downstream parsers execute or misinterpret. | Provide adversarial prompts designed to produce malformed output (e.g., JSON with extra fields, nested scripts). Confirm the application rejects non-conforming responses and does not pass them downstream. Test with JSON Schema validators or equivalent for the output format in use. Use the OWASP AI Testing Guide (v1, November 2025) test cases for structured validation coverage. | Most LLM providers now offer JSON mode or structured output modes (OpenAI, Anthropic, Google). Constrained decoding libraries (Outlines, Guidance, LMQL) can enforce grammar-level conformance at generation time, reducing post-hoc rejection rates. High-performance engines like XGrammar and Microsoft's llguidance (Rust-based) achieve near-zero overhead constrained decoding (~50 microseconds CPU per token for 128K-token vocabulary), making production-scale enforcement practical. As of 2025, Pre3 (ACL 2025) uses deterministic pushdown automata to improve constrained decoding throughput by up to 36%, and "Thinking Before Constraining" (2026) proposes a unified decoding framework that lets models reason before structural constraints are applied — reducing semantic errors on complex schemas. |
| **7.1.2** | **Verify that** the system uses "stop sequences" or token limits to strictly cut off generation before it can overflow buffers or execute unintended commands. | 1 | D/V | **Buffer overflow / runaway generation.** Unbounded generation can exhaust memory, produce excessively long outputs that overwhelm downstream systems, or continue generating past intended boundaries into unsafe territory. | Review API call configurations for max_tokens and stop sequences. Test by prompting the model to generate extremely long outputs and confirm truncation occurs. Verify that truncated outputs are handled gracefully (not parsed as incomplete structures). | All major inference APIs support max_tokens and stop sequences. The risk is not missing tooling but misconfiguration — teams must set appropriate limits per use case rather than relying on defaults. |
| **7.1.3** | **Verify that** components processing model output treat it as untrusted input (e.g., using parameterized queries or safe de-serializers). | 1 | D/V | **Second-order injection.** If model output is interpolated into SQL queries, shell commands, HTML templates, or deserialized without sanitization, an attacker who controls model output (via prompt injection) can achieve code execution, data exfiltration, or XSS. This is particularly dangerous in text-to-SQL systems where natural language is converted to database queries — traditional WAFs fail to detect these attacks because the injection payload is generated after user input, not embedded in it. Real-world proof: CVE-2026-32626 (AnythingLLM, CVSS 9.6) demonstrated streaming-phase XSS escalating to RCE because the chat renderer used `dangerouslySetInnerHTML` without DOMPurify on streamed LLM output, while historical messages were correctly sanitized. CVE-2025-68664 (LangChain Core "LangGrinch", CVSS 9.3) showed how LLM-influenced dictionaries containing a reserved `lc` key were deserialized into arbitrary object instantiation, enabling secret extraction and code execution across hundreds of millions of LangChain installations. | Code review all locations where model output is consumed. Confirm parameterized queries for database interactions, context-appropriate output encoding for HTML/JS (using DOMPurify or equivalent), Content Security Policy (CSP) headers for browser-rendered output, and safe deserialization (e.g., `json.loads` not `eval`, no `pickle` on model output). Fuzz model outputs with injection payloads. For text-to-SQL systems, verify the application defines query templates with parameterized placeholders and only uses LLM output to fill data values, never query structure. Pay special attention to streaming vs. historical rendering paths — CVE-2026-32626 showed that sanitization applied only to saved messages but not to the streaming renderer creates an exploitable gap. | This is the most critical control in C7.1. It directly maps to OWASP LLM05:2025 (Improper Output Handling). The 2025–2026 CVE landscape demonstrates this is not theoretical: AnythingLLM's CVE-2026-32626 (XSS-to-RCE via streaming output, March 2026), LangChain Core's CVE-2025-68664 (serialization injection, December 2025), and CVE-2026-25802 (prompt injection to stored XSS in new-api) all stem from treating model output as trusted. NIST AI 600-1 (GenAI Profile) reinforces this with its TEVV (Test, Evaluate, Validate, Verify) requirements for output handling controls. |
| **7.1.4** | **Verify that** the system logs the specific error type when an output is rejected for bad formatting. | 2 | D/V | **Blind failure / missed attack signals.** Without logging, schema validation failures are invisible. Repeated formatting failures may indicate an ongoing prompt injection attack or a model degradation issue that goes undetected. | Trigger schema validation failures and confirm log entries include: error type (schema violation, token limit hit, etc.), timestamp, request identifier, and the nature of the violation. Confirm no sensitive user data is logged. | Logging rejected outputs supports both security monitoring (detecting injection attempts) and operational monitoring (detecting model drift or degraded output quality). Feed these logs into C7.6 monitoring integration. |

---

## Implementation Guidance

### Constrained Decoding vs. Post-hoc Validation

There are two complementary strategies for enforcing output format, and production systems should use both:

**Constrained decoding** inserts a logit processor between the model's raw output logits and the sampling step. The processor tracks the current position within a target grammar (JSON Schema, regex, or CFG) and masks out tokens that would violate the grammar. This guarantees syntactic conformance at generation time.

- **XGrammar** splits vocabulary tokens into context-independent tokens (~99% of vocabulary, precomputed into bitmask tables) and context-dependent tokens (~1% requiring runtime stack inspection), achieving up to 100x speedup over earlier grammar-constrained methods.
- **Microsoft llguidance** uses a derivative-based regex engine and optimized Earley parser for CFG rules, running in Rust with ~50 microseconds CPU time per token.
- **Pre3** (ACL 2025) uses deterministic pushdown automata with precomputed prefix-conditioned edges, improving time per output token by up to 40% and throughput by up to 36% over existing constrained decoding approaches.
- **Outlines** (dottxt) and **LMQL** provide Python-native constrained decoding for open-weight models.
- **Provider-side structured output**: OpenAI Structured Outputs (which credited llguidance as foundational work in May 2025), Anthropic tool-use schemas, and Google Gemini JSON mode all offer API-level format enforcement.

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
| **Serialization injection** | LLM-influenced data containing framework-reserved keys (e.g., LangChain's `lc` marker) triggers arbitrary object instantiation during deserialization | Sanitize LLM output before passing to any framework serialization layer; strip or escape reserved keys; pin framework versions |

Traditional WAFs often miss these attacks because the injection payload originates from the model's generation, not from raw user input. Defense must be applied at the point where LLM output enters a downstream system.

### Real-World Incident Case Studies

These incidents illustrate why output format enforcement is not optional:

**CVE-2026-32626 — AnythingLLM Streaming XSS to RCE (March 2026).** AnythingLLM Desktop v1.11.1 and earlier had a critical flaw (CVSS 9.6) in its streaming chat renderer. The `PromptReply` component used `dangerouslySetInnerHTML` without DOMPurify sanitization on streamed tokens, while the `HistoricalMessage` component correctly applied `DOMPurify.sanitize()`. An attacker could embed malicious payloads in RAG documents or control a malicious LLM endpoint; when the model generated output containing the payload, JavaScript executed in the Electron renderer context, escalating to full RCE on the host OS. This perfectly demonstrates why sanitization must be applied uniformly across all rendering paths — streaming and historical — not just on saved content.

**CVE-2025-68664 — LangChain Core "LangGrinch" (December 2025).** LangChain Core's `dumps()` and `dumpd()` functions failed to escape dictionaries containing the reserved `lc` key (CVSS 9.3). An attacker who influenced LLM output (e.g., via prompt injection populating `additional_kwargs` or `response_metadata`) could inject structures that were treated as legitimate LangChain objects during deserialization. This enabled secret extraction via `secrets_from_env`, arbitrary class instantiation across multiple LangChain provider packages, and code execution through Jinja2 template rendering in `PromptTemplate`. The vulnerability affected 12 common flows including event streaming, message history, and caching — impacting hundreds of millions of installations.

**CVE-2026-25802 — Prompt Injection to Stored XSS in new-api (2026).** Another example of LLM output being rendered in web UIs without sanitization, enabling persistent cross-site scripting through prompt injection payloads embedded in model responses.

### Streaming Output Validation

When using streaming responses (SSE/WebSocket), full schema validation cannot be applied until generation completes. CVE-2026-32626 demonstrated the real danger: AnythingLLM sanitized historical messages but not streaming tokens, creating an exploitable gap. Recommended approaches:

1. **Buffer and validate**: Accumulate streamed tokens, validate the complete output before forwarding to downstream systems. Display partial output to users but gate any programmatic consumption on full validation. Apply the same sanitization (DOMPurify, output encoding) to streaming renderers as to historical/saved content — never assume streaming output is safe because it will be "re-sanitized later."
2. **Incremental parsing**: Use incremental JSON parsers that can detect structural violations mid-stream and abort generation early. CRANE (2025) introduces reasoning-aware constrained generation that can validate semantic constraints incrementally during streaming.
3. **Constrained decoding**: When available, constrained decoding at the inference layer eliminates the need for post-hoc streaming validation since every emitted token is guaranteed to be grammar-conformant.
4. **Uniform sanitization paths**: As a design principle, ensure every code path that renders or processes LLM output — streaming, cached, historical, or real-time — uses the same sanitization pipeline. The streaming/historical renderer divergence in CVE-2026-32626 is a common anti-pattern.

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
- [CVE-2026-32626: AnythingLLM Streaming XSS to RCE](https://github.com/Mintplex-Labs/anything-llm/security/advisories/GHSA-rrmw-2j6x-4mf2) — streaming-phase output injection escalating to host-level RCE (CVSS 9.6)
- [CVE-2025-68664: LangGrinch LangChain Core Serialization Injection](https://cyata.ai/blog/langgrinch-langchain-core-cve-2025-68664/) — deserialization of LLM-influenced data enabling secret extraction and code execution (CVSS 9.3)
- [Pre3: Deterministic Pushdown Automata for Faster Structured LLM Generation](https://aclanthology.org/2025.acl-long.551/) — ACL 2025, up to 36% throughput improvement for constrained decoding
- [OWASP AI Testing Guide v1](https://owasp.org/www-project-ai-testing-guide/) — first comprehensive AI security testing standard (November 2025)
- [NIST AI 600-1: GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — generative AI risk management including output validation TEVV requirements
- [OWASP AI Exchange](https://owaspai.org/) — comprehensive AI security guidance including output handling controls (2026 edition)
- [Focused.io: LLM Output Sanitization](https://focused.io/lab/improper-ai-output-handling---owasp-llm05) — practical guidance on preventing XSS, SQLi, and RCE in AI-generated output

---

## Open Research Questions

- How should applications handle partial schema conformance (e.g., output is valid JSON but missing optional fields)? Should this be a hard reject or a soft warning?
- What is the performance impact of constrained decoding vs. post-hoc validation, and when is each approach preferable? Pre3 (ACL 2025) and llguidance show near-zero overhead, but the "Thinking Before Constraining" framework (2026) demonstrates that constrained decoding can degrade semantic correctness on reasoning-intensive tasks — suggesting the optimal strategy depends on task complexity, not just latency.
- How should streaming outputs be validated when the full schema cannot be checked until generation is complete? CVE-2026-32626 demonstrated real exploitation of the streaming/historical sanitization gap. Incremental parsing and buffered validation are emerging but not yet standardized.
- Can constrained decoding prevent semantic injection (e.g., a valid JSON string field containing a script payload)? Grammar-level enforcement guarantees structure but not content safety — the gap between syntactic and semantic validation remains an open problem. CRANE (2025) explores reasoning-aware constrained generation but is still experimental.
- How effective are backdoor attacks against fine-tuned text-to-SQL models, and what defenses beyond parameterized queries can mitigate model-level compromise?
- How should frameworks handle LLM output that contains reserved internal markers (like LangChain's `lc` key)? CVE-2025-68664 showed that framework-level serialization assumptions create novel attack surfaces when LLM output flows through framework internals. Should frameworks adopt namespace isolation for serialized objects?

---
