## 1. Token set and DESIGN.md

- [ ] 1.1 Extract the token set from `moh-rwanda-research/out/moh-rwanda-architecture.v2.html`: colours, type families, scale, rule weights
- [ ] 1.2 Decide which of the nine category accents and six persona accents the bulletin uses, and what each means here
- [ ] 1.3 Write `DESIGN.md` at the repo root, derived from tokens in use, covering colour roles, type scale, spacing rhythm, and state channels
- [ ] 1.4 Write `PRODUCT.md` at the repo root: readers, their questions, tone, anti-references, and the `register` field
- [ ] 1.5 Replace the bulletin's invented palette with the token set, changing no numbers

## 2. Reading order

- [ ] 2.1 Resolve the open question in `design.md`: is the Director's first question "is mortality getting worse" or "can I trust this"
- [ ] 2.2 Declare, per reader, the question they arrive with and the section that answers it
- [ ] 2.3 Reorder sections so the primary reader's question is answered in the first screen
- [ ] 2.4 Verify a secondary reader reaches their section without reading the first
- [ ] 2.5 Verify the first screen at 1280x800 and at a phone viewport

## 3. Chart registry

- [ ] 3.1 Define the registry: figure kind to chart type, with the visual channels each uses
- [ ] 3.2 Add `vl-convert-python`; build the Vega-Lite theme from the token set
- [ ] 3.3 Implement `ranking` as a horizontal bar, for top facilities by volume
- [ ] 3.4 Implement `distribution across units` as a sorted bar with a reference line, for district mortality
- [ ] 3.5 Implement `composition` as a stacked bar, for cause-of-death breakdown
- [ ] 3.6 Implement `per-unit rate against a benchmark` as a dot plot with a benchmark rule
- [ ] 3.7 Verify a figure kind absent from the registry fails the render rather than improvising
- [ ] 3.8 Verify every visual channel used maps to a measure present in that figure
- [ ] 3.9 Produce both a choropleth and a sorted dot plot for district mortality, and decide from the output

## 4. State visibility

- [ ] 4.1 Implement provisional as a hatched fill in charts and a dotted rule in tables
- [ ] 4.2 Implement withheld as a full-width block holding the position the panel would have had
- [ ] 4.3 Implement unmeasured as an explicit glyph, never an empty cell
- [ ] 4.4 Verify all three remain distinguishable with colour removed
- [ ] 4.5 Verify a scanning reader perceives provisional figures without reading labels

## 5. Ban conformance

- [ ] 5.1 Remove every meaning-carrying `border-left` and replace with a tinted background and a rule above
- [ ] 5.2 Remove every em dash from generated copy
- [ ] 5.3 Write the automated check over rendered output for both rules
- [ ] 5.4 Run the check against both rendered quarters and confirm zero violations

## 6. Verify in a browser

- [ ] 6.1 Render both quarters and screenshot the first screen of each
- [ ] 6.2 Measure the rendered byte size against the email clipping threshold, with charts included
- [ ] 6.3 Confirm zero script tags and zero external asset references
- [ ] 6.4 Confirm every chart renders with no network
- [ ] 6.5 Confirm chart text is legible at published dimensions
- [ ] 6.6 Run `$impeccable critique` against the rendered output and record the findings

## 7. Record and hand off

- [ ] 7.1 Record the Flint decision in Deliverable 3 as the productionization path, with the reason it was not adopted now
- [ ] 7.2 Answer or explicitly defer the two open questions in `design.md`
- [ ] 7.3 Confirm `explore-surface` can inherit the same token set
