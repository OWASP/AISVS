# AISVS PDF Build

Generates the OWASP AISVS standard as a professionally typeset PDF using
[pandoc](https://pandoc.org/) + the
[Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template) LaTeX
template — the same pipeline OWASP ASVS uses.

## Output

`dist/OWASP-AISVS-<version>-RC.pdf`

- A4, single-column, Source Serif 4 / Source Sans 3 typography.
- OWASP-blue title page with the OWASP logo and accent rule.
- Table of contents on its own page, two levels deep.
- Each chapter and appendix starts on a fresh page.
- Running header (`OWASP AISVS` / standard title) and footer (version,
  license, page number) on every page.
- Requirement tables rendered with shaded header rows and zebra striping.

The source markdown already carries its own identifier scheme (`C1`,
`C1.1`, `C1.1.1`), so the build intentionally **does not** add LaTeX
section numbers.

## Prerequisites

```bash
# Toolchain
brew install pandoc tectonic

# Fonts declared in 1.0/en/0x00-Header.yaml
brew install --cask font-source-serif-4 font-source-sans-3
```

`tools/eisvogel.latex` (the template) and `images/owasp_logo_1c_notext.png`
(the title-page logo) are committed in this repo, so no extra downloads are
needed. The first `tectonic` run fetches the required LaTeX packages and
caches them.

## Build

```bash
tools/build-pdf.sh          # builds 1.0/en
tools/build-pdf.sh 1.0 en   # explicit version / language
```

## Design notes

The repository header file `1.0/en/0x00-Header.yaml` is left untouched. All
release styling (colors, running header/footer, page breaks, link colors) is
layered on at build time inside `build-pdf.sh` so the source stays clean and
the look can be tuned in one place.

The OWASP accent color is `#0B5394`.
