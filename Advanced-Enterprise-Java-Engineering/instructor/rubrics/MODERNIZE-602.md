# Rubric — MODERNIZE-602

**Type:** MODERNIZE  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Validation is a **checklist**, not a Liberty process. Do not deduct for skipping optional Docker. Installing traditional ND is out of scope.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | `servlet-6.0`, `jdbc-4.3`, `jndi-1.0`, `persistence-3.1`; `jdbc/baypay-payment`; `/payment`; well-formed XML | Features mostly present; one missing feature or wrong context root | Cell-wide `jdbc/baypay` remains; XML not well-formed |
| Diagnostic method | Listed starter defects (missing features, wrong JNDI, incomplete env) before editing | Edited until it “looked like” L-4.5 | Copied `solutions/` first |
| Production awareness | Isolated pool; no shared `jdbc/baypay`; ND is source, Liberty is target | Isolated name, still copies `maxConnections=50` as a shared cell fact | Recommends a new ND cell or keeps cell-wide bind “for compatibility” |
| Trade-off analysis | Liberty XML vs Boot JAR; one vs two servers for payment/refund; unused feature blast radius | One honest trade-off | “Enable everything” or “XML is just WAS” |
| Security / reliability | Password only `${env.BAYPAY_DB_PASSWORD}`; no plaintext in XML | Env used; leftover host literals (603 will finish) | Password literal in `server.xml` |
| Communication | Checklist complete; files a peer can review | Files work; no defect list | Unreadable XML |
| Efficiency | Checklist only; no required install | Finished in session | Built a live cell or unused feature pack |

Keeping `jdbc/baypay` as the Liberty bind caps Technical accuracy and Production awareness. A plaintext password caps Security / reliability at 1. Optional Open Liberty Docker neither raises nor lowers the score.
