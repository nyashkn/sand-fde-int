# Deliverable 1 — Problem Decomposition and Scoping

**Role:** Forward Deployed Engineer · **Country:** Rwanda · **Sprint:** 6 weeks, 2 FDEs
**Sponsor:** MoH Director · **Internal:** Solutions Manager, Country Director, Operations Specialist

---

## How to read this

Section 1 is what I would do in Week 1 before proposing anything. Section 2 is the commitment
I would make at the end of it. Everything is written to be falsifiable — where I could be wrong,
I say what observation would prove it and what I would do instead.

Assumptions are flagged inline as **[A#]** and collected in §2.5. The evidence base behind the
Sand-product claims is in [`../research/sand-product-research.md`](../research/sand-product-research.md);
the adversarial review of the problem selection is in
[`../artifacts/03-opportunity-map-council-verdict.html`](../artifacts/03-opportunity-map-council-verdict.html).

**[A1]** The country is Rwanda. The brief says "one of our expansion countries (i.e. Rwanda)" and
the provided data uses Rwandan facility names, districts and RWF.
**[A2]** I have no access to a live Sand or MoH environment. Everything below is built against the
provided data and public sources.

---

# Section 1 — Discovery Process

## 1.1 "Our data is a mess" is a symptom report, not a problem statement

The Director's sentence contains at least three distinct failure classes, and they imply
completely different projects:

| Failure class | What it means | What it would imply |
|---|---|---|
| **Absence** | The data was never captured | Digitisation problem. 175 of ~250 facilities are paper-only. |
| **Latency** | Captured, but arrives too late to act on | Pipeline problem. DHIS2 runs 2–3 weeks behind. |
| **Distrust** | Arrives on time, but nobody believes it | Provenance problem. Two sources disagree and nobody reconciles. |
| **Last mile** | Believed, but never reaches a decision | Workflow problem. The bulletin is read after the decision is made. |

Week 1's job is to find which dominates. My prior going in — to be tested, not assumed — is that
the Director is describing **distrust**, because "we cannot make good decisions" is a statement
about confidence, not about throughput. A dashboard fixes latency. It does not fix distrust.

## 1.2 Who I would talk to, and in what order

Sequence matters: each conversation is priced by what the previous one unlocked.

| Day | Who | The question that actually matters |
|---|---|---|
| **1** | Solutions Manager, Country Director | *Why were the use cases chosen before discovery?* What does the MoU actually commit us to, and what has already been promised to whom? |
| **1–2** | **MoH Director** (sponsor) | *"Tell me about a decision last quarter you'd have made differently with better data."* Then: *"When the numbers you're shown disagree with what you believe, which do you act on?"* |
| **2** | **The bulletin analyst** | The single most important interview. Not "what do you need" — *"show me last quarter's, and open the files you built it from."* |
| **2–3** | DHIS2 / HMIS focal point | *Where does the 2–3 week delay actually accrue* — facility→district, district→national, or in validation? Who can already see the data before it's published? |
| **3** | 2 district health officers — one strong district, one weak | *"What did you look at immediately before your last resource decision?"* If the answer isn't data, B is solving the wrong problem. |
| **3–4** | 1 HealthTrack hospital, 1 OpenMRS clinic, 1 paper-only facility — the **data clerk**, not the medical director | Watch month-end reporting happen. The clerk knows where the numbers come from; the director knows what they're supposed to be. |
| **4** | TB and HIV programme managers | Size C honestly: how many co-infected patients, how are they currently identified, what happens today when one is missed? |
| **5** | The other FDE, Central FDEs, Product | What reusable patterns already exist? Do not rebuild what Sand has shipped in another country. |

**Question discipline.** Every question above is **counterfactual** ("what did you do last month")
or **observational** ("show me"), never **solicitational** ("what would you like"). Solicitation
returns a feature list that reflects what the person thinks you can build, not what they need.

**One question I would ask everyone**, because the answers will not match:
> *"When two systems give different numbers for the same thing, what happens?"*

If there is a clear answer, someone is reconciling and I should find them. If there is no answer,
nobody is checking — and that, not latency, is the mess.

## 1.3 Patterns I would hunt when decomposing

Named so they are checkable, not vibes:

- **Re-keying points.** Every place a human retypes data from one system into another. Each is
  simultaneously a latency source, a defect source, and an automation candidate. Count them and
  time them.
- **Shadow spreadsheets.** Every Excel file being emailed around is a system failing someone.
  They map the real gaps better than any architecture diagram. The brief already names one
  (immunisation).
- **The reconciliation tell.** See above. Absence of a reconciliation process is the strongest
  available evidence for the distrust hypothesis.
- **Decision latency vs. data latency.** *The decisive question for Problem B.* If districts make
  resource decisions monthly or quarterly, then 3-week-old data is not the binding constraint and
  B solves a problem nobody has. If they make them weekly, B is urgent.
- **The denominator problem.** Do current catchment populations exist, and when were they last
  updated? Every *rate* in the bulletin depends on them. A wrong denominator is invisible and
  corrupts every trend.
- **Accountability mapping.** Data quality only improves where someone is measured on it. Who is
  currently accountable for reporting completeness, and what happens to them if it's low?
- **Definition drift.** Do "ANC visit" and "complication" mean the same thing in HealthTrack,
  OpenMRS and DHIS2? If not, the bulletin has been aggregating incomparable things.

## 1.4 What I would observe directly, not take on report

This is the part that separates a scoping document from a plausible one.

1. **Sit through a full bulletin build with a stopwatch**, screen-recorded with permission.
   40 hours is a claim until you have watched where it goes. The critical measurement is the
   **mechanical : judgement ratio** — if 30 of the 40 hours are analyst narrative and
   interpretation, the automation ceiling collapses and the headline number in §2.3 is wrong.
2. **Open the actual DHIS2 export.** Not a description of it. Completeness rates per district,
   missing org units, duplicate submissions, how late the late ones are.
3. **Try to reproduce last quarter's published figures from source.** If I cannot, nobody can —
   and that finding is worth more than anything I could build in week 1. It is also the single
   most persuasive demo I will have (§2.6).
4. **Watch month-end at a paper-only facility.** The actual register, the actual transcription,
   the actual person doing it, in the actual light.
5. **Watch a district officer make a real decision.** Not describe one. What did they open?
6. **Measure the infrastructure claim.** "4–6 hrs/day power, spotty 3G" is inherited from the
   brief. Verify it at the facilities that matter rather than designing around a number nobody
   sourced.

## 1.5 What would change my mind

| Observation | What it falsifies | What I'd do |
|---|---|---|
| District officers make resource decisions **weekly** and currently cannot | The core argument against B | Re-scope toward B for the ~75 digital facilities, honestly named as partial coverage |
| The 40 hours is mostly **analyst judgement**, not mechanical assembly | The ROI case for A | Automate the assembly only; reset the outcome number; consider a different problem |
| The bulletin is **not actually read** by anyone who makes decisions | A's value entirely | Stop. Find what *is* read. Automating an ignored artifact is worse than doing nothing |
| Co-infected patients are being **actively harmed today** at measurable volume | The deferral of C | Escalate C as a clinical-safety issue, not a data project, and resource it properly |

---

# Section 2 — Problem Selection

## 2.1 A, B and C are solutions, not problems

The brief states three *things to build*. Before choosing, they need mapping back to the needs
they serve — because siblings exist that the brief does not list, and one opportunity is missing
entirely.

```
OUTCOME — MoH leadership acts on data within the period it describes
│
├─ O1  the MoH analyst · 40 hrs/month
│  "40 hours a month on a document that is stale before it is read,
│   and I cannot defend its numbers."
│  ├─ S-A1  Automate the bulletin end to end        ← PROBLEM A
│  ├─ S-A2  Publish monthly instead of quarterly
│  └─ S-A3  Retire the PDF for a live page
│
├─ O2  the District Health Officer · 3-week lag
│  "By the time I see a stockout it is a crisis, never a warning."
│  ├─ S-B1  Real-time facility status dashboard     ← PROBLEM B
│  ├─ S-B2  SMS exception reporting from facilities
│  └─ S-B3  Supply-chain-only feed (eLMIS), no clinical
│
├─ O3  TB + HIV programme managers
│  "Co-infected patients are counted twice and treated once."
│  ├─ S-C1  Unified patient view across CommCare    ← PROBLEM C
│  ├─ S-C2  Weekly reconciliation report, no merging
│  └─ S-C3  Shared patient identifier (policy, not software)
│
└─ O4  the MoH Director — NOT IN THE BRIEF
   "I cannot trust any number I am shown, so I do not use them."
   ├─ S-D1  Every figure traceable to its source record
   ├─ S-D2  Publish completeness beside every indicator
   └─ S-D3  Reproduce last quarter from source as a trust proof
```

**Two things fall out of this that the A/B/C framing hides:**

**O4 is the Director's actual complaint.** She said *"we cannot make good decisions"* — a trust
statement. A, B and C all answer throughput. None answers trust directly. Whatever ships must
therefore carry S-D1 and S-D2 as **requirements**, not as polish. This is the single most
important reframing in this document.

**S-C2 is a cheaper answer to O3 than C.** A weekly reconciliation report flags likely co-infected
patients for a human to review, without merging any records. It captures much of the value with
none of the false-merge risk. The brief does not consider it. Worth putting to the programme
managers in Week 1 regardless of what I commit to.

## 2.2 The choice: **Problem A**, plus one bounded handover act

> **Commitment:** automate the Quarterly Health Bulletin, with figure-level traceability built in
> from the start, and one named Digital Health Officer running the pipeline restart themselves,
> unassisted, before I leave.

Four arguments, in order of weight:

**1 — Existence proof beats ambition.** Week 6 must produce something the Ministry *uses*, not
something 60% built. A's entire delivery path already exists inside Sand's stack: a DHIS2 pull,
a conformed org-unit × indicator × period mart, a Superset template, and Superset's built-in
scheduled report. Superset is named explicitly in Sand's own FDE job posting; dbt and Airflow are
listed alongside it. Nothing on A's path is greenfield, which is what makes six weeks credible
rather than optimistic.

**2 — It is the only option with a baseline that already exists.** 40 hrs/month is measurable
today and measurable after. B and C have no instrumented baseline; two of six weeks would go to
building one before any claim could be made.

**3 — It de-risks B rather than competing with it.** A forces the conformed facility × indicator ×
period mart into existence. That mart is most of B's data layer. Sequencing A→B means B starts
from a warehouse instead of from zero.

**4 — It is the trust purchase.** It delivers a visible win to the analyst — the person best
positioned to advocate internally — and to the Director who signed the MoU. In a first-country,
template-setting engagement, proof is the currency.

### Why not B

Not because it is unimportant — it is closest to what the Solutions Manager pre-committed to, and
closest to the maternal/neonatal mortality priority. Because **175 of ~250 facilities have no
digital capture at all.** There is no sensor, no app, no feed. B's honest scope today is
"real-time for the ~75 digital facilities," which is a materially smaller promise than the one
being asked for, and the gap is exactly where the need is greatest.

*Correction to a claim I initially made too strongly:* B is **not** permanently impossible — see
§2.4.1, where a field-capture pipeline is named as the real unlock. It is out of reach *in this
sprint*, which is a different and more honest statement.

### Why not C

Probabilistic patient-identity matching across CommCare silos with no shared identifier, in six
weeks, with no MoH clinical-safety review process to catch a bad merge. The failure mode is not a
wrong dashboard cell — it is a wrong drug regimen or a missed contraindication. That is a coroner's
inquest, not a bug ticket. Highest clinical value of the three, and the wrong first engagement.
**S-C2 (reconciliation report, no merging) is the version of C I would actually propose.**

### The internal disagreement I would surface, not hide

The Solutions Manager pre-identified the use cases *before* discovery happened, and his hypothesis
points at B. Discovery points at A. I would not quietly build A and let the B narrative stand.
I would put the sequencing in writing to both him and the Director in Week 1: **A now, B next, and
here is the specific thing that unblocks B.** An FDE who lets a pre-sold narrative survive contact
with contradicting evidence has chosen internal comfort over the client.

## 2.3 The specific, measurable outcome

> By the end of Week 6, the Q[N] Health Bulletin is generated from source data in **under 30
> minutes** of analyst time (from 40 hours), containing all four required sections, with **every
> figure traceable to the DHIS2 source record and period snapshot it came from**, published within
> **5 working days** of quarter close (from ~3 weeks) — and the Q[N+1] edition is produced by the
> Ministry **without me in the room**.

Four numbers, each independently checkable:

| Measure | Before | After |
|---|---|---|
| Analyst time per cycle | 40 hrs | < 30 min |
| Quarter close → publication | ~3 weeks | ≤ 5 working days |
| Figures traceable to source | 0% | 100% |
| Facilities with reporting status shown | not shown | 100% (including the non-reporting 175) |

The fourth row is the O4 requirement made concrete, and it is the one I would refuse to drop.

## 2.4 Explicitly out of scope

- **The 175 paper-only facilities as data sources.** They appear in the bulletin as
  *not reporting* — never as estimates, never silently omitted. See §2.4.1.
- **HealthTrack EMR integration** (45 hospitals, buggy, local servers). Its own project.
- **Problem C in any form**, including S-C2 — proposed, not built, this sprint.
- **Real-time anything.** That is B.
- **Correcting source data.** We surface completeness; we do not fix what DHIS2 contains.
- **Patient-level data of any kind.** The bulletin is aggregate-only. This also keeps the sprint
  out of PHI scope entirely, which materially simplifies the security and consent conversation.
- **Redefining any indicator.** We automate the bulletin *as currently defined*. Definition
  changes are a Ministry decision, not an FDE decision, and are the classic scope-creep vector on
  reporting projects ("while you're in there, could you also…").
- **Mobile apps, new hardware, new user accounts** for anyone outside the existing bulletin workflow.

### 2.4.1 The 175 paper facilities — named as the real unlock, not ignored

Out of scope for six weeks, but this is the structural problem and it deserves a stated path
rather than silence.

**The bias this creates must be printed in the bulletin.** Paper-only facilities are
disproportionately small and rural — which is exactly where maternal and neonatal mortality is
highest, and exactly the MoH's stated priority. A "top 10 facilities by patient volume" table
computed only over digital facilities systematically describes the better-resourced end of the
system. Publishing that without the caveat would be actively misleading, and it is the kind of
error that destroys the trust the engagement exists to build.

**The path I would propose for engagement 2** — and prototype cheaply *now* as evidence, not as a
deliverable:

```
Field officer photographs the paper register on a phone
    → on-device queue (works offline; syncs when connectivity returns)
    → VLM extracts the tally grid into structured fields
    → confidence scored per field; low-confidence fields flagged, never guessed
    → the officer CONFIRMS or CORRECTS each figure on screen
    → submitted with the officer's identity + the source photograph attached
    → the photograph travels with the number forever as its provenance
```

Three design rules that make this safe rather than dangerous:

1. **The model proposes; a human commits.** The VLM never submits a number on its own authority.
   A fabricated `47` is worse than a missing `47`, because a missing value is visibly missing and
   a fabricated one is indistinguishable from a real one.
2. **The system must be able to say "I cannot read this."** An extraction pipeline without a
   refusal path will confabulate on the degraded inputs — faded carbon copies, poor light,
   non-standard forms — which is precisely the population it exists to serve.
3. **Measure before building.** The first deliverable is not a pipeline, it is a *number*: take
   ~50 real register photographs, run extraction, compare field-by-field against manual
   transcription, and report the accuracy and the failure modes. That measurement is cheap, is
   itself valuable to the Ministry, and either justifies the project or kills it honestly.

This also closes the loop with O4: **a figure whose provenance is a photograph of the register it
came from is the most defensible number in the entire system.** The trust mechanism and the
coverage mechanism turn out to be the same mechanism.

## 2.5 Assumptions and what needs validating in Week 2

| # | Assumption | Why it matters | How I validate it | If false |
|---|---|---|---|---|
| **A3** | The 40 hrs/month is mostly *mechanical*, not analyst judgement | The entire automation ceiling and the headline outcome number | **Stopwatch, not interview.** Shadow one full cycle in Week 1–2 | Automate assembly only; reset the outcome to a defensible number; escalate early |
| **A4** | DHIS2 API access will be granted to a service account | Determines ingest architecture | Ask Day 1; escalate through the Country Director by Day 3 | Fall back to scheduled CSV export drop — same mart, same output, loses ingest automation |
| **A5** | Bulletin indicator definitions are documented and stable | Determines whether we automate or first archaeologise | Ask the analyst for the definition source on Day 2 | Budget 3 days for definition reconstruction; ship the uncontested sections first |
| **A6** | Machine-readable historical bulletins exist for ≥2 past quarters | Required for both trend analysis *and* the validation demo | Request in Week 1 | Ship without the trend section in v1; rebuild history from DHIS2 where possible |
| **A7** | A **named** DHO with cleared hours can be committed to a Week 6 session | The handover act has no subject without one | **Written ask by Week 1 Day 2** | Downgrade honestly to bulletin-only and stop calling it capacity transfer |
| **A8** | The bulletin is actually read by someone who makes decisions | A's entire value | Ask the Director and two district officers what they did with the last one | Stop and re-scope. This is the highest-severity failure in the list |
| **A9** | Indicator definitions are consistent across HealthTrack, OpenMRS and DHIS2 | Whether aggregates are comparable at all | Sample-compare the same indicator across three facilities | Scope the bulletin to consistent indicators; flag the rest as non-comparable |

**A3 and A8 are the dangerous ones.** Both are cheap to check and both can invalidate the whole
commitment. Both are checked by watching, not by asking.

## 2.6 Success metric

**Primary:** analyst hours per bulletin cycle. 40 → under 0.5.

**Secondary:** days from quarter close to publication (≈21 → ≤5); percentage of published figures
that resolve to a source record (0% → 100%).

**The one that actually matters:** *is the Q[N+1] bulletin produced without me?* Every other number
can be true while the system quietly dies after handover. This is the FDE metric, not the
engineering metric, and it is why the bounded handover act is in the commitment rather than
in a documentation appendix.

**The demo I would give in Week 3** is not a dashboard tour. It is: *"here is last quarter's
published bulletin; here is my pipeline re-deriving it from source; here are the figures that
match, and here is the one that doesn't — and here is why."* A reconciliation that finds a genuine
discrepancy is a far stronger trust event than one that finds none.

## 2.7 Fallback plan

Tiered, not binary. Every rung still leaves an artifact and still leaves the Ministry better off.

| If | Then | What survives |
|---|---|---|
| DHIS2 API access blocked (**A4**) | Scheduled CSV export drop into the same mart | Everything except ingest automation — ~80% of the win |
| Indicator definitions contested (**A5**) | Ship the 3 uncontested sections; 4th as a manual annex | Most of the bulletin, plus a named Ministry decision |
| History too sparse for trends (**A6**) | Ship current-quarter sections + a completeness report | The completeness report is itself the argument for fixing reporting |
| No named DHO (**A7**) | Bulletin-only; walk-through with whoever the IT contact is | The artifact, honestly labelled — not called capacity transfer |
| The 40 hrs is mostly judgement (**A3**) | Automate assembly; reset the target publicly in Week 2 | A smaller, true claim instead of a larger, false one |
| Everything slips | **Floor deliverable:** the conformed mart + a documented query set | Kills the re-keying step, is handoverable, and is B's foundation |

The floor deliverable is deliberately chosen: even in the worst case, the mart exists, the
re-keying is gone, and the next engagement starts from a warehouse.

---

## Appendix — how this scoping was produced

The problem selection was put through a six-seat adversarial review (three rounds, anonymised
cross-examination, confidence-weighted tally) rather than asserted, specifically because I had
already formed a preference for Problem A and a solo judgement is worth least under exactly that
condition.

It changed the output in three ways: it surfaced **O4** (the trust opportunity absent from the
brief); it established that an initial unanimous "pick A" was six positions meaning four
incompatible things; and it produced the falsifiable kill criteria rather than conclusions.

Honest limits, recorded rather than buried: the review used a single model provider, produced zero
empirical measurements, and no seat seriously entertained B or C as the final pick. It is not
possible to fully separate *"A is correct"* from *"one model's priors, run six ways, land on A."*
That is precisely why §1.5, §2.5 and §2.7 are written as things to check in the field rather than
as conclusions to defend.

- Full deliberation record: [`../decisions/council-d1-problem-selection/`](../decisions/council-d1-problem-selection/)
- Decision record: [`../decisions/0006-problem-a-plus-handover-act.md`](../decisions/0006-problem-a-plus-handover-act.md)
- Visual artifact: [`../artifacts/03-opportunity-map-council-verdict.html`](../artifacts/03-opportunity-map-council-verdict.html)
