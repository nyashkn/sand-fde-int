# Round 2 — Anonymised Cross-Examination

Identity remains masked. Members are the same A–F as Round 1.

---

## Member A (Round 2)

### Disagree: Member C
Walk through the moment: a district health officer opens Member C's "clearly-labeled-stale,
read-only" B situation-map. The label is metadata; the map is a colour-coded grid of facility
status. Under time pressure — the exact condition the Director specified — a human reads the
visual first and the caption second, if at all. A green cell for a paper-only facility whose last
DHIS2 sync was 3 weeks ago doesn't say "unknown," it says "fine," because the UI grammar of a
status map *is* "current state." That's not advisory, it's decisional by default regardless of the
label — the same dishonesty I flagged in Round 1 for full B, now smuggled in as a "zero-downside"
side bet. A label doesn't neutralise a UI whose entire visual vocabulary asserts freshness it
doesn't have. If it's genuinely advisory, it shouldn't look like a dashboard at all — it should
look like a list of facilities with "no data since [date]," no colour, no map. **Convexity doesn't
launder honesty.**

### Strengthened by: Member E
Member E's DHO co-build reframes the DHO from an add-on constituency into the actual second *user*
of the deliverable — someone who needs to operate the pipeline, not just view a report. From that
DHO's chair: a finished tool handed over is one more system to babysit alone; a pipeline they
helped wire is one they can debug at 2am without calling Sand. That's discoverability solved
structurally, not through documentation.

### Position Update
None — Member E strengthens my original design, doesn't correct it.

### Evidence Label
ethical

---

## Member B (Round 2)

### Disagree: Member E
Shifting the Burden is a real trap, but E's fix inverts the risk it names. E's own "Where I May Be
Wrong" admits DHO engagement is unverified. Make co-build the *rule* for A and you've built a
second unproven precondition into a 6-week, 2-FDE sprint — if the DHO doesn't show up (likely;
they're not idle), A ships *nothing*, not a working-but-unmaintained cron job. A broken cron job is
a bug ticket. A stalled co-build is zero delivered value and a worse trust hit than the thing E is
trying to prevent. Capacity transfer doesn't require joint architecture — it requires the DHO in
the room for the final build session, running the restart themselves once while the FDE watches,
before exit. That's hours, not a redesign, and it still moves the "who owns the rule after week 6"
lever E correctly identifies as the one that matters.

### Strengthened by: Member D
D's contradiction test (A repackages the mess, doesn't resolve it) is the sharpest attack on "A as
artifact" — it's why I'd fold in the handover-restart requirement above, not because E's systems
framing wins, but because D shows A-as-pure-artifact is provably hollow.

### Position Update
Ship A. **Add:** mandatory DHO-runs-the-restart session in week 6. **Cut:** any joint pipeline
architecture, any capacity-building ceremony beyond that. C's read-only B map is not zero-cost — a
Director sees a screen, she acts on it regardless of the label, and it costs FDE hours A needs.
Scope creep with a disclaimer.

### Evidence Label
mechanistic

---

## Member C (Round 2)

### Disagree: Member A
Member A calls any B-shaped artifact "dishonest UI over stale data" — collapsing my proposal into
the exact thing I explicitly ruled out. My B prototype is read-only, clearly-labelled-stale,
advisory not decisional. Dishonesty requires a decision-maker acting on data believing it's live; a
labelled-stale map removes the deception mechanism, it doesn't paint over it. Member A is right
that an *unlabelled* real-time claim is fraud dressed as UX — but that's a different artifact.
**Concede:** if "stale" labelling degrades under Ministry political pressure to look more current
than it is (a plausible tail risk), Member A's critique reattaches. I flag that as a fragility in
my own design, not a refutation of it.

### Disagree: Member B
Member B's "scope creep" charge assumes the barbell adds build-time. It doesn't — it's the *same*
pipeline output rendered as a map instead of a bulletin table, near-zero marginal engineering.
Scope creep is when the small bet threatens the core deliverable's timeline; mine is asymmetric by
construction — small aggressive bet, capped loss.

### Strengthened by: Member D
Member D's contradiction test sharpens *why* the barbell exists — A alone is provably-true but not
provably-valuable, and my B-sliver is the cheap option on "valuable" without betting the sprint.

### Member E fragility check
Capacity-transfer-as-condition is the most fragile Round-1 proposal precisely because it's
**domain-dependent Extremistan disguised as Mediocristan**: DHO co-build reads like a linear
staffing problem (add a collaborator, get proportional capacity), but it's a single dependency with
a binary failure mode. Fragile BECAUSE if DHO co-build stalls halfway, the FDE has spent 3 of 6
weeks in a teaching posture with nothing shippable, and must either revert to a compressed solo
build or miss the deadline. Who bears the downside: not Member E, not the Solutions Manager who
gets credit for the "capacity transfer" narrative regardless — the **FDE and the Director**, who
owns a broken artifact and a second disappointment in front of cabinet. **Skin in the game is
inverted.**

### Position Update
Unchanged on A + read-only-B. Refined: the label must survive institutional pressure to over-claim,
or Member A's critique is correct.

### Evidence Label
mechanistic

---

## Member D (Round 2)

### Disagree: Member E
Member E's "capacity transfer" condition and Member B's "smallest possible wiring" condition cannot
both be true, and E doesn't notice this. Co-building the pipeline *with* the DHO means the DHO's
ramp-up, availability and skill gaps become the sprint's critical path — that is strictly more
schedule risk than "wire it and hand it off," not a variant of it. E calls this "architecting a
rule-level change," but a rule-level change inside a 6-week, 2-FDE sprint is a *scope increase*
wearing a systems-thinking vocabulary. E's own "Where I May Be Wrong" admits the DHO's engagement
is unverified — meaning E is recommending we bet the entire timeline on an assumption E itself
flags as unverified. That's not a refinement of A. That's a different, riskier project that happens
to output the same artifact.

### Strengthened by: Member C
C's Extremistan/Mediocristan split exposes something I underweighted: my "provable by week 6"
standard treated all provability as equally valuable, but C shows bounded-loss provability (A) is
categorically different from tail-risk provability (C). A is defensible not merely because it's
provable, but because its failure mode is *correctable*, which is what makes proof meaningful as
currency here.

### Position Update
Unchanged on the verdict, sharpened on the reason. **The unanimity is not independent convergence**
— five of six converged on "A" while smuggling in incompatible payloads (minimal wiring, capacity
transfer, side-bet, cover instrumentation). That's anchoring on a *label*, not agreement on a
*thing*. My commitment: A, scoped as the provable artifact only — Members B and E cannot both be
describing the same commitment.

### Evidence Label
heuristic

---

## Member E (Round 2)

### Disagree: Member B
Member B calls capacity-transfer "over-engineering that risks shipping nothing." That conflates
*scope* with *leverage level*. My proposal adds zero new artifacts — same DHIS2→mart→Superset
pipeline B specs, built *alongside* the DHO instead of *for* them. The risk isn't the deliverable
slipping; it's who holds the keyboard during weeks 3–5. If B's version ships and only Sand's FDE
understands the dbt model, we've re-run the exact reinforcing loop the brief exists to break:
capable-outsider-as-crutch → tool degrades post-exit → distrust compounds. **I concede one thing:**
if the DHO is genuinely unavailable, B's minimal-wiring version is the correct fallback — not
because it's simpler, but because a rule-change with no counterparty collapses back to
parameter-tweaking anyway.

### Strengthened by: Member D
Member D's contradiction-check — "mess" implies quality problems, but 70% paper-only means
*absence*, not messiness — sharpens my stock map: the missing stock isn't data, it's MoH IT
capacity. Same variable, arrived at via a different method. Converging evidence, not converging
bias.

### Position Update
No update on the verdict. Update on emphasis: the unanimous "A" consensus is itself a leverage-level
illusion — six members agreeing on *which artifact* while disagreeing on *what A must include* means
the vote measured the wrong variable. **Unintended consequence** of shipping A-as-artifact even with
"quiet instrumentation toward B": it teaches the Ministry that Sand's real deliverable is
impressive-looking software, reinforcing the paradigm (Sand builds *for*, not *with*) that produces
this exact failure mode in country #2.

### Evidence Label
mechanistic

---

## Member F (Round 2)

### Disagree: Member E
E's "structural fix" requires the DHO to co-build the pipeline — but E's own "Where I May Be Wrong"
admits this is unverified. That's not a footnote, it's the whole plan collapsing. Institutions don't
allocate scarce staff time to a visiting FDE's capacity-transfer agenda by default — the DHO has an
existing job, existing incentives, and zero stake in Sand's 15-country rollout narrative. Absent a
costed commitment from MoH leadership (not "the DHO role exists in-country," but "this named person
has cleared hours"), E's rule-level fix is a wish dressed as an architecture. Revealed preference:
nobody at MoH asked for co-building, they asked for their 40 hours back. **E's plan should be
conditional** — "if DHO commits, do this; if not, revert to bare A" — not a verdict.

### Disagree: Member C
"Zero downside" for the read-only B side-prototype is a category error. The downside isn't
technical, it's political: once the Solutions Manager sees a stale-labelled situation-map exists, it
becomes the thing he shows the funder, labels quietly drop off in the retelling, and the FDE now
owns a half-built B narrative with none of the 6 weeks budgeted to make it safe. **"Read-only"
doesn't bind how *other people* use an artifact once it exists.**

### Strengthened by: Member D
D's point that A "doesn't answer what was structurally meant" sharpens my incentive read: A succeeds
by satisfying the Director's stated preference *and* being provable — that's exactly what makes it
politically safe to ship.

### Position Update
None on my Round 1 pick. Confidence unchanged: Medium.

### Evidence Label
strategic
