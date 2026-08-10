## Context

See `proposal.md` — Why.

Constraints, in the order they bind:

- **The surface executes nothing.** HTML embedded in email: no script, no external assets,
  and Gmail clips past roughly 102KB. That single fact eliminates every runtime charting
  library and forces charts to be markup.
- **The reader is not a data analyst.** The Director wants one question answered and the
  ability to defend the answer. A District Health Officer wants their district. An analyst
  wants the lineage. Three readers, one document, in that priority.
- **Tokens already exist.** `moh-rwanda-architecture.v2.html` carries the engagement's system:
  ink `#1A1917`, cream `#FAF9F5`, oat `#EFEBE0`, sage `#A8B89A`, olive `#6F855A`, clay
  `#C36A47`, plus nine category and six persona accents, over serif/sans/mono.
- **The `impeccable` skill's absolute bans apply**, and the current renderer violates two of
  them.

## Goals / Non-Goals

**Goals:**

- A first screen that answers the Director's question without scrolling.
- Charts where shape reads faster than digits, as static SVG.
- State perceivable while scanning, and surviving loss of colour.
- A recorded token set so the next artifact inherits rather than reinvents.

**Non-Goals:**

- Interactivity. That is `explore-surface`; this artifact is deliberately inert.
- A component library. One document, not a design system product.
- Print or PDF stylesheets. Submission packaging is a separate concern.
- Changing any number. This is presentation only; the guards decide what is shown.

## Decisions

**Inherit the MoH artifact's tokens rather than choosing a palette.**
Two documents for one client that look unrelated undercut both. *Alternative considered:*
designing a bulletin-specific palette. Rejected — the engagement already has a system, and
the reflex answer for this domain (white and teal "healthcare") is the first-order category
cliché the design laws call out by name.

**Vega-Lite specs generated in Python, rendered by `vl-convert` to inline SVG.**
`vl-convert` is pure Rust with no browser, so it fits the existing pipeline and produces
markup that satisfies the no-script constraint. *Alternative considered:* `microsoft/flint-chart`.
Genuinely attractive for its themes, semantic types, and agent-authorable specs, but it is
npm-only with no PyPI package, so adopting it means Node plus a TypeScript build step inside
a Python pipeline four days from submission. Its themes are the main draw and the engagement's
own tokens serve that better. Recorded as the Deliverable 3 productionization path.
*Alternative considered:* hand-written SVG. Rejected — axis scaling and label placement by
hand is where the time would go, and it is the least interesting part.

**A chart registry keyed by figure kind, not by panel.**
`ranking` gets a horizontal bar; `distribution across units` gets a sorted bar with a
reference line; `composition` gets a stacked bar; `per-unit rate against a benchmark` gets a
dot plot with a benchmark rule. *Alternative considered:* choosing per panel. Rejected — that
is how a document ends up with five chart types that encode the same thing differently, and
it makes the choice unreviewable.

**State gets a non-colour channel.**
Provisional is a hatched fill and a dotted rule; withheld is a full-width block occupying the
position the panel would have had; unmeasured is an explicit glyph, never an empty cell.
*Alternative considered:* colour-coded tags, which is the current implementation. Rejected —
it fails a reader scanning rather than reading, and fails entirely without colour.

**The withheld panel keeps the real panel's position and prominence.**
Demoting it to a footnote would make refusal look like absence. The refusal is a finding.

**Fix the two ban violations structurally, not by recolouring.**
Callouts lose `border-left` and gain a tinted background with a rule above; em dashes are
removed from generated copy and a check over the output enforces it. *Alternative considered:*
keeping the stripes since they read acceptably. Rejected — a mechanically checkable rule that
is knowingly violated is worse than no rule.

**DESIGN.md is derived from tokens in use, not authored fresh.**
The `impeccable` gate requires it, and deriving it from what already ships keeps it honest.

## Risks / Trade-offs

- **Charts push the document past the email size ceiling** → SVG is text and compresses well,
  but this needs measuring, not assuming. Budget one chart per section, and measure before
  committing to more. If the ceiling binds, the email carries the summary and the charts live
  in the linked artifact.
- **Hatched fills render inconsistently across email clients** → the hatch is an SVG pattern
  inside the chart, and the table-level channel is a border-style change rather than a fill.
- **`vl-convert` adds a binary wheel dependency** → pure Rust, no browser, no system libs;
  passes the dependency test. Falls back to omitting charts rather than failing the render.
- **Designing for three readers in one document risks serving none** → the reading order is
  declared and testable: the primary question is answered in the first screen, and the other
  two sections are reachable without reading it.
- **Skipping Flint may read as not knowing about it** → recorded explicitly in the proposal
  and in Deliverable 3 with the reason, which is stronger than adopting it badly.

## Migration Plan

`render.py` keeps its structure; the stylesheet and the section order change, and a chart
module is added. No pipeline or mart changes: this consumes existing gold marts.

## Open Questions

- Whether the Director's first-screen question is "is mortality getting worse" or "can I
  trust this document". The temporal guard withholds the first, which arguably makes the
  second the honest primary. Resolve before fixing the reading order.
- Whether a district choropleth earns its place given district is the finest usable grain.
  A sorted dot plot may read better than a map at 30 units. Decide by producing both.
