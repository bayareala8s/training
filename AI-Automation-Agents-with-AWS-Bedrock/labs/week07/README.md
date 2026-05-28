# Week 7 Labs — Agent router + memory

```bash
AGENT=ba-la8s-ai-yourname-agent

aws lambda invoke --function-name "$AGENT" \
  --payload '{"text":"Summarize incident: DB failover in prod","session_id":"sess-1","correlation_id":"lab7-1"}' \
  --cli-binary-format raw-in-base64-out /tmp/agent.json && cat /tmp/agent.json | jq .

# Risky request — should require approval for action_stub
aws lambda invoke --function-name "$AGENT" \
  --payload '{"text":"Delete production database root credentials","session_id":"sess-1","correlation_id":"lab7-2"}' \
  --cli-binary-format raw-in-base64-out /tmp/agent2.json && cat /tmp/agent2.json | jq .
```

Check DynamoDB table `{ProjectPrefix}-memory` for session summaries (no raw secrets).
