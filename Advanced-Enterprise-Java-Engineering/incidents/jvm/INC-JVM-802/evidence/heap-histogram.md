# Heap class histogram — pay-prod-east-2

**Captured:** 2026-10-08T21:48:00Z  
**Gate:** 3  
**Command (teaching equivalent):** `jcmd 22840 GC.class_histogram`  
**Synthetic BayPay.** Not a full HPROF.

```text
 num     #instances         #bytes  class name (module)
-------------------------------------------------------
   1:       2204102     352656320  [C
   2:       1102884     176461440  com.baypay.shared.idempotency.IdempotencyRecord
   3:       1102901     132348120  [B
   4:       1102890      52938720  java.util.concurrent.ConcurrentHashMap$Node
   5:         18402      17665920  [Ljava.util.concurrent.ConcurrentHashMap$Node;
   6:          2204       1410560  com.baypay.shared.domain.Payment
   7:          1988        795200  com.baypay.shared.domain.Account
   8:          1204        385280  java.util.HashMap
   9:           880        211200  java.lang.String  (distinct intern-ish; most payload is in [C / [B)
  10:           214         68480  org.hibernate.engine.spi.EntityEntry
```

## Notes from the capture

- Histogram taken after a full collection. Old generation was still **1280 MB**.
- `IdempotencyRecord` instance count matches the in-process cache `size=` log line at 21:42 UTC (1,102,880).
- `[C` and `[B` bytes are consistent with key strings and payload copies held by those records.
- `Payment` / `Account` counts are in the thousands, not millions.
- `pay-prod-east-1` histogram from the same hour (not in this pack; Priya’s note on the bridge): `IdempotencyRecord` instances **1,104** — DB-backed lookups, no in-process map of this size.

No `OutOfMemoryError` in the Java heap log yet. The replica was recycled earlier when readiness failed on heap used.
