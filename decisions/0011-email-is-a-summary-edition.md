# 0011 - Email is a summary edition, not the bulletin inlined

- **Date:** 2026-08-10
- **Status:** Accepted
- **Method:** measured against the built output; each rejection has a number

## Context

ADR 0010 established that Astro renders every surface from one token set. That left open
what the email surface actually contains. The assumed answer was "the bulletin, with its
CSS inlined" - the standard email-HTML pattern, and the one the tasks were written for.

Two measurements killed it.

**Bytes.** Inlining the full bulletin produced 99.0 KB against Gmail's ~102 KB clipping
threshold: 3 KB of headroom on the first quarter, before Q2 adds a row. Gmail hides
everything past the threshold behind "[Message clipped]", and the disclosure sections -
withheld panels, known defects, lineage - are at the bottom. The first thing clipped is
the part that makes the document trustworthy.

**Rendering.** 33.8 KB of that payload was inline SVG. Embedded `<svg>` is unsupported in
Gmail, Outlook and Yahoo (caniemail: ~38% support), and Microsoft began retiring inline
SVG in Outlook in August 2025. The charts do not draw for most recipients.

So the inlined bulletin spends 97% of a hard budget to ship charts the majority of readers
cannot see, and clips the disclosures to do it.

## Decision

The email edition is a **separate, smaller document** that carries what survives a client
which can draw nothing: the figure, its state as a word, what backs it, what is missing,
and a link to the full bulletin.

No charts. No SVG. Table layout, since Outlook's Word engine supports neither flex nor
grid. It measures **6.3 KB, 6% of the ceiling**.

This is not a reduction in scope. It is the split already agreed earlier in the
engagement: the email carries the number and its state, the bulletin carries the rows,
rules, conflicts and absent periods. This ADR records that email cannot carry more, and
supplies the numbers.

## Consequences

**The state-not-colour rule extends one surface further.** DESIGN.md requires state to
survive greyscale. Email requires it to survive a client that drops CSS entirely, so
`provisional` and `withheld` appear as words in the copy, not only as hatch or hollow
markers. `check-email.mjs` enforces it.

**Three surfaces now share one mart and one token set**, and the stylesheet is split so
the email never ships rules it cannot honour. A `display:grid` sitting unused in the email
stylesheet fails `check-email.mjs`; that is deliberate, and it is what forced the split.

**Two surfaces can disagree.** They format shared figures independently, and did: the
email counted withheld guard *rows* and published 6 where the bulletin counted *panels*
and published 2. Same data, same build, two answers. Fixed by deriving the count once in
the mart, and held by `check-agreement.mjs`, which compares six shared figures in the
rendered HTML of both surfaces.

That check is the one most worth keeping. Every other rule here protects rendering; this
one protects the claim the whole deliverable rests on - that a figure means the same thing
wherever the Ministry reads it.

## Reverses if

- The Ministry's clients change such that inline SVG renders in Gmail and Outlook, and
  the full document fits under the clip threshold with charts included.
- A raster path is added at build time, making PNG charts cheap enough to inline. The
  byte ceiling still binds, so this would be a chart or two, not the document.

## Artifacts

- `deliverable-2-prototype/web/src/pages/email.astro` - the edition
- `deliverable-2-prototype/web/scripts/check-email.mjs` - ceiling, SVG, flex/grid, state words
- `deliverable-2-prototype/web/scripts/check-agreement.mjs` - cross-surface figure agreement
- `bun run verify` - build, inline, and all three checks
