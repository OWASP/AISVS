#!/usr/bin/env python3
"""Convert Western digits to Gurmukhi numerals in the PANJABI lines of pa-IN.

Rule (locked with the ASVS Panjabi styleguide, 2026-09-29; extended to AISVS
2026-09-30): in Panjabi text, requirement IDs, chapter/section references,
assurance levels and plain quantities use Gurmukhi numerals (੦-੯).

What is NOT converted (kept as in the source):
  - any line with no Gurmukhi letter (the English block stays untouched, so
    every ID still maps 1:1 to the English original and to v1.0-Cx.y.z);
  - code spans, URLs, link targets, HTML comments, HTML entities;
  - version identifiers after ਸੰਸਕਰਣ or a licence name (version 1.0, CC BY-SA 4.0);
  - digits inside Latin-script names and versions (TLS 1.3, SHA-256, FIPS 140-3,
    NIST SP 800-190, AML.T0024.001, GPT-4, v1.0, ASVS 5.0). Tag R (Retained).

Usage:
  python3 tools/gurmukhi-numerals.py            # dry run, prints counts
  python3 tools/gurmukhi-numerals.py --write    # rewrite pa-IN/*.md and pa-IN/print/**/*.md
  python3 tools/gurmukhi-numerals.py --check    # exit 1 if any convertible digit remains
Stdlib only. Idempotent.
"""
import re
import sys
from pathlib import Path

PA_IN = Path(__file__).resolve().parent.parent / "pa-IN"
GURMUKHI = re.compile(r"[\u0A00-\u0A7F]")
DIGITS = str.maketrans("0123456789", "੦੧੨੩੪੫੬੭੮੯")
CHUNK = re.compile(r"[A-Za-z0-9._\-/]+")
REF_PREFIX = re.compile(r"^(?:(?:AC|AD|C|V)\.?)?(\d+(?:\.\d+)*)([.\-]?)$")
# Version identifiers of named standards/licences stay Western (Tag R): the
# word right before them names the thing being versioned.
VERSION_PREFIXES = ("ਸੰਸਕਰਣ ", "ਸ਼ੇਅਰਅਲਾਈਕ ")
SKIP_FILES = {"CLAUDE.md", "TRANSLATION-RULES.md", "GLOSSARY.md",
              "OPEN-QUESTIONS.md", "REVISIONS.md"}


def convert_segment(seg: str) -> str:
    out, last = [], 0
    for m in CHUNK.finditer(seg):
        chunk = m.group(0)
        s, e = m.span()
        if not re.search(r"\d", chunk):
            continue
        # Chunks glued to entities / anchors / hex-like identifiers stay as is.
        if s > 0 and seg[s - 1] in "#&_":
            continue
        pm = REF_PREFIX.match(chunk)
        if not pm:
            continue
        # A bare number right after a Latin word is part of a name ("TLS 1.3").
        # Ref-prefixed chunks (C5.1, AC.1.3, V2) are always references.
        bare = not re.match(r"^(?:AC|AD|C|V)", chunk)
        if bare:
            before = seg[:s].rstrip(" ")
            prev = re.search(r"(\S+)$", before)
            after_ref = bool(prev and re.match(r"^(?:AC|AD|C|V)\.?[\d੦-੯]", prev.group(1)))
            if (len(before) < len(seg[:s]) and not after_ref
                    and re.search(r"[A-Za-z][A-Za-z0-9]*$", before)):
                continue
            if s > 0 and seg[s - 1] in "-/":
                continue
            if any(seg[:s].endswith(v) for v in VERSION_PREFIXES) and "." in chunk:
                continue
        out.append(seg[last:s])
        out.append(re.sub(r"\d", lambda d: d.group(0).translate(DIGITS), chunk))
        last = e
    out.append(seg[last:])
    return "".join(out)


def convert_line(line: str) -> str:
    if line.lstrip().startswith("<!--") or not GURMUKHI.search(line):
        return line
    # Protect code spans and markdown link targets.
    parts = re.split(r"(`[^`]*`|\]\([^)]*\)|https?://\S+)", line)
    return "".join(p if i % 2 else convert_segment(p) for i, p in enumerate(parts))


def targets():
    for p in sorted(PA_IN.glob("0x*.md")):
        yield p
    for p in sorted((PA_IN / "print").rglob("*.md")):
        if p.name not in SKIP_FILES:
            yield p


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    changed = remaining = 0
    for p in targets():
        text = p.read_text(encoding="utf-8")
        new = "\n".join(convert_line(l) for l in text.split("\n"))
        if new != text:
            changed += 1
            if mode == "--write":
                p.write_text(new, encoding="utf-8")
            elif mode == "--check":
                remaining += sum(1 for a, b in zip(text.split("\n"), new.split("\n")) if a != b)
                print(f"{p.relative_to(PA_IN)}: {sum(1 for a, b in zip(text.split(chr(10)), new.split(chr(10))) if a != b)} line(s) still use Western digits")
    if mode == "--check":
        if remaining:
            return 1
        print("Gurmukhi-numeral check: clean.")
        return 0
    print(f"{'wrote' if mode == '--write' else 'would change'} {changed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
