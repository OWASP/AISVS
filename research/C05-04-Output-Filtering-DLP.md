# C5.4: Output Entitlement Enforcement

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-04-16

## Purpose

Deploy post-processing controls to prevent unauthorized data exposure in AI-generated content. AI models memorize and regurgitate training data, RAG pipelines surface sensitive documents in responses, and prompt injection causes models to output restricted information. Post-inference filtering, citation validation against caller entitlements, and output format restrictions are all necessary to prevent data loss through AI-generated outputs. The emergence of agentic browsers and autonomous tool use has introduced a new class of exfiltration risk where agents leak data through their own authorized channels, bypassing traditional DLP controls entirely.

This control stack sits downstream of retrieval-time filtering (C5.3) and complements it. Retrieval-time enforcement prevents unauthorized documents from entering the model's context; output-time enforcement is the last line of defense when retrieval filters fail, when the model hallucinates plausible-but-restricted content, or when indirect prompt injection causes the model to restate data the caller is not entitled to see. In 2026, output filtering is also the decision point that sees the full model response and has one chance to redact or block it before it is rendered to the caller or passed to a downstream tool.

> **Scope note:** Controls in this section govern post-inference output filtering, citation access validation, and output format restrictions. Query-time enforcement at the data layer is in C5.3; policy decision point isolation for agents is in C5.5; multi-tenant isolation is in C5.6. General safety filtering (toxicity, PII redaction, confidential data blocking where entitlements don't vary per caller) is in C7.3.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.4.1** | **Verify that** post-inference filtering mechanisms prevent responses from including classified information or proprietary data that the requestor is not authorized to receive. | 1 | Training-data memorization leaking PII in model outputs (OWASP LLM02:2025 Sensitive Information Disclosure, which moved from #6 to #2 in the 2025 Top 10 after targeted extraction techniques matured); RAG pipelines surfacing documents the caller cannot read; indirect prompt injection causing the model to restate restricted information (MITRE ATLAS AML.T0051 LLM Prompt Injection, AML.T0057 Exfiltration via ML Inference API); agentic exfiltration where write-capable tools (email, calendar, CRM) encode secrets in parameter strings (MITRE ATLAS AML.TA0010 Exfiltration, sub-technique "Exfiltration via AI Agent Tool Invocation" added in ATLAS v5.4.0, Feb 2026). | Submit prompts engineered to elicit PII, credentials, and memorized training snippets using the OWASP LLM02 extraction playbook. Probe with multilingual payloads — the Zenity PerplexedBrowser work showed guardrails that only inspect English output miss Hebrew-language exfiltration instructions. Verify redaction covers structured PII (SSN, credit card, passport via regex), unstructured PII (names, addresses via NER), and domain-specific secrets (internal project codenames, revenue figures). Inspect the filtering pipeline's fail-closed behavior: when the detector errors or times out, the response must be blocked, not forwarded. Confirm logs record every redaction event with the rule that fired so incident responders can reconstruct what was almost leaked. | **Tooling.** Microsoft Presidio (open-source, supports text and image PII via Tesseract OCR), Google Cloud DLP API, AWS Comprehend PII detection, Nightfall AI (commercial, purpose-built for LLM pipelines), Netwrix Endpoint Protector DLP-for-LLMs, PrivacyScrubber. Microsoft Fabric's native `ai.extract` and `ai.generate_response` functions redact PII inline without external libraries. **Gaps.** NER-based detectors have consistent false-negative rates on novel PII formats and non-Latin scripts. System-prompt instructions telling the model "do not return SSNs" are regularly bypassed via prompt injection (OWASP LLM02 explicitly warns against relying on them). **[2026-02]** Check Point Research disclosed a ChatGPT code-execution-runtime vulnerability where a single prompt activated a hidden exfiltration channel silently streaming conversation content to an attacker-controlled server — a reminder that output filtering running inside the same sandbox as the model is itself part of the attack surface. **[2026-03]** Zenity Labs' PleaseFix / PerplexedBrowser family (disclosed March 3 2026) demonstrated zero-click agent compromise in Perplexity Comet via a weaponized calendar invite: indirect prompt injection caused the agent to read local `file://` paths and exfiltrate contents via URL query parameters to an attacker site while returning expected results to the user. Perplexity's fix was a hard-coded `file://` boundary rather than relying on the LLM to self-restrict, reinforcing that output filtering must treat the agent itself as untrusted. Microsoft Edge at RSAC 2026 (March 23 2026) announced that existing Purview DLP policies now automatically apply to Agent Mode multi-tab reasoning sessions. |
| **5.4.2** | **Verify that** citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 2 | RAG systems citing documents the caller is not authorized to view; source attribution revealing the existence (even just the filename or title) of classified or restricted documents; indirect information disclosure through citation metadata such as document IDs, author names, or project codenames embedded in footnotes; "phantom citations" where the model fabricates a plausible-looking URL that happens to match a real restricted resource. | Query the system as each persona in an access tier (anonymous, employee, contractor, executive) and diff the citation sets. Any citation that appears for a lower tier but points to higher-tier content is a leak. Test with documents at multiple Purview sensitivity labels and confirm citations to higher-label content are stripped for low-label users without breaking response coherence. Verify the filter runs after response generation but before any tool call that might send the citation list downstream (Slack message, email, webhook). Seed the index with canary documents readable only by a specific test user, then verify other users never receive the canary's title or ID in any citation, footnote, or "sources consulted" block. | **Native platform support (2026).** Azure AI Search (2025-11-01-preview API) supports four document-level access models: security-string filters, POSIX-like ACL / RBAC scopes for ADLS Gen2 and Azure Blob, Microsoft Purview sensitivity labels, and SharePoint ACLs — all enforced at query time via the `x-ms-query-source-authorization` header carrying the user's Microsoft Entra token. Azure Logic Apps Agent Loop now integrates these filters by default. Glean enforces source-system ACLs (Google Drive, SharePoint) with Purview sensitivity labels in beta and blocks out-of-scope actions via alignment models. Google Vertex AI Search inherits ACLs from Drive, Cloud Storage, BigQuery, and web connectors. Pinecone documents the pattern for metadata-based security trimming. **Gaps.** LangChain and LlamaIndex still do not natively enforce citation-level access control — applications have to layer Human-in-the-Loop middleware or custom retrieval callbacks on top. CVE-2025-1793 (LlamaIndex SQL injection) illustrated how tool-level bypasses can sidestep application-layer entitlement checks entirely. Cross-tenant RAG deployments still struggle with citation sanitization when a single index serves multiple tenants with overlapping but non-identical document sets. No widely-adopted standard exists for proving to an external auditor that every citation in a production response was entitlement-checked — most teams rely on sampled replay against a ground-truth ACL dataset. |

---

## Implementation Notes

**Defense-in-depth stack.** Treat output filtering as the third layer, not the only layer. Layer 1: retrieval-time entitlement enforcement (C5.3) — prevents unauthorized documents from entering context. Layer 2: data classification propagation (C5.2.3) — labels follow content through embeddings and prompt caches so output filters can see what sensitivity level they're inspecting. Layer 3 (this control): post-inference redaction, citation validation, and format restriction.

**Fail-closed posture.** When the output filter errors, times out, or encounters an unparseable response, the default must be to block, not pass. Attackers who can induce detector errors (malformed UTF-8, extremely long outputs, structured data that breaks the parser) will otherwise get a free pass. Log every fail-closed event.

**Agentic outputs.** For agents that can invoke write-capable tools, filtering the final text response is insufficient — every tool invocation is an output channel. Apply the same entitlement checks to tool arguments as to user-visible text. The PerplexedBrowser case is the canonical example: exfiltration happened through URL navigation, not through the rendered response.

**Monitoring signals.** Track per-user redaction rates (sudden spikes suggest a new jailbreak), citation-strip rates (a user whose citations are constantly stripped is either misconfigured or probing), and detector-error rates (rising errors may indicate adversarial input crafted to fail the detector).

**Regulatory hooks.** EU AI Act high-risk obligations become fully enforceable August 2 2026 — output filtering that handles PII or makes entitlement decisions is typically in scope. NIST AI RMF's MEASURE and MANAGE functions expect documented output-filtering controls with effectiveness evidence. ISO/IEC 42001 clauses on information security controls map directly to these requirements.

---

## References

* [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
* [OWASP Top 10 for LLM Applications 2025 (PDF)](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)
* [MITRE ATLAS](https://atlas.mitre.org/)
* [Microsoft Presidio (GitHub)](https://github.com/microsoft/presidio)
* [Microsoft Presidio (docs)](https://microsoft.github.io/presidio/)
* [Azure AI Search — Document-Level Access Control](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview)
* [Secure AI Agent Knowledge Retrieval — Security Filters in Agent Loop (Microsoft, 2026)](https://techcommunity.microsoft.com/blog/integrationsonazureblog/%F0%9F%94%90secure-ai-agent-knowledge-retrieval---introducing-security-filters-in-agent-lo/4467561)
* [Microsoft Edge RSAC 2026 — Shadow AI and Agent Mode DLP announcements](https://blogs.windows.com/msedgedev/2026/03/23/protect-your-enterprise-from-shadow-ai-and-more-announcements-at-rsac-2026/)
* [Zenity Labs — PerplexedBrowser local file exfiltration](https://labs.zenity.io/p/perplexedbrowser-perplexity-s-agent-browser-can-leak-your-personal-pc-local-files)
* [Zenity Labs — PerplexedBrowser 1Password vault takeover](https://labs.zenity.io/p/perplexedbrowser-how-attackers-can-weaponize-comet-to-takeover-your-1password-vault)
* [Help Net Security — The vulnerability that turns your AI agent against you (March 2026)](https://www.helpnetsecurity.com/2026/03/04/agentic-browser-vulnerability-perplexedbrowser/)
* [Glean — Permissions-aware AI frameworks](https://www.glean.com/perspectives/security-permissions-aware-ai)
* [Pinecone — RAG with Access Control](https://www.pinecone.io/learn/rag-access-control/)
* [Nightfall AI — DLP for LLMs guide](https://www.nightfall.ai/ai-security-101/data-leakage-prevention-dlp-for-llms)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

## Related Pages

- [C7.3 Output Safety & Privacy Filtering](C07-03-Output-Safety-Privacy-Filtering.md) — general-purpose output safety (content moderation, PII redaction, exfiltration defense) that applies before the entitlement-aware checks in this section.
- [C8.1 Access Controls for Memory & RAG](C08-01-Access-Controls-Memory-RAG.md) — retrieval-side entitlement enforcement for vector stores; upstream of the citation validation in 5.4.2.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
