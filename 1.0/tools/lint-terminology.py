#!/usr/bin/env python3
"""Mechanical terminology-consistency lint for the AISVS pa-IN corpus.

Why this exists: the 2026-08-26 cross-file consistency audit (see
OPEN-QUESTIONS.md Q66, Q69, Q71, Q86) found that "unsafe" and "threshold"
had ALREADY drifted into a second spelling across chapters despite being
documented as locked picks in OPEN-QUESTIONS.md before this lint existed.
A rule that only lives in prose does not prevent recurrence — this script
is the mechanical gate. Run it before every commit that touches pa-IN/*.md,
and wire it into CI once this repo has one.

The 2026-08-27 full-corpus audit (all 18 files on disk) repeated the lesson:
three terms had drifted across files and every Gurmat rejection in
OPEN-QUESTIONS.md was still prose-only, so the same rejected word could be —
and at Q144(a) had been — re-introduced by the next file. Those guards are the
second block of PINNED_TERMS below.

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
# carve_out_regex: if a forbidden match falls INSIDE an occurrence of this
# pattern, that one match is allowed (e.g. ਫ੍ਰੇਮਵਰਕ is explicitly grandfathered
# from the /f/-nukta rule). The overlap is checked per match, not per line —
# a line-wide carve-out would let one legitimate ਪਹੁੰਚ ਕੰਟਰੋਲ suppress every
# other violation sharing its line, which for table rows is most of a section.
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
        # NOTE: do NOT re-add a trailing (?!\s) here. It was present until the
        # 2026-08-27 C10 review and made this rule blind to the exact violation
        # Q80 was written to prevent — a bare ਕੰਟਰੋਲ inside a compound followed
        # by a space, e.g. "ਲੰਬਾਈ ਕੰਟਰੋਲ ਲਾਗੂ". Only ਕੰਟਰੋਲਾਂ and a
        # sentence-final ਕੰਟਰੋਲ। were being caught. The ਪਹੁੰਚ lookbehind, not a
        # whitespace lookahead, is what exempts the one locked compound.
        re.compile(r"(?<!ਪਹੁੰਚ )ਕੰਟਰੋਲ(ਾਂ)?"),
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
    # ---------------------------------------------------------------------
    # Added by the 2026-08-27 full-corpus audit (all 18 files present).
    # Each entry below guards a finding that a HUMAN or an independent review
    # caught, not this lint — which is exactly the recurrence risk the file
    # header describes. Every pattern was verified to match 0 sites in the
    # corpus at the time it was added, so a future hit is a real regression.
    # ---------------------------------------------------------------------
    (
        "confidential (as a loan)",
        # Found 2026-08-27: C05 5.3.2 rendered *confidential computing* as
        # ਕਾਨਫ਼ੀਡੈਂਸ਼ੀਅਲ ਕੰਪਿਊਟਿੰਗ while C04, Appendix A and Appendix B — the
        # last of which indexes that very requirement — all used ਗੁਪਤ.
        re.compile(r"ਕਾਨਫ਼ੀਡੈਂਸ਼ੀਅਲ"),
        "ਗੁਪਤ (e.g. ਗੁਪਤ ਕੰਪਿਊਟਿੰਗ, ਗੁਪਤ ਇਨਫ਼ਰੈਂਸ)",
        "OPEN-QUESTIONS.md Q50; AISVS audit 2026-08-27",
        None,
    ),
    (
        "Gurmat — ਸੱਚ / ਸਤਿ for 'truth'",
        # Q97 rejects ਸੱਚ/ਸਤਿ by name (Divine Truth in Gurbani) for *source of
        # truth*; Q144(a) had to apply the same rejection again to *ground
        # truth* in Appendix A. Rejected twice in prose, never mechanically.
        re.compile(r"(?<![਀-੿])(?:ਸੱਚ(?:ਾਈ)?|ਸਤਿ)(?![਀-੿])"),
        "a neutral technical rendering, or the retained English head "
        "(e.g. `ground-truth ਮੁੱਲ`, ਸਰੋਤ-ਪ੍ਰਮਾਣ)",
        "OPEN-QUESTIONS.md Q97, Q144(a); TRANSLATION-RULES.md §5",
        None,
    ),
    (
        "Gurmat — ਮੁਦਰਾ for 'posture/state'",
        # The original ASVS collision (Q5, commit 9e1e96b). GLOSSARY.md marks it
        # "NEVER ਮੁਦਰਾ" but nothing enforced that on the AISVS side.
        re.compile(r"(?<![਀-੿])ਮੁਦਰਾ"),
        "ਸਥਿਤੀ",
        "GLOSSARY.md (locked, ASVS Q5)",
        None,
    ),
    (
        "Gurmat — standalone ਕਰਤਾ for 'principal/actor'",
        # Q124: bare ਕਰਤਾ is load-bearing devotional vocabulary (ਕਰਤਾ ਪੁਰਖੁ).
        # The lookbehind/lookahead keep the locked compounds ਜਾਰੀਕਰਤਾ (issuer)
        # and ਪਛਾਣਕਰਤਾ (identifier) out of scope — only the bare word trips.
        re.compile(r"(?<![਀-੿])ਕਰਤਾ(?![਀-੿])"),
        "ਪਛਾਣ-ਇਕਾਈ",
        "OPEN-QUESTIONS.md Q124; TRANSLATION-RULES.md §5",
        None,
    ),
    (
        "'error' noun spelled with nukta",
        # Q98 fixes the NOUN as ਗਲਤੀ (matching GLOSSARY.md ਗਲਤੀ ਪ੍ਰਬੰਧਨ) and says
        # explicitly that no file may introduce a second spelling; Appendix A had
        # carried both until Q144(h). The adjective ਗ਼ਲਤ keeps its nukta and does
        # not match this pattern.
        re.compile(r"ਗ਼ਲਤੀ"),
        "ਗਲਤੀ (no nukta on the noun; the adjective ਗ਼ਲਤ keeps it)",
        "OPEN-QUESTIONS.md Q98, Q144(h)",
        None,
    ),
    (
        "Q144 superseded Appendix A forms",
        # Four renderings an independent review replaced on 2026-08-27. Each was
        # a collision with a term already fixed elsewhere in the corpus:
        #   ਦ੍ਰਿਸ਼ਟਾਂਤ  = parable/illustrative example, not *visualization*
        #   ਪਿਛਲਖੁਰੀ    = walking backwards, not *post-hoc*
        #   ਵਿਸ਼ੇਸ਼-ਵੇਰਵਾ = collides with the Description column and ਵਿਸ਼ੇਸ਼-ਅਧਿਕਾਰ
        #   ਮਾੜੇ ਪ੍ਰਭਾਵ  = "adverse effects", a judgement the source does not make
        re.compile(r"ਦ੍ਰਿਸ਼ਟਾਂਤ|ਪਿਛਲਖੁਰੀ|ਵਿਸ਼ੇਸ਼-ਵੇਰਵਾ|ਮਾੜੇ ਪ੍ਰਭਾਵ"),
        "ਦ੍ਰਿਸ਼ ਪੇਸ਼ਕਾਰੀ / -ਉਪਰੰਤ / ਸਪੈਸੀਫ਼ਿਕੇਸ਼ਨ / ਸਹਿ-ਪ੍ਰਭਾਵ respectively",
        "OPEN-QUESTIONS.md Q144(b), (d), (e), (g)",
        None,
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
            exempt = (
                [c.span() for c in carve_out.finditer(line)] if carve_out else []
            )
            for m in forbidden.finditer(line):
                start, end = m.span()
                if any(s <= start and end <= e for s, e in exempt):
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
