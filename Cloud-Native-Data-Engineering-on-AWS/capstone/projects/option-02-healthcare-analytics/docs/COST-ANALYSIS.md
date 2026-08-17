# Cost Analysis – Healthcare Analytics Platform

**Author:** Capstone Reference Implementation  
**Last Updated:** 2024-01-15  
**Scenario:** Capstone Option 2 – Healthcare  
**Project key:** `cnde-cap-healthcare`  
**Region assumption:** us-east-1 · student lab scale

---

## 1. Summary

| Mode | Estimated monthly cost |
|------|------------------------|
| **Local-only** | **$0** |
| **Lab AWS** (shared `lab-cycle.sh` + light usage) | **$8 – $18** |
| **Small clinic production-like** (50 GB, daily Glue) | **$40 – $85** |

Prefer local demos; upload curated outputs only for AWS evidence.

---

## 2. Lab Breakdown

| Service | Assumption | Est. |
|---------|------------|------|
| S3 storage + requests | &lt; 5 GB | $0.20 |
| Glue job (optional) | 2 DPU × 10 min × 15 runs | $3.30 |
| Athena | Small curated scans | $0.10 |
| CloudWatch | Logs/metrics | $1.00 |
| KMS (optional CMK) | 1 key | $1.00 |
| **Total** | | **~$6 – $12** |

Idle lab stacks dominate cost—stop resources after demos.

---

## 3. Healthcare-Specific Cost Notes

- Masking/hashing CPU cost is negligible vs Glue DPU time  
- Quarantine storage is tiny relative to raw imaging (out of scope)  
- Athena cost rises if analysts scan raw by mistake—**deny raw in analyst IAM** (also a privacy control)

---

## 4. Optimizations

| Action | Savings |
|--------|---------|
| Develop with `scripts/run_local.sh` | Avoid Glue entirely in build week |
| Partition by date | Lower Athena scan |
| Parquet for curated labs | Lower scan vs CSV |
| Lifecycle expire quarantine @ 90d | Storage hygiene |
| Budget alarm $25 + tag `Project=capstone-option-2` | Governance |

---

## 5. Local vs Upload

| | Local | Upload |
|--|-------|--------|
| Privacy demo | Inspect curated CSV masks | Same files under `s3://.../capstone/cnde-cap-healthcare/` |
| Cost | $0 | S3 PUT + storage only if not running Glue |

---

## 6. Guardrails

- Monthly budget: **$25** student  
- Alert on unexpected Athena bytes scanned from `raw/`  
- Teardown via `./scripts/lab-cycle.sh stop`
