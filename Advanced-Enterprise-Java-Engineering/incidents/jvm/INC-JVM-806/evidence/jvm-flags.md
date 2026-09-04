# JVM flags and last GC — pay-prod-east-2

**Captured:** 2026-10-15T23:52:40Z (current Running container, 11 minutes after last restart)  
**Gate:** 3  
**Command (teaching equivalent):** `jcmd 1 VM.flags` plus `jcmd 1 GC.heap_info`  
**Synthetic BayPay.**

## `JAVA_TOOL_OPTIONS` (container env)

```text
JAVA_TOOL_OPTIONS=-Xmx512m -Xms512m
```

## Effective flags (excerpt)

```text
-XX:+UseContainerSupport
-XX:MaxHeapSize=536870912
-XX:InitialHeapSize=536870912
-XX:+UseG1GC
-XX:NativeMemoryTracking=off
```

`MaxHeapSize` is **512 MiB**. The pod memory **limit is 512Mi**. Heap max equals the cgroup limit.

## `GC.heap_info` (same instant)

```text
 garbage-first heap   total 524288K, used 398112K [0x00000000e0000000, 0x0000000100000000)
  region size 1024K, 18 young (18432K), 3 survivors (3072K)
 Metaspace       used 90112K, committed 92160K, reserved 1179648K
```

Heap used ~389 MB / 512 MB. The previous container was killed at RSS 512Mi while heap used was ~402 MB (dashboard last scrape). Headroom for metaspace, thread stacks, direct buffers, and native is **inside** the same 512Mi.

## Contrast (east-1, not this container)

```text
limit 2Gi
-Xmx1536m
```

That pairing leaves ~512Mi outside the heap. east-1 has not been `OOMKilled`.

## Last GC line recovered from the **previous** container (emptyDir scrap)

```text
[2026-10-15T23:40:51.002+0000][info][gc] GC(88) Pause Young (Normal) (G1 Evacuation Pause) 412M->389M(512M) 18.440ms
```

Last successful young GC finished at **389M used of 512M** about a minute before the 16:41 Pacific `OOMKilled`. No Java heap OOME line in that scrap.
