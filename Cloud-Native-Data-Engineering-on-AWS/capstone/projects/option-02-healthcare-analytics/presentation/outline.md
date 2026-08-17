# Presentation Outline – Healthcare Analytics Platform

**Duration:** 15–18 minutes (+ Q&A)  
**Project:** `cnde-cap-healthcare` · Capstone Option 2

---

## Slide Deck (14 slides)

| # | Slide | Time | Content |
|---|-------|------|---------|
| 1 | Title | 0:30 | Healthcare Analytics Platform; synthetic data disclaimer |
| 2 | Problem | 1:30 | Ops needs metrics; raw extracts expose SSN/email |
| 3 | Stakeholders | 1:00 | Clinical ops, privacy office, analysts |
| 4 | Requirements | 1:00 | Masking, quarantine, department summary, audit |
| 5 | Architecture | 2:00 | Medallion + HIPAA-aware boundaries |
| 6 | Datasets | 1:00 | 30 patients / 40 appointments / 50 labs (synthetic) |
| 7 | Data quality | 1:30 | Lab 4.1 rules; show quarantine examples |
| 8 | PII masking | 1:30 | `***-**-XXXX` SSN; SHA-256 email in curated |
| 9 | Appointment summary | 1:00 | Metrics by department |
| 10 | Governance | 1:30 | IAM zones, encryption, minimum necessary |
| 11 | Cost | 1:00 | $0 local; lab ~$8–18; budget alarms |
| 12 | Demo | 3:00 | Local pipeline → masked curated → dept summary |
| 13 | Lessons | 1:00 | Mask in curated ETL, not only in dashboards |
| 14 | Q&A | — | Repo paths; `Project=capstone-option-2` |

---

## Demo Script (~4 minutes)

### Pre-demo

- [ ] `cd capstone/projects/option-02-healthcare-analytics`
- [ ] Remind audience: **synthetic only**
- [ ] Terminal ready

### Flow

| Step | Action | Say |
|------|--------|-----|
| 1 | Show `sample-data/patients.csv` SSN/email columns | "Raw landing zone keeps source shape for reprocessing—ETL only." |
| 2 | `bash scripts/run_local.sh` | "Validate, quarantine, curate—offline." |
| 3 | Open quarantine patient failures | "Bad IDs and ages never reach analytics." |
| 4 | Open `output/curated/patients/.../data.csv` | "SSN masked, email hashed—analysts never see plaintext." |
| 5 | Open curated appointments summary | "Department KPIs: counts, completion rate, duration." |
| 6 | Optional upload mention | "lab-cycle.sh + `--upload` under capstone/cnde-cap-healthcare." |

---

## Opening Story

> "A scheduling dashboard once exposed full patient emails in a shared Athena workgroup. We rebuilt the pipeline so curated marts only carry masked SSNs and hashed emails, while quality rules stop impossible ages and invalid IDs before they skew department performance reports."
