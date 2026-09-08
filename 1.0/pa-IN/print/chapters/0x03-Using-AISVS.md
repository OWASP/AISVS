<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x03-Using-AISVS.md -->
<!-- Translator: GeeksikhSecurity -->

# Using the AISVS
# AISVS ਦੀ ਵਰਤੋਂ

The Artificial Intelligence Security Verification Standard (AISVS) defines security requirements for modern AI applications and services, focusing on aspects within the control of application developers.

ਬਣਾਉਟੀ ਬੁੱਧੀ ਸੁਰੱਖਿਆ ਤਸਦੀਕ ਮਿਆਰ (Artificial Intelligence Security Verification Standard, AISVS) ਆਧੁਨਿਕ AI ਐਪਲੀਕੇਸ਼ਨਾਂ ਅਤੇ ਸੇਵਾਵਾਂ ਲਈ ਸੁਰੱਖਿਆ ਲੋੜਾਂ ਪਰਿਭਾਸ਼ਿਤ ਕਰਦਾ ਹੈ, ਅਤੇ ਉਹਨਾਂ ਪਹਿਲੂਆਂ 'ਤੇ ਕੇਂਦ੍ਰਿਤ ਹੈ ਜੋ ਐਪਲੀਕੇਸ਼ਨ ਵਿਕਾਸਕਾਰਾਂ ਦੇ ਨਿਯੰਤਰਣ ਵਿੱਚ ਹਨ।

The AISVS is intended for anyone developing or evaluating the security of AI applications, including developers, architects, security engineers, and auditors. This chapter introduces the structure and use of the AISVS, including its verification levels, intended use cases, and how it is positioned alongside other security standards.

AISVS ਉਹਨਾਂ ਸਾਰਿਆਂ ਲਈ ਹੈ ਜੋ AI ਐਪਲੀਕੇਸ਼ਨਾਂ ਦੀ ਸੁਰੱਖਿਆ ਨੂੰ ਵਿਕਸਤ ਕਰ ਰਹੇ ਹਨ ਜਾਂ ਉਸਦਾ ਮੁਲਾਂਕਣ ਕਰ ਰਹੇ ਹਨ, ਜਿਸ ਵਿੱਚ ਵਿਕਾਸਕਾਰ, ਆਰਕੀਟੈਕਟ, ਸੁਰੱਖਿਆ ਇੰਜੀਨੀਅਰ, ਅਤੇ ਆਡੀਟਰ ਸ਼ਾਮਲ ਹਨ। ਇਹ ਅਧਿਆਇ AISVS ਦੇ ਢਾਂਚੇ ਅਤੇ ਵਰਤੋਂ ਨੂੰ ਪੇਸ਼ ਕਰਦਾ ਹੈ, ਜਿਸ ਵਿੱਚ ਇਸਦੇ ਤਸਦੀਕ ਪੱਧਰ, ਇੱਛਤ ਵਰਤੋਂ-ਮਾਮਲੇ, ਅਤੇ ਇਹ ਹੋਰ ਸੁਰੱਖਿਆ ਮਿਆਰਾਂ ਦੇ ਨਾਲ ਕਿਵੇਂ ਸਥਿਤ ਹੈ, ਸ਼ਾਮਲ ਹਨ।

## How to Read This Standard
## ਇਸ ਮਿਆਰ ਨੂੰ ਕਿਵੇਂ ਪੜ੍ਹਨਾ ਹੈ

### Chapter Structure
### ਅਧਿਆਇ ਢਾਂਚਾ

Each of the 12 requirement chapters follows the same format:

* **Control Objective.** A brief statement of the security goal for the chapter.
* **Sections.** Requirements are grouped into related sections, each with a short description of the defense goal.
* **Requirement Tables.** Individual requirements are presented in tables with the following columns:

12 ਲੋੜ ਅਧਿਆਵਾਂ ਵਿੱਚੋਂ ਹਰ ਇੱਕ ਇੱਕੋ ਫ਼ਾਰਮੈਟ[^0x03-Using-AISVS-format] ਦੀ ਪਾਲਣਾ ਕਰਦਾ ਹੈ:

* **ਨਿਯੰਤਰਣ ਉਦੇਸ਼।** ਅਧਿਆਇ ਲਈ ਸੁਰੱਖਿਆ ਟੀਚੇ ਦਾ ਸੰਖੇਪ ਬਿਆਨ।
* **ਭਾਗ।** ਲੋੜਾਂ ਨੂੰ ਸੰਬੰਧਿਤ ਭਾਗਾਂ ਵਿੱਚ ਵੰਡਿਆ ਗਿਆ ਹੈ, ਹਰ ਭਾਗ ਦੇ ਨਾਲ ਬਚਾਅ ਟੀਚੇ ਦਾ ਸੰਖੇਪ ਵੇਰਵਾ ਦਿੱਤਾ ਗਿਆ ਹੈ।
* **ਲੋੜ ਸਾਰਣੀਆਂ।** ਵਿਅਕਤੀਗਤ ਲੋੜਾਂ ਹੇਠ ਲਿਖੇ ਕਾਲਮਾਂ ਵਾਲੀਆਂ ਸਾਰਣੀਆਂ ਵਿੱਚ ਪੇਸ਼ ਕੀਤੀਆਂ ਗਈਆਂ ਹਨ:

| Column | Meaning |
| --- | --- |
| **#** | Unique requirement identifier (e.g., 1.1.1, 9.3.2). |
| **Description** | The requirement text, always beginning with "Verify that" to emphasize testability. |
| **Level** | The verification level (1, 2, or 3) indicating the depth of assurance required; see the verification levels below. |

| ਕਾਲਮ | ਅਰਥ |
| --- | --- |
| **#** | ਵਿਲੱਖਣ ਲੋੜ ਪਛਾਣਕਰਤਾ (ਜਿਵੇਂ, 1.1.1, 9.3.2)। |
| **ਵੇਰਵਾ** | ਲੋੜ ਦਾ ਪਾਠ, ਜੋ ਪਰਖਯੋਗਤਾ 'ਤੇ ਜ਼ੋਰ ਦੇਣ ਲਈ ਹਮੇਸ਼ਾ "ਤਸਦੀਕ ਕਰੋ ਕਿ" ਨਾਲ ਸ਼ੁਰੂ ਹੁੰਦਾ ਹੈ। |
| **ਪੱਧਰ** | ਤਸਦੀਕ ਪੱਧਰ (1, 2, ਜਾਂ 3) ਜੋ ਲੋੜੀਂਦੇ ਭਰੋਸੇ (assurance) ਦੀ ਡੂੰਘਾਈ ਦਰਸਾਉਂਦਾ ਹੈ; ਹੇਠਾਂ ਦਿੱਤੇ ਤਸਦੀਕ ਪੱਧਰ ਵੇਖੋ। |

### Appendices
### ਅੰਤਿਕਾਵਾਂ

Three appendices support the core requirements:

* **Appendix A (Glossary)** defines key terms and acronyms used throughout the standard.
* **Appendix B (AI Security Controls Inventory)** is a cross-reference of every defense technique in AISVS, organized by security control category (authentication, authorization, encryption, input validation, and so on) with mappings back to specific requirement identifiers.
* **Appendix C (AI-Assisted Secure Coding)** provides controls for the safe use of AI coding tools during software development.

ਤਿੰਨ ਅੰਤਿਕਾਵਾਂ[^0x03-Using-AISVS-appendix] ਮੁੱਖ ਲੋੜਾਂ ਦਾ ਸਮਰਥਨ ਕਰਦੀਆਂ ਹਨ:

* **ਅੰਤਿਕਾ A (ਸ਼ਬਦਾਵਲੀ)** ਪੂਰੇ ਮਿਆਰ ਵਿੱਚ ਵਰਤੇ ਗਏ ਮੁੱਖ ਸ਼ਬਦਾਂ ਅਤੇ ਸੰਖੇਪ-ਰੂਪਾਂ ਨੂੰ ਪਰਿਭਾਸ਼ਿਤ ਕਰਦੀ ਹੈ।
* **ਅੰਤਿਕਾ B (AI ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ ਇਨਵੈਂਟਰੀ)** AISVS ਵਿੱਚ ਹਰ ਬਚਾਅ ਤਕਨੀਕ ਦਾ ਅੰਤਰ-ਹਵਾਲਾ ਹੈ, ਜੋ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ ਸ਼੍ਰੇਣੀ (ਪ੍ਰਮਾਣੀਕਰਨ, ਅਧਿਕਾਰੀਕਰਨ, ਏਨਕ੍ਰਿਪਸ਼ਨ, ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ, ਆਦਿ) ਅਨੁਸਾਰ ਵਿਵਸਥਿਤ ਹੈ ਅਤੇ ਖ਼ਾਸ ਲੋੜ ਪਛਾਣਕਰਤਾਵਾਂ ਨਾਲ ਵਾਪਸ ਮੈਪਿੰਗ ਦਿੰਦਾ ਹੈ।
* **ਅੰਤਿਕਾ C (AI-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਸੁਰੱਖਿਅਤ ਕੋਡਿੰਗ)** ਸਾਫ਼ਟਵੇਅਰ ਵਿਕਾਸ ਦੌਰਾਨ AI ਕੋਡਿੰਗ ਟੂਲਾਂ ਦੀ ਸੁਰੱਖਿਅਤ ਵਰਤੋਂ ਲਈ ਨਿਯੰਤਰਣ ਪ੍ਰਦਾਨ ਕਰਦੀ ਹੈ।

## Artificial Intelligence Security Verification Levels
## ਬਣਾਉਟੀ ਬੁੱਧੀ ਸੁਰੱਖਿਆ ਤਸਦੀਕ ਪੱਧਰ

The AISVS defines three ascending levels of security verification. Each level adds depth and complexity, enabling organizations to tailor their security posture to the risk level of their AI systems.

AISVS ਸੁਰੱਖਿਆ ਤਸਦੀਕ ਦੇ ਤਿੰਨ ਵਧਦੇ ਕ੍ਰਮ ਵਾਲੇ ਪੱਧਰ ਪਰਿਭਾਸ਼ਿਤ ਕਰਦਾ ਹੈ। ਹਰ ਪੱਧਰ ਡੂੰਘਾਈ ਅਤੇ ਜਟਿਲਤਾ ਜੋੜਦਾ ਹੈ, ਜਿਸ ਨਾਲ ਸੰਸਥਾਵਾਂ ਆਪਣੀ ਸੁਰੱਖਿਆ ਸਥਿਤੀ ਨੂੰ ਆਪਣੇ AI ਸਿਸਟਮਾਂ ਦੇ ਜੋਖਮ ਪੱਧਰ ਅਨੁਸਾਰ ਢਾਲ ਸਕਦੀਆਂ ਹਨ।

Organizations may begin at Level 1 and progressively adopt higher levels as security maturity and threat exposure increase. AISVS levels are aligned with [ASVS](https://owasp.org/www-project-application-security-verification-standard/) levels and are intended to be applied at the matching ASVS level (see Alignment with ASVS Levels below).

ਸੰਸਥਾਵਾਂ ਪੱਧਰ 1 ਤੋਂ ਸ਼ੁਰੂ ਕਰ ਸਕਦੀਆਂ ਹਨ ਅਤੇ ਸੁਰੱਖਿਆ ਪਰਿਪੱਕਤਾ ਅਤੇ ਖ਼ਤਰੇ ਦੇ ਸਾਹਮਣੇ ਆਉਣ ਵਿੱਚ ਵਾਧੇ ਦੇ ਨਾਲ-ਨਾਲ ਹੌਲੀ-ਹੌਲੀ ਉੱਚੇ ਪੱਧਰ ਅਪਣਾ ਸਕਦੀਆਂ ਹਨ। AISVS ਪੱਧਰ [ASVS](https://owasp.org/www-project-application-security-verification-standard/) ਪੱਧਰਾਂ ਨਾਲ ਇਕਸਾਰ ਹਨ ਅਤੇ ਇਹਨਾਂ ਨੂੰ ਮੇਲ ਖਾਂਦੇ ASVS ਪੱਧਰ 'ਤੇ ਲਾਗੂ ਕਰਨ ਦਾ ਇਰਾਦਾ ਹੈ (ਹੇਠਾਂ "ASVS ਪੱਧਰਾਂ ਨਾਲ ਇਕਸਾਰਤਾ" ਵੇਖੋ)।

### Definition of the Levels
### ਪੱਧਰਾਂ ਦੀ ਪਰਿਭਾਸ਼ਾ

Each requirement in AISVS v1.0 is assigned to one of the following levels:

AISVS v1.0 ਵਿੱਚ ਹਰ ਲੋੜ ਨੂੰ ਹੇਠ ਲਿਖੇ ਪੱਧਰਾਂ ਵਿੱਚੋਂ ਇੱਕ ਸੌਂਪਿਆ ਗਿਆ ਹੈ:

#### Level 1 requirements
#### ਪੱਧਰ 1 ਦੀਆਂ ਲੋੜਾਂ

Level 1 includes the most critical and foundational security requirements. These focus on preventing common attacks that do not rely on other preconditions or vulnerabilities. Most Level 1 controls are either straightforward to implement or essential enough to justify the effort.

ਪੱਧਰ 1 ਵਿੱਚ ਸਭ ਤੋਂ ਨਾਜ਼ੁਕ ਅਤੇ ਬੁਨਿਆਦੀ ਸੁਰੱਖਿਆ ਲੋੜਾਂ ਸ਼ਾਮਲ ਹਨ। ਇਹ ਉਹਨਾਂ ਆਮ ਹਮਲਿਆਂ ਨੂੰ ਰੋਕਣ 'ਤੇ ਕੇਂਦ੍ਰਿਤ ਹਨ ਜੋ ਹੋਰ ਪੂਰਵ-ਸ਼ਰਤਾਂ ਜਾਂ ਕਮਜ਼ੋਰੀਆਂ 'ਤੇ ਨਿਰਭਰ ਨਹੀਂ ਕਰਦੇ। ਜ਼ਿਆਦਾਤਰ ਪੱਧਰ 1 ਨਿਯੰਤਰਣ ਜਾਂ ਤਾਂ ਲਾਗੂ ਕਰਨ ਵਿੱਚ ਸਿੱਧੇ-ਸਾਦੇ ਹਨ ਜਾਂ ਇੰਨੇ ਜ਼ਰੂਰੀ ਹਨ ਕਿ ਉਹ ਲੱਗਣ ਵਾਲੀ ਮਿਹਨਤ ਨੂੰ ਜਾਇਜ਼ ਠਹਿਰਾਉਂਦੇ ਹਨ।

#### Level 2 requirements
#### ਪੱਧਰ 2 ਦੀਆਂ ਲੋੜਾਂ

Level 2 addresses more advanced or less common attacks, as well as layered defenses against widespread threats. These requirements may involve more complex logic or target specific attack prerequisites.

ਪੱਧਰ 2 ਵਧੇਰੇ ਉੱਨਤ ਜਾਂ ਘੱਟ ਆਮ ਹਮਲਿਆਂ ਨੂੰ, ਨਾਲ ਹੀ ਵਿਆਪਕ ਖ਼ਤਰਿਆਂ ਵਿਰੁੱਧ ਪਰਤਦਾਰ ਬਚਾਵਾਂ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ। ਇਹਨਾਂ ਲੋੜਾਂ ਵਿੱਚ ਵਧੇਰੇ ਗੁੰਝਲਦਾਰ ਤਰਕ ਸ਼ਾਮਲ ਹੋ ਸਕਦਾ ਹੈ ਜਾਂ ਇਹ ਖ਼ਾਸ ਹਮਲਾ ਪੂਰਵ-ਲੋੜਾਂ ਨੂੰ ਨਿਸ਼ਾਨਾ ਬਣਾ ਸਕਦੀਆਂ ਹਨ।

#### Level 3 requirements
#### ਪੱਧਰ 3 ਦੀਆਂ ਲੋੜਾਂ

Level 3 includes controls that are typically harder to implement or situational in applicability. These often represent defense-in-depth mechanisms or mitigations against niche, targeted, or high-complexity attacks.

ਪੱਧਰ 3 ਵਿੱਚ ਉਹ ਨਿਯੰਤਰਣ ਸ਼ਾਮਲ ਹਨ ਜੋ ਆਮ ਤੌਰ 'ਤੇ ਲਾਗੂ ਕਰਨੇ ਔਖੇ ਹੁੰਦੇ ਹਨ ਜਾਂ ਜਿਨ੍ਹਾਂ ਦੀ ਲਾਗੂ ਹੋਣ ਦੀ ਯੋਗਤਾ ਹਾਲਾਤ 'ਤੇ ਨਿਰਭਰ ਕਰਦੀ ਹੈ। ਇਹ ਅਕਸਰ ਡੂੰਘਾਈ ਵਿੱਚ ਬਚਾਅ (defense-in-depth)[^0x03-Using-AISVS-defense-in-depth] ਵਿਧੀਆਂ ਜਾਂ ਸੀਮਤ-ਦਾਇਰੇ, ਨਿਸ਼ਾਨਾਬੱਧ, ਜਾਂ ਉੱਚ-ਜਟਿਲਤਾ ਵਾਲੇ ਹਮਲਿਆਂ ਵਿਰੁੱਧ ਘਟਾਉਣ ਦੇ ਉਪਾਅ ਦਰਸਾਉਂਦੇ ਹਨ।

## Alignment with ASVS Levels
## ASVS ਪੱਧਰਾਂ ਨਾਲ ਇਕਸਾਰਤਾ

AISVS levels are aligned with [ASVS](https://owasp.org/www-project-application-security-verification-standard/) levels. Verifying an AI application against AISVS Level _N_ assumes the application has also been, or is being, verified against ASVS Level _N_. The two standards are designed to be applied together at matching levels:

AISVS ਪੱਧਰ [ASVS](https://owasp.org/www-project-application-security-verification-standard/) ਪੱਧਰਾਂ ਨਾਲ ਇਕਸਾਰ ਹਨ। ਕਿਸੇ AI ਐਪਲੀਕੇਸ਼ਨ ਦੀ AISVS ਪੱਧਰ _N_ ਵਿਰੁੱਧ ਤਸਦੀਕ ਇਹ ਮੰਨ ਕੇ ਚੱਲਦੀ ਹੈ ਕਿ ਉਸ ਐਪਲੀਕੇਸ਼ਨ ਦੀ ASVS ਪੱਧਰ _N_ ਵਿਰੁੱਧ ਵੀ ਤਸਦੀਕ ਹੋ ਚੁੱਕੀ ਹੈ ਜਾਂ ਹੋ ਰਹੀ ਹੈ। ਦੋਵੇਂ ਮਿਆਰ ਮੇਲ ਖਾਂਦੇ ਪੱਧਰਾਂ 'ਤੇ ਇਕੱਠੇ ਲਾਗੂ ਕਰਨ ਲਈ ਤਿਆਰ ਕੀਤੇ ਗਏ ਹਨ:

| AISVS Level | Corresponding ASVS Level | Typical use |
| :---: | :---: | --- |
| 1 | 1 | Baseline security for any AI application that handles untrusted input or operates on data of any sensitivity. |
| 2 | 2 | AI applications handling sensitive business data, regulated data, or operating in adversarial contexts. |
| 3 | 3 | High-assurance AI applications such as those handling life-safety decisions, critical infrastructure, or highly sensitive personal data. |

| AISVS ਪੱਧਰ | ਸੰਬੰਧਿਤ ASVS ਪੱਧਰ | ਆਮ ਵਰਤੋਂ |
| :---: | :---: | --- |
| 1 | 1 | ਕਿਸੇ ਵੀ ਅਜਿਹੀ AI ਐਪਲੀਕੇਸ਼ਨ ਲਈ ਬੁਨਿਆਦੀ ਸੁਰੱਖਿਆ ਜੋ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟ ਸੰਭਾਲਦੀ ਹੈ ਜਾਂ ਕਿਸੇ ਵੀ ਸੰਵੇਦਨਸ਼ੀਲਤਾ ਵਾਲੇ ਡਾਟੇ 'ਤੇ ਕੰਮ ਕਰਦੀ ਹੈ। |
| 2 | 2 | ਸੰਵੇਦਨਸ਼ੀਲ ਕਾਰੋਬਾਰੀ ਡਾਟਾ ਜਾਂ ਨਿਯੰਤ੍ਰਿਤ ਡਾਟਾ ਸੰਭਾਲਣ ਵਾਲੀਆਂ, ਜਾਂ ਵਿਰੋਧੀ ਸੰਦਰਭਾਂ ਵਿੱਚ ਕੰਮ ਕਰਨ ਵਾਲੀਆਂ AI ਐਪਲੀਕੇਸ਼ਨਾਂ। |
| 3 | 3 | ਉੱਚ-ਭਰੋਸੇ ਵਾਲੀਆਂ AI ਐਪਲੀਕੇਸ਼ਨਾਂ, ਜਿਵੇਂ ਕਿ ਜੀਵਨ-ਸਲਾਮਤੀ ਦੇ ਫ਼ੈਸਲੇ, ਨਾਜ਼ੁਕ ਬੁਨਿਆਦੀ ਢਾਂਚਾ, ਜਾਂ ਬਹੁਤ ਸੰਵੇਦਨਸ਼ੀਲ ਨਿੱਜੀ ਡਾਟਾ ਸੰਭਾਲਣ ਵਾਲੀਆਂ ਐਪਲੀਕੇਸ਼ਨਾਂ। |

If an AISVS requirement appears to overlap with an ASVS requirement, the AISVS version is restated only because it has AI-specific implementation details, attack surface, or evidence that an auditor needs to evaluate differently.

ਜੇ ਕੋਈ AISVS ਲੋੜ ਕਿਸੇ ASVS ਲੋੜ ਨਾਲ ਓਵਰਲੈਪ ਹੁੰਦੀ ਜਾਪਦੀ ਹੈ, ਤਾਂ AISVS ਵਾਲਾ ਰੂਪ ਸਿਰਫ਼ ਇਸ ਲਈ ਦੁਬਾਰਾ ਦੱਸਿਆ ਗਿਆ ਹੈ ਕਿਉਂਕਿ ਉਸ ਵਿੱਚ AI-ਵਿਸ਼ੇਸ਼ ਲਾਗੂਕਰਨ ਵੇਰਵੇ, ਹਮਲਾ ਸਤ੍ਹਾ (attack surface), ਜਾਂ ਸਬੂਤ ਹਨ ਜਿਨ੍ਹਾਂ ਦਾ ਮੁਲਾਂਕਣ ਆਡੀਟਰ ਨੂੰ ਵੱਖਰੇ ਢੰਗ ਨਾਲ ਕਰਨਾ ਪੈਂਦਾ ਹੈ।

## Scope of the AISVS
## AISVS ਦਾ ਦਾਇਰਾ

AISVS is intentionally narrow. It only defines security requirements that are specific to AI and ML systems, or where general security controls have AI-specific nuances that warrant restating. It is not a self-contained security program for an AI application. AISVS assumes that the underlying application, infrastructure, and organizational practices are already verified against established general-purpose standards, and adds the AI-specific layer.

AISVS ਜਾਣ-ਬੁੱਝ ਕੇ ਸੀਮਤ ਦਾਇਰੇ ਵਾਲਾ ਹੈ। ਇਹ ਸਿਰਫ਼ ਉਹ ਸੁਰੱਖਿਆ ਲੋੜਾਂ ਪਰਿਭਾਸ਼ਿਤ ਕਰਦਾ ਹੈ ਜੋ AI ਅਤੇ ML ਸਿਸਟਮਾਂ ਲਈ ਵਿਸ਼ੇਸ਼ ਹਨ, ਜਾਂ ਜਿੱਥੇ ਆਮ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣਾਂ ਵਿੱਚ AI-ਵਿਸ਼ੇਸ਼ ਬਾਰੀਕੀਆਂ ਹਨ ਜੋ ਦੁਬਾਰਾ ਦੱਸਣ ਯੋਗ ਹਨ। ਇਹ ਕਿਸੇ AI ਐਪਲੀਕੇਸ਼ਨ ਲਈ ਸਵੈ-ਨਿਰਭਰ ਸੁਰੱਖਿਆ ਪ੍ਰੋਗਰਾਮ ਨਹੀਂ ਹੈ। AISVS ਇਹ ਮੰਨ ਕੇ ਚੱਲਦਾ ਹੈ ਕਿ ਹੇਠਲੀ ਐਪਲੀਕੇਸ਼ਨ, ਬੁਨਿਆਦੀ ਢਾਂਚਾ, ਅਤੇ ਸੰਸਥਾਗਤ ਅਭਿਆਸ ਪਹਿਲਾਂ ਹੀ ਸਥਾਪਿਤ ਆਮ-ਮਕਸਦ ਮਿਆਰਾਂ ਵਿਰੁੱਧ ਤਸਦੀਕ ਕੀਤੇ ਜਾ ਚੁੱਕੇ ਹਨ, ਅਤੇ ਇਹ ਉਹਨਾਂ ਉੱਤੇ AI-ਵਿਸ਼ੇਸ਼ ਪਰਤ ਜੋੜਦਾ ਹੈ।

The following are intentionally out of scope and are not duplicated in AISVS chapters:

* **General application security.** Authentication, session management, authorization, transport security, input and output handling for non-AI surfaces, secrets management, file upload handling, error handling, and similar controls are defined by the [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/).
* **General software supply chain security.** Dependency scanning, version pinning, lockfile enforcement, build provenance, reproducible builds, generic SBOM generation, and CI/CD pipeline integrity are defined by the [OWASP Software Component Verification Standard (SCVS)](https://owasp.org/www-project-software-component-verification-standard/), [SLSA](https://slsa.dev/), and the [CIS Controls](https://www.cisecurity.org/controls).
* **General infrastructure and platform hardening.** Container, host, network, cloud, and Kubernetes baseline hardening are defined by the [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks), [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), [NIST SP 800-190](https://csrc.nist.gov/pubs/sp/800/190/final), and the [NIST Cybersecurity Framework (CSF)](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20).
* **General data protection and privacy operations.** Data classification, encryption at rest and in transit, retention scheduling, secure deletion of conventional storage, audit log immutability, and consent management platform operation are defined by ASVS, [ISO/IEC 27001](https://www.iso.org/standard/27001), and applicable privacy regulations such as the GDPR.
* **General logging and monitoring.** Log storage access control, retention, backup, encryption, redaction, tamper protection, SIEM integration, and operational telemetry are defined by ASVS and standard observability practice.
* **AI governance and risk management.** Organizational AI governance, AI impact assessments, fairness and ethics documentation, model cards, public transparency reports, and risk-management process design are defined by [ISO/IEC 42001](https://www.iso.org/standard/81230.html), [ISO/IEC 23894](https://www.iso.org/standard/77304.html), and the [NIST AI RMF](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10).
* **Vendor-specific guidance.** AISVS is vendor-neutral. It specifies what to verify, not which product to use.

ਹੇਠ ਲਿਖੀਆਂ ਗੱਲਾਂ ਜਾਣ-ਬੁੱਝ ਕੇ ਦਾਇਰੇ ਤੋਂ ਬਾਹਰ ਹਨ ਅਤੇ AISVS ਅਧਿਆਵਾਂ ਵਿੱਚ ਦੁਹਰਾਈਆਂ ਨਹੀਂ ਗਈਆਂ:

* **ਆਮ ਐਪਲੀਕੇਸ਼ਨ ਸੁਰੱਖਿਆ।** ਪ੍ਰਮਾਣੀਕਰਨ, ਸੈਸ਼ਨ ਪ੍ਰਬੰਧਨ, ਅਧਿਕਾਰੀਕਰਨ, ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ[^0x03-Using-AISVS-transport], ਗ਼ੈਰ-AI ਸਤ੍ਹਾਵਾਂ ਲਈ ਇਨਪੁੱਟ ਅਤੇ ਆਊਟਪੁੱਟ ਪ੍ਰਬੰਧਨ, ਗੁਪਤ ਭੇਦ ਪ੍ਰਬੰਧਨ, ਫ਼ਾਈਲ ਅਪਲੋਡ ਪ੍ਰਬੰਧਨ, ਗਲਤੀ ਪ੍ਰਬੰਧਨ, ਅਤੇ ਇਸੇ ਤਰ੍ਹਾਂ ਦੇ ਨਿਯੰਤਰਣ [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) ਦੁਆਰਾ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤੇ ਗਏ ਹਨ।
* **ਆਮ ਸਾਫ਼ਟਵੇਅਰ ਸਪਲਾਈ ਚੇਨ ਸੁਰੱਖਿਆ।** ਡਿਪੈਂਡੈਂਸੀ ਸਕੈਨਿੰਗ, ਵਰਜ਼ਨ ਪਿੰਨਿੰਗ, ਲੌਕਫ਼ਾਈਲ ਲਾਗੂਕਰਨ, ਬਿਲਡ ਮੂਲ-ਸਰੋਤ (build provenance)[^0x03-Using-AISVS-provenance], ਦੁਹਰਾਉਣਯੋਗ ਬਿਲਡ, ਆਮ SBOM ਤਿਆਰੀ, ਅਤੇ CI/CD ਪਾਈਪਲਾਈਨ ਅਖੰਡਤਾ [OWASP Software Component Verification Standard (SCVS)](https://owasp.org/www-project-software-component-verification-standard/), [SLSA](https://slsa.dev/), ਅਤੇ [CIS Controls](https://www.cisecurity.org/controls) ਦੁਆਰਾ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤੇ ਗਏ ਹਨ।
* **ਆਮ ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਅਤੇ ਪਲੇਟਫ਼ਾਰਮ ਸਖ਼ਤੀਕਰਨ।** ਕੰਟੇਨਰ, ਹੋਸਟ, ਨੈੱਟਵਰਕ, ਕਲਾਊਡ, ਅਤੇ Kubernetes ਦਾ ਬੁਨਿਆਦੀ ਸਖ਼ਤੀਕਰਨ [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks), [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), [NIST SP 800-190](https://csrc.nist.gov/pubs/sp/800/190/final), ਅਤੇ [NIST Cybersecurity Framework (CSF)](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) ਦੁਆਰਾ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤਾ ਗਿਆ ਹੈ।
* **ਆਮ ਡਾਟਾ ਸੁਰੱਖਿਆ ਅਤੇ ਨਿੱਜਤਾ ਸੰਚਾਲਨ।** ਡਾਟਾ ਵਰਗੀਕਰਨ, ਭੰਡਾਰਨ ਅਤੇ ਪ੍ਰਸਾਰਣ ਵਿੱਚ ਏਨਕ੍ਰਿਪਸ਼ਨ, ਧਾਰਨ ਸਮਾਂ-ਸੂਚੀ, ਰਵਾਇਤੀ ਭੰਡਾਰਨ ਦੀ ਸੁਰੱਖਿਅਤ ਮਿਟਾਈ, ਆਡਿਟ ਲੌਗ ਦੀ ਅਪਰਿਵਰਤਨਸ਼ੀਲਤਾ[^0x03-Using-AISVS-immutable], ਅਤੇ ਸਹਿਮਤੀ ਪ੍ਰਬੰਧਨ[^0x03-Using-AISVS-consent] ਪਲੇਟਫ਼ਾਰਮ ਦਾ ਸੰਚਾਲਨ ASVS, [ISO/IEC 27001](https://www.iso.org/standard/27001), ਅਤੇ ਲਾਗੂ ਹੋਣ ਵਾਲੇ ਨਿੱਜਤਾ ਨਿਯਮਾਂ ਜਿਵੇਂ ਕਿ GDPR ਦੁਆਰਾ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤੇ ਗਏ ਹਨ।
* **ਆਮ ਲੌਗਿੰਗ ਅਤੇ ਨਿਗਰਾਨੀ।** ਲੌਗ ਭੰਡਾਰਨ ਦਾ ਪਹੁੰਚ ਕੰਟਰੋਲ, ਧਾਰਨ, ਬੈਕਅੱਪ, ਏਨਕ੍ਰਿਪਸ਼ਨ, ਰਿਡੈਕਸ਼ਨ, ਛੇੜਛਾੜ ਸੁਰੱਖਿਆ, SIEM ਏਕੀਕਰਨ, ਅਤੇ ਸੰਚਾਲਨ ਟੈਲੀਮੈਟਰੀ ASVS ਅਤੇ ਮਿਆਰੀ ਨਿਰੀਖਣਯੋਗਤਾ (observability) ਅਭਿਆਸ ਦੁਆਰਾ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤੇ ਗਏ ਹਨ।
* **AI ਸ਼ਾਸਨ ਅਤੇ ਜੋਖਮ ਪ੍ਰਬੰਧਨ।** ਸੰਸਥਾਗਤ AI ਸ਼ਾਸਨ, AI ਪ੍ਰਭਾਵ ਮੁਲਾਂਕਣ, ਨਿਰਪੱਖਤਾ ਅਤੇ ਨੈਤਿਕਤਾ ਦਸਤਾਵੇਜ਼ੀਕਰਨ, ਮਾਡਲ ਕਾਰਡ[^0x03-Using-AISVS-model-card], ਜਨਤਕ ਪਾਰਦਰਸ਼ਤਾ[^0x03-Using-AISVS-transparency] ਰਿਪੋਰਟਾਂ, ਅਤੇ ਜੋਖਮ-ਪ੍ਰਬੰਧਨ ਪ੍ਰਕਿਰਿਆ ਦਾ ਡਿਜ਼ਾਈਨ [ISO/IEC 42001](https://www.iso.org/standard/81230.html), [ISO/IEC 23894](https://www.iso.org/standard/77304.html), ਅਤੇ [NIST AI RMF](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) ਦੁਆਰਾ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤੇ ਗਏ ਹਨ।
* **ਵਿਕਰੇਤਾ-ਵਿਸ਼ੇਸ਼ ਮਾਰਗਦਰਸ਼ਨ।** AISVS ਵਿਕਰੇਤਾ-ਨਿਰਪੱਖ ਹੈ। ਇਹ ਦੱਸਦਾ ਹੈ ਕਿ ਕੀ ਤਸਦੀਕ ਕਰਨਾ ਹੈ, ਨਾ ਕਿ ਕਿਹੜਾ ਉਤਪਾਦ ਵਰਤਣਾ ਹੈ।

When verifying an AI application against AISVS, the equivalent level of those underlying standards should be verified in parallel.

ਕਿਸੇ AI ਐਪਲੀਕੇਸ਼ਨ ਦੀ AISVS ਵਿਰੁੱਧ ਤਸਦੀਕ ਕਰਦੇ ਸਮੇਂ, ਉਹਨਾਂ ਹੇਠਲੇ ਮਿਆਰਾਂ ਦੇ ਬਰਾਬਰ ਪੱਧਰ ਦੀ ਤਸਦੀਕ ਨਾਲੋ-ਨਾਲ ਕੀਤੀ ਜਾਣੀ ਚਾਹੀਦੀ ਹੈ।

## Cross-References Inside AISVS
## AISVS ਦੇ ਅੰਦਰ ਅੰਤਰ-ਹਵਾਲੇ

AISVS chapters are organized by control family rather than by attack or component. As a result, defending against a given AI threat usually requires applying requirements from several chapters together. For example, defending against prompt injection in an agentic application combines requirements from C2 (input validation), C7 (model behavior), C9 (orchestration and agentic security), C10 (MCP-specific controls), C11 (adversarial robustness), and C12 (detection and logging).

AISVS ਅਧਿਆਇ ਹਮਲੇ ਜਾਂ ਹਿੱਸੇ[^0x03-Using-AISVS-component] ਦੀ ਬਜਾਏ ਨਿਯੰਤਰਣ ਪਰਿਵਾਰ[^0x03-Using-AISVS-control-family] ਅਨੁਸਾਰ ਵਿਵਸਥਿਤ ਹਨ। ਨਤੀਜੇ ਵਜੋਂ, ਕਿਸੇ ਦਿੱਤੇ AI ਖ਼ਤਰੇ ਵਿਰੁੱਧ ਬਚਾਅ ਲਈ ਆਮ ਤੌਰ 'ਤੇ ਕਈ ਅਧਿਆਵਾਂ ਦੀਆਂ ਲੋੜਾਂ ਨੂੰ ਇਕੱਠੇ ਲਾਗੂ ਕਰਨਾ ਪੈਂਦਾ ਹੈ। ਉਦਾਹਰਨ ਲਈ, ਕਿਸੇ ਏਜੰਟ-ਆਧਾਰਿਤ (agentic)[^0x03-Using-AISVS-agent-based] ਐਪਲੀਕੇਸ਼ਨ ਵਿੱਚ prompt ਇੰਜੈਕਸ਼ਨ ਵਿਰੁੱਧ ਬਚਾਅ C2 (ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ), C7 (ਮਾਡਲ ਵਿਵਹਾਰ), C9 (ਆਰਕੈਸਟ੍ਰੇਸ਼ਨ[^0x03-Using-AISVS-orchestration] ਅਤੇ ਏਜੰਟ-ਆਧਾਰਿਤ ਸੁਰੱਖਿਆ), C10 (MCP-ਵਿਸ਼ੇਸ਼ ਨਿਯੰਤਰਣ), C11 (ਵਿਰੋਧੀ ਮਜ਼ਬੂਤੀ[^0x03-Using-AISVS-adversarial-robustness]), ਅਤੇ C12 (ਪਛਾਣ ਅਤੇ ਲੌਗਿੰਗ) ਦੀਆਂ ਲੋੜਾਂ ਨੂੰ ਜੋੜਦਾ ਹੈ।

When applying AISVS, treat the standard as a whole and consult Appendix B (AI Security Controls Inventory) for a cross-cutting view of where each defense technique appears.

AISVS ਲਾਗੂ ਕਰਦੇ ਸਮੇਂ, ਮਿਆਰ ਨੂੰ ਸਮੁੱਚੇ ਰੂਪ ਵਿੱਚ ਲਵੋ ਅਤੇ ਹਰ ਬਚਾਅ ਤਕਨੀਕ ਕਿੱਥੇ-ਕਿੱਥੇ ਆਉਂਦੀ ਹੈ, ਇਸਦੇ ਅੰਤਰ-ਵਿਆਪੀ ਦ੍ਰਿਸ਼ ਲਈ ਅੰਤਿਕਾ B (AI ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ ਇਨਵੈਂਟਰੀ) ਵੇਖੋ।

## AISVS Requirements and Scope in Assessments
## ਮੁਲਾਂਕਣਾਂ ਵਿੱਚ AISVS ਲੋੜਾਂ ਅਤੇ ਦਾਇਰਾ

Requirements can often be assessed using a combination of technical testing and vendor documentation, such as model cards for AI models. Another option is to mark requirements outside the organization's control as out of scope.

ਲੋੜਾਂ ਦਾ ਮੁਲਾਂਕਣ ਅਕਸਰ ਤਕਨੀਕੀ ਪਰਖ ਅਤੇ ਵਿਕਰੇਤਾ ਦਸਤਾਵੇਜ਼ੀਕਰਨ — ਜਿਵੇਂ ਕਿ AI ਮਾਡਲਾਂ ਲਈ ਮਾਡਲ ਕਾਰਡ — ਦੇ ਸੁਮੇਲ ਨਾਲ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ। ਇੱਕ ਹੋਰ ਵਿਕਲਪ ਇਹ ਹੈ ਕਿ ਸੰਸਥਾ ਦੇ ਨਿਯੰਤਰਣ ਤੋਂ ਬਾਹਰ ਦੀਆਂ ਲੋੜਾਂ ਨੂੰ ਦਾਇਰੇ ਤੋਂ ਬਾਹਰ ਵਜੋਂ ਚਿੰਨ੍ਹਿਤ ਕੀਤਾ ਜਾਵੇ।

[^0x03-Using-AISVS-format]: **format** (EN) -> ਫ਼ਾਰਮੈਟ — spelled with nukta (ਫ਼) for English /f/, correcting a corpus-wide split where "format" and "platform" appeared both with and without the nukta in different chapters. Full discussion: OPEN-QUESTIONS.md Q86.
[^0x03-Using-AISVS-appendix]: **Appendix** (EN) -> ਅੰਤਿਕਾ — the settled Panjabi term for a document appendix; the division letter (A/B/C) stays Latin as a cross-reference target, matching how requirement IDs are kept unconverted. Full discussion: OPEN-QUESTIONS.md Q121.
[^0x03-Using-AISVS-defense-in-depth]: **Defense-in-Depth** (EN, retained) -> ਡੂੰਘਾਈ ਵਿੱਚ ਬਚਾਅ — the named security doctrine keeps its fixed English name, as auditors and the NIST/CIS literature use it, with a literal Panjabi gloss; this file's hyphenation was normalised to match Appendix A after a corpus audit found it diverging. Full discussion: OPEN-QUESTIONS.md Q141.
[^0x03-Using-AISVS-transport]: **transport security** (EN) -> ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ — ਟ੍ਰਾਂਸਪੋਰਟ is kept a loan rather than translated (e.g. ਢੋਆ-ਢੁਆਈ, "freight," would be absurd for a protocol channel); this compound is the conformance anchor the C10 (MCP transport) chapter matches later. Full discussion: OPEN-QUESTIONS.md Q90.
[^0x03-Using-AISVS-provenance]: **provenance** (EN, in "build provenance") -> ਮੂਲ-ਸਰੋਤ ("root-source") — states "documented chain of origin" plainly, avoiding ਉਤਪਤੀ's creation-narrative/devotional overtone. Full discussion: OPEN-QUESTIONS.md Q73.
[^0x03-Using-AISVS-immutable]: **immutability** (EN, "audit log immutability") -> ਅਪਰਿਵਰਤਨਸ਼ੀਲਤਾ — the settled adjective/noun form, kept consistent with C12 and Appendix C rather than paraphrased as "cannot be changed," so the term stays searchable across the corpus. Full discussion: OPEN-QUESTIONS.md Q112.
[^0x03-Using-AISVS-consent]: **consent** (EN, "consent management platform") -> ਸਹਿਮਤੀ — fixes ਸਹਿਮਤੀ to *consent* corpus-wide, deliberately keeping ਮਨਜ਼ੂਰੀ free for *approval* so the two obligations do not collapse into one word in C10. Full discussion: OPEN-QUESTIONS.md Q93.
[^0x03-Using-AISVS-model-card]: **model card** (EN) -> ਮਾਡਲ ਕਾਰਡ — kept as a loan pair rather than a descriptive phrase (e.g. "documentation") because a model card is a named artifact type with a fixed evidentiary meaning; a vaguer rendering would soften what an auditor can accept as proof. Full discussion: OPEN-QUESTIONS.md Q85.
[^0x03-Using-AISVS-transparency]: **transparency** (EN, "public transparency reports") -> ਪਾਰਦਰਸ਼ਤਾ — reserved for *transparency* specifically so Appendix C can use a different word (ਵਿਆਖਿਆਯੋਗਤਾ) for the separate governance concept of *explainability*. Full discussion: OPEN-QUESTIONS.md Q120.
[^0x03-Using-AISVS-component]: **component** (EN, "attack or component") -> ਹਿੱਸੇ — correct here because the source means a generic part, not a named system component; other chapters split between ਹਿੱਸਾ and the loan ਕੰਪੋਨੈਂਟ for the term-of-art sense, a corpus-wide split that is logged but not yet resolved. Full discussion: OPEN-QUESTIONS.md Q95.
[^0x03-Using-AISVS-control-family]: **control family** (EN) -> ਨਿਯੰਤਰਣ ਪਰਿਵਾਰ — ਪਰਿਵਾਰ mirrors the English "family" metaphor and matches how NIST SP 800-53 control families are discussed in Panjabi security writing; recorded again here because the term recurs in every control chapter and must not drift. Full discussion: OPEN-QUESTIONS.md Q80.
[^0x03-Using-AISVS-agent-based]: **agentic / agent-based** (EN) -> ਏਜੰਟ-ਆਧਾਰਿਤ — normalised to the long-vowel ਆਧਾਰਿਤ (never the short ਅਧਾਰਿਤ) after a cross-file audit found this file internally split between the two spellings for the same compound. Full discussion: OPEN-QUESTIONS.md Q71.
[^0x03-Using-AISVS-orchestration]: **orchestration** (EN, C09 title) -> ਆਰਕੈਸਟ੍ਰੇਸ਼ਨ — kept as a loan because the nearest native word, ਤਾਲਮੇਲ ("coordination"), loses the specific sense of a control plane driving multi-step model/tool/agent execution. Full discussion: OPEN-QUESTIONS.md Q83.
[^0x03-Using-AISVS-adversarial-robustness]: **adversarial robustness** (EN, C11 title) -> ਵਿਰੋਧੀ ਮਜ਼ਬੂਤੀ — ਮਜ਼ਬੂਤੀ ("sturdiness") was chosen over ਦ੍ਰਿੜ੍ਹਤਾ ("steadfastness/resolve"), which would ascribe an inner quality to a model. Full discussion: OPEN-QUESTIONS.md Q84.
