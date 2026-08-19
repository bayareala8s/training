window.EIA_CHALLENGES = [
  {
    id: "c01",
    module: "1",
    title: "25 GB customer upload",
    scenario: "A customer uploads a 25 GB file. Should you:",
    options: [
      { id: "A", label: "Send it through API Gateway" },
      { id: "B", label: "Upload directly to object storage" },
      { id: "C", label: "Put the entire payload in SQS" },
      { id: "D", label: "Store it in DynamoDB" },
    ],
    correct: "B",
    explanation:
      "Direct-to-object-storage (claim-check) is the only option that respects payload and timeout physics. API Gateway, SQS, and DynamoDB have hard size limits and are the wrong style. Explain: init API + presigned multipart upload + FileReceived event + status API.",
  },
  {
    id: "c02",
    module: "1",
    title: "Account balances in 300 ms",
    scenario: "Retail banking needs account balances returned within 300 ms. Style?",
    options: [
      { id: "A", label: "Nightly file extract to the mobile app" },
      { id: "B", label: "Synchronous API against the ledger (or an SLO-fresh replica)" },
      { id: "C", label: "SQS command the app waits on" },
      { id: "D", label: "Event projection with unbounded lag" },
    ],
    correct: "B",
    explanation:
      "Tight latency + request/reply + small payload = API. Files and queues cannot meet 300 ms in-band. A projection is only acceptable if its lag SLO fits inside the remaining budget—usually it does not for money.",
  },
  {
    id: "c03",
    module: "1",
    title: "Address change to twenty systems",
    scenario: "Twenty downstream systems must know whenever a customer changes address.",
    options: [
      { id: "A", label: "Customer service HTTP-calls all twenty" },
      { id: "B", label: "One nightly CSV to a shared inbox" },
      { id: "C", label: "AddressChanged event with independent consumers, plus a SoR read API" },
      { id: "D", label: "A new ESB map per consumer as the default" },
    ],
    correct: "C",
    explanation:
      "Fan-out of a fact is an event. Keep GET on the system of record for the call center. Point-to-point and per-consumer ESB maps recreate coupling. A nightly file is too slow unless NFRs actually say T+1.",
  },
  {
    id: "c04",
    module: "1",
    title: "20 GB × 50 organizations nightly",
    scenario: "Exchange 20 GB datasets with 50 external organizations every night.",
    options: [
      { id: "A", label: "REST POST of the dataset through a gateway" },
      { id: "B", label: "File landing zone (SFTP and/or S3) plus catalog, validation, and processing" },
      { id: "C", label: "One SQS message containing the dataset" },
      { id: "D", label: "An AI agent that copies files with admin credentials" },
    ],
    correct: "B",
    explanation:
      "Bulk + partner heterogeneity + nightly rhythm = file style. Events notify that a file arrived; they do not carry 20 GB. Agents may query status, not become the transport.",
  },
  {
    id: "c05",
    module: "2",
    title: "Mobile timeout on POST /orders",
    scenario: "The client retries POST /orders after a timeout. What prevents double charge?",
    options: [
      { id: "A", label: "Using PUT because PUT is magic" },
      { id: "B", label: "Idempotency-Key stored with request hash" },
      { id: "C", label: "Shorter timeouts so retries never happen" },
      { id: "D", label: "FIFO SQS in front of the API" },
    ],
    correct: "B",
    explanation:
      "HTTP retries are at-least-once. Idempotency keys (and conflict on same key/different body) make effectively-once creates. FIFO does not belong in front of a user API as the primary fix.",
  },
  {
    id: "c06",
    module: "2",
    title: "API Gateway as ESB",
    scenario: "A team wants mapping templates on the gateway to orchestrate five systems.",
    options: [
      { id: "A", label: "Approve—gateways should own domain orchestration" },
      { id: "B", label: "Reject—gateway is a policy edge; use a visible workflow or domain services" },
      { id: "C", label: "Put the maps in VTL for performance" },
      { id: "D", label: "Only allow it for 50 GB files" },
    ],
    correct: "B",
    explanation:
      "Gateways terminate HTTP, auth, and throttle. Orchestration in mapping templates recreates an untestable ESB. Use Step Functions or domain services.",
  },
  {
    id: "c07",
    module: "3",
    title: "Exactly-once SQS",
    scenario: "A vendor promises exactly-once payments because FIFO is on. You should:",
    options: [
      { id: "A", label: "Accept and skip consumer idempotency" },
      { id: "B", label: "Require idempotent handlers; FIFO is not a ledger" },
      { id: "C", label: "Disable FIFO to be safe" },
      { id: "D", label: "Move payments to SNS" },
    ],
    correct: "B",
    explanation:
      "FIFO helps per-group order and short producer dedupe windows. Side effects in other systems still see at-least-once. Effectively-once is an application invariant.",
  },
  {
    id: "c08",
    module: "3",
    title: "Visibility timeout vs function timeout",
    scenario: "Lambda timeout 70s, SQS visibility 30s. Predict the incident.",
    options: [
      { id: "A", label: "Messages disappear forever" },
      { id: "B", label: "Concurrent duplicate processing as the message reappears mid-work" },
      { id: "C", label: "API Gateway 429s" },
      { id: "D", label: "KMS key rotation" },
    ],
    correct: "B",
    explanation:
      "When work exceeds visibility, another consumer receives the same message. Set visibility > function timeout, or extend visibility / shrink work.",
  },
  {
    id: "c09",
    module: "4",
    title: "Kill one subscriber",
    scenario: "Notification consumer is down. Checkout still publishes OrderCreated. Inventory should:",
    options: [
      { id: "A", label: "Also stop, because pub/sub is a transaction" },
      { id: "B", label: "Continue independently from its own queue" },
      { id: "C", label: "Call checkout to replay" },
      { id: "D", label: "Write to the notification table to help" },
    ],
    correct: "B",
    explanation:
      "Fan-out with a queue per subscriber isolates failure. Publisher success is broker accept, not email sent.",
  },
  {
    id: "c10",
    module: "5",
    title: "Command disguised as an event",
    scenario: "A payload named SendEmail is published on the enterprise bus for anyone to handle.",
    options: [
      { id: "A", label: "Correct EDA" },
      { id: "B", label: "This is a command; put it on a worker queue (or an API) with an owner" },
      { id: "C", label: "Put it in DynamoDB streams only" },
      { id: "D", label: "Name it EmailSent even if the email did not send" },
    ],
    correct: "B",
    explanation:
      "Past-tense facts fan out. Commands have a responsible worker. EmailSent is the fact after success.",
  },
  {
    id: "c11",
    module: "5",
    title: "Replay six months of OrderCreated",
    scenario: "Analytics is stale. Someone replays the archive to the production bus with all subscribers live.",
    options: [
      { id: "A", label: "Fine if EventBridge supports replay" },
      { id: "B", label: "Dangerous—inventory and email will re-act unless targeted and idempotent" },
      { id: "C", label: "Always safe because events are facts" },
      { id: "D", label: "Use SQS FIFO instead" },
    ],
    correct: "B",
    explanation:
      "Replay is an operation: bound time, filter types, target consumers that can no-op or that are projections, and audit who replayed.",
  },
  {
    id: "c12",
    module: "6",
    title: "Ack at SFTP receive",
    scenario: "Partner wants an ACK as soon as SFTP PUT succeeds, labeled POSTED.",
    options: [
      { id: "A", label: "Agree—bytes landed equals settlement" },
      { id: "B", label: "Ack RECEIVED only; POSTED after validation and ledger posting" },
      { id: "C", label: "Never ack files" },
      { id: "D", label: "Ack via the AI agent in natural language only" },
    ],
    correct: "B",
    explanation:
      "Protocol success is not business success. Separate received / validated / posted states in the catalog.",
  },
  {
    id: "c13",
    module: "6",
    title: "Duplicate payroll file",
    scenario: "Partner retries the same settlement file after a timeout. First file already posted.",
    options: [
      { id: "A", label: "Post again to be safe" },
      { id: "B", label: "Detect duplicate (file id/hash) and reject without double-post" },
      { id: "C", label: "Overwrite the S3 key and hope" },
      { id: "D", label: "Delete the catalog" },
    ],
    correct: "B",
    explanation:
      "File idempotency is checksum + business file identity + catalog status. Retries must not double-post.",
  },
  {
    id: "c14",
    module: "7",
    title: "Init API waits for processing",
    scenario: "POST /uploads hashes the 10 GB file inside the request and returns 200 when done.",
    options: [
      { id: "A", label: "Good user experience" },
      { id: "B", label: "Wrong—202 + status; processing is async after direct upload" },
      { id: "C", label: "Use DynamoDB to hold the 10 GB during the wait" },
      { id: "D", label: "Increase API Gateway timeout to 15 minutes" },
    ],
    correct: "B",
    explanation:
      "Init is a control-plane call. Bytes go to S3. Status is polled or pushed. Gateway timeouts cannot be the architecture.",
  },
  {
    id: "c15",
    module: "8",
    title: "New digital product on the ESB",
    scenario: "A new mobile feature needs a mapping. Bus lead time is six weeks. Default?",
    options: [
      { id: "A", label: "Add the map; the bus is the enterprise standard" },
      { id: "B", label: "Prefer a published API/event on a golden path; exception ADR if the bus is required" },
      { id: "C", label: "Skip integration" },
      { id: "D", label: "Give the mobile app the database credentials" },
    ],
    correct: "B",
    explanation:
      "Modernization policy: new work defaults off the bus. Exceptions are documented. Credentials to the ledger are not an interface.",
  },
  {
    id: "c16",
    module: "9",
    title: "Strangler order",
    scenario: "Pick the first flow to strangler off the ESB.",
    options: [
      { id: "A", label: "Card settlement (highest importance)" },
      { id: "B", label: "A high-change, lower-blast flow (e.g. marketing notification)" },
      { id: "C", label: "All flows in one weekend" },
      { id: "D", label: "Whatever the vendor demo uses" },
    ],
    correct: "B",
    explanation:
      "Learn on lower ruin-probability flows. Settlement is a later wave with dual-run and reconcilers. Big bang is not plan A.",
  },
  {
    id: "c17",
    module: "10",
    title: "Payment ok, inventory fail",
    scenario: "In an order saga, payment succeeded and inventory reservation failed. Next?",
    options: [
      { id: "A", label: "Ignore—eventual consistency will fix money" },
      { id: "B", label: "Idempotent compensating transaction (release/refund per policy) and a visible state" },
      { id: "C", label: "Delete the order row only" },
      { id: "D", label: "Replay OrderCreated to everyone" },
    ],
    correct: "B",
    explanation:
      "Saga + compensating transaction. Refund/void must be idempotent. Replay of Created would make it worse. Product policy chooses reserve-then-pay vs pay-then-reserve.",
  },
  {
    id: "c18",
    module: "11",
    title: "Retry multiplication",
    scenario: "SDK, Lambda, and SQS each retry 3 times on the same 500. Risk?",
    options: [
      { id: "A", label: "None, retries are independent" },
      { id: "B", label: "Worst-case attempt explosion and duplicate side effects" },
      { id: "C", label: "Exactly-once is guaranteed" },
      { id: "D", label: "Only cost increases" },
    ],
    correct: "B",
    explanation:
      "Overlapping retry layers multiply. Count them, add jitter, idempotency, and prefer one primary retry layer.",
  },
  {
    id: "c19",
    module: "12",
    title: "Agent IAM",
    scenario: "Proposed role for the ops agent: dynamodb:Scan on * and s3:GetObject on *.",
    options: [
      { id: "A", label: "Efficient for support" },
      { id: "B", label: "Unacceptable—tools must be least-privilege catalog/status APIs" },
      { id: "C", label: "OK if the model is aligned" },
      { id: "D", label: "OK in a VPC" },
    ],
    correct: "B",
    explanation:
      "LLM/agent must not have unrestricted data-plane access. VPC and alignment are not substitutes for least privilege.",
  },
  {
    id: "c20",
    module: "12",
    title: "Public write prefix",
    scenario: "S3 prefix uploads/ is public-write so browsers can PUT large files.",
    options: [
      { id: "A", label: "Standard large-file pattern" },
      { id: "B", label: "Unsafe—use time-boxed presigned URLs to server-chosen keys" },
      { id: "C", label: "Fine with SSE-S3" },
      { id: "D", label: "Fine if Transfer Family is also on" },
    ],
    correct: "B",
    explanation:
      "Public write is a malware hotel. Presign specific keys. Encryption does not stop untrusted writes.",
  },
  {
    id: "c21",
    module: "13",
    title: "99.9% API success, zero settlements",
    scenario: "Gateway 202 rate is excellent. Posted payments are zero. What is missing?",
    options: [
      { id: "A", label: "More load balancers" },
      { id: "B", label: "Business metrics at ledger completion, not only edge 202s" },
      { id: "C", label: "FIFO" },
      { id: "D", label: "A bigger ESB" },
    ],
    correct: "B",
    explanation:
      "Technical success ≠ business success. Instrument PaymentsPosted / FilesQuarantined. Agents must not answer from gateway 200s alone.",
  },
  {
    id: "c22",
    module: "14",
    title: "Stakeholder: we need Kafka",
    scenario: "First sentence of the ADR problem statement should:",
    options: [
      { id: "A", label: "Name Kafka as the requirement" },
      { id: "B", label: "State the business/NFR need without naming the product" },
      { id: "C", label: "List Terraform resources" },
      { id: "D", label: "Reject the project" },
    ],
    correct: "B",
    explanation:
      "Start with the requirement. Kafka may be an option later. Technology-first ADRs fail this course.",
  },
  {
    id: "c23",
    module: "15",
    title: "Did Customer ABC’s file arrive?",
    scenario: "The ops agent should:",
    options: [
      { id: "A", label: "Query production PostgreSQL" },
      { id: "B", label: "Call a governed file-status tool that reads the catalog" },
      { id: "C", label: "SSH to Transfer Family" },
      { id: "D", label: "List all S3 objects into the prompt" },
    ],
    correct: "B",
    explanation:
      "User → agent → tool → integration catalog. No direct DB, no payload dump, no SSH.",
  },
  {
    id: "c24",
    module: "15",
    title: "Reprocess via agent",
    scenario: "User asks the agent to reprocess a failed payment file.",
    options: [
      { id: "A", label: "Agent posts immediately using admin role" },
      { id: "B", label: "Agent requests action; human approval; workflow reprocesses; audit event" },
      { id: "C", label: "Agent edits S3 until it works" },
      { id: "D", label: "Reads can wait; writes never need approval if logged" },
    ],
    correct: "B",
    explanation:
      "HITL for writes. Durable approval, idempotent reprocess, audit. Reads may execute when authorized.",
  },
  {
    id: "c25",
    module: "15",
    title: "MCP server with SQL tool",
    scenario: "A popular MCP server exposes raw SQL against prod. Adopt?",
    options: [
      { id: "A", label: "Yes—MCP is an enterprise standard so it is safe" },
      { id: "B", label: "No—discovery ≠ authorization; SQL-on-prod is the forbidden architecture" },
      { id: "C", label: "Yes if we rename SQL to “query tool”" },
      { id: "D", label: "Yes inside a container" },
    ],
    correct: "B",
    explanation:
      "MCP is a protocol. Governance still forbids unrestricted production queries. Allow-list servers that wrap your APIs.",
  },
];
