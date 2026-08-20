<div class="masthead">
<strong>D3 — Production hardening</strong> &amp; <strong>D4 — Handover</strong> (condensed; full:
<code>deliverable-3-hardening/README.md</code>, <code>deliverable-4-handover/README.md</code>)
</div>

## D3 — top 5 fixes before this runs unattended, ranked by impact if skipped

**1. The batch conflict has no resolution path.** 2024-01 and 2024-03 each arrived twice, 234
rows, no timestamp or revision flag to arbitrate. Pipeline defaults to `DEFAULT-BATCH-01` and
marks every derived figure provisional — honest, not useful, at 100% provisional. *Fix:* a
triage queue where a named analyst records the choice and figures promote to settled (specified,
not built).

**2. Ingestion assumes one file shape.** The 71-field crosswalk was learned by hand; real DHIS2,
HealthTrack, OpenMRS and paper forms won't hold still. *Fix:* LLM-proposed, human-confirmed,
cached column mapping — never re-inferred per run. Free win: HXL-tagged sources map by lookup,
no model call needed.

**3. Chart runtime decided for the bulletin, open for the surface that doesn't exist yet.**
Flint → Vega-Lite adopted and working. *Do not* default the unbuilt explore surface to whichever
runtime is closest to hand — decide explicitly, in writing, before its first line is written.

**4. Nothing runs on a schedule, no one is told when it fails.** Hamilton already exposes the DAG
as a callable — orchestration is a wrapper, not a rewrite. What matters more than the scheduler:
publication must gate on the 5 checks passing, and a failed run must reach a person.

**5. Facility geography is unusable.** GPS is uniform-random inside Rwanda's bounding box for all
117 facilities; the bulletin honestly maps at district grain. *Fix:* join HDX's Rwanda
Healthsites layer (1,345 real facilities, open licence). *Do not* reverse-geocode district
centroids as a substitute — that manufactures false precision.

## D4 — Handover

The deliverable is not the artifact, it's a named Digital Health Officer independently restarting
the pipeline once, unassisted, before exit. Two training sessions: run the full cycle
hands-on-keyboard-DHO; diagnose a deliberately seeded failure using only the runbook. Full
clean-rebuild verified 2026-08-11 from a wiped state — 5/5 checks passed, output reproduced at
the same byte hash, confirming the pipeline is deterministic. That run predates later pipeline
changes (ADR-0012) and has **not been re-verified against current code** — flagged here, not
hidden; re-running and diff-checking the hash is the next action before reproducibility can be
re-claimed.

Three documents answer "what would you hand the MoH IT team" and ship in the repository, not
this PDF — at nine pages combined they would have made D3+D4 a third of a document whose brief
asks for 80% of the effort on D1+D2:

`deliverable-4-handover/runbook.md` · `data-contract.md` · `decision-register.md`

**Full detail for all four deliverables, the pipeline code, and the openspec behaviour specs:**
**github.com/nyashkn/sand-fde-int**


<div class="pagebreak"></div>

