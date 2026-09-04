# MODERNIZE-603 — Instructor solution

**Do not share these files with students before they remove `changeme-baypay` from XML.**

Traditional ND stored the DataSource secret as J2C `baypayDbAlias` in the cell console. That is **not** externalization. Liberty makes the same mistake when `password="changeme-baypay"` sits in `server.xml`.

## Files

| File | Role |
|---|---|
| [server.xml](server.xml) | Isolated `jdbc/baypay-payment`; all connection fields are `${env.BAYPAY_DB_*}` |
| [server.env](server.env) | Topology only — host, port, name, user. No password value. |

## What the starter got wrong

Features and isolated JNDI were already correct (the 602 lesson). Host, port, database, user, and password were still console-shaped literals. The fake password `changeme-baypay` must not appear in any submitted XML or env file.

## Required interpolation

| Property | XML value |
|---|---|
| `serverName` | `${env.BAYPAY_DB_HOST}` |
| `portNumber` | `${env.BAYPAY_DB_PORT}` |
| `databaseName` | `${env.BAYPAY_DB_NAME}` |
| `user` | `${env.BAYPAY_DB_USER}` |
| `password` | `${env.BAYPAY_DB_PASSWORD}` |

`server.env` supplies the first four from TOPOLOGY (`db-east.baypay.example`, `5432`, `baypay`, `baypay_app`). `BAYPAY_DB_PASSWORD` is injected at runtime. Committing `BAYPAY_DB_PASSWORD=changeme-baypay` in env is still a Security miss.

JNDI `jdbc/baypay-payment` stays in XML — it is the application lookup contract, not a secret.

## ND contrast (acceptable student sentences)

On ND, Morgan typed the password into `baypayDbAlias`. A console is a privileged GUI over the same secret. Boot already used `BAYPAY_DB_*` in `application-prod.yml`. Liberty `server.env` is the matching operator surface.

## Diagram

AEJE-D-026: hardcoded XML versus `${env.BAYPAY_DB_*}` plus runtime secret; serving path `ihs-east` → payment WAR → isolated DataSource → `db-east` unchanged.

## Scoring notes

Full marks require zero `changeme-baypay`, password only as `${env.BAYPAY_DB_PASSWORD}`, topology in env, isolated JNDI retained, features retained, well-formed XML. Moving JNDI itself into env and breaking the name is a Technical miss. Reintroducing `jdbc/baypay` caps Production awareness.
