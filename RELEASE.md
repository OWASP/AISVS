# AISVS Release Policy

AISVS addresses a fast-moving technology, so it has to update more often than most security standards. At the same time, adopters, auditors, and tooling vendors need stable identifiers they can cite. This document defines the release model that balances those two goals.

## Current Release Plan

**1.02 is the only active development release.** All new work targets `1.02-dev/`. Version 2.0 is deferred, and its `2.0-dev/` folder has been removed. The released `1.0/` and `1.01/` folders remain locked.

Version 1.02 may add chapters, sections, and requirements while preserving the numbering and organization of existing requirements. Proposals are reviewed for scope, evidence, and testability before inclusion; targeting 1.02 does not guarantee inclusion in that release.

## Versioning Scheme

AISVS uses a two-part version number:

```text
v<MAJOR>.<MINOR>
```

Examples: `v1.0`, `v1.01`, `v1.02`, `v2.0`, `v2.01`.

- **MAJOR** changes when existing chapters or sections are removed, renamed, or restructured, existing requirements are moved or renumbered, or existing control objectives change.
- **MINOR** changes when requirements are added, retired, or materially modified, or new chapters or sections are appended without changing the numbering or organization of existing requirements.

The public AISVS version that adopters, auditors, and tooling cite is always two-part. Patch-level fixes (typos, link corrections, language polish that does not change a requirement's meaning) are applied directly to the in-progress minor and do not produce a separate public version number. The next minor release rolls them up.

> **Why two parts instead of three.** AISVS identifiers like `v1.0-C9.4.3` already encode the version that owns the requirement ID. A three-part scheme would push patch-level noise into citations without changing what the identifier means. Two parts keep the public surface simple and stable for downstream users.

## Scope Rules by Change Type

### Patch fix (in-branch, no version bump)

Allowed:

- Typo and grammar fixes.
- Broken or relocated reference links.
- Editorial clarifications that do not change which evidence an auditor would request or accept.

Not allowed:

- Changing the verifiable condition of a requirement.
- Changing a requirement's level.
- Adding or removing requirements.

### Minor release (for example, `v1.0` to `v1.01`)

Allowed:

- Adding new requirements within an existing section.
- Appending new chapters and sections with new identifiers, preserving existing chapter and section names, control objectives, and requirement placement.
- Retiring requirements that are obsolete, duplicated, or superseded, leaving their identifiers marked as removed rather than reusing them or renumbering later requirements.
- Materially modifying requirement text, including level changes, when the change reflects evolving technology or threat landscape.
- All patch-level changes accumulated since the previous minor.

Not allowed:

- Removing, renaming, or reorganizing existing chapters or sections.
- Moving or renumbering existing requirements, or reusing retired identifiers.
- Changing an existing chapter's control objective.

Assign additions the next unused identifier at the end of the relevant chapter, section, or requirement sequence. For example, a new chapter after C12 becomes C13; existing chapters and their requirements retain their identifiers and placement.

These limits preserve the chapter and section identity encoded by `v<version>-Cx.y.z`. New coverage can be added without reorganizing existing material. Requirement text and levels may still change between minor releases, so assessments must cite the version they use.

### Major release (for example, `v1.x` to `v2.0`)

Allowed:

- Anything a minor release allows.
- Adding, removing, or restructuring chapters and sections.
- Revising control objectives.
- Renumbering requirements where structural change requires it.

A major release is the only release type that can break the meaning of existing identifiers, so it must be the only release type that does.

## Cadence

- **Minor releases ship as the content requires.** There is no fixed calendar. If a class of AI attack or defense is established enough to specify and test, it lands in the next minor. Patch-level editorial fixes ship continuously into the in-progress minor.
- **Major releases ship when warranted, not on a schedule.** If a chapter-level rethink is needed, a new major version is preferable to overloading minor releases with breaking changes.

## Parallel Maintenance

Version 2.0 is deferred; there is no active parallel major-version development. If a future major release is opened:

- The previous major line continues to receive minor releases and in-branch patch fixes for a defined maintenance period announced at the time the next major opens.
- Adopters and auditors targeting the previous major are not forced to migrate before the maintenance period ends.
- After the maintenance period, the previous major line is locked. Identifiers remain citable, but no further changes are made.

The intent is that organizations should never be in a position where the only supported AISVS version requires a structural migration of their existing compliance work.

## Repository Layout

Each released minor version lives in its own folder. Once a version is released its folder is locked, and the next version is opened in a new folder with a `-dev` suffix:

```text
/
├── 1.0/         <- released (locked)
├── 1.01/        <- released (locked)
├── 1.02-dev/    <- next minor release in progress
```

Only `1.02-dev/` is currently open for development. A future major release may receive a separate `-dev` folder when maintainers explicitly resume that work; contributors should not create or target `2.0-dev/` while 2.0 is deferred.

## Referencing Across Versions

For citing requirements in reports, tools, audits, or other documents, use the full versioned form:

```text
v<version>-C<chapter>.<section>.<requirement>
```

For example, `v1.0-C9.4.3`. The unversioned form `C9.4.3` resolves to the latest released minor, which works for casual reference but should be avoided in anything that needs to remain stable across versions. See [How to Reference AISVS Requirements](https://github.com/OWASP/AISVS#how-to-reference-aisvs-requirements) in the README for the full convention.
