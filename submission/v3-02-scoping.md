<div class="masthead">
<strong>D1 &mdash; Problem decomposition &amp; scoping</strong> (condensed; full document: <code>deliverable-1-scoping/README.md</code>, red-team amendment log: <code>decisions/0007-cross-provider-redteam-amendments.md</code>)
</div>

## "Our data is a mess" is a symptom report, not a problem statement

| Failure class | Meaning | Implies |
|---|---|---|
| Absence | Never captured at all | Digitisation problem |
| Latency | Captured, arrives too late to act on | Pipeline problem &mdash; DHIS2 runs 2&ndash;3wk behind |
| Distrust | Arrives on time, nobody believes it | Provenance problem &mdash; sources disagree, nobody reconciles |
| Last mile | Believed, never reaches a decision | Workflow problem |

Week 1's job is to find which dominates. Distrust is tested first &mdash; cheapest to check, most commonly missed. One question for every interview, because the answers won't match: *"When two systems give different numbers, what happens?"*

## Who I'd talk to, in what order (Week 1)

| Day | Who | The question that matters |
|---|---|---|
| 1 | Solutions Manager, Country Director | Why were the use cases chosen before discovery? |
| 1&ndash;2 | **MoH Director** (sponsor) | *"Tell me about a decision last quarter you'd have made differently with better data."* Then: *"When the numbers you're shown disagree with what you believe, which do you act on?"* |
| 2 | The bulletin analyst | Not "what do you need" &mdash; *"show me last quarter's, and open the files you built it from."* |
| 2&ndash;3 | DHIS2/HMIS focal point | Where does the 2&ndash;3wk delay actually accrue, and how do paper facilities report today? |
| 3 | 2 district health officers (1 strong, 1 weak district) | *"What did you look at immediately before your last resource decision?"* |
| 3&ndash;4 | 1 hospital, 1 clinic, 1 paper-only facility &mdash; the data clerk, not the medical director | Watch month-end reporting happen |
| 4 | MoH ICT / InfoSec | Hosting, data residency, approval lead times &mdash; the classic 6-week killer |

Every question is counterfactual ("what did you do last month") or observational ("show me"), never solicitational ("what would you like") &mdash; solicitation just returns a feature list.

## The Week 1 gate

The commitment to A is conditional on five gates assessed at end of Week 1, not final at proposal time: **G1** Value (a decision-maker used the last bulletin for something identifiable) &middot; **G2** Mechanisability (&ge;60% of cycle time is mechanical) &middot; **G3** Inputs (DHIS2 access confirmed with a stated cutoff) &middot; **G4** Runtime (a place to run and hand over exists) &middot; **G5** Operator (a named receiver is assigned). G1 or G3 failing means A is the wrong commitment &mdash; said in Week 1, not Week 5.
