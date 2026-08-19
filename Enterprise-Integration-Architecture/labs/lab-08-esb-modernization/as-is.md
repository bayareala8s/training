# As-is ESB (Lab 8)

Northbridge runs a central ESB (conceptual — not a vendor product).

Flows on the bus today:

1. Mobile balance lookup (sync SOAP through the bus to core) — 300 ms needed
2. Address change mapped to 12 downstreams via bus transforms
3. Marketing email triggered from the bus after any customer update
4. Nightly 8 GB settlement file dropped to the bus FTP adapter
5. ISO 20022 MQ to the scheme (certified map, two changes in five years)
6. Warehouse inventory commands during store hours; warehouse down Sundays
7. New collections SaaS — waiting 6 weeks for a map
8. A point-to-point JDBC from reporting that bypasses the bus (undocumented)

Problems: mapping lead time 6 weeks; weekend freezes; one bad map pages everyone; canonical Customer committee.

Produce keep/change/retire, strangler waves, dual-run for money, and `templates/adr.md`.
