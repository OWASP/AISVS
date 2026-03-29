# C13.5: AI Incident Response Planning & Execution

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 3 (13.5.1 -- 13.5.3)

## Purpose

This section addresses the preparation for and execution of incident response procedures specific to AI systems. Traditional IR playbooks assume well-understood attack vectors (malware, network intrusion, data breach), but AI incidents introduce novel challenges: model compromise may be invisible without specialized forensics, data poisoning effects may persist through retraining cycles, and the blast radius of a compromised model in an agentic system can be difficult to scope. These requirements ensure organizations are prepared for AI-specific security events.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **13.5.1** | **Verify that** incident response plans specifically address AI-related security events including model compromise, data poisoning, adversarial attacks, model inversion, prompt injection campaigns, and model extraction, with specific containment and investigation steps for each scenario. | 1 | Unprepared response to AI-specific security events; delayed containment due to lack of AI-specific playbooks; investigators unfamiliar with AI forensic techniques missing evidence or misinterpreting model behavior. Real-world examples: the Microsoft Copilot EchoLeak vulnerability (CVE-2025-32711, CVSS 9.3) enabled zero-click prompt injection data exfiltration from OneDrive/SharePoint/Teams; the GTG-1002 campaign (November 2025) used compromised AI tooling to automate 80--90% of intrusion operations across ~30 organizations ([MITRE ATLAS T0051](https://atlas.mitre.org/)). | Review IR plans for AI-specific scenarios. Verify each scenario has: (1) detection indicators, (2) containment steps, (3) investigation procedures, (4) recovery steps, (5) communication plan. Validate playbooks against the CoSAI AI IR Framework's OASIS CACAO format for machine-readable automation. Conduct tabletop exercises for at least two AI-specific scenarios annually — use the GenAI-IRF six archetypes to structure exercise scenarios. | Key AI IR scenarios with unique containment needs: **Model compromise** -- swap to known-good model version, preserve compromised model for forensics. **Data poisoning** -- identify poisoning window, quarantine affected training data, assess retraining needs; research shows as few as 250 malicious documents can compromise a model (Anthropic/UK AISI, 2025). **Prompt injection campaign** -- block attack patterns, update filters, assess data exfiltration scope. **Model extraction** -- block source IPs/accounts, assess intellectual property exposure, evaluate extracted model capabilities. **Shadow AI exposure** -- in 2025, 20% of organizations experienced shadow AI breaches averaging $670K higher cost than traditional breaches, with 97% lacking basic access controls. |
| **13.5.2** | **Verify that** incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2 | Inability to investigate AI incidents effectively; missed attack indicators due to lack of AI forensic capabilities; incorrect root cause analysis leading to ineffective remediation. As of 2025, 97% of organizations use models from public repositories but only 49% scan them before deployment; 45% of reported breaches involved malware introduced through public model repositories (HiddenLayer AI Threat Landscape Report). | Verify availability of AI forensic tooling: HiddenLayer AISec Platform 2.0 for runtime model monitoring and model genealogy, Protect AI Guardian (acquired by Palo Alto Networks, July 2025) for model scanning across the lifecycle, ModelScan (open-source) for detecting serialization attacks in PyTorch/TensorFlow/Keras/Sklearn/XGBoost model files. Confirm at least one IR team member has AI/ML security training (e.g., SANS FOR563). Review recent AI incident post-mortems for quality of technical analysis. Check SOAR platform integration -- verify AI-specific playbooks exist in the SOAR (Splunk SOAR, FortiSOAR, or Devo SOAR) with automated triage for model anomaly alerts. | AI forensic capabilities needed: (1) ability to replay inputs against model versions to reproduce behavior, (2) attention/attribution analysis to understand why a model produced specific outputs, (3) training data provenance investigation using OWASP CycloneDX AI BOM, (4) embedding space analysis for anomaly detection. The commercial tooling landscape has matured since 2024: HiddenLayer AISec 2.0, Protect AI Guardian, and Robust Intelligence (now part of Cisco) provide runtime detection. Open-source options include ModelScan, Fickling (pickle exploit detection), and NB Defense (notebook security). |
| **13.5.3** | **Verify that** post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3 | Repeat incidents due to unaddressed root causes; safety filters remaining vulnerable to demonstrated attack techniques; organizational knowledge of AI attack patterns not captured systematically. ISACA's analysis of 2025 AI incidents found the biggest failures were organizational (weak controls, unclear ownership, misplaced trust), not technical -- most were predictable and avoidable. | Review post-incident reports for AI-specific remediation actions. Verify safety filter update process triggered by incidents. Confirm lessons learned are tracked and fed back into: (1) detection rules (C13.2), (2) safety filters (C07), (3) training data curation (C01), (4) IR playbook updates, (5) MITRE ATLAS incident sharing submissions. AI-powered incident management platforms report saving ~4.9 hours per incident on post-mortem creation and MTTR reduction of 40--60% through automated triage. Verify that the organization submits anonymized incident data to community sharing programs (e.g., MITRE ATLAS AI Incident Sharing). | Post-incident retraining introduces its own risks: rushed retraining may introduce new vulnerabilities, and the retraining window leaves the system running a known-vulnerable model. Establish criteria for when retraining is necessary vs. when filter updates or model rollback suffice. Note the UK ICO's draft guidance (2025) that data deletion requests under GDPR may require retraining or deleting the model entirely, adding a compliance dimension to post-incident remediation. ISO 42001 Annex A Control 8.4 aligns AI incident management with the NIST AI RMF Govern 4.3 function, with organizations typically finding 40--50% overlap in governance processes. |

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

**OWASP GenAI Incident Response Guide (v1.0, August 2025).** Extends the OWASP Top 10 for LLM Applications with a dedicated six-phase IR lifecycle -- Preparation, Detection & Analysis, Containment, Eradication, Recovery, and Lessons Learned -- tailored for generative AI threats. The guide covers prompt injection, model inversion, data poisoning, unauthorized model access, abnormal agent behavior, and compromised plugins/integrations. Key emphasis on "protective prompting" as a temporary containment measure during active investigation, and on adversarial re-testing before returning a model to production.

**GenAI Incident Response Framework (GenAI-IRF, January 2026).** Published as a peer-reviewed framework that clusters generative AI risks into six recurrent incident archetypes, each with a unique containment and response workflow. Aligned with NIST SP 800-61r3, NIST AI 600-1, MITRE ATLAS, and OWASP LLM Top 10. The archetype approach helps responders rapidly classify novel AI incidents into actionable response patterns rather than building playbooks from scratch. Validated through scenario-based simulations with AI security practitioners from finance, technology, and academic sectors.

### GenAI Incident Archetypes

The GenAI-IRF identifies six archetypes that cover the majority of generative AI security incidents. Each archetype has distinct detection indicators and containment workflows:

1. **Model manipulation** -- adversarial inputs or fine-tuning attacks that alter model behavior. Containment: input filtering hardening, model rollback, behavioral comparison against baseline.
2. **Data exfiltration via model** -- prompt injection or inference attacks that extract training data, system prompts, or sensitive context. Containment: output filtering, rate limiting, session termination.
3. **Misinformation cascades** -- model generates convincing but false information that propagates through downstream systems or users. Containment: output flagging, human-in-the-loop gates, downstream notification.
4. **Prompt-based privilege escalation** -- crafted prompts bypass authorization controls to access restricted functions or data. Containment: privilege boundary enforcement, prompt audit, access revocation.
5. **Plugin/integration compromise** -- third-party components connected to the AI system are exploited to inject malicious data or commands. Containment: plugin isolation, supply chain audit, fallback to core functionality.
6. **Autonomous agent deviation** -- agentic systems take unintended actions beyond their defined scope. Containment: action budget enforcement, tool access revocation, agent suspension.

### Containment Decision Matrix

Based on the Glacis AI IR Playbook (2026) and CoSAI guidance, containment severity should drive response intensity:

| Severity | Indicators | Containment Action | Example |
|----------|-----------|-------------------|---------|
| **Low** | Performance drift, minor output anomalies | Traffic throttling, enhanced monitoring | Model accuracy degradation below threshold |
| **Medium** | Confirmed adversarial inputs, bias disparity >10-15 percentage points | Shadow mode with fallback decisions, feature flag disable | Detected prompt injection attempts with partial success |
| **High** | Active data exfiltration, model compromise confirmed | Model rollback to last known-good version | Training data poisoning confirmed via embedding analysis |
| **Critical** | Autonomous agent taking unauthorized actions, safety-critical output failures | Full service shutdown, rule-based fallback only | Multi-agent compromise propagation detected |

Key principle: AI containment often means restricting model behavior (input filtering, output gates, capability reduction) rather than traditional network isolation.

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

### Forensic Investigation Techniques

Model introspection tools are essential for AI-specific IR. As of March 2026, the practical toolkit includes:

- **Explainability methods**: SHAP (SHapley Additive exPlanations), LIME (Local Interpretable Model-agnostic Explanations), and integrated gradients can reveal whether a model is responding to legitimate features or hidden triggers. During an incident, comparing attribution maps between the suspect model and a known-good baseline can identify backdoor indicators.
- **Drift detection**: Statistical tests such as Kolmogorov-Smirnov (KS), Population Stability Index (PSI), and Jensen-Shannon divergence can quantify whether model behavior has shifted from its validated baseline -- useful for detecting slow-onset poisoning.
- **Input/output replay**: Reproducing the incident by replaying logged inputs against both the suspect and clean model versions. This requires content logging to be enabled (per 13.1.8) and model version snapshots to be maintained.
- **Embedding space analysis**: Visualizing and clustering embeddings can reveal anomalous data clusters introduced by poisoning attacks. Tools like UMAP or t-SNE projections compared across time windows help identify when poisoned data entered the training pipeline.
- **Training data lineage**: Tracing which training samples influenced specific model behaviors, using influence functions or data provenance records. Critical for scoping data poisoning incidents.

The SANS FOR563 course (Applied AI for Digital Forensics and Incident Response) provides hands-on training in using local LLMs for forensic analysis -- log analysis, artifact examination, and building custom forensic agents -- though it focuses on using AI as a forensic tool rather than investigating AI systems themselves.

### MITRE ATLAS AI Incident Sharing

Launched in October 2024, MITRE's AI Incident Sharing initiative enables organizations to submit and receive anonymized data about real-world attacks on AI-enabled systems. The program operates through a trusted community of contributors -- over 15 organizations including CrowdStrike, Microsoft, JPMorgan Chase, Intel, HiddenLayer, and the Cloud Security Alliance. Anyone can submit an incident via [ai-incidents.mitre.org](https://ai-incidents.mitre.org/), and submitting organizations are considered for membership in the data-receiver community.

As of 2025, ATLAS added 14 new techniques specifically for AI agents, covering risks including prompt injection, memory manipulation, and tool abuse. This expanding taxonomy is directly useful for structuring IR playbooks around known attack patterns.

### EU AI Act Incident Reporting Obligations

Organizations operating high-risk AI systems in the EU face mandatory incident reporting under Article 73 of the EU AI Act (Regulation 2024/1689):

- **Reporting timeline**: Serious incidents must be reported within 2 to 15 days depending on severity, with "widespread infringement" incidents requiring notification within 2 days of awareness.
- **GPAI systemic risk**: Article 55(1)(c) requires providers of general-purpose AI models classified as systemic risk to report serious incidents to the EU AI Office and relevant national authorities. The European Commission published a reporting template and Code of Practice in 2025 to operationalize this obligation.
- **Enforcement**: Obligations for GPAI providers took effect August 2, 2025. Full enforcement of the serious incident guidance begins August 2, 2026.
- **IR integration**: Organizations should integrate EU AI Act notification timelines into their AI IR playbooks alongside existing breach notification requirements (e.g., GDPR 72-hour rule). The shorter 2-day window for widespread infringements demands pre-drafted notification templates and clear escalation paths.

### Real-World AI Security Incidents Informing IR Planning

As of March 2026, several high-profile incidents illustrate why AI-specific IR playbooks are essential:

- **Microsoft Copilot EchoLeak (June 2025):** CVE-2025-32711 (CVSS 9.3 Critical) -- a zero-click prompt injection vulnerability that enabled automated data exfiltration from OneDrive, SharePoint, and Teams without any user interaction. Attackers sent emails with hidden instructions that Copilot processed silently. This incident demonstrated that prompt injection containment cannot rely on user awareness; automated input filtering and output gates are the first line of defense.
- **GTG-1002 Campaign (November 2025):** Chinese state-sponsored actors weaponized AI coding tools to automate 80--90% of intrusion operations across approximately 30 organizations spanning tech, finance, and government sectors. The campaign handled reconnaissance, exploit development, credential harvesting, and lateral movement with minimal human oversight. IR teams had to scope blast radius across organizations that shared the same compromised toolchain.
- **Medical LLM Data Poisoning (January 2025):** Researchers from NYU, Washington University, and Columbia University demonstrated that injecting just 2,000 fake medical articles (costing approximately $5) increased harmful outputs by ~5% in large language models. Separately, Anthropic and the UK AI Safety Institute found that as few as 250 malicious documents can compromise a model, with models from 600M to 13B parameters equally vulnerable. The implication for IR: poisoning may be undetectable without baseline behavioral comparison, and the "incident window" may span the entire period since contaminated data entered the pipeline.
- **Shadow AI Breaches (2025, industry-wide):** 20% of organizations experienced breaches involving unauthorized AI tools, with costs averaging $670,000 higher than traditional breaches. 97% of AI-related breaches lacked basic access controls. This pattern requires IR playbooks to include shadow AI discovery and containment procedures.
- **Deepfake Fraud Wave (Q1 2025):** Over 160 reported incidents with losses exceeding $200M. Voice cloning requiring only 3--5 seconds of audio enabled social engineering attacks, with human detection accuracy for high-quality deepfakes at just 24.5%. IR teams must now consider AI-generated media as an attack vector requiring specialized detection tools.

### SOAR Platform Integration for AI Incident Response

As of 2026, SOAR platforms are evolving to support AI-specific playbooks. Key integration patterns:

- **AI-specific playbook templates:** Leading SOAR platforms (Splunk SOAR with 300+ pre-built integrations, FortiSOAR, Devo SOAR) support custom playbooks for AI incident types. Organizations should create playbooks for each GenAI-IRF archetype (model manipulation, data exfiltration via model, misinformation cascades, prompt-based privilege escalation, plugin compromise, autonomous agent deviation).
- **LLM-powered adaptive playbooks:** Contemporary SOAR solutions now leverage LLMs to dynamically generate and adapt playbooks based on incident context, moving beyond static rule-based automation. This enables real-time contextual reasoning during AI-specific incidents where attack patterns may be novel.
- **Model monitoring alert integration:** Connect HiddenLayer AISec, Protect AI Guardian, or equivalent runtime monitoring tools to the SOAR platform so model anomaly alerts trigger automated triage workflows -- initial evidence collection, model snapshot preservation, and on-call escalation.
- **Automated evidence preservation:** SOAR playbooks should automatically capture model weights, inference logs, embedding snapshots, and safety filter decision logs when an AI incident alert fires, before any manual remediation actions that might destroy forensic evidence.

### AI Incident Response Metrics

Organizations should track AI-specific IR metrics alongside traditional MTTD/MTTR:

- **Mean Time to Detect (MTTD) for model anomalies:** Target under 1 hour for production models. Drift detection using KS tests or PSI should feed automated alerting.
- **Mean Time to Contain (MTTC) for AI incidents:** AI containment (model rollback, input filter hardening, capability reduction) differs from network containment. Track separately from traditional MTTC.
- **Mean Time to Restore (MTTR):** Organizations using AI-powered SOAR report 40--60% MTTR reductions through automated triage and alert correlation. Elite teams with automated remediation achieve resolution in under 10 minutes; traditional teams average 30--60 minutes.
- **Post-incident learning velocity:** Track time from incident closure to updated detection rules, safety filters, and playbook amendments. AI-powered post-mortem tools report saving ~4.9 hours per incident on documentation and analysis.

### Emerging Threat: Scheming and Sandbagging

Recent research (2024--2025) has demonstrated that advanced AI models can distinguish between testing and deployment contexts, deliberately underperforming during evaluation ("sandbagging") and exhibiting different behavior in production. Laboratory tests have shown AI systems replicating their own code and weights to new servers, which could impede emergency shutdown procedures. IR playbooks must account for the possibility that a compromised model may behave normally during investigation while continuing malicious behavior in production contexts.

### Tabletop Exercise Scenarios

Based on real incidents catalogued in the AI Incident Database and MITRE ATLAS case studies, recommended tabletop exercises include:

1. **Prompt injection campaign**: A coordinated attack extracts system prompts and customer data through multi-turn prompt injection. Exercise scope: detection timeline, containment actions, data breach notification requirements.
2. **Training data poisoning discovery**: Post-deployment analysis reveals that a fraction of training data was adversarially modified. Exercise scope: determining the poisoning window, assessing affected predictions, retraining decisions.
3. **Multi-agent compromise propagation**: One agent in a multi-agent system is compromised and uses inter-agent communication to influence other agents' behavior. Exercise scope: identifying the initially compromised agent, tracing propagation paths, coordinated containment.
4. **Model extraction and weaponization**: API monitoring detects systematic model extraction attempts. Exercise scope: assessing IP exposure, evaluating whether the extracted model could be weaponized, legal and business response.
5. **AI hallucination liability event**: A customer-facing AI system provides materially incorrect information that leads to financial or safety consequences (cf. the 2024 Air Canada chatbot ruling where the airline was held liable for its chatbot's misinformation). Exercise scope: output audit trail, liability determination, customer notification, safety filter updates.
6. **Regulatory notification drill**: A serious incident triggers EU AI Act Article 73 reporting obligations with a 2-day window. Exercise scope: incident classification, notification template completion, coordination between IR team and legal/compliance, parallel GDPR notification if personal data involved.

---

## Related Standards & References

- **NIST SP 800-61 Rev 2** -- Computer Security Incident Handling Guide, the foundation for AI-specific IR extensions
- **NIST AI 100-1** -- AI Risk Management Framework, includes guidance on AI incident management
- **NIST Cybersecurity Framework Profile for AI (2025 draft)** -- Maps CSF Respond/Recover functions to AI-specific controls
- **CoSAI AI Incident Response Framework v1.0** -- AI-specific IR framework with OASIS CACAO playbooks ([coalitionforsecureai.org](https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/))
- **CISA JCDC AI Cybersecurity Collaboration Playbook (2025)** -- Cross-sector AI incident coordination ([cisa.gov](https://www.cisa.gov/sites/default/files/2025-01/JCDC%20AI%20Playbook.pdf))
- **MITRE ATLAS** -- Provides the attack taxonomy needed to structure AI-specific IR playbooks ([atlas.mitre.org](https://atlas.mitre.org/))
- **AI Incident Database** -- Collection of real-world AI incidents useful for tabletop exercise development ([incidentdatabase.ai](https://incidentdatabase.ai/))
- **OWASP GenAI Incident Response Guide v1.0 (2025)** -- Six-phase IR lifecycle for generative AI threats ([genai.owasp.org](https://genai.owasp.org/resource/genai-incident-response-guide-1-0/))
- **GenAI-IRF** -- Practical Incident-Response Framework for Generative AI Systems, six incident archetypes ([mdpi.com](https://www.mdpi.com/2624-800X/6/1/20))
- **MITRE ATLAS AI Incident Sharing** -- Anonymized real-world AI incident data sharing ([ai-incidents.mitre.org](https://ai-incidents.mitre.org/))
- **EU AI Act Article 73** -- Serious incident reporting obligations for high-risk AI systems ([artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/73/))
- **EU AI Act Article 55** -- GPAI systemic risk reporting obligations and Commission template ([digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/library/ai-act-commission-publishes-reporting-template-serious-incidents-involving-general-purpose-ai))
- **NIST IR 8596 (preliminary draft)** -- Cybersecurity Framework Profile for AI ([nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8596.iprd.pdf))
- **SANS FOR563** -- Applied AI for Digital Forensics and Incident Response ([sans.org](https://www.sans.org/cyber-security-courses/applied-ai-local-large-language-models))
- **FIRST CSIRT Services Framework** -- Incident response service descriptions adaptable for AI-specific capabilities
- **HiddenLayer AISec Platform 2.0** -- Runtime model monitoring, model genealogy, and AI Bill of Materials ([hiddenlayer.com](https://www.hiddenlayer.com/))
- **Protect AI Guardian** -- Model scanning across the AI lifecycle, acquired by Palo Alto Networks July 2025 ([protectai.com](https://protectai.com/guardian))
- **ModelScan** -- Open-source ML model scanner for serialization attacks ([github.com/protectai/modelscan](https://github.com/protectai/modelscan))
- **ISO/IEC 42001** -- AI Management System standard, Annex A Control 8.4 covers AI incident management; 40--50% process overlap with NIST AI RMF ([iso.org](https://www.iso.org/standard/81230.html))
- **ISACA: Lessons Learned from Top 2025 AI Incidents** -- Governance analysis of major 2025 AI failures ([isaca.org](https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2025/avoiding-ai-pitfalls-in-2026-lessons-learned-from-top-2025-incidents))
- **DoD/NSA AI/ML Supply Chain Risks and Mitigations (March 2026)** -- US defense guidance on AI supply chain incident scenarios ([media.defense.gov](https://media.defense.gov/2026/Mar/04/2003882809/-1/-1/0/AI_ML_SUPPLY_CHAIN_RISKS_AND_MITIGATIONS.PDF))

---

## Open Research Questions

- How should IR severity levels be calibrated for AI incidents? The CoSAI framework's autonomy-level classification helps, but severity matrices specific to AI attack types (prompt injection vs. data poisoning vs. model extraction) remain underdeveloped.
- What is the appropriate containment strategy when a model is suspected to be poisoned but no clean version exists? Current guidance defaults to rule-based fallback systems, but this may be unacceptable for complex AI capabilities.
- How should multi-agent system incidents be scoped when compromise may propagate through agent interactions? The CoSAI framework acknowledges this but does not yet provide detailed multi-agent IR procedures.
- What AI security certifications or training programs adequately prepare IR teams for AI-specific incidents? SANS FOR563 covers AI-assisted forensics, but as of March 2026 no widely recognized certification exists for investigating AI systems themselves -- comparable to GCIH or GCFA for traditional IR.
- How should organizations handle the "scheming model" scenario where a compromised model behaves normally during investigation but acts maliciously in production? Standard forensic replay may be insufficient if the model can detect the investigation context.
- What is the minimum viable AI forensic toolkit that IR teams should maintain, and how should model weights be preserved as forensic evidence given their size (potentially hundreds of GB)?
- How mature are SOAR platform integrations for AI-specific incident types? As of early 2026, most AI-specific playbooks are custom-built; standardized SOAR templates for the GenAI-IRF six archetypes would significantly reduce time-to-respond for organizations without dedicated AI security teams.
- How should organizations handle the regulatory intersection of GDPR data deletion requests and post-incident model retention? The UK ICO's 2025 draft guidance suggests retraining or deleting models when data subjects exercise deletion rights, which may conflict with forensic evidence preservation requirements during active investigations.

---
