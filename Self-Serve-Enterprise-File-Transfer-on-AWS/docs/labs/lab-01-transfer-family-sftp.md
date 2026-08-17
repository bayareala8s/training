# Lab 1 — Transfer Family SFTP server

**Week 1 · Estimated time: 3 hours**

> **Terraform:** Provisioned by `./scripts/start_stack.sh`. Guide: [TERRAFORM-LABS.md](TERRAFORM-LABS.md)

## Objectives

Deploy an SFTP-enabled Transfer Family server backed by S3. Upload a file and verify the object in S3.

## Prerequisites

- Lab stack running: `./scripts/start_stack.sh --yes`
- AWS CLI configured

## Steps (Terraform lab environment)

### 1. Load outputs

```bash
export AWS_REGION=$(terraform -chdir=infra/environments/lab output -raw aws_region)
export BUCKET=$(terraform -chdir=infra/environments/lab output -raw landing_bucket)
export SFTP_HOST=$(terraform -chdir=infra/environments/lab output -raw transfer_server_endpoint)
export SFTP_USER=$(terraform -chdir=infra/environments/lab output -raw sftp_username)
./scripts/get_sftp_private_key.sh
```

### 2. Test SFTP upload

```bash
echo "partner,sku" > /tmp/sample.csv
sftp -i .lab/sftp_key.pem -o StrictHostKeyChecking=no ${SFTP_USER}@${SFTP_HOST} <<EOF
put /tmp/sample.csv sample.csv
bye
EOF
```

### 3. Verify in S3

```bash
aws s3 ls s3://${BUCKET}/partners/demo/inbound/ --recursive
```

### 4. (Optional) Console exploration

Review **Transfer Family** server, IAM access role, and **S3** versioning/KMS in the console.

## Manual / console path (optional)

If not using Terraform: create bucket, IAM role, Transfer server, and user per [Module 1](../modules/week-01.md). Reference: [Transfer IAM requirements](https://docs.aws.amazon.com/transfer/latest/userguide/requirements-roles.html).

## Deliverables

1. Architecture diagram (partner → SFTP → S3)  
2. Screenshot of S3 object after upload  
3. `submissions/week-01/README.md` with server ID and region  

## Rubric (10 pts)

| Criterion | Points |
|-----------|--------|
| Server online, SFTP upload works | 4 |
| Correct S3 prefix / home directory | 2 |
| Versioning enabled on bucket | 2 |
| Diagram + README | 2 |

## Cleanup

Stop or delete Transfer server when not in use to avoid hourly charges.
