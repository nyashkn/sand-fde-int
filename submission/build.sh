#!/usr/bin/env bash
# Assemble the single-PDF submission the brief asks for.
#
#   ./submission/build.sh
#
# Produces submission/sand-fde-submission.pdf: the four deliverable documents
# rendered from their markdown sources, followed by the rendered bulletin as the
# "output demonstrating your solution".
#
# Dependencies: bun (for bunx marked), Chrome, uv (for pypdf at merge time).
# Nothing is installed globally; bunx and uv fetch on demand.
#
# ponytail: markdown to HTML to PDF via the browser already on the machine,
# rather than a LaTeX toolchain. Upgrade path if the layout ever needs real
# typesetting is typst, not pandoc.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/submission"
WORK="$OUT/.work"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

rm -rf "$WORK"; mkdir -p "$WORK"

# The document order. Each entry is a markdown file; a bare "---" inserts a page
# break. Keep this list as the single definition of what the submission contains.
DOCS=(
  "$OUT/00-cover.md"
  "$OUT/01-executive-summary.md"
  "$ROOT/deliverable-1-scoping/README.md"
  "$ROOT/deliverable-2-prototype/SOLUTION-DESIGN.md"
  "$ROOT/deliverable-2-prototype/README.md"
  "$ROOT/deliverable-3-hardening/README.md"
  "$ROOT/deliverable-4-handover/README.md"
)
# The three handover documents themselves (runbook, data contract, decision
# register) ship in the repository rather than in this PDF. They ran to nine
# pages, which inverted the brief's own weighting: it asks for 80% of the effort
# on Parts 1 and 2, and the appendix pushed Parts 3 and 4 to a third of the
# document. D4 names them and says where they are.

echo "==> concatenating $(( ${#DOCS[@]} )) documents"
: > "$WORK/all.md"
for f in "${DOCS[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "    MISSING: ${f#$ROOT/}" >&2
    exit 1
  fi
  echo "    ${f#$ROOT/}"
  cat "$f" >> "$WORK/all.md"
  printf '\n\n<div class="pagebreak"></div>\n\n' >> "$WORK/all.md"
done

echo "==> markdown to html"
bunx marked --gfm -i "$WORK/all.md" > "$WORK/body.html"

{
  echo '<!doctype html><html lang="en"><head><meta charset="utf-8">'
  echo '<title>Sand FDE assignment submission</title><style>'
  cat "$OUT/print.css"
  echo '</style></head><body>'
  cat "$WORK/body.html"
  echo '</body></html>'
} > "$WORK/docs.html"

echo "==> docs to pdf"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$WORK/docs.pdf" "file://$WORK/docs.html" 2>/dev/null

# The bulletin is the solution's output. Q1 is the edition the documents discuss,
# because it is the quarter carrying both the batch conflict and a missing month,
# so it exercises every caveat path the build has.
BULLETIN="$ROOT/deliverable-2-prototype/output/bulletin-2024-Q1.html"
echo "==> bulletin to pdf"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$WORK/bulletin.pdf" "file://$BULLETIN" 2>/dev/null

# The architecture artifact carries the rendered data-flow diagram and mart ERD
# that SOLUTION-DESIGN.md's Mermaid block used to gesture at (Mermaid never
# rendered in this pipeline: `bunx marked` emits `<pre><code class=
# "language-mermaid">` and stops, so the PDF used to carry raw diagram
# *definition* text). This artifact is a dated deliverable and stays untouched;
# a generated page is built from pieces extracted out of it instead.
#
# Printing the artifact whole was tried and rejected: both SVGs are fixed at
# viewBox 1489x719 / 1160x520 inside a `.canvas { overflow-x: auto }` designed
# for a scrolling screen, and its build-vs-buy cards section (which duplicates
# the 10-row table in SOLUTION-DESIGN §1.3, and pre-dates a red-team pass that
# revised those verdicts — see 0007) sits physically between the two diagrams,
# so page-break tricks to skip it were fragile. Regex-extracting exactly the
# two <svg>, the <style>, the two .legend divs and the .erd-note div into a
# purpose-built landscape page is deterministic instead: the cards can never
# leak in because their markup is never touched, and the assertions below fail
# the build outright if the artifact's structure ever changes under this.
ARCHITECTURE="$ROOT/artifacts/06-bulletin-architecture-data-flow.html"
echo "==> architecture artifact: extracting figures"
uv run --quiet python - "$ARCHITECTURE" "$WORK/architecture.html" <<'PY'
import re, pathlib, sys

artifact, out = sys.argv[1:]
html = pathlib.Path(artifact).read_text()

style_m = re.search(r"<style>.*?</style>", html, re.S)
if not style_m:
    sys.exit("architecture artifact: no <style> block found")
# Palette handoff: the artifact's ivory/slate are already near-identical to
# the submission's paper/ink (see print.css); only the accent diverges, so
# recolor the "custom component" clay to the submission red rather than
# reskinning the whole thing. Leave olive alone: it separately encodes
# bought/adopted with no equivalent in the submission palette.
style = style_m.group(0).replace("#FAF9F5", "#f6f4ef").replace("#141413", "#161513")

svgs = re.findall(r"<svg\b.*?</svg>", html, re.S)
legends = re.findall(r'<div class="legend">.*?</div>', html, re.S)
erd_note_m = re.search(r'<div class="erd-note">.*?</div>', html, re.S)

# Fail loudly rather than silently dropping a figure if the artifact's markup
# ever changes shape (e.g. a third diagram added, a legend renamed).
if len(svgs) != 2 or len(legends) != 2 or erd_note_m is None:
    sys.exit(
        f"architecture artifact: expected 2 <svg>, 2 .legend, 1 .erd-note; "
        f"found {len(svgs)} svg(s), {len(legends)} legend(s), "
        f"erd-note={'found' if erd_note_m else 'MISSING'} — "
        "update the extraction in build.sh to match"
    )

flow_svg, erd_svg = svgs
flow_svg = flow_svg.replace("#D97757", "#c22029")  # clay -> submission red
flow_legend, erd_legend = legends
erd_note = erd_note_m.group(0)

# Both pages can be lifted/screenshotted on their own and carry no other
# context, so each repeats the synthetic-data disclosure rather than relying
# on the front matter a reader of just this page never saw.
cap = ('<p class="cap">Synthetic test data throughout (assignment CSVs plus a '
       'hand-built DHIS2 sample) &mdash; not real Rwanda health records.</p>')

pathlib.Path(out).write_text(f"""<!doctype html><html><head><meta charset="utf-8">
{style}
<style>
@page {{ size: A4 landscape; margin: 12mm 14mm 14mm; }}
body {{ margin: 0; padding: 6mm; }}
svg {{ min-width: 0 !important; width: 100%; height: auto; }}
.cap {{ font-size: 10px; color: var(--g500); margin-top: 6px; }}
.figure {{ break-after: page; }}
.figure:last-child {{ break-after: auto; }}
</style>
</head><body>
<section class="figure">{flow_svg}{flow_legend}{cap}</section>
<section class="figure">{erd_note}{erd_svg}{erd_legend}{cap}</section>
</body></html>""")
print(f"    extracted 2 svgs, 2 legends, 1 erd-note -> {out}")
PY

echo "==> architecture figures to pdf"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$WORK/architecture.pdf" "file://$WORK/architecture.html" 2>/dev/null

echo "==> merging"
# Only representative pages of the bulletin ship in the PDF. The full four
# editions are live at the URL cited in the documents, and rendered in the
# repository. Carrying all ten pages made the output section a quarter of the
# submission for something the reader can open in a browser.
uv run --quiet --with pypdf python - "$WORK/docs.pdf" "$WORK/bulletin.pdf" "$WORK/architecture.pdf" "$OUT/sand-fde-submission.pdf" <<'PY'
import sys
from pypdf import PdfReader, PdfWriter

docs, bulletin, architecture, target = sys.argv[1:]

# pypdf's text extraction drops the "fi"/"fl" ligatures Iowan Old Style (the
# submission's --serif) renders as single glyphs ("figure-level" ->
# "gure-level"), and line-wraps introduce inconsistent whitespace. Every
# search below goes through this rather than a raw `in` check.
def norm(page):
    return " ".join((page.extract_text() or "").split())

writer = PdfWriter()

docs_reader = PdfReader(docs)
# Splice the architecture figures in mid-document, right where SOLUTION-DESIGN
# §1.1 refers to them, rather than tacking them on after the bulletin. The
# split point is the page carrying that reference sentence — found by search,
# not a fixed index, same as everything else here. Both docs_split_at and the
# sentinel avoid "fi"/"fl" (the ligature-drop hazard above).
docs_split_at = None
for i, page in enumerate(docs_reader.pages):
    if "product-decision cards" in norm(page).lower():
        docs_split_at = i
        break
if docs_split_at is None:
    raise SystemExit(
        "docs.pdf: reference sentence to the architecture figures not found — "
        "SOLUTION-DESIGN.md §1.1 wording changed, update the sentinel in build.sh "
        "(falling back to appending the figures at the end is NOT done "
        "automatically so this doesn't fail silently)"
    )
writer.append(docs, pages=(0, docs_split_at + 1))

# The architecture page is generated (see the extraction step above), not
# selected by search: it is always exactly the dataflow diagram followed by
# the ERD, nothing else, so every page ships.
arch_reader = PdfReader(architecture)
if len(arch_reader.pages) != 2:
    raise SystemExit(
        f"architecture.pdf: expected exactly 2 pages (dataflow, ERD), got "
        f"{len(arch_reader.pages)} — the generated figure page overflowed or "
        "underflowed, check $WORK/architecture.html"
    )
writer.append(architecture)
writer.append(docs, pages=(docs_split_at + 1, len(docs_reader.pages)))

reader = PdfReader(bulletin)
# The opening spread carries the synthetic-data disclosure, the headline figure
# and the first chart. Then find the tier-confound section, which is the
# strongest analytical page and is located by its heading rather than a fixed
# index, so it survives the bulletin's layout changing. (Other workstreams are
# concurrently regenerating this bulletin file — the page count and index
# below are expected to move; only the search result matters.)
keep = [0, 1, 2]
for i, page in enumerate(reader.pages):
    if "Tier confound" in norm(page) and i not in keep:
        keep.append(i)
        break
writer.append(bulletin, pages=sorted(keep))

writer.write(target)
writer.close()

# Positive checks: the two figures actually rendered with real content, not a
# blank or clipped canvas (SVG text nodes extract as real text via pypdf).
final_reader = PdfReader(target)
final_text = " ".join(norm(p) for p in final_reader.pages)
for needed in ("SOURCES INGEST CANONICAL MARTS", "canonical hub"):
    if needed.lower() not in final_text.lower():
        raise SystemExit(
            f"expected text {needed!r} not found anywhere in the built PDF — "
            "the architecture dataflow/ERD figure did not render as expected"
        )

# Regression guard for the defect this build step fixed: raw Mermaid source
# (`flowchart TD ...`) must never again land in the PDF as literal text.
for i, page in enumerate(final_reader.pages):
    if "flowchart TD" in norm(page):
        raise SystemExit(
            f"flowchart TD literal text found on merged page {i + 1} — "
            "unrendered Mermaid source leaked into the PDF"
        )

print(f"    {len(writer.pages)} pages -> {target}")
print(f"    architecture figures inserted after docs page {docs_split_at + 1}, "
      "immediately following §1.1's reference to them")
print(f"    bulletin pages included: {[i + 1 for i in sorted(keep)]} of {len(reader.pages)} (may shift — see comment above)")
PY

echo "==> done: ${OUT#"$ROOT"/}/sand-fde-submission.pdf"
