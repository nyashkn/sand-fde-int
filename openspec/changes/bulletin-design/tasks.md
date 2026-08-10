## 1. Token set and DESIGN.md

- [x] 1.1 Extract the token set from `moh-rwanda-research/out/moh-rwanda-architecture.v2.html`: colours, type families, scale, rule weights
- [x] 1.2 Decide which of the nine category accents and six persona accents the bulletin uses, and what each means here
- [x] 1.3 Write `DESIGN.md` at the repo root, derived from tokens in use, covering colour roles, type scale, spacing rhythm, and state channels
- [x] 1.4 Write `PRODUCT.md` at the repo root: readers, their questions, tone, anti-references, and the `register` field
- [x] 1.5 Replace the bulletin's invented palette with the token set, changing no numbers

## 1b. Move rendering to Astro (ADR 0010)

- [x] 1b.1 Scaffold `web/` with Astro, zero-JS default, static output
- [x] 1b.2 Read gold Parquet at build time with `@duckdb/node-api`
- [x] 1b.3 Port the eight bulletin sections to Astro components
- [x] 1b.4 Verify the static build emits zero script tags and zero external asset references
- [ ] 1b.5 Add the inline-CSS step required for the email surface
- [ ] 1b.6 Delete `pipeline/render.py` once parity is confirmed against the committed output

## 2. Reading order

- [x] 2.1 Resolve the open question in `design.md`: is the Director's first question "is mortality getting worse" or "can I trust this"
- [x] 2.2 Declare, per reader, the question they arrive with and the section that answers it
- [x] 2.3 Reorder sections so the primary reader's question is answered in the first screen
- [ ] 2.4 Verify a secondary reader reaches their section without reading the first
- [ ] 2.5 Verify the first screen at 1280x800 and at a phone viewport

## 3. Chart registry

- [x] 3.1 Define the registry: figure kind to chart type, with the visual channels each uses
- [x] 3.2 Scaffold `web/` as an Astro project; read gold Parquet at build via `@duckdb/node-api`; build the Observable Plot theme from the token set
- [x] 3.3 Implement `ranking` as a horizontal bar, for top facilities by volume
- [x] 3.4 Implement `distribution across units` as a sorted bar with a reference line, for district mortality
- [x] 3.5 Implement `composition` as a stacked bar, for cause-of-death breakdown
- [ ] 3.6 Implement `per-unit rate against a benchmark` as a dot plot with a benchmark rule
- [x] 3.7 Verify a figure kind absent from the registry fails the render rather than improvising
- [x] 3.8 Verify every visual channel used maps to a measure present in that figure
- [x] 3.9 Produce both a choropleth and a sorted dot plot for district mortality, and decide from the output

## 4. State visibility

- [x] 4.1 Implement provisional as a hatched fill in charts and a dotted rule in tables
- [x] 4.2 Implement withheld as a full-width block holding the position the panel would have had
- [x] 4.3 Implement unmeasured as an explicit glyph, never an empty cell
- [ ] 4.4 Verify all three remain distinguishable with colour removed
- [ ] 4.5 Verify a scanning reader perceives provisional figures without reading labels

## 5. Ban conformance

- [x] 5.1 Remove every meaning-carrying `border-left` and replace with a tinted background and a rule above
- [x] 5.2 Remove every em dash from generated copy
- [x] 5.3 Write the automated check over rendered output for both rules
- [x] 5.4 Run the check against both rendered quarters and confirm zero violations

## 6. Verify in a browser

- [x] 6.1 Render both quarters and screenshot the first screen of each
- [ ] 6.2 Measure the rendered byte size against the email clipping threshold, with charts included
- [x] 6.3 Confirm zero script tags and zero external asset references
- [x] 6.4 Confirm every chart renders with no network
- [ ] 6.5 Confirm chart text is legible at published dimensions
- [ ] 6.6 Run `$impeccable critique` against the rendered output and record the findings

## 7. Record and hand off

- [ ] 7.1 Record the Flint decision in Deliverable 3 as the productionization path, with the reason it was not adopted now
- [x] 7.2 Answer or explicitly defer the two open questions in `design.md`
- [ ] 7.3 Confirm `explore-surface` can inherit the same token set
