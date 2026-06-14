# C6 Supply Chain Security for Models, Frameworks & Data

## Control Objective

AI supply-chain attacks exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code. These controls ensure traceability, vetting, and monitoring of AI-specific supply chain artifacts throughout the model lifecycle. This chapter focuses on supply chain risks unique to AI: model artifact integrity, backdoor detection in pretrained weights, dataset poisoning, AI-specific bills of materials, and model-publisher trust.

---

## C6.1 Model Artifact Integrity & Source Trust

Assess and authenticate third-party model origins and hidden behaviors before any fine-tuning or deployment, and allow AI artifact downloads only from organization-approved sources.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **Verify that** every third-party model artifact includes a signed record identifying its source, version, and integrity checksum. | 2 |
| **6.1.2** | **Verify that** models are scanned for malicious code or unsafe serialization payloads before import. | 1 |
| **6.1.3** | **Verify that** high-risk models remain quarantined until human review and sign-off. | 2 |
| **6.1.4** | **Verify that** third-party or open-source models pass a behavioral acceptance test suite before being imported or promoted to any non-development environment. | 2 |
| **6.1.5** | **Verify that** model weights, datasets, and fine-tuning adapters are downloaded only from approved sources or internal registries. | 1 |
| **6.1.6** | **Verify that** transfer-learning fine-tunes pass adversarial evaluation to detect hidden behaviors. | 3 |

---

## C6.2 Dataset Risk Assessment

Evaluate external datasets for poisoning and legal compliance, and monitor them throughout their lifecycle.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **Verify that** disallowed content is detected and removed by automated scrubbing before training. | 1 |
| **6.2.2** | **Verify that** external datasets undergo poisoning risk assessment. | 2 |
| **6.2.3** | **Verify that** origin, lineage, and license terms for datasets are captured in AI BOM entries. | 1 |
| **6.2.4** | **Verify that** periodic monitoring detects drift or corruption in hosted datasets. | 2 |

---

## C6.3 AI BOM & Supply Chain Monitoring

Generate and sign detailed AI-specific bills of materials and ensure readiness to respond to supply chain compromise events.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.3.1** | **Verify that** every model artifact publishes a version-controlled, machine-readable AI BOM listing datasets, weights, licenses, and data-origin statements. | 1 |
| **6.3.2** | **Verify that** AI BOMs are cryptographically signed before deployment. | 2 |
| **6.3.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata is missing. | 2 |
| **6.3.4** | **Verify that** incident response playbooks include procedures specific to compromised AI artifacts, such as rollback of poisoned models and revocation of model signatures. | 2 |

---

## References

* [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
* [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
* [SBOM Overview: CISA](https://www.cisa.gov/sbom)
* [CycloneDX: Machine Learning Bill of Materials](https://cyclonedx.org/capabilities/mlbom/)
* [OWASP AIBOM](https://genai.owasp.org/owasp-aibom/)
