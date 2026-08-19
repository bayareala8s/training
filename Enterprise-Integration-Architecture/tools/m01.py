#!/usr/bin/env python3
"""Modules 1–5 lesson records."""

from __future__ import annotations

M01 = [
    {
        "id": "1.1",
        "title": "What Is Enterprise Integration?",
        "module": "01 — Enterprise Integration Fundamentals",
        "objectives": [
            "Define enterprise integration as the governed exchange of data and commands across ownership boundaries.",
            "Name the typical systems that sit on either side of an integration: systems of record, SaaS, partners, data platforms, legacy, and cloud.",
            "Draw an integration boundary and explain who owns availability, schema, and security on each side.",
        ],
        "scenario": (
            "Northbridge Bank runs a core banking system of record, a cloud CRM, a partner-bank settlement network, "
            "a data lake, a 1990s loan origination mainframe, and a mobile app. The CIO asks you to “connect everything.” "
            "That request is not an architecture. Enterprise integration starts by naming systems, ownership, and the "
            "boundary where a message, file, API call, or event actually crosses from one team’s control to another."
        ),
        "why": (
            "Enterprises do not fail because they lack HTTP clients. They fail because customer, payment, inventory, "
            "and partner data live in different applications with different owners, SLAs, and regulatory constraints. "
            "Integration is the discipline of moving meaning—not just bytes—across those boundaries without creating "
            "an unmaintainable mesh of hidden dependencies.\n\n"
            "A **system of record** is the authoritative store for a business entity (the ledger for an account balance). "
            "A **system of engagement** (mobile, portal, chatbot) should not become a second system of record. "
            "SaaS products you do not operate still sit inside your architecture the moment you depend on their APIs. "
            "Partners are other enterprises: they will not adopt your internal event bus. Data platforms consume "
            "integration output; they are rarely the operational path for a payment. Legacy applications often expose "
            "files or MQ rather than REST. Cloud systems add identity, network, and account boundaries on top of all of this."
        ),
        "when": [
            "You must exchange data or trigger work across applications, teams, companies, or cloud accounts.",
            "A business process spans more than one system of record.",
            "A partner, regulator, or SaaS vendor owns part of the workflow.",
            "You are defining an integration inventory before selecting technology.",
        ],
        "when_not": [
            "The work is a local function call inside a single service and bounded context.",
            "You are only replicating data for analytics with no operational contract (that is still integration, but a different style—batch/CDC—do not pretend it is a real-time API).",
            "You have not identified the owner of the contract. “Someone will write a Lambda” is not a boundary.",
        ],
        "nfr": [
            "Volume and payload size",
            "Latency (synchronous human wait vs overnight batch)",
            "Reliability and whether loss is acceptable",
            "Security classification and who may see the payload",
            "Ownership of schema and versioning",
        ],
        "how_pattern": (
            "Start with an **integration inventory**: source, destination, data subject, direction, frequency, payload "
            "shape, sensitivity, and failure impact. Draw the **trust boundary**: identity, network, and data classification "
            "change at that line. Then classify the interaction as command (do this), query (tell me this), event "
            "(this happened), or batch (here is a set).\n\n"
            "Only after the inventory is honest do you choose API, message, event, file, adapter, or agent. "
            "The inventory is the architect’s primary artifact in week one of any engagement."
        ),
        "how_aws": (
            "AWS does not change the inventory. API Gateway might terminate an API boundary. SQS might hold a command. "
            "EventBridge might route a fact. S3 and Transfer Family might land a file. IAM and KMS implement the trust "
            "boundary. None of those services tell you whether the mobile app should call core banking synchronously "
            "for a 20 GB settlement file—that is still a bad idea on any cloud."
        ),
        "diagram": """flowchart LR
  subgraph Engagement
    Mobile[Mobile / Portal]
    Agent[Ops Agent]
  end
  subgraph Integration[Integration boundary]
    API[APIs]
    Q[Queues]
    Ev[Events]
    F[Files]
  end
  subgraph Record
    Core[System of record]
    SaaS[SaaS]
    Legacy[Legacy]
    Partner[Partner]
    Lake[Data platform]
  end
  Mobile --> API
  Agent --> API
  API --> Core
  Q --> Core
  Ev --> SaaS
  F --> Partner
  Ev --> Lake
  Legacy --> F""",
        "tradeoffs": [
            ("Clarity", "Named boundaries make ownership and SLAs explicit", "Inventory work feels slow to delivery teams"),
            ("Coupling", "Contracts localize change", "Poor contracts recreate point-to-point chaos on new tech"),
            ("Cost", "Right-sized style avoids overbuilding", "Wrong style (API for bulk files) creates outage and spend"),
        ],
        "decision": (
            "Northbridge wants the mobile app, CRM, settlement partners, and the data lake to “see the same customer.” "
            "Is that one integration or four? Which are queries, which are events, which are files? Who owns the customer identifier?"
        ),
        "checks": [
            {
                "q": "What is an integration boundary?",
                "a": "The line where control of identity, schema, availability, or data classification changes—typically between applications, teams, accounts, or organizations.",
            },
            {
                "q": "Why is a data lake rarely the system of record for a payment?",
                "a": "Operational correctness, latency, and legal authority live in the payment/ledger system. The lake is a consumer of facts, not the place you authorize a transfer.",
            },
        ],
        "anti_patterns": [
            "Calling every HTTP call “the architecture.”",
            "Letting SaaS become an accidental system of record because it was easy to write to.",
            "Skipping partner constraints (“they will just use our Kafka”).",
        ],
        "architect_note": (
            "If you cannot list the systems of record and the owners, you are not designing an integration platform. "
            "You are decorating a mystery."
        ),
    },
    {
        "id": "1.2",
        "title": "Why Enterprise Integration Is Difficult",
        "module": "01 — Enterprise Integration Fundamentals",
        "objectives": [
            "Explain why protocol, schema, availability, security, network, legacy, and organizational ownership make integration hard.",
            "Separate technical difficulty from organizational difficulty.",
            "Map a failure (timeout, poison message, duplicate file) to a missing contract rather than a missing service.",
        ],
        "scenario": (
            "Harbor Retail’s “order” means different things in web checkout (intent), warehouse (pickable unit), "
            "finance (recognized revenue), and a 3PL partner (carton). The warehouse is down for two hours every Sunday. "
            "The 3PL only accepts SFTP CSV. Security will not allow the warehouse VLAN to call the public API Gateway. "
            "Four teams own four definitions. This is why integration is difficult—not because SQS is hard to click in a console."
        ),
        "why": (
            "**Different protocols** (HTTPS, SFTP, MQ, EDI, FHIR, ISO 20022) exist because industries and decades of "
            "vendors standardized differently. **Different schemas** exist because bounded contexts optimize for different "
            "jobs. **Different availability** exists because a storefront’s 99.99% target is not a batch mainframe’s "
            "weekend window. **Security boundaries** exist because PCI, HIPAA, and partner contracts forbid flattening "
            "all data into one account. **Network boundaries** (VPC, private link, partner VPN, air-gapped plants) exist "
            "because not everything should be on the public internet. **Legacy technologies** persist because they still "
            "settle money or ship product. **Organizational ownership** means no single team can change both sides of a contract.\n\n"
            "Architects who ignore ownership produce beautiful diagrams that nobody can deploy."
        ),
        "when": [
            "You are diagnosing chronic integration incidents (timeouts, poison messages, reconciliation breaks).",
            "You are asked to “just put an ESB/API in front” of incompatible systems.",
            "You need to explain to executives why a two-week integration estimate became a two-quarter program.",
        ],
        "when_not": [
            "The problem is a single team’s internal module wiring.",
            "You are using “it’s complex” to avoid writing a contract and an SLA.",
        ],
        "nfr": [
            "Availability mismatch (sync call to a batch system)",
            "Schema ownership and canonical vs translated models",
            "Data classification and need-to-know",
            "Change velocity on each side of the boundary",
        ],
        "how_pattern": (
            "Treat difficulty as a checklist, not a vibe. For every flow document: protocol, schema owner, SLA on each "
            "side, identity, network path, data class, and the team that gets paged. Where two sides cannot share an SLA, "
            "you **must** insert an asynchronous buffer, a file landing zone, or an anti-corruption layer—not a hope.\n\n"
            "Canonical models can reduce translation cost, but they become a political object. Prefer **published language** "
            "at the boundary (an event schema, an API contract, a file spec) over a single enterprise object that every "
            "system must adopt internally."
        ),
        "how_aws": (
            "AWS gives you primitives that absorb some difficulties: SQS absorbs availability mismatch; S3 absorbs large "
            "payloads; PrivateLink and VPC endpoints absorb some network constraints; KMS and IAM absorb some security "
            "mechanics. AWS does not absorb schema politics or a partner who only speaks SFTP. Transfer Family exists "
            "because that partner constraint is real."
        ),
        "diagram": """flowchart TB
  P[Protocol mismatch] --> B[Boundary contract]
  S[Schema mismatch] --> B
  A[Availability mismatch] --> B
  Sec[Security boundary] --> B
  N[Network boundary] --> B
  L[Legacy constraint] --> B
  O[Org ownership] --> B
  B --> Style{API / Queue / Event / File / Adapter}""",
        "tradeoffs": [
            ("Sync simplicity", "Easier happy-path UX", "Couples availability and latency"),
            ("Canonical model", "One translation to the hub", "Hub becomes a bottleneck and a committee"),
            ("Copying data everywhere", "Local speed", "Divergent truth and compliance risk"),
        ],
        "decision": (
            "The 3PL is unavailable on Sundays. Checkout is not. Do you fail Sunday orders, queue them, or write a file "
            "for Monday morning? What does the customer see, and which system is the source of truth for “accepted order”?"
        ),
        "checks": [
            {
                "q": "Name three non-technical reasons integration fails.",
                "a": "Conflicting ownership, incompatible SLAs/business calendars, and contractual partner constraints (protocol, data residency, liability).",
            },
            {
                "q": "What should you insert when availability SLAs cannot be shared?",
                "a": "An asynchronous buffer (queue), a landing zone (files), or a scheduled reconciliation—not a synchronous call that pages the wrong team.",
            },
        ],
        "anti_patterns": [
            "Point-to-point “temporary” interfaces that become the enterprise.",
            "A single “integration team” owning every mapping with no domain owners.",
            "Assuming cloud migration removes partner SFTP or mainframe batch windows.",
        ],
        "architect_note": (
            "Write the constraints on the diagram. A diagram without Sunday downtime and SFTP is a wish."
        ),
    },
    {
        "id": "1.3",
        "title": "Integration Styles",
        "module": "01 — Enterprise Integration Fundamentals",
        "objectives": [
            "Describe API, messaging, events, files, ESB, streaming, and agentic integration as styles—not products.",
            "Map each style to coupling, latency, cardinality, and payload size.",
            "Choose a style from characteristics rather than from a preferred vendor.",
        ],
        "scenario": (
            "CareMesh Health’s PMO lists seven “integrations” on one slide: a patient lookup, lab result distribution, "
            "nightly claims files, an HL7 feed from a hospital, a pub/sub of appointment changes, a Kafka-like clickstream, "
            "and a proposed chatbot that “talks to the EHR.” They are seven different styles. Treating them as one "
            "“interface project” will produce the wrong platform."
        ),
        "why": (
            "Styles encode **coupling and time**. An API couples caller and provider in time (both must be up) but gives "
            "an immediate answer. A queue decouples time and absorbs bursts. An event decouples knowledge of consumers. "
            "A file decouples protocol and batch size. An ESB centralizes mediation when you cannot change endpoints. "
            "Streaming is a continuous ordered (or partitioned) fact feed—closer to events at high volume. An AI agent "
            "is not a transport; it is a reasoning consumer of **governed tools** that still use the other styles."
        ),
        "when": [
            "API: the consumer knows the provider, needs a response now, payload is modest (GET /patients/{id}).",
            "Message/queue: one worker should process a command; work must survive consumer outages.",
            "Event: a fact occurred; many independent reactions are valid (LabResultReady).",
            "File: bulk or partner protocol constraint (nightly 2 GB claims).",
            "ESB/adapter: protocol mediation you cannot yet remove.",
            "Streaming: high-volume continuous facts with consumer lag semantics.",
            "Agent: a human needs a natural-language operational interface over existing tools.",
        ],
        "when_not": [
            "Do not use an API as a bulk file pipe.",
            "Do not use a queue when you mean “notify whoever cares” (that is an event/topic).",
            "Do not use an agent as a bypass around authorization.",
            "Do not use an ESB as the default for greenfield service-to-service calls.",
        ],
        "how_pattern": (
            "Put the styles on one decision table used for the rest of the course:\n\n"
            "| Style | Time coupling | Consumer knowledge | Typical payload | Cardinality |\n"
            "|-------|---------------|--------------------|-----------------|-------------|\n"
            "| API | Coupled | Known provider | Small | 1:1 request/reply |\n"
            "| Queue | Decoupled | Known worker type | Small–medium | Competing consumers |\n"
            "| Event | Decoupled | Unknown | Small | 1:N |\n"
            "| File | Decoupled | Known landing zone | Large | Batch |\n"
            "| ESB | Mixed | Hub knows both | Mixed | Many:many via hub |\n"
            "| Stream | Decoupled | Unknown / lagging | Small, high rate | 1:N |\n"
            "| Agent | Mixed | Tools known, users not | Prompts + tool IO | Orchestrated |\n"
        ),
        "how_aws": (
            "Illustrative mapping only: API Gateway + Lambda; SQS; EventBridge/SNS; S3 + Transfer Family; adapters or "
            "Step Functions for orchestration; Kinesis/MSK for streams; Bedrock agents or custom tool-calling loops "
            "for agents. The mapping is a **consequence** of the style, not the definition of the style."
        ),
        "diagram": """flowchart TB
  R[Requirement] --> C[Characteristics]
  C --> S{Style}
  S --> API[API]
  S --> MSG[Message / Queue]
  S --> EV[Event]
  S --> FILE[File]
  S --> ESB[ESB / Adapter]
  S --> STR[Stream]
  S --> AI[AI Agent + tools]""",
        "tradeoffs": [
            ("API", "Immediate consistency for the caller", "Availability and latency coupling"),
            ("Events", "Independent evolution of consumers", "Eventual consistency and replay design"),
            ("Files", "Partner reach and bulk efficiency", "Latency and operational file hygiene"),
        ],
        "decision": (
            "Classify CareMesh’s seven items. Which two are most dangerous to implement as synchronous APIs, and why?"
        ),
        "checks": [
            {
                "q": "Is an AI agent an integration style for moving a 10 GB file?",
                "a": "No. The agent may *ask* for file status through a tool. The file still moves via a file style (SFTP/S3).",
            },
            {
                "q": "What is the cardinality difference between a queue and an event?",
                "a": "A queue is competing consumers for a command (usually processed once). An event is fan-out: many consumers may each react.",
            },
        ],
        "anti_patterns": [
            "“We are event-driven” while every consumer is a synchronous HTTP call in disguise.",
            "Streaming platform as a default because it is fashionable.",
            "One “integration microservice” that implements all seven styles poorly.",
        ],
        "architect_note": (
            "Memorize the decision table. You will reuse it in every lab and every capstone."
        ),
    },
    {
        "id": "1.4",
        "title": "Synchronous vs Asynchronous Integration",
        "module": "01 — Enterprise Integration Fundamentals",
        "objectives": [
            "Draw sequence diagrams for request/reply versus fire-and-forget versus async status.",
            "Explain how timeouts, user experience, and compensating actions differ.",
            "Choose sync, async, or sync-over-async (accepted + status) from latency SLAs.",
        ],
        "scenario": (
            "Atlas Manufacturing’s sales portal must show whether a configured product can be built. Engineering’s "
            "configurator sometimes takes 40 seconds. Sales wants a spinner. Plant systems want no blocking calls during "
            "shift changes. You must decide what “the user waits” actually means."
        ),
        "why": (
            "Synchronous integration is a **distributed function call**: the caller’s thread, UX, or SLA is held hostage "
            "by the provider. Asynchronous integration returns an acknowledgement of *receipt* (or nothing) and completes "
            "work later. Most enterprise pain is using sync where the provider cannot meet the caller’s timeout, or using "
            "async where the business process legally cannot proceed without an answer (authorization of a payment).\n\n"
            "A third pattern—**synchronous acceptance, asynchronous completion**—issues an ID and a status resource. "
            "Large files and long workflows almost always need this."
        ),
        "when": [
            "Synchronous: user-facing reads with tight latency (account balance in 300 ms), or a command that must succeed or fail before the next legal step.",
            "Asynchronous: work that may exceed UX timeouts, bursty load, or providers with weaker SLAs.",
            "Accepted+status: multi-step or large payload processing the user can poll or subscribe to.",
        ],
        "when_not": [
            "Do not make a UI wait on a partner SFTP round trip.",
            "Do not make payment authorization fire-and-forget without a defined completion event and reconciliation.",
            "Do not hide a 30-second chain of sync calls behind one API and call it “real time.”",
        ],
        "how_pattern": (
            "Draw time on the vertical axis. If any hop can exceed the caller’s timeout, the design is already wrong. "
            "Budgets compose: a 300 ms API with three 150 ms dependencies cannot work. Async designs need a **correlation ID**, "
            "an **idempotency key**, and a **completion signal** (event, status row, or callback). Without those, async "
            "becomes “we lost the work.”"
        ),
        "how_aws": (
            "API Gateway has integration timeouts (and payload limits). Lambda has duration limits. SQS and Step Functions "
            "exist specifically so the HTTP request does not wait for the whole business process. Status APIs typically "
            "read DynamoDB. None of that excuses a 40-second synchronous configurator behind a 29-second gateway timeout."
        ),
        "diagram": """sequenceDiagram
  participant U as User
  participant P as Portal
  participant G as Integration
  participant E as Engineering
  U->>P: Configure product
  P->>G: POST /configurations
  G-->>P: 202 Accepted + id
  P-->>U: Show "checking..."
  G->>E: Queue ConfigureRequested
  E-->>G: ConfigurationCompleted
  U->>P: GET /configurations/id
  P->>G: GET status
  G-->>P: READY / FAILED
  P-->>U: Result""",
        "tradeoffs": [
            ("Sync", "Simple UX and easier transactional mental model", "Timeouts and cascading failure"),
            ("Async", "Resilience and elasticity", "Status UX, eventual consistency, harder debugging"),
            ("202 + poll/push", "Honest about duration", "More moving parts (store, events, UI)"),
        ],
        "decision": (
            "If the configurator p95 is 40 s and the portal SLA is 2 s to first response, which sequence diagram is acceptable? "
            "What does the customer see if engineering is down for an hour?"
        ),
        "checks": [
            {
                "q": "Why do timeouts compose badly in synchronous chains?",
                "a": "Each hop consumes part of the caller’s budget. Tail latency adds. A chain that “usually works” fails at p99 and takes the user experience with it.",
            },
            {
                "q": "What three elements must an async process include?",
                "a": "Correlation identifier, idempotent processing, and a completion/failure signal the caller can observe.",
            },
        ],
        "anti_patterns": [
            "Raising every timeout to 15 minutes instead of changing style.",
            "Async with no status—users refresh and raise tickets.",
            "Callback URLs to unauthenticated internet endpoints.",
        ],
        "architect_note": (
            "If you cannot draw the sequence diagram including failure, you do not understand the integration yet."
        ),
    },
    {
        "id": "1.5",
        "title": "Point-to-Point Integration",
        "module": "01 — Enterprise Integration Fundamentals",
        "objectives": [
            "Explain why N systems can produce N(N-1) integrations.",
            "Recognize when point-to-point is the correct simple choice.",
            "Describe the maintenance failure mode of an undocumented mesh.",
        ],
        "scenario": (
            "Northbridge started with core banking calling fraud. Then CRM called core. Then mobile called CRM and core. "
            "Then the data team copied from all three. Then a new collections SaaS called CRM and core. Nobody can answer "
            "“what happens if we change the customer address schema?” without a two-week discovery. That is point-to-point decay."
        ),
        "why": (
            "Point-to-point is the default of delivery teams: the shortest path from this project to that API. Each link "
            "is locally rational. The estate becomes a complete graph. Every schema change, credential rotation, and "
            "outage multiplies. Observability fragments because there is no common correlation. Security reviews cannot "
            "enumerate the blast radius.\n\n"
            "Hub-and-spoke, event notification, and API products exist to **reduce the number of unique contracts**, not "
            "because hubs are fashionable. But a hub that simply tunnels every point-to-point mapping is the same mesh "
            "with extra latency—the ESB anti-pattern you will study in Module 8."
        ),
        "when": [
            "Two systems, stable contract, low change rate, same owner—point-to-point can be correct and cheaper.",
            "A temporary strangler link during migration, with an expiry date in the ADR.",
        ],
        "when_not": [
            "Many consumers of the same fact (use events).",
            "Many partners with similar files (use a file platform and templates).",
            "Every new product requires a new custom link to the same six systems.",
        ],
        "how_pattern": (
            "Count unique contracts, not boxes. If the same business event is mapped six times, you have a notification "
            "problem. If six partners each have a unique private protocol, you have a partner-adapter problem—not a "
            "requirement for 36 unique APIs. Publish a contract (API product, event schema, file spec) and make "
            "consumers come to it. Record exceptions as ADRs with owners and expiry."
        ),
        "how_aws": (
            "It is just as easy to build a point-to-point mesh on AWS as on premises: Lambda A calls Lambda B calls "
            "a private ALB calls a partner URL. EventBridge, SNS, and API products are tools to *reduce* unique links. "
            "They do not automatically prevent a mesh if every team still creates a custom event and a custom queue "
            "for each pair of applications."
        ),
        "diagram": """flowchart LR
  A[App A] --> B[App B]
  A --> C[App C]
  A --> D[App D]
  B --> C
  B --> D
  C --> D
  B --> A
  C --> A
  D --> A
  C --> B
  D --> B
  D --> C""",
        "tradeoffs": [
            ("P2P speed", "Fast for the first two systems", "Quadratic operational cost"),
            ("Platform", "Reusable contracts and shared ops", "Requires governance so it does not become a new mesh"),
        ],
        "decision": (
            "You have 80 internal applications. If each needs a custom pair-wise integration with 10 others, how many "
            "contracts exist? What inventory question would you ask before approving the 801st?"
        ),
        "checks": [
            {
                "q": "When is point-to-point acceptable?",
                "a": "Stable, low-N, same-owner links with a documented contract—or time-boxed migration links with an expiry.",
            },
            {
                "q": "How does an ESB recreate point-to-point?",
                "a": "If every pair still has a unique mapping owned by the bus team, you have moved the mesh into the hub. Change still requires hub releases.",
            },
        ],
        "anti_patterns": [
            "Undocumented integrations discovered only in packet captures.",
            "Shared databases as “integration” between apps.",
            "Permanent “temporary” interfaces.",
        ],
        "architect_note": (
            "Your first operating metric for an integration platform is *unique contracts per business event*, not number of Lambdas."
        ),
    },
    {
        "id": "1.6",
        "title": "Integration Architecture Decision Framework",
        "module": "01 — Enterprise Integration Fundamentals",
        "objectives": [
            "Apply API vs Message vs Event vs File vs ESB vs Agent as a repeatable decision procedure.",
            "List the NFRs that drive the choice (volume, payload, latency, reliability, ordering, security, cost, coupling).",
            "Produce a one-page ADR fragment from a business requirement.",
        ],
        "scenario": (
            "A product owner says: “When a customer updates their address, twenty systems need to know, and the call "
            "center needs the new address immediately, and once a night we send a full extract to a regulator, and "
            "agents should be able to ask whether the update succeeded.” That is four requirements. The framework exists "
            "so you do not pick EventBridge for all of them because the last project used EventBridge."
        ),
        "why": (
            "Without a framework, teams copy the last success. The last success had different NFRs. The framework forces "
            "you to name **characteristics** before **technology**. It is the spine of this course: you will use it in "
            "Lab 1, every architecture challenge, Module 14, and all four capstones."
        ),
        "when": [
            "Any new integration request, including “small” ones.",
            "Any modernization of an ESB mapping.",
            "Any proposal to let an AI agent take action.",
        ],
        "when_not": [
            "Do not skip the framework because the team already “knows it is SQS.”",
            "Do not use the framework to delay a two-system, same-owner, obvious API for a week of ceremony.",
        ],
        "how_pattern": (
            "Procedure:\n\n"
            "1. Write the business action in one sentence.\n"
            "2. Score: latency, payload size, volume, ordering, delivery guarantee, number of consumers, protocol constraints, sensitivity, cost sensitivity, operational skill.\n"
            "3. Choose style from the Module 1.3 table.\n"
            "4. Choose architecture (sync, queue, topic, landing zone, adapter, tool+HITL).\n"
            "5. Choose technology.\n"
            "6. Write the ADR: options, decision, security, reliability, cost, operations.\n\n"
            "Worked micro-examples: GET balance → API. Process payment instruction that can retry → message. "
            "AddressChanged to twenty systems → event. 20 GB nightly to 50 partners → file. ISO20022 over MQ to a "
            "host you cannot change this year → adapter. “Did the file arrive?” → agent over a status API, not over the database."
        ),
        "how_aws": (
            "Technology selection is last: API Gateway, SQS, EventBridge/SNS, S3/Transfer Family, an adapter (often still "
            "a container or a commercial iPaaS connector), Bedrock or a tool-calling loop. Cost and operational complexity "
            "are first-class NFRs—Transfer Family hourly cost, Lambda concurrency, EventBridge bus strategy, and CloudWatch "
            "ingestion all belong in the ADR, not as afterthoughts."
        ),
        "diagram": """flowchart TD
  BR[Business requirement] --> NFR[NFRs / characteristics]
  NFR --> ST[Style]
  ST --> AR[Architecture]
  AR --> TE[Technology]
  TE --> IM[Implementation]
  IM --> FT[Failure testing]
  FT --> OP[Operations]
  OP --> ADR[ADR]""",
        "tradeoffs": [
            ("Framework discipline", "Comparable decisions across teams", "Feels bureaucratic if over-applied to trivial links"),
            ("Recording ADRs", "Future you can defend the choice", "Requires a repository people actually read"),
        ],
        "decision": (
            "Split the product owner’s sentence into four flows. Select a style for each. Which flow is most likely "
            "to be mis-implemented as a synchronous API, and what incident would that cause?"
        ),
        "checks": [
            {
                "q": "What comes before technology selection?",
                "a": "Requirement, characteristics/NFRs, style, and architecture.",
            },
            {
                "q": "Why might an agent still use an API?",
                "a": "Agents should call governed tools. Those tools are ordinary integrations (API, queue, file status). The agent is not a new transport into the database.",
            },
        ],
        "anti_patterns": [
            "Starting the design with a service name (“we will use EventBridge”).",
            "One style applied to an entire domain regardless of NFRs.",
            "ADRs written after implementation to rubber-stamp the code.",
        ],
        "architect_note": (
            "Lab 1 is this lesson made interactive. If you guess without characteristics, you will fail the lab even if you guess the popular AWS service."
        ),
    },
]
