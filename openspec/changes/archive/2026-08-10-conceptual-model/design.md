## Context

See `proposal.md`, Why.

Constraints that shape the approach:

- The sample data forces most identity decisions. `gps_lat`/`gps_lon` are uniform random
  within Rwanda's bbox, so no object may take spatial identity. `facility_id` prefixes are
  ambiguous, `NYA` maps to seven districts. `facility_name` contradicts `tier_level` in 62
  of 117 rows. `district` and `province` are correct 30/30 against real Rwanda structure and
  are the only trustworthy geography.
- The reporting period is partial: 2024-01 and 2024-03 are duplicated for every facility
  with differing values, and 2024-02 and 2024-12 are absent. Any object spanning a quarter
  is incomplete for Q1 and Q4 by construction.
- Rwanda runs DHIS2. Its data model is the country's existing vocabulary, so the canonical
  terms are largely a binding exercise, not an authoring one.
- The bulletin is delivered as HTML embedded in email. Canonical URLs must survive being
  pasted into a mail client and clicked days later with no session.

## Goals / Non-Goals

**Goals:**

- One canonical term per concept, with every source synonym recorded against it.
- Identity rules that survive an ambiguous or fabricated source key.
- A URL contract that distinguishes an object address from a serialised selection.
- Grain declared per object, so no metric can be presented without one.

**Non-Goals:**

- Patient-level modelling. This is aggregate reporting; no object represents a person.
- Modelling source systems not present in the sample (CommCare, immunisation Excel).
  Recorded as future synonyms only.
- Authorisation or visibility rules. Object addressability is about linkability, not access.
- Physical storage layout. That belongs to `ingest-mart`.

## Decisions

**Bind canonical terms to DHIS2, extend with ICD-10, invent nothing else.**
`orgUnit`, `period`, and `dataElement` come from DHIS2; cause-of-death terms bind to ICD-10
perinatal P-codes. *Alternative considered:* authoring a clean project vocabulary. Rejected,
the MoH already speaks DHIS2, and a competing vocabulary would have to be translated back at
handover, which is precisely the cost the ubiquitous language exists to avoid.

**Identity is `(source_system, source_key)` resolved to a surrogate, never the source key
alone.** *Alternative considered:* using `facility_id` directly. Rejected because the prefix
is ambiguous across seven districts and the sample's keys are not real DHIS2 UIDs, so
adopting them would bake a fabricated identifier into the canonical layer.

**Grain is a declared property of the object, not of the query.** *Alternative considered:*
inferring grain from `GROUP BY`. Rejected, it makes mixed-grain aggregation silently
possible, and the spec requires refusing it.

**Two URL forms, distinguished by shape rather than convention.** Canonical object URLs are
path-based and carry no query parameters that affect identity. Explore state is a single
opaque parameter on a distinct path root. *Alternative considered:* one URL space with
optional filters. Rejected, the bulletin must be unable to emit a state URL by accident,
and a structural difference makes that checkable rather than a review habit.

**Completeness is an enumerated object state, not a derived warning.** A quarter missing a
source period is *incomplete*, and that state travels with the object into every rendering.
*Alternative considered:* a footnote at render time. Rejected, a footnote is attached by the
renderer and can be dropped by a different renderer; a state on the object cannot.

**Unmeasured and zero are different states.** An entity with no source rows is unmeasured.
*Alternative considered:* coalescing to zero for chart continuity. Rejected, on a per-entity
accountability table, a rendered zero is read as a measured result and is materially
misleading.

## Risks / Trade-offs

- **Canonical URLs must stay stable while the mart is still moving** → derive them from
  identity and grain only, never from storage paths or row offsets.
- **Binding to DHIS2 imports its awkwardness** (long `dataElement` names, UID opacity) →
  accepted deliberately; the interoperability is worth more than the ergonomics.
- **Declared grain adds friction to every new metric** → that is the intent; the friction is
  what prevents a mixed-grain figure reaching a Minister.
- **A closed object set can block a late requirement** → adding an object is a spec delta,
  which is cheap; the alternative is unaddressable figures.
- **Surrogate identity adds a resolution step at ingest** → contained to one place, and it is
  the same step the crosswalk already performs.

## Migration Plan

None. No implementation exists; this establishes the contract that later capabilities are
held to. `ingest-mart` consumes the vocabulary, `trust-lineage` and `bulletin-render`
consume the URL contract.

## Open Questions

- Whether provinces need to be addressable objects in their own right, or only as an
  attribute of district. Deferrable: it adds an object without changing any existing one.
- Whether the bulletin itself is an addressable object (a citable quarterly edition) or
  merely a rendering of district and facility objects. Deferrable: affects one URL, not the
  identity or grain rules.
