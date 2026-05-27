# Answer key — Week 3 quiz

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | Distributed events may duplicate; design idempotent handlers. |
| 2 | **B** | Idempotency table deduplicates event/business keys. |
| 3 | **B** | Quarantine preserves evidence; operators can investigate. |
| 4 | **B** | Heavy transforms belong in workflows/batch, not tiny validators. |
| 5 | **B** | Business key survives duplicate notifications and re-uploads. |
| 6 | **B** | EventBridge enables flexible routing and multi-consumer patterns. |
| 7 | **B** | Lambda role needs KMS decrypt on CMK-encrypted objects. |
| 8 | **B** | Correlate logs to jobs/workflows; never log secrets. |
| 9 | **B** | Duplicate processing is a classic MFT failure mode. |
| 10 | **B** | Prefix filters limit blast radius and cost. |
| 11 | **Sample:** The eventing system may deliver the same event more than once; retries and partner re-uploads also duplicate work without idempotency. | |
| 12 | **Sample:** Max size 100 MB; allowed extensions `.csv`, `.json`, `.xml`; reject 0-byte (any two from Lab 3). | |
