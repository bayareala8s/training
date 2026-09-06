# BayPay architecture and stack

Three teaching pictures for [reference-apps/baypay](../../../reference-apps/baypay/README.md). Not new AEJE-D catalog IDs. BayPay is fictional.

| # | File | What to see |
|---|---|---|
| 1 | [modular-monolith.svg](modular-monolith.svg) | Five Maven modules in one JVM. Posting and notify are in-process. One database. |
| 2 | [runtime-stack.svg](runtime-stack.svg) | Laptop (`localhost:8080` + H2) versus student Fargate in `us-west-2` (ALB, no NAT/RDS). |
| 3 | [payment-path.svg](payment-path.svg) | `POST /api/v1/payments` from Idempotency-Key to `201 COMPLETED`. |

Open the SVG (or the mermaid in `*.source.md`). PNG is a raster sibling for slides.

Read left to right: **who lives in the process → where it runs → what one create does.**
