# Option C — Multi-step Approval Workflow

**Status:** Implemented · API request/decide + DynamoDB state + Step Functions + notify stub

**Problem:** Gate risky automation behind human approval.

## Implemented flow

1. Evaluate risk (keywords + optional `risk_level`)
2. Low/medium → auto-execute stub
3. High → `pending_approval` in DynamoDB + notify stub
4. `POST /capstone/approval/decide` → approve (execute) or deny
5. Audit both request and decide

## API

```bash
# High risk → pending
curl -sS -X POST "$API_ENDPOINT/capstone/approval/request" \
  -H "Content-Type: application/json" \
  -d @week08/samples/approval_high_risk.json | python3 -m json.tool

# Decide
curl -sS -X POST "$API_ENDPOINT/capstone/approval/decide" \
  -H "Content-Type: application/json" \
  -d '{"approval_id":"APR-XXXXXXXXXX","decision":"approve","correlation_id":"capstone-approval-high","approver_id":"instructor"}'
```

## Demo

```bash
./week08/option_c_approval_workflow/demo.sh
```

Samples: `approval_high_risk.json`, `approval_low_risk.json`

## Step Functions

Choice branch: pending vs auto-approved (`CAPSTONE_APPROVAL_SM_ARN`)

## Portfolio extensions

- SNS email to approvers
- WaitForTaskToken human callback
- Change-management ticket ID on execute
