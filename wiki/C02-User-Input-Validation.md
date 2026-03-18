# C02: User Input Validation

> **Source:** [`1.0/en/0x10-C02-User-Input-Validation.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C02-User-Input-Validation.md)
> **Requirements:** 33 | **Sections:** 8

## Control Objective

Robust validation of user input is a first-line defense against some of the most damaging attacks on AI systems. Prompt injection attacks can override system instructions, leak sensitive data, or steer the model toward behavior that is not allowed.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C2.1 | Prompt Injection Defense | 4 | 2.1.1–2.1.4 |
| C2.2 | Adversarial-Example Resistance | 5 | 2.2.1–2.2.5 |
| C2.3 | Prompt Character Set | 2 | 2.3.1–2.3.2 |
| C2.4 | Schema, Type & Length Validation | 5 | 2.4.1–2.4.5 |
| C2.5 | Content & Policy Screening | 4 | 2.5.1–2.5.4 |
| C2.6 | Input Rate Limiting & Abuse Prevention | 4 | 2.6.1–2.6.4 |
| C2.7 | Multi-Modal Input Validation | 5 | 2.7.1–2.7.5 |
| C2.8 | Real-Time Adaptive Threat Detection | 4 | 2.8.1–2.8.4 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Direct prompt injection (overriding system instructions via user input)
- Indirect prompt injection (injected instructions in retrieved content)
- Unicode/encoding-based evasion (invisible characters, homoglyphs, RTL overrides)
- Multi-modal injection (instructions hidden in images, audio, or documents)
- Crescendo attacks (gradually escalating benign prompts toward harmful outputs)

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Prompt injection detection:** Rebuff, Prompt Guard (Meta), LLM Guard, Lakera Guard
- **Input validation:** JSON Schema, Pydantic, Zod (for structured input validation)
- **Content filtering:** OpenAI Moderation API, Anthropic content filtering, Azure AI Content Safety
- **Rate limiting:** API gateway rate limiting (Kong, AWS API Gateway), custom token-bucket implementations

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C2.1 Prompt Injection Defense | _TBD_ | |
| C2.2 Adversarial-Example Resistance | _TBD_ | |
| C2.3 Prompt Character Set | _TBD_ | |
| C2.4 Schema, Type & Length Validation | _TBD_ | |
| C2.5 Content & Policy Screening | _TBD_ | |
| C2.6 Input Rate Limiting & Abuse Prevention | _TBD_ | |
| C2.7 Multi-Modal Input Validation | _TBD_ | |
| C2.8 Real-Time Adaptive Threat Detection | _TBD_ | |

---

## Open Research Questions

- [ ] Is there a reliable automated benchmark for prompt injection defense effectiveness?
- [ ] How do you balance input filtering strictness with usability for legitimate multi-language users?
- [ ] What's the current best practice for defending against indirect prompt injection in RAG pipelines?
- [ ] How should multi-modal input validation differ from text-only validation?

---

## Related Standards & Cross-References

- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [MITRE ATLAS: Adversarial Input Detection](https://atlas.mitre.org/mitigations/AML.M00150)
- [Mitigate jailbreaks and prompt injections (Anthropic)](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

