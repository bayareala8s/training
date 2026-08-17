#!/usr/bin/env python3
"""Add missing Mermaid diagrams to overview pages, case studies, and interview docs."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CASE_STUDIES = ROOT / "case-studies"

FENCE_RE = re.compile(r"```mermaid")

# Domain overview diagrams (inserted after first paragraph under H1)
OVERVIEW_DIAGRAMS: dict[str, str] = {
    "01-computer-architecture": """```mermaid
flowchart TB
    subgraph CPU["CPU Core"]
        IF[Instruction Fetch]
        EX[Execute]
        WB[Write Back]
    end
    subgraph Memory["Memory Hierarchy"]
        L1[L1 Cache]
        L2[L2 Cache]
        RAM[Main Memory]
        SSD[Storage]
    end
    IF --> EX --> WB
    WB --> L1 --> L2 --> RAM --> SSD
```
*Figure: Memory hierarchy and CPU pipeline — foundation for latency reasoning.*""",
    "02-operating-systems": """```mermaid
flowchart LR
    User[User Space] -->|syscall| Kernel[Kernel]
    Kernel --> Sched[Scheduler]
    Kernel --> VM[Virtual Memory]
    Kernel --> FS[File System]
    Kernel --> Net[Network Stack]
```
*Figure: OS kernel responsibilities — scheduling, memory, I/O, and networking.*""",
    "03-networking": """```mermaid
flowchart TB
    App[Application] --> TLS[TLS]
    TLS --> TCP[TCP]
    TCP --> IP[IP]
    IP --> ETH[Ethernet]
    ETH --> PHY[Physical Link]
```
*Figure: Network stack layering from application to physical transport.*""",
    "04-distributed-systems-foundations": """```mermaid
flowchart TB
    subgraph Cluster["Distributed Cluster"]
        N1[Node A]
        N2[Node B]
        N3[Node C]
    end
    Client[Client] --> N1
    N1 <-.->|partial failure| N2
    N2 <-.-> N3
```
*Figure: Independent nodes with partial failure — the defining constraint of distributed systems.*""",
    "05-time-ordering-and-coordination": """```mermaid
sequenceDiagram
    participant P1 as Process 1
    participant P2 as Process 2
    P1->>P2: send event
    P2->>P2: local event
    Note over P1,P2: Logical clocks establish happened-before
```
*Figure: Event ordering across processes without a global clock.*""",
    "06-consensus": """```mermaid
stateDiagram-v2
    [*] --> Follower
    Follower --> Candidate: election timeout
    Candidate --> Leader: majority votes
    Leader --> Follower: discover higher term
    Leader --> Leader: replicate log
```
*Figure: Raft leader election and replication states.*""",
    "07-replication": """```mermaid
flowchart LR
    Primary[Primary] -->|async/sync| R1[Replica 1]
    Primary --> R2[Replica 2]
    Client[Client] -->|writes| Primary
    Client -->|reads| R1
```
*Figure: Primary-secondary replication with read/write paths.*""",
    "08-consistency": """```mermaid
flowchart TB
    Strong[Linearizability] --> Seq[Sequential]
    Seq --> Causal[Causal]
    Causal --> Eventual[Eventual]
```
*Figure: Consistency model spectrum — stronger models imply more constraints.*""",
    "09-transactions": """```mermaid
sequenceDiagram
    participant C as Coordinator
    participant P1 as Participant 1
    participant P2 as Participant 2
    C->>P1: prepare
    C->>P2: prepare
    P1-->>C: vote commit
    P2-->>C: vote commit
    C->>P1: commit
    C->>P2: commit
```
*Figure: Two-phase commit protocol for distributed transactions.*""",
    "10-storage-engines": """```mermaid
flowchart TB
    Write[Write] --> WAL[WAL append]
    WAL --> Mem[Memtable]
    Mem -->|flush| SST[SSTable]
    SST -->|compaction| SST2[Compacted SSTables]
    Read[Read] --> Mem
    Read --> SST
```
*Figure: LSM-tree write path — WAL, memtable, and SSTable compaction.*""",
    "11-distributed-databases": """```mermaid
flowchart TB
    Client[Client] --> Router[Partition Router]
    Router --> Shard1[Shard 1]
    Router --> Shard2[Shard 2]
    Router --> Shard3[Shard 3]
    Shard1 --> Rep1[Replicas]
    Shard2 --> Rep2[Replicas]
```
*Figure: Sharded distributed database with per-partition replication.*""",
    "12-messaging-and-streaming": """```mermaid
flowchart LR
    P[Producer] --> T[Topic]
    T --> P0[Partition 0]
    T --> P1[Partition 1]
    P0 --> CG[Consumer Group]
    P1 --> CG
```
*Figure: Event log with partitions and consumer group parallelism.*""",
    "13-caching": """```mermaid
flowchart TB
    App[Application] --> L1[Local Cache]
    L1 -->|miss| L2[Distributed Cache]
    L2 -->|miss| DB[(Database)]
    DB -->|populate| L2
    L2 --> L1
```
*Figure: Multi-tier cache-aside read path.*""",
    "14-microservices": """```mermaid
flowchart TB
    GW[API Gateway] --> S1[Service A]
    GW --> S2[Service B]
    GW --> S3[Service C]
    S1 --> MQ[Message Bus]
    S2 --> MQ
    S1 --> DB1[(DB A)]
    S2 --> DB2[(DB B)]
```
*Figure: Microservices with gateway, async messaging, and database-per-service.*""",
    "15-api-and-integration-architecture": """```mermaid
flowchart LR
    Client[Client] --> REST[REST API]
    Client --> GRPC[gRPC]
    Client --> GQL[GraphQL]
    REST --> Svc[Backend Services]
    GRPC --> Svc
    GQL --> Svc
```
*Figure: API style tradeoffs — REST, gRPC, and GraphQL integration patterns.*""",
    "16-cloud-architecture": """```mermaid
flowchart TB
    subgraph Region["AWS Region"]
        AZ1[AZ-a]
        AZ2[AZ-b]
        AZ3[AZ-c]
    end
    Edge[CloudFront] --> Region
    Region --> S3[S3]
    Region --> DDB[DynamoDB]
    Region --> Lambda[Lambda]
```
*Figure: Regional AWS deployment across availability zones.*""",
    "17-kubernetes-and-platform-engineering": """```mermaid
flowchart TB
    subgraph CP["Control Plane"]
        API[API Server]
        ETCD[etcd]
        Sched[Scheduler]
    end
    subgraph Nodes["Worker Nodes"]
        K1[kubelet]
        K2[kubelet]
    end
    API --> Sched
    API --> K1
    API --> K2
    ETCD --> API
```
*Figure: Kubernetes control plane and worker node architecture.*""",
    "18-reliability-and-resilience": """```mermaid
flowchart LR
    SLI[SLI Metrics] --> SLO[SLO Target]
    SLO --> EB[Error Budget]
    EB --> Policy[Release Policy]
    Policy --> Deploy[Deployments]
```
*Figure: Reliability engineering loop — SLIs, SLOs, and error budgets.*""",
    "19-observability": """```mermaid
flowchart TB
    Svc[Services] --> Logs[Logs]
    Svc --> Metrics[Metrics]
    Svc --> Traces[Traces]
    Logs --> OTEL[OpenTelemetry Collector]
    Metrics --> OTEL
    Traces --> OTEL
    OTEL --> Backend[Observability Backend]
```
*Figure: Three pillars of observability unified via OpenTelemetry.*""",
    "20-security": """```mermaid
flowchart TB
    User[User] --> IdP[Identity Provider]
    IdP --> Token[JWT / mTLS]
    Token --> GW[Gateway]
    GW --> Policy[Policy Engine]
    Policy --> Svc[Microservice]
    Svc --> KMS[KMS / Secrets]
```
*Figure: Zero-trust request flow — authenticate, authorize, encrypt.*""",
    "21-data-platforms": """```mermaid
flowchart LR
    Ingest[Ingestion] --> Lake[Data Lake]
    Lake --> WH[Warehouse]
    Lake --> Stream[Stream Processing]
    Stream --> Serving[Serving Layer]
    WH --> BI[BI / Analytics]
```
*Figure: Lakehouse architecture — batch and stream paths to analytics.*""",
    "22-ai-distributed-systems": """```mermaid
flowchart TB
    Client[Client] --> GW[Model Gateway]
    GW --> Router[Model Router]
    Router --> GPU1[GPU Pool 1]
    Router --> GPU2[GPU Pool 2]
    GPU1 --> Cache[KV Cache]
```
*Figure: Distributed LLM inference with routing and GPU pools.*""",
    "23-agentic-ai-architecture": """```mermaid
flowchart TB
    User[User] --> Orch[Orchestrator]
    Orch --> Agent[Agent Runtime]
    Agent --> Tools[Tool Registry]
    Agent --> Mem[Memory Store]
    Tools --> AuthZ[Authorization]
    Orch --> Audit[Audit Trail]
```
*Figure: Agentic platform — orchestration, tools, memory, and governance.*""",
    "24-system-design": """```mermaid
flowchart LR
    Req[Requirements] --> Scale[Scale Estimation]
    Scale --> API[API Design]
    API --> Data[Data Model]
    Data --> Arch[Architecture]
    Arch --> Deep[Deep Dives]
    Deep --> Trade[Tradeoffs]
```
*Figure: System design interview methodology — structured progression.*""",
    "25-architecture-leadership": """```mermaid
flowchart TB
    Vision[Architecture Vision] --> Principles[Principles]
    Principles --> ADR[ADRs]
    ADR --> ARB[Architecture Review Board]
    ARB --> Adoption[Organizational Adoption]
```
*Figure: Architecture leadership — from vision to governed adoption.*""",
    "26-cost-and-finops": """```mermaid
flowchart LR
    Usage[Cloud Usage] --> Tag[Tagging / Allocation]
    Tag --> Report[Cost Reports]
    Report --> Optimize[Optimization]
    Optimize --> Policy[FinOps Policy]
```
*Figure: FinOps feedback loop — measure, allocate, optimize.*""",
    "27-production-failures": """```mermaid
flowchart TB
    Incident[Incident] --> Triage[Triage]
    Triage --> Mitigate[Mitigate]
    Mitigate --> PM[Postmortem]
    PM --> Actions[Action Items]
    Actions --> Prevent[Prevention]
```
*Figure: Incident lifecycle — from detection to systemic improvement.*""",
    "28-company-specific-preparation": """```mermaid
flowchart LR
    Research[Company Research] --> Tech[Technical Prep]
    Tech --> Stories[STAR Stories]
    Stories --> Mock[Mock Interviews]
    Mock --> Interview[Interview Day]
```
*Figure: Company-specific interview preparation workflow.*""",
    "29-behavioral-and-leadership": """```mermaid
flowchart TB
    Situation[Situation] --> Task[Task]
    Task --> Action[Action]
    Action --> Result[Result]
    Result --> Lesson[Lessons Learned]
```
*Figure: STAR framework for behavioral interview stories.*""",
    "30-mock-interviews": """```mermaid
flowchart LR
    Problem[Problem Statement] --> Clarify[Clarify]
    Clarify --> Design[Design]
    Design --> Deep[Deep Dive]
    Deep --> Score[Scoring Rubric]
```
*Figure: Mock interview session structure with rubric evaluation.*""",
    "31-reference": """```mermaid
mindmap
  root((Reference))
    Glossary
    Decision Frameworks
    Reading List
    Cheat Sheets
    Question Banks
```
*Figure: Reference materials for rapid review and lookup.*""",
}

CASE_STUDY_EXTRA: dict[str, str] = {
    "dynamodb": """```mermaid
sequenceDiagram
    participant C as Client
    participant D as DynamoDB
    participant S as Stream
    participant L as Lambda
    C->>D: TransactWriteItems
    D-->>C: OK
    D->>S: stream record
    S->>L: trigger
```
*Figure: Write path with DynamoDB Streams triggering downstream processing.*""",
    "kafka": """```mermaid
flowchart LR
    P[Producer] --> B1[Broker 1]
    P --> B2[Broker 2]
    B1 --> ISR[ISR Replicas]
    CG[Consumer Group] --> B1
    CG --> B2
```
*Figure: Kafka broker cluster with ISR replication and consumer groups.*""",
    "s3": """```mermaid
flowchart TB
    Client[Client] --> MPU[Multipart Upload]
    MPU --> O1[Object Part 1]
    MPU --> O2[Object Part 2]
    O1 --> Bucket[S3 Bucket]
    O2 --> Bucket
    Bucket --> Repl[Cross-Region Replication]
```
*Figure: S3 multipart upload and replication topology.*""",
    "netflix": """```mermaid
flowchart TB
    User[User] --> CDN[Open Connect CDN]
    CDN --> Origin[Origin Services]
    Origin --> MS[Microservices]
    MS --> Chaos[Chaos Engineering]
```
*Figure: Netflix control plane vs CDN data plane separation.*""",
    "stripe": """```mermaid
sequenceDiagram
    participant M as Merchant
    participant S as Stripe API
    participant L as Ledger
  participant B as Bank
    M->>S: POST /charges (Idempotency-Key)
    S->>L: append entry
    S->>B: settle
    S-->>M: 200 OK
```
*Figure: Idempotent payment flow with ledger and settlement.*""",
    "global-file-transfer": """```mermaid
flowchart TB
    Partner[Partner] --> Ingest[Ingest Gateway]
    Ingest --> S3[S3 Landing]
    S3 --> EB[EventBridge]
    EB --> SF[Step Functions]
    SF --> Proc[Processing]
```
*Figure: Event-driven enterprise file transfer pipeline on AWS.*""",
    "spanner": """```mermaid
flowchart TB
    Client[Client] --> Paxos[Paxos Group per Tablet]
    Paxos --> TT[TrueTime]
    TT --> Commit[Commit Wait]
```
*Figure: Spanner tablet with Paxos replication and TrueTime commit.*""",
    "cassandra": """```mermaid
flowchart LR
    C[Coordinator] --> N1[Node 1]
    C --> N2[Node 2]
    C --> N3[Node 3]
    N1 -.->|gossip| N2
    N2 -.->|gossip| N3
```
*Figure: Cassandra coordinator write with gossip-based cluster membership.*""",
    "snowflake": """```mermaid
flowchart TB
    Storage[Cloud Storage] --> Compute[Snowflake Compute]
    Compute --> WH[Warehouse Cluster]
    WH --> Query[Query Engine]
    Query --> Result[Results]
```
*Figure: Snowflake storage/compute separation architecture.*""",
    "cloudflare": """```mermaid
flowchart TB
    User[User] --> Edge[Edge PoP]
    Edge --> Cache[Edge Cache]
    Edge --> Origin[Origin Server]
    Edge --> WAF[WAF / DDoS]
```
*Figure: Cloudflare edge-first request path with security layer.*""",
    "uber": """```mermaid
flowchart TB
    Rider[Rider App] --> Dispatch[Dispatch Service]
    Driver[Driver App] --> Dispatch
    Dispatch --> Geo[Geospatial Index]
    Dispatch --> Pricing[Pricing Engine]
```
*Figure: Ride-matching dispatch with geospatial indexing.*""",
    "slack": """```mermaid
flowchart TB
    Client[WebSocket Client] --> GW[Gateway]
    GW --> Channel[Channel Service]
    Channel --> Shard[Database Shard]
    GW --> RT[Real-time Fan-out]
```
*Figure: Slack message path — gateway, sharding, and fan-out.*""",
    "discord": """```mermaid
flowchart TB
    Text[Text Gateway] --> Cassandra[(Cassandra)]
    Voice[Voice UDP] --> SFU[Media SFU]
    Text --> Guild[Guild Router]
```
*Figure: Discord dual-plane architecture — text vs voice.*""",
    "dropbox": """```mermaid
flowchart TB
    Client[Sync Client] --> Block[Block Server]
    Block --> Meta[Metadata Service]
    Block --> Magic[Object Storage]
    Meta --> Cursor[Sync Cursor]
```
*Figure: Dropbox block-level sync and metadata separation.*""",
    "bigtable": """```mermaid
flowchart TB
    Client[Client] --> Master[Master Server]
    Master --> Tablet1[Tablet Server 1]
    Master --> Tablet2[Tablet Server 2]
    Tablet1 --> GFS[Colossus / GFS]
```
*Figure: Bigtable master-tablet-storage layering.*""",
    "agentic-ai-platform": """```mermaid
flowchart TB
    User[User] --> Orch[Agent Orchestrator]
    Orch --> LLM[LLM]
    Orch --> Tools[MCP Tools]
    Orch --> HITL[Human Approval]
    Orch --> Audit[Audit Log]
```
*Figure: Enterprise agentic platform with HITL and audit.*""",
}


def count_mermaid(text: str) -> int:
    return len(FENCE_RE.findall(text))


def insert_after_h1(text: str, block: str) -> str:
    """Insert diagram block after first paragraph following H1."""
    if count_mermaid(text) >= 1:
        return text
    lines = text.split("\n")
    h1_idx = next((i for i, l in enumerate(lines) if l.startswith("# ")), 0)
    # Find first blank line after h1 content paragraph
    insert_at = h1_idx + 1
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    while insert_at < len(lines) and lines[insert_at].strip() != "":
        insert_at += 1
    new_lines = lines[:insert_at] + ["", block, ""] + lines[insert_at:]
    return "\n".join(new_lines)


def append_before_references(text: str, block: str) -> str:
    if block.strip() in text:
        return text
    marker = "## 20. References"
    if marker in text:
        return text.replace(marker, block + "\n\n" + marker)
    return text + "\n\n" + block + "\n"


def fix_overviews() -> int:
    count = 0
    for folder, diagram in OVERVIEW_DIAGRAMS.items():
        path = DOCS / folder / "overview.md"
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = insert_after_h1(original, diagram)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            count += 1
    return count


def fix_case_studies() -> int:
    count = 0
    for name, diagram in CASE_STUDY_EXTRA.items():
        path = CASE_STUDIES / name / "README.md"
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        if count_mermaid(original) >= 2:
            continue
        updated = append_before_references(original, "## Supplementary Diagram\n\n" + diagram)
        path.write_text(updated, encoding="utf-8")
        count += 1
    return count


def fix_interview_docs() -> int:
    extras = {
        "docs/28-company-specific-preparation/adobe.md": """```mermaid
flowchart TB
    Prep[Technical Depth] --> SaaS[Multi-tenant SaaS]
    Prep --> AI[Agentic AI]
    Prep --> Gov[Data Governance]
    SaaS --> Interview[Interview]
    AI --> Interview
    Gov --> Interview
```
*Figure: Adobe interview focus areas — SaaS, AI, and governance.*""",
        "docs/28-company-specific-preparation/amazon-aws.md": """```mermaid
flowchart LR
    LP[Leadership Principles] --> Ops[Operational Excellence]
    Ops --> Design[Simple Designs]
    Design --> Deep[Deep Dives]
```
*Figure: Amazon interview loop — LPs, operations, and first-principles design.*""",
        "docs/28-company-specific-preparation/google.md": """```mermaid
flowchart TB
    Algo[Algorithms] --> DS[Distributed Systems]
    DS --> Scale[Scale Estimation]
    Scale --> Leadership[Leadership]
```
*Figure: Google interview emphasis — algorithms, distributed systems, scale.*""",
        "docs/29-behavioral-and-leadership/enterprise-file-transfer-stories.md": """```mermaid
flowchart LR
    Scale[Scale Challenge] --> DR[Multi-Region DR]
    DR --> SelfService[Self-Service Onboarding]
    SelfService --> AI[AI Operations]
```
*Figure: Enterprise file transfer story themes for behavioral interviews.*""",
        "docs/30-mock-interviews/mock-interview-rubric.md": """```mermaid
flowchart TB
    Req[Requirements 20%] --> Arch[Architecture 25%]
    Arch --> DS[Distributed Reasoning 20%]
    DS --> Ops[Operations 15%]
    Ops --> Comm[Communication 20%]
```
*Figure: Weighted scoring dimensions for principal-level mock interviews.*""",
        "docs/28-company-specific-preparation/microsoft.md": """```mermaid
flowchart TB
    Cloud[Azure / Cloud] --> Enterprise[Enterprise Integration]
    Enterprise --> Security[Security]
    Security --> Leadership[Architecture Leadership]
```
*Figure: Microsoft interview focus — cloud, enterprise, security, leadership.*""",
        "docs/28-company-specific-preparation/nvidia.md": """```mermaid
flowchart TB
    GPU[GPU Infrastructure] --> Inference[Distributed Inference]
    Inference --> Scheduling[Scheduling]
    Scheduling --> Networking[High-Performance Networking]
```
*Figure: NVIDIA interview focus — GPU platforms and inference at scale.*""",
        "docs/28-company-specific-preparation/snowflake-databricks.md": """```mermaid
flowchart TB
    Sep[Storage/Compute Separation] --> Query[Query Execution]
    Query --> Multi[Multi-tenancy]
    Multi --> Cost[Performance and Cost]
```
*Figure: Snowflake/Databricks interview focus — data platform internals.*""",
        "docs/28-company-specific-preparation/openai-anthropic.md": """```mermaid
flowchart TB
    Infra[AI Infrastructure] --> Safety[Safety and Alignment]
    Safety --> Agents[Agent Platforms]
    Agents --> Eval[Evaluation and Observability]
```
*Figure: OpenAI/Anthropic interview focus — AI infra, safety, agents.*""",
        "docs/29-behavioral-and-leadership/star-story-framework.md": """```mermaid
flowchart LR
    S[Situation] --> T[Task]
    T --> A[Action]
    A --> R[Result]
    R --> L[Lessons]
```
*Figure: STAR story structure for behavioral interviews.*""",
        "docs/29-behavioral-and-leadership/leadership-principles.md": """```mermaid
mindmap
  root((Leadership))
    Ownership
    Customer Obsession
    Dive Deep
    Deliver Results
    Earn Trust
    Think Big
```
*Figure: Leadership principles map for principal-level behavioral interviews.*""",
        "docs/30-mock-interviews/distributed-systems-mock.md": """```mermaid
flowchart TB
    F1[Failure Modes] --> F2[Consistency]
    F2 --> F3[Replication]
    F3 --> F4[Operations]
```
*Figure: Distributed systems mock interview depth progression.*""",
        "docs/30-mock-interviews/system-design-mock.md": """```mermaid
flowchart TB
    W1[Week 1-4: Fundamentals] --> W2[Week 5-8: Data]
    W2 --> W3[Week 9-12: Full Mocks]
```
*Figure: 12-week system design mock interview calendar.*""",
        "docs/31-reference/decision-frameworks.md": """```mermaid
flowchart TB
    Problem[Problem] --> CAP[CAP / PACELC]
    CAP --> BuildBuy[Build vs Buy]
    BuildBuy --> TechSelect[Technology Selection]
    TechSelect --> ADR[Document in ADR]
```
*Figure: Decision framework cascade for architecture choices.*""",
    }
    count = 0
    for rel, diagram in extras.items():
        path = ROOT / rel
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        if count_mermaid(original) >= 2:
            continue
        updated = original.rstrip() + "\n\n## Diagram\n\n" + diagram + "\n"
        path.write_text(updated, encoding="utf-8")
        count += 1
    return count


def main() -> None:
    o = fix_overviews()
    c = fix_case_studies()
    i = fix_interview_docs()
    print(f"Updated {o} overviews, {c} case studies, {i} interview/reference docs.")


if __name__ == "__main__":
    main()
