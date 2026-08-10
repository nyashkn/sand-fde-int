## Purpose

Turn "our data is a mess" into a standing measurement: a registry of named checks that run
at ingest, record findings as data, refuse analyses the data cannot support, and hand
anything they cannot decide to a human without ever blocking the pipeline.

## ADDED Requirements

### Requirement: Every check is named, versioned, and registered

A validation check SHALL have a stable identifier, a version, a declared scope, a severity,
and a disposition. Data SHALL NOT be altered, excluded, or deduplicated by any operation
that is not a registered check.

#### Scenario: A registered check records its identity with its finding

- **WHEN** a check evaluates any input
- **THEN** the finding records the check identifier and version
- **AND** the finding is retrievable from the rows the check examined

#### Scenario: An unregistered mutation is refused

- **WHEN** a pipeline step would alter, exclude, or collapse rows without a registered check
- **THEN** the step SHALL fail rather than execute

#### Scenario: Changing a rule's behaviour requires a new version

- **WHEN** a check's logic changes such that it could produce a different disposition on the
  same input
- **THEN** its version changes
- **AND** findings recorded under the previous version remain attributed to it

### Requirement: A failing check records, and never silently repairs

A check SHALL NOT mutate a value, drop a row, or substitute a default. It SHALL record a
finding against the examined rows. Where the correct resolution is not determined by the
rule itself, it SHALL raise a conflict for human decision.

#### Scenario: A contradiction is recorded rather than corrected

- **WHEN** two fields in a record contradict each other
- **THEN** both values are retained unchanged
- **AND** a finding is recorded against that record

#### Scenario: A rejected row remains available

- **WHEN** a check rejects a row
- **THEN** the row remains retrievable in its original form
- **AND** the reason for rejection is retrievable with it

### Requirement: Conflicts are resolved asynchronously and never block ingestion

An unresolved conflict SHALL NOT prevent the pipeline from completing. Resolutions SHALL be
recorded as durable data, independent of any pipeline execution, and SHALL be reapplied on
subsequent runs.

#### Scenario: The pipeline completes with conflicts outstanding

- **WHEN** a run raises conflicts that no resolution covers
- **THEN** the run completes and produces output
- **AND** figures derived from the affected rows are marked provisional

#### Scenario: A recorded resolution is reapplied without human involvement

- **WHEN** a later run encounters a conflict for which a resolution already exists
- **THEN** the resolution is applied automatically
- **AND** the resulting figures are no longer provisional on that basis

#### Scenario: A resolution records who decided and why

- **WHEN** a human resolves a conflict
- **THEN** the resolution records the decider, the time, the option chosen, and a stated reason
- **AND** that record is reachable from any figure the decision affected

### Requirement: Provisional state propagates to every presentation

A figure derived from rows under an unresolved conflict SHALL be marked provisional, and
that marking SHALL survive every transformation and rendering between the mart and the reader.

#### Scenario: A provisional figure is labelled wherever it appears

- **WHEN** a provisional figure is presented in any surface
- **THEN** its provisional state is presented with it

#### Scenario: Aggregation does not launder provisional state

- **WHEN** an aggregate includes at least one provisional input
- **THEN** the aggregate is provisional
- **AND** the count of provisional inputs is retrievable

#### Scenario: A renderer that cannot express the state refuses the figure

- **WHEN** a rendering target cannot represent provisional state
- **THEN** it SHALL omit the figure rather than present it as settled

### Requirement: Whole-batch collisions resolve at batch scope

Where the same logical period arrives more than once and the collision spans an entire
batch rather than individual records, the conflict SHALL be raised once at batch scope. The
system SHALL NOT auto-select between batches on record ordering, and SHALL NOT merge them.

#### Scenario: A repeated period raises one conflict, not one per record

- **WHEN** every entity in a period has more than one record and the collision is
  batch-wide
- **THEN** exactly one conflict is raised for that period
- **AND** all affected records are attached to it

#### Scenario: Ordering is refused as a tiebreaker

- **WHEN** no field distinguishes which batch was submitted later
- **THEN** the system SHALL NOT infer submission order from position in the source
- **AND** the conflict remains unresolved until a human decides

#### Scenario: Both batches are retained until resolved

- **WHEN** a batch-scope conflict is unresolved
- **THEN** both batches remain retrievable in full

### Requirement: Analyses unsupported by the data are refused at source

Where a required presentation depends on a property the data does not exhibit, the system
SHALL refuse to produce it rather than produce a figure that implies the property holds.

#### Scenario: A period-over-period change is refused on a series with no temporal signal

- **WHEN** a period-over-period delta is requested for a series whose observed
  autocorrelation is not distinguishable from a within-entity permutation of itself
- **THEN** the delta SHALL NOT be presented as a trend
- **AND** the absence of temporal signal is reported in its place

#### Scenario: A pooled association is refused when it does not survive stratification

- **WHEN** an association between two measures is presented as explanatory
- **AND** that association does not hold within the strata of a variable both measures
  depend on
- **THEN** the association SHALL NOT be presented as explanatory
- **AND** the stratified result is reported alongside the pooled one

#### Scenario: A derived column that does not reconcile is not presented as derived

- **WHEN** a column named as a derivation of other columns cannot be reconstructed from them
  more accurately than a constant predictor
- **THEN** it SHALL NOT be presented or documented as a derived metric

### Requirement: Passing checks produce positive evidence

A check that finds no defect SHALL record that result. Absence of a finding SHALL be
distinguishable from absence of a check.

#### Scenario: A clean run is evidenced rather than silent

- **WHEN** a run completes with checks that found no defects
- **THEN** each check records that it ran, over what input, and found nothing
- **AND** the record includes the population examined

#### Scenario: A check that did not run is distinguishable from one that passed

- **WHEN** a check is not executed for any reason
- **THEN** its absence is recorded and is not reported as a pass

### Requirement: Findings are summarised for the reader, not only for the operator

Each published edition SHALL carry a completeness and quality summary stating expected
versus received inputs, unresolved conflicts by scope, and any presentation withheld under
the refusal rules.

#### Scenario: An edition states what was missing

- **WHEN** an edition is produced from inputs with absent periods or entities
- **THEN** the summary names what was expected and not received

#### Scenario: A withheld presentation is disclosed, not omitted silently

- **WHEN** a presentation is refused under the analysis-refusal rules
- **THEN** the edition states that it was withheld and why
