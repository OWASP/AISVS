# C9.7: Intent Verification and Constraint Gates

[Back to C09 Index](C09-Orchestration-and-Agents.md)

## Purpose

Authorization answers "is the agent allowed to do this?" but intent verification answers "is this what the user actually wanted?" An agent can be fully authorized to perform an action that the user never intended -- for example, deleting all files in a directory when the user asked to "clean up." This section introduces pre-execution constraint gates, explicit intent confirmation for high-impact actions, post-condition checks, and integrity verification of agent policy configurations -- preventing "technically authorized but unintended" actions.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **9.7.1** | **Verify that** pre-execution gates evaluate proposed actions and parameters against hard policy constraints (deny rules, data handling constraints, allow-lists, side-effect budgets) and block execution on any violation. | 1 | **Policy-violating actions bypassing authorization (MITRE ATLAS AML.T0051 — LLM Prompt Injection; OWASP LLM06:2025 Excessive Agency).** Authorization policies may be too permissive (an agent authorized to "manage files" could delete critical system files). Lakera's Q4 2025 threat report found that indirect prompt injection attacks required fewer attempts to succeed than direct injections, and structured obfuscation (e.g., embedding commands in JSON-like parameters) is a growing vector for hijacking agent intent. Pre-execution gates add a defense-in-depth layer with hard constraints: explicit deny rules (never delete /etc), data handling restrictions (never send PII to external APIs), and side-effect budgets (max N write operations per session). These are invariants that should never be violated regardless of authorization. | Review pre-execution gate configuration. Verify deny rules, data handling constraints, and allow-lists are defined. Test by submitting actions that violate each constraint type and confirming they are blocked before execution. Verify gates cannot be bypassed by the agent (gates must be enforced by the orchestration layer, not by the agent's own prompt). Evaluate with tools such as Superagent's Safety Agent component (policy enforcement layer), Lakera Guard, or NVIDIA NeMo Guardrails for runtime constraint enforcement. Use Promptfoo or DeepTeam for red-team testing of gate bypass attempts. | As of March 2026, production guardrail frameworks (Superagent, NeMo Guardrails, Guardrails AI) can enforce pre-execution constraints within 200--300ms latency budgets, but defining constraints that are specific enough to be useful without blocking legitimate actions remains a design challenge. Risk-based routing — dynamically adjusting guardrail intensity based on action risk classification — is emerging as best practice to balance security and usability. |
| **9.7.2** | **Verify that** post-execution checks confirm the intended outcome was achieved. | 2 | **Intent substitution and stale approvals.** Related to 9.2.2 but focused on user intent rather than organizational approval. An agent may misinterpret ambiguous instructions ("clean up the database" -> DROP TABLE) and execute with the user's implicit consent. Research on prompt fidelity (Towards Data Science, early 2026) found agents may use only ~25% of user-specified constraints as validated input, with the remaining 75% filled by model inference — making explicit confirmation essential for high-impact operations. Noma Security's analysis of production incidents highlights "open-ended prompting" and "ambiguous guardrails" as root causes of unauthorized agent actions including financial transfers and data exports. | Verify high-impact actions trigger an intent confirmation flow that presents exact parameters to the user. Confirm confirmations are cryptographically bound to the action parameters (changing parameters invalidates the confirmation). Test that confirmations expire after a short window (seconds to minutes). Verify stale confirmations are rejected. Use HMAC or digital signatures over the action parameter set to create tamper-evident confirmation tokens. | This overlaps with 9.2.1/9.2.2 but addresses a different threat: 9.2 is about organizational approval workflows; 9.7.2 is about confirming that the agent correctly interpreted the user's intent. UX design is critical — confirmation fatigue will cause users to approve blindly. Progressive disclosure (showing summary first, details on expand) can help. Consider implementing risk-tiered confirmation: low-risk actions proceed with logging only, medium-risk show a confirmation summary, high-risk require explicit parameter review and cryptographic binding. |
| **9.7.3** | **Verify that** post-execution checks detect unintended side effects. | 2 | **Undetected unintended consequences and goal drift.** Even with pre-execution checks and intent confirmation, an action may produce unexpected outcomes (a file move operation that also changes permissions, an API call that triggers a webhook chain). Research on agentic alignment drift (March 2026, arxiv:2603.03456) demonstrates that models exhibit asymmetric drift — they are more likely to violate system prompts when constraints oppose strongly-held values. Long-running agents can accumulate context shifts that cause gradual divergence from original objectives (memory decay and goal forgetting). Post-condition checks provide the final layer of defense by verifying that the actual outcome matches the intended outcome and that no unintended side effects occurred. | Define expected outcomes and side-effect boundaries for key actions. Verify post-condition checks run after action execution. Test by introducing actions with unintended side effects and confirming they are detected. Verify that detection triggers containment (halting further actions) and compensating actions where feasible. Use behavioral baseline modeling (comparing expected vs. observed actions) with observability tools like Arize AI, Phoenix, or AgentOps. Monitor for goal drift using Jensen-Shannon divergence between current and baseline action distributions. | Post-condition checking requires defining what "intended outcome" means programmatically, which is action-specific. For simple actions (file write), checking that the file exists with correct content is straightforward. For complex actions (deploy to production), defining and checking all expected outcomes is much harder. The MI9 framework proposes goal-conditioned drift detection with FSM-triggered graduated containment as one approach. Static guardrails alone are insufficient for detecting runtime drift in production environments — continuous behavioral monitoring is needed. |
| **9.7.4** | **Verify that** any mismatch between intended outcome and actual results triggers containment and, where supported, compensating actions. | 2 | **Uncontained outcome mismatches leading to cascading failures (OWASP LLM06:2025 Excessive Agency; MITRE ATLAS AML.T0054 — LLM Jailbreak).** When post-condition checks (9.7.2, 9.7.3) detect a mismatch between intended and actual outcomes, the system must respond — not just log. Without automated containment, a misaligned action can propagate through downstream agents and tools, compounding damage. The ClawHavoc campaign (February 2026) demonstrated how 1,184 poisoned OpenClaw skills on ClawHub executed malicious payloads including reverse shells and credential theft once triggered — actions whose outcomes clearly diverged from user intent but were not caught by any containment mechanism. Noma Security's analysis of production incidents identifies "missing containment" as a root cause where agents performed unauthorized financial transfers and data exports that continued unchecked after initial misalignment. | Verify that outcome mismatch detection (from 9.7.2/9.7.3) triggers an automated containment response: halt the current execution chain, prevent further agent actions, and alert operators. Test by inducing an intentional mismatch (e.g., action returns unexpected state) and confirming the system halts rather than continuing. Verify compensating actions are defined for reversible operations (rollback database transaction, revert file change, cancel API call) and that they execute correctly. Confirm that containment events are logged with full context (action attempted, expected outcome, actual outcome, compensating action taken). Evaluate with observability platforms (Arize AI, AgentOps, LangSmith) that can trigger automated responses on drift detection. | Compensating actions are feasible for reversible operations (database transactions, file writes, API calls with cancel endpoints) but many real-world agent actions are irreversible (sent emails, published content, executed financial transfers). For irreversible actions, containment reduces to halting further damage and alerting humans. As of March 2026, defining and testing compensating actions for each action type remains a manual process — no framework automates compensating action generation from action schemas. The MI9 framework's FSM-triggered graduated containment (alert → throttle → halt) provides a structured model but requires per-deployment tuning. |
| **9.7.5** | **Verify that** prompt templates and agent policy configurations retrieved from a remote source are integrity-verified at load time against their approved versions (e.g., via hashes or signatures). | 3 | **Supply chain attacks on agent behavior via configuration tampering (MITRE ATLAS — seven new OpenClaw-specific techniques identified February 2026; OWASP LLM06:2025 Excessive Agency).** If an attacker can modify prompt templates, skill definitions, or policy configurations — whether through a compromised deployment pipeline, package registry, filesystem access, or configuration management vulnerability — they alter agent behavior without changing any code. The ClawHavoc campaign (February 2026, Antiy CERT) demonstrated this at scale: 1,184 poisoned skills were uploaded to OpenClaw's ClawHub marketplace, each containing a malicious SKILL.md that, when loaded into an agent's context, directed the LLM to execute attacker-controlled commands — delivering reverse shells, credential stealers (Atomic macOS Stealer), and ClickFix payloads. CVE-2025-68664 ("LangGrinch") showed how LangChain's serialization could be exploited to inject malicious objects through user-controlled fields. CVE-2025-61260 exploited config files (.env, .codex/config.toml) in OpenAI Codex CLI for arbitrary command execution. MITRE ATLAS now classifies "modifying an agentic configuration" as a distinct attack technique. | Verify that prompt templates and policy files have associated integrity hashes (SHA-256 or better) or digital signatures stored separately from the artifacts themselves. Confirm the runtime checks integrity at load time and refuses to start with tampered configurations. Test by modifying a prompt template and verifying the integrity check fails and the agent does not load the modified template. For skills and plugins fetched from registries, verify signature validation occurs before any content is loaded into the agent's context. Evaluate using Sigstore/cosign for signing configuration artifacts as OCI bundles (supports keyless signing with OIDC identity binding), or JWS-signed payloads for API-served configurations. For Git-managed templates, verify the deployment pipeline checks commit signatures (GPG/SSH) before deployment. Use hash chaining (each configuration entry includes a hash of the previous entry) for tamper-evident audit trails across configuration versions. | As of March 2026, there is no widely-adopted standard specifically for signing AI agent prompt templates or policy configurations. The Sigstore model-signing project (model-transparency v1.0) provides CLI and Python tooling for signing ML models with transparency logs and plans to extend to datasets and other ML artifacts — prompt templates and policy configs are a natural extension but not yet explicitly supported. For container-native deployments, cosign can sign and verify configuration bundles packaged as OCI artifacts, and OPA policy bundles can be signed the same way. Git commit hashes serve as integrity anchors when the deployment pipeline verifies commit signatures, but this does not cover dynamic configurations loaded at runtime from APIs or databases. The ClawHavoc incident accelerated discussion of mandatory signature verification for agent skill marketplaces, but ClawHub's verification mechanisms remain opt-in as of March 2026. Cisco's State of AI Security 2026 report notes only 29% of organizations feel ready to secure agentic deployments, suggesting configuration integrity is widely under-addressed. |

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

Requirement 9.7.5 addresses supply chain attacks on agent behavior. If an attacker can modify prompt templates, skill definitions, or policy configurations, they alter agent behavior without changing code. Two incidents in the 2025--2026 timeframe illustrate the threat at different scales:

- **LangGrinch (CVE-2025-68664):** LangChain's serialization functions could be exploited to inject malicious object structures through user-controlled fields — a targeted configuration-level tampering attack in a widely-used agent framework.
- **ClawHavoc (February 2026):** A large-scale supply chain campaign where 1,184 poisoned skills were uploaded to OpenClaw's ClawHub marketplace (Antiy CERT, Trend Micro). Each skill contained a malicious SKILL.md file that, when loaded into an agent's context, directed the LLM to execute attacker commands — delivering reverse shells, the Atomic macOS Stealer, and ClickFix payloads. MITRE ATLAS identified seven new OpenClaw-specific attack techniques from this campaign. The attack exploited the absence of mandatory signature verification on the skill marketplace.
- **Codex CLI config injection (CVE-2025-61260):** OpenAI Codex CLI implicitly trusted configuration in `.env` and `.codex/config.toml` files, enabling arbitrary command execution via config file manipulation.

Practical integrity verification approaches:

- **Git commit signatures as integrity anchors:** If the deployment pipeline verifies GPG or SSH commit signatures (not just hashes), prompt templates committed to version control have a cryptographically strong integrity chain. Plain commit hashes prevent accidental corruption but not targeted attacks — signature verification is needed for adversarial resistance.
- **Sigstore/cosign for configuration artifacts:** The Sigstore model-signing project (model-transparency v1.0, released 2025) provides keyless signing using OIDC identity binding with transparency logs. While currently focused on ML models, the same infrastructure signs any OCI artifact — including policy bundles and configuration archives. OPA policy bundles can be signed as OCI images with cosign today.
- **Hash chaining for audit trails:** Each configuration entry includes a cryptographic hash of the previous entry, creating a sequential chain where modifying any single entry breaks the entire chain — the same principle used in tamper-evident logging.
- **JWS-signed dynamic configurations:** For configurations loaded from databases or APIs (where Git-based integrity does not apply), JWS-signed configuration payloads with signature verification against a trusted key store provide equivalent guarantees.
- **Load-time verification with fail-closed behavior:** The runtime must verify integrity at startup and refuse to operate with tampered configurations, similar to code signing for executables. This is non-negotiable — a "warn and continue" mode defeats the purpose.
- **Skill marketplace signing:** The ClawHavoc incident demonstrates that agent plugin/skill marketplaces need mandatory publisher signature verification before any skill content is loaded into an agent's context. As of March 2026, ClawHub's signature verification remains opt-in.

### Verifiable Intent in Commerce (Mastercard/Google, March 2026)

Mastercard and Google introduced Verifiable Intent in March 2026 — an open-source, standards-based cryptographic framework for agentic commerce. While narrowly focused on payment transactions, it demonstrates a general pattern for binding user authorization to agent actions:

- **Immutable authorization records:** Links three elements into a single tamper-resistant record — the consumer's identity, their original instructions, and the transaction outcome. This is effectively a cryptographic proof that a specific user authorized a specific agent action with specific parameters.
- **Selective disclosure:** Shares only the minimum information needed with each party (consumer, merchant, issuer), enabling authorization verification without exposing unnecessary data.
- **Standards foundation:** Built on FIDO Alliance, EMVCo, IETF, and W3C specifications — leveraging existing identity and cryptographic infrastructure rather than inventing new primitives.
- **Open-source reference implementation:** Published on GitHub at verifiableintent.dev, with support from Google, Fiserv, IBM, Checkout.com, Basis Theory, and Getnet.

The pattern of cryptographically binding user identity + intent + action parameters + outcome into a tamper-evident record is directly applicable beyond commerce to any high-impact agent action requiring verifiable intent.

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
- [ClawHavoc: Large-Scale Poisoning Campaign Targeting the OpenClaw Skill Market (Antiy CERT, February 2026)](https://www.antiy.net/p/clawhavoc-analysis-of-large-scale-poisoning-campaign-targeting-the-openclaw-skill-market-for-ai-agents/) -- 1,184 malicious skills demonstrating agent configuration supply chain attacks
- [ClawHavoc Poisons OpenClaw's ClawHub With 1,184 Malicious Skills (CyberPress)](https://cyberpress.org/clawhavoc-poisons-openclaws-clawhub-with-1184-malicious-skills/) -- detailed analysis of attack techniques and payloads
- [Malicious OpenClaw Skills Used to Distribute Atomic macOS Stealer (Trend Micro, February 2026)](https://www.trendmicro.com/en_us/research/26/b/openclaw-skills-used-to-distribute-atomic-macos-stealer.html) -- malware distribution via poisoned agent skills
- [Mastercard Verifiable Intent: Open Standard for AI Agent Transaction Authorization (March 2026)](https://www.pymnts.com/mastercard/2026/mastercard-unveils-open-standard-to-verify-ai-agent-transactions/) -- cryptographic proof of user authorization for agent actions
- [Sigstore Model Signing: Practical Model Signing with Sigstore (model-transparency v1.0)](https://blog.sigstore.dev/model-transparency-v1.0/) -- keyless signing and transparency logs for ML artifacts, extensible to configurations
- [MITRE ATLAS OpenClaw Investigation (February 2026)](https://www.mitre.org/sites/default/files/2026-02/PR-26-00176-1-MITRE-ATLAS-OpenClaw-Investigation.pdf) -- seven new agent-specific attack techniques identified
- [Securing AI Agents: The Defining Cybersecurity Challenge of 2026 (Bessemer Venture Partners)](https://www.bvp.com/atlas/securing-ai-agents-the-defining-cybersecurity-challenge-of-2026) -- industry analysis of agent security landscape
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
- After ClawHavoc, what level of mandatory signature verification should agent skill marketplaces enforce — and should unsigned skills be blocked entirely or sandboxed with reduced privileges?
- Can the Mastercard Verifiable Intent pattern (cryptographic binding of identity + instructions + outcome) be generalized to non-commerce agent actions, and what is the minimum viable implementation for open-source agent frameworks?

---
