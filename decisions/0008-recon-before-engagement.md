# 0008 — Ship pre-engagement recon as a reusable pipeline (Deliverable 0)

- **Date:** 2026-08-10
- **Status:** Accepted

## Context

Every deliverable in this repo assumes the terrain is understood — which systems exist, who
touches them, how they connect, what the data-protection regime demands. [0001](0001-research-before-scoping.md)
already committed to research before scoping, but did it as a one-off pass for this assignment.
The same need recurs at the start of *any* engagement, and doing it by hand each time is slow and
inconsistent. There is a reusable machine hiding in the one-off.

Separately, the FDE artifacts in `artifacts/` are hand-built HTML. A repeatable way to generate a
sourced, readable landscape map — and to *verify* it looks right — would make the recon step a
deliverable rather than a prerequisite buried in prose.

## Decision

Package the recon as `deliverable-0-recon/`: three [fabro](https://fabro.sh) workflows
(`recon` → `refine` → `polish`) that take a target org and produce a self-contained HTML artifact
(systems map, persona journeys, integration/data-flow, data-protection posture), fully sourced.

Two design commitments worth recording:

- **A machine-vision review loop.** The artifact is screenshotted and shown to a vision model that
  critiques it; a refine pass applies the critique. This catches what a text-only agent cannot see
  (overlapping labels, unreadable contrast, density). fabro agents are text-only, so the vision runs
  in a side-channel script and only its text critique re-enters the graph.
- **A subtractive polish pass, gated on the vision verdict.** Adding content and improving
  readability are opposing forces; a refiner told to add makes a page denser every pass. The polish
  pass may only restyle, never change facts, and the run fails while the vision verdict is still
  "weak".

The Rwanda MoH is the worked example, since it is this assignment's target — but the pipeline is
target-agnostic (`pipeline/` is parameterised; `example-moh-rwanda/` is the concrete run).

## Alternatives

- **Keep recon as prose in D1.** What 0001 did. Fine for one target, but not reusable and not
  independently verifiable — the reader takes the landscape on trust.
- **`git init` the recon workspace as its own repo, decide at submission whether to include it.**
  Keeps this repo clean, but it orphans the work from the assignment it serves and defers a
  decision that is cheap to make now. Rejected in favour of committing it here on a branch; it can
  still be excluded from a final submission by not merging the branch.
- **Hand-build each artifact (as with `artifacts/01–03`).** Higher craft ceiling per artifact, but
  no leverage across engagements and no built-in verification.

## Reverses if

The generated artifact is consistently worse than a hand-built one, or the pipeline needs so much
per-target hand-tuning that it saves no time over doing the recon manually — i.e. the "reusable"
claim doesn't survive a second, non-MoH target.
