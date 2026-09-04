# Rubric — MODERNIZE-603

**Type:** MODERNIZE  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

The starter password `changeme-baypay` is the defect. A submission that still contains it must not pass Security / reliability.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | All connection fields are `${env.BAYPAY_DB_*}`; `jdbc/baypay-payment` kept; four features kept; well-formed XML | Env used for password only; host still literal | Broken JNDI name; missing features; malformed XML |
| Diagnostic method | Grepped `changeme-baypay`; listed every literal before editing | Removed password only | Opened `solutions/` first |
| Production awareness | Console / `baypayDbAlias` contrasted with `server.env`; ND is source | Mentions env without the ND contrast | Recommends storing secrets in a new cell console |
| Trade-off analysis | `server.env` vs vault/K8s secrets; one env file vs two (payment/refund); JNDI name stays | One honest trade-off | Claims env file is the final secret store forever |
| Security / reliability | No `changeme-baypay` in XML or env; password only `${env.BAYPAY_DB_PASSWORD}`; no committed password value | XML clean; env contains the fake password | Password literal remains in XML |
| Communication | `server.env` comments explain runtime injection | Files only | No env file |
| Efficiency | Checklist only; no Liberty install | Finished in session | Live cell or unused platform |

`changeme-baypay` remaining in `server.xml` caps Security / reliability at 1 and Technical accuracy at 3 or below. Reintroducing `jdbc/baypay` caps Production awareness at 1.
