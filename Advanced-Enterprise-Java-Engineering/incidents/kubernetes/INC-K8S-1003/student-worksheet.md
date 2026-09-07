# INC-K8S-1003 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Ingress 503 while payment pods stay Running  
**Namespace:** `baypay-prod`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Pods are **Running**, Ready **False** (0/1). Not CrashLoop (Last State Completed Exit 0, Restart 1 = Sam’s roll). Image `3.9.1-slim`. Liveness `GET /actuator/health` **200**. Readiness `GET /actuator/health/readiness` **404** (×88 over 43m). Same on three pods. Desired 3 / Ready 0. Process is up; kubelet will not mark Ready because the BUILD-305 readiness path is missing on the slim image (or not mapped). Not INC-1001 Exit 1, not INC-1002 137, not “Postgres down” from this file. Next: Endpoints — expect empty if no Ready pods. Then curl Ingress only to confirm the 503 is empty backends, not TLS/app 500.

Gate 2: Endpoints `payment-service` **`subsets: []`** / `<none>`. Service selector `app=payment-service` matches the three Running pods — **not INC-1006**. Endpoints are empty **because Ready is 0**. Ingress therefore has no backend. Question for gate 3: does curl of `payments.apps.baypay.example` return **503** from the edge (no endpoints) rather than a pod 404/500 or a TLS failure? If yes, do not delete Ingress and do not bounce Postgres.

Gate 3: Yes. Ingress **HTTP 503** from **nginx** (`X-Request-Id: c1003-ing-503-001`). TLS completed. `/api/v1/payments` and even `/actuator/health` at the host are 503 — Avery never reached a pod. RCA: Sam rolled `3.9.1-slim` (BAYPAY-10033, “still has Actuator”) and left readiness on `/actuator/health/readiness`. Slim serves aggregate `/actuator/health` (liveness 200) but **404s the readiness group**. Running ≠ in Endpoints ≠ merchant path.

## Supporting evidence

(File, timestamp, quote. Ready, probe path, probe status, Endpoints, Ingress HTTP.)

- `timeline.json` 16:55Z Sam: rolled `3.9.1-slim`, left readinessProbe on BUILD-305 path (BAYPAY-10033). 17:18Z Priya: Running, Ready 0/1; describe probes before blaming DB. 17:40Z pager: host HTTP 503, Ready 0. 17:41Z Harbor Market / Avery `c1003c33-…-111003` HTTP 503; same Idempotency-Key. 17:43Z Riley: do not bounce Postgres while Ready 0/1 and process Running.
- Gate 1 `evidence/describe.txt`: Status Running; Ready False; Liveness `http://:8080/actuator/health` **200**; Readiness `http://:8080/actuator/health/readiness` **404**; Restart Count 1; Last State Completed Exit 0; image `3.9.1-slim`; Desired 3 / Ready 0.
- Gate 2 `evidence/endpoints.txt` 17:44Z: `subsets: []`; selector `app=payment-service`; comment: not a selector mismatch.
- Gate 3 `evidence/curl-ingress.txt` 17:45Z: `HTTP/1.1 503` nginx HTML; TLS ok; Avery never reached a pod.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: Endpoints (gate 2) — Ready 0 should empty the Service. After gate 2: Ingress curl (gate 3) — empty Endpoints should be edge 503, not Spring. Omitted app logs: a 404 on `/actuator/health/readiness` vs a DB-down readiness **503/503 from Actuator** (group down, path exists). Heapdump still must stay **off** the public host (BUILD-305). Deployment history omitted; timeline already names the slim roll. Do not invent SQL metrics.

## Stabilization action

(What restores Ready *now*? Probe versus image? What do you explicitly not do?)

Restore a **matching** pair: either (a) revert image to `3.9.1` (non-slim) that exposes `/actuator/health/readiness`, or (b) add the Actuator **readiness group** to slim and keep the BUILD-305 path, or (c) **emergency only** point readiness at a path slim actually serves (`/actuator/health`) — do **not** leave liveness and readiness on the same aggregate permanently. Restarting the Deployment without a path/image change will not create Endpoints. Do **not** bounce Postgres. Do **not** delete Ingress. Do **not** treat Running as healthy. Paper only.

## Remediation

(What remains after the page is quiet?)

**Contract:** kubelet paths must match BUILD-305 groups. App repo owns which groups the image exposes; platform YAML owns the probe path — a slim tag is not a free “still has Actuator.” CI must curl `/actuator/health/liveness` and `/actuator/health/readiness` against the **image** before the Deployment merges. A single `/actuator/health` for both probes is a reliability smell: a 30s DB blip should fail **readiness** (drop Endpoints) and must **not** fail **liveness** (restart the JVM). Avery’s 503 is not a domain decline; same Idempotency-Key is correct.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 `payments.apps.baypay.example` HTTP **503** (nginx). Harbor Market / Avery `c1003c33-…-111003` never reached a pod; same Idempotency-Key.  
Pods **Running**, Ready **0/3**. Not CrashLoop, not OOM.  
Liveness `/actuator/health` **200**. Readiness `/actuator/health/readiness` **404** on `3.9.1-slim`. Endpoints empty — that is the 503.  
Sam’s BAYPAY-10033 left the BUILD-305 readiness path on an image that does not expose the group. Restoring path↔image (revert slim or add the group).  
Not a database outage. Not deleting Ingress. Next update when Endpoints list three Ready addresses.
