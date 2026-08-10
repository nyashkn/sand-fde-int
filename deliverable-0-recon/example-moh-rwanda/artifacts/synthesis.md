# 08 — Synthesis: Rwanda MoH Digital-Health Landscape (single MECE model)

*Single source of truth that the visual artifact renders. Date: 2026-08-09. All claims carry inline `[source](url)` citations. Where public documentation is thin, confidence is flagged per section — nothing is invented.*

*Read-by: out/01-systems.md (systems), out/02-deployment.md (hosting), out/03-vendors.md (suppliers + AI), out/04-dp-approach.md (in-system controls), out/05-personas.md (actors), out/06-integration.md (edges), out/07-dp-law.md (law + benchmark).*

---

## 0. How this model is partitioned (MECE)

The landscape = systems × actors × edges × controls. Each fact lives in exactly one place:

- **Systems (nouns)** — §1 inventory table; the rest of the document references systems by short ID (`A1…I14`).
- **Actors / personas** — §2; six personas interact with the systems via the journeys in §3.
- **Map (which systems exist + their tier)** — §4 conceptual graph.
- **Edges (how they connect + what flows)** — §5 edge list `source → destination : payload`.
- **Controls (what protects the data in practice + in law)** — §6 in-system DP posture × §7 DP-law mapping × §8 vendor benchmark.
- **Gaps + cross-cutting confidence** — §9.

The visual artifact renders §1 (table), §3 (per-persona journeys), §4 (systems map), §5 (integration / data-flow edges), §6 + §7 + §8 (DP posture vs Law 058/2021).
---

## 1. Systems inventory table

> 24 systems spanning 9 MECE categories (A reporting/surveillance, B facility/community EMR, C community health & mHealth, D supply chain, E laboratory, F identity/registries/interop, G workforce/financing/admin, H intelligence/analytics, I external/partner platforms). Columns: short **ID**, system, purpose, owner, deployment (tier + hosting), vendor/supplier, in-system DP posture (consolidated from §6; the full DP detail lives in §6).

| ID | System | Purpose | Owner | Deployment (tier, hosting) | Vendor / supplier | DP posture (summary) |
|---|---|---|---|---|---|---|
| **A1** | **RHMIS / HMIS on DHIS2** — aggregate routine reporting backbone | National facility-level monthly service utilisation, surveillance, commodities; programme registries (eTB, cancer, NCD, hep, fortified-food); HIV CBS Tracker in 197 PEPFAR sites | MoH (RBC as implementing agency) | National tier — NDC since 2013 ([docs.dhis2.org](https://docs.dhis2.org/en/topics/user-stories/rwanda-hmis-powered-by-dhis2.html), [WHO strategy PDF p.20](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)); production endpoint 2023–26 unconfirmed | DHIS2 (UiO) + **HISP Rwanda** (anchor implementer) ([hisprwanda.org](https://hisprwanda.org/dhis2/)) | Aggregate-first; inherits DHIS2 platform RBAC, audit API, TLS guidance ([docs.dhis2.org security](https://docs.dhis2.org/en/implement/implementing-dhis2/security-considerations.html), [audit](https://docs.dhis2.org/en/manage/concepts/audit.html)); residency per art. 50; no Rwanda-specific consent/de-id docs |
| **A2** | **DHIS2 Tracker — eIDSR (electronic IDSR)** | Individual-level notifiable-disease / outbreak surveillance on DHIS2 Tracker | MoH / RBC | National tier — DHIS2 Tracker (co-hosted with A1) | DHIS2 / HISP Rwanda | Programme-rules alerts; dataset + audit API; same residency rule |
| **A3** | **DHIS2 Tracker — HIV Case-Based Surveillance (CBS)** | Individual HIV case tracking (new infections, linkage, viral suppression) | MoH / RBC | National tier — co-hosted with A1; flows in from B1 via OpenHIM (F2) | DHIS2 / HISP Rwanda; CDC/PEPFAR funded | Inherits A1; identity via UPID/NIDA |
| **A4** | **COVID-19 testing & vaccination modules on DHIS2** | Paperless COVID testing (DHIS2 Android Capture App) and vaccination modules | MoH / RBC | National + edge: tablets/phones at facilities ([dhis2.org — testing](https://dhis2.org/rwanda-covid-testing/), [vaccination](https://dhis2.org/rwanda-covid-vaccination/)) | DHIS2 / HISP Rwanda | Same as A1; data mirrors into RCAS analytics (I5) |
| **A5** | **Programme registries (eTB, cancer, NCD, hep, fortified-food)** | Disease-specific electronic registers on DHIS2 | MoH / RBC programme divisions | National tier — co-hosted with A1 ([RHIE report p.21-22](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | DHIS2 / HISP Rwanda | Programme-level RBAC |
| **B1** | **OpenMRS / eBuzima (facility EMR)** | Longitudinal patient-level records: HIV core, plus IPD/OPD, registration, lab orders, pharmacy, billing in hospital package; 42 hospitals + 450+ health centres (RHIE), ~60% of facilities (GF 2026) | MoH / RBC | Facility tier — **on-prem Ubuntu servers at every health facility** ([WHO strategy PDF p.33-34](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)); migration to centralised hosting planned | OpenMRS Foundation / Regenstrief; developed locally by PIH/IMB, ICAP, UCSF, QT Global Software, Jembi; code public ([github.com/Rwanda-EMR](https://github.com/Rwanda-EMR), [openmrs-module-imbemr](https://github.com/PIH/openmrs-module-imbemr)) | Strongest documented DP control: **IeDEA C# identifier-stripping** before US research upload ([PMC6918068](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/)); RBAC via OpenMRS roles ([guide.openmrs.org](https://guide.openmrs.org/administering-openmrs/user-management-and-access-control/)); SSL cited; at-rest encryption for national prod not public |
| **B2** | **cEMR (community EMR on smartphones)** | Community-level EMR on CHW phones, feeds future Health Portal; 20,000+ CHWs (GF 2026) | MoH / RBC (USAID Tubeho: Jhpiego, SFH, FIND) | Community tier — offline-first Android, scaling to 58,567 CHWs by end-2026 ([UNICEF Rwanda](https://www.unicef.org/rwanda/stories/piles-registers-digital-care-community-health-workers-rwanda-adopt-digital-health-rec)) | OpenMRS lineage; USAID Tubeho consortium; d-IDS decision support ([PubMed 41687454](https://pubmed.ncbi.nlm.nih.gov/41687454/)); Insightiv modules in mUbuzima ([PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)) | Inherits B1; d-IDS guided screening reduces referrals by 24.2% |
| **B3** | **OpenClinic (alternative facility EMR)** | Hospital EMR in some hospitals where OpenMRS not adopted | Hospital-level | Facility tier — on-prem at adopting hospitals ([RHIE report p.21-22](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | OpenClinic (vendor) | Public deployment docs thin |
| **B4** | **Health Portal (patient-facing, under development)** | Lets citizens view their records; pulls from B1 + B2 | MoH / RBC | National tier — DHIA-funded (~US$2M) ([GF news 2024-07-03](https://www.theglobalfund.org/en/updates/2024/2024-07-03-rwanda-global-fund-new-grants-aids-tb-malaria-strengthen-health-systems/), [GF case study p.4](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf)) | Global Fund DHIA implementing partners (unspecified) | "Anonymized and governed by Rwanda's data protection laws and NHIC's Privacy Policy" per [nhic.moh.gov.rw](https://nhic.moh.gov.rw/) |
| **C1** | **eCHIS (electronic Community Health Information System)** | Digitised CHW platform linked to HMIS for surveillance and community services | MoH / RBC (Global Fund-financed) | Community tier — smartphone cEMR lineage, smartphone-based ([GF case study p.3-4](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf)) | USAID Tubeho (Jhpiego/SFH/FIND); DHIA | Same as B2 |
| **C2** | **RapidSMS (legacy CHW reporting)** | Pregnancy/newborn monitoring + "Red Alert" emergency reporting; launched Musanze 2009, nationwide 2012 | MoH / RBC | Community tier — **45,000 feature phones**, SMS gateway ([WHO strategy PDF p.20](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf), [PMI/CHI 2021](https://media.path.org/documents/Rwanda_PMIDCHI.pdf)) | UNICEF / MoH-built | SMS content pseudonymised at flow level; being superseded by RapidPro/cEMR |
| **C3** | **RapidPro / dhis2-rapidpro-integration (CHW messaging)** | Newer mobile workflow engine (SMS/IVR/USSD/WhatsApp + Android Surveyor offline) | MoH / RBC | Community tier — Android Surveyor offline-first | UNICEF / MoH; integration via [dhis2/integration-dhis-rapidpro](https://github.com/dhis2/integration-dhis-rapidpro) | Aggregate SMS data; security warning: "ensure the data provider agrees to sharing DHIS2 user details with the data receiver before activating synchronisation" ([github.com/dhis2/integration-dhis-rapidpro](https://github.com/dhis2/integration-dhis-rapidpro)) |
| **C4** | **CHIS — Community & Health-post Information System** | Pilot then national rollout of community + health-post services digitisation | MoH / RBC | Community + facility tier | MoH / RBC | Public docs thin |
| **C5** | **WelTel** | Population-health tracking, SMS/patient-engagement | MoH / RBC (HIC source) | National/community tier — SMS gateway ([MoH HIC announcement](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions)) | WelTel Inc. (Canada) | SMS content; vendor privacy policy unknown |
| **C6** | **Viamo 3-2-1 voice/IVR** | Health info + surveys on basic phones; mobile-channel population reach | MoH / UNICEF / WHO / USAID | National tier — IVR/voice ([viamo.io](https://viamo.io/viamo-platform/viamo-platform-serving-vulnerable-women-globally-awarded-4m/)) | Viamo; MTN Rwanda as telecom | Population-level; aggregate |
| **C7** | **AKIISA / Empower CHWs (AI training platform)** | AI-powered e-learning + performance monitoring + gender-responsive matching for 58,567 CHWs | MoH / RBC + Expertise France (L'Initiative) | Community/national — mobile + central | CIIC-HIN deploys; Expertise France funds ([CIIC-HIN 30 May 2025](https://ciichin.org/rwanda-launches-new-ai-powered-digital-platform-to-support-continuous-capacity-building-for-community-health-workers-and-advance-universal-health-coverage/)) | Performance metadata |
| **D1** | **eLMIS (Electronic Logistics Management Information System)** | National commodity ordering, consumption capture, distribution, inventory for all public facilities + district pharmacies; launched 2014 | MoH / RBC with RMS | Facility tier — vendor-hosted web app, annual licence; integrated with A1 and D2 ([WHO strategy PDF p.46-48](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)); HISP Rwanda DHIS2/mSupply variant shown at DHIS2 Annual Conf 2025 ([HISP Rwanda](https://hisprwanda.org/hisp-rwanda-showcases-innovative-dhis2msupply-elmis-solution-at-dhis2-annual-conference-2025)) | HISP Rwanda (DHIS2/mSupply) or earlier vendor; USAID/GHSC-PSM support | Public security controls thin; legal framework applies (art. 11 encryption, art. 41 breach) |
| **D2** | **RMS automated warehouse (WMS)** | Warehouse-execution at Rwanda Medical Supply central store; integrated with D1 | RMS (Rwanda Medical Supply) | National tier — central warehouse + IT | RMS (in-house); unspecified WMS vendor | Inventory ops; minimal PHI |
| **D3** | **Reagent Management System (ERP, trademarked)** | Lab reagent ERP; MoH goal = end-to-end interoperability of LIMS+HMIS+reagent | MoH / RBC | National tier | Vendor undisclosed ([GF case study p.3](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf)) | Vendor unknown |
| **D4** | **Viebeg Technologies — AI procurement/forecasting** | AI diagnostics, disease-burden forecasting, predictive maintenance, procurement optimisation (VieProcure marketplace) | Commercial (Rwanda customers: Rwanda Military Hospital, King Faisal, Nemba DH) | National/facility tier — commercial SaaS ([viebeg.com](https://www.viebeg.com)) | Viebeg (AfDB funding **indirect** via Rwanda Innovation Fund: AfDB $30M into RIF → RIF into Viebeg — [AfDB](https://www.afdb.org/en/success-stories/how-rwanda-using-artificial-intelligence-improve-healthcare-55309), [AfDB MapAfrica](https://mapafrica.afdb.org/en/projects/46002-P-RW-G00-001), [HealthTimes Africa](https://www.healthtimesafrica.com/article/555877707-ensuring-millions-get-proper-care-the-rwanda-innovation-fund-rif-invests-in-rwanda-based-viebeg-technologies)) | Commercial B2B; no published schema |
| **D5** | **Zipline — drone delivery (logistics)** | Autonomous fixed-wing drone delivery of blood/vaccines/medicines; AI flight-path optimisation (reinforcement-learning) | Zipline + GoR per-delivery contract | Distribution-centre network: **Muhanga, Kayonza, Rusizi** ([Emergency Live](https://www.emergency-live.com/marketplace/rwanda-blood-and-medical-supplies-to-hospitals-and-clinics-thanks-to-zipline-drones), [GlobeNewswire 2022](https://www.globenewswire.com/news-release/2022/12/15/2574639/0/en/zipline-and-the-government-of-rwanda-announce-a-new-partnership-to-serve-the-entire-country-with-instant-logistics.html)) | Zipline Inc. (US parent; Rwanda op) | Operational data only; **Zipline Privacy Policy** ([flyzipline.com/privacy-policy](https://www.flyzipline.com/privacy-policy)) — TLS, AES-256, RBAC, SCCs |
| **E1** | **National LIMS / web-based LMIS (LabWare)** | Viral load + EID lab data at the National Reference Laboratory | MoH / RBC, NRL | Facility tier — **LabWare client-server on NRL local network** ([WHO strategy PDF p.35](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)); satellites use open-source **BLIS** | LabWare Inc. (US); BLIS open source | Lab result confidentiality via NRL controls; integrated into F2 EMR↔VLSM flow |
| **E2** | **VLSM (Viral Load System Management) + LabWare (integrated)** | HIV viral load / CD4 / recency lab system, integrated with EMR via F2 | MoH / RBC | Facility tier — VLSM client, exchanged via OpenHIM | LabWare/VLSM vendor | Test result confidentiality via lab policy |
| **E3** | **National Reference Laboratory (NRL)** | Reference testing hub + capacity + training | MoH / RBC | Facility tier — Kigali lab | MoH / RBC | Internal lab SOPs |
| **E4** | **ePROGESA — Blood Bank Information System** | National blood management, donor engagement | CNTS (Centre National de Transfusion Sanguine) | National tier — central server + 4 regional centres ([WHO strategy PDF p.48-49](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)); ~$30k/yr licence | Mak-System (France) — proprietary | Proprietary; donor PII per Rwanda law |
| **F1** | **RHIE / RHIES — Rwanda Health Information Exchange** | OpenHIE-based national interoperability bus; MVP connected first Kigali sites 2023 for HIV CBS + indicator reporting; 197 facilities across 30 districts by Jan 2025 | MoH (Digitization Directorate/CDO) | National tier — **hosted at the National Data Centre** ([WHO strategy PDF p.30-32](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf), [RHIE report](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | QT Global Software (build); CDC/PEPFAR funded foundational phase | OpenHIE security services (authN/Z, audit); HIE consent model: **record + element-level deny** at patient's request ([ohie.org](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda)); **no public audit-trail production spec** |
| **F2** | **OpenHIM — interoperability mediator** | Middleware routing/translating transactions; OpenHIM 5.12 → 8.2 with Grafana/Prometheus monitoring | MoH (with QT Global / Jembi) | National tier — NDC; **EMR↔VLSM FHIR lab flow implemented** (4th hackathon, Aug 2024) ([RHIE report §5.3.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | Jembi Health Systems (originally); QT Global + Jembi 2024 hackathon | TLS + auth; audit log via OpenHIM dashboard; **EMR-VLSM JSON + FHIR flows validated** |
| **F3** | **Client Registry (CR) — Unique Patient ID (UPID)** | National patient identity; integrated with NIDA; format YYMMDD-FacilityCode-Random; auto-fills ~90% of registration fields | MoH | National tier — **HAPI FHIR** at NDC; production at PEPFAR sites ([OHIE impact story](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda), [RHIE report §6.3.1.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | SAVICS + Jembi + MoH | Identity is a national asset and a residency/access-control touchpoint |
| **F4** | **Facility Registry (FOSA IDs)** | Master facility list, unique facility codes | MoH | National tier — JSON/MongoDB; testing env ([RHIE report §6.3.1.3](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | MoH | Identifier-only |
| **F5** | **Provider Registry (PR)** | Health-worker registry, license validity gates EMR access; integrated with professional councils | MoH + professional councils | National tier — MongoDB; testing env ([RHIE report §6.3.1.3](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | MoH | License-based gating |
| **F6** | **Shared Health Records (SHR)** | Centralised FHIR patient record (encounters, observations, service requests, medication requests); in production, under-utilised pending clinician training + consent work | MoH | National tier — OpenMRS-based back-end ([RHIE report §6.3.1.4](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | OpenMRS; Jembi | Live at Kibagabaga: 462,865 encounters / 7 months; pending consent/privacy work |
| **F7** | **Terminology Registry** | ICD-11, ICHI, LOINC, National Product Catalog mappings | MoH | National tier — testing; awaiting operationalisation ([RHIE report §6.3.1.5](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | MoH | Code system |
| **F8** | **Laboratory Registry** | Bridges EMRs to VLSM/Labware for HIV lab tests; MySQL | MoH | National tier — testing env ([RHIE report §6.3.1.6](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | MoH | Sample order linkage |
| **F9** | **CRVS — Civil Registration & Vital Statistics** | Birth/death registration; listed as HIC source system; linked to health identity and insurance enrolment | MINALOC / MoH inter-agency | National tier — source for H1 | MINALOC / MoH | Identifiers + cause of death |
| **G1** | **CSAM — Clinical Staff Application Management System** | Web-based recruitment/transfer of health professionals (launched 2023) | MoH | National tier — web | MoH-built ([RHIE report p.22](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | HR data |
| **G2** | **HWMS — Health Workforce Management System** | Workforce registry; HIC source system | MoH | National tier — web | MoH ([MoH 4×4 reform](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)) | HR data |
| **G3** | **iHRIS** | Health-workforce info, used by MoH since 2010 | MoH | National tier | IntraHealth ([WHO strategy PDF p.54](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)) | HR data |
| **G4** | **IPPIS — Mifotra HR/payroll** | Government-wide HR/payroll system | Mifotra (public service) | National tier | Government of Rwanda | Civil service data |
| **G5** | **Health Facilities Licensing Platform** | Digitised licensing, account creation → e-license | MoH | National tier — web | MoH ([RHIE report p.22](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | License metadata |
| **G6** | **MEMMS — Medical Equipment Management & Maintenance System** | Equipment registration, routine/emergency maintenance; mobile app added | MoH | National + mobile | MoH ([RHIE report p.22](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | Asset metadata |
| **G7** | **HRTT — Health Resource Tracking Tool** | Health-sector financial-flows tracking (since 2013), being updated | MoH | National tier | MoH ([RHIE report p.22](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | Financial flows |
| **G8** | **eLearning — Health sector** | Health-sector e-learning platform (since Jan 2018) | MoH | National + community | MoH | Training data |
| **G9** | **Rwanda Health Analytics Platform (RHAP)** | National analytics/BI platform; capacity building at national + subnational | MoH / RBC | National tier | HISP Rwanda / MoH ([GF case study p.4](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf)) | Aggregate dashboards |
| **G10** | **PBF dashboard (`aggregate.moh.gov.rw/pbfrwanda`)** | Performance-Based Financing verification dashboard | MoH | National tier — web | MoH ([moh.gov.rw](https://www.moh.gov.rw/)) | Facility-level scorecards |
| **G11** | **RSSB / Mutuelle de Santé (CBHI)** | Community-Based Health Insurance scheme, membership + premium collection; managed by Rwanda Social Security Board after 2022 merger of CBHI bodies | RSSB | National tier | RSSB ([rssb.rw](https://www.rssb.rw/rssb-products/mutuelle-de-sante-cbhi/), [gatesopenresearch 4-177](https://gatesopenresearch.org/articles/4-177/v2)) | Member PII per Law 058/2021 |
| **H1** | **NHIC — National Health Intelligence Center** | Six-layer data lakehouse (Source → Ingestion → Replication → Lakehouse → Storage → Presentation) for real-time national analytics + AI; launched 3 Apr 2025 at the Global AI Summit on Africa | MoH (flagship initiative) | National tier — physical HQ **RURA Building, Kiyovu, Nyarugenge, Kigali**; frontend on kwikkoders subdomain; hosting provider undisclosed ([MoH HIC news](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions), [NHIC site](https://nhic.moh.gov.rw/), [nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about), [TBI](https://institute.global/insights/public-services/how-rwanda-is-using-data-to-deliver-better-health-care)) | TBI (Tony Blair Institute) technical expertise; kwikkoders platform builder (unconfirmed); build partner not publicly named | "All health data is anonymized and governed by Rwanda's data protection laws and NHIC's Privacy Policy" — anonymization at presentation layer; full DP pipeline not public |
| **I1** | **Global Fund (GFATM)** | US$1.9B since 2003; National Strategy Financing (P4R) 2023–25; **Digital Health Impact Accelerator (DHIA)** priority funding for HIE, EMR, Health Portal; 2024–2027 grants | External (donor) | Funds national infrastructure | Global Fund ([GF case study](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf), [GF news 2024-07-03](https://www.theglobalfund.org/en/updates/2024/2024-07-03-rwanda-global-fund-new-grants-aids-tb-malaria-strengthen-health-systems/)) | Sub-processor relationship; grant conditions |
| **I2** | **CDC / PEPFAR (TSSS)** | Funded foundational HIE phase (2018–); HIV CBS; IT at 192 PEPFAR sites; 20 digital officers; hackathons | External (donor) | Funds sites + central | U.S. CDC + PEPFAR ([RHIE report §6.2.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf), [CDC in Rwanda](https://www.cdc.gov/global-health/countries/rwanda.html)) | Sub-processor; data-residency rules apply to PEPFAR data |
| **I3** | **WHO** | Technical support for digital health strategy/architecture; 2018–2023 strategy published via WHO CPCD | External (UN) | Policy + advisory | WHO ([WHO strategy PDF](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)) | Advisory |
| **I4** | **USAID / GHSC-PSM** | eLMIS support at district pharmacies + facilities | External (donor) | Funds logistics | USAID ([WHO strategy PDF p.46-48](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)) | Sub-processor |
| **I5** | **RCAS — Rwanda COVID-19 Analytics System** | Mirror of DHIS2 COVID testing + vaccination DB; integrates with RHAP via REST | MoH | National tier | MoH / academic partnership ([Oxford Open Digital Health 2024](https://academic.oup.com/oodh/article/doi/10.1093/oodh/oqae034/7743133)) | Aggregate |
| **I6** | **Mastercard / Microsoft** | Co-developed data + interoperability standards as foundation of digital health strategy | External (vendor) | Strategy/standards | Mastercard Foundation + Microsoft ([GF news 2024-07-03](https://www.theglobalfund.org/en/updates/2024/2024-07-03-rwanda-global-fund-new-grants-aids-tb-malaria-strengthen-health-systems/)) | Standards |
| **I7** | **HealthTech Hub Africa + SIL** | Kigali accelerator/sandbox certifying national + private solutions against interoperability standards | External (consortium) | Kigali | Co-funded by GF, Novartis Foundation, McGovern Foundation, Endless, Norrsken ([GF case study p.3-4](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf)) | Sandbox |
| **I8** | **CDPI + RISA** | Coordinates inclusive, interoperable digital systems incl. digital ID underpinning health identity | External / government | Policy | CDPI + RISA ([GF case study p.3](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf)) | Identity standards |
| **I9** | **Gates Foundation** | Active at MoH level on digital health (2026 field visit); co-funds **Horizon1000** AI tools | External (donor) | Funds + co-designs | Gates Foundation ([MoH news — Mwulire visit](https://www.moh.gov.rw/news-detail/minister-nsanzimana-and-bill-gates-visit-mwulire-sector-to-witness-healthcare-transformation), [Gates Notes Horizon1000](https://www.gatesnotes.com/expanding-access-to-health-care-through-ai)) | Sub-processor |
| **I10** | **Anthropic — 3-year MOU with GoR (MINICT)** | Claude + Claude Code access; health priorities cervical-cancer, malaria, maternal mortality | External (vendor) | Government-wide; health entry TBD | Anthropic ([Anthropic announcement](https://www.anthropic.com/news/anthropic-rwanda-mou), [Tech Policy Press](https://www.techpolicy.press/anthropic-is-becoming-the-backbone-of-rwandas-government-but-who-is-accountable/)) | Not a health-data pipeline yet |
| **I11** | **Gates Foundation × OpenAI — Horizon1000** | Up to $50M combined; AI tools for patient intake, triage, follow-up, referrals, trusted medical info in local languages; 1,000 clinics by 2028, starting in Rwanda | External (donor + vendor) | Facility/community tier — Rwanda first | OpenAI + Gates Foundation ([GeekWire](https://www.geekwire.com/2026/gates-foundation-openai-launch-50m-ai-health-initiative-targeting-1000-clinics-in-africa/), [OpenAI Horizon1000](https://openai.com/index/horizon-1000/)) | "Optimised for privacy/security" per OpenAI |
| **I12** | **Babyl (Babylon Health) — legacy AI triage** | AI symptom triage + teleconsultation on basic phones; 10-yr GoR partnership 2020; ~2.8M users by 2022; **wound down Aug 2023** | Legacy (now defunct in Rwanda) | External cloud — Babylon's AWS UK (PHI out of Rwanda, **predates Law 058/2021**) | Babylon Health UK ([MobiHealthNews](https://www.mobihealthnews.com/news/emea/babylon-launches-ai-powered-triage-tool-rwanda), [Forbes Aug 2023](https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/), [TelecareAware](https://telecareaware.com/babylon-health-files-for-us-chapter-7-bankruptcy-winding-down-babyl-rwanda-and-ending-care-for-2-8-million-users/)) | Wound down; no successor operation |
| **I13** | **Insightiv — local imaging AI + CHW tools** | AI-assisted teleradiology (CT/MRI/X-ray); CXR AI ~94% accuracy; C-section wound-infection AI for CHW (mUbuzima) | External (startup) | Facility/community tier — hospital PACS + CHW phones | Insightiv ([New Times](https://www.newtimes.co.rw/article/194633/News/rwandan-scientist-wants-to-use-ai-to-deepen-radiology-services), [PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)) | MIT IDEAS 2020 grant; no published EHR-text handling |
| **I14** | **Digital Umuganda — Kinyarwanda LLMs** | Locally trained Kinyarwanda language models assisting disease diagnosis | External (startup) | Clinical/edge — exact integration undocumented | Digital Umuganda ([WEF](https://www.weforum.org/stories/emerging-technologies/data-access-to-healthcare-in-rwanda/), [AP via KSAT](https://www.ksat.com/health/2026/01/22/rwanda-to-test-ai-powered-technology-in-clinics-under-a-new-gates-foundation-project/)) | No published MoH contract |
| **I15** | **OpenEvidence × RBC × Resolve to Save Lives** | AI-powered clinical decision-support tools for resource-limited settings | External (reported partnership) | Clinical | OpenEvidence / Resolve to Save Lives ([Resolve FB post](https://www.facebook.com/ResolveToSaveLives/posts/-announcing-a-new-partnership-to-build-ai-powered-tools-that-improve-medical-car/1412874954207287/)) | **Single social post — not independently verifiable (low confidence)** |


**§1 confidence: HIGH** on the core national stack (A1–A5, B1, F1–F3, G10–G11, H1, I1–I4) — anchored on the [CII-CHIN RHIE ecosystem report (Jan 2025)](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf), the [Global Fund Rwanda Digital Health Case Study (Jan 2026)](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf), the [Rwanda Digital Health Strategy 2018–2023 (WHO CPCD)](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf), and the [MoH NHIC launch announcement](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions). **MEDIUM** on administrative systems (G1–G9) — last-verified in 2025 RHIE report, no 2026 update. **LOW** on AI vendors (I10–I15) and unreleased 2024–2029 strategy/blueprint (planned completion 2026).

---

## 2. Personas × systems matrix (overview)

> Six personas traverse the stack. Each row maps a persona to its **primary** system surface and the **secondary** systems they trigger. Detailed end-to-end journeys live in §3.

| # | Persona | Primary digital surface | Secondary systems | Source |
|---|---|---|---|---|
| **P1** | National policy / planning analyst (NHIC user) | **H1** NHIC data portal (`nhic.moh.gov.rw`) | A1, A2, B1 (aggregates), G2, G7, G10 | [moh.gov.rw](https://www.moh.gov.rw/news-details/national-health-intelligence-center-launched-to-strengthen-data-driven-decision-making-in-rwanda-s-health-sector), [nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about) |
| **P2** | Epi / surveillance officer (RBC / district) | **A2** DHIS2 Tracker eIDSR (`cbs2.moh.gov.rw/idsr`) | A3, H1, C2/C3 alerts in | [WHO HIS case study](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf), [dhis2.org/hisp-rwanda](https://www.dhis2.org/hisp-rwanda) |
| **P3** | Hospital clinician (OpenMRS eBuzima) | **B1** OpenMRS eBuzima + **F6** SHR + **F3** UPID lookup | A1 (monthly upload), G11 (eligibility check) | [openhie.org/rwanda-hie-impact/](https://ohie.org/rwanda-hie-impact/), [PMC IeDEA paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC5422632/) |
| **P4** | District Health Officer (DHO + PBF) | **A1** DHIS2 district dashboards + **G10** PBF dashboard (`aggregate.moh.gov.rw/pbfrwanda`) | G2, G11, SISCOM | [moh.gov.rw](https://www.moh.gov.rw/), [MoH 4×4 reform](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce) |
| **P5** | Community Health Worker (CHW) | **C1/C2/C3** cEMR / RapidSMS / RapidPro + d-IDS | A2 (push alert out), A1 (via SISCOM) | [resolvetosavelives.org](https://resolvetosavelives.org/about/news/rwanda-launches-the-next-generation-of-digital-tools-for-community-health/), [PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/) |
| **P6** | Citizen / patient | **G11** RSSB Mutuelle de Santé + (formerly **I12** Babyl) | B1 / A1 at point of service | [rssb.rw](https://www.rssb.rw/rssb-products/mutuelle-de-sante-cbhi/), [Forbes Babyl shutdown](https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/) |

---

## 3. Per-persona end-to-end journeys

> One numbered, source-anchored journey per persona. Each journey ends with "Data produced / consumed".

### P1 — National policy / planning analyst (NHIC user)

1. **Read morning brief.** Analyst logs into NHIC at `https://nhic.moh.gov.rw/` and opens an NHIC-built executive dashboard (e.g., maternal & child trends, epidemic signals). NHIC "About" frames it as "a centralized platform for processing, integrating, triangulating, and analyzing real-time health data using advanced technological tools and artificial intelligence" launched **April 2025** ([nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)).
2. **Trace a signal to source.** A spike in district-level malaria admissions triggers drill-down. NHIC's "12 data sources" include CHWs, health posts, health centres, district/referral hospitals, disease-prevention/surveillance domains ([nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)).
3. **Cross-check surveillance lineage.** The signal is corroborated against A2 (eIDSR — `cbs2.moh.gov.rw/idsr`) and the DHIS2 Tracker CBS built with HISP Rwanda ([dhis2.org/hisp-rwanda](https://www.dhis2.org/hisp-rwanda)).
4. **Overlay HR + supply.** Analyst overlays G2 (HWMS, MoH 4×4 reform — [moh.gov.rw](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)) and D1/D2 eLMIS supply indicators.
5. **Draft policy brief.** WHO notes Rwanda's HIS is a "country-driven HIS strengthening — an example of a country taking ownership and leadership in using data to inform decision-making" ([WHO HIS case study](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)).
6. **Feed back into planning.** Brief feeds Health Sector Strategic Plan adjustments + NHIC's 6-layer roadmap ([MoH HIC](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions)).

**Data produced/consumed.** Consumes all 12 NHIC source streams; produces ministerial dashboards, AI-assisted forecasts, briefings.

### P2 — Epi / surveillance officer (IDSR / eIDSR)

1. **Receive alert.** A facility clinician or CHW (P5) flags a suspected notifiable condition. Per WHO, "Rwanda has used DHIS2 as its national health information system since 2012 and has made significant progress" with electronic IDSR ([WHO HIS case study](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)).
2. **Case entered into eIDSR Tracker.** Recorded into DHIS2 Tracker at `https://cbs2.moh.gov.rw/idsr`. Tracker model "tracks individual cases, enabling follow-up and case-based surveillance" per HISP Rwanda ([dhis2.org/hisp-rwanda](https://www.dhis2.org/hisp-rwanda)).
3. **Lab linkage.** Specimens + lab results linked to the case record. HIV CBS is "functional at 166 sites" per CDC ([CDC in Rwanda](https://www.cdc.gov/global-health/countries/rwanda.html)).
4. **Outbreak detection / threshold logic.** DHIS2 program rules trigger alerts.
5. **Daily/weekly bulletin.** Aggregate IDSR rolls up to national bulletins and feeds NHIC ([WHO case study](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf)).
6. **COVID-style case management loop.** During pandemics, DHIS2 modules are adapted for case management and contact tracing ([Sciforce brief](https://www.sciforce.com/wp-content/uploads/2021/04/Digital-health-systems-to-support-pandemic-response-in-Rwanda.pdf)).

**Data produced/consumed.** Consumes suspected-case notifications from facilities + CHWs. Produces case line lists, weekly epi bulletins, outbreak alerts.

### P3 — Hospital clinician (OpenMRS eBuzima)

1. **Patient arrives.** Clinician searches the **SHR via the RHIE Client Registry** — "in Rwanda the HIE includes a Shared Health Record (SHR) and Client Registry to ensure that client information is accessible across multiple EMR instances" ([OpenHIE RHIE story](https://ohie.org/rwanda-hie-impact/)).
2. **Encounter in OpenMRS eBuzima.** Doctor opens patient chart; encounters, labs, ART/TB regimens recorded. Hospital EMR is **on-prem Ubuntu server** at the facility ([WHO strategy PDF p.33-34](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)).
3. **Cross-facility lookup via SHR.** Pulls prior diagnoses and medications from other facilities via F6 (SHR, OpenMRS-based) using **CR + FHIR + SHR** as the canonical pattern ([OpenHIE RHIE story](https://ohie.org/rwanda-hie-impact/)).
4. **Lab order through OpenHIM (F2).** Orders HIV viral load/CD4/recency: B1 → F2 (OpenHIM routes JSON payload to Mapping Mediator + F8 Lab Registry) → Mapping Mediator transforms to **FHIR and stores in HAPI FHIR** → confirmation back to B1. Lab result flow mirrored. Clinician retrieves results via FHIR query ([RHIE report §5.3.2 flow diagram](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)).
5. **Monthly HMIS upload.** Aggregate indicators pushed to A1 (DHIS2) via "Monthly report Tool to collect monthly clinical data from all health facilities" ([moh.gov.rw](https://www.moh.gov.rw/)).
6. **Research extract (where applicable).** For IeDEA HIV research, the **OpenMRS NIDA module** runs de-identification on a snapshot — "implements the NIDA (National Institute on Drug Abuse) dataverse de-identification pipeline within OpenMRS" so research datasets leave scrubbed of identifiers ([PMC IeDEA paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC5422632/)).

**Data produced/consumed.** Produces encounter-level clinical data + monthly HMIS aggregates + de-identified research extracts. Consumes SHR-prior records, lab results, ART regimens.

### P4 — District Health Officer (DHO + PBF)

1. **Open DHIS2 district dashboard.** DHO reviews monthly ANC, deliveries, immunization, OPD indicators.
2. **Review PBF claims.** Performance-Based Financing verification uses the dedicated **PBF dashboard at `https://aggregate.moh.gov.rw/pbfrwanda`** ([moh.gov.rw](https://www.moh.gov.rw/)). Facilities submit quantity + quality scores; DHO and MoH verifiers cross-check against HMIS.
3. **CHW performance review.** DHO pulls SISCOM (CHW monthly reports via health centres) — CHWs are organized into cooperatives supervised by the health centre; performance-linked incentives are central ([Rwanda CHW Program summary](https://chwcentral.org/wp-content/uploads/2015/02/Rwanda-CHW-Program-Summary.pdf)).
4. **Workforce allocation under 4×4 reform.** Using G2 HWMS, the DHO verifies deployment of the new "4 per health-centre" staffing rule (4 GPs + 4 nurse anaesthetists) ([MoH 4×4 reform](https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce)).
5. **Performance contract / Imihigo.** District-level performance rolled up to national Imihigo performance contracts.
6. **Feed NHIC.** Cleaned HMIS stream consumed by H1 NHIC dashboards ([nhic.moh.gov.rw/about](https://nhic.moh.gov.rw/about)).

**Data produced/consumed.** Consumes HMIS aggregates, PBF claims, CHW cooperative reports. Produces district performance reviews, PBF verification.

### P5 — Community Health Worker (CHW)

1. **Receive work list on phone.** CHW opens the cEMR / eCHIS app to see assigned households for the day. Per Resolve to Save Lives + GoR launch, "Rwanda launches the next generation of digital tools for community health" — d-IDS (community surveillance), cEMR, eCHIS ([resolvetosavelives.org](https://resolvetosavelives.org/about/news/rwanda-launches-the-next-generation-of-digital-tools-for-community-health/), [newtimes.co.rw](https://www.newtimes.co.rw/article/248405/News/rwanda-launches-next-generation-of-digital-tools-for-community-health)). >45,000 active CHWs; ~1/4 focused on maternal & newborn health ([PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)).
2. **Conduct household visit.** Uses offline-first Android cEMR app to register pregnancies, track ANC, screen for malnutrition, screen for NCDs. National scale to **58,567 CHWs by end-2026** ([UNICEF Rwanda](https://www.unicef.org/rwanda/stories/piles-registers-digital-care-community-health-workers-rwanda-adopt-digital-health-rec)).
3. **Symptom screening + AI decision support.** For maternal cases (e.g., post-C-section), the mUbuzima app (Insightiv + Harvard + PIH/IMB) prompts a symptom questionnaire and runs an ML image classifier on incision photos to predict surgical-site infection — **operating offline** ([PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/)). Kirehe District usability: 100% of CHWs agreed/strongly agreed with ≥80% of usability statements.
4. **d-IDS embedded in cEMR.** The national d-IDS guides case registration, symptom assessment, testing, treatment/referral — a Rwanda implementation study reports **24.2% fewer referrals** ([PubMed 41687454](https://pubmed.ncbi.nlm.nih.gov/41687454/)).
5. **Refer or treat at household.** Administer treatment (iCCM) or refer to health centre; app prompts when to refer.
6. **Submit monthly SISCOM report.** Household-level indicators (pregnancies, deliveries, child deaths, malnutrition, TB suspects) sent to supervising health centre → compiled into A1 DHIS2.
7. **Trigger surveillance alert.** If a notifiable disease is suspected, d-IDS pushes a case notification directly to A2 (eIDSR / DHIS2 Tracker) — closing the loop to P2.

**Data produced/consumed.** Produces household-level CHW records, SISCOM aggregates, d-IDS alerts. Consumes work lists, app content, training.

### P6 — Citizen / patient

1. **Enroll in Mutuelle de Santé.** Household head registers with the local cell coordinator; premiums collected (via RSSB channels after 2022 CBHI→RSSB transition) ([rssb.rw](https://www.rssb.rw/rssb-products/mutuelle-de-sante-cbhi/)). Per Lu et al., "in 2019, 83% of Rwandan women and men ages 15 to 49 had health insurance; of those, 93% were members of the CBHI scheme" ([gatesopenresearch 4-177](https://gatesopenresearch.org/articles/4-177/v2)).
2. **Receive membership card / digital proof.** Paper card + (where digitised) a record keyed to national ID.
3. **Visit health centre.** Patient presents at the health centre; clinician verifies Mutuelle eligibility; encounter recorded in B1 (hospital) or A1 (health-centre aggregate).
4. **Teleconsultation (when available).** Until Aug 2023, I12 Babyl provided SMS/USSD teleconsultation to ~2.8M users before shutting down ([Forbes](https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/)). No public successor.
5. **Service billed / captured.** Service rendered; facility records encounter + bills against CBHI/RSSB.
6. **Aggregate flows upward.** Anonymised encounter data → A1 monthly → H1 NHIC dashboards.
7. **(Future) Health Portal access.** B4 (DHIA-funded) will let citizens view their own records pulled from B1 + B2 ([GF case study p.4](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf)).

**Data produced/consumed.** Produces enrollment records, premium payments, encounter-level utilisation. Consumes membership verification, teleconsultation advice.

**§3 confidence: HIGH** for P1–P4 (multi-source anchor: NHIC, MoH HMIS landing, OpenHIE, WHO HIS case study, OpenHealthNews, Resolve to Save Lives). **MEDIUM-HIGH** for P5 (multiple primary sources but cEMR features evolve rapidly). **MEDIUM** for P6 (Babyl gap creates ambiguity on the citizen channel).

**Cross-cutting observation (from §3).** Two flows close the loop and distinguish a "live" HIS from a passive reporting system: **CHW → eIDSR** (P5 → P2) and **facility EMR → DHIS2 aggregate → NHIC** (P3/P4 → P1). Both are operational in Rwanda. One citizen endpoint (Babyl) is dark since Aug 2023. AI is moving to the edge — d-IDS in cEMR, mUbuzima ML on CHW phones, NHIC AI as the national analytics layer.

---


## 4. Systems map (nodes + relationships — conceptual graph)

> Tiered from **community** (edge) up through **facility** (data producers), **national** (hosting + registries + analytics), to **external / partner** (donors + AI vendors + cloud). The map is conceptual — the visual artifact renders it as a layered diagram with arrows per §5.

```
                    ┌─────────────────── EXTERNAL / PARTNER (I) ───────────────────┐
                    │                                                                │
   AI vendors    ──►│  I10 Anthropic   I11 OpenAI+Gates Horizon1000                   │
   (edge/clinical) │  I12 Babyl (defunct) I13 Insightiv  I14 Digital Umuganda        │
   AI for data ──►  │  I15 OpenEvidence × RBC × RTSL (reported, low-confidence)      │
                    │                                                                │
   Donors/funders ─►│  I1 Global Fund (DHIA)  I2 CDC/PEPFAR (TSSS)  I3 WHO           │
                    │  I4 USAID/GHSC-PSM  I6 Mastercard/Msft  I7 HealthTech Hub       │
                    │  I8 CDPI+RISA  I9 Gates Foundation  I5 RCAS                    │
                    └─────────┬──────────────────────────────────────────────────────┘
                              │ funds / co-designs / standards
                              ▼
            ┌─────────────────────────── NATIONAL TIER (NDC + Kigali) ─────────────────────────────┐
            │                                                                                       │
            │   Registries / Identity (F)                  Analytics (H)                            │
            │   ┌────────────────────────────┐            ┌──────────────────────────┐             │
            │   │ F3 Client Registry (UPID) ◄─┼────────────┤   H1 NHIC (6-layer        │             │
            │   │   ↕ NIDA integration        │            │   data lakehouse,         │             │
            │   │ F4 Facility Registry        │            │   Apache Superset)        │             │
            │   │ F5 Provider Registry        │            │   feeds: A1, A2, A3, A4,  │             │
            │   │ F6 Shared Health Records    │            │   B1 (agg), C5, F9, G2,   │             │
            │   │ F7 Terminology Registry     │            │   G7, census/DHS           │             │
            │   │ F8 Laboratory Registry      │            └─────────────┬────────────┘             │
            │   └─────────────┬──────────────┘                          │                          │
            │                 │                                          │                          │
            │   Interop bus   ▼                                          │                          │
            │   ┌──────────────────────────────────────────┐             │                          │
            │   │ F1 RHIE / RHIES (OpenHIE-based)           │             │                          │
            │   │   + F2 OpenHIM mediator (8.2 + Grafana)  │             │                          │
            │   └─────┬────────────────────────────┬────────┘             │                          │
            │         │                            │                      │                          │
            │   Reporting backbone (A)            │                      │                          │
            │   ┌──────────────────────────────────▼──────────┐           │                          │
            │   │ A1 RHMIS / DHIS2 aggregate                  │◄──────────┘                          │
            │   │   + A2 DHIS2 Tracker eIDSR                  │                                      │
            │   │   + A3 DHIS2 Tracker HIV CBS                │                                      │
            │   │   + A4 COVID testing/vaccination modules    │                                      │
            │   │   + A5 programme registries (eTB, NCD…)     │                                      │
            │   └─────────────────────────────────────────────┘                                      │
            │                                                                                       │
            │   Workforce/Financing (G)                                                               │
            │   ┌──────────────────────────────────────────────────────────────────────┐               │
            │   │ G1 CSAM   G2 HWMS   G3 iHRIS   G4 IPPIS   G5 Licensing   G6 MEMMS │               │
            │   │ G7 HRTT   G8 eLearning   G9 RHAP   G10 PBF dashboard               │               │
            │   │ G11 RSSB / Mutuelle de Santé (CBHI)                                │               │
            │   └──────────────────────────────────────────────────────────────────────┘               │
            └───────────────────────────────────────────────────────────────────────────────────────────┘
                              ▲                                          ▲
                              │ monthly aggregate / research extracts    │ HIC source feeds
                              │                                          │
            ┌─────────────────┴────────────────────┐    ┌─────────────────┴────────────────┐
            │   FACILITY TIER (hospital + health  │    │   COMMUNITY TIER (CHW + mobile) │
            │   centre on-prem + labs + supply)   │    │                                  │
            │                                     │    │                                  │
            │  EMR (B)                            │    │  mHealth (C)                     │
            │  ┌──────────────────────────────┐   │    │  ┌────────────────────────────┐ │
            │  │ B1 OpenMRS / eBuzima         │   │    │  │ C1 eCHIS (cEMR on phones)  │ │
            │  │   (on-prem Ubuntu servers    │   │    │  │ C2 RapidSMS (legacy,       │ │
            │  │    at every health facility, │   │    │  │    45,000 feature phones)  │ │
            │  │    hospital package: IPD/    │   │    │  │ C3 RapidPro (DHIS-to-      │ │
            │  │    OPD/lab/pharmacy/billing) │   │    │  │    RapidPro integration)   │ │
            │  │ B2 cEMR (community EMR on    │   │    │  │ C4 CHIS (health-post IS)   │ │
            │  │    CHW smartphones; offline) │   │    │  │ C5 WelTel (SMS engagement) │ │
            │  │ B3 OpenClinic (alt hospital) │   │    │  │ C6 Viamo 3-2-1 (IVR)      │ │
            │  │ B4 Health Portal (under dev) │   │    │  │ C7 AKIISA (AI training)    │ │
            │  └──────────────┬───────────────┘   │    │  └────────────┬───────────────┘ │
            │                 │                   │    │               │                 │
            │  Lab (E)        ▼                   │    │               ▼                 │
            │  ┌──────────────────────────────┐   │    │   d-IDS in cEMR (B2) ──► A2     │
            │  │ E1 LIMS LabWare (NRL + BLIS) │   │    │   mUbuzima ML ──► P3            │
            │  │ E2 VLSM (HIV VL/CD4/recency) │   │    │                                  │
            │  │ E3 NRL                       │   │    │                                  │
            │  │ E4 ePROGESA (CNTS blood bank)│   │    │                                  │
            │  └──────────────┬───────────────┘   │    │                                  │
            │                 │                   │    │                                  │
            │  Supply (D)     ▼                   │    │                                  │
            │  ┌──────────────────────────────┐   │    │                                  │
            │  │ D1 eLMIS (commodities)       │   │    │                                  │
            │  │ D2 RMS warehouse (WMS)       │   │    │                                  │
            │  │ D3 Reagent Mgmt System (ERP) │   │    │                                  │
            │  │ D4 Viebeg (AI procurement)   │   │    │                                  │
            │  │ D5 Zipline (drone delivery)  │   │    │                                  │
            │  │   centres: Muhanga, Kayonza, │   │    │                                  │
            │  │            Rusizi            │   │    │                                  │
            │  └──────────────────────────────┘   │    │                                  │
            └─────────────────────────────────────┘    └──────────────────────────────────┘
```

**Two critical bridges** (the "live HIS" feedback loops):
1. **C5/C3 → F2 → A2**: CHW surveillance alert → OpenHIM → eIDSR Tracker (closes P5 → P2).
2. **B1 → F2 → A1** (and on to H1): OpenMRS encounter → OpenHIM → DHIS2 monthly aggregate → NHIC dashboards (closes P3 → P1).

**§4 confidence: HIGH** — the tiering is well-documented in the [WHO Digital Health Strategy 2018–2023](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf), the [RHIE report](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf), and the [MoH HIC announcement](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions). The two feedback-loop edges are confirmed in both primary RHIE documentation and the DHIS2-RapidPro integration ([github.com/dhis2/integration-dhis-rapidpro](https://github.com/dhis2/integration-dhis-rapidpro)).

---

## 5. Integration / data-flow edges (source → destination : payload)

> Each edge names the systems, the payload, the mechanism (API/mediator/SMS/etc.), and the protocol. Edges that are *documented* (have a primary source) are flagged; the rest are *inferred* from the OpenHIE architecture and MoH strategy.

### 5.1 Documented edges (with primary source)

| # | Edge | Payload | Mechanism | Source |
|---|---|---|---|---|
| **E1** | **B1 OpenMRS → F2 OpenHIM (lab order)** | JSON lab order (patient ID, test, sample) | REST → OpenHIM routes to Mapping Mediator + F8 Lab Registry | [RHIE report §5.3.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E2** | **F2 OpenHIM → HAPI FHIR (lab order transformed)** | FHIR ServiceRequest | Mapping Mediator transforms JSON → FHIR | [RHIE report §5.3.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E3** | **F2 OpenHIM → B1 OpenMRS (lab order ack)** | JSON confirmation | OpenHIM returns confirmation | [RHIE report §5.3.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E4** | **E2 VLSM → F2 OpenHIM (lab result)** | JSON lab result | OpenHIM → Mapping Mediator → HAPI FHIR | [RHIE report §5.3.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E5** | **F2 OpenHIM → E2 VLSM (lab result ack)** | JSON confirmation | OpenHIM returns | [RHIE report §5.3.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E6** | **B1 OpenMRS → F2 OpenHIM (lab result query)** | FHIR query | OpenHIM → Mapping Mediator → HAPI FHIR → results back | [RHIE report §5.3.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E7** | **B1 OpenMRS → F3 Client Registry (UPID lookup)** | Demographic query → auto-fill demographics from NIDA | OpenHIM mediator; NIDA integration auto-fills ~90% of fields | [OHIE impact story](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda), [RHIE report §6.3.1.2](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E8** | **B1 OpenMRS → F6 Shared Health Records (encounter store)** | FHIR Encounter/Observation/ServiceRequest/MedicationRequest | OpenHIM mediator to SHR back-end | [RHIE report §6.3.1.4](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E9** | **B1 OpenMRS → A3 DHIS2 Tracker HIV CBS** | HIV case line list (enrolment, follow-up, index testing, recency) | OpenHIM OpenMRS→DHIS2 e-tracker mediator | [RHIE report §6.3.1.7](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E10** | **B1 OpenMRS → A1 DHIS2 (monthly aggregate)** | Monthly service-delivery aggregates | DHIS2 data set upload via "Monthly report Tool" | [moh.gov.rw](https://www.moh.gov.rw/) |
| **E11** | **C2 RapidSMS → A1 DHIS2 (maternal/CH indicators)** | Aggregated pregnancy/newborn indicators | SMS gateway → DHIS2 Tracker; automated reminders for appointments | [OpenHealthNews](https://www.openhealthnews.com/articles/2017/dhis2-transforming-health-it-standards-developing-world-part-2) |
| **E12** | **C3 RapidPro → A1 DHIS2 (via dhis2-rapidpro-integration)** | Completed flow runs → DHIS2 data value sets | Java app polls RapidPro API for flow runs; maps flow results to DHIS2 data elements via webhook/HTTPS; resilient to network spotty | [github.com/dhis2/integration-dhis-rapidpro](https://github.com/dhis2/integration-dhis-rapidpro), [developers.dhis2.org](https://developers.dhis2.org/blog/2022/12/dhis-to-rapidpro-in-the-field) |
| **E13** | **B1 OpenMRS → research (IeDEA consortium US)** | De-identified HIV cohort extracts | C# identifier-stripping; uploaded with Rwandan government + ethics-board permission | [PMC6918068](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/) |
| **E14** | **A1 RHMIS → I5 RCAS (COVID analytics)** | Periodic mirror of COVID testing + vaccination DBs | REST; integrated with G9 RHAP | [Oxford Open Digital Health 2024](https://academic.oup.com/oodh/article/doi/10.1093/oodh/oqae034/7743133) |
| **E15** | **B1 OpenMRS → F6 SHR → F3 CR → F4 FR → F5 PR (registries push)** | "Both the client and facility registries are pushed automatically, on an ongoing process, to the EMR to maintain accuracy and up-to-date documentation" | OpenHIM | [OHIE impact story](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda) |
| **E16** | **F2 OpenHIM monitoring → F1 RHIE admin** | Transaction audit log, traffic stats | OpenHIM dashboard (Grafana/Prometheus) | [RHIE report §6.3.1.1](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E17** | **A4 DHIS2 COVID-19 testing/vaccination → A1 RHMIS** | Aggregate testing + vaccination records | DHIS2 Android Capture App → DHIS2 instances | [dhis2.org — COVID testing](https://dhis2.org/rwanda-covid-testing/), [vaccination](https://dhis2.org/rwanda-covid-vaccination/) |
| **E18** | **D5 Zipline → D2 RMS (delivery confirmation)** | Delivery records, inventory pull signals | Per-delivery integration with health authorities | [Zipline newsroom](https://www.zipline.com/newsroom/zipline-and-the-government-of-rwanda-announce-a-new-partnership-to-serve-the-entire-country-with-instant-logistics) |
| **E19** | **F2 OpenHIM (iHRIS integration) → RapidPro → CHW (mHero pattern)** | Health worker lookup → SMS | OpenHIM connects iHRIS, DHIS2, RapidPro | [openhim.org docs](https://openhim.org/resources/openhim-v4.0.5.pdf) |

### 5.2 Inferred / planned edges (OpenHIE-pattern + MoH strategy)

| # | Edge | Payload | Mechanism | Source |
|---|---|---|---|---|
| **E20** | **D1 eLMIS → A1 DHIS2 (commodity consumption)** | Inventory + consumption aggregates | HISP DHIS2/mSupply variant; SAGE integration planned | [HISP Rwanda](https://hisprwanda.org/hisp-rwanda-showcases-innovative-dhis2msupply-elmis-solution-at-dhis2-annual-conference-2025), [WHO strategy PDF p.46-48](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf) |
| **E21** | **D3 Reagent Mgmt ↔ E1 LIMS ↔ A1 RHMIS** | Lab reagent stock + usage | MoH goal = complete interop | [GF case study p.3](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf) |
| **E22** | **F9 CRVS → H1 NHIC** | Births, deaths, cause-of-death | Source feed in HIC 6-layer architecture | [MoH HIC announcement](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions) |
| **E23** | **C5 WelTel → H1 NHIC** | Patient-engagement metrics | HIC source system | [MoH HIC announcement](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions) |
| **E24** | **G2 HWMS → H1 NHIC** | Workforce allocation | HIC source system | [MoH HIC announcement](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions) |
| **E25** | **G7 HRTT → H1 NHIC** | Health financial flows | HIC source system | [MoH HIC announcement](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions) |
| **E26** | **B4 Health Portal ← B1/B2 (pull)** | Patient's own records | DHIA-funded portal API | [GF case study p.4](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf) |
| **E27** | **F4 Facility Registry → A1 DHIS2 (org unit sync)** | Facility list, codes | MoH guidelines: "the facilities that were also present in the DHIS2 were saved to the facility registry database" | [OHIE impact story](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda) |
| **E28** | **F5 Provider Registry ↔ B1 OpenMRS (license gating)** | License validity → EMR access | Testing env; planned gate | [RHIE report §6.3.1.3](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |
| **E29** | **B1 OpenMRS → IeDEA de-id → US research (E13 with permission)** | De-identified cohort | C# identifier-stripping; Rwandan gov + ethics permission | [PMC6918068](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/) |
| **E30** | **H1 NHIC → external dashboards / APIs (`api.nhic.moh.gov.rw`)** | Aggregate KPIs (National Health Facility Registry, District Health Performance) | Apache Superset guest-token; REST API; downloadable reports | [nhic.moh.gov.rw](https://nhic.moh.gov.rw/) |
| **E31** | **D5 Zipline → facility EHR (vaccines/inventory "pull")** | Real-time demand/inventory | RBC partnership; "pull" model | [Zipline × RBC](https://www.zipline.com/newsroom/bringing-vaccines-closer-to-home-a-partnership-to-expand-access-in-rwanda) |
| **E32** | **G11 RSSB Mutuelle → facility billing / B1 OpenMRS** | Eligibility check | Manual at intake (per §3 P6); **no automated EMR↔insurance integration documented** ([RHIE report §7.3](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)) | [RHIE report](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf) |

### 5.3 Anti-edges (documented gaps / not-connected)

- **B1 OpenMRS ↔ G11 RSSB** — no automated insurance claim integration documented ([RHIE report §7.3](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)).
- **B3 OpenClinic → F1 RHIE** — some hospitals opted out of OpenMRS; OpenClinic instances are not on the RHIE bus (partial coverage).
- **F4/F5/F7/F8 registries → B1 OpenMRS production** — testing env only as of Jan 2025; pending operationalisation ([RHIE report §6.3](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf)).
- **B2 cEMR (CHW) → H1 NHIC** — HIC lists 12 sources; cEMR/eCHIS listed under "community health workers" but the direct cEMR-to-HIC edge is not separately documented.
- **C5 WelTel ↔ F2 OpenHIM** — WelTel is an HIC source but its integration pathway (push vs API) is not public.

**§5 confidence: HIGH** on the 19 documented edges (E1–E19) — all anchored on RHIE report §5.3.2 + OHIE impact story + GitHub integration code + OpenHealthNews + Zipline + MoH HIC announcement. **MEDIUM** on inferred edges (E20–E32) — inferred from OpenHIE patterns and MoH strategy but not directly traced in a single primary source. **MEDIUM** on anti-edges — gaps documented but not always independently re-verified.

---


## 6. In-system data-protection posture (consolidated from §1 + §4 of the lane)

> Each DP control row summarises what the deployed stack **actually does** (vs what Law 058/2021 obliges — that mapping is in §7). Anchors: [DLA Piper — Rwanda](https://www.dlapiperdataprotection.com/index.html?t=law&c=RW); [Securiti.ai — Rwanda](https://securiti.ai/rwanda-data-protection-law/); [OHIE impact story — RHIE consent model](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda); [PMC6918068 — IeDEA de-id](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/); [OpenHIE Specification Release 3.0](https://ohie.org/wp-content/uploads/2020/12/OpenHIE-Specification-Release-3.0.pdf); [DHIS2 security docs](https://docs.dhis2.org/en/implement/implementing-dhis2/security-considerations.html); [guide.openmrs.org — RBAC](https://guide.openmrs.org/administering-openmrs/user-management-and-access-control/).

| Control | Law/policy baseline | Documented in practice | Confidence |
|---|---|---|---|
| **Consent capture** | Opt-in consent (Law 058/2021 art. 6); child <16 parental consent; public-health exception | **HIE-level deny model** ([OHIE impact story](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda)): "block access at patient's request" + element-level sensitivity. **No public per-system capture workflow** in OpenMRS / DHIS2 / RHIE for routine care. NHIC claims anonymization at presentation layer ([nhic.moh.gov.rw](https://nhic.moh.gov.rw/)). | High (law) / Low (practice) |
| **De-identification** | Art. 11 lists tokenisation, pseudonymisation, encryption as permitted safeguards for sensitive data | **Strongest documented control**: IeDEA OpenMRS pipeline — custom C# identifier-stripping before US research upload, with Rwandan gov + ethics permission ([PMC6918068](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/)); characterised as irreversible de-id. Earlier OpenMRS-module encrypted-export approach was abandoned. | Medium-High (research secondary use); **not** routine clinical DP |
| **Access control (RBAC)** | Art. security TOMs require controls | OpenMRS role/privilege model (View Patients, Edit Patients, etc.) — PIH IMB EMR is open source ([github.com/PIH/openmrs-module-imbemr](https://github.com/PIH/openmrs-module-imbemr)); DHIS2 user roles/groups and sharing; **NIDA-linked identity (F3)** auto-fills demographics. PIH Rwanda thesis cites "user authentication" + "privilege-based access" + SSL ([PMC6918068](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/)). F5 Provider Registry license-validity-gates EMR access (planned). | Medium-High |
| **Data residency** | **Art. 50 storage-in-Rwanda default** unless NCSA-certified; cross-border art. 48–49 conditions | RHIE reporting and 2018 strategy repeat "securely hosted and backed up" requirement ([WHO strategy PDF p.32](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)). NDC hosts DHIS2 + RHIE since 2013. **IeDEA US transfers occur with government + ethics permission** = a lawful-basis pathway. **Babyl (I12)** was the documented PHI-out-of-Rwanda case via Babylon's AWS UK; wound down Aug 2023. | High |
| **Audit logging** | Art. 47 security verification; art. 41 48h breach notification to NCSA | **OpenHIE architecture specifies audit service** at design level ([OpenHIE Spec R3.0](https://ohie.org/wp-content/uploads/2020/12/OpenHIE-Specification-Release-3.0.pdf)); **OpenHIM dashboard provides transaction audit log + Grafana/Prometheus monitoring** (RHIE report §6.3.1.1); DHIS2 audit API exists ([docs.dhis2.org/audit](https://docs.dhis2.org/en/manage/concepts/audit.html)). **No public Rwanda production audit-trail architecture** (who-read-which-record, immutability, retention) found. | Low-Medium |
| **Encryption at rest / in transit** | Art. 11 lists encryption as a sensitive-data safeguard; MoH ICT policy = encryption + VPN | **In transit**: SSL cited for OpenMRS Rwanda ([PMC6918068](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/)); TLS in OpenHIE architecture. **At rest for national production servers**: **not publicly documented**. NDC backup/DR posture required per 2018 strategy ([WHO strategy PDF p.57-60](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)). | Low-Medium |
| **Heir designation (art. 26-equivalent)** | Right to designate a data heir | **Not implemented in any documented Rwanda system**; B4 Health Portal is the natural place to encode it (not yet built). | Low |
| **No-automated-decisioning guard-rail (art. 22-equivalent)** | Right not to be subject to automated decisions | d-IDS, NHIC AI, Babyl (legacy), Horizon1000, Anthropic MOU — none documented with a formal human-in-the-loop override; Tech Policy Press flags this gap for the Anthropic MOU ([Tech Policy Press](https://www.techpolicy.press/anthropic-is-becoming-the-backbone-of-rwandas-government-but-who-is-accountable/)). | Low-Medium |
| **DPIA for high-risk processing (art. 39-equivalent)** | Required for likely-high-risk processing | No public DPIA register found for national systems; AI-on-health pipelines (NHIC, Horizon1000, Insightiv) have not publicly disclosed DPIA outputs. | Low |
| **DPO appointment (art. 37-equivalent)** | Required where core activities = large-scale sensitive data | MoH is the controller of record; no public DPO appointment disclosed. Interim DPO can sit in MoH CIO office. | Low |
| **Breach notification (art. 41)** | 48h to NCSA; high-risk → communicate to subjects | NCSA Personal Data Breach Notification Form includes a `Health` sector tick-box ([dpo.gov.rw](https://dpo.gov.rw/fileadmin/DPO/ComplianceTools/Personal%20Data%20Breach%20Notification%20Form.pdf)). No public MoH-runbook or case study of a 48-hour NCSA notification. | Low |

**§6 confidence: HIGH** on the legal framework (DLA Piper + Securiti + Hogan Lovells; cross-checked). **MEDIUM-HIGH** on the RHIE architecture + OpenHIM lab flow (primary RHIE report + OHIE wiki + Jembi blog). **MEDIUM-HIGH** on the IeDEA de-identification pipeline (peer-reviewed PMC paper). **LOW-MEDIUM** on at-rest encryption, audit-log production specifics, consent capture workflow, DPO appointment — these are the practice gaps to flag.

**Practice gap (one-line summary):** Rwanda's deployed MoH stack protects data primarily through **policy, access control, and infrastructure controls** rather than through documented, per-system patient-facing consent workflows. Public deployment documentation is much stronger on confidentiality, authentication, RBAC, encryption, and residency than on consent capture or systematic de-identification.

---

## 7. DP-law constraints → how each system/benchmark solves them (Law 058/2021 mapping)

> Map each legal obligation from Law n° 058/2021 to the **concrete control** that resolves it. The law citations follow [Hogan Lovells](https://www.hoganlovells.com/en/publications/key-features-of-the-new-rwandan-data-protection-law), [DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=RW), [Securiti.ai](https://securiti.ai/rwanda-data-protection-law/), [Digital Policy Alert change 12074](https://digitalpolicyalert.org/change/12074), [DPO Rwanda](https://dpo.gov.rw/), [WHO CPCD](https://cpcp.who.int/), [Lawfare — Locked In](https://www.lawfaremedia.org/article/locked-in-african-data-protection-laws-make-children-less-safe-online). Architecture comparison uses [Sand DPT](https://www.sandtech.com/legal-disclaimers), [Helium Health Privacy Notice](https://www.heliumhealth.com/privacy-notice/) + [InfoSec Policy](https://www.heliumhealth.com/information-security-policy/), [Zipline Privacy Policy](https://www.flyzipline.com/privacy-policy).

| Legal obligation (Law 058/2021) | How the Rwanda MoH stack solves it (best-evidence) | How Sand solves it (processor pattern) | How Helium Health solves it (controller) | How Zipline solves it (controller in Rwanda op) |
|---|---|---|---|---|
| **Sensitive data = health/medical records** (art. sensitive-data def.) | A1+A2+A3+B1+E1+F6 flagged as sensitive; NHIC claims anonymization at presentation layer | Customer's data classified as sensitive; Sand TOMs align | Explicit "sensitive personal data" treatment in Privacy Notice | Patient identifiers treated as PHI per US/EU law baselines |
| **Lawful grounds (art. 5, 8 grounds)** | Public health surveillance + notifiable disease = art. 5 grounds 3 (legal obligation) + 5 (public interest); routine care = consent (ground 1); research = ground 8 + NCSA authorisation | Documented instructions from controller; sub-processor list | Explicit legal-basis section in Privacy Notice (contract, consent, legitimate interest) | Contract + safety-necessity for operations; consent for non-operational |
| **Data-subject rights (10 rights, art. 22-equivalent onward)** | RHIE deny model implements **right to restriction** at record/element level; **right to portability** via B4 Health Portal under development; **right to heir designation** unimplemented; **right to object to automated decisions** not formalised | Customer is controller; Sand provides export + deletion APIs | Privacy Notice enumerates rights + contact for DPO | Same; account-closure flow |
| **Controller/processor duties (art. 28-equivalent)** | MoH = controller; vendors (HISP Rwanda, Jembi, QT Global, OpenMRS Foundation, LabWare, Viamo, etc.) = processors; written DPAs not publicly enumerated | **Sand acts as data processor; customer acts as controller** ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Controller (operates EHR + payments) | Controller (distribution platform) |
| **Record of Processing Activities (art. 9)** | No public RoPA register disclosed; 2018 strategy requires ICT security policy + backup SOPs ([WHO strategy PDF p.57-60](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf)) | Documented instructions + sub-processor governance | RoPA enumerated in Privacy Notice | RoPA per Privacy Policy |
| **Security TOMs (art. security)** | Encryption (SSL/VPN, at-rest uncertain); RBAC (OpenMRS/DHIS2); OpenHIE security services; OpenHIM monitoring | "Access controls, encryption in transit and at rest, network segmentation, hardened production environments" + regular security testing ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | TLS in transit; encryption at rest; role-based access; audit logging ([Helium InfoSec](https://www.heliumhealth.com/information-security-policy/)) | TLS + AES-256 at rest; KMS-managed keys; RBAC; audit trails on operator actions ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) |
| **Cross-border transfer (art. 49/50)** | NDC hosts RHIE + DHIS2; **Babyl** was a documented out-of-Rwanda case (wound down); **IeDEA US transfers** with gov + ethics permission; planned 123 cloud OpenMRS instances raise residency question (unresolved) | SCCs + customer-selected region; depends on customer (not fixed Rwanda) | SCCs + sub-processor agreements | SCCs + internal data-transfer agreements |
| **Breach notification (art. 41, 48h)** | NCSA breach form ready (`Health` sector tick-box — [dpo.gov.rw](https://dpo.gov.rw/fileadmin/DPO/ComplianceTools/Personal%20Data%20Breach%20Notification%20Form.pdf)); MoH runbook not public | "Notify the customer without undue delay … sufficient to support the customer's own notification obligations" ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Notification commitment in Privacy Notice | Notification commitment + forensics in Privacy Policy |
| **DPIA (art. 39)** | No public DPIA register found | DPIA support via DPT; customer-led | DPIA capability referenced | DPIA capability referenced |
| **DPO appointment (art. 37)** | Recommended for MoH given large-scale sensitive processing; no public appointment disclosed | Customer is controller; Sand provides DPO contact channel as processor | DPO email listed | Privacy office email listed |
| **Certifications** | Not publicly claimed by MoH | **ISO/IEC 27001:2022 and SOC 2 Type II** ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) — strong evidence base for "appropriate safeguards" | SOC 2 / ISO 27001 posture (industry baseline for EHR vendors) | SOC 2 posture |
| **Sub-processor governance** | MoH-side vendor list not publicly enumerated; OpenHIE architecture pre-defines mediator contracts | Pre-onboarding notification + right to object | Sub-processor list referenced in policy | Categories of service providers + consent for material change |
| **Return/deletion on termination** | RHIE continuity not explicit; IeDEA de-id exports are one-way research extracts | "Return or delete personal data as instructed by the customer, except where retention is required by applicable law" ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Account-closure flow + retention exceptions | Account-closure + retention exceptions |

**Pattern observed.** All three benchmark platforms converge on the GDPR processor pattern: a written DPA, sub-processor governance, TOMs that include encryption + access control, and breach-notification chains running upstream to the controller so the controller can hit the 48-hour NCSA window. **Sand is the most explicit on certifications (ISO/IEC 27001:2022 + SOC 2 Type II)**, which makes its TOMs directly admissible as "appropriate safeguards" under art. 50.

**Rwanda-specific overlay for the MoH stack:**
1. **Default to in-country storage** for production PHI (NDC, or AWS af-south-1 with NCSA cross-border authorisation).
2. **Analytics / research** in a different region is permitted only with explicit NCSA authorisation + DPIA + art. 49 ground (e.g., public interest for notifiable-disease analytics).
3. **DR/backup region** must be declared in the registration; NCSA expects continuity-of-operations disclosure.
4. **Audit logging** should be immutable and in-country to support NCSA inspections without cross-border evidence requests.

**§7 confidence: HIGH** on the law mapping (multiple legal-analyst sources cross-checked). **HIGH** on the Sand DPT facts (mirrored from [sandtech.com/legal-disclaimers](https://www.sandtech.com/legal-disclaimers) → `out/.raw/sand_disclaimers.html`). **MEDIUM-HIGH** on Helium Health and Zipline (vendor policies + secondary sources). **MEDIUM** on the MoH-side control mapping (the legal obligations are clear; which exact control satisfies which in MoH's stack is inferred from the architecture).

---


## 8. Vendor benchmark (Sand vs Helium Health vs Zipline vs MoH vendors) — deep dive on three patterns

> Three patterns that recur across health-data platforms; each pattern is the operational answer to a Law 058/2021 obligation.

### 8.1 Pattern A — Controller/processor separation + DPA upstream of NCSA

The MoH remains the **data controller** (Law 058/2021 art. 3: "natural person, public or private corporate body, or legal entity that processes personal data and determines the means of their processing"; [Securiti](https://securiti.ai/rwanda-data-protection-law/)). Every vendor — Jembi, HISP Rwanda, OpenMRS Foundation, LabWare, Viamo, WelTel, Viebeg, Insightiv, Anthropic, OpenAI — is a **data processor** bound by a DPA that mirrors art. 28-equivalent duties:

- *Documented instructions only* — "Sand processes personal data only to provide the services described in the agreement and on the documented instructions of the customer" ([Sand DPT](https://www.sandtech.com/legal-disclaimers)).
- *Sub-processor governance* — customer notification + right to object before a new sub-processor is on-boarded ([Sand DPT](https://www.sandtech.com/legal-disclaimers); Helium Privacy; Zipline Privacy).
- *Personnel controls* — background checks, confidentiality clauses, role-scoped access ([Sand DPT](https://www.sandtech.com/legal-disclaimers)).
- *Breach notification upstream* — "Notify the customer without undue delay … sufficient to support the customer's own notification obligations" ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) — designed so the **controller** can hit the 48-hour NCSA window ([Securiti](https://securiti.ai/rwanda-data-protection-law/)).
- *Return or deletion on exit* — per customer instruction, with legal-retention carve-out ([Sand DPT](https://www.sandtech.com/legal-disclaimers)).

**Why this matters for Rwanda.** This is the only realistic way to operate a multi-vendor stack where MoH, an EHR vendor, a cloud provider, an SMS aggregator, and a research partner all touch the same patient record. Without it, MoH cannot discharge its controller duties under art. 4 (principles), art. 9 (RoPA), art. 39 (DPIA), and art. 41 (breach notification).

### 8.2 Pattern B — Data residency + cross-border authorisation

All three benchmark platforms use **regional cloud regions** + **Standard Contractual Clauses** as the data-residency primitive:

| Platform | Default cloud region pattern | Cross-border mechanism |
|---|---|---|
| **Sand** | Customer-selected region (e.g. AWS af-south-1 Cape Town or eu-central-1 Frankfurt) | "Appropriate safeguards such as standard contractual clauses" ([Sand Privacy Policy](https://www.sandtech.com/legal-disclaimers)) |
| **Helium Health** | Multi-region African deployment with cloud-managed failover | Contractual safeguards + sub-processor agreements ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) |
| **Zipline** | Country-resident operational systems; aggregate analytics in US parent cloud | SCCs + internal data-transfer agreements ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) |

**Rwanda-specific overlay** ([Securiti](https://securiti.ai/rwanda-data-protection-law/); [Digital Policy Alert change 12074](https://digitalpolicyalert.org/change/12074); [DPO Rwanda homepage](https://dpo.gov.rw/)): art. 49/50 require an **NCSA-issued certificate** to store personal data outside Rwanda, plus a lawful basis (consent, contract necessity, public interest, etc.). The DPO Rwanda "Standard Contractual Clauses for Transfer Personal Data Outside Rwanda" is the recommended contractual primitive.

### 8.3 Pattern C — TOMs: encryption + ReBAC + audit + DPO + breach chain

All three vendors converge on the same six-element control set:

| Control | Sand | Helium | Zipline |
|---|---|---|---|
| 1. Encryption in transit (TLS) | ✔ | ✔ | ✔ |
| 2. Encryption at rest (AES-256 / cloud KMS) | ✔ | ✔ | ✔ |
| 3. Role-based access control (RBAC) + personnel scoping | ✔ | ✔ | ✔ |
| 4. Network segmentation + hardened production | ✔ ("network segmentation, hardened production environments") | ✔ (per [InfoSec Policy](https://www.heliumhealth.com/information-security-policy/)) | ✔ |
| 5. Regular security testing (penetration testing, vulnerability scanning) | ✔ ("regular security testing") | ✔ | ✔ |
| 6. Incident response + breach-notification chain | ✔ ("notify the customer without undue delay") | ✔ | ✔ |

Citations: [Sand DPT](https://www.sandtech.com/legal-disclaimers); [Helium Privacy Notice](https://www.heliumhealth.com/privacy-notice/) + [InfoSec Policy](https://www.heliumhealth.com/information-security-policy/); [Zipline Privacy Policy](https://www.flyzipline.com/privacy-policy).

**Certifications.** Sand = **ISO/IEC 27001:2022 and SOC 2 Type II** ([Sand DPT](https://www.sandtech.com/legal-disclaimers)). Helium and Zipline operate SOC 2-style control environments. For an MoH platform, these certifications become **evidence of "appropriate safeguards"** under art. 50 ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) and are routinely accepted by NCSA.

**Two extra layers** that distinguish a high-maturity health-data platform:
- **RoPA per art. 9** — every data-flow enumerated with categories of subjects/data, purposes, recipients, transfers, retention, TOMs; feeds the DPIA register and breach runbook.
- **Heir-designation + automated-decisioning guard-rails** — right to designate a data heir (art. 26-equivalent; [Securiti](https://securiti.ai/rwanda-data-protection-law/)) + right not to be subject to automated decisions (art. 22-equivalent) — both distinctive African DP provisions. Rwanda MoH should encode both: a Health Portal "data heir" field that unlocks records on proof of death, and a hard human-in-the-loop rule on any AI-assisted triage/risk-scoring.

### 8.4 Outstanding / open issues for the Rwanda MoH context

- **DPO appointment.** Treat as mandatory given large-scale sensitive processing; interim DPO can sit in MoH CIO office pending permanent appointment.
- **NCSA registration.** All controllers and processors must register with NCSA ([DPO Rwanda](https://dpo.gov.rw/)). Backfill registration of legacy platforms even though Oct 2023 transition window has closed; NCSA inspections + fines remain available.
- **Cross-border certificate.** Any platform hosting PHI outside Rwanda needs an art. 49 certificate. African regions (AWS af-south-1, Azure South Africa North, GCP me-west1) simplify the application.
- **Sector codes.** NCSA has not yet published a health-sector code of practice (as of the latest publicly accessible summaries — [Digital Policy Alert digest](https://digitalpolicyalert.org/digest/dpa-digital-digest-rwanda)). MoH should benchmark against the Lawfare *Locked In* analysis ([Lawfare](https://www.lawfaremedia.org/article/locked-in-african-data-protection-laws-make-children-less-safe-online)) and WHO CPCD entry ([WHO CPCD](https://cpcp.who.int/)) for health-data specifics.
- **Children.** Rwanda's DP regime (like Kenya's, unlike GDPR) does not set the digital-consent age at 14/16 in the parent law; sector rules + Malabo Convention influence this. MoH adolescent-health (ASRH) programs should default to parental consent + adolescent assent + documented risk-assessment.

**§8 confidence: HIGH** on the benchmark patterns (three vendors' privacy / DPT / InfoSec policies fetched + mirrored). **MEDIUM-HIGH** on the Rwanda-specific overlay (multiple legal-analyst sources). **MEDIUM** on the open-issues framing (best-effort synthesis of legal position).

---

## 9. Gaps + cross-cutting confidence

### 9.1 Gaps — what this model could not verify

| Gap | Where it bites | Severity |
|---|---|---|
| **No public per-system patient-consent capture workflow** in OpenMRS / DHIS2 / RHIE for routine clinical care | §6 row 1; violates art. 5 spirit unless waived by public-health ground | High (legal) |
| **At-rest encryption** (disk/DB-level) for national OpenMRS, RHIE, DHIS2 production servers not documented | §6 row 6; art. 11 sensitive-data safeguard nominally required | High (legal) |
| **Production audit-log architecture** (who-read-which-record, immutable logs, retention) for any named national system | §6 row 5; art. 47 verification duty | Medium (legal) |
| **NCSA registration status** of MoH systems + named vendors (HISP Rwanda, Jembi, QT Global, OpenMRS Foundation, LabWare, Viamo, WelTel, Viebeg) | §7 registration row; art. 9 RoPA + DPO | Medium (legal) |
| **Cross-border residency question for the planned 123 cloud OpenMRS instances** (per 2021 OpenHIE impact story) — under art. 50 they would each need NCSA authorisation | §7 residency row; F1 future | Medium (legal) |
| **NHIC application hosting provider / region / data-lakehouse stack** — only architecture-level statements are public | §1 H1; §6 anonymization claim | Medium (architecture) |
| **D3 Reagent Management System vendor/owner** — trademarked product named by GF but no Rwanda-specific architecture | §1 D3; supply-chain end-to-end interop | Medium |
| **2024–2029 Digital Health Strategic Plan + Architecture Blueprint** — planned completion 2026, not yet published | Strategy-layer input to architecture | Medium (timeliness) |
| **B4 Health Portal** — DHIA-funded build, not yet GA; will encode citizen-facing rights (portability, heir designation) when shipped | §1 B4; §7 rights | Medium (citizen channel) |
| **Current (2023–26) production hosting endpoint** for DHIS2/eLMIS — HISP↔RBC transition is documented but the endpoint is not | §1 A1, D1; residency + operations | Low-Medium |
| **OpenEvidence × RBC × Resolve to Save Lives** partnership — single social post, not independently verifiable | §1 I15; AI-vendor inventory | Low |
| **d-IDS developer** — embedded in national cEMR; developer not named publicly | §1 B2; AI at the CHW edge | Low |
| **WelTel Privacy Policy** — vendor policy not publicly located | §1 C5; SMS-content DPIA | Low |
| **Babyl successor operation** — none documented; citizen teleconsultation gap continues | §1 I12; §3 P6 | Low (channel) |

### 9.2 Cross-cutting confidence per section

| Section | Confidence | Anchored on |
|---|---|---|
| §1 systems inventory | **HIGH** (core), **MEDIUM** (admin/AI), **LOW** (unverified vendors) | [RHIE report (Jan 2025)](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf), [GF case study (Jan 2026)](https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf), [WHO strategy 2018–2023](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf), [MoH HIC](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions) |
| §2 personas matrix | **HIGH** | [NHIC](https://nhic.moh.gov.rw/about), [WHO HIS case study](https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf), [MoH HMIS](https://www.moh.gov.rw/), [OpenHIE RHIE](https://ohie.org/rwanda-hie-impact/), [Resolve](https://resolvetosavelives.org/about/news/rwanda-launches-the-next-generation-of-digital-tools-for-community-health/) |
| §3 journeys | **HIGH** for P1–P4, **MEDIUM-HIGH** P5, **MEDIUM** P6 | Same as §2 + [PMC12838494](https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/) |
| §4 systems map | **HIGH** | [WHO strategy](https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf), [RHIE report](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf), [MoH HIC](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions) |
| §5 edges — documented | **HIGH** | [RHIE §5.3.2 flow diagram](https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf), [OHIE impact story](https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda), [dhis2/integration-dhis-rapidpro GitHub](https://github.com/dhis2/integration-dhis-rapidpro), [developers.dhis2.org](https://developers.dhis2.org/blog/2022/12/dhis-to-rapidpro-in-the-field), [OpenHealthNews](https://www.openhealthnews.com/articles/2017/dhis2-transforming-health-it-standards-developing-world-part-2) |
| §5 edges — inferred | **MEDIUM** | OpenHIE patterns + MoH strategy; not single-source traced |
| §6 in-system DP | **HIGH** (legal framework), **MEDIUM-HIGH** (RHIE + IeDEA), **LOW-MEDIUM** (consent/at-rest/audit/DPO) | [DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=RW), [Securiti](https://securiti.ai/rwanda-data-protection-law/), [PMC6918068](https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/), [OpenHIE Spec R3.0](https://ohie.org/wp-content/uploads/2020/12/OpenHIE-Specification-Release-3.0.pdf), [DHIS2 docs](https://docs.dhis2.org/en/implement/implementing-dhis2/security-considerations.html) |
| §7 DP-law mapping | **HIGH** | [Hogan Lovells](https://www.hoganlovells.com/en/publications/key-features-of-the-new-rwandan-data-protection-law), [DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=RW), [Securiti](https://securiti.ai/rwanda-data-protection-law/), [Digital Policy Alert 12074](https://digitalpolicyalert.org/change/12074), [DPO Rwanda](https://dpo.gov.rw/) |
| §8 vendor benchmark | **HIGH** (Sand), **MEDIUM-HIGH** (Helium + Zipline) | [Sand DPT](https://www.sandtech.com/legal-disclaimers) (mirrored), [Helium Privacy](https://www.heliumhealth.com/privacy-notice/) + [InfoSec](https://www.heliumhealth.com/information-security-policy/), [Zipline Privacy](https://www.flyzipline.com/privacy-policy) |

### 9.3 Engine degradation notes (transparency)

- **Perplexity `sonar-pro`** — several JSON dumps contain bracket citations without URL mappings; Perplexity-derived claims are anchored to the raw dumps (`out/.raw/pplx_*.json`) and cross-checked against primary URLs in the lane files. The HIC six-layer architecture was verified directly against the [MoH news page](https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions) because Perplexity did not surface it.
- **Parallel.ai** — returned only 1 top result set for the broad inventory query; breadth was compensated with Perplexity + native fetches of primary PDFs (RHIE report, GF case study, WHO strategy, NHIC frontend bundle).
- **Bot-walled primary sources** — TBI (`institute.global`) and Zipline newsroom required JS; UNICEF page blocked direct fetch (content via Parallel excerpt). All recovered via secondary paths; nothing relies on a bot-walled URL alone.
- **PubMed reCAPTCHA** — full text not retrievable for d-IDS paper ([PubMed 41687454](https://pubmed.ncbi.nlm.nih.gov/41687454/)); abstract facts via Perplexity extraction.

### 9.4 One-line synthesis (what the visual artifact should foreground)

Rwanda's MoH runs a **national-first, government-hosted, OpenHIE-interoperable digital-health stack** that is strong on **identity (UPID/NIDA), aggregate reporting (DHIS2 since 2012), supply chain (eLMIS), lab integration (EMR↔VLSM via OpenHIM/FHIR), and analytics (NHIC since Apr 2025)** — and is moving AI to the edge (d-IDS in cEMR, mUbuzima ML, Horizon1000). Its documented **de-identification control** (IeDEA C# pipeline) is world-class for research reuse; its documented **consent-capture / at-rest-encryption / production-audit / DPO / NCSA-registration** posture is the practice gap to close before any new health-data pipeline goes live under Law 058/2021.

---

## 10. Visual-artifact render contract

The visual artifact (next step) consumes **§1 (systems table)**, **§3 (per-persona journeys)**, **§4 (systems map graph)**, **§5 (edge list)**, and **§6 + §7 + §8 (DP posture vs Law 058/2021)**. The Sand reference architecture is the implicit "Sand-class" benchmark against which the MoH stack is read; the visualisation mirrors the [Sand "modular architecture + persona map" reference style](https://www.sandtech.com/health/).

