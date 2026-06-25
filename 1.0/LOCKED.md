# AISVS 1.0 is locked

This folder holds the published **AISVS v1.0** standard. As of the v1.0 release it is frozen: the requirement text, levels, structure, and identifiers under `1.0/en/` are stable and will not change. Downstream adopters, auditors, and tooling can cite `v1.0-Cx.y.z` identifiers against this folder with confidence that they will not move.

Do not edit files under `1.0/en/`. A CI guard rejects pull requests that modify them.

Future work happens in the next version folders:

- `1.01-dev/en/` for the next minor release.
- `2.0-dev/en/` for the next major release.

See [RELEASE.md](../RELEASE.md) for the versioning and release policy.
