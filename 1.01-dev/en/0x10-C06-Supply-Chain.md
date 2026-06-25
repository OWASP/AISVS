# C6 Supply Chain Security for Models

## Control Objective

This chapter addresses defending against AI supply chain attacks that exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code.

---

## C6.1 Model Artifact Integrity

Third-party model origins must be authenticated and checked for hidden behavior before fine-tuning or deployment, and AI artifacts should be downloaded only from approved sources.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **Verify that** models are scanned for malicious code before import. | 1 |
| **6.1.2** | **Verify that** model weights, datasets, and fine-tuning adapters are downloaded only from approved sources. | 1 |
| **6.1.3** | **Verify that** every third-party model artifact can be integrity-verified. | 2 |
| **6.1.4** | **Verify that** models pass a behavioral acceptance test suite before being promoted to any non-development environment. | 2 |

---

## C6.2 AI BOM & Supply Chain Monitoring

Detailed AI-specific bills of materials must be generated and signed, with readiness to respond to supply chain compromise events.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **Verify that** every model artifact publishes a version-controlled, machine-readable AI BOM listing datasets, weights, licenses, and data-origin statements. | 1 |
| **6.2.2** | **Verify that** AI BOMs are cryptographically signed before deployment. | 2 |
| **6.2.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata is missing. | 2 |

---

## References

* [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
* [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
* [SBOM Overview: CISA](https://www.cisa.gov/sbom)
* [CycloneDX: Machine Learning Bill of Materials](https://cyclonedx.org/capabilities/mlbom/)
* [OWASP AIBOM](https://genai.owasp.org/owasp-aibom/)
