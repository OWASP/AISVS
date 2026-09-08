#!/usr/bin/env python3
"""Modal-strength check: every English "must not" (hard prohibition) clause
must have a correspondingly strong Panjabi rendering, not the weaker bare
ਨਹੀਂ...ਚਾਹੀਦਾ form (which reads like "should not").

Ported from the sibling ASVS corpus's identically-purposed script. Origin:
a 2026-08-27 adversarial fidelity audit found 12 "must not" softening sites
in ASVS plus 2 in this AISVS corpus (AC.4.1, AC.12.5, both in
0x92-Appendix-C_AI_for_Code_Generation.md) -- both now fixed. This script
is the mechanical gate against regression.

Requirement IDs here include the Appendix C "AC.N.N" prefix format in
addition to the plain "N.N.N" format used elsewhere, so the row regex is
slightly more permissive than the ASVS version.

Zero-dep (stdlib only).

Usage: python3 verify-modal-strength.py
Exit 0 = clean. Exit 1 = a must-not/may-not clause has no strong PA marker.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # .../pa-IN
SKIP_FILES = {"CLAUDE.md", "TRANSLATION-RULES.md", "GLOSSARY.md", "OPEN-QUESTIONS.md"}

# Table-row requirement lines: | **id** | text | level |  (id: "1.1.1" or "AC.4.1")
ROW_RE = re.compile(r"^\|\s*\*\*([A-Z]*\.?[\d.]+)\*\*\s*\|(.+)\|\s*\S+\s*\|\s*$")
MUST_NOT_EN = re.compile(r"\bmust not\b|\bmay not\b", re.IGNORECASE)
WEAK_MODAL = re.compile(r"ਨਹੀਂ\s*[^।]{0,25}ਚਾਹੀਦ[ਾੇੀ]")
STRONG_MARKER = re.compile(r"ਲਾਜ਼ਮੀ")


def check_file(path):
    findings = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = ROW_RE.match(line)
        if not m or not MUST_NOT_EN.search(m.group(2)):
            continue
        req_id = m.group(1)
        for j in range(i + 1, min(i + 30, len(lines))):
            pm = ROW_RE.match(lines[j])
            if pm and pm.group(1) == req_id:
                pa_text = pm.group(2)
                if WEAK_MODAL.search(pa_text) and not STRONG_MARKER.search(pa_text):
                    findings.append((j + 1, req_id))
                break
    return findings


def main():
    total = 0
    for path in sorted(ROOT.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        for lineno, req_id in check_file(path):
            total += 1
            print(f"{path.relative_to(ROOT.parent.parent)}:{lineno}: [modal-strength] "
                  f"requirement {req_id} — EN has must-not/may-not, PA uses bare "
                  f"ਨਹੀਂ...ਚਾਹੀਦਾ with no ਲਾਜ਼ਮੀ marker")
    if total:
        print(f"\n{total} modal-strength violation(s) found.", file=sys.stderr)
        return 1
    print("Modal-strength check: clean — every EN must-not/may-not clause has a strong Panjabi rendering.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
