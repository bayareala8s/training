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
