#!/usr/bin/env python3
"""Dictionary-backed spelling check for the AISVS pa-IN corpus, using a
177k-word Panjabi Wikipedia frequency list (pa-wikipedia-wordlist/wordlist.tsv,
CC BY, Leipzig Corpora Collection — see
pa-wikipedia-wordlist/LICENSE_AND_PROVENANCE.md for the full story,
including why this replaced an earlier Hunspell-based attempt that didn't
work, documented in the sibling ASVS corpus).

Design: flag a word only when BOTH:
  1. it appears exactly ONCE in this corpus (no established repeated use), AND
  2. it does not appear in the 177k-word Wikipedia list, AND
  3. it is not in the ALLOWLIST below (this corpus's own specialized/coined
     AI-security vocabulary that legitimately won't appear in general
     Wikipedia prose).

Real dictionary membership check, not fuzzy matching. Every flag is a
hypothesis for human review against CLAUDE.md's dictionary sources, same
as this project's other spelling checks.

Zero-dep (stdlib only).

Usage: python3 verify-spelling-wikipedia.py
Exit 0 = clean. Exit 1 = candidates found.
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # .../pa-IN
WORDLIST_PATH = Path(__file__).resolve().parent / "pa-wikipedia-wordlist" / "wordlist.tsv"
SKIP_FILES = {"CLAUDE.md", "TRANSLATION-RULES.md", "GLOSSARY.md", "OPEN-QUESTIONS.md"}

GURMUKHI = r"਀-੿"
WORD_RE = re.compile(f"[{GURMUKHI}]+")
MIN_WORD_LEN = 3

# This corpus's own specialized/coined AI-security vocabulary that
# legitimately won't appear in general Panjabi Wikipedia prose. Grown from
# review passes — see individual commit messages.
ALLOWLIST = {
    # -ਯੋਗ/-ਯੋਗਤਾ "-able/-ability" compounds (ਟੈਸਟ+ਯੋਗ, ਪਰਖ+ਯੋਗਤਾ, etc.)
    "ਟੈਸਟਯੋਗ", "ਪਰਖਯੋਗਤਾ", "ਨਿਰੀਖਣਯੋਗਤਾ", "ਲਾਗੂਕਰਨਯੋਗ", "ਨਿਰਧਾਰਨਯੋਗ",
    "ਲਗਾਉਣਯੋਗ", "ਆਡਿਟਯੋਗ", "ਪ੍ਰਵਾਨਯੋਗ", "ਵਿਆਖਿਆਯੋਗ", "ਕੱਢਣਯੋਗ",

    # Loanwords + Panjabi oblique-plural/inflection suffixes (-ਾਂ/-ਰਾਂ/-ਵਾਂ)
    "ਟੈਸਟਰਾਂ", "ਵਰਕਫ਼ਲੋਜ਼", "ਬਚਾਵਾਂ", "ਵਰਗੀਕਾਰਾਂ", "ਪ੍ਰਮਾਣਿਕਤਾਵਾਂ",
    "ਐਂਡਪੌਇੰਟਾਂ", "ਚੈੱਕਸਮਾਂ", "ਸਕੋਪਾਂ", "ਆਊਟਪੁੱਟਾਂ", "ਪ੍ਰੋਫ਼ਾਈਲਾਂ",
    "ਪੱਖਪਾਤਾਂ", "ਪ੍ਰਤੀਨਿਧਤਾਵਾਂ", "ਮਾਡਿਊਲਾਂ", "ਐਨੋਟੇਟਰਾਂ", "ਸਰਟੀਫ਼ਿਕੇਟਾਂ",
    "ਬਿਲਡਾਂ", "ਵਹਾਵਾਂ", "ਐਕਟੀਵੇਸ਼ਨਾਂ", "ਪਲੱਗਇਨਾਂ", "ਡਾਈਜੈਸਟਾਂ",
    "ਰਨਟਾਈਮਾਂ", "ਇੰਟਰਕਨੈਕਟਾਂ", "ਅਡੈਪਟਰਾਂ", "ਨੇਮਸਪੇਸਾਂ", "ਓਵਰਰਾਈਡਾਂ",
    "ਵਰਕਸਪੇਸਾਂ", "ਰਨਰਾਂ", "ਫ਼ੋਰਕਾਂ", "ਬਾਈਨਰੀਆਂ", "ਰਿਪੌਜ਼ਟਰੀਆਂ", "ਜੌਬਾਂ",
    "ਸੰਭਾਲਕਰਤਾਵਾਂ", "ਜਾਰੀਕਰਤਾਵਾਂ", "ਰਾਖਿਆਂ", "ਰਿਕੁਐਸਟਾਂ", "ਮਰਜਾਂ",
    "ਨਾਕਾਮੀਆਂ",

    # Loanwords (transliterated technical/security terms, often glossed inline)
    "ਸ਼ੇਅਰਅਲਾਈਕ", "ਲੌਕਫ਼ਾਈਲ", "ਰਿਡੈਕਟ", "ਸੈਨੀਟਾਈਜ਼", "ਚੈੱਕਪੁਆਇੰਟ",
    "ਇੰਟਰਕਨੈਕਟ", "ਟੋਕਨਾਈਜ਼", "ਕਲੱਸਟਰਿੰਗ", "ਆਰਕੈਸਟ੍ਰੇਟਰ", "ਬੈਂਚਮਾਰਕਿੰਗ",
    "ਡੀਬੱਗਿੰਗ", "ਹਾਈਪਰਪੈਰਾਮੀਟਰ", "ਫ਼ਾਲਟ", "ਕਾਨਸੈਪਟ", "ਡਿਸਟਿਲੇਸ਼ਨ",
    "ਸਰਟੀਫ਼ਾਈ", "ਐਨੋਟੇਟਰ", "ਜਨਰੇਟਿਵ", "ਸਪੈਸੀਫ਼ਿਕੇਸ਼ਨ", "ਗੁਮਨਾਮੀਕਰਨ",
    "ਚੈੱਕਸਮ", "ਸਨੈਪਸ਼ਾਟਿੰਗ", "ਪੈਰਾਫ਼ਰੇਜ਼", "ਥ੍ਰੌਟਲਿੰਗ", "ਪਰਖੋ",
    "ਕ੍ਰਿਪਟੋਗ੍ਰਾਫ਼ੀ", "ਫ਼ਜ਼", "ਹਾਰਨੈੱਸ", "ਕੋਪਾਇਲਟ", "ਇਨਲਾਈਨ", "ਚੈੱਕਆਊਟ",
    "ਪ੍ਰੋਫ਼ਾਈਲਿੰਗ", "ਸਟਾਈਲੋਮੈਟ੍ਰਿਕ", "ਫ਼ੌਰੈਂਸਿਕ", "ਟੇਬਲਟੌਪ", "ਰਿਕੁਐਸਟ",

    # Panjabi compounds/derivations coined for this corpus (root + standard
    # productive suffix: -ਪਰਕ "-ive", -ਕਰਨ/-ਈਕਰਨ "-ization", -ਬੰਦੀ "-ing/binding",
    # -ਆਨਾ "-ish/-like", -ਈ "-ness/adjectival", -ਕਾਰ/-ਕਰਤਾ "-er")
    "ਵਸਤੂਪਰਕ", "ਸ਼ਬਦਬੰਦੀ", "ਮਕਸਦੀ", "ਪ੍ਰਮਾਣੀਕ੍ਰਿਤ", "ਸੀਮਾਬੰਦੀ",
    "ਦੁਸ਼ਮਣਾਨਾ", "ਤਫ਼ਤੀਸ਼ਕਾਰ", "ਦੁਵਿਧਾਪੂਰਨ", "ਸਧਾਰਨੀਕ੍ਰਿਤ", "ਅਸਰਦਾਰੀ",
    "ਇਨਸਾਫ਼ੀ", "ਰਖਾਅ",

    # Ordinary inflected Panjabi verb/adjective forms
    "ਪਹੁੰਚਣੇ", "ਉਲਟਾਈਆਂ", "ਉਲਟਾਏ", "ਪੁੱਗਣਾ", "ਅਪਣਾਓ", "ਖੁੰਝਾਉਣਾ",
    "ਛਾਣਿਆ", "ਛਾਣੋ", "ਟਾਲਣਾ", "ਵਿਗੜਦੀਆਂ", "ਪਰੋਸਣੇ",
}


def load_wordlist():
    if not WORDLIST_PATH.exists():
        print(f"ERROR: word list not found at {WORDLIST_PATH} — see "
              f"{WORDLIST_PATH.parent}/LICENSE_AND_PROVENANCE.md for how to fetch it.",
              file=sys.stderr)
        sys.exit(2)
    words = set()
    with WORDLIST_PATH.open(encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts and parts[0]:
                words.add(parts[0])
    return words


def collect_words():
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
    wiki_words = load_wordlist()
    counts, locations = collect_words()
    once_words = [w for w, c in counts.items() if c == 1]

    findings = [w for w in once_words if w not in wiki_words and w not in ALLOWLIST]
    findings.sort(key=lambda w: locations[w])

    for w in findings:
        fname, lineno = locations[w]
        print(f"{fname}:{lineno}: [spelling-wikipedia] {w!r} (1x, only occurrence in corpus) "
              f"not found in the Panjabi Wikipedia word list — verify against CLAUDE.md's "
              f"dictionary sources before treating as a typo")

    if findings:
        print(f"\n{len(findings)} spelling candidate(s) found out of {len(once_words)} "
              f"once-only words checked — hypotheses, not confirmed errors.", file=sys.stderr)
        return 1
    print(f"Wikipedia-wordlist spelling check: clean — every once-only word ({len(once_words)} "
          f"checked) is either in the 177k-word Wikipedia list or the corpus allowlist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
