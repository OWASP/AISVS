# Appendix C: AI-Assisted Secure Coding

## Objective

This chapter defines baseline organizational controls for the safe and effective use of AI-assisted coding tools during software development, ensuring security and traceability across the SDLC.

---

## AC.1 AI-Assisted Secure-Coding Workflow

Integrate AI tooling into the organization's secure-software-development lifecycle (SSDLC) without weakening existing security gates.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.1.1** | **Verify that** a documented workflow describes when and how AI tools may generate, refactor, or review code. | 1 | D/V |
| **AC.1.2** | **Verify that** the workflow maps to each SSDLC phase (design, implementation, code review, testing, deployment). | 2 | D |
| **AC.1.3** | **Verify that** metrics (e.g., vulnerability density, mean-time-to-detect) are collected on AI-produced code and compared to human-only baselines. | 3 | D/V |

---

## AC.2 AI Tool Qualification & Threat Modeling

Ensure AI coding tools are evaluated for security capabilities, risk, and supply-chain impact before adoption.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.2.1** | **Verify that** a threat model for each AI tool identifies misuse, model-inversion, data leakage, and dependency-chain risks. | 1 | D/V |
| **AC.2.2** | **Verify that** tool evaluations include static/dynamic analysis of any local components and assessment of SaaS endpoints (TLS, authentication/authorization, logging). | 2 | D |
| **AC.2.3** | **Verify that** evaluations follow a recognized framework and are re-performed after major version changes. | 3 | D/V |

---

## AC.3 Secure Prompt & Context Management

Prevent leakage of secrets, proprietary code, and personal data when constructing prompts or contexts for AI models.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.3.1** | **Verify that** written guidance prohibits sending secrets, credentials, or classified data in prompts. | 1 | D/V |
| **AC.3.2** | **Verify that** technical controls (client-side redaction, approved context filters) automatically strip sensitive artifacts. | 2 | D |
| **AC.3.3** | **Verify that** prompts and responses are tokenized, encrypted in transit and at rest, and retention periods comply with data-classification policy. | 3 | D/V |

---

## AC.4 Validation of AI-Generated Code

Detect and remediate vulnerabilities introduced by AI output before the code is merged or deployed.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.4.1** | **Verify that** AI-generated code is always subjected to human code review. | 1 | D/V |
| **AC.4.2** | **Verify that** automated scanners (SAST/IAST/DAST) run on every pull request containing AI-generated code and block merges on critical findings. | 2 | D |
| **AC.4.3** | **Verify that** differential fuzz testing or property-based tests prove security-critical behaviors (e.g., input validation, authorization logic). | 3 | D/V |

---

## AC.5 Explainability & Traceability of Code Suggestions

Provide auditors and developers with insight into why a suggestion was made and how it evolved.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.5.1** | **Verify that** prompt/response pairs are logged with commit IDs. | 1 | D/V |
| **AC.5.2** | **Verify that** developers can surface model citations (training snippets, documentation) supporting a suggestion. | 2 | D |
| **AC.5.3** | **Verify that** explainability reports are stored with design artifacts and referenced in security reviews, satisfying ISO/IEC 42001 traceability principles. | 3 | D/V |

---

## AC.6 Continuous Feedback & Model Fine-Tuning

Improve model security performance over time while preventing negative drift.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.6.1** | **Verify that** developers can flag insecure or non-compliant suggestions, and that flags are tracked. | 1 | D/V |
| **AC.6.2** | **Verify that** aggregated feedback informs periodic fine-tuning or retrieval-augmented generation with vetted secure-coding corpora (e.g., OWASP Cheat Sheets). | 2 | D |
| **AC.6.3** | **Verify that** a closed-loop evaluation harness runs regression tests after every fine-tune; security metrics must meet or exceed prior baselines before deployment. | 3 | D/V |

---

## AC.7 AI-Generated Infrastructure & Pipeline Artifacts

Ensure that AI-generated infrastructure-as-code (IaC), CI/CD workflows, deployment configurations, and security policy artifacts are subject to appropriate validation and governance controls.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.7.1** | **Verify that** AI-generated infrastructure-as-code, CI/CD workflows, and security policy artifacts are clearly identified and tracked. | 1 | D/V |
| **AC.7.2** | **Verify that** AI-generated infrastructure and pipeline configurations require appropriate review and approval prior to execution. | 2 | D |
| **AC.7.3** | **Verify that** AI-generated infrastructure and workflow changes are subject to security validation, configuration checks, and policy enforcement equivalent to or stricter than application code. | 3 | D/V |

---

## AC.8 Autonomous Agent Change Control Constraints

Ensure that autonomous AI agents involved in code or configuration generation are subject to appropriate separation of duties and cannot independently approve or promote their own changes.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.8.1** | **Verify that** autonomous agents cannot approve, merge, sign, or deploy artifacts that they have generated. | 1 | D/V |
| **AC.8.2** | **Verify that** AI systems operate with scoped identities and permissions that prevent self-promotion of generated artifacts across environments. | 2 | D |
| **AC.8.3** | **Verify that** separation of duties is enforced between artifact generation, review, approval, and deployment stages for AI-generated changes. | 3 | D/V |

---

## AC.9 AI Artifact Origin Validation for Deployment

Ensure that deployment and promotion pipelines validate the origin and generation history of AI-generated artifacts before they are promoted.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.9.1** | **Verify that** AI-generated artifacts include origin and generation metadata identifying the AI system that produced them, the generation context, and associated audit records. | 1 | D/V |
| **AC.9.2** | **Verify that** deployment pipelines validate the presence and integrity of origin and generation metadata for AI-generated artifacts prior to promotion. | 2 | D |
| **AC.9.3** | **Verify that** artifacts lacking required origin and generation information, or produced by untrusted AI systems or environments, are rejected during deployment. | 3 | D/V |

---

## AC.10 Generation Audit Trail Completeness and Validation

Ensure that AI-generated artifacts include complete and consistent origin and generation records, and that these records are validated prior to integration or deployment.

In practice, policy-based enforcement depends on the availability and quality of origin and generation records. Incomplete or inconsistent records can lead to missed detections or enforcement gaps. These controls ensure that origin tracking is treated as a first-class requirement and validated prior to artifact acceptance.

| # | Description | Level | Role |
|:--------:|---------------------------------------------------------------------------------------------------------------------|:---:|:---:|
| **AC.10.1** | **Verify that** AI-generated artifacts include required origin and generation fields (e.g., model identity, generation context, human involvement, and session identifiers). | 1 | D/V |
| **AC.10.2** | **Verify that** origin and generation metadata is validated for completeness and consistency (e.g., no missing or ambiguous fields, normalized representations). | 2 | D |
| **AC.10.3** | **Verify that** artifacts with incomplete, inconsistent, or unverifiable origin and generation metadata are rejected prior to merge or deployment. | 3 | D/V |

---

## References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [OWASP Secure Coding Practices: Quick Reference Guide](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
