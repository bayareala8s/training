# CloudTrail Central Audit

| Field | Value |
| ----- | ----- |
| ID | `m05-aws-cloudtrail-central-audit` |
| Category | `aws` |
| Module | `module-05` |
| Lesson | 5.2 |
| Lab | lab-05 |
| Learning objective | Cloud/platform strategy: CloudTrail Central Audit |
| AWS icons | AWS CloudTrail, Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`module-05/mermaid/aws/m05-aws-cloudtrail-central-audit.mmd`](module-05/mermaid/aws/m05-aws-cloudtrail-central-audit.mmd)
- Draw.io: [`module-05/drawio/aws/m05-aws-cloudtrail-central-audit.drawio`](module-05/drawio/aws/m05-aws-cloudtrail-central-audit.drawio)
- SVG: [`module-05/svg/aws/m05-aws-cloudtrail-central-audit.svg`](module-05/svg/aws/m05-aws-cloudtrail-central-audit.svg)
- PNG: [`module-05/png/aws/m05-aws-cloudtrail-central-audit.png`](module-05/png/aws/m05-aws-cloudtrail-central-audit.png)

## Mermaid

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#E6F2FF",
    "primaryTextColor": "#232F3E",
    "primaryBorderColor": "#146EB4",
    "lineColor": "#545B64",
    "secondaryColor": "#F0F7E6",
    "tertiaryColor": "#FFF3E0",
    "background": "#FFFFFF",
    "fontFamily": "Amazon Ember, Helvetica, Arial, sans-serif"
  }
}}%%
flowchart LR
  Acc["Member Accounts"] -->|Org Trail| CT["CloudTrail"]
  CT --> S3["S3 Log Bucket"]
  CT --> CW["CloudWatch Logs"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
