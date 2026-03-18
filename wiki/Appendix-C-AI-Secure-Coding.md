# Appendix C: AI-Assisted Secure Coding

> **Source:** [`1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)
> **Requirements:** 27 | **Sections:** 9

## Overview

Controls for the safe use of AI-assisted coding tools, covering workflow security, tool qualification, prompt management, code validation, and deployment controls.

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| AC.1 | AI-Assisted Secure-Coding Workflow | 3 | AC.1.1–AC.1.3 |
| AC.2 | AI Tool Qualification & Threat Modeling | 3 | AC.2.1–AC.2.3 |
| AC.3 | Secure Prompt & Context Management | 3 | AC.3.1–AC.3.3 |
| AC.4 | Validation of AI-Generated Code | 3 | AC.4.1–AC.4.3 |
| AC.5 | Explainability & Traceability of Code Suggestions | 3 | AC.5.1–AC.5.3 |
| AC.6 | Continuous Feedback & Model Fine-Tuning | 3 | AC.6.1–AC.6.3 |
| AC.7 | AI-Generated Infrastructure & Pipeline Artifacts | 3 | AC.7.1–AC.7.3 |
| AC.8 | Autonomous Agent Change Control Constraints | 3 | AC.8.1–AC.8.3 |
| AC.9 | AI Provenance-Aware Deployment Controls | 3 | AC.9.1–AC.9.3 |

---

## Threat Landscape

- AI-generated code introducing subtle vulnerabilities (SQL injection, XSS, insecure defaults)
- Prompt injection through repository context (malicious CLAUDE.md, .cursorrules files)
- Over-reliance on AI-generated code without human review
- Leaked secrets or PII in prompts sent to cloud-hosted coding assistants
- AI-generated infrastructure-as-code with insecure defaults

## Tooling & Implementation

- **Coding assistants:** GitHub Copilot, Cursor, Claude Code, Amazon Q Developer
- **Code scanning:** Semgrep, CodeQL, Snyk Code (applied to AI-generated output)
- **Provenance tracking:** Git metadata, AI attribution in commit messages
- **Sandbox testing:** CI/CD gates for AI-generated code, pre-commit hooks

## Open Research Questions

- [ ] What percentage of AI-generated code contains security vulnerabilities in practice?
- [ ] How should organizations track and audit AI-generated vs. human-written code?
- [ ] What constitutes adequate review of AI-generated infrastructure-as-code?
- [ ] How do autonomous coding agents change the threat model for SDLC security?

---

## Community Notes

_Discussion about AI-assisted coding security practices._

---

