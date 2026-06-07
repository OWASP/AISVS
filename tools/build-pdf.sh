#!/usr/bin/env bash
#
# build-pdf.sh — Generate the OWASP AISVS standard as a professionally
# typeset PDF using pandoc + the Eisvogel LaTeX template (the same
# pipeline used by OWASP ASVS).
#
# Requirements (install once):
#   brew install pandoc tectonic
#   brew install --cask font-source-serif-4 font-source-sans-3
#   Eisvogel template at tools/eisvogel.latex
#
# Usage:
#   tools/build-pdf.sh [VERSION_DIR] [LANG]
#   tools/build-pdf.sh            # defaults to 1.0/en
#   tools/build-pdf.sh 1.0 en
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

VERSION="${1:-1.0}"
LANG="${2:-en}"
SRC_DIR="${VERSION}/${LANG}"
TEMPLATE="tools/eisvogel.latex"
OUT_DIR="dist"
OUT_PDF="${OUT_DIR}/OWASP-AISVS-${VERSION}-RC.pdf"

mkdir -p "$OUT_DIR"

echo "==> Source:   $SRC_DIR"
echo "==> Template: $TEMPLATE"
echo "==> Output:   $OUT_PDF"

# --- sanity checks --------------------------------------------------------
command -v pandoc   >/dev/null || { echo "ERROR: pandoc not found";   exit 1; }
command -v tectonic >/dev/null || { echo "ERROR: tectonic not found"; exit 1; }
[ -f "$TEMPLATE" ] || { echo "ERROR: missing $TEMPLATE"; exit 1; }
[ -d "$SRC_DIR" ]  || { echo "ERROR: missing $SRC_DIR"; exit 1; }

# --- assemble the manuscript in reading order -----------------------------
# Header YAML first, then front matter, chapters, then appendices — all by
# lexical filename order, which already encodes the intended sequence.
HEADER_SRC="${SRC_DIR}/0x00-Header.yaml"
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT

# The repo header declares a CJK font (Noto Sans CJK JP) that is not part of
# the build toolchain and is unused by the English text. Drop that one line
# so the build does not hard-depend on a CJK font being installed.
grep -v 'CJKmainfont' "$HEADER_SRC" > "${BUILD_DIR}/header.yaml"

# Ordered content: everything except the header yaml (portable; no mapfile).
CONTENT=()
while IFS= read -r f; do
  CONTENT+=("$f")
done < <(ls "${SRC_DIR}"/*.md | sort)

echo "==> Chapters/sections found: ${#CONTENT[@]}"

# --- design metadata (sleek, professional, OWASP-flavoured) ---------------
# These are layered on at build time so the source header file stays clean.
# Eisvogel variables: https://github.com/Wandmalfarbe/pandoc-latex-template
read -r -d '' DESIGN <<'YAML' || true
---
titlepage: true
titlepage-rule-color: "0B5394"
titlepage-rule-height: 4
titlepage-text-color: "1A1A1A"
toc-own-page: true
toc-depth: 2
colorlinks: true
linkcolor: "owaspblue"
urlcolor: "owaspblue"
toccolor: "owaspink"
fontsize: 10pt
linestretch: 1.15
header-left: "OWASP AISVS"
header-right: "Artificial Intelligence Security Verification Standard"
footer-left: "Version .9 — Working Draft Pre-Release"
footer-center: "CC BY-SA 4.0"
footer-right: "\\thepage"
listings-no-page-break: true
table-use-row-colors: true
disable-header-and-footer: false
header-includes: |
  \definecolor{owaspblue}{HTML}{0B5394}
  \definecolor{owaspink}{HTML}{1A1A1A}
  \usepackage{etoolbox}
  \pretocmd{\section}{\clearpage}{}{}
  \setcounter{secnumdepth}{0}
  \makeatletter
  \@ifundefined{c@none}{\newcounter{none}}{}
  \makeatother
---
YAML
printf '%s\n' "$DESIGN" > "${BUILD_DIR}/design.yaml"

# --- build ----------------------------------------------------------------
echo "==> Running pandoc + tectonic (first run fetches LaTeX packages)…"
pandoc \
  "${BUILD_DIR}/header.yaml" \
  "${BUILD_DIR}/design.yaml" \
  "${CONTENT[@]}" \
  --from=markdown+pipe_tables+yaml_metadata_block \
  --template="$TEMPLATE" \
  --pdf-engine=tectonic \
  --listings \
  --toc \
  --resource-path=".:${SRC_DIR}:images" \
  --metadata=lang:en \
  -o "$OUT_PDF"

echo ""
echo "==> Done: $OUT_PDF"
ls -lh "$OUT_PDF" | awk '{print "    size: "$5}'
