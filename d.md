{
  "schemaVersion": "1.0",
  "flowId": "FLOW-004287",
  "flowName": "Daily Business Data Transfer",
  "service": {
    "customer": "Customer A",
    "businessService": "Business Processing",
    "businessPurpose": "Supports downstream business processing.",
    "environment": "PROD",
    "status": "PROPOSED",
    "criticality": "HIGH"
  },
  "flow": {
    "from": {
      "organization": "Organization A",
      "application": "Application A"
    },
    "to": {
      "organization": "Organization B",
      "application": "Application B"
    },
    "direction": "INBOUND",
    "flowType": "APPLICATION_TO_APPLICATION"
  },
  "files": {
    "businessFileType": "Business Data Files",
    "filePattern": "DATA_*.CSV",
    "fileFormat": "CSV",
    "expectedVolume": {
      "filesPerHour": 250,
      "filesPerDay": 6000
    },
    "fileSize": {
      "averageMB": 25,
      "maximumMB": 350
    }
  },
  "schedule": {
    "frequency": "HOURLY",
    "trigger": "FILE_ARRIVAL",
    "serviceWindow": "24x7"
  },
  "serviceLevel": {
    "classification": "BUSINESS_CRITICAL",
    "expectedDeliveryMinutes": 30,
    "missingFileThresholdMinutes": 60
  },
  "ownership": {
    "businessOwner": "Business Team A",
    "applicationOwner": "Application Team A",
    "serviceOwner": "File Transfer Services",
    "supportTeam": "File Transfer Operations"
  },
  "security": {
    "dataClassification": "CONFIDENTIAL",
    "authentication": "SSH_KEY",
    "transportEncryption": "SSH",
    "fileEncryption": "PGP"
  },
  "monitoring": {
    "transferFailureAlert": true,
    "missingFileAlert": true,
    "volumeMonitoring": true,
    "latencyMonitoring": true,
    "hourlyVolumeReport": true,
    "dailyVolumeReport": true
  },
  "implementation": {
    "platform": "CLOUD_MFT",
    "implementationPattern": "SFTP_TO_OBJECT_STORAGE",
    "source": {
      "protocol": "SFTP",
      "endpoint": "source-endpoint",
      "port": 22,
      "directory": "/outbound/data"
    },
    "destination": {
      "type": "OBJECT_STORAGE",
      "endpoint": "target-storage",
      "directory": "/incoming/data"
    },
    "resiliency": {
      "highAvailabilityRequired": true,
      "disasterRecoveryRequired": true
    }
  },
  "lifecycle": {
    "origin": "EXISTING",
    "onboardingMethod": "MIGRATION",
    "catalogStatus": "REGISTERED",
    "createdDate": "2026-09-17",
    "lastReviewedDate": "2026-09-17"
  },
  "migration": {
    "applicable": true,
    "sourcePlatform": "LEGACY_MFT",
    "targetPlatform": "CLOUD_MFT",
    "status": "ASSESSED",
    "complexity": "LOW",
    "migrationWave": "TBD",
    "dependencies": []
  },
  "review": {
    "classification": "PIPELINE_GAP",
    "selfServiceEligible": false,
    "decision": "PIPELINE_GAP",
    "implementationPattern": "SFTP_TO_OBJECT_STORAGE",
    "domainAssessments": {
      "catalog": "PASS",
      "architecture": "PASS",
      "security": "PASS",
      "operations": "PASS",
      "resiliency": "PASS",
      "pipelineCapability": "GAP",
      "migration": "NOT_READY"
    },
    "guardrailValidation": {
      "supportedProtocol": true,
      "supportedSourceDestination": true,
      "fileSizeWithinLimit": true,
      "volumeWithinLimit": true,
      "supportedSchedule": true,
      "serviceLevelSupported": true,
      "securityRequirementsSupported": true,
      "resiliencyRequirementsSupported": true
    },
    "gaps": [
      {
        "domain": "PIPELINE_CAPABILITY",
        "capability": "PGP_PROVISIONING",
        "description": "The approved flow requires PGP encryption, but the current GitLab provisioning pipeline does not automate this capability."
      }
    ],
    "requiredReviews": {
      "architectureReview": false,
      "securityReview": false,
      "operationsReview": false,
      "capacityReview": false,
      "pipelineEngineeringReview": true,
      "migrationReview": true
    },
    "decisionReason": "The flow meets the approved architecture, security, operational and resiliency guardrails, but the current provisioning pipeline cannot implement all required capabilities.",
    "recommendedAction": {
      "owner": "PIPELINE_ENGINEERING",
      "action": "ADD_PGP_PROVISIONING_CAPABILITY"
    },
    "reviewStatus": "BLOCKED_BY_PIPELINE_CAPABILITY",
    "lastEvaluatedDate": "2026-09-17"
  }
}


Team — as we review upcoming file flows, I’d like to propose a **Service Catalog–driven Rules Engine** to make our flow implementation decisions more standardized, repeatable and self-service.

Each flow would have a canonical Service Catalog definition covering the business requirement, source/destination, file characteristics, SLA, security, monitoring, resiliency and implementation requirements.

The Rules Engine would evaluate that definition against agreed **Architecture, Security, Operations and Resiliency guardrails**, determine the approved implementation pattern, and then validate whether our **GitLab provisioning pipeline** can implement the complete flow.

**Service Catalog → Rules Engine → Guardrail Validation → Standard Pattern / Exception → GitLab Capability Check → Provisioning**

The engine would distinguish between a true **architecture exception** and a **pipeline capability gap**. This is important because a flow may fully comply with our approved architecture but still require a capability that our current automation does not yet provision.

For standard flows that satisfy the guardrails and pipeline capabilities, the team could proceed through a self-service path. Architecture and other specialized reviews would primarily focus on exceptions.

The same framework can also support existing-flow migration by determining whether a flow meets the target architecture and whether the pipeline has everything required to provision it.

I’d like to use a small set of upcoming flows to validate the rules and demonstrate the approach with the working Python reference implementation.


Here’s a concise description you can use directly in architecture documentation or when walking stakeholders through the JSON.

| JSON Section                   | Purpose                                                                                                                      |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **schemaVersion**              | Identifies the version of the canonical Service Catalog schema.                                                              |
| **flowId**                     | Provides a unique, persistent identifier for the file flow throughout its lifecycle.                                         |
| **flowName**                   | Provides a human-readable name for identifying the flow.                                                                     |
| **service**                    | Captures the business context, customer, environment, purpose and criticality of the flow.                                   |
| **flow**                       | Defines the logical source-to-destination relationship and direction of the transfer.                                        |
| **files**                      | Describes file characteristics including format, pattern, expected volume and file size.                                     |
| **schedule**                   | Defines when and how frequently files are expected to be transferred.                                                        |
| **serviceLevel**               | Captures delivery expectations, SLA and missing-file thresholds.                                                             |
| **ownership**                  | Identifies business, application, service and operational accountability for the flow.                                       |
| **security**                   | Defines data classification, authentication and encryption requirements.                                                     |
| **monitoring**                 | Defines operational monitoring, alerting and reporting requirements.                                                         |
| **implementation**             | Describes the target technical platform, transfer pattern, endpoints and resiliency requirements.                            |
| **lifecycle**                  | Tracks where the flow is in its onboarding, operation or migration lifecycle.                                                |
| **migration**                  | Captures migration applicability, source/target platforms, complexity, dependencies and migration status.                    |
| **review**                     | Stores the Rules Engine's assessment and final decision for the flow.                                                        |
| **review.domainAssessments**   | Shows PASS/GAP results independently across Catalog, Architecture, Security, Operations, Resiliency, Pipeline and Migration. |
| **review.guardrailValidation** | Records whether individual architectural requirements satisfy approved standards.                                            |
| **review.gaps**                | Identifies the specific capabilities or requirements preventing self-service provisioning.                                   |
| **review.requiredReviews**     | Determines which teams—Architecture, Security, Operations, Pipeline Engineering, etc.—need to review the flow.               |
| **review.decisionReason**      | Provides a human-readable explanation of why the Rules Engine reached its decision.                                          |
| **review.recommendedAction**   | Identifies the next action and responsible team needed to move the flow forward.                                             |
| **review.reviewStatus**        | Provides the final workflow status, such as ready, exception, incomplete or blocked by pipeline capability.                  |

The simplest way to explain the overall structure to stakeholders is:

> **The first sections describe what the flow requires; `implementation` describes how it should be implemented; and `review` captures the Rules Engine's evaluation, gaps, required reviews and resulting decision.**
