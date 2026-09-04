# Rubric — CAPSTONE-2 Modernize BayPay

**Type:** CAPSTONE  
**After:** Modules 4–10  
**awsLab:** no  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. Paper is enough. Absence of Docker, kind, or OpenShift must not fail the capstone. A new traditional ND cell or ND-in-Docker cannot outscore a TOPOLOGY-based brief.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Locked names (`BayPayCell`, `dmgr-east`, `PaymentCluster`, `ihs-east`); waves 0–3; Wave 1 refund + restore `refund.ear`; Wave 2 one canary + 100% `PaymentCluster`; Wave 3 + 14-day backup; AEJE-D-071 current + AEJE-D-072 target; CLUSTER.md objects | Waves numbered; one rollback thin or Ingress/Route confused | Wave 1 is payment; Wave 2 flips all members; invented hosts |
| Diagnostic method | 20% | Built inventory from TOPOLOGY.md / CLUSTER.md, then waves and tests | Pasted the four-line table and added a sentence | Opened `solutions/CAPSTONE-2/` first |
| Production awareness | 15% | ND as rollback *target* then exit; IHS canary; isolated JNDI; no DMGR bounce; **not** ND-in-Docker; **not** a new cell; paper sufficient | Mentions rollback without owners | New ND cell or “WAS profile in Docker” as the plan |
| Trade-off analysis | 15% | Refund-first vs payment-first; Liberty vs Boot; plugin canary vs DNS; Git ≠ ND backup; Ingress vs Route | One honest trade-off | Big-bang as simpler |
| Security / reliability | 10% | Sessionless `/payment`; `BAYPAY_DB_*` not in XML or image; canary must not use `jdbc/baypay`; **never** `-Xmx` = cgroup/limit | Mentions secrets or heap | Sticky `JSESSIONID` canary or password in Dockerfile |
| Communication | 10% | PF-modernize.md a Staff engineer could run at 02:00 | Readable table, thin cards | Fragment notes or lorem |
| Efficiency | 5% | 4–8 hours, paper path, no required engine | Complete but unfocused | Required live ND, paid OCP, or AWS apply |

**Automatic caps**

- Recommending a **new traditional ND cell** (or second DMGR) as greenfield or “safe rollback environment” caps Production awareness at 20 regardless of table quality.
- **ND-in-Docker** or scheduling `dmgr-east` as a Pod caps Production awareness at 20.
- Wave 1 as payment, or Wave 2 as a full `PaymentCluster` cutover, caps Technical accuracy at 60 or below.
- Bounce `dmgr-east` as rollback or stabilize caps Production awareness at 60 or below.
- `-Xmx` equal to the container / cgroup memory limit as the JVM story caps Security / reliability at 60.
- Requiring Docker, kind, or live OpenShift to pass must not lower Technical accuracy; if the *student* invented that gate, cap Efficiency at 60.

**Pass guideline:** weighted score ≥ 70, locked names present, waves 0–3 with refund-first and payment-canary rollback, AEJE-D-071 / AEJE-D-072 cited correctly, no new cell, no ND-in-Docker, PF-modernize.md filled. Optional local engines neither raise nor lower the score.
