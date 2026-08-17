# Lab 3.2: Glue Crawlers and the Data Catalog

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-3.2-glue-crawlers.drawio)](../../../../docs/diagrams/drawio/lab-3.2-glue-crawlers.drawio) · [PNG](../../../../docs/diagrams/png/lab-3.2-glue-crawlers.png) · [SVG](../../../../docs/diagrams/svg/lab-3.2-glue-crawlers.svg)

**Estimated time:** 90 minutes · **Module 3**

---

## Objectives

- Configure Glue Crawlers for raw and cleaned S3 prefixes
- Understand schema inference, classifiers, and partition detection
- Register and query tables in the Glue Data Catalog via Athena
- Compare crawler-discovered schema with your ETL schema contract
- Apply recrawl and schema change policies for production readiness

---

## Prerequisites

- Lab 3.1 complete (Cleaned Parquet written to S3)
- Glue Terraform module deployed (`glue-etl`)
- Athena query access in the same AWS Region as your data lake

---


## Platform Setup

From the **repository root**, start the shared lab environment (once per session):

```bash
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh
```

Stop when finished: `./scripts/lab-cycle.sh stop --yes` (avoids ongoing AWS charges).

---


## Architecture

```text
S3 raw/retail/orders/          S3 cleaned/retail/orders/
         │                                │
         ▼                                ▼
  Glue Crawler (raw)            Glue Crawler (cleaned)
         │                                │
         └────────────┬───────────────────┘
                      ▼
           Glue Data Catalog
           Database: cnde_dev_datalake
           ├── raw_retail_orders
           └── cleaned_retail_orders
                      │
                      ▼
                 Amazon Athena
                 (SQL analytics)
```

---

## Step 1: Confirm Terraform Crawler Resources

The `glue-etl` Terraform module creates:

- A **Glue catalog database** (e.g., `cnde_dev_datalake`)
- A **cleaned zone crawler** targeting `s3://{bucket}/cleaned/`

List crawlers:

```bash
cd infrastructure/environments/dev
export BUCKET=$(terraform output -raw data_lake_bucket)
export GLUE_DB=$(terraform output -raw glue_catalog_database)

aws glue list-crawlers --query 'CrawlerNames' --output table
```

---

## Step 2: Create Raw Zone Crawler

Raw data is CSV; a dedicated crawler helps analysts explore source schema before ETL.

Create `raw-retail-orders-crawler` via CLI (or add to Terraform in a follow-up):

```bash
export GLUE_ROLE=$(aws glue get-crawler \
  --name "${GLUE_DB}-cleaned-crawler" \
  --query 'Crawler.Role' --output text 2>/dev/null || \
  aws iam list-roles --query "Roles[?contains(RoleName,'glue')].Arn | [0]" --output text)

aws glue create-crawler \
  --name "${GLUE_DB}-raw-crawler" \
  --role "${GLUE_ROLE}" \
  --database-name "${GLUE_DB}" \
  --targets "S3Targets=[{Path=s3://${BUCKET}/raw/retail/orders/}]" \
  --schema-change-policy "UpdateBehavior=UPDATE_IN_DATABASE,DeleteBehavior=LOG" \
  --recrawl-policy "RecrawlBehavior=CRAWL_NEW_FOLDERS_ONLY" \
  --configuration '{"Version":1,"CrawlerOutput":{"Partitions":{"AddOrUpdateBehavior":"InheritFromTable"}}}'
```

> **Note:** If the cleaned crawler name differs, find the Glue service role in IAM → Roles → search `glue`.

---

## Step 3: Run Crawlers

Run **cleaned** crawler first (Parquet from Lab 3.1):

```bash
export CLEANED_CRAWLER="${GLUE_DB}-cleaned-crawler"

aws glue start-crawler --name "${CLEANED_CRAWLER}"
```

Wait until state is `READY` (2–5 minutes):

```bash
aws glue get-crawler --name "${CLEANED_CRAWLER}" \
  --query 'Crawler.{State:State,LastCrawl:LastCrawl.Status}' --output table
```

Run **raw** crawler:

```bash
export RAW_CRAWLER="${GLUE_DB}-raw-crawler"

aws glue start-crawler --name "${RAW_CRAWLER}"
# Wait for READY (same as above)
```

---

## Step 4: Inspect Catalog Tables

List tables in the database:

```bash
aws glue get-tables --database-name "${GLUE_DB}" \
  --query 'TableList[].{Name:Name,Location:StorageDescriptor.Location,Columns:length(StorageDescriptor.Columns)}' \
  --output table
```

Get detailed schema for the cleaned table (table name may vary slightly — adjust):

```bash
# Find cleaned table name
export CLEANED_TABLE=$(aws glue get-tables --database-name "${GLUE_DB}" \
  --query "TableList[?contains(Name, 'clean')].Name | [0]" --output text)

aws glue get-table --database-name "${GLUE_DB}" --name "${CLEANED_TABLE}" \
  --query 'Table.{Columns:StorageDescriptor.Columns,Partitions:PartitionKeys}' \
  --output json | python -m json.tool
```

Compare columns to your Lab 3.1 `schema-contract.md`.

---

## Step 5: Query with Athena

Create an Athena workgroup (optional) or use `primary`. Set query result location:

```bash
aws s3 mb s3://${BUCKET}/athena-results/ 2>/dev/null || true
```

Run queries in **Athena console** or CLI:

```sql
-- Replace database and table names from Step 4
SELECT order_status, COUNT(*) AS order_count, SUM(total_amount) AS revenue
FROM cnde_dev_datalake.cleaned_retail_orders
WHERE year = '2024' AND month = '01' AND day = '15'
GROUP BY order_status
ORDER BY order_count DESC;
```

```sql
-- Partition pruning check: compare row counts raw vs cleaned
SELECT 'cleaned' AS zone, COUNT(*) AS cnt
FROM cnde_dev_datalake.cleaned_retail_orders
WHERE year = '2024' AND month = '01' AND day = '15';
```

**Verify partition pruning:** In Athena query details, confirm **Data scanned** is a fraction of full table size when filtering on `year`, `month`, `day`.

---

## Step 6: Schema Evolution Simulation

Simulate a new column in raw CSV:

```bash
cd modules/module-01-foundations/labs/lab-1.2-data-lake-zones
python scripts/generate_sample_orders.py --date 2024-01-16 --count 100

# Add a promotional_code column to the generated file (manual edit or script)
python -c "
import csv
from pathlib import Path
p = Path('sample-data/orders_2024-01-16.csv')
rows = list(csv.DictReader(p.open()))
for r in rows:
    r['promotional_code'] = 'LAB3PROMO'
with p.open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print('Added promotional_code column')
"

export BUCKET=$(cd ../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)
aws s3 cp sample-data/orders_2024-01-16.csv \
  s3://${BUCKET}/raw/retail/orders/year=2024/month=01/day=16/orders_2024-01-16.csv
```

Re-run raw crawler:

```bash
aws glue start-crawler --name "${RAW_CRAWLER}"
```

After crawl completes, check if `promotional_code` appears in raw table schema. Note: **cleaned ETL ignores it** until you update the contract — this is intentional schema governance.

Document in `schema-evolution-notes.md`:

- What the crawler did
- Whether ETL should adopt the new column
- Backfill strategy if yes

---

## Step 7: Crawler Best Practices Checklist

Create a checklist in your lab report:

| Setting | Recommended Value | Your Crawler |
|---------|-------------------|--------------|
| Recrawl policy | `CRAWL_NEW_FOLDERS_ONLY` | |
| Schema update | `UPDATE_IN_DATABASE` | |
| Schema delete | `LOG` (never delete in prod) | |
| Schedule | Off for labs; nightly in prod | |
| Table prefix | Consistent naming (`cleaned_`, `raw_`) | |

---

## Step 8: Lab Report

Create `LAB-REPORT.md`:

```markdown
# Lab 3.2 Report

## Crawlers
- Raw crawler: <name> — Last crawl: <status>
- Cleaned crawler: <name> — Last crawl: <status>

## Catalog Tables
| Table | Format | Partitions | Column Count |
|-------|--------|------------|--------------|
| | | | |

## Athena Queries
- Revenue by status query: <paste results summary>
- Data scanned with partition filter: <size>

## Schema Evolution
- Added promotional_code to raw: Yes/No
- Visible in catalog: Yes/No
- ETL impact: <notes>

## Screenshots
Glue Crawler run, Athena query results, Table schema in Glue console.
```

---

## Deliverables

- [ ] Raw and cleaned crawlers run successfully
- [ ] Tables visible in Glue Data Catalog
- [ ] Athena query returns results from cleaned table
- [ ] Schema evolution exercise documented
- [ ] `LAB-REPORT.md` with verification evidence

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Crawler stuck in `RUNNING` | Wait 5–10 min; check CloudWatch logs for `/aws-glue/crawlers` |
| `Insufficient Lake Formation permissions` | For labs, use IAM-only catalog; disable LF enforcement or grant LF permissions |
| Athena `TABLE_NOT_FOUND` | Run crawler first; refresh Athena schema cache (repair: `MSCK REPAIR TABLE`) |
| Partition columns missing | Ensure S3 path uses `year=`, `month=`, `day=` Hive format |
| Duplicate tables from crawler | Use single S3 target per dataset; set table prefix in crawler config |
| CSV types all `string` | Expected for raw; cleaned Parquet should have proper types |
| `HIVE_PARTITION_SCHEMA_MISMATCH` | Crawler found inconsistent partitions; fix path layout |

### Repair Partitions (if needed)

```sql
MSCK REPAIR TABLE cnde_dev_datalake.cleaned_retail_orders;
```

---

## Cleanup

Retain crawlers and tables for Lab 3.3. Remove raw crawler if created manually:

```bash
aws glue delete-crawler --name "${GLUE_DB}-raw-crawler"
```

---

## What You Learned

- Automated schema discovery with Glue Crawlers
- Catalog as the integration point for Athena and Spark
- Schema evolution behavior and governance trade-offs
- Partition-aware querying for cost-efficient analytics

**Next:** [Lab 3.3 – ETL Optimization](../lab-3.3-etl-optimization/README.md)
