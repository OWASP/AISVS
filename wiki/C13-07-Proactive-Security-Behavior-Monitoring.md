# C13.7: Proactive Security Behavior Monitoring

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 5 (13.7.1 -- 13.7.5)

## Purpose

This section addresses the monitoring and security validation of proactive agent behaviors -- actions that AI agents initiate autonomously rather than in direct response to user instructions. As AI systems gain more autonomy (scheduling tasks, initiating communications, making decisions without explicit prompts), the security surface expands significantly. Proactive behaviors introduce risks that reactive monitoring cannot catch: an agent may take harmful actions that appear individually benign, operate outside expected contexts, or exhibit compromised behavior through subtle changes in its autonomous patterns.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **13.7.1** | **Verify that** proactive agent behaviors are security-validated before execution with risk assessment integration. | 1 | Autonomous agents executing harmful actions without pre-execution security checks; proactive behaviors bypassing safety controls designed for user-initiated actions; agents acting on compromised or stale context without validation. | Review the pre-execution validation pipeline for proactive actions. Verify risk assessment scoring is applied before execution. Test with proactive actions of varying risk levels and confirm appropriate gating. Verify that validation failures are logged and alerted. | Pre-execution validation for proactive behaviors should include: (1) action classification against a risk taxonomy, (2) context validation (is the triggering context still valid?), (3) scope verification (is this action within the agent's authorized scope?), (4) conflict detection (does this action conflict with other pending actions?). This is a runtime control, not just a monitoring control -- it bridges C09 (Orchestration) and C13. |
| **13.7.2** | **Verify that** autonomous initiative triggers include security context evaluation and threat landscape assessment. | 2 | Agents initiating actions based on adversarially manipulated triggers; proactive behaviors triggered by poisoned data or compromised external signals; agents operating without awareness of current threat conditions (e.g., during an active attack). | Review trigger evaluation logic for proactive behaviors. Verify that trigger inputs are validated and authenticated. Test with manipulated triggers and verify rejection. Confirm threat context integration (e.g., suppressing proactive actions during active incident response). | Proactive triggers may come from: scheduled timers, external events (webhooks, data changes), other agents, or model-internal reasoning. Each trigger source has different trust properties and attack surfaces. During active security incidents, proactive behaviors should be suppressed or elevated to require human approval to prevent compromised agents from taking autonomous actions. |
| **13.7.3** | **Verify that** proactive behavior patterns are analyzed for potential security implications and unintended consequences. | 2 | Emergent harmful behavior patterns not visible in individual action analysis; unintended consequences from sequences of individually safe proactive actions; agents developing unexpected behavioral patterns through reinforcement or feedback loops. | Review analysis methodology for proactive behavior patterns. Verify temporal analysis across action sequences. Test with sequences of individually benign but collectively problematic actions. Confirm pattern analysis reports are reviewed by security personnel. | Pattern analysis should consider: (1) action frequency trends (is the agent becoming more active?), (2) scope creep (is the agent expanding its action types?), (3) target patterns (is the agent consistently targeting specific resources or users?), (4) timing patterns (is the agent acting during unusual hours?). This overlaps with UEBA (User and Entity Behavior Analytics) applied to AI agents rather than human users. |
| **13.7.4** | **Verify that** audit logs capture the complete approval chain for security-critical proactive actions, including approver identity, timestamp, action parameters, and decision outcome. | 3 | High-impact autonomous actions taken without human oversight; compromised agents executing privileged operations; inability to attribute responsibility for autonomous agent decisions. | Identify the classification of "security-critical" proactive actions. Verify approval chain implementation (human-in-the-loop for critical actions). Test that critical actions are blocked pending approval. Verify audit trail completeness (who approved, when, with what context). Confirm timeout behavior for unapproved actions. | Defining "security-critical" is the key challenge. Criteria may include: (1) actions that modify security configurations, (2) actions that access sensitive data, (3) actions that communicate with external systems, (4) actions that exceed cost thresholds, (5) actions that affect other users or agents. The approval mechanism should be lightweight enough to not defeat the purpose of proactive behavior. |
| **13.7.5** | **Verify that** behavioral anomaly detection identifies deviations in proactive agent patterns that may indicate compromise. | 3 | Compromised agents exhibiting subtly altered proactive behavior (different action types, targets, or frequencies); backdoored agents activating on specific triggers; slow-acting compromises that gradually shift agent behavior over time. | Establish baseline proactive behavior profiles per agent. Simulate behavioral deviations (changed action frequency, new action types, altered targets). Verify anomaly detection identifies deviations. Test with both sudden and gradual behavioral shifts. Review false positive rates. | This is UEBA for AI agents. Baseline profiles should capture: (1) typical action types and frequencies, (2) normal operating hours, (3) expected target resources, (4) typical action outcomes. Anomaly detection methods: statistical process control (SPC) charts on action metrics, isolation forests on behavioral feature vectors, or rule-based deviation detection. Detection of gradual shifts requires long-term baseline comparison (weeks/months). |

---

## Implementation Guidance

### Incident Data and Threat Landscape (as of March 2026)

The scale of agent-related security incidents has grown dramatically. CrowdStrike and Mandiant data from 2025--early 2026 indicate that **1 in 8 enterprise security breaches now involves an agentic system**, with agent-involved breach incidents growing 340% year-over-year between 2024 and 2025. IBM's 2025 Cost of a Data Breach Report found that shadow AI breaches (including unauthorized agent deployments) average **$4.63 million per incident** -- $670K more than standard breaches.

Several high-profile incidents illustrate the speed and cascading nature of agent compromise:

- **McKinsey "Lilli" red-team exercise**: In a controlled red-team engagement, an autonomous agent compromised McKinsey's internal AI platform "Lilli," gaining broad system access in under two hours. The speed of lateral movement underscored that traditional detection cycles (hours to days) are inadequate for agentic threats.
- **Galileo AI cascading compromise study (December 2025)**: In multi-agent systems, a single compromised agent poisoned 87% of downstream decision-making within four hours. This finding has direct implications for 13.7.3 (pattern analysis) and 13.7.5 (anomaly detection) -- monitoring individual agent behavior in isolation is insufficient when compromise propagates through inter-agent communication channels.
- **Dark Reading industry poll (2026)**: 48% of cybersecurity professionals identify agentic AI as the single most dangerous attack vector, ahead of supply chain and ransomware.

Despite these risks, visibility remains poor: 80% of organizations report risky agent behaviors (unauthorized system access, improper data exposure), but only 21% of executives report complete visibility into agent permissions, tool usage, or data access patterns. Detecting compromised agent behavior requires action-level logging, behavioral baselining, and anomaly detection on semantic patterns -- capabilities that most enterprise security stacks do not yet have.

### Proactive AI Security Monitoring Landscape (2024--2026)

The security industry is undergoing a significant shift toward proactive, AI-augmented defense capabilities that are directly relevant to monitoring autonomous AI agents:

**Behavioral Anomaly Detection for AI Agents.** Applying User and Entity Behavior Analytics (UEBA) principles to AI agents requires establishing behavioral baselines that capture:

- Typical action types and their frequencies per agent
- Normal operating time windows and trigger patterns
- Expected target resources and interaction partners
- Typical action outcomes and error rates
- Token consumption patterns and cost profiles

Research and industry practice (2025--2026) indicate that behavioral baselines require **60--90 days of data collection** before anomaly detection becomes reliable. Organizations that begin baseline establishment should expect a maturation period before proactive hunting capabilities become effective. This timeline has implications for 13.7.5 -- newly deployed agents will have a vulnerability window during baseline establishment where behavioral anomalies cannot be reliably detected.

**Anomaly Detection Methods for Agent Behavior:**

| Method | Strengths | Limitations |
|--------|-----------|-------------|
| Statistical Process Control (SPC) charts | Simple, interpretable, low false-positive rates for stable behaviors | Struggles with legitimately evolving agent behavior |
| Isolation Forests | Effective for high-dimensional behavioral feature vectors | Requires careful feature engineering; opaque decisions |
| Rule-based deviation detection | Precise, auditable, no training period needed | Cannot detect novel anomaly patterns |
| Sequence-based models (LSTM/Transformer) | Can detect complex temporal patterns in action sequences | Requires substantial training data; expensive to maintain |
| LSTM autoencoder networks | Learn API call sequences and authentication patterns; flag high reconstruction errors (95th--99.9th percentile) | Requires representative training data; threshold tuning needed |
| Graph-based access pattern analysis | Captures inter-agent relationships and lateral movement patterns | Computationally expensive at scale; graph construction is non-trivial |

### Agent Behavior Analytics: Industry Tooling (as of early 2026)

The monitoring gap for AI agents is closing. Traditional SIEM and EDR tools were built for human behavioral patterns -- an agent executing code perfectly 10,000 times in sequence looks normal to these systems, even if it is executing an attacker's instructions. Several vendors are now shipping agent-aware detection capabilities:

**Exabeam Agent Behavior Analytics (ABA).** Released January 2026, this is the first SIEM vendor to deliver behavioral analytics specifically designed for AI agent activity. ABA extends the UEBA foundation to treat agents as autonomous entities, tracking queries, tool calls, automations, and updates in rapid succession. The core detection mechanism uses a session-based data model rather than isolated event analysis -- connecting related activity into a single narrative and preserving the full history of what happened. This is critical because agent misuse manifests as patterns across sequences (prompt → tool call → data access → action → output → repeat) rather than single anomalous events. Specific detections include abnormal guardrail violation counts, first-time guardrail violations per user/org/department, and guardrail violation observation trending.

**Microsoft AI Observability.** As of March 2026, Microsoft is building out observability for AI systems spanning functionality, operations, security, compliance, and human factors. Their approach emphasizes proactive risk detection rather than reactive log review, with Microsoft Agent 365 (GA expected May 2026) providing a control plane for agent visibility, security, and governance at scale.

**Cisco AI Defense.** Expanded in February 2026 to add runtime protections against tool abuse and supply chain manipulation at the MCP layer, addressing the execution-layer gap in agent monitoring.

**Non-Human Identity (NHI) Monitoring.** The definition of "insider" is expanding beyond human users to include service accounts and AI agents. As of 2026, the UEBA market is valued at approximately $4.27 billion (growing at 33.8% CAGR), with 40% of organizations now using AI-enhanced UEBA capabilities. Microsoft Entra ID Protection establishes observation periods from 2 to 60 days for non-human identities, profiling IP addresses, autonomous system numbers, user agents, credential types, and geographic locations for service principals and managed identities.

### Seven Detection Methods for Non-Human Identities

Research published in early 2026 identifies seven proven approaches for detecting compromised AI agent credentials and rogue agent behavior, which map well to 13.7.5 requirements:

1. **Statistical & ML hybrid models** -- AWS CloudWatch Anomaly Detection analyzes up to two weeks of historical metric data to create behavioral baselines. Carnegie Mellon SEI research demonstrates statistical process control using exponentially weighted moving averages to detect subtle reconnaissance patterns.
2. **Behavioral baseline learning** -- Observation periods ranging from 2 to 60 days, profiling authentication patterns, API usage, and geographic patterns per agent identity.
3. **UEBA with peer group comparison** -- Three-dimensional profiles: individual entity baselines, peer group comparisons, and temporal patterns. Reduces false positives by detecting deviations relative to similar workload cohorts.
4. **Cloud-native metrics monitoring** -- Identity-aware telemetry with high-cardinality labels, Random Cut Forest algorithms for dynamic thresholding, distributed tracing for contextual anomalies (e.g., sudden cross-region data transfers).
5. **Real-time event stream analysis** -- Google Cloud Event Threat Detection combines signature-based detection, ML-based anomaly detection, and rule-based analysis on Cloud Logging streams.
6. **Temporal sequence analysis** -- LSTM autoencoder networks learn API call sequences and authentication patterns, flagging high reconstruction errors at the 95th--99.9th percentile as anomalous.
7. **Graph-based access pattern analysis** -- Maps inter-agent relationships and resource access patterns, detecting lateral movement and influence propagation in multi-agent systems.

The core challenge: agent identities authenticate successfully with legitimate credentials, operating within authorized permissions while blending into normal traffic. Unlike humans showing suspicious login locations, a compromised agent remains inconspicuous unless its behavioral patterns deviate significantly. Human-focused identity tools struggle with short-lived credentials (hours vs. days), dynamic scaling events, and agents exhibiting non-deterministic behaviors based on learned probability distributions.

### AI Honeypots and Deception Technology

An emerging area directly relevant to proactive monitoring of AI systems is the adaptation of deception technology for AI contexts:

**Traditional honeypots adapted for AI systems.** Research published in 2025 demonstrates the use of honeypot-style systems (building on frameworks like the Cowrie honeypot) to lure attackers targeting AI endpoints and collect behavioral data that enhances detection capabilities. These systems capture indicators of compromise (IOCs) and attack patterns that production monitoring may miss.

**AI-specific deception approaches include:**

1. **Decoy model endpoints** that appear to be production AI APIs but are monitored for model extraction attempts, systematic probing, and prompt injection campaigns. These complement 13.7.1 (pre-execution validation) by providing an early warning layer.
2. **Canary prompts and responses** injected into agent memory or knowledge bases that, if surfaced in outputs, indicate unauthorized access to internal data stores or memory poisoning.
3. **Synthetic agent identities** in multi-agent systems that appear as legitimate peer agents but monitor for attempts by compromised agents to influence or recruit other agents.

### MITRE ATLAS Agentic Techniques (2025--2026 Updates)

In October 2025, MITRE ATLAS (which as of that release contained 15 tactics, 66 techniques, and 46 sub-techniques) integrated 14 new attack techniques and sub-techniques specifically focused on AI agents and generative AI systems, developed in collaboration with Zenity Labs. These are directly relevant to what 13.7.3 and 13.7.5 should be detecting:

- **AML.T0098 -- AI Agent Tool Credential Harvesting**: Adversaries use their access to an agent's LLM to collect credentials stored in internal documents inadvertently ingested into RAG databases or agent-accessible tools like SharePoint and OneDrive.
- **AML.T0099 -- AI Agent Tool Data Poisoning**: Attackers place malicious or inaccurate content in agent-accessible data stores to hijack agent behavior -- a trigger manipulation attack relevant to 13.7.2.
- **AML.T0100 -- AI Agent Clickbait**: Agents are manipulated through hidden instructions embedded in HTML or metadata, causing them to perform unintended actions -- a variant of indirect prompt injection targeting autonomous behavior.
- **AML.T0101 -- Data Destruction via AI Agent Tool Invocation**: Attackers leverage agent tool capabilities to destroy data and disrupt systems -- exactly the kind of high-impact action that 13.7.4 approval chains should gate.
- **AML.T0096 -- AI Service API**: Exploitation of AI service APIs as part of broader attack chains, including command and control operations.
- **AML.CS0042 -- SesameOp**: A documented case study of a backdoor using the OpenAI Assistants API for covert command and control, demonstrating real-world agent compromise.

Additional agent-specific attack patterns documented include AI Agent Context Poisoning (manipulating the context used by an agent's LLM to persistently influence its responses), Memory Manipulation (altering long-term memory to ensure malicious changes persist across sessions), Thread Injection (introducing malicious instructions into specific chat threads), and Modify AI Agent Configuration (changing agent configuration files to create persistent malicious behavior across all agents sharing that config).

### NIST AI Agent Standards Initiative (February 2026)

NIST's Center for AI Standards and Innovation (CAISI) launched the AI Agent Standards Initiative in February 2026, focusing on three pillars directly relevant to proactive behavior monitoring:

1. **Identity and authorization infrastructure** -- Establishing how existing identity standards apply to agent-to-agent and human-to-agent interactions. An NCCoE concept paper on "Software and AI Agent Identity and Authorization" (comments closed April 2, 2026) addresses JWT-based delegation chain authorization with diminishing permissions -- relevant to 13.7.4's approval chain requirements.
2. **Interoperable agent protocols** -- Standardizing how agents communicate and authenticate with each other, with NSF funding open-source ecosystems through its Pathways program.
3. **Agent security research** -- Fundamental research into agent authentication, identity infrastructure, and secure multi-agent interactions.

The initiative emphasizes that every decision and action of an agent must be reconstructable -- audit logs must record not only "what was done" but "why it was done," including the agent's reasoning process, referenced data sources, communications with other agents, and rejected alternatives. This maps directly to 13.7.4's audit trail requirements.

As of March 2026, compliance remains a challenge: only 14.4% of organizations report their AI agents go live with full security approval (per the Gravitee State of AI Agent Security 2026 Report), meaning the vast majority of agents launch without complete oversight.

### Agentic AI Threat Hunting (2025--2026)

The threat hunting discipline is evolving to address AI-specific concerns. Key developments:

**Autonomous threat hunting agents.** Tools like Dropzone AI's AI Threat Hunter (announced March 2026, GA expected Summer 2026) represent the next generation of proactive security: AI agents that continuously hunt for threats across environments. This creates a recursive security challenge -- the threat hunting AI agent itself must be monitored for compromise (applying 13.7.5 to security tooling).

**AI-specific threat hunting hypotheses** that security teams should investigate proactively:

- **Behavioral drift as compromise indicator**: Is an agent's action distribution shifting in ways not explained by legitimate updates or changing inputs? (Connects to 13.7.3 and 13.7.5)
- **Privilege escalation through tool discovery**: Is an agent discovering and using tools or API endpoints beyond its documented scope? This may indicate prompt injection or jailbreaking of the agent's system instructions.
- **Data exfiltration through normal operations**: Is an agent encoding sensitive information in its normal outputs (covert channels through AI responses, connecting to C13.2.10)?
- **Inter-agent influence campaigns**: In multi-agent systems, is one agent systematically influencing other agents' behavior through shared memory, message passing, or tool invocation patterns?

**Threat hunting cadence for AI systems**: Given the speed at which AI agents operate, traditional weekly or monthly threat hunting cycles are insufficient. Automated hypothesis-driven hunts should run continuously, with human-led deep-dive investigations triggered by automated findings.

**AI-assisted cyber attack trends**: AI-assisted cyber attacks surged 72% in 2025. Tool misuse and privilege escalation remain the most common agentic AI incidents (520 incidents reported), but memory poisoning and supply chain attacks carry disproportionate severity and persistence risk despite lower frequency.

### AI Runtime Security Tooling for Pre-Execution Validation (as of March 2026)

A new category of AI runtime security tools has emerged that directly supports 13.7.1's pre-execution validation requirement. Unlike traditional observability platforms that focus on post-hoc analysis, these tools enforce security policy at the moment of execution:

**F5 AI Guardrails (formerly CalypsoAI Inference Defend).** F5 completed its acquisition of CalypsoAI in March 2026, delivering real-time protection at the inference layer. AI Guardrails blocks prompt injection, jailbreaks, and data exfiltration at execution time. The companion product F5 AI Red Team deploys autonomous agent swarms simulating thousands of attack patterns, drawing from a vulnerability database updated with over 10,000 new attack patterns each month. "Agentic Fingerprints" provide granular insight into every AI interaction with detailed reasoning for why a prompt was accepted or blocked -- directly relevant to 13.7.1 audit requirements.

**Lasso Security AI Runtime Platform.** Lasso integrates offensive red-teaming with defensive runtime enforcement, continuously validating that agents operate within their intended scope. The Lasso--Portkey integration embeds security controls directly into the MCP Gateway request pipeline, with every tool call, data exchange, and agent-to-server interaction passing through protection with sub-50ms latency overhead. Key capabilities include inline enforcement (deterministic prevention in request/response paths), behavioral pattern analysis across sessions for goal drift detection, and automated response options (blocking outputs, restricting tool access, triggering review).

**Microsoft Defender for AI Agents.** In Microsoft Copilot Studio, Defender performs real-time security checks at tool invocation time, determining whether each action should be allowed or blocked before execution. Combined with Microsoft Entra for identity governance and Microsoft Agent 365 (GA expected May 2026) for agent lifecycle management, this creates an integrated pre-execution validation chain. Microsoft's March 2026 RSA Conference presentation outlined end-to-end coverage from pre-deployment through runtime monitoring.

**Galileo AI.** Galileo provides configurable rules, rulesets, and stages that block unsafe outputs before execution. Dedicated agentic metrics (Action Advancement, Tool Selection Quality, Agent Efficiency) enable security teams to detect behavioral anomalies without manual trace review. Confidence thresholds with automated escalation support human-in-the-loop approval for high-risk decisions (relevant to 13.7.4).

**Arize AI / Phoenix.** Built on the OpenInference standard (OpenTelemetry-based), Arize provides production-scale behavioral assessment with LLM-as-Judge evaluation frameworks and drift detection from its ML observability heritage. Agent Graph visualization shows exactly which step in an agent workflow broke and why, supporting forensic analysis of proactive behavior failures.

The architectural distinction that matters for implementation: **inline enforcement** (controls in the request/response path) provides deterministic prevention and is appropriate for high-risk proactive actions, while **out-of-band enforcement** (asynchronous observation via logs/traces) is primarily detective and allows post-action intervention. Most production deployments will need both modes operating simultaneously.

### Pre-Execution Validation Pipeline

Implementing 13.7.1 effectively requires a structured validation pipeline for proactive agent actions:

1. **Action classification**: Categorize the proposed action against a risk taxonomy (read-only vs. write, internal vs. external, cost implications).
2. **Context validation**: Verify that the triggering context is still valid and has not been tampered with. Stale context is a common source of unintended proactive actions.
3. **Scope verification**: Confirm the action falls within the agent's authorized scope as defined in its governance policy (C09).
4. **Conflict detection**: Check whether the proposed action conflicts with other pending actions, active incidents, or current threat conditions.
5. **Threat context integration**: During active security incidents, suppress or elevate proactive behaviors to require human approval to prevent compromised agents from taking autonomous actions while IR is in progress.

### OWASP AI Agent Security Cheat Sheet Guidance

The OWASP AI Agent Security Cheat Sheet (published 2025, maintained at [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)) provides concrete thresholds and patterns directly applicable to implementing C13.7 requirements:

- **Risk-tiered action classification** (13.7.1, 13.7.4): Classify actions as Low, Medium, High, or Critical risk. Auto-approve only low-risk operations; escalate Medium and above for review. Require explicit user confirmation before irreversible actions (deletions, financial transfers, configuration changes).
- **Circuit breaker pattern** (13.7.5): Implement circuit breakers that halt agents showing anomalous behavior. Monitor tool call frequency and flag when calls exceed 30 per minute as a potential indicator of runaway or compromised behavior.
- **Denial-of-wallet detection** (13.7.3): Track token usage and costs per session and per user to detect resource abuse patterns where compromised agents consume excessive compute.
- **Memory integrity verification** (13.7.2): Store checksums and cryptographic signatures for agent memory, enabling detection of memory poisoning attacks that could manipulate proactive behavior triggers.
- **Inter-agent communication sanitization**: Verify tool calls against allowlists, sanitize inter-agent communications with signature verification, and filter outputs for PII and sensitive data leakage.

### Compliance Timeline: EU AI Act and Agent Oversight

The EU AI Act's high-risk AI requirements become fully enforceable on **August 2, 2026**. Article 14 mandates effective human oversight for high-risk AI systems, which has direct implications for 13.7.4 (approval chains):

- **Mandatory risk assessments** before deployment of autonomous agents in high-risk categories
- **Logging obligations and auditability** -- audit trails must include timestamps, decision rationale, tool usage history with parameters, policy compliance check results, and identity mapping linking agents to human owners
- **Human oversight mechanisms** for autonomous workflows, with proven robustness and cybersecurity controls
- **Boundary enforcement** -- agents must not exceed authorized operational boundaries

The OECD AI Principles further reinforce accountability for autonomous actions and transparency in decision-making. ISO 42001 (AI Management System) provides the organizational framework for implementing these requirements systematically.

As of March 2026, the compliance gap remains significant: per the Gravitee State of AI Agent Security 2026 Report, only 14.4% of organizations deploy agents with full security approval, and only 21% of executives have complete visibility into agent permissions and data access patterns. The practical implication is that most organizations will need to retrofit proactive monitoring capabilities onto already-deployed agents rather than building them in from scratch.

---

## Related Standards & References

- **NIST AI 100-1 Section GOVERN 1.7** -- Discusses autonomous system monitoring and oversight requirements
- **NIST AI Agent Standards Initiative (February 2026)** -- Three-pillar framework covering identity/authorization, interoperable protocols, and agent security research ([nist.gov](https://www.nist.gov/caisi/ai-agent-standards-initiative))
- **MITRE ATLAS TA0040 (ML Attack Staging)** -- Relevant to detecting compromised agent behavior patterns
- **MITRE ATLAS 2025--2026 Agentic Techniques** -- 14 new techniques for AI agent attacks including AML.T0098 (Tool Credential Harvesting), AML.T0099 (Tool Data Poisoning), AML.T0100 (Agent Clickbait), AML.T0101 (Data Destruction via Tool Invocation) ([zenity.io](https://zenity.io/blog/current-events/mitre-atlas-ai-security))
- **IEEE 7001-2021** -- Transparency of Autonomous Systems, relevant to audit trail requirements
- **OWASP Top 10 Risks for Agentic Applications (December 2025)** -- Identifies tool misuse, prompt injection, and data leakage as primary agentic AI threats
- **Exabeam Agent Behavior Analytics (January 2026)** -- First SIEM vendor with behavioral analytics for AI agent activity, session-based detection model ([exabeam.com](https://www.exabeam.com/blog/siem-trends/exabeam-agent-behavior-analytics-first-of-its-kind-behavioral-detections-for-ai-agents/))
- **Microsoft Agent 365 (GA May 2026)** -- Control plane for agent visibility, security, and governance at scale
- **Cisco AI Defense (February 2026)** -- Runtime protections against tool abuse and supply chain manipulation at the MCP layer
- **UEBA (User and Entity Behavior Analytics)** -- Established discipline applicable to agent behavior monitoring (Exabeam, Microsoft Sentinel UEBA, Microsoft Entra ID Protection)
- **AISVS C09 (Orchestration and Agents)** -- Defines the agent governance controls that C13.8 monitors
- **Anomaly Detection for Non-Human Identities (January 2026)** -- Seven detection methods for catching rogue workloads and AI agents ([securityboulevard.com](https://securityboulevard.com/2026/01/anomaly-detection-for-non-human-identities-catching-rogue-workloads-and-ai-agents/))
- **Dropzone AI Threat Hunter** -- Autonomous threat hunting agent for continuous SOC detection ([helpnetsecurity.com](https://www.helpnetsecurity.com/2026/03/18/dropzone-ai-ai-threat-hunting/))
- **AI-Powered Intrusion Detection with Honeypot Integration (2025)** -- Research on adaptive honeypots for AI system defense ([sciencepublishinggroup.com](https://www.sciencepublishinggroup.com/article/10.11648/j.ijiis.20251404.11))
- **SecurityWeek: Threat Hunting in an Age of Automation and AI (2026)** -- Industry analysis of agentic AI threat hunting ([securityweek.com](https://www.securityweek.com/cyber-insights-2026-threat-hunting-in-an-age-of-automation-and-ai/))
- **Gravitee State of AI Agent Security 2026 Report** -- Only 14.4% of organizations deploy agents with full security approval
- **Bessemer Venture Partners: Securing AI Agents (2026)** -- Three-stage framework (visibility, configuration, runtime protection) for agent security ([bvp.com](https://www.bvp.com/atlas/securing-ai-agents-the-defining-cybersecurity-challenge-of-2026))
- **OWASP AI Agent Security Cheat Sheet** -- Concrete thresholds for risk-tiered classification, circuit breakers, and monitoring ([cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html))
- **F5 AI Guardrails (CalypsoAI, March 2026)** -- Inference-layer runtime protection with Agentic Fingerprints and autonomous red-teaming ([calypsoai.com](https://calypsoai.com/))
- **Lasso Security AI Runtime Platform** -- MCP Gateway integration with sub-50ms enforcement, behavioral drift detection ([lasso.security](https://www.lasso.security/blog/ai-runtime-security))
- **Galileo AI Agent Monitoring** -- Agentic metrics (Action Advancement, Tool Selection Quality), configurable runtime rules ([galileo.ai](https://galileo.ai/blog/best-agent-monitoring-tools-production))
- **Arize AI / Phoenix** -- OpenInference-based agent observability with drift detection and Agent Graph visualization ([arize.com](https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/))
- **Microsoft: Secure Agentic AI End-to-End (March 2026)** -- RSA Conference presentation on Defender + Entra + Agent 365 integration ([microsoft.com](https://www.microsoft.com/en-us/security/blog/2026/03/20/secure-agentic-ai-end-to-end/))
- **Token Security: Compliance and Audit Frameworks for Agentic AI** -- EU AI Act, NIST RMF, and OECD mapping for agent audit requirements ([token.security](https://www.token.security/blog/compliance-and-audit-frameworks-for-agentic-ai-systems))
- **IBM 2025 Cost of a Data Breach Report** -- Shadow AI breaches average $4.63M, $670K above standard breaches
- **Galileo AI Cascading Compromise Study (December 2025)** -- Single compromised agent poisons 87% of downstream decisions in 4 hours

---

## Open Research Questions

- How should "normal" proactive behavior baselines be established for agents whose behavior is expected to evolve and improve over time? The 60--90 day baseline establishment period creates a vulnerability window for newly deployed agents.
- What approval mechanisms provide adequate security without creating bottlenecks that negate the value of autonomous agent behavior? Lightweight approval mechanisms (e.g., risk-tiered auto-approval with audit) are needed but not yet standardized.
- Can UEBA models trained on human user behavior be adapted for AI agent behavior monitoring, or do agents require fundamentally different behavioral models? Agent behavior is higher-volume, more deterministic, and lacks the natural variability of human users -- existing UEBA may produce excessive false positives or miss subtle agent-specific anomalies.
- How should proactive behavior monitoring scale in multi-agent systems where agents interact and influence each other's behavior? Graph-based anomaly detection on agent interaction networks is a promising but immature approach.
- What is the minimum monitoring granularity needed to detect subtle agent compromise without generating excessive telemetry data? The trade-off between detection fidelity and telemetry cost is especially acute for high-throughput agentic systems.
- How should AI honeypots and deception technology be validated to ensure they do not interfere with legitimate agent operations or create false positive cascades?
- Who monitors the monitoring agents? Autonomous threat hunting AI (e.g., Dropzone AI Threat Hunter) introduces recursive trust challenges -- compromised monitoring agents could suppress detection of other compromised agents.
- How should organizations handle the compliance gap where only ~14% of agents launch with full security approval? Is pre-deployment security gating practical at the speed of agent adoption, or do we need runtime-first security models that assume agents will deploy without full vetting?
- How do the new MITRE ATLAS agentic techniques (AML.T0098--T0101) change the threat model for proactive behavior monitoring? Traditional anomaly detection may not catch attacks like Agent Clickbait (AML.T0100) where the agent behaves "normally" but is following adversarial instructions embedded in legitimate-looking content.
- Given that a single compromised agent can poison 87% of downstream decisions in four hours (Galileo AI, 2025), is per-agent behavioral monitoring sufficient, or do production multi-agent deployments require system-level anomaly detection that models inter-agent influence propagation as a first-class concern?
- How should organizations balance the latency cost of inline pre-execution validation (sub-50ms per tool call in current tooling) against the security benefit, particularly for high-throughput agentic workflows where accumulated latency may degrade user experience or time-sensitive operations?

---
