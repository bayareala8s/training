# Cost Analysis — Capstone Option 3

| Resource | Primary | Secondary | Notes |
|----------|---------|-----------|-------|
| VPC foundation | $0 | $0 | |
| NAT instance each | ~$4 | ~$4 | Stop when idle |
| Lab EC2 each | ~$8 | optional | Default secondary compute off |
| Data transfer cross-region | variable | — | Avoid large sync in lab |

**Demo tip:** set `enable_secondary_compute = false` and `enable_primary_compute = false` for architecture-only demos (~VPC only cost ≈ $0 + tiny flow logs).
