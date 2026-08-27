#!/usr/bin/env bash
#
# build-print-pdf.sh
#
# Bilingual (English/Gurmukhi) PDF builder for OWASP AISVS 1.0 Panjabi Edition
#
# Converts consolidated markdown to a print-ready PDF with Gurmukhi-capable fonts
# and binder-safe margins (1.25in left, 0.75in right/top/bottom).
#
# Reused as-is from the sibling OWASP ASVS 5.0 Panjabi print pipeline
# (../../../../OWASP-Panjabi/5.0/pa-IN/print/build-print-pdf.sh) — same
# geometry, same font, same debugged pandoc invocation. See that repo's
# print/ directory for the issues this configuration already resolved
# (eisvogel.tex missing packages -> pandoc default template; monofont must
# match mainfont or Gurmukhi text inside inline code renders as tofu boxes).
#
# USAGE:
#   ./build-print-pdf.sh <input.md> <output.pdf>
#   ./build-print-pdf.sh OWASP-AISVS-1.0-pa-IN-print.md OWASP-AISVS-1.0-pa-IN.pdf
#
# REQUIREMENTS:
#   - pandoc 3.0+
#   - xelatex or lualatex (for Gurmukhi Unicode support)
#   - Gurmukhi-capable font installed (e.g., Mukta Mahee, Gurmukhi MN)
#
# GEOMETRY:
#   Binder-safe margins for 3-hole punch, single-sided:
#   - left: 1.25in (binding margin)
#   - right: 0.75in
#   - top: 1in
#   - bottom: 1in
#
# FONT:
#   Default: Mukta Mahee (supports both Gurmukhi and Latin scripts).
#   NOTE: Mukta Mahee has no glyph for → (U+2192) or ‑ (U+2011 non-breaking
#   hyphen) — the print/chapters/*.md source should already use ASCII "->"
#   and "-" instead (see the print-safety rules baked into the assembly
#   step). If you see "Missing character" warnings for either, the source
#   markdown needs the same fix applied to the ASVS corpus.
#
# PDF ENGINE:
#   - xelatex (default; faster, broader compatibility)
#   - lualatex (alternative; if xelatex fails)
#

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

# Font for bilingual content (Gurmukhi + Latin) — used for BOTH mainfont and
# monofont, so inline code containing Gurmukhi text (e.g. quoted headings in
# footnotes) doesn't fall back to a Latin-only monospace font.
MAINFONT="${MAINFONT:-Mukta Mahee}"

# PDF engine: xelatex or lualatex
PDF_ENGINE="${PDF_ENGINE:-xelatex}"

# Print geometry: binder-safe single-sided 3-hole punch
# Geometry must be passed as ONE value to Pandoc
GEOMETRY="left=1.25in,right=0.75in,top=1in,bottom=1in,includehead=true,includefoot=true"

# ============================================================================
# MAIN
# ============================================================================

main() {
  local input_file="${1:-}"
  local output_file="${2:-}"

  if [[ -z "$input_file" || -z "$output_file" ]]; then
    usage
    exit 1
  fi

  if [[ ! -f "$input_file" ]]; then
    echo "ERROR: Input file not found: $input_file" >&2
    exit 1
  fi

  echo "Building PDF: $input_file → $output_file"
  echo "  Engine: $PDF_ENGINE"
  echo "  Font: $MAINFONT"
  echo "  Geometry: $GEOMETRY"
  echo ""

  pandoc \
    "$input_file" \
    --from markdown \
    --to pdf \
    --pdf-engine "$PDF_ENGINE" \
    -V mainfont="$MAINFONT" \
    -V monofont="$MAINFONT" \
    -V geometry="$GEOMETRY" \
    -o "$output_file"

  if [[ -f "$output_file" ]]; then
    local size
    size=$(ls -lh "$output_file" | awk '{print $5}')
    echo ""
    echo "SUCCESS: PDF created at $output_file ($size)"
  else
    echo "ERROR: PDF generation failed" >&2
    exit 1
  fi
}

usage() {
  cat >&2 <<'EOF'
USAGE:
  build-print-pdf.sh <input.md> <output.pdf>

EXAMPLES:
  build-print-pdf.sh OWASP-AISVS-1.0-pa-IN-print.md OWASP-AISVS-1.0-pa-IN.pdf
  PDF_ENGINE=lualatex ./build-print-pdf.sh input.md output.pdf

ENVIRONMENT VARIABLES:
  MAINFONT              Font name (default: Mukta Mahee)
  PDF_ENGINE            xelatex or lualatex (default: xelatex)

EOF
}

main "$@"
