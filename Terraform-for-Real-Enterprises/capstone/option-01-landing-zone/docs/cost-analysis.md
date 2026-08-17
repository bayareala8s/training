# Cost Analysis — Capstone Option 1

Assumptions: `us-west-2`, NAT **instance** (t3.nano), optional lab EC2 (t3.micro), VPC flow logs low volume.

| Resource | Qty | Approx monthly (always-on) | With pause/stop |
|----------|-----|----------------------------|-----------------|
| NAT instance (shared) | 1 | ~$3–5 | ~$0 when stopped |
| Lab EC2 (workload-dev) | 0–1 | ~$7–8 | ~$0 when stopped |
| NAT Gateway (if enabled) | 1 | ~$32 + data | Destroy on pause |
| VPC / subnets / IGW | — | $0 | $0 |
| Flow logs → CloudWatch | low | $1–5 | — |
| S3 state + DynamoDB | — | <$1 | — |

**Recommendation:** run `make lab-pause` between sessions. Do not leave NAT Gateway enabled for demos.

**Tags for allocation:** `Course`, `Project`, `Environment`, `Owner`, `Capstone=option-01`.
