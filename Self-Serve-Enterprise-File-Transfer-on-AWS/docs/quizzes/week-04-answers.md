# Answer key — Week 4 quiz

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | Orchestration centralizes control flow and history; choreography is decentralized event reactions. |
| 2 | **B** | Standard supports long runs and detailed history for enterprise audit. |
| 3 | **B** | Retry transient infra errors; not bad business data. |
| 4 | **B** | Catch routes to NotifyFailure/recovery paths. |
| 5 | **B** | Express &lt; ~5 min and lighter history—poor fit for long regulated flows. |
| 6 | **B** | Originate at API/job submit; propagate for ops correlation. |
| 7 | **B** | Map iterates over collections (manifest files). |
| 8 | **B** | Workflow-level failure metric catches orchestration failures. |
| 9 | **B** | DynamoDB + conditional start prevents duplicate executions. |
| 10 | **B** | Business validation outcome drives Choice, not transient errors. |
| 11 | **Sample:** **Retry** transient/service errors; **Catch** terminal/business failures to recovery/notify. | |
| 12 | **Sample:** Provides a durable record of state transitions, inputs/outputs (where configured), and failure points for auditors and on-call. | |
