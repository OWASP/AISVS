# Appendix B: References — Research Notes

> **Source:** [`1.0/en/0x91-Appendix-B_References.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x91-Appendix-B_References.md)

## Overview

Appendix B lists the standards, frameworks, specifications, and publications referenced throughout AISVS. This research page audits coverage: which chapter references are missing from Appendix B, which Appendix B entries aren't cited, and where URL inconsistencies exist. As of June 2026, **~110 additional references** have been identified from recent standards publications, framework releases, and specification updates that should be considered for inclusion. The Q1/Q2 2026 period has been particularly active: CSA stood up the CSAI Foundation as a standalone 501(c)(3) with six strategic programs (AI Risk Observatory, Agentic Best Practices, Education and Credentialing, CxOtrust, Global Assurance and Trust, and Future Forward Initiatives), obtained CNA authorization for agentic AI, published the AICM v1.0.3 release, and released the SANS/CSA/[un]prompted/OWASP joint *AI Vulnerability Storm* emergency briefing in April 2026; NIST published the AI 100-2 E2025 final revision of its adversarial ML taxonomy (covering generative AI, agent vulnerabilities, and enterprise reference architectures), the dual-use misuse risk draft (AI 800-1 IPD2), the benchmark-evaluation draft (AI 800-2), the statistical-models evaluation report (AI 800-3), the post-deployment monitoring report (AI 800-4), the CAISI DeepSeek V4 Pro evaluation, and signalled a summer-2026 cybersecurity framework profile with predictive- and agentic-AI control overlays; MITRE ATLAS published the OpenClaw investigation and moved to a monthly release cadence with a Technique Maturity filter and a Rapid Response Report pipeline; the EU Council and Parliament reached a provisional Digital AI Omnibus agreement on 7 May 2026 that pushes transparency watermarking to 2 December 2026 and high-risk Annex III obligations to 2 December 2027; and OWASP released new exploit, red-teaming, MCP, AIBOM, FinBot, landscape, and data-security resources. The late-May/early-June 2026 window added five more developments worth tracking: CISA and five international partners (NSA, ASD ACSC, CCCS, NCSC-UK, NCSC-NZ) published the first joint Five Eyes guide on *Careful Adoption of Agentic AI Services* (30 April 2026); OWASP released *State of Agentic AI Security and Governance 2.01* (1 June 2026); the CSAI Foundation announced RiskRubric V2 as its next agentic-control-plane milestone (8 June 2026, launching Q3 2026); the MCP project locked the 2026-07-28 release candidate (21 May 2026) — the largest protocol revision since launch, with a stateless core that removes protocol-level sessions; and the European Parliament's plenary adopted the Digital AI Omnibus on 16 June 2026 (423 in favour, 57 against, 174 abstentions), leaving only formal Council adoption — expected before the original 2 August 2026 high-risk deadline — to finalise the revised timeline that defers stand-alone high-risk obligations to 2 December 2027.

---

## Coverage Audit

### References Cited in Chapters but Missing from Appendix B

The original audit identified 39 references cited across chapters but absent from Appendix B. These have been expanded with newly published standards and frameworks from 2025–2026.

#### Standards and Frameworks (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| NIST AI 600-1: Generative AI Profile | Jul 2024 | C07, C01, C11, C09 | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence |
| NIST IR 8596: Cybersecurity Framework Profile for AI (draft) | Dec 2025 | C04, C12, C11 | https://csrc.nist.gov/pubs/ir/8596/iprd |
| NIST COSAiS: SP 800-53 Control Overlays for AI (predictive-AI overlay draft expected summer 2026; agentic-AI overlay draft expected late summer/early fall 2026; finalisation targeted for 2027) | Aug 2025+ | C04, C05, C06, C09 | https://csrc.nist.gov/projects/cosais |
| Nextgov coverage: NIST summer-2026 AI cyber guidelines roadmap (CSF profile, predictive overlay, agentic overlay) | May 2026 | C04, C09, C12 | https://www.nextgov.com/artificial-intelligence/2026/05/nist-aims-summer-release-ai-cyber-guidelines/413559/ |
| NIST CAISI Frontier Model Pre-Release Evaluation Program (Google DeepMind, Microsoft, xAI agreements announced 5 May 2026, joining OpenAI and Anthropic; 40+ completed evaluations including classified interagency TRAINS Taskforce assessments) | May 2026 | C03, C07, C11, C09 | https://www.cybersecuritydive.com/news/nist-ai-model-testing-caisi-google-microsoft/819452/ |
| CISA / NSA / ASD ACSC / CCCS / NCSC-UK / NCSC-NZ joint guide: Careful Adoption of Agentic AI Services (first Five Eyes agentic AI security guidance; five risk categories: privilege escalation, design and configuration flaws, behavioral misalignment, structural cascading failures, accountability opacity) | Apr 2026 | C04, C09 | https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-ai-services |
| CSAI Foundation RiskRubric V2 announcement (systematic AI model risk quantification methodology spanning models to autonomous control loops; partners include Deloitte Italy, PointGuardAI, Tumeryk; launch slated for Q3 2026) | Jun 2026 | C03, C07, C11 | https://cloudsecurityalliance.org/press-releases/2026/06/08/csai-foundation-announces-riskrubric-v2-as-the-next-key-milestone-to-secure-the-agentic-control-plane |
| CSA Research Note: MITRE ATT&CK and ATLAS Agentic Gap Analysis (techniques unique to autonomous agent control planes) | Mar 2026 | C09, C11 | https://labs.cloudsecurityalliance.org/agentic/csa-research-note-atlas-agentic-gap-analysis-20260327/ |
| NIST AI 800-1 (IPD2): Managing Misuse Risk for Dual-Use Foundation Models | Jan 2025 (2nd public draft) | C03, C11, C07, C09 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-1.ipd2.pdf |
| NIST AI 800-2: Practices for Automated Benchmark Evaluations of Language Models (draft) | Jan 2026 | C03, C07, C11, C09 | https://www.nist.gov/news-events/news/2026/01/towards-best-practices-automated-benchmark-evaluations |
| NIST Cybersecurity Framework 2.0 | Feb 2024 | C4 | https://www.nist.gov/cyberframework |
| NIST SP 800-207: Zero Trust Architecture | Aug 2020 | C5, C9, C10 | https://csrc.nist.gov/pubs/sp/800/207/final |
| NIST SP 800-162: Guide to ABAC | Jan 2014 | C5 | https://csrc.nist.gov/pubs/sp/800/162/final |
| NIST SP 800-63-4: Digital Identity Guidelines | Jul 2025 | C05, C09, C10 | https://csrc.nist.gov/pubs/sp/800/63/4/final |
| NIST IR 8360: ML for Access Control Policy Verification | Nov 2021 | C5 | https://csrc.nist.gov/pubs/ir/8360/final |
| NIST AI 100-2e2023: Adversarial Machine Learning | Jan 2024 | C11 | https://csrc.nist.gov/pubs/ai/100/2/e2023/final |
| NIST AI 100-2 E2025: Adversarial Machine Learning — Taxonomy and Terminology of Attacks and Mitigations (final, supersedes E2023; adds GenAI misuse/prompt-injection, agent vulnerabilities, supply-chain risk, and enterprise reference architectures) | Mar 2025 | C02, C03, C08, C11 | https://csrc.nist.gov/pubs/ai/100/2/e2025/final |
| NIST CAISI AI Agent Standards Initiative | Feb 2026 | C09, C05, C10 | https://www.nist.gov/caisi/ai-agent-standards-initiative |
| NIST AI 800-3: Expanding the AI Evaluation Toolbox with Statistical Models | Feb 2026 | C03, C07, C11, C09 | https://www.nist.gov/publications/expanding-ai-evaluation-toolbox-statistical-models |
| NIST AI 800-4: Challenges to Monitoring Deployed AI Systems | Mar 2026 | C12, C09, C07 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf |
| NIST CAISI Evaluation of DeepSeek V4 Pro | May 2026 | C03, C11, C09 | https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro |
| NIST CAISI RFI: Security Considerations for AI Agents | Jan 2026 | C09, C05, C10 | https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents |
| NIST NCCoE Concept Paper: AI Agent Identity and Authorization | Feb 2026 | C05, C09, C10 | https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd |
| MITRE SAFE-AI Framework | Apr 2025 | C04, C03, C11 | https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf |
| CSA AI Controls Matrix (AICM) — 243 controls, 18 domains; v1.0.3 maintenance release (CCM v4.0.13 alignment, synchronized to upcoming CCM v4.1) | Jul 2025 (v1), 2026 (v1.0.3) | All chapters | https://cloudsecurityalliance.org/artifacts/ai-controls-matrix |
| CSA STAR for AI: Catastrophic Risk Annex (extends AICM/STAR-for-AI to catastrophic-risk scenarios; rollout runs June 2026 through December 2027) | Apr 2026 | C04, C12, C09 | https://cloudsecurityalliance.org/blog/2026/04/29/the-catastrophic-risk-annex-next-gen-ai-security-controls |
| CSA / SANS / [un]prompted / OWASP GenAI — *The AI Vulnerability Storm: Building a Mythos-Ready Security Program* (13-item risk register mapped to OWASP LLM Top 10 2025, OWASP Agentic Top 10 2026, MITRE ATLAS, NIST CSF 2.0; 11-item priority actions table; board-briefing pack) | Apr 2026 | C04, C11, C12, C09 | https://cloudsecurityalliance.org/artifacts/the-ai-vulnerability-storm |
| SANS / CSA / [un]prompted / OWASP joint press briefing on the AI Vulnerability Storm (exploit windows now sub-day; Zero Day Clock context) | Apr 2026 | C04, C11, C12 | https://www.sans.org/press/announcements/emergency-strategy-briefing-ai-driven-vulnerability-discovery-compresses-exploit-timelines |
| CSA CSAI Foundation: Securing the Agentic Control Plane | Mar 2026 | C05, C09, C10, C12 | https://cloudsecurityalliance.org/press-releases/2026/03/23/csa-securing-the-agentic-control-plane |
| CSAI Foundation 2026 Strategic Mission (six programs: AI Risk Observatory, Agentic Best Practices, Education/Credentialing, CxOtrust, Global Assurance & Trust, Future Forward) | 2026 | C09, C10, C12, C05 | https://csai.foundation/csai-mission |
| CSAI Foundation Key Milestones: Catastrophic Risk Annex, CNA authorization, AARM, and ATF | Apr 2026 | C09, C10, C12 | https://cloudsecurityalliance.org/press-releases/2026/04/29/csai-foundation-announces-key-milestones-to-secure-the-agentic-control-plane |
| CSA Broadens Agentic AI Security Work — new risk and vulnerability efforts | May 2026 | C09, C10, C12 | https://redmondmag.com/articles/2026/05/05/csa-broadens-agentic-ai-security-work-with-new-risk.aspx |
| ISO/IEC 42005:2025: AI System Impact Assessment | May 2025 | C09, C11, C03 | https://www.iso.org/standard/42005 |
| ISO/IEC 42006:2025: AIMS Audit and Certification | 2025 | C03, C09 | https://www.iso.org/standard/42006 |
| ISO/IEC FDIS 27090: Cybersecurity — AI — Guidance for Security Threats | FDIS final text registered 12 Mar 2026; publication expected later in 2026 | C11, C07, C04 | https://www.iso.org/standard/56581.html |
| ISO/IEC DIS 27091: Cybersecurity and Privacy — AI — Privacy Protection | DIS ballot closed 26 Feb 2026; publication possible late 2026 | C11, C01 | https://www.iso27001security.com/post/iso-iec-27091-ai-privacy-dis |
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
| OWASP AI Testing Guide v1 | Nov 2025 | C07, C11, C01 | https://owasp.org/www-project-ai-testing-guide/ |
| OWASP AI Exchange (Flagship) | Ongoing | All | https://owaspai.org/ |
| OWASP Agentic Security Initiative | Feb 2025+ | C09, C10, C05 | https://genai.owasp.org/initiatives/agentic-security-initiative/ |
| OWASP Agentic AI Threats and Mitigations | 2025 | C09 | https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/ |
| OWASP Guide for Secure MCP Server Development | Feb 2026 | C10, C09 | https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/ |
| OWASP Cheat Sheet: Securely Using Third-Party MCP Servers | 2026 | C10, C06 | https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/ |
| OWASP AIBOM Generator (AI Bill of Materials) | Dec 2025 | C06 | https://genai.owasp.org/resource/owasp-aibom-generator/ |
| OWASP Vendor Evaluation Criteria for AI Red Teaming v1.0 | Feb 2026 | C11, C07 | https://genai.owasp.org/resource/owasp-vendor-evaluation-criteria-for-ai-red-teaming-providers-tooling-v1-0/ |
| OWASP GenAI Red Teaming Guide | Jan 2025 | C11, C07 | https://genai.owasp.org/resource/genai-red-teaming-guide/ |
| OWASP GenAI Data Security Risks and Mitigations 2026 | Mar 2026 | C01, C08, C11 | https://genai.owasp.org/resource/owasp-genai-data-security-risks-mitigations-2026/ |
| OWASP AI Security Solutions Landscape for LLM and GenAI Apps Q2 2026 | Mar 2026 | C02, C07, C12 | https://genai.owasp.org/resource/al-security-solutions-landscape-for-llm-and-gen-al-apps-q2-2026/ |
| OWASP AI Security Solutions Landscape for Agentic AI Q2 2026 | Mar 2026 | All | https://genai.owasp.org/resource/ai-security-solutions-landscape-for-agentic-ai-q2-2026/ |
| OWASP AI Security Solutions Landscape for AI and Agentic Red Teaming Q2 2026 | Apr 2026 | C07, C11, C12 | https://genai.owasp.org/resource/ai-security-solutions-landscape-for-ai-and-agentic-red-teaming-q2-2026/ |
| OWASP GenAI Exploit Round-up Report Q1 2026 | Apr 2026 | C02, C06, C09, C10, C12 | https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/ |
| OWASP FinBot Agentic AI CTF | Apr 2026 | C09, C10, C11 | https://genai.owasp.org/2026/04/28/finbot-ctf-is-live-a-hands-on-companion-to-the-owasp-genai-security-project/ |
| OWASP State of Agentic AI Security and Governance 2.01 (landscape report on securing and governing autonomous AI systems: security frameworks, governance models, global regulatory mapping) | Jun 2026 | C09, C05 | https://genai.owasp.org/resource/state-of-agentic-ai-security-and-governance/ |
| OWASP AI Maturity Assessment (AIMA) — five-domain maturity model (Strategy, Design, Implementation, Operations, Governance); v1.0 Aug 2025, v1.1 refinements targeted Spring 2026 | Aug 2025 | C03, C12, C09 | https://owasp.org/www-project-ai-maturity-assessment/ |
| LLM Prompt Injection Prevention Cheat Sheet | — | C2 | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html |
| AI Agent Security Cheat Sheet | — | C9, C10 | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html |

#### OWASP LLM Top 10 Individual Entries (missing — only parent project page is in Appendix B)

| Reference | Cited In | Link |
|-----------|----------|------|
| LLM01:2025 Prompt Injection | C2 | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| LLM02:2025 Sensitive Information Disclosure | C8, C11, C07 | https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/ |
| LLM03:2025 Supply Chain | C6 | https://genai.owasp.org/llmrisk/llm032025-supply-chain/ |
| LLM04:2025 Data and Model Poisoning | C8, C11 | https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/ |
| LLM05:2025 Improper Output Handling | C7 | https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ |
| LLM06:2025 Excessive Agency | C7, C9 | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ |
| LLM07:2025 System Prompt Leakage | C2, C8, C07 | https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/ |
| LLM08:2025 Vector and Embedding Weaknesses | C8 | https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ |
| LLM09:2025 Misinformation | C7, C11, C09 | https://genai.owasp.org/llmrisk/llm092025-misinformation/ |
| LLM10:2025 Unbounded Consumption | C9, C11 | https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ |

#### CoSAI Publications (missing — new organization, not in Appendix B)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| CoSAI Principles for Secure-by-Design Agentic Systems | Jul 2025 | C09, C05 | https://www.coalitionforsecureai.org/announcing-the-cosai-principles-for-secure-by-design-agentic-systems/ |
| CoSAI MCP Security Taxonomy (12 threats, ~40 distinct attack patterns) | Jan 2026 | C10, C09 | https://www.coalitionforsecureai.org/coalition-for-secure-ai-releases-extensive-taxonomy-for-model-context-protocol-security/ |
| CoSAI AI Model Signing Framework | Nov 2025 | C06, C03 | https://www.coalitionforsecureai.org/building-trust-in-ai-supply-chains-why-model-signing-is-critical-for-enterprise-security/ |
| CoSAI AI Incident Response Framework v1.0 | Nov 2025 | C12, C04 | https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/ |

#### EU AI Act Implementing Guidance (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| EU Code of Practice for General-Purpose AI (GPAI) — Final Version | Jul 2025 | C07, C01 | https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai |
| EU Code of Practice on Transparency of AI-Generated Content | Dec 2025 | C07 | https://artificialintelligenceact.eu/introduction-to-code-of-practice/ |
| EC Guidelines for Providers of General-Purpose AI Models | 2025 | C07, C03 | https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers |
| EU Digital AI Omnibus — Provisional Council/Parliament Agreement (Omnibus VII) | May 2026 | C07, C01 | https://www.whitecase.com/insight-alert/eu-agrees-digital-omnibus-deal-simplify-ai-rules |
| European Parliament Legislative Train: Digital Omnibus on AI (tracks plenary vote, Council adoption, and Official Journal publication status) | 2026 | C07 | https://www.europarl.europa.eu/legislative-train/package-digital-package/file-digital-omnibus-on-ai |
| European Parliament plenary adoption of the Digital Omnibus on AI (16 Jun 2026, 423 in favour / 57 against / 174 abstentions; confirms high-risk deferral to 2 Dec 2027 stand-alone and 2 Aug 2028 embedded, adds the non-consensual-imagery/CSAM prohibition; only Council formal adoption remains) | Jun 2026 | C07, C01 | https://www.matheson.com/insights/eu-parliament-approves-amendments-to-the-ai-act/ |
| EU AI Act Article 55: Obligations for Providers of GPAI with Systemic Risk | 2024 | C07, C03, C09 | https://artificialintelligenceact.eu/article/55/ |

#### MCP Specification Updates (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| MCP Authorization Specification (2025-06-18) | Jun 2025 | C10 | https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization |
| MCP Specification 2025-11-25 Revision | Nov 2025 | C10 | https://modelcontextprotocol.io/specification/2025-11-25/changelog |
| MCP Draft Authorization Spec (client-credentials, enterprise IdP) | Draft 2026 | C10, C05 | https://modelcontextprotocol.io/specification/draft/basic/authorization |
| MCP Draft Specification Changelog (post-2025-11-25) | Draft 2026 | C10 | https://modelcontextprotocol.io/specification/draft/changelog |
| The 2026 MCP Roadmap (transport scalability, agent communication, governance maturation, enterprise readiness) | 2026 | C10, C09, C05 | https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/ |
| MCP 2026-07-28 Specification Release Candidate (locked 21 May 2026; stateless core removes initialization handshake and `Mcp-Session-Id`, Tasks and MCP Apps extensions, OAuth/OIDC-aligned authorization, formal deprecation policy; final spec scheduled 28 Jul 2026) | May 2026 | C10, C09, C05 | https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ |

#### Key RFCs Mandated by MCP (missing)

| Reference | Date | Cited In | Link |
|-----------|------|----------|------|
| OAuth 2.1 Authorization Framework draft-15 | Mar 2026 | C05, C10 | https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-15 |
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
| MITRE ATLAS Secure AI expansion and release-cadence update | C09, C11, C12 | https://ctid.mitre.org/blog/2026/05/06/secure-ai-v2-release/ |

#### Vendor Documentation (missing)

| Reference | Cited In | Link |
|-----------|----------|------|
| Mitigate jailbreaks and prompt injections (Anthropic) | C2 | https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks |
| Reinforcement fine-tuning (OpenAI) | C3 | https://platform.openai.com/docs/guides/reinforcement-fine-tuning |
| AI adversarial robustness (IBM Research) | C3 | https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness |
| OpenAI Privacy Center: Data Deletion Controls | C1 | https://privacy.openai.com/policies?modal=take-control |
| SBOM Overview (CISA) | C6 | https://www.cisa.gov/sbom |

---

### References in Appendix B Not Cited by Any Chapter (C1–C12)

| Reference | Category | Notes |
|-----------|----------|-------|
| NIST SP 800-218A: Secure Software Dev for GenAI | Standards | Cited in Appendix C and D only; consider pairing with NIST AI 800-3 for evaluation evidence and uncertainty reporting |
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
| NIST AI RMF 1.0 | `nist.gov/itl/ai-risk-management-framework` (C1, C4, C11), `nist.gov/system/files/documents/...` (C12), `doi.org/10.6028/NIST.AI.100-1` (C12), `nvlpubs.nist.gov/...` (Appendix B) | Standardize on `nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf` |
| NIST SP 800-207 | `csrc.nist.gov/pubs/sp/800/207/final` (C5) vs `csrc.nist.gov/pubs/detail/sp/800-207/final` (C9, C10) | Standardize on `/pubs/sp/` form |
| MITRE ATLAS AML.T0024.001 | "Invert AI Model" (C8) vs "Invert ML Model" (C11) | Use consistent title "Invert ML Model" (ATLAS canonical) |
| ISO/IEC 42001 | Appendix B source previously used `iso.org/standard/81230.html`; current source now uses `iso.org/standard/42001` | Keep the corrected short ISO URL and avoid reintroducing the stale numeric page |
| OAuth 2.1 | `draft-ietf-oauth-v2-1-11` in Appendix B source vs `draft-ietf-oauth-v2-1-15` (current as of March 2026) | Update to latest draft number |
| MCP Specification | `modelcontextprotocol.io` (Appendix B) — needs versioned links to authorization spec, November 2025 revision, and draft changelog | Add versioned spec links and keep draft-only items clearly marked as unstable |
| NIST Digital Identity Guidelines | Several chapter references still point to SP 800-63-3-era identity guidance | Prefer SP 800-63-4 final and cite the A/B/C companion volumes where proofing, authentication, or federation details matter |

---

## Structural Issues

1. **Decision needed: granular MITRE ATLAS links** — 10 specific ATLAS technique/mitigation pages are cited across chapters. **Recommendation: list them individually** since they are primary threat references for specific requirements, not just background context.

2. **Decision needed: OWASP LLM Top 10 entries** — 8 individual risk entries are cited. **Recommendation: list them individually** since each maps to specific chapters and requirements.

3. **OAuth 2.1 draft number is stale** — Appendix B source cites `draft-ietf-oauth-v2-1-11` but current is `draft-ietf-oauth-v2-1-15` (March 2026). Should be updated before the draft becomes an RFC.

4. **New category needed: "AI Agent and Agentic Frameworks"** — CoSAI, OWASP Agentic Security Initiative, NIST CAISI, and the OWASP Top 10 for Agentic Applications form a distinct category not well served by current Appendix B structure.

5. **New category needed: "MCP-Specific References"** — MCP specification versions, authorization spec, OWASP MCP Top 10, OWASP Guide for Secure MCP Server Development, CoSAI MCP taxonomy, and mandated RFCs warrant their own section given MCP has its own dedicated chapter (C10).

6. **NIST AI 800-3 and AI 800-4 cross-references needed** — NIST AI 800-3 (February 2026) is directly relevant to evaluation evidence because it distinguishes benchmark accuracy from generalized accuracy and recommends explicit uncertainty modeling. NIST AI 800-4 (March 2026) is directly relevant to C12 (Monitoring and Logging) and C09 (Human Oversight) because it documents post-deployment monitoring challenges from workshops and literature review. These should be referenced together where AISVS asks for evaluation, monitoring, or model-performance evidence.

7. **OWASP GenAI project publication velocity** — The OWASP GenAI Security Project published at least eleven high-value resources between December 2025 and April 2026 (AIBOM generator, MCP server security guide, MCP third-party server cheat sheet, red teaming vendor evaluation criteria, data security risks guide, three Q2 2026 solution landscapes, the GenAI Red Teaming Guide, the Q1 2026 exploit round-up, and the FinBot Agentic AI CTF launch). Appendix B should consider a dedicated "OWASP GenAI Security Project Resources" sub-section.

8. **EU GPAI Code of Practice now final** — The Code of Practice for general-purpose AI was finalized in July 2025 and the Commission now maintains the official code and signatory page at https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai. The complementary GPAI provider guidelines explain the obligations that entered into application on August 2, 2025; Commission enforcement powers begin August 2, 2026.

9. **MITRE ATLAS v5.4.0 and May 2026 Secure AI expansion** — The framework now covers 16 tactics and 84+ techniques after the October 2025 and February 2026 updates added agentic AI attack techniques including AI Agent Clickbait (AML.T0100), Publish Poisoned AI Agent Tool, and Escape to Host. The OpenClaw investigation (February 2026) demonstrated real-world exploit paths in AI-first ecosystems. The May 2026 Secure AI update adds a Technique Maturity filter, monthly release cadence, more rapid-response reporting, and a larger corpus of techniques, mitigations, and case studies. These should be cross-referenced in C09, C11, and C12.

10. **NIST NCCoE AI Agent Identity concept paper** — Published February 5, 2026, this concept paper outlines a potential NCCoE project applying identity standards (OAuth 2.0, SPIFFE) to AI agents. It covers identification, authorization, auditing, non-repudiation, and prompt injection mitigation for autonomous agents. Comment period closes April 2, 2026. Directly relevant to C05, C09, and C10.

11. **CSA launches and expands CSAI Foundation (March-April 2026)** — The Cloud Security Alliance launched CSAI as a dedicated 501(c)(3) for AI security, with the strategic mission of "Securing the Agentic Control Plane." Six programs cover visibility, best practices, education, governance, assurance, and research. In April 2026 CSA announced CNA authorization, the STAR for AI Catastrophic Risk Annex, and stewardship for AARM and the Agentic Trust Framework. Relevant to C09, C10, and C12.

12. **Exploit reporting now spans model, agent, and orchestration layers** — OWASP's Q1 2026 exploit round-up maps incidents such as OpenClaw, CustomMCP/Flowise, indirect prompt injection, and AI-assisted attack workflows to LLM and agentic risk categories. The Q1 report covers 1 January through 11 April 2026; as of June 2026 no Q2 round-up has been published, so the Q1 edition remains the current threat-intelligence baseline. Appendix B should treat quarterly exploit reports as threat-intelligence references for C02, C06, C09, C10, and C12 rather than as generic news.

13. **NIST SP 800-63-4 supersedes the older digital identity baseline** — The final July 2025 revision supersedes SP 800-63-3 and is more useful for AISVS access-control chapters because it splits identity proofing, authentication, and federation into companion volumes. C05, C09, and C10 should cite revision 4 where agent identity, federated authorization, or credential assurance is discussed.

14. **FinBot is now a practical verification reference, not just a project note** — OWASP's April 2026 FinBot launch provides a live, agentic CTF mapped to OWASP LLM Top 10, OWASP Agentic Top 10, CWE, and MITRE ATLAS. It is useful as a hands-on validation reference for prompt injection, MCP tool misuse, policy bypass, data exfiltration, privilege escalation, and remote code execution scenarios.

15. **MCP draft changes affect C10 implementation guidance** — The post-2025-11-25 draft changelog removes protocol-level sessions and the `Mcp-Session-Id` header from Streamable HTTP, adds capability extensions, and documents trace-context metadata conventions. As of 21 May 2026 these changes are locked into the 2026-07-28 release candidate (SEP-2567 removes the initialization handshake and protocol-level session header entirely; Tasks becomes an official extension with `tasks/get`, `tasks/update`, `tasks/cancel`; MCP Apps adds server-rendered UIs; a formal deprecation policy is introduced), with the final specification scheduled for 28 July 2026. This is the largest protocol revision since launch — remote MCP servers that previously needed sticky sessions can run behind plain round-robin load balancers. Appendix B should keep the RC separate from stable versioned MCP references so C10 can distinguish current stable guidance (2025-11-25) from the migration path.

16. **EU Digital AI Omnibus (May 7, 2026) shifts compliance dates** — The provisional Council/Parliament agreement reduces the grace period for transparency-watermarking implementation from six months to three (new deadline 2 December 2026), defers high-risk obligations to 2 December 2027 for stand-alone high-risk AI systems and 2 August 2028 for high-risk AI embedded in regulated products, and clarifies the AI Office's competence for supervising systems built on general-purpose AI models. Two new prohibitions on non-consensual intimate imagery and child sexual abuse material take effect 2 December 2026. On 16 June 2026 the European Parliament adopted the package in plenary (423 in favour, 57 against, 174 abstentions), so the deal is no longer provisional on the Parliament side; only formal Council adoption and Official Journal publication remain, both targeted before 2 August 2026 when the original high-risk rules would otherwise apply. C07 should track these revised dates rather than the original Article 113 timeline; this also affects how C01 documents lawful-basis and provenance requirements.

17. **NIST AI 800-1 and AI 800-2 form a complete evaluation pipeline with 800-3 and 800-4** — NIST AI 800-1 (second public draft, January 2025) covers misuse risk management for dual-use foundation models including chemical, biological, and cyber misuse appendices; NIST AI 800-2 (draft, January 30, 2026) sets best practices for automated benchmark evaluations of language models and AI agent systems; AI 800-3 (February 2026) supplies a statistical model for distinguishing benchmark accuracy from generalized accuracy; AI 800-4 (March 2026) documents post-deployment monitoring challenges. Together these four publications should be cited as a series wherever AISVS requires evaluation evidence, threat modeling for misuse, or post-deployment monitoring (primarily C03, C07, C11, C12, C09).

18. **OWASP LLM Top 10 (2025) requires LLM07 and LLM09 callouts** — Earlier Appendix B reviews omitted the two newest entries: LLM07 System Prompt Leakage (relevant to C02 prompt-injection, C08 data flows, and C07 transparency) and LLM09 Misinformation (relevant to C07 output handling, C11 robustness, and C09 governance). Both entries map to mature MITRE ATLAS techniques and existing OWASP cheat sheets, so their absence has produced gaps in chapter-to-Top-10 cross-references.

19. **CSAI Foundation's six-program mission is the canonical anchor for agentic governance references** — The csai.foundation 2026 mission page enumerates AI Risk Observatory, Agentic Best Practices, Education/Credentialing, CxOtrust for Agentic AI, Global Assurance & Trust, and Future Forward Initiatives. Appendix B should treat this page as a stable anchor for the agentic-control-plane program rather than relying on press releases alone; updates such as the May 2026 expansion of risk and vulnerability work fold naturally under the existing program structure.

20. **NIST AI 100-2 E2025 supersedes the 2023 adversarial-ML taxonomy** — The March 2025 final revision of NIST AI 100-2 (published as `NIST.AI.100-2e2025`) replaces the older E2023 edition and is the canonical taxonomy reference for C11 going forward. It expands GenAI coverage (prompt injection, misuse), introduces the first NIST treatment of autonomous-agent vulnerabilities, and adds reference architectures for securing enterprise GenAI integrations and supply chains. Appendix B should cite both editions until the rest of AISVS migrates references to E2025; chapter requirements that lean on the older taxonomy text need to be re-checked against the E2025 categorisation (PredAI: evasion/poisoning/privacy; GenAI: evasion/poisoning/privacy/misuse).

21. **"AI Vulnerability Storm" / Mythos-ready briefing is now a primary CISO reference** — The April 2026 joint paper from SANS, CSA, [un]prompted, and the OWASP GenAI Security Project — *The AI Vulnerability Storm: Building a Mythos-Ready Security Program* — was assembled by 60+ named contributors (including Jen Easterly, Bruce Schneier, Chris Inglis, Phil Venables, Heather Adkins, Rob Joyce, Sounil Yu) and reviewed by 250+ CISOs. It introduces the Zero Day Clock framing for mean-time-to-exploit and provides a 13-item risk register mapped to OWASP LLM Top 10 2025, OWASP Agentic Top 10 2026, MITRE ATLAS, and NIST CSF 2.0, an 11-item priority actions table, a 10-question CISO diagnostic, and a board-briefing template. It belongs in C04 (governance/security architecture), C11 (adversarial robustness), C12 (monitoring/IR), and C09 (oversight) and is currently the cleanest single artifact for cross-mapping AISVS to all four reference frameworks.

22. **CSA AICM v1.0.3 plus the Catastrophic Risk Annex are now the active controls baseline** — The AICM has moved to v1.0.3, which keeps it aligned with CCM v4.0.13 and on a synchronisation path with CCM v4.1 expected during 2026. The April 2026 *Catastrophic Risk Annex* extends AICM and the broader STAR-for-AI assurance program to cover catastrophic-risk scenarios, with rollout beginning in late Q2 2026. AISVS should cite the v1.0.3 release (rather than the original v1 announcement) when describing CSA-aligned controls and should treat the Catastrophic Risk Annex as the canonical reference for catastrophic-risk evidence in C04, C12, and C09.

23. **NIST AI cybersecurity guidance is on a phased summer-2026 release schedule** — NIST has publicly signalled that the AI cybersecurity framework profile, predictive-AI control overlay draft, and agentic-AI control overlay draft will land in three steps during 2026 (profile and predictive overlay in summer 2026; agentic overlay in late summer/early fall 2026; full finalization targeted for 2027), with overlays explicitly tied to COSAiS. Appendix B should record the public schedule alongside the IR 8596 and COSAiS entries so chapter references can distinguish "final" guidance from drafts and call out when chapter language depends on an unreleased overlay.

24. **CAISI is now actively evaluating frontier models pre-release** — The 5 May 2026 CAISI announcement added pre-deployment testing agreements with Google DeepMind, Microsoft, and xAI to existing arrangements with OpenAI and Anthropic, bringing the program to five major labs. CAISI has completed more than 40 evaluations — including unreleased models — covering cybersecurity, biosecurity, and chemical-weapons risk, with some conducted in classified environments by the interagency TRAINS Taskforce, in addition to the published DeepSeek V4 Pro evaluation. Appendix B should treat the CAISI program as an ongoing source of evaluation evidence for C03 (lifecycle), C07 (output safety), C11 (robustness), and C09 (oversight), and chapter authors should expect CAISI publications to land at irregular cadence rather than on a fixed release schedule.

25. **Five Eyes agencies issued their first joint agentic-AI security guidance** — On 30 April 2026, CISA, NSA, Australia's ASD ACSC, the Canadian Centre for Cyber Security, the UK NCSC, and New Zealand's NCSC jointly published *Careful Adoption of Agentic AI Services*. The guide defines five agentic risk categories (privilege escalation, design and configuration flaws, behavioral misalignment, structural cascading failures, accountability opacity) and argues that agentic AI should be folded into existing zero-trust, defense-in-depth, and least-privilege frameworks rather than treated as a new security discipline. It recommends starting with low-risk, non-sensitive use cases and avoiding broad access grants. This is the first government-consensus reference for C09 execution-budget and approval controls, C04 security architecture, and C09 oversight, and it complements the NIST CAISI agent work and CSA agentic-control-plane program.

26. **CSAI RiskRubric V2 extends model-risk scoring to autonomous control loops** — Announced 8 June 2026 and launching in Q3 2026 with Deloitte Italy, PointGuardAI, and Tumeryk as partners, RiskRubric V2 is a systematic methodology to quantify AI model risk that aims to measure "the true boundary of modern AI systems, from models to autonomous control loops" while preserving reproducibility and transparency. Combined with OWASP's *State of Agentic AI Security and Governance 2.01* (1 June 2026), which maps security frameworks, governance models, and global regulatory standards for autonomous systems, June 2026 produced two complementary agentic-governance references: RiskRubric for quantitative model/agent risk scoring (C03, C07, C11) and the OWASP report for program-level governance (C09, C05).

---

## Recommended Appendix B Structure

Based on the audit, Appendix B should be restructured to cover the full reference landscape:

| Category | Current Count | Missing | Recommended Total |
|----------|:------------:|:-------:|:-----------------:|
| Standards and Frameworks | 7 | 39 (incl. NIST AI 100-2 E2025 final, AI 800-1 IPD2, AI 800-2, AI 800-3/800-4, SP 800-63-4, CAISI RFI and frontier-model program, COSAiS overlay roadmap, NCCoE AI Agent Identity, CSA CSAI six-program mission, AICM v1.0.3, STAR-for-AI Catastrophic Risk Annex, RiskRubric V2, ISO/IEC FDIS 27090, ISO/IEC DIS 27091, Five Eyes Careful Adoption of Agentic AI Services, CSA ATT&CK/ATLAS agentic gap analysis) | ~46 |
| Specifications and Protocols | 5 | 12 (MCP spec versions, draft auth/changelog, MCP 2026 Roadmap, 2026-07-28 release candidate, OAuth 2.1 draft-15 + RFCs) | ~17 |
| OWASP Publications | 3 | 27 (full LLM Top 10 2025 entries including LLM07 and LLM09, agentic, MCP guides, AIBOM, red teaming, data security, landscapes, exploit reporting, FinBot, State of Agentic AI Security and Governance 2.01, AI Maturity Assessment, AI Vulnerability Storm joint paper) | ~30 |
| MITRE ATLAS | 1 (main site) | 13 (individual techniques plus OpenClaw and Secure AI update) | ~14 |
| CoSAI | 0 | 4 | 4 |
| EU AI Act & Implementing Guidance | 1 | 7 (codes of practice, GPAI guidelines, Article 55, Digital AI Omnibus May 2026, Parliament legislative-train tracker, 16 Jun 2026 plenary adoption) | 8 |
| Privacy and Data Protection | 3 | 0 | 3 |
| Cryptographic Standards | 2 | 0 | 2 |
| Policy Engines | 2 | 0 | 2 |
| Vendor Documentation | 0 | 5 | 5 |
| **Total** | **18** | **~112** | **~135** |

---

## Related Pages

- [C11: Adversarial Robustness](../chapters/C11-Adversarial-Robustness/C11-Adversarial-Robustness.md) — Tracks the MITRE ATLAS, red-team tooling, and robustness references most likely to need Appendix B coverage.
- [Appendix A: Glossary](Appendix-A-Glossary.md) — Useful companion when reference additions introduce new terminology around ATLAS, MCP, NIST, EU AI Act, A2A, and agent-security concepts.
- [Appendix D: Controls Inventory](Appendix-D-Controls-Inventory.md) — Helps connect Appendix B source coverage to external frameworks, control families, platform tooling, and adoption gaps.
- [C03-04: Secure Development Practices](../chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md) — Shows where secure build, MCP scanner, package quarantine, and AI configuration references should support lifecycle controls.
- [C11-10: Adversarial Bias Exploitation Defense](../chapters/C11-Adversarial-Robustness/C11-01-Model-Alignment-Safety.md) — Links bias, classifier evasion, guardrail testing, and red-team references back to adversarial robustness evidence.

---

## Community Notes

_Discussion about reference scope, URL standardization, and completeness._

---

[README](../README.md)
