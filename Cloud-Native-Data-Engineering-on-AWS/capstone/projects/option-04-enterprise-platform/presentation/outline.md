# Presentation Outline – Option 4 Enterprise Data Platform

**Duration:** 15–20 minutes + Q&A  
**Project:** `cnde-cap-enterprise`

---

## Slide Deck (15 slides)

| # | Slide | Time | Talking points |
|---|-------|------|----------------|
| 1 | Title | 0:30 | Enterprise Data Platform · Option 4 · Modules 1–9 integration |
| 2 | Problem | 1:30 | Fragmented orders/inventory/vendors; no KPI+features platform |
| 3 | Requirements | 1:00 | Medallion, multi-ingest, quality, orchestration, monitoring, ML features |
| 4 | Module coverage map | 1:30 | Table mapping Modules 1–9 → evidence files |
| 5 | Architecture | 2:00 | Full platform diagram; Step Functions spine |
| 6 | Medallion zones | 1:00 | raw→cleaned→curated→quarantine→metadata (+ features) |
| 7 | Multi-ingest | 1:00 | Parallel ASL branches for file + vendor JSON |
| 8 | Quality framework | 1:30 | Rules, gate at 85%, quarantine, reports |
| 9 | Curated products | 1:30 | enterprise_kpi_daily + customer_order_features |
| 10 | Orchestration | 1:00 | Walk `daily_etl.asl.json` states |
| 11 | Monitoring | 1:00 | Dashboard widgets + suggested alarms |
| 12 | Governance & cost | 1:00 | Vendor cost confidentiality; ~$37/mo pilot; tags |
| 13 | Demo | 3:00 | Local pipeline + KPI/features + ASL snippet |
| 14 | Lessons & roadmap | 1:00 | Platform breadth; Feature Store next; LF-TBAC |
| 15 | Q&A | — | Repo, `run_local.sh`, lab-cycle deploy notes |

---

## Demo Script (~5 minutes)

### Prep

- [ ] `bash scripts/run_local.sh` succeeds
- [ ] Open quality reports + quarantine for orders
- [ ] Open curated inventory KPI CSV and orders features CSV
- [ ] Open `src/orchestration/daily_etl.asl.json` and `monitoring/dashboard_widgets.json`

### Flow

| Step | Action | Say |
|------|--------|-----|
| 1 | Module map slide | "Every module leaves an artifact in this repo." |
| 2 | Pipeline output | "Same quality engine as Lab 4.1 across three domains." |
| 3 | Quarantine sample | "Bad vendor costs and order statuses stop here." |
| 4 | `enterprise_kpi_daily` row | "Ops gets fill rate and stockout counts daily." |
| 5 | `customer_order_features` | "ML-ready aggregates—cancel rate, AOV, GMV." |
| 6 | ASL + dashboard JSON | "Production spine: orchestrate, observe, alert." |

### Fallback

Screenshots of `output/` plus architecture mermaid rendered to PNG.
