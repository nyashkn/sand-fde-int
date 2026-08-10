# Deliverable 1, Problem Decomposition and Scoping

**Role:** Forward Deployed Engineer · **Country:** Rwanda · **Sprint:** 6 weeks, 2 FDEs
**Sponsor:** MoH Director · **Internal:** Solutions Manager, Country Director, Operations Specialist

> **Revision note.** This is v2. The problem selection survived an adversarial review by three
> independent model families (GPT-5.6-sol, Gemini 3.1 Pro, Grok 4.5), all three independently
> chose Problem A. The *justification* did not survive: they found four errors unanimously and
> around a dozen more between them. Every one is corrected below, and the corrections are logged
> in [`../decisions/0007-cross-provider-redteam-amendments.md`](../decisions/0007-cross-provider-redteam-amendments.md).
> Raw reviews: [`../decisions/redteam-d1-cross-provider/`](../decisions/redteam-d1-cross-provider/).

---

## How to read this

Section 1 is what I would do in Week 1 before proposing anything. Section 2 is the commitment I
would make **at the Week 1 gate**, conditional on the gate passing. Everything is written to be
falsifiable.

Assumptions are flagged **[A#]** and collected in §2.5.

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
| **2–3** | DHIS2 / HMIS focal point | *Where does the 2–3 week delay actually accrue?* And critically: **how do the paper facilities report today?** (see §1.3) |
| **3** | 2 district health officers, one strong district, one weak | *"What did you look at immediately before your last resource decision?"* If the answer isn't data, B solves the wrong problem |
| **3–4** | 1 HealthTrack hospital, 1 OpenMRS clinic, 1 paper-only facility, the **data clerk**, not the medical director | Watch month-end reporting happen |
| **4** | TB and HIV programme managers | Size C honestly: how many co-infected, how identified today, what happens when one is missed |
| **4** | **MoH ICT / InfoSec** | Hosting, data residency, service accounts, approval lead times. See §2.4, this is the classic six-week killer |
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
§2.4.1 becomes conditional rather than certain, and (b) the argument against B shifts, B fails
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
   light. This is also how §1.3 gets answered.
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

The brief states three *things to build*. Mapping them back to needs surfaces siblings the brief
omits, and one opportunity it misses entirely.

**The quoted statements below are my hypotheses phrased in stakeholder language, not interview
evidence.** They are what I would go and try to falsify in Week 1, not things anyone has said.

```
OUTCOME, MoH leadership acts on health-system data it can defend,
          early enough to change the next planning cycle
│
├─ O1  the MoH analyst  [hypothesis]
│  "I spend most of a working month on a document that is stale before
│   it is read, and I cannot defend its numbers."
│  ├─ S-A1  Automate the bulletin end to end        ← PROBLEM A
│  ├─ S-A2  Shorten the cadence (quarterly → monthly)
│  └─ S-A3  Retire the PDF for a live page
│
├─ O2  the District Health Officer  [hypothesis]
│  "By the time I see a stockout it is a crisis, never a warning."
│  ├─ S-B1  Real-time facility status dashboard     ← PROBLEM B
│  ├─ S-B2  SMS exception reporting from facilities
│  └─ S-B3  Supply-chain-only feed (eLMIS), no clinical
│
├─ O3  TB + HIV programme managers  [hypothesis]
│  "Co-infected patients are counted twice and treated once."
│  ├─ S-C1  Unified patient view across CommCare    ← PROBLEM C
│  ├─ S-C2  Weekly reconciliation report, no merging
│  └─ S-C3  Shared patient identifier (policy, not software)
│
└─ O4  the MoH Director  [hypothesis, NOT IN THE BRIEF]
   "I cannot defend the numbers I am shown, so I do not act on them."
   ├─ S-D1  Every figure traceable to its DHIS2 value + snapshot
   ├─ S-D2  Publish completeness beside every indicator
   └─ S-D3  Reproduce a past quarter from source as a trust proof
```

**Note the root outcome changed in this revision, and why it matters.** My first draft wrote
*"acts on data within the period it describes."* That root **selects for B**, no quarterly
retrospective artifact can support in-period action, and I then chose A anyway. That was a
reverse-fit: picking the shippable wedge and retrofitting an outcome it cannot serve. The root
above is what A can honestly serve. The gap between the two is real and is stated in §2.2.

**Two things the A/B/C framing hides:**

**O4 may be the Director's actual complaint**, and if it is, none of A, B or C answers it
directly, because all three answer throughput. Whatever ships should therefore carry S-D1 and S-D2
as requirements. This is a hypothesis to test in Week 1, not a finding.

**S-C2 is a cheaper answer to O3 than C.** A weekly reconciliation report flags likely co-infected
patients for human review without merging records. Most of the value, none of the merge risk. The
brief does not consider it. Worth putting to the programme managers regardless.

## 2.2 The choice: **Problem A**, plus one bounded handover act

> **Commitment (conditional on the Week 1 gate in §2.5a):** automate the Quarterly Health
> Bulletin, with figure-level lineage built in from the start, and one named Digital Health
> Officer independently producing a bulletin from a replayed quarter before I leave.

**What I am giving up, stated first.** The highest-value outcome for this Ministry is probably
operational, closer to O2 than O1. A does not deliver that. I am choosing the reachable wedge
over the valuable-but-unreachable one, and the honest framing to the Director is *"this is the
thing I can finish and prove in six weeks; here is what it does not do."* Selling A as though it
serves the operational need would be the failure mode.

Three arguments for A:

**1, It is the only option that can finish and be proven inside six weeks.** C is disqualified on
clinical-safety grounds. B requires facility-level freshness that monthly aggregate reporting
cannot supply, regardless of how many facilities report (§1.3). A operates on data that already
arrives, in a shape that already exists.

**2, It is the only option with a baseline that plausibly already exists.** Subject to §2.5 A3 , 
the baseline must be measured, not assumed. B and C would need one built first.

**3, It is the trust wedge.** Delivering a defensible artifact to the analyst and the Director
buys the standing to attempt B. In a first-country, template-setting engagement, proof is the
currency.

**An argument I withdraw.** My first draft claimed *"A's mart is most of B's data layer."* Three
independent reviewers rejected this and they are right. A builds an **aggregate, period-grain**
mart refreshed on bulletin cadence. B needs facility-status freshness, stock/supply event data,
intra-period updates, alert state and freshness monitoring. What genuinely transfers is the
**org-unit dimension and the indicator dictionary**, real, reusable, and far less than "most."
I was narrating a reporting mart as B's foundation because that resolves the internal conflict with
the Solutions Manager, not because the architecture says so. The honest sequencing pitch is
*"A gives us the org-unit hierarchy, the indicator dictionary, and a working relationship, B is
still most of a project."*

**On "nothing greenfield."** I over-claimed. Superset, dbt and Airflow appear in Sand's own FDE job
postings; my research file grades that as *strong* evidence, not *confirmed*. It is not evidence
that a Rwanda MoH DHIS2 connector, a conformed mart, an approved Superset instance, service
accounts or a bulletin-grade template exist and work today. The correct claim is: **the component
types are in Sand's stack and staffed for; whether an instance exists for Rwanda MoH is a Week 1
question, not an assumption.** See gate G4.

**One category risk to name.** A government quarterly bulletin is typically narrative + tables +
interpretation, not a dashboard export. If it turns out the Ministry's product cannot be a Superset
scheduled report, then either the architecture claim is wrong or I have silently redefined the
Ministry's artifact. §2.5 A5 resolves this; I will not redefine the bulletin without saying so.

### Why not B

Not because it is unimportant, it is closest to the Solutions Manager's pre-commitment and closest
to the maternal/neonatal priority. Because B needs **facility-level freshness**, and the reporting
substrate is monthly aggregates on a 2–3 week lag. That is a granularity and cadence gap, not
merely a coverage gap, and closing it is a separate project. B is out of reach *in this sprint* , 
not impossible.

### Why not C

Probabilistic identity matching across CommCare silos with no shared identifier, in six weeks, with
no MoH clinical-safety review process. I will not overstate the causal chain: a unified *view* does
not itself prescribe treatment, and the real risk depends on whether matching is advisory or
authoritative and what review controls exist. But that is precisely the point, **C requires a
hazard analysis I cannot complete in six weeks**, and shipping identity matching without one is the
wrong first engagement. **S-C2 is the version of C I would propose.**

### The internal disagreement I would surface, not hide

The Solutions Manager pre-identified the use cases before discovery, and his hypothesis points at
B. Discovery points at A. I would put the sequencing in writing to him and the Director in Week 1 , 
including the honest version of what A does and does not give B. An FDE who lets a pre-sold
narrative survive contradicting evidence has chosen internal comfort over the client.

## 2.3 The measurable outcome

The first draft committed to *"published within 5 working days of quarter close."* **That is
impossible by construction** and all three reviewers caught it: DHIS2 runs 2–3 weeks behind, and
nothing in A makes inputs arrive faster. Generating a document faster does not make its data
appear. Worse, publishing fast on incomplete data would *reduce* trust, the opposite of the goal.

The metric is therefore measured from **data availability**, not from quarter close:

| Measure | Baseline | Target |
|---|---|---|
| Analyst time per publication cycle | **To be measured in Week 1** (see below) | ≥ 90% reduction |
| **Data-availability cutoff → published** | ~1–2 weeks after data lands | **≤ 2 working days** |
| Published figures resolving to a DHIS2 value + snapshot | 0% | 100% |
| Facilities with reporting status shown | not shown | 100%, by the six states in §1.3 |
| Ministry can produce a bulletin unaided (replay test) | no | yes |

**On the baseline number.** The brief says *"40 hours/month"* for a *quarterly* bulletin. Those are
inconsistent by roughly 3× and I propagated the ambiguity. It could mean 40 hrs every month on
reporting generally, 40 hrs in the publication month, or ~120 hrs per quarterly cycle. **I commit
to a 90% reduction, not to a number, until the stopwatch resolves it in Week 1.** Committing "40
hours → 30 minutes" before measuring is how a credibility problem gets manufactured in Week 2.

**On lineage.** The honest claim is traceability to *the DHIS2 data value, org unit, period,
version and extraction snapshot*, not to the underlying facility register or patient record. For
paper-sourced aggregates, record-level provenance does not exist to trace to.

**One adoption measure, because hours saved is production efficiency, not health value:** is the
bulletin reviewed before a named decision meeting, and does any exception in it generate an
assigned action? If A meets every engineering metric and this stays "no," A has not worked.

## 2.4 Explicitly out of scope

- **HealthTrack EMR integration** (45 hospitals, buggy, local servers). Its own project.
- **Problem C in any form**, including S-C2, proposed, not built.
- **Real-time anything.** That is B.
- **Correcting source data.** We surface completeness; we do not fix DHIS2's contents.
- **Patient-level data.** Aggregate only.
- **Redefining any indicator.** Definition changes are a Ministry decision. This is the classic
  scope-creep vector on reporting projects.
- **New hardware, new mobile apps, new user accounts** outside the existing bulletin workflow.

**Two things I previously put out of scope that are actually in scope**, because all three
reviewers flagged them as sprint-killers:

- **Hosting, service accounts and InfoSec approval.** Where dbt/Airflow/Superset run for MoH
  Rwanda, who holds credentials after Week 6, and whether national health data may sit in a
  Sand-hosted environment. Unresolved, this consumes the sprint. Day 1 question, Day 3 escalation.
- **Small-cell suppression.** "Aggregate-only, therefore no PHI" was too categorical. Rare events
  at facility level, combined with geography, can re-identify. A suppression rule is required
  before publication, and access control, audit logging and retention remain in scope regardless.

### 2.4.1 The 175 paper facilities, coverage gap, honestly bounded

Out of scope for six weeks. Three things about it, deliberately shorter than the first draft:

**First, establish the facts (§1.3).** How many of the 175 already reach DHIS2 as monthly
aggregates via district clerks? Until that is known, the size of the gap is unknown.

**Second, whatever the gap is, print it.** Paper-only facilities are plausibly smaller and more
rural, and if so, that is where maternal and neonatal mortality is likely highest. *I am asserting
this, not evidencing it; it is checkable against the provided facility data and should be checked.*
If it holds, a "top 10 facilities by volume" table computed over reporting facilities only
systematically describes the better-resourced end of the system, and publishing that uncaveated
would be actively misleading.

**Third, engagement 2 is a measurement, not a pipeline.** A VLM-assisted capture path (photograph
the register, extract, human confirms, submit with the photo attached as provenance) is a plausible
unlock, and it is a research programme, not a sketch I should be costing here. The only thing I
would commit to is the cheap experiment that decides it: **~50 real register photographs, extraction
run, field-by-field accuracy against manual transcription, failure modes reported.** That number
either justifies the project or kills it honestly.

Two objections to record now rather than discover later: if the officer must confirm every digit on
screen, that may be *slower* than typing aggregates into a simple form, so the design has to earn
its complexity against that baseline. And a photograph of a register may capture names and
diagnoses, which reintroduces the PHI exposure this sprint avoids.

## 2.5 Assumptions and Week 2 validation

| # | Assumption | Why it matters | Validation | If false |
|---|---|---|---|---|
| **A3** | The reporting labour is mostly *mechanical* | The automation ceiling and the headline number | **Stopwatch**, Week 1 | Automate assembly only; reset the target publicly |
| **A4** | DHIS2 API access granted to a service account | Ingest architecture | Ask Day 1, escalate Day 3 | CSV export drop, same mart, same output |
| **A5** | The bulletin is reproducible as a templated artifact | Whether Superset can be the output at all | Inspect last 2 editions, Day 2 | Generate tables/charts only; narrative stays manual and is named as such |
| **A6** | ≥2 machine-readable historical editions exist | Trends *and* the validation demo | Request Week 1 | Ship without trends in v1 |
| **A7** | A **named** DHO with cleared hours exists | The handover act has no subject otherwise | **Written ask, Week 1 Day 2** | Downgrade honestly; stop calling it capacity transfer |
| **A8** | The bulletin is read by someone who decides | A's entire value | Ask Director + 2 district officers what they did with the last one | Stop and re-scope |
| **A9** | Indicator definitions are consistent across sources | Whether aggregates are comparable | Sample-compare across 3 facilities | Scope to consistent indicators, flag the rest |
| **A10** | Hosting and InfoSec approval achievable in ≤ 3 weeks | Whether anything can be deployed | Meet MoH ICT Day 4 | Re-plan around an artifact that runs on Ministry-owned infrastructure |
| **A11** | A quarter close or a replayable prior quarter falls inside the sprint | Whether the success criteria are observable at all | Check the reporting calendar Day 1 | Use the replay protocol in §2.6 |

### 2.5a The Week 1 gate

The first draft committed at the end of Week 1 while planning to resolve existential assumptions in
Week 2. That is incoherent, A8 alone can invalidate the whole commitment. So the commitment in
§2.2 is **conditional on five gates**, assessed at end of Week 1:

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

**Primary:** percentage reduction in analyst time per cycle (target ≥ 90%), against a Week-1
measured baseline.

**Secondary:** data-availability → publication (≤ 2 working days); figures resolving to a DHIS2
value + snapshot (100%).

**The one that matters:** *can the Ministry produce it without me?*

Because a Q[N+1] edition may not fall inside a six-week window (**A11**), this is tested by
**controlled replay** in Week 6 rather than left to luck. The named DHO, unaided, must:

1. trigger the pipeline for a prior quarter
2. diagnose a **seeded** failure (a deliberately broken credential or a malformed export)
3. review the completeness exceptions
4. generate the bulletin
5. route it for the normal approval step
6. publish it

Steps 2 and 5 are the ones that usually get skipped and are the ones that actually predict survival.

**The Week 3 demo** is not a dashboard tour. It is: *"here is last quarter's published bulletin,
here is the pipeline re-deriving it from source, here are the figures that match, and here is the
one that doesn't, and why."* A reconciliation that surfaces a genuine discrepancy is a far stronger
trust event than one that finds none.

**Ownership after exit** needs naming, not just a person: who owns pipeline operations, indicator
definitions, source corrections, late submissions, bulletin approval, and infrastructure incidents.
Without that, every anomaly routes back to Sand or the bulletin stalls between generation and
approval.

## 2.7 Fallback plan

| If | Then | What survives |
|---|---|---|
| DHIS2 API blocked (**A4**) | Scheduled CSV export drop into the same mart | Everything except ingest automation |
| Bulletin not templatable (**A5**) | Automate tables/charts; narrative stays manual, labelled | The mechanical majority, honestly scoped |
| Definitions contested (**A9**) | Ship uncontested sections; rest as annex | Most of the bulletin + a named Ministry decision |
| History too sparse (**A6**) | Current quarter + completeness report | The completeness report is itself the argument for fixing reporting |
| No named DHO (**A7**) | Bulletin-only; walk-through with the IT contact | The artifact, correctly labelled |
| Hosting blocked (**A10**) | Deliver mart + queries + runbook on Ministry infrastructure | A handoverable asset with no Sand dependency |
| Labour mostly judgement (**A3**) | Reset the target publicly in Week 2 | A smaller true claim instead of a larger false one |
| Everything slips | **Floor:** conformed mart + documented query set + runbook | Removes the re-keying step and is handoverable |

The floor is chosen deliberately: even at worst, the mart exists and the next engagement starts
from a warehouse rather than from zero.

---

## Appendix, how this scoping was produced, and where it was wrong

The problem selection was reviewed twice. First by a six-persona adversarial council, which was
**single-provider**, and therefore could not distinguish "A is correct" from "one model's priors
sampled six ways." That limitation was recorded rather than hidden, and it is why the second review
happened.

Second, by **three independent model families** (GPT-5.6-sol, Gemini 3.1 Pro, Grok 4.5), prompted
hostilely against this document.

**Result: all three independently chose Problem A.** The convergence is therefore probably not a
single-family artifact, A is the unique option that is clinically non-catastrophic, partially
instrumented, and finishable.

**But all three rejected the justification**, and four errors were unanimous:

1. The 5-day-from-quarter-close target was impossible given a 2–3 week upstream lag
2. "A's mart is most of B's data layer" was false
3. "40 hrs/month" vs "40 hrs/cycle" inflated the ROI ~3×
4. "Nothing greenfield" converted job-posting copy into an existence proof

Plus, from single reviewers but equally real: paper-only ≠ non-reporting (the domain error in
§1.3); the root outcome statement selected for B while I chose A; hypotheses were presented as
stakeholder quotations; hosting and InfoSec were omitted entirely; "aggregate-only therefore no
PHI" was too categorical; success criteria depended on a quarter boundary falling inside the sprint
by luck; and "if I cannot reproduce it, nobody can" was invalid reasoning.

All are corrected above. The lesson worth carrying into the engagement is Grok's: *the blind spot
was justification quality, not the letter A.* A confident, thorough, internally-consistent document
can still be wrong in ways only an outside reader sees, which is the same reason §2.5a exists as a
gate rather than a formality.

- Cross-provider reviews: [`../decisions/redteam-d1-cross-provider/`](../decisions/redteam-d1-cross-provider/)
- Amendment log: [`../decisions/0007-cross-provider-redteam-amendments.md`](../decisions/0007-cross-provider-redteam-amendments.md)
- Council record: [`../decisions/council-d1-problem-selection/`](../decisions/council-d1-problem-selection/) · [`0006`](../decisions/0006-problem-a-plus-handover-act.md)
- Visual artifact: [`../artifacts/03-opportunity-map-council-verdict.html`](../artifacts/03-opportunity-map-council-verdict.html)
