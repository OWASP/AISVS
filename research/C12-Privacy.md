# C12: Privacy Protection & Personal Data Management

> **Source:** [`1.0/en/0x10-C12-Privacy.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C12-Privacy.md)
> **Requirements:** 26 | **Sections:** 6

## Control Objective

Maintain rigorous privacy assurances across the entire AI lifecycle (collection, training, inference, and incident response) so that personal data is only processed with clear consent, minimum necessary scope, provable erasure, and formal privacy guarantees.

> **2025-2026 Highlights:** AI privacy incidents jumped 56.4% in 2024, with nearly half involving customer PII. As of March 2026, at least 20 AI-app data breaches have been documented since January 2025 — including Chat & Ask AI (300M+ messages), McHire/McDonald's (64M job applicants), OmniGPT (34M conversation lines), Bondu AI Toy (50K children's transcripts), and the Sears Home Services chatbot breach (3.7M records). The EDPB's 2024 opinion set an extremely high bar for anonymization in LLMs, the 2025 CEF report on right to erasure found widespread compliance gaps across 764 controllers, and the Italian Garante fined OpenAI EUR 15M for lack of lawful basis. Machine unlearning faces a credibility crisis after ICLR 2025 relearning attacks showed approximate methods are fundamentally flawed. On the DP front, Google's VaultGemma demonstrated production-grade DP-SGD at LLM scale (epsilon <= 2.0), while DP reversal via LLM feedback emerged as a new attack vector. The EU AI Act high-risk requirements take effect August 2026, with the Digital Omnibus potentially delaying to December 2027.

---

## Section Pages

| Section | Title | Reqs | Page |
|---------|-------|:----:|------|
| C12.1 | Anonymization & Data Minimization | 4 | [C12-01-Anonymization-Data-Minimization](C12-01-Anonymization-Data-Minimization.md) |
| C12.2 | Right-to-be-Forgotten & Deletion Enforcement | 4 | [C12-02-Right-to-be-Forgotten-Deletion](C12-02-Right-to-be-Forgotten-Deletion.md) |
| C12.3 | Differential-Privacy Safeguards | 5 | [C12-03-Differential-Privacy-Safeguards](C12-03-Differential-Privacy-Safeguards.md) |
| C12.4 | Purpose-Limitation & Scope-Creep Protection | 5 | [C12-04-Purpose-Limitation-Scope-Creep](C12-04-Purpose-Limitation-Scope-Creep.md) |
| C12.5 | Consent Management & Lawful-Basis Tracking | 4 | [C12-05-Consent-Management-Lawful-Basis](C12-05-Consent-Management-Lawful-Basis.md) |
| C12.6 | Federated Learning with Privacy Controls | 4 | [C12-06-Federated-Learning-Privacy-Controls](C12-06-Federated-Learning-Privacy-Controls.md) |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Training data memorization leaking PII in model outputs — AI privacy/security incidents jumped 56.4% in 2024, with nearly half of all breaches involving customer PII
- Re-identification attacks on anonymized training data; EDPB (2024) ruled that LLMs "rarely achieve anonymization standards" and set an extremely high bar for considering model outputs anonymous
- Inability to truly 'forget' data already learned by a trained model — machine unlearning remains an active research area with exact, approximate, and certified approaches all having significant limitations
- Scope creep — data collected for one purpose being used for model training; 77% of employees paste company information into AI/LLM services (2026 survey), with 82% using personal accounts
- Cross-border data transfer violations in distributed training setups
- Shadow AI data leakage — breaches via unmanaged AI tools take an average of 247 days to detect, disproportionately affecting customer PII (65%) and intellectual property (40%)
- Model inversion and gradient inversion attacks using mathematically optimized queries to reverse-engineer training data from model outputs or gradient updates
- EchoLeak-style prompt injection attacks (CVE-2025-32711) that force AI assistants to exfiltrate sensitive business data to external URLs
- Differential privacy reversal via LLM feedback — adversaries analyze model confidence scores (logits, perplexity) to determine training set membership and reconstruct individual records from anonymized datasets (2025-2026 research)
- Approximate unlearning shown to be fundamentally flawed — CMU researchers (ICLR 2025) demonstrated "benign relearning attacks" that reverse gradient-ascent-based unlearning using small amounts of loosely related public data
- AI-app data breaches at alarming scale: as of March 2026, at least 20 documented AI-specific breaches since January 2025 including Chat & Ask AI (300M+ messages), McHire/McDonald's (64M applicants), OmniGPT (34M lines), and Bondu AI Toy (50K children's chat transcripts)
- Children's AI products emerging as a high-risk category — the Bondu AI Toy breach (January 2026) exposed 50K children's transcripts with names and birthdates via a vulnerability where any Gmail account granted admin access
- AI chatbot infrastructure as a systemic attack surface — the Sears Home Services breach (February 2026) exposed 3.7M chat logs and audio recordings from AI chatbots via unsecured databases with no password protection or encryption, demonstrating that customer-facing AI assistants create large, often unprotected PII repositories
- User-level versus example-level DP — Google research (2025-2026) showed that prior user-level DP implementations added orders of magnitude more noise than necessary; new ELS/ULS approaches significantly improve the privacy-utility tradeoff for LLM fine-tuning on sensitive datasets
- Brazil's ANPD targeting AI training data — enforcement actions against social media companies using personal data for AI training without proper consent, extending GDPR-style enforcement to Latin America

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2017 | Shokri et al. — Membership Inference Attacks Against Machine Learning Models | Foundational work showing ML models leak training set membership | [Paper](https://arxiv.org/abs/1610.05820) |
| 2019 | Zhu et al. — Deep Leakage from Gradients | Demonstrated pixel-accurate reconstruction of training images from shared gradients in federated learning | [Paper](https://arxiv.org/abs/1906.17744) |
| 2019 | Carlini et al. — The Secret Sharer: Evaluating and Testing Unintended Memorization | Canary-based methodology for measuring memorization in neural networks | [Paper](https://arxiv.org/abs/1802.08232) |
| 2021 | Carlini et al. — Extracting Training Data from Large Language Models | Showed GPT-2 memorizes and regurgitates PII, code, and other training data | [Paper](https://arxiv.org/abs/2012.07805) |
| 2021 | Bourtoule et al. — Machine Unlearning (SISA Training) | Proposed sharded training to enable efficient data removal without full retraining | [Paper](https://arxiv.org/abs/1912.03817) |
| 2022 | Italian DPA — Clearview AI fine (EUR 20M) | Fined for GDPR violations including failure to honor deletion requests for biometric data | [Decision](https://www.garanteprivacy.it/) |
| 2023 | Italian DPA — Temporary ban on ChatGPT | Raised questions about lawful basis for processing personal data in LLM training | [Coverage](https://www.bbc.com/news/technology-65139406) |
| 2024 | EDPB Opinion on AI Models and Personal Data | Set high bar for LLM anonymization; clarified legitimate interest requirements for AI training; ruled controllers deploying third-party LLMs must conduct comprehensive legitimate interest assessments | [EDPB](https://www.edpb.europa.eu/news/news/2024/edpb-opinion-ai-models-gdpr-principles-support-responsible-ai_en) |
| 2024 | EU AI Act enters force (August 1, 2024) | Prohibited AI practices effective February 2025; high-risk AI system requirements effective August 2026 (extended to December 2027 pending standards) | [EU AI Act](https://artificialintelligenceact.eu/) |
| 2024 | Italian Garante fines OpenAI EUR 15M | Violations of GDPR Articles 5(1)(a), 5(2), 6, 12, 13, 24, 25, 33 — lack of lawful basis, insufficient transparency, missing age verification, breach notification failures; six-month mandatory information campaign ordered | [Coverage](https://www.dataprotectionreport.com/2025/01/the-edpb-opinion-on-training-ai-models-using-personal-data-and-recent-garante-fine-lawful-deployment-of-llms/) |
| 2025 | EDPB Coordinated Enforcement Framework — Right to Erasure | EDPB selected right to erasure (Art. 17 GDPR) as the 2025 coordinated enforcement priority, as it is the most frequently exercised GDPR right and a top complaint category | [EDPB](https://www.edpb.europa.eu/news/news/2025/cef-2025-launch-coordinated-enforcement-right-erasure_en) |
| 2025 | ChatGPT prompt injection extracting training data | Security researchers demonstrated practical prompt injection attacks that extract training data snippets from ChatGPT, confirming the attack vector in production systems | [Coverage](https://www.protecto.ai/blog/ai-data-privacy-breaches-incidents-analysis/) |
| 2025 | EchoLeak vulnerability (CVE-2025-32711) in Microsoft 365 Copilot | Sophisticated character substitutions forced AI assistants to exfiltrate sensitive business data to external URLs | [Coverage](https://www.reco.ai/blog/ai-and-cloud-security-breaches-2025) |
| 2025 | NIST Privacy Framework 1.1 draft (April 2025) | New section on AI privacy risks covering training data exposure, algorithmic bias, and likeness rights infringement; recommended alongside AI RMF and CSF 2.0 | [NIST](https://www.nist.gov/privacy-framework) |
| 2025 | MUGen Workshop at ICML 2025 — Machine Unlearning for Generative AI | First major workshop bringing together AI safety, privacy, and policy experts to advance verifiable unlearning methods and standardized evaluation frameworks | [Workshop](https://mugenworkshop.github.io/) |
| 2025 | MMUnlearner — Multimodal Machine Unlearning | First framework addressing machine unlearning for multimodal large language models, extending unlearning beyond text-only models | [Paper](https://arxiv.org/abs/2502.11051) |
| 2025 | European Commission proposes GDPR + AI Act amendments | Targeted amendments in Q4 2025 to reshape cookie consent, expand SME exemptions, and clarify AI obligations under GDPR | [IAPP](https://iapp.org/news/a/european-commission-proposes-significant-reforms-to-gdpr-ai-act) |
| 2025 | Google releases VaultGemma — first production-grade DP-trained LLM | 1B-parameter Gemma 2 model trained with DP-SGD achieving epsilon <= 2.0, delta <= 1.1e-10; weights released on Hugging Face and Kaggle; derived new scaling laws for DP | [Google Research](https://research.google/blog/vaultgemma-the-worlds-most-capable-differentially-private-llm/) |
| 2025 | CMU — Relearning attacks break approximate unlearning (ICLR 2025) | Hu et al. demonstrated that benign relearning on small, loosely related public data reverses gradient-ascent-based unlearning — relearning on medical articles restored bioweapon knowledge in an unlearned LLM | [Paper](https://openreview.net/forum?id=fMNRYBvcQN) |
| 2025 | EUPG — Efficient Unlearning with Privacy Guarantees | Universitat Rovira i Virgili framework combining k-anonymity/DP pre-training with fine-tuning for utility; enables efficient deletion by reverting to privacy-protected checkpoint | [Coverage](https://www.helpnetsecurity.com/2025/07/17/machine-unlearning-privacy-upgrade/) |
| 2025 | McHire/McDonald's AI hiring platform breach | Default credentials (123456) and IDOR vulnerability exposed 64M job applicants' names, emails, and interview transcripts | [Coverage](https://blog.barrack.ai/every-ai-app-data-breach-2025-2026/) |
| 2026 | EDPB publishes 2025 CEF report on right to erasure | 32 DPAs examined 764 controllers; found seven critical compliance gaps including absent deletion procedures, backup erasure failures, and weak anonymization substitutes; nine DPAs launched formal investigations | [EDPB Report](https://www.edpb.europa.eu/our-work-tools/our-documents/other/coordinated-enforcement-action-implementation-right-erasure_en) |
| 2026 | EDPB/EDPS joint opinion on EU Digital Omnibus | Proposes delaying high-risk AI obligations from August 2026 to December 2027; EDPB/EDPS warn delays may harm fundamental rights | [Joint Opinion](https://www.edpb.europa.eu/system/files/2026-01/edpb_edps_jointopinion_202601_proposal_ai-omnibus_en.pdf) |
| 2026 | EDPB 2026 CEF — Transparency and information obligations | 2026 coordinated enforcement will focus on Articles 12-14 GDPR transparency requirements; expected to drive stricter penalties than prior years | [EDPB](https://www.edpb.europa.eu/news/news/2026/cef-2026-edpb-launches-coordinated-enforcement-action-transparency-and-information_en) |
| 2026 | Chat & Ask AI breach — 300M+ messages exposed | Firebase rule misconfiguration exposed 300M+ messages from 18-25M users including names, emails, and phone numbers | [Coverage](https://blog.barrack.ai/every-ai-app-data-breach-2025-2026/) |
| 2026 | Bondu AI Toy — 50K children's transcripts exposed | Any Gmail account granted admin access to 50K children's chat transcripts with names and birthdates | [Coverage](https://blog.barrack.ai/every-ai-app-data-breach-2025-2026/) |
| 2026 | OpenClaw AI agent security crisis | Over 21,000 exposed instances of an open-source AI agent; first major AI agent-specific privacy/security incident | [Coverage](https://purplesec.us/learn/ai-security-risks/) |
| 2026 | Sears Home Services chatbot breach — 3.7M records | Researcher Jeremiah Fowler discovered three unsecured databases (February 2026) containing 3.7M chat logs, audio recordings, and call transcriptions from AI chatbots "Samantha" and "KAIros"; PII included names, addresses, emails, phone numbers; databases were neither password-protected nor encrypted | [Coverage](https://cybernews.com/ai-news/ai-chatbot-data-leak-sears/) |
| 2026 | PrivCode — first DP synthesizer for code datasets (NDSS 2026) | Two-stage framework generating DP-compliant synthetic code via DP-SGD while preserving code structure; utility-boosting stage fine-tunes a larger LLM on the synthetic code | [Paper](https://arxiv.org/abs/2512.05459) |
| 2026 | Google — User-Level DP for LLM Fine-Tuning | Example-Level Sampling (ELS) and User-Level Sampling (ULS) approaches providing user-level DP guarantees with orders of magnitude less noise than prior methods; ULS generally superior for strong privacy or large compute budgets | [Paper](https://arxiv.org/abs/2407.07737) |
| 2026 | MUV Workshop at CVPR 2026 (Denver, June) | First CVPR workshop on Machine Unlearning for Vision — data-centric removal, parameter-centric strategies, and training-free steering for generative and recognition models | [Workshop](https://machine-unlearning-for-vision.github.io/) |
| 2026 | TPDP 2026 — Theory and Practice of Differential Privacy (Boston, June) | 12th annual DP workshop with special session on Differential Privacy for Health; selected papers published in Journal of Privacy and Confidentiality | [Workshop](https://tpdp.journalprivacyconfidentiality.org/2026/) |
| 2026 | WIPE-OUT 2026 Workshop at ECML-PKDD (Naples, September) | Second edition of the Machine Unlearning and Privacy Preservation workshop, building on ECML-PKDD 2025 with Google DeepMind keynotes | [Workshop](https://aiimlab.org/events/ECML_PKDD_2026_WIPE-OUT_2_Workshop_on_Machine_Unlearning_and_Privacy_Preservation.html) |

---

## Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C12.1 Anonymization & Data Minimization | Medium-High | PII detection tools are mature and production-ready. Automated k-anonymity auditing (ARX, sdcMicro) requires custom CI/CD integration. Synthetic data tools (SDV, Gretel, MOSTLY AI) are production-ready but privacy guarantees vary — the EDPB's 2024 opinion sets an extremely high bar for anonymization in AI contexts. |
| C12.2 Right-to-be-Forgotten & Deletion Enforcement | Low-Medium | Machine unlearning is advancing but faces a credibility crisis — ICLR 2025 relearning attacks (CMU) demonstrated that approximate methods merely suppress outputs rather than truly forgetting, meaning only exact unlearning (full retraining/SISA) and emerging certified methods are reliable. EUPG (2025) offers a promising hybrid approach. The EDPB's 2025 CEF report on right to erasure (published February 2026) found widespread compliance gaps across 764 controllers, with nine DPAs launching formal investigations. The research community is accelerating: three dedicated workshops in 2026 (MUV at CVPR, WIPE-OUT at ECML-PKDD, MUGen at ICML) now cover vision, NLP, and multimodal unlearning. |
| C12.3 Differential-Privacy Safeguards | Medium-High | Opacus, TF Privacy, and Google DP Library are production-quality for training. Google's VaultGemma (September 2025) is the first production-grade DP-trained LLM — 1B params, epsilon <= 2.0 — proving DP-SGD works at LLM scale, though with a utility gap vs. non-private models. DynamoEnhance (2024-2026) extends DP-SGD to >7B-parameter LLMs via multi-GPU DeepSpeed integration. Google's user-level DP fine-tuning (ELS/ULS) dramatically reduces noise overhead. PrivCode (NDSS 2026) demonstrates DP-SGD for code generation — a first for structured-output domains. OpenDP/SmartNoise and PipelineDP4j expand ecosystem options. NIST finalized formal guidelines in early 2025 standardizing DP evaluation. Budget tracking dashboards and RDP/zCDP/PLD accountants are maturing. Caution: DP reversal via LLM feedback (2025-2026 research) shows that confidence score analysis can defeat DP protections at the inference layer — API-level mitigations (hiding logits) are needed alongside training-time DP. |
| C12.4 Purpose-Limitation & Scope-Creep Protection | Low | No standardized tooling for purpose tagging or runtime purpose enforcement. Requires custom policy-as-code integration with MLOps platforms. The EU AI Act's high-risk classification (effective August 2026) will drive demand for purpose-limitation enforcement tooling. |
| C12.5 Consent Management & Lawful-Basis Tracking | Low-Medium | CMPs are mature for web consent but poorly integrated with ML pipelines. No standard for consent tokens in inference APIs. Italian Garante's EUR 15M OpenAI fine (2024) for lack of lawful basis underscores the compliance risk. European Commission's proposed GDPR amendments (Q4 2025) may reshape consent requirements for AI. |
| C12.6 Federated Learning with Privacy Controls | Medium-High | FL frameworks (Flower, TFF, NVIDIA FLARE) support local DP and secure aggregation. Google's distributed DP for federated learning is production-deployed (Gboard). Robust aggregation (Krum, Trimmed-Mean, FLTrust) is available but configuration is manual. Canary-based auditing and Federated Unlearning are research-stage but advancing. Apple Private Cloud Compute demonstrates production-grade privacy-preserving inference at scale. |

---

## Open Research Questions

- [ ] Is machine unlearning practical at scale, or is retraining the only reliable option? The ICML 2025 MUGen workshop is pushing toward standardized evaluation but no production-ready solution exists for foundation models. Federated Unlearning adds a distributed dimension to this challenge.
- [ ] What epsilon values for differential privacy provide meaningful protection without destroying model utility? Apple uses epsilon 2-8 for telemetry; the US Census used epsilon ~19.6 (controversial). NIST's 2025 formal guidelines standardize DP evaluation but do not prescribe specific thresholds.
- [ ] How should GDPR Article 17 (right to erasure) apply to foundation models? The EDPB's 2025 coordinated enforcement focus on right to erasure will produce enforcement decisions that may set precedent. The Italian Garante's EUR 15M OpenAI fine demonstrates willingness to enforce against AI companies.
- [ ] What constitutes adequate anonymization for AI training data? The EDPB's 2024 opinion sets an extremely high bar — LLMs "rarely achieve anonymization standards" and controllers must use "all means reasonably likely" to test for data extraction.
- [ ] How will the EU AI Act's high-risk classification (effective August 2026) interact with GDPR's privacy requirements for AI systems? The European Commission's proposed GDPR/AI Act amendments (Q4 2025) aim to clarify but may introduce new compliance complexity.
- [ ] Can certified machine unlearning (provable guarantees) scale to multimodal foundation models? MMUnlearner (2025) is a first step but the field is nascent. The ICLR 2025 relearning attack results make this more urgent — approximate methods are now considered fundamentally flawed.
- [ ] How should privacy-preserving inference architectures (Apple PCC model, confidential computing enclaves) be evaluated and certified for regulatory compliance?
- [ ] What is the appropriate standard for "shadow AI" privacy governance, given that 77% of employees leak corporate data into unmanaged AI tools?
- [ ] How should organizations defend against DP reversal via LLM feedback attacks? Hiding confidence scores is a practical first step but reduces model utility for downstream applications that depend on calibrated probabilities.
- [ ] Will the EU Digital Omnibus delay of high-risk AI obligations (potentially to December 2027) create a regulatory gap that harms privacy protections, as the EDPB/EDPS joint opinion warns?
- [ ] How should VaultGemma-style DP-SGD scaling laws inform epsilon threshold policies? The current "comparable to 5-year-old models" utility gap may be acceptable for some use cases but not others.
- [ ] Can user-level DP (Google's ELS/ULS) close the practical gap for fine-tuning on sensitive user data without major utility degradation? Early results are promising but limited to specific model families and data distributions.
- [ ] How should organizations secure AI chatbot infrastructure (chat logs, audio recordings, transcriptions) against the kind of mass exposure seen in the Sears breach? Current PII-at-rest protections are clearly inadequate for the volume of sensitive data AI assistants generate.
- [ ] Will GPU-accelerated FHE (~200x speedup over CPU) eventually make privacy-preserving LLM inference practical for production workloads, or are alternative approaches (confidential computing, PCC-style attestation) the more viable path?

---

## Related Standards & Cross-References

- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [General Data Protection Regulation (GDPR)](https://gdpr-info.eu/)
- [California Consumer Privacy Act (CCPA)](https://oag.ca.gov/privacy/ccpa)
- [EU Artificial Intelligence Act](https://artificialintelligenceact.eu/) — entered force August 2024; prohibited practices effective February 2025; high-risk AI requirements effective August 2026
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST Privacy Framework 1.1 (draft April 2025)](https://www.nist.gov/privacy-framework) — new section on AI privacy risks covering training data exposure, algorithmic bias, and likeness rights infringement
- [NIST Cybersecurity Framework Profile for AI (December 2025)](https://www.nist.gov/itl/ai-risk-management-framework) — integrates AI risk management into established security practices
- [EDPB Opinion on AI Models and Personal Data (2024)](https://www.edpb.europa.eu/news/news/2024/edpb-opinion-ai-models-gdpr-principles-support-responsible-ai_en) — anonymization standards, legitimate interest for AI training, unlawful processing consequences
- [EDPB 2025 Coordinated Enforcement — Right to Erasure](https://www.edpb.europa.eu/news/news/2025/cef-2025-launch-coordinated-enforcement-right-erasure_en)
- [ISO 27701](https://www.iso.org/standard/71670.html) — certifiable privacy information management system (PIMS) extension of ISO 27001; complementary to NIST PF for AI privacy governance
- [European Commission Proposed GDPR + AI Act Amendments (Q4 2025)](https://iapp.org/news/a/european-commission-proposes-significant-reforms-to-gdpr-ai-act)
- [EU Digital Omnibus — EDPB/EDPS Joint Opinion (January 2026)](https://www.edpb.europa.eu/system/files/2026-01/edpb_edps_jointopinion_202601_proposal_ai-omnibus_en.pdf) — proposes delaying high-risk AI obligations; EDPB/EDPS warn of fundamental rights impact
- [EDPB 2025 CEF Report — Right to Erasure](https://www.edpb.europa.eu/our-work-tools/our-documents/other/coordinated-enforcement-action-implementation-right-erasure_en) — 764 controllers examined, seven critical compliance gaps, nine DPAs launched investigations
- [EDPB 2026 CEF — Transparency and Information Obligations](https://www.edpb.europa.eu/news/news/2026/cef-2026-edpb-launches-coordinated-enforcement-action-transparency-and-information_en)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C03 Data Governance | Data lineage, classification, retention | C03 covers general data governance; C12 focuses on privacy-specific controls for personal data |
| C05 AI Model Security | Model extraction, membership inference | Model security controls in C05 complement privacy protections by defending against information extraction attacks |
| C09 AI Supply Chain | Third-party data provenance | Supply chain controls ensure privacy obligations flow to data suppliers and model providers |
| C14 Logging & Monitoring | Audit trails, immutable logging | C14 logging requirements support C12.2.4 deletion audit trails and C12.3 budget tracking |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

**2026-03-20 research update:** Enriched all 6 sections with 2024-2026 research including: EDPB 2024 opinion on AI models/personal data (anonymization bar, legitimate interest), Italian Garante EUR 15M OpenAI fine, EDPB 2025 coordinated enforcement on right to erasure, EU AI Act timeline (prohibited practices Feb 2025, high-risk Aug 2026), NIST Privacy Framework 1.1 AI section, machine unlearning advances (MUGen @ ICML 2025, MMUnlearner for multimodal LLMs, Federated Unlearning), expanded DP tooling (OpenDP, PipelineDP4j, Diffprivlib), Apple Private Cloud Compute, EchoLeak CVE-2025-32711, shadow AI statistics, and European Commission proposed GDPR/AI Act amendments (Q4 2025).

**2026-03-22 research update:** Major additions across threat landscape, tooling, and regulatory sections. New attack vectors: DP reversal via LLM feedback (confidence score analysis to reverse anonymization), ICLR 2025 relearning attacks showing approximate unlearning is fundamentally flawed (CMU — Hu et al.). New tools: Google VaultGemma (first production-grade DP-trained LLM, epsilon <= 2.0, September 2025), EUPG framework (hybrid k-anonymity/DP unlearning), FedRecovery (federated unlearning). Regulatory updates: EDPB 2025 CEF report on right to erasure (764 controllers, 7 critical gaps, 9 DPA investigations), EU Digital Omnibus proposing high-risk AI delay to December 2027 with EDPB/EDPS joint opinion warning of fundamental rights impact, EDPB 2026 CEF targeting transparency (Articles 12-14). New incidents: Chat & Ask AI (300M+ messages), McHire/McDonald's (64M applicants), Bondu AI Toy (50K children), and 17 more documented AI breaches since January 2025.

**2026-03-28 research update:** Expanded DP tooling coverage with DynamoEnhance (multi-GPU DP-SGD for >7B-param LLMs via DeepSpeed), Google's user-level DP fine-tuning (ELS/ULS — orders of magnitude noise reduction), and PrivCode (NDSS 2026, first DP synthesizer for code datasets). Added Sears Home Services chatbot breach (February 2026, 3.7M records via unsecured databases). New incidents table entries for MUV at CVPR 2026 (first vision unlearning workshop) and TPDP 2026 (DP for health special session). Updated privacy-preserving inference tooling with GPU-accelerated FHE (~200x speedup). Added Brazil ANPD enforcement against AI training data collection without consent. Three new open research questions on user-level DP, chatbot infrastructure security, and FHE viability.

**2026-03-29 structure update:** Split chapter into 6 per-section sub-pages, preserving all existing research. Hub page now links to individual section pages for easier navigation and independent updates.

---
