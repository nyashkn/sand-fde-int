# DESIGN.md

Derived from tokens already in use in `moh-rwanda-research/out/moh-rwanda-architecture.v2.html`.
Not authored fresh: two artifacts for one client should not look unrelated.

## Colour

Warm neutrals with an earth accent. Deliberately not the category reflex for this domain
(white and teal), which the design laws call out by name as a first-order cliché.

| Token | Value | Role |
|---|---|---|
| `--ink` | `#1A1917` | Headings, primary text |
| `--ink-soft` | `#3D3D3A` | Body text |
| `--muted` | `#5A5248` | Secondary text, labels |
| `--paper` | `#FFFFFF` | Surfaces that must lift off the page |
| `--cream` | `#FAF9F5` | Page background |
| `--oat` | `#EFEBE0` | Tinted blocks, table zebra |
| `--rule` | `#DED9CC` | Structural rules |
| `--rule-2` | `#ECE8DD` | Hairlines inside tables |
| `--clay` | `#C36A47` | Primary accent, section numbers |
| `--clay-d` | `#A9532F` | Accent text on light backgrounds |
| `--olive` | `#6F855A` | Settled, complete, positive |
| `--sage` | `#A8B89A` | Olive at low emphasis |

**Strategy: restrained.** Tinted neutrals plus one accent under 10% of surface. Data
visualisation is the exception, where the category accents below carry meaning.

### Category accents

Inherited from the architecture artifact. Used only where a chart needs more than one series.

`--cat-a #C36A47` · `--cat-b #3E857C` · `--cat-c #8A6B9E` · `--cat-d #B58A34`
`--cat-e #5E7FA6` · `--cat-f #6F855A` · `--cat-g #94806F` · `--cat-h #A9532F` · `--cat-i #86857D`

### State channels

State is never carried by colour alone. Every state has a second, non-colour channel so it
survives a scanning reader and a greyscale render.

| State | Colour | Second channel |
|---|---|---|
| Settled | `--olive` | none needed, it is the default |
| Provisional | `--clay` | diagonal hatch fill in charts, dotted bottom rule in tables |
| Withheld | `--clay` on `--oat` | occupies the full panel position it would have had |
| Unmeasured | `--muted` | explicit glyph, never an empty cell |

## Typography

| Token | Stack |
|---|---|
| `--serif` | `ui-serif, Georgia, "Times New Roman", Times, serif` |
| `--sans` | `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif` |
| `--mono` | `ui-monospace, "SF Mono", Menlo, Monaco, monospace` |

Serif for headings and the headline figure. Sans for body. Mono for identifiers, codes,
measurements, and anything a reader might copy.

Scale, ratio 1.25 or greater between adjacent steps:

```
44 / 34   headline figure, page title      serif 600
23        section heading                   serif 600
16 / 15   subheading, lead                  sans 650 / 400
14        body                              sans 400
13        table cell                        sans 400
11        table header, label               mono 500, tracked .08em
10        state tag, provenance             mono 600, tracked .06em
```

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

One grammar across static and interactive: Observable Plot at build time, Mosaic vgplot in
islands. Mosaic is built on Observable Plot, so a single registry serves both.

| Figure kind | Chart | Channels |
|---|---|---|
| `ranking` | horizontal bar | length = value, y = entity |
| `distribution-across-units` | sorted dot plot with reference rule | x = value, y = entity, rule = benchmark |

A `composition` kind (stacked bar) was registered and removed. Five causes needed five
hues in a one-accent palette, its percentage labels collided, and it sat directly above a
table carrying the same numbers plus their ICD-10 codes. A chart is registered only when
it does something a table cannot.
| `rate-vs-benchmark` | dot plot with benchmark rule | x = rate, rule = benchmark |

A figure kind absent from this table fails the render. It is never improvised.

Axis labels, tick values and annotations are legible at published dimensions. Charts carry no
title element; the section heading is the title.

## Verification

`node scripts/check-style.mjs` runs over built output and fails on: any em dash, any
`border-left` or `border-right` above a hairline carrying colour, any `<script>` tag, any
external asset reference.
