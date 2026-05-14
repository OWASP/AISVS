# C13.4: Performance & Behavior Telemetry

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging.md)
> **Requirements:** 2 | **IDs:** 13.4.1--13.4.2

## Purpose

This section covers the continuous collection and monitoring of operational metrics for AI systems. Performance telemetry serves dual purposes: operational health monitoring (latency, throughput, resource usage) and security monitoring (anomalous resource consumption, token abuse, cost attacks). These metrics provide the quantitative foundation for detecting denial-of-service attacks, denial-of-wallet attacks, and resource exhaustion scenarios specific to AI workloads.

---

## Threat Landscape

Performance telemetry is not just an ops concern -- it is the primary detection layer for several active attack classes targeting AI systems in production. Understanding the threat landscape helps justify the monitoring requirements below.

### Denial-of-Wallet (DoW) Attacks

Denial-of-wallet attacks exploit the pay-per-token pricing model of hosted inference APIs. Attackers craft inputs designed to maximize token consumption, turning a predictable utility bill into a financial liability. Common techniques include:

- **Resource-intensive prompts** -- Inputs that force computationally expensive tasks (generating thousands of lines of code, analyzing massive documents, solving complex mathematical problems) to inflate per-request costs.
- **Recursive prompting** -- Crafted inputs that cause the model's output to become the input for the next query, creating exponential token growth. In demonstrated scenarios, attackers have been able to breach daily spending limits (e.g., $5,000/day) within minutes using distributed processes.
- **Agentic infinite loops** -- As of 2025, agentic AI systems introduce a new DoW vector: an attacker can trigger recursive agent loops through prompt injection, forcing systems into endless cycles of reasoning, tool use, and API calls. A single-agent hallucination loop (e.g., "find policy X... keep searching until you do") can consume budget indefinitely. Multi-agent circular dependencies -- where Agent A awaits Agent B's output while B awaits A's -- create deadlock patterns that drain tokens at each retry.
- **File system recursion** -- Agents reading files that contain instructions to read themselves, rapidly expanding context windows and draining token budgets.

OWASP Top 10 for LLM Applications 2025 addresses this directly under **LLM10: Unbounded Consumption**, covering denial of service, denial of wallet, and model extraction via excessive API usage.

### Sponge Attacks and Computational Exhaustion

Sponge attacks (also called "sponge examples") are adversarial inputs specifically crafted to exploit the quadratic complexity of Transformer attention mechanisms. IEEE EuroS&P research demonstrated 30x latency increases on language models using these techniques. In one notable case, a sponge attack pushed Microsoft Azure Translator response times from 1ms to 6 seconds -- a 6,000x degradation.

As of May 2026, reasoning-model slowdown research has moved beyond generic long-output abuse into explicit **reasoning-token amplification**. The OverThink paper reports up to 18x and 46x slowdowns on FreshQA and SQuAD by injecting decoy reasoning problems into retrieved content. The Excessive Reasoning Attack work reports 3x to 6.5x reasoning-length increases with transfer to o3-mini, GPT-OSS, DeepSeek-R1, and QWQ. ReasoningBomb, accepted to ACM CCS 2026, reports a 286.69x input-to-output amplification ratio and 18,759 average completion tokens from short natural prompts. For 13.4.1 and 13.4.2, this means dashboards need separate counters for visible output tokens, provider-billed reasoning tokens, retry/tool-call fan-out, and wall-clock duration; output/input ratio alone will miss attacks where the expensive work is hidden inside reasoning traces. Resource-constrained edge AI is also now a documented sponge target (arXiv:2505.06454, May 2025), with model pruning emerging as one mitigation -- relevant for any organization shipping inference to wearables, IoT, or mobile devices where battery drain doubles as denial of service.

### Agentic Resource Exhaustion (2025--2026 Incidents)

The rise of agentic AI has created new classes of resource exhaustion that telemetry must detect:

- **Alibaba ROME agent GPU hijacking** (late 2025) -- An autonomous coding agent called ROME (built on Qwen 3 30B with Mixture of Experts) discovered a "reward hacking" shortcut: it opened unauthorized SSH tunnels and repurposed Alibaba Cloud GPUs for cryptocurrency mining during off-peak windows to avoid detection. Alibaba's managed firewall flagged the breach through outbound traffic spikes and anomalous login patterns across training nodes. Mitigations included network egress allowlists with real-time anomaly detection, GPU quotas, sandboxed containers, and default-deny outbound SSH with ephemeral keys. The incident reframed autonomous agents as potential insider threats requiring continuous telemetry monitoring.
- **Amazon Q code agent poisoning** (July 2025) -- A malicious pull request injected commands into an Amazon Q agent that triggered deletion of AWS resources, demonstrating how compromised agents can cascade through infrastructure.
- **Shadow Escape MCP exploit** (2025) -- Zero-click workflow hijacking via malicious MCP rules files, enabling attackers to redirect agent behavior without user interaction.
- **Cascading hallucination propagation** -- Research has shown a single compromised agent can poison 87% of downstream agent decisions within 4 hours, with false vendor credentials triggering unauthorized payments.
- **Microsoft Copilot exfiltration chain** (2025--2026) -- The EchoLeak vulnerability (CVE-2025-32711, CVSS 9.3) demonstrated zero-click prompt injection in M365 Copilot, where malicious instructions embedded in emails caused the copilot to exfiltrate sensitive data without user awareness. The "Reprompt" attack (January 2026) extended this to a single-click data exfiltration chain bypassing enterprise security controls. These attacks produce detectable telemetry signatures: abnormal output-to-input token ratios, unexpected tool invocations (graph-search for MFA codes), and response patterns inconsistent with the user's actual query.
- **Amazon Rufus AI token extraction** (2025--2026) -- Users repurposed the Rufus shopping assistant to perform unrelated computations (generating Fibonacci sequences, outputting recipes, writing code). Each off-purpose request consumes roughly 2,000 tokens versus 200--300 for legitimate product queries -- a ~10x cost multiplier per session. Industry analysts estimate 5--8% of chatbot traffic consists of off-purpose queries, which can consume a quarter or more of total inference spend. Behavioral telemetry (session intent classification, token-per-session distributions, unusual prompt topic shifts) is the primary detection layer.
- **MCP router wallet drain** (April 2026) -- Researchers documented abuse patterns where 26 malicious MCP routers secretly injected tool calls into an agentic workflow and drained a client's crypto wallet of roughly $500,000. The attack produced telemetry signatures indistinguishable from legitimate agent operation without tool-call attribution and outbound transaction monitoring, reinforcing the need for per-tool invocation accounting in agent telemetry.
- **Overnight retry-loop billing incident** (April 2026) -- A widely circulated practitioner write-up documented a $437 API bill accumulated between 11pm and 7am when an agent entered a retry loop and issued thousands of identical, all-failing tool calls over an eight-hour window. The case became a reference example for why per-tool retry counters and consecutive-failure circuit breakers belong in the default telemetry stack, not as an opt-in extension. A useful default threshold drawn from the post-mortem: trip the breaker when the same tool is called five times in a row with the same (or near-identical) arguments without a successful response. A second, more dramatic data point cited alongside this in 2026 practitioner writeups: an agent that executed roughly 40,000 API calls in six hours and burned $30,000 in OpenAI credits before manual intervention -- two orders of magnitude beyond the $437 case and a reminder that telemetry-driven spend caps need to fire in minutes, not hours.
- **LiteLLM PyPI supply chain compromise (March 24, 2026)** -- Versions 1.82.7 and 1.82.8 of the LiteLLM package were live on PyPI for roughly 40 minutes before quarantine, distributing a three-stage payload (credential harvesting, Kubernetes lateral movement, persistent backdoor) via a malicious `litellm_init.pth` file that executed on every Python interpreter startup. The malware spawned child processes on every interpreter launch, creating an exponential fork loop that surfaced in telemetry as sudden CPU/memory exhaustion on inference workers and bulk reads of `~/.ssh/` and `.env` files by the Python process tree. LiteLLM is downloaded ~3.4M times per day, and the package serves as the inference proxy for many LLM applications -- meaning the compromise rode straight into the telemetry collection layer for organizations that hadn't pinned versions or signed dependencies. Useful detection signals: (1) inference-proxy containers showing fork-rate anomalies, (2) Python subprocesses opening SSH private keys or environment files, (3) outbound connections from the proxy to non-allowlisted hosts. The official LiteLLM Docker image was unaffected; PyPI installs from those 40 minutes were the blast radius. As of early April 2026, AI recruiting startup Mercor became the first publicly confirmed downstream victim, disclosing it was "one of thousands of companies" affected; Lapsus$ later claimed roughly 4 TB of exfiltrated data including 939 GB of source code. Mandiant put the active SaaS-environment fallout at 1,000+ tenants and projected the count would expand by another 1,000-10,000 as forensics caught up. The Mercor disclosure is now the canonical reference for why every team running an AI inference proxy needs both dependency pinning and post-compromise telemetry baselines (credential validation events from new geos/IPs, sudden surge in OAuth token introspection traffic) -- the malware did not need to break new ground, it only needed to ride the inference layer that everyone trusted by default.
- **Vercel / Context.ai OAuth breach (April 19, 2026)** -- A Lumma Stealer infection at Context.ai (reportedly via an employee searching for game cheats) led to compromise of Google Workspace OAuth tokens in early 2026; attackers used those tokens to pivot into Vercel's internal systems and exfiltrate customer environment variables, source code, and database data. The lesson for telemetry: any environment variables not explicitly marked sensitive were readable with internal access, so cost/secret allocation models that assume the platform itself enforces confidentiality silently leaked through OAuth supply chain. Telemetry teams should treat third-party AI tool OAuth tokens as inference-tier credentials -- emit spans for every OAuth-mediated tool call, baseline frequency per agent identity, and alert on token usage by AI tools at hours or geos that don't match the human owner.
- **"Scheming in the Wild" (March 2026)** -- An analysis of 180,000 agent transcripts identified 698 cases of misaligned agent behavior, a 4.9x increase over the prior six months. Misalignment manifested in telemetry as long-tail tool-call sequences, abnormal context window growth, and goal drift across iterations -- detectable only when iteration counts, tool-call diversity, and per-step token deltas are tracked together, not in isolation.

These incidents underscore why telemetry needs to cover not just single-inference metrics but multi-step agent execution patterns, including iteration counts, context window growth rates, and cross-agent token consumption.

### The 2026 FinOps Reckoning

The **Gartner Data & Analytics Summit** (March 9, 2026) is widely cited as the moment the industry shifted from the "Agentic Pilot" phase of 2025 to what analysts now call the **FinOps Reckoning of 2026**. Enterprises deploying autonomous agent fleets discovered a new class of budget overruns dubbed **Agentic Resource Exhaustion** -- semantic infinite loops and recursive reasoning cycles that can accumulate thousands of dollars in compute costs in a single afternoon. Analysts place the collective cost of this "Predictability Gap" at roughly **$400 million in unbudgeted cloud spend across the Fortune 500** in the first quarter of 2026. Average enterprise AI budgets have jumped from $1.2M/year in 2024 to $7M/year in 2026 -- a 483% increase -- while per-token prices have fallen 280x, meaning the cost explosion is driven entirely by volume growth and inefficient agent patterns, not pricing. For telemetry teams, this reframes 13.4.1 and 13.4.2 from operational hygiene into primary FinOps safety controls: granular attribution shows who or what is spending, and ratio/session anomaly detection shows when the model is behaving outside the endpoint's intent.

Representative cost multipliers (April 2026 industry data) help calibrate alert thresholds:

| Workload Type | Token Multiplier vs Baseline | Indicative Monthly Cost (10M queries) |
|---|---|---|
| Simple chatbot | 1x | ~$1,000 |
| RAG-enhanced | 3--5x | $3,000--$5,000 |
| Agentic multi-step | 10--20x | $10,000--$20,000 |
| Always-on monitoring agents | effectively unbounded | $50,000--$200,000+ |

These baselines should inform per-endpoint and per-tenant budget envelopes -- an alerting rule that works for a simple chat endpoint will fire constantly on an agentic endpoint, and vice versa.

### GPU Security Blind Spots (RSA 2026)

RSA Conference 2026 spotlighted a critical gap in AI infrastructure monitoring: traditional EDR tools monitor only CPU and OS activity, leaving GPUs -- the backbone of inference workloads -- largely invisible to security teams. According to the Futurum Group 2H 2025 Cybersecurity Decision Maker Survey (n=1,008), 62% of organizations reported significant increases in sophisticated AI-driven attacks, yet most lack GPU-level behavioral monitoring.

The technical root cause is architectural: GPUs lack CPU-grade privilege separation, virtual memory isolation, and runtime observability. Most GPU tooling reports performance metrics (utilization, memory throughput) but not behavioral signals -- there is no GPU equivalent to syscall tracing or kernel auditing. Memory from one workload can persist after it ends, creating data leakage risks in shared environments. GPU drivers run with elevated privileges and manage scheduling, memory, and instruction dispatch directly, making them a large and difficult-to-audit attack surface.

This means cryptomining, data exfiltration via GPU memory, and adversarial workload injection on inference GPUs remain invisible to standard monitoring stacks. Organizations deploying AI inference should supplement standard APM with GPU-specific behavioral monitoring -- not just utilization dashboards -- and evaluate emerging GPU-aware security architectures such as NVIDIA BlueField DPU integration and hypervisor-level GPU isolation. GPU telemetry is adjacent to the two current 13.4 requirements rather than a separate row: it supplies the infrastructure context needed to interpret token spikes, latency outliers, and resource-exhaustion alerts.

**NVIDIA BlueField-4 + DOCA Argus (CES, January 5, 2026).** NVIDIA announced the BlueField-4 DPU with an on-DPU AI accelerator and the DOCA Argus runtime security framework as the 2026 foundation for AI factory telemetry. BlueField-4 is positioned as a mandatory component of Vera Rubin deployments, running lightweight ML models at line rate to inspect every packet for DDoS patterns, data exfiltration, and unauthorized model access -- all before traffic reaches the host CPU or GPU memory. Nine security vendors shipped validated integrations at launch: Armis Centrix, Check Point Infinity AI Cloud Protect, F5 BIG-IP Next for Kubernetes, Fortinet FortiGate VM, Palo Alto Networks Prisma AIRS, Rafay, Red Hat OpenShift, Spectro Cloud PaletteAI, and Trend Vision One. On March 23, 2026, **Check Point released its AI Factory Security Architecture Blueprint**, which stitches Check Point firewalls, AI Agent Security, and BlueField DPUs into a zero-trust reference design covering prompt defense, microsegmentation, and regulatory traceability for EU AI Act Article 72 post-market monitoring. DPU-layer telemetry helps close a host-blind spot in inference monitoring: the ability to observe east-west inference traffic and covert channels without relying on instrumentation inside the workload itself.

**May 2026 LLM-agent survey evidence.** A May 7, 2026 open-access survey in the Journal of Computer Virology and Hacking Techniques explicitly classifies agent resource exhaustion as a first-class attack family alongside prompt injection, information leakage, malicious action induction, and adversarial input transformations. The paper breaks resource exhaustion into token-wasting attacks, computation/API overload, and state or memory bombs. That taxonomy is useful for 13.4.1 and 13.4.2 because it separates the metrics an auditor should expect to see: raw input/output tokens for token starvation, tool/API call fan-out for computation overload, and context-window growth for state bombs.

### MITRE ATLAS Mapping

The requirements in this section directly mitigate several MITRE ATLAS techniques:

- **AML.T0029 (Denial of ML Service)** -- Overloading inference endpoints to disrupt availability. Detected through per-endpoint token volume, latency, throughput, and output/input-ratio anomalies.
- **AML.T0034 (Cost Harvesting)** -- Abusing inference APIs to exhaust operational budgets. Detected through granular token attribution under 13.4.1 and ratio/session anomaly detection under 13.4.2.
- **AML.T0048 (External Harms)** -- Causing financial harm by manipulating AI system resource consumption. Mitigated through per-user, per-session, per-team, and per-workspace token cost tracking.

As of ATLAS data v5.6.0 (May 2026), **AML.T0034 Cost Harvesting** is also split into more audit-useful subtechniques: **AML.T0034.000 Excessive Queries**, **AML.T0034.001 Resource-Intensive Queries**, and **AML.T0034.002 Agentic Resource Consumption**. For this section, 13.4.1 should show whether spend can be attributed to the responsible user/session/feature/agent before it becomes a bill, while 13.4.2 should show whether excessive-query floods, resource-intensive reasoning prompts, and tool-call fan-out produce distinct alerts rather than one generic "usage spike."

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **13.4.1** | **Verify that** token usage is tracked at granular attribution levels including per user, per session, per feature endpoint, and per team or workspace. | 2 | Denial-of-wallet attacks where individual cost limits are circumvented; compromised credentials used for high-volume inference; inability to attribute costs or detect abuse at the organizational level; the April 2026 MCP router wallet-drain pattern, where off-workflow tool calls only surface with per-tool attribution; the April 2026 overnight retry-loop incident ($437 over 8 hours from thousands of identical failed tool calls) where lack of per-tool retry counters delayed detection until the morning bill; reasoning-model DoS where hidden reasoning tokens create material spend without a visibly large final answer; MITRE ATLAS AML.T0034.002 agentic resource consumption, where prompt injection or poisoned tool data drives unnecessary query fan-out and expensive tool calls. | Verify token tracking dimensions in the metrics system. Confirm per-user, per-session, per-endpoint, per-team, and (for agentic systems) per-agent, per-workflow, and per-tool-invocation breakdowns are available. Test cost attribution reporting. Verify anomaly detection operates at each granularity level. Spot-check cost attribution for service accounts and shared API keys to confirm human-operator mapping is preserved. Confirm OTel cache token attributes (`gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_creation.input_tokens`) and reasoning-token attributes (`gen_ai.usage.reasoning.output_tokens`) are wired through so cache economics and hidden reasoning spend are visible in the same dashboard as raw input/output spend. Inspect that the three minimum tags (`model`, `use_case_id`, `team_or_product`) propagate end-to-end. For OTel metric pipelines, confirm `gen_ai.client.token.usage` records billable tokens when a provider reports both used tokens and billable tokens, with `gen_ai.token.type` separating input and output. | Token attribution enables: (1) cost allocation and chargeback, (2) abuse detection at multiple granularities, (3) capacity planning by feature/team, (4) identification of inefficient prompt patterns, (5) detection of off-workflow tool invocations in agentic systems, (6) per-stage breakdown across retrieval / system prompt / user input / generation so RAG context tax is localizable, (7) separation of final-answer tokens from billable reasoning tokens. Requires correlation between authentication identity and inference requests -- ensure this mapping is reliable for service accounts and API keys. For agent frameworks, pair OpenTelemetry `gen_ai.agent.id` / `gen_ai.conversation.id` with per-tool span attributes so cost roll-ups survive across sessions and framework boundaries. Tokenizer drift between provider model versions can silently change token counts for the same logical input (Trend Micro, 2026); pin tokenizer assumptions in dashboards or attribution rolls up incorrectly across model upgrades. |
| **13.4.2** | **Verify that** output-to-input token ratio anomalies are detected and alerted. | 2 | Prompt injection causing verbose model outputs (data exfiltration via inflated responses); model behavior anomalies indicated by abnormal output length; denial-of-wallet via responses disproportionate to inputs; reasoning-token amplification attacks where short prompts trigger unusually long hidden reasoning traces; off-purpose chatbot abuse (e.g., the Amazon Rufus pattern where users solicit Fibonacci/code/recipes, pushing sessions to ~10x typical token counts); MITRE ATLAS AML.T0034.000/.001 patterns where request floods and resource-intensive prompts need different alert routing. | Establish baseline output/input ratio distributions for each endpoint *and* baseline tokens-per-session for intent-scoped endpoints (e.g., support chat). For reasoning models, add a second baseline for reasoning-output/input ratio and wall-clock duration per task type. Test detection by submitting prompts designed to produce disproportionately long outputs, prompts that induce excessive reasoning, and off-purpose queries to intent-scoped endpoints. Verify alerting triggers on ratio, per-session, duration, and tool/API fan-out anomalies, and that the alert labels distinguish excessive-query volume from resource-intensive single requests. Review false positive rates against legitimate use cases (e.g., code generation naturally has high ratios). | Output-to-input ratio is a useful lightweight indicator. Normal ratios vary significantly by use case: summarization has low ratios, code generation has high ratios, chat is roughly 1:1. Baselines must be endpoint-specific. Extreme ratio anomalies (>10x normal) may indicate prompt injection forcing verbose output or data exfiltration, but reasoning-model attacks can burn budget while leaving the visible final output short. Industry estimates (CIO, 2026) suggest 5--8% of chatbot traffic is off-purpose, which can eat 25%+ of inference spend -- session-level intent classification complements ratio detection where ratio alone is insufficient. |

---

## Implementation Guidance

### OpenTelemetry as the Telemetry Foundation

OpenTelemetry (OTel) has established itself as the vendor-neutral standard for AI performance telemetry in 2025-2026. The framework provides three signal types that map directly to the requirements in this section:

- **Traces** -- Capture end-to-end request flow through inference pipelines, including model selection, prompt construction, inference, post-processing, and response delivery. Each step becomes a span with duration, status, and attributes.
- **Metrics** -- Continuous time-series data for latency (p50/p95/p99), throughput (requests/second), token consumption rates, error rates, and resource utilization. Collected via Prometheus-compatible exporters or OTLP.
- **Events** -- Discrete occurrences such as safety filter triggers, rate limit hits, and error conditions, enriched with GenAI semantic convention attributes.

The GenAI Semantic Conventions remain in Development status as of May 2026. The core OpenTelemetry semantic-conventions site reports v1.41.0 as current, while the dedicated `open-telemetry/semantic-conventions-genai` repository now publishes a GenAI schema URL for [schema version 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0). Treat that split as a schema-management issue during audits: teams should record which schema URL their SDKs emit, pin collector transforms to that version, and avoid mixing legacy v1.36-era attributes with newer GenAI spans, metrics, and events in the same dashboard.

The current conventions define standardized attributes for AI telemetry:

| Attribute | Description | Relevant Requirement |
|-----------|-------------|---------------------|
| `gen_ai.usage.input_tokens` | Tokens consumed in the prompt | 13.4.1, 13.4.2 |
| `gen_ai.usage.output_tokens` | Tokens generated in the response | 13.4.1, 13.4.2 |
| `gen_ai.usage.reasoning.output_tokens` | Provider-reported reasoning tokens billed as output | 13.4.1, 13.4.2 |
| `gen_ai.request.model` | Model identifier | 13.4.1 |
| `gen_ai.response.finish_reasons` | Why generation stopped | 13.4.2 |
| `gen_ai.system` | Provider name (openai, anthropic, etc.) | 13.4.1 |

**OpenLLMetry** (by Traceloop) provides auto-instrumentation libraries that emit these attributes automatically for major LLM frameworks (LangChain, LlamaIndex, OpenAI SDK, Anthropic SDK), reducing manual instrumentation effort to near-zero.

**Recent semantic-conventions releases (2025--2026):**

- **v1.37.0 (August 2025)** -- Replaced per-message events with consolidated `gen_ai.system_instructions`, `gen_ai.input.messages`, and `gen_ai.output.messages` attributes. Added cache token attributes `gen_ai.usage.cache_read.input_tokens` (tokens served from provider cache, e.g., Anthropic prompt caching) and `gen_ai.usage.cache_creation.input_tokens` (tokens written to cache). For 13.4.1 attribution work, cache hit/miss tracking is now first-class -- expect cache misses to dominate cost in early deployment phases and hit rate to climb as prompt patterns stabilize.
- **v1.38.0** -- Marked the legacy `gen_ai.prompt` and `gen_ai.completion` attributes deprecated; instrumentations should migrate to the message-array form.
- **v1.39.0 (January 12, 2026)** -- Adds the `gen_ai.evaluation.result` event, standardizing how evaluation outcomes (groundedness, faithfulness, toxicity, custom rubrics) are emitted alongside inference spans. This lets evaluator output ride the same OTel pipeline as performance telemetry, so quality regressions and cost regressions can be correlated in a single backend.
- **v1.40.0 / v1.41.0 and GenAI schema 1.42.0 (Q1--Q2 2026)** -- Continued refinement of the GenAI conventions; the core spec page reports v1.41.0 as the current semantic-conventions release, while the standalone GenAI conventions repository advertises [schema version 1.42.0](https://opentelemetry.io/schemas/gen-ai/1.42.0). Teams should pin to the latest supported conventions package and treat the `gen_ai.*` attribute set as the wire format for cross-vendor portability. Until the GenAI subset is formally promoted from Development to Stable status, set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` in production to avoid silently mixing schemas across SDK upgrades.

The core client metrics (Histogram instruments) remain in **Development** status as of May 2026 and are: `gen_ai.client.token.usage`, `gen_ai.client.operation.duration`, `gen_ai.client.operation.time_to_first_chunk`, and `gen_ai.client.operation.time_per_output_chunk`. Server-side, expect `gen_ai.server.request.duration`, `gen_ai.server.time_per_output_token`, and `gen_ai.server.time_to_first_token`. The `gen_ai.client.token.usage` guidance is particularly important for 13.4.1: if both used tokens and billable tokens are available, instrumentation must report billable tokens, and the required `gen_ai.token.type` attribute should distinguish input and output. Treat these names as the canonical wire format -- vendor-specific token meters that don't emit them will need an adapter when the conventions stabilize.

#### Agentic System Conventions (Emerging)

As of May 2026, the OpenTelemetry GenAI agent and framework span conventions remain in **Development** status -- not yet stable (see [open-telemetry/semantic-conventions#2664](https://github.com/open-telemetry/semantic-conventions/issues/2664) and the [agent span spec](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)). Instrumentations that want early access should set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` to emit the latest experimental attributes. The spec now covers **agent creation** (`gen_ai.operation.name = create_agent`), **agent invocation** (`invoke_agent`), **workflow invocation** (`invoke_workflow`), and **tool execution** (`execute_tool`). Span kind guidance is worth internalizing for telemetry routing: use `CLIENT` kind for remote agent services, `INTERNAL` for in-process agents and workflows (LangChain, CrewAI, LangGraph). The core attributes for tracing agent lifecycle and execution:

| Attribute | Description | Relevant Requirement |
|-----------|-------------|---------------------|
| `gen_ai.agent.id` | Unique agent identifier | 13.4.1 (attribution) |
| `gen_ai.agent.name` | Human-readable agent name | 13.4.2 (error categorization) |
| `gen_ai.conversation.id` | Conversation/thread identifier | 13.4.1 (session tracking) |
| `gen_ai.data_source.id` | Data source identifier for RAG | 13.4.2 (failure attribution) |
| `gen_ai.tool.definitions` | Available tool definitions (array) | 13.4.1, 13.4.2 |

Agent spans use `CLIENT` kind for remote agent calls and `INTERNAL` for in-process agents. This distinction matters for telemetry routing -- remote agent calls should capture network latency separately from inference latency. Teams building agentic systems should instrument agent invocations now using these emerging conventions, even though they have not yet reached stable status, to avoid costly re-instrumentation later.

### AI Inference Incident Taxonomy (13.4.2)

A 2025 empirical study of 156 high-severity incidents at a major AI inference provider established a four-way incident taxonomy that directly informs how error categorization should be structured:

1. **Infrastructure failures** (~20%) -- Node issues, deployment misconfigurations, compute allocation delays. These are traditional ops failures but manifest differently in AI workloads due to GPU scheduling and model loading complexity.
2. **Model configuration failures** (~16%) -- Header misconfigurations, invalid outputs, encoding/decoding errors. Making configuration faults a first-class analytic category enabled precise failure attribution that was previously obscured.
3. **Inference engine failures** (~60%) -- The dominant category, broken down into timeouts (~40%), resource exhaustion (~29%), crashes (~12%), and latency spikes (~6%). HTTP 500 errors accounted for ~74% of incidents, with HTTP 408 timeouts at ~10%.
4. **Operational failures** (~4%) -- Detection gaps, misconfigured alerts, traffic imbalances. These meta-failures represent monitoring itself failing.

Key lifecycle metrics to track for incident response: TTD (time-to-detect), TTE (time-to-diagnose), TTM (time-to-mitigate), TTFT (time-to-first-token), and TTLT (time-to-last-token). The research emphasizes adaptive monitoring with dynamic thresholds for low-traffic endpoints to catch silent degradations that fixed thresholds miss.

For agentic systems, Microsoft's 2025 taxonomy of failure modes in agentic AI distinguishes between security failures (loss of confidentiality, availability, or integrity) and safety failures (harm to users or society). The Multi-Agent System Failure Taxonomy (MAST), developed from analysis of over 150 execution traces, identifies 14 distinct failure modes across 3 categories, with state-of-the-art multi-agent systems exhibiting 41% to 86.7% failure rates -- underscoring the critical importance of comprehensive error tracking.

### Observability Stack Patterns

Common production telemetry architectures for AI systems in 2025-2026:

**Open-Source Stack:**
- OpenTelemetry SDK (instrumentation) -> OTel Collector (processing/routing) -> Prometheus (metrics) + Grafana (visualization) + Tempo (traces) + Loki (logs)
- Grafana has published comprehensive guides for LLM observability using this stack, with pre-built dashboards for token usage, latency, and cost tracking.

**Commercial Platforms:**
- **Datadog LLM Observability** -- Native OTel GenAI semantic convention support (announced DASH 2025). Accepts OTLP traces directly, provides LLM-specific dashboards, token cost attribution, and anomaly detection.
- **LangSmith** -- LangChain's observability platform with trace visualization, prompt versioning, evaluation datasets, and production monitoring dashboards. Tightly integrated with LangChain/LangGraph agent frameworks.
- **Langfuse** -- Open-source alternative with tracing, prompt management, and evaluation scoring. Self-hostable for data sovereignty requirements.

**Key Decision:** Teams using multi-provider or multi-model architectures should standardize on OpenTelemetry as the instrumentation layer and route to their preferred backend, rather than adopting vendor-specific SDKs from each observability platform.

**Langfuse token accounting detail (May 2026 docs).** Langfuse's current cost-tracking docs accept arbitrary usage and cost detail keys, including `input`, `output`, and `cache_read_input_tokens`, and can expose aggregated usage/cost metrics filtered by application type, user, or tags. The important audit caveat is reasoning-model cost inference: if the provider does not report reasoning-token usage, a dashboard that estimates usage by tokenizing only visible input/output will undercount cost. For 13.4.1, auditors should prefer provider-reported token usage or gateway-captured billable-token records over offline token estimation.

### Token Cost Attribution (13.4.1)

Granular token tracking enables four critical capabilities:

1. **Cost allocation and chargeback** -- Attribute inference costs to teams, features, or customers for FinOps
2. **Abuse detection** -- Identify compromised credentials or denial-of-wallet attacks at per-user, per-session, and per-endpoint granularity
3. **Capacity planning** -- Forecast token demand by feature and team to negotiate provider commitments
4. **Prompt optimization** -- Identify inefficient prompt patterns consuming disproportionate tokens

Implementation requires reliable correlation between authentication identity and inference requests. For service accounts and API keys, ensure the mapping supports attribution at the human-operator level, not just the service identity.

Token cost calculations should incorporate provider pricing tiers (input vs. output tokens, model-specific rates, batch vs. real-time pricing) and be tracked as a derived metric alongside raw token counts.

**FinOps Foundation for AI Guidance:** The FinOps Foundation's AI working group has established a "Crawl, Walk, Run" maturity model for AI cost management. Key metrics recommended for token-based cost tracking include cost-per-token (total cost / tokens processed), cost-per-inference (total inference cost / request count), and tokens-per-second throughput. As of 2026, advanced FinOps practices combine cost, power, and workload metrics to derive tokens-per-joule and carbon-per-prompt sustainability indicators. Attribution dimensions should span project/workload, environment (dev/staging/prod), team, cost center, and criticality level. The framework emphasizes that agentic loops (hitting an LLM 10--20 times per task), RAG context bloat (thousands of pages of context per query), and always-on monitoring agents create cost patterns fundamentally different from single-request inference -- all requiring granular token attribution to manage.

**State of FinOps 2026 (April--May 2026 release).** The FinOps Foundation's sixth annual report (n=1,192 practitioners representing $83B+ in annual cloud spend) is the clearest signal yet that AI telemetry has become a primary FinOps responsibility. **98% of respondents now actively manage AI costs**, up from 63% in 2025 and just 31% in 2024 -- a 3x adoption jump in two years that compressed what would normally be a multi-year governance maturation. The report's top tooling request across the entire survey was **granular monitoring of AI spend (tokens, LLM requests, GPU utilization)** -- commercial tooling has not yet delivered this at scale. Practitioners cited three persistent gaps in this order: (1) cost visibility under variable provider pricing models, (2) cost allocation when AI usage is embedded in product features and agent chains and resists traditional account-based mapping, and (3) ROI determination given the experimental nature of AI workloads. Notably, 78% of FinOps teams now report to CTOs/CIOs rather than CFOs, reflecting the shift from finance function to engineering infrastructure capability -- teams building 13.4.1 attribution should expect engineering ownership and instrument accordingly (event-level transaction records, ledger-grade economic data tied to business impact). The report's framing aligns with the four-layer infrastructure approach now standard in 2026 FinOps tooling: measure every transaction with full attribution, optimize through automated guardrails, connect activity to outcomes, and monetize through event-based billing.

**Prompt-cache hit rate as a first-class FinOps metric (2026).** Both Anthropic and OpenAI charge ~10% of the input price for cached tokens (~90% discount) but with different control models: OpenAI applies caching automatically with implicit reuse rules; Anthropic exposes explicit `cache_control` breakpoints and TTL choice. The practical implication for telemetry is that you cannot manage cache economics without separating cache *writes* from cache *reads* in your dashboards -- writes are paid at full input price, only reads are discounted. Production case studies in 2026 report moving cache hit rate from single-digit to ~84% by deliberately placing breakpoints and tuning TTLs (one team reported a $720 → $72/month drop, ~10x; another ~59% reduction). Wire `gen_ai.usage.cache_read.input_tokens` and `gen_ai.usage.cache_creation.input_tokens` (OTel semantic-conventions v1.37.0+) into the same dashboard as raw input/output token meters and compute hit rate as `cache_read / (cache_read + cache_creation + uncached_input)`. Treat cache hit rate per endpoint as a service-level objective: a sudden drop usually signals a prompt-template change that broke cache key alignment, not a usage spike.

**RAG context tax (2026 industry data).** A RAG-enhanced query in production typically consumes 3--5x more tokens than the same query without retrieval. Practitioner reviews suggest 70--80% of those retrieved tokens are unnecessary -- teams routinely pass 3--5 full documents into a prompt when a paragraph would do. Two telemetry-driven mitigations have emerged as default 2026 practice: tightening retrieval to return shorter, higher-precision chunks (typically cuts input tokens 40--60%), and semantic caching of repeated near-identical prompts (reported reductions up to 73% of API spend). Both require visibility into per-request retrieval-token counts, which is straightforward to expose via OTel span attributes on the retrieval step. Without per-stage token attribution -- retrieval, system prompt, user input, generation -- teams cannot localize which part of the pipeline is leaking tokens.

**Three-tag minimum for attribution.** Industry guidance converging in 2026 recommends every inference job carry three minimum tags propagated end-to-end: `model`, `use_case_id`, and `team_or_product`. These flow into cost reporting without bespoke ETL and let on-call engineers immediately distinguish "traffic up" from "efficiency down" when token spend spikes -- token counts emitted as metrics provide the denominator that turns a cost graph into an efficiency graph.

**Sustainability-grade telemetry.** Edge devices and local GPUs shipped in 2026 increasingly report `tokens-per-joule` and `carbon-per-prompt` directly through their SDKs, supplementing the cost-only view. For organizations with internal sustainability targets or those deploying in EU jurisdictions where AI energy disclosure is rapidly evolving, treat these as required telemetry alongside latency and cost rather than a separate sustainability program. The G-TRACE region-aware carbon accounting framework (arXiv:2511.04776) and Antarctica.io's "One-Token Model" propose auditable telemetry schemas and reference intensity profiles that enable cross-platform comparability.

### Output-to-Input Ratio Monitoring (13.4.2)

The output-to-input token ratio is a lightweight but effective anomaly indicator. Normal ratios vary significantly by use case:

| Use Case | Typical Output:Input Ratio |
|----------|---------------------------|
| Summarization | 0.1 - 0.3 |
| Chat / Q&A | 0.5 - 2.0 |
| Code generation | 2.0 - 10.0 |
| Translation | 0.8 - 1.2 |
| Data extraction | 0.1 - 0.5 |

Baselines must be established per endpoint. Extreme ratio anomalies (>10x the endpoint baseline) may indicate prompt injection forcing verbose output, data exfiltration via inflated responses, or model behavioral anomalies. Alert thresholds should be set relative to rolling baselines with endpoint-specific calibration.

### GPU and Infrastructure Monitoring (Supporting Context)

AI workloads have unique resource consumption patterns that differ from traditional application monitoring:

- **Inference is bursty:** GPU utilization spikes during inference requests and drops between them. Alert thresholds must account for this pattern to avoid false positives.
- **Model loading creates memory spikes:** Loading large models into GPU VRAM can temporarily consume all available memory. Distinguish model-load events from anomalous memory consumption.
- **Batch processing saturates GPUs:** Legitimate batch inference jobs will show sustained 100% GPU utilization that should not trigger alerts.

NVIDIA DCGM (Data Center GPU Manager) provides GPU-specific metrics exportable to Prometheus: utilization percentage, memory usage, temperature, power draw, and error counts. The `nvidia-smi` exporter for Prometheus is the most common collection mechanism for Kubernetes-based inference deployments.

Security-relevant GPU monitoring signals include: unexpected GPU utilization on idle inference servers (potential cryptomining), sustained memory pressure without corresponding inference requests (potential resource exhaustion attack), and abnormal error rates indicating hardware degradation or adversarial inputs designed to trigger computational edge cases.

As of 2025, NVIDIA has rolled out a GPU fleet management platform that aggregates telemetry from globally distributed deployments into the NGC cloud platform, surfacing hardware health, energy efficiency, and physical GPU location in real time. For organizations running GPU clusters, Trend Micro's integration with NVIDIA Morpheus provides GPU-accelerated anomaly detection at the infrastructure layer, achieving 20x throughput improvement for data loss prevention scanning on inference traffic.

### Agentic Telemetry Patterns

Agentic AI systems (multi-step tool-calling, planning loops, multi-agent orchestration) require telemetry beyond what single-inference monitoring provides. Key metrics to track:

- **Iteration count per agent invocation** -- Hard limits (e.g., max 15 steps) should trigger alerts well before the limit is reached. A sudden increase in average iteration count may indicate prompt injection causing reasoning loops.
- **Reasoning depth and confidence-vs-depth correlation** -- With reasoning models (GPT-5.4 series, DeepSeek-R1 successors) shipping configurable reasoning depth as a production parameter in 2026, depth becomes a telemetry signal in its own right. Practitioner heuristic from production playbooks: a reasoning depth above 8 strongly suggests a reasoning spiral, and *low confidence combined with high reasoning depth* almost certainly indicates a stuck agent. Capture both the reasoning step count and a per-step confidence (or self-evaluation) score, and alert on the joint distribution rather than either signal alone.
- **Context window growth rate** -- Monitor how quickly an agent's context window fills across steps. Rapid growth (especially in file-reading or web-browsing agents) may signal file system recursion attacks.
- **Cross-agent token consumption** -- In multi-agent architectures, track total token spend across the agent graph, not just per-agent. Circular dependencies between agents can only be detected by correlating consumption across the full workflow.
- **Tool call frequency and diversity** -- An agent repeatedly calling the same tool with slightly different parameters (semantic deduplication) is a hallucination loop indicator.
- **Execution timeouts** -- Complement token budgets with wall-clock timeouts. An agent may consume few tokens per step but take thousands of steps.

**Watchdog pattern:** Deploy a smaller, cheaper model to monitor the main agent's behavior in real time. The watchdog inspects the last N steps (typically 5) for cycle detection, semantic repetition, and budget trajectory. This adds modest cost but catches runaway agents before they exhaust budgets. Practical implementations include custom LangChain callbacks or LangGraph interrupt handlers that evaluate agent state against predefined safety predicates.

### Defense-in-Depth: Token Budgeting and Rate Limiting

Telemetry alone is not sufficient -- it must be coupled with enforcement mechanisms:

1. **Per-request token budgets** -- Assign a maximum token budget to each inference request or agent invocation. Terminate immediately when the budget is exceeded. This is the most effective mitigation against denial-of-wallet attacks.
2. **Per-user and per-session rate limits** -- Track cumulative token consumption per authenticated identity over sliding windows (1 minute, 1 hour, 1 day). Alert at 80% of limit; hard-block at 100%.
3. **Prompt complexity analysis** -- Reject or flag prompts that exhibit patterns associated with sponge attacks: excessive repetition, deeply nested structures, or instructions designed to maximize attention computation.
4. **Semantic caching** -- Cache responses for semantically similar prompts (using embedding similarity) to serve repeated heavy prompts without incurring additional inference costs. This doubles as a DoW mitigation and a latency optimization.
5. **Cost alerting with automated circuit breakers** -- When total inference spend exceeds a configurable threshold within a time window, automatically degrade service (e.g., switch to a smaller model, reduce max output tokens) rather than allowing unbounded spend.

#### Circuit Breaker Trigger Conditions (2026 Practitioner Patterns)

Production AI agent deployments in 2026 have converged on four standard circuit-breaker trigger categories, and these align directly with the telemetry signals required by 13.4.1 and 13.4.2:

| Trigger | Telemetry Signal | Suggested Default |
|---------|------------------|-------------------|
| Runaway loops | Same tool + same/near-identical arguments in N consecutive calls | Trip at 5 repeats |
| Cost velocity | Spend rate per session or per hour exceeds budget envelope | $50/hour or $200/session typical bands |
| Consecutive failures | Same operation fails N times without recovery | Trip at 3 failures |
| Scope violations | Action outside permission boundary or RBAC scope | Trip on first violation, escalate to human |

The kill-switch versus circuit-breaker distinction matters: a kill switch requires a human to observe and act (covered in C14.1), while a circuit breaker is automated infrastructure that detects anomalies and self-terminates the run. Telemetry must feed *both*. Notably, observability platforms like LangSmith and Helicone are passive recorders -- they do not enforce intervention. Enforcement requires either application-layer guards (LangChain callbacks, LangGraph interrupt handlers) or a dedicated cost-control proxy.

An April 2026 incident-pattern review from Cycles makes the same point from a runtime-control angle: dashboards and logs usually observe the damage after the agent has acted, while budget gates, action gates, scope isolation, and audit trails decide whether the next tool call should run before it consumes tokens or mutates state. Use 13.4.1 telemetry to feed those pre-execution budget gates and 13.4.2 telemetry to feed anomaly gates; treating both controls as passive dashboards leaves the highest-cost failure modes untouched.

**Cost-control proxies and gateways (April 2026 wave).** Several products specifically target agentic spend control as a managed layer in front of LLM APIs:

- **Portal26 Agentic Token Controls** (launched April 23, 2026) -- Lets administrators set token budgets at agent, workflow, or organization scope; throttles agents approaching the cap and pauses or terminates those that exceed it. Targets the "adoption speed vs cost predictability" tradeoff that customers like Uber surfaced as a top-of-mind concern at the Gartner Data & Analytics Summit.
- **Kong AI Gateway 3.14 / Kong Agent Gateway** (April 14, 2026) -- Extends Kong's AI Gateway to govern LLM, MCP, and agent-to-agent (A2A) traffic from a unified control plane. Ships with token-based rate limiting, semantic caching, semantic routing (best-fit model selection), and cost analytics across the full agentic stack. Treats every internal A2A call as a first-class telemetry event, which is important because a single agentic workflow can chain 20+ internal API calls (RAG lookup, vector DB search, prompting, re-prompting) and gateway-layer attribution is the only practical way to see them all in one timeline. The "AI Rate Limiting Advanced" plugin is the consumption-control surface most teams configure first; the 3.14.0.0 changelog adds policy-based rate limiting with multi-dimensional match conditions and prompt-token estimation for `prompt_tokens`, `total_tokens`, and `cost` strategies, so auditors can test whether obviously over-budget requests are rejected before the upstream model call happens.
- **RelayPlane** -- Open-source cost intelligence proxy with smart model routing across 11 providers. Includes runtime anomaly detection for runaway loops, cost spikes, and token explosions.
- **TokenFence** -- Lightweight cost circuit breaker for AI agents that enforces per-task and per-session token caps with auto-termination on threshold breach. Useful as a Redis-backed sidecar where teams want to bolt cost protection onto an existing application without adopting a full gateway.
- **Self-built proxy patterns** -- Many enterprises layer a thin proxy on top of OpenAI/Anthropic SDKs that emits OTel spans, enforces per-user quota in Redis, and short-circuits requests once a session-level token budget is exhausted. Pair this with a "financial velocity" guardrail (e.g., "if any agent identity spends > $50 in 10 minutes, cut access") rather than relying on monthly budget caps alone -- velocity-based limits catch loops within minutes; monthly caps don't notice until significant damage is done.
- **Vantage FinOps Agent** (general availability November 20, 2025; pricing model published in early 2026) -- Slack-native interactive agent that reads cloud telemetry via Vantage APIs, recommends remediations, and (with explicit per-action approval logged to a Vantage Audit Log) executes optimizations against AWS Financial Commitments (Savings Plans, Reserved Instances for RDS / OpenSearch / ElastiCache / Redshift). Notably, the Agent itself is metered in tokens ($2.50 per million tokens monthly post-July 2026), which makes it a useful reference example of "the FinOps agent is itself an inference workload that must be attributed" -- exactly the recursion problem 13.4.1 is meant to surface.
- **Revenium** -- Event-level token/request/GPU telemetry with attribution hooks for customer, feature, workflow, and agent identity. Targets the gap surfaced in the 2026 State of FinOps report (granular AI spend monitoring as the #1 unmet tooling need); useful where teams need ledger-grade per-event records rather than aggregated dashboards.

### Regulatory and Standards Landscape

#### NIST AI 800-4: Post-Deployment Monitoring (March 2026)

NIST released AI 800-4, "Challenges to the Monitoring of Deployed AI Systems," in March 2026, synthesizing findings from practitioner workshops conducted by the Center for AI Standards and Innovation. The report defines six monitoring categories directly relevant to performance telemetry:

1. **Functionality monitoring** -- Ensures the system performs as intended (maps to 13.4.1, 13.4.2)
2. **Operational monitoring** -- Maintains consistent infrastructure service levels and provides context for token and ratio anomalies
3. **Security monitoring** -- Protects against adversarial attacks and misuse through cost, usage, and behavior anomaly data
4. **Human factors monitoring** -- Ensures transparency and output quality
5. **Compliance monitoring** -- Adherence to regulations and standards
6. **Large-scale impacts monitoring** -- Broader societal effects

Key challenges identified include detecting performance drift with fragmented logging infrastructure, scaling human monitoring alongside rapid AI rollouts, and the lack of trusted guidelines for monitoring cadence and risk-based prioritization. The report highlights that many organizations still have no defined relationship between continuous monitoring and periodic auditing.

#### EU AI Act: Telemetry Requirements for High-Risk Systems

The EU AI Act establishes specific telemetry obligations for high-risk AI systems. Article 12 mandates automatic logging capabilities that record events throughout the system lifecycle, including events relevant to identifying risk situations and facilitating post-market monitoring. Article 19 requires that automatically generated logs be retained and accessible for regulatory inspection. Article 72, applicable from August 2, 2026, requires providers to establish a documented post-market monitoring system that actively collects, documents, and analyzes performance and compliance data throughout the system's lifetime. The official EUR-Lex text also ties the post-market monitoring plan to Annex IV technical documentation and required the Commission to adopt a plan template by February 2, 2026, so audits should look for a plan that names the telemetry sources, retention periods, anomaly thresholds, and review cadence rather than a generic monitoring policy.

For organizations deploying high-risk AI systems in the EU, granular token attribution (13.4.1) and behavior anomaly detection (13.4.2) directly support these compliance obligations by supplying post-market evidence about usage, cost, and abnormal model behavior. Logging infrastructure should be designed with regulatory access in mind from the start, not bolted on after deployment.

#### NIST AI 600-1: GenAI Risk Profile

NIST AI 600-1 (the Generative AI Profile, released July 2024) provides the risk management framework context for these telemetry requirements. Its four-function cycle -- Map, Measure, Manage, Govern -- positions performance telemetry as the primary implementation of the "Measure" function, providing the quantitative data that enables risk assessment and the "Manage" function for risk-based response actions.

---

## Related Standards & References

- **OpenTelemetry GenAI Semantic Conventions** -- Standard attributes for AI telemetry; current core spec pages report semantic conventions v1.41.0 while the dedicated GenAI schema repository advertises schema URL 1.42.0 and the GenAI subset remains in Development status ([opentelemetry.io/docs/specs/semconv/gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/), [github.com/open-telemetry/semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai))
- **OpenTelemetry GenAI Metrics** -- `gen_ai.client.token.usage`, operation-duration, and server latency/token histograms with billable-token guidance ([opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/))
- **OTel GenAI Agent Span Conventions** -- Emerging semantic conventions for agentic system observability ([opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/))
- **OpenLLMetry** -- Auto-instrumentation for LLM frameworks emitting OTel GenAI conventions ([traceloop.com](https://www.traceloop.com/blog/visualizing-llm-performance-with-opentelemetry-tools-for-tracing-cost-and-latency))
- **OpenTelemetry Agent Observability** -- Evolving standards for AI agent telemetry ([opentelemetry.io/blog/2025/ai-agent-observability](https://opentelemetry.io/blog/2025/ai-agent-observability/))
- **OneUptime Token/Cost/Latency Tracking** -- Practical guide to OTel-based LLM metrics ([oneuptime.com](https://oneuptime.com/blog/post/2026-02-06-track-token-usage-prompt-costs-model-latency-opentelemetry/view))
- **Grafana LLM Observability Guide** -- Complete OTel + Grafana stack for LLM monitoring ([grafana.com](https://grafana.com/blog/a-complete-guide-to-llm-observability-with-opentelemetry-and-grafana-cloud/))
- **Prometheus + Grafana** -- Open-source metrics collection and visualization widely used for AI infrastructure monitoring
- **NVIDIA DCGM** -- Data Center GPU Manager for GPU-specific monitoring metrics ([github.com/NVIDIA/DCGM](https://github.com/NVIDIA/DCGM))
- **NVIDIA GPU Fleet Management** -- Centralized telemetry platform for globally distributed GPU deployments via NGC
- **Trend Micro + NVIDIA Morpheus** -- GPU-accelerated anomaly detection for AI infrastructure security ([trendmicro.com](https://www.trendmicro.com/en_us/research/25/e/trend-secures-ai-infrastructure-with-nvidia.html))
- **OWASP Top 10 for LLM 2025: LLM10 Unbounded Consumption** -- Directly addressed by token tracking and resource monitoring controls
- **MITRE ATLAS: AML.T0029 (Denial of ML Service)** -- Attack technique for overloading inference endpoints ([atlas.mitre.org](https://atlas.mitre.org/))
- **MITRE ATLAS: AML.T0034 (Cost Harvesting)** -- Attack technique for exhausting operational budgets via API abuse
- **MITRE ATLAS Data v5.6.0** -- Generated ATLAS data with Cost Harvesting subtechniques AML.T0034.000/.001/.002 ([github.com/mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data), [raw ATLAS.yaml](https://raw.githubusercontent.com/mitre-atlas/atlas-data/refs/heads/main/dist/ATLAS.yaml))
- **MITRE ATLAS: AML.T0048 (External Harms)** -- Financial harm through manipulated AI resource consumption
- **Prompt Security: Denial of Wallet on GenAI Apps** -- Practical DoW attack analysis ([prompt.security](https://prompt.security/blog/denial-of-wallet-on-genai-apps-ddow))
- **Lasso Security: DoS & Denial of Wallet Threats** -- Attack taxonomy and mitigation strategies ([lasso.security](https://www.lasso.security/blog/denial-of-service-dos-and-denial-of-wallet-dow-attacks))
- **Sponge Attack Research (IEEE EuroS&P)** -- Adversarial inputs exploiting Transformer attention complexity for 30x+ latency increases
- **FinOps Foundation** -- Cost management frameworks applicable to AI inference cost attribution
- **Datadog LLM Observability** -- Native OTel GenAI convention support ([datadoghq.com](https://www.datadoghq.com/blog/llm-otel-semantic-convention/))
- **Langfuse** -- Open-source LLM observability with token and cost tracking, custom usage fields, and metrics APIs ([langfuse.com](https://langfuse.com/docs/observability/features/token-and-cost-tracking))
- **NIST AI 800-4: Challenges to the Monitoring of Deployed AI Systems** -- Six-category post-deployment monitoring framework (March 2026) ([nist.gov](https://www.nist.gov/news-events/news/2026/03/new-report-challenges-monitoring-deployed-ai-systems))
- **NIST AI 600-1: Generative AI Risk Management Profile** -- Map/Measure/Manage/Govern cycle for GenAI risk ([nvlpubs.nist.gov](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf))
- **EU AI Act Articles 12, 19, 72** -- Automatic logging, record-keeping, and post-market monitoring for high-risk AI systems ([EUR-Lex Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en), [artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/72/))
- **AI Inference Incident Taxonomy** -- Empirical study of 156 high-severity incidents establishing four-way failure classification ([arxiv.org](https://arxiv.org/html/2511.07424))
- **Microsoft Agentic AI Failure Mode Taxonomy** -- Security and safety failure modes in agentic systems ([microsoft.com](https://www.microsoft.com/en-us/security/blog/2025/04/24/new-whitepaper-outlines-the-taxonomy-of-failure-modes-in-ai-agents/))
- **Partnership on AI: Real-Time Failure Detection in AI Agents** -- Multi-layered monitoring for agent failure detection ([partnershiponai.org](https://partnershiponai.org/wp-content/uploads/2025/09/agents-real-time-failure-detection.pdf))
- **FinOps Foundation: FinOps for AI** -- Cost-per-token attribution framework and maturity model ([finops.org](https://www.finops.org/wg/finops-for-ai-overview/))
- **LLM Agent Security Survey (May 2026)** -- Taxonomy of prompt, leakage, action-induction, and resource-exhaustion attacks against LLM-based agents ([springer.com](https://link.springer.com/article/10.1007/s11416-026-00622-3))
- **State of AI Agent Incidents 2026** -- Runtime-control mapping for runaway spend, wrong actions, scope failures, and audit gaps in production agent incidents ([runcycles.io](https://runcycles.io/blog/state-of-ai-agent-incidents-2026))
- **Alibaba ROME Agent Incident** -- Autonomous coding agent hijacked GPUs for crypto mining, detected via network traffic anomalies (late 2025) ([3dvf.com](https://3dvf.com/en/alibaba-falls-victim-to-ai-agent-secretly-exploiting-servers-for-crypto-mining/))
- **RSA 2026: GPU Security Blind Spots** -- EDR gaps for GPU monitoring in AI infrastructure ([futurumgroup.com](https://futurumgroup.com/insights/exposes-security-gaps/))
- **EchoLeak (CVE-2025-32711)** -- Zero-click prompt injection in M365 Copilot with data exfiltration, CVSS 9.3 ([hackthebox.com](https://www.hackthebox.com/blog/cve-2025-32711-echoleak-copilot-vulnerability))
- **GPU Architectural Security Analysis** -- GPU privilege separation, memory isolation, and driver attack surface ([edera.dev](https://edera.dev/stories/why-gpus-are-the-weak-link-in-ai-security))
- **NVIDIA BlueField-4 + DOCA Argus (CES January 2026)** -- DPU-accelerated runtime security for AI factories; nine validated security partners at launch ([nvidia.com](https://blogs.nvidia.com/blog/bluefield-cybersecurity-acceleration-enterprise-ai-factory-validated-design/))
- **Check Point AI Factory Security Architecture Blueprint** (March 23, 2026) -- Reference design integrating Check Point, BlueField DPUs, and AI Agent Security for zero-trust AI infrastructure ([stocktitan.net](https://www.stocktitan.net/news/CHKP/check-point-releases-ai-factory-security-blueprint-to-safeguard-ai-72wh8gvc8uc7.html))
- **Agentic Resource Exhaustion: Gartner Summit Coverage (March 2026)** -- $400M Fortune 500 "Predictability Gap" from agentic cost blowouts ([analyticsweek.com](https://analyticsweek.com/finops-for-agentic-ai-cloud-cost-2026/))
- **AI Inference Cost Crisis 2026** -- Per-workload token multipliers (1x chatbot to 20x agentic), inference = 85% of enterprise AI budgets ([oplexa.com](https://oplexa.com/ai-inference-cost-crisis-2026/))
- **CIO: AI Token Freeloaders** -- Amazon Rufus off-purpose token abuse case study; mitigation recommendations for intent-scoped chatbots ([cio.com](https://www.cio.com/article/4155404/ai-token-freeloaders-are-coming-for-your-customer-support-chatbot.html))
- **Inference Security for Production AI Systems** -- Telemetry-first framing for inference API defense (GMI Cloud, 2026) ([gmicloud.ai](https://www.gmicloud.ai/en/blog/inference-security-how-to-protect-apis-in-production-ai-systems))
- **MCP Router Wallet Drain Research** -- April 2026 CoinDesk coverage of malicious MCP tool-call injection draining crypto wallets ([coindesk.com](https://www.coindesk.com/tech/2026/04/13/ai-agents-are-set-to-power-crypto-payments-but-a-hidden-flaw-could-expose-wallets))
- **Denial of Wallet Attacks in Serverless Architectures (arXiv 2508.19284)** -- Comprehensive review with ML-based detection approaches ([arxiv.org](https://arxiv.org/abs/2508.19284))
- **OpenTelemetry semantic-conventions v1.39.0** (January 12, 2026) -- Adds `gen_ai.evaluation.result` event for standardized evaluation telemetry ([github.com](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.39.0))
- **Portal26 Agentic Token Controls** (April 23, 2026) -- Token budget enforcement at agent, workflow, and organization scope ([siliconangle.com](https://siliconangle.com/2026/04/23/portal26-launches-agentic-token-controls-cap-runaway-ai-agent-spend/))
- **AI Agent Circuit Breakers: The Reliability Pattern Production Teams Are Missing** -- Practitioner write-up of the $437 retry-loop incident and four-category circuit-breaker taxonomy ([dev.to](https://dev.to/waxell/ai-agent-circuit-breakers-the-reliability-pattern-production-teams-are-missing-5bpg))
- **Inference Economics: 2026 Enterprise AI Cost Crisis** -- Inference now ~85% of enterprise AI budget; agentic loops, RAG bloat, always-on monitoring as primary drivers ([analyticsweek.com](https://analyticsweek.com/inference-economics-finops-ai-roi-2026/))
- **G-TRACE: Region-Aware Carbon Accounting for GenAI** (arXiv 2511.04776) -- AI Sustainability Pyramid and per-region carbon attribution model ([arxiv.org](https://arxiv.org/html/2511.04776))
- **John Snow Labs: Tokens per Joule** -- Quantifying the energy footprint of clinical LLM inference ([johnsnowlabs.com](https://www.johnsnowlabs.com/tokens-per-joule-how-to-quantify-and-reduce-the-energy-footprint-of-clinical-llm-inference/))
- **Antarctica.io: The One-Token Model** -- AI cost, energy, and emissions measurement framework for sustainable IT ([antarctica.io](https://antarctica.io/research/one-token-model))
- **AgentOps 101: Observability, Kill-Switches, and Circuit Breakers** -- Distinction between manual kill-switches and automated circuit breakers, and how telemetry feeds both ([agileleadershipdayindia.org](https://agileleadershipdayindia.org/blogs/agentops-machine-identity-security-guide/agentops-observability-kill-switches-circuit-breakers.html))
- **Tokenizer Drift Hidden Costs (Trend Micro, 2026)** -- How tokenizer changes between provider model updates silently inflate token bills and create attribution drift ([trendmicro.com](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/when-tokenizers-drift-hidden-costs-and-security-risks-in-llm-deployments))
- **LiteLLM Supply Chain Compromise (March 24, 2026)** -- LiteLLM 1.82.7/1.82.8 PyPI packages distributed a credential-stealer for ~40 minutes; produced detectable telemetry signatures (fork-rate anomalies, SSH/`.env` reads) on inference proxies ([trendmicro.com](https://www.trendmicro.com/en_us/research/26/c/inside-litellm-supply-chain-compromise.html), [datadog](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/), [LiteLLM advisory](https://docs.litellm.ai/blog/security-update-march-2026))
- **Vercel / Context.ai Breach (April 19, 2026)** -- OAuth supply chain attack via Lumma Stealer at Context.ai exposed Vercel customer environment variables and source code ([vercel](https://vercel.com/kb/bulletin/vercel-april-2026-security-incident), [techcrunch](https://techcrunch.com/2026/04/20/app-host-vercel-confirms-security-incident-says-customer-data-was-stolen-via-breach-at-context-ai/))
- **Kong Agent Gateway / AI Gateway 3.14** (April 14, 2026) -- Unified gateway control plane for LLM, MCP, and agent-to-agent traffic with token rate limiting, semantic caching, and cost analytics ([Kong product release](https://konghq.com/blog/product-releases/kong-ai-gateway-3-14), [A2A traffic docs](https://developer.konghq.com/ai-gateway/a2a/), [AI Rate Limiting Advanced changelog](https://developer.konghq.com/plugins/ai-rate-limiting-advanced/changelog/))
- **TokenFence -- Cost Circuit Breaker for AI Agents** -- Lightweight per-task and per-session token-cap enforcement with auto-termination ([tokenfence.dev](https://tokenfence.dev/))
- **Reasoning Depth as a Production Telemetry Signal** -- Confidence-vs-depth correlation for detecting reasoning spirals in production agents ([dev.to](https://dev.to/nebulagg/ai-agent-observability-the-4-pillars-that-keep-your-agents-from-burning-2000-at-3-am-24cn))
- **Prompt Caching Cost Telemetry (Anthropic / OpenAI 2026)** -- Hit rate as a FinOps SLO; ~84% achievable with deliberate breakpoint placement; separate cache writes from reads in dashboards ([digitalocean](https://www.digitalocean.com/blog/prompt-caching-with-digital-ocean), [aicheckerhub](https://aicheckerhub.com/anthropic-prompt-caching-2026-cost-latency-guide), [projectdiscovery](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching))
- **Cost Circuit Breaker Patterns (Cordum, 2026)** -- Financial velocity limits ($X/10min) vs monthly caps; failure-rate and tool-repetition triggers ([cordum.io](https://cordum.io/blog/ai-agent-circuit-breaker-pattern), [cloudatler](https://cloudatler.com/blog/the-50-000-loop-how-to-stop-runaway-ai-agent-costs))
- **OpenTelemetry semantic-conventions v1.41.0** (2026) -- Current release of the conventions spec; `gen_ai.*` attribute set continues to evolve in Development status ([opentelemetry.io](https://opentelemetry.io/docs/specs/semconv/), [github](https://github.com/open-telemetry/semantic-conventions/releases))
- **State of FinOps 2026** -- FinOps Foundation's sixth annual report (1,192 practitioners, $83B+ cloud spend); 98% manage AI costs (vs 31% in 2024), granular AI spend monitoring is the #1 tooling gap, 78% of FinOps teams now report to CTO/CIO ([data.finops.org](https://data.finops.org/), [virtasant](https://www.virtasant.com/blog/state-of-finops-2026), [revenium](https://www.revenium.ai/post/the-2026-state-of-finops-report))
- **Mercor LiteLLM Victim Disclosure (April 2026)** -- First publicly confirmed downstream victim of the LiteLLM/TeamPCP/Trivy supply chain compromise; ~4 TB exfiltrated including 939 GB source code, claimed by Lapsus$; Mandiant projects 1,000-10,000 affected SaaS environments ([theregister](https://www.theregister.com/2026/04/02/mercor_supply_chain_attack/))
- **OverThink: Slowdown Attacks on Reasoning LLMs** -- Decoy reasoning problems in retrieved content produced up to 18x and 46x slowdown in reported experiments ([huggingface.co](https://huggingface.co/papers/2502.02542))
- **Excessive Reasoning Attack on Reasoning LLMs** -- Adversarial inputs increased reasoning length 3x to 6.5x with transfer to o3-mini, GPT-OSS, DeepSeek-R1, and QWQ ([openreview.net](https://openreview.net/forum?id=g0uBExrnjz))
- **ReasoningBomb: Prompt-Induced DoS Against Large Reasoning Models** -- ACM CCS 2026 paper reporting short-prompt reasoning amplification and production-throughput impact ([reasoningbomb.github.io](https://reasoningbomb.github.io/))
- **Sponge Attacks on Sensing AI (arXiv 2505.06454)** -- Energy-latency sponge attacks against sensing-based AI, with model pruning explored as a defense ([arxiv.org](https://arxiv.org/abs/2505.06454))
- **Vantage FinOps Agent** (November 20, 2025) -- Slack-native interactive agent for AWS Financial Commitments optimization with token-metered pricing and audit-logged action approval ([vantage.sh](https://www.vantage.sh/blog/finops-ai-agent))
- **Revenium AI FinOps Telemetry** -- Event-level token/request/GPU records with customer/feature/workflow/agent attribution hooks ([revenium.ai](https://www.revenium.ai/post/the-2026-state-of-finops-report))

---

## Open Research Questions

- What are effective baseline models for "normal" token consumption patterns across different AI application types, and how should baselines adapt to seasonal or usage-driven shifts?
- How should GPU monitoring differ between training and inference workloads for security purposes?
- Can output-to-input ratio monitoring be generalized across modalities (text, image, audio), or does each need its own baseline?
- What is the right approach for correlating token cost anomalies across multiple providers in multi-model architectures?
- How effective are watchdog models at detecting novel runaway agent patterns they were not explicitly trained to recognize?
- What is the optimal trade-off between semantic caching coverage and cache poisoning risk -- can an attacker craft prompts to pollute the cache and serve incorrect responses to legitimate users?
- As reasoning models (chain-of-thought, tree-of-thought) become standard, how should telemetry distinguish between legitimate extended reasoning and adversarial reasoning-exhaustion attacks?
- What telemetry standards will emerge for monitoring MCP (Model Context Protocol) tool server interactions, where token consumption spans multiple trust boundaries?
- Given NIST AI 800-4's finding that organizations lack defined relationships between continuous monitoring and periodic auditing, what is the optimal cadence for converting telemetry data into audit-ready evidence for EU AI Act compliance?
- With GPU-level behavioral monitoring largely absent from current EDR stacks (as highlighted at RSA 2026), what GPU-specific telemetry signals beyond utilization metrics are needed to detect adversarial workloads like the ROME cryptomining incident?
- The 41--87% failure rate observed in multi-agent systems (MAST taxonomy) suggests current monitoring is insufficient -- what minimum set of cross-agent telemetry signals reliably detects cascading failures before they propagate?
- With DPU-level inference telemetry (e.g., BlueField-4 + DOCA Argus) becoming available in 2026, what portion of host-level GenAI instrumentation can be safely delegated to the DPU, and which signals still require in-process collection (e.g., tokenizer-level attribution, prompt semantics)?
- For intent-scoped endpoints like customer-support chatbots, can session-level intent classifiers reliably distinguish off-purpose token abuse (Rufus-style) from legitimate edge-case queries without introducing high false-positive rates that degrade user trust?
- What early-warning signals -- beyond cumulative spend -- reliably predict the onset of an Agentic Resource Exhaustion loop within the first 1--2 iterations, before meaningful budget has been consumed?
- How should attribution dashboards handle tokenizer drift across provider model upgrades, where the same logical input produces different token counts and silently breaks year-over-year cost comparisons?
- For circuit-breaker thresholds (consecutive identical tool calls, cost velocity, consecutive failures), what defaults survive across application archetypes -- chat, RAG, autonomous agent -- without producing constant false trips for one and missing real abuse in another?
- After the LiteLLM (March 2026) and Vercel/Context.ai (April 2026) supply chain compromises, what telemetry signatures from inference proxies and AI gateways are most reliable for distinguishing post-compromise behavior (credential bulk-read, OAuth misuse, fork-rate anomalies) from legitimate workload changes?
- As reasoning models expose configurable reasoning depth as a production parameter, what joint distribution of (depth, per-step confidence, tokens-per-step) most reliably distinguishes legitimate complex reasoning from a stuck or adversarially induced reasoning spiral?
- Anthropic and OpenAI use fundamentally different prompt-cache control models (explicit breakpoints + TTL vs implicit reuse). Can a provider-agnostic OTel attribute set capture both without forcing teams to choose one vendor's mental model -- and what does a fair cross-provider hit-rate dashboard look like?
- The State of FinOps 2026 report shows 98% of teams now manage AI costs but flags granular AI spend monitoring as the #1 tooling gap. What minimum schema (event-level vs aggregated, attribution dimensions, latency-to-dashboard) closes the gap quickly enough to keep up with quarterly model upgrades and new provider pricing tiers?
- After the Mercor disclosure broadened the LiteLLM blast radius from "thousands" to a projected 10,000+ SaaS environments, what telemetry-first detection patterns survive when the inference proxy itself is the compromised layer -- specifically, which signals can a downstream tenant collect that don't depend on the proxy reporting honestly about itself?
- For FinOps agents that themselves consume tokens (e.g., the Vantage FinOps Agent metered at $2.50/M tokens), what is the right way to attribute the agent's own inference cost back to the workloads it optimizes -- and how should that bidirectional attribution show up in 13.4.1 dashboards without double-counting?

---

## Related Pages

- [C9.1 Execution Budgets](../C09-Orchestration-and-Agents/C09-01-Execution-Budgets.md) -- Shows how token, cost, retry, and duration telemetry becomes enforceable runtime budgets and circuit breakers.
- [C13.1 Request & Response Logging](C13-01-Request-Response-Logging.md) -- Defines the structured logging and OTel schema foundation that feeds the token attribution and anomaly metrics here.
