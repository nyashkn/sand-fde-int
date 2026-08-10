# 0006, Commit to Problem A plus one bounded handover act

- **Date:** 2026-08-09
- **Status:** Accepted
- **Method:** six-seat adversarial council, 3 rounds + restate gate, confidence-weighted tally

## Context

Deliverable 1 requires choosing one of Problems A, B or C for a 6-week sprint and defending
the choice. The brief states all three as *solutions*, not as needs, so the choice can only be
defended after mapping them back to the underlying opportunities.

I had already argued informally for Problem A earlier in the session, which is exactly the
condition under which a solo decision is worth least. So the selection was put through an
adversarial council rather than asserted.

## Decision

Commit to **`A-plus-handover-act`**: Problem A (bulletin automation), plus exactly one bounded
capacity-transfer act, a *named* Digital Health Officer personally runs the pipeline restart
once, unassisted, before exit. No joint architecture. No co-build. No hedged B artifact.

Consensus at **5.625** against a **4.333** threshold (`W_total` 6.5). Every rejected option
scored 0.0 in the final round.

## Alternatives

- **`A-minimal`**, ship the artifact, ordinary handover docs. Rejected: the systems seat showed
  this reproduces the "Shifting the Burden" archetype, a finished tool handed to a Ministry with
  near-zero IT capacity degrades post-exit and leaves trust *lower* than before.
- **`A-plus-cobuild`**, restructure the sprint so the DHO co-builds weeks 3–5. Rejected: makes an
  unverified counterparty the critical path, with inverted skin in the game, the FDE and Director
  eat the downside, the Solutions Manager keeps the "capacity transfer" narrative either way.
  Carries a formal dealbreaker flag.
- **`A-plus-B-sliver`**, add a read-only, stale-labelled situation map as a cheap hedge. Rejected:
  a status map's visual grammar asserts a freshness the label cannot revoke, and "read-only" does
  not bind how the artifact gets re-used politically once it exists.
- **Problem B**, real-time facility status. Rejected: 175 of ~250 facilities have no digital
  capture. Its honest scope is "real-time for 30% of the fleet."
- **Problem C**, unified TB/HIV view. Rejected on tail risk: the failure mode is a false patient
  record merge, wrong regimen, missed contraindication. A coroner's inquest, not a bug ticket.

## What the council added that I did not have

1. **A fourth opportunity the brief never names.** Two seats independently surfaced it: the
   Director's complaint is about *trust*, not throughput. "I cannot trust any number I am shown."
   A, B and C all answer throughput. Consequence: end-to-end figure traceability moves from
   nice-to-have to a stated requirement of the outcome.
2. **Round 1 unanimity was false.** All six seats picked A immediately, then cross-examination
   established they meant four incompatible things by it. Anchoring on a label, not agreement on
   a thing. My own earlier reasoning had the same defect.
3. **A cheaper answer to Problem C** that the brief does not consider: a weekly reconciliation
   report flagging co-infected patients for human review, with no record merging. Most of the
   value, none of the tail risk.
4. **The real unknown.** Nobody has asked whether a named DHO has cleared hours. Three rounds
   argued over an empirical fact that one email would settle. That becomes the Week 1 Day 2 action.

## Reverses if

Any of the five kill criteria in the artifact trip, most importantly: if no named DHO with
cleared hours is confirmed by end of Week 1, this decision downgrades to `A-minimal` and the
deliverable must stop being described as capacity transfer.

## Honest limits

Single-provider council (Claude-only, as instructed). Six personas of one model are not six
independent opinions, and no seat seriously entertained B or C as the final pick. It is not
possible from the transcript to separate "A is correct" from "this model's priors reliably land
on A." Zero empirical evidence was produced in any round, every argument reasons from the brief.
That is precisely why the output is written as falsifiable field checks rather than conclusions.

## Artifacts

- `artifacts/03-opportunity-map-council-verdict.html`, opportunity map, option comparison, tally, kill criteria, verdict
- `decisions/council-d1-problem-selection/`, briefing packet and full anonymised round records
