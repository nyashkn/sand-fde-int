---
name: html-artifact
description: Render the final research synthesis as a single self-contained HTML page matching the Sand "modular architecture + persona map" reference style. Load this in the visual node before writing the artifact.
---

# html-artifact

Produce one **self-contained** HTML file: all CSS inline in a `<style>` block, all diagrams as
inline **SVG**, no external scripts, fonts, or image URLs. It must open correctly from `file://`.

## Match the reference

Before writing, **read the reference artifact** and mirror its layout, palette, typography, and the
way it presents modularity + persona journeys:

```
../product-docs/artifacts/02-modular-architecture-persona-map.html
```

(Path is relative to the run working_dir. Use `read_file`.) Reuse its structural conventions —
section rhythm, card/lane treatment, color roles, legend style — so this artifact reads as a
sibling of the existing Sand product docs, not a foreign template.

## Required sections (in order)

1. **Executive summary** — what the Rwanda MoH digital-health landscape is, in ~5 bullets.
2. **Systems map** — inline SVG: nodes = systems (grouped internal vs external / by tier:
   national / district / facility / community), edges = relationships. Legend for node types.
3. **Persona journeys** — one horizontal lane per persona (policy, epidemiology, clinician,
   district health officer, CHW, citizen): the steps each takes and the systems they touch.
4. **Integration & data-flow** — inline SVG: directed edges `source -> destination : payload`
   across the HIE / interop layer (FHIR, DHIS2, ADX, registries).
5. **Data-protection posture** — table mapping Rwanda Law 058/2021 obligations to how each
   system / benchmark (incl. Sand-like platforms) satisfies them; flag gaps.

## Rules

- **Source only from `out/08-synthesis.md`.** Do not invent systems, vendors, or edges not present
  there. If the synthesis flags a gap, render it visibly as a gap (e.g. dashed node / "unverified"
  tag) — never paper over it.
- Keep it accessible: semantic headings, sufficient contrast, `<title>`, alt/`<desc>` on SVGs.
- Responsive-ish: readable at 1280px and on a laptop; no horizontal scroll for text.
- Write to the path in your node prompt (`out/moh-rwanda-architecture.html`). After writing, verify
  it exists and is substantial (a real page, not a stub).
