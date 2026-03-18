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

## Related Standards & References

- [NIST SP 800-184: Guide for Cybersecurity Event Recovery](https://csrc.nist.gov/publications/detail/sp/800-184/final)
- [CIS Controls v8 -- Control 11: Data Recovery](https://www.cisecurity.org/controls/data-recovery)
- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [NVIDIA MIG User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/)
- [AWS S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

---

## Open Research Questions

- [ ] How should resource quotas account for the variable compute cost of different inference requests (short vs. long sequences, simple vs. complex generation)?
- [ ] What is the optimal checkpoint frequency for long-running training jobs balancing storage cost against potential recompute cost?
- [ ] How can WORM-protected backups handle the iterative nature of model development where old checkpoints are regularly superseded?

---
