<div class="masthead">
<strong>D1 — Problem decomposition &amp; scoping</strong> (condensed; full document:
<code>deliverable-1-scoping/README.md</code>, red-team amendment log:
<code>decisions/0007-cross-provider-redteam-amendments.md</code>)
</div>

## "Our data is a mess" is a symptom report, not a problem statement

| Failure class | Meaning | Implies |
|---|---|---|
| Absence | Never captured at all | Digitisation problem |
| Latency | Captured, arrives too late to act on | Pipeline problem — DHIS2 runs 2–3wk behind |
| Distrust | Arrives on time, nobody believes it | Provenance problem — sources disagree, nobody reconciles |
| Last mile | Believed, never reaches a decision | Workflow problem |

Week 1's job is to find which dominates. Distrust is tested *first* — cheapest to check, most
commonly missed — not because the brief's sentence says so. One question for every interview,
because the answers won't match: *"When two systems give different numbers, what happens?"*

## Who I'd talk to, in what order (Week 1)

| Day | Who | The question that matters |
|---|---|---|
| 1 | Solutions Manager, Country Director | Why were the use cases chosen *before* discovery? |
| 1–2 | **MoH Director** (sponsor) | *"Tell me about a decision last quarter you'd have made differently with better data."* Then: *"When the numbers you're shown disagree with what you believe, which do you act on?"* |
| 2 | The bulletin analyst | Not "what do you need" — *"show me last quarter's, and open the files you built it from."* |
| 2–3 | DHIS2/HMIS focal point | Where does the 2–3wk delay actually accrue, and how do paper facilities report today? |
| 3 | 2 district health officers (1 strong, 1 weak district) | *"What did you look at immediately before your last resource decision?"* |
| 3–4 | 1 hospital, 1 clinic, 1 paper-only facility — **the data clerk**, not the medical director | Watch month-end reporting happen |
| 4 | MoH ICT / InfoSec | Hosting, data residency, approval lead times — the classic 6-week killer |

Every question is **counterfactual** ("what did you do last month") or **observational** ("show
me"), never **solicitational** ("what would you like") — solicitation just returns a feature list.

## Top assumptions and risks (of 9 tracked in full)

| # | Assumption | If false |
|---|---|---|
| A3 | Reporting labour is mostly mechanical | Automate assembly only; reset the ROI target publicly |
| A7 | A named DHO with cleared hours exists | Downgrade honestly; stop calling it capacity transfer |
| A8 | The bulletin is read by someone who decides | Stop. Find what *is* read |
| A10 | Hosting / InfoSec approval achievable in ≤3 weeks | Re-plan around Ministry-owned infrastructure |

**The Week 1 gate.** The commitment to A is conditional on five gates assessed at end of Week 1,
not final at proposal time: **G1** Value (a decision-maker used the last bulletin for something
identifiable) · **G2** Mechanisability (≥60% of cycle time is mechanical) · **G3** Inputs (DHIS2
access confirmed with a stated cutoff) · **G4** Runtime (a place to run and hand over exists) ·
**G5** Operator (a named receiver is assigned). G1 or G3 failing means A is the wrong commitment —
said in Week 1, not Week 5.

## What would change my mind

| Observation | Response |
|---|---|
| Districts decide **weekly** and can't today | Re-scope toward B for adequate-granularity facilities, honestly named partial |
| The bulletin is **not read** by any decision-maker | Stop. Find what is read |
| Co-infected patients harmed **today**, measurably | Escalate C as clinical safety, resourced properly |
| Hosting/InfoSec approval takes **>3 weeks** | Re-plan around an offline deliverable; escalate Day 3 |

**How this survived review.** The problem selection was prompted hostilely against three
independent model families (GPT-5.6-sol, Gemini 3.1 Pro, Grok 4.5). All three independently chose
**Problem A** — but rejected the original justification, finding errors unanimously (an
impossible 5-day publication target given a 2–3wk upstream lag; an overstated ROI baseline; a
false claim that A's mart is "most of" B's data layer). All corrected in the full document.
