#!/usr/bin/env python3
"""Modules 2–3 lesson records (API + messaging)."""

from __future__ import annotations

def L(id, title, module, objectives, scenario, why, when, when_not, how_pattern, how_aws, decision, **kw):
    d = dict(
        id=id, title=title, module=module, objectives=objectives, scenario=scenario,
        why=why, when=when, when_not=when_not, how_pattern=how_pattern, how_aws=how_aws,
        decision=decision,
    )
    d.update(kw)
    return d

M02_MOD = "02 — API-Based Integration"

M02 = [
    L("2.1", "API Fundamentals", M02_MOD,
      ["Define an API as a productized contract, not a URL.",
       "Distinguish public, partner, and private APIs.",
       "Explain why APIs are the wrong default for bulk and fan-out."],
      "Northbridge’s mobile team “just needs an API to payments.” Payments already has a 15-year ISO message interface. "
      "The architect’s job is to decide whether a sync API is the right *product* for this consumer, or a façade over async settlement.",
      "APIs exist so consumers can invoke a known provider with request/reply semantics. They are the right tool when the "
      "caller needs an answer in-band: balances, quotes, create-order with validation errors. They are also how you productize "
      "a capability for many consuming teams without giving them database credentials. An API is a **contract plus an SLA**, "
      "not a Lambda with API Gateway in front of a table.",
      ["Immediate response is required and payload is modest.",
       "The consumer knows (or is allowed to know) the provider.",
       "You need input validation and typed errors back to a human or app.",
       "You are exposing a stable capability as a product."],
      ["The payload is hundreds of megabytes.",
       "Many unknown consumers should react to a fact (use events).",
       "The provider cannot meet the caller’s timeout (use async acceptance)."],
      "Treat APIs as products: owner, version policy, SLOs, authn/z, error model, deprecation. Classify **query APIs** "
      "(safe, cacheable reads) versus **command APIs** (state change, need idempotency). Record who is allowed to call, "
      "from which network, and what happens when the API is down.",
      "Amazon API Gateway (HTTP or REST), Lambda or containers, IAM/JWT authorizers, WAF, and CloudWatch. Private APIs "
      "and VPC links exist for in-estate callers. The presence of API Gateway does not make an integration synchronous-safe "
      "if the backend is a 40-second batch job.",
      "Should the mobile app call payments synchronously to *initiate* a transfer, to *read status*, or both? What is the "
      "user-visible failure if payments is in a maintenance window?",
      nfr=["Latency SLO", "Payload size", "Authn audience (employee vs customer vs partner)", "Write vs read"],
      diagram="sequenceDiagram\n  participant C as Consumer\n  participant A as API\n  participant S as System of record\n  C->>A: Request + auth\n  A->>A: Validate + authorize\n  A->>S: Command or query\n  S-->>A: Result\n  A-->>C: Response + correlation ID",
      tradeoffs=[("Productized API", "Reusable, governed access", "Versioning and support load"),
                 ("Bespoke API per app", "Fits one client perfectly", "Becomes point-to-point")],
      checks=[{"q": "What makes an API a product?",
               "a": "Named owner, contract, SLO, security model, versioning, and support—not merely a deployed URL."}],
      anti_patterns=["Database-as-API (exposing tables).", "Chatty APIs that require 20 round trips for one screen."],
      architect_note="If you cannot name the SLO, you do not have an API product yet."),
    L("2.2", "REST Architecture", M02_MOD,
      ["Apply resource-oriented design (nouns, not verbs-in-URLs as the only model).",
       "Use uniform interface ideas: identification, representations, self-describing messages.",
       "Recognize when RPC-over-HTTP is honest and when it is a REST costume."],
      "Harbor Retail’s first order API was POST /doCreateOrder with a 40-field blob. Mobile, warehouse, and finance each "
      "parsed it differently. REST is not aesthetics; it is a way to make resources evolvable and cacheable.",
      "REST (Representational State Transfer) is an architectural style for networked applications. Resources are identified "
      "by URIs. Clients manipulate representations (usually JSON). Uniform methods reduce the need for custom verbs. "
      "Hypermedia is optional in most enterprises; **stable resource models and status codes** are not. RPC-over-HTTP can "
      "be fine for internal actions (“POST /transfers/{id}/reverse”) if you do not pretend it is REST and then expect caching.",
      ["CRUD-ish domain objects that many clients share.",
       "Need for cacheable reads (GET) and explicit unsafe writes.",
       "Public or partner APIs where predictability matters."],
      ["Extremely chatty orchestration better modeled as a process API or async workflow.",
       "Binary bulk transfer.",
       "When the only “resource” is a stored procedure with 90 parameters—fix the model first."],
      "Identify resources (Order, Payment, CustomerAddress). Separate collection and item URLs. Use representations that "
      "match consumer jobs, not internal tables. Keep commands that are not CRUD as documented RPC-style resources rather "
      "than twisting nouns until they lie.",
      "API Gateway maps HTTP methods to integrations. You still design the resource model. OpenAPI is the contract artifact. "
      "CloudFront caching is only valid for true GETs with correct cache keys and authorization.",
      "Is “ReserveInventory” a resource state change on an Order, a new InventoryReservation resource, or a message? "
      "What breaks if two clients use different models?",
      diagram="flowchart LR\n  Client -->|GET /orders/123| API\n  API -->|representation JSON| Client\n  Client -->|POST /orders| API",
      tradeoffs=[("REST resources", "Evolvable, cacheable reads", "Awkward for long-running processes"),
                 ("RPC/HTTP", "Fits actions", "Weaker caching and easier to explode into unique verbs")],
      checks=[{"q": "Why is GET special?",
               "a": "It is safe and idempotent in HTTP semantics, enabling caching, retries, and simpler reasoning—if you do not hide writes in GET."}],
      anti_patterns=["GET that places orders.", "Verbs in paths for every action without a resource model."],
      architect_note="REST is a style. If you violate HTTP safety, say so in the contract."),
    L("2.3", "HTTP Methods", M02_MOD,
      ["Choose GET, POST, PUT, PATCH, DELETE with correct safety and idempotency expectations.",
       "Explain why POST is not always non-idempotent in practice (and why you still need keys).",
       "Map methods to order-create and order-read in Lab 2."],
      "A partner retries POST /orders because of a mobile timeout. Without an Idempotency-Key, Harbor creates two orders "
      "and two payment attempts. Method choice and idempotency are inseparable.",
      "GET retrieves a representation and must not change server state. POST creates or triggers processing; it is not "
      "idempotent by HTTP definition. PUT replaces a resource at a known ID and should be idempotent. PATCH applies a "
      "partial update; idempotency depends on the patch semantics. DELETE removes or tombstones; repeating DELETE should "
      "not create a new error after the resource is gone (typically 404 or 204). Architects choose methods to make **retries safe**.",
      ["GET for reads, including status resources.",
       "POST for creation when the server assigns IDs.",
       "PUT when the client knows the ID and replacement is the model.",
       "PATCH for partial updates with a documented merge model.",
       "DELETE for removal with defined tombstone behavior."],
      ["Do not use GET for side effects.",
       "Do not use PUT to “create or append a payment” if replacement would destroy history.",
       "Do not assume POST retries are safe."],
      "Publish a method table in the API contract. For POST creates, require Idempotency-Key (Lesson 2.11). For PUT, "
      "define whether lost updates are prevented with ETags. Align status codes: 201 created, 202 accepted, 204 no content, "
      "409 conflict, 422 validation.",
      "API Gateway + Lambda can implement any method. Gateway does not enforce HTTP safety for you. Lab 2 implements "
      "POST /orders and GET /orders/{id}—notice there is no GET that creates.",
      "If POST /orders times out after the server committed, what should the client send on retry, and which method remains GET?",
      diagram="flowchart TB\n  GET[GET safe idempotent] --> R[Read]\n  PUT[PUT idempotent replace] --> W[Write]\n  PATCH[PATCH maybe idempotent] --> W\n  DELETE[DELETE idempotent remove] --> W\n  POST[POST not idempotent unless keyed] --> C[Create/action]",
      tradeoffs=[("POST + server IDs", "Simple clients", "Must add idempotency keys"),
                 ("PUT + client IDs", "Natural retries", "ID allocation and ownership rules")],
      checks=[{"q": "Is PUT always safe to retry?",
               "a": "It should be idempotent as a replacement, but lost-update races still need ETags or version fields."}],
      anti_patterns=["Using 200 for created resources with no Location.", "DELETE that physically erases audit history in a bank."],
      architect_note="Lab 2 will punish a GET with side effects. Do not invent one."),
    L("2.4", "API Contracts", M02_MOD,
      ["Treat OpenAPI as the source of truth for fields, errors, and auth.",
       "Explain consumer-driven vs provider-driven contract testing at an architecture level.",
       "Decide what is in the public contract versus internal domain model."],
      "CareMesh published a PDF of “the API.” Three vendors implemented three interpretations of optional birthdate. "
      "A machine-readable contract would have failed CI before patients were mismatched.",
      "A contract is the **supported behavior** of the API: resources, schemas, required headers, error envelopes, "
      "pagination, rate limits, and lifecycle. Documents in slides are not contracts. Code is not a contract if consumers "
      "cannot see it. Breaking a contract is a business event: pagers, version bumps, or both.",
      ["Any API with more than one consuming team or a partner.",
       "When you need generated clients or mock servers.",
       "When security wants a reviewable surface."],
      ["A one-off script between the same two developers this afternoon—still write a JSON example, just do not pretend it is a platform."],
      "Write OpenAPI (or equivalent) first for public/partner APIs. Keep an anti-corruption layer so internal models can "
      "change. Version the contract. Add examples for error paths. Require contract tests in CI: provider verifies it still "
      "meets the spec; consumers verify they can parse it.",
      "API Gateway can import OpenAPI. That import is not governance. Store specs in git next to Terraform. Reject deploys "
      "that silently drop fields. JSON Schema (next lesson) is often embedded in the contract.",
      "A field must move from optional to required. Is that a breaking change? What is your communication path to twenty consumers?",
      diagram="flowchart LR\n  Spec[OpenAPI contract] --> GW[Gateway]\n  Spec --> Tests[Contract tests]\n  Spec --> Docs[Developer portal]\n  Spec --> Mocks[Mocks]",
      tradeoffs=[("Spec-first", "Clear review and mocks", "Feels slower on day one"),
                 ("Code-first", "Fast spike", "Consumers reverse-engineer production")],
      checks=[{"q": "What is a breaking change?",
               "a": "Any change that causes a well-behaved consumer of the previous contract to fail or misinterpret data—removed fields, tighter required, changed meaning, auth changes."}],
      anti_patterns=["Optional fields that are actually required in the implementation.", "Undocumented headers that production depends on."],
      architect_note="If it is not in the contract, it is not supported—even if a Lambda still reads it."),
    L("2.5", "JSON Schema", M02_MOD,
      ["Use JSON Schema (or equivalent) to validate payloads at the edge.",
       "Distinguish syntactic validation from business validation.",
       "Place validation where poison messages and bad files cannot enter the estate."],
      "A partner sent amount as a string \"1,000.00\" with a comma. Downstream payment posting treated it as 1. Harbor "
      "lost a day to reconciliation. Schema validation at the edge would have returned 422 in milliseconds.",
      "JSON Schema describes types, required fields, ranges, formats, and enumerations. It catches **malformed** data. "
      "It does not catch “this account is frozen” or “this SKU is discontinued.” Architects still need business rules. "
      "But most incidents start as malformed messages that were stored, queued, and replayed for hours.",
      ["Public and partner APIs.",
       "Events and file row schemas as well as REST bodies.",
       "Anywhere you currently parse JSON and hope."],
      ["Do not encode the entire credit policy in JSON Schema.",
       "Do not reject unknown fields if you promised forward compatibility—configure additionalProperties deliberately."],
      "Validate at the first trust boundary. Return a stable error envelope with a machine-readable code and a correlation ID. "
      "Keep schemas versioned with the contract. For files, validate the header and a sample of rows before the whole batch posts.",
      "API Gateway HTTP APIs have limited native JSON Schema; many teams validate in Lambda with a library. That is acceptable "
      "if it is the first thing the function does and failures are metric’d. Do not validate only in a deep domain service "
      "after the payload has fanned out.",
      "Where should validation live if both API Gateway and a later SQS consumer can receive the same logical order?",
      diagram="flowchart LR\n  In[Payload] --> Syn[Syntactic schema]\n  Syn -->|fail| 422[422 / poison]\n  Syn -->|pass| Biz[Business rules]\n  Biz -->|fail| 409[409 / 422 business]\n  Biz -->|pass| Dom[Domain]",
      tradeoffs=[("Strict schema", "Fewer poison messages", "Harder evolution"),
                 ("Loose schema", "Easier change", "Garbage enters queues and lakes")],
      checks=[{"q": "Does a valid JSON Schema document mean the payment is legal?",
               "a": "No. It means the document is well-formed. Business eligibility is a separate layer."}],
      anti_patterns=["Validating only in the UI.", "Different schemas for the same event in each consumer."],
      architect_note="Lab 2 requires validation. Fail closed on types; be explicit about additional properties."),
    L("2.6", "API Versioning", M02_MOD,
      ["Choose URI, header, or media-type versioning with eyes open.",
       "Define compatible vs breaking evolution.",
       "Plan deprecation, dual-run, and sunset."],
      "Northbridge’s /v1/customers returns a single address string. /v2 returns structured lines plus country. Mobile "
      "can migrate in a quarter; a corporate payroll partner cannot. Versioning is a product strategy, not a URL fashion.",
      "APIs change. Versioning is how you change without a flag day. Compatible changes (additive optional fields, new "
      "endpoints) should not require a major version if consumers ignore unknowns. Breaking changes need a new version "
      "and a sunset policy. Running two versions has a real cost: double tests, double bugs, double IAM.",
      ["External or numerous consumers.",
       "Breaking semantic changes to existing fields.",
       "Regulatory formats that must remain stable for years."],
      ["Do not version every additive field.",
       "Do not keep v1 forever without an owner and a kill date.",
       "Do not use versions to hide a bad resource model (fix the model)."],
      "Prefer additive evolution. When you must break: introduce vN, route both, emit metrics on vN-1 usage, communicate, "
      "sunset. Header versioning keeps URLs pretty but is harder to try in a browser. URI versioning is explicit for partners. "
      "Either is fine if it is consistent and automated.",
      "API Gateway stage variables or path prefixes (/v1, /v2) are implementation. Custom domains can hide this. "
      "The hard part is data: can v1 and v2 share the same DynamoDB item shape with translation?",
      "You must add a second address. Is that a new field on v1 or a v2? What is the sunset for the payroll partner?",
      diagram="flowchart LR\n  C1[v1 clients] --> V1[/v1]\n  C2[v2 clients] --> V2[/v2]\n  V1 --> T[Translator]\n  V2 --> D[(Store)]\n  T --> D",
      tradeoffs=[("URI version", "Obvious to partners", "URL proliferation"),
                 ("Header version", "Cleaner URLs", "Worse discoverability")],
      checks=[{"q": "Is adding an optional field a breaking change?",
               "a": "Usually no, if clients ignore unknown fields and the field is truly optional in behavior."}],
      anti_patterns=["Silent reinterpretation of an existing field’s meaning.", "v1, v2, v3 all eternally in production."],
      architect_note="Put the sunset date in the ADR, not in Slack."),
    L("2.7", "Authentication and Authorization", M02_MOD,
      ["Separate authentication (who) from authorization (what).",
       "Choose OAuth2/OIDC, IAM, mTLS, or API keys for the right audience.",
       "Apply least privilege to the integration identity, not the human user only."],
      "A vendor kept a static API key in a mobile binary. The key could POST refunds. Authentication happened; authorization "
      "was “if you have the key, you are God.” That is not an enterprise API.",
      "Authentication establishes identity: a user, an app, a partner system. Authorization decides permitted operations "
      "and data. They are different controls. API keys identify an app poorly and do not bind a user. OAuth2/OIDC binds "
      "users and apps with scopes. mTLS binds machines. IAM binds AWS principals. Fine-grained authorization (this customer "
      "may see only their orders) often lives in the application after identity is proven.",
      ["Human users: OIDC + scoped tokens.",
       "Service-to-service inside AWS: IAM or private mTLS.",
       "Partners: OAuth client credentials or mTLS plus allow lists.",
       "Always: least privilege on the execution role behind the API."],
      ["API keys as the only control for money movement.",
       "Long-lived God tokens in Git.",
       "Authorizing only at the edge and trusting every downstream call blindly without identity propagation."],
      "Define the audience. Propagate a correlation ID and a subject. Enforce object-level auth in the service. Log "
      "access decisions for audit. Rotate credentials. Prefer short-lived tokens. For employees versus customers, "
      "do not mix identity stores accidentally.",
      "API Gateway authorizers: JWT, Lambda, IAM. Cognito can issue tokens. The Lambda’s IAM role is a second identity—"
      "it must not have dynamodb:* on all tables. Module 12 deepens this. Lab 2 requires IAM least privilege on DynamoDB.",
      "The mobile app and the batch partner both create orders. Do they share a credential? What scope prevents the mobile app from issuing refunds?",
      diagram="flowchart LR\n  U[User] --> IdP[IdP]\n  IdP --> T[Token]\n  T --> GW[API Gateway]\n  GW --> AuthZ[Authorize]\n  AuthZ --> Svc[Service]\n  Svc --> IAM[Execution role]",
      tradeoffs=[("JWT user tokens", "User-aware authz", "Revocation and clock skew complexity"),
                 ("IAM service auth", "Strong AWS binding", "Awkward for external partners")],
      checks=[{"q": "Why are API keys insufficient for refunds?",
               "a": "They poorly bind identity, are often embedded or shared, and rarely encode least-privilege user context."}],
      anti_patterns=["Logging raw access tokens.", "Using the same role for read APIs and administrative replay."],
      architect_note="Security is an NFR in the decision framework, not a later overlay."),
    L("2.8", "API Gateway Patterns", M02_MOD,
      ["Place a gateway for cross-cutting concerns without turning it into an ESB.",
       "Compare edge gateway, private gateway, and backend-for-frontend.",
       "Know payload and timeout limits as architectural constraints."],
      "A team put content-based routing, transformation, orchestration, and business rules into API Gateway mappings "
      "because it was “free.” It became an untestable ESB. Gateways should terminate HTTP, auth, rate limits, and routing—"
      "not own the domain.",
      "An API gateway is a **reverse proxy with policy**. Good jobs: TLS, authn, throttling, WAF, routing to services, "
      "API keys for partners, request IDs. Bad jobs: canonical data model of the enterprise, multi-step sagas, large "
      "file ingest. Backend-for-frontend (BFF) gateways adapt for one channel (mobile vs web) without polluting the domain API.",
      ["North-south entry from internet or partners.",
       "East-west only when you need a consistent policy enforcement point.",
       "BFF when channels need radically different representations."],
      ["Do not push 10 GB through the gateway (Module 7).",
       "Do not implement the saga in mapping templates.",
       "Do not require every internal call to hairpin through a public gateway."],
      "Draw the gateway as a policy boundary. Keep domain logic in services. If you need orchestration, use a workflow "
      "engine or a service—not the gateway’s Swiss-army transformations. Document timeout and payload limits as first-class NFRs.",
      "Amazon API Gateway REST vs HTTP APIs: features vs cost/simplicity. Integrations: Lambda, HTTP, private. "
      "Payload limits (~10 MB) and integration timeouts (~29 s for REST) **force** async patterns for long work. "
      "That is an architecture decision, not a ticket to AWS support.",
      "A client wants to upload a 25 GB media file via POST through API Gateway. Which lesson’s pattern replaces this, and why is the gateway the wrong edge?",
      diagram="flowchart TB\n  Inet[Internet] --> Edge[Edge API Gateway]\n  Edge --> BFF[BFF]\n  Edge --> Dom[Domain APIs]\n  Dom --> Svc[Services]\n  BFF --> Svc",
      tradeoffs=[("Shared gateway", "Central policy", "Risk of becoming an ESB"),
                 ("Per-domain gateway", "Team autonomy", "Inconsistent security if ungoverned")],
      checks=[{"q": "Name two hard limits that change API style.",
               "a": "Payload size and integration timeout. Exceeding them requires claim-check / async status, not a bigger gateway."}],
      anti_patterns=["VTL/mapping-template business logic.", "Public gateway for high-privilege admin APIs without extra controls."],
      architect_note="When the gateway needs unit tests for business rules, you have the wrong design."),
    L("2.9", "Rate Limiting", M02_MOD,
      ["Use rate limits as a fairness and survival control, not as punishment after an outage.",
       "Distinguish burst, steady-state, and per-principal throttles.",
       "Plan client backoff and partner SLAs together."],
      "A well-meaning partner replayed a day’s worth of payments at 8:00 on Monday. Northbridge’s API scaled until DynamoDB "
      "throttled and the mobile app died. Rate limits exist to keep one consumer from becoming a denier of service.",
      "Rate limiting protects shared capacity. It is an architecture control: you are allocating a scarce resource (downstream "
      "IOPS, fraud engine, human-equivalent process). Burst allows short spikes; steady-state protects the platform. "
      "Per-key limits implement fairness among partners. Global limits protect the bank.",
      ["Any public or partner API.",
       "Any dependency with a hard TPS limit.",
       "When a retry storm is a realistic failure mode."],
      ["Do not set limits so low that legitimate onboarding fails without a quota product.",
       "Do not rate-limit without telling the client how to back off (429 + Retry-After)."],
      "Publish quotas in the contract. Return 429 with a retry hint. Combine with idempotency so retries are safe. "
      "Consider token buckets per principal. For internal APIs, still limit—retry storms from your own microservices are common.",
      "API Gateway usage plans and throttles, WAF rate rules, and service-level limiters. DynamoDB and downstream APIs have "
      "their own limits—the gateway limit should be **tighter** than the weakest dependency if you want graceful 429s instead of 500s.",
      "Partner A is allowed 10 TPS, Partner B 100 TPS. A shared unauthenticated limit would be wrong—why?",
      diagram="flowchart LR\n  P[Partners] --> RL[Per-key throttle]\n  RL --> G[Global throttle]\n  G --> API[API]\n  API --> Dep[Weakest dependency]",
      tradeoffs=[("Strict throttle", "Protects the platform", "Can stall a legitimate recovery replay"),
                 ("No throttle", "Easy demo", "First noisy neighbor wins")],
      checks=[{"q": "What should a client do on 429?",
               "a": "Back off, preferably with jitter, honor Retry-After, and retry only idempotent requests."}],
      anti_patterns=["Unlimited retries on 429.", "One global TPS for all partners regardless of contract."],
      architect_note="Quotas are commercial and technical. Architects should sit with the partner manager."),
    L("2.10", "API Error Handling", M02_MOD,
      ["Return a stable error envelope with correlation ID and a machine-readable code.",
       "Map validation, auth, conflict, and dependency failures to the right HTTP statuses.",
       "Avoid leaking internals while remaining operable."],
      "Mobile showed “Internal Server Error” for both “account frozen” and “DynamoDB throughput.” Agents could not help. "
      "Ops could not find the request. Error handling is an UX, ops, and security design.",
      "Errors are part of the contract. Clients need a code they can branch on, a human message that is safe to show, "
      "and a correlation ID for support. Operators need logs with the same ID. Security needs no stack traces or SQL on the wire. "
      "Retryable (503, 429) versus not (400, 401, 403, 404, 409, 422) must be explicit or clients will retry the unretryable.",
      ["Every external API.",
       "Internal APIs too—your other teams are clients."],
      ["Do not invent a new JSON error shape per microservice.",
       "Do not map every problem to 500.",
       "Do not return 200 with a failure payload unless you are trapped in a legacy SOAP-style constraint (and then document it as a defect)."],
      "Standardize: { code, message, details[], correlationId, retryable }. Use 401/403 correctly (unauthenticated vs unauthorized). "
      "Use 409 for conflicts (duplicate idempotency replay with different body). Use 422 for schema/business validation if you "
      "standardize on it. Include no secrets in details.",
      "API Gateway can return custom responses. Lambda should still emit structured logs. X-Ray/CloudWatch traces must share "
      "the correlation ID. Lab 2 requires this envelope.",
      "A downstream payment network times out. What status and retryable flag do you return to mobile, and what do you log internally?",
      diagram="flowchart TB\n  E[Error] --> T{Type}\n  T -->|schema| 422\n  T -->|authn| 401\n  T -->|authz| 403\n  T -->|conflict| 409\n  T -->|throttle| 429\n  T -->|down| 503\n  T -->|bug| 500",
      tradeoffs=[("Rich errors", "Better UX and ops", "Risk of leaking internals if undisciplined"),
                 ("Opaque 500s", "Safer leakage", "Unsupportable products")],
      checks=[{"q": "Why include correlationId in the error body?",
               "a": "So support and the user/agent can find the exact logs and traces without asking for timestamps and IPs."}],
      anti_patterns=["Different error JSON in each resource.", "Stack traces in partner responses."],
      architect_note="Your error model is as important as your success schema. Put it in OpenAPI."),
    L("2.11", "API Idempotency", M02_MOD,
      ["Require idempotency keys for unsafe POSTs that can be retried.",
       "Define store semantics: same key + same body = replay response; same key + different body = conflict.",
       "Relate HTTP retries, mobile timeouts, and at-least-once messaging to the same idea."],
      "Lab 2 will create orders. Mobile will retry. If you skip this lesson, you will double-charge in the capstone.",
      "Networks fail after commit but before the client sees 201. At-least-once delivery is the reality of HTTP retries. "
      "Idempotency means processing the same logical request once, returning the original result thereafter. It is not "
      "optional for payments, orders, or filings. Keys must be unique per client intent, not reused for a different cart.",
      ["Any POST that creates a business transaction.",
       "Any client on mobile or flaky networks.",
       "Any API that might later be called from a queue worker too."],
      ["Do not key only on customer ID (too coarse).",
       "Do not expire keys so fast that a 10-minute retry becomes a duplicate.",
       "GET is already idempotent—do not invent keys for reads."],
      "Client sends Idempotency-Key (UUID or ULID). Server stores key → request hash → response. On repeat: if hash matches, "
      "return stored response; if not, 409. Persist long enough to cover client retry windows (hours to days in banking). "
      "Combine with natural keys (orderId) when the client can assign IDs.",
      "DynamoDB is a common key store (condition expressions). The Lambda in Lab 2 should honor the header. This is the "
      "same discipline as idempotent consumers in Module 3—learn it once, apply it everywhere.",
      "A client retries POST with the same key but a changed amount. What must the API do, and why is returning 201 with the new amount worse?",
      diagram="flowchart TB\n  P[POST + key] --> K{Key seen?}\n  K -->|no| Proc[Process + store]\n  K -->|yes same hash| Replay[Return stored response]\n  K -->|yes different hash| Conf[409 Conflict]",
      tradeoffs=[("Keyed POST", "Safe retries", "Storage and TTL design"),
                 ("Client-assigned IDs only", "Simple PUT", "Harder for naive mobile clients")],
      checks=[{"q": "Does an idempotency key replace authorization?",
               "a": "No. It only prevents duplicate processing of the same intent by the same authorized principal."}],
      anti_patterns=["Keys logged as if they were secrets when they are not, while skipping actual secrets hygiene.",
                     "In-memory maps on Lambda (lost on cold start—use durable store)."],
      architect_note="If money can move twice, the architecture is wrong no matter how clean the Terraform is."),
]

M03_MOD = "03 — Enterprise Messaging"

M03 = [
    L("3.1", "Messaging Fundamentals", M03_MOD,
      ["Define a message as a command or document sent to a worker, not a public broadcast.",
       "Explain decoupling of time and availability.",
       "Contrast messaging with APIs and events."],
      "Northbridge’s fraud check sometimes takes 8 seconds and sometimes 90. The API that opened the account cannot wait. "
      "A message says “perform fraud check on application 55” to a worker that may start later.",
      "Messaging exists to **decouple producers from the availability and speed of consumers** while retaining a delivery "
      "intention. Unlike a broadcast event, someone is supposed to do the work. Unlike an API, the producer does not wait "
      "for completion (unless a reply queue is designed). Messages survive consumer crashes if the broker does its job.",
      ["Work can be asynchronous.",
       "You need back-pressure and buffering.",
       "The producer should not fail when the consumer is down (for a bounded time).",
       "A single logical worker type should process each command."],
      ["The caller must have the answer in 200 ms in-band.",
       "You need unknown fan-out of facts (events).",
       "The payload is a 20 GB file (claim check + file style)."],
      "Producer writes a message to a queue (point-to-point) with a contract (schema, ID, correlation). Consumers compete. "
      "Ack on success; retry on failure; DLQ after policy. Include idempotency because delivery is at-least-once in practice.",
      "Amazon SQS is the canonical AWS queue. SNS is not a queue (it is pub/sub). EventBridge is an event router. "
      "Choosing SQS means you chose the **message** style. Lab 3 implements that style.",
      "Fraud check vs “CustomerRegistered so marketing may send email”—which is a message and which is an event?",
      diagram="flowchart LR\n  P[Producer] --> Q[(Queue)]\n  Q --> C1[Consumer]\n  Q --> C2[Consumer]\n  C1 --> D[(Work store)]",
      tradeoffs=[("Queue", "Absorb outages and spikes", "Operational lag and at-least-once duplicates"),
                 ("Sync API", "Immediate result", "Coupled failure")],
      checks=[{"q": "Who is the consumer of a command message?",
               "a": "A competing worker of a known type, not “anyone interested.”"}],
      anti_patterns=["Using a queue as an event broadcast to 15 unrelated teams.", "Unbounded payload in the message body."],
      architect_note="If nobody is on the hook to process it, it is not a command—do not put it in a work queue."),
    L("3.2", "Queue Architecture", M03_MOD,
      ["Draw producer, queue, competing consumers, DLQ, and poison handling.",
       "Place the queue relative to the system of record.",
       "Decide what is stored in the message versus claimed in object storage."],
      "Harbor’s inventory reservation workers scale from 2 to 50 at noon. The queue is the architectural shock absorber "
      "between checkout and warehouse capacity.",
      "A queue is a durable buffer with competing consumers. Architecture concerns: visibility timeout, retention, "
      "encryption, access policy, DLQ, and the idempotent store. The queue is not the system of record for the business "
      "entity; it is the record of **work to be done**. After success, the business entity lives in the domain database; "
      "the message should be deleted.",
      ["Spike absorption.",
       "Protecting a slower downstream.",
       "Retryable work."],
      ["As a database.",
       "As a broadcast mechanism.",
       "As a place to store 256 KB+ of accidental XML plus images."],
      "Keep messages small: identifiers, command type, version, correlation, idempotency key. Use claim-check for blobs. "
      "Secure the queue so only the producer role can send and only the consumer role can receive. Monitor depth as an SLO.",
      "SQS standard vs FIFO (later lessons). Encryption with KMS. Resource policies. CloudWatch ApproximateNumberOfMessagesVisible "
      "is an operational metric you will put on the Module 13 dashboard.",
      "If the queue is at 2 million messages, is the architecture wrong, the consumer too small, or the producer in a retry storm?",
      diagram="flowchart LR\n  API[Order API] --> Q[Work queue]\n  Q --> W[Workers]\n  Q --> DLQ[DLQ]\n  W --> DB[(Domain DB)]",
      tradeoffs=[("Buffer", "Smooths load", "Stale work and memory of old bugs in the backlog"),
                 ("No buffer", "Simple", "Downstream outage becomes caller outage")],
      checks=[{"q": "Should the queue be the system of record for an order?",
               "a": "No. It holds work items. The order’s business state belongs in the domain store."}],
      anti_patterns=["Infinite retention as an archive.", "Consumers that never delete messages."],
      architect_note="Queue depth is both a scaling signal and a customer-delay signal. Treat it as business telemetry."),
    L("3.3", "Producer/Consumer Pattern", M03_MOD,
      ["Assign responsibilities: producer validates and sends; consumer processes idempotently.",
       "Avoid dual-write bugs when the producer also writes a database.",
       "Know when to use transactional outbox."],
      "The order service wrote “ORDERED” to DynamoDB and then failed to send SQS. Warehouse never reserved stock. "
      "Or it sent SQS and failed to write DynamoDB. Dual write is the classic producer bug.",
      "Producers are responsible for a valid, authorized command and for not losing it. Consumers are responsible for "
      "effect and ack. The dangerous pattern is **two stores** (DB and queue) updated without a transaction. Architects "
      "choose: outbox pattern, listen-to-yourself, or a single write (queue only, with the DB as a consumer).",
      ["Any reliable command pipeline.",
       "When the producer is also a system of record."],
      ["Fire-and-forget telemetry where loss is acceptable (still consider events)."],
      "Preferred: write domain state and an outbox row atomically; a relay publishes to the queue. Alternative: write "
      "the queue first with enough data to reconstruct, then let the consumer be the system of record (not always valid "
      "in banking). Document the choice in an ADR.",
      "DynamoDB streams or outbox tables + Lambda relay to SQS. Lab 3 starts simpler (producer Lambda sends to SQS) so "
      "you can see failure, then you should discuss the dual-write gap in architecture questions.",
      "If Lab 3’s producer times out after SQS accepted the message, what must the consumer do when the producer retries?",
      diagram="flowchart LR\n  Svc[Service] --> TX[(Atomic DB+outbox)]\n  TX --> Relay[Relay]\n  Relay --> Q[Queue]\n  Q --> C[Consumer]",
      tradeoffs=[("Outbox", "No lost/dup at the producer boundary", "More moving parts"),
                 ("Best-effort send", "Simple lab", "Lost or duplicate commands under failure")],
      checks=[{"q": "What is a dual-write?",
               "a": "Updating two uncoordinated stores (for example a database and a queue) and hoping both succeed."}],
      anti_patterns=["Producer catching all errors and swallowing them.", "Consumer assuming uniqueness without a key."],
      architect_note="Capstone 2’s saga will fail if you cannot explain producer reliability."),
    L("3.4", "Delivery Semantics", M03_MOD,
      ["Define at-most-once, at-least-once, and exactly-once as distributed systems claims.",
       "Explain why exactly-once across systems is usually “effectively once” via idempotency.",
       "Choose operations that can be made idempotent."],
      "A vendor promised “exactly-once SQS.” Then a consumer timed out after posting a payment but before ack. The message "
      "reappeared. Exactly-once delivery of the *message* is not the same as exactly-once *side effect*.",
      "At-most-once: send and forget; loss is possible. At-least-once: retries until ack; duplicates are possible. "
      "Exactly-once delivery in the wild is typically **at-least-once plus idempotent handlers plus dedupe storage**. "
      "Brokers may offer FIFO dedupe windows; they do not erase side effects in other systems. Architects design "
      "**effectively-once business outcomes**.",
      ["At-least-once + idempotency: money, orders, provisioning.",
       "At-most-once: optional metrics where loss is cheaper than complexity."],
      ["Do not tell executives “the queue guarantees exactly-once payments.”",
       "Do not skip idempotency because FIFO is enabled."],
      "Make handlers idempotent. Store processed IDs. Use natural transactions where a single store can commit the effect "
      "and the processed marker. Design compensating actions when a side effect cannot be made idempotent (rare; prefer "
      "to change the API).",
      "SQS standard: at-least-once, occasional duplicates. SQS FIFO: at-least-once with deduplication on a 5-minute producer "
      "window—still not a substitute for consumer idempotency if your side effect is outside SQS. Lab 3 will duplicate on purpose.",
      "Is “exactly-once” a delivery property, a handler property, or a business invariant? Who owns it in the ADR?",
      diagram="flowchart TB\n  M[Message] --> AL[At-least-once delivery]\n  AL --> IH[Idempotent handler]\n  IH --> EO[Effectively-once outcome]",
      tradeoffs=[("At-least-once", "No silent loss", "Must handle duplicates"),
                 ("At-most-once", "Simple", "Silent loss")],
      checks=[{"q": "Why is FIFO not enough for payment side effects?",
               "a": "Dedupe windows and delivery guarantees do not include the external ledger. The handler must still be idempotent."}],
      anti_patterns=["Non-idempotent email + auto-retry forever.", "Using wall-clock “we probably sent it” as dedupe."],
      architect_note="Say “effectively once” in design reviews. It signals you have met production."),
    L("3.5", "Visibility Timeout", M03_MOD,
      ["Set visibility timeout relative to processing time, not to a guess of zero.",
       "Explain why too short causes duplicate in-flight work and too long stalls recovery.",
       "Use heartbeat/extend when work duration varies."],
      "A Lambda runs 70 seconds. Visibility was 30 seconds. Two Lambdas posted the same shipment. The queue was “working as designed.”",
      "Visibility timeout is how long a received message is hidden from other consumers. It is not the same as retention. "
      "If processing exceeds visibility, another consumer receives the same message—at-least-once becomes concurrent duplicate "
      "processing. If visibility is huge and a consumer dies, work stalls until the timeout.",
      ["Always, for every queue.",
       "When p99 processing time is known from metrics."],
      ["Do not set visibility to maximum “just in case” without a dead-consumer story.",
       "Do not set it below the function timeout."],
      "Rule of thumb: visibility > function timeout + buffer, and extend if using long workers. Prefer smaller units of work. "
      "Measure processing time; alert when it approaches visibility. Document in the runbook.",
      "SQS visibility timeout, ChangeMessageVisibility, Lambda event source mapping (it coordinates deletes). "
      "Lambda timeout must be less than visibility or you will double-process. Lab 3 asks you to break this on purpose.",
      "Worker p99 is 12s, timeout is 15s, visibility is 10s. Predict the incident.",
      diagram="sequenceDiagram\n  participant Q as Queue\n  participant C as Consumer\n  Q->>C: Receive hide T vis\n  Note over C: Work longer than T\n  Q->>C: Deliver again to C2",
      tradeoffs=[("Short visibility", "Fast redelivery on crash", "Duplicate concurrent work"),
                 ("Long visibility", "Time to finish", "Slow recovery after a crash")],
      checks=[{"q": "Does a visibility timeout ack the message?",
               "a": "No. It only hides it. Delete/ack happens after successful processing."}],
      anti_patterns=["Visibility = 0.", "Visibility = 12 hours for a 2-second job."],
      architect_note="Chaos lab: shrink visibility and watch duplicates. Then you will never forget it."),
    L("3.6", "Retry", M03_MOD,
      ["Distinguish retryable vs not (schema vs dependency).",
       "Apply exponential backoff and jitter.",
       "Cap retries before DLQ."],
      "An invalid JSON message was retried 10,000 times against a healthy worker. The queue never drained. Retry without "
      "classification is an outage amplifier.",
      "Retries exist because transient failures exist: network blips, throttling, downstream 503. Retries must not exist "
      "for poison: bad schema, authz denial, business rejection. Backoff prevents retry storms. Jitter prevents synchronized "
      "thundering herds. A max attempt count protects the platform.",
      ["Transient dependency failure.",
       "Throttling (with respect for Retry-After).",
       "Unknown 5xx that your runbook marks retryable."],
      ["4xx validation errors.",
       "Non-idempotent effects without keys.",
       "Unlimited immediate retries."],
      "Classify errors in the consumer. Retry transient with backoff+jitter. Send poison to DLQ quickly. Keep original "
      "payload and error reason. Align API-level retries (clients) with queue retries so you do not multiply (3 client retries "
      "× 5 queue retries × 4 Lambda retries).",
      "SQS redrive, Lambda retry policies, AWS SDK default retries—**count them**. Lab 3 uses a redrive policy to DLQ. "
      "Module 11 expands jitter math.",
      "If both the SDK and SQS retry, how do you compute worst-case duplicate side-effect attempts?",
      diagram="flowchart TB\n  F[Failure] --> R{Retryable?}\n  R -->|no| DLQ[DLQ]\n  R -->|yes| BO[Backoff + jitter]\n  BO --> N{Attempts left?}\n  N -->|yes| Retry[Retry]\n  N -->|no| DLQ",
      tradeoffs=[("Aggressive retry", "Survives blips", "Amplifies outages"),
                 ("No retry", "Simple", "Fragile to transients")],
      checks=[{"q": "Why jitter?",
               "a": "To desynchronize retrying clients so they do not hit the dependency in lockstep."}],
      anti_patterns=["Retrying 400s.", "Sleep(1) in a hot loop without a cap."],
      architect_note="Draw the retry graph. If it is a tree that explodes, you designed an outage."),
    L("3.7", "Dead Letter Queues", M03_MOD,
      ["Use a DLQ as a controlled failure bucket, not a trash can.",
       "Require inspection, fix, and replay.",
       "Alert on DLQ depth as a customer-impact metric."],
      "Payments silently “succeeded” because failures went to a DLQ nobody watched. Reconciliation found them on Friday. "
      "A DLQ without an owner is loss with extra steps.",
      "A dead letter queue holds messages that exceeded retry policy. It preserves evidence: payload, approximate receive "
      "count, error context. The operating model is: alert, diagnose, fix code or data, replay, confirm drain. Some messages "
      "are permanently invalid and must be compensated in the business (contact the partner), not infinitely replayed.",
      ["Any queue that can poison or exhaust retries.",
       "Any pipeline with a human-impacting failure."],
      ["As long-term storage.",
       "As a way to ignore errors.",
       "Without IAM so everyone can purge production evidence."],
      "Attach DLQ with maxReceiveCount appropriate to transient vs poison (often 3–5). Encrypt it. Restrict purge. "
      "Build a replay tool that re-sends to the main queue with audit. Include DLQ depth on the ops dashboard (Module 13). "
      "Lab 3 forces you through inspect → fix → replay.",
      "SQS redrive to DLQ; Lambda onFailure destinations; EventBridge DLQs. The service name changes; the operating model does not.",
      "A message in DLQ is schema-invalid. Should you replay it before or after deploying a parser fix—or never, and notify the partner?",
      diagram="flowchart LR\n  Q[Main queue] -->|max receives| DLQ[DLQ]\n  DLQ --> Ops[Inspect]\n  Ops --> Fix[Fix]\n  Fix --> Rep[Replay]\n  Rep --> Q",
      tradeoffs=[("DLQ", "No silent loss; room to fix", "Requires ops discipline"),
                 ("Drop on failure", "Clean queues", "Silent business loss")],
      checks=[{"q": "What are the three operational steps after a DLQ alert?",
               "a": "Inspect (root cause), fix (code/data/IAM), replay (or compensate) with audit."}],
      anti_patterns=["Purging DLQ to “go green.”", "Same alarm threshold as the main queue (too late)."],
      architect_note="Capstone 1 requires replay. Practice it in Lab 3 until it is boring."),
    L("3.8", "Back Pressure", M03_MOD,
      ["Explain back-pressure as protecting the downstream instead of infinite buffering.",
       "Use queue depth, concurrency limits, and 429s as controls.",
       "Know when buffering hides a systemic overload."],
      "Checkout scaled to 10,000 TPS. Inventory workers were 50 TPS. The queue grew for three hours. Every order looked "
      "“accepted.” Then warehouse SLA died. Buffering without a policy is a delayed outage.",
      "Back-pressure is how a system says “slow down.” In messaging, infinite queues postpone the truth. Architects set "
      "limits: max outstanding messages, consumer concurrency, producer throttling, load shedding with a user-visible "
      "degradation (queue the order, or refuse). The point is to fail in a **controlled** way.",
      ["Any producer that can outrun consumers.",
       "Downstream systems with hard TPS or license limits.",
       "Batch windows that must finish by a clock time."],
      ["Unbounded queues as a personality trait.",
       "Hiding multi-hour lag behind 202 Accepted without a status UX."],
      "Define a lag SLO (for example, p95 time-in-queue). Alarm before the SLO. Autoscale consumers. If still behind, "
      "throttle producers (429) or shed load. For files, stop accepting the next file until the previous completes if "
      "that is the business rule.",
      "SQS does not magically back-pressure producers. API Gateway throttles, Lambda reserved concurrency, and explicit "
      "queue-depth alarms implement it. ECS workers with scaling policies are an alternative for slow consumers.",
      "If inventory cannot exceed 50 TPS by license, where do you enforce 50—at the worker, the queue, or the API?",
      diagram="flowchart LR\n  Prod[Producers] -->|throttle 429| API[API]\n  API --> Q[Queue depth SLO]\n  Q --> Con[Limited concurrency]\n  Con --> Down[Downstream cap]",
      tradeoffs=[("Buffer", "Smooth short spikes", "Hides chronic overload"),
                 ("Shed load", "Protects core", "Requires a product answer for rejected work")],
      checks=[{"q": "Is a growing queue always healthy elasticity?",
               "a": "No. After a lag SLO, it is an incident. Elasticity without a ceiling is a time bomb."}],
      anti_patterns=["No max receive rate.", "Autoscaling that never catches a 100× producer."],
      architect_note="Ask “what happens at 10× volume?” in every design review."),
    L("3.9", "FIFO Messaging", M03_MOD,
      ["Use FIFO when the business invariant is per-key ordering, not because it sounds safer.",
       "Understand throughput and key design (message group ID).",
       "Avoid global FIFO as a default."],
      "Account postings for a single account must not apply a debit before the opening credit. Across different accounts, "
      "ordering does not matter. Global FIFO would throttle the bank for no reason.",
      "FIFO queues preserve order **per message group** and provide producer-side deduplication windows. They cost "
      "throughput and operational complexity. Most estates need per-entity ordering, not a single global sequence. "
      "If you can design commutative, idempotent events, you may not need FIFO at all.",
      ["Per-aggregate invariants (account ledger, inventory SKU count with no commutative ops).",
       "Partners who cannot tolerate out-of-order files *and* you chose messaging rather than files."],
      ["High-throughput telemetry.",
       "Independent aggregates stuffed into one group ID.",
       "As a substitute for idempotency."],
      "Choose message group ID = the entity whose order matters (accountId). Keep groups numerous to preserve throughput. "
      "Document that FIFO ≠ exactly-once side effects. Consider whether a sequential store (ledger table with version) "
      "is a better invariant than the broker’s order.",
      "SQS FIFO: 300 TPS default (batching higher), 5-minute dedupe. If you need more, you may have chosen the wrong "
      "grouping—or you need a different architecture (sharded ledgers). Do not FIFO the entire enterprise bus.",
      "If group ID is always “ORDERS”, what happens to throughput and blast radius?",
      diagram="flowchart TB\n  M[Messages] --> G1[Group account A]\n  M --> G2[Group account B]\n  G1 --> O1[Ordered consumer A]\n  G2 --> O2[Ordered consumer B]",
      tradeoffs=[("FIFO per key", "Preserves local invariants", "Throughput and stuck-group risk"),
                 ("Standard + version checks", "Scale", "Must reject stale versions in the app")],
      checks=[{"q": "What sticks a FIFO group?",
               "a": "A poison message at the head of that group blocks later messages in the same group until it is handled."}],
      anti_patterns=["One group ID for the company.", "FIFO plus a non-idempotent handler."],
      architect_note="Stuck FIFO groups are a distinct incident type. Put them in the runbook."),
    L("3.10", "Message Ordering", M03_MOD,
      ["Separate “order of arrival” from “order of application.”",
       "Use versions, vector-like stamps, or per-key FIFO deliberately.",
       "Design for out-of-order as the default on the public internet."],
      "AddressChanged events arrived as v4 then v3 because two regions published. CRM applied v3 last and rolled back "
      "the address. Ordering is a business rule, not a network property.",
      "Distributed systems reorder. Even FIFO only orders within a group on one broker path. Architects put a **monotonic "
      "version** on the entity and refuse stale writes (conditional update). For sagas, name the legal sequences. For "
      "files, use sequence numbers in names (Module 6). Hoping Kafka/SQS “just orders” is how you corrupt CRMs.",
      ["Any entity with concurrent updates.",
       "Multi-region or multi-producer facts.",
       "Workflows where step 2 before step 1 is illegal."],
      ["Do not global-sequence the enterprise.",
       "Do not assume consumer clock time is event time."],
      "Include entity version or occurredAt plus a tie-breaker in the contract. Consumers apply compare-and-set. "
      "Buffer only when you must wait for a gap (and have a timeout). Document legal reorderings. Test out-of-order in the chaos lab.",
      "DynamoDB conditional writes on a version attribute. FIFO group IDs. EventBridge does not magically order unrelated events. "
      "Kinesis/MSK give partition order—partition key design is the architecture.",
      "v4 arrives before v3. What should CRM store, and what log line proves it refused the stale event?",
      diagram="sequenceDiagram\n  participant P as Producers\n  participant C as Consumer\n  participant D as Store\n  P->>C: Address v4\n  C->>D: CAS version 3 to 4 OK\n  P->>C: Address v3\n  C->>D: CAS fail stale",
      tradeoffs=[("CAS versions", "Correct last-write-wins with intent", "Need a version authority"),
                 ("Last arrival wins", "Simple", "Silent rollback of good data")],
      checks=[{"q": "Does a timestamp from the producer always define order?",
               "a": "No. Clocks skew. Prefer entity versions issued by the system of record."}],
      anti_patterns=["Sorting by consumer received-at.", "Dropping sequence numbers from file names."],
      architect_note="Module 5’s eventual consistency is this lesson in event clothing. You already know the move: versions."),
]
