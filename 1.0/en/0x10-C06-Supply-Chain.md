# C6 Supply Chain Security for Models, Frameworks & Data

## Control Objective

AI supply-chain attacks exploit third-party models, frameworks, or datasets to embed backdoors, bias, or exploitable code. These controls provide end-to-end traceability, vulnerability management, and monitoring to protect the entire model lifecycle.

---

## C6.1 Pretrained Model Vetting & Origin Integrity

Assess and authenticate third-party model origins, licenses, and hidden behaviors before any fine-tuning or deployment.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :---: |
| **6.1.1** | **Verify that** every third-party model artifact includes a signed origin-and-integrity record identifying its source, version, and integrity checksum. | 1 | D/V |
| **6.1.2** | **Verify that** models are scanned for malicious layers or Trojan triggers using automated tools before import. | 1 | D/V |
| **6.1.3** | **Verify that** model licenses, export-control tags, and data-origin statements are recorded in an AI BOM entry. | 2 | V |
| **6.1.4** | **Verify that** high-risk models (e.g., publicly uploaded weights, unverified creators) remain quarantined until human review and sign-off. | 2 | D/V |
| **6.1.5** | **Verify that** transfer-learning fine-tunes pass adversarial evaluation to detect hidden behaviors. | 3 | D |
| **6.1.6** | **Verify that** third-party or open-source models pass a defined behavioral acceptance test suite (covering safety, alignment, and capability boundaries relevant to the deployment context) before being imported or promoted to any non-development environment. | 2 | D/V |

---

## C6.2 Framework & Library Scanning

Continuously scan AI frameworks and libraries for vulnerabilities and malicious code to keep the runtime stack secure.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :---: |
| **6.2.1** | **Verify that** CI pipelines run dependency scanners on AI frameworks and critical libraries. | 1 | D/V |
| **6.2.2** | **Verify that** critical and high-severity vulnerabilities block promotion to production images. | 2 | D/V |
| **6.2.3** | **Verify that** static code analysis runs on forked or vendored AI libraries. | 2 | D |
| **6.2.4** | **Verify that** framework upgrade proposals include a security impact assessment referencing public vulnerability feeds. | 2 | V |
| **6.2.5** | **Verify that** runtime sensors alert on unexpected dynamic library loads that deviate from the signed SBOM. | 3 | V |

---

## C6.3 Dependency Pinning & Verification

Pin every dependency to immutable digests and verify builds to guarantee tamper-free artifacts.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :---: |
| **6.3.1** | **Verify that** all package managers enforce version pinning via lockfiles. | 1 | D/V |
| **6.3.2** | **Verify that** immutable digests are used instead of mutable tags in container references. | 1 | D/V |
| **6.3.3** | **Verify that** expired or unmaintained dependencies trigger automated notifications to update or replace pinned versions. | 2 | D |
| **6.3.4** | **Verify that** build attestations are retained for a period defined by organizational policy for audit traceability. | 3 | V |
| **6.3.5** | **Verify that** reproducible-build checks compare hashes across CI runs to ensure identical outputs. | 3 | D |

---

## C6.4 Trusted Source Enforcement

Allow artifact downloads only from cryptographically verified, organization-approved sources and block everything else.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :---: |
| **6.4.1** | **Verify that** model weights, datasets, and containers are downloaded only from approved sources or internal registries. | 1 | D/V |
| **6.4.2** | **Verify that** cryptographic signatures validate publisher identity before artifacts are cached locally. | 1 | D/V |
| **6.4.3** | **Verify that** egress controls block unauthenticated artifact downloads to enforce trusted-source policy. | 2 | D |
| **6.4.4** | **Verify that** repository allow-lists are reviewed periodically with evidence of business justification for each entry. | 3 | V |
| **6.4.5** | **Verify that** policy violations trigger quarantining of artifacts and rollback of dependent pipeline runs. | 3 | V |

---

## C6.5 Third-Party Dataset Risk Assessment

Evaluate external datasets for poisoning, bias, and legal compliance, and monitor them throughout their lifecycle.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :---: |
| **6.5.1** | **Verify that** external datasets undergo poisoning risk assessment (e.g., data fingerprinting, outlier detection). | 1 | D/V |
| **6.5.2** | **Verify that** disallowed content (e.g., copyrighted material, PII) is detected and removed via automated scrubbing prior to training. | 1 | D |
| **6.5.3** | **Verify that** origin, lineage, and license terms for datasets are captured in AI BOM entries. | 2 | V |
| **6.5.4** | **Verify that** bias metrics (e.g., demographic parity, equal opportunity) are calculated before dataset approval. | 2 | D |
| **6.5.5** | **Verify that** periodic monitoring detects drift or corruption in hosted datasets. | 3 | V |

---

## C6.6 Supply Chain Attack Monitoring

Detect supply-chain threats early through vulnerability feeds, audit-log analytics, and incident response readiness.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :---: |
| **6.6.1** | **Verify that** incident response playbooks include rollback procedures for compromised models or libraries. | 2 | D |
| **6.6.2** | **Verify that** CI/CD audit logs are streamed to centralized security monitoring with detections for anomalous package pulls or tampered build steps. | 2 | V |
| **6.6.3** | **Verify that** threat-intelligence enrichment tags AI-specific indicators (e.g., model-poisoning indicators of compromise) in alert triage. | 3 | V |

---

## C6.7 AI BOM for Model Artifacts

Generate and sign detailed AI-specific bills of materials (AI BOMs) so downstream consumers can verify component integrity at deploy time.

| # | Description | Level | Role |
| :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: | :---: |
| **6.7.1** | **Verify that** every model artifact publishes an AI BOM that lists datasets, weights, hyperparameters, and licenses. | 1 | D/V |
| **6.7.2** | **Verify that** AI BOM generation and cryptographic signing are automated in CI and required for merge. | 2 | D/V |
| **6.7.3** | **Verify that** AI BOM completeness checks fail the build if any component metadata (hash and license) is missing. | 2 | D |
| **6.7.4** | **Verify that** downstream consumers can query AI BOMs via API to validate imported models at deploy time. | 2 | V |
| **6.7.5** | **Verify that** AI BOMs are version-controlled and diffed to detect unauthorized modifications. | 3 | V |

---

## References

* [OWASP LLM03:2025 Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/)
* [MITRE ATLAS: Supply Chain Compromise](https://atlas.mitre.org/techniques/AML.T0010)
* [SBOM Overview: CISA](https://www.cisa.gov/sbom)
* [CycloneDX: Machine Learning Bill of Materials](https://cyclonedx.org/capabilities/mlbom/)
