<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x02-Preface.md -->
<!-- Translator: GeeksikhSecurity -->

# Preface
# ਮੁਖਬੰਧ

Welcome to the **Artificial Intelligence Security Verification Standard (AISVS) version 1.0**.

**ਬਣਾਉਟੀ ਬੁੱਧੀ ਸੁਰੱਖਿਆ ਤਸਦੀਕ ਮਿਆਰ (Artificial Intelligence Security Verification Standard, AISVS) ਸੰਸਕਰਣ 1.0** ਵਿੱਚ ਜੀ ਆਇਆਂ ਨੂੰ।

By adopting AISVS, organizations can systematically evaluate and strengthen the security posture of their AI systems, building a foundation of secure AI engineering practices that evolves alongside the technology itself.

AISVS ਨੂੰ ਅਪਣਾ ਕੇ, ਸੰਸਥਾਵਾਂ ਆਪਣੇ AI ਸਿਸਟਮਾਂ ਦੀ ਸੁਰੱਖਿਆ ਸਥਿਤੀ ਦਾ ਵਿਵਸਥਿਤ ਢੰਗ ਨਾਲ ਮੁਲਾਂਕਣ ਕਰ ਸਕਦੀਆਂ ਹਨ ਅਤੇ ਉਸ ਨੂੰ ਮਜ਼ਬੂਤ ਬਣਾ ਸਕਦੀਆਂ ਹਨ, ਅਤੇ ਸੁਰੱਖਿਅਤ AI ਇੰਜੀਨੀਅਰਿੰਗ ਅਭਿਆਸਾਂ ਦੀ ਇੱਕ ਅਜਿਹੀ ਨੀਂਹ ਉਸਾਰ ਸਕਦੀਆਂ ਹਨ ਜੋ ਤਕਨਾਲੋਜੀ ਦੇ ਨਾਲ-ਨਾਲ ਹੀ ਵਿਕਸਿਤ ਹੁੰਦੀ ਰਹੇ।

## Why AISVS Exists
## AISVS ਕਿਉਂ ਮੌਜੂਦ ਹੈ

AI systems introduce security risks that traditional application security standards were not designed to address. Prompt injection allows attackers to override model instructions through crafted inputs, turning a language model into a tool for data exfiltration, unauthorized actions, or bypassing safety controls. Training data can be poisoned to install backdoors or degrade model behavior. Models can be extracted, inverted, or manipulated through adversarial inputs. Autonomous agents can take actions with real-world consequences, acting on prompt-injected instructions they cannot tell apart from legitimate ones. Retrieval pipelines can be exploited to leak sensitive information or to inject malicious content into model context. The supply chain for models, datasets, and frameworks presents novel integrity challenges that existing software composition analysis alone cannot solve.

AI ਸਿਸਟਮ ਅਜਿਹੇ ਸੁਰੱਖਿਆ ਜੋਖਮ ਪੇਸ਼ ਕਰਦੇ ਹਨ ਜਿਨ੍ਹਾਂ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਨ ਲਈ ਰਵਾਇਤੀ ਐਪਲੀਕੇਸ਼ਨ ਸੁਰੱਖਿਆ ਮਿਆਰ ਤਿਆਰ ਹੀ ਨਹੀਂ ਕੀਤੇ ਗਏ ਸਨ। prompt ਇੰਜੈਕਸ਼ਨ (prompt injection) ਹਮਲਾਵਰਾਂ ਨੂੰ ਘੜੇ ਹੋਏ ਇਨਪੁੱਟਾਂ ਰਾਹੀਂ ਮਾਡਲ ਦੀਆਂ ਹਦਾਇਤਾਂ ਨੂੰ ਓਵਰਰਾਈਡ ਕਰਨ ਦਿੰਦਾ ਹੈ, ਜਿਸ ਨਾਲ ਇੱਕ ਭਾਸ਼ਾ ਮਾਡਲ ਡਾਟਾ ਬਾਹਰ ਕੱਢਣ (data exfiltration), ਅਣਅਧਿਕਾਰਤ ਕਾਰਵਾਈਆਂ, ਜਾਂ ਸਲਾਮਤੀ (safety) ਨਿਯੰਤਰਣਾਂ ਨੂੰ ਬਾਈਪਾਸ ਕਰਨ ਦਾ ਸੰਦ ਬਣ ਜਾਂਦਾ ਹੈ। ਸਿਖਲਾਈ ਡਾਟੇ (training data) ਨੂੰ ਬੈਕਡੋਰ ਸਥਾਪਤ ਕਰਨ ਜਾਂ ਮਾਡਲ ਦੇ ਵਿਵਹਾਰ ਨੂੰ ਵਿਗਾੜਨ ਲਈ data poisoning (ਡਾਟਾ ਜ਼ਹਿਰੀਕਰਨ) ਦਾ ਨਿਸ਼ਾਨਾ ਬਣਾਇਆ ਜਾ ਸਕਦਾ ਹੈ। ਮਾਡਲਾਂ ਨੂੰ ਵਿਰੋਧੀ ਇਨਪੁੱਟਾਂ (adversarial inputs) ਰਾਹੀਂ ਕੱਢਿਆ (model extraction), ਉਲਟਾਇਆ (model inversion), ਜਾਂ ਤੋੜ-ਮਰੋੜ ਕੇ ਵਰਤਿਆ ਜਾ ਸਕਦਾ ਹੈ। ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਏਜੰਟ (autonomous agents) ਅਸਲ-ਸੰਸਾਰ ਨਤੀਜਿਆਂ ਵਾਲੀਆਂ ਕਾਰਵਾਈਆਂ ਕਰ ਸਕਦੇ ਹਨ, ਅਤੇ ਉਹਨਾਂ prompt-ਇੰਜੈਕਟ ਕੀਤੀਆਂ ਹਦਾਇਤਾਂ ਉੱਤੇ ਅਮਲ ਕਰ ਸਕਦੇ ਹਨ ਜਿਨ੍ਹਾਂ ਨੂੰ ਉਹ ਜਾਇਜ਼ ਹਦਾਇਤਾਂ ਤੋਂ ਵੱਖ ਨਹੀਂ ਕਰ ਸਕਦੇ। ਪ੍ਰਾਪਤੀ ਪਾਈਪਲਾਈਨਾਂ (retrieval pipelines) ਦਾ ਸ਼ੋਸ਼ਣ ਸੰਵੇਦਨਸ਼ੀਲ ਜਾਣਕਾਰੀ ਲੀਕ ਕਰਨ ਜਾਂ ਮਾਡਲ ਸੰਦਰਭ ਵਿੱਚ ਖ਼ਤਰਨਾਕ ਸਮੱਗਰੀ ਦਾਖ਼ਲ ਕਰਨ ਲਈ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ। ਮਾਡਲਾਂ, ਡਾਟਾਸੈੱਟਾਂ, ਅਤੇ ਫ੍ਰੇਮਵਰਕਾਂ ਦੀ ਸਪਲਾਈ ਚੇਨ (supply chain) ਅਖੰਡਤਾ (integrity) ਦੀਆਂ ਨਵੀਆਂ ਚੁਣੌਤੀਆਂ ਪੇਸ਼ ਕਰਦੀ ਹੈ ਜਿਨ੍ਹਾਂ ਨੂੰ ਮੌਜੂਦਾ ਸਾਫ਼ਟਵੇਅਰ ਕੰਪੋਜ਼ੀਸ਼ਨ ਵਿਸ਼ਲੇਸ਼ਣ (software composition analysis) ਇਕੱਲਾ ਹੱਲ ਨਹੀਂ ਕਰ ਸਕਦਾ।

AISVS was created to give organizations a structured, testable set of security controls purpose-built for these risks. It does not replace existing standards; it fills the gap that none of them cover.

AISVS ਇਸ ਲਈ ਬਣਾਇਆ ਗਿਆ ਸੀ ਤਾਂ ਜੋ ਸੰਸਥਾਵਾਂ ਨੂੰ ਇਹਨਾਂ ਜੋਖਮਾਂ ਲਈ ਉਚੇਚੇ ਤੌਰ 'ਤੇ ਬਣਾਏ ਗਏ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣਾਂ ਦਾ ਇੱਕ ਵਿਵਸਥਿਤ, ਪਰਖਣਯੋਗ ਸੈੱਟ ਦਿੱਤਾ ਜਾ ਸਕੇ। ਇਹ ਮੌਜੂਦਾ ਮਿਆਰਾਂ ਦੀ ਥਾਂ ਨਹੀਂ ਲੈਂਦਾ; ਇਹ ਉਸ ਪਾੜੇ ਨੂੰ ਭਰਦਾ ਹੈ ਜਿਸ ਨੂੰ ਉਹਨਾਂ ਵਿੱਚੋਂ ਕੋਈ ਵੀ ਨਹੀਂ ਢੱਕਦਾ।

## Design Principles
## ਡਿਜ਼ਾਈਨ ਸਿਧਾਂਤ

AISVS is organized into 12 control families. Each control family is divided into focused sections that support its control objective. Each section contains verification requirements. AISVS defines three verification levels, defined under Using the AISVS; sections need not include requirements at every level.

AISVS ਨੂੰ 12 ਨਿਯੰਤਰਣ ਪਰਿਵਾਰਾਂ (control families) ਵਿੱਚ ਵਿਵਸਥਿਤ ਕੀਤਾ ਗਿਆ ਹੈ। ਹਰ ਨਿਯੰਤਰਣ ਪਰਿਵਾਰ ਨੂੰ ਕੇਂਦ੍ਰਿਤ ਭਾਗਾਂ ਵਿੱਚ ਵੰਡਿਆ ਗਿਆ ਹੈ ਜੋ ਉਸ ਦੇ ਨਿਯੰਤਰਣ ਉਦੇਸ਼ ਦਾ ਸਮਰਥਨ ਕਰਦੇ ਹਨ। ਹਰ ਭਾਗ ਵਿੱਚ ਤਸਦੀਕ ਲੋੜਾਂ ਸ਼ਾਮਲ ਹਨ। AISVS ਤਿੰਨ ਤਸਦੀਕ ਪੱਧਰ ਪਰਿਭਾਸ਼ਿਤ ਕਰਦਾ ਹੈ, ਜੋ AISVS ਦੀ ਵਰਤੋਂ (Using the AISVS) ਹੇਠ ਪਰਿਭਾਸ਼ਿਤ ਕੀਤੇ ਗਏ ਹਨ; ਹਰ ਭਾਗ ਵਿੱਚ ਹਰ ਪੱਧਰ ਦੀਆਂ ਲੋੜਾਂ ਦਾ ਹੋਣਾ ਜ਼ਰੂਰੀ ਨਹੀਂ ਹੈ।

Each requirement must address a single concern that can ordinarily be implemented and verified as one technical mechanism. Requirements must not duplicate controls defined elsewhere in AISVS. Higher assurance levels may introduce stricter criteria, but those criteria must be stated as separate requirements. Requirements should use clear, technology-neutral language, referencing specific technologies only as examples where they improve clarity.

ਹਰ ਲੋੜ ਲਈ ਇੱਕੋ ਸਰੋਕਾਰ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ, ਜਿਸ ਨੂੰ ਆਮ ਤੌਰ 'ਤੇ ਇੱਕ ਤਕਨੀਕੀ ਵਿਧੀ ਵਜੋਂ ਲਾਗੂ ਅਤੇ ਤਸਦੀਕ ਕੀਤਾ ਜਾ ਸਕੇ। ਲੋੜਾਂ ਲਈ AISVS ਵਿੱਚ ਹੋਰ ਕਿਤੇ ਪਰਿਭਾਸ਼ਿਤ ਨਿਯੰਤਰਣਾਂ ਨੂੰ ਨਾ ਦੁਹਰਾਉਣਾ ਲਾਜ਼ਮੀ ਹੈ। ਉੱਚੇ ਭਰੋਸਾ ਪੱਧਰ ਸਖ਼ਤ ਮਾਪਦੰਡ ਪੇਸ਼ ਕਰ ਸਕਦੇ ਹਨ, ਪਰ ਉਹਨਾਂ ਮਾਪਦੰਡਾਂ ਨੂੰ ਵੱਖਰੀਆਂ ਲੋੜਾਂ ਵਜੋਂ ਦੱਸਣਾ ਲਾਜ਼ਮੀ ਹੈ। ਲੋੜਾਂ ਨੂੰ ਸਪੱਸ਼ਟ, ਤਕਨਾਲੋਜੀ-ਨਿਰਪੱਖ ਭਾਸ਼ਾ ਵਰਤਣੀ ਚਾਹੀਦੀ ਹੈ, ਅਤੇ ਖ਼ਾਸ ਤਕਨਾਲੋਜੀਆਂ ਦਾ ਹਵਾਲਾ ਸਿਰਫ਼ ਉਦਾਹਰਨਾਂ ਵਜੋਂ ਉੱਥੇ ਦੇਣਾ ਚਾਹੀਦਾ ਹੈ ਜਿੱਥੇ ਉਹ ਸਪੱਸ਼ਟਤਾ ਵਧਾਉਂਦੀਆਂ ਹਨ।

Every AISVS requirement follows four design principles derived from the standard’s name:

ਹਰ AISVS ਲੋੜ ਮਿਆਰ ਦੇ ਨਾਮ ਤੋਂ ਲਏ ਗਏ ਚਾਰ ਡਿਜ਼ਾਈਨ ਸਿਧਾਂਤਾਂ ਦੀ ਪਾਲਣਾ ਕਰਦੀ ਹੈ:

* **Artificial Intelligence.** Requirements must address AI/ML-specific assets, workflows, or runtime behavior, including datasets, models, training and evaluation pipelines, retrieval systems, agents, tools, memory, and inference-time operation. AISVS does not duplicate general application security controls from standards such as ASVS unless the control has AI-specific implementation or verification concerns.

* **ਬਣਾਉਟੀ ਬੁੱਧੀ (Artificial Intelligence)।** ਲੋੜਾਂ ਲਈ AI/ML-ਵਿਸ਼ੇਸ਼ ਸੰਪਤੀਆਂ, ਵਰਕਫ਼ਲੋਜ਼, ਜਾਂ ਰਨਟਾਈਮ ਵਿਵਹਾਰ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ, ਜਿਸ ਵਿੱਚ ਡਾਟਾਸੈੱਟ, ਮਾਡਲ, ਸਿਖਲਾਈ ਅਤੇ ਮੁਲਾਂਕਣ ਪਾਈਪਲਾਈਨਾਂ, ਪ੍ਰਾਪਤੀ ਸਿਸਟਮ, ਏਜੰਟ, ਟੂਲ, ਮੈਮੋਰੀ, ਅਤੇ ਇਨਫ਼ਰੈਂਸ-ਸਮੇਂ ਦਾ ਸੰਚਾਲਨ ਸ਼ਾਮਲ ਹਨ। AISVS, ASVS ਵਰਗੇ ਮਿਆਰਾਂ ਤੋਂ ਆਮ ਐਪਲੀਕੇਸ਼ਨ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣਾਂ ਨੂੰ ਨਹੀਂ ਦੁਹਰਾਉਂਦਾ, ਜਦੋਂ ਤੱਕ ਉਸ ਨਿਯੰਤਰਣ ਦੇ AI-ਵਿਸ਼ੇਸ਼ ਅਮਲ ਜਾਂ ਤਸਦੀਕ ਸਰੋਕਾਰ ਨਾ ਹੋਣ।

* **Security.** Requirements must mitigate an identifiable security, privacy, or safety risk. Controls that serve only operational, governance, compliance, or business objectives are out of scope.

* **ਸੁਰੱਖਿਆ (Security)।** ਲੋੜਾਂ ਲਈ ਕਿਸੇ ਪਛਾਣਯੋਗ ਸੁਰੱਖਿਆ, ਨਿੱਜਤਾ, ਜਾਂ ਸਲਾਮਤੀ (safety) ਜੋਖਮ ਨੂੰ ਘਟਾਉਣਾ ਲਾਜ਼ਮੀ ਹੈ। ਉਹ ਨਿਯੰਤਰਣ ਜੋ ਸਿਰਫ਼ ਸੰਚਾਲਨ, ਸ਼ਾਸਨ (governance), ਪਾਲਣਾ, ਜਾਂ ਕਾਰੋਬਾਰੀ ਉਦੇਸ਼ਾਂ ਦੀ ਪੂਰਤੀ ਕਰਦੇ ਹਨ, ਘੇਰੇ ਤੋਂ ਬਾਹਰ ਹਨ।

* **Verification.** Requirements must be objectively verifiable through testing, inspection, or audit. Sufficient implementation guidance or tooling must exist to support both implementation and verification. Purely theoretical, subjective, or aspirational guidance is excluded.

* **ਤਸਦੀਕ (Verification)।** ਲੋੜਾਂ ਲਈ ਟੈਸਟਿੰਗ, ਨਿਰੀਖਣ, ਜਾਂ ਆਡਿਟ ਰਾਹੀਂ ਵਸਤੂਪਰਕ ਤੌਰ 'ਤੇ ਤਸਦੀਕਯੋਗ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ। ਅਮਲ ਅਤੇ ਤਸਦੀਕ ਦੋਵਾਂ ਦਾ ਸਮਰਥਨ ਕਰਨ ਲਈ ਲੋੜੀਂਦਾ ਅਮਲ ਮਾਰਗਦਰਸ਼ਨ ਜਾਂ ਟੂਲਿੰਗ ਮੌਜੂਦ ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ। ਪੂਰੀ ਤਰ੍ਹਾਂ ਸਿਧਾਂਤਕ, ਵਿਅਕਤੀਪਰਕ, ਜਾਂ ਇੱਛਾ-ਆਧਾਰਿਤ ਮਾਰਗਦਰਸ਼ਨ ਨੂੰ ਬਾਹਰ ਰੱਖਿਆ ਗਿਆ ਹੈ।

* **Standard.** Requirements must use consistent structure, terminology, and assurance-level semantics so AISVS remains coherent, navigable, and suitable for repeatable assessment.

* **ਮਿਆਰ (Standard)।** ਲੋੜਾਂ ਲਈ ਇਕਸਾਰ ਬਣਤਰ, ਸ਼ਬਦਾਵਲੀ, ਅਤੇ ਭਰੋਸਾ-ਪੱਧਰ ਅਰਥ-ਵਿਗਿਆਨ ਵਰਤਣਾ ਲਾਜ਼ਮੀ ਹੈ ਤਾਂ ਜੋ AISVS ਸੁਸੰਗਤ, ਸੌਖਾ ਨੈਵੀਗੇਟ ਕਰਨਯੋਗ, ਅਤੇ ਦੁਹਰਾਉਣਯੋਗ ਮੁਲਾਂਕਣ ਲਈ ਢੁਕਵਾਂ ਰਹੇ।
