# ADR-M05-01 — Cloud Audit Trail Approach

**Status:** Accepted (reference)  
**Context:** NorthStar needs enterprise audit evidence for cloud API activity.

## Decision

Use provider-native CloudTrail (or equivalent) into a central audit account/bucket; do not build a custom audit ingestion platform in year one.

## Alternatives

1. Build custom event pipeline — high cost, slow
2. Buy SIEM-only without trail baseline — gaps in cloud API evidence
3. Per-account trails with no centralization — weak investigations

## Consequences

+ Fast compliance evidence baseline  
+ Lower build burden  
− Vendor/provider coupling (accept with exit notes)  
− Need bucket policy and access governance
