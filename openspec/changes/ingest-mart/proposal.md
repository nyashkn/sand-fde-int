## Why

Three capabilities now constrain a mart that does not exist. `conceptual-model` fixed the
vocabulary and the object identities that rows must resolve to. `data-validation` requires
that rejected rows stay retrievable and that findings attach to the rows they examined.
`trust-lineage` requires that provenance be *columns*, not logs, because a log is not
addressable from a figure.

Applying any of them means inventing the mart inside a validation task or a lineage task —
which is how a schema ends up decided by whichever piece of work reached it first, and then
quietly contradicted by the next one.

There is also a claim to make good on. The crosswalk is named throughout this engagement as
the reusable asset — new source becomes new rows, not a new pipeline. With one source in
bronze that claim is untested, and a crosswalk with a single source is a rename with extra
ceremony.

The MoH's real estate makes the grain choice for us: DHIS2 for monthly reporting, 45
hospitals on HealthTrack, 30 clinics on OpenMRS, 175 facilities on paper, plus separate TB,
HIV, and immunisation systems. A mart shaped around the sample CSVs would need rebuilding at
the first real source. A mart shaped around DHIS2's own grain accepts all of them.

## What Changes

- Establish **three layers**: bronze as received and immutable, silver at DHIS2 grain with
  provenance, gold as the marts a bulletin reads.
- Fix silver's grain at `(org_unit, period, data_element, batch)` — **batch is in the key**,
  because without it the two January loads collide and one silently overwrites the other,
  which is the defect rather than a fix for it.
- Establish the **crosswalk as a table**, not an in-code rename: source system, source field,
  canonical element, code system, code. Bronze must remain auditable against the file the
  Ministry actually sent.
- Carry provenance as **columns on silver**: source system, source key, batch, ingest time,
  rules applied, quality flags, provisional state.
- Retain **rejected rows in bronze** in original form, with their rejection reason.
- Emit gold as **Parquet**, readable by both the Python batch and the browser over HTTP range
  requests, so no API sits between the pipeline and the surface.
- Prove the crosswalk with a **second source**: a small DHIS2-shaped export landing in
  identical silver rows.
- Record **unmapped fields explicitly** rather than dropping them. The audit found 9 of 66
  unusable; unmapped means not presented and not aggregated, never deleted.

## Capabilities

### New Capabilities

- `ingest-mart`: the three-layer structure, silver's grain and provenance columns, the
  crosswalk registry, bronze retention rules, and the gold artifact contract.

### Modified Capabilities

None. `conceptual-model` defines objects, not storage; `data-validation` and `trust-lineage`
state requirements *on* a mart without specifying one.

## Impact

- **Depends on** `conceptual-model` for identity, grain, and the canonical vocabulary that
  the crosswalk maps to.
- **Unblocks** `data-validation` — checks need Hamilton nodes over real tables to attach to.
- **Unblocks** `trust-lineage` — the lineage projection needs columns to project over.
- **Constrains** `bulletin-render` and `explore-surface`: both read gold Parquet directly.
  No service, no query API.
- **Supplies** the reusability argument for Deliverable 4. The crosswalk and the silver grain
  are what transfer to the next source and the next country; the Rwanda-specific parts do not.
- **Inputs**: `openspec/specs/conceptual-model/model.md` (object map, 66-field mapping),
  `artifacts/04-data-quality-audit.html` (what bronze must tolerate),
  `decisions/0008-technical-stack.md`, `decisions/0009-bind-vocabulary-to-dhis2.md`.
