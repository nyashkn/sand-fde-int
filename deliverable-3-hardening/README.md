# Deliverable 3, Production Hardening

Top five things to fix before this runs unattended for a Ministry.

Each is ranked by what happens if it is skipped, not by effort. Every one is grounded in
something this build actually did, and the numbers are reproducible from the repo.

---

## 1. The batch conflict has no resolution path, and it is silently arbitrary

**What happens now.** 2024-01 and 2024-03 each arrived twice with differing values, 234
rows, no timestamp, no submission id, no revision flag. Both loads are internally
consistent, and the directional bias is 113 rows favouring the first against 119 the
second, so nothing in the file establishes which is correct. The pipeline applies
`DEFAULT-BATCH-01`, takes the lowest occurrence ordinal, and marks every derived figure
provisional. All 30 Q1 district figures carry that mark.

**Why it cannot ship as-is.** The default is a coin flip wearing a rule name. A quarter
where 100% of figures are provisional is honest but not useful, and the Ministry has no
way to make it un-provisional.

**Fix.** The conflicts table and triage queue specified in `data-validation`. A named
analyst chooses a batch, the choice is recorded with who and when and why, figures
promote from provisional to settled, and the lineage record shows the human decision.
This is the difference between a pipeline that discloses a problem and one that lets
someone fix it.

**Do not** resolve this by making the pipeline wait for approval. A blocked pipeline in a
Ministry with near-zero IT capacity produces no bulletin at all. Decisions are data, not
control flow: the run always completes, and unresolved figures ship provisional.

---

## 2. Ingestion assumes one file shape, and DHIS2 will not stay still

**What happens now.** `bronze.py` reads five CSVs whose columns were learned by hand. The
crosswalk maps 71 fields across two source systems (66 from the assignment CSVs, 5 from
DHIS2). A real deployment ingests DHIS2 exports, HealthTrack dumps, OpenMRS extracts and
paper-entry forms, all naming the same field differently, and the mapping table is
currently a CSV that a human edits.

**Fix.** The LLM-proposed, human-confirmed, then cached mapping already argued for in the
stack decision. The model proposes a column mapping once, a person confirms it, and it
becomes a deterministic entry in the crosswalk. Never re-inferred per run, or the same
file parses differently on Tuesday.

**Free win first.** HDX files carry HXL tags, a machine-readable semantic row above the
header. Where the source is HXL-tagged the mapping is a lookup, not a guess, and no model
call is needed at all.

---

## 3. The chart runtime question was answered for the static bulletin, and left open for the surface that doesn't exist yet

**What was decided.** Flint (`microsoft/flint-chart`) was adopted. `web/src/lib/charts.ts`
now authors a Flint spec, compiles it to Vega-Lite (`assembleVegaLite`), and renders it to
static SVG with `vega`, headless, in Node at build time. It replaced Observable Plot
outright; nothing in this build still calls Observable Plot.

**On what grounds.** This item originally argued Flint was rejected because it is
npm-only with no PyPI package, and the renderer was Python. That objection evaporated on
its own schedule: ADR 0010 moved rendering to Astro before this item was ever revisited,
so Node and a TypeScript build step were already project dependencies by the time the
question came up again. What tipped the decision from "could" to "should" was narrower
than the original case for Flint: its theme system (a `swiss` preset, narrowly overridden
to this project's exact tokens) removes the literal-hex-duplication problem
`check-tokens.mjs` exists to guard against, which a hand-rolled Observable Plot theme
could not.

**What it actually cost.** Flint's semantic layer deliberately does not expose
colour/font/tick derivation, so two presentation details had no Flint knob: the hatch
fill on provisional bars and the district benchmark rule line. Both are handled by the
documented escape hatch, author the Flint spec, then hand-edit the compiled Vega-Lite
spec for exactly those two things, not by fighting the grammar. Flint's Vega-Lite
compiler also has a real bug: a bar chart using Flint's own auto-generated value-label
layers unions the `y` domain across layers and silently falls back to alphabetical
sorting under specific multi-layer conditions. Worked around by disabling Flint's
auto-labels and hand-authoring one label layer instead; not filed upstream, and worth a
minimal repro if it recurs on a chart shape this bulletin does not yet use. Net cost: one
theme override that still duplicates hex values against `tokens.css` (same guard,
different source shape), one documented compiler workaround, zero new runtime
dependencies beyond what ADR 0010 had already added.

**What is still open, checked against the code as it stands.** The original version of
this item flagged that Mosaic (coordinating an explore surface, built on Observable Plot)
composing against Flint's Vega-Lite output would mean running two chart runtimes. As of
this build, that conflict has not materialised, because the explore surface was never
built: it is referenced in the architecture diagram's product-decision cards and in ADR
0012's honest-limits section as "scoped, not implemented." There is exactly one chart
runtime in this repo today. That is not the same as the question being resolved, it is
the question not having come up yet. ADR 0012 keeps Observable Plot's git history at its
parent commit as the named fallback if Flint or Vega prove unable to render server-side
outside this session's build environment, which is itself still untested.

**Do not** build the explore surface against whichever runtime is closest to hand when
that work starts. Decide explicitly, in writing, whether it extends Flint/Vega-Lite or
brings back Mosaic/Observable Plot for a second runtime, before the first line of that
surface is written. A silent default here is exactly the mistake this item was originally
written down to avoid, and writing the Flint decision down instead of silently deferring
it is the reason it got revisited and actually made.

---

## 4. Nothing runs on a schedule, and no one is told when it fails

**What happens now.** `uv run python run.py && bun run publish`, by hand, by someone who
knows the command.

**Fix.** Hamilton already exposes the DAG, so orchestration is a wrapper rather than a
rewrite. What matters more than the scheduler choice is the failure surface: a quarterly
job that fails silently is worse than no job, because the last good bulletin stays up and
looks current. Publication must be gated on the checks passing, and a failed run must
reach a person.

The five checks in `web/scripts/` are already the gate. Wire them to the schedule.

---

## 5. Facility geography is unusable, and the Health Atlas story depends on it

**What happens now.** `gps_lat` and `gps_lon` are uniform random inside Rwanda's bounding
box for all 117 facilities: every province spans the full country extent, and the
district column is the only real geography in the file. The bulletin therefore maps at
district grain and says so.

**Fix.** The HDX Rwanda Healthsites layer carries 1,345 real facilities with real
coordinates, free and openly licensed. Joining the register to it converts a stated defect
into a working facility layer, and it is the precondition for anything the Health Atlas
would do, including the browser-local geoprocessing path.

**Do not** reverse-geocode the district names to synthesise coordinates. That manufactures
false precision: a district centroid looks surveyed and cannot be distinguished downstream
from a real clinic location. Keep the honest district grain until real points exist.

---

## What is already hardened

Not a to-do list, but the reviewer should know where the line is.

| Concern | State |
|---|---|
| Analyses the data cannot support | Disclosed with a caveat by two structural checks (`temporal_signal_check`, `stratification_check`), not by reviewer discretion. The statistical bar is unchanged (permutation test, stratified-correlation test, fixed seed); ADR 0012 removed the withhold gate that used to render nothing when a claim failed it, and replaced it with a caveat sentence that always renders. Disclosure, not silence, is now the failure mode. |
| Figures disagreeing across surfaces | `check-agreement.mjs`, seven shared figures compared in rendered output |
| A file whose name and contents disagree | `publish.mjs` refuses; the check exists because it happened |
| Email clipping and unsupported SVG | `check-email.mjs`, measured at 6% of the ceiling |
| House style violations | `check-style.mjs`, five bans, proven to fail |
| Chart palette drifting from the stylesheet | `check-tokens.mjs`, nine colours compared |
| Provenance of every published figure | Lineage record per figure, section 6 |
| Known defects in the source | Published in the bulletin, section 5, not corrected silently |
