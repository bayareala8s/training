# S3 Versioning and Replication

| Field | Value |
| ----- | ----- |
| ID | `m07-security-s3-versioning-and-replication` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.4 |
| Lab | lab-07 |
| Learning objective | Security/resilience: S3 Versioning and Replication |
| AWS icons | Amazon S3, AWS KMS |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-s3-versioning-and-replication.mmd`](module-07/mermaid/security/m07-security-s3-versioning-and-replication.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-s3-versioning-and-replication.drawio`](module-07/drawio/security/m07-security-s3-versioning-and-replication.drawio)
- SVG: [`module-07/svg/security/m07-security-s3-versioning-and-replication.svg`](module-07/svg/security/m07-security-s3-versioning-and-replication.svg)
- PNG: [`module-07/png/security/m07-security-s3-versioning-and-replication.png`](module-07/png/security/m07-security-s3-versioning-and-replication.png)

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
  P["Primary Bucket"] -->|Versioning| V["Object Versions"]
  P -->|Replication optional| S["Secondary Bucket"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
