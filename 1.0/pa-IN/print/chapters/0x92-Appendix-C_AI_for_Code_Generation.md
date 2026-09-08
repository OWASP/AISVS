<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md -->
<!-- Translator: GeeksikhSecurity -->

# Appendix C: AI-Assisted Secure Coding
# ਅੰਤਿਕਾ[^0x92-appendix] C: AI-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਸੁਰੱਖਿਅਤ ਕੋਡਿੰਗ

<!-- markdownlint-disable-next-line MD013 -->
<!-- cspell:words SSDF SAMM CICD PBAC Pulumi Conftest tfsec KICS Allstar unreviewed weaponization stylometric -->

## Objective
## ਉਦੇਸ਼

This appendix lists organizational controls for using AI coding tools safely. The range is baseline to advanced. Scope is coding, code review, and the rest of the SSDLC.

ਇਹ ਅੰਤਿਕਾ AI ਕੋਡਿੰਗ ਟੂਲਾਂ ਨੂੰ ਸਲਾਮਤ (safe) ਢੰਗ ਨਾਲ ਵਰਤਣ ਲਈ ਸੰਸਥਾਗਤ ਨਿਯੰਤਰਣ ਸੂਚੀਬੱਧ ਕਰਦੀ ਹੈ। ਇਹਨਾਂ ਦਾ ਘੇਰਾ ਬੇਸਲਾਈਨ[^0x92-baseline] (baseline) ਤੋਂ ਲੈ ਕੇ ਉੱਨਤ ਤੱਕ ਹੈ। ਦਾਇਰੇ ਵਿੱਚ ਕੋਡਿੰਗ, ਕੋਡ ਸਮੀਖਿਆ, ਅਤੇ ਬਾਕੀ SSDLC ਸ਼ਾਮਲ ਹਨ।

---

## AC.1 AI-Assisted Secure-Coding Workflow
## AC.1 AI-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਸੁਰੱਖਿਅਤ-ਕੋਡਿੰਗ ਵਰਕਫ਼ਲੋ

AI tooling has to slot into the existing SSDLC without weakening any of the security gates already in place. Equally important: write down the adversarial-AI threat scenarios that justify each guardrail. Doing this up front is much easier than reconstructing it after the fact.

AI ਟੂਲਿੰਗ ਨੂੰ ਮੌਜੂਦਾ SSDLC ਵਿੱਚ ਇਸ ਤਰ੍ਹਾਂ ਸਮਾਉਣਾ ਪੈਂਦਾ ਹੈ ਕਿ ਪਹਿਲਾਂ ਤੋਂ ਲੱਗੇ ਕਿਸੇ ਵੀ ਸੁਰੱਖਿਆ ਗੇਟ ਕਮਜ਼ੋਰ ਨਾ ਪੈਣ। ਓਨਾ ਹੀ ਜ਼ਰੂਰੀ: ਉਹ ਵਿਰੋਧੀ-AI ਖ਼ਤਰਾ ਦ੍ਰਿਸ਼[^0x92-threat-scenario] (adversarial-AI threat scenarios) ਲਿਖਤੀ ਰੂਪ ਵਿੱਚ ਦਰਜ ਕਰੋ ਜੋ ਹਰ ਗਾਰਡਰੇਲ[^0x92-guardrail] (guardrail) ਨੂੰ ਜਾਇਜ਼ ਠਹਿਰਾਉਂਦੇ ਹਨ। ਇਹ ਕੰਮ ਪਹਿਲਾਂ ਹੀ ਕਰ ਲੈਣਾ ਬਾਅਦ ਵਿੱਚ ਮੁੜ ਜੋੜਨ ਨਾਲੋਂ ਕਿਤੇ ਸੌਖਾ ਹੈ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.1.1** | **Verify that** a written workflow says when AI tools may generate, refactor, or review code. The workflow names the approved tools, the prohibited use cases, and the data classifications that are allowed as input. | 1 |
| **AC.1.2** | **Verify that** the workflow covers every SSDLC phase from design and implementation through code review, testing, deployment, and post-deployment monitoring, and names the security gates that stay mandatory whether AI was involved or not. | 2 |
| **AC.1.3** | **Verify that** the workflow names the adversarial-AI threat scenarios it is built to mitigate. The list should cover prompt injection delivered through PR content, AI-generated supply-chain payloads, autonomous agents approving their own work, fork-PR secret exfiltration, and compromise of the model supply chain. | 2 |
| **AC.1.4** | **Verify that** metrics are collected on AI-produced and AI-mediated code, and that the results are compared against a human-only baseline. Vulnerability density, mean-time-to-detect, AI-attributable defect rate, prompt-injection detection rate, and fork-PR rejection rate are all useful. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇੱਕ ਲਿਖਤੀ ਵਰਕਫ਼ਲੋ[^0x92-workflow] (workflow) ਦੱਸਦਾ ਹੈ ਕਿ AI ਟੂਲ ਕਦੋਂ ਕੋਡ ਤਿਆਰ ਕਰ ਸਕਦੇ ਹਨ, ਮੁੜ-ਸੰਗਠਿਤ (refactor) ਕਰ ਸਕਦੇ ਹਨ, ਜਾਂ ਉਸ ਦੀ ਸਮੀਖਿਆ ਕਰ ਸਕਦੇ ਹਨ। ਵਰਕਫ਼ਲੋ ਪ੍ਰਵਾਨਿਤ ਟੂਲਾਂ, ਵਰਜਿਤ ਵਰਤੋਂ-ਮਾਮਲਿਆਂ, ਅਤੇ ਉਹਨਾਂ ਡਾਟਾ ਵਰਗੀਕਰਨਾਂ ਦੇ ਨਾਂ ਦੱਸਦਾ ਹੈ ਜਿਨ੍ਹਾਂ ਨੂੰ ਇਨਪੁੱਟ ਵਜੋਂ ਦੇਣ ਦੀ ਇਜਾਜ਼ਤ ਹੈ। | 1 |
| **AC.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਵਰਕਫ਼ਲੋ ਡਿਜ਼ਾਈਨ ਅਤੇ ਲਾਗੂਕਰਨ ਤੋਂ ਲੈ ਕੇ ਕੋਡ ਸਮੀਖਿਆ, ਟੈਸਟਿੰਗ, ਤੈਨਾਤੀ, ਅਤੇ ਤੈਨਾਤੀ-ਉਪਰੰਤ ਨਿਗਰਾਨੀ ਤੱਕ ਹਰ SSDLC ਪੜਾਅ ਨੂੰ ਢੱਕਦਾ ਹੈ, ਅਤੇ ਉਹਨਾਂ ਸੁਰੱਖਿਆ ਗੇਟਾਂ ਦੇ ਨਾਂ ਦੱਸਦਾ ਹੈ ਜੋ AI ਦੇ ਸ਼ਾਮਲ ਹੋਣ ਜਾਂ ਨਾ ਹੋਣ ਦੇ ਬਾਵਜੂਦ ਲਾਜ਼ਮੀ ਰਹਿੰਦੇ ਹਨ। | 2 |
| **AC.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਵਰਕਫ਼ਲੋ ਉਹਨਾਂ ਵਿਰੋਧੀ-AI ਖ਼ਤਰਾ ਦ੍ਰਿਸ਼ਾਂ ਦੇ ਨਾਂ ਦੱਸਦਾ ਹੈ ਜਿਨ੍ਹਾਂ ਨੂੰ ਘਟਾਉਣ ਲਈ ਇਹ ਬਣਾਇਆ ਗਿਆ ਹੈ। ਇਸ ਸੂਚੀ ਵਿੱਚ PR ਸਮੱਗਰੀ ਰਾਹੀਂ ਪਹੁੰਚਾਇਆ ਗਿਆ prompt ਇੰਜੈਕਸ਼ਨ, AI ਦੁਆਰਾ ਤਿਆਰ ਸਪਲਾਈ ਚੇਨ ਪੇਲੋਡ, ਆਪਣੇ ਹੀ ਕੰਮ ਨੂੰ ਮਨਜ਼ੂਰੀ ਦਿੰਦੇ ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਏਜੰਟ, ਫ਼ੋਰਕ-PR[^0x92-fork] ਰਾਹੀਂ ਗੁਪਤ ਭੇਦ ਬਾਹਰ ਕੱਢਣਾ (exfiltration), ਅਤੇ ਮਾਡਲ ਸਪਲਾਈ ਚੇਨ ਦਾ ਸਮਝੌਤਾ (compromise) ਸ਼ਾਮਲ ਹੋਣੇ ਚਾਹੀਦੇ ਹਨ। | 2 |
| **AC.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਕੀਤੇ ਅਤੇ AI-ਵਿਚੋਲਗੀ ਵਾਲੇ ਕੋਡ ਬਾਰੇ ਮੈਟ੍ਰਿਕਸ (metrics) ਇਕੱਠੇ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ ਨਤੀਜਿਆਂ ਦੀ ਤੁਲਨਾ ਸਿਰਫ਼-ਮਨੁੱਖੀ ਬੇਸਲਾਈਨ ਨਾਲ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਕਮਜ਼ੋਰੀ ਘਣਤਾ, ਔਸਤ-ਪਛਾਣ-ਸਮਾਂ, AI ਨੂੰ ਸਰੋਤ-ਨਿਰਧਾਰਿਤ ਕੀਤੀ ਜਾ ਸਕਣ ਵਾਲੀ ਨੁਕਸ ਦਰ, prompt ਇੰਜੈਕਸ਼ਨ ਪਛਾਣ ਦਰ, ਅਤੇ ਫ਼ੋਰਕ-PR ਰੱਦਗੀ ਦਰ — ਇਹ ਸਾਰੇ ਲਾਭਦਾਇਕ ਹਨ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.1.1:** NIST SSDF PO.1 (Define Security Requirements for Software Development); ISO/IEC 42001 Clauses 6, 8; OWASP SAMM Strategy & Metrics (SM), Policy & Compliance (PC).
* **AC.1.2:** NIST SSDF PW.1, PW.7; OWASP SAMM Education & Guidance (EG); ISO/IEC 5338 Clause 6.
* **AC.1.3:** MITRE ATLAS (Reconnaissance & Initial Access tactics); NIST AI 600-1 GOVERN; OWASP LLM Top 10 (2025) LLM03; OWASP Agentic Top 10 (2026) ASI04.
* **AC.1.4:** NIST AI RMF MEASURE; ISO/IEC 42001 Clause 9; OWASP SAMM Strategy & Metrics (SM).

---

## AC.2 AI Tool Qualification & Threat Modeling
## AC.2 AI ਟੂਲ ਯੋਗਤਾ-ਨਿਰਧਾਰਨ ਅਤੇ ਖ਼ਤਰਾ ਮਾਡਲਿੰਗ

Do not adopt an AI coding tool until it has been evaluated. Three areas in particular: its security capabilities, its resistance to adversarial input, and the risk inherited from its supply chain.

ਕਿਸੇ AI ਕੋਡਿੰਗ ਟੂਲ ਨੂੰ ਉਦੋਂ ਤੱਕ ਨਾ ਅਪਣਾਓ ਜਦੋਂ ਤੱਕ ਉਸ ਦਾ ਮੁਲਾਂਕਣ ਨਾ ਹੋ ਜਾਵੇ। ਖ਼ਾਸ ਕਰਕੇ ਤਿੰਨ ਖੇਤਰ: ਉਸ ਦੀਆਂ ਸੁਰੱਖਿਆ ਸਮਰੱਥਾਵਾਂ, ਵਿਰੋਧੀ ਇਨਪੁੱਟ ਪ੍ਰਤੀ ਉਸ ਦਾ ਟਾਕਰਾ, ਅਤੇ ਉਸ ਦੀ ਸਪਲਾਈ ਚੇਨ ਤੋਂ ਵਿਰਸੇ ਵਿੱਚ ਮਿਲਿਆ ਜੋਖਮ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.2.1** | **Verify that** every AI tool, whether it is an assistant, a reviewer, an agent, or an MCP server, has a threat model. The threat model covers misuse, model inversion, training-data leakage, prompt injection from untrusted input, insecure output handling, excessive agency, and risk inherited from its dependency chain. | 1 |
| **AC.2.2** | **Verify that** the evaluation of each tool covers the local components (static and dynamic analysis), the SaaS endpoints (TLS, AuthN/AuthZ, logging, data residency), and the vendor's model supply chain (training-data provenance, fine-tune history, RAG sources). Each of these is reviewed and the review is written down. | 2 |
| **AC.2.3** | **Verify that** each tool goes through adversarial robustness testing before onboarding. The testing is repeated after any material change to the model or to the system prompts. Coverage includes automated prompt-injection probes, jailbreak suites, and indirect-injection corpora delivered through realistic PR and issue surfaces. | 2 |
| **AC.2.4** | **Verify that** evaluations follow a recognized framework such as NIST AI RMF, NIST AI 600-1 Generative AI Profile, or ISO/IEC 42001. Evaluations are repeated after a major version change, a vendor incident, or new threat intelligence relevant to the tool class. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ AI ਟੂਲ ਦਾ — ਭਾਵੇਂ ਉਹ ਸਹਾਇਕ ਹੋਵੇ, ਸਮੀਖਿਅਕ, ਏਜੰਟ, ਜਾਂ MCP ਸਰਵਰ — ਇੱਕ ਖ਼ਤਰਾ ਮਾਡਲ ਹੈ। ਇਹ ਖ਼ਤਰਾ ਮਾਡਲ ਦੁਰਵਰਤੋਂ, model inversion, ਸਿਖਲਾਈ-ਡਾਟਾ ਲੀਕੇਜ, ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟ ਤੋਂ prompt ਇੰਜੈਕਸ਼ਨ, ਗ਼ੈਰ-ਸੁਰੱਖਿਅਤ ਆਊਟਪੁੱਟ ਪ੍ਰਬੰਧਨ, ਲੋੜ ਤੋਂ ਵੱਧ ਏਜੰਸੀ (excessive agency), ਅਤੇ ਉਸ ਦੀ ਡਿਪੈਂਡੈਂਸੀ ਲੜੀ ਤੋਂ ਵਿਰਸੇ ਵਿੱਚ ਮਿਲੇ ਜੋਖਮ ਨੂੰ ਢੱਕਦਾ ਹੈ। | 1 |
| **AC.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਟੂਲ ਦਾ ਮੁਲਾਂਕਣ ਸਥਾਨਕ ਕੰਪੋਨੈਂਟਾਂ (ਸਥਿਰ ਅਤੇ ਗਤੀਸ਼ੀਲ ਵਿਸ਼ਲੇਸ਼ਣ), SaaS ਐਂਡਪੁਆਇੰਟਾਂ (TLS, AuthN/AuthZ, ਲੌਗਿੰਗ, ਡਾਟਾ ਨਿਵਾਸ), ਅਤੇ ਵਿਕਰੇਤਾ ਦੀ ਮਾਡਲ ਸਪਲਾਈ ਚੇਨ (ਸਿਖਲਾਈ-ਡਾਟਾ ਦਾ ਮੂਲ-ਸਰੋਤ, ਫ਼ਾਈਨ-ਟਿਊਨ ਇਤਿਹਾਸ, RAG ਸਰੋਤ) ਨੂੰ ਢੱਕਦਾ ਹੈ। ਇਹਨਾਂ ਵਿੱਚੋਂ ਹਰੇਕ ਦੀ ਸਮੀਖਿਆ ਕੀਤੀ ਜਾਂਦੀ ਹੈ ਅਤੇ ਸਮੀਖਿਆ ਲਿਖਤੀ ਰੂਪ ਵਿੱਚ ਦਰਜ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **AC.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਟੂਲ ਨੂੰ ਸ਼ਾਮਲ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਵਿਰੋਧੀ ਮਜ਼ਬੂਤੀ (adversarial robustness) ਟੈਸਟਿੰਗ ਵਿੱਚੋਂ ਲੰਘਾਇਆ ਜਾਂਦਾ ਹੈ। ਮਾਡਲ ਜਾਂ ਸਿਸਟਮ prompt ਵਿੱਚ ਕਿਸੇ ਵੀ ਮਹੱਤਵਪੂਰਨ ਤਬਦੀਲੀ ਤੋਂ ਬਾਅਦ ਇਹ ਟੈਸਟਿੰਗ ਦੁਹਰਾਈ ਜਾਂਦੀ ਹੈ। ਇਸ ਦੇ ਘੇਰੇ ਵਿੱਚ ਸਵੈਚਾਲਿਤ prompt ਇੰਜੈਕਸ਼ਨ ਪੜਤਾਲਾਂ, jailbreak ਸੂਟ, ਅਤੇ ਅਸਲੀਅਤ ਵਰਗੀਆਂ PR ਤੇ ਮੁੱਦਾ ਸਤ੍ਹਾਵਾਂ ਰਾਹੀਂ ਪਹੁੰਚਾਏ ਗਏ ਅਸਿੱਧੇ-ਇੰਜੈਕਸ਼ਨ ਕਾਰਪੋਰਾ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **AC.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮੁਲਾਂਕਣ ਕਿਸੇ ਮਾਨਤਾ-ਪ੍ਰਾਪਤ ਫ੍ਰੇਮਵਰਕ ਦੀ ਪਾਲਣਾ ਕਰਦੇ ਹਨ, ਜਿਵੇਂ NIST AI RMF, NIST AI 600-1 Generative AI Profile, ਜਾਂ ISO/IEC 42001। ਵੱਡੀ ਵਰਜ਼ਨ ਤਬਦੀਲੀ, ਵਿਕਰੇਤਾ ਦੀ ਕਿਸੇ ਘਟਨਾ, ਜਾਂ ਟੂਲ ਸ਼੍ਰੇਣੀ ਨਾਲ ਸੰਬੰਧਿਤ ਨਵੀਂ ਖ਼ਤਰਾ ਖ਼ੁਫ਼ੀਆ ਜਾਣਕਾਰੀ ਤੋਂ ਬਾਅਦ ਮੁਲਾਂਕਣ ਦੁਹਰਾਏ ਜਾਂਦੇ ਹਨ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.2.1:** OWASP LLM Top 10 (2025) LLM01, LLM06; OWASP Agentic Top 10 (2026) ASI01, ASI02, ASI03; AISVS C9; MITRE ATLAS (Threat modeling).
* **AC.2.2:** OWASP LLM Top 10 (2025) LLM03; OWASP Agentic Top 10 (2026) ASI04; NIST SSDF PO.1, PO.5; ISO/IEC 42001 Clause 8.
* **AC.2.3:** MITRE ATLAS (Adversarial ML testing); AISVS C2.1, C11.1; NIST AI 600-1 MEASURE.
* **AC.2.4:** ISO/IEC 42001 Clause 9.2; NIST AI RMF GOVERN.

---

## AC.3 Secure Prompt & Context Management
## AC.3 ਸੁਰੱਖਿਅਤ prompt ਅਤੇ ਸੰਦਰਭ ਪ੍ਰਬੰਧਨ

Two goals in this family. First: stop secrets, proprietary code, and personal data from leaking into prompts. Second: treat any content sourced from the repository, a PR, or a third party as untrusted input. Any of it can carry a prompt-injection payload, and most of it usually does not, which is part of what makes the rare hostile case easy to miss.

ਇਸ ਪਰਿਵਾਰ ਵਿੱਚ ਦੋ ਟੀਚੇ ਹਨ। ਪਹਿਲਾ: ਗੁਪਤ ਭੇਦਾਂ, ਮਲਕੀਅਤੀ ਕੋਡ, ਅਤੇ ਨਿੱਜੀ ਡਾਟੇ ਨੂੰ prompt ਵਿੱਚ ਲੀਕ ਹੋਣ ਤੋਂ ਰੋਕਣਾ। ਦੂਜਾ: ਰਿਪੌਜ਼ਟਰੀ, ਕਿਸੇ PR, ਜਾਂ ਕਿਸੇ ਤੀਜੀ ਧਿਰ ਤੋਂ ਆਈ ਹਰ ਸਮੱਗਰੀ ਨੂੰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟ ਵਜੋਂ ਲੈਣਾ। ਇਹਨਾਂ ਵਿੱਚੋਂ ਕੋਈ ਵੀ prompt ਇੰਜੈਕਸ਼ਨ ਪੇਲੋਡ ਲੈ ਕੇ ਆ ਸਕਦੀ ਹੈ, ਅਤੇ ਵਧੇਰੇ ਕਰਕੇ ਨਹੀਂ ਲਿਆਉਂਦੀ — ਇਹੀ ਗੱਲ ਵਿਰਲੇ ਦੁਸ਼ਮਣਾਨਾ ਮਾਮਲੇ ਨੂੰ ਨਜ਼ਰੋਂ ਖੁੰਝਾਉਣਾ ਸੌਖਾ ਬਣਾ ਦਿੰਦੀ ਹੈ।

> **Relationship to AISVS C2.1:** AC.3.3, AC.3.4, and AC.3.5 apply AISVS C2.1 (Prompt Injection Defenses) to the secure-coding case. If a finding here is something that C2.1 verification did not already close, count it as an additional gap (specific to coding-tool prompt construction). If C2.1 already closed it, do not count it twice.

> **AISVS C2.1 ਨਾਲ ਸੰਬੰਧ:** AC.3.3, AC.3.4, ਅਤੇ AC.3.5 AISVS C2.1 (Prompt Injection Defenses) ਨੂੰ ਸੁਰੱਖਿਅਤ-ਕੋਡਿੰਗ ਦੇ ਮਾਮਲੇ ਉੱਤੇ ਲਾਗੂ ਕਰਦੇ ਹਨ। ਜੇ ਇੱਥੋਂ ਦਾ ਕੋਈ ਖੋਜ-ਨਤੀਜਾ ਅਜਿਹਾ ਹੈ ਜਿਸ ਨੂੰ C2.1 ਦੀ ਤਸਦੀਕ ਨੇ ਪਹਿਲਾਂ ਹੀ ਬੰਦ ਨਹੀਂ ਕੀਤਾ ਸੀ, ਤਾਂ ਉਸ ਨੂੰ ਇੱਕ ਵਾਧੂ ਪਾੜੇ ਵਜੋਂ ਗਿਣੋ (ਜੋ ਕੋਡਿੰਗ-ਟੂਲ ਦੇ prompt ਨਿਰਮਾਣ ਲਈ ਵਿਸ਼ੇਸ਼ ਹੈ)। ਜੇ C2.1 ਨੇ ਉਸ ਨੂੰ ਪਹਿਲਾਂ ਹੀ ਬੰਦ ਕਰ ਦਿੱਤਾ ਸੀ, ਤਾਂ ਉਸ ਨੂੰ ਦੋ ਵਾਰ ਨਾ ਗਿਣੋ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.3.1** | **Verify that** written guidance forbids putting secrets, credentials, PII, or classified data in any prompt sent to an AI tool. The guidance is enforced in pre-commit hooks, IDE integrations, and CI. | 1 |
| **AC.3.2** | **Verify that** technical controls automatically strip sensitive material from any context window sent to an AI tool. Client-side redaction, approved context filters, and secret scanners with pre-prompt hooks all qualify. | 1 |
| **AC.3.3** | **Verify that** any externally sourced context being fed to an AI tool is treated as untrusted and screened for prompt injection before it reaches the prompt. Sources to cover: PR descriptions and comments, fork-supplied diffs, issue bodies, commit messages, third-party documentation, web search results, and MCP tool outputs. | 1 |
| **AC.3.4** | **Verify that** the AI tool enforces an instruction hierarchy, with system and developer messages taking precedence over untrusted repository content. This hierarchy has to hold across multi-turn conversations and tool-augmented workflows. | 1 |
| **AC.3.5** | **Verify that** input length controls stop untrusted PR or repository content from crowding system instructions or safety directives out of the effective context window. Oversized inputs are rejected outright. Silent truncation is not acceptable. | 2 |
| **AC.3.6** | **Verify that** prompts and AI responses are encrypted in transit and at rest, and retained per the data-classification policy. Tenants and projects are cryptographically separated from each other. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਲਿਖਤੀ ਮਾਰਗਦਰਸ਼ਨ AI ਟੂਲ ਨੂੰ ਭੇਜੇ ਜਾਂਦੇ ਕਿਸੇ ਵੀ prompt ਵਿੱਚ ਗੁਪਤ ਭੇਦ, ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ, PII, ਜਾਂ ਵਰਗੀਕ੍ਰਿਤ ਡਾਟਾ ਪਾਉਣ ਤੋਂ ਵਰਜਦਾ ਹੈ। ਇਹ ਮਾਰਗਦਰਸ਼ਨ pre-commit ਹੁੱਕਾਂ, IDE ਏਕੀਕਰਨਾਂ, ਅਤੇ CI ਵਿੱਚ ਲਾਗੂ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **AC.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਤਕਨੀਕੀ ਨਿਯੰਤਰਣ AI ਟੂਲ ਨੂੰ ਭੇਜੀ ਜਾਂਦੀ ਕਿਸੇ ਵੀ ਸੰਦਰਭ ਵਿੰਡੋ (context window) ਵਿੱਚੋਂ ਸੰਵੇਦਨਸ਼ੀਲ ਸਮੱਗਰੀ ਆਪਣੇ-ਆਪ ਹਟਾ ਦਿੰਦੇ ਹਨ। ਕਲਾਇੰਟ-ਪਾਸੇ ਦੀ ਰਿਡੈਕਸ਼ਨ, ਪ੍ਰਵਾਨਿਤ ਸੰਦਰਭ ਫ਼ਿਲਟਰ, ਅਤੇ prompt-ਤੋਂ-ਪਹਿਲਾਂ ਵਾਲੀਆਂ ਹੁੱਕਾਂ ਵਾਲੇ ਗੁਪਤ-ਭੇਦ ਸਕੈਨਰ — ਇਹ ਸਾਰੇ ਯੋਗ ਹਨ। | 1 |
| **AC.3.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਟੂਲ ਨੂੰ ਦਿੱਤੇ ਜਾ ਰਹੇ ਕਿਸੇ ਵੀ ਬਾਹਰੀ ਸਰੋਤ ਵਾਲੇ ਸੰਦਰਭ ਨੂੰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਮੰਨਿਆ ਜਾਂਦਾ ਹੈ ਅਤੇ prompt ਤੱਕ ਪਹੁੰਚਣ ਤੋਂ ਪਹਿਲਾਂ prompt ਇੰਜੈਕਸ਼ਨ ਲਈ ਛਾਣਿਆ ਜਾਂਦਾ ਹੈ। ਢੱਕੇ ਜਾਣ ਵਾਲੇ ਸਰੋਤ: PR ਵੇਰਵੇ ਅਤੇ ਟਿੱਪਣੀਆਂ, ਫ਼ੋਰਕ ਤੋਂ ਦਿੱਤੇ diff, ਮੁੱਦਿਆਂ ਦਾ ਮਜ਼ਮੂਨ, ਕਮਿਟ ਸੁਨੇਹੇ, ਤੀਜੀ-ਧਿਰ ਦਸਤਾਵੇਜ਼ੀਕਰਨ, ਵੈੱਬ ਖੋਜ ਨਤੀਜੇ, ਅਤੇ MCP ਟੂਲ ਆਊਟਪੁੱਟ। | 1 |
| **AC.3.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਟੂਲ ਇੱਕ ਹਦਾਇਤ ਲੜੀ-ਕ੍ਰਮ (instruction hierarchy) ਲਾਗੂ ਕਰਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਸਿਸਟਮ ਅਤੇ ਡਿਵੈਲਪਰ ਸੁਨੇਹਿਆਂ ਨੂੰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਰਿਪੌਜ਼ਟਰੀ ਸਮੱਗਰੀ ਉੱਤੇ ਪਹਿਲ ਮਿਲਦੀ ਹੈ। ਇਹ ਲੜੀ-ਕ੍ਰਮ ਬਹੁ-ਵਾਰੀ ਗੱਲਬਾਤਾਂ ਅਤੇ ਟੂਲ-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਵਰਕਫ਼ਲੋ ਵਿੱਚ ਵੀ ਕਾਇਮ ਰਹਿਣਾ ਚਾਹੀਦਾ ਹੈ। | 1 |
| **AC.3.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇਨਪੁੱਟ ਲੰਬਾਈ ਨਿਯੰਤਰਣ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ PR ਜਾਂ ਰਿਪੌਜ਼ਟਰੀ ਸਮੱਗਰੀ ਨੂੰ ਸਿਸਟਮ ਹਦਾਇਤਾਂ ਜਾਂ ਸਲਾਮਤੀ ਨਿਰਦੇਸ਼ਾਂ ਨੂੰ ਅਸਰਦਾਰ ਸੰਦਰਭ ਵਿੰਡੋ ਵਿੱਚੋਂ ਧੱਕ ਦੇਣ ਤੋਂ ਰੋਕਦੇ ਹਨ। ਲੋੜੋਂ ਵੱਡੇ ਇਨਪੁੱਟ ਸਿੱਧੇ ਰੱਦ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। ਚੁੱਪ-ਚਾਪ ਕਟੌਤੀ (truncation) ਪ੍ਰਵਾਨ ਨਹੀਂ ਹੈ। | 2 |
| **AC.3.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** prompt ਅਤੇ AI ਜਵਾਬ ਪ੍ਰਸਾਰਣ ਅਤੇ ਭੰਡਾਰਨ ਦੋਵਾਂ ਵਿੱਚ ਏਨਕ੍ਰਿਪਟ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ ਡਾਟਾ-ਵਰਗੀਕਰਨ ਨੀਤੀ ਅਨੁਸਾਰ ਧਾਰਨ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। ਟੈਨੈਂਟ ਅਤੇ ਪ੍ਰੋਜੈਕਟ ਇੱਕ-ਦੂਜੇ ਤੋਂ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਵੱਖ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.3.1:** OWASP LLM Top 10 (2025) LLM02 (Sensitive Information Disclosure); OWASP ASVS v5 V14 (Data Protection); ISO/IEC 27001:2022 A.8.12 (Data Leakage Prevention).
* **AC.3.2:** AISVS C2.2; OWASP LLM Top 10 (2025) LLM02; NIST SSDF PW.3.
* **AC.3.3:** AISVS C2.1; OWASP LLM Top 10 (2025) LLM01; OWASP Agentic Top 10 (2026) ASI06; MITRE ATLAS (Indirect prompt injection).
* **AC.3.4:** AISVS C2.1.2; OWASP LLM Top 10 (2025) LLM01; CISA Secure by Design.
* **AC.3.5:** OWASP LLM Top 10 (2025) LLM10; AISVS C2.1.4.
* **AC.3.6:** OWASP ASVS v5 V6 (Cryptography), V14 (Data Protection); ISO/IEC 27001:2022 A.8.24 (Use of Cryptography).

---

## AC.4 Validation of AI-Generated Code
## AC.4 AI ਦੁਆਰਾ ਤਿਆਰ ਕੋਡ ਦੀ ਪ੍ਰਮਾਣਿਕਤਾ

Catch the vulnerabilities AI output introduces. Fix them before the code reaches a merge or a deployment.

AI ਆਊਟਪੁੱਟ ਵੱਲੋਂ ਪੇਸ਼ ਕੀਤੀਆਂ ਕਮਜ਼ੋਰੀਆਂ ਨੂੰ ਫੜੋ। ਕੋਡ ਦੇ ਮਰਜ ਜਾਂ ਤੈਨਾਤੀ ਤੱਕ ਪਹੁੰਚਣ ਤੋਂ ਪਹਿਲਾਂ ਉਹਨਾਂ ਨੂੰ ਠੀਕ ਕਰੋ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.4.1** | **Verify that** AI-generated code always goes through code review by a qualified human engineer. The reviewer must not be the same identity that asked for the AI generation in the first place (separation of duties). And the AI agent itself does not count as the human reviewer. | 1 |
| **AC.4.2** | **Verify that** automated security testing runs on every pull request containing AI-generated code: SAST, IAST, DAST, secret scanning, IaC scanning, and SCA. Where the scanner supports them, AI-attribution-aware rules are turned on. | 2 |
| **AC.4.3** | **Verify that** pull requests containing AI-generated code are blocked from merging when an automated scan surfaces a critical security finding, defined as CVSS >= 9.0 or the equivalent threshold in the organization's vulnerability severity policy. Bypassing the block requires a written exception approved by an authorized human. | 2 |
| **AC.4.4** | **Verify that** security-critical files require an elevated review threshold when AI generated or modified them: two-person review, security-team sign-off, or stricter. Security-critical files here include authentication, authorization, and cryptography code; IAM policy; CI/CD workflow definitions; deployment manifests; and sandbox or network policy artifacts. | 2 |
| **AC.4.5** | **Verify that** differential fuzz testing or property-based tests cover the security-critical behaviors of AI-generated code: input validation, authorization logic, and deserialization safety. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.4.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਕੋਡ ਹਮੇਸ਼ਾ ਕਿਸੇ ਯੋਗ ਮਨੁੱਖੀ ਇੰਜੀਨੀਅਰ ਦੀ ਕੋਡ ਸਮੀਖਿਆ ਵਿੱਚੋਂ ਲੰਘਦਾ ਹੈ। ਸਮੀਖਿਅਕ ਉਹੀ ਪਛਾਣ ਲਾਜ਼ਮੀ ਤੌਰ 'ਤੇ ਨਹੀਂ ਹੋਣੀ ਚਾਹੀਦੀ ਜਿਸ ਨੇ ਪਹਿਲਾਂ AI ਤੋਂ ਕੋਡ ਤਿਆਰ ਕਰਵਾਇਆ ਸੀ (ਕਰਤੱਵਾਂ ਦੀ ਵੰਡ[^0x92-separation-of-duties], separation of duties)। ਅਤੇ AI ਏਜੰਟ ਆਪ ਮਨੁੱਖੀ ਸਮੀਖਿਅਕ ਵਜੋਂ ਨਹੀਂ ਗਿਣਿਆ ਜਾਂਦਾ। | 1 |
| **AC.4.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਕੋਡ ਵਾਲੀ ਹਰ ਪੁੱਲ ਰਿਕੁਐਸਟ[^0x92-pull-request] (pull request) ਉੱਤੇ ਸਵੈਚਾਲਿਤ ਸੁਰੱਖਿਆ ਟੈਸਟਿੰਗ ਚੱਲਦੀ ਹੈ: SAST, IAST, DAST, ਗੁਪਤ-ਭੇਦ ਸਕੈਨਿੰਗ, IaC ਸਕੈਨਿੰਗ, ਅਤੇ SCA। ਜਿੱਥੇ ਸਕੈਨਰ ਸਮਰਥਨ ਕਰਦਾ ਹੈ, ਉੱਥੇ AI-ਸਰੋਤ-ਨਿਰਧਾਰਨ ਨੂੰ ਪਛਾਣਨ ਵਾਲੇ ਨਿਯਮ ਚਾਲੂ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 2 |
| **AC.4.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਦੋਂ ਕੋਈ ਸਵੈਚਾਲਿਤ ਸਕੈਨ ਕੋਈ ਨਾਜ਼ੁਕ ਸੁਰੱਖਿਆ ਖੋਜ-ਨਤੀਜਾ ਸਾਹਮਣੇ ਲਿਆਉਂਦਾ ਹੈ — ਜਿਸ ਦੀ ਪਰਿਭਾਸ਼ਾ CVSS >= 9.0 ਜਾਂ ਸੰਸਥਾ ਦੀ ਕਮਜ਼ੋਰੀ-ਗੰਭੀਰਤਾ ਨੀਤੀ ਵਿਚਲਾ ਬਰਾਬਰ ਦਾ ਥ੍ਰੈਸ਼ਹੋਲਡ ਹੈ — ਤਾਂ AI ਦੁਆਰਾ ਤਿਆਰ ਕੋਡ ਵਾਲੀਆਂ ਪੁੱਲ ਰਿਕੁਐਸਟਾਂ ਨੂੰ ਮਰਜ ਹੋਣ ਤੋਂ ਰੋਕ ਦਿੱਤਾ ਜਾਂਦਾ ਹੈ। ਇਸ ਰੋਕ ਨੂੰ ਬਾਈਪਾਸ ਕਰਨ ਲਈ ਕਿਸੇ ਅਧਿਕਾਰਤ ਮਨੁੱਖ ਵੱਲੋਂ ਮਨਜ਼ੂਰ ਕੀਤੀ ਲਿਖਤੀ ਛੋਟ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ। | 2 |
| **AC.4.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਦੋਂ ਸੁਰੱਖਿਆ-ਨਾਜ਼ੁਕ ਫ਼ਾਈਲਾਂ AI ਨੇ ਤਿਆਰ ਜਾਂ ਸੋਧੀਆਂ ਹੋਣ, ਤਾਂ ਉਹਨਾਂ ਲਈ ਉੱਚਾ ਸਮੀਖਿਆ ਥ੍ਰੈਸ਼ਹੋਲਡ ਲਾਜ਼ਮੀ ਹੁੰਦਾ ਹੈ: ਦੋ-ਵਿਅਕਤੀ ਸਮੀਖਿਆ, ਸੁਰੱਖਿਆ-ਟੀਮ ਦੀ ਮਨਜ਼ੂਰੀ, ਜਾਂ ਇਸ ਤੋਂ ਵੀ ਸਖ਼ਤ। ਇੱਥੇ ਸੁਰੱਖਿਆ-ਨਾਜ਼ੁਕ ਫ਼ਾਈਲਾਂ ਵਿੱਚ ਪ੍ਰਮਾਣੀਕਰਨ, ਅਧਿਕਾਰੀਕਰਨ, ਅਤੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ੀ ਕੋਡ; IAM ਨੀਤੀ; CI/CD ਵਰਕਫ਼ਲੋ ਪਰਿਭਾਸ਼ਾਵਾਂ; ਤੈਨਾਤੀ ਮੈਨੀਫ਼ੈਸਟ; ਅਤੇ ਸੈਂਡਬਾਕਸ ਜਾਂ ਨੈੱਟਵਰਕ ਨੀਤੀ ਆਰਟੀਫ਼ੈਕਟ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **AC.4.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡਿਫ਼ਰੈਂਸ਼ੀਅਲ ਫ਼ਜ਼ ਟੈਸਟਿੰਗ (differential fuzz testing) ਜਾਂ ਵਿਸ਼ੇਸ਼ਤਾ-ਆਧਾਰਿਤ ਟੈਸਟ AI ਦੁਆਰਾ ਤਿਆਰ ਕੋਡ ਦੇ ਸੁਰੱਖਿਆ-ਨਾਜ਼ੁਕ ਵਿਵਹਾਰਾਂ ਨੂੰ ਢੱਕਦੇ ਹਨ: ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ, ਅਧਿਕਾਰੀਕਰਨ ਤਰਕ, ਅਤੇ ਡੀਸੀਰੀਅਲਾਈਜ਼ੇਸ਼ਨ ਸਲਾਮਤੀ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.4.1:** NIST SSDF PW.7; OWASP ASVS v5 V10 (Coding Quality); ISO/IEC 27001:2022 A.5.3 (Segregation of Duties).
* **AC.4.2:** NIST SP 800-204D (Pipeline scanning controls); SLSA v1.2 Build Track L2; OWASP SAMM Security Testing (ST).
* **AC.4.3:** OWASP CI/CD Top 10 CICD-SEC-04 (Poisoned Pipeline Execution); NIST SSDF PW.7, PW.8.
* **AC.4.4:** NIST SSDF PW.4, PW.7; OWASP CI/CD Top 10 CICD-SEC-01 (Insufficient Flow Control); ISO/IEC 27001:2022 A.8.32 (Change Management).
* **AC.4.5:** NIST SSDF PW.8; OWASP ASVS v5 V11 (Business Logic).

---

## AC.5 Explainability & Traceability of Code Suggestions
## AC.5 ਕੋਡ ਸੁਝਾਵਾਂ ਦੀ ਵਿਆਖਿਆਯੋਗਤਾ[^0x92-explainability] ਅਤੇ ਟਰੇਸਯੋਗਤਾ

Auditors, defenders, and the developers themselves need to be able to see why a given AI suggestion was made, and how it ended up in a shipped artifact.

ਆਡੀਟਰਾਂ, ਬਚਾਅ ਕਰਨ ਵਾਲਿਆਂ, ਅਤੇ ਖ਼ੁਦ ਡਿਵੈਲਪਰਾਂ ਨੂੰ ਇਹ ਦੇਖ ਸਕਣਾ ਚਾਹੀਦਾ ਹੈ ਕਿ ਕੋਈ ਖ਼ਾਸ AI ਸੁਝਾਅ ਕਿਉਂ ਦਿੱਤਾ ਗਿਆ ਸੀ, ਅਤੇ ਉਹ ਭੇਜੇ ਗਏ ਆਰਟੀਫ਼ੈਕਟ ਵਿੱਚ ਕਿਵੇਂ ਪਹੁੰਚਿਆ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.5.1** | **Verify that** prompt-and-response pairs are logged with stable correlation identifiers, so that an investigator can later replay the whole chain: prompt -> response -> commit -> build -> deployment. | 1 |
| **AC.5.2** | **Verify that** developers can pull up the citations (training snippets, retrieved documents, MCP tool outputs) that support a suggestion, and that the citation chain travels with the artifact. | 3 |
| **AC.5.3** | **Verify that** explainability reports, AI-event logs, and citation records are kept in tamper-evident storage (append-only, WORM, or an immutable log store) and are referenced during security reviews. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.5.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** prompt-ਅਤੇ-ਜਵਾਬ ਜੋੜੇ ਸਥਿਰ ਸਹਿ-ਸੰਬੰਧ ਪਛਾਣਕਰਤਾਵਾਂ ਨਾਲ ਲੌਗ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਤਾਂ ਜੋ ਕੋਈ ਤਫ਼ਤੀਸ਼ਕਾਰ ਬਾਅਦ ਵਿੱਚ ਪੂਰੀ ਲੜੀ ਮੁੜ ਚਲਾ ਸਕੇ: prompt -> ਜਵਾਬ -> ਕਮਿਟ -> ਬਿਲਡ -> ਤੈਨਾਤੀ। | 1 |
| **AC.5.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡਿਵੈਲਪਰ ਉਹ ਹਵਾਲੇ (ਸਿਖਲਾਈ ਦੇ ਟੁਕੜੇ, ਪ੍ਰਾਪਤ ਕੀਤੇ ਦਸਤਾਵੇਜ਼, MCP ਟੂਲ ਆਊਟਪੁੱਟ) ਸਾਹਮਣੇ ਲਿਆ ਸਕਦੇ ਹਨ ਜੋ ਕਿਸੇ ਸੁਝਾਅ ਦਾ ਆਧਾਰ ਬਣਦੇ ਹਨ, ਅਤੇ ਇਹ ਹਵਾਲਾ ਲੜੀ ਆਰਟੀਫ਼ੈਕਟ ਦੇ ਨਾਲ-ਨਾਲ ਸਫ਼ਰ ਕਰਦੀ ਹੈ। | 3 |
| **AC.5.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਵਿਆਖਿਆਯੋਗਤਾ ਰਿਪੋਰਟਾਂ, AI-ਘਟਨਾ ਲੌਗ, ਅਤੇ ਹਵਾਲਾ ਰਿਕਾਰਡ ਛੇੜਛਾੜ-ਪ੍ਰਗਟ[^0x92-tamper-evident] (tamper-evident) ਭੰਡਾਰਨ ਵਿੱਚ ਰੱਖੇ ਜਾਂਦੇ ਹਨ (ਸਿਰਫ਼-ਜੋੜਨਯੋਗ, WORM, ਜਾਂ ਕੋਈ ਅਪਰਿਵਰਤਨਸ਼ੀਲ ਲੌਗ ਸਟੋਰ) ਅਤੇ ਸੁਰੱਖਿਆ ਸਮੀਖਿਆਵਾਂ ਦੌਰਾਨ ਉਹਨਾਂ ਦਾ ਹਵਾਲਾ ਦਿੱਤਾ ਜਾਂਦਾ ਹੈ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.5.1:** ISO/IEC 42001 Clause 7.5 (Documented Information); OWASP ASVS v5 V8 (Logging); NIST SP 800-218A (Generative AI logging guidance).
* **AC.5.2:** NIST AI RMF MEASURE; OWASP LLM Top 10 (2025) LLM03.
* **AC.5.3:** ISO/IEC 27001:2022 A.8.15 (Logging); NIST AI 600-1 MEASURE; ISO/IEC 42001 (traceability).

---

## AC.6 Continuous Feedback, Adversarial Testing & Model Fine-Tuning
## AC.6 ਲਗਾਤਾਰ ਫ਼ੀਡਬੈਕ, ਵਿਰੋਧੀ ਟੈਸਟਿੰਗ, ਅਤੇ ਮਾਡਲ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ

Improve model security over time. Watch for negative drift. Keep red-teaming the AI tooling. The red-team scope in this family is the AI tooling itself; the underlying systems and services the tooling depends on are handled by separate programs.

ਸਮੇਂ ਦੇ ਨਾਲ ਮਾਡਲ ਦੀ ਸੁਰੱਖਿਆ ਬਿਹਤਰ ਬਣਾਓ। ਨਾਂਹ-ਪੱਖੀ ਡ੍ਰਿਫ਼ਟ (drift) ਉੱਤੇ ਨਜ਼ਰ ਰੱਖੋ। AI ਟੂਲਿੰਗ ਦੀ ਰੈੱਡ-ਟੀਮਿੰਗ[^0x92-red-teaming] (red-teaming) ਜਾਰੀ ਰੱਖੋ। ਇਸ ਪਰਿਵਾਰ ਵਿੱਚ ਰੈੱਡ-ਟੀਮ ਦਾ ਦਾਇਰਾ ਖ਼ੁਦ AI ਟੂਲਿੰਗ ਹੈ; ਜਿਨ੍ਹਾਂ ਹੇਠਲੇ ਸਿਸਟਮਾਂ ਅਤੇ ਸੇਵਾਵਾਂ ਉੱਤੇ ਇਹ ਟੂਲਿੰਗ ਨਿਰਭਰ ਕਰਦੀ ਹੈ, ਉਹਨਾਂ ਨੂੰ ਵੱਖਰੇ ਪ੍ਰੋਗਰਾਮ ਸੰਭਾਲਦੇ ਹਨ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.6.1** | **Verify that** developers and reviewers can flag insecure or non-compliant suggestions, and that each flag is tracked to closure with links back to the originating prompt and response and forward to any downstream artifacts. | 1 |
| **AC.6.2** | **Verify that** aggregated feedback feeds into periodic system-prompt updates or retrieval-augmented generation against vetted secure-coding corpora (OWASP Cheat Sheets, internal coding standards). Where the organization controls model training infrastructure, fine-tuning on the same feedback corpus is also required. | 2 |
| **AC.6.3** | **Verify that** scheduled red-team exercises target the AI tooling itself. The exercises include direct and indirect prompt-injection probes delivered through realistic PR, issue, and comment surfaces, jailbreak corpora, and supply-chain payload generation. Findings are remediated under tracked severity SLAs. | 2 |
| **AC.6.4** | **Verify that** a closed-loop evaluation harness runs regression tests after every fine-tune, system-prompt change, or model upgrade. Security metrics must meet or exceed the prior baseline before deployment. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.6.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡਿਵੈਲਪਰ ਅਤੇ ਸਮੀਖਿਅਕ ਗ਼ੈਰ-ਸੁਰੱਖਿਅਤ ਜਾਂ ਗ਼ੈਰ-ਅਨੁਕੂਲ ਸੁਝਾਵਾਂ ਨੂੰ ਨਿਸ਼ਾਨਬੱਧ ਕਰ ਸਕਦੇ ਹਨ, ਅਤੇ ਹਰ ਨਿਸ਼ਾਨਦੇਹੀ ਨੂੰ ਬੰਦ ਹੋਣ ਤੱਕ ਟਰੈਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਪਿੱਛੇ ਮੂਲ prompt ਤੇ ਜਵਾਬ ਅਤੇ ਅੱਗੇ ਕਿਸੇ ਵੀ ਡਾਊਨਸਟ੍ਰੀਮ ਆਰਟੀਫ਼ੈਕਟ ਤੱਕ ਦੇ ਲਿੰਕ ਹੁੰਦੇ ਹਨ। | 1 |
| **AC.6.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇਕੱਤਰ ਕੀਤਾ ਫ਼ੀਡਬੈਕ ਸਮੇਂ-ਸਮੇਂ ਸਿਰ ਸਿਸਟਮ-prompt ਅੱਪਡੇਟਾਂ ਵਿੱਚ, ਜਾਂ ਪਰਖੇ ਹੋਏ ਸੁਰੱਖਿਅਤ-ਕੋਡਿੰਗ ਕਾਰਪੋਰਾ (OWASP Cheat Sheets, ਅੰਦਰੂਨੀ ਕੋਡਿੰਗ ਮਿਆਰ) ਦੇ ਵਿਰੁੱਧ RAG (retrieval-augmented generation) ਵਿੱਚ ਪਾਇਆ ਜਾਂਦਾ ਹੈ। ਜਿੱਥੇ ਸੰਸਥਾ ਦਾ ਮਾਡਲ ਸਿਖਲਾਈ ਬੁਨਿਆਦੀ ਢਾਂਚੇ ਉੱਤੇ ਨਿਯੰਤਰਣ ਹੈ, ਉੱਥੇ ਉਸੇ ਫ਼ੀਡਬੈਕ ਕਾਰਪਸ ਉੱਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਵੀ ਲਾਜ਼ਮੀ ਹੈ। | 2 |
| **AC.6.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਮਾਂ-ਸਾਰਣੀ ਅਨੁਸਾਰ ਹੋਣ ਵਾਲੀਆਂ ਰੈੱਡ-ਟੀਮ ਮਸ਼ਕਾਂ ਦਾ ਨਿਸ਼ਾਨਾ ਖ਼ੁਦ AI ਟੂਲਿੰਗ ਹੁੰਦੀ ਹੈ। ਇਹਨਾਂ ਮਸ਼ਕਾਂ ਵਿੱਚ ਅਸਲੀਅਤ ਵਰਗੀਆਂ PR, ਮੁੱਦਾ, ਅਤੇ ਟਿੱਪਣੀ ਸਤ੍ਹਾਵਾਂ ਰਾਹੀਂ ਪਹੁੰਚਾਈਆਂ ਸਿੱਧੀਆਂ ਤੇ ਅਸਿੱਧੀਆਂ prompt ਇੰਜੈਕਸ਼ਨ ਪੜਤਾਲਾਂ, jailbreak ਕਾਰਪੋਰਾ, ਅਤੇ ਸਪਲਾਈ ਚੇਨ ਪੇਲੋਡ ਤਿਆਰੀ ਸ਼ਾਮਲ ਹਨ। ਖੋਜ-ਨਤੀਜਿਆਂ ਨੂੰ ਟਰੈਕ ਕੀਤੇ ਗੰਭੀਰਤਾ SLA ਦੇ ਅਧੀਨ ਦਰੁਸਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **AC.6.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਫ਼ਾਈਨ-ਟਿਊਨ, ਸਿਸਟਮ-prompt ਤਬਦੀਲੀ, ਜਾਂ ਮਾਡਲ ਅੱਪਗ੍ਰੇਡ ਤੋਂ ਬਾਅਦ ਇੱਕ ਬੰਦ-ਲੂਪ ਮੁਲਾਂਕਣ ਹਾਰਨੈੱਸ (closed-loop evaluation harness) ਰਿਗਰੈਸ਼ਨ ਟੈਸਟ ਚਲਾਉਂਦਾ ਹੈ। ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਸੁਰੱਖਿਆ ਮੈਟ੍ਰਿਕਸ ਦਾ ਪਿਛਲੀ ਬੇਸਲਾਈਨ ਦੇ ਬਰਾਬਰ ਜਾਂ ਉਸ ਤੋਂ ਉੱਤੇ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.6.1:** NIST AI RMF MANAGE; ISO/IEC 42001 Clause 10; OWASP SAMM Defect Management (DM).
* **AC.6.2:** OWASP LLM Top 10 (2025) LLM03; NIST SSDF PO.3.
* **AC.6.3:** MITRE ATLAS (Adversarial ML lifecycle); NIST AI 600-1 MEASURE 2.7; OWASP SAMM Security Testing (ST).
* **AC.6.4:** ISO/IEC 42001 Clause 9.1; NIST AI RMF MEASURE.

---

## AC.7 AI-Generated Infrastructure & Pipeline Artifacts
## AC.7 AI ਦੁਆਰਾ ਤਿਆਰ ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਅਤੇ ਪਾਈਪਲਾਈਨ ਆਰਟੀਫ਼ੈਕਟ

Infrastructure code, CI/CD workflow files, deployment manifests, and security policy artifacts each have outsized impact when they are wrong. When AI has generated them, the validation needs to be correspondingly stricter than for ordinary application code.

ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਕੋਡ, CI/CD ਵਰਕਫ਼ਲੋ ਫ਼ਾਈਲਾਂ, ਤੈਨਾਤੀ ਮੈਨੀਫ਼ੈਸਟ, ਅਤੇ ਸੁਰੱਖਿਆ ਨੀਤੀ ਆਰਟੀਫ਼ੈਕਟ — ਇਹਨਾਂ ਵਿੱਚੋਂ ਹਰੇਕ ਦੇ ਗ਼ਲਤ ਹੋਣ ਦਾ ਪ੍ਰਭਾਵ ਹੱਦੋਂ ਵੱਧ ਹੁੰਦਾ ਹੈ। ਜਦੋਂ ਇਹ AI ਨੇ ਤਿਆਰ ਕੀਤੇ ਹੋਣ, ਤਾਂ ਇਹਨਾਂ ਦੀ ਪ੍ਰਮਾਣਿਕਤਾ ਆਮ ਐਪਲੀਕੇਸ਼ਨ ਕੋਡ ਦੇ ਮੁਕਾਬਲੇ ਉਸੇ ਅਨੁਪਾਤ ਵਿੱਚ ਵਧੇਰੇ ਸਖ਼ਤ ਹੋਣੀ ਚਾਹੀਦੀ ਹੈ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.7.1** | **Verify that** AI-generated or AI-modified artifacts are clearly labeled and tracked as such. Artifact classes in scope include infrastructure-as-code (Terraform, CloudFormation, Pulumi, Bicep), CI/CD workflow files (GitHub Actions, GitLab CI, Jenkinsfile, Argo Workflows, Tekton), container and orchestration manifests (Dockerfile, Kubernetes, Helm), and security policy artifacts (IAM, OPA/Rego, NetworkPolicy, admission controllers). | 1 |
| **AC.7.2** | **Verify that** AI-generated infrastructure and pipeline configurations require human review and approval before they run in any environment beyond a hermetic sandbox. | 2 |
| **AC.7.3** | **Verify that** AI-generated infrastructure and workflow changes pass policy-as-code enforcement (OPA, Conftest, Checkov, tfsec, KICS, kube-linter) at the same level as, or stricter than, human-authored changes. Policy violations block promotion. | 2 |
| **AC.7.4** | **Verify that** changes to high-impact pipeline trigger configurations require both dual control and a security-team review, no matter who or what produced the change. The configurations in scope include GitHub Actions `pull_request_target` and `workflow_run`, self-hosted runner labels, workflow `permissions:` blocks, OIDC trust policies, and secret-environment mappings. | 2 |
| **AC.7.5** | **Verify that** drift detection compares deployed infrastructure and live workflow configurations against signed, AI-attributed baselines, and alerts on any unauthorized modification. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.7.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਜਾਂ AI ਦੁਆਰਾ ਸੋਧੇ ਆਰਟੀਫ਼ੈਕਟਾਂ ਉੱਤੇ ਸਪੱਸ਼ਟ ਲੇਬਲ ਲੱਗਦਾ ਹੈ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਉਸੇ ਤਰ੍ਹਾਂ ਟਰੈਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। ਦਾਇਰੇ ਵਿਚਲੀਆਂ ਆਰਟੀਫ਼ੈਕਟ ਸ਼੍ਰੇਣੀਆਂ ਵਿੱਚ infrastructure-as-code (Terraform, CloudFormation, Pulumi, Bicep), CI/CD ਵਰਕਫ਼ਲੋ ਫ਼ਾਈਲਾਂ (GitHub Actions, GitLab CI, Jenkinsfile, Argo Workflows, Tekton), ਕੰਟੇਨਰ ਅਤੇ ਆਰਕੈਸਟ੍ਰੇਸ਼ਨ ਮੈਨੀਫ਼ੈਸਟ (Dockerfile, Kubernetes, Helm), ਅਤੇ ਸੁਰੱਖਿਆ ਨੀਤੀ ਆਰਟੀਫ਼ੈਕਟ (IAM, OPA/Rego, NetworkPolicy, admission controllers) ਸ਼ਾਮਲ ਹਨ। | 1 |
| **AC.7.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਅਤੇ ਪਾਈਪਲਾਈਨ ਸੰਰਚਨਾਵਾਂ ਨੂੰ ਪੂਰੀ ਤਰ੍ਹਾਂ ਸੀਲਬੰਦ (hermetic) ਸੈਂਡਬਾਕਸ ਤੋਂ ਬਾਹਰ ਕਿਸੇ ਵੀ ਵਾਤਾਵਰਣ ਵਿੱਚ ਚੱਲਣ ਤੋਂ ਪਹਿਲਾਂ ਮਨੁੱਖੀ ਸਮੀਖਿਆ ਅਤੇ ਮਨਜ਼ੂਰੀ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ। | 2 |
| **AC.7.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਅਤੇ ਵਰਕਫ਼ਲੋ ਤਬਦੀਲੀਆਂ ਕੋਡ-ਵਜੋਂ-ਨੀਤੀ[^0x92-policy-as-code] (policy-as-code) ਲਾਗੂਕਰਨ (OPA, Conftest, Checkov, tfsec, KICS, kube-linter) ਨੂੰ ਮਨੁੱਖ-ਲਿਖਤ ਤਬਦੀਲੀਆਂ ਦੇ ਬਰਾਬਰ ਜਾਂ ਉਸ ਤੋਂ ਸਖ਼ਤ ਪੱਧਰ ਉੱਤੇ ਪਾਸ ਕਰਦੀਆਂ ਹਨ। ਨੀਤੀ ਦੀਆਂ ਉਲੰਘਣਾਵਾਂ ਤਰੱਕੀ ਨੂੰ ਰੋਕ ਦਿੰਦੀਆਂ ਹਨ। | 2 |
| **AC.7.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੀਆਂ ਪਾਈਪਲਾਈਨ ਟ੍ਰਿਗਰ ਸੰਰਚਨਾਵਾਂ ਵਿੱਚ ਤਬਦੀਲੀਆਂ ਲਈ ਦੋਹਰਾ ਨਿਯੰਤਰਣ[^0x92-dual-control] (dual control) ਅਤੇ ਸੁਰੱਖਿਆ-ਟੀਮ ਦੀ ਸਮੀਖਿਆ ਦੋਵੇਂ ਲਾਜ਼ਮੀ ਹਨ, ਭਾਵੇਂ ਤਬਦੀਲੀ ਕਿਸੇ ਨੇ ਵੀ ਜਾਂ ਕਿਸੇ ਵੀ ਚੀਜ਼ ਨੇ ਕੀਤੀ ਹੋਵੇ। ਦਾਇਰੇ ਵਿਚਲੀਆਂ ਸੰਰਚਨਾਵਾਂ ਵਿੱਚ GitHub Actions ਦੇ `pull_request_target` ਅਤੇ `workflow_run`, ਸਵੈ-ਹੋਸਟ ਕੀਤੇ ਰਨਰ[^0x92-runner] ਲੇਬਲ, ਵਰਕਫ਼ਲੋ ਦੇ `permissions:` ਬਲਾਕ, OIDC ਭਰੋਸਾ ਨੀਤੀਆਂ, ਅਤੇ ਗੁਪਤ-ਭੇਦ ਤੋਂ ਵਾਤਾਵਰਣ ਦੀਆਂ ਮੈਪਿੰਗਾਂ ਸ਼ਾਮਲ ਹਨ। | 2 |
| **AC.7.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡ੍ਰਿਫ਼ਟ ਪਛਾਣ ਤੈਨਾਤ ਬੁਨਿਆਦੀ ਢਾਂਚੇ ਅਤੇ ਜਿਊਂਦੀਆਂ ਵਰਕਫ਼ਲੋ ਸੰਰਚਨਾਵਾਂ ਦੀ ਤੁਲਨਾ ਦਸਤਖ਼ਤ ਕੀਤੀਆਂ, AI ਨੂੰ ਸਰੋਤ-ਨਿਰਧਾਰਿਤ ਬੇਸਲਾਈਨਾਂ ਨਾਲ ਕਰਦੀ ਹੈ, ਅਤੇ ਕਿਸੇ ਵੀ ਅਣਅਧਿਕਾਰਤ ਸੋਧ ਉੱਤੇ ਚੇਤਾਵਨੀ ਦਿੰਦੀ ਹੈ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.7.1:** OWASP CI/CD Top 10 CICD-SEC-05 (Insufficient PBAC); SLSA v1.2 Build Track provenance; NIST SSDF PW.1.
* **AC.7.2:** NIST SP 800-204D (Approval gating); OWASP CI/CD Top 10 CICD-SEC-01; ISO/IEC 27001:2022 A.8.32 (Change Management).
* **AC.7.3:** OWASP ASVS v5 V10 (CI/CD Deployment Security); OWASP CI/CD Top 10 CICD-SEC-07 (Insecure System Configuration); NIST SSDF PW.4.
* **AC.7.4:** OWASP CI/CD Top 10 CICD-SEC-01, CICD-SEC-02; GitHub Security Lab "Preventing pwn requests" series; NIST SP 800-204D (Pipeline governance).
* **AC.7.5:** NIST SP 800-204D (Continuous monitoring); ISO/IEC 27001:2022 A.8.19.

---

## AC.8 Autonomous Agent Change Control Constraints
## AC.8 ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਏਜੰਟ ਤਬਦੀਲੀ-ਨਿਯੰਤਰਣ ਪਾਬੰਦੀਆਂ

Autonomous AI agents that generate code or configuration get the same separation-of-duties treatment that humans do. They cannot approve, merge, or promote their own work. This applies at the policy layer and at the technical layer.

ਕੋਡ ਜਾਂ ਸੰਰਚਨਾ ਤਿਆਰ ਕਰਨ ਵਾਲੇ ਖ਼ੁਦਮੁਖ਼ਤਾਰ AI ਏਜੰਟਾਂ ਨਾਲ ਕਰਤੱਵਾਂ ਦੀ ਵੰਡ ਦਾ ਉਹੀ ਸਲੂਕ ਹੁੰਦਾ ਹੈ ਜੋ ਮਨੁੱਖਾਂ ਨਾਲ ਹੁੰਦਾ ਹੈ। ਉਹ ਆਪਣੇ ਹੀ ਕੰਮ ਨੂੰ ਮਨਜ਼ੂਰੀ ਨਹੀਂ ਦੇ ਸਕਦੇ, ਮਰਜ ਨਹੀਂ ਕਰ ਸਕਦੇ, ਜਾਂ ਤਰੱਕੀ ਨਹੀਂ ਦੇ ਸਕਦੇ। ਇਹ ਗੱਲ ਨੀਤੀ ਪਰਤ ਉੱਤੇ ਵੀ ਲਾਗੂ ਹੁੰਦੀ ਹੈ ਅਤੇ ਤਕਨੀਕੀ ਪਰਤ ਉੱਤੇ ਵੀ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.8.1** | **Verify that** autonomous agents cannot approve, merge, sign, or deploy artifacts that they themselves generated, and that this constraint is enforced by the source-control system, the CI system, and the artifact registry. Policy alone does not satisfy this control. | 1 |
| **AC.8.2** | **Verify that** AI systems run with scoped, non-human identities (service accounts, workload identities, OIDC-issued ephemeral tokens), and that those identities cannot be used to promote their own generated artifacts across environments. | 2 |
| **AC.8.3** | **Verify that** autonomous agents cannot bypass branch protection, required reviews, required status checks, signed-commit requirements, or merge queues. Any attempt by an agent to change these settings raises a security alert. | 2 |
| **AC.8.4** | **Verify that** separation of duties holds across the stages of an AI-generated change. Each stage (generation, review, approval, deployment) is performed by a distinct principal, whether human or system. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.8.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਏਜੰਟ ਉਹਨਾਂ ਆਰਟੀਫ਼ੈਕਟਾਂ ਨੂੰ ਮਨਜ਼ੂਰੀ ਨਹੀਂ ਦੇ ਸਕਦੇ, ਮਰਜ ਨਹੀਂ ਕਰ ਸਕਦੇ, ਦਸਤਖ਼ਤ ਨਹੀਂ ਕਰ ਸਕਦੇ, ਜਾਂ ਤੈਨਾਤ ਨਹੀਂ ਕਰ ਸਕਦੇ ਜੋ ਉਹਨਾਂ ਨੇ ਆਪ ਤਿਆਰ ਕੀਤੇ ਸਨ, ਅਤੇ ਇਹ ਪਾਬੰਦੀ ਸਰੋਤ-ਨਿਯੰਤਰਣ ਸਿਸਟਮ, CI ਸਿਸਟਮ, ਅਤੇ ਆਰਟੀਫ਼ੈਕਟ ਰਜਿਸਟਰੀ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਇਕੱਲੀ ਨੀਤੀ ਇਸ ਨਿਯੰਤਰਣ ਨੂੰ ਪੂਰਾ ਨਹੀਂ ਕਰਦੀ। | 1 |
| **AC.8.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਸਿਸਟਮ ਸੀਮਿਤ ਦਾਇਰੇ ਵਾਲੀਆਂ, ਗ਼ੈਰ-ਮਨੁੱਖੀ ਪਛਾਣਾਂ (ਸੇਵਾ ਖਾਤੇ, ਵਰਕਲੋਡ ਪਛਾਣਾਂ, OIDC ਦੁਆਰਾ ਜਾਰੀ ਥੋੜ੍ਹ-ਚਿਰੇ ਟੋਕਨ) ਨਾਲ ਚੱਲਦੇ ਹਨ, ਅਤੇ ਇਹ ਪਛਾਣਾਂ ਆਪਣੇ ਹੀ ਤਿਆਰ ਕੀਤੇ ਆਰਟੀਫ਼ੈਕਟਾਂ ਨੂੰ ਵਾਤਾਵਰਣਾਂ ਵਿਚਕਾਰ ਤਰੱਕੀ ਦੇਣ ਲਈ ਨਹੀਂ ਵਰਤੀਆਂ ਜਾ ਸਕਦੀਆਂ। | 2 |
| **AC.8.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਏਜੰਟ ਬ੍ਰਾਂਚ ਸੁਰੱਖਿਆ, ਲੋੜੀਂਦੀਆਂ ਸਮੀਖਿਆਵਾਂ, ਲੋੜੀਂਦੀਆਂ ਸਥਿਤੀ ਜਾਂਚਾਂ, ਦਸਤਖ਼ਤ-ਕੀਤੇ-ਕਮਿਟ ਦੀਆਂ ਲੋੜਾਂ, ਜਾਂ ਮਰਜ ਕਤਾਰਾਂ ਨੂੰ ਬਾਈਪਾਸ ਨਹੀਂ ਕਰ ਸਕਦੇ। ਕਿਸੇ ਏਜੰਟ ਵੱਲੋਂ ਇਹ ਸੈਟਿੰਗਾਂ ਬਦਲਣ ਦੀ ਕੋਈ ਵੀ ਕੋਸ਼ਿਸ਼ ਸੁਰੱਖਿਆ ਚੇਤਾਵਨੀ ਪੈਦਾ ਕਰਦੀ ਹੈ। | 2 |
| **AC.8.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਕਿਸੇ ਤਬਦੀਲੀ ਦੇ ਸਾਰੇ ਪੜਾਵਾਂ ਵਿੱਚ ਕਰਤੱਵਾਂ ਦੀ ਵੰਡ ਕਾਇਮ ਰਹਿੰਦੀ ਹੈ। ਹਰ ਪੜਾਅ (ਤਿਆਰੀ, ਸਮੀਖਿਆ, ਮਨਜ਼ੂਰੀ, ਤੈਨਾਤੀ) ਇੱਕ ਵੱਖਰੀ ਪਛਾਣ-ਇਕਾਈ[^0x92-principal] (principal) ਦੁਆਰਾ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਭਾਵੇਂ ਉਹ ਮਨੁੱਖ ਹੋਵੇ ਜਾਂ ਸਿਸਟਮ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.8.1:** OWASP Agentic Top 10 (2026) ASI03 (Identity and Privilege Abuse), ASI10 (Rogue Agents); OWASP ASVS v5 V10; NIST SP 800-53r5 AC-5 (Separation of Duties).
* **AC.8.2:** NIST SP 800-207 (Zero Trust Architecture); OWASP CI/CD Top 10 CICD-SEC-02; ISO/IEC 27001:2022 A.5.15 (Access Control).
* **AC.8.3:** OWASP CI/CD Top 10 CICD-SEC-01; GitHub Docs (Branch protection rules and rulesets); OWASP Agentic Top 10 (2026) ASI03.
* **AC.8.4:** NIST SSDF PO.2; ISO/IEC 27001:2022 A.5.3; NIST SP 800-53r5 AC-5.

---

## AC.9 AI Artifact Origin Validation for Deployment
## AC.9 ਤੈਨਾਤੀ ਲਈ AI ਆਰਟੀਫ਼ੈਕਟ ਮੂਲ ਦੀ ਪ੍ਰਮਾਣਿਕਤਾ

Deployment and promotion pipelines need to validate the cryptographic origin and the generation history of AI-generated artifacts. They do this before letting the artifact through.

ਤੈਨਾਤੀ ਅਤੇ ਤਰੱਕੀ ਪਾਈਪਲਾਈਨਾਂ ਨੂੰ AI ਦੁਆਰਾ ਤਿਆਰ ਆਰਟੀਫ਼ੈਕਟਾਂ ਦੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਮੂਲ ਅਤੇ ਤਿਆਰੀ ਇਤਿਹਾਸ ਨੂੰ ਪ੍ਰਮਾਣਿਤ ਕਰਨਾ ਪੈਂਦਾ ਹੈ। ਇਹ ਕੰਮ ਉਹ ਆਰਟੀਫ਼ੈਕਟ ਨੂੰ ਅੱਗੇ ਲੰਘਾਉਣ ਤੋਂ ਪਹਿਲਾਂ ਕਰਦੀਆਂ ਹਨ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.9.1** | **Verify that** AI-generated artifacts carry signed origin and generation metadata (in-toto or SLSA provenance attestations, AI BOM entries) identifying the AI system that produced them, the generation context, the humans involved, and the associated audit records. | 2 |
| **AC.9.2** | **Verify that** deployment pipelines check the presence, signature, and integrity of origin and generation metadata on AI-generated artifacts before promotion, using a trusted verifier (Sigstore/cosign, in-toto verification). | 3 |
| **AC.9.3** | **Verify that** artifacts are rejected at deployment and quarantined for review when they are missing required origin and generation information, signed by untrusted keys, or produced by an unapproved AI system or environment. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.9.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਆਰਟੀਫ਼ੈਕਟ ਦਸਤਖ਼ਤ ਕੀਤਾ ਮੂਲ ਅਤੇ ਤਿਆਰੀ ਮੈਟਾਡਾਟਾ (in-toto ਜਾਂ SLSA ਮੂਲ-ਸਰੋਤ ਅਟੈਸਟੇਸ਼ਨ, AI BOM ਇੰਦਰਾਜ) ਨਾਲ ਲੈ ਕੇ ਚੱਲਦੇ ਹਨ, ਜੋ ਉਹਨਾਂ ਨੂੰ ਪੈਦਾ ਕਰਨ ਵਾਲੇ AI ਸਿਸਟਮ, ਤਿਆਰੀ ਦੇ ਸੰਦਰਭ, ਸ਼ਾਮਲ ਮਨੁੱਖਾਂ, ਅਤੇ ਸੰਬੰਧਿਤ ਆਡਿਟ ਰਿਕਾਰਡਾਂ ਦੀ ਪਛਾਣ ਕਰਾਉਂਦਾ ਹੈ। | 2 |
| **AC.9.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਤੈਨਾਤੀ ਪਾਈਪਲਾਈਨਾਂ ਤਰੱਕੀ ਤੋਂ ਪਹਿਲਾਂ AI ਦੁਆਰਾ ਤਿਆਰ ਆਰਟੀਫ਼ੈਕਟਾਂ ਉੱਤੇ ਮੂਲ ਅਤੇ ਤਿਆਰੀ ਮੈਟਾਡਾਟਾ ਦੀ ਮੌਜੂਦਗੀ, ਦਸਤਖ਼ਤ, ਅਤੇ ਅਖੰਡਤਾ ਦੀ ਜਾਂਚ ਕਿਸੇ ਭਰੋਸੇਯੋਗ ਤਸਦੀਕਕਾਰ (Sigstore/cosign, in-toto ਤਸਦੀਕ) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕਰਦੀਆਂ ਹਨ। | 3 |
| **AC.9.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਿਹੜੇ ਆਰਟੀਫ਼ੈਕਟਾਂ ਵਿੱਚ ਲੋੜੀਂਦੀ ਮੂਲ ਅਤੇ ਤਿਆਰੀ ਜਾਣਕਾਰੀ ਗ਼ੈਰ-ਮੌਜੂਦ ਹੈ, ਜੋ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਕੁੰਜੀਆਂ ਨਾਲ ਦਸਤਖ਼ਤ ਕੀਤੇ ਗਏ ਹਨ, ਜਾਂ ਜੋ ਕਿਸੇ ਗ਼ੈਰ-ਪ੍ਰਵਾਨਿਤ AI ਸਿਸਟਮ ਜਾਂ ਵਾਤਾਵਰਣ ਨੇ ਪੈਦਾ ਕੀਤੇ ਹਨ, ਉਹਨਾਂ ਨੂੰ ਤੈਨਾਤੀ ਵੇਲੇ ਰੱਦ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਅਤੇ ਸਮੀਖਿਆ ਲਈ ਕੁਆਰੰਟੀਨ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.9.1:** SLSA v1.2 (Provenance attestations); CycloneDX ML-BOM; in-toto Attestation Framework.
* **AC.9.2:** SLSA v1.2 (Verification Summary Attestations); Sigstore/cosign (Signature verification); OWASP SCVS.
* **AC.9.3:** SLSA v1.2 (Verifier requirements); NIST SP 800-204D (Promotion gating).

---

## AC.10 Generation Audit Trail Completeness and Validation
## AC.10 ਤਿਆਰੀ ਆਡਿਟ ਟ੍ਰੇਲ ਦੀ ਸੰਪੂਰਨਤਾ ਅਤੇ ਪ੍ਰਮਾਣਿਕਤਾ

AI-generated artifacts need complete and consistent origin and generation records, validated before integration or deployment. The reason matters. Policy-based enforcement of origin tracking only works if the recorded information is itself complete and consistent. When records are missing fields, or when the fields they do have contradict each other, detections get missed and enforcement opens gaps. So origin tracking is treated as a first-class requirement here, and validated before an artifact is accepted.

AI ਦੁਆਰਾ ਤਿਆਰ ਆਰਟੀਫ਼ੈਕਟਾਂ ਲਈ ਸੰਪੂਰਨ ਅਤੇ ਇਕਸਾਰ ਮੂਲ ਤੇ ਤਿਆਰੀ ਰਿਕਾਰਡ ਲੋੜੀਂਦੇ ਹਨ, ਜਿਨ੍ਹਾਂ ਦੀ ਏਕੀਕਰਨ ਜਾਂ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਪ੍ਰਮਾਣਿਕਤਾ ਕੀਤੀ ਜਾਵੇ। ਇਸ ਦਾ ਕਾਰਨ ਮਹੱਤਵ ਰੱਖਦਾ ਹੈ। ਮੂਲ-ਟਰੈਕਿੰਗ ਦਾ ਨੀਤੀ-ਆਧਾਰਿਤ ਲਾਗੂਕਰਨ ਉਦੋਂ ਹੀ ਕੰਮ ਕਰਦਾ ਹੈ ਜਦੋਂ ਦਰਜ ਕੀਤੀ ਜਾਣਕਾਰੀ ਖ਼ੁਦ ਸੰਪੂਰਨ ਅਤੇ ਇਕਸਾਰ ਹੋਵੇ। ਜਦੋਂ ਰਿਕਾਰਡਾਂ ਵਿੱਚ ਖੇਤਰ ਗ਼ੈਰ-ਮੌਜੂਦ ਹੋਣ, ਜਾਂ ਜਿਹੜੇ ਖੇਤਰ ਮੌਜੂਦ ਹਨ ਉਹ ਇੱਕ-ਦੂਜੇ ਦਾ ਖੰਡਨ ਕਰਦੇ ਹੋਣ, ਤਾਂ ਪਛਾਣਾਂ ਖੁੰਝ ਜਾਂਦੀਆਂ ਹਨ ਅਤੇ ਲਾਗੂਕਰਨ ਵਿੱਚ ਪਾੜੇ ਖੁੱਲ੍ਹ ਜਾਂਦੇ ਹਨ। ਇਸੇ ਲਈ ਇੱਥੇ ਮੂਲ-ਟਰੈਕਿੰਗ ਨੂੰ ਪਹਿਲੇ ਦਰਜੇ ਦੀ ਲੋੜ ਵਜੋਂ ਲਿਆ ਜਾਂਦਾ ਹੈ, ਅਤੇ ਕਿਸੇ ਆਰਟੀਫ਼ੈਕਟ ਨੂੰ ਸਵੀਕਾਰ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਇਸ ਦੀ ਪ੍ਰਮਾਣਿਕਤਾ ਕੀਤੀ ਜਾਂਦੀ ਹੈ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.10.1** | **Verify that** AI-generated artifacts carry the required origin and generation fields: model identity and version, tool or agent identity, generation context, prompt hash, human involvement, session identifiers, and correlation IDs. | 1 |
| **AC.10.2** | **Verify that** origin and generation metadata is checked for completeness and consistency: no missing or ambiguous fields, values normalized to a single representation, and a signature chain that validates back to a trusted root. | 2 |
| **AC.10.3** | **Verify that** artifacts with incomplete, inconsistent, or unverifiable origin and generation metadata are rejected before merge or deployment, and that the rejection event is logged so trends can be tracked. Rejection happens on the verifier side, against the attestation or proof model defined in SLSA and the verification criteria in ISO/IEC 42001. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.10.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਦੁਆਰਾ ਤਿਆਰ ਆਰਟੀਫ਼ੈਕਟ ਲੋੜੀਂਦੇ ਮੂਲ ਅਤੇ ਤਿਆਰੀ ਖੇਤਰ ਨਾਲ ਲੈ ਕੇ ਚੱਲਦੇ ਹਨ: ਮਾਡਲ ਦੀ ਪਛਾਣ ਤੇ ਵਰਜ਼ਨ, ਟੂਲ ਜਾਂ ਏਜੰਟ ਦੀ ਪਛਾਣ, ਤਿਆਰੀ ਦਾ ਸੰਦਰਭ, prompt ਹੈਸ਼, ਮਨੁੱਖੀ ਸ਼ਮੂਲੀਅਤ, ਸੈਸ਼ਨ ਪਛਾਣਕਰਤਾ, ਅਤੇ ਸਹਿ-ਸੰਬੰਧ ID। | 1 |
| **AC.10.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮੂਲ ਅਤੇ ਤਿਆਰੀ ਮੈਟਾਡਾਟੇ ਦੀ ਸੰਪੂਰਨਤਾ ਅਤੇ ਇਕਸਾਰਤਾ ਲਈ ਜਾਂਚ ਕੀਤੀ ਜਾਂਦੀ ਹੈ: ਕੋਈ ਗ਼ੈਰ-ਮੌਜੂਦ ਜਾਂ ਦੁਵਿਧਾਪੂਰਨ ਖੇਤਰ ਨਾ ਹੋਵੇ, ਮੁੱਲ ਇੱਕੋ ਪ੍ਰਤੀਨਿਧਤਾ ਵਿੱਚ ਸਧਾਰਨੀਕ੍ਰਿਤ ਹੋਣ, ਅਤੇ ਦਸਤਖ਼ਤ ਲੜੀ ਪਿੱਛੇ ਕਿਸੇ ਭਰੋਸੇਯੋਗ ਰੂਟ ਤੱਕ ਪ੍ਰਮਾਣਿਤ ਹੁੰਦੀ ਹੋਵੇ। | 2 |
| **AC.10.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਅਧੂਰੇ, ਬੇਮੇਲ, ਜਾਂ ਤਸਦੀਕ ਨਾ ਕੀਤੇ ਜਾ ਸਕਣ ਵਾਲੇ ਮੂਲ ਤੇ ਤਿਆਰੀ ਮੈਟਾਡਾਟੇ ਵਾਲੇ ਆਰਟੀਫ਼ੈਕਟ ਮਰਜ ਜਾਂ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਰੱਦ ਕੀਤੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ ਰੱਦਗੀ ਦੀ ਘਟਨਾ ਲੌਗ ਕੀਤੀ ਜਾਂਦੀ ਹੈ ਤਾਂ ਜੋ ਰੁਝਾਨ ਟਰੈਕ ਕੀਤੇ ਜਾ ਸਕਣ। ਰੱਦਗੀ ਤਸਦੀਕਕਾਰ ਵਾਲੇ ਪਾਸੇ ਹੁੰਦੀ ਹੈ, SLSA ਵਿੱਚ ਪਰਿਭਾਸ਼ਿਤ ਅਟੈਸਟੇਸ਼ਨ ਜਾਂ ਸਬੂਤ ਮਾਡਲ ਅਤੇ ISO/IEC 42001 ਦੇ ਤਸਦੀਕ ਮਾਪਦੰਡਾਂ ਦੇ ਵਿਰੁੱਧ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.10.1:** CycloneDX ML-BOM schema; NIST SP 800-218A (Generative AI provenance); ISO/IEC 42001 Clause 7.5.
* **AC.10.2:** OWASP SCVS (Provenance and Pedigree); SLSA v1.2 VSA verification.
* **AC.10.3:** SLSA v1.2 (Verifier-side enforcement); ISO/IEC 42001 Clause 9.

---

## AC.11 AI Code-Review & Assistant Bot Hardening
## AC.11 AI ਕੋਡ-ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟਾਂ[^0x92-bot] ਦਾ ਸਖ਼ਤੀਕਰਨ

AI code-review bots, PR-comment bots, MCP-driven assistants (Model Context Protocol), and IDE copilots are all reachable through untrusted repository content. The reachable surfaces include PR diffs, descriptions, comments, issues, and any workflow files supplied from a fork. This family covers the case where an attacker uses one of those surfaces to push a defender's own AI agent into approving, ignoring, or actively assisting a supply-chain attack.

AI ਕੋਡ-ਸਮੀਖਿਆ ਬੋਟ, PR-ਟਿੱਪਣੀ ਬੋਟ, MCP-ਚਾਲਿਤ ਸਹਾਇਕ (Model Context Protocol), ਅਤੇ IDE ਕੋਪਾਇਲਟ — ਇਹ ਸਾਰੇ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਰਿਪੌਜ਼ਟਰੀ ਸਮੱਗਰੀ ਰਾਹੀਂ ਪਹੁੰਚਯੋਗ ਹਨ। ਪਹੁੰਚਯੋਗ ਸਤ੍ਹਾਵਾਂ ਵਿੱਚ PR diff, ਵੇਰਵੇ, ਟਿੱਪਣੀਆਂ, ਮੁੱਦੇ, ਅਤੇ ਕਿਸੇ ਫ਼ੋਰਕ ਤੋਂ ਦਿੱਤੀਆਂ ਕੋਈ ਵੀ ਵਰਕਫ਼ਲੋ ਫ਼ਾਈਲਾਂ ਸ਼ਾਮਲ ਹਨ। ਇਹ ਪਰਿਵਾਰ ਉਸ ਮਾਮਲੇ ਨੂੰ ਢੱਕਦਾ ਹੈ ਜਿੱਥੇ ਹਮਲਾਵਰ ਇਹਨਾਂ ਵਿੱਚੋਂ ਕਿਸੇ ਸਤ੍ਹਾ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਬਚਾਅ ਕਰਨ ਵਾਲੇ ਦੇ ਆਪਣੇ ਹੀ AI ਏਜੰਟ ਨੂੰ ਕਿਸੇ ਸਪਲਾਈ ਚੇਨ ਹਮਲੇ ਨੂੰ ਮਨਜ਼ੂਰੀ ਦੇਣ, ਅਣਡਿੱਠ ਕਰਨ, ਜਾਂ ਸਰਗਰਮੀ ਨਾਲ ਉਸ ਵਿੱਚ ਸਹਾਇਤਾ ਕਰਨ ਵੱਲ ਧੱਕ ਦਿੰਦਾ ਹੈ।

> **Relationship to AISVS C2.1, C9.3, and C9.5:** AC.11.1 through AC.11.5 are applications of three AISVS chapter controls to the specific case of AI code-review and assistant bots operating over untrusted PR content. The three chapter controls are C2.1 (Prompt Injection Defenses), C9.3 (Component Isolation and Tool Authorization), and C9.5 (Agent Authorization, Delegation, and Continuous Enforcement). The appendix restates each one with bot-specific guidance. Counting rule is the same as elsewhere: a finding here is either an additional gap that the upstream chapter did not close, or it is already counted under the chapter. Not both.

> **AISVS C2.1, C9.3, ਅਤੇ C9.5 ਨਾਲ ਸੰਬੰਧ:** AC.11.1 ਤੋਂ AC.11.5 ਤੱਕ ਤਿੰਨ AISVS ਅਧਿਆਇ ਨਿਯੰਤਰਣਾਂ ਦੇ ਉਸ ਖ਼ਾਸ ਮਾਮਲੇ ਉੱਤੇ ਲਾਗੂਕਰਨ ਹਨ ਜਿੱਥੇ AI ਕੋਡ-ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ PR ਸਮੱਗਰੀ ਉੱਤੇ ਕੰਮ ਕਰਦੇ ਹਨ। ਉਹ ਤਿੰਨ ਅਧਿਆਇ ਨਿਯੰਤਰਣ ਹਨ C2.1 (Prompt Injection Defenses), C9.3 (Component Isolation and Tool Authorization), ਅਤੇ C9.5 (Agent Authorization, Delegation, and Continuous Enforcement)। ਇਹ ਅੰਤਿਕਾ ਹਰੇਕ ਨੂੰ ਬੋਟ-ਵਿਸ਼ੇਸ਼ ਮਾਰਗਦਰਸ਼ਨ ਨਾਲ ਦੁਬਾਰਾ ਬਿਆਨ ਕਰਦੀ ਹੈ। ਗਿਣਤੀ ਦਾ ਨਿਯਮ ਬਾਕੀ ਥਾਵਾਂ ਵਾਲਾ ਹੀ ਹੈ: ਇੱਥੋਂ ਦਾ ਖੋਜ-ਨਤੀਜਾ ਜਾਂ ਤਾਂ ਇੱਕ ਵਾਧੂ ਪਾੜਾ ਹੈ ਜਿਸ ਨੂੰ ਉੱਪਰਲੇ ਅਧਿਆਇ ਨੇ ਬੰਦ ਨਹੀਂ ਕੀਤਾ, ਜਾਂ ਉਹ ਪਹਿਲਾਂ ਹੀ ਉਸ ਅਧਿਆਇ ਹੇਠ ਗਿਣਿਆ ਜਾ ਚੁੱਕਾ ਹੈ। ਦੋਵੇਂ ਨਹੀਂ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.11.1** | **Verify that** AI review and assistant bots treat every piece of PR-supplied content (diff, title, description, comments, file contents, commit messages, linked external URLs) as untrusted input, and apply the AISVS C2.1 prompt-injection defenses: instruction-hierarchy enforcement, content sanitization, and indirect-injection detection. | 1 |
| **AC.11.2** | **Verify that** AI review and assistant bot system prompts and policy configurations are integrity-checked at load time (signed, hash-pinned), and that nothing in the repository, in branch contents, in PR-sourced environment variables, or in any other user-controllable input can modify them. | 1 |
| **AC.11.3** | **Verify that** AI review and assistant bots emit only structured, schema-validated output (JSON with an allow-list of fields and actions). Any free-form output is treated as untrusted and never executed as a command, a query, a shell snippet, or a workflow step. | 1 |
| **AC.11.4** | **Verify that** AI review and assistant bots run in network-isolated, least-privilege sandboxes: a dedicated namespace, default-deny egress with an allow-list to approved APIs only, no mounted repository secrets, and ephemeral credentials only. | 2 |
| **AC.11.5** | **Verify that** any privileged action a bot can take (approving a PR, merging, labeling, dismissing reviews, posting comments outside its sandbox, invoking external tools) goes through a separate, audited authorization path. That path is adjudicated by a policy engine, not by the LLM. | 2 |
| **AC.11.6** | **Verify that** AI review and assistant bots log all prompts (including externally sourced context), tool calls, and outputs to tamper-evident storage. Egress patterns (URLs, IPs, DNS, payload sizes) are continuously monitored for exfiltration indicators, with alerting tuned for webhook, paste-site, and bin-service destinations. | 2 |
| **AC.11.7** | **Verify that** AI review bots run in a zero-privilege, read-only shadow mode for untrusted fork PRs. In shadow mode, inline code-generation commentary is restricted and privileged workflow interaction is forbidden, until a repository maintainer has cleared an initial first-time-contributor verification gate. | 2 |
| **AC.11.8** | **Verify that** AI review and assistant bots are subject to continuous adversarial testing: indirect-prompt-injection corpora are replayed against the bot through simulated PRs, issues, and comments. Detection effectiveness is tracked over time, and a regression blocks the model or prompt update that caused it. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.11.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟ PR ਤੋਂ ਆਈ ਹਰ ਸਮੱਗਰੀ (diff, ਸਿਰਲੇਖ, ਵੇਰਵਾ, ਟਿੱਪਣੀਆਂ, ਫ਼ਾਈਲ ਸਮੱਗਰੀ, ਕਮਿਟ ਸੁਨੇਹੇ, ਲਿੰਕ ਕੀਤੇ ਬਾਹਰੀ URL) ਨੂੰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟ ਵਜੋਂ ਲੈਂਦੇ ਹਨ, ਅਤੇ AISVS C2.1 ਦੇ prompt ਇੰਜੈਕਸ਼ਨ ਬਚਾਅ ਲਾਗੂ ਕਰਦੇ ਹਨ: ਹਦਾਇਤ ਲੜੀ-ਕ੍ਰਮ ਦਾ ਲਾਗੂਕਰਨ, ਸਮੱਗਰੀ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ[^0x92-sanitization], ਅਤੇ ਅਸਿੱਧੇ-ਇੰਜੈਕਸ਼ਨ ਦੀ ਪਛਾਣ। | 1 |
| **AC.11.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟਾਂ ਦੇ ਸਿਸਟਮ prompt ਅਤੇ ਨੀਤੀ ਸੰਰਚਨਾਵਾਂ ਦੀ ਲੋਡ ਹੋਣ ਵੇਲੇ ਅਖੰਡਤਾ ਜਾਂਚ ਕੀਤੀ ਜਾਂਦੀ ਹੈ (ਦਸਤਖ਼ਤ ਕੀਤੇ, ਹੈਸ਼-ਪਿੰਨ ਕੀਤੇ), ਅਤੇ ਰਿਪੌਜ਼ਟਰੀ ਵਿਚਲੀ ਕੋਈ ਚੀਜ਼, ਬ੍ਰਾਂਚ ਦੀ ਸਮੱਗਰੀ, PR ਤੋਂ ਆਏ ਵਾਤਾਵਰਣ ਵੇਰੀਏਬਲ, ਜਾਂ ਕੋਈ ਹੋਰ ਵਰਤੋਂਕਾਰ-ਨਿਯੰਤਰਿਤ ਇਨਪੁੱਟ ਉਹਨਾਂ ਨੂੰ ਸੋਧ ਨਹੀਂ ਸਕਦਾ। | 1 |
| **AC.11.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟ ਸਿਰਫ਼ ਢਾਂਚਾਗਤ, ਸਕੀਮਾ-ਪ੍ਰਮਾਣਿਤ ਆਊਟਪੁੱਟ ਹੀ ਦਿੰਦੇ ਹਨ (ਖੇਤਰਾਂ ਅਤੇ ਕਾਰਵਾਈਆਂ ਦੀ ਇਜਾਜ਼ਤ-ਸੂਚੀ ਵਾਲਾ JSON)। ਕਿਸੇ ਵੀ ਖੁੱਲ੍ਹੇ-ਰੂਪ ਆਊਟਪੁੱਟ ਨੂੰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਮੰਨਿਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਉਸ ਨੂੰ ਕਦੇ ਵੀ ਕਮਾਂਡ, ਕਿਊਰੀ, ਸ਼ੈੱਲ ਟੁਕੜੇ, ਜਾਂ ਵਰਕਫ਼ਲੋ ਪੜਾਅ ਵਜੋਂ ਨਹੀਂ ਚਲਾਇਆ ਜਾਂਦਾ। | 1 |
| **AC.11.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟ ਨੈੱਟਵਰਕ-ਪੱਖੋਂ ਅਲੱਗ-ਥਲੱਗ, ਘੱਟੋ-ਘੱਟ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਸੈਂਡਬਾਕਸਾਂ ਵਿੱਚ ਚੱਲਦੇ ਹਨ: ਇੱਕ ਸਮਰਪਿਤ ਨੇਮਸਪੇਸ, ਮੂਲ-ਰੂਪ-ਵਿੱਚ-ਇਨਕਾਰ ਵਾਲਾ ਬਾਹਰ ਜਾਣ ਵਾਲਾ ਟਰੈਫ਼ਿਕ (egress) ਜਿਸ ਵਿੱਚ ਸਿਰਫ਼ ਪ੍ਰਵਾਨਿਤ API ਦੀ ਇਜਾਜ਼ਤ-ਸੂਚੀ ਹੋਵੇ, ਕੋਈ ਮਾਊਂਟ ਕੀਤੇ ਰਿਪੌਜ਼ਟਰੀ ਗੁਪਤ ਭੇਦ ਨਾ ਹੋਣ, ਅਤੇ ਸਿਰਫ਼ ਥੋੜ੍ਹ-ਚਿਰੇ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਹੋਣ। | 2 |
| **AC.11.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕੋਈ ਬੋਟ ਜੋ ਵੀ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲੀ ਕਾਰਵਾਈ ਕਰ ਸਕਦਾ ਹੈ (ਕਿਸੇ PR ਨੂੰ ਮਨਜ਼ੂਰੀ ਦੇਣਾ, ਮਰਜ ਕਰਨਾ, ਲੇਬਲ ਲਾਉਣਾ, ਸਮੀਖਿਆਵਾਂ ਖ਼ਾਰਜ ਕਰਨਾ, ਆਪਣੇ ਸੈਂਡਬਾਕਸ ਤੋਂ ਬਾਹਰ ਟਿੱਪਣੀਆਂ ਪਾਉਣਾ, ਬਾਹਰੀ ਟੂਲ ਸੱਦਣਾ), ਉਹ ਇੱਕ ਵੱਖਰੇ, ਆਡਿਟ ਕੀਤੇ ਅਧਿਕਾਰੀਕਰਨ ਰਾਹ ਵਿੱਚੋਂ ਲੰਘਦੀ ਹੈ। ਉਸ ਰਾਹ ਦਾ ਨਿਬੇੜਾ ਇੱਕ ਨੀਤੀ ਇੰਜਣ ਕਰਦਾ ਹੈ, LLM ਨਹੀਂ। | 2 |
| **AC.11.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟ ਸਾਰੇ prompt (ਬਾਹਰੀ ਸਰੋਤ ਵਾਲੇ ਸੰਦਰਭ ਸਮੇਤ), ਟੂਲ ਸੱਦੇ, ਅਤੇ ਆਊਟਪੁੱਟ ਛੇੜਛਾੜ-ਪ੍ਰਗਟ ਭੰਡਾਰਨ ਵਿੱਚ ਲੌਗ ਕਰਦੇ ਹਨ। ਬਾਹਰ ਜਾਣ ਵਾਲੇ ਟਰੈਫ਼ਿਕ ਦੇ ਪੈਟਰਨਾਂ (URL, IP, DNS, ਪੇਲੋਡ ਆਕਾਰ) ਦੀ ਡਾਟਾ ਬਾਹਰ ਕੱਢਣ (exfiltration) ਦੇ ਸੰਕੇਤਾਂ ਲਈ ਲਗਾਤਾਰ ਨਿਗਰਾਨੀ ਕੀਤੀ ਜਾਂਦੀ ਹੈ, ਅਤੇ ਚੇਤਾਵਨੀ webhook, paste-site, ਤੇ bin-service ਟਿਕਾਣਿਆਂ ਲਈ ਸੁਰ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **AC.11.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਫ਼ੋਰਕ PR ਲਈ AI ਸਮੀਖਿਆ ਬੋਟ ਜ਼ੀਰੋ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ, ਸਿਰਫ਼-ਪੜ੍ਹਨਯੋਗ ਸ਼ੈਡੋ ਮੋਡ[^0x92-shadow-mode] (shadow mode) ਵਿੱਚ ਚੱਲਦੇ ਹਨ। ਸ਼ੈਡੋ ਮੋਡ ਵਿੱਚ, ਜਦੋਂ ਤੱਕ ਕੋਈ ਰਿਪੌਜ਼ਟਰੀ ਸੰਭਾਲਕਰਤਾ ਪਹਿਲੀ-ਵਾਰੀ-ਯੋਗਦਾਨਕਰਤਾ ਦਾ ਸ਼ੁਰੂਆਤੀ ਤਸਦੀਕ ਗੇਟ ਪਾਸ ਨਹੀਂ ਕਰਾ ਦਿੰਦਾ, ਉਦੋਂ ਤੱਕ ਇਨਲਾਈਨ ਕੋਡ-ਤਿਆਰੀ ਟਿੱਪਣੀ ਸੀਮਤ ਰਹਿੰਦੀ ਹੈ ਅਤੇ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲਾ ਵਰਕਫ਼ਲੋ ਮੇਲ-ਜੋਲ ਵਰਜਿਤ ਹੁੰਦਾ ਹੈ। | 2 |
| **AC.11.8** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਸਮੀਖਿਆ ਅਤੇ ਸਹਾਇਕ ਬੋਟ ਲਗਾਤਾਰ ਵਿਰੋਧੀ ਟੈਸਟਿੰਗ ਦੇ ਅਧੀਨ ਹਨ: ਅਸਿੱਧੇ-prompt-ਇੰਜੈਕਸ਼ਨ ਕਾਰਪੋਰਾ ਨੂੰ ਨਕਲੀ PR, ਮੁੱਦਿਆਂ, ਅਤੇ ਟਿੱਪਣੀਆਂ ਰਾਹੀਂ ਬੋਟ ਦੇ ਵਿਰੁੱਧ ਮੁੜ ਚਲਾਇਆ ਜਾਂਦਾ ਹੈ। ਪਛਾਣ ਦੀ ਅਸਰਦਾਰੀ ਨੂੰ ਸਮੇਂ ਦੇ ਨਾਲ ਟਰੈਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਅਤੇ ਕੋਈ ਰਿਗਰੈਸ਼ਨ ਉਸ ਮਾਡਲ ਜਾਂ prompt ਅੱਪਡੇਟ ਨੂੰ ਰੋਕ ਦਿੰਦਾ ਹੈ ਜਿਸ ਨੇ ਉਸ ਨੂੰ ਪੈਦਾ ਕੀਤਾ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.11.1:** AISVS C2.1; OWASP LLM Top 10 (2025) LLM01; OWASP Agentic Top 10 (2026) ASI01, ASI06.
* **AC.11.2:** AISVS C2.1; OWASP LLM Top 10 (2025) LLM01; OWASP Agentic Top 10 (2026) ASI01.
* **AC.11.3:** AISVS C7.1; OWASP LLM Top 10 (2025) LLM05; OWASP Agentic Top 10 (2026) ASI02, ASI05.
* **AC.11.4:** AISVS C9.3; OWASP Agentic Top 10 (2026) ASI02, ASI03, ASI05; NIST SP 800-204D (Workload isolation).
* **AC.11.5:** AISVS C9.5, C5.2.5; OWASP ASVS v5 V4 (Access Control); OWASP Agentic Top 10 (2026) ASI02, ASI03.
* **AC.11.6:** OWASP ASVS v5 V8 (Logging & Error Handling); OWASP LLM Top 10 (2025) LLM02; ISO/IEC 27001:2022 A.8.15, A.8.16.
* **AC.11.7:** GitHub Security Lab "Preventing pwn requests" series (Parts 1-4); OWASP Agentic Top 10 (2026) ASI01, ASI03, ASI09; OWASP CI/CD Top 10 CICD-SEC-01.
* **AC.11.8:** MITRE ATLAS (Indirect prompt injection); AISVS C2.1, C11.1; OWASP SAMM Security Testing (ST).

---

## AC.12 CI/CD Pipeline Hardening Specific to AI Augmentation
## AC.12 AI ਵਾਧੇ ਲਈ ਵਿਸ਼ੇਸ਼ CI/CD ਪਾਈਪਲਾਈਨ ਸਖ਼ਤੀਕਰਨ

Two kinds of CI/CD pipeline control are in scope for this family: those that AI augmentation _newly requires_, and those that AI augmentation _breaks_. Generic CI/CD hygiene is not in scope here; it is covered elsewhere. Short-lived credentials, immutable action pinning, branch protection, SLSA Build Track L3 provenance, and multi-party production approval are all addressed by OWASP ASVS v5 V10, the OWASP Top 10 CI/CD Security Risks (CICD-SEC-01 through CICD-SEC-10), NIST SP 800-204D, and SLSA v1.2. Adopters implement those baselines and verify them against the originating standards. We do not repeat that assessment here.

ਇਸ ਪਰਿਵਾਰ ਦੇ ਦਾਇਰੇ ਵਿੱਚ ਦੋ ਕਿਸਮਾਂ ਦੇ CI/CD ਪਾਈਪਲਾਈਨ ਨਿਯੰਤਰਣ ਆਉਂਦੇ ਹਨ: ਉਹ ਜਿਹੜੇ AI ਵਾਧਾ _ਨਵੇਂ ਸਿਰਿਓਂ ਲੋੜੀਂਦੇ ਬਣਾ ਦਿੰਦਾ ਹੈ_, ਅਤੇ ਉਹ ਜਿਹੜੇ AI ਵਾਧਾ _ਤੋੜ ਦਿੰਦਾ ਹੈ_। ਆਮ CI/CD ਸਫ਼ਾਈ ਇੱਥੇ ਦਾਇਰੇ ਵਿੱਚ ਨਹੀਂ ਹੈ; ਉਸ ਨੂੰ ਹੋਰ ਥਾਂ ਢੱਕਿਆ ਗਿਆ ਹੈ। ਥੋੜ੍ਹ-ਚਿਰੇ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ, ਅਪਰਿਵਰਤਨਸ਼ੀਲ ਐਕਸ਼ਨ ਪਿੰਨਿੰਗ, ਬ੍ਰਾਂਚ ਸੁਰੱਖਿਆ, SLSA Build Track L3 ਮੂਲ-ਸਰੋਤ, ਅਤੇ ਬਹੁ-ਧਿਰੀ ਉਤਪਾਦਨ ਮਨਜ਼ੂਰੀ — ਇਹ ਸਾਰੇ OWASP ASVS v5 V10, OWASP Top 10 CI/CD Security Risks (CICD-SEC-01 ਤੋਂ CICD-SEC-10), NIST SP 800-204D, ਅਤੇ SLSA v1.2 ਦੁਆਰਾ ਸੰਬੋਧਿਤ ਕੀਤੇ ਗਏ ਹਨ। ਅਪਣਾਉਣ ਵਾਲੇ ਉਹ ਬੇਸਲਾਈਨਾਂ ਲਾਗੂ ਕਰਦੇ ਹਨ ਅਤੇ ਮੂਲ ਮਿਆਰਾਂ ਦੇ ਵਿਰੁੱਧ ਉਹਨਾਂ ਦੀ ਤਸਦੀਕ ਕਰਦੇ ਹਨ। ਅਸੀਂ ਉਹ ਮੁਲਾਂਕਣ ਇੱਥੇ ਨਹੀਂ ਦੁਹਰਾਉਂਦੇ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.12.1** | **Verify that** workflows triggered by untrusted contributions (GitHub Actions `pull_request_target`, `workflow_run`, and equivalent fork-aware triggers in other CI systems) never check out, build, test, or otherwise execute untrusted code in a context that has repository write permissions or access to repository, organization, package-registry, cloud, or deployment secrets. Where a privileged follow-up step is needed, the untrusted contribution is first processed in an unprivileged `pull_request` workflow, and only validated passive artifacts are passed forward to a separate privileged workflow. | 1 |
| **AC.12.2** | **Verify that** secrets, credentials, and pipeline job tokens are not persisted into workspaces that process AI-touched or fork-originated untrusted code. For example, set `persist-credentials: false` on checkout where the platform supports it, and scrub CI runners of cached credentials before AI tooling runs. | 1 |
| **AC.12.3** | **Verify that** secrets are not exposed to workflows running code from forks or first-time contributors. Environment-protection rules (or the platform equivalent, such as protected variables and deployment approvals) require a manual approval before any secret-bearing job runs for those contributions. This control pairs with AC.11.7 and AC.13.2. Bot-level enforcement under AC.11.7 does not substitute for the platform-level enforcement required here. | 1 |
| **AC.12.4** | **Verify that** self-hosted or persistent runners used by AI tooling are ephemeral (destroyed after each job), network-segmented, and isolated from production credentials. Persistent or long-lived runners do not process fork PRs or AI-generated untrusted artifacts under any circumstances. | 2 |
| **AC.12.5** | **Verify that** changes to workflow definition files (`.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, Argo, Tekton, and equivalents) are detected on every PR and route through an elevated review path that includes a security reviewer, regardless of who the contributor is or whether AI was involved. AI agents must not be granted bypass authority over this review path. | 2 |
| **AC.12.6** | **Verify that** pipeline audit logs (workflow runs, secret access, runner registration, permission grants, OIDC token issuance) are streamed in real time to centralized security monitoring. Detection rules are tuned for AI-augmented threat patterns: bulk PR creation from new accounts, workflow-file modifications in fork PRs, unexpected secret access from AI-runner pools, and unusual egress (webhooks, paste sites, bin services) from AI workloads. | 2 |
| **AC.12.7** | **Verify that** artifacts produced by untrusted PR workflows are treated as untrusted passive data when a privileged follow-up workflow consumes them. The privileged workflow never executes binaries, scripts, packages, caches, or generated workflow fragments that originated in an untrusted contribution. | 2 |
| **AC.12.8** | **Verify that** the remediation of a vulnerable workflow includes invalidating or re-validating any PR that was opened before the fix landed. Without this step, a later commit to the same PR can pick up the stale workflow definition and route around the fix. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.12.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਯੋਗਦਾਨਾਂ ਦੁਆਰਾ ਟ੍ਰਿਗਰ ਹੋਏ ਵਰਕਫ਼ਲੋ (GitHub Actions ਦੇ `pull_request_target`, `workflow_run`, ਅਤੇ ਹੋਰ CI ਸਿਸਟਮਾਂ ਵਿਚਲੇ ਬਰਾਬਰ ਦੇ ਫ਼ੋਰਕ-ਜਾਣੂ ਟ੍ਰਿਗਰ) ਕਦੇ ਵੀ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਕੋਡ ਨੂੰ ਅਜਿਹੇ ਸੰਦਰਭ ਵਿੱਚ ਚੈੱਕ-ਆਊਟ, ਬਿਲਡ, ਟੈਸਟ, ਜਾਂ ਕਿਸੇ ਹੋਰ ਢੰਗ ਨਾਲ ਨਹੀਂ ਚਲਾਉਂਦੇ ਜਿਸ ਕੋਲ ਰਿਪੌਜ਼ਟਰੀ ਲਿਖਣ ਦੀਆਂ ਇਜਾਜ਼ਤਾਂ ਹੋਣ ਜਾਂ ਰਿਪੌਜ਼ਟਰੀ, ਸੰਸਥਾ, ਪੈਕੇਜ-ਰਜਿਸਟਰੀ, ਕਲਾਊਡ, ਜਾਂ ਤੈਨਾਤੀ ਦੇ ਗੁਪਤ ਭੇਦਾਂ ਤੱਕ ਪਹੁੰਚ ਹੋਵੇ। ਜਿੱਥੇ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲਾ ਅਗਲਾ ਕਦਮ ਲੋੜੀਂਦਾ ਹੋਵੇ, ਉੱਥੇ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਯੋਗਦਾਨ ਦੀ ਪ੍ਰਕਿਰਿਆ ਪਹਿਲਾਂ ਇੱਕ ਗ਼ੈਰ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲੇ `pull_request` ਵਰਕਫ਼ਲੋ ਵਿੱਚ ਕੀਤੀ ਜਾਂਦੀ ਹੈ, ਅਤੇ ਸਿਰਫ਼ ਪ੍ਰਮਾਣਿਤ ਨਿਸ਼ਕਿਰਿਆ ਆਰਟੀਫ਼ੈਕਟ ਹੀ ਇੱਕ ਵੱਖਰੇ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲੇ ਵਰਕਫ਼ਲੋ ਨੂੰ ਅੱਗੇ ਦਿੱਤੇ ਜਾਂਦੇ ਹਨ। | 1 |
| **AC.12.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਗੁਪਤ ਭੇਦ, ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ, ਅਤੇ ਪਾਈਪਲਾਈਨ ਜੌਬ ਟੋਕਨ ਉਹਨਾਂ ਵਰਕਸਪੇਸਾਂ ਵਿੱਚ ਸੰਭਾਲ ਕੇ ਨਹੀਂ ਰੱਖੇ ਜਾਂਦੇ ਜਿਹੜੇ AI-ਛੂਹੇ ਜਾਂ ਫ਼ੋਰਕ ਤੋਂ ਆਏ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਕੋਡ ਦੀ ਪ੍ਰਕਿਰਿਆ ਕਰਦੇ ਹਨ। ਮਿਸਾਲ ਵਜੋਂ, ਜਿੱਥੇ ਪਲੇਟਫ਼ਾਰਮ ਸਮਰਥਨ ਕਰਦਾ ਹੈ ਉੱਥੇ ਚੈੱਕਆਊਟ ਉੱਤੇ `persist-credentials: false` ਸੈੱਟ ਕਰੋ, ਅਤੇ AI ਟੂਲਿੰਗ ਚੱਲਣ ਤੋਂ ਪਹਿਲਾਂ CI ਰਨਰਾਂ ਵਿੱਚੋਂ ਕੈਸ਼ ਕੀਤੇ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਸਾਫ਼ ਕਰੋ। | 1 |
| **AC.12.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਫ਼ੋਰਕਾਂ ਜਾਂ ਪਹਿਲੀ-ਵਾਰੀ ਯੋਗਦਾਨਕਰਤਾਵਾਂ ਦਾ ਕੋਡ ਚਲਾਉਣ ਵਾਲੇ ਵਰਕਫ਼ਲੋ ਨੂੰ ਗੁਪਤ ਭੇਦ ਨਹੀਂ ਦਿਖਾਏ ਜਾਂਦੇ। ਵਾਤਾਵਰਣ-ਸੁਰੱਖਿਆ ਨਿਯਮ (ਜਾਂ ਪਲੇਟਫ਼ਾਰਮ ਦਾ ਬਰਾਬਰ ਦਾ ਪ੍ਰਬੰਧ, ਜਿਵੇਂ ਸੁਰੱਖਿਅਤ ਵੇਰੀਏਬਲ ਅਤੇ ਤੈਨਾਤੀ ਮਨਜ਼ੂਰੀਆਂ) ਇਹਨਾਂ ਯੋਗਦਾਨਾਂ ਲਈ ਕੋਈ ਵੀ ਗੁਪਤ-ਭੇਦ ਵਾਲੀ ਜੌਬ ਚੱਲਣ ਤੋਂ ਪਹਿਲਾਂ ਦਸਤੀ ਮਨਜ਼ੂਰੀ ਦੀ ਲੋੜ ਪਾਉਂਦੇ ਹਨ। ਇਹ ਨਿਯੰਤਰਣ AC.11.7 ਅਤੇ AC.13.2 ਨਾਲ ਜੋੜੀ ਬਣਾਉਂਦਾ ਹੈ। AC.11.7 ਅਧੀਨ ਬੋਟ-ਪੱਧਰੀ ਲਾਗੂਕਰਨ ਇੱਥੇ ਲੋੜੀਂਦੇ ਪਲੇਟਫ਼ਾਰਮ-ਪੱਧਰੀ ਲਾਗੂਕਰਨ ਦਾ ਬਦਲ ਨਹੀਂ ਹੈ। | 1 |
| **AC.12.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਟੂਲਿੰਗ ਦੁਆਰਾ ਵਰਤੇ ਜਾਂਦੇ ਸਵੈ-ਹੋਸਟ ਕੀਤੇ ਜਾਂ ਸਥਾਈ ਰਨਰ ਥੋੜ੍ਹ-ਚਿਰੇ ਹਨ (ਹਰ ਜੌਬ ਤੋਂ ਬਾਅਦ ਨਸ਼ਟ ਕੀਤੇ ਜਾਂਦੇ ਹਨ), ਨੈੱਟਵਰਕ-ਪੱਖੋਂ ਵੰਡੇ ਹੋਏ ਹਨ, ਅਤੇ ਉਤਪਾਦਨ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲਾਂ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਹਨ। ਸਥਾਈ ਜਾਂ ਲੰਮੇ ਸਮੇਂ ਵਾਲੇ ਰਨਰ ਕਿਸੇ ਵੀ ਹਾਲਤ ਵਿੱਚ ਫ਼ੋਰਕ PR ਜਾਂ AI ਦੁਆਰਾ ਤਿਆਰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਆਰਟੀਫ਼ੈਕਟਾਂ ਦੀ ਪ੍ਰਕਿਰਿਆ ਨਹੀਂ ਕਰਦੇ। | 2 |
| **AC.12.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਵਰਕਫ਼ਲੋ ਪਰਿਭਾਸ਼ਾ ਫ਼ਾਈਲਾਂ (`.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, Argo, Tekton, ਅਤੇ ਬਰਾਬਰ ਦੀਆਂ) ਵਿਚਲੀਆਂ ਤਬਦੀਲੀਆਂ ਹਰ PR ਉੱਤੇ ਪਛਾਣੀਆਂ ਜਾਂਦੀਆਂ ਹਨ ਅਤੇ ਇੱਕ ਉੱਚੇ ਸਮੀਖਿਆ ਰਾਹ ਵਿੱਚੋਂ ਲੰਘਦੀਆਂ ਹਨ ਜਿਸ ਵਿੱਚ ਇੱਕ ਸੁਰੱਖਿਆ ਸਮੀਖਿਅਕ ਸ਼ਾਮਲ ਹੁੰਦਾ ਹੈ — ਭਾਵੇਂ ਯੋਗਦਾਨਕਰਤਾ ਕੋਈ ਵੀ ਹੋਵੇ ਅਤੇ ਭਾਵੇਂ AI ਸ਼ਾਮਲ ਸੀ ਜਾਂ ਨਹੀਂ। AI ਏਜੰਟਾਂ ਨੂੰ ਇਸ ਸਮੀਖਿਆ ਰਾਹ ਉੱਤੇ ਬਾਈਪਾਸ ਕਰਨ ਦਾ ਅਧਿਕਾਰ ਲਾਜ਼ਮੀ ਤੌਰ 'ਤੇ ਨਹੀਂ ਦਿੱਤਾ ਜਾਣਾ ਚਾਹੀਦਾ। | 2 |
| **AC.12.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪਾਈਪਲਾਈਨ ਆਡਿਟ ਲੌਗ (ਵਰਕਫ਼ਲੋ ਰਨ, ਗੁਪਤ-ਭੇਦ ਪਹੁੰਚ, ਰਨਰ ਰਜਿਸਟਰੇਸ਼ਨ, ਇਜਾਜ਼ਤਾਂ ਦੇਣਾ, OIDC ਟੋਕਨ ਜਾਰੀ ਕਰਨਾ) ਅਸਲ ਸਮੇਂ ਵਿੱਚ ਕੇਂਦਰੀਕ੍ਰਿਤ ਸੁਰੱਖਿਆ ਨਿਗਰਾਨੀ ਨੂੰ ਭੇਜੇ ਜਾਂਦੇ ਹਨ। ਪਛਾਣ ਨਿਯਮ AI-ਵਧਾਏ ਖ਼ਤਰਾ ਪੈਟਰਨਾਂ ਲਈ ਸੁਰ ਕੀਤੇ ਜਾਂਦੇ ਹਨ: ਨਵੇਂ ਖਾਤਿਆਂ ਤੋਂ ਥੋਕ PR ਬਣਾਉਣਾ, ਫ਼ੋਰਕ PR ਵਿੱਚ ਵਰਕਫ਼ਲੋ-ਫ਼ਾਈਲ ਸੋਧਾਂ, AI-ਰਨਰ ਪੂਲਾਂ ਤੋਂ ਅਣਕਿਆਸੀ ਗੁਪਤ-ਭੇਦ ਪਹੁੰਚ, ਅਤੇ AI ਵਰਕਲੋਡਾਂ ਤੋਂ ਅਸਧਾਰਨ ਬਾਹਰ ਜਾਣ ਵਾਲਾ ਟਰੈਫ਼ਿਕ (webhook, paste site, bin service)। | 2 |
| **AC.12.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜਦੋਂ ਕੋਈ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲਾ ਅਗਲਾ ਵਰਕਫ਼ਲੋ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ PR ਵਰਕਫ਼ਲੋ ਦੁਆਰਾ ਪੈਦਾ ਕੀਤੇ ਆਰਟੀਫ਼ੈਕਟਾਂ ਦੀ ਵਰਤੋਂ ਕਰਦਾ ਹੈ, ਤਾਂ ਉਹਨਾਂ ਨੂੰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਨਿਸ਼ਕਿਰਿਆ ਡਾਟਾ ਮੰਨਿਆ ਜਾਂਦਾ ਹੈ। ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲਾ ਵਰਕਫ਼ਲੋ ਕਦੇ ਵੀ ਅਜਿਹੀਆਂ ਬਾਈਨਰੀਆਂ, ਸਕ੍ਰਿਪਟਾਂ, ਪੈਕੇਜਾਂ, ਕੈਸ਼ਾਂ, ਜਾਂ ਤਿਆਰ ਕੀਤੇ ਵਰਕਫ਼ਲੋ ਟੁਕੜਿਆਂ ਨੂੰ ਨਹੀਂ ਚਲਾਉਂਦਾ ਜੋ ਕਿਸੇ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਯੋਗਦਾਨ ਵਿੱਚੋਂ ਆਏ ਹੋਣ। | 2 |
| **AC.12.8** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕਿਸੇ ਕਮਜ਼ੋਰ ਵਰਕਫ਼ਲੋ ਦੀ ਦਰੁਸਤੀ ਵਿੱਚ ਹਰ ਉਸ PR ਨੂੰ ਅਯੋਗ ਕਰਨਾ ਜਾਂ ਮੁੜ-ਪ੍ਰਮਾਣਿਤ ਕਰਨਾ ਸ਼ਾਮਲ ਹੈ ਜੋ ਦਰੁਸਤੀ ਲਾਗੂ ਹੋਣ ਤੋਂ ਪਹਿਲਾਂ ਖੋਲ੍ਹੀ ਗਈ ਸੀ। ਇਸ ਕਦਮ ਤੋਂ ਬਿਨਾਂ, ਉਸੇ PR ਉੱਤੇ ਬਾਅਦ ਵਿੱਚ ਕੀਤਾ ਕਮਿਟ ਪੁਰਾਣੀ ਵਰਕਫ਼ਲੋ ਪਰਿਭਾਸ਼ਾ ਚੁੱਕ ਸਕਦਾ ਹੈ ਅਤੇ ਦਰੁਸਤੀ ਦੇ ਦੁਆਲਿਓਂ ਲੰਘ ਸਕਦਾ ਹੈ। | 2 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.12.1:** OWASP CI/CD Top 10 CICD-SEC-01, CICD-SEC-04; GitHub Security Lab "Preventing pwn requests" series; NIST SP 800-204D (Pipeline isolation).
* **AC.12.2:** OWASP CI/CD Top 10 CICD-SEC-02, CICD-SEC-06; GitHub Docs (Automatic token authentication and permissions); NIST SP 800-53r5 AC-6 (Least Privilege).
* **AC.12.3:** OWASP CI/CD Top 10 CICD-SEC-01; GitHub Docs (Approving workflow runs from public forks; Protected environments); GitLab Docs (Protected variables).
* **AC.12.4:** OWASP CI/CD Top 10 CICD-SEC-06; NIST SP 800-204D (Runner isolation); ISO/IEC 27001:2022 A.8.22 (Segregation of Networks).
* **AC.12.5:** OWASP CI/CD Top 10 CICD-SEC-01; NIST SSDF PW.7; ISO/IEC 27001:2022 A.8.32.
* **AC.12.6:** OWASP ASVS v5 V8 (Logging); OWASP CI/CD Top 10 CICD-SEC-10 (Insufficient Logging and Visibility); ISO/IEC 27001:2022 A.8.16.
* **AC.12.7:** GitHub Security Lab "Preventing pwn requests" series; OWASP CI/CD Top 10 CICD-SEC-01; NIST SP 800-204D (Cross-workflow trust boundaries).
* **AC.12.8:** GitHub Security Lab "Preventing pwn requests" Part 4 (Alvaro Munoz, 2025); OWASP CI/CD Top 10 CICD-SEC-01; NIST SSDF RV.1.

---

## AC.13 Adversarial AI Detection in Inbound Contributions
## AC.13 ਅੰਦਰ ਆਉਣ ਵਾਲੇ ਯੋਗਦਾਨਾਂ ਵਿੱਚ ਵਿਰੋਧੀ AI ਦੀ ਪਛਾਣ

The previous families were about defending your own AI from misuse. This one flips the lens. Here the AI is on the attacker's side, and you are trying to spot the signal in inbound contributions and content. The scenario worth defending against is the one where an attacker uses AI to run fork-and-PR campaigns at scale, with malicious payloads tailored to the target repository.

ਪਿਛਲੇ ਪਰਿਵਾਰ ਤੁਹਾਡੇ ਆਪਣੇ AI ਨੂੰ ਦੁਰਵਰਤੋਂ ਤੋਂ ਬਚਾਉਣ ਬਾਰੇ ਸਨ। ਇਹ ਪਰਿਵਾਰ ਨਜ਼ਰੀਆ ਉਲਟਾ ਦਿੰਦਾ ਹੈ। ਇੱਥੇ AI ਹਮਲਾਵਰ ਦੇ ਪਾਸੇ ਹੈ, ਅਤੇ ਤੁਸੀਂ ਅੰਦਰ ਆਉਣ ਵਾਲੇ ਯੋਗਦਾਨਾਂ ਤੇ ਸਮੱਗਰੀ ਵਿੱਚ ਉਸ ਦਾ ਸੰਕੇਤ ਪਛਾਣਨ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰ ਰਹੇ ਹੋ। ਜਿਸ ਦ੍ਰਿਸ਼ ਤੋਂ ਬਚਾਅ ਕਰਨਾ ਬਣਦਾ ਹੈ ਉਹ ਇਹ ਹੈ ਕਿ ਹਮਲਾਵਰ AI ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਵੱਡੇ ਪੈਮਾਨੇ ਉੱਤੇ ਫ਼ੋਰਕ-ਅਤੇ-PR ਮੁਹਿੰਮਾਂ ਚਲਾਉਂਦਾ ਹੈ, ਜਿਨ੍ਹਾਂ ਵਿੱਚ ਖ਼ਤਰਨਾਕ ਪੇਲੋਡ ਨਿਸ਼ਾਨਾ ਰਿਪੌਜ਼ਟਰੀ ਮੁਤਾਬਕ ਢਾਲੇ ਹੁੰਦੇ ਹਨ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.13.1** | **Verify that** contribution-velocity and contributor-reputation analytics flag anomalies: bulk PR creation from newly created accounts, coordinated fork waves immediately preceding PRs, PR volumes that are inconsistent with human authorship, and reuse of payload patterns across unrelated repositories. | 1 |
| **AC.13.2** | **Verify that** PRs from first-time or low-reputation contributors require maintainer approval before any privileged workflow processes them. Privileged workflows here include AI review bots, secret-bearing jobs, and external-integration calls. | 1 |
| **AC.13.3** | **Verify that** automated PR pipeline gates detect known indicators of LLM-generated or LLM-assisted malicious payload patterns: registry-confusable or typosquatted dependency names, package references that do not resolve to any published version, and dependencies whose creation, first-publication, or maintainer-change timestamps look anomalous relative to the PR. | 2 |
| **AC.13.4** | **Verify that** detection rules are tagged to MITRE ATT&CK (T1195 Supply Chain Compromise and CI/CD-relevant sub-techniques) and to MITRE ATLAS techniques, maintained for the inbound contribution analysis use case, and reviewed against current threat intelligence. | 2 |
| **AC.13.5** | **Verify that** confirmed or high-confidence adversarial contributions trigger automated containment: block the PR, quarantine the fork, suspend the contributor, notify maintainers, and freeze affected workflow files. Triage decisions feed back into detection tuning. | 3 |
| **AC.13.6** | **Verify that** PR analytics include structural AST profiling and stylometric or entropy-based heuristics tuned to identify LLM-generated code patterns. Detection in this category is still maturing, so compensating controls are accepted in place of high-precision automated detection: mandatory human review on flagged PRs, sandboxed execution of suspect payloads, and deferred merge until additional signals accrue. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.13.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਯੋਗਦਾਨ-ਰਫ਼ਤਾਰ ਅਤੇ ਯੋਗਦਾਨਕਰਤਾ-ਸਾਖ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਅਸਧਾਰਨਤਾਵਾਂ ਨੂੰ ਨਿਸ਼ਾਨਬੱਧ ਕਰਦਾ ਹੈ: ਨਵੇਂ ਬਣੇ ਖਾਤਿਆਂ ਤੋਂ ਥੋਕ PR ਬਣਾਉਣਾ, PR ਤੋਂ ਐਨ ਪਹਿਲਾਂ ਤਾਲਮੇਲ ਨਾਲ ਆਈਆਂ ਫ਼ੋਰਕ ਲਹਿਰਾਂ, ਅਜਿਹੀ PR ਮਾਤਰਾ ਜੋ ਮਨੁੱਖੀ ਲੇਖਣੀ ਨਾਲ ਮੇਲ ਨਹੀਂ ਖਾਂਦੀ, ਅਤੇ ਗ਼ੈਰ-ਸੰਬੰਧਿਤ ਰਿਪੌਜ਼ਟਰੀਆਂ ਵਿੱਚ ਉਹੀ ਪੇਲੋਡ ਪੈਟਰਨ ਮੁੜ ਵਰਤੇ ਜਾਣਾ। | 1 |
| **AC.13.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪਹਿਲੀ-ਵਾਰੀ ਜਾਂ ਘੱਟ-ਸਾਖ ਵਾਲੇ ਯੋਗਦਾਨਕਰਤਾਵਾਂ ਦੀਆਂ PR ਲਈ ਕਿਸੇ ਵੀ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲੇ ਵਰਕਫ਼ਲੋ ਵੱਲੋਂ ਉਹਨਾਂ ਦੀ ਪ੍ਰਕਿਰਿਆ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਸੰਭਾਲਕਰਤਾ ਦੀ ਮਨਜ਼ੂਰੀ ਲਾਜ਼ਮੀ ਹੈ। ਇੱਥੇ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਵਾਲੇ ਵਰਕਫ਼ਲੋ ਵਿੱਚ AI ਸਮੀਖਿਆ ਬੋਟ, ਗੁਪਤ-ਭੇਦ ਵਾਲੀਆਂ ਜੌਬਾਂ, ਅਤੇ ਬਾਹਰੀ-ਏਕੀਕਰਨ ਸੱਦੇ ਸ਼ਾਮਲ ਹਨ। | 1 |
| **AC.13.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਵੈਚਾਲਿਤ PR ਪਾਈਪਲਾਈਨ ਗੇਟ LLM ਦੁਆਰਾ ਤਿਆਰ ਜਾਂ LLM-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਖ਼ਤਰਨਾਕ ਪੇਲੋਡ ਪੈਟਰਨਾਂ ਦੇ ਜਾਣੇ-ਪਛਾਣੇ ਸੰਕੇਤ ਪਛਾਣਦੇ ਹਨ: ਰਜਿਸਟਰੀ ਵਿੱਚ ਭੁਲੇਖਾ ਪਾਉਣ ਵਾਲੇ ਜਾਂ typosquatted[^0x92-typosquatted] ਡਿਪੈਂਡੈਂਸੀ ਨਾਂ, ਅਜਿਹੇ ਪੈਕੇਜ ਹਵਾਲੇ ਜੋ ਕਿਸੇ ਵੀ ਪ੍ਰਕਾਸ਼ਿਤ ਵਰਜ਼ਨ ਨਾਲ ਨਹੀਂ ਮਿਲਦੇ, ਅਤੇ ਉਹ ਡਿਪੈਂਡੈਂਸੀਆਂ ਜਿਨ੍ਹਾਂ ਦੀ ਸਿਰਜਣਾ, ਪਹਿਲੇ-ਪ੍ਰਕਾਸ਼ਨ, ਜਾਂ ਸੰਭਾਲਕਰਤਾ-ਬਦਲੀ ਦੇ ਸਮਾਂ-ਚਿੰਨ੍ਹ PR ਦੇ ਮੁਕਾਬਲੇ ਅਸਧਾਰਨ ਲੱਗਦੇ ਹਨ। | 2 |
| **AC.13.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪਛਾਣ ਨਿਯਮ MITRE ATT&CK (T1195 Supply Chain Compromise ਅਤੇ CI/CD ਨਾਲ ਸੰਬੰਧਿਤ ਉਪ-ਤਕਨੀਕਾਂ) ਅਤੇ MITRE ATLAS ਤਕਨੀਕਾਂ ਨਾਲ ਟੈਗ ਕੀਤੇ ਗਏ ਹਨ, ਅੰਦਰ ਆਉਣ ਵਾਲੇ ਯੋਗਦਾਨ ਦੇ ਵਿਸ਼ਲੇਸ਼ਣ ਵਾਲੇ ਵਰਤੋਂ-ਮਾਮਲੇ ਲਈ ਬਰਕਰਾਰ ਰੱਖੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ ਮੌਜੂਦਾ ਖ਼ਤਰਾ ਖ਼ੁਫ਼ੀਆ ਜਾਣਕਾਰੀ ਦੇ ਵਿਰੁੱਧ ਸਮੀਖਿਆ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 2 |
| **AC.13.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪੁਸ਼ਟ ਜਾਂ ਉੱਚ-ਭਰੋਸੇ ਵਾਲੇ ਵਿਰੋਧੀ ਯੋਗਦਾਨ ਸਵੈਚਾਲਿਤ ਘੇਰਾਬੰਦੀ[^0x92-containment] (containment) ਸ਼ੁਰੂ ਕਰਦੇ ਹਨ: PR ਨੂੰ ਰੋਕੋ, ਫ਼ੋਰਕ ਨੂੰ ਕੁਆਰੰਟੀਨ ਕਰੋ, ਯੋਗਦਾਨਕਰਤਾ ਨੂੰ ਮੁਅੱਤਲ ਕਰੋ, ਸੰਭਾਲਕਰਤਾਵਾਂ ਨੂੰ ਸੂਚਿਤ ਕਰੋ, ਅਤੇ ਪ੍ਰਭਾਵਿਤ ਵਰਕਫ਼ਲੋ ਫ਼ਾਈਲਾਂ ਨੂੰ ਜਮਾ ਦਿਓ। ਛਾਂਟੀ ਦੇ ਫ਼ੈਸਲੇ ਵਾਪਸ ਪਛਾਣ ਦੀ ਸੁਰ-ਸੈਟਿੰਗ ਵਿੱਚ ਜਾਂਦੇ ਹਨ। | 3 |
| **AC.13.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** PR ਵਿਸ਼ਲੇਸ਼ਣ ਵਿੱਚ ਢਾਂਚਾਗਤ AST ਪ੍ਰੋਫ਼ਾਈਲਿੰਗ ਅਤੇ LLM ਦੁਆਰਾ ਤਿਆਰ ਕੋਡ ਪੈਟਰਨ ਪਛਾਣਨ ਲਈ ਸੁਰ ਕੀਤੇ ਸਟਾਈਲੋਮੈਟ੍ਰਿਕ[^0x92-stylometric] (stylometric) ਜਾਂ ਐਂਟਰੌਪੀ-ਆਧਾਰਿਤ ਅਨੁਮਾਨ-ਨੇਮ ਸ਼ਾਮਲ ਹਨ। ਇਸ ਸ਼੍ਰੇਣੀ ਵਿੱਚ ਪਛਾਣ ਅਜੇ ਪੱਕ ਰਹੀ ਹੈ, ਇਸ ਲਈ ਉੱਚ-ਸ਼ੁੱਧਤਾ ਵਾਲੀ ਸਵੈਚਾਲਿਤ ਪਛਾਣ ਦੀ ਥਾਂ ਭਰਪਾਈ ਕਰਨ ਵਾਲੇ ਨਿਯੰਤਰਣ ਪ੍ਰਵਾਨ ਹਨ: ਨਿਸ਼ਾਨਬੱਧ PR ਉੱਤੇ ਲਾਜ਼ਮੀ ਮਨੁੱਖੀ ਸਮੀਖਿਆ, ਸ਼ੱਕੀ ਪੇਲੋਡਾਂ ਦਾ ਸੈਂਡਬਾਕਸ ਵਿੱਚ ਐਗਜ਼ੀਕਿਊਸ਼ਨ, ਅਤੇ ਹੋਰ ਸੰਕੇਤ ਇਕੱਠੇ ਹੋਣ ਤੱਕ ਮਰਜ ਨੂੰ ਟਾਲਣਾ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.13.1:** OWASP CI/CD Top 10 CICD-SEC-01; NIST AI RMF MANAGE; MITRE ATLAS (Reconnaissance).
* **AC.13.2:** GitHub Docs (Approving workflow runs from public forks); OWASP CI/CD Top 10 CICD-SEC-01; NIST SSDF PW.4.
* **AC.13.3:** OWASP LLM Top 10 (2025) LLM03; OWASP CI/CD Top 10 CICD-SEC-03 (Dependency Chain Abuse); NIST SSDF PW.4.
* **AC.13.4:** MITRE ATT&CK T1195; MITRE ATLAS (Technique catalogue); OWASP SAMM Threat Assessment (TA).
* **AC.13.5:** NIST AI RMF MANAGE; ISO/IEC 27001:2022 A.5.25 (Assessment of Information Security Events); OWASP SAMM Incident Management (IM).
* **AC.13.6:** MITRE ATLAS (Adversarial ML output detection, research-edge); OWASP LLM Top 10 (2025) LLM03; NIST SSDF PW.8.

---

## AC.14 Compromise Containment & Automated Remediation
## AC.14 ਸਮਝੌਤੇ ਦੀ ਘੇਰਾਬੰਦੀ ਅਤੇ ਸਵੈਚਾਲਿਤ ਦਰੁਸਤੀ

Things go wrong eventually. When an AI-adjacent compromise (a prompt-injected bot, a leaked CI secret, a malicious AI-generated artifact in a build) is suspected or confirmed, the goal is to contain the damage and shorten the recovery.

ਗੱਲਾਂ ਆਖ਼ਰ ਵਿਗੜਦੀਆਂ ਹੀ ਹਨ। ਜਦੋਂ ਕਿਸੇ AI-ਨਾਲ ਲੱਗਦੇ ਸਮਝੌਤੇ (compromise) ਦਾ ਸ਼ੱਕ ਪਵੇ ਜਾਂ ਪੁਸ਼ਟੀ ਹੋ ਜਾਵੇ — ਜਿਵੇਂ prompt-ਇੰਜੈਕਟ ਕੀਤਾ ਬੋਟ, ਲੀਕ ਹੋਇਆ CI ਗੁਪਤ ਭੇਦ, ਜਾਂ ਬਿਲਡ ਵਿੱਚ AI ਦੁਆਰਾ ਤਿਆਰ ਕੋਈ ਖ਼ਤਰਨਾਕ ਆਰਟੀਫ਼ੈਕਟ — ਤਾਂ ਟੀਚਾ ਹੁੰਦਾ ਹੈ ਨੁਕਸਾਨ ਦੀ ਘੇਰਾਬੰਦੀ ਕਰਨਾ ਅਤੇ ਮੁੜ-ਬਹਾਲੀ ਦਾ ਸਮਾਂ ਘਟਾਉਣਾ।

<!-- markdownlint-disable MD013 -->
| # | Description | Level |
| --- | --- | --- |
| **AC.14.1** | **Verify that** an incident-response playbook exists for AI-in-pipeline compromise. At minimum it covers: revoking AI-agent credentials, rotating every secret that touched the compromised workflow run, quarantining the compromised artifacts, notifying downstream consumers, notifying regulators where applicable, and preserving prompts, responses, and audit logs for forensics. | 1 |
| **AC.14.2** | **Verify that** any secret that touched a workflow run associated with a suspicious PR, a prompt-injection event, or an AI-agent anomaly is automatically rotated, and that downstream issuers (cloud IAM, package registries, signing-key custodians) are notified of the rotation. | 1 |
| **AC.14.3** | **Verify that** AI agent identities (keys, tokens, OIDC trust grants) can be rapidly revoked and quarantined, with a target time-to-revoke that is written down and tested at least once a year. | 2 |
| **AC.14.4** | **Verify that** build provenance and AI BOM records are used during incident response to identify every downstream artifact produced under the suspect AI agent or the compromised pipeline run, so that recall, rebuild, or quarantine can be targeted. | 2 |
| **AC.14.5** | **Verify that** automated remediation is tested in tabletop or live-fire exercises at least once a year. The scenarios include a prompt-injected reviewer bot, fork-PR secret exfiltration, and an AI-generated malicious workflow file. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| --- | --- | --- |
| **AC.14.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪਾਈਪਲਾਈਨ ਵਿਚਲੇ AI ਦੇ ਸਮਝੌਤੇ ਲਈ ਇੱਕ ਘਟਨਾ-ਜਵਾਬ ਪਲੇਬੁੱਕ (incident-response playbook) ਮੌਜੂਦ ਹੈ। ਘੱਟੋ-ਘੱਟ ਇਹ ਗੱਲਾਂ ਢੱਕੀਆਂ ਹੋਣ: AI-ਏਜੰਟ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਰੱਦ ਕਰਨਾ, ਸਮਝੌਤਾਗ੍ਰਸਤ ਵਰਕਫ਼ਲੋ ਰਨ ਨੂੰ ਛੂਹਣ ਵਾਲਾ ਹਰ ਗੁਪਤ ਭੇਦ ਬਦਲਣਾ, ਸਮਝੌਤਾਗ੍ਰਸਤ ਆਰਟੀਫ਼ੈਕਟਾਂ ਨੂੰ ਕੁਆਰੰਟੀਨ ਕਰਨਾ, ਡਾਊਨਸਟ੍ਰੀਮ ਵਰਤੋਂਕਾਰਾਂ ਨੂੰ ਸੂਚਿਤ ਕਰਨਾ, ਜਿੱਥੇ ਲਾਗੂ ਹੋਵੇ ਉੱਥੇ ਨਿਯਾਮਕਾਂ ਨੂੰ ਸੂਚਿਤ ਕਰਨਾ, ਅਤੇ ਫ਼ੌਰੈਂਸਿਕ ਲਈ prompt, ਜਵਾਬ, ਤੇ ਆਡਿਟ ਲੌਗ ਸਾਂਭ ਕੇ ਰੱਖਣਾ। | 1 |
| **AC.14.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕਿਸੇ ਸ਼ੱਕੀ PR, prompt ਇੰਜੈਕਸ਼ਨ ਦੀ ਘਟਨਾ, ਜਾਂ AI-ਏਜੰਟ ਦੀ ਅਸਧਾਰਨਤਾ ਨਾਲ ਜੁੜੇ ਵਰਕਫ਼ਲੋ ਰਨ ਨੂੰ ਛੂਹਣ ਵਾਲਾ ਹਰ ਗੁਪਤ ਭੇਦ ਆਪਣੇ-ਆਪ ਬਦਲਿਆ (rotate) ਜਾਂਦਾ ਹੈ, ਅਤੇ ਡਾਊਨਸਟ੍ਰੀਮ ਜਾਰੀਕਰਤਾਵਾਂ (ਕਲਾਊਡ IAM, ਪੈਕੇਜ ਰਜਿਸਟਰੀਆਂ, ਦਸਤਖ਼ਤ-ਕੁੰਜੀ ਦੇ ਰਾਖਿਆਂ) ਨੂੰ ਇਸ ਬਦਲੀ ਬਾਰੇ ਸੂਚਿਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **AC.14.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI ਏਜੰਟ ਪਛਾਣਾਂ (ਕੁੰਜੀਆਂ, ਟੋਕਨ, OIDC ਭਰੋਸਾ ਗ੍ਰਾਂਟਾਂ) ਨੂੰ ਤੇਜ਼ੀ ਨਾਲ ਰੱਦ ਅਤੇ ਕੁਆਰੰਟੀਨ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ, ਅਤੇ ਰੱਦ ਕਰਨ ਦਾ ਨਿਸ਼ਾਨਾ-ਸਮਾਂ ਲਿਖਤੀ ਰੂਪ ਵਿੱਚ ਦਰਜ ਹੈ ਤੇ ਸਾਲ ਵਿੱਚ ਘੱਟੋ-ਘੱਟ ਇੱਕ ਵਾਰ ਪਰਖਿਆ ਜਾਂਦਾ ਹੈ। | 2 |
| **AC.14.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਘਟਨਾ ਜਵਾਬ ਦੌਰਾਨ ਬਿਲਡ ਮੂਲ-ਸਰੋਤ ਅਤੇ AI BOM ਰਿਕਾਰਡਾਂ ਦੀ ਵਰਤੋਂ ਸ਼ੱਕੀ AI ਏਜੰਟ ਜਾਂ ਸਮਝੌਤਾਗ੍ਰਸਤ ਪਾਈਪਲਾਈਨ ਰਨ ਅਧੀਨ ਪੈਦਾ ਹੋਏ ਹਰ ਡਾਊਨਸਟ੍ਰੀਮ ਆਰਟੀਫ਼ੈਕਟ ਦੀ ਪਛਾਣ ਕਰਨ ਲਈ ਕੀਤੀ ਜਾਂਦੀ ਹੈ, ਤਾਂ ਜੋ ਵਾਪਸੀ, ਮੁੜ-ਬਿਲਡ, ਜਾਂ ਕੁਆਰੰਟੀਨ ਨੂੰ ਨਿਸ਼ਾਨਾਬੱਧ ਕੀਤਾ ਜਾ ਸਕੇ। | 2 |
| **AC.14.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਵੈਚਾਲਿਤ ਦਰੁਸਤੀ ਨੂੰ ਸਾਲ ਵਿੱਚ ਘੱਟੋ-ਘੱਟ ਇੱਕ ਵਾਰ ਟੇਬਲਟੌਪ ਜਾਂ ਲਾਈਵ-ਫ਼ਾਇਰ ਮਸ਼ਕਾਂ ਵਿੱਚ ਪਰਖਿਆ ਜਾਂਦਾ ਹੈ। ਇਹਨਾਂ ਦ੍ਰਿਸ਼ਾਂ ਵਿੱਚ prompt-ਇੰਜੈਕਟ ਕੀਤਾ ਸਮੀਖਿਅਕ ਬੋਟ, ਫ਼ੋਰਕ-PR ਰਾਹੀਂ ਗੁਪਤ ਭੇਦ ਬਾਹਰ ਕੱਢਣਾ, ਅਤੇ AI ਦੁਆਰਾ ਤਿਆਰ ਖ਼ਤਰਨਾਕ ਵਰਕਫ਼ਲੋ ਫ਼ਾਈਲ ਸ਼ਾਮਲ ਹਨ। | 3 |

**Mappings & References:**

**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**

* **AC.14.1:** ISO/IEC 27001:2022 A.5.24, A.5.26; NIST AI RMF MANAGE; OWASP SAMM Incident Management (IM).
* **AC.14.2:** OWASP ASVS v5 V6 (Cryptography), V14; OWASP CI/CD Top 10 CICD-SEC-06; NIST SSDF RV.2.
* **AC.14.3:** AISVS C9.4 (Agent and Orchestrator Identity); NIST SP 800-207 (Zero Trust Architecture); ISO/IEC 27001:2022 A.5.18 (Access Rights).
* **AC.14.4:** OWASP SCVS (Bill-of-materials analysis); CycloneDX ML-BOM tracing; NIST SSDF RV.1.
* **AC.14.5:** NIST SSDF RV.1; ISO/IEC 27001:2022 A.5.28 (Collection of Evidence); OWASP SAMM Incident Management (IM).

[^0x92-appendix]: **Appendix** (EN) -> ਅੰਤਿਕਾ — the settled Panjabi term for a document appendix in academic/government publishing; the division letter stays Latin as a cross-reference target, matching Appendix A and Appendix B. Full discussion: OPEN-QUESTIONS.md Q121.
[^0x92-baseline]: **baseline** (EN) -> ਬੇਸਲਾਈਨ — kept as a loan rather than ਆਧਾਰ-ਰੇਖਾ, since ਆਧਾਰ is already load-bearing corpus-wide as the pinned -ਆਧਾਰਿਤ ("-based") suffix and the two would collide when adjacent; one word has to cover a maturity floor, a comparison measurement, and a signed reference artifact. Full discussion: OPEN-QUESTIONS.md Q118.
[^0x92-threat-scenario]: **threat scenario** (EN) -> ਖ਼ਤਰਾ ਦ੍ਰਿਸ਼ — ਦ੍ਰਿਸ਼ ("scene, depicted situation") names a described hypothetical, kept visibly distinct from ਪਰਿਦ੍ਰਿਸ਼ (*threat landscape*) the way "scene" and "panorama" are distinct in English. Full discussion: OPEN-QUESTIONS.md Q122.
[^0x92-guardrail]: **guardrail** (EN) -> ਗਾਰਡਰੇਲ — kept as a neutral loan after excluding ਮਰਿਆਦਾ, which names the Sikh code of conduct and would be a Gurmat-safety violation if applied to a machine constraint. Full discussion: OPEN-QUESTIONS.md Q105.
[^0x92-workflow]: **workflow** (EN) -> ਵਰਕਫ਼ਲੋ — one loan covers both the written-process sense and the CI/CD-artifact sense, because the appendix uses the English word for both and two Panjabi words would suggest two unrelated concepts; deliberately kept distinct from ਪਾਈਪਲਾਈਨ (*pipeline*). Full discussion: OPEN-QUESTIONS.md Q110.
[^0x92-fork]: **fork** (EN) -> ਫ਼ੋਰਕ — kept as a loan because the security meaning here is a trust boundary (a fork PR originates outside the repository's permission domain), a sense that ਨਕਲ ("copy") or ਵੰਡ ("split") would lose and that ਸ਼ਾਖ਼ਾ would collide with *branch*. Full discussion: OPEN-QUESTIONS.md Q107.
[^0x92-separation-of-duties]: **separation of duties** (EN) -> ਕਰਤੱਵਾਂ ਦੀ ਵੰਡ — ਕਰਤੱਵ ("duty, assigned task") reads as a named ISO/IEC 27001 control, where ਜ਼ਿੰਮੇਵਾਰੀ ("responsibility") would drift to ordinary work allocation. Full discussion: OPEN-QUESTIONS.md Q109.
[^0x92-pull-request]: **pull request** (EN) -> ਪੁੱਲ ਰਿਕੁਐਸਟ, glossed on first use, then the retained acronym **PR** — a named platform object with an identity and an API (GitHub/GitLab), so a descriptive native rendering would break the mapping to the literal `pull_request` trigger name used in the same requirement set. Full discussion: OPEN-QUESTIONS.md Q106.
[^0x92-explainability]: **Explainability** (EN) -> ਵਿਆਖਿਆਯੋਗਤਾ — built with the -ਯੋਗਤਾ property-noun suffix, matching how the corpus already forms ਟਰੇਸਯੋਗਤਾ (*traceability*), the very word paired with it in this chapter title; kept distinct from ਪਾਰਦਰਸ਼ਤਾ (*transparency*), a separate governance concept elsewhere in the corpus. Full discussion: OPEN-QUESTIONS.md Q120.
[^0x92-tamper-evident]: **tamper-evident** (EN) -> ਛੇੜਛਾੜ-ਪ੍ਰਗਟ — ਪ੍ਰਗਟ ("manifest, apparent") keeps the detectability claim distinct from ਛੇੜਛਾੜ-ਰੋਧਕ (*tamper-resistant*, prevention), which is a different property than this control asks for. Full discussion: OPEN-QUESTIONS.md Q112.
[^0x92-red-teaming]: **Red-Teaming** (EN) -> ਰੈੱਡ-ਟੀਮਿੰਗ — kept as a loan because the colour term is a naming convention for a security discipline, not a description; translating it (ਲਾਲ ਟੀਮ) would leave a reader with an unexplained colour. Full discussion: OPEN-QUESTIONS.md Q108.
[^0x92-policy-as-code]: **policy-as-code** (EN) -> ਕੋਡ-ਵਜੋਂ-ਨੀਤੀ — a transparent compound built from already-settled ਨੀਤੀ (*policy*) and the ordinary loan ਕੋਡ, with word order following the Panjabi head-final pattern rather than transliterating the English order. Full discussion: OPEN-QUESTIONS.md Q113.
[^0x92-dual-control]: **dual control** (EN) -> ਦੋਹਰਾ ਨਿਯੰਤਰਣ — kept visibly separate from *separation of duties* because this requirement demands dual control **and** a security-team review as two distinct obligations in the same sentence. Full discussion: OPEN-QUESTIONS.md Q109.
[^0x92-runner]: **runner** (CI runner) (EN) -> ਰਨਰ — kept as a loan because a runner is a named CI-platform component (a registered, labelled execution host); ਦੌੜਾਕ (literal "runner," as in athlete) would make "persistent or long-lived runners" read as a statement about people. Full discussion: OPEN-QUESTIONS.md Q111.
[^0x92-principal]: **principal** (security principal) (EN) -> ਪਛਾਣ-ਇਕਾਈ — built on the already-settled ਪਛਾਣ ("identity") rather than ਕਰਤਾ, which is rejected on Gurmat grounds as load-bearing devotional vocabulary for a divine doer. Full discussion: OPEN-QUESTIONS.md Q124.
[^0x92-bot]: **bot** (EN) -> ਬੋਟ — kept as a neutral loan distinct from ਸਹਾਇਕ (*assistant*), ਏਜੰਟ (*agent*, reserved elsewhere), and *copilot* (its own loan), because this appendix restricts what each of the four actors may do and the family's structure collapses if any two share one Panjabi word. Full discussion: OPEN-QUESTIONS.md Q119.
[^0x92-sanitization]: **sanitization** (EN) -> ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ — corrected from an earlier draft's ਸਫ਼ਾਈ ("cleaning"), which renders *hygiene* elsewhere in this same appendix; ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ is the form already settled across the corpus for neutralising a payload rather than tidying. Full discussion: OPEN-QUESTIONS.md Q125.
[^0x92-shadow-mode]: **shadow mode** (EN) -> ਸ਼ੈਡੋ ਮੋਡ — kept as a loan because it names a fixed industry deployment pattern (the component still runs and evaluates, but holds no privilege); ਪਰਛਾਵਾਂ ("shadow") was rejected because it carries an ominous/inauspicious shading in ordinary Panjabi usage. Full discussion: OPEN-QUESTIONS.md Q117.
[^0x92-typosquatted]: **typosquatted** (EN) -> retained in Latin — a named supply-chain technique catalogued by OWASP CI/CD Top 10 CICD-SEC-03, which this requirement cites, so a practitioner searching for it needs the English string rather than a translated description. Full discussion: OPEN-QUESTIONS.md Q116.
[^0x92-containment]: **containment** (EN) -> ਘੇਰਾਬੰਦੀ ("cordoning off, encircling") — deliberately not ਰੋਕਥਾਮ ("prevention"), which would state the opposite of the requirement since this control is explicitly the post-compromise phase. Full discussion: OPEN-QUESTIONS.md Q114.
[^0x92-stylometric]: **stylometric** (EN) -> ਸਟਾਈਲੋਮੈਟ੍ਰਿਕ — kept as a loan because stylometry is a named forensic-linguistics discipline, not a description, matching the corpus's treatment of other named disciplines like federated learning. Full discussion: OPEN-QUESTIONS.md Q115.
