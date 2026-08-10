## Purpose

Define the objects the system works with, their identity and grain rules, one canonical
term per concept, and the URL contract that addresses them — so that every figure a reader
sees can be traced to a named, addressable thing rather than to an anonymous query result.

## ADDED Requirements

### Requirement: Canonical object set

The system SHALL define a closed set of objects. Every figure presented to a human SHALL
resolve to exactly one object in that set. An object SHALL declare whether it is
*addressable* (may be a deeplink target) or *internal*.

#### Scenario: A bulletin figure resolves to an addressable object

- **WHEN** the bulletin renders any numeric figure
- **THEN** that figure references exactly one addressable object
- **AND** the object's canonical URL is emitted alongside it

#### Scenario: A figure with no corresponding object is rejected

- **WHEN** a renderer requests a figure that maps to no object in the canonical set
- **THEN** the render SHALL fail with a named error rather than emit an unlinked figure

### Requirement: Explicit grain on every metric-bearing object

Every object that carries a metric SHALL declare its grain as an ordered tuple of
dimensions. A metric SHALL NOT be presented without its object, and therefore never
without its grain.

#### Scenario: Grain is stated for a district figure

- **WHEN** a district-level neonatal mortality rate is presented
- **THEN** the grain `(district, quarter)` is recorded with the figure
- **AND** the figure's provenance names the number of finer-grained rows aggregated into it

#### Scenario: Mixed-grain aggregation is refused

- **WHEN** an aggregation would combine rows of two different grains
- **THEN** the operation SHALL fail rather than silently produce a figure

### Requirement: Stable object identity independent of source keys

Each object SHALL have an identity rule that does not depend on any single source system's
key. Where a source key is ambiguous, the identity rule SHALL name the disambiguating
attributes.

#### Scenario: Ambiguous source prefix does not determine identity

- **WHEN** a facility identifier's prefix maps to more than one district
- **THEN** identity SHALL be resolved by the full identifier plus its declared district
- **AND** the prefix SHALL NOT be used as a district code anywhere in the system

#### Scenario: The same real-world entity from two sources resolves to one object

- **WHEN** the same facility arrives from two source systems under different keys
- **THEN** both SHALL resolve to a single object identity
- **AND** the originating keys SHALL remain recorded against that object

### Requirement: Ubiquitous language with recorded synonyms

The system SHALL define exactly one canonical term per concept. Every known source-system
synonym SHALL be recorded against its canonical term. Canonical terms SHALL be taken from
an existing published standard where one applies, and SHALL only be invented where none
does.

#### Scenario: A source synonym maps to its canonical term

- **WHEN** a source system supplies a field under a synonym of a canonical term
- **THEN** the synonym resolves to the canonical term through a recorded mapping
- **AND** the mapping is inspectable without reading code

#### Scenario: An unmapped term is surfaced rather than guessed

- **WHEN** an ingested field matches no canonical term or recorded synonym
- **THEN** the system SHALL report it as unmapped
- **AND** SHALL NOT infer a mapping automatically

### Requirement: Canonical object URLs are stable and shareable

Every addressable object SHALL have exactly one canonical URL. That URL SHALL be derivable
from the object's identity and grain alone, SHALL be stable across renders of the same
period, and SHALL be safe to paste into an email or a message.

#### Scenario: The same object yields the same URL across two runs

- **WHEN** the bulletin is regenerated for an unchanged period
- **THEN** each figure's canonical URL is byte-identical to the previous run

#### Scenario: A canonical URL resolves without prior session state

- **WHEN** a recipient opens a canonical URL in a fresh browser with no stored state
- **THEN** the referenced object is presented in full

### Requirement: Explore state URLs are distinct from canonical object URLs

A serialised selection in the explore surface SHALL use a URL form that is distinguishable
from a canonical object URL. Explore state SHALL NOT be presented as an object address, and
SHALL carry no stability guarantee across releases.

#### Scenario: A selection is shared and reproduces the same view

- **WHEN** a user shares a URL representing an active filter selection
- **THEN** opening it reproduces that selection
- **AND** the URL is recognisable as state rather than as a canonical object

#### Scenario: The bulletin never links to an explore state URL

- **WHEN** the bulletin emits a link for any figure
- **THEN** that link is a canonical object URL

### Requirement: Object states are enumerated and observable

Objects whose completeness varies SHALL declare an enumerated state. The state SHALL be
presented wherever the object is presented, and SHALL never be inferred by the reader from
the absence of information.

#### Scenario: A period with missing source data is labelled

- **WHEN** a reporting period is presented for which one or more expected source periods
  are absent
- **THEN** the object is presented in its incomplete state
- **AND** the absent periods are named on the face of the presentation

#### Scenario: An entity with no instrumentation is distinguished from one measuring zero

- **WHEN** an entity has no source rows for a metric
- **THEN** it is presented as unmeasured
- **AND** SHALL NOT be presented as a zero value
