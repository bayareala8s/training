# Integration Pattern Selection Matrix

**Organization:** NorthStar Financial Services (fictional)  
**Initiative / interface:**  

---

## Context

| Field | Value |
| ----- | ----- |
| Producers | |
| Consumers | |
| Data classification | |
| Volume / velocity | |
| Latency need | |
| Consistency need | |
| Reliability need | |
| Team ownership model | |

---

## Pattern options

Score fit 1–5 (higher = better fit).

| Pattern | Latency | Coupling | Volume | Reliability | Security | Cost | Ops complexity | Fit | Notes |
| ------- | ------: | -------: | -----: | ----------: | -------: | ---: | -------------: | --: | ----- |
| Synchronous API | | | | | | | | | |
| Async events | | | | | | | | | |
| Queue / competing consumers | | | | | | | | | |
| Streaming | | | | | | | | | |
| File / SFTP batch | | | | | | | | | |
| Batch ETL | | | | | | | | | |
| Shared database *(discouraged)* | | | | | | | | | |
| Manual process | | | | | | | | | |

---

## Selected pattern(s)

**Primary:**  
**Secondary / backup:**  

## Rationale (trade-offs)

## Failure handling

| Failure mode | Detection | Response | Customer impact |
| ------------ | --------- | -------- | --------------- |
| | | | |

## ADR reference

ADR-___
