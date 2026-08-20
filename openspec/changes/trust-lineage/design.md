## Context

See `proposal.md`, Why.

What is already fixed and must not be re-decided here:

- `conceptual-model` gives objects, identity, grain, states, and the URL contract. Lineage
  is a **sub-resource**, `/metric/nmr/district/nyanza/2024-Q3/lineage`, not a new address
  space.
- `data-validation` gives findings, conflicts, resolutions, and the rule that provisional
  state propagates through aggregation. Lineage *reads* those records; it does not define
  them.
- ADR 0008 fixes the batch engine as Hamilton, whose DAG is derived from function parameter
  names. Compute lineage therefore exists whether or not anyone asks for it.

What makes this hard: the primary delivery surface is **HTML embedded in email**. No
JavaScript, no round trip, inline CSS, table layout, and Gmail clips past roughly 102KB.
Any design that computes provenance at render time fails there, and email is the surface the
Director actually reads.

The sample makes the requirement concrete rather than abstract. A 2024-Q1 figure sits on 2
of 3 expected months, both duplicated batches under an unresolved conflict with no tiebreaker
available in the source. All of that has to reach the page.

## Goals / Non-Goals

**Goals:**

- One lineage record shape covering every figure, from a facility-month to a district-quarter.
- Reachability that survives email, sharing, and a reader with no session.
- Gaps and provisional state visible at the figure, not in an appendix.
- Reproducibility strong enough that the named DHO's restart is checkable.

**Non-Goals:**

- Defining findings, conflicts, or resolutions. Owned by `data-validation`.
- Object identity, grain, or URL patterns. Owned by `conceptual-model`.
- The visual design of the lineage view. Owned by `bulletin-render` and `explore-surface`.
- Audit logging of system access. This is data provenance, not security audit.

## Decisions

**Lineage is a projection over recorded columns, not a separate log.**
Every fact lineage needs, source, batch, ingest time, rule applications, conflict
references, is already a column on the observation rows, per `data-validation`. Lineage
assembles them. *Alternative considered:* an append-only lineage log written alongside the
pipeline. Rejected, a log is not addressable from a figure, drifts from the data it
describes, and would need its own retention story.

**Compute lineage comes from Hamilton's graph; data lineage comes from the columns. Both are
required, neither substitutes.**
Hamilton answers *which function produced this*; the columns answer *which rows, which
batch, which rule*. *Alternative considered:* relying on Hamilton's graph alone. Rejected,
it describes the pipeline, not the data that went through it, and cannot say that Q1 is
missing February.

**Every figure carries its lineage reference and state inline; the lineage *record* is
fetched only when followed.**
The email carries the link and the provisional/withheld state as delivered content. It does
not carry the full record. *Alternative considered:* inlining the whole lineage record in the
email. Rejected on the size ceiling, 117 facilities with full provenance would clip.
*Alternative considered:* computing state client-side. Rejected, email cannot execute code.

**Reproducibility is pinned by recording rule *versions* and *seeds*, not by freezing code.**
An edition records which rule versions and which seeds produced it, so regeneration is
verifiable without preserving a binary. *Alternative considered:* container digests.
Rejected, it fails the ADR 0006 dependency test; the named DHO should not need a registry
to check a number.

**Regeneration fails loudly on a missing input rather than substituting.**
A silent substitution during regeneration would make an unreproducible edition look
reproducible, which is worse than no reproducibility claim at all.

**Immutability with revisions, not correction in place.**
A Minister who quoted a figure last quarter must still be able to reach what they saw.
*Alternative considered:* correcting in place with a change log. Rejected, the log tells you
a number changed but not what the earlier audience actually saw.

**Defects are published in the edition, not fixed silently upstream.**
*Alternative considered:* cleaning defects before publication and noting them internally.
Rejected, this is the whole thesis. A bulletin that opens with what was found wrong and how
it was handled earns more trust than one producing clean-looking numbers, and it inoculates
against the defect being discovered later by someone else.

## Risks / Trade-offs

- **Lineage links in email look like tracking pixels or phishing** → same origin as the
  bulletin, human-readable paths, no redirect service.
- **Every figure carrying a link doubles the email's element count against a hard size
  ceiling** → link per figure, not per cell; the completeness summary is one block, not
  per-row annotations.
- **Disclosing defects undermines confidence in the bulletin** → the opposite is the wager,
  and it is the council's finding: the Director already distrusts clean numbers. Untested
  until it reaches a real reader, and worth naming as an assumption rather than a certainty.
- **Reproducibility guarantees decay as rules evolve** → versions are recorded per edition,
  so an old edition is reproducible under the rules that produced it, not under current ones.
- **A lineage view is a second surface to build and maintain** → it is a projection with a
  fixed shape, so one implementation serves every figure.
- **Provisional labelling everywhere causes fatigue** → provisional attaches only to
  unresolved *conflicts*; the sample's entire provisional load clears with 2 batch decisions.

## Migration Plan

None, no implementation exists. `ingest-mart` inherits the requirement that lineage inputs
are columns rather than logs; `bulletin-render` inherits inline state plus link, with the
record fetched on follow.

## Open Questions

- Whether the lineage view is public or requires authentication. It contains no
  patient-level data, and a public view maximises the "check me" property, but that is the
  Ministry's decision, not ours. Deferrable: it changes deployment, not the record shape.
- How long superseded revisions are retained. Immutability implies indefinitely; storage
  says otherwise eventually. Deferrable at this scale.
- Whether the completeness summary opens or closes the edition. A presentation decision,
  owned by `bulletin-render`, though opening with it is the stronger trust signal.
