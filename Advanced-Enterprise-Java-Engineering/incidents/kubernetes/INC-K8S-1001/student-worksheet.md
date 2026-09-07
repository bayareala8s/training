# INC-K8S-1001 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Payment pods CrashLoopBackOff in baypay-prod  
**Namespace:** `baypay-prod`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06  

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: CrashLoopBackOff is kubelet backoff, not an RCA. Pod `payment-service-6c8d7f9b4-n2p8w` (and two siblings) are Ready **False**, Restart Count **7**, last State **Terminated / Error / Exit 1** after ~6s (10:18:02–10:18:08 PT). Image `…payment-service:3.9.1` **pulled** (`Pulled` 812ms, Image ID present). Not ImagePullBackOff, not Exit 137 / OOMKilled (limit is 2Gi). Process started and refused to stay up. Timeline: Sam rolled ConfigMap `payment-config` (“non-secret env cleanup”) at 17:40Z; Priya saw restarts climb before the 18:22Z page. Next suspect is **env the process received** from `payment-config` (mounted Optional:false) plus Spring fail-fast — not a bad image and not Postgres.

Gate 2: Spring Boot **failed to start** — not a kube probe kill. Logs (18:18:06Z): `Failed to bind properties under 'spring.datasource.url'` because `BAYPAY_DB_URL` is **empty**; “Prod profile refuses the localhost default.” `ApplicationContextException` / `BindException`. JVM then exits 1. Tomcat initialized 8080 then ApplicationContext failed — image and JVM ran. `JAVA_TOOL_OPTIONS` shows 75% / container support (not INC-806). CrashLoopBackOff is the kubelet reaction to that Exit 1. Question for gate 3: did Sam’s `payment-config` roll **drop or empty** `BAYPAY_DB_URL` (and which other `BAYPAY_DB_*` keys remain)?

Gate 3: Yes. After BAYPAY-10011 (`sam.okada`), `payment-config` data has `SPRING_PROFILES_ACTIVE`, `BAYPAY_DB_USER`, `BAYPAY_LOG_LEVEL`, `JAVA_TOOL_OPTIONS` — **no `BAYPAY_DB_URL`**. Secret `baypay-db` still supplies `BAYPAY_DB_PASSWORD`. Prod profile + missing URL → empty bind → Exit 1 → CrashLoop. Image 3.9.1 is fine. Registry is up. Postgres was never shown failing.

## Supporting evidence

(File, timestamp, quote. Ready, Restarts, Exit code, log line, ConfigMap keys.)

- `timeline.json` 17:40Z Sam Okada: rolled ConfigMap `payment-config` (BAYPAY-10011) “non-secret env cleanup” ahead of 3.9.1 pin. 18:05Z Priya: restart count climbing; asked for describe before another apply. 18:22Z pager: CrashLoopBackOff, Ingress 502/503, Ready 0. 18:23Z Harbor Market / Avery `c1001a11-…-111001` never 201; same Idempotency-Key.
- Gate 1 `evidence/describe.txt`: Ready False; Restart Count 7; Last State Terminated Reason=Error Exit Code=1 (started 10:18:02 finished 10:18:08); Image pulled `registry.baypay.example/baypay/payment-service:3.9.1`; envFrom `payment-config` Optional:false; Secret `BAYPAY_DB_PASSWORD`; Events `Pulled` then `Error: crash loop detected, last exit 1`. Desired 3 / Ready 0. Same last State on `-k8m1q` and `-t4r0c`.
- Gate 2 `evidence/logs.txt` 18:18:06.220Z: `Failed to bind properties under 'spring.datasource.url'` / `Value: ""` / `Origin: System Environment Property "BAYPAY_DB_URL"` / `Binding failed because BAYPAY_DB_URL is not set (empty). Prod profile refuses the localhost default.` / `ApplicationContext failed to refresh.`
- Gate 3 `evidence/configmap.yaml` 18:26Z: keys present `SPRING_PROFILES_ACTIVE`, `BAYPAY_DB_USER`, `BAYPAY_LOG_LEVEL`, `JAVA_TOOL_OPTIONS`. Ticket BAYPAY-10011. `BAYPAY_DB_URL` absent vs CLUSTER.md / healthy `infrastructure/kubernetes/payment-service/configmap.yaml`.

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

After gate 1: container previous logs (gate 2) — Exit 1 in 6s needs a Spring bind / ApplicationContext line, not a heap dump. After gate 2: ConfigMap `payment-config` (gate 3) — confirm whether `BAYPAY_DB_URL` was dropped or emptied. Omitted Deployment revision history would show whether Sam also rolled the Deployment or only the ConfigMap (timeline says ConfigMap). Thread dump / heap histogram would be empty value: process never finished start. Database metrics omitted on purpose — do not invent a SQL outage. Do not rebuild the image: describe showed a successful pull and a start.

## Stabilization action

(What restores a Ready replica *now*? Config versus revision? What do you explicitly not do?)

Restore `BAYPAY_DB_URL` on ConfigMap `payment-config` in `baypay-prod` to the last known good JDBC URL (`jdbc:postgresql://db-east.baypay.example:5432/baypay` from the healthy tree). Then restart / rolling-restart the Deployment so pods remount env (a ConfigMap edit does not by itself create a new ReplicaSet). If git still has the pre-BAYPAY-10011 ConfigMap, apply that. `kubectl rollout undo` on the Deployment is a stabilize move only if a Deployment revision also shipped; the timeline names a ConfigMap roll — undo of an unchanged image does not put the key back. Do **not** bounce Postgres. Do **not** bounce `dmgr-east`. Do **not** roll a new image “to fix CrashLoop.” Do **not** bake the URL into the image. Do **not** `kubectl` a paid cluster (paper restore).

## Remediation

(What remains after the page is quiet?)

Treat `BAYPAY_DB_URL` (and the rest of the CLUSTER `BAYPAY_DB_*` contract) as **required** in a schema / Kyverno / CI check — not an optional string with a localhost default. Keep the 3.9.1 fail-fast (refuse localhost in prod); fail in CI, not in `baypay-prod`. Gate ConfigMap rolls with a dry-run that boots the JAR against the **rendered** env. Review BAYPAY-10011 so “env cleanup” cannot drop a required key. Avery’s client reused the same Idempotency-Key — good; do not replay a second authorization once Ready returns. `rollout undo` is not a remediating control: the next “cleanup” can drop the key again.

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)

SEV-2 `baypay-prod` / `payment-service`: Ready 0/3, Ingress 502/503. Harbor Market / Avery `c1001a11-…-111001` did not get 201; same Idempotency-Key on retry.  
Pods Exit **1** in ~6s after a successful pull of `payment-service:3.9.1` — not ImagePull, not OOM 137.  
Spring bind failed: `BAYPAY_DB_URL` empty; ApplicationContext did not refresh.  
Sam’s 17:40Z `payment-config` roll (BAYPAY-10011) no longer contains `BAYPAY_DB_URL`. Restoring that key and rolling pods. Not treating this as a database outage.  
Next update when a replica is Ready. Riley asked Sam not to pin another image until then.
