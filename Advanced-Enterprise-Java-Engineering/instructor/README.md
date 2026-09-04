# Instructor pack — Modules 1–16 and capstones

Solutions are under `../solutions/`. Rubrics are under `rubrics/`.

Do not ship this folder to students.

## Facilitation notes

- Time-box BUILD/MODERNIZE/ARCHITECT labs at 60–90 minutes; incident labs at 45–75 minutes.
- For FIX-103, FIX-902, BREAKFIX-201, INCIDENT-202, INCIDENT-402, INCIDENT-403, INCIDENT-502, INCIDENT-503, INCIDENT-504, INCIDENT-801–806, and INCIDENT-1001–1006, do not walk the room to the root cause in the first 20 minutes.
- Module 8 is the Boot canary (`pay-prod-east-2`), not `BayPayCell`. Do not accept “bounce the DMGR” as a stabilize path.
- Modules 9–10 are Dockerfile/YAML first. Do not require Docker, kind, or a live OpenShift cluster.
- Modules 11–12: `terraform validate` is the grade path. Do not require `apply`. If a student applies, confirm `us-west-2`, no NAT/EKS/RDS, and same-day destroy. Watch leftover ALBs.
- Modules 13–14 are paper plus files. Do not require live Grafana, ACM, Route 53, or a second region. Do not walk INCIDENT-1301 or INCIDENT-1402 to the RCA in the first 20 minutes. Lucky “database” or “cert expired” does not max Diagnostic method.
- Module 15: paper JSON. Do not require Bedrock. Do not accept auto-approve or a proven RCA field. Lucky “the AI is wrong” without quotes does not max Diagnostic method on AI-1504.
- Module 16: Phase A is the JSON bank plus `simulator.py`. Do not require a portal UI. One memorized paragraph for all seniorities fails. Lucky RCA in INTERVIEW-1603 does not max Diagnostic method.
- Capstones: time-box 4–8 hours (C4 90–150 minutes). Do not walk CAPSTONE-4 to the RCA in the first 20 minutes. Lucky “database” or “bad deploy” does not max Diagnostic method. C3: `terraform validate` is enough; watch leftover ALBs if anyone applies.
- Capstone 1 comes after Module 3 in the *story*; in this repo all four ship together in Stage 11.
- Score incidents with the standard weights in `COURSE_MASTER_SPEC.md` §24. A lucky guess is not a high Diagnostic method score.
- Modules 5–6 are simulation-first. Do not require a live WebSphere ND cell. Open Liberty is optional.
- Traditional WAS is the source estate. Do not accept “new ear on PaymentCluster” as a greenfield answer.
- Capstone 1 comes after Module 3; Capstone 2 waits for later stages.

## Standard rubric weights

| Dimension | Weight |
|---|---|
| Technical accuracy | 25% |
| Diagnostic method | 20% |
| Production awareness | 15% |
| Trade-off analysis | 15% |
| Security / reliability | 10% |
| Communication | 10% |
| Efficiency | 5% |
