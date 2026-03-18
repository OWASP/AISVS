# C4.3 Network Security & Access Control

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Implement zero-trust networking with default-deny policies and encrypted communications. AI infrastructure has a uniquely large attack surface: inference endpoints are internet-facing, training clusters require high-bandwidth interconnects, model registries hold high-value intellectual property, and data pipelines span multiple network zones. This section ensures that network architecture limits blast radius and prevents lateral movement even when individual components are compromised.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.3.1** | Verify that network policies enforce default-deny ingress and egress, with only required services explicitly allowed. | 1 | D/V | Lateral movement from a compromised inference pod to internal services (model registry, training data stores, metadata services). Unauthorized data exfiltration from training workloads. | Inspect Kubernetes NetworkPolicy resources for `policyTypes: [Ingress, Egress]` with empty default rules. Verify with network scanning tools (nmap) that unlisted ports/destinations are unreachable. Test that newly deployed pods without explicit policies cannot reach any services. | Kubernetes NetworkPolicy alone does not cover all cases -- it requires a CNI that supports it (Calico, Cilium, Antrea). AWS Security Groups and VPC NACLs are a separate layer. AI workloads often need broad egress for pulling model weights or datasets during initialization -- these should be time-limited or handled via init containers with different network policies. |
| **4.3.2** | Verify that AI workloads across environments (development, testing, production) run in isolated network segments with no direct internet access and no shared identity roles, security groups, or cross-environment connectivity. | 1 | D/V | Development environment compromise leading to production access. Staging models trained on production data being accessible from dev networks. Shared IAM roles allowing cross-environment privilege escalation. | Verify separate VPCs/VNets per environment with no peering. Confirm distinct IAM roles/service accounts per environment. Attempt cross-environment network access and confirm failure. Audit security group membership for cross-environment overlap. | Common anti-pattern: sharing a model registry across environments with the same credentials. Each environment should have its own registry or use separate credentials with read-only access for lower environments. GPU clusters are often shared across environments due to cost -- this must be mitigated with strong logical isolation. |
| **4.3.3** | Verify that administrative and remote access protocols and access to cloud metadata services are restricted and require strong authentication. | 1 | D/V | SSRF attacks from ML workloads accessing cloud metadata services (IMDSv1 on AWS returning IAM credentials). Unauthorized SSH/RDP access to GPU nodes. Kubectl access without proper RBAC. | Confirm IMDSv2 is enforced (hop limit = 1, PUT required) or metadata service is blocked. Verify SSH/RDP requires MFA or certificate-based auth. Check that Kubernetes API access uses RBAC with least privilege. Audit admin access logs for anomalies. | IMDSv1 SSRF is a well-documented attack vector. ML workloads are particularly vulnerable because they often process untrusted input that could be crafted to trigger SSRF. Jupyter notebooks with internet access and IMDS access are a common high-risk combination. Block metadata endpoints from all workload pods unless explicitly needed. |
| **4.3.4** | Verify that inter-service communication uses mutual TLS with certificate validation and regular automated rotation. | 2 | D/V | Man-in-the-middle attacks on model serving traffic. Interception of model weights during transfer between training and serving infrastructure. Spoofed inference endpoints returning manipulated results. | Verify service mesh (Istio, Linkerd) or application-level mTLS is configured. Check certificate rotation frequency (should be < 24 hours for short-lived certs). Confirm certificate validation is strict (no `verify=False` or `InsecureSkipVerify`). Test with expired or wrong-CA certificates. | Service mesh mTLS is straightforward for HTTP-based inference APIs but more complex for gRPC model serving (TensorFlow Serving, Triton) and custom protocols. High-bandwidth training interconnects (NCCL, Gloo) may not support mTLS natively -- consider network-level encryption (WireGuard, IPsec) as an alternative for training cluster traffic. |
| **4.3.5** | Verify that egress traffic is restricted to approved destinations and all requests are logged. | 3 | D/V | Data exfiltration of model weights or training data via DNS tunneling, HTTPS to attacker-controlled servers, or cloud storage APIs. Command-and-control communication from compromised workloads. | Configure egress proxy (Squid, Envoy) or cloud-native egress controls (AWS VPC endpoints, Azure Private Link). Verify DNS resolution is controlled and logged. Confirm logging captures destination, payload size, and source workload identity. Test with unauthorized egress attempts. | ML workloads frequently need to download large files (model weights, datasets) from external sources like HuggingFace Hub, PyPI, or cloud storage. Approved destination lists must be maintained and should use domain-based (FQDN) filtering, not just IP-based. DNS-over-HTTPS from within containers can bypass DNS-based filtering -- consider blocking DoH endpoints. |

---

## Related Standards & References

- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Cilium Network Policy documentation](https://docs.cilium.io/en/stable/security/policy/)
- [AWS IMDSv2 requirements](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)
- [NIST SP 800-204A: Building Secure Microservices-based Applications Using Service-Mesh Architecture](https://csrc.nist.gov/publications/detail/sp/800-204a/final)

---

## Open Research Questions

- [ ] How can network policies be dynamically adjusted for ML training jobs that have different network requirements during data loading vs. training phases?
- [ ] What is the performance impact of mTLS on high-throughput inference endpoints serving thousands of requests per second?
- [ ] How should egress policies handle legitimate ML workflow needs (pulling models from HuggingFace Hub, accessing cloud APIs) without overly broad allowlists?
- [ ] Can eBPF-based network observability tools (Hubble, Retina) provide sufficient visibility for detecting anomalous ML workload communication patterns?

---
