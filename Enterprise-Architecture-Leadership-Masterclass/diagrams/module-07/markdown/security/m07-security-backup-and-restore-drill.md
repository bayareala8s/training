# Backup and Restore Drill

| Field | Value |
| ----- | ----- |
| ID | `m07-security-backup-and-restore-drill` |
| Category | `security` |
| Module | `module-07` |
| Lesson | 7.4 |
| Lab | lab-07 |
| Learning objective | Security/resilience: Backup and Restore Drill |
| AWS icons | Amazon S3, Amazon CloudWatch |

## Formats

- Mermaid: [`module-07/mermaid/security/m07-security-backup-and-restore-drill.mmd`](module-07/mermaid/security/m07-security-backup-and-restore-drill.mmd)
- Draw.io: [`module-07/drawio/security/m07-security-backup-and-restore-drill.drawio`](module-07/drawio/security/m07-security-backup-and-restore-drill.drawio)
- SVG: [`module-07/svg/security/m07-security-backup-and-restore-drill.svg`](module-07/svg/security/m07-security-backup-and-restore-drill.svg)
- PNG: [`module-07/png/security/m07-security-backup-and-restore-drill.png`](module-07/png/security/m07-security-backup-and-restore-drill.png)

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
  Backup["Backup"] --> Drill["Restore Drill"]
  Drill --> Evidence["Evidence / Report"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
