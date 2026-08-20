<div class="masthead">
<strong>Forward Deployed Engineer assignment</strong> &middot; Kinyanjui Njoroge &middot; August 2026 &middot;
Live bulletin: sand-fde-bulletin.pages.dev &middot; Repo: github.com/nyashkn/sand-fde-int &middot;
Full working notes, runbook, data contract and decision register are in the repository.
</div>

<p class="disclosure">All figures below are computed on <strong>synthetic data</strong> &mdash; the assignment CSVs plus a hand-built DHIS2 sample &mdash; not real Rwanda health records. Facility mortality of 14.3&ndash;73.2 per 1,000 live births runs three to four times real Rwandan rates.</p>

## The choice: Problem A, and why not B or C

| Option | Verdict | Why |
|---|---|---|
| **A &mdash; Quarterly Health Bulletin, automated** | **Chosen** | Only option finishable and provable in 6 weeks; operates on data that already arrives, in a shape that already exists. The trust wedge for later work. |
| B &mdash; Real-time facility dashboard | Out of reach this sprint | Needs facility-level freshness. Reporting substrate is monthly aggregates on a 2&ndash;3wk lag &mdash; a granularity/cadence gap, not a coverage gap, regardless of how many facilities report. |
| C &mdash; Unified patient view (TB/HIV) | Rejected | Needs a clinical-safety hazard analysis that does not fit in 6 weeks. Propose a weekly reconciliation report instead &mdash; flags likely co-infection for human review, no record merging, none of the risk. |

**How this survived review.** The choice was prompted hostilely against three independent model families (GPT-5.6-sol, Gemini 3.1 Pro, Grok 4.5). All three independently chose Problem A &mdash; but rejected the original justification, unanimously finding errors (an impossible 5-day publication target given the 2&ndash;3wk upstream lag; an overstated ROI baseline; a false claim that A's mart is "most of" B's data layer). All corrected in the full document.

## What was built

A pipeline that reads the five provided CSVs plus a DHIS2-shaped sample, resolves every field through a 71-row declared crosswalk, and publishes all four 2024 quarters as self-contained HTML with zero client-side JavaScript. Python + Hamilton + DuckDB + Parquet (bronze &rarr; silver &rarr; gold &rarr; checks); Astro + Vega-Lite compiled to static SVG for render. 5 automated checks gate publication, each one added because it caught a real defect.

## Two findings that shaped it more than any metric in the brief

**1 &mdash; The largest cause of neonatal death isn't a clinical cause.** `death_other` is 30.7% of resolved deaths, the largest single bucket in all ten held months (28.8%&ndash;32.1%). The two named causes behind it can't be separated: birth asphyxia 23.7% vs prematurity 23.6%, a gap of 15 deaths in 9,036 &mdash; and which one leads flips between months. A bulletin ranking named clinical causes would be reporting noise. The finding is about the reporting system, not newborn medicine.

**2 &mdash; A striking correlation is a confound.** A composite equipment index correlates &asymp; &minus;0.87 with facility mortality, pooled across 117 facilities &mdash; reads as "equip facilities, save newborns." Stratified by tier it collapses to near zero: District &minus;0.07, Health Centre +0.04, Provincial &minus;0.29. The pooled number describes which tier a facility sits in, not what equipping it would do. Publishing the pooled figure alone would have pointed a Ministry's budget at a confound; the bulletin shows every covariate pooled and within tier, caveat attached, not withheld.


<div class="pagebreak"></div>

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


<div class="pagebreak"></div>

