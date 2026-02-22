Below is your updated **SADD-ready narrative**, incorporating the additional customer endpoint configuration details and failover expectations into the Active-Active Architecture section in formal, production-grade language.

---

## 10. Active-Active Architecture and Regional Strategy

This section defines the multi-region deployment strategy, the active-active execution model, and the disaster recovery behavior of the Self-Serve File Transfer Backend Engine deployed in AWS GovCloud. The architecture is designed to minimize blast radius, ensure regional independence, and provide controlled failover capabilities while maintaining operational transparency for customers.

The platform operates in a true active-active configuration across two AWS GovCloud regions: **us-gov-west-1** and **us-gov-east-1**. Both regions are fully provisioned and continuously active. There is no passive standby region. Each region hosts a complete control plane and data plane, including routing logic, workflow orchestration, storage, delivery execution, monitoring, and alerting.

Networking, outbound connectivity, and monitoring stacks are implemented independently per region to avoid shared failure domains. Each region can independently process file transfers, execute routing logic, and deliver files without dependency on the other region during steady-state operations.

---

## 10.1 Customer Endpoint and Regional Resource Model

Each sending customer is provisioned with region-aware and failover-capable endpoint configurations. Specifically, customers are assigned:

* DNS CNAME records for East, West, and a PRIMARY SFTP endpoint.
* A dedicated S3 bucket in the East region.
* A dedicated S3 bucket in the West region.
* DNS TXT records used for dynamic lookup of East, West, and PRIMARY bucket names.

All DNS records are configured with failover routing policies to allow traffic to shift away from a failed region. The PRIMARY endpoint acts as the canonical client-facing entry point, while region-specific CNAME records allow deterministic targeting when required.

DNS TXT record lookups enable dynamic destination identification for S3-based transfers. SDK-based clients are expected to leverage TXT lookups to determine the correct bucket per region. This mechanism supports dynamic routing without requiring hard-coded bucket names in client implementations.

This design provides the flexibility to isolate customer workloads, minimize blast radius, and shift traffic between regions without requiring architectural changes at the client level.

---

## 10.2 Failover Behavior and Operational Expectations

Failover between regions is controlled through DNS failover record updates managed by NIS. In the event of a regional impairment, DNS records are updated to route all inbound traffic to the designated failover region. Clients using PRIMARY endpoints will automatically resolve to the healthy region based on updated DNS policies.

Upon failover activation:

* Clients begin sending all new requests to the designated primary/failover region.
* SDK clients that do not use TXT lookup records to retrieve bucket names must manually retarget to the secondary region. NIS will issue operational notice in the event of failover to guide such clients.
* Strong consistency between regions is not guaranteed. Cross-region S3 replication has an RPO of up to 15 minutes. DynamoDB replication is typically under one minute. There is no formal SLA for inter-region latency.
* Customers are responsible for retrying any file submissions for which delivery success notifications were not received. Operational guidance may instruct customers to retry submissions within a defined time window following failover.
* The Managed File Transfer system implements best-effort duplicate prevention. If an MFT-TransferTracker record exists and indicates that a file has already been successfully delivered, the system will skip reprocessing to prevent duplicate sends.
* There are potential edge scenarios where files are successfully delivered to destination endpoints and recorded in MFT-TransferTracker but are not yet present in the replicated archive bucket due to cross-region replication timing.

This architecture prioritizes availability and operational continuity over strict inter-region synchronization. The system is designed to tolerate transient replication delays while minimizing duplicate delivery risk and preserving transfer audit integrity.

---

## 10.3 Consistency and Data Integrity Considerations

Because the system operates in active-active mode with independent regional execution, strong cross-region transactional consistency is not guaranteed. Data replication mechanisms operate asynchronously:

* S3 cross-region replication may have an RPO of up to approximately 15 minutes.
* DynamoDB global table replication typically occurs within less than one minute.
* Network latency between regions is variable and not covered by formal SLA guarantees.

The system mitigates risks associated with eventual consistency through:

* TransferTracker-based idempotency checks
* Duplicate detection logic
* Controlled replay mechanisms
* Explicit client retry guidance during failover events

These controls ensure that the system can maintain integrity and auditability even under regional disruption scenarios.

---

If you would like, I can now:

* Add a **Blast Radius Analysis subsection**
* Convert this into a formal **Disaster Recovery (DR) chapter**
* Add measurable **RTO/RPO commitments**
* Create a **failover sequence flow narrative**
* Or elevate this language further for ARC executive-level review**

Let me know the audience (technical review vs ARC board vs AWS review), and I will tune the tone accordingly.
