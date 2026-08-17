# Week 6 Labs — Observability & governance

## Audit query

After running APIs or Lambdas:

```bash
export AUDIT_TABLE_NAME=ba-la8s-ai-yourname-audit
python week06/query_audit.py <correlation-id-from-api-response>
```

## Dashboard & alarm

- Open CloudWatch → Dashboards → `{ProjectPrefix}-ai-ops` (includes capstone widgets after Week 8 deploy)
- Alarm: `{ProjectPrefix}-api-errors` — trigger with the helper script:

```bash
source ../.stack.env
python trigger_alarm.py
```

This sends malformed JSON to `/classify` so Lambda errors appear on the dashboard and can fire the alarm.

## Governance deliverable

Document in your assignment:

- Fields logged vs forbidden
- Retention (DynamoDB on-demand; add TTL in production)
- Human-in-the-loop triggers (`human_review` route, agent `requires_approval`)
