# C2.3 Prompt Character Set

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation)

## Purpose

Restricting the character set of user inputs to only allow characters necessary for business requirements is a foundational input validation technique. In the AI context, this is particularly effective at blocking encoding-based evasion attacks, Unicode tricks, and control character injection. An allow-list approach ensures that only expected characters reach the model, reducing the attack surface for adversarial input manipulation. While simple in concept, character set restrictions must be carefully designed to avoid breaking legitimate multilingual or technical use cases.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.3.1** | **Verify that** the system implements a character set limitation for user inputs, allowing only characters that are explicitly required for business purposes using an allow-list approach. | 1 | D | Unicode-based filter bypass; control character injection; invisible character attacks; homoglyph attacks; encoding-based prompt injection evasion; character set exploitation for smuggling payloads. | 1. Review the input validation code for character allow-list implementation. 2. Confirm the allow-list is defined per input field/endpoint (e.g., a name field allows Unicode letters; a numeric field allows digits and decimal points). 3. Test with characters outside the allow-list: control characters (U+0000-U+001F), Unicode format characters, private use area characters, emoji (if not needed), mathematical symbols used as homoglyphs. 4. Verify the allow-list is enforced before any other processing. | The challenge is defining the right allow-list. For multilingual applications, restricting to ASCII breaks legitimate use. A pragmatic approach: allow Unicode letter/number categories (L, N) plus explicitly needed punctuation, and block control characters (Cc), format characters (Cf), surrogate pairs (Cs), and private use (Co). Tools: Python `regex` library with Unicode categories, Java `Character.getType()`. This overlaps with C2.2.1 normalization but operates at a different layer (rejection vs. normalization). |
| **2.3.2** | **Verify that** inputs containing characters outside of the allowed set are rejected and logged with trace metadata (source, tool or MCP server, agent ID, session). | 1 | D/V | Undetected evasion attempts; inability to investigate character-based attack patterns; lack of forensic trail for encoding attacks. | 1. Submit inputs with disallowed characters and confirm they are rejected with a safe error message (not revealing internal validation logic). 2. Check logs for: rejected characters (hex-encoded), input source, tool/MCP server if applicable, agent ID, session ID, timestamp. 3. Verify rejection is fail-closed (input is not partially processed). 4. Confirm error responses do not leak allow-list details that would help an attacker craft bypass attempts. | Logging rejected characters in hex encoding is important -- logging raw control characters can cause log injection. The error message to the user should be generic ("invalid input") without revealing which specific characters are blocked or the allow-list pattern. Log volume may be high if legitimate users encounter overly restrictive allow-lists; monitoring for false positive spikes is advisable. |

---

## Related Standards & References

- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [ASVS V5: Validation, Sanitization and Encoding](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V5-Validation.md)
- [Unicode Security Mechanisms (Unicode TR39)](https://unicode.org/reports/tr39/)
- [Unicode General Categories](https://www.unicode.org/reports/tr44/#General_Category_Values)

---

## Open Research Questions

- What is the optimal character allow-list strategy for multilingual AI applications that need to support dozens of scripts?
- How do character set restrictions interact with tokenizer behavior -- can a restricted character set inadvertently produce unexpected token sequences?
- Should character set restrictions be applied per-field (structured input) or globally (free-text prompts), and how does this affect usability?

---
