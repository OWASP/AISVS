<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x91-Appendix-B_AI_Security_Controls_Inventory.md -->
<!-- Translator: GeeksikhSecurity -->

# Appendix B: AI Security Controls Inventory
# ਅੰਤਿਕਾ[^0x91-appendix] B: AI ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣ ਇਨਵੈਂਟਰੀ

## Objective
## ਉਦੇਸ਼

This appendix is a consolidated, developer-facing inventory of the security controls mandated across the AISVS requirements. Controls are grouped by control family so an implementer can find all related defenses in one place, regardless of which chapter defines them, and each control links back to the AISVS requirement IDs that mandate it.

ਇਹ ਅੰਤਿਕਾ AISVS ਦੀਆਂ ਲੋੜਾਂ ਵਿੱਚ ਲਾਜ਼ਮੀ ਕੀਤੇ ਗਏ ਸੁਰੱਖਿਆ ਨਿਯੰਤਰਣਾਂ ਦੀ ਇੱਕ ਇਕੱਠੀ ਕੀਤੀ ਹੋਈ, ਡਿਵੈਲਪਰ-ਮੁਖੀ ਇਨਵੈਂਟਰੀ ਹੈ। ਨਿਯੰਤਰਣਾਂ ਨੂੰ ਨਿਯੰਤਰਣ ਪਰਿਵਾਰ (control family) ਅਨੁਸਾਰ ਸਮੂਹਬੱਧ ਕੀਤਾ ਗਿਆ ਹੈ ਤਾਂ ਜੋ ਲਾਗੂ ਕਰਨ ਵਾਲਾ ਸਾਰੇ ਸੰਬੰਧਿਤ ਬਚਾਅ ਇੱਕੋ ਥਾਂ ਲੱਭ ਸਕੇ, ਭਾਵੇਂ ਉਹਨਾਂ ਨੂੰ ਕੋਈ ਵੀ ਅਧਿਆਇ ਪਰਿਭਾਸ਼ਿਤ ਕਰਦਾ ਹੋਵੇ, ਅਤੇ ਹਰ ਨਿਯੰਤਰਣ ਉਹਨਾਂ AISVS ਲੋੜ ID ਨਾਲ ਵਾਪਸ ਜੁੜਦਾ ਹੈ ਜੋ ਉਸ ਨੂੰ ਲਾਜ਼ਮੀ ਕਰਦੇ ਹਨ।

This inventory is non-normative. It reorganizes existing requirements for ease of implementation and does not add, remove, or change any requirement. The requirement chapters (C1 through C12) remain the source of truth. Requirement IDs are written in canonical `C{chapter}.{section}.{requirement}` form (for example, `C5.1.1`). Every numbered requirement in the standard appears in exactly one control family below, so the inventory can be checked for completeness against the chapters.

ਇਹ ਇਨਵੈਂਟਰੀ ਗ਼ੈਰ-ਨਿਯਮਬੱਧ[^0x91-non-normative] (non-normative) ਹੈ। ਇਹ ਮੌਜੂਦਾ ਲੋੜਾਂ ਨੂੰ ਲਾਗੂ ਕਰਨ ਦੀ ਸੌਖ ਲਈ ਮੁੜ-ਵਿਵਸਥਿਤ ਕਰਦੀ ਹੈ ਅਤੇ ਕਿਸੇ ਵੀ ਲੋੜ ਨੂੰ ਜੋੜਦੀ, ਹਟਾਉਂਦੀ, ਜਾਂ ਬਦਲਦੀ ਨਹੀਂ। ਲੋੜ ਅਧਿਆਇ (C1 ਤੋਂ C12) ਹੀ ਫ਼ੈਸਲਾਕੁੰਨ ਸਰੋਤ[^0x91-source-of-truth] (source of truth) ਬਣੇ ਰਹਿੰਦੇ ਹਨ। ਲੋੜ ID ਕੈਨੋਨੀਕਲ `C{chapter}.{section}.{requirement}` ਰੂਪ ਵਿੱਚ ਲਿਖੇ ਜਾਂਦੇ ਹਨ (ਉਦਾਹਰਨ ਲਈ, `C5.1.1`)। ਮਿਆਰ ਵਿਚਲੀ ਹਰ ਨੰਬਰ ਵਾਲੀ ਲੋੜ ਹੇਠਾਂ ਦਿੱਤੇ ਬਿਲਕੁਲ ਇੱਕ ਨਿਯੰਤਰਣ ਪਰਿਵਾਰ ਵਿੱਚ ਆਉਂਦੀ ਹੈ, ਇਸ ਲਈ ਇਨਵੈਂਟਰੀ ਦੀ ਸੰਪੂਰਨਤਾ ਨੂੰ ਅਧਿਆਵਾਂ ਦੇ ਵਿਰੁੱਧ ਜਾਂਚਿਆ ਜਾ ਸਕਦਾ ਹੈ।

---

## AD.1 Authentication & Identity
## AD.1 ਪ੍ਰਮਾਣੀਕਰਨ ਅਤੇ ਪਛਾਣ

Verify the identity of users, agents, services, edge devices, and MCP clients/servers before granting access.

ਪਹੁੰਚ ਦੇਣ ਤੋਂ ਪਹਿਲਾਂ ਉਪਭੋਗਤਾਵਾਂ, ਏਜੰਟਾਂ, ਸੇਵਾਵਾਂ, ਐਜ ਡਿਵਾਈਸਾਂ, ਅਤੇ MCP ਕਲਾਇੰਟਾਂ/ਸਰਵਰਾਂ ਦੀ ਪਛਾਣ ਦੀ ਤਸਦੀਕ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Step-up authentication for high-risk AI operations (model deployment, weight export, training-data access, production configuration changes) | C5.1.1 |
| Short-lived, minimal-scoped, cryptographically signed tokens for federated or multi-system agent authentication | C5.1.2 |
| Strong authentication of edge AI devices to central infrastructure | C4.3.1 |
| Unique cryptographic identity per agent instance, authenticating as a first-class principal to downstream systems | C9.4.1 |
| Scheduled rotation of agent identity credentials | C9.4.3 |
| MCP per-request access-token validation (not transport security alone) | C10.2.1 |
| MCP access-token claim validation (issuer, audience, expiration, scope) per OAuth 2.1 | C10.2.2 |
| MCP resource servers do not store or persist access tokens or user credentials | C10.2.3 |
| Removal of all MCP session artifacts on session termination | C10.2.6 |
| No pass-through of client access tokens to downstream APIs | C10.2.7 |
| Sender-constrained MCP access tokens (mTLS or DPoP) | C10.3.5 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਉੱਚ-ਜੋਖਮ ਵਾਲੀਆਂ AI ਕਾਰਵਾਈਆਂ (ਮਾਡਲ ਤੈਨਾਤੀ, ਵੇਟਸ ਨਿਰਯਾਤ, ਸਿਖਲਾਈ-ਡਾਟਾ ਪਹੁੰਚ, ਪ੍ਰੋਡਕਸ਼ਨ ਸੰਰਚਨਾ ਤਬਦੀਲੀਆਂ) ਲਈ ਸਟੈੱਪ-ਅੱਪ ਪ੍ਰਮਾਣੀਕਰਨ | C5.1.1 |
| ਫ਼ੈਡਰੇਟਿਡ ਜਾਂ ਬਹੁ-ਸਿਸਟਮ ਏਜੰਟ ਪ੍ਰਮਾਣੀਕਰਨ ਲਈ ਥੋੜ੍ਹੇ ਸਮੇਂ ਵਾਲੇ, ਘੱਟੋ-ਘੱਟ ਸਕੋਪ ਵਾਲੇ, ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਦਸਤਖ਼ਤ ਕੀਤੇ ਟੋਕਨ | C5.1.2 |
| ਕੇਂਦਰੀ ਬੁਨਿਆਦੀ ਢਾਂਚੇ ਨਾਲ ਐਜ AI ਡਿਵਾਈਸਾਂ ਦਾ ਮਜ਼ਬੂਤ ਪ੍ਰਮਾਣੀਕਰਨ | C4.3.1 |
| ਪ੍ਰਤੀ ਏਜੰਟ ਇੰਸਟਾਂਸ ਵਿਲੱਖਣ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਪਛਾਣ, ਜੋ ਡਾਊਨਸਟ੍ਰੀਮ ਸਿਸਟਮਾਂ ਲਈ ਪਹਿਲੇ-ਦਰਜੇ ਦੀ ਪਛਾਣ-ਇਕਾਈ[^0x91-principal-identity-entity] (first-class principal) ਵਜੋਂ ਪ੍ਰਮਾਣੀਕਰਨ ਕਰਦੀ ਹੈ | C9.4.1 |
| ਏਜੰਟ ਪਛਾਣ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲਾਂ ਦੀ ਸਮਾਂ-ਸਾਰਣੀ ਅਨੁਸਾਰ ਅਦਲਾ-ਬਦਲੀ (rotation) | C9.4.3 |
| MCP ਪ੍ਰਤੀ-ਬੇਨਤੀ ਪਹੁੰਚ-ਟੋਕਨ ਪ੍ਰਮਾਣਿਕਤਾ (ਸਿਰਫ਼ ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ ਨਹੀਂ) | C10.2.1 |
| OAuth 2.1 ਅਨੁਸਾਰ MCP ਪਹੁੰਚ-ਟੋਕਨ ਦੇ ਦਾਅਵਿਆਂ (claims) — ਜਾਰੀਕਰਤਾ, ਉਦੇਸ਼ਿਤ ਪ੍ਰਾਪਤਕਰਤਾ (audience), ਮਿਆਦ ਸਮਾਪਤੀ, ਸਕੋਪ — ਦੀ ਪ੍ਰਮਾਣਿਕਤਾ | C10.2.2 |
| MCP ਸਰੋਤ ਸਰਵਰ ਪਹੁੰਚ ਟੋਕਨ ਜਾਂ ਉਪਭੋਗਤਾ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਨਾ ਤਾਂ ਭੰਡਾਰ ਕਰਦੇ ਹਨ ਅਤੇ ਨਾ ਹੀ ਸਥਾਈ ਤੌਰ 'ਤੇ ਰੱਖਦੇ ਹਨ | C10.2.3 |
| ਸੈਸ਼ਨ ਸਮਾਪਤੀ 'ਤੇ ਸਾਰੇ MCP ਸੈਸ਼ਨ ਆਰਟੀਫ਼ੈਕਟਾਂ ਨੂੰ ਹਟਾਉਣਾ | C10.2.6 |
| ਕਲਾਇੰਟ ਪਹੁੰਚ ਟੋਕਨਾਂ ਨੂੰ ਡਾਊਨਸਟ੍ਰੀਮ API ਤੱਕ ਅੱਗੇ ਨਾ ਲੰਘਾਉਣਾ[^0x91-pass-through] (pass-through) | C10.2.7 |
| ਭੇਜਣ ਵਾਲੇ ਨਾਲ ਬੰਨ੍ਹੇ ਹੋਏ (sender-constrained) MCP ਪਹੁੰਚ ਟੋਕਨ (mTLS ਜਾਂ DPoP) | C10.3.5 |

**Common pitfalls:** reusing end-user credentials for agent-to-agent calls; not rotating agent credentials on suspected compromise; treating transport security as a substitute for per-request token validation.

**ਆਮ ਗਲਤੀਆਂ[^0x91-common-pitfalls] (common pitfalls):** ਏਜੰਟ-ਤੋਂ-ਏਜੰਟ ਕਾਲਾਂ ਲਈ ਅੰਤਮ-ਉਪਭੋਗਤਾ ਦੇ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਮੁੜ-ਵਰਤਣਾ; ਸ਼ੱਕੀ ਸਮਝੌਤੇ (compromise) 'ਤੇ ਏਜੰਟ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲ ਨਾ ਬਦਲਣਾ; ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ ਨੂੰ ਪ੍ਰਤੀ-ਬੇਨਤੀ ਟੋਕਨ ਪ੍ਰਮਾਣਿਕਤਾ ਦੇ ਬਦਲ ਵਜੋਂ ਲੈਣਾ।

---

## AD.2 Authorization & Access Control
## AD.2 ਅਧਿਕਾਰੀਕਰਨ ਅਤੇ ਪਹੁੰਚ ਕੰਟਰੋਲ

Enforce access decisions across users, agents, tools, and resources using policy that the model cannot override.

ਉਪਭੋਗਤਾਵਾਂ, ਏਜੰਟਾਂ, ਟੂਲਾਂ, ਅਤੇ ਸਰੋਤਾਂ ਦੇ ਆਰ-ਪਾਰ ਪਹੁੰਚ ਫ਼ੈਸਲੇ ਅਜਿਹੀ ਨੀਤੀ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਲਾਗੂ ਕਰੋ ਜਿਸ ਨੂੰ ਮਾਡਲ ਓਵਰਰਾਈਡ ਨਾ ਕਰ ਸਕੇ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Access controls on every AI resource (datasets, endpoints, vector collections, embedding indices, compute) with explicit allow-lists and default-deny | C5.2.1 |
| End-user authorization context enforced at each retrieval and assembly stage, not the service account alone | C5.2.2 |
| Post-inference filtering so responses exclude data the requester is not entitled to receive | C5.2.4 |
| Policy decision point isolated from the agent execution environment | C5.2.5 |
| Just-in-time privileged access to model weights, training pipelines, and production configuration with automatic expiry | C5.2.6 |
| Fine-grained, runtime-enforced authorization of agent actions (which tools, which parameter values) | C9.5.1 |
| Integrity-protected, scope-limited delegation token propagated to every downstream call | C9.5.2 |
| Access-control decisions enforced by application logic or a policy engine, never by the model | C9.5.3 |
| Inter-agent task delegation restricted by an explicit authorization policy | C9.5.5 |
| Re-evaluation of backend authorization on every privileged action in long-running sessions | C9.5.6 |
| Scope-filtered MCP tool discovery (tools/list returns only authorized tools) | C10.2.4 |
| Per-invocation MCP access control validating both the tool and the supplied argument values | C10.2.5 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਹਰ AI ਸਰੋਤ (ਡਾਟਾਸੈੱਟ, ਐਂਡਪੁਆਇੰਟ, ਵੈਕਟਰ ਸੰਗ੍ਰਹਿ, embedding ਇੰਡੈਕਸ, ਕੰਪਿਊਟ) ਉੱਤੇ ਸਪੱਸ਼ਟ allow-list ਅਤੇ ਡਿਫ਼ਾਲਟ-ਇਨਕਾਰ ਨਾਲ ਪਹੁੰਚ ਕੰਟਰੋਲ | C5.2.1 |
| ਸਿਰਫ਼ ਸੇਵਾ ਖਾਤੇ ਦੀ ਬਜਾਏ, ਹਰ ਪ੍ਰਾਪਤੀ ਅਤੇ ਅਸੈਂਬਲੀ ਪੜਾਅ 'ਤੇ ਲਾਗੂ ਕੀਤਾ ਗਿਆ ਅੰਤਮ-ਉਪਭੋਗਤਾ ਅਧਿਕਾਰੀਕਰਨ ਸੰਦਰਭ | C5.2.2 |
| ਇਨਫ਼ਰੈਂਸ-ਉਪਰੰਤ ਫ਼ਿਲਟਰਿੰਗ, ਤਾਂ ਜੋ ਜਵਾਬਾਂ ਵਿੱਚ ਉਹ ਡਾਟਾ ਸ਼ਾਮਲ ਨਾ ਹੋਵੇ ਜਿਸ ਨੂੰ ਪ੍ਰਾਪਤ ਕਰਨ ਦਾ ਬੇਨਤੀਕਰਤਾ ਹੱਕਦਾਰ ਨਹੀਂ | C5.2.4 |
| ਏਜੰਟ ਦੇ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਕੀਤਾ ਨੀਤੀ ਫ਼ੈਸਲਾ ਬਿੰਦੂ (policy decision point) | C5.2.5 |
| ਮਾਡਲ ਵੇਟਸ, ਸਿਖਲਾਈ ਪਾਈਪਲਾਈਨਾਂ, ਅਤੇ ਪ੍ਰੋਡਕਸ਼ਨ ਸੰਰਚਨਾ ਤੱਕ ਆਪਣੇ-ਆਪ ਸਮਾਪਤੀ ਵਾਲੀ, ਸਿਰਫ਼ ਲੋੜ ਪੈਣ 'ਤੇ (just-in-time) ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ ਪਹੁੰਚ | C5.2.6 |
| ਏਜੰਟ ਕਾਰਵਾਈਆਂ ਦਾ ਬਾਰੀਕ-ਪੱਧਰੀ, ਰਨਟਾਈਮ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤਾ ਅਧਿਕਾਰੀਕਰਨ (ਕਿਹੜੇ ਟੂਲ, ਕਿਹੜੇ ਪੈਰਾਮੀਟਰ ਮੁੱਲ) | C9.5.1 |
| ਹਰ ਡਾਊਨਸਟ੍ਰੀਮ ਕਾਲ ਤੱਕ ਅੱਗੇ ਸੰਚਾਰਿਤ ਕੀਤਾ ਅਖੰਡਤਾ-ਸੁਰੱਖਿਅਤ, ਸਕੋਪ-ਸੀਮਿਤ ਸੌਂਪਣੀ (delegation) ਟੋਕਨ | C9.5.2 |
| ਐਪਲੀਕੇਸ਼ਨ ਤਰਕ ਜਾਂ ਨੀਤੀ ਇੰਜਣ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤੇ ਪਹੁੰਚ ਕੰਟਰੋਲ ਫ਼ੈਸਲੇ, ਕਦੇ ਵੀ ਮਾਡਲ ਦੁਆਰਾ ਨਹੀਂ | C9.5.3 |
| ਸਪੱਸ਼ਟ ਅਧਿਕਾਰੀਕਰਨ ਨੀਤੀ ਦੁਆਰਾ ਸੀਮਤ ਕੀਤੀ ਏਜੰਟਾਂ ਵਿਚਕਾਰ ਕਾਰਜ ਸੌਂਪਣੀ | C9.5.5 |
| ਲੰਬੇ ਸਮੇਂ ਤੱਕ ਚੱਲਣ ਵਾਲੇ ਸੈਸ਼ਨਾਂ ਵਿੱਚ ਹਰ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ ਕਾਰਵਾਈ 'ਤੇ ਬੈਕਐਂਡ ਅਧਿਕਾਰੀਕਰਨ ਦਾ ਮੁੜ-ਮੁਲਾਂਕਣ | C9.5.6 |
| ਸਕੋਪ-ਫ਼ਿਲਟਰ ਕੀਤੀ MCP ਟੂਲ ਖੋਜ (tools/list ਸਿਰਫ਼ ਅਧਿਕਾਰਤ ਟੂਲ ਵਾਪਸ ਕਰਦਾ ਹੈ) | C10.2.4 |
| ਪ੍ਰਤੀ-ਸੱਦਾ MCP ਪਹੁੰਚ ਕੰਟਰੋਲ ਜੋ ਟੂਲ ਅਤੇ ਦਿੱਤੇ ਗਏ ਆਰਗੂਮੈਂਟ ਮੁੱਲ ਦੋਵਾਂ ਨੂੰ ਪ੍ਰਮਾਣਿਤ ਕਰਦਾ ਹੈ | C10.2.5 |

**Common pitfalls:** relying on the service account's permissions instead of the caller's; letting model-generated output drive authorization; not re-checking authorization when context changes mid-session.

**ਆਮ ਗਲਤੀਆਂ:** ਕਾਲ ਕਰਨ ਵਾਲੇ ਦੀਆਂ ਇਜਾਜ਼ਤਾਂ ਦੀ ਬਜਾਏ ਸੇਵਾ ਖਾਤੇ ਦੀਆਂ ਇਜਾਜ਼ਤਾਂ 'ਤੇ ਨਿਰਭਰ ਰਹਿਣਾ; ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਕੀਤੇ ਆਊਟਪੁੱਟ ਨੂੰ ਅਧਿਕਾਰੀਕਰਨ ਚਲਾਉਣ ਦੇਣਾ; ਸੈਸ਼ਨ ਦੇ ਵਿਚਕਾਰ ਸੰਦਰਭ ਬਦਲਣ 'ਤੇ ਅਧਿਕਾਰੀਕਰਨ ਦੀ ਮੁੜ-ਜਾਂਚ ਨਾ ਕਰਨਾ।

---

## AD.3 Data Classification & Tenant Isolation
## AD.3 ਡਾਟਾ ਵਰਗੀਕਰਨ ਅਤੇ ਟੈਨੈਂਟ ਅਲੱਗ-ਥਲੱਗਤਾ

Keep data within its authorization and tenancy boundaries as it flows through AI-specific transformations and shared infrastructure.

ਡਾਟੇ ਨੂੰ AI-ਵਿਸ਼ੇਸ਼ ਪਰਿਵਰਤਨਾਂ ਅਤੇ ਸਾਂਝੇ ਬੁਨਿਆਦੀ ਢਾਂਚੇ ਵਿੱਚੋਂ ਲੰਘਦੇ ਸਮੇਂ ਉਸ ਦੇ ਅਧਿਕਾਰੀਕਰਨ ਅਤੇ ਟੈਨੈਂਸੀ ਦੀਆਂ ਸੀਮਾਵਾਂ ਦੇ ਅੰਦਰ ਰੱਖੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Sensitive data served through retrieval pipelines rather than persisted into model weights | C5.2.3 |
| Classification labels propagated to downstream resources (embeddings, prompt caches, model outputs) | C5.2.7 |
| Cross-tenant isolation in shared model serving (fine-tuning, inference, embedding operations) | C5.3.1 |
| Cross-tenant isolation across shared compute (hardware partitioning, confidential computing, or dedicated allocation) | C5.3.2 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਸੰਵੇਦਨਸ਼ੀਲ ਡਾਟਾ ਮਾਡਲ ਵੇਟਸ ਵਿੱਚ ਸਥਾਈ ਰੱਖਣ ਦੀ ਬਜਾਏ ਪ੍ਰਾਪਤੀ ਪਾਈਪਲਾਈਨਾਂ ਰਾਹੀਂ ਦਿੱਤਾ ਜਾਣਾ | C5.2.3 |
| ਵਰਗੀਕਰਨ ਲੇਬਲਾਂ ਦਾ ਡਾਊਨਸਟ੍ਰੀਮ ਸਰੋਤਾਂ (embeddings, prompt ਕੈਸ਼, ਮਾਡਲ ਆਊਟਪੁੱਟ) ਤੱਕ ਅੱਗੇ ਸੰਚਾਰ | C5.2.7 |
| ਸਾਂਝੇ ਮਾਡਲ ਸਰਵਿੰਗ ਵਿੱਚ ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ ਅਲੱਗ-ਥਲੱਗਤਾ (ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ, ਇਨਫ਼ਰੈਂਸ, embedding ਕਾਰਵਾਈਆਂ) | C5.3.1 |
| ਸਾਂਝੇ ਕੰਪਿਊਟ ਦੇ ਆਰ-ਪਾਰ ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ ਅਲੱਗ-ਥਲੱਗਤਾ (ਹਾਰਡਵੇਅਰ ਵਿਭਾਜਨ, ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ, ਜਾਂ ਰਾਖਵੀਂ ਵੰਡ) | C5.3.2 |

**Common pitfalls:** dropping classification labels when data is embedded or cached; assuming logical multi-tenancy is sufficient against side channels in shared inference caches.

**ਆਮ ਗਲਤੀਆਂ:** ਡਾਟਾ embed ਜਾਂ ਕੈਸ਼ ਹੋਣ ਵੇਲੇ ਵਰਗੀਕਰਨ ਲੇਬਲ ਗੁਆ ਦੇਣਾ; ਇਹ ਮੰਨ ਲੈਣਾ ਕਿ ਸਾਂਝੇ ਇਨਫ਼ਰੈਂਸ ਕੈਸ਼ਾਂ ਵਿਚਲੇ ਸਾਈਡ-ਚੈਨਲਾਂ ਵਿਰੁੱਧ ਤਾਰਕਿਕ ਬਹੁ-ਟੈਨੈਂਸੀ ਹੀ ਕਾਫ਼ੀ ਹੈ।

---

## AD.4 Encryption & Data Protection
## AD.4 ਏਨਕ੍ਰਿਪਸ਼ਨ ਅਤੇ ਡਾਟਾ ਸੁਰੱਖਿਆ

Protect data and secrets at rest, in transit, and in the model's observable context.

ਡਾਟਾ ਅਤੇ ਗੁਪਤ ਭੇਦਾਂ ਦੀ ਸਥਿਰ ਸਥਿਤੀ ਵਿੱਚ (at rest), ਪ੍ਰਸਾਰਣ ਦੌਰਾਨ, ਅਤੇ ਮਾਡਲ ਦੇ ਦੇਖਣਯੋਗ ਸੰਦਰਭ ਵਿੱਚ ਸੁਰੱਖਿਆ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Integrity protection of training data while stored and transferred | C1.1.3 |
| Redaction, anonymization, or encryption of sensitive information in labels before use in any labeling artifact | C1.2.3 |
| Encryption of locally stored model weights and sensitive parameters using hardware-backed key stores or secure enclaves | C4.3.4 |
| Encryption at rest of models packaged in mobile, IoT, or embedded apps, decrypted only inside a trusted runtime or secure enclave | C4.3.5 |
| Secrets and credentials kept out of the model's observable context (context window, system prompts, tool-call parameters) | C9.5.4 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਸਿਖਲਾਈ ਡਾਟੇ ਦੇ ਭੰਡਾਰਨ ਅਤੇ ਪ੍ਰਸਾਰਣ ਦੌਰਾਨ ਉਸ ਦੀ ਅਖੰਡਤਾ ਦੀ ਸੁਰੱਖਿਆ | C1.1.3 |
| ਕਿਸੇ ਵੀ ਲੇਬਲਿੰਗ ਆਰਟੀਫ਼ੈਕਟ ਵਿੱਚ ਵਰਤੋਂ ਤੋਂ ਪਹਿਲਾਂ ਲੇਬਲਾਂ ਵਿਚਲੀ ਸੰਵੇਦਨਸ਼ੀਲ ਜਾਣਕਾਰੀ ਦੀ ਰਿਡੈਕਸ਼ਨ, ਗੁਮਨਾਮੀਕਰਨ, ਜਾਂ ਏਨਕ੍ਰਿਪਸ਼ਨ | C1.2.3 |
| ਹਾਰਡਵੇਅਰ-ਸਮਰਥਿਤ ਕੁੰਜੀ ਸਟੋਰਾਂ ਜਾਂ ਸੁਰੱਖਿਅਤ ਐਨਕਲੇਵਾਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਸੰਭਾਲੇ ਮਾਡਲ ਵੇਟਸ ਅਤੇ ਸੰਵੇਦਨਸ਼ੀਲ ਪੈਰਾਮੀਟਰਾਂ ਦੀ ਏਨਕ੍ਰਿਪਸ਼ਨ | C4.3.4 |
| ਮੋਬਾਈਲ, IoT, ਜਾਂ ਏਮਬੈਡਡ ਐਪਾਂ ਵਿੱਚ ਪੈਕ ਕੀਤੇ ਮਾਡਲਾਂ ਦੀ ਸਥਿਰ ਸਥਿਤੀ ਵਿੱਚ ਏਨਕ੍ਰਿਪਸ਼ਨ, ਜੋ ਸਿਰਫ਼ ਭਰੋਸੇਯੋਗ ਰਨਟਾਈਮ ਜਾਂ ਸੁਰੱਖਿਅਤ ਐਨਕਲੇਵ ਦੇ ਅੰਦਰ ਹੀ ਡੀਕ੍ਰਿਪਟ ਹੁੰਦੇ ਹਨ | C4.3.5 |
| ਗੁਪਤ ਭੇਦਾਂ ਅਤੇ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲਾਂ ਨੂੰ ਮਾਡਲ ਦੇ ਦੇਖਣਯੋਗ ਸੰਦਰਭ (ਸੰਦਰਭ ਵਿੰਡੋ, system prompt, ਟੂਲ-ਕਾਲ ਪੈਰਾਮੀਟਰ) ਤੋਂ ਬਾਹਰ ਰੱਖਣਾ | C9.5.4 |

**Common pitfalls:** encrypting the database but not model checkpoints or embeddings; leaving model weights extractable from an app package; exposing API keys inside tool-call parameters.

**ਆਮ ਗਲਤੀਆਂ:** ਡਾਟਾਬੇਸ ਨੂੰ ਏਨਕ੍ਰਿਪਟ ਕਰਨਾ ਪਰ ਮਾਡਲ ਚੈੱਕਪੁਆਇੰਟਾਂ ਜਾਂ embeddings ਨੂੰ ਨਹੀਂ; ਮਾਡਲ ਵੇਟਸ ਨੂੰ ਐਪ ਪੈਕੇਜ ਵਿੱਚੋਂ ਕੱਢਣਯੋਗ ਛੱਡ ਦੇਣਾ; ਟੂਲ-ਕਾਲ ਪੈਰਾਮੀਟਰਾਂ ਦੇ ਅੰਦਰ API ਕੁੰਜੀਆਂ ਜ਼ਾਹਰ ਕਰਨਾ।

---

## AD.5 Integrity, Signing & Provenance
## AD.5 ਅਖੰਡਤਾ, ਦਸਤਖ਼ਤ, ਅਤੇ ਮੂਲ-ਸਰੋਤ

Verify authenticity and detect tampering of models, artifacts, messages, tool definitions, and generated media.

ਮਾਡਲਾਂ, ਆਰਟੀਫ਼ੈਕਟਾਂ, ਸੁਨੇਹਿਆਂ, ਟੂਲ ਪਰਿਭਾਸ਼ਾਵਾਂ, ਅਤੇ ਤਿਆਰ ਕੀਤੇ ਮੀਡੀਆ ਦੀ ਅਸਲੀਅਤ[^0x91-authenticity] (authenticity) ਦੀ ਤਸਦੀਕ ਕਰੋ ਅਤੇ ਛੇੜਛਾੜ ਦਾ ਪਤਾ ਲਗਾਓ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Integrity monitoring of training data against unauthorized modification or corruption | C1.1.4 |
| Cryptographic integrity for labeling artifacts | C1.2.2 |
| Cryptographic signing of all model artifacts (weights, configs, tokenizers, base models, fine-tunes, adapters, safety/policy models) | C3.1.2 |
| Signature verification at deployment admission and on load | C3.1.3 |
| Signed edge/mobile model packages with on-device signature or checksum validation before load | C4.3.2 |
| Cryptographic binding of agent-initiated actions to each step of the execution chain for non-repudiation | C9.4.2 |
| Integrity protection of agent state persisted between invocations | C9.4.4 |
| Signed MCP tool responses with a unique nonce and timestamp for replay defense | C10.4.6 |
| Tool-definition snapshotting with re-approval required on any change before invocation | C10.4.8 |
| Watermarking of AI-generated media to prove it was AI-generated | C7.4.4 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਅਣਅਧਿਕਾਰਤ ਸੋਧ ਜਾਂ ਵਿਗਾੜ ਵਿਰੁੱਧ ਸਿਖਲਾਈ ਡਾਟੇ ਦੀ ਅਖੰਡਤਾ ਨਿਗਰਾਨੀ | C1.1.4 |
| ਲੇਬਲਿੰਗ ਆਰਟੀਫ਼ੈਕਟਾਂ ਲਈ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਅਖੰਡਤਾ | C1.2.2 |
| ਸਾਰੇ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟਾਂ (ਵੇਟਸ, ਸੰਰਚਨਾਵਾਂ, ਟੋਕਨਾਈਜ਼ਰ, ਬੇਸ ਮਾਡਲ, ਫ਼ਾਈਨ-ਟਿਊਨ, ਅਡੈਪਟਰ, ਸਲਾਮਤੀ/ਨੀਤੀ ਮਾਡਲ) ਦੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਦਸਤਖ਼ਤ | C3.1.2 |
| ਤੈਨਾਤੀ ਦਾਖ਼ਲੇ ਸਮੇਂ ਅਤੇ ਲੋਡ ਹੋਣ ਸਮੇਂ ਦਸਤਖ਼ਤਾਂ ਦੀ ਤਸਦੀਕ | C3.1.3 |
| ਦਸਤਖ਼ਤ ਕੀਤੇ ਐਜ/ਮੋਬਾਈਲ ਮਾਡਲ ਪੈਕੇਜ, ਜਿਨ੍ਹਾਂ ਦੇ ਦਸਤਖ਼ਤ ਜਾਂ ਚੈੱਕਸਮ ਲੋਡ ਤੋਂ ਪਹਿਲਾਂ ਡਿਵਾਈਸ ਉੱਤੇ ਹੀ ਪ੍ਰਮਾਣਿਤ ਹੁੰਦੇ ਹਨ | C4.3.2 |
| ਗ਼ੈਰ-ਇਨਕਾਰਯੋਗਤਾ (non-repudiation) ਲਈ ਏਜੰਟ ਦੁਆਰਾ ਸ਼ੁਰੂ ਕੀਤੀਆਂ ਕਾਰਵਾਈਆਂ ਦਾ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਲੜੀ ਦੇ ਹਰ ਪੜਾਅ ਨਾਲ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਬੰਧਨ | C9.4.2 |
| ਸੱਦਿਆਂ ਵਿਚਕਾਰ ਸਥਾਈ ਰੱਖੀ ਗਈ ਏਜੰਟ ਸਥਿਤੀ ਦੀ ਅਖੰਡਤਾ ਸੁਰੱਖਿਆ | C9.4.4 |
| replay (ਦੁਹਰਾਓ)[^0x91-replay] ਵਿਰੁੱਧ ਬਚਾਅ ਲਈ ਵਿਲੱਖਣ ਨੌਂਸ (nonce) ਅਤੇ ਟਾਈਮਸਟੈਂਪ ਸਮੇਤ ਦਸਤਖ਼ਤ ਕੀਤੇ MCP ਟੂਲ ਜਵਾਬ | C10.4.6 |
| ਟੂਲ ਪਰਿਭਾਸ਼ਾਵਾਂ ਦੀ ਸਨੈਪਸ਼ਾਟਿੰਗ, ਜਿਸ ਵਿੱਚ ਕਿਸੇ ਵੀ ਤਬਦੀਲੀ 'ਤੇ ਸੱਦੇ ਤੋਂ ਪਹਿਲਾਂ ਮੁੜ-ਮਨਜ਼ੂਰੀ ਲਾਜ਼ਮੀ ਹੈ | C10.4.8 |
| AI ਦੁਆਰਾ ਤਿਆਰ ਕੀਤੇ ਮੀਡੀਆ ਦੀ ਵਾਟਰਮਾਰਕਿੰਗ ਤਾਂ ਜੋ ਇਹ ਸਾਬਤ ਹੋ ਸਕੇ ਕਿ ਇਹ AI ਦੁਆਰਾ ਤਿਆਰ ਕੀਤਾ ਗਿਆ ਸੀ | C7.4.4 |

**Common pitfalls:** using mutable tags instead of immutable digests; not re-verifying tool definitions between MCP invocations; missing replay protection on tool responses.

**ਆਮ ਗਲਤੀਆਂ:** ਅਪਰਿਵਰਤਨਸ਼ੀਲ ਡਾਈਜੈਸਟਾਂ ਦੀ ਬਜਾਏ ਬਦਲਣਯੋਗ ਟੈਗ ਵਰਤਣੇ; MCP ਸੱਦਿਆਂ ਵਿਚਕਾਰ ਟੂਲ ਪਰਿਭਾਸ਼ਾਵਾਂ ਦੀ ਮੁੜ-ਤਸਦੀਕ ਨਾ ਕਰਨੀ; ਟੂਲ ਜਵਾਬਾਂ ਉੱਤੇ replay ਵਿਰੁੱਧ ਸੁਰੱਖਿਆ ਦਾ ਗ਼ੈਰ-ਮੌਜੂਦ ਹੋਣਾ।

---

## AD.6 Input Validation & Sanitization
## AD.6 ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ ਅਤੇ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ

Validate, normalize, and constrain all inputs (including tool, MCP, and retrieved content) before they reach the model or downstream systems.

ਸਾਰੇ ਇਨਪੁੱਟਾਂ (ਟੂਲ, MCP, ਅਤੇ ਪ੍ਰਾਪਤ ਕੀਤੀ ਸਮੱਗਰੀ ਸਮੇਤ) ਨੂੰ ਮਾਡਲ ਜਾਂ ਡਾਊਨਸਟ੍ਰੀਮ ਸਿਸਟਮਾਂ ਤੱਕ ਪਹੁੰਚਣ ਤੋਂ ਪਹਿਲਾਂ ਪ੍ਰਮਾਣਿਤ ਕਰੋ, ਸਧਾਰਨ ਬਣਾਓ, ਅਤੇ ਸੀਮਿਤ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Input normalization applied before tokenization or embedding | C2.1.1 |
| Encoding and representation-smuggling detection and mitigation (canonicalization, strict schema validation, policy-based rejection, or explicit marking) | C2.1.2 |
| Untrusted-input screening by a prompt-injection detection ruleset or classifier, with blocking | C2.1.3 |
| Input length controls that reject (not truncate) content exceeding the context window | C2.1.4 |
| Allow-list character-set restriction on all inputs | C2.1.5 |
| Instruction hierarchy enforcement (system and developer messages override user and untrusted input) | C2.1.6 |
| Reserved special tokens encoded as literal characters and not injectable into context | C2.1.7 |
| Many-shot jailbreaking pattern detection | C2.1.8 |
| Adversarial-perturbation, steganography, and hidden-content checks on non-text inputs (image, video, audio) | C2.2.3 |
| Cross-modal coordinated attack detection | C2.2.4 |
| Schema validation of tool outputs | C9.3.2 |
| Verification of external resources named in model output against an approved allow-list or registry before install or invocation | C9.3.7 |
| MCP response schema validation before injection into model context | C10.4.1 |
| Indirect-prompt-injection screening of MCP responses before injection into model context | C10.4.2 |
| Rejection of unrecognized or oversized MCP function-call parameters | C10.4.3 |
| Strict MCP schema validation | C10.4.4 |
| Maximum MCP payload size limits | C10.4.5 |
| Anomaly detection on external or untrusted inputs before inference | C11.4.1 |
| Gating actions on inputs flagged as anomalous | C11.4.2 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਟੋਕਨਾਈਜ਼ੇਸ਼ਨ ਜਾਂ embedding ਤੋਂ ਪਹਿਲਾਂ ਲਾਗੂ ਕੀਤਾ ਇਨਪੁੱਟ ਸਧਾਰਨੀਕਰਨ | C2.1.1 |
| ਏਨਕੋਡਿੰਗ ਅਤੇ ਪ੍ਰਤੀਨਿਧਤਾ ਤਸਕਰੀ ਦੀ ਪਛਾਣ ਅਤੇ ਉਸ ਨੂੰ ਘਟਾਉਣਾ (ਕੈਨੋਨੀਕਲਾਈਜ਼ੇਸ਼ਨ, ਸਖ਼ਤ ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ, ਨੀਤੀ-ਆਧਾਰਿਤ ਰੱਦਗੀ, ਜਾਂ ਸਪੱਸ਼ਟ ਨਿਸ਼ਾਨਦੇਹੀ) | C2.1.2 |
| ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟ ਦੀ prompt ਇੰਜੈਕਸ਼ਨ ਪਛਾਣ ਨਿਯਮ-ਸਮੂਹ ਜਾਂ ਵਰਗੀਕਾਰ ਦੁਆਰਾ ਛਾਣਬੀਣ, ਅਤੇ ਰੋਕ | C2.1.3 |
| ਇਨਪੁੱਟ ਲੰਬਾਈ ਨਿਯੰਤਰਣ ਜੋ ਸੰਦਰਭ ਵਿੰਡੋ ਤੋਂ ਵੱਧ ਸਮੱਗਰੀ ਨੂੰ ਕੱਟਣ ਦੀ ਬਜਾਏ ਰੱਦ ਕਰਦੇ ਹਨ | C2.1.4 |
| ਸਾਰੇ ਇਨਪੁੱਟਾਂ ਉੱਤੇ allow-list ਅੱਖਰ-ਸਮੂਹ ਪਾਬੰਦੀ | C2.1.5 |
| ਹਦਾਇਤ ਲੜੀ-ਕ੍ਰਮ ਦਾ ਲਾਗੂਕਰਨ (ਸਿਸਟਮ ਅਤੇ ਡਿਵੈਲਪਰ ਸੁਨੇਹੇ ਉਪਭੋਗਤਾ ਅਤੇ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟ ਉੱਤੇ ਭਾਰੂ ਰਹਿੰਦੇ ਹਨ) | C2.1.6 |
| ਰਾਖਵੇਂ ਵਿਸ਼ੇਸ਼ ਟੋਕਨ ਸ਼ਾਬਦਿਕ ਅੱਖਰਾਂ ਵਜੋਂ ਏਨਕੋਡ ਕੀਤੇ ਜਾਣ ਅਤੇ ਸੰਦਰਭ ਵਿੱਚ ਇੰਜੈਕਟ ਨਾ ਕੀਤੇ ਜਾ ਸਕਣ | C2.1.7 |
| many-shot jailbreaking ਪੈਟਰਨਾਂ ਦੀ ਪਛਾਣ | C2.1.8 |
| ਗ਼ੈਰ-ਲਿਖਤੀ ਇਨਪੁੱਟਾਂ (ਚਿੱਤਰ, ਵੀਡੀਓ, ਆਡੀਓ) ਉੱਤੇ ਵਿਰੋਧੀ ਵਿਗਾੜ, ਸਟੈਗਨੋਗ੍ਰਾਫ਼ੀ, ਅਤੇ ਲੁਕਵੀਂ ਸਮੱਗਰੀ ਦੀਆਂ ਜਾਂਚਾਂ | C2.2.3 |
| ਕਈ ਇਨਪੁੱਟ ਕਿਸਮਾਂ ਵਿੱਚ ਫੈਲੇ ਤਾਲਮੇਲ ਵਾਲੇ ਹਮਲਿਆਂ ਦੀ ਪਛਾਣ | C2.2.4 |
| ਟੂਲ ਆਊਟਪੁੱਟ ਦੀ ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ | C9.3.2 |
| ਮਾਡਲ ਆਊਟਪੁੱਟ ਵਿੱਚ ਨਾਮਜ਼ਦ ਬਾਹਰੀ ਸਰੋਤਾਂ ਦੀ, ਸਥਾਪਨਾ ਜਾਂ ਸੱਦੇ ਤੋਂ ਪਹਿਲਾਂ, ਪ੍ਰਵਾਨਿਤ allow-list ਜਾਂ ਰਜਿਸਟਰੀ ਦੇ ਵਿਰੁੱਧ ਤਸਦੀਕ | C9.3.7 |
| ਮਾਡਲ ਸੰਦਰਭ ਵਿੱਚ ਦਾਖ਼ਲ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ MCP ਜਵਾਬਾਂ ਦੀ ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ | C10.4.1 |
| ਮਾਡਲ ਸੰਦਰਭ ਵਿੱਚ ਦਾਖ਼ਲ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ MCP ਜਵਾਬਾਂ ਦੀ ਅਸਿੱਧੀ prompt ਇੰਜੈਕਸ਼ਨ ਲਈ ਛਾਣਬੀਣ | C10.4.2 |
| ਅਣਪਛਾਤੇ ਜਾਂ ਹੱਦੋਂ ਵੱਧ ਵੱਡੇ MCP function-call ਪੈਰਾਮੀਟਰਾਂ ਦੀ ਰੱਦਗੀ | C10.4.3 |
| ਸਖ਼ਤ MCP ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ | C10.4.4 |
| ਵੱਧ ਤੋਂ ਵੱਧ MCP ਪੇਲੋਡ ਆਕਾਰ ਸੀਮਾਵਾਂ | C10.4.5 |
| ਇਨਫ਼ਰੈਂਸ ਤੋਂ ਪਹਿਲਾਂ ਬਾਹਰੀ ਜਾਂ ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਇਨਪੁੱਟਾਂ ਉੱਤੇ ਅਸਧਾਰਨਤਾ ਪਛਾਣ | C11.4.1 |
| ਅਸਧਾਰਨ ਵਜੋਂ ਨਿਸ਼ਾਨਬੱਧ ਇਨਪੁੱਟਾਂ ਉੱਤੇ ਗੇਟਿੰਗ ਕਾਰਵਾਈਆਂ | C11.4.2 |

**Common pitfalls:** validating only the text modality while ignoring image/audio channels; relying on regex alone without semantic detection; not validating tool and MCP outputs before they re-enter agent context.

**ਆਮ ਗਲਤੀਆਂ:** ਸਿਰਫ਼ ਲਿਖਤੀ ਮਾਡੈਲਿਟੀ ਨੂੰ ਪ੍ਰਮਾਣਿਤ ਕਰਨਾ ਅਤੇ ਚਿੱਤਰ/ਆਡੀਓ ਚੈਨਲਾਂ ਨੂੰ ਅਣਗੌਲਿਆਂ ਛੱਡਣਾ; ਅਰਥ-ਪੱਖੀ ਪਛਾਣ ਤੋਂ ਬਿਨਾਂ ਸਿਰਫ਼ regex 'ਤੇ ਨਿਰਭਰ ਰਹਿਣਾ; ਟੂਲ ਅਤੇ MCP ਆਊਟਪੁੱਟ ਦੇ ਏਜੰਟ ਸੰਦਰਭ ਵਿੱਚ ਮੁੜ-ਦਾਖ਼ਲ ਹੋਣ ਤੋਂ ਪਹਿਲਾਂ ਉਹਨਾਂ ਨੂੰ ਪ੍ਰਮਾਣਿਤ ਨਾ ਕਰਨਾ।

---

## AD.7 Inbound Content & Policy Screening
## AD.7 ਆਉਣ ਵਾਲੀ ਸਮੱਗਰੀ ਅਤੇ ਨੀਤੀ ਛਾਣਬੀਣ

Screen prompts and training content against policy before they reach the model or the training pipeline.

prompt ਅਤੇ ਸਿਖਲਾਈ ਸਮੱਗਰੀ ਨੂੰ ਮਾਡਲ ਜਾਂ ਸਿਖਲਾਈ ਪਾਈਪਲਾਈਨ ਤੱਕ ਪਹੁੰਚਣ ਤੋਂ ਪਹਿਲਾਂ ਨੀਤੀ ਦੇ ਵਿਰੁੱਧ ਛਾਣੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Inbound content classification (violence, self-harm, hate, sexual) against configurable thresholds, with rejection or sanitization before model context | C2.2.1 |
| Evaluation of content classification for unsupported languages | C2.2.2 |
| Detection and removal of disallowed content before training | C1.3.4 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਸੰਰਚਨਾਯੋਗ ਥ੍ਰੈਸ਼ਹੋਲਡਾਂ ਦੇ ਵਿਰੁੱਧ ਆਉਣ ਵਾਲੀ ਸਮੱਗਰੀ ਦਾ ਵਰਗੀਕਰਨ (ਹਿੰਸਾ, ਸਵੈ-ਨੁਕਸਾਨ, ਨਫ਼ਰਤ, ਜਿਨਸੀ), ਅਤੇ ਮਾਡਲ ਸੰਦਰਭ ਤੋਂ ਪਹਿਲਾਂ ਰੱਦਗੀ ਜਾਂ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ | C2.2.1 |
| ਗ਼ੈਰ-ਸਮਰਥਿਤ ਭਾਸ਼ਾਵਾਂ ਲਈ ਸਮੱਗਰੀ ਵਰਗੀਕਰਨ ਦਾ ਮੁਲਾਂਕਣ | C2.2.2 |
| ਸਿਖਲਾਈ ਤੋਂ ਪਹਿਲਾਂ ਮਨਾਹੀ ਵਾਲੀ ਸਮੱਗਰੀ ਦੀ ਪਛਾਣ ਅਤੇ ਉਸ ਨੂੰ ਹਟਾਉਣਾ | C1.3.4 |

**Common pitfalls:** deploying classifiers tuned only for one language; screening prompts but not the training corpus.

**ਆਮ ਗਲਤੀਆਂ:** ਸਿਰਫ਼ ਇੱਕ ਭਾਸ਼ਾ ਲਈ ਟਿਊਨ ਕੀਤੇ ਵਰਗੀਕਾਰ ਤੈਨਾਤ ਕਰਨੇ; prompt ਦੀ ਛਾਣਬੀਣ ਕਰਨੀ ਪਰ ਸਿਖਲਾਈ ਭੰਡਾਰ (corpus) ਦੀ ਨਹੀਂ।

---

## AD.8 Output Handling & Safety
## AD.8 ਆਊਟਪੁੱਟ ਪ੍ਰਬੰਧਨ ਅਤੇ ਸਲਾਮਤੀ

Constrain, filter, and validate model outputs before they reach users or downstream systems.

ਮਾਡਲ ਆਊਟਪੁੱਟ ਨੂੰ ਉਪਭੋਗਤਾਵਾਂ ਜਾਂ ਡਾਊਨਸਟ੍ਰੀਮ ਸਿਸਟਮਾਂ ਤੱਕ ਪਹੁੰਚਣ ਤੋਂ ਪਹਿਲਾਂ ਸੀਮਿਤ ਕਰੋ, ਫ਼ਿਲਟਰ ਕਰੋ, ਅਤੇ ਪ੍ਰਮਾਣਿਤ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Schema validation of model outputs with rejection on mismatch | C7.1.1 |
| Length limits and termination controls on generated output | C7.1.2 |
| Confidence or uncertainty estimation for generated answers | C7.2.1 |
| Automatic blocking or fallback when confidence drops below a defined threshold | C7.2.2 |
| Additional verification step for responses classified as high-risk by policy | C7.2.3 |
| Automated classifiers that scan responses and block defined harmful-content categories | C7.3.1 |
| Detection and blocking of responses that disclose system prompt content or backend data | C7.3.2 |
| Prevention of model-generated output triggering outbound requests | C7.3.3 |
| Detection of hidden, encoded, or misleading output (homoglyphs, formatting, metadata, structured fields) | C7.3.4 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਮਾਡਲ ਆਊਟਪੁੱਟ ਦੀ ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ, ਅਤੇ ਮੇਲ ਨਾ ਖਾਣ 'ਤੇ ਰੱਦਗੀ | C7.1.1 |
| ਤਿਆਰ ਕੀਤੇ ਆਊਟਪੁੱਟ ਉੱਤੇ ਲੰਬਾਈ ਸੀਮਾਵਾਂ ਅਤੇ ਸਮਾਪਤੀ ਨਿਯੰਤਰਣ | C7.1.2 |
| ਤਿਆਰ ਕੀਤੇ ਜਵਾਬਾਂ ਲਈ ਭਰੋਸਾ ਜਾਂ ਅਨਿਸ਼ਚਿਤਤਾ ਦਾ ਅਨੁਮਾਨ | C7.2.1 |
| ਭਰੋਸਾ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਥ੍ਰੈਸ਼ਹੋਲਡ ਤੋਂ ਹੇਠਾਂ ਡਿੱਗਣ 'ਤੇ ਆਪਣੇ-ਆਪ ਰੋਕ ਜਾਂ ਫ਼ਾਲਬੈਕ | C7.2.2 |
| ਨੀਤੀ ਦੁਆਰਾ ਉੱਚ-ਜੋਖਮ ਵਜੋਂ ਵਰਗੀਕ੍ਰਿਤ ਜਵਾਬਾਂ ਲਈ ਵਾਧੂ ਤਸਦੀਕ ਪੜਾਅ | C7.2.3 |
| ਸਵੈਚਾਲਿਤ ਵਰਗੀਕਾਰ ਜੋ ਜਵਾਬਾਂ ਨੂੰ ਸਕੈਨ ਕਰਦੇ ਹਨ ਅਤੇ ਪਰਿਭਾਸ਼ਿਤ ਨੁਕਸਾਨਦੇਹ-ਸਮੱਗਰੀ ਸ਼੍ਰੇਣੀਆਂ ਨੂੰ ਰੋਕਦੇ ਹਨ | C7.3.1 |
| system prompt ਦੀ ਸਮੱਗਰੀ ਜਾਂ ਬੈਕਐਂਡ ਡਾਟੇ ਦਾ ਖੁਲਾਸਾ ਕਰਨ ਵਾਲੇ ਜਵਾਬਾਂ ਦੀ ਪਛਾਣ ਅਤੇ ਰੋਕ | C7.3.2 |
| ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਕੀਤੇ ਆਊਟਪੁੱਟ ਦੁਆਰਾ ਬਾਹਰ ਜਾਣ ਵਾਲੀਆਂ ਬੇਨਤੀਆਂ ਸ਼ੁਰੂ ਕਰਨ ਦੀ ਰੋਕਥਾਮ | C7.3.3 |
| ਲੁਕੇ ਹੋਏ, ਏਨਕੋਡ ਕੀਤੇ, ਜਾਂ ਗੁਮਰਾਹਕੁਨ ਆਊਟਪੁੱਟ ਦੀ ਪਛਾਣ (homoglyph, ਫ਼ਾਰਮੈਟਿੰਗ, ਮੈਟਾਡਾਟਾ, ਢਾਂਚਾਗਤ ਖੇਤਰ) | C7.3.4 |

**Common pitfalls:** enforcing stop sequences in batch mode but not on streaming output; leaking the system prompt through paraphrase; treating a confidence score as available when the provider does not expose one.

**ਆਮ ਗਲਤੀਆਂ:** ਬੈਚ ਮੋਡ ਵਿੱਚ stop sequence ਲਾਗੂ ਕਰਨੇ ਪਰ ਸਟ੍ਰੀਮਿੰਗ ਆਊਟਪੁੱਟ ਉੱਤੇ ਨਹੀਂ; ਪੈਰਾਫ਼ਰੇਜ਼ ਰਾਹੀਂ system prompt ਲੀਕ ਕਰ ਦੇਣਾ; ਭਰੋਸਾ ਸਕੋਰ ਨੂੰ ਉਪਲਬਧ ਮੰਨ ਲੈਣਾ ਜਦੋਂ ਪ੍ਰਦਾਤਾ ਉਹ ਦਿੰਦਾ ਹੀ ਨਹੀਂ।

---

## AD.9 Rate Limiting, Budgets & Resource Control
## AD.9 ਦਰ ਸੀਮਾ, ਬਜਟ, ਅਤੇ ਸਰੋਤ ਨਿਯੰਤਰਣ

Bound consumption to prevent abuse, runaway execution, denial of service, and model extraction.

ਦੁਰਵਰਤੋਂ, ਬੇਕਾਬੂ ਐਗਜ਼ੀਕਿਊਸ਼ਨ, ਸੇਵਾ-ਇਨਕਾਰ, ਅਤੇ model extraction ਨੂੰ ਰੋਕਣ ਲਈ ਖਪਤ ਨੂੰ ਸੀਮਾਬੱਧ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Per-tool quotas and timeouts (CPU, memory, disk, egress, execution time) | C9.1.1 |
| Per-execution budgets (maximum recursion depth, token use, monetary spend) enforced by the runtime | C9.1.2 |
| Per-principal and global inference rate limits sized to the extraction threat model, not a generic API throttle | C11.2.2 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਪ੍ਰਤੀ-ਟੂਲ ਕੋਟੇ ਅਤੇ ਟਾਈਮਆਊਟ (CPU, ਮੈਮੋਰੀ, ਡਿਸਕ, ਬਾਹਰ ਜਾਣ ਵਾਲਾ ਟਰੈਫ਼ਿਕ, ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਸਮਾਂ) | C9.1.1 |
| ਰਨਟਾਈਮ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤੇ ਪ੍ਰਤੀ-ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਬਜਟ (ਵੱਧ ਤੋਂ ਵੱਧ ਰੀਕਰਸ਼ਨ ਡੂੰਘਾਈ, ਟੋਕਨ ਵਰਤੋਂ, ਵਿੱਤੀ ਖ਼ਰਚ) | C9.1.2 |
| ਪ੍ਰਤੀ-ਪ੍ਰਿੰਸੀਪਲ[^0x91-principal-loan] ਅਤੇ ਸਮੁੱਚੀਆਂ ਇਨਫ਼ਰੈਂਸ ਦਰ ਸੀਮਾਵਾਂ, ਜੋ ਆਮ API ਥ੍ਰੌਟਲ ਦੀ ਬਜਾਏ extraction ਖ਼ਤਰਾ ਮਾਡਲ ਦੇ ਅਨੁਸਾਰ ਮਿਥੀਆਂ ਗਈਆਂ ਹੋਣ | C11.2.2 |

**Common pitfalls:** rate-limiting per endpoint but not per agent session; ignoring tool fan-out when sizing budgets; treating extraction defense as ordinary throttling.

**ਆਮ ਗਲਤੀਆਂ:** ਪ੍ਰਤੀ ਐਂਡਪੁਆਇੰਟ ਦਰ ਸੀਮਾ ਲਾਉਣੀ ਪਰ ਪ੍ਰਤੀ ਏਜੰਟ ਸੈਸ਼ਨ ਨਹੀਂ; ਬਜਟ ਮਿਥਦੇ ਸਮੇਂ ਟੂਲ ਫ਼ੈਨ-ਆਊਟ (fan-out) ਨੂੰ ਅਣਗੌਲਿਆਂ ਕਰਨਾ; extraction ਵਿਰੁੱਧ ਬਚਾਅ ਨੂੰ ਆਮ ਥ੍ਰੌਟਲਿੰਗ ਸਮਝ ਲੈਣਾ।

---

## AD.10 Sandboxing & Workload Isolation
## AD.10 ਸੈਂਡਬਾਕਸਿੰਗ ਅਤੇ ਵਰਕਲੋਡ ਅਲੱਗ-ਥਲੱਗਤਾ

Isolate models, tools, agents, and hardware workloads to contain failures and prevent lateral movement.

ਨਾਕਾਮੀਆਂ ਨੂੰ ਘੇਰਨ ਅਤੇ lateral movement (ਪਾਸੇ-ਵੱਲ ਫੈਲਾਅ)[^0x91-lateral-movement] ਨੂੰ ਰੋਕਣ ਲਈ ਮਾਡਲਾਂ, ਟੂਲਾਂ, ਏਜੰਟਾਂ, ਅਤੇ ਹਾਰਡਵੇਅਰ ਵਰਕਲੋਡਾਂ ਨੂੰ ਅਲੱਗ-ਥਲੱਗ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Execution of AI models in isolated sandboxes | C4.1.1 |
| Allow-list of serialization formats that do not permit code execution during deserialization | C4.1.2 |
| Workload attestation before model loading | C4.1.3 |
| Confidential inference protecting model weights at runtime through isolated execution | C4.1.4 |
| Trusted execution environment with hardware-enforced isolation, memory encryption, and integrity protection | C4.2.2 |
| GPU integrity validation via hardware attestation before each workload | C4.2.3 |
| GPU memory partitioning with sanitization between jobs | C4.2.4 |
| Version-pinned, signed, boot-attested accelerator firmware | C4.2.1 |
| Process, memory, and file-access isolation in edge inference runtimes | C4.3.3 |
| Least-privilege sandbox or isolation for each tool or plugin | C9.3.1 |
| Tool manifests declaring required privileges, resource limits, and output-validation requirements | C9.3.3 |
| Runtime enforcement of declared tool-manifest privileges and limits | C9.3.4 |
| Isolation of untrusted-data processing from tool-calling capability | C9.3.5 |
| Architectural separation of untrusted tool-output processing from agent operations | C9.3.6 |
| Least-privilege sandbox for locally launched MCP servers (restricted file system, network, system access) | C10.1.3 |
| AI-specific runtime components not shared across environment boundaries (development, staging, production) | C3.4.1 |
| Training and fine-tuning environments isolated from production | C3.4.2 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| AI ਮਾਡਲਾਂ ਦਾ ਅਲੱਗ-ਥਲੱਗ ਕੀਤੇ ਸੈਂਡਬਾਕਸਾਂ ਵਿੱਚ ਐਗਜ਼ੀਕਿਊਸ਼ਨ | C4.1.1 |
| ਅਜਿਹੇ ਸੀਰੀਅਲਾਈਜ਼ੇਸ਼ਨ ਫ਼ਾਰਮੈਟਾਂ ਦੀ allow-list ਜੋ ਡੀਸੀਰੀਅਲਾਈਜ਼ੇਸ਼ਨ ਦੌਰਾਨ ਕੋਡ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਦੀ ਆਗਿਆ ਨਹੀਂ ਦਿੰਦੇ | C4.1.2 |
| ਮਾਡਲ ਲੋਡ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਵਰਕਲੋਡ ਅਟੈਸਟੇਸ਼ਨ | C4.1.3 |
| ਗੁਪਤ ਇਨਫ਼ਰੈਂਸ, ਜੋ ਅਲੱਗ-ਥਲੱਗ ਕੀਤੇ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਰਾਹੀਂ ਰਨਟਾਈਮ ਦੌਰਾਨ ਮਾਡਲ ਵੇਟਸ ਦੀ ਸੁਰੱਖਿਆ ਕਰਦਾ ਹੈ | C4.1.4 |
| ਹਾਰਡਵੇਅਰ ਦੁਆਰਾ ਲਾਗੂ ਕੀਤੀ ਅਲੱਗ-ਥਲੱਗਤਾ, ਮੈਮੋਰੀ ਏਨਕ੍ਰਿਪਸ਼ਨ, ਅਤੇ ਅਖੰਡਤਾ ਸੁਰੱਖਿਆ ਵਾਲਾ ਭਰੋਸੇਯੋਗ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣ (TEE) | C4.2.2 |
| ਹਰ ਵਰਕਲੋਡ ਤੋਂ ਪਹਿਲਾਂ ਹਾਰਡਵੇਅਰ ਅਟੈਸਟੇਸ਼ਨ ਰਾਹੀਂ GPU ਅਖੰਡਤਾ ਦੀ ਪ੍ਰਮਾਣਿਕਤਾ | C4.2.3 |
| ਕੰਮਾਂ ਦੇ ਵਿਚਕਾਰ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ ਸਮੇਤ GPU ਮੈਮੋਰੀ ਦਾ ਵਿਭਾਜਨ | C4.2.4 |
| ਵਰਜ਼ਨ-ਪਿੰਨ ਕੀਤਾ, ਦਸਤਖ਼ਤ ਕੀਤਾ, ਬੂਟ ਵੇਲੇ ਅਟੈਸਟ ਕੀਤਾ ਐਕਸਲੇਰੇਟਰ ਫ਼ਰਮਵੇਅਰ | C4.2.1 |
| ਐਜ ਇਨਫ਼ਰੈਂਸ ਰਨਟਾਈਮਾਂ ਵਿੱਚ ਪ੍ਰਕਿਰਿਆ, ਮੈਮੋਰੀ, ਅਤੇ ਫ਼ਾਈਲ-ਪਹੁੰਚ ਦੀ ਅਲੱਗ-ਥਲੱਗਤਾ | C4.3.3 |
| ਹਰ ਟੂਲ ਜਾਂ ਪਲੱਗਇਨ ਲਈ ਘੱਟੋ-ਘੱਟ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਸੈਂਡਬਾਕਸ ਜਾਂ ਅਲੱਗ-ਥਲੱਗਤਾ | C9.3.1 |
| ਲੋੜੀਂਦੇ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰਾਂ, ਸਰੋਤ ਸੀਮਾਵਾਂ, ਅਤੇ ਆਊਟਪੁੱਟ-ਪ੍ਰਮਾਣਿਕਤਾ ਲੋੜਾਂ ਦੀ ਘੋਸ਼ਣਾ ਕਰਨ ਵਾਲੇ ਟੂਲ ਮੈਨੀਫ਼ੈਸਟ | C9.3.3 |
| ਟੂਲ ਮੈਨੀਫ਼ੈਸਟਾਂ ਵਿੱਚ ਘੋਸ਼ਿਤ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰਾਂ ਅਤੇ ਸੀਮਾਵਾਂ ਦਾ ਰਨਟਾਈਮ ਲਾਗੂਕਰਨ | C9.3.4 |
| ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਡਾਟਾ ਪ੍ਰਕਿਰਿਆ ਦੀ ਟੂਲ-ਕਾਲ ਕਰਨ ਦੀ ਸਮਰੱਥਾ ਤੋਂ ਅਲੱਗ-ਥਲੱਗਤਾ | C9.3.5 |
| ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਟੂਲ-ਆਊਟਪੁੱਟ ਪ੍ਰਕਿਰਿਆ ਦਾ ਏਜੰਟ ਕਾਰਵਾਈਆਂ ਤੋਂ ਆਰਕੀਟੈਕਚਰਲ ਵਿਭਾਜਨ | C9.3.6 |
| ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਚਲਾਏ ਗਏ MCP ਸਰਵਰਾਂ ਲਈ ਘੱਟੋ-ਘੱਟ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਸੈਂਡਬਾਕਸ (ਸੀਮਿਤ ਫ਼ਾਈਲਸਿਸਟਮ, ਨੈੱਟਵਰਕ, ਸਿਸਟਮ ਪਹੁੰਚ) | C10.1.3 |
| AI-ਵਿਸ਼ੇਸ਼ ਰਨਟਾਈਮ ਕੰਪੋਨੈਂਟ ਵਾਤਾਵਰਣ ਸੀਮਾਵਾਂ (ਵਿਕਾਸ, ਸਟੇਜਿੰਗ, ਪ੍ਰੋਡਕਸ਼ਨ) ਦੇ ਆਰ-ਪਾਰ ਸਾਂਝੇ ਨਾ ਕੀਤੇ ਜਾਣ | C3.4.1 |
| ਸਿਖਲਾਈ ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਵਾਤਾਵਰਣਾਂ ਦਾ ਪ੍ਰੋਡਕਸ਼ਨ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਹੋਣਾ | C3.4.2 |

**Common pitfalls:** sharing infrastructure between dev and prod; granting tool sandboxes more capability than needed; allowing untrusted data processing to reach tool-calling paths.

**ਆਮ ਗਲਤੀਆਂ:** ਵਿਕਾਸ ਅਤੇ ਪ੍ਰੋਡਕਸ਼ਨ ਵਿਚਕਾਰ ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਸਾਂਝਾ ਕਰਨਾ; ਟੂਲ ਸੈਂਡਬਾਕਸਾਂ ਨੂੰ ਲੋੜ ਤੋਂ ਵੱਧ ਸਮਰੱਥਾ ਦੇਣੀ; ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ ਡਾਟਾ ਪ੍ਰਕਿਰਿਆ ਨੂੰ ਟੂਲ-ਕਾਲ ਦੇ ਰਾਹਾਂ ਤੱਕ ਪਹੁੰਚਣ ਦੇਣਾ।

---

## AD.11 Network & Egress Control
## AD.11 ਨੈੱਟਵਰਕ ਅਤੇ ਬਾਹਰ ਜਾਣ ਵਾਲੇ ਟਰੈਫ਼ਿਕ (egress) ਦਾ ਨਿਯੰਤਰਣ

Control network boundaries, transport security, and traffic flow for AI workloads and MCP integrations.

AI ਵਰਕਲੋਡਾਂ ਅਤੇ MCP ਏਕੀਕਰਨਾਂ ਲਈ ਨੈੱਟਵਰਕ ਸੀਮਾਵਾਂ, ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ, ਅਤੇ ਟਰੈਫ਼ਿਕ ਦੇ ਵਹਾਅ ਨੂੰ ਨਿਯੰਤਰਿਤ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Authenticated, encrypted streamable HTTP for remote MCP transport | C10.3.1 |
| stdio MCP transport restricted to controlled local environments | C10.3.2 |
| Independent Origin and Host header validation on HTTP-based transports (DNS rebinding defense) | C10.3.3 |
| MCP client minimum protocol-version enforcement (downgrade defense) | C10.3.4 |
| Accelerator interconnects restricted to approved topologies and authenticated endpoints | C4.2.5 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਰਿਮੋਟ MCP ਟ੍ਰਾਂਸਪੋਰਟ ਲਈ ਪ੍ਰਮਾਣੀਕਰਨ ਕੀਤਾ, ਏਨਕ੍ਰਿਪਟ ਕੀਤਾ streamable HTTP | C10.3.1 |
| stdio MCP ਟ੍ਰਾਂਸਪੋਰਟ ਸਿਰਫ਼ ਨਿਯੰਤਰਿਤ ਸਥਾਨਕ ਵਾਤਾਵਰਣਾਂ ਤੱਕ ਸੀਮਿਤ | C10.3.2 |
| HTTP-ਆਧਾਰਿਤ ਟ੍ਰਾਂਸਪੋਰਟਾਂ ਉੱਤੇ Origin ਅਤੇ Host header ਦੀ ਸੁਤੰਤਰ ਪ੍ਰਮਾਣਿਕਤਾ (DNS rebinding ਵਿਰੁੱਧ ਬਚਾਅ) | C10.3.3 |
| MCP ਕਲਾਇੰਟ ਦੁਆਰਾ ਘੱਟੋ-ਘੱਟ ਪ੍ਰੋਟੋਕੋਲ-ਵਰਜ਼ਨ ਦਾ ਲਾਗੂਕਰਨ (ਡਾਊਨਗ੍ਰੇਡ[^0x91-downgrade] ਵਿਰੁੱਧ ਬਚਾਅ) | C10.3.4 |
| ਐਕਸਲੇਰੇਟਰ ਇੰਟਰਕਨੈਕਟਾਂ ਦਾ ਪ੍ਰਵਾਨਿਤ ਟੋਪੋਲੋਜੀਆਂ ਅਤੇ ਪ੍ਰਮਾਣੀਕਰਨ ਕੀਤੇ ਐਂਡਪੁਆਇੰਟਾਂ ਤੱਕ ਸੀਮਿਤ ਹੋਣਾ | C4.2.5 |

**Common pitfalls:** exposing stdio or SSE transports beyond the local host; skipping Origin/Host validation and enabling DNS rebinding; accepting downgraded protocol versions.

**ਆਮ ਗਲਤੀਆਂ:** stdio ਜਾਂ SSE ਟ੍ਰਾਂਸਪੋਰਟਾਂ ਨੂੰ ਸਥਾਨਕ ਹੋਸਟ ਤੋਂ ਪਰੇ ਜ਼ਾਹਰ ਕਰਨਾ; Origin/Host ਪ੍ਰਮਾਣਿਕਤਾ ਛੱਡ ਦੇਣੀ ਅਤੇ DNS rebinding ਨੂੰ ਸੰਭਵ ਬਣਾ ਦੇਣਾ; ਡਾਊਨਗ੍ਰੇਡ ਕੀਤੇ ਪ੍ਰੋਟੋਕੋਲ ਵਰਜ਼ਨ ਸਵੀਕਾਰ ਕਰਨੇ।

---

## AD.12 Supply Chain & Artifact Integrity
## AD.12 ਸਪਲਾਈ ਚੇਨ ਅਤੇ ਆਰਟੀਫ਼ੈਕਟ ਅਖੰਡਤਾ

Verify origin and authenticity of models, datasets, frameworks, and MCP components, and maintain an AI bill of materials.

ਮਾਡਲਾਂ, ਡਾਟਾਸੈੱਟਾਂ, ਫ੍ਰੇਮਵਰਕਾਂ, ਅਤੇ MCP ਕੰਪੋਨੈਂਟਾਂ ਦੇ ਮੂਲ ਅਤੇ ਅਸਲੀਅਤ ਦੀ ਤਸਦੀਕ ਕਰੋ, ਅਤੇ ਇੱਕ AI ਬਿਲ ਆਫ਼ ਮਟੀਰੀਅਲਜ਼ ਬਰਕਰਾਰ ਰੱਖੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Model registry inventory of all deployed model artifacts and their origin | C3.1.1 |
| Malicious-code scanning of models before import | C6.1.1 |
| Approved-source-only download of model weights, datasets, and fine-tuning adapters | C6.1.2 |
| Integrity verification of every third-party model artifact | C6.1.3 |
| Behavioral acceptance test suite passed before promotion beyond development | C6.1.4 |
| Version-controlled, machine-readable AI BOM per model artifact (datasets, weights, licenses, data-origin statements) | C6.2.1 |
| Cryptographic signing of AI BOMs before deployment | C6.2.2 |
| Build-failing AI BOM completeness checks when component metadata is missing | C6.2.3 |
| MCP components obtained only from trusted sources and cryptographically verified | C10.1.1 |
| Allow-listed MCP servers only | C10.1.2 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਸਾਰੇ ਤੈਨਾਤ ਕੀਤੇ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟਾਂ ਅਤੇ ਉਹਨਾਂ ਦੇ ਮੂਲ ਦੀ ਮਾਡਲ ਰਜਿਸਟਰੀ ਇਨਵੈਂਟਰੀ | C3.1.1 |
| ਆਯਾਤ ਤੋਂ ਪਹਿਲਾਂ ਮਾਡਲਾਂ ਦੀ ਖ਼ਤਰਨਾਕ ਕੋਡ ਲਈ ਸਕੈਨਿੰਗ | C6.1.1 |
| ਮਾਡਲ ਵੇਟਸ, ਡਾਟਾਸੈੱਟਾਂ, ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਅਡੈਪਟਰਾਂ ਦਾ ਸਿਰਫ਼ ਪ੍ਰਵਾਨਿਤ ਸਰੋਤਾਂ ਤੋਂ ਡਾਊਨਲੋਡ | C6.1.2 |
| ਹਰ ਤੀਜੀ-ਧਿਰ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਦੀ ਅਖੰਡਤਾ ਦੀ ਤਸਦੀਕ | C6.1.3 |
| ਵਿਕਾਸ ਤੋਂ ਪਰੇ ਤਰੱਕੀ ਤੋਂ ਪਹਿਲਾਂ ਵਿਵਹਾਰਕ ਸਵੀਕ੍ਰਿਤੀ ਟੈਸਟ ਸੂਟ ਦਾ ਪਾਸ ਹੋਣਾ | C6.1.4 |
| ਪ੍ਰਤੀ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ ਵਰਜ਼ਨ-ਨਿਯੰਤਰਿਤ, ਮਸ਼ੀਨ-ਪੜ੍ਹਨਯੋਗ AI BOM (ਡਾਟਾਸੈੱਟ, ਵੇਟਸ, ਲਾਇਸੈਂਸ, ਡਾਟਾ-ਮੂਲ ਬਿਆਨ) | C6.2.1 |
| ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ AI BOM ਦੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਦਸਤਖ਼ਤ | C6.2.2 |
| ਕੰਪੋਨੈਂਟ ਮੈਟਾਡਾਟਾ ਗ਼ੈਰ-ਮੌਜੂਦ ਹੋਣ 'ਤੇ ਬਿਲਡ ਨੂੰ ਫ਼ੇਲ੍ਹ ਕਰਨ ਵਾਲੀਆਂ AI BOM ਸੰਪੂਰਨਤਾ ਜਾਂਚਾਂ | C6.2.3 |
| MCP ਕੰਪੋਨੈਂਟ ਸਿਰਫ਼ ਭਰੋਸੇਯੋਗ ਸਰੋਤਾਂ ਤੋਂ ਪ੍ਰਾਪਤ ਕੀਤੇ ਅਤੇ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਤਸਦੀਕ ਕੀਤੇ ਜਾਣ | C10.1.1 |
| ਸਿਰਫ਼ allow-list ਕੀਤੇ MCP ਸਰਵਰ | C10.1.2 |

**Common pitfalls:** treating AI BOMs as static documents rather than signed, version-controlled artifacts; not scanning pretrained weights for backdoors; pulling models from unapproved registries.

**ਆਮ ਗਲਤੀਆਂ:** AI BOM ਨੂੰ ਦਸਤਖ਼ਤ ਕੀਤੇ, ਵਰਜ਼ਨ-ਨਿਯੰਤਰਿਤ ਆਰਟੀਫ਼ੈਕਟਾਂ ਦੀ ਬਜਾਏ ਸਥਿਰ ਦਸਤਾਵੇਜ਼ ਸਮਝਣਾ; ਪਹਿਲਾਂ ਤੋਂ ਸਿਖਲਾਈ ਪ੍ਰਾਪਤ ਵੇਟਸ ਦੀ backdoor ਲਈ ਸਕੈਨਿੰਗ ਨਾ ਕਰਨੀ; ਗ਼ੈਰ-ਪ੍ਰਵਾਨਿਤ ਰਜਿਸਟਰੀਆਂ ਤੋਂ ਮਾਡਲ ਲੈਣੇ।

---

## AD.13 Model Lifecycle, Deployment & Rollback
## AD.13 ਮਾਡਲ ਜੀਵਨ-ਚੱਕਰ, ਤੈਨਾਤੀ, ਅਤੇ ਰੋਲਬੈਕ

Manage model validation, deployment, rollback, and fine-tuning pipeline integrity.

ਮਾਡਲ ਪ੍ਰਮਾਣਿਕਤਾ, ਤੈਨਾਤੀ, ਰੋਲਬੈਕ, ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਪਾਈਪਲਾਈਨ ਦੀ ਅਖੰਡਤਾ ਦਾ ਪ੍ਰਬੰਧ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Pre-deployment automated input-validation, safety-evaluation, and output-sanitization testing | C3.2.1 |
| Re-evaluation of models subjected to post-training quantization against the same safety and alignment test suite before deployment | C3.2.2 |
| Security re-evaluation triggered by provider model, version, or routing changes | C3.2.3 |
| Rollout mechanisms with automated rollback triggers | C3.3.1 |
| Complete model-state restoration on rollback | C3.3.2 |
| Isolated runtime state for model versions running in parallel | C3.3.3 |
| Versioned, integrity-verified RLHF reward models before a training run | C3.5.1 |
| Detection of reward hacking or reward-model over-optimization in RLHF stages | C3.5.2 |
| Stage-by-stage integrity verification in multi-stage fine-tuning pipelines | C3.5.3 |
| Fine-tuning checkpoints registered as distinct artifacts | C3.5.4 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ ਸਵੈਚਲਿਤ ਇਨਪੁੱਟ-ਪ੍ਰਮਾਣਿਕਤਾ, ਸਲਾਮਤੀ-ਮੁਲਾਂਕਣ, ਅਤੇ ਆਊਟਪੁੱਟ-ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ ਟੈਸਟਿੰਗ | C3.2.1 |
| ਸਿਖਲਾਈ-ਉਪਰੰਤ ਕੁਆਂਟਾਈਜ਼ੇਸ਼ਨ ਵਿੱਚੋਂ ਲੰਘੇ ਮਾਡਲਾਂ ਦਾ, ਤੈਨਾਤੀ ਤੋਂ ਪਹਿਲਾਂ, ਉਸੇ ਸਲਾਮਤੀ ਅਤੇ ਅਲਾਈਨਮੈਂਟ ਟੈਸਟ ਸੂਟ ਦੇ ਵਿਰੁੱਧ ਮੁੜ-ਮੁਲਾਂਕਣ | C3.2.2 |
| ਪ੍ਰਦਾਤਾ ਦੇ ਮਾਡਲ, ਵਰਜ਼ਨ, ਜਾਂ ਰੂਟਿੰਗ ਵਿੱਚ ਤਬਦੀਲੀਆਂ ਦੁਆਰਾ ਸ਼ੁਰੂ ਕੀਤਾ ਸੁਰੱਖਿਆ ਮੁੜ-ਮੁਲਾਂਕਣ | C3.2.3 |
| ਸਵੈਚਲਿਤ ਰੋਲਬੈਕ ਟ੍ਰਿਗਰਾਂ ਸਮੇਤ ਰੋਲਆਊਟ ਵਿਧੀਆਂ | C3.3.1 |
| ਰੋਲਬੈਕ 'ਤੇ ਮਾਡਲ ਦੀ ਸੰਪੂਰਨ ਸਥਿਤੀ ਦੀ ਬਹਾਲੀ | C3.3.2 |
| ਸਮਾਨਾਂਤਰ ਚੱਲ ਰਹੇ ਮਾਡਲ ਵਰਜ਼ਨਾਂ ਲਈ ਅਲੱਗ-ਥਲੱਗ ਕੀਤੀ ਰਨਟਾਈਮ ਸਥਿਤੀ | C3.3.3 |
| ਸਿਖਲਾਈ ਦੌਰ ਤੋਂ ਪਹਿਲਾਂ ਵਰਜ਼ਨਬੱਧ, ਅਖੰਡਤਾ-ਤਸਦੀਕਸ਼ੁਦਾ RLHF ਇਨਾਮ ਮਾਡਲ | C3.5.1 |
| RLHF ਪੜਾਵਾਂ ਵਿੱਚ reward hacking ਜਾਂ ਇਨਾਮ ਮਾਡਲ ਦੇ ਹੱਦੋਂ ਵੱਧ ਅਨੁਕੂਲਨ ਦੀ ਪਛਾਣ | C3.5.2 |
| ਬਹੁ-ਪੜਾਵੀ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਪਾਈਪਲਾਈਨਾਂ ਵਿੱਚ ਪੜਾਅ-ਦਰ-ਪੜਾਅ ਅਖੰਡਤਾ ਤਸਦੀਕ | C3.5.3 |
| ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਚੈੱਕਪੁਆਇੰਟਾਂ ਦਾ ਵੱਖਰੇ ਆਰਟੀਫ਼ੈਕਟਾਂ ਵਜੋਂ ਰਜਿਸਟਰ ਹੋਣਾ | C3.5.4 |

**Common pitfalls:** not testing rollback before it is needed; leaving retired model artifacts in serving caches; treating reward models as static infrastructure rather than versioned, validated artifacts.

**ਆਮ ਗਲਤੀਆਂ:** ਲੋੜ ਪੈਣ ਤੋਂ ਪਹਿਲਾਂ ਰੋਲਬੈਕ ਦੀ ਪਰਖ ਨਾ ਕਰਨੀ; ਸੇਵਾ-ਮੁਕਤ ਕੀਤੇ ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟਾਂ ਨੂੰ ਸਰਵਿੰਗ ਕੈਸ਼ਾਂ ਵਿੱਚ ਛੱਡ ਦੇਣਾ; ਇਨਾਮ ਮਾਡਲਾਂ ਨੂੰ ਵਰਜ਼ਨਬੱਧ, ਪ੍ਰਮਾਣਿਤ ਆਰਟੀਫ਼ੈਕਟਾਂ ਦੀ ਬਜਾਏ ਸਥਿਰ ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਸਮਝਣਾ।

---

## AD.14 Training Data Integrity & Governance
## AD.14 ਸਿਖਲਾਈ ਡਾਟਾ ਅਖੰਡਤਾ ਅਤੇ ਸ਼ਾਸਨ

Source, vet, and document training data so tampering, poisoning, and corruption can be detected and traced.

ਸਿਖਲਾਈ ਡਾਟਾ ਨੂੰ ਇਸ ਤਰ੍ਹਾਂ ਪ੍ਰਾਪਤ ਕਰੋ, ਪਰਖੋ, ਅਤੇ ਦਸਤਾਵੇਜ਼ਬੱਧ ਕਰੋ ਕਿ ਛੇੜਛਾੜ, poisoning, ਅਤੇ ਵਿਗਾੜ ਦਾ ਪਤਾ ਲਗਾਇਆ ਅਤੇ ਟਰੇਸ ਕੀਤਾ ਜਾ ਸਕੇ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Data minimization to only the features, attributes, and fields required for the stated purpose | C1.1.1 |
| Up-to-date inventory of every training-data source (origin, responsible party, license, collection method, use constraints, processing history) | C1.1.2 |
| Dataset watermarking for usage attribution and detection of unauthorized use | C1.1.5 |
| Labeling-platform access controls restricting who can create, modify, or approve annotations | C1.2.1 |
| Poisoning detection in training and fine-tuning pipelines | C1.3.1 |
| Confidence thresholds and consistency checks on automatically generated labels | C1.3.2 |
| Bias evaluation for models used in security-relevant decisions | C1.3.3 |
| Defenses against clean-label poisoning attacks | C1.3.5 |
| Dataset lineage recording (transformations, augmentations, merges) | C12.5.1 |
| Logging of all labeling activities | C12.5.2 |
| Write-time tagging of every ingested document (source, writer identity, timestamp) | C12.5.4 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਡਾਟਾ ਨੂੰ ਸਿਰਫ਼ ਦੱਸੇ ਗਏ ਮਕਸਦ ਲਈ ਲੋੜੀਂਦੇ ਫ਼ੀਚਰਾਂ, ਗੁਣਾਂ, ਅਤੇ ਖੇਤਰਾਂ ਤੱਕ ਘਟਾਉਣਾ | C1.1.1 |
| ਹਰ ਸਿਖਲਾਈ-ਡਾਟਾ ਸਰੋਤ ਦੀ ਅੱਪ-ਟੂ-ਡੇਟ ਇਨਵੈਂਟਰੀ (ਮੂਲ, ਜ਼ਿੰਮੇਵਾਰ ਧਿਰ, ਲਾਇਸੰਸ, ਇਕੱਤਰੀਕਰਨ ਵਿਧੀ, ਵਰਤੋਂ ਪਾਬੰਦੀਆਂ, ਪ੍ਰਕਿਰਿਆ ਇਤਿਹਾਸ) | C1.1.2 |
| ਵਰਤੋਂ ਦੇ ਸਰੋਤ-ਨਿਰਧਾਰਨ ਅਤੇ ਅਣਅਧਿਕਾਰਤ ਵਰਤੋਂ ਦੀ ਪਛਾਣ ਲਈ ਡਾਟਾਸੈੱਟ ਵਾਟਰਮਾਰਕਿੰਗ | C1.1.5 |
| ਲੇਬਲਿੰਗ-ਪਲੇਟਫ਼ਾਰਮ ਪਹੁੰਚ ਕੰਟਰੋਲ ਜੋ ਇਹ ਸੀਮਤ ਕਰਦੇ ਹਨ ਕਿ ਕੌਣ ਐਨੋਟੇਸ਼ਨਾਂ ਬਣਾ, ਸੋਧ, ਜਾਂ ਮਨਜ਼ੂਰ ਕਰ ਸਕਦਾ ਹੈ | C1.2.1 |
| ਸਿਖਲਾਈ ਅਤੇ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਪਾਈਪਲਾਈਨਾਂ ਵਿੱਚ poisoning ਪਛਾਣ | C1.3.1 |
| ਸਵੈਚਾਲਿਤ ਢੰਗ ਨਾਲ ਪੈਦਾ ਕੀਤੇ ਲੇਬਲਾਂ ਉੱਤੇ ਭਰੋਸਾ ਥ੍ਰੈਸ਼ਹੋਲਡ ਅਤੇ ਇਕਸਾਰਤਾ ਜਾਂਚਾਂ | C1.3.2 |
| ਸੁਰੱਖਿਆ-ਸੰਬੰਧਿਤ ਫ਼ੈਸਲਿਆਂ ਵਿੱਚ ਵਰਤੇ ਜਾਣ ਵਾਲੇ ਮਾਡਲਾਂ ਲਈ ਪੱਖਪਾਤ ਮੁਲਾਂਕਣ | C1.3.3 |
| clean-label poisoning ਹਮਲਿਆਂ ਵਿਰੁੱਧ ਬਚਾਅ | C1.3.5 |
| ਡਾਟਾਸੈੱਟ ਵੰਸ਼ਾਵਲੀ ਦਾ ਦਰਜ ਹੋਣਾ (ਪਰਿਵਰਤਨ, ਔਗਮੈਂਟੇਸ਼ਨ, ਮਰਜ) | C12.5.1 |
| ਸਾਰੀਆਂ ਲੇਬਲਿੰਗ ਗਤੀਵਿਧੀਆਂ ਦੀ ਲੌਗਿੰਗ | C12.5.2 |
| ਹਰ ਦਾਖ਼ਲ ਕੀਤੇ ਦਸਤਾਵੇਜ਼ ਦੀ ਲਿਖਣ-ਸਮੇਂ ਟੈਗਿੰਗ (ਸਰੋਤ, ਲਿਖਣ ਵਾਲੇ ਦੀ ਪਛਾਣ, ਟਾਈਮਸਟੈਂਪ) | C12.5.4 |

**Common pitfalls:** not scanning fine-tuning datasets for poisoning; collecting more attributes than the purpose requires; losing dataset lineage across transformations and merges.

**ਆਮ ਗਲਤੀਆਂ:** ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਡਾਟਾਸੈੱਟਾਂ ਦੀ poisoning ਲਈ ਸਕੈਨਿੰਗ ਨਾ ਕਰਨੀ; ਮਕਸਦ ਦੀ ਲੋੜ ਤੋਂ ਵੱਧ ਗੁਣ ਇਕੱਠੇ ਕਰਨੇ; ਪਰਿਵਰਤਨਾਂ ਅਤੇ ਮਰਜਾਂ ਦੇ ਆਰ-ਪਾਰ ਡਾਟਾਸੈੱਟ ਵੰਸ਼ਾਵਲੀ ਗੁਆ ਦੇਣੀ।

---

## AD.15 Memory, Embeddings & RAG Security
## AD.15 ਮੈਮੋਰੀ, embeddings, ਅਤੇ RAG ਸੁਰੱਖਿਆ

Harden vector stores, memory pipelines, and retrieval-augmented generation against leakage, poisoning, and fabricated provenance.

ਵੈਕਟਰ ਸਟੋਰਾਂ, ਮੈਮੋਰੀ ਪਾਈਪਲਾਈਨਾਂ, ਅਤੇ retrieval-augmented generation (RAG) ਨੂੰ ਲੀਕੇਜ, poisoning, ਅਤੇ ਘੜੇ ਹੋਏ ਮੂਲ-ਸਰੋਤ ਵਿਰੁੱਧ ਸਖ਼ਤ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Per-tenant uniqueness of vector identifiers and namespaces, preventing cross-tenant collisions | C8.1.1 |
| Immutability of document metadata tags after the initial write | C8.1.2 |
| Scope constraints enforced on retrieval operations | C8.1.3 |
| Detection and masking, tokenization, or dropping of sensitive fields before embedding | C8.2.1 |
| Detection, rejection, or quarantine of retrieval-manipulation content before vectorization | C8.2.4 |
| Flagging and quarantine of outlier vectors before they enter production indices | C8.2.2 |
| Source validation before agent or tool outputs are written to trusted memory | C8.2.3 |
| Contradiction checks on new memory writes, with conflicts triggering alerts | C8.2.5 |
| Exclusion of expired vectors from retrieval results | C8.3.1 |
| Memory reset capability | C8.3.2 |
| Retention of quarantined content while excluding it from all retrieval results | C8.3.3 |
| Attribution of RAG responses to their source documents | C7.4.1 |
| RAG attributions derived from retrieval metadata, not generated by the model | C7.4.2 |
| Traceability of RAG claims to the retrieved chunk | C7.4.3 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਵੈਕਟਰ ਪਛਾਣਕਰਤਾਵਾਂ ਅਤੇ ਨੇਮਸਪੇਸਾਂ ਦੀ ਪ੍ਰਤੀ-ਟੈਨੈਂਟ ਵਿਲੱਖਣਤਾ, ਜੋ ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ ਟਕਰਾਵਾਂ ਨੂੰ ਰੋਕਦੀ ਹੈ | C8.1.1 |
| ਸ਼ੁਰੂਆਤੀ ਲਿਖਤ ਤੋਂ ਬਾਅਦ ਦਸਤਾਵੇਜ਼ ਮੈਟਾਡਾਟਾ ਟੈਗਾਂ ਦੀ ਅਪਰਿਵਰਤਨਸ਼ੀਲਤਾ[^0x91-immutable] | C8.1.2 |
| ਪ੍ਰਾਪਤੀ ਕਾਰਵਾਈਆਂ ਉੱਤੇ ਲਾਗੂ ਕੀਤੀਆਂ ਸਕੋਪ ਪਾਬੰਦੀਆਂ | C8.1.3 |
| embedding ਤੋਂ ਪਹਿਲਾਂ ਸੰਵੇਦਨਸ਼ੀਲ ਖੇਤਰਾਂ ਦੀ ਪਛਾਣ ਅਤੇ ਉਹਨਾਂ ਦੀ ਮਾਸਕਿੰਗ, ਟੋਕਨਾਈਜ਼ੇਸ਼ਨ, ਜਾਂ ਹਟਾਈ | C8.2.1 |
| ਵੈਕਟਰਾਈਜ਼ੇਸ਼ਨ ਤੋਂ ਪਹਿਲਾਂ ਪ੍ਰਾਪਤੀ-ਹੇਰਾਫੇਰੀ ਵਾਲੀ ਸਮੱਗਰੀ ਦੀ ਪਛਾਣ, ਰੱਦਗੀ, ਜਾਂ ਕੁਆਰੰਟੀਨ | C8.2.4 |
| ਬਾਹਰਲੇ (outlier) ਵੈਕਟਰਾਂ ਦਾ ਉਤਪਾਦਨ ਇੰਡੈਕਸਾਂ ਵਿੱਚ ਦਾਖ਼ਲ ਹੋਣ ਤੋਂ ਪਹਿਲਾਂ ਨਿਸ਼ਾਨਬੱਧ ਹੋਣਾ ਅਤੇ ਕੁਆਰੰਟੀਨ | C8.2.2 |
| ਏਜੰਟ ਜਾਂ ਟੂਲ ਆਊਟਪੁੱਟ ਦੇ ਭਰੋਸੇਯੋਗ ਮੈਮੋਰੀ ਵਿੱਚ ਲਿਖੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਸਰੋਤ ਪ੍ਰਮਾਣਿਕਤਾ | C8.2.3 |
| ਨਵੀਆਂ ਮੈਮੋਰੀ ਲਿਖਤਾਂ ਉੱਤੇ ਵਿਰੋਧਾਭਾਸ ਜਾਂਚਾਂ, ਅਤੇ ਟਕਰਾਅ 'ਤੇ ਚੇਤਾਵਨੀਆਂ | C8.2.5 |
| ਮਿਆਦ ਪੁੱਗ ਚੁੱਕੇ ਵੈਕਟਰਾਂ ਨੂੰ ਪ੍ਰਾਪਤੀ ਨਤੀਜਿਆਂ ਵਿੱਚੋਂ ਬਾਹਰ ਰੱਖਣਾ | C8.3.1 |
| ਮੈਮੋਰੀ ਰੀਸੈੱਟ ਦੀ ਸਮਰੱਥਾ | C8.3.2 |
| ਕੁਆਰੰਟੀਨ ਕੀਤੀ ਸਮੱਗਰੀ ਦਾ ਧਾਰਨ, ਪਰ ਉਸ ਨੂੰ ਸਾਰੇ ਪ੍ਰਾਪਤੀ ਨਤੀਜਿਆਂ ਵਿੱਚੋਂ ਬਾਹਰ ਰੱਖਣਾ | C8.3.3 |
| RAG ਜਵਾਬਾਂ ਦਾ ਉਹਨਾਂ ਦੇ ਸਰੋਤ ਦਸਤਾਵੇਜ਼ਾਂ ਤੱਕ ਸਰੋਤ-ਨਿਰਧਾਰਨ | C7.4.1 |
| RAG ਸਰੋਤ-ਨਿਰਧਾਰਨ ਪ੍ਰਾਪਤੀ ਮੈਟਾਡਾਟਾ ਤੋਂ ਲਏ ਜਾਣ, ਮਾਡਲ ਦੁਆਰਾ ਤਿਆਰ ਨਾ ਕੀਤੇ ਜਾਣ | C7.4.2 |
| RAG ਦਾਅਵਿਆਂ ਦੀ ਪ੍ਰਾਪਤ ਕੀਤੇ ਚੰਕ ਤੱਕ ਟਰੇਸਯੋਗਤਾ | C7.4.3 |

**Common pitfalls:** auto-writing tool output into trusted memory without validation; serving expired or quarantined vectors; letting the model fabricate citations instead of deriving them from retrieval metadata.

**ਆਮ ਗਲਤੀਆਂ:** ਟੂਲ ਆਊਟਪੁੱਟ ਨੂੰ ਪ੍ਰਮਾਣਿਕਤਾ ਤੋਂ ਬਿਨਾਂ ਆਪਣੇ-ਆਪ ਭਰੋਸੇਯੋਗ ਮੈਮੋਰੀ ਵਿੱਚ ਲਿਖ ਦੇਣਾ; ਮਿਆਦ ਪੁੱਗ ਚੁੱਕੇ ਜਾਂ ਕੁਆਰੰਟੀਨ ਕੀਤੇ ਵੈਕਟਰ ਪਰੋਸਣੇ; ਮਾਡਲ ਨੂੰ ਪ੍ਰਾਪਤੀ ਮੈਟਾਡਾਟਾ ਤੋਂ ਲੈਣ ਦੀ ਬਜਾਏ ਹਵਾਲੇ ਘੜਨ ਦੇਣਾ।

---

## AD.16 Adversarial Robustness & Privacy Defense
## AD.16 ਵਿਰੋਧੀ ਮਜ਼ਬੂਤੀ ਅਤੇ ਨਿੱਜਤਾ ਬਚਾਅ

Test for and defend against evasion, membership inference, model inversion, extraction, and poisoning of the improvement loop.

evasion (ਪਛਾਣ ਤੋਂ ਬਚ ਨਿਕਲਣਾ), membership inference, model inversion, extraction, ਅਤੇ ਸੁਧਾਰ ਲੂਪ ਦੇ poisoning ਲਈ ਪਰਖ ਕਰੋ ਅਤੇ ਉਹਨਾਂ ਵਿਰੁੱਧ ਬਚਾਅ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Alignment and safety training or fine-tuning to suppress disallowed content categories | C11.1.1 |
| Version-controlled alignment test suite run on every model update or release | C11.1.2 |
| Evaluation against known adversarial attack techniques relevant to the modality | C11.1.3 |
| Hardening of models against adversarial inputs | C11.1.4 |
| Automated evaluator that measures harmful-content rate and flags regressions beyond a threshold | C11.1.5 |
| Suppression of directly returned model-inferred sensitive attributes | C11.2.1 |
| Output calibration to reduce overconfident predictions exploitable by inference attacks | C11.2.3 |
| Differentially-private optimization for training on sensitive datasets | C11.2.4 |
| Membership-inference attack simulation demonstrating accuracy no better than random guessing | C11.2.5 |
| Raw model outputs not exposed beyond the backend, with externally visible responses calibrated to extraction risk | C11.3.2 |
| Model watermarking or fingerprinting so unauthorized copies can be identified | C11.3.3 |
| Poisoning detection and human review gates protecting the safety-violation feedback pipeline | C11.4.3 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਮਨਾਹੀ ਵਾਲੀਆਂ ਸਮੱਗਰੀ ਸ਼੍ਰੇਣੀਆਂ ਨੂੰ ਦਬਾਉਣ ਲਈ ਅਲਾਈਨਮੈਂਟ ਅਤੇ ਸਲਾਮਤੀ ਸਿਖਲਾਈ ਜਾਂ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ | C11.1.1 |
| ਹਰ ਮਾਡਲ ਅੱਪਡੇਟ ਜਾਂ ਰਿਲੀਜ਼ ਉੱਤੇ ਚਲਾਇਆ ਜਾਣ ਵਾਲਾ ਵਰਜ਼ਨ-ਨਿਯੰਤਰਿਤ ਅਲਾਈਨਮੈਂਟ ਟੈਸਟ ਸੂਟ | C11.1.2 |
| ਮਾਡੈਲਿਟੀ ਨਾਲ ਸੰਬੰਧਿਤ ਜਾਣੀਆਂ-ਪਛਾਣੀਆਂ ਵਿਰੋਧੀ ਹਮਲਾ ਤਕਨੀਕਾਂ ਦੇ ਵਿਰੁੱਧ ਮੁਲਾਂਕਣ | C11.1.3 |
| ਵਿਰੋਧੀ ਇਨਪੁੱਟਾਂ ਵਿਰੁੱਧ ਮਾਡਲਾਂ ਨੂੰ ਸਖ਼ਤ ਕਰਨਾ | C11.1.4 |
| ਸਵੈਚਾਲਿਤ ਮੁਲਾਂਕਣਕਾਰ ਜੋ ਨੁਕਸਾਨਦੇਹ-ਸਮੱਗਰੀ ਦਰ ਮਾਪਦਾ ਹੈ ਅਤੇ ਇੱਕ ਥ੍ਰੈਸ਼ਹੋਲਡ ਤੋਂ ਪਰੇ ਦੇ ਰਿਗਰੈਸ਼ਨਾਂ ਨੂੰ ਨਿਸ਼ਾਨਬੱਧ ਕਰਦਾ ਹੈ | C11.1.5 |
| ਮਾਡਲ ਦੁਆਰਾ ਅਨੁਮਾਨਿਤ ਸੰਵੇਦਨਸ਼ੀਲ ਗੁਣਾਂ ਦੇ ਸਿੱਧੇ ਵਾਪਸ ਕੀਤੇ ਜਾਣ ਦੀ ਰੋਕਥਾਮ | C11.2.1 |
| ਇਨਫ਼ਰੈਂਸ ਹਮਲਿਆਂ ਦੁਆਰਾ ਵਰਤੇ ਜਾ ਸਕਣ ਵਾਲੇ ਹੱਦੋਂ ਵੱਧ ਭਰੋਸੇ ਵਾਲੇ ਪੂਰਵ-ਅਨੁਮਾਨਾਂ ਨੂੰ ਘਟਾਉਣ ਲਈ ਆਊਟਪੁੱਟ ਕੈਲੀਬ੍ਰੇਸ਼ਨ | C11.2.3 |
| ਸੰਵੇਦਨਸ਼ੀਲ ਡਾਟਾਸੈੱਟਾਂ ਉੱਤੇ ਸਿਖਲਾਈ ਲਈ differential privacy-ਆਧਾਰਿਤ ਅਨੁਕੂਲਨ | C11.2.4 |
| membership-inference ਹਮਲੇ ਦਾ ਸਿਮੂਲੇਸ਼ਨ ਜੋ ਦਰਸਾਏ ਕਿ ਸਟੀਕਤਾ ਬੇਤਰਤੀਬ ਅੰਦਾਜ਼ੇ ਤੋਂ ਵੱਧ ਨਹੀਂ | C11.2.5 |
| ਕੱਚੇ ਮਾਡਲ ਆਊਟਪੁੱਟ ਦਾ ਬੈਕਐਂਡ ਤੋਂ ਪਰੇ ਜ਼ਾਹਰ ਨਾ ਹੋਣਾ, ਅਤੇ ਬਾਹਰੋਂ ਦਿਖਾਈ ਦੇਣ ਵਾਲੇ ਜਵਾਬਾਂ ਦਾ extraction ਜੋਖਮ ਅਨੁਸਾਰ ਕੈਲੀਬ੍ਰੇਟ ਹੋਣਾ | C11.3.2 |
| ਮਾਡਲ ਵਾਟਰਮਾਰਕਿੰਗ ਜਾਂ ਫ਼ਿੰਗਰਪ੍ਰਿੰਟਿੰਗ ਤਾਂ ਜੋ ਅਣਅਧਿਕਾਰਤ ਨਕਲਾਂ ਦੀ ਪਛਾਣ ਹੋ ਸਕੇ | C11.3.3 |
| ਸਲਾਮਤੀ-ਉਲੰਘਣਾ ਫ਼ੀਡਬੈਕ ਪਾਈਪਲਾਈਨ ਦੀ ਰਾਖੀ ਕਰਨ ਵਾਲੇ poisoning ਪਛਾਣ ਅਤੇ ਮਨੁੱਖੀ ਸਮੀਖਿਆ ਗੇਟ | C11.4.3 |

**Common pitfalls:** testing only known jailbreak patterns without adaptive attacks; not re-running the alignment suite after model updates; exposing raw confidence vectors that accelerate extraction.

**ਆਮ ਗਲਤੀਆਂ:** ਅਨੁਕੂਲ ਹੋਣ ਵਾਲੇ ਹਮਲਿਆਂ ਤੋਂ ਬਿਨਾਂ ਸਿਰਫ਼ ਜਾਣੇ-ਪਛਾਣੇ jailbreak ਪੈਟਰਨਾਂ ਦੀ ਪਰਖ ਕਰਨੀ; ਮਾਡਲ ਅੱਪਡੇਟਾਂ ਤੋਂ ਬਾਅਦ ਅਲਾਈਨਮੈਂਟ ਸੂਟ ਮੁੜ ਨਾ ਚਲਾਉਣਾ; ਕੱਚੇ ਭਰੋਸਾ ਵੈਕਟਰ ਜ਼ਾਹਰ ਕਰਨੇ ਜੋ extraction ਨੂੰ ਤੇਜ਼ ਕਰਦੇ ਹਨ।

---

## AD.17 Logging & Audit
## AD.17 ਲੌਗਿੰਗ ਅਤੇ ਆਡਿਟ

Capture security-relevant events with sufficient context and integrity for forensic reconstruction and accountability.

ਸੁਰੱਖਿਆ-ਸੰਬੰਧਿਤ ਘਟਨਾਵਾਂ ਨੂੰ ਫ਼ੋਰੈਂਸਿਕ ਪੁਨਰ-ਨਿਰਮਾਣ ਅਤੇ ਜਵਾਬਦੇਹੀ ਲਈ ਲੋੜੀਂਦੇ ਸੰਦਰਭ ਅਤੇ ਅਖੰਡਤਾ ਨਾਲ ਦਰਜ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| AI interaction logging with session context and AI-specific telemetry | C12.1.1 |
| Logging of safety filtering and policy decisions in enough detail to audit content moderation | C12.1.2 |
| Structured, interoperable log schema for inference events (model identifier, token usage, provider, operation type) | C12.1.3 |
| Logging of RAG pipeline retrieval events (query, documents retrieved, knowledge source) | C12.1.4 |
| Audit logs capturing the approval chain for security-critical proactive actions (approver identity, timestamp, parameters, outcome) | C12.4.2 |
| Logging of kill-switch activations and override commands | C12.4.3 |
| Immutable audit records for all model changes | C12.5.3 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਸੈਸ਼ਨ ਸੰਦਰਭ ਅਤੇ AI-ਵਿਸ਼ੇਸ਼ ਟੈਲੀਮੈਟਰੀ ਸਮੇਤ AI ਪਰਸਪਰ-ਕਿਰਿਆਵਾਂ ਦੀ ਲੌਗਿੰਗ | C12.1.1 |
| ਸਲਾਮਤੀ ਫ਼ਿਲਟਰਿੰਗ ਅਤੇ ਨੀਤੀ ਫ਼ੈਸਲਿਆਂ ਦੀ ਇੰਨੇ ਵੇਰਵੇ ਨਾਲ ਲੌਗਿੰਗ ਕਿ ਸਮੱਗਰੀ ਮਾਡਰੇਸ਼ਨ ਦਾ ਆਡਿਟ ਹੋ ਸਕੇ | C12.1.2 |
| ਇਨਫ਼ਰੈਂਸ ਘਟਨਾਵਾਂ ਲਈ ਢਾਂਚਾਗਤ, ਅੰਤਰ-ਕਾਰਜਸ਼ੀਲ ਲੌਗ ਸਕੀਮਾ (ਮਾਡਲ ਪਛਾਣਕਰਤਾ, ਟੋਕਨ ਵਰਤੋਂ, ਪ੍ਰਦਾਤਾ, ਸੰਚਾਲਨ ਕਿਸਮ) | C12.1.3 |
| RAG ਪਾਈਪਲਾਈਨ ਦੀਆਂ ਪ੍ਰਾਪਤੀ ਘਟਨਾਵਾਂ ਦੀ ਲੌਗਿੰਗ (ਕਿਊਰੀ, ਪ੍ਰਾਪਤ ਕੀਤੇ ਦਸਤਾਵੇਜ਼, ਗਿਆਨ ਸਰੋਤ) | C12.1.4 |
| ਸੁਰੱਖਿਆ-ਨਾਜ਼ੁਕ ਪੂਰਵ-ਸਰਗਰਮ ਕਾਰਵਾਈਆਂ ਦੀ ਮਨਜ਼ੂਰੀ ਲੜੀ ਦਰਜ ਕਰਨ ਵਾਲੇ ਆਡਿਟ ਲੌਗ (ਮਨਜ਼ੂਰੀ ਦੇਣ ਵਾਲੇ ਦੀ ਪਛਾਣ, ਟਾਈਮਸਟੈਂਪ, ਪੈਰਾਮੀਟਰ, ਨਤੀਜਾ) | C12.4.2 |
| kill-switch ਦੀਆਂ ਸਰਗਰਮੀਆਂ ਅਤੇ ਓਵਰਰਾਈਡ ਕਮਾਂਡਾਂ ਦੀ ਲੌਗਿੰਗ | C12.4.3 |
| ਸਾਰੀਆਂ ਮਾਡਲ ਤਬਦੀਲੀਆਂ ਲਈ ਅਪਰਿਵਰਤਨਸ਼ੀਲ ਆਡਿਟ ਰਿਕਾਰਡ | C12.5.3 |

**Common pitfalls:** logging prompts without redaction; using mutable log storage without integrity protection; logging agent actions and approvals but not human-initiated overrides such as kill-switch activations.

**ਆਮ ਗਲਤੀਆਂ:** prompt ਨੂੰ ਰਿਡੈਕਸ਼ਨ ਤੋਂ ਬਿਨਾਂ ਲੌਗ ਕਰਨਾ; ਅਖੰਡਤਾ ਸੁਰੱਖਿਆ ਤੋਂ ਬਿਨਾਂ ਬਦਲਣਯੋਗ ਲੌਗ ਭੰਡਾਰਨ ਵਰਤਣਾ; ਏਜੰਟ ਕਾਰਵਾਈਆਂ ਅਤੇ ਮਨਜ਼ੂਰੀਆਂ ਨੂੰ ਲੌਗ ਕਰਨਾ ਪਰ kill-switch ਸਰਗਰਮੀਆਂ ਵਰਗੇ ਮਨੁੱਖੀ ਓਵਰਰਾਈਡਾਂ ਨੂੰ ਨਹੀਂ।

---

## AD.18 Monitoring, Detection & Incident Response
## AD.18 ਨਿਗਰਾਨੀ, ਪਛਾਣ, ਅਤੇ ਘਟਨਾ ਪ੍ਰਤੀਕਿਰਿਆ

Detect AI-specific abuse, drift, and anomalies, and respond to incidents.

AI-ਵਿਸ਼ੇਸ਼ ਦੁਰਵਰਤੋਂ, ਡ੍ਰਿਫ਼ਟ, ਅਤੇ ਅਸਧਾਰਨਤਾਵਾਂ ਦਾ ਪਤਾ ਲਗਾਓ, ਅਤੇ ਘਟਨਾਵਾਂ ਦਾ ਜਵਾਬ ਦਿਓ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Automated tool containment triggered by policy violations | C9.3.8 |
| Extraction-attempt detector fed by query-pattern analysis | C11.3.1 |
| Response measures triggered on detection of suspected model extraction | C11.3.4 |
| Signature-based detection and alerting on jailbreak patterns, prompt injection, and adversarial inputs | C12.2.1 |
| Behavioral anomaly detection (unusual conversation patterns, excessive retries, systematic probing) | C12.2.2 |
| Custom detection rules for AI-specific threat patterns (coordinated jailbreak attempts, prompt injection, system prompt extraction) | C12.2.3 |
| Extraction-alert events including offending query metadata | C12.2.4 |
| Granular token-usage attribution (per user, session, feature endpoint, team or workspace) | C12.2.5 |
| Monitoring of LLM API traffic for covert-channel and command-and-control indicators | C12.2.6 |
| Data drift detection using methods matched to the input type (KS test or PSI for tabular, embedding-distance for text/image) | C12.3.1 |
| Hallucination detection monitoring of model outputs | C12.3.2 |
| Hallucination rates tracked as continuous time-series metrics | C12.3.3 |
| Distinction of unexplained behavioral shifts from gradual operational drift | C12.3.4 |
| Security evaluation and threat-landscape assessment for autonomous action triggers | C12.4.1 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਨੀਤੀ ਉਲੰਘਣਾਵਾਂ ਦੁਆਰਾ ਸ਼ੁਰੂ ਕੀਤੀ ਸਵੈਚਾਲਿਤ ਟੂਲ ਘੇਰਾਬੰਦੀ | C9.3.8 |
| ਕਿਊਰੀ-ਪੈਟਰਨ ਵਿਸ਼ਲੇਸ਼ਣ ਤੋਂ ਇਨਪੁੱਟ ਲੈਣ ਵਾਲਾ extraction-ਕੋਸ਼ਿਸ਼ ਡਿਟੈਕਟਰ | C11.3.1 |
| ਸ਼ੱਕੀ model extraction ਦੀ ਪਛਾਣ ਹੋਣ 'ਤੇ ਸ਼ੁਰੂ ਹੋਣ ਵਾਲੇ ਜਵਾਬੀ ਉਪਾਅ | C11.3.4 |
| jailbreak ਪੈਟਰਨਾਂ, prompt ਇੰਜੈਕਸ਼ਨ, ਅਤੇ ਵਿਰੋਧੀ ਇਨਪੁੱਟਾਂ ਉੱਤੇ ਸਿਗਨੇਚਰ-ਆਧਾਰਿਤ ਪਛਾਣ ਅਤੇ ਚੇਤਾਵਨੀ | C12.2.1 |
| ਵਿਵਹਾਰਕ ਅਸਧਾਰਨਤਾ ਪਛਾਣ (ਅਸਧਾਰਨ ਗੱਲਬਾਤ ਪੈਟਰਨ, ਹੱਦੋਂ ਵੱਧ ਮੁੜ-ਕੋਸ਼ਿਸ਼ਾਂ, ਵਿਵਸਥਿਤ ਟੋਹ) | C12.2.2 |
| AI-ਵਿਸ਼ੇਸ਼ ਖ਼ਤਰਾ ਪੈਟਰਨਾਂ ਲਈ ਕਸਟਮ ਪਛਾਣ ਨਿਯਮ (ਤਾਲਮੇਲ ਵਾਲੀਆਂ jailbreak ਕੋਸ਼ਿਸ਼ਾਂ, prompt ਇੰਜੈਕਸ਼ਨ, system prompt extraction) | C12.2.3 |
| ਦੋਸ਼ੀ ਕਿਊਰੀ ਦਾ ਮੈਟਾਡਾਟਾ ਸ਼ਾਮਲ ਕਰਨ ਵਾਲੀਆਂ extraction-ਚੇਤਾਵਨੀ ਘਟਨਾਵਾਂ | C12.2.4 |
| ਬਾਰੀਕ ਟੋਕਨ-ਵਰਤੋਂ ਨਿਰਧਾਰਨ (ਪ੍ਰਤੀ ਉਪਭੋਗਤਾ, ਸੈਸ਼ਨ, ਫ਼ੀਚਰ ਐਂਡਪੁਆਇੰਟ, ਟੀਮ ਜਾਂ ਵਰਕਸਪੇਸ) | C12.2.5 |
| ਲੁਕਵੇਂ-ਚੈਨਲ ਅਤੇ command-and-control ਸੰਕੇਤਾਂ ਲਈ LLM API ਟਰੈਫ਼ਿਕ ਦੀ ਨਿਗਰਾਨੀ | C12.2.6 |
| ਇਨਪੁੱਟ ਕਿਸਮ ਨਾਲ ਮੇਲ ਖਾਂਦੀਆਂ ਵਿਧੀਆਂ ਵਰਤ ਕੇ ਡਾਟਾ ਡ੍ਰਿਫ਼ਟ ਪਛਾਣ (ਸਾਰਣੀਬੱਧ ਲਈ KS test ਜਾਂ PSI, ਟੈਕਸਟ/ਚਿੱਤਰ ਲਈ embedding-ਦੂਰੀ) | C12.3.1 |
| ਮਾਡਲ ਆਊਟਪੁੱਟ ਦੀ hallucination (ਮਨਘੜਤ ਸਮੱਗਰੀ) ਪਛਾਣ ਨਿਗਰਾਨੀ | C12.3.2 |
| hallucination ਦਰਾਂ ਦਾ ਲਗਾਤਾਰ ਸਮਾਂ-ਲੜੀ ਮੈਟ੍ਰਿਕਾਂ ਵਜੋਂ ਟਰੈਕ ਹੋਣਾ | C12.3.3 |
| ਅਣ-ਵਿਆਖਿਆਤ ਵਿਵਹਾਰਕ ਤਬਦੀਲੀਆਂ ਨੂੰ ਹੌਲੀ-ਹੌਲੀ ਹੋਣ ਵਾਲੇ ਸੰਚਾਲਨ ਡ੍ਰਿਫ਼ਟ ਤੋਂ ਵੱਖ ਕਰਨਾ | C12.3.4 |
| ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਕਾਰਵਾਈ ਦੇ ਟ੍ਰਿਗਰਾਂ ਲਈ ਸੁਰੱਖਿਆ ਮੁਲਾਂਕਣ ਅਤੇ ਖ਼ਤਰਾ-ਪਰਿਦ੍ਰਿਸ਼ ਮੁਲਾਂਕਣ | C12.4.1 |

**Common pitfalls:** not correlating AI-specific events with broader SIEM alerts; treating drift as a scheduled check rather than continuous monitoring; lacking AI-specific forensic tooling during an incident.

**ਆਮ ਗਲਤੀਆਂ:** AI-ਵਿਸ਼ੇਸ਼ ਘਟਨਾਵਾਂ ਦਾ ਵਡੇਰੀਆਂ SIEM ਚੇਤਾਵਨੀਆਂ ਨਾਲ ਸਹਿ-ਸੰਬੰਧ ਨਾ ਬਣਾਉਣਾ; ਡ੍ਰਿਫ਼ਟ ਨੂੰ ਲਗਾਤਾਰ ਨਿਗਰਾਨੀ ਦੀ ਬਜਾਏ ਸਮਾਂ-ਸਾਰਣੀ ਵਾਲੀ ਜਾਂਚ ਸਮਝਣਾ; ਘਟਨਾ ਦੌਰਾਨ AI-ਵਿਸ਼ੇਸ਼ ਫ਼ੋਰੈਂਸਿਕ ਸੰਦਾਂ ਦਾ ਨਾ ਹੋਣਾ।

---

## AD.19 Human Oversight & Shutdown Control
## AD.19 ਮਨੁੱਖੀ ਨਿਗਰਾਨੀ ਅਤੇ ਬੰਦ ਕਰਨ ਦਾ ਨਿਯੰਤਰਣ

Require human approval for high-impact actions and provide reliable, exercised shutdown and graceful-degradation paths under human control.

ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੀਆਂ ਕਾਰਵਾਈਆਂ ਲਈ ਮਨੁੱਖੀ ਮਨਜ਼ੂਰੀ ਦੀ ਲੋੜ ਰੱਖੋ, ਅਤੇ ਮਨੁੱਖੀ ਨਿਯੰਤਰਣ ਹੇਠ ਭਰੋਸੇਯੋਗ, ਪਰਖੇ ਹੋਏ ਬੰਦ ਕਰਨ ਅਤੇ ਸੁਚੱਜੀ ਗਿਰਾਵਟ (graceful degradation) ਦੇ ਰਾਹ ਪ੍ਰਦਾਨ ਕਰੋ।

| Control / Technique | Requirement IDs |
| --- | --- |
| Swarm-level kill-switch that halts all active agent instances | C9.1.3 |
| Runtime blocking of privileged, high-impact, or irreversible actions until explicit human approval is received and verified | C9.2.1 |
| Approval requests displaying canonicalized, complete action parameters (diffs, commands, recipients, amounts, resources, scopes) without truncation | C9.2.2 |
| Trusted reversibility classification for each high-impact action (read-only, reversible, externally reversible, irreversible) | C9.2.3 |
| Runtime enforcement of reversibility classifications (block, require approval, or restrict) | C9.2.4 |
| Restriction and bounding of any self-modification capability (prompt rewriting, tool-list changes, parameter updates) | C9.2.5 |
| AI-augmented review of planned high-risk actions, adding to (not replacing) the deterministic policy gate | C9.2.6 |
| Protection of the AI-augmented review mechanism against prompt-injection bypass | C9.2.7 |
| Approvals cryptographically bound to parameters, requester identity, execution context, and a single-use nonce | C9.2.8 |
| Isolation of approval-issuing key material or credentials from the agent runtime | C9.2.9 |
| Multi-step or multi-agent chains enforcing the highest-impact reversibility classification in the chain | C9.2.10 |
| Manual kill-switch to immediately halt model inference and outputs | C9.6.1 |
| Fail-closed blocking of a pending action when a human-approval gate is not satisfied within the defined time | C9.6.2 |
| Kill-switch commands delivered through an out-of-band channel isolated from the agent runtime | C9.6.3 |
| Explicit consent dialogue and cancellation option on installation of a local MCP server | C10.4.7 |

| ਨਿਯੰਤਰਣ / ਤਕਨੀਕ | ਲੋੜ ID |
| --- | --- |
| ਸਵਾਰਮ-ਪੱਧਰੀ kill-switch ਜੋ ਸਾਰੇ ਸਰਗਰਮ ਏਜੰਟ ਇੰਸਟਾਂਸਾਂ ਨੂੰ ਰੋਕ ਦਿੰਦਾ ਹੈ | C9.1.3 |
| ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ, ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੀਆਂ, ਜਾਂ ਗ਼ੈਰ-ਉਲਟਾਉਣਯੋਗ ਕਾਰਵਾਈਆਂ ਦੀ ਰਨਟਾਈਮ ਰੋਕ, ਜਦੋਂ ਤੱਕ ਸਪੱਸ਼ਟ ਮਨੁੱਖੀ ਮਨਜ਼ੂਰੀ ਪ੍ਰਾਪਤ ਅਤੇ ਤਸਦੀਕ ਨਾ ਹੋ ਜਾਵੇ | C9.2.1 |
| ਮਨਜ਼ੂਰੀ ਬੇਨਤੀਆਂ ਜੋ ਕੈਨੋਨੀਕਲਾਈਜ਼ ਕੀਤੇ, ਸੰਪੂਰਨ ਕਾਰਵਾਈ ਪੈਰਾਮੀਟਰ (diff, ਕਮਾਂਡਾਂ, ਪ੍ਰਾਪਤਕਰਤਾ, ਰਕਮਾਂ, ਸਰੋਤ, ਸਕੋਪ) ਬਿਨਾਂ ਕਟੌਤੀ ਦੇ ਦਿਖਾਉਂਦੀਆਂ ਹਨ | C9.2.2 |
| ਹਰ ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੀ ਕਾਰਵਾਈ ਲਈ ਭਰੋਸੇਯੋਗ ਉਲਟਾਉਣਯੋਗਤਾ ਵਰਗੀਕਰਨ (ਸਿਰਫ਼-ਪੜ੍ਹਨਯੋਗ, ਉਲਟਾਉਣਯੋਗ, ਬਾਹਰੀ ਤੌਰ 'ਤੇ ਉਲਟਾਉਣਯੋਗ, ਗ਼ੈਰ-ਉਲਟਾਉਣਯੋਗ) | C9.2.3 |
| ਉਲਟਾਉਣਯੋਗਤਾ ਵਰਗੀਕਰਨਾਂ ਦਾ ਰਨਟਾਈਮ ਲਾਗੂਕਰਨ (ਰੋਕਣਾ, ਮਨਜ਼ੂਰੀ ਦੀ ਲੋੜ ਪਾਉਣੀ, ਜਾਂ ਸੀਮਤ ਕਰਨਾ) | C9.2.4 |
| ਕਿਸੇ ਵੀ ਸਵੈ-ਸੋਧ ਸਮਰੱਥਾ (prompt ਮੁੜ-ਲਿਖਣਾ, ਟੂਲ-ਸੂਚੀ ਤਬਦੀਲੀਆਂ, ਪੈਰਾਮੀਟਰ ਅੱਪਡੇਟ) ਦੀ ਪਾਬੰਦੀ ਅਤੇ ਸੀਮਾਬੰਦੀ | C9.2.5 |
| ਯੋਜਨਾਬੱਧ ਉੱਚ-ਜੋਖਮ ਕਾਰਵਾਈਆਂ ਦੀ AI-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਸਮੀਖਿਆ, ਜੋ ਨਿਸ਼ਚਿਤ ਨੀਤੀ ਗੇਟ ਵਿੱਚ ਵਾਧਾ ਕਰਦੀ ਹੈ (ਉਸ ਦੀ ਥਾਂ ਨਹੀਂ ਲੈਂਦੀ) | C9.2.6 |
| AI-ਸਹਾਇਤ ਪ੍ਰਾਪਤ ਸਮੀਖਿਆ ਵਿਧੀ ਦੀ prompt ਇੰਜੈਕਸ਼ਨ ਰਾਹੀਂ ਬਾਈਪਾਸ ਵਿਰੁੱਧ ਸੁਰੱਖਿਆ | C9.2.7 |
| ਮਨਜ਼ੂਰੀਆਂ ਦਾ ਪੈਰਾਮੀਟਰਾਂ, ਬੇਨਤੀਕਰਤਾ ਦੀ ਪਛਾਣ, ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਸੰਦਰਭ, ਅਤੇ ਇੱਕ-ਵਾਰੀ-ਵਰਤੋਂ ਵਾਲੇ ਨੌਂਸ ਨਾਲ ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਬੰਧਨ | C9.2.8 |
| ਮਨਜ਼ੂਰੀ ਜਾਰੀ ਕਰਨ ਵਾਲੀ ਕੁੰਜੀ ਸਮੱਗਰੀ ਜਾਂ ਕ੍ਰੈਡੈਂਸ਼ੀਅਲਾਂ ਦੀ ਏਜੰਟ ਰਨਟਾਈਮ ਤੋਂ ਅਲੱਗ-ਥਲੱਗਤਾ | C9.2.9 |
| ਬਹੁ-ਪੜਾਵੀ ਜਾਂ ਬਹੁ-ਏਜੰਟ ਲੜੀਆਂ ਵਿੱਚ ਲੜੀ ਦੇ ਸਭ ਤੋਂ ਉੱਚ-ਪ੍ਰਭਾਵ ਵਾਲੇ ਉਲਟਾਉਣਯੋਗਤਾ ਵਰਗੀਕਰਨ ਦਾ ਲਾਗੂਕਰਨ | C9.2.10 |
| ਮਾਡਲ ਇਨਫ਼ਰੈਂਸ ਅਤੇ ਆਊਟਪੁੱਟ ਨੂੰ ਤੁਰੰਤ ਰੋਕਣ ਲਈ ਹੱਥੀਂ ਚਲਾਈ ਜਾਣ ਵਾਲੀ kill-switch | C9.6.1 |
| ਪਰਿਭਾਸ਼ਿਤ ਸਮੇਂ ਦੇ ਅੰਦਰ ਮਨੁੱਖੀ-ਮਨਜ਼ੂਰੀ ਗੇਟ ਪੂਰਾ ਨਾ ਹੋਣ 'ਤੇ ਬਕਾਇਆ ਕਾਰਵਾਈ ਦੀ ਨਾਕਾਮੀ-'ਤੇ-ਬੰਦ[^0x91-fail-closed] (fail-closed) ਰੋਕ | C9.6.2 |
| ਏਜੰਟ ਰਨਟਾਈਮ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਆਊਟ-ਆਫ਼-ਬੈਂਡ ਚੈਨਲ ਰਾਹੀਂ ਦਿੱਤੀਆਂ ਜਾਣ ਵਾਲੀਆਂ kill-switch ਕਮਾਂਡਾਂ | C9.6.3 |
| ਸਥਾਨਕ MCP ਸਰਵਰ ਦੀ ਸਥਾਪਨਾ 'ਤੇ ਸਪੱਸ਼ਟ ਸਹਿਮਤੀ ਸੰਵਾਦ ਅਤੇ ਰੱਦ ਕਰਨ ਦਾ ਵਿਕਲਪ | C10.4.7 |

**Common pitfalls:** documenting a high-risk action policy never wired to a runtime gate; binding approval to parameters without binding to identity or context; defaulting to fail-open when the approver does not respond; assuming an in-band kill-switch will work against a compromised agent; implementing a kill-switch that is never exercised.

**ਆਮ ਗਲਤੀਆਂ:** ਉੱਚ-ਜੋਖਮ ਕਾਰਵਾਈ ਨੀਤੀ ਨੂੰ ਦਸਤਾਵੇਜ਼ਬੱਧ ਕਰਨਾ ਪਰ ਉਸ ਨੂੰ ਕਦੇ ਰਨਟਾਈਮ ਗੇਟ ਨਾਲ ਨਾ ਜੋੜਨਾ; ਮਨਜ਼ੂਰੀ ਨੂੰ ਪੈਰਾਮੀਟਰਾਂ ਨਾਲ ਬੰਨ੍ਹਣਾ ਪਰ ਪਛਾਣ ਜਾਂ ਸੰਦਰਭ ਨਾਲ ਨਹੀਂ; ਮਨਜ਼ੂਰੀ ਦੇਣ ਵਾਲੇ ਦੇ ਜਵਾਬ ਨਾ ਦੇਣ 'ਤੇ ਡਿਫ਼ਾਲਟ ਰੂਪ ਵਿੱਚ ਨਾਕਾਮੀ-'ਤੇ-ਖੁੱਲ੍ਹਾ[^0x91-fail-open] (fail-open) ਰਹਿਣਾ; ਇਹ ਮੰਨ ਲੈਣਾ ਕਿ ਇਨ-ਬੈਂਡ kill-switch ਸਮਝੌਤਾ ਹੋਏ ਏਜੰਟ ਵਿਰੁੱਧ ਕੰਮ ਕਰੇਗਾ; ਅਜਿਹਾ kill-switch ਲਾਗੂ ਕਰਨਾ ਜਿਸ ਨੂੰ ਕਦੇ ਪਰਖਿਆ ਹੀ ਨਾ ਜਾਵੇ।

---

## References
## ਹਵਾਲੇ

* [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)
* [ISO/IEC 42001:2023: AI Management Systems Requirements](https://www.iso.org/standard/42001)
* [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
* [NIST SP 800-218A: Secure Software Development Practices for Generative AI](https://csrc.nist.gov/pubs/sp/800/218/a/final)

[^0x91-appendix]: **Appendix** (EN) -> ਅੰਤਿਕਾ — the settled Panjabi term for a document appendix in academic/government publishing; the division letter stays Latin as a cross-reference target, matching Appendix A and Appendix C. Full discussion: OPEN-QUESTIONS.md Q121.
[^0x91-non-normative]: **non-normative** (EN) -> ਗ਼ੈਰ-ਨਿਯਮਬੱਧ — built on ਨਿਯਮ ("rule"), not ਲਾਜ਼ਮੀ (bound corpus-wide to the hard "must" of requirement text), so the negation reads as a statement about document status rather than obligation strength. Full discussion: OPEN-QUESTIONS.md Q96.
[^0x91-source-of-truth]: **source of truth** (EN) -> ਫ਼ੈਸਲਾਕੁੰਨ ਸਰੋਤ — "decisive, settling the matter," built on the already-settled ਫ਼ੈਸਲਾ (ਨੀਤੀ ਫ਼ੈਸਲਾ ਬਿੰਦੂ); ਸੱਚ ਦਾ ਸਰੋਤ was rejected on Gurmat grounds since ਸੱਚ/ਸਤਿ is load-bearing devotional vocabulary for Divine Truth. Full discussion: OPEN-QUESTIONS.md Q97.
[^0x91-principal-identity-entity]: **principal** (security principal) (EN) -> ਪਛਾਣ-ਇਕਾਈ — built on the already-settled ਪਛਾਣ ("identity") rather than ਕਰਤਾ, which is rejected on Gurmat grounds as load-bearing devotional vocabulary for a divine doer. Full discussion: OPEN-QUESTIONS.md Q124.
[^0x91-pass-through]: **pass-through** (of client access tokens) (EN) -> ਅੱਗੇ ਲੰਘਾਉਣਾ — states the mechanism the control forbids (relaying a client's token unchanged downstream), deliberately kept distinct from ਅੱਗੇ ਸੰਚਾਰਿਤ ਕਰਨਾ, which names the *approved* propagation of a scope-limited delegation token elsewhere in this file. Full discussion: OPEN-QUESTIONS.md Q101.
[^0x91-common-pitfalls]: **Common pitfalls** (EN) -> ਆਮ ਗਲਤੀਆਂ — a recurring implementation mistake, not a vulnerability class or an attacker's trap, so the plain word (spelled without nukta, matching the corpus's existing ਗਲਤੀ ਪ੍ਰਬੰਧਨ) is the honest one; ਫੰਦਾ and ਭੁਲੇਖਾ were rejected as devotionally loaded or already spoken for. Full discussion: OPEN-QUESTIONS.md Q98.
[^0x91-authenticity]: **authenticity** (EN) -> ਅਸਲੀਅਤ — a sixth distinct verb-precision term alongside the already-locked verify/validate/authenticate/certify/attest cluster; kept clear of ਪ੍ਰਮਾਣਿਕਤਾ, which renders *validation* throughout the corpus including elsewhere in this same appendix. Full discussion: OPEN-QUESTIONS.md Q99.
[^0x91-replay]: **replay** (EN) -> retained in Latin, glossed (ਦੁਹਰਾਓ) — conforms to the C10 chapter's decision so the named attack class stays searchable across the corpus; an earlier draft's transliterated ਰੀਪਲੇ was normalised away. Full discussion: OPEN-QUESTIONS.md Q102.
[^0x91-lateral-movement]: **lateral movement** (EN) -> retained in Latin, glossed ਪਾਸੇ-ਵੱਲ ਫੈਲਾਅ ("spread sideways") — a MITRE ATT&CK tactic name, so the English stays for cross-reference against the threat-intel literature while the gloss carries the descriptive sense. Full discussion: OPEN-QUESTIONS.md Q103.
[^0x91-downgrade]: **downgrade** (protocol) (EN) -> ਡਾਊਨਗ੍ਰੇਡ — the one term in this control row not already settled by the C10 chapter's transport vocabulary; kept as a loan since it names a forced protocol-version rollback, consistent with the corpus's treatment of protocol-layer terms. Full discussion: OPEN-QUESTIONS.md Q100.
[^0x91-immutable]: **immutable** (EN) -> ਅਪਰਿਵਰਤਨਸ਼ੀਲਤਾ — this exact requirement (C8.1.2) was found paraphrased elsewhere in the corpus as "cannot be changed," which hid the term from a reader searching for it beside this file's own index entry; this site is the corpus's standing form. Full discussion: OPEN-QUESTIONS.md Q112.
[^0x91-principal-loan]: **per-principal** (EN) -> ਪ੍ਰਿੰਸੀਪਲ (loan) — a recorded, still-open corpus split: this site and C11.2.2 use the loan, while C9.4.1 and another site in this same file use ਪਛਾਣ-ਇਕਾਈ for the same underlying concept; flagged for a reviewer rather than silently resolved. Full discussion: OPEN-QUESTIONS.md Q124.
[^0x91-fail-closed]: **fail-closed** (EN) -> ਨਾਕਾਮੀ-'ਤੇ-ਬੰਦ — the literal compound was chosen over the shorter transliterated loan because the control states fail-closed and names fail-open as its pitfall in the same family, and only the literal compound inverts cleanly for both. Full discussion: OPEN-QUESTIONS.md Q104.
[^0x91-fail-open]: **fail-open** (EN) -> ਨਾਕਾਮੀ-'ਤੇ-ਖੁੱਲ੍ਹਾ — the inverse of ਨਾਕਾਮੀ-'ਤੇ-ਬੰਦ, deliberately not rendered as "safe failure," which would name the desirable outcome rather than the mechanism and make this pitfall untranslatable as fail-closed's opposite. Full discussion: OPEN-QUESTIONS.md Q104.
