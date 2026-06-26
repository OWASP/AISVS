# AISVS 1.0 is locked

This folder holds the published **AISVS v1.0** standard. As of the v1.0 release it is frozen: the requirement text, levels, structure, and identifiers under `1.0/en/` are stable and will not change. Downstream adopters, auditors, and tooling can cite `v1.0-Cx.y.z` identifiers against this folder with confidence that they will not move.

The research wiki under `1.0/research/` is part of this snapshot. It maps each v1.0 requirement to threats, tooling, and verification approaches, and is frozen alongside the standard it documents. Newer research is published with the dev folders below.

Do not edit files under `1.0/en/`, `1.0/dist/`, or `1.0/research/`. A CI guard rejects pull requests that modify them.

Future work happens in the next version folders:

- `1.01-dev/en/` for the next minor release.
- `2.0-dev/en/` for the next major release.

See [RELEASE.md](../RELEASE.md) for the versioning and release policy.
