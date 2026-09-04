# Rubric — INCIDENT-1006

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “selector mismatch” with no quoted selector and label pair must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Service `app=payment`; pods `app=payment-service`; Endpoints empty; Ready 1/1; Ingress 503 | Selector named; one side quoted | “Readiness 404” or “CrashLoop” as RCA without contrast |
| Diagnostic method | Gate 1→2→3; Endpoints opened to confirm selection; both YAML files quoted | Used all files; skipped a hypothesis | Opened solutions or Endpoints first |
| Production awareness | Align selector/labels (prefer CLUSTER.md); no Ingress delete; no DB bounce | Restart Deployment only | Delete namespace or bounce Postgres |
| Trade-off analysis | kustomize `commonLabels` vs hand edit; policy test on Endpoints | Mentions labels | Unique-per-roll hash as selector |
| Security / reliability | Avery 503 retries; two-object rename; no invented secret change | Mentions 503 | Ignores customer retries |
| Communication | Ready vs unselected named; does not invent a probe 404 | Usable, slightly over-confident | Blames “routing” with no selector value |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the pods” while they are already Ready and unselected loses Production awareness.
