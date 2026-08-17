# Option A — AI Operations / Incident Triage Platform

**Status:** Implemented · API + Step Functions + audit + severity scoring + notify stub

**Problem:** Reduce time-to-triage for production incidents.

## Implemented flow

1. Summarize incident (Bedrock)
2. Classify category
3. Route to team + confidence gate
4. Score severity (`critical` / `high` / `medium` / `needs_review`) with explainable reasons
5. Create ticket stub with owner
6. Notification stub for high/critical (optional SNS via `CAPSTONE_NOTIFY_TOPIC_ARN`)
7. Persist to DynamoDB + write audit event

## API

```bash
curl -sS -X POST "$API_ENDPOINT/capstone/incident" \
  -H "Content-Type: application/json" \
  -d @week08/samples/incident_happy.json | python3 -m json.tool
```

## Demo (full)

```bash
chmod +x week08/option_a_incident_triage/demo.sh
./week08/option_a_incident_triage/demo.sh
```

Samples: `incident_happy.json`, `incident_critical.json`, `incident_ambiguous.json`

## Step Functions

```bash
aws stepfunctions start-execution \
  --state-machine-arn "$CAPSTONE_INCIDENT_SM_ARN" \
  --input '{"text":"API 503 in production","correlation_id":"demo-a-1"}'
```

States: **Classify → Validate → EnrichTriage → Persist**

## Portfolio extensions

- EventBridge rule for CloudWatch alarms
- Real SNS/PagerDuty topic ARN
- Human queue UI for `needs_review`
