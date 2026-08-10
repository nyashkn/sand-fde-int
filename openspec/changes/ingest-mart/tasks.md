## 1. Crosswalk table

- [ ] 1.1 Create the crosswalk with columns: source_system, source_field, canonical_element, code_system, code, note
- [ ] 1.2 Populate the 57 mapped fields from `openspec/specs/conceptual-model/model.md`
- [ ] 1.3 Populate the 9 unmapped fields with their stated reason, marked not-presented and not-aggregated
- [ ] 1.4 Bind the five cause-of-death elements to ICD-10 codes (P21, P07, P36, Q00–Q99, residual) and the neonatal mortality rate to its WHO GHO definition
- [ ] 1.5 Verify the crosswalk is readable as data with no code execution, and that every canonical element it names exists in the conceptual model

## 2. Bronze

- [ ] 2.1 Load all five CSVs preserving original field names and values
- [ ] 2.2 Assign a batch identity per load: source system, file, load time, row range
- [ ] 2.3 Verify re-ingesting a period does not overwrite the earlier load, and both remain distinguishable
- [ ] 2.4 Add the rejection-reason column and verify a rejected row is retained unmodified alongside its reason
- [ ] 2.5 Verify bronze is never rewritten by a later run

## 3. Silver

- [ ] 3.1 Unpivot the wide CSVs to `(org_unit, period, data_element, batch, value)`
- [ ] 3.2 Resolve org_unit identity as a surrogate from `(source_system, source_key)`, retaining the source key; never use the id prefix as a district code
- [ ] 3.3 Map source fields to canonical elements via the crosswalk, not in code
- [ ] 3.4 Add provenance columns: source_system, source_key, batch, ingested_at, rules_applied, quality_flags, provisional
- [ ] 3.5 Verify both January loads and both March loads produce distinct silver rows attributable to their batch
- [ ] 3.6 Verify unmapped fields produce no silver observations while remaining in bronze
- [ ] 3.7 Verify the row count reconciles: mapped measures × facility-months × batches

## 4. Second source

- [ ] 4.1 Hand-write a small DHIS2-shaped export using real DHIS2 field names (`dataElement`, `orgUnit`, `period`, `value`), covering a few org_units and periods already present from the CSVs
- [ ] 4.2 Add its crosswalk rows only — no new loader logic beyond format parsing
- [ ] 4.3 Verify both sources produce silver rows carrying the same canonical data_element and resolving to the same org_unit identity
- [ ] 4.4 Verify the two observations are retained separately and neither is silently preferred

## 5. Gold

- [ ] 5.1 Define the gold marts the bulletin needs: facility-quarter, district-quarter, and the edition completeness summary
- [ ] 5.2 Emit gold as Parquet
- [ ] 5.3 Verify provenance needed to reach inputs survives aggregation into gold
- [ ] 5.4 Verify a browser client can read a gold mart directly over HTTP range requests and retrieve a subset without the whole file
- [ ] 5.5 Verify a cached mart remains readable with no connectivity
- [ ] 5.6 Verify the same artifact is read by both the batch environment and the browser client

## 6. Reproducibility

- [ ] 6.1 Verify silver regenerates identically from unchanged bronze, crosswalk, rules, and resolutions
- [ ] 6.2 Verify gold regenerates identically from unchanged silver
- [ ] 6.3 Verify a crosswalk change alters silver and leaves bronze untouched

## 7. Record and hand off

- [ ] 7.1 Answer or explicitly defer the two open questions in `design.md` (source blob in bronze, gold partitioning)
- [ ] 7.2 Confirm `data-validation` has silver nodes its checks can attach to
- [ ] 7.3 Confirm `trust-lineage` has every column its projection requires, with no new write path needed
- [ ] 7.4 Write the README setup and run instructions required by the brief's submission list
