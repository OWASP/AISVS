# C6.6 Supply Chain Attack Monitoring

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 3 | **IDs:** 6.6.1–6.6.3

## Purpose

Preventive controls (vetting, scanning, pinning) reduce supply-chain risk but cannot eliminate it. This section addresses the detection and response layer — ensuring that when a supply-chain compromise does occur, the organization can detect it quickly, respond effectively, and roll back to a known-good state. AI supply chains have unique monitoring challenges: model poisoning may not manifest as a traditional indicator of compromise, and CI/CD pipelines for ML workloads have distinct attack patterns.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.6.1** | **Verify that** incident response playbooks include rollback procedures for compromised models or libraries. | 2 | D | **Delayed or ineffective response to supply-chain compromise.** Without pre-planned rollback procedures, teams waste critical time during an incident figuring out how to revert to a clean model or library version, extending the window of exploitation. (SolarWinds-style supply chain attacks demonstrated the cost of slow response.) | Request and review incident response playbooks. Verify they include: identification of the compromised artifact, immediate containment (isolation of affected systems), rollback to the last known-good version (with specific steps for model rollback, container rollback, and library rollback), notification procedures, and post-incident analysis. Conduct a tabletop exercise to validate the playbook. | Model rollback is more complex than code rollback — it may require re-serving a previous model version, updating feature stores, and reverting any downstream systems that consumed the model's outputs. Playbooks should address cascade effects. |
| **6.6.2** | **Verify that** CI/CD audit logs are streamed to centralized security monitoring with detections for anomalous package pulls or tampered build steps. | 2 | V | **Stealthy modification of build pipelines.** An attacker with CI/CD access can modify build steps to inject malicious dependencies, alter training configurations, or exfiltrate model weights. Without centralized audit logging and anomaly detection, these modifications go unnoticed. (Codecov supply chain attack 2021; CircleCI breach 2023) | Confirm that CI/CD platform audit logs (GitHub Actions audit log, GitLab audit events, Jenkins build logs) are forwarded to a SIEM or centralized log platform. Verify that detection rules exist for: unusual package source changes, new or modified build steps, downloads from non-approved registries, abnormal build durations (which may indicate injected steps), and privilege escalation within CI runners. | ML-specific CI/CD anomalies are not well-covered by standard SIEM detection rules. Organizations should develop custom detections for: changes to training hyperparameters, dataset source modifications, model registry write operations from unexpected service accounts, and GPU resource consumption anomalies. |
| **6.6.3** | **Verify that** threat-intelligence enrichment tags AI-specific indicators (e.g., model-poisoning indicators of compromise) in alert triage. | 3 | V | **Missed AI-specific supply-chain threats due to generic threat intelligence.** Standard threat intelligence feeds focus on traditional software supply-chain indicators (malicious packages, compromised credentials). AI-specific threats (poisoned models, backdoored adapters, manipulated datasets) require specialized intelligence sources. | Verify that the organization's threat intelligence platform or SIEM enrichment pipeline includes AI-specific indicator sources. Check for: subscriptions to AI security advisories (Protect AI Huntr, MITRE ATLAS updates, Hugging Face security bulletins), custom indicators for known AI supply-chain attack patterns, and tagging/categorization that distinguishes AI supply-chain alerts from general software supply-chain alerts in the triage workflow. | AI-specific threat intelligence is an immature field. There is no equivalent of VirusTotal or the NVD specifically for AI supply-chain threats. Protect AI's Huntr bug bounty and MITRE ATLAS are the closest resources. Organizations will likely need to supplement with manual monitoring of AI security research publications and community forums. |

---

## Related Standards & References

- [MITRE ATLAS — ML Attack Techniques](https://atlas.mitre.org/)
- [Protect AI Huntr — AI/ML Bug Bounty](https://huntr.com/)
- [NIST Cybersecurity Framework — Respond Function](https://www.nist.gov/cyberframework)
- [CISA — Defending CI/CD Pipelines](https://www.cisa.gov/news-events/alerts)
- [OpenSSF Scorecard — Supply Chain Security](https://securityscorecards.dev/)
- [Codecov Supply Chain Attack Analysis (2021)](https://about.codecov.io/security-update/)
- [CircleCI Security Incident (2023)](https://circleci.com/blog/jan-4-2023-incident-report/)

---

## Open Research Questions

- What are the most reliable indicators of compromise for AI-specific supply-chain attacks (as opposed to traditional software supply-chain IOCs)?
- How can model behavior monitoring (C13) be integrated with supply-chain monitoring to detect poisoning that only manifests in production inference behavior?
- What does an effective AI supply-chain incident response tabletop exercise look like — what scenarios should it cover?
- How should organizations handle "slow-burn" supply-chain attacks where poisoning is introduced gradually across multiple dataset or model updates?
