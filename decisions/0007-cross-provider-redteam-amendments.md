# 0007 — Red-team D1 across three model families, and amend

- **Date:** 2026-08-09
- **Status:** Accepted
- **Supersedes nothing.** Amends decision [0006](0006-problem-a-plus-handover-act.md) — the choice
  stands, the justification was rebuilt.

## Context

Decision 0006 selected Problem A via a six-persona council. That council was **single-provider**
(Claude-only, by instruction), and it said so in its own verdict: it could not separate *"A is
correct"* from *"one model's priors, run six ways, land on A."*

Leaving that unresolved would have meant shipping a scoping document whose central claim rested on
a review process that had structurally disqualified itself from validating it.

## Decision

Run a hostile cross-provider review of the D1 document — not a second council. Three frontier
models from three different families, one pass each, prompted explicitly against sycophancy and
told how the first review was produced and why it was suspect:

- `openai/gpt-5.6-sol`
- `google/gemini-3.1-pro-preview`
- `x-ai/grok-4.5`

Cost: three API calls. Runner preserved at `redteam-d1-cross-provider/redteam.py`.

## Result

**All three verdicts: `survives-with-amendments`. All three independently chose Problem A.**

So the *choice* is not a single-family artifact. Grok stated the finding precisely:

> "Same selection, weaker confidence in the supporting theory. Different model family, same wedge
> logic; the council's blind spot was justification quality, not the letter A."

### Unanimous errors (all three)

| # | Error | Fix |
|---|---|---|
| 1 | "Published within 5 working days of quarter close" is **impossible** — DHIS2 runs 2–3 weeks behind and nothing in A makes inputs arrive faster | Metric re-based on **data availability**, not quarter close |
| 2 | "A's mart is most of B's data layer" is **false** — aggregate period-grain ≠ real-time operational | Claim withdrawn explicitly; replaced with what actually transfers (org-unit dimension, indicator dictionary) |
| 3 | "40 hrs/month" vs "40 hrs/cycle" for a *quarterly* artifact — ~3× ROI inflation | No number committed; a **90% reduction** against a Week-1 measured baseline |
| 4 | "Nothing greenfield" converted **job-posting copy into an existence proof** — against my own research file, which grades it *strong*, not *confirmed* | Downgraded to a Week 1 question; added gate G4 |

### The single most valuable catch (GPT-5.6-sol)

> "**Paper-only" is improperly equated with "not reporting.**" A facility can use paper clinical
> registers while still submitting monthly aggregate HMIS forms keyed into DHIS2 at district level.

This is a **domain error, not a logic error**, and it was load-bearing: it was the principal
argument against B and the basis for marking 70% of facilities non-reporting. Paper-at-the-facility
with aggregate-reporting-via-district is the standard African HMIS model.

New §1.3 disaggregates six reporting states and makes establishing the real distribution a Week 1
task. Consequences: the bulletin's coverage may be much better than assumed; the sampling-bias
warning becomes conditional; and the argument against B shifts from *absence* to *granularity and
cadence* — which is both more accurate and more durable.

### Other accepted corrections

- **The root outcome statement selected for B while I chose A** (Grok). "Acts on data within the
  period it describes" cannot be served by a quarterly retrospective artifact. That was a
  reverse-fit. Root rewritten; the gap between the valuable outcome and the reachable one is now
  stated openly in §2.2 rather than papered over.
- **O1–O4 were invented framings presented as stakeholder quotations** (GPT). Now labelled
  `[hypothesis]`. Also removed an unfounded gender attribution for the Director.
- **Hosting, service accounts and InfoSec were absent entirely** (all three, independently). The
  classic six-week government-deployment killer. Moved *into* scope with a Day 4 meeting and gate G4.
- **"Aggregate-only, therefore out of PHI scope entirely" is too categorical** (GPT, Grok).
  Small-cell suppression added as a requirement.
- **Committing at end of Week 1 while validating existential assumptions in Week 2 is incoherent**
  (GPT). Added §2.5a — five explicit pass/fail gates.
- **Success criteria assumed a quarter boundary falls inside the sprint by luck** (Grok, GPT).
  Replaced with a controlled **replay protocol** including a seeded failure and the approval step.
- **"If I cannot reproduce it, nobody can" is invalid** (GPT). The analyst may hold undocumented
  exclusions — the correct conclusion is "not independently reproducible from materials supplied."
- **The clinical-safety argument against C overstated the causal chain** (GPT). A unified *view*
  does not itself prescribe treatment. Re-argued: C needs a hazard analysis that does not fit in
  six weeks — which is the real reason, and a defensible one.
- **Invented precision** — "~80% of the win", "two of six weeks" — removed.
- **The VLM section was a research programme presented as a sketch** (Grok) and its confirm-each-digit
  loop may be slower than plain data entry (Gemini). Cut back to the one thing worth committing to:
  the ~50-photo accuracy measurement. Both objections recorded in-line.
- **Missing an adoption measure** (GPT) — hours saved is production efficiency, not health value.
  Added: is the bulletin reviewed before a named decision meeting, and does any exception generate
  an assigned action?
- **Missing post-exit ownership** beyond one named person (Grok, GPT). Added to §2.6.

### Rejected

- **Gemini's TOP_FIX: shift the bulletin to monthly cadence (S-A2) to justify ROI.** Sound in
  principle — and it is already S-A2 in the opportunity tree — but changing the Ministry's
  publication cadence is a Ministry decision, not an FDE decision, and taking it unilaterally in a
  first engagement is precisely the overreach §2.4 exists to prevent. Correct move is to propose it
  once A works, with the automation as the evidence that it is now cheap.

## Reverses if

Nothing here reverses the choice of Problem A — three independent families converged on it. The
Week 1 gates in §2.5a are what would reverse it, and G1 (does anyone use the bulletin) is the one
most likely to fire.

## What this cost, and why it was worth it

Three API calls. It found four unanimous errors, one load-bearing domain error, and roughly a dozen
further defects in a document I had already put through a six-round adversarial process and
believed was good.

The generalisable lesson: **a single-provider review can produce excellent internal argument quality
and still not be an independent second opinion.** The council improved how well the position was
argued. It could not tell me the position was argued for the wrong reasons. Only a different
training lineage did that.
