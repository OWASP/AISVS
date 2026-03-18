# C13: Monitoring, Logging & Anomaly Detection

> **Source:** [`1.0/en/0x10-C13-Monitoring-and-Logging.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C13-Monitoring-and-Logging.md)
> **Requirements:** 47 | **Sections:** 8

## Control Objective

This section provides requirements for delivering real-time and forensic visibility into what the model and other AI components see, do, and return, so threats can be detected, triaged, and learned from.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C13.1 | Request & Response Logging | 8 | 13.1.1–13.1.8 |
| C13.2 | Abuse Detection and Alerting | 10 | 13.2.1–13.2.10 |
| C13.3 | Model Drift Detection | 5 | 13.3.1–13.3.5 |
| C13.4 | Performance & Behavior Telemetry | 5 | 13.4.1–13.4.5 |
| C13.5 | AI Incident Response Planning & Execution | 3 | 13.5.1–13.5.3 |
| C13.6 | AI Performance Degradation Detection | 6 | 13.6.1–13.6.6 |
| C13.7 | DAG Visualization & Workflow Security | 5 | 13.7.1–13.7.5 |
| C13.8 | Proactive Security Behavior Monitoring | 5 | 13.8.1–13.8.5 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Undetected model drift leading to degraded or biased outputs over time
- Abuse pattern escalation (testing boundaries before launching full attack)
- Log injection or log poisoning to hide attack traces
- Insufficient logging of AI-specific events (tool calls, RAG retrievals, agent actions)
- Alert fatigue from overly broad anomaly detection

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

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
| C13.1 Request & Response Logging | _TBD_ | |
| C13.2 Abuse Detection and Alerting | _TBD_ | |
| C13.3 Model Drift Detection | _TBD_ | |
| C13.4 Performance & Behavior Telemetry | _TBD_ | |
| C13.5 AI Incident Response Planning & Execution | _TBD_ | |
| C13.6 AI Performance Degradation Detection | _TBD_ | |
| C13.7 DAG Visualization & Workflow Security | _TBD_ | |
| C13.8 Proactive Security Behavior Monitoring | _TBD_ | |

---

## Open Research Questions

- [ ] What's the right granularity for logging AI interactions (full prompts vs. metadata only)?
- [ ] How do you balance logging completeness with privacy (PII in prompts/responses)?
- [ ] What AI-specific SIEM rules are most effective for detecting attacks?
- [ ] How should model drift detection thresholds be calibrated?

---

## Related Standards & Cross-References

- [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf)
- [NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

