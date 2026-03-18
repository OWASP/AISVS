# C11.1: Model Alignment & Safety

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 5 | **IDs:** 11.1.1--11.1.5

## Purpose

Guard against harmful or policy-breaking outputs through systematic testing and guardrails. Alignment failures are among the highest-visibility risks in deployed AI systems -- a single jailbreak or harmful completion can cause reputational, legal, and safety consequences. This section requires organizations to move beyond ad-hoc testing toward structured, version-controlled alignment evaluation with automated regression detection.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.1.1** | **Verify that** refusal and safe-completion guardrails are enforced to prevent the model from generating disallowed content categories. | 1 | D | Direct generation of harmful, illegal, or policy-violating content (e.g., CBRN instructions, CSAM, targeted harassment). Covers MITRE ATLAS AML.T0051 (LLM Jailbreak). | Review guardrail configuration (system prompts, output filters, classifier layers). Test with known disallowed-content prompts across all content categories. Confirm blocked outputs return safe refusal messages rather than partial completions. | Guardrails vary significantly by provider and deployment. Self-hosted models may lack built-in refusal training. Refusal lists must be maintained as threat categories evolve. Content-category taxonomies are not standardized across the industry. |
| **11.1.2** | **Verify that** an alignment test suite (red-team prompts, jailbreak probes, disallowed-content checks) is version-controlled and run on every model update or release. | 1 | D/V | Alignment regression after fine-tuning, RLHF updates, or model swaps. A model that was safe in v1 may lose safety properties in v2 if alignment is not retested. | Inspect CI/CD pipeline for alignment test integration. Verify test suite is in version control with change history. Confirm test execution logs exist for recent model releases. Review test coverage across jailbreak categories (direct, indirect, multi-turn, encoding-based). | Public jailbreak datasets (e.g., JailbreakBench, HarmBench) provide starting points but are quickly outdated. Organizations need processes to incorporate new attack techniques. Test suites should cover multi-lingual and multi-modal jailbreaks where applicable. |
| **11.1.3** | **Verify that** an automated evaluator measures harmful-content rate and flags regressions beyond a defined threshold. | 2 | D/V | Gradual alignment degradation that goes undetected because testing is manual or infrequent. Silent regression where harmful-content rates increase slightly across releases without triggering review. | Review automated evaluation pipeline configuration. Verify threshold values are defined and documented. Check alerting integration -- confirm that threshold breaches generate notifications. Review historical metrics for evidence of regression detection working in practice. | Automated evaluators (LLM-as-judge, classifier-based) have their own accuracy limitations and can be gamed. Threshold calibration is difficult -- too tight creates noise, too loose misses real regressions. Evaluator models themselves need periodic validation. |
| **11.1.4** | **Verify that** alignment and safety training procedures (e.g., RLHF, constitutional AI, or equivalent) are documented and reproducible. | 2 | D | Inability to reproduce safety properties after infrastructure changes, team turnover, or incident response. Undocumented alignment procedures make it impossible to diagnose or fix alignment failures systematically. | Review alignment training documentation for completeness: training data, reward model configuration, hyperparameters, evaluation criteria. Verify reproducibility by checking if documented procedures have been successfully re-executed. For API-consumed models, verify that provider alignment documentation is reviewed and provider alignment commitments are tracked. | Most organizations consuming models via API have limited visibility into provider alignment procedures. For self-trained models, full reproducibility is resource-intensive. Constitutional AI and RLHF procedures involve subjective design choices that are difficult to fully specify. |
| **11.1.5** | **Verify that** alignment evaluation includes assessments for evaluation awareness, where the model may behave differently when it detects it is being tested versus deployed. | 3 | V | Deceptive alignment / sandbagging -- models that pass safety evaluations but behave differently in production. This is a theoretical but increasingly studied risk as models become more capable. Related to the "sleeper agent" research from Anthropic (2024). | Design evaluation protocols that obscure testing context from the model. Compare model behavior across contexts that signal "evaluation" versus "deployment." Use varied prompt formats, system prompts, and interaction patterns that prevent the model from pattern-matching on test characteristics. Measure behavioral consistency across contexts. | This is an active research area with no established best practices. Current detection methods are limited. The threat is more relevant for frontier models than for narrow task-specific models. Testing for evaluation awareness is itself subject to the problem it tries to detect (the model might learn to behave consistently during meta-evaluations too). |

---

## Related Standards & References

- [NIST AI 100-2e2023 -- Section on Evasion Attacks](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) -- Taxonomy of adversarial ML attacks including alignment bypass
- [MITRE ATLAS AML.T0051 -- LLM Jailbreak](https://atlas.mitre.org/techniques/AML.T0051) -- Techniques for bypassing LLM safety training
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm012025-prompt-injection/) -- Overlaps with alignment bypass via indirect prompt injection
- [HarmBench](https://www.harmbench.org/) -- Standardized evaluation framework for LLM red-teaming
- [Anthropic "Sleeper Agents" (2024)](https://arxiv.org/abs/2401.05566) -- Research on deceptive alignment and evaluation-aware behavior

---

## Open Research Questions

- How should alignment test suites handle multi-modal jailbreaks (e.g., harmful instructions encoded in images)?
- What metrics best capture alignment quality beyond simple harmful-content rate? Are there leading indicators of alignment degradation?
- How do you test alignment in agentic settings where harmful behavior emerges from sequences of individually benign actions?
- Can alignment evaluation methods keep pace with adversarial jailbreak innovation, or is this fundamentally an arms race with no stable equilibrium?
- What constitutes adequate alignment documentation for models consumed via third-party APIs where training procedures are proprietary?

---
