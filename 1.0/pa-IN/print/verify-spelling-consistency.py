#!/usr/bin/env python3
"""Spelling-consistency check for the AISVS pa-IN corpus.

Ported from the sibling ASVS corpus's identically-purposed script — see
that file's docstring for the full rationale. Same heuristic: a rare word
(1-3 occurrences) that is edit-distance-1 from a much more common word
elsewhere in the corpus is a candidate typo, surfaced for human review
against a dictionary, not auto-corrected.

Zero-dep (stdlib only).

Usage: python3 verify-spelling-consistency.py [--min-ratio N]
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # .../pa-IN
SKIP_FILES = {"CLAUDE.md", "TRANSLATION-RULES.md", "GLOSSARY.md", "OPEN-QUESTIONS.md"}

GURMUKHI = r"਀-੿"
WORD_RE = re.compile(f"[{GURMUKHI}]+")
MIN_WORD_LEN = 4
MAX_RARE_COUNT = 3
DEFAULT_MIN_RATIO = 15


def edit_distance_1(a, b):
    if a == b:
        return False
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        diffs = sum(1 for x, y in zip(a, b) if x != y)
        return diffs == 1
    shorter, longer = (a, b) if la < lb else (b, a)
    i = j = 0
    mismatches = 0
    while i < len(shorter) and j < len(longer):
        if shorter[i] == longer[j]:
            i += 1
            j += 1
        else:
            mismatches += 1
            j += 1
            if mismatches > 1:
                return False
    return True


def collect_word_counts():
    counts = Counter()
    locations = {}
    for path in sorted(ROOT.glob("*.md")):
        if path.name in SKIP_FILES:
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for m in WORD_RE.finditer(line):
                w = m.group(0)
                if len(w) < MIN_WORD_LEN:
                    continue
                counts[w] += 1
                if w not in locations:
                    locations[w] = (path.name, lineno)
    return counts, locations


def main():
    min_ratio = DEFAULT_MIN_RATIO
    if "--min-ratio" in sys.argv:
        min_ratio = int(sys.argv[sys.argv.index("--min-ratio") + 1])

    counts, locations = collect_word_counts()
    common_words = [w for w, c in counts.items() if c > MAX_RARE_COUNT * min_ratio]
    rare_words = [w for w, c in counts.items() if 1 <= c <= MAX_RARE_COUNT]

    by_len = {}
    for w in common_words:
        by_len.setdefault(len(w), []).append(w)

    findings = []
    for rare in rare_words:
        for length in (len(rare) - 1, len(rare), len(rare) + 1):
            for common in by_len.get(length, []):
                if edit_distance_1(rare, common):
                    ratio = counts[common] / counts[rare]
                    if ratio >= min_ratio:
                        fname, lineno = locations[rare]
                        findings.append((fname, lineno, rare, counts[rare], common, counts[common], ratio))

    findings.sort(key=lambda f: -f[6])
    for fname, lineno, rare, rc, common, cc, ratio in findings:
        print(f"{fname}:{lineno}: [spelling-candidate] {rare!r} ({rc}x) looks like a typo of "
              f"{common!r} ({cc}x, {ratio:.0f}x more common) — verify against a dictionary before changing")

    if findings:
        print(f"\n{len(findings)} spelling candidate(s) found — these are hypotheses for human review, "
              f"not confirmed errors.", file=sys.stderr)
        return 1
    print("Spelling consistency check: no rare-word-vs-common-word candidates found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
