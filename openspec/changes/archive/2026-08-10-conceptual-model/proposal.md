## Why

ADR 0006 promoted end-to-end figure traceability from nice-to-have to a stated requirement,
after an adversarial council found the MoH Director's complaint is about trust rather than
throughput — *"I cannot trust any number I am shown."* The mechanism chosen for that is a
deeplink: click any figure in the bulletin, land on the rows and rules that produced it.

A deeplink is a URL for an object. Nothing downstream can be specified until the objects
have names: `trust-lineage` cannot say what a figure resolves *to*, `bulletin-render`
cannot emit hyperlinks, and `explore-surface` cannot hydrate state from parameters that
have not been defined.

There is also a live vocabulary conflict. DHIS2 says `orgUnit`, the sample CSVs say
`facility_id`, HealthTrack says facility, and the brief says site — for the same thing.
Ingestion cannot map to canonical names before canonical names exist.

## What Changes

- Establish the **object map**: the entities the system works with, their identity rules,
  their relationships, and their states.
- Establish the **ubiquitous language**: one canonical term per concept, with the source-system
  synonyms it reconciles. This is the vocabulary `ingest-mart`'s crosswalk maps *to*.
- Define the **deeplink URL contract**, separating two kinds of address that must not be
  conflated:
  - canonical object URLs — stable, shareable, one per addressable object
  - parameterised state URLs — a serialised selection in the explore surface, not an object
- Define **grain** explicitly for every metric-bearing object, so `facility-month`,
  `district-quarter`, and `facility-quarter` stop being implied by whichever query ran.
- Record which objects are **addressable** (may appear as a deeplink target) versus internal.
- **BREAKING** for nothing yet — no implementation exists. This change sets the contract that
  later capabilities are held to.

## Capabilities

### New Capabilities

- `conceptual-model`: the object map, identity and grain rules, ubiquitous language, and the
  deeplink URL contract that addresses those objects.

### Modified Capabilities

None — this is the first capability in the repository.

## Impact

- **Blocks**: `trust-lineage`, `ingest-mart`, `bulletin-render`, `explore-surface`,
  `geo-context`. Every one of them consumes either the vocabulary or the URL contract.
- **Constrains**: silver-layer column naming in `ingest-mart` — canonical terms defined here
  become `data_element` values there.
- **Constrains**: `bulletin-render` — every figure it emits must reference an addressable
  object defined here, or it cannot be deeplinked.
- **No code changes.** This produces specification only.
- **Method**: `jamiemill/layers-skills` Layer 5 (`/layers-conceptual-model`) for the object
  map and Layer 2 (`/layers-domain`) for the noun harvest and terminology conflicts.
- **Inputs**: the five sample CSVs, `decisions/0006-problem-a-plus-handover-act.md`,
  `decisions/0008-technical-stack.md`, DHIS2's data model, and the Bluelake Admin UI
  vocabulary reconstructed in `artifacts/01-bluelake-admin-ux-walkthrough.html`.
