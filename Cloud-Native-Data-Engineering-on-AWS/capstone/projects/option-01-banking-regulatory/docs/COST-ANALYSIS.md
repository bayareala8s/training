# Cost Analysis – Banking Regulatory Data Platform

**Author:** Capstone Reference Implementation  
**Last Updated:** 2024-01-15  
**Scenario:** Capstone Option 1 – Banking  
**Project key:** `cnde-cap-banking`  
**Assumptions:** us-east-1, student lab scale, ~1 GB raw/month, daily Glue run (optional)

---

## 1. Summary

| Mode | Estimated monthly cost |
|------|------------------------|
| **Local-only** (Python runner) | **$0** |
| **Lab AWS** (reuse `lab-cycle.sh` stack + light Glue/Athena) | **$8 – $18** |
| **Production-like small bank** (10 GB/month, daily Glue 5 DPU × 15 min) | **$45 – $90** |

Student recommendation: stay on the shared course lab stack, run locally for demos, upload outputs only when needed.

---

## 2. Lab Footprint Breakdown

| Service | Usage assumption | Est. monthly |
|---------|------------------|--------------|
| S3 Standard | 5 GB stored + requests | $0.15 |
| S3 PUT/GET | Pipeline uploads / Athena reads | $0.05 |
| AWS Glue (optional) | 2 DPU × 10 min × 20 days | $4.40 |
| Athena | 20 queries × 100 MB scanned | $0.10 |
| CloudWatch Logs / metrics | Lab dashboards | $1.00 |
| KMS (if CMK) | 1 key + API calls | $1.00 |
| Data transfer | Negligible in-region | $0.00 |
| **Total (lab)** | | **~$7 – $12** (+ idle stack if not destroyed) |

> Always run `./scripts/lab-cycle.sh stop` (or course teardown) when idle—idle Glue endpoints / leftover resources dominate student bills more than S3.

---

## 3. Cost Drivers for Settlement Workloads

1. **Glue DPU-hours** – largest variable if Spark jobs run daily with oversized DPUs  
2. **Athena bytes scanned** – unpartitioned / CSV scans vs Parquet + partition predicates  
3. **Raw retention** – 7-year regulatory retention pushes archive tiers  
4. **Failed reprocessing** – quarantine volume is tiny; full-day re-runs of Glue matter more  

---

## 4. Optimization Plan

| Optimization | Impact | Effort |
|--------------|--------|--------|
| Prefer local `run_local.sh` for development | High | Low |
| Partition by `year/month/day` | High | Already implemented |
| Convert curated to Parquet in Glue for Athena | Medium | Medium |
| Lifecycle: raw → Glacier after 90 days | High long-term | Low |
| Cap Glue at 2 DPU for lab | High | Low |
| Tag + Cost Explorer filter `Project=capstone-option-1` | Visibility | Low |

---

## 5. Comparison: Local vs Upload Path

| Activity | Local | AWS upload |
|----------|-------|------------|
| Quality + curated | Free | Same compute locally, then S3 PUT |
| Demo evidence | `output/` folder | `s3://$BUCKET/capstone/cnde-cap-banking/` |
| Auditor review | Share JSON reports | Athena over curated |

---

## 6. Production Scale Sketch (illustrative)

| Item | Assumption | Monthly |
|------|------------|---------|
| Storage (raw+curated) | 2 TB avg | ~$47 |
| Glue | 5 DPU × 20 min × 30 | ~$22 |
| Athena | 2 TB scanned | ~$10 |
| Monitoring / KMS | — | ~$5 |
| **Rough total** | | **~$84** |

FX enrichment, multi-region DR, and Lake Formation add incremental cost not required for the capstone.

---

## 7. Budget Guardrails

- Monthly budget alarm: **$25** for student accounts  
- Alert on Glue job duration &gt; 30 minutes  
- Destroy or stop lab resources after presentation week  
