# C13.5: AI Incident Response Planning & Execution

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 3 (13.5.1 -- 13.5.3)

## Purpose

This section addresses the preparation for and execution of incident response procedures specific to AI systems. Traditional IR playbooks assume well-understood attack vectors (malware, network intrusion, data breach), but AI incidents introduce novel challenges: model compromise may be invisible without specialized forensics, data poisoning effects may persist through retraining cycles, and the blast radius of a compromised model in an agentic system can be difficult to scope. These requirements ensure organizations are prepared for AI-specific security events.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **13.5.1** | Verify that incident response plans specifically address AI-related security events including model compromise, data poisoning, adversarial attacks, model inversion, prompt injection campaigns, and model extraction, with specific containment and investigation steps for each scenario. | 1 | D/V | Unprepared response to AI-specific security events; delayed containment due to lack of AI-specific playbooks; investigators unfamiliar with AI forensic techniques missing evidence or misinterpreting model behavior. | Review IR plans for AI-specific scenarios. Verify each scenario has: (1) detection indicators, (2) containment steps, (3) investigation procedures, (4) recovery steps, (5) communication plan. Conduct tabletop exercises for at least two AI-specific scenarios annually. | Key AI IR scenarios with unique containment needs: **Model compromise** -- swap to known-good model version, preserve compromised model for forensics. **Data poisoning** -- identify poisoning window, quarantine affected training data, assess retraining needs. **Prompt injection campaign** -- block attack patterns, update filters, assess data exfiltration scope. **Model extraction** -- block source IPs/accounts, assess intellectual property exposure, evaluate extracted model capabilities. |
| **13.5.2** | Verify that incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2 | D/V | Inability to investigate AI incidents effectively; missed attack indicators due to lack of AI forensic capabilities; incorrect root cause analysis leading to ineffective remediation. | Verify availability of AI forensic tooling (model introspection tools, input/output replay capability, embedding analysis tools). Confirm at least one IR team member has AI/ML security training. Review recent AI incident post-mortems for quality of technical analysis. | AI forensic capabilities needed: (1) ability to replay inputs against model versions to reproduce behavior, (2) attention/attribution analysis to understand why a model produced specific outputs, (3) training data provenance investigation, (4) embedding space analysis for anomaly detection. Few commercial tools exist -- most organizations build custom tooling. |
| **13.5.3** | Verify that post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3 | D/V | Repeat incidents due to unaddressed root causes; safety filters remaining vulnerable to demonstrated attack techniques; organizational knowledge of AI attack patterns not captured systematically. | Review post-incident reports for AI-specific remediation actions. Verify safety filter update process triggered by incidents. Confirm lessons learned are tracked and fed back into: (1) detection rules (C13.2), (2) safety filters (C07), (3) training data curation (C01), (4) IR playbook updates. | Post-incident retraining introduces its own risks: rushed retraining may introduce new vulnerabilities, and the retraining window leaves the system running a known-vulnerable model. Establish criteria for when retraining is necessary vs. when filter updates or model rollback suffice. |

---

## Related Standards & References

- **NIST SP 800-61 Rev 2** -- Computer Security Incident Handling Guide, the foundation for AI-specific IR extensions
- **NIST AI 100-1** -- AI Risk Management Framework, includes guidance on AI incident management
- **MITRE ATLAS** -- Provides the attack taxonomy needed to structure AI-specific IR playbooks ([atlas.mitre.org](https://atlas.mitre.org/))
- **AI Incident Database** -- Collection of real-world AI incidents useful for tabletop exercise development ([incidentdatabase.ai](https://incidentdatabase.ai/))
- **FIRST CSIRT Services Framework** -- Incident response service descriptions adaptable for AI-specific capabilities

---

## Open Research Questions

- What does AI-specific digital forensics look like in practice? What artifacts should be preserved from a compromised model?
- How should IR severity levels be calibrated for AI incidents (e.g., is a jailbreak that exposes system prompts a P1 or P2)?
- What is the appropriate containment strategy when a model is suspected to be poisoned but no clean version exists?
- How should multi-agent system incidents be scoped when compromise may propagate through agent interactions?
- What AI security certifications or training programs adequately prepare IR teams for AI-specific incidents?

---
