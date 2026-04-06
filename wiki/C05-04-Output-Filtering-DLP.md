# C5.4: Output Filtering & Data Loss Prevention

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-03-29

## Purpose

Deploy post-processing controls to prevent unauthorized data exposure in AI-generated content. AI models can memorize and regurgitate training data, RAG pipelines can surface sensitive documents in responses, and prompt injection can cause models to output restricted information. Post-inference filtering, citation validation against caller entitlements, and output format restrictions are all necessary to prevent data loss through AI-generated outputs. The emergence of agentic browsers and autonomous tool use has introduced a new class of exfiltration risk where agents leak data through their own authorized channels, bypassing traditional DLP controls entirely.

> **Scope note:** Controls in this section govern post-inference output filtering, citation access validation, and output format restrictions. Query-time enforcement at the data layer is in C5.3; multi-tenant isolation is in C5.5.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.4.1** | **Verify that** post-inference filtering mechanisms prevent responses from including classified information or proprietary data that the requestor is not authorized to receive. | 1 | Model memorization leaking training data PII in outputs; RAG pipelines surfacing sensitive documents in responses; prompt injection causing the model to output restricted information. | Submit prompts designed to elicit PII (names, SSNs, emails); confirm redaction in outputs; test with known training data snippets; verify redaction covers structured and unstructured PII patterns. | NER-based PII detection (spaCy, Presidio, Google DLP API) provides baseline coverage. False negatives are common with novel PII formats or multilingual content. Balancing redaction aggressiveness with output utility is an ongoing challenge. **[2026-03]** The PerplexedBrowser vulnerability family (Zenity Labs, Mar 2026) demonstrated how agentic browsers operating in authenticated sessions can be hijacked via indirect prompt injection embedded in routine content (e.g., calendar invites), causing the agent to exfiltrate data while returning expected results to the user. This "zero-click agent compromise" pattern bypasses traditional output filtering because the exfiltration occurs through the agent's own authorized channels. |
| **5.4.2** | **Verify that** citations, references, and source attributions in model outputs are validated against caller entitlements and removed if unauthorized access is detected. | 2 | RAG systems citing documents the user is not authorized to view; source attribution revealing the existence of classified or restricted documents; indirect information disclosure through citation metadata. | Query the system as a low-privilege user; verify cited sources are within the user's access scope; test with documents at multiple classification levels; confirm unauthorized citations are stripped without breaking response coherence. | Unique to RAG architectures. Requires cross-referencing citation source IDs against the caller's document-level entitlements at output time. Most RAG frameworks (LlamaIndex, LangChain) do not natively enforce citation-level access control. |
| **5.4.3** | **Verify that** output format restrictions (sanitized documents, metadata-stripped images, approved file types) are enforced based on user permission levels and data classifications. | 2 | Data exfiltration through unrestricted output formats (e.g., raw model weights in JSON, unsanitized PDFs with embedded metadata); metadata leakage in generated images (EXIF data, generation parameters). | Request outputs in various formats with different privilege levels; confirm format restrictions are enforced; verify metadata stripping (EXIF, document properties) is applied; test that unapproved file types are rejected. | Multimodal AI systems generate diverse output types (images, audio, documents) each with format-specific metadata risks. EXIF stripping for images, PDF sanitization, and format allow-listing are needed. Tools like ExifTool and Apache Tika can support implementation. |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
