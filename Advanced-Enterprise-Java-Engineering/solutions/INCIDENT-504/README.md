# INCIDENT-504 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

`payment.ear` **4.12** was installed during a **`nodeagent-pay-2` restart**. Synchronize to `node-pay-2` did not finish. **Pay1** (node-pay-1) runs **4.12** and **expects `jdbc/baypayXA`**. The XA DataSource object was never created (Morgan’s 18 Sep note; canary on Pay1 already threw). **Pay2** and **Pay3** still run **4.11** and look up `jdbc/baypay`. `ihs-east` still load-balances all three, so Avery Chen sees **intermittent `NameNotFoundException`** (Pay1) and occasional “wrong class” / response-shape mismatches when a retry lands on 4.11.

The cell checkbox is green because `dmgr-east` recorded the install. STARTED on Pay2/Pay3 is the old edition. Two clocks: rollout vs sync.

## Stabilization

Pick **one edition on all members**. Either:

1. **Roll Pay1 back to 4.11.3** (binaries still in the cell repository). All members use `jdbc/baypay`. Fastest restoration of a consistent contract; 4.12 / XA wait for a later window, or
2. **Complete the 4.12 path:** create and bind `jdbc/baypayXA` on every payment node, wait for `nodeagent-pay-2` healthy, finish distribution, then roll Pay2/Pay3 forward.

Do not run both directions at once. Do not bounce `db-east`. Do not click Finish again hoping sync will catch up while merchants are failing. Optional: drain Pay1 at the plugin until the cluster agrees, if you keep 4.11 on Pay2/Pay3.

Jordan’s canary against Pay1 only was not a cluster canary.

## Remediation

- **Gate deploys** on node-agent health and **full cluster distribution** (every member’s on-server edition equals the cell target).
- Refuse install start if any targeted node agent is restarting or sync is incomplete.
- Require the new JNDI object (`jdbc/baypayXA`) to exist on each node *before* the ear that looks it up is started.
- Canary must hit more than one member, or drain non-canary members.
- No mixed-edition “best effort” without a feature flag — 4.12 notes already say mixed is unsupported.
- Document the two clocks on the ARCHITECT-501 operations inset.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| Dashboard | Pay1 edition 4.12 with most 5xx; Pay2/Pay3 edition 4.11 still 2xx; node-pay-2 sync incomplete after node-agent restart; pool not exhausted |
| Logs | Pay1 `NameNotFoundException` for `jdbc/baypayXA`; Pay2/Pay3 still 4.11.3 and `jdbc/baypay`; Avery retry 201 on Pay2 |
| Deployment history | 4.12 install BAYPAY-5122; XA required; XA object missing; node-pay-2 copy interrupted; Morgan’s two-way choice |

A worksheet that says only “sync failed” with no edition table and no JNDI name scores poorly on Diagnostic method even if the phrase is directionally right.

## Comms (acceptable example)

SEV-2 during the `payment.ear` 4.12 window. Pay1 is on 4.12 and failing name lookup; Pay2 and Pay3 are still on 4.11 and completing most creates. Sync to `node-pay-2` did not finish after the node agent restart. We are restoring one edition on every member (rollback Pay1 unless XA is bound and distribution completes). `ihs-east` still has all three members — expect intermittent errors until the cluster agrees. Next update 20 minutes.
