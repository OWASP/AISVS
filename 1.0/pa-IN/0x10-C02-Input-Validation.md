<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C02-Input-Validation.md -->
<!-- Translator: GeeksikhSecurity -->

# C2 Input Validation
# C2 ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses validation of all inputs as a first-line defense against prompt injection, one of the most damaging attacks on AI systems.

ਇਹ ਅਧਿਆਇ prompt ਇੰਜੈਕਸ਼ਨ — AI ਸਿਸਟਮਾਂ ਉੱਤੇ ਸਭ ਤੋਂ ਵੱਧ ਨੁਕਸਾਨਦੇਹ ਹਮਲਿਆਂ ਵਿੱਚੋਂ ਇੱਕ — ਦੇ ਵਿਰੁੱਧ ਪਹਿਲੀ-ਕਤਾਰ ਬਚਾਅ ਵਜੋਂ ਸਾਰੇ ਇਨਪੁੱਟਾਂ ਦੀ ਪ੍ਰਮਾਣਿਕਤਾ (validation) ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ।

---

## C2.1 Prompt Injection Defenses
## C2.1 Prompt ਇੰਜੈਕਸ਼ਨ ਬਚਾਅ

Prompt injection is one of the top risks for AI systems, and defending against it requires a combination of pattern filters, data classifiers, and instruction hierarchy enforcement.

Prompt ਇੰਜੈਕਸ਼ਨ AI ਸਿਸਟਮਾਂ ਲਈ ਸਭ ਤੋਂ ਵੱਡੇ ਜੋਖਮਾਂ ਵਿੱਚੋਂ ਇੱਕ ਹੈ, ਅਤੇ ਇਸ ਦੇ ਵਿਰੁੱਧ ਬਚਾਅ ਲਈ ਪੈਟਰਨ ਫ਼ਿਲਟਰਾਂ, ਡਾਟਾ ਵਰਗੀਕਾਰਾਂ (classifiers), ਅਤੇ ਹਦਾਇਤ ਲੜੀ-ਕ੍ਰਮ (instruction hierarchy) ਨੂੰ ਲਾਗੂ ਕਰਨ ਦੇ ਸੁਮੇਲ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.1.1** | **Verify that** input normalization is applied before tokenization or embedding. | 1 |
| **2.1.2** | **Verify that** encoding and representation smuggling in inputs is detected and mitigated. Approved mitigations include canonicalization, strict schema validation, policy-based rejection, or explicit marking. | 1 |
| **2.1.3** | **Verify that** all inputs that could steer model behavior are treated as untrusted and screened by a prompt injection detection ruleset or classifier, with flagged inputs blocked. | 1 |
| **2.1.4** | **Verify that** input length controls prevent content from exceeding the context window. The controls must reject inputs that exceed token limits rather than truncating them. | 1 |
| **2.1.5** | **Verify that** the system implements a character set restriction for all inputs. The restriction must use an allow-list approach that permits only characters that are explicitly required. | 1 |
| **2.1.6** | **Verify that** the system enforces an instruction hierarchy in which system and developer messages override user instructions and other untrusted inputs, even after user instructions have been processed. | 2 |
| **2.1.7** | **Verify that** reserved special tokens are encoded as literal characters and cannot be injected into the model context. | 2 |
| **2.1.8** | **Verify that** the system can detect many-shot jailbreaking patterns. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਟੋਕਨਾਈਜ਼ੇਸ਼ਨ (tokenization) ਜਾਂ embedding ਤੋਂ ਪਹਿਲਾਂ ਇਨਪੁੱਟ ਸਧਾਰਨੀਕਰਨ (normalization) ਲਾਗੂ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **2.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇਨਪੁੱਟਾਂ ਵਿੱਚ ਏਨਕੋਡਿੰਗ ਅਤੇ ਪ੍ਰਤੀਨਿਧਤਾ ਤਸਕਰੀ (representation smuggling) ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਇਸ ਨੂੰ ਘਟਾਇਆ ਜਾਂਦਾ ਹੈ। ਪ੍ਰਵਾਨਿਤ ਉਪਾਵਾਂ ਵਿੱਚ ਕੈਨੋਨੀਕਲਾਈਜ਼ੇਸ਼ਨ (canonicalization), ਸਖ਼ਤ ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ, ਨੀਤੀ-ਆਧਾਰਿਤ ਰੱਦਗੀ, ਜਾਂ ਸਪੱਸ਼ਟ ਨਿਸ਼ਾਨਦੇਹੀ ਸ਼ਾਮਲ ਹਨ। | 1 |
| **2.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਉਹ ਸਾਰੇ ਇਨਪੁੱਟ ਜੋ ਮਾਡਲ ਦੇ ਵਿਵਹਾਰ ਨੂੰ ਦਿਸ਼ਾ ਦੇ ਸਕਦੇ ਹਨ, ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਮੰਨੇ ਜਾਂਦੇ ਹਨ ਅਤੇ ਇੱਕ prompt ਇੰਜੈਕਸ਼ਨ ਪਛਾਣ ਨਿਯਮ-ਸਮੂਹ ਜਾਂ ਵਰਗੀਕਾਰ ਦੁਆਰਾ ਛਾਣੇ ਜਾਂਦੇ ਹਨ, ਅਤੇ ਨਿਸ਼ਾਨਬੱਧ ਕੀਤੇ ਇਨਪੁੱਟ ਰੋਕ ਦਿੱਤੇ ਜਾਂਦੇ ਹਨ। | 1 |
| **2.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇਨਪੁੱਟ ਲੰਬਾਈ ਨਿਯੰਤਰਣ ਸਮੱਗਰੀ ਨੂੰ ਸੰਦਰਭ ਵਿੰਡੋ (context window) ਤੋਂ ਵੱਧ ਜਾਣ ਤੋਂ ਰੋਕਦੇ ਹਨ। ਇਹਨਾਂ ਨਿਯੰਤਰਣਾਂ ਲਈ ਟੋਕਨ ਸੀਮਾਵਾਂ ਤੋਂ ਵੱਧ ਜਾਣ ਵਾਲੇ ਇਨਪੁੱਟਾਂ ਨੂੰ ਕੱਟਣ (truncate) ਦੀ ਬਜਾਏ ਰੱਦ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ। | 1 |
| **2.1.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਸਟਮ ਸਾਰੇ ਇਨਪੁੱਟਾਂ ਲਈ ਇੱਕ ਅੱਖਰ-ਸਮੂਹ (character set) ਪਾਬੰਦੀ ਲਾਗੂ ਕਰਦਾ ਹੈ। ਇਸ ਪਾਬੰਦੀ ਲਈ allow-list ਤਰੀਕਾ ਵਰਤਣਾ ਲਾਜ਼ਮੀ ਹੈ ਜੋ ਸਿਰਫ਼ ਉਹਨਾਂ ਅੱਖਰਾਂ ਦੀ ਆਗਿਆ ਦਿੰਦਾ ਹੈ ਜੋ ਸਪੱਸ਼ਟ ਤੌਰ 'ਤੇ ਲੋੜੀਂਦੇ ਹਨ। | 1 |
| **2.1.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਸਟਮ ਇੱਕ ਹਦਾਇਤ ਲੜੀ-ਕ੍ਰਮ (instruction hierarchy) ਲਾਗੂ ਕਰਦਾ ਹੈ ਜਿਸ ਵਿੱਚ ਸਿਸਟਮ ਅਤੇ ਡਿਵੈਲਪਰ ਸੁਨੇਹੇ ਉਪਭੋਗਤਾ ਹਦਾਇਤਾਂ ਅਤੇ ਹੋਰ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟਾਂ ਉੱਤੇ ਭਾਰੂ ਰਹਿੰਦੇ ਹਨ, ਭਾਵੇਂ ਉਪਭੋਗਤਾ ਹਦਾਇਤਾਂ ਦੀ ਪ੍ਰਕਿਰਿਆ ਹੋ ਚੁੱਕੀ ਹੋਵੇ। | 2 |
| **2.1.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਰਾਖਵੇਂ ਵਿਸ਼ੇਸ਼ ਟੋਕਨ ਸ਼ਾਬਦਿਕ ਅੱਖਰਾਂ ਵਜੋਂ ਏਨਕੋਡ ਕੀਤੇ ਜਾਂਦੇ ਹਨ ਅਤੇ ਮਾਡਲ ਸੰਦਰਭ ਵਿੱਚ ਇੰਜੈਕਟ ਨਹੀਂ ਕੀਤੇ ਜਾ ਸਕਦੇ। | 2 |
| **2.1.8** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਿਸਟਮ many-shot jailbreaking ਪੈਟਰਨਾਂ ਦਾ ਪਤਾ ਲਗਾ ਸਕਦਾ ਹੈ। | 3 |

---

## C2.2 Content & Policy Screening
## C2.2 ਸਮੱਗਰੀ ਅਤੇ ਨੀਤੀ ਛਾਣਬੀਣ

Syntactically valid prompts may still request disallowed content such as policy-violating instructions, harmful material, or restricted information. Input-side content screening prevents such prompts from reaching the model.

ਵਾਕ-ਬਣਤਰ ਪੱਖੋਂ ਜਾਇਜ਼ prompt ਵੀ ਮਨਾਹੀ ਵਾਲੀ ਸਮੱਗਰੀ ਦੀ ਮੰਗ ਕਰ ਸਕਦੇ ਹਨ, ਜਿਵੇਂ ਕਿ ਨੀਤੀ ਦੀ ਉਲੰਘਣਾ ਕਰਨ ਵਾਲੀਆਂ ਹਦਾਇਤਾਂ, ਨੁਕਸਾਨਦੇਹ ਸਮੱਗਰੀ, ਜਾਂ ਪਾਬੰਦੀਸ਼ੁਦਾ ਜਾਣਕਾਰੀ। ਇਨਪੁੱਟ-ਪਾਸੇ ਦੀ ਸਮੱਗਰੀ ਛਾਣਬੀਣ ਅਜਿਹੇ prompt ਨੂੰ ਮਾਡਲ ਤੱਕ ਪਹੁੰਚਣ ਤੋਂ ਰੋਕਦੀ ਹੈ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.2.1** | **Verify that** every prompt is scored by a content classifier for violence, self-harm, hate, and sexual content against configurable thresholds. Prompts that exceed those thresholds are rejected or sanitized before reaching the model context. | 1 |
| **2.2.2** | **Verify that** prompt content classification is evaluated for unsupported languages. | 1 |
| **2.2.3** | **Verify that** non-text inputs (image/video/audio) are checked for adversarial perturbations, steganographic payloads, hidden or embedded content, or known attack patterns. | 2 |
| **2.2.4** | **Verify that** coordinated attacks spanning multiple input types (e.g., steganographic payloads in images combined with prompt injection in text) are detected and blocked. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **2.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ prompt ਨੂੰ ਹਿੰਸਾ, ਸਵੈ-ਨੁਕਸਾਨ, ਨਫ਼ਰਤ, ਅਤੇ ਜਿਨਸੀ ਸਮੱਗਰੀ ਲਈ ਇੱਕ ਸਮੱਗਰੀ ਵਰਗੀਕਾਰ ਦੁਆਰਾ ਸੰਰਚਨਾਯੋਗ ਥ੍ਰੈਸ਼ਹੋਲਡਾਂ (thresholds) ਦੇ ਵਿਰੁੱਧ ਅੰਕ ਦਿੱਤੇ ਜਾਂਦੇ ਹਨ। ਜਿਹੜੇ prompt ਇਹਨਾਂ ਥ੍ਰੈਸ਼ਹੋਲਡਾਂ ਤੋਂ ਵੱਧ ਜਾਂਦੇ ਹਨ, ਉਹਨਾਂ ਨੂੰ ਮਾਡਲ ਸੰਦਰਭ ਤੱਕ ਪਹੁੰਚਣ ਤੋਂ ਪਹਿਲਾਂ ਰੱਦ ਜਾਂ ਸੈਨੀਟਾਈਜ਼ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **2.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** prompt ਸਮੱਗਰੀ ਵਰਗੀਕਰਨ ਦਾ ਗ਼ੈਰ-ਸਮਰਥਿਤ ਭਾਸ਼ਾਵਾਂ ਲਈ ਮੁਲਾਂਕਣ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **2.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਗ਼ੈਰ-ਲਿਖਤੀ ਇਨਪੁੱਟਾਂ (ਚਿੱਤਰ/ਵੀਡੀਓ/ਆਡੀਓ) ਦੀ ਵਿਰੋਧੀ ਵਿਗਾੜਾਂ (adversarial perturbations), ਸਟੈਗਨੋਗ੍ਰਾਫ਼ਿਕ ਪੇਲੋਡਾਂ, ਲੁਕਵੀਂ ਜਾਂ ਜੜੀ ਹੋਈ ਸਮੱਗਰੀ, ਜਾਂ ਜਾਣੇ-ਪਛਾਣੇ ਹਮਲਾ ਪੈਟਰਨਾਂ ਲਈ ਜਾਂਚ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। | 2 |
| **2.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਕਈ ਇਨਪੁੱਟ ਕਿਸਮਾਂ ਵਿੱਚ ਫੈਲੇ ਤਾਲਮੇਲ ਵਾਲੇ ਹਮਲਿਆਂ (ਜਿਵੇਂ, ਚਿੱਤਰਾਂ ਵਿੱਚ ਸਟੈਗਨੋਗ੍ਰਾਫ਼ਿਕ ਪੇਲੋਡ ਜੋ ਲਿਖਤ ਵਿੱਚ prompt ਇੰਜੈਕਸ਼ਨ ਨਾਲ ਜੋੜੇ ਗਏ ਹੋਣ) ਦਾ ਪਤਾ ਲਗਾਇਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਉਹਨਾਂ ਨੂੰ ਰੋਕਿਆ ਜਾਂਦਾ ਹੈ। | 3 |

---

## References
## ਹਵਾਲੇ

* [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
* [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
* [MITRE ATLAS: Adversarial Input Detection](https://atlas.mitre.org/mitigations/AML.M0015)
* [MITRE ATLAS: LLM Prompt Injection (AML.T0051)](https://atlas.mitre.org/techniques/AML.T0051)
