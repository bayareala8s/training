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
