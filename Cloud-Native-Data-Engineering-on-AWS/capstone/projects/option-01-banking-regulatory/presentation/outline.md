# Presentation Outline – Banking Regulatory Data Platform

**Duration:** 15–18 minutes (+ Q&A)  
**Project:** `cnde-cap-banking` · Capstone Option 1

---

## Slide Deck (14 slides)

| # | Slide | Time | Content |
|---|-------|------|---------|
| 1 | Title | 0:30 | Banking Regulatory Data Platform; Option 1; project key `cnde-cap-banking` |
| 2 | Business problem | 1:30 | Daily settlement packs fail audits when bad amounts/IDs reach reports |
| 3 | Stakeholders & outcomes | 1:00 | Compliance, finance, risk stewards; trusted daily_settlement_summary |
| 4 | Requirements | 1:00 | FR: ingest 3 datasets, quarantine, summary, lineage; NFR: encrypt, ≤$25 lab |
| 5 | Architecture overview | 2:00 | Medallion lake diagram (raw → cleaned/quarantine → curated) |
| 6 | Data zones & paths | 1:00 | Partition layout; metadata manifests for SOX evidence |
| 7 | Datasets | 1:00 | Transactions (~50), settlements (~20), accounts (~15); intentional bad rows |
| 8 | Data quality | 1:30 | Lab 4.1 rules: not_null, range, enum, regex; show pass rates |
| 9 | Curated model | 1:00 | daily_settlement_summary grouped by date, currency, status |
| 10 | Security & governance | 1:30 | IAM by zone, encryption, audit trail, tagging `Project=capstone-option-1` |
| 11 | Cost awareness | 1:00 | Local $0; lab ~$8–18; lifecycle + Glue DPU caps |
| 12 | Demo | 3:00 | Live local pipeline + quarantine + curated summary |
| 13 | Lessons learned | 1:00 | Quarantine beats silent drop; reuse lab stack |
| 14 | Q&A / repo | — | Paths to docs, `scripts/run_local.sh` |

---

## Demo Script (~4 minutes)

### Pre-demo

- [ ] `cd capstone/projects/option-01-banking-regulatory`
- [ ] Sample data present (or run `python3 src/ingestion/generate_sample_data.py`)
- [ ] Terminal ready; optional second pane on `output/`

### Flow

| Step | Action | Say |
|------|--------|-----|
| 1 | Open `sample-data/transactions.csv` and point to a bad `TX-BAD` / negative amount row | "Sources include deliberately invalid rows so we can prove quarantine." |
| 2 | Run `bash scripts/run_local.sh` | "Same runner as production logic—quality, cleaned, curated, metadata." |
| 3 | Open `output/metadata/quality-reports/transactions_report.json` | "Pass rate reflects quarantined bad transactions." |
| 4 | Open `output/quarantine/transactions/.../failed.json` | "Each failure carries rule, field, and message—steward evidence." |
| 5 | Open `output/curated/settlements/.../data.csv` | "daily_settlement_summary: counts and sums by date, currency, status." |
| 6 | (Optional) Mention `--upload` + `lab-cycle.sh` | "AWS path reuses course lab bucket under capstone/cnde-cap-banking." |

### Backup if live run fails

Show a prior `output/` tree and the quality report screenshots from the repo run.

---

## Opening Story (first 30 seconds)

> "When a single reversed wire with a blank settlement date slipped into last quarter's pack, compliance spent two weeks reconstructing totals. This platform validates every settlement and transaction, quarantines failures, and publishes an auditable daily settlement summary before analysts ever query Athena."
