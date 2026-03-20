# C7.3 Output Safety & Privacy Filtering

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Output safety and privacy filtering prevents harmful, toxic, or privacy-violating content from reaching end users. Models can generate hate speech, harassment, sexually explicit material, or leak personally identifiable information (PII) memorized from training data. These controls apply automated classifiers and redaction mechanisms as a final gate before output delivery. The challenge is balancing effective filtering with avoiding excessive censorship that degrades model utility.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.3.1** | **Verify that** automated classifiers scan every response and block content that matches hate, harassment, or sexual violence categories. | 1 | D/V | **Toxic output delivery.** Without content classification, the model may generate hate speech, harassment, threats, or graphic violence that reaches users — creating legal liability, brand damage, and direct user harm. | Submit prompts designed to elicit toxic content (red-teaming). Confirm the classifier catches and blocks outputs matching defined categories. Test across multiple categories (hate, harassment, sexual violence, self-harm). Verify both direct toxic content and subtler forms (coded language, euphemisms). | Mature tooling exists: OpenAI Moderation API, Perspective API (Google/Jigsaw), Azure AI Content Safety, LLM Guard. Key risk is classifier evasion — adversarial prompts can produce toxic content in forms classifiers do not flag. Multi-layered classification (keyword + ML-based + LLM-as-judge) improves coverage. |
| **7.3.2** | **Verify that** the system scans every response for PII (like credit cards or emails) and automatically redacts it before display. | 1 | D/V | **PII leakage from memorized training data.** LLMs can memorize and reproduce PII from training data (names, emails, phone numbers, SSNs, credit card numbers). Without output-side PII scanning, this data can be exfiltrated through crafted prompts. | Test with prompts designed to extract memorized PII (e.g., "What is [public figure]'s phone number?", completion attacks). Confirm the system detects and redacts PII patterns (credit cards, SSNs, email addresses, phone numbers) in outputs before delivery. Test with multiple PII formats and locales. | Tools: Microsoft Presidio (open-source, configurable entity recognizers), AWS Comprehend PII detection, Google Cloud DLP. Regex-based detection catches structured PII (credit cards, SSNs) well but struggles with unstructured PII (names in context). NER-based approaches provide better coverage for names and addresses. |
| **7.3.3** | **Verify that** PII detection and redaction events are logged without including the redacted PII values themselves, to maintain an audit trail without creating secondary PII exposure. | 1 | D/V | **Secondary PII exposure via logs.** If PII redaction events are logged with the actual PII values, the logs themselves become a data breach vector — creating exactly the exposure the redaction was meant to prevent. | Trigger PII redaction events and examine the resulting log entries. Confirm logs include: event type, timestamp, PII category detected (e.g., "credit_card", "email"), request ID, and redaction action taken. Confirm the actual PII values are NOT present in logs. | This is a common implementation mistake. Developers log the "before" and "after" of redaction for debugging, inadvertently storing PII in log systems that may have weaker access controls than the primary application. Log entry should contain the PII type and position, not the value. |
| **7.3.4** | **Verify that** data labeled as "confidential" in the system remains blocked or redacted. | 2 | D | **Confidential data leakage.** If the system has access to data with confidentiality labels (e.g., internal documents, classified information, proprietary data), the model may include this data in responses to unauthorized users. | Ingest documents with explicit confidentiality markings. Query the system with prompts designed to extract the confidential content. Verify the system either blocks the response or redacts the confidential portions. Test with various phrasing to attempt indirect extraction. | Requires the system to have a data classification scheme and to propagate labels through the retrieval and generation pipeline. In RAG systems, this means checking confidentiality labels on retrieved chunks before including them in the context window. Integration with existing DLP/classification systems is needed. |
| **7.3.5** | **Verify that** safety filters can be configured differently based on the user's role or location (e.g., stricter filters for minors) as appropriate. | 2 | D/V | **Inappropriate content for vulnerable users.** A single filtering threshold cannot serve all audiences. Content acceptable for adult professionals (e.g., medical terminology) may be inappropriate for minors. Without configurable filters, the system either over-censors for adults or under-protects children. | Configure different filter profiles for different user roles (e.g., adult/minor, internal/external). Submit identical prompts under each role and verify that filter behavior differs appropriately. Confirm role assignment cannot be tampered with by end users. | Implementation requires integrating safety filters with the application's identity and access management system. Age verification for minor protection adds complexity. Regulatory requirements vary by jurisdiction (COPPA in the US, Age Appropriate Design Code in the UK). |
| **7.3.6** | **Verify that** the system requires a human approval step or re-authentication if the model generates high-risk content. | 3 | D/V | **Automated delivery of high-risk outputs.** Some outputs (e.g., medical diagnoses, legal advice, financial recommendations, content involving minors) carry enough risk that automated delivery is unacceptable regardless of classifier confidence. Human review provides a final safety net. | Identify the system's high-risk output criteria. Submit prompts that trigger high-risk classification. Verify the system queues the output for human review or requires re-authentication before delivery. Confirm the output is not delivered until approval is granted. | Level 3 because human-in-the-loop introduces latency and operational cost. Applicable primarily in regulated domains (healthcare, legal, finance). Relates to C14 (Human Oversight). The challenge is defining "high-risk" precisely enough to avoid either flooding reviewers or missing critical cases. |

---

## Implementation Guidance (2025-2026 Landscape)

### Content Moderation Tooling

The output safety filtering ecosystem has matured significantly through 2025-2026, with multiple production-ready options:

- **LLM Guard** (Protect AI): Open-source library providing output scanners for content moderation, bias detection, malicious URL detection, and PII anonymization. Supports configurable scanner pipelines.
- **OpenAI Moderation API**: Cloud-hosted content classification covering hate, harassment, self-harm, sexual, and violence categories.
- **Azure AI Content Safety**: Microsoft's multi-category classifier with adjustable severity thresholds.
- **Perspective API** (Google/Jigsaw): Toxicity scoring specialized for text, with multi-language support.
- **SafeGPT** (2026): A two-sided guardrail system integrating input-side detection/redaction, output-side moderation/reframing, and human-in-the-loop feedback. Published results show 92% precision, 87% recall, and 84% policy violation remediation.
- **Agreement Validation Interface (AVI)** (2025): Demonstrated 82% reduction in successful injection attacks, 75% decrease in toxic content generation, and PII detection F1-score of approximately 0.95.
- **Agentgateway**: Provides layered content safety through prompt guards that can reject, mask, or moderate content before it reaches the LLM or returns to users.

### Critical Finding: Output Guardrails Are Weak

A 2025 Palo Alto Unit 42 study comparing LLM guardrails across major GenAI platforms revealed that **output filters consistently underperform input filters**. While input filters blocked 53-92% of malicious prompts depending on platform, output filter detection rates were critically low (0-1.6% of harmful responses caught). The study found that model alignment itself blocked harmful content in 109 out of 123 jailbreak prompts across all platforms, meaning output guardrails provided only marginal additional protection. This underscores the need for **multi-layered classification** (keyword + ML-based + LLM-as-judge) rather than relying on a single output filter.

Common evasion techniques that succeeded included role-play scenarios, indirect phrasing without explicit harmful keywords, and narrative framing embedding malicious requests in fictional contexts.

### PII Detection and Redaction

A 2025 study revealed that 8.5% of prompts submitted to tools like ChatGPT and Copilot included sensitive information -- PII, credentials, and internal file references -- most of which were not flagged by traditional DLP systems because they occurred during natural language interactions rather than structured data entry.

Key PII detection tools for output filtering:

- **Microsoft Presidio**: Open-source, configurable entity recognizers supporting 30+ PII types. Best-in-class for structured PII (credit cards, SSNs, emails).
- **AWS Comprehend PII Detection**: Managed service with NER-based detection for names and addresses in addition to pattern-based detection.
- **Google Cloud DLP**: Enterprise DLP with over 150 built-in infoTypes and custom detector support.
- **Lakera Guard**: Provides PII detection integrated with prompt injection defense as a unified guardrail layer.

Regex-based detection handles structured PII well but struggles with unstructured PII (names in context). NER-based approaches provide better coverage for names, addresses, and contextual PII. Best practice is to combine both approaches.

---

## Related Standards & References

- [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/) — broader output handling risks
- [Microsoft Presidio](https://microsoft.github.io/presidio/) — open-source PII detection and anonymization
- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation) — content classification endpoint
- [Perspective API (Jigsaw/Google)](https://perspectiveapi.com/) — toxicity scoring for text
- [NIST AI 600-1 (GenAI Profile)](https://csrc.nist.gov/pubs/ai/600/1/final) — addresses content safety for generative AI
- [COPPA (Children's Online Privacy Protection Act)](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa) — US regulation relevant to C7.3.5
- [LLM Guard (Protect AI)](https://protectai.com/llm-guard) — open-source LLM security guardrails
- [Palo Alto Unit 42: Comparing LLM Guardrails](https://unit42.paloaltonetworks.com/comparing-llm-guardrails-across-genai-platforms/) — 2025 comparative study of guardrail effectiveness
- [SafeGPT (2026)](https://arxiv.org/html/2601.06366) — two-sided guardrail system for data leakage and unethical output prevention
- [Lakera Guard](https://www.lakera.ai/blog/personally-identifiable-information) — unified PII detection and prompt injection defense
- [Datadog LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/) — deployment guidance for LLM safety filters

---

## Open Research Questions

- How should safety filters handle multilingual content where toxicity classifiers have lower accuracy in non-English languages?
- What is the right trade-off between filtering aggressiveness and model utility? The Unit 42 study found false positive rates ranged from 0.1% to 13.1% across platforms -- how should these be measured and managed?
- How can PII detection be extended to handle emerging PII types (biometric descriptions, behavioral patterns, AI-inferred attributes)?
- Should safety filter configurations be transparent to users, or does transparency enable filter evasion?
- Given that output guardrails catch less than 2% of harmful responses (Unit 42, 2025), should the industry shift investment toward model alignment and input filtering rather than output-side classification?
- How can multi-layered classification approaches (keyword + ML-based + LLM-as-judge) be standardized and benchmarked for consistent cross-platform evaluation?

---
