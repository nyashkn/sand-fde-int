# Lane 05 — Personas across the Rwanda MoH digital-health stack

**Lane:** L5 / Personas
**Date:** 2026-08-09
**Method:** Six persona-targeted deep searches via Perplexity sonar-pro (OpenRouter); one breadth-discovery pass via Parallel.ai; targeted native `web_fetch` against primary sources (MoH, WHO, OpenHIE, HISP Rwanda, RSSB, Resolve to Save Lives, Forbes, PMC).
**Raw dumps:** `out/.raw/pplx_*_journey.json` (6 files) + `out/.raw/parallel_personas_discover.json`
**Reads from:** `out/01-systems.md` (systems inventory), `out/02-deployment.md` (hosting topology), `out/04-dp-approach.md` (consent + SOP regime)

## Overview

Six personas interact with the Rwanda MoH digital-health stack end-to-end. Each one touches a different slice of the layered architecture described in lanes 01–02:

| # | Persona | Primary digital surface | Secondary systems |
|---|---|---|---|
| 1 | National policy / planning analyst (NHIC) | NHIC data portal (`nhic.moh.gov.rw`) | DHIS2, eIDSR, OpenMRS aggregate feeds |
| 2 | Epi / surveillance officer (IDSR / eIDSR) | DHIS2 Tracker (`tracker.moh.gov.rw`) | IDSR line lists, eIDSR push alerts |
| 3 | Hospital clinician (OpenMRS eBuzima) | OpenMRS at district/referral hospitals | DHIS2 monthly aggregate, SHR via RHIE |
| 4 | District Health Officer (DHO + PBF) | DHIS2 + PBF dashboard (`aggregate.moh.gov.rw/pbfrwanda`) | HWMS workforce data |
| 5 | Community Health Worker (CHW) | RapidSMS → RapidPro, emerging eCHIS / cEMR | HMIS aggregate feed |
| 6 | Citizen / patient | RSSB Mutuelle de Santé card, Babyl (until Aug 2023) | Facility EMR encounter records |

The MoH owns the data; partners implement and host the tools. Each persona's journey below is anchored to the named source systems and the primary documentation/press URLs that were fetched.

---

## Persona 1 — National Policy / Planning Analyst (NHIC user)

**Source: NHIC launch page ([moh.gov.rw](https://www.moh.gov.rw/news-details/national-health-intelligence-center-launched-to-strengthen-data-driven-decision-making-in-rwanda-s-health-sector)) and NHIC data portal ([nhic.moh.gov.rw](https://nhic.moh.gov.rw/)).**

**Goals.** Convert fragmented, multi-source health data into ministerial dashboards that drive national policy (resource allocation, pandemic preparedness, UHC progress).

**Systems touched.** NHIC (the 6-layer "data lake → AI/analytics → dashboard" stack), DHIS2 national instance, eIDSR, OpenMRS aggregate feeds, HMIS, SISCOM (community reports).

**End-to-end journey.**

1. **Read morning brief.** Analyst logs in to the NHIC data portal at `https://nhic.moh.gov.rw/` and opens an NHIC-built executive dashboard (e.g., maternal & child health trends, epidemic signals). Per the NHIC "About" page, the portal is positioned as "a centralized platform for processing, integrating, triangulating, and analyzing real-time health data using advanced technological tools and artificial intelligence" launched in **April 2025** ([nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)).
2. **Trace a signal to source.** A spike in district-level malaria admissions triggers drill-down. NHIC's "12 data sources" include community health workers, health posts, health centers, district and referral hospitals, and disease-prevention/surveillance domains — meaning the analyst can pivot from a chart to the originating dataset without leaving the portal ([nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)).
3. **Cross-check surveillance lineage.** The signal is corroborated against eIDSR case-based reports (DHIS2 Tracker instance at `cbs2.moh.gov.rw/idsr`) and against the DHIS2 Tracker case-based surveillance built with HISP Rwanda ([HISP Rwanda DHIS2 page](https://www.dhis2.org/hisp-rwanda)). This triangulates what was reported vs. what facilities actually saw.
4. **Pull workforce and supply context.** The analyst overlays HWMS (Health Workforce Management System, part of the MoH 4×4 reform — [MoH 4×4 page](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)) and eLMIS supply indicators to see whether the spike aligns with HRH gaps or stockouts.
5. **Draft policy brief.** Outputs are packaged into a ministerial briefing. The WHO case study notes Rwanda's HIS "represents a noteworthy example of country-driven HIS strengthening — an example of a country taking ownership and leadership in using data to inform decision-making" ([WHO Data-Driven Development: Rwanda Pioneering HIS](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)).
6. **Feed back into planning.** Brief informs MoH strategic-plan adjustments (Health Sector Strategic Plan IV alignment, NHIC's 6-layer architecture roadmap).

**Data produced / consumed.** Consumes all 12 NHIC source streams (CHW data, IDSR, HMIS, EMR aggregates, SISCOM, PBF, FBF, hepatitis, HIV/RBC, immunization, etc.). Produces ministerial dashboards, briefings, AI-assisted forecasts.

---

## Persona 2 — Epi / Surveillance Officer (IDSR / eIDSR)

**Source: WHO Rwanda HIS case study ([WHO Data-Driven Development](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)); HISP Rwanda DHIS2 page ([dhis2.org/hisp-rwanda](https://www.dhis2.org/hisp-rwanda)); MoH HMIS landing page ([moh.gov.rw](https://www.moh.gov.rw/)).**

**Goals.** Detect, confirm, and respond to notifiable diseases and outbreaks within 24 hours; maintain IDSR line lists; produce weekly epidemiological reports.

**Systems touched.** DHIS2 Tracker (eIDSR), DHIS2 aggregate, HMIS portal (`aggregate.moh.gov.rw`), MoH lab/SMS gateways (formerly RapidSMS, now RapidPro), NHIC dashboards.

**End-to-end journey.**

1. **Receive alert.** A health-center clinician or CHW flags a suspected notifiable condition (e.g., measles, cholera, COVID-19). Per WHO's documentation, "Rwanda has used DHIS2 as its national health information system since 2012 and has made significant progress" with electronic IDSR ([WHO HIS case study](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)).
2. **Case entered into eIDSR Tracker.** The case is recorded into DHIS2 Tracker's case-based surveillance model at `https://cbs2.moh.gov.rw/idsr`. The MoH HMIS landing lists this as one of the dedicated CBS domains ([moh.gov.rw](https://www.moh.gov.rw/)). The Tracker model "tracks individual cases, enabling follow-up and case-based surveillance" per HISP Rwanda ([dhis2.org/hisp-rwanda](https://www.dhis2.org/hisp-rwanda)).
3. **Lab linkage.** Specimens and lab results are linked to the case record (e.g., HIV case-based surveillance is "functional at 166 sites" per CDC Rwanda's country page — [CDC in Rwanda](https://www.cdc.gov/global-health/countries/rwanda.html)).
4. **Outbreak detection / threshold logic.** DHIS2's program rules trigger automatic alerts when thresholds are crossed. The officer sees the alert in their Tracker dashboard.
5. **Daily/weekly bulletin.** Aggregate IDSR data rolls up to national bulletins; per WHO, Rwanda's eIDSR is the cornerstone of "real-time data for informed policy decisions and system optimization" via NHIC ([WHO case study](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)).
6. **COVID-style case management loop.** During the pandemic, Rwanda adapted DHIS2 modules for case management and contact tracing, as documented in the "Digital health systems to support pandemic response in Rwanda" brief ([sciforce.com](https://www.sciforce.com/wp-content/uploads/2021/04/Digital-health-systems-to-support-pandemic-response-in-Rwanda.pdf)).

**Data produced / consumed.** Consumes suspected-case notifications from facilities + CHWs. Produces case line lists, weekly epi bulletins, outbreak alerts, lab-linked records. Feeds NHIC and DHIS2 national aggregates.

---

## Persona 3 — Hospital Clinician (OpenMRS eBuzima)

**Source: OpenHIE RHIE impact story ([openhie.org](https://ohie.org/rwanda-hie-impact/)), PMC IeDEA paper on OpenMRS NIDA de-identification ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5422632/)), MoH HMIS landing ([moh.gov.rw](https://www.moh.gov.rw/)).**

**Goals.** Document patient encounters (HIV, TB, NCDs, maternal); enable continuity of care; support research use-cases via de-identified extracts; satisfy monthly HMIS reporting.

**Systems touched.** OpenMRS "eBuzima" at district and referral hospitals; SHR (OpenMRS instance at central level) connected via the RHIE/HIE exchange; DHIS2 monthly aggregate upload; OpenHIE-compliant interoperability layer (FHIR + SHR + Client Registry).

**End-to-end journey.**

1. **Patient arrives at hospital.** Clinician searches the Shared Health Record (SHR) via the RHIE Client Registry — per OpenHIE's case study, "in Rwanda the HIE includes a Shared Health Record (SHR) and Client Registry to ensure that client information is accessible across multiple EMR instances" ([OpenHIE RHIE story](https://ohie.org/rwanda-hie-impact/)).
2. **Encounter documented in OpenMRS eBuzima.** Doctor opens the patient chart in OpenMRS (eBuzima distro deployed at district/referral hospitals per systems inventory). Encounters, labs, ART/TB regimens are recorded.
3. **Cross-facility lookup via SHR.** If the patient was seen at another facility, the clinician pulls prior diagnoses and medications through the SHR. Rwanda's HIE architecture uses "CR (Client Registry) + FHIR + SHR" as the canonical pattern ([OpenHIE RHIE story](https://ohie.org/rwanda-hie-impact/)).
4. **Monthly HMIS upload.** Aggregate indicators from OpenMRS are pushed to DHIS2 via the MoH HMIS "Monthly report Tool to collect monthly clinical data from all health facilities" ([moh.gov.rw](https://www.moh.gov.rw/)).
5. **Research extract (where applicable).** For IeDEA consortium HIV research, the OpenMRS NIDA module runs de-identification on a snapshot; per the PMC paper, the workflow "implements the NIDA (National Institute on Drug Abuse) dataverse de-identification pipeline within OpenMRS" so research datasets leave the EMR scrubbed of identifiers ([PMC IeDEA](https://pmc.ncbi.nlm.nih.gov/articles/PMC5422632/)).
6. **Reporting loop.** Aggregate flows up to NHIC (Persona 1), informing national planning; individual records remain in OpenMRS and SHR.

**Data produced / consumed.** Produces encounter-level clinical data + monthly HMIS aggregates + de-identified research extracts. Consumes SHR-prior records, lab results, ART regimens.

---

## Persona 4 — District Health Officer (DHO + PBF)

**Source: MoH HMIS landing ([moh.gov.rw](https://www.moh.gov.rw/)), MoH 4×4 workforce reform ([moh.gov.rw](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)).**

**Goals.** Monitor district performance against indicators; verify PBF (Performance-Based Financing) claims; manage CHW cooperatives; allocate staff per the 4×4 reform.

**Systems touched.** DHIS2 district dashboards; PBF dashboard (`aggregate.moh.gov.rw/pbfrwanda`); SISCOM (CHW monthly reports from health centers — see MoH HMIS landing); HWMS (workforce registry).

**End-to-end journey.**

1. **Open DHIS2 district dashboard.** DHO logs in and reviews monthly service-delivery indicators for the district (ANC, deliveries, immunization, OPD).
2. **Review PBF claims.** Performance-Based Financing verification uses the dedicated PBF dashboard at `https://aggregate.moh.gov.rw/pbfrwanda` ([moh.gov.rw](https://www.moh.gov.rw/)). Facilities submit quantity + quality scores; DHO and MoH verifiers cross-check against HMIS.
3. **CHW performance review.** The DHO pulls SISCOM (CHW monthly reports from health centers) to assess cooperative productivity. CHWs are organized into cooperatives supervised by the health center; performance-linked incentives are central to the model ([Rwanda CHW Program summary](https://chwcentral.org/wp-content/uploads/2015/02/Rwanda-CHW-Program-Summary.pdf)).
4. **Workforce allocation under 4×4 reform.** Using HWMS data, the DHO verifies deployment of the new "4 per health-center" staffing rule (4 general practitioners + 4 nurse anesthetists in each health center per the 4×4 reform — [MoH 4×4](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)).
5. **Performance contract / Imihigo.** District-level performance is rolled up to feed national Imihigo performance contracts.
6. **Feed NHIC.** Indicators aggregate upward; NHIC consumes the district's cleaned HMIS stream ([nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)).

**Data produced / consumed.** Consumes HMIS aggregates, PBF claims, CHW cooperative reports. Produces district performance reviews, PBF verification, CHW cooperative supervision notes.

---

## Persona 5 — Community Health Worker (CHW)

**Source: Resolve to Save Lives + New Times coverage ([resolvetosavelives.org](https://resolvetosavelives.org/about/news/rwanda-launches-the-next-generation-of-digital-tools-for-community-health/)); CHW Central ([chwcentral.org](https://chwcentral.org/wp-content/uploads/2015/02/Rwanda-CHW-Program-Summary.pdf)); PMC mHealth usability study ([PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)).**

**Goals.** Conduct integrated community case management (iCCM); register pregnancies and newborns; deliver maternal-child health, nutrition, and NCD screening; submit monthly SISCOM reports; flag suspected outbreaks.

**Systems touched.** Legacy RapidSMS (now transitioning to RapidPro for case-based messaging — see L1 inventory); emerging eCHIS / cEMR on smartphones; HMIS via SISCOM; new digital CHW tools (Resolve-supported: d-IDS for community-level integrated disease surveillance, cEMR, eCHIS).

**End-to-end journey.**

1. **Receive work list on phone.** The CHW opens the cEMR / eCHIS app to see assigned households for the day. Per the Resolve to Save Lives + Government of Rwanda launch, "Rwanda launches the next generation of digital tools for community health" — a suite including d-IDS (community surveillance), cEMR (community EMR), and eCHIS ([resolvetosavelives.org](https://resolvetosavelives.org/about/news/rwanda-launches-the-next-generation-of-digital-tools-for-community-health/)). The New Times coverage frames these as "the future of community health" ([newtimes.co.rw](https://www.newtimes.co.rw/article/248405/News/rwanda-launches-next-generation-of-digital-tools-for-community-health)).
2. **Conduct household visit.** CHW uses the smartphone app to register pregnant women, track antenatal care attendance, screen for malnutrition, and screen for NCDs (Rwanda has >45,000 active CHWs, ~1/4 focused on maternal & newborn health — [PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)).
3. **Symptom screening + clinical decision support.** For maternal cases (e.g., post-cesarean follow-up), the mHealth-CHW app (built by Insightiv + Harvard + PIH/IMB) prompts a symptom-based questionnaire and uses a machine-learning image classifier on incision photos to predict surgical-site infection, operating offline ([PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)). Usability research in Kirehe District showed 100% of CHWs agreed/strongly agreed with ≥80% of usability statements.
4. **Refer or treat at the household.** CHW either administers treatment (iCCM) or refers to the health center. The app pushes decision-support prompts on when to refer.
5. **Submit monthly SISCOM report.** Aggregated household-level indicators (pregnancies, deliveries, child deaths, malnutrition, TB suspects) are sent to the supervising health center; the health center compiles the SISCOM submission into DHIS2 ([moh.gov.rw](https://www.moh.gov.rw/)).
6. **Trigger surveillance alert.** If a CHW suspects a notifiable disease, the d-IDS module pushes a case notification directly to eIDSR (DHIS2 Tracker), closing the loop to Persona 2.

**Data produced / consumed.** Produces household-level CHW records, SISCOM aggregates, d-IDS alerts. Consumes work lists, app content, training materials.

---

## Persona 6 — Citizen / Patient

**Source: RSSB Mutual Health Insurance page ([rssb.rw](https://www.rssb.rw/rssb-products/mutuelle-de-sante-cbhi/)); Forbes Babyl shutdown coverage ([forbes.com](https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/)).**

**Goals.** Enroll in insurance; access services at health facilities; use teleconsultation or digital health ID where available; verify entitlements.

**Systems touched.** RSSB Mutuelle de Santé (CBHI) enrollment and membership verification (now managed by RSSB after merger with former health-insurance bodies); facility EMR (OpenMRS / DHIS2) at point of service; formerly Babyl (SMS/USSD teleconsultation, ~2.8M registered users, shut down August 2023 per Forbes).

**End-to-end journey.**

1. **Enroll in Mutuelle de Santé.** Household head registers with the local cell coordinator; premiums are collected (via RSSB channels after the 2022 transition that merged CBHI into RSSB — [RSSB Mutuelle de Santé page](https://www.rssb.rw/rssb-products/mutuelle-de-sante-cbhi/)). Per the strategic purchasing literature, "in 2019, 83% of Rwandan women and men ages 15 to 49 had health insurance; of those, 93% were members of the CBHI scheme" ([Lu et al. CBHI strategic purchasing analysis](https://gatesopenresearch.org/articles/4-177/v2)).
2. **Receive membership card / digital proof.** Member receives a paper card and (where digitized) a record keyed to national ID.
3. **Visit health center.** Patient presents at the health center. The clinician verifies Mutuelle eligibility via the facility's intake process; the encounter is recorded in OpenMRS (hospital) or DHIS2 (health-center aggregate).
4. **Teleconsultation (when available).** Until August 2023, Babyl provided SMS/USSD-based teleconsultations and had reached ~2.8M registered users before abruptly shutting down ([Forbes](https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/)). The platform's closure left a service gap that other digital channels have had to absorb.
5. **Service billed / captured.** Service is rendered; the facility records the encounter (paper or digital) and bills against CBHI/RSSB.
6. **Aggregate flows upward.** Anonymized encounter data flows into DHIS2 monthly reports → NHIC dashboards.

**Data produced / consumed.** Produces enrollment records, premium payments, encounter-level utilization. Consumes membership verification, teleconsultation advice.

---

## Persona × System touchpoint matrix

| Persona | DHIS2 aggregate | DHIS2 Tracker (eIDSR) | OpenMRS / SHR / RHIE | NHIC portal | HWMS | eLMIS | RapidSMS / RapidPro / eCHIS / cEMR / d-IDS | PBF | RSSB Mutuelle / Babyl (legacy) |
|---|---|---|---|---|---|---|---|---|---|
| 1. NHIC policy analyst | ✓ | ✓ | ✓ (agg) | ✓ (primary) | ✓ | ✓ | ✓ (via feeds) | ✓ | — |
| 2. Epi / surveillance officer | ✓ | ✓ (primary) | — | ✓ | — | — | ✓ (d-IDS alerts in) | — | — |
| 3. Hospital clinician | ✓ (monthly upload) | — | ✓ (primary) | — | — | — | — | — | — (eligibility check) |
| 4. District Health Officer | ✓ (primary) | ✓ | — | ✓ | ✓ | ✓ | ✓ (via SISCOM) | ✓ | — |
| 5. CHW | ✓ (via SISCOM) | ✓ (d-IDS push) | — | — | — | — | ✓ (primary) | — | — |
| 6. Citizen / patient | — | — | ✓ (at facility) | — | — | — | — | — | ✓ |

---

## Cross-cutting observations

- **Two flows close the loop.** CHW → eIDSR (Persona 5 → Persona 2) and facility EMR → DHIS2 aggregate → NHIC (Personas 3 & 4 → Persona 1) are the two data-return paths that distinguish a "live" HIS from a passive reporting system. Rwanda has both operational.
- **One endpoint is dark for citizens.** Babyl's 2023 shutdown ([Forbes](https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/)) means the citizen persona has no direct digital channel today; the MoH focus has shifted to facility-anchored digital touchpoints.
- **Workforce is becoming digital.** The 4×4 reform brings HWMS + CSAM (Civil Service Attribute Management) into the DHO persona's daily life ([MoH 4×4](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)).
- **AI is moving to the edge.** Insightiv's post-c-section SSI image classifier is the first documented CHW-side ML use ([PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)); NHIC advertises AI as core to its 6-layer stack ([nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)).

---

## Source bibliography (inline citations)

- MoH, *National Health Intelligence Center launched to strengthen data-driven decision-making in Rwanda's health sector* — [moh.gov.rw](https://www.moh.gov.rw/news-details/national-health-intelligence-center-launched-to-strengthen-data-driven-decision-making-in-rwanda-s-health-sector)
- NHIC Data Portal, *About* — [nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)
- WHO, *Data-Driven Development: Rwanda Pioneering HIS* — [extranet.who.int](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)
- HISP Rwanda / DHIS2, *Rwanda Tracker case-based surveillance* — [dhis2.org/hisp-rwanda](https://www.dhis2.org/hisp-rwanda)
- OpenHIE, *Rwanda HIE Impact Story* — [openhie.org](https://ohie.org/rwanda-hie-impact/)
- PMC, *IeDEA — OpenMRS NIDA de-identification* — [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC5422632/)
- MoH HMIS landing — [moh.gov.rw](https://www.moh.gov.rw/)
- MoH, *Rwanda pioneers the 4×4 reform* — [moh.gov.rw](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)
- Resolve to Save Lives, *Rwanda launches next-generation digital tools for community health* — [resolvetosavelives.org](https://resolvetosavelives.org/about/news/rwanda-launches-the-next-generation-of-digital-tools-for-community-health/)
- New Times, *Rwanda launches next-generation digital tools for community health* — [newtimes.co.rw](https://www.newtimes.co.rw/article/248405/News/rwanda-launches-next-generation-of-digital-tools-for-community-health)
- Estrada et al. (PMC12838494), *Community health workers' usability and acceptability of an mHealth tool for post-cesarean assessments in rural Rwanda* — [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)
- CHW Central, *Rwanda CHW Program Summary* — [chwcentral.org](https://chwcentral.org/wp-content/uploads/2015/02/Rwanda-CHW-Program-Summary.pdf)
- CDC, *CDC in Rwanda* — [cdc.gov](https://www.cdc.gov/global-health/countries/rwanda.html)
- RSSB, *Mutuelle de Santé (CBHI)* — [rssb.rw](https://www.rssb.rw/rssb-products/mutuelle-de-sante-cbhi/)
- Forbes, *Babyl Rwanda shuts down operations* (Aug 2023) — [forbes.com](https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/)
- Lu et al., *Strengths and weaknesses of strategic health purchasing for UHC in Rwanda* — [gatesopenresearch.org](https://gatesopenresearch.org/articles/4-177/v2)
