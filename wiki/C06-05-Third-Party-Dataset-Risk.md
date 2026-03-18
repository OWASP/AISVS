# C6.5 Third-Party Dataset Risk Assessment

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.5.1–6.5.5

## Purpose

Datasets are a uniquely dangerous supply-chain vector for AI systems. Unlike code dependencies where vulnerabilities are typically detectable, poisoned training data can embed subtle behavioral changes into a model that are extremely difficult to detect post-training. Third-party datasets also carry legal risks — copyrighted content, personally identifiable information, and biased distributions can create liability. This section ensures external datasets are assessed for poisoning, legal compliance, and bias before use, and monitored throughout their lifecycle.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **6.5.1** | **Verify that** external datasets undergo poisoning risk assessment (e.g., data fingerprinting, outlier detection). | 1 | D/V | **Training data poisoning.** An attacker injects crafted samples into a public dataset (e.g., web-scraped corpus, crowdsourced labels) to cause the trained model to exhibit attacker-chosen behaviors. Research shows as little as 0.1% poisoned data can compromise model behavior. (Carlini et al. 2023 "Poisoning Web-Scale Training Datasets"; MITRE ATLAS AML.T0020) | Verify that a data validation pipeline exists and runs on all external datasets before training. Check for: statistical outlier detection (isolation forests, z-score analysis), data fingerprinting to detect known poison patterns, label-consistency checks, and duplicate/near-duplicate detection. Tools: Great Expectations, Cleanlab, Dataperf benchmarks. | Poisoning detection is an active research area with no silver-bullet solution. Detection rates vary significantly by attack type (clean-label attacks are harder to detect than dirty-label). Organizations should layer multiple detection methods and accept residual risk. |
| **6.5.2** | **Verify that** disallowed content (e.g., copyrighted material, PII) is detected and removed via automated scrubbing prior to training. | 1 | D | **Legal liability from training on copyrighted or personal data.** Models trained on copyrighted content face litigation risk (NYT v. OpenAI, Getty v. Stability AI). Models trained on PII can memorize and regurgitate personal data, violating GDPR, CCPA, and similar regulations. | Confirm that a content-filtering pipeline runs before training, including: PII detection and redaction (Presidio, spaCy NER, regex patterns for SSN/email/phone), copyright/license detection for code datasets (ScanCode, REUSE), and NSFW/harmful content classifiers for image/text data. Verify that filtered records are logged for audit. | PII detection in unstructured text has significant false-negative rates, especially for non-English content or domain-specific identifiers. Copyright detection is legally ambiguous — "substantial similarity" is a legal judgment, not a technical measurement. Best-effort scrubbing is necessary but not sufficient for full legal protection. |
| **6.5.3** | **Verify that** origin, lineage, and license terms for datasets are captured in AI BOM entries. | 2 | V | **Undisclosed data provenance creating compliance blind spots.** Without documented lineage, organizations cannot respond to legal challenges, regulatory inquiries, or data subject access requests regarding their training data. | Audit AI BOM entries for dataset components. Each should include: source URL or provider, collection date, license identifier (SPDX format), data subjects description (if applicable), preprocessing steps applied, and any known limitations or biases documented by the provider. Cross-reference with dataset documentation (Datasheets for Datasets, Croissant metadata). | The "Datasheets for Datasets" framework (Gebru et al. 2021) provides a template, but adoption is inconsistent. Many popular datasets (especially web-scraped ones) lack adequate documentation. The Croissant metadata format (MLCommons) is gaining traction but still emerging. |
| **6.5.4** | **Verify that** bias metrics (e.g., demographic parity, equal opportunity) are calculated before dataset approval. | 2 | D | **Biased training data leading to discriminatory model outputs.** Datasets with demographic imbalances or label bias produce models that perform unequally across protected groups, creating legal risk (anti-discrimination law) and reputational harm. | Confirm that bias analysis is part of the dataset approval workflow. Check for: demographic distribution analysis across protected attributes (where available), label-distribution analysis by demographic group, comparison against benchmark fairness metrics (demographic parity, equalized odds, calibration). Tools: Fairlearn, AI Fairness 360 (AIF360), What-If Tool. | Bias measurement requires demographic metadata, which may not be available or appropriate to collect. Proxy-based bias detection is an alternative but less reliable. The appropriate fairness metric is domain- and context-dependent — there is no universal "correct" metric. |
| **6.5.5** | **Verify that** periodic monitoring detects drift or corruption in hosted datasets. | 3 | V | **Post-approval dataset modification or degradation.** Datasets hosted on third-party platforms can be modified after initial approval (either maliciously or accidentally). Web-scraped datasets drift naturally as source content changes. Stored datasets can suffer silent corruption. | Verify that a monitoring process exists for datasets that are hosted externally or re-fetched periodically. Checks should include: hash comparison against the approved version, statistical distribution comparison (population stability index, KL divergence), automated re-running of data quality checks on updated versions. Alert on deviations beyond defined thresholds. | For static downloaded datasets, integrity monitoring is straightforward (hash checks). For streaming or periodically re-scraped datasets, drift monitoring is substantially more complex and requires statistical infrastructure. Level 3 reflects the operational maturity required. |

---

## Related Standards & References

- [MITRE ATLAS AML.T0020 — Poison Training Data](https://atlas.mitre.org/techniques/AML.T0020)
- [Carlini et al. — Poisoning Web-Scale Training Datasets (2023)](https://arxiv.org/abs/2302.10149)
- [Gebru et al. — Datasheets for Datasets (2021)](https://arxiv.org/abs/1803.09010)
- [MLCommons Croissant Metadata Format](https://mlcommons.org/working-groups/data/croissant/)
- [Microsoft Presidio — PII Detection](https://microsoft.github.io/presidio/)
- [Cleanlab — Data-Centric AI](https://cleanlab.ai/)
- [IBM AI Fairness 360](https://aif360.mybluemix.net/)
- [Microsoft Fairlearn](https://fairlearn.org/)
- [Great Expectations — Data Validation](https://greatexpectations.io/)

---

## Open Research Questions

- How can poisoning detection scale to web-scale datasets (billions of examples) without prohibitive compute costs?
- What legal frameworks will emerge for dataset liability — is the dataset provider, the model trainer, or the deployer responsible for content issues?
- How should organizations handle "inherited bias" when fine-tuning on a clean dataset but starting from a base model trained on a biased one?
- Can data provenance be established retroactively for models already in production that were trained on insufficiently documented datasets?
