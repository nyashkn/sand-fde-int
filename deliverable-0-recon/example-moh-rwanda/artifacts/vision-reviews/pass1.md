# Vision review PASS1

_model: moonshotai/kimi-k3 · usage: {'prompt_tokens': 10084, 'completion_tokens': 1305, 'total_tokens': 11389, 'cost': 0.04932873, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.049827, 'upstream_inference_prompt_cost': 0.030252, 'upstream_inference_completions_cost': 0.019575}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}_

1. **VERDICT:** **Acceptable** — information-dense and structurally sound, but body text contrast is too low for executive readability and the systems map is visually overwhelming at 100% zoom.

2. **READABILITY:**
   - **Global body text:** The primary content uses a low-contrast grey (`#666` or similar) on cream/off-white backgrounds. This fails WCAG AA for normal text. **Fix:** Darken body text to `#333` or darker; increase font weight to 400/500.
   - **Systems map labels (§2):** Text inside tier boxes is small (likely 10-11px) and low-contrast against the cream background. **Fix:** Increase label font size to 12px minimum and darken to `#222`.
   - **Persona journey lanes (§3):** Step descriptions use light grey text on slightly darker cream cards. **Fix:** Darken step text to `#333` and increase card padding from ~8px to 16px for breathing room.
   - **Data-protection table (§5):** Status column text ("PARTIAL", "GAP") is readable, but the "MoH Stack Today" column body text is too light. **Fix:** Darken to `#333`.
   - **Line length:** Executive summary bullets (§1) run too wide (likely >100 characters). **Fix:** Constrain paragraph width to 65-75 characters or increase font size to reduce characters per line.
   - **Visual hierarchy:** Section headers (§1-§6) are clear, but the "Evidence Base" box and stat cards (42+, 58,567, etc.) compete for attention with the map. **Fix:** Reduce stat card border weight or background saturation to push them back visually.

3. **VISUALS:**
   - **Systems map (§2):** Information-dense but visually noisy. The dashed borders for "planned/unverified" are hard to distinguish from solid lines at a glance. **Fix:** Add a clear legend swatch showing "Documented (solid)" vs. "Planned (dashed)" vs. "Defunct (dotted)" with 20px samples; increase spacing between the External tier and National tier to reduce arrow crossing.
   - **Integration/data-flow (§4):** The OpenHIM bus diagram is clear but the edge labels (E1, E7, E8, etc.) are small and crowded near the center. **Fix:** Add a numbered edge list beside the diagram or increase label font size; consider color-coding edges by data type (red for alerts, blue for clinical, green for aggregates).
   - **Persona journeys (§3):** Currently text-heavy cards. **Upgrade:** Convert each persona lane into a horizontal timeline with numbered step nodes (1→2→3→4→5) and system chips (A1, B2, etc.) visually connected by lines, rather than stacked cards.
   - **Data-protection posture (§5):** The table is functional but dry. **Upgrade:** Convert the status column into a horizontal stacked bar chart showing the 2/6/5 distribution (Met/Partial/Gap) with icons; add a color-coded heat-map column for quick scanning.
   - **Missing visual:** No high-level "Rwanda Digital Health Architecture" overview diagram exists before §2. **Add:** A simplified 3-tier stack diagram (Community → Facility → National) in the Executive Summary to orient readers before the complex §2 map.

4. **LAYOUT DEFECTS:**
   - **Systems map overflow:** The External tier (I1-I6) appears to extend close to the right edge; verify no horizontal clipping occurs on 1440px viewports.
   - **Persona card alignment:** In §3, the step cards within each persona lane appear to have inconsistent heights (step 5 cards look shorter than step 1). **Fix:** Set `align-items: stretch` on the flex container or enforce min-height.
   - **Data-protection table:** The "Benchmark Pattern" column text wraps awkwardly ("Sand · Helium · Zipline" splits mid-word in some rows). **Fix:** Increase column width or reduce font size to prevent mid-word breaks.
   - **Sources section (§6):** The two-column layout for references 1-12 appears cramped; the right column (refs 7-12) has tighter line-height than the left. **Fix:** Standardize line-height to 1.5 across both columns.

5. **CITATIONS:**
   - **Present and credible.** §6 "Sources & further reading" is visibly populated with 12+ specific references (RHIE reports, WHO CPCD, DHIS2 docs, Zipline newsroom, etc.) grouped by theme. Inline citations like `[1,1]` and `[5,8]` appear throughout the text. **Fix:** Make the inline citation markers superscript and slightly darker (`#555`) to improve scannability; ensure the Sources section uses a hanging indent for wrapped reference titles.

---

### Punch-list (ordered by impact)

- [ ] **Critical:** Darken all body text from grey (`#666`) to `#333` for WCAG AA compliance (affects §1-§5).
- [ ] **High:** Increase padding in §3 persona step cards to 16px and darken step text to `#333`.
- [ ] **High:** Add a prominent legend to §2 Systems Map distinguishing solid (documented) vs. dashed (planned) vs. dotted (defunct) borders with 20px visual samples.
- [ ] **Medium:** Convert §5 Data-protection status column into a visual stacked bar (2 Met / 6 Partial / 5 Gap) with color coding.
- [ ] **Medium:** Add a simplified 3-tier architecture overview diagram to §1 before the complex §2 map.
- [ ] **Medium:** Standardize line-height in §6 Sources columns to 1.5 and add hanging indents for reference titles.
- [ ] **Low:** Constrain §1 Executive Summary paragraph width to 70 characters for readability.
- [ ] **Low:** Increase font size of edge labels (E1-E32) in §4 Integration diagram to 11px minimum.
