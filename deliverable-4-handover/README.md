# Deliverable 4, Handover

Reversing ADR 0006: the deliverable is not the artifact, it is a named Digital Health
Officer personally restarting the pipeline once, unassisted, before exit. That is the line
between real capacity transfer and "shifting the burden": a finished tool handed to a
Ministry with near-zero IT capacity degrades post-exit and leaves trust lower than before.

## Contents

The three documents below are the answer to "what would you document for the MoH IT
team". They are written, not proposed. They ship in the repository at
`deliverable-4-handover/` rather than in this PDF, because at nine pages they would have
made Parts 3 and 4 a third of a document whose brief asks for 80% of the effort on
Parts 1 and 2.

- `runbook.md`: the four-command quarterly cycle, what each check failing means, how to
  recover from a failed run.
- `data-contract.md`: the required input shape, the crosswalk, and precisely what
  happens when a source column is renamed, absent, or new (verified by running each
  case, not inferred).
- `decision-register.md`: what happens to a batch conflict today (`DEFAULT-BATCH-01`,
  unconditional, provisional), and what is specified but not built (the triage queue).

## Exit criterion

A named DHO, given only these three documents and no live assistance, runs the full
quarterly cycle from a clean checkout and produces a bulletin that passes all five checks.

**Not yet satisfied.** This requires a named person with cleared hours, which ADR 0006's
own kill criteria treat as an unconfirmed empirical fact rather than an assumption:
"Nobody has asked whether a named DHO has cleared hours." What this deliverable can and
does verify is the half of the criterion within this repo's control: that the runbook
itself is complete enough for an unassisted restart to succeed, by following it literally
against a fully wiped state. See "Verification" below.

## Training plan

Two sessions, because the runbook is four commands and the judgment calls are what
actually need a person, not a memorised sequence.

**Session 1 (60 to 90 min): run the cycle.** Screen-share, the DHO drives, I do not touch
the keyboard. `runbook.md` end to end against last quarter's real data: sync, rebuild,
publish, verify. The DHO reads every line the terminal prints, including a full checks
pass, so "verify passed" has a face they have seen, not a green checkmark they trust
blind.

**Session 2 (45 to 60 min): read a failure.** I break something in a scratch copy in
front of them (a renamed CSV column, per `data-contract.md`; a check made to fail on
purpose, then restored) and the DHO diagnoses it using only `runbook.md`'s recovery
table. Success is the DHO stating which document to open before I tell them, not fixing
the specific break, since next quarter's break will not be this one.

Between sessions: the DHO gets read access to this repo, `data-contract.md`, and one
week to sit with the material before session 2, which is deliberately the same cadence
ADR 0006's Week 1 Day 2 action treats as the earliest honest checkpoint on this handover.

## Verification

Run 2026-08-11, from a fully wiped state (`pipeline/mart`, `web/dist`,
`web/node_modules`, `pipeline/.venv` all removed), following `runbook.md`'s "Full clean
rebuild" section with no step added, removed, or reordered from what is written there:

```
uv sync                                    ok
uv run python run.py                       ok, 10 parquet files written
bun install                                ok
bun run publish                            ok, both quarters published
bun run verify                             5/5 checks passed
```

`output/bulletin-2024-Q1.html` regenerated at the same byte hash
(`05ce82f7889cc85f38ec61cdf3d4e0ab`) as the previously committed copy, on a rerun with no
inputs changed, confirming the pipeline is deterministic rather than merely "usually
working."

**This run predates ADR 0012 and is stale.** The withhold-gate removal, the four-quarter
build, the four new gold-layer tables, and the Flint chart rewrite all landed after
2026-08-11 and change what this command sequence produces: `run.py` now writes 14
parquet files (`facility_capability`, `capability_summary`, `cause_capability_links` and
`known_contradictions` joined the original ten), and `bun run publish` builds all four
quarters, not two. The committed `output/bulletin-2024-Q1.html` at the current commit
hashes to `2bafa326c8925bfe508bc337e97e9e6e`, which does not and should not match the
2026-08-11 hash above; the underlying document changed on purpose. What this run does
**not** re-establish is the determinism claim itself: I did not rerun the full clean
rebuild against the post-ADR-0012 code for this pass, specifically to avoid writing into
`deliverable-2-prototype/` while it has other work in flight. Re-running `runbook.md`'s
"Full clean rebuild" section once, twice, and diffing the two hashes is the next action
before this deliverable can claim reproducibility again; until then, treat determinism as
carried over by design but **not measured** post-rework.

One correction to the sentence above, since it was measured after this was first written
and the earlier wording would not survive a reviewer running the pipeline twice. The mart
is **not** byte-identical between runs, and by design: `bronze.py` stamps every row with
`ingested_at = datetime.now(timezone.utc)`, one timestamp per run, so that one run is one
provenance event. Two consecutive runs therefore produce differing `silver.parquet` and
`observations_resolved.parquet`. Excluding that column and sorting, every other column is
byte-identical. So the accurate claim is that the pipeline is deterministic **in its
outputs given its inputs, excluding the provenance timestamp it deliberately varies**, not
that the files hash the same. The rendered bulletin is unaffected, because no figure reads
`ingested_at`. This proves the runbook's commands were sufficient for
a rebuild from nothing as of 2026-08-11. It never proved, and still cannot prove, that a
specific named person can execute them unassisted; that half of the exit criterion is the
confirmation named in "Exit criterion" above, still open.

## What is deliberately not here

No architecture diagram beyond what `decisions/` and `openspec/specs/` already carry;
duplicating it here would be a second copy that drifts from the first. No slide deck: the
brief asks for a runbook the DHO can act on at 2am with no one to call, and a deck is not
that document.
