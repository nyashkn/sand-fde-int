# Deliverable 2 — Rapid Prototyping

Working prototype for Problem A: automating the MoH Quarterly Health Bulletin.

## Run it

```bash
cd pipeline
uv sync                          # duckdb, pandas, pyarrow, sf-hamilton
uv run python run.py             # build the mart
uv run python render.py          # render 2024-Q3
uv run python render.py --quarter 2024-Q1
open ../output/bulletin-2024-Q1.html
```

Two commands, no server, no API key, no cloud account. Output is one self-contained HTML
file with no external assets and no JavaScript.

## What it produces

`output/bulletin-<quarter>.html` — the bulletin, with every figure carrying its value, its
state, and a link to the rows and rules behind it. Lineage records live in the same file as
anchors, so it works offline and survives being forwarded.

Four required metrics, one of which is refused:

| Brief requirement | Status |
|---|---|
| Top 10 facilities by volume | rendered — labelled as volume, not quality |
| Maternal health indicators | rendered — bound to ICD-10 perinatal codes |
| Facility performance scores | **reframed** as a capability inventory |
| Trend vs previous quarters | **withheld** — the data has no temporal signal |

The last two are the interesting ones. Both are decided by computed guards, not editorial
judgement, and the bulletin prints the measurement that decided each.

## Layout

```
pipeline/
  run.py                 build the mart          Hamilton -> DuckDB -> Parquet
  render.py              render the bulletin     DuckDB -> HTML
  dataflow/
    bronze.py            source data, verbatim, nothing dropped
    silver.py            canonical observations at DHIS2 grain
    gold.py              the marts a bulletin reads
    guards.py            refuse analyses the data cannot support
  mart/
    crosswalk.csv        source field -> canonical element        (data, not code)
    org_unit_map.csv     (source, key) -> one org_unit identity   (declared, not inferred)
    dhis2_sample.csv     second source, proves the crosswalk
    *.parquet            published artifacts
output/
  bulletin-*.html        the deliverable
```

## Where to put things

| Adding | Goes in |
|---|---|
| A new source system | rows in `crosswalk.csv` + a loader in `bronze.py` |
| A new measure from an existing source | one row in `crosswalk.csv` |
| A facility identity from another system | one row in `org_unit_map.csv` |
| A data quality check | `guards.py`, or a `@check_output` on the silver node |
| A new bulletin panel | a method on `Bulletin` in `render.py` |

## Three decisions worth reading the code for

**`batch` is in the silver key** — `dataflow/silver.py`. The sample ships 2024-01 and
2024-03 twice with differing values. Without batch in the key they collide and one silently
wins, which is the defect rather than a fix for it. Both are retained; figures drawing on
them are provisional and name the conflict.

**Identity resolves through a declared table** — `mart/org_unit_map.csv`. Not exact-key
auto-matching. Two systems using the string `NYA001` is evidence they share a code space,
not proof, and fusing on string equality is how an identity graph merges two distinct real
entities. An unresolved key raises rather than quietly inventing a facility.

**Guards refuse claims, not rows** — `dataflow/guards.py`. Ordinary validation rejects a
bad row. These reject a bad *claim*: a trend line on a series with no temporal signal, or a
pooled correlation that vanishes inside every stratum. They are code rather than a
documented rule because during this engagement the ecological fallacy was explicitly warned
against and then committed three messages later, by the person who raised it.

## Shortcuts taken

- Lineage records are anchors in one file rather than addressable URLs. The contract is the
  same; the explore surface would serve them at `/metric/.../lineage`.
- The batch collision uses a declared arbitrary default (`DEFAULT-BATCH-01`, lowest
  occurrence ordinal) so the pipeline completes. Every figure it touches is provisional.
  Resolution belongs to an analyst, and the queue is specified but not built.
- Gold regenerates fully on every run. Correct and trivially reproducible; would need
  incremental logic at real scale.
- The stratification guard tests against tier only. It should take the stratification
  variable as a declared input per association.

## Specification

Behaviour is specified in `../openspec/specs/` and `../openspec/changes/`. The specs are
deliberately ahead of the code — what is specified and unbuilt is the honest answer to
Deliverable 3, rather than five paragraphs of intent.
