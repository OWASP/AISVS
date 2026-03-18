# C13.3: Model Drift Detection

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 5 (13.3.1 -- 13.3.5)

## Purpose

This section addresses the detection of changes in model behavior over time that may indicate degradation, data quality issues, or adversarial manipulation. Model drift encompasses both gradual shifts (concept drift, data drift) and sudden behavioral changes that could signal model compromise. For traditional ML models, drift detection is well-established; for LLMs and generative models, it remains an emerging discipline with different metrics and challenges.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **13.3.1** | Verify that the system tracks basic performance metrics such as accuracy, confidence scores, latency, and error rates across model versions and time periods. | 1 | D/V | Undetected model degradation leading to unreliable outputs; inability to identify when model quality drops below acceptable thresholds; lack of historical baseline for comparison. | Confirm metrics collection pipeline is active. Review dashboards for time-series tracking of accuracy, confidence, latency, error rates. Verify data is segmented by model version. Check historical data availability (minimum 30 days). | For LLMs, "accuracy" may need to be operationalized differently than for classification models -- consider task-specific metrics (e.g., ROUGE for summarization, exact match for QA). Confidence scores from LLMs (logprobs) may not be well-calibrated. |
| **13.3.2** | Verify that automated alerting triggers when performance metrics exceed predefined degradation thresholds or deviate significantly from baselines. | 2 | D/V | Silent model degradation going unnoticed for extended periods; gradual quality erosion that individually falls below notice but cumulatively is significant. | Review threshold configurations for each metric. Test alerting by injecting degraded performance signals. Verify alert routing and escalation. Confirm dynamic baseline recalculation procedures. | Static thresholds are a starting point; adaptive thresholds (e.g., based on rolling standard deviations) reduce false positives from normal variance. Consider separate thresholds for different data segments or user populations. |
| **13.3.3** | Verify that hallucination detection monitors identify and flag instances when model outputs contain factually incorrect, inconsistent, or fabricated information, and that hallucination rates are tracked as continuous time-series metrics to enable trend analysis and detection of sustained model degradation. | 2 | D/V | Increasing hallucination rates indicating model degradation or data quality issues; user trust erosion from factually incorrect outputs; liability from fabricated information in high-stakes applications. | Review hallucination detection pipeline. Test with known hallucination-inducing prompts. Verify time-series tracking of hallucination rates. Confirm trend alerting is configured. Evaluate detection method accuracy (precision/recall). | Hallucination detection methods: (1) retrieval-based fact checking against knowledge bases, (2) self-consistency checks (multiple generations compared), (3) LLM-as-judge evaluation, (4) entailment-based verification. Each has trade-offs in accuracy, latency, and cost. No method achieves reliable detection across all hallucination types. |
| **13.3.4** | Verify that schema drift in incoming data (unexpected field additions, removals, type changes, or format variations) is detected and triggers alerting. | 2 | D/V | Breaking changes in upstream data sources degrading model inputs silently; data pipeline failures producing malformed inputs; adversarial manipulation of data schemas to influence model behavior. | Introduce schema changes to input data (add/remove fields, change types). Verify detection and alerting triggers. Review schema validation rules. Confirm compatibility with both structured data and semi-structured (JSON) inputs. | Most relevant for ML pipelines with structured feature inputs. For LLM applications, "schema drift" applies to: RAG document format changes, API request format changes, tool/function calling schema changes, and structured output format validation. Great Expectations and Pandera provide schema validation for structured data. |
| **13.3.5** | Verify that sudden unexplained behavioral shifts are distinguished from gradual expected operational drift, with a security escalation path defined for unexplained sudden drift. | 3 | V | Model poisoning or backdoor activation causing abrupt behavioral changes; unauthorized model replacement (model swapping attacks); compromised fine-tuning pipelines injecting malicious behavior. | Review the process for classifying drift as expected vs. unexplained. Test the escalation path by simulating sudden behavioral changes. Verify that security investigation procedures exist for unexplained drift. Confirm rollback capabilities. | This requirement bridges monitoring and security. Sudden drift indicators: (1) step-change in output distribution, (2) new output patterns not seen in training, (3) behavioral changes uncorrelated with known data/config changes. Changepoint detection algorithms (CUSUM, PELT) are relevant statistical methods. |

---

## Related Standards & References

- **Evidently AI** -- Open-source ML monitoring with drift detection for tabular and text data ([evidentlyai.com](https://www.evidentlyai.com/))
- **NannyML** -- Drift detection and performance estimation without ground truth ([nannyml.com](https://www.nannyml.com/))
- **WhyLabs / whylogs** -- Data logging and drift monitoring for ML pipelines
- **NIST AI 100-1 Section 5.1** -- Discusses monitoring for AI system degradation
- **Google MLOps: Continuous Delivery for ML** -- Describes drift detection in production ML systems

---

## Open Research Questions

- How should drift detection be adapted for LLMs where output distributions are high-dimensional and non-stationary by design?
- What hallucination detection methods are reliable enough for production alerting without excessive false positives?
- Can embedding-space drift detection (monitoring shifts in output embedding distributions) serve as a general-purpose LLM drift indicator?
- How do you establish meaningful baselines for models that are expected to exhibit different behavior across different prompt types?
- What is the minimum sample size needed to detect statistically significant drift in LLM outputs?

---
