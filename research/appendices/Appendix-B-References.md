# Appendix B: References — Research Notes

> **Source:** [`1.0/en/0x91-Appendix-B_References.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x91-Appendix-B_References.md)

## Overview

Appendix B lists the standards, frameworks, specifications, and publications referenced throughout AISVS. This research page audits coverage: which chapter references are missing from Appendix B, which Appendix B entries aren't cited, and where URL inconsistencies exist. As of May 2026, **80+ additional references** have been identified from recent standards publications, framework releases, and specification updates that should be considered for inclusion. The Q1/Q2 2026 period has been particularly active: CSA expanded the CSAI Foundation with agentic assurance and CNA work, NIST published AI Agent Identity and AI 800-4 monitoring guidance, MITRE ATLAS published the OpenClaw investigation, and OWASP released new exploit, red-teaming, MCP, AIBOM, landscape, and data-security resources.

---

## Coverage Audit

### References Cited in Chapters but Missing from Appendix B

The original audit identified 39 references cited across chapters but absent from Appendix B. These have been expanded with newly published standards and frameworks from 2025–2026.

#### Standards and Frameworks (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| NIST AI 600-1: Generative AI Profile | Jul 2024 | C07, C01, C12, C14 | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence |
| NIST IR 8596: Cybersecurity Framework Profile for AI (draft) | Dec 2025 | C04, C13, C11 | https://csrc.nist.gov/pubs/ir/8596/iprd |
| NIST COSAiS: SP 800-53 Control Overlays for AI | Aug 2025 | C04, C05, C09, C06 | https://csrc.nist.gov/projects/cosais |
| NIST Cybersecurity Framework 2.0 | Feb 2024 | C4 | https://www.nist.gov/cyberframework |
| NIST SP 800-207: Zero Trust Architecture | Aug 2020 | C5, C9, C10 | https://csrc.nist.gov/pubs/sp/800/207/final |
| NIST SP 800-162: Guide to ABAC | Jan 2014 | C5 | https://csrc.nist.gov/pubs/sp/800/162/final |
| NIST SP 800-63-3: Digital Identity Guidelines | Jun 2017 | C5 | https://csrc.nist.gov/pubs/sp/800/63/3/final |
| NIST IR 8360: ML for Access Control Policy Verification | Nov 2021 | C5 | https://csrc.nist.gov/pubs/ir/8360/final |
| NIST AI 100-2e2023: Adversarial Machine Learning | Jan 2024 | C11 | https://csrc.nist.gov/pubs/ai/100/2/e2023/final |
| NIST CAISI AI Agent Standards Initiative | Feb 2026 | C09, C05, C10 | https://www.nist.gov/caisi/ai-agent-standards-initiative |
| NIST AI 800-4: Challenges to Monitoring Deployed AI Systems | Mar 2026 | C13, C14, C07 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf |
| NIST CAISI RFI: Security Considerations for AI Agents | Jan 2026 | C09, C05, C10 | https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents |
| NIST NCCoE Concept Paper: AI Agent Identity and Authorization | Feb 2026 | C05, C09, C10 | https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd |
| MITRE SAFE-AI Framework | Apr 2025 | C04, C03, C11 | https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf |
| CSA AI Controls Matrix (AICM) — 243 controls, 18 domains | Jul 2025 | All chapters | https://cloudsecurityalliance.org/artifacts/ai-controls-matrix |
| CSA CSAI Foundation: Securing the Agentic Control Plane | Mar 2026 | C05, C09, C10, C13 | https://cloudsecurityalliance.org/press-releases/2026/03/23/csa-securing-the-agentic-control-plane |
| CSAI Foundation Key Milestones: Catastrophic Risk Annex, CNA authorization, AARM, and ATF | Apr 2026 | C09, C10, C13, C14 | https://cloudsecurityalliance.org/press-releases/2026/04/29/csai-foundation-announces-key-milestones-to-secure-the-agentic-control-plane |
| ISO/IEC 42005:2025: AI System Impact Assessment | May 2025 | C14, C12, C03 | https://www.iso.org/standard/42005 |
| ISO/IEC 42006:2025: AIMS Audit and Certification | 2025 | C03, C14 | https://www.iso.org/standard/42006 |
| ISO/IEC 27090 (in development): AI Security | Expected 2026 | C11, C07, C04 | Referenced via https://owaspai.org/ |
| ISO/IEC 27091 (in development): AI Privacy | Expected 2026 | C12, C01 | Referenced via https://owaspai.org/ |
| CISA Advisory: Securing Data for AI Systems | 2025 | C1 | https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-142a |
| Cloud Security Alliance: Cloud Controls Matrix | — | C4 | https://cloudsecurityalliance.org/research/cloud-controls-matrix/ |
| ENISA: Secure Infrastructure Design | — | C4 | https://www.enisa.europa.eu/topics/critical-information-infrastructures-and-services |
| CIS Controls v8 | — | C4 | https://www.cisecurity.org/controls/v8 |
| Kubernetes Security Best Practices | — | C4 | https://kubernetes.io/docs/concepts/security/ |
| MLOps Principles | — | C3 | https://ml-ops.org/content/mlops-principles |

#### OWASP Publications (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| OWASP Top 10 for Agentic Applications 2026 | Dec 2025 | C09 | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| OWASP MCP Top 10 (v0.1 Beta) | 2025 | C10 | https://owasp.org/www-project-mcp-top-10/ |
| OWASP AI Testing Guide v1 | Nov 2025 | C07, C11, C01, C12 | https://owasp.org/www-project-ai-testing-guide/ |
| OWASP AI Exchange (Flagship) | Ongoing | All | https://owaspai.org/ |
| OWASP Agentic Security Initiative | Feb 2025+ | C09, C10, C05 | https://genai.owasp.org/initiatives/agentic-security-initiative/ |
| OWASP Agentic AI Threats and Mitigations | 2025 | C09 | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ |
| OWASP Guide for Secure MCP Server Development | Feb 2026 | C10, C09 | https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/ |
| OWASP Cheat Sheet: Securely Using Third-Party MCP Servers | 2026 | C10, C06 | https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/ |
| OWASP AIBOM Generator (AI Bill of Materials) | Dec 2025 | C06 | https://genai.owasp.org/resource/owasp-aibom-generator/ |
| OWASP Vendor Evaluation Criteria for AI Red Teaming v1.0 | Feb 2026 | C11, C07 | https://genai.owasp.org/resource/owasp-vendor-evaluation-criteria-for-ai-red-teaming-providers-tooling-v1-0/ |
| OWASP GenAI Red Teaming Guide | Jan 2025 | C11, C07 | https://genai.owasp.org/resource/genai-red-teaming-guide/ |
| OWASP GenAI Data Security Risks and Mitigations 2026 | Mar 2026 | C01, C08, C12 | https://genai.owasp.org/resource/owasp-genai-data-security-risks-mitigations-2026/ |
| OWASP AI Security Solutions Landscape for Agentic AI Q2 2026 | Mar 2026 | All | https://genai.owasp.org/resource/ai-security-solutions-landscape-for-agentic-ai-q2-2026/ |
| OWASP AI Security Solutions Landscape for AI and Agentic Red Teaming Q2 2026 | Apr 2026 | C07, C11, C13 | https://genai.owasp.org/resource/ai-security-solutions-landscape-for-ai-and-agentic-red-teaming-q2-2026/ |
| OWASP GenAI Exploit Round-up Report Q1 2026 | Apr 2026 | C02, C06, C09, C10, C13 | https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/ |
| LLM Prompt Injection Prevention Cheat Sheet | — | C2 | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html |
| AI Agent Security Cheat Sheet | — | C9, C10 | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html |

#### OWASP LLM Top 10 Individual Entries (missing — only parent project page is in Appendix B)

| Reference | Cited In | Link |
|-----------|----------|------|
| LLM01:2025 Prompt Injection | C2 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| LLM02:2025 Sensitive Information Disclosure | C8, C11, C12 | https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/ |
| LLM03:2025 Supply Chain | C6 | https://genai.owasp.org/llmrisk/llm032025-supply-chain/ |
| LLM04:2025 Data and Model Poisoning | C8, C11 | https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/ |
| LLM05:2025 Improper Output Handling | C7 | https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ |
| LLM06:2025 Excessive Agency | C7, C9 | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ |
| LLM08:2025 Vector and Embedding Weaknesses | C8 | https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ |
| LLM10:2025 Unbounded Consumption | C9, C11 | https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ |

#### CoSAI Publications (missing — new organization, not in Appendix B)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| CoSAI Principles for Secure-by-Design Agentic Systems | Jul 2025 | C09, C14, C05 | https://www.coalitionforsecureai.org/announcing-the-cosai-principles-for-secure-by-design-agentic-systems/ |
| CoSAI MCP Security Taxonomy (12 threats, ~40 distinct attack patterns) | Jan 2026 | C10, C09 | https://www.coalitionforsecureai.org/coalition-for-secure-ai-releases-extensive-taxonomy-for-model-context-protocol-security/ |
| CoSAI AI Model Signing Framework | Nov 2025 | C06, C03 | https://www.coalitionforsecureai.org/building-trust-in-ai-supply-chains-why-model-signing-is-critical-for-enterprise-security/ |
| CoSAI AI Incident Response Framework v1.0 | Nov 2025 | C13, C04 | https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/ |

#### EU AI Act Implementing Guidance (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| EU Code of Practice for General-Purpose AI (GPAI) — Final Version | Jul 2025 | C07, C01, C14 | https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai |
| EU Code of Practice on Transparency of AI-Generated Content | Dec 2025 | C07, C14 | https://artificialintelligenceact.eu/introduction-to-code-of-practice/ |
| EC Guidelines for Providers of General-Purpose AI Models | 2025 | C07, C03, C14 | https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers |

#### MCP Specification Updates (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| MCP Authorization Specification (2025-06-18) | Jun 2025 | C10 | https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization |
| MCP Specification 2025-11-25 Revision | Nov 2025 | C10 | https://modelcontextprotocol.io/specification/2025-11-25/changelog |
| MCP Draft Authorization Spec (client-credentials, enterprise IdP) | Draft 2026 | C10, C05 | https://modelcontextprotocol.io/specification/draft/basic/authorization |

#### Key RFCs Mandated by MCP (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| RFC 8707: Resource Indicators for OAuth 2.0 | Feb 2020 | C10, C05 | https://www.rfc-editor.org/rfc/rfc8707 |
| RFC 9728: OAuth 2.0 Protected Resource Metadata | Dec 2024 | C10, C05 | https://www.rfc-editor.org/rfc/rfc9728 |
| RFC 7636: Proof Key for Code Exchange (PKCE) | Sep 2015 | C10, C05 | https://datatracker.ietf.org/doc/html/rfc7636 |
| RFC 9449: OAuth 2.0 DPoP (Demonstrating Proof of Possession) | Sep 2023 | C10, C05 | https://www.rfc-editor.org/rfc/rfc9449.html |
| RFC 8693: OAuth 2.0 Token Exchange | Jan 2020 | C10, C09 | https://datatracker.ietf.org/doc/html/rfc8693 |

#### MITRE ATLAS Technique Pages and Case Studies (missing — only main ATLAS site in Appendix B)

| Reference | Cited In | Link |
|-----------|----------|------|
| AML.T0051: LLM Prompt Injection | C2 | https://atlas.mitre.org/techniques/AML.T0051 |
| AML.T0029: Denial of ML Service | C2, C9 | https://atlas.mitre.org/techniques/AML.T0029 |
| AML.T0034: Cost Harvesting | C2, C9 | https://atlas.mitre.org/techniques/AML.T0034 |
| AML.T0010: Supply Chain Compromise | C6 | https://atlas.mitre.org/techniques/AML.T0010 |
| AML.T0018: Backdoor ML Model | C11 | https://atlas.mitre.org/techniques/AML.T0018 |
| AML.T0024.000: Infer Training Data Membership | C8, C11 | https://atlas.mitre.org/techniques/AML.T0024.000 |
| AML.T0024.001: Invert ML Model | C8, C11 | https://atlas.mitre.org/techniques/AML.T0024.001 |
| AML.T0024.002: Extract ML Model | C11 | https://atlas.mitre.org/techniques/AML.T0024.002 |
| AML.T0070: RAG Poisoning | C8 | https://atlas.mitre.org/techniques/AML.T0070 |
| AML.T0100: AI Agent Clickbait | C09 | https://atlas.mitre.org/techniques/AML.T0100 |
| AML.M00150: Adversarial Input Detection | C2 | https://atlas.mitre.org/mitigations/AML.M00150 |
| MITRE ATLAS OpenClaw Investigation | C09, C10, C11 | https://www.mitre.org/news-insights/publication/mitre-atlas-openclaw-investigation |

#### Vendor Documentation (missing)

| Reference | Cited In | Link |
|-----------|----------|------|
| Mitigate jailbreaks and prompt injections (Anthropic) | C2 | https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks |
| Reinforcement fine-tuning (OpenAI) | C3 | https://platform.openai.com/docs/guides/reinforcement-fine-tuning |
| AI adversarial robustness (IBM Research) | C3 | https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness |
| OpenAI Privacy Center: Data Deletion Controls | C1 | https://privacy.openai.com/policies?modal=take-control |
| SBOM Overview (CISA) | C6 | https://www.cisa.gov/sbom |

---

### References in Appendix B Not Cited by Any Chapter (C1-C14)

| Reference | Category | Notes |
|-----------|----------|-------|
| NIST SP 800-218A: Secure Software Dev for GenAI | Standards | Cited in Appendix C and D only |
| ISO/IEC 42001:2023 | Standards | Cited in Appendix C and D only — but now also relevant to Appendix D maturity ratings |
| OWASP ASVS | Standards | Cited in Appendix D only |
| OWASP Secure Coding Practices | Standards | Cited in Appendix C only |
| OpenID Connect Core 1.0 | Specifications | Not cited in any chapter or appendix |
| NIST Post-Quantum Cryptography Standards | Cryptographic | Not cited in any chapter — potential gap for C4.7 hardware security |

---

## URL Inconsistencies

The same document is referenced with different URLs across chapters:

| Document | URLs Used | Recommendation |
|----------|-----------|----------------|
| NIST AI RMF 1.0 | `nist.gov/itl/ai-risk-management-framework` (C1, C4, C12), `nist.gov/system/files/documents/...` (C13), `doi.org/10.6028/NIST.AI.100-1` (C13), `nvlpubs.nist.gov/...` (Appendix B) | Standardize on `nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf` |
| NIST SP 800-207 | `csrc.nist.gov/pubs/sp/800/207/final` (C5) vs `csrc.nist.gov/pubs/detail/sp/800-207/final` (C9, C10) | Standardize on `/pubs/sp/` form |
| MITRE ATLAS AML.T0024.001 | "Invert AI Model" (C8) vs "Invert ML Model" (C11) | Use consistent title "Invert ML Model" (ATLAS canonical) |
| ISO/IEC 42001 | Appendix B source previously used `iso.org/standard/81230.html`; current source now uses `iso.org/standard/42001` | Keep the corrected short ISO URL and avoid reintroducing the stale numeric page |
| OAuth 2.1 | `draft-ietf-oauth-v2-1-11` in Appendix B source vs `draft-ietf-oauth-v2-1-15` (current as of March 2026) | Update to latest draft number |
| MCP Specification | `modelcontextprotocol.io` (Appendix B) — needs versioned links to authorization spec and November 2025 revision | Add versioned spec links |

---

## Structural Issues

1. **C14 has an empty References section** — the `## References` header exists but no references are listed. Relevant references: ISO 42005 (AI Impact Assessment), CoSAI Principles for Secure-by-Design Agentic Systems, EU GPAI Code of Practice.

2. **Decision needed: granular MITRE ATLAS links** — 10 specific ATLAS technique/mitigation pages are cited across chapters. **Recommendation: list them individually** since they are primary threat references for specific requirements, not just background context.

3. **Decision needed: OWASP LLM Top 10 entries** — 8 individual risk entries are cited. **Recommendation: list them individually** since each maps to specific chapters and requirements.

4. **OAuth 2.1 draft number is stale** — Appendix B source cites `draft-ietf-oauth-v2-1-11` but current is `draft-ietf-oauth-v2-1-15` (March 2026). Should be updated before the draft becomes an RFC.

5. **New category needed: "AI Agent and Agentic Frameworks"** — CoSAI, OWASP Agentic Security Initiative, NIST CAISI, and the OWASP Top 10 for Agentic Applications form a distinct category not well served by current Appendix B structure.

6. **New category needed: "MCP-Specific References"** — MCP specification versions, authorization spec, OWASP MCP Top 10, OWASP Guide for Secure MCP Server Development, CoSAI MCP taxonomy, and mandated RFCs warrant their own section given MCP has its own dedicated chapter (C10).

7. **NIST AI 800-4 (March 2026) cross-references needed** — This new NIST publication on post-deployment AI monitoring challenges is directly relevant to C13 (Monitoring and Logging) and C14 (Human Oversight). It identifies six monitoring categories and documents barriers from workshops with 200+ practitioners. Should be referenced in those chapters.

8. **OWASP GenAI project publication velocity** — The OWASP GenAI Security Project published at least nine high-value resources between December 2025 and April 2026 (AIBOM generator, MCP server security guide, MCP third-party server cheat sheet, red teaming vendor evaluation criteria, data security risks guide, two Q2 2026 solution landscapes, the GenAI Red Teaming Guide, and the Q1 2026 exploit round-up). Appendix B should consider a dedicated "OWASP GenAI Security Project Resources" sub-section.

9. **EU GPAI Code of Practice now final** — The Code of Practice for general-purpose AI was finalized in July 2025 and the Commission now maintains the official code and signatory page at https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai. The complementary GPAI provider guidelines explain the obligations that entered into application on August 2, 2025; Commission enforcement powers begin August 2, 2026.

10. **MITRE ATLAS v5.4.0 (February 2026) agentic techniques** — The framework now covers 16 tactics and 84+ techniques after the October 2025 and February 2026 updates added 14 new agentic AI attack techniques including AI Agent Clickbait (AML.T0100), Publish Poisoned AI Agent Tool, and Escape to Host. The OpenClaw investigation (February 2026) demonstrated real-world exploit paths in AI-first ecosystems. These should be cross-referenced in C09 and C11.

11. **NIST NCCoE AI Agent Identity concept paper** — Published February 5, 2026, this concept paper outlines a potential NCCoE project applying identity standards (OAuth 2.0, SPIFFE) to AI agents. It covers identification, authorization, auditing, non-repudiation, and prompt injection mitigation for autonomous agents. Comment period closes April 2, 2026. Directly relevant to C05, C09, and C10.

12. **CSA launches and expands CSAI Foundation (March-April 2026)** — The Cloud Security Alliance launched CSAI as a dedicated 501(c)(3) for AI security, with the strategic mission of "Securing the Agentic Control Plane." Six programs cover visibility, best practices, education, governance, assurance, and research. In April 2026 CSA announced CNA authorization, the STAR for AI Catastrophic Risk Annex, and stewardship for AARM and the Agentic Trust Framework. Relevant to C09, C10, C13, and C14.

13. **Exploit reporting now spans model, agent, and orchestration layers** — OWASP's Q1 2026 exploit round-up maps incidents such as OpenClaw, CustomMCP/Flowise, indirect prompt injection, and AI-assisted attack workflows to LLM and agentic risk categories. Appendix B should treat quarterly exploit reports as threat-intelligence references for C02, C06, C09, C10, and C13 rather than as generic news.

---

## Recommended Appendix B Structure

Based on the audit, Appendix B should be restructured to cover the full reference landscape:

| Category | Current Count | Missing | Recommended Total |
|----------|:------------:|:-------:|:-----------------:|
| Standards and Frameworks | 7 | 27 (incl. NIST AI 800-4, CAISI RFI, NCCoE AI Agent Identity, CSA CSAI) | ~34 |
| Specifications and Protocols | 5 | 8 (MCP spec versions, draft auth + RFCs) | ~13 |
| OWASP Publications | 3 | 20 (LLM entries, agentic, MCP guides, AIBOM, red teaming, data security, landscapes, exploit reporting) | ~23 |
| MITRE ATLAS | 1 (main site) | 12 (individual techniques plus OpenClaw investigation) | ~13 |
| CoSAI | 0 | 4 | 4 |
| EU AI Act & Implementing Guidance | 1 | 3 (codes of practice + GPAI guidelines) | 4 |
| Privacy and Data Protection | 3 | 0 | 3 |
| Cryptographic Standards | 2 | 0 | 2 |
| Policy Engines | 2 | 0 | 2 |
| Vendor Documentation | 0 | 5 | 5 |
| **Total** | **18** | **~80** | **~104** |

---

## Related Pages

- [Appendix A: Glossary](Appendix-A-Glossary.md) — Useful companion when reference additions introduce new terminology, especially around agent security, MCP, MITRE ATLAS, and supply-chain assurance.
- [C01-01: Training Data Origin Traceability](../chapters/C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md) — Connects Appendix B reference coverage to provenance, data-source inventories, and regulatory traceability requirements.
- [C03-04: Secure Development Practices](../chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md) — Shows where MCP, agent runtime, prompt versioning, and secure build references need direct chapter support.
- [C03-05: Hosted Provider Managed Controls](../chapters/C03-Model-Lifecycle-Management/C03-05-Hosted-Provider-Managed-Controls.md) — Helps map provider-dependency and hosted-model reference gaps back to lifecycle and change-management controls.
- [C06-03: Third-Party Dataset Risk](../chapters/C06-Supply-Chain/C06-03-Third-Party-Dataset-Risk.md) — Shares the supply-chain, AI BOM, dataset provenance, and compliance references most likely to require Appendix B coverage.

---

## Community Notes

_Discussion about reference scope, URL standardization, and completeness._

---

[README](../README.md)
