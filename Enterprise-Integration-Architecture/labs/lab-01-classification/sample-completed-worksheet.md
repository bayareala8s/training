**Instructor sample only.** Do not submit this file as Lab 1. Copy `worksheet.md` and write your own rationales.

# Lab 1 sample completed worksheet (instructor smoke test)

Copy to `submissions/lab-01/worksheet.md` only if you are verifying the validator—not as a student submission.

## Item 1

- **Style:** API
- **Characteristics:** 300 ms, small payload, one consumer (mobile), HTTPS, confidential balances
- **Architecture (one paragraph):** Request/reply to the system of record with caching only if freshness NFRs allow.
- **AWS example (last):** API Gateway HTTP API + Lambda + DynamoDB
- **Rejected options:** Queue (too slow/async), file (batch), ESB hop (extra latency)
- **Data class:** Confidential
- **Rationale (≥ 40 words):** The caller is blocked on the answer and the NFR is a hard latency budget. A message or event cannot return the current balance inside the request. An ESB SOAP hop adds mapping latency the mobile channel cannot afford. Start with the NFR, then pick the API style, then a service.

## Item 2

- **Style:** Message
- **Characteristics:** minutes of outage tolerance, command, one posting engine, at-least-once with idempotency
- **Architecture (one paragraph):** Durable command queue in front of the ledger poster; ACK at the edge is not posted.
- **AWS example (last):** SQS + Lambda + DLQ
- **Rejected options:** Sync API only (drops work when poster is down)
- **Data class:** Restricted
- **Rationale (≥ 40 words):** Work must survive a twenty-minute posting outage. That is a command buffer, not a request/reply. Idempotency keys prevent double-post on retry. Events would fan out; this flow has one destination that must not lose instructions.

## Item 3

- **Style:** Event
- **Characteristics:** many consumers, no shared transaction, address payload, independent failure
- **Architecture (one paragraph):** CustomerChanged event; each downstream projects what it needs.
- **AWS example (last):** EventBridge or SNS
- **Rejected options:** Twenty point-to-point APIs
- **Data class:** Confidential
- **Rationale (≥ 40 words):** Twenty systems must learn independently. Coupling them through one sync API or one ESB map creates a blast radius. An event lets consumers fail in isolation. Pub/sub is the style; the broker is a later technology choice.

## Item 4

- **Style:** File
- **Characteristics:** 20 GB, nightly, fifty recipients, high integrity
- **Architecture (one paragraph):** Landing zone, checksums, catalog, fan-out copies or signed URLs—not a 20 GB POST.
- **AWS example (last):** S3 + inventory/notifications
- **Rejected options:** REST POST of the extract
- **Data class:** Confidential
- **Rationale (≥ 40 words):** The payload size and schedule dominate. APIs time out; queues have message size limits. A file landing zone with checksums and a catalog is the honest style. Transfer Family is a cost decision after the file architecture exists.

## Item 5

- **Style:** File / SFTP adapter
- **Characteristics:** partner constraint, mixed names, no API budget this year
- **Architecture (one paragraph):** Keep SFTP at the edge; normalize in the landing zone; do not pretend they speak REST.
- **AWS example (last):** S3 landing; Transfer Family only if the hourly cost is accepted
- **Rejected options:** Force an API rewrite this year
- **Data class:** Confidential
- **Rationale (≥ 40 words):** The partner will not fund an API. Architecture follows the constraint: an SFTP edge into the same inbound pipeline as other files. Leave Transfer Family offline until a named partner needs it, because ONLINE hours dominate cost.

## Item 6

- **Style:** AI agent + status API
- **Characteristics:** natural language, read-only first, governed tools
- **Architecture (one paragraph):** Planner may call GetFileStatus; it must not query the warehouse.
- **AWS example (last):** Lambda tools over HTTP APIs
- **Rejected options:** LLM with a database user
- **Data class:** Confidential
- **Rationale (≥ 40 words):** The question is operational and conversational, but the answer must come from an authorized status API. An agent is a channel, not a data store. Tool allow-lists and audit matter more than the model brand.

## Item 7

- **Style:** AI agent + HITL workflow
- **Characteristics:** write path, approval, audit
- **Architecture (one paragraph):** RequestReprocess creates PENDING; a human approval API executes.
- **AWS example (last):** approvals table + POST /approve
- **Rejected options:** Agent UpdateItem on catalog
- **Data class:** Restricted
- **Rationale (≥ 40 words):** Reprocess is a write with financial impact. The agent may request; it may not execute. Human-in-the-loop plus an audit event is the NFR. This is why LLM-to-database fails the course even when it “works” in a demo.

## Item 8

- **Style:** ESB / adapter
- **Characteristics:** certified ISO map, rare change, MQ residue
- **Architecture (one paragraph):** Keep the adapter; strangler everything else; dual-run before any cutover.
- **AWS example (last):** Existing MQ; do not lift-and-shift to EventBridge this year
- **Rejected options:** Rewrite ISO onto a new bus in one quarter
- **Data class:** Restricted
- **Rationale (≥ 40 words):** Certified scheme connections are residue. Changing the map for fashion violates reliability and cost NFRs. An adapter is an honest keep. New flows must not be added to that bus.

## Item 9

- **Style:** API
- **Characteristics:** user-visible validation, small JSON, sync
- **Architecture (one paragraph):** POST /orders with schema errors in the same response.
- **AWS example (last):** HTTP API + Lambda
- **Rejected options:** Fire-and-forget queue for the checkout click
- **Data class:** Confidential
- **Rationale (≥ 40 words):** The website must show validation errors immediately. That is request/reply. A queue can post the order later but cannot return 422s to the browser. Idempotency keys cover retries when the client times out.

## Item 10

- **Style:** Event / pub-sub
- **Characteristics:** independent consumers, isolation, no shared commit
- **Architecture (one paragraph):** OrderCreated fans out to inventory, email, analytics.
- **AWS example (last):** SNS or EventBridge
- **Rejected options:** Checkout HTTP-calls all three inside one transaction
- **Data class:** Internal
- **Rationale (≥ 40 words):** After acceptance, downstreams should not share the checkout transaction. Email outages must not fail card authorization UX. Fan-out is the style; pick SNS vs EventBridge after filtering and schema needs are scored.

## Item 11

- **Style:** File / claim-check
- **Characteristics:** 10–50 GB, browser, authenticated user
- **Architecture (one paragraph):** Init job, presigned PUT to object storage, process asynchronously, GET status.
- **AWS example (last):** S3 presigned URL + Lambda
- **Rejected options:** Multipart through API Gateway
- **Data class:** Internal
- **Rationale (≥ 40 words):** API Gateways are the wrong pipe for tens of gigabytes. Claim-check: the API hands a pointer; the bytes go to the file store; status is polled or pushed. That is file architecture, not “a bigger REST POST.”

## Item 12

- **Style:** Message
- **Characteristics:** 90 s scoring, user must not block, command
- **Architecture (one paragraph):** Enqueue fraud score; account opening continues with a pending state.
- **AWS example (last):** SQS
- **Rejected options:** Sync call in the opening API
- **Data class:** Restricted
- **Rationale (≥ 40 words):** Ninety seconds exceeds any reasonable HTTP client timeout for onboarding. Treat fraud scoring as a command with a later event. Blocking the API couples a slow dependency to a user-visible flow.

## Item 13

- **Style:** Domain API / event (not more ESB)
- **Characteristics:** political canonical model, delivery date
- **Architecture (one paragraph):** Publish a bounded context API; do not wait for Customer v42 on the bus.
- **AWS example (last):** HTTP API owned by the domain
- **Rejected options:** Another ESB canonical attribute
- **Data class:** Confidential
- **Rationale (≥ 40 words):** The committee is the constraint. Adding maps extends lead time. A domain API or event for the mobile-needed subset is the strangler move. ESB modernization is keep/change/retire, not a bigger canonical XML.

## Item 14

- **Style:** Message / queue buffer
- **Characteristics:** planned downtime, commands must wait, checkout must not
- **Architecture (one paragraph):** Queue absorbs Sunday; warehouse drains Monday; idempotent commands.
- **AWS example (last):** SQS with DLQ
- **Rejected options:** Fail checkout when warehouse is down
- **Data class:** Internal
- **Rationale (≥ 40 words):** Planned unavailability is what queues are for. Events still need a durable buffer if the consumer is off. Do not make the customer wait on a plant network. Drain and replay with idempotency on Monday.

## Item 15

- **Style:** HITL store + audit event
- **Characteristics:** who approved, what replayed, non-repudiation
- **Architecture (one paragraph):** Approval record plus an audit event; replay is a governed write.
- **AWS example (last):** DynamoDB approvals + EventBridge audit
- **Rejected options:** Chat message “looks like ops said yes”
- **Data class:** Restricted
- **Rationale (≥ 40 words):** Security asked for an audit trail of who approved a poison replay. That is not a vibe from a chatbot. It is a stored approval, an identity, and an event others can SIEM. Agents request; humans approve; systems emit audit.
