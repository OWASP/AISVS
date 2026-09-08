# Open Terminology Questions — Reviewer Adjudication

This document collects terminology decisions made during the Panjabi (pa-IN)
translation of OWASP AISVS 1.0 that the translator deferred for community
review. Each entry shows the **current pick**, **alternatives considered**,
and the **reasoning** that led to the current choice. Format mirrors the
sibling ASVS corpus's `OPEN-QUESTIONS.md` so both documents can be reviewed
the same way.

Terms already settled in the ASVS corpus are **not** re-litigated here — see
[`GLOSSARY.md`](GLOSSARY.md). This file is only for AISVS-specific terms with
no ASVS precedent.

**Author commitment:** every entry below is **v0.1 — open for change**. The
current pick is what's on disk; it is not the final answer. Final answer is
the community-adjudicated form.

---

## How to read this file

| Field | Meaning |
|---|---|
| **EN term** | The English source term as it appears in OWASP AISVS 1.0 |
| **Current pick** | The Gurmukhi rendering committed on disk today |
| **Alternatives** | Other candidates considered with their tradeoffs |
| **Type** | T = Translated, L = Loan, R = Retained (acronym/proper noun), H = Hybrid |
| **Reasoning** | Why the current pick — and what could flip it |
| **Reviewer notes** | (Empty — reviewers fill this in) |

---

## Q1 — supply chain

| Field | Value |
|---|---|
| **EN term** | supply chain (as in "AI supply chain attack", C6 title) |
| **Current pick** | ਸਪਲਾਈ ਚੇਨ |
| **Alternatives** | ਸਪਲਾਈ ਲੜੀ (H — loan head + native "chain"); ਪੂਰਤੀ ਲੜੀ (T — fully native, "provision chain"); ਸਪਲਾਈ ਸ਼੍ਰਿੰਖਲਾ (Sanskritic, over-formal) |
| **Type** | L |
| **Reasoning** | No ASVS precedent (`GLOSSARY.md` explicitly marks this as new for AISVS). The ASVS corpus resolves modern Western infrastructure compounds toward the loan rather than a coined native form — ਇਨਵੈਂਟਰੀ (Q19), ਫ੍ਰੇਮਵਰਕ, ਆਰਕੀਟੈਕਚਰ (Q17) — and "supply chain" is already the circulating form in Panjabi business/technology press. ਪੂਰਤੀ ਲੜੀ is the most defensible native option but is not attested in security writing and would read as a neologism to the target practitioner. Glossed once in English on first use in C6. **What could flip it:** if reviewers prefer a native compound corpus-wide, ਸਪਲਾਈ ਲੜੀ is the cheapest change — it keeps the recognisable head and only nativises "chain". |
| **Reviewer notes** | |

---

## Q2 — model weights

| Field | Value |
|---|---|
| **EN term** | model weights (C6.1.2, C6.2.1) |
| **Current pick** | ਮਾਡਲ ਵੇਟਸ |
| **Alternatives** | ਮਾਡਲ ਭਾਰ (T, Sanskritic "weight/mass"); ਮਾਡਲ ਵਜ਼ਨ (T, Perso-Panjabi "weight/mass"); ਮਾਡਲ ਪੈਰਾਮੀਟਰ (paraphrase) |
| **Type** | L |
| **Reasoning** | Both native candidates (ਭਾਰ, ਵਜ਼ਨ) carry only the physical mass sense and would mislead a reader — an ML weight is a learned numeric parameter, not a mass or an importance score. `TRANSLATION-RULES.md` §4 assigns L to modern Western terms with no settled Panjabi word, and the term is a distributable artifact name in practice ("download the weights"). Glossed as ਮਾਡਲ ਵੇਟਸ (model weights) on first use; the bare ਵੇਟਸ is used in the AI BOM listing at C6.2.1 after that gloss. **What could flip it:** if C03 (Model Lifecycle) or C07 needs a possessive/plural-heavy construction where ਵੇਟਸ reads awkwardly, ਮਾਡਲ ਪੈਰਾਮੀਟਰ may be preferable — but that loses the distinction between weights and hyperparameters and should not be adopted without checking C03. |
| **Reviewer notes** | |

---

## Q3 — fine-tuning / fine-tuning adapter

| Field | Value |
|---|---|
| **EN term** | fine-tuning, fine-tuning adapter (C6.1, C6.1.2) |
| **Current pick** | ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ / ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ ਅਡੈਪਟਰ |
| **Alternatives** | ਸੂਖਮ-ਸੁਧਾਈ (T, "fine refinement"); ਬਾਰੀਕ ਟਿਊਨਿੰਗ (H); ਮੁੜ-ਸਿਖਲਾਈ (T, "retraining" — wrong, retraining is a different operation) |
| **Type** | L (adapter: L) |
| **Reasoning** | Fine-tuning is a named, specific training operation distinct from pre-training, retraining, and prompt-tuning; a descriptive native rendering (ਸੂਖਮ-ਸੁਧਾਈ) loses that specificity and collides with generic "refinement". Retained as a loan per §4, glossed in English on first use in C6.1. LoRA and similar adapter names remain R (never translated) per `GLOSSARY.md`. **What could flip it:** a Sangat preference for native training vocabulary across C01/C03 — in which case all training-operation names should move together, not just this one. |
| **Reviewer notes** | |

---

## Q4 — AI BOM / bill of materials

| Field | Value |
|---|---|
| **EN term** | AI BOM, AI-specific bill of materials (C6.2) |
| **Current pick** | AI BOM (retained); the spelled-out phrase rendered ਬਿਲ ਆਫ਼ ਮਟੀਰੀਅਲਜ਼ (bills of materials) |
| **Alternatives** | ਸਮੱਗਰੀ-ਸੂਚੀ (T, "materials list" — collides with ਸਮੱਗਰੀ = "content" as used throughout the ASVS file-handling chapter); ਏਆਈ ਬੀਓਐਮ (transliterated acronym — prohibited by §4 R-rule) |
| **Type** | R (acronym) + L (spelled-out phrase) |
| **Reasoning** | `GLOSSARY.md` lists acronyms as always-retained and never transliterated, so AI BOM stays Latin exactly as in source, matching how SBOM/CycloneDX appear in the reference list. The spelled-out phrase is kept as a loan with an English gloss so a reader connects it to the acronym. ਸਮੱਗਰੀ-ਸੂਚੀ was rejected because ਸਮੱਗਰੀ is already load-bearing for "content" in the sibling corpus and the collision would be silent. **What could flip it:** if a later chapter needs the expansion frequently, a short native gloss may be worth coining once and reused — but the acronym itself must stay R either way. |
| **Reviewer notes** | |

---

## Q5 — dataset

| Field | Value |
|---|---|
| **EN term** | dataset (C6 objective, C6.1.2, C6.2.1) |
| **Current pick** | ਡਾਟਾਸੈੱਟ |
| **Alternatives** | ਡਾਟਾ ਸਮੂਹ (T/H, "data group"); ਅੰਕੜਾ-ਸਮੂਹ (T, Sanskritic "statistics group" — misleading, ਅੰਕੜੇ means statistics/figures, not training data) |
| **Type** | L |
| **Reasoning** | A dataset in AISVS is a named, versioned, downloadable artifact, not a generic collection; the loan preserves that artifact sense and matches the corpus's existing ਡਾਟਾ / ਮੈਟਾਡਾਟਾ loans. ਅੰਕੜਾ-ਸਮੂਹ actively misleads for text/image corpora. Logged here because C01 (Training Data Integrity) will use this term heavily and both files must agree. **What could flip it:** nothing likely; flagged mainly so C01 does not re-derive it differently. |
| **Reviewer notes** | |

---

## Q6 — bias (AI/model bias)

| Field | Value |
|---|---|
| **EN term** | bias (C6 control objective — "embed backdoors, bias, or exploitable code") |
| **Current pick** | ਪੱਖਪਾਤ |
| **Alternatives** | ਝੁਕਾਅ (T, "inclination/leaning" — too weak, loses the unfairness sense); ਪੂਰਵ-ਧਾਰਨਾ (T, "preconception" — attributes a mental state to the model); ਬਾਇਅਸ (L) |
| **Type** | T |
| **Reasoning** | Per the AI/ML-specific risk rule in `CLAUDE.md` and `TRANSLATION-RULES.md` §5.2, an AI-behavior term must not be rendered with vocabulary that implies cognition or carries devotional/metaphysical colour. ਪੱਖਪਾਤ is neutral, standard, dictionary-attested Panjabi for partiality/discrimination and describes the *output property* (systematically unfair outcomes) rather than an inner state — which is exactly the security-relevant meaning here. ਪੂਰਵ-ਧਾਰਨਾ was rejected precisely because it anthropomorphises the model. Glossed in English on first use. **What could flip it:** if C07 (Model Behavior) needs to distinguish statistical bias from fairness bias, a second term may be needed for the statistical sense; ਪੱਖਪਾਤ should stay with the fairness sense. |
| **Reviewer notes** | |

---

## Q7 — behavior / behavioral (of a model)

| Field | Value |
|---|---|
| **EN term** | hidden behavior (C6.1), behavioral acceptance test suite (C6.1.4) |
| **Current pick** | ਵਿਵਹਾਰ / ਵਿਵਹਾਰਕ |
| **Alternatives** | ਆਚਰਣ (T, "conduct" — carries a moral/ethical register unsuitable for a machine); ਕਾਰਜ-ਢੰਗ (T, "mode of operation" — loses the observed-output sense); ਬਿਹੇਵੀਅਰ (L) |
| **Type** | T |
| **Reasoning** | The ASVS sibling corpus already uses ਵਿਵਹਾਰ for system behavior (`0x14-V5-File-Handling.md` 5.1.1: "ਐਪਲੀਕੇਸ਼ਨ ਕਿਵੇਂ ਵਿਵਹਾਰ ਕਰਦੀ ਹੈ"), so this is a consistency carry-over rather than a fresh coinage — but it is logged because AISVS makes model behavior a first-class subject (C07) and the term must be fixed before that chapter. ਵਿਵਹਾਰ is neutral and Gurmat-safe; ਆਚਰਣ was rejected for its moral-conduct register, which would read as ascribing moral agency to a model. **What could flip it:** C07 review may want a distinct term for "behavior" as an evaluated property vs. "behavior" as runtime output. |
| **Reviewer notes** | |

---

## Q8 — artificial intelligence

| Field | Value |
|---|---|
| **EN term** | artificial intelligence (the expanded phrase, in the standard's own name; the acronym **AI** stays R) |
| **Current pick** | ਬਣਾਉਟੀ ਬੁੱਧੀ |
| **Alternatives** | ਨਕਲੀ ਬੁੱਧੀ (T, "fake/imitation intelligence" — carries a pejorative shade); ਮਸਨੂਈ ਬੁੱਧੀ (T, Perso-Arabic, attested in Shahmukhi Panjabi but less familiar to Gurmukhi readers); leave the phrase fully retained as "artificial intelligence" |
| **Type** | T (the acronym AI remains R) |
| **Reasoning** | ਬਣਾਉਟੀ is the Punjabi University Patiala entry for "artificial" and the form used in Gurmukhi-script encyclopedic writing. ਬੁੱਧੀ is neutral technical vocabulary for "intelligence/intellect" — deliberately **not** ਸੁਰਤ or ਮੱਤ, which carry Gurbani-devotional weight and would violate `TRANSLATION-RULES.md` §5. The acronym AI is retained everywhere in running prose; the Panjabi phrase appears only in the expanded standard name on first use, mirroring the ASVS frontispiece pattern (`ਐਪਲੀਕੇਸ਼ਨ ਸੁਰੱਖਿਆ ਤਸਦੀਕ ਮਿਆਰ (Application Security Verification Standard)`). First used in `0x01-Frontispiece.md`. **What could flip it:** a reviewer preference for ਮਸਨੂਈ on register grounds. |
| **Reviewer notes** | |

---

## Q9 — AI lifecycle

| Field | Value |
|---|---|
| **EN term** | AI lifecycle / model lifecycle (frontispiece; C03 title) |
| **Current pick** | AI ਜੀਵਨ-ਚੱਕਰ |
| **Alternatives** | AI ਜੀਵਨ-ਕਾਲ (T, "lifespan" — denotes duration, not the sequence of stages); AI ਲਾਈਫ਼ਸਾਈਕਲ (L) |
| **Type** | H (retained AI + translated ਜੀਵਨ-ਚੱਕਰ) |
| **Reasoning** | ਚੱਕਰ = cycle is ordinary technical Panjabi; in the compound ਜੀਵਨ-ਚੱਕਰ it is **not** the yoga cakra sense that `CLAUDE.md` prohibits (that is the standalone energy-centre meaning). The hybrid keeps the retained acronym intact per §4 while translating the head noun. Logged because the term recurs across the frontispiece, C01, and C03 and must not drift between them. First used in `0x01-Frontispiece.md`. |
| **Reviewer notes** | |

---

## Q10 — safety (as distinct from security)

| Field | Value |
|---|---|
| **EN term** | safety — AI safety, distinct from *security* (ਸੁਰੱਖਿਆ) |
| **Current pick** | ਸਲਾਮਤੀ |
| **Alternatives** | ਸੁਰੱਖਿਅਤਤਾ (awkward derived abstract noun, and still collides with ਸੁਰੱਖਿਆ); ਬਚਾਅ (T, "protection/defence" — narrower); reuse ਸੁਰੱਖਿਆ for both (collapses a distinction the standard depends on) |
| **Type** | T |
| **Reasoning** | AISVS uses "security" and "safety" as separate concepts inside one sentence ("resilience, privacy, and safety"), so they cannot share a single Panjabi word. ਸਲਾਮਤੀ is well-established everyday Panjabi for safety/well-being, Perso-Arabic in origin and therefore free of yoga/Hindu-devotional connotation per §5. ਸੁਰੱਖਿਆ stays reserved corpus-wide for "security", consistent with the ASVS sibling corpus. Glossed on first use as `ਸਲਾਮਤੀ (safety)` in `0x01-Frontispiece.md`. **What could flip it:** C07/C11 may need "safety" as an attribute of model output, where a reviewer might prefer a periphrasis. |
| **Reviewer notes** | |

---

## Q11 — threat landscape

| Field | Value |
|---|---|
| **EN term** | threat landscape ("the AI threat landscape") |
| **Current pick** | ਖ਼ਤਰਾ ਪਰਿਦ੍ਰਿਸ਼ |
| **Alternatives** | ਖ਼ਤਰਿਆਂ ਦਾ ਮਾਹੌਲ (T, "environment of threats" — vaguer); ਖ਼ਤਰਾ ਦ੍ਰਿਸ਼ (T, "threat scene" — too literal); ਖ਼ਤਰਾ ਲੈਂਡਸਕੇਪ (H) |
| **Type** | T |
| **Reasoning** | ਖ਼ਤਰਾ for "threat" is already normalised in `GLOSSARY.md` (Q13) and kept distinct from ਜੋਖਮ "risk", so only the head noun was open. ਪਰਿਦ੍ਰਿਸ਼ is neutral Sanskritic-register vocabulary for an overall scene/panorama with no devotional loading, and matches the formal academic register required by §4. Glossed in English on first use in `0x01-Frontispiece.md`. |
| **Reviewer notes** | |

---

## Q12 — resilience

| Field | Value |
|---|---|
| **EN term** | resilience (of an AI solution) |
| **Current pick** | ਲਚਕੀਲਾਪਣ (oblique form: ਲਚਕੀਲੇਪਣ) |
| **Alternatives** | ਲਚਕਤਾ (T, "flexibility" — a different property); ਸਹਿਣਸ਼ੀਲਤਾ (T, "tolerance/endurance" — closer to fault tolerance); ਰੈਜ਼ੀਲੀਐਂਸ (L) |
| **Type** | T |
| **Reasoning** | No ASVS precedent in `GLOSSARY.md`. ਲਚਕੀਲਾਪਣ carries the "recovers its shape after stress" sense that resilience means in a security context, whereas ਲਚਕਤਾ reads as mere flexibility or configurability. ਸਹਿਣਸ਼ੀਲਤਾ is deliberately kept free for "tolerance" (e.g. fault tolerance) so the two do not collide in C04/C11. Glossed in English on first use in `0x01-Frontispiece.md`. |
| **Reviewer notes** | |

---

## Q13 — privacy

| Field | Value |
|---|---|
| **EN term** | privacy |
| **Current pick** | ਨਿੱਜਤਾ |
| **Alternatives** | ਗੋਪਨੀਯਤਾ (T, Sanskritic/Hindi register, and semantically closer to *confidentiality*); ਪ੍ਰਾਈਵੇਸੀ (L); ਨਿੱਜੀ ਜਾਣਕਾਰੀ ਦੀ ਸੁਰੱਖਿਆ (periphrastic) |
| **Type** | T |
| **Reasoning** | ਨਿੱਜਤਾ is native Panjabi register (from ਨਿੱਜ, "one's own") and is the form used in Gurmukhi-script legal and technical writing. ਗੋਪਨੀਯਤਾ is deliberately reserved so that *confidentiality* — a distinct concept in both AISVS and ASVS — can take it later without collision. Glossed in English on first use in `0x01-Frontispiece.md`; C08 (Memory, Embeddings, Vector DB) will reuse it heavily. |
| **Reviewer notes** | |

---

## Q14 — governance framework

| Field | Value |
|---|---|
| **EN term** | governance framework (e.g. NIST AI RMF, ISO/IEC 42001) |
| **Current pick** | ਸ਼ਾਸਨ ਫ੍ਰੇਮਵਰਕ |
| **Alternatives** | ਪ੍ਰਸ਼ਾਸਨ ਫ੍ਰੇਮਵਰਕ (T/L, "administration" — implies day-to-day operations); ਪ੍ਰਬੰਧਨ ਫ੍ਰੇਮਵਰਕ (T/L, "management" — collides with ਪ੍ਰਬੰਧਨ already used for "handling/management"); ਗਵਰਨੈਂਸ ਫ੍ਰੇਮਵਰਕ (L) |
| **Type** | H (translated head + loan ਫ੍ਰੇਮਵਰਕ) |
| **Reasoning** | ਫ੍ਰੇਮਵਰਕ is already corpus precedent in `GLOSSARY.md` (Q17), so only "governance" was open. ਸ਼ਾਸਨ carries the oversight/direction sense that governance has in NIST AI RMF and ISO/IEC 42001, and keeps ਪ੍ਰਬੰਧਨ free for "management/handling" (already load-bearing in ਗਲਤੀ ਪ੍ਰਬੰਧਨ, error handling). The standard names themselves stay R. Glossed in English on first use in `0x01-Frontispiece.md`. |
| **Reviewer notes** | |

---

## Q15 — retirement (lifecycle stage)

| Field | Value |
|---|---|
| **EN term** | retirement — the final stage of the AI/model lifecycle |
| **Current pick** | ਸੇਵਾ-ਮੁਕਤੀ |
| **Alternatives** | ਬੰਦ ਕਰਨਾ (T, "shutting down" — an action, not a lifecycle stage); ਰਿਟਾਇਰਮੈਂਟ (L — reads as human retirement); ਨਿਪਟਾਰਾ (T, "disposal" — overlaps with data disposal/deletion) |
| **Type** | T |
| **Reasoning** | ਸੇਵਾ-ਮੁਕਤੀ ("release from service") names a lifecycle *stage* rather than a single act, which is what the frontispiece and C03 require. ਨਿਪਟਾਰਾ is kept free for data disposal so the two stages stay distinguishable in C01/C03. Glossed in English on first use in `0x01-Frontispiece.md`. |
| **Reviewer notes** | |

---

## Q16 — deployment

| Field | Value |
|---|---|
| **EN term** | deployment / deploy (of a model or AI system) |
| **Current pick** | ਤੈਨਾਤੀ |
| **Alternatives** | ਡਿਪਲੌਇਮੈਂਟ (L); ਲਾਗੂ ਕਰਨਾ (T, "to apply/enforce" — collides with the very common "enforce" sense in requirement text); ਵਰਤੋਂ ਵਿੱਚ ਲਿਆਉਣਾ (periphrastic) |
| **Type** | T |
| **Reasoning** | No ASVS precedent in `GLOSSARY.md`. ਤੈਨਾਤੀ is established Panjabi for putting something into active service and is short enough for repeated use in requirement prose. Critically it avoids ਲਾਗੂ ਕਰਨਾ, which the sibling corpus already uses heavily for "enforce/apply" — reusing that for deployment would silently blur a distinction that matters in C03 and C04. Glossed in English on first use in `0x01-Frontispiece.md`. |
| **Reviewer notes** | |

---

## Q17 — AI agent

| Field | Value |
|---|---|
| **EN term** | AI agent / agent (C5.1, C5.2.5) |
| **Current pick** | AI ਏਜੰਟ / ਏਜੰਟ |
| **Alternatives** | ਪ੍ਰਤੀਨਿਧ (T, "representative" — implies a delegated human); ਦੂਤ (T, "messenger/emissary" — devotional-mythological connotation, disqualified by §5); ਕਾਰਕ (T, grammatical "agent") |
| **Type** | L (with retained AI head) |
| **Reasoning** | `CLAUDE.md` flags "agent" as one of the highest-risk AI metaphor terms, so a spiritually-loaded near-synonym is excluded outright — ਦੂਤ fails on those grounds. ਪ੍ਰਤੀਨਿਧ loses the software sense and ਕਾਰਕ is a grammar term. The transliterated loan ਏਜੰਟ is neutral, already current in Panjabi business/technical prose, and composes for "agentic" (ਏਜੰਟ-ਆਧਾਰਿਤ — long ā, per Q71) in C09. **What could flip it:** C09 (Orchestration & Agentic Action) is the deciding chapter — if it coins a native form, it should be applied corpus-wide, not per chapter. |
| **Reviewer notes** | |

---

## Q18 — inference

| Field | Value |
|---|---|
| **EN term** | inference; also post-inference, inference cache, inference chain (C5.2, C5.2.4, C5.3) |
| **Current pick** | ਇਨਫ਼ਰੈਂਸ (ਇਨਫ਼ਰੈਂਸ-ਉਪਰੰਤ = post-inference) |
| **Alternatives** | ਅਨੁਮਾਨ (T, "estimate/inference"); ਨਿਗਮਨ (T, logical deduction); ਸਿੱਟਾ (T, "conclusion") |
| **Type** | L |
| **Reasoning** | ਅਨੁਮਾਨ is unusable here: the sibling ASVS corpus already uses ਅਨੁਮਾਨਿਤ for "expected/anticipated" (`0x14-V5-File-Handling.md` 5.1.1, 5.2.2), so ਅਨੁਮਾਨ would read as "expected value", not "running the model". ਨਿਗਮਨ is logic-textbook register and never denotes model execution. The loan keeps the runtime sense unambiguous and composes cleanly for the compounds. **What could flip it:** nothing likely; logged because C07 and C11 use the term heavily and must not re-derive it. |
| **Reviewer notes** | |

---

## Q19 — embedding / embedding index

| Field | Value |
|---|---|
| **EN term** | embedding, embedding index, embedding lookup (C5.2, C5.2.1, C5.2.2, C5.3.1) |
| **Current pick** | `embedding` retained in Latin script; compounds `embedding ਇੰਡੈਕਸ`, `embedding ਖੋਜ` |
| **Alternatives** | ਏਮਬੈਡਿੰਗ (L, transliterated); ਸ਼ਾਮਲੀਕਰਨ (T, "act of embedding" — wrong sense); ਵੈਕਟਰ ਪ੍ਰਤੀਨਿਧਤਾ (T, "vector representation") |
| **Type** | H |
| **Reasoning** | `TRANSLATION-RULES.md` §4 already gives `embedding ਸਟੋਰ` as a canonical hybrid, which fixes the retained Latin head; this entry only records the extension to *index* and *lookup*. ਸ਼ਾਮਲੀਕਰਨ names the act of embedding one thing inside another and loses the vector sense. ਵੈਕਟਰ ਪ੍ਰਤੀਨਿਧਤਾ is accurate but too long for repeated table use and collides with "vector collections" in the same requirement (5.2.1). **What could flip it:** C08 (Memory, Embeddings & Vector Database) should settle whether the transliteration ਏਮਬੈਡਿੰਗ replaces the retained head corpus-wide. |
| **Reviewer notes** | |

---

## Q20 — retrieval pipeline (RAG)

| Field | Value |
|---|---|
| **EN term** | retrieval pipeline, retrieval (as in RAG retrieval) (C5.2, C5.2.2, C5.2.3) |
| **Current pick** | ਪ੍ਰਾਪਤੀ ਪਾਈਪਲਾਈਨ / ਪ੍ਰਾਪਤੀ — RAG stays retained |
| **Alternatives** | ਮੁੜ-ਪ੍ਰਾਪਤੀ (T, "re-retrieval" — adds a "re-" the English lacks); ਖੋਜ ਪਾਈਪਲਾਈਨ (T, "search pipeline"); ਰੀਟ੍ਰੀਵਲ ਪਾਈਪਲਾਈਨ (L) |
| **Type** | T + L (RAG = R) |
| **Reasoning** | ਪ੍ਰਾਪਤੀ ("obtaining") is the closest neutral technical noun and is cognate with the verb ਪ੍ਰਾਪਤ ਕੀਤਾ ਜਾਂਦਾ ਹੈ used in 5.2.3, so noun and verb stay consistent inside one requirement. ਖੋਜ must stay reserved for "lookup/search" — it renders *embedding lookups* in the very same sentence, and reusing it for retrieval would collapse two distinct pipeline stages. RAG itself is a retained acronym per `GLOSSARY.md`. |
| **Reviewer notes** | |

---

## Q21 — prompt cache

| Field | Value |
|---|---|
| **EN term** | prompt cache (C5.2.7); and `prompt` as a head noun generally |
| **Current pick** | `prompt ਕੈਸ਼` — `prompt` retained in Latin script |
| **Alternatives** | ਪ੍ਰੌਂਪਟ ਕੈਸ਼ (L, transliterated); ਸੰਕੇਤ ਕੈਸ਼ (T, "hint/signal"); ਹਿਦਾਇਤ ਕੈਸ਼ (T, "instruction") |
| **Type** | H |
| **Reasoning** | `TRANSLATION-RULES.md` §4 lists `prompt ਇੰਜੈਕਸ਼ਨ` as a canonical hybrid, fixing the retained Latin `prompt` head corpus-wide; this entry only records the extension to *cache*. ਸੰਕੇਤ and ਹਿਦਾਇਤ both lose the specific LLM-input meaning and would make "prompt injection" and "prompt cache" look unrelated to a reader. **What could flip it:** C02 / C07 own the final call on whether `prompt` ever transliterates. |
| **Reviewer notes** | |

---

## Q22 — tenant / multi-tenant

| Field | Value |
|---|---|
| **EN term** | tenant, multi-tenant, cross-tenant, per-tenant (C5.3) |
| **Current pick** | ਟੈਨੈਂਟ / ਬਹੁ-ਟੈਨੈਂਟ / ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ / ਪ੍ਰਤੀ-ਟੈਨੈਂਟ |
| **Alternatives** | ਕਿਰਾਏਦਾਰ (T, "renter/lessee"); ਵਸਨੀਕ (T, "resident"); ਗਾਹਕ (T, "customer") |
| **Type** | L |
| **Reasoning** | ਕਿਰਾਏਦਾਰ is the literal dictionary equivalent but denotes a person renting property; applied to shared model-serving infrastructure it reads as a housing term and obscures the isolation boundary the whole section is about. ਗਾਹਕ is a different entity — one customer may hold many tenants. The loan is standard in Panjabi cloud/SaaS prose and keeps the four compound forms regular. Isolation itself is rendered ਅਲੱਗ-ਥਲੱਗਤਾ (neutral, no ASVS precedent needed). |
| **Reviewer notes** | |

---

## Q23 — step-up authentication

| Field | Value |
|---|---|
| **EN term** | step-up authentication (C5.1.1) |
| **Current pick** | ਸਟੈੱਪ-ਅੱਪ ਪ੍ਰਮਾਣੀਕਰਨ |
| **Alternatives** | ਵਾਧੂ ਪ੍ਰਮਾਣੀਕਰਨ (T, "additional authentication"); ਉੱਚ-ਪੱਧਰੀ ਪ੍ਰਮਾਣੀਕਰਨ (T, "higher-level"); ਮੁੜ-ਪ੍ਰਮਾਣੀਕਰਨ (T, "re-authentication" — a different control) |
| **Type** | H |
| **Reasoning** | ਪ੍ਰਮਾਣੀਕਰਨ for *authentication* is locked in `GLOSSARY.md`; only the modifier was open. "Step-up" is a named industry pattern (NIST SP 800-63-3; OIDC `acr_values`) distinct both from plain re-authentication and from simply adding a factor, so a descriptive Panjabi modifier would flatten a distinction the requirement depends on. Retained modifier + locked Panjabi head keeps the term searchable against the references the chapter cites; English glossed on first use. |
| **Reviewer notes** | |

---

## Q24 — policy decision point

| Field | Value |
|---|---|
| **EN term** | policy decision point (C5.2.5) |
| **Current pick** | ਨੀਤੀ ਫ਼ੈਸਲਾ ਬਿੰਦੂ (policy decision point) |
| **Alternatives** | ਪਾਲਿਸੀ ਡਿਸੀਜ਼ਨ ਪੁਆਇੰਟ (L, full transliteration); retain `policy decision point` verbatim (R) |
| **Type** | T (with English gloss) |
| **Reasoning** | Unlike model-internals vocabulary, this is a plain architectural compound whose parts all have settled Panjabi equivalents (ਨੀਤੀ = policy, ਫ਼ੈਸਲਾ = decision, ਬਿੰਦੂ = point), so translating loses nothing and reads naturally in formal register. Glossed in English on first use because the NIST SP 800-207 reference cited by this chapter uses the English term and readers must be able to match it. **What could flip it:** if a later chapter needs the PDP/PEP pair, the policy *enforcement* point should be settled at the same time so the two stay parallel. |
| **Reviewer notes** | |

---

## Q25 — Zero Standing Privilege (ZSP)

| Field | Value |
|---|---|
| **EN term** | Zero Standing Privilege (ZSP) (C5.2.6) |
| **Current pick** | Zero Standing Privilege (ZSP) — retained verbatim |
| **Alternatives** | ਜ਼ੀਰੋ ਸਥਾਈ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ (H); ਕੋਈ ਸਥਾਈ ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਨਹੀਂ (T, descriptive) |
| **Type** | R |
| **Reasoning** | Follows the `GLOSSARY.md` "always-retained" rule for named security models and techniques — the same treatment Zero Trust Architecture gets in the NIST SP 800-207 reference this chapter cites. The acronym ZSP is load-bearing in practitioner usage and does not survive translation. Note that "privileged access" in the surrounding prose *is* translated (ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ ਪ੍ਰਾਪਤ ਪਹੁੰਚ); only the named model stays English. **What could flip it:** reviewers may want a one-time descriptive Panjabi gloss in parentheses if the bare English reads as opaque. |
| **Reviewer notes** | |

---

## Q26 — prompt injection

| Field | Value |
|---|---|
| **EN term** | prompt injection (C2 title, C2.1, C2.1.3, C2.2.4) |
| **Current pick** | prompt ਇੰਜੈਕਸ਼ਨ |
| **Alternatives** | ਪ੍ਰੌਂਪਟ ਇੰਜੈਕਸ਼ਨ (L, both halves transliterated); ਹਦਾਇਤ ਇੰਜੈਕਸ਼ਨ (T head, "instruction injection") |
| **Type** | H |
| **Reasoning** | `TRANSLATION-RULES.md` §4 already gives prompt ਇੰਜੈਕਸ਼ਨ as the canonical hybrid example, and `GLOSSARY.md` directs that named attacks stay Latin on first mention. ਇੰਜੈਕਸ਼ਨ matches the sibling corpus's SQL ਇੰਜੈਕਸ਼ਨ, so the attack family reads consistently across both standards; keeping "prompt" Latin also preserves searchability against OWASP LLM01:2025. This decision also governs the bare noun "prompt", which C02 keeps in Latin throughout (ਹਰ prompt, ਅਜਿਹੇ prompt). **What could flip it:** a reviewer preference for a fully transliterated ਪ੍ਰੌਂਪਟ in running prose — it would then have to change everywhere, including C07 and C09. |
| **Reviewer notes** | |

---

## Q27 — input normalization

| Field | Value |
|---|---|
| **EN term** | input normalization (C2.1.1) |
| **Current pick** | ਸਧਾਰਨੀਕਰਨ |
| **Alternatives** | ਨਾਰਮਲਾਈਜ਼ੇਸ਼ਨ (L); ਮਿਆਰੀਕਰਨ (T, "standardization" — imprecise) |
| **Type** | T |
| **Reasoning** | ਸਧਾਰਨੀਕਰਨ is the attested Punjabi University rendering for "normalization" and is fully neutral. Kept deliberately distinct from ਕੈਨੋਨੀਕਲਾਈਜ਼ੇਸ਼ਨ (next entry): C2.1.1 and C2.1.2 name normalization and canonicalization as separate operations, so collapsing both into one Panjabi word would silently merge two requirements. Glossed in English on first use. **What could flip it:** little; logged so C08's pre-processing prose does not re-derive it differently. |
| **Reviewer notes** | |

---

## Q28 — canonicalization

| Field | Value |
|---|---|
| **EN term** | canonicalization (C2.1.2, as an approved mitigation) |
| **Current pick** | ਕੈਨੋਨੀਕਲਾਈਜ਼ੇਸ਼ਨ |
| **Alternatives** | ਪ੍ਰਮਾਣਿਕ ਰੂਪੀਕਰਨ (T); ਮਿਆਰੀ ਰੂਪ ਵਿੱਚ ਬਦਲਣਾ (descriptive phrase) |
| **Type** | L |
| **Reasoning** | No settled Panjabi noun exists, and a descriptive phrase reads badly inside a requirement clause that lists four mitigations in series. The loan also keeps the term visibly distinct from ਸਧਾਰਨੀਕਰਨ. ਪ੍ਰਮਾਣਿਕ was rejected because the ਪ੍ਰਮਾਣ- root is already load-bearing in `GLOSSARY.md` for authentication (ਪ੍ਰਮਾਣੀਕਰਨ) and validation (ਪ੍ਰਮਾਣਿਤ ਕਰਨਾ); a third sense would blur all three. Glossed in English on first use. **What could flip it:** a Sangat push toward native forms across the input-handling vocabulary — normalization and canonicalization must then move together or not at all. |
| **Reviewer notes** | |

---

## Q29 — tokenization

| Field | Value |
|---|---|
| **EN term** | tokenization (C2.1.1 — splitting input into model tokens) |
| **Current pick** | ਟੋਕਨਾਈਜ਼ੇਸ਼ਨ |
| **Alternatives** | ਟੋਕਨੀਕਰਨ (H, loan stem + native suffix); ਟੋਕਨ ਵੰਡ (T, "token splitting") |
| **Type** | L |
| **Reasoning** | ਟੋਕਨ is already the locked loan for "token" (`TRANSLATION-RULES.md` §4), so extending the same loan to the process keeps the pair recognisable to a reader coming from the ASVS corpus. Note this is the ML tokenizer sense, not the session/security-token sense ASVS uses — logged so a reviewer can decide whether the two senses need visually distinct renderings before C08 lands. **What could flip it:** if both senses appear in one chapter, a disambiguating modifier may become necessary. |
| **Reviewer notes** | |

---

## Q30 — context window / model context

| Field | Value |
|---|---|
| **EN term** | context window (C2.1.4); model context (C2.1.7, C2.2.1) |
| **Current pick** | ਸੰਦਰਭ ਵਿੰਡੋ / ਮਾਡਲ ਸੰਦਰਭ |
| **Alternatives** | ਸੰਦਰਭ ਖਿੜਕੀ (T, native "window"); ਕਾਨਟੈਕਸਟ ਵਿੰਡੋ (L) |
| **Type** | H |
| **Reasoning** | ਸੰਦਰਭ for "context" is locked in `GLOSSARY.md`, so only the second half was open. ਵਿੰਡੋ is the settled computing loan in Panjabi technical prose; ਖਿੜਕੀ reads architectural rather than technical and would be the only native-window usage in either corpus. ਮਾਡਲ ਸੰਦਰਭ reuses the same locked head noun so both terms visibly belong to one family — this matters because C02 moves between them across adjacent requirements (2.1.4 vs 2.1.7). Glossed in English on first use. **What could flip it:** little; logged for C08/C09 consistency. |
| **Reviewer notes** | |

---

## Q31 — instruction hierarchy

| Field | Value |
|---|---|
| **EN term** | instruction hierarchy (C2.1, C2.1.6) |
| **Current pick** | ਹਦਾਇਤ ਲੜੀ-ਕ੍ਰਮ |
| **Alternatives** | ਹਦਾਇਤ ਦਰਜਾਬੰਦੀ (T, "ranking"); ਨਿਰਦੇਸ਼ ਸ਼੍ਰੇਣੀ-ਕ੍ਰਮ (T, Sanskritic) |
| **Type** | T |
| **Reasoning** | ਹਦਾਇਤ is everyday formal Panjabi for a directive and avoids ਨਿਰਦੇਸ਼, which drifts toward "guidance/direction" and would weaken a hard override requirement. ਲੜੀ-ਕ੍ਰਮ renders hierarchy as an ordered chain, which is precisely the C2.1.6 semantics (system and developer messages override user instructions), without the rank-of-persons connotation ਦਰਜਾਬੰਦੀ can carry. Glossed in English on first use. **What could flip it:** C09 (Orchestration and Agentic Action) needs the same concept for tool/agent instruction precedence — it should reuse this term rather than re-coin one. |
| **Reviewer notes** | |

---

## Q32 — many-shot jailbreaking

| Field | Value |
|---|---|
| **EN term** | many-shot jailbreaking (C2.1.8) |
| **Current pick** | many-shot jailbreaking (retained, Latin) |
| **Alternatives** | ਮੈਨੀ-ਸ਼ਾਟ ਜੇਲਬ੍ਰੇਕਿੰਗ (L); ਬਹੁ-ਉਦਾਹਰਨ ਪਾਬੰਦੀ-ਤੋੜ (T, descriptive) |
| **Type** | R |
| **Reasoning** | `GLOSSARY.md` sets the ASVS precedent of retaining named attacks and techniques verbatim (Padding Oracle, TOCTOU) and explicitly names jailbreak among the AISVS equivalents. A literal native rendering (ਕੈਦ ਤੋੜਨਾ, "breaking out of jail") would add carceral imagery the source does not carry and would not be recognised by a practitioner reading MITRE ATLAS. Left unglossed because no clean native rendering exists for a gloss to point at. **What could flip it:** reviewers may want a one-time explanatory parenthetical on first use without changing the retained form. |
| **Reviewer notes** | |

---

## Q33 — classifier / content classification

| Field | Value |
|---|---|
| **EN term** | classifier (C2.1, C2.1.3, C2.2.1); content classification (C2.2.2) |
| **Current pick** | ਵਰਗੀਕਾਰ / ਵਰਗੀਕਰਨ |
| **Alternatives** | ਕਲਾਸੀਫਾਇਰ (L); ਸ਼੍ਰੇਣੀਕਾਰ (T, Sanskritic) |
| **Type** | T |
| **Reasoning** | ਵਰਗੀਕਰਨ (classification) is attested Punjabi University lexicography and fully neutral; the agent noun ਵਰਗੀਕਾਰ derives regularly from it, so the component and the process it performs share one root — which matters because C2.2.1 and C2.2.2 use the two forms in adjacent requirements. Preferred over the loan because classification is an established concept, not a coined product name, which is the T-vs-L test in `TRANSLATION-RULES.md` §4. Glossed in English on first use. **What could flip it:** if a later chapter uses "classifier" for a shipped vendor component rather than a technique, the loan may read better there. |
| **Reviewer notes** | |

---

## Q34 — representation smuggling

| Field | Value |
|---|---|
| **EN term** | encoding and representation smuggling (C2.1.2) |
| **Current pick** | ਪ੍ਰਤੀਨਿਧਤਾ ਤਸਕਰੀ (encoding stays ਏਨਕੋਡਿੰਗ) |
| **Alternatives** | ਰੂਪ-ਲੁਕਾਈ (T, "form concealment"); retaining `representation smuggling` verbatim |
| **Type** | T |
| **Reasoning** | Unlike jailbreak or prompt injection, this is a descriptive phrase in the source rather than a branded technique name, so the retention precedent does not apply. ਤਸਕਰੀ (smuggling) carries exactly the right sense of moving something illicitly past a control, which ਲੁਕਾਈ (concealment) does not — the threat is transit past a filter, not mere hiding. ਏਨਕੋਡਿੰਗ follows the loan family already normalised in `GLOSSARY.md` (ਏਨਕ੍ਰਿਪਸ਼ਨ). Glossed in English on first use. **What could flip it:** if upstream AISVS later promotes this to a named attack class, it should move to R alongside many-shot jailbreaking. |
| **Reviewer notes** | |

---

## Q35 — adversarial perturbation

| Field | Value |
|---|---|
| **EN term** | adversarial perturbations (C2.2.3) |
| **Current pick** | ਵਿਰੋਧੀ ਵਿਗਾੜ |
| **Alternatives** | ਵਿਰੋਧੀ ਗੜਬੜੀ (T, "disorder/malfunction"); ਦੁਸ਼ਮਣ-ਪ੍ਰੇਰਿਤ ਵਿਗਾੜ (T, "enemy-induced"); ਐਡਵਰਸੇਰੀਅਲ ਪਰਟਰਬੇਸ਼ਨ (L) |
| **Type** | T |
| **Reasoning** | ਵਿਰੋਧੀ is the neutral technical sense of "adversarial" (opposing, attacking) without the personal-enmity charge of ਦੁਸ਼ਮਣ, which would over-dramatise a signal-processing concept. ਵਿਗਾੜ denotes a deliberate distortion of a signal, matching C2.2.3 better than ਗੜਬੜੀ (accidental disorder or malfunction) — the distinction is security-relevant, because a perturbation is crafted, not incidental. Glossed in English on first use. **What could flip it:** this sets the head term for C11 (Adversarial Robustness); if C11 needs a different register for its chapter title, both must change together. **Overload flagged 2026-08-26 (see Q40):** ਵਿਗਾੜ is doing triple duty on disk — *perturbation* here (C02 2.2.3), *corruption* at Q40 (C01, Preface), and the participle ਵਿਗੜੇ for *malformed* in C07's control objective. The two entries picked the same word independently without cross-referencing each other. No single sentence is ambiguous (the modifier ਵਿਰੋਧੀ disambiguates the C02 sense), so no change was made, but reviewers should decide whether *malformed* deserves a separate word. |
| **Reviewer notes** | |

---

## Q36 — steganographic payload

| Field | Value |
|---|---|
| **EN term** | steganographic payloads (C2.2.3, C2.2.4) |
| **Current pick** | ਸਟੈਗਨੋਗ੍ਰਾਫ਼ਿਕ ਪੇਲੋਡ |
| **Alternatives** | ਗੁਪਤ-ਲਿਖਤ ਪੇਲੋਡ (T, "secret-writing"); retaining `steganographic payload` verbatim |
| **Type** | L |
| **Reasoning** | Steganography has no settled Panjabi noun, and ਗੁਪਤ-ਲਿਖਤ collides conceptually with cryptography (ਏਨਕ੍ਰਿਪਸ਼ਨ, `GLOSSARY.md`) — the entire point of the C2.2.3 control is that hidden-channel content is a different threat from encrypted content, so a rendering that blurs them would weaken the requirement. The loan keeps the distinction visible. ਪੇਲੋਡ follows the corpus pattern of loaning payload-class computing nouns. **What could flip it:** reviewers may prefer full Latin retention to match the treatment of named techniques. |
| **Reviewer notes** | |

---

## Q37 — training data / training (a model)

| Field | Value |
|---|---|
| **EN term** | training data, training (C01 title, C1.1, C1.3) |
| **Current pick** | ਸਿਖਲਾਈ ਡਾਟਾ / ਸਿਖਲਾਈ |
| **Alternatives** | ਟ੍ਰੇਨਿੰਗ ਡਾਟਾ (full loan); ਅਭਿਆਸ ਡਾਟਾ (**rejected** — ਅਭਿਆਸ reads as spiritual practice/repetition in Gurmat register, e.g. naam abhiās) |
| **Type** | T (head) + L (ਡਾਟਾ, corpus-standard loan) |
| **Reasoning** | ਸਿਖਲਾਈ is the ordinary, neutral Panjabi noun for training/instruction and carries no devotional colour — the neutral-technical default required by `CLAUDE.md` §AI/ML-specific risk. ਅਭਿਆਸ is exactly the class of collision that rule warns about and was rejected outright. The full loan was rejected because a settled native word exists and this term appears in the chapter title. **What could flip it:** reviewers finding ਸਿਖਲਾਈ too vocational-training-flavoured for an ML context; it must also stay consistent with ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ (Q3) and with "retraining" when C03 needs it. **Residue flagged for reviewer 2026-08-26 — not changed:** ਸਿਖਲਾਈ is applied consistently for *training* everywhere it occurs (C01, C03, C05, Preface; 0x03, C02, C04, C06 have no "training" in source, so their absence is correct). However ਅਭਿਆਸ — rejected outright by this entry on §5 Gurmat grounds (naam abhiās) — is still on disk three times rendering English *practice(s)* in a professional-practice sense (`0x02-Preface.md`:14, `0x03-Using-AISVS.md`:128 and :146). That is a different English word, applied self-consistently, so it is **not** a rendering inconsistency and was left untouched; but it sits against this entry's own stated rationale and is a translator-policy call, not a mechanical one. Reviewer decision needed: keep ਅਭਿਆਸ for *practice*, or move to ਅਮਲ / ਵਿਹਾਰ. |
| **Reviewer notes** | |

---

## Q38 — traceability

| Field | Value |
|---|---|
| **EN term** | traceability (C01 title, C01 control objective) |
| **Current pick** | ਟਰੇਸਯੋਗਤਾ |
| **Alternatives** | ਪਤਾ-ਲਗਾਉਣਯੋਗਤਾ (transparent but clumsy); ਸੁਰਾਗ਼ਯੋਗਤਾ (ਸੁਰਾਗ਼ = clue, forensic flavour); ਖੋਜਯੋਗਤਾ (**collides** with "discoverability"/"searchability") |
| **Type** | H — English head `trace` + Panjabi suffix `-ਯੋਗਤਾ` |
| **Reasoning** | Chapter-title term with no ASVS precedent. ਖੋਜਯੋਗਤਾ was rejected for silent collision with the search/discovery vocabulary AISVS uses elsewhere. The hybrid keeps the audit-trail sense recognisable to practitioners reading against the English standard, and `-ਯੋਗਤਾ` is the same productive suffix already in the corpus (ਭਰੋਸੇਯੋਗਤਾ, ਤਸਦੀਕਯੋਗ). **What could flip it:** a reviewer preference for zero English roots in chapter titles, in which case ਪਤਾ-ਲਗਾਉਣਯੋਗਤਾ is the honest fallback. |
| **Reviewer notes** | |

---

## Q39 — data poisoning / poisoning detection / clean-label poisoning

| Field | Value |
|---|---|
| **EN term** | data poisoning, poisoning detection, clean-label poisoning (C1.1, C1.3, 1.3.1, 1.3.5) |
| **Current pick** | `data poisoning` retained, glossed once as **(ਡਾਟਾ ਜ਼ਹਿਰੀਕਰਨ)**; thereafter bare `poisoning` in hybrids — `poisoning ਪਛਾਣ`, `clean-label poisoning ਹਮਲੇ` |
| **Alternatives** | ਡਾਟਾ ਜ਼ਹਿਰੀਕਰਨ used throughout (T); ਪੌਇਜ਼ਨਿੰਗ (L) |
| **Type** | R (attack name) + T gloss on first mention → H thereafter |
| **Reasoning** | `GLOSSARY.md` §Always-retained sets the precedent that named attacks/techniques stay Latin/English on first mention with a Panjabi gloss in parens, and names `data poisoning` explicitly among them. ਜ਼ਹਿਰੀਕਰਨ is an accurate calque (ਜ਼ਹਿਰ = poison) and Gurmat-safe, but using it alone would break the reader's link to MITRE ATLAS AML.T0020, cited in this chapter's own reference list. `clean-label` stays untranslated for the same reason — it names a technique, it is not a description. **What could flip it:** if C11 (Adversarial Robustness) establishes a full native attack-name vocabulary, this should move with it rather than diverge. |
| **Reviewer notes** | |

---

## Q40 — corruption (of data)

| Field | Value |
|---|---|
| **EN term** | corruption, unintentional corruption (C1.1, 1.1.4, C1.3, 1.3.1) |
| **Current pick** | ਵਿਗਾੜ |
| **Alternatives** | ਭ੍ਰਿਸ਼ਟਾਚਾਰ (**rejected — false friend**, means bribery/moral corruption); ਖਰਾਬੀ (= malfunction/defect); ਕਰੱਪਸ਼ਨ (loan, same false-friend problem) |
| **Type** | T |
| **Reasoning** | A genuine trap worth logging: ਭ੍ਰਿਸ਼ਟਾਚਾਰ is *the* standard Panjabi word for corruption in the bribery sense and would read as an accusation of human misconduct rather than a data-integrity event — a silent meaning inversion inside a security requirement. ਵਿਗਾੜ (spoiling, distortion, going out of order) carries the mechanical sense AISVS means. Logged because the term recurs in C03, C06, and C08 and the corpus must settle on one word. **Overload flagged 2026-08-26 (see Q35):** Q35 independently picked the same ਵਿਗਾੜ for *adversarial perturbation*, and C07 uses ਵਿਗੜੇ for *malformed* — three source concepts on one root, arrived at without either entry citing the other. Left as-is (context disambiguates) but recorded so a reviewer sees the collision rather than discovering it. |
| **Reviewer notes** | |

---

## Q41 — labeling / annotation

| Field | Value |
|---|---|
| **EN term** | labeling, label; annotation, annotate (C1.2 heading, 1.2.1–1.2.3) |
| **Current pick** | ਲੇਬਲਿੰਗ / ਲੇਬਲ; ਐਨੋਟੇਸ਼ਨ |
| **Alternatives** | ਟਿੱਪਣੀਕਰਨ for annotation (= commenting/remark-making); ਨਿਸ਼ਾਨਦੇਹੀ for labeling (= marking/demarcation) |
| **Type** | L (both) |
| **Reasoning** | AISVS C1.2 uses *labeling* and *annotation* as two distinct terms of art for one industry workflow, and the requirements depend on keeping them distinguishable (a labeling platform vs. approving annotations). ਟਿੱਪਣੀਕਰਨ carries a "written commentary" sense that misdescribes an ML annotation pipeline; ਨਿਸ਼ਾਨਦੇਹੀ suggests boundary-marking. The loans preserve the distinction and match the ਡਾਟਾਸੈੱਟ (Q5) / ਪਾਈਪਲਾਈਨ register used in the same section. **What could flip it:** a reviewer decision that the two English terms are synonymous in practice and may collapse into one Panjabi word. |
| **Reviewer notes** | |

---

## Q42 — confidence threshold / low-confidence

| Field | Value |
|---|---|
| **EN term** | confidence thresholds, low-confidence labels (1.3.2) |
| **Current pick** | ਭਰੋਸਾ ਥ੍ਰੈਸ਼ਹੋਲਡ; ਘੱਟ-ਭਰੋਸੇ ਵਾਲੇ |
| **Alternatives** | ਵਿਸ਼ਵਾਸ ਸੀਮਾ; ਆਤਮ-ਵਿਸ਼ਵਾਸ (**rejected** — that is human self-confidence and anthropomorphises the model); ਕਾਨਫ਼ੀਡੈਂਸ ਸਕੋਰ (full loan) |
| **Type** | H — T head (ਭਰੋਸਾ) + L (ਥ੍ਰੈਸ਼ਹੋਲਡ) |
| **Reasoning** | ਭਰੋਸਾ is plainer and less devotional than ਵਿਸ਼ਵਾਸ, which leans toward faith/belief — the neutral-technical default. ਸੀਮਾ was avoided for *threshold* because `GLOSSARY.md` already binds ਸੀਮਾ to "limit" in **ਦਰ ਸੀਮਾ** (rate limiting), and a threshold that triggers review is not a limit that blocks. **What could flip it:** whether the corpus adopts ਥ੍ਰੈਸ਼ਹੋਲਡ as the standing loan for *threshold* everywhere — worth deciding once, corpus-wide. See also Q44, where ਭਰੋਸਾ is doing double duty. |
| **Reviewer notes** | |

---

## Q43 — watermarking (datasets)

| Field | Value |
|---|---|
| **EN term** | watermarked (1.1.5) |
| **Current pick** | ਵਾਟਰਮਾਰਕ ਕੀਤਾ ਜਾਂਦਾ ਹੈ |
| **Alternatives** | ਜਲ-ਚਿੰਨ੍ਹ (literal calque); ਗੁਪਤ ਪਛਾਣ-ਚਿੰਨ੍ਹ (descriptive) |
| **Type** | L |
| **Reasoning** | ਜਲ-ਚਿੰਨ੍ਹ literally renders the paper-making metaphor and conveys nothing about the ML technique — an embedded statistical signal used for provenance attribution. The loan is what practitioners use and preserves the link to the English control. Paired here with ਸਰੋਤ-ਨਿਰਧਾਰਨ (Q45). |
| **Reviewer notes** | |

---

## Q44 — assurance

| Field | Value |
|---|---|
| **EN term** | quality and security assurance (C1.3 heading and prose) |
| **Current pick** | ਭਰੋਸਾ |
| **Alternatives** | ਯਕੀਨ-ਦਹਾਨੀ (= the act of reassuring someone, a speech act); ਅਸ਼ਿਓਰੈਂਸ (L) |
| **Type** | T |
| **Reasoning** | *Assurance* in a verification standard means grounded confidence produced by controls — ਭਰੋਸਾ. ਯਕੀਨ-ਦਹਾਨੀ describes one party reassuring another, which is the wrong act entirely. **Flagged rather than settled:** ਭਰੋਸਾ is now doing double duty — *assurance* here and *confidence* in Q42. Reviewers may want to split them (keep ਭਰੋਸਾ for assurance, take a loan for ML confidence scores) before the overload propagates corpus-wide. |
| **Reviewer notes** | |

---

## Q45 — attribution (of dataset use)

| Field | Value |
|---|---|
| **EN term** | attributed / attribution (1.1.5) |
| **Current pick** | ਸਰੋਤ-ਨਿਰਧਾਰਨ, glossed **ਸਰੋਤ-ਨਿਰਧਾਰਨ (attribution)** |
| **Alternatives** | ਸਿਹਰਾ (**rejected** — = credit/honour, congratulatory register); ਜ਼ਿੰਮੇਵਾਰੀ-ਨਿਰਧਾਰਨ (= assigning blame/responsibility) |
| **Type** | T |
| **Reasoning** | In 1.1.5 *attributed* means "traced back to its source dataset," not "credited to an author." ਸਿਹਰਾ carries a congratulatory sense that would invert the meaning of a control about detecting unauthorized use. ਸਰੋਤ-ਨਿਰਧਾਰਨ (source-determination) states the mechanism plainly and aligns with the chapter's ਟਰੇਸਯੋਗਤਾ theme (Q38). **What could flip it:** threat-intel "attribution" (naming an attacker) in C11/C12 likely needs a different rendering — do not assume this pick transfers. |
| **Reviewer notes** | |

---

## Q46 — feature (ML input variable) / pipeline

| Field | Value |
|---|---|
| **EN term** | features (1.1.1); pipeline, training pipeline (C1.2, C1.3, 1.3.1) |
| **Current pick** | ਫ਼ੀਚਰ — glossed **ਫ਼ੀਚਰ (features)** on first use; ਪਾਈਪਲਾਈਨ |
| **Alternatives** | ਵਿਸ਼ੇਸ਼ਤਾ / ਗੁਣ for feature (**collision** — see reasoning); ਪ੍ਰਕਿਰਿਆ-ਲੜੀ for pipeline (invented compound, unattested) |
| **Type** | L (both) |
| **Reasoning** | *feature* needed the gloss specifically because 1.1.1 lists "features, attributes, and fields" in one breath: ਗੁਣ is used there for *attributes*, so rendering *features* as ਵਿਸ਼ੇਸ਼ਤਾ would collapse two deliberately distinct terms into near-synonyms and weaken a data-minimisation requirement. Both terms are modern engineering vocabulary with no settled Panjabi word, which `TRANSLATION-RULES.md` §4 routes to L. **What could flip it:** if C08 (Embeddings & Vector Database) coins a native term for *feature* in the feature-vector sense, C01 should follow rather than diverge. |
| **Reviewer notes** | |

---

## Q47 — sandbox / sandboxing

| Field | Value |
|---|---|
| **EN term** | sandbox, sandboxing (C4.1 title and intro, C4.1.1) |
| **Current pick** | ਸੈਂਡਬਾਕਸ / ਸੈਂਡਬਾਕਸਿੰਗ |
| **Alternatives** | ਸੁਰੱਖਿਅਤ ਘੇਰਾ (T, "safe enclosure" — descriptive but unattested, and collides with "secure enclave" in the same chapter); ਵੱਖਰਾ ਖ਼ਾਨਾ (T, "separate compartment" — too vague for a named isolation primitive) |
| **Type** | L |
| **Reasoning** | A sandbox is a named technical primitive with a specific operational meaning (kernel-enforced process confinement), not a general metaphor; a descriptive rendering leaves the reader guessing at scope. The loan follows the sibling corpus's treatment of comparable infrastructure primitives — ਪ੍ਰੌਕਸੀ, ਵਾਲਟ, ਟੋਕਨ (`GLOSSARY.md`). Glossed in English on first use in C4.1. **What could flip it:** an attested native rendering in a Panjabi computer-science lexicon. |
| **Reviewer notes** | |

---

## Q48 — attestation / attest

| Field | Value |
|---|---|
| **EN term** | attestation, attested (C4.1.3, C4.2.1, C4.2.3) |
| **Current pick** | ਅਟੈਸਟੇਸ਼ਨ / ਅਟੈਸਟ ਕੀਤਾ |
| **Alternatives** | ਪ੍ਰਮਾਣਨ — **rejected**, collides with ਪ੍ਰਮਾਣੀਕਰਨ (authentication, locked); ਤਸਦੀਕ — **rejected**, locked to "verify"; ਪ੍ਰਮਾਣਿਤ — **rejected**, locked to "validate"; ਸਰਟੀਫ਼ਿਕੇਸ਼ਨ — **rejected**, locked to "certification" (ASVS Q18); ਗਵਾਹੀ (T, "testimony") — legal/witness register, not a cryptographic-proof sense |
| **Type** | L |
| **Reasoning** | This is a verb-precision problem (`TRANSLATION-RULES.md` §4), not a vocabulary gap. Four adjacent English verbs — verify / validate / authenticate / certify — are *already* locked to four distinct Panjabi words in `GLOSSARY.md`. "Attestation" is a fifth distinct concept (a signed hardware claim about runtime state), and every remaining native candidate is one of the four locked words, so a loan is the only rendering that preserves a distinction the standard depends on. C4.2 exercises the collision directly: 4.2.1 says *attested*, 4.2.3 says *validated … using attestation mechanisms*, 4.2.5 says *authenticated* — collapsing any two would corrupt the requirements. **What could flip it:** a reviewer-coined native term demonstrably free of all four locked senses. |
| **Reviewer notes** | |

---

## Q49 — memory (hardware / computational)

| Field | Value |
|---|---|
| **EN term** | memory, memory encryption, memory sanitization, memory isolation (C4.2.2, C4.2.4, C4.3.3) |
| **Current pick** | ਮੈਮੋਰੀ |
| **Alternatives** | ਯਾਦਦਾਸ਼ਤ — **rejected**, means human recollection and anthropomorphises hardware; ਸਿਮਰਨ — **absolutely rejected**, devotional remembrance; using it would be a Gurmat-safety violation of exactly the class `CLAUDE.md` §AI/ML-specific risk warns about |
| **Type** | L |
| **Reasoning** | "Memory" sits on the `CLAUDE.md` watch-list of AI terms carrying metaphorical baggage. Throughout C04 the referent is unambiguously *hardware* memory (GPU VRAM, process address space), so the neutral loan is both technically correct and the safest choice under §5.2. Logged explicitly as a hand-off: when C08 (Memory, Embeddings & Vector Database) reaches the *agent-memory* sense, the reviewer should see that C04 deliberately claimed the loan for the hardware sense — C08 must decide separately for the other sense and must not reach for a cognitive or devotional near-synonym. |
| **Reviewer notes** | |

---

## Q50 — trusted execution environment (TEE) / secure enclave / confidential computing

| Field | Value |
|---|---|
| **EN term** | trusted execution environment (TEE), secure enclave, confidential computing (C4.1 intro, C4.1.4, C4.2.2, C4.3.4, C4.3.5) |
| **Current pick** | ਭਰੋਸੇਯੋਗ ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਵਾਤਾਵਰਣ (acronym **TEE** retained) / ਸੁਰੱਖਿਅਤ ਐਨਕਲੇਵ / ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ |
| **Alternatives** | Full retention of all three phrases in English — considered, but the modifiers (trusted / secure / confidential) are semantically load-bearing and the Panjabi reader benefits from them; ਭਰੋਸੇਯੋਗ ਅਮਲ ਵਾਤਾਵਰਣ for TEE — ਅਮਲ carries a "doing/practice" sense rather than "a program runs" |
| **Type** | H (acronym R) |
| **Reasoning** | One consistent hybrid pattern across all three: translate the adjective, loan the technical head noun, retain the acronym per §4 (R). This keeps ਭਰੋਸੇਯੋਗ (trusted) / ਸੁਰੱਖਿਅਤ (secure) / ਗੁਪਤ (confidential) visibly distinct, which the source relies on — C4.3.5 contrasts a *trusted runtime* with a *secure enclave* inside one sentence. "Enclave" stays a loan because it names a specific vendor primitive (SGX / TrustZone class), not a generic region. Glossed in English on first use. **Found by the full-corpus audit 2026-08-27:** C05 5.3.2 (`0x10-C05`:80) rendered *confidential computing* as the loan ਕਾਨਫ਼ੀਡੈਂਸ਼ੀਅਲ ਕੰਪਿਊਟਿੰਗ — the only one in the corpus, and the worst possible site, because `0x91-Appendix-B`:124 indexes that same requirement C5.3.2 with ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ, so one control read two ways across two files. Normalised to ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ, matching C04 4.1 intro and `0x90-Appendix-A`:82. ਕਾਨਫ਼ੀਡੈਂਸ਼ੀਅਲ is now lint-blocked (`tools/lint-terminology.py`), because losing ਗੁਪਤ here would also break the three-way ਭਰੋਸੇਯੋਗ / ਸੁਰੱਖਿਅਤ / ਗੁਪਤ contrast this entry exists to protect. |
| **Reviewer notes** | |

---

## Q51 — accelerator / workload / edge

| Field | Value |
|---|---|
| **EN term** | AI accelerator, workload, edge (edge computing, edge AI devices) (C4.1, C4.2, C4.3) |
| **Current pick** | ਐਕਸਲੇਰੇਟਰ / ਵਰਕਲੋਡ / ਐਜ |
| **Alternatives** | accelerator → ਤੇਜ਼ਕਾਰ ("speeder-up") — a coinage, unattested in technical Panjabi; workload → ਕਾਰਜ-ਭਾਰ — readable, but reads as human effort/load rather than a schedulable compute unit; edge → ਕਿਨਾਰਾ ("edge/margin") — **rejected**, purely spatial and loses the deployment-topology meaning entirely |
| **Type** | L |
| **Reasoning** | All three are deployment-topology terms of art whose English form is what a Panjabi-reading practitioner meets in vendor documentation and job specifications; native renderings would be locally readable but not translatable back. ਕਿਨਾਰਾ is the clearest failure — it would make the whole of C4.3 unintelligible. Glossed in English on first use. **What could flip it:** ਕਾਰਜ-ਭਾਰ for "workload" is the most defensible of the three if reviewers want one nativised. |
| **Reviewer notes** | |

---

## Q52 — federated learning

| Field | Value |
|---|---|
| **EN term** | federated learning (C4.3 intro) |
| **Current pick** | ਫ਼ੈਡਰੇਟਿਡ ਲਰਨਿੰਗ |
| **Alternatives** | ਸੰਘੀ ਸਿਖਲਾਈ — ਸੰਘੀ is a political-federation adjective (federal government) and misleads here; ਵੰਡਵੀਂ ਸਿਖਲਾਈ ("distributed learning") — **rejected**, that names a different technique, and the same source sentence already contains "distributed" |
| **Type** | L |
| **Reasoning** | A named ML technique. `GLOSSARY.md` §Always-retained sets the precedent that named techniques (prompt injection, model extraction, membership inference, data poisoning) keep their English form with an optional Panjabi gloss; federated learning belongs to that class, consistent with Q3 (fine-tuning). **Spelling normalised 2026-08-26:** C04 had ਫੈਡਰੇਟਿਡ and C05 5.1.2 had ਫ਼ੈਡਰੇਟਿਡ for the same English word. Normalised to **ਫ਼ੈਡਰੇਟਿਡ** per the new Q86 (English /f/ takes the nukta ਫ਼) — see Q86 for the corpus-wide rule. The source sentence lists "edge computing, federated learning, and multi-site architectures" together, so the rendering must keep *federated* and *distributed* visibly distinct — hence ਵੰਡੀਆਂ ਹੋਈਆਂ for distributed and the loan here. |
| **Reviewer notes** | |

---

## Q53 — contamination (cross-tenant)

| Field | Value |
|---|---|
| **EN term** | contamination, in "cross-tenant contamination" (C4 Control Objective) |
| **Current pick** | ਦੂਸ਼ਣ — full phrase rendered ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ ਦੂਸ਼ਣ |
| **Alternatives** | ਗੰਦਗੀ (T, "filth/dirt") — wrong register, moral shading; ਪ੍ਰਦੂਸ਼ਣ (T) — environmental-pollution sense; ਮਿਲਾਵਟ (T, "adulteration") — implies deliberate dilution of a substance |
| **Type** | T |
| **Reasoning** | Only the head noun was open: *tenant* / *cross-tenant* is already settled at Q22 (ਟੈਨੈਂਟ / ਟੈਨੈਂਟਾਂ ਵਿਚਕਾਰ) and this entry adopts that form rather than re-deriving a prefix. ਦੂਸ਼ਣ carries the neutral "one thing tainting another" sense used in scientific Panjabi, which is what cross-tenant leakage means here — data from one tenant tainting another's context. English glossed in parens on first use. |
| **Reviewer notes** | |

---

## Q54 — model theft / model artifact

| Field | Value |
|---|---|
| **EN term** | model theft (C4 Control Objective); model artifact (C4.1.2) |
| **Current pick** | ਮਾਡਲ ਚੋਰੀ / ਮਾਡਲ ਆਰਟੀਫ਼ੈਕਟ |
| **Alternatives** | model theft → retain the English technique name in the "model extraction" style per `GLOSSARY.md` — but the source says *theft* (the harm/outcome), not *extraction* (the technique), and ਚੋਰੀ renders that exactly; model artifact → ਮਾਡਲ ਵਸਤੂ — **rejected**, ਵਸਤੂ was already deprecated in the sibling corpus for "inventory" (ASVS Q19) |
| **Type** | H |
| **Reasoning** | ਚੋਰੀ is plain, unambiguous Panjabi for theft and the source uses the everyday sense, so no loan is warranted. ਆਰਟੀਫ਼ੈਕਟ follows the settled ASVS rendering ਬਿਲਡ ਆਰਟੀਫ਼ੈਕਟ (`GLOSSARY.md`, V13) — same head noun, different modifier — so reusing it costs nothing and keeps the two corpora aligned. **Boundary to preserve:** ਚੋਰੀ names the harm; the C11 technique name "model extraction" stays English. C06 and C11 should not blur the two. |
| **Reviewer notes** | |

---

## Q55 — tokenizer

| Field | Value |
|---|---|
| **EN term** | tokenizer (C3.1.2) |
| **Current pick** | ਟੋਕਨਾਈਜ਼ਰ |
| **Alternatives** | ਟੋਕਨਕਾਰ (H, coined agent-noun); ਟੋਕਨ-ਵਿਭਾਜਕ (T, "token splitter" — descriptive, but invents a term no practitioner uses and misdescribes subword tokenizers) |
| **Type** | L |
| **Reasoning** | `TRANSLATION-RULES.md` §4 already fixes token → ਟੋਕਨ (L), and a tokenizer is a shipped, signable model artifact listed alongside weights and adapters in C3.1.2 — a reviewer must be able to match it to the file in their own registry. Straight transliteration preserves that identity. **What could flip it:** nothing likely; logged so C02 (Input Validation) does not re-derive it differently. |
| **Reviewer notes** | |

---

## Q56 — alignment

| Field | Value |
|---|---|
| **EN term** | alignment (C3.2.2, "the same safety and alignment test suite") |
| **Current pick** | ਅਲਾਈਨਮੈਂਟ — glossed `ਅਲਾਈਨਮੈਂਟ (alignment)` on first use |
| **Alternatives** | ਇਕਸੁਰਤਾ (T, "harmony/attunement" — the ਸੁਰ root is musical/devotional); ਸੁਮੇਲ (T, "harmonious union" — same objection); ਤਾਲਮੇਲ (T, "coordination" — ਤਾਲ is a rhythmic/devotional term, and the sense is coordination, not value alignment); ਅਨੁਕੂਲਨ (already load-bearing for "optimization", Q59) |
| **Type** | L |
| **Reasoning** | `CLAUDE.md` §AI/ML-specific risk names "alignment" explicitly as a high-risk term, and every native candidate here is a harmony/attunement word with devotional colour — the same class of failure as the ਮੁਦਰਾ collision the ASVS corpus had to correct (`GLOSSARY.md`, ASVS Q5). The neutral loan carries none of that freight, and it keeps ਅਨੁਕੂਲਨ free for "optimization", which C3.5.2 needs in the same chapter. **What could flip it:** C07 (Model Behavior) and C11 will use this term heavily; a native form must be chosen for all three chapters at once and must avoid the ਸੁਰ/ਤਾਲ roots. |
| **Reviewer notes** | |

---

## Q57 — quantization

| Field | Value |
|---|---|
| **EN term** | post-training quantization (C3.2.2) |
| **Current pick** | ਕੁਆਂਟਾਈਜ਼ੇਸ਼ਨ — glossed with the full English phrase on first use; "post-training" rendered T as ਸਿਖਲਾਈ-ਉਪਰੰਤ |
| **Alternatives** | ਮਾਤਰਾਕਰਨ (T, literal, from ਮਾਤਰਾ); ਸੰਖਿਆਕਰਨ (T, "numeralization" — wrong sense) |
| **Type** | L |
| **Reasoning** | The literal calque ਮਾਤਰਾਕਰਨ collides head-on with ਮਾਤਰਾ as the Gurmukhi vowel-sign term named in `TRANSLATION-RULES.md` §1.4 — a silent collision inside this corpus's own vocabulary. The loan is unambiguous for a named compression technique. The ਸਿਖਲਾਈ-ਉਪਰੰਤ pattern matches ਇਨਫ਼ਰੈਂਸ-ਉਪਰੰਤ (Q18). |
| **Reviewer notes** | |

---

## Q58 — rollout / rollback

| Field | Value |
|---|---|
| **EN term** | rollout mechanisms, automated rollback triggers, rollback capabilities (C3.3, C3.3.1, C3.3.2) |
| **Current pick** | ਰੋਲਆਊਟ / ਰੋਲਬੈਕ |
| **Alternatives** | ਵਾਪਸ ਮੋੜਨਾ (T, verb phrase — cannot carry the noun sense in "rollback capabilities"); ਪਿਛਾਂਹ-ਮੋੜ (T, coinage); ਬਹਾਲੀ (T, "restoration" — collides with ਬਹਾਲ ਕਰਨਾ, used for "restore" inside C3.3.2 itself) |
| **Type** | L |
| **Reasoning** | Both name configured deployment-pipeline mechanisms, not described actions — "automated rollback triggers" is a feature a reviewer inspects, so the noun form must survive translation. Consistent with the ASVS pattern of loaning deployment-infrastructure vocabulary (ਪ੍ਰੌਕਸੀ, ਬਿਲਡ ਆਰਟੀਫ਼ੈਕਟ, ਕਨੈਕਸ਼ਨ ਪੂਲ), and pairs with ਤੈਨਾਤੀ for deployment (Q16). |
| **Reviewer notes** | |

---

## Q59 — reward hacking / reward model over-optimization

| Field | Value |
|---|---|
| **EN term** | reward hacking, reward model over-optimization (C3.5.2) |
| **Current pick** | `reward hacking (ਇਨਾਮ ਦੀ ਦੁਰਵਰਤੋਂ)` and `reward model (ਇਨਾਮ ਮਾਡਲ) ਦਾ ਹੱਦੋਂ ਵੱਧ ਅਨੁਕੂਲਨ (over-optimization)` |
| **Alternatives** | full translation ਇਨਾਮ ਹੈਕਿੰਗ (loses the retrievable English identity of a named AI-safety failure mode); full retention with no gloss (leaves a Gurmukhi-only reader without the concept); ਫਲ for "reward" (rejected — ਫਲ carries a karmic fruit-of-action connotation, a §5 Gurmat violation) |
| **Type** | H (retained English head + Panjabi gloss) |
| **Reasoning** | `GLOSSARY.md` §Always-retained sets the pattern for named attacks and techniques: Latin on first mention, Panjabi gloss in parentheses where a clear native rendering exists, and the gloss decision logged here rather than assumed. ਇਨਾਮ is the neutral, dictionary-attested word for reward/prize. ਦੁਰਵਰਤੋਂ ("misuse/exploitation") conveys that the reward *signal* is being gamed, not that a system was broken into — ਹੈਕਿੰਗ alone would wrongly imply intrusion. **What could flip it:** C11 (Adversarial Robustness) may settle a house style for named-failure-mode glosses; this entry should then follow it. |
| **Reviewer notes** | |

---

## Q60 — checkpoint

| Field | Value |
|---|---|
| **EN term** | fine-tuning checkpoints (C3.5.4) |
| **Current pick** | ਚੈੱਕਪੁਆਇੰਟ |
| **Alternatives** | ਜਾਂਚ-ਬਿੰਦੂ (T, literal "check point" — misleading, since an ML checkpoint is a saved artifact and not an inspection gate; ਜਾਂਚ is also reserved for "check" per `GLOSSARY.md`); ਸੰਭਾਲ-ਬਿੰਦੂ (T, "save point" — ਸੰਭਾਲ is reserved, it collides with "handling") |
| **Type** | L |
| **Reasoning** | The ML sense is a serialized snapshot of training state that C3.5.4 requires to be registered as a distinct artifact; neither literal calque conveys that, and both collide with terms already reserved in `GLOSSARY.md`. The loan keeps the artifact sense intact and parallels ਬਿਲਡ ਆਰਟੀਫ਼ੈਕਟ. |
| **Reviewer notes** | |

---

## Q61 — model registry

| Field | Value |
|---|---|
| **EN term** | model registry (C3.1.1) |
| **Current pick** | ਮਾਡਲ ਰਜਿਸਟਰੀ |
| **Alternatives** | ਮਾਡਲ ਰਜਿਸਟਰ (L, "register" — a ledger, not the system of record); ਮਾਡਲ ਸੂਚੀ (T, "list" — too weak for a governed system that also gates deployment admission); ਮਾਡਲ ਭੰਡਾਰ (T, "repository" — a different component) |
| **Type** | L |
| **Reasoning** | A named piece of MLOps infrastructure, parallel to the loan already settled for what it holds: inventory → ਇਨਵੈਂਟਰੀ (`GLOSSARY.md`, ASVS Q19 normalisation). Translating the container while loaning its contents would read inconsistently inside the single sentence of C3.1.1. |
| **Reviewer notes** | |

---

## Q62 — memory (AI system / agent memory)

| Field | Value |
|---|---|
| **EN term** | memory (C8 title and control objective — semi-persistent and persistent "memory"); agent memory (8.2.3); memory writes (C8.2); memory reset (8.3.2) |
| **Current pick** | ਮੈਮੋਰੀ — glossed **"ਮੈਮੋਰੀ" (memory)** on first use in the C8 control objective |
| **Alternatives** | ਯਾਦਦਾਸ਼ਤ (T, human recollection — anthropomorphises the system, and its root ਯਾਦ is load-bearing devotional vocabulary in Gurbani for remembrance of the Divine); ਸਿਮ੍ਰਤੀ / ਸਿਮਰਤੀ (Sanskritic *smṛti* — **categorically rejected**: Smriti names a class of Hindu religious literature, a direct violation of `CLAUDE.md` §Gurmat Language Constraints); ਭੰਡਾਰ (T, "store" — loses the memory sense and collides with ਭੰਡਾਰਨ = "storage" in the ASVS sibling corpus) |
| **Type** | L |
| **Reasoning** | The single highest-risk term in this chapter under `TRANSLATION-RULES.md` §5.2, which names "memory" explicitly as a term whose English metaphorical baggage must not be carried into a spiritually-loaded Panjabi near-synonym. Two independent reasons fix the loan. **First, Gurmat safety:** the two native candidates are both disqualified — ਸਿਮ੍ਰਤੀ outright (Smriti = Hindu scriptural category), and ਯਾਦਦਾਸ਼ਤ because ਯਾਦ carries devotional remembrance colour and because it ascribes recollection, a mental faculty, to a vector index. **Second, corpus consistency:** C04 already uses ਮੈਮੋਰੀ for hardware/GPU memory (4.2.2, 4.2.4, 4.3.3), so the loan is established on disk and lets one word serve one concept — a machine store of state — across both chapters. AISVS itself puts "memory" in scare quotes in the C8 objective, signalling that it is a metaphor rather than cognition; the loan preserves that neutrality, where any native cognition word would silently assert it. **What could flip it:** C09 (Orchestration & Agentic Action) uses agent memory heavily; if reviewers prefer a native rendering it must be adopted in C04, C08 and C09 together, never in one chapter alone. |
| **Reviewer notes** | |

---

## Q63 — quarantine (of vectors and content)

| Field | Value |
|---|---|
| **EN term** | quarantined (8.2.2, 8.2.4, 8.3.3) |
| **Current pick** | ਕੁਆਰੰਟੀਨ — glossed **ਕੁਆਰੰਟੀਨ (quarantine)** on first use in 8.2.2 |
| **Alternatives** | ਇਕਾਂਤਵਾਸ (T, "solitary dwelling" — ascetic/devotional register, wrong for a data-handling control); ਅਲੱਗ-ਥਲੱਗ ਕਰਨਾ (T, "isolate" — **collision**: already load-bearing for infrastructure isolation in C04 4.2.2 / 4.2.4 / 4.3.3 and for policy-engine isolation in C05 5.2.5); ਵੱਖਰਾ ਰੱਖਣਾ (T, "kept separate" — readable, but loses the retained-yet-blocked sense that 8.3.3 depends on) |
| **Type** | L |
| **Reasoning** | Quarantine in C8 is a precise third state, not a synonym for isolation or deletion: 8.3.3 requires quarantined content to be **retained** while being **excluded from all retrieval results**. A rendering that reads as "isolated" would collide with the infrastructure sense already fixed in C04/C05, and one that reads as "removed" would silently soften the retention obligation — forbidden by `TRANSLATION-RULES.md` §6.3. ਕੁਆਰੰਟੀਨ has been in wide circulation in Panjabi since 2020 and is the only candidate carrying "held aside but still present". ਇਕਾਂਤਵਾਸ was rejected on the §5 register rule before its accuracy was even considered. **What could flip it:** C11 (Adversarial Robustness) is likely to need the same state; whatever it picks and this chapter picks must match. |
| **Reviewer notes** | |

---

## Q64 — clustering / vectorization

| Field | Value |
|---|---|
| **EN term** | normal clustering patterns (8.2.2); vectorization (C8.2 objective, 8.2.4) |
| **Current pick** | ਕਲੱਸਟਰਿੰਗ / ਵੈਕਟਰਾਈਜ਼ੇਸ਼ਨ — each glossed in English on first use |
| **Alternatives** | For *clustering*: ਸਮੂਹਬੰਦੀ (T, "grouping" — generic, loses the reference to the named unsupervised-learning technique); ਗੁੱਛਾਬੰਦੀ (T, "bunching" — unattested in technical writing). For *vectorization*: ਵੈਕਟਰੀਕਰਨ (T-style derivation on the loan stem); ਵੈਕਟਰ ਵਿੱਚ ਬਦਲਣਾ (descriptive paraphrase — too long for repeated table use) |
| **Type** | L (both) |
| **Reasoning** | Both are named machine-learning operations, which `TRANSLATION-RULES.md` §4 routes to L and which this corpus already treats that way — ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ (Q3), ਟੋਕਨਾਈਜ਼ੇਸ਼ਨ (C02 2.1.1). In 8.2.2 the security claim is specifically that an anomaly detector compares a new vector against the *distribution produced by clustering*; a generic ਸਮੂਹਬੰਦੀ would let a reader take it as any ad-hoc grouping and weaken the requirement. ਵੈਕਟਰਾਈਜ਼ੇਸ਼ਨ is built on ਵੈਕਟਰ, which `TRANSLATION-RULES.md` §4 already lists as a locked L example, so it is a derivation rather than a fresh coinage. This chapter also **keeps the retained Latin head `embedding`** rather than transliterating to ਏਮਬੈਡਿੰਗ, resolving the deferral left open at the end of Q19 — C02 (2.1.1) and C05 (5.2.1, 5.2.2, 5.2.3, 5.2.7, 5.3.1) are all already on disk with the retained head, and changing it here alone would split the corpus. **What could flip it:** a corpus-wide move to transliterate `embedding`, which would have to be applied to C02, C05 and C08 in one change. |
| **Reviewer notes** | |

---

## Q65 — hallucination

| Field | Value |
|---|---|
| **EN term** | hallucination (C7.2 heading and section intro) |
| **Current pick** | `hallucination` retained in Latin script, glossed on first use as ਮਨਘੜਤ ਸਮੱਗਰੀ ("fabricated content") |
| **Alternatives** | ਭਰਮ (T); ਭੁਲੇਖਾ (T); ਵਹਿਮ (T); ਕਲਪਨਾ (T, "imagination") |
| **Type** | R (+ T gloss) |
| **Reasoning** | ਭਰਮ, ਭੁਲੇਖਾ and ਵਹਿਮ all carry Gurbani-specific spiritual weight (delusion under māyā, doubt of the mind) — precisely the spiritually-loaded near-synonym class that `TRANSLATION-RULES.md` §5.2 and `CLAUDE.md` §AI/ML-specific risk forbid, and the same failure shape as the ASVS ਮੁਦਰਾ/ਸਥਿਤੀ collision (Q5 there). ਕਲਪਨਾ is Gurmat-neutral but names a creative faculty rather than a defect, which understates a security failure mode. "Hallucination" is a *named AI failure mode*, so it takes the `GLOSSARY.md` retained-technique pattern (prompt injection, jailbreak, data poisoning): keep the English name, add a neutral descriptive gloss. **What could flip it:** a Sangat preference for a fully native rendering — in which case ਮਨਘੜਤ ਸਮੱਗਰੀ is the candidate to promote from gloss to term. C11 (Adversarial Robustness) must not re-derive this. |
| **Reviewer notes** | |

---

## Q66 — unsafe (as an attribute of content or output)

| Field | Value |
|---|---|
| **EN term** | unsafe content, unsafe responses (C7 control objective, C7.3 intro) |
| **Current pick** | ਗ਼ੈਰ-ਸਲਾਮਤ, glossed `(unsafe)` on first use |
| **Alternatives** | ਅਸੁਰੱਖਿਅਤ (T — derives from ਸੁਰੱਖਿਆ = *security*, which the "safety" entry reserves); ਖ਼ਤਰਨਾਕ (T, "dangerous" — the ASVS corpus uses it for *malicious* files, `0x14-V5-File-Handling.md` 5.1.1); ਅਣ-ਸਲਾਮਤ (same coinage, rarer negation prefix) |
| **Type** | T |
| **Reasoning** | This answers the hook left open by the **safety** entry in this file ("C07/C11 may need safety as an attribute of model output"). That entry fixes safety = ਸਲਾਮਤੀ and reserves ਸੁਰੱਖਿਆ for security corpus-wide; the adjective must therefore derive from ਸਲਾਮਤ, not ਸੁਰੱਖਿਅਤ, or C7's own chapter title (ਸਲਾਮਤੀ ਯਕੀਨਦਹਾਨੀ) would contradict its requirement text two paragraphs later. The ਗ਼ੈਰ- negation prefix follows the corpus's ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ (untrusted, `GLOSSARY.md` Q15) pattern. **What could flip it:** reviewers may prefer a periphrasis (ਸਲਾਮਤੀ ਲਈ ਖ਼ਤਰਾ ਪੈਦਾ ਕਰਨ ਵਾਲੀ ਸਮੱਗਰੀ) if ਗ਼ੈਰ-ਸਲਾਮਤ reads as a neologism. **Cross-file audit 2026-08-26:** C03 (chapter intro) and C08 8.2 both rendered source-English *unsafe* as ਅਸੁਰੱਖਿਅਤ — the exact form this entry rejects, and a silent re-collapse of the ਸਲਾਮਤੀ/ਸੁਰੱਖਿਆ split. Both normalised to ਗ਼ੈਰ-ਸਲਾਮਤ with an English gloss on chapter-first use. ਅਸੁਰੱਖਿਅਤ now appears nowhere in the corpus. |
| **Reviewer notes** | |

---

## Q67 — assurance in C7 (conformance note on the ਭਰੋਸਾ overload)

| Field | Value |
|---|---|
| **EN term** | Safety Assurance (C7 chapter title) — alongside *confidence* (7.2.1, 7.2.2) in the same chapter |
| **Current pick** | ਭਰੋਸਾ — ਸਲਾਮਤੀ ਭਰੋਸਾ, conforming to the earlier **assurance** entry in this file rather than competing with it |
| **Alternatives** | ਯਕੀਨਦਹਾਨੀ (T — the split candidate if reviewers separate the two senses); ਗਾਰੰਟੀ (**rejected** — assurance is evidence, not a guarantee, and §6.3 forbids strengthening a requirement beyond the source); ਅਸ਼ਿਓਰੈਂਸ (L) |
| **Type** | T |
| **Reasoning** | **C7 is the forcing case the earlier assurance entry anticipated.** That entry picked ਭਰੋਸਾ for *assurance* and flagged that ਭਰੋਸਾ was already carrying *confidence* from the confidence-threshold entry; C7 is the first chapter where both senses appear in one document — ਸਲਾਮਤੀ ਭਰੋਸਾ in the title and ਭਰੋਸਾ ਸਕੋਰ in 7.2.2. The overload does not create ambiguity inside any single sentence, so C7 conforms to the standing pick rather than unilaterally splitting the term mid-corpus. Recorded here so reviewers can see the collision in situ. **What could flip it:** if reviewers do split them, ਯਕੀਨਦਹਾਨੀ is the recommended form for *assurance* (it names the giving of assurance through evidence, which is what a verification standard asserts), leaving ਭਰੋਸਾ to ML confidence scores; the change would touch this chapter's title and every C1 assurance heading together. |
| **Reviewer notes** | |

---

## Q68 — confidence score / confidence estimation method (C7 extension)

| Field | Value |
|---|---|
| **EN term** | confidence score, confidence estimation method (7.2.1, 7.2.2) — extending the earlier **confidence threshold** entry |
| **Current pick** | ਭਰੋਸਾ ਸਕੋਰ (confidence score); ਭਰੋਸਾ ਅਨੁਮਾਨ ਵਿਧੀ (confidence estimation method) |
| **Alternatives** | ਵਿਸ਼ਵਾਸ ਸਕੋਰ (**rejected** — ਵਿਸ਼ਵਾਸ leans to faith/belief, excluded by §5.2); ਕਾਨਫ਼ੀਡੈਂਸ ਸਕੋਰ (L, full loan) |
| **Type** | T + L |
| **Reasoning** | The head noun ਭਰੋਸਾ is already settled by the earlier confidence-threshold entry; this entry only records the two C7 compounds built on it. ਭਰੋਸਾ also underpins the corpus's ਭਰੋਸੇਯੋਗ / ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ (trusted/untrusted, `GLOSSARY.md`), which matters in 7.2.1 where "reliability" (ਭਰੋਸੇਯੋਗਤਾ) and "confidence" (ਭਰੋਸਾ) appear in one sentence — the shared root is intentional, not an accident. Note ਅਨੁਮਾਨ is used here in its true *estimation* sense, which is precisely the sense the **inference** entry rejected it for; the two uses do not conflict. |
| **Reviewer notes** | |

---

## Q69 — threshold (C7 conformance note)

| Field | Value |
|---|---|
| **EN term** | a defined threshold (7.2.2) |
| **Current pick** | ਥ੍ਰੈਸ਼ਹੋਲਡ (L), conforming to the earlier **confidence threshold** entry |
| **Alternatives** | ਹੱਦ (T, "limit/bound" — this chapter's initial draft pick, changed to conform); ਸੀਮਾ (**rejected** — `GLOSSARY.md` binds ਸੀਮਾ to *limit* in ਦਰ ਸੀਮਾ, and 7.1.2 uses it for length limits in this same chapter) |
| **Type** | L |
| **Reasoning** | The earlier confidence-threshold entry already took the loan ਥ੍ਰੈਸ਼ਹੋਲਡ and asked whether it should become the corpus-wide standing form for *threshold*. C7 answers that in the affirmative by conforming. The native ਹੱਦ was the initial C7 draft and remains a viable corpus-wide alternative — it is short and keeps ਸੀਮਾ free for *limit* just as well — but it should be adopted everywhere at once or not at all. C7 is the chapter where the limit/threshold contrast is sharpest: 7.1.2 bounds output length (ਸੀਮਾ) while 7.2.2 trips a behavior change (ਥ੍ਰੈਸ਼ਹੋਲਡ). **What could flip it:** a reviewer decision to nativise; ਹੱਦ is then the recommended form. **Cross-file audit 2026-08-26:** C02 2.2.1 was still carrying the pre-conformance ਹੱਦਾਂ (thresholds) while C01 1.3.2 and C07 7.2.2 were on ਥ੍ਰੈਸ਼ਹੋਲਡ — the conformance decision recorded here had never been propagated back to C02. C02 2.2.1 normalised to ਥ੍ਰੈਸ਼ਹੋਲਡਾਂ. Note C03 3.5.2's ਹੱਦੋਂ ਵੱਧ is *not* this term (it renders "over-" in over-optimization) and was left alone. |
| **Reviewer notes** | |

---

## Q70 — fallback (message)

| Field | Value |
|---|---|
| **EN term** | fallback message (7.2.2) |
| **Current pick** | ਫ਼ਾਲਬੈਕ ਸੁਨੇਹਾ |
| **Alternatives** | ਬਦਲਵਾਂ ਸੁਨੇਹਾ (T, "alternative message"); ਪਿੱਛੇ-ਹਟਾਅ ਸੁਨੇਹਾ (T, coined) |
| **Type** | H (L head + T) |
| **Reasoning** | "Fallback" is settled software-engineering vocabulary with no established Panjabi equivalent, so §4 assigns it the L path. ਬਦਲਵਾਂ would understate the obligation — a fallback is the *safe* response, not merely a different one — and §6.3 forbids softening a requirement. ਪਿੱਛੇ-ਹਟਾਅ is unattested and would read as retreat. |
| **Reviewer notes** | |

---

## Q71 — grounded / grounding (RAG-grounded)

| Field | Value |
|---|---|
| **EN term** | RAG-grounded outputs (C7.4 section intro) |
| **Current pick** | RAG-ਆਧਾਰਿਤ ("RAG-based") |
| **Alternatives** | ਜ਼ਮੀਨੀ / ਧਰਾਤਲੀ (T, literal "grounded"); ਟਿਕਾਇਆ ਹੋਇਆ (T, "anchored"); ਆਧਾਰਬੱਧ (T, acceptable synonym) |
| **Type** | T |
| **Reasoning** | "Grounding" sits on the `CLAUDE.md` high-risk metaphor list. The English is a metaphor for "anchored in retrieved evidence," and the neutral technical rendering of that is ਆਧਾਰਿਤ (based on / founded on); any literal earth/ground rendering imports imagery the source does not intend, and ਟਿਕਾਇਆ ਹੋਇਆ is unattested in this sense. ਆਧਾਰਿਤ is also the commoner form over ਆਧਾਰਬੱਧ and already composes with the **AI agent** entry's ਏਜੰਟ-ਅਧਾਰਿਤ. **Cross-file audit 2026-08-27 — earlier claim corrected:** this entry previously asserted "**Must stay consistent with C8 (Memory, Embeddings & Vector Database)**, which uses the same term." It does not. *ground / grounded / grounding* does not occur anywhere in C08's English source, and RAG-ਆਧਾਰਿਤ appears exactly once corpus-wide, at `0x10-C07`:85. The real second site is `0x90-Appendix-A`:184, where the **Hallucination** definition renders "not grounded in" as ਉੱਤੇ ਆਧਾਰਿਤ ਨਹੀਂ — the same pick, so the two must move together. The consistency obligation transfers to C08 only if a later revision introduces the term there. **Cross-file audit 2026-08-26:** the corpus was split 3–3 between ਆਧਾਰਿਤ (Preface, C04, C07) and the short-vowel ਅਧਾਰਿਤ (0x03 ×2 in ਏਜੰਟ-ਅਧਾਰਿਤ, C02 2.1.2 in ਨੀਤੀ-ਅਧਾਰਿਤ) — including inside this entry's own claim that it "already composes with ਏਜੰਟ-ਅਧਾਰਿਤ," which was self-contradictory. All normalised to **ਆਧਾਰਿਤ** (the ਆਧਾਰ root takes the long ā); Q17 corrected to match. |
| **Reviewer notes** | |

---

## Q72 — attribution in RAG responses (extends the dataset-attribution entry)

| Field | Value |
|---|---|
| **EN term** | source attribution, RAG attributions (C7.4 heading, 7.4.1, 7.4.2) |
| **Current pick** | ਸਰੋਤ-ਨਿਰਧਾਰਨ, glossed `(attribution)` on first use — the same rendering the earlier **attribution (of dataset use)** entry picked |
| **Alternatives** | ਹਵਾਲਾ (**rejected** — reserved for *citation*, which stands beside *attribution* in this very heading, and for the References/ਹਵਾਲੇ section per ASVS precedent); ਸਿਹਰਾ (**rejected** — congratulatory register); ਐਟ੍ਰੀਬਿਊਸ਼ਨ (L) |
| **Type** | T |
| **Reasoning** | The earlier entry warned that other senses of *attribution* may not inherit its pick, so this is an explicit check rather than an assumption: C7.4's sense is "which retrieved document produced this claim," which is the same traceability mechanism as 1.1.5's "traced back to its source dataset" — so the rendering does transfer, and using a second form would fragment one concept across two chapters. Kept distinct from ਹਵਾਲਾ because 7.4.2 turns on the difference: attributions must come from retrieval metadata, not from the model, whereas a citation is the artifact the reader sees. **Still the weakest pick in C7 — flagged for reviewer adjudication**, and note the earlier entry's caution that threat-intel attribution in C11/C12 likely needs a different word again. |
| **Reviewer notes** | |

---

## Q73 — provenance

| Field | Value |
|---|---|
| **EN term** | provenance (7.4.2 — "so provenance cannot be fabricated") |
| **Current pick** | ਮੂਲ-ਸਰੋਤ, glossed `(provenance)` on first use |
| **Alternatives** | ਉਤਪਤੀ (T, "origination" — cosmological/creation overtones in Panjabi religious register); ਵੰਸ਼ (T, "lineage" — genealogical); ਪ੍ਰੋਵੀਨੈਂਸ (L) |
| **Type** | T |
| **Reasoning** | Provenance means "documented chain of origin". ਮੂਲ-ਸਰੋਤ (root-source) states that plainly without ਉਤਪਤੀ's creation-narrative connotation, which §5 puts out of bounds. **Cross-file audit 2026-08-26 — earlier claim corrected:** this entry previously asserted that C1 and C6 "use the same word." They do not: *provenance* does not occur in the English source of C01 or C06 at all, and ਮੂਲ-ਸਰੋਤ appears nowhere in either Panjabi file. The term's only two occurrences corpus-wide are C7 7.4.2 and `0x03-Using-AISVS.md` (out-of-scope list, "build provenance") — both already ਮੂਲ-ਸਰੋਤ, so the pick is consistent. The harmonisation obligation transfers to C11/C12 if they introduce the term. |
| **Reviewer notes** | |

---

## Q74 — chunk (retrieved chunk)

| Field | Value |
|---|---|
| **EN term** | retrieved chunk (7.4.3) |
| **Current pick** | ਚੰਕ (L), glossed `(chunk)` on first use |
| **Alternatives** | ਟੁਕੜਾ (T, "piece" — too generic, collides with generic "fragment"); ਖੰਡ (T, "segment") |
| **Type** | L |
| **Reasoning** | A chunk is a specific RAG-pipeline artifact (a retrieval unit of a document), not a generic piece of text; the loan keeps it identifiable to practitioners. ਖੰਡ is additionally excluded by its morphological near-collision with ਅਖੰਡਤਾ, the locked term for *integrity*, which appears in this very chapter's C7.4 title. **Cross-file audit 2026-08-26 — earlier claim corrected:** "Must match C8" was unverifiable as written: *chunk* does not occur in C08's English source, and ਚੰਕ appears only once corpus-wide (C7 7.4.3). Nothing to reconcile today; the constraint becomes live only if C08 or C09 introduces the retrieval-unit sense. |
| **Reviewer notes** | |

---

## Q75 — homoglyph

| Field | Value |
|---|---|
| **EN term** | homoglyphs (7.3.4) |
| **Current pick** | `homoglyph` retained in Latin, glossed ਸਮਰੂਪ ਅੱਖਰ ("look-alike characters") |
| **Alternatives** | ਸਮਰੂਪ ਅੱਖਰ alone (T — clear, but loses the searchable technique name); ਹੋਮੋਗਲਿਫ਼ (L — transliteration adds nothing over retention) |
| **Type** | R (+ T gloss) |
| **Reasoning** | Follows `GLOSSARY.md`'s named-attack/technique retention pattern (Padding Oracle, TOCTOU, prompt injection): the English name is what an implementer will search for in Unicode security literature, with a native gloss for readability. |
| **Reviewer notes** | |

---

## Q76 — classifier (C7 conformance note)

| Field | Value |
|---|---|
| **EN term** | automated classifiers (7.3.1); classified as high-risk (7.2.3) |
| **Current pick** | ਵਰਗੀਕਾਰ (classifier) / ਵਰਗੀਕ੍ਰਿਤ (classified), conforming to the earlier **classifier / content classification** entry |
| **Alternatives** | ਵਰਗੀਕਰਤਾ (T — this chapter's initial draft pick, changed to conform; both derive regularly from ਵਰਗੀਕਰਨ); ਕਲਾਸੀਫਾਇਰ (L) |
| **Type** | T |
| **Reasoning** | C2 already settled the agent noun as ਵਰਗੀਕਾਰ; C7 uses the identical component for output-side filtering and must not introduce a second form of the same word. Recorded because C7 adds the participle **ਵਰਗੀਕ੍ਰਿਤ** ("classified as", 7.2.3), which was not covered by the C2 entry and shares the ਵਰਗੀਕਰਨ root. The term must stay mechanical — a classifier here is a model acting as a filter, and §5.2 forbids vocabulary implying cognition. |
| **Reviewer notes** | |

---

## Q77 — downstream (systems / risk)

| Field | Value |
|---|---|
| **EN term** | downstream systems, downstream injection risk (C7 control objective, C7.1, C7.2) |
| **Current pick** | ਡਾਊਨਸਟ੍ਰੀਮ (L) |
| **Alternatives** | ਹੇਠਲੇ-ਧਾਰਾ / ਪ੍ਰਵਾਹ-ਅਧੀਨ (T, literal "down-current"); ਅੱਗੇ ਵਾਲੇ ਸਿਸਟਮ (T, "systems further on") |
| **Type** | L |
| **Reasoning** | "Downstream" is pipeline vocabulary with no settled Panjabi equivalent, and literal water-flow renderings mislead a reader into a physical-flow reading. ਅੱਗੇ ਵਾਲੇ is readable but imprecise about data-flow direction, which is the whole point of the term in an injection-risk sentence. Consistent with the corpus's willingness to take loans for pipeline/infrastructure nouns (ਪ੍ਰੌਕਸੀ, ਕਨੈਕਸ਼ਨ ਪੂਲ, ਇਨਵੈਂਟਰੀ in `GLOSSARY.md`, ਪਾਈਪਲਾਈਨ in the **retrieval pipeline** entry). Recurs in C9 and C10. |
| **Reviewer notes** | |

---

## Q78 — output (model output)

| Field | Value |
|---|---|
| **EN term** | output, model output, model-generated output (C7 chapter-wide, incl. the chapter title) |
| **Current pick** | ਆਊਟਪੁੱਟ (L) |
| **Alternatives** | ਨਿਕਾਸ (T, "emission/exit" — industrial connotation); ਨਤੀਜਾ (T, "result") |
| **Type** | L |
| **Reasoning** | Mirrors the ASVS corpus's ਇਨਪੁੱਟ (input, `0x14-V5-File-Handling.md` 5.3.1) so the input/output pair reads symmetrically across both standards; ਨਤੀਜਾ would break that pairing and collide with "result". This is C7's most frequent term, logged so C2 (Input Validation), C9 and C11 do not re-derive it differently. |
| **Reviewer notes** | |

---

## Q79 — memory (AI/agent sense, as a system component)

| Field | Value |
|---|---|
| **EN term** | memory — listed as an AI system component alongside datasets, models, retrieval systems, agents and tools (Preface, Design Principles; C08 title) |
| **Current pick** | ਮੈਮੋਰੀ |
| **Alternatives** | ਯਾਦਦਾਸ਼ਤ (T, human recollection — anthropomorphises the store); ਸਿਮਰਤੀ / ਸਮ੍ਰਿਤੀ (T, Sanskritic) — **rejected**; ਭੰਡਾਰ (T, "store" — loses the term of art) |
| **Type** | L |
| **Reasoning** | Q49 claimed ਮੈਮੋਰੀ for the *hardware* sense in C04 and explicitly deferred the agent-memory sense to C08; the Preface uses the term in that deferred sense, so it is logged here rather than silently reused. Same pick, for the same reason: ਸਿਮਰਤੀ shares a root with ਸਿਮਰਨ (devotional remembrance) and is a direct Gurmat collision excluded by `TRANSLATION-RULES.md` §5.2, while ਯਾਦਦਾਸ਼ਤ ascribes human recollection to a stored-state component — the anthropomorphism failure Q6 (bias) and Q7 (behavior) already guard against. **What could flip it:** C08 owns the final call; if it distinguishes agent memory from hardware memory, the distinction should be carried by the modifier, not by swapping the head noun. |
| **Reviewer notes** | |

---

## Q80 — control family

| Field | Value |
|---|---|
| **EN term** | control family — the 12 top-level AISVS divisions (Preface, Design Principles) |
| **Current pick** | ਨਿਯੰਤਰਣ ਪਰਿਵਾਰ |
| **Alternatives** | ਨਿਯੰਤਰਣ ਸਮੂਹ (T, "control group" — collides with the experimental-design sense); ਨਿਯੰਤਰਣ ਸ਼੍ਰੇਣੀ (T, "control category"); ਕੰਟਰੋਲ ਫ਼ੈਮਲੀ (L) |
| **Type** | T |
| **Reasoning** | ਨਿਯੰਤਰਣ for *control* carries ASVS sibling precedent (the chapter heading ਨਿਯੰਤਰਣ ਉਦੇਸ਼ = Control Objective), so only the head noun was open. ਪਰਿਵਾਰ mirrors the English metaphor exactly and matches how NIST SP 800-53 "control families" are discussed in Panjabi-language security writing. ਸਮੂਹ was rejected for the statistics collision; ਸ਼੍ਰੇਣੀ is defensible but should stay free for "category/class". Logged because the term recurs in `0x03-Using-AISVS.md` and in every C-chapter and must not drift between them. **Boundary recorded 2026-08-26:** standalone *control(s)* = **ਨਿਯੰਤਰਣ** corpus-wide (40+ uses); the loan **ਕੰਟਰੋਲ** is reserved for the fixed compound ਪਹੁੰਚ ਕੰਟਰੋਲ (*access control*, per `GLOSSARY.md`). C02 2.1.4 was the single violation — it rendered "input length controls" as ਲੰਬਾਈ ਕੰਟਰੋਲ / ਇਹਨਾਂ ਕੰਟਰੋਲਾਂ while C07 7.1.2 rendered the parallel "termination controls" as ਸਮਾਪਤੀ ਨਿਯੰਤਰਣਾਂ. Normalised to ਨਿਯੰਤਰਣ / ਨਿਯੰਤਰਣਾਂ. |
| **Reviewer notes** | |

---

## Q81 — autonomous (agents)

| Field | Value |
|---|---|
| **EN term** | autonomous agents (Preface; C09 Orchestration and Agentic Action) |
| **Current pick** | ਖ਼ੁਦਮੁਖ਼ਤਾਰ ਏਜੰਟ |
| **Alternatives** | ਸਵੈ-ਚਾਲਿਤ (T, "self-driven/automatic" — describes unattended automation, not delegated decision authority); ਸੁਤੰਤਰ (T, "free/independent"); ਆਟੋਨੋਮਸ (L) |
| **Type** | T modifier + L head (ਏਜੰਟ per Q17) |
| **Reasoning** | The head noun is settled at Q17; only the modifier was open. ਖ਼ੁਦਮੁਖ਼ਤਾਰ ("self-governing") is well-attested political and administrative Panjabi and carries the security-relevant sense — the system decides and acts with no human in the loop — rather than merely running unattended, which is what ਸਵੈ-ਚਾਲਿਤ says. ਸੁਤੰਤਰ was rejected because ਸੁਤੰਤਰਤਾ/ਮੁਕਤੀ vocabulary carries liberation connotations of the class `TRANSLATION-RULES.md` §5.2 warns against for agent and behaviour terms. **What could flip it:** C09 is the deciding chapter for the agentic vocabulary; a change there should propagate here. |
| **Reviewer notes** | |

---

## Q82 — model inversion (and model extraction in prose)

| Field | Value |
|---|---|
| **EN term** | "models can be extracted, inverted, or manipulated" (Preface) |
| **Current pick** | English attack names retained in parentheses — `(model extraction)`, `(model inversion)` — with the surrounding prose verbs translated (ਕੱਢਿਆ / ਉਲਟਾਇਆ) |
| **Alternatives** | Coin standalone Panjabi noun phrases ਮਾਡਲ ਕੱਢਣਾ / ਮਾਡਲ ਉਲਟਾਉਣਾ (T); retain the English with no Panjabi verb at all (R) |
| **Type** | R (attack names) + T (prose verbs) |
| **Reasoning** | `GLOSSARY.md` retains named attacks and techniques verbatim (ASVS precedent: Padding Oracle, TOCTOU) and requires the gloss decision to be logged. Q54 already fixes the boundary for *model extraction* — ਮਾਡਲ ਚੋਰੀ names the harm, the technique name stays English — and this entry records the same treatment for *model inversion*, which Q54 does not cover. Because the Preface sentence is explanatory prose rather than normative requirement text, a translated verb reads naturally while the parenthetical keeps the technique name searchable against the English standard. **What could flip it:** if C03 or C11 uses these as noun phrases in requirement text, they must stay fully retained there rather than inheriting the prose treatment. |
| **Reviewer notes** | |

---

## Q83 — orchestration

| Field | Value |
|---|---|
| **EN term** | orchestration (C09 title, cited in `0x03-Using-AISVS.md` cross-reference prose) |
| **Current pick** | ਆਰਕੈਸਟ੍ਰੇਸ਼ਨ |
| **Alternatives** | ਤਾਲਮੇਲ (T, "coordination" — accurate but generic); ਪ੍ਰਬੰਧ (T — collides with ਪ੍ਰਬੰਧਨ, already load-bearing for "management/handling" in ਗਲਤੀ ਪ੍ਰਬੰਧਨ, ਸੈਸ਼ਨ ਪ੍ਰਬੰਧਨ); ਸੰਚਾਲਨ (T — reserved for "operation(s)", used in this same file for platform/telemetry operations) |
| **Type** | L |
| **Reasoning** | ਤਾਲਮੇਲ is the closest native word but means plain coordination between parties and loses the AISVS sense of a *control plane that drives multi-step model, tool and agent execution* — exactly the thing C09 requires you to constrain. Both obvious Sanskritic alternatives are already spoken for elsewhere in the corpus, so a native pick would create a silent collision rather than avoid one. The loan follows the ASVS practice for infrastructure-layer terms (ਪ੍ਰੌਕਸੀ, ਕਨੈਕਸ਼ਨ, ਇਨਵੈਂਟਰੀ in `GLOSSARY.md`). **What could flip it:** C09 is the deciding chapter — if it coins a compound that keeps the control-plane sense (e.g. ਸੰਚਾਲਨ-ਤਾਲਮੇਲ), it should propagate back here rather than diverge. |
| **Reviewer notes** | |

---

## Q84 — robustness (adversarial robustness)

| Field | Value |
|---|---|
| **EN term** | adversarial robustness (C11 title, cited in `0x03-Using-AISVS.md` cross-reference prose) |
| **Current pick** | ਵਿਰੋਧੀ ਮਜ਼ਬੂਤੀ |
| **Alternatives** | ਵਿਰੋਧੀ ਸਹਿਣਸ਼ੀਲਤਾ (T, "tolerance/endurance" — robustness is resistance to crafted input, not endurance, and ਸਹਿਣਸ਼ੀਲਤਾ should stay free for fault tolerance); ਵਿਰੋਧੀ ਦ੍ਰਿੜ੍ਹਤਾ (T, "steadfastness" — ascribes resolve, an inner quality, to a model); ਰੋਬਸਟਨੈੱਸ (L) |
| **Type** | T |
| **Reasoning** | Only the head noun was open: *adversarial* is already fixed as ਵਿਰੋਧੀ at Q35, and this file reuses it for "adversarial contexts" in the levels table, so one modifier serves both. ਮਜ਼ਬੂਤੀ ("sturdiness, strength") is the plain non-metaphorical robustness word; ਦ੍ਰਿੜ੍ਹਤਾ was rejected under `TRANSLATION-RULES.md` §5.2 because words for inner resolve drift toward a devotional register and anthropomorphise the model — the same failure shape guarded against at Q6 (bias) and Q7 (behavior). **What could flip it:** C11 owns the chapter title; if it prefers a different head noun, this cross-reference must move with it, and ਵਿਰੋਧੀ must not change independently of Q35. |
| **Reviewer notes** | |

---

## Q85 — model card

| Field | Value |
|---|---|
| **EN term** | model cards — vendor documentation used as assessment evidence (`0x03-Using-AISVS.md`, Assessments section; also listed as out-of-scope governance artifacts) |
| **Current pick** | ਮਾਡਲ ਕਾਰਡ |
| **Alternatives** | ਮਾਡਲ ਵੇਰਵਾ-ਪੱਤਰ (H, "model detail-sheet"); ਮਾਡਲ ਦਸਤਾਵੇਜ਼ (T, "model documentation" — too broad); retain `model card` in Latin (R) |
| **Type** | L (ਮਾਡਲ per `GLOSSARY.md`; ਕਾਰਡ ordinary Panjabi loan) |
| **Reasoning** | A model card is a *named artifact type* with a fixed industry meaning — documented provenance, training data, evaluation results, and stated limitations. A descriptive rendering such as ਵੇਰਵਾ-ਪੱਤਰ or ਦਸਤਾਵੇਜ਼ would suggest that any vendor documentation satisfies the requirement, weakening the evidentiary claim the assessment section makes; that would be a softening of an obligation, which `TRANSLATION-RULES.md` §6.3 forbids. ਮਾਡਲ is already settled as a loan in `GLOSSARY.md`, so the loan pair keeps a one-to-one mapping to the artifact an auditor will actually request. **What could flip it:** if Appendix A defines the artifact in full, a one-time native gloss on first use becomes affordable without loss of precision. |
| **Reviewer notes** | |

---

## Q86 — English /f/ in loanwords: nukta or bare ਫ (orthographic rule, not a term)

| Field | Value |
|---|---|
| **EN term** | any transliterated loan whose English source begins or contains /f/ — *format*, *platform*, *federated*, *firmware*, *feedback*, *filter*, *file*, *fine-tuning*, *feature*, *fallback*, *format(ting)* |
| **Current pick** | **ਫ਼** (with nukta) for English /f/ |
| **Alternatives** | bare ਫ (aspirated /pʰ/) throughout; per-word case-by-case |
| **Type** | orthographic convention governing L-type terms |
| **Reasoning** | Raised by the 2026-08-26 cross-file terminology audit, which found the corpus split on five loans rendering the *same* English word two ways across chapters: *format* — ਫਾਰਮੈਟ (`0x03`:28, C04 4.1.2) vs ਫ਼ਾਰਮੈਟ (C07 C7.1, 7.3.4); *platform* — ਪਲੇਟਫਾਰਮ (`0x03`:144, :145) vs ਪਲੇਟਫ਼ਾਰਮ (C01 C1.2, 1.2.1); *federated* — ਫੈਡਰੇਟਿਡ (C04 C4.3) vs ਫ਼ੈਡਰੇਟਿਡ (C05 5.1.2); plus singletons ਫਰਮਵੇਅਰ (C04 4.2.1) and ਫੀਡਬੈਕ (`0x01`:43) against the corpus's own ਸਾਫ਼ਟਵੇਅਰ. Bare ਫ is the aspirated stop /pʰ/, a different phoneme; `TRANSLATION-RULES.md` §1.4 requires proper use of nukta, and the corpus's dominant practice already follows it — ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ (×10), ਇਨਫ਼ਰੈਂਸ, ਆਰਟੀਫ਼ੈਕਟ, ਫ਼ਿਲਟਰ, ਫ਼ਾਈਲ, ਫ਼ੀਚਰ, ਫ਼ਾਲਬੈਕ, ਸਾਫ਼ਟਵੇਅਰ, ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ. All five splits normalised to ਫ਼. **Explicit carve-outs:** (a) ਫ੍ਰੇਮਵਰਕ keeps bare ਫ because it is locked that way in `GLOSSARY.md` from the ASVS sibling corpus — changing it unilaterally would diverge the two corpora, so it must move in both or neither; (b) native Panjabi words with genuine /pʰ/ (ਫੈਲਣਾ, ਫੇਰੀ) are untouched. **What could flip it:** a reviewer decision to carry ਫ੍ਰੇਮਵਰਕ's bare-ਫ treatment to all loans instead — in which case this rule inverts and ~30 sites change together, never per chapter. |
| **Reviewer notes** | |

---

## Q87 — Model Context Protocol (MCP) and its method names

| Field | Value |
|---|---|
| **EN term** | Model Context Protocol (MCP) (C10 title and chapter-wide); the protocol method names `tools/list`, `tools/call`, `initialize` (10.2.4, 10.3.4, 10.4.1, 10.4.2) |
| **Current pick** | `Model Context Protocol (MCP)` retained verbatim, including the expanded phrase; method names retained verbatim in backticks |
| **Alternatives** | ਮਾਡਲ ਸੰਦਰਭ ਪ੍ਰੋਟੋਕੋਲ (T/L — every part has a settled rendering: ਮਾਡਲ, ਸੰਦਰਭ locked in `GLOSSARY.md`, ਪ੍ਰੋਟੋਕੋਲ a loan); ਐਮਸੀਪੀ (transliterated acronym — prohibited by `TRANSLATION-RULES.md` §4 R-rule); translating the method names descriptively (ਟੂਲ-ਸੂਚੀ / ਟੂਲ-ਸੱਦਾ) |
| **Type** | R |
| **Reasoning** | `GLOSSARY.md` lists MCP among the always-retained protocol names and states that model/dataset/library/**protocol** names are never translated or transliterated. Unlike "artificial intelligence" (Q8), where the expanded phrase appears once in the standard's own name and earns a Panjabi rendering, "Model Context Protocol" is the wire-protocol's proper name — a reader must be able to match it against the specification this chapter cites. The method names are literal strings sent on the wire: translating them would produce text that cannot be typed into a request, so they are kept in backticks exactly as the source spells them (the source writes them unformatted; the backticks are a readability addition, not a change of content). **What could flip it:** nothing likely; logged so C12 and the appendices do not introduce a competing Panjabi expansion. |
| **Reviewer notes** | |

---

## Q88 — server / client (MCP server, MCP client)

| Field | Value |
|---|---|
| **EN term** | MCP server, MCP client, locally launched server, resource server (C10 chapter-wide) |
| **Current pick** | ਸਰਵਰ / ਕਲਾਇੰਟ |
| **Alternatives** | ਸੇਵਾਦਾਰ (T, "one who serves" — **rejected**: ਸੇਵਾ/ਸੇਵਾਦਾਰ is load-bearing devotional vocabulary in Gurmat register for selfless service, and the corpus already binds ਸੇਵਾ to *service* in ਸੇਵਾ ਖਾਤਾ / ਸੇਵਾ-ਇਨਕਾਰ); ਪਰੋਸਣਹਾਰ (T, coinage); ਗਾਹਕ for client (T, "customer" — a different entity, and already the rejected candidate for *tenant* at Q22) |
| **Type** | L (both) |
| **Reasoning** | No ASVS precedent — neither word occurs anywhere in the pa-IN corpus before this chapter. Both are the ordinary loans in Panjabi computing prose, and they must stay a matched pair because C10 contrasts them in a single requirement six times (10.2.7, 10.3.5, 10.4.6, 10.4.7, 10.4.8). ਸੇਵਾਦਾਰ was excluded on `TRANSLATION-RULES.md` §5 grounds before its accuracy was considered; ਗਾਹਕ would additionally collide with the reading Q22 already rejected for *tenant*. Note that *resource server* (10.2.3) is rendered ਸਰੋਤ ਸਰਵਰ and *resource owner* (10.2.4) ਸਰੋਤ ਮਾਲਕ — see Q89. **What could flip it:** nothing likely; logged because C12 (Monitoring & Logging) will need the same pair. |
| **Reviewer notes** | |

---

## Q89 — OAuth 2.1 role and claim vocabulary (claims, audience, resource server, resource owner)

| Field | Value |
|---|---|
| **EN term** | access token, issuer / audience / expiration / scope **claims**, resource server, resource owner (10.2.1–10.2.5) |
| **Current pick** | ਪਹੁੰਚ ਟੋਕਨ; ਦਾਅਵੇ (claims); ਜਾਰੀਕਰਤਾ (issuer), ਉਦੇਸ਼ਿਤ ਪ੍ਰਾਪਤਕਰਤਾ (audience), ਮਿਆਦ ਸਮਾਪਤੀ (expiration); ਸਰੋਤ ਸਰਵਰ (resource server), ਸਰੋਤ ਮਾਲਕ (resource owner) — each glossed in English on first use |
| **Alternatives** | Retain the four claim names verbatim as `iss` / `aud` / `exp` / `scope` (the source spells them out in words, not as JWT keys, so retention would be less faithful, not more); ਸਰੋਤੇ or ਦਰਸ਼ਕ for *audience* (**rejected** — both mean a listening/viewing public, a silent meaning inversion: an OAuth audience is the single intended recipient); ਸ਼੍ਰੋਤਾ (same objection, plus Sanskritic devotional register); ਕਲੇਮ (L) |
| **Type** | T (with English glosses); ਟੋਕਨ and ਸਕੋਪ per existing corpus picks |
| **Reasoning** | `TRANSLATION-RULES.md` §4 retains "header/claim/parameter names **as they appear verbatim in source**" — here the source does *not* use the wire keys, it names the concepts in English words inside a prose sentence, so the R-rule does not bite and a translated-with-gloss rendering is the faithful one. ਜਾਰੀਕਰਤਾ for *issuer* is already locked in `GLOSSARY.md`, which fixes the register for the other three; leaving *audience* in Latin beside a translated ਜਾਰੀਕਰਤਾ would read as an arbitrary split inside one list. ਉਦੇਸ਼ਿਤ ਪ੍ਰਾਪਤਕਰਤਾ ("intended recipient") states what the aud claim actually constrains, and ਪ੍ਰਾਪਤਕਰਤਾ is already used for *recipients* in C09 9.2.2. ਦਾਅਵਾ for *claim* matches C07 7.4.3, where ਦਾਅਵਿਆਂ renders the claims in a RAG response — the same "asserted statement" sense. **What could flip it:** if a later chapter quotes the JWT keys themselves, those stay R and this entry must not be read as licence to translate them. |
| **Reviewer notes** | |

---

## Q90 — transport (MCP transport; stdio, streamable HTTP)

| Field | Value |
|---|---|
| **EN term** | transport, secure transport, MCP transport, stdio transport, HTTP-based transports, streamable HTTP (C10.3, 10.3.1–10.3.3, 10.4.5) |
| **Current pick** | ਟ੍ਰਾਂਸਪੋਰਟ — conforming to `0x03-Using-AISVS.md` (ਟ੍ਰਾਂਸਪੋਰਟ ਸੁਰੱਖਿਆ, *transport security*); the named transports `stdio` and `streamable HTTP` retained verbatim |
| **Alternatives** | ਢੋਆ-ਢੁਆਈ (T, "haulage/freight" — physical goods transport, absurd for a protocol channel); ਸੰਚਾਰ ਪਰਤ (T, "communication layer" — describes the layer, not the specific channel, and ਸੰਚਾਰ is already used for *communications* in this same section intro); ਵਾਹਕ (T, "carrier") |
| **Type** | L (named transports R) |
| **Reasoning** | The loan was already on disk before this chapter, so this entry is a conformance record plus an extension: `0x03` used *transport* only inside the compound "transport security," whereas C10.3 uses it as a countable noun for the channel itself (ਸਾਰੇ MCP ਟ੍ਰਾਂਸਪੋਰਟ, 10.4.5). The same loan carries both without strain. `stdio` is a POSIX stream name and `streamable HTTP` is the MCP specification's own name for a transport mode — both are identifiers a reviewer must match against the spec, so they stay Latin per the `GLOSSARY.md` retained-names rule. Note *communications* in the C10.3 intro is ਸੰਚਾਰ, deliberately a different word so the channel and the traffic on it stay distinguishable. |
| **Reviewer notes** | |

---

## Q91 — sender-constrained (mTLS, DPoP)

| Field | Value |
|---|---|
| **EN term** | sender-constrained access tokens (10.3.5) |
| **Current pick** | ਭੇਜਣ ਵਾਲੇ ਨਾਲ ਬੰਨ੍ਹੇ ਹੋਏ, glossed `(sender-constrained)`; mTLS and DPoP retained |
| **Alternatives** | ਭੇਜਣਹਾਰ-ਬੰਧਿਤ (T, compact coinage — unattested, and the ਬੰਧਿਤ form is Sanskritic where the corpus's existing verb is ਬੰਨ੍ਹਣਾ); ਪ੍ਰੇਸ਼ਕ-ਸੀਮਿਤ (T, Sanskritic ਪ੍ਰੇਸ਼ਕ = sender — register too high and unattested in Panjabi security writing); retain `sender-constrained` verbatim |
| **Type** | T (mechanism names R) |
| **Reasoning** | This is a descriptive OAuth property, not a branded technique, so the `GLOSSARY.md` retention rule for named attacks does not apply; the branded parts are the *mechanisms* (mTLS, DPoP), which are retained. The chosen phrase reuses the corpus's established verb for cryptographic binding — C09 9.2.8 and 9.4.2 both render "cryptographically bound" as ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ਿਕ ਤੌਰ 'ਤੇ … ਬੰਨ੍ਹੀਆਂ — so a reader sees 10.3.5 as the same mechanism applied to tokens rather than a new concept. ਸੀਮਿਤ was avoided for *constrained* here because it would suggest the token is merely restricted in scope, which is 9.5.2's ਸਕੋਪ-ਸੀਮਿਤ and a different control. **What could flip it:** reviewers may prefer the compact hyphenated coinage for table density. |
| **Reviewer notes** | |

---

## Q92 — replay attempts and DNS rebinding

| Field | Value |
|---|---|
| **EN term** | replay attempts (10.4.6); DNS rebinding attacks (10.3.3) |
| **Current pick** | `replay` retained in Latin, glossed **(ਦੁਹਰਾਓ)** on first use — `replay (ਦੁਹਰਾਓ) ਕੋਸ਼ਿਸ਼ਾਂ`; `DNS rebinding` retained verbatim — `DNS rebinding ਹਮਲੇ` |
| **Alternatives** | ਰੀਪਲੇ (L, transliterated — adds nothing over retention and breaks the search link); ਮੁੜ-ਭੇਜਣ ਹਮਲਾ (T, "resend attack" — loses the named-attack identity); for DNS rebinding: ਡੀਐਨਐਸ ਮੁੜ-ਬੰਧਨ (**rejected** — transliterating the acronym violates the §4 R-rule and the calque names nothing a practitioner would recognise) |
| **Type** | R (+ T gloss for *replay*) |
| **Reasoning** | Both are named attack classes, which `GLOSSARY.md` §Always-retained keeps Latin on first mention with a Panjabi gloss where a clean native rendering exists — the same treatment Q39 gave `data poisoning` and Q32 gave `many-shot jailbreaking`. ਦੁਹਰਾਓ ("repetition") is an accurate and Gurmat-neutral gloss for *replay* and is offered once; `DNS rebinding` gets no gloss because no native rendering of "rebinding" would point at the DNS-record behaviour the attack exploits, so a gloss would mislead rather than help. Both names are what an implementer will search for in the OWASP MCP Security Cheat Sheet this chapter cites. |
| **Reviewer notes** | |

---

## Q93 — consent dialogue / cancellation

| Field | Value |
|---|---|
| **EN term** | explicit consent dialogue and cancellation options (10.4.7) |
| **Current pick** | ਸਪੱਸ਼ਟ ਸਹਿਮਤੀ ਸੰਵਾਦ, glossed `(consent dialogue)`; *cancellation options* → ਰੱਦ ਕਰਨ ਦੇ ਵਿਕਲਪ |
| **Alternatives** | ਸਹਿਮਤੀ ਡਾਇਲਾਗ (H, loan for the UI widget); ਸਹਿਮਤੀ ਬਾਕਸ (H); ਰਜ਼ਾਮੰਦੀ (T, "willing agreement" — everyday register, and ਰਜ਼ਾ carries a Gurbani sense of the Divine Will that §5 puts out of bounds for a UI control); ਮਨਜ਼ੂਰੀ (**rejected** — locked to *approval* throughout C09 and 10.4.8's ਮੁੜ-ਮਨਜ਼ੂਰੀ) |
| **Type** | T |
| **Reasoning** | ਸਹਿਮਤੀ for *consent* already appears in `0x03-Using-AISVS.md` (ਸਹਿਮਤੀ ਪ੍ਰਬੰਧਨ, consent-management platforms), so only the head noun was open. ਸੰਵਾਦ is neutral formal Panjabi for a two-way exchange and is the standard rendering of a UI dialogue; the loan ਡਾਇਲਾਗ would be equally readable but introduces a new loan where an attested native word exists, which `TRANSLATION-RULES.md` §4 routes to T. ਰਜ਼ਾਮੰਦੀ was excluded on §5 grounds. Keeping ਮਨਜ਼ੂਰੀ free matters inside this very section: 10.4.7 is about *consent* at install time and 10.4.8 about *re-approval* of a changed tool, and collapsing them would blur two separate obligations. **What could flip it:** if C12 or an appendix needs "dialogue" in the conversational-turn sense, that use must not inherit this pick. |
| **Reviewer notes** | |

---

## Q94 — discovery (MCP component/tool discovery)

| Field | Value |
|---|---|
| **EN term** | secure discovery … of MCP-based tool and resource integrations (C10 control objective) |
| **Current pick** | ਖੋਜ, glossed `(discovery)` on first use |
| **Alternatives** | ਲੱਭਤ (T, "finding" — unattested as a technical noun); ਪਤਾ ਲਾਉਣਾ (T, verb phrase — cannot head a noun list); ਡਿਸਕਵਰੀ (L) |
| **Type** | T |
| **Reasoning** | **Logged specifically because of a known collision.** Q20 reserved ਖੋਜ for *lookup/search* (embedding ਖੋਜ) precisely so it would not be spent on *retrieval*; C10 now needs it for a third sense — the protocol act of enumerating available MCP servers and tools. The senses are close enough that no single sentence is ambiguous, and the English gloss on first use resolves it for a reader working against the source, so no new word was coined. Recorded so a reviewer sees the overload rather than discovering it: ਖੋਜ is now carrying *lookup* (C05, C08) and *discovery* (C10). **What could flip it:** if a reviewer splits them, ਖੋਜ should stay with the vector/embedding lookup sense that has the most sites on disk, and *discovery* should take the new word. |
| **Reviewer notes** | |

---

## Q95 — component (corpus split flagged by the C10 review, not silently changed)

| Field | Value |
|---|---|
| **EN term** | component(s) — as a term of art for a named part of an AI or MCP system (C5 title, C6.2.3, C9.3 heading, 9.3.5, C10.1 heading, C10.1 intro, 10.1.1; and C3.4.1, C4 control objective, C4.2 intro, C12 control objective) |
| **Current pick** | **ਕੰਪੋਨੈਂਟ** (L) — the form C10 uses, and the majority form on disk |
| **Alternatives** | ਹਿੱਸਾ (T, "part/portion" — the form C03, C04 and C12 use for the same English word); ਅੰਗ (T, "limb/member" — bodily register, worse); ਘਟਕ (T, Sanskritic "constituent" — unattested in Panjabi security writing) |
| **Type** | L |
| **Reasoning** | **Logged as a split, not resolved.** The 2026-08-27 independent review of C10 found *component* rendered two ways corpus-wide for the same term-of-art sense, with neither form recorded anywhere: the loan **ਕੰਪੋਨੈਂਟ** at 7 sites — `0x10-C05`:6 (chapter title), `0x10-C06`:57, `0x10-C09`:74 (section heading) and :97, `0x10-C10`:18 (section heading), :22 and :32 — against the native **ਹਿੱਸਾ** at 4 term-of-art sites — `0x10-C03`:94 ("runtime components"), `0x10-C04`:13 ("infrastructure components") and :45 ("hardware components"), `0x10-C12`:13 ("AI components"). Same failure shape as Q86 (English /f/) and Q80 (control/ਨਿਯੰਤਰਣ): two chapters picked independently, neither cited the other, and no lint check covers it. **C10 was left untouched** — it is on the majority side and matches its nearest neighbour C09, so changing it alone would deepen the split rather than close it, and a corpus normalisation must move all sites in one change (the Q86 rule). **Recommendation for the reviewer:** normalise the 4 native term-of-art sites to ਕੰਪੋਨੈਂਟ — the loan already holds three *headings* (C5 title, C9.3, C10.1), which are the costliest sites to move and the ones a reader navigates by. **Explicit carve-out:** ਹਿੱਸਾ is correct and should stay where the source means a generic part rather than a named system component — `0x03`:159 ("by attack or component") and `0x10-C12`:127 (12.5.1, "each dataset and its components"). **What could flip it:** a reviewer preference for native vocabulary in chapter titles, in which case all 7 loan sites move to ਹਿੱਸਾ together, never per chapter. |
| **Reviewer notes** | |

---

## Q96 — non-normative

| Field | Value |
|---|---|
| **EN term** | non-normative ("This inventory is non-normative", Appendix B objective) |
| **Current pick** | ਗ਼ੈਰ-ਨਿਯਮਬੱਧ, glossed `(non-normative)` on first use |
| **Alternatives** | ਗ਼ੈਰ-ਲਾਜ਼ਮੀ (T, "non-mandatory" — **rejected**, ਲਾਜ਼ਮੀ is bound corpus-wide to the hard *must* of requirement text per `GLOSSARY.md`, so reusing its negation here would read as a statement about obligation strength rather than about document status); ਗ਼ੈਰ-ਆਦੇਸ਼ਾਤਮਕ (T, Sanskritic "non-imperative" — over-formal and unattested); ਨਾਨ-ਨਾਰਮੇਟਿਵ (L) |
| **Type** | T |
| **Reasoning** | *Normative* is a standards term of art: it marks which parts of a document state requirements. ਨਿਯਮ ("rule") is free — the corpus uses ਨਿਯੰਤਰਣ for *control* and ਨਿਯਮ-ਸਮੂਹ for *ruleset* (C02 2.1.3), neither of which collides — so ਨਿਯਮਬੱਧ ("rule-bound") is available and reads correctly as "does not itself lay down rules". The ਗ਼ੈਰ- negation prefix follows the corpus pattern (ਗ਼ੈਰ-ਭਰੋਸੇਯੋਗ, ਗ਼ੈਰ-ਸਲਾਮਤ). Glossed in English because a reader checking conformance must be able to match the term to the English standard. **What could flip it:** if Appendix C or a future edition needs the positive form *normative* in contrast within one sentence, both forms must be settled together. |
| **Reviewer notes** | |

---

## Q97 — source of truth

| Field | Value |
|---|---|
| **EN term** | source of truth ("The requirement chapters (C1 through C12) remain the source of truth", Appendix B objective) |
| **Current pick** | ਫ਼ੈਸਲਾਕੁੰਨ ਸਰੋਤ, glossed `(source of truth)` on first use |
| **Alternatives** | ਸੱਚ ਦਾ ਸਰੋਤ (**rejected on Gurmat grounds** — ਸੱਚ / ਸਤਿ is load-bearing devotional vocabulary for Divine Truth in Gurbani; using it for a document's editorial precedence is exactly the spiritually-loaded near-synonym class `TRANSLATION-RULES.md` §5 forbids); ਪ੍ਰਮਾਣਿਕ ਸਰੋਤ (**rejected** — the ਪ੍ਰਮਾਣ- root is already triple-booked in `GLOSSARY.md` for authentication, validation, and *input validation* as ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ, which appears in this very file); ਅਧਿਕਾਰਤ ਸਰੋਤ (T, "authoritative" — ਅਧਿਕਾਰਤ is already in use for *authorized* across C09) |
| **Type** | T |
| **Reasoning** | What the English means here is narrow and procedural: when the appendix and a chapter disagree, the chapter decides. ਫ਼ੈਸਲਾਕੁੰਨ ("decisive, settling the matter") states precisely that, is neutral technical register, and builds on ਫ਼ੈਸਲਾ, already settled in the corpus (ਨੀਤੀ ਫ਼ੈਸਲਾ ਬਿੰਦੂ, Q24). Every shorter candidate was blocked either by Gurmat safety or by an existing lock. Glossed in English on first use. **What could flip it:** Appendix A (Glossary) may define the term; if so both files must agree. |
| **Reviewer notes** | |

---

## Q98 — common pitfalls

| Field | Value |
|---|---|
| **EN term** | Common pitfalls (the closing note of all 19 control families in Appendix B) |
| **Current pick** | ਆਮ ਗਲਤੀਆਂ, glossed `(common pitfalls)` on first use |
| **Alternatives** | ਆਮ ਫੰਦੇ (T, "common snares" — **rejected**, ਫੰਦਾ carries the Gurbani sense of the snare of māyā, §5); ਆਮ ਭੁਲੇਖੇ (**rejected** — ਭੁਲੇਖਾ is already excluded at Q65 as devotionally loaded); ਆਮ ਖ਼ਾਮੀਆਂ (**rejected** — `GLOSSARY.md` locks ਖ਼ਾਮੀ to *weakness* as a finding class, a different thing from an implementer's habitual mistake); ਆਮ ਸਮੱਸਿਆਵਾਂ (T, "common problems" — vaguer) |
| **Type** | T |
| **Reasoning** | A pitfall in this appendix is a recurring implementation mistake, not a vulnerability class and not a trap laid by an attacker, so the plain word is the honest one. Spelled **ਗਲਤੀ** without nukta to match the corpus's existing form (`GLOSSARY.md` ਗਲਤੀ ਪ੍ਰਬੰਧਨ = error handling; C01 uses ਗਲਤੀਆਂ) — this file must not introduce a second spelling of a word already on disk. English glossed on first use only; the remaining 18 occurrences are bare, since the pattern is established by then. **What could flip it:** ਆਮ ਸਮੱਸਿਆਵਾਂ if reviewers find ਗਲਤੀ too close to "error" in the ਗਲਤੀ ਪ੍ਰਬੰਧਨ sense. |
| **Reviewer notes** | |

---

## Q99 — authenticity

| Field | Value |
|---|---|
| **EN term** | authenticity (AD.5 and AD.12 section objectives — "verify authenticity and detect tampering", "verify origin and authenticity") |
| **Current pick** | ਅਸਲੀਅਤ, glossed `(authenticity)` on first use in AD.5 |
| **Alternatives** | ਪ੍ਰਮਾਣਿਕਤਾ (**rejected — collision**: this exact word renders *validation* throughout the corpus, including ਇਨਪੁੱਟ ਪ੍ਰਮਾਣਿਕਤਾ and ਸਕੀਮਾ ਪ੍ਰਮਾਣਿਕਤਾ in the same appendix, several rows above); ਸੱਚਾਈ (**rejected** — devotional register, same objection as Q88); ਪ੍ਰਮਾਣਿਕਤਾ ਅਤੇ ਮੂਲ ਦੀ ਪੁਸ਼ਟੀ (periphrastic); ਆਥੈਂਟਿਸਿਟੀ (L) |
| **Type** | T |
| **Reasoning** | This is the fifth member of the verb-precision cluster Q48 identified: verify (ਤਸਦੀਕ), validate (ਪ੍ਰਮਾਣਿਤ), authenticate (ਪ੍ਰਮਾਣੀਕਰਨ), certify (ਸਰਟੀਫ਼ਿਕੇਸ਼ਨ), attest (ਅਟੈਸਟੇਸ਼ਨ) are all locked, and *authenticity* is a sixth distinct property — "this artifact is genuinely what it claims to be". ਅਸਲੀਅਤ (from ਅਸਲ, "genuine/original") states that plainly, is Gurmat-neutral, and collides with none of the five. Unlike Q48 the loan was not needed here, because a free native word exists. **What could flip it:** Appendix A may define the term; C10 (MCP) uses the concept heavily for tool responses and must reuse this pick rather than reach for ਪ੍ਰਮਾਣਿਕਤਾ. |
| **Reviewer notes** | |

---

## Q100 — protocol downgrade (conformance note on the C10 transport vocabulary)

| Field | Value |
|---|---|
| **EN term** | MCP client minimum protocol-version enforcement, "downgrade defense" (Appendix B AD.11; source C10.3.4) |
| **Current pick** | ਡਾਊਨਗ੍ਰੇਡ (L) — everything else in this row conforms to Q90 and Q92 rather than competing with them |
| **Alternatives** | ਦਰਜਾ-ਘਟਾਈ (T, "rank reduction" — reads as demotion of a person); ਹੇਠਲੇ ਵਰਜ਼ਨ ਵੱਲ ਧੱਕਣਾ (descriptive phrase — cannot serve as the attributive modifier the row needs); ਪਿਛਾਂਹ-ਪਰਤਾਅ (coinage, unattested) |
| **Type** | L |
| **Reasoning** | **Written after a numbering collision, and recorded as such.** This appendix was translated in parallel with C10 and independently reached the same picks for *transport* (ਟ੍ਰਾਂਸਪੋਰਟ), for the retained `stdio` / `streamable HTTP` / `Origin` / `Host`, and for the retained `DNS rebinding`. C10 owns that vocabulary and logged it first at **Q90** and **Q92**; this appendix conforms to both and does not restate them. The single term C10 did not cover is *downgrade*, which is genuinely open here: it names a forced protocol-version rollback, and the loan is what a practitioner meets in TLS and OAuth literature, consistent with the corpus's treatment of protocol-layer vocabulary. **What could flip it:** C10 remains the deciding chapter — if it later nativises *downgrade*, this row moves with it. |
| **Reviewer notes** | |

---

## Q101 — MCP token vocabulary (conformance note; only *pass-through* is new)

| Field | Value |
|---|---|
| **EN term** | access token, token claims, sender-constrained tokens, and **pass-through of client access tokens** (Appendix B AD.1; source C10.2.1–C10.2.7, C10.3.5) |
| **Current pick** | Conforms to C10: ਪਹੁੰਚ ਟੋਕਨ, ਦਾਅਵੇ (claims), ਉਦੇਸ਼ਿਤ ਪ੍ਰਾਪਤਕਰਤਾ (audience), ਭੇਜਣ ਵਾਲੇ ਨਾਲ ਬੰਨ੍ਹੇ ਹੋਏ (sender-constrained). New here: *pass-through* → **ਅੱਗੇ ਲੰਘਾਉਣਾ** |
| **Alternatives** | For *pass-through*: ਪਾਸ-ਥਰੂ (L); ਸਿੱਧਾ ਅੱਗੇ ਭੇਜਣਾ (T, "forwarding directly" — ਭੇਜਣਾ is now load-bearing in ਭੇਜਣ ਵਾਲੇ ਨਾਲ ਬੰਨ੍ਹੇ ਹੋਏ two rows above, and reusing it would suggest the two rows describe one mechanism) |
| **Type** | T |
| **Reasoning** | **Corrective entry.** This appendix's first draft independently coined ਭੇਜਣਹਾਰ-ਸੀਮਿਤ for *sender-constrained* and retained `claim` / `audience` in Latin — both of which contradict C10's **Q89** and **Q91**, logged in the same session by the C10 translation. Because C10 is the owning chapter, this file was corrected to C10's forms rather than the reverse (`0x91`, AD.1 rows for C10.2.2 and C10.3.5), and the collision is recorded here rather than left for a reviewer to find. Only *pass-through* was genuinely uncovered: ਅੱਗੇ ਲੰਘਾਉਣਾ ("to let through onward") states the mechanism the control forbids — relaying a client's token unchanged to a downstream API — and is deliberately kept distinct from ਅੱਗੇ ਸੰਚਾਰਿਤ ਕਰਨਾ, which C09 9.5.2 uses for the *approved* propagation of a scope-limited delegation token. Blurring the two would make a prohibition and an obligation look like the same act. **What could flip it:** C10 owns the final call on all MCP token vocabulary, including this one. |
| **Reviewer notes** | |

---

## Q102 — replay (conformance note)

| Field | Value |
|---|---|
| **EN term** | replay defense, replay protection (Appendix B AD.5 and its common-pitfalls note; source C10.4.6) |
| **Current pick** | `replay` retained in Latin, glossed **(ਦੁਹਰਾਓ)** on first use — conforming to C10's entry, not competing with it; ਨੌਂਸ (nonce) carried over unchanged from C09 9.2.8 |
| **Alternatives** | ਰੀਪਲੇ (L, transliterated — **this appendix's first draft used it, and it is exactly the form C10's entry rejects** for breaking the search link to the named attack class) |
| **Type** | R (+ T gloss) |
| **Reasoning** | **Corrective entry.** Drafted in parallel with C10, this appendix transliterated *replay* as ਰੀਪਲੇ before C10's decision existed; on discovering C10's **Q92**, both occurrences in `0x91` (the AD.5 control row for C10.4.6 and the AD.5 common-pitfalls note) were normalised to the retained Latin form with C10's ਦੁਹਰਾਓ gloss. ਰੀਪਲੇ now appears nowhere in the corpus. The substantive contribution of this entry is the **nonce hand-off**: C09 9.2.8 fixed ਨੌਂਸ in an approval-binding context, and this appendix is the first place the same term is used for MCP tool-response freshness. Same word, same reason — it is a single-use value, not an identifier — so no second rendering was coined. **What could flip it:** C10 owns *replay*; if it moves, this file follows. |
| **Reviewer notes** | |

---

## Q103 — lateral movement

| Field | Value |
|---|---|
| **EN term** | lateral movement ("contain failures and prevent lateral movement", AD.10 objective) |
| **Current pick** | `lateral movement` retained in Latin, glossed ਪਾਸੇ-ਵੱਲ ਫੈਲਾਅ ("spread sideways") |
| **Alternatives** | ਪਾਸੇ-ਵੱਲ ਫੈਲਾਅ alone (T — readable, but loses the searchable technique name); ਪਾਸਲੀ ਹਿਲਜੁਲ (T, "sideways movement" — reads as physical motion); ਲੈਟਰਲ ਮੂਵਮੈਂਟ (L — transliteration adds nothing over retention) |
| **Type** | R (+ T gloss) |
| **Reasoning** | Lateral movement is a MITRE ATT&CK tactic name, which puts it squarely in the `GLOSSARY.md` retained-technique family alongside Padding Oracle, TOCTOU, and prompt injection — an implementer reading isolation guidance needs to be able to match it to the threat-intel literature. The gloss is descriptive rather than a competing term, following the pattern set for homoglyph (Q75) and many-shot jailbreaking (Q32). **What could flip it:** if C12 introduces the term in an incident-response context, both places must use one treatment. |
| **Reviewer notes** | |

---

## Q104 — fail-closed / fail-open

| Field | Value |
|---|---|
| **EN term** | fail-closed blocking (AD.19 control row); defaulting to fail-open (AD.19 common pitfalls) |
| **Current pick** | ਨਾਕਾਮੀ-'ਤੇ-ਬੰਦ (fail-closed) / ਨਾਕਾਮੀ-'ਤੇ-ਖੁੱਲ੍ਹਾ (fail-open), each glossed in English on first use |
| **Alternatives** | ਫ਼ੇਲ੍ਹ-ਕਲੋਜ਼ਡ / ਫ਼ੇਲ੍ਹ-ਓਪਨ (L, full transliteration); ਸੁਰੱਖਿਅਤ ਨਾਕਾਮੀ (T, "safe failure" — **rejected**, it names the desirable outcome rather than the mechanism, and would make the *fail-open* pitfall untranslatable as its opposite); ਬੰਦ ਹੋ ਕੇ ਨਾਕਾਮ ਹੋਣਾ (verb phrase — cannot serve as the attributive modifier the requirement row needs) |
| **Type** | T (with the apostrophe-clitic `'ਤੇ`, explicitly permitted by `TRANSLATION-RULES.md` §2.4) |
| **Reasoning** | The pair is the point: AD.19 states the control as fail-closed and names fail-open as the corresponding pitfall two paragraphs later, so whatever renders one must invert cleanly for the other. The literal compound does that, where both the loan and the "safe failure" paraphrase break the symmetry. ਨਾਕਾਮੀ ("failure") is kept distinct from ਗਲਤੀ (*error*, Q89) and ਖ਼ਰਾਬੀ (*malfunction*): the referent here is a control that did not complete, not a fault. **What could flip it:** a reviewer preference for the transliterated pair on the grounds that fail-open/fail-closed are fixed industry terms; they would then have to move together. |
| **Reviewer notes** | |

---

## Q105 — guardrail

| Field | Value |
|---|---|
| **EN term** | guardrail — "the adversarial-AI threat scenarios that justify each guardrail" (Appendix C, AC.1 intro) |
| **Current pick** | ਗਾਰਡਰੇਲ |
| **Alternatives** | ਸੁਰੱਖਿਆ-ਬੰਨ੍ਹ (T, "safety embankment" — coined, and swaps one physical metaphor for another); ਰੋਕ-ਬਾੜ (T, "barrier fence" — suggests a hard block, but a guardrail is a steering constraint that still allows the action space); ਮਰਿਆਦਾ — **absolutely rejected**, it names the Sikh code of conduct and using it for a machine constraint would be a Gurmat-safety violation of exactly the class `CLAUDE.md` §AI/ML-specific risk warns about; ਹੱਦਬੰਦੀ — rejected, ਹੱਦ is lint-forbidden corpus-wide (Q69 pins *threshold* to ਥ੍ਰੈਸ਼ਹੋਲਡ and the lint blocks the bare noun) |
| **Type** | L |
| **Reasoning** | `CLAUDE.md` names "guardrail" on the short list of AI terms carrying spiritually-loaded metaphorical baggage, so the first job was to exclude the near-synonym that would fit superficially — ਮਰਿਆਦਾ — rather than to find the prettiest native word. Once that is off the table, the remaining native candidates are coinages that each shift the meaning: a guardrail in AI-tooling usage is a *policy-layer constraint that shapes permitted behaviour*, not a fence and not an embankment. The transliterated loan is neutral, carries no devotional colour, and is already how the term circulates in Panjabi-language technical writing. Glossed **ਗਾਰਡਰੇਲ (guardrail)** on first use in AC.1. **What could flip it:** a Sangat-approved native coinage that is demonstrably free of both the devotional register and the hard-block reading. |
| **Reviewer notes** | |

---

## Q106 — pull request (PR) / merge / branch protection

| Field | Value |
|---|---|
| **EN term** | pull request, PR, merge, merge queue, branch protection (Appendix C, chapter-wide — AC.4.2, AC.4.3, AC.8.1, AC.8.3, AC.11.5, AC.12.5, AC.13.1) |
| **Current pick** | ਪੁੱਲ ਰਿਕੁਐਸਟ — glossed **ਪੁੱਲ ਰਿਕੁਐਸਟ (pull request)** on first use, then the retained acronym **PR** everywhere else; ਮਰਜ / ਮਰਜ ਕਤਾਰ; ਬ੍ਰਾਂਚ ਸੁਰੱਖਿਆ |
| **Alternatives** | ਖਿੱਚਣ ਦੀ ਬੇਨਤੀ (T, literal "request to pull" — unattested and reads as a physical pull); ਵਿਲੀਨ ਕਰਨਾ / ਰਲੇਵਾਂ for merge (T — ਰਲੇਵਾਂ is political-merger vocabulary; ਵਿਲੀਨ carries a dissolution sense); ਸ਼ਾਖਾ ਸੁਰੱਖਿਆ for branch protection (T — ਸ਼ਾਖਾ reads botanical/organisational, not VCS) |
| **Type** | L (PR = R) |
| **Reasoning** | These are platform primitives of a specific hosting model (GitHub/GitLab), not general concepts: a pull request is a named object with an identity, a state machine, and an API, and AC.12.1 depends on the reader mapping it to the literal `pull_request` trigger name in the very same requirement. A descriptive native rendering would break that mapping. The acronym **PR** is load-bearing in practitioner usage and appears in compounds throughout the appendix (fork-PR, PR-supplied content, PR-comment bots), so it is retained per the `GLOSSARY.md` always-retained rule for acronyms, with the spelled-out loan glossed once at AC.4.2 so the reader can connect them. **What could flip it:** a reviewer preference for a fully native VCS vocabulary — it would have to move pull request, merge, branch, and fork (Q107) together, never one at a time. |
| **Reviewer notes** | |

---

## Q107 — fork (fork PR, forked repository)

| Field | Value |
|---|---|
| **EN term** | fork, fork PR, fork-supplied diffs, coordinated fork waves (Appendix C — AC.1.3, AC.3.3, AC.11.7, AC.12.1, AC.12.3, AC.13.1, AC.13.5) |
| **Current pick** | ਫ਼ੋਰਕ (nukta per Q86) |
| **Alternatives** | ਸ਼ਾਖ਼ਾ (T, "branch" — **rejected**, it collides head-on with VCS *branch*, which Q106 renders ਬ੍ਰਾਂਚ, and the appendix uses both words in the same requirement); ਵੰਡ (T, "split"); ਨਕਲ (T, "copy" — loses the "independent line of development with its own permissions" sense that the whole untrusted-contribution threat model rests on) |
| **Type** | L |
| **Reasoning** | The security meaning of *fork* in this appendix is precisely a trust boundary: a fork PR is untrusted because it originates outside the repository's permission domain (AC.12.1, AC.12.3). ਨਕਲ and ਵੰਡ both describe the mechanical act and say nothing about that boundary, and ਸ਼ਾਖ਼ਾ would make the fork/branch distinction — which AC.8.3 and AC.11.2 rely on — invisible. The loan takes the nukta under the Q86 /f/ rule, consistent with ਫ਼ਾਈਲ, ਫ਼ਿਲਟਰ, ਫ਼ੀਚਰ. |
| **Reviewer notes** | |

---

## Q108 — red team / red-teaming; exercise (drill)

| Field | Value |
|---|---|
| **EN term** | red-teaming the AI tooling, scheduled red-team exercises, tabletop or live-fire exercises (Appendix C, AC.6 intro, AC.6.3, AC.14.5) |
| **Current pick** | ਰੈੱਡ-ਟੀਮ / ਰੈੱਡ-ਟੀਮਿੰਗ; *exercise* = **ਮਸ਼ਕ** |
| **Alternatives** | ਲਾਲ ਟੀਮ (T, literal "red team" — translates a colour-code that only means anything untranslated); ਹਮਲਾਵਰ ਟੀਮ (T, "attacker team" — descriptive but loses the named-discipline sense); for *exercise*: ਅਭਿਆਸ — **rejected** on the same grounds Q37 rejected it for *training* (ਨਾਮ ਅਭਿਆਸ, devotional-practice register); ਕਸਰਤ (T — physical exercise) |
| **Type** | L (red team) + T (ਮਸ਼ਕ) |
| **Reasoning** | Red teaming is a named security discipline whose colour term is a convention, not a description; ਲਾਲ ਟੀਮ would translate the convention away and leave a Panjabi reader with an unexplained colour. The second half of this entry matters more: the appendix needs "exercise" three times, and the obvious dictionary word ਅਭਿਆਸ is exactly the term Q37 excluded on Gurmat grounds and flagged as unresolved residue elsewhere in the corpus. **ਮਸ਼ਕ** ("drill, rehearsal") is ordinary Perso-Panjabi, carries the repeat-until-ready sense a tabletop or live-fire exercise has, and is free of devotional colour — so this file deliberately does not add to the ਅਭਿਆਸ residue Q37 asks reviewers to settle. **What could flip it:** a reviewer ruling on the Q37 ਅਭਿਆਸ question; if ਅਭਿਆਸ is cleared for professional-practice senses, ਮਸ਼ਕ still stays correct for *drill*. |
| **Reviewer notes** | |

---

## Q109 — separation of duties / dual control

| Field | Value |
|---|---|
| **EN term** | separation of duties (Appendix C, AC.4.1, AC.8 intro, AC.8.4); dual control (AC.7.4) |
| **Current pick** | ਕਰਤੱਵਾਂ ਦੀ ਵੰਡ (separation of duties) / ਦੋਹਰਾ ਨਿਯੰਤਰਣ (dual control) |
| **Alternatives** | ਜ਼ਿੰਮੇਵਾਰੀਆਂ ਦੀ ਵੰਡ (T, "division of responsibilities" — reads as ordinary work allocation, not a security control); ਫ਼ਰਜ਼ਾਂ ਦਾ ਵਖਰੇਵਾਂ (T — ਫ਼ਰਜ਼ carries a moral-obligation register); ਦੋ-ਵਿਅਕਤੀ ਨਿਯੰਤਰਣ (T, "two-person control" — accurate for the common case but the source separately says *two-person review* at AC.4.4, and collapsing them would lose a distinction) |
| **Type** | T |
| **Reasoning** | ISO/IEC 27001:2022 A.5.3 (cited by AC.4.1 and AC.8.4) treats separation of duties as a named control, so the rendering has to read as a control name rather than as a management practice — ਕਰਤੱਵ ("duty, assigned task") is the neutral administrative noun that does that, where ਜ਼ਿੰਮੇਵਾਰੀ drifts to "responsibility" in the ordinary sense. *Dual control* is kept visibly separate (ਦੋਹਰਾ ਨਿਯੰਤਰਣ) because AC.7.4 requires dual control **and** a security-team review as two distinct obligations. ਨਿਯੰਤਰਣ is the corpus-wide rendering for *control* per Q80; the loan ਕੰਟਰੋਲ is lint-blocked outside ਪਹੁੰਚ ਕੰਟਰੋਲ. Glossed in English on first use. |
| **Reviewer notes** | |

---

## Q110 — workflow (CI/CD workflow file)

| Field | Value |
|---|---|
| **EN term** | workflow — both the written process sense (AC.1.1, AC.1.2) and the CI/CD artifact sense (`.github/workflows/*`, workflow files, workflow runs, workflow triggers — AC.7.1, AC.7.4, AC.12.1–AC.12.8) |
| **Current pick** | ਵਰਕਫ਼ਲੋ (both senses) |
| **Alternatives** | ਕਾਰਜ-ਪ੍ਰਵਾਹ (T, "work flow" — readable for the process sense, actively wrong for the file sense: a `.gitlab-ci.yml` is not a "flow"); ਕਾਰਜ-ਵਿਧੀ (T, "procedure" — collides with ਵਿਧੀ already used for *method*); mixing the two, native for the process sense and loan for the file sense |
| **Type** | L |
| **Reasoning** | The mixed option was considered first and rejected: AC.1.2 ("the workflow covers every SSDLC phase") and AC.12.5 ("workflow definition files") are the same English word doing related work, and AC.12.6 audits *workflow runs* of the file kind under a policy written as a workflow of the process kind. Two Panjabi words would suggest two unrelated concepts. The loan carries both senses the way the English does, and matches the corpus's treatment of pipeline/infrastructure nouns (ਪਾਈਪਲਾਈਨ, ਪ੍ਰੌਕਸੀ, ਇਨਵੈਂਟਰੀ). Takes the nukta per Q86. Glossed **ਵਰਕਫ਼ਲੋ (workflow)** on first use at AC.1.1. **Boundary to preserve:** ਪਾਈਪਲਾਈਨ stays reserved for *pipeline*. **Cross-file audit 2026-08-27 — earlier claim corrected:** this entry previously said "the appendix uses both in one sentence at AC.7.1 and AC.12.6." Only AC.12.6 does (`0x92`:432, ਪਾਈਪਲਾਈਨ ਆਡਿਟ ਲੌਗ … ਵਰਕਫ਼ਲੋ ਰਨ). AC.7.1 (`0x92`:238/246) contains *workflow* but no *pipeline* at all, in either language — the intended neighbour was almost certainly **AC.7.4** (`0x92`:249), which does carry both. The three rows where the two words share one requirement are AC.7.4, AC.12.6, and AC.14.1 (`0x92`:508); those are the sites where the boundary is load-bearing. |
| **Reviewer notes** | |

---

## Q111 — runner (CI runner, self-hosted runner)

| Field | Value |
|---|---|
| **EN term** | self-hosted runner labels, CI runners, persistent runners, AI-runner pools (AC.7.4, AC.12.2, AC.12.4, AC.12.6) |
| **Current pick** | ਰਨਰ |
| **Alternatives** | ਚਾਲਕ (T, "operator/driver" — names a person or a driving component, not an execution host); ਐਗਜ਼ੀਕਿਊਟਰ (L, "executor" — plausible but not the term any CI platform uses, so it is not translatable back); ਦੌੜਾਕ (T, literal "runner" as in athlete — misleading) |
| **Type** | L |
| **Reasoning** | A runner is a named CI-platform component — a registered, labelled execution host — and AC.7.4 requires verifying *runner labels* and AC.12.6 *runner registration*, both of which are literal platform features the reader must find in vendor documentation. ਦੌੜਾਕ is the clearest failure: it would make AC.12.4's "persistent or long-lived runners" read as a statement about athletes. Consistent with the loan treatment of ਵਰਕਲੋਡ and ਐਕਸਲੇਰੇਟਰ at Q51 for the same reason. |
| **Reviewer notes** | |

---

## Q112 — tamper-evident (append-only, WORM, immutable log store)

| Field | Value |
|---|---|
| **EN term** | tamper-evident storage (append-only, WORM, or an immutable log store) (AC.5.3, AC.11.6) |
| **Current pick** | ਛੇੜਛਾੜ-ਪ੍ਰਗਟ (tamper-evident); ਸਿਰਫ਼-ਜੋੜਨਯੋਗ (append-only); **WORM** retained; ਅਪਰਿਵਰਤਨਸ਼ੀਲ (immutable) |
| **Alternatives** | ਛੇੜਛਾੜ-ਰੋਧਕ (T, "tamper-resistant" — **rejected**, it names a different property: resistant means the change is prevented, evident means the change is detectable afterwards, and the whole point of an append-only forensic log is the second one); ਛੇੜਛਾੜ-ਸਬੂਤ (T — reads as "proof of tampering", ambiguous); ਟੈਂਪਰ-ਐਵੀਡੈਂਟ (L) |
| **Type** | T (WORM = R) |
| **Reasoning** | ਛੇੜਛਾੜ for *tampering* is locked in `GLOSSARY.md`, so only the modifier was open, and the modifier is where the security meaning sits. Rendering *evident* as ਪ੍ਰਗਟ ("manifest, apparent") keeps the detectability claim that AC.5.3 makes about forensic storage, and keeps it distinct from the prevention claim made elsewhere (AC.11.2's integrity-check-at-load). ਅਪਰਿਵਰਤਨਸ਼ੀਲ for *immutable* carries C12 precedent (`0x10-C12-Monitoring-and-Logging.md` 12.5.3). WORM is an acronym and stays Latin per the always-retained rule. **Found by the full-corpus audit 2026-08-27:** C08 8.1.2 (`0x10-C08`:33) was the corpus's one holdout — it paraphrased *immutable* as ਬਦਲੇ ਨਹੀਂ ਜਾ ਸਕਦੇ ("cannot be changed"), while `0x91-Appendix-B`:572 indexes that same requirement C8.1.2 as ਅਪਰਿਵਰਤਨਸ਼ੀਲਤਾ. The paraphrase is not wrong in isolation; it is wrong beside its own index entry, and it hides the term from a reader searching the corpus for it. Normalised to the adjective, matching C12 12.5.3, AC.5.3, and `0x03`:145. No lint rule was added: a forbidden *paraphrase* cannot be pattern-matched without false positives on ordinary prose — this one is caught by the requirement-id join against Appendix B instead. |
| **Reviewer notes** | |

---

## Q113 — policy-as-code

| Field | Value |
|---|---|
| **EN term** | policy-as-code enforcement (OPA, Conftest, Checkov, tfsec, KICS, kube-linter) (AC.7.3) |
| **Current pick** | ਕੋਡ-ਵਜੋਂ-ਨੀਤੀ — glossed **ਕੋਡ-ਵਜੋਂ-ਨੀਤੀ (policy-as-code)** on first use; tool names stay R |
| **Alternatives** | retain `policy-as-code` fully in Latin (R); ਪਾਲਿਸੀ-ਐਜ਼-ਕੋਡ (L, full transliteration); ਨੀਤੀ ਦਾ ਕੋਡੀਕਰਨ (T, "codification of policy" — that is a legal-drafting phrase, and it loses the "executable artifact evaluated in a pipeline" meaning) |
| **Type** | T (with English gloss) |
| **Reasoning** | Both halves already have settled Panjabi renderings — ਨੀਤੀ for *policy* (corpus precedent, C05/C09) and ਕੋਡ as the ordinary loan — so this is a transparent compound rather than a branded product name, which is the T-vs-R test applied at Q24 (policy decision point). The English gloss is kept because AC.7.3 cites the named tools that implement it and a reader must be able to match the phrase to their documentation. Word order follows the Panjabi head-final pattern (ਕੋਡ-ਵਜੋਂ ਸਭ ਤੋਂ ਪਹਿਲਾਂ, ਨੀਤੀ ਸਿਰ) rather than transliterating the English order. **What could flip it:** if a later document needs the paired term *infrastructure-as-code* translated too — this file keeps `infrastructure-as-code` Latin at AC.7.1 because it appears there as the label of an artifact class alongside Terraform and Pulumi, and the two decisions should be aligned by a reviewer rather than left split. |
| **Reviewer notes** | |

---

## Q114 — containment (compromise containment) / incident-response playbook

| Field | Value |
|---|---|
| **EN term** | Compromise Containment (AC.14 title), "contain the damage" (AC.14 intro), automated containment (AC.13.5); incident-response playbook (AC.14.1) |
| **Current pick** | ਘੇਰਾਬੰਦੀ (containment) / ਘਟਨਾ-ਜਵਾਬ ਪਲੇਬੁੱਕ (incident-response playbook) |
| **Alternatives** | ਰੋਕਥਾਮ (T — **rejected**, it means *prevention*, and AC.13.5/AC.14 are explicitly the post-compromise phase; using it would state the opposite of the requirement); ਕਾਬੂ (T, "control/restraint" — collides conceptually with ਨਿਯੰਤਰਣ, the corpus word for *control*); ਸੀਮਤਬੰਦੀ (coinage, unattested); for playbook: ਕਾਰਜ-ਪੁਸਤਿਕਾ (T, "handbook" — loses the rehearsed-response sense) |
| **Type** | T (ਘੇਰਾਬੰਦੀ) + L (ਪਲੇਬੁੱਕ) |
| **Reasoning** | The rejection matters more than the pick here: ਰੋਕਥਾਮ is the word a Panjabi reader would most expect for "containment" from public-health usage, and it is wrong in a security standard, where containment begins *after* prevention has failed. ਘੇਰਾਬੰਦੀ ("cordoning off, encircling") carries the limit-the-spread meaning that AC.14's stated goal — contain the damage, shorten the recovery — requires, and keeps ਰੋਕਥਾਮ free should a later chapter need *prevention*. ਘਟਨਾ ਜਵਾਬ for *incident response* carries C12 precedent (`0x10-C12-Monitoring-and-Logging.md`:22). Glossed in English on first use. **What could flip it:** ਘੇਰਾਬੰਦੀ has a siege register that a reviewer may find over-dramatic; a Sangat-preferred neutral coinage would be a straight swap since the term appears only three times. |
| **Reviewer notes** | |

---

## Q115 — stylometric / entropy-based heuristics

| Field | Value |
|---|---|
| **EN term** | structural AST profiling and stylometric or entropy-based heuristics (AC.13.6) |
| **Current pick** | ਸਟਾਈਲੋਮੈਟ੍ਰਿਕ (stylometric) / ਐਂਟਰੌਪੀ-ਆਧਾਰਿਤ / ਅਨੁਮਾਨ-ਨੇਮ (heuristics); **AST** retained |
| **Alternatives** | ਸ਼ੈਲੀ-ਮਾਪਕ (T, "style-measuring" — a readable coinage, but stylometry is a named forensic-linguistics discipline and the coinage is not translatable back to the literature AC.13.6 depends on); ਅਵਿਵਸਥਾ for entropy (T, "disorder" — the thermodynamic reading, not the information-theoretic one the requirement means); ਹਿਊਰਿਸਟਿਕ (L) for heuristics |
| **Type** | L (AST = R) |
| **Reasoning** | ਅਵਿਵਸਥਾ is the clear failure: AC.13.6 means Shannon entropy over token distributions, and a thermodynamic-disorder word would mislead an implementer about what to measure. Stylometry keeps its loan for the same reason Q52 loans *federated learning* — it names a discipline, not a description. *Heuristics* takes the native ਅਨੁਮਾਨ-ਨੇਮ ("rule of estimate") rather than a loan because it is a general methodological word here, not a product name; note ਅਨੁਮਾਨ alone is unusable (Q18 records that the sibling corpus uses ਅਨੁਮਾਨਿਤ for *expected*), hence the compound. The **-ਆਧਾਰਿਤ** suffix follows the pinned Q71 form. **What could flip it:** if C11 (Adversarial Robustness) needs *entropy* as a standalone measured quantity, a loan/native decision should be made once for both. |
| **Reviewer notes** | |

---

## Q116 — typosquatted / registry-confusable dependency names

| Field | Value |
|---|---|
| **EN term** | registry-confusable or typosquatted dependency names (AC.13.3) |
| **Current pick** | `typosquatted` retained in Latin; *registry-confusable* rendered ਰਜਿਸਟਰੀ ਵਿੱਚ ਭੁਲੇਖਾ ਪਾਉਣ ਵਾਲੇ |
| **Alternatives** | ਟਾਈਪੋਸਕੁਐਟ ਕੀਤੇ (L, transliterated); ਨਾਂ-ਨਕਲੀ ਪੈਕੇਜ (T, "name-counterfeit packages"); ਸ਼ਬਦ-ਜੋੜ ਹਮਲਾ (T, "spelling attack" — vague) |
| **Type** | R (typosquatting) + T (confusable) |
| **Reasoning** | `GLOSSARY.md` retains named attacks and techniques verbatim, and typosquatting is a named supply-chain technique catalogued as such by OWASP CI/CD Top 10 CICD-SEC-03, which AC.13.3 cites — a practitioner searching for it needs the English string. *Registry-confusable*, by contrast, is descriptive prose in the source rather than a technique name, so it is translated, following the same descriptive-vs-branded split applied at Q34 (representation smuggling). ਭੁਲੇਖਾ ("confusion, mistaken impression") is ordinary Panjabi and carries the deceive-the-reader sense the requirement is about. **What could flip it:** upstream AISVS promoting "registry confusion" to a named class, in which case it moves to R alongside typosquatting. |
| **Reviewer notes** | |

---

## Q117 — shadow mode

| Field | Value |
|---|---|
| **EN term** | zero-privilege, read-only shadow mode (AC.11.7) |
| **Current pick** | ਸ਼ੈਡੋ ਮੋਡ — glossed **ਸ਼ੈਡੋ ਮੋਡ (shadow mode)** on first use |
| **Alternatives** | ਪਰਛਾਵਾਂ ਮੋਡ (T, native "shadow" — reads as a literal shadow and, worse, ਪਰਛਾਵਾਂ carries an ominous/inauspicious shading in ordinary Panjabi usage that the neutral technical term does not have); ਨਿਰੀਖਣ ਮੋਡ (T, "observation mode" — describes the effect but loses the named deployment pattern); ਚੁੱਪ ਮੋਡ (T, "silent mode") |
| **Type** | L |
| **Reasoning** | Shadow mode is a named deployment pattern (run the component, record what it would have done, let it act on nothing) with a fixed industry meaning, and AC.11.7 depends on that precise reading — the bot still runs and still evaluates, it merely holds no privilege. ਨਿਰੀਖਣ ਮੋਡ would suggest a monitoring component rather than the real component running powerless. ਪਰਛਾਵਾਂ was rejected on register as much as on precision. Consistent with the loan treatment of named operational primitives (ਸੈਂਡਬਾਕਸ, Q47). |
| **Reviewer notes** | |

---

## Q118 — baseline

| Field | Value |
|---|---|
| **EN term** | baseline — "the range is baseline to advanced" (Objective), human-only baseline (AC.1.4), signed AI-attributed baselines (AC.7.5), the prior baseline (AC.6.4), those baselines (AC.12 intro) |
| **Current pick** | ਬੇਸਲਾਈਨ — glossed **ਬੇਸਲਾਈਨ (baseline)** on first use |
| **Alternatives** | ਆਧਾਰ-ਰੇਖਾ (T, "base line" — attested in statistics, but ਆਧਾਰ is already load-bearing corpus-wide as the pinned **-ਆਧਾਰਿਤ** suffix for *-based* (Q71), and the two would sit adjacent in AC.13.6 "ਐਂਟਰੌਪੀ-ਆਧਾਰਿਤ … ਬੇਸਲਾਈਨ"); ਮੁੱਢਲਾ ਪੱਧਰ (T, "initial level" — works for the Objective's range sense, wrong for AC.7.5 where a baseline is a signed artifact you compare against); ਸ਼ੁਰੂਆਤੀ ਮਾਪ (periphrastic) |
| **Type** | L |
| **Reasoning** | The appendix uses *baseline* in three distinct ways — a maturity floor (Objective), a comparison measurement (AC.1.4, AC.6.4), and a signed reference artifact (AC.7.5) — and only a single word that carries all three keeps the requirements internally consistent. ਮੁੱਢਲਾ ਪੱਧਰ covers only the first. The ਆਧਾਰ-ਰੇਖਾ collision with the pinned *-based* suffix is the deciding factor against the most defensible native option: two adjacent ਆਧਾਰ- forms carrying unrelated meanings in one requirement is exactly the silent-collision failure Q80 and Q37 were opened to prevent. **What could flip it:** a reviewer decision to unpin ਆਧਾਰਿਤ, which would free ਆਧਾਰ-ਰੇਖਾ. |
| **Reviewer notes** | |

---

## Q119 — bot (AI review bot, assistant bot, IDE copilot)

| Field | Value |
|---|---|
| **EN term** | AI code-review bots, PR-comment bots, assistant bots, IDE copilots (AC.11 title and intro, AC.11.1–AC.11.8, AC.12.3, AC.13.2, AC.14.5) |
| **Current pick** | ਬੋਟ / ਸਹਾਇਕ ਬੋਟ / IDE ਕੋਪਾਇਲਟ |
| **Alternatives** | ਰੋਬੋਟ (L — wrong referent, suggests a physical machine); ਸਵੈਚਾਲਿਤ ਏਜੰਟ (T/L, "automated agent" — **rejected**, it collapses into ਏਜੰਟ, which Q17 and Q81 reserve for the agent sense, and AC.11.5 needs bots and agents distinguishable); ਸਹਾਇਕ for copilot (T, "assistant" — already used for *assistant*, so reusing it would merge two source terms) |
| **Type** | L |
| **Reasoning** | The appendix keeps *bot*, *assistant*, *agent*, and *copilot* as four distinct actors in one family — AC.11.5 restricts what a bot may do, AC.8 restricts what an agent may do, and AC.11 intro lists assistants and copilots as separate reachable surfaces — so each needs its own Panjabi form or the family's structure collapses. ਬੋਟ is the neutral loan already current in Panjabi technical prose; ਸਹਾਇਕ (native, "assistant") carries the *assistant* sense; ਏਜੰਟ stays reserved per Q17; *copilot* keeps its loan because it names a product class. **What could flip it:** nothing likely; logged so C09/C10 do not re-derive *bot* differently. |
| **Reviewer notes** | |

---

## Q120 — explainability

| Field | Value |
|---|---|
| **EN term** | Explainability & Traceability of Code Suggestions (AC.5 title); explainability reports (AC.5.3) |
| **Current pick** | ਵਿਆਖਿਆਯੋਗਤਾ |
| **Alternatives** | ਸਮਝਾਉਣਯੋਗਤਾ (T, "able to be explained to someone" — puts the burden on a human explainer rather than naming a property of the system); ਪਾਰਦਰਸ਼ਤਾ (T, "transparency" — **rejected**, it is a separate governance concept and `0x03-Using-AISVS.md`:147 already uses it for *transparency reports*); ਐਕਸਪਲੇਨੇਬਿਲਟੀ (L) |
| **Type** | T |
| **Reasoning** | ਵਿਆਖਿਆ ("exposition, interpretation") is standard formal Panjabi and the -ਯੋਗਤਾ suffix builds the property noun regularly, matching how the corpus already forms ਟਰੇਸਯੋਗਤਾ (traceability, Q38) — which is the very word paired with it in this chapter title, so the two read as a matched pair. The ਪਾਰਦਰਸ਼ਤਾ rejection is the load-bearing one: NIST AI RMF and ISO/IEC 42001, both cited by AC.5, treat explainability and transparency as separate properties, and the corpus has already spent ਪਾਰਦਰਸ਼ਤਾ on the second. Note ਵਿਆਖਿਆ carries a scriptural-exegesis association in Gurmat contexts (as in Darpan-style commentary); it is retained here because the association is with scholarly interpretation generally, not with devotional practice, and no neutral alternative survives the ਪਾਰਦਰਸ਼ਤਾ collision — flagged so a reviewer can rule on it explicitly rather than inherit it silently. |
| **Reviewer notes** | |

---

## Q121 — appendix (ਅੰਤਿਕਾ)

| Field | Value |
|---|---|
| **EN term** | Appendix — "Appendix C: AI-Assisted Secure Coding"; also Appendix A (Glossary) and Appendix B (AI Security Controls Inventory) |
| **Current pick** | ਅੰਤਿਕਾ — the letter stays Latin: **ਅੰਤਿਕਾ C** |
| **Alternatives** | ਅਪੈਂਡਿਕਸ (L); ਵਾਧਾ (T, "addition" — too vague); ਸਹਾਇਕ ਭਾਗ (T, "supplementary section" — periphrastic and would not read as a document division) |
| **Type** | T (division letter R) |
| **Reasoning** | ਅੰਤਿਕਾ is the settled Panjabi term for a document appendix in academic and government publishing, so the loan buys nothing. The division letter stays Latin for the same reason requirement IDs do (`TRANSLATION-RULES.md` §2.3): "Appendix C" is a cross-reference target that must match the English standard exactly, and `0x03-Using-AISVS.md` refers to these appendices by letter. Logged **specifically as a hand-off**: `0x90-Appendix-A_Glossary.md` and `0x91-Appendix-B_AI_Security_Controls_Inventory.md` are not yet translated, and they must use this same form rather than re-deriving one. |
| **Reviewer notes** | |

---

## Q122 — threat scenario

| Field | Value |
|---|---|
| **EN term** | adversarial-AI threat scenarios (AC.1 intro, AC.1.3); "the scenario worth defending against" (AC.13 intro); "the scenarios include…" (AC.14.5) |
| **Current pick** | ਖ਼ਤਰਾ ਦ੍ਰਿਸ਼ |
| **Alternatives** | ਖ਼ਤਰਾ ਸਥਿਤੀ (T — **rejected**, ਸਥਿਤੀ is locked in `GLOSSARY.md` for *posture/state*, the Q5 Gurmat-corrected term, and must not take a second sense); ਖ਼ਤਰਾ ਹਾਲਾਤ (T, "circumstances" — plural-only in ordinary use and awkward as a countable item); ਸਿਨੇਰੀਓ (L) |
| **Type** | T |
| **Reasoning** | ਖ਼ਤਰਾ for *threat* is normalised in `GLOSSARY.md` (Q13) and kept distinct from ਜੋਖਮ (*risk*), so only the head noun was open — and the obvious candidate was already spoken for. ਦ੍ਰਿਸ਼ ("scene, depicted situation") names a described hypothetical, which is what a threat scenario is in AC.1.3 (a written list) and AC.14.5 (rehearsed cases). It stays visibly distinct from ਪਰਿਦ੍ਰਿਸ਼, which Q11 assigns to *threat landscape* — the two are related in Panjabi exactly as *scene* and *panorama* are in English, which mirrors the source relationship rather than obscuring it. Glossed in English on first use. |
| **Reviewer notes** | |

---

## Q123 — treatment of "Mappings & References" citation lists (structural, not a term)

| Field | Value |
|---|---|
| **EN term** | the `**Mappings & References:**` bullet list that closes each AC family in Appendix C (14 lists, ~60 bullets) |
| **Current pick** | Dual bold label (`**Mappings & References:**` then `**ਮੈਪਿੰਗ ਅਤੇ ਹਵਾਲੇ:**`) followed by a **single** citation list, retained verbatim from the source |
| **Alternatives** | Full dual-block duplication of every bullet, matching how `0x03-Using-AISVS.md`:132–148 duplicates its out-of-scope bullets; translate the parenthetical control titles (e.g. "(Segregation of Duties)", "(Data Leakage Prevention)") while retaining the identifiers |
| **Type** | structural convention |
| **Reasoning** | This follows the `0x10-C06-Supply-Chain.md` References precedent (dual heading, single list) rather than the `0x03` bullet precedent, because the two lists are different kinds of content. The `0x03` bullets are explanatory prose that happens to cite standards; these bullets are pure citation — a requirement ID, then standard identifiers and the clause titles **as those clauses are named in the source standards**. `TRANSLATION-RULES.md` §4 puts clause/parameter names "as they appear verbatim in source" under R, so a duplicated Panjabi list would differ from the English one only in the word "Clauses" while doubling the file and creating 60 near-identical lines that can silently drift apart on the next upstream revision. An auditor matching AISVS to ISO/IEC 27001:2022 A.5.3 needs the English string intact either way. **What could flip it:** a reviewer ruling that dual-block discipline is absolute regardless of content type — in which case all 14 lists duplicate together, and the same ruling should be applied back to C06's References section rather than leaving the corpus split. |
| **Reviewer notes** | |

---

## Q124 — principal (security principal)

| Field | Value |
|---|---|
| **EN term** | "performed by a distinct principal, whether human or system" (Appendix C, AC.8.4); also C9.4.1 ("first-class principal") and C11.2.2 ("per-principal rate limits") |
| **Current pick** | ਪਛਾਣ-ਇਕਾਈ — glossed **ਪਛਾਣ-ਇਕਾਈ (principal)** on first use in a file |
| **Alternatives** | ਪ੍ਰਿੰਸੀਪਲ (L — the form C11 11.2.2 and `0x91-Appendix-B` currently use for *per-principal*); ਕਰਤਾ (T, "doer/agent") — **rejected on Gurmat grounds**: bare ਕਰਤਾ is load-bearing devotional vocabulary in Sikh usage (ਕਰਤਾ ਪੁਰਖੁ, ਕਰਤਾਰ) and applying it to a machine actor is precisely the spiritually-loaded near-synonym class `TRANSLATION-RULES.md` §5 forbids — the same failure shape as Q5 (ਮੁਦਰਾ) and Q88 (ਸੱਚ); ਮੁੱਖ ਪਾਤਰ (T, "leading character" — theatrical); ਕਰਤੱਵਧਾਰੀ (coinage, and collides with ਕਰਤੱਵ at Q109) |
| **Type** | T (with English gloss) |
| **Reasoning** | A *principal* is the authenticated identity an action is attributed to — which is exactly what AC.8.4 needs, since the requirement is that no two stages of an AI-generated change share one identity. ਪਛਾਣ-ਇਕਾਈ ("identity entity") states that and builds on ਪਛਾਣ, already settled corpus-wide, without borrowing ਏਜੰਟ (Q17, reserved) or ਕਰਤਾ. **Found by review 2026-08-27:** Appendix C AC.8.4 originally rendered this ਕਰਤਾ — the only standalone ਕਰਤਾ in the corpus — and was corrected to the C9.4.1 form. **Corpus split still open for a reviewer:** C9.4.1 and `0x91-Appendix-B`:47 use ਪਛਾਣ-ਇਕਾਈ; C11.2.2 and `0x91-Appendix-B`:336 use the loan ਪ੍ਰਿੰਸੀਪਲ for *per-principal*. Both must move together, in whichever direction, rather than staying split. |
| **Reviewer notes** | |

---

## Q125 — sanitization / sanitize

| Field | Value |
|---|---|
| **EN term** | content sanitization (Appendix C, AC.11.1); output sanitization (C3.2.1); memory sanitization (C4.2.4); "rejected or sanitized" (C2.2.1) |
| **Current pick** | ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ / ਸੈਨੀਟਾਈਜ਼ ਕਰਨਾ |
| **Alternatives** | ਸਫ਼ਾਈ (T, "cleaning" — **rejected**: it renders *hygiene* in the very same appendix at AC.12 intro, so one word would carry two unrelated source terms); ਸ਼ੁੱਧੀਕਰਨ (T, "purification" — devotional-ritual register, excluded by `TRANSLATION-RULES.md` §5); ਸਾਫ਼ ਕਰਨਾ (T, "to clean" — same collision as ਸਫ਼ਾਈ, and loses the security sense of neutralising a payload rather than tidying) |
| **Type** | L |
| **Reasoning** | Not a new pick — this entry records an already-settled corpus convention that had drifted. ਸੈਨੀਟਾਈਜ਼ is the form used in C02 2.2.1, C03 3.2.1, C04 4.2.4, C08 and `0x91-Appendix-B` (8 occurrences across 5 files). **Found by review 2026-08-27:** Appendix C AC.11.1 rendered *content sanitization* as ਸਮੱਗਰੀ ਦੀ ਸਫ਼ਾਈ — the only ਸਫ਼ਾਈ-for-sanitization in the corpus, and the worst place for it, since AC.11.1 explicitly instructs the reader to apply "the AISVS C2.1 prompt-injection defenses" and C02 is where the matching term lives. Normalised to ਸਮੱਗਰੀ ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ; ਸਫ਼ਾਈ is left to *hygiene* alone. **What could flip it:** a Sangat preference for a native rendering of the whole input-handling family — it would have to move C02/C03/C04/C08 and this file together. |
| **Reviewer notes** | |

---

## Q126 — attention / attention map

| Field | Value |
|---|---|
| **EN term** | attention map, "which parts of an input a transformer model attends to" (Appendix A) |
| **Current pick** | ਅਟੈਂਸ਼ਨ ਮੈਪ |
| **Alternatives** | ਧਿਆਨ ਮੈਪ (**categorically rejected** — ਧਿਆਨ is core Gurbani/devotional vocabulary for focused remembrance and meditation); ਸੁਰਤ (**rejected** on the same grounds, and already excluded at Q8 for *intelligence*); ਤਵੱਜੋ ਮੈਪ (T, Perso-Panjabi "notice/heed" — free of devotional colour but reads as human attentiveness); ਭਾਰ-ਵੰਡ ਮੈਪ (T, "weight-distribution map" — descriptive and accurate, but not the term of art) |
| **Type** | L |
| **Reasoning** | "attention" sits on the `CLAUDE.md` §AI/ML-specific-risk watch-list, and it is the sharpest case on that list: the literal Panjabi equivalent ਧਿਆਨ is not merely a near-synonym with religious colour but a load-bearing Gurmat term, so a literal calque would be the ਮੁਦਰਾ failure (ASVS Q5) repeated exactly. It also anthropomorphises — a transformer computes a softmax weighting, it does not attend. The loan is neutral, matches the corpus's treatment of other named model-internals (ਟੋਕਨਾਈਜ਼ਰ Q55, ਏਮਬੈਡਿੰਗ-family Q19), and keeps the term searchable against the interpretability literature. The prose gloss in Appendix A deliberately says "ਭਾਰ ਦਿੰਦਾ ਹੈ" ("assigns weight to") rather than any verb of noticing. **What could flip it:** if reviewers want a native form, ਭਾਰ-ਵੰਡ ਮੈਪ is the only candidate that describes the mechanism instead of a mental act — but it must not be ਧਿਆਨ. |
| **Reviewer notes** | |

---

## Q127 — interpretability (extends the explainability entry)

| Field | Value |
|---|---|
| **EN term** | interpretability — appearing only as a modifier: "an interpretability tool" (Attention Map), "an interpretability technique" (Counterfactual Explanation), "an interpretability method" (Feature Attribution). Distinct from **Explainability**, which has its own glossary entry |
| **Current pick** | **ਵਿਆਖਿਆਯੋਗਤਾ** — the same word the explainability entry (Q120) already pins — with the English glossed at each site so the two remain recoverable |
| **Alternatives** | split them: keep ਵਿਆਖਿਆਯੋਗਤਾ for *explainability* and coin ਸਮਝਯੋਗਤਾ for *interpretability* — **rejected**, because ਸਮਝਯੋਗਤਾ is needed one line away for the source's own "human-understandable" inside the Explainability definition; ਬੋਧਗਮਯਤਾ (Sanskritic, over-formal, and reads as cognition); ਇੰਟਰਪ੍ਰੈਟੇਬਿਲਿਟੀ (L — unwieldy and buys nothing) |
| **Type** | T (conformance to Q120) |
| **Reasoning** | Q120 settled *explainability* on ਵਿਆਖਿਆਯੋਗਤਾ from Appendix C; Appendix A is the first file where **both** English words appear, so this entry records what happened rather than deciding it fresh. The appendix uses them near-synonymously — the Explainability entry names attention maps and counterfactual explanations as *its* techniques, which are exactly the three entries that call themselves "interpretability" methods — so coining a second Panjabi word would assert a distinction the source does not make. One word is used and the English is preserved at every site. **Flagged, not resolved**, in the manner of the ਭਰੋਸਾ overload (Q44/Q67): if a later chapter treats interpretability as a property separate from explainability, the reviewer should see the collision here rather than discover it there. Note Q120's own caution about ਵਿਆਖਿਆ's scriptural-exegesis association carries over unchanged. |
| **Reviewer notes** | |

---

## Q128 — covert channel / side-channel

| Field | Value |
|---|---|
| **EN term** | Covert Channel; Side-Channel Attack (Appendix A; covert channels also appear in the Exfiltration definition) |
| **Current pick** | ਲੁਕਵਾਂ ਚੈਨਲ (covert channel); ਸਾਈਡ-ਚੈਨਲ ਹਮਲਾ (side-channel attack) |
| **Alternatives** | ਗੁਪਤ ਚੈਨਲ (**rejected — collision**: ਗੁਪਤ is already fixed at Q50 for *confidential* in ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ / ਗੁਪਤ ਇਨਫ਼ਰੈਂਸ, both of which appear in this same appendix, so "covert" and "confidential" would become one word); ਛੁਪਿਆ ਚੈਨਲ (T, acceptable variant of the current pick); for side-channel — ਪਾਸੇ-ਦਾ-ਚੈਨਲ / ਪਾਰਸ਼ਵ-ਚੈਨਲ (T, literal, unattested and opaque) |
| **Type** | T (covert) + L (side-channel) |
| **Reasoning** | The two terms had to be settled together because both are "information leaks through an unintended path," and the corpus must keep them distinguishable. *Covert* is translated because ਲੁਕਵਾਂ is plain, attested Panjabi ("hidden") and already used in C02 2.2.3 for hidden content; *side-channel* stays a loan because it names a specific attack class in hardware-security literature that a literal Panjabi compound would render unrecognisable. The decisive constraint was the ਗੁਪਤ collision: rendering "covert channel" as ਗੁਪਤ ਚੈਨਲ inside a glossary that also defines ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ would put the protective and the adversarial senses on the same adjective. |
| **Reviewer notes** | |

---

## Q129 — trust boundary / security boundary

| Field | Value |
|---|---|
| **EN term** | trust boundary (own entry); security boundary (Exfiltration); authorization or consent boundary (Downgrade); perturbation bound (Certified Robustness); decision boundaries (Defensive Distillation) |
| **Current pick** | **ਸੀਮਾ** as the standing rendering for *boundary* / *bound* — ਭਰੋਸਾ ਸੀਮਾ, ਸੁਰੱਖਿਆ ਸੀਮਾ, ਸਹਿਮਤੀ ਸੀਮਾ, ਵਿਗਾੜ ਸੀਮਾ, ਫ਼ੈਸਲਾ-ਸੀਮਾ |
| **Alternatives** | ਸਰਹੱਦ (T, "border" — **doubly rejected**: it reads as a territorial/national border, and it contains the string ਹੱਦ, which `tools/lint-terminology.py` flags under the Q69 threshold rule); ਹੱਦਬੰਦੀ (same lint collision); ਬਾਊਂਡਰੀ (L) |
| **Type** | T |
| **Reasoning** | `GLOSSARY.md` binds ਸੀਮਾ to *limit* in the fixed compound ਦਰ ਸੀਮਾ, and Q69 keeps ਥ੍ਰੈਸ਼ਹੋਲਡ separate for *threshold* — but neither claims ਸੀਮਾ exclusively, and the corpus already uses ਸੀਮਾਬੱਧ for "bounded" (C09 C9.1) and ਸੀਮਾਵਾਂ for rate limits (C11 11.2.2). Extending it to *boundary* keeps one geometric-extent word doing one job, with the modifier carrying the distinction (ਭਰੋਸਾ / ਸੁਰੱਖਿਆ / ਸਹਿਮਤੀ / ਵਿਗਾੜ). The ਸਰਹੱਦ rejection is worth recording because it is the first-instinct translation and is mechanically blocked by this repo's own lint — a case where the executable check caught a term before a human did. **What could flip it:** if reviewers want *boundary* visually distinct from *limit*, the change must be made in one pass across all five compounds above. |
| **Reviewer notes** | |

---

## Q130 — data minimization

| Field | Value |
|---|---|
| **EN term** | Data Minimization (own entry); minimization (Sensitive Fields); "minimizing standing privilege exposure" (JIT) |
| **Current pick** | ਘੱਟੋ-ਘੱਟਕਰਨ — ਡਾਟਾ ਘੱਟੋ-ਘੱਟਕਰਨ |
| **Alternatives** | ਨਿਊਨਤਮਕਰਨ (T, Sanskritic — correct but a register jump from the corpus's plain ਘੱਟੋ-ਘੱਟ); ਸੀਮਿਤਕਰਨ (T, "limiting" — a weaker obligation, and §6.3 forbids softening); ਮਿਨੀਮਾਈਜ਼ੇਸ਼ਨ (L) |
| **Type** | T |
| **Reasoning** | ਘੱਟੋ-ਘੱਟ is already the corpus's settled word for *minimum / least* (C05 5.1.2 "ਘੱਟੋ-ਘੱਟ ਸਕੋਪ", C09 9.3.1 "ਘੱਟੋ-ਘੱਟ-ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ"), so deriving the process noun from it keeps the GDPR principle and the least-privilege principle visibly related — which they are. ਸੀਮਿਤਕਰਨ was rejected specifically because data minimization is a *floor* obligation ("only the minimum necessary"), not a request to limit; rendering it as limiting would weaken the control. |
| **Reviewer notes** | |

---

## Q131 — role-based / attribute-based access control (RBAC / ABAC)

| Field | Value |
|---|---|
| **EN term** | RBAC (Role-Based Access Control); ABAC (Attribute-Based Access Control) — acronyms retained |
| **Current pick** | ਭੂਮਿਕਾ-ਆਧਾਰਿਤ ਪਹੁੰਚ ਕੰਟਰੋਲ (RBAC); ਗੁਣ-ਆਧਾਰਿਤ ਪਹੁੰਚ ਕੰਟਰੋਲ (ABAC) |
| **Alternatives** | for *role*: ਰੋਲ (L); ਪਦਵੀ (T, "post/rank" — organisational rank, not an access-control role); ਕਿਰਦਾਰ (T, "character/part" — theatrical). For *attribute*: ਵਿਸ਼ੇਸ਼ਤਾ (**rejected — collision**: Q46 assigns ਗੁਣ to *attributes* precisely so ਵਿਸ਼ੇਸ਼ਤਾ stays clear of *features*, and both words appear in this appendix) |
| **Type** | H — translated modifier + `GLOSSARY.md` ਪਹੁੰਚ ਕੰਟਰੋਲ + retained acronym |
| **Reasoning** | Both expansions are plain architectural compounds whose parts are already fixed elsewhere: ਪਹੁੰਚ ਕੰਟਰੋਲ is locked in `GLOSSARY.md` (and is the one sanctioned ਕੰਟਰੋਲ compound per Q80), ਆਧਾਰਿਤ is locked at Q71, and ਗੁਣ = *attribute* is fixed by Q46 and already on disk in C11 11.2.1. Only ਭੂਮਿਕਾ was genuinely open; it is ordinary formal Panjabi for a role one occupies, carries no theatrical or devotional colour, and composes cleanly. Acronyms stay R per `GLOSSARY.md`. Treated as one entry because the two models are defined against each other and must not diverge in register. |
| **Reviewer notes** | |

---

## Q132 — machine unlearning

| Field | Value |
|---|---|
| **EN term** | Machine Unlearning (Appendix A) |
| **Current pick** | ਮਸ਼ੀਨ ਅਨਲਰਨਿੰਗ |
| **Alternatives** | ਸਿਖਲਾਈ-ਮਿਟਾਈ (T, "training-erasure" — describes the outcome, but the technique does not erase the training, it removes one dataset's influence); ਵਿਸਮਰਨ (**rejected** — Sanskritic "forgetting", and the ਸਮਰਨ/ਸਿਮਰਨ root is devotional, the exact collision Q62 and Q79 guard against for *memory*); ਭੁਲਾਉਣਾ (T, "causing to forget" — anthropomorphises) |
| **Type** | L |
| **Reasoning** | Every native candidate for *unlearning* runs through a verb of forgetting, and Panjabi's formal register for that reaches straight into ਸਿਮਰਨ-adjacent vocabulary — the same trap `TRANSLATION-RULES.md` §5.2 flags for "memory". The loan is consistent with the corpus's other ML-operation loans (ਫ਼ੈਡਰੇਟਿਡ ਲਰਨਿੰਗ Q52, ਟ੍ਰਾਂਸਫ਼ਰ ਲਰਨਿੰਗ Q140) and keeps the regulatory link (right-to-erasure) visible to a practitioner. **What could flip it:** ਸਿਖਲਾਈ-ਪ੍ਰਭਾਵ ਹਟਾਉਣਾ ("removing the training influence") is the most honest native periphrasis if reviewers want one. |
| **Reviewer notes** | |

---

## Q133 — synthetic data

| Field | Value |
|---|---|
| **EN term** | Synthetic Data (Appendix A) |
| **Current pick** | ਸਿੰਥੈਟਿਕ ਡਾਟਾ |
| **Alternatives** | ਬਣਾਉਟੀ ਡਾਟਾ (T — **rejected for the head term**: Q8 assigns ਬਣਾਉਟੀ to *artificial* in ਬਣਾਉਟੀ ਬੁੱਧੀ, so ਬਣਾਉਟੀ ਡਾਟਾ would read as "AI data" by association); ਨਕਲੀ ਡਾਟਾ (T, "fake data" — pejorative, and synthetic data is not counterfeit); ਸਿਰਜਿਆ ਡਾਟਾ (T, "created" — ਸਿਰਜਣਾ carries creation-narrative colour) |
| **Type** | L |
| **Reasoning** | Synthetic data is a named privacy-engineering artifact class, not a description, and the one accurate native adjective is already load-bearing for *artificial* at Q8 — using it here would blur "artificially generated data" with "artificial intelligence" inside one appendix that defines both. Note the definition body still uses ਬਣਾਉਟੀ ਢੰਗ ਨਾਲ ਤਿਆਰ ਕੀਤਾ for the source's "artificially generated", which is correct there because it is describing the generation, not naming the artifact. |
| **Reviewer notes** | |

---

## Q134 — downgrade (of a response)

| Field | Value |
|---|---|
| **EN term** | Downgrade (response) (Appendix A) |
| **Current pick** | ਡਾਊਨਗ੍ਰੇਡ |
| **Alternatives** | ਦਰਜਾ ਘਟਾਉਣਾ (T, "lowering the rank" — reads as demotion of a person); ਸੀਮਤ ਜਵਾਬ (T, "limited response" — **rejected**: it names one of several downgrade behaviours and would silently narrow a defined term); ਨਿਘਾਰ (**rejected — collision**: already on disk in C12 C12.3 for *degradation* in the drift-monitoring sense) |
| **Type** | L |
| **Reasoning** | AISVS gives *downgrade* a precise, enumerated meaning — a family of reduced-scope responses of which refusal is one member — so the rendering must be a name, not a description; §6.3 forbids narrowing it. The loan also keeps it visibly distinct from ਨਿਘਾਰ (*degradation*, an unwanted quality loss) and from ਸੁਚੱਜੀ ਗਿਰਾਵਟ (*graceful degradation*, C09 C9.6), both of which are nearby concepts that mean something else. The full behaviour list is preserved verbatim in the definition. |
| **Reviewer notes** | |

---

## Q135 — excessive agency

| Field | Value |
|---|---|
| **EN term** | Excessive Agency (Appendix A; OWASP LLM06:2025, cited in C07 and C09 reference lists) |
| **Current pick** | Excessive Agency (retained), glossed ਹੱਦੋਂ ਵੱਧ ਏਜੰਟ-ਸਮਰੱਥਾ |
| **Alternatives** | ਹੱਦੋਂ ਵੱਧ ਅਧਿਕਾਰ (**rejected — collision**: ਅਧਿਕਾਰ is bound to *authorization* / *entitlements* per `GLOSSARY.md` Q3, and the source definition already distinguishes capability from permission); ਹੱਦੋਂ ਵੱਧ ਖ਼ੁਦਮੁਖ਼ਤਾਰੀ (T — **too narrow**: autonomy is only the third of the three things the definition says can be excessive); ਵਾਧੂ ਕਾਰਜ-ਸ਼ਕਤੀ (T, coined) |
| **Type** | R (+ T gloss) |
| **Reasoning** | This is a named OWASP vulnerability class with a catalogue identifier, so `GLOSSARY.md` retention applies and the English must survive for a reader cross-referencing LLM06:2025. The gloss had to avoid ਅਧਿਕਾਰ (locked elsewhere) and could not collapse to autonomy alone, so ਏਜੰਟ-ਸਮਰੱਥਾ ("agent capability") was chosen as the broadest neutral head; ਏਜੰਟ is fixed at Q17 and ਖ਼ੁਦਮੁਖ਼ਤਾਰੀ at Q81, both reused in the definition body. ਹੱਦੋਂ ਵੱਧ is the corpus's existing form for *over-* (C03 3.5.2) and is the one ਹੱਦ- form the terminology lint permits. |
| **Reviewer notes** | |

---

## Q136 — certified / certified robustness

| Field | Value |
|---|---|
| **EN term** | Certified Robustness; "certify that model predictions are robust" (Interval-Bound Propagation) |
| **Current pick** | ਸਰਟੀਫ਼ਾਈਡ ਮਜ਼ਬੂਤੀ; verb ਸਰਟੀਫ਼ਾਈ ਕੀਤਾ ਜਾ ਸਕੇ |
| **Alternatives** | ਪ੍ਰਮਾਣਿਤ ਮਜ਼ਬੂਤੀ (**rejected** — ਪ੍ਰਮਾਣਿਤ is locked to *validate* in `GLOSSARY.md`); ਤਸਦੀਕਸ਼ੁਦਾ (**rejected** — ਤਸਦੀਕ is locked to *verify*, and it appears in the same sentence as this term's own definition); ਗਾਰੰਟੀਸ਼ੁਦਾ (T, "guaranteed" — the source already says "guarantee" separately, so this would flatten guarantee and certification into one word) |
| **Type** | L |
| **Reasoning** | The same verb-precision squeeze that forced the loan at Q48 (*attestation*): verify / validate / authenticate / certify are four distinct locked words in this corpus, and *certified robustness* is a fifth adjacent claim — a formal mathematical proof, not a check. `GLOSSARY.md` already locks *certification* to the loan ਸਰਟੀਫ਼ਿਕੇਸ਼ਨ (ASVS Q18) for exactly this reason, so the adjective derives from the loan the corpus has already chosen. The `Certified Robustness` and `Interval-Bound Propagation` entries were settled together because the second entry's definition contains the first entry's verb. |
| **Reviewer notes** | |

---

## Q137 — fault tolerance (Byzantine Fault Tolerance)

| Field | Value |
|---|---|
| **EN term** | Byzantine Fault Tolerance (Appendix A) |
| **Current pick** | Byzantine Fault Tolerance (retained), glossed ਬਾਈਜ਼ੈਂਟਾਈਨ ਫ਼ਾਲਟ ਸਹਿਣਸ਼ੀਲਤਾ |
| **Alternatives** | ਨੁਕਸ ਸਹਿਣਸ਼ੀਲਤਾ for *fault tolerance* (T, fully native — defensible, but ਨੁਕਸ reads as a manufacturing defect rather than a node failure); ਖ਼ਰਾਬੀ ਸਹਿਣਸ਼ੀਲਤਾ (ਖ਼ਰਾਬੀ was already set aside at Q40 as "malfunction"); full translation of the whole term (loses a named distributed-systems property) |
| **Type** | R (+ H gloss) |
| **Reasoning** | This entry finally spends the word Q12 and Q84 both deliberately reserved: **ਸਹਿਣਸ਼ੀਲਤਾ is kept free of *resilience* (ਲਚਕੀਲਾਪਣ, Q12) and *robustness* (ਮਜ਼ਬੂਤੀ, Q84) precisely so that *tolerance* could take it here**, and this is the first place in the corpus where all three English words are in play. The named property itself stays English because it references a specific consensus result; only the head noun is glossed. |
| **Reviewer notes** | |

---

## Q138 — concept drift

| Field | Value |
|---|---|
| **EN term** | Concept Drift (Appendix A), alongside Data Drift |
| **Current pick** | ਕਾਨਸੈਪਟ ਡ੍ਰਿਫ਼ਟ |
| **Alternatives** | ਸੰਕਲਪ ਡ੍ਰਿਫ਼ਟ (T head — ਸੰਕਲਪ is standard academic Panjabi for *concept*, but in religious register it also names a ritual vow, and the corpus's default is to avoid a loaded near-synonym where a neutral option exists); ਧਾਰਨਾ ਡ੍ਰਿਫ਼ਟ (**rejected** — Q6 set ਪੂਰਵ-ਧਾਰਨਾ aside for anthropomorphising the model, and ਧਾਰਨਾ here would suggest the model holds notions that shift); ਅਰਥ-ਖਿਸਕਾਅ (T, coined) |
| **Type** | L |
| **Reasoning** | ਡ੍ਰਿਫ਼ਟ is already the corpus's loan for *drift* (C12 C12.3, ਡਾਟਾ ਡ੍ਰਿਫ਼ਟ), and the two drift types are defined against each other — the source's whole point is that data drift and concept drift are different failures. Keeping both heads as loans makes the pair read as one family and avoids asserting, via ਧਾਰਨਾ, that a model holds concepts. **What could flip it:** ਸੰਕਲਪ ਡ੍ਰਿਫ਼ਟ is the reasonable native pick if reviewers judge the ritual sense of ਸੰਕਲਪ too marginal to matter; it would change one site. |
| **Reviewer notes** | |

---

## Q139 — chain of thought

| Field | Value |
|---|---|
| **EN term** | Chain of Thought (Appendix A) |
| **Current pick** | Chain of Thought (retained), glossed ਸੋਚ ਦੀ ਲੜੀ |
| **Alternatives** | ਵਿਚਾਰ-ਲੜੀ (T — ਵਿਚਾਰ is central Gurbani vocabulary for contemplation, e.g. *gurbāṇī vīchār*, and carries devotional weight the source does not); ਤਰਕ-ਲੜੀ (T, "reasoning chain" — accurate but it is the *technique's effect*, and ਤਰਕ is already used for *reasoning* in the Agent and Chain-of-Thought definitions themselves); ਚੇਨ ਆਫ਼ ਥਾਟ (L) |
| **Type** | R (+ T gloss) |
| **Reasoning** | A named prompting technique, so `GLOSSARY.md` retention applies. The gloss deliberately takes the plainest available word for *thought* — ਸੋਚ, everyday and neutral — rather than ਵਿਚਾਰ, which would import a contemplative-devotional register into a description of intermediate token generation. ਲੜੀ for *chain* matches ਲੜੀ-ਕ੍ਰਮ (Q31) and ਐਗਜ਼ੀਕਿਊਸ਼ਨ ਲੜੀ (C09 9.4.2), so the chain metaphor stays consistent corpus-wide. |
| **Reviewer notes** | |

---

## Q140 — named ML techniques carried as loans (conformance batch)

| Field | Value |
|---|---|
| **EN term** | Transfer Learning; Temperature Scaling; Defensive Distillation; Data Augmentation; Quantization (conformance); Tokenizer (conformance) |
| **Current pick** | ਟ੍ਰਾਂਸਫ਼ਰ ਲਰਨਿੰਗ; ਟੈਂਪਰੇਚਰ ਸਕੇਲਿੰਗ; ਬਚਾਅ-ਪੱਖੀ ਡਿਸਟਿਲੇਸ਼ਨ; ਡਾਟਾ ਔਗਮੈਂਟੇਸ਼ਨ |
| **Alternatives** | transfer learning → ਤਬਾਦਲਾ ਸਿਖਲਾਈ (T — ਤਬਾਦਲਾ is administrative transfer of a person); temperature scaling → ਤਾਪਮਾਨ ਸਕੇਲਿੰਗ (T — the ML "temperature" is a softmax parameter, not heat, and the literal calque actively misleads); defensive distillation → ਰੱਖਿਆਤਮਕ ਨਿਖੇੜ (T, coined); data augmentation → ਡਾਟਾ ਵਾਧਾ (T, "increase" — loses the transform-and-copy mechanism) |
| **Type** | L (ਬਚਾਅ-ਪੱਖੀ is a T modifier on an L head) |
| **Reasoning** | One entry for the batch because they are one decision, already made: `TRANSLATION-RULES.md` §4 routes named ML operations with no settled Panjabi word to L, and this corpus has applied that at Q3 (ਫ਼ਾਈਨ-ਟਿਊਨਿੰਗ), Q52 (ਫ਼ੈਡਰੇਟਿਡ ਲਰਨਿੰਗ), Q57 (ਕੁਆਂਟਾਈਜ਼ੇਸ਼ਨ), and Q64 (ਕਲੱਸਟਰਿੰਗ / ਵੈਕਟਰਾਈਜ਼ੇਸ਼ਨ). ਟ੍ਰਾਂਸਫ਼ਰ ਲਰਨਿੰਗ is deliberately built on the same ਲਰਨਿੰਗ head as ਫ਼ੈਡਰੇਟਿਡ ਲਰਨਿੰਗ so the two read as siblings. *Temperature scaling* is the one worth flagging: it is the clearest case in this appendix where the literal calque would be wrong rather than merely awkward, since ਤਾਪਮਾਨ means heat. Only *defensive* was translated, because it is an ordinary adjective and ਬਚਾਅ is the corpus's word for *defence* (C11 C11.3 title). ਔਗਮੈਂਟੇਸ਼ਨ follows C12 12.5.1, already on disk. |
| **Reviewer notes** | |

---

## Q141 — defense-in-depth

| Field | Value |
|---|---|
| **EN term** | Defense-in-Depth (Appendix A; also `0x03-Using-AISVS.md` Level 3 prose) |
| **Current pick** | Defense-in-Depth (retained), glossed ਡੂੰਘਾਈ ਵਿੱਚ ਬਚਾਅ |
| **Alternatives** | ਬਹੁ-ਪਰਤੀ ਬਚਾਅ (T, "multi-layered defence" — clearer to a first-time reader, and arguably a better description; **rejected only because** it renames a doctrine that has a fixed English name across NIST/CIS literature); ਡੈਪਥ ਡਿਫ਼ੈਂਸ (L) |
| **Type** | R (+ T gloss) |
| **Reasoning** | A named security doctrine, treated like Zero Trust (Q25) and Zero Standing Privilege: the English is what an auditor and a reference list will use. The gloss is literal rather than explanatory because the definition immediately beneath it states the layering mechanism in full. **Note for reviewers:** ਬਹੁ-ਪਰਤੀ ਬਚਾਅ is the strongest native candidate anywhere in this appendix — if the corpus ever adopts native forms for named doctrines, this is the one to start with. **Found by the full-corpus audit 2026-08-27:** the entry's own second site, `0x03-Using-AISVS.md`:98 (Level 3 prose), diverged twice — it hyphenated the gloss as ਡੂੰਘਾਈ-ਵਿੱਚ-ਬਚਾਅ, and it wrote the *retained English* as "defense in depth" while `1.0/en/0x03-Using-AISVS.md`:51 and Appendix A both hyphenate it. Under this entry's own R-classification the English head must reproduce the source form, so both halves were normalised to ਡੂੰਘਾਈ ਵਿੱਚ ਬਚਾਅ (defense-in-depth). The attributive hyphenation was defensible Panjabi style in that sentence; it was dropped for corpus consistency, and a reviewer who prefers the hyphenated attributive should change Appendix A with it rather than re-splitting the two. |
| **Reviewer notes** | |

---

## Q142 — Appendix A conformance to picks settled in the C10/Appendix-C/Appendix-D batches

| Field | Value |
|---|---|
| **EN term** | fail-closed / fail-open; red-teaming; policy-as-code; baseline; principal; guardrail; explainability; appendix (all appearing in `0x90-Appendix-A_Glossary.md`) |
| **Current pick** | ਨਾਕਾਮੀ-'ਤੇ-ਬੰਦ / ਨਾਕਾਮੀ-'ਤੇ-ਖੁੱਲ੍ਹਾ (Q104); ਰੈੱਡ-ਟੀਮਿੰਗ (Q108); ਕੋਡ-ਵਜੋਂ-ਨੀਤੀ (Q113); ਬੇਸਲਾਈਨ (Q118); ਪਛਾਣ-ਇਕਾਈ (Q124); ਗਾਰਡਰੇਲ (Q105); ਵਿਆਖਿਆਯੋਗਤਾ (Q120); ਅੰਤਿਕਾ A (Q121) |
| **Alternatives** | the Appendix A draft's own first picks, all **changed to conform rather than defended**: ਫ਼ੇਲ੍ਹ-ਕਲੋਜ਼ਡ / ਫ਼ੇਲ੍ਹ-ਓਪਨ (loan pair); `Red-Teaming` retained Latin with a ਵਿਰੋਧੀ-ਧਿਰ ਪਰਖ gloss; ਨੀਤੀ-ਵਜੋਂ-ਕੋਡ (constituents reversed); ਆਧਾਰ-ਰੇਖਾ for *baseline*; ਪ੍ਰਿੰਸੀਪਲ (loan) |
| **Type** | conformance record — no new terminology decision |
| **Reasoning** | Appendix A was drafted in parallel with the C10, Appendix C, and Appendix D files, and five of its terms were independently rendered before those files' entries (Q104, Q108, Q113, Q118, Q124) landed in this document. Rather than leave the corpus split — the exact failure the 2026-08-26 cross-file audit and `tools/lint-terminology.py` exist to prevent — Appendix A was changed to the picks already recorded here, and the superseded drafts are listed above so a reviewer can see what was given up. Three further terms (ਗਾਰਡਰੇਲ, ਵਿਆਖਿਆਯੋਗਤਾ, ਅੰਤਿਕਾ) were arrived at independently and **already matched**, which is weak but real evidence that the reasoning rules in `TRANSLATION-RULES.md` §4–§5 reproduce across translators. **Two of the changes cost something and should be reviewed as such:** (a) ਰੈੱਡ-ਟੀਮਿੰਗ transliterates a named practice that `GLOSSARY.md`'s retention rule would arguably keep in Latin — Q108 chose the loan and Appendix A follows, but the retention-vs-transliteration line for named practices is now visibly inconsistent with `many-shot jailbreaking` (Q32) and should be settled once; (b) ਨਾਕਾਮੀ-'ਤੇ-ਬੰਦ is longer than the loan and appears in Appendix A as a defined head term rather than in running prose, where a compact form reads better — Q104's symmetry argument is sound and was accepted, but the glossary is the place where its cost is highest. |
| **Reviewer notes** | |

---

## Q143 — Appendix A layout: entry-level dual-block

| Field | Value |
|---|---|
| **EN term** | (not a term — the bilingual structure of `0x90-Appendix-A_Glossary.md`) |
| **Current pick** | Per-entry pairing: the English bullet, then immediately the Panjabi bullet, one blank line between entries. Panjabi heads follow the §6.2 pattern `ਪੰਜਾਬੀ (English)`; retained heads keep the English form with a Panjabi gloss in parentheses where one exists |
| **Alternatives** | two full blocks (all 152 English entries, then all 152 Panjabi entries) — the literal reading of §6.1 for a list; a single merged bullet per entry with both languages in one line (**rejected** — it is the "merged table" failure the chapter convention forbids) |
| **Type** | structural convention |
| **Reasoning** | §6.1 fixes the order (English block, then Panjabi block) and the chapters apply it at the granularity of the *unit*: paragraph-then-paragraph, table-then-table. For a 152-entry alphabetical reference the unit is the entry, not the list — splitting into two 152-entry blocks would put each definition roughly 300 lines from its translation and make the appendix unusable as a lookup, which is the one thing a glossary must be. Per-entry pairing preserves the English-first order, keeps the two blocks unmerged, and matches how `0x03-Using-AISVS.md` handles its bullet lists (English block, then Panjabi block) at the scale that file's lists actually are. Every English line is byte-identical to `1.0/en/`. **What could flip it:** a reviewer preference for whole-list blocks; it is a mechanical transformation either way. |
| **Reviewer notes** | |

---

## Q144 — Appendix A corrections found by independent review (2026-08-27)

| Field | Value |
|---|---|
| **EN term** | ground-truth values (Labeling); side effects (Exfiltration); replay (DPoP, Strong Authentication); post-hoc (Temperature Scaling); visualization (Attention Map); consensus (Byzantine Fault Tolerance); specification (OAuth 2.1); error/mistake noun spelling |
| **Current pick** | `ground-truth ਮੁੱਲ` (retained head + ਮੁੱਲ); ਸਹਿ-ਪ੍ਰਭਾਵ (side effects); `replay (ਦੁਹਰਾਓ)`; ਉਪਰੰਤ-ਲਾਗੂ (post-hoc); ਦ੍ਰਿਸ਼ ਪੇਸ਼ਕਾਰੀ (visualization); ਸਰਬ-ਸਹਿਮਤੀ (consensus); ਸਪੈਸੀਫ਼ਿਕੇਸ਼ਨ (specification); ਗਲਤੀ (no nukta) |
| **Alternatives** | the Appendix A draft's own forms, all **superseded**: ਮੂਲ-ਸੱਚ ਮੁੱਲ; ਮਾੜੇ ਪ੍ਰਭਾਵ; ਮੁੜ-ਵਰਤੋਂ / ਮੁੜ ਵਰਤਣਾ; ਪਿਛਲਖੁਰੀ; ਦ੍ਰਿਸ਼ਟਾਂਤ; ਸਹਿਮਤੀ; ਵਿਸ਼ੇਸ਼-ਵੇਰਵਾ; ਗ਼ਲਤੀ |
| **Type** | corrective record — seven conformance fixes and one fidelity fix, no new terminology decision |
| **Reasoning** | **Corrective entry, in the manner of Q102 and Q125.** An independent adversarial review of `0x90-Appendix-A_Glossary.md` on 2026-08-27 found eight sites where the appendix competed with a decision already recorded here, or mistranslated. (a) **Gurmat — the load-bearing one:** *ground-truth values* was rendered ਮੂਲ-ਸੱਚ ਮੁੱਲ, the only ਸੱਚ in the translated corpus, and **Q97 rejects ਸੱਚ / ਸਤਿ by name** as load-bearing devotional vocabulary for Divine Truth in Gurbani. Q97 forbade it for *source of truth*; the same rejection binds *ground truth*, which is the same metaphor applied to a label column. Corrected to the retained Latin head plus ਮੁੱਲ, matching the `prompt ਕੈਸ਼` / `embedding ਇੰਡੈਕਸ` hybrid pattern (Q19, Q21). (b) *side effects* was ਮਾੜੇ ਪ੍ਰਭਾਵ ("adverse effects") — a value judgement the source does not make, and a split from C09 9.3 (`0x10-C09`:78), which already glosses ਸਹਿ-ਪ੍ਰਭਾਵ (side effects). (c) *replay* was ਮੁੜ-ਵਰਤੋਂ at two sites, breaking Q92/Q102 (`replay` retained Latin, glossed ਦੁਹਰਾਓ) and additionally colliding with ਮੁੜ-ਵਰਤੋਂ = *reuse* in `0x01-Frontispiece`:36. (d) *post-hoc* was ਪਿਛਲਖੁਰੀ, which means "retrograde / walking backwards" and reads as regression rather than "applied afterwards"; the corpus's settled form for that is -ਉਪਰੰਤ (Q18, Q57, and ਸਿਖਲਾਈ-ਉਪਰੰਤ in this same file). (e) *visualization* was ਦ੍ਰਿਸ਼ਟਾਂਤ, which means an illustrative example or parable and is a term of art in commentarial exegesis — the wrong word twice over, and in the single entry (Attention Map, Q126) that carries the most Gurmat scrutiny in the appendix. (f) *consensus* was ਸਹਿਮਤੀ, which is fixed to *consent* corpus-wide (`0x03`:145, C10 10.4.7, Q93, Q129) and appears with that sense four times in this same file — the ਗੁਪਤ collision shape of Q128. (g) *specification* was the coinage ਵਿਸ਼ੇਸ਼-ਵੇਰਵਾ, which double-collides: ਵੇਰਵਾ is the requirement tables' *Description* column corpus-wide, and ਵਿਸ਼ੇਸ਼- is bound to ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ (*privilege*). Routed to L per §4. (h) The appendix carried both ਗ਼ਲਤੀ and ਗਲਤੀ for the same noun; **Q98 rules the noun is spelled ਗਲਤੀ without nukta** to match `GLOSSARY.md` ਗਲਤੀ ਪ੍ਰਬੰਧਨ and C01, and says explicitly that a file must not introduce a second spelling. Normalised; ਗ਼ਲਤ (adjective, with nukta) is left alone because C07, C11, C12 and `0x92` all use that form. `tools/lint-terminology.py` exits 0 after all eight changes. **Open for the reviewer:** (i) the corpus is split between the adjective ਗ਼ਲਤ (nukta) and the noun ਗਲਤੀ (no nukta) — defensible, but if reviewers want one orthography it must move in a single pass across all files, per the Q86 rule; (ii) the `Model Extraction` entry glosses the head ਮਾਡਲ ਚੋਰੀ while leaving *model theft* in English inside the definition, which inverts the boundary Q54 set (ਚੋਰੀ names the harm, `model extraction` stays English) — left unchanged because the source entry itself declares the two synonymous, but it is the one place in the appendix where Q54's line is not visible. |
| **Reviewer notes** | |

---

## Q145 — full-corpus terminology audit, 2026-08-27 (all 18 files)

| Field | Value |
|---|---|
| **EN term** | (not a term — the corpus-wide consistency pass run once every chapter, appendix, and front-matter file existed on disk) |
| **Current pick** | three cross-file splits normalised (Q50 *confidential computing*, Q112 *immutable*, Q141 *defense-in-depth*); two false cross-reference claims in this file corrected (Q71, Q110); six new rules added to `tools/lint-terminology.py` |
| **Alternatives** | logging the findings without the lint rules — **rejected**, that is the exact failure mode this file keeps re-discovering; adding a rule for every finding — **rejected**, two findings are not mechanically expressible without false positives and are recorded as such below |
| **Type** | audit record — no new terminology decision |
| **Reasoning** | **What the audit checked.** (1) `tools/lint-terminology.py` over all 14 translated files — clean before and after. (2) Every "`<Panjabi>` (`<English>`)" first-use gloss in the corpus, harvested and grouped by English term, to find any gloss preceded by two different Panjabi forms. (3) All 152 Appendix A headwords joined to this file's picks — **33 direct joins, zero mismatches**, which is the strongest single piece of evidence that the appendix conforms rather than competes. (4) Every Appendix A headword whose Panjabi form appears in no other file, searched by its *English* term across the corpus to find a competing rendering. (5) Every assertive cross-reference claim in this file ("already used in", "matches", "carries precedent") re-derived against the actual files. **The three splits.** All three shared one shape: the chapter and `0x91-Appendix-B` — which restates every requirement — rendered *the same requirement id* two ways. That makes Appendix B the corpus's most useful consistency instrument, because a split there is checkable by joining on the requirement id rather than by reading. Details in Q50, Q112, Q141. **The two false claims.** Q71 asserted C08 "uses the same term" for *grounding*; it does not use it at all. Q110 asserted AC.7.1 carries both *workflow* and *pipeline*; it carries only the first. Both are the Q73/Q74 shape — a plausible-sounding harmonisation obligation written from memory of what a sibling file *probably* says, never checked. Corrected in place with the real second site named, so the next audit can verify rather than re-derive. **Why six lint rules and not two.** The three splits produced one mechanically-expressible rule (ਕਾਨਫ਼ੀਡੈਂਸ਼ੀਅਲ). The other five rules guard something worse: **every Gurmat rejection in this file was prose-only.** Q97 rejected ਸੱਚ/ਸਤਿ, Q124 rejected bare ਕਰਤਾ, `GLOSSARY.md` rejected ਮੁਦਰਾ — and Q144(a) shows a rejected word being re-introduced by the next file anyway, because nothing stopped it. Those three are now blocked, along with the noun spelling ਗ਼ਲਤੀ (Q98) and the four superseded Appendix A forms (Q144). Every added pattern was verified to match zero sites before being committed, and each was negative-tested against its legitimate near-miss — ਜਾਰੀਕਰਤਾ and ਪਛਾਣਕਰਤਾ do not trip the ਕਰਤਾ rule, the adjective ਗ਼ਲਤ does not trip the ਗ਼ਲਤੀ rule, ਸੱਚਮੁੱਚ does not trip the ਸੱਚ rule. **Two findings deliberately left unguarded.** (i) *immutable*: the C08 holdout was a paraphrase, and no regex forbids a paraphrase without firing on ordinary prose. (ii) *sanitization*: Q125 pins ਸੈਨੀਟਾਈਜ਼ੇਸ਼ਨ, but bare ਸਫ਼ਾਈ must stay legal because it correctly renders *hygiene* at `0x92`:411 — linting it would break a correct line to protect an incorrect one. Both are caught by the Appendix B requirement-id join instead, which is the check to automate next. **Left open, not fixed.** Q124's ਪਛਾਣ-ਇਕਾਈ vs ਪ੍ਰਿੰਸੀਪਲ split (C9.4.1 and `0x91`:47 against C11.2.2 and `0x91`:336) is a live reviewer decision; linting either form would silently settle a question this file explicitly refers to the Sangat. |
| **Reviewer notes** | |

---

## Maintainer

Gurvinder Singh (@GeeksikhSecurity)
