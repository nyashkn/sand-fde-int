## 1. Noun harvest and terminology reconciliation

- [ ] 1.1 Extract every field name from the five sample CSVs into a flat inventory with its file, dtype, and a one-line meaning
- [ ] 1.2 Extract the vocabulary observed in the Bluelake Admin UI walkthrough artifact (nav labels, entity names, screen titles)
- [ ] 1.3 Pull the DHIS2 data model terms that apply (`orgUnit`, `period`, `dataElement`, `categoryOptionCombo`, `dataSet`) with their definitions
- [ ] 1.4 Produce the terminology conflict table: one row per concept, columns for each source's term, flagging every case where two sources use one word differently or two words for one thing
- [ ] 1.5 Resolve each conflict to a single canonical term, citing the standard it binds to, or marking it invented with a reason

## 2. Object map

- [ ] 2.1 List candidate objects from the noun harvest and mark each addressable or internal
- [ ] 2.2 Write the identity rule for each object, naming the disambiguating attributes where a source key is ambiguous
- [ ] 2.3 Declare the grain tuple for every metric-bearing object
- [ ] 2.4 Draw the relationships between objects, including cardinality
- [ ] 2.5 Enumerate the states for each object whose completeness varies, including the unmeasured-versus-zero distinction

## 3. Deeplink URL contract

- [ ] 3.1 Define the canonical object URL pattern per addressable object, derived from identity and grain only
- [ ] 3.2 Define the explore state URL form, structurally distinguishable from canonical URLs
- [ ] 3.3 Write the rule a renderer can mechanically check to prove it emitted no state URL in the bulletin
- [ ] 3.4 Verify each canonical pattern round-trips: object → URL → object, with no session state

## 4. Validation against the sample

- [ ] 4.1 Confirm every column across the five CSVs maps to a canonical term or is explicitly listed as unmapped
- [ ] 4.2 Confirm the identity rules survive the known ambiguities: `NYA` prefix across seven districts, `facility_name` contradicting `tier_level` in 62 of 117 rows
- [ ] 4.3 Confirm the incomplete state correctly fires for 2024 Q1 and Q4 given the absent and duplicated periods
- [ ] 4.4 Confirm no rule anywhere depends on `gps_lat`/`gps_lon`

## 5. Record and hand off

- [ ] 5.1 Write the object map and ubiquitous language into `openspec/specs/conceptual-model/` via the archive step
- [ ] 5.2 Record any canonical term that was invented rather than bound, as an ADR
- [ ] 5.3 Answer or explicitly defer the two open questions in `design.md` (province as object, bulletin as object)
- [ ] 5.4 Confirm `ingest-mart` and `trust-lineage` have what they need: the vocabulary and the URL contract respectively
