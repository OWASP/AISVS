# C5.4: Output Entitlement Enforcement

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-05-13

## Purpose

Deploy post-processing controls to prevent unauthorized data exposure in model-generated content. AI models memorize and regurgitate training data, RAG pipelines surface sensitive documents in responses, and prompt injection causes models to output restricted information. Post-inference filtering, citation validation against caller entitlements, and output format restrictions are all necessary to prevent data loss through model-generated outputs. The emergence of agentic browsers and autonomous tool use has introduced a new class of exfiltration risk where agents leak data through their own authorized channels, bypassing traditional DLP controls entirely.

This control stack sits downstream of retrieval-time filtering (C5.3) and complements it. Retrieval-time enforcement prevents unauthorized documents from entering the model's context; output-time enforcement is the last line of defense when retrieval filters fail, when the model hallucinates plausible-but-restricted content, or when indirect prompt injection causes the model to restate data the caller is not entitled to see. As of May 2026, output filtering is also the decision point that sees the full model response and has one chance to redact or block it before it is rendered to the caller, embedded in citation metadata, or passed to a downstream tool.

The highest-risk failures now show up outside the visible answer. Check Point Research disclosed a March 2026 ChatGPT code-execution runtime issue where DNS resolution became a hidden outbound channel for conversation and uploaded-file data. Zenity's March 2026 PerplexedBrowser disclosure showed an agentic browser reading local `file://` resources and exfiltrating them through routine navigation. Palo Alto Networks Unit 42 has also documented web-based indirect prompt injection in the wild, including payloads aimed at ad-review systems, unauthorized transactions, data destruction, and sensitive information leakage. These cases reinforce that output filtering must inspect final text, citations, structured fields, network-bound tool arguments, and browser or agent actions as separate output channels.

> **Scope note:** Controls in this section govern post-inference output filtering, citation access validation, and output format restrictions. Query-time enforcement at the data layer is in C5.3; policy decision point isolation for agents is in C5.5; multi-tenant isolation is in C5.6. General safety filtering (toxicity, PII redaction, confidential data blocking where entitlements don't vary per caller) is in C7.3.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.4.1** | **Verify that** post-inference filtering mechanisms prevent responses from including classified information or proprietary data that the requestor is not authorized to receive. | 1 | Training-data memorization leaking PII in model outputs; RAG pipelines surfacing documents the caller cannot read; prompt injection causing the model to restate restricted information (OWASP LLM01:2025 Prompt Injection and LLM02:2025 Sensitive Information Disclosure; MITRE ATLAS AML.T0051 LLM Prompt Injection and AML.T0057 LLM Data Leakage); agentic exfiltration where write-capable tools such as email, calendar, browser navigation, CRM, or webhooks encode secrets in parameter strings (MITRE ATLAS AML.T0086 Exfiltration via AI Agent Tool Invocation). Unit 42's 2026 in-the-wild web IDPI cases show that hidden page content is now being used against production review and agent workflows, not just lab demos. | Submit prompts engineered to elicit PII, credentials, proprietary snippets, and memorized training fragments using OWASP LLM02-style extraction tests. Seed the prompt, retrieved context, uploaded files, and tool outputs with canary secrets, then confirm they never appear in final text, hidden markdown, rendered HTML attributes, citations, URLs, DNS labels, tool arguments, logs forwarded to users, or webhook payloads. Probe with multilingual and non-Latin payloads; the PerplexedBrowser work showed that single-language guardrails miss exfiltration instructions. Verify redaction covers structured PII (SSN, credit card, passport via regex), unstructured PII (names and addresses via NER), credentials (API keys, SSH keys, cloud tokens), and domain-specific secrets such as project codenames or deal terms. Inspect fail-closed behavior: when the detector errors, times out, receives malformed Unicode, or sees an oversized structured payload, the response and any pending tool invocation must be blocked. Confirm logs record every redaction, block, detector failure, and near-miss canary hit with the rule, user, model, source document, and destination that triggered it. | **Tooling.** Microsoft Presidio supports text anonymization with analyzer and anonymizer modules, including regex, deny-list, checksum, NER, and context-aware recognizers. Google Sensitive Data Protection can inspect and de-identify text, tables, and Cloud Storage content; AWS Comprehend detects PII entities such as credentials and national identifiers; Nightfall's Firewall for AI exposes `/v3/scan` APIs for scanning text and files in RAG data sets and unsupported SaaS flows. Elastic now ships GenAI-oriented detection rules for suspicious outbound domains and encoding/chunking before network activity, which are useful companion telemetry but not a substitute for inline blocking. **Gaps.** NER and regex detectors still miss novel identifiers, non-Latin scripts, and business-specific secrets without custom recognizers. System-prompt instructions telling the model not to return sensitive data are not reliable controls; OWASP LLM02 explicitly notes that prompt-based restrictions can be bypassed. Hidden outbound channels and agent tool arguments are the hard part: the Check Point DNS-channel case and Zenity PerplexedBrowser case both leaked data through channels that a plain final-answer filter would not see. Microsoft Purview's Edge for Business DLP policy activation helps govern unmanaged generative-app use in the browser, but endpoint/browser DLP does not prove that server-side model output, citation metadata, or tool payloads were entitlement-checked. |
| **5.4.2** | **Verify that** citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 2 | RAG systems citing documents the caller is not authorized to view; source attribution revealing the existence of restricted documents through filenames, titles, URLs, authors, labels, or document IDs; citation snippets leaking sensitive passages even when the answer text is redacted; phantom citations that fabricate a plausible URL matching a real restricted resource; indirect prompt injection in retrieved web pages or documents steering the system to expose sources the user should not know exist. | Query the system as each persona in an access tier (anonymous, employee, contractor, executive) and diff both answer text and citation objects. Treat each citation as structured output: validate `source_id`, title, URL, snippet, sensitivity label, author, path, and retrieval score against the caller's live ACL before rendering or passing the response downstream. Seed the index with canary documents readable only by a specific test user, then verify other users never receive the canary's title, URL, chunk ID, embedding metadata, or "sources consulted" entry. Replay production-like questions against a ground-truth ACL dataset and fail the test if the citation filter cannot explain why each displayed source was permitted. For Azure AI Search deployments, inspect whether `x-ms-query-source-authorization` is attached with the caller's Microsoft Entra token and whether SharePoint, ADLS Gen2, Blob, and Purview-label permissions are preserved through ingestion and query time. Verify the filter runs after response generation but before Slack, email, webhook, browser, or agent tool calls that might forward citation lists. | **Native platform support (2026).** Azure AI Search documents four document-level access models: security-string filters, POSIX-like ACL / RBAC scopes for ADLS Gen2 and Azure Blob, Microsoft Purview sensitivity labels, and SharePoint ACLs, with token-based query-time trimming available through preview APIs. Google Vertex AI Search inherits ACLs from connected sources; Glean enforces source-system ACLs and Purview labels; Pinecone documents metadata-based security trimming patterns. LangChain's Human-in-the-Loop middleware can pause risky tool calls for approval, but it does not prove that every citation was entitlement-checked. **Gaps.** Azure preview limitations matter in audits: SharePoint groups are not supported in the current SharePoint ACL preview, Purview sensitivity-label enforcement is single-tenant, and autocomplete/suggest APIs are unavailable for Purview-enabled indexes. Most RAG frameworks still treat citations as application metadata rather than protected output, so teams need custom post-generation checks. Cross-tenant indexes remain difficult because tenants often share filenames, document templates, and chunk IDs. There is still no widely adopted evidence format for proving to an external auditor that every citation in a production response was checked against the caller's entitlements. |

---

## Implementation Notes

**Defense-in-depth stack.** Treat output filtering as the third layer, not the only layer. Layer 1: retrieval-time entitlement enforcement (C5.3) — prevents unauthorized documents from entering context. Layer 2: data classification propagation (C5.2.3) — labels follow content through embeddings and prompt caches so output filters can see what sensitivity level they're inspecting. Layer 3 (this control): post-inference redaction, citation validation, and format restriction.

**Fail-closed posture.** When the output filter errors, times out, or encounters an unparseable response, the default must be to block, not pass. Attackers who can induce detector errors (malformed UTF-8, extremely long outputs, structured data that breaks the parser) will otherwise get a free pass. Log every fail-closed event.

**Gateway placement.** AI gateway and guardrail products are starting to expose controls that are close enough to the model boundary to inspect generated responses before users or downstream tools see them. As of April 2026, Cloudflare AI Gateway DLP scans prompts and responses and explicitly documents that text in tool call arguments and tool results is in scope when it appears in the JSON message body. Its documented limits are audit-relevant: response scanning buffers streamed output, base64-encoded images and file attachments are not decoded, and external URLs are not followed. Lakera Guard takes a similar runtime placement approach, recommending screening after generation and before return to the user or downstream system, with repeated calls at each tool interaction in multi-step agent workflows. These controls are useful only when the application routes every outbound channel through them; separate gateways or policy projects are still needed when tenants, data classes, or latency-sensitive streaming paths require different enforcement.

**Agentic outputs.** For agents that can invoke write-capable tools, filtering the final text response is insufficient; every tool invocation is an output channel. Apply the same entitlement checks to tool arguments as to user-visible text, including email recipients, calendar descriptions, CRM fields, webhook bodies, browser URLs, DNS labels, file names, and attachment metadata. The PerplexedBrowser case is the canonical example: exfiltration happened through URL navigation, not through the rendered response.

**MCP and tool-description poisoning.** Invariant Labs' April 2025 MCP tool-poisoning work showed that malicious tool descriptions can cause an agent to read local configuration or SSH keys and transmit them through a hidden tool parameter. The same research demonstrated "shadowing," where a malicious MCP server changes how the agent uses a separate trusted email tool. For this control, the practical lesson is that output entitlement enforcement must inspect the exact tool payload that will execute, not the summarized approval text in the user interface. Pinning and scanning MCP servers belongs in supply-chain controls, but C5.4 should still block tool arguments that contain secrets, unauthorized source identifiers, or external destinations that the caller is not allowed to use.

**Citation objects are output.** Treat citations, footnotes, source cards, tool traces, and "sources consulted" lists as protected output fields. The caller must be authorized to see the document and the specific metadata shown. If the answer can be shown but the source cannot, render the answer without that citation and log the strip event.

**Audit evidence to collect.**
- Output-filter policy versions, detector configuration, allowlists, and deny-lists active for each environment.
- Canary replay results covering answer text, citation metadata, hidden markdown, rendered HTML attributes, tool arguments, webhook payloads, and logs exposed to users.
- Entitlement decision logs that tie every displayed citation to the caller, source document, ACL or label, policy version, and final allow or strip decision.
- Tool-call enforcement logs with destination, normalized payload, data-classification labels, redaction or block reason, and reviewer decision for any override.
- Fail-closed events for detector timeout, malformed Unicode, oversized payload, parser failure, and unavailable policy services.
- Sampling records showing that streamed responses and low-latency paths do not bypass the output filter.

**Canary replay.** Keep a small set of synthetic secrets and restricted canary documents in each environment. Use them in regression tests and sampled production replay to verify that answer text, citations, browser actions, and tool payloads are blocked before leaving the trust boundary.

**Monitoring signals.** Track per-user redaction rates (sudden spikes suggest a new jailbreak), citation-strip rates (a user whose citations are constantly stripped is either misconfigured or probing), and detector-error rates (rising errors may indicate adversarial input crafted to fail the detector).

**Regulatory hooks.** The EU AI Act's core high-risk AI system obligations apply from August 2 2026, with Article 15 requiring lifecycle accuracy, robustness, and cybersecurity, including resilience against confidentiality attacks and adversarial manipulation. NIST AI RMF's Generative AI Profile expects evidence that risks are measured, monitored, and managed across the lifecycle. ISO/IEC 42001 gives auditors a management-system frame for documenting ownership, risk treatment, control monitoring, and continual improvement around these output-filtering controls.

---

## References

* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [OWASP Top 10 for LLM Applications 2025 (PDF)](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)
* [MITRE ATLAS](https://atlas.mitre.org/)
* [MITRE ATLAS AML.T0086 — Exfiltration via AI Agent Tool Invocation](https://atlas.mitre.org/techniques/AML.T0086/)
* [Check Point Research — ChatGPT Data Leakage via a Hidden Outbound Channel in the Code Execution Runtime](https://research.checkpoint.com/2026/chatgpt-data-leakage-via-a-hidden-outbound-channel-in-the-code-execution-runtime/)
* [Palo Alto Networks Unit 42 — Web-Based Indirect Prompt Injection Observed in the Wild](https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/)
* [Microsoft Presidio (GitHub)](https://github.com/microsoft/presidio)
* [Microsoft Presidio (docs)](https://microsoft.github.io/presidio/)
* [Google Cloud Sensitive Data Protection — De-identifying Sensitive Data](https://cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data)
* [AWS Comprehend — Detect PII Entities](https://docs.aws.amazon.com/cli/latest/reference/comprehend/detect-pii-entities.html)
* [Nightfall — Firewall for AI DLP APIs](https://help.nightfall.ai/developer-api/nightfall_apis/dlp)
* [Cloudflare AI Gateway — Data Loss Prevention (DLP)](https://developers.cloudflare.com/ai-gateway/features/dlp/)
* [Lakera Guard API Endpoint](https://docs.lakera.ai/docs/api/guard)
* [Azure AI Search — Document-Level Access Control](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview)
* [Microsoft Edge — Automatic Activation of Microsoft Purview DLP Policies](https://learn.microsoft.com/en-us/deployedge/microsoft-edge-dlp-purview-configuration)
* [Secure AI Agent Knowledge Retrieval — Security Filters in Agent Loop (Microsoft, 2026)](https://techcommunity.microsoft.com/blog/integrationsonazureblog/%F0%9F%94%90secure-ai-agent-knowledge-retrieval---introducing-security-filters-in-agent-lo/4467561)
* [Microsoft Edge RSAC 2026 — Shadow AI and Agent Mode DLP announcements](https://blogs.windows.com/msedgedev/2026/03/23/protect-your-enterprise-from-shadow-ai-and-more-announcements-at-rsac-2026/)
* [Zenity Labs — PerplexedBrowser local file exfiltration](https://labs.zenity.io/p/perplexedbrowser-perplexity-s-agent-browser-can-leak-your-personal-pc-local-files)
* [Zenity Labs — PerplexedBrowser 1Password vault takeover](https://labs.zenity.io/p/perplexedbrowser-how-attackers-can-weaponize-comet-to-takeover-your-1password-vault)
* [Help Net Security — The vulnerability that turns your AI agent against you (March 2026)](https://www.helpnetsecurity.com/2026/03/04/agentic-browser-vulnerability-perplexedbrowser/)
* [Invariant Labs — MCP Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
* [Glean — Permissions-aware AI frameworks](https://www.glean.com/perspectives/security-permissions-aware-ai)
* [Pinecone — RAG with Access Control](https://www.pinecone.io/learn/rag-access-control/)
* [Nightfall AI — DLP for LLMs guide](https://www.nightfall.ai/ai-security-101/data-leakage-prevention-dlp-for-llms)
* [LangChain — Human-in-the-Loop Middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
* [EU AI Act Service Desk — Article 15: Accuracy, Robustness and Cybersecurity](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-15)
* [EU AI Act Service Desk — Article 113: Entry into Force and Application](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113)
* [ISO/IEC 42001:2023 — AI Management Systems](https://www.iso.org/standard/42001)

---

## Related Pages

- [C2.1 Prompt Injection Defense](../C02-User-Input-Validation/C02-01-Prompt-Injection-Defense.md) — covers the injection paths that can coerce a model or agent into leaking data through final text, citations, or tool calls.
- [C7.6 Source Attribution and Citation Integrity](../C07-Model-Behavior/C07-06-Source-Attribution-Citation-Integrity.md) — pairs with this section where citations must be both truthful and authorized for the caller.
- [C8.2 Embedding Sanitization Validation](../C08-Memory-and-Embeddings/C08-02-Embedding-Sanitization-Validation.md) — addresses upstream RAG and memory hygiene before retrieved content becomes answer text or citation metadata.
- [C9.6 Authorization and Delegation](../C09-Orchestration-and-Agents/C09-06-Authorization-and-Delegation.md) — covers the agent-side authority boundaries that output filters must enforce on delegated actions.
- [C9.7 Intent Verification](../C09-Orchestration-and-Agents/C09-07-Intent-Verification.md) — complements output filtering by checking whether write actions and tool payloads still match the user's approved intent.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
