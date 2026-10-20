<!-- cspell:words pathlib rglob splitlines fullmatch -->

## Lineup

| Step | Model | Job |
| --- | --- | --- |
| 1. Build | Astra (`gpt-6-astra`, through Codex) | Takes one scoped topic on a clean branch from `main`. Reads the affected requirements before researching, drafts the research or requirement change, and runs the checks below. |
| 2. Second build | Opus 5.5 (`claude-opus-5-5`, through the Claude Code CLI) | Works on Astra's commit. Fetches primary sources, corrects requirement mappings and unsupported claims, fills gaps in the agreed scope, and cuts unnecessary prose. |
| 3. Review | Sol 6.1 (`gpt-6.1-sol`, through Codex) | Independently checks requirement synchronization, AI-specific scope, verification approaches, tooling support, and level justification. |
| 3. Review | Daybreak Blue (`gpt-daybreak-blue-latest`, through Codex) | Independently checks threat assumptions, attack preconditions, mitigation limits, and bypass claims. |
| 3. Review | Mythos 5.1 (`claude-mythos-5-1`, through the Claude Code CLI) | Independently checks difficult technical claims against primary sources: vulnerability records, paper results and test scope, statistics, and conflicting sources. |
| 3. Review | Sonnet 5.5 (`claude-sonnet-5-5`, through the Claude Code CLI) | Independently reviews concision, duplication, placement, and plain US English while preserving evidence qualifications. |
| 4. Decide and ship | Astra (`gpt-6-astra`, through Codex) | Resolves every finding with evidence, checks the final commit, and gives the maintainer a concrete decision, or merges if authorized. |

Use the full lineup for substantial research and requirement changes; use focused review for small corrections.

Model IDs were checked on October 20, 2026 against `codex debug models`, the Claude Code CLI, and the [OpenAI](https://developers.openai.com/api/docs/models) and [Claude](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) model documentation. Before starting, confirm the latest version of each family is available, record its exact model ID, and report unavailable reviewers explicitly. Mythos 5.1 requires Anthropic's [Cyber Verification Program](https://support.claude.com/en/articles/14604842), and Daybreak Blue requires [Daybreak](https://openai.com/daybreak/) access.

Daybreak Blue is the Codex catalog entry for `gpt-daybreak-blue-latest`. OpenAI [marks this alias deprecated](https://developers.openai.com/api/docs/models/gpt-daybreak-blue-latest) and says to use the latest cyber model available to the account. Use the newest cyber model in `codex debug models`, record its ID, and note that Codex does not report which snapshot an alias resolved to.

1.02 is the next and only planned release; 2.0 work is on hold. Requirement changes go in `1.02-dev/en/`. `1.02-dev/research/` does not exist yet. If creating it is in scope, seed it from the latest snapshot as [#1144](https://github.com/OWASP/AISVS/pull/1144) did, then synchronize requirements and carry forward the unresolved claims. Copying a snapshot does not renew its source review.

## Review contract

- Follow [AGENTS.md](AGENTS.md), [CONTRIBUTING.md](CONTRIBUTING.md), [RELEASE.md](RELEASE.md), and [Using AISVS](1.02-dev/en/0x03-Using-AISVS.md). Read the existing requirements in detail and consider implicit coverage before proposing additions.
- Give every reviewer the same commit SHA, intent, complete diff, full affected pages, the matching `en/` chapters, and the review status. Keep sessions independent until each returns its findings. Reviewers propose changes without editing the shared branch; Astra applies accepted fixes and sends affected changes back for review. Earlier reviews do not cover later edits.
- Require a **MERGE**, **REQUEST_CHANGES**, or **CLOSE** recommendation with exact locations, evidence, and concrete fixes. Separate new regressions from inherited problems. Agreement between models is not evidence.
- Research pages map each requirement to threats, tooling, verification approaches, and open questions. Quoted requirement text, IDs, and levels must match the same version's `en/` exactly. Research never adds requirements or changes levels.
- AISVS covers AI-specific concerns and complements ASVS and similar standards; a general control is not missing because AISVS omits it. A requirement change must be testable and backed by research on current practice, implementation effort, and tooling support that justifies its level. Minor releases keep the chapter and section structure.
- Apply the [research evidence standard](1.01/research/REVIEW-STATUS.md#completion-criteria). Fetch the original source and confirm it says what the claim says; a resolving URL is not support. Check the publication date and the population or test scope, and keep wording within the evidence. Separate forecasts, vendor claims, observed incidents, and controlled experiments, and distinguish documented capability from demonstrated effectiveness. "Checked" means matched to the publisher's material, not independently validated. Source review does not require reproducing exploits.
- Record source conflicts, such as CNA, NVD, and GitHub CVSS differences, with attribution instead of picking one. Describe reserved CVE IDs as reserved and unpublished as of the check date; a reservation does not substantiate vulnerability details.
- Correct, qualify, or remove unsupported assertions, and fix repeated occurrences across pages. List unresolved claims in the version's `REVIEW-STATUS.md` with page, claim, evidence gap, and next step so they do not read as checked. Record blocked sources, sampled claim classes, and stale "as of" statements.
- Cut introductions, repetition, and unsupported certainty. Report word counts before and after substantial rewrites.

## Local checks

Run from the repository root after the last content change. These need Node.js, Python 3, and [lychee](https://lychee.cli.rs/).

```bash
version=1.02-dev
changed=$(git diff --name-only --diff-filter=d origin/main...HEAD -- '*.md')
npx --yes markdownlint-cli --config .github/workflows/config/markdownlint.jsonc $changed
npx --yes cspell --no-progress --config .github/workflows/config/cspell.json $changed
lychee --offline --include-fragments --no-progress '*.md' "$version/**/*.md"
git diff --check origin/main...HEAD
```

Research pages carry inherited lint and spelling findings, so compare against `main` and report only new ones. CI lints README and `en/`, and spell-checks root Markdown and `en/`; it does not check research pages.

Compare requirement rows, including Appendix C, with the same version's `en/`. Until research is seeded for the version, report this check as not run.

```bash
python3 - "$version" <<'PY'
import re, sys
from pathlib import Path

version = Path(sys.argv[1])
if not (version / "research").is_dir():
    sys.exit("NOT RUN: no research folder")

def rows(folder):
    found = set()
    for path in folder.rglob("*.md"):
        for line in path.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)]
            if len(cells) >= 5 and re.fullmatch(r"\*\*(\d+\.\d+\.\d+|AC\.\d+\.\d+)\*\*", cells[1]):
                found.add(tuple(cells[1:4]))
    return found

standard, research = rows(version / "en"), rows(version / "research")
for row in sorted(standard - research):
    print("Missing or changed in research:", row)
for row in sorted(research - standard):
    print("Not in en/:", row)
sys.exit(not standard or standard != research)
PY
```

Also check table column counts, requirement counts, Appendix A and B mappings, and incoming links after moves. Inspect CI on the final commit. Passing checks does not establish source support.

## Decide and ship

- Keep one topic per branch and PR. Non-maintainers open an issue first. If the research produces no meaningful addition or correction, recommend against an issue or PR.
- Structure the PR description as Scope, What changed, Validation, and Known limitations, as in [#1184](https://github.com/OWASP/AISVS/pull/1184) and [#1185](https://github.com/OWASP/AISVS/pull/1185). Quote current requirement text where relevant and link the supporting sources.
- Record each reviewer's actual model, reviewed SHA, findings, and resolution, including unavailable reviews. Update `REVIEW-STATUS.md` with completed work and remaining limitations.
- `1.0/` and `1.01/` are locked. Released research changes only through the [research sync path](.github/workflows/lock-released.yml): an internal `wiki/sync-*` PR labeled `research-sync` from an owner, member, or collaborator.
- Give the maintainer the verdict, remaining blockers, unresolved claims, and validation results. Post reviews, merge, or close only within the maintainer's authorization.
