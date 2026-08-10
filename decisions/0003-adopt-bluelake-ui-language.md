# 0003, Build the prototype in the Bluelake Admin UI language

- **Date:** 2026-08-09
- **Status:** Accepted

## Context

Deliverable 2 asks for a bulletin output "in a usable format (simple HTML, or dashboard)".
That's an open brief, any competent dashboard would satisfy it literally.

But the video analysis established what Sand's real product looks like in specific detail:
a two-level nav (`Dashboard | Operations | Finance | Situation Map` over
`Operational | Financial | Clinical`), a persistent filter bar (facility, date range, gender,
age group), and a repeating four-chart vocabulary, line for trend, donut for totals,
stacked bar for breakdowns, dot map for geography.

## Decision

Structure the bulletin prototype to echo that pattern rather than inventing a UI language:
same filter-bar shape, same chart vocabulary, same Operational/Clinical separation.

Two reasons, in order of weight:

1. **It's the correct engineering answer.** An FDE ships things a Ministry team maintains
   after handover. Something that looks and behaves like the platform they already run is
   cheaper to absorb than a bespoke artifact.
2. It demonstrates the research actually changed the build, rather than sitting in an
   appendix.

## Alternatives

- **Generic BI dashboard.** Satisfies the brief, signals nothing.
- **Pixel-copy the Bluelake UI.** Overfitting to marketing footage of unknown vintage, and
  the demo data behind those charts may be synthetic. Echo the structure, don't clone the
  skin.

## Reverses if

The interview reveals the real bulletin consumers work in a different tool entirely
(Excel, a PDF circulated by email), in which case matching the *consumption* format beats
matching the platform's dashboard.
