# Heap class histogram — pay-prod-east-2

**Captured:** 2026-10-14T22:38:00Z  
**Gate:** 3  
**Command (teaching equivalent):** `jcmd 23255 GC.class_histogram`  
**Synthetic BayPay.** Taken a few seconds after a young collection.

```text
 num     #instances         #bytes  class name (module)
-------------------------------------------------------
   1:       1842201     147376080  [C
   2:        920410      22089840  java.lang.String
   3:        410208      13126656  java.lang.Object[]
   4:         88402       4243296  java.util.HashMap$Node
   5:          2408       1541120  com.baypay.shared.domain.Payment
   6:          1880        752000  com.baypay.shared.domain.Account
   7:          1620        518400  com.baypay.shared.domain.AuditEvent
   8:          1108        354560  com.baypay.shared.idempotency.IdempotencyRecord
   9:           640        204800  ch.qos.logback.classic.spi.LoggingEvent
  10:           214         68480  org.hibernate.engine.spi.EntityEntry
```

## Notes from the capture

- A second histogram 20 seconds later (Priya, bridge paste) showed `[C` and `String` counts **within 8%** of this snapshot after another young GC — the set is **turning over**, not accumulating in old gen.
- `IdempotencyRecord` is ~1.1k, not ~1.1M. Do not import INCIDENT-802’s retained map into this page.
- `Payment` / `Account` counts are in the thousands. Bytes are dominated by character arrays and `String`.
- Old generation on the dashboard stayed ~228 MB through the pause storm.

No `OutOfMemoryError`. No classloader leak signature.
