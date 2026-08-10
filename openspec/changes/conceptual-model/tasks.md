## 1. Noun harvest and terminology reconciliation

- [x] 1.1 Extract every field name from the five sample CSVs into a flat inventory with its file, dtype, and a one-line meaning
- [x] 1.2 Extract the vocabulary observed in the Bluelake Admin UI walkthrough artifact (nav labels, entity names, screen titles)
- [x] 1.3 Pull the DHIS2 data model terms that apply (`orgUnit`, `period`, `dataElement`, `categoryOptionCombo`, `dataSet`) with their definitions
- [x] 1.4 Produce the terminology conflict table: one row per concept, columns for each source's term, flagging every case where two sources use one word differently or two words for one thing
- [x] 1.5 Resolve each conflict to a single canonical term, citing the standard it binds to, or marking it invented with a reason

## 2. Object map

- [x] 2.1 List candidate objects from the noun harvest and mark each addressable or internal
- [x] 2.2 Write the identity rule for each object, naming the disambiguating attributes where a source key is ambiguous
- [x] 2.3 Declare the grain tuple for every metric-bearing object
- [x] 2.4 Draw the relationships between objects, including cardinality
- [x] 2.5 Enumerate the states for each object whose completeness varies, including the unmeasured-versus-zero distinction

## 3. Deeplink URL contract

- [x] 3.1 Define the canonical object URL pattern per addressable object, derived from identity and grain only
- [x] 3.2 Define the explore state URL form, structurally distinguishable from canonical URLs
- [x] 3.3 Write the rule a renderer can mechanically check to prove it emitted no state URL in the bulletin
- [x] 3.4 Verify each canonical pattern round-trips: object → URL → object, with no session state

## 4. Validation against the sample

- [x] 4.1 Confirm every column across the five CSVs maps to a canonical term or is explicitly listed as unmapped
- [x] 4.2 Confirm the identity rules survive the known ambiguities: `NYA` prefix across seven districts, `facility_name` contradicting `tier_level` in 62 of 117 rows
- [x] 4.3 Confirm the incomplete state correctly fires for 2024 Q1 and Q4 given the absent and duplicated periods
- [x] 4.4 Confirm no rule anywhere depends on `gps_lat`/`gps_lon`

## 5. Record and hand off

- [ ] 5.1 Write the object map and ubiquitous language into `openspec/specs/conceptual-model/` via the archive step
- [x] 5.2 Record any canonical term that was invented rather than bound, as an ADR
- [x] 5.3 Answer or explicitly defer the two open questions in `design.md` (province as object, bulletin as object)
- [x] 5.4 Confirm `ingest-mart` and `trust-lineage` have what they need: the vocabulary and the URL contract respectively
