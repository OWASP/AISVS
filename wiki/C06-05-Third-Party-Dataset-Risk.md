# C6.5 Third-Party Dataset Risk Assessment

> **Parent:** [C06: Supply Chain Security](C06-Supply-Chain.md) | **Requirements:** 5 | **IDs:** 6.5.1–6.5.5

## Purpose

Datasets are a uniquely dangerous supply-chain vector for AI systems. Unlike code dependencies where vulnerabilities are typically detectable, poisoned training data can embed subtle behavioral changes into a model that are extremely difficult to detect post-training. Third-party datasets also carry legal risks — copyrighted content, personally identifiable information, and biased distributions can create liability. This section ensures external datasets are assessed for poisoning, legal compliance, and bias before use, and monitored throughout their lifecycle.

---

## 2025-2026 Landscape Update

### Web-Scale Dataset Poisoning is Practical and Cheap

Carlini et al. (2023) demonstrated two concrete attack methods against web-scale datasets that remain relevant and under-mitigated:

- **Split-view poisoning**: Many distributed datasets (LAION-400M, COYO-700M, Conceptual 12M) store URLs rather than actual data. Domain names in these URL lists continuously expire. An attacker can purchase expired domains for as little as $10 each and serve malicious content to any future downloader. The researchers found that all ten tested datasets contained between 0.14% and 6.48% purchasable expired domains. Poisoning 0.01% of LAION-400M or COYO-700M costs approximately $60 USD. Critically, nearly all third-party download tools for these datasets ignore the hash checksums that were provided.

- **Frontrunning poisoning**: For crowdsourced datasets derived from Wikipedia snapshots, attackers can predict snapshot timing to the minute and inject malicious edits that are captured in the dataset but quickly reverted. This could theoretically poison approximately 6.5% of English Wikipedia-derived documents, with multilingual Wikipedias showing vulnerability rates up to 25.3%.

Even poisoning rates as low as 0.00025% of a dataset can achieve 60% success in targeted misclassification attacks. These findings mean that any organization using URL-based or web-scraped datasets without hash verification is accepting a materially exploitable risk.

### LAION Dataset Controversies and Remediation

The LAION-5B dataset saga illustrates the full spectrum of third-party dataset risks:

- **CSAM discovery (December 2023)**: The Stanford Internet Observatory found 3,226 suspected instances of links to child sexual abuse material in LAION-5B, with 1,008 externally validated. LAION temporarily removed LAION-5B and LAION-400M.
- **Sensitive personal data**: An investigation by Bayerischer Rundfunk found that LAION datasets contain large amounts of private and sensitive data harvested from public websites without consent.
- **Hateful and harmful content**: Research (Birhane et al. 2023) documented widespread instances of rape, pornography, malign stereotypes, racist and ethnic slurs, and other extremely problematic content within LAION-5B.
- **Re-LAION-5B (August 2024)**: LAION released a cleaned version, removing 2,236 links after matching against known-abuse lists. However, the fundamental architecture of URL-based datasets means that the content behind remaining links continues to change over time.

The LAION case is instructive: even well-intentioned, widely-used datasets can harbor serious content and legal risks that are only discovered years after initial release and widespread adoption.

### Legal Landscape for Training Data

The legal environment for training data has become more complex:

- **NYT v. OpenAI** and **Getty v. Stability AI** established that training on copyrighted content carries real litigation risk.
- **LAION v. Kneschke (2024)**: A German court ruled that building public datasets is covered by the text and data mining (TDM) exception under EU copyright law, providing some legal cover for research datasets, but the ruling's applicability to commercial use remains contested.
- **GDPR and CCPA enforcement**: Models that memorize and regurgitate PII from training data face regulatory action. The EU AI Act imposes additional transparency requirements for training data documentation.

### Dataset Vetting Tools: Current State

The tooling landscape for dataset security has matured but remains incomplete:

- **Cleanlab**: Identifies label errors, outliers, and near-duplicates in datasets. Useful for detecting dirty-label poisoning but limited against clean-label attacks.
- **Great Expectations**: General-purpose data validation framework that can enforce schema, statistical, and distribution constraints on incoming datasets.
- **Microsoft Presidio**: PII detection and redaction for unstructured text. Supports multiple languages but has significant false-negative rates for non-English content and domain-specific identifiers.
- **Croissant (MLCommons)**: Metadata format for ML datasets gaining adoption, providing standardized fields for provenance, license, and content description. Complementary to the "Datasheets for Datasets" framework.
- **ScanCode / REUSE**: License detection for code datasets, important for detecting copyleft or restricted-license code in training corpora.
- **Data Provenance Initiative**: Academic effort to catalog and document the provenance of major ML training datasets, providing a reference for organizations performing due diligence.

### Data Supply Chain Security

Organizations should treat datasets with the same supply-chain rigor applied to code dependencies:

1. **Hash-verify on download**: Always verify dataset integrity using cryptographic hashes. Do not rely on URL stability.
2. **Mirror locally**: Download and snapshot datasets to internal storage rather than re-fetching from external URLs at training time.
3. **Version-pin datasets**: Reference specific dataset versions or commits (e.g., Hugging Face dataset revisions) rather than "latest."
4. **Scan before training**: Run automated content scanning (PII, CSAM, copyright, poisoning indicators) before any training use.
5. **Document in AI BOM**: Capture provenance, license, preprocessing steps, and known limitations for every dataset.

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
- [Carlini et al. — Poisoning Web-Scale Training Datasets is Practical (2023)](https://arxiv.org/abs/2302.10149)
- [Gebru et al. — Datasheets for Datasets (2021)](https://arxiv.org/abs/1803.09010)
- [MLCommons Croissant Metadata Format](https://mlcommons.org/working-groups/data/croissant/)
- [Microsoft Presidio — PII Detection](https://microsoft.github.io/presidio/)
- [Cleanlab — Data-Centric AI](https://cleanlab.ai/)
- [IBM AI Fairness 360](https://aif360.mybluemix.net/)
- [Microsoft Fairlearn](https://fairlearn.org/)
- [Great Expectations — Data Validation](https://greatexpectations.io/)
- [LAION Re-LAION-5B — Transparent Iteration with Safety Fixes](https://laion.ai/blog/relaion-5b/)
- [Stanford Internet Observatory — CSAM in LAION-5B](https://incidentdatabase.ai/reports/3555/)
- [Birhane et al. — Into the LAION's Den: Investigating Hate in Multimodal Datasets (2023)](https://arxiv.org/abs/2311.03449)
- [LAION v. Kneschke — TDM Exception Ruling (2024)](https://communia-association.org/2024/10/11/laion-vs-kneschke-building-public-datasets-is-covered-by-the-tdm-exception/)
- [Data Provenance Initiative](https://dataprovenance.org/)

---

## Open Research Questions

- How can poisoning detection scale to web-scale datasets (billions of examples) without prohibitive compute costs?
- What legal frameworks will emerge for dataset liability — is the dataset provider, the model trainer, or the deployer responsible for content issues?
- How should organizations handle "inherited bias" when fine-tuning on a clean dataset but starting from a base model trained on a biased one?
- Can data provenance be established retroactively for models already in production that were trained on insufficiently documented datasets?
- Given that split-view poisoning costs as little as $60 for web-scale datasets, should URL-based dataset distribution be considered fundamentally insecure? What alternative distribution models (content-addressed storage, IPFS-pinned datasets) could replace it?
- How should the LAION v. Kneschke TDM exception ruling affect organizational risk assessments for training on web-scraped data in EU jurisdictions?
- What automated tooling is needed to continuously monitor the domain registration status of URLs within active training datasets?
