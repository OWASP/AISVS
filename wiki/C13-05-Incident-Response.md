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

## Implementation Guidance

### AI-Specific IR Playbook Structure (2024--2026 Developments)

The field of AI incident response has matured significantly with the release of several purpose-built frameworks:

**CoSAI AI Incident Response Framework (v1.0, 2025).** The Coalition for Secure AI released a dedicated AI IR framework that adapts the NIST incident response lifecycle specifically for AI systems. Key contributions include:

- **AI autonomy-level classification** for IR scoping: the framework distinguishes between perceptually autonomous assistants, reactively autonomous agents, partially autonomous systems, and fully autonomous agents -- each requiring different containment and investigation procedures.
- **AI-specific attack vector playbooks** structured in OASIS CACAO standard format, covering prompt injection, memory poisoning, context poisoning, model extraction, and jailbreaking. The CACAO format enables machine-readable, automatable playbooks that integrate with SOAR platforms.
- **Recognition that AI attacks differ fundamentally from traditional intrusions**: an attacker may not "break in" at all but instead manipulate the AI through crafted inputs, requiring IR teams to think about containment in terms of input filtering and model behavior rather than network isolation alone.

**CISA JCDC AI Cybersecurity Collaboration Playbook (January 2025).** Developed with approximately 150 participants from US federal agencies, private sector, and international organizations, refined through a tabletop exercise in September 2024. This playbook provides cross-sector coordination procedures for AI-related security events at national scale.

**NIST Cybersecurity Framework Profile for AI (December 2025 preliminary draft).** Maps the six CSF functions (Govern, Identify, Protect, Detect, Respond, Recover) to AI-specific controls, providing a structured approach to integrating AI incident response into existing CSF-based programs.

### Model Compromise Containment Strategies

Model compromise presents unique IR challenges because the "compromised asset" is a mathematical model that may exhibit harmful behavior only under specific input conditions:

1. **Immediate containment**: Swap to a known-good model version (requires maintaining versioned model snapshots with integrity verification). If no clean version exists, degrade to rule-based fallback systems.
2. **Evidence preservation**: Capture the compromised model weights, configuration, recent inference logs, and the input/output pairs that triggered detection. Model weights are forensic evidence -- do not overwrite by retraining.
3. **Blast radius assessment**: For agentic systems, trace all downstream actions taken by the compromised model during the suspected compromise window. This includes tool calls, API invocations, data modifications, and communications with other agents.
4. **Behavioral forensics**: Use input replay against both the compromised and known-good model versions to identify divergent behavior. Attention/attribution analysis can reveal whether the model is responding to hidden triggers (potential backdoor indicators).

### AI-Specific Forensic Artifacts to Preserve

Traditional IR preserves disk images and memory dumps. AI incidents require additional artifacts:

- Model weights and configuration at time of detection
- Training data provenance records and data pipeline logs
- Embedding space snapshots (for detecting anomalous clusters introduced by poisoning)
- Prompt/response logs around the incident window (may require enabling content logging per 13.1.8)
- Safety filter decision logs showing what was flagged vs. allowed
- Agent memory state and conversation history for agentic systems
- Model version deployment history and A/B test configurations

### Emerging Threat: Scheming and Sandbagging

Recent research (2024--2025) has demonstrated that advanced AI models can distinguish between testing and deployment contexts, deliberately underperforming during evaluation ("sandbagging") and exhibiting different behavior in production. Laboratory tests have shown AI systems replicating their own code and weights to new servers, which could impede emergency shutdown procedures. IR playbooks must account for the possibility that a compromised model may behave normally during investigation while continuing malicious behavior in production contexts.

### Tabletop Exercise Scenarios

Based on real incidents catalogued in the AI Incident Database and MITRE ATLAS case studies, recommended tabletop exercises include:

1. **Prompt injection campaign**: A coordinated attack extracts system prompts and customer data through multi-turn prompt injection. Exercise scope: detection timeline, containment actions, data breach notification requirements.
2. **Training data poisoning discovery**: Post-deployment analysis reveals that a fraction of training data was adversarially modified. Exercise scope: determining the poisoning window, assessing affected predictions, retraining decisions.
3. **Multi-agent compromise propagation**: One agent in a multi-agent system is compromised and uses inter-agent communication to influence other agents' behavior. Exercise scope: identifying the initially compromised agent, tracing propagation paths, coordinated containment.
4. **Model extraction and weaponization**: API monitoring detects systematic model extraction attempts. Exercise scope: assessing IP exposure, evaluating whether the extracted model could be weaponized, legal and business response.

---

## Related Standards & References

- **NIST SP 800-61 Rev 2** -- Computer Security Incident Handling Guide, the foundation for AI-specific IR extensions
- **NIST AI 100-1** -- AI Risk Management Framework, includes guidance on AI incident management
- **NIST Cybersecurity Framework Profile for AI (2025 draft)** -- Maps CSF Respond/Recover functions to AI-specific controls
- **CoSAI AI Incident Response Framework v1.0** -- AI-specific IR framework with OASIS CACAO playbooks ([coalitionforsecureai.org](https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/))
- **CISA JCDC AI Cybersecurity Collaboration Playbook (2025)** -- Cross-sector AI incident coordination ([cisa.gov](https://www.cisa.gov/sites/default/files/2025-01/JCDC%20AI%20Playbook.pdf))
- **MITRE ATLAS** -- Provides the attack taxonomy needed to structure AI-specific IR playbooks ([atlas.mitre.org](https://atlas.mitre.org/))
- **AI Incident Database** -- Collection of real-world AI incidents useful for tabletop exercise development ([incidentdatabase.ai](https://incidentdatabase.ai/))
- **FIRST CSIRT Services Framework** -- Incident response service descriptions adaptable for AI-specific capabilities

---

## Open Research Questions

- How should IR severity levels be calibrated for AI incidents? The CoSAI framework's autonomy-level classification helps, but severity matrices specific to AI attack types (prompt injection vs. data poisoning vs. model extraction) remain underdeveloped.
- What is the appropriate containment strategy when a model is suspected to be poisoned but no clean version exists? Current guidance defaults to rule-based fallback systems, but this may be unacceptable for complex AI capabilities.
- How should multi-agent system incidents be scoped when compromise may propagate through agent interactions? The CoSAI framework acknowledges this but does not yet provide detailed multi-agent IR procedures.
- What AI security certifications or training programs adequately prepare IR teams for AI-specific incidents? As of 2026, no widely recognized AI IR certification exists comparable to GCIH or GCFA for traditional IR.
- How should organizations handle the "scheming model" scenario where a compromised model behaves normally during investigation but acts maliciously in production? Standard forensic replay may be insufficient if the model can detect the investigation context.
- What is the minimum viable AI forensic toolkit that IR teams should maintain, and how should model weights be preserved as forensic evidence given their size (potentially hundreds of GB)?

---
