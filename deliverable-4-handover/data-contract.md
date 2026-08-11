# Data contract

What the pipeline requires from its inputs, and, precisely, what happens when an input
stops matching that shape. Every claim below was read from the code that enforces it or
demonstrated by running it, not inferred from what the code is supposed to do.

## Required inputs

Five CSVs in `assignment/data/`, verified against the files this pipeline was built and
tested on:

| File | Rows | Columns |
|---|---|---|
| `facilities.csv` | 117 | `facility_id, facility_name, district, province, tier_level, gps_lat, gps_lon, nicu_available, nicu_beds, incubators_functional, incubators_total, radiant_warmers, phototherapy_units, cpap_machines, resuscitation_tables, kangaroo_care_space, electricity_reliable, backup_generator` |
| `clinical_neonatal.csv` | 1,404 | `facility_id, reporting_month, total_deliveries, live_births, neonatal_deaths_0_7d, neonatal_deaths_8_28d, stillbirths, death_birth_asphyxia, death_prematurity, death_sepsis, death_congenital, death_other, avg_gestational_age, preterm_births_28_32w, preterm_births_32_37w, apgar_less_7_at_5min, birth_weight_less_2500g` |
| `governance.csv` | 117 | `facility_id, newborn_protocol_exists, protocol_last_updated, death_audits_conducted_pct, staff_trained_on_protocol_pct, quality_improvement_active, supervision_visits_quarterly, hmis_reporting_completeness, bag_mask_ventilation_competency, thermal_care_protocol_compliance, infection_prevention_score` |
| `healthcare_workers.csv` | 117 | `facility_id, total_nurses, neonatal_trained_nurses, midwives, obstetricians, pediatricians, neonatologists, anesthetists, last_neonatal_training_date, staff_per_delivery_2024, night_shift_coverage` |
| `operations.csv` | 117 | `facility_id, avg_referral_time_hrs, referrals_out_monthly, referrals_in_monthly, oxygen_cylinders_available, oxygen_concentrators, oxygen_plant, ambulance_available, kangaroo_care_practiced, essential_drugs_stockouts_days, antibiotics_available, surfactant_available, referral_feedback_rate` |

Plus one long-format DHIS2-shaped source (`pipeline/mart/dhis2_sample.csv` in this
prototype; a real deployment points this at DHIS2's own export or API), carrying
`orgUnit, dataElement, period, value`. This second source exists specifically to prove
the mapping works on DHIS2's actual shape, not only on the wide CSVs the assignment
provided.

Every row keys on `facility_id`. There is no other required key; a source may carry any
subset of the columns above.

## The crosswalk: how a column becomes a figure

`pipeline/mart/crosswalk.csv`, 71 rows: 66 from the assignment CSVs, 5 from DHIS2. Each
row is `(source_system, source_field, canonical_element, role, code_system, code, note)`.
`role` is one of:

- **`identity`** (2 rows): resolves to an `org_unit` through `mart/org_unit_map.csv`.
- **`dimension`** (5 rows): `district`, `province`, `tier_level`, and the two grain
  columns; describes an org_unit rather than measuring it.
- **`observation`** (55 rows): becomes a row in the silver table, one per
  `(org_unit, period, data_element)`.
- **`unmapped`** (9 rows): present in the source, deliberately not carried forward, with
  the reason recorded in `note`. This is `gps_lat`/`gps_lon` (uniform random, see
  `artifacts/04-data-quality-audit.html`), `facility_name` (contradicts `tier_level` in 62
  of 117 rows), `staff_per_delivery_2024` (unreconstructable from any formula tested), and
  five columns with no clinical reconciliation the audit could establish.

## What happens when a column changes

**A column is renamed.** Read from `dataflow/silver.py` line 102:
`measures = [c for c in df.columns if c in lookup]`. A column whose name no longer
matches a `source_field` in the crosswalk is **silently excluded** from that source file's
melt. No error. No warning. No row anywhere downstream. Run against a copy of
`clinical_neonatal.csv` with `total_deliveries` renamed to `deliveries_count`:

```
total_deliveries rows: 0
deliveries_count rows: 0
live_births rows (unaffected sibling column): 1408
run raised no exception: True
```

Every other metric in the same file survives untouched; the renamed one drops to zero
rows under both its old and new name, indistinguishable from a metric that was never
collected, and nothing about the run signals that anything is wrong. **This is the
sharpest edge in this pipeline.** If a figure the bulletin used to carry disappears with
no error and no explanation, check whether its source column was renamed before checking
anything else.

*Not yet built:* a coverage check comparing each source file's actual column set against
the crosswalk's expected `source_field` set, failing loud on a column present in neither
`role=observation` nor `role=unmapped`. This is the first thing to add if `data-validation`
resumes; see D3 hardening item 2 for the same gap from the ingestion side.

**A column is absent entirely.** Same code path, same outcome: absent from `df.columns`
means absent from `measures`, so a missing column behaves identically to a renamed one.
No file-level row-count or column-count check exists today.

**A new column appears.** Ignored. `measures` only includes columns the crosswalk
recognises, so an unrecognised new column is inert until someone adds a crosswalk row for
it. This is the safe direction: new data does not silently enter a bulletin figure without
a person deciding what it means.

**A row's `facility_id` does not resolve.** This one fails loud, by design. From
`dataflow/silver.py`:

```
ValueError: N observations have no org_unit resolution.
Add rows to mart/org_unit_map.csv for: [(source_system, facility_id), ...]
```

The pipeline stops. Nothing partially publishes. Add the missing facility to
`org_unit_map.csv` and rerun.

**Two batches of the same period collide.** Handled, not an error: see
`decision-register.md` for the batch-conflict process.

## Onboarding a second source system

`dataflow/silver.py`'s own comment states the intent directly: "Mapping happens through
`mart/crosswalk.csv`, never through logic here." Adding HealthTrack, OpenMRS, or a
paper-entry export means: add rows to `crosswalk.csv` mapping that system's field names to
the same `canonical_element` values already in use, add an `org_unit_map.csv` entry per
facility identity that system uses, and nothing in `dataflow/*.py` changes. The DHIS2
source in this prototype exists to prove that claim on a second, structurally different
(long, not wide) source, not only assert it.
