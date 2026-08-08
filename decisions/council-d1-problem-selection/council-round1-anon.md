# Round 1 — Anonymised Peer Analyses

**Identity is masked.** Evaluate by argument quality, not by source. Refer to peers as
"Member A", "Member B", etc. Do not use real council member names in your response.

You are one of these six. Do not attempt to identify which.

---

## Member A

### Essential Question
Whose 40 hours get returned, and does the Ministry still trust and run the thing after the FDE walks?

### The User
Three distinct users, not one. The **MoH Director**: decides under time pressure, non-technical,
needs a number she can defend in a cabinet meeting without checking it twice. The **MoH analyst**:
40 hrs/month copying DHIS2 Excel exports into a bulletin — expert at the domain, not the tooling;
needs the copying gone, not a new system to learn. The **clinic-level DHO**: already exists,
already does data analysis and IT support per facility — the overlooked user every candidate
ignores. Building B or C without routing through the DHO builds a system the Ministry can't
operate solo.

### Design Honesty Audit
Problem B promises "real-time" against 70% paper-only facilities and DHIS2's 2–3 week lag.
That's not a dashboard problem — that's dishonest UI over stale data, exactly the "mess" the
Director complained about, just prettier. Problem A is honest: the analyst's 40 hours produce a
real report from real (if aggregate) data; automating it removes labor, not truth.

### Complexity Reduction
The DHO role already does data analysis per clinic. Any solution requiring a new central team,
new login, new mental model to interpret is unnecessary complexity layered atop existing
capacity. Wire into the DHO, don't route around them.

### Less, But Better
A dashboard nobody asked for, showing data that's 3 weeks late anyway, is more design than the
Director needs. A report that already runs monthly, minus 40 hours, is less — and better.

### Verdict
**Problem A.** Confidence: **Medium.**

### Where I May Be Wrong
User-centred design isn't sufficient — A is a smaller market/political win. If Sand's business
needs the B narrative to scale to 15 countries, the "losing position" isn't UX, it's strategy.

---

## Member B

### Essential Question
Which of A/B/C ships in 6 weeks, keeps running with zero Sand engineers in the room, and doesn't
require infrastructure that doesn't exist?

### What Actually Works
DHIS2 exports already run monthly. A "conformed mart → Superset template → scheduled report"
pipeline is not R&D — it's wiring together tools Sand already staffs for (Superset, dbt, Airflow
per their own job postings). Problem B needs real-time facility status feeding off 175 paper-only
sites (70% of facilities) with 4–6hr/day power. There is no sensor, no app, no data source for
those 175 sites. You can't dashboard data that doesn't exist. B is not "harder," it's currently
*impossible* for most of the fleet — you'd be building a beautiful UI over a null field.

### The Maintenance Cost
A's runtime cost after handover: a cron job and a Superset dashboard. An MoH IT team person can
restart a stalled scheduled query. B's runtime cost: an ingestion pipeline plus a paper-to-digital
data collection process for 175 facilities that doesn't currently exist and that Sand isn't
building in 6 weeks. That's not a maintenance cost, that's a second unstarted project wearing B's
clothes.

### The Boring Solution
Automate the bulletin. DHIS2 pull, existing Excel structure as the target schema, scheduled
Superset report. Boring, proven, ships week 3, leaves weeks 4–6 for hardening and handover
training.

### Over-Engineering Check
B is the over-engineered choice here — not because it's technically complex, but because it's
solving for infrastructure Sand doesn't have permission or time to build. That's premature
abstraction dressed as ambition.

### Verdict
**Problem A.** Confidence: **High.**

### Where I May Be Wrong
If the Solutions Manager's B-narrative is unmovable politically, shipping A "correctly" but losing
the internal argument means A never gets credited as a win.

---

## Member C

### Essential Question
Which of three exposures has a payoff structure where being wrong is survivable, and being right
compounds — versus one where being wrong is a tail event you cannot walk back?

### Domain Classification
Mixed. Reporting cadence (A) sits in **Mediocristan** — errors are additive, a wrong bulletin
number is corrected next quarter, bounded loss. Patient identity matching (C) sits in
**Extremistan** — the loss function is not linear. One false merge (co-infected TB/HIV patient B
fused with patient A's record) doesn't cost "a bad dashboard cell," it costs a wrong drug regimen,
a missed contraindication, a death, and a Ministry that now distrusts every record Sand ever
touched. That's a fat left tail hiding inside what reads as a data-integration ticket.

### Fragility Audit
**A (Bulletin):** Fragile only to *effort* (40 hrs/month), not to *catastrophe*. Robust — errors
are visible, correctable, low-stakes. **B (Facility status):** Fragile to staleness masquerading as
freshness — a "real-time" dashboard fed by 175 paper facilities creates false confidence, but the
harm is diffuse, not a single triggering event. **C (Unified patient view):** Antifragile-*looking*
(more integration = more insight) but actually the most fragile candidate in the set —
probabilistic identity matching across CommCare silos, in 6 weeks, with no existing MoH
clinical-safety review process, is a single-point catastrophic failure mode disguised as a data
project.

### Via Negativa
Don't ask what dashboard to add. Ask what to remove: remove the FDE's exposure to irreversible
clinical error. Remove any solution whose failure mode requires a coroner's inquest rather than a
bug ticket.

### The Barbell
Extreme safety: ship A — bounded, reversible, rebuilds the 40 hours *and* the Director's trust
cheaply. Small aggressive bet: prototype B's situation-map view as a read-only,
clearly-labeled-stale add-on — upside optionality for the Solutions Manager's narrative, zero
downside since it's advisory, not decisional. Leave C alone entirely until the Ministry has an
actual patient-safety review process to catch merge errors — that's a precondition, not a sprint.

### Verdict
**Problem A.** Confidence: **High** on the Extremistan classification of C; **Medium** on A over B
as the single pick.

### Where I May Be Wrong
I may be pattern-matching "identity merge = malpractice risk" onto a system that already has
downstream human clinical review as a backstop. I also may be undervaluing that a good B could
reveal the exact 175-facility paper gap I care about, making it the more convex bet.

---

## Member D

### Essential Question
The Director said "our data is a mess," not "automate our bulletin" — who decided A/B/C exhaust
the solution space, and is "which problem" itself premature when the real deliverable in week 1
may be trust, not software?

### Assumptions Examined
**1. "Our data is a mess" refers to data quality.** If true, fixing it means cleaning/consolidating
records. But test: 70% of facilities are paper-only — there is no data to be messy, there is
*absence*. If the assumption held, A (which repackages DHIS2 exports) would satisfy her. It won't —
it automates the mess, doesn't resolve it. Contradiction: the stated words and the literal problem
don't match.

**2. Six weeks produces a "problem solved."** If true, handover succeeds by week 6. But the brief's
own success criterion is whether the Ministry *still runs it after exit* — a fact about week 7
onward, unmeasurable at week 6. The sprint cannot prove its own success criterion within its own
timeframe.

**3. Discovery week correctly scoped the options.** The Solutions Manager pre-selected B before
discovery occurred. If discovery genuinely generated A/B/C, why does the pre-discovery hypothesis
exactly match one of the three? Either discovery was theater, or B was fitted to a prior
conclusion.

### The Hidden Question
Not "which problem" but "whose 40 hours, and whose trust, is the unit actually being purchased
here?" The Director bought relief from *not trusting the numbers she's shown*, not a bulletin.

### What Survives Examination
A is the only candidate whose delivery path (DHIS2→mart→Superset) is entirely pre-built, verifiable
against the paper record within 6 weeks, and directly answers what was literally said — even though
it doesn't answer what was structurally meant.

### Verdict
Commit to **A** — not because it is the deepest need, but because it is the only claim the FDE can
*prove true* by week 6, and proof is the actual currency being traded for trust in a first-country,
template-setting engagement. Confidence: **Medium.**

### Where I May Be Wrong
I may be mistaking "provable" for "valuable". A working bulletin that nobody at the Ministry needed
once trust existed would be a hollow win.

---

## Member E

### Essential Question
What stock is the 6-week sprint meant to build — and does the chosen intervention change the
*structure* that produces "our data is a mess," or just relocate the mess to a new format?

### System Map
**Stocks:** (1) MoH trust in Sand — depletes on missed handover, replenishes on visible delivered
value; (2) MoH IT capacity/skill — currently near-zero, the accumulating variable that determines
post-exit survival; (3) Director's decision-confidence — currently near-zero; (4) the 40 hrs/month
staff-time stock, currently drained into manual compilation.

**Reinforcing loop (the trap):** FDE builds sophisticated tool → MoH IT team never touches it (no
capacity stock built) → tool breaks after handover → Director's data distrust *increases* → next
Sand engagement starts from a worse trust baseline than this one. This is **Shifting the Burden**:
the FDE (capable outsider) becomes the crutch; the intervention that "solves" the symptom erodes
the capacity to solve it internally.

**Balancing loop (the delay):** Bulletin automation *feels* like it closes the loop (task done →
hours freed) but the delay between "dashboard shipped" and "MoH IT can maintain it" is invisible in
week 6 — it only shows up months later, past the FDE's exit.

### Leverage Point Analysis (ranked)
- **Parameter** (weakest): report frequency, chart choices — irrelevant to outcome.
- **Rule**: who owns/runs the pipeline after week 6 — this is where A/B/C actually diverge in effect.
- **Goal**: is the sprint's goal "deliver an artifact" or "transfer a capability"? Currently the
  system's operative goal (the pre-sold B-narrative) is artifact-delivery, not transfer.
- **Paradigm** (strongest, out of scope for 6 weeks): "Sand builds for the Ministry" → "Ministry
  builds with Sand."

### Unintended Consequences
Picking B risks building situational-awareness UI on the 70%-paper substrate — a balancing loop
(data doesn't exist at facility level) resists any dashboard, producing a polished UI over garbage
data, which *accelerates* distrust rather than mitigating it. Picking A without the
capacity-transfer rule reproduces the same trap in a smaller, faster form.

### The Structural Fix
Choose A, but architect it as a rule-level change, not a parameter tweak: the DHO role (already
exists in-country) co-builds the DHIS2→mart→Superset pipeline alongside the FDE rather than
receiving a finished tool. The deliverable is the reusable loop, not the bulletin artifact.

### Verdict
**Problem A** — executed as capacity transfer, not artifact delivery. Confidence: **Medium.**

### Where I May Be Wrong
I'm assuming the DHO role is actually engaged, available and willing to co-build — unverified. If
genuine capacity-building is structurally impossible in 6 weeks regardless of which problem is
chosen, my leverage argument collapses back into pure artifact delivery anyway.

---

## Member F

### Essential Question
Whose incentives does the 6-week choice actually serve — the Director who spoke, or the Solutions
Manager who already decided?

### Incentive Map
Current state (data chaos) benefits nobody formally, but it benefits whoever owns "we need more
time/budget/staff" as an excuse — likely MoH mid-managers who've survived audits by blaming the
system. Change benefits the Director (credibility, decisions she can defend) and Sand's Country
Director (a referenceable win for the 15-country rollout). The Solutions Manager can *block* — he
pre-committed to B/Health Atlas before discovery, and he outranks the FDE. Ignoring him isn't
zero-cost even if he's wrong.

### Stated vs Revealed Preferences
The Director's revealed preference is legible: 40 hours/month, recurring, already scoped, already
causing her personal pain. That's a budget line, not a strategy slide. The Solutions Manager's
revealed preference is a pitch deck written pre-discovery — it wasn't derived from Rwanda, it was
imported. When stated (B, situational awareness) and revealed (A, the thing someone actually
complained about first, with a number attached) diverge, the number wins.

### The Uncomfortable Truth
The Solutions Manager isn't wrong out of malice — he's wrong out of ordinary institutional
laziness: reusing a template pitch is easier than doing new discovery, and abandoning it now costs
him face internally. Nobody schemes here; everyone just defaults to what protects their prior
commitment.

### The Pragmatic Path
Deliver A as the visible win (it's Superset-trivial — near-zero build risk), while quietly
instrumenting toward B's data (facility status) as a byproduct, so the Solutions Manager's
narrative isn't publicly falsified, just deferred.

### Verdict
**Problem A.** Confidence: **Medium.**

### Where I May Be Wrong
The Solutions Manager may have real information I don't — a funder or NHIC mandate tied to B —
that makes ignoring him organizationally fatal regardless of technical logic.
