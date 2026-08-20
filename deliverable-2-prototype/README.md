# Deliverable 2, Rapid Prototyping

Working prototype for Problem A: automating the MoH Quarterly Health Bulletin.

## Run it

```bash
cd pipeline
uv sync                          # duckdb, pandas, pyarrow, sf-hamilton
uv run python run.py             # build the mart
cd web && bun install
bun run publish                  # build + publish all four quarters, 2024-Q1 through 2024-Q4
bun run verify                   # build, inline email, run all five checks
open ../output/bulletin-2024-Q1.html
```

Two commands, no server, no API key, no cloud account. Output is one self-contained HTML
file with no external assets and no JavaScript.

## Solution design (D2 §1)

`../artifacts/06-bulletin-architecture-data-flow.html`. Two diagrams: the data-flow
pipeline (sources through Bronze/Silver/Gold to the published surfaces), which Sand
products are used and why, what is built custom and why, build vs. buy per component; and
the data-mart ERD (not a normalized schema, six source files unpivoted through one
crosswalk into one canonical fact table).

The written counterpart, same reasoning in prose and tables, standing alone without the
HTML artifact, is `SOLUTION-DESIGN.md`.

## What it produces

`output/bulletin-<quarter>.html`, one edition per quarter, all four built by `bun run
publish`, with every figure carrying its value, its state, and a link to the rows and
rules behind it. Lineage records live in the same file as anchors, so it works offline and
survives being forwarded.

Four required metrics, two answered directly and two substituted, with the substitution
stated rather than papered over:

| Brief requirement | Status |
|---|---|
| Top 10 facilities by volume | rendered, labelled as volume, not quality |
| Maternal health indicators | **substituted.** The brief names ANC visits, deliveries and complications. The provided CSVs carry deliveries, but no ANC column and no complication column. What ships is neonatal cause of death (ICD-10 P21, P07, P36, Q00 to Q99) and the stillbirth ratio, which are perinatal outcomes, not maternal ones. |
| Facility performance scores | **partly substituted.** Reporting completeness ships. Timeliness does not and cannot: no source file carries a submission timestamp, so no lag is derivable. What ships instead is governance, operations and staffing capability per tier, section 3. Nothing is scored per facility. |
| Trend vs previous quarters | shown, caveated: all four quarters, not a two-point delta |

**What would close the gap.** ANC visits, maternal complications and reporting timeliness
are all standard DHIS2 data elements. Ingesting them is a Week 2 crosswalk addition, not a
pipeline change: the crosswalk already resolves six heterogeneous sources to one grain, and
these are three more rows in it. The reason they are absent is the provided extract, not the
design. Claiming them as delivered would have been the easier sentence to write and the
first thing a reviewer checked.

Facility performance and the trend were the interesting ones to build. `governance.csv`/`operations.csv`/
`healthcare_workers.csv` were already resolved through the crosswalk and never queried
past three covariates; the trend was withheld because a guard blocked the whole section
rather than stating what it could and could not support. Both are gold-layer queries
against data already in the mart, not new ingestion. Every check still computes exactly
what it always computed; it now always renders its finding, caveated, never gated.

## Layout

```
pipeline/
  run.py                 build the mart          Hamilton -> DuckDB -> Parquet
  eda.py                 marimo notebook, all five source files, reuses gold/checks
  web/                   render every surface    Parquet -> HTML
  dataflow/
    bronze.py            source data, verbatim, nothing dropped
    silver.py            canonical observations at DHIS2 grain
    gold.py              the marts a bulletin reads, incl. facility_capability
    checks.py            annotate analyses the data may not fully support
  mart/
    crosswalk.csv              source field -> canonical element      (data, not code)
    org_unit_map.csv           (source, key) -> one org_unit identity (declared, not inferred)
    cause_capability_links.csv cause of death -> the capability that treats it (declared)
    known_contradictions.csv   crosswalk notes worth stating as findings (declared)
    dhis2_sample.csv           second source, proves the crosswalk
    *.parquet                  published artifacts
output/
  bulletin-*.html        the deliverable, one per quarter
```

## Where to put things

| Adding | Goes in |
|---|---|
| A new source system | rows in `crosswalk.csv` + a loader in `bronze.py` |
| A new measure from an existing source | one row in `crosswalk.csv` |
| A facility identity from another system | one row in `org_unit_map.csv` |
| A data quality check | `checks.py`, or a `@check_output` on the silver node |
| A cause-of-death to capability pairing | one row in `cause_capability_links.csv` |
| A new bulletin panel | a section in `web/src/pages/index.astro` |

## Three decisions worth reading the code for

**`batch` is in the silver key**, `dataflow/silver.py`. The sample ships 2024-01 and
2024-03 twice with differing values. Without batch in the key they collide and one silently
wins, which is the defect rather than a fix for it. Both are retained; figures drawing on
them are provisional and name the conflict.

**Identity resolves through a declared table**, `mart/org_unit_map.csv`. Not exact-key
auto-matching. Two systems using the string `NYA001` is evidence they share a code space,
not proof, and fusing on string equality is how an identity graph merges two distinct real
entities. An unresolved key raises rather than quietly inventing a facility.

**Checks annotate claims, never gate rows**, `dataflow/checks.py`. Ordinary validation
rejects a bad row. These annotate a *claim*: a trend line on a series with no measured
temporal signal, or a pooled correlation that vanishes inside every stratum. The statistics
are unchanged from when they gated content (ADR 0008); what changed (ADR 0012) is the
consumer contract, a check's finding now always renders with a caveat, never hides the
section it qualifies.

## Shortcuts taken

- Lineage records are anchors in one file rather than addressable URLs. The contract is the
  same; the explore surface would serve them at `/metric/.../lineage`.
- The batch collision uses a declared arbitrary default (`DEFAULT-BATCH-01`, lowest
  occurrence ordinal) so the pipeline completes. Every figure it touches is provisional.
  Resolution belongs to an analyst, and the queue is specified but not built.
- Gold regenerates fully on every run. Correct and trivially reproducible; would need
  incremental logic at real scale.
- The stratification check tests against tier only. It should take the stratification
  variable as a declared input per association.

Further shortcuts (the second source is synthetic, no scheduler, no auth, GPS excluded as
fabricated, single-machine DuckDB), the Week 3 plan, and what building this surfaced about
the capability-mortality correlation, are in `SOLUTION-DESIGN.md` §3.

## Specification

Behaviour is specified in `../openspec/specs/` and `../openspec/changes/`. The specs are
deliberately ahead of the code, what is specified and unbuilt is the honest answer to
Deliverable 3, rather than five paragraphs of intent.

## Checks

`bun run verify` runs five. Four caught a real defect in this build; one is preventive and
is marked as such, because a table claiming otherwise would be the first thing to check:

| Check | Holds | Caught |
|---|---|---|
| `check-shipped.mjs` | every declared input the pipeline reads by name is tracked by git | `known_contradictions.csv` and `cause_capability_links.csv`, both read by `gold.py` and neither ever added, so a clone raised `FileNotFoundError` on the first command. Every other check ran against the working tree, where they exist |
| `check-tokens.mjs` | chart theme colours identical to `tokens.css` | nothing yet. Preventive: added when the chart engine moved to a `THEME_SPEC` override, and it guards the same drift class the previous hand-typed palette had |
| `check-style.mjs` | em dashes, side stripes, script tags, external assets | a latent em dash, and a false positive in its own first rule |
| `check-email.mjs` | 102 KB clip ceiling, no SVG, no flex or grid, state as words | `display:grid` shipped in the email stylesheet |
| `check-agreement.mjs` | seven shared figures identical across both surfaces | email published 6 withheld panels where the bulletin said 2; later, the trend/correlation caveat wording after the withhold gate was removed |

`bun run publish` additionally refuses to write a file whose name and contents disagree
on the quarter. That guard exists because the unchecked version shipped `bulletin-2024-Q3.html`
containing Q1 figures.
