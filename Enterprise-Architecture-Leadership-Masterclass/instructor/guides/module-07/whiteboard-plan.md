# Whiteboard Plan — Module 07

**Time:** ~10–12 minutes across concept blocks  
**Materials:** Board or digital whiteboard; three colors (identity, data, detection)

---

## Sequence

### Board 1 — Trust boundaries (Lesson 7.1)

1. Draw four swim lanes: Identity | Control | Data | Detect
2. Place Partner → Operator → Roles → S3 → Alarms
3. Mark boundary crossings with a red slash; label control at each slash (AuthN, KMS, prefix IAM, alarm)

### Board 2 — STRIDE (Lesson 7.2)

1. Write S T R I D E as columns
2. Ask the room for one abuse case per column specific to settlement files
3. Star the top three; assign fictional owners (Platform, Security, Payments Ops)

### Board 3 — RTO/RPO trade-off (Lesson 7.3)

| Pattern | RPO help | RTO help | Cost |
| Versioning | Med-High | Med | Low |
| CRR | High (region) | Med | Med |
| Active-active | Highest | Highest | High |
| Drill only | Low alone | Organizational | Lowest |

Circle “versioning + drill” as default lab posture; box “CRR optional.”

### Close

Leave the control-evidence table headers drawn for lab: Risk | Control | Implementation | Evidence | Owner
