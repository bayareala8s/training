# Lab 1.1: Build S3 Data Lake with Terraform

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-1.1-build-s3-data-lake.drawio)](../../../../docs/diagrams/drawio/lab-1.1-build-s3-data-lake.drawio) · [PNG](../../../../docs/diagrams/png/lab-1.1-build-s3-data-lake.png) · [SVG](../../../../docs/diagrams/svg/lab-1.1-build-s3-data-lake.svg)

**Estimated time:** 90 minutes · **Module 1**

---

## Objectives

- Deploy an S3 data lake using Terraform
- Configure encryption, versioning, and public access blocking
- Apply lifecycle policies for cost optimization
- Verify deployment with AWS CLI

---

## Prerequisites

- [Environment setup](../../../../setup/SETUP.md) complete
- Terraform 1.5+ installed
- AWS CLI configured

---

## Architecture

```text
Terraform
    │
    ▼
S3 Bucket (cnde-dev-datalake-{account-id})
├── Versioning: Enabled
├── Encryption: AES-256
├── Public access: Blocked
├── Lifecycle: raw/ → IA @ 90d, curated/ → Glacier @ 180d
└── Zones: raw/, cleaned/, curated/, quarantine/, metadata/
```

---

## Step 1: Configure Variables

```bash
cd infrastructure/environments/dev
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
aws_region  = "us-east-1"
environment = "dev"
project     = "cnde"
student     = "your-name"
```

---

## Step 2: Deploy

```bash
terraform init
terraform plan
terraform apply
```

Review the plan. You should see:

- 1 S3 bucket
- Versioning, encryption, public access block
- Lifecycle rules
- Zone prefix objects

Type `yes` to apply.

**Save the output:**

```bash
terraform output -json > ../../../modules/module-01-foundations/labs/lab-1.1-build-s3-data-lake/bucket-info.json
```

---

## Step 3: Verify with AWS CLI

Replace `BUCKET` with your bucket name from `terraform output`:

```bash
export BUCKET=$(terraform output -raw data_lake_bucket)

# Confirm bucket exists
aws s3 ls s3://$BUCKET/

# Verify zones
aws s3 ls s3://$BUCKET/ --recursive

# Check encryption
aws s3api get-bucket-encryption --bucket $BUCKET

# Check public access block
aws s3api get-public-access-block --bucket $BUCKET
```

Expected zone prefixes:

```text
cleaned/
curated/
metadata/
quarantine/
raw/
```

---

## Step 4: Inspect in AWS Console

1. Open **S3** → your bucket
2. Confirm **Properties** → Versioning: Enabled
3. Confirm **Permissions** → Block all public access: On
4. Confirm **Management** → Lifecycle rules present

---

## Step 5: Document Your Deployment

Create `LAB-REPORT.md` in this folder:

```markdown
# Lab 1.1 Report

## Bucket Name
<your-bucket>

## Resources Created
- S3 bucket with versioning, encryption, lifecycle

## Verification
- [ ] Zones visible in S3 console
- [ ] Encryption confirmed via CLI
- [ ] Public access blocked

## Screenshots
Attach S3 console screenshots.
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `AccessDenied` on apply | Verify IAM user has S3 and IAM permissions |
| Bucket name already exists | S3 names are global; change `project` in tfvars |
| Lifecycle warning | Ensure filter blocks are present (included in module) |

---

## Cleanup

**Do not destroy yet** — Lab 1.2 uses this bucket.

After completing Module 1:

```bash
cd infrastructure/environments/dev
terraform destroy
```

---

## What You Learned

- Infrastructure as Code for data platforms
- S3 security defaults for enterprise lakes
- Lifecycle policies for tiered storage costs
- Zone-based organization pattern

**Next:** [Lab 1.2 – Raw / Cleaned / Curated Zones](../lab-1.2-data-lake-zones/README.md)
