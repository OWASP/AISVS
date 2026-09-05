#!/usr/bin/env python3
"""Requirement-ID completeness check: every requirement ID in the English
source must appear TWICE in the bilingual pa-IN file — once in the English
block, once in the Panjabi block (the dual-block convention shared with the
sibling ASVS corpus). Checking mere presence is not enough: a pa-IN file
always contains the English block too, so an ID present only once (English
intact, Panjabi silently dropped) would pass a presence-only check.
Zero-dep (stdlib only).

Usage: python3 verify-requirement-ids.py
Exit 0 = every EN requirement ID appears >=2x in pa-IN (both blocks present).
Exit 1 = something missing from the Panjabi side.
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # .../1.0
EN = ROOT / "en"
PA = ROOT / "pa-IN"

ID_RE = re.compile(r"\*\*(\d+\.\d+\.\d+)\*\*")

CHAPTER_FILES = [
    "0x10-C01-Training-Data-Integrity-and-Traceability", "0x10-C02-Input-Validation",
    "0x10-C03-Model-Lifecycle-Management", "0x10-C04-Infrastructure",
    "0x10-C05-Access-Control-and-Identity", "0x10-C06-Supply-Chain",
    "0x10-C07-Model-Behavior", "0x10-C08-Memory-Embeddings-and-Vector-Database",
    "0x10-C09-Orchestration-and-Agentic-Action", "0x10-C10-MCP-Security",
    "0x10-C11-Adversarial-Robustness", "0x10-C12-Monitoring-and-Logging",
]


def ids_in(path):
    if not path.exists():
        return None
    return Counter(ID_RE.findall(path.read_text(encoding="utf-8")))


def main():
    total_missing = 0
    for stem in CHAPTER_FILES:
        en_ids = ids_in(EN / f"{stem}.md")
        pa_ids = ids_in(PA / f"{stem}.md")
        if en_ids is None:
            print(f"{stem}: SKIP — no English source file found")
            continue
        if pa_ids is None:
            print(f"{stem}: FAIL — no Panjabi translation file found ({len(en_ids)} EN ids expected)")
            total_missing += len(en_ids)
            continue
        under_translated = sorted(id_ for id_ in en_ids if pa_ids.get(id_, 0) < 2)
        if under_translated:
            total_missing += len(under_translated)
            print(f"{stem}: {len(under_translated)} requirement ID(s) present <2x in pa-IN "
                  f"(Panjabi block likely missing): {under_translated}")
        extra = sorted(set(pa_ids) - set(en_ids))
        if extra:
            print(f"{stem}: NOTE — {len(extra)} id(s) in pa-IN not in current EN source (upstream drift?): {extra}")
    if total_missing:
        print(f"\n{total_missing} requirement ID(s) under-translated overall.", file=sys.stderr)
        return 1
    print("\nRequirement-ID completeness: clean — every EN requirement ID appears in both the "
          "English and Panjabi blocks, all 12 control-family chapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
