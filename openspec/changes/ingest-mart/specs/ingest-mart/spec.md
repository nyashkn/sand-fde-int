## Purpose

Give every figure a substrate that can answer where it came from: source data kept exactly
as received, a canonical layer at the grain the country's own HMIS speaks, and marts that
both a batch job and a browser can read without a service between them.

## ADDED Requirements

### Requirement: Bronze retains source data exactly as received

Bronze SHALL store incoming data with its original field names and values, unmodified. Rows
that fail any check SHALL be retained in bronze in original form together with the reason
they were rejected. Bronze SHALL NOT be rewritten by a later run.

#### Scenario: Source field names survive ingestion

- **WHEN** a source file is ingested
- **THEN** bronze holds its fields under the names the source used
- **AND** the values are byte-identical to the source

#### Scenario: A rejected row remains retrievable with its reason

- **WHEN** a check rejects a row
- **THEN** the row is retained in bronze unmodified
- **AND** the rejection reason is retrievable with it

#### Scenario: Re-ingesting the same source does not overwrite the earlier load

- **WHEN** a source covering an already-ingested period is ingested again
- **THEN** both loads are retained and distinguishable
- **AND** neither is altered

### Requirement: Silver is canonical, at a fixed grain, with batch in the key

Silver SHALL store observations at the grain `(org_unit, period, data_element, batch)`. Field
names SHALL be canonical terms. Two loads of the same logical period SHALL occupy distinct
silver rows rather than colliding.

#### Scenario: Two loads of one period coexist in silver

- **WHEN** the same org_unit, period, and data_element arrive in two batches
- **THEN** silver holds both observations
- **AND** each is attributable to its batch

#### Scenario: Silver uses canonical terms, not source terms

- **WHEN** an observation is written to silver
- **THEN** its data_element is a canonical term
- **AND** the source field it came from remains recoverable

#### Scenario: An observation resolves to a canonical object identity

- **WHEN** an observation is written to silver
- **THEN** its org_unit is a resolved identity, not a raw source key
- **AND** the originating source key is retained alongside it

### Requirement: Provenance is carried as columns on every observation

Every silver observation SHALL carry, as columns, the source system it came from, the source
key it was identified by, its batch, the time it was ingested, every rule applied to it, and
its quality and provisional state. Provenance SHALL NOT be recorded only in logs or run
metadata.

#### Scenario: Provenance is queryable alongside the value

- **WHEN** an observation is retrieved
- **THEN** its source system, source key, batch, ingest time, applied rules, and state are
  retrieved with it in the same operation

#### Scenario: Provenance survives promotion to gold

- **WHEN** observations are aggregated into a gold mart
- **THEN** the aggregate carries the provenance needed to reach its inputs

### Requirement: Mapping between source and canonical terms is a table

The mapping from source fields to canonical elements SHALL be stored as data, containing at
minimum the source system, the source field, the canonical element, and where a published
standard applies, the code system and code. Mapping SHALL NOT be expressed only as logic in
transformation code.

#### Scenario: A new source is onboarded by adding rows

- **WHEN** a source system not previously ingested is added
- **AND** its fields map to canonical elements already in use
- **THEN** ingestion succeeds by adding mapping rows only

#### Scenario: The mapping is inspectable without reading code

- **WHEN** a reader asks which source field produced a canonical element
- **THEN** the answer is retrievable from the mapping data

#### Scenario: An unmapped source field is recorded, not dropped

- **WHEN** a source field maps to no canonical element
- **THEN** it is retained in bronze
- **AND** it is recorded as unmapped with a stated reason
- **AND** it is neither presented nor aggregated

### Requirement: Two sources naming the same measure land in identical silver rows

Where two source systems supply the same measure for the same org_unit and period under
different field names, both SHALL produce silver observations differing only in source
system, source key, and batch.

#### Scenario: Differently-named source fields converge

- **WHEN** two sources supply the same measure for one org_unit and period
- **THEN** both silver rows carry the same canonical data_element
- **AND** both resolve to the same org_unit identity

#### Scenario: Convergence does not merge the observations

- **WHEN** two sources supply the same measure for one org_unit and period
- **THEN** both observations are retained separately
- **AND** neither is silently preferred

### Requirement: Gold marts are readable without a service

Gold marts SHALL be published as files readable directly by both the batch environment and a
browser client, without an intermediating query service. A client SHALL be able to retrieve
only the portions it needs.

#### Scenario: The same artifact serves both consumers

- **WHEN** a gold mart is published
- **THEN** the batch environment and a browser client read the same artifact
- **AND** neither requires a running service to do so

#### Scenario: A client retrieves a subset without downloading the whole mart

- **WHEN** a client needs a subset of a gold mart
- **THEN** it can retrieve that subset without transferring the entire artifact

#### Scenario: A cached mart remains usable offline

- **WHEN** a client has previously retrieved a gold mart and has no connectivity
- **THEN** the mart remains readable

### Requirement: Every layer transition is reproducible from the layer above

Given bronze, the mapping table, the rule versions, and recorded resolutions, silver and gold
SHALL be regenerable with identical contents.

#### Scenario: Silver regenerates identically from bronze

- **WHEN** silver is regenerated from unchanged bronze, mapping, rules, and resolutions
- **THEN** its contents are identical to the previous generation

#### Scenario: Gold regenerates identically from silver

- **WHEN** gold is regenerated from unchanged silver
- **THEN** every figure is identical to the previous generation

#### Scenario: A changed mapping produces a changed silver, not a changed bronze

- **WHEN** the mapping table changes and ingestion is re-run
- **THEN** bronze is unchanged
- **AND** silver reflects the new mapping
