# Vision review POLISH iteration

_model: moonshotai/kimi-k3 · usage: {'prompt_tokens': 9063, 'completion_tokens': 1978, 'total_tokens': 11041, 'cost': 0.05629041, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.056859, 'upstream_inference_prompt_cost': 0.027189, 'upstream_inference_completions_cost': 0.02967}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}_

# Design Review: Rwanda MoH Digital-Health Landscape Briefing

## 1. VERDICT
**Acceptable** — information-dense and structurally credible, but the systems map and data-flow SVG are too small to read at render size, and several sections are text-heavy where a visual would serve better.

---

## 2. READABILITY

- [ ] **Global body text**: The base font size appears to be ~11–12px at render. For an executive briefing this is too small. Raise base to 14px minimum; section body copy to 13px.
- [ ] **Section 1 · Executive Summary**: Bullet text is dense and long-lined. Max-width appears unconstrained — lines run nearly full container width. Constrain to ~72ch and increase line-height to 1.65.
- [ ] **Section 2 · Systems map SVG**: Text inside boxes is illegibly small at current render width. The SVG viewBox is too wide relative to its rendered size. Either increase the rendered height/width of the SVG container or split the map into two stacked SVGs (National+Facility / Community+External).
- [ ] **Section 4 · Integration & data-flow SVG**: Same problem — node labels and edge labels are sub-8px at render. Unreadable without zoom. This is the most critical readability failure on the page.
- [ ] **Section 5 · Data-protection table**: Table body text is very small (~10px). Status column dots are legible but the obligation descriptions require squinting. Increase cell padding to 10px and font to 12px minimum.
- [ ] **Section 6 · Sources**: Three-column layout at ~9–10px per entry is very dense. Acceptable for a reference section, but entry titles should be at least 11px and the group headers (e.g. "1 · EXECUTIVE SUMMARY / SYSTEMS INVENTORY") need more visual weight — currently they blend into the entries.
- [ ] **KPI stat cards** (row of 8 metrics): Numbers are large and legible — good. But the label text beneath each number is too small and low-contrast (appears ~9px grey on cream). Darken to `#444` and raise to 11px.
- [ ] **Persona journey lanes (Section 3)**: Step card body text is small but the numbered step headers are clear. The "DATA — consumes / produces" strip beneath each lane is useful but rendered in very small grey text — raise to 11px and darken.

---

## 3. VISUALS

- [ ] **Section 2 · Systems map — UPGRADE (highest priority)**: The nine-category, four-tier map is the centrepiece but is functionally unreadable at current size. Options: (a) render it full-width in a scrollable/zoomable container with a min-width of 1200px; (b) split into two side-by-side SVGs at larger scale; (c) provide a simplified "tier overview" diagram above the detailed map. The colour-coded category strip legend below the map is good — keep it, but it cannot compensate for illegible node labels.
- [ ] **Section 4 · Integration & data-flow — UPGRADE**: The OpenHIM bus diagram has the right structure (producers left, bus centre, national right) but edge labels (E1–E32) are unreadable. Add a companion **edge register table** (E1–E32 as rows: source → destination → payload → status) rendered as an actual visible table, not hidden behind a `<details>` toggle. The toggle is fine as a secondary view, but the primary diagram must be legible standalone.
- [ ] **Section 1 · Executive Summary — ADD visual**: The five bullet findings are text-only. Add a simple horizontal bar or dot-strip showing the 13 obligations: 2 met / 6 partial / 5 gap (this data already appears in Section 5's summary strip — surface a mini version in Section 1).
- [ ] **Section 3 · Persona journeys — UPGRADE**: The six lanes are structurally good (numbered steps, system chips). However the system chips (A1, B2, F3 etc.) are not colour-coded to match the nine-category colour strip from Section 2. Apply the same category colours to chips so a reader can cross-reference visually without reading the legend again.
- [ ] **Section 5 · Data-protection table — ADD summary visual**: The "2 met / 6 partial / 5 gap" strip at top is good. Consider adding a per-obligation status icon column that is wider/more scannable — currently the status dots are small and the colour distinction between PARTIAL (orange) and GAP (red) is subtle at small size.
- [ ] **KPI cards row — ADD sparkline or context**: The 8 stat cards are visually strong but isolated. A one-line "so what" caption beneath each (already partially present) should be more prominent — currently in very small grey text.

---

## 4. LAYOUT DEFECTS

- [ ] **Section 2 · Systems map SVG**: The map appears to overflow or be clipped at its container's right edge — the "EXTERNAL / PARTNER TIER" boxes on the far right (I1–I5) appear to run to the very edge with no breathing room. Add 16px internal padding to the SVG container.
- [ ] **Section 4 · Data-flow SVG**: The "SECONDARY USE" box (IeDEA research extract) at bottom-left appears to be partially clipped or very close to the container edge. Verify overflow behaviour.
- [ ] **Section 3 · Persona P5 (CHW) lane**: Step 5 card ("Treat or refer") text appears truncated — "CC referral to the health c" is cut off. Check card overflow.
- [ ] **Section 3 · Persona P6 (Citizen) lane**: Step 5 card ("Billing") text appears truncated — "CBHI/RSSB — manual; link documented" is cut. Same overflow issue.
- [ ] **Section 3 · Persona P1 lane**: Step 5 card ("Draft policy brief") text truncated — "per WHO's Rwanda ca" cut off.
- [ ] **Section 3 · Persona P2 lane**: Step 5 card ("Bulletin") truncated — "and feed NHIC. AI" cut off.
- [ ] **Section 3 · Persona P4 lane**: Step 5 card ("imingo") truncated — "performance rolls into performance contracts" cut.
- [ ] **Section 3 · Persona P3 lane**: Step 5 card ("Monthly upload") truncated — "Aggregate indicators f… Report Tool" cut.
- [ ] **Section 6 · Sources**: Column 3 (groups 3 and 6) appears to have less content than columns 1–2, leaving visible whitespace imbalance at the bottom of the section. Not a defect per se, but consider balancing column heights.
- [ ] **Page footer**: The footer line ("Rendered from out/08-synthesis.md…") is clipped at the right edge — "reviewed also" is the last visible text and appears cut mid-sentence.

---

## 5. CITATIONS

- [ ] **Sources section is present and well-structured** — Section 6 is genuinely credible: grouped by section, numbered entries, publisher + URL + date visible. This is a strength.
- [ ] **In-text citation markers** (e.g. `[1,2]`, `[3,4]`) appear throughout the Executive Summary and other sections — good. However the `[group,source]` convention is explained only in the Section 6 preamble. Add a one-line explainer of the citation convention in the header or Section 1 so first-time readers understand the bracket notation before encountering it.
- [ ] **Edge register (E1–E32)** is behind a `<details>` toggle — the edge-level evidence is a credibility asset. Surface at least a summary count ("32 directed edges, 28 documented, 4 inferred") visibly in Section 4 intro text rather than requiring expansion.
- [ ] **Verified gaps register** is also behind a `<details>` toggle — same recommendation: surface the count of unverifiable items in the Section 5 intro.

---

## Priority-ordered punch-list

1. **Fix Section 4 SVG legibility** — increase rendered size or split; this is the analytical core of the briefing
2. **Fix Section 2 SVG legibility** — same treatment; consider a simplified tier-overview diagram above the detail map
3. **Fix persona lane step-card text truncation** (P1–P6, step 5 cards all appear clipped)
4. **Raise global body font from ~11px to 13–14px**; constrain line length to 72ch
5. **Colour-code persona journey system chips** to match the Section 2 category colour strip
6. **Surface edge-register and gaps-register counts** outside the `<details>` toggles
7. **Fix footer clipping** at right edge
8. **Add mini obligation-status strip** (2/6/5) to Section 1 Executive Summary
9. **Darken and enlarge KPI card labels** (currently ~9px grey on cream)
10. **Add citation convention explainer** to page header or Section 1
