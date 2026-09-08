<!-- Translation Status: ✅ Complete -->
<!-- Original: 1.0/en/0x10-C05-Access-Control-and-Identity.md -->
<!-- Translator: GeeksikhSecurity -->

# C5 Access Control & Identity for AI Components & Users
# C5 AI ਕੰਪੋਨੈਂਟਾਂ[^0x10-C05-component] ਅਤੇ ਉਪਭੋਗਤਾਵਾਂ ਲਈ ਪਹੁੰਚ ਕੰਟਰੋਲ ਅਤੇ ਪਛਾਣ

## Control Objective
## ਨਿਯੰਤਰਣ ਉਦੇਸ਼

This chapter addresses access control challenges that AI systems introduce beyond traditional application security.

ਇਹ ਅਧਿਆਇ ਉਹਨਾਂ ਪਹੁੰਚ ਕੰਟਰੋਲ ਚੁਣੌਤੀਆਂ ਨੂੰ ਸੰਬੋਧਿਤ ਕਰਦਾ ਹੈ ਜੋ AI ਸਿਸਟਮ ਰਵਾਇਤੀ ਐਪਲੀਕੇਸ਼ਨ ਸੁਰੱਖਿਆ ਤੋਂ ਪਰੇ ਪੇਸ਼ ਕਰਦੇ ਹਨ।

---

## C5.1 Authentication
## C5.1 ਪ੍ਰਮਾਣੀਕਰਨ

AI agents and human users accessing resources must be properly authenticated and authorized for their level of access.

ਸਰੋਤਾਂ ਤੱਕ ਪਹੁੰਚ ਕਰਨ ਵਾਲੇ AI ਏਜੰਟਾਂ[^0x10-C05-agent] ਅਤੇ ਮਨੁੱਖੀ ਉਪਭੋਗਤਾਵਾਂ ਦਾ ਉਹਨਾਂ ਦੀ ਪਹੁੰਚ ਦੇ ਪੱਧਰ ਲਈ ਸਹੀ ਢੰਗ ਨਾਲ ਪ੍ਰਮਾਣੀਕਰਨ (authentication) ਅਤੇ ਅਧਿਕਾਰੀਕਰਨ (authorization) ਹੋਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.1.1** | **Verify that** high-risk AI operations (model deployment, weight export, training data access, production configuration changes) require step-up authentication. | 3 |
| **5.1.2** | **Verify that** AI agents in federated or multi-system deployments authenticate using short-lived, minimal-scoped, cryptographically signed tokens. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.1.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਉੱਚ-ਜੋਖਮ ਵਾਲੀਆਂ AI ਕਾਰਵਾਈਆਂ (ਮਾਡਲ ਤੈਨਾਤੀ, ਮਾਡਲ ਵੇਟਸ ਨਿਰਯਾਤ, ਸਿਖਲਾਈ ਡਾਟਾ ਪਹੁੰਚ, ਪ੍ਰੋਡਕਸ਼ਨ ਸੰਰਚਨਾ ਤਬਦੀਲੀਆਂ) ਲਈ ਸਟੈੱਪ-ਅੱਪ ਪ੍ਰਮਾਣੀਕਰਨ[^0x10-C05-stepup] (step-up authentication) ਲੋੜੀਂਦਾ ਹੈ। | 3 |
| **5.1.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਫ਼ੈਡਰੇਟਿਡ[^0x10-C05-federated] ਜਾਂ ਬਹੁ-ਸਿਸਟਮ ਤੈਨਾਤੀਆਂ ਵਿੱਚ AI ਏਜੰਟ ਥੋੜ੍ਹੇ ਸਮੇਂ ਵਾਲੇ, ਘੱਟੋ-ਘੱਟ ਸਕੋਪ ਵਾਲੇ, ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ ਦਸਤਖ਼ਤ ਕੀਤੇ ਟੋਕਨਾਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਪ੍ਰਮਾਣੀਕਰਨ ਕਰਦੇ ਹਨ। | 3 |

---

## C5.2 AI Resource Authorization & Classification
## C5.2 AI ਸਰੋਤ ਅਧਿਕਾਰੀਕਰਨ ਅਤੇ ਵਰਗੀਕਰਨ

The caller's authorization context must be enforced through AI-specific query pipelines (RAG retrieval, embedding lookups, inference chains) so the system does not return data the caller is not entitled to access.

ਕਾਲਰ ਦੇ ਅਧਿਕਾਰੀਕਰਨ ਸੰਦਰਭ ਨੂੰ AI-ਵਿਸ਼ੇਸ਼ ਕਿਊਰੀ ਪਾਈਪਲਾਈਨਾਂ (RAG ਪ੍ਰਾਪਤੀ[^0x10-C05-retrieval], embedding[^0x10-C05-embedding] ਖੋਜਾਂ, ਇਨਫ਼ਰੈਂਸ[^0x10-C05-inference] ਲੜੀਆਂ) ਰਾਹੀਂ ਲਾਗੂ ਕਰਨਾ ਲਾਜ਼ਮੀ ਹੈ ਤਾਂ ਜੋ ਸਿਸਟਮ ਅਜਿਹਾ ਡਾਟਾ ਵਾਪਸ ਨਾ ਕਰੇ ਜਿਸ ਤੱਕ ਪਹੁੰਚ ਦਾ ਕਾਲਰ ਨੂੰ ਹੱਕ ਨਹੀਂ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.2.1** | **Verify that** every AI resource (datasets, endpoints, vector collections, embedding indices, compute instances) enforces access controls with explicit allow-lists and default-deny policies. | 2 |
| **5.2.2** | **Verify that** retrieval pipelines (e.g., RAG queries, embedding lookups) enforce the end-user's authorization context at each retrieval and assembly stage, rather than relying solely on the service account's permissions. | 2 |
| **5.2.3** | **Verify that** sensitive data is retrieved via retrieval pipelines (e.g., RAG queries, embedding lookups) to prevent permanent storage in models. | 2 |
| **5.2.4** | **Verify that** post-inference filtering mechanisms prevent responses from including data that the requester is not authorized to receive. | 2 |
| **5.2.5** | **Verify that** the policy decision point for agent authorization is isolated from the agent's execution environment. | 2 |
| **5.2.6** | **Verify that** privileged access to model weights, training pipelines, and production AI configuration is granted just in time, with a defined maximum session duration and automatic expiry. Zero Standing Privilege (ZSP) to these resources is encouraged. | 3 |
| **5.2.7** | **Verify that** data classification labels propagate to downstream resources (embeddings, prompt caches, model outputs). | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.2.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਹਰ AI ਸਰੋਤ (ਡਾਟਾਸੈੱਟ, ਐਂਡਪੁਆਇੰਟ, ਵੈਕਟਰ ਸੰਗ੍ਰਹਿ, embedding ਇੰਡੈਕਸ, ਕੰਪਿਊਟ ਇੰਸਟਾਂਸ) ਸਪੱਸ਼ਟ allow-list ਅਤੇ ਡਿਫ਼ਾਲਟ-ਇਨਕਾਰ ਨੀਤੀਆਂ ਨਾਲ ਪਹੁੰਚ ਕੰਟਰੋਲ ਲਾਗੂ ਕਰਦਾ ਹੈ। | 2 |
| **5.2.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਪ੍ਰਾਪਤੀ ਪਾਈਪਲਾਈਨਾਂ (ਜਿਵੇਂ, RAG ਕਿਊਰੀਆਂ, embedding ਖੋਜਾਂ) ਸਿਰਫ਼ ਸੇਵਾ ਖਾਤੇ ਦੀਆਂ ਇਜਾਜ਼ਤਾਂ 'ਤੇ ਨਿਰਭਰ ਰਹਿਣ ਦੀ ਬਜਾਏ, ਹਰ ਪ੍ਰਾਪਤੀ ਅਤੇ ਅਸੈਂਬਲੀ ਪੜਾਅ 'ਤੇ ਅੰਤਮ-ਉਪਭੋਗਤਾ ਦੇ ਅਧਿਕਾਰੀਕਰਨ ਸੰਦਰਭ ਨੂੰ ਲਾਗੂ ਕਰਦੀਆਂ ਹਨ। | 2 |
| **5.2.3** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸੰਵੇਦਨਸ਼ੀਲ ਡਾਟਾ ਮਾਡਲਾਂ ਵਿੱਚ ਸਥਾਈ ਭੰਡਾਰਨ ਨੂੰ ਰੋਕਣ ਲਈ ਪ੍ਰਾਪਤੀ ਪਾਈਪਲਾਈਨਾਂ (ਜਿਵੇਂ, RAG ਕਿਊਰੀਆਂ, embedding ਖੋਜਾਂ) ਰਾਹੀਂ ਪ੍ਰਾਪਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 2 |
| **5.2.4** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇਨਫ਼ਰੈਂਸ-ਉਪਰੰਤ ਫ਼ਿਲਟਰਿੰਗ ਵਿਧੀਆਂ ਜਵਾਬਾਂ ਵਿੱਚ ਅਜਿਹਾ ਡਾਟਾ ਸ਼ਾਮਲ ਹੋਣ ਤੋਂ ਰੋਕਦੀਆਂ ਹਨ ਜਿਸਨੂੰ ਪ੍ਰਾਪਤ ਕਰਨ ਲਈ ਬੇਨਤੀਕਰਤਾ ਅਧਿਕਾਰਤ ਨਹੀਂ ਹੈ। | 2 |
| **5.2.5** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਏਜੰਟ ਅਧਿਕਾਰੀਕਰਨ ਲਈ ਨੀਤੀ ਫ਼ੈਸਲਾ ਬਿੰਦੂ[^0x10-C05-pdp] (policy decision point) ਏਜੰਟ ਦੇ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣ ਤੋਂ ਅਲੱਗ-ਥਲੱਗ ਹੈ। | 2 |
| **5.2.6** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਮਾਡਲ ਵੇਟਸ (model weights), ਸਿਖਲਾਈ ਪਾਈਪਲਾਈਨਾਂ, ਅਤੇ ਪ੍ਰੋਡਕਸ਼ਨ AI ਸੰਰਚਨਾ ਤੱਕ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ ਪਹੁੰਚ ਇੱਕ ਪਰਿਭਾਸ਼ਿਤ ਵੱਧ ਤੋਂ ਵੱਧ ਸੈਸ਼ਨ ਮਿਆਦ ਅਤੇ ਆਪਣੇ-ਆਪ ਸਮਾਪਤੀ ਦੇ ਨਾਲ, ਸਿਰਫ਼ ਲੋੜ ਪੈਣ 'ਤੇ ਹੀ (just in time) ਦਿੱਤੀ ਜਾਂਦੀ ਹੈ। ਇਹਨਾਂ ਸਰੋਤਾਂ ਲਈ Zero Standing Privilege (ZSP)[^0x10-C05-zsp] ਨੂੰ ਉਤਸ਼ਾਹਿਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ। | 3 |
| **5.2.7** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਡਾਟਾ ਵਰਗੀਕਰਨ ਲੇਬਲ ਡਾਊਨਸਟ੍ਰੀਮ ਸਰੋਤਾਂ (embeddings, prompt ਕੈਸ਼[^0x10-C05-promptcache], ਮਾਡਲ ਆਊਟਪੁੱਟ) ਤੱਕ ਅੱਗੇ ਸੰਚਾਰਿਤ ਹੁੰਦੇ ਹਨ। | 3 |

---

## C5.3 Multi-Tenant Isolation
## C5.3 ਬਹੁ-ਟੈਨੈਂਟ[^0x10-C05-tenant] ਅਲੱਗ-ਥਲੱਗਤਾ

Cross-tenant information leakage through AI-specific shared infrastructure, such as inference caches and shared model state, must be prevented.

AI-ਵਿਸ਼ੇਸ਼ ਸਾਂਝੇ ਬੁਨਿਆਦੀ ਢਾਂਚੇ, ਜਿਵੇਂ ਕਿ ਇਨਫ਼ਰੈਂਸ ਕੈਸ਼ ਅਤੇ ਸਾਂਝੀ ਮਾਡਲ ਸਥਿਤੀ, ਰਾਹੀਂ ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ ਜਾਣਕਾਰੀ ਲੀਕ ਹੋਣ ਨੂੰ ਰੋਕਣਾ ਲਾਜ਼ਮੀ ਹੈ।

| # | Description | Level |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.3.1** | **Verify that** shared model serving infrastructure prevents one tenant's fine-tuning, inference, or embedding operations from influencing or observing another tenant's operations. | 2 |
| **5.3.2** | **Verify that** one tenant cannot influence or observe another tenant's operations through shared compute resources. Satisfying this requirement typically requires hardware partitioning, confidential computing, or dedicated per-tenant compute allocation. | 3 |

| # | ਵੇਰਵਾ | ਪੱਧਰ |
| :--------: | --------------------------------------------------------------------------------------------- | :---: |
| **5.3.1** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਸਾਂਝਾ ਮਾਡਲ ਸਰਵਿੰਗ ਬੁਨਿਆਦੀ ਢਾਂਚਾ ਇੱਕ ਟੈਨੈਂਟ ਦੀਆਂ ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ, ਇਨਫ਼ਰੈਂਸ, ਜਾਂ embedding ਕਾਰਵਾਈਆਂ ਨੂੰ ਕਿਸੇ ਹੋਰ ਟੈਨੈਂਟ ਦੀਆਂ ਕਾਰਵਾਈਆਂ ਨੂੰ ਪ੍ਰਭਾਵਿਤ ਕਰਨ ਜਾਂ ਵੇਖਣ ਤੋਂ ਰੋਕਦਾ ਹੈ। | 2 |
| **5.3.2** | **ਤਸਦੀਕ ਕਰੋ ਕਿ** ਇੱਕ ਟੈਨੈਂਟ ਸਾਂਝੇ ਕੰਪਿਊਟ ਸਰੋਤਾਂ ਰਾਹੀਂ ਕਿਸੇ ਹੋਰ ਟੈਨੈਂਟ ਦੀਆਂ ਕਾਰਵਾਈਆਂ ਨੂੰ ਪ੍ਰਭਾਵਿਤ ਨਹੀਂ ਕਰ ਸਕਦਾ ਜਾਂ ਵੇਖ ਨਹੀਂ ਸਕਦਾ। ਇਸ ਲੋੜ ਨੂੰ ਪੂਰਾ ਕਰਨ ਲਈ ਆਮ ਤੌਰ 'ਤੇ ਹਾਰਡਵੇਅਰ ਵਿਭਾਜਨ, ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ[^0x10-C05-confidential] (confidential computing), ਜਾਂ ਪ੍ਰਤੀ-ਟੈਨੈਂਟ ਰਾਖਵੀਂ (dedicated) ਕੰਪਿਊਟ ਵੰਡ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ। | 3 |

---

## References
## ਹਵਾਲੇ

* [NIST SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
* [NIST SP 800-63-3: Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/3/final)
* [OAuth 2.1 (IETF Draft)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-11)
* [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
* [I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving (NDSS 2025)](https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/)

[^0x10-C05-component]: **component** (EN) -> ਕੰਪੋਨੈਂਟ — kept as the established loan (this chapter title is one of the sites that fixes it) rather than the native ਹਿੱਸਾ used for generic parts elsewhere in the corpus; a full-corpus audit found the two forms split by usage and recommended normalising the minority native sites toward this one. Full discussion: OPEN-QUESTIONS.md Q95.
[^0x10-C05-agent]: **AI agent** (EN) -> AI ਏਜੰਟ — rendered as a transliterated loan because "agent" is flagged as a high-risk anthropomorphising term, and every native alternative (ਦੂਤ "messenger", ਪ੍ਰਤੀਨਿਧ "representative") either carries devotional colour or loses the software sense. Full discussion: OPEN-QUESTIONS.md Q17.
[^0x10-C05-stepup]: **step-up authentication** (EN) -> ਸਟੈੱਪ-ਅੱਪ ਪ੍ਰਮਾਣੀਕਰਨ — the modifier is kept as a retained loan rather than translated because "step-up" names a specific industry pattern (NIST SP 800-63-3) distinct from plain re-authentication, and a descriptive Panjabi modifier would flatten that distinction. Full discussion: OPEN-QUESTIONS.md Q23.
[^0x10-C05-federated]: **federated** (EN, as in federated deployments) -> ਫ਼ੈਡਰੇਟਿਡ — spelled with the nukta ਫ਼ per the corpus-wide rule that English /f/ takes the nukta; this chapter was one of the sites normalised to match. Full discussion: OPEN-QUESTIONS.md Q52 (spelling rule recorded at Q86).
[^0x10-C05-retrieval]: **retrieval** (EN, as in RAG retrieval) -> ਪ੍ਰਾਪਤੀ — chosen because it is cognate with the verb ਪ੍ਰਾਪਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ used elsewhere in this chapter, while ਖੋਜ is deliberately reserved for "lookup/search" so the two RAG pipeline stages stay distinguishable. Full discussion: OPEN-QUESTIONS.md Q20.
[^0x10-C05-embedding]: **embedding** (EN) -> `embedding` (retained in Latin script) — kept as a retained Latin head rather than transliterated to ਏਮਬੈਡਿੰਗ because that is already the canonical hybrid pattern fixed corpus-wide (`embedding ਸਟੋਰ`, `embedding ਇੰਡੈਕਸ`). Full discussion: OPEN-QUESTIONS.md Q19.
[^0x10-C05-inference]: **inference** (EN) -> ਇਨਫ਼ਰੈਂਸ — kept as a loan rather than ਅਨੁਮਾਨ, because that word is already used elsewhere in the corpus for "expected/anticipated" and would misread inference as an estimated value rather than the act of running the model. Full discussion: OPEN-QUESTIONS.md Q18.
[^0x10-C05-pdp]: **policy decision point** (EN) -> ਨੀਤੀ ਫ਼ੈਸਲਾ ਬਿੰਦੂ — translated rather than retained because all three parts already have settled Panjabi equivalents, and the term is glossed in English on first use so it stays matchable to the NIST SP 800-207 reference this chapter cites. Full discussion: OPEN-QUESTIONS.md Q24.
[^0x10-C05-zsp]: **Zero Standing Privilege (ZSP)** (EN) -> Zero Standing Privilege (ZSP) (retained verbatim) — kept in English as a named security model, the same treatment Zero Trust Architecture gets in the reference this chapter cites, while the surrounding "privileged access" prose is translated normally. Full discussion: OPEN-QUESTIONS.md Q25.
[^0x10-C05-promptcache]: **prompt cache** (EN) -> `prompt` ਕੈਸ਼ — the head noun `prompt` stays in Latin script per the corpus-wide hybrid pattern already fixed for `prompt ਇੰਜੈਕਸ਼ਨ`, extended here to *cache*. Full discussion: OPEN-QUESTIONS.md Q21.
[^0x10-C05-tenant]: **tenant / multi-tenant** (EN) -> ਟੈਨੈਂਟ / ਬਹੁ-ਟੈਨੈਂਟ — kept as a loan rather than ਕਿਰਾਏਦਾਰ ("renter"), because the literal dictionary word denotes a person renting property and would obscure the isolation boundary this section is about. Full discussion: OPEN-QUESTIONS.md Q22.
[^0x10-C05-confidential]: **confidential computing** (EN) -> ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ — normalised from an earlier loan rendering (ਕਾਨਫ਼ੀਡੈਂਸ਼ੀਅਲ ਕੰਪਿਊਟਿੰਗ) that was the corpus's only instance of that form and read two ways against the same requirement indexed in Appendix B; the fix also protects the three-way ਭਰੋਸੇਯੋਗ / ਸੁਰੱਖਿਅਤ / ਗੁਪਤ (trusted/secure/confidential) contrast the C4 sibling chapter depends on. Full discussion: OPEN-QUESTIONS.md Q50.
