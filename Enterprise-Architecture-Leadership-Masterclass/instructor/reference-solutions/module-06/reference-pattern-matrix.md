# Reference Pattern Matrix (NorthStar fictional)

| Interface | Primary | Secondary | Notes |
| --------- | ------- | --------- | ----- |
| Account lookup/create | Sync API | Event on create | User latency |
| Payment submitted | Event → queue | Status API read | Buffer + DLQ |
| Partner files | File landing | Event on arrival | S3 sim in lab |
| Regulatory batch | Workflow orchestration | Manual | Step Functions |
