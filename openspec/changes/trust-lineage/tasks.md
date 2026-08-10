## 1. Lineage record shape

- [ ] 1.1 Define the lineage record: figure identity (element, org_unit, period, grain), input observation count, input references, rule applications with version and affected count, conflict references, absent expected inputs, indicator definition reference
- [ ] 1.2 Define how compute lineage from the Hamilton graph and data lineage from observation columns are combined into one record
- [ ] 1.3 Define the aggregate case: how a district-quarter figure's lineage reaches its component facility-month figures
- [ ] 1.4 Confirm every field in the record is derivable from columns `data-validation` and `ingest-mart` already require, adding no new write path
- [ ] 1.5 Define what a figure carries inline (lineage reference, provisional or withheld state) versus what is fetched on follow (the full record)

## 2. Reachability

- [ ] 2.1 Bind the lineage sub-resource to the URL patterns in `openspec/specs/conceptual-model/model.md`, for every addressable metric grain
- [ ] 2.2 Verify a lineage reference resolves with no session state, in a fresh client
- [ ] 2.3 Verify the reference survives being shared to a different reader
- [ ] 2.4 Verify aggregate lineage reaches component figures, and that following the chain terminates at observations

## 3. Survival across surfaces

- [ ] 3.1 Specify how state and lineage reference are carried in a surface that cannot execute code, within the email size ceiling
- [ ] 3.2 Verify state and reference survive every transformation between mart and presentation
- [ ] 3.3 Verify a renderer that cannot express provisional or withheld state omits the figure rather than presenting it as settled
- [ ] 3.4 Measure the size cost of one lineage reference per figure against a realistic edition, and confirm headroom under the clipping threshold

## 4. Gap presentation

- [ ] 4.1 Specify how absent expected inputs are named adjacent to a figure rather than in an appendix
- [ ] 4.2 Specify the visual distinction between unmeasured and a measured zero, in a form that survives a non-executing surface
- [ ] 4.3 Verify a 2024-Q1 figure names both the absent month and the unresolved batch conflict at the point it appears
- [ ] 4.4 Verify a 2024-Q4 figure names its absent month and is not marked contested, since no conflict touches it

## 5. Edition completeness summary

- [ ] 5.1 Specify the summary: expected versus received per source and per period, unresolved conflicts by scope, withheld presentations with reasons
- [ ] 5.2 Verify the summary correctly reports 2024-02 and 2024-12 absent, Q1 incomplete and contested, Q4 incomplete
- [ ] 5.3 Verify a withheld presentation appears with its reason rather than vanishing
- [ ] 5.4 Specify how published defects appear in the edition and link to the figures they affect

## 6. Reproducibility and immutability

- [ ] 6.1 Specify what an edition records to be regenerable: input references, rule versions, resolution references, seeds
- [ ] 6.2 Verify regeneration from a recorded edition produces byte-identical figures
- [ ] 6.3 Verify a stochastic rule reuses its recorded seed and yields the same disposition
- [ ] 6.4 Verify regeneration fails with the missing input named, rather than substituting
- [ ] 6.5 Specify revision semantics: an issued edition is never altered, a correction supersedes, the superseded revision stays retrievable
- [ ] 6.6 Verify a reference to a superseded revision resolves to the figures as originally issued and states that a later revision exists

## 7. Record and hand off

- [ ] 7.1 Confirm the regeneration check is the mechanism by which the named DHO's restart is verified, per ADR 0006
- [ ] 7.2 Answer or explicitly defer the three open questions in `design.md`
- [ ] 7.3 Confirm `ingest-mart` has the column requirements lineage depends on
- [ ] 7.4 Confirm `bulletin-render` has the inline-state, link-per-figure, and summary requirements it inherits
