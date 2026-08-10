## Context

See `proposal.md`, Why. The finding inventory is `artifacts/04-data-quality-audit.html`.

Constraints that shape the approach:

- Hamilton is the batch engine (ADR 0008). Its DAG is derived from function parameter names,
  and `@check_output` attaches validation to the node it guards. That makes "every check is
  registered" enforceable by construction rather than by convention.
- The named-DHO restart test from ADR 0006 rules out anything that can wedge. A validation
  layer that halts on a failing check produces no bulletin, which is worse than a bulletin
  with a labelled provisional figure.
- 17 findings across 5 scopes are already known. The registry is being designed against a
  real inventory, not an imagined one, so the scope enum and disposition set can be closed
  rather than open-ended.
- Two findings are not row defects at all, they invalidate a *class of analysis*. Nothing in
  a conventional row-level validation framework expresses that.

## Goals / Non-Goals

**Goals:**

- One mechanism covering all five observed scopes: row, column, batch, cross-file, file.
- Ingest-time execution with zero blocking, so the pipeline is always runnable.
- Findings and resolutions as queryable data reachable from any figure they touch.
- Structural refusal of the two unsupported analyses, enforced rather than remembered.

**Non-Goals:**

- Data repair. Nothing here corrects a value; that is a human decision recorded as data.
- The triage user interface. This fixes the record shape; `explore-surface` renders it.
- Statistical validity of the checks as epidemiology. These are data-integrity checks.
- Schema validation of arriving files. That is `ingest-mart`'s boundary.

## Decisions

**Checks are Hamilton nodes with `@check_output`, not a separate validation pass.**
A check lives on the node whose output it guards, so it cannot be skipped by running the
pipeline differently, and its position in the lineage graph is its scope. *Alternative
considered:* a standalone validation stage after load. Rejected, it can be bypassed, and it
loses the lineage attachment that makes a finding reachable from a figure.

**Findings and resolutions are two tables, never one.**
Findings are machine-produced and immutable. Resolutions are human-produced and append-only,
keyed to a finding, with `supersedes` for a changed mind. *Alternative considered:* a mutable
status column on the finding. Rejected, it destroys the decision history, which is the part
that answers *"why is this number what it is."*

**Provisional is a column that propagates, not a flag computed at render time.**
Any aggregate over a provisional input is provisional, and the count of provisional inputs
travels with it. *Alternative considered:* recomputing provisional state in the renderer.
Rejected, two renderers would disagree, and the email render (no JavaScript) is the one
least able to compute it.

**Batch-scope conflicts are first-class, not 234 row conflicts sharing a reason.**
The duplicate finding is a property of the load, so the resolution attaches to the load.
*Alternative considered:* per-record conflicts with a bulk-resolve action. Rejected, it
presents an analyst with 234 decisions where there are 2, and invites resolving them
inconsistently.

**Analysis refusal is a check on the *series*, not on the presentation.**
The temporal-signal guard tests the series against a within-entity permutation of itself and
records the result; the renderer reads that result. The stratification guard requires any
association presented as explanatory to declare the variable it was stratified against.
*Alternative considered:* a documented rule that reviewers enforce. Rejected, this
engagement has already demonstrated that a reviewer, having explicitly warned against the
ecological fallacy, then committed it three messages later. A rule a human must remember is
not a control.

**Clean results are recorded with their population.**
`ran, examined N, found 0` is a different fact from silence, and it is what makes the defect
list credible. *Alternative considered:* logging only failures. Rejected, it makes a broken
check indistinguishable from a clean dataset.

## Risks / Trade-offs

- **Registry becomes bureaucratic and slows real work** → the scope and disposition enums are
  closed, derived from 17 real findings; adding a check is one decorator plus one registry row.
- **Provisional labelling everywhere causes alarm fatigue and gets ignored** → provisional is
  reserved for unresolved *conflicts*, not for every informational finding; the 2 batch
  decisions clear most of it at once.
- **Analysis refusal blocks a required bulletin panel** → that is the intended behaviour, and
  the refusal is disclosed in the edition rather than the panel silently disappearing.
- **Permutation-based temporal guard is stochastic** → fix the seed and record it with the
  result, so the same input yields the same disposition.
- **Retaining rejected rows grows bronze** → the sample is kilobytes; revisit if a real
  deployment makes it material.
- **The stratification guard needs to know which variable to stratify on** → it does not infer
  it; the declaration is required from whoever presents the association, and an undeclared
  association is refused.

## Migration Plan

None, no implementation exists. DUP-01 as previously drafted was never implemented, so its
withdrawal is a documentation change, recorded in the proposal as BREAKING for traceability.

## Open Questions

- The permutation-test threshold for declaring "no temporal signal". The observed case is
  unambiguous (true 0.867 versus a null of 0.876±0.004, the null exceeds the true value), so
  any sane threshold decides it identically. Deferrable until a borderline series appears.
- Whether informational findings should ever surface in the triage queue or only in the
  edition summary. Affects queue volume, not the record shape.
