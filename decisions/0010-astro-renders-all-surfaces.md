# 0010, Astro renders every surface; Python stops at Parquet

- **Date:** 2026-08-10
- **Status:** Accepted
- **Supersedes:** the rendering half of ADR 0008. The batch and mart decisions there stand.

## Context

ADR 0008 fixed two surfaces on one substrate: a static bulletin for email, and an
interactive explore surface in the browser. The mart landed as specified. The rendering did
not.

`pipeline/render.py` builds the bulletin by f-string templating HTML inside Python. That is
wrong in three ways, and the third is the one that matters:

1. **DX.** No components, no hot reload, no type checking across markup. Changing a section
   means editing a Python string literal.
2. **Duplication.** The explore surface needs the same tables, the same figures, the same
   state treatment. Building it separately means two implementations of one design, which
   drift.
3. **A ceiling on UX.** This is the direct cause of the bulletin reading as eight sections of
   inert tables. Templating markup in a data language biases every decision toward whatever
   is easy to concatenate, and the output shows it.

The split we actually want is the obvious one: **Python owns data, the frontend owns the
frontend.** The mistake was letting the pipeline keep going after Parquet.

The constraint that made this look hard is that the email surface can execute nothing. A
single-page app cannot serve it. That constraint is real, and it is what selects the
framework rather than ruling one out.

## Decision

**Python stops at Parquet.**

```
pipeline/   Python    CSVs -> Hamilton -> DuckDB -> Parquet.  Ends here.
web/        Astro     reads Parquet, renders every surface.
```

**Astro renders all three surfaces from one component set.** It is the framework that
resolves the constraint rather than working around it: zero JavaScript by default, so its
static output *is* email-safe HTML; islands, so the explore surface hydrates only where
interaction is needed; and build-time data loading, so Parquet is read once at build rather
than fetched by a client that may have no network.

```
build time   @duckdb/node-api reads gold Parquet
                -> static HTML, zero JS          email + the standalone artifact
islands      @duckdb/duckdb-wasm + Mosaic
                -> interactive, data stays local  explore surface + triage
```

One token set, one component set, three outputs, no duplicated implementation.

**Charts share a grammar across static and interactive.** Observable Plot renders to SVG in
Node at build time; Mosaic's vgplot is built on Observable Plot and drives the interactive
surface. The same chart grammar therefore serves both, which is what makes a single chart
registry possible rather than two that drift.

**`render.py` is deleted, not kept as a fallback.** A second renderer is the duplication this
decision exists to remove.

## Alternatives

- **Keep `render.py` for email, add a separate frontend for explore.** Rejected. Two
  implementations of one design, guaranteed to drift, and it preserves the UX ceiling on the
  surface the Director actually reads.
- **A single-page app for everything.** Rejected on the hard constraint: email clients strip
  script, so a SPA cannot produce the email surface at all.
- **Next.js or SvelteKit static export.** Both can emit static HTML, but both ship a
  JavaScript runtime by default and require opting out. Astro's default is zero JS and its
  exception is the island, which is the shape of this problem rather than a configuration of
  it.
- **`vl-convert` in Python, as proposed in `bulletin-design`.** Rejected by this decision. It
  works, and it keeps rendering in the wrong layer. The chart registry moves to the frontend
  with everything else.
- **`microsoft/flint-chart`.** Its npm-only packaging was the objection when the renderer was
  Python. That objection disappears once the frontend is TypeScript, so it returns to the
  table for the chart layer. Not adopted now on time grounds alone; recorded in Deliverable 3.

## Reverses if

- The email surface is dropped entirely, which would remove the constraint that selects Astro
  over a plain SPA.
- Build-time Parquet reading proves impractical, forcing a fetch-at-runtime model that the
  offline requirement cannot accept.

## Honest limits

This is a correction to my own architecture, made after building the wrong thing. The mart
below Parquet is unaffected and stays: bronze, silver, gold, guards, and the crosswalk all
survive unchanged. What is discarded is one file.

Astro is new to this repo but not to the operator, who has three existing Astro projects on
this machine. The risk is schedule, not capability, and the mitigation is that the already
rendered static bulletins remain committed as output until the Astro build replaces them.

## Artifacts

- `openspec/changes/bulletin-design/`, the visual system this decision renders
- `deliverable-2-prototype/pipeline/`, unchanged below Parquet
