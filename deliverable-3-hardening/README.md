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
crosswalk maps 66 fields across two source systems. A real deployment ingests DHIS2
exports, HealthTrack dumps, OpenMRS extracts and paper-entry forms, all naming the same
field differently, and the mapping table is currently a CSV that a human edits.

**Fix.** The LLM-proposed, human-confirmed, then cached mapping already argued for in the
stack decision. The model proposes a column mapping once, a person confirms it, and it
becomes a deterministic entry in the crosswalk. Never re-inferred per run, or the same
file parses differently on Tuesday.

**Free win first.** HDX files carry HXL tags, a machine-readable semantic row above the
header. Where the source is HXL-tagged the mapping is a lookup, not a guess, and no model
call is needed at all.

---

## 3. Charts are rendered by a registry that is correct but not yet themeable: adopt Flint

**Decision recorded here rather than acted on now.**

[Flint](https://github.com/microsoft/Flint-chart) is a chart grammar that compiles one
input to Vega-Lite, ECharts, Chart.js, Plotly and Excel, with 70+ semantic types, 10 theme
presets and an MCP server. It is a strong fit for two reasons specific to this engagement:

- **Themes.** A Ministry bulletin has to look institutional. Flint ships presets including
  a `swiss` and an `economist` register that could be overridden with the MoH palette,
  which is exactly the layer this build hand-rolled.
- **Agent authorship.** Flint is a constrained grammar with validation before render. An
  agent authoring a Flint spec cannot hallucinate its way to a broken chart, which is
  meaningfully safer than emitting raw Vega-Lite. That is the real argument, and it
  matters for the "upload a file and it figures out the chart" flow.

**Why it was not adopted now, with the reason stated.** Flint is npm-only, no PyPI
package. At the time the renderer was Python, so adopting it meant adding Node and a
TypeScript build step to a Python pipeline four days from delivery, and the alternative,
`vl-convert-python`, rendered Vega-Lite to SVG with no browser in pure Rust and worked in
the stack that already existed.

**That objection has since evaporated and the decision should be revisited first.** ADR
0010 moved rendering to Astro, so the frontend is already TypeScript and Node is already a
build dependency. The reason Flint was rejected no longer holds. It is now an honest "not
yet on schedule grounds" rather than a "cannot", and it is the first thing to reassess in
hardening.

**What blocks it today.** Mosaic coordinates the explore surface and is built on Observable
Plot; Flint emits Vega-Lite. Composing them means running two chart runtimes, or accepting
that the static and interactive surfaces use different grammars. Resolve that before
adopting, not after.

---

## 4. Nothing runs on a schedule, and no one is told when it fails

**What happens now.** `uv run python run.py && bun run publish`, by hand, by someone who
knows the command.

**Fix.** Hamilton already exposes the DAG, so orchestration is a wrapper rather than a
rewrite. What matters more than the scheduler choice is the failure surface: a quarterly
job that fails silently is worse than no job, because the last good bulletin stays up and
looks current. Publication must be gated on the checks passing, and a failed run must
reach a person.

The four checks in `web/scripts/` are already the gate. Wire them to the schedule.

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
| Analyses the data cannot support | Refused at source by two structural guards, not by reviewer discipline |
| Figures disagreeing across surfaces | `check-agreement.mjs`, six shared figures compared in rendered output |
| A file whose name and contents disagree | `publish.mjs` refuses; the guard exists because it happened |
| Email clipping and unsupported SVG | `check-email.mjs`, measured at 6% of the ceiling |
| House style violations | `check-style.mjs`, four bans, proven to fail |
| Chart palette drifting from the stylesheet | `check-tokens.mjs`, eight colours compared |
| Provenance of every published figure | Lineage record per figure, section 6 |
| Known defects in the source | Published in the bulletin, section 5, not corrected silently |
