## Purpose

Make the bulletin legible to the person who has to act on it: a reading order that answers
the Director's question in the first screen, charts where shape carries meaning better than
digits, and state visible without stopping to read.

## ADDED Requirements

### Requirement: One design system across engagement artifacts

Rendered artifacts for this engagement SHALL draw colour, type, and spacing from a single
recorded token set. A document SHALL NOT introduce a palette of its own.

#### Scenario: A new artifact inherits the token set

- **WHEN** a new rendered artifact is produced for this engagement
- **THEN** its colours and type scale resolve to the recorded tokens
- **AND** no colour outside the token set carries meaning

#### Scenario: The token set is recorded, not implied

- **WHEN** a reader asks which colours and type scale the artifact uses
- **THEN** the answer is retrievable from a recorded design document
- **AND** that document is derived from tokens actually in use

### Requirement: Charts render without executing anything

Every chart SHALL be embedded in the document as static markup. The document SHALL contain
no script, no external asset reference, and no runtime charting library.

#### Scenario: A chart survives a surface that cannot execute code

- **WHEN** the document is opened in a surface that executes no script
- **THEN** every chart renders as published

#### Scenario: A chart survives having no network

- **WHEN** the document is opened with no connectivity
- **THEN** every chart renders as published

#### Scenario: Chart text is legible at the size it is published

- **WHEN** a chart carries axis labels, tick values, or annotations
- **THEN** they are legible at the chart's published dimensions without magnification

### Requirement: A figure's kind determines its chart type

The mapping from figure kind to chart type SHALL be recorded and applied consistently.
Chart type SHALL NOT be chosen per panel.

#### Scenario: Two figures of the same kind get the same chart type

- **WHEN** two figures share a kind
- **THEN** they are rendered with the same chart type

#### Scenario: A figure kind with no registered chart type is refused

- **WHEN** a figure is presented whose kind has no entry in the registry
- **THEN** the render SHALL fail rather than improvise a chart type

#### Scenario: A chart never encodes a dimension the data does not carry

- **WHEN** a chart is produced for a figure
- **THEN** every visual channel it uses maps to a measure or dimension present in that figure

### Requirement: Reading order is designed for a named reader

The document SHALL declare, for each of its readers, the question they arrive with and where
it is answered. The first screen SHALL answer the primary reader's question.

#### Scenario: The primary reader's question is answered before scrolling

- **WHEN** the document is opened at its top
- **THEN** the primary reader's stated question is answered within the first screen

#### Scenario: A secondary reader can reach their section without reading the first

- **WHEN** a secondary reader opens the document
- **THEN** their section is reachable without reading sections addressed to other readers

### Requirement: State is visible before it is read

Provisional, withheld, and unmeasured SHALL be distinguishable by a non-textual channel, so a
reader scanning the page perceives them without reading a label. Colour SHALL NOT be the only
channel carrying the distinction.

#### Scenario: A scanning reader perceives provisional figures

- **WHEN** a reader scans a table containing both settled and provisional figures
- **THEN** the provisional ones are distinguishable without reading their labels

#### Scenario: State survives loss of colour

- **WHEN** the document is viewed without colour
- **THEN** provisional, withheld, and unmeasured remain distinguishable from settled

#### Scenario: A withheld panel is as visible as a rendered one

- **WHEN** a panel is withheld
- **THEN** it occupies the position and prominence the rendered panel would have had

### Requirement: Rendered copy conforms to the house style

Rendered output SHALL contain no em dash. Meaning-carrying accents SHALL NOT be applied as a
coloured left or right border.

#### Scenario: No em dash reaches the reader

- **WHEN** the document is rendered
- **THEN** it contains no em dash character

#### Scenario: No meaning is carried by a side-stripe border

- **WHEN** an element distinguishes itself from body content
- **THEN** it does so without a coloured left or right border exceeding a hairline

#### Scenario: Style conformance is mechanically checkable

- **WHEN** the document is rendered
- **THEN** conformance to the two rules above is verifiable by an automated check over the output
