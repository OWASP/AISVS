---
name: update-wiki
description: Research and update one AISVS research wiki page. Picks the stalest page from the rotation tracker, reads the corresponding AISVS chapter source, web-searches for recent threats/tools/incidents, updates the wiki page with per-requirement research context, and commits.
user-invocable: true
allowed-tools: Agent, Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# Update AISVS Research Wiki

You are a research agent that keeps the AISVS research wiki comprehensive and current. You update one wiki page per invocation using the AISVS chapter source and web research.

**Wiki root:** `wiki/` (relative to repository root)
**AISVS source:** `1.0/en/` (relative to repository root)
**Tracker:** `wiki/.update-tracker.json` (relative to repository root)

All paths in this skill are relative to the repository root. Use the current working directory or determine the repo root via `git rev-parse --show-toplevel`.

## Context

This is the OWASP AI Security Verification Standard (AISVS) research wiki. Each wiki page corresponds to a chapter or section of the standard and provides research context for every requirement: what threat it mitigates, how to verify it, what tools exist, and what gaps remain.

The wiki is AI-generated and experimental. Content must be clearly substantive and technically accurate.

## Arguments

- No arguments: update the stalest page (oldest `last_updated` in tracker)
- `<filename>`: update that specific page (e.g., `C02-User-Input-Validation.md`)
- `--dry-run`: print the target page and what would be researched, then stop

Parse `$ARGUMENTS` to determine which mode to use.

## Page Types

There are two types of wiki pages:

1. **Single-page chapters** (≤25 requirements): One page covers the entire chapter with all requirements in per-section tables. Examples: C01, C03, C05, C08, C12, C14.

2. **Split chapters** (>25 requirements): An index page links to individual section pages. The index page has the chapter overview; each section page has the full requirement tables with research. Examples: C02, C04, C06, C07, C09, C10, C11, C13.

When updating a split chapter's index page, also check if its section pages exist. If they don't, create them. When updating a section page, focus research narrowly on that section's topic.

## Requirement Table Format

Every requirement must appear in a research table:

```markdown
| # | Requirement | Level | Role | Threat Mitigated | Verification Approach | Gaps / Notes |
|---|-------------|:-----:|:----:|-----------------|----------------------|--------------|
| X.Y.Z | Verify that ... | 1/2/3 | D/V/D/V | Specific attack or failure mode | Concrete audit steps, tools, checks | Tooling maturity, open issues, caveats |
```

**Research column guidelines:**
- **Threat Mitigated**: Name the specific attack technique, failure mode, or risk. Reference MITRE ATLAS technique IDs, OWASP LLM Top 10 entries, or known incidents where possible.
- **Verification Approach**: Describe what an auditor would actually do — review logs, test with specific tools, inspect configurations, run specific commands. Name real tools.
- **Gaps / Notes**: Be honest about tooling maturity. Flag areas where no good tooling exists, where requirements are hard to test, or where the state of the art is still evolving.

## Research Approach

**Research execution model:** Use the Agent tool with subagent_type "general-purpose" to run deep research in parallel. Launch **3–4 research agents simultaneously**, each with a narrow scope:

1. **Threats & attacks** — recent CVEs, published attacks, MITRE ATLAS techniques, real-world incidents relevant to this section's requirements
2. **Defensive tools & implementation** — libraries, frameworks, cloud services, open-source tools that help implement or verify these controls. Fetch actual documentation, not just titles.
3. **Standards & compliance** — OWASP, NIST, MITRE ATLAS, EU AI Act, ISO 42001 guidance relevant to these specific requirements

Each agent should run **at least 3 WebSearch queries** and **fetch at least 2 full pages** via WebFetch.

**Content priorities:**
- Defense-first: lead with how to implement/verify, not just what the threat is
- Name specific tools with versions where possible
- Include real MITRE ATLAS technique IDs (e.g., AML.T0010)
- Reference real incidents and papers (with dates)
- Be honest about gaps — "no mature tooling exists" is valuable information

**Depth targets per page update:**
- Every requirement must have substantive content in all 3 research columns (not placeholders like "TBD")
- Include at least 1 Notable Incidents entry with date, description, and link
- Fill in Implementation Maturity ratings for each section
- Populate Cross-Chapter Links where requirements overlap with other chapters

## Workflow

### Step 1 — Select the target page

Read `.update-tracker.json` from the wiki root. Find the page with the oldest `last_updated` date (or null = never updated). If `$ARGUMENTS` names a specific `.md` file, use that instead.

If the tracker doesn't exist, create it by scanning all `.md` files in the wiki directory (excluding README.md). Initialize all pages with `last_updated: null, update_count: 0`.

If `--dry-run`, print the selected page and stop.

### Step 2 — Read the source

1. Read the target wiki page in full
2. Read the corresponding AISVS chapter source file from `1.0/en/` to get the exact requirement text, levels, and roles
3. Identify which requirements are missing research content or have placeholder text ("TBD", empty cells)

**Source file mapping:**
- `C01-Training-Data.md` → `0x10-C01-Training-Data-Integrity-and-Traceability.md`
- `C02-User-Input-Validation.md` → `0x10-C02-User-Input-Validation.md`
- `C02-01-*.md` through `C02-08-*.md` → same source, specific section
- Pattern: chapter files are `0x10-CXX-*.md`, appendices are `0x9X-Appendix-*.md`
- Section pages (e.g., `C04-01-Runtime-Environment-Isolation.md`) map to the same chapter source — extract only the relevant section

### Step 3 — Research

Run parallel research agents focused on the specific topic of the target page. See Research Approach above.

**Adaptive strategy:** Check the tracker's quality history:
- **low_yield_streak >= 2:** Try fundamentally different search strategies
- **Mature page (page_lines > 500):** Focus on improving existing content rather than adding new sections
- **No quality history:** Standard approach

### Step 4 — Update the page

Use Edit to modify the wiki page. Rules:

- **Preserve existing structure** — don't remove sections, add to them
- **All requirements must be present** — cross-check against the chapter source
- **No placeholders** — every research cell must have substantive content
- **All URLs must be `https://`**
- **No marketing language or unsubstantiated claims**
- **Date-stamp significant additions** (e.g., "As of March 2026, ...")

**If a page needs splitting** (>25 requirements and currently a single page):
1. Convert the main page to an index with links to section pages
2. Create section pages with the full requirement tables
3. Each section page gets its own intro, research questions, and references

### Step 4.5 — Self-assessment

1. Run `git diff --numstat` on changed files to measure lines added/removed
2. Count new `https://` URLs introduced
3. Get total page lines via `wc -l`
4. **Skip-if-empty:** If `lines_added < 5` and only the date changed, skip the page commit. Still update the tracker.
5. Record strategy labels and yield for the tracker

### Step 5 — Update the tracker

Read `.update-tracker.json`, then write it back with:
- Target page's `last_updated` set to current date (YYYY-MM-DD)
- Target page's `update_count` incremented by 1
- `last_run` set to today's date
- `total_runs` incremented by 1
- Quality metrics:
  ```json
  "quality": {
    "lines_added": <from git diff>,
    "lines_removed": <from git diff>,
    "refs_added": <count of new URLs>,
    "page_lines": <from wc -l>,
    "low_yield_streak": <0 if lines_added >= 15, else previous + 1>,
    "last_strategies": ["threats", "tools", "standards"],
    "last_strategies_yield": [10, 25, 8],
    "last_summary": "<one-line summary>"
  }
  ```

### Step 6 — Commit

```bash
cd "$(git rev-parse --show-toplevel)"
git add wiki/<changed-files> wiki/.update-tracker.json
git commit -m "wiki: update <page-name> research content"
```

- Only stage wiki files and the tracker
- Do NOT push — the user will handle PRs and merging
- If skip-if-empty, commit only the tracker with message: `"wiki: tracker updated for <page-name> (no new content)"`

### Step 7 — Summary

Print:
- Which page was updated
- How many requirements now have full research content
- Key findings incorporated (threats, tools, incidents)
- Quality metrics: lines added/removed, refs added, total page lines
- Low yield streak value
- Strategies used and their yield
