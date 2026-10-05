# AISVS 1.01 is locked

This folder holds the published **AISVS v1.01** standard. As of the v1.01 release it is frozen: the requirement text, levels, structure, and identifiers under `1.01/en/` are stable and will not change. Downstream adopters, auditors, and tooling can cite `v1.01-Cx.y.z` identifiers against this folder with confidence that they will not move.

The research wiki under `1.01/research/` is part of this snapshot. It maps each v1.01 requirement to threats, tooling, and verification approaches, and is frozen alongside the standard it documents.

Do not edit files under `1.01/en/`, `1.01/dist/`, or `1.01/research/`. A CI guard rejects pull requests that modify them. Research corrections are accepted only through the automated research synchronization path.

Future work happens in the next version folders:

- `1.02-dev/en/` for the next minor release.
- `2.0-dev/en/` for the next major release.

See [RELEASE.md](../RELEASE.md) for the versioning and release policy.
