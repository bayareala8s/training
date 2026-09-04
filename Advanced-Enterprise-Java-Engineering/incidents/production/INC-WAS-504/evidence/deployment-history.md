# Deployment history — payment.ear on PaymentCluster

**Gate:** 3  
**Synthetic BayPay. Change tickets are fictional.**

| When (Pacific) | Edition | Actor | Target | Notes |
|---|---|---|---|---|
| 2026-09-08 11:02 | 4.11.3 | deploy-bot | `PaymentCluster` | Routine. All three members 4.11.3 after sync complete. |
| 2026-09-18 09:40 | 4.11.3 | Morgan Hale | bindings only | Confirmed `jdbc/baypay` cell-scoped. `jdbc/baypayXA` **not** created. |
| 2026-09-22 15:40 | **4.12.0** | Jordan Voss | `PaymentCluster` | Ticket BAYPAY-5122. Install started while `nodeagent-pay-1` healthy. |

## BAYPAY-5122 release notes (excerpt)

```
payment.ear 4.12.0

PaymentBean now requires XA DataSource jdbc/baypayXA so payment
persist and jms/paymentEvents can enlist in one JTA transaction.

Resource-ref added in ibm-web-bnd / ibm-ejb-jar-bnd:
  jdbc/baypayXA  →  cell/clusters/PaymentCluster/jdbc/baypayXA

Rollback: redeploy 4.11.3 (still in the cell repository).
Feature flag: none. Mixed 4.11/4.12 is unsupported.
```

## Distribution / sync (16:12 Pacific)

| Node | Node agent | Application files | Bindings for 4.12 | Console “installed” checkbox |
|---|---|---|---|---|
| `node-pay-1` | up entire window | **4.12.0** present; Pay1 restarted onto it | resource-ref present; **XA DataSource object missing** on the node | green |
| `node-pay-2` | **restarted 15:47–15:51** | **4.11.3** still on disk; 4.12 copy incomplete | 4.12 bindings not applied | green on the *cell* app, stale on the node |
| `node-ref-1` | up | n/a (`refund.ear` only) | n/a | n/a |

Jordan Voss comment (15:53 Pacific):

> Install wizard finished on dmgr-east. I did not wait for node-pay-2 file transfer after the node agent bounce. I thought STARTED on Pay2/Pay3 meant they had the new ear.

Morgan Hale comment (16:14 Pacific):

> I can (a) stop Pay1 and restore 4.11.3 on node-pay-1, or (b) create jdbc/baypayXA, complete sync to node-pay-2, and roll Pay2/Pay3 forward. I will not do both at once. I will not bounce db-east.

## Plugin

`plugin-cfg.xml` on `ihs-east` was **not** regenerated. All three members remain in rotation. Edition is not a plugin field.

## Operator canary (15:48 Pacific)

Jordan posted a canary payment for Avery Chen against `Pay1` only from a jump host. Result: `NameNotFoundException` for `jdbc/baypayXA`. He did not halt the rollout.
