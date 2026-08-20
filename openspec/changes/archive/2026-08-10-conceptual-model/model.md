# Conceptual model

Working output of the `conceptual-model` change. Archives into
`openspec/specs/conceptual-model/` alongside `spec.md`.

Sources: 66 distinct fields (70 column slots) across the five sample CSVs, the Bluelake
Admin UI vocabulary
reconstructed in `artifacts/01-bluelake-admin-ux-walkthrough.html`, the DHIS2 data model,
and the defect inventory in `artifacts/04-data-quality-audit.html`.

---

## 1. Terminology conflicts

Four sources, one domain. Every conflict below is real, observed in the data, in Sand's
own product, or in the standard we are binding to.

| Concept | Sample CSVs | Bluelake UI | DHIS2 | Brief | Resolution |
|---|---|---|---|---|---|
| The place care is delivered | `facility_id` | **both** "Health Post" (chart titles) and "Facility" (filter bar) | `orgUnit` | "facility", "site" | **`org_unit`** |
| A reporting time window | `reporting_month` | "Last N Days", "From" | `period` | "quarter" | **`period`** |
| A thing measured | column name | chart title | `dataElement` | "metric", "indicator" | **`data_element`** |
| A measured value | cell |, | `dataValue` |, | **`observation`** |
| One arrival/contact |, | **"Footfall"**, "visits" |, |, | *not modelled*, no analogue in the data |
| Administrative parent | `district`, `province` |, | `orgUnit` at a higher level | "district" | **`org_unit`** (same type, different level) |
| Service capability band | `tier_level` |, | `orgUnitGroup` | "tier" | **`tier`** |

### Conflicts worth naming explicitly

**Health Post ≡ Facility.** Bluelake uses both words for one entity on the same screen.
Adopting either would perpetuate the ambiguity, so both become synonyms of `org_unit`.

**District is not a different kind of thing from a facility.** DHIS2 models the whole
administrative hierarchy as `orgUnit` at different levels. The sample flattens this into
string columns on the facility row. We adopt the DHIS2 shape: one type, a level attribute,
a parent reference. This is what makes a district figure and a facility figure the same
kind of object, addressable by the same URL pattern.

**Bluelake filters on `gender` and `age group`; the sample has neither.** Recorded as a
known gap, not invented. In DHIS2 terms these are `categoryOptionCombo` disaggregations.
The model reserves the slot so a later source can populate it without a reshape.

**`tier_level` is nominally four bands and measurably two.** District-tier facilities are
statistically indistinguishable from Health Centers across all seven equipment columns and
three specialist-staffing columns. The model keeps the source's four values, inventing a
two-band enum would silently discard a distinction the MoH uses administratively, but
records the collapse as an attribute of the tier, not of any facility.

### Invented terms

Two, both recorded here because nothing in DHIS2, ICD-10, or WHO GHO covers them:

- **`observation`**, DHIS2 calls this a `dataValue`; we use `observation` because
  `dataValue` reads as a scalar and this object carries provenance and state.
- **`edition`**, a published bulletin for a period. No standard term exists.

---

## 2. Object map

Seven objects. Four addressable, three internal.

### `org_unit`, addressable

The place, at any administrative level. One type, not three.

| | |
|---|---|
| **Identity** | surrogate key resolved from `(source_system, source_key)`. **Never** the source key alone. |
| **Grain** | one row per unit |
| **Levels** | `country` → `province` → `district` → `facility` |
| **Attributes** | `name`, `level`, `parent`, `tier` (facility level only) |
| **States** | `active` · `unmeasured` (exists, reports nothing for the requested period) |

**Why a surrogate.** `facility_id` prefixes are ambiguous, `NYA` maps to seven districts
(Nyabihu, Nyagatare, Nyamagabe, Nyamasheke, Nyanza, Nyarugenge, Nyaruguru) and `NGO` to two.
The numeric suffix is globally unique, so joins work, but any consumer reading the prefix as
a district code is wrong seven ways. The identity rule is the full identifier plus its
declared district; **the prefix is not a district code and is not used as one anywhere.**

**Explicitly excluded from identity:** `gps_lat`, `gps_lon` (uniform random within Rwanda's
bbox), `facility_name` (templated, and contradicts `tier_level` in 62 of 117 rows).

### `period`, addressable

A reporting window.

| | |
|---|---|
| **Identity** | ISO 8601 interval. Month `2024-01`, quarter `2024-Q1`, year `2024`. |
| **Grain** | one row per window per type |
| **Attributes** | `type` (month/quarter/year), `start`, `end`, `expected_children` |
| **States** | `complete` · `incomplete` (≥1 expected child absent) · `contested` (≥1 child under an unresolved batch conflict) |

`expected_children` is what makes `incomplete` computable rather than asserted: `2024-Q1`
expects `{2024-01, 2024-02, 2024-03}`, receives `{2024-01, 2024-03}`, and is therefore
`incomplete` **and** `contested`, both January and March are duplicated batches.

### `data_element`, internal

What is measured. The canonical vocabulary target for the crosswalk.

| | |
|---|---|
| **Identity** | canonical name |
| **Attributes** | `code_system` + `code` where a standard applies, `unit`, `value_type`, `aggregation` |
| **States** | `bound` (maps to a published standard) · `local` (invented, with a recorded reason) |

Cause-of-death elements bind to ICD-10 perinatal codes: `death_birth_asphyxia`→P21,
`death_prematurity`→P07, `death_sepsis`→P36, `death_congenital`→Q00–Q99, `death_other`→
residual. `nmr` binds to the WHO GHO definition.

### `observation`, internal

One measured value. The atom everything aggregates from.

| | |
|---|---|
| **Identity** | `(org_unit, period, data_element, source_system, batch)` |
| **Grain** | the tuple above |
| **Attributes** | `value`, `ingested_at`, `rule_applied`, `quality_flags` |
| **States** | `settled` · `provisional` (under unresolved conflict) · `superseded` |

`batch` is **in the identity**. Without it the two January loads collide and one silently
overwrites the other, which is exactly the defect. With it, both are retained and the
conflict is representable.

### `metric`, addressable

A computed figure presented to a human. The thing a deeplink points at.

| | |
|---|---|
| **Identity** | `(data_element_or_formula, org_unit, period)` |
| **Grain** | declared per metric, `(facility, month)`, `(district, quarter)`, `(facility, quarter)` |
| **Attributes** | `value`, `numerator`, `denominator`, `definition_ref`, `provisional_input_count` |
| **States** | `settled` · `provisional` · `withheld` (refused under the analysis-refusal rules) · `unmeasured` |

`withheld` is a first-class state, not an absence. A period-over-period delta on a series
with no temporal signal, or a pooled association that does not survive stratification, is
`withheld`, and the edition says so rather than the panel quietly vanishing.

`unmeasured` ≠ zero. An org_unit with no observations for a metric other units report is
`unmeasured`, and is rendered visually distinct from a measured `0`.

### `edition`, addressable

A published bulletin for a period. Citable, immutable once issued.

| | |
|---|---|
| **Identity** | `(period, revision)` |
| **Attributes** | `issued_at`, `metric_set`, `completeness_summary`, `withheld_list` |
| **States** | `draft` · `issued` · `superseded` |

An `issued` edition is never edited. A correction produces revision *n+1* that supersedes it,
so a figure a Minister quoted last quarter still resolves to what they actually saw.

### `conflict`, internal, but reachable

A decision the data cannot make for itself.

| | |
|---|---|
| **Identity** | `(kind, scope_key)` |
| **Scope** | `row` · `column` · `batch` · `cross_file` · `file` |
| **Attributes** | `detected_at`, `options`, `default_applied`, `finding_ref` |
| **States** | `unresolved` · `resolved` · `void` |

Not addressable as a top-level URL, but **reachable from any metric it makes provisional**,
that reachability is the trust mechanism.

### Relationships

```
org_unit ──parent──> org_unit                    (self, hierarchical, 0..1)
observation ──> org_unit, period, data_element   (many-to-one each)
metric ──derives from──> observation             (1..n)
metric ──> org_unit, period                      (many-to-one each)
edition ──contains──> metric                     (1..n)
edition ──> period                               (many-to-one)
conflict ──attaches to──> scope key              (batch | column | row | file)
conflict ──makes provisional──> observation      (0..n) ──> metric (transitively)
```

---

## 3. Deeplink URL contract

Two forms, **structurally** distinguishable. Not by convention, by path root, so a
renderer can be mechanically checked.

### Canonical object URLs, path-based, no identifying query

```
/edition/2024-Q3
/unit/district/nyanza
/unit/facility/NYA017
/metric/nmr/district/nyanza/2024-Q3
/metric/nmr/facility/NYA017/2024-08
/period/2024-Q3
```

Rules:
- Derived from **identity and grain only**. Never from storage paths, row offsets, or
  query results.
- Byte-identical across two renders of the same period, that is the stability test.
- Resolves with no session state: a recipient opening it in a fresh browser sees the object
  in full.
- Query parameters may affect *presentation* (`?units=per1000`) but never *identity*.

The metric pattern embeds grain in the path, `/metric/<element>/<level>/<unit>/<period>`,
so `/metric/nmr/district/nyanza/2024-Q3` and `/metric/nmr/facility/NYA017/2024-Q3` are
visibly different grains, and a mixed-grain URL cannot be constructed.

### Explore state URLs, distinct root, opaque payload

```
/explore?s=<opaque>
```

Rules:
- Single opaque parameter under a **different path root**.
- Carries **no stability guarantee** across releases.
- Represents a selection, not an object.

### The mechanical check

> Every href emitted by the bulletin renderer MUST match `^/(edition|unit|metric|period)/`
> and MUST NOT match `^/explore`.

One regex, runnable in a test. That is why the two forms differ by path root rather than by
a naming habit a reviewer has to police.

### Reaching provenance

Provenance is not a separate URL space, it is a view on the object:

```
/metric/nmr/district/nyanza/2024-Q3            the figure
/metric/nmr/district/nyanza/2024-Q3/lineage    rows, rules, conflicts, absent periods
```

Sub-resource, not a query parameter, so it is addressable and shareable in its own right.

---

## 4. Validation against the sample

Every rule above tested against the real data.

| Check | Result |
|---|---|
| All distinct fields map to a canonical term or are explicitly unmapped | **66/66**, 57 mapped, 9 unmapped-by-decision. 70 column slots, `facility_id` recurring in all five files |
| Identity survives `NYA` → 7 districts | **pass**, surrogate from `(source_system, source_key)`; prefix never used as a district code |
| Identity survives `facility_name` ⊥ `tier_level` (62/117) | **pass**, name excluded from identity, retained as a label |
| `incomplete` fires for 2024-Q1 and 2024-Q4 | **pass**, Q1 expects 3 children, receives 2; Q4 expects 3, receives 2 |
| `contested` fires for 2024-Q1 | **pass**, 2024-01 and 2024-03 both under batch conflict |
| No rule depends on `gps_lat`/`gps_lon` | **pass**, excluded from identity, from grain, and from every URL pattern |
| Mixed-grain URL is unconstructable | **pass**, grain is a path segment |
| `unmeasured` distinguishable from `0` | **pass**, separate state on both `org_unit` and `metric` |

### The 9 unmapped fields, and why

| Field | Reason |
|---|---|
| `gps_lat`, `gps_lon` | uniform random within Rwanda's bbox; unusable |
| `facility_name` | templated; contradicts `tier_level` in 53% of rows. Retained as a display label with no semantic content |
| `staff_per_delivery_2024` | unreconstructable, best of 8 formulas matched 58.1%, worse than the column's own mode at 65.8% |
| `avg_gestational_age` | uniform-sd-ratio 1.004, no facility anchor; carries no information |
| `apgar_less_7_at_5min` | independent of every clinical covariate it should track |
| `birth_weight_less_2500g` | r=0.018 against prematurity, where reality gives 0.6–0.9 |
| `preterm_births_28_32w`, `preterm_births_32_37w` | two fields, both independent of gestational age |

Unmapped means **not presented and not aggregated**. It does not mean deleted: bronze
retains every field verbatim, and the reason is recorded here so a later source with a
trustworthy version of the same field can bind it.

---

## 5. Open questions

**Is `province` an addressable object in its own right?** Resolved: yes, implicitly. Modelling
the hierarchy as `org_unit` with a `level` attribute makes `/unit/province/southern` fall out
for free. No separate object needed.

**Is `edition` addressable?** Resolved: yes. A quarterly bulletin the Director may quote must
be citable, and immutability-with-revisions is what lets a past quote still resolve to what
was actually seen.

Both open questions from `design.md` are now closed by the hierarchy decision.
