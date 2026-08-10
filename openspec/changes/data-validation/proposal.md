## Why

The MoH Director's stated problem is *"I cannot trust any number I am shown."* That is
unfalsifiable as posed, and so it never gets fixed. A validation layer converts it into
something measurable: a named check, a number, a denominator, and a disposition.

The sweep recorded in `artifacts/04-data-quality-audit.html` found 4 blockers and 13
material contradictions in 117 facilities and 1,404 facility-months — every one of them
reproducible by a one-line check. It also found 31 checks clean, which is what makes the
defect list credible rather than a fishing expedition.

Two of those findings change what can be built at all:

- **No genuine month-to-month signal exists.** A within-facility shuffle reproduces the
  observed autocorrelation exactly (true 0.867, shuffled null 0.876±0.004). The brief
  requires *"trend analysis vs previous quarters"*; on this data any period-over-period
  delta is noise.
- **The capability→outcome correlation is tier-confounded.** Pooled r=−0.844 collapses to
  +0.042 / +0.111 / +0.144 within tier. A "what drives mortality" panel built on the pooled
  figure would report tier membership as causation.

Neither is a data-cleaning problem. Both are claims the system must be structurally unable
to make. That is validation's job, not a reviewer's memory.

## What Changes

- Introduce a **check registry**: every validation is a named, versioned rule with a stated
  scope, severity, and disposition. No anonymous cleaning steps anywhere in the pipeline.
- Checks run **at ingest**, not as a separate audit pass, and their results are recorded as
  data against the rows they examined.
- A failing check **never silently mutates or drops a row**. It records a finding and, where
  the rule cannot be auto-resolved, raises a conflict for human triage.
- Figures derived from unresolved conflicts are marked **provisional** and carry that state
  into every rendering.
- **BREAKING for DUP-01** (previously drafted as "keep the latest submission"). That rule is
  withdrawn: nothing in the source establishes row order as submission order, both rows are
  always internally consistent, and there is no directional bias (113 vs 119 of 234). The
  replacement resolves at *batch* scope and defers to a human — 2 decisions, not 234.
- Introduce **structural guards**: checks that block a class of *analysis*, not just a class
  of row. A correlation that does not survive stratification, and a period-over-period delta
  on a series with no temporal signal, must both be refused at source.
- Every check ships with the **clean case recorded too**, so a passing dataset produces
  positive evidence rather than silence.

## Capabilities

### New Capabilities

- `data-validation`: the check registry, the disposition rules for what a failing check may
  and may not do, the conflict records it raises, and the provisional marking that follows
  an unresolved conflict.

### Modified Capabilities

None. `conceptual-model` is still in proposal and not yet archived, so there is no existing
spec to delta against.

## Impact

- **Depends on** `conceptual-model` for object identity, grain, and the unmeasured-versus-zero
  distinction. Checks attach to objects; scope is meaningless without them.
- **Constrains** `ingest-mart`: bronze must retain rows a check rejected, since a rejected row
  is evidence, not garbage. Silver carries the finding and provisional columns.
- **Constrains** `bulletin-render`: a provisional figure must be renderable *as* provisional.
  A renderer that cannot express the state cannot present the figure.
- **Constrains** `explore-surface`: the triage queue is a surface over conflict records, so
  its shape is fixed here.
- **Supplies** the handover artifact. The check registry, not the cleaned data, is what
  outlives the engagement — it generalises to the next quarter's file and the next country's.
- **Inputs**: `artifacts/04-data-quality-audit.html` (17 findings, 31 clean checks, each with
  a runnable reproduction), `decisions/0008-technical-stack.md`, `decisions/0006-problem-a-plus-handover-act.md`.
