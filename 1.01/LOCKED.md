# AISVS 1.01 is locked

This folder holds the published **AISVS v1.01** standard. As of the v1.01 release it is frozen: the requirement text, levels, structure, and identifiers under `1.01/en/` are stable and will not change. Downstream adopters, auditors, and tooling can cite `v1.01-Cx.y.z` identifiers against this folder with confidence that they will not move.

Do not edit files under `1.01/en/` or `1.01/dist/`. A CI guard rejects pull requests that modify them.

Future work happens in the next version folder:

- `1.02-dev/en/` for the next minor release.

See [RELEASE.md](../RELEASE.md) for the versioning and release policy.
