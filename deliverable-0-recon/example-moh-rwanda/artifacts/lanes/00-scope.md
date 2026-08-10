# Scope — MECE research plan: Rwanda MoH digital-health landscape

**Stage:** scope · **Goal:** turn the research question into 7 MECE lane briefs · **Status:** plan only, no research executed in this file.

**Pipeline note:** `out/01-systems.md` already exists from a partial earlier run (L1 inventory: DHIS2/HMIS, OpenMRS EMR, eLMIS, RapidSMS→RapidPro, NHIC, RHIE). It is retained as a head-start for L1; lanes 2–7 are yet to run. This scope doc still defines **all** 7 lane briefs so the full run is reproducible and MECE from a single source.

---

## 0. How to read this plan

- **Method contract:** every lane follows the `deep-web-search` skill — two passes ("discover" breadth, then "double-click" depth on the 3–5 most central items), engines in priority order (Perplexity `sonar-pro` under `uv run --with litellm`, Parallel.ai `search`/`deep`, then native `web_fetch`/`web_search`), raw dumps under `out/.raw/`, and inline `[claim](url)` citations. Never rely on parametric memory for named systems/vendors/laws — verify against primary sources.
- **MECE partition (the whole = systems landscape):**
  - **L1** = the *nouns*: the inventory of systems (internal + external).
  - **L2–L4** = *attributes of those nouns*: where each runs (deployment), who builds/supplies it (vendors, incl. AI), and how it is protected in practice (in-system DP approach).
  - **L5** = the *actors*: personas and their journeys through the stack.
  - **L6** = the *edges*: how the systems connect and what data flows where.
  - **L7** = the *external constraint set*: Rwandan DP law + how health organisations (e.g. sandtech.com, comparable African platforms) architect compliance.
  - **Explicit boundaries:** L4 = what deployed systems *actually do* (consent capture, de-identification, access control, residency, audit, encryption) vs L7 = what the *law obliges* and how *organisations comply* (benchmark). L2 = physical/logical hosting + tiering vs L4 = security/privacy controls. L1 = the system itself vs L3 = the supplier (a vendor may supply many systems; each stays under one lane).
- **Output contract per lane:** `out/NN-<lane>.md` — overview (3–6 sentences), discovered inventory (bulleted, each item name + one line + source URL), double-click subsections, gaps + confidence (high/med/low), citations inline.
- **Artifact dependency:** L5 feeds the persona-journey map, L6 feeds the integration/data-flow diagram, L4+L7 feed the data-protection-posture section of the final HTML (exec summary · systems map · persona journeys · integration & data-flow · DP posture vs Law 058/2021).

---

## 1. Lane map

| # | Lane | File | Question it answers | Partition role |
|---|------|------|---------------------|----------------|
| 1 | Systems (internal + external) | `out/01-systems.md` | What digital-health systems exist and who owns them? | Nouns (inventory) |
| 2 | Deployment | `out/02-deployment.md` | Where is each system deployed (data centre / cloud / facility / community)? | Attribute: location |
| 3 | Vendors + AI | `out/03-vendors.md` | Who builds/supplies the systems — which AI vendors are in play? | Attribute: supplier |
| 4 | Data-protection approach (in-system) | `out/04-dp-approach.md` | How do the deployed systems handle data protection in practice? | Attribute: control posture |
| 5 | Personas + journeys | `out/05-personas.md` | Who uses the stack, and what are their end-to-end journeys? | Actors |
| 6 | Integration + data-flow | `out/06-integration.md` | How do the systems connect; what data flows where? | Edges |
| 7 | DP law + benchmark | `out/07-dp-law.md` | What does Rwandan law require, and how do health orgs comply? | External constraints |

---

## 2. L1 — Systems (internal + external) → `out/01-systems.md`

**Objective:** complete inventory of every digital-health system the Rwanda MoH runs or relies on, with purpose, owner, and status. (Head-start inventory exists — validate, correct, and extend it.)

**Key sub-questions:**
1. Which systems are **internal to MoH/RBC** — routine reporting, EMR, logistics, laboratory, community health, surveillance, civil registration, workforce, financing?
2. Which are **external/partner** platforms the MoH depends on (donor, WHO/Global Fund/PEPFAR, telecom, logistics/drone)?
3. For each system: purpose, owner (MoH vs RBC vs agency vs partner), current status (production / pilot / legacy / planned), and primary users.
4. What is the authoritative source for the national system portfolio (digital-health strategy 2024–2029, MoH/RBC websites, NHIC, tenders)?

**Candidate systems (verify, don't assume):**
- **Internal:** HMIS/RHMIS on DHIS2 (incl. program modules: TB, IDSR, immunization, malaria, NCD, COVID-19/vaccination, LMIS, health financing); OpenMRS-based EMR (eBuzima / cEMR); eLMIS (DHIS2/mSupply lineage); laboratory/LIMS (national lab information system); blood transfusion (CNTS); RapidSMS (legacy) → RapidPro (CHW reporting); eCHIS/CHW mobile tools (m'Ubuzima pilot); telemedicine (Babyl); National Health Intelligence Center (NHIC, launched Apr 2025); Rwanda Health Information Exchange (RHIE); disease surveillance (IDSR, EWARN); immunization registry; CRVS/vital registration linkage; health-workforce registry (HRIS); health-insurance/claims (RSSB, Mutuelle de Santé); pharmacy; radiology/PACS if present.
- **External/partner:** WHO (DHIS2 data-quality/immunization apps), Global Fund/PEPFAR program systems (e.g. DATIM), PIH/Inshuti Mu Buzima (OpenMRS), UNICEF (RapidPro), USAID/GIZ projects, Zipline (drone medical delivery), telecom + mobile-money rails (MTN/Airtel) where they carry health services.

**Search keywords:** `Rwanda MoH digital health systems list`, `Rwanda HMIS DHIS2 modules`, `Rwanda EMR OpenMRS eBuzima cEMR`, `Rwanda eLMIS`, `Rwanda laboratory information system LIMS`, `Rwanda RapidSMS RapidPro CHW`, `Rwanda NHIC National Health Intelligence Center`, `Rwanda RHIE`, `Rwanda digital health strategy 2024-2029`, `Rwanda telemedicine Babyl`, `Rwanda health workforce registry`, `Rwanda CRVS digital health`, `Rwanda blood transfusion information system`, `Rwanda health insurance digital claims RSSB Mutuelle`.

**Primary sources to target:** moh.gov.rw, RBC (rbc.gov.rw), nhic.moh.gov.rw, MINICT, HISP Rwanda, dhis2.org/docs.dhis2.org, OpenMRS, WHO/Global Fund/PEPFAR country pages, published tenders, peer-reviewed digital-health papers.

**Double-click targets:** DHIS2 platform (modules + users), OpenMRS EMR, NHIC, eLMIS, RHIE.

---

## 3. L2 — Deployment → `out/02-deployment.md`

**Objective:** where each system physically/logically runs, and the national→district→facility→community tiering.

**Key sub-questions:**
1. Per system: **national data centre** (which — NIB/government DC, RDB-hosted?), **cloud** (AWS/Azure/GCP — which provider/region, e.g. Babyl), **facility/on-prem** (hospital servers), or **community/mobile** (CHW tablets, SMS/USSD, apps)?
2. What is the hosting/ownership split between MoH/RBC, HISP Rwanda, and private/donor operators?
3. What are the **connectivity assumptions** at each tier (4G/5G coverage, offline-first sync for CHWs)?
4. What **data-residency and DR/backup** posture applies per system?
5. Where do donor-owned systems physically live (e.g. DATIM in the US; DHIS2 cloud regions)?

**Candidate deployment targets (verify per system):** national government data centre / RDB data centres; cloud regions used by partner platforms; RBC-hosted servers; hospital/health-centre on-prem; CHW tablets + SMS gateways; drone logistics network (Zipline distribution centres).

**Search keywords:** `Rwanda MoH DHIS2 hosting`, `Rwanda national data centre health systems`, `Rwanda government data centre NIB RDB`, `Rwanda EMR deployment district hospitals on-prem`, `Rwanda CHW tablet eCHIS deployment`, `Rwanda health facility connectivity 4G offline-first`, `Babyl Rwanda cloud hosting`, `Rwanda NHIC infrastructure hosting`, `Rwanda health data residency`.

**Primary sources to target:** MoH/RBC infrastructure announcements, MINICT/NCSA, HISP Rwanda, DHIS2 user stories, vendor/partner engineering pages, tender documents.

**Double-click targets:** DHIS2 hosting arrangement, OpenMRS facility deployment model, NHIC infrastructure.

---

## 4. L3 — Vendors + AI → `out/03-vendors.md`

**Objective:** who supplies the MoH stack, with **emphasis on AI vendors** (product, integration point, data used).

**Key sub-questions:**
1. Which **implementers/integrators** supply the MoH stack (HISP Rwanda, PIH/Inshuti Mu Buzima, Dimagi, Ona, Viamo, Text to Change, Jembi, local Rwandan firms)?
2. Which **AI vendors** are active — triage/chatbots, diagnostics/imaging, forecasting/supply-chain, CHW decision support, analytics?
3. Per vendor: product, **integration point** in the stack, **data used** (inputs/outputs), contract/grant context if public.
4. What is the MoH/Rwanda **AI policy** context (national AI strategy, health-AI governance)?

**Candidate vendors (verify):** HISP Rwanda; PIH/Inshuti Mu Buzima; Dimagi (CommCare lineage); Ona Systems; Viamo; Text to Change; Babyl (AI triage/telemedicine); Zipline (AI logistics); AI diagnostics/radiology players; NLP/chatbot vendors (e.g. MoH chatbot initiatives); DHIS2/HISP ecosystem; local startups (e.g. m'Ubuzima-era CHW tools).

**Search keywords:** `Rwanda MoH health IT vendors`, `HISP Rwanda DHIS2 implementer`, `Rwanda EMR vendor OpenMRS PIH`, `Babyl Rwanda AI triage`, `Rwanda health AI chatbot`, `Zipline Rwanda drones AI logistics`, `Rwanda AI diagnostics radiology`, `Rwanda AI in health startups`, `Rwanda MoH tender digital health vendors`, `Rwanda national AI policy health`.

**Primary sources to target:** MoH/RBC procurement announcements, company press releases + engineering blogs, tender portals, DHIS2 annual conference coverage, Rwanda ICT/AI strategy documents.

**Double-click targets:** every AI vendor (product → integration point → data used), plus HISP Rwanda's role.

---

## 5. L4 — Data-protection approach (in-system) → `out/04-dp-approach.md`

**Objective:** how deployed systems handle data protection **in practice** — the operational posture, not the law (law = L7).

**Key sub-questions:**
1. **Consent capture:** where and how is patient consent captured (explicit at registration? verbal for CHW? implied for routine reporting)?
2. **De-identification:** anonymisation/pseudonymisation in DHIS2 reporting, NHIC analytics, and research extracts.
3. **Access control:** RBAC per role (clinician, DHO, national analyst); facility-level scoping; who can see what.
4. **Data residency & flows:** where PHI physically resides; cross-border flows to donor/cloud systems.
5. **Audit & incident:** audit logging, encryption at rest/in transit, breach-response practice.
6. **Standards:** ISO 27001 or equivalent security posture claimed/observed per system.

**Candidate DP postures to characterise (verify per system):** DHIS2/RBC security configuration; OpenMRS role-based access + audit design; NHIC data-governance layer; CHW SMS/tablet data capture (PII minimisation); telemedicine (Babyl) consent + records; lab/LIMS result confidentiality.

**Search keywords:** `Rwanda health data privacy practices systems`, `DHIS2 Rwanda data security configuration`, `Rwanda EMR access control audit`, `Rwanda health data anonymization NHIC`, `Rwanda patient consent digital health`, `Rwanda CHW data collection privacy`, `OpenMRS security Rwanda`, `Rwanda health data encryption residency`, `ISO 27001 Rwanda health systems`.

**Primary sources to target:** system documentation (DHIS2/HISP, OpenMRS, NHIC), MoH/RBC data-governance documents, partner technical reports, peer-reviewed assessments.

**Double-click targets:** DHIS2/RBC security design, OpenMRS EMR DP design, NHIC data handling.

---

## 6. L5 — Personas + journeys → `out/05-personas.md`

**Objective:** the six mandated personas and **one clear end-to-end journey each** through the systems they touch (feeds the persona map in the artifact).

**Key sub-questions:**
1. **Policy/planning** (MoH leadership, MINECOFIN, development partners): dashboard/analytics journeys (NHIC), financing data, evidence-to-decision flow.
2. **Epidemiology/surveillance** (RBC, district surveillance officers): IDSR/EWARN case reporting, outbreak alert → investigation → response journey.
3. **Hospitals/clinicians** (referral + district hospitals, health centres): registration → consultation → lab → pharmacy → discharge on EMR; telemedicine consult journey.
4. **District health** (District Health Officers, district hospital managers): supervision, data review, logistics ordering, performance dashboards.
5. **Community health workers** (CHWs/Binômes): home visits, antenatal/postnatal follow-up, SMS/tablet reporting, referral escalation, decision-support prompts.
6. **Citizens/patients:** insurance enrollment (Mutuelle/RSSB), facility visit, telemedicine, vaccination records, any patient-facing apps/portals.
7. Per persona: goals, systems touched (ordered), pain points, data produced/consumed.

**Candidate journey anchors (verify):** eCHIS/RapidPro CHW flows; OpenMRS clinician workflow; IDSR/EWARN alert chain; NHIC policy dashboard; RSSB/Mutuelle claims; Babyl patient app; Zipline delivery to facility staff.

**Search keywords:** `Rwanda CHW eCHIS workflow digital`, `Rwanda community health workers digital tools journey`, `Rwanda clinician EMR workflow hospital`, `Rwanda IDSR surveillance outbreak workflow`, `Rwanda NHIC dashboard policy use`, `Rwanda Mutuelle de sante digital enrollment claims`, `Rwanda telemedicine patient journey Babyl`, `Rwanda health worker digital tools UX`.

**Primary sources to target:** MoH CHD strategic plan, RBC surveillance protocols, OpenMRS/HISP user stories, NHIC about pages, UNICEF/WHO case studies, academic evaluations.

**Double-click targets:** CHW journey, clinician EMR journey, epidemiology outbreak journey.

---

## 7. L6 — Integration + data-flow → `out/06-integration.md`

**Objective:** how disparate systems connect, and an explicit list of data-flow edges (source → destination : payload).

**Key sub-questions:**
1. **Interoperability architecture:** RHIE status, OpenHIE patterns, middleware (e.g. OpenHIM), standards (HL7 FHIR, HL7 v2, ADX, DHIS2 APIs, OpenMRS REST, SMS).
2. **Registries:** master patient index / unique patient identifier (NIDA ID linkage), facility registry, health-worker registry.
3. **Data-flow edges:** enumerate who sends what to whom — e.g. RapidSMS/RapidPro → DHIS2; EMR → RHIE → NHIC; eLMIS → DHIS2; lab → NHIC; CRVS → NHIC; insurance claims ↔ RSSB.
4. **Mechanics:** APIs vs file/SMS fallback, offline sync, message queues, real-time vs batch.
5. **Barriers/gaps:** standards not yet implemented, missing registry, RHIE production status.

**Candidate integration points (verify):** RHIE (OpenHIM/FHIR), DHIS2 API + ADX, OpenMRS REST/webservices, NHIC ingestion layer, unique-patient-ID initiative, national ID (NIDA) linkage, mobile-money/telecom APIs, government interoperability (RISA/Irembo).

**Search keywords:** `Rwanda Health Information Exchange RHIE`, `Rwanda OpenHIE interoperability`, `Rwanda FHIR HL7 health exchange`, `Rwanda unique patient identifier`, `Rwanda EMR DHIS2 integration`, `Rwanda RapidPro DHIS2 integration`, `Rwanda master patient index`, `Rwanda NHIC data sources integration`, `Rwanda digital health interoperability framework`, `OpenHIM Rwanda`.

**Primary sources to target:** RHIE/OpenHIE publications, ResearchGate architecture papers, HISP Rwanda, MoH digital-health strategy, NHIC announcements, NIDA/RISA documents.

**Double-click targets:** RHIE/interoperability layer, NHIC ingestion, unique-patient-ID initiative. **Output must include** a bulleted edge list `source -> destination : payload`.

---

## 8. L7 — DP law + benchmark → `out/07-dp-law.md`

**Objective:** the Rwandan legal regime for health data + how health organisations (sandtech.com and comparable African digital-health platforms) architect compliance.

**Key sub-questions:**
1. **Law No. 058/2021** relating to the protection of personal data and privacy: scope, **health data as sensitive data**, controller/processor duties, consent rules, data-subject rights, **cross-border transfer** conditions, DPO appointment, penalties; implementation status (regulations, supervisory authority).
2. **NCSA** cybersecurity guidance and any health-sector DP guidance; interaction with e-health regulations.
3. **Benchmark — sandtech.com:** how does this health-software org architect DP compliance (data residency, consent, access control/ReBAC, audit, DPO, breach handling)? What is publicly documented?
4. **Benchmark — comparable platforms:** how other African digital-health platforms/EMR/HIE/telemedicine operators implement Law-058-style regimes (or GDPR analogues) — residency choices, consent capture, ReBAC, audit trails, DPO function, breach process.
5. Map each legal obligation → concrete control (the "how orgs solve it" layer).

**Candidate benchmark orgs (verify):** sandtech.com; DHIS2/HISP operators in the region; OpenMRS/PIH deployments; telemedicine providers in East Africa; cloud hosts serving African health data; Rwanda-registered health-tech firms.

**Search keywords:** `Rwanda Law 058/2021 personal data protection`, `Rwanda data protection authority health data`, `Rwanda NCSA data protection guidance`, `Rwanda cross-border transfer personal data`, `Rwanda sensitive health data law`, `Rwanda DPO obligation 058/2021`, `sandtech.com health data protection compliance`, `African digital health data protection compliance`, `health data residency architecture Africa`, `DHIS2 GDPR compliance data protection`.

**Primary sources to target:** official gazette / RURA-NCSA publications, law firm summaries, sandtech.com site + engineering content, platform privacy policies, academic/DPO commentary.

**Double-click targets:** sandtech.com's approach, 2–3 comparable platform approaches, the Law-058→control mapping.

---

## 9. MECE verification

- **Exhaustive (collectively):** any fact about the landscape lands in exactly one lane — a system (L1), its location (L2), its supplier (L3), its DP controls (L4), its users (L5), its connections (L6), or the law/benchmark governing it (L7).
- **Exclusive (mutually):** L4 (what systems do) vs L7 (what law demands + how orgs comply) are separated by the in-practice vs normative boundary; L2 (where) vs L4 (how protected) by hosting vs controls; L1 (systems) vs L3 (suppliers) by product vs producer.
- **Coverage gate:** the downstream `coverage` node asserts all 8 markdowns + the HTML artifact exist and are non-empty; this plan supplies the briefs those lanes execute against.
- **Confidence rule:** every lane ends with a gaps + confidence note (high/med/low); MoH-internal system detail is expected to be thin in public sources — flag rather than invent.
