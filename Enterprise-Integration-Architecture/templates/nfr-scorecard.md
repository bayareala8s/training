# NFR scorecard (optional worksheet)

Use before choosing a style. Copy into lab or capstone notes.

| Characteristic | Value / SLO | Implication |
|----------------|-------------|-------------|
| Latency | | Sync API vs async |
| Payload size | | File / claim-check vs JSON API |
| Consumers | 1 / many / unknown | Queue vs event vs API |
| Protocol constraint | REST / SFTP / MQ / other | Adapter vs native |
| Sensitivity | public / internal / confidential / restricted | Authz, minimization, audit |
| Availability of destination | | Buffer (queue) vs fail the caller |
| Ordering | | FIFO / outbox / don’t pretend |
| Cost of the edge | hourly vs per-request | Transfer Family, NAT, always-on bus |

**Style chosen:**  
**Rejected:**  
**AWS mapping (last):**  
