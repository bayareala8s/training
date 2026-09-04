# Rubric — SECURITY-1404 Threat model BayPay

**Type:** SECURITY  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

The compact scope box in the student lab is a *post-attempt* hint. Generic OWASP with no BayPay names caps Diagnostic method. Exploit steps, payloads, or malware language are **not** extra credit.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | STRIDE (or named equivalent) on payments, refunds, Idempotency-Key, frozen `…222`, IAM/secrets, edge TLS, module boundary | Surfaces listed; one paragraph missing | `PaymentCluster` as the model; no frozen or idempotency row |
| Diagnostic method | TRUST.md scope first; BayPay names in cells | Pasted a blog list | Opened `solutions/` first |
| Production awareness | Refuses prod scanner, PCI ROC, KMS/ACM/RDS apply; 30/7-day TLS alerts | Mentions paper only | Scanned a live account or required a ROC |
| Trade-off analysis | Monolith vs extracted refunds; injected secrets vs SDK; 90-day leaves vs long leaves | One honest trade-off | “Encrypt everything” as the only row |
| Security / reliability | No payloads; no PAN; task ≠ execution; frozen cannot be skipped internally; keys off metric labels | Mentions IAM or TLS | Exploit PoC, payload instructions, or private key |
| Communication | PF-security threat section a Staff engineer could run | Readable table, thin paragraphs | Fragment notes |
| Efficiency | 60–90 minutes, complete threat section | Complete but unfocused | Incomplete worksheet |

Exploit / payload / malware write-ups cap Security / reliability at 1 regardless of table quality. A real PCI ROC as the deliverable caps Production awareness at 1.

**Pass guideline:** weighted score ≥ 70, named BayPay surfaces, idempotency + frozen paragraphs, no exploit content, no live apply.
