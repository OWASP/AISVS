# Preface

Welcome to the **Artificial Intelligence Security Verification Standard (AISVS) version 1.0**.

## Why AISVS Exists

AI systems introduce security risks that traditional application security standards were not designed to address. Prompt injection allows attackers to override model instructions through crafted inputs, turning a language model into a tool for data exfiltration, unauthorized actions, or safety bypass. Training data can be poisoned to install backdoors or degrade model behavior. Models can be extracted, inverted, or manipulated through adversarial inputs. Autonomous agents can take actions with real-world consequences based on prompt-injected instructions they cannot distinguish from legitimate ones. Retrieval pipelines can be exploited to leak sensitive information or to inject malicious content into model context. And the supply chain for models, datasets, and frameworks presents novel integrity challenges that existing software composition analysis alone cannot solve.

AISVS was created to give organizations a structured, testable set of security controls purpose-built for these risks. It does not replace existing standards; it fills the gap that none of them cover.

## Design Principles

Every requirement in AISVS follows four principles derived from the standard's name:

* **Artificial Intelligence.** Each control operates at the AI or ML layer (data, model, pipeline, agent, or inference) and addresses risks specific to AI systems rather than general application security.
* **Security.** Each requirement directly mitigates an identified security, privacy, or safety risk. Controls that serve only operational or business objectives are out of scope.
* **Verification.** Requirements are written so that conformance can be objectively validated through testing, inspection, or audit. Subjective or aspirational guidance is excluded.
* **Standard.** All chapters follow a consistent structure and terminology to form a coherent, navigable reference document.

## How to Read This Standard

### Chapter Structure

Each of the 14 requirement chapters follows the same format:

* **Control Objective.** A brief statement of the security goal for the chapter.
* **Sections.** Requirements are grouped into related sections, each with a short description of the defense goal.
* **Requirement Tables.** Individual requirements are presented in tables with the following columns:

| Column | Meaning |
|---|---|
| **#** | Unique requirement identifier (e.g., 1.1.1, 9.3.2). |
| **Description** | The requirement text, always beginning with "Verify that" to emphasize testability. |
| **Level** | The verification level (1, 2, or 3) indicating the depth of assurance required. |
| **Role** | Who is responsible: **D** (developer/builder), **V** (verifier/auditor), or **D/V** (both). |

### Appendices

Four appendices support the core requirements:

* **Appendix A (Glossary)** defines key terms and acronyms used throughout the standard.
* **Appendix B (References)** lists external standards, research, and frameworks referenced by AISVS requirements.
* **Appendix C (AI-Assisted Secure Coding)** provides controls for the safe use of AI coding tools during software development.
* **Appendix D (AI Security Controls Inventory)** is a cross-reference of every defense technique in AISVS, organized by security control category (authentication, authorization, encryption, input validation, and so on) with mappings back to specific requirement identifiers.

## Scope Boundaries

AISVS focuses on security controls that are specific to AI and ML systems. It intentionally excludes:

* **General application security.** Requirements covered by the [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) (such as session management, CSRF protection, or SQL injection prevention) are not repeated here. Organizations should apply ASVS alongside AISVS.
* **AI governance and risk management.** Organizational governance, risk assessment methodology, and compliance processes are better addressed by frameworks such as the NIST AI RMF and ISO/IEC 42001.
* **Vendor-specific guidance.** AISVS is vendor-neutral. It specifies what to verify, not which product to use.

## Acknowledgments

AISVS v1.0 is the result of a collaborative effort by its project leads, working group members, and community contributors. We thank everyone who has contributed requirements, reviews, and feedback to make this standard possible. A full list of contributors is available in the [Frontispiece](0x01-Frontispiece.md).

By adopting AISVS, organizations can systematically evaluate and strengthen the security posture of their AI systems, building a foundation of secure AI engineering practices that evolves alongside the technology itself.
