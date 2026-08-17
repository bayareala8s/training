# KMS Encryption Envelope

| Field | Value |
| ----- | ----- |
| ID | `m07-security-kms-encryption-envelope` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.2 |
| Lab | lab-07 |
| Learning objective | Security/resilience: KMS Encryption Envelope |
| AWS icons | AWS KMS, Amazon S3 |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-kms-encryption-envelope.mmd`](module-07/mermaid/security/m07-security-kms-encryption-envelope.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-kms-encryption-envelope.drawio`](module-07/drawio/security/m07-security-kms-encryption-envelope.drawio)
- SVG: [`module-07/svg/security/m07-security-kms-encryption-envelope.svg`](module-07/svg/security/m07-security-kms-encryption-envelope.svg)
- PNG: [`module-07/png/security/m07-security-kms-encryption-envelope.png`](module-07/png/security/m07-security-kms-encryption-envelope.png)

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
  App["App"] --> KMS["KMS"]
  KMS --> DEK["Data Key"]
  DEK --> S3["Encrypted Object S3"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
