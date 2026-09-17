For the **Final Canonical JSON**, I would use the following table in your AWS/internal architecture discussion. It explains not only what each section contains, but **why it exists and who benefits from it**.

| JSON Section                          | Purpose                                                                                           | Key Information                                                                             | Primary Audience                                      | How It Helps                                                                                            |
| ------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Root / Flow Identity**              | Provides a permanent identity for the file flow                                                   | `schemaVersion`, `flowId`, `flowName`                                                       | Everyone                                              | Gives every flow a unique NIS identity that remains consistent even if the underlying platform changes  |
| **`service`**                         | Describes the file flow from a business/service perspective                                       | Customer, business service, description, business purpose, environment, status, criticality | Business, Product, Management, Architecture           | Allows non-technical users to understand **what the service is and why it exists**                      |
| **`flow`**                            | Describes the business-level movement of information                                              | From organization/application, to organization/application, direction, flow type            | Business, Application Teams, Operations, Architecture | Clearly answers **who sends files and who receives them** without requiring knowledge of SFTP/S3/EFEDS  |
| **`files`**                           | Describes the files associated with the service                                                   | Business file type, filename pattern, format, expected volume, average/max size             | Business, Operations, Engineering, Capacity Planning  | Establishes what files belong to the flow and provides baselines for monitoring, reporting and capacity |
| **`schedule`**                        | Defines when/how frequently the flow is expected to operate                                       | Frequency, trigger, service window                                                          | Business, Operations, Support                         | Establishes expected behavior such as hourly, daily, event-driven or 24x7                               |
| **`serviceLevel`**                    | Defines the business expectations for the flow                                                    | Criticality/service level, expected delivery time, missing-file threshold                   | Business, Service Management, Operations              | Converts a technical transfer into a measurable **business service expectation**                        |
| **`ownership`**                       | Establishes accountability                                                                        | Business owner, application owner, service owner, support team                              | Everyone                                              | Makes it immediately clear **who owns, supports and is accountable for the flow**                       |
| **`monitoring`**                      | Defines operational observability requirements                                                    | Failure alerts, missing-file alerts, volume monitoring, latency, hourly/daily reporting     | Operations, Support, Engineering                      | Provides standardized monitoring expectations and supports proactive detection of abnormal behavior     |
| **`technical`**                       | Contains implementation-specific details while keeping them separate from the business definition | Platform, technology, source/destination connectivity, security, platform configuration     | NIS Engineering, AWS, Architecture                    | Allows the same business catalog model to support **EFEDS today and AWS NIS tomorrow**                  |
| **`technical.source`**                | Describes technical source connectivity                                                           | Protocol, endpoint, port, directory                                                         | Engineering, AWS, Support                             | Provides the information required to establish or troubleshoot source connectivity                      |
| **`technical.destination`**           | Describes technical target connectivity                                                           | Protocol, endpoint, port, directory                                                         | Engineering, AWS, Support                             | Provides the information required to configure or troubleshoot delivery                                 |
| **`technical.security`**              | Captures security requirements                                                                    | Authentication, transport encryption, file encryption, data classification                  | Security, Architecture, Engineering                   | Makes security requirements explicit and enables validation before provisioning/migration               |
| **`technical.platformConfiguration`** | Stores platform-specific configuration                                                            | EFEDS partner/routing/mailbox/BP or AWS-specific configuration                              | EFEDS Team, AWS Team, NIS Engineering                 | Keeps implementation details flexible without contaminating the common business/service model           |
| **`lifecycle`**                       | Tracks how the service entered the catalog and its current lifecycle state                        | Existing/new origin, onboarding method, catalog status, created/reviewed dates              | Architecture, Governance, Management                  | Supports existing flows, new flows, changes and eventual retirement using the same model                |
| **`migration`**                       | Manages movement of an existing flow between platforms                                            | Candidate status, source/target platform, complexity, migration wave                        | Migration Team, AWS, Architecture, Management         | Turns the catalog into an actionable source for **EFEDS → AWS migration planning**                      |
| **`migration.dependencies`**          | Identifies migration blockers/dependencies                                                        | Connectivity, keys, application changes, partner dependencies, etc.                         | AWS, NIS, Application Teams                           | Helps identify what must be completed before migration                                                  |
| **`migration.validation`**            | Tracks required approvals/validation                                                              | Business, technical and security validation                                                 | Business, NIS, Security, AWS                          | Prevents technically migrating a flow without validating the complete service                           |
| **`migration.testing`**               | Tracks migration testing                                                                          | Connectivity, file transfer, volume and business validation tests                           | QA, NIS, AWS, Application Teams                       | Provides measurable migration readiness and evidence before cutover                                     |
| **`migration.cutover`**               | Tracks production transition                                                                      | Planned and actual cutover dates                                                            | Operations, AWS, NIS, Management                      | Provides visibility into migration execution and completion                                             |

### How I would explain the five views

| View                            | JSON Sections                                    | Audience                           | Primary Question                                               |
| ------------------------------- | ------------------------------------------------ | ---------------------------------- | -------------------------------------------------------------- |
| **Business View**               | `service`, `flow`, `files`, `schedule`           | Customer, Product, Management      | **What is this flow and why does the business need it?**       |
| **Service View**                | `serviceLevel`, `ownership`                      | Business, Service Management       | **How important is it and who owns it?**                       |
| **Operations View**             | `monitoring`, `schedule`, `files.expectedVolume` | Operations, Support                | **Is the flow operating as expected?**                         |
| **Technical View**              | `technical.*`                                    | NIS Engineering, AWS, Architecture | **How is the flow technically implemented?**                   |
| **Governance & Migration View** | `lifecycle`, `migration`                         | Architecture, AWS, Management      | **Where is this flow in its lifecycle and migration journey?** |

The key point for the AWS discussion is that these are **not five different data models**. They are five projections of **one canonical File Flow JSON**:

```text
                    Canonical File Flow JSON
                              │
       ┌──────────┬───────────┼───────────┬─────────────┐
       ▼          ▼           ▼           ▼             ▼
   Business     Service    Operations   Technical    Governance
     View         View        View         View       / Migration
       │          │           │           │             │
       └──────────┴───────────┼───────────┴─────────────┘
                              │
                        NIS Flow ID
                              │
                    NIS-CASH-000123
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
                 EFEDS                AWS NIS
```

I would summarize the architecture to the team as:

> **“The canonical JSON gives us one representation of a File Flow as a Service. Business, operations, engineering and migration teams consume different views of the same record, while the permanent Flow ID provides traceability across EFEDS and AWS throughout the service lifecycle.”**

That is probably the clearest framing for your AWS Phase 2 discussion because it positions the JSON as a **shared enterprise contract**, rather than an AWS-specific onboarding payload.


I’d finalize the concept as a **Unified NIS File Flow Service Catalog** supporting existing EFEDS flows, migration, new AWS flows, operations, and future changes. The JSON below is intentionally business-readable at the top and progressively technical deeper down.

### Final canonical JSON

```json
{
  "schemaVersion": "1.0",

  "flowId": "NIS-CASH-000123",
  "flowName": "Cash Settlement Files",

  "service": {
    "customer": "FedCash",
    "businessService": "Cash Settlement",
    "description": "Transfers settlement files from FedCash to the Cash Processing application.",
    "businessPurpose": "Supports daily cash settlement processing.",
    "environment": "PROD",
    "status": "ACTIVE",
    "criticality": "HIGH"
  },

  "flow": {
    "from": {
      "organization": "FedCash",
      "application": "FedCash Source System"
    },
    "to": {
      "organization": "Federal Reserve",
      "application": "Cash Processing"
    },
    "direction": "INBOUND",
    "flowType": "APPLICATION_TO_APPLICATION"
  },

  "files": {
    "businessFileType": "Settlement Files",
    "filePattern": "CASH_*.DAT",
    "fileFormat": "DAT",
    "expectedVolume": {
      "filesPerHour": 100,
      "filesPerDay": 2400
    },
    "fileSize": {
      "averageMB": 25,
      "maximumMB": 500
    }
  },

  "schedule": {
    "frequency": "HOURLY",
    "trigger": "FILE_ARRIVAL",
    "serviceWindow": "24x7"
  },

  "serviceLevel": {
    "serviceLevel": "BUSINESS_CRITICAL",
    "expectedDelivery": "Within 15 minutes",
    "missingFileThreshold": "60 minutes"
  },

  "ownership": {
    "businessOwner": "FedCash",
    "applicationOwner": "Cash Processing",
    "serviceOwner": "NIS File Transfer",
    "supportTeam": "NIS File Transfer"
  },

  "monitoring": {
    "transferFailureAlert": true,
    "missingFileAlert": true,
    "volumeMonitoring": true,
    "latencyMonitoring": true,
    "hourlyVolumeReport": true,
    "dailyVolumeReport": true
  },

  "technical": {
    "platform": "EFEDS",
    "technology": "IBM Sterling File Gateway",

    "source": {
      "protocol": "SFTP",
      "endpoint": "fedcash-source",
      "port": 22,
      "directory": "/outbound/cash"
    },

    "destination": {
      "protocol": "SFTP",
      "endpoint": "cash-target",
      "port": 22,
      "directory": "/incoming/cash"
    },

    "security": {
      "authentication": "SSH_KEY",
      "transportEncryption": "SSH",
      "fileEncryption": "PGP",
      "dataClassification": "CONFIDENTIAL"
    },

    "platformConfiguration": {
      "partnerId": "FEDCASH",
      "routingChannel": "CASH_SETTLEMENT_IN",
      "mailbox": "FEDCASH_INBOUND",
      "businessProcess": "CASH_INBOUND_BP"
    }
  },

  "lifecycle": {
    "origin": "EXISTING",
    "onboardingMethod": "LEGACY_DISCOVERY",
    "catalogStatus": "REGISTERED",
    "createdDate": "2024-01-15",
    "lastReviewedDate": "2026-09-17"
  },

  "migration": {
    "candidate": true,
    "status": "NOT_ASSESSED",
    "sourcePlatform": "EFEDS",
    "targetPlatform": "AWS_NIS",
    "complexity": "NOT_ASSESSED",
    "migrationWave": null,

    "dependencies": [],

    "validation": {
      "businessValidated": false,
      "technicalValidated": false,
      "securityValidated": false
    },

    "testing": {
      "connectivityTest": "NOT_STARTED",
      "fileTransferTest": "NOT_STARTED",
      "volumeTest": "NOT_STARTED",
      "businessValidation": "NOT_STARTED"
    },

    "cutover": {
      "plannedDate": null,
      "actualDate": null
    }
  }
}
```

This one record supports five logical views:

```text
                    NIS FILE FLOW
                  NIS-CASH-000123
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
 BUSINESS VIEW     OPERATIONS VIEW    TECHNICAL VIEW
      │                  │                  │
 Service             Monitoring         Platform
 Flow                Volume             Protocol
 Files               Alerts             Endpoints
 Schedule            SLA                Security
      │                  │                  │
      └──────────────────┼──────────────────┘
                         │
               GOVERNANCE / MIGRATION
                         │
                  Lifecycle
                  Ownership
                  Migration
                  Testing/Cutover
```

The same schema supports the complete lifecycle:

**Existing EFEDS:** `Discover → Catalog → Assess → Migrate → AWS`

**New AWS:** `Request → Catalog → Validate → Provision → AWS`

**Existing AWS:** `Catalog → Monitor → Change → Operate`

**Retirement:** `Assess → Deactivate → Retire`

The `flowId` remains the permanent identity throughout.

### Teams message

Team — as we move into the next phase of NIS Self-Service File Transfer, I’d like to propose a **Unified NIS File Flow Service Catalog** as an architectural building block.

The concept is to establish **one canonical JSON representation and permanent Flow ID for every NIS-managed file flow**, regardless of whether the flow currently runs on EFEDS/IBM Sterling or is implemented on the new AWS NIS platform.

The JSON would provide different logical views from the same record:

• **Business View** – customer, business purpose, source, destination, files and schedule
• **Service View** – criticality, SLA and ownership
• **Operations View** – expected volume, monitoring, alerts and reporting
• **Technical View** – EFEDS/AWS platform, protocols, endpoints, security and implementation details
• **Governance/Migration View** – lifecycle, migration readiness, dependencies, testing and cutover status

This gives us a technology-neutral definition of a **File Flow as a Service**, with EFEDS and AWS becoming the underlying execution platforms.

I see several immediate use cases:

**Existing EFEDS flows:** discover and register them in a normalized format, understand dependencies and use the catalog to drive migration assessment and wave planning.

**New flows:** capture the business requirement first, create the Flow ID/catalog record, validate it and use the technical portion to drive AWS self-service provisioning.

**Operations:** use the same Flow ID across monitoring, hourly/daily volume reporting, SLA tracking and support.

**Future changes:** additions or modifications to a flow become lifecycle changes to an existing service rather than disconnected configuration requests.

Conceptually:

**Customer → Business Service → File Flow → Service Catalog → EFEDS / AWS NIS**

Over time, I believe the catalog could become the common foundation for **discovery → onboarding → provisioning → operations → migration → retirement**, and potentially enable automation to transform an existing EFEDS flow definition into an AWS onboarding request.

I’d like us to discuss whether we can incorporate this into the Phase 2 architecture so the self-service JSON evolves beyond just a provisioning contract and becomes part of the broader File Flow service lifecycle.

The strongest point to emphasize in discussion is: **we are not proposing another inventory database. We are defining the canonical identity and lifecycle of a file flow.** That distinction should help both the AWS team and internal stakeholders see why this belongs in Phase 2.

