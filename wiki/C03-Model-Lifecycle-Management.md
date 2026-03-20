# C03: Model Lifecycle Management & Change Control

> **Source:** [`1.0/en/0x10-C03-Model-Lifecycle-Management.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C03-Model-Lifecycle-Management.md)
> **Requirements:** 23 | **Sections:** 6

## Control Objective

AI systems must implement change control processes that prevent unauthorized or unsafe model modifications from reaching production. Only authorized, validated models reach production by employing controlled processes that maintain integrity, traceability, and recoverability.

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Model tampering during training or fine-tuning pipeline
- Unauthorized model deployment bypassing validation gates
- Model supply chain attacks (compromised checkpoints on Hugging Face, etc.) -- 6.5x increase in malicious models in 2024 (JFrog); 352K unsafe issues across 51.7K models (Protect AI, 2025)
- Model namespace reuse/hijacking: attackers reclaim deleted namespaces to distribute malicious models via trusted names (Unit 42, 2025)
- Picklescan evasion via nullifAI techniques, bypassing format-based defenses (ReversingLabs, 2025)
- Stale or vulnerable models remaining in production without rotation -- 91% of ML models degrade over time (MIT)
- Silent hosted model updates changing behavior without consumer awareness -- prompts degrade after provider updates
- Provider model deprecations with limited notice windows (60 days for Azure GA models; varies widely across providers)
- Incomplete decommissioning leaving model artifacts accessible to attackers
- Weaponized open-source AI repositories (NullBulge campaign, 2024: ransomware delivery via Hugging Face/GitHub)

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2025-02 | Model Namespace Reuse attack (Palo Alto Unit 42) | Attackers reclaim deleted Hugging Face namespaces to upload malicious models; demonstrated RCE on Google Vertex AI Model Garden and Microsoft Azure AI Foundry | [Unit 42](https://unit42.paloaltonetworks.com/model-namespace-reuse/) |
| 2025-01 | nullifAI evasion of Picklescan (ReversingLabs) | Malicious models on Hugging Face bypassed Picklescan detection using novel evasion techniques; removed within 24 hours | [ReversingLabs](https://www.reversinglabs.com/blog/ai-and-transparency-how-ml-model-creators-can-protect-against-supply-chain-attacks) |
| 2025 | Protect AI scan: 352K unsafe model issues | Scan of 4.47M model versions found 352,000 unsafe or suspicious issues across 51,700 models on Hugging Face | [Trend Micro](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/exploiting-trust-in-open-source-ai-the-hidden-supply-chain-risk-no-one-is-watching) |
| 2025 | Sonatype: 454,600 new malicious packages (cumulative 1.23M) | Growing supply chain malware across npm, PyPI, Maven, NuGet, and Hugging Face | [Sonatype 2026 Report](https://www.sonatype.com/state-of-the-software-supply-chain/2026/open-source-malware) |
| 2024 | NullBulge campaign: weaponized HF/GitHub repos | Threat actor distributed malicious code via Hugging Face and GitHub targeting AI tools; exfiltrated data via Discord webhooks, delivered LockBit ransomware | [Hacker News](https://thehackernews.com/2025/11/cisos-expert-guide-to-ai-supply-chain.html) |
| 2024-02 | Hugging Face malicious pickle-based models | Supply chain attack via unsigned model artifacts on public hub; JFrog documented 6.5x increase in malicious models in 2024 | [JFrog blog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/) |
| 2024-02 | Hugging Face conversion service vulnerability | Attacker could run arbitrary code via model conversion, hijacking widely used models without indication to users | [The Hacker News](https://thehackernews.com/2024/02/new-hugging-face-vulnerability-exposes.html) |
| 2023-04 | PyTorch nightly supply chain compromise | Malicious dependency injected into torchtriton package via PyPI | [PyTorch advisory](https://pytorch.org/blog/compromised-nightly-dependency/) |
| 2023 | ShadowRay (Anyscale Ray) CVE-2023-48022 | Unauthenticated access to ML training infrastructure and model artifacts | [Oligo Security](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild) |

---

## C3.1 Model Authorization & Integrity

Only authorized models with verified integrity reach production environments.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.1.1** | Verify that a model registry maintains an inventory of all deployed model artifacts and produces a machine-readable Model/AI Bill of Materials (MBOM/AIBOM) (e.g., SPDX or CycloneDX). | 1 | V | Untracked model deployments; inability to audit what is running in production; shadow AI. | Inspect model registry (MLflow, Vertex AI Model Registry, SageMaker Model Registry). Confirm MBOM/AIBOM export exists in SPDX or CycloneDX format. Validate completeness against deployed endpoints. | CycloneDX ML BOM support is maturing (added in v1.5); CycloneDX supports integrity verification via hash values and enveloped signing (JSF/XMLsig). SPDX AI/ML profile still evolving. Syft can generate SBOMs in both formats from container images. NIST AI RMF (2025) expects organizations to maintain AI inventories describing model purpose, data sources, risk exposure, and deployment environments. EU AI Act GPAI obligations (effective Aug 2025) require technical documentation and lifecycle oversight. *(Updated 2026-03)* |
| **3.1.2** | Verify that all model artifacts (weights, configurations, tokenizers, base models, fine-tunes, adapters, and safety/policy models) are cryptographically signed by authorized entities and verified at deployment admission (and on load), blocking any unsigned or tampered artifact. | 1 | D/V | Supply chain tampering; loading of backdoored or poisoned model weights; man-in-the-middle substitution during artifact transfer. | Verify signing workflow exists (e.g., Sigstore cosign, in-toto attestations, or GPG). Test by deploying an unsigned or modified artifact and confirm it is rejected. Inspect admission controller or model loader code for signature verification logic. | Sigstore model signing is available but adoption is early; ReversingLabs (2025) advocates extending Sigstore to ML models to prevent hub-level swaps. Hugging Face added safetensors format to mitigate pickle-based attacks but signing is not yet universal. nullifAI (2025) showed Picklescan evasion--signing would have provided a stronger guarantee than format-based defenses alone. Note: digital signatures verify integrity/provenance only, not model quality, fairness, or safety. Large model files (100GB+) create performance challenges for signature verification on load. *(Updated 2026-03)* |
| **3.1.3** | Verify that lineage and dependency tracking maintains a dependency graph that enables identification of all consuming services and agents per environment (e.g., dev, staging, prod). | 3 | V | Blast radius ambiguity when a model is compromised; inability to perform targeted incident response; cascading failures from untracked dependencies. | Review dependency graph tooling (e.g., ML Metadata, DVC, custom service mesh telemetry). Pick a model and trace all consumers across environments. Validate that the graph updates when new consumers are added. | Full dependency graph tracking across microservices, agents, and multi-model pipelines is operationally difficult. Most MLOps tools track model-to-experiment lineage but not model-to-consumer-service graphs. The Model Namespace Reuse attack (Unit 42, 2025) demonstrated the need for dependency tracking: thousands of open-source projects with hardcoded model references were vulnerable because they could not identify impacted consumers. Level 3 is appropriate given tooling gaps. *(Updated 2026-03)* |
| **3.1.4** | Verify that model origin integrity and trace records include an authorizing entity's identity, training data checksums, validation test results with pass/fail status, signature fingerprint/certificate chain ID, a creation timestamp, and approved deployment environments. | 3 | D/V | Deploying models without provenance; inability to audit who authorized a model; forensic gaps during incident investigation. | Inspect model metadata records for all required fields. Cross-reference authorizing identity against access control lists. Verify training data checksums match archived datasets. Confirm validation test results are linked and verifiable. | Comprehensive provenance records require tight integration between training pipelines, CI/CD, and registries. SLSA framework concepts apply--ReversingLabs (2025) proposes extending SLSA to ML by including ML-specific information in provenance files to detect undertrained models or those trained on compromised data. SLSA for ML is not yet standardized but adoption is growing. EU AI Act (effective Aug 2025) mandates technical documentation including training data provenance for GPAI models. Level 3 reflects the integration complexity. *(Updated 2026-03)* |

---

## C3.2 Model Validation & Testing

Models must pass defined security and safety validations before deployment.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.2.1** | Verify that models undergo automated security testing that includes input validation, output sanitization, and safety evaluations with pass/fail thresholds before deployment. | 1 | D/V | Deploying models vulnerable to prompt injection, jailbreaks, or producing unsafe/toxic outputs; regressions in safety behavior between versions. | Review CI/CD pipeline for automated test stages. Inspect test suites for input fuzzing, output content filtering, and safety red-teaming. Confirm pass/fail gates exist with defined thresholds. Check that failed tests block deployment. | Tools like Giskard, Deepchecks, and custom evaluation harnesses exist. Defining universal pass/fail thresholds for safety remains an open challenge--thresholds are highly application-specific. OWASP ML Security Top 10 (v0.3) identifies input manipulation and data poisoning as top threats requiring pre-deployment testing. Cleanlab's 2025 production survey found only 5% of AI agents in production have mature monitoring, underscoring the need for pre-deployment gates. *(Updated 2026-03)* |
| **3.2.2** | Verify that security testing covers agent workflows, tool and MCP integrations, RAG and memory interactions, multimodal inputs, and guardrails (safety models or detection services) using a versioned evaluation harness. | 2 | D/V | Exploits through agent tool chains, RAG poisoning, MCP server compromise, multimodal bypass of text-only guardrails; untested integration points becoming attack surface. | Inspect evaluation harness for test coverage across agent, tool, RAG, and multimodal code paths. Verify harness is versioned in source control. Check that test scenarios include adversarial inputs targeting each integration type. | MCP security testing is nascent--few established frameworks exist for testing MCP server interactions. Multimodal attack testing (e.g., adversarial images triggering unsafe text outputs) requires specialized tooling. Level 2 reflects moderate implementation complexity. |
| **3.2.3** | Verify that all model changes (deployment, configuration, retirement) generate immutable audit records including a timestamp, an authenticated actor identity, a change type, and before/after states, with trace metadata (environment and consuming services/agents) and a model identifier (version/digest/signature). | 2 | V | Unauthorized changes going undetected; inability to reconstruct incident timelines; compliance failures; repudiation of destructive actions. | Review audit log storage (append-only log, WORM storage, or blockchain-anchored). Verify logs contain all required fields by inspecting sample entries. Test immutability by attempting to modify or delete a log entry. Confirm logs capture all change types (deploy, config change, retire). | Immutable audit logging is well-supported by cloud providers (CloudTrail, Cloud Audit Logs). The challenge is ensuring all model lifecycle events--not just infrastructure events--are captured with the required metadata fields. EU AI Act (effective Aug 2025) requires lifecycle oversight documentation for GPAI models; ISO/IEC 42001 aligns quality management system requirements with audit trail expectations. *(Updated 2026-03)* |
| **3.2.4** | Verify that validation failures automatically block model deployment unless an explicit override approval from pre-designated authorized personnel with documented business justifications. | 3 | D/V | Deploying models that failed safety or security validation; normalization of overriding gates without accountability; audit trail gaps for exception handling. | Trigger a deliberate validation failure and confirm deployment is blocked. Test override workflow: verify it requires approval from pre-designated personnel, captures business justification, and logs the override. Confirm override approvers are a restricted, named set. | Requires tight CI/CD integration with approval workflows (e.g., GitHub branch protection, ServiceNow, PagerDuty). Level 3 because many organizations lack formal override processes for ML pipelines specifically. |

---

## C3.3 Controlled Deployment & Rollback

Model deployments must be controlled, monitored, and reversible.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.3.1** | Verify that deployment processes validate cryptographic signatures and compute integrity checksums before model activation or load, failing deployment on any mismatch. | 1 | D/V | Loading tampered model artifacts in production; supply chain substitution attacks; bit-rot or corruption during artifact transfer. | Review deployment scripts/controllers for signature verification and checksum validation steps. Deploy a model with a modified checksum and confirm the process rejects it. Inspect error handling to confirm fail-closed behavior. | Overlaps with 3.1.2 but focuses specifically on the deployment-time gate rather than the signing workflow. Checksum validation (SHA-256/SHA-512) is straightforward; signature verification adds PKI complexity but cosign simplifies this. The Model Namespace Reuse attack (Unit 42, 2025) showed that Google Vertex AI and Azure AI Foundry deployed Hugging Face models by name without integrity verification, enabling RCE--deployment-time signature checks would have prevented this. *(Updated 2026-03)* |
| **3.3.2** | Verify that production deployments implement gradual rollout mechanisms (e.g., canary or blue-green deployments) with automated rollback triggers based on pre-agreed error rates, latency thresholds, guardrail alerts, or tool/MCP failure rates. | 2 | D | Catastrophic failures from deploying a broken or adversarial model to 100% of traffic; inability to detect degradation before full exposure; delayed response to safety incidents. | Inspect deployment configuration for canary/blue-green settings (e.g., Kubernetes Argo Rollouts, Istio traffic splitting, cloud-native canary configs). Verify rollback trigger thresholds are defined and automated. Test by injecting elevated error rates and confirming automatic rollback fires. | Well-supported by Kubernetes ecosystem (Argo Rollouts, Flagger, Istio). AI-specific rollback triggers (guardrail alert rates, tool/MCP failure rates) may require custom metric collection beyond standard HTTP error rates. |
| **3.3.3** | Verify that rollback capabilities restore the complete model state (weights, configurations, dependencies including adapters and safety/policy models) atomically. | 2 | D/V | Partial rollback leaving inconsistent state (e.g., new weights with old safety model); cascading failures from version mismatches between model components. | Execute a rollback and verify that all components (weights, config, adapters, safety models) revert to the previous known-good version. Confirm atomicity--no intermediate state is served during rollback. Check that rollback is tested as part of deployment runbooks. | Atomic rollback of multi-artifact model stacks (base model + adapter + safety model + config) is harder than single-artifact rollback. Model serving platforms vary in support--some require custom orchestration. |
| **3.3.4** | Verify that emergency model shutdown capabilities can disable model endpoints within a pre-defined response time. | 3 | D/V | Continued exposure to an actively exploited or misbehaving model; inability to stop harm during a live incident; regulatory or legal requirement for rapid containment. | Review emergency shutdown runbook and SLA. Execute a shutdown drill and measure time-to-disable against the pre-defined target. Verify that shutdown is accessible to on-call incident responders without requiring full deployment pipeline access. | Pre-defined response time should be documented (e.g., under 5 minutes). Kill switches at the load balancer or API gateway level are fastest. DNS-based approaches are slower due to TTL propagation. Level 3 because formalized emergency shutdown with SLA is rare in ML deployments. |
| **3.3.5** | Verify that emergency shutdown cascades to all parts of the system including e.g. deactivating agent tool and MCP access, RAG connectors, database and API credentials, and memory-store bindings. | 3 | D/V | Orphaned agent sessions continuing to execute tools or access data after model shutdown; dangling MCP connections maintaining unauthorized access; data exfiltration through unrevoked credentials post-shutdown. | During a shutdown drill, verify that all dependent resources are deactivated: tool/MCP connections severed, RAG connectors disabled, credentials rotated or revoked, memory stores isolated. Check for any residual access paths post-shutdown. | Cascading shutdown across heterogeneous infrastructure (MCP servers, vector DBs, external APIs) requires an inventory of all integration points. Most organizations lack a unified "kill switch" that covers the full agent stack. Level 3 reflects this operational complexity. |

---

## C3.4 Secure Development Practices

Model development and training processes must follow secure practices to prevent compromise.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.4.1** | Verify that model development, testing, and production environments are physically or logically separated. They have no shared infrastructure, distinct access controls, and isolated data stores, and agent orchestration and tool or MCP servers are also isolated. | 1 | D/V | Lateral movement from dev to prod; accidental deployment of experimental models; data leakage between environments; compromised dev environment providing prod access. | Review network architecture diagrams and IAM policies for environment separation. Verify no shared service accounts, databases, or compute resources. Attempt cross-environment access and confirm it is denied. Check that MCP servers and tool endpoints are environment-specific. | Standard practice in software engineering but often neglected in ML workflows where data scientists may have broad access. Cloud providers offer good tooling (separate VPCs/projects, IAM boundaries). MCP server isolation is a newer concern with limited established patterns. |
| **3.4.2** | Verify that model development artifacts (such as hyperparameters, training scripts, configuration files, prompt templates, agent policies/routing graphs, tool or MCP contracts/schemas, and action catalogs or capability allow-lists) are stored in version control and require peer review approval before use in training. | 1 | D | Unauthorized changes to training configuration introducing backdoors or degrading safety; lack of accountability for training decisions; inability to reproduce training runs. | Inspect version control repository for all listed artifact types. Verify branch protection rules require peer review (e.g., GitHub CODEOWNERS, required reviewers). Check that training pipelines pull from version-controlled sources, not ad-hoc local files. | Well-supported by Git-based workflows. DVC and Git-LFS handle large artifacts. The challenge is cultural--ensuring data scientists use version control for all artifacts including prompt templates and agent routing configs, not just code. |
| **3.4.3** | Verify that model training and fine-tuning occur in isolated environments with controlled network access using egress allow-lists and no access to production tools or MCP resources. | 2 | D/V | Training pipeline exfiltrating data or model weights; compromised training job pivoting to production systems; supply chain attacks through uncontrolled package downloads during training. | Review network policies for training environments. Verify egress rules are allow-list based (not deny-list). Confirm no network paths exist from training to production endpoints. Test by attempting outbound connections to unauthorized destinations from training compute. | Cloud-native network policies (VPC Service Controls, Azure Private Link, AWS PrivateLink) support this well. The difficulty is maintaining allow-lists as training dependencies change--package mirrors and approved registries help. |
| **3.4.4** | Verify that training data sources are validated through integrity checks and authenticated via trusted sources with documented chain of custody before use in model development, including RAG indexes, tool logs, and agent-generated data used for fine-tuning. | 2 | D | Training data poisoning; fine-tuning on manipulated agent logs or RAG content; data integrity compromise leading to backdoored models; using unvetted third-party datasets. | Inspect data ingestion pipeline for integrity checks (checksums, schema validation). Verify data source authentication (signed datasets, authenticated API sources). Review chain of custody documentation for training datasets. Check that agent-generated data used for fine-tuning passes quality and integrity gates. | Data provenance tooling is immature compared to code provenance. Dataset signing is rare. ReversingLabs (2025) notes that digital signatures cannot adequately secure training data because it is "vast and dynamic," making integrity verification through signatures alone insufficient. Chain of custody for dynamically generated data (agent logs, RAG content) is particularly challenging. OWASP ML Top 10 identifies data poisoning as a top-tier threat. EU AI Act requires training data provenance documentation for GPAI models. Organizations often rely on process controls rather than technical enforcement. *(Updated 2026-03)* |

---

## C3.5 Model Retirement & Decommissioning

Models must be securely retired when they are no longer needed or when security issues are identified.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.5.1** | Verify that retired model artifacts (including adapters and safety/policy models) are securely wiped using secure cryptographic erasure. | 1 | D/V | Exfiltration of retired model IP; attackers recovering deprecated models with known vulnerabilities; regulatory exposure from retaining unnecessary model artifacts containing embedded training data. | Verify deletion procedures use cryptographic erasure (destroying encryption keys for encrypted-at-rest artifacts) or secure wipe standards (NIST SP 800-88). Confirm deletion covers all storage locations (primary, backups, caches, CDN edges). Attempt to recover a retired artifact and confirm failure. | Cryptographic erasure is the preferred approach for cloud-hosted artifacts (delete the KMS key). Physical media sanitization is relevant for on-premises deployments. The Model Namespace Reuse attack (Unit 42, 2025) demonstrated that incomplete decommissioning (deleting a namespace without clearing downstream references) can enable attackers to reclaim and weaponize the identity. Challenge: ensuring all copies are identified, including cached versions in model serving infrastructure. *(Updated 2026-03)* |
| **3.5.2** | Verify that model retirement events are logged with timestamp and actor identity, model identifier (version/digest/signature), and trace metadata (environment and consuming services/agents). Model signatures are revoked, registry/serving deny-lists are updated, and model loader caches are invalidated to prevent agents from loading retired artifacts. | 2 | V | Zombie models persisting in caches or edge nodes after official retirement; agents loading stale retired models; gaps in audit trail for decommissioning actions; re-deployment of models with revoked signatures. | Review retirement logs for completeness of required fields. Verify signature revocation in certificate/key management system. Check registry deny-lists include retired model identifiers. Attempt to load a retired model through standard serving infrastructure and confirm rejection. Test cache invalidation across all serving nodes. | Signature revocation and deny-lists require active enforcement at the model loader level. Most model serving frameworks (TorchServe, Triton, vLLM) do not natively support deny-lists--custom admission logic is needed. Cache invalidation across distributed serving infrastructure is operationally complex. |

---

## C3.6 Hosted and Provider-Managed Model Controls

Hosted and provider-managed models may change behavior without notice. These controls help ensure visibility, reassessment, and safe operation when the organization does not control the model weights.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.6.1** | Verify that hosted model dependencies are inventoried with provider, endpoint, provider-exposed model identifier, version or release identifier when available, and fallback or routing relationships. | 1 | D/V | Shadow use of hosted models; inability to assess blast radius when a provider changes or deprecates a model; untracked dependencies creating single points of failure. | Review inventory for completeness against actual API calls (trace logs, billing records). Verify each entry includes provider name, endpoint URL, model identifier, and version. Confirm fallback/routing relationships are documented and match implementation. | Providers vary significantly in version transparency. OpenAI exposes model IDs (e.g., gpt-4-0613) but may alias them. Anthropic exposes version identifiers. Some providers offer no versioning at all. Deprecation tracking services like [deprecations.info](https://deprecations.info/) now monitor OpenAI, Anthropic, Google Vertex AI, AWS Bedrock, Cohere, and xAI via JSON/RSS feeds. Azure AI Foundry provides 60-day retirement notices for GA models with 12-month minimum availability. Recent deprecations (2025-2026): OpenAI deprecated GPT-5.1 models (Mar 2026), Anthropic deprecated Claude 3.7 Sonnet (Nov 2025) and Claude 3.5 Haiku (Jan 2026), Google deprecated Gemini 3 Pro Preview (Mar 2026). Inventory must be maintained manually or through API call instrumentation. *(Updated 2026-03)* |
| **3.6.2** | Verify that provider model, version, or routing changes trigger security re-evaluation before continued use in high-risk workflows. | 2 | D/V | Silently degraded safety behavior after provider model update; new vulnerabilities introduced by model version change; compliance violations from using an unevaluated model version in regulated workflows. | Review change detection mechanism (provider changelogs, API response header monitoring, behavioral drift detection). Verify re-evaluation workflow exists with defined criteria. Confirm high-risk workflows are identified and mapped to model dependencies. Check that re-evaluation results are documented before resuming use. | Detection of provider changes is unreliable--not all providers announce changes. Silent updates are a documented risk: when providers update models, "every enterprise using those APIs gets the update silently" (ExtraHop, 2025). MIT research found 91% of ML models experience degradation over time; Gartner reports 67% of enterprises see measurable AI model degradation within 12 months. Azure AI Foundry auto-upgrades pinned deployments after retirement dates unless explicitly configured otherwise. Behavioral monitoring (tracking output distributions, safety test regressions) can serve as a detection proxy. Pinning to specific model versions where supported is a practical mitigation. *(Updated 2026-03)* |
| **3.6.3** | Verify that logs record the exact hosted model identifier returned by the provider, or explicitly record that no such identifier was exposed. | 2 | D/V | Inability to correlate incidents with specific model versions; forensic gaps when investigating provider-side changes; lack of evidence for compliance audits. | Inspect application logs for API responses that include model identifiers (e.g., OpenAI response headers, Anthropic model fields). Verify that when identifiers are absent, logs explicitly record this gap. Sample logs across time periods and confirm consistency. | Most major providers return model identifiers in API responses (OpenAI: `model` field, Anthropic: `model` field). Google Gemini API returns model metadata in responses. The requirement to log the absence of identifiers ensures the gap is visible rather than silently ignored. EU AI Act lifecycle oversight requirements (effective Aug 2025) strengthen the compliance case for comprehensive model version logging. *(Updated 2026-03)* |
| **3.6.4** | Verify that high-assurance deployments fail closed or require explicit approval when the provider does not expose sufficient model identity or change notification information for verification. | 3 | D/V | Operating high-risk workflows on unverifiable model versions; inability to meet audit requirements for model traceability; accepting unknown risk from opaque provider behavior. | Identify high-assurance workflows and their model dependencies. Verify fail-closed logic triggers when provider identity information is insufficient. Test by simulating a provider response without model identity metadata and confirm the system halts or routes to an approval workflow. | Defining "sufficient" model identity information requires organization-specific risk criteria. Fail-closed behavior may conflict with availability requirements--explicit approval as an alternative preserves availability while maintaining accountability. Azure AI Foundry's auto-upgrade-on-expiry behavior (where pinned deployments auto-upgrade after retirement) is an example of provider behavior that could trigger this control for high-assurance deployments. NIST AI RMF expects organizations to document human-in-the-loop expectations per AI system--fail-closed is a natural extension. Level 3 reflects the operational maturity needed. *(Updated 2026-03)* |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **MLOps platforms:** MLflow, Weights & Biases, Kubeflow, SageMaker, Vertex AI Model Registry, Azure AI Foundry
- **Model signing:** Sigstore/cosign for model artifacts, in-toto attestations, TUF (The Update Framework); ReversingLabs advocates extending Sigstore to ML models (2025)
- **SBOM/MBOM:** CycloneDX (v1.5+ ML BOM support with JSF/XMLsig enveloped signing), SPDX AI/ML profile, Syft (generates SBOMs from container images in both formats)
- **Deployment:** Seldon Core, BentoML, TorchServe, Triton Inference Server, vLLM with canary/blue-green strategies via Argo Rollouts or Flagger
- **Testing:** Giskard, Deepchecks, Great Expectations (for data validation), custom red-team harnesses
- **Data versioning:** DVC, LakeFS, Delta Lake
- **Audit logging:** Cloud-native (CloudTrail, Cloud Audit Logs, Azure Monitor), append-only log stores
- **Hosted model monitoring:** [deprecations.info](https://deprecations.info/) (tracks deprecations across OpenAI, Anthropic, Google, AWS Bedrock, Cohere, xAI via JSON/RSS), [llm-stats.com](https://llm-stats.com/llm-updates) (model release tracking)
- **Supply chain scanning:** Protect AI model scanning (352K issues found across 51.7K models in 2025), Hugging Face Picklescan (updated after nullifAI evasion), safetensors format
- **Standards/Frameworks:** NIST AI RMF (RMF 1.1 addenda expected through 2026), ISO/IEC 42001 (AI management systems), EU AI Act GPAI obligations (effective Aug 2025), SLSA for ML (emerging)

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C3.1 Model Authorization & Integrity | Medium | Model registries are mature; Sigstore model signing gaining advocacy (ReversingLabs 2025) but adoption still early. CycloneDX ML BOM and SPDX AI profiles maturing. EU AI Act GPAI obligations (Aug 2025) drive inventory requirements. SLSA for ML proposed but not standardized. *(Updated 2026-03)* |
| C3.2 Model Validation & Testing | Medium | Safety testing tools exist but lack standardized pass/fail benchmarks; MCP testing is nascent. Only 5% of production AI agents have mature monitoring (Cleanlab 2025). *(Updated 2026-03)* |
| C3.3 Controlled Deployment & Rollback | High | Canary/blue-green well-supported in Kubernetes ecosystem; atomic multi-artifact rollback less mature. Model Namespace Reuse attack (2025) demonstrated need for deployment-time integrity checks at cloud platform level. *(Updated 2026-03)* |
| C3.4 Secure Development Practices | High | Version control and environment isolation are solved problems; cultural adoption in ML teams varies. Data provenance remains a gap--digital signatures cannot adequately cover dynamic training data. *(Updated 2026-03)* |
| C3.5 Model Retirement & Decommissioning | Low | Cryptographic erasure supported by cloud KMS; deny-lists and cache invalidation require custom work. Namespace reuse attacks (2025) showed incomplete decommissioning enables supply chain hijacking. *(Updated 2026-03)* |
| C3.6 Hosted and Provider-Managed Model Controls | Low-Medium | Provider transparency improving: deprecation tracking services (deprecations.info) now cover 7 providers. Azure offers 60-day retirement notices. However, silent updates remain common and 91% of models degrade over time (MIT). No standard protocol for change notifications. *(Updated 2026-03)* |

---

## Open Research Questions

- [ ] What's the right cadence for model re-validation in production (drift vs. cost)? (MIT finding: 91% of models degrade; Gartner: 67% within 12 months)
- [ ] How do hosted model providers (OpenAI, Anthropic, Google) handle versioning transparency? (Partially answered: deprecations.info tracks 7 providers; Azure offers 60-day notices; OpenAI provides model IDs but aliases them; transparency remains inconsistent)
- [ ] What constitutes 'adequate' pre-deployment security testing for fine-tuned models? (Only 5% of production AI agents have mature monitoring per Cleanlab 2025)
- [ ] How should organizations manage rollback for models with stateful fine-tuning?
- [ ] Can SLSA (Supply-chain Levels for Software Artifacts) be adapted for ML model provenance? (ReversingLabs 2025 proposes extending SLSA provenance files with ML-specific metadata; not yet standardized)
- [ ] What standards should govern cascading emergency shutdown across agent infrastructure?
- [ ] How should organizations handle provider auto-upgrade behavior (e.g., Azure's upgrade-on-expiry for pinned model deployments)?
- [ ] What is the minimum viable model identity information that providers should expose for audit compliance under the EU AI Act?

---

## Related Standards & Cross-References

- [MITRE ATLAS](https://atlas.mitre.org/)
- [MLOps Principles](https://ml-ops.org/content/mlops-principles)
- [Reinforcement fine-tuning (OpenAI)](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
- [What is AI adversarial robustness? (IBM Research)](https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness)
- [SLSA Framework](https://slsa.dev/)
- [NIST SP 800-88 Guidelines for Media Sanitization](https://csrc.nist.gov/publications/detail/sp/800-88/rev-1/final)
- [CycloneDX ML BOM](https://cyclonedx.org/capabilities/mlbom/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act GPAI Obligations (CSA Guide)](https://cloudsecurityalliance.org/blog/2025/01/29/how-can-iso-iec-42001-nist-ai-rmf-help-comply-with-the-eu-ai-act)
- [OWASP Machine Learning Security Top 10](https://owasp.org/www-project-machine-learning-security-top-10/)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OpenAI Model Deprecations](https://developers.openai.com/api/docs/deprecations)
- [Azure AI Foundry Model Lifecycle](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/model-lifecycle-retirement)
- [AI Deprecations Feed](https://deprecations.info/)
- [Model Namespace Reuse Attack (Unit 42)](https://unit42.paloaltonetworks.com/model-namespace-reuse/)
- [Sigstore Cosign SBOM Spec](https://github.com/sigstore/cosign/blob/main/specs/SBOM_SPEC.md)

### AISVS Cross-Chapter Links

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| C01 (AI Governance) | Model inventory and accountability | C01 covers organizational governance; C03 covers technical lifecycle controls |
| C02 (Data Governance) | Training data integrity | C3.4.4 training data validation connects to C02 data quality and provenance controls |
| C05 (Agent Security) | Agent tool/MCP isolation and shutdown | C3.3.5 cascading shutdown and C3.4.1 MCP isolation overlap with C05 agent security controls |
| C06 (Output Security) | Output sanitization testing | C3.2.1 output sanitization testing relates to C06 output handling requirements |
| C10 (Logging & Monitoring) | Audit logging for model changes | C3.2.3 immutable audit records for model lifecycle events connect to C10 logging standards |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
