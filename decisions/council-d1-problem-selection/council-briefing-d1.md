# Council Briefing — Forward Deployed Engineer, Problem Selection

You are deliberating a real decision for a real deliverable. Read this in full before responding.

---

## 1. The situation

A Forward Deployed Engineer (FDE) from Sand Technologies is being deployed to **Rwanda** as
part of a 2-person FDE team, supported by a Solutions Manager and a Country Director. The
Ministry of Health (MoH) has signed an MoU with Sand to *"improve health data systems and
decision-making capabilities."*

**Week 1, Monday.** The MoH Director says: *"Our data is a mess. We cannot make good
decisions. We need you to fix it."*

After Week 1 discovery, three candidate problems are identified. The FDE must choose **one**
to solve in a **6-week sprint**.

---

## 2. The three candidate problems (as stated in the brief)

**Problem A — Quarterly Health Bulletin automation.**
The MoH spends **40 hours/month** manually compiling a "Quarterly Health Bulletin" from DHIS2
Excel exports. They want it automated. The bulletin contains: top 10 facilities by patient
volume; maternal health indicators (ANC visits, deliveries, complications); facility
performance scores (reporting completeness, timeliness); trend analysis vs. previous quarters.

**Problem B — Real-time facility status.**
District health officers cannot see which facilities are operational, which have stockouts, or
where disease outbreaks are happening. They make decisions on 3-week-old data.

**Problem C — TB/HIV unified patient view.**
The TB program and HIV program use separate systems (CommCare). Co-infected patients fall
through the cracks because no one has a unified view.

---

## 3. The data and infrastructure terrain

- **DHIS2** — monthly aggregate reporting, **2–3 week delay**
- **45 hospitals** — "HealthTrack" EMR (buggy, local servers)
- **30 clinics** — OpenMRS
- **175 rural facilities** — **paper only**
- **Separate systems** — TB program, HIV program (CommCare), immunisation (Excel)
- **Infrastructure** — unreliable power (**4–6 hrs/day rural**), spotty 3G/4G

Total facility count is therefore ~250, of which **175 (70%) have no digital data capture at
all.**

**Provided dataset** (5 CSVs, real, already inspected): 117 facilities, monthly records,
strongly maternal/neonatal-focused — facility metadata (tier, NICU/equipment capacity),
clinical neonatal outcomes (1,404 monthly records: deliveries, live births, deaths by cause),
governance (protocol compliance, HMIS reporting completeness, audits), healthcare workers
(staffing ratios, training), operations (referrals, oxygen and drug stockouts).

---

## 4. What Sand's platform actually is (independently researched, evidence-graded)

Sand publishes no technical documentation. The following was reconstructed from public
sources and frame-by-frame analysis of two Sand product videos.

**Confirmed (directly observed):**
- The real product UI is called **`Bluelake Admin`**, at `bluelake.rhos.africa`. Neither
  "HealthOS", "RHOS" nor "Symmetri" appears anywhere in the product UI — those are
  marketing/internal names.
- Nav structure: top-level `Dashboard | Operations | Finance | Situation Map`, sub-level
  `Operational | Financial | Clinical`, with a persistent filter bar
  (Facility / Last N Days / From date / Gender / Age Group).
- Confirmed charts include: Footfall Per Health Post, Visits Per Gender, **Average Fridge
  Temperature and Humidity** (i.e. real IoT cold-chain monitoring), Daily Revenue Per Health
  Post, Disease Occurrence Over Time, Disease Burden Per Health Post.
- The clinician-facing EMR is **OpenMRS** (visible on a laptop in the video).
- Rwanda's National Health Intelligence Center publishes a **six-layer architecture**:
  Source → Ingestion/Transformation → Landing Zone → Lakehouse → Storage → Presentation.
- A clinic-level staff role called the **DHO (Digital Health Officer)** already exists,
  providing IT support, data analysis and technical integration per clinic.
- Third-party integrations named in narration: Zipline drone delivery, vital-sign devices,
  on-demand remote doctor consults, Starlink connectivity, solar power.

**Strong (named in Sand's own job postings):** Apache Superset as the BI/dashboard layer;
dbt and Airflow as preferred data-engineering skills; DHIS2 and OpenMRS integration.

**Inferred (no public spec):** medallion (bronze/silver/gold) warehouse pattern; OpenHIM /
FHIR mediator layer; conformed dimensional model of org-unit × indicator × period.

**Unevidenced (claimed but not observed):** the "Health Insight Engine" — AI-powered
anomaly detection and alerting. Marketing claims it; Rwanda's NHIC is genuinely used for
Ebola outbreak surveillance; but **zero alerting or predictive UI appears in any analysed
video frame.** Everything actually shown is descriptive BI.

**Architectural consequence:** Problem A's entire delivery path — DHIS2 pull → conformed
mart → Superset template → scheduled report — touches only capability that already exists.
Nothing on that path is a greenfield build.

---

## 5. Political terrain

The Solutions Manager **pre-identified the use cases before discovery happened**. His stated
opportunities were (i) maternal and neonatal mortality situational awareness and (ii)
deploying the "Health Atlas" for a single view of the health system. Both are
**Problem-B-flavoured** (situational awareness), not Problem-A-flavoured.

So Sand's internal hypothesis, formed pre-discovery, points at B — while the discovered
40-hour pain points at A. The FDE sits on that fault line, between an employer with a
pre-committed narrative and a client with a differently-shaped problem.

The MoU is signed. The working relationship is not yet established. This is the first
engagement in a country Sand is expanding into (public target: 15 countries, 80+ FDEs by
end-2026), so the engagement is also a template and a reference case.

---

## 6. Constraints that bound any answer

- **6 weeks**, 2 FDEs (not full-time solely on this), plus a Solutions Manager and Country
  Director who are not engineers.
- The FDE's job is explicitly to **prove value fast, build trust, deliver tangible ROI** —
  and then **hand over** to the MoH IT team and exit.
- Deliverable success is judged partly on whether the Ministry still runs the thing after
  the FDE leaves.
- The candidate must also, separately, produce a working prototype for Problem A regardless
  of which problem is selected — but that constraint is an artifact of the recruitment
  exercise and **should NOT influence your reasoning about which problem is genuinely
  correct to pick.** Reason about the real engagement.

---

## 7. The question before the council

**Two parts. Address both.**

**(1) Opportunity mapping.** Problems A, B and C are stated as *solutions*, not needs. Working
from the situation above, what are the **actual underlying opportunities** — the needs, pains
and structural failures that an intervention could address? Name them in the language of the
people experiencing them, not in the language of things to build. Then position A, B and C
(and any solution the brief did not list) against those opportunities.

**(2) Selection.** Which single problem should the FDE commit to for the 6-week sprint, and
what is the strongest argument against your own choice?

Be concrete. Vague strategic language is worthless here — this becomes a document a Ministry
and a hiring panel will both read.
