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
- Model supply chain attacks (compromised checkpoints on Hugging Face, etc.)
- Stale or vulnerable models remaining in production without rotation
- Silent hosted model updates changing behavior without consumer awareness
- Incomplete decommissioning leaving model artifacts accessible to attackers

### Notable Incidents & Research

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| 2024-02 | Hugging Face malicious pickle-based models | Supply chain attack via unsigned model artifacts on public hub | [JFrog blog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/) |
| 2023-04 | PyTorch nightly supply chain compromise | Malicious dependency injected into torchtriton package via PyPI | [PyTorch advisory](https://pytorch.org/blog/compromised-nightly-dependency/) |
| 2023 | ShadowRay (Anyscale Ray) CVE-2023-48022 | Unauthenticated access to ML training infrastructure and model artifacts | [Oligo Security](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild) |

---

## C3.1 Model Authorization & Integrity

Only authorized models with verified integrity reach production environments.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.1.1** | Verify that a model registry maintains an inventory of all deployed model artifacts and produces a machine-readable Model/AI Bill of Materials (MBOM/AIBOM) (e.g., SPDX or CycloneDX). | 1 | V | Untracked model deployments; inability to audit what is running in production; shadow AI. | Inspect model registry (MLflow, Vertex AI Model Registry, SageMaker Model Registry). Confirm MBOM/AIBOM export exists in SPDX or CycloneDX format. Validate completeness against deployed endpoints. | CycloneDX ML BOM support is maturing (added in v1.5). SPDX AI/ML profile is still evolving. Organizations may need custom tooling to auto-generate BOMs from training pipelines. |
| **3.1.2** | Verify that all model artifacts (weights, configurations, tokenizers, base models, fine-tunes, adapters, and safety/policy models) are cryptographically signed by authorized entities and verified at deployment admission (and on load), blocking any unsigned or tampered artifact. | 1 | D/V | Supply chain tampering; loading of backdoored or poisoned model weights; man-in-the-middle substitution during artifact transfer. | Verify signing workflow exists (e.g., Sigstore cosign, in-toto attestations, or GPG). Test by deploying an unsigned or modified artifact and confirm it is rejected. Inspect admission controller or model loader code for signature verification logic. | Sigstore model signing is available but adoption is early. Hugging Face added safetensors format to mitigate pickle-based attacks but signing is not yet universal. Large model files (100GB+) create performance challenges for signature verification on load. |
| **3.1.3** | Verify that lineage and dependency tracking maintains a dependency graph that enables identification of all consuming services and agents per environment (e.g., dev, staging, prod). | 3 | V | Blast radius ambiguity when a model is compromised; inability to perform targeted incident response; cascading failures from untracked dependencies. | Review dependency graph tooling (e.g., ML Metadata, DVC, custom service mesh telemetry). Pick a model and trace all consumers across environments. Validate that the graph updates when new consumers are added. | Full dependency graph tracking across microservices, agents, and multi-model pipelines is operationally difficult. Most MLOps tools track model-to-experiment lineage but not model-to-consumer-service graphs. Level 3 is appropriate given tooling gaps. |
| **3.1.4** | Verify that model origin integrity and trace records include an authorizing entity's identity, training data checksums, validation test results with pass/fail status, signature fingerprint/certificate chain ID, a creation timestamp, and approved deployment environments. | 3 | D/V | Deploying models without provenance; inability to audit who authorized a model; forensic gaps during incident investigation. | Inspect model metadata records for all required fields. Cross-reference authorizing identity against access control lists. Verify training data checksums match archived datasets. Confirm validation test results are linked and verifiable. | Comprehensive provenance records require tight integration between training pipelines, CI/CD, and registries. SLSA framework concepts apply but SLSA for ML is not yet standardized. Level 3 reflects the integration complexity. |

---

## C3.2 Model Validation & Testing

Models must pass defined security and safety validations before deployment.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.2.1** | Verify that models undergo automated security testing that includes input validation, output sanitization, and safety evaluations with pass/fail thresholds before deployment. | 1 | D/V | Deploying models vulnerable to prompt injection, jailbreaks, or producing unsafe/toxic outputs; regressions in safety behavior between versions. | Review CI/CD pipeline for automated test stages. Inspect test suites for input fuzzing, output content filtering, and safety red-teaming. Confirm pass/fail gates exist with defined thresholds. Check that failed tests block deployment. | Tools like Giskard, Deepchecks, and custom evaluation harnesses exist. Defining universal pass/fail thresholds for safety remains an open challenge--thresholds are highly application-specific. |
| **3.2.2** | Verify that security testing covers agent workflows, tool and MCP integrations, RAG and memory interactions, multimodal inputs, and guardrails (safety models or detection services) using a versioned evaluation harness. | 2 | D/V | Exploits through agent tool chains, RAG poisoning, MCP server compromise, multimodal bypass of text-only guardrails; untested integration points becoming attack surface. | Inspect evaluation harness for test coverage across agent, tool, RAG, and multimodal code paths. Verify harness is versioned in source control. Check that test scenarios include adversarial inputs targeting each integration type. | MCP security testing is nascent--few established frameworks exist for testing MCP server interactions. Multimodal attack testing (e.g., adversarial images triggering unsafe text outputs) requires specialized tooling. Level 2 reflects moderate implementation complexity. |
| **3.2.3** | Verify that all model changes (deployment, configuration, retirement) generate immutable audit records including a timestamp, an authenticated actor identity, a change type, and before/after states, with trace metadata (environment and consuming services/agents) and a model identifier (version/digest/signature). | 2 | V | Unauthorized changes going undetected; inability to reconstruct incident timelines; compliance failures; repudiation of destructive actions. | Review audit log storage (append-only log, WORM storage, or blockchain-anchored). Verify logs contain all required fields by inspecting sample entries. Test immutability by attempting to modify or delete a log entry. Confirm logs capture all change types (deploy, config change, retire). | Immutable audit logging is well-supported by cloud providers (CloudTrail, Cloud Audit Logs). The challenge is ensuring all model lifecycle events--not just infrastructure events--are captured with the required metadata fields. |
| **3.2.4** | Verify that validation failures automatically block model deployment unless an explicit override approval from pre-designated authorized personnel with documented business justifications. | 3 | D/V | Deploying models that failed safety or security validation; normalization of overriding gates without accountability; audit trail gaps for exception handling. | Trigger a deliberate validation failure and confirm deployment is blocked. Test override workflow: verify it requires approval from pre-designated personnel, captures business justification, and logs the override. Confirm override approvers are a restricted, named set. | Requires tight CI/CD integration with approval workflows (e.g., GitHub branch protection, ServiceNow, PagerDuty). Level 3 because many organizations lack formal override processes for ML pipelines specifically. |

---

## C3.3 Controlled Deployment & Rollback

Model deployments must be controlled, monitored, and reversible.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.3.1** | Verify that deployment processes validate cryptographic signatures and compute integrity checksums before model activation or load, failing deployment on any mismatch. | 1 | D/V | Loading tampered model artifacts in production; supply chain substitution attacks; bit-rot or corruption during artifact transfer. | Review deployment scripts/controllers for signature verification and checksum validation steps. Deploy a model with a modified checksum and confirm the process rejects it. Inspect error handling to confirm fail-closed behavior. | Overlaps with 3.1.2 but focuses specifically on the deployment-time gate rather than the signing workflow. Checksum validation (SHA-256/SHA-512) is straightforward; signature verification adds PKI complexity but cosign simplifies this. |
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
| **3.4.4** | Verify that training data sources are validated through integrity checks and authenticated via trusted sources with documented chain of custody before use in model development, including RAG indexes, tool logs, and agent-generated data used for fine-tuning. | 2 | D | Training data poisoning; fine-tuning on manipulated agent logs or RAG content; data integrity compromise leading to backdoored models; using unvetted third-party datasets. | Inspect data ingestion pipeline for integrity checks (checksums, schema validation). Verify data source authentication (signed datasets, authenticated API sources). Review chain of custody documentation for training datasets. Check that agent-generated data used for fine-tuning passes quality and integrity gates. | Data provenance tooling is immature compared to code provenance. Dataset signing is rare. Chain of custody for dynamically generated data (agent logs, RAG content) is particularly challenging. Organizations often rely on process controls rather than technical enforcement. |

---

## C3.5 Model Retirement & Decommissioning

Models must be securely retired when they are no longer needed or when security issues are identified.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.5.1** | Verify that retired model artifacts (including adapters and safety/policy models) are securely wiped using secure cryptographic erasure. | 1 | D/V | Exfiltration of retired model IP; attackers recovering deprecated models with known vulnerabilities; regulatory exposure from retaining unnecessary model artifacts containing embedded training data. | Verify deletion procedures use cryptographic erasure (destroying encryption keys for encrypted-at-rest artifacts) or secure wipe standards (NIST SP 800-88). Confirm deletion covers all storage locations (primary, backups, caches, CDN edges). Attempt to recover a retired artifact and confirm failure. | Cryptographic erasure is the preferred approach for cloud-hosted artifacts (delete the KMS key). Physical media sanitization is relevant for on-premises deployments. Challenge: ensuring all copies are identified, including cached versions in model serving infrastructure. |
| **3.5.2** | Verify that model retirement events are logged with timestamp and actor identity, model identifier (version/digest/signature), and trace metadata (environment and consuming services/agents). Model signatures are revoked, registry/serving deny-lists are updated, and model loader caches are invalidated to prevent agents from loading retired artifacts. | 2 | V | Zombie models persisting in caches or edge nodes after official retirement; agents loading stale retired models; gaps in audit trail for decommissioning actions; re-deployment of models with revoked signatures. | Review retirement logs for completeness of required fields. Verify signature revocation in certificate/key management system. Check registry deny-lists include retired model identifiers. Attempt to load a retired model through standard serving infrastructure and confirm rejection. Test cache invalidation across all serving nodes. | Signature revocation and deny-lists require active enforcement at the model loader level. Most model serving frameworks (TorchServe, Triton, vLLM) do not natively support deny-lists--custom admission logic is needed. Cache invalidation across distributed serving infrastructure is operationally complex. |

---

## C3.6 Hosted and Provider-Managed Model Controls

Hosted and provider-managed models may change behavior without notice. These controls help ensure visibility, reassessment, and safe operation when the organization does not control the model weights.

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **3.6.1** | Verify that hosted model dependencies are inventoried with provider, endpoint, provider-exposed model identifier, version or release identifier when available, and fallback or routing relationships. | 1 | D/V | Shadow use of hosted models; inability to assess blast radius when a provider changes or deprecates a model; untracked dependencies creating single points of failure. | Review inventory for completeness against actual API calls (trace logs, billing records). Verify each entry includes provider name, endpoint URL, model identifier, and version. Confirm fallback/routing relationships are documented and match implementation. | Providers vary significantly in version transparency. OpenAI exposes model IDs (e.g., gpt-4-0613) but may alias them. Anthropic exposes version identifiers. Some providers offer no versioning at all. Inventory must be maintained manually or through API call instrumentation. |
| **3.6.2** | Verify that provider model, version, or routing changes trigger security re-evaluation before continued use in high-risk workflows. | 2 | D/V | Silently degraded safety behavior after provider model update; new vulnerabilities introduced by model version change; compliance violations from using an unevaluated model version in regulated workflows. | Review change detection mechanism (provider changelogs, API response header monitoring, behavioral drift detection). Verify re-evaluation workflow exists with defined criteria. Confirm high-risk workflows are identified and mapped to model dependencies. Check that re-evaluation results are documented before resuming use. | Detection of provider changes is unreliable--not all providers announce changes. Behavioral monitoring (tracking output distributions, safety test regressions) can serve as a detection proxy. Pinning to specific model versions where supported is a practical mitigation. |
| **3.6.3** | Verify that logs record the exact hosted model identifier returned by the provider, or explicitly record that no such identifier was exposed. | 2 | D/V | Inability to correlate incidents with specific model versions; forensic gaps when investigating provider-side changes; lack of evidence for compliance audits. | Inspect application logs for API responses that include model identifiers (e.g., OpenAI response headers, Anthropic model fields). Verify that when identifiers are absent, logs explicitly record this gap. Sample logs across time periods and confirm consistency. | Most major providers return model identifiers in API responses (OpenAI: `model` field, Anthropic: `model` field). The requirement to log the absence of identifiers ensures the gap is visible rather than silently ignored. |
| **3.6.4** | Verify that high-assurance deployments fail closed or require explicit approval when the provider does not expose sufficient model identity or change notification information for verification. | 3 | D/V | Operating high-risk workflows on unverifiable model versions; inability to meet audit requirements for model traceability; accepting unknown risk from opaque provider behavior. | Identify high-assurance workflows and their model dependencies. Verify fail-closed logic triggers when provider identity information is insufficient. Test by simulating a provider response without model identity metadata and confirm the system halts or routes to an approval workflow. | Defining "sufficient" model identity information requires organization-specific risk criteria. Fail-closed behavior may conflict with availability requirements--explicit approval as an alternative preserves availability while maintaining accountability. Level 3 reflects the operational maturity needed. |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **MLOps platforms:** MLflow, Weights & Biases, Kubeflow, SageMaker, Vertex AI
- **Model signing:** Sigstore/cosign for model artifacts, in-toto attestations, TUF (The Update Framework)
- **SBOM/MBOM:** CycloneDX (v1.5+ ML BOM support), SPDX AI/ML profile
- **Deployment:** Seldon Core, BentoML, TorchServe, Triton Inference Server, vLLM with canary/blue-green strategies via Argo Rollouts or Flagger
- **Testing:** Giskard, Deepchecks, Great Expectations (for data validation), custom red-team harnesses
- **Data versioning:** DVC, LakeFS, Delta Lake
- **Audit logging:** Cloud-native (CloudTrail, Cloud Audit Logs, Azure Monitor), append-only log stores

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C3.1 Model Authorization & Integrity | Medium | Model registries are mature; signing and MBOM tooling is emerging but not yet standard practice |
| C3.2 Model Validation & Testing | Medium | Safety testing tools exist but lack standardized pass/fail benchmarks; MCP testing is nascent |
| C3.3 Controlled Deployment & Rollback | High | Canary/blue-green well-supported in Kubernetes ecosystem; atomic multi-artifact rollback less mature |
| C3.4 Secure Development Practices | High | Version control and environment isolation are solved problems; cultural adoption in ML teams varies |
| C3.5 Model Retirement & Decommissioning | Low | Cryptographic erasure supported by cloud KMS; deny-lists and cache invalidation require custom work |
| C3.6 Hosted and Provider-Managed Model Controls | Low | Provider transparency varies widely; no standard protocol for change notifications or version pinning |

---

## Open Research Questions

- [ ] What's the right cadence for model re-validation in production (drift vs. cost)?
- [ ] How do hosted model providers (OpenAI, Anthropic, Google) handle versioning transparency?
- [ ] What constitutes 'adequate' pre-deployment security testing for fine-tuned models?
- [ ] How should organizations manage rollback for models with stateful fine-tuning?
- [ ] Can SLSA (Supply-chain Levels for Software Artifacts) be adapted for ML model provenance?
- [ ] What standards should govern cascading emergency shutdown across agent infrastructure?

---

## Related Standards & Cross-References

- [MITRE ATLAS](https://atlas.mitre.org/)
- [MLOps Principles](https://ml-ops.org/content/mlops-principles)
- [Reinforcement fine-tuning (OpenAI)](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
- [What is AI adversarial robustness? (IBM Research)](https://research.ibm.com/blog/securing-ai-workflows-with-adversarial-robustness)
- [SLSA Framework](https://slsa.dev/)
- [NIST SP 800-88 Guidelines for Media Sanitization](https://csrc.nist.gov/publications/detail/sp/800-88/rev-1/final)
- [CycloneDX ML BOM](https://cyclonedx.org/capabilities/mlbom/)

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
