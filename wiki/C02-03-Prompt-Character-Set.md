# C2.3 Prompt Character Set

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation)

## Purpose

Restricting the character set of user inputs to only allow characters necessary for business requirements is a foundational input validation technique. In the AI context, this is particularly effective at blocking encoding-based evasion attacks, Unicode tricks, and control character injection. An allow-list approach ensures that only expected characters reach the model, reducing the attack surface for adversarial input manipulation. While simple in concept, character set restrictions must be carefully designed to avoid breaking legitimate multilingual or technical use cases.

Character-level filtering sits upstream of normalization (C2.2) and prompt injection defense (C2.1) in the input pipeline. By stripping dangerous characters before any other processing, the system eliminates entire categories of evasion — invisible Unicode tag smuggling, zero-width character injection, homoglyph substitution, and RTL override attacks — before they reach the tokenizer or safety classifiers. As of March 2026, research demonstrates that these character-level attacks achieve near-100% bypass rates against commercial guardrails when no pre-tokenization character filtering is in place.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.3.1** | **Verify that** the system implements a character set limitation for user inputs, allowing only characters that are explicitly required for business purposes using an allow-list approach. | 1 | D | **Unicode tag smuggling** (U+E0000–U+E007F): invisible characters that LLM tokenizers decode back into ASCII, enabling hidden prompt injection while UIs display nothing (AML.T0051.001). **Homoglyph substitution**: Cyrillic/Latin cross-script swaps (e.g., Cyrillic "а" U+0430 for Latin "a" U+0061) achieve 58.7% average bypass rate against safety filters. **Zero-width character injection** (U+200B, U+200C, U+200D, U+FEFF): fragments BPE tokenization, producing non-canonical token sequences that evade safety-trained patterns. **RTL/Bidi override** (U+202E): reverses text display while preserving raw byte order for LLM interpretation. **Emoji smuggling**: text embedded in emoji variation selectors achieved 100% evasion across multiple commercial guardrails including Protect AI and Azure Prompt Shield (Mindgard, April 2025). **Control character injection** (U+0000–U+001F): can cause log injection, parser confusion, and unexpected behavior in downstream tool calls. CWE-20 (Improper Input Validation), CWE-176 (Improper Handling of Unicode Encoding). | 1. Review the input validation code for character allow-list implementation using Unicode category-based filtering. Confirm the allow-list uses `unicodedata.category()` codes (Python), `Character.getType()` (Java), or ICU4J `UCharacter.getType()` to allow specific categories (L, N, P, Z as needed) and block Cc, Cf, Co, Cn, Cs. 2. Confirm the allow-list is defined per input field/endpoint (e.g., a name field allows Unicode letter categories; a numeric field allows digits and decimal points; a free-text field allows L+N+P+Zs but blocks Cf+Cc+Co). 3. **Explicitly test** the following attack vectors: (a) Unicode Tags block U+E0000–U+E007F — submit text with embedded tag characters and confirm rejection. (b) Zero-width characters U+200B/U+200C/U+200D/U+2060/U+FEFF — insert between words and confirm stripping or rejection. (c) Private Use Area U+E000–U+F8FF and Supplementary PUA U+F0000–U+10FFFD — confirm blocked. (d) Variation Selectors U+FE00–U+FE0F and U+E0100–U+E01EF — confirm blocked. (e) Control characters U+0000–U+001F and U+007F–U+009F. (f) Homoglyphs — submit mixed Cyrillic+Latin strings and confirm detection via confusable analysis (UTS #39 skeleton comparison). 4. Verify the allow-list is enforced **before** NFKC normalization and before any other processing (CWE-180: Validate Before Canonicalize is a risk, but for character stripping specifically, dangerous characters should be removed before normalization to prevent normalization from transforming blocked sequences into allowed ones). 5. Use red-team tools: **Garak** for automated character-level attack testing, **Promptfoo** ASCII smuggling plugin for Unicode tag injection testing. | **Defining the right allow-list is the core challenge.** For multilingual applications, restricting to ASCII breaks legitimate use. The Unicode Consortium's UTS #39 defines six restriction levels — from ASCII-Only to Unrestricted — that provide a principled framework for choosing the right level per input field. A pragmatic default: allow Unicode letter/number categories (L, N) plus explicitly needed punctuation (P), block control (Cc), format (Cf), surrogate (Cs), private use (Co), and unassigned (Cn). **Specific tools:** Python `confusable_homoglyphs` (v3.2.0) for homoglyph detection, `sanitext` for suspicious Unicode detection, **LLM Guard** `InvisibleText` scanner (Protect AI, pip install llm-guard) for AI-specific invisible character filtering. ICU4J v78.3 `SpoofChecker` for Java. ICU4X v2.0 for Rust/WASM. JavaScript ES2024 RegExp v-flag enables Unicode set operations for precise allow-lists. **Key caveat:** LLM Guard's InvisibleText scanner was shown bypassable by basic techniques as of 2025 (arXiv:2504.11168) — layered defense is mandatory, not optional. This requirement overlaps with C2.2.1 normalization but operates at a different layer (rejection vs. transformation). |
| **2.3.2** | **Verify that** inputs containing characters outside of the allowed set are rejected and logged with trace metadata (source, tool or MCP server, agent ID, session). | 1 | D/V | **Undetected evasion attempts**: without logging, character-based attacks leave no forensic trail, preventing pattern analysis and incident response. **Log injection via raw control characters**: logging rejected characters without hex-encoding can itself be an attack vector (CWE-117: Improper Output Neutralization for Logs). **Inability to tune allow-lists**: without rejection telemetry, teams cannot distinguish between attack attempts and legitimate users hitting false positives, leading to either overly permissive or overly restrictive allow-lists. **Blind spot for coordinated attacks**: character-based probing often precedes more sophisticated prompt injection — rejection logs correlated with session metadata can reveal reconnaissance patterns (relates to C13 Monitoring requirements). | 1. Submit inputs containing disallowed characters from each blocked category (Cf, Cc, Co, Tags block, zero-width) and confirm they are rejected with a safe, generic error message (e.g., "invalid input") that does **not** reveal which specific characters are blocked or the allow-list pattern. 2. Check structured logs (JSON format preferred) for the following fields on each rejection: (a) rejected characters hex-encoded (e.g., `U+E0041`, `U+200B`), (b) Unicode category of rejected characters, (c) input source identifier, (d) tool or MCP server name if applicable, (e) agent ID, (f) session ID, (g) timestamp (ISO 8601). 3. Verify rejection is **fail-closed**: the input must not be partially processed or forwarded with disallowed characters stripped — it must be rejected entirely and the rejection must occur before any prompt assembly or tool execution. 4. Confirm error responses do not leak allow-list details that would help an attacker iteratively probe for the exact boundary. 5. Test that rejection logs are written to a tamper-resistant log sink with appropriate retention (cross-reference C13.1 logging requirements). 6. Verify that high-volume rejection events from a single source trigger rate-limiting or alerting (cross-reference C2.6 rate limiting requirements). | **Log encoding is critical** — logging raw control characters can cause log injection (CWE-117), where an attacker crafts rejected input that, when logged, manipulates log entries. Always hex-encode or escape rejected characters in log output. **False positive monitoring**: overly restrictive allow-lists will generate high rejection volumes from legitimate users, particularly in multilingual deployments. Build dashboards that track rejection rates per input field, per user locale, and per character category. Spikes in rejections for letter categories (L) likely indicate a too-narrow allow-list; spikes in rejections for format characters (Cf) or tags likely indicate attack attempts. **Correlation value**: rejection metadata becomes significantly more valuable when correlated with other signals — a session that triggers character rejections followed by prompt injection attempts is a strong indicator of adversarial probing. Feed rejection events into SIEM/SOC workflows (C13.2). **Tooling gap**: as of March 2026, no off-the-shelf AI security tool automatically correlates character-rejection events with downstream prompt injection attempts. This correlation must be built into custom SIEM rules or detection pipelines. |

---

## Attack Techniques Deep Dive

### Unicode Tag Smuggling (U+E0000–U+E007F)

The most impactful character-level attack against LLMs, publicly documented by Riley Goodside in January 2024. ASCII characters are converted to invisible Unicode by adding offset 0xE0000 to their codepoints (e.g., 'A' at U+0041 becomes U+E0041). These tag characters render invisibly in UIs but LLM tokenizers split them back into tag prefixes and original characters, reconstructing the payload. The LLM interprets the hidden text while humans and monitoring systems see nothing.

**Detection:** Strip the entire Tags block (U+E0000–U+E007F). Cisco published a YARA rule for detection: byte pattern `{ F3 A0 [0-2] ?? }` with threshold >10 matches.

### Homoglyph Substitution

Cross-script character substitution exploits visual similarity between characters from different Unicode scripts. The Unicode Consortium maintains a confusables matrix (part of UTS #39) that maps visually similar characters. Two strings are "confusable" when they produce identical "skeletons" via the `skeleton()` function (NFD normalization → prototype mapping → removal of default-ignorable characters).

**Detection:** Use ICU4J `SpoofChecker` or Python `confusable_homoglyphs` to flag mixed-script strings. UTS #39 restriction levels provide a principled per-field policy.

### Zero-Width and Invisible Character Injection

Zero-width spaces (U+200B), joiners (U+200C, U+200D), word joiners (U+2060), and BOM/ZWNBSP (U+FEFF) fragment BPE tokenization without any visible effect. Safety training is performed against canonically-tokenized text, so when inputs produce non-canonical token sequences via invisible character insertion, safety-trained patterns do not activate, but the model's general language understanding still processes the semantic content.

### Adversarial Tokenization

Research by Geh, Shao, and Van den Broeck (ACL 2025, arXiv:2503.02174) demonstrated that BPE tokenizers have exponentially many valid ways to segment any given string. Simply changing token boundaries — without modifying the text itself — can bypass safety alignment. This is "competitive against existing state-of-the-art adversarial approaches." Character set restrictions reduce the input alphabet, limiting the tokenizer's segmentation options and constraining this attack surface.

### Emoji Smuggling via Variation Selectors

Variation Selectors (U+FE00–U+FE0F and U+E0100–U+E01EF) are legitimate Unicode characters used to specify glyph variants, but attackers repurpose them to embed invisible payloads inside ordinary emoji. A shift cipher transforms standard Unicode characters into Variation Selector codepoints, producing a string that displays as a harmless emoji but contains hidden instructions. FireTail research (2025) confirmed that Google Gemini and Grok decode these payloads when given a decoding algorithm in-context, while Meta, ChatGPT, DeepSeek, and Claude rejected the technique. The Mindgard study (arXiv:2504.11168) measured up to 100% bypass rates against commercial guardrails using this method.

**Detection:** Block all Variation Selectors (U+FE00–U+FE0F, U+E0100–U+E01EF) at the input layer. If emoji rendering is required, re-encode through a known-safe emoji library that strips non-standard variation sequences. The Black Box Emoji Fix technique (Renee M. Gagnon, 2025) applies NFKC normalization followed by grapheme cluster analysis to detect token-explosion triggers and strip injected variation selectors.

### Token Explosion Attacks

Certain Unicode characters — particularly complex emoji sequences, deeply nested combining characters, and abuse of Variation Selectors — can cause a single visible character to expand into dozens or hundreds of tokens during BPE tokenization. This enables denial-of-service by consuming the model's context window with a small input, and can also cause misclassification of harmful content when safety classifiers operate on unexpected token counts. OWASP classifies unbounded consumption as a top-10 LLM vulnerability (LLM10:2025).

**Detection:** Implement a pre-tokenization check that measures the token-to-grapheme ratio. Flag inputs where any single grapheme cluster produces more than a configurable threshold of tokens (e.g., >10 tokens per cluster). The Black Box Emoji Fix approach uses a custom tokenizer to detect excessive tokenization within grapheme clusters before the input reaches the model.

### Invisible Unicode in Supply-Chain Attacks (Glassworm)

As of March 2026, the Glassworm campaign demonstrated that invisible Unicode characters are now used to hide malicious code in software repositories — not just in LLM prompts. Attackers embed payloads using Variation Selectors and PUA characters that render as empty strings in editors, terminals, and code review interfaces. When executed, a decoder extracts the hidden payload and passes it to `eval()`. This is directly relevant to AI coding assistants (Copilot, Cursor, Amp) that process repository code as context: if the assistant ingests invisible-Unicode payloads from compromised dependencies, the hidden instructions may be interpreted as part of the prompt context.

**Detection:** Apply the same character allow-list filtering to code inputs ingested by AI assistants. Scan for Variation Selectors, PUA ranges, and Tags block characters in source code files. Tools like Aikido Safe Chain and Snyk can detect invisible Unicode payloads in package dependencies.

---

## Notable Incidents

| Date | Incident | Relevance |
|------|----------|-----------|
| January 2024 | Riley Goodside publicly demonstrates Unicode tag smuggling against LLMs — invisible text encoded in U+E0000 block is decoded by tokenizers while invisible to users and safety monitors | Directly motivates stripping the Tags block as a character-level defense |
| April 2025 | Mindgard research (arXiv:2504.11168) tests 12 character injection methods against 6 commercial guardrails — emoji smuggling achieves 100% bypass, zero-width and Unicode tags routinely defeat classifiers | Demonstrates that guardrails alone are insufficient without upstream character filtering |
| September 2025 | FireTail/Viktor Markopoulos demonstrates ASCII smuggling against Google Gemini, Grok, and DeepSeek — Google Calendar identity spoofing and e-commerce review poisoning. Google declined to patch after responsible disclosure | Shows real-world exploitation of Unicode tag attacks against production systems |
| 2025 | Sourcegraph Amp Code vulnerable to invisible Unicode prompt injection in code files, allowing agent hijacking. Fixed after disclosure by Johann Rehberger | Demonstrates Unicode tag attacks in agentic coding tools, not just chat interfaces |
| December 2025 | Palo Alto Unit 42 documents real-world indirect prompt injection using invisible Unicode targeting AI-based product ad review systems in production | First documented in-the-wild exploitation of invisible Unicode against production AI business systems |
| March 2026 | Glassworm supply-chain campaign uses invisible Unicode characters (Variation Selectors U+FE00–U+FE0F and Supplementary PUA U+E0100–U+E01EF) to hide malicious payloads in 151+ GitHub repositories and npm packages — code renders as empty strings in editors but executes second-stage payloads via `eval()`. Compromised projects include Wasmer and Reworm (1,460 stars). Discovered by Aikido Security and Koi Security | Demonstrates that invisible Unicode is now weaponized in software supply chains, not just LLM prompts. Character filtering must extend to code inputs processed by AI coding assistants |
| 2025–2026 | FireTail research confirms emoji smuggling via Variation Selectors successfully exploits Google Gemini and Grok — hidden payloads invisible to humans are decoded when the model is given a decoding algorithm. Meta, ChatGPT, DeepSeek, and Claude are not vulnerable to this specific technique | Highlights that emoji smuggling is model-dependent; defense-in-depth at the input layer catches attacks regardless of model resilience |
| 2025 | Palo Alto Unit 42 documents homograph attacks using Cyrillic/Greek substitution to bypass email and content security filters, with AI-driven phishing at scale making detection harder. Cortex analysis reveals multiple financial-services impersonation campaigns | Reinforces that homoglyph detection (UTS #39 confusable analysis) is critical even outside LLM-specific contexts |

---

## Implementation Guidance

### Recommended Allow-List Strategy

A layered approach, applied in order before any prompt assembly:

1. **Strip dangerous Unicode ranges outright:** Tags block (U+E0000–U+E007F), zero-width characters (U+200B, U+200C, U+200D, U+2060, U+FEFF), Variation Selectors (U+FE00–U+FE0F, U+E0100–U+E01EF), Private Use Area (U+E000–U+F8FF, U+F0000–U+10FFFD), control characters (U+0000–U+001F, U+007F–U+009F).

2. **Apply NFKC normalization** to collapse compatibility equivalences (e.g., fullwidth Latin → ASCII Latin).

3. **Validate against Unicode category allow-list** per input field. Default: allow L (Letters), N (Numbers), P (Punctuation), Zs (Space Separator). Block Cc, Cf, Co, Cn, Cs, and any remaining Mc/Me/Mn not needed.

4. **Run confusable detection** on remaining text — flag or reject strings mixing confusable scripts (e.g., Latin + Cyrillic) unless the application explicitly requires mixed-script input.

5. **Validate at every entry point** — not just direct user input but also indirect inputs from RAG retrieval, tool outputs, MCP server responses, and web content (per C2.1.1).

6. **Deploy WAF-level character filtering** as an additional perimeter layer. Cisco documented a YARA rule for Unicode tag detection (`{ F3 A0 [0-2] ?? }` with threshold >10 matches), and Kemp LoadMaster WAF supports custom rules to block requests containing Tags block characters. WAF filtering catches attacks before they reach application code, providing defense-in-depth even if application-level validation has bugs.

### UTS #39 Restriction Levels

The Unicode Consortium defines six restriction levels that provide a ready-made policy framework:

| Level | Description | When to Use |
|-------|-------------|-------------|
| ASCII-Only | Characters ≤ U+007F only | Numeric fields, identifiers, API keys |
| Single Script | One resolved script set | Username fields, single-language inputs |
| Highly Restrictive | Single Script or Latin+CJK | East Asian applications needing Latin interop |
| Moderately Restrictive | Latin + one recommended script (excluding Cyrillic/Greek) | Most multilingual applications |
| Minimally Restrictive | No script mixing restrictions | Research or translation use cases |
| Unrestricted | No restrictions | Not recommended for AI-facing inputs |

### Tools and Libraries

| Tool | Language | Purpose | Notes |
|------|----------|---------|-------|
| [LLM Guard InvisibleText](https://github.com/protectai/llm-guard) | Python | Filters Cf, Cc, Co, Cn categories and PUA ranges for LLM inputs | Bypassable alone — use as one layer. 225k+ monthly downloads |
| [confusable_homoglyphs](https://github.com/vhf/confusable_homoglyphs) v3.2.0 | Python | Detects cross-script homoglyph substitution using Unicode confusables.txt | Now maintained at sr.ht/~valhalla/confusable_homoglyphs |
| [sanitext](https://github.com/panispani/sanitext) | Python/CLI | Detects suspicious Unicode, normalizes lookalikes to ASCII via NFKC, custom allow-lists | Lightweight, good for pipelines |
| [ICU4J](https://icu.unicode.org/) v78.3 | Java | `SpoofChecker` for confusable detection per UTS #39, `UCharacter.getType()` for category filtering | Unicode Consortium's official implementation |
| [ICU4X](https://github.com/unicode-org/icu4x) v2.0 | Rust/WASM | Modern Unicode property queries and normalization with FFI bindings to JS, C++, Dart | Suitable for edge/browser deployment |
| [Garak](https://github.com/NVIDIA/garak) | Python | Red-team testing for character-level attacks on LLMs | Validates that defenses actually hold |
| [Promptfoo](https://www.promptfoo.dev/) | Node.js | ASCII smuggling plugin for testing Unicode tag injection | Integrates into CI/CD red-team pipelines |
| [Black Box Emoji Fix](https://www.tdcommons.org/dpubs_series/7836/) | Python | NFKC normalization + grapheme cluster analysis + token explosion detection for emoji-based injection | Apache 2.0. Detects variation selector abuse and anomalous token-to-grapheme ratios |
| [Prompt Security](https://prompt.security/) | SaaS/API | Real-time Unicode-level text inspection with configurable blocking/redaction of visible and invisible characters | Commercial. Includes both input scanning and output filtering |
| [Aikido Safe Chain](https://www.aikido.dev/) | npm wrapper | Scans npm/yarn/pnpm dependencies for invisible Unicode payloads (Glassworm-style supply-chain attacks) | Protects AI coding assistants that ingest repository code |

---

## Implementation Maturity

| Aspect | Maturity | Notes |
|--------|----------|-------|
| Basic character stripping (Tags, zero-width, control) | **High** — straightforward to implement with stdlib | Python one-liner: `''.join(ch for ch in text if not (0xE0000 <= ord(ch) <= 0xE007F))` |
| Unicode category-based allow-listing | **High** — well-supported across all major languages | `unicodedata.category()` in Python, `Character.getType()` in Java |
| Homoglyph/confusable detection | **Medium** — libraries exist but require tuning for false positives | UTS #39 restriction levels help, but mixed-script legitimate content (academic, multilingual) needs careful policy |
| Automated correlation of rejection logs with prompt injection attempts | **Low** — no off-the-shelf tooling as of March 2026 | Must build custom SIEM rules; significant gap for SOC teams |
| Per-field adaptive allow-lists | **Low** — most implementations use a single global policy | Dynamic allow-lists that adjust per input context are an open research area |
| Token explosion detection | **Medium** — grapheme cluster analysis approach documented (Black Box Emoji Fix, 2025) but not yet widely adopted | Requires custom tokenizer integration; no standard library support yet |
| Supply-chain invisible Unicode scanning | **Medium** — Aikido Safe Chain and Snyk detect Glassworm-style payloads in npm/GitHub | Growing adoption after March 2026 Glassworm campaign; most CI/CD pipelines still lack this check |
| WAF-level Unicode tag filtering | **Medium** — YARA rules and WAF custom rules documented by Cisco and Kemp | Effective perimeter defense but requires tuning to avoid blocking legitimate Unicode in multilingual deployments |

---

## Cross-Chapter Links

| Requirement | Related | Relationship |
|-------------|---------|-------------|
| 2.3.1 (Character allow-list) | **C2.2.1** (Unicode normalization) | Character stripping operates upstream of normalization — strip first, then normalize remaining characters. Different layers: rejection vs. transformation |
| 2.3.1 (Character allow-list) | **C2.1.1** (Prompt injection defense) | Character filtering removes encoding-based evasion vectors before prompt injection classifiers run. Without it, classifiers are blind to invisible payloads |
| 2.3.2 (Rejection logging) | **C13.1** (Security event logging) | Rejection events should flow into the same structured logging pipeline and SIEM as other security events |
| 2.3.2 (Rejection logging) | **C2.6** (Rate limiting) | High-volume rejection events from a single source should trigger rate-limiting thresholds |
| 2.3.1 (Character allow-list) | **C2.7.1** (Multi-modal input validation) | Extracted text from images, audio, and documents (OCR, STT) must pass through the same character allow-list before prompt assembly |
| 2.3.1 (Character allow-list) | **C11.1** (Model alignment safety) | Character-level filtering is a defense-in-depth layer for adversarial robustness — restricts the input alphabet available to adversaries |
| 2.3.1 (Character allow-list) | **C6** (Supply chain) | Invisible Unicode in code dependencies (Glassworm, March 2026) can inject payloads into AI coding assistants — character filtering must extend to code inputs |

---

## Related Standards & References

- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [ASVS V5: Validation, Sanitization and Encoding](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V5-Validation.md) — V5.1.3, V5.1.4, V5.2.2, V5.3.2
- [Unicode Security Mechanisms (UTS #39)](https://www.unicode.org/reports/tr39/) — confusable detection, restriction levels, mixed-script analysis
- [Unicode General Categories (UAX #44)](https://www.unicode.org/reports/tr44/#General_Category_Values)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CWE-176: Improper Handling of Unicode Encoding](https://cwe.mitre.org/data/definitions/176.html)
- [CWE-180: Incorrect Behavior Order: Validate Before Canonicalize](https://cwe.mitre.org/data/definitions/180.html)
- [CWE-1289: Improper Validation of Unsafe Equivalence](https://cwe.mitre.org/data/definitions/1289.html)
- [MITRE ATLAS AML.T0051: LLM Prompt Injection](https://atlas.mitre.org/techniques/AML.T0051)
- [EU AI Act Article 15: Accuracy, Robustness and Cybersecurity](https://artificialintelligenceact.eu/article/15/) — Article 15(5) mandates resilience against adversarial inputs
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [Cisco: Understanding and Mitigating Unicode Tag Prompt Injection](https://blogs.cisco.com/ai/understanding-and-mitigating-unicode-tag-prompt-injection)
- [AWS: Defending LLM Applications Against Unicode Character Smuggling](https://aws.amazon.com/blogs/security/defending-llm-applications-against-unicode-character-smuggling/)
- [Mindgard: Outsmarting AI Guardrails with Invisible Characters (arXiv:2504.11168)](https://mindgard.ai/blog/outsmarting-ai-guardrails-with-invisible-characters-and-adversarial-prompts)
- [FireTail: ASCII Smuggling across Various LLMs](https://www.firetail.ai/blog/ghosts-in-the-machine-ascii-smuggling-across-various-llms)
- Geh, Shao, Van den Broeck. "Adversarial Tokenization." ACL 2025 (arXiv:2503.02174)
- "Special-Character Adversarial Attacks on Open-Source Language Models." arXiv:2508.14070 (November 2025)
- "Tokenization Matters! Degrading Large Language Models through Challenging Their Tokenization." arXiv:2405.17067 (May 2025)
- [Aikido: Glassworm Returns — Invisible Unicode Attack on GitHub, npm, and VS Code](https://www.aikido.dev/blog/glassworm-returns-unicode-attack-github-npm-vscode) (March 2026)
- [FireTail: Emoji Smuggling and Modern LLMs](https://www.firetail.ai/blog/peek-a-boo-emoji-smuggling-and-modern-llms)
- [Palo Alto Unit 42: The Homograph Illusion — Not Everything Is As It Seems](https://unit42.paloaltonetworks.com/homograph-attacks/)
- [Black Box Emoji Fix: A Unicode Sanitization Method for Mitigating Emoji-Based Injection Attacks in LLM Systems](https://www.tdcommons.org/dpubs_series/7836/) (2025)
- [Keysight: Understanding Invisible Prompt Injection Attack](https://www.keysight.com/blogs/en/tech/nwvs/2025/05/16/invisible-prompt-injection-attack)
- [Prompt Security: Unicode Exploits Are Compromising Application Security](https://prompt.security/blog/unicode-exploits-are-compromising-application-security)
- [NIST Cybersecurity Framework Profile for Artificial Intelligence](https://www.nist.gov/news-events/news/2025/12/draft-nist-guidelines-rethink-cybersecurity-ai-era) (December 2025)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- "Emoji Attack: Enhancing Jailbreak Attacks Against Judge LLM Detection." arXiv:2411.01077 (2024)

---

## Open Research Questions

- What is the optimal character allow-list strategy for multilingual AI applications that need to support dozens of scripts? UTS #39 restriction levels provide a starting framework, but real-world deployment data on false positive rates per restriction level in AI applications is scarce.
- How do character set restrictions interact with tokenizer behavior — can a restricted character set inadvertently produce unexpected token sequences? Research on adversarial tokenization (Geh et al., ACL 2025) suggests that reducing the input alphabet constrains the tokenizer's segmentation space, but the interaction is not fully characterized.
- Should character set restrictions be applied per-field (structured input) or globally (free-text prompts), and how does this affect usability? Current implementations largely use a single global policy; adaptive per-field allow-lists remain an open area.
- Can character-level rejection telemetry be reliably used as an early-warning signal for prompt injection campaigns? No published work correlates character rejection patterns with downstream attack success rates.
- How should character filtering handle code inputs (e.g., in coding assistants) where control characters, Unicode escapes, and unusual symbols may be legitimate? The tension between security and functionality is especially acute for developer-facing AI tools. The Glassworm campaign (March 2026) makes this question urgent — AI coding assistants must filter invisible Unicode from ingested code without breaking legitimate use of Unicode in string literals and comments.
- What is the optimal token-to-grapheme ratio threshold for detecting token explosion attacks? The Black Box Emoji Fix approach proposes grapheme cluster analysis, but real-world calibration data across different tokenizers (GPT-4, Claude, Llama) is lacking.
- How should emoji smuggling defenses differ between models? FireTail research shows Gemini and Grok are vulnerable while Claude and ChatGPT are not — should defenses be model-aware, or should input-layer filtering be uniform regardless of downstream model?

---
