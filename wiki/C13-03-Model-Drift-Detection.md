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

## Implementation Guidance

### Drift Detection Tool Landscape (2025-2026)

The model monitoring ecosystem has consolidated around several mature platforms, each with distinct strengths:

- **Evidently AI** -- Open-source Python library with 20+ pre-built drift detection methods. Supports tabular, text, and embedding data. Generates interactive data drift reports, integrates with orchestration workflows via test suites, and provides live monitoring dashboards. Best suited for teams wanting flexible, self-hosted drift analysis with strong visualization.
- **NannyML** -- Specializes in performance estimation without ground truth labels and precise drift timing detection using the Confidence-Based Performance Estimation (CBPE) and Direct Loss Estimation (DLE) methods. Its meaningful alerting approach reduces false positives by focusing on performance-impacting drift rather than all statistical shifts. Primary limitation: strongest for tabular data, less mature for text/embedding modalities.
- **WhyLabs / whylogs** -- Enterprise-grade AI observability platform, open-sourced under Apache 2.0 in January 2025. Provides real-time data drift monitoring, anomaly detection, and profile-based logging. Lightweight profiling approach scales to high-volume production workloads.
- **Fiddler AI** -- Enterprise ML monitoring platform with explainability features, drift detection, and performance analytics. Focuses on model governance and compliance use cases.
- **Arize AI** -- Production ML observability with embedding drift visualization, performance tracing, and automated root cause analysis. Strong integration with LLM evaluation workflows.

PeerSpot's 2025 rankings place Evidently AI, NannyML, Fiddler AI, Arize AI, and H2O.ai as the top 5 model monitoring solutions.

### Statistical Methods for Drift Detection

Choosing the right statistical method depends on data type, sample size, and sensitivity requirements:

**For Numerical Features:**
- **Kolmogorov-Smirnov (KS) test** -- Non-parametric test comparing cumulative distributions. Good default for continuous features. Generates p-values indicating statistical significance.
- **Wasserstein Distance** -- Measures the "earth mover's distance" between distributions. Produces an interpretable drift magnitude score rather than a binary test result.
- **Population Stability Index (PSI)** -- Originally from credit scoring, widely used for production monitoring. Thresholds: PSI < 0.1 (no drift), 0.1-0.25 (moderate), > 0.25 (significant).
- **Jensen-Shannon Divergence** -- Symmetric, bounded (0-1) divergence measure suitable for comparing probability distributions.

**For Categorical Features:**
- **Chi-square test** -- Tests whether observed frequency distributions differ from expected.
- **PSI (binned)** -- Applied to category frequency distributions.

**For Text and Embeddings (LLM-relevant):**
- **Embedding centroid drift** -- Track the centroid of output embeddings over time; significant centroid shift indicates behavioral change.
- **Maximum Mean Discrepancy (MMD)** -- Kernel-based test for comparing embedding distributions, applicable to high-dimensional spaces.
- **Cosine similarity distributions** -- Monitor the distribution of cosine similarities between current outputs and a reference corpus.

An important caveat from current research: a statistically significant difference may not always be practically significant. Teams should analyze drift before taking action, distinguishing between legitimate distribution changes, data quality issues, and true model degradation.

### Drift Detection for LLM Systems

Traditional drift detection was designed for tabular ML models with well-defined feature spaces. Adapting to LLMs requires different approaches:

- **Output embedding drift:** Embed model outputs using a reference embedding model and monitor distribution shifts in embedding space. This captures semantic behavioral changes even when surface-level text varies.
- **Topic distribution drift:** Use topic modeling (BERTopic, LDA) on model outputs and track topic proportion changes over time.
- **Quality metric drift:** Track task-specific quality metrics (ROUGE, BLEU, exact match, human eval scores) as time series per 13.3.1, and apply changepoint detection (CUSUM, PELT algorithms) to identify sudden vs. gradual shifts per 13.3.5.
- **Hallucination rate tracking:** Per 13.3.3, monitor hallucination rates using retrieval-based fact checking, self-consistency checks (multiple generations compared), LLM-as-judge evaluation, or entailment-based verification. Track as continuous time-series metrics to detect sustained degradation trends.
- **Schema drift for structured AI inputs:** Per 13.3.4, for LLM applications "schema drift" applies to RAG document format changes, API request format changes, tool/function calling schema changes, and structured output format validation. Great Expectations and Pandera provide schema validation for structured data pipelines.

### Distinguishing Expected vs. Unexplained Drift

Requirement 13.3.5 addresses the security-critical distinction between gradual operational drift and sudden unexplained behavioral shifts. Implementation approaches:

- **Changepoint detection algorithms** (CUSUM, PELT) identify abrupt statistical changes in metric time series
- **Correlation analysis** cross-references drift events with known changes (deployments, data updates, config changes) to classify drift as expected vs. unexplained
- **Security escalation triggers:** Sudden drift indicators that warrant investigation include step-changes in output distribution, new output patterns unseen in training data, and behavioral changes uncorrelated with any known data or configuration change

---

## Related Standards & References

- **Evidently AI** -- Open-source ML monitoring with 20+ drift detection methods for tabular, text, and embedding data ([evidentlyai.com](https://www.evidentlyai.com/))
- **NannyML** -- Drift detection and performance estimation without ground truth ([nannyml.com](https://www.nannyml.com/))
- **WhyLabs / whylogs** -- Open-sourced (Apache 2.0, January 2025) AI observability platform for data drift and anomaly detection
- **Arize AI** -- Production ML observability with embedding drift visualization and automated root cause analysis
- **Fiddler AI** -- Enterprise ML monitoring with explainability and drift detection
- **Evidently AI Data Drift Guide** -- Comprehensive guide to drift detection methods and best practices ([evidentlyai.com/ml-in-production/data-drift](https://www.evidentlyai.com/ml-in-production/data-drift))
- **Open-Source Drift Detection Tools in Action** -- Comparative study of drift detection tools across use cases ([arxiv.org/abs/2404.18673](https://arxiv.org/abs/2404.18673))
- **NIST AI 100-1 Section 5.1** -- Discusses monitoring for AI system degradation
- **Google MLOps: Continuous Delivery for ML** -- Describes drift detection in production ML systems

---

## Open Research Questions

- How should drift detection be adapted for LLMs where output distributions are high-dimensional and non-stationary by design?
- What hallucination detection methods are reliable enough for production alerting without excessive false positives?
- Can embedding-space drift detection (monitoring shifts in output embedding distributions) serve as a general-purpose LLM drift indicator?
- How do you establish meaningful baselines for models that are expected to exhibit different behavior across different prompt types?
- What is the minimum sample size needed to detect statistically significant drift in LLM outputs?
- How do the open-source tools (Evidently, NannyML, WhyLabs) compare in detection sensitivity and false positive rates for text/embedding drift in LLM applications specifically?
- Can topic distribution monitoring reliably detect subtle capability degradation in general-purpose LLMs, or is it only effective for narrow-domain models?

---
