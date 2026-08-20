# DESIGN.md

Derived from tokens already in use in `moh-rwanda-research/out/moh-rwanda-architecture.v2.html`.
Not authored fresh: two artifacts for one client should not look unrelated.

## Colour

Warm neutrals with an earth accent. Deliberately not the category reflex for this domain
(white and teal), which the design laws call out by name as a first-order cliché.

**Superseded by the Swiss/Economist redesign, `decisions/0012`.** The palette below is the
one this project shipped with; the table was not updated when the redesign landed. Current
tokens, from `deliverable-2-prototype/web/src/styles/tokens.css`:

| Token | Value | Role |
|---|---|---|
| `--ink` | `#161513` | Headings, primary text, page border |
| `--paper` | `#f6f4ef` | Page background |
| `--panel` | `#fffef9` | Surfaces that must lift off the page |
| `--red` | `#c22029` | Sole accent: section numbers, provisional state, benchmark rules |
| `--gray-track` | `#e2ded2` | Tinted blocks, table zebra |
| `--gray-mid` | `#6b6659` | Secondary text, labels |
| `--gray-line` | `#c9c4b4` | Structural rules, hairlines |

Every text/background pair clears WCAG AA (4.5:1) at full saturation (measured: ink/paper
16.6:1, red/paper 5.41:1, gray-mid/paper 5.21:1), which is why there is no darkened `-d`
variant of any colour, unlike the palette this replaced.

**Strategy: restrained.** Tinted neutrals plus one accent under 10% of surface.

### Category accents

**Removed in the redesign.** The category-accent palette below no longer exists in
`tokens.css` or `charts.ts`; `THEME_SPEC` themes every chart with the single `--red` accent.
Kept here for the record of what the architecture artifact originally specified:

`--cat-a #C36A47` · `--cat-b #3E857C` · `--cat-c #8A6B9E` · `--cat-d #B58A34`
`--cat-e #5E7FA6` · `--cat-f #6F855A` · `--cat-g #94806F` · `--cat-h #A9532F` · `--cat-i #86857D`

### State channels

State is never carried by colour alone. Every state has a second, non-colour channel so it
survives a scanning reader and a greyscale render.

| State | Colour | Second channel |
|---|---|---|
| Settled | `--ink` | none needed, it is the default |
| Provisional | `--red` | diagonal hatch fill in charts, hollow points in dot plots, dashed lines in trends, underlined in tables |
| Unmeasured | `--gray-mid` | explicit glyph, never an empty cell |

There is no "Withheld" state. `decisions/0012` removed the withhold gate: a check that fails
its statistical bar renders its full panel unconditionally, with a caveat sentence stating so,
never a blank section.

## Typography

**Font stacks below are superseded**, same redesign, same `tokens.css`:

| Token | Stack |
|---|---|
| `--serif` | `'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, 'Times New Roman', serif` |
| `--slab` | `Rockwell, 'Roboto Slab', Georgia, 'Times New Roman', serif` |
| `--sans` | `'Helvetica Neue', Helvetica, Arial, sans-serif` |
| `--mono` | `'SFMono-Regular', 'IBM Plex Mono', Menlo, Consolas, 'Courier New', monospace` |

`--slab` did not exist at the version of this document below the line; it is what the
verdict-first headline figure uses today.

Serif for headings. Slab for the headline figure. Sans for body. Mono for identifiers, codes,
measurements, and anything a reader might copy.

Scale, ratio 1.25 or greater between adjacent steps. **Every row below is stale**, same
redesign. Each was re-verified against the selector that implements it in `bulletin.css`,
confirmed by where that selector is actually used in `Bulletin.astro` (a role name matching
a class name was not treated as proof by itself):

```
88        headline figure    .answer-figure     slab 800   (was 44, serif 600)
30        page title         .masthead h1       slab 800   (was 34, serif 600)
21        section heading    h2 (the § N titles) slab 700  (was 23, serif 600)
17        subheading         .implication       sans 600   (was 16, sans 650)
14.5      lead               .verdict-para       sans 400   (was 15, unchanged weight)
14        body               p                   sans 400   (unchanged)
13        table cell         td (inherits table) sans 400   (unchanged)
10        table header, label th                 mono 500, tracked .08em   (was 11, weight/tracking unchanged)
9         state tag          .tag                mono 600, tracked .06em   (was 10, weight/tracking unchanged)
```

"Headline figure, page title" and "subheading, lead" were originally one row each, a
paired value for two roles; the pairing held once verified, so each is split into its own
row above rather than kept as a slash pair, for a direct one-role-to-one-number match.

**"State tag, provenance" did not survive as a single row.** They were documented as one
treatment; they are two today. `.tag` (`tr` state markers: provisional/settled/caveat/
unmeasured) matches the original mono 600, tracked .06em exactly, at 9px not 10, corrected
above. `a.lineage` (the "lineage, §N" links) is also mono at 10px, matching the original
size, but renders at weight 400 with no letter-spacing, not mono 600 tracked .06em. The two
roles diverged; there is no single accurate row for both, which is itself the finding.

Body line length capped at 72ch.

## Spacing

Rhythm rather than a uniform grid. Section separation is deliberately larger than internal
padding so the eye finds section boundaries while scanning.

```
--s-1: 4px    --s-2: 8px    --s-3: 12px   --s-4: 16px
--s-5: 24px   --s-6: 32px   --s-7: 48px   --s-8: 72px
```

Section top margin `--s-8`. Internal block padding `--s-4` to `--s-5`. Table cell padding
`--s-2` vertical, `--s-3` horizontal.

## Structure

- No side-stripe borders. A block distinguishes itself with a tinted background and a rule
  above, never a coloured left or right border.
- No card grids. Tables and charts sit directly on the page.
- Rules are hairlines except the one under a section heading.
- No em dash anywhere in rendered copy.

## Charts

**Superseded, `decisions/0012`.** Observable Plot and Mosaic were replaced: charts now
compile a Flint spec to Vega-Lite, rendered to static SVG by `vega`, headless, at build time
(`web/src/lib/charts.ts`). The interactive surface that would have used Mosaic vgplot in
islands was never built; it remains scoped, not implemented. There is one chart runtime
today, not the two this section originally described.

| Figure kind | Chart | Channels |
|---|---|---|
| `ranking` | horizontal bar | x = value, y = entity |
| `distribution-across-units` | sorted dot plot with reference rule | x = value, y = entity, rule = benchmark |
| `grouped-by-category` | grouped bar | x = category, y = value, group = category |
| `district-trend` | line, one series per district plus a bolder national overlay | x = quarter, y = value, detail = district |

A `composition` kind (stacked bar) was registered and removed. Five causes needed five
hues in a one-accent palette, its percentage labels collided, and it sat directly above a
table carrying the same numbers plus their ICD-10 codes. A chart is registered only when
it does something a table cannot. `rate-vs-benchmark`, in this table's earlier version, no
longer exists; `grouped-by-category` and `district-trend` replaced it, added for the
capability/contradiction mart outputs and the four-quarter trend section.

A figure kind absent from this table fails the render. It is never improvised.

Axis labels, tick values and annotations are legible at published dimensions. Charts carry no
title element; the section heading is the title.

## Verification

`node scripts/check-style.mjs` runs over built output and fails on: any em dash, any
`border-left` or `border-right` above a hairline carrying colour, any `<script>` tag, any
external asset reference, or template code (a function, `[object Object]`, `undefined`)
that leaked into rendered markup.
