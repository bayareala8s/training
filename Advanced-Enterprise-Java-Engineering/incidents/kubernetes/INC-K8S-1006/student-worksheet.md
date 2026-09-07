# INC-K8S-1006 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Ingress 503 with empty Service endpoints  
**Namespace:** `baypay-prod`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Service `payment-service` ClusterIP `10.8.200.41` port 8080. **`spec.selector.app: payment`** — not CLUSTER’s intended `app=payment-service`. Annotation: selector **not** in Sam’s Deployment label-cleanup PR (BAYPAY-10066). Hypothesis: Sam relabeled pods to `app=payment-service`; Service still queries `app=payment` → **empty Endpoints** → Ingress 503. Not CrashLoop (timeline: replicas 3). Contrast INC-1003: that pack was Ready 0 + probe 404; this pack starts with Service YAML. Next: Deployment/pod labels. Then Endpoints only to confirm the query returns zero addresses.

Gate 2: Deployment and pods now match CLUSTER: `app=payment-service` (template, matchLabels, three pods **Ready 1/1**). Service still selects **`app=payment`**. Quoted pair: selector `app=payment` vs labels `app=payment-service`. Ready-but-**unselected** — not INC-1003 (that was Ready 0 / probe 404). Question for gate 3: are Endpoints **empty** (`subsets: []`) because the Service query matches zero pods? If yes, align the pair (prefer CLUSTER `app=payment-service` on the Service). Do not delete Ingress; do not bounce Postgres; do not restart Ready pods as the fix.

Gate 3: Yes. Endpoints `subsets: []` / `<none>`. Three Ready pods exist; zero addresses. Ingress 503 is empty backends. RCA: **selector mismatch** after a one-object rename. A Service is a label query, not “the Deployment is named payment-service.”

## Supporting evidence

(File, timestamp, quote. Service selector, pod labels, Endpoints.)

- `timeline.json` 18:50Z Sam: label cleanup on Deployment (BAYPAY-10066); names now match CLUSTER intended `app` label; **Service not in the same PR**. 19:12Z Priya: replicas 3, Ingress 503; selector + pod labels before a probe hunt. 19:33Z pager: Endpoints empty. 19:34Z Avery `c1006f66-…-111006` HTTP 503; same Idempotency-Key. 19:36Z Riley: do not delete Ingress; do not bounce db-east.
- Gate 1 `evidence/service.yaml`: `selector.app: payment`; metadata label `app: payment-service`; note “selector not in the Deployment label-cleanup PR.”
- Gate 2 `evidence/deploy-labels.yaml`: template/matchLabels `app: payment-service`; pods Ready **1/1** `app=payment-service`.
- Gate 3 `evidence/endpoints.txt` 19:39Z: `subsets: []`. Contrast 1003: Running not Ready. This pack: Ready 1/1, unselected.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: Deployment labels (gate 2) — quote the pair. After gate 2: Endpoints (gate 3) — empty if the query matches nothing. Omitted probes: would be 200 if this is not 1003; do not start a probe hunt when selector ≠ labels. App logs omitted: Spring may be healthy and silent. Do not invent TLS or SQL.

## Stabilization action

(What restores Endpoints *now*? Selector versus labels? What do you explicitly not do?)

Align the pair. **Prefer** setting Service `spec.selector.app: payment-service` (CLUSTER intended; pods already there). Relabeling pods back to `app=payment` also works but undoes Sam’s CLUSTER cleanup and is a **two-object** change if Deployment `matchLabels` must stay consistent. Do **not** restart Ready pods. Do **not** delete Ingress. Do **not** bounce Postgres / `dmgr-east`. Do **not** retarget every label in the namespace. Do **not** select on `pod-template-hash` (unique per roll; Service would empty again). Paper patch only.

## Remediation

(What remains after the page is quiet?)

**kustomize `commonLabels`** (or one overlay) owns `app=payment-service` for Deployment + Service + Ingress. A hand-edited selector in a different PR is how BAYPAY-10066 shipped. CI: dry-run apply and assert Endpoints length > 0 (or a policy test: Service selector ⊆ pod template labels). Renaming `app=payment` → `app=payment-service` is **two objects**, not one. Avery’s 503 retries / same Idempotency-Key are correct.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 `payments.apps.baypay.example` HTTP **503**. Harbor Market / Avery `c1006f66-…-111006`; same Idempotency-Key.  
Pods **Ready 3/3**. Not CrashLoop, not a readiness 404.  
Service selector is **`app=payment`**. Pods are **`app=payment-service`** (Sam BAYPAY-10066; Service not in that PR). Endpoints empty.  
Patching Service selector to `app=payment-service`. Not deleting Ingress. Not bouncing db-east.  
Next update when Endpoints list three Ready addresses.
