# CLAUDE.md — OWASP AISVS Panjabi Translation Rules

## Project

OWASP AISVS 1.0 Panjabi (pa-IN) translation. Bilingual English/Gurmukhi format.
Repository: `OWASP-AISVS-Panjabi`, branch `panjabi-translation-v1`.
Sibling corpus: OWASP ASVS 5.0 Panjabi — `GeeksikhSecurity/ASVS` branch
`panjabi-translation-v5`, `5.0/pa-IN/`. This translation reuses that project's
rules and vocabulary so both standards read as one consistent corpus.

> **Canonical rule set:** [`TRANSLATION-RULES.md`](TRANSLATION-RULES.md) is the
> authoritative source for all translation decisions (script, orthography,
> numerals, romanization, T/L/R/H terminology, Gurmat safety, bilingual
> structure). This file is the operational companion; if the two ever diverge,
> `TRANSLATION-RULES.md` wins.
>
> **Shared vocabulary:** [`GLOSSARY.md`](GLOSSARY.md) seeds the settled terms
> from the ASVS sibling corpus. Check it before coining any new rendering —
> an AISVS-specific term with no ASVS precedent gets logged fresh in
> `OPEN-QUESTIONS.md` (create it in the same format as the ASVS one:
> EN term / current pick / alternatives / reasoning).

## Spelling

Use **"Panjabi"** (not "Punjabi") per Sikhri.org and Panjab Digital Library standards.

---

## Translation Dictionary Sources (MANDATORY)

All Panjabi translations MUST cross-reference these scraped dictionary sources before using any term:

1. **Guru Granth Sahib Dictionary** — https://gurugranthsahibdictionary.io/
   - Primary source for Gurmukhi vocabulary, word roots, and semantic context
   - Scraped content available in project data files when present

2. **Guru Granth Sahib Reference** — https://gurugranthsahib.io/info/english/guru-granth-sahib
   - Contextual definitions and usage patterns rooted in Gurbani tradition
   - Gurmukhi script institutionalized by Guru Angad Sahib

3. **Punjabi University Patiala English-Punjabi Dictionary** (ISBN 81-7380-095-2)
   - Secondary reference for technical/modern terms not found in Gurbani sources
   - Use entries for authentication (ਪ੍ਰਮਾਣੀਕਰਨ, ਤਸਦੀਕ), authorization (ਅਧਿਕਾਰੀਕਰਨ), access (ਪਹੁੰਚ), etc.

### Dictionary Lookup Order
1. Check `GLOSSARY.md` first — the term may already be settled from the ASVS corpus
2. Check gurugranthsahibdictionary.io
3. Check gurugranthsahib.io for contextual usage
4. Fall back to Punjabi University Patiala dictionary for technical/AI-specific terms
5. If no match found, document as "open terminology question" in `OPEN-QUESTIONS.md`

---

## Gurmat Language Constraints (MANDATORY)

Adapted from the Gurmat-Centered Bilingual Prompt (Google Doc ID: 1G23l0TJ9594K0yYBUcp4quR4vsOcTUjVCTYWWmopx0Y).

### NEVER USE — Prohibited Terminology
- ❌ Yoga terminology (chakras, kundalini, pranayama, third eye)
- ❌ Hindu deity names or mythology references
- ❌ Energy centers, auras, or metaphysical yoga concepts
- ❌ Sanskrit mantras or terms outside of Gurbani context
- ❌ Any term with yoga/Hindu connotation when a Gurmat or neutral Panjabi equivalent exists

### AI/ML-specific risk (read before translating these)
English AI vocabulary borrows spiritually-loaded metaphors far more than
general security prose does. Apply extra scrutiny to: **hallucination,
alignment, guardrail, agent/agentic, memory, attention, grounding, emergent
behavior, embodiment**. The ASVS corpus already had one exact version of this
failure — "posture" first rendered ਮੁਦਰਾ (yoga hand-gesture) before being
corrected to ਸਥਿਤੀ (commit `9e1e96b`, ASVS Q5). Default to neutral technical
Panjabi over a spiritually-loaded near-synonym every time; see `GLOSSARY.md`
for the full precedent.

### ALWAYS PREFER — Gurmat-Aligned Vocabulary
- ✅ Terms rooted in Gurmukhi tradition and Sikh scholarly usage
- ✅ Vocabulary from Guru Granth Sahib Dictionary when applicable
- ✅ Prof. Sahib Singh's Darpan methodology for interpretive guidance
- ✅ Contemporary Panjabi that resonates with modern technical readers
- ✅ Bilingual format maintaining parallel meaning (English | ਪੰਜਾਬੀ)

### Quality Check Before Every Commit
- [ ] Zero yoga/Hindu/Sanskrit influence outside Gurbani
- [ ] All terms cross-referenced against `GLOSSARY.md`, then the dictionary sources above
- [ ] Open terminology questions documented in `OPEN-QUESTIONS.md`
- [ ] Bilingual format maintained (English term | Gurmukhi term)
- [ ] T/L/R/H classification applied (Translated/Loan/Retained/Hybrid)

---

## Translation Classification System (T/L/R/H)

| Code | Type | Example |
|------|------|---------|
| **T** | Translated | Access control → ਪਹੁੰਚ ਕੰਟਰੋਲ |
| **L** | Loan word | Model → ਮਾਡਲ |
| **R** | Retained | OWASP, AISVS, MCP, RAG, LLM (kept as-is) |
| **H** | Hybrid | Prompt injection → prompt ਇੰਜੈਕਸ਼ਨ |

---

## Numerals

Use Western numerals in technical prose, including version numbers: 1.0 (not ੧.੦). See `TRANSLATION-RULES.md` §2.

---

## Reverence Note

Sri Guru Granth Sahib Ji is the eternal Guru and supreme guiding authority for Sikhs. It contains the divine utterances of six Gurus, three Sikhs, fifteen saints, and eleven court poets. Never refer to it as a "scripture" or "book." The Gurmukhi script was institutionalized by Guru Angad Sahib.

---

## Blog Post Structure (SecurityLeader.ai)

When creating blog posts about this translation project for SecurityLeader.ai:

1. Italic hook question after H1
2. Executive Summary blockquote
3. "Your Next Move" section with role-specific CTAs
4. Board talking points + author attribution (Gurvinder Singh, Principal Security Researcher)

Publish workflow: Claude Code → `git push origin main` → Vercel auto-deploy

---

## File Structure

```
1.0/pa-IN/
├── CLAUDE.md                  ← This file (translation rules)
├── TRANSLATION-RULES.md       ← Canonical rule set (forked from ASVS)
├── GLOSSARY.md                ← Shared terminology seeded from ASVS corpus
├── OPEN-QUESTIONS.md          ← AISVS-specific terminology judgment calls
├── 0x01-Frontispiece.md       ← Front matter
├── 0x02-Preface.md            ← Front matter
├── 0x03-Using-AISVS.md        ← Front matter
├── 0x10-C01-Training-Data-Integrity-and-Traceability.md
├── 0x10-C02-Input-Validation.md
├── 0x10-C03-Model-Lifecycle-Management.md
├── 0x10-C04-Infrastructure.md
├── 0x10-C05-Access-Control-and-Identity.md
├── 0x10-C06-Supply-Chain.md
├── 0x10-C07-Model-Behavior.md
├── 0x10-C08-Memory-Embeddings-and-Vector-Database.md
├── 0x10-C09-Orchestration-and-Agentic-Action.md
├── 0x10-C10-MCP-Security.md
├── 0x10-C11-Adversarial-Robustness.md
├── 0x10-C12-Monitoring-and-Logging.md
├── 0x90-Appendix-A_Glossary.md
├── 0x91-Appendix-B_AI_Security_Controls_Inventory.md
└── 0x92-Appendix-C_AI_for_Code_Generation.md
```

Source (English, upstream): `1.0/en/` — cloned from `github.com/OWASP/AISVS`, untouched.

---

## Sentence-ending punctuation (MANDATORY)

Panjabi (Gurmukhi-script) prose uses the **Indic danda `।` (U+0964)** as
sentence terminator — never the Western period `.`. The double-danda
`॥` (U+0965) is reserved for verse separation in Gurbani quotations and
should not be used in technical prose.

### Rule

- Every Panjabi sentence ends with `।` followed by a space or end-of-line
- Sentences that end with a parenthetical also use `।` after the closing
  paren: `(ਜਿਵੇਂ, RFC 6266 ਦੇ ਅਨੁਸਾਰ)।` — not `(ਜਿਵੇਂ, RFC 6266 ਦੇ ਅਨੁਸਾਰ).`
- Bullet-list items and table cells follow the same rule when their content
  is a Panjabi sentence

### Exceptions (Western `.` retained)

- ASCII digits and version numbers: `1.0`, `1.0.0`
- URLs, file extensions, English abbreviations
- English text on lines that contain no Gurmukhi
- Decimal numbers and percentages

### Applied corpus-wide (ASVS precedent)

The ASVS sibling corpus applied this rule in commit `bdda1806` (2026-06-02)
across 8 files, 127 substitutions. AISVS translations must honor this rule
from creation — do not draft Western-period sentences and plan to fix later.
