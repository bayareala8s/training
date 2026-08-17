# Week 4 Labs — Step Functions

## Start execution

```bash
SM_ARN=$(aws cloudformation describe-stacks --stack-name ba-la8s-ai-yourname-course-labs \
  --query "Stacks[0].Outputs[?OutputKey=='StateMachineArn'].OutputValue" --output text)

aws stepfunctions start-execution --state-machine-arn "$SM_ARN" \
  --input '{"text":"API 503 after deployment","correlation_id":"lab4-happy"}'
```

## Lab 4.2 — Failure simulation

```bash
aws stepfunctions start-execution --state-machine-arn "$SM_ARN" \
  --input '{"text":"test","correlation_id":"lab4-fail","simulate_validation_failure":true}'
```

Document retry/fallback behavior in your retry report.
