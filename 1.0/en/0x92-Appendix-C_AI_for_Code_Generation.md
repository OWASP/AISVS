# Appendix C: AI-Assisted Secure Coding

## Objective

This chapter defines baseline organizational controls for the safe and effective use of AI-assisted coding tools during software development, ensuring security and traceability across the SDLC.

---

## AC.1 AI-Assisted Secure-Coding Workflow

Integrate AI tooling into the organization’s secure-software-development lifecycle (SSDLC) without weakening existing security gates.

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

### References

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/81230.html)
* [OWASP Secure Coding Practices: Quick Reference Guide](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
