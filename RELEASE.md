# AISVS Release Policy

AISVS addresses a fast-moving technology, so it has to update more often than most security standards. At the same time, adopters, auditors, and tooling vendors need stable identifiers they can cite. This document defines the release model that balances those two goals.

## Versioning Scheme

AISVS uses a two-part version number:

```
v<MAJOR>.<MINOR>
```

Examples: `v1.0`, `v1.01`, `v1.02`, `v2.0`, `v2.01`.

- **MAJOR** changes when chapters or sections are added, removed, restructured, or when control objectives change.
- **MINOR** changes when requirements are added, removed, or materially modified within the existing chapter and section structure.

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
- Removing requirements that are obsolete, duplicated, or superseded.
- Materially modifying requirement text, including level changes, when the change reflects evolving technology or threat landscape.
- All patch-level changes accumulated since the previous minor.

Not allowed:

- Adding, removing, or renaming chapters.
- Adding, removing, or renaming sections within a chapter.
- Changing a chapter's control objective.

These limits exist because the `v<version>-Cx.y.z` referencing convention encodes chapter and section identity. If a minor release reshapes what `C9.4` means, every downstream citation against the previous minor becomes ambiguous without a major-version signal.

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

When work begins on the next major version (for example, `v2.0`):

- The previous major line continues to receive minor releases and in-branch patch fixes for a defined maintenance period announced at the time the next major opens.
- Adopters and auditors targeting the previous major are not forced to migrate before the maintenance period ends.
- After the maintenance period, the previous major line is locked. Identifiers remain citable, but no further changes are made.

The intent is that organizations should never be in a position where the only supported AISVS version requires a structural migration of their existing compliance work.

## Repository Layout

Each released minor version lives in its own folder. Once a version is released its folder is locked, and the next version is opened in a new folder with a `-dev` suffix:

```
/
├── 1.0/         <- released (locked after release)
├── 1.01-dev/    <- next minor release in progress
```

When work on a new major opens, it lives alongside the active minor line in its own `-dev` folder (for example, `2.0-dev/`) so the previous major can continue to receive minor releases during the maintenance period. This mirrors the approach used by [OWASP ASVS](https://github.com/OWASP/ASVS).

## Referencing Across Versions

For citing requirements in reports, tools, audits, or other documents, use the full versioned form:

```
v<version>-C<chapter>.<section>.<requirement>
```

For example, `v1.0-C9.4.3`. The unversioned form `C9.4.3` resolves to the latest released minor, which works for casual reference but should be avoided in anything that needs to remain stable across versions. See [How to Reference AISVS Requirements](https://github.com/OWASP/AISVS#how-to-reference-aisvs-requirements) in the README for the full convention.
