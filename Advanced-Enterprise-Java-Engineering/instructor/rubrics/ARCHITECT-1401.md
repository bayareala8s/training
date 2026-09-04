# Rubric — ARCHITECT-1401 Design BayPay for 99.99 percent

**Type:** ARCHITECT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

The compact shape in the student lab is a *post-attempt* hint. Using it as the first draft of `PF-security.md` without a six-row table caps Diagnostic method. A plan that applies a second region or multi-AZ RDS “for realism” must not outscore a TRUST.md-based page.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Six domains (task, AZ, ALB, identity/TLS, datastore, region); multi-AZ single-region is a complete 99.99% shape; ~52 min/year named | Domains present; region or TLS thin | “Always add a region”; `PaymentCluster` as HA |
| Diagnostic method | Expanded TRUST.md + OBSERVABILITY.md (99.9% stays) after writing the table | Pasted a blog four-nines list | Opened `solutions/` first |
| Production awareness | Refuses NAT/EKS/RDS/ACM/Route 53 apply; refuses ND as HA; no `us-east-1` apply | Mentions cost without a refusal | Applied or recommended a second-region stack as the lab path |
| Trade-off analysis | 99.99% ≠ automatic multi-region; ALB is multi-AZ and still regional; SLO vs architecture goal | One honest trade-off | Four nines = two regions, no argument |
| Security / reliability | Identity/TLS is a first-class domain; HTTP `:8080` ≠ merchant HTTPS; secrets/KMS named | Mentions TLS | TLS omitted; admin task role as the design |
| Communication | Table a Staff engineer could run at 02:00 | Readable table, thin paragraphs | Fragment notes |
| Efficiency | 60–90 minutes, complete PF-security HA sections | Complete but unfocused | Incomplete worksheet |

A recommendation to apply NAT, EKS, multi-AZ RDS, or `us-east-1` for this lab caps Production awareness at 1 regardless of table quality. Silently upgrading the Module 13 SLO to 99.99% caps Technical accuracy at 3 or below.

**Pass guideline:** weighted score ≥ 70, six domains, 52 minutes named, Module 13 SLO still 99.9% unless an explicit contract change is written, `PaymentCluster` not the HA target.
