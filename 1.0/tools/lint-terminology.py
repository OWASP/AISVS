#!/usr/bin/env python3
"""Mechanical terminology-consistency lint for the AISVS pa-IN corpus.

Why this exists: the 2026-08-26 cross-file consistency audit (see
OPEN-QUESTIONS.md Q66, Q69, Q71, Q86) found that "unsafe" and "threshold"
had ALREADY drifted into a second spelling across chapters despite being
documented as locked picks in OPEN-QUESTIONS.md before this lint existed.
A rule that only lives in prose does not prevent recurrence — this script
is the mechanical gate. Run it before every commit that touches pa-IN/*.md,
and wire it into CI once this repo has one.

Zero third-party dependencies (stdlib only) so it never silently no-ops for
a missing package.

Usage: python3 tools/lint-terminology.py
Exit 0 = clean. Exit 1 = forbidden variant(s) found, printed as file:line.
"""
import re
import sys
from pathlib import Path

PA_IN = Path(__file__).resolve().parent.parent / "pa-IN"

# Only lint actual translated content — not the rulebook/glossary/log files
# themselves, which legitimately discuss the forbidden forms by name.
SKIP_FILES = {"CLAUDE.md", "TRANSLATION-RULES.md", "GLOSSARY.md", "OPEN-QUESTIONS.md"}

# Each entry: (label, forbidden_regex, correct_form, source, carve_out_regex_or_None)
# carve_out_regex: if a forbidden match falls inside this pattern, it's allowed
# (e.g. ਫ੍ਰੇਮਵਰਕ is explicitly grandfathered from the /f/-nukta rule).
PINNED_TERMS = [
    (
        "unsafe",
        re.compile(r"ਅਸੁਰੱਖਿਅਤ"),
        "ਗ਼ੈਰ-ਸਲਾਮਤ",
        "OPEN-QUESTIONS.md Q66",
        None,
    ),
    (
        "threshold",
        re.compile(r"ਹੱਦਾਂ|(?<!ਹੱਦੋਂ )ਹੱਦ(?!ੋਂ)"),
        "ਥ੍ਰੈਸ਼ਹੋਲਡ",
        "OPEN-QUESTIONS.md Q69",
        re.compile(r"ਹੱਦੋਂ ਵੱਧ"),  # "over-" / "beyond the limit" — a different sense, not a threshold
    ),
    (
        "-based (suffix)",
        re.compile(r"ਅਧਾਰਿਤ"),
        "ਆਧਾਰਿਤ",
        "OPEN-QUESTIONS.md Q71",
        None,
    ),
    (
        "control(s)",
        re.compile(r"(?<!ਪਹੁੰਚ )ਕੰਟਰੋਲ(ਾਂ)?(?!\s)"),
        "ਨਿਯੰਤਰਣ / ਨਿਯੰਤਰਣਾਂ",
        "GLOSSARY.md (locked from ASVS); AISVS audit 2026-08-26",
        re.compile(r"ਪਹੁੰਚ ਕੰਟਰੋਲ"),  # "access control" is the one locked ਕੰਟਰੋਲ compound
    ),
    (
        "English /f/ — bare ਫ instead of ਫ਼",
        re.compile(r"ਫ(?!਼)(ਾਰਮੈਟ|ਾਰਮ|ੈਡਰੇਟਿਡ|ਰਮਵੇਅਰ|ੀਡਬੈਕ)"),
        "ਫ਼ (with nukta) — e.g. ਫ਼ਾਰਮੈਟ, ਫ਼ੈਡਰੇਟਿਡ",
        "OPEN-QUESTIONS.md Q86",
        re.compile(r"ਫ੍ਰੇਮਵਰਕ"),  # explicit carve-out: locked bare-ਫ from the ASVS sibling corpus
    ),
]


def iter_lint_targets():
    for path in sorted(PA_IN.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        yield path


def check_file(path):
    findings = []
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        for label, forbidden, correct, source, carve_out in PINNED_TERMS:
            for m in forbidden.finditer(line):
                if carve_out and carve_out.search(line):
                    continue
                findings.append((lineno, label, m.group(0), correct, source))
    return findings


def main():
    total = 0
    for path in iter_lint_targets():
        findings = check_file(path)
        for lineno, label, matched, correct, source in findings:
            total += 1
            rel = path.relative_to(PA_IN.parent.parent)
            print(f"{rel}:{lineno}: [{label}] found {matched!r} — pinned pick is {correct} ({source})")
    if total:
        print(f"\n{total} pinned-terminology violation(s) found.", file=sys.stderr)
        return 1
    print("Terminology lint: clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
