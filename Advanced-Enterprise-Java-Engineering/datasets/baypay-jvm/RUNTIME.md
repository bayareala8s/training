# BayPay JVM runtime — synthetic notes for Modules 7–8

**Fictional.** Hosts, pods, and dumps are teaching data. Not a real employer’s JVM estate.

Students may read this file. Instructor RCAs live only under `solutions/`.

## Teaching runtime (local)

`reference-apps/baypay` — Java 21, Spring Boot 3.5.5, G1 by default, one process (`payment-service` composition root).

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
./mvnw -pl payment-service -am spring-boot:run
```

Useful flags students will turn on in Module 7 labs (never required in production dumps):

```text
-XX:+UnlockDiagnosticVMOptions
-XX:NativeMemoryTracking=summary
-Xlog:gc*:file=gc.log:time,uptime,level,tags
```

`jcmd <pid> GC.heap_info`, `VM.native_memory summary`, `Thread.print`, `GC.class_histogram`.

## Synthetic prod-east canary (Module 8 incidents)

| Instance | Role |
|---|---|
| `pay-prod-east-1` | Stable `payment-service` 3.8.0 — usually healthy |
| `pay-prod-east-2` | Canary — first place pages land in Module 8 |
| `fx-east.baypay.example` | Downstream FX quote (used when an incident mentions it) |
| Container (when named) | cgroup memory limit stated in that pack |

Demo customer Avery Chen: `11111111-1111-1111-1111-111111111111`.  
Active account: `22222222-2222-2222-2222-222222222221`.

On-call: Riley Okonkwo. SRE: Priya Nair. Release: Jordan Voss.

## What these modules are not

- Module 7 is **observe and explain**, not “tune GC for a 1% win.”
- Module 8 is **gated evidence**. A lucky label (leak, deadlock, OOM) does not max Diagnostic method.
- Module 5 WAS cell incidents are a different estate. Do not bounce `dmgr-east` for a Boot canary page.
- Do not recommend `-Xmx` equal to the container limit. Leave headroom for metaspace, stacks, and native.
- Do not treat a heap histogram as a closed leak without a growth story.

## Optional PAKS

- Module 7: `docs/01-computer-architecture/cpu-and-memory-fundamentals.md`
- Module 8: `docs/27-production-failures/failure-analysis-methodology.md`

Lessons stand alone without PAKS.
