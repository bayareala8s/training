# Week 3 Labs — Structured outputs & routing

## Local tests (no AWS)

```bash
cd labs && source .venv/bin/activate
pytest tests/ -v
```

## AWS (after deploy)

```bash
PREFIX=ba-la8s-ai-yourname
aws lambda invoke --function-name ${PREFIX}-classify \
  --payload '{"text":"Suspicious login from unknown IP","correlation_id":"lab3-1"}' \
  --cli-binary-format raw-in-base64-out /tmp/c.json && cat /tmp/c.json

aws lambda invoke --function-name ${PREFIX}-route \
  --payload '{"text":"I was charged twice on my invoice","correlation_id":"lab3-2","label":"billing"}' \
  --cli-binary-format raw-in-base64-out /tmp/r.json && cat /tmp/r.json
```

Expect: rules-based route for billing keywords; JSON validation in response.
