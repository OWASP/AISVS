# C7.2 Hallucination Detection & Mitigation

[Back to C07 Index](C07-Model-Behavior)

## Purpose

Hallucination — the generation of plausible-sounding but factually incorrect or fabricated content — is one of the most consequential failure modes of generative AI. In high-stakes domains (medical, legal, financial), hallucinated outputs can cause direct harm. This section addresses detecting unreliable outputs before they reach users, establishing fallback behaviors, logging hallucination events for analysis, and performing independent verification for high-risk responses. The goal is not to eliminate hallucination (which remains an open research problem) but to build layered defenses that limit its impact.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **7.2.1** | **Verify that** the system assesses the reliability of generated answers using a confidence or uncertainty estimation method (e.g., confidence scoring, retrieval-based verification, or model uncertainty estimation). | 1 | D/V | **Undetected hallucination.** Without any reliability signal, the system has no basis for distinguishing high-quality outputs from fabricated ones, and users receive all outputs with equal implied authority. | Confirm the system produces a confidence or reliability score for outputs. Test with known-hallucination-inducing prompts (e.g., questions about nonexistent entities) and verify that low scores are assigned. Review the scoring method (logit-based, retrieval overlap, ensemble disagreement, etc.). | Multiple approaches exist: token-level logprob analysis, semantic similarity to retrieved documents (for RAG), multi-sample consistency (self-consistency decoding), and dedicated hallucination detection models (Vectara HHEM, Lynx). No single method is definitive — combining approaches improves coverage. |
| **7.2.2** | **Verify that** the application automatically blocks answers or switches to a fallback message if the confidence score drops below a defined threshold. | 2 | D/V | **Serving unreliable content.** If low-confidence outputs are served without intervention, users may act on fabricated information. Automatic gating ensures unreliable outputs are caught before delivery. | Configure the confidence threshold to a known value. Submit prompts that produce below-threshold scores and verify the system returns a fallback response (e.g., "I'm not confident in this answer") rather than the low-confidence output. Test edge cases near the threshold boundary. | Threshold selection is domain-dependent. Medical/legal contexts demand higher thresholds (fewer false negatives) at the cost of more refusals. Conversational assistants may tolerate lower thresholds. Threshold tuning requires labeled evaluation data. |
| **7.2.3** | **Verify that** hallucination events (low-confidence responses) are logged with input/output metadata for analysis. | 2 | D/V | **Inability to improve.** Without logging hallucination events, teams cannot identify patterns (e.g., specific topics that consistently hallucinate), track hallucination rates over time, or use the data for model fine-tuning and prompt improvement. | Trigger low-confidence responses and verify log entries include: timestamp, confidence score, input prompt (or hash), output text (or hash), model version, and retrieval context (if RAG). Confirm PII is not logged or is appropriately redacted. | Logs should feed into C7.6 monitoring dashboards. Consider whether to log the full output or a hash/summary to balance forensic value against data retention risks. |
| **7.2.4** | **Verify that** for responses classified as high-risk or high-impact by policy, the system performs an additional verification step through an independent mechanism, such as retrieval-based grounding against authoritative sources, deterministic rule-based validation, tool-based fact-checking, or consensus review by a separately provisioned model. | 3 | D/V | **Single-point-of-failure hallucination in critical contexts.** A single model's confidence score may be miscalibrated. For high-stakes decisions, an independent verification mechanism provides a second line of defense against hallucinated content. | Identify the system's high-risk classification criteria. Submit prompts that trigger high-risk classification and confirm a secondary verification step executes. Verify the verification method is genuinely independent (e.g., a different model, a knowledge base lookup, a deterministic rule engine — not just re-querying the same model). | This is Level 3 because independent verification is computationally expensive and architecturally complex. Approaches include: separate "judge" model evaluation, retrieval-based fact verification against curated knowledge bases, and deterministic validation for structured claims (e.g., checking dates, calculations, entity existence via APIs). |
| **7.2.5** | **Verify that** the system tracks tool and function invocation history within a request chain and flags high-confidence factual assertions that were not preceded by relevant verification tool usage, as a practical hallucination detection signal independent of confidence scoring. | 2 | D/V | **Unsupported factual claims in agentic workflows.** In tool-augmented systems, a model may assert facts with high confidence without actually having called a verification tool. Tracking tool invocation history catches assertions that lack evidential grounding. | In an agentic or tool-augmented system, submit prompts that require factual lookup (e.g., "What is the current stock price of X?"). Verify that the system flags responses containing factual assertions where no relevant tool (e.g., stock price API) was invoked in the request chain. | This control is specific to agentic/tool-augmented architectures. It provides a structural hallucination signal — if the model claims to know something it never looked up, that is inherently suspect. Requires maintaining a tool invocation log per request chain and defining which assertion types require tool backing. |

---

## Related Standards & References

- [OWASP LLM Top 10 — Overreliance](https://genai.owasp.org/) — risks from trusting model outputs without verification
- [Vectara HHEM (Hughes Hallucination Evaluation Model)](https://huggingface.co/vectara/hallucination_evaluation_model) — open-source hallucination detection model
- [RAGAS (Retrieval Augmented Generation Assessment)](https://docs.ragas.io/) — framework for evaluating RAG pipeline faithfulness, relevance, and context utilization
- [SelfCheckGPT (Manakul et al., 2023)](https://arxiv.org/abs/2303.08896) — zero-resource hallucination detection via sampling consistency
- [FActScore (Min et al., 2023)](https://arxiv.org/abs/2305.14251) — fine-grained atomic fact scoring for long-form generation

---

## Open Research Questions

- What hallucination rate is acceptable for different risk domains (medical vs. creative writing vs. customer support)?
- How should confidence thresholds be calibrated when models are frequently updated and calibration may shift?
- Can hallucination detection methods generalize across domains, or do they require domain-specific training data?
- How should systems handle "confident hallucinations" — factually wrong outputs that receive high confidence scores from the model?
- Is there a principled way to distinguish creative embellishment (acceptable) from factual fabrication (unacceptable) in mixed-mode outputs?

---
