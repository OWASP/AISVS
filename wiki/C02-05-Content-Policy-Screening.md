# C2.5 Content & Policy Screening

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation)

## Purpose

Even syntactically valid and well-formed prompts may request disallowed content — violence, self-harm instructions, hate speech, sexual content, illegal activities, or content that violates organizational policies. Content screening classifiers analyze the semantic intent of inputs and outputs to detect policy violations before they propagate through the system. This section requires both automated classification and policy-based gating, with configurable thresholds to balance safety with usability across different deployment contexts.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.5.1** | **Verify that** a content classifier scores every input and output for violence, self-harm, hate, sexual content and illegal requests, with configurable thresholds. | 1 | D | Generation of harmful content; policy-violating outputs; liability exposure from producing illegal or dangerous content; reputational damage from harmful AI responses. Relevant MITRE ATLAS techniques: AML.T0054 (LLM Jailbreak), AML.T0051 (Prompt Injection), AML.T0043 (Craft Adversarial Data). | 1. Confirm a content classification service is integrated (e.g., OpenAI Moderation API, Azure AI Content Safety, AWS Bedrock Guardrails, Anthropic content filtering, LLM Guard, Perspective API, IBM Granite Guardian). 2. Verify it runs on both inputs (pre-model) and outputs (post-model). 3. Test with known harmful content across all categories (violence, self-harm, hate, sexual, illegal). 4. Confirm thresholds are configurable per category (not hard-coded). 5. Check that threshold configuration is documented and reviewed periodically. 6. Test multilingual content — verify classifier effectiveness in languages beyond English (low-resource languages exhibit ~3x the harmful content generation rate per ICLR 2024 research). 7. Verify classifiers return numerical confidence scores, not just pass/fail, to support threshold tuning. | Most major providers offer content classification APIs. OpenAI's `omni-moderation-latest` (GPT-4o-based) is free and covers 11 subcategories across 40+ languages with 42% improvement on multilingual evaluation. Azure AI Content Safety provides 4-level severity scoring (Safe/Low/Medium/High) plus Prompt Shields for jailbreak detection. AWS Bedrock Guardrails offers configurable filter strength across 6 categories including prompt attack detection. For self-hosted models, LLM Guard (MIT license, 2.5M+ downloads) provides 15 input scanners and 20 output scanners. Classifier evasion through paraphrasing, coded language, and encoding tricks remains a known limitation — adversarial paraphrasing achieves 87.88% true positive reduction in some evaluations (2025 research). The Palo Alto Unit 42 study (March 2025) found output-only guardrails blocked just 0–1.6% of harmful responses across major platforms, underscoring the need for input-side screening. As of March 2026, an empirical analysis of evasion attacks across six popular guardrail systems (Azure Prompt Shield, Meta Prompt Guard, ProtectAI, NeMo Guard, Vijil) found that simple character transformations and algorithmic AML evasion can reach up to 100% bypass rates — most guardrails are lightweight NLP classifiers fine-tuned on curated datasets and inherently misaligned with the broader corpora their protected LLMs were trained on. |
| **2.5.2** | **Verify that** inputs which violate policies will be rejected so they will not propagate to downstream model or tool/MCP calls. | 1 | D/V | Policy-violating content reaching the model and producing harmful outputs; cascade of harmful content through tool calls or agent chains; downstream systems acting on policy-violating instructions. Crescendo attacks (Russinovich et al., USENIX Security 2025) achieved 98% bypass on GPT-4 via gradual escalation across turns. The Skeleton Key attack (Microsoft, June 2024) bypassed guardrails on Llama3-70b, Gemini Pro, and Claude 3 Opus. | 1. Confirm screening runs before prompt assembly / model invocation — screening must be a gateway, not advisory. 2. Test with policy-violating inputs and verify they are rejected (not passed to the model with a warning). 3. For agent architectures, verify that rejected content does not propagate to downstream tool calls, MCP servers, or sub-agents. 4. Verify the rejection response is safe — does not echo back harmful content, does not explain how to rephrase to bypass the filter, and does not provide a "helpful refusal." 5. Test multi-turn escalation scenarios: send a sequence of individually benign messages that progressively escalate toward harmful content (crescendo attack pattern). 6. Verify that encoding-based bypasses (Base64, hex, Unicode homoglyphs) are handled — character injection reduced OpenAI Prompt Guard detection accuracy by 78–100% in Mindgard testing. | "Rejected" means the input does not reach the model at all — not that the model is asked to handle it. This is a critical architectural requirement: screening must be a pre-model gateway. In agent chains, a rejected input at one hop must not be retried or reformulated by the agent to bypass the filter. The rejection response must avoid being a "helpful refusal" that teaches the attacker how to rephrase. Multi-turn attacks (crescendo, Bad Likert Judge, Deceptive Delight) exploit the fact that most content filters evaluate individual messages rather than conversational trajectories — organizations should evaluate NeMo Guardrails (Apache 2.0) for its unique multi-turn dialog flow control via the Colang DSL. The EchoGram token flip attack (HiddenLayer, November 2025) demonstrated that single "flip tokens" can cause defensive classifiers to misclassify harmful prompts as benign, affecting both text classification and LLM-as-a-judge safety systems. |
| **2.5.3** | **Verify that** screening respects user-specific policies (age and regional legal constraints) via attribute-based rules resolved at request time, including agent-role attributes. | 2 | D | Exposure of age-inappropriate content to minors; violation of regional regulations (e.g., GDPR, COPPA, EU AI Act, China's AI regulations, UK/California Age-Appropriate Design Codes); failure to enforce role-based content restrictions in multi-tenant systems. Updated COPPA rule (effective June 2025, compliance deadline April 22, 2026) expands "personal information" to biometric identifiers and requires separate verifiable parental consent for AI training data from children. EU AI Act Article 5 prohibits AI that exploits vulnerabilities of specific age groups. | 1. Review the policy engine for attribute-based access control (ABAC) integration. 2. Confirm user attributes (age, region, role) are available at request time and used to select screening policies. 3. Test with different user profiles (minor vs. adult, EU vs. US vs. China, admin vs. standard user) and verify different screening thresholds apply. 4. For agent roles, verify that an agent's role attribute constrains what content it can process and generate. 5. Verify age-determination happens before data collection per updated COPPA rules for mixed-audience services. 6. Confirm regional policy variants exist for at least: EU (AI Act + DSA requirements), US (COPPA + state AADC laws), China (Generative AI Measures + content labeling rules), UK (AADC 15 standards). 7. Verify policy rules are externalized in a policy engine, not hard-coded — test policy changes deploy without code changes. | Requires integration with identity/authentication systems to obtain user attributes at request time. Open Policy Agent (OPA/Rego, CNCF Graduated) is the industry-standard general-purpose policy engine for ABAC — supports decision caching, sub-millisecond evaluation, and full decision audit logging. AWS Cedar (CNCF Sandbox as of January 2026) is purpose-built for fine-grained authorization with formally verified safety properties — particularly well-suited for governing agent tool invocations with step-by-step enforcement and ephemeral credentials. Regional legal requirements are complex and evolving: the EU AI Act enforces prohibited practices since February 2025 with penalties up to 35M EUR / 7% global turnover; China's AI content labeling rules took effect September 2025; the US COPPA update takes effect April 2026. Agent-role attributes are critical in multi-agent systems where different agents operate at different privilege levels — Cedar's native tool-authorization model fits this pattern well. As of March 2026, California, Nebraska, Vermont, and Maryland have enacted age-appropriate design codes alongside the federal COPPA update. |
| **2.5.4** | **Verify that** screening logs include classifier confidence scores and policy category tags with applied stage (pre-prompt or post-response) and trace metadata (source, tool or MCP server, agent ID, session) for SOC correlation and future red-team replay. | 3 | V | Inability to audit content screening decisions; missing data for tuning classifier thresholds; failure to detect classifier drift or evasion patterns; regulatory non-compliance with audit requirements. EU AI Act Articles 6–49 require automatic logging and post-market monitoring for high-risk AI — as of August 2026, Annex III high-risk AI system rules become enforceable with penalties up to 15M EUR / 3% global turnover for logging failures. EU DSA mandates transparency reporting on content moderation decisions. ISO 42001 Annex A.8 requires continuous monitoring of performance and drift. Without structured logs correlated to SOC workflows, organizations cannot detect evasion pattern evolution or replay red-team scenarios to validate classifier improvements. | 1. Review screening log format and confirm it includes: classifier name/version, confidence scores per category, policy category matched, screening stage (pre-prompt/post-response), trace metadata (source, tool/MCP server, agent ID, session). 2. Verify logs are forwarded to the organization's SIEM/SOC platform (e.g., Splunk, Sentinel, Datadog) with correlation IDs that link screening decisions to broader request traces. 3. Confirm logs support red-team replay — test that a logged screening decision can be replayed against an updated classifier to measure improvement (requires storing the original input text or a hash reference, classifier version, and decision metadata). 4. Test that logs are generated for both blocked and borderline (near-threshold) content. 5. Verify log storage security — logs contain representations of harmful content and must be access-controlled. 6. Confirm logs are retained per regulatory requirements (EU AI Act post-market monitoring, COPPA written retention policy, China's national AI security standards). 7. Verify audit trail is tamper-evident (immutable logging). 8. Validate that SOC analysts can query screening logs by category, confidence band, and time range to identify evasion trends. | Level 3 because comprehensive structured logging with SOC correlation and replay capability requires significant operational infrastructure. Datadog LLM Observability (SOC 2 Type II compliant) provides end-to-end tracing across AI agents with prompt injection tracking, toxicity scoring, and full trace export for replay — integrates natively with Datadog's SIEM product for SOC correlation. LangWatch (SOC 2 compliant) captures per-request traces across agents, tools, and chains with cost visibility and configurable alerts. Azure AI Content Safety provides built-in monitoring via Content Safety Studio (category/severity distribution, latency, error rates, block rates, Azure Monitor integration for SOC forwarding). AWS Bedrock Guardrails returns guardrail trace data in API responses showing which filters triggered, integrated with CloudWatch and CloudTrail for SOC pipelines. For red-team replay, organizations should archive screening inputs (or secure hashes) alongside decisions so that updated classifiers can be tested against historical attack payloads — tools like Promptfoo (MIT license, acquired by OpenAI March 2026) and DeepTeam (MIT license, 80+ vulnerability types) support automated replay of attack datasets against guardrails in CI/CD pipelines. WhyLabs LangKit provides continuous monitoring with statistical profiling and alerts aligned to MITRE ATLAS and OWASP LLM Top 10. |

---

## Notable Incidents

| Date | Incident | Impact | Relevance |
|------|----------|--------|-----------|
| **Jan 2025** | DeepSeek R1 failed 58% of 885 jailbreak attacks in Qualys testing (18 attack types) | Model produced instructions for money laundering, malware creation, and drug production | Demonstrates consequences of inadequate content screening — content classifiers must cover diverse attack categories |
| **Jan 2025** | US Navy and House of Representatives banned DeepSeek | Institutional access restrictions due to content safety and security concerns | Regulatory and institutional consequences of content screening failures |
| **Mar 2025** | Palo Alto Unit 42 guardrail study found output filters blocked 0–1.6% of harmful responses across 3 major platforms | Role-play disguise bypassed 42 of 51 test cases on one platform | Output-only guardrails are insufficient; input-side screening is essential |
| **Nov 2025** | HiddenLayer published EchoGram token flip attack | Single "flip tokens" (e.g., `=coffee`) defeat both classification and LLM-as-judge guardrails | Content classifiers themselves are vulnerable to adversarial manipulation |
| **Jun 2024** | Microsoft disclosed Skeleton Key jailbreak technique | Bypassed guardrails on Llama3-70b, Gemini Pro, Claude 3 Opus to produce weapons instructions | "Augment rather than change" framing circumvents safety alignment |
| **Apr 2024** | Anthropic published Many-Shot Jailbreaking research (NeurIPS 2024) | Long-context exploitation follows power-law effectiveness across Claude, GPT, Llama, Mistral | Long context windows create new content screening bypass surfaces |
| **2024** | Chevrolet dealership chatbot manipulated into offering vehicles at $1 | Financial and reputational damage from uncontrolled content generation | Business impact of missing content policy enforcement |
| **Apr 2025** | China "Clear and Bright" campaign: 3,500+ AI products removed, 960K+ illegal content pieces removed | Largest AI content enforcement action globally | Demonstrates scale of regulatory enforcement for content screening failures |
| **Apr 2025** | FTC enforcement against AI content detector company for false 98% accuracy claims | Regulatory action for overstating content screening accuracy | Accuracy claims for content classifiers must be substantiated |
| **Oct 2025** | HiddenLayer bypassed OpenAI's guardrails framework using straightforward techniques | Both jailbreak and prompt injection detection defeated; the security judge (itself an LLM) was susceptible to the same manipulation as the model it protected | Architectural limitation: LLM-as-judge guardrails inherit the vulnerabilities of the models they evaluate |
| **Feb 2024** | Mindgard demonstrated Azure AI Content Safety bypasses via character injection and adversarial ML | Character injection reduced AI Text Moderation detection accuracy by 83–100%; Prompt Shield accuracy reduced by 78–100% via homoglyphs, diacritics, and zero-width characters | Even major cloud content safety services are vulnerable to simple text transformations; mitigations deployed by Microsoft by October 2024 |
| **Dec 2025** | European Commission published first draft Code of Practice for marking and labeling AI-generated content | Final version expected June 2026; establishes labeling obligations under AI Act Article 50 | Content screening systems must support AI-generated content detection and labeling to meet upcoming EU transparency requirements |

---

## Tool & Framework Landscape

### Commercial Content Safety APIs

| Tool | Vendor | Categories | Multilingual | Key Differentiator | Pricing |
|------|--------|------------|:------------:|-------------------|---------|
| **Moderation API** (`omni-moderation-latest`) | OpenAI | 11 subcategories (harassment, hate, self-harm, sexual, violence, illicit) | 40+ languages (42% multilingual improvement) | Free, multimodal (text + image), GPT-4o-based | Free |
| **Azure AI Content Safety** | Microsoft | Hate, violence, sexual, self-harm (4 severity levels each) | 8 trained languages + broad coverage | Prompt Shields, Protected Material Detection, Custom Categories, Content Safety Studio monitoring dashboard | Free tier (5 RPS) + pay-per-call |
| **Bedrock Guardrails** | AWS | 6 categories including prompt attack | English-primary, expanding | PII detection/masking, contextual grounding checks, code-element filtering (2025), automated reasoning | Pay-per-evaluation |
| **Vertex AI Safety** | Google | Hate, harassment, sexually explicit, dangerous | Gemini language support | Non-configurable auto-block for CSAM/PII, configurable content filters, Gemini-as-classifier | Included with API usage |
| **Anthropic Filtering** | Anthropic | Aligned to Usage Policy | Claude language support | Constitutional classifiers, free moderation tooling, asynchronous monitoring | Included with API usage |

### Open-Source Tools

| Tool | License | Focus | Maturity |
|------|---------|-------|----------|
| **LLM Guard** (Protect AI) | MIT | 15 input + 20 output scanners; model-agnostic | Production (2.5M+ downloads) |
| **NeMo Guardrails** (NVIDIA) | Apache 2.0 | Multi-turn dialog flow control via Colang DSL; unique conversation-level policy enforcement | Production |
| **Guardrails AI** | Apache 2.0 | Composable validator chains; Guardrails Hub with pre-built validators; Guardrails Index benchmark (Feb 2025) | Production |
| **WhyLabs LangKit** | Apache 2.0 | LLM observability; statistical anomaly detection; alerts aligned to MITRE ATLAS and OWASP LLM Top 10 | Production |
| **IBM Granite Guardian** | Apache 2.0 | Content moderation model for LLM output safety | Production |

### Red-Teaming & Replay Tools

| Tool | License | Focus | Key Feature |
|------|---------|-------|-------------|
| **Promptfoo** (OpenAI, acquired March 2026) | MIT | 50+ vulnerability types; prompt injection, jailbreak, PII leak, toxic content scanning | CI/CD integration via YAML configs and GitHub Actions; adaptive guardrails for production; red-team replay against historical datasets |
| **DeepTeam** (Confident AI) | MIT | 80+ vulnerability types; 7 production guardrails; OWASP Top 10, MITRE ATLAS, NIST AI RMF alignment | Programmatic and CLI-based red teaming; risk assessment tracking across iterations; custom vulnerability type registration |
| **Mindgard** | Commercial | Adversarial ML evasion testing for guardrails; character injection and AML attack simulation | Tested against Azure Prompt Shield, Meta Prompt Guard, NeMo Guard, ProtectAI models; quantifies evasion rates per technique |

### SOC-Integrated Monitoring Platforms

| Platform | Compliance | Content Safety Features | SOC Integration |
|----------|-----------|------------------------|-----------------|
| **Datadog LLM Observability** | SOC 2 Type II | End-to-end agent tracing, prompt injection tracking, toxicity scoring, full trace export | Native SIEM integration, correlation IDs, configurable alerts, dashboard visualization |
| **LangWatch** | SOC 2 | Per-request traces across agents/tools/chains, cost visibility, quality evaluations | Configurable alerts, trace export for replay, multi-step workflow monitoring |

### Policy Engines for ABAC

| Engine | Governance Body | Best For | Key Feature |
|--------|----------------|----------|-------------|
| **OPA / Rego** | CNCF Graduated | General ABAC policy enforcement | Sub-millisecond evaluation, decision caching, tamper-evident audit trails |
| **Cedar** | CNCF Sandbox (Jan 2026) | Agent tool authorization, fine-grained ABAC | Formally verified safety properties, ephemeral credentials, natural policy syntax |

---

## Implementation Maturity

| Requirement | Maturity | Notes |
|-------------|----------|-------|
| **2.5.1** Content classifiers | **High** | Multiple production-ready commercial APIs (OpenAI free, Azure, AWS, Google) and open-source options (LLM Guard, Granite Guardian). Main gap: multilingual coverage in low-resource languages and classifier evasion resistance. |
| **2.5.2** Pre-model rejection | **Medium** | Architectural pattern is well-understood (gateway not advisory), but multi-turn attacks (crescendo, Bad Likert Judge) and token flip attacks (EchoGram) expose fundamental weaknesses. NeMo Guardrails offers unique multi-turn awareness. |
| **2.5.3** User-specific policies (ABAC) | **Medium-Low** | Policy engines (OPA, Cedar) are mature, but integration with content screening systems is typically custom work. No turnkey solution combines content classification with ABAC-based policy resolution. Regional regulatory requirements are complex and rapidly evolving. |
| **2.5.4** Structured screening logs with SOC correlation | **Medium** | Datadog LLM Observability and LangWatch now provide SOC 2-compliant tracing with native SIEM integration — a significant improvement over custom-built pipelines. Azure Content Safety Studio and WhyLabs provide built-in dashboards. Red-team replay tooling (Promptfoo, DeepTeam) supports automated regression testing against archived attack payloads. Main gap: few organizations have established workflows for systematically replaying screening logs against updated classifiers. |

---

## Cross-Chapter Links

| Related Section | Connection |
|----------------|------------|
| [C02-01 Prompt Injection Defense](C02-01-Prompt-Injection-Defense) | Content classifiers complement prompt injection detection — prompt injection bypasses can circumvent content screening (AML.T0051) |
| [C02-02 Adversarial Example Resistance](C02-02-Adversarial-Example-Resistance) | Encoding and obfuscation attacks (Unicode, Base64, homoglyphs) affect both adversarial example detection and content classifiers |
| [C05 Access Control & Identity](C05-Access-Control) | ABAC policy resolution (2.5.3) depends on identity infrastructure for user attributes (age, region, role) |
| [C09 Orchestration & Agentic Action](C09-Orchestration-and-Agents) | Agent-role attributes in 2.5.3 intersect with agentic permission models; rejected content must not propagate through agent chains (2.5.2) |
| [C10 MCP Security](C10-MCP-Security) | Content screening must cover MCP tool inputs/outputs; policy-violating content must not propagate to MCP servers (2.5.2) |
| [C13 Monitoring & Logging](C13-Monitoring-and-Logging) | Screening logs (2.5.4) feed into the broader monitoring and SIEM infrastructure |
| [C14 Human Oversight](C14-Human-Oversight) | Borderline content screening decisions may require human-in-the-loop escalation |

---

## Regulatory Compliance Matrix

| Regulation | Applicable Articles | Content Screening Requirements | Enforcement |
|------------|-------------------|-------------------------------|-------------|
| **EU AI Act** | Art. 5 (prohibited), Art. 50 (transparency), Arts. 51–56 (GPAI), Arts. 6–49 (high-risk) | GPAI must prevent illegal content generation; mandatory deepfake labeling; prohibited AI exploiting age-group vulnerabilities; Annex III high-risk AI system rules enforceable August 2, 2026 (including automatic logging and post-market monitoring); first draft Code of Practice for AI content labeling published December 2025, final version expected June 2026 | Up to 35M EUR / 7% global turnover for prohibited practices (enforced since Feb 2025); up to 15M EUR / 3% for high-risk non-compliance (from Aug 2026) |
| **EU DSA** | Art. 6 (illegal content), Art. 17 (reasons for restriction) | Platforms must act diligently to remove illegal content; transparency reporting on AI-assisted content moderation | Transparency reports due early 2026 |
| **NIST AI RMF** | MAP, MEASURE, MANAGE functions | Voluntary — harm taxonomy, content safety metrics, operational controls | Voluntary; referenced in US federal procurement |
| **COPPA (updated)** | New rule effective June 2025 | Age screening before data collection; separate parental consent for AI training data; biometric identifiers covered | FTC enforcement; compliance deadline April 22, 2026 |
| **ISO 42001** | Annex A.2, A.5, A.8, A.9, A.10 | AI risk assessment, data governance, continuous monitoring, incident management, adversarial robustness | Certification-based |
| **China AI Regulations** | Generative AI Measures (Aug 2023), Labeling Rules (Sept 2025), CSL Amendments (Jan 2026) | Content must adhere to regulatory standards; mandatory AI content labeling; pre-publication review mechanisms | Administrative takedowns — 3,500+ AI products removed in April 2025 "Clear and Bright" campaign |
| **UK AADC** | 15 standards | High-privacy defaults for children; no profiling of minors; age-appropriate content delivery | ICO fines up to 17.5M GBP / 4% turnover |

---

## Related Standards & References

- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/)
- [AWS Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Anthropic Usage Policy](https://www.anthropic.com/policies/aup)
- [LLM Guard by Protect AI](https://llm-guard.com/)
- [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- [Guardrails AI](https://github.com/guardrails-ai/guardrails)
- [WhyLabs LangKit](https://whylabs.ai/langkit)
- [IBM Granite Guardian](https://www.ibm.com/think/tutorials/llm-content-moderation-with-granite-guardian)
- [Perspective API (Google/Jigsaw)](https://perspectiveapi.com/)
- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/)
- [AWS Cedar](https://www.cedarpolicy.com/)
- [EU AI Act — Official Text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [EU Digital Services Act](https://digital-strategy.ec.europa.eu/en/policies/digital-services-act)
- [COPPA Updated Rule](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [Palo Alto Unit 42 — LLM Guardrails Comparison (March 2025)](https://unit42.paloaltonetworks.com/comparing-llm-guardrails-across-genai-platforms/)
- [HiddenLayer — EchoGram Token Flip Attack (November 2025)](https://www.hiddenlayer.com/research/echogram-the-hidden-vulnerability-undermining-ai-guardrails)
- [Crescendo Attack Paper (USENIX Security 2025)](https://arxiv.org/abs/2404.01833)
- [Many-Shot Jailbreaking (Anthropic, NeurIPS 2024)](https://www.anthropic.com/research/many-shot-jailbreaking)
- [Microsoft Skeleton Key Disclosure](https://www.microsoft.com/en-us/security/blog/2024/06/26/mitigating-skeleton-key-a-new-type-of-generative-ai-jailbreak-technique/)
- [Promptfoo — LLM Red Teaming Framework](https://www.promptfoo.dev/docs/red-team/)
- [DeepTeam — LLM Red Teaming by Confident AI](https://github.com/confident-ai/deepteam)
- [Mindgard — Bypassing Azure AI Content Safety Guardrails](https://mindgard.ai/blog/bypassing-azure-ai-content-safety-guardrails)
- [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/)
- [LangWatch — LLM Monitoring](https://langwatch.ai/)
- [Bypassing LLM Guardrails: Empirical Analysis of Evasion Attacks (2025)](https://arxiv.org/html/2504.11168)
- [EU AI Act Code of Practice — AI-Generated Content Labeling (Draft, December 2025)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

---

## Open Research Questions

- How effective are current content classifiers against adversarial paraphrasing and coded language? (Adversarial paraphrasing achieves 87.88% TPR reduction across detector types as of 2025 — the gap remains significant.)
- What is the right balance between over-blocking (false positives harming usability) and under-blocking (false negatives allowing harmful content)? How should organizations measure and report this tradeoff?
- How should content screening evolve for multi-turn conversations where individual messages are benign but the conversation trajectory is harmful? (Crescendo attacks achieve 98% bypass via gradual escalation — NeMo Guardrails' Colang DSL is one approach, but maturity is limited.)
- Can content classifiers be reliably evaluated across languages and cultures, or are they inherently biased toward English-language norms? (Low-resource languages show ~3x harmful content generation rates; code-mixing attacks achieve 99% success.)
- How should organizations handle the tension between open-ended AI assistants and strict content policies in multi-tenant deployments with diverse regulatory requirements?
- Can content classifiers themselves be hardened against adversarial manipulation (e.g., EchoGram token flip attacks), or will the classifier-vs-attacker arms race remain fundamentally asymmetric?
- How should content screening adapt to agentic architectures where content flows through chains of tool calls, MCP servers, and sub-agents with different trust levels?
- What is the minimum viable logging schema for effective red-team replay — can organizations replay screening decisions without storing the original harmful input text, using only hashes and metadata? What are the privacy and regulatory implications of retaining harmful content in screening logs?

---
