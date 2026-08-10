# Worked example — Rwanda MoH recon

The recon pipeline run against the Rwanda Ministry of Health digital-health landscape. This is the
concrete output that produced Deliverable 0's artifact, kept for audit and reproduction.

## Contents

```
artifacts/
  moh-rwanda-architecture.html          # FINAL — v2 structural redesign: SVG persona swimlanes +
                                        #   persona×systems access matrix, tiered diagrams, 45 links
  moh-rwanda-architecture.v1-dense.html # v1 — link-rich but text-dense (the redesign's "before")
  moh-rwanda-architecture.baseline.html # first render, pre-links
  synthesis.md                          # the single sourced model the artifact renders from (166 citations)
  sources.md                            # the 25–45 load-bearing sources, grouped by section
  lanes/00..07-*.md                     # the seven MECE research lanes + scope
  vision-reviews/                       # what the vision model said each pass
    pass0.md        # baseline: "Acceptable"
    pass1.md        # after link-embed
    pass2-final.md  # after two kimi refine passes: "Weak" (density regression)
    latest.md       # after the subtractive polish: "Acceptable"
  screenshots/
    baseline.png    # what the vision model saw first
    final.png       # what it scored "Acceptable"
workflows-as-run/                       # the exact .fabro/.toml that ran (incl. two throwaway smokes)
```

## What ran, and what it cost

| Run | Workflow | Outcome | Cost |
|---|---|---|---|
| `01KZHWDZ…` | `moh-rwanda` (recon) | 8 lane files + first artifact | $0.31 |
| `01KZN4B3…` | `refine` | 45 links + 88 citations; verdict regressed to **Weak** | $4.24 |
| `01KZN8XD…` | `polish` | subtractive pass on flash; verdict **Weak → Acceptable** | $0.05 |

After `polish`, the artifact was cited and readable but still a text-dense single column — the
refine/polish loop can restyle but not restructure. A **v2 structural redesign** (built fresh from
`synthesis.md` against the reference exemplar `artifacts/02-…persona-map.html`) rebuilt the personas
as **SVG swimlane journeys** plus a **persona×systems access matrix**, added a tiered systems-map
SVG with a legend, and cut the page from 102 KB back to 65 KB — same 45 sources. Verdict holds at
*Acceptable* ("strong analyst draft"); the residual gap to "polished executive" is typographic
fine-tuning best done by hand, not another automated pass. `moh-rwanda-architecture.v1-dense.html`
is kept as the before.

Two earlier `polish` attempts failed first and were superseded: one was killed before doing work,
one hit the OpenRouter credit wall on kimi (`max_output=131072` reserves ~$2/request). Both are
written up in [`../pipeline/README.md`](../pipeline/README.md) gotchas 6–7.

## The findings, grounded

The lanes surfaced real, sourced systems — DHIS2/HMIS, OpenMRS EMR, e-LMIS, RapidSMS→RapidPro,
the Rwanda Health Information Exchange (RHIE) on OpenHIE/OpenHIM with HAPI FHIR registries, and the
National Health Insurance (NHIC, launched Apr 2025) — and the data-protection lane covers Law
No. 058/2021 and the NCSA. `06-integration.md` came out thin (the lane file truncated); its content
survives in `synthesis.md`, which the artifact renders from. Confidence is flagged per section in
each lane file rather than smoothed over.

## Reproduce

The `workflows-as-run/` graphs are target-specific (Rwanda MoH baked into the prompts). To re-run,
point them at a fresh `working_dir` and start the server; the generalized, target-agnostic versions
are in [`../pipeline/workflows/`](../pipeline/workflows/).
