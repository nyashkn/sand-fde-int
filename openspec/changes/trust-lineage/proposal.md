## Why

An adversarial council found that the MoH Director's complaint is not about throughput.
It is *"I cannot trust any number I am shown."* ADR 0006 accepted that finding and promoted
end-to-end figure traceability from a nice-to-have to a stated requirement of the outcome.

Automating 40 hours of monthly compilation does not address it. A pipeline that produces
clean-looking numbers faster produces *distrusted numbers faster*, and on a quarterly
schedule, with the Ministry's name on them.

The distinction that matters: **"trust me" is not an answer, "check me" is.** A figure the
Director can interrogate, down to the rows behind it, the rules applied, what was missing,
and who decided what, is defensible when challenged in public. A figure that cannot be
interrogated is exactly the object he already refuses.

Two capabilities are now in place and neither closes this. `conceptual-model` established
what a figure resolves *to*, objects, identity, grain, and a URL contract with a
`/lineage` sub-resource. `data-validation` established which checks run, what findings and
conflicts look like, and when a figure becomes provisional. Nothing yet specifies what a
reader is actually *shown*, or guarantees that provenance survives the journey from mart to
inbox.

The sweep in `artifacts/04-data-quality-audit.html` makes this concrete. A Q1 figure is
built on 2 of 3 expected months, both of them duplicated batches under an unresolved
conflict, with no tiebreaker available in the source. Every one of those facts must reach
the reader, not an appendix, not a log.

## What Changes

- Define the **lineage record**: for any presented figure, the complete set of facts needed
  to reconstruct how it came to be, inputs and their count, rules applied and what each
  changed, conflicts touching it, absent expected inputs, and the indicator definition used.
- Require lineage to be **reachable from every figure**, via the `/lineage` sub-resource
  already defined in the URL contract.
- Require that **lineage survives every hop** between mart and reader, including surfaces
  that cannot execute code. An email client runs no JavaScript, so provenance must be
  carried, not computed on arrival.
- Require **gaps to be presented, not merely recorded**, closing a hole in
  `conceptual-model`, which established that incompleteness is a state on the object but
  never required a reader to see it.
- Require every **edition** to carry a completeness summary: expected versus received,
  unresolved conflicts by scope, and any presentation withheld.
- Require **published defects**. Known data quality problems appear in the edition rather
  than being silently corrected upstream.
- Require **reproducibility**: an issued edition can be regenerated from recorded inputs,
  rules, and resolutions, and yields identical figures.
- Require **immutability with revisions**: an issued edition is never edited, so a figure
  quoted last quarter still resolves to what was actually seen.

## Capabilities

### New Capabilities

- `trust-lineage`: the lineage record, its reachability from every figure, its survival
  across rendering surfaces, gap presentation, the edition completeness summary, and the
  reproducibility and immutability guarantees.

### Modified Capabilities

None. `conceptual-model`'s seven requirements remain accurate, it defines what a figure
resolves to and that objects carry state. What a reader is *shown* was never in its scope
(its Non-Goals rule out rendering), so everything here is additive rather than a delta.

## Impact

- **Depends on** `conceptual-model` for object identity, grain, states, and the `/lineage`
  URL pattern; on `data-validation` for finding, conflict, and resolution records.
- **Constrains** `ingest-mart`: silver must retain everything lineage needs, source
  identity, batch, ingest time, rule applications, as columns rather than logs, because a
  log is not addressable from a figure.
- **Constrains** `bulletin-render` hard: every figure must be emitted with its lineage link
  and its provisional or withheld state, in a surface with no scripting and a size ceiling.
- **Constrains** `explore-surface`: the lineage view is a named destination, not a debug
  panel.
- **Supplies** the ADR 0006 handover act. The named DHO's unassisted restart must reproduce
  an identical edition, which is only checkable if reproducibility is specified here.
- **Inputs**: `decisions/0006-problem-a-plus-handover-act.md`,
  `artifacts/03-opportunity-map-council-verdict.html`,
  `artifacts/04-data-quality-audit.html`, `openspec/specs/conceptual-model/model.md`.
