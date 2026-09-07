# INC-WAS-504 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** Deployment failure  
**Cell / cluster:** `BayPayCell` / `PaymentCluster`  
**Your name / cohort:**  
**Time started:** 2026-09-06  
**Time submitted:** 2026-09-06

## Current hypothesis

Gate 1: Cell target is `payment.ear` **4.12**; members do not agree. **Pay1** (`node-pay-1`) reports **4.12**, STARTED, and is the failure: 61×5xx / 5m, `NameNotFoundException` **Pay1 only**. **Pay2** and **Pay3** (`node-pay-2`) still report **4.11**, STARTED, low 5xx (~240 ms). `nodeagent-pay-2` restarted 15:47; sync **incomplete** (“repository copy interrupted”). `nodeagent-pay-1` sync complete 15:46. `dmgr-east` is up — that is not “the cluster is on 4.12.” Pool 8–14/50 and DB CPU 19% — not INC-WAS-503. Avery `c504d333-…` 500 on Pay1, 201 on Pay2 (same key). First guess: rolling install + interrupted sync left **two editions behind one plugin**. 4.12 on Pay1 is missing a name 4.11 still has (or 4.12 expects a bind that only exists after a finished node-pay-2 rollout). Next: logs — **which name**, **which server**. Do not click Finish again (Riley).

Gate 2: Not a “bad payment.ear” and not a random JNDI outage. **Pay1 / 4.12** requires `jdbc/baypayXA`; lookup fails: `NMSV0612E` / `NameNotFoundException: Name "jdbc/baypayXA" not found in context "java:comp/env"` on Avery `c504d333-…`. **Pay2 / Pay3 / 4.11.3** still bind `jdbc/baypay`; “lookup jdbc/baypayXA skipped (4.11 code path)”; same payment **201** on Pay2. `nodeagent-pay-2` restart **interrupted file transfer**; Pay2: “no 4.12 binary on this node.” Class-load warning: Pay2 `PaymentBean` is 4.11.3 after a client spoke to 4.12 — mixed contract, not flaky merchant. Two defects stacked: (1) **split editions** (4.12 only on `node-pay-1`), (2) **4.12 shipped a required XA name that is not bound** on the member that actually got it. Next: deployment history — did 4.12 distribute to `node-pay-2`? Was `jdbc/baypayXA` in the 4.12 resource map? Forward to one 4.12 (sync + bind XA) vs back to one 4.11 (roll Pay1).

Gate 3: History confirms both stacked defects and which way to stabilize. **4.12 never finished on `node-pay-2`:** files still 4.11.3; 4.12 copy incomplete; cell checkbox green, node stale. **`jdbc/baypayXA` was never created** (Morgan 09-18: cell `jdbc/baypay` only). 4.12 release notes: `PaymentBean` requires XA so persist + `jms/paymentEvents` enlist; bind `jdbc/baypayXA` → `cell/clusters/PaymentCluster/jdbc/baypayXA`; **mixed 4.11/4.12 unsupported**; rollback is redeploy **4.11.3** (still in the cell repository). Jordan finished the wizard without waiting for `node-pay-2` transfer; he treated Pay2/Pay3 STARTED as “they have the new ear.” Canary against **Pay1 only** at 15:48 already `NameNotFoundException` — rollout was not halted. Plugin **not** regenerated; edition is not a plugin field. Morgan: (a) restore 4.11.3 on Pay1, or (b) create XA + complete sync + roll Pay2/Pay3 forward — not both, not bounce `db-east`.

Pick **(a) one 4.11.3 cluster**. 4.12 has **no proven-good member** (canary failed; XA object missing). Pay2/Pay3 are already last-known-good and serving Avery’s 201. Forward (b) is a longer mixed-contract window and needs a new resource mid-incident.

## Supporting evidence

| File | Quote |
|---|---|
| timeline.json 22:40 | Jordan: 4.12 install on `PaymentCluster`; 4.11 last known good on all three |
| timeline.json 22:47 | `nodeagent-pay-2` restarted 4m12s (watchdog); `nodeagent-pay-1` stayed up |
| timeline.json 22:52 | Console: cell edition 4.12; `node-pay-2` sync incomplete |
| timeline.json 23:10 | Harbor Market: Avery `c504d333-…` 500 then 201; same Idempotency-Key |
| dashboard.md | Pay1 **4.12** 61×5xx; Pay2/Pay3 **4.11** healthy; `NameNotFoundException` **Pay1 only** |
| dashboard.md | `node-pay-2` sync “repository copy interrupted”; pool 8–14/50; DB CPU 19% |
| logs.txt Pay1 15:46 | `payment.ear version=4.12.0`; resource-ref `jdbc/baypayXA` (required) |
| logs.txt Pay1 16:08 | `NMSV0612E` / `Name "jdbc/baypayXA" not found` on `c504d333-…` |
| logs.txt Pay2 15:47–16:00 | file transfer interrupted; **no 4.12 binary**; 4.11.3 `jdbc/baypay`; retry **201** |
| logs.txt Pay3 | sync aborted (`nodeagent-pay-2` not reachable); XA lookup skipped (4.11 path) |
| deployment-history.md 09-18 | `jdbc/baypayXA` **not created** |
| deployment-history.md 4.12 notes | XA required; mixed unsupported; rollback = redeploy 4.11.3 |
| deployment-history.md 16:12 | `node-pay-1` 4.12 present, **XA object missing**; `node-pay-2` 4.11.3 on disk |
| deployment-history.md 15:48 | Pay1-only canary already `NameNotFoundException`; rollout not halted |

No plugin file in this pack (omitted). Dashboard + Priya + history are enough: all three members still in rotation; we stabilize by **stopping / draining Pay1** from the console, not by inventing a `plugin-cfg.xml`. No heap/thread dump needed — this is edition + bind, not a hung JVM.

## Next investigation

Release / deployment history should confirm or refute: (1) 4.12 binaries actually landed on `node-pay-2` or only on `node-pay-1`; (2) whether `jdbc/baypayXA` was created/bound as part of BAYPAY-5122 or only declared in the ear; (3) last-known-good 4.11 still present on Pay1 so we can roll back; (4) whether Morgan/Jordan already marked the install “complete” on the cell. Then pick **one edition** — not “finish the click.”

## Stabilization action

Get **one** edition on every member. Two directions (Morgan already framed them):

| Direction | What | Merchant cost this window |
|---|---|---|
| **(a) Back to 4.11.3** | Drain/stop **Pay1 only**, restore 4.11.3 from the cell repository on `node-pay-1`, start Pay1 | Minutes. Pay2/Pay3 already 201. Same Idempotency-Key is safe. |
| (b) Forward to 4.12 | Create the missing XA DataSource, complete sync to `node-pay-2`, then roll Pay2 and Pay3 | Longer mixed-contract window; 4.12 has **never** succeeded (15:48 canary failed). |

**Choose (a).** Then regenerate plugin only if Pay1 was stopped and IHS still lists it (file omitted; Priya: no regen this window — console stop / drain is enough).

Do **not**: click Finish / continue 4.12; bounce `db-east`; stop **node** `was-pay-2` (takes Pay2 **and** Pay3 down); invent a feature flag (release: none); treat cell “installed” as member edition.

Boot analog (literacy): a rolling deploy with a readiness gate would not take 4.12 traffic until the new instance could bind what it needs. This ND install advanced the cell target without waiting for the node agent **and** without a working canary halt.

## Remediation

- **Sync/node-agent gate:** refuse `PaymentCluster` install if any targeted node agent is down or distribution is incomplete. Green on `dmgr-east` is not the gate.
- **Binding prerequisite:** create and verify `jdbc/baypayXA` on the cluster **before** 4.12 is targeted. Resource-ref in the ear is not a DataSource.
- **Canary halt:** Pay1-only canary already failed at 15:48 — that should have stopped the window, not “STARTED looks fine.”
- **Edition discipline:** mixed 4.11/4.12 unsupported. Optional IHS drain when a member’s reported edition ≠ agreed edition (cell target during a good rollout, last-known-good during rollback).
- Feature flags do not save you when **bindings differ by node**. They hide code paths; they do not create a missing XA object.

## Communication update

SEV-2 is a **split PaymentCluster**, not a down database and not a flaky Harbor Market client. `ihs-east` still sends Avery to all three members. Pay1 is on the new edition and failing name lookup; Pay2 and Pay3 are on last-known-good 4.11 and already returned 201 for `c504d333-…` (same Idempotency-Key). The cell console showing the new edition is not proof that `node-pay-2` received the files (`nodeagent-pay-2` bounced mid-install). We are draining Pay1 and restoring 4.11.3 so every member runs one edition. We are not finishing 4.12 in this window. Next update when Pay1 is back on 4.11 and error rate is flat.
