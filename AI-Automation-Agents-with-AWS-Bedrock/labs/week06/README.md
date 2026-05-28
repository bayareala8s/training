# Week 6 Labs — Observability & governance

## Audit query

After running APIs or Lambdas:

```bash
export AUDIT_TABLE_NAME=ba-la8s-ai-yourname-audit
python week06/query_audit.py <correlation-id-from-api-response>
```

## Dashboard & alarm

- Open CloudWatch → Dashboards → `{ProjectPrefix}-ai-ops`
- Alarm: `{ProjectPrefix}-api-errors` — trigger by sending malformed requests to the API

## Governance deliverable

Document in your assignment:

- Fields logged vs forbidden
- Retention (DynamoDB on-demand; add TTL in production)
- Human-in-the-loop triggers (`human_review` route, agent `requires_approval`)
