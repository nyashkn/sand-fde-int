## Why

The bulletin renders correctly and reads poorly. Eight sections of tables and prose with no
charts, no visual hierarchy beyond heading size, and no way for a Director to find the one
number that matters without reading the whole page. It is a correct document that nobody
wants to open.

That is not cosmetic. The engagement's premise is that the Director's problem is trust, and
a quarterly document he does not read cannot earn any. Deliverable 2 is also the artifact a
reviewer opens first, so its legibility is doing more work than its correctness.

Two concrete failures beyond blandness. The current renderer uses coloured `border-left`
accents on every callout, which is a named anti-pattern, and em dashes throughout, which the
house style bans. Both are mechanical to check and were shipped anyway.

There is also brand continuity available and unused. `moh-rwanda-research/out/moh-rwanda-architecture.v2.html`
already establishes a design system for this engagement: ink, cream, oat, sage, olive, clay,
plus nine category accents and six persona accents. The bulletin invented its own palette
instead of inheriting that one, so two artifacts for the same client look unrelated.

## What Changes

- Adopt the **engagement design tokens** from the MoH architecture artifact as the bulletin's
  source of truth, rather than a palette invented per document.
- Introduce **charts**, rendered as static SVG embedded in the document. No JavaScript, no
  external assets, no runtime chart library, the email surface can execute nothing.
- Establish a **chart template registry**: a figure's shape determines its chart type, so the
  choice is made once per figure kind rather than improvised per panel.
- Give the document a **reading order for a specific reader**: what the Director sees in the
  first screen, what a District Health Officer scans for, what an analyst drills into.
- Make **state visible at a glance**, provisional, withheld, unmeasured, rather than as
  inline text tags a reader must stop and parse.
- **BREAKING** for the current stylesheet: `border-left` accents are removed wherever they
  carry meaning, replaced with structure that does not rely on a banned pattern.
- Remove em dashes from all rendered copy.
- Produce **DESIGN.md**, derived from the tokens already in use, so subsequent work inherits
  the system instead of re-deriving it.

## Capabilities

### New Capabilities

- `bulletin-design`: the visual system, the chart template registry, the reading order, and
  the state-visibility rules the rendered bulletin is held to.

### Modified Capabilities

None. `trust-lineage` requires that state and lineage reach the reader; it does not say what
that looks like. `bulletin-render` is proposed but not yet written, and will consume this.

## Impact

- **Depends on** `trust-lineage` for which states must be expressible, and on
  `conceptual-model` for the objects a figure addresses.
- **Constrains** `bulletin-render`: the chart registry fixes which chart type a figure kind
  gets, and the state rules fix how provisional and withheld are shown.
- **Constrains** `explore-surface`: the interactive surface inherits the same tokens, so the
  hand-off from static artifact to explore view is visually continuous.
- **Adds one dependency**: `vl-convert-python`, which renders Vega-Lite to SVG without a
  browser. Passes the ADR 0006 dependency test, it is a pip install and a pure function.
- **Explicitly does not adopt** `microsoft/flint-chart` as a runtime dependency. It is npm
  only with no PyPI package, so using it would add Node and a TypeScript build step to a
  Python pipeline. Its themes and semantic types are the draw, and both are better served
  here by the engagement's own tokens. Recorded in Deliverable 3 as the productionization
  path, where agent-authored chart specs and multi-backend rendering earn their cost.
- **Inputs**: `moh-rwanda-research/out/moh-rwanda-architecture.v2.html` (tokens),
  `artifacts/04-data-quality-audit.html` (what must be disclosed),
  the `impeccable` design skill's shared laws and absolute bans.
