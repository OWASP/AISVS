# 1.01 Research Review Status

This checklist tracks [#1109](https://github.com/OWASP/AISVS/issues/1109). It is a review record, not an extension of AISVS requirements or a release announcement.

## Current position

- Requirement-text and level synchronization has been checked for all 213 active core requirements and all 69 Appendix C requirements, and rechecked after the source audit: no requirement text, ID, or level quoted in the research pages differs from `1.01-dev/en`.
- The source audit of all research documents was completed on 2026-09-30. About 4,900 factual claims were checked against original sources; roughly 70% matched as written, and the rest were corrected, qualified, re-sourced, or removed. Each area's changes were re-verified in a separate review pass, which also spot-checked about 400 unchanged claims. Counts are approximate tallies, not a per-claim ledger.
- Appendix B retains 41 statistics rows, all source-checked; none are pending. Seven held entries below cover former rows and associated prose that are not presented as established findings.
- OWASP Top 10 for LLM Applications citations now use the 2026 edition adopted by the standard, and EU AI Act dates reflect the Digital Omnibus on AI (Regulation (EU) 2026/1744, in force 27 July 2026).
- Known limitations are listed below. Otto owns the formal release, including final metadata, dates, and artifacts.

## Completion criteria

For each retained factual claim, check the original source, publication date, population or test scope, and whether the wording follows the evidence. Distinguish forecasts, vendor claims, observed incidents, and controlled experiments. Correct or remove unsupported assertions; record unresolved source conflicts. Then check consistency with the normative standard, links, counts, and document checks.

General application security, infrastructure hardening, and organizational governance remain complementary frameworks' concerns; research corrections do not add AISVS requirements or change levels. Technical source review does not require reproducing exploits.

A checked statistic means its stated measure was matched to the publisher's material. It is not independent validation of the underlying study, an endorsement, or a completed review of every claim elsewhere citing that source.

## Completed consistency work

- [x] Core requirement text and levels aligned with research, including agent state isolation, MCP updates, and adversarial evaluation changes: [#1170](https://github.com/OWASP/AISVS/pull/1170), [#1171](https://github.com/OWASP/AISVS/pull/1171), [#1172](https://github.com/OWASP/AISVS/pull/1172).
- [x] Appendix C requirements and ASVS references synchronized: [#1168](https://github.com/OWASP/AISVS/pull/1168), [#1169](https://github.com/OWASP/AISVS/pull/1169).
- [x] Appendix B mappings and 19 family counts aligned to 213 active requirements: [#1173](https://github.com/OWASP/AISVS/pull/1173).
- [x] First Appendix B source corrections merged: [#1175](https://github.com/OWASP/AISVS/pull/1175), [#1176](https://github.com/OWASP/AISVS/pull/1176), [#1177](https://github.com/OWASP/AISVS/pull/1177), [#1178](https://github.com/OWASP/AISVS/pull/1178), [#1179](https://github.com/OWASP/AISVS/pull/1179).
- [x] Evidence checklist established; unsupported adoption claims held for further research: [#1180](https://github.com/OWASP/AISVS/pull/1180).
- [x] Full source audit of chapter and appendix research, pending Appendix B statistics resolved, LLM Top 10 2026 and EU AI Act timeline consistency, and README anchor fixes (September 30, 2026).

## Source audit by area

The inventory covers the 60 research documents that existed before this checklist: 56 chapter documents, three appendices, and the README. Each chapter group includes its hub and section pages. Claim counts are approximate.

| Area | Documents | Claims checked | Status |
| --- | ---: | ---: | --- |
| [C1 Training Data](chapters/C01-Training-Data/) | 4 | 150 | Audited |
| [C2 Input Validation](chapters/C02-User-Input-Validation/) | 3 | 344 | Audited |
| [C3 Model Lifecycle](chapters/C03-Model-Lifecycle-Management/) | 6 | 328 | Audited |
| [C4 Infrastructure](chapters/C04-Infrastructure/) | 4 | 296 | Audited |
| [C5 Access Control](chapters/C05-Access-Control/) | 4 | 246 | Audited |
| [C6 Supply Chain](chapters/C06-Supply-Chain/) | 3 | 185 | Audited |
| [C7 Model Behavior](chapters/C07-Model-Behavior/) | 5 | 455 | Audited |
| [C8 Memory and Embeddings](chapters/C08-Memory-and-Embeddings/) | 4 | 165 | Audited |
| [C9 Orchestration and Agents](chapters/C09-Orchestration-and-Agents/) | 7 | 1,044 | Audited |
| [C10 MCP Security](chapters/C10-MCP-Security/) | 5 | 413 | Audited |
| [C11 Adversarial Robustness](chapters/C11-Adversarial-Robustness/) | 5 | 382 | Audited |
| [C12 Monitoring and Logging](chapters/C12-Monitoring-and-Logging/) | 6 | 488 | Audited |
| [Appendix A](appendices/Appendix-A-Glossary.md) | 1 | Counted with B | Audited; term table completed to 158 rows |
| [Appendix B](appendices/Appendix-B-Controls-Inventory.md) | 1 | 314 with A | Audited; 14 pending statistics resolved |
| [Appendix C](appendices/Appendix-C-AI-Secure-Coding.md) | 1 | 92 | Audited |
| [README](README.md) | 1 | — | Navigation, counts, and anchors checked |

### Appendix B statistics

This is the complete row inventory for the current adoption snapshot. Update the count above and this table when a row changes or is checked. A checked or corrected row matches the publisher's material; it is not independent validation of the study.

| Metric and reported value | State | Evidence or next step |
| --- | --- | --- |
| Tech execs rating autonomous AI as high/essential priority (97%) | Checked | Publisher's tech-sector survey; February 2026 fieldwork, March 2026 publication. |
| Surveyed orgs reporting implementation of specific GenAI security controls (47%) | Checked | February 2026 publication; 1,725 data security leaders surveyed July-August 2025. Self-reported implementation, not verified control effectiveness. |
| Surveyed orgs enforcing AI security inline, at point of action (23%) | Checked | Publisher's 2026 survey summary; distinct deployment, inline enforcement, and governance measures. |
| Surveyed orgs with comprehensive AI security governance policies (26%) | Checked | Publisher's December 2025 survey summary; 26% policy coverage. |
| Surveyed orgs with an advanced AI security strategy (6.4%) | Checked | Publisher's 2025 report landing page gives 6.4%; formerly attributed to Gartner. |
| Surveyed orgs with full security approval for their entire AI-agent fleet (14.4%) | Checked | Publisher's 2026 survey summary; fleet shares and suspected incidents preserved. |
| Surveyed orgs with real-time governance enforcement (7%) | Checked | Publisher's 2026 survey summary; distinct deployment, inline enforcement, and governance measures. |
| Dept-level AI initiatives without formal oversight (52%) | Checked | Publisher's tech-sector survey; February 2026 fieldwork, March 2026 publication. |
| Average share of AI agents actively monitored or secured within surveyed orgs (47.1%) | Checked | Publisher's 2026 survey summary; fleet shares and suspected incidents preserved. |
| Surveyed orgs reporting confirmed or suspected AI-agent security incidents in the past year (88%) | Checked | Publisher's 2026 survey summary; fleet shares and suspected incidents preserved. |
| Confirmed/suspected sensitive data leak via unauthorized GenAI (45%) | Checked | Publisher's tech-sector survey; February 2026 fieldwork, March 2026 publication. |
| Confirmed/suspected proprietary IP leak via unauthorized GenAI (39%) | Checked | Publisher's tech-sector survey; February 2026 fieldwork, March 2026 publication. |
| Reader-poll respondents expecting agentic AI to be the top attack vector by end-2026 (48%) | Checked | Publisher's January 2026 reader poll offered four predictions. Not observed attacks or a representative professional survey. |
| OWASP Top 10 for Agentic Applications (ASI) categories that the report maps prompt injection to (6 of 10) | Checked | Report PDF v2.01 (June 2026), p. 24: "maps to six of the ten ASI categories"; the publisher's resource page dates it June 1, 2026. The mapping is the authors' classification, not an incident count. |
| Studied breached orgs with governance policies to manage AI or detect shadow AI (37%) | Checked | IBM 2025 breached-organization sample; original report Figures 28 and 31. |
| Year-over-year growth in enterprise AI/ML traffic (83%) | Checked | Publisher's 2026 report summary; traffic growth, not organization prevalence. |
| Unique AI/ML applications observed in enterprise traffic (3,400+) | Checked | Publisher's 2026 report summary; traffic growth, not organization prevalence. |
| Studied orgs with employees using unsanctioned apps, including shadow AI (not AI-only) (98%) | Checked | Original 2025 report, pp. 2-5; 1,000 organizations; apps generally, not AI-only. |
| Avg cost of studied breaches involving unsanctioned or shadow AI (USD 4.63M) | Checked | IBM 2025 breached-organization sample; original report Figures 28 and 31. |
| Surveyed orgs reporting control of agent actions with guardrails and live monitoring (24%) | Checked | Original 2025 report, pp. 24, 26; 8,039 senior leaders in organizations with 500+ employees; August 2025 survey. |
| Machine-to-human identity ratio in a 2022 survey of 1,750 IT security decision makers (~45:1) | Corrected | Original is CyberArk's April 12, 2022 press release ("45x on average"; Vanson Bourne survey). The "NHI Forum / industry aggregate (2026)" attribution and "modern enterprises" framing were replaced; later vendor pieces (Rubrik Zero Labs blog, One Identity columns) repeat 45:1 without new measurement. |
| NHI-to-human ratio across enterprise environments analyzed by Entro Labs (144:1) | Corrected | Entro Labs NHI & Secrets Risk Report H1 2025 (July 22, 2025) states 144 to 1 across the enterprise environments it analyzed (more than 27 million NHIs); the summary gives 44% year-over-year NHI growth and a 56% rise in the ratio. The "cloud-native / DevOps" qualifier came from a May 2026 One Identity column, not the publisher, and was removed. |
| Analyzed applications not routing authentication through a central identity provider (57%) | Checked | Original report, finding 3; April 2025-March 2026 application telemetry. The denominator is applications, not identities; no AI-only prevalence measure. |
| KEVs disclosed in Q1 2025 with exploitation evidence within one day of CVE publication (28.3%) | Corrected | VulnCheck, April 24, 2025: 28.3% of the 159 KEVs added in Q1 2025. Not a Mandiant figure; M-Trends 2026 (March 23, 2026) reports a mean time-to-exploit of about -7 days and exploits as 32% of initial infection vectors. |
| Internet-accessible MCP services whose tools Censys enumerated without authentication (12,520) | Corrected | Censys report (May 27, 2026; data as of April 28, 2026): 12,520 services on 8,758 IPs, enumerated without authentication; the dataset passed 21,000 by May 6. Attributed directly instead of through the Adversa AI roundup. |
| Live remote MCP servers exposing tools without authentication (40.55%) | Corrected | Zhou et al., arXiv 2605.22333 (May 21, 2026): 40.55% of 7,973 live remote servers; nine CVE IDs obtained through disclosure. The rounded "~40%" and roundup attribution were replaced. |
| Internet-exposed MCP servers in Trend Micro's follow-up scan (1,467) | Corrected | Trend Micro, April 28, 2026: 1,467 exposed servers, up from 492 in July 2025. The CVSS 9.8 command-injection flaws (CVE-2026-5058 and CVE-2026-5059 in aws-mcp-server; ZDI-CAN-28042) are separate disclosures, so the former "servers carrying CVSS 9.8 vulnerabilities" wording was wrong. |
| MCP CVEs assigned via one automated taint-analysis study (VIPER-MCP) (67) | Checked | arXiv 2605.21392 (v1 May 20, 2026): 39,884 repositories, 106 zero-days, 67 CVE IDs assigned at publication. |
| Audited LLM API providers with global cross-user prompt-cache sharing detected (7 of 8 with caching) | Corrected | Gu et al. (Stanford), arXiv 2502.07776 v2 (July 2025): 17 providers audited, caching detected in 8, global sharing in 7; at least five providers mitigated after the October 2024 disclosure. Denominators and post-disclosure status added. |
| Poisoned pretraining documents sufficient for a narrow denial-of-service backdoor across the 600M–13B models tested (~250) | Corrected | Anthropic / UK AISI / Alan Turing Institute, October 9, 2025: 600M, 2B, 7B, and 13B models; gibberish-output trigger. "Regardless of model size" was replaced with the tested range and backdoor type. |
| Surveyed orgs reporting advanced API security maturity (not an AI maturity score) (8%) | Checked | Publisher's April 2026 announcement; 327 security professionals surveyed in early 2026. Direct API measure replaces a 92% complement mislabeled AI maturity. |
| Surveyed orgs unable to monitor non-human traffic, according to the publisher's summary (48.9%) | Checked | Publisher's April 2026 survey summary; no independent observation of every organization's traffic. |
| Surveyed orgs unable to effectively distinguish legitimate AI agents from malicious bots (48.3%) | Checked | Publisher's April 2026 survey summary; self-reported capability. |
| Attack attempts analyzed by Salt Labs originating from authenticated sources (not an AI-agent share) (99%) | Checked | Publisher's April 2026 announcement; separate telemetry, not the 327-person survey. Does not quantify attacks attributable to agents. |
| Surveyed security leaders reporting increased executive scrutiny of AI security risks (78.6%) | Checked | Publisher's April 2026 survey summary; reported scrutiny, not an incident rate. |
| Surveyed orgs that delayed production releases over API security concerns (47%) | Checked | Publisher's April 2026 announcement; percentage of surveyed organizations, not percentage of all releases. |
| Surveyed orgs without written agentic AI policies that had deployed agents anyway (79%) | Checked | EMA press release (December 2, 2025; 271 IT, security, and IAM respondents) states the conditional measure. EMA's research landing page summarizes the same figure as "79% lack written policies"; the full report is paywalled, so the press-release wording is kept and the summary conflict remains recorded. |
| Surveyed orgs continuously monitoring agent-to-agent (A2A) interactions (17%) | Checked | Publisher's 2025 survey; agent-to-agent monitoring. |
| Surveyed orgs with a tested AI-specific incident response plan (20%) | Checked | Publisher's 2026 survey; tested AI-specific incident response plans. |
| Survey respondents highly confident current IAM systems can manage agent identities effectively (18%) | Checked | CSA report landing page; February 2026 publication. [Survey announcement](https://www.strata.io/resources/news/new-survey-from-cloud-security-alliance-strata-identity-finds-that-enterprises-are-in-a-time-to-trust-phase/) describes 285 IT/security respondents, September-October 2025 fieldwork. |
| Analyzed non-human accounts established and managed locally, outside central IAM (67%) | Checked | Original report, finding 2; April 2025-March 2026 application telemetry. Includes non-human accounts generally, not just AI agents. |

### Held statistical claims

These claims have been removed from the adoption snapshot pending adequate evidence. “Held” does not mean proved false. Do not restore them solely because another aggregate repeats the same number.

| Former claim | Evidence reviewed and reason for holding | Needed to restore |
| --- | --- | --- |
| Production AI adoption 94%; mature security programs 23%; models without scanning 67%; prompt-attack vulnerability 89%; unvetted models 91%; maturity distribution 34/28/23/12/3% | The [CyberSecFeed article](https://docs.cybersecfeed.com/blog/ai-security-maturity-model-2025) contains these figures and describes analysis of 500+ implementations. A study instrument, sampling explanation, and tests supporting population or vulnerability estimates were not established in this review. Its maturity levels are not AISVS verification levels. | Traceable study methods, populations, and testing definitions; wording limited to that evidence. |
| Formal GenAI governance reduces data leakage by up to 46% | The [Practical DevSecOps article](https://www.practical-devsecops.com/ai-security-statistics-2026-research-report/) repeats this in an FAQ, but a supporting primary study for this causal comparison was not identified. | Original comparative study and methodology; do not substitute CSA's unrelated 46% adoption measure. |
| Production AI workload adoption 72%; mature adoption across functions 28% | The cited report title was not resolved to evidence for these measures. The publisher's [January 2026 risk report](https://www.cybersecurity-insiders.com/2026-ciso-ai-risk-report/) and [March 2026 readiness report](https://www.cybersecurity-insiders.com/ai-risk-and-readiness-report-2026/) report different measures. | Exact original report, question, sample, and date. |
| Organizations with a shadow-AI data exposure event: about 60% | The aggregate citation did not establish the original population, event definition, or study. The current [Second Talent page](https://www.secondtalent.com/resources/shadow-ai-statistics/) includes a different 60% measure about confidence in detection. | Primary evidence for exposure events, not tool use, concern, or detection confidence. |
| Organizations with no visibility into AI data flows: 86% | The cited chain leads through the [February 2026 briefing](https://www.aiuc-1.com/research/whitepaper-the-end-of-vibe-adoption) to a [June 2025 data-security report](https://www.kiteworks.com/sites/default/files/resources/kiteworks-report-ai-data-security-and-compliance.pdf), pp. 5, 15, which cites Stanford's AI Index. The original question, population, and 86% measure were not established; [later summaries](https://www.teramind.co/l/shadow-ai-report-2026/) also repeat it. | Exact primary study and measurement; repetition across summaries does not resolve the source chain. |
| NHIs older than one year without credential rotation: 47%; enterprises breached via a compromised NHI: about 67% | Both figures appear only in two May 2026 One Identity vendor columns ([The Hacker News](https://thehackernews.com/expert-insights/2026/05/the-non-human-identity-crisis-why-your.html), [Infosecurity Magazine](https://www.infosecurity-magazine.com/blogs/90-days-to-full-nhi-management/)) without attribution. The cited [DoControl 2026 NHI report](https://www.docontrol.io/blog/2026-non-human-identities-nhi-report) is SaaS event telemetry and contains neither figure. | Primary study with population, credential-age definition, and breach definition. |
| MCP-related CVEs filed in January-February 2026: 30+ | The source is a [personal blog post](https://www.heyuan110.com/posts/ai/2026-03-10-mcp-security-2026/) (March 2026) with no CVE list or counting method. An NVD keyword search for "MCP" returns 28 CVEs published in that window (6 for "Model Context Protocol"), which neither confirms nor refutes the count. | A tracked CVE list with IDs and inclusion criteria for that period, such as a dated Vulnerable MCP Project snapshot. |

## Known limitations

- "Checked" means a claim matched the publisher's own material: report, abstract, advisory, or CVE record. Vendor telemetry, self-reported surveys, and single-study results were not independently validated.
- Some publishers blocked automated retrieval, including ISO, NSA, OpenAI, Gartner, OpenReview, and several journal platforms. Claims that depend only on those sources remain attributed but unverified.
- Some claim classes were sampled rather than exhausted: vendor capability and release-date rows in tool tables, conference-venue attributions, figures that appear only in paper bodies, the C02-02 regulatory matrix, legal-sanction rows in C07-02, and standards-status rows in C04-03.
- Where publishers disagree, the conflict is recorded rather than resolved. Most cases are CVSS scores that differ between the CNA, NVD, and GitHub advisories, plus a few incident timelines.
- Statements dated "as of" April to June 2026, such as patch status, ATLAS technique counts, IETF draft versions, and MCP roadmap items, were not re-surveyed for September 2026.
- About 350 claims were recorded as unresolved during the audit. A follow-up review on 2026-10-01 checked each against primary sources: 112 were confirmed as written, 130 were corrected, and 48 had already been fixed in earlier passes. The 64 that remain are listed under [Unresolved claims](#unresolved-claims); their text is unchanged.

## Unresolved claims

These claims were left as written after the 2026-10-01 review because the primary source was blocked or gated, could not be found, only partly supported the claim, or conflicted with another primary source. They are candidates for post-1.01 review; do not treat them as checked.

| Page | Claim |
| --- | --- |
| [C01-01-Training-Data-Origin-Traceability](chapters/C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md) | WATERSHED: five schemes, two LLM families, three data domains |
| [C01-01-Training-Data-Origin-Traceability](chapters/C01-Training-Data/C01-01-Training-Data-Origin-Traceability.md) | CVE-2026-4372 affected range 4.56.0-5.2.x |
| [C01-02-Data-Labeling-Annotation-Security](chapters/C01-Training-Data/C01-02-Data-Labeling-Annotation-Security.md) | Scale AI customer pullback after Meta deal |
| [C01-Training-Data](chapters/C01-Training-Data/C01-Training-Data.md) | HF Sigstore 'in development'; JFrog partnership; JFrog and Palo Alto AIBOM generators |
| [C02-01-Prompt-Injection-Defense](chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) | Agent systems with auto-execution: 66.9-84.1% ASR (Cisco 2026) |
| [C02-01-Prompt-Injection-Defense](chapters/C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) | Body-text figures for ClawGuard, DefensiveTokens, DataSentinel, PromptArmor, LlamaFirewall, Meta-SecAlign, provenance framework, Nature PromptGuard, MASpi, TensorTrust, BIPIA, PromptGame |
| [C02-02-Content-Policy-Screening](chapters/C02-User-Input-Validation/C02-02-Content-Policy-Screening.md) | Vendor metrics: Luna-2 0.95 F1/98% vs GPT-4o; <200ms; LLM Guard 2.5M+; Pindrop 93–94%; Azure imageWithText preview Sep 2024 |
| [C02-User-Input-Validation](chapters/C02-User-Input-Validation/C02-User-Input-Validation.md) | NIST COSAiS five overlays, drafts summer 2026; OWASP State of Agentic AI v2.01 additions |
| [C03-01-Model-Authorization-Integrity](chapters/C03-Model-Lifecycle-Management/C03-01-Model-Authorization-Integrity.md) | NVIDIA has signed all NGC Catalog models with OMS since March 2025 (also C03-05) |
| [C03-03-Controlled-Deployment-Rollback](chapters/C03-Model-Lifecycle-Management/C03-03-Controlled-Deployment-Rollback.md) | SafeLoRA fusion 42% harmfulness reduction; PROMPTPEEK up to 99%; LMCache v0.4.4-0.4.6 per-request hit metrics; Triton May 2026 bulletin r26.03 |
| [C03-04-Secure-Development-Practices](chapters/C03-Model-Lifecycle-Management/C03-04-Secure-Development-Practices.md) | Trend Micro 492 unauthenticated MCP servers; AI Accelerator Institute 281 servers / 92%; Unit 42 Hydra RCE December 2025 |
| [C03-Model-Lifecycle-Management](chapters/C03-Model-Lifecycle-Management/C03-Model-Lifecycle-Management.md) | JFrog: 6.5x increase in malicious models in 2024 |
| [C04-02-Hardware-Security](chapters/C04-Infrastructure/C04-02-Hardware-Security.md) | Blackwell CC encrypts GPU-resident HBM |
| [C04-02-Hardware-Security](chapters/C04-Infrastructure/C04-02-Hardware-Security.md) | Confidential AI inference with CPU+GPU TEEs in production at Alibaba, ByteDance, Google, Oracle |
| [C04-02-Hardware-Security](chapters/C04-Infrastructure/C04-02-Hardware-Security.md) | Alpha Compute 504-chip B200 cluster CC hand-off May 8, 2026 |
| [C04-02-Hardware-Security](chapters/C04-Infrastructure/C04-02-Hardware-Security.md) | Red Hat OSC v1.10.0 GA confidential containers on Azure; RHEL day-zero Rubin support |
| [C04-02-Hardware-Security](chapters/C04-Infrastructure/C04-02-Hardware-Security.md) | GDDRHammer/GeForge 'tested and not reproduced on' RTX 3080, 4060/4060 Ti, RTX 6000 Ada, RTX 5050 |
| [C04-03-Edge-Distributed-Security](chapters/C04-Infrastructure/C04-03-Edge-Distributed-Security.md) | Over 12,000 internet-facing Flowise instances (April 2026) |
| [C04-Infrastructure](chapters/C04-Infrastructure/C04-Infrastructure.md) | 37% of cloud environments affected by NVIDIAScape (Wiz) |
| [C04-Infrastructure](chapters/C04-Infrastructure/C04-Infrastructure.md) | Intel Trust Authority composite CPU+GPU attestation (Mar 2026); NIST AI Agent Standards Initiative (Feb 2026) and Q4 2026 interoperability profile |
| [C05-01-Identity-Management-Authentication](chapters/C05-Access-Control/C05-01-Identity-Management-Authentication.md) | Codex payload hidden behind 94 ideographic spaces (U+3000) |
| [C05-03-Multi-Tenant-Isolation](chapters/C05-Access-Control/C05-03-Multi-Tenant-Isolation.md) | CVE-2026-25960 CVSS 5.4 |
| [C06-01-Model-Artifact-Integrity](chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md) | Pattern Recognition 2026 backdoor defense: 100% detection on 630 models, six attack types |
| [C06-01-Model-Artifact-Integrity](chapters/C06-Supply-Chain/C06-01-Model-Artifact-Integrity.md) | ClawHavoc delivered Atomic Stealer to ~300,000 users (line 265) |
| [C06-02-AI-BOM-Supply-Chain-Monitoring](chapters/C06-Supply-Chain/C06-02-AI-BOM-Supply-Chain-Monitoring.md) | OpenAI, Anthropic, Google all published AB 2013 training-data summaries by Jan 1, 2026 |
| [C06-Supply-Chain](chapters/C06-Supply-Chain/C06-Supply-Chain.md) | JFrog: 59% of serialized model files use pickle-based formats; JFrog 2025 report: 1M+ new HF models in 2024, 6.5x increase in malicious models (also C06-02) |
| [C06-Supply-Chain](chapters/C06-Supply-Chain/C06-Supply-Chain.md) | Ultralytics library with 60M+ (PyPI) downloads |
| [C06-Supply-Chain](chapters/C06-Supply-Chain/C06-Supply-Chain.md) | Shai-Hulud 2.0 compromised ~1,000 npm packages |
| [C07-02-Hallucination-Detection](chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md) | MIT (Jan 2025): models 34% more likely to use confident language when false |
| [C07-02-Hallucination-Detection](chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md) | 79% of lawyers use AI tools (ABA TechReport 2025) |
| [C07-02-Hallucination-Detection](chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md) | AA-Omniscience Gemini 3 Pro ~half accuracy / 88% halluc.; Grok 4 64%; Opus 4.6 46.4% |
| [C07-02-Hallucination-Detection](chapters/C07-Model-Behavior/C07-02-Hallucination-Detection.md) | May 18, 2026 Charlotin breakdown (1,005 US/451 non-US; 865 pro se/555 lawyers; Canada 152 etc.) |
| [C07-03-Output-Safety-Privacy-Explainability](chapters/C07-Model-Behavior/C07-03-Output-Safety-Privacy-Explainability.md) | Sockpuppeting (Dotsinski & Eustratiadis, 2026): 95% ASR on Qwen-8B, 77% on Llama-3.1-8B |
| [C07-04-Source-Attribution-Citation-Integrity](chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md) | Attention-Aware RAG poisoning defenses (OpenReview PS43wqCSME, NeurIPS 2025): NPAS/AV Filter, ~20% improvement, adaptive attacks ~35% |
| [C07-04-Source-Attribution-Citation-Integrity](chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md) | Lancet: 4,046 fabricated refs across 2,810 papers; >12x rise 2023 to early 2026 |
| [C07-04-Source-Attribution-Citation-Integrity](chapters/C07-Model-Behavior/C07-04-Source-Attribution-Citation-Integrity.md) | Over 300 federal judges have standing orders; 5-6 new cases/day |
| [C07-Model-Behavior](chapters/C07-Model-Behavior/C07-Model-Behavior.md) | Deepfake files ~500K (2023) to 8M+ (2025) |
| [C07-Model-Behavior](chapters/C07-Model-Behavior/C07-Model-Behavior.md) | Social platforms strip C2PA; vendor signing list |
| [C08-03-Memory-Expiry-Revocation-Leakage-Prevention](chapters/C08-Memory-and-Embeddings/C08-03-Memory-Expiry-Revocation-Leakage-Prevention.md) | prEN 18229-1 at Enquiry stage; Help Net Security April 2026 Article 12 analysis recommending signed logs |
| [C08-Memory-and-Embeddings](chapters/C08-Memory-and-Embeddings/C08-Memory-and-Embeddings.md) | Milvus v2.6.15 release date (Apr 24) |
| [C09-01-Execution-Budgets](chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md) | Five Eyes 'Careful adoption of agentic AI services' (May 1, 2026); NIST page updated April 20; NCCoE concept paper description |
| [C09-01-Execution-Budgets](chapters/C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md) | Uber 84%/95%/70% figures, ClawHavoc 341 skills, 82 countries, ~346K stars, Gravitee 21% runtime visibility |
| [C09-02-High-Impact-Action-Approval](chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md) | OWASP State of Agentic AI Security and Governance 2.01 quote; June 3 paper / June 4 summit |
| [C09-02-High-Impact-Action-Approval](chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md) | Prisma AIRS 3.0 AI Agent Gateway integrates with CyberArk for agent identity |
| [C09-02-High-Impact-Action-Approval](chapters/C09-Orchestration-and-Agents/C09-02-High-Impact-Action-Approval.md) | Cisco RSAC keynote quote 'know your agents, authorize every action, and adapt to risk...' |
| [C09-03-Tool-and-Plugin-Isolation](chapters/C09-Orchestration-and-Agents/C09-03-Tool-and-Plugin-Isolation.md) | MCP CVE count 'dozens' January-April 2026 |
| [C09-05-Agent-Authorization-Delegation](chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md) | Proofpoint Agent Integrity Framework defines 'Mean Time to Understand (MTU)' and an Understand-Align-Authorize sequence |
| [C09-05-Agent-Authorization-Delegation](chapters/C09-Orchestration-and-Agents/C09-05-Agent-Authorization-Delegation.md) | Kurtz RSAC keynote: two incidents at Fortune 50 companies; Sevii 'Autonomous Proactive Security' module at RSAC 2026 |
| [C09-Orchestration-and-Agents](chapters/C09-Orchestration-and-Agents/C09-Orchestration-and-Agents.md) | Agent Governance Toolkit: authentication primitives shipped with zero production callers (hackerbot-claw coverage) |
| [C10-MCP-Security](chapters/C10-MCP-Security/C10-MCP-Security.md) | May 19 high-risk classification draft requires composite/agentic systems to be assessed holistically |
| [C10-MCP-Security](chapters/C10-MCP-Security/C10-MCP-Security.md) | Unnamed 2,614-implementation survey (82%/67%) and 41% of 518 registry servers with zero auth |
| [C10-MCP-Security](chapters/C10-MCP-Security/C10-MCP-Security.md) | TS SDK 161 contributors; Uber/Amazon tens of thousands weekly executions over Thrift/Protobuf/HTTP |
| [C11-01-Model-Alignment-Safety](chapters/C11-Adversarial-Robustness/C11-01-Model-Alignment-Safety.md) | OBLITERATUS 1,000 stars in one day; six-stage pipeline with 13 methods |
| [C11-03-Model-Extraction-Defense](chapters/C11-Adversarial-Robustness/C11-03-Model-Extraction-Defense.md) | Gartner: through 2026, over 80% of unauthorized AI incidents will result from internal misuse |
| [C11-04-Model-Runtime-Anomaly-Detection](chapters/C11-Adversarial-Robustness/C11-04-Model-Runtime-Anomaly-Detection.md) | ISO/IEC 27090 draft says detecting poisoning is 'often difficult' |
| [C11-04-Model-Runtime-Anomaly-Detection](chapters/C11-Adversarial-Robustness/C11-04-Model-Runtime-Anomaly-Detection.md) | Cisco mcp-scanner, Snyk agent-scan, Backslash, Pipelock do SHA-256 tool-description pinning; mcp-scan first with rug-pull detection |
| [C12-01-Request-Response-Logging](chapters/C12-Monitoring-and-Logging/C12-01-Request-Response-Logging.md) | prEN 18229-1 enquiry since Jan 23 2026; M/593 Q4 2026; prEN ISO/IEC 24970 formal-vote dispatch May 20 |
| [C12-02-Abuse-Detection-Alerting](chapters/C12-Monitoring-and-Logging/C12-02-Abuse-Detection-Alerting.md) | CrowdStrike AIDR SDK languages/gateways/MCP; Cisco Identity Intelligence/Duo/Secure Access; Zenity Foundry GA; Model Armor auto-routing |
| [C12-03-Model-Drift-Detection](chapters/C12-Monitoring-and-Logging/C12-03-Model-Drift-Detection.md) | Vendor capability claims (Galileo, Driftbase, Superwise, Evidently, Opik, Langfuse, OpenObserve, DriftWatch) |
| [C12-05-Training-Data-Model-Lifecycle-Audit](chapters/C12-Monitoring-and-Logging/C12-05-Training-Data-Model-Lifecycle-Audit.md) | EU AI Omnibus political agreement date (7 May 2026) |
| [Appendix-B-Controls-Inventory](appendices/Appendix-B-Controls-Inventory.md) | NVIDIA NGC, Kaggle, Hugging Face rolling out OMS signing |
| [Appendix-B-Controls-Inventory](appendices/Appendix-B-Controls-Inventory.md) | Microsoft Zero Trust for AI 7 pillars; COSAiS IR 8605 series; AI Exchange 70 pages; AIMA Aug 2025; lakeFS acquired DVC 2025 |
| [Appendix-C-AI-Secure-Coding](appendices/Appendix-C-AI-Secure-Coding.md) | Apiiro CLI / Guardian Agent launched April 9, 2026 with six agent skills |
| [Appendix-C-AI-Secure-Coding](appendices/Appendix-C-AI-Secure-Coding.md) | Claude Code markdown prompt injection disclosed April 3, 2026 |

## Close-out

- [x] Resolve the 14 pending Appendix B statistics rows, recording evidence or moving unsupported claims to the held list.
- [x] Check remaining Appendix B product capabilities, maturity assessments, incident descriptions, and framework/legal claims.
- [x] Review chapter and appendix supporting claims, including repeated occurrences of corrected or held statistics.
- [x] Re-run requirement alignment, counts, links, and documentation checks after the final edits.
- [x] Record remaining limitations.
- [ ] Obtain maintainer acceptance, then close #1109 and hand the review to Otto.
