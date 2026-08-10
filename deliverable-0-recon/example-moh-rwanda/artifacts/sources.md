# Sources & further reading

Curated, de-duplicated reference list distilled from `out/08-synthesis.md` (166 raw citations reduced to the ~45 most load-bearing). Primary sources (MoH Rwanda, RBC, HISP/DHIS2, OpenHIE, WHO, Global Fund, NCSA/DPO, peer-reviewed) are deliberately favoured over secondary press. Each thematic group is numbered independently so the artifact's in-page anchors can link per section.

## 1. Executive summary / systems inventory

1. CII-CHIN — Rwanda Health Information System Ecosystem (RHIE) Achievement Report, Jan 2025 — https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf
2. Global Fund — Rwanda Digital Health Case Study (Jan 2026) — https://www.theglobalfund.org/media/spalexqj/publication_rwanda-digital-health_casestudy_en.pdf
3. WHO CPCD — Rwanda Digital Health Strategy 2018–2023 — https://extranet.who.int/countryplanningcycles/sites/default/files/public_file_rep/RWA_Rwanda_Digital-Health-Strategy_2018-2023.Pdf
4. DHIS2 — Rwanda HMIS, powered by DHIS2 (user story) — https://docs.dhis2.org/en/topics/user-stories/rwanda-hmis-powered-by-dhis2.html
5. HISP Rwanda — national DHIS2 anchor implementation — https://hisprwanda.org/dhis2/
6. GitHub — Rwanda-EMR open facility-EMR codebase — https://github.com/Rwanda-EMR
7. GitHub — PIH openmrs-module-imbemr (IMB EMR) — https://github.com/PIH/openmrs-module-imbemr
8. UNICEF Rwanda — cEMR: piles of registers to digital CHW care — https://www.unicef.org/rwanda/stories/piles-registers-digital-care-community-health-workers-rwanda-adopt-digital-health-rec
9. The Global Fund — 2024–2027 Rwanda grants & Digital Health Impact Accelerator — https://www.theglobalfund.org/en/updates/2024/2024-07-03-rwanda-global-fund-new-grants-aids-tb-malaria-strengthen-health-systems/
10. RSSB — Mutuelle de Santé / Community-Based Health Insurance — https://www.rssb.rw/rssb-products/mutuelle-de-sante-cbhi/

## 2. Systems map

1. OpenHIE — Impact story: creating a health-information-exchange system in Rwanda (RHIE node + registries) — https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda
2. OpenHIE — Rwanda HIE impact — https://ohie.org/rwanda-hie-impact/
3. MoH Rwanda — National Health Intelligence Center launch announcement (H1 + source-feeder systems) — https://www.moh.gov.rw/news-detail/new-health-intelligence-center-to-drive-real-time-evidence-based-decisions
4. NHIC — About / six-layer data-lakehouse architecture — https://nhic.moh.gov.rw/about
5. WHO CPCD — Data-driven development: Rwanda pioneering its HIS (architecture & tiers) — https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf
6. Zipline — nationwide instant-logistics partnership (distribution-centre nodes) — https://www.globenewswire.com/news-release/2022/12/15/2574639/0/en/zipline-and-the-government-of-rwanda-announce-a-new-partnership-to-serve-the-entire-country-with-instant-logistics.html
7. CHW Central — Rwanda CHW Program summary (community tier scope) — https://chwcentral.org/wp-content/uploads/2015/02/Rwanda-CHW-Program-Summary.pdf

## 3. Persona journeys

1. WHO CPCD — Data-driven development: Rwanda pioneering its HIS (policy analyst + epi journeys) — https://extranet.who.int/countryplanningcycles/sites/default/files/country_docs/Rwanda/data-driven-development-rwanda-pioneering-his.pdf
2. SciForce — Digital health systems to support pandemic response in Rwanda (epi / eIDSR) — https://www.sciforce.com/wp-content/uploads/2021/04/Digital-health-systems-to-support-pandemic-response-in-Rwanda.pdf
3. OpenHIE — Rwanda HIE impact (hospital clinician journey) — https://ohie.org/rwanda-hie-impact/
4. MoH Rwanda — 4×4 health-workforce reform (district health officer journey) — https://www.moh.gov.rw/rwanda-pioneers-the-4x4-reform-to-strengthen-its-health-workforce
5. New Times — Rwanda launches next-generation digital tools for community health (CHW) — https://www.newtimes.co.rw/article/248405/News/rwanda-launches-next-generation-of-digital-tools-for-community-health
6. PubMed — d-IDS decision support in community digital health (CHW, peer-reviewed) — https://pubmed.ncbi.nlm.nih.gov/41687454/
7. PMC — Insightiv AI-assisted tools in community health (mUbuzima, CHW) — https://pmc.ncbi.nlm.nih.gov/articles/PMC12838494/
8. Forbes — Babyl Rwanda shuts down operations (citizen / legacy telemedicine) — https://www.forbes.com/sites/joshuadaviscampbell/2023/08/24/babyl-rwanda-shuts-down-operations/

## 4. Integration & data-flow

1. CII-CHIN RHIE report — §5.3.2 documented EMR↔VLSM FHIR + §6.3 registry edges — https://ciichin.org/wp-content/uploads/2025/01/Rwanda-Health-Information-System-Ecosystem-RHIE-Achievement-over-last-Three-years-Full-Report.pdf
2. OpenHIE — Impact story: client/facility registry push + deny model (E7/E15/E27) — https://ohie.org/impact-stories/creating-a-health-information-exchange-system-in-rwanda
3. GitHub — dhis2/integration-dhis-rapidpro (RapidPro → DHIS2 runner, E12) — https://github.com/dhis2/integration-dhis-rapidpro
4. DHIS2 developers — DHIS2 to RapidPro in the field (E12) — https://developers.dhis2.org/blog/2022/12/dhis-to-rapidpro-in-the-field
5. OpenHealthNews — DHIS2 transforming health IT standards in the developing world (RapidSMS → DHIS2, E11) — https://www.openhealthnews.com/articles/2017/dhis2-transforming-health-it-standards-developing-world-part-2
6. OpenHIM — v4.0.5 documentation (iHRIS↔RapidPro mHero flow, E19) — https://openhim.org/resources/openhim-v4.0.5.pdf
7. Oxford Open Digital Health — RCAS COVID analytics mirror & RHAP integration (E14, peer-reviewed) — https://academic.oup.com/oodh/article/doi/10.1093/oodh/oqae034/7743133
8. Zipline newsroom — government partnership delivery confirmation & facility "pull" (E18/E31) — https://www.zipline.com/newsroom/zipline-and-the-government-of-rwanda-announce-a-new-partnership-to-serve-the-entire-country-with-instant-logistics

## 5. Data-protection & Law 058/2021

1. Hogan Lovells — Key features of the new Rwanda data protection law — https://www.hoganlovells.com/en/publications/key-features-of-the-new-rwandan-data-protection-law
2. DLA Piper — Data Protection Laws of the World: Rwanda — https://www.dlapiperdataprotection.com/index.html?t=law&c=RW
3. Securiti.ai — Rwanda data protection law overview — https://securiti.ai/rwanda-data-protection-law/
4. Digital Policy Alert — Law n° 058/2021 change record — https://digitalpolicyalert.org/change/12074
5. DPO Rwanda — national data-protection authority — https://dpo.gov.rw/
6. DPO Rwanda — NCSA Personal Data Breach Notification Form (incl. Health sector) — https://dpo.gov.rw/fileadmin/DPO/ComplianceTools/Personal%20Data%20Breach%20Notification%20Form.pdf
7. OpenHIE — Specification Release 3.0 (security services, audit) — https://ohie.org/wp-content/uploads/2020/12/OpenHIE-Specification-Release-3.0.pdf
8. PMC — IeDEA de-identification pipeline in Rwanda OpenMRS (peer-reviewed) — https://pmc.ncbi.nlm.nih.gov/articles/PMC6918068/
9. DHIS2 — Security considerations (platform TOMs) — https://docs.dhis2.org/en/implement/implementing-dhis2/security-considerations.html
10. Sand — Data Protection Terms / legal disclaimers (processor pattern, ISO 27001 + SOC 2) — https://www.sandtech.com/legal-disclaimers
11. Zipline — Privacy Policy (TLS, AES-256, RBAC, SCCs) — https://www.flyzipline.com/privacy-policy
12. Tech Policy Press — Anthropic and accountability in Rwandan government (automated-decisioning gap) — https://www.techpolicy.press/anthropic-is-becoming-the-backbone-of-rwandas-government-but-who-is-accountable/

