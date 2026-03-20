# C13: Monitoring, Logging & Anomaly Detection

> **Source:** [`1.0/en/0x10-C13-Monitoring-and-Logging.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C13-Monitoring-and-Logging.md)
> **Requirements:** 47 | **Sections:** 8

## Control Objective

This section provides requirements for delivering real-time and forensic visibility into what the model and other AI components see, do, and return, so threats can be detected, triaged, and learned from.

> **2025-2026 Highlights:** OpenTelemetry GenAI SIG and LLM observability platforms (LangSmith, Langfuse, Arize) are establishing standard schemas for AI telemetry. New requirements address covert channel detection in LLM API traffic (C13.2.10) and session-level multi-turn jailbreak trajectory analysis (C13.2.8).

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C13.1 | Request & Response Logging | 8 | [C13-01-Request-Response-Logging](C13-01-Request-Response-Logging) |
| C13.2 | Abuse Detection and Alerting | 10 | [C13-02-Abuse-Detection-Alerting](C13-02-Abuse-Detection-Alerting) |
| C13.3 | Model Drift Detection | 5 | [C13-03-Model-Drift-Detection](C13-03-Model-Drift-Detection) |
| C13.4 | Performance & Behavior Telemetry | 5 | [C13-04-Performance-Behavior-Telemetry](C13-04-Performance-Behavior-Telemetry) |
| C13.5 | AI Incident Response Planning & Execution | 3 | [C13-05-Incident-Response](C13-05-Incident-Response) |
| C13.6 | AI Performance Degradation Detection | 6 | [C13-06-Performance-Degradation-Detection](C13-06-Performance-Degradation-Detection) |
| C13.7 | DAG Visualization & Workflow Security | 5 | [C13-07-DAG-Visualization-Workflow-Security](C13-07-DAG-Visualization-Workflow-Security) |
| C13.8 | Proactive Security Behavior Monitoring | 5 | [C13-08-Proactive-Security-Behavior-Monitoring](C13-08-Proactive-Security-Behavior-Monitoring) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Undetected model drift leading to degraded or biased outputs over time
- Abuse pattern escalation (testing boundaries before launching full attack)
- Log injection or log poisoning to hide attack traces
- Insufficient logging of AI-specific events (tool calls, RAG retrievals, agent actions)
- Alert fatigue from overly broad anomaly detection

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **LLM observability:** LangSmith, Langfuse, Arize AI, WhyLabs, Helicone
- **Drift detection:** Evidently AI, NannyML, Great Expectations
- **SIEM integration:** Splunk AI, Elastic AI Assistant, custom OpenTelemetry exporters
- **Incident response:** PagerDuty, Opsgenie with AI-specific runbooks

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C13.1 Request & Response Logging | Medium | OpenTelemetry GenAI SIG and LLM observability platforms provide solid foundations |
| C13.2 Abuse Detection and Alerting | Low-Medium | Signature-based detection exists; behavioral analysis is emerging |
| C13.3 Model Drift Detection | Medium | Well-established for traditional ML; less mature for LLMs |
| C13.4 Performance & Behavior Telemetry | Medium-High | Standard APM tools extend to AI workloads |
| C13.5 AI Incident Response Planning & Execution | Low | Few AI-specific IR frameworks or playbooks exist |
| C13.6 AI Performance Degradation Detection | Medium | Mature for tabular ML; nascent for generative AI |
| C13.7 DAG Visualization & Workflow Security | Low | Emerging area with limited dedicated tooling |
| C13.8 Proactive Security Behavior Monitoring | Low | Research-stage; minimal production tooling |

---

## Open Research Questions

- [ ] What's the right granularity for logging AI interactions (full prompts vs. metadata only)?
- [ ] How do you balance logging completeness with privacy (PII in prompts/responses)?
- [ ] What AI-specific SIEM rules are most effective for detecting attacks?
- [ ] How should model drift detection thresholds be calibrated?
- [ ] How do you distinguish adversarial drift from natural concept drift?
- [ ] What DAG visualization security controls are necessary vs. theoretical?

---

## Related Standards & Cross-References

- [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf)
- [NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C02 User Input Validation | Prompt injection detection | C13.2 monitors for attacks that C02 prevents at input |
| C07 Model Behavior | Safety filter logging | C13.1 logs filter decisions defined in C07 |
| C09 Orchestration & Agents | Agent action logging | C13.8 monitors agent behaviors governed by C09 |
| C12 Privacy | PII redaction in logs | C13.1.4 redaction supports C12 privacy requirements |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
