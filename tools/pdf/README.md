# AISVS PDF build

Builds the release PDF for a version folder with the same layout as the AISVS 1.0 PDF.

```sh
pip install -r tools/pdf/requirements.txt
python tools/pdf/build_pdf.py 1.01        # writes 1.01/dist/AISVS-1.01.pdf
python tools/pdf/build_pdf.py 1.02-dev -o /tmp/preview.pdf
```

The cover title, version and date come from `<folder>/en/0x00-Header.yaml`. Chapters are the `<folder>/en/0x*.md` files in file-name order. The table of contents, PDF bookmarks and page footers are generated.

Fonts: Helvetica if installed (macOS), otherwise Liberation Sans, which has the same metrics. Font choice can move a line break, so rebuild and commit the PDF from one machine per release.

Only rebuild the PDF for a version before it is released. Released `dist/` folders are locked.
