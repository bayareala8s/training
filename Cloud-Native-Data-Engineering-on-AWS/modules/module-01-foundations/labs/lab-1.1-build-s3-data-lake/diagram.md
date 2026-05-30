# Lab 1.1 Architecture — Build S3 Data Lake with Terraform

Deploy the RetailCo CNDE data lake foundation on S3 using Infrastructure as Code with encryption, versioning, lifecycle policies, and medallion zone prefixes.

## Infrastructure Overview

```mermaid
flowchart TB
    subgraph dev["Developer Workstation"]
        TF[Terraform CLI]
        CLI[AWS CLI]
    end

    subgraph iac["Infrastructure as Code"]
        TFVARS["terraform.tfvars<br/>project=cnde, env=dev"]
        MOD["modules/data-lake<br/>S3 module"]
    end

    subgraph aws["AWS Account"]
        S3[("Amazon S3<br/>cnde-dev-datalake-{account-id}")]

        subgraph zones["Medallion Zones"]
            RAW["raw/"]
            CLEANED["cleaned/"]
            CURATED["curated/"]
            QUAR["quarantine/"]
            META["metadata/"]
        end

        subgraph policies["Bucket Policies & Settings"]
            ENC["SSE-S3 AES-256"]
            VER["Versioning: Enabled"]
            PAB["Block Public Access"]
            LC["Lifecycle Rules"]
        end
    end

    TF --> TFVARS
    TF --> MOD
    MOD -->|terraform apply| S3
    S3 --> zones
    S3 --> policies
    LC -->|"raw/ → IA @ 90 days"| RAW
    LC -->|"curated/ → Glacier @ 180 days"| CURATED
    CLI -->|verify deployment| S3
```

## Deployment Sequence

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant TF as Terraform
    participant S3 as Amazon S3
    participant IAM as AWS IAM

    Dev->>TF: terraform init && plan && apply
    TF->>IAM: Validate credentials
    TF->>S3: Create bucket cnde-dev-datalake-{account-id}
    TF->>S3: Enable versioning & encryption
    TF->>S3: Block all public access
    TF->>S3: Apply lifecycle rules
    TF->>S3: Create zone prefix markers
    Note over S3: raw/, cleaned/, curated/, quarantine/, metadata/
    TF-->>Dev: Output data_lake_bucket
    Dev->>S3: aws s3 ls / get-bucket-encryption
```

## Key Components

| Component | AWS Service | Purpose |
|-----------|-------------|---------|
| Data Lake Bucket | Amazon S3 | Central storage for RetailCo medallion architecture |
| Zone Prefixes | Amazon S3 | Logical separation of raw, cleaned, curated, quarantine, metadata |
| Server-Side Encryption | Amazon S3 (SSE-S3) | Encrypt all objects at rest with AES-256 |
| Versioning | Amazon S3 | Protect against accidental overwrites and enable recovery |
| Public Access Block | Amazon S3 | Prevent accidental public exposure of data |
| Lifecycle Rules | Amazon S3 | Tier raw data to IA and curated data to Glacier for cost optimization |
| IaC Deployment | Terraform | Reproducible, version-controlled infrastructure provisioning |

## S3 Path Conventions

| Zone | Path Pattern | Notes |
|------|--------------|-------|
| Bucket | `s3://cnde-dev-datalake-{account-id}/` | Globally unique; `{account-id}` from AWS account |
| Raw | `raw/` | Append-only landing zone for source data |
| Cleaned | `cleaned/` | Validated, typed data (populated in Module 3) |
| Curated | `curated/` | Business-ready aggregates and star schemas |
| Quarantine | `quarantine/` | Failed validation records and error manifests |
| Metadata | `metadata/` | Manifests, watermarks, and dataset documentation |

## Lifecycle Policy Summary

| Prefix | Transition | Timing |
|--------|------------|--------|
| `raw/` | Standard → S3 Standard-IA | 90 days |
| `curated/` | Standard → S3 Glacier | 180 days |
