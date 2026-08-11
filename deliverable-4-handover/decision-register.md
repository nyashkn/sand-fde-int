# Decision register: batch conflicts

What happens today when two loads of the same period disagree, what a human decision
looks like, and what is specified but not built. Read `dataflow/gold.py` alongside this
document; nothing here is aspirational without being labelled so.

## What a batch conflict is

Two full-batch loads of the same `(source_system, source_file, period)` land in bronze
with different values for the same facilities. This happened for real in the sample data:
2024-01 and 2024-03 in `clinical_neonatal.csv` each arrived twice, 234 rows, no
timestamp, no submission id, no revision flag distinguishing the two loads, and both
loads are internally consistent (each parses and reconciles cleanly on its own). The
row-index gap between every pair is exactly 117, the facility count, confirming these are
two whole-batch double-loads, not 234 independent per-row corrections.

## What happens today

`pipeline/dataflow/gold.py`, `BATCH_DEFAULT_RULE = "DEFAULT-BATCH-01"`:

```python
resolved = df.drop_duplicates(subset=key, keep="first").copy()
```

The first-occurring row for each key survives; the second is dropped. Every row this
touches is stamped `provisional`, and the rule name is carried into every downstream
figure's lineage record (`observations_resolved.rules_applied`), which is what makes
`DEFAULT-BATCH-01` a fact a reader can check rather than an invisible default. The
bulletin's §4 lineage table reads this column at render time rather than having the rule
name typed into the template, specifically so the two cannot drift; see
`decisions/0011-email-is-a-summary-edition.md` and the commit that fixed a real instance
of that drift.

**"First occurring" is arbitrary and stated as such.** It is not "most recent", not
"most complete", not "most plausible": there is no signal in the source data to prefer
either load, so the rule picks a deterministic, auditable default rather than an
undisclosed one. Nothing in this pipeline calls this resolved, and the bulletin marks
every affected figure `provisional` for exactly this reason, indefinitely, until a
resolution is recorded.

## What a human decision looks like today

There is no mechanism. This is the honest statement, not a gap smoothed over:
`DEFAULT-BATCH-01` runs unconditionally, with no override, no queue, and no way to record
that a person looked at the two loads and picked one. D3 hardening item 1 names this as
the top production-readiness gap for exactly this reason: a quarter where every district
figure is provisional is disclosed, not fixed, and the Ministry has no lever to fix it.

## What is specified but not built

`openspec/changes/data-validation/design.md` and its `tasks.md` §1 specify a
**conflicts table and triage queue**: a finding is written per conflict rather than
auto-resolved, an analyst chooses a batch, the choice is recorded as
`(finding key, decider, decided at, option chosen, stated reason, supersedes)`, and a
recorded resolution reapplies automatically on every subsequent run without re-asking a
human, clearing the provisional mark on exactly the figures it affects.

None of this exists in code today. `data-validation`'s tasks are 0 of 33 checked in
openspec as of this document; the guard tables it also specifies
(`temporal_signal_guard`, `stratification_guard`) ARE built and running, so the change is
partially, not wholly, unimplemented, and this register does not claim otherwise.

**The deliberate design choice that carries over if this is built:** decisions are data,
not control flow. A named DHO's restart of the pipeline must never block on an unresolved
conflict, because a pipeline that waits for human approval is a pipeline the Ministry
cannot restart alone at 2am with no one to call. The specified queue is a table an analyst
works asynchronously, not a gate the batch job stops for. `DEFAULT-BATCH-01` already
follows this principle: it runs unconditionally and completes every quarter, provisional
or not. Any future resolution mechanism inherits that constraint or it is the wrong
mechanism.

## Who decides, once the queue exists

Not specified in this repo beyond the record shape above; a real deployment names this
role during onboarding. The record shape itself (`decider`, `decided at`, `stated reason`)
is designed so that whoever fills the role, the record answers "who decided this and why"
without depending on that person still being reachable.

## Precedent this pipeline already sets

The identity resolution for prefix-ambiguous facility IDs (`NYA` maps to 7 districts,
`NGO` to 2) is resolved the same way conflicts should be: `mart/org_unit_map.csv` is a
small, hand-curated override table, concatenated over a roster derived from
`facilities.csv`, so a person's decision is a durable row in a file rather than a rule
buried in code. The conflicts table, once built, is the same pattern applied to batch
disputes instead of identity disputes.
