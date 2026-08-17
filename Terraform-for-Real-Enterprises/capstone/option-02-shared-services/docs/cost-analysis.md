# Cost Analysis — Capstone Option 2

| Resource | Approx monthly always-on | With lab-pause |
|----------|--------------------------|----------------|
| Hub NAT instance | ~$3–5 | ~$0 stopped |
| Spoke NAT instance | ~$3–5 | ~$0 stopped |
| Flow logs / CW | $1–5 | — |
| Transit Gateway (if added) | ~$36+ attachments | Avoid for lab |

Prefer NAT instances for demos. Document TGW costs in presentation as “production next step.”
