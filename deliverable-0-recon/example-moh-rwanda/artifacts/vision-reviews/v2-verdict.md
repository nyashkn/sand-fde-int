# Vision review V3 overlap-fix+links+glossary

_model: moonshotai/kimi-k3 · usage: {'prompt_tokens': 7780, 'completion_tokens': 2485, 'total_tokens': 10265, 'cost': 0.06000885, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.060615, 'upstream_inference_prompt_cost': 0.02334, 'upstream_inference_completions_cost': 0.037275}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}_

# Design Review: Rwanda MoH Digital-Health Landscape Briefing

## 1. VERDICT
**Acceptable** — the information architecture is strong and the content is dense, but the page is undermined by a catastrophic layout failure (massive blank whitespace consuming the bottom ~60% of the viewport) and several readability issues in body text and diagram labels.

---

## 2. READABILITY

### Critical
- [ ] **Global body text**: The primary body copy (intro paragraph, section descriptions, table cells) renders at what appears to be ~11–12px in a light grey on cream background. This is below WCAG AA contrast thresholds. **Fix**: Darken body text to `#333` minimum; increase base font size to 14px; ensure contrast ratio ≥ 4.5:1 against the cream/off-white background.

- [ ] **Section 02 Systems Map**: Node labels inside the SVG boxes are extremely small (~8–9px equivalent) and rendered in a muted grey-green that blends into the box fills. The tier labels ("EXTERNAL / PARTNER", "FACILITY TIER", "COMMUNITY TIER") are slightly better but still low-contrast. **Fix**: Increase node label font-size to minimum 11px; darken label colour to `#1a1a1a`; add `font-weight: 500` to node titles.

- [ ] **Section 03 Persona × System matrix**: The persona row labels (P1–P6) and column headers (A–I) are readable, but the dot markers are small and the colour differentiation between "uses" (filled circle), "feeds" (diamond), and "reads" (open circle) is subtle at this scale. **Fix**: Increase marker size by 30%; add a slightly darker stroke to open-circle markers; consider adding a hover tooltip or making the legend more prominent.

- [ ] **Section 04 Persona Journeys**: The stage boxes contain multi-line text at very small sizes. The bracketed system references like `[H1 NHIC PORTAL]` are legible but the descriptive text above them is cramped. **Fix**: Increase stage box padding from ~8px to 12px; increase font-size of stage descriptions to 11px minimum.

- [ ] **Section 05 Integration & Data Flow**: Edge labels (e.g., "UPID lookup · lab order → SHR", "HIV CBS Line List · FHIR ServiceRequest") are rendered in a light grey italic that is difficult to read against the cream background. **Fix**: Darken edge labels to `#555`; increase font-size to 10px minimum; consider adding a subtle background rect behind labels for readability.

- [ ] **Section 06 Data-protection table**: The "HOW THE MOH STACK ADDRESSES IT TODAY" column contains long prose in small text. The STATUS badges (DOCUMENTED / PARTIAL / GAP) are colour-coded but the badge text is small. **Fix**: Increase table cell font-size to 12px; add `line-height: 1.5`; make status badges slightly larger with bolder text.

- [ ] **Section 07 Sources**: Reference entries are rendered at very small size (~9–10px). The superscript numbers are barely legible. **Fix**: Increase source entry font-size to 11px; make superscripts at least 8px with a distinct colour.

### Moderate
- [ ] **Hero section**: The main title "Rwanda's national digital-health stack, at a glance" is strong. The subtitle paragraph below it is well-sized but the inline bold/coloured spans (e.g., "identity (UPID/NIDA)", "aggregate reporting (DHIS2)") create visual noise. **Fix**: Reduce the number of inline colour changes; use bold sparingly for 3–4 key terms maximum.

- [ ] **Stat cards row** (58,567 / 42 / 97 / Apr 2025 / 2012): Numbers are large and clear, but the descriptive text below each number is small and low-contrast. **Fix**: Darken descriptive text to `#444`; increase to 12px.

---

## 3. VISUALS

### Systems Map (Section 02)
- [ ] **Generally good** — the tiered architecture is clear with distinct visual bands. The colour-coding by category (reporting, facility EMR, community, supply chain, etc.) is present in the legend but the colours within nodes are subtle.
- [ ] **Upgrade**: The legend at the bottom is a horizontal strip of tiny colour swatches with labels. Make it more prominent — consider a 2-row grid with larger swatches (16×16px) and clearer labels.
- [ ] **Add**: Connection lines between tiers are present but thin. Consider adding subtle arrows or making the flow direction (top-down) more explicit with labelled arrows between tier bands.

### Persona × System Matrix (Section 03)
- [ ] **Good concept** — the dot-matrix approach is clean. However, the grid lines are very faint, making it hard to trace across a row.
- [ ] **Fix**: Add slightly more visible row separator lines (`#ddd` instead of current near-invisible lines); consider alternating row background tint (`#fafafa` / `#fff`).

### Persona Journeys (Section 04)
- [ ] **Strong** — this is the best visual on the page. Six horizontal lanes with colour-coded left borders, stage boxes with system references, and outcome chips at the end. Clear and information-dense.
- [ ] **Minor fix**: The outcome chips on the right (e.g., "OUTCOME: MINISTERIAL BRIEF") could be slightly larger and more visually distinct — consider a filled background rather than outlined.

### Integration & Data Flow (Section 05)
- [ ] **Adequate but could be stronger** — the three-column layout (Producers → Interoperability Layer → Consumers) is logical. The OpenHIM mediator box in the centre is well-placed.
- [ ] **Upgrade**: The dashed vs. solid line distinction (documented vs. integration-app) is explained in the legend but the visual difference is subtle. Make dashed lines more distinctly dashed (longer dashes) and consider adding a colour difference (e.g., solid = dark, dashed = amber).
- [ ] **Add**: The flow from NHIC down to "Dashboards / API" is present but the Superset connection could be more visually prominent given its importance.

### Data-Protection Table (Section 06)
- [ ] **Functional but plain** — this is a table, not a diagram. For an executive briefing, this is acceptable, but consider:
- [ ] **Optional upgrade**: Convert the STATUS column into a visual heat-map or traffic-light indicator strip for faster scanning.

### Missing Visual
- [ ] **Add a summary/takeaway visual** at the very top or bottom — a single "state of the stack" scorecard or maturity radar chart that an executive can absorb in 5 seconds. Currently the "one-line read" callout box serves this purpose textually but has no visual anchor.

---

## 4. LAYOUT DEFECTS

### Critical
- [ ] **MASSIVE BLANK SPACE**: Approximately 55–60% of the total page height below the Sources section (Section 07) is completely empty cream-coloured whitespace. This is the single most damaging visual defect. It makes the page look broken or unfinished. **Fix**: Identify and remove whatever is generating this space — likely an absolutely-positioned element, an SVG with excessive viewBox height, an uncleared float, or a `min-height` / `padding-bottom` on the body or a wrapper div. The page should end shortly after the Sources section footer.

### Moderate
- [ ] **Right-edge "BACK TO TOP" button**: A small orange/red element is visible at the extreme right edge of the viewport, partially clipped. It appears to be a floating action button. **Fix**: Either position it fully within the viewport with adequate right margin (16px), or remove it if the page is intended as a single-viewport artifact.

- [ ] **Section 02 Systems Map SVG**: The SVG appears to extend full-width but the content within it is centred with generous margins. On wide viewports this creates excessive left/right padding within the map container. **Fix**: Constrain the SVG max-width to ~1200px and centre it, or allow the node boxes to flex wider.

### Minor
- [ ] **Stat cards row**: The five stat cards are evenly spaced but the last card ("2012") has noticeably less descriptive text, making it visually unbalanced. **Fix**: Add a supplementary line to the 2012 card or equalize card heights with `align-items: stretch`.

- [ ] **Section 06 table**: The table appears to render correctly but the rightmost column edges are very close to the container border. **Fix**: Add 8–12px right padding to the table container.

---

## 5. CITATIONS

- [ ] **Sources section is present and credible** — Section 07 "Sources — 45 vetted references, grouped by section" is well-organized with numbered references grouped by the section they support (Systems Inventory, Systems Map, Persona Journeys, Integration & Data-Flow, Data-Protection & Law). This is excellent practice.
- [ ] **In-body superscript references**: The intro text mentions "In-body superscripts link here" and some superscripts are visible in the hero paragraph (small numbers after key claims). However, they are very small and easy to miss. **Fix**: Make superscripts slightly larger and use a distinct link colour (e.g., blue or the accent orange) to signal interactivity.
- [ ] **Footer note**: The closing note about "Single source of truth" and confidence levels is a nice touch for credibility.
- [ ] **No visible hyperlinks**: The source entries appear to be plain text (author — title format) without visible URL links. For a digital artifact, consider making each source entry a clickable link. **Fix**: Wrap source titles in `<a>` tags with `text-decoration: underline` and a link colour.

---

## Summary Punch-List (Ordered by Impact)

| # | Priority | Fix |
|---|----------|-----|
| 1 | 🔴 Critical | Remove the massive blank whitespace below Section 07 — page should end after the footer |
| 2 | 🔴 Critical | Raise global body text contrast: darken to `#333`, increase base size to 14px |
| 3 | 🔴 Critical | Increase font sizes in all SVG diagrams (systems map, integration flow) to minimum 10–11px for labels |
| 4 | 🟠 High | Fix or remove the clipped floating button at the right viewport edge |
| 5 | 🟠 High | Darken edge labels in Section 05 integration diagram; add label backgrounds |
| 6 | 🟠 High | Increase source entry font-size in Section 07; make entries clickable links |
| 7 | 🟡 Medium | Strengthen grid lines in Section 03 matrix; enlarge dot/diamond markers |
| 8 | 🟡 Medium | Add padding to Section 04 journey stage boxes; increase description font-size |
| 9 | 🟡 Medium | Make Section 02 legend more prominent (larger swatches, clearer layout) |
| 10 | 🟡 Medium | Differentiate dashed vs. solid edges in Section 05 more strongly (colour + dash pattern) |
| 11 | 🟢 Low | Reduce inline colour/bold noise in hero paragraph |
| 12 | 🟢 Low | Equalize stat card heights; add content to the "2012" card |
| 13 | 🟢 Low | Consider adding a visual summary/scorecard element for executive scanning |
