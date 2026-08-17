# Diagrams — Module 07

Mermaid sources for slides and labs. NorthStar Financial Services is fictional.

---

## 01 — Trust boundaries (platform slice)

```mermaid
flowchart TB
  subgraph External
    Partner[Partner / operator]
  end
  subgraph TB1["Trust boundary: Identity"]
    IdP[Identity / IAM principal]
  end
  subgraph TB2["Trust boundary: Control"]
    Roles[Least-privilege roles]
    KMS[KMS CMK]
  end
  subgraph TB3["Trust boundary: Data"]
    Primary[S3 primary + versions]
    Replica[Replica or DR target]
  end
  subgraph TB4["Trust boundary: Detect"]
    Alarms[CloudWatch alarms]
    Notify[SNS]
  end
  Partner --> IdP --> Roles
  Roles --> Primary
  KMS --> Primary
  Primary --> Replica
  Primary --> Alarms --> Notify
```

---

## 02 — STRIDE to controls

```mermaid
flowchart LR
  S[Spoofing] --> C1[Strong identity / short-lived creds]
  T[Tampering] --> C2[Versioning + deny unencrypted put]
  R[Repudiation] --> C3[CloudTrail / access logs]
  I[Disclosure] --> C4[SSE-KMS + prefix IAM]
  D[DoS / destructive] --> C5[Alarms + restore runbook]
  E[Elevation] --> C6[No wildcards / permission boundaries]
```

---

## 03 — Recovery drill flow

```mermaid
sequenceDiagram
  participant S as Student
  participant B as Primary bucket
  participant V as Prior version
  participant A as Alarm / evidence
  S->>B: Upload sample Restricted object
  S->>B: Delete current version (controlled)
  S->>A: Observe alarm / note timestamp
  S->>V: Restore prior version
  S->>A: Record elapsed time vs RTO
```
