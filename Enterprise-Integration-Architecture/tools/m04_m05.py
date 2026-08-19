#!/usr/bin/env python3
"""Modules 4–5 lesson records (pub/sub + events)."""

from __future__ import annotations

def L(id, title, module, objectives, scenario, why, when, when_not, how_pattern, how_aws, decision, **kw):
    d = dict(
        id=id, title=title, module=module, objectives=objectives, scenario=scenario,
        why=why, when=when, when_not=when_not, how_pattern=how_pattern, how_aws=how_aws,
        decision=decision,
    )
    d.update(kw)
    return d

M04_MOD = "04 — Pub/Sub Architecture"

M04 = [
    L("4.1", "Publisher and Subscriber", M04_MOD,
      ["Define pub/sub as senders of facts/notifications that do not enumerate consumers.",
       "Contrast with competing consumers on a queue.",
       "Name ownership of the topic versus ownership of each subscription."],
      "Harbor’s checkout should not import inventory, email, and analytics SDKs. It should publish OrderCreated. "
      "Those teams subscribe independently. That is the organizational point of pub/sub.",
      "Publish/subscribe exists so a producer can announce without knowing who cares. The publisher owns the **contract "
      "of the notification**. Each subscriber owns its reaction, failure handling, and scale. This is how you avoid "
      "N-point-to-point callbacks from checkout to twenty systems.",
      ["Multiple independent reactions to one fact or notification.",
       "Producer must not change when a new consumer appears.",
       "Consumers have different SLAs (email can lag; inventory cannot)."],
      ["A single worker must do the work (queue/command).",
       "The producer needs an in-band result from all consumers (use saga/orchestration, not naive pub/sub).",
       "You are hiding a command inside an “event” that only one team is allowed to process."],
      "Publisher emits to a topic. Broker fans out. Each subscriber gets a copy (possibly filtered). Failures are isolated "
      "if each subscriber has its own queue. The publisher’s success is “the broker accepted the publish,” not “email was sent.”",
      "Amazon SNS topics plus SQS subscriptions is the classic AWS mapping. EventBridge is often a better event bus when "
      "you need content-based routing across domains (Module 5). Lab 4 uses SNS → three SQS queues to make isolation tangible.",
      "If analytics is down, should checkout fail? What does that imply about coupling?",
      diagram="flowchart LR\n  Pub[Publisher] --> T[Topic]\n  T --> S1[Sub inventory]\n  T --> S2[Sub notify]\n  T --> S3[Sub analytics]",
      tradeoffs=[("Pub/sub", "Independent consumers", "Harder end-to-end transactional guarantees"),
                 ("Direct calls", "Easy to see the chain", "Checkout owns everyone else's outages")],
      checks=[{"q": "What is the publisher responsible for after a successful publish?",
               "a": "The durability of the notification into the broker per the topic’s SLA—not the success of every subscriber’s business logic."}],
      anti_patterns=["Publisher waiting synchronously for all subscribers.", "One shared queue for all subscriber types."],
      architect_note="If adding a consumer requires a deploy of the producer, you do not have pub/sub."),
    L("4.2", "Fan-out", M04_MOD,
      ["Design fan-out so one slow subscriber cannot block others.",
       "Give each subscriber its own buffer.",
       "Measure fan-out as a reliability graph, not a slide."],
      "SNS delivered to three HTTPS endpoints. The email endpoint hung. Depending on configuration, you can stall or "
      "retry in ways that surprise you. Fan-out to queues is the enterprise default for a reason.",
      "Fan-out copies a message to N destinations. The architecture question is isolation: separate retry, DLQ, and "
      "scaling per destination. Fan-out to Lambda directly is convenient; fan-out to SQS in front of Lambda is usually "
      "safer for back-pressure and replay.",
      ["N independent consumers.",
       "When you would otherwise loop HTTP calls in the producer."],
      ["Fan-out of huge payloads (claim-check first).",
       "Fan-out of secrets to destinations that should not see them (filter/minimize)."],
      "Pattern: topic → per-consumer queue → consumer. Apply filters so finance does not get marketing events. "
      "Encrypt. Do not put PII on a topic with 40 casual subscribers.",
      "SNS fan-out to SQS, Lambda, HTTP, email. Prefer SQS subscriptions for operational control. Lab 4 implements three queues.",
      "Draw blast radius if the topic policy allows any account to subscribe.",
      diagram="flowchart TB\n  E[OrderCreated] --> SNS[SNS topic]\n  SNS --> Q1[Inventory Q]\n  SNS --> Q2[Notification Q]\n  SNS --> Q3[Analytics Q]",
      tradeoffs=[("Queue per subscriber", "Isolation and replay", "More Terraform"),
                 ("HTTP fan-out", "Fewer resources", "Coupled timeouts and weaker replay")],
      checks=[{"q": "Why is a queue per subscriber the default enterprise fan-out?",
               "a": "Independent retry, DLQ, scaling, and the publisher does not wait on HTTP timeouts."}],
      anti_patterns=["All consumers sharing one queue and peeking by type.", "Unfiltered PII blast."],
      architect_note="Fan-out is a security decision as much as a scaling decision."),
    L("4.3", "Topics", M04_MOD,
      ["Name topics after business facts, not after teams.",
       "Avoid a single mega-topic and a million micro-topics.",
       "Set retention, encryption, and access at topic grain."],
      "A company created topic-john-test and topic-orders-final-v3-real. Nobody could find the contract. Topics are APIs.",
      "A topic is a named channel with a contract. Good names: order-created, payment-authorized. Ownership sits with "
      "the domain that owns the fact. Access policies are part of the design: who may publish, who may subscribe. "
      "Too coarse (everything on bus) recreates an ESB. Too fine (topic per field change) recreates a mesh.",
      ["Stable business facts with multiple consumers.",
       "When you need a permission boundary around a class of notifications."],
      ["A topic per environment hacked into the name instead of using accounts/prefixes.",
       "Reusing a topic for commands and facts."],
      "Treat the topic like an API product: schema, version, owners, SLOs. Document payload (or claim-check pointer). "
      "Prefer a modest set of domain topics. Use filters for subtypes.",
      "SNS topic resource policies, KMS, FIFO topics when you truly need ordered fan-out. Event buses (Module 5) may "
      "replace many topics when routing is content-based and cross-domain.",
      "Should OrderCreated and OrderCancelled share a topic with a type field, or be two topics? What happens to IAM and filters?",
      diagram="flowchart LR\n  D[Orders domain] --> T[orders.events topic]\n  T --> F[Filters]\n  F --> C[Consumers]",
      tradeoffs=[("Few topics + filters", "Simpler IAM surface", "Noisy if filters are sloppy"),
                 ("Many topics", "Clear contracts", "Topic sprawl and missed subscribers")],
      checks=[{"q": "Who should own the OrderCreated topic?",
               "a": "The orders domain that is the source of truth for that fact—not the integration team by default."}],
      anti_patterns=["topic-final-final.", "Publishers from any team without review."],
      architect_note="Put topic contracts in git next to OpenAPI. They are the same kind of artifact."),
    L("4.4", "Filtering", M04_MOD,
      ["Use server-side filters to reduce fan-out cost and data exposure.",
       "Keep filters coarse enough to be understandable.",
       "Do not replace schema versioning with filter spaghetti."],
      "Analytics only needs orders over $500. If you deliver everything, you pay to move and store noise—and you widen "
      "the PII blast radius.",
      "Filters are predicates on notification attributes or payload (depending on the broker). They are a performance "
      "and security control. They are a poor substitute for splitting truly different facts. Over-filtering makes "
      "debugging “why didn’t I get it?” expensive.",
      ["Subscribers that need a subset of a stable fact.",
       "Reducing sensitive fields by not subscribing to events that contain them—better: minimize the payload."],
      ["Encoding the entire business process in filter syntax.",
       "Filters so specific they break when a new optional field appears."],
      "Put stable attributes in metadata (orderType, country, amountBand) so filters do not parse opaque blobs. "
      "Test filters as code. Document them for each subscription.",
      "SNS subscription filter policies; EventBridge pattern matching (richer). Lab 4 can start without filters, then "
      "add an attribute so analytics ignores test orders.",
      "A filter drops “TEST” orders. A partner uses customer name TESTCO. What is the defect class?",
      diagram="flowchart LR\n  T[Topic] --> F{Filter}\n  F -->|match| Q[Subscriber queue]\n  F -->|no| X[Drop]",
      tradeoffs=[("Filters", "Less noise, less data", "Invisible delivery failures"),
                 ("Separate topics", "Obvious contracts", "More artifacts")],
      checks=[{"q": "Are filters a security boundary?",
               "a": "They reduce exposure but are not a substitute for authorization and payload minimization. Misconfiguration can still leak."}],
      anti_patterns=["Parsing JSON in filters when attributes would do.", "No metric for filtered-out count."],
      architect_note="Always log a sample of unmatched events in non-prod when bringing a new subscriber live."),
    L("4.5", "Independent Consumers", M04_MOD,
      ["Prove that consumer failure is isolated.",
       "Give each consumer its own idempotency and DLQ.",
       "Avoid shared databases as a secret coupling between “independent” consumers."],
      "Inventory and email “independently” subscribed but both wrote the same DynamoDB row with overlapping keys. "
      "Email outages locked inventory. Independence is a property of failure and of data ownership.",
      "Independence means: own queue, own compute, own datastore for *their* projection, own alerts, own deploy. "
      "They may read the same event contract. They may not share a lock table casually. If a saga requires a joint "
      "outcome, that is a different pattern (Module 10)—do not fake it with pub/sub plus a shared row.",
      ["Truly different reasons to react.",
       "Different scale and languages."],
      ["When a single atomic business transaction must span them (use orchestration or a two-phase design)."],
      "In Lab 4, kill the notification consumer and show inventory still drains. That experiment is the lesson. "
      "Then inspect data ownership: three tables or three prefixes, not one OrdersWorking table everyone fights over.",
      "Three Lambdas, three SQS, optionally three DynamoDB tables. IAM so notify cannot write inventory items. "
      "This is also a security lesson.",
      "If analytics needs a complete copy of the order, should it call the order API or consume the event payload? What is the coupling?",
      diagram="flowchart TB\n  T[Topic] --> I[Inventory stack]\n  T --> N[Notify stack]\n  T --> A[Analytics stack]\n  I --> DI[(inv table)]\n  N --> DN[(notify table)]\n  A --> DA[(analytics table)]",
      tradeoffs=[("Isolated stacks", "Failure isolation", "Duplicated projection logic"),
                 ("Shared working table", "Less duplication", "Coupled outages and schema fights")],
      checks=[{"q": "What experiment proves independence?",
               "a": "Stop one consumer; others continue; publisher still succeeds; DLQ only for the stopped path if messages expire retries."}],
      anti_patterns=["Shared IAM role for all consumers.", "A “misc” Lambda that does all three jobs."],
      architect_note="Lab 4’s grading should include the kill-one-consumer test."),
    L("4.6", "Pub/Sub vs Event Bus vs Queue", M04_MOD,
      ["Choose SNS-style topics vs EventBridge-style buses vs SQS without cargo-culting.",
       "Use a decision table the rest of the course will reuse.",
       "Explain why all three might appear in one platform."],
      "A platform team mandated EventBridge for everything, including “resize this image” commands. Commands sat on a "
      "bus with 70 rules. Operators could not see work. The tool was not wrong; the style was.",
      "Queues carry commands to competing workers. Topics fan out notifications to known subscription types. Event buses "
      "route facts using content and metadata across many domains with rules. A mature platform uses all three. The "
      "decision framework from Module 1 still applies: command vs fact, cardinality, routing need, ops skill.",
      ["Queue: one work type, back-pressure.",
       "Topic: simple fan-out of a named notification.",
       "Bus: many event types, content-based routing, archive/replay (Module 5)."],
      ["Bus for pixel-resize jobs.",
       "Queue for 40 unrelated teams peeking.",
       "Topic for a single consumer (probably just a queue)."],
      "Write the table in the ADR. It is acceptable to publish an event to a bus *and* have a rule send a command to SQS. "
      "That composition is normal: fact then work.",
      "SNS + SQS (Lab 4), EventBridge + SQS/Lambda (Lab 5), SQS alone (Lab 3). Step Functions when you need orchestration "
      "rather than notification.",
      "OrderCreated should notify three teams and also start a payment command. Sketch topic vs bus vs queue for each hop.",
      diagram="flowchart TB\n  Fact[Fact] --> Bus[Event bus / topic]\n  Bus --> Cmd[Command queues]\n  Cmd --> W[Workers]",
      tradeoffs=[("All on one bus", "Unified routing", "Ops fog and style confusion"),
                 ("Right tool per hop", "Clarity", "More moving parts to document")],
      checks=[{"q": "Can a rule on an event bus create a command?",
               "a": "Yes. That is a common composition. The event remains a fact; the SQS message is the command."}],
      anti_patterns=["One AWS service mandated enterprise-wide.", "Renaming commands to events to satisfy a standard."],
      architect_note="You will reuse this comparison in Module 14’s challenges. Memorize the table, not the ARNs."),
]

M05_MOD = "05 — Event-Driven Architecture"

M05 = [
    L("5.1", "Events vs Messages", M05_MOD,
      ["Define an event as an immutable fact about something that happened.",
       "Define a message/command as an intent that someone must do.",
       "Spot “pseudo-events” that are commands in disguise."],
      "PaymentAuthorized is a fact. AuthorizePayment is a command. Teams that name both “events” cannot design retries. "
      "Facts can fan out. Commands need a responsible worker and often a DLQ.",
      "Events describe the past: OrderCreated, FileReceived. They should not say “please do.” Commands describe the "
      "future work: ProcessFile, ChargeCard. Mixing them causes duplicate side effects (everyone “helps”) or lost work "
      "(nobody is on the hook). Event-driven architecture is not “we use EventBridge.” It is facts + independent reactions "
      "+ eventual consistency you can live with.",
      ["Facts with multiple reactions.",
       "Auditability of what happened.",
       "Decoupling producers from consumer set."],
      ["User is waiting for a single result in 200 ms (API).",
       "Exactly one worker must perform a side effect (queue).",
       "You need a distributed transaction illusion without a saga design."],
      "Name events in past tense. Include event ID, time, producer, entity IDs, version, and payload or claim-check. "
      "Do not include “nextHopUrl” that only one consumer understands. If you need a next hop, that is orchestration.",
      "EventBridge events vs SQS messages vs SNS notifications. The AWS object is not the definition. Lab 5 uses facts: "
      "OrderCreated, PaymentAuthorized, InventoryReserved, OrderCompleted.",
      "Is “SendEmail” an event? What would the fact be instead, and who commands the email worker?",
      diagram="flowchart LR\n  Cmd[Command: do X] --> Q[Queue]\n  Fact[Event: X happened] --> Bus[Bus / topic]",
      tradeoffs=[("Facts", "Many consumers, audit", "Eventual consistency"),
                 ("Commands", "Clear ownership of work", "Producer knows a worker type")],
      checks=[{"q": "How should events be named?",
               "a": "Past-tense business facts (PaymentAuthorized), not verbs (DoPayment)."}],
      anti_patterns=["Event payload that is actually a stored procedure call.", "Consumers that ignore the fact and always call back the producer."],
      architect_note="If you can replace the event with POST /pleaseDoThis, it was a command."),
    L("5.2", "Event Producers", M05_MOD,
      ["Place production of events at the system of record after a successful state change.",
       "Avoid dual-write between DB and bus.",
       "Include identity of the producer in the envelope."],
      "Checkout published OrderCreated before the order row committed. Payments authorized a ghost order. Producer "
      "timing is a correctness problem.",
      "The producer is the authority for the fact. It should emit **after** the state change is durable, or atomically "
      "via outbox/change-data-capture. Producers must not lie (publishing success on a failed write). They must version "
      "the schema. They should not wait for consumers.",
      ["Domain services that own entities.",
       "File landing zones that own “file received” facts.",
       "Integration layers that translate partner facts into internal facts (anti-corruption)."],
      ["Random Lambdas that guess domain state.",
       "Consumers re-publishing the same fact under a new name without adding meaning (noise)."],
      "Outbox, CDC, or “write event store first” are the honest options. Include occurredAt from the domain, not only "
      "the broker timestamp. Sign or at least hash if auditors will care (payments, health).",
      "DynamoDB Streams / EventBridge Pipes, outbox relay, or application publish after transact-write. Lab 5 may start "
      "with a simple put-event for learning, then the architecture questions must call out the dual-write risk.",
      "If the producer emits twice because of a retry, what must every consumer already be?",
      diagram="flowchart LR\n  Dom[Domain write] --> Out[Outbox]\n  Out --> Bus[Event bus]\n  Dom --> DB[(System of record)]",
      tradeoffs=[("After-commit emit", "No ghost facts", "Tiny window if process dies—mitigate with outbox"),
                 ("Before-commit emit", "Faster notify", "Ghost facts and reconciliation pain")],
      checks=[{"q": "Who may produce OrderCreated?",
               "a": "The orders system of record (or a dedicated anti-corruption publisher it owns)—not every service that heard a rumor."}],
      anti_patterns=["Consumers producing “OrderCreated” again when they finish their slice.", "Unsigned payment facts on a public bus."],
      architect_note="Producer quality determines whether EDA is an audit log or a rumor mill."),
    L("5.3", "Event Consumers", M05_MOD,
      ["Build consumers as idempotent projectors or command issuers.",
       "Keep consumer state in a store they own.",
       "Handle late, duplicate, and out-of-order events."],
      "Inventory reserved twice on duplicate OrderCreated. Stock went negative. The consumer was a tutorial Lambda.",
      "Consumers translate facts into *their* world: update a projection, send a command, start a workflow. They must "
      "tolerate at-least-once facts. They should not become mini-systems-of-record for someone else’s entity. If they "
      "need a command performed, they send a message to a queue they own or call an API with an idempotency key.",
      ["Projections, notifications, triggering workflows, analytics.",
       "When independent reaction is actually desired."],
      ["When they must lock the producer’s database.",
       "When they need a synchronous answer back to the original user without a status model."],
      "Idempotency store keyed by event ID. Version checks on the entity. Timeouts and DLQ. Observability with the "
      "correlation ID from the producer. Consumer-specific alarms (lag, DLQ).",
      "EventBridge targets: Lambda, SQS, Step Functions. Prefer SQS in front of Lambda for retry control. Lab 5 wires "
      "payment, inventory, and notification consumers.",
      "PaymentAuthorized arrives twice. What row in DynamoDB proves you will not authorize twice?",
      diagram="flowchart LR\n  Bus[Bus] --> SQS[Consumer queue]\n  SQS --> Fn[Idempotent handler]\n  Fn --> P[(Projection)]",
      tradeoffs=[("Queue in front of consumer", "Control and replay", "More latency"),
                 ("Direct Lambda target", "Simple", "Retry semantics harder to reason")],
      checks=[{"q": "What is a projector?",
               "a": "A consumer that updates a read model from events without claiming to be the system of record for the producer’s entity."}],
      anti_patterns=["Dropping event IDs.", "Calling a non-idempotent payment API from the consumer."],
      architect_note="Every Lab 5 consumer is a chance to practice Lesson 2.11 and 3.4 again. That repetition is intentional."),
    L("5.4", "Event Schemas", M05_MOD,
      ["Publish a schema registry-like contract for events.",
       "Include envelope vs data, compatibility rules, and examples.",
       "Reject unschematized “JSON blobs” on enterprise buses."],
      "Two teams used customerId vs customer_id vs custNo. Analytics joined garbage. Schema is the event’s OpenAPI.",
      "Event schemas need an envelope (id, type, source, time, specversion) and a data payload. Compatibility: additive "
      "optional fields are usually OK; renaming is a new version. Examples of invalid events should exist. Producers "
      "validate before put; consumers validate before effect (defense in depth).",
      ["Any shared bus.",
       "Any event that crosses team or compliance boundaries."],
      ["Pair-programming a one-off internal ping.",
       "Using schema to encode the entire workflow (keep facts small)."],
      "Adopt a convention (CloudEvents-like) so tracing and routing work. Version the type name (order.created.v1). "
      "Store schemas in git. CI: producer tests emit valid examples; consumer tests parse them.",
      "EventBridge schema registry can discover schemas; do not rely on discovery as governance. Prefer explicit schemas "
      "in the repo (sample-data/events). Lab 5 events are defined as JSON Schema in sample-data.",
      "You need a new field paymentMethod. v1 additive or v2? Who does not deploy in time?",
      diagram="flowchart TB\n  Env[Envelope: id type source time correlation] --> Data[Data: business payload]\n  Data --> Sch[JSON Schema]",
      tradeoffs=[("Strict registry", "Safe evolution", "Process overhead"),
                 ("Free JSON", "Fast", "Unjoinable data and poison events")],
      checks=[{"q": "Why separate envelope from data?",
               "a": "Routing, tracing, and replay tools should not need to understand every domain payload."}],
      anti_patterns=["PII in the envelope for convenience.", "Type names that include environment (OrderCreated-dev)."],
      architect_note="sample-data/events is part of the contract, not a convenience folder."),
    L("5.5", "EventBridge", M05_MOD,
      ["Describe an event bus as a routed fact backbone, not a queue.",
       "Use custom buses per domain or enterprise with a plan.",
       "Know archive/replay as a first-class capability."],
      "A default bus with 200 rules became unreadable. A custom bus per domain with a clearly owned integration bus "
      "for cross-domain facts is an architecture, not a setting.",
      "EventBridge is AWS’s event router: buses, rules (patterns), targets, archives, pipes. Conceptually it is closer "
      "to an enterprise event backbone than to SQS. You still need the styles: facts on the bus, commands on queues. "
      "Bus strategy (one vs many) is an ADR: blast radius, IAM, noise, cost of rules.",
      ["Cross-service facts inside the estate.",
       "SaaS/AWS service events you want to route (with care).",
       "When you need archive and replay."],
      ["High-volume clickstream where a stream processor is cheaper.",
       "Large payloads (claim-check to S3).",
       "Partner SFTP (file style) pretending to be events without a landing fact."],
      "Choose bus topology. Put IAM so only Orders can put OrderCreated. Use rules to fan out to SQS. Enable archive "
      "on the bus that holds legally relevant facts. Watch cost of custom events and CloudWatch.",
      "Amazon EventBridge custom bus, rules, targets, archive, schema registry, pipes from SQS/DynamoDB. Lab 5 builds "
      "the happy path. Module 11 will break it.",
      "One enterprise bus vs bus-per-domain: what IAM and operational problem does each solve?",
      diagram="flowchart LR\n  P[Producers] --> B[Custom event bus]\n  B --> R[Rules]\n  R --> T1[SQS payment]\n  R --> T2[SQS inventory]\n  R --> T3[Lambda notify]\n  B --> Arch[Archive]",
      tradeoffs=[("Single bus", "Easy discovery", "Noisy neighbors and IAM sprawl"),
                 ("Domain buses", "Clear ownership", "Cross-domain bridging to design")],
      checks=[{"q": "Is EventBridge a replacement for SQS?",
               "a": "No. It routes facts. SQS still buffers commands and isolates consumers."}],
      anti_patterns=["Putting 256 KB payloads on the bus as a habit.", "Everyone PutEvents to the default bus with star IAM."],
      architect_note="If you cannot name who may PutEvents of type X, the bus is a rumor mill (again)."),
    L("5.6", "Event Routing", M05_MOD,
      ["Route on type and metadata first, payload second.",
       "Keep rule sets reviewable.",
       "Avoid routing that implements a hidden workflow engine."],
      "Rules chained events into a de facto saga: Created → if paid then → if reserved then → email. Nobody could "
      "see the process. Routing should deliver facts, not hide a state machine.",
      "Routing matches predicates to targets. Good routing: type == OrderCreated → inventory queue. Bad routing: "
      "nested conditions that encode “if this then that unless Thursday.” When the path is a business process with "
      "compensations, use an orchestrator (Step Functions / saga) that is visible.",
      ["Dispatch facts to the right consumers.",
       "Environment splitting (careful with prod data).",
       "Content-based subsetting (country, product line)."],
      ["As a substitute for an orchestrator.",
       "Hundreds of overlapping rules with no test."],
      "Keep a routing table in git. Test patterns with sample events. Limit who can create rules in production. "
      "Prefer one rule per consumer need, named with the consumer’s name.",
      "EventBridge rules and event patterns. Resource policies on buses. Lab 5 rules are explicit and listed in Terraform.",
      "A rule sends OrderCreated to payments only if amount > 0. Where should that invariant actually live?",
      diagram="flowchart TB\n  E[Event] --> P{Pattern}\n  P -->|type OrderCreated| Inv[Inventory]\n  P -->|type PaymentAuthorized| Pay[Payment projector]\n  P -->|else| None[No target]",
      tradeoffs=[("Declarative rules", "Fast wiring", "Opaque processes if overused"),
                 ("Orchestrator", "Visible process", "More coupling to the workflow definition")],
      checks=[{"q": "When do you stop adding rules and start a state machine?",
               "a": "When order of steps, compensation, and time-outs are business-critical rather than independent reactions."}],
      anti_patterns=["Copy-paste rules with tiny differences and no tests.", "Rules that call a Lambda which then does all routing anyway."],
      architect_note="Capstone 2 will tempt you to hide the saga in rules. Do not."),
    L("5.7", "Content-Based Filtering", M05_MOD,
      ["Filter on declared attributes you control.",
       "Minimize sensitive content in matchable fields.",
       "Test filters as part of CI."],
      "A healthcare bus filtered “if payload contains HIV.” That created a secondary disclosure risk in logs and rules. "
      "Content-based routing must respect data classification.",
      "Content-based filtering is powerful and dangerous. Match on coarse, non-sensitive attributes (eventType, orgId, "
      "severity). Do not put diagnoses, PANs, or secrets in rule patterns. For healthcare (Capstone 3), filters follow "
      "minimum necessary—often you route a pointer, not the clinical payload.",
      ["High-volume buses where most consumers need a slice.",
       "Multi-tenant events with a tenant key."],
      ["Matching on raw clinical or payment PAN fields.",
       "Filters that require scanning huge payloads (cost and latency)."],
      "Promote keys into the envelope. Encrypt the payload. Authorize consumers independently of filters. Review rules "
      "in security design.",
      "EventBridge pattern matching on detail-type and detail fields. Prefer detail-type. Lab 5 can route on event type "
      "only; challenges may add amount bands with care.",
      "Should a rule match on patient.mrn? What is the least-privilege alternative?",
      diagram="flowchart LR\n  E[Event] --> F[Match type + tenant]\n  F --> T[Target]\n  Pay[Sensitive payload] -.->|not in pattern| X[Encrypted data / claim-check]",
      tradeoffs=[("Rich payload matching", "Flexible", "Leakage and brittleness"),
                 ("Envelope matching", "Safer, faster", "Must design attributes up front")],
      checks=[{"q": "Why promote tenantId to the envelope?",
               "a": "So routing and IAM can use it without parsing or logging sensitive payload fields."}],
      anti_patterns=["Logging the entire matching event including PHI.", "Filters as access control."],
      architect_note="Security architects should review event patterns the same way they review API paths."),
    L("5.8", "Event Replay", M05_MOD,
      ["Replay as a deliberate, auditable operation.",
       "Make consumers idempotent before you replay.",
       "Bound the time range and event types."],
      "Someone replayed six months of OrderCreated to “fix analytics.” Inventory reserved again. Replay without "
      "consumer readiness is a self-inflicted incident.",
      "Replay exists because consumers bug, projections corrupt, or new consumers need history. It requires an archive, "
      "a time window, type filters, a target, and a communication plan. Consumers must be effectively-once. Some events "
      "must never be naively replayed (physical shipments already sent)—those consumers must no-op on old facts or "
      "you replay only to analytics.",
      ["Rebuilding a projection.",
       "After a poison-bug fix.",
       "Onboarding a new read model."],
      ["As a substitute for a DLQ inspect/fix of a handful of poisons.",
       "Against consumers with non-idempotent real-world side effects."],
      "Archive facts. Document replay runbooks. Use a replay flag or separate replay bus if side-effecting consumers "
      "must be excluded. Record who replayed what in the audit log.",
      "EventBridge archive + replay. S3 + redrive for files. SQS replay from DLQ is different (commands). Do not confuse them.",
      "You need analytics to catch up but inventory must not. How do you target the replay?",
      diagram="flowchart LR\n  Arch[Archive] --> Rep[Replay job]\n  Rep --> Bus[Bus]\n  Bus --> A[Analytics consumer]\n  Bus -.->|not targeted| I[Inventory]",
      tradeoffs=[("Archive everything", "Forensic power", "Cost and retention law"),
                 ("No archive", "Cheap", "Cannot rebuild or investigate")],
      checks=[{"q": "What must be true before a production replay?",
               "a": "Idempotent target consumers, a bounded query, an owner, and a plan for side-effecting subscribers."}],
      anti_patterns=["Replay to the production topic with all subscribers live “to keep it real.”", "No audit of who replayed."],
      architect_note="Capstones require a replay story. Write it before go-live, not during the outage."),
    L("5.9", "Eventual Consistency", M05_MOD,
      ["Set user and operator expectations for lag.",
       "Design read APIs that do not lie about freshness.",
       "Use compensating UX (refresh, status) instead of distributed locks by default."],
      "Customer paid; UI still showed “unpaid” for 8 seconds. Support refunded. The architecture was correct; the UX "
      "and support playbook were not. Eventual consistency is a product problem.",
      "EDA accepts that views catch up. Architects must quantify lag SLOs, show status resources, and train support. "
      "Read-after-write can be preserved on the producer’s API (read your own write) while other systems lag. Do not "
      "promise a globally consistent dashboard across 12 projections without a design.",
      ["Independent projections.",
       "Cross-enterprise facts.",
       "Any fan-out."],
      ["Hard legal constraints that two ledgers must match in the same commit (then you need a different pattern or a single ledger)."],
      "Producer reads remain consistent. Downstream UIs display “updating…” or poll status. Business metrics track lag. "
      "Reconciliation jobs catch permanent divergence. Sagas handle business-level undo (Module 10).",
      "DynamoDB reads on the orders table vs a projection table. CloudWatch lag metrics from consumer checkpoints. "
      "Do not use strongly consistent reads on a projection that is fed asynchronously and then claim the platform is strongly consistent.",
      "The call center agent asks whether the address update “went through.” Which API is allowed to answer authoritatively?",
      diagram="sequenceDiagram\n  participant U as User\n  participant O as Orders API\n  participant P as Projection\n  U->>O: Update address\n  O-->>U: 200 write-your-own\n  O->>P: AddressChanged\n  Note over P: lag\n  U->>P: stale read possible",
      tradeoffs=[("EDA", "Availability and decoupling", "Lag and reconciliation"),
                 ("Single sync write to all", "Simple reads", "Coupled outages")],
      checks=[{"q": "Where is read-your-write most easily guaranteed?",
               "a": "On the system of record’s own API after its durable write—not on a random projection."}],
      anti_patterns=["Support tools reading the slowest projection.", "No lag SLO."],
      architect_note="Write the support one-liner: “Source of truth is X; Y updates within N seconds.”"),
    L("5.10", "Event Versioning", M05_MOD,
      ["Version event types explicitly.",
       "Run dual publishers only with a plan.",
       "Keep consumers tolerant of additive fields."],
      "v1 had amount as string; v2 as number. Half the consumers broke on a Tuesday. Versioning without dual-run is a flag day.",
      "Event types are contracts. Additive optional fields: bump a minor if you even number them; consumers ignore unknowns. "
      "Semantic change: new type (order.created.v2) or a new field with a new meaning plus a period of dual publish. "
      "Remove fields only after consumers are gone (metrics!).",
      ["Any event that already has a second consumer.",
       "When you must change types or required fields."],
      ["Version in the payload only with no type change and no docs.",
       "Infinite dual publish."],
      "Include version in the type name or envelope. Consumers subscribe to the versions they support. Producers dual-publish "
      "during migration. Measure v1 vs v2. Stop v1 with an ADR.",
      "EventBridge detail-type can carry the version. Schema registry versions. Lab 5 starts at v1; an architecture "
      "challenge asks you to add a field without breaking notification.",
      "You must change currency from implied USD to an explicit code. Is that compatible? How do you dual-run?",
      diagram="flowchart LR\n  P[Producer] --> V1[order.created.v1]\n  P --> V2[order.created.v2]\n  V1 --> C1[Old consumers]\n  V2 --> C2[New consumers]\n  V2 --> C1b[Tolerant consumers]",
      tradeoffs=[("Explicit types per version", "Clear routing", "More rules"),
                 ("Single type + hidden meaning change", "Looks simple", "Silent corruption")],
      checks=[{"q": "What metric tells you you can sunset v1?",
               "a": "Zero healthy consumers (or zero traffic) on v1 plus a written owner sign-off."}],
      anti_patterns=["Reuse of event IDs across versions with different meanings.", "No example payloads for v2."],
      architect_note="Event versioning is API versioning with more spectators. Be stricter, not looser."),
]
