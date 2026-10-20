## Lineup

| Step | Model | Job |
| --- | --- | --- |
| 1. Build | Astra (`gpt-6-astra`, through Codex) | Takes one scoped topic on a clean branch from `main`. Reads the standard before researching, drafts research or justified requirement changes, and runs checks. |
| 2. Second build | Opus 5.5 (`claude-opus-5-5`, through the Claude Code CLI) | Checks primary sources, corrects requirement mappings and unsupported claims, fills agreed gaps, and cuts unnecessary prose. |
| 3. Review | Sol 6.1 (`gpt-6.1-sol`, through Codex) | Independently checks requirement synchronization, AI-specific scope, verification approaches, tooling support, and level justification. |
| 3. Review | Daybreak Blue (Codex CLI access program; current model required) | Independently checks threat assumptions, mitigation limits, and bypass claims when eligible account access permits. |
| 3. Review | Mythos 5.1 (`claude-mythos-5-1`, through the Claude Code CLI) | Independently checks difficult technical claims, vulnerability records, experimental scope, and conflicting sources. |
| 3. Review | Sonnet 5.5 (`claude-sonnet-5-5`, through the Claude Code CLI) | Independently reviews concision, duplication, placement, and plain US English while preserving evidence qualifications. |
| 4. Decide and ship | Astra (`gpt-6-astra`, through Codex) | Resolves findings with evidence, checks the final commit, and presents a decision or merges within the maintainer's authorization. |

Use the full lineup for substantial research and requirement changes; use focused review for small corrections. Before starting, confirm the latest version of each selected family against installed CLIs and official documentation, verify access, and record exact model IDs. Report unavailable reviewers explicitly.

Daybreak Blue is an access program, not a model. Record both the eligible current model and program. General model availability does not establish program eligibility; a deprecated alias without a resolved current model does not satisfy this review.

1.02 is the next and only planned release; 2.0 work is on hold. Target requirement changes at `1.02-dev/en/`. There is no `1.02-dev/research/` yet. If creating it is in scope, seed from the previous snapshot, following the approach in [#1144](https://github.com/OWASP/AISVS/pull/1144), then synchronize requirements and carry forward unresolved claims. Copying a snapshot does not renew its source review.

## Review contract

- Follow [AGENTS.md](AGENTS.md), [CONTRIBUTING.md](CONTRIBUTING.md), [RELEASE.md](RELEASE.md), and [Using AISVS](1.02-dev/en/0x03-Using-AISVS.md). Confirm the release and topic. Read existing requirements in detail before researching; consider implicit coverage before proposing additions.
- Give reviewers the same commit SHA, intent, complete diff, full affected pages, corresponding `en/` material, and review status. Keep sessions independent until findings return. Reviewers propose changes without editing the shared branch; Astra applies fixes and requests review of affected changes.
- Require **MERGE**, **REQUEST_CHANGES**, or **CLOSE**, with locations, evidence, and concrete fixes. Separate regressions from inherited problems. Earlier reviews do not automatically cover later edits; model agreement is not evidence.
- Research chapter, section, and appendix pages map requirements to threats, tooling, verification approaches, and open questions. Quoted requirement text, IDs, and levels must match the same version's `en/` exactly. Research never adds requirements or changes levels.
- AISVS covers AI-specific concerns and complements ASVS and other standards. General security controls are not missing merely because AISVS omits them. Requirement changes need a distinct, testable correction supported by current practice, implementation feasibility, tooling support, and the proposed level. Preserve the minor release's chapter and section structure.
- Apply the [research evidence standard](1.01/research/REVIEW-STATUS.md#completion-criteria): fetch the original source, check publication date and population or test scope, and make wording follow evidence. Separate forecasts, vendor claims, observed incidents, and controlled experiments. “Checked” means matched to the publisher's material, not independently validated or endorsed. Technical source review does not require reproducing exploits.
- Record source conflicts, including CNA, NVD, and GitHub CVSS differences, with attribution rather than guessing a single answer. Identify reserved CVE IDs as reserved and unpublished as of the check date; reservation alone does not substantiate vulnerability details.
- Correct, qualify, or remove unsupported assertions. List unresolved claims in the version's `REVIEW-STATUS.md`, with page, claim, evidence gap, and next step; do not leave them looking checked. Record blocked sources, sampling limits, and stale “as of” claims. Check repeated occurrences across pages.
- Cut introductions, repetition, and unsupported certainty. Keep tooling examples vendor-neutral and distinguish documented capability from demonstrated effectiveness. Report before-and-after word counts for substantial rewrites.

## Local checks

Run from the repository root in Bash after the final content change. These commands require Node.js/npm, Python 3, and [lychee](https://lychee.cli.rs/recipes/anchors/). They check root Markdown, the target standard, and research when present.

```bash
version=1.02-dev
docs=('*.md' "$version/en/**/*.md")
if [ -d "$version/research" ]; then
  docs+=("$version/research/**/*.md")
fi

npx --yes markdownlint-cli \
  --config .github/workflows/config/markdownlint.jsonc "${docs[@]}"
npx --yes cspell \
  --config .github/workflows/config/cspell.json "${docs[@]}"
lychee --offline --include-fragments "${docs[@]}"
git diff --check
git diff --check origin/main...HEAD
```

Compare requirement rows, including Appendix C, against the same version's `en/`. This ignores cell padding and identical repeated rows, preserving quoted text, IDs, and levels.

```bash
python3 - "$version" <<'PY'
from pathlib import Path
import re
import sys

version = Path(sys.argv[1])
if not (version / "research").is_dir():
    sys.exit("NOT RUN: no research directory; synchronization is unverified.")

def rows(folder):
    result = set()
    for path in folder.rglob("*.md"):
        for line in path.read_text(encoding="utf-8").splitlines():
            cells = [s.strip() for s in re.split(r"(?<!\\)\|", line)]
            if len(cells) >= 5 and re.fullmatch(
                r"\*\*(?:\d+\.\d+\.\d+|AC\.\d+\.\d+)\*\*", cells[1]
            ):
                result.add(tuple(cells[1:4]))
    return result

standard, research = rows(version / "en"), rows(version / "research")
if not standard or not research:
    sys.exit("FAIL: no requirement rows found.")
for row in sorted(standard - research):
    print("Missing or changed in research:", row)
for row in sorted(research - standard):
    print("Extra or changed in research:", row)
sys.exit(standard != research)
PY
```

Also inspect table columns, requirement counts, appendix mappings, prose quotations, and incoming links after moves. Report inherited findings separately. Until research is seeded, report synchronization as not run.

CI spell-checks `en/` and root Markdown, not research pages. Markdown lint CI covers README and `en/`; run research checks explicitly. Inspect final-commit CI and record tool versions and check scope. Passing checks does not establish source support.

## Decide and ship

- Keep one topic per branch and PR. Non-maintainers open an issue first. If research yields no meaningful addition or correction, recommend no issue or PR.
- Use **Scope / What changed / Validation / Known limitations**, following [#1184](https://github.com/OWASP/AISVS/pull/1184) and [#1185](https://github.com/OWASP/AISVS/pull/1185). Identify the version and affected pages; quote current requirements where applicable, explain revisions, and link supporting research.
- Record each reviewer's actual model, reviewed SHA, findings, and resolution, including unavailable reviews. Update review status with completed work and remaining limitations. Contributors remain responsible for every submitted claim.
- `1.0/` and `1.01/` are locked. Released requirements and rendered output remain immutable. Released research corrections require the [trusted synchronization path](.github/workflows/lock-released.yml): an internal `OWASP/AISVS` PR from `wiki/sync-*`, labeled `research-sync`, authored by an owner, member, or collaborator.
- Present the verdict, blockers, unresolved claims, and validation results. Obtain maintainer acceptance of the research review; post reviews, merge, or close only within the maintainer's authorization.