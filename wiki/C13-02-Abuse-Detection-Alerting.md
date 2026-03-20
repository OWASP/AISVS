# C13.2: Abuse Detection and Alerting

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 10 (13.2.1 -- 13.2.10)

## Purpose

This section addresses the detection of adversarial activity, abuse patterns, and attack campaigns targeting AI systems. Unlike traditional application security monitoring, AI abuse detection must account for natural language attack vectors (prompt injection, jailbreaks), multi-turn attack strategies, and AI-specific exfiltration techniques. These controls bridge the gap between raw logging (C13.1) and incident response (C13.5).

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **13.2.1** | Verify that the system detects and alerts on known jailbreak patterns, prompt injection attempts, and adversarial inputs using signature-based detection. | 1 | D/V | Known jailbreak techniques (DAN, role-play exploits, instruction override) and documented prompt injection patterns bypassing safety controls. | Deploy known jailbreak payloads from public datasets (e.g., JailbreakBench, PromptInject) and confirm detection. Review signature database update frequency. Test both direct and indirect injection patterns. | Signature-based detection is a necessary baseline but insufficient alone -- novel jailbreaks evade signatures. Must be paired with behavioral detection (13.2.4, 13.2.8). Signature databases require continuous updates as new techniques emerge. |
| **13.2.2** | Verify that the system integrates with existing Security Information and Event Management (SIEM) platforms using standard log formats and protocols. | 1 | D/V | AI security events remaining siloed from enterprise security operations; delayed detection due to AI events not reaching SOC analysts; inability to correlate AI attacks with broader infrastructure compromise. | Confirm log forwarding to SIEM via standard protocols (syslog, CEF, LEEF, or OTLP). Verify events appear in SIEM dashboards. Test correlation rules between AI events and traditional security events. | Most SIEMs lack native AI event parsers. Custom parsing rules and field mappings are typically required. OpenTelemetry-to-SIEM pipelines (via Fluentd/Vector) are the most maintainable approach. |
| **13.2.3** | Verify that enriched security events include AI-specific context such as model identifiers, confidence scores, and safety filter decisions. | 2 | D/V | SOC analysts lacking context to triage AI security events; inability to determine which model or safety filter was involved in an incident; missed correlations between model-specific attack patterns. | Review security event payloads in SIEM for AI-specific fields. Confirm model identifier, confidence score, and safety filter outcome are present and queryable. Test alerting rules that filter on these fields. | Event enrichment should happen at the collection layer (agent/exporter), not in the SIEM, to avoid parsing overhead. Define a standard AI security event taxonomy to ensure consistency. |
| **13.2.4** | Verify that behavioral anomaly detection identifies unusual conversation patterns, excessive retry attempts, or systematic probing behaviors. | 2 | D/V | Attackers probing model boundaries through repeated variations; automated attack tools generating high-volume prompt variations; reconnaissance activity preceding targeted attacks. | Simulate probing patterns (rapid retries, systematic variation of inputs, boundary-testing sequences). Verify anomaly detection triggers. Review false positive rates against legitimate usage patterns. | Requires baseline establishment of normal conversation patterns. Statistical methods (z-score on session length, token usage, retry rates) provide a starting point. ML-based anomaly detection improves accuracy but adds complexity. |
| **13.2.5** | Verify that real-time alerting mechanisms notify security teams when potential policy violations or attack attempts are detected. | 2 | D/V | Delayed response to active attacks allowing attackers to achieve objectives; policy violations going unnoticed until post-hoc review. | Trigger known attack patterns and measure time-to-alert. Verify alert routing to appropriate channels (PagerDuty, Slack, email). Test alert prioritization and deduplication. Confirm on-call rotation coverage. | Alert fatigue is the primary operational risk. Implement severity tiers: P1 for active exploitation, P2 for policy violations, P3 for anomalous patterns. Tune thresholds to minimize false positives while maintaining detection coverage. |
| **13.2.6** | Verify that custom rules are included to detect AI-specific threat patterns including coordinated jailbreak attempts, prompt injection campaigns, and model extraction attacks. | 2 | D/V | Coordinated attacks from multiple accounts/IPs; slow-and-low model extraction via systematic querying; prompt injection campaigns targeting specific model behaviors. | Review SIEM rule library for AI-specific detection rules. Test rules against simulated coordinated attacks (multi-source jailbreak attempts, systematic extraction queries). Verify cross-session correlation capabilities. | Model extraction detection should monitor for: high query volumes with systematic input variations, requests that map decision boundaries, and unusual output collection patterns. Coordinate with C11 (Adversarial Robustness) controls. |
| **13.2.7** | Verify that automated incident response workflows can isolate compromised models, block malicious users, and escalate critical security events. | 3 | D/V | Continued exploitation after detection due to slow manual response; attacker persistence across model compromise; cascading damage from compromised models in multi-agent systems. | Test automated playbooks: trigger a critical event and verify model isolation occurs within defined SLA. Test user blocking across all AI endpoints. Verify escalation reaches incident commander. Test rollback procedures. | SOAR (Security Orchestration, Automation, and Response) integration is ideal but complex. Minimum viable automation: API-driven model endpoint disable, user/IP blocklist update, and Slack/PagerDuty escalation. Full automation requires high confidence in detection to avoid availability impact. |
| **13.2.8** | Verify that session-level conversation trajectory analysis detects multi-turn jailbreak patterns where no individual turn is overtly malicious in isolation but the aggregate conversation exhibits attack indicators. | 3 | D/V | Multi-turn jailbreaks that incrementally shift model behavior (crescendo attacks, context manipulation, progressive persona shifting); attacks designed to evade per-message classifiers. | Execute documented multi-turn attack sequences (crescendo attack, progressive jailbreak). Verify session-level analysis flags the trajectory even when individual turns pass per-message checks. Measure detection latency (which turn triggers the alert). | This is a research-frontier requirement. Current approaches: sliding window analysis over conversation embeddings, cumulative risk scoring across turns, and LLM-as-judge on conversation summaries. Few production-ready tools exist. |
| **13.2.9** | Verify that per-user and per-session token consumption is tracked, with anomaly detection alerting when consumption exceeds defined thresholds. | 2 | D/V | Denial-of-wallet attacks via excessive token consumption; compromised accounts used for unauthorized inference at scale; cost runaway from automated abuse. | Review token tracking granularity (per-user, per-session, per-endpoint). Test threshold alerting by exceeding limits. Verify rate limiting integration. Check for anomaly detection beyond static thresholds (e.g., deviation from user's historical pattern). | Token consumption anomalies can indicate: (1) denial-of-wallet attacks, (2) model extraction attempts (high volume), (3) compromised API keys, or (4) prompt injection causing verbose outputs. Integrate with billing systems for cost attribution. |
| **13.2.10** | Verify that LLM API traffic is monitored for covert channel indicators, including Base64-encoded payloads, structured non-human query patterns, and communication signatures consistent with malware command-and-control activity using LLM endpoints. | 3 | D/V | Malware using LLM APIs as C2 channels (documented in the wild); data exfiltration through model interactions; steganographic communication via AI-generated content. | Inject Base64-encoded payloads, structured non-natural-language queries, and periodic beacon-like patterns. Verify detection triggers. Test entropy analysis on input/output streams. Review for known C2-over-LLM indicators. | Threat is real: security researchers have demonstrated C2 frameworks using ChatGPT and Claude APIs as communication channels. Detection approaches: entropy analysis on inputs, periodicity detection in session patterns, and structural analysis distinguishing human vs. automated query patterns. |

---

## Implementation Guidance

### AI Firewall and Guardrail Products (2025-2026)

A new category of "AI Firewalls" has emerged to address requirements 13.2.1 and 13.2.4-13.2.6 at the infrastructure layer:

- **Azure AI Content Safety -- Prompt Shields** -- Microsoft's unified API that analyzes prompts and documents before content generation, detecting both direct jailbreak attempts and indirect prompt injection from retrieved documents. Provides classification scores and block/allow decisions that can be logged per 13.1.5.
- **Cloudflare Firewall for AI** -- Edge-layer protection that intercepts LLM API traffic, applying prompt injection and jailbreak detection rules across all models behind a single policy. Enforces guardrails at the network layer before requests reach model endpoints.
- **Akamai Firewall for AI** -- Real-time monitoring and adaptive filtering that detects jailbreaks, prompt injections, and toxic content with guardrail policies applied at the CDN/WAF layer.
- **Palo Alto Networks AI Security** -- Enterprise AI security posture management with prompt injection detection integrated into their NGFW and Prisma Cloud platforms. Unit 42 research has documented web-based indirect prompt injection attacks against AI agents observed in the wild.

These products enable requirement 13.2.2 (SIEM integration) by emitting structured security events via standard protocols (CEF, syslog, OTLP) that flow into existing SOC workflows.

### Evolving Attack Landscape

The threat landscape for AI abuse detection continues to evolve rapidly:

- **Best-of-N (BoN) Jailbreaking** -- Automated attacks that generate large numbers of prompt variations using obfuscation techniques (character substitution, encoding, rephrasing), achieving near-100% success rates against safety filters in seconds. This makes signature-based detection (13.2.1) necessary but insufficient -- behavioral detection (13.2.4) and session analysis (13.2.8) are critical complementary layers.
- **Multi-turn Crescendo Attacks** -- Attackers gradually shift model behavior across conversation turns, with no single turn being overtly malicious. Detection requires session-level trajectory analysis (13.2.8) using sliding window analysis over conversation embeddings or cumulative risk scoring.
- **Indirect Prompt Injection via Tool Use** -- As AI agents gain tool-calling capabilities, adversarial content embedded in retrieved documents, web pages, or API responses can hijack agent behavior. Detection must extend beyond user-submitted prompts to cover all inputs the model processes.
- **LLM-as-C2-Channel** -- Security researchers have demonstrated command-and-control frameworks using LLM APIs (ChatGPT, Claude) as communication channels, validating the threat addressed by 13.2.10. Detection relies on entropy analysis of inputs/outputs, periodicity detection in session patterns, and structural analysis of query patterns.

### Detection Architecture

A layered detection architecture addresses the full spectrum of requirements:

1. **Layer 1 -- Signature-Based (13.2.1):** Pattern matching against known jailbreak databases (JailbreakBench, PromptInject). Fast, low false-positive, but easily evaded by novel attacks. Signature databases require continuous updates.
2. **Layer 2 -- Classifier-Based (13.2.4):** ML classifiers trained on adversarial input datasets detect prompt injection and jailbreaks that evade signatures. Azure Prompt Shields and similar products operate at this layer.
3. **Layer 3 -- Behavioral Anomaly (13.2.4, 13.2.9):** Statistical anomaly detection on session-level features (retry rates, token consumption patterns, input diversity scores, query timing). Catches automated attack tools and probing behavior.
4. **Layer 4 -- Session Trajectory (13.2.8):** Multi-turn conversation analysis using embedding similarity, cumulative risk scoring, or LLM-as-judge evaluation of conversation summaries. Detects crescendo attacks and progressive manipulation.
5. **Layer 5 -- Cross-Session Correlation (13.2.6):** SIEM rules correlating events across users, IPs, and time windows to detect coordinated campaigns and model extraction attempts.

### SIEM Integration Patterns

For requirement 13.2.2, the most maintainable integration approach in 2025-2026 uses OpenTelemetry pipelines:

- **Collection:** OpenTelemetry SDK emits GenAI spans with security event attributes
- **Processing:** OpenTelemetry Collector or Vector/Fluentd normalizes and enriches events
- **Routing:** OTLP export to SIEM (Splunk, Elastic, Sentinel) alongside observability backends
- **Detection:** Custom SIEM rules augmented with AI-specific detection logic (13.2.6)

Most SIEMs still lack native AI event parsers as of 2026, requiring custom parsing rules and field mappings for AI-specific attributes.

---

## Related Standards & References

- **MITRE ATLAS** -- Tactics and techniques for adversarial ML, directly informing detection rules ([atlas.mitre.org](https://atlas.mitre.org/))
- **OWASP Top 10 for LLM Applications 2025** -- LLM01 (Prompt Injection) remains the top-ranked vulnerability
- **Azure AI Content Safety -- Prompt Shields** -- Unified API for jailbreak and prompt injection detection ([learn.microsoft.com](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection))
- **Cloudflare Firewall for AI** -- Edge-layer AI security with prompt injection detection ([blog.cloudflare.com](https://blog.cloudflare.com/block-unsafe-llm-prompts-with-firewall-for-ai/))
- **Akamai Firewall for AI** -- CDN-layer guardrails for AI applications ([akamai.com](https://www.akamai.com/products/firewall-for-ai))
- **Palo Alto Unit 42 -- Indirect Prompt Injection in the Wild** -- Research documenting web-based indirect prompt injection against AI agents ([unit42.paloaltonetworks.com](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/))
- **Best-of-N Jailbreaking** -- Automated attack technique achieving near-100% bypass rates ([giskard.ai](https://www.giskard.ai/knowledge/best-of-n-jailbreaking-the-automated-llm-attack-that-takes-only-seconds))
- **JailbreakBench** -- Standardized jailbreak evaluation dataset useful for testing 13.2.1
- **NIST SP 800-61 Rev 2** -- Computer Security Incident Handling Guide, foundation for AI IR workflows
- **Elastic Detection Rules** -- Open-source SIEM rules that can be extended with AI-specific patterns

---

## Open Research Questions

- How effective are embedding-based similarity detectors at catching novel jailbreaks not in signature databases?
- What is the optimal window size for multi-turn trajectory analysis (13.2.8) that balances detection latency with false positive rates?
- Can LLM-as-judge approaches reliably detect adversarial conversations without introducing unacceptable latency?
- What entropy thresholds reliably distinguish C2 traffic from legitimate Base64 usage (e.g., image uploads) in LLM API traffic?
- How should detection rules be shared across organizations without revealing proprietary model vulnerabilities?
- How do AI firewall products (Azure Prompt Shields, Cloudflare, Akamai) compare in detection rates for novel vs. known jailbreak techniques, and what are the latency/accuracy tradeoffs of edge-layer vs. application-layer detection?
- What is the false positive rate of behavioral anomaly detection systems in high-volume production environments, and how should thresholds adapt to different user populations?

---
