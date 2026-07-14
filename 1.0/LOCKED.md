# AISVS 1.0 is locked

This folder holds the published **AISVS v1.0** standard. As of the v1.0 release it is frozen: the requirement text, levels, structure, and identifiers under `1.0/en/` are stable and will not change. Downstream adopters, auditors, and tooling can cite `v1.0-Cx.y.z` identifiers against this folder with confidence that they will not move.

The research wiki under `1.0/research/` is part of this snapshot. It maps each v1.0 requirement to threats, tooling, and verification approaches, and is frozen alongside the standard it documents. Newer research is published with the dev folders below.

Do not edit files under `1.0/en/`, `1.0/dist/`, or `1.0/research/`. A CI guard rejects pull requests that modify them.

The only exception is correcting the mistakes in the original `1.0/research/` folder which is AI generated. As newer models handle this type of research in a more capable way, we may update this content via automation only.

Future work happens in the next version folder:

- `1.01-dev/en/` for the next minor release.

See [RELEASE.md](../RELEASE.md) for the versioning and release policy.
