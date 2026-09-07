# MODERNIZE-603 — hardcoded values (before edit)

`jndiName="jdbc/baypay-payment"` stays. That is the WAR contract, not a secret.

| XML attribute | Starter literal | Becomes |
|---|---|---|
| `serverName` | `db-east.baypay.example` | `${env.BAYPAY_DB_HOST}` |
| `portNumber` | `5432` | `${env.BAYPAY_DB_PORT}` |
| `databaseName` | `baypay` | `${env.BAYPAY_DB_NAME}` |
| `user` | `baypay_app` | `${env.BAYPAY_DB_USER}` |
| `password` | `changeme-baypay` | `${env.BAYPAY_DB_PASSWORD}` |

Also delete any comment that still names `changeme-baypay`. Features, isolated bind, pool, `/payment` stay.
