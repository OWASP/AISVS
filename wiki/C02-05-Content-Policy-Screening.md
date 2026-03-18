# C2.5 Content & Policy Screening

> **Parent:** [C02: User Input Validation](C02-User-Input-Validation)

## Purpose

Even syntactically valid and well-formed prompts may request disallowed content -- violence, self-harm instructions, hate speech, sexual content, illegal activities, or content that violates organizational policies. Content screening classifiers analyze the semantic intent of inputs and outputs to detect policy violations before they propagate through the system. This section requires both automated classification and policy-based gating, with configurable thresholds to balance safety with usability across different deployment contexts.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **2.5.1** | **Verify that** a content classifier scores every input and output for violence, self-harm, hate, sexual content and illegal requests, with configurable thresholds. | 1 | D | Generation of harmful content; policy-violating outputs; liability exposure from producing illegal or dangerous content; reputational damage from harmful AI responses. | 1. Confirm a content classification service is integrated (e.g., OpenAI Moderation API, Azure AI Content Safety, Anthropic content filtering, LLM Guard, Perspective API). 2. Verify it runs on both inputs (pre-model) and outputs (post-model). 3. Test with known harmful content across all categories (violence, self-harm, hate, sexual, illegal). 4. Confirm thresholds are configurable per category (not hard-coded). 5. Check that threshold configuration is documented and reviewed periodically. | Most major providers offer content classification APIs. OpenAI Moderation API is free and covers the listed categories. Azure AI Content Safety provides severity scores (0-6) per category. For self-hosted models, LLM Guard or custom classifiers are needed. Thresholds should be configurable because appropriate sensitivity varies by use case (e.g., a medical chatbot needs to discuss self-harm without blocking). Classifier evasion through paraphrasing or coded language remains a known limitation. |
| **2.5.2** | **Verify that** inputs which violate policies will be rejected so they will not propagate to downstream model or tool/MCP calls. | 1 | D/V | Policy-violating content reaching the model and producing harmful outputs; cascade of harmful content through tool calls or agent chains; downstream systems acting on policy-violating instructions. | 1. Confirm screening runs before prompt assembly / model invocation. 2. Test with policy-violating inputs and verify they are rejected (not passed to the model with a warning). 3. For agent architectures, verify that rejected content does not propagate to downstream tool calls, MCP servers, or sub-agents. 4. Verify the rejection response is safe (does not echo back the harmful content or explain how to rephrase it to bypass the filter). | "Rejected" means the input does not reach the model at all -- not that the model is asked to handle it. This is a critical architectural requirement: screening must be a gateway, not advisory. In agent chains, a rejected input at one hop must not be retried or reformulated by the agent to bypass the filter. The rejection response must avoid being a "helpful refusal" that teaches the attacker how to rephrase. |
| **2.5.3** | **Verify that** screening respects user-specific policies (age and regional legal constraints) via attribute-based rules resolved at request time, including agent-role attributes. | 2 | D | Exposure of age-inappropriate content to minors; violation of regional regulations (e.g., GDPR, COPPA, EU AI Act, China's AI regulations); failure to enforce role-based content restrictions in multi-tenant systems. | 1. Review the policy engine for attribute-based access control (ABAC) integration. 2. Confirm user attributes (age, region, role) are available at request time and used to select screening policies. 3. Test with different user profiles (minor vs. adult, EU vs. US, admin vs. standard user) and verify different screening thresholds apply. 4. For agent roles, verify that an agent's role attribute constrains what content it can process and generate. | Requires integration with identity/authentication systems to obtain user attributes at request time. Policy rules should be externalized (not hard-coded) for maintainability. Regional legal constraints are complex and evolving -- the EU AI Act, COPPA, and various national AI regulations impose different requirements. A policy engine (e.g., OPA/Rego, Cedar, or custom ABAC) is recommended over ad-hoc if/else logic. Agent-role attributes are particularly important in multi-agent systems where different agents have different privilege levels. |
| **2.5.4** | **Verify that** screening logs include classifier confidence scores and policy category tags with applied stage (pre-prompt or post-response) and trace metadata (source, tool or MCP server, agent ID, session as applicable), and generate alerts for investigation. | 3 | V | Inability to audit content screening decisions; missing data for tuning classifier thresholds; failure to detect classifier drift or evasion patterns; regulatory non-compliance with audit requirements. | 1. Review screening log format and confirm it includes: classifier name/version, confidence scores per category, policy category matched, screening stage (pre-prompt/post-response), trace metadata. 2. Verify alerts are generated for high-confidence policy violations (integration with SIEM/alerting platform). 3. Confirm logs are retained per regulatory requirements. 4. Test that logs are generated for both blocked and borderline (near-threshold) content. | Level 3 because comprehensive structured logging with alerting requires significant operational infrastructure. Logging borderline cases (near-threshold) is important for threshold tuning. Classifier confidence scores should be numerical, not just pass/fail, to enable trend analysis. Alert fatigue is a real risk -- alerting rules should be tuned to escalate only high-confidence violations or emerging patterns. Logs must be stored securely as they contain representations of harmful content. |

---

## Related Standards & References

- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/)
- [Anthropic Usage Policy](https://www.anthropic.com/policies/aup)
- [LLM Guard by Protect AI](https://llm-guard.com/)
- [Perspective API (Google/Jigsaw)](https://perspectiveapi.com/)
- [EU AI Act -- High-Risk AI Systems Requirements](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [COPPA -- Children's Online Privacy Protection Act](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)

---

## Open Research Questions

- How effective are current content classifiers against adversarial paraphrasing and coded language?
- What is the right balance between over-blocking (false positives harming usability) and under-blocking (false negatives allowing harmful content)?
- How should content screening evolve for multi-turn conversations where individual messages are benign but the conversation trajectory is harmful (crescendo attacks)?
- Can content classifiers be reliably evaluated across languages and cultures, or are they inherently biased toward English-language norms?
- How should organizations handle the tension between open-ended AI assistants and strict content policies?

---
