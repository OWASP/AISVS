<!-- cspell:words pathlib rglob splitlines fullmatch IFS -->

## Lineup

| Step | Model | Job |
| --- | --- | --- |
| 1. Build | Astra (`gpt-6-astra`, through Codex) | Builds one scoped change on a clean branch from `main`; reads requirements before researching and runs the checks below. |
| 2. Second build | Opus 5.5 (`claude-opus-5-5`, through the Claude Code CLI) | Checks Astra's commit against primary sources, fixes mappings and claims, fills scoped gaps, and cuts prose. |
| 3. Review | Sol 6.1 (`gpt-6.1-sol`, through Codex) | Independently checks requirement synchronization, AI-specific scope, verification approaches, tooling support, and level justification. |
| 3. Review | Daybreak Blue (`gpt-daybreak-blue-latest`, through Codex) | Independently checks threat assumptions, attack preconditions, mitigation limits, and bypass claims. |
| 3. Review | Mythos 5.1 (`claude-mythos-5-1`, through the Claude Code CLI) | Independently checks vulnerability records, paper results, statistics, and source conflicts. |
| 3. Review | Sonnet 5.5 (`claude-sonnet-5-5`, through the Claude Code CLI) | Independently reviews concision, placement, and plain US English, preserving evidence qualifications. |
| 4. Decide and ship | Astra (`gpt-6-astra`, through Codex) | Resolves every finding with evidence, checks the final commit, and gives the maintainer a concrete decision, or merges if authorized. |

Use the full lineup for requirement changes and added, removed, or revised research claims. One reviewer suffices for typo or link repairs that leave meaning and source support unchanged.

Confirm the listed IDs are available in the installed CLIs before starting. [Mythos 5.1](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) requires organizational verification through an Anthropic program, such as the Cyber Verification Program.

Use the native Daybreak Blue entry, `gpt-daybreak-blue-latest`, from `codex debug models`; do not substitute another model. [OpenAI describes it](https://developers.openai.com/api/docs/models/gpt-daybreak-blue-latest) as a deprecated alias for general-purpose models with defensive cybersecurity safeguards and lists `gpt-5.6-sol` as its default; the Codex catalog describes the same entry as the latest frontier agentic coding model for defensive cybersecurity work. [Daybreak access requires approval](https://developers.openai.com/api/docs/guides/daybreak). Record the exact ID and any snapshot exposed by the run; otherwise record the snapshot as unknown, without inferring it from the documented default.

1.02 is the only active development release; 2.0 is deferred and `2.0-dev/` has been removed. Requirement changes target `1.02-dev/en/`. `1.0/` and `1.01/` are locked; the [released research sync exception](.github/workflows/lock-released.yml) requires an internal OWASP/AISVS `wiki/sync-*` PR labeled `research-sync` from an owner, member, or collaborator.

`1.02-dev/research/` does not exist yet. If creating it is in scope, seed the latest snapshot as [#1144](https://github.com/OWASP/AISVS/pull/1144) did and carry forward unresolved claims. Copying does not renew source review.

## Review contract

- Follow [AGENTS.md](AGENTS.md), [CONTRIBUTING.md](CONTRIBUTING.md), [RELEASE.md](RELEASE.md), and [Using AISVS](1.02-dev/en/0x03-Using-AISVS.md). Read the existing requirements in detail and consider implicit coverage before proposing additions.
- Give every reviewer the same commit SHA, intent, complete diff, full affected pages, the matching `en/` chapters, and the review status. Keep sessions independent until each returns its findings. Reviewers propose changes without editing the shared branch; Astra applies accepted fixes and sends affected changes back for review.
- Require a **MERGE**, **REQUEST_CHANGES**, or **CLOSE** recommendation with exact locations, evidence, and concrete fixes. Separate new regressions from inherited problems. Agreement between models is not evidence.
- Research pages map each requirement to threats, tooling, verification approaches, and open questions. Quoted requirement text, IDs, and levels must match the same version's `en/` exactly. Research never adds requirements or changes levels.
- Requirement changes must be AI-specific, testable, and justified by current practice, implementation effort, and tooling support at the proposed level; general controls covered by ASVS are not missing. [Minor releases](RELEASE.md#minor-release-for-example-v10-to-v101) may append chapters, sections, and requirements while preserving existing identifiers, placement, chapter and section names, and control objectives. Do not renumber existing requirements or reuse retired identifiers.
- Apply the [research evidence standard](1.01/research/REVIEW-STATUS.md#completion-criteria). Fetch the original source and confirm it says what the claim says; a URL that resolves is not support by itself. Distinguish documented capability from demonstrated effectiveness.
- For attack claims, identify affected components and versions, lifecycle stage, attacker access, knowledge and capabilities, trust boundaries, prerequisites, configuration, security impact, and demonstrated outcome. Preserve evidence type, sample sizes, trial counts, denominators, baselines, and uncertainty; do not generalize beyond tested conditions or infer prevalence from possibility. Do not execute untrusted proofs of concept or probe systems without explicit authorization.
- For mitigation claims, identify the attack step and control layer addressed, deployment assumptions, evaluation conditions and baselines, adaptive-attacker coverage, known bypasses, and residual risk. Check evidence for each claimed layer; vendor documentation, non-adaptive tests, or absent bypass reports do not establish complete protection.
- Check CVE records and vendor/CNA advisories; record check dates, state, disputes, affected versions/configurations, and exploitation evidence. Reserved IDs substantiate no details; rejected IDs are not valid vulnerability identifiers. Record each CVSS source, check date, version, score, and vector; Base scores measure severity, not exploit likelihood or risk. Attribute conflicts rather than choosing silently.
- Correct, qualify, or remove unsupported claims across pages. In the version's `REVIEW-STATUS.md`, record unresolved claims with page, claim, evidence gap, and next step; identify blocked sources, sampling, and stale dates.
- Cut introductions, repetition, and unsupported certainty.

## Local checks

Run in Bash from the repository root after the final commit. Use installed Node.js, Python 3, [lychee](https://lychee.cli.rs/), markdownlint, and cspell; do not auto-download executables during review.

```bash
version=1.02-dev
changed=()
while IFS= read -r -d '' path; do
  changed+=("./$path")
done < <(git diff --name-only -z --diff-filter=d origin/main...HEAD -- '*.md')
if ((${#changed[@]})); then
  markdownlint --config .github/workflows/config/markdownlint.jsonc "${changed[@]}"
  cspell --no-progress --config .github/workflows/config/cspell.json "${changed[@]}"
fi
lychee --offline --include-fragments --no-progress '*.md' "$version/**/*.md"
git diff --check origin/main...HEAD
```

Separate inherited research lint/spelling findings from new ones against `main`. CI lints README and `en/`, and spell-checks root Markdown and `en/`; research pages need local checks.

Compare requirement rows, including Appendix C, with the same version's `en/`; report NOT RUN until research exists.

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

Also check table column counts, requirement counts, Appendix A and B mappings, and incoming links after moves. Inspect CI on the final commit.

## Decide and ship

- Keep one topic per branch and PR. Non-maintainers open an issue first. If the research produces no meaningful addition or correction, recommend against an issue or PR.
- Structure the PR description as Scope, What changed, Validation, and Known limitations. Quote current requirement text where relevant and link the supporting sources.
- Record each reviewer's actual model ID, reviewed SHA, findings, and resolution; mark unusable slots unavailable. Update the version's research `REVIEW-STATUS.md` when present.
- Give the maintainer the verdict, remaining blockers, unresolved claims, and validation results. Post reviews, merge, or close only within the maintainer's authorization.
