## Purpose

Make every published figure interrogable. A reader who doubts a number must be able to
reach the rows behind it, the rules applied to them, what was missing, and who decided
what — without asking anyone, and without the answer depending on a surface that can run code.

## ADDED Requirements

### Requirement: Every presented figure carries a lineage record

A figure presented to a human SHALL have a lineage record containing the inputs it was
derived from and their count, every rule applied and what each changed, every conflict
touching those inputs, every expected input that was absent, and the definition used to
compute it.

#### Scenario: A figure's lineage names its inputs and their count

- **WHEN** a lineage record is retrieved for a presented figure
- **THEN** it states how many input observations the figure was derived from
- **AND** those observations are retrievable

#### Scenario: A rule that changed the figure is named with its effect

- **WHEN** a rule was applied to any input of a figure
- **THEN** the lineage names the rule and its version
- **AND** states how many inputs it affected

#### Scenario: The definition used is recorded, not assumed

- **WHEN** a figure is computed from a named indicator definition
- **THEN** the lineage records which definition and which published standard it came from

#### Scenario: A figure with no lineage record is not presentable

- **WHEN** a renderer requests a figure for which no lineage record exists
- **THEN** the figure SHALL NOT be presented

### Requirement: Lineage is reachable from the figure

Every presented figure SHALL carry a reference to its own lineage record, resolvable by a
reader without prior session state and without knowledge of how the figure was produced.

#### Scenario: A reader reaches lineage from a published figure

- **WHEN** a reader follows the lineage reference attached to a figure
- **THEN** the lineage record for that exact figure, at that exact grain and period, is presented

#### Scenario: The reference survives being shared

- **WHEN** a lineage reference is opened in a fresh session by a different reader
- **THEN** the same lineage record resolves

#### Scenario: Lineage of an aggregate reaches its components

- **WHEN** lineage is retrieved for a figure aggregated from finer-grained figures
- **THEN** the component figures are reachable from it

### Requirement: Provenance is carried, never computed on arrival

Provenance SHALL travel with a figure as data through every hop between the mart and the
reader. A surface SHALL NOT be required to execute code, query a service, or hold session
state in order to present provenance.

#### Scenario: A non-executing surface still presents provenance

- **WHEN** a figure is presented in a surface that cannot execute code
- **THEN** its provisional or withheld state and its lineage reference are present in the
  delivered content

#### Scenario: Provenance is not lost in transformation

- **WHEN** a figure passes through any transformation between mart and presentation
- **THEN** its lineage reference and state are preserved

### Requirement: Gaps are presented, not merely recorded

Where a figure is derived from incomplete input, the presentation SHALL name what is absent
at the point the figure appears — not in an appendix, a footnote elsewhere, or a log.

#### Scenario: A partial period names what is missing beside the figure

- **WHEN** a figure covers a period for which expected inputs were not received
- **THEN** the absent inputs are named adjacent to the figure
- **AND** the figure is not presented as if complete

#### Scenario: An unmeasured entity is visually distinct from a measured zero

- **WHEN** an entity has no observations for a metric that other entities report
- **THEN** it is presented as unmeasured
- **AND** its presentation is distinguishable from an entity whose measured value is zero

#### Scenario: A provisional figure states why it is provisional

- **WHEN** a provisional figure is presented
- **THEN** the unresolved conflict making it provisional is named and reachable

### Requirement: Every edition carries a completeness summary

A published edition SHALL include a summary stating expected versus received inputs per
source and per period, unresolved conflicts grouped by scope, and every presentation
withheld under the analysis-refusal rules with its reason.

#### Scenario: The summary states expected versus received

- **WHEN** an edition is produced
- **THEN** the summary states, per source and per period, what was expected and what was received

#### Scenario: A withheld presentation is disclosed rather than omitted

- **WHEN** a presentation is refused because the data cannot support it
- **THEN** the edition states that it was withheld and why

#### Scenario: Unresolved conflicts are visible to the reader

- **WHEN** an edition is produced while conflicts remain unresolved
- **THEN** the summary states how many, at what scope, and which figures they affect

### Requirement: Known defects are published, not silently corrected

Data quality findings that affect a published figure SHALL be disclosed in the edition. A
defect SHALL NOT be repaired upstream in a way that leaves the reader unaware it existed.

#### Scenario: A defect affecting a figure is disclosed with it

- **WHEN** a finding affects inputs to a published figure
- **THEN** the edition discloses the finding and the figures it touches

#### Scenario: A resolution is disclosed with what it changed

- **WHEN** a human resolution altered which inputs a figure used
- **THEN** the edition states that a resolution was applied and makes the decision reachable

### Requirement: An issued edition is reproducible

An issued edition SHALL be regenerable from its recorded inputs, rule versions, and
resolutions, producing identical figures. Where a rule is stochastic, its seed SHALL be
recorded and reused.

#### Scenario: Regeneration produces identical figures

- **WHEN** an issued edition is regenerated from its recorded inputs, rule versions, and resolutions
- **THEN** every figure is identical to the issued version

#### Scenario: A stochastic rule reuses its recorded seed

- **WHEN** a rule whose outcome depends on randomness is reapplied during regeneration
- **THEN** the recorded seed is reused
- **AND** the disposition is unchanged

#### Scenario: An input that can no longer be reproduced is reported

- **WHEN** regeneration cannot retrieve an input the edition recorded
- **THEN** regeneration SHALL fail with that input named, rather than substitute a value

### Requirement: An issued edition is immutable, corrections are revisions

An issued edition SHALL NOT be altered. A correction SHALL produce a new revision that
supersedes it, and the superseded revision SHALL remain retrievable.

#### Scenario: A correction produces a new revision

- **WHEN** a figure in an issued edition requires correction
- **THEN** a new revision is issued
- **AND** the previous revision remains retrievable in its original form

#### Scenario: A past citation still resolves to what was seen

- **WHEN** a reference to a superseded revision is followed
- **THEN** the figures as originally issued are presented
- **AND** the existence of a later revision is stated
