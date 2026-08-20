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
| C &mdash; Unified patient view (TB/HIV) | Rejected | No shared patient ID between the TB and HIV systems, so records are matched by probability. A wrong match puts one patient's HIV status into another's treatment decision, and no MoH process exists to review and sign that risk off inside 6 weeks. Propose a weekly reconciliation report instead: flags likely co-infection for human review, no record merging, no clinical claim. |

## What was built

A pipeline that reads the five provided CSVs plus a DHIS2-shaped sample, resolves every field through a 71-row declared crosswalk, and publishes all four 2024 quarters as self-contained HTML with zero client-side JavaScript. Python + Hamilton + DuckDB + Parquet (bronze &rarr; silver &rarr; gold &rarr; checks); Astro + Vega-Lite compiled to static SVG for render. 5 automated checks gate publication, each one added because it caught a real defect.

## Two findings that shaped it more than any metric in the brief

**1 &mdash; The largest cause of neonatal death isn't a clinical cause.** `death_other` is 30.7% of resolved deaths, the largest single bucket in all ten held months (28.8%&ndash;32.1%). The two named causes behind it can't be separated: birth asphyxia 23.7% vs prematurity 23.6%, a gap of 15 deaths in 9,036 &mdash; and which one leads flips between months. A bulletin ranking named clinical causes would be reporting noise. The finding is about the reporting system, not newborn medicine.

**2 &mdash; A striking correlation is a confound.** A composite equipment index correlates &asymp; &minus;0.87 with facility mortality, pooled across 117 facilities &mdash; reads as "equip facilities, save newborns." Stratified by tier it collapses to near zero: District &minus;0.07, Health Centre +0.04, Provincial &minus;0.29. The pooled number describes which tier a facility sits in, not what equipping it would do. Publishing the pooled figure alone would have pointed a Ministry's budget at a confound; the bulletin shows every covariate pooled and within tier, caveat attached, not withheld.
