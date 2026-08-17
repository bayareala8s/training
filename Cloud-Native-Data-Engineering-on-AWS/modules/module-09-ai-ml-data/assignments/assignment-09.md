# Assignment 9: Design AI Data Pipeline for Recommendation System

**Due:** End of Week 9 · **Weight:** Part of Assignments (20%)

---

## Scenario

**RetailCo** wants a **product recommendation engine** for its e-commerce site. The data science team has selected a hybrid approach:

- **Collaborative filtering** on user–item interactions (clicks, add-to-cart, purchases)
- **Content-based filtering** using product catalog attributes and text embeddings
- **Real-time session features** for homepage personalization

Currently:

- Clickstream events land in `raw/events/clickstream/` (~2M events/day)
- Orders are in `curated/sales/fact_orders/`
- Product catalog is in `curated/products/dim_product/`
- No feature store; ML team manually exports CSVs from Athena weekly
- Last model deployment failed due to **training/serving skew** and **label leakage**

Your task is to design the **data engineering pipeline** that feeds this recommendation system—not to build the ML model itself.

---

## Your Task

Design a complete **AI data pipeline architecture** for RetailCo's recommendation system. Focus on data flow, feature engineering, quality gates, and serving patterns.

---

## Deliverables

Submit a document (3–4 pages) plus one architecture diagram containing:

### 1. Executive Summary (½ page)

- Business goal and recommendation use cases (homepage, email, post-purchase)
- Current pain points and proposed data engineering solution
- Expected outcomes (reduced skew, faster retraining, governed embeddings)

### 2. Architecture Diagram

Include all components:

- Data sources (clickstream, orders, catalog, product descriptions)
- Ingestion and streaming/batch paths
- Feature engineering and feature store (offline + online)
- Embedding pipeline for product text
- ML training dataset zones (`ml/interactions/`, `ml/features/`, `ml/embeddings/`)
- Quality validation gates
- Serving layer (batch + real-time)
- Monitoring (feature drift, embedding freshness)

Use Draw.io, Lucidchart, Mermaid, or hand-drawn (legible scan).

### 3. Feature Engineering Design (1 page)

Define at least **two feature groups**:

#### Feature Group A: `user_behavior` (entity: `customer_id`)

| Feature | Computation | Freshness |
|---------|-------------|-----------|
| `click_count_7d` | ? | ? |
| `purchase_count_30d` | ? | ? |
| `avg_session_duration_7d` | ? | ? |
| *(add 2 more)* | | |

#### Feature Group B: `item_attributes` (entity: `product_id`)

| Feature | Computation | Freshness |
|---------|-------------|-----------|
| `category` | ? | ? |
| `price_tier` | ? | ? |
| `embedding_vector` | ? | ? |
| *(add 2 more)* | | |

Include a **feature registry excerpt** in JSON (follow Lab 9.2 pattern).

### 4. Interaction Matrix Design (½ page)

Define how implicit feedback is encoded for collaborative filtering:

- Which events count as positive signals (purchase vs click vs view)?
- How are negative samples generated?
- Train/validation/test split strategy (temporal? per-user?)
- Cold-start handling for new users and new products

Example interaction record:

```json
{
  "user_id": "CUST-00142",
  "item_id": "PROD-0089",
  "event_type": "purchase",
  "event_timestamp": "2024-06-15T14:32:00Z",
  "weight": 5.0,
  "session_id": "sess-abc123"
}
```

### 5. Embedding Pipeline (½ page)

Design the product text embedding workflow:

- Source: product title + description from catalog
- PII/safety checks before embedding
- Chunking strategy (if descriptions are long)
- Model choice (e.g., Amazon Titan Embeddings, open-source alternative)
- Storage: S3 path convention and vector index (OpenSearch k-NN or similar)
- Refresh trigger when catalog updates

### 6. AI Data Quality Plan (½ page)

Define quality checks specific to this pipeline:

| Check | Threshold | Action on Fail |
|-------|-----------|----------------|
| Interaction sparsity | ? | ? |
| Label/event balance | ? | ? |
| Feature PSI (train vs prod) | ? | ? |
| Embedding dimension consistency | ? | ? |
| Duplicate interaction rate | ? | ? |

Reference Lab 9.3 patterns. Specify where the quality gate blocks promotion to `ml/training/production/`.

### 7. Serving Architecture (½ page)

Compare batch vs real-time serving:

| Mode | Use Case | Data Source | Latency Target |
|------|----------|-------------|----------------|
| Batch | Email campaigns | Offline feature store | Daily |
| Near real-time | Homepage | Online store + cache | < 100ms |
| Offline | Model retraining | S3 Parquet snapshots | Weekly |

Address **training/serving skew prevention**: single feature definition source, point-in-time joins, version pinning.

### 8. S3 Path Conventions

Provide example paths for all ML zones:

```text
s3://retailco-prod-datalake/ml/interactions/v1/train/year=2024/month=06/
s3://retailco-prod-datalake/ml/features/user_behavior/v=1.0.0/snapshot=.../
s3://retailco-prod-datalake/ml/embeddings/products/v=1/model=titan-embed/
s3://retailco-prod-datalake/quarantine/ml/interactions/run_id={uuid}/
```

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Architecture completeness and diagram | 25 |
| Feature engineering and registry design | 20 |
| Interaction matrix and split strategy | 15 |
| Embedding pipeline design | 10 |
| AI quality plan | 15 |
| Serving architecture and skew prevention | 10 |
| Clarity and professionalism | 5 |
| **Total** | **100** |

---

## Submission Format

- File: `assignment-09-{your-name}.md` or PDF
- Include architecture diagram as embedded image or separate file
- Include feature registry JSON excerpt
- Submit via your learning platform

---

## Tips

- Reference [Week 9 Lecture](../lectures/week-09-lecture.md) and Labs 9.1–9.3
- Purchases are stronger signals than clicks—weight interactions accordingly
- Temporal splits prevent leakage from future interactions into training
- Embeddings require governance (PII in product descriptions, access control on index)
- Connect monitoring to Module 8 (feature drift alarms, cost of embedding jobs)

---

**Next week:** [Module 10 – Enterprise Capstone Project](../../module-10-capstone/README.md)
