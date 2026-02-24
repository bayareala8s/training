This section defines all human and automated actors that interact with the EFT Platform and describes the interfaces through which traffic enters, exits, or traverses the system. The objective of this section is to clearly identify:

Actor type (human or automated)

Trust level

Whether interaction is attended or unattended

Interface protocol

Authentication and authorization model

Direction and purpose of information flow

Security controls applied

For clarity, a Universal Interface represents a single instance of system traffic (for example, one SFTP session, one HTTPS request, or one S3 PUT event). A Universal Interface does not represent a user or system principal itself, but rather a discrete request or transaction initiated by that actor.

Standard enterprise management flows (e.g., AWS platform-native operational traffic) are governed by existing organizational security controls and are not enumerated individually in this section. Where applicable, references to enterprise standard controls are provided in the Security section.

If any actor flow contains documented exceptions, risk acceptances, or POA&Ms, those conditions are explicitly captured in Section X – Security Considerations.

Actors are categorized into two primary groups:

Human Actors (Attended Interfaces)

Automated Actors (Unattended Interfaces)



I-1 – External Automated Actor (Unattended, Lowest Trust)

The I-1 resource profile represents external automated systems that interact with the EFT Platform without human intervention. These actors originate outside of the AWS GovCloud trust boundary and therefore operate at the lowest trust level within the system’s actor classification model. Typical examples include external partner systems uploading files via SFTP using AWS Transfer Family, partner applications invoking HTTPS-based APIs, or external systems performing S3 PUT operations into designated landing buckets.

All I-1 interactions are unattended and machine-to-machine in nature. Because these actors originate from untrusted or semi-trusted external networks, the platform enforces strict security controls at the boundary before traffic is admitted into the internal automation domain.

Authentication for I-1 actors requires strong cryptographic mechanisms, including SSH key-based authentication for SFTP connections or IAM role- or credential-based authentication for API and S3 interactions. All communications must be encrypted in transit using TLS or SSH protocols. Authorization is enforced through IAM policies implementing strict least-privilege principles, limiting actors to only the specific buckets, prefixes, or API operations explicitly required.

Network boundary controls ensure that ingress is permitted only through approved endpoints, such as AWS Transfer Family endpoints or explicitly exposed HTTPS APIs. Direct access to internal services is not permitted. All requests are subject to comprehensive logging and monitoring, including CloudTrail logging, S3 access logging, Transfer Family logs, and event tracking via EventBridge. File integrity validation mechanisms, such as checksum verification or size validation, are applied prior to downstream processing.

Due to their exposure to untrusted networks, I-1 actors represent the highest exposure risk within the platform’s actor model. As such, input validation, payload inspection, and defensive processing controls are mandatory. Where enabled in the platform roadmap, malware scanning or antivirus inspection may be integrated into the ingestion workflow to further reduce risk. These controls collectively ensure that externally sourced traffic is authenticated, validated, and auditable before it is processed within the trusted internal automation environment.






I-3 – Internal Business User (Attended, Moderate Trust)

The I-3 resource profile represents internal organizational users who interact with the EFT Platform through attended HTTPS interfaces. These users typically access the system for operational monitoring, reporting, or status review functions.

Authentication is integrated with enterprise single sign-on (SSO) mechanisms, ensuring alignment with corporate identity governance. Authorization is governed by RBAC policies that restrict access to only approved datasets and operational views. Internal business users generally have read-only access to transfer metadata and reporting dashboards.

All traffic is encrypted using TLS, and access is logged through centralized audit logging systems. Audit records include user identity, access timestamps, queries performed, and any data export activity.

While I-3 actors operate within the organizational boundary, access segregation remains critical, particularly in multi-tenant or customer-segmented environments. Controls ensure that internal users cannot access data beyond their authorized scope.


Excellent. Below are the remaining **I-2 through I-8 profiles written in formal SADD narrative format**, consistent with the I-1 section. These can be placed directly under Section 4 in your SADD.

---

## I-2 – External Human User (Attended, Lower Trust)

The I-2 resource profile represents external human users who interact directly with the EFT Platform through attended interfaces. These actors are external to the AWS GovCloud trust boundary but initiate interactions manually rather than through automated systems. Examples may include partner users accessing a secure portal to retrieve transfer status or submit requests via HTTPS-based interfaces.

All I-2 interactions are attended and occur through secure web-based interfaces. Because these users originate outside the internal trust boundary, the platform applies strong identity verification and session controls. Authentication is enforced using federated identity providers or approved IAM user accounts, with multi-factor authentication (MFA) required where supported. Authorization is implemented through role-based access control (RBAC), ensuring that users are restricted to the minimum dataset and functionality required for their role.

All communication is encrypted in transit using TLS. Session management controls include inactivity timeouts, account lockout policies, and protection against session hijacking. Detailed session logs, including login events, access attempts, and data retrieval actions, are recorded for audit and forensic purposes.

Although I-2 actors operate in an attended context, they present moderate risk due to potential credential compromise or social engineering attacks. Therefore, strict identity management and continuous monitoring controls are enforced.

---

## I-3 – Internal Business User (Attended, Moderate Trust)

The I-3 resource profile represents internal organizational users who interact with the EFT Platform through attended HTTPS interfaces. These users typically access the system for operational monitoring, reporting, or status review functions.

Authentication is integrated with enterprise single sign-on (SSO) mechanisms, ensuring alignment with corporate identity governance. Authorization is governed by RBAC policies that restrict access to only approved datasets and operational views. Internal business users generally have read-only access to transfer metadata and reporting dashboards.

All traffic is encrypted using TLS, and access is logged through centralized audit logging systems. Audit records include user identity, access timestamps, queries performed, and any data export activity.

While I-3 actors operate within the organizational boundary, access segregation remains critical, particularly in multi-tenant or customer-segmented environments. Controls ensure that internal users cannot access data beyond their authorized scope.

---

## I-4 – Privileged Administrative User (Attended, Elevated Trust)

The I-4 resource profile represents internal users with elevated administrative privileges. These actors have the ability to modify system configuration, manage IAM roles, adjust encryption policies, or initiate operational overrides such as file replay or configuration updates.

Because of the elevated impact potential associated with these privileges, I-4 interactions require strict security enforcement. Authentication mandates multi-factor authentication (MFA), and authorization is implemented through tightly scoped privileged IAM roles. Access may be granted through controlled workflows such as approval-based CI/CD pipelines or just-in-time access mechanisms.

All administrative actions are comprehensively logged using immutable audit logging (e.g., CloudTrail with retention enforcement). Configuration changes are tracked through version-controlled infrastructure-as-code processes, and separation of duties principles are enforced to prevent unilateral high-risk changes.

Although I-4 actors operate within a high-trust internal environment, the potential impact of misuse is significant. Therefore, governance and oversight controls are prioritized over boundary validation.

---

## I-5 – Management and Governance (Attended, Oversight Role)

The I-5 resource profile represents internal governance stakeholders, such as compliance teams or executive management, who access reporting or audit artifacts but do not modify system configuration.

Interactions are attended and occur through secured dashboards or exported compliance reports. Authentication is enforced via enterprise SSO, and authorization is limited to read-only governance roles.

Security controls emphasize data confidentiality and integrity. Audit logs must be immutable and tamper-evident, ensuring compliance with regulatory requirements. Data exports are controlled and monitored to prevent unauthorized dissemination of sensitive information.

While I-5 actors do not possess system modification capabilities, the sensitivity of accessible data requires careful access restriction and monitoring.

---

## I-6 – Internal Automated Management Systems (Unattended, High Trust)

The I-6 resource profile represents internal automated systems responsible for management and orchestration functions, such as CI/CD pipelines, monitoring services, infrastructure automation, and configuration deployment workflows.

These interactions are unattended and occur within the AWS GovCloud boundary using IAM service roles. Authorization is implemented through scoped IAM policies aligned with least-privilege principles.

Deployment workflows are version-controlled, approval-gated, and logged. Configuration drift detection and monitoring systems validate the integrity of deployed infrastructure. Logs generated by automation components are retained and monitored for anomaly detection.

Although I-6 actors operate at high trust, misconfiguration risk is a primary concern. Therefore, governance controls and change validation mechanisms are critical.

---

## I-7 – Intra-Enclave Automated Service (Unattended, Controlled Internal Domain)

The I-7 resource profile represents automated service-to-service communication occurring entirely within the same enclave or internal domain. Examples include Lambda functions invoking DynamoDB, Step Functions orchestrating ECS tasks, or internal services communicating via private networking constructs.

All I-7 interactions are unattended and occur over private networking boundaries without exposure to public endpoints. Authentication is enforced through IAM role-to-role trust relationships. Authorization policies restrict each service to explicitly defined resources.

Encryption in transit is enforced through AWS-managed secure channels. Detailed service logs, execution traces, and correlation identifiers support monitoring and diagnostics.

The primary risk consideration for I-7 actors is lateral movement within the internal domain. Therefore, service-level isolation and least-privilege IAM scoping are critical safeguards.

---

## I-8 – Inter-Enclave Automated Actor (Unattended, Cross-Domain)

The I-8 resource profile represents automated systems interacting across enclave boundaries, such as cross-region replication, cross-account event routing, or inter-environment synchronization.

These interactions are unattended and governed by explicit cross-account IAM trust policies. Encryption in transit and at rest is mandatory, particularly when replication or cross-region data movement is involved.

Monitoring controls must detect replication failures, latency, or divergence. Given that cross-region replication may involve eventual consistency (e.g., S3 replication RPO considerations), the system must account for potential temporary inconsistencies.

Audit logs must capture cross-boundary operations, and failover procedures must be documented to ensure continuity in the event of regional impairment.

I-8 interactions represent segmented high trust but introduce cross-boundary complexity. Controls focus on explicit trust configuration, replication validation, and comprehensive monitoring.



