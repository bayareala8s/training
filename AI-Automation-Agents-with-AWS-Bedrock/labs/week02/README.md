# Week 2 Labs

## Lab 2.1 (AWS Lambda)

Deploy the course stack (see `labs/README.md`), then:

```bash
aws lambda invoke \
  --function-name <ProjectPrefix>-week2-invoke \
  --payload '{"prompt":"Hello from Lambda","correlation_id":"lab2-test-1"}' \
  --cli-binary-format raw-in-base64-out \
  /tmp/week2-out.json && cat /tmp/week2-out.json
```

Check CloudWatch Logs for correlation ID and latency (no full prompt logged in audit).

## Lab 2.2 (local)

```bash
python week02/prompt_eval.py
```

Review `week02/prompt_eval_results.json` and write your decision note.
