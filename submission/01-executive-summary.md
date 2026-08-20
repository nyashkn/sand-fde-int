# Executive summary

**The choice.** Problem A, the Quarterly Health Bulletin, automated end to end, with
figure-level lineage built in from the start rather than added later. B needs
facility-level freshness that monthly aggregate reporting on a two to three week lag
cannot supply, which is a cadence gap and a separate project. C matches TB and HIV
records by probability, since the systems share no patient identifier, so a wrong match
puts one patient's HIV status into another's treatment decision, and no MoH process
exists to review and sign that risk off inside six weeks. I would propose a weekly
reconciliation report instead of record merging. A is the reachable wedge, not the most
valuable outcome available, and Deliverable 1 says so in those words.

**What is built.** A working pipeline that reads the five provided CSVs, resolves every
column through a declared crosswalk, and publishes all four 2024 quarters as
self-contained HTML with no client-side JavaScript. Python with Hamilton, DuckDB and
Parquet for the data layer; Astro with Flint compiled to Vega-Lite for the render. Five
automated checks gate publication; four of them exist because they caught a real defect,
and the fifth is preventive and labelled as such rather than counted as a catch.
Setup and run instructions are in the accompanying repository.

All four editions are live at **https://sand-fde-bulletin.pages.dev**. The pages carry
no client-side JavaScript and no external assets, so they render identically offline
from the repository. Four representative pages are reproduced at the end of this
document; the site is the whole thing.

**What the data actually says, which is not what it looks like.** Two findings shaped
the bulletin more than any metric in the brief did.

The largest single category of neonatal death in this dataset is not a clinical cause.
"Other" accounts for 30.7% of resolved deaths across the year, and it is the largest
bucket in every one of the ten months held, ranging from 28.8% to 32.1%. The two named
causes behind it cannot be separated: birth asphyxia takes 23.7% and prematurity 23.6%,
a gap of 15 deaths in 9,036, and which of the two leads flips between months. So a
bulletin that ranked named clinical causes would be reporting noise, and one that led
with asphyxia as the top killer would be wrong twice over. The finding is about the
reporting system rather than about newborn medicine, and it is the more actionable of
the two.

A composite equipment index correlates about -0.87 with facility mortality across all
117 facilities, which reads as "equip facilities, save newborns." Stratified by facility
tier it collapses to near zero. The pooled number describes which tier a facility sits
in, not what equipping it would do, and the within-tier residual is too small and too
unstable across index compositions to support a claim. A bulletin that had published the
pooled figure would have pointed a Ministry's budget at a confound. Every covariate in
the bulletin is therefore shown pooled and within tier, with the caveat attached rather
than the section withheld.

**What it does not do.** It does not correct source data, redefine any indicator, touch
patient-level data, or attempt real-time anything. The 2024-01 and 2024-03 batch conflict
is disclosed, not resolved, because nothing in the file establishes which load is
authoritative and inventing a rule would be worse than naming the problem.

**One thing to hold in mind throughout.** The provided data is synthetic. Facility
mortality of 14 to 73 per 1,000 live births runs three to four times real Rwandan rates,
February and December are absent, and the facility coordinates are uniform random inside
the country's bounding box. The pipeline, the checks and the reasoning are the deliverable.
The health findings are not claims about Rwanda.
