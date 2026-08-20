# Deliverable 1, Problem Decomposition and Scoping

**Role:** Forward Deployed Engineer · **Country:** Rwanda · **Sprint:** 6 weeks, 2 FDEs
**Sponsor:** MoH Director · **Internal:** Solutions Manager, Country Director, Operations Specialist

---

## How to read this

Section 1 is what I would do in Week 1 before proposing anything. Section 2 is the commitment I
would make **at the Week 1 gate**, conditional on the gate passing. Everything is written to be
falsifiable.

Assumptions are flagged **[A#]** and collected in 2.5.

**[A1]** The country is Rwanda, the brief says "one of our expansion countries (i.e. Rwanda)" and
the provided data uses Rwandan facility names, districts and RWF.
**[A2]** I have no access to a live Sand or MoH environment. Everything below is built against the
provided data and public sources, and I have tried not to convert either into an existence proof.

---

# Section 1, Discovery Process

## 1.1 "Our data is a mess" is a symptom report, not a problem statement

The sentence contains at least four distinct failure classes, implying four different projects:

| Failure class | What it means | What it would imply |
|---|---|---|
| **Absence** | Never captured at all | Digitisation problem |
| **Latency** | Captured, arrives too late to act on | Pipeline problem. DHIS2 runs 2–3 weeks behind |
| **Distrust** | Arrives on time, nobody believes it | Provenance problem. Sources disagree, nobody reconciles |
| **Last mile** | Believed, never reaches a decision | Workflow problem |

Week 1's job is to find which dominates. **I do not know which it is, and the phrase does not tell
me.** "We cannot make good decisions" is compatible with all four, it could mean missing data,
late data, inaccessible data, untrusted data, weak analysis, or absent decision authority.
Distrust is the hypothesis I would test *first* because it is the cheapest to check and the most
commonly missed, not because the sentence establishes it.

## 1.2 Who I would talk to, and in what order

| Day | Who | The question that actually matters |
|---|---|---|
| **1** | Solutions Manager, Country Director | *Why were the use cases chosen before discovery?* What does the MoU commit us to in writing, and what has been promised to whom? |
| **1–2** | **MoH Director** (sponsor) | *"Tell me about a decision last quarter you'd have made differently with better data."* Then: *"When the numbers you're shown disagree with what you believe, which do you act on?"* |
| **2** | **The bulletin analyst** | The most important interview. Not "what do you need", *"show me last quarter's, and open the files you built it from."* |
| **2–3** | DHIS2 / HMIS focal point | *Where does the 2–3 week delay actually accrue?* And critically: **how do the paper facilities report today?** (see 1.3) |
| **3** | 2 district health officers, one strong district, one weak | *"What did you look at immediately before your last resource decision?"* If the answer isn't data, B solves the wrong problem |
| **3–4** | 1 HealthTrack hospital, 1 OpenMRS clinic, 1 paper-only facility, the **data clerk**, not the medical director | Watch month-end reporting happen |
| **4** | TB and HIV programme managers | Size C honestly: how many co-infected, how identified today, what happens when one is missed |
| **4** | **MoH ICT / InfoSec** | Hosting, data residency, service accounts, approval lead times. See 2.4, this is the classic six-week killer |
| **5** | Other FDE, Central FDEs, Product | What patterns already exist. Do not rebuild |

**Question discipline.** Every question is **counterfactual** ("what did you do last month") or
**observational** ("show me"), never **solicitational** ("what would you like"). Solicitation
returns a feature list reflecting what the person thinks you can build.

**One question for everyone**, because the answers will not match:
> *"When two systems give different numbers for the same thing, what happens?"*

## 1.3 The reporting-status question I got wrong, and would now ask first

My first draft treated "paper-only facility" as equivalent to "absent from DHIS2." **That is
probably false, and it was load-bearing.** A facility can keep paper clinical registers and still
submit a monthly aggregate HMIS form that a district data clerk keys into DHIS2. That is the
standard model across most African HMIS deployments.

So Week 1 must establish the actual distribution across at least six states, not one:

1. No patient-level digital system, **but aggregate HMIS reporting via district** ← likely the majority
2. No local DHIS2 access, reports on paper to an intermediary
3. Reports directly but **late**
4. Reports but **incomplete** (subset of indicators)
5. Reports **inconsistently** (some months)
6. Genuinely absent from the national feed

**Why this changes things materially:** if most of the 175 do reach DHIS2 as monthly aggregates,
then (a) the bulletin's coverage is far better than I assumed and the sampling-bias warning in
2.4.1 becomes conditional rather than certain, and (b) the argument against B shifts, B fails
not on *absence* but on *granularity and freshness*, since monthly aggregates cannot drive
real-time facility status regardless of how many facilities send them.

## 1.4 Patterns I would hunt

- **Re-keying points.** Every place a human retypes data between systems. Latency source, defect
  source, and automation candidate simultaneously. Count and time them.
- **Shadow spreadsheets.** Every emailed Excel file is a system failing someone. The brief already
  names one (immunisation).
- **The reconciliation tell.** No answer to "what happens when sources disagree" means nobody is
  checking, that is the mess.
- **Decision latency vs. data latency.** *Decisive for B.* If districts decide monthly or
  quarterly, 3-week-old data is not the binding constraint.
- **The denominator problem.** Do current catchment populations exist? Every *rate* depends on
  them, and a wrong denominator is invisible.
- **Accountability mapping.** Data quality improves only where someone is measured on it.
- **Definition drift.** Do "ANC visit" and "complication" mean the same thing in HealthTrack,
  OpenMRS and DHIS2? If not, the bulletin aggregates incomparable things.
- **Who loses from automation.** The analyst's 40 hours are someone's job content. Champion or
  blocker? This determines whether A's political theory holds at all.

## 1.5 What I would observe directly, not take on report

1. **Sit through a bulletin build with a stopwatch**, screen-recorded with permission. The critical
   measurement is the **mechanical : judgement ratio**, it sets the automation ceiling.
2. **Open the actual DHIS2 export.** Completeness per district, missing org units, duplicate
   submissions, how late the late ones are, and **when in the cycle the data actually lands**.
3. **Attempt to reproduce last quarter's published figures from source.** If I cannot, the correct
   conclusion is *"this is not independently reproducible from the materials supplied"*, not
   "nobody can." The analyst may hold undocumented exclusions and corrections, and finding those
   is the point.
4. **Watch month-end at a paper-only facility**, the register, the transcription, the person, the
   light. This is also how 1.3 gets answered.
5. **Watch a district officer make a real decision.** Not describe one.
6. **Measure the infrastructure claim.** "4–6 hrs/day power, spotty 3G" is inherited from the
   brief. Verify where it matters.

## 1.6 What would change my mind

| Observation | Falsifies | Response |
|---|---|---|
| Districts decide **weekly** and cannot today | The case against B | Re-scope toward B for facilities with adequate granularity, honestly named as partial |
| The 40 hrs is mostly **judgement** | The ROI case for A | Automate assembly only; reset the number publicly |
| The bulletin is **not read** by any decision-maker | A's value entirely | Stop. Find what *is* read |
| Co-infected patients harmed **today at measurable volume** | The deferral of C | Escalate as clinical safety, resource properly |
| Hosting/InfoSec approval takes **> 3 weeks** | The whole sprint shape | Re-plan around an offline deliverable; escalate on Day 3 |

---

# Section 2, Problem Selection

## 2.1 A, B and C are solutions, not problems

The brief states three *things to build*. Mapping each back to the need it serves surfaces siblings
the brief omits, and one need it misses entirely. The statements below are my hypotheses phrased in
stakeholder language, not interview evidence: they are what I would try to falsify in Week 1, not
things anyone has said.

**Root outcome: MoH leadership acts on health-system data it can defend, early enough to change the
next planning cycle.**

| Need | Whose | The brief's answer | Siblings worth pricing |
|---|---|---|---|
| **O1** "I spend most of a working month on a document that is stale before it is read, and I cannot defend its numbers." | MoH analyst | **A**, automate the bulletin end to end | Shorten the cadence, quarterly → monthly; retire the PDF for a live page |
| **O2** "By the time I see a stockout it is a crisis, never a warning." | District Health Officer | **B**, real-time facility dashboard | SMS exception reporting from facilities; supply-chain-only feed (eLMIS), no clinical |
| **O3** "Co-infected patients are counted twice and treated once." | TB + HIV programme managers | **C**, unified patient view across CommCare | **Weekly reconciliation report, no merging**; shared patient identifier (policy, not software) |
| **O4** "I cannot defend the numbers I am shown, so I do not act on them." | MoH Director | **none, not in the brief** | Every figure traceable to its DHIS2 value + snapshot; completeness published beside every indicator; a past quarter reproduced from source as a trust proof |

**Two things the A/B/C framing hides.** O4 may be the Director's actual complaint, and none of A, B
or C answers it, because all three answer throughput. Whatever ships should therefore carry
traceability and published completeness as requirements rather than features. Separately, the weekly
reconciliation report is a cheaper answer to O3 than C: most of the value, none of the merge risk,
and the brief does not consider it. Both are hypotheses to test in Week 1, not findings.

## 2.2 The choice: **Problem A**, plus one bounded handover act

> **Commitment (conditional on the Week 1 gate in 2.5a):** automate the Quarterly Health
> Bulletin, with figure-level lineage carried in the data from the start, and one named Digital Health
> Officer independently producing a bulletin from a replayed quarter before I leave.

**What I am giving up, stated first.** The highest-value outcome for this Ministry is probably
operational, closer to O2 than O1. A does not deliver that. I am choosing the reachable wedge over
the valuable-but-unreachable one, and the honest framing to the Director is *"this is the thing I
can finish and prove in six weeks; here is what it does not do."* Selling A as though it serves the
operational need would be the failure mode.

**Why A.** It is the only option that can finish and be proven inside six weeks, operating on data
that already arrives in a shape that already exists. It is the only one with a baseline that
plausibly already exists, subject to **A3**, which must be measured rather than assumed. And it is
the trust wedge: a defensible artifact delivered to the analyst and the Director buys the standing
to attempt B, and in a first-country, template-setting engagement, proof is the currency.

**Why not B, why not C.** B is out of reach *in this sprint*, not impossible: it needs
facility-level freshness, and the reporting substrate is monthly aggregates on a 2–3 week lag. That
is a granularity and cadence gap rather than a coverage gap (1.3), and closing it is a separate
project. C matches records across CommCare silos with no shared patient
identifier, so matching is probabilistic in both directions. A wrong match puts one patient's HIV
status into another's treatment decision, which matters concretely: rifampicin, first-line for TB,
collapses the plasma levels of several antiretrovirals, so co-infection status drives the regimen.
A missed match loses the co-infection entirely. A unified *view* does not itself prescribe
treatment, so the risk turns on whether the match is advisory or authoritative, and settling that
needs a named clinical reviewer and a Ministry sign-off route that do not exist here and cannot be
created in six weeks. The weekly reconciliation report is the version of C I would propose: it
flags a likely co-infection for a person to check and merges nothing, so the system makes no
clinical claim.

**What A does not give B**, since the sequencing pitch is where this gets oversold. A builds an
aggregate, period-grain mart on bulletin cadence; B needs facility-status freshness, stock and
supply events, intra-period updates, alert state and freshness monitoring. What genuinely transfers
is the **org-unit dimension and the indicator dictionary**: real, reusable, and far less than a
foundation. Two further claims I will not make: that anything here is greenfield-free, since Superset,
dbt and Airflow appearing in Sand's job postings evidences the component types, not a working
Rwanda-configured instance (gate **G4**); and that the bulletin is necessarily templatable, since a
government quarterly is typically narrative + tables + interpretation rather than a dashboard export,
and **A5** resolves whether I am automating the Ministry's artifact or quietly redefining it.

**The internal disagreement I would surface, not hide.** The Solutions Manager pre-identified the
use cases before discovery, and his hypothesis points at B. Discovery points at A. I would put the
sequencing in writing to him and the Director in Week 1, including the honest version of what A does
and does not give B. An FDE who lets a pre-sold narrative survive contradicting evidence has chosen
internal comfort over the client.

## 2.3 The measurable outcome

Measured from **data availability**, not from quarter close. DHIS2 runs 2–3 weeks behind and nothing
in A makes inputs arrive faster; generating a document faster does not make its data appear, and
publishing fast on incomplete data would *reduce* trust, which is the opposite of the goal.

| Measure | Baseline | Target |
|---|---|---|
| Analyst time per publication cycle | **To be measured in Week 1** (see below) | ≥ 90% reduction |
| **Data-availability cutoff → published** | ~1–2 weeks after data lands | **≤ 2 working days** |
| Published figures resolving to a DHIS2 value + snapshot | 0% | 100% |
| Facilities with reporting status shown | not shown | 100%, by the six states in 1.3 |
| Ministry can produce a bulletin unaided (replay test) | no | yes |

**On the baseline number.** The brief says *"40 hours/month"* for a *quarterly* bulletin. Those are
inconsistent by roughly 3×: it could mean 40 hrs every month on reporting generally, 40 hrs in the
publication month, or ~120 hrs per quarterly cycle. **I commit to a 90% reduction, not to a number,
until the stopwatch resolves it in Week 1.** Committing "40 hours → 30 minutes" before measuring is
how a credibility problem gets manufactured in Week 2.

**On lineage.** Traceability is to *the DHIS2 data value, org unit, period, version and extraction
snapshot*, not to the underlying facility register or patient record. For paper-sourced aggregates,
record-level provenance does not exist to trace to.

**One adoption measure, because hours saved is production efficiency, not health value:** is the
bulletin reviewed before a named decision meeting, and does any exception in it generate an assigned
action? If A meets every engineering metric and this stays "no," A has not worked.

## 2.4 Explicitly out of scope

- **HealthTrack EMR integration** (45 hospitals, buggy, local servers). Its own project.
- **Problem C in any form**, including the reconciliation report: proposed, not built.
- **Real-time anything.** That is B.
- **Correcting source data.** We surface completeness; we do not fix DHIS2's contents.
- **Patient-level data.** Aggregate only.
- **Redefining any indicator.** A Ministry decision, and the classic scope-creep vector on
  reporting projects.
- **New hardware, new mobile apps, new user accounts** outside the existing bulletin workflow.

**Two things that look out of scope and are not**, because unresolved they consume the sprint.
**Hosting, service accounts and InfoSec approval:** where the pipeline runs for MoH Rwanda, who
holds credentials after Week 6, and whether national health data may sit in a Sand-hosted
environment. Day 1 question, Day 3 escalation. **Small-cell suppression:** "aggregate-only,
therefore no PHI" is too categorical, since rare events at facility level combined with geography
can re-identify. A suppression rule is required before publication, and access control, audit
logging and retention remain in scope regardless.

### 2.4.1 The 175 paper facilities

Out of scope for six weeks, and the largest thing this bulletin will not see. How many of the 175
already reach DHIS2 as monthly aggregates via district clerks is unestablished (1.3), so the size
of the gap is unknown, and whatever it turns out to be, the bulletin should print it: paper-only
facilities are plausibly smaller and more rural, which is where maternal and neonatal mortality is
likely highest, so a "top 10 facilities by volume" computed over reporting facilities only would
systematically describe the better-resourced end of the system. *I am asserting that, not evidencing
it; it is checkable against the provided facility data and should be checked.* Closing the gap is a
measurement programme rather than a pipeline, and the experiment that decides it is cheap: ~50 real
register photographs, extraction run, field-by-field accuracy against manual transcription. Costed
in the repository, not here.

## 2.5 Assumptions and Week 2 validation

| # | Assumption | Validation | If false |
|---|---|---|---|
| **A3** |The reporting labour is mostly *mechanical* |**Stopwatch**, Week 1 |Automate assembly only; reset the target publicly |
| **A4** |DHIS2 API access granted to a service account |Ask Day 1, escalate Day 3 |CSV export drop, same mart, same output |
| **A5** |The bulletin is reproducible as a templated artifact |Inspect last 2 editions, Day 2 |Generate tables/charts only; narrative stays manual and is named as such |
| **A6** |≥2 machine-readable historical editions exist |Request Week 1 |Ship without trends in v1 |
| **A7** |A **named** DHO with cleared hours exists |**Written ask, Week 1 Day 2** |Downgrade honestly; stop calling it capacity transfer |
| **A8** |The bulletin is read by someone who decides |Ask Director + 2 district officers what they did with the last one |Stop and re-scope |
| **A9** |Indicator definitions are consistent across sources |Sample-compare across 3 facilities |Scope to consistent indicators, flag the rest |
| **A10** |Hosting and InfoSec approval achievable in ≤ 3 weeks |Meet MoH ICT Day 4 |Re-plan around an artifact that runs on Ministry-owned infrastructure |
| **A11** |A quarter close or a replayable prior quarter falls inside the sprint |Check the reporting calendar Day 1 |Use the replay protocol in 2.6 |

### 2.5a The Week 1 gate

Committing at the end of Week 1 while planning to resolve existential assumptions in Week 2 is
incoherent: **A8** alone can invalidate the whole commitment. The commitment in 2.2 is therefore
**conditional on five gates**, assessed at end of Week 1.

| Gate | Passes if |
|---|---|
| **G1, Value** | At least one named decision-maker used the last bulletin for something identifiable |
| **G2, Mechanisability** | ≥ 60% of measured cycle time is mechanical assembly |
| **G3, Inputs** | DHIS2 access (API or scheduled export) confirmed, with a stated availability cutoff |
| **G4, Runtime** | A viable place to run and hand over the pipeline is identified and approvable |
| **G5, Operator** | A named person is assigned to receive it |

**G1 or G3 fails → A is the wrong commitment**, and I say so in Week 1 rather than Week 5.
**G2 fails → the outcome is re-stated smaller** before anything is promised.
**G4 or G5 fails → build proceeds, handover claim is dropped**, honestly and in writing.

## 2.6 Success metric

**Primary:** percentage reduction in analyst time per cycle, target ≥ 90%, against a Week-1 measured
baseline. **Secondary:** data-availability → publication, ≤ 2 working days; figures resolving to a
DHIS2 value + snapshot, 100%. **The one that matters:** *can the Ministry produce it without me?*

Because a Q[N+1] edition may not fall inside a six-week window (**A11**), that is tested by
**controlled replay** in Week 6 rather than left to luck. The named DHO, unaided, triggers the
pipeline for a prior quarter, diagnoses a **seeded** failure (a deliberately broken credential or a
malformed export), reviews the completeness exceptions, generates the bulletin, routes it for the
normal approval step, and publishes it. The seeded failure and the approval step are the two that
usually get skipped, and they are the two that actually predict survival.

**The Week 3 demo** is not a dashboard tour. It is: *"here is last quarter's published bulletin,
here is the pipeline re-deriving it from source, here are the figures that match, and here is the
one that doesn't, and why."* A reconciliation that surfaces a genuine discrepancy is a far stronger
trust event than one that finds none.

**Ownership after exit** needs naming, not just a person: who owns pipeline operations, indicator
definitions, source corrections, late submissions, bulletin approval, and infrastructure incidents.
Without that, every anomaly routes back to Sand, or the bulletin stalls between generation and
approval.

## 2.7 Fallback plan

Each assumption in 2.5 has a stated failure branch, and none ends the engagement. A blocked DHIS2 API
(**A4**) becomes a scheduled CSV export into the same mart, costing ingest automation and nothing
else. A bulletin that is not templatable (**A5**) means automating tables and charts while the
narrative stays manual and labelled. Contested definitions (**A9**) ship the uncontested sections and
annex the rest against a named Ministry decision; sparse history (**A6**) ships the current quarter
with a completeness report. No named DHO (**A7**) ships the artifact correctly labelled with the
capacity-transfer claim dropped; blocked hosting (**A10**) delivers mart, queries and runbook on
Ministry infrastructure with no Sand dependency; labour that proves mostly judgement (**A3**) resets
the target publicly in Week 2, a smaller true claim instead of a larger false one.

**The floor, if everything slips:** a conformed mart, a documented query set and a runbook. Even at
worst that removes the re-keying step, is handoverable, and starts the next engagement from a
warehouse rather than zero. The branch-by-branch table is in the repository.
