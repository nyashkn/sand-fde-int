# Deliverable 4, Handover

Reversing ADR 0006: the deliverable is not the artifact, it is a named Digital Health
Officer personally restarting the pipeline once, unassisted, before exit. This is what
the council decided distinguishes real capacity transfer from "shifting the burden": a
finished tool handed to a Ministry with near-zero IT capacity degrades post-exit and
leaves trust lower than before.

## Contents

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
working." This proves the runbook's commands are sufficient for a rebuild from nothing.
It does not, and cannot, prove that a specific named person can execute them unassisted;
that half of the exit criterion is the confirmation named in "Exit criterion" above, still
open.

## What is deliberately not here

No architecture diagram beyond what `decisions/` and `openspec/specs/` already carry;
duplicating it here would be a second copy that drifts from the first. No slide deck: the
brief asks for a runbook the DHO can act on at 2am with no one to call, and a deck is not
that document.
