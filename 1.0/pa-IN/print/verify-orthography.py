#!/usr/bin/env python3
"""Mechanical orthography lint for the AISVS pa-IN corpus, encoding the
"Mechanical QA before review" checklist that TRANSLATION-RULES.md §7 and
CLAUDE.md's sentence-ending-punctuation section already state in prose:
  - 0 Western-period sentence-ends after Gurmukhi text (danda rule, CLAUDE.md)
  - 0 Devanagari-block leaks outside the permitted danda/double-danda
    (U+0964/U+0965 are shared Indic punctuation, not Devanagari letters)
  - NFC normalisation
Ported from the sibling ASVS corpus's identically-purposed script (same
logic, same false-positive fix already applied for Gurmukhi-rendered
dotted acronyms like ਓ.ਆਈ.ਡੀ.ਸੀ.). Zero-dep (stdlib only).

Usage: python3 verify-orthography.py
Exit 0 = clean. Exit 1 = violations found, printed as file:line.
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # .../pa-IN
SKIP_FILES = {"CLAUDE.md", "TRANSLATION-RULES.md", "GLOSSARY.md", "OPEN-QUESTIONS.md"}

GURMUKHI = r"਀-੿"
WESTERN_PERIOD_AFTER_GURMUKHI = re.compile(f"[{GURMUKHI}]\\.(?!\\d)")
# Dotted acronym chains rendered in Gurmukhi (e.g. ਓ.ਆਈ.ਡੀ.ਸੀ.) are a
# legitimate corpus convention, not sentence-ending dandas.
ACRONYM_CHAIN = re.compile(f"(?:[{GURMUKHI}]{{1,3}}\\.){{2,}}")
# Devanagari block (U+0900-U+097F) EXCLUDING the two permitted shared-Indic
# punctuation codepoints (danda U+0964, double-danda U+0965).
DEVANAGARI_LEAK = re.compile("[ऀ-ॣ०-ॿ]")


def iter_targets():
    for path in sorted(ROOT.glob("*.md")):
        if path.name in SKIP_FILES:
            yield path, True
        else:
            yield path, False


def check_file(path, rules_only_skip):
    findings = []
    text = path.read_text(encoding="utf-8")
    if unicodedata.normalize("NFC", text) != text:
        findings.append((0, "NFC", "file is not NFC-normalised"))
    if rules_only_skip:
        return findings
    for lineno, line in enumerate(text.splitlines(), start=1):
        exempt = [c.span() for c in ACRONYM_CHAIN.finditer(line)]
        for m in WESTERN_PERIOD_AFTER_GURMUKHI.finditer(line):
            pos = m.start() + 1
            if any(s <= pos < e for s, e in exempt):
                continue
            findings.append((lineno, "danda", f"Western period after Gurmukhi at col {m.start()}"))
        for m in DEVANAGARI_LEAK.finditer(line):
            findings.append((lineno, "devanagari-leak",
                              f"Devanagari char {m.group(0)!r} (U+{ord(m.group(0)):04X}) at col {m.start()}"))
    return findings


def main():
    total = 0
    for path, rules_only in iter_targets():
        for lineno, kind, msg in check_file(path, rules_only):
            total += 1
            print(f"{path.relative_to(ROOT.parent.parent)}:{lineno}: [{kind}] {msg}")
    if total:
        print(f"\n{total} orthography violation(s) found.", file=sys.stderr)
        return 1
    print("Orthography lint: clean — danda rule, Devanagari-leak check, NFC normalisation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
