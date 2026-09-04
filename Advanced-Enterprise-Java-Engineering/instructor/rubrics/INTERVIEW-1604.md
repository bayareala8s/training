# Rubric — INTERVIEW-1604 System design

**Type:** INTERVIEW  
**awsLab:** no (paper)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

PF-design.md is the **portfolio artifact**. Slogan-only (“always add a region” / “always extract”) must **not** max Technical accuracy. Applying the design must **not** outscore a TRUST.md / Module-3 paper page.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | One prompt complete: six domains + ~52 min **or** stay/extract with a criterion; ND not HA; 99.9% SLO not silently upgraded | Decision present; domain or criterion thin | Only “add a region” or “split into microservices” |
| Diagnostic method | Expanded TRUST.md / OBSERVABILITY.md / monolith literacy after writing the page; own words | Used notes; pasted a blog list | Opened `solutions/INTERVIEW-1604/` or `solutions/ARCHITECT-1401/` first |
| Production awareness | Refuses NAT/EKS/RDS/ACM/Route 53/`us-east-1` apply; refuses ND as HA/extract target; no Bedrock/portal required | Mentions cost without a hard refusal | Applied or recommended a live stack as the lab path |
| Trade-off analysis | ≥3 honest rows; four nines ≠ automatic multi-region **or** in-process vs hop; ECS default vs EKS/OpenShift on paper | One honest trade-off | No this-quarter pick |
| Security / reliability | TLS/identity first-class (prompt 1) or idempotency + frozen `…222` on any hop (prompt 2); no PAN; Avery `c1604d44-…` named | Mentions TLS or idempotency | TLS omitted; secrets on the page |
| Communication | PF-design a Staff engineer could run at 02:00; Staff spoken slice present | Readable tables, thin paragraphs | Fragment slogans |
| Efficiency | 60–90 minutes; one prompt finished | Complete but both prompts half-done | Incomplete PF-design |

A recommendation to apply NAT, EKS, multi-AZ RDS, or `us-east-1` for this lab caps Production awareness at 1 regardless of table quality.

**Pass guideline:** weighted score ≥ 70, one prompt, drawing + this-quarter decision, ≥3 trade-offs, 52-minute paragraph **or** extract criterion, Module 13 SLO still 99.9% unless a contract change is written, `PaymentCluster` not the design, PF-design.md in the student’s words.
