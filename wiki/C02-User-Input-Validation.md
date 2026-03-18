# C02: User Input Validation

> **Source:** [`1.0/en/0x10-C02-User-Input-Validation.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C02-User-Input-Validation.md)
> **Requirements:** 33 | **Sections:** 8

## Control Objective

Robust validation of user input is a first-line defense against some of the most damaging attacks on AI systems. Prompt injection attacks can override system instructions, leak sensitive data, or steer the model toward behavior that is not allowed. Unless dedicated filters and other validation is in place, research shows that jailbreaks that exploit context windows will continue to be effective.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C2.1 | Prompt Injection Defense | 4 | [C02-01-Prompt-Injection-Defense](C02-01-Prompt-Injection-Defense) |
| C2.2 | Adversarial-Example Resistance | 5 | [C02-02-Adversarial-Example-Resistance](C02-02-Adversarial-Example-Resistance) |
| C2.3 | Prompt Character Set | 2 | [C02-03-Prompt-Character-Set](C02-03-Prompt-Character-Set) |
| C2.4 | Schema, Type & Length Validation | 5 | [C02-04-Schema-Type-Length-Validation](C02-04-Schema-Type-Length-Validation) |
| C2.5 | Content & Policy Screening | 4 | [C02-05-Content-Policy-Screening](C02-05-Content-Policy-Screening) |
| C2.6 | Input Rate Limiting & Abuse Prevention | 4 | [C02-06-Input-Rate-Limiting-Abuse-Prevention](C02-06-Input-Rate-Limiting-Abuse-Prevention) |
| C2.7 | Multi-Modal Input Validation | 5 | [C02-07-Multi-Modal-Input-Validation](C02-07-Multi-Modal-Input-Validation) |
| C2.8 | Real-Time Adaptive Threat Detection | 4 | [C02-08-Real-Time-Adaptive-Threat-Detection](C02-08-Real-Time-Adaptive-Threat-Detection) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Direct prompt injection (overriding system instructions via user input)
- Indirect prompt injection (injected instructions in retrieved content)
- Unicode/encoding-based evasion (invisible characters, homoglyphs, RTL overrides)
- Multi-modal injection (instructions hidden in images, audio, or documents)
- Crescendo attacks (gradually escalating benign prompts toward harmful outputs)

---

## Related Standards & Cross-References

- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [MITRE ATLAS: Adversarial Input Detection](https://atlas.mitre.org/mitigations/AML.M00150)
- [Mitigate jailbreaks and prompt injections (Anthropic)](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)
- [NIST AI 100-2e2025: Adversarial Machine Learning](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C7 Model Behavior | Output validation, guardrails | C2 handles input-side; C7 handles output-side enforcement |
| C9 Orchestration & Agents | Agent input surfaces, tool call validation | Agent chains amplify prompt injection risk across hops |
| C10 MCP Security | MCP tool argument validation | MCP surfaces are explicit input vectors covered by C2.4 |
| C11 Adversarial Robustness | Adversarial perturbation defense | C2.2 focuses on input-layer detection; C11 covers model-level robustness |
| C13 Monitoring & Logging | Logging requirements for input validation events | C2 specifies what to log; C13 specifies how to store and alert |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
