Subject: Transitioning from On-Premises Infrastructure to the Cloud – A Step Toward Modernization

Dear [Customer Name/Valued Customer],

As part of our ongoing efforts to support your digital transformation journey, we are excited to assist you in transitioning from traditional on-premises infrastructure to a more scalable, secure, and cost-efficient cloud environment.

This move offers several benefits, including:

Enhanced scalability and flexibility

Improved security posture

Cost optimization through pay-as-you-go models

Faster deployment and innovation cycles

the ingress path from external SFTP clients to the NIS SFTP server:

SFTP Client Ingress Path to NIS SFTP Server
To ensure secure, scalable, and reliable access, incoming SFTP traffic from external clients to the NIS SFTP server follows a multi-layered ingress architecture. Here's how the flow works:

1. SFTP Client Connection Initiation
External SFTP clients initiate a connection to a public DNS name (e.g., sftp.customer-domain.com) that is managed via Amazon Route 53.

This DNS entry is mapped to an Akamai Edge endpoint, ensuring global traffic optimization and DDoS protection.

2. Akamai Edge Security & Routing
Akamai acts as the first line of defense, providing:

TLS termination and re-encryption (if enabled)

Bot protection and geo-filtering (if configured)

Caching and acceleration (if applicable)

Akamai then forwards the traffic to the next hop within the DMZ (Demilitarized Zone) via a secure and predefined route.

3. DMZ Layer (Network Isolation & Inspection)
The traffic lands in the DMZ, which serves as a buffer zone between the external network (internet) and internal systems.

Here, firewalls and inspection tools verify and log incoming sessions for compliance and threat detection.

Only whitelisted ports (typically TCP 22 for SFTP) and IP addresses are allowed to proceed.

4. Routing to Internal NIS SFTP Server
Once validated, the traffic is routed to the NIS-hosted SFTP server (e.g., AWS Transfer Family or a managed EC2-based SFTP endpoint).

This endpoint resides in a private subnet, protected by security groups and IAM roles, and is not directly accessible from the public internet.

Route 53 Private Hosted Zones (or VPC-specific endpoints) help route the traffic internally as needed for high availability and failover.

Key Benefits of This Architecture
Security: Multi-layer protection through Akamai, DMZ firewalls, and internal access control.

Scalability: Akamai offloads load and distributes traffic efficiently.

Resilience: DNS-based routing via Route 53 allows for disaster recovery and regional failover.



![image](https://github.com/user-attachments/assets/609f817d-62e3-408e-802b-7410fdad8346)

egress communication to external SFTP servers via the NIS External Landing Zone:

gress (From NIS to External SFTP Servers)
NIS can also initiate outbound SFTP connections to external servers using the NIS External Landing Zone, allowing for seamless integration with your partners, vendors, or legacy file systems:

Outbound SFTP traffic is securely routed through the NIS External Landing Zone.

Firewalls and route controls enforce compliance and logging.

This architecture allows automated scheduled transfers or manual push workflows to external destinations.

SFTP Connectivity Architecture
Inbound (Ingress) Traffic – External Clients to NIS SFTP Server
External SFTP clients securely connect to the NIS-hosted SFTP service through a layered ingress path:

Step	Description
1.	DNS Routing via Amazon Route 53: Public DNS (e.g., sftp.yourdomain.com) resolves to Akamai
2.	Akamai Edge Network: Delivers global traffic optimization, edge protection, and caching
3.	DMZ Firewall Layer: Validates sessions and restricts unauthorized access
4.	NIS SFTP Server (Private Network): Final destination within secure AWS environment

Outbound (Egress) Traffic – From NIS to External SFTP Servers
Outbound file transfers are initiated by NIS to third-party or customer-hosted SFTP endpoints via the NIS External Landing Zone:

Step	Description
1.	File Transfer Trigger: Scheduled or event-driven file movements originate from NIS
2.	Route via External Landing Zone: Egress traffic is securely routed through NAT gateways and firewalls
3.	Secure SFTP Connection: Encrypted connections established with external servers
4.	Logging & Governance: Transfer activity is logged and monitored for audit compliance

