# MODERNIZE-602 — starter defects (before edit)

Listed from `labs/MODERNIZE-602/starter/` before changing XML.

| File | Defect |
|---|---|
| `server.xml` `featureManager` | Only `servlet-6.0`. Missing `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`. |
| `server.xml` DataSource | `jndiName="jdbc/baypay"` — cell-wide name. Must be `jdbc/baypay-payment`. |
| `server.xml` DataSource `id` | `BayPaySharedDS` advertises a shared pool. |
| `server.xml` properties | Host, port, database, user are literals. Lab wants `${env.BAYPAY_DB_HOST}`, `${env.BAYPAY_DB_PORT}`, `${env.BAYPAY_DB_NAME}`, `${env.BAYPAY_DB_USER}`. Password already `${env.BAYPAY_DB_PASSWORD}` (keep). |
| `server.xml` pool | No `connectionManager`. Would inherit defaults and invite copying cell `maxConnections=50`. |
| `server.xml` | No `jdbc/baypayXA` (good — do not add). WAR / context `/payment` already correct. |
| `server.env` | Only `BAYPAY_DB_HOST`. Missing `BAYPAY_DB_PORT`, `BAYPAY_DB_NAME`, `BAYPAY_DB_USER`. |
| `server.env` | Must not contain a password value. `BAYPAY_DB_PASSWORD` stays process-env at runtime. |

Fix: isolated bind, four features, env-wired JDBC, own pool (not 50), well-formed XML. Checklist only — no Liberty install.
