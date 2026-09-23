<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C06-Supply-Chain.md -->
<!-- Translator: GeeksikhSecurity -->

# C6 Supply Chain Security for Models
# C6 ਮਾਡਲਾਂ ਲਈ ਸਪਲਾਈ ਚੇਨ ਸੁਰੱਖਿਆ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses defending against AI supply chain attacks that exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code.

ਇਹ ਅਧਿਆਇ AI ਸਪਲਾਈ ਚੇਨ (supply chain) ਹਮਲਿਆਂ ਤੋਂ ਬਚਾਅ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ, ਜੋ ਬੈਕਡੋਰ, ਪੱਖਪਾਤ (bias), ਜਾਂ ਸ਼ੋਸ਼ਣਯੋਗ ਕੋਡ ਨੂੰ ਅੰਦਰ ਬਿਠਾਉਣ ਲਈ ਤੀਜੀ-ਧਿਰ ਦੇ ਮਾਡਲਾਂ, ਫ੍ਰੇਮਵਰਕਾਂ, ਜਾਂ ਡਾਟਾਸੈੱਟਾਂ ਦਾ ਸ਼ੋਸ਼ਣ ਕਰਦੇ ਹਨ।

---

## C6.1 Model Artifact Integrity
## C6.1 ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਅਖੰਡਤਾ

Third-party model origins must be authenticated and checked for hidden behavior before fine-tuning or deployment, and AI artifacts should be downloaded only from approved sources.

ਤੀਜੀ-ਧਿਰ ਦੇ ਮਾਡਲਾਂ ਦੇ ਮੂਲ ਦਾ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ (fine-tuning) ਜਾਂ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਪ੍ਰਮਾਣੀਕਰਨ (authentication) ਕੀਤਾ ਜਾਣਾ ਅਤੇ ਲੁਕਵੇਂ ਵਿਵਹਾਰ ਲਈ ਜਾਂਚ ਕੀਤੀ ਜਾਣੀ ਲਾਜ਼ਮੀ ਹੈ, ਅਤੇ AI ਆਰਟੀਫ਼ੈਕਟ ਸਿਰਫ਼ ਪ੍ਰਵਾਨਿਤ ਸਰੋਤਾਂ ਤੋਂ ਹੀ ਡਾਊਨਲੋਡ ਕੀਤੇ ਜਾਣੇ ਚਾਹੀਦੇ ਹਨ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **Verify that** models are scanned for malicious code before import. | 1 |
| **6.1.2** | **Verify that** model weights, datasets, and fine-tuning adapters are downloaded only from approved sources. | 1 |
| **6.1.3** | **Verify that** every third-party model artifact can be integrity-verified. | 2 |
| **6.1.4** | **Verify that** models pass a behavioral acceptance test suite before being promoted to any non-development environment. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲਾਂ ਨੂੰ ਆਯਾਤ (import) ਤੋਂ ਪਹਿਲਾਂ ਖ਼ਤਰਨਾਕ ਕੋਡ ਲਈ ਸਕੈਨ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 1 |
| **6.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਵੇਟਸ (model weights), ਡਾਟਾਸੈੱਟ, ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਅਡੈਪਟਰ ਸਿਰਫ਼ ਪ੍ਰਵਾਨਿਤ ਸਰੋਤਾਂ ਤੋਂ ਹੀ ਡਾਊਨਲੋਡ ਕੀਤੇ ਜਾਂਦੇ ਹਨ। | 1 |
| **6.1.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਤੀਜੀ-ਧਿਰ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਦੀ ਅਖੰਡਤਾ (integrity) ਦੀ ਤਸਦੀਕ ਕੀਤੀ ਜਾ ਸਕਦੀ ਹੈ। | 2 |
| **6.1.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਕਿਸੇ ਵੀ ਗ਼ੈਰ-ਵਿਕਾਸ ਵਾਤਾਵਰਣ ਵਿੱਚ ਤਰੱਕੀ ਦਿੱਤੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਇੱਕ ਵਿਵਹਾਰਕ ਸਵੀਕ੍ਰਿਤੀ ਟੈਸਟ ਸੂਟ ਪਾਸ ਕਰਦੇ ਹਨ। | 2 |

---

## C6.2 AI BOM & Supply Chain Monitoring
## C6.2 AI BOM ਅਤੇ ਸਪਲਾਈ ਚੇਨ ਨਿਗਰਾਨੀ

Detailed AI-specific bills of materials must be generated and signed, with readiness to respond to supply chain compromise events.

ਵਿਸਤ੍ਰਿਤ AI-ਵਿਸ਼ੇਸ਼ ਬਿਲ ਆਫ਼ ਮਟੀਰੀਅਲਜ਼ (bills of materials) ਤਿਆਰ ਅਤੇ ਦਸਤਖ਼ਤ ਕੀਤੇ ਜਾਣੇ ਲਾਜ਼ਮੀ ਹਨ, ਨਾਲ ਹੀ ਸਪਲਾਈ ਚੇਨ ਦੇ ਸਮਝੌਤੇ (compromise) ਦੀਆਂ ਘਟਨਾਵਾਂ ਦਾ ਜਵਾਬ ਦੇਣ ਦੀ ਤਿਆਰੀ ਸਮੇਤ।

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **Verify that** every model artifact publishes a version-controlled, machine-readable AI BOM listing datasets, weights, licenses, and data-origin statements. | 1 |
| **6.2.2** | **Verify that** AI BOMs are cryptographically signed before deployment. | 2 |
| **6.2.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata is missing. | 2 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਇੱਕ ਵਰਜ਼ਨ-ਨਿਯੰਤਰਿਤ, ਮਸ਼ੀਨ-ਪੜ੍ਹਨਯੋਗ AI BOM ਪ੍ਰਕਾਸ਼ਿਤ ਕਰਦਾ ਹੈ ਜਿਸ ਵਿੱਚ ਡਾਟਾਸੈੱਟ, ਵੇਟਸ, ਲਾਇਸੈਂਸ, ਅਤੇ ਡਾਟਾ-ਮੂਲ ਬਿਆਨ ਸੂਚੀਬੱਧ ਹੁੰਦੇ ਹਨ। | 1 |
| **6.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** AI BOM ਨੂੰ ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਦਸਤਖ਼ਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **6.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਜੇ ਕਿਸੇ ਕੰਪੋਨੈਂਟ ਦਾ ਮੈਟਾਡਾਟਾ ਗ਼ੈਰ-ਮੌਜੂਦ ਹੋਵੇ ਤਾਂ AI BOM ਸੰਪੂਰਨਤਾ ਜਾਂਚਾਂ ਬਿਲਡ ਨੂੰ ਫ਼ੇਲ੍ਹ ਕਰ ਦਿੰਦੀਆਂ ਹਨ। | 2 |

---

## References
## ਹਵਾਲੇ

* [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
* [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
* [SBOM Overview: CISA](https://www.cisa.gov/sbom)
* [CycloneDX: Machine Learning Bill of Materials](https://cyclonedx.org/capabilities/mlbom/)
* [OWASP AIBOM](https://genai.owasp.org/owasp-aibom/)
