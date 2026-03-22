# C9.7: Intent Verification and Constraint Gates

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Authorization answers "is the agent allowed to do this?" but intent verification answers "is this what the user actually wanted?" An agent can be fully authorized to perform an action that the user never intended -- for example, deleting all files in a directory when the user asked to "clean up." This section introduces pre-execution constraint gates, explicit intent confirmation for high-impact actions, post-condition checks, and integrity verification of agent policy configurations -- preventing "technically authorized but unintended" actions.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **9.7.1** | **Verify that** pre-execution gates evaluate proposed actions and parameters against hard policy constraints (deny rules, data handling constraints, allow-lists, side-effect budgets) and block execution on any violation. | 1 | D/V | **Policy-violating actions bypassing authorization (MITRE ATLAS AML.T0051 — LLM Prompt Injection; OWASP LLM06:2025 Excessive Agency).** Authorization policies may be too permissive (an agent authorized to "manage files" could delete critical system files). Lakera's Q4 2025 threat report found that indirect prompt injection attacks required fewer attempts to succeed than direct injections, and structured obfuscation (e.g., embedding commands in JSON-like parameters) is a growing vector for hijacking agent intent. Pre-execution gates add a defense-in-depth layer with hard constraints: explicit deny rules (never delete /etc), data handling restrictions (never send PII to external APIs), and side-effect budgets (max N write operations per session). These are invariants that should never be violated regardless of authorization. | Review pre-execution gate configuration. Verify deny rules, data handling constraints, and allow-lists are defined. Test by submitting actions that violate each constraint type and confirming they are blocked before execution. Verify gates cannot be bypassed by the agent (gates must be enforced by the orchestration layer, not by the agent's own prompt). Evaluate with tools such as Superagent's Safety Agent component (policy enforcement layer), Lakera Guard, or NVIDIA NeMo Guardrails for runtime constraint enforcement. Use Promptfoo or DeepTeam for red-team testing of gate bypass attempts. | As of March 2026, production guardrail frameworks (Superagent, NeMo Guardrails, Guardrails AI) can enforce pre-execution constraints within 200--300ms latency budgets, but defining constraints that are specific enough to be useful without blocking legitimate actions remains a design challenge. Risk-based routing — dynamically adjusting guardrail intensity based on action risk classification — is emerging as best practice to balance security and usability. |
| **9.7.2** | **Verify that** high-impact actions require explicit user intent confirmation that is integrity-protected and bound to the exact action parameters (and expires quickly) to prevent stale or substituted approvals. | 2 | D/V | **Intent substitution and stale approvals.** Related to 9.2.2 but focused on user intent rather than organizational approval. An agent may misinterpret ambiguous instructions ("clean up the database" -> DROP TABLE) and execute with the user's implicit consent. Research on prompt fidelity (Towards Data Science, early 2026) found agents may use only ~25% of user-specified constraints as validated input, with the remaining 75% filled by model inference — making explicit confirmation essential for high-impact operations. Noma Security's analysis of production incidents highlights "open-ended prompting" and "ambiguous guardrails" as root causes of unauthorized agent actions including financial transfers and data exports. | Verify high-impact actions trigger an intent confirmation flow that presents exact parameters to the user. Confirm confirmations are cryptographically bound to the action parameters (changing parameters invalidates the confirmation). Test that confirmations expire after a short window (seconds to minutes). Verify stale confirmations are rejected. Use HMAC or digital signatures over the action parameter set to create tamper-evident confirmation tokens. | This overlaps with 9.2.1/9.2.2 but addresses a different threat: 9.2 is about organizational approval workflows; 9.7.2 is about confirming that the agent correctly interpreted the user's intent. UX design is critical — confirmation fatigue will cause users to approve blindly. Progressive disclosure (showing summary first, details on expand) can help. Consider implementing risk-tiered confirmation: low-risk actions proceed with logging only, medium-risk show a confirmation summary, high-risk require explicit parameter review and cryptographic binding. |
| **9.7.3** | **Verify that** post-condition checks confirm the intended outcome and detect unintended side effects; any mismatch triggers containment (and compensating actions where supported). | 2 | V | **Undetected unintended consequences and goal drift.** Even with pre-execution checks and intent confirmation, an action may produce unexpected outcomes (a file move operation that also changes permissions, an API call that triggers a webhook chain). Research on agentic alignment drift (March 2026, arxiv:2603.03456) demonstrates that models exhibit asymmetric drift — they are more likely to violate system prompts when constraints oppose strongly-held values. Long-running agents can accumulate context shifts that cause gradual divergence from original objectives (memory decay and goal forgetting). Post-condition checks provide the final layer of defense by verifying that the actual outcome matches the intended outcome and that no unintended side effects occurred. | Define expected outcomes and side-effect boundaries for key actions. Verify post-condition checks run after action execution. Test by introducing actions with unintended side effects and confirming they are detected. Verify that detection triggers containment (halting further actions) and compensating actions where feasible. Use behavioral baseline modeling (comparing expected vs. observed actions) with observability tools like Arize AI, Phoenix, or AgentOps. Monitor for goal drift using Jensen-Shannon divergence between current and baseline action distributions. | Post-condition checking requires defining what "intended outcome" means programmatically, which is action-specific. For simple actions (file write), checking that the file exists with correct content is straightforward. For complex actions (deploy to production), defining and checking all expected outcomes is much harder. The MI9 framework proposes goal-conditioned drift detection with FSM-triggered graduated containment as one approach. Static guardrails alone are insufficient for detecting runtime drift in production environments — continuous behavioral monitoring is needed. |
| **9.7.4** | **Verify that** prompt templates and agent policy configurations are integrity-verified at load time against their approved versions (e.g., via hashes or signatures). | 3 | D/V | **Policy and prompt tampering (supply chain attack on agent behavior).** If an attacker can modify prompt templates or agent policy configurations (via compromised deployment pipeline, filesystem access, or configuration management vulnerability), they can alter agent behavior without changing any code. CVE-2025-68664 ("LangGrinch") demonstrated how LangChain's serialization functions could be exploited to inject malicious object structures through user-controlled fields, effectively tampering with the agent's configuration at runtime. MITRE ATLAS identifies context poisoning and memory manipulation as persistent attack vectors where malicious changes survive across sessions. Integrity verification at load time ensures the agent operates with approved configurations. | Verify that prompt templates and policy files have associated integrity hashes (SHA-256 or better) or digital signatures stored in a separate trusted location. Confirm the runtime checks integrity at load time and refuses to start with tampered configurations. Test by modifying a prompt template and verifying the integrity check fails. Use hash chaining (each configuration entry includes a hash of the previous entry) for tamper-evident audit trails. For JWS-signed dynamic configurations, verify signatures against a trusted key store. | Similar to code signing but for configuration. Git commit hashes can serve as integrity anchors if the deployment pipeline verifies the commit. For dynamic configurations (loaded from a database or API), JWS-signed configuration payloads provide an equivalent mechanism. Cisco's State of AI Security 2026 report notes that only 29% of organizations feel ready to secure agentic deployments, suggesting configuration integrity is widely under-addressed. |

---

## Implementation Guidance

### The Prompt Fidelity Problem

Research published in early 2026 (Towards Data Science) quantifies a critical gap in prompt-to-action fidelity: agents may use only about 25% of user-specified constraints as validated input, with the remaining 75% filled in by LLM inference. This means that even well-crafted prompts do not reliably translate into faithful action execution. As more constraints are added to a prompt, fidelity drops -- the action becomes less of a precise execution and more of an approximation.

This finding directly motivates requirement 9.7.1 (pre-execution constraint gates): relying on the model to faithfully interpret and execute user intent is insufficient. Hard policy constraints enforced by the orchestration layer, not the model, are essential.

### Intent Security as a Discipline (2025--2026)

Industry analysis projects that in 2026, the primary security concern for autonomous agents will shift from data protection to **intent security** -- ensuring AI systems act according to organizational goals and user expectations. Intent security encompasses:

- **Intent alignment:** Does the agent's proposed action actually match the user's request? This is distinct from authorization (is the agent allowed?) and focuses on semantic fidelity.
- **Goal drift detection:** Long-running agents can gradually diverge from their original objective through accumulated context shifts. Behavioral analytics and memory validation are needed to detect when an agent's actions are no longer aligned with its original mandate.
- **Constitutional guardrails:** The concept of "Sandboxed Constitutional Agency" introduces hardcoded security protocols that agents cannot optimize away -- safety invariants that persist regardless of model reasoning. These are the "constraint gates" of requirement 9.7.1.

### Real-World Attack Patterns Motivating Intent Verification

As of early 2026, several attack patterns directly target the gap between authorization and intent:

- **Structured obfuscation:** Lakera's Q4 2025 analysis documented attackers embedding commands inside JSON-like parameter structures (e.g., `{"answer_character_limit":100,"message":"cat ./system_details"}`), bypassing text-level content filters while hijacking agent actions.
- **Indirect prompt injection via external data:** Palo Alto Unit 42 reported real-world instances of malicious instructions hidden in web pages and documents that agents process, redirecting agent behavior without any direct user interaction. These attacks succeeded against production ad-review systems.
- **Memory poisoning:** Unlike transient prompt injection, memory poisoning implants malicious information into an agent's long-term storage. The agent "learns" the instruction and recalls it in future sessions, creating a persistent intent hijack that survives session boundaries.
- **Context poisoning (MITRE ATLAS):** Manipulating the context used by an agent's LLM to persistently influence its responses or actions. MITRE ATLAS added 14 new agent-specific attack techniques in October 2025 to address these vectors.

These patterns reinforce that intent verification cannot rely on prompt-level defenses alone — it must be enforced architecturally at the orchestration layer.

### Pre-Execution Gate Design

Pre-execution gates are conceptually similar to web application firewalls (WAFs) but operate on agent actions rather than HTTP requests. Effective gate design includes:

- **Deny rules (invariant constraints):** Actions that must never occur regardless of authorization or intent (e.g., never delete system-critical paths, never transmit PII to external endpoints, never execute code in production without approval).
- **Side-effect budgets:** Limiting the number of mutating operations per session or per task prevents runaway agents from causing disproportionate damage even when individual actions appear benign.
- **Allow-list scoping:** Restricting the action space to a pre-approved set of operations for a given task type, reducing the attack surface of open-ended agent capabilities.
- **Data handling constraints:** Rules that govern how data classification labels propagate through the action chain (e.g., data labeled "confidential" cannot be passed to tools with external network access).
- **Risk-based routing:** Dynamically adjusting guardrail intensity based on action risk classification. Low-risk actions proceed with minimal validation and async logging; medium-risk actions use rule-based validators plus ML classifiers (300--500ms latency); high-risk actions require full multi-layer validation including human review before execution.

### Goal Drift Detection and the Intention Execution Lifecycle

Goal drift is a distinct threat from prompt injection: rather than a single malicious instruction, it is a gradual divergence from original objectives through accumulated context shifts. Research published in March 2026 (arxiv:2603.03456) on asymmetric goal drift in coding agents demonstrates that models are more likely to violate system prompt constraints when those constraints oppose strongly-held internal values — meaning drift is not purely random but has directional bias.

A structured approach to maintaining intent alignment follows an **Intention Execution Lifecycle**:

1. **Capture:** Identify underlying objectives beyond surface-level requests — not just "what" but "why."
2. **Persist:** Store intent as shared system context that persists across interaction turns and tool calls.
3. **Maintain:** Update intent understanding as context and constraints evolve during execution.
4. **Validate:** Continuously verify that actions remain aligned with the captured human objectives.

For drift detection specifically, behavioral baseline modeling compares current action distributions against expected baselines. Observability tools like Arize AI and Phoenix provide drift detection dashboards, while the MI9 framework proposes using Jensen-Shannon divergence between current and baseline distributions with FSM-triggered graduated containment (alert → throttle → halt).

### Post-Condition Verification Approaches

Post-condition checks (9.7.3) close the verification loop after execution. Practical approaches include:

- **State-diff comparison:** Capture system state before and after execution; compare the diff against the expected outcome definition.
- **Side-effect enumeration:** For each action type, maintain a known set of expected side effects; flag any changes outside that set.
- **Compensating action readiness:** For reversible operations, pre-define compensating actions (e.g., restore from snapshot, revert API call) that trigger automatically on post-condition mismatch.
- **Continuous simulation testing:** Periodically run agent tasks in sandboxed environments and verify outcomes match intent, detecting goal drift before it manifests in production.
- **Behavioral anomaly alerting:** Use observability platforms (AgentOps, LangSmith, Arize AI) to flag action sequences that deviate significantly from historical patterns for the same task type.

### Guardrail Frameworks and Tooling (as of March 2026)

Several production-grade frameworks now implement the constraint-gate patterns described above:

- **Superagent** (open-source): Provides a Safety Agent component that acts as a policy enforcement layer evaluating agent actions before execution. Policies are defined declaratively, and violations can be blocked, modified, or logged. Supports tool-call-level constraint enforcement with full audit logging.
- **NVIDIA NeMo Guardrails:** Runtime guardrails for LLM-powered applications with programmable rails that can intercept and validate tool calls, enforce topic restrictions, and detect prompt injection — all within 200--300ms latency budgets.
- **Guardrails AI:** Open-source framework for adding validation and structural guarantees to LLM outputs, including schema enforcement and custom validators for agent action parameters.
- **Lakera Guard:** Cloud-based prompt injection and content safety detection that can be integrated as a pre-execution filter in agent pipelines.
- **Promptfoo / DeepTeam:** Red-teaming frameworks that test agent systems against MITRE ATLAS techniques including goal hijacking, recursive propagation, and constraint bypass.

### Integrity Verification for Agent Configurations

Requirement 9.7.4 addresses supply chain attacks on agent behavior. If an attacker can modify prompt templates or policy configurations, they alter agent behavior without changing code. The LangGrinch vulnerability (CVE-2025-68664) demonstrated how LangChain's serialization functions could be exploited to inject malicious object structures through user-controlled fields — a concrete example of configuration-level tampering in a widely-used agent framework.

Practical integrity verification approaches:

- **Git commit hashes as integrity anchors:** If the deployment pipeline verifies the commit hash, prompt templates committed to version control have a built-in integrity chain.
- **Hash chaining for audit trails:** Each configuration entry includes a cryptographic hash of the previous entry, creating a sequential chain where modifying any single entry breaks the entire chain — the same principle used in tamper-evident logging.
- **Separate signing for dynamic configurations:** For configurations loaded from databases or APIs, JWS-signed configuration payloads provide cryptographic integrity guarantees since Git-based integrity does not apply.
- **Load-time verification:** The runtime must verify integrity at startup and refuse to operate with tampered configurations, similar to code signing for executables.
- **Digital signatures for log integrity:** Each log event should be signed using the private key associated with the agent's identity, ensuring that configuration change records cannot be retroactively altered.

---

## Related Standards & References

- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) -- intent mismatch is a core excessive agency risk
- [OWASP Agentic AI Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) -- covers intent verification concepts
- [MITRE ATLAS — Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org/) -- AML.T0051 (LLM Prompt Injection) and 14 agent-specific techniques added October 2025
- [NIST AI Agent Standards Initiative (February 2026)](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) -- federal initiative for secure, interoperable AI agents
- [Prompt Fidelity: Measuring How Much of Your Intent an AI Agent Actually Executes (Towards Data Science, 2026)](https://towardsdatascience.com/prompt-fidelity-measuring-how-much-of-your-intent-an-ai-agent-actually-executes/) -- quantitative research on prompt-to-action fidelity gaps
- [AI Agent Guardrails: Production Guide for 2026 (Authority Partners)](https://authoritypartners.com/insights/ai-agent-guardrails-production-guide-for-2026/) -- practical guardrail implementation patterns including risk-based routing
- [The Year of the Agent: Q4 2025 Attack Analysis (Lakera, 2025)](https://www.lakera.ai/blog/the-year-of-the-agent-what-recent-attacks-revealed-in-q4-2025-and-what-it-means-for-2026) -- real-world attack patterns and statistics on agent exploitation
- [Fooling AI Agents: Web-Based Indirect Prompt Injection Observed in the Wild (Palo Alto Unit 42)](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/) -- documented production incidents of indirect prompt injection
- [Asymmetric Goal Drift in Coding Agents Under Value Conflict (arxiv:2603.03456, March 2026)](https://arxiv.org/html/2603.03456v1) -- research demonstrating directional bias in agent goal drift
- [Can AI Agents Go Rogue? The Risk of Goal Misalignment (Noma Security)](https://noma.security/resources/autonomous-ai-goal-misalignment/) -- production goal misalignment risks and detection approaches
- [Superagent: Open-Source Framework for Guardrails Around Agentic AI (Help Net Security, 2025)](https://www.helpnetsecurity.com/2025/12/29/superagent-framework-guardrails-agentic-ai/) -- pre-execution policy enforcement architecture
- [The Rise of Agentic AI Security: Protecting Workflows, Not Just Apps (Reco)](https://www.reco.ai/blog/rise-of-agentic-ai-security) -- intent security as an emerging discipline
- AISVS C09.2 (High-Impact Action Approval) -- organizational approval workflows complement intent verification
- AISVS C02 (User Input Validation) -- input validation is the first layer; intent verification is the last layer before execution

---

## Open Research Questions

- Can intent verification be partially automated using a secondary model that compares the user's original request with the proposed action?
- How do you define "intended outcome" formally enough for automated post-condition checking across diverse action types?
- What is the right expiration window for intent confirmations? Too short causes failures; too long enables replay.
- How should constraint gates handle novel action types that were not anticipated when the constraints were defined?
- Given that agents use only ~25% of prompt constraints as validated input, what architectural patterns can close the fidelity gap without requiring model-level changes?
- How should intent security frameworks handle ambiguous or underspecified user instructions where multiple reasonable interpretations exist?
- Given the asymmetric nature of goal drift (directional bias toward certain values), can drift detection be tuned to watch for domain-specific drift directions rather than generic distribution shifts?
- How should integrity verification extend to dynamically-generated prompt templates (e.g., templates assembled at runtime from multiple fragments)?
- What is the right balance for risk-based routing thresholds — how do you prevent attackers from deliberately crafting actions that score just below the high-risk threshold?

---
