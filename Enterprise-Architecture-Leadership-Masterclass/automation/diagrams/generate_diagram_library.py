#!/usr/bin/env python3
"""
BayLearn Diagram Generation Framework
Generates Mermaid, Draw.io, Markdown, and (optionally) SVG/PNG for the
Enterprise Architecture Leadership Masterclass diagram library.
"""
from __future__ import annotations

import json
import re
import subprocess
import shutil
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS = ROOT / "diagrams"
LIBRARY = ROOT / "diagram-library"
MANIFEST_PATH = DIAGRAMS / "diagram-manifest.json"


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


# ---------------------------------------------------------------------------
# Catalog builders — return list of diagram dicts
# ---------------------------------------------------------------------------

def D(module, category, title, lo, mermaid, lesson=None, lab=None, slides=None,
      workbook=None, aws_icons=None, tags=None, shared_path=None):
    mid = f"m{module}" if module and not str(module).startswith("lab") and module != "cap" else str(module)
    if module == "cap":
        did = f"cap-{category}-{slugify(title)}"
    elif str(module).startswith("lab"):
        did = f"{module}-{category}-{slugify(title)}"
    else:
        did = f"m{int(module):02d}-{category}-{slugify(title)}"
    return {
        "id": did,
        "title": title,
        "category": category,
        "module": f"module-{int(module):02d}" if isinstance(module, int) else module,
        "lesson": lesson,
        "lab": lab,
        "slides": slides or f"slides/{('module-'+f'{int(module):02d}') if isinstance(module, int) else module}/",
        "workbook": workbook,
        "learningObjective": lo,
        "awsIcons": aws_icons or [],
        "tags": tags or [],
        "sharedLibraryPath": shared_path,
        "mermaid": mermaid.strip() + "\n",
    }


def theme_header() -> str:
    return """%%{init: {
  "theme": "base",
  "themeVariables": {
    "primaryColor": "#E6F2FF",
    "primaryTextColor": "#232F3E",
    "primaryBorderColor": "#146EB4",
    "lineColor": "#545B64",
    "secondaryColor": "#F0F7E6",
    "tertiaryColor": "#FFF3E0",
    "background": "#FFFFFF",
    "fontFamily": "Amazon Ember, Helvetica, Arial, sans-serif"
  }
}}%%
"""


def build_catalog() -> list[dict]:
    cat: list[dict] = []
    H = theme_header()

    # ========== MODULE 1 (15+) ==========
    cat += [
        D(1, "concept", "Enterprise Architecture Domains",
          "Map EA domains to NorthStar transformation scope",
          H + """flowchart TB
  subgraph EA["Enterprise Architecture Domains — NorthStar (fictional)"]
    B["Business Architecture"]
    D["Data Architecture"]
    A["Application Architecture"]
    T["Technology Architecture"]
    S["Security Architecture"]
  end
  Strat["Business Strategy"] --> B
  B --> D & A
  A --> T
  B & D & A & T --> S
  S --> Outcomes["Outcomes: Cost · Speed · Risk · Visibility"]
""", lesson="1.1", tags=["ea", "domains"]),
        D(1, "concept", "Architecture Pyramid",
          "Distinguish strategic, segment, and solution architecture",
          H + """flowchart TB
  Strat["Strategic Architecture<br/>Enterprise direction"] --> Seg["Segment / Domain Architecture"]
  Seg --> Sol["Solution Architecture"]
  Sol --> Del["Delivery & Engineering"]
  Strat -.-> Prin["Principles & Guardrails"]
  Prin -.-> Seg & Sol
""", lesson="1.1"),
        D(1, "concept", "Business vs Solution Architecture",
          "Contrast EA leadership with solution delivery architecture",
          H + """flowchart LR
  subgraph EA["Enterprise Architect"]
    E1["Strategy → Priorities"]
    E2["Cross-domain trade-offs"]
    E3["Standards & governance"]
  end
  subgraph SA["Solution Architect"]
    S1["Product / project scope"]
    S2["Design within guardrails"]
    S3["Delivery enablement"]
  end
  EA -->|"Guardrails & ADRs"| SA
  SA -->|"Patterns & feedback"| EA
""", lesson="1.1"),
        D(1, "concept", "Architecture Roles RACI Overview",
          "Show role boundaries across EA, domain, solution, platform",
          H + """flowchart TB
  CIO["CIO / CTO"] --> EA["Lead Enterprise Architect"]
  EA --> DA["Domain Architects"]
  EA --> PA["Platform Architects"]
  DA --> SA["Solution Architects"]
  PA --> SA
  EA --> ARB["Architecture Review Board"]
  ARB --> Dec["Decisions / Exceptions"]
""", lesson="1.2"),
        D(1, "process", "Architecture Governance Flow",
          "Describe how proposals move from intake to decision",
          H + """flowchart LR
  Intake["1 Intake"] --> Align["2 Principle Alignment"]
  Align --> Review["3 ARB / Design Authority"]
  Review --> Dec{"Decision"}
  Dec -->|Approve| Impl["Implement + ADR"]
  Dec -->|Conditional| Cond["Conditions + Re-review"]
  Dec -->|Reject| Alt["Alternatives"]
""", lesson="1.2", tags=["governance"]),
        D(1, "concept", "Architecture Principles Stack",
          "Relate principles to exceptions and metrics",
          H + """flowchart TB
  Mission["Architecture Mission"] --> Prin["Principles 8–10"]
  Prin --> Impl["Implications for Teams"]
  Prin --> Exc["Exception Process"]
  Prin --> Met["Signals / Metrics"]
  Exc --> ARB["ARB Decision"]
""", lesson="1.3"),
        D(1, "concept", "Current vs Target State Arc",
          "Frame transformation as managed transitions",
          H + """flowchart LR
  CS["Current State"] --> T1["Transition A"]
  T1 --> T2["Transition B"]
  T2 --> TS["Target State"]
  CS -.-> Risk["Risk & Debt"]
  TS -.-> Value["Business Value"]
""", lesson="1.1"),
        D(1, "concept", "Decision Hierarchy",
          "Clarify local autonomy vs enterprise decisions",
          H + """flowchart TB
  E["Enterprise Decisions<br/>Standards · Multi-year · Material risk"] --> D["Domain Decisions"]
  D --> L["Local Solution Decisions<br/>Within guardrails"]
  E --> G["Automated Guardrails"]
  G --> L
""", lesson="1.2"),
        D(1, "executive", "Stakeholder Influence Map",
          "Position stakeholders by interest and influence",
          H + """quadrantChart
    title NorthStar Stakeholder Map (fictional)
    x-axis Low Influence --> High Influence
    y-axis Low Interest --> High Interest
    quadrant-1 Manage Closely
    quadrant-2 Keep Informed
    quadrant-3 Monitor
    quadrant-4 Keep Satisfied
    CEO: [0.8, 0.85]
    CIO: [0.75, 0.9]
    CISO: [0.7, 0.8]
    BU President: [0.65, 0.7]
    Platform Lead: [0.55, 0.75]
    Eng Managers: [0.45, 0.6]
""", lesson="1.4"),
        D(1, "process", "Architecture Lifecycle",
          "Show continuous architecture cycle",
          H + """flowchart LR
  Disc["Discover"] --> Assess["Assess"]
  Assess --> Target["Target"]
  Target --> Road["Roadmap"]
  Road --> Gov["Govern"]
  Gov --> Disc
""", lesson="1.1"),
        D(1, "concept", "Federated Operating Model",
          "Illustrate Year-1 hybrid/federated EA operating model",
          H + """flowchart TB
  subgraph Center["Enterprise Architecture Center"]
    EA["Lead EA"]
    Std["Standards · ADRs · ARB"]
  end
  subgraph BUs["Business Units"]
    DA1["Domain Arch — Payments"]
    DA2["Domain Arch — Retail"]
    DA3["Domain Arch — Partners"]
  end
  subgraph Plat["Platform"]
    PA["Platform Architect"]
    GP["Golden Paths"]
  end
  Center --> BUs & Plat
  BUs --> SA["Solution Architects"]
""", lesson="1.2", tags=["operating-model"]),
        D(1, "concept", "Architecture Deliverables Map",
          "Connect weekly artifacts to portfolio outcomes",
          H + """mindmap
  root((EA Deliverables))
    Principles
    Capability Map
    Portfolio TIME
    Target State
    Roadmap
    ADRs
    Exec Memo
""", lesson="1.4"),
        D(1, "concept", "Capability Relationships to Systems",
          "Show capabilities independent of systems",
          H + """flowchart LR
  Cap["Capability:<br/>Customer Onboarding"] --> P["Process"]
  Cap --> Data["Data Objects"]
  Cap --> Sys["Systems / Apps"]
  Cap --> Own["Business Owner"]
  note["Systems change; capability persists"]
""", lesson="1.1"),
        D(1, "concept", "Architecture Layers Stack",
          "Present layered enterprise view",
          H + """block-beta
  columns 1
  block:layers
    BUSINESS[\"Business Outcomes & Capabilities\"]
    APP[\"Applications & Integration\"]
    DATA[\"Data Products & MDM\"]
    TECH[\"Cloud · Platform · Ops\"]
    SEC[\"Security · Resilience · Compliance\"]
  end
""", lesson="1.1"),
        D(1, "executive", "Architecture Value Chain",
          "Tie EA work to measurable business value",
          H + """flowchart LR
  Strat["Strategy"] --> Cap["Capabilities"]
  Cap --> Arch["Architecture Choices"]
  Arch --> Plat["Platforms & Patterns"]
  Plat --> Del["Delivery Speed"]
  Arch --> Risk["Risk Reduction"]
  Del & Risk --> Value["Executive Outcomes"]
""", lesson="1.4"),
        D(1, "process", "Influence Without Authority Loop",
          "Show how EAs create alignment without hierarchy",
          H + """flowchart LR
  Listen["Listen & Diagnose"] --> Frame["Frame Trade-offs"]
  Frame --> Coal["Build Coalition"]
  Coal --> Dec["Decide via ADR/ARB"]
  Dec --> Prove["Prove with Outcomes"]
  Prove --> Listen
""", lesson="1.4"),
    ]

    # ========== MODULE 2 (20+) ==========
    m2 = [
        ("Business Capability Map L1", "concept", """flowchart TB
  subgraph NorthStar["NorthStar L1 Capabilities (fictional)"]
    C1["Customer Management"]
    C2["Payments"]
    C3["Partner Management"]
    C4["Risk & Compliance"]
    C5["Product Management"]
    C6["Data & Analytics"]
    C7["Enterprise Platforms"]
    C8["Workforce"]
  end
"""),
        ("Capability Hierarchy L1-L3", "concept", """flowchart TB
  L1["L1 Customer Management"] --> L2a["L2 Onboarding"]
  L1 --> L2b["L2 Servicing"]
  L2a --> L3a["L3 KYC"]
  L2a --> L3b["L3 Account Opening"]
  L2a --> L3c["L3 Identity Proofing"]
"""),
        ("Capability Heatmap", "executive", """flowchart LR
  subgraph Heat["Maturity Heatmap"]
    R1["Onboarding — 2 Fragile"]
    A1["Payments — 3 Adequate"]
    G1["Ledger — 4 Good"]
  end
  R1 --> X["Invest / Migrate"]
  style R1 fill:#FCE8E6,stroke:#D13212
  style A1 fill:#FFF3E0,stroke:#ED7100
  style G1 fill:#F0F7E6,stroke:#1D8102
"""),
        ("Customer Onboarding Value Stream", "process", """flowchart LR
  A["Acquire"] --> B["Verify Identity"]
  B --> C["Risk Decision"]
  C --> D["Open Account"]
  D --> E["Activate Products"]
  E --> F["Ongoing Service"]
"""),
        ("Payment Processing Value Stream", "process", """flowchart LR
  Init["Initiate Payment"] --> Auth["Authorize"]
  Auth --> Clear["Clear / Settle"]
  Clear --> Recon["Reconcile"]
  Recon --> Report["Report"]
"""),
        ("Partner Integration Value Stream", "process", """flowchart LR
  Req["Partner Request"] --> Contract["Contract & Risk"]
  Contract --> Tech["Technical Onboarding"]
  Tech --> Test["Certification Test"]
  Test --> Live["Production Enablement"]
"""),
        ("Customer Journey Overlay", "dataflow", """flowchart LR
  Aware["Aware"] --> Consider["Consider"]
  Consider --> Onboard["Onboard"]
  Onboard --> Transact["Transact"]
  Transact --> Support["Support"]
  Support --> Grow["Grow / Retain"]
"""),
        ("Stakeholder Network", "concept", """flowchart TB
  EA["Lead EA"] --- CIO["CIO"]
  EA --- CISO["CISO"]
  EA --- BU["BU Sponsors"]
  EA --- Plat["Platform"]
  EA --- Data["Data Leaders"]
  BU --- Prod["Product Owners"]
"""),
        ("Organization vs Capability", "concept", """flowchart LR
  Org["Org Chart<br/>(changes often)"] -.-> Cap["Capability Map<br/>(stable)"]
  Cap --> Invest["Investment Decisions"]
"""),
        ("KPI to Capability Traceability", "process", """flowchart LR
  KPI["KPI: Onboarding Cycle Time"] --> Cap["Capability: Customer Onboarding"]
  Cap --> Arch["Architecture Levers"]
  Arch --> Init["Roadmap Initiatives"]
"""),
        ("Capability Maturity Model", "concept", """flowchart LR
  M1["1 Initial"] --> M2["2 Managed"]
  M2 --> M3["3 Defined"]
  M3 --> M4["4 Measured"]
  M4 --> M5["5 Optimizing"]
"""),
        ("Investment Priority Matrix", "executive", """quadrantChart
    title Capability Investment Priorities
    x-axis Low Effort --> High Effort
    y-axis Low Value --> High Value
    quadrant-1 Strategic Bets
    quadrant-2 Quick Wins
    quadrant-3 Park
    quadrant-4 Foundations
    Onboarding: [0.35, 0.85]
    Integration Hub: [0.7, 0.8]
    Partner Portal: [0.55, 0.75]
    Legacy Batch: [0.8, 0.3]
"""),
        ("Core vs Supporting Capabilities", "concept", """flowchart TB
  Core["Core: Payments · Onboarding · Partner"] 
  Supp["Supporting: HR · ITSM · Finance Ops"]
  Comm["Commodity: Email · Collaboration"]
  Core --> Diff["Differentiate"]
  Supp --> Eff["Efficiency"]
  Comm --> Std["Standardize / Buy"]
"""),
        ("Business Outcome Tree", "executive", """flowchart TB
  Goal["Reduce OpEx 20% + Faster Products"] --> O1["Consolidate Platforms"]
  Goal --> O2["Improve Onboarding"]
  Goal --> O3["Governed AI"]
  O1 --> C1["Integration · Cloud"]
  O2 --> C2["Customer · Data"]
  O3 --> C3["AI Platform"]
"""),
        ("Value Stream to Systems Bridge", "dataflow", """flowchart LR
  VS["Value Stream Step"] --> Cap["Capability"]
  Cap --> App["Applications"]
  Cap --> Int["Integrations"]
  Cap --> Data["Data Products"]
"""),
        ("Incident Response Value Stream", "process", """flowchart LR
  Det["Detect"] --> Tri["Triage"]
  Tri --> Mit["Mitigate"]
  Mit --> Rec["Recover"]
  Rec --> Learn["Learn / Improve"]
"""),
        ("Product Delivery Value Stream", "process", """flowchart LR
  Idea["Idea"] --> Prior["Prioritize"]
  Prior --> Build["Build"]
  Build --> Secure["Secure Review"]
  Secure --> Release["Release"]
  Release --> Measure["Measure"]
"""),
        ("Capability Ownership Model", "concept", """flowchart TB
  Cap["Capability"] --> BO["Business Owner"]
  Cap --> TO["Technical Owner"]
  Cap --> DO["Data Owner"]
  BO & TO & DO --> ADR["Joint ADRs"]
"""),
        ("Strategy to Architecture Cascade", "process", """flowchart TB
  S["Strategic Objectives"] --> O["Outcomes / KPIs"]
  O --> C["Capabilities"]
  C --> A["Architecture Priorities"]
  A --> R["Roadmap Waves"]
"""),
        ("Heatmap Legend and Scoring", "concept", """flowchart LR
  R["1–2 Red: Fragile"] --> A["3 Amber: Adequate"]
  A --> G["4–5 Green: Strong"]
  style R fill:#FCE8E6,stroke:#D13212
  style A fill:#FFF3E0,stroke:#ED7100
  style G fill:#F0F7E6,stroke:#1D8102
"""),
    ]
    for i, (title, catg, body) in enumerate(m2):
        cat.append(D(2, catg, title, f"Apply business architecture visual: {title}", H + body, lesson=f"2.{(i%4)+1}"))

    # ========== MODULE 3 (20+) ==========
    m3 = [
        ("Application Portfolio Overview", "concept", """flowchart TB
  Inv["Application Inventory 50+"] --> Score["Value × Health"]
  Score --> TIME["TIME Disposition"]
  TIME --> Heat["Portfolio Heatmap"]
"""),
        ("TIME Model", "concept", """flowchart LR
  T["Tolerate"] --- I["Invest"]
  I --- M["Migrate"]
  M --- E["Eliminate"]
"""),
        ("TIME Decision Tree", "process", """flowchart TB
  Start["App Assessment"] --> Q1{Strategic Fit High?}
  Q1 -->|Yes| Q2{Health Strong?}
  Q1 -->|No| Q3{Still Required?}
  Q2 -->|Yes| Invest["Invest"]
  Q2 -->|No| Migrate["Migrate / Modernize"]
  Q3 -->|Yes| Tolerate["Tolerate (timebox)"]
  Q3 -->|No| Eliminate["Eliminate"]
"""),
        ("Technology Landscape", "infrastructure", """flowchart TB
  subgraph Stacks["Technology Stacks — NorthStar (fictional)"]
    MF["Mainframe / COBOL"]
    Java["Java / Spring"]
    Dot[".NET"]
    Node["Node / Python"]
    SaaS["SaaS Packaged"]
  end
  MF --> Risk["EOL / Skills Risk"]
  SaaS --> Op["OpEx Concentration"]
"""),
        ("Integration Sprawl Current", "dataflow", """flowchart LR
  A1["App A"] -->|Point-to-point| A2["App B"]
  A1 -->|Files| SFTP1["SFTP Hub East"]
  A2 -->|Files| SFTP2["SFTP Hub West"]
  A3["App C"] -->|DB Link| A4["App D"]
  A1 -->|API ad-hoc| A5["App E"]
"""),
        ("Current Data Flow Customer", "dataflow", """flowchart LR
  Web["Web Portal"] --> CRM["CallCenter CRM"]
  Mobile["Mobile BFF"] --> CRM
  CRM --> C360["Cust360 MDM"]
  C360 --> Replica["Cust360 Replica EU"]
  C360 --> Lake["DataLake Alpha"]
"""),
        ("Risk Heatmap Top 10", "security", """flowchart TB
  R1["1 Fragmented Identity"]
  R2["2 Dual SFTP Platforms"]
  R3["3 EOL Mainstreet Core"]
  R4["4 Weak DR"]
  R5["5 Ungoverned Cloud Accounts"]
  style R1 fill:#FCE8E6,stroke:#D13212
  style R2 fill:#FCE8E6,stroke:#D13212
  style R3 fill:#FFF3E0,stroke:#ED7100
"""),
        ("Technical Debt Categories", "concept", """mindmap
  root((Technical Debt))
    Obsolescence
    Concentration
    Operational Burden
    Security Gaps
    Resilience Gaps
    Skills
"""),
        ("Legacy System Cluster", "infrastructure", """flowchart TB
  subgraph Acquired["Acquired Estates"]
    MS["Mainstreet Core"]
    EU["Europa Cards Core"]
    Asia["Asia Partner Hub"]
  end
  MS & EU & Asia --> Dup["Duplicate Capabilities"]
"""),
        ("Dependency Graph Sample", "dataflow", """flowchart LR
  Pay["PulsePay Gateway"] --> Ledger["LedgerOne"]
  Pay --> Fraud["FraudShield"]
  Orbit["Orbit Onboarding"] --> KYC["KYC Studio"]
  Orbit --> C360["Cust360"]
  Partner["PartnerLink"] --> SFTP["SFTP Hubs"]
"""),
        ("Application Ownership Matrix View", "concept", """flowchart TB
  App["Application"] --> BO["Business Owner"]
  App --> TO["Technical Owner"]
  App --> Cap["Primary Capability"]
  App --> Crit["Criticality"]
"""),
        ("Discovery Methods", "process", """flowchart LR
  Int["Interviews"] --> Syn["Synthesis"]
  Doc["Docs Review"] --> Syn
  Inv["Inventory"] --> Syn
  Flow["Data-flow Analysis"] --> Syn
  Syn --> Findings["Executive Findings"]
"""),
        ("Business Value vs Tech Health", "executive", """quadrantChart
    title Portfolio Value vs Health
    x-axis Poor Health --> Strong Health
    y-axis Low Value --> High Value
    quadrant-1 Invest
    quadrant-2 Migrate
    quadrant-3 Eliminate
    quadrant-4 Tolerate
    PulsePay: [0.7, 0.9]
    Mainstreet: [0.2, 0.8]
    SFTP East: [0.35, 0.4]
    Loyalty: [0.55, 0.25]
"""),
        ("EOL Technology Timeline", "process", """timeline
    title End-of-Life Pressure
    2025 : Mainstreet components
    2026 : Legacy API Gateway
    2027 : Replica MDM EU
    2028 : Selected batch platforms
"""),
        ("Duplicate Capability Detection", "concept", """flowchart LR
  Cap["Capability: File Transfer"] --> S1["SFTP Hub East"]
  Cap --> S2["SFTP Hub West"]
  Cap --> S3["PartnerFile Dropzone"]
  S1 & S2 & S3 --> Consol["Consolidate"]
"""),
        ("Current Network Conceptual", "infrastructure", """flowchart TB
  OnPrem["On-Prem DC"] --- Hybrid["Hybrid Links"]
  Hybrid --- AWS["AWS Accounts (sprawl)"]
  Hybrid --- Azure["Azure (limited)"]
  AWS --> Ungov["Weak Guardrails"]
"""),
        ("Security Risk Overlay", "security", """flowchart TB
  Apps["Apps with High Security Risk"] --> Id["Inconsistent Identity"]
  Apps --> Enc["Uneven Encryption"]
  Apps --> Priv["Excess Privilege"]
"""),
        ("Cost Concentration View", "executive", """flowchart LR
  Cost["Annual Run Cost"] --> Top["Top 10 Apps ~ majority"]
  Top --> Action["TIME + Platform Shift"]
"""),
        ("Executive Findings Storyboard", "executive", """flowchart LR
  F1["Fragmentation"] --> F2["Risk"]
  F2 --> F3["Cost"]
  F3 --> F4["Ask: Fund Waves"]
"""),
        ("Assessment to Roadmap Handoff", "process", """flowchart LR
  Assess["Current-State Assessment"] --> Debt["Debt Register"]
  Assess --> TIME["TIME"]
  Debt & TIME --> M4["Module 4 Target & Roadmap"]
"""),
    ]
    for i, (title, catg, body) in enumerate(m3):
        cat.append(D(3, catg, title, f"Assess current estate: {title}", H + body, lesson=f"3.{(i%4)+1}", lab="lab-03"))

    return cat  # extended in extend_catalog


def extend_catalog(cat: list[dict]) -> list[dict]:
    """Modules 4–10, labs, capstone — appended for file size management."""
    H = theme_header()

    # MODULE 4
    m4 = [
        ("Target State Vision", "executive", """flowchart TB
  Vision["NorthStar Target Vision (fictional)"] --> Cap["Strategic Capabilities"]
  Vision --> Plat["Shared Platforms"]
  Vision --> Cloud["Governed Cloud"]
  Vision --> AI["Governed AI"]
"""),
        ("Modernization 7 Rs", "concept", """flowchart LR
  Rehost --> Replatform --> Refactor
  Replace --> Retire
  Retain --> Consolidate
"""),
        ("Retain Replace Consolidate Retire", "process", """flowchart TB
  Port["Portfolio"] --> R1["Retain"]
  Port --> R2["Replace"]
  Port --> R3["Consolidate"]
  Port --> R4["Retire"]
"""),
        ("Three Transition States", "concept", """flowchart LR
  CS["Current"] --> TA["Transition A<br/>Guardrails + Hub"]
  TA --> TB["Transition B<br/>Platform Scale"]
  TB --> TS["Target<br/>Standardized"]
"""),
        ("Migration Waves 24 Month", "process", """timeline
    title 24-Month Transformation Waves
    section Phase 0
      Foundation : Guardrails : Identity : Logging
    section Phase 1
      Wave 1 : Integration Hub : Onboarding data
    section Phase 2
      Wave 2 : Platform golden paths
    section Phase 3
      Wave 3 : AI + optimize cost
"""),
        ("Value versus Risk Matrix", "executive", """quadrantChart
    title Value vs Risk Reduction
    x-axis Low Risk Reduction --> High Risk Reduction
    y-axis Low Value --> High Value
    quadrant-1 Do First
    quadrant-2 Value Plays
    quadrant-3 Later
    quadrant-4 Risk Must-Dos
    Integration Hub: [0.75, 0.85]
    DR Uplift: [0.9, 0.7]
    AI Assistant: [0.4, 0.65]
"""),
        ("Coexistence Pattern", "infrastructure", """flowchart LR
  Legacy["Legacy Core"] <-->|Sync / Anti-corruption| Hub["Integration Hub"]
  Hub <--> Modern["Modern Services"]
"""),
        ("Dependency-Based Sequencing", "process", """flowchart TB
  Id["Identity Standard"] --> Apps["App Migrations"]
  Log["Central Logging"] --> Apps
  Hub["Integration Hub"] --> Partner["Partner Onboarding"]
  Hub --> Pay["Payment Events"]
"""),
        ("Future Capability Map", "concept", """flowchart TB
  subgraph Target Caps
    Onb["Onboarding — Strengthened"]
    Pay["Payments — Event-driven"]
    Part["Partner — API-first"]
    Plat["Platform — Golden paths"]
  end
"""),
        ("Business Transformation Overlay", "executive", """flowchart LR
  Cost["-20% OpEx"] --- Speed["Faster Digital Products"]
  Speed --- Trust["Resilience & Compliance"]
  Trust --- Vis["Exec Visibility"]
"""),
        ("Cloud Migration Context", "aws", """flowchart LR
  OnPrem["On-Prem"] -->|Migrate waves| LZ["AWS Landing Zone"]
  LZ --> Plat["Platform Services"]
""", ["AWS Organizations", "IAM"]),
        ("Architecture Roadmap Swimlanes", "process", """flowchart TB
  subgraph Business
    B1["Onboarding KPI"]
  end
  subgraph Platform
    P1["Landing Zone"]
    P2["Integration Hub"]
  end
  subgraph Security
    S1["Identity"]
    S2["DR"]
  end
  B1 --- P2
  P1 --> P2
  S1 --> P1
"""),
        ("Interim Controls During Transition", "security", """flowchart LR
  Dual["Dual-run Period"] --> Ctrl["Compensating Controls"]
  Ctrl --> Mon["Extra Monitoring"]
  Ctrl --> Exc["Time-boxed Exceptions"]
"""),
        ("Target Application Architecture", "concept", """flowchart TB
  Exp["Experience Apps"] --> API["API Platform"]
  API --> Dom["Domain Services"]
  Dom --> Data["Data Products"]
  Dom --> Events["Event Backbone"]
"""),
        ("Funding Logic Phases", "executive", """flowchart LR
  P0["Fund Foundation"] --> V1["Value Wave 1"]
  V1 --> V2["Value Wave 2"]
  V2 --> Opt["Optimize / AI"]
"""),
        ("Assumptions and Constraints Board", "concept", """flowchart TB
  A["Assumptions"] --> D["Decisions"]
  C["Constraints"] --> D
  D --> R["Roadmap"]
"""),
        ("Wave Exit Criteria", "process", """flowchart LR
  Wave["Wave N"] --> Exit{"Exit Criteria Met?"}
  Exit -->|Yes| Next["Wave N+1"]
  Exit -->|No| Fix["Remediate"]
"""),
        ("Platform Before Products", "concept", """flowchart LR
  Guard["Guardrails"] --> GP["Golden Paths"]
  GP --> Prod["Product Acceleration"]
"""),
        ("Executive Roadmap One-Pager", "executive", """flowchart TB
  Now["Now: Risk & Cost Truth"] --> Next["Next: Platforms"]
  Next --> Later["Later: Scale & AI"]
"""),
        ("Target State Principles Link", "concept", """flowchart LR
  Prin["Target Principles"] --> Pat["Patterns"]
  Pat --> Std["Standards"]
  Std --> Exc["Exceptions"]
"""),
    ]
    for i, item in enumerate(m4):
        title, catg, body = item[0], item[1], item[2]
        icons = item[3] if len(item) > 3 else []
        cat.append(D(4, catg, title, f"Design target-state: {title}", H + body, lesson=f"4.{(i%4)+1}", lab="lab-04", aws_icons=icons))

    # MODULE 5 — Cloud (25+) with AWS icons listed
    m5_specs = [
        ("AWS Organizations Structure", "aws", ["AWS Organizations", "IAM"], """flowchart TB
  subgraph Org["AWS Organizations"]
    Mgmt["Management Account"]
    Sec["Security / Audit OU"]
    Shared["Shared Services OU"]
    Work["Workloads OU"]
    Sand["Sandbox OU"]
  end
  Mgmt --> Sec & Shared & Work & Sand
"""),
        ("Landing Zone Conceptual", "aws", ["AWS Organizations", "IAM", "CloudTrail", "AWS Config"], """flowchart TB
  LZ["Landing Zone"] --> Id["Identity Center / IAM"]
  LZ --> Log["Central Logging"]
  LZ --> Net["Network Baseline"]
  LZ --> Guard["Guardrails / SCPs"]
"""),
        ("Multi-Account Strategy", "infrastructure", ["AWS Organizations"], """flowchart LR
  Dev["Dev Account"] --> Test["Test Account"]
  Test --> Prod["Prod Account"]
  Shared["Shared Services"] --- Dev & Test & Prod
"""),
        ("Shared Services Account", "aws", ["Amazon S3", "AWS Lambda", "AWS Systems Manager"], """flowchart TB
  Shared["Shared Services Account"] --> Art["Artifacts / Params"]
  Shared --> Log["Log Archive"]
  Shared --> Net["Network Hub"]
"""),
        ("IAM Least Privilege Pattern", "security", ["IAM", "AWS KMS"], """flowchart LR
  User["Human / Role"] --> IAM["IAM Policies"]
  IAM --> Res["AWS Resources"]
  IAM --> KMS["KMS Key Policies"]
"""),
        ("CloudTrail Central Audit", "aws", ["AWS CloudTrail", "Amazon S3", "Amazon CloudWatch"], """flowchart LR
  Acc["Member Accounts"] -->|Org Trail| CT["CloudTrail"]
  CT --> S3["S3 Log Bucket"]
  CT --> CW["CloudWatch Logs"]
"""),
        ("Central Logging Architecture", "infrastructure", ["Amazon S3", "Amazon CloudWatch", "AWS KMS"], """flowchart LR
  App["Apps / Accounts"] --> CW["CloudWatch Logs"]
  App --> CT["CloudTrail"]
  CW & CT --> Arch["S3 Log Archive<br/>KMS Encrypted"]
"""),
        ("Terraform Apply Flow", "process", ["AWS Systems Manager"], """flowchart LR
  Code["Terraform Code"] --> Plan["terraform plan"]
  Plan --> Apply["terraform apply"]
  Apply --> Tag["Tagged Lab Resources"]
  Apply --> SSM["SSM Parameter Store"]
"""),
        ("Platform Engineering Model", "concept", ["Amazon API Gateway", "AWS Lambda"], """flowchart TB
  Dev["Developers"] --> IDP["Internal Developer Platform"]
  IDP --> GP["Golden Paths"]
  GP --> AWS["AWS Accounts via Guardrails"]
"""),
        ("Golden Path Self-Service", "aws", ["Amazon API Gateway", "AWS Lambda", "Amazon DynamoDB", "AWS Systems Manager"], """flowchart LR
  Dev["Developer"] --> APIGW["API Gateway"]
  APIGW --> L["Lambda"]
  L --> DDB["DynamoDB"]
  L --> SSM["Parameter Store"]
"""),
        ("Cloud Governance Guardrails", "process", ["AWS Organizations", "AWS Config", "AWS Budgets"], """flowchart TB
  SCP["SCPs"] --> Acc["Accounts"]
  Config["AWS Config"] --> Acc
  Budgets["AWS Budgets"] --> Acc
"""),
        ("FinOps Feedback Loop", "executive", ["AWS Budgets", "Amazon CloudWatch"], """flowchart LR
  Tag["Tagging"] --> Alloc["Cost Allocation"]
  Alloc --> Budget["Budgets / Alerts"]
  Budget --> Act["Architecture Action"]
  Act --> Tag
"""),
        ("Developer Platform Layers", "concept", [], """flowchart TB
  UX["Developer UX"] --> Paths["Golden Paths"]
  Paths --> Comp["Platform Capabilities"]
  Comp --> Cloud["Cloud Foundations"]
"""),
        ("Cloud Architecture Layers", "infrastructure", ["Amazon VPC", "IAM"], """flowchart TB
  Edge["Edge / DNS"] --> Net["Network"]
  Net --> Comp["Compute / App"]
  Comp --> Data["Data"]
  Net & Comp & Data --> Sec["Security Controls"]
"""),
        ("Account Vending Conceptual", "process", ["AWS Organizations"], """flowchart LR
  Req["Request Account"] --> Approve["Approve"]
  Approve --> Prov["Provision Baseline"]
  Prov --> Handoff["Handoff to Team"]
"""),
        ("Tagging Standard Model", "concept", ["AWS Budgets"], """flowchart TB
  Res["Resource"] --> Tags["Project · Course · Module · Student · Env · Expiration"]
"""),
        ("Budget Alert Flow", "aws", ["AWS Budgets", "Amazon SNS"], """flowchart LR
  Spend["Spend"] --> Budget["AWS Budget"]
  Budget -->|Threshold| SNS["SNS Alert"]
  SNS --> Owner["Account Owner"]
"""),
        ("Lab 5 Platform Foundation", "aws", ["IAM", "Amazon S3", "AWS CloudTrail", "Amazon CloudWatch", "AWS Budgets", "Amazon DynamoDB", "AWS Lambda", "Amazon API Gateway", "AWS Systems Manager"], """flowchart TB
  subgraph Lab5["Lab 5 — Platform Foundation"]
    APIGW["API Gateway"] --> L["Lambda"]
    L --> DDB["DynamoDB"]
    L --> SSM["SSM Params"]
    CT["CloudTrail"] --> S3["S3 Audit"]
    B["Budgets"] --> Alert["Alert"]
  end
"""),
        ("Hybrid Cloud Placement", "concept", [], """flowchart LR
  OnPrem["On-Prem (retain)"] --> Criteria["Placement Criteria"]
  Criteria --> AWS["AWS (default modern)"]
  Criteria --> SaaS["SaaS (buy)"]
"""),
        ("Concentration Risk View", "executive", [], """flowchart TB
  Single["Single Cloud Concentration"] --> Mit["Mitigations: Portable patterns · Exit criteria · Critical DR"]
"""),
        ("Workload Placement Decision", "process", [], """flowchart TB
  WL["Workload"] --> Q{Latency · Data · Skills · Cost}
  Q --> Place["Place: AWS / On-Prem / SaaS"]
"""),
        ("SCP Deny Dangerous Services", "security", ["AWS Organizations"], """flowchart LR
  Org["Organizations"] --> SCP["SCP Guardrails"]
  SCP --> Deny["Deny high-risk unmanaged patterns"]
"""),
        ("Config Conformance Pack Concept", "aws", ["AWS Config"], """flowchart LR
  Res["Resources"] --> Config["AWS Config"]
  Config --> Rule["Rules / Conformance"]
  Rule --> Rem["Remediation / Ticket"]
"""),
        ("Platform Capability Map", "concept", [], """mindmap
  root((Platform Capabilities))
    Identity
    Networking
    Observability
    CI/CD Baseline
    Secrets
    FinOps
"""),
        ("Build vs Buy Platform ADR", "process", [], """flowchart TB
  Need["Platform Need"] --> Opt["Build · Buy · Reuse"]
  Opt --> ADR["ADR"]
"""),
    ]
    for i, (title, catg, icons, body) in enumerate(m5_specs):
        cat.append(D(5, catg, title, f"Cloud/platform strategy: {title}", H + body,
                     lesson=f"5.{(i%4)+1}", lab="lab-05", aws_icons=icons))

    # MODULE 6 Integration (25+)
    m6 = [
        ("Integration Reference Architecture", ["Amazon API Gateway", "AWS Lambda", "Amazon EventBridge", "Amazon SQS", "AWS Step Functions", "Amazon S3", "Amazon DynamoDB", "Amazon SNS"],
         """flowchart TB
  Clients["Clients / Partners"] --> APIGW["Amazon API Gateway"]
  APIGW --> Lapi["AWS Lambda — API"]
  Lapi --> EB["Amazon EventBridge"]
  EB --> SQS["Amazon SQS"]
  SQS --> Lproc["AWS Lambda — Processors"]
  Lproc --> DDB["Amazon DynamoDB"]
  S3["Amazon S3 Batches"] --> SF["AWS Step Functions"]
  SF --> Lval["Validate / Route"]
  Lproc --> SNS["Amazon SNS Notify"]
"""),
        ("REST API Request Flow", ["Amazon API Gateway", "AWS Lambda", "Amazon DynamoDB"],
         """sequenceDiagram
  participant C as Client
  participant A as API Gateway
  participant L as Lambda
  participant D as DynamoDB
  C->>A: HTTPS request
  A->>L: Invoke
  L->>D: Get/Put item
  D-->>L: Result
  L-->>A: JSON response
  A-->>C: 200 OK
"""),
        ("Payment Event Flow", ["Amazon EventBridge", "Amazon SQS", "AWS Lambda", "Amazon SNS"],
         """flowchart LR
  Pay["Payment Service"] -->|event| EB["EventBridge"]
  EB --> SQS["SQS"]
  SQS --> L["Lambda"]
  L --> SNS["SNS Notification"]
"""),
        ("Partner File Ingest Simulated", ["Amazon S3", "AWS Step Functions", "AWS Lambda"],
         """flowchart LR
  Partner["Partner File"] --> S3["S3 Landing"]
  S3 --> SF["Step Functions"]
  SF --> Val["Validate"]
  Val --> Route["Route / Store Status"]
"""),
        ("Batch Regulatory Pipeline", ["Amazon S3", "AWS Step Functions", "Amazon DynamoDB"],
         """flowchart LR
  Batch["Daily Batch"] --> S3["S3"]
  S3 --> SF["Step Functions"]
  SF --> Status["DynamoDB Status"]
"""),
        ("Pattern Selection Matrix Visual", [],
         """flowchart TB
  Need["Integration Need"] --> P{Latency · Coupling · Volume}
  P --> API["Sync API"]
  P --> Event["Events"]
  P --> Queue["Queues"]
  P --> File["Files / Batch"]
"""),
        ("Sync vs Async Trade-offs", [],
         """flowchart LR
  Sync["Synchronous API<br/>Simple · Coupling"] --- Async["Async Events/Queues<br/>Resilience · Complexity"]
"""),
        ("EventBridge Fan-out", ["Amazon EventBridge", "AWS Lambda"],
         """flowchart TB
  Prod["Producer"] --> EB["EventBridge"]
  EB --> R1["Rule → Fraud"]
  EB --> R2["Rule → Analytics"]
  EB --> R3["Rule → Notify"]
"""),
        ("SQS Competing Consumers", ["Amazon SQS", "AWS Lambda"],
         """flowchart LR
  Q["SQS Queue"] --> C1["Consumer 1"]
  Q --> C2["Consumer 2"]
  Q --> C3["Consumer 3"]
"""),
        ("SNS Pub Sub Notifications", ["Amazon SNS", "Amazon SQS"],
         """flowchart TB
  Pub["Publisher"] --> SNS["SNS Topic"]
  SNS --> E1["Email"]
  SNS --> Q["SQS Subscriber"]
  SNS --> L["Lambda"]
"""),
        ("Step Functions State Machine", ["AWS Step Functions", "AWS Lambda"],
         """stateDiagram-v2
  [*] --> Validate
  Validate --> Route: OK
  Validate --> Quarantine: Fail
  Route --> Notify
  Notify --> [*]
  Quarantine --> [*]
"""),
        ("API Gateway Lambda DynamoDB", ["Amazon API Gateway", "AWS Lambda", "Amazon DynamoDB"],
         """flowchart LR
  C["Client"] --> A["API Gateway"]
  A --> L["Lambda"]
  L --> D["DynamoDB"]
"""),
        ("Transfer Family Conceptual Optional", ["AWS Transfer Family", "Amazon S3"],
         """flowchart LR
  Partner["SFTP Client"] --> TF["AWS Transfer Family<br/>(optional / cost)"]
  TF --> S3["S3"]
  note["Labs simulate with S3 put"]
"""),
        ("Microservices vs Modular Monolith", [],
         """flowchart LR
  MM["Modular Monolith"] --- MS["Microservices"]
  MM --> When1["Clear module boundaries · smaller team"]
  MS --> When2["Independent scale · strong platform"]
"""),
        ("Bounded Context Map", [],
         """flowchart TB
  subgraph Payments
    P1["Accounts"]
    P2["Ledger"]
  end
  subgraph Customer
    C1["Profile"]
    C2["Onboarding"]
  end
  Payments <-.->|Events| Customer
"""),
        ("Data Product Ownership", [],
         """flowchart LR
  Dom["Domain Team"] --> DP["Data Product"]
  DP --> Contr["Contracts / Quality"]
  DP --> Cons["Consumers"]
"""),
        ("Lakehouse Conceptual", ["Amazon S3", "AWS Glue", "Amazon Athena"],
         """flowchart LR
  Src["Sources"] --> S3["S3 Lake"]
  S3 --> Glue["Glue Catalog"]
  Glue --> Athena["Athena / Analytics"]
"""),
        ("MDM Flow", [],
         """flowchart LR
  Sys["Source Systems"] --> MDM["Master Data Services"]
  MDM --> Gold["Golden Record"]
  Gold --> Cons["Downstream"]
"""),
        ("Failure Handling Dead Letter", ["Amazon SQS", "Amazon CloudWatch"],
         """flowchart LR
  Q["SQS"] --> L["Lambda"]
  L -->|fail| DLQ["DLQ"]
  DLQ --> Alarm["CloudWatch Alarm"]
"""),
        ("Idempotency Pattern", ["Amazon DynamoDB", "AWS Lambda"],
         """flowchart LR
  Ev["Event"] --> L["Lambda"]
  L --> DDB["Idempotency Table"]
  DDB -->|duplicate| Skip["Skip"]
  DDB -->|new| Proc["Process"]
"""),
        ("Partner Onboarding Sequence", ["Amazon API Gateway", "AWS Step Functions"],
         """sequenceDiagram
  participant P as Partner
  participant A as API
  participant S as Step Functions
  P->>A: Register
  A->>S: Start onboarding
  S-->>P: Pending certification
  S->>S: Validate artifacts
  S-->>P: Enabled
"""),
        ("Notification Workflow", ["Amazon SNS", "Amazon EventBridge"],
         """flowchart LR
  Ev["Domain Event"] --> EB["EventBridge"]
  EB --> SNS["SNS"]
  SNS --> Chan["Email / SMS / Webhook"]
"""),
        ("Analytics Pipeline Tap", ["Amazon EventBridge", "Amazon S3"],
         """flowchart LR
  EB["EventBridge"] --> Firehose["Stream/Buffer"]
  Firehose --> S3["S3 Analytics Zone"]
"""),
        ("Lab 6 Expected Final Architecture", ["Amazon API Gateway", "AWS Lambda", "Amazon EventBridge", "Amazon SQS", "AWS Step Functions", "Amazon S3", "Amazon DynamoDB", "Amazon SNS"],
         """flowchart TB
  subgraph Final["Lab 6 Final"]
    APIGW --> L1
    L1 --> EB
    EB --> SQS --> L2 --> DDB
    S3 --> SF --> L3
    L2 --> SNS
  end
"""),
        ("Integration Governance Overlay", [],
         """flowchart TB
  Std["API & Event Standards"] --> Hub["Integration Hub"]
  Hub --> Exc["Exceptions via ARB"]
"""),
    ]
    for i, item in enumerate(m6):
        title, icons, body = item[0], item[1], item[2]
        catg = "sequence" if body.strip().startswith("sequenceDiagram") or body.strip().startswith("stateDiagram") else "aws"
        if not icons:
            catg = "concept" if "Trade" in title or "vs" in title or "Bounded" in title or "Product" in title or "Governance" in title else catg
        if "Lakehouse" in title or "MDM" in title or "Analytics" in title:
            catg = "dataflow"
        cat.append(D(6, catg, title, f"Integration/data architecture: {title}", H + body,
                     lesson=f"6.{(i%4)+1}", lab="lab-06", aws_icons=icons))

    return cat


def extend_catalog_security_ai_gov_cap(cat: list[dict]) -> list[dict]:
    H = theme_header()

    # MODULE 7 Security (25+)
    m7 = [
        ("Zero Trust Overview", ["IAM", "Amazon VPC"], """flowchart LR
  User["User / Service"] --> Verify["Verify Explicitly"]
  Verify --> Least["Least Privilege"]
  Least --> Assume["Assume Breach"]
  Assume --> Monitor["Continuous Monitoring"]
"""),
        ("Defense in Depth Layers", ["AWS WAF", "IAM", "AWS KMS"], """flowchart TB
  Edge["Edge WAF / Shield"] --> Net["Network Segmentation"]
  Net --> Id["Identity"]
  Id --> App["App Controls"]
  App --> Data["Data Encryption"]
"""),
        ("Trust Boundaries", ["Amazon API Gateway", "AWS Lambda", "Amazon DynamoDB"], """flowchart TB
  subgraph Public["Untrusted"]
    Client
  end
  subgraph Edge["Edge Trust"]
    APIGW["API Gateway"]
  end
  subgraph App["App Trust"]
    L["Lambda"]
  end
  subgraph Data["Data Trust"]
    DDB["DynamoDB"]
    KMS["KMS"]
  end
  Client --> APIGW --> L --> DDB
  L --> KMS
"""),
        ("STRIDE Threat Overlay", [], """flowchart TB
  S["Spoofing"] --- T["Tampering"]
  R["Repudiation"] --- I["Info Disclosure"]
  D["DoS"] --- E["Elevation"]
"""),
        ("IAM Role Assumption", ["IAM"], """sequenceDiagram
  participant W as Workload
  participant I as IAM
  participant R as Resource
  W->>I: AssumeRole
  I-->>W: Temp creds
  W->>R: Signed request
"""),
        ("KMS Encryption Envelope", ["AWS KMS", "Amazon S3"], """flowchart LR
  App["App"] --> KMS["KMS"]
  KMS --> DEK["Data Key"]
  DEK --> S3["Encrypted Object S3"]
"""),
        ("Secrets Manager Usage", ["AWS Secrets Manager", "AWS Lambda"], """flowchart LR
  L["Lambda"] --> Sec["Secrets Manager"]
  Sec --> Rot["Rotation"]
"""),
        ("S3 Versioning and Replication", ["Amazon S3", "AWS KMS"], """flowchart LR
  P["Primary Bucket"] -->|Versioning| V["Object Versions"]
  P -->|Replication optional| S["Secondary Bucket"]
"""),
        ("CloudWatch Alarms Loop", ["Amazon CloudWatch", "Amazon SNS"], """flowchart LR
  Metric["Metric"] --> Alarm["CloudWatch Alarm"]
  Alarm --> SNS["SNS"]
  SNS --> OnCall["Responder"]
"""),
        ("RTO RPO Targets", [], """flowchart TB
  Biz["Business Impact"] --> RTO["RTO Target"]
  Biz --> RPO["RPO Target"]
  RTO & RPO --> Strat["Recovery Strategy"]
"""),
        ("Multi-AZ vs Multi-Region", ["Amazon S3", "Amazon DynamoDB"], """flowchart LR
  AZ["Multi-AZ<br/>Default resilience"] --- Reg["Multi-Region<br/>Higher cost/complexity"]
"""),
        ("Backup and Restore Drill", ["Amazon S3", "Amazon CloudWatch"], """flowchart LR
  Backup["Backup"] --> Drill["Restore Drill"]
  Drill --> Evidence["Evidence / Report"]
"""),
        ("DR Runbook Flow", [], """flowchart TB
  Detect["Detect Failure"] --> Declare["Declare Incident"]
  Declare --> Failover["Failover Steps"]
  Failover --> Validate["Validate"]
  Validate --> Comm["Communicate"]
"""),
        ("Control Evidence Matrix Visual", [], """flowchart LR
  Risk["Risk"] --> Control["Control"]
  Control --> Evidence["Evidence"]
  Evidence --> Audit["Audit Ready"]
"""),
        ("Network Segmentation Conceptual", ["Amazon VPC"], """flowchart TB
  Pub["Public Subnet"] --> Priv["Private Subnet"]
  Priv --> Data["Data Subnet"]
"""),
        ("Incident Response Swimlane", [], """flowchart LR
  Sec["Security"] --> Triage
  Plat["Platform"] --> Triage
  Triage --> Mitigate --> Recover
"""),
        ("Lab 7 Secure Platform", ["IAM", "AWS KMS", "Amazon S3", "Amazon CloudWatch"], """flowchart TB
  subgraph Lab7
    IAM --> App
    App --> KMS
    App --> S3v["S3 Versioned"]
    CW["CloudWatch Alarms"]
  end
"""),
        ("Data Classification Overlay", [], """flowchart LR
  Pub["Public"] --> Int["Internal"]
  Int --> Conf["Confidential"]
  Conf --> Res["Restricted"]
"""),
        ("Third Party Risk Path", [], """flowchart LR
  Vendor["Vendor"] --> Assess["Risk Assess"]
  Assess --> Controls["Controls / Contracts"]
  Controls --> Monitor["Ongoing Monitor"]
"""),
        ("Security Monitoring Stack", ["AWS CloudTrail", "Amazon CloudWatch", "AWS Config"], """flowchart TB
  CT["CloudTrail"] --> SIEM["Detect / Alert"]
  CW["CloudWatch"] --> SIEM
  Config["Config"] --> SIEM
"""),
        ("Compensating Controls", [], """flowchart TB
  Gap["Control Gap"] --> Comp["Compensating Control"]
  Comp --> Expiry["Time-boxed Review"]
"""),
        ("Encryption In Transit At Rest", ["AWS KMS", "Amazon API Gateway"], """flowchart LR
  Client -->|TLS| APIGW
  APIGW --> App
  App -->|KMS| Data["Data at Rest"]
"""),
        ("Failure Injection Learning", ["Amazon CloudWatch"], """flowchart LR
  Fail["Inject Failure"] --> Observe["Observe Alarms"]
  Observe --> Learn["Improve Design"]
"""),
        ("Recovery Test Report Flow", [], """flowchart LR
  Plan["Test Plan"] --> Exec["Execute"]
  Exec --> Results["Results"]
  Results --> Actions["Actions"]
"""),
        ("Security Architecture Executive", "executive_override", """flowchart TB
  Trust["Zero Trust Direction"] --> Id["Identity First"]
  Trust --> Data["Protect Data"]
  Trust --> Det["Detect & Recover"]
"""),
    ]
    for i, item in enumerate(m7):
        title, icons, body = item[0], item[1], item[2]
        catg = "executive" if icons == "executive_override" or title.endswith("Executive") else (
            "sequence" if body.strip().startswith("sequenceDiagram") else "security"
        )
        if icons == "executive_override":
            icons = []
        cat.append(D(7, catg, title, f"Security/resilience: {title}", H + body,
                     lesson=f"7.{(i%4)+1}", lab="lab-07", aws_icons=icons if isinstance(icons, list) else []))

    # MODULE 8 AI (25+)
    m8 = [
        ("Enterprise AI Platform", ["Amazon Bedrock", "Amazon API Gateway", "AWS Lambda"], """flowchart TB
  Apps["LOB Apps"] --> GW["AI Gateway"]
  GW --> Bedrock["Amazon Bedrock"]
  GW --> Policy["Policy · HITL · Audit"]
  Bedrock --> Obs["Cost · Quality Monitor"]
"""),
        ("Bedrock Decision Assistant", ["Amazon Bedrock", "AWS Lambda", "AWS Step Functions", "Amazon DynamoDB"], """flowchart LR
  Inc["Incident"] --> API["API Gateway"]
  API --> L["Lambda"]
  L --> BR["Bedrock"]
  L --> Rules["Deterministic Rules"]
  Rules --> SF["Step Functions HITL"]
  L --> DDB["Audit DynamoDB"]
"""),
        ("AI Gateway Pattern", ["Amazon API Gateway", "Amazon Bedrock"], """flowchart LR
  Cons["Consumers"] --> GW["Model Gateway"]
  GW --> Auth["AuthZ"]
  GW --> Bedrock["Bedrock Models"]
"""),
        ("RAG Conceptual", ["Amazon Bedrock", "Amazon S3"], """flowchart LR
  Q["Query"] --> Retr["Retrieve"]
  Retr --> KB["Knowledge Sources"]
  Retr --> Gen["Generate via Bedrock"]
  Gen --> Ans["Grounded Answer"]
"""),
        ("Vector Search Conceptual", [], """flowchart LR
  Doc["Documents"] --> Emb["Embeddings"]
  Emb --> Vec["Vector Index (conceptual)"]
  Q["Query"] --> Vec --> Ctx["Top-K Context"]
"""),
        ("Prompt Flow Structured JSON", ["Amazon Bedrock", "AWS Lambda"], """flowchart LR
  In["Input"] --> Prompt["Structured Prompt"]
  Prompt --> Model["Bedrock"]
  Model --> JSON["JSON Schema Validate"]
  JSON --> Out["Typed Decision"]
"""),
        ("Human in the Loop", ["AWS Step Functions"], """stateDiagram-v2
  [*] --> AutoDecide
  AutoDecide --> HumanReview: High Risk
  AutoDecide --> Execute: Low Risk
  HumanReview --> Execute: Approved
  HumanReview --> Reject: Denied
  Execute --> [*]
  Reject --> [*]
"""),
        ("AI Governance Lifecycle", [], """flowchart LR
  Propose["Propose Use Case"] --> Score["Scorecard"]
  Score --> Pilot["Pilot Controls"]
  Pilot --> Eval["Evaluate"]
  Eval --> Prod["Production Gate"]
"""),
        ("Model Evaluation Loop", ["Amazon S3", "Amazon CloudWatch"], """flowchart LR
  Set["Eval Dataset"] --> Run["Run Cases"]
  Run --> Score["Quality Scores"]
  Score --> Dec["Ship / Fix / Block"]
"""),
        ("Guardrails Overlay", ["Amazon Bedrock"], """flowchart TB
  Input --> GuardIn["Input Guardrails"]
  GuardIn --> Model["Model"]
  Model --> GuardOut["Output Guardrails"]
  GuardOut --> App
"""),
        ("Token Cost Tracking", ["Amazon CloudWatch", "Amazon DynamoDB"], """flowchart LR
  Call["Model Call"] --> Tokens["Token Meter"]
  Tokens --> Cost["Cost Estimate"]
  Cost --> CW["CloudWatch / Table"]
"""),
        ("AI Agent Pattern", ["Amazon Bedrock", "AWS Step Functions"], """flowchart LR
  Goal["Goal"] --> Agent["Agent Loop"]
  Agent --> Tools["Tools / APIs"]
  Agent --> HITL["HITL Checkpoints"]
"""),
        ("Workflow Intelligence", ["AWS Step Functions", "Amazon Bedrock"], """flowchart TB
  WF["Business Workflow"] --> DecPoints["Decision Points"]
  DecPoints --> AI["AI Suggestion"]
  AI --> Human["Human Accountable"]
"""),
        ("AI Risk Register Visual", [], """flowchart TB
  Priv["Privacy"] --- Safety["Safety"]
  Hall["Hallucination"] --- Cost["Cost Overrun"]
  Access["Over-broad Access"] --- Drift["Quality Drift"]
"""),
        ("Safe Audit Logging", ["Amazon DynamoDB", "Amazon S3"], """flowchart LR
  IO["Inputs/Outputs"] --> Redact["Redact Sensitive"]
  Redact --> Log["Audit Store"]
"""),
        ("Use Case Portfolio Board", ["executive"], """flowchart LR
  Quick["Quick Wins"] --- Strat["Strategic"]
  Defer["Defer"] --- Reject["Reject"]
"""),
        ("Lab 8 Mock vs Bedrock", ["Amazon Bedrock", "AWS Lambda"], """flowchart TB
  Flag{"use_mock_bedrock?"}
  Flag -->|true| Mock["Deterministic Mock JSON"]
  Flag -->|false| BR["Amazon Bedrock"]
  Mock & BR --> Validate["Validate + Rules"]
"""),
        ("AI Operating Model", [], """flowchart TB
  Biz["Business Sponsor"] --> Plat["AI Platform Team"]
  Plat --> Dom["Domain Teams"]
  Plat --> Risk["Risk / Compliance"]
"""),
        ("Knowledge Base Ingestion", ["Amazon S3", "Amazon Bedrock"], """flowchart LR
  Docs["Approved Docs"] --> S3["S3"]
  S3 --> Ingest["Ingest / Index"]
  Ingest --> KB["Knowledge Base"]
"""),
        ("Approval Routing Severity", ["AWS Step Functions"], """flowchart LR
  Sev{"Severity"}
  Sev -->|Low| Auto
  Sev -->|High| HITL
"""),
        ("Prompt Version Control", [], """flowchart LR
  PromptV["Prompt vN"] --> Review["Change Review"]
  Review --> Deploy["Deploy"]
  Deploy --> Eval["Regression Eval"]
"""),
        ("AI Reference Architecture Exec", [], """flowchart TB
  Value["Business Decisions"] --> Ctrl["Governed AI Platform"]
  Ctrl --> Out["Outcomes + Audit"]
"""),
        ("Multi Model Routing Conceptual", ["Amazon Bedrock"], """flowchart LR
  Req --> Router["Model Router"]
  Router --> M1["Model A"]
  Router --> M2["Model B"]
"""),
        ("Quality Metrics Dashboard Concept", ["Amazon CloudWatch"], """flowchart TB
  Acc["Accuracy"] --- Lat["Latency"]
  Cost["Cost/Token"] --- Hit["HITL Rate"]
"""),
        ("Responsible AI Checklist Visual", [], """flowchart LR
  Privacy --> Safety --> Transparency --> Accountability
"""),
    ]
    for i, (title, icons, body) in enumerate(m8):
        catg = "executive" if "Exec" in title or "Portfolio" in title or icons == ["executive"] else (
            "sequence" if "stateDiagram" in body else "aws"
        )
        if icons == ["executive"]:
            icons = []
            catg = "executive"
        if any(x in title for x in ["Governance", "Operating", "Risk", "Responsible", "Prompt Version", "Quality"]):
            catg = "concept" if catg != "executive" else catg
        cat.append(D(8, catg, title, f"AI strategy: {title}", H + body,
                     lesson=f"8.{(i%4)+1}", lab="lab-08", aws_icons=icons if isinstance(icons, list) else []))

    # MODULE 9 Governance (20+)
    m9 = [
        ("ARB Operating Model", """flowchart TB
  Prop["Proposal Intake"] --> Pack["Review Pack"]
  Pack --> ARB["Architecture Review Board"]
  ARB --> Dec["Approve / Conditional / Reject"]
  Dec --> ADR["ADRs"]
"""),
        ("Guardrails vs Gates", """flowchart LR
  Guard["Automated Guardrails"] --> Speed["Safe Autonomy"]
  Gate["Human Gates"] --> Material["Material Risk Decisions"]
"""),
        ("Exception Waiver Process", """flowchart LR
  Req["Exception Request"] --> Risk["Risk Assess"]
  Risk --> Dec["Decide + Expiry"]
  Dec --> Review["Re-review Date"]
"""),
        ("ADR Lifecycle", """flowchart LR
  Draft["Draft"] --> Review["Review"]
  Review --> Accepted["Accepted"]
  Accepted --> Superseded["Superseded"]
"""),
        ("Standards Repository", """flowchart TB
  Ref["Reference Architectures"] --> Std["Standards"]
  Std --> Patterns["Patterns"]
  Patterns --> Teams["Delivery Teams"]
"""),
        ("Governance Lifecycle", """flowchart LR
  Set["Set Direction"] --> Enable["Enable"]
  Enable --> Assure["Assure"]
  Assure --> Improve["Improve"]
"""),
        ("Federated vs Centralized", """flowchart LR
  Cent["Centralized"] --- Fed["Federated"]
  Cent --> Fit1["High risk standardization"]
  Fed --> Fit2["Domain speed + guardrails"]
"""),
        ("Review Workflow 30 Minute", """gantt
  title ARB 30-Minute Simulation
  dateFormat mm
  axisFormat %M
  section Agenda
  Intake summary           :a1, 00, 5m
  Principle alignment      :a2, after a1, 5m
  Risks and alternatives   :a3, after a2, 10m
  Decision and conditions  :a4, after a3, 7m
  ADR owners               :a5, after a4, 3m
"""),
        ("Decision Memo Structure", """flowchart TB
  Rec["Recommendation"] --> Why["Why Now"]
  Why --> Options["Options"]
  Options --> Ask["Clear Ask"]
"""),
        ("Portfolio Governance Cadence", """flowchart LR
  Weekly["Domain Reviews"] --> Monthly["ARB"]
  Monthly --> Quarterly["Portfolio Exec"]
"""),
        ("Lab 9 Divergent Proposal Risks", """flowchart TB
  Prop["Alt Cloud + Proprietary DB + Custom Integration + Direct Prod Access"] --> Risks["Misalignment Risks"]
  Risks --> Dec["ARB Decision"]
"""),
        ("Architecture Organization Chart", """flowchart TB
  CIO --> EA
  EA --> Domain
  EA --> Platform
  EA --> ARB
"""),
        ("Reference Architecture Adoption", """flowchart LR
  RA["Reference Architecture"] --> Adopt["Adopt"]
  RA --> Adapt["Adapt with ADR"]
  RA --> Exception["Exception"]
"""),
        ("Design Authority Interaction", """flowchart LR
  Team["Delivery Team"] --> DA["Design Authority"]
  DA --> ARB["Escalate Material"]
"""),
        ("Exec Communication Stack", """flowchart TB
  Detail["Detailed Architecture"] --> Brief["5-Slide Brief"]
  Brief --> Memo["Decision Memo"]
"""),
        ("Principle Alignment Scorecard", """flowchart LR
  P1["Principle"] --> Align{"Aligns?"}
  Align -->|No| Risk["Document Risk"]
  Align -->|Yes| Proceed["Proceed"]
"""),
        ("Architecture Repository Contents", """mindmap
  root((Arch Repo))
    Principles
    ADRs
    Reference Arch
    Standards
    Exceptions
"""),
        ("Conditional Approval Path", """flowchart TB
  Cond["Conditional Approve"] --> Track["Track Conditions"]
  Track --> Met{"Met?"}
  Met -->|Yes| Full["Full Approve"]
  Met -->|No| Escalate["Escalate"]
"""),
        ("Reject with Alternatives", """flowchart LR
  Reject["Reject"] --> Alts["Document Alternatives"]
  Alts --> Coach["Coach Requester"]
"""),
        ("Governance Metrics", """flowchart TB
  M1["Cycle Time to Decision"] --- M2["Exception Aging"]
  M3["ADR Coverage"] --- M4["Guardrail Violations"]
"""),
    ]
    for i, (title, body) in enumerate(m9):
        catg = "process" if any(x in title for x in ["Process", "Workflow", "Lifecycle", "Cadence", "Path"]) else "concept"
        if "Memo" in title or "Exec" in title:
            catg = "executive"
        cat.append(D(9, catg, title, f"Governance: {title}", H + body, lesson=f"9.{(i%4)+1}", lab="lab-09"))

    # MODULE 10 + Capstone (30+)
    m10 = [
        ("Capstone Narrative Arc", "executive", """flowchart LR
  Prob["Problem"] --> Cur["Current"]
  Cur --> Target["Target"]
  Target --> Road["Roadmap"]
  Road --> Ask["Decision Ask"]
"""),
        ("Complete Enterprise Architecture Layers", "concept", """block-beta
  columns 1
  BUSINESS[\"Business\"]
  APP[\"Application & Integration\"]
  DATA[\"Data\"]
  CLOUD[\"Cloud & Platform\"]
  SEC[\"Security & Resilience\"]
  AI[\"Governed AI\"]
"""),
        ("Executive Transformation Overview", "executive", """flowchart TB
  NS["NorthStar Transformation (fictional)"] --> Out["Outcomes"]
  Out --> Plat["Platforms"]
  Out --> Risk["Risk Down"]
  Out --> Speed["Speed Up"]
"""),
        ("Trade-off Defense Loop", "process", """flowchart LR
  Claim["Recommendation"] --> Chal["Challenge"]
  Chal --> Alt["Alternatives"]
  Alt --> Cons["Consequences"]
  Cons --> Decide["Decide"]
"""),
        ("Fifteen Slide Storyboard", "executive", """flowchart LR
  S1["Ask"] --> S2["Outcomes"]
  S2 --> S3["Current"]
  S3 --> S4["Target"]
  S4 --> S5["Roadmap"]
  S5 --> S6["Decisions"]
"""),
        ("Integrated Target State", "aws", """flowchart TB
  Exp["Experiences"] --> APIGW["API Platform"]
  APIGW --> Dom["Domain Services"]
  Dom --> EB["Event Backbone"]
  Dom --> Data["Data Products"]
  Plat["Landing Zone + IDP"] --> Dom
  Sec["Security Controls"] --> Plat & Dom
  AI["Governed AI"] --> Dom
"""),
        ("Cost Model Overlay", "executive", """flowchart LR
  Run["Run Cost"] --> Shift["Platform Shift"]
  Shift --> Save["Target Savings Trajectory"]
"""),
        ("Operational Model Target", "concept", """flowchart TB
  Prod["Product Teams"] --> GP["Golden Paths"]
  EA["EA / ARB"] --> Guard["Guardrails"]
  Guard --> Prod
"""),
        ("Monitoring Target Stack", "infrastructure", """flowchart LR
  Apps --> CT["CloudTrail"]
  Apps --> CW["CloudWatch"]
  CT & CW --> Ops["Ops + Sec Detect"]
"""),
        ("Career Portfolio Map", "concept", """mindmap
  root((Portfolio))
    Operating Model
    Capability Map
    TIME Portfolio
    Target Roadmap
    Cloud Platform
    Integration
    Security DR
    AI Governance
    ARB Pack
    Capstone Deck
"""),
    ]
    for i, (title, catg, body) in enumerate(m10):
        icons = ["Amazon API Gateway", "Amazon EventBridge", "IAM", "Amazon Bedrock"] if catg == "aws" else []
        cat.append(D(10, catg, title, f"Capstone leadership: {title}", H + body,
                     lesson=f"10.{(i%4)+1}", lab="lab-10", aws_icons=icons))

    # Extra capstone compositions
    cap_extras = [
        ("Business Layer View", "executive", """flowchart LR
  Strat --> Cap --> KPI --> Value
"""),
        ("Application Layer View", "concept", """flowchart TB
  Exp --> Services --> Platforms
"""),
        ("Technology Layer View", "infrastructure", """flowchart TB
  LZ["Landing Zone"] --> Comp["Compute Patterns"]
  LZ --> Data["Data Platform"]
"""),
        ("Security Layer View", "security", """flowchart LR
  Id["Identity"] --> Protect["Protect"]
  Protect --> Detect["Detect"]
  Detect --> Recover["Recover"]
"""),
        ("Integration Layer View", "aws", """flowchart LR
  API --> Events --> Files --> Batch
"""),
        ("AI Layer View", "aws", """flowchart LR
  Gateway --> Bedrock --> HITL --> Audit
"""),
        ("Cloud Layer View", "aws", """flowchart TB
  Org --> Accounts --> Guardrails --> Workloads
"""),
        ("Transformation Roadmap Exec", "executive", """timeline
    title Executive Roadmap
    0-3m : Foundation
    3-9m : Value platforms
    9-18m : Scale
    18-24m : Optimize + AI
"""),
        ("Panel Q&A Defense Map", "process", """flowchart TB
  Q["Panel Question"] --> Type{"Type"}
  Type --> Cost
  Type --> Risk
  Type --> Autonomy
  Type --> Speed
"""),
        ("Before After Consolidation", "executive", """flowchart LR
  Before["300+ Apps · Sprawl"] --> After["Governed Platforms · Fewer Duplicates"]
"""),
    ]
    for title, catg, body in cap_extras:
        cat.append(D("cap", catg, title, f"Capstone integrated view: {title}", H + body,
                     lab="lab-10", slides="slides/module-10/",
                     aws_icons=["Amazon API Gateway", "Amazon Bedrock", "AWS Organizations"] if catg == "aws" else []))

    # LAB diagram sets for labs 5-8 (12 each) + lighter for 1-4,9,10
    def lab_set(lab_no: int, name: str, aws: list[str], tech_body: str):
        lab_id = f"lab-{lab_no:02d}"
        bases = [
            ("Business Context", "concept", f"""flowchart TB
  Biz["NorthStar Business Need (fictional)"] --> Lab["Lab {lab_no}: {name}"]
  Lab --> Out["Learning Outcomes"]
"""),
            ("Current Architecture", "concept", """flowchart LR
  AsIs["As-Is Fragmented"] --> Pain["Pain: Cost · Risk · Slow"]
"""),
            ("Target Architecture", "aws", tech_body),
            ("Step by Step Deployment", "process", """flowchart LR
  Prep["Prep / Tags / Budget"] --> Init["terraform init"]
  Init --> Plan["plan"] --> Apply["apply"] --> Validate["Validate"]
"""),
            ("AWS Resources", "aws", tech_body),
            ("Data Flow", "dataflow", """flowchart LR
  In["Input"] --> Proc["Process"] --> Out["Output / Store"]
"""),
            ("Security", "security", """flowchart TB
  IAM["Least Privilege IAM"] --> Enc["Encryption"]
  Enc --> Audit["Audit Logging"]
"""),
            ("Monitoring", "infrastructure", """flowchart LR
  Metrics --> Alarms --> Notify
"""),
            ("Failure Scenario", "process", """flowchart LR
  Fail["Failure Injected"] --> Detect["Detect"] --> Respond["Respond"]
"""),
            ("Recovery", "process", """flowchart LR
  Detect --> Recover["Recover / Restore"] --> Confirm["Confirm RTO/RPO"]
"""),
            ("Cleanup Flow", "process", """flowchart LR
  Done["Lab Done"] --> Destroy["terraform destroy / cleanup script"] --> Verify["Verify no lab tags remain"]
"""),
            ("Expected Final Architecture", "aws", tech_body),
        ]
        for title, catg, body in bases:
            cat.append(D(lab_id, catg, f"{name} — {title}", f"Lab {lab_no} visual: {title}", H + body,
                         lab=lab_id, aws_icons=aws, slides=f"slides/module-{lab_no:02d}/"))

    lab_set(5, "Platform Foundation",
            ["IAM", "Amazon S3", "AWS CloudTrail", "Amazon CloudWatch", "AWS Budgets", "Amazon DynamoDB", "AWS Lambda", "Amazon API Gateway", "AWS Systems Manager"],
            """flowchart TB
  APIGW["API Gateway"] --> L["Lambda"]
  L --> DDB["DynamoDB"]
  L --> SSM["SSM"]
  CT["CloudTrail"] --> S3["S3"]
  Bud["Budgets"]
""")
    lab_set(6, "Integration Platform",
            ["Amazon API Gateway", "AWS Lambda", "Amazon EventBridge", "Amazon SQS", "AWS Step Functions", "Amazon S3", "Amazon DynamoDB", "Amazon SNS"],
            """flowchart LR
  APIGW --> L --> EB --> SQS --> L2
  S3 --> SF --> L3
  L2 --> SNS
  L2 --> DDB
""")
    lab_set(7, "Security Resilience",
            ["IAM", "AWS KMS", "Amazon S3", "Amazon CloudWatch"],
            """flowchart TB
  App --> IAM
  App --> KMS
  App --> S3
  CW["CloudWatch"]
""")
    lab_set(8, "AI Decision Assistant",
            ["Amazon Bedrock", "AWS Lambda", "AWS Step Functions", "Amazon DynamoDB", "Amazon API Gateway", "Amazon CloudWatch"],
            """flowchart LR
  API --> L --> Bedrock
  L --> Rules --> SF
  L --> DDB
""")

    # Labs 1-4, 9, 10 lighter sets (6 each) to push toward 200+
    for lab_no, name in [(1, "Architecture Operating Model"), (2, "Capability Mapping"), (3, "Portfolio Assessment"),
                         (4, "Target State Roadmap"), (9, "Architecture Review Board"), (10, "Capstone")]:
        lab_id = f"lab-{lab_no:02d}"
        for title, catg, body in [
            ("Business Context", "concept",
             f"flowchart TB\n  NS[NorthStar Need] --> Lab[Lab {lab_no}: {name}]\n"),
            ("Current State", "concept",
             "flowchart LR\n  Current[Current Pain] --> Insight[Architecture Insight]\n"),
            ("Target Artifact", "concept",
             "flowchart LR\n  Work[Student Work] --> Artifact[Professional Artifact]\n"),
            ("Process Steps", "process",
             "flowchart LR\n  S1[1] --> S2[2] --> S3[3] --> S4[4]\n"),
            ("Review Checkpoint", "process",
             "flowchart LR\n  Draft --> Peer[Peer/Instructor Review] --> Refine\n"),
            ("Capstone Contribution", "executive",
             "flowchart LR\n  LabOut[Lab Output] --> Capstone[Capstone Pack]\n"),
        ]:
            cat.append(D(lab_id, catg, f"{name} — {title}", f"Lab {lab_no}: {title}", H + body, lab=lab_id))

    return cat


def mermaid_to_drawio(diagram: dict) -> str:
    """Create a diagrams.net file with Mermaid embedded + AWS icon notes."""
    title = diagram["title"]
    mid = diagram["id"]
    mermaid = diagram["mermaid"].replace("]]>", "]] >")
    icons = ", ".join(diagram.get("awsIcons") or []) or "N/A"
    # Escape for XML text
    mermaid_xml = (
        mermaid.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="BayLearn" modified="{date.today().isoformat()}" agent="BayLearnDiagramFramework" version="22.1.0" type="device">
  <diagram id="{mid}" name="{title[:40]}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="title" value="{title.replace('&', '&amp;')} — BayLearn&#xa;AWS icons: {icons.replace('&', '&amp;')}&#xa;Open Mermaid panel / recreate with AWS19 stencil for presentation master" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1520" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="mermaid" value="&lt;pre&gt;{mermaid_xml}&lt;/pre&gt;" style="text;html=1;strokeColor=#146EB4;fillColor=#E6F2FF;align=left;verticalAlign=top;whiteSpace=wrap;rounded=1;fontSize=10;fontFamily=Courier New;spacing=8;" vertex="1" parent="1">
          <mxGeometry x="40" y="100" width="1520" height="740" as="geometry"/>
        </mxCell>
        <mxCell id="footer" value="NorthStar Financial Services (fictional) · BayLearn Diagram Library · Progressive groups: g1→g6" style="text;html=1;strokeColor=none;fillColor=none;fontSize=10;fontColor=#545B64;" vertex="1" parent="1">
          <mxGeometry x="40" y="850" width="1520" height="30" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''


def write_markdown(diagram: dict, rel_mermaid: str, rel_drawio: str, rel_svg: str, rel_png: str) -> str:
    icons = ", ".join(diagram.get("awsIcons") or []) or "_None (non-AWS concept)_"
    return f"""# {diagram['title']}

| Field | Value |
| ----- | ----- |
| ID | `{diagram['id']}` |
| Category | `{diagram['category']}` |
| Module | `{diagram['module']}` |
| Lesson | {diagram.get('lesson') or '—'} |
| Lab | {diagram.get('lab') or '—'} |
| Learning objective | {diagram['learningObjective']} |
| AWS icons | {icons} |

## Formats

- Mermaid: [`{rel_mermaid}`]({rel_mermaid})
- Draw.io: [`{rel_drawio}`]({rel_drawio})
- SVG: [`{rel_svg}`]({rel_svg})
- PNG: [`{rel_png}`]({rel_png})

## Mermaid

```mermaid
{diagram['mermaid']}```

> Presentation masters for AWS reference architectures should be refined in Draw.io using official **AWS Architecture Icons** (AWS19/AWS23 stencil). Mermaid preserves structure and learning intent.
"""


def simple_svg(diagram: dict) -> str:
    """Minimal valid SVG placeholder that references title; replaced by mmdc when available."""
    title = diagram["title"].replace("&", "&amp;")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
  <rect width="1600" height="900" fill="#FFFFFF"/>
  <rect x="40" y="40" width="1520" height="820" rx="8" fill="#E6F2FF" stroke="#146EB4" stroke-width="2"/>
  <text x="80" y="120" font-family="Helvetica, Arial, sans-serif" font-size="28" fill="#232F3E">{title}</text>
  <text x="80" y="170" font-family="Helvetica, Arial, sans-serif" font-size="16" fill="#545B64">BayLearn · {diagram['id']}</text>
  <text x="80" y="220" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#545B64">Export via mermaid-cli for rendered diagram. Draw.io file includes source.</text>
  <text x="80" y="820" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#545B64">NorthStar Financial Services (fictional)</text>
</svg>
'''


def try_mmdc_export(mmd_path: Path, svg_path: Path, png_path: Path) -> bool:
    mmdc = shutil.which("mmdc")
    if not mmdc:
        # try npx
        npx = shutil.which("npx")
        if not npx:
            return False
        cmd_base = [npx, "-y", "@mermaid-js/mermaid-cli"]
    else:
        cmd_base = [mmdc]
    try:
        subprocess.run(cmd_base + ["-i", str(mmd_path), "-o", str(svg_path), "-b", "white"],
                       check=True, capture_output=True, timeout=120)
        subprocess.run(cmd_base + ["-i", str(mmd_path), "-o", str(png_path), "-b", "white", "-s", "2"],
                       check=True, capture_output=True, timeout=120)
        return True
    except Exception:
        return False


def module_dir(module_field: str) -> Path:
    if module_field.startswith("lab-"):
        return DIAGRAMS / "labs" / module_field
    if module_field == "cap" or module_field.startswith("cap"):
        return DIAGRAMS / "capstone"
    return DIAGRAMS / module_field


def generate_all(export_images: bool = True) -> dict:
    cat = build_catalog()
    cat = extend_catalog(cat)
    cat = extend_catalog_security_ai_gov_cap(cat)

    # dedupe ids
    seen = set()
    unique = []
    for d in cat:
        if d["id"] in seen:
            d["id"] = d["id"] + f"-{len(seen)}"
        seen.add(d["id"])
        unique.append(d)
    cat = unique

    manifest = {
        "manifestVersion": "1.0.0",
        "courseId": "enterprise-architecture-leadership-masterclass",
        "generatedOn": date.today().isoformat(),
        "awsIconPack": "AWS Architecture Icons — use latest; Draw.io AWS19/AWS23 stencils",
        "visualStyle": "diagram-library/standards/VISUAL_STYLE_GUIDE.md",
        "counts": {},
        "diagrams": [],
    }

    exported = 0
    for d in cat:
        base = module_dir(d["module"] if not str(d["module"]).startswith("lab") else d["module"])
        # labs use module field like lab-05
        if d["id"].startswith("lab-") or (d.get("module") or "").startswith("lab-"):
            base = DIAGRAMS / "labs" / (d["module"] if str(d["module"]).startswith("lab-") else d.get("lab"))
        elif d["id"].startswith("cap-") or d["module"] == "cap":
            base = DIAGRAMS / "capstone"

        cat_dir = d["category"] if d["category"] in {
            "concept", "process", "aws", "sequence", "infrastructure", "dataflow", "security", "executive"
        } else "concept"

        # Course layout: diagrams/module-XX/{mermaid,drawio,svg,png,markdown}/category/
        if base.parent.name == "labs" or base.name == "capstone":
            mmd_dir = base / "mermaid" / cat_dir
            dio_dir = base / "drawio" / cat_dir
            svg_dir = base / "svg" / cat_dir
            png_dir = base / "png" / cat_dir
            md_dir = base / "markdown" / cat_dir
        else:
            mmd_dir = base / "mermaid" / cat_dir
            dio_dir = base / "drawio" / cat_dir
            svg_dir = base / "svg" / cat_dir
            png_dir = base / "png" / cat_dir
            md_dir = base / "markdown" / cat_dir

        for p in (mmd_dir, dio_dir, svg_dir, png_dir, md_dir):
            p.mkdir(parents=True, exist_ok=True)

        stem = d["id"]
        mmd_path = mmd_dir / f"{stem}.mmd"
        dio_path = dio_dir / f"{stem}.drawio"
        svg_path = svg_dir / f"{stem}.svg"
        png_path = png_dir / f"{stem}.png"
        md_path = md_dir / f"{stem}.md"

        mmd_path.write_text(d["mermaid"], encoding="utf-8")
        dio_path.write_text(mermaid_to_drawio(d), encoding="utf-8")

        rendered = False
        if export_images:
            rendered = try_mmdc_export(mmd_path, svg_path, png_path)
            if rendered:
                exported += 1
        if not svg_path.exists():
            svg_path.write_text(simple_svg(d), encoding="utf-8")
        if not png_path.exists():
            # minimal 1x1 PNG is bad; write SVG-note sidecar instead + tiny valid PNG via pure python
            write_minimal_png(png_path, d["title"])

        rel = lambda p: str(p.relative_to(DIAGRAMS))
        md_path.write_text(
            write_markdown(d, rel(mmd_path), rel(dio_path), rel(svg_path), rel(png_path)),
            encoding="utf-8",
        )

        # Also publish selected into shared library buckets
        publish_shared(d, mmd_path)

        entry = {k: v for k, v in d.items() if k != "mermaid"}
        entry["formats"] = {
            "mermaid": rel(mmd_path),
            "drawio": rel(dio_path),
            "svg": rel(svg_path),
            "png": rel(png_path),
            "markdown": rel(md_path),
        }
        entry["renderedWithMermaidCli"] = rendered
        manifest["diagrams"].append(entry)

    # counts
    by_mod: dict[str, int] = {}
    by_cat: dict[str, int] = {}
    for e in manifest["diagrams"]:
        by_mod[e["module"]] = by_mod.get(e["module"], 0) + 1
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + 1
    manifest["counts"] = {
        "total": len(manifest["diagrams"]),
        "byModule": by_mod,
        "byCategory": by_cat,
        "mermaidCliExports": exported,
    }

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def publish_shared(d: dict, mmd_path: Path) -> None:
    mapping = {
        "concept": "enterprise-architecture",
        "process": "enterprise-architecture",
        "aws": "aws",
        "sequence": "integration",
        "infrastructure": "cloud",
        "dataflow": "data",
        "security": "security",
        "executive": "enterprise-architecture",
    }
    # refine
    tags = set(d.get("tags") or [])
    folder = mapping.get(d["category"], "enterprise-architecture")
    if d["category"] == "aws" and any("Bedrock" in x for x in d.get("awsIcons") or []):
        folder = "ai"
    if d["category"] == "dataflow":
        folder = "data"
    if "operating-model" in tags:
        folder = "enterprise-architecture"
    dest = LIBRARY / folder / "mermaid"
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / mmd_path.name
    if not target.exists():
        target.write_text(mmd_path.read_text(encoding="utf-8"), encoding="utf-8")


def write_minimal_png(path: Path, title: str) -> None:
    """Write a small valid solid-color PNG (presentation note: replace via mmdc)."""
    import struct
    import zlib

    width, height = 1600, 900
    # white background raw rows
    row = b"\x00" + b"\xff\xff\xff" * width
    raw = row * height
    compressed = zlib.compress(raw, 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")
    path.write_bytes(png)


def main():
    print("Generating BayLearn diagram library…")
    # Skip slow npx by default unless BL_DIAGRAM_EXPORT=1
    export = Path.cwd()  # placeholder
    do_export = False
    import os
    do_export = os.environ.get("BL_DIAGRAM_EXPORT", "0") == "1"
    manifest = generate_all(export_images=do_export)
    print(f"Generated {manifest['counts']['total']} diagrams")
    print(f"By module: {json.dumps(manifest['counts']['byModule'], indent=2)}")
    print(f"Manifest: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
