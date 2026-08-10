# Vision review PASS0 baseline

_model: moonshotai/kimi-k3 · usage: {'prompt_tokens': 10303, 'completion_tokens': 2328, 'total_tokens': 12631, 'cost': 0.06517071, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.065829, 'upstream_inference_prompt_cost': 0.030909, 'upstream_inference_completions_cost': 0.03492}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}_

# Design Review: Rwanda MoH Digital-Health Landscape Briefing

## 1. VERDICT
**Acceptable** — information-dense and structurally ambitious, but undermined by cramped typography, low-contrast secondary text, and a cluttered integration diagram that fights the reader.

---

## 2. READABILITY

- [ ] **Global body text**: Secondary/descriptive text (e.g., under "Executive summary" bullets, persona card subtitles, table cells in §5) renders in a light grey (~#999–#aaa) on off-white. This fails WCAG AA for body text. **Fix**: Darken all body copy to minimum #444; reserve light grey only for de-emphasized metadata (timestamps, IDs).

- [ ] **Executive summary bullets**: The bold lead-ins ("National-first, government-hosted stack.") work well, but the supporting text is too small (~11px) and too light. At this density, an executive reader will skip. **Fix**: Increase body text to 13px minimum; increase line-height to 1.6.

- [ ] **Section 2 intro paragraph** ("Tiered from community edge up to external partners…"): Set in small, light-grey italic-adjacent text that reads as an afterthought. **Fix**: Style as a proper lead paragraph — 14px, #333, regular weight.

- [ ] **Section 3 persona cards**: The step cards (e.g., "Morning brief", "Trace a signal") have tiny body text (~10px) in light grey. The numbered step chips (①②③) are legible but the descriptive text beneath them strains. **Fix**: Minimum 11.5px for card body; darken to #333; add 4px more vertical padding inside each card.

- [ ] **Section 5 table**: The "MOH STACK TODAY" and "BENCHMARK PATTERN" columns contain long, multi-clause sentences in small type. Line length within cells is acceptable, but the font size (~10px) and grey tone make sustained reading difficult. **Fix**: Bump to 12px; consider breaking multi-clause cells into bullet fragments.

- [ ] **Evidence base footnote** (below §1): Rendered in very small, light-grey text that is nearly illegible. This is critical credibility content. **Fix**: Promote to a styled "Evidence Base" callout box with 12px text and clear separation from body.

- [ ] **Visual hierarchy**: Section headings (1–5) are clear and well-weighted. However, sub-elements within sections (e.g., the "DATA — consumes/produces" lines in §3) blend into the background. **Fix**: Style these as labelled metadata rows with a left border or background tint.

---

## 3. VISUALS

- [ ] **§2 Systems map SVG**: This is the strongest visual — tiered, colour-coded, with a legend. However:
  - [ ] The **"G — CSAM · HWMS · iHRIS…"** bar is a dense text string, not a visual element. It reads as an overflow error. **Fix**: Break into individual labelled chips or a sub-grid within the national tier.
  - [ ] The **dashed boxes** (B4 Health Portal, D3 Reagent ERP, I15 OpenEvidence) are good, but the dashed style is too subtle at this scale. **Fix**: Add a "planned/unverified" tag icon (⏳ or ⚠) inside dashed boxes for instant recognition.
  - [ ] **Edge labels** (E1–E9, E10, E18) are present but tiny. **Fix**: Increase edge label font size by 1–2px; ensure labels don't overlap box borders.

- [ ] **§4 Integration/data-flow SVG**: This is the weakest visual — it is cluttered, overlapping, and confusing:
  - [ ] **Edge crossings**: Multiple edges (E1, E4, E6, E7, E8, E9, E10, E11, E12) converge on the F1 RHIE/F2 OpenHIM box from both sides, creating a spaghetti junction. **Fix**: Route edges orthogonally with clear entry/exit ports; consider a left-to-right flow layout instead of the current radial approach.
  - [ ] **Overlapping text**: The "C2 RapidSMS · C3 RapidPro" box has overlapping/garbled text ("d-IDS de-identified cohort → strip CHW…" collides with "E13 de-id… E16…"). **Fix**: Increase box height; separate the two data flows into distinct labelled edges.
  - [ ] **The "× E32" anti-edge** (no automated EMR↔RSSB link) is a nice touch but visually lost. **Fix**: Render as a prominent red dashed X with a label, not a tiny footnote.
  - [ ] **The "SECONDARY USE" box** (IeDEA research extract) dangles at the bottom-left with a single thin arrow. **Fix**: Integrate into the main flow with a clear labelled edge from F1/F2.
  - [ ] **Missing legend**: The intro text describes solid/dashed/clay/rose conventions, but there is no visual legend within the SVG itself. **Fix**: Add a compact legend strip at the bottom of the SVG.

- [ ] **§3 Persona journeys**: These are text-heavy card grids, not visual journey lanes. They read as tables, not journeys. **Fix**: Convert to horizontal swim-lane diagrams with numbered step nodes connected by arrows, colour-coded by system tier (community/facility/national/external). Each persona lane should visually show the *flow* left-to-right, not just stack cards in a grid.

- [ ] **§5 Data-protection table**: The status column (●/◐/○ dots) is good but tiny. **Fix**: Increase dot size; add a text label ("Met", "Partial", "Gap") alongside each dot for accessibility. Consider a colour-coded left border per row (green/amber/red).

- [ ] **Missing visual — timeline**: The briefing references multiple time-bound events (Babyl shutdown Aug 2023, NHIC launch Apr 2025, Law 058/2021 in force Oct 2021, Horizon1000 by 2028). **Fix**: Add a compact horizontal timeline strip between §1 and §2 showing key dates/milestones.

- [ ] **Missing visual — data-protection radar/heatmap**: §5 is a long table. A summary radar chart or heatmap (obligations × status) would give executives a 5-second takeaway. **Fix**: Add a small multiples bar chart or colour-coded matrix above the table.

---

## 4. LAYOUT DEFECTS

- [ ] **§4 SVG — text overflow in C2/C3 box**: As noted above, text visibly overflows and overlaps within the "C2 RapidSMS · C3 RapidPro" box. This is a rendering defect.

- [ ] **§2 Systems map — "G" bar**: The workforce/financing/admin bar ("G — CSAM · HWMS · iHRIS · IPPIS · Licensing · MEMS · HRTT · eLearning · RHAP · PBF dashboard · RSSB/Mutuelle (CBHI)") is a single line of text that stretches the full width and breaks the visual grid. It looks like an unstyled overflow.

- [ ] **§4 SVG — bottom-left "IeDEA research extract (US)" box**: Appears visually disconnected; the arrow connecting it is thin and easy to miss. Alignment with the rest of the diagram is ambiguous.

- [ ] **§5 table — "Residency + cross-border" row**: The cell content is 4 lines long while adjacent cells are 1–2 lines, causing row height imbalance. Not a defect per se, but consider truncating with a "more" expander.

- [ ] **Collapsed sections** ("Edge register — E1–E32 condensed" and "Verified gaps register"): These render as collapsed `<details>` elements with a small triangle. They are easy to miss. **Fix**: Style as prominent expandable cards with a border and background tint.

- [ ] **Footer/sources**: The sources line at the very bottom is a single run-on line of small text. It should be a structured, multi-column or bulleted list.

---

## 5. CITATIONS

- [ ] **Sources section**: Present but inadequate. The "Sources:" line at the bottom is a dense, unpunctuated string of report names and URLs in tiny grey text. It is not credible as a citation apparatus. **Fix**: Create a proper "Sources" section with numbered references, each with title, publisher, date, and URL. Use a two-column layout for compactness.

- [ ] **Inline citations**: The briefing uses inline references (e.g., "PMC6918868", "E22–E25", "art. 50") which is good practice, but there is no key or bibliography mapping these to full citations. **Fix**: Add a reference list that maps edge IDs, PMC IDs, and legal article references to full source entries.

- [ ] **"EVIDENCE BASE" footnote** (below §1): Contains important confidence assessments ("HIGH on the core stack · MEDIUM on admin systems + AI vendors · LOW where flagged dashed") but is rendered in nearly invisible grey. **Fix**: Promote to a styled callout with a coloured left border.

---

## Priority-Ordered Punch List

| # | Priority | Fix |
|---|----------|-----|
| 1 | 🔴 Critical | §4 Integration SVG: fix overlapping text in C2/C3 box; re-route edges to reduce crossings; add visual legend |
| 2 | 🔴 Critical | Global: darken all body/secondary text to ≥#444; increase base font size to ≥12px |
| 3 | 🔴 Critical | Sources: restructure into a proper numbered reference section with full citations |
| 4 | 🟠 High | §3 Persona journeys: convert card grids to horizontal swim-lane flow diagrams with arrows |
| 5 | 🟠 High | §2 Systems map: fix the "G" bar overflow; break into individual system chips |
| 6 | 🟠 High | §5 Table: increase status dot size; add text labels; add row colour-coding |
| 7 | 🟡 Medium | Add milestone timeline strip between §1 and §2 |
| 8 | 🟡 Medium | Add data-protection summary heatmap/matrix above §5 table |
| 9 | 🟡 Medium | Promote "EVIDENCE BASE" footnote to a styled, visible callout |
| 10 | 🟡 Medium | Style collapsed `<details>` sections as prominent expandable cards |
| 11 | 🟢 Low | §5 "Residency" row: truncate long cell with expander |
| 12 | 🟢 Low | §4 SVG: integrate IeDEA secondary-use box into main flow |
