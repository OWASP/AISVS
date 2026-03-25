# Wiki Requirements Reconciliation

Date: 2026-03-25

This document compares the wiki requirements under `wiki/` against the canonical AISVS `1.0/en` source files in the parent repository.

## Summary

- Canonical `1.0/en` controls: 449
- Wiki controls: 450
- Exact content matches with the same control ID: 406
- Exact content matches after renumbering or section moves: 21
- Exact content match rate after normalization: 427/449 (95.1%)

The wiki is close to the canonical requirements, but it is not an exact mirror. The remaining deltas are concentrated in a small set of chapters and are a mix of:

- True content drift
- Renumbering or section reshuffles
- Minor editorial or punctuation differences
- Wiki-only extra controls
- Canonical controls missing from the wiki

## Chapters With Real Reconciliation Work

### C01

File: `wiki/C01-Training-Data.md`

- `1.3.1` is shortened in the wiki and drops the canonical requirement to export and retain annotator identity metadata across the full training pipeline, including preference pairs.
- `1.3.2` is shortened in the wiki and drops the canonical reference to fine-tuning feedback records, including RLHF preference pairs.

### C03

File: `wiki/C03-Model-Lifecycle-Management.md`

- The wiki keeps retirement controls at `3.5.1` and `3.5.2`.
- Hosted-model dependency controls from canonical `3.5.1` to `3.5.4` appear in the wiki as `3.6.1` to `3.6.4`.
- Canonical `3.7.1` to `3.7.4` are missing from the wiki:
  - `3.7.1` separation of duties for fine-tuning or retraining authorization
  - `3.7.2` reward model signing and integrity verification
  - `3.7.3` reward hacking or over-optimization detection
  - `3.7.4` integrity verification and rollback for multi-stage fine-tuning

### C05

File: `wiki/C05-Access-Control.md`

- Canonical `5.5.5` is missing from the wiki:
  - KV-cache partitioning by authenticated session or tenant identity, including prefix caching isolation
- `5.4.1` is broadened in the wiki to explicitly redact PII; the canonical text focuses on preventing unauthorized classified or proprietary data disclosure.

### C09

File: `wiki/C09-04-Agent-Identity-and-Audit.md`

- `9.4.3` is materially similar, but the wiki drops the canonical explicit allowance for cryptographic hash chaining as a tamper-evidence mechanism.

### C10

Files:

- `wiki/C10-01-Component-Integrity.md`
- `wiki/C10-MCP-Security.md`

The numbering diverges in `10.1.x`:

- Canonical `10.1.2` is the allowlisted MCP server identifiers control.
- The wiki has that control as `10.1.3`.
- The wiki uses `10.1.2` for a different plaintext-secrets control not present in canonical `1.0/en`.

This creates both a numbering mismatch and a wiki-only extra control.

### C12

File: `wiki/C12-Privacy.md`

The remaining differences are mostly editorial normalization issues:

- `12.1.3`
- `12.1.4`
- `12.2.1`
- `12.3.1`
- `12.3.2`
- `12.6.4`

These mostly involve symbol substitution such as `epsilon`, `delta`, `<=`, and phrasing changes like `SLAs` versus `service level agreements`.

### C13

Files:

- `wiki/C13-03-Model-Drift-Detection.md`
- `wiki/C13-06-Performance-Degradation-Detection.md`
- `wiki/C13-07-DAG-Visualization-Workflow-Security.md`
- `wiki/C13-08-Proactive-Security-Behavior-Monitoring.md`

This is the largest structural divergence.

Canonical `1.0/en` structure:

- `13.3.x` model drift and degradation controls
- `13.6.x` DAG visualization and workflow security controls
- `13.7.x` proactive security behavior monitoring controls

Wiki structure:

- `13.3.x` drift detection controls
- `13.6.x` performance degradation detection controls
- `13.7.x` DAG visualization and workflow security controls
- `13.8.x` proactive security behavior monitoring controls

Specific issues:

- Canonical `13.3.6` to `13.3.9` are not present at those IDs in the wiki, but most of their text exists under different wiki IDs.
- Wiki `13.6.2`, `13.6.3`, and `13.6.5` map exactly to canonical `13.3.5`, `13.3.7`, and `13.3.8`.
- Wiki `13.7.1` to `13.7.5` map exactly to canonical `13.6.1` to `13.6.5`.
- Wiki `13.8.1` to `13.8.5` map exactly to canonical `13.7.1` to `13.7.5`.
- Wiki `13.6.6` is a wiki-only extra control:
  - Baseline performance profiles are formally documented and version-controlled, reviewed at an appropriate frequency.

There are also a few true wording changes in the wiki for:

- `13.3.1`
- `13.3.2`
- `13.6.1`
- `13.6.4`

### C14

File: `wiki/C14-Human-Oversight.md`

- Wiki-only extra control: `14.3.2`
- `14.1.2` differs only because the canonical `1.0/en` text contains a duplicated word (`only to authorized personnel`), while the wiki reads correctly.

## Exact Renumbered Matches

The following controls appear to match canon exactly after normalization but have different IDs in the wiki:

- `3.6.1` -> canonical `3.5.1`
- `3.6.2` -> canonical `3.5.2`
- `3.6.3` -> canonical `3.5.3`
- `3.6.4` -> canonical `3.5.4`
- `10.1.3` -> canonical `10.1.2`
- `13.3.3` -> canonical `13.3.4`
- `13.3.4` -> canonical `13.3.6`
- `13.3.5` -> canonical `13.3.9`
- `13.6.2` -> canonical `13.3.5`
- `13.6.3` -> canonical `13.3.7`
- `13.6.5` -> canonical `13.3.8`
- `13.7.1` -> canonical `13.6.1`
- `13.7.2` -> canonical `13.6.2`
- `13.7.3` -> canonical `13.6.3`
- `13.7.4` -> canonical `13.6.4`
- `13.7.5` -> canonical `13.6.5`
- `13.8.1` -> canonical `13.7.1`
- `13.8.2` -> canonical `13.7.2`
- `13.8.3` -> canonical `13.7.3`
- `13.8.4` -> canonical `13.7.4`
- `13.8.5` -> canonical `13.7.5`

## Recommended Follow-Up

1. Decide whether the wiki should be a strict mirror of `1.0/en` IDs and control text, or whether wiki-only editorial extensions are allowed.
2. If strict mirroring is the goal, reconcile C03, C05, C10, C13, and C14 first.
3. Restore missing canonical controls in C03 and C05.
4. Resolve whether the wiki-only controls in C10, C13, and C14 should be retained, moved, or removed.
5. Normalize editorial differences in C01, C09, and C12.
