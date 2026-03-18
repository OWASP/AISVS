# C04: Infrastructure, Configuration & Deployment Security

> **Source:** [`1.0/en/0x10-C04-Infrastructure.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C04-Infrastructure.md)
> **Requirements:** 46 | **Sections:** 8

## Control Objective

AI infrastructure must be hardened against privilege escalation, supply chain tampering, and lateral movement through secure configuration, runtime isolation, trusted deployment pipelines, and comprehensive monitoring.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C4.1 | Runtime Environment Isolation | 5 | 4.1.1–4.1.5 |
| C4.2 | Secure Build & Deployment Pipelines | 4 | 4.2.1–4.2.4 |
| C4.3 | Network Security & Access Control | 5 | 4.3.1–4.3.5 |
| C4.4 | Secrets & Cryptographic Key Management | 5 | 4.4.1–4.4.5 |
| C4.5 | AI Workload Sandboxing & Validation | 7 | 4.5.1–4.5.7 |
| C4.6 | AI Infrastructure Resource Management, Backup and Recovery | 3 | 4.6.1–4.6.3 |
| C4.7 | AI Hardware Security | 8 | 4.7.1–4.7.8 |
| C4.8 | Edge & Distributed AI Security | 9 | 4.8.1–4.8.9 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- GPU side-channel attacks (leaking model weights or data from shared GPU memory)
- Container escape from AI workloads gaining host access
- Supply chain compromise of ML framework dependencies (PyTorch, TensorFlow packages)
- Lateral movement from compromised inference endpoints to training infrastructure
- Edge device tampering or model extraction from on-device deployments

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Container isolation:** gVisor, Kata Containers, Firecracker for AI workloads
- **GPU security:** NVIDIA MIG (Multi-Instance GPU), Confidential Computing (AMD SEV, Intel TDX)
- **Secrets management:** HashiCorp Vault, AWS Secrets Manager, Azure Key Vault
- **Network security:** Cilium, Calico for Kubernetes network policies
- **Edge deployment:** ONNX Runtime with TEE, TFLite with attestation

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C4.1 Runtime Environment Isolation | _TBD_ | |
| C4.2 Secure Build & Deployment Pipelines | _TBD_ | |
| C4.3 Network Security & Access Control | _TBD_ | |
| C4.4 Secrets & Cryptographic Key Management | _TBD_ | |
| C4.5 AI Workload Sandboxing & Validation | _TBD_ | |
| C4.6 AI Infrastructure Resource Management, Backup and Recovery | _TBD_ | |
| C4.7 AI Hardware Security | _TBD_ | |
| C4.8 Edge & Distributed AI Security | _TBD_ | |

---

## Open Research Questions

- [ ] What's the maturity of confidential computing for GPU workloads?
- [ ] How do you isolate multi-tenant GPU workloads without significant performance overhead?
- [ ] What are the best practices for securing AI inference at the edge with limited compute?
- [ ] How should hardware security requirements differ for training vs. inference infrastructure?

---

## Related Standards & Cross-References

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [CIS Controls v8](https://www.cisecurity.org/controls/v8)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Cloud Security Alliance: Cloud Controls Matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix/)
- [ENISA: Secure Infrastructure Design](https://www.enisa.europa.eu/topics/critical-information-infrastructures-and-services)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

