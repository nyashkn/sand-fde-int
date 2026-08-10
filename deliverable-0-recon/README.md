# Deliverable 0 — Pre-Engagement Recon Deep-Dive

**Role:** Forward Deployed Engineer · **Premise:** *Before* proposing anything, run a full,
MECE technical reconnaissance of the target's digital landscape — and produce an artifact a
sponsor can read in ten minutes.

> **Why "Deliverable 0"?** D1–D4 assume you already understand the terrain. This is the step
> that earns that assumption. It is the reusable machine I would run in the first days of *any*
> engagement, before a single line of scoping. The worked example here is the Rwanda MoH — the
> same target as the rest of this repo — but the pipeline is target-agnostic (see
> [`pipeline/`](pipeline/)).

---

## What it produces

A single self-contained HTML artifact (inline CSS/SVG, no external assets, opens offline) with
five sections, sourced entirely from a synthesis file so every claim is traceable:

1. Executive summary
2. Systems map — every system of record and the tiers they sit in
3. Persona journeys — one lane per role, leadership down to the field
4. Integration & data-flow — who sends what to whom
5. Data-protection posture — mapped against the jurisdiction's law

The worked example is [`example-moh-rwanda/artifacts/architecture.html`](example-moh-rwanda/artifacts/moh-rwanda-architecture.html).
Open it in a browser. Before/after screenshots are in
[`example-moh-rwanda/artifacts/screenshots/`](example-moh-rwanda/artifacts/screenshots/).

---

## How it works

Three [fabro](https://fabro.sh) workflows (deterministic DAGs of agent + script nodes). The full
mechanics, and the eight hard-won gotchas behind them, are in [`pipeline/README.md`](pipeline/README.md).

### 1. `recon` — MECE deep-research (7 lanes)

`scope` decomposes the goal into seven mutually-exclusive, collectively-exhaustive lanes, then a
static fan-out researches them in parallel, each following a shared **deep-web-search** skill
(Perplexity + Parallel.ai + Exa + native web tools, two-pass "discover then double-click"). A
`synth` node fuses the seven lane files into one sourced model; a `visual` node renders the HTML;
a `coverage` goal-gate fails the run unless every lane file and the artifact exist.

The seven lanes are the recon axes: **systems** (internal + external) · **deployment** · **vendors
incl. AI** · **data-protection in practice** · **personas + journeys** · **integration + data-flow**
· **data-protection law + peer benchmark**.

### 2. `refine` — citations + machine-vision review

Embeds the load-bearing source links back into the artifact (believability), then runs a
**machine-vision loop**: render the page to a screenshot → a vision model (kimi-k3) *sees the
pixels* and writes a concrete critique → a refine agent applies it. Two passes.

> fabro agents are text-only — `read_file` does not hand pixels to the model (verified). So the
> vision runs in a side-channel script (`scripts/vision_review.py`) and only its **text** critique
> re-enters the graph. fabro's own answer to "UI work" is a human preview gate; this pipeline adds
> the automated eye on top.

### 3. `polish` — subtractive readability pass

The catch we hit and fixed: a refiner told to *add* (sources, KPIs, fixes) monotonically increases
density — the vision verdict actually regressed from *Acceptable* to *Weak*. The fix is a separate
**subtractive** pass: CSS/layout only, forbidden from adding, removing, or rewording any fact or link. A
verdict-gate blocks completion while the vision model still says "weak", so a failed run simply
means "iterate again". One cheap pass flipped it back to *Acceptable*.

---

## The worked run (Rwanda MoH), honestly

| Stage | Result | Cost |
|---|---|---|
| `recon` | 8 sourced lane files + first artifact; systems/deployment/vendors/integration all grounded (DHIS2/HMIS, OpenMRS, e-LMIS, RapidPro, RHIE/OpenHIE, NHIC) | $0.31 |
| `refine` | 45 external source links + 88 in-page citations embedded; still self-contained; **but vision verdict regressed to Weak** (density) | $4.24 |
| `polish` | subtractive pass on a cheap model; **verdict Weak → Acceptable**, all 45 links kept | $0.05 |
| `v2 redesign` | rebuilt fresh from `synthesis.md` against the reference exemplar — personas as **SVG swimlane journeys** + a **persona×systems access matrix**, tiered diagrams, 102→65 KB, 45 links kept | — |

The refine/polish loop restyles but cannot restructure; the v2 redesign is what turned a dense
draft into a visual-first briefing. Its design system is extracted to
[`pipeline/assets/design-system.css`](pipeline/assets/design-system.css) and the required section
structure is baked into [`pipeline/skills/html-artifact/SKILL.md`](pipeline/skills/html-artifact/SKILL.md),
so future recon runs inherit it.

Full artifact set (final + baseline HTML, synthesis, the seven lanes, the extracted sources, and
every vision-review verdict) is under [`example-moh-rwanda/artifacts/`](example-moh-rwanda/artifacts/).
The exact workflows that produced it — including the two throwaway smokes — are in
[`example-moh-rwanda/workflows-as-run/`](example-moh-rwanda/workflows-as-run/).

### What I would not claim

- Public documentation on a ministry's *internal* systems is thin; the lane files flag confidence
  per section rather than inventing detail.
- The artifact is a **credible reconnaissance map, not ground truth** — it is built from public
  sources and would be corrected against a live environment in Week 1.
- The vision verdict tops out at *Acceptable*. One more `polish` pass would chase *Strong*; I
  stopped at the target bar rather than burn credits proving a point.

---

## Reuse

The pipeline is target-agnostic. To run it for a new engagement:

1. Copy [`pipeline/`](pipeline/) into a fresh workspace, drop the two `skills/` under `.fabro/skills/`.
2. Edit `workflows/recon.toml`: set the `goal` (name the target, sector, jurisdiction) and
   `working_dir`; optionally add domain seed-terms at the `SEED:` markers in `recon.fabro`.
3. `fabro create workflows/recon.toml && fabro start <id>` → then `refine` → `polish`.

See [`pipeline/README.md`](pipeline/README.md) for the operator guide, model/credit notes, and the
gotchas. Rationale for shipping recon as a numbered deliverable is in
[`../decisions/0008-recon-before-engagement.md`](../decisions/0008-recon-before-engagement.md).
