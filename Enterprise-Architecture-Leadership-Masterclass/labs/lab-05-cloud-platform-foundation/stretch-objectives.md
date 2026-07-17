# Stretch Objectives — Lab 05

Complete only after core validation and if time/budget allow.

1. **Disable CloudTrail via tfvars** (`enable_cloudtrail=false`), re-apply, and write a ½-page note on audit trade-offs.
2. **Optional AWS Config** (`enable_config=true`) for S3+Lambda only — **cost warning** — then immediately destroy and document cost risk.
3. Add a second SSM parameter for `data-classification=internal` and have Lambda return it in `/health`.
4. Propose (do not deploy) an SCP-style guardrail list for NorthStar sandboxes.
