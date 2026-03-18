# C11.7: Security Policy Adaptation

> **Chapter:** [C11 Adversarial Robustness & Attack Resistance](C11-Adversarial-Robustness)
> **Requirements:** 4 | **IDs:** 11.7.1--11.7.4

## Purpose

Enable real-time security policy updates based on threat intelligence and behavioral analysis. AI systems face a dynamic threat landscape where new attack techniques emerge frequently. The ability to update security policies (content filters, rate limits, guardrail configurations, detection thresholds) without full system redeployment is essential for rapid response. This section ensures that policy updates are fast, controlled, auditable, and protected against tampering.

---

## Requirements

| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| **11.7.1** | **Verify that** security policies (e.g., content filters, rate-limit thresholds, guardrail configurations) can be updated without full system redeployment, and that policy versions are tracked. | 1 | D/V | Slow response to emerging threats due to heavyweight deployment cycles. If updating a content filter requires a full model redeployment (hours to days), the system is vulnerable during the gap. Version tracking prevents configuration drift and enables rollback. | Review system architecture for policy update mechanisms (hot-reload, feature flags, configuration management systems). Verify that policy changes can be applied within an acceptable time window (minutes, not hours). Check version tracking system for policy configurations. Test a policy update end-to-end and confirm it takes effect without system restart. | "Without full system redeployment" does not mean without any deployment -- canary or staged rollouts of policy changes are acceptable and encouraged. Policy update mechanisms themselves become an attack surface (see 11.7.2). The distinction between "policy" and "model" updates should be clearly defined -- model updates inherently require redeployment. |
| **11.7.2** | **Verify that** policy updates are authorized, integrity-protected (e.g., cryptographically signed), and validated before application. | 2 | D/V | Unauthorized or tampered policy modifications that weaken security controls. An attacker who can modify policies can disable content filters, raise rate limits, or weaken guardrails -- effectively disarming the system without touching the model. Supply-chain attacks on policy configuration repositories. | Review authorization controls for policy updates (RBAC, approval workflows, MFA requirements). Verify cryptographic signing of policy artifacts (who signs, key management, signature verification in the deployment pipeline). Test that unsigned or improperly signed policies are rejected. Verify that validation includes schema checks, constraint verification, and sanity testing before application. | Cryptographic signing adds operational complexity. Organizations need policy signing infrastructure that may not exist. Validation must check for internally consistent policies -- a "valid" policy that disables all content filters should be caught by constraint checks. Consider requiring dual authorization for high-impact policy changes (e.g., disabling a content filter category). |
| **11.7.3** | **Verify that** policy changes are logged with audit trails including timestamp, author, justification, and rollback procedures. | 2 | D/V | Unaccountable policy changes that cannot be investigated after an incident. Without audit trails, it is impossible to determine whether a security failure resulted from a policy change, who authorized it, or why. Supports forensic investigation and regulatory compliance. | Review audit log schema for policy changes. Verify completeness: timestamp, author identity, justification/ticket reference, before/after policy state, rollback procedure reference. Test that policy changes generate audit entries. Verify audit logs are tamper-protected (append-only, separate storage, integrity verification). Check that rollback procedures are documented and tested. | Audit trails must be integrated with the organization's broader security logging infrastructure (C13). Justification fields should reference change tickets or incident IDs, not free-text explanations. Rollback procedures should be tested periodically, not just documented. Consider automated rollback triggers (e.g., if a policy change causes a spike in blocked legitimate requests). |
| **11.7.4** | **Verify that** threat-detection sensitivity can be adjusted based on risk context (e.g., elevated threat level, incident response) with appropriate authorization. | 3 | D/V | Inability to respond proportionally to elevated threat conditions. During an active attack or incident, organizations may need to tighten detection thresholds, enable additional monitoring, or restrict capabilities -- and relax them when the threat passes. Static sensitivity creates a binary choice between too permissive and too restrictive. | Review risk-context mechanisms: threat-level definitions, sensitivity profiles for each level, authorization requirements for level changes. Verify that sensitivity adjustments are reversible and time-bounded (auto-revert to baseline after a defined period). Test sensitivity adjustment end-to-end. Verify that elevated sensitivity levels are logged and subject to the same audit requirements as other policy changes. | Risk-context-based sensitivity adjustment is conceptually sound but operationally complex. Defining threat levels and mapping them to specific sensitivity changes requires careful analysis. Overly aggressive sensitivity during elevated threat levels may cause service degradation. Auto-revert timers prevent "elevated mode" from becoming permanent through inertia. |

---

## Related Standards & References

- [NIST SP 800-53 -- SI-4 System Monitoring](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) -- Adaptive monitoring and threat response controls
- [NIST CSF -- Respond Function](https://www.nist.gov/cyberframework) -- Incident response and adaptive security posture
- [OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) -- Rate limiting and resource control

---

## Open Research Questions

- How should AI-specific security policies be structured for hot-reload -- what is the right abstraction layer between model behavior and configurable policy?
- Can policy updates themselves be tested automatically before deployment (policy-as-code with automated safety validation)?
- What threat-level frameworks are appropriate for AI systems -- should they align with organizational SOC threat levels or have AI-specific escalation criteria?
- How do you prevent policy update mechanisms from becoming an attack vector themselves (e.g., an attacker compromising the policy signing key)?
- What is the appropriate granularity for policy versioning -- per-parameter, per-policy-document, or per-deployment?

---
