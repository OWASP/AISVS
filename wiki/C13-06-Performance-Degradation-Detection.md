# C13.6: AI Performance Degradation Detection

> **Parent:** [C13 Monitoring, Logging & Anomaly Detection](C13-Monitoring-and-Logging)
> **Requirements:** 6 (13.6.1 -- 13.6.6)

## Purpose

This section focuses on detecting and responding to declining model quality over time. While C13.3 covers drift detection (shifts in data or behavior distribution), C13.6 addresses the downstream impact: measurable degradation in model accuracy, reliability, and fitness for purpose. This section is most directly applicable to supervised ML models with measurable performance metrics, but also applies to LLM-based systems where quality can be assessed through evaluation benchmarks or human feedback loops.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **13.6.1** | Verify that model accuracy, precision, recall, and F1 scores are continuously monitored and compared against baseline thresholds. | 1 | D/V | Undetected degradation in model decision quality; models making increasingly incorrect predictions without operator awareness; compliance failures from models operating below documented accuracy levels. | Verify metrics collection pipeline with ground truth labels. Confirm baseline thresholds are documented and enforced. Review dashboards for continuous monitoring. Test alerting by simulating degraded performance. Check metric calculation frequency and sample sizes. | Requires ground truth labels, which may be delayed (e.g., fraud labels arrive weeks after prediction). For LLMs, proxy metrics may be needed: human evaluation scores, automated evaluation (LLM-as-judge), task completion rates, or user satisfaction signals. NannyML's CBPE (Confidence-Based Performance Estimation) can estimate performance without immediate ground truth. |
| **13.6.2** | Verify that data drift detection monitors input distribution changes that may impact model performance, using statistically validated methods appropriate to the data type. | 1 | D/V | Model serving on out-of-distribution data where predictions are unreliable; upstream data pipeline changes silently altering input characteristics; adversarial data poisoning shifting input distributions. | Review statistical methods used for drift detection. Verify they are appropriate for the data types (e.g., KS test for continuous, chi-squared for categorical, embedding distance for text). Confirm monitoring window sizes and significance thresholds. Test by introducing known distribution shifts. | Statistical drift detection methods by data type: **Numerical** -- Kolmogorov-Smirnov test, Population Stability Index (PSI), Wasserstein distance. **Categorical** -- Chi-squared test, Jensen-Shannon divergence. **Text/Embeddings** -- Maximum Mean Discrepancy (MMD), cosine similarity distribution shifts. **Images** -- FID (Frechet Inception Distance). Choose significance levels carefully to avoid alert fatigue. |
| **13.6.3** | Verify that concept drift detection identifies changes in the relationship between inputs and expected outputs. | 2 | D/V | Models that are accurate on individual features but wrong on outcomes because the underlying relationship has changed (e.g., a fraud model trained before a new payment method was introduced). | Verify concept drift monitoring methodology. Confirm it measures changes in P(Y|X), not just P(X). Review detection approach (e.g., performance-based monitoring with ground truth, or model-based concept drift detection). Test with synthetic concept drift scenarios. | Concept drift is fundamentally harder to detect than data drift because it requires ground truth labels. Approaches: (1) Direct monitoring of performance metrics when labels are available; (2) ADWIN or Page-Hinkley tests on error rates; (3) DDM (Drift Detection Method) tracking model error rates over time. For LLMs, concept drift may manifest as changing user expectations or task definitions. |
| **13.6.4** | Verify that performance degradation triggers automated alerts and initiates model retraining or replacement workflows. | 2 | D/V | Prolonged operation of degraded models due to manual-only remediation processes; slow human response to degradation events during off-hours; cascading degradation in downstream systems dependent on model outputs. | Verify automated workflow triggers are configured for degradation events. Test end-to-end: inject degradation, verify alert, confirm workflow initiation (retraining pipeline trigger or model swap). Review fallback behavior during retraining. | Automated retraining triggered by drift/degradation is core MLOps but has security implications: (1) adversaries could manipulate drift signals to trigger retraining on poisoned data, (2) automated retraining pipelines must be secured (C03 Model Lifecycle), (3) model validation gates must exist before automated deployment of retrained models. |
| **13.6.5** | Verify that degradation root cause analysis correlates performance drops with data changes, infrastructure issues, or external factors. | 3 | V | Incorrect remediation due to misidentified root causes; repeated degradation incidents from unresolved underlying issues; wasted retraining effort when the cause is infrastructure, not model quality. | Review root cause analysis capabilities and tooling. Verify correlation analysis between performance metrics and: data source changes, infrastructure events, model updates, external events. Review past degradation incidents for quality of root cause attribution. | Root cause correlation requires combining multiple data sources: model metrics, data pipeline logs, infrastructure telemetry, deployment events, and external data source change logs. This is a verification-focused (V role) requirement because the analysis requires broad system knowledge. Few tools automate this correlation for AI systems. |
| **13.6.6** | Verify that baseline performance profiles are formally documented and version-controlled, reviewed at an appropriate frequency. | 2 | D/V | Drifting baselines that gradually normalize degraded performance; inability to compare current performance against original deployment standards; lack of accountability for performance thresholds. | Verify baseline documents exist and are version-controlled. Confirm they include: metrics, thresholds, measurement methodology, data characteristics, and review date. Check review cadence. Verify baselines are updated when models are retrained or replaced (with justification for threshold changes). | Baselines should be established during model validation (C03) and maintained as living documents. Each model version should have its own baseline profile. Review triggers: scheduled (quarterly minimum), event-driven (after retraining, after significant data changes), and performance-driven (after sustained metric changes). |

---

## Implementation Guidance

### Canary Testing and Phased Model Rollouts (2024--2026 Practices)

Canary testing has become a standard practice for detecting performance degradation before it affects the full user base. The methodology involves routing a small percentage of production traffic to a new model version while the majority remains on the stable version:

1. **Phased traffic allocation**: Start with 5% of traffic to the canary model, then incrementally increase to 10%, 25%, and eventually 100% as confidence builds. Traffic splitting is typically implemented via weighted load balancing at the API gateway layer (e.g., Portkey AI Gateway, custom routing in Kubernetes Ingress).
2. **Metrics monitored during canary**: Response accuracy, latency/response times, cost per request, hallucination rates, user feedback signals, and error rates. If any KPI degrades beyond acceptable thresholds, traffic is automatically redirected back to the previous model version.
3. **Automated rollback**: Detection systems continuously compare canary metrics against the stable version. When degradation is detected, automated rollback redirects all traffic to the previous version without manual intervention. This requires pre-configured rollback triggers with clearly defined threshold values.
4. **LLM-specific canary considerations**: For LLM applications, canary metrics must include semantic quality measures (not just latency and error rates). Automated evaluation using LLM-as-judge, task completion rates, and structured output validation scores are used alongside traditional SLIs.

### A/B Testing for Model Comparison

A/B testing differs from canary testing in purpose: while canary testing validates a new version for safety, A/B testing compares two or more model versions against specific business metrics over a defined duration with statistical analysis to select a winner. Key considerations:

- Traffic is typically split evenly (50/50) or in controlled ratios for a predetermined duration.
- Results require statistical significance testing (e.g., chi-squared tests for categorical outcomes, t-tests for continuous metrics) before making deployment decisions.
- A/B testing can serve as a degradation detection mechanism: running the current production model against a known baseline in continuous A/B tests reveals gradual performance drift.

### SLA Monitoring with Prometheus and Automated SLI Checks

Modern AI SLA monitoring uses automated queries against metrics backends (typically Prometheus or Datadog) to continuously check service-level indicators:

- **Latency SLIs**: P50, P95, P99 inference latency tracked per model endpoint, with alerting when SLA thresholds are breached.
- **Availability SLIs**: Request success rates tracked with automatic escalation when error rates exceed defined budgets.
- **Quality SLIs**: Custom metrics such as average prediction confidence scores, hallucination rates, and safety filter trigger rates are queried on regular intervals to detect model-specific regressions.
- **Cost SLIs**: Per-request token consumption and cost tracking to detect unexpected cost increases that may indicate prompt injection attacks or model misbehavior inflating output length.

### Data Drift Detection Methods by Data Type

Statistical drift detection should use methods appropriate to the data type being monitored:

| Data Type | Recommended Methods | Notes |
|-----------|-------------------|-------|
| Numerical/continuous | Kolmogorov-Smirnov test, Population Stability Index (PSI), Wasserstein distance | PSI > 0.2 typically indicates significant drift |
| Categorical | Chi-squared test, Jensen-Shannon divergence | Choose significance levels carefully to avoid alert fatigue |
| Text/Embeddings | Maximum Mean Discrepancy (MMD), cosine similarity distribution shifts | Requires embedding model consistency across measurement periods |
| Images | Frechet Inception Distance (FID) | Computationally expensive; consider sampling strategies |

### Concept Drift Detection

Concept drift (changes in P(Y|X), not just P(X)) is fundamentally harder to detect because it requires ground truth labels. Practical approaches:

- **ADWIN (Adaptive Windowing)**: Automatically adjusts window size to detect changes in error rates.
- **Page-Hinkley test**: Sequential analysis method for detecting changes in the average of a Gaussian signal -- applicable to streaming error rate monitoring.
- **DDM (Drift Detection Method)**: Tracks model error rates over time and triggers alerts when error rate increases exceed statistical thresholds.
- **For LLMs**: Concept drift may manifest as changing user expectations or task definitions. Proxy detection uses periodic evaluation against curated benchmark sets with known-good answers, tracking score trends over time.

### Adoption Reality Check

As of 2025, only approximately 16% of organizations have fully implemented AI-specific monitoring and testing processes, highlighting a significant gap between recognized best practices and actual deployment maturity. This suggests that many AI systems in production operate without adequate degradation detection, making the Level 1 requirements in this section especially important as baseline expectations.

---

## Related Standards & References

- **Evidently AI** -- Open-source monitoring with data drift, concept drift, and performance tracking ([evidentlyai.com](https://www.evidentlyai.com/))
- **NannyML** -- Performance estimation without ground truth using CBPE and DLE methods ([nannyml.com](https://www.nannyml.com/))
- **Portkey AI Gateway** -- Provides canary testing infrastructure with weighted load balancing and observability for LLM applications ([portkey.ai](https://portkey.ai/blog/canary-testing-for-llm-apps/))
- **Google Monitoring ML Models in Production** -- Describes data and concept drift monitoring patterns
- **NIST AI 100-1 Section MAP 2.3** -- AI system performance metrics and monitoring
- **MLflow Model Registry** -- Supports baseline versioning and model lifecycle management

---

## Open Research Questions

- How should performance degradation be measured for generative AI models where there is no single "correct" output? LLM-as-judge approaches show promise but introduce their own drift risks (the judge model itself may degrade).
- What is the appropriate balance between automated retraining triggers and human review gates? Adversaries could potentially manipulate drift signals to trigger retraining on poisoned data (see 13.6.4 security implications).
- Can synthetic data be used to continuously evaluate LLM quality as a proxy for real-world performance? Early results from canary testing frameworks suggest curated evaluation sets can serve as effective regression tests.
- How should performance baselines account for legitimate changes in user behavior and task distribution? Static baselines become stale; adaptive baselines risk normalizing gradual degradation.
- What minimum sample sizes are required for statistically significant degradation detection across different model types? This varies significantly between high-volume classification models and low-volume generative AI use cases.
- How should canary testing and A/B testing be secured against adversarial manipulation? An attacker who can identify canary traffic (e.g., through timing or routing analysis) could selectively target or avoid the canary model.

---
