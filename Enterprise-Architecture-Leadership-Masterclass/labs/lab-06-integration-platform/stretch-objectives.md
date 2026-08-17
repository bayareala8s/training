# Stretch Objectives — Lab 06

Complete only after core deliverables and cleanup. Optional for distinction; not required to pass.

1. **DLQ alarm:** Add (or design) a CloudWatch alarm on DLQ `ApproximateNumberOfMessagesVisible > 0` with SNS notify; document threshold rationale.
2. **AccountCreated consumer note:** One page listing which production domains should subscribe, what they must not mutate, and replay expectations.
3. **MFT decision brief:** One-pager justifying **when** NorthStar should buy Transfer Family or an MFT platform versus S3 landing + partner connectivity (cost, compliance, protocol, ops skills).
4. **Event schema versioning:** Propose versioning rules for `PaymentSubmitted` (compat policy, deprecation window, registry vs wiki).
5. **Isolation sketch:** Propose how partner-file bursts are isolated from payment workers (queues, concurrency, priority) without a second enterprise ESB.
