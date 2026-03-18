# C4.4 Secrets & Cryptographic Key Management

[Back to C04 Index](C04-Infrastructure.md)

## Purpose

Protect secrets and cryptographic keys with secure storage, automated rotation, and strong access controls. AI systems manage a wide variety of sensitive credentials: API keys for model providers, database credentials for training data stores, signing keys for model artifacts, encryption keys for model weights, and service account tokens for cloud resources. Compromise of any of these can lead to data theft, model tampering, or unauthorized access to expensive GPU infrastructure.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **4.4.1** | Verify that secrets are stored in a dedicated secrets management system with encryption at rest and isolated from application workloads. | 1 | D/V | Secrets exposed through container image layers, configuration files, or application logs. Compromise of one workload leading to access to all secrets. | Confirm use of a secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager). Verify encryption at rest is enabled (check KMS key configuration). Confirm the secrets store runs in a separate network segment from AI workloads. | ML notebooks (Jupyter, Colab) are a common source of leaked secrets -- developers embed API keys directly in notebook cells. Secrets management integration with notebook environments is immature. Consider pre-commit hooks (detect-secrets, truffleHog) to catch secrets before they reach version control. |
| **4.4.2** | Verify that access to production secrets requires strong authentication. | 1 | D/V | Unauthorized access to production model serving keys, training data encryption keys, or cloud provider credentials. Insider threat from developers with overly broad access. | Verify authentication to the secrets manager uses MFA or certificate-based auth for human access. Confirm workload identity (IRSA, Workload Identity, pod identity) is used for service access rather than long-lived credentials. Audit access logs for anomalous patterns. | AI workloads often run as shared service accounts with broad secrets access. Use fine-grained policies: inference services should not access training data encryption keys. Vault policies or AWS IAM conditions should scope access by workload identity, not just by role. |
| **4.4.3** | Verify that secrets are deployed to applications at runtime through a dedicated secrets management system. Secrets must never be embedded in source code, configuration files, build artifacts, container images, or environment variables. | 1 | D/V | Secrets leaking through container image layers (recoverable via `docker history`), git history, CI/CD logs, or process environment dumps (`/proc/*/environ`). | Scan container images for embedded secrets (Trivy, Syft). Search git history for secrets patterns. Verify secrets are injected via volume mounts (Vault Agent, CSI driver) or API calls, not environment variables. Check CI/CD logs for secret masking. | Environment variables are explicitly excluded because they appear in process listings, crash dumps, and debug logs. The Kubernetes Secrets CSI driver or Vault Agent sidecar are preferred injection mechanisms. Note: many ML frameworks read API keys from environment variables by default (e.g., `OPENAI_API_KEY`, `HF_TOKEN`) -- wrappers may be needed to read from mounted secret files instead. |
| **4.4.4** | Verify that cryptographic keys are generated and stored in hardware-backed modules (e.g., HSMs, cloud KMS). | 2 | D/V | Key extraction from software keystores via memory dumps, cold boot attacks, or host compromise. Weak key generation from poor entropy sources. | Verify KMS or HSM is used for key generation (not `openssl genrsa` on a dev machine). Check that keys are non-exportable from HSMs. Confirm cloud KMS keys use HSM-backed key types (AWS KMS with CloudHSM, Azure Managed HSM, GCP Cloud HSM). | Applicable to model signing keys, data encryption keys, and TLS certificate private keys. For AI-specific use cases: model weight encryption keys and inference API authentication keys should use HSM-backed storage. Cloud KMS services provide a practical middle ground between software keystores and dedicated HSMs. |
| **4.4.5** | Verify that secrets rotation is automated. | 2 | D/V | Long-lived credentials remaining valid after team member departure, credential leak, or periodic compromise. Difficulty determining blast radius of a compromised credential when rotation history is unclear. | Verify automated rotation is configured (Vault dynamic secrets, AWS Secrets Manager rotation lambdas). Check rotation frequency is appropriate (database credentials: 30-90 days; API keys: 90 days; certificates: < 24 hours for short-lived). Confirm rotation does not cause downtime. | Dynamic secrets (Vault, AWS STS) are preferred over static secrets with rotation. For ML-specific credentials: model provider API keys (OpenAI, Anthropic) may not support automated rotation via API -- manual rotation workflows need documentation. GPU cloud provider credentials (Lambda Labs, CoreWeave) may have limited rotation API support. |

---

## Related Standards & References

- [NIST SP 800-57: Recommendation for Key Management](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [HashiCorp Vault documentation](https://developer.hashicorp.com/vault/docs)
- [CIS Benchmark for Kubernetes -- Secrets section](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST SP 800-63B: Digital Identity Guidelines -- Authentication](https://pages.nist.gov/800-63-3/sp800-63b.html)

---

## Open Research Questions

- [ ] How should secrets management handle the unique lifecycle of ML experiment tracking credentials (many short-lived experiments across multiple researchers)?
- [ ] What is the best practice for managing API keys to external model providers (OpenAI, Anthropic, etc.) where the provider's rotation API support varies?
- [ ] How can secrets injection work seamlessly with distributed training frameworks (Horovod, DeepSpeed) that spawn processes across multiple nodes?

---
