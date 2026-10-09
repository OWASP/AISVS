#!/usr/bin/env python3
"""Build the AISVS PDF for one version folder.

Usage:
    python tools/pdf/build_pdf.py 1.01            # writes 1.01/dist/AISVS-1.01.pdf
    python tools/pdf/build_pdf.py 1.02-dev -o out.pdf

The cover title, version and date come from <folder>/en/0x00-Header.yaml.
Chapters are the <folder>/en/0x*.md files in file-name order.
"""

import argparse
import hashlib
import html
import re
import sys
from pathlib import Path

import yaml
from markdown_it import MarkdownIt
from weasyprint import HTML

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CC_BADGE_URL = "https://licensebuttons.net/l/by-sa/4.0/88x31.png"


def slugify(text, used):
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"
    slug, n = base, 2
    while slug in used:
        slug, n = f"{base}-{n}", n + 1
    used.add(slug)
    return slug


def strip_tags(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def render_chapters(en_dir, md):
    used, toc, parts = set(), [], []
    for path in sorted(en_dir.glob("0x*.md")):
        body = md.render(path.read_text(encoding="utf-8"))
        body = body.replace(CC_BADGE_URL, (HERE / "assets" / "cc-by-sa-88x31.png").as_uri())

        def tag_heading(m):
            level, attrs, inner = m.group(1), m.group(2), m.group(3)
            text = strip_tags(inner)
            slug = slugify(text, used)
            cls = ' class="chapter"' if level == "1" else ""
            if level in ("1", "2"):
                toc.append((int(level), text, slug))
            return f'<h{level} id="{slug}"{cls}{attrs}>{inner}</h{level}>'

        body = re.sub(r"<h([1-4])([^>]*)>(.*?)</h\1>", tag_heading, body, flags=re.S)
        # Requirement tables (first header cell is "#") keep the ID column on one line.
        body = re.sub(r"<table>(\s*<thead>\s*<tr>\s*<th[^>]*>#</th>)", r'<table class="req">\1', body)
        # Appendix B inventory tables keep requirement IDs on one line.
        body = re.sub(r"<table>(\s*<thead>\s*<tr>\s*<th[^>]*>[^<]*</th>\s*<th[^>]*>Requirement IDs</th>)", r'<table class="ids">\1', body)
        parts.append(f'<section class="file" data-src="{path.name}">{body}</section>')
    return "\n".join(parts), toc


def render_toc(toc):
    items, open_l1 = [], False
    for level, text, slug in toc:
        link = f'<a href="#{slug}">{html.escape(text)}</a>'
        if level == 1:
            if open_l1:
                items.append("</ul></li>")
            items.append(f'<li class="l1">{link}<ul>')
            open_l1 = True
        else:
            items.append(f'<li class="l2">{link}</li>')
    if open_l1:
        items.append("</ul></li>")
    return '<nav class="toc"><h1>Table of Contents</h1><ul>' + "".join(items) + "</ul></nav>"


def build(folder, output):
    en_dir = REPO / folder / "en"
    if not en_dir.is_dir():
        sys.exit(f"No such folder: {en_dir}")

    raw = (en_dir / "0x00-Header.yaml").read_text(encoding="utf-8")
    header = next(d for d in yaml.safe_load_all(raw) if d)
    version = str(header["subtitle"]).replace("Version", "").strip()
    title = re.sub(r"\s+" + re.escape(version) + r"$", "", str(header["title"]).strip())
    date = str(header.get("date", ""))

    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    chapters, toc = render_chapters(en_dir, md)

    shield = (REPO / "images" / "aisvs-logo-dark.png").as_uri()
    owasp = (HERE / "assets" / "owasp-logo-white.png").as_uri()

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(title)} {html.escape(version)}</title>
<meta name="author" content="OWASP AISVS Project">
<meta name="description" content="{html.escape(title)}, version {html.escape(version)}">
<style>@page {{ @bottom-left {{ content: "OWASP AISVS {html.escape(version)}"; }} }} @page cover {{ @bottom-left {{ content: none; }} }} @page toc {{ @bottom-left {{ content: none; }} }}</style>
</head><body>
<section class="cover"><div class="cover-panel">
  <img class="cover-shield" src="{shield}" alt="AISVS">
  <div class="cover-rule"></div>
  <h1 class="cover-title">{html.escape(title)}</h1>
  <div class="cover-version">VERSION {html.escape(version)}</div>
  <div class="cover-date">{html.escape(date)}</div>
  <img class="cover-owasp" src="{owasp}" alt="OWASP">
  <div class="cover-foot">Open Worldwide Application Security Project (OWASP) Foundation</div>
</div></section>
{render_toc(toc)}
{chapters}
</body></html>"""

    output.parent.mkdir(parents=True, exist_ok=True)
    # Fixed identifier and no creation date keep rebuilds byte-identical when content is unchanged.
    ident = hashlib.sha256(doc.encode("utf-8")).hexdigest()[:32].encode("ascii")
    HTML(string=doc, base_url=str(en_dir)).write_pdf(
        output, stylesheets=[str(HERE / "aisvs.css")], pdf_variant="pdf/ua-1", pdf_identifier=ident
    )
    print(f"Wrote {output.relative_to(REPO) if output.is_relative_to(REPO) else output}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", help="version folder, e.g. 1.01 or 1.02-dev")
    ap.add_argument("-o", "--output", type=Path, help="output PDF path")
    args = ap.parse_args()
    version = args.folder.removesuffix("-dev")
    out = args.output or REPO / args.folder / "dist" / f"AISVS-{version}.pdf"
    build(args.folder, out.resolve())


if __name__ == "__main__":
    main()
