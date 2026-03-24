# OWASP Artificial Intelligence Security Verification Standard (AISVS)

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg

## What is AISVS?

The **Artificial Intelligence Security Verification Standard (AISVS)** is a community-driven catalogue of testable security requirements for AI-enabled systems. It gives developers, architects, security engineers, and auditors a structured framework to design, build, test, and verify the security of AI applications throughout their lifecycle, from data collection and model training to deployment, monitoring, and retirement.

AISVS is modeled after the [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/) and follows the same philosophy: every requirement should be **verifiable, testable, and implementable**.

### What AISVS is NOT

* **Not a governance framework.** Governance is well-covered by [NIST AI RMF](https://www.nist.gov/artificial-intelligence/risk-management-framework), [ISO/IEC 42001](https://www.iso.org/standard/81230.html), and EU AI Act compliance guides.
* **Not a risk management framework.** AISVS provides the technical controls that risk frameworks point to, but does not define risk assessment methodology.
* **Not a tool recommendation list.** AISVS is vendor-neutral and does not endorse specific products or frameworks.

### How AISVS complements other standards

| Standard | Focus | AISVS relationship |
|---|---|---|
| OWASP ASVS | Web application security | AISVS extends ASVS concepts to AI-specific threats |
| [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Awareness of top LLM risks | AISVS provides the detailed controls to mitigate those risks |
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Awareness of top agentic AI risks | AISVS provides the detailed controls to address agentic-specific threats |
| NIST AI RMF | AI risk governance | AISVS supplies the testable technical controls that AI RMF references |
| ISO/IEC 42001 | AI management systems | AISVS complements with implementation-level security verification |

## Verification Levels

Each AISVS requirement is assigned a verification level (1, 2, or 3) indicating the depth of security assurance:

| Level | Description | When to use |
|:---:|---|---|
| **1** | Essential baseline controls that every AI system should implement. | All AI applications, including internal tools and low-risk systems. |
| **2** | Standard controls for systems handling sensitive data or making consequential decisions. | Production systems, customer-facing AI, systems processing personal data. |
| **3** | Advanced controls for high-assurance environments requiring defense against sophisticated attacks. | Critical infrastructure, safety-critical AI, high-value targets, regulated industries. |

Organizations should select a target level based on the risk profile of their AI system. Most production systems should aim for at least Level 2.

## How to use AISVS

* **During design.** Use requirements as a security checklist when architecting AI systems.
* **During development.** Integrate requirements into CI/CD pipelines, code reviews, and testing.
* **During security assessments.** Use as a verification framework for penetration testing and audits.
* **For procurement.** Reference specific requirements when evaluating AI vendors and third-party models.

## Requirement Chapters

1. [Training Data Integrity & Traceability](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C01-Training-Data-Integrity-and-Traceability.md)
2. [User Input Validation](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C02-User-Input-Validation.md)
3. [Model Lifecycle Management & Change Control](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
4. [Infrastructure, Configuration & Deployment Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C04-Infrastructure.md)
5. [Access Control & Identity](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
6. [Supply Chain Security for Models, Frameworks & Data](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C06-Supply-Chain.md)
7. [Model Behavior, Output Control & Safety Assurance](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C07-Model-Behavior.md)
8. [Memory, Embeddings & Vector Database Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C08-Memory-Embeddings-and-Vector-Database.md)
9. [Autonomous Orchestration & Agentic Action Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C09-Orchestration-and-Agentic-Action.md)
10. [Model Context Protocol (MCP) Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C10-MCP-Security.md)
11. [Adversarial Robustness & Attack Resistance](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C11-Adversarial-Robustness.md)
12. [Privacy Protection & Personal Data Management](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C12-Privacy.md)
13. [Monitoring, Logging & Anomaly Detection](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C13-Monitoring-and-Logging.md)
14. [Human Oversight and Trust](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C14-Human-Oversight.md)

## Appendices

* [Appendix A: Glossary](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x90-Appendix-A_Glossary.md)
* [Appendix B: References](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x91-Appendix-B_References.md)
* [Appendix C: AI-Assisted Secure Coding](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x92-Appendix-C_AI_for_Code_Generation.md)
* [Appendix D: AI Security Controls Inventory](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x93-Appendix-D_AI_Security_Controls_Inventory.md)

## Contributing

We welcome contributions from the community. Please [open an issue](https://github.com/OWASP/AISVS/issues) to report bugs or suggest improvements. We may ask you to [submit a pull request](https://github.com/OWASP/AISVS/pulls) based on the discussion.

## Project Leaders

This project was founded by [Jim Manico](https://github.com/jmanico). Current project leadership includes [Jim Manico](https://github.com/jmanico), [Otto Sulin](https://github.com/ottosulin), and [Russ Memisyazici](https://github.com/vtknightmare).

## License

The entire project content is under the **[Creative Commons Attribution-Share Alike v4.0](https://creativecommons.org/licenses/by-sa/4.0/)** license.
