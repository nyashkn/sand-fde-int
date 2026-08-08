# Sand Technologies Healthcare Products — Research Deep-Dive

Research conducted via 6 parallel scout agents against public sources (sandtech.com, AWS
Marketplace, job postings, Rwanda MoH press, LinkedIn). None of the 5 product names in the
assignment (`Health Atlas`, `Health Outcome Tracker`, `Health Insight Engine`,
`Analytics Template Toolkit`, `HealthOS Data Models`) are literal public product names — they
map to real, evidenced capabilities inside Sand's actual platform stack:

```
Symmetri (cross-industry platform: Sense → Analyze → Act, AWS-native)
  └── HealthOS / RHOS (healthcare vertical, live in Rwanda; expanding — 15 countries / 80+ FDEs by end-2026)
        ├── Health Atlas          → 3D facility mapping + catchment analysis
        ├── Health Outcome Tracker → "Health Outcome Visibility" pillar (ANC/maternal/child/malaria/NCD)
        ├── Health Insight Engine  → AI anomaly/alert layer (mirrors Rwanda's live National Health Intelligence Center)
        ├── Analytics Template Toolkit → Apache Superset dashboards
        └── HealthOS Data Models  → DHIS2 3-dim model + openHIE registry pattern
```

Confidence is **high** on the underlying HealthOS/Symmetri architecture (Sand's own AWS
Marketplace listings, job postings, Rwanda MoH press all corroborate independently). Confidence
is **low** on exact schemas, algorithms, or literal product-name branding — Sand does not publish
a technical spec sheet; treat anything below marked [INFERENCE] as informed extrapolation, not a
sourced fact.

---

## 1. Health Atlas — Geographic mapping & facility intelligence

**What it maps to:** No page literally titled "Health Atlas." Strongest public evidence is a
LinkedIn feature on Sand Senior Software Engineer Linda Prinsloo (Healthcare team, since RHOS's
Rwanda launch) describing **3D national-scale facility mapping and catchment-area resolution** —
she physically carried a projector to Rwanda to show MoH stakeholders a 3D facility map, later
digitized into the platform. Explicit stated goal: find undigitized/unregistered facilities that
"couldn't accurately serve the population and catchment area."

**Likely ingests:** facility registries/GPS coordinates, EMR data, supply-chain/LMIS stock data,
population/census data, GIS layers. [INFERENCE, from Sand's own "GIS asset & network model" data
category used across its water/energy/telecom verticals too.]

**Likely used for:** facility mapping/visualization, catchment-population estimation per
facility, service-coverage/gap analysis, feeding a geographic model into triage/resource-
allocation decision support.

**Sources:**
- https://healthcare.sandtech.com/ — RHOS (Rural Health Operating System) Rwanda microsite, 1M+ patients served
- https://www.sandtech.com/health/ — "Global Health Systems" case study: "connected thousands of rural clinics... improved triage, resource allocation, and operational planning"
- https://www.sandtech.com/operational-diagnostic/ — names "GIS asset & network model" and "Geospatial coverage & traffic data" as canonical data-source categories
- https://startup.jobs/forward-deployed-engineer-zambia-sand-tech-holdings-limited-c-8129253 — Zambia FDE posting; references DHIS2, OpenMRS, SCADA, GIS as integrated domain platforms; confirms 15-country/80+FDE-by-end-2026 target
- https://www.linkedin.com/posts/sandtechinc_meet-sands-senior-software-engineer-linda-activity-7487462062030389248-ehqy — primary source for the 3D mapping/catchment work

---

## 2. Health Outcome Tracker — Patient outcome analytics

**What it maps to:** "Health Outcome Visibility" — one of five named Ministry priority pillars
inside HealthOS (the other four: Digital Transformation, Supplies & Commodities, Health
Financing, Pandemic Preparedness). Explicitly covers maternal/child health, malaria, and NCD
monitoring.

**Documented outcomes** (from Sand's own marketing, treat as vendor-claimed not independently
audited):
- Targeted ultrasound deployment guided by HOS insight → **19% increase** in women completing 4+ antenatal care visits (ANC4)
- Rwanda: proactive coverage management cut a seasonal **60% → 17%** drop in clinic visits over three years
- **73% more citizens** maintaining continuous health insurance coverage
- Rwanda deployment also publicly branded "Rwanda Health Intelligence Center" / RHOS

**Likely architecture:** cohort- and indicator-based tracking (ANC visit completion, malaria case
trends, NCD screening) rolled up facility → district/region → national, feeding
dashboards/bulletins/analytics reports [per a Sand employee LinkedIn profile describing exactly
this deliverable type].

**Sources:**
- https://aws.amazon.com/marketplace/pp/prodview-erbppddpsw4ck — **Sand HealthOS AWS Marketplace listing** (primary technical source: Sense→Analyze→Act framing, AWS-native, "deployable in a new country in under eight weeks")
- https://www.sandtech.com/health/
- Sand FDE job posting, Sierra Leone (French fluency required) — describes end-to-end deployment, ministry data-sharing agreements, local capacity-building [URL not captured by scout; re-fetchable on request]

---

## 3. Health Insight Engine — AI-powered analytics and alerts

**What it maps to:** the AI-driven analytics/alerting layer of HealthOS. The closest public
description of the actual architecture underneath an "insight engine" is Rwanda's live
**National Health Intelligence Center (NHIC/HIC)**, launched April 2025, with a published
**six-layer architecture**:

```
Source Layer (DHIS2, EMRs [eBuzima, cEMR], eLMIS logistics, CRVS, WelTel population tracking, EMS, workforce systems, census)
  → Data Ingestion & Transformation
    → Data Replication / Landing Zone (raw staging)
      → Data Lakehouse (validate, enrich, aggregate)
        → Data Storage Layer (secure structured repository)
          → Presentation Layer (dashboards, reports, external API access)
```

The AI/alerting function sits at the lakehouse→presentation boundary: anomaly detection against
expected baselines (case counts, commodity consumption, clinic visit volume) driving early-warning
outbreak alerts, stockout flags, resource-allocation triggers. [INFERENCE — no published detail on
specific ML algorithms, training data, or alert thresholds.]

**Live confirmed use:** actively used for 2026 Ebola/EVD outbreak monitoring and surveillance in
Rwanda.

**Sources:**
- https://aws.amazon.com/marketplace/pp/prodview-erbppddpsw4ck — Sand HealthOS listing
- https://www.sandtech.com/health/
- https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions — **Rwanda MoH, publishes the 6-layer HIC architecture** (best primary technical source found)
- https://www.gatesnotes.com/home/home-page-topic/reader/expanding-access-to-health-care-through-ai — third-party corroboration
- https://www.moh.gov.rw/news-detail/evd-updates-16-june-2026-update-on-ebola-outbreak — live outbreak-monitoring use, dated 2026

---

## 4. Analytics Template Toolkit — Pre-built reporting templates (Apache Superset)

**What it maps to:** No literal product page, but strong direct evidence HealthOS uses
**Apache Superset** as its BI/dashboarding layer — Sand's own Greenhouse job posting for
"Forward Deployed Engineer, Nigeria" explicitly lists *"Experience with BI and dashboarding
tools, particularly Apache Superset"* as a preferred requirement, alongside DHIS2/OpenMRS
integration. A Sand data engineer's LinkedIn profile independently corroborates Superset +
Amazon QuickSight use on national health system work.

**Best working interpretation:** "Analytics Template Toolkit" = pre-built/reusable Superset
dashboard templates FDEs deploy against MoH data sources as part of Sand's reusable "playbooks" —
consistent with the FDE JD's explicit description of using "Sand's product components and
playbooks" to rapidly deploy MVPs, and HOS's "deployable in under 8 weeks" claim.

**Apache Superset capabilities relevant to this assignment** (from superset.apache.org docs):
- No-code drag-and-drop dashboard/chart builder, 22+ chart types incl. geospatial, time-series, pivot tables, big-number KPIs
- SQL Lab: ad-hoc + templated SQL (Jinja templating) against 40+ database backends
- Dataset-level RBAC/row-column security
- Embedded dashboard support (iframe/SDK)
- **Built-in scheduled report/alert emailing** — directly relevant to automating a quarterly bulletin: `SQL Lab query/virtual dataset → saved chart set on a templated dashboard → scheduled report feature` auto-generates and emails/publishes the bulletin without manual rebuild each cycle.

**Sources:**
- http://job-boards.eu.greenhouse.io/sandtechholdingslimited/jobs/4836497101 — FDE Nigeria posting, names Apache Superset explicitly as a preferred skill
- https://aws.amazon.com/marketplace/pp/prodview-erbppddpsw4ck — Sand HealthOS listing
- https://superset.apache.org/docs/ — Apache Superset official docs (capabilities list above)
- LinkedIn profile of a Sand data engineer corroborating Superset + QuickSight use [URL not captured by scout]

---

## 5. HealthOS Data Models — Standard healthcare data transformations

**What it maps to:** the underlying data-integration/transformation layer inside HealthOS. No
public docs describe schema-level specifics (table names, transformation logic) — treat any
schema specifics as illustrative, not sourced.

**Likely architecture** [INFERENCE, standard for this problem space, not confirmed Sand-specific]:

- **DHIS2's native aggregate data model** (since DHIS2 is the named integration point): 3 core
  dimensions — org unit (facility/hierarchy), data element (indicator), period
  (day/week/month/quarter/year) — pulled via DHIS2 Web API, reshaped into a warehouse-friendly
  long/tidy fact table `(org_unit_id, data_element_id, period, value)`.
- For patient/EMR-level (not aggregate) data, DHIS2 increasingly bridges to **FHIR** — DHIS2
  Tracker entities map to FHIR resources (Patient, Encounter, Observation) per WHO SMART
  Guidelines profiles.
- **openHIE** is the dominant reference architecture for exactly this MoH-integration problem: a
  Health Information Mediator/Interoperability Layer (OpenHIM) routes between point-of-service
  systems and shared registries — Client Registry (patient identity), Facility Registry (org
  units, aligns with DHIS2 org unit hierarchy), Health Worker Registry, Shared Health Record,
  terminology service. HealthOS's "connects existing data systems, facilities and workflows into
  a single coherent view" language matches this pattern closely.
- **ETL/transformation layer**: no public evidence of Sand's specific tooling, but Sense→Analyze→
  Act plus AWS-native delivery imply a conventional bronze/silver/gold medallion pattern: raw
  DHIS2/EMR/supply-chain pulls → normalized/conformed dimensional model (org unit hierarchy dim,
  indicator dim, time period dim, fact tables) → curated marts feeding dashboards. The FDE Nigeria
  posting lists **dbt/Airflow** as preferred skills, consistent with this pattern.

**Sources:**
- https://aws.amazon.com/marketplace/pp/prodview-erbppddpsw4ck — Sand HealthOS listing (integration surface: DHIS2, EMRs, supply chain/logistics, population/geospatial data)
- https://dhis2.org/integration and https://docs.dhis2.org — DHIS2 data model docs
- https://dhis2.org/integration/fhir — DHIS2↔FHIR mapping
- https://ohie.org/framework/ — openHIE reference architecture
- https://guides.ohie.org/arch-spec/architecture-specification/overview-of-the-architecture — openHIE architecture spec
- https://openhim.org/docs — OpenHIM (interoperability layer/mediator) docs
- http://job-boards.eu.greenhouse.io/sandtechholdingslimited/jobs/4836497101 — FDE Nigeria posting, lists dbt/Airflow/FHIR as preferred skills

---

## 6. Sand HOS / Symmetri — Platform overview

**Symmetri** (cross-industry platform Sand markets as "the control layer for critical
infrastructure"): unified platform (not per-vertical rewrites) organized around a continuous
**Sense → Analyze → Act** loop:

1. **Sense** — ingests real-time and historical data from sensors/SCADA/enterprise
   systems/EMRs/DHIS2/satellite links into a live "system model"
2. **Analyze** — consequence modelling, physics-aware simulation, and AI prediction on top of
   that model, producing auditable, role-aware recommendations suited to regulated/government
   environments
3. **Act** — routes recommendations into a control layer and operational apps, ranging from
   automated low-risk execution to AI-generated decision briefs for complex cases, with autonomy
   staged to the client's risk tolerance

Deployed 18+ countries (cross-industry, per AWS Marketplace claim). Underlying AWS infra
(platform-wide, not health-specific): **EKS w/ Hybrid Nodes + Karpenter, Aurora Serverless v2
(Postgres), ElastiCache (Valkey), OpenSearch, S3/ECR, Cognito, Secrets Manager, Route53/SES,
VPN/VPC** — standard AWS-native microservices + data-lake architecture.

**HOS** is this same Sense/Analyze/Act loop applied to Ministry-of-Health data, with FDEs embedded
in-country to integrate client data sources, build POCs/MVPs on Sand's existing product
components, and harden them into production systems the Ministry depends on daily.

**FDE role model** (from the Nigeria posting, richest source): two tracks (roaming vs.
permanently embedded 12–24 months), triple role (SWE + PM + Consultant), product-led delivery
motion (POC → MVP → hardened production), field-feedback loop claimed to drive **30% of the
product roadmap**, explicit local-capacity-building mandate. Rwanda is the flagship live
deployment (1M+ patients, hundreds of clinics digitized, partnered with Society for Family Health
and Rwanda MoH). Nigeria is the newest active deployment (FDE embedding just started, no public
results yet). The 15-country/80+FDE-by-end-2026 target is quoted verbatim from Sand's own job
postings.

**No public technical whitepaper exists** — everything above is inferred from Sand's own
marketing/AWS listing language and job-posting technical-skill lists, not verified engineering
documentation.

**Sources:**
- https://healthcare.sandtech.com/ — RHOS (Rural Health Operating System) Rwanda microsite
- https://www.sandtech.com/health/ — canonical "Global Health Systems" case study
- https://aws.amazon.com/marketplace/pp/prodview-ae2fh6326bbpi — **Symmetri AWS Marketplace listing** (Sense/Analyze/Act framework description, AWS stack detail, "18+ countries deployed" claim)
- https://aws.amazon.com/marketplace/pp/prodview-erbppddpsw4ck — **Sand HealthOS AWS Marketplace listing**
- http://job-boards.eu.greenhouse.io/sandtechholdingslimited/jobs/4836497101 — **FDE Nigeria posting** (richest primary source: confirms 15-country/80-FDE target verbatim, full FDE role definition, technical skills list: DHIS2, FHIR, Superset, dbt, Airflow)
- https://jobs.norrsken.org/companies/sand-technologies-2/jobs/59277397-technical-lead — corroborates Rwanda as first live HOS deployment ("hundreds of clinics already digitized")

---

## Gaps / not independently verified

- Exact literal product names (`Health Atlas`, `Health Outcome Tracker`, etc.) are not confirmed
  public Sand branding — they read as internal or assignment-generic labels over real capabilities.
- No public technical spec, database schema, or ML model documentation for any HOS component.
- Two source URLs were referenced by scouts but not captured verbatim: the Sierra Leone FDE job
  posting (Health Outcome Tracker) and a Sand data engineer's LinkedIn profile (Analytics
  Template Toolkit / Superset + QuickSight corroboration). Re-fetchable on request.
- All quantitative outcome claims (19% ANC4 increase, 60%→17% visit-drop reduction, 73% insurance
  coverage increase) are Sand's own vendor marketing — not independently audited.

---

## 7. Video Evidence — Direct Product Footage (visual/audio analysis, not marketing copy)

Three Vimeo videos embedded on `healthcare.sandtech.com` (RHOS microsite) were downloaded and
run through `meta/muse-spark-1.2` (native video-input model, via OpenRouter) with a prompt asking
for grounded, specific, non-marketing observations of what's actually shown/said. This is the
single richest source in this research pack — it shows the real product UI, real workflow, and
direct narration quotes, not vendor copy.

**Source videos:** `https://player.vimeo.com/video/882854711` (Rwanda Digital Healthcare, 5:11),
`.../882854905` (Bwiza Health Post & Blue Room, 3:19), `.../882903629` (RHOS Blue Room, 3:07).

**Model/method note:** `meta/muse-spark-1.2` accepts video natively but has a hard 50MB per-file
input cap and appears to hit provider-side gateway timeouts (`524`/`400`) on longer clips
regardless of resolution. 2 of 3 videos analyzed successfully; the third ("Rwanda Digital
Healthcare," the longest at 5:11) failed at 1080p/720p/540p/360p across repeated retries — flagged
as a gap, not attempted further given diminishing returns.

### 7.1 Critical correction: the product is NOT branded "HOS"/"Symmetri" on screen

Across both successfully analyzed videos, **the actual on-screen platform name is `Bluelake
Admin`**, at the URL `bluelake.rhos.africa` (also seen as `bluelake.roa.africa` in one frame —
likely a subdomain typo/variant in the same deployment). Neither "HOS," "RHOS" as an acronym on
its own, nor "Symmetri" appears as on-screen text or in spoken narration in either video. The
spoken term used is **"the rural health operating system, developed by Sand Technologies"** —
narration, not a UI label. `Rural Health Operating System` does appear as one tile among several
partner/module logos on a wall display, alongside `Kumva Insights`, `THE PULSE`, `Kapsule`,
`zipline`, `eFiche`, `Starlink` — consistent with the "integration layer over third-party
services" architecture inferred in section 5/6 above, now directly confirmed.

**Read for the FDE interview:** if asked to describe the actual product, ground the answer in
`Bluelake Admin` (the UI you can point to) rather than "HOS"/"Symmetri" (marketing/internal
naming not visible in the product itself).

### 7.2 RHOS Blue Room — the NOC/control-room dashboard, in detail

Staged demo in a small command-center-style office (2-4 workstations, wall projector, dark
cinematic lighting — clearly produced marketing footage, not candid ops footage). No clinical or
field footage; entire video is one office room.

**Confirmed UI structure of `Bluelake Admin`:**
- Top nav: `Dashboard | Operations | Finance | Situation Map`
- Sub-nav: `Operational | Financial | Clinical`
- Filter bar: `Facility: All | Last N Days: 90 | From: [date] | Gender: All | Age Group: All`
- Geospatial **Situation Map** (Mapbox-based) — facility locations as colored status dots over a
  regional map (Rwanda / Lake Kivu region)

**Confirmed chart/metric inventory, by module:**
- *Operational:* `Footfall Per Health Post` (multi-line time series, per-facility), `Visits Per
  Gender` (donut, ~28K total in the demo data), `Daily Footfall Per Gender`, **`Average of Fridge
  Temperature`** and **`Average of Fridge Humidity`** (line charts, ~4-5°C baseline — confirms
  **IoT cold-chain/vaccine monitoring** is a real, working capability, not just claimed)
- *Financial:* `Daily Revenue Per Health Post` (RWF), `Total Revenue` donut (~RF 14M in demo
  data), `Daily Revenue Per Age Group`, `Daily Revenue Per Gender`, `Revenue per Insurance`
- *Clinical:* `Disease Occurrence Over Time` (stacked bar), `Disease Burden Per Health Post`
  (stacked horizontal bar + bubble map), `Disease Prevalence Per Age Group/Gender`, `Diagnosis
  Dates` small-multiples grid with real diagnosis categories legible: *Acute Respiratory (other),
  Intestinal parasite, Physical trauma (other than fracture), Skin diseases, Diseases of urinary
  tract system, Gynecological conditions*

All data is facility/cohort-aggregate — no PHI, no individual patient records visible in this
video. Numbers shown are plausibly demo/synthetic data (unverifiable from visuals alone). No
predictive AI/ML, automated alerting, or "Health Insight Engine"-style anomaly detection UI is
visible — what's shown is descriptive BI/analytics, not the AI-driven layer claimed in marketing.

**Direct relevance to the assignment's Problem A (Quarterly Health Bulletin):** this dashboard
*already computes* nearly every metric the Bulletin needs — footfall/facility volume, maternal-
adjacent categories would sit under the Clinical module's diagnosis breakdowns, and reporting-
completeness-style filters already exist. A prototype build should visually and structurally echo
this `Bluelake Admin` module pattern (Operational/Financial/Clinical tabs, per-facility filter bar,
time-series + donut + stacked-bar chart mix) rather than inventing a new UI language.

### 7.3 Bwiza Health Post & Blue Room — end-to-end clinic workflow, with direct quotes

This video shows both a real facility (Bwiza Health Post, Rwanda, partnered with **Society for
Family Health Rwanda**) and the control-room dashboard, connected by narration explaining the
actual workflow.

**Facility infrastructure (directly observed, not claimed):**
- 10kW solar inverter + rooftop solar panels, rainwater harvesting tanks, **Starlink** dish +
  router — confirms the assignment's "unreliable power (4-6 hrs/day rural)" and "spotty 3G/4G"
  constraints are real problems Sand has already built infrastructure workarounds for
- Neonatal/birthing room with infant warmer, general ward, consultation rooms (laptop + paper
  register — **hybrid digital/paper workflow still exists in practice**), lab with microscope,
  pharmacy shelving

**Confirmed software stack (directly visible, not inferred):**
- A clinician's laptop browser tab is labeled **`OpenMRS`** — the EMR is built on/integrated with
  OpenMRS, not a from-scratch Sand product. This directly confirms the HealthOS Data Models
  research (§5)'s inference that DHIS2/OpenMRS integration is real, not just a job-posting
  requirement.
- A developer's monitor shows VS Code with visible code (`getApplicationTarget...`, `const
  notification = ...`) — confirms custom integration engineering work is happening, consistent
  with "integration layer over third-party services" architecture.
- Same `Bluelake Admin` dashboard/Situation Map as in the RHOS Blue Room video, confirming one
  consistent product across both videos.

**Direct narration quotes (verbatim, useful for grounding interview answers):**
- Scale: *"This health post is one of hundreds managed by Society for Family Health... serving
  hundreds of thousands of patients across Rwanda."*
- Attribution: *"The clinics are powered by the rural health operating system, which was
  developed by Sand Technologies."*
- Staffing model: *"This model is driven by the nurse entrepreneur who runs the clinic... in
  addition to a key new role that we've introduced: the Digital Health Officer or DHO. This DHO
  provides all the I.T. support, data analysis and technical integration for the clinic."*
- Integration claim: *"Sand's system integrates the various software and technology in use in
  healthcare systems today. APIs, third party services that include vital sign collection devices
  to on demand drug deliveries via Zipline drone deliveries. Nurses can also call in a doctor on
  demand to get a second opinion..."*
- One-file claim: *"The patient is able to have one file tracked from registration to lab results
  to pharmaceutical scripts seamlessly."*
- Closing philosophy: *"The technology to provide high quality health care is already here. Let's
  not reinvent the wheel by integrating all these pieces into a unified operating system."*

**Read for the FDE interview:** the "DHO" (Digital Health Officer) role is a concrete, named
staffing pattern Sand has already deployed — worth referencing directly if discussing your own
role's local capacity-building mandate, since it's the clinic-level analog to what an FDE does at
the Ministry level.

### 7.4 Gap: Rwanda Digital Healthcare video (5:11) — not analyzed

Repeated `524`/gateway-timeout failures from `meta/muse-spark-1.2` via OpenRouter across four
resolution attempts (1080p 108MB — exceeds 50MB cap; 720p 54.7MB — exceeds cap by ~2MB; 540p
31MB — succeeded upload but gateway timed out after 5-10 min processing; 360p 16MB — same gateway
timeout, faster this time, then a truncated/malformed JSON response). This looks like a
provider-side processing-time limit tied to video duration (5:11, longest of the three) rather
than file size — not something further resolution reduction will fix. Options if this content is
needed: (a) split into 2-3 minute segments and analyze separately, (b) try `qwen/qwen3.8-max` as
an alternate video-capable model, (c) fall back to `mlx-whisper` for audio-only transcription
(loses visual UI evidence but is free/local/reliable). Not pursued further given the two
successful videos already establish the product, UI, and architecture pattern consistently.
