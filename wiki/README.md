# AISVS Research Wiki

**OWASP AI Security Verification Standard — Research & Analysis Hub**

> **Experimental, AI-generated content.** This research wiki was generated using Claude to bootstrap research scaffolding for every chapter and appendix in AISVS 1.0. The threat landscapes, tooling references, and open research questions are starting points — not vetted conclusions. All content requires human review, validation, and ongoing refinement by the community. Treat this as a living research workspace, not an authoritative source.

The goal is to attach structured research context to each set of requirements in the standard: what threats motivate them, what tools exist to implement them, where the gaps are, and what questions remain open. Each chapter page provides a template for the community to fill in with real-world incidents, tooling evaluations, and cross-references as the standard matures.

> **Standard source:** [`1.0/en/`](https://github.com/OWASP/AISVS/tree/main/1.0/en) in the main repository

---

## Chapters

| # | Chapter | Requirements | Page |
|---|---------|:---:|------|
| C1 | Training Data Integrity & Traceability | 24 | [C01 Training Data](C01-Training-Data.md) |
| C2 | User Input Validation | 33 | [C02 User Input Validation](C02-User-Input-Validation.md) |
| C3 | Model Lifecycle Management | 23 | [C03 Model Lifecycle Management](C03-Model-Lifecycle-Management.md) |
| C4 | Infrastructure & Deployment Security | 46 | [C04 Infrastructure](C04-Infrastructure.md) |
| C5 | Access Control & Identity | 26 | [C05 Access Control](C05-Access-Control.md) |
| C6 | Supply Chain Security | 33 | [C06 Supply Chain](C06-Supply-Chain.md) |
| C7 | Model Behavior & Output Control | 30 | [C07 Model Behavior](C07-Model-Behavior.md) |
| C8 | Memory, Embeddings & Vector DB Security | 25 | [C08 Memory and Embeddings](C08-Memory-and-Embeddings.md) |
| C9 | Orchestration & Agentic Action Security | 32 | [C09 Orchestration and Agents](C09-Orchestration-and-Agents.md) |
| C10 | MCP Security | 33 | [C10 MCP Security](C10-MCP-Security.md) |
| C11 | Adversarial Robustness | 38 | [C11 Adversarial Robustness](C11-Adversarial-Robustness.md) |
| C12 | Privacy Protection | 23 | [C12 Privacy](C12-Privacy.md) |
| C13 | Monitoring, Logging & Anomaly Detection | 47 | [C13 Monitoring and Logging](C13-Monitoring-and-Logging.md) |
| C14 | Human Oversight & Accountability | 25 | [C14 Human Oversight](C14-Human-Oversight.md) |
| | **Total** | **438** | |

## Appendices

| Appendix | Page |
|----------|------|
| A: Glossary | [Appendix A Glossary](Appendix-A-Glossary.md) |
| B: References | [Appendix B References](Appendix-B-References.md) |
| C: AI-Assisted Secure Coding (27 reqs) | [Appendix C AI Secure Coding](Appendix-C-AI-Secure-Coding.md) |
| D: AI Security Controls Inventory | [Appendix D Controls Inventory](Appendix-D-Controls-Inventory.md) |

## How to Use This Wiki

Each chapter page follows a consistent structure:

1. **Overview** — Control objective and chapter scope
2. **Section Breakdown** — Each section with requirement count and IDs
3. **Threat Landscape** — Known attacks, CVEs, and real-world incidents relevant to the chapter
4. **Tooling & Implementation** — Current tools, frameworks, and libraries that help implement these controls
5. **Open Research Questions** — Gaps in tooling, unresolved debates, areas needing more research
6. **Related Standards** — Cross-references to NIST, MITRE ATLAS, OWASP Top 10 for LLMs, EU AI Act, etc.
7. **Community Notes** — Space for contributor observations and discussion

---

_This wiki is maintained alongside the [AISVS repository](https://github.com/OWASP/AISVS). Contributions welcome._
