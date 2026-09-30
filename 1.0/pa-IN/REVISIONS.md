# pa-IN revision log

## 2026-09-30 revision (v0.1 draft, not certified)

Source of revisions: locked styleguide from the ASVS V6 manual review (Sept 28-29, 2026), applied to all 18 AISVS pa-IN files. Certification status is unchanged. Machine-assisted output stays at v0.1 until human (Sangat and academic) review.

### Changes applied
1. **Control-head verb:** `ਤਸਦੀਕ ਕਰੋ ਕਿ` -> `ਜਾਂਚ ਕਰੋ ਕਿ` (263 uses).
2. **Security "compromise":** `ਸਮਝੌਤਾ` (primary sense "agreement", OPEN-QUESTIONS Q19) -> `ਭੇਦੀ ਹੋ-` forms (13 uses). The locked term is `ਭੇਦੀ ਹੋ ਗਿਆ` (breach). Inflected noun and adjective forms (`ਭੇਦੀ ਹੋਣ`, `ਭੇਦੀ ਹੋਏ`) are proposed and need reviewer confirmation.
3. `GLOSSARY.md`, `TRANSLATION-RULES.md` and `tools/lint-terminology.py` updated so the old forms cannot return.
4. Print-edition markdown mirrored with the same replacements. **The PDF must be rebuilt** with `print/build-print-pdf.sh`.

### Per-file counts (before revision)
| File | ਤਸਦੀਕ ਕਰੋ -> ਜਾਂਚ ਕਰੋ | ਸਮਝੌਤ- -> ਭੇਦੀ ਹੋ- |
|---|---|---|
| `0x01-Frontispiece.md` | 0 | 0 |
| `0x02-Preface.md` | 0 | 0 |
| `0x03-Using-AISVS.md` | 1 | 0 |
| `0x10-C01-Training-Data-Integrity-and-Traceability.md` | 13 | 1 |
| `0x10-C02-Input-Validation.md` | 12 | 0 |
| `0x10-C03-Model-Lifecycle-Management.md` | 15 | 1 |
| `0x10-C04-Infrastructure.md` | 14 | 0 |
| `0x10-C05-Access-Control-and-Identity.md` | 11 | 0 |
| `0x10-C06-Supply-Chain.md` | 7 | 1 |
| `0x10-C07-Model-Behavior.md` | 13 | 0 |
| `0x10-C08-Memory-Embeddings-and-Vector-Database.md` | 11 | 0 |
| `0x10-C09-Orchestration-and-Agentic-Action.md` | 34 | 1 |
| `0x10-C10-MCP-Security.md` | 23 | 0 |
| `0x10-C11-Adversarial-Robustness.md` | 17 | 0 |
| `0x10-C12-Monitoring-and-Logging.md` | 21 | 0 |
| `0x90-Appendix-A_Glossary.md` | 0 | 0 |
| `0x91-Appendix-B_AI_Security_Controls_Inventory.md` | 3 | 2 |
| `0x92-Appendix-C_AI_for_Code_Generation.md` | 68 | 7 |

### Open items needing a decision (not applied)
- **Numerals:** the locked ASVS styleguide uses Gurmukhi numerals for section and control references. AISVS rules (2.2, 2.3) keep Western digits and English requirement IDs so `v1.0-Cx.y.z` citations and the ID-completeness lint keep working.
- **Register:** AISVS rules say formal academic Panjabi. The locked styleguide says colloquial over academic. Moving the register is a chapter-by-chapter retranslation pass, not a find-and-replace.
- **Verb precision:** `ਜਾਂਚ ਕਰੋ` now covers "verify" and is also used for "check" in 20 places. Review those 20 uses so the two stay distinct.
