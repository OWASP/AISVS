# C4.6 AI Infrastructure Resource Management, Backup & Recovery

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Prevent resource exhaustion attacks and ensure fair resource allocation through quotas and monitoring. Maintain infrastructure resilience through secure backups, tested recovery procedures, and disaster recovery capabilities. AI workloads are resource-intensive by nature -- a single training job can consume hundreds of GPUs for weeks, and inference endpoints can be overwhelmed by adversarial input patterns. This section ensures that resource consumption is bounded and that critical AI assets (model weights, training checkpoints, configuration) can be recovered after incidents.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.6.1** | Verify that workload resource consumption is limited through quotas and limits (e.g., CPU, memory, GPU) to mitigate denial-of-service attacks. | 1 | D/V | Resource exhaustion DoS: a single malicious or buggy workload consuming all GPU memory, CPU, or network bandwidth, starving other workloads. Cryptomining on hijacked GPU infrastructure. | Verify Kubernetes resource requests and limits are set for all containers (CPU, memory). Check GPU resource limits via device plugin (nvidia.com/gpu). Confirm namespace-level ResourceQuotas are configured. Validate LimitRange defaults prevent pods without explicit limits. | GPU resource limits in Kubernetes are coarse-grained -- you can limit GPU count but not GPU memory percentage. NVIDIA MIG (Multi-Instance GPU) enables finer partitioning on A100/H100 GPUs. For inference, consider request-level rate limiting in addition to infrastructure-level quotas. Memory limits are critical for ML workloads that load large models -- OOM kills should be handled gracefully. |
| **4.6.2** | Verify that resource exhaustion triggers automated protections (e.g., rate limiting or workload isolation) once defined CPU, memory, or request thresholds are exceeded. | 2 | D/V | Slow-burn resource exhaustion that stays below quota limits but degrades service over time. Inference endpoints overwhelmed by adversarial queries designed to maximize compute cost (e.g., extremely long prompts, high-complexity inputs). | Verify autoscaling policies include maximum bounds. Check that HPA/VPA configurations have proper ceiling limits. Confirm alerts fire when resource usage exceeds thresholds (e.g., > 80% GPU utilization sustained for > 5 minutes). Test that circuit breakers activate under sustained load. | AI-specific DoS patterns include: crafted inputs that trigger worst-case inference latency (long sequences for transformers), repeated requests for expensive operations (image generation at max resolution), and prompt injection causing recursive tool calls in agentic systems. Rate limiting should consider both request count and estimated compute cost per request. |
| **4.6.3** | Verify that backup systems run in isolated networks with separate credentials, and the storage system is either run in an air-gapped network or implements WORM (write-once-read-many) protection against unauthorized modification. | 2 | D/V | Ransomware encrypting or deleting model weights, training checkpoints, and training data. Insider threat deleting backups to cover tracks after model tampering. Supply chain attack that corrupts model artifacts and their backups simultaneously. | Verify backup infrastructure uses separate credentials from production (different IAM roles, different service accounts). Confirm network isolation (separate VPC or air-gapped). Check WORM configuration (AWS S3 Object Lock, Azure Immutable Blob Storage, GCP Bucket Lock). Test that backup deletion requires separate authorization. | AI assets requiring backup include: trained model weights (potentially terabytes), training checkpoints, training data references/manifests, model configuration, evaluation results, and experiment tracking metadata. Backup frequency should match the cost of retraining -- if a model costs $1M to train, backup strategy should prevent any scenario requiring full retraining. Consider incremental checkpoint backup during long training runs. |

---

## Implementation Guidance

### GPU Resource Quotas and Admission Control

Traditional Kubernetes ResourceQuotas limit GPU consumption per namespace, enabling fair sharing across teams. However, GPU-bound AI architectures need more advanced admission control. Two mature solutions have emerged by 2025-2026:

- **Kueue** (Kubernetes-native): Admits entire workloads atomically only when quota allows, preventing partial allocations that waste GPU capacity. ClusterQueues implement quotas by ResourceFlavor (e.g., H100 vs. A100), preventing any single tenant from monopolizing GPU inventory. Each queue has a `nominalQuota` cap with explicit borrowing rules between cohorts.
- **Volcano**: Uses PodGroup semantics with `minMember` thresholds and preemption plugins to enforce fair eviction across multi-GPU training jobs. As of mid-2025, Volcano added Network Topology-Aware Scheduling (alpha), Dynamic MIG Partitioning for GPU virtualization, DRA support, and LeaderWorkerSet support for large model inference scenarios.
- **NVIDIA KAI Scheduler**: An open-source Kubernetes-native scheduler for AI workloads that allows customization of quotas, over-quota weights, limits, and priorities per queue while ensuring equitable distribution using Dominant Resource Fairness (DRF) and resource reclamation across queues.

LimitRanges should set both default and maximum GPU requests per pod. Defaults ensure pods without explicit GPU requests still receive appropriate allocations; maximums prevent individual pods from requesting excessive GPU capacity.

For multi-tenant environments, use per-tenant LocalQueues bound to ClusterQueues with borrowing controls rather than a single shared production queue. Implement WorkloadPriorityClasses to ensure critical inference workloads are not starved by lower-priority batch training jobs.

### Dynamic Resource Allocation (DRA) for GPUs

As of Kubernetes v1.34 (2025), Dynamic Resource Allocation (DRA) reached GA, fundamentally changing how GPUs are consumed in Kubernetes. Under DRA, accelerators like GPUs are no longer exposed as static extended resources through device plugins. Instead, they are dynamically allocated through DeviceClasses and ResourceClaims, which unlocks richer scheduling semantics and better integration with virtualization technologies like NVIDIA vGPU and MIG.

Key benefits for AI workload security and resource management:

- **Fine-grained partitioning**: DRA enables requesting specific GPU slices (e.g., a single MIG partition) rather than whole GPUs, reducing resource waste and limiting the blast radius if a workload is compromised
- **Vendor-neutral device classes**: Cluster administrators define DeviceClasses (e.g., `gpu-h100-mig-3g.20gb`) that abstract hardware details while enforcing security boundaries -- workloads request capabilities rather than raw device paths
- **Dynamic reclamation**: Resources are released and reclaimed dynamically when pods complete, preventing GPU hoarding by long-idle workloads that would otherwise block legitimate jobs
- **Integration with admission control**: DRA works alongside Kueue and Volcano, enabling quota enforcement at the ResourceClaim level rather than just pod-level resource requests

Major cloud providers (GKE, AKS, EKS) now support DRA for GPU workloads as of early 2026. Organizations running Kubernetes 1.34+ should migrate from the legacy device plugin model to DRA for improved multi-tenant isolation and scheduling flexibility.

### GPU Partitioning and Multi-Tenant Isolation

NVIDIA Multi-Instance GPU (MIG) provides hardware-enforced isolation on Ampere and Hopper GPUs (A100, H100), partitioning a single GPU into up to seven independent instances with dedicated memory, cache, and compute slices. This is critical for multi-tenant safety because workloads cannot interfere with each other's memory or execution, unlike time-slicing approaches where a crash or memory leak in one workload can destabilize neighbors.

Best practices for GPU isolation include:

- **Separate node pools** by GPU family and MIG policy, exposed as distinct Flavors to prevent unexpected layout conflicts
- **Topology Manager** (`single-numa-node`) on kubelet to ensure CPU/device alignment and prevent performance degradation from cross-NUMA access
- **Node Feature Discovery (NFD)** to label GPU capabilities, enabling placement constraints that segregate workload types by security sensitivity

### GPU Cryptojacking and Resource Abuse

GPU infrastructure is a high-value target for cryptojacking attacks because GPU compute is directly monetizable through cryptocurrency mining. Real-world attacks targeting AI clusters have escalated significantly in 2024-2026:

- **ShadowRay 2.0 (2024-2025)**: Exploits CVE-2023-48022 (CVSS 9.8) in the Ray framework, allowing unauthenticated remote code execution via the Jobs API on internet-exposed dashboards. Exposed Ray environments grew from a few thousand to approximately 230,000 by late 2025. Attackers (tracked as IronErn440) turned Ray's legitimate orchestration features into a self-propagating, globally distributed cryptojacking operation that spreads autonomously across exposed clusters.
- **Dero Cryptojacking Campaign**: Targets Kubernetes clusters with anonymous access enabled on the Kubernetes API listening on non-standard ports. Attackers deploy a DaemonSet named "proxy-api" that places a malicious pod on every node, harnessing all GPU resources simultaneously for mining.
- **NVIDIAScape / CVE-2025-23266 (July 2025)**: A critical (CVSS 9.0) container escape vulnerability in the NVIDIA Container Toolkit (versions up to 1.17.7) and GPU Operator (up to 25.3.0). Exploitable with a three-line Dockerfile -- attackers set `LD_PRELOAD` in their container image, causing the `nvidia-ctk` OCI hook to load a malicious shared library with root privileges on the host. Wiz Research estimated approximately 37% of cloud environments were susceptible, making this a systemic risk for any multi-tenant GPU infrastructure. Remediation: upgrade to Container Toolkit v1.17.8+ or GPU Operator v25.3.1+, or disable the `enable-cuda-compat-lib-hook` as an interim measure.
- **GPUHammer (July 2025)**: Researchers at the University of Toronto demonstrated the first Rowhammer attack against NVIDIA GDDR6 GPU memory (RTX A6000). By inducing bit flips in GPU DRAM, a single bit flip in FP16 model weight exponents degraded model accuracy from 80% to 0.1% across five tested ImageNet DNN models. This is particularly dangerous in multi-tenant cloud GPU environments where attackers and victims share physical hardware. GPUs with HBM3 memory (H100) and GDDR7 (RTX 5090) feature on-die ECC that likely mitigates single-bit flips, but GDDR6 GPUs remain vulnerable.

Detection indicators for cryptojacking on AI infrastructure:

- Sustained high GPU utilization (>90%) on nodes that should be idle or running light inference workloads
- Unexpected outbound network connections, particularly to mining pool addresses
- DaemonSets or pods deployed outside normal CI/CD pipelines
- Anomalous power draw and temperature patterns on accelerator telemetry
- Unexplained increases in cloud compute bills (enterprises underestimate AI infrastructure costs by 30% on average, making cryptojacking charges easy to miss)

Mitigations: enforce network policies with default-deny egress, require authentication on all orchestration APIs (Ray, Kubernetes), monitor accelerator telemetry for anomalous utilization patterns, and implement admission controllers that reject unsigned container images.

### Agentic Resource Exhaustion

As agentic AI systems become more prevalent, a distinct class of resource exhaustion attacks has emerged: infinite loop and recursive tool-call attacks. An attacker crafts inputs that cause an agent to enter expensive computational loops -- repeatedly invoking tools, spawning sub-agents, or generating unbounded chains of reasoning -- running up GPU and API costs without producing useful output. Industry surveys from late 2025 indicate that nearly half of security practitioners expect agentic AI to represent a top attack vector by the end of 2026.

Defenses against agentic resource exhaustion should be architectural, not just reactive:

- **Execution budgets**: Hard caps on total tokens generated, tool calls made, and wall-clock time per agent invocation. The system should assume the agent will get stuck and build guardrails to terminate it before costs spiral.
- **Cost-per-request estimation**: Before dispatching to a GPU, estimate the compute cost of a request (based on input length, model size, and expected generation length) and reject requests exceeding a per-user or per-session budget.
- **Recursive call depth limits**: Cap the number of nested tool invocations or sub-agent spawns. Log and alert when agents approach these limits, as it may indicate adversarial input.
- **Circuit breakers with cooldown**: When an agent hits its budget cap, enforce a cooldown period before it can be re-invoked, preventing rapid retry loops.

### AI-Specific Cost Management

AI workloads present unique cost management challenges due to GPU price volatility, token-based inference pricing, and the ease with which resource abuse can hide in legitimately high utilization. Key practices for 2025-2026:

- **Cost-per-inference tracking**: Track cost per inference or per thousand tokens as a first-class operational metric, not just aggregate GPU-hours. This makes unauthorized workloads visible.
- **Rightsizing models and hardware**: Use the smallest model that satisfies accuracy requirements. A 7B parameter model running on a single GPU may serve the same business need as a 70B model on eight GPUs at 10x the cost.
- **AI-native FinOps**: Organizations applying AI-specific financial operations practices report 30-40% reductions in cloud spend through dynamic pooling, priority scheduling, and automated lifecycle management that eliminates idle capacity between training runs.
- **Utilization as security signal**: Organizations achieving sustained 90% GPU utilization under active load have better visibility into anomalous resource consumption. GPUs sitting idle 70-85% of the time (a common finding) make it easy for cryptojacking to go unnoticed.

---

## Backup and Recovery for AI Assets

### What Must Be Backed Up

AI disaster recovery requires protecting a broader set of artifacts than traditional application backups. Critical components include:

- **Model weights** (potentially 100GB-1TB+ for large language models)
- **Training checkpoints** saved every 1,000-5,000 steps (every 500 steps for high-stakes models)
- **Tokenizer vocabularies and quantization configurations** -- 32% of recovery failures occur because teams back up weights but forget tokenizer files or quantization configs, causing models to load but fail to process input correctly
- **Prompt templates and system prompts**
- **Fine-tuning adapters** (LoRA weights, configuration files)
- **API rate limits and security filter configurations**
- **Preprocessing scripts, data versioning, and augmentation rules** (back up metadata rather than raw training data)
- **Experiment tracking metadata and evaluation results**

All components must be version-consistent: if model weights are out of sync with prompt templates or API endpoint configurations, recovery will fail even if individual artifacts are intact.

### Recovery Targets (RTO/RPO)

Industry benchmarks for AI infrastructure disaster recovery as of 2025:

| Workload Type | RTO Target | RPO Target | Notes |
|---|---|---|---|
| Inference APIs | 22-47 minutes | Under 5 minutes | Bandwidth-constrained: transferring a 200GB model over 1 Gbps takes 27 minutes |
| Training environments | 4-8 hours | 24 hours | Acceptable due to checkpoint-based resumption |
| Real-time fine-tuned models | 30-60 minutes | 15 minutes | Frequent incremental backup required |

### Immutable Storage and the 3-2-1-1-0 Rule

The traditional 3-2-1 backup rule has been adapted for AI environments as the **3-2-1-1-0 rule**:

- **3** copies of data (production + two backups)
- **2** different storage types (e.g., object storage + tape/cold storage)
- **1** offsite location (different region or cloud provider)
- **1** immutable copy (WORM-protected, cannot be modified or deleted even by administrators)
- **0** errors through automated verification (hash-based integrity checks on every backup)

WORM-protected storage options: AWS S3 Object Lock (Governance or Compliance mode), Azure Immutable Blob Storage, GCP Bucket Lock with retention policies. Compliance mode prevents even root/admin users from deleting backups before the retention period expires.

### Automated Failover Process

A proven failover sequence used by major enterprises (JPMorgan Chase, Mayo Clinic):

1. Monitor model performance continuously (latency, error rates, output quality)
2. Trigger failover if accuracy drops below threshold for 3+ minutes
3. Route traffic to standby region via DNS/API gateway updates
4. Load latest checkpoint from object storage (S3, GCS, Blob Storage)
5. Validate model with a test batch before enabling live traffic
6. Alert the team and log the incident

Organizations following structured recovery playbooks recover 63% faster than those using generic IT DR plans and spend 40% less on emergency fixes.

### Recovery Testing

A critical gap: as of early 2026, **fewer than 50% of organizations have verified their backup recovery procedures**, even though 98% report having ransomware playbooks. Meanwhile, **89% of organizations have had backup repositories directly targeted** by ransomware operators -- modern ransomware variants are specifically designed to locate and destroy backups before encrypting production data. The LockBit 3.0 Reborn campaign (February 2026) compromised 20+ victims, with the worst outcomes consistently linked to organizations that lacked immutable backups, resulting in multi-million-dollar payouts. Recovery testing should include:

- Quarterly simulated regional outages with full end-to-end recovery
- Validation that all artifacts load correctly together (not just that individual backups exist)
- Verification of version consistency between model weights, tokenizers, prompt templates, and configurations
- Measurement of actual RTO against target RTO
- Offline runbooks with step-by-step recovery instructions that do not depend on systems that might be unavailable during an outage

Use incremental backups to reduce storage costs (e.g., 200GB monthly vs. 6TB for daily full backups), but test that incremental restoration actually produces a functional system.

---

## Related Standards & References

- [NIST SP 800-184: Guide for Cybersecurity Event Recovery](https://csrc.nist.gov/publications/detail/sp/800-184/final)
- [CIS Controls v8 -- Control 11: Data Recovery](https://www.cisecurity.org/controls/data-recovery)
- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Kubernetes Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [NVIDIA MIG User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/)
- [AWS S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)
- [NVIDIA KAI Scheduler (GitHub)](https://github.com/NVIDIA/KAI-Scheduler)
- [Kueue: Kubernetes-Native AI Workload Scheduling](https://www.coreweave.com/blog/kueue-a-kubernetes-native-system-for-ai-training-workloads)
- [Kubernetes GPU Scheduling 2025: Kueue, Volcano, MIG](https://debugg.ai/resources/kubernetes-gpu-scheduling-2025-kueue-volcano-mig)
- [CrowdStrike: Dero Cryptojacking Campaign Targeting Kubernetes](https://www.crowdstrike.com/en-us/blog/crowdstrike-discovers-first-ever-dero-cryptojacking-campaign-targeting-kubernetes/)
- [Disaster Recovery for LLM Infrastructure: Backups and Failover](https://brics-econ.org/disaster-recovery-for-large-language-model-infrastructure-backups-and-failover)
- [Securing GPU-Accelerated AI Workloads in Kubernetes (Oracle/Sysdig)](https://blogs.oracle.com/cloud-infrastructure/securing-gpu-accelerated-ai-workloads-kubernetes)
- [NVIDIAScape: CVE-2025-23266 Container Escape Analysis (Wiz Research)](https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape)
- [GPUHammer: Rowhammer Attacks on GPU Memories (USENIX Security 2025)](https://www.usenix.org/conference/usenixsecurity25/presentation/lin-shaopeng)
- [Kubernetes Dynamic Resource Allocation](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/)
- [CNCF: Why Every AI Platform Is Converging on Kubernetes (March 2026)](https://www.cncf.io/blog/2026/03/05/the-great-migration-why-every-ai-platform-is-converging-on-kubernetes/)
- [Navigating the Threat Landscape for Cloud-Based GPUs (Trend Micro)](https://www.trendmicro.com/vinfo/us/security/news/threat-landscape/navigating-the-threat-landscape-for-cloud-based-gpus)

---

## Open Research Questions

- [ ] How should resource quotas account for the variable compute cost of different inference requests (short vs. long sequences, simple vs. complex generation)? Kueue's ResourceFlavor approach is promising but does not yet support per-request cost estimation.
- [ ] What is the optimal checkpoint frequency for long-running training jobs balancing storage cost against potential recompute cost? Current guidance (every 1,000-5,000 steps) is rule-of-thumb; cost-optimal frequency depends on training cost per step and probability of failure.
- [ ] How can WORM-protected backups handle the iterative nature of model development where old checkpoints are regularly superseded? Retention policies must balance immutability guarantees against storage cost growth.
- [ ] Can accelerator telemetry (power draw, temperature, performance counters) reliably distinguish cryptojacking from legitimate high-utilization AI training workloads without unacceptable false positive rates?
- [ ] As model sizes continue to grow (potentially multi-terabyte weights), how should disaster recovery strategies adapt when network transfer times dominate RTO? Pre-staged warm replicas across regions may become mandatory for critical inference services.
- [ ] How should organizations handle backup and recovery for agentic AI systems where state includes not just model weights but also tool configurations, memory stores, and active execution context?
- [ ] GPUHammer demonstrated that GDDR6 GPU memory is vulnerable to Rowhammer bit-flip attacks that can silently corrupt model weights. Should cloud providers mandate ECC-capable GPUs (HBM3, GDDR7) for multi-tenant AI inference, and how should integrity verification of in-memory model weights be performed at runtime without unacceptable latency overhead?

---
