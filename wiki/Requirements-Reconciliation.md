# AISVS Wiki Requirements Reconciliation Report

**Date:** 2026-03-28
**Source of truth:** [`OWASP/AISVS/1.0/en`](https://github.com/OWASP/AISVS/tree/main/1.0/en) (main branch)
**Wiki:** [`OWASP/AISVS` wiki](https://github.com/OWASP/AISVS/wiki) (this folder)

---

## Executive Summary

The wiki is **in sync** with the source requirements. All 454 chapter requirements and 30 Appendix C requirements (484 total) in the source repo are present in the corresponding wiki pages. No requirement IDs are missing, added, or renumbered in the wiki relative to the source.

One anomaly was identified: PR #602 (commit `162ddd9`) claims to add requirement **8.2.6** (Summarization Security) but the PR merged with **zero file changes** -- the requirement does not exist in either the source repo or the wiki.

---

## Requirement Counts by Chapter

| Chapter | Source | Wiki | Match |
|---------|-------:|-----:|:-----:|
| C1 Training Data | 24 | 24 | Yes |
| C2 User Input Validation | 33 | 33 | Yes |
| C3 Model Lifecycle Management | 26 | 26 | Yes |
| C4 Infrastructure | 46 | 46 | Yes |
| C5 Access Control & Identity | 27 | 27 | Yes |
| C6 Supply Chain | 34 | 34 | Yes |
| C7 Model Behavior | 33 | 33 | Yes |
| C8 Memory & Embeddings | 25 | 25 | Yes |
| C9 Orchestration & Agents | 40 | 40 | Yes |
| C10 MCP Security | 33 | 33 | Yes |
| C11 Adversarial Robustness | 41 | 41 | Yes |
| C12 Privacy | 23 | 23 | Yes |
| C13 Monitoring & Logging | 45 | 45 | Yes |
| C14 Human Oversight | 24 | 24 | Yes |
| **Chapter subtotal** | **454** | **454** | **Yes** |
| Appendix C (AI Secure Coding) | 30 | 30 | Yes |
| **Grand total** | **484** | **484** | **Yes** |

---

## Section-Level Coverage

### Chapters with dedicated wiki sub-pages (8 of 14)

These chapters have both a chapter-level overview page and per-section deep-dive pages in the wiki.

| Chapter | Source sections | Wiki sub-pages | Match |
|---------|:--------------:|:--------------:|:-----:|
| C2 | 8 (2.1-2.8) | 8 | Yes |
| C4 | 8 (4.1-4.8) | 8 | Yes |
| C6 | 7 (6.1-6.7) | 7 | Yes |
| C7 | 8 (7.1-7.8) | 8 | Yes |
| C9 | 8 (9.1-9.8) | 8 | Yes |
| C10 | 6 (10.1-10.6) | 6 | Yes |
| C11 | 10 (11.1-11.10) | 10 | Yes |
| C13 | 7 (13.1-13.7) | 7 | Yes |

### Chapters without wiki sub-pages (6 of 14)

These chapters have only the chapter-level wiki page. All requirements are present in the chapter page, but no per-section deep-dive pages exist.

| Chapter | Source sections | Notes |
|---------|:--------------:|-------|
| C1 | 5 (1.1-1.5) | No sub-pages |
| C3 | 5 (3.1-3.5, 3.7; no 3.6) | No sub-pages |
| C5 | 6 (5.1-5.6) | No sub-pages |
| C8 | 5 (8.1-8.5) | No sub-pages |
| C12 | 6 (12.1-12.6) | No sub-pages |
| C14 | 7 (14.1-14.7) | No sub-pages |

### Appendices

| Appendix | Source | Wiki | Match |
|----------|:------:|:----:|:-----:|
| A -- Glossary | Yes | Yes | Yes |
| B -- References | Yes | Yes | Yes |
| C -- AI Secure Coding (30 reqs) | Yes | Yes | Yes |
| D -- Controls Inventory | Yes | Yes | Yes |

---

## Anomalies

### 1. Ghost requirement 8.2.6 (Summarization Security)

- **PR:** [#602](https://github.com/OWASP/AISVS/pull/602) -- merged 2026-03-29
- **Commit:** `162ddd9` "feat(C8): add 8.2.6 summarization security (OASB 8.4)"
- **Problem:** The PR was merged with zero file changes. Requirement 8.2.6 does not appear in the source chapter file (`0x10-C08-Memory-Embeddings-and-Vector-Database.md`) or the wiki page (`C08-Memory-and-Embeddings.md`).
- **Impact:** The git log implies 8.2.6 exists, but it was never added to any file. This should be resolved by either adding the requirement content or reverting the empty commit.

### 2. Section numbering gap in C3

- C3 has no section 3.6 (jumps from 3.5 to 3.7). This is **intentional** in the source and correctly reflected in the wiki.

### 3. Inconsistent sub-page coverage

- 8 of 14 chapters have per-section wiki sub-pages with expanded guidance (threat landscape, tooling, implementation notes, research questions).
- 6 chapters (C1, C3, C5, C8, C12, C14) lack sub-pages entirely.
- This is a wiki completeness gap, not a requirements gap -- the requirement tables are present in all chapter-level pages.

---

## Methodology

1. Extracted all requirement IDs from the source repo via `gh api` (GitHub Contents API), parsing bold-formatted IDs (`**X.Y.Z**`) from markdown table rows in each chapter file.
2. Extracted all requirement IDs from wiki chapter files using regex matching against the same ID format.
3. Compared requirement ID sets per chapter for additions, deletions, and mismatches.
4. Verified section-level wiki sub-pages against source section headings.
5. Checked appendix presence in both source and wiki.
6. Investigated commit history for recent changes (specifically PR #602 / commit `162ddd9`).
