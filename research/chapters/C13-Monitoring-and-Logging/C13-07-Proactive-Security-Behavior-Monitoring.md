# C13.7: Proactive Security Behavior Monitoring

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 5 (13.7.1 -- 13.7.5)

## Purpose

This section addresses the monitoring and security validation of proactive agent behaviors -- actions that AI agents initiate autonomously rather than in direct response to user instructions. As AI systems gain more autonomy (scheduling tasks, initiating communications, making decisions without explicit prompts), the security surface expands significantly. Proactive behaviors introduce risks that reactive monitoring cannot catch: an agent may take harmful actions that appear individually benign, operate outside expected contexts, or exhibit compromised behavior through subtle changes in its autonomous patterns.

> **Scope note (from AISVS source):** C13.7 addresses monitoring and logging of proactive agent behaviors. 13.7.4 requires audit trail coverage for approval events on security-critical actions. The requirement to actually obtain approval before executing such actions is governed by **C9.2 (runtime execution gate)** and **C14.2 (oversight policy)**. Satisfying 13.7.4 therefore requires evidence that approval events are logged with sufficient detail -- not merely that approvals occur. Verification should look at both sides: the upstream gate (does the system block execution pending approval?) and the downstream log record (is every gating decision captured with approver identity, timestamp, inputs considered, and outcome?).

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

### Incident Data and Threat Landscape (as of April 2026)

The scale of agent-related security incidents has grown dramatically. CrowdStrike and Mandiant data from 2025--early 2026 indicate that **1 in 8 enterprise security breaches now involves an agentic system**, with agent-involved breach incidents growing 340% year-over-year between 2024 and 2025. HiddenLayer's 2026 AI Threat Landscape Report reaches the same "1 in 8" figure from a different dataset, suggesting the ratio is holding steady even as the denominator grows. IBM's 2025 Cost of a Data Breach Report found that shadow AI breaches (including unauthorized agent deployments) average **$4.63 million per incident** -- $670K more than standard breaches.

Several high-profile incidents illustrate the speed and cascading nature of agent compromise:

- **LiteLLM supply chain compromise (March 24, 2026)**: TeamPCP used exfiltrated credentials (harvested in late February 2026 via a misconfigured `pull_request_target` workflow in Trivy's CI) to publish backdoored LiteLLM wheels 1.82.7 and 1.82.8 to PyPI. The packages were live for roughly 40 minutes before quarantine, but LiteLLM's 95M monthly downloads and near-ubiquitous presence as a transitive dependency of MCP plugins, agent frameworks, and LLM orchestration tools meant that victims (including Mercor) were compromised **without ever running `pip install litellm`** -- the package was pulled in by an MCP plugin running inside Cursor. The payload was a three-stage credential stealer, Kubernetes lateral-movement tool, and persistent RCE backdoor. This incident is now catalogued in MITRE ATLAS as an Initial Access case study for ML software dependency compromise and is highly relevant to 13.7.2 (trigger integrity -- agents executing on compromised library code) and 13.7.5 (anomaly detection on agent tool-call patterns after the compromise window). See [Trend Micro analysis](https://www.trendmicro.com/en_us/research/26/c/inside-litellm-supply-chain-compromise.html), [LiteLLM security update](https://docs.litellm.ai/blog/security-update-march-2026), and [InfoQ reporting](https://www.infoq.com/news/2026/03/litellm-supply-chain-attack/).
- **McKinsey "Lilli" red-team exercise**: In a controlled red-team engagement, an autonomous agent compromised McKinsey's internal AI platform "Lilli," gaining broad system access in under two hours. The speed of lateral movement underscored that traditional detection cycles (hours to days) are inadequate for agentic threats.
- **Galileo AI cascading compromise study (December 2025)**: In multi-agent systems, a single compromised agent poisoned 87% of downstream decision-making within four hours. This finding has direct implications for 13.7.3 (pattern analysis) and 13.7.5 (anomaly detection) -- monitoring individual agent behavior in isolation is insufficient when compromise propagates through inter-agent communication channels.
- **Dark Reading industry poll (2026)**: 48% of cybersecurity professionals identify agentic AI as the single most dangerous attack vector, ahead of supply chain and ransomware.

The LiteLLM case is worth dwelling on: it is the first documented mass-production example where agent-framework telemetry (tool-call frequency, credential access patterns, outbound connections from agent workloads) would have been the single best detector. Network IDS and EDR did not catch the three-stage payload because it operated from within legitimate agent processes. Behavioural monitoring at the agent layer -- the core 13.7.3 and 13.7.5 capabilities -- is the only control that could have caught the deviation in time.

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

As of the **ATLAS v5.3.0 update (January 2026)**, the framework catalogues **16 tactics, 84 techniques, 56 sub-techniques, and 42 case studies** -- up from 15 tactics / 66 techniques / 46 sub-techniques at the October 2025 baseline. The January 2026 release specifically shifted focus from model-centric attacks to execution-layer exposure, adding three new case studies covering MCP server compromises, indirect prompt injection via MCP channels, and malicious AI agent deployment. A subsequent update in the first quarter of 2026, developed with Zenity Labs, added the following agent-focused techniques, all directly relevant to what 13.7.3 and 13.7.5 should be detecting:

- **AML.T0098 -- AI Agent Tool Credential Harvesting**: Adversaries use their access to an agent's LLM to collect credentials stored in internal documents inadvertently ingested into RAG databases or agent-accessible tools like SharePoint and OneDrive.
- **AML.T0099 -- AI Agent Tool Data Poisoning**: Attackers place malicious or inaccurate content in agent-accessible data stores to hijack agent behavior -- a trigger manipulation attack relevant to 13.7.2.
- **AML.T0100 -- AI Agent Clickbait**: A novel attack class targeting agentic browsers. Adversaries embed hidden instructions in HTML or page metadata, causing agents to execute unintended workflows like downloading malicious files. Particularly dangerous because the agent behaves "normally" from a telemetry perspective -- the anomaly is in the *source of the instruction*, not the action itself.
- **AML.T0101 -- Data Destruction via AI Agent Tool Invocation**: Attackers leverage agent tool capabilities to destroy data and disrupt systems -- exactly the kind of high-impact action that 13.7.4 approval chains should gate.
- **AML.T0096 -- AI Service API**: Exploitation of AI service APIs as part of broader attack chains, including command and control operations.
- **AML.CS0042 -- SesameOp**: A documented case study of a backdoor leveraging the OpenAI Assistants API for covert command and control, disguised as legitimate agent workflows.

Additional agent-specific attack patterns documented include AI Agent Context Poisoning (manipulating the context used by an agent's LLM to persistently influence its responses), Memory Manipulation (altering long-term memory to ensure malicious changes persist across sessions), Thread Injection (introducing malicious instructions into specific chat threads), and Modify AI Agent Configuration (changing agent configuration files to create persistent malicious behavior across all agents sharing that config).

The practical takeaway for verifiers: MITRE ATLAS 2026 has matured from a research taxonomy into a practical defensive checklist. For 13.7.3 pattern analysis, map each detection rule to one or more ATLAS technique IDs; gaps in the mapping are concrete coverage gaps. See the [Zenity analysis](https://zenity.io/blog/current-events/mitre-atlas-ai-security) and the [ATLAS matrix](https://atlas.mitre.org/).

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

### AI Runtime Security Tooling for Pre-Execution Validation (as of April 2026)

A new category of AI runtime security tools has emerged that directly supports 13.7.1's pre-execution validation requirement. Unlike traditional observability platforms that focus on post-hoc analysis, these tools enforce security policy at the moment of execution. The Q1 2026 vendor landscape has matured significantly, with three notable new entrants joining the established tools:

**Microsoft Agent Governance Toolkit (open-source, April 2, 2026).** Microsoft released the Agent Governance Toolkit as an open-source MIT-licensed project designed to be the first toolkit to address all ten OWASP agentic AI risks with deterministic enforcement. Its centrepiece is **Agent OS**, a stateless policy engine that intercepts every agent action before execution with advertised latency of **<0.1ms p99** -- fast enough to sit inline without noticeable overhead. Policies are written in YAML, OPA Rego, or Cedar. A companion component, **Agent Mesh**, maintains cryptographic agent identity and computes a 0--1000 trust score per agent that can be used to gate privileged actions (e.g., an agent whose trust score decays below a threshold is denied write tool access). Seven packages cover Agent OS (policy engine), Agent Mesh (identity/trust), Agent Runtime (execution rings and kill switches), Agent SRE (reliability), Agent Compliance (EU AI Act / HIPAA / SOC2 mapping), Agent Marketplace (plugin lifecycle with Ed25519 signing), and Agent Lightning (RL governance). SDKs are available in Python, TypeScript, Rust, Go, and .NET. This toolkit is directly usable as the enforcement substrate for 13.7.1 pre-execution validation and 13.7.4 approval audit. See [Microsoft Open Source Blog](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/).

**HiddenLayer Agentic Runtime Security (March 23, 2026).** HiddenLayer expanded its AI Runtime Security module with three agentic capabilities: (1) **Agentic Runtime Visibility** -- session reconstruction allowing auditors to trace every interaction between agents, data, and tools; (2) **Agentic Investigation & Threat Hunting** -- cross-session search to surface anomalous behaviour, with findings convertible into enforceable runtime policies; (3) **Agentic Detection & Enforcement** -- inline identification of prompt injection, malicious tool calls, data exfiltration, and cascading attack chains, with adaptive policies that block unauthorised actions. The explicit emphasis on "cascading attack chain" detection is notable because it aligns with the Galileo multi-agent cascading compromise finding -- HiddenLayer is one of the first runtime tools to treat cross-agent influence propagation as a first-class threat surface (13.7.3). CEO Chris Sestito framed the product around a specific gap: existing AI controls focus on prompts and policies, leaving "execution-time behavior" unobserved and uncontrolled. See [PR Newswire announcement](https://www.prnewswire.com/news-releases/hiddenlayer-unveils-new-agentic-runtime-security-capabilities-for-securing-autonomous-ai-execution-302721517.html).

**Qualys Agent Val (March 23, 2026).** Integrated into Qualys Enterprise TruRisk Management, Agent Val delivers a closed-loop "validate, mitigate, revalidate" workflow for AI agents. Distinct from the pure detection tools, it emphasises *proven* risk reduction -- every mitigation is re-tested automatically and reopened if the agent reintroduces the behaviour. Directly relevant to 13.7.3 (pattern analysis) and 13.7.5 (deviation detection) because the validation loop itself becomes a source of behavioural baseline data.

**F5 AI Guardrails (formerly CalypsoAI Inference Defend).** F5 completed its acquisition of CalypsoAI in March 2026, delivering real-time protection at the inference layer. AI Guardrails blocks prompt injection, jailbreaks, and data exfiltration at execution time. The companion product F5 AI Red Team deploys autonomous agent swarms simulating thousands of attack patterns, drawing from a vulnerability database updated with over 10,000 new attack patterns each month. "Agentic Fingerprints" provide granular insight into every AI interaction with detailed reasoning for why a prompt was accepted or blocked -- directly relevant to 13.7.1 audit requirements.

**Lasso Security AI Runtime Platform.** Lasso integrates offensive red-teaming with defensive runtime enforcement, continuously validating that agents operate within their intended scope. The Lasso--Portkey integration embeds security controls directly into the MCP Gateway request pipeline, with every tool call, data exchange, and agent-to-server interaction passing through protection with sub-50ms latency overhead. Key capabilities include inline enforcement (deterministic prevention in request/response paths), behavioral pattern analysis across sessions for goal drift detection, and automated response options (blocking outputs, restricting tool access, triggering review).

**Microsoft Defender for AI Agents + Agent 365.** In Microsoft Copilot Studio, Defender performs real-time security checks at tool invocation time, determining whether each action should be allowed or blocked before execution. **Microsoft Agent 365 reaches general availability on May 1, 2026** at $15 per user, as a standalone plan or an add-on to qualifying Microsoft 365 subscriptions. Agent 365 operationalises five capabilities explicitly aligned with C13.7 requirements: **Registry** (inventory of every agent in the tenant), **Access Control** (identity and permission scoping via Entra), **Visualization** (agent-to-agent relationship graphs for 13.7.3 pattern analysis), **Interoperability** (standardised telemetry), and **Security** (logging, audit trails, data-security risk detection, and alerting). See [Microsoft Agent 365 product page](https://www.microsoft.com/en-us/microsoft-agent-365) and the [Microsoft 365 Blog announcement](https://www.microsoft.com/en-us/microsoft-365/blog/2025/11/18/microsoft-agent-365-the-control-plane-for-ai-agents/).

**Galileo AI.** Galileo provides configurable rules, rulesets, and stages that block unsafe outputs before execution. Dedicated agentic metrics (Action Advancement, Tool Selection Quality, Agent Efficiency) enable security teams to detect behavioral anomalies without manual trace review. Confidence thresholds with automated escalation support human-in-the-loop approval for high-risk decisions (relevant to 13.7.4).

**Arize AI / Phoenix.** Built on the OpenInference standard (OpenTelemetry-based), Arize provides production-scale behavioral assessment with LLM-as-Judge evaluation frameworks and drift detection from its ML observability heritage. Agent Graph visualization shows exactly which step in an agent workflow broke and why, supporting forensic analysis of proactive behavior failures.

The architectural distinction that matters for implementation: **inline enforcement** (controls in the request/response path) provides deterministic prevention and is appropriate for high-risk proactive actions, while **out-of-band enforcement** (asynchronous observation via logs/traces) is primarily detective and allows post-action intervention. Most production deployments will need both modes operating simultaneously. The Microsoft Agent Governance Toolkit's sub-0.1ms policy engine and Lasso's sub-50ms MCP gateway represent the current inline-latency state of the art -- these numbers matter when building the latency budget for 13.7.1 validation pipelines.

### OpenTelemetry GenAI Semantic Conventions as a Detection Substrate

A standardised telemetry substrate is essential for 13.7.3 (pattern analysis) and 13.7.5 (anomaly detection) at enterprise scale. The OpenTelemetry GenAI Special Interest Group has been developing semantic conventions for LLM calls, vector DB queries, and agent operations since April 2024. As of April 2026, most GenAI semantic conventions remain in **experimental status** (unstable APIs), though the AI-agent-application semantic convention has been finalised based on Google's AI agent white paper. Practical implications:

- Organisations should correlate traces to user sessions by setting `user.id` and `session.id` as span attributes on the root span -- this is the minimum viable instrumentation for session-based anomaly detection.
- Standardised agent spans capture tool invocations, reasoning steps, token usage, and cost at a cross-vendor abstraction level, making it feasible to build detectors that work across LangChain, CrewAI, LlamaIndex, AutoGen, LangGraph, and frameworks not yet built.
- Vendors including Arize, Braintrust, Uptrace, and Elastic are rolling out OTel-native backends in 2026, so the tooling ecosystem around these conventions is maturing rapidly.
- The "experimental" status is the key caveat for verifiers: audit evidence collected against experimental spans may need schema migration as conventions stabilise. Plan for schema versioning in log retention.

See the [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) and [AI Agent Observability blog post](https://opentelemetry.io/blog/2025/ai-agent-observability/).

### OWASP Top 10 for Agentic Applications 2026

OWASP's Agentic Security Initiative released the **Top 10 for Agentic Applications 2026** (peer-reviewed with input from 100+ contributors), naming the categories that C13.7 is effectively the detection-and-audit layer for. The five that map most directly to 13.7.x requirements:

- **ASI01 -- Agent Goal Hijack**: Attackers redirect agent objectives through manipulated instructions, tool outputs, or external content. Maps to 13.7.2 (trigger integrity) and 13.7.3 (pattern analysis -- goal drift detection).
- **ASI03 -- Tool Misuse & Exploitation**: Agents misuse or abuse tools through unsafe composition, recursion, or excessive execution even with valid permissions. Maps to 13.7.1 (pre-execution validation on tool calls) and 13.7.5 (frequency/cadence anomalies).
- **ASI10 -- Rogue Agents**: Compromised or misaligned agents diverge from intended behavior. Maps directly to 13.7.5 (compromise detection via behavioral deviation).
- **Memory poisoning and inter-agent communication failures** (also in the Top 10): Map to 13.7.2 (trigger authentication) and 13.7.3 (multi-agent pattern analysis).

The Microsoft Copilot Studio guidance on addressing the OWASP Agentic Top 10 (March 30, 2026) provides a concrete mapping of each risk to Copilot Studio features plus Defender, Entra, and Purview controls -- useful as a reference implementation for verifiers. See [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) and [Microsoft's Copilot Studio mapping](https://www.microsoft.com/en-us/security/blog/2026/03/30/addressing-the-owasp-top-10-risks-in-agentic-ai-with-microsoft-copilot-studio/).

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

The EU AI Act's general obligations become enforceable on **August 2, 2026**, with enforcement of **Article 6 and the full suite of high-risk AI system obligations starting August 2, 2027**. Article 14 (human oversight for high-risk AI systems) has direct implications for 13.7.4 (approval chains):

- **Mandatory risk assessments** before deployment of autonomous agents in high-risk categories
- **Logging obligations and auditability** -- audit trails must include timestamps, decision rationale, tool usage history with parameters, policy compliance check results, and identity mapping linking agents to human owners
- **Human oversight mechanisms** for autonomous workflows, with proven robustness and cybersecurity controls
- **Boundary enforcement** -- agents must not exceed authorized operational boundaries

The staggered timeline (August 2026 for general-purpose AI and governance provisions, August 2027 for full high-risk enforcement) gives organisations roughly 16 months from now to operationalise 13.7.4 approval-chain logging if they operate agents in scope. Providers are explicitly encouraged to comply on a voluntary basis during the interim. The OECD AI Principles further reinforce accountability for autonomous actions and transparency in decision-making. ISO 42001 (AI Management System) provides the organizational framework for implementing these requirements systematically. See [AI Act Service Desk timeline](https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act).

As of April 2026, the compliance gap remains significant: per the Gravitee State of AI Agent Security 2026 Report, only 14.4% of organizations deploy agents with full security approval, and only 21% of executives have complete visibility into agent permissions and data access patterns. The practical implication is that most organizations will need to retrofit proactive monitoring capabilities onto already-deployed agents rather than building them in from scratch.

### NIST AI Agent Standards Initiative -- April 2026 Activity

NIST's Center for AI Standards and Innovation (CAISI) is running **sector-specific listening sessions in April 2026** on barriers to AI agent adoption in healthcare, finance, and education. CAISI is explicitly seeking input on audit and non-repudiation mechanisms for agents -- directly relevant to 13.7.4's approval-chain audit requirements. The initiative's three pillars (identity/authorization, interoperable protocols, agent security research) continue to anchor the US federal approach. The NCCoE concept paper on "Software and AI Agent Identity and Authorization" (comment period closed April 2, 2026) proposes JWT-based delegation chain authorization with diminishing permissions down the chain -- a concrete pattern verifiers can look for when assessing 13.7.4 implementations. See [NIST AI Agent Standards Initiative](https://www.nist.gov/caisi/ai-agent-standards-initiative) and the [February 2026 announcement](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure).

---

## Related Standards & References

- **NIST AI 100-1 Section GOVERN 1.7** -- Discusses autonomous system monitoring and oversight requirements
- **NIST AI Agent Standards Initiative (February 2026; April 2026 listening sessions)** -- Three-pillar framework covering identity/authorization, interoperable protocols, and agent security research; sector-specific sessions on healthcare, finance, education ([nist.gov](https://www.nist.gov/caisi/ai-agent-standards-initiative), [announcement](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure))
- **MITRE ATLAS TA0040 (ML Attack Staging)** -- Relevant to detecting compromised agent behavior patterns
- **MITRE ATLAS v5.3.0 (January 2026)** -- 16 tactics, 84 techniques, 56 sub-techniques, 42 case studies; added AML.T0096--T0101 agentic techniques and MCP-related case studies ([atlas.mitre.org](https://atlas.mitre.org/), [Zenity analysis](https://zenity.io/blog/current-events/mitre-atlas-ai-security))
- **IEEE 7001-2021** -- Transparency of Autonomous Systems, relevant to audit trail requirements
- **OWASP Top 10 for Agentic Applications 2026** -- Peer-reviewed framework naming Agent Goal Hijack (ASI01), Tool Misuse (ASI03), and Rogue Agents (ASI10) as top risks; direct input for detection rule design ([genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/))
- **Microsoft: Addressing the OWASP Top 10 Risks in Agentic AI with Copilot Studio (March 30, 2026)** -- Concrete mapping of each OWASP Agentic risk to Defender / Entra / Purview controls ([microsoft.com](https://www.microsoft.com/en-us/security/blog/2026/03/30/addressing-the-owasp-top-10-risks-in-agentic-ai-with-microsoft-copilot-studio/))
- **Exabeam Agent Behavior Analytics (January 2026)** -- First SIEM vendor with behavioral analytics for AI agent activity, session-based detection model ([exabeam.com](https://www.exabeam.com/blog/siem-trends/exabeam-agent-behavior-analytics-first-of-its-kind-behavioral-detections-for-ai-agents/))
- **Microsoft Agent 365 (GA May 1, 2026)** -- Control plane for agent visibility, security, and governance at scale; $15/user; Registry/Access Control/Visualization/Interoperability/Security capabilities ([microsoft.com](https://www.microsoft.com/en-us/microsoft-agent-365), [Nov 2025 blog](https://www.microsoft.com/en-us/microsoft-365/blog/2025/11/18/microsoft-agent-365-the-control-plane-for-ai-agents/))
- **Microsoft Agent Governance Toolkit (April 2, 2026)** -- Open-source MIT-licensed runtime governance; Agent OS <0.1ms p99 policy engine; YAML/OPA Rego/Cedar policies; covers all 10 OWASP agentic risks ([opensource.microsoft.com](https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/))
- **HiddenLayer Agentic Runtime Security (March 23, 2026)** -- Session reconstruction, cross-session investigation, cascading attack chain detection ([prnewswire.com](https://www.prnewswire.com/news-releases/hiddenlayer-unveils-new-agentic-runtime-security-capabilities-for-securing-autonomous-ai-execution-302721517.html))
- **Qualys Agent Val (March 23, 2026)** -- Closed-loop validate/mitigate/revalidate for AI agents inside Enterprise TruRisk Management ([qualys.com](https://blog.qualys.com/product-tech/2026/03/23/meet-agent-val-closing-the-validation-gap-in-exposure-management-at-machine-speed-with-agentic-ai))
- **Cisco AI Defense (February 2026)** -- Runtime protections against tool abuse and supply chain manipulation at the MCP layer
- **OpenTelemetry GenAI Semantic Conventions** -- Cross-vendor span attributes for agents, tools, and sessions; experimental status as of April 2026 ([opentelemetry.io spec](https://opentelemetry.io/docs/specs/semconv/gen-ai/), [agent observability blog](https://opentelemetry.io/blog/2025/ai-agent-observability/))
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
- **HiddenLayer 2026 AI Threat Landscape Report** -- "1 in 8 AI breaches are linked to agentic systems" (corroborates CrowdStrike/Mandiant 2025 figure)
- **LiteLLM Supply Chain Compromise (March 24, 2026)** -- TeamPCP published backdoored PyPI wheels via Trivy CI pivot; Mercor confirmed breached via transitive MCP plugin dependency ([LiteLLM security update](https://docs.litellm.ai/blog/security-update-march-2026), [Trend Micro](https://www.trendmicro.com/en_us/research/26/c/inside-litellm-supply-chain-compromise.html), [InfoQ](https://www.infoq.com/news/2026/03/litellm-supply-chain-attack/))
- **EU AI Act Implementation Timeline** -- General obligations enforce Aug 2, 2026; high-risk Article 6 obligations enforce Aug 2, 2027 ([ai-act-service-desk.ec.europa.eu](https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act))

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
- How should organizations balance the latency cost of inline pre-execution validation against the security benefit, particularly for high-throughput agentic workflows where accumulated latency may degrade user experience or time-sensitive operations? As of April 2026 the state-of-the-art inline latency envelope spans three orders of magnitude -- Microsoft Agent OS advertises <0.1ms p99 while Lasso's MCP gateway reports sub-50ms; where on that curve does the cost/benefit trade-off actually sit for a typical enterprise agent fleet?
- Given the LiteLLM supply chain compromise (March 2026), where malicious code ran inside legitimate agent processes via transitive MCP-plugin dependencies, how should 13.7.5 behavioural baselines be designed to flag *library-level* compromise without generating false positives on every legitimate dependency update?
- The OpenTelemetry GenAI semantic conventions remain experimental as of April 2026. What schema-migration strategy should auditors require for audit logs that must survive into the 7--10 year retention windows mandated by some regulated industries when the underlying span attribute names may change?

---

## Related Pages

- [C09-02 High-Impact Action Approval](C09-02-High-Impact-Action-Approval) -- Defines the runtime execution gate for security-critical proactive actions; 13.7.4 audits the approval events that this page requires the system to collect.
- [C09-04 Agent Identity and Audit](C09-04-Agent-Identity-and-Audit) -- Cryptographic agent identity and tamper-evident audit trails; the primary record layer that C13.7 monitoring consumes and verifies.
- [C11-08 Agent Security Self-Assessment](C11-08-Agent-Security-Self-Assessment) -- Pre-execution adversarial review and red-team hardening; complements 13.7.1 validation with offensive assurance.
- [C13-02 Abuse Detection and Alerting](C13-02-Abuse-Detection-Alerting) -- Signature and behavioural detection for user-facing abuse; 13.7.x extends these primitives to agent-initiated rather than user-initiated events.
- [C14-01 Kill-Switch and Override Mechanisms](C14-01-Kill-Switch-Override-Mechanisms) -- The human-oversight escape hatch that 13.7.5 anomaly detection ultimately needs to trigger when compromise is suspected.

---
