# Common Misconceptions — Module 06

| Misconception | Reality | Teaching move |
| ------------- | ------- | ------------- |
| Async/events are always better | User journeys often need sync reads/writes with clear latency SLAs | Score account lookup as sync-primary |
| Files are legacy-only | Partner ecosystems still require bulk file exchange | Partner landing swimlane |
| Platform owns event meaning | Domains own semantics; platform owns mechanisms | Ownership board stickies |
| One ESB fits every interaction | Pattern mismatch creates coupling and failure-mode debt | Force matrix scores per interface |
| Lab public API is production-ready | Missing authZ is intentional teaching debt | Explicit “not prod” callout in demo |
| No DLQ needed if volume is low | Poison messages still stall consumers | Ask poison-message fate |
| Transfer Family is required to learn file patterns | S3 landing simulates file arrival for lab cost control | ADR-M06-02 cost discussion |
| Master data can live in partner files | Files are exchange formats; masters need owned systems of record | Dual-master callout from Module 03 |
| Shared database “just for now” is fine | Hidden coupling becomes permanent | Ban shared-DB in lab designs |
| Schema versioning can wait | Breaking event changes break unknown consumers | Payment event versioning stretch |
