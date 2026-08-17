# AWS Deployment

Host the Principal Architect Knowledge System on **S3 + CloudFront** (~$0–1/month for personal use).

## Quick Start

```bash
# 1. One-time: create S3 bucket + CloudFront (5–15 min)
make aws-setup

# 2. Build and deploy the portal
make aws-deploy
```

Share the **Portal URL** printed at the end with students.

Full guide: [AWS Deployment Guide](docs/00-start-here/aws-deployment.md) (also in the portal under Start Here).

## What Gets Created

| Resource | Purpose |
|----------|---------|
| S3 bucket | Private storage for static `build/` files |
| CloudFront | HTTPS CDN, global access for students |
| OAC | Secure S3 access (no public bucket) |

Infrastructure is defined in `infrastructure/cloudfront-static-site.yaml`.

## Configuration

After `make aws-setup`, settings are saved to `deploy/aws.env` (gitignored):

```bash
AWS_REGION=us-west-2
S3_BUCKET=principal-architect-ks-prod-277374794397
CLOUDFRONT_DISTRIBUTION_ID=E1234ABCDEF
SITE_URL=https://d1234abcd.cloudfront.net
```

Copy `deploy/aws.env.example` if you need to recreate manually.

## CI/CD (GitHub Actions)

Workflow: `.github/workflows/deploy-aws.yml`

**Secrets required** (Repository → Settings → Secrets → Actions):

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `S3_BUCKET`
- `CLOUDFRONT_DISTRIBUTION_ID`
- `SITE_URL`

Deploys automatically on push to `main` when docs change, or manually via **Actions → Deploy to AWS → Run workflow**.

## Build Targets

| Command | Description |
|---------|-------------|
| `npm run build` | Local / generic build |
| `npm run build:aws` | Build with `SITE_URL` from env |
| `npm run build:gh-pages` | GitHub Pages subpath build |
| `make aws-setup` | Create/update CloudFormation stack |
| `make aws-domain` | Attach custom domain + ACM + Route 53 |
| `make aws-deploy` | Build + S3 sync + CloudFront invalidation |

## IAM Policy (minimum)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "cloudfront:*",
        "acm:*",
        "route53:ChangeResourceRecordSets",
        "route53:ListHostedZonesByName",
        "route53:GetChange"
      ],
      "Resource": "*"
    }
  ]
}
```

Tighten to specific resources in production.

## Custom Domain (BayLearn-style)

**`bayareala8s.com` is on Wix DNS** — same as [BayLearn](https://baylearn.bayareala8s.com/). Add records in **Wix → Domains → DNS**, not Route 53.

Target URL: **`https://paks.bayareala8s.com`**

### Wix records to add

| Step | Host | Type | Points to |
|------|------|------|-----------|
| 1. ACM validation | `_9dbdf38ca242ddc073130aa19bbb0a6c.paks` | CNAME | `_4a710f4d7c8f7ba986fcb883f7e16fa7.jkddzztszm.acm-validations.aws` |
| 2. Live site (after `make aws-domain`) | `paks` | CNAME | `d2ambt9h3ai0tg.cloudfront.net` |

Then:

```bash
ACM_CERTIFICATE_ARN=arn:aws:acm:us-east-1:277374794397:certificate/bb3189ca-d056-4e4e-84dd-4ade6b24cba1 \
CUSTOM_DOMAIN=paks.bayareala8s.com \
make aws-domain

make aws-deploy
```

Full guide: [AWS Deployment — Custom Domain](docs/00-start-here/aws-deployment.md#custom-domain-baylearn-style-branded-url).

## Student URL

After deploy, students use your **custom domain** or CloudFront URL:

```
https://paks.bayareala8s.com          # after make aws-domain
https://<distribution>.cloudfront.net # default
```

Entry point: **Get Started** → [Welcome](docs/00-start-here/welcome.md)

No login required — the portal is a public static documentation site.
