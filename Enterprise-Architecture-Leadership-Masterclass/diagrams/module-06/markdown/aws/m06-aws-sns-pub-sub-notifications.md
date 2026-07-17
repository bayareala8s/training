# SNS Pub Sub Notifications

| Field | Value |
| ----- | ----- |
| ID | `m06-aws-sns-pub-sub-notifications` |
| Category | `aws` |
| Module | `module-06` |
| Lesson | 6.2 |
| Lab | lab-06 |
| Learning objective | Integration/data architecture: SNS Pub Sub Notifications |
| AWS icons | Amazon SNS, Amazon SQS |

## Formats

- Mermaid: [`module-06/mermaid/aws/m06-aws-sns-pub-sub-notifications.mmd`](module-06/mermaid/aws/m06-aws-sns-pub-sub-notifications.mmd)
- Draw.io: [`module-06/drawio/aws/m06-aws-sns-pub-sub-notifications.drawio`](module-06/drawio/aws/m06-aws-sns-pub-sub-notifications.drawio)
- SVG: [`module-06/svg/aws/m06-aws-sns-pub-sub-notifications.svg`](module-06/svg/aws/m06-aws-sns-pub-sub-notifications.svg)
- PNG: [`module-06/png/aws/m06-aws-sns-pub-sub-notifications.png`](module-06/png/aws/m06-aws-sns-pub-sub-notifications.png)

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
flowchart TB
  Pub["Publisher"] --> SNS["SNS Topic"]
  SNS --> E1["Email"]
  SNS --> Q["SQS Subscriber"]
  SNS --> L["Lambda"]
```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
