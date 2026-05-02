# C5.1: Authentication

> [Back to C05 Index](C05-Access-Control.md)
> **Last Researched:** 2026-05-02

## Purpose

Establish verified identities for all entities interacting with AI systems, with authentication strength appropriate to the risk level. AI systems introduce identity challenges beyond traditional web applications: model-serving endpoints, inference APIs, model registries, and agent tool gateways often bypass centralized identity providers in favor of standalone API keys. In multi-agent and federated deployments, agent identity itself is now a first-order control: short-lived, cryptographically signed credentials must identify both the workload and the user delegation path so compromised agents cannot replay broad bearer tokens across systems.

> **Scope note:** Controls in this section govern the authentication layer for humans, services, and AI agents accessing AI system resources. Resource authorization, query-time enforcement, output entitlement enforcement, PDP isolation, and multi-tenant isolation are addressed in C5.2–C5.6. General identity management, federation, and MFA patterns are covered by ASVS v5 V6; this chapter addresses AI-specific concerns that ASVS does not cover.

---

## Requirements

| # | Requirement | Level | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|-----------------|----------------------|--------------|
| **5.1.1** | **Verify that** high-risk AI operations (model deployment, weight export, training data access, production configuration changes) require step-up authentication with session re-validation. | 2 | Stolen session tokens used to exfiltrate model weights or poison training data; insider threats performing high-impact changes with passive credentials; OAuth device-code phishing that grants attackers valid tokens even when MFA is enabled; static API keys leaked from model tooling, MCP configs, notebooks, deleted forks, or CI/CD logs; compromised CI/CD pipelines issuing unauthorized production changes. MITRE ATLAS AML.T0024 (Exfiltration via ML Inference API), AML.T0010 (ML Supply Chain Compromise). | Trigger each high-risk operation (model registry push, weight download, training-data bucket read, production config change) and confirm a fresh MFA challenge is presented; verify session re-validation timestamps in audit logs and that elevated sessions carry a shorter TTL than base sessions; test that expired step-up sessions are denied without silent downgrade; confirm phishing-resistant authenticator is enforced (FIDO2 security key, managed device-bound passkey, or equivalent AAL3 authenticator) rather than SMS/TOTP; inspect IdP policy using Okta Identity Engine, Auth0 Adaptive MFA, Microsoft Entra Conditional Access, or Ping DaVinci to confirm re-authentication frequency and authenticator-class constraints; in Entra-backed deployments, map high-risk methods to Conditional Access authentication context IDs and verify the API raises a claims challenge when the `acrs` claim is missing; review authentication-flow policies and block OAuth device-code flow except for documented, network-bounded device scenarios; run secret scanning across model registries, MCP configuration files, notebooks, and CI logs before granting step-up bypass exceptions. | Defining "high-risk" remains organization-specific. Model weight export and training-data access are AI-specific high-value targets not typically covered by general MFA policies — they need to be explicitly enumerated in Conditional Access / policy-as-code. **[2026-05]** NIST SP 800-63B AAL3 requires phishing-resistant cryptographic authenticators with non-exportable private keys; syncable passkeys are explicitly not AAL3 because their keys are exportable. AAL3 is the baseline recommendation for model-weight export and training-pipeline write access. Microsoft's April 2026 device-code phishing research and Huntress' March 2026 Railway.com campaign both show that device-code flows can hand attackers valid OAuth tokens without defeating the user's MFA factor, so step-up paths should not permit device-code authentication. GitGuardian's 2026 State of Secrets Sprawl reported 28.65M new hardcoded secrets in public GitHub commits during 2025, 1.27M AI-service secrets, and 24,008 unique secrets in MCP-related config files; Wiz found verified secret leaks in 65% of Forbes AI 50 companies with GitHub footprints, including cases exposing private models. The Jul 2025 xAI/Grok key leak, the 2024 Hugging Face 1,500+ exposed-token incident, Truffle Security's 2025 Common Crawl credential findings, and the Mercor/LiteLLM compromise all point to the same failure mode: static credentials and weak re-authentication collapse quickly when model infrastructure is treated like a normal SaaS app. |
| **5.1.2** | **Verify that** AI agents in federated or multi-system deployments authenticate via short-lived, cryptographically signed authentication tokens (e.g., signed JWT assertions) with a maximum lifetime appropriate to the risk level and including cryptographic proof of origin. | 3 | Agent impersonation in multi-agent orchestration; token replay attacks enabling unauthorized agent actions; long-lived credentials being exfiltrated from agent memory, traces, prompt logs, or local tool configs; confused-deputy attacks where a compromised MCP proxy reuses a broadly-scoped static client credential; token-passthrough attacks where an MCP server forwards a token it was never issued. MITRE ATLAS AML.T0051 (LLM Prompt Injection) chained with agent-identity abuse; OWASP LLM09 (Excessive Agency). | Inspect token lifetimes and signing algorithms (reject `alg: none`, prefer EdDSA/ES256 over RS256 where feasible); verify token rotation occurs well before expiry; test that expired or tampered tokens are rejected with a clock-skew tolerance no wider than 60s; confirm proof-of-origin claims (SPIFFE IDs, `iss`/`aud` pair, `cnf`/JWK binding, x5t#S256 binding, or WIMSE Workload Identity Token confirmation claims) are validated on every hop; verify application-layer proof-of-possession where supported, such as WIMSE Workload Proof Token or HTTP Message Signatures, and reject WITs presented as bearer tokens; check that `act` or equivalent delegation claims document the user, client, and agent chain; audit MCP servers to ensure they refuse tokens not explicitly issued with the MCP server in the `aud` claim and obtain separate downstream tokens instead of passing user tokens through; run `step certificate inspect` against SPIRE-issued SVIDs to confirm lifetime ≤ a few minutes for JWT-SVIDs and ≤ a few hours for X.509-SVIDs; verify incremental/progressive scope elevation rather than omnibus scopes. | Multi-agent identity is maturing quickly, but the standards set is still uneven. SPIFFE/SPIRE provides workload identity with short-lived JWT-SVID and X.509-SVID formats that auto-rotate, while the April 2026 WIMSE drafts split workload authentication into concrete credential and protocol pieces: Workload Identity Tokens (WITs) and Workload Identity Certificates (WICs) identify workloads, and proof-of-possession is supplied through WPT, HTTP signatures, or transport-level mutual TLS. **[2026-05]** NIST NCCoE's concept paper on software and AI agent identity names MCP, OAuth 2.0/2.1, OpenID Connect, SPIFFE/SPIRE, SCIM, and NGAC as candidate standards mapped against SP 800-207 Zero Trust and SP 800-63-4; the comment period closed on 2026-04-02. The individual IETF OAuth on-behalf-of AI agents draft expired on 2026-02-27, so treat its `requested_actor` / `actor_token` pattern as useful design input rather than a current standard. Auth0 Token Vault implements RFC 8693 token exchange for agents, keeping long-lived provider credentials off agent infrastructure and issuing short-lived scoped tokens per transaction; HashiCorp Vault's dynamic-secrets pattern for AI agents offers an on-prem alternative with user attribution, OBO token exchange, JWT auth, dynamic credentials, and audit correlation. The 2026 MCP authorization specification mandates OAuth 2.1, PKCE, resource-indicator binding (RFC 8707), per-client consent to prevent confused-deputy attacks against proxy servers, and incremental scope consent; token passthrough is explicitly forbidden. Gaps remain: agent-level granularity inside a single workload is still workload-coarse in SPIFFE; production support for WIMSE WIT/WPT is early; and tooling to verify delegation-chain claims end-to-end remains scarce outside Auth0, Okta/Auth0 agent identity offerings, Keycloak/Ory customization, and gateway-specific implementations. |

---

## Implementation Notes

**High-risk operation inventory.** Maintain a machine-readable list of operations that always require step-up: model-weight export, production model deployment, training-pipeline write access, dataset export, model-registry admin changes, inference endpoint key creation, and production agent tool permission changes. The list should be owned jointly by security and the model platform team, not buried in application code.

**Device-code flow boundary.** Device-code authentication is useful for constrained devices, but it is a poor fit for high-risk AI administration because the user authorizes an attacker-controlled session on a legitimate identity-provider page. Where the IdP supports it, block device-code flow globally and allow it only for documented device classes, managed networks, and non-administrative resources.

**Non-human identity lifecycle.** Every agent, model-serving workload, CI/CD job, and MCP server should have an owner, an issuance path, a rotation schedule, and a revocation path. Prefer workload identity, token exchange, and dynamic secrets over API keys stored in environment variables or local agent configuration files.

**Audit evidence.** For humans, preserve the auth context / ACR value, authenticator class, step-up timestamp, operation name, and session expiry. For agents, preserve issuer, audience, subject, proof-of-possession status, delegated user or actor chain, token exchange event ID, and downstream credential lease ID where available.

---

## Key References

- [NIST SP 800-63-4: Digital Identity Guidelines (final, July 2025)](https://csrc.nist.gov/pubs/sp/800/63/4/final)
- [NIST SP 800-63B: Authentication Assurance Level 3](https://pages.nist.gov/800-63-4/sp800-63b/aal/)
- [NIST SP 800-63B: Syncable Authenticators](https://pages.nist.gov/800-63-4/sp800-63b/syncable/)
- [NIST NCCoE Concept Paper: Accelerating the Adoption of Software and AI Agent Identity and Authorization (Feb 2026)](https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd)
- [NCCoE project page: Software and AI Agent Identity and Authorization](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization)
- [Microsoft Entra Conditional Access authentication flows](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-authentication-flows)
- [Microsoft Entra Conditional Access authentication context developer guide](https://learn.microsoft.com/en-us/entra/identity-platform/developer-guide-conditional-access-authentication-context)
- [Okta Identity Engine: Phishing-resistant authentication](https://help.okta.com/oie/en-us/content/topics/identity-engine/authenticators/phishing-resistant-auth.htm)
- [IETF draft-oauth-ai-agents-on-behalf-of-user (expired individual draft)](https://datatracker.ietf.org/doc/draft-oauth-ai-agents-on-behalf-of-user/)
- [IETF WIMSE architecture draft](https://datatracker.ietf.org/doc/draft-ietf-wimse-arch/)
- [IETF WIMSE Workload Credentials draft (April 2026)](https://ietf-wg-wimse.github.io/draft-ietf-wimse-s2s-protocol/draft-ietf-wimse-workload-creds.html)
- [IETF WIMSE Workload-to-Workload Authentication draft (April 2026)](https://ietf-wg-wimse.github.io/draft-ietf-wimse-s2s-protocol/draft-ietf-wimse-s2s-protocol.html)
- [IETF WIMSE Workload Proof Token draft](https://datatracker.ietf.org/doc/html/draft-ietf-wimse-wpt-01)
- [SPIFFE/SPIRE documentation](https://spiffe.io/docs/latest/spire-about/spire-concepts/)
- [RFC 8693: OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693)
- [RFC 8707: Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707)
- [Model Context Protocol Authorization](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Model Context Protocol Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [Auth0 Token Vault for AI Agents](https://auth0.com/ai/docs/intro/token-vault)
- [HashiCorp Vault dynamic secrets for AI agents](https://developer.hashicorp.com/validated-patterns/vault/ai-agent-identity-with-hashicorp-vault)
- [ARIA Protocol — open standard for AI agent identity and verification](https://www.aria.bar/)
- [Microsoft Security Blog: AI-enabled device code phishing campaign (April 2026)](https://www.microsoft.com/en-us/security/blog/2026/04/06/ai-enabled-device-code-phishing-campaign-april-2026/)
- [Huntress: Railway.com PaaS as Microsoft 365 token attack infrastructure](https://www.huntress.com/blog/railway-paas-m365-token-replay-campaign)
- [GitGuardian: The State of Secrets Sprawl 2026](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/)
- [Wiz: 65% of Forbes AI 50 companies found with verified secret leaks](https://www.wiz.io/blog/forbes-ai-50-leaking-secrets)
- [Lasso Security: 1,500+ Hugging Face API tokens exposed](https://www.lasso.security/blog/1500-huggingface-api-tokens-were-exposed-leaving-millions-of-meta-llama-bloom-and-pythia-users-for-supply-chain-attacks)

---

## Related Pages

- [C10.2 Authentication & Authorization](../C10-MCP-Security/C10-02-Authentication-Authorization.md) — applies the OAuth, audience-binding, and token-passthrough rules to MCP clients, servers, and gateways.
- [C9.6 Authorization and Delegation](../C09-Orchestration-and-Agents/C09-06-Authorization-and-Delegation.md) — covers the downstream delegation and policy enforcement questions that start after an agent has authenticated.
- [C9.4 Agent Identity and Audit](../C09-Orchestration-and-Agents/C09-04-Agent-Identity-and-Audit.md) — expands the cryptographic identity and audit evidence expected for multi-agent systems.
- [C5.2 AI Resource Authorization & Classification](C05-02-Authorization-Policy.md) — defines how authenticated users and agents are authorized to access models, datasets, endpoints, and derived AI resources.

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---
