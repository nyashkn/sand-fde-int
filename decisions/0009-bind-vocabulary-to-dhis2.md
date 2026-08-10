# 0009 — Bind the vocabulary to DHIS2; invent only where no standard exists

- **Date:** 2026-08-10
- **Status:** Accepted
- **Method:** noun harvest across four sources — 66 distinct fields in the sample CSVs, the
  Bluelake Admin UI, the DHIS2 data model, and the brief

## Context

Four sources name the same domain differently, and one of them contradicts itself. Bluelake
labels the same entity **Health Post** in its chart titles and **Facility** in its filter
bar, on the same screen. The sample CSVs say `facility_id`. DHIS2 says `orgUnit`. The brief
uses "facility" and "site" interchangeably.

Nothing downstream can proceed through that. `ingest-mart`'s crosswalk maps source fields
*to* canonical terms, so the canonical terms must exist first. Deeplinks address objects, so
the objects must be named.

The tempting move is to author a clean project vocabulary — pick the clearest word for each
concept, unencumbered by any legacy system's awkwardness.

## Decision

**Bind to DHIS2 as the primary vocabulary.** `org_unit`, `period`, `data_element` are taken
directly from the DHIS2 data model. Rwanda runs DHIS2; it is the country's existing language,
not a legacy system we are tolerating.

**Extend with ICD-10 and WHO GHO where DHIS2 is silent.** Cause-of-death elements bind to
ICD-10 perinatal codes (P21 asphyxia, P07 prematurity, P36 sepsis, Q00–Q99 congenital).
Indicator definitions bind to WHO GHO, so a published rate is comparable to national
reporting rather than bespoke.

**Adopt the DHIS2 hierarchy shape, not the sample's flattening.** The sample stores
`district` and `province` as string columns on a facility row. DHIS2 models the whole
administrative tree as `orgUnit` at different levels. We take the DHIS2 shape: one type, a
level attribute, a parent reference. A district figure and a facility figure become the same
kind of object, addressable by one URL pattern.

**Invent exactly two terms, both recorded with a reason.**

| Term | Why not the standard's word |
|---|---|
| `observation` | DHIS2 calls this a `dataValue`. Ours carries provenance, batch identity, and state; `dataValue` reads as a bare scalar and would understate it. |
| `edition` | No standard term exists for a published bulletin for a period. |

**Record every source synonym rather than discarding it.** Health Post, Facility, site, and
`facility_id` all resolve to `org_unit` through a recorded mapping that is inspectable
without reading code.

## Alternatives

- **Author a clean project vocabulary.** Rejected. Every term would need translating back to
  DHIS2 at handover, which is precisely the cost a ubiquitous language exists to remove. It
  also fails the ADR 0006 test: a named DHO restarting this alone should meet words their
  own HMIS already uses.
- **Adopt Bluelake's vocabulary**, on the grounds that it is the Sand product this work sits
  beside. Rejected — it is internally inconsistent (Health Post versus Facility on one
  screen), and it is a product vocabulary rather than a national data standard.
- **Adopt the sample CSVs' field names**, since they are what the pipeline actually ingests.
  Rejected — they are an artifact of one export, `facility_id` prefixes are ambiguous across
  seven districts, and 9 of 66 fields are unusable. Binding canonical names to a defective
  export would bake the defects into the vocabulary.
- **Model district and province as separate object types**, mirroring the sample's shape.
  Rejected — it triples the URL patterns, forces three near-identical aggregation paths, and
  diverges from DHIS2 for no gain.
- **Invent nothing; force every concept onto an existing standard term.** Rejected — it would
  have meant calling a provenance-bearing, state-carrying record a `dataValue`, which
  misleads about what the object is.

## Reverses if

- Rwanda migrates off DHIS2, which would make the binding a translation cost rather than a
  saving.
- A source arrives whose concepts genuinely do not fit the `orgUnit`/`period`/`dataElement`
  triple — patient-level clinical data would be the obvious case, and would call for FHIR
  rather than an extension of this vocabulary.
- The two invented terms turn out to have published equivalents we missed.

## Honest limits

The noun harvest covers four sources. Two systems named in the brief — CommCare and the
immunisation Excel workbook — were not available and are unrepresented. Their terms are
recorded as expected future synonyms, not as reconciled ones.

Binding to DHIS2 imports its awkwardness: long `dataElement` names and opaque UIDs. That
cost is accepted deliberately in exchange for interoperability with the system the Ministry
already runs.

## Artifacts

- `openspec/changes/conceptual-model/model.md` — the terminology conflict table, object map,
  and URL contract this decision produces
- `openspec/changes/conceptual-model/specs/conceptual-model/spec.md` — the requirements it
  is held to
