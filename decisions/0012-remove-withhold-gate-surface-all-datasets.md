# 0012, Remove the withhold gate, surface all five datasets, redesign the bulletin

- **Date:** 2026-08-14
- **Status:** Accepted
- **Supersedes:** ADR 0010's deferred-Flint-to-D3 line (adopted now); implicitly amends
  ADR 0008's "guards refuse claims, not rows" framing (refusal is replaced by
  disclosure-with-caveat; the statistical logic ADR 0008 committed to is unchanged)
- **Method:** measured against the built output and the provided sample data; every claim
  below is a number produced by `uv run python run.py` or `bun run verify`, not asserted

## Context

Three separate problems, found in the same review pass:

**The withhold gate hid real findings, not just weak ones.** `guards.py` computed two
real statistical tests, then rendered nothing when a claim did not clear a threshold. KN,
directly: "let us be able to see off the data." The tests are correct; a bulletin that
answers "what is the trend" with an empty section titled "Withheld" is not more honest
than one that answers it, caveated. It is less useful for the identical reason.

**Three of five source files were loaded and never queried past three covariates.**
`mart/crosswalk.csv` already maps every field in `governance.csv`, `operations.csv`, and
`healthcare_workers.csv` to a canonical element, and `silver.py` already resolves all of
them into `observations_resolved` at `period="ALL"`. Confirmed this session: of
governance's 11 fields and operations' 13, exactly three fed anything downstream
(`governance_staff_trained_rate`, `capability_cpap_machines`, `ops_referral_time_hrs`, the
stratification guard's own covariates). `healthcare_workers.csv`'s 11 fields fed nothing.
This was not an ingestion gap. It was unused gold-layer queries against data already
sitting in the mart.

**The trend was a 2-point delta because only two of four quarters were checked.** The
bulletin's own `temporal_signal_guard` withheld the trend section, which made "is there
more data" look like a closed question. It was not: `clinical_neonatal.csv` has real rows
for every month except `2024-02` and `2024-12`. Checked this session: Q1 2/3 months
(NMR 50.6), Q2 3/3 (50.3), Q3 3/3 (50.8), Q4 2/3 (49.9). Four points, not two.

## Decision

**Checks always render; a caveat replaces a gate.** `guards.py` → `checks.py`.
`temporal_signal_guard`/`stratification_guard` → `temporal_signal_check`/
`stratification_check`. The permutation test, the stratified-correlation test, the fixed
seed (`20260810`) and trial count (200) are byte-for-byte unchanged. What is removed is
`disposition`/`has_signal`/`survives_stratification` as fields a renderer branches on; what
is added is `caveat`, a sentence that is always populated and states plainly whether the
bar was cleared. Zero occurrences of "withheld" or "disposition" survive in
`web/src` or `pipeline/dataflow`, mechanically checked.

**Four new gold-layer functions, no new bronze or silver.** `facility_capability` pivots
`observations_resolved` (already-resolved data) to one row per facility across the ~40
governance/operations/staffing/capability elements the crosswalk already declares.
`capability_summary` rolls that up nationally, one row per metric (numeric fields) or
metric-category pair (categorical fields; every category gets its own count, not a single
hand-picked "affirmative" bucket, since the finding differs by field: "Yes" for protocol
status, "Never" for last-training-date). `known_contradictions` and
`cause_capability_links` are declared tables, following the crosswalk's own convention:
the pairing between a cause of death and the capability that treats it is a clinical
judgement call, not a statistical inference, so it lives in a CSV a non-engineer can
review, not in code.

**The trend section shows all four quarters**, each labelled with the months it actually
held (`gold.py`'s existing `QUARTER_MONTHS` constant already buckets all twelve months
correctly; only the Astro publish step was building two of four editions).
`web/package.json`'s `publish` script now builds `2024-Q1` through `2024-Q4`.

**Visual redesign: verdict-first fold, Swiss/Economist institutional direction.** Chosen
from three live mockups built with real Q1 figures (OWID dense-grid, Swiss/Economist,
Goalkeepers narrative); KN selected the Swiss direction after reviewing rendered HTML, not
a description. Everything above a hard visual break (`hr.fold-break`) is the number, its
implication against the WHO benchmark, a verdict paragraph, and an action line; the
masthead, navigation, and receipts strip move below it. New tokens
(`--ink #161513`, `--paper #f6f4ef`, `--red #c22029`) all clear WCAG AA against each other
at full saturation (measured 16.6:1, 5.41:1, 5.21:1), unlike the prior palette, which
needed darkened `-d` variants to reach the same bar.

**Chart engine: Flint (`microsoft/flint-chart`) compiling to Vega-Lite, rendered by
`vega`.** ADR 0010 deferred this "on time grounds alone." Flint's own `agent-skills/
flint-chart-author/SKILL.md` (pulled from the GitHub repo, not the docs site, which
returned inconsistent responses this session) is the authoritative API reference:
`assembleVegaLite(ChartAssemblyInput)` returns a Vega-Lite spec; `swiss` is a real
registered theme preset. Two things Flint's semantic layer deliberately does not expose
(colour/font/tick derivation is the product) are handled as the documented escape hatch:
author the Flint spec, then edit the compiled Vega-Lite spec for the one presentation
detail with no Flint knob: `HATCH_DEF` (a `fill` condition on the `provisional` field,
value `url(#hatch)`) and the district benchmark line (an added `rule` layer, positioned at
`y: {value: 0}` so its label anchors to the plot's top edge rather than colliding with
whichever district sits in the vertical middle of a 30-row list). A narrow `theme_spec`
override (`extends: 'swiss'`) pins Flint's own close-but-not-identical defaults
(`#1a1a1a`/`#f4f1ea`/`#e2231a`) to this project's exact tokens; `check-tokens.mjs` now
verifies that override against `tokens.css` directly, the same duplication-drift guard as
before, against a different source shape.

**Architecture artifact: two diagrams, one HTML file, `artifacts/
06-bulletin-architecture-data-flow.html`.** The data-flow diagram (D2 §1's three required
elements: data flow, which Sand products and why, build vs. buy per component) is
rendered via `plantuml -tsvg` (component diagram, `skinparam` mapped to the Anthropic
palette, stereotypes double as both semantic tags and colour selectors) and embedded as
static SVG, chosen over hand-coded SVG because a full local toolchain (`plantuml`, `dot`,
`java`) was confirmed present and Graphviz's auto-layout eliminates the exact class of bug
(hand-picked bezier coordinates drifting from the node grid) this repo's own html-kit
recipe already warns about. The ERD stays hand-drawn: it is deliberately *not* a
conventional FK-cardinality schema (a hub-and-spoke "six sources through one crosswalk
mechanism into one canonical fact table" shape), and PlantUML's `entity`/`||--o{` notation
assumes exactly the table-cardinality reading the diagram exists to argue against.

## Alternatives

- **Keep the gate, soften the threshold.** Rejected. The threshold (`observed > null_mean
  + 3·null_sd`) is a real statistical bar, not an arbitrary knob; softening it to let more
  content through would make the check meaningless rather than making the bulletin more
  honest. The fix is disclosure with a caveat, not a weaker test.
- **A single "affirmative" bucket per categorical capability field**, matching the
  original plan's verification query. Rejected once `staff_last_training`'s real values
  (`Never`, or an actual date) were checked: no single "Yes"-shaped category exists for
  every field, and forcing one would have made the "never trained" finding (the one
  actually cited in the brief's own required "facility performance scores") unreachable.
  `capability_summary` reports every category's own count instead.
- **PlantUML for the ERD too.** Rejected; see Decision above.
- **Keep Observable Plot, defer Flint again.** Rejected: ADR 0010's stated reason for
  deferral (frontend was still Python) no longer applies, and Flint's theme system removes
  the literal-hex-duplication `check-tokens.mjs` was written to guard against.

## Reverses if

- A reviewer specifically wants a bulletin that only ever shows statistically airtight
  claims. The old gate behaviour is a straightforward revert: the underlying check
  computations are byte-for-byte unchanged, only the consumer contract (`caveat` vs.
  `disposition`) would need to flip back.
- Flint or Vega prove unable to render server-side in the Ministry's actual deployment
  environment (untested outside this session's `bun x astro build`); Observable Plot's
  `git history` at this commit's parent is the fallback.

## Honest limits

- The correlation and trend figures still come from a synthetic sample (ADR 0008's own
  honest-limits note stands): what changed this session is *disclosure*, not the
  underlying epistemic status of the numbers. Showing four quarters instead of two, and a
  caveat instead of a blank section, does not make the sample non-synthetic.
- Flint's Vega-Lite compiler drops a custom `sortBy`/`sortOrder` encoding under specific
  multi-layer conditions (confirmed: a `Bar Chart` with Flint's own auto-generated
  value-label layers unions the `y` domain across layers and silently falls back to
  `sort: true`, alphabetical). Worked around by disabling Flint's auto-labels
  (`chartProperties.showValueLabels: false`) and adding one hand-authored label layer
  instead, which keeps the layer count low enough to avoid the union. Not filed upstream;
  worth a minimal repro if this recurs on a chart shape this bulletin doesn't use yet.
- The explore/interactive surface named in ADR 0008 (Mosaic over DuckDB-WASM, Apache
  Superset for the MoH office) is referenced in the architecture diagram's product-decision
  cards but not built in this deliverable; it remains scoped, not implemented.

## Artifacts

- `pipeline/dataflow/checks.py` - renamed from `guards.py`, gate fields removed
- `pipeline/dataflow/gold.py` - `facility_capability`, `capability_summary`,
  `cause_capability_links`, `known_contradictions`
- `pipeline/mart/cause_capability_links.csv`, `pipeline/mart/known_contradictions.csv`
- `pipeline/eda.py` - marimo notebook across all five source files, reusing
  `gold`/`checks` directly rather than reimplementing their computations
- `web/src/pages/index.astro`, `web/src/pages/email.astro` - verdict-first redesign
- `web/src/styles/tokens.css`, `web/src/styles/bulletin.css` - Swiss/Economist tokens
- `web/src/lib/charts.ts` - Flint + Vega-Lite + Vega, replacing Observable Plot
- `web/scripts/check-tokens.mjs`, `check-agreement.mjs`, `check-email.mjs` - updated
  guards for the new palette source and the caveat-not-withheld contract
- `artifacts/06-bulletin-architecture-data-flow.html` - D2 §1 diagram + ERD
- `artifacts/04-data-quality-eda.html` - marimo export, replaces `04-data-quality-audit.html`
