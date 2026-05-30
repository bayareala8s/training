# Week 9 Lecture: Data Engineering for AI & Machine Learning

**Duration:** 2 hours · **Module 9**

---

## Learning Objectives

By the end of this lecture you will:

1. Explain how data engineering enables ML and generative AI workloads
2. Design feature engineering pipelines from curated zone datasets
3. Understand vector data concepts for search and RAG applications
4. Build AI-ready data pipelines with feature store patterns
5. Apply AI-specific data quality standards for training and inference

---

## 1. The Data Engineer's Role in AI/ML

Machine learning models are only as good as the data feeding them. Data engineers own the **reliable, versioned, quality-assured datasets** that data scientists and ML engineers consume.

### ML Lifecycle and Data Touchpoints

```text
Business Problem
       │
       ▼
Data Collection ──→ Data Engineering ──→ Feature Engineering
       │                    │                      │
       │                    ▼                      ▼
       │              Curated Zone            Feature Store
       │                    │                      │
       └────────────────────┴──────────────────────┘
                            │
                            ▼
                    Model Training (SageMaker)
                            │
                            ▼
                    Inference / Bedrock / Apps
```

| Phase | Data Engineer Responsibility |
|-------|------------------------------|
| **Exploration** | Provide sampled, documented datasets from curated zone |
| **Training** | Point-in-time correct feature datasets, train/val/test splits |
| **Serving** | Low-latency feature retrieval, batch inference inputs |
| **Monitoring** | Feature drift detection, prediction input validation |
| **GenAI / RAG** | Chunked documents, embeddings metadata, retrieval indexes |

---

## 2. Feature Engineering Fundamentals

### Features vs Raw Data

| Concept | Definition | Example |
|---------|------------|---------|
| **Raw attribute** | Column as captured from source | `order_amount`, `order_date` |
| **Feature** | Transformed input for ML | `customer_lifetime_value_90d`, `days_since_last_order` |
| **Label / Target** | What the model predicts | `will_churn`, `recommended_product` |

### Common Feature Transformations

- **Aggregations:** Rolling sums, counts, averages over time windows
- **Encoding:** One-hot, target encoding for categoricals
- **Scaling:** Normalization, log transforms for skewed distributions
- **Temporal:** Day-of-week, seasonality flags, recency features
- **Interaction:** Cross-features (category × region)
- **Text:** Token counts, TF-IDF, embeddings (for NLP/LLM)

### Point-in-Time Correctness

Training features must reflect **only data available at prediction time**. Leakage occurs when future information enters training features.

**Example (wrong):** `total_orders_next_30_days` as a feature to predict churn today.

**Example (correct):** `total_orders_last_30_days` computed as of each training snapshot date.

Feature stores enforce point-in-time joins between entity tables and event tables.

---

## 3. Data Preparation for ML on AWS

### Curated Zone → ML Dataset Pattern

```text
s3://datalake/curated/sales/fact_orders/     ──┐
s3://datalake/curated/customers/dim_customer/ ──┼──→ Feature Engineering Job
s3://datalake/curated/products/dim_product/   ──┘           │
                                                            ▼
                                              s3://datalake/ml/features/
                                              s3://datalake/ml/training/
                                              s3://datalake/ml/inference/
```

### AWS Services for ML Data Pipelines

| Service | Role in ML Data Pipeline |
|---------|--------------------------|
| **Amazon S3** | Storage for training data, model artifacts, embeddings |
| **AWS Glue** | Spark feature engineering at scale |
| **Amazon Athena** | Ad-hoc feature exploration and validation |
| **Amazon SageMaker Feature Store** | Online/offline feature serving |
| **Amazon Bedrock** | Foundation models; RAG with your data |
| **AWS Lambda** | Lightweight transforms, embedding orchestration |

### Train / Validation / Test Splits

| Split | Purpose | Typical Size |
|-------|---------|--------------|
| **Training** | Fit model parameters | 70–80% |
| **Validation** | Tune hyperparameters | 10–15% |
| **Test** | Final unbiased evaluation | 10–15% |

**Split strategies:**

- **Random:** Simple; risks temporal leakage for time-series
- **Temporal:** Train on past, test on future (recommended for retail, finance)
- **Entity-based:** All records for an entity in one split (avoid customer leakage)

Lab 9.1 implements temporal splits from curated orders data.

---

## 4. Feature Store Patterns

### Why Feature Stores?

Without a feature store, teams duplicate feature logic across notebooks, batch jobs, and serving code—causing **training/serving skew**.

A feature store provides:

1. **Central registry** of feature definitions and lineage
2. **Offline store** (S3/Parquet) for batch training
3. **Online store** (DynamoDB/ElastiCache) for low-latency inference
4. **Point-in-time APIs** for correct historical joins

### Logical Architecture (Course Pattern)

```text
┌─────────────────────────────────────────────────────────────┐
│                    FEATURE DEFINITIONS                       │
│         (metadata/feature_registry.json)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│  OFFLINE STORE  │                 │  ONLINE STORE   │
│  S3 / Parquet   │                 │  (optional)     │
│  ml/features/   │                 │  DynamoDB       │
└────────┬────────┘                 └────────┬────────┘
         │                                   │
         ▼                                   ▼
   SageMaker Training                  Real-time Inference
```

Lab 9.2 implements the offline store pattern with a feature registry—production teams often adopt SageMaker Feature Store or Feast on top of this foundation.

### Feature Registry Metadata

```json
{
  "feature_group": "customer_behavior",
  "version": "1.0",
  "entity_key": "customer_id",
  "features": [
    {
      "name": "order_count_30d",
      "dtype": "int",
      "description": "Orders in trailing 30 days",
      "source": "curated/sales/fact_orders"
    }
  ],
  "freshness_sla_hours": 24
}
```

---

## 5. Vector Data and Generative AI

### Embeddings and Vector Search

Large language models and recommendation systems often rely on **vector embeddings**—dense numerical representations of text, products, or users.

| Concept | Description |
|---------|-------------|
| **Embedding** | Fixed-dimension vector (e.g., 768 floats) representing semantic meaning |
| **Vector database** | Optimized store for similarity search (OpenSearch k-NN, Pinecone, pgvector) |
| **RAG** | Retrieval-Augmented Generation—fetch relevant chunks, inject into LLM prompt |

### RAG Data Pipeline

```text
Documents (PDF, HTML, tickets)
        │
        ▼
   Chunking (512 tokens, overlap 50)
        │
        ▼
   Embedding model (Bedrock Titan, open-source)
        │
        ▼
   Vector index + metadata (source, date, ACL)
        │
        ▼
   Query → Retrieve top-k → Prompt LLM → Answer
```

### Data Engineering Responsibilities for RAG

1. **Ingestion** — Sync source documents with versioning
2. **Chunking strategy** — Balance context vs retrieval precision
3. **Metadata** — Source URL, last updated, access control tags
4. **Refresh pipeline** — Re-embed when documents change
5. **Quality** — Validate chunk count, embedding dimensions, empty documents

---

## 6. LLM Data Pipelines

### Prompt Context Data

LLM applications need curated, governed context—not raw lake dumps.

| Dataset Type | Purpose | Quality Requirement |
|--------------|---------|-------------------|
| **Knowledge base** | RAG document chunks | Accurate, deduplicated, ACL-aware |
| **Fine-tuning set** | Instruction/response pairs | Human-reviewed, PII-scrubbed |
| **Evaluation set** | Benchmark Q&A with expected answers | Representative, versioned |

### Pipeline Stages for GenAI Data

```text
Raw documents → PII scan → Clean text → Chunk → Embed → Index
                      ↓
              Quarantine (PII detected)
```

Use Module 7 governance patterns (PII masking) before any text enters an embedding pipeline.

### Amazon Bedrock Integration (Optional)

- **Knowledge Bases** — Managed RAG over S3 data
- **Model access** — Claude, Titan embeddings via API
- Data engineers prepare S3 prefixes and metadata; ML engineers configure retrieval

---

## 7. AI Data Quality

Standard data quality (Module 4) is necessary but not sufficient for ML.

### ML-Specific Quality Dimensions

| Dimension | Question | Example Check |
|-----------|----------|---------------|
| **Label quality** | Are targets correct? | Spot-check 1% manual review |
| **Feature drift** | Did distributions change? | PSI > 0.2 vs training baseline |
| **Leakage** | Do features contain future info? | Correlation audit vs target |
| **Bias** | Are groups represented fairly? | Demographic parity checks |
| **Completeness** | Missing features imputed correctly? | Null rate thresholds per feature |
| **Cardinality** | Too many unique values? | High-cardinality categoricals flagged |

### Population Stability Index (PSI)

Measures distribution shift between training and production:

- PSI < 0.1 — No significant shift
- 0.1–0.2 — Moderate shift; investigate
- PSI > 0.2 — Significant drift; retrain or halt inference

Lab 9.3 implements feature distribution checks and leakage detection.

### AI Quality vs Traditional Quality

| Traditional (Module 4) | AI-Specific (Module 9) |
|------------------------|------------------------|
| `order_amount > 0` | Feature drift on `order_amount` distribution |
| Email regex valid | PII not present in embedding corpus |
| Enum status valid | Label class balance within bounds |
| Freshness SLO | Feature freshness for online serving |

---

## 8. Recommendation System Data Pattern

Preview for Assignment 9:

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Interactions │     │ User Features│     │ Item Features│
│ (clicks,buy) │     │ (demographics│     │ (category,   │
│              │     │  behavior)   │     │  price tier) │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
                   Training Matrix / Embeddings
                            │
                            ▼
              Collaborative + Content-Based Model
```

Key engineering decisions:

- Implicit vs explicit feedback encoding
- Negative sampling strategy
- Cold-start handling for new users/items
- Real-time feature refresh for session-based recommendations

---

## 9. Industry Use Cases

### Retail
Product recommendation features from clickstream + order history; embedding catalog descriptions for semantic search.

### Banking
Fraud detection features with strict point-in-time joins; no future transaction leakage.

### Healthcare
De-identified feature sets for readmission prediction; PHI never in embedding corpora.

### Media
Content embeddings for personalization; chunk transcripts for RAG-powered support bots.

---

## 10. Key Terminology

| Term | Definition |
|------|------------|
| **Feature** | ML model input derived from raw data |
| **Feature store** | System managing feature computation and serving |
| **Embedding** | Dense vector representation of data |
| **RAG** | Retrieval-Augmented Generation |
| **Training/serving skew** | Different feature logic in training vs inference |
| **Data leakage** | Future information in training features |
| **PSI** | Population Stability Index—distribution drift metric |
| **Cold start** | New user/item with no interaction history |

---

## 11. Discussion Questions

1. Why is point-in-time correctness harder in data lakes than warehouses?
2. When would you skip a feature store and use curated Parquet directly?
3. What metadata should every RAG chunk carry for governance?
4. How do you detect label leakage before deploying a model?
5. What features would you engineer for a product recommendation system?

---

## 12. This Week's Labs

| Lab | Goal |
|-----|------|
| **Lab 9.1** | Prepare ML training datasets from curated zone |
| **Lab 9.2** | Build AI-ready pipeline with feature store patterns |
| **Lab 9.3** | AI data quality validation |

**Assignment 9:** Design an AI data pipeline for a recommendation system.

---

## Further Reading

- [Amazon SageMaker Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
- [AWS Generative AI Data Governance](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-gen-ai-data/data-governance.html)
- [Feature Engineering for Machine Learning (book)](https://www.oreilly.com/library/view/feature-engineering-for/9781491953234/)

---

**Next:** [Lab 9.1 – ML Training Dataset Preparation](../labs/lab-9.1-ml-dataset-prep/README.md)
