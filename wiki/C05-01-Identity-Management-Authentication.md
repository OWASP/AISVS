# C5.1: Identity Management & Authentication

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-03-29

## Purpose

Establish verified identities for all entities interacting with AI systems, with authentication strength appropriate to the risk level. AI systems introduce identity challenges beyond traditional web applications: model-serving endpoints, inference APIs, and model registries often bypass centralized identity providers in favor of standalone API keys. In multi-agent and federated deployments, agent identity itself is an emerging concern -- short-lived, cryptographically signed tokens are needed to prevent impersonation and replay attacks across agent boundaries.

> **Scope note:** Controls in this section govern the identity and authentication layer for humans, services, and AI agents accessing AI system resources. Authorization policies, access control enforcement, and output-level filtering are addressed in C5.2-C5.6.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.1.1** | **Verify that** all human users and service principals authenticate through a centralized identity provider using industry-standard federation protocols (e.g., OIDC, SAML). | 1 | Credential sprawl and inconsistent authentication enforcement across AI endpoints; lateral movement via compromised local accounts. | Confirm IdP integration in architecture diagrams; test that direct API access without IdP-issued tokens is rejected; review service principal registrations in the IdP. | Standard practice for web applications; the AI-specific nuance is ensuring model-serving endpoints (e.g., inference APIs, model registries) are behind the same IdP rather than using separate API keys. **[2026-03]** 93% of audited AI agent projects still use unscoped API keys rather than IdP-issued tokens (Grantex State of Agent Security 2026). The Feb 2026 Google Cloud API key exposure (2,863 live keys found in client-side code, granting Gemini access) demonstrates the risk of API-key-only authentication for AI endpoints. |
| **5.1.2** | **Verify that** high-risk operations (model deployment, weight export, training data access, production configuration changes) require multi-factor authentication or step-up authentication with session re-validation. | 2 | Stolen session tokens used to exfiltrate model weights or poison training data; insider threats performing high-impact changes with passive credentials. | Trigger each high-risk operation and confirm MFA challenge is presented; verify session re-validation timestamps in audit logs; test that expired step-up sessions are denied. | Defining the boundary of "high-risk" is organization-specific. Model weight export and training data access are AI-specific high-value targets not typically covered by general MFA policies. **[2026-03]** The Jul 2025 xAI/Grok incident (DOGE staffer committed API key to public GitHub, exposing 52 LLMs) shows how a single compromised credential without step-up auth can expose entire model inventories. Grantex recommends optional FIDO2/WebAuthn passkeys for high-risk AI operations. |
| **5.1.3** | **Verify that** AI agents in federated or multi-system deployments authenticate via short-lived, cryptographically signed authentication tokens (e.g., signed JWT assertions) with a maximum lifetime appropriate to the risk level and including cryptographic proof of origin. | 3 | Agent impersonation in multi-agent orchestration; token replay attacks enabling unauthorized agent actions; long-lived credentials being exfiltrated from agent memory. | Inspect token lifetimes and signing algorithms; verify token rotation occurs before expiry; test that expired or tampered tokens are rejected; confirm proof-of-origin claims (e.g., SPIFFE IDs) are validated. | Multi-agent identity is an emerging area. SPIFFE/SPIRE provides workload identity but agent-level granularity is still maturing. Token lifetime guidance varies; NIST SP 800-63B suggests risk-proportionate session timeouts. **[2026-03]** NIST NCCoE released concept paper (Feb 2026) "Accelerating the Adoption of Software and AI Agent Identity and Authorization" proposing practical guidance for enterprise AI agent identity. OpenID Connect for Agents (OIDC-A) 1.0 proposal published Apr 2025 extends OIDC with agent-specific claims. ARIA (Agent Relationship-Based Identity and Authorization) model tracks delegation as cryptographically verifiable graph entities. Microsoft is extending OAuth 2.0 token exchange with on-behalf-of profile specifically for AI agent delegation chains. The IETF draft `draft-oauth-ai-agents-on-behalf-of-user` (draft-02, 2025) introduces `requested_actor` and `actor_token` parameters for OAuth 2.0, enabling explicit user consent for agent delegation with JWT `act` claims that document the full delegation chain. Auth0 Token Vault (GA Jan 2026) implements RFC 8693 token exchange for AI agents with 30+ pre-integrated providers, keeping long-lived provider credentials off agent infrastructure. |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
