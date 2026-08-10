## Context

See `proposal.md`, Why.

Fixed upstream, not re-decided here:

- ADR 0008 sets the engine: Hamilton for the DAG, DuckDB for compute, Parquet on disk.
- ADR 0009 binds the vocabulary to DHIS2, extended by ICD-10 and WHO GHO.
- `conceptual-model` fixes identity as a surrogate resolved from `(source_system,
  source_key)`, and puts `batch` inside the observation identity.
- `data-validation` requires rejected rows to stay retrievable and findings to attach to
  examined rows.
- `trust-lineage` requires provenance as columns, and gold readable by a non-executing
  surface.

Shape of the real input: five wide CSVs, 66 distinct fields across 70 column slots, 1,404
facility-months, 9 fields unusable, two whole-batch duplicate loads, two absent months. The
mart has to hold all of that without flinching, because concealing any of it defeats the
point.

## Goals / Non-Goals

**Goals:**

- A silver grain that accepts DHIS2, HealthTrack, OpenMRS, and paper-entry without reshaping.
- Provenance rich enough that lineage is a projection, requiring no new write path.
- Gold artifacts a browser can read directly, offline, with no service.
- A crosswalk demonstrated against two sources rather than asserted against one.

**Non-Goals:**

- Check logic. `data-validation` owns which checks exist and what they mean.
- The lineage record shape. `trust-lineage` owns it; this layer supplies the columns.
- Incremental or streaming ingestion. Quarterly batch over a kilobyte-scale dataset.
- Any write path from the mart back into a source system.

## Decisions

**Wide-to-long at the bronze→silver boundary.**
The CSVs are DHIS2's model pivoted wide; unpivoting recovers `(org_unit, period,
data_element, value)`. *Alternative considered:* keeping silver wide, one column per measure.
Rejected, every new source would add columns, provenance would have to be per-column rather
than per-observation, and the shape would diverge from the system the Ministry runs.

**`batch` is part of the observation identity, not an attribute.**
Without it the two January loads collide on the natural key and one silently wins. *Alternative
considered:* deduplicating at ingest. Rejected, that is the defect. Nothing in the source
establishes which load is correct, so the mart's job is to represent the ambiguity, not to
resolve it.

**Provenance columns, not a provenance table.**
Joining to a provenance table to answer "where did this come from" adds a hop that lineage
would perform for every figure, and makes it possible to have an observation with no
provenance row. Columns make that state unrepresentable. *Alternative considered:* a separate
`lineage` table keyed by observation. Rejected on both counts.

**The crosswalk is a table read at runtime, not a generated module.**
It must be inspectable by a non-engineer at handover. *Alternative considered:* generating a
Python module from the table at build time for speed. Rejected, the dataset is kilobytes,
and the generated artifact would become the thing people actually read.

**Gold is Parquet, not SQLite or CSV.**
Parquet supports HTTP range requests, so DuckDB-WASM pulls only the row groups and columns it
needs; the same file serves the batch job. *Alternative considered:* SQLite, which DuckDB also
reads. Rejected, no columnar range-request story, so a browser client would download the
whole database. *Alternative considered:* CSV for inspectability. Rejected, no types, no
predicate pushdown; a CSV export alongside is cheap if inspectability is wanted.

**Unmapped is a recorded state, not an omission.**
The 9 unusable fields stay in bronze with a stated reason. *Alternative considered:* dropping
them at ingest. Rejected, a later source may supply a trustworthy version of the same field,
and the reason for exclusion is itself a finding worth publishing.

**The second source is hand-written, small, and DHIS2-shaped.**
Enough rows to prove convergence on a shared `org_unit` and `data_element`, using DHIS2's real
field names. *Alternative considered:* a full synthetic DHIS2 export. Rejected, cost without
additional proof; convergence is demonstrated by two rows as well as by two thousand.

## Risks / Trade-offs

- **Long format inflates row count**, 1,404 facility-months × ~16 measures ≈ 22k observation
  rows. Trivial at this scale; the DHIS2 shape is what makes the mart reusable, and that is
  worth paying for.
- **Retaining rejected rows and both duplicate batches grows bronze** → kilobytes here;
  revisit only if a real deployment makes it material.
- **Provenance columns widen every silver row** → the columns are small and highly
  compressible in Parquet; the alternative is an unrepresentable-state bug.
- **A browser reading Parquet over range requests needs correct server support** → the
  fallback is downloading the whole mart, which is small enough to be acceptable; worth
  verifying early rather than discovering on Wednesday.
- **The crosswalk becomes a place to hide business logic** → it holds mapping only; anything
  conditional belongs in a registered check.
- **Regenerating gold from silver on every run may look wasteful** → at this scale it is
  cheaper than reasoning about incremental correctness, and it makes the reproducibility
  requirement trivially true.

## Migration Plan

None, no implementation exists. Order of build: crosswalk table, then bronze loaders, then
the unpivot to silver, then gold marts. `data-validation` attaches to the silver nodes once
they exist; `trust-lineage` projects over silver's provenance columns.

## Open Questions

- Whether bronze stores the source file verbatim as a blob in addition to parsed rows. It
  strengthens the audit claim; it duplicates data. Deferrable, parsed rows with original
  field names satisfy every stated requirement.
- Partitioning strategy for gold Parquet. At kilobyte scale a single file per mart is
  simplest; period partitioning matters only when a browser client would otherwise fetch far
  more than it needs. Deferrable until the explore surface exists and can be measured.
