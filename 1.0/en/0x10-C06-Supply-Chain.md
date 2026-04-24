# C6 Supply Chain Security for Models, Frameworks & Data

## Control Objective

AI supply-chain attacks exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code. These controls ensure traceability, vetting, and monitoring of AI-specific supply chain artifacts throughout the model lifecycle.

Generic software supply chain controls (dependency scanning, version pinning, lockfile enforcement, container digest pinning, build attestation, reproducible builds, SBOM generation, CI/CD audit logging, etc.) are covered by ASVS v5 (V13, V15), OWASP SCVS, SLSA, and CIS Controls, and are not repeated here. This chapter focuses on supply chain risks unique to AI: model artifact integrity, backdoor detection in pretrained weights, dataset poisoning, AI-specific bills of materials, and model-publisher trust.

---

## C6.1 Pretrained Model Vetting & Origin Integrity

Assess and authenticate third-party model origins and hidden behaviors before any fine-tuning or deployment.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.1.1** | **Verify that** every third-party model artifact includes a signed origin-and-integrity record identifying its source, version, and integrity checksum. | 1 |
| **6.1.2** | **Verify that** models are scanned for malicious layers or Trojan triggers using automated tools before import. | 1 |
| **6.1.3** | **Verify that** high-risk models (e.g., publicly uploaded weights, unverified creators) remain quarantined until human review and sign-off. | 2 |
| **6.1.4** | **Verify that** third-party or open-source models pass a defined behavioral acceptance test suite (covering safety, alignment, and capability boundaries relevant to the deployment context) before being imported or promoted to any non-development environment. | 2 |
| **6.1.5** | **Verify that** transfer-learning fine-tunes pass adversarial evaluation to detect hidden behaviors. | 3 |

---

## C6.2 Trusted Source Enforcement for AI Artifacts

Allow AI artifact downloads only from organization-approved sources and verify model publisher identity.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.2.1** | **Verify that** model weights, datasets, and fine-tuning adapters are downloaded only from approved sources or internal registries. | 1 |
| **6.2.2** | **Verify that** cryptographic signing keys used to authenticate model publishers are pinned per source registry, and that key rotation events require explicit re-approval before updated keys are trusted. | 3 |

---

## C6.3 Third-Party Dataset Risk Assessment

Evaluate external datasets for poisoning and legal compliance, and monitor them throughout their lifecycle.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.3.1** | **Verify that** disallowed content (e.g., copyrighted material, PII) is detected and removed via automated scrubbing prior to training. | 1 |
| **6.3.2** | **Verify that** external datasets undergo poisoning risk assessment (e.g., data fingerprinting, outlier detection). | 2 |
| **6.3.3** | **Verify that** origin, lineage, and license terms for datasets are captured in AI BOM entries. | 2 |
| **6.3.4** | **Verify that** periodic monitoring detects drift or corruption in hosted datasets. | 3 |

---

## C6.4 Supply Chain Attack Monitoring

Detect AI-specific supply-chain threats through threat intelligence enrichment and incident response readiness.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.4.1** | **Verify that** incident response playbooks include procedures specific to compromised AI artifacts, such as rollback of poisoned models, revocation of model signatures, and re-evaluation of downstream systems that consumed affected artifacts. | 2 |
| **6.4.2** | **Verify that** threat-intelligence enrichment tags AI-specific indicators (e.g., model-poisoning indicators of compromise) in alert triage. | 3 |

---

## C6.5 AI BOM for Model Artifacts

Generate and sign detailed AI-specific bills of materials (AI BOMs) so downstream consumers can verify component integrity at deploy time.

| # | Description | Level |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
| **6.5.1** | **Verify that** every model artifact publishes a version-controlled AI BOM that lists datasets, weights, hyperparameters, licenses, export-control tags, and data-origin statements. | 1 |
| **6.5.2** | **Verify that** AI BOMs are cryptographically signed before deployment. | 2 |
| **6.5.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata (hash and license) is missing. | 2 |
| **6.5.4** | **Verify that** downstream consumers can query AI BOMs via API to validate imported models at the deployment time. | 2 |

---

## References

* [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
* [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
* [SBOM Overview: CISA](https://www.cisa.gov/sbom)
* [CycloneDX: Machine Learning Bill of Materials](https://cyclonedx.org/capabilities/mlbom/)
* [OWASP AIBOM](https://genai.owasp.org/owasp-aibom/)
