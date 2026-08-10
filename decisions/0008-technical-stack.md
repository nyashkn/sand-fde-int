# 0008, Technical stack: Hamilton + DuckDB/Parquet batch, browser-first surfaces

- **Date:** 2026-08-10
- **Status:** Accepted
- **Method:** measured against the provided sample data; every rejection has a stated number or a stated constraint

## Context

ADR 0006 committed to Problem A plus one bounded handover act, and promoted end-to-end
figure traceability to a requirement after the council found the Director's complaint is
about trust rather than throughput.

That decision constrains the stack more than the feature list does. Two things follow:

1. Every figure a human reads must be traceable to the rows that produced it, so lineage
   has to be a property of the pipeline rather than documentation beside it.
2. The deliverable's success is defined by a **named Digital Health Officer restarting the
   pipeline unassisted before exit**. Every dependency added lowers the odds of that.

The brief's infrastructure line is also binding, not colour: unreliable power (4-6 hrs/day
rural) and spotty 3G/4G. A server-round-trip dashboard fails in exactly the districts with
the worst outcomes.

## Decision

**The dependency test.** Any dependency must pass: *can the named DHO restart this alone,
at 2am, with no internet?* If not, it needs a stronger justification than convenience.
This is the rule that settles most stack arguments below.

**Batch, Python + Apache Hamilton + DuckDB + Parquet.**
Hamilton derives its DAG from function parameter names, so the compute lineage of every
figure is generated from the code rather than maintained beside it. `@check_output` puts
named validation rules (DUP-01 and the rest) on the nodes they guard. Pure Python, so a
failure is a traceback the DHO can read. It also runs under Pyodide (tryhamilton.dev), and
GeoLibre already ships a Pyodide kernel, so the same module can run in the batch job and
in the browser.

**Two surfaces, one substrate.**
- Bulletin, published, HTML, embedded in email. Static render, no JavaScript, inline CSS,
  table layout, charts as images. Capability metrics only. Every figure deeplinked.
- Explore, interactive. Mosaic coordinator over DuckDB-WASM. Toggleable context layers.
  Hydrates filter state from deeplink URL params.

**Charts, Flint (microsoft/flint-chart).** One spec compiles to a static Vega-Lite render
for the email and an interactive backend for the page. Ten theme presets give a government
bulletin an institutional look without days of CSS. Its MCP server and constrained grammar
make agent-authored charts validatable, which raw Vega-Lite or D3 would not be.

**Mart, medallion in DuckDB, Parquet on disk, silver at DHIS2 grain**
`(org_unit, period, data_element, value)` plus `source_system`, `ingested_at`,
`rule_applied`, `quality_flags`. Rwanda runs DHIS2, so this is the country's own shape,
not an invented one. Parquet over HTTP range requests means the same files serve the
Python batch and the browser, no API between them, and they cache for offline use.

**Standards, bind, do not invent.** DHIS2 data model (silver grain), ICD-10 perinatal
P-codes for cause of death, WHO GHO indicator definitions, HXL for humanitarian context
layers, ADX as the exchange envelope. Mapping lives in a crosswalk **table**
`(source_system, source_field, canonical_element, code_system, code)`, never an in-code
rename, bronze must stay auditable against the file the MoH actually sent.

**Geography, district grain only.** `gps_lat`/`gps_lon` in the sample are uniform random
within Rwanda's bbox (every province spans the full country extent), so facility-point
mapping is impossible. District and province strings are correct 30/30 against real Rwanda
administrative structure. Choropleth on FAO GAUL level2; HDX Rwanda Healthsites (1,345 real
facilities) as basemap context.

## Alternatives

- **DBOS for durable orchestration**, rejected. Durable execution solves crash-and-resume
  for long workflows; this is a quarterly batch that runs in seconds, where re-running is
  cheaper than making it durable. It needs a live process plus a database, so it cannot
  serve the browser surface either. Decisively, it fails the dependency test: it is a
  runtime the DHO would have to understand to debug. The power-outage argument is the best
  case for it and still fails, the pipeline runs at the central MoH office, not in a rural
  facility.
- **Google Earth Engine for raster covariates**, rejected on two grounds. Analytically:
  NMR is explained by capability, not geography (`staff_trained_on_protocol` r=-0.844,
  volume r=-0.832, `cpap_machines` r=-0.811) while `avg_referral_time_hrs`, the variable a
  travel-time raster would proxy, is r=+0.125, and monthly NMR sd is 0.77 so there is no
  seasonality to explain. Operationally: HDX publishes rainfall and NDVI already aggregated
  to subnational units as CSV, and a submission repo that needs a Google Cloud project to
  run is a worse deliverable. Raster layers are basemap context only, never explanation.
- **Apache Superset for the dashboard**, not rejected, scoped. Superset is server-rendered
  and needs a live connection, so it fails in the low-power districts. It still serves the
  central MoH office, where power and connectivity are fine. Two audiences, two tools, one
  data model.
- **Turborepo / pnpm monorepo scaffold**, rejected for now. Two apps (Python pipeline,
  browser frontend) do not justify workspace tooling built for coordinating many packages.
  Adopt the conventions (`.agents/skills/` in-repo, a "where to put things" table, one
  shared contract package); add the tooling the day a third app appears.
- **Forking GeoLibre**, rejected. 1,615+ files including Tauri, iOS and Android builds,
  and app-store workflows: a maintenance surface far exceeding a 6-week deliverable. Lift
  four patterns instead, the Pyodide worker, MapLibre + DuckDB-WASM wiring, the
  project-format concept, and COG/PMTiles handling.
- **FHIR**, rejected as category error. FHIR is patient-level clinical exchange; this is
  aggregate reporting. Naming it would read as a buzzword.
- **PathGen HealthMap/BeaconBio outbreak feeds**, rejected for this window. The archive is
  entirely 2025 with one Rwanda row, against 2024 assignment data. More fundamentally the
  data has no pathogen dimension: `death_sepsis` is the only infectious channel and it is
  flat (sd 0.309 across ten months). Retained as rationale for why Problem B was tempting.

## Reverses if

- The pipeline grows past a single-machine quarterly batch into something long-running or
  multi-stage that genuinely fails partway, then durable execution earns its place and
  DBOS returns to the table.
- Hamilton proves not to install cleanly under Pyodide, which would break the one-module
  two-runtime claim and reduce it to a batch-only choice.
- A facility-level geography source appears that can be joined to the sample, which would
  reopen facility-point mapping and change the geo grain.
- A third deployable app appears, which would justify the monorepo tooling.

## Honest limits

The correlation figures come from a synthetic sample whose outcome was generated as a
function of capability variables. They establish what is *in this dataset*, not what drives
neonatal mortality in Rwanda. The rejection of raster covariates is therefore a decision
about this deliverable, not an epidemiological claim.

Hamilton-under-Pyodide is asserted from tryhamilton.dev and GeoLibre's shipped
`jupyterlite-pyodide-kernel`; it has not been verified in this repo. First task in the
prototype is to prove it or fall back to batch-only.

## Artifacts

- `openspec/config.yaml`, the always-loaded operating summary of this decision
- `openspec/BACKLOG.md`, capability specs and their dependency order
