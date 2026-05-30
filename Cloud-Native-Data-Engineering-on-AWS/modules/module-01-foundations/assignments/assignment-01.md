# Assignment 1: Data Platform Architecture Design

**Due:** End of Week 1 · **Weight:** Part of Assignments (20%)

---

## Scenario

**RetailCo** is a mid-size e-commerce company with:

- 500K daily orders across web and mobile
- Product catalog updated hourly from internal ERP
- Customer clickstream events (~2M events/day)
- Third-party supplier inventory feeds (CSV, daily)
- Finance team needs daily revenue reports
- Marketing wants customer segmentation for campaigns
- Leadership wants a path to ML-based demand forecasting

Currently, data lives in siloed PostgreSQL databases, flat files on FTP, and a legacy Hadoop cluster that is expensive to maintain.

---

## Your Task

Design a **cloud-native data platform on AWS** that replaces the legacy Hadoop environment and supports all RetailCo use cases.

---

## Deliverables

Submit a document (2–3 pages) plus one architecture diagram containing:

### 1. Executive Summary (½ page)

- Problem statement
- Proposed solution overview
- Expected business outcomes

### 2. Architecture Diagram

Include all layers:

- Data sources
- Ingestion (batch and event-driven)
- S3 data lake zones (Raw, Cleaned, Curated)
- Processing (Glue ETL)
- Catalog and analytics (Athena)
- Monitoring and governance

Use Draw.io, Lucidchart, Mermaid, or hand-drawn (legible scan).

### 3. Component Selection (1 page)

For each layer, specify AWS services and justify your choices:

| Layer | Service(s) | Justification |
|-------|------------|---------------|
| Storage | ? | |
| Batch ingestion | ? | |
| Event ingestion | ? | |
| ETL | ? | |
| Orchestration | ? | |
| Analytics | ? | |
| Security | ? | |
| Monitoring | ? | |

### 4. Data Zone Design (½ page)

Define what data lands in each zone:

- **Raw:** List datasets and formats
- **Cleaned:** Validation rules applied
- **Curated:** Business entities / star schema subjects

Include example S3 paths for the orders dataset.

### 5. Non-Functional Requirements

Address:

- **Scalability:** How does the design handle 10× growth?
- **Cost:** 3 strategies to control AWS spend
- **Security:** How is PII (customer email, address) protected?
- **Reliability:** What happens if an ingestion job fails?

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Architecture completeness | 25 |
| AWS service justification | 25 |
| Zone design and naming | 20 |
| Non-functional requirements | 20 |
| Clarity and professionalism | 10 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-01-{your-name}.md` or PDF
- Include diagram as embedded image or separate file
- Submit via your learning platform

---

## Example S3 Path (Reference)

```text
s3://retailco-prod-datalake/raw/orders/ecommerce/year=2024/month=01/day=15/orders.parquet
s3://retailco-prod-datalake/cleaned/sales/orders/year=2024/month=01/day=15/
s3://retailco-prod-datalake/curated/sales/fact_orders/year=2024/month=01/
```

---

## Tips

- Reference concepts from [Week 1 Lecture](../lectures/week-01-lecture.md)
- Prefer managed services over self-managed clusters
- Design for the medallion architecture taught in class
- Keep the diagram readable—avoid listing every service icon

---

**Next week:** [Module 2 – Data Ingestion Patterns](../../module-02-ingestion/README.md)
