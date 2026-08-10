# Vision review V2b darker text

_model: moonshotai/kimi-k3 · usage: {'prompt_tokens': 9332, 'completion_tokens': 1296, 'total_tokens': 10628, 'cost': 0.04696164, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.047436, 'upstream_inference_prompt_cost': 0.027996, 'upstream_inference_completions_cost': 0.01944}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}_

## 1. VERDICT

**Acceptable** — information-dense and credible, but undermined by small body text, low-contrast secondary text, and cramped diagrams that strain readability at typical viewing distances.

---

## 2. READABILITY

| Section | Issue | Fix |
|---------|-------|-----|
| **Global body text** | ~11–12px equivalent; grey `#666` on cream `#faf9f7` fails WCAG AA for sustained reading | Bump to 14px minimum; darken to `#333` or `#2d2d2d` |
| **Section 02 Systems map** | Box labels (`B1 OpenMRS`, `F3 Client Reg`) are ~9px; tier headers (`EXTERNAL / PARTNER`) are low-contrast grey | Increase box text to 11px bold; darken tier headers to `#444` |
| **Section 03 Persona matrix** | Row labels (`National policy / planning`) are small and grey; category headers (`A REPORT`, `B EMR`) are tiny uppercase | 13px minimum for row labels; add `letter-spacing: 0.05em` to headers |
| **Section 04 Persona journeys** | Lane labels (`National policy analyst`) are readable, but stage chips (`Morning briefing`, `Trace a signal`) are ~9px with low contrast | Increase chip text to 11px; add 8px internal padding |
| **Section 05 Integration flow** | Edge labels (`UPID lookup`, `lab order`) are ~8px, dashed lines are faint | 10px minimum for edge labels; increase stroke width to 1.5px |
| **Section 06 Data-protection table** | Status pills (`DOCUMENTED`, `PARTIAL`, `GAP`) are small; description text is dense | 12px for descriptions; increase row padding to 12px |
| **Section 07 Sources** | Reference text is ~10px; two-column layout creates long line lengths | 12px; consider single-column with hanging indents |

---

## 3. VISUALS

| Current | Assessment | Recommendation |
|---------|-----------|----------------|
| **Systems map (02)** | Functional but flat; boxes are uniform, no visual encoding of "where each system runs" beyond tier bands | **Upgrade**: add subtle background tint per tier (external=warm grey, national=cool blue, facility=green, community=amber); add small icons for system type (database, mobile, API) |
| **Persona matrix (03)** | Dots/diamonds are clear, but no summary view | **Add**: a "coverage heatmap" strip below showing which categories have strongest persona engagement |
| **Persona journeys (04)** | Good lane structure; outcome chips (`MINISTERIAL BRIEF`, `EPI BULLETIN`) are strong | **Upgrade**: add small loop-back arrows for the two "live HIS" loops mentioned in text (`CHW→eIDSR`, `EMR→DHIS2→NHIC`) — currently only described in caption |
| **Integration flow (05)** | Clear left-to-right flow; mediator box is well-emphasised | **Add**: a small legend for line styles (solid vs dashed) is present but tiny — enlarge; consider colour-coding edges by data type (clinical=blue, lab=green, community=orange) |
| **Data-protection table (06)** | Text-heavy; status is scannable via pills | **Add**: a summary donut or stacked bar showing 3 documented / 4 partial / 5 gap at a glance |
| **Missing** | No timeline visual | **Add**: a horizontal timeline in Section 01 showing `2012 DHIS2 → 2025 NHIC launch → 2026 targets` |

---

## 4. LAYOUT DEFECTS

- [ ] **Section 02**: `monthly aggregate` label overlaps the arrow between National and Facility tiers — reposition or add white background
- [ ] **Section 02**: `F1 RHIE / F2 OpenHIM` box is wider than siblings, breaking grid rhythm — equalise widths or make it intentionally prominent
- [ ] **Section 04**: Journey lanes have uneven left margins (P1–P4 indented, P5–P6 flush) — align all persona labels to same x-position
- [ ] **Section 05**: `F9 CRVS` box is orphaned at bottom left with excessive whitespace above — tighten vertical rhythm
- [ ] **Section 07**: Two-column source list has uneven column heights (left column ends at item 12, right at 8) — balance or use CSS columns with `column-fill: balance`

---

## 5. CITATIONS

- [x] **Sources section present** — 45 numbered references, grouped by section, with in-body superscripts
- [ ] **Superscript legibility** — superscripts (`¹`, `²`) are ~7px and low-contrast; increase to 9px and darken
- [ ] **Link affordance** — unclear if sources are clickable; add `text-decoration: underline` or colour to indicate hyperlinks
- [ ] **Access dates** — no "accessed [date]" stamps; add for credibility on web sources

---

## PUNCH-LIST (ordered by impact)

1. **Global**: Increase body text from ~11px to 14px; darken grey text from `#666` to `#333`
2. **Section 02**: Fix `monthly aggregate` label overlap; increase box label size to 11px
3. **Section 04**: Align persona lane left margins; increase stage chip text to 11px
4. **Section 05**: Enlarge edge labels to 10px; thicken dashed lines
5. **Section 06**: Add summary visual (donut/bar) for status counts
6. **Section 01**: Add timeline visual for 2012–2026 milestones
7. **Section 07**: Increase source text to 12px; add link styling and access dates
8. **Global**: Add tier background tints to systems map; enlarge superscripts to 9px
