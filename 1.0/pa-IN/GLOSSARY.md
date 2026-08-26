# Shared Panjabi Terminology — seeded from the OWASP ASVS 5.0 pa-IN corpus

**Purpose:** single source of truth for terms that already have a settled Panjabi
rendering in the sibling OWASP ASVS 5.0 Panjabi translation
(`GeeksikhSecurity/ASVS`, branch `panjabi-translation-v5`, `5.0/pa-IN/`). Check
here before coining a new rendering for any term below — AISVS reuses the ASVS
corpus's picks so a reader moving between both standards sees one consistent
vocabulary, not two competing translations of the same security concept.

Terms **not** in this file are AISVS-specific (prompt injection, model weights,
embeddings, agentic, guardrail, hallucination, etc.) and have no ASVS
precedent — translate those fresh per `TRANSLATION-RULES.md` and log the
decision in this repo's own `OPEN-QUESTIONS.md`.

Source: `5.0/pa-IN/TRANSLATION-RULES.md` §4 (locked terms) and
`5.0/pa-IN/OPEN-QUESTIONS.md` Q5 (resolved), Q13, Q19 (corpus-wide
normalisations applied 2026-08-22). Status column reflects the ASVS side —
`locked` means pinned in `TRANSLATION-RULES.md`; `normalised` means the
corpus converged on it but it has not gone through Sangat sign-off; both are
safe defaults for AISVS.

## Core / locked terms

| EN term | Panjabi | Type | Status |
|---|---|---|---|
| fraud / scam | ਠੱਗੀ | T | locked |
| community (generic) | ਭਾਈਚਾਰਾ | T | locked |
| community (named Sikh religious context only) | ਸੰਗਤ | T | locked |
| self-contained | ਸਵੈ-ਨਿਰਭਰ | T | locked |
| integrity | ਅਖੰਡਤਾ | T | locked |
| validity period | ਜਾਇਜ਼ਤਾ ਮਿਆਦ | T | locked |
| context | ਸੰਦਰਭ | T | locked |
| issuer | ਜਾਰੀਕਰਤਾ | T | locked |
| tampering | ਛੇੜਛਾੜ | T | locked |
| verify | ਤਸਦੀਕ ਕਰੋ | T | locked |
| validate | ਪ੍ਰਮਾਣਿਤ ਕਰਨਾ | T | locked |
| authentication | ਪ੍ਰਮਾਣੀਕਰਨ | T | locked |
| authorization | ਅਧਿਕਾਰੀਕਰਨ | T | locked (Q3) |
| entitlements / right | ਹੱਕ / ਅਧਿਕਾਰ | T | locked (Q3 — do not use ਅਧਿਕਾਰ for entitlements, it collides with authorization) |
| posture / state | ਸਥਿਤੀ | T | **locked — NEVER ਮੁਦਰਾ (yoga-connoted, Gurmat violation, Q5)** |
| certification / certify | ਸਰਟੀਫ਼ਿਕੇਸ਼ਨ | L | locked (Q18 — never ਪ੍ਰਮਾਣੀਕਰਨ, that's authentication) |
| weakness (vs vulnerability) | ਖ਼ਾਮੀ | T | locked (ਕਮਜ਼ੋਰੀ reserved for "vulnerability") |
| risk | ਜੋਖਮ | T | normalised (Q13) |
| threat | ਖ਼ਤਰਾ | T | normalised (Q13) — keep distinct from risk |
| must / must not (hard requirement) | ਲਾਜ਼ਮੀ ਹੈ / ਨਹੀਂ … ਚਾਹੀਦਾ | — | normalised (Q13) — never soften to "cannot"/ਟਾਲ ਸਕਦਾ |

## AI/security infra terms likely reused in AISVS

| EN term | Panjabi | Type | Status |
|---|---|---|---|
| access control | ਪਹੁੰਚ ਕੰਟਰੋਲ / ਪਹੁੰਚ | T/L | corpus precedent |
| configuration / configure (verb) | ਸੰਰਚਨਾ / ਸੰਰਚਿਤ ਕਰਨਾ | T | normalised (Q19 — noun locked; verb still had 2 competing forms in ASVS, prefer ਸੰਰਚਿਤ ਕਰਨਾ) |
| inventory (SBOM/asset/model registry) | ਇਨਵੈਂਟਰੀ | L | normalised (Q19 — majority usage, not ਵਸਤੂ-ਸੂਚੀ) |
| connection / connection pool | ਕਨੈਕਸ਼ਨ / ਕਨੈਕਸ਼ਨ ਪੂਲ | L | normalised (Q19) |
| retention | ਧਾਰਨ | T | normalised (Q19 — never ਸੰਭਾਲ, collides with "handling") |
| error handling | ਗਲਤੀ ਪ੍ਰਬੰਧਨ | T | normalised (Q19) |
| encryption | ਏਨਕ੍ਰਿਪਸ਼ਨ | L | normalised (Q19) |
| logging | ਲੌਗਿੰਗ | L | corpus precedent (V16) |
| monitoring | ਨਿਗਰਾਨੀ | T | corpus precedent |
| correlation | ਸਹਿ-ਸੰਬੰਧ | T | corpus precedent (V16) |
| investigation (security incident) | ਤਫ਼ਤੀਸ਼ | T | locked (V16 — never ਜਾਂਚ, that's "check") |
| rate limiting | ਦਰ ਸੀਮਾ (no hyphen) | T | normalised (Q19) |
| proxy | ਪ੍ਰੌਕਸੀ | L | normalised (Q19) |
| vault (secrets) | ਵਾਲਟ | L | corpus precedent (V13) |
| service account | ਸੇਵਾ ਖਾਤਾ | T | corpus precedent (V13) |
| hardened | ਸਖ਼ਤ ਕੀਤਾ | T | corpus precedent (V13) |
| build artifacts | ਬਿਲਡ ਆਰਟੀਫ਼ੈਕਟ | L | corpus precedent (V13) |
| supply chain | (no ASVS precedent — new for AISVS, log in OPEN-QUESTIONS.md) | — | new |
| dependency | ਡਿਪੈਂਡੈਂਸੀ | L | corpus precedent (V15, as "dependency confusion") |
| untrusted | ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ | T | normalised (Q15) |
| identifier | ਪਛਾਣਕਰਤਾ | T | corpus precedent (Q17) |
| framework | ਫ੍ਰੇਮਵਰਕ | L | corpus precedent (Q17) |
| architecture | ਆਰਕੀਟੈਕਚਰ | L | flagged inconsistency in ASVS itself (Q17 — README used ਢਾਂਚਾ; chapters use loan). AISVS: prefer the loan, note the ASVS split in OPEN-QUESTIONS.md if it resurfaces |
| compromise (security, verb/noun) | ਸਮਝੌਤਾ | T | flagged, not Sangat-resolved (Q19 — primary dictionary sense is "agreement"; use with care, consider glossing on first use) |
| business logic | ਕਾਰੋਬਾਰੀ ਤਰਕ | T | normalised (Q15) |
| session hijacking | ਸੈਸ਼ਨ ਹਾਈਜੈਕਿੰਗ | L | corpus precedent (Q16) |
| denial of service | ਸੇਵਾ-ਇਨਕਾਰ | T | normalised (Q15) |
| spoofing | ਸਪੂਫ਼ਿੰਗ | L | corpus precedent (Q15) |

## Always-retained (R) terms — never translate or transliterate

OWASP, AISVS, ASVS, CWE, API, URL, TLS, JSON, JWT, JWS, JWK, OAuth, OIDC, SAML,
HTTP, GPU, CPU — plus, carried from ASVS precedent, the pattern of retaining
**named attacks/techniques verbatim** (e.g. Padding Oracle, TOCTOU, Web Cache
Deception, prototype pollution — AISVS equivalents: prompt injection, jailbreak,
model extraction, membership inference, data poisoning stay Latin/English on
first mention, with a Panjabi gloss in parens if a clear native rendering
exists — log the gloss decision in `OPEN-QUESTIONS.md` rather than assuming).

Model/dataset/library/protocol names (e.g. specific model architectures,
MCP, RAG, LoRA) are always retained (R) — never translated or transliterated.

## Gurmat-safety precedent (read before translating any AI-specific term)

The ASVS corpus already hit and fixed one Gurmat collision: "posture" was
first rendered ਮੁਦਰਾ (yoga hand-gesture connotation) and corrected to ਸਥਿਤੀ
(commit `9e1e96b`, Q5). AISVS vocabulary is at *higher* risk of this than
ASVS because AI/ML English borrows spiritually-loaded metaphors routinely —
"hallucination," "alignment," "guardrail," "agent," "memory," "attention,"
"grounding," "emergent behavior." For each of these, check
`5.0/pa-IN/CLAUDE.md` §Gurmat Language Constraints before picking a Panjabi
term, and default to neutral technical vocabulary over a spiritually-loaded
near-synonym every time.
