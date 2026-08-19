# Capstone / final-assessment portfolio checklist

Copy this file into `submissions/capstones/<name>/README.md` (or `submissions/final-assessment/`) and complete every section. Diagrams may be Mermaid in-repo or an exported PNG referenced here.

## 1. Engagement summary

- Fictional enterprise:
- Business outcome:
- What is **out of scope**:

## 2. Integration inventory

| ID | Source | Destination | Style | Why this style | Rejected |
|----|--------|-------------|-------|----------------|----------|

## 3. Architecture diagram

Link or paste Mermaid. Label styles on the arrows (API / Message / Event / File / Adapter / Agent).

## 4. NFRs scored

Latency, payload, reliability, ordering, security, cost, operability — scores and the style they forced.

## 5. ADRs

At least three, using `templates/adr.md` (file vs API, event vs queue, agent HITL, or equivalent).

## 6. Working slice

```bash
./scripts/lab_up.sh <banking|ecommerce|healthcare|manufacturing>
python3 scripts/validate_lab.py <id>
./scripts/lab_down.sh <id>
```

Notes: what the slice proves vs what remains design-only.

## 7. Failure scenarios

At least: timeout/retry, poison/DLQ, duplicate, dependency down, IAM deny.

## 8. Security

Identity, classification, partner isolation, encryption, audit. Agent path: tools only.

## 9. Observability

Correlation ID, dashboard, DLQ alarm, who is paged.

## 10. Cost

What you refused to leave running (Transfer Family, NAT, idle ESB).

## Forbidden architectures (must not appear)

- LLM → production database
- 10+ GB through API Gateway as the data path
- “Everything on EventBridge” with no NFR
