# Provenance: Panjabi Wikipedia word-frequency list

Identical to the sibling ASVS corpus's copy — see that repo's
`5.0/pa-IN/print/pa-wikipedia-wordlist/LICENSE_AND_PROVENANCE.md` for the
full provenance and the reasoning for why this replaced an earlier
Hunspell-based attempt (which was built, tested, and dropped entirely —
never merged — after proving too imprecise for a technical corpus).

Quick summary:
- Source: Leipzig Corpora Collection, `pan_wikipedia_2021_300K` corpus
  (362,065 sentences / 6.19M tokens from pa.wikipedia.org, 2021 crawl).
- Fetched from: https://downloads.wortschatz-leipzig.de/corpora/pan_wikipedia_2021_300K.tar.gz
- License: CC BY (Leipzig Corpora Collection standard).
- `wordlist.tsv` here is the word-frequency list filtered to Gurmukhi-script
  entries only (177,020 of 249,758 original entries).
