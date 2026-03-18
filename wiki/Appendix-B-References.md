# Appendix B: References — Research Notes

> **Source:** [`1.0/en/0x91-Appendix-B_References.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x91-Appendix-B_References.md)

## Overview

Appendix B lists the standards, frameworks, specifications, and publications referenced throughout AISVS. This research page audits coverage: which chapter references are missing from Appendix B, which Appendix B entries aren't cited, and where URL inconsistencies exist.

---

## Coverage Audit

### References Cited in Chapters but Missing from Appendix B

39 references are cited across the 14 chapters but do not appear in Appendix B. Grouped by suggested category:

#### Standards and Frameworks (missing)

| Reference | Cited In | Link |
|-----------|----------|------|
| NIST Cybersecurity Framework 2.0 | C4 | https://www.nist.gov/cyberframework |
| CIS Controls v8 | C4 | https://www.cisecurity.org/controls/v8 |
| NIST SP 800-207: Zero Trust Architecture | C5, C9, C10 | https://csrc.nist.gov/pubs/sp/800/207/final |
| NIST SP 800-162: Guide to ABAC | C5 | https://csrc.nist.gov/pubs/sp/800/162/final |
| NIST SP 800-63-3: Digital Identity Guidelines | C5 | https://csrc.nist.gov/pubs/sp/800/63/3/final |
| NIST IR 8360: ML for Access Control Policy Verification | C5 | https://csrc.nist.gov/pubs/ir/8360/final |
| NIST AI 100-2e2023: Adversarial Machine Learning | C11 | https://csrc.nist.gov/pubs/ai/100/2/e2023/final |
| CISA Advisory: Securing Data for AI Systems | C1 | https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a |
| Cloud Security Alliance: Cloud Controls Matrix | C4 | https://cloudsecurityalliance.org/research/cloud-controls-matrix/ |
| ENISA: Secure Infrastructure Design | C4 | https://www.enisa.europa.eu/topics/critical-information-infrastructures-and-services |
| Kubernetes Security Best Practices | C4 | https://kubernetes.io/docs/concepts/security/ |
| MLOps Principles | C3 | https://ml-ops.org/content/mlops-principles |

#### OWASP LLM Top 10 Individual Entries (missing — only parent project page is in Appendix B)

| Reference | Cited In | Link |
|-----------|----------|------|
| LLM01:2025 Prompt Injection | C2 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| LLM02:2025 Sensitive Information Disclosure | C8, C11, C12 | https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/ |
| LLM03:2025 Supply Chain | C6 | https://genai.owasp.org/llmrisk/llm032025-supply-chain/ |
| LLM04:2025 Data and Model Poisoning | C8, C11 | https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/ |
| LLM05:2025 Improper Output Handling | C7 | https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ |
| LLM06:2025 Excessive Agency | C7, C9 | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ |
| LLM08:2025 Vector and Embedding Weaknesses | C8 | https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ |
| LLM10:2025 Unbounded Consumption | C9, C11 | https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ |

#### OWASP Agentic AI Resources (missing)

| Reference | Cited In | Link |
|-----------|----------|------|
| OWASP Agentic AI Threats and Mitigations | C9 | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ |
| OWASP Top 10 for Agentic Applications 2026 | C9 | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026 |

#### OWASP Cheat Sheets (missing)

| Reference | Cited In | Link |
|-----------|----------|------|
| LLM Prompt Injection Prevention Cheat Sheet | C2 | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html |

#### MITRE ATLAS Technique Pages (missing — only main ATLAS site in Appendix B)

| Reference | Cited In | Link |
|-----------|----------|------|
| AML.M00150: Adversarial Input Detection | C2 | https://atlas.mitre.org/mitigations/AML.M00150 |
| AML.T0010: Supply Chain Compromise | C6 | https://atlas.mitre.org/techniques/AML.T0010 |
| AML.T0018: Backdoor ML Model | C11 | https://atlas.mitre.org/techniques/AML.T0018 |
| AML.T0024.000: Infer Training Data Membership | C8, C11 | https://atlas.mitre.org/techniques/AML.T0024.000 |
| AML.T0024.001: Invert ML Model | C8, C11 | https://atlas.mitre.org/techniques/AML.T0024.001 |
| AML.T0024.002: Extract ML Model | C11 | https://atlas.mitre.org/techniques/AML.T0024.002 |
| AML.T0070: RAG Poisoning | C8 | https://atlas.mitre.org/techniques/AML.T0070 |
| AML.T0071: False RAG Entry Injection | C8 | https://atlas.mitre.org/techniques/AML.T0071 |

#### Vendor Documentation (missing)

| Reference | Cited In | Link |
|-----------|----------|------|
| Mitigate jailbreaks and prompt injections (Anthropic) | C2 | https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks |
| Reinforcement fine-tuning (OpenAI) | C3 | https://platform.openai.com/docs/guides/reinforcement-fine-tuning |
| AI adversarial robustness (IBM Research) | C3 | https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness |
| OpenAI Privacy Center: Data Deletion Controls | C1 | https://privacy.openai.com/policies?modal=take-control |
| SBOM Overview (CISA) | C6 | https://www.cisa.gov/sbom |

---

### References in Appendix B Not Cited by Any Chapter (C1-C14)

These references are in Appendix B but only appear in appendices, not in the main chapters:

| Reference | Category | Notes |
|-----------|----------|-------|
| NIST SP 800-218A: Secure Software Dev for GenAI | Standards | Cited in Appendix C and D only |
| ISO/IEC 42001:2023 | Standards | Cited in Appendix C and D only |
| OWASP ASVS | Standards | Cited in Appendix D only |
| OWASP Secure Coding Practices | Standards | Cited in Appendix C only |
| OpenID Connect Core 1.0 | Specifications | Not cited in any chapter or appendix references |
| NIST Post-Quantum Cryptography Standards | Cryptographic | Not cited in any chapter |

---

## URL Inconsistencies

The same document is referenced with different URLs across chapters:

| Document | URLs Used | Recommendation |
|----------|-----------|----------------|
| NIST AI RMF 1.0 | `nist.gov/itl/ai-risk-management-framework` (C1, C4, C12), `nist.gov/system/files/documents/...` (C13), `doi.org/10.6028/NIST.AI.100-1` (C13), `nvlpubs.nist.gov/...` (Appendix B) | Standardize on one canonical URL |
| NIST SP 800-207 | `csrc.nist.gov/pubs/sp/800/207/final` (C5) vs `csrc.nist.gov/pubs/detail/sp/800-207/final` (C9, C10) | Standardize on `/pubs/sp/` form |
| MITRE ATLAS AML.T0024.001 | "Invert AI Model" (C8) vs "Invert ML Model" (C11) | Use consistent title |

---

## Structural Issues

1. **C14 has an empty References section** — the `## References` header exists but no references are listed. Should be populated.

2. **Decision needed: granular MITRE ATLAS links** — 8 specific ATLAS technique/mitigation pages are cited across chapters. Should these be listed individually in Appendix B, or does the main ATLAS site link suffice?

3. **Decision needed: OWASP LLM Top 10 entries** — 8 individual risk entries are cited. Should each be listed in Appendix B, or does the parent project link suffice?

---

## Community Notes

_Discussion about reference scope, URL standardization, and completeness._

---

[README](README.md)
