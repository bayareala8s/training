# Rubric — INCIDENT-403

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky `REQUIRES_NEW` guess without logs + deploy evidence must **not** match a full diagnostic score.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | Split unit of work: payment committed, ledger rolled back; 184 demarcation | Status vs ledger named; mechanism incomplete | “Notifications are wrong” as RCA |
| Diagnostic method | Logs → dashboard → deploy; quotes payment id and coverage break at 17:10 | All files, weak quotes | Solution folder or deploy file first |
| Production awareness | Rollback 184; hold six ids out of settlement | Rollback only | Replay all COMPLETED blindly |
| Trade-off analysis | Join-caller now; outbox later — not silent isolation | Mentions outbox or JTA | Wants XA to hide the split |
| Security / reliability | 201 is not money; finance uses ledger | Mentions recon | Treats HTTP as system of record |
| Communication | Finance + merchant; no annotation name until deploy evidence | Clear, slightly technical | Accuses a developer by name |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete |

Auto-replay of the six payments without finance review caps Security / reliability at 1.
