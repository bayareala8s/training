# MODERNIZE-602 — Instructor solution

**Do not share these files with students before they submit a checklist-complete `server.xml`.**

This folder is the answer key for adapting BayPay payment onto Liberty **on paper**. Students are not required to install Liberty. Traditional ND remains the source estate.

## Files

| File | Role |
|---|---|
| [server.xml](server.xml) | Features, isolated `jdbc/baypay-payment`, `${env.BAYPAY_DB_*}` |
| [server.env](server.env) | Host / port / name / user for `db-east.baypay.example` |

A student file that matches contracts (feature names, JNDI, env placeholders, `/payment`) passes even if `id` values or attribute order differ.

## What the starter got wrong

- Only `servlet-6.0` was enabled. JDBC, JNDI, and JPA were missing.
- `jndiName="jdbc/baypay"` copied the cell-wide smell.
- Host, port, database, and user were XML literals; `server.env` had only `BAYPAY_DB_HOST`.

## Required contracts

```text
features:     servlet-6.0, jdbc-4.3, jndi-1.0, persistence-3.1
jndi:         jdbc/baypay-payment
forbidden:    jdbc/baypay, jdbc/baypayXA
context:      /payment
password:     ${env.BAYPAY_DB_PASSWORD} only — no plaintext
host:         db-east.baypay.example via ${env.BAYPAY_DB_HOST}
```

Pool `maxPoolSize` is **this server’s** isolated manager. Do not treat `50` from TOPOLOGY as a shared definition to copy. Reporting stays off this pool.

## Checklist (same as the student lab)

- [x] Four features present
- [x] Isolated bind `jdbc/baypay-payment`
- [x] No cell-wide `jdbc/baypay`
- [x] No password literal in XML
- [x] `server.env` names `db-east.baypay.example` and `baypay`
- [x] Well-formed XML

## Optional Docker

Not required. If a student runs Open Liberty locally, treat it as extra. Do not deduct Efficiency for skipping Docker. Do deduct Production awareness if they reintroduce `jdbc/baypay` “so it matches the cell.”

## Diagram

AEJE-D-025: IHS still fans to `Pay1`/`Pay2`/`Pay3`; the Liberty WAR uses isolated JNDI and `server.env` toward `db-east`. No DMGR around the WAR.

## Scoring notes

Full marks require the four features, isolated JNDI, env password, and well-formed XML. Missing `jndi-1.0` or keeping `jdbc/baypay` fails Technical accuracy. A plaintext password in XML fails Security / reliability regardless of features.
