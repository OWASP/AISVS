# OWASP AISVS — Panjabi (pa-IN) Translation Rules

**Status:** canonical · **Updated:** 2026-08-26 · **Lead:** Gurvinder Singh (@GeeksikhSecurity)
**Method:** AI-assisted draft (v0.1) → Sangat/community review is the certification gate.

This rule set is forked verbatim from the OWASP ASVS 5.0 Panjabi translation's
[`TRANSLATION-RULES.md`](https://github.com/GeeksikhSecurity/ASVS/blob/panjabi-translation-v5/5.0/pa-IN/TRANSLATION-RULES.md)
so both standards read as one consistent corpus. Where a rule below references
"the sibling corpus," that means the ASVS 5.0 pa-IN translation — consult its
`GLOSSARY.md`-equivalent (`OPEN-QUESTIONS.md` resolved entries, seeded here as
[`GLOSSARY.md`](GLOSSARY.md)) before inventing a new rendering for any term
that could plausibly already exist there.

---

## 1. Script & encoding

1. **Gurmukhi only** (U+0A00–U+0A7F). NEVER Devanagari letters; NEVER Latin transliteration
   of the Panjabi body text.
2. **Unicode NFC**-normalise all Panjabi text (precomposed nukta — e.g. ੜ, not ਡ+਼).
3. Allowed shared punctuation: danda `।` (U+0964), double-danda `॥` (U+0965).
4. Proper use of mātrā (ਮਾਤਰਾ), addak (ੱ), tippi/bindi (ੰ/ਂ), nukta (਼).

## 2. Orthography

1. **Sentence-end = danda `।`** for full Panjabi sentences (prose). NEVER the Western period.
   Do **not** add a danda to short UI labels, headings, or list fragments.
2. **Numerals = Western digits** (0–9) in technical prose — years, quantities, **and version
   numbers** (write `1.0`, not `੧.੦`). Gurmukhi numerals are reserved for traditional/decorative
   contexts only.
3. **Requirement IDs stay exactly as the source** (e.g. AISVS `C01.1.1` or equivalent) —
   English digits, never converted.
4. **The apostrophe-clitic `'ਤੇ` is ACCEPTABLE** Panjabi orthography (attested in real academic
   text, e.g. `…ਡੀ)'ਤੇ`). It is **NOT** a translation error and must **not** be flagged by lint.
5. **Spelling:** "Panjabi" / "Panjab" (per Sikhri.org and Panjab Digital Library), not
   "Punjabi" / "Punjab", in any English appearing in the translation.

## 3. Romanization

When romanizing a Panjabi term, use **IAST** diacritics (ṭ ḍ ṇ ā ī ū ṅ ñ, "chh", the ʼ for
addak) — never doubled-vowel English style (write `ṭhaggī`, not `thaggee`).

## 4. Register & terminology (T/L/R/H)

Match the register of **formal academic Panjabi**. Classify every term:

| Tag | Use | Examples (attested in real academic Panjabi) |
|---|---|---|
| **T — Translated** (native/Sanskritic) for established concepts | ਪ੍ਰਮਾਣੀਕਰਨ (authentication), ਅਖੰਡਤਾ (integrity), ਸਿਧਾਂਤ (theory), ਅੰਤਰ-ਅਨੁਸ਼ਾਸਨੀ (inter-disciplinary) |
| **L — Loan** (transliterated) for modern/Western terms with no settled Panjabi word | ਟੋਕਨ (token), ਡਾਊਨਲੋਡ (download), ਮਾਡਲ (model), ਵੈਕਟਰ (vector) |
| **R — Retained** in English/Latin — never translate or transliterate | OWASP, AISVS, CWE, API, URL, TLS, JSON, LLM, MCP, RAG, GPU, model/dataset/library names, algorithm names, header/claim/parameter names as they appear verbatim in source |
| **H — Hybrid** (English head + Panjabi word) | SQL ਇੰਜੈਕਸ਼ਨ, prompt ਇੰਜੈਕਸ਼ਨ, embedding ਸਟੋਰ |

**Glossary anchoring:** check [`GLOSSARY.md`](GLOSSARY.md) (seeded from the ASVS sibling
corpus) first, then Punjabi University lexicography, before coining a new term. Cite sources
(APA) for contested choices. Any new AISVS-specific term (e.g. "prompt injection," "model
weights," "hallucination," "agentic," "guardrail") that has no ASVS precedent gets logged as a
new entry in `OPEN-QUESTIONS.md` using the ASVS corpus's format (EN term / current pick /
alternatives / reasoning) — do not silently improvise.

### Verb precision
Preserve "verify" / "validate" / "check" / "detect" / "monitor" as distinct — they are not
interchangeable in a security standard. AISVS requirements typically open "Verify that…" →
**ਤਸਦੀਕ ਕਰੋ ਕਿ…** (matches the ASVS convention).

### First-use gloss
On first use of a translated technical concept, give the Panjabi term followed by the English
in parentheses, e.g. **ਅਖੰਡਤਾ (integrity)**. Do not repeat the gloss every time.

## 5. Gurmat / cultural safety

1. No yoga/Hindu/Sanskrit-devotional vocabulary outside a direct Gurbani quotation. (E.g.
   render "posture/state" as **ਸਥਿਤੀ** (sthitī), never **ਮੁਦਰਾ** (mudrā, yoga-connoted) — this
   exact collision already happened once in the ASVS corpus (Q5) and must not recur here.)
2. AI/ML-specific risk: terms like "hallucination," "alignment," "guardrail," "agent," and
   "memory" carry metaphorical baggage in English that must NOT be rendered via any
   yoga/Hindu-connoted Panjabi word even when a literal cognate would superficially fit. Prefer
   neutral technical Panjabi over a spiritually-loaded near-synonym every time.
3. Sacred/Gurbani material requires **Sangat sign-off**; no AI output self-certifies above v0.1.

## 6. Bilingual structure

1. **Dual-block:** English block, then the Panjabi translation block (consistent order
   corpus-wide, matching the ASVS sibling corpus).
2. **Heading model:** `Panjabi Heading (English)` or `English Heading ਪੰਜਾਬੀ ਸਿਰਲੇਖ`, applied
   consistently.
3. Do not soften, omit, or add security obligations; translate the requirement as written.

## 7. Process

- AI-assisted draft (highest-available model, Opus) using these rules as the system-prompt
  contract → mechanical QA → **Sangat/community review = certification gate**.
- Mechanical QA before review: 0 Devanagari leaks, 0 Western-period sentence-ends, 0
  Gurmat-prohibited terms, retained-terms intact, NFC-clean, every requirement ID from
  `1.0/en/` present in `1.0/pa-IN/`.

---

*Forked from the ASVS 5.0 pa-IN `TRANSLATION-RULES.md`. Changes here that should also apply
to the ASVS corpus (or vice versa) get proposed as a change to `GLOSSARY.md` in both repos,
not silently diverged.*
