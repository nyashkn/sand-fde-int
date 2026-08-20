#!/usr/bin/env bash
# Assemble the 5-page "plain Word document" v3 submission.
#
#   ./submission/build-v3.sh
#
# Same content as v2, restyled to look like an ordinary document typed in
# Microsoft Word and exported to PDF: pure white background, black text,
# Calibri, plain thin-rule tables, ~1in margins. No editorial palette.
#
# Produces submission/sand-fde-submission-v3.pdf. Does NOT touch build.sh,
# build-v2.sh, print.css, v2-print.css, any v2-*.md, 00-cover.md or
# 01-executive-summary.md — v1 and v2 keep building unchanged from their own
# scripts. This is a separate, additive build using only v3-prefixed files.
#
# Same mechanism as build.sh/build-v2.sh: markdown -> bunx marked -> Chrome
# headless --print-to-pdf -> merge with uv run --with pypdf. Hard requirement:
# the final PDF must be <= 5 pages. This script asserts it and exits nonzero
# otherwise.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/submission"
WORK="$OUT/.work-v3"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MAX_PAGES=5

# Single point of control for the architecture data-flow diagram. Another
# workstream is concurrently rebuilding artifacts/06-bulletin-architecture-
# data-flow.html; repoint this one variable at the new file (or a new path
# entirely) and re-run this script — nothing else below needs to change.
ARCHITECTURE_SRC="$ROOT/artifacts/06-bulletin-architecture-data-flow.html"

rm -rf "$WORK"; mkdir -p "$WORK"

render_md_to_pdf() {
  # $1 = space-separated list of markdown files, in order
  # $2 = output pdf path
  local files="$1" target="$2" tag
  tag="$(basename "$target" .pdf)"
  : > "$WORK/$tag.md"
  for f in $files; do
    cat "$OUT/$f" >> "$WORK/$tag.md"
    printf '\n\n<div class="pagebreak"></div>\n\n' >> "$WORK/$tag.md"
  done
  bunx marked --gfm -i "$WORK/$tag.md" > "$WORK/$tag.body.html"
  {
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    echo '<title>Sand FDE submission v3</title><style>'
    cat "$OUT/v3-print.css"
    echo '</style></head><body>'
    cat "$WORK/$tag.body.html"
    echo '</body></html>'
  } > "$WORK/$tag.html"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$target" "file://$WORK/$tag.html" 2>/dev/null
}

echo "==> front matter: p1 (choice/build/findings), p2 (D1 scoping)"
render_md_to_pdf "v3-01-summary.md v3-02-scoping.md" "$WORK/front.pdf"

echo "==> back matter: p5 (D3 hardening + D4 handover)"
render_md_to_pdf "v3-05-hardening-handover.md" "$WORK/back.pdf"

# Architecture figure: p3. Only the data-flow diagram (not the ERD, which v1
# carries in full) plus a short D2 architecture summary, so one page carries
# both the text and the image. Same extraction approach as build.sh/
# build-v2.sh: regex the <style>, the flow <svg> and its <div class="legend">
# out of the artifact rather than printing it whole. The diagram keeps its
# own native colour (KN's objection was to the document's background tint,
# not to a legible figure) — only the page background/ink around it is
# recoloured to match the plain white/black document.
echo "==> architecture artifact: extracting the data-flow figure"
uv run --quiet python - "$ARCHITECTURE_SRC" "$WORK/architecture.html" <<'PY'
import re, pathlib, sys

artifact, out = sys.argv[1:]
html = pathlib.Path(artifact).read_text()

style_m = re.search(r"<style>.*?</style>", html, re.S)
if not style_m:
    sys.exit("architecture artifact: no <style> block found")
# Recolour the artifact's ivory/slate to pure white/black to match the plain
# document. The diagram's own accent colours (clay = custom component, olive
# = bought/adopted) are left untouched — they are the figure's own legible
# colour-coding, not a document-wide accent, and stay per KN's instruction.
style = style_m.group(0).replace("#FAF9F5", "#ffffff").replace("#141413", "#000000")

svgs = re.findall(r"<svg\b.*?</svg>", html, re.S)
legends = re.findall(r'<div class="legend">.*?</div>', html, re.S)
if len(svgs) != 2 or len(legends) != 2:
    sys.exit(
        f"architecture artifact: expected 2 <svg> and 2 .legend (flow + ERD); "
        f"found {len(svgs)} svg(s), {len(legends)} legend(s) — "
        "update the extraction in build-v3.sh to match"
    )

flow_svg, _erd_svg = svgs
flow_legend, _erd_legend = legends

cap = ('<p class="cap">Synthetic test data throughout (assignment CSVs plus a hand-built DHIS2 '
       'sample) &mdash; not real Rwanda health records. Mart ERD and build-vs-buy detail in the '
       'full submission and repository.</p>')

intro = ('<p class="intro">Four layers plus checks plus render (D2 &sect;1.1, condensed). '
         'Sources &rarr; <b>bronze</b> (verbatim, stamped with lineage) &rarr; <b>silver</b> '
         '(melted, crosswalk-resolved to one canonical observation grain) &rarr; <b>gold</b> '
         '(the marts a bulletin reads, plus two seeded statistical checks that always annotate, '
         'never gate) &rarr; publish to Parquet/DuckDB &rarr; render (Astro/Vega-Lite, static '
         'bulletin + email + Superset for the connected office). One Sand product used '
         '(Superset); the crosswalk, per-figure lineage, and the two checks are custom &mdash; '
         'the rest is standard warehouse plumbing, not the reason this took six weeks.</p>')

pathlib.Path(out).write_text(f"""<!doctype html><html><head><meta charset="utf-8">
{style}
<style>
@page {{ size: A4 landscape; margin: 10mm 12mm 11mm; }}
body {{ margin: 0; padding: 4mm; background: #ffffff; font-family: Calibri, Carlito, 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
h2 {{ margin: 0 0 4px; font-size: 13px; color: #000000; }}
.intro {{ font-size: 9.5px; line-height: 1.35; color: #000000; margin: 0 0 6px; max-width: 1100px; }}
svg {{ min-width: 0 !important; width: 100%; height: auto; max-height: 118mm; }}
.cap {{ font-size: 9px; color: #555555; margin-top: 4px; }}
</style>
</head><body>
<h2>D2 &mdash; Solution architecture: data flow, product choices, custom components</h2>
{intro}
{flow_svg}{flow_legend}{cap}
</body></html>""")
print(f"    extracted flow svg + legend -> {out}")
PY

echo "==> architecture figure to pdf"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$WORK/architecture.pdf" "file://$WORK/architecture.html" 2>/dev/null

# Bulletin: p4, one representative page as evidence of output. The opening
# spread carries the synthetic-data disclosure and the headline figures.
BULLETIN="$ROOT/deliverable-2-prototype/output/bulletin-2024-Q1.html"
echo "==> bulletin to pdf (evidence page)"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$WORK/bulletin-full.pdf" "file://$BULLETIN" 2>/dev/null

echo "==> merging"
uv run --quiet --with pypdf python - "$WORK/front.pdf" "$WORK/architecture.pdf" \
  "$WORK/bulletin-full.pdf" "$WORK/back.pdf" "$OUT/sand-fde-submission-v3.pdf" "$MAX_PAGES" <<'PY'
import sys
from pypdf import PdfReader, PdfWriter

front, architecture, bulletin_full, back, target, max_pages = sys.argv[1:]
max_pages = int(max_pages)

def norm(page):
    return " ".join((page.extract_text() or "").split())

front_reader = PdfReader(front)
if len(front_reader.pages) != 2:
    raise SystemExit(
        f"front.pdf: expected exactly 2 pages (v3-01-summary, v3-02-scoping), got "
        f"{len(front_reader.pages)} — content overflowed a page; tighten v3-*.md or v3-print.css"
    )

arch_reader = PdfReader(architecture)
if len(arch_reader.pages) != 1:
    raise SystemExit(
        f"architecture.pdf: expected exactly 1 page, got {len(arch_reader.pages)} — "
        "the intro + diagram overflowed the landscape page, check .work-v3/architecture.html"
    )

back_reader = PdfReader(back)
if len(back_reader.pages) != 1:
    raise SystemExit(
        f"back.pdf: expected exactly 1 page (v3-05-hardening-handover), got "
        f"{len(back_reader.pages)} — content overflowed a page; tighten the markdown or CSS"
    )

writer = PdfWriter()
writer.append(front)
writer.append(architecture)

# One bulletin page as evidence of output: page 0 (headline figures + the
# synthetic-data disclosure the opening spread carries).
bull_reader = PdfReader(bulletin_full)
writer.append(bulletin_full, pages=(0, 1))

writer.append(back)

writer.write(target)
writer.close()

n = len(writer.pages)
if n > max_pages:
    raise SystemExit(f"FAIL: built {n} pages, hard ceiling is {max_pages}. Cut content and rebuild.")

# Sanity: synthetic-data disclosure must be on page 1.
final_reader = PdfReader(target)
p1 = norm(final_reader.pages[0]).lower()
if "synthetic" not in p1:
    raise SystemExit("page 1 does not contain the required synthetic-data disclosure")

print(f"    {n} pages -> {target} (ceiling {max_pages})")
PY

echo "==> done: ${OUT#"$ROOT"/}/sand-fde-submission-v3.pdf"
