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
| **Reasoning** | One consistent hybrid pattern across all three: translate the adjective, loan the technical head noun, retain the acronym per §4 (R). This keeps ਭਰੋਸੇਯੋਗ (trusted) / ਸੁਰੱਖਿਅਤ (secure) / ਗੁਪਤ (confidential) visibly distinct, which the source relies on — C4.3.5 contrasts a *trusted runtime* with a *secure enclave* inside one sentence. "Enclave" stays a loan because it names a specific vendor primitive (SGX / TrustZone class), not a generic region. Glossed in English on first use. |
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
| **Reasoning** | "Grounding" sits on the `CLAUDE.md` high-risk metaphor list. The English is a metaphor for "anchored in retrieved evidence," and the neutral technical rendering of that is ਆਧਾਰਿਤ (based on / founded on); any literal earth/ground rendering imports imagery the source does not intend, and ਟਿਕਾਇਆ ਹੋਇਆ is unattested in this sense. ਆਧਾਰਿਤ is also the commoner form over ਆਧਾਰਬੱਧ and already composes with the **AI agent** entry's ਏਜੰਟ-ਅਧਾਰਿਤ. **Must stay consistent with C8 (Memory, Embeddings & Vector Database)**, which uses the same term. **Cross-file audit 2026-08-26:** the corpus was split 3–3 between ਆਧਾਰਿਤ (Preface, C04, C07) and the short-vowel ਅਧਾਰਿਤ (0x03 ×2 in ਏਜੰਟ-ਅਧਾਰਿਤ, C02 2.1.2 in ਨੀਤੀ-ਅਧਾਰਿਤ) — including inside this entry's own claim that it "already composes with ਏਜੰਟ-ਅਧਾਰਿਤ," which was self-contradictory. All normalised to **ਆਧਾਰਿਤ** (the ਆਧਾਰ root takes the long ā); Q17 corrected to match. |
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

## Maintainer

Gurvinder Singh (@GeeksikhSecurity)
