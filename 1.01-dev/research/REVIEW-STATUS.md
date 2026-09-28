# 1.01 Research Review Status

This checklist tracks [#1109](https://github.com/OWASP/AISVS/issues/1109). It is a review record, not an extension of AISVS requirements or a release announcement.

## Current position

- Requirement-text and level synchronization has been checked for all 213 active core requirements and all 69 Appendix C requirements. That does not validate the surrounding research claims.
- Appendix B retains 44 statistics rows: 30 source-checked and 14 pending. Nine former rows and associated prose are held below rather than presented as established findings.
- Full source review remains open across the 12 chapter groups and three appendices. No overall completion percentage is claimed.
- Otto owns the formal release, including final metadata, dates, and artifacts.

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

## Remaining content review

The inventory covers the 60 research documents that existed before this checklist: 56 chapter documents, three appendices, and the README. Each chapter group includes its hub and section pages. “Open” means a full source audit is not signed off; targeted corrections have already been made in some groups.

| Area | Documents | Remaining source review |
| --- | ---: | --- |
| [C1 Training Data](chapters/C01-Training-Data/) | 4 | Open |
| [C2 Input Validation](chapters/C02-User-Input-Validation/) | 3 | Open |
| [C3 Model Lifecycle](chapters/C03-Model-Lifecycle-Management/) | 6 | Open |
| [C4 Infrastructure](chapters/C04-Infrastructure/) | 4 | Open |
| [C5 Access Control](chapters/C05-Access-Control/) | 4 | Open |
| [C6 Supply Chain](chapters/C06-Supply-Chain/) | 3 | Open |
| [C7 Model Behavior](chapters/C07-Model-Behavior/) | 5 | Open |
| [C8 Memory and Embeddings](chapters/C08-Memory-and-Embeddings/) | 4 | Open |
| [C9 Orchestration and Agents](chapters/C09-Orchestration-and-Agents/) | 7 | Open |
| [C10 MCP Security](chapters/C10-MCP-Security/) | 5 | Open |
| [C11 Adversarial Robustness](chapters/C11-Adversarial-Robustness/) | 5 | Open |
| [C12 Monitoring and Logging](chapters/C12-Monitoring-and-Logging/) | 6 | Open |
| [Appendix A](appendices/Appendix-A-Glossary.md) | 1 | Definitions and supporting claims |
| [Appendix B](appendices/Appendix-B-Controls-Inventory.md) | 1 | Remaining statistics, product coverage, incidents, framework and legal claims |
| [Appendix C](appendices/Appendix-C-AI-Secure-Coding.md) | 1 | Supporting research beyond synchronized requirements |
| [README](README.md) | 1 | Final navigation and count check after remaining edits |

### Appendix B statistics

This is the complete row inventory for the current adoption snapshot. Update the count above and this table when a row changes or is checked. Figures in pending rows are recorded for review, not independently affirmed here.

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
| OWASP Agentic Top 10 categories that prompt injection maps to (6 of 10) | Pending | Confirm original study, date, denominator, and claim scope. |
| Studied breached orgs with governance policies to manage AI or detect shadow AI (37%) | Checked | IBM 2025 breached-organization sample; original report Figures 28 and 31. |
| Year-over-year growth in enterprise AI/ML traffic (83%) | Checked | Publisher's 2026 report summary; traffic growth, not organization prevalence. |
| Unique AI/ML applications observed in enterprise traffic (3,400+) | Checked | Publisher's 2026 report summary; traffic growth, not organization prevalence. |
| Studied orgs with employees using unsanctioned apps, including shadow AI (not AI-only) (98%) | Checked | Original 2025 report, pp. 2-5; 1,000 organizations; apps generally, not AI-only. |
| Avg cost of studied breaches involving unsanctioned or shadow AI (USD 4.63M) | Checked | IBM 2025 breached-organization sample; original report Figures 28 and 31. |
| Surveyed orgs reporting control of agent actions with guardrails and live monitoring (24%) | Checked | Original 2025 report, pp. 24, 26; 8,039 senior leaders in organizations with 500+ employees; August 2025 survey. |
| NHI-to-human identity ratio in modern enterprises (~45:1) | Pending | Confirm original study, date, denominator, and claim scope. |
| NHI-to-human identity ratio in cloud-native / DevOps environments (~144:1) | Pending | Confirm original study, date, denominator, and claim scope. |
| NHIs older than one year without credential rotation (47%) | Pending | Confirm original study, date, denominator, and claim scope. |
| Enterprises that have suffered a breach via a compromised NHI (~67%) | Pending | Confirm original study, date, denominator, and claim scope. |
| Analyzed applications not routing authentication through a central identity provider (57%) | Checked | Original report, finding 3; April 2025-March 2026 application telemetry. The denominator is applications, not identities; no AI-only prevalence measure. |
| CVEs exploited within 24 hours of disclosure (28.3%) | Pending | Confirm original study, date, denominator, and claim scope. |
| MCP-related CVEs filed in Jan–Feb 2026 (30+) | Pending | Confirm original study, date, denominator, and claim scope. |
| Internet-accessible MCP services (mostly unauthenticated) (12,520) | Pending | Confirm original study, date, denominator, and claim scope. |
| Remote MCP servers exposing tools with no authentication (~40%) | Pending | Confirm original study, date, denominator, and claim scope. |
| Exposed MCP servers carrying CVSS 9.8 vulnerabilities (1,467) | Pending | Confirm original study, date, denominator, and claim scope. |
| MCP CVEs assigned via one automated taint-analysis study (VIPER-MCP) (67) | Pending | Confirm original study, date, denominator, and claim scope. |
| Commercial LLM APIs sharing prompt caches globally across users (7 of 8 caching APIs) | Pending | Confirm original study, date, denominator, and claim scope. |
| Documents needed to backdoor an LLM regardless of model size (~250) | Pending | Confirm original study, date, denominator, and claim scope. |
| Surveyed orgs reporting advanced API security maturity (not an AI maturity score) (8%) | Checked | Publisher's April 2026 announcement; 327 security professionals surveyed in early 2026. Direct API measure replaces a 92% complement mislabeled AI maturity. |
| Surveyed orgs unable to monitor non-human traffic, according to the publisher's summary (48.9%) | Checked | Publisher's April 2026 survey summary; no independent observation of every organization's traffic. |
| Surveyed orgs unable to effectively distinguish legitimate AI agents from malicious bots (48.3%) | Checked | Publisher's April 2026 survey summary; self-reported capability. |
| Attack attempts analyzed by Salt Labs originating from authenticated sources (not an AI-agent share) (99%) | Checked | Publisher's April 2026 announcement; separate telemetry, not the 327-person survey. Does not quantify attacks attributable to agents. |
| Surveyed security leaders reporting increased executive scrutiny of AI security risks (78.6%) | Checked | Publisher's April 2026 survey summary; reported scrutiny, not an incident rate. |
| Surveyed orgs that delayed production releases over API security concerns (47%) | Checked | Publisher's April 2026 announcement; percentage of surveyed organizations, not percentage of all releases. |
| Surveyed orgs without written agentic AI policies that had deployed agents (79%) | Pending | The press release supports the conditional wording; reconcile conflicting publisher summaries against the full report. |
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

## Next review batches

- [ ] Resolve the 14 pending Appendix B statistics rows, recording evidence or moving unsupported claims to the held list.
- [ ] Check remaining Appendix B product capabilities, maturity assessments, incident descriptions, and framework/legal claims.
- [ ] Review chapter and appendix supporting claims, including repeated occurrences of corrected or held statistics.
- [ ] Re-run requirement alignment, counts, links, and documentation checks after the final edits.
- [ ] Record remaining limitations and obtain maintainer acceptance before closing #1109 and handing the review to Otto.
