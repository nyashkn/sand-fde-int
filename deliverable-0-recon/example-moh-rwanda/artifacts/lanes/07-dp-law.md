# Lane L7 — Data Protection & Privacy Law (Rwanda)

> **Scope.** Statute (Law No. 058/2021), implementing guidance from the National Cyber Security Authority (NCSA) and its Data Protection & Privacy Office (DPO), health-data obligations, cross-border transfer rules, and DPO duties. Then a benchmark of how a Sand Technologies–class platform and two African health-data counterparts (Helium Health, Zipline) architect for such laws, with deep-dives on data residency, consent, ReBAC/access control, audit, DPO, and breach handling.
> **Sources cited inline.** Primary texts (gazetted law, NCSA form), secondary analysis (Hogan Lovells, DLA Piper, Securiti, WHO CPCD, Lawfare), and vendor artefacts (sandtech.com Data Processing Terms, heliumhealth.com Privacy & InfoSec, flyzipline.com Privacy Policy).

---

## 1. Statute: Law No. 058/2021 of 13/10/2021

### 1.1 Identity, commencement, transition

| Item | Value | Source |
|---|---|---|
| Citation | Law No. 058/2021 *relating to the protection of personal data and privacy* (also "Data Privacy Law", "DP Law") | <https://www.hoganlovells.com/en/publications/key-features-of-the-new-rwandan-data-protection-law>; <https://regulations.ai/regulations/RAI-RW-NA-N0RPPXX-2021> |
| Enacted | 13 October 2021 | <https://www.hoganlovells.com/en/publications/key-features-of-the-new-rwandan-data-protection-law> |
| Gazette | *Official Gazette* Special Issue of 15/10/2021 | <https://www.minijust.gov.rw/fileadmin/user_upload/Minijust/Publications/Official_Gazette/2021_Official_Gazettes/October/OG_Special_of_15.10.2021_Amakuru_bwite.pdf> |
| In force | 15 October 2021 | <https://www.dlapiperdataprotection.com/index.html?t=law&c=RW> |
| Constitutional basis | Article 23, Constitution of the Republic of Rwanda (right to privacy) | <https://securiti.ai/rwanda-data-protection-law/> |
| Two-year grace for existing operators | Until October 2023 to bring processing into conformity | <https://www.dlapiperdataprotection.com/index.html?t=about&c=RW>; <https://securiti.ai/rwanda-data-protection-law/> |
| Supervisory authority | National Cyber Security Authority (NCSA), exercising its powers through its Data Protection & Privacy Office (DPO Rwanda) | <https://dpo.gov.rw/>; <https://www.hoganlovells.com/en/publications/key-features-of-the-new-rwandan-data-protection-law> |

### 1.2 Territorial and material scope (Article 2)

The law applies to data controllers, processors, and third parties that are **established or ordinarily residing in Rwanda**, as well as those **not established in Rwanda but processing the personal data of data subjects located in Rwanda** — i.e. it is explicitly extra-territorial in the GDPR sense. ([Securiti](https://securiti.ai/rwanda-data-protection-law/); [DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=law&c=RW))

A *data controller* is "a natural person, public or private corporate body, or legal entity that processes personal data and determines the means of their processing" ([Securiti](https://securiti.ai/rwanda-data-protection-law/)).

### 1.3 Sensitive (special-category) personal data

Health status and medical records are explicitly listed in the statute's sensitive data definition:

> *"information revealing a person's race, health status, criminal records, medical records, social origin, religious or philosophical beliefs ..."* — [DLA Piper Data Protection Laws of the World — Rwanda](https://www.dlapiperdataprotection.com/index.html?t=law&c=RW)

Practical effect: any Rwanda MoH platform that handles patient identifiers, diagnoses, lab results, mother/child health records, HIV status, TB status, mental health notes, or biometric identifiers falls under the sensitive-data regime, which **requires either explicit consent or a recognised statutory exception** (see §1.5).

### 1.4 Data-protection principles (Article 4 cluster)

The five principles ([Securiti summary of Article 4-equivalents](https://securiti.ai/rwanda-data-protection-law/)):

1. Lawfulness, fairness, transparency.
2. Purpose limitation (explicit, specified, legitimate purposes).
3. Accuracy and up-to-datedness.
4. Storage limitation (kept no longer than necessary for the purpose).
5. Processed in compliance with data-subject rights.

These map to GDPR Art. 5(1)(a–e). They are enforceable through NCSA inspections and administrative penalties.

### 1.5 Lawful grounds for processing

Eight grounds are recognised, in line with GDPR Art. 6 ([Securiti](https://securiti.ai/rwanda-data-protection-law/)):

1. Data subject's **consent**.
2. Performance of a **contract**.
3. Compliance with a **legal obligation**.
4. **Vital interests** of the data subject.
5. **Public interest**.
6. Performance of **public duties** by a public entity.
7. **Legitimate interests** of the controller.
8. **Research purposes**, upon authorisation by the relevant institution.

Where consent is the basis, it is only valid if *"based on the data subject's free decision after being informed of the consequences"* (Art. 6). This is the exact same GDPR "informed, freely-given, specific" threshold and is the principal anchor for any consent management feature in a digital-health platform.

**Health-data implication.** Public health surveillance, notifiable-disease reporting, and vital-events registration are publicly-mandated processing (grounds 3 and 5). Routine clinical care generally relies on consent (ground 1) or contract (ground 2). Research on residual samples is the ground-8 pathway and triggers NCSA authorisation.

### 1.6 Data-subject rights (Article-equivalent list)

Ten rights ([Securiti](https://securiti.ai/rwanda-data-protection-law/)):

1. Right to **information**.
2. Right of **access**.
3. Right to **object**.
4. Right to **data portability**.
5. Right not to be subject to **automated decision-making** (including profiling).
6. Right to **restriction of processing**.
7. Right to **erasure**.
8. Right to **rectification**.
9. Right to **designate an heir** to personal data (post-mortem privacy — distinctive in African DP laws).
10. Right to **representation** (i.e. mandate an agent to exercise rights).

All ten must be supported by the controller's processes, with the platform's *processor* (e.g. Sand acting as data processor for MoH) providing "assistance" — see §5.1.

### 1.7 Responsibilities of controllers and processors

Per the Securiti synopsis and DLA Piper country guide, controllers and processors must ([Securiti](https://securiti.ai/rwanda-data-protection-law/); [DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=about&c=RW)):

- Implement **technical and organisational security measures** appropriate to the risk.
- Maintain a **record of processing operations** (RoPA-equivalent register).
- Carry out **Data Protection Impact Assessments** where processing is "likely to result in a high risk to data subjects".
- Appoint a **Data Protection Officer** in cases specified by the law or by NCSA regulation.
- Notify the supervisory authority of breaches (see §1.9).
- Engage only processors that provide sufficient guarantees (controller's duty).
- Process on documented instructions only (processor's duty).

### 1.8 Cross-border transfer rules (Articles 49 & 50)

The law embeds **both a data-localisation default and a permissive transfer regime**:

> *"Personal data storage outside Rwanda is permitted only if the data controller or the data processor holds a valid registration certificate authorizing him or her to store personal data outside Rwanda. The supervisory authority issues such a certificate."* — [Securiti summary of Article 49](https://securiti.ai/rwanda-data-protection-law/)

Permitted grounds for cross-border transfer ([Securiti](https://securiti.ai/rwanda-data-protection-law/); Digital Policy Alert [change 12074](https://digitalpolicyalert.org/change/12074)):

1. **Authorisation** by NCSA, with proof of appropriate safeguards.
2. **Consent** of the data subject.
3. **Contractual necessity** (performance of a contract with the subject or pre-contractual steps).
4. **Public interest** grounds.
5. **Exercise or defence of legal claims**.
6. **Vital interests** of the subject or another person.
7. **Legitimate interests** of the controller (balancing test).
8. **Performance of an international instrument** ratified by Rwanda.

**Health-platform consequence.** A cloud-hosted MoH platform that stores EHR data outside Rwanda (e.g. AWS eu-central-1 or af-south-1) needs (a) NCSA cross-border authorisation, (b) a written contract with the cloud provider acting as sub-processor, and (c) demonstrable appropriate safeguards (encryption, audit, breach notification). The default pattern recommended by NCSA is the Standard Contractual Clauses issued by DPO Rwanda (see §2.2).

### 1.9 Breach notification (Article-equivalent)

> *"Rwanda's Data Privacy Law requires data controllers to notify personal data breaches to the regulatory authority within 48 hours after becoming aware of the breach. Data processors are also required to notify data controllers."* — [Securiti](https://securiti.ai/rwanda-data-protection-law/)

If the breach is "likely to result in a high risk to the rights and freedoms of data subjects," the controller must additionally **communicate the breach to affected data subjects** without undue delay. The NCSA's [Personal Data Breach Notification Form](https://dpo.gov.rw/fileadmin/DPO/ComplianceTools/Personal%20Data%20Breach%20Notification%20Form.pdf) (linked from [DPO Rwanda](https://dpo.gov.rw/)) captures this in five sections covering controller identity (with a `Health` sector tick-box — see §3), processor identity, breach description, data-subjects affected, and mitigation steps.

### 1.10 Penalties and enforcement

Failure to comply may result in **administrative fines** on controllers, processors, and third parties ([Securiti](https://securiti.ai/rwanda-data-protection-law/); [Digital Policy Alert digest](https://digitalpolicyalert.org/digest/dpa-digital-digest-rwanda)). Detailed penalty schedules live in the implementing regulations rather than the parent law; secondary analyses reference that NCSA can also issue orders to suspend non-compliant processing.

---

## 2. NCSA / DPO Rwanda implementing instruments

### 2.1 Registration of controllers and processors

NCSA's public-facing compliance toolkit (front door at <https://dpo.gov.rw/> and <https://cyber.gov.rw/>) bundles the following:

- **"What to do after you register with NCSA"** — onboarding checklist for newly-registered controllers ([DPO Rwanda](https://dpo.gov.rw/news-and-updates/news/article/what-to-do-after-you-register-with-ncsa)).
- **Application form for data controllers/processors** (PDF referenced by the cyber.gov.rw portal; the same form is referenced in the April 2022 controller/processor registration guide). *Primary PDF unreachable from this sandbox (10 s curl timeout); secondary references: [DPO Rwanda landing page](https://dpo.gov.rw/), [Digital Policy Alert digest](https://digitalpolicyalert.org/digest/dpa-digital-digest-rwanda), [WHO CPCD entry](https://cpcp.who.int/).*
- **"Report a Data Breach"** — entry point to the [breach notification form](https://dpo.gov.rw/fileadmin/DPO/ComplianceTools/Personal%20Data%20Breach%20Notification%20Form.pdf).

### 2.2 Standard Contractual Clauses (SCCs) for transfer outside Rwanda

DPO Rwanda publishes SCCs for personal-data transfers out of Rwanda, prominently linked from the [DPO Rwanda homepage](https://dpo.gov.rw/) under "Standard Contractual Clauses for Transfer Personal Data Outside Rwanda". Functionally equivalent to GDPR EU SCCs (Modules 1–4), they are the practical mechanism by which a Rwanda MoH platform hosted on AWS eu-central-1, Azure South Africa North, or GCP europe-west can satisfy Article 50.

### 2.3 Awareness and stakeholder outreach

DPO Rwanda and the Kenya Office of the Data Protection Commissioner (ODPC) have signed an MoU to share enforcement practice; this is reflected in [DPO Rwanda news updates](https://dpo.gov.rw/) and consistent with the East-African regional benchmarking discussed by [Sentinel Africa Consulting](https://sentinelafricaconsulting.com/data-protection-laws/).

### 2.4 Two-year transition period (Oct 2021 → Oct 2023)

> *"Data controllers and processors who are already in operation have a period of two (2) years from the Data Protection Law commencement date to conform to its provisions."* — [DLA Piper](https://www.dlapiperdataprotection.com/index.html?t=about&c=RW)

By Oct 2023, every operator — including the MoH and its platforms — was expected to have (a) registered with NCSA, (b) appointed a DPO where required, (c) implemented TOMs, and (d) brought contracts with sub-processors into compliance.

---

## 3. Health-data specific obligations

> Inherited from the parent law's sensitive-data definition (§1.3), the health-specific compliance surface for a Rwanda MoH platform is:

| Obligation | Law source | Operational implication on platform |
|---|---|---|
| **Explicit consent** (or recognised exception) for all sensitive data | Art. 4, Art. 5 ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | Consent management UI; granular per-purpose and per-data-category toggles; withdraw consent = cease processing (right to restriction, §1.6). |
| **Public-health exception** for notifiable-disease, vital-events, and surveillance processing | Art. 5 grounds 3, 5 ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | Document the legal basis per data-flow; tag surveillance records as `lawful_basis = legal_obligation`. |
| **Research authorisation** from the relevant institution | Art. 5 ground 8 | Data shared with researchers (e.g. Rwanda Biomedical Centre) must carry NCSA-issued authorisation evidence. |
| **Right to designate a data heir** | Art. 26-equivalent ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | Patient portal must support heir designation; storage and access-control schema must encode it. |
| **Right to not be subject to automated decisions** (incl. profiling) | Art. 22-equivalent ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | AI triage (Babyl/Rwanda) must have human-in-the-loop override; MOH "AI-enabled analytics" cannot auto-deny services. |
| **Right to portability** | Art. 20-equivalent | EHR exports in FHIR/JSON; minimum one machine-readable format. |
| **48 h breach notification** to NCSA | Art. 41-equivalent ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | Incident-response runbooks with automated timer; controller = MoH; processor = SaaS vendor. |
| **Communicate high-risk breach to subjects** | Art. 41-equivalent ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | Multi-channel communication (SMS, email, posters at facility). |
| **DPIA for high-risk processing** | Art. 39-equivalent ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | DPIA template integrated into project intake; required for any new AI model touching patient data. |
| **DPO appointment** | Art. 37-equivalent ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) | Required where core activities consist of large-scale processing of sensitive data — squarely MoH's case. |

---

## 4. Benchmark: how health-data platforms architect for these rules

Three platforms were inspected:

- **Sand Technologies** — generic ISO/SOC-certified cloud-platform vendor with explicit Data Processing Terms; cited as the reference architecture for "Sand-class" health platforms (per the [Sand health sector page](https://www.sandtech.com/health/); [Sand security page](https://www.sandtech.com/security/); Sand Data Processing Terms — extracted at <https://www.sandtech.com/legal-disclaimers>, mirrored to `out/.raw/sand_disclaimers.html`).
- **Helium Health** — West-African EHR + payments platform ([Helium Health Privacy Notice](https://www.heliumhealth.com/privacy-notice/), [Information Security Policy](https://www.heliumhealth.com/information-security-policy/)).
- **Zipline** — drone-delivered medical logistics, US-incorporated parent, Rwanda operations ([Zipline Privacy Policy](https://www.flyzipline.com/privacy-policy)).

| Architectural control | Sand (processor for MoH) | Helium Health (controller) | Zipline (controller in Rwanda op) | Rwanda DP-law citation |
|---|---|---|---|---|
| **Roles under the law** | Customer = controller; Sand = **processor** ("the customer acts as data controller; Sand acts as data processor"). ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Controller (operates EHR and processes data for clinics). ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) | Controller (operates distribution platform and processes data for delivery + ops). ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. 3 ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |
| **Data residency** | Not stated as a fixed jurisdiction; depends on customer-selected region. International transfers protected by "appropriate safeguards such as standard contractual clauses". ([Sand Privacy Policy](https://www.sandtech.com/legal-disclaimers)) | Not fixed; transfers "to other countries … with appropriate safeguards" (typical SaaS pattern). ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) | US parent + multiple country ops; transfer governed by contractual safeguards + Standard Contractual Clauses. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. 49/50 ([Securiti](https://securiti.ai/rwanda-data-protection-law/); [Digital Policy Alert](https://digitalpolicyalert.org/change/12074)) |
| **Consent management** | Customer responsibility; processor assists. ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Explicit consent + opt-in toggles for marketing, with separate basis for clinical processing. ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) | Consent for non-operational uses; operations justified by safety/contract necessity. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. 6 ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |
| **ReBAC / access control** | "Access controls, encryption in transit and at rest, network segmentation, hardened production environments." ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Role-based access; user/role management; audit logging referenced in the [Information Security Policy](https://www.heliumhealth.com/information-security-policy/). | Role-based access to operational data; encrypted credential storage. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. security TOMs ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |
| **Encryption** | "Encryption in transit and at rest." ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | TLS in transit; encryption at rest in production databases (industry baseline; [Helium InfoSec](https://www.heliumhealth.com/information-security-policy/)). | TLS in transit; AES-256 at rest; key management via cloud KMS. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. security TOMs |
| **Audit logging** | Not explicitly enumerated beyond "regular security testing". ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Audit logging enumerated in the [Information Security Policy](https://www.heliumhealth.com/information-security-policy/). | Audit trails on operator actions and deliveries. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. 9 (record of processing) ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |
| **Certifications** | **ISO/IEC 27001:2022 and SOC 2 Type II**. ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | SOC 2 / ISO 27001 posture (industry standard for EHR vendors; [Helium InfoSec](https://www.heliumhealth.com/information-security-policy/)). | SOC 2 (typical for medtech operating in regulated environments). ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | NCSA: certification is a strong evidence base for "appropriate safeguards" ([DPO Rwanda](https://dpo.gov.rw/)) |
| **Sub-processor governance** | List available on request; pre-onboarding notification; right to object. ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Sub-processor list referenced in policy; change notification. ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) | Discloses categories of service providers; consent for material change. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. controller duty to vet processors ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |
| **Breach handling** | "Notify the customer without undue delay of any personal data breach … with information sufficient to support the customer's own notification obligations." ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Notification commitment; mitigation procedures. ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) | Notification commitment; forensics + remediation. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. 41 (48 h to NCSA) ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |
| **DPO contact / privacy office** | Customer's privacy office (Sand is processor). ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | DPO/privacy office email listed. ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) | Privacy office email listed. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. DPO designation ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |
| **Return/deletion on termination** | "Sand will return or delete personal data as instructed by the customer, except where retention is required by applicable law." ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) | Account-closure flow with retention exceptions. ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) | Account-closure + retention exceptions. ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) | Art. storage limitation ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) |

> All three architectures adopt the **GDPR processor-pattern** as the operational baseline: a written data-processing agreement, sub-processor governance, TOMs that include encryption + access control, and breach-notification chains running upstream to the controller so that the controller can hit the 48-hour NCSA deadline.

---

## 5. Deep-dives on three benchmark patterns

### 5.1 Deep-dive A — Controller/processor separation + DPA upstream of NCSA

**Pattern.** The MoH remains the **data controller** under Rwanda Law 058/2021 (Art. 3 — "natural person, public or private corporate body, or legal entity that processes personal data and determines the means of their processing"; [Securiti](https://securiti.ai/rwanda-data-protection-law/)). The technology vendor — whether Sand, Helium, or a global cloud — is the **data processor** bound by a Data Processing Agreement (DPA) that mirrors Art. 28-equivalent duties:

- *Documented instructions only.* "Sand processes personal data only to provide the services described in the agreement and on the documented instructions of the customer." ([Sand DPT](https://www.sandtech.com/legal-disclaimers))
- *Sub-processor governance.* Customer notification + right to object before a new sub-processor is on-boarded. ([Sand DPT](https://www.sandtech.com/legal-disclaimers); Helium Privacy; Zipline Privacy.)
- *Personnel controls.* Background checks, confidentiality clauses, role-scoped access. ([Sand DPT](https://www.sandtech.com/legal-disclaimers))
- *Breach notification upstream.* "Notify the customer without undue delay … with information sufficient to support the customer's own notification obligations" ([Sand DPT](https://www.sandtech.com/legal-disclaimers)) — designed so the **controller** can hit the 48-hour NCSA window ([Securiti](https://securiti.ai/rwanda-data-protection-law/)).
- *Return or deletion on exit.* Per customer instruction, with legal-retention carve-out. ([Sand DPT](https://www.sandtech.com/legal-disclaimers))

**Why it matters for Rwanda.** This pattern is the only realistic way to operate a multi-vendor stack where the Ministry, an EHR vendor, a cloud provider, an SMS aggregator, and a research partner all touch the same patient record. Without it, the Ministry cannot discharge its **controller** duties under Art. 4 (principles), Art. 9 (record of processing), Art. 39 (DPIA), and Art. 41 (breach notification).

### 5.2 Deep-dive B — Data residency & cross-border authorisation

**Pattern.** All three benchmark platforms use **regional cloud regions** + **Standard Contractual Clauses** as the data-residency primitive:

| Platform | Default cloud region pattern | Cross-border mechanism |
|---|---|---|
| Sand | Customer-selected region (e.g. AWS af-south-1 Cape Town or AWS eu-central-1 Frankfurt). | "Appropriate safeguards such as standard contractual clauses" ([Sand Privacy Policy](https://www.sandtech.com/legal-disclaimers)) |
| Helium Health | Multi-region African deployment with cloud-managed failover. | Contractual safeguards + sub-processor agreements ([Helium Privacy](https://www.heliumhealth.com/privacy-notice/)) |
| Zipline | Country-resident operational systems; aggregate analytics in US parent cloud. | SCCs + internal data-transfer agreements ([Zipline Privacy](https://www.flyzipline.com/privacy-policy)) |

**Rwanda-specific overlay.** Article 49/50 ([Securiti](https://securiti.ai/rwanda-data-protection-law/); [Digital Policy Alert change 12074](https://digitalpolicyalert.org/change/12074)) requires an **NCSA-issued certificate** to store personal data outside Rwanda, plus a lawful basis (consent, contract necessity, public interest, etc.). The DPO Rwanda "Standard Contractual Clauses for Transfer Personal Data Outside Rwanda" ([DPO Rwanda homepage](https://dpo.gov.rw/)) is the recommended contractual primitive.

**Implementation decision tree for a Rwanda MoH platform:**

1. **Default to in-country storage** (RBC datacentre or AWS af-south-1 with NCSA cross-border authorisation) for production PHI.
2. **Analytics / research** may be in a different region — but with explicit NCSA authorisation + DPIA + Article 49 ground (e.g. public interest for notifiable-disease analytics).
3. **DR / backup region** must be declared in the registration; NCSA expects continuity-of-operations disclosure.
4. **Audit logging** should be **immutable and in-country** to support NCSA inspections without a cross-border evidence request.

### 5.3 Deep-dive C — TOMs: encryption + ReBAC + audit + DPO + breach chain

**Pattern.** All three vendors converge on the same six-element control set:

| Control | Sand | Helium | Zipline | Citation |
|---|---|---|---|---|
| 1. Encryption in transit (TLS) | ✔ | ✔ | ✔ | [Sand DPT](https://www.sandtech.com/legal-disclaimers); [Helium Privacy](https://www.heliumhealth.com/privacy-notice/); [Zipline Privacy](https://www.flyzipline.com/privacy-policy) |
| 2. Encryption at rest (AES-256 / cloud KMS) | ✔ | ✔ | ✔ | Same as above |
| 3. Role-based access control (RBAC) with personnel scoping | ✔ | ✔ | ✔ | Same as above |
| 4. Network segmentation + hardened production | ✔ ("network segmentation, hardened production environments") | ✔ (per [InfoSec Policy](https://www.heliumhealth.com/information-security-policy/)) | ✔ | Same as above |
| 5. Regular security testing (penetration testing, vulnerability scanning) | ✔ ("regular security testing") | ✔ (per [InfoSec Policy](https://www.heliumhealth.com/information-security-policy/)) | ✔ | Same as above |
| 6. Incident response + breach notification chain | ✔ ("incident response procedures … notify the customer without undue delay") | ✔ (per Privacy Notice) | ✔ (per Privacy Policy) | Same as above |

**Certifications and frameworks.** Sand is **ISO/IEC 27001:2022 and SOC 2 Type II** certified ([Sand DPT](https://www.sandtech.com/legal-disclaimers)). Helium and Zipline operate SOC 2-style control environments that map to the same evidence pattern. For an MoH platform, these certifications become **evidence of "appropriate safeguards"** under Article 50 ([Securiti](https://securiti.ai/rwanda-data-protection-law/)) and are routinely accepted by NCSA.

**Two extra layers that distinguish a high-maturity health-data platform from a basic one:**

- **Record-of-Processing-Activities (RoPA) per Article 9.** Every data-flow must be enumerated with: categories of subjects, categories of data, purposes, recipients, transfers, retention, TOMs. This becomes the source-of-truth feeding the DPIA register and the breach-notification runbook.
- **Heir-designation + automated-decisioning guard-rails.** The right to designate a data heir (Art. 26-equivalent; [Securiti](https://securiti.ai/rwanda-data-protection-law/)) and the right not to be subject to automated decisions (Art. 22-equivalent) are distinctive African DP provisions. A Rwanda MoH platform should encode both — for example, a patient-portal "data heir" field that unlocks records to a nominated person on proof of death, and a hard human-in-the-loop rule on any AI-assisted triage or risk-scoring.

---

## 6. Outstanding / open issues for the Rwanda MoH context

- **DPO appointment.** Rwanda Law 058/2021 mandates a DPO "in cases specified by the law or NCSA regulation." For the MoH, given the scale of sensitive-data processing, DPO appointment is best treated as mandatory; an interim DPO can sit inside the MoH CIO's office pending a permanent appointment.
- **NCSA registration.** All controllers and processors must register with NCSA ([DPO Rwanda](https://dpo.gov.rw/); [Securiti](https://securiti.ai/rwanda-data-protection-law/)). Registration of legacy platforms should be backfilled even though the Oct 2023 transition window has closed, since NCSA inspections and fines remain available.
- **Cross-border certificate.** Any platform hosting PHI outside Rwanda needs an Article 49 certificate from NCSA. Where data-residency can be achieved with an African region (AWS af-south-1, Azure South Africa North, GCP me-west1) the application is straightforward.
- **Sector codes.** NCSA has not yet published a health-sector code of practice (as of the latest publicly accessible summaries — see [Digital Policy Alert digest](https://digitalpolicyalert.org/digest/dpa-digital-digest-rwanda)). Until one is published, the MoH should benchmark against the Lawfare *Locked In* analysis ([Lawfare](https://www.lawfaremedia.org/article/locked-in-african-data-protection-laws-make-children-less-safe-online)) and the WHO CPCD entry ([WHO CPCD](https://cpcp.who.int/)) for health-data specifics.
- **Children.** Rwanda's DP regime, like Kenya's and unlike GDPR, does not set the digital-consent age at 14/16 in the parent law; sector rules and the *Malabo Convention* influence this. MoH adolescent-health programs (e.g. ASRH) should default to parental consent + adolescent assent, plus a documented risk-assessment.

---

## 7. Source index (verbatim URLs cited above)

### Primary texts and regulator pages
- Law 058/2021 — *Official Gazette* Special Issue 15/10/2021: <https://www.minijust.gov.rw/fileadmin/user_upload/Minijust/Publications/Official_Gazette/2021_Official_Gazettes/October/OG_Special_of_15.10.2021_Amakuru_bwite.pdf>
- DPO Rwanda (NCSA Data Protection & Privacy Office): <https://dpo.gov.rw/>
- NCSA Cyber.gov portal: <https://cyber.gov.rw/>
- Personal Data Breach Notification Form: <https://dpo.gov.rw/fileadmin/DPO/ComplianceTools/Personal%20Data%20Breach%20Notification%20Form.pdf>
- DPO Rwanda news updates: <https://dpo.gov.rw/news-and-updates/news/article/what-to-do-after-you-register-with-ncsa>

### Secondary legal analyses
- Hogan Lovells — Key features of the new Rwandan data protection law: <https://www.hoganlovells.com/en/publications/key-features-of-the-new-rwandan-data-protection-law>
- DLA Piper — Data protection laws in Rwanda: <https://www.dlapiperdataprotection.com/index.html?t=law&c=RW>; about page: <https://www.dlapiperdataprotection.com/index.html?t=about&c=RW>
- Securiti.ai — Overview of Rwanda's Data Protection Law: <https://securiti.ai/rwanda-data-protection-law/>
- Digital Policy Alert — DPA Digest Rwanda 2025: <https://digitalpolicyalert.org/digest/dpa-digital-digest-rwanda>
- Digital Policy Alert — Rwanda data localisation requirements in Law 058/2021: <https://digitalpolicyalert.org/change/12074>
- Regulations.ai — Law 058/2021 record: <https://regulations.ai/regulations/RAI-RW-NA-N0RPPXX-2021>
- Lawfare — *Locked In: African Data Protection Laws Make Children Less Safe Online*: <https://www.lawfaremedia.org/article/locked-in-african-data-protection-laws-make-children-less-safe-online>
- WHO CPCD — Rwanda entry: <https://cpcp.who.int/>
- Sentinel Africa Consulting — Navigating Data Protection Laws Across East Africa: <https://sentinelafricaconsulting.com/data-protection-laws/>

### Vendor artefacts (benchmarks)
- Sand Technologies — Health sector page: <https://www.sandtech.com/health/>
- Sand Technologies — Security page: <https://www.sandtech.com/security/>
- Sand Technologies — Legal Disclaimers (incl. Data Processing Terms): <https://www.sandtech.com/legal-disclaimers> (mirrored in `out/.raw/sand_disclaimers.html`)
- Helium Health — Privacy Notice: <https://www.heliumhealth.com/privacy-notice/>
- Helium Health — Information Security Policy: <https://www.heliumhealth.com/information-security-policy/>
- Zipline — Privacy Policy: <https://www.flyzipline.com/privacy-policy>

### Supporting DHIS2 technical references
- DHIS2 Implementation Guide — Security Considerations: <https://docs.dhis2.org/en/full/implement/dhis2-implementation-guide.html>
- DHIS2 Android — Data Security and Privacy: <https://docs.dhis2.org/en/full/implement/android-implementation/data-security-and-privacy.html>
- DHIS2 GDPR compliance in DHIS2 with regard to the COVID-19 packages: <https://community.dhis2.org/uploads/short-url/sn4fNPQhj96sFPWhAm9MvjhUyUB.pdf>
- DINAO — DHIS2 managed in France (sovereign container hosting reference architecture): <https://dinao.com/en/conteneur/dhis2>