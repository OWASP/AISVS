# C1.1: Training Data Origin & Traceability

> [Back to C01 Index](C01-Training-Data.md)
> **Last Researched:** 2026-03-29

## Purpose

Maintaining a verifiable inventory of all datasets, accepting only trusted sources, and logging every change for auditability form the foundation of training data security. Without knowing where data came from, who is responsible for it, and what happened to it over time, organizations cannot detect supply-chain compromises, trace poisoned samples back to their origin during incident response, or satisfy emerging regulatory requirements like California AB 2013 (effective Jan 2026) which mandates public training data documentation.

This section focuses on provenance metadata — ensuring every dataset entry includes origin, responsible party, license, collection method, intended use constraints, and processing history. It also addresses minimizing unnecessary data exposure, enforcing approval gates on dataset changes, and fingerprinting datasets for attribution and theft detection.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **1.1.1** | **Verify that** an up-to-date inventory of every training-data source (origin, responsible party, license, collection method, intended use constraints, and processing history) is maintained. | 1 | Supply-chain compromise via unknown or unvetted data sources; inability to trace poisoned data back to origin during incident response. | Review the data catalog or asset inventory system (e.g., DataHub, Amundsen, or internal registry). Confirm each dataset entry includes all six required metadata fields. Spot-check a sample of datasets against their listed sources. | Most organizations track datasets informally. Tooling like DataHub and MLflow supports metadata but does not enforce completeness. Manual audit remains necessary to verify all fields are populated and accurate. |
| **1.1.2** | **Verify that** training data processes exclude unnecessary features, attributes, or fields (e.g., unused metadata, sensitive PII, leaked test data). | 1 | Data leakage (test data in training sets causing inflated accuracy and masked vulnerabilities); PII exposure in model weights via memorization attacks; larger attack surface from unnecessary features. | Review data pipeline code and ETL configurations for feature selection steps. Confirm PII scanning tools (e.g., Microsoft Presidio, AWS Macie) are integrated. Verify test/validation holdout separation. | Automated PII detection has high false-negative rates for non-English text and domain-specific identifiers. Feature minimization is often a manual design decision with no automated enforcement. |
| **1.1.3** | **Verify that** all dataset changes are subject to a logged approval workflow. | 1 | Unauthorized data modification or injection; insider threat inserting poisoned samples; untracked drift in training data composition. | Inspect version control logs (DVC, LakeFS, or Git LFS) for dataset changes. Verify that an approval gate (PR review, ticket approval) exists before data merges. Check audit logs for completeness. | DVC and LakeFS provide versioning but do not natively enforce approval gates. Approval workflows typically require integration with CI/CD or ticketing systems (Jira, GitHub Issues). |
| **1.1.4** | **Verify that** datasets or subsets are watermarked or fingerprinted where feasible. | 3 | Unauthorized redistribution of proprietary datasets; difficulty attributing data in a trained model back to its source; detecting if stolen data was used in competitor models (MITRE ATLAS AML.T0010.002). | Check for implementation of dataset fingerprinting (e.g., [Datasig](https://blog.trailofbits.com/2025/05/02/datasig-fingerprinting-ai/ml-datasets-to-stop-data-borne-attacks/) MinHash-based fingerprints, radioactive data techniques, embedded statistical watermarks). Verify watermark detection tooling is available and tested. For text datasets, evaluate corpus-level watermarking via biased synonym selection (ICASSP 2025). | As of March 2026, Datasig (Trail of Bits, May 2025) is the first practical fingerprinting tool but remains prototype-stage with ~5% error margin. Corpus-level text watermarking (ICASSP 2025) is research-only. No standardized watermarking scheme exists. Appropriately Level 3. |

---
