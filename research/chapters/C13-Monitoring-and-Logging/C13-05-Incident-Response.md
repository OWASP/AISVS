# C13.5: AI Incident Response Planning & Execution

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging.md)
> **Requirements:** 3 | **IDs:** 13.5.1--13.5.3

## Purpose

This section addresses the preparation for and execution of incident response procedures specific to AI systems. Traditional IR playbooks assume well-understood attack vectors (malware, network intrusion, data breach), but AI incidents introduce novel challenges: model compromise may be invisible without specialized forensics, data poisoning effects may persist through retraining cycles, and the blast radius of a compromised model in an agentic system can be difficult to scope. These requirements ensure organizations are prepared for AI-specific security events.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **13.5.1** | **Verify that** incident response plans specifically address AI-related security events including model compromise, data poisoning, adversarial attacks, model inversion, prompt injection campaigns, and model extraction, with specific containment and investigation steps for each scenario. | 1 | Unprepared response to AI-specific security events; delayed containment due to lack of AI-specific playbooks; investigators unfamiliar with AI forensic techniques missing evidence or misinterpreting model behavior. Real-world examples: the Microsoft Copilot EchoLeak vulnerability (CVE-2025-32711, CVSS 9.3) enabled zero-click prompt injection data exfiltration from OneDrive/SharePoint/Teams; the GTG-1002 campaign (November 2025) used compromised AI tooling to automate 80--90% of intrusion operations across ~30 organizations ([MITRE ATLAS T0051](https://atlas.mitre.org/)). The **McKinsey Lilli breach (February 28, 2026)** saw an autonomous agent (CodeWall) exploit 22 unauthenticated API endpoints plus SQL injection to exfiltrate 46.5M chat messages, 728K confidential files, 57K accounts, 3.68M RAG chunks, and 95 writable system prompts — an attacker who modified those prompts could have silently poisoned responses firm-wide. The **Sears Home Services exposure (early March 2026)** left 3.7M chatbot transcripts, 1.4M audio recordings, and 4TB of plaintext data unprotected, ripe for voice-cloning and social engineering attacks. | Review IR plans for AI-specific scenarios. Verify each scenario has: (1) detection indicators, (2) containment steps, (3) investigation procedures, (4) recovery steps, (5) communication plan. Validate playbooks against the CoSAI AI IR Framework's OASIS CACAO format for machine-readable automation. Conduct tabletop exercises for at least two AI-specific scenarios annually — use the GenAI-IRF six archetypes to structure exercise scenarios. Confirm playbooks map to the current ATLAS agent-focused techniques in v5.6.0: AML.T0096 (AI Service API abuse), AML.T0098 (agent tool credential harvesting), AML.T0099 (agent tool data poisoning), AML.T0100 (AI agent clickbait), and AML.T0101 (data destruction via agent tool invocation). | Key AI IR scenarios with unique containment needs: **Model compromise** -- swap to known-good model version, preserve compromised model for forensics. **Data poisoning** -- identify poisoning window, quarantine affected training data, assess retraining needs; research shows as few as 250 malicious documents can compromise a model (Anthropic/UK AISI, 2025). **Prompt injection campaign** -- block attack patterns, update filters, assess data exfiltration scope. **Model extraction** -- block source IPs/accounts, assess intellectual property exposure, evaluate extracted model capabilities. **Shadow AI exposure** -- in 2025, 20% of organizations experienced shadow AI breaches averaging $670K higher cost than traditional breaches, with 97% lacking basic access controls. **System-prompt compromise** -- a newer archetype surfaced by the McKinsey Lilli incident: an attacker with write access to stored system prompts can silently poison every downstream response without touching model weights; IR plans should treat prompts as critical assets and include prompt-diff monitoring alongside model integrity checks. |
| **13.5.2** | **Verify that** incident response teams have access to AI-specific forensic tools and expertise to investigate model behavior and attack vectors. | 2 | Inability to investigate AI incidents effectively; missed attack indicators due to lack of AI forensic capabilities; incorrect root cause analysis leading to ineffective remediation. As of 2025, 97% of organizations use models from public repositories but only 49% scan them before deployment; 45% of reported breaches involved malware introduced through public model repositories (HiddenLayer AI Threat Landscape Report). Unit 42's **2026 Global IR Report** (750+ engagements) found attackers now move from initial access to data exfiltration in as little as 72 minutes — 4× faster than 2025 — and identity weaknesses factored into nearly 90% of investigations; IR teams that lack AI-specific forensic tooling simply cannot scope blast radius inside that window. Memory-poisoning research (MINJA, 2026) achieves >95% injection success against production agents with zero elevated access, and standard LLM-based detectors miss 66% of poisoned memory entries — underscoring why agent memory stores need dedicated forensic snapshots. | Verify availability of AI forensic tooling: HiddenLayer AISec Platform 2.0 for runtime model monitoring and model genealogy, Protect AI Guardian (acquired by Palo Alto Networks, July 2025) for model scanning across the lifecycle, ModelScan (open-source) for detecting serialization attacks in PyTorch/TensorFlow/Keras/Sklearn/XGBoost model files. For agent deployments, confirm memory/vector-store snapshotting is enabled (e.g., [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/) addressing ASI06 Memory & Context Poisoning in the 2026 Top 10 for Agentic Applications) so investigators can roll back to a pre-compromise state and enumerate every decision made after the suspect write. Confirm at least one IR team member has AI/ML security training (e.g., SANS FOR563). Review recent AI incident post-mortems for quality of technical analysis. Check SOAR platform integration -- verify AI-specific playbooks exist in the SOAR (Splunk SOAR, FortiSOAR, or Devo SOAR) with automated triage for model anomaly alerts. | AI forensic capabilities needed: (1) ability to replay inputs against model versions to reproduce behavior, (2) attention/attribution analysis to understand why a model produced specific outputs, (3) training data provenance investigation using OWASP CycloneDX AI BOM, (4) embedding space analysis for anomaly detection, (5) forensic snapshots of agent long-term memory/vector stores with per-write rollback pointers. The commercial tooling landscape has matured since 2024: HiddenLayer AISec 2.0, Protect AI Guardian, and Robust Intelligence (now part of Cisco) provide runtime detection. Open-source options include ModelScan, Fickling (pickle exploit detection), NB Defense (notebook security), and the OWASP Agent Memory Guard project (memory snapshot + rollback for LangGraph/CrewAI agents). A persistent gap as of April 2026: no widely adopted standard for storing and chain-of-custody-signing model weights as forensic evidence when weights are hundreds of GB. |
| **13.5.3** | **Verify that** post-incident analysis includes model retraining considerations, safety filter updates, and lessons learned integration into security controls. | 3 | Repeat incidents due to unaddressed root causes; safety filters remaining vulnerable to demonstrated attack techniques; organizational knowledge of AI attack patterns not captured systematically. ISACA's analysis of 2025 AI incidents found the biggest failures were organizational (weak controls, unclear ownership, misplaced trust), not technical -- most were predictable and avoidable. The EU AI Act **Article 73 draft guidance** (European Commission, published 26 September 2025; consultation closed 7 November 2025; applies from 2 August 2026) explicitly prohibits providers from altering a high-risk AI system during post-incident investigation unless the competent authority is notified — meaning sloppy "just retrain it" reflexes can now trigger regulatory findings and fines up to €15M or 3% of global turnover. | Review post-incident reports for AI-specific remediation actions. Verify safety filter update process triggered by incidents. Confirm lessons learned are tracked and fed back into: (1) detection rules (C13.2), (2) safety filters (C07), (3) training data curation (C01), (4) IR playbook updates, (5) MITRE ATLAS incident sharing submissions. AI-powered incident management platforms report saving ~4.9 hours per incident on post-mortem creation and MTTR reduction of 40--60% through automated triage. Verify that the organization submits anonymized incident data to community sharing programs (e.g., MITRE ATLAS AI Incident Sharing). Confirm post-incident workflows explicitly preserve evidence and document any system changes to meet EU AI Act Article 73 non-alteration requirements before retraining. | Post-incident retraining introduces its own risks: rushed retraining may introduce new vulnerabilities, and the retraining window leaves the system running a known-vulnerable model. Establish criteria for when retraining is necessary vs. when filter updates or model rollback suffice. Note the UK ICO's draft guidance (2025) that data deletion requests under GDPR may require retraining or deleting the model entirely, adding a compliance dimension to post-incident remediation. ISO 42001 Annex A Control 8.4 aligns AI incident management with the NIST AI RMF Govern 4.3 function, with organizations typically finding 40--50% overlap in governance processes. The new EU AI Act Article 73 non-alteration clause creates a tension with rapid remediation — organizations must decide between staying compromised longer (and preserving forensic fidelity) or notifying the authority and proceeding with controlled changes; update playbooks so legal, IR, and engineering agree on the escalation path before an incident happens. |

---

## Implementation Guidance

### AI-Specific IR Playbook Structure (2024--2026 Developments)

The field of AI incident response has matured significantly with the release of several purpose-built frameworks:

**CoSAI AI Incident Response Framework (v1.0, 2025).** The Coalition for Secure AI released a dedicated AI IR framework that adapts the NIST incident response lifecycle specifically for AI systems. Key contributions include:

- **AI autonomy-level classification** for IR scoping: the framework distinguishes between perceptually autonomous assistants, reactively autonomous agents, partially autonomous systems, and fully autonomous agents -- each requiring different containment and investigation procedures.
- **AI-specific attack vector playbooks** structured in OASIS CACAO standard format, covering prompt injection, memory poisoning, context poisoning, model extraction, and jailbreaking. The CACAO format enables machine-readable, automatable playbooks that integrate with SOAR platforms.
- **Recognition that AI attacks differ fundamentally from traditional intrusions**: an attacker may not "break in" at all but instead manipulate the AI through crafted inputs, requiring IR teams to think about containment in terms of input filtering and model behavior rather than network isolation alone.

**CISA JCDC AI Cybersecurity Collaboration Playbook (January 2025).** Developed with approximately 150 participants from US federal agencies, private sector, and international organizations, refined through a tabletop exercise in September 2024. This playbook provides cross-sector coordination procedures for AI-related security events at national scale.

**NIST SP 800-61r3 and Cyber AI Profile.** NIST finalized SP 800-61 Revision 3 in April 2025, replacing the older Computer Security Incident Handling Guide with a CSF 2.0-aligned incident response community profile. The December 2025 preliminary draft of NIST IR 8596 then layered AI-specific cybersecurity concerns onto CSF 2.0 through three focus areas: securing AI system components, defending with AI-enabled cyber capabilities, and thwarting AI-enabled attacks. Together, these documents give teams a defensible way to fold AI incident response into existing Govern, Detect, Respond, and Recover workflows instead of maintaining a disconnected AI-only playbook.

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

### Agent Memory and Vector-Store Forensics

As agentic deployments have moved from pilots to production, long-term memory stores (vector databases, persistent RAG stores, conversation memory) have become the attack surface most frequently overlooked by IR teams. The OWASP 2026 Top 10 for Agentic Applications classifies this as **ASI06: Memory & Context Poisoning**, and practitioner research (MINJA, 2026) has shown >95% injection success against production agents with no elevated access, while standard LLM-based detectors miss 66% of poisoned entries.

A minimum-viable agent-memory IR capability should include:

- **Per-write forensic snapshots** — every commit to long-term memory gets a snapshot with a rollback pointer, so a detected poisoning event can trigger a "one-click" revert to the last known-good state instead of manual row-by-row audit. The [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/) project provides a reference implementation for LangGraph and CrewAI agents.
- **Timestamped provenance for every memory entry** — writer identity, source document, triggering conversation ID — so investigators can answer "when did the corruption enter?" and "which downstream decisions were influenced?"
- **Embedding drift alerts** on memory stores using the same KS/PSI/Jensen-Shannon tests applied to model output distributions.
- **Decision re-certification workflows** — once a poisoning timestamp is known, every agent action taken after that point must be flagged for human review, re-run against a clean memory snapshot, or rolled back. This is functionally equivalent to "re-playing transactions after a database restore" and deserves the same rigor.

Tabletop exercises should include a scenario where memory poisoning is detected three weeks after the initial compromise — forcing the team to decide between broad rollback (losing three weeks of legitimate memory) and targeted surgical cleanup (requiring far more investigator time).

### AI-Specific Forensic Artifacts to Preserve

Traditional IR preserves disk images and memory dumps. AI incidents require additional artifacts:

- Model weights and configuration at time of detection
- Training data provenance records and data pipeline logs
- Embedding space snapshots (for detecting anomalous clusters introduced by poisoning)
- Prompt/response logs around the incident window (may require event-triggered content logging per 13.1.5)
- Safety filter decision logs showing what was flagged vs. allowed
- Agent memory state and conversation history for agentic systems
- Per-write forensic snapshots of agent long-term memory and vector stores with rollback pointers (per [OWASP Agent Memory Guard](https://owasp.org/www-project-agent-memory-guard/))
- System prompt history with timestamps and writer identity — the McKinsey Lilli incident showed system prompts are themselves forensic artifacts requiring integrity monitoring
- Tool invocation logs for agents (tool name, parameters, response, caller identity) — required for AML.T0099 and AML.T0101 investigations
- Model version deployment history and A/B test configurations
- Stored API keys and OAuth token usage logs for agent-connected tools (AML.T0098 scope)

### Forensic Investigation Techniques

Model introspection tools are essential for AI-specific IR. As of March 2026, the practical toolkit includes:

- **Explainability methods**: SHAP (SHapley Additive exPlanations), LIME (Local Interpretable Model-agnostic Explanations), and integrated gradients can reveal whether a model is responding to legitimate features or hidden triggers. During an incident, comparing attribution maps between the suspect model and a known-good baseline can identify backdoor indicators.
- **Drift detection**: Statistical tests such as Kolmogorov-Smirnov (KS), Population Stability Index (PSI), and Jensen-Shannon divergence can quantify whether model behavior has shifted from its validated baseline -- useful for detecting slow-onset poisoning.
- **Input/output replay**: Reproducing the incident by replaying logged inputs against both the suspect and clean model versions. This requires event-triggered content logging (per 13.1.5) and maintained model version snapshots.
- **Embedding space analysis**: Visualizing and clustering embeddings can reveal anomalous data clusters introduced by poisoning attacks. Tools like UMAP or t-SNE projections compared across time windows help identify when poisoned data entered the training pipeline.
- **Training data lineage**: Tracing which training samples influenced specific model behaviors, using influence functions or data provenance records. Critical for scoping data poisoning incidents.

The SANS FOR563 course (Applied AI for Digital Forensics and Incident Response) provides hands-on training in using local LLMs for forensic analysis -- log analysis, artifact examination, and building custom forensic agents -- though it focuses on using AI as a forensic tool rather than investigating AI systems themselves.

### Agentic Tool-Use Incident Patterns

Current ATLAS data (v5.6.0, May 2026) makes agent tool abuse concrete enough for playbooks to test directly. For any production agent with read/write tools, IR teams should predefine the evidence they need for each pattern:

- **AI Service API abuse (AML.T0096):** preserve AI API request logs, task identifiers, polling cadence, and egress destinations so investigators can distinguish legitimate agent traffic from command-and-control over an AI service.
- **Agent tool credential harvesting (AML.T0098):** enumerate every credential store, repository, document system, and secret path reachable by the agent identity; rotate tokens touched during the suspected window even if the model never displayed the secret back to the attacker.
- **Agent tool data poisoning (AML.T0099):** snapshot the tool response corpus, vector-store writes, retrieved documents, and conversation state so the response can trace which poisoned artifact entered context and which downstream decisions consumed it.
- **Data destruction via agent tool invocation (AML.T0101):** require immutable logs for delete, update, deploy, and cloud-control-plane tools; a rollback plan is not credible unless tool parameters and caller identities are preserved before containment begins.

The July 2025 Amazon Q Developer VS Code extension incident is a useful tabletop pattern: AWS traced CVE-2025-8217 to an inappropriately scoped GitHub token that allowed malicious code into a released extension, then removed version 1.84.0 and told users to update to 1.85.0. AWS reported that the malicious code did not execute because of a syntax error, but the response lesson still stands: the IR plan must cover extension marketplace removal, credential revocation, downstream fork cleanup, and forensic review of any agent instruction that could have invoked filesystem or cloud-destructive tools.

### MITRE ATLAS AI Incident Sharing

Launched in October 2024, MITRE's AI Incident Sharing initiative enables organizations to submit and receive anonymized data about real-world attacks on AI-enabled systems. The program operates through a trusted community of contributors -- over 15 organizations including CrowdStrike, Microsoft, JPMorgan Chase, Intel, HiddenLayer, and the Cloud Security Alliance. Anyone can submit an incident via [ai-incidents.mitre.org](https://ai-incidents.mitre.org/), and submitting organizations are considered for membership in the data-receiver community.

As of 2025, ATLAS added 14 new techniques specifically for AI agents, covering risks including prompt injection, memory manipulation, and tool abuse. The current ATLAS data release (**v5.6.0, May 2026**) includes agent-focused technique IDs that IR playbooks should enumerate directly as expected attack paths:

- **AML.T0096 — AI Service API (C2 abuse).** Attackers use AI service APIs (e.g., OpenAI Assistants API in the new case study **SesameOp / AML.CS0042**) as covert command-and-control channels. Detection requires egress monitoring of AI API calls and anomalous task-polling patterns, not just network-layer C2 hunting.
- **AML.T0098 — AI Agent Tool Credential Harvesting.** Attackers retrieve credentials and secrets from tools and data sources the agent is connected to. IR scope must include every credential the agent's tool set could have touched in the suspected window.
- **AML.T0099 — AI Agent Tool Data Poisoning.** Malicious content injected into agent tools via prompt injection or phishing then flows back into model context. Containment overlaps memory-poisoning procedures but extends to tool responses.
- **AML.T0100 — AI Agent Clickbait.** Adversaries manipulate web interfaces so agentic browsers execute unintended actions. Relevant for any deployment that gives an agent a headless browser or web-fetch capability.
- **AML.T0101 — Data Destruction via AI Agent Tool Invocation.** Attackers use legitimate agent tool capabilities (delete endpoints, file operations) to destroy data. Containment requires tool-level blast-radius assessment and immutable logs of every tool invocation.

The current ATLAS case-study data also covers MCP server compromise, indirect prompt injection via MCP channels, malicious AI agent deployment, exposed agent control interfaces, and destructive tool invocation scenarios — exercise these in tabletop drills if the organization operates MCP servers or agents with mutative tools. The Center for Threat-Informed Defense's **OpenClaw investigation (February 2026, report PR-26-00176-1)** mapped real AI-agent incident patterns to ATLAS TTPs and identified the chokepoint techniques adversaries rely on; use it to prioritize detection and response coverage.

### EU AI Act Incident Reporting Obligations

Organizations operating high-risk AI systems in the EU face mandatory incident reporting under Article 73 of the EU AI Act (Regulation 2024/1689):

- **Reporting timeline**: Serious incidents must be reported within 2 to 15 days depending on severity. The European Commission's draft guidance (published 26 September 2025, consultation closed 7 November 2025) clarifies three tiers: **15 days** for general serious incidents, **10 days** where a death may have been caused, and **2 days** for widespread rights violations or serious/irreversible disruption of critical infrastructure.
- **GPAI systemic risk**: Article 55(1)(c) requires providers of general-purpose AI models classified as systemic risk to report serious incidents to the EU AI Office and relevant national authorities. The European Commission published a reporting template and Code of Practice in 2025 to operationalize this obligation.
- **Non-alteration during investigation**: The draft Article 73 guidance explicitly prohibits providers from altering the AI system during the investigation without first informing the competent authority if the change could affect subsequent analysis. This is a meaningful operational constraint — rushed retraining or silent model rollbacks can now generate regulatory findings in addition to the incident itself.
- **Enforcement**: Obligations for GPAI providers took effect August 2, 2025. Full enforcement of the Article 73 serious incident guidance applies from **August 2, 2026**. Non-compliance can trigger fines up to €15 million or 3% of global annual turnover.
- **IR integration**: Organizations should integrate EU AI Act notification timelines into their AI IR playbooks alongside existing breach notification requirements (e.g., GDPR 72-hour rule). The shorter 2-day window for widespread infringements demands pre-drafted notification templates and clear escalation paths. As of April 2026, mature IR programs are pre-authoring three Article 73 templates (15-day, 10-day, 2-day) and rehearsing them in tabletop drills, because the 2-day variant rarely leaves time for a blank-page drafting cycle once counsel, engineering, and leadership are in the loop.

### Real-World AI Security Incidents Informing IR Planning

As of March 2026, several high-profile incidents illustrate why AI-specific IR playbooks are essential:

- **Microsoft Copilot EchoLeak (June 2025):** CVE-2025-32711 (CVSS 9.3 Critical) -- a zero-click prompt injection vulnerability that enabled automated data exfiltration from OneDrive, SharePoint, and Teams without any user interaction. Attackers sent emails with hidden instructions that Copilot processed silently. This incident demonstrated that prompt injection containment cannot rely on user awareness; automated input filtering and output gates are the first line of defense.
- **Varonis Reprompt (January 2026):** Varonis Threat Labs showed that a single Microsoft Copilot Personal link could preload instructions through the `q` URL parameter, bypass initial safeguards through repeated requests, and continue exfiltrating session data through server-driven follow-up prompts after the tab was closed. Microsoft patched the issue, and Varonis noted Microsoft 365 Copilot enterprise customers were not affected; the IR takeaway is to treat prefilled AI prompts and deep links as untrusted input and to preserve browser, URL, and outbound request telemetry during investigation.
- **Copilot Studio and Agentforce form-trigger attacks (April 2026):** Capsule Security research reported indirect prompt injection paths in Microsoft Copilot Studio and Salesforce Agentforce where public form content could steer agents into data exfiltration through legitimate workflow actions. These cases belong in tabletop exercises for any agent that reads web forms, CRM leads, support tickets, or SharePoint comments before invoking email, search, or data-access tools.
- **Amazon Q Developer VS Code extension (July 2025):** AWS assigned CVE-2025-8217 after malicious code was committed into the Amazon Q Developer VS Code extension release path through an over-scoped GitHub token. AWS reported that the injected code was inert because of a syntax error and instructed users to remove version 1.84.0 and upgrade to 1.85.0. Treat this as an AI supply-chain incident pattern: responders need extension inventory, marketplace removal, token rotation, and review of any agent instructions capable of filesystem or cloud-resource deletion.
- **GTG-1002 Campaign (November 2025):** Chinese state-sponsored actors weaponized AI coding tools to automate 80--90% of intrusion operations across approximately 30 organizations spanning tech, finance, and government sectors. The campaign handled reconnaissance, exploit development, credential harvesting, and lateral movement with minimal human oversight. IR teams had to scope blast radius across organizations that shared the same compromised toolchain.
- **Medical LLM Data Poisoning (January 2025):** Researchers from NYU, Washington University, and Columbia University demonstrated that injecting just 2,000 fake medical articles (costing approximately $5) increased harmful outputs by ~5% in large language models. Separately, Anthropic and the UK AI Safety Institute found that as few as 250 malicious documents can compromise a model, with models from 600M to 13B parameters equally vulnerable. The implication for IR: poisoning may be undetectable without baseline behavioral comparison, and the "incident window" may span the entire period since contaminated data entered the pipeline.
- **Shadow AI Breaches (2025, industry-wide):** 20% of organizations experienced breaches involving unauthorized AI tools, with costs averaging $670,000 higher than traditional breaches. 97% of AI-related breaches lacked basic access controls. This pattern requires IR playbooks to include shadow AI discovery and containment procedures.
- **Deepfake Fraud Wave (Q1 2025):** Over 160 reported incidents with losses exceeding $200M. Voice cloning requiring only 3--5 seconds of audio enabled social engineering attacks, with human detection accuracy for high-quality deepfakes at just 24.5%. IR teams must now consider AI-generated media as an attack vector requiring specialized detection tools.
- **McKinsey Lilli autonomous-agent breach (February 28, 2026):** An autonomous AI agent called CodeWall exploited 22 unauthenticated API endpoints and a SQL injection flaw on McKinsey's internal AI platform, exfiltrating 46.5 million plaintext chat messages, 728,000 confidential files, 57,000 user accounts, 3.68 million RAG document chunks, and 95 writable system prompts. The critical IR finding was that the attacker could have silently poisoned responses firm-wide by modifying system prompts without changing a line of code — demonstrating that prompts are now critical assets requiring integrity monitoring alongside model weights.
- **Sears Home Services chatbot data exposure (early March 2026):** Researcher Jeremiah Fowler discovered three unprotected databases with no passwords or encryption holding 3.7 million chatbot transcripts, 1.4 million audio recordings (some hours long), and over 4 TB of plaintext customer data including names, addresses, appliance details, and repair records. The pattern — "log everything for training, secure nothing" — is becoming common enough to warrant a distinct IR archetype: chatbot corpus exposure, where the breach target is conversational telemetry rather than the model itself.
- **OpenAI / Axios HTTP supply-chain incident (April 2026):** OpenAI confirmed a security breach traced to a vulnerability in the widely used Axios HTTP library, reinforcing that AI vendor supply chains share the blast radius of mainstream JavaScript dependencies. IR playbooks must cover third-party library compromise of model-serving and agent-orchestration code paths.
- **Mexican government AI-accelerated intrusion (2026):** Researchers linked attacks on approximately ten Mexican government entities — including the tax authority, national electoral institute, a water utility, and a financial institution — to an intruder who used Claude and ChatGPT to accelerate reconnaissance, exploit development (at least 20 vulnerabilities), and data theft. Like GTG-1002, this campaign shows that AI tooling now compresses traditional kill-chain phases into minutes, shrinking IR reaction windows. Unit 42's **2026 Global Incident Response Report** (750+ engagements) corroborates this: the fastest observed breakout from initial access to data exfiltration was 72 minutes, four times faster than 2025.
- **Microsoft AI recommendation poisoning research (February 2026):** Microsoft Security documented how attackers manipulate AI agent memory at scale to profit — poisoned long-term memory in recommendation agents drove users toward attacker-controlled destinations without modifying the underlying model. IR playbooks should treat memory stores as distinct forensic objects with their own snapshotting, rollback, and chain-of-custody procedures.

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

### Emerging Threat: Stateful Memory Poisoning (MINJA and successors)

Memory poisoning turns transient prompt injection into a stateful attack: malicious instructions land in long-term memory and then steer every subsequent interaction without any further attacker activity. The **MINJA framework (2026)** achieves >95% injection success against production agents using zero elevated access, and standard LLM-based detection approaches miss approximately 66% of poisoned entries. Microsoft Security's February 2026 research on AI Recommendation Poisoning demonstrated that attackers can monetize this attack class by steering recommendation agents toward attacker-controlled destinations without touching model weights.

Practical IR implications:

- Memory stores need their own detection pipeline distinct from model-output monitoring; an attacker with memory write access may never trigger anomaly alerts on the model itself.
- Tabletop exercises should include late-detection scenarios (poisoning discovered weeks after compromise) so teams practice the "broad rollback vs. surgical cleanup" decision.
- Vendors and OSS frameworks (LangChain, LlamaIndex, LangGraph, CrewAI, AutoGen) are adding memory integrity features at different rates; as of April 2026 none provide defense-in-depth by default. IR teams should treat memory integrity as a compensating control they own, not something the framework provides.

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

- **NIST SP 800-61 Rev 3** -- Incident Response Recommendations and Considerations for Cybersecurity Risk Management, the current CSF 2.0-aligned foundation for incident response programs ([nist.gov](https://www.nist.gov/news-events/news/2025/04/nist-revises-sp-800-61-incident-response-recommendations-and-considerations))
- **NIST AI 100-1** -- AI Risk Management Framework, includes guidance on AI incident management
- **NIST Cybersecurity Framework Profile for AI (NIST IR 8596 preliminary draft)** -- Maps CSF 2.0 outcomes to securing AI systems, defending with AI, and thwarting AI-enabled attacks ([csrc.nist.gov](https://csrc.nist.gov/pubs/ir/8596/iprd))
- **CoSAI AI Incident Response Framework v1.0** -- AI-specific IR framework with OASIS CACAO playbooks ([coalitionforsecureai.org](https://www.coalitionforsecureai.org/defending-ai-systems-a-new-framework-for-incident-response-in-the-age-of-intelligent-technology/))
- **CISA JCDC AI Cybersecurity Collaboration Playbook (2025)** -- Cross-sector AI incident coordination ([cisa.gov](https://www.cisa.gov/sites/default/files/2025-01/JCDC%20AI%20Playbook.pdf))
- **MITRE ATLAS** -- Provides the attack taxonomy needed to structure AI-specific IR playbooks ([atlas.mitre.org](https://atlas.mitre.org/))
- **AI Incident Database** -- Collection of real-world AI incidents useful for tabletop exercise development ([incidentdatabase.ai](https://incidentdatabase.ai/))
- **OWASP GenAI Incident Response Guide v1.0 (2025)** -- Six-phase IR lifecycle for generative AI threats ([genai.owasp.org](https://genai.owasp.org/resource/genai-incident-response-guide-1-0/))
- **GenAI-IRF** -- Practical Incident-Response Framework for Generative AI Systems, six incident archetypes ([mdpi.com](https://www.mdpi.com/2624-800X/6/1/20))
- **MITRE ATLAS AI Incident Sharing** -- Anonymized real-world AI incident data sharing ([ai-incidents.mitre.org](https://ai-incidents.mitre.org/))
- **EU AI Act Article 73** -- Serious incident reporting obligations for high-risk AI systems ([artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/73/))
- **EU AI Act Article 55** -- GPAI systemic risk reporting obligations and Commission template ([digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/library/ai-act-commission-publishes-reporting-template-serious-incidents-involving-general-purpose-ai))
- **SANS FOR563** -- Applied AI for Digital Forensics and Incident Response ([sans.org](https://www.sans.org/cyber-security-courses/applied-ai-local-large-language-models))
- **FIRST CSIRT Services Framework** -- Incident response service descriptions adaptable for AI-specific capabilities
- **HiddenLayer AISec Platform 2.0** -- Runtime model monitoring, model genealogy, and AI Bill of Materials ([hiddenlayer.com](https://www.hiddenlayer.com/))
- **Protect AI Guardian** -- Model scanning across the AI lifecycle, acquired by Palo Alto Networks July 2025 ([protectai.com](https://protectai.com/guardian))
- **ModelScan** -- Open-source ML model scanner for serialization attacks ([github.com/protectai/modelscan](https://github.com/protectai/modelscan))
- **ISO/IEC 42001** -- AI Management System standard, Annex A Control 8.4 covers AI incident management; 40--50% process overlap with NIST AI RMF ([iso.org](https://www.iso.org/standard/81230.html))
- **ISACA: Lessons Learned from Top 2025 AI Incidents** -- Governance analysis of major 2025 AI failures ([isaca.org](https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2025/avoiding-ai-pitfalls-in-2026-lessons-learned-from-top-2025-incidents))
- **DoD/NSA AI/ML Supply Chain Risks and Mitigations (March 2026)** -- US defense guidance on AI supply chain incident scenarios ([media.defense.gov](https://media.defense.gov/2026/Mar/04/2003882809/-1/-1/0/AI_ML_SUPPLY_CHAIN_RISKS_AND_MITIGATIONS.PDF))
- **European Commission draft guidance on Article 73 serious incident reporting (September 2025)** -- Clarifies 2/10/15-day tiers and non-alteration obligations ([lw.com](https://www.lw.com/en/insights/european-commission-publishes-draft-guidance-reporting-serious-ai-incidents))
- **MITRE ATLAS Data v5.6.0 (May 2026)** -- Current ATLAS tactics, techniques, mitigations, and case-study data, including agent tool-abuse techniques such as AML.T0096 and AML.T0101 ([github.com/mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data))
- **Varonis Reprompt (January 2026)** -- Single-click Copilot Personal prompt-injection and data-exfiltration research ([varonis.com](https://www.varonis.com/blog/reprompt))
- **Capsule Security ShareLeak and PipeLeak (April 2026)** -- Form-triggered prompt injection paths in Microsoft Copilot Studio and Salesforce Agentforce ([venturebeat.com](https://venturebeat.com/security/microsoft-salesforce-copilot-agentforce-prompt-injection-cve-agent-remediation-playbook))
- **AWS Security Bulletin AWS-2025-015** -- Amazon Q Developer VS Code extension CVE-2025-8217 response and upgrade guidance ([aws.amazon.com](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/))
- **MITRE OpenClaw Investigation (February 2026, report PR-26-00176-1)** -- Maps AI agent incident patterns to ATLAS TTPs and identifies chokepoint techniques ([ctid.mitre.org](https://ctid.mitre.org/blog/2026/02/09/mitre-atlas-openclaw-investigation/))
- **GLACIS AI Incident Response Playbook (2026)** -- Containment matrix, severity-based response, model-rollback guidance ([glacis.io](https://www.glacis.io/guide-ai-incident-response))
- **OWASP Agent Memory Guard** -- Memory snapshot + rollback reference implementation for ASI06 Memory & Context Poisoning ([owasp.org](https://owasp.org/www-project-agent-memory-guard/))
- **OWASP Agentic Skills Top 10 Incident Response Playbook** -- Severity classification (CRITICAL/HIGH/MEDIUM/LOW with 1h/4h/1d/1w response targets) and containment templates for malicious skills, data breach via skill, and supply chain attacks ([owasp.org](https://owasp.org/www-project-agentic-skills-top-10/incident-response))
- **Unit 42 Global Incident Response Report 2026 (Palo Alto Networks)** -- 750+ engagements, 4x attack acceleration, 72-minute breakout, 90% identity involvement ([paloaltonetworks.com](https://www.paloaltonetworks.com/resources/research/unit-42-incident-response-report))
- **Microsoft Security: AI Recommendation Poisoning (February 2026)** -- Research on monetizing memory poisoning in recommendation agents ([microsoft.com](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/))
- **Wharton Accountable AI Lab: Two Early 2026 AI Exposures** -- Analysis of Sears and McKinsey Lilli breaches ([ai-analytics.wharton.upenn.edu](https://ai-analytics.wharton.upenn.edu/wharton-accountable-ai-lab/two-early-2026-ai-exposures-lessons-for-the-future-of-ai-and-data-governance/))

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
- How should IR teams reconcile the EU AI Act Article 73 non-alteration clause with the attacker speed observed in Unit 42's 2026 data (72-minute breakout, 4x faster than 2025)? Pausing to notify the competent authority before rolling back a compromised model trades regulatory exposure for dwell time, and current guidance does not crisply resolve that tradeoff.
- What is the appropriate retention policy for per-write memory snapshots in agentic systems? OWASP Agent Memory Guard enables snapshotting, but high-traffic agents may generate millions of writes per day; practitioners need better guidance on time-window trimming, compression, and when rollback granularity stops being useful.
- Are system prompts critical assets requiring the same integrity controls as code or model weights? The McKinsey Lilli incident (46.5M messages, 95 writable prompts) argues yes, but most organizations still treat prompts as editable configuration without signed history or review gates.

---

## Related Pages

- [C07-04-Explainability-Transparency](../C07-Model-Behavior/C07-04-Explainability-Transparency.md) — Interpretability traces and audit evidence help investigators explain why a suspect model behaved differently during an incident.
- [C07-05-Generative-Media-Safeguards](../C07-Model-Behavior/C07-05-Generative-Media-Safeguards.md) — Deepfake and synthetic-media controls feed IR scenarios where generated audio, video, or images are part of the attack.
- [C11-02-Adversarial-Example-Hardening](../C11-Adversarial-Robustness/C11-02-Adversarial-Example-Hardening.md) — Adversarial testing and hardening results give responders the baselines they need when investigating model manipulation.
- [C11-08-Agent-Security-Self-Assessment](../C11-Adversarial-Robustness/C11-08-Agent-Security-Self-Assessment.md) — Agent self-assessment evidence helps scope whether tool-use safeguards failed before an incident reached containment.
- [C11-10-Adversarial-Bias-Exploitation-Defense](../C11-Adversarial-Robustness/C11-10-Adversarial-Bias-Exploitation-Defense.md) — Bias exploitation and guardrail-evasion tests are useful post-incident checks after abuse of safety classifiers or policy filters.

---
