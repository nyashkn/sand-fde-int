# Bulletin design critique

Task `bulletin-design` §6.6. Run against the rendered output
(`deliverable-2-prototype/output/bulletin-2024-Q1.html`), post-distill, at 1280x900,
390x844, and greyscale. Self-review is biased toward finding nothing, so the mechanical
probes ran first, before any subjective read, and every fix below was re-measured after
applying it rather than assumed.

## Method

- Contrast: computed WCAG relative luminance and contrast ratio for every distinct
  (foreground, background, size, weight) combination actually rendered, via
  `getComputedStyle` in a live tab. Not estimated.
- Line length: `getComputedStyle(...).maxWidth`, not eyeballed.
- Tap targets: `getBoundingClientRect()` on every `<a>`/`<button>` at 390px.
- Layout: `display`, `gridTemplateColumns`, and child `getBoundingClientRect()` directly,
  because a CSS property can be set and still be a no-op under the wrong `display`.

## Findings

`location: SEVERITY problem. fix.`

- `tokens.css --clay-d`: BLOCKER 4.45:1 contrast on `--oat`, below WCAG AA's 4.5:1, on the
  provisional tag, withheld-panel headers, and every `<code>` element. Darkened to
  `#a14f2d` (4.8:1 on oat, 5.4:1 on cream). Fixed.
- `.tag.withheld`: BLOCKER white on `--clay` measured 3.84:1. Background swapped to
  `--clay-d`, now 5.7:1. Fixed.
- `.kicker`, `h2 .n`: BLOCKER `--clay` on `--cream` measured 3.64:1 on informative text
  (report scope/date, section numbers). Switched to `--clay-d`. Fixed.
- `.tag.settled`: MATERIAL `--olive` on transparent measured 3.85:1. Added `--olive-d`
  (`#627650`, 4.72:1) for tag text; `--olive` kept for fills. Fixed.
- `.receipts` at ≤760px: BLOCKER the responsive rule set `grid-template-columns` without
  `display: grid`. The base rule is `display: table` / `table-cell`, on which
  `grid-template-columns` is inert, so all four receipts still rendered in one
  86px-per-cell row at 390px width despite the media query existing. Added
  `display: grid` to the override. Reverified: genuine 2x2, all four receipts land above
  the fold (bottom 800px of an 844px viewport). This had been reported fixed earlier in
  the session on the strength of a screenshot; the screenshot was misread at reduced
  scale and the underlying `display` property was never checked.
- `.withheld-panel .lead`: MATERIAL measured `max-width: 76ch`, one character over the
  stated 65-75ch design law and inconsistent with the rest of the document's 72ch rhythm.
  Fixed to 72ch.
- `.lineage-card`, `.lineage-card h4/dl/dt/dd` (5 rules): MATERIAL dead CSS, orphaned when
  the four lineage cards were collapsed into one table during the earlier distill pass.
  Removed.
- Category-colour tokens `--cat-a` through `--cat-e`, `--sage`: MATERIAL dead, left over
  from the removed composition chart. Removed with the contrast-token edit.
- `a.lineage` inline links: COSMETIC 42x12px tap target at 390px, under the 44px
  guideline (WCAG 2.5.5, AAA-level, not the AA bar the contrast fixes cleared). Recorded,
  not fixed: these are inline running-text links in a document read primarily on desktop,
  email, and print, and enlarging them changes the reading-line rhythm for a target
  audience that is not touch-primary. Revisit if usage data shows phone reading is
  material.

## Verified clean

- Contrast: 33 distinct combinations, 0 failures after fixes (was 8).
- Heading order: H1 -> H2x6, no skipped levels.
- Body/lead paragraph line length: all at or under 72ch.
- No horizontal overflow at 390px.
- Greyscale: `withheld` tags read as dark pills with white text; tinted panel backgrounds
  distinguishable from page background. State survives colour removal.
- `check-style.mjs` (5 rules), `check-email.mjs` (5 rules), `check-tokens.mjs`,
  `check-agreement.mjs` (6 figures): all pass on the post-fix build.

## Most consequential finding

The `.receipts` grid bug. It is the second time in this project a fix was believed
applied on the strength of a screenshot and was not: the layout property that would have
made the media query inert (`display: table`) was never checked directly, only the
property the media query set (`grid-template-columns`), which reported correctly while
doing nothing. The general lesson already recorded in this project's memory, that a
control must be proven able to fail before it is trusted, applies to visual verification
too: a screenshot confirms an outcome, not a mechanism, and at reduced scale it can
confirm the wrong outcome.
