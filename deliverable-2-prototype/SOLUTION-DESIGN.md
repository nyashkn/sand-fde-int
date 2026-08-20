# Deliverable 2, Solution Design and Implementation Notes

Written counterpart to `../artifacts/06-bulletin-architecture-data-flow.html` (mart ERD as
inline SVG). This document carries the required prose (products, what is custom, build vs.
buy) and stands alone when printed. Section 2 (prototype code) is done: see `README.md`.
Covers Section 1 in full, Section 3 where the README does not already.

## Section 1: Solution Design and Architecture

### 1.1 Architecture and data flow

Four layers, plus checks, plus render. Python stops at Parquet (ADR 0010); everything past
that is Astro.

**Sources.** The assignment's five CSVs (`facilities`, `clinical_neonatal`, `governance`,
`healthcare_workers`, `operations`), plus `dhis2_sample.csv`, a DHIS2-shaped source,
hand-built to prove the crosswalk pattern, not a live API pull (see 3.1).

**Bronze** (`dataflow/bronze.py`). Loads all six sources verbatim, `dtype=str`, stamped with
`_source_system`, `_source_file`, `_source_row`, `_batch`, `_row_hash`, `_ingested_at`.
Where facility and period arrive twice (2024-01 and 2024-03, 234 rows), both loads are
kept: silently colliding and picking a winner is the defect this stamps against.

**Crosswalk and identity** (`mart/crosswalk.csv`, `mart/org_unit_map.csv`). Two declared
CSV tables, not code. The crosswalk maps 71 source fields (66 assignment, 5 DHIS2) to a
canonical element, role (`identity`, `dimension`, `observation`, `unmapped`), and note;
`org_unit_map` declares which facility identifiers across source systems mean the same
facility. Both read as data at runtime, not hardcoded (see 1.4).

**Silver** (`dataflow/silver.py`). Melts every wide source into long form, unions it with
the DHIS2 source, inner-joins to the crosswalk (dropping every `unmapped` field, see 3.1 on
GPS), resolves identity through `org_unit_map` (raising on an unresolved key, not inventing
a facility), and emits one canonical `observation` at DHIS2 grain: `(org_unit, period,
data_element, batch)`.

**Gold** (`dataflow/gold.py`). The marts a bulletin actually reads: `observations_resolved`
(batch collision resolved, arbitrarily, see 3.1), `facility_quarter` / `district_quarter`,
`nmr_facility_quarter` / `nmr_district_quarter` (neonatal mortality rate per 1,000 live
births, WHO GHO definition), `completeness_summary`, `facility_capability` /
`capability_summary`, plus two declared-not-derived tables read verbatim:
`known_contradictions.csv` (8 findings, each a contradiction between two populated fields,
not missing data; see 3.2 for an example) and `cause_capability_links.csv` (4
cause-of-death to capability pairings).

**Checks** (`dataflow/checks.py`). Two statistical tests, seeded (`PERMUTATION_SEED =
20260810`, 200 trials), that annotate a claim rather than gate a row: `temporal_signal_check`
(momentum vs. a shuffled baseline) and `stratification_check` (pooled correlation split by
facility tier). Both always emit a caveat; ADR 0012 made a failed check annotate rather
than hide the section it qualifies.

**Publish, then render.** All of the above lands in `mart.duckdb` and individual `.parquet`
files. Astro reads Parquet at build time and renders three surfaces from one component set:
the static Bulletin (zero JavaScript, one file per quarter, works forwarded and offline),
the Email edition (a separate, smaller document; see 1.3), and an Explore surface (Mosaic
over DuckDB-WASM), scoped but not built (see 3.2). Apache Superset also reads the same
Gold-layer Parquet, server-rendered, scoped to the connected central MoH office only (1.2,
1.3).

Plain-text version of the same flow, for a reader of this file directly:

```
5 assignment CSVs ┐
                   ├─> bronze() ─┐
dhis2_sample.csv  ┘              │
                                  ├─> silver()  <── crosswalk.csv, org_unit_map.csv (declared)
                                  │        │
                                  │        v
                                  │   observations_resolved (batch collision resolved)
                                  │        │
                                  │        ├─> facility_quarter / district_quarter / nmr_*
                                  │        ├─> facility_capability / capability_summary / completeness_summary
                                  │        └─> checks.py: temporal_signal_check, stratification_check
                                  │                 (always annotate, never gate)
                                  v
                     known_contradictions.csv, cause_capability_links.csv (declared, read verbatim)
                                  │
                                  v
                        mart.duckdb + *.parquet
                                  │
                    ┌─────────────┼──────────────────┬─────────────────────┐
                    v             v                  v                     v
              Bulletin       Email edition     Explore surface      Apache Superset
           (static, per     (separate doc,      (scoped, not         (connected MoH
            quarter)         under 102KB)          built)             office only)
```

The rendered version of this diagram, plus the mart ERD — deliberately not a star or
snowflake schema — are reproduced from `artifacts/06-bulletin-architecture-data-flow.html`
in the PDF submission; open that file directly for the interactive version, including the
product-decision cards (§1.2 below covers the same ground in prose).

### 1.2 Which Sand products, and why

**Firm honesty constraint, applied throughout.** Sand's stack components (Superset, DHIS2
integration, dbt/Airflow) appear in Sand's own FDE job postings.
`research/sand-product-research.md` grades that evidence *strong*, not *confirmed*: good
evidence the component types exist and are staffed for, not evidence a working,
Rwanda-configured instance exists today. D1 made exactly this error once (job-posting copy
read as existence proof), caught in cross-provider red-team review
(`decisions/0007-cross-provider-redteam-amendments.md`), downgraded to a Week 1 question
(gate G4). Below, "in Sand's stack" and "confirmed live for this engagement" stay two
separate claims; the second is never asserted without a source that supports it.

| Product | Use in this design | Why | Evidence grade |
|---|---|---|---|
| **Analytics Template Toolkit** (Apache Superset) | Yes, scoped to the connected central MoH office audience only | Superset is server-rendered, needing a live connection: fails in low-power districts (4-6 hrs/day power, spotty 3G/4G) but works in the central office. The Gold-layer marts are already Superset-ready: documented Parquet/DuckDB tables with a field dictionary in `crosswalk.csv`. Two audiences, two tools, one data model (ADR 0008). | Moderate: named directly in a Sand FDE job posting (Nigeria), corroborated by a second employee's LinkedIn profile (URL not captured). A live, Rwanda-configured instance is unconfirmed; per D1's gate G4, a Week 1 question, not an assumption here. |
| **HealthOS Data Models** | No | This binds directly to DHIS2's own public data model (`org_unit`, `period`, `data_element`, ADR 0009): the naming conflict resolved (Bluelake's UI vs. the CSVs' fields vs. DHIS2's UIDs vs. the brief's prose) is specific to this engagement's sources. A generic product cannot pre-resolve a conflict defined by which systems a Ministry runs and what its analysts call things. | Weakest of the five. The research doc's entire "likely architecture" section for this product is marked `[INFERENCE]`, drawn from generic DHIS2/openHIE/medallion patterns, not from anything Sand-specific. |
| **Health Outcome Tracker** | No | The bulletin's facility to district to national indicator roll-up is built directly in the Gold layer (`district_quarter`, `nmr_district_quarter`). No working, Rwanda-configured instance is established to plug a new bulletin into. If one exists, in a real engagement the roll-up logic would migrate to configuration on that product rather than stay bespoke Hamilton nodes (see 1.3, cost to reverse). | Moderate: the pillar name and scope trace to an AWS Marketplace listing (the research's strongest technical source); architecture inferred from one employee's LinkedIn profile; quantitative outcome claims (ANC4 increase, etc.) are vendor marketing, not audited. |
| **Health Insight Engine** | No | Documented shape: AI-driven anomaly detection and alerting. The closest analog, Rwanda's National Health Intelligence Center, is live (2026 outbreak surveillance), but the brief's four metrics (top facilities, maternal indicators, performance scores, trend) are descriptive analytics, not alerting: no fit even where a confirmed instance exists. The two checks built instead are simple, seeded, auditable, the opposite of an opaque model: a DHO needs a traceable method, not a score to trust unread. | Best-evidenced architecture of the five (Rwanda MoH published its own six-layer HIC diagram), but the AI/alerting mechanics themselves remain unverified inference even against that source. |
| **Health Atlas** | No | GPS coordinates are fabricated (uniform random inside Rwanda's bounding box, every province spans the full extent), structurally excluded at the crosswalk's `unmapped` role, not just hidden downstream: no facility-point layer to hand to a mapping product. If real coordinates arrive later (Deliverable 3 proposes HDX's Rwanda Healthsites layer, 1,345 facilities), this reopens, including whether Health Atlas is the right home. | Weakest single sourced fact of the five: the 3D-mapping capability traces to one LinkedIn post by a named engineer describing Rwanda work; ingestion and use details are inference from cross-vertical Sand language. |

Net: one product used (Superset), four not, each for a stated evidence-or-fit reason. None
of the four "not used" calls says the underlying capability is fictional, only that this
design does not get to assume it is available.

### 1.3 Build vs. buy, per component

| Component | Decision | Why | Cost to reverse |
|---|---|---|---|
| Ingestion (DHIS2 and legacy CSV sources) | Build: `crosswalk.csv` + Hamilton loaders in `bronze.py` | No evidence a Rwanda-configured DHIS2 connector exists in Sand's stack (D1 gate G4); a reviewable CSV fits the "restart alone, 2am, no internet" test better than a connector's internal mapping (ADR 0006, 0008). | Low to moderate: `crosswalk.csv` grows by adding rows; a real connector would replace `bronze_dhis2` only, since silver and gold already read a crosswalk-mapped table. |
| Transformation and mart (bronze to silver to gold) | Build: Apache Hamilton + DuckDB + Parquet | Passes the dependency test the stack is chosen against. DAG derives from function parameter names, so lineage comes from code. Server-side today; a Pyodide/browser path is asserted from `tryhamilton.dev`, unverified here (ADR 0008). | Moderate: Hamilton nodes are backend-agnostic pandas/pyarrow functions; swapping DuckDB for a warehouse re-points `run.py`, not the DAG. |
| Orchestration and scheduling | Neither built nor bought yet: `run.py` is invoked by hand today | A quarterly batch completing in seconds doesn't clear the bar for a durable-execution runtime; DBOS was rejected on the same test (ADR 0008). Nothing runs on schedule, no failure alerts (Deliverable 3, item 4). | Low: Hamilton exposes the DAG as a callable graph; wrapping it in cron or the Ministry's own scheduler is additive. |
| Chart rendering | Buy: Flint (`microsoft/flint-chart`, npm), over hand-rolled Vega-Lite or D3 | One spec compiles to a static render (email, build-time SVG) and an interactive backend (unbuilt explore surface). Constrained grammar and MCP server make agent-authored charts validatable; raw Vega-Lite or D3 would not be (ADR 0008). Deferred in ADR 0010 over npm-only packaging while Python-rendered, re-adopted in ADR 0012 once Astro/TypeScript. | Moderate: a real Vega-Lite compiler bug was worked around (custom sort dropped under multi-layer auto-labels), unfiled upstream. Two details (a hatch fill, a benchmark rule line) use a hand-edit escape hatch since Flint's semantic layer doesn't expose them. |
| Document rendering (bulletin and email) | Build: Astro, zero JavaScript by default, over a Superset export or the earlier hand-rolled Python renderer (`render.py`, deleted) | Email clients strip script, so a Superset export or SPA cannot produce the email surface at all. The earlier hand-rolled Python renderer duplicated logic against the interactive surface, capping UX (ADR 0010). | Low to moderate: Astro components are the one thing every surface shares; replacing the renderer rebuilds all three, but the Parquet contract doesn't change. |
| Explore and dashboard surface, connected office | Buy: Apache Superset | Server-rendered dashboards over a live connection suit reliable power and connectivity; not attempted for the offline majority, where it would fail. | Low if a live instance exists in Sand's stack (unconfirmed, see 1.2); moderate to high if stood up from scratch: hosting, credentials, InfoSec approval all open (D1 §2.2). |
| Distribution (email) | Build: a deliberately separate, smaller HTML document, not the bulletin inlined | Measured, not assumed: inlining the full bulletin hit 99.0 KB against Gmail's ~102 KB clip threshold, with trust-critical disclosure sections (withheld panels, known defects, lineage) at the bottom, first clipped. Inline SVG is also unsupported across major clients (ADR 0011). | Low: already a distinct document; reversing to inline-everything is a template change that reopens the clipping problem ADR 0011 measured. |
| Hosting | Deferred: no hosting decision made, none needed for a local prototype | D1 originally assumed Sand-hosting, flipped to explicit in-scope after red-team review (§2.2). Where this runs, who owns credentials after week 6, and whether health data may sit in a Sand-hosted environment are open, not settled by a laptop prototype. | Unknown, deliberately unestimated: deciding without InfoSec or Ministry input is the same Rwanda-specific-instance assumption D1's red-team already caught once. |
| Statistical checks (temporal signal, stratification survival) | Build: permutation test and stratified correlation, in-repo, seeded | Tests this bulletin's claims against this dataset's structure (117 facilities, 4 tiers, quarterly). None of the five Sand products does statistics this in-context; Health Insight Engine's alerting is closest, unverified, and different (anomaly detection, not per-claim validity). | Low mechanically: ~150 lines of pandas/numpy, seeded, no dependency. The real cost is institutional: a Ministry reading a caveat as correct, not a bug. |
| Facility identity resolution | Build: declared `org_unit_map.csv`, not auto-matching on a shared key string | Two systems using `NYA001` for the same facility is evidence of a shared code space, not proof of identity. Auto-matching on string equality is how an identity graph silently fuses two real facilities. | Low: additive rows; the real cost is process, since someone must make and record each match. |

### 1.4 What is custom, and why

Three things are genuinely custom (written for this engagement, not configuration on a
bought tool), each for a specific reason, not by default.

**The crosswalk and indicator dictionary** (`mart/crosswalk.csv`). This resolves a real
naming conflict: Bluelake's UI says "Health Post" in chart titles and "Facility" in its
filter bar; the sample CSVs say `facility_id`; DHIS2 says `orgUnit`; the brief says
"facility" and "site" interchangeably (ADR 0009). That conflict is specific to which
systems this Ministry runs and what its analysts call things. A bought mapping tool
resolves a generic version; it cannot resolve this one without the same 71-row harvest
already done, because the harvest is the work.

**Per-figure lineage.** Carried as columns through the pipeline (`rules_applied`,
`quality_flags`, `provisional`, `source_system`, `source_row`, `row_hash`,
`ingested_at`), not a bolted-on audit log. `observations_resolved` publishes to Parquet
because it is the only table carrying `rules_applied`, so the bulletin's lineage section
reads the actual rule name, not a restatement. A generic BI tool's lineage feature
describes a generic ETL's; it cannot name this pipeline's own arbitrary tie-break
(`DEFAULT-BATCH-01`, see 3.1) without this pipeline's code producing that fact first.

**The two statistical checks.** As in 1.3: they answer whether a specific correlation
survives being split by a specific stratification variable, narrower than the question a
bought anomaly-detection layer is built to ask ("is this point unusual").

One non-custom call on the opposite principle: `known_contradictions.csv` and
`cause_capability_links.csv` stay declared CSV data, not code. Pairing a cause of death
with the capability that treats it, or flagging a kangaroo-care contradiction, is a
clinical judgement call, not a statistical inference; encoding it in Python would make it
harder to review, the same failure mode the crosswalk avoids.

## Section 3: Implementation Notes

### 3.1 Shortcuts taken

`README.md` already lists four (lineage as file anchors rather than addressable URLs, the
`DEFAULT-BATCH-01` arbitrary tie-break, gold regenerating fully on every run, and the
stratification check testing tier only). This adds the ones that document does not cover.

- **Second source is synthetic, not a live DHIS2 pull** (see 1.1). `bronze_dhis2` loads a
  hand-built, 12-row, 3-facility CSV shaped like a DHIS2 export, to prove the crosswalk's
  claim that a new source onboards via mapping rows, not pipeline code; not evidence of a
  real API pull.
- **No scheduler.** The full build (`uv run python run.py && bun run publish`) runs by
  hand. Nothing runs on a quarterly cadence and no one is told when a run fails. Hamilton
  already exposes the DAG as a callable, so this is a wrapper away, not built yet
  (Deliverable 3, item 4).
- **No auth.** No server process, nothing to authenticate against: no API key, no cloud
  account, no login. A consequence of the offline-first design, not deferred; the day this
  runs against a live source or a hosted surface, auth becomes a real open question
  untouched here.
- **GPS excluded because it is fabricated, not out of scope to try** (see 1.2). Coordinates
  are structurally dropped at the crosswalk's `unmapped` role before silver, not just
  hidden in the render. The bulletin maps at district grain, the coarsest the real data
  supports.
- **Single-machine DuckDB.** `mart.duckdb` is a local file, no server, no connection
  string. Correct for a quarterly batch running in seconds; ADR 0008 names its own
  reversal condition (growing long-running or multi-stage enough to genuinely fail
  partway), which has not happened.

### 3.2 What I would show in Week 3, what works, and what is genuinely broken

D1 §2.6 specifies the Week 3 demo as a reconciliation, not a dashboard tour: last quarter's
published bulletin, the pipeline re-deriving it from source, the figures that match, and
the one that does not, with why. This build cannot do that literally: the data is
synthetic and no prior bulletin exists to reconcile against, a gap between plan and what is
buildable here, named rather than glossed over.

**What works today.** All four 2024 quarterly editions build and pass the five checks
(`check-shipped`, `check-tokens`, `check-style`, `check-email`, `check-agreement`), plus the
publish-time guard that refuses to write a file whose name and contents disagree on the
quarter (shipped once with a mismatched filename, hence the guard). Of the four required
bulletin metrics, two are answered directly and two are substituted with the substitution
declared: top-10 facilities by volume, and a genuine four-quarter trend rather than a
two-point delta, are direct. Maternal health indicators are not: the provided CSVs carry no
ANC column and no complication column, so what ships is neonatal cause of death and the
stillbirth ratio, which are perinatal rather than maternal. Facility performance ships
completeness but not timeliness, because no source file carries a submission timestamp, so
no lag is derivable. Both gaps are in the extract, not the design, and both close with three
more crosswalk rows against standard DHIS2 elements in Week 2. The full accounting is in
`README.md`. The checks disclose rather
than hide: a correlation that fails stratification, or a trend with no measured temporal
signal, ships with a caveat sentence instead of an empty "withheld" section (ADR 0012).
Eight known contradictions surface by name, not corrected silently (`staff_last_training` =
"Never" at facilities that also report trained nurses, a referral imbalance, oxygen plants
without backup power, among others).

**What I would demo instead:** the pipeline re-deriving all four quarters from the same six
source files live, then walking one `known_contradictions` row end to end, from the raw CSV
rows through the crosswalk to the exact sentence in the bulletin, so the audience sees a
real discrepancy traced through every layer, not asserted. Same trust event D1 §2.6 is
after (a genuine mismatch, explained, not a clean run with nothing to show), built from
what this pipeline actually has.

**What is genuinely broken, beyond the reconciliation gap above.**
- The batch conflict has no analyst-actionable resolution: disclosed (every affected figure
  marked provisional) but not fixable in-tool; the triage queue is specified in
  `openspec/changes/data-validation`, not built.
- Ingestion assumes one file shape per source, learned by hand. Real DHIS2 exports,
  HealthTrack dumps, OpenMRS extracts, and paper forms will not hold still, and the mapping
  table is a CSV a human edits, not a confirmed pipeline.
- The explore surface (architecture diagram, ADR 0012's honest-limits note) does not
  exist; chart-runtime is open for whatever gets built there.
- `pipeline/README.md` is empty, the file someone would open first.
- The stratification check tests facility tier only, not a declared variable per
  association, though its design implies it should.

### 3.3 What I learned from building this

The clearest finding is a confound, already shipped in the bulletin, not found after the
fact for this document. `checks.stratification_check` computes, and
`mart/stratification_check.parquet` records: pooled correlation between
`governance_staff_trained_rate` and neonatal mortality across all 117 facilities is
**r = -0.844**. Split by facility tier, it flips sign and collapses toward zero in every
tier: **District +0.111, Health Center +0.042, Provincial +0.144**. The pipeline's own
caveat states it directly: "the association describes tier, not the covariate." A second
covariate, `capability_cpap_machines`, shows the same shape pooled (**r = -0.811**), failing
harder within tier (only Provincial has enough variance to test, **-0.269**). A bulletin
reporting either pooled figure alone would tell a Ministry that training or an equipment
purchase drives survival, when what actually drives both the correlation and the outcome is
which tier of facility a patient reaches: District and Health Center facilities have worse
neonatal outcomes and less of nearly everything, independent of any specific covariate.

Section 6 of the published bulletin also reports a composite equipment index, built in the
web layer, not `checks.py`: pooled **r = -0.867** across all 117 facilities (stated in
prose as -0.87), collapsing within tier to **District -0.071, Health Center +0.036,
Provincial -0.288**. I verified this independently: a z-scored sum of nine equipment fields
against average facility-level mortality gives pooled **r = -0.868** (n = 117), within tier
District **-0.06**, Health Center **+0.04**, Provincial **-0.26** (n = 45, 45, 25; Referral
excluded), deferring to the bulletin's published figures rather than competing with them.

The two constructions agree in sign and land within a hundredth pooled, so the pooled
effect is robust to which fields get chosen. The within-tier numbers are not: they move by
two to four hundredths between constructions at n=45 (District, Health Center) or n=25
(Provincial) per tier, small enough that composing the index differently (which fields, how
weighted) can shift it. That instability is the finding: once the tier effect is removed,
what remains is too small and too dependent on construction choices to support a claim
either way. A bulletin publishing a within-tier number as stable and composition-independent
would be making the same overclaim the pooled figure makes, one level down.

The general lesson, stated to a Ministry directly, not softened: a pooled statistic across
a stratified population is not evidence about the stratum-level relationship; it can be
almost entirely evidence about the stratification itself, and the within-tier residual left
after removing that effect can be too small, at this sample size, to read at all. The
stratification check is mechanical (runs on every covariate it is pointed at, currently
three, always emits a caveat, ADR 0012), so this finding does not depend on remembering to
check the one figure that matters this quarter. The composite-index instability is a
caveat this document adds on top, since `checks.py` tests declared covariates, not
constructed indices, worth naming for Deliverable 3.

Data note, because it matters every time these numbers appear: outcomes in this dataset are
synthetic, generated as a function of the capability variables themselves (ADR 0008's
honest-limits note), and facility-level mortality here (roughly 14 to 73 per 1,000, pooled
per facility across the year) runs three to four times real Rwanda rates. These figures
establish what this synthetic sample contains, not what actually drives neonatal mortality
in Rwanda, and nothing here should be read as a claim about real Rwandan outcomes.
