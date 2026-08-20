<div class="masthead">
<strong>D3 &mdash; Production hardening</strong> &amp; <strong>D4 &mdash; Handover</strong> (condensed; full: <code>deliverable-3-hardening/README.md</code>, <code>deliverable-4-handover/README.md</code>)
</div>

## D3 &mdash; top 5 fixes before this runs unattended, ranked by impact if skipped

**1. The batch conflict has no resolution path.** 2024-01 and 2024-03 each arrived twice, 234 rows, no timestamp or revision flag to arbitrate. Pipeline defaults to `DEFAULT-BATCH-01` and marks every derived figure provisional &mdash; honest, not useful, at 100% provisional. *Fix:* a triage queue where a named analyst records the choice, with who/when/why, and figures promote to settled (specified, not built). *Do not* block the pipeline on approval &mdash; a Ministry with near-zero IT capacity would then get no bulletin at all.

**2. Ingestion assumes one file shape.** The 71-field crosswalk was learned by hand; real DHIS2, HealthTrack, OpenMRS and paper forms won't hold still. *Fix:* LLM-proposed, human-confirmed, cached column mapping &mdash; never re-inferred per run. Free win: HXL-tagged sources map by lookup, no model call needed.

**3. Chart runtime decided for the bulletin, open for the surface that doesn't exist yet.** Flint &rarr; Vega-Lite adopted and working; it replaced Observable Plot outright. *Do not* default the unbuilt explore surface to whichever runtime is closest to hand when that work starts &mdash; decide explicitly, in writing, first.

**4. Nothing runs on a schedule, no one is told when it fails.** Hamilton already exposes the DAG as a callable &mdash; orchestration is a wrapper, not a rewrite. What matters more than the scheduler: publication must gate on the 5 checks passing, and a failed run must reach a person.

**5. Facility geography is unusable.** GPS is uniform-random inside Rwanda's bounding box for all 117 facilities; the bulletin honestly maps at district grain. *Fix:* join HDX's Rwanda Healthsites layer (1,345 real facilities, open licence). *Do not* reverse-geocode district centroids as a substitute &mdash; that manufactures false precision.

**Already hardened, not just flagged:** disclosed-not-withheld statistical caveats (temporal-signal and stratification checks always annotate, never gate); cross-surface figure agreement (`check-agreement.mjs`, 7 shared figures); filename/content mismatch refused at publish; chart-palette drift against the stylesheet (`check-tokens.mjs`); per-figure lineage recorded for every published number.

## D4 &mdash; Handover

The deliverable is not the artifact, it's a named Digital Health Officer independently restarting the pipeline once, unassisted, before exit. Two training sessions: Session 1 (60&ndash;90min) the DHO drives the full cycle hands-on-keyboard against last quarter's real data, reading every check pass rather than trusting a green tick; Session 2 (45&ndash;60min) diagnoses a deliberately seeded failure &mdash; a renamed CSV column, a check made to fail on purpose &mdash; using only the runbook's recovery table. Success is naming which document to open, not fixing that specific break.

Full clean-rebuild verified 2026-08-11 from a wiped state (`mart`, `web/dist`, `node_modules`, `.venv` all removed): sync &rarr; rebuild (10 parquet files) &rarr; publish (both quarters) &rarr; verify &mdash; 5/5 checks passed, output reproduced at the same byte hash. That run predates later pipeline changes (ADR-0012) and has **not been re-verified against current code** &mdash; flagged here, not hidden; re-running and diff-checking the hash is the next action before reproducibility can be re-claimed.

Three documents (`deliverable-4-handover/runbook.md` &middot; `data-contract.md` &middot; `decision-register.md`) answer "what would you hand the MoH IT team" and ship in the repository, not this PDF. **Full detail for all four deliverables, the pipeline code, and the openspec behaviour specs: github.com/nyashkn/sand-fde-int**
