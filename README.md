# Sand Technologies, Forward Deployed Engineer Assignment

Working repository for the FDE recruitment assignment. This is deliberately a **working**
repo, not a polished submission folder: the research, the dead ends, the decision log and the
throwaway prototypes are all here, because how the answer was reached matters as much as the
answer.

The four deliverables map 1:1 to the folders below.

---

## Navigating this repo

| Folder | What's in it |
|---|---|
| `assignment/` | The brief as issued, plus the five provided CSVs. Inputs, not authored by me. |
| `research/` | What I learned before deciding anything. Product research, source videos, the analysis script. |
| `decisions/` | Numbered decision records. Every non-obvious call, with the reasoning and what would reverse it. |
| `artifacts/` | Rendered HTML visuals referenced from the written docs. Open them in a browser. |
| `deliverable-1-scoping/` | **D1**, discovery process and problem selection. |
| `deliverable-2-prototype/` | **D2**, solution design + working bulletin prototype. |
| `deliverable-3-hardening/` | **D3**, top 5 production-readiness gaps. |
| `deliverable-4-handover/` | **D4**, runbook, data contract, decision register, exit criteria. |

**Start here if you're reviewing:** `deliverable-1-scoping/` for the reasoning,
`deliverable-2-prototype/` for the code, `deliverable-4-handover/` for whether this
survives without me, `decisions/` if you want to know why something is the way it is.

---

## Provenance discipline

Sand publishes no technical documentation for HealthOS. Everything in `research/` is
reconstructed from public sources, and every claim carries an evidence grade:

- **Confirmed**, directly observed in a Sand video frame, or stated in a published source
  (Rwanda MoH release, AWS Marketplace listing, Sand's own job postings).
- **Inferred**, a reasonable extrapolation from the above, explicitly marked `[INFERENCE]`.
- **Unevidenced**, claimed in marketing but not corroborated anywhere. Named as such.

The most consequential finding: the product's real on-screen name is **`Bluelake Admin`** at
`bluelake.rhos.africa`, not "HealthOS", "RHOS" or "Symmetri", none of which appear in the
product UI. The assignment's five product names map onto real capabilities but are not
Sand's public branding. See `research/sand-product-research.md` §7.1.

---

## Running things

### Videos (Git LFS)

The three source videos in `research/videos/` are tracked with Git LFS. To get them:

```bash
git lfs install
git lfs pull
```

Without LFS you'll see pointer files instead of `.mp4`s. The written analysis in
`research/sand-product-research.md` §7 stands on its own, the videos are there for
verification, not required reading.

### Video analysis script

```bash
export OPENROUTER_API_KEY=...
python3 research/analyze-video.py research/videos/rhos-blue-room.mp4
```

Sends the file to `meta/muse-spark-1.2` (native video input) and prints the raw JSON
response. Note the 50 MB per-file cap and the gateway timeouts on longer clips , 
documented in `research/sand-product-research.md` §7.4.

### Prototype

`deliverable-4-handover/runbook.md` is the authoritative sequence, kept accurate because
it is run, not just read: `uv sync`, `run.py`, `bun install`, `bun run publish`,
`bun run verify`. `deliverable-2-prototype/README.md` covers what got built and why.

---

## Artifacts

| File | What it shows |
|---|---|
| `artifacts/01-bluelake-admin-ux-walkthrough.html` | Click-through reconstruction of the real Bluelake Admin UI, 4 screens, rebuilt from video frames. |
| `artifacts/02-modular-architecture-persona-map.html` | Every assignment module placed on the layered architecture, with a persona access matrix and evidence grades. |
| `artifacts/03-opportunity-map-council-verdict.html` | Problems A/B/C mapped to opportunities, the adversarial council's tally, and the kill criteria behind the D1 verdict. |
| `artifacts/04-data-quality-audit.html` | The full data-quality sweep: fabricated GPS, the batch-duplicate defect, the ecological-fallacy correlation, every finding behind D2's structural guards. |
| `artifacts/05-bulletin-critique.md` | The D2 §6.6 design critique: measured WCAG contrast failures and a real layout bug caught by checking the property that would make a fix inert, not just the property it set. |

The four HTML files are self-contained, no build step, no assets, open directly in a
browser. `05` is markdown; it documents a critique of rendered output rather than being
one itself.

---

## Assumptions

Collected here so they're easy to challenge in one place; each is restated in context where
it's load-bearing.

1. **Rwanda is the deployment country.** The brief says "one of our expansion countries
   (i.e. Rwanda)", and the provided data uses Rwandan facility names, districts and RWF.
   Treated as Rwanda throughout.
2. **The provided CSVs are the DHIS2-like data referenced in Deliverable 2**, even though
   they are neonatal/maternal-focused rather than a general DHIS2 export.
3. **The five named Sand products are capability labels, not literal product SKUs.** Justified
   in `research/sand-product-research.md`; the architecture maps them to what actually exists.
4. **No access to a real Sand or MoH environment.** Everything is built against the provided
   data and public sources only.
