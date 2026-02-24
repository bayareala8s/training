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
