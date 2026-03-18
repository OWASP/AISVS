# C05: Access Control & Identity for AI Components & Users

> **Source:** [`1.0/en/0x10-C05-Access-Control-and-Identity.md`](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md)
> **Requirements:** 26 | **Sections:** 6

## Control Objective

Effective access control for AI systems requires robust identity management, context-aware authorization, and runtime enforcement following zero-trust principles.

---

## Section Breakdown

| Section | Title | Reqs | IDs |
|---------|-------|:----:|-----|
| C5.1 | Identity Management & Authentication | 3 | 5.1.1–5.1.3 |
| C5.2 | Authorization & Policy | 8 | 5.2.1–5.2.8 |
| C5.3 | Query-Time Security Enforcement | 4 | 5.3.1–5.3.4 |
| C5.4 | Output Filtering & Data Loss Prevention | 3 | 5.4.1–5.4.3 |
| C5.5 | Multi-Tenant Isolation | 4 | 5.5.1–5.5.4 |
| C5.6 | Autonomous Agent Authorization | 4 | 5.6.1–5.6.4 |

---

## Threat Landscape

Known attacks, real-world incidents, and threat vectors relevant to this chapter:

- Privilege escalation through prompt injection causing the model to act with elevated permissions
- Cross-tenant data leakage in shared AI infrastructure
- Agent identity spoofing in multi-agent systems
- Confused deputy attacks where AI tools act with the user's credentials beyond intended scope

### Notable Incidents & Research

_Add links to CVEs, published attacks, blog posts, and academic papers relevant to this chapter._

| Date | Incident / Paper | Relevance | Link |
|------|------------------|-----------|------|
| | | | |

---

## Tooling & Implementation

Current tools, frameworks, and libraries that help implement these controls:

- **Policy engines:** OPA (Open Policy Agent), Cedar (AWS), Casbin
- **Identity:** SPIFFE/SPIRE for workload identity, OAuth 2.0 for user-facing AI apps
- **DLP:** Google DLP API, Microsoft Purview, custom regex/NER-based PII filters
- **Multi-tenant isolation:** Kubernetes namespaces, database row-level security

### Implementation Maturity

| Control Area | Tooling Maturity | Notes |
|--------------|:---:|-------|
| C5.1 Identity Management & Authentication | _TBD_ | |
| C5.2 Authorization & Policy | _TBD_ | |
| C5.3 Query-Time Security Enforcement | _TBD_ | |
| C5.4 Output Filtering & Data Loss Prevention | _TBD_ | |
| C5.5 Multi-Tenant Isolation | _TBD_ | |
| C5.6 Autonomous Agent Authorization | _TBD_ | |

---

## Open Research Questions

- [ ] How should authorization policies account for the non-deterministic nature of AI outputs?
- [ ] What's the right model for agent identity in multi-agent orchestration?
- [ ] How do you enforce query-time access control in vector databases that lack native RBAC?
- [ ] Should AI systems have their own identity distinct from the calling user?

---

## Related Standards & Cross-References

- [NIST SP 800-162: Guide to ABAC](https://csrc.nist.gov/pubs/sp/800/162/final)
- [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
- [NIST IR 8360: ML for Access Control Policy Verification](https://csrc.nist.gov/pubs/ir/8360/final)

### AISVS Cross-Chapter Links

_Which other AISVS chapters have related or overlapping requirements?_

| Related Chapter | Overlap Area | Notes |
|-----------------|--------------|-------|
| | | |

---

## Community Notes

_Space for contributor observations, discussion, and context that doesn't fit elsewhere._

---

