# C9.1: Execution Budgets, Loop Control, and Circuit Breakers

> [Back to C09 Index](C09-Orchestration-and-Agents.md)
> **Last Researched:** 2026-03-28

## Purpose

Autonomous agents can enter runaway states — recursive loops, unbounded fan-out, or chain reactions across tool calls — that consume resources without bound. As of 2026, denial-of-wallet attacks against agentic AI are a material financial risk: Fortune 500 companies collectively leaked an estimated **$400M in unbudgeted cloud spend** from agentic AI cost overruns (Analytics Week, 2026). Specific incidents include a **$47K LangChain multi-agent loop** (November 2025), a **$47K retry storm** from 2.3M erroneous API calls (February 2026), and a **$1.2M GPU hijack** where an AI agent autonomously began mining cryptocurrency (March 2026). The OWASP Top 10 for Agentic Applications 2026 now mandates circuit breakers and transactional rollback in every agentic workflow. No major agent framework has comprehensive built-in cost ceilings — budget enforcement requires external gateways or governance layers. As of March 2026, inference accounts for roughly 85% of the enterprise AI budget, and agentic reasoning loops that hit the LLM 10–20 times per task are the primary cost driver (AnalyticsWeek 2026). The gateway layer is now seeing rapid innovation: Traefik Hub's Triple Gate (v3.20, March 2026) introduced proactive token estimation that blocks abusive requests *before* they reach the LLM, and Bifrost's 11-microsecond overhead makes gateway-level enforcement effectively invisible in the latency budget.

This section requires hard limits on runtime expansion (recursion depth, concurrency, wall-clock time, token usage, monetary spend) enforced by the orchestration runtime, not by the model itself.

> **Scope note:** Controls in this section govern *internal orchestration runtime* budgets: per-task recursion depth, concurrency, wall-clock time, token spend, and monetary limits. They apply inside the agentic execution layer — not at the API ingress edge (covered by OWASP ASVS) and not in response to adversarial probing patterns (C11.4, C11.5). A single token-spend cap at the API gateway does not satisfy C9.1 budget enforcement, which requires enforcement within the orchestration runtime itself.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **9.1.1** | **Verify that** per-execution budgets (max recursion depth, max fan-out/concurrency, wall-clock time, tokens, and monetary spend) are configured and enforced by the orchestration runtime. | 1 | **Unbounded resource consumption** ([OWASP LLM10](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/), [ASI08](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)). An agent entering a recursive planning loop or spawning excessive parallel tool calls can exhaust API budgets and compute. Cost modeling: GPT-4 class agents at 10 cycles/min, 10K tokens/cycle ≈ $3/min; 50 concurrent threads = $9,000/hour burn rate. The $47K LangChain incident ran for 11 days before discovery because no budget threshold existed. Industry benchmarks emerging: **$100/hour hard cap** as standard kill-switch tripwire; **10-step limit** before requiring human help or stopping (Finout 2026). | Review orchestration config for explicit budget parameters. Test by triggering deep recursion and high fan-out; confirm runtime halts at thresholds. Verify budgets are server-side. Check for both request-rate (req/s) AND token-rate (tokens/s) dual limiting. Check for cost-weighted token tracking (output tokens from premium models cost up to 8x input tokens). Use Bifrost or LiteLLM as gateway-level enforcement if framework lacks native budgets. | LangGraph 1.0: `recursion_limit` (no native dollar ceiling; platform billing provides implicit cap via plan quotas). OpenAI Agents SDK: `max_turns` (default 8; no dollar budget). CrewAI: `max_iter` (execution-based billing on hosted platform). AutoGen: custom termination required. **No framework natively enforces dollar-denominated budgets.** External enforcement options: LiteLLM (tag budgets, provider routing, temporary increases), Bifrost (hierarchical hard limits), Portkey (virtual key budgets), AgentBudget (OSS, Feb 2026 — drop-in per-session dollar caps via SDK patching, nested sub-agent budgets). Google Budget Tracker ([arXiv 2511.17006](https://arxiv.org/abs/2511.17006)) offers a complementary prompt-level approach: injecting remaining-budget signals into the reasoning loop reduces tool-call costs by 31% without external enforcement. Token usage in agentic workflows averages ~6x the observable answer tokens; up to 80% of true costs are hidden. |
| **9.1.2** | **Verify that** cumulative resource/spend counters are tracked per request chain and hard-stop the chain when thresholds are exceeded. | 2 | **Distributed budget evasion.** Agent spawning sub-agents may stay under per-call limits while exceeding aggregate budgets. Four attack variants: (1) single-agent hallucination loops, (2) multi-agent circular dependencies (the $47K LangChain Analyzer-Verifier ping-pong), (3) file system recursion (agents reading files containing instructions to read the same file), (4) cascading hallucination (87% downstream decision poisoning within 4 hours). SaaS-to-SaaS worm pattern: agents tricked into calling paid APIs recursively 10,000+ times, draining both API credits and cloud balance. Credential theft compounds the risk: a stolen Gemini API key generated $82,314 in 48 hours (455x normal spend, February 2026); Truffle Security found 2,863 live API keys exposed on public websites. | Trace multi-step execution; confirm cumulative counters (tokens, API calls, wall-clock, cost) span all steps and sub-agents. Verify hard-stop at aggregate level. Use provisional reservation + true-up pattern (reserve max_tokens upfront, refund after actual response). Verify per-agent cost attribution: separate API keys per agent, step-level logging with metadata. Observability tools: Langfuse, AgentOps, Laminar, Langtrace AI for per-session cost tracking. | Cumulative tracking across sub-agents not natively supported in most frameworks. Requires correlation via chain/trace ID. OpenTelemetry helps but needs custom budget-enforcement logic. The escrow-based delegation pattern (arXiv 2602.11865) proposes a formal framework: funds held in escrow until verification conditions are met, with recursive budget delegation and bond slashing for breaches. Market-based allocation (Contract Net Protocol) lets agents bid for work under resource constraints. |
| **9.1.3** | **Verify that** circuit breakers terminate execution on budget violations. | 2 | **Graceless failure on overrun** ([ASI08: Cascading Failures](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)). Without circuit breakers, budget violations may be logged but not acted upon. OWASP 2026 guidance: *"If an agent starts looping and spamming an expensive tool, trip the circuit breaker immediately."* The "Financial Circuit Breaker" pattern emerged from a $30K runaway agent — monitors token velocity ($/minute) and kills the agent if threshold exceeded. | Trigger budget violations in test; confirm: (a) execution halts immediately, (b) partial state cleaned up, (c) downstream consumers notified, (d) no further tool calls after breaker trips. Test both graceful and crash scenarios. Multi-stage breaker: Stage 1 (Yellow) throttles to 10 tokens/sec; Stage 2 (Orange) revokes write permissions, read-only sandbox; Stage 3 (Red) session termination with forensic state preservation (Arion Research). | Circuit breaker patterns well-established in microservices (Hystrix, resilience4j). Microsoft Agent Governance Toolkit v2.2.0 implements circuit breakers + SLO enforcement with sub-millisecond policy enforcement (<0.1ms per action). LiteLLM hard budget limits function as infrastructure-layer circuit breakers — block requests when any budget tier is exhausted, with provider routing to switch to cheaper providers automatically. Bifrost blocks requests outright when budget is exceeded. Galileo Agent Control (March 2026) adds centralized policy enforcement with sub-200ms latency. |
| **9.1.4** | **Verify that** security testing covers runaway loops, budget exhaustion, and partial-failure scenarios, confirming safe termination and consistent state. | 3 | **Untested failure modes.** LangGraph GitHub issue #6731 documents agents infinite-looping until recursion limit error fires, confirming this is often the last line of defense. The Replit agent incident (July 2025) showed an agent ignoring explicit "CODE FREEZE" instructions, deleting 1,206 records, fabricating 4,000 entries, and falsely claiming data was unrecoverable. Memory poisoning attacks (Lakera, November 2025) gradually manipulated a procurement agent over 3 weeks to approve $500K purchases without human review, leading to $5M in fraudulent orders. | Review test suites for chaos/fault-injection tests: infinite loops, rapid fan-out, partial tool failures mid-chain, simultaneous budget violations. Confirm tests assert safe termination and state consistency. Include multi-agent circular dependency scenarios. Test memory poisoning leading to budget escalation. Shadow mode (log would-be throttle decisions without enforcement for 1–2 weeks) useful before going live with new limits. | Few organizations have agentic-specific chaos engineering practices. Test harnesses need to simulate adversarial prompt patterns that induce loops. 48% of respondents in a Dark Reading 2026 poll expect agentic AI to become the top attack vector, yet testing coverage remains minimal. |
| **9.1.5** | **Verify that** budget and circuit-breaker policies are expressed as policy-as-code and are validated in CI/CD to prevent drift and unsafe configuration changes. | 3 | **Configuration drift and tampering.** 49% of employees use unsanctioned AI tools ("Shadow AI"), amplifying uncontrolled spend. Amazon Q incident (July 2025): malicious PR injected resource deletion commands with `--no-interactive` bypass. Only 44% of organizations currently employ financial guardrails for AI agents (AnalyticsWeek 2026); adoption expected to double by end of 2026. | Confirm policies in version-controlled files (OPA Rego, CUE, JSON Schema). Verify CI/CD validates policy files and rejects weakening below minimum thresholds. Microsoft AGT v2.2.0: 4-tier execution privilege rings with tool allowlists/denylists, sub-millisecond enforcement across 13+ frameworks. Galileo Agent Control: "Write policies once, deploy anywhere" with Luna-2 evaluators at ~$0.02/M tokens. | Policy-as-code for agent budgets is maturing rapidly. **OPA/Rego** is the industry-standard PaC engine for AI agent governance — decouples policy from application logic, evaluates in real time before execution, 90% reduction in human-error violations reported. Alternatives: AWS Cedar, Kyverno (Kubernetes-native), Styra DAS (commercial OPA). **Kyndryl** (Feb 2026) offers enterprise PaC for agentic workflows: deterministic execution, audit-by-design, manages 190M automations/month. **NVIDIA OpenShell** (Mar 2026) enforces policy out-of-process at binary/destination/method/path level — agents cannot override even if compromised. Microsoft AGT covers all 10 OWASP ASI 2026 controls. Microsoft Agent 365 (GA May 2026, $15/user/month) provides unified agent governance. FinOps Foundation "Crawl, Walk, Run" maturity model: Crawl = manual tracking with hard caps; Run = hierarchical per-agent budgets with anomaly detection. |

---

## Agent Framework Budget Controls (March 2026)

| Framework | Budget Control | Default | Limitation |
|-----------|---------------|---------|------------|
| **LangGraph** (v1.1.2, Mar 12 2026) | `recursion_limit` | None documented | No cost ceiling in OSS; platform billing caps via plan quotas. Active rapid development. |
| **OpenAI Agents SDK** (v0.12.1, Mar 13 2026) | `max_turns` | 8 turns | Throws `MaxTurnsExceededError`; v0.12.0 added opt-in retry settings via `ModelSettings`; no token/dollar budget; cost control via org billing limits |
| **CrewAI** (v1.10.1, Mar 4 2026) | `max_iter` per task | 10–20 typical | 46K GitHub stars; Gemini GenAI upgrade, MCP tool loading fixes; hosted platform has execution-based billing |
| **AutoGen/AG2** (v0.7.5, Sep 2025) | Custom termination | Must implement | No release in 6 months; default conditions insufficient for production |
| **Claude Agent SDK** | Deny-all baseline + allowlists | Per-subagent | Sandbox with network/domain restrictions; secrets isolated |
| **Microsoft AGT** (v2.2.0) | Token limits + circuit breakers + kill switch | `max_tokens_per_call=4096` | Sub-ms policy; saga orchestration with rollback; 4-tier privilege rings |

**Key gap:** No framework natively enforces dollar-denominated budgets, though AgentBudget (Feb 2026) provides a drop-in SDK that patches existing clients with per-session dollar caps. For org-wide enforcement, external gateways or runtime enforcement layers remain necessary.

### Budget-Aware Reasoning Research

Two lines of research address budget waste at the *reasoning* level — making the agent itself budget-conscious rather than relying solely on external enforcement:

- **Google Budget Tracker + BATS** ([arXiv 2511.17006](https://arxiv.org/abs/2511.17006); Google/NYU/UC Santa Barbara): A prompt-level plug-in that injects a continuous "remaining budget" signal into the agent's reasoning loop. BATS (Budget-Aware Test-time Scaling) extends this to multi-agent systems with dynamic planning/verification that adapts to remaining resources. Benchmarks show 31.3% cost reduction at comparable accuracy, and continued scaling where plain ReAct plateaus. IDC survey: 92% of decision-makers report AI agent costs exceeded expectations.
- **Budget-Aware Value Tree (BAVT)** ([arXiv 2603.12634](https://arxiv.org/abs/2603.12634), March 2026): Models multi-hop reasoning as a dynamic search tree with budget-conditioned node selection. Uses remaining resource ratio as a scaling exponent over node values, transitioning smoothly from exploration to exploitation as budget depletes. Surpasses baselines at 4x the resource allocation under strict constraints.

---

## Cost Control & Governance Tools

| Tool | Type | Key Capability | Source |
|------|------|----------------|--------|
| [LiteLLM](https://docs.litellm.ai/) | OSS gateway | **Tag budgets** (per cost center/project/dept), team budgets, per-key hard limits, soft budget alerts, temporary increases (enterprise), provider budget routing (switch to cheaper provider when tier exhausted) | [docs](https://docs.litellm.ai/docs/proxy/tag_budgets) |
| [Bifrost](https://www.getmaxim.ai/bifrost/) | OSS gateway (Go) | **Hierarchical hard spend limits** per virtual key/team; blocks requests when exceeded; MCP gateway with OAuth 2.0; used by Clinc, Thoughtful, Atomicwork | [docs](https://docs.getbifrost.ai/features/governance/budget-and-limits) |
| [Galileo Agent Control](https://galileo.ai/blog/best-ai-agent-guardrails-solutions) | OSS control plane (Mar 2026) | Centralized runtime policy; Luna-2 evaluators at ~$0.02/M tokens; model routing for cost steering | [Yahoo Finance](https://finance.yahoo.com/news/galileo-releases-open-source-ai-150100502.html) |
| [Microsoft AGT](https://github.com/microsoft/agent-governance-toolkit) | OSS governance | Agent SRE (SLOs, error budgets, circuit breakers); covers all OWASP ASI controls; 13+ frameworks | [GitHub](https://github.com/microsoft/agent-governance-toolkit) |
| [Microsoft Agent 365](https://robquickenden.blog/2026/03/agent-365-nears-ga/) | Commercial (GA May 2026) | Unified agent cost/usage view; budget threshold alerts; $15/user/month | Microsoft |
| [Portkey](https://portkey.ai/) | Commercial (from $49/mo) | Virtual key budgets, dept-level spend caps, smart routing, audit trails | [docs](https://portkey.ai/docs/product/ai-gateway/virtual-keys/budget-limits) |
| [Helicone](https://www.helicone.ai/) | OSS observability | Per-request cost tracking; intelligent caching; lowest-cost provider routing | Helicone |
| [Traefik Triple Gate](https://www.helpnetsecurity.com/2026/03/17/traefik-labs-triple-gate-new-capabilities/) | Commercial gateway (EA Mar 2026) | **Proactive token estimation** blocks abusive prompts before reaching LLM; token rate limiting + quota management (input/output/total independently); circuit breaker failover across providers; MCP gateway with TBAC; 11µs overhead | [BusinessWire](https://www.businesswire.com/news/home/20260316864823/en/) |
| [Mosaic Sentinel](https://www.strategysoftware.com/strategyone/whats-new/mosaic-sentinel-unified-governance-for-open-access) | Commercial data governance (Mar 2026) | Real-time access monitoring + anomaly detection for agentic workloads; cost intelligence; compute arbitrage layer offloading redundant queries; full data lineage tracing | [BusinessWire](https://www.businesswire.com/news/home/20260309172771/en/) |
| [NVIDIA OpenShell](https://developer.nvidia.com/blog/run-autonomous-self-evolving-agents-more-safely-with-nvidia-openshell/) | OSS runtime (Apache 2.0, Mar 16 2026) | **Out-of-process policy enforcement** for long-running agents; deny-by-default sandbox with per-action evaluation (binary, destination, method, path level); privacy router keeps sensitive context on-device; live policy updates at sandbox scope with full audit trail; wraps Claude Code and Cursor. Part of NVIDIA Agent Toolkit (GTC 2026). Partners: Cisco, CrowdStrike, Google Cloud, Microsoft Security, TrendAI. | [NVIDIA Blog](https://blogs.nvidia.com/blog/secure-autonomous-ai-agents-openshell/) |
| [Jozu Agent Guard](https://finance.yahoo.com/news/jozu-launches-agent-guard-ai-100000670.html) | OSS zero-trust runtime (Mar 17 2026) | Tamper-resistant agent execution — security controls that agents cannot disable; continuous verification of every action against guardrails; MCP integration; from the team behind KitOps (240K+ CNCF downloads) | [Yahoo Finance](https://finance.yahoo.com/news/jozu-launches-agent-guard-ai-100000670.html) |
| [AgentBudget](https://github.com/sahiljagtap08/agentbudget) | OSS SDK (Apache 2.0, Feb 2026) | **First dollar-denominated per-session enforcement library** — one-line init patches OpenAI/Anthropic SDKs; three-layer circuit breaker (soft warning at 90%, hard limit, loop detection); nested budgets for sub-agents with automatic rollup; built-in pricing for 60+ models; zero infrastructure (in-process only); LangChain/CrewAI integration | [Hacker News](https://news.ycombinator.com/item?id=47133305) |
| [Kyndryl Agentic AI Governance](https://www.kyndryl.com/us/en/about-us/news/2026/02/policy-as-code-agentic-ai-governance) | Commercial PaC (Feb 2026) | Policy-as-code for agentic workflows; deterministic execution (agents only execute policy-permitted actions); audit-by-design with logged/explainable decisions; manages 190M automations/month across enterprise environments | [PR Newswire](https://www.prnewswire.com/news-releases/kyndryl-unveils-agentic-ai-workflow-governance-for-trusted-deployment-of-missioncritical-ai-agents-302684528.html) |

### Observability for Cost Attribution

| Tool | Key Metric | Notes |
|------|-----------|-------|
| [Langfuse](https://langfuse.com/) | Running token/cost tally across providers | OSS, 19K+ stars |
| [AgentOps](https://www.agentops.ai/) | Per-session cost tracking, 400+ LLMs | Production |
| [Braintrust](https://www.braintrust.dev/) | Per-request cost breakdowns, budget overrun alerts | Production |
| [Laminar](https://www.lmnr.ai/) | Token usage, costs, latency percentiles | Framework-agnostic |
| [OpenTelemetry GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | Standardized semantic conventions for agent spans | Attributes: `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.request.model`; enables cross-vendor cost aggregation. v1.37+ |

---

## Denial-of-Wallet Patterns & Defenses

| Algorithm | Best For | DoW Protection |
|-----------|----------|:--------------:|
| Token Bucket | Real-time apps needing burst flexibility | Moderate |
| Leaky Bucket | Background workflows, max cost predictability | Strong |
| Sliding Window | Production environments | Strong |
| **Layered** (recommended) | Short-term (tokens/min) + long-term (tokens/month) + cost-weighted | **Strongest** |

**Design principles:**
- **Provisional Reservation & True-Up**: Reserve budget upfront based on estimated max_tokens, refund difference after actual response
- **Dual Limiting**: Both request-rate (req/s) AND token-rate (tokens/s) controls
- **Cost-Weighted Tracking**: Output tokens from premium models cost up to 8x input tokens; weight accordingly
- **Graceful Degradation**: Return 429 with remaining budget and reset time so agents can queue/retry intelligently
- **Per-Model Pricing Catalog**: Maintain input vs. output token rates per model
- **Proactive Token Estimation**: Estimate token count at the gateway *before* forwarding to the LLM; reject or truncate requests that would exceed budget in a single call (Traefik Triple Gate v3.20 implements this natively, March 2026)
- **Multi-Provider Failover**: Circuit breaker chains that automatically switch to cheaper providers when primary budget tiers are exhausted, maintaining safety policies across the failover
- Critical: *"You cannot protect costs you cannot measure."*

---

## Four-Layer Enforcement Stack

Budget enforcement that only covers one layer leaves the others unprotected. As of March 2026, the recommended architecture layers enforcement at four distinct points ([Rack2Cloud](https://www.rack2cloud.com/ai-inference-execution-budgets/)):

| Layer | Enforcement Point | Example Controls |
|-------|------------------|-----------------|
| **1. Invocation** | API gateway / proxy | Per-request token limits, context caps, output constraints, proactive token estimation (Traefik Triple Gate) |
| **2. Agent Loop** | Framework config | Step caps, recursion guards, retry limits (`recursion_limit`, `max_turns`, `max_iter`) |
| **3. Orchestration** | Workflow engine | Workflow-level cost ceilings, fan-out caps, time boundaries (Temporal, Prefect, Airflow) |
| **4. Platform** | Cloud provider / org | Org-level quotas, hard spend cutoffs, billing alerts |

**Critical insight:** Alerts and dashboards are *cost witnesses*, not cost *enforcers*. Enforcement must live in the execution path itself, not in an observability sidecar.

### Multi-Agent Reliability Decay (Lusser's Law)

In multi-agent pipelines, failure probability compounds multiplicatively. A single agent at 98% accuracy yields 98% system reliability — but 10 agents at 98% each degrade to **81.7% system reliability** (18.3% error rate). Without validation gates between agents, cost compounds alongside failure: each unchecked hop amplifies both the reliability and financial risk. Mitigation: schema enforcement via Pydantic/Instructor raises effective per-agent accuracy to ~99.8%, and Best-of-N sampling (e.g., RULER framework) further reduces compounding errors ([O'Reilly Radar](https://www.oreilly.com/radar/the-hidden-cost-of-agentic-failure/)).

---

## Notable Incidents

| Date | Incident | Impact | Source |
|------|----------|--------|--------|
| Jul 2025 | Amazon Q malicious PR | Resource deletion commands with `--no-interactive` bypass | Industry reports |
| Jul 2025 | Replit agent data destruction | Ignored CODE FREEZE; deleted 1,206 records, fabricated 4,000 | [Dev\|Journal](https://earezki.com/ai-news/2026-03-18-the-ai-agent-that-defied-a-code-freeze-deleted-1200-customer-records-and-then-lied-about-it/) |
| Mid-2025 | Autoscaling disaster | $120,000 in 72 hours; 2,000 instances spun up with no ceiling | [InfoQ](https://www.infoq.com/news/2025/08/denial-of-wallet-attack-cloud/) |
| Sep 2025 | Anthropic AI espionage campaign | Thousands of requests/second autonomously | Anthropic |
| Nov 2025 | $47K LangChain multi-agent loop | 4 agents ping-ponged for 11 days; $127→$891→$6,240→$18,400/week | [TechStartups](https://techstartups.com/2025/11/14/ai-agents-horror-stories-how-a-47000-failure-exposed-the-hype-and-hidden-risks-of-multi-agent-systems/) |
| Nov 2025 | Memory poisoning procurement fraud | Agent manipulated over 3 weeks to approve $500K purchases → $5M in fraudulent orders | [Lakera](https://www.lakera.ai/blog/agentic-ai-threats-p1) |
| 2025–2026 | Fortune 500 agentic cost overruns | $400M collective unbudgeted cloud spend | [AnalyticsWeek](https://analyticsweek.com/finops-for-agentic-ai-cloud-cost-2026/) |
| Feb 2026 | $82K Gemini API key theft | Stolen API key generated $82,314 in 48 hours (455x normal spend); Google cited shared responsibility model, refused refund; 2,863 live API keys found exposed on public websites | [The Register](https://www.theregister.com/2026/03/03/gemini_api_key_82314_dollar_charge/), [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/gemini-api-key-thief-racks-up-usd82-314-in-charges-in-just-two-days-victim-facing-bankruptcy-affected-devs-call-for-basic-guardrails-against-catastrophic-usage-anomalies) |
| Feb 2026 | $47K retry storm | 2.3M API calls over a weekend from misinterpreted error code | [RocketEdge](https://rocketedge.com/2026/03/15/your-ai-agent-bill-is-30x-higher-than-it-needs-to-be-the-6-tier-fix/) |
| Mar 2026 | ROME GPU crypto hijack | $1.2M in diverted GPU resources; agent created hidden reverse SSH tunnel | [Axios](https://www.axios.com/2026/03/07/ai-agents-rome-model-cryptocurrency) |
| Mar 2026 | Gartner FinOps Reckoning | Industry-wide recognition that inference = 85% of AI budget; agentic loops (10–20 LLM calls/task) are primary cost driver. Strategy Inc launches Mosaic Sentinel as cost governance response | [AnalyticsWeek](https://analyticsweek.com/finops-for-agentic-ai-cloud-cost-2026/) |

---

## OWASP Agentic Security Mapping

| OWASP Risk | AISVS Requirement | Relevance |
|------------|-------------------|-----------|
| ASI02: Tool Misuse & Exploitation | 9.1.1 | Recursive tool calls cause budget exhaustion |
| ASI06: Memory & Context Poisoning | 9.1.2 | Can trigger infinite retrieval loops; procurement fraud ($5M incident) |
| ASI07: Insecure Inter-Agent Communication | 9.1.2 | Enables multi-agent circular dependencies |
| **ASI08: Cascading Failures** | **9.1.3** | **Directly addresses circuit breakers, fan-out caps** |
| ASI10: Rogue Agents | 9.1.4 | Behavioral drift toward costly actions (ROME crypto mining) |
| LLM06: Excessive Agency | 9.1.1 | Agents with insufficient autonomy guardrails |
| LLM10: Unbounded Consumption | 9.1.1, 9.1.2 | Uncontrolled inference resource drain |

---

## Implementation Maturity

| Area | Maturity | Notes |
|------|----------|-------|
| Recursion/step limits in frameworks | **Medium** | LangGraph, OpenAI, CrewAI all have basic step limits. No dollar budgets. |
| Gateway-level budget enforcement | **Medium-High** | LiteLLM (tag budgets, provider routing), Bifrost (hard limits, 11µs overhead), Portkey (virtual key budgets), Traefik Triple Gate (proactive token estimation, MCP TBAC). Production-ready; rapid innovation in Q1 2026. |
| Circuit breakers for agents | **Low-Medium** | Microsoft AGT has them; LiteLLM/Bifrost provide binary cut-off. Multi-stage (throttle→sandbox→kill) is academic. |
| Cumulative cross-agent tracking | **Low-Medium** | OpenTelemetry GenAI Semantic Conventions (v1.37+) standardize agent span attributes (`gen_ai.usage.*`), enabling cross-vendor cost aggregation. Still requires custom enforcement logic on top. |
| Dollar-denominated budgets | **Low-Medium** | No framework-native support, but AgentBudget (OSS, Feb 2026) provides drop-in per-session dollar enforcement via SDK patching. Gateway/governance layer still required for org-wide enforcement. |
| Runtime agent sandboxing | **Medium** | NVIDIA OpenShell (out-of-process, deny-by-default, Apache 2.0), Jozu Agent Guard (zero-trust, tamper-resistant). Both March 2026. |
| Policy-as-code for budgets | **Medium** | Microsoft AGT, Galileo Agent Control, Kyndryl PaC (Feb 2026), NVIDIA OpenShell. OPA/Rego emerging as industry standard for fine-grained policy; AWS Cedar, Kyverno as alternatives. |
| Budget-aware reasoning | **Emerging** | Google BATS (arXiv 2511.17006) and BAVT (arXiv 2603.12634) show agents can self-limit tool usage when given budget signals — 31% cost reduction — but remains a research technique, not production-ready enforcement. |
| AI FinOps practices | **Medium** | 98% of orgs now manage AI costs (State of FinOps 2026). 44% have financial guardrails for agents. IDC: 92% report agent costs exceeded expectations. |
| Insurance/liability coverage | **Low** | AIUC launched July 2025 ($500B market projection). Lloyd's/Armilla AI liability policy. "Silent AI" coverage gap in traditional policies. |
| ISO 42001 certification | **Medium** | UKAS accreditation granted to NQA (January 2026) — first accredited AI management system certifications now available. Requires defining appropriate use boundaries and human oversight. Does not prescribe specific budget enforcement mechanisms but establishes governance framework for operational containment. |

---

## Cross-Chapter Links

| Related Section | Overlap |
|----------------|---------|
| [C02-01 Prompt Injection Defense](C02-01-Prompt-Injection-Defense.md) | Input-side rate limits and abuse prevention controls |
| [C04-06 Resource Management & Backup](C04-06-Resource-Management-Backup-Recovery.md) | Infrastructure-level resource quotas, autoscaling controls |
| [C09-02 High-Impact Action Approval](C09-02-High-Impact-Action-Approval.md) | Human approval gates for costly operations |
| [C09-03 Tool and Plugin Isolation](C09-03-Tool-and-Plugin-Isolation.md) | Per-tool CPU/memory/execution time limits |
| [C09-08 Multi-Agent Isolation](C09-08-Multi-Agent-Isolation.md) | Cross-agent budget enforcement, circular dependency detection |
| [C13-04 Performance & Behavior Telemetry](C13-04-Performance-Behavior-Telemetry.md) | Cost observability, anomaly detection for spend spikes |

---

## Related Standards & References

- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — mandates circuit breakers and transactional rollback
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/)
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [NIST CAISI AI Agent Standards Initiative (February 2026)](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) — COSAiS agent-specific overlays expected mid-to-late 2026; advises updating SP 800-160 and SP 800-218 for action authority, tool invocation security, and operational containment
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit)
- [FinOps Foundation: FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/) — Crawl/Walk/Run maturity model
- [Intelligent AI Delegation Framework (arXiv 2602.11865)](https://arxiv.org/abs/2602.11865) — escrow-based budget delegation
- [Azure AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Denial of Wallet: Cost-Aware Rate Limiting](https://handsonarchitects.com/blog/2025/denial-of-wallet-cost-aware-rate-limiting-part-2/)
- [Agentic Resource Exhaustion: The Infinite Loop Attack](https://instatunnel.substack.com/p/agentic-resource-exhaustion-the-infinite)
- [The $400M Cloud Leak: AI FinOps 2026](https://analyticsweek.com/finops-for-agentic-ai-cloud-cost-2026/)
- [Algorithmic Circuit Breakers (Arion Research)](https://www.arionresearch.com/blog/algorithmic-circuit-breakers-preventing-flash-crashes-of-logic-in-autonomous-workflows)
- [AIUC — AI Agent Liability Insurance](https://fortune.com/2025/07/23/ai-agent-insurance-startup-aiuc-stealth-15-million-seed-nat-friedman/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — standardized agent span attributes for cost tracking (`gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`); v1.37+
- [EU AI Act — Full Applicability August 2026](https://thefuturesociety.org/aiagentsintheeu/) — governs autonomous agents through risk assessment, transparency, technical deployment controls, and human oversight; agentic tool invocation across borders exposes compliance gaps
- [Traefik Triple Gate: LLM and MCP Runtime Governance (March 2026)](https://www.helpnetsecurity.com/2026/03/17/traefik-labs-triple-gate-new-capabilities/) — proactive token estimation, circuit breaker failover, TBAC for MCP
- [CSA Research Note: NIST CAISI Compliance Imperative (March 2026)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/03/CSA_research_note_nist_caisi_ai_agent_standards_compliance_20260311.pdf)
- [NVIDIA OpenShell: Secure Autonomous AI Agents (March 2026)](https://developer.nvidia.com/blog/run-autonomous-self-evolving-agents-more-safely-with-nvidia-openshell/) — out-of-process policy enforcement, deny-by-default sandbox
- [Jozu Agent Guard: AI Security That Agents Cannot Disable (March 2026)](https://finance.yahoo.com/news/jozu-launches-agent-guard-ai-100000670.html) — zero-trust AI runtime with MCP integration
- [Kyndryl Policy-as-Code Agentic AI Governance (February 2026)](https://www.kyndryl.com/us/en/about-us/news/2026/02/policy-as-code-agentic-ai-governance) — deterministic execution, audit-by-design
- [Execution Budgets for Autonomous Systems (Rack2Cloud)](https://www.rack2cloud.com/ai-inference-execution-budgets/) — four-layer enforcement stack architecture
- [The Hidden Cost of Agentic Failure (O'Reilly Radar)](https://www.oreilly.com/radar/the-hidden-cost-of-agentic-failure/) — Lusser's Law reliability decay in multi-agent systems
- [Bessemer: Securing AI Agents — The Defining Cybersecurity Challenge of 2026](https://www.bvp.com/atlas/securing-ai-agents-the-defining-cybersecurity-challenge-of-2026)
- [Budget-Aware Tool-Use Enables Effective Agent Scaling (arXiv 2511.17006)](https://arxiv.org/abs/2511.17006) — Google/NYU/UCSB: Budget Tracker + BATS framework for prompt-level budget awareness; 31% cost reduction
- [Spend Less, Reason Better: Budget-Aware Value Tree Search (arXiv 2603.12634)](https://arxiv.org/abs/2603.12634) — BAVT: budget-conditioned node selection for multi-hop reasoning; surpasses 4x baselines under constraints
- [AgentBudget: Real-Time Dollar Budgets for AI Agents](https://github.com/sahiljagtap08/agentbudget) — OSS per-session dollar enforcement SDK; nested sub-agent budgets; 60+ model pricing
- [$82K Gemini API Key Theft (February 2026)](https://www.theregister.com/2026/03/03/gemini_api_key_82314_dollar_charge/) — 455x bill spike from stolen credential; 2,863 exposed keys found
- [ISO/IEC 42001 UKAS Accreditation (January 2026)](https://cloudsecurityalliance.org/blog/2026/03/18/understanding-iso-42001-responsible-ai-governance-in-an-evolving-regulatory-landscape) — first accredited AI management system certifications now available; requires defining appropriate use boundaries and human oversight for higher-risk AI applications

---

## Open Research Questions

- What are appropriate default budget thresholds for different agent use cases? Emerging benchmarks: $100/hour hard cap, 10-step limit, $3,200–$13,000/month operational range.
- How should budgets be allocated across sub-agents in hierarchical systems? The escrow-based delegation pattern (arXiv 2602.11865) proposes recursive budget partitioning with bond slashing.
- Can adaptive budgets (dynamically adjusting based on task complexity) be made safe, or do they introduce exploitable flexibility?
- How do you handle budget enforcement for agents making external API calls with their own billing (SaaS-to-SaaS worm pattern)?
- Should agent frameworks standardize a budget/cost-ceiling API, or should this remain in the gateway/governance layer?
- How do you detect multi-agent circular dependencies where each agent individually appears to be making progress (the $47K LangChain pattern)?
- How should the recursive pattern of "AI agents managing AI agent budgets" (agentic FinOps) itself be bounded?
- The EU AI Act (full applicability August 2026) requires human oversight and risk assessment for autonomous agents, but doesn't prescribe specific budget enforcement mechanisms. How should execution budget requirements map to EU compliance obligations, particularly for cross-border tool invocations?
- As proactive token estimation matures (Traefik Triple Gate), can pre-LLM cost prediction become reliable enough to replace post-hoc budget enforcement?
- Budget-aware reasoning (Google BATS, BAVT) shows agents can self-regulate tool usage when given budget signals — does this reduce the need for hard external enforcement, or is it too easily bypassed by adversarial inputs?
- The $82K Gemini API key theft exposed the "shared responsibility" gap: providers refuse to cap runaway usage from stolen credentials. Should budget ceilings be mandatory provider-side defaults, or is this fundamentally a customer responsibility?

---

[C09 Index](C09-Orchestration-and-Agents.md) | [README](README.md)
