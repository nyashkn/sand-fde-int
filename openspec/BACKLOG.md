# Capability backlog

Seven capabilities, in dependency order. Spec them **lazily**, one at a time, immediately
before building. This file exists so nothing discussed gets lost, not to be scoped upfront.

Governed by `decisions/0008-technical-stack.md` and `openspec/config.yaml`.

## Waves

```
WAVE 0  serial, defines the vocabulary everything else uses
  conceptual-model   object map, ubiquitous language, deeplink URL contract
  trust-lineage      provenance columns, figure→rows traceability, rule naming

WAVE 1  parallel, both depend on wave 0
  ingest-mart        bronze/silver/gold, DHIS2 grain, crosswalk registry
  data-validation    DUP-01 dedup + the three defect checks, as Hamilton @check_output

WAVE 2  parallel, all depend on wave 1
  bulletin-render    Flint specs → static HTML, email constraints, deeplinks
  explore-surface    Mosaic + DuckDB-WASM, layer toggles, URL state hydration
  geo-context        GAUL districts, HDX healthsites, choropleth

WAVE 3
  handover-runbook   the named-DHO restart act, ADR 0006's actual deliverable
```

Wave 2's three are genuinely independent (different files, different surfaces), real
3-way parallel. Wave 1's two overlap on the silver schema, so either one worktree or the
schema is frozen in `trust-lineage` first.

## What each must not lose

**conceptual-model**, objects get canonical URLs, explore state gets parameterised ones;
conflating them is the trap. Nouns to reconcile: DHIS2 `orgUnit` / HealthTrack `facility` /
brief `site`. Run `/layers-conceptual-model` and `/layers-domain` from `jamiemill/layers-skills`.

**trust-lineage**, a deeplink is a lineage receipt, not navigation. Click a figure, see:
rows behind it, dedup rule applied and how many rows it removed, source file, ingest time,
absent periods, indicator definition. Provenance is **columns in silver**, not logs. Rules
are named and versioned (`DUP-01`), never anonymous `.drop_duplicates()`. Publish the
defects found rather than silently correcting them.

**ingest-mart**, silver at `(org_unit, period, data_element, value)`. Bronze keeps source
field names verbatim. Crosswalk is a table, not code. Prove it with a **second source**: ~50
rows of hand-written DHIS2-shaped JSON landing in identical silver rows, otherwise the
reusability claim is untested.

**data-validation**, four checks, all one-liners, all generic beyond Rwanda:
geo-containment (`groupby('province').gps_lat.std()`), duplicate `(facility, period)`,
id-prefix ambiguity (NYA→7 districts), name vs `tier_level` contradiction (62/117).
Ship as `@check_output` on the Hamilton nodes they guard.

**bulletin-render**, email is the hard constraint: no JS, inline CSS, table layout, charts
as images, ~102KB before Gmail clips. One Flint spec → static for email, interactive for
page. Choropleth is a pre-rendered PNG hyperlinked to the live map.

**explore-surface**, Mosaic coordinator hydrates from URL params. Raster layers live here
and **never in the bulletin**, the published artifact must not invite causal inference the
data does not support. Basemap/terrain/healthsites are always-on context, not toggles.

**geo-context**, district grain only, GPS is unusable. Check the GAUL name-collision set
first (Nyaruguru/Nyarugenge, Ngoma/Ngororero), those are exactly the pairs that silently
cross-join. HDX Rwanda Healthsites gives 1,345 real facility points as basemap.

**handover-runbook**, not documentation, it is the artifact that makes ADR 0006 true.
Should be written by whoever did least of the build, since it must be followable by someone
who was not there.

## Open questions

| # | Question | Blocks | Status |
|---|---|---|---|
| 1 | Hamilton installs cleanly under Pyodide? | one-module-two-runtimes claim | first prototype task |
| 2 | Second source (DHIS2-shaped JSON) in scope? | crosswalk credibility | recommended, ~30 min |
| 3 | Submission PDF generated from artifacts or written separately? | deliverable packaging | deferred |
| 4 | Named DHO with cleared hours confirmed? | ADR 0006 downgrades to `A-minimal` | Week 1 Day 2 field action |

## Settled, do not relitigate

| Question | Answer | Where |
|---|---|---|
| GEE auth needed? | No. HDX has subnational CSV; MapLibre has basemaps | 0008 |
| PDF output? | No. HTML only, embedded in email | 0008 |
| DBOS? | No. Fails the dependency test | 0008 |
| Raster covariates as explanation? | No. r=+0.125 vs capability r=-0.844 | 0008 |
| Monorepo tooling? | Not yet. Conventions only | 0008 |
| Fork GeoLibre? | No. Lift four patterns | 0008 |
