# Cost Estimate — Lab 06 Integration Platform

**Module:** 06 — Integration, Application, and Data Architecture  
**Case study:** NorthStar Financial Services (fictional)  
**Region assumed:** us-east-1  
**Target:** **~<$5** when cleaned up the same day

---

## Cost drivers (typical 2–4 hour lab)

| Service | Usage assumption | Approx. cost |
| ------- | ---------------- | ------------ |
| API Gateway HTTP API | <1,000 requests | <$0.01 |
| Lambda (5 functions) | <2,000 invocations total | Free tier / pennies |
| EventBridge custom bus | <500 events | <$0.01 |
| SQS + DLQ | <500 messages | <$0.01 |
| Step Functions | <50 transitions | <$0.01 |
| DynamoDB on-demand | Light lab traffic | <$0.05 |
| S3 partner bucket | Few small files, 3-day lifecycle | <$0.01 |
| SNS email | Few notifications | Free / negligible |
| CloudWatch Logs | 7-day retention | <$0.20 |
| **Transfer Family (NOT deployed)** | Continuous endpoint | **$0.30/hour+ — do not enable for class** |

## Cost control decisions taught in lab

1. **S3 simulation** replaces Transfer Family for partner SFTP
2. Serverless eventing instead of always-on brokers
3. Short log retention and force-destroy buckets
4. Same-day cleanup script

## Residual risk

| Risk | Mitigation |
| ---- | ---------- |
| SNS subscription left active | Destroy removes topic; confirm email |
| Objects blocking S3 delete | Cleanup script empties bucket first |
| Forgotten state machine executions | Destroy deletes state machine |

## Cleanup verification

After destroy, confirm no residual resources tagged `Project=BayLearn` + `Module=06`.
