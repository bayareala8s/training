# PERFORMANCE-904 — Instructor solution

**Do not share these files with students before they write COPY order and `JAVA_TOOL_OPTIONS`.**

## Files

| File | Role |
|---|---|
| [Dockerfile](Dockerfile) | Pom-first cache, `dependency:go-offline`, JRE runtime, `MaxRAMPercentage=75.0` |

## Build-cache contract

1. Copy `mvnw`, `.mvn/`, reactor `pom.xml`.
2. Copy each module `pom.xml` (`shared`, `payment-service`, `refund-service`, `notification-service`, `transaction-worker`).
3. `RUN ./mvnw -pl payment-service -am dependency:go-offline -B`.
4. Copy module sources.
5. `RUN ./mvnw -pl payment-service -am -DskipTests package`.

A student who copies poms first and packages in a **single** later `RUN` (without `go-offline`) can still score well on Technical accuracy if the COPY order is correct and they explain why. `go-offline` is the preferred explicit resolve.

## Runtime contract

```text
FROM eclipse-temurin:21-jre
ENV JAVA_TOOL_OPTIONS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
USER 10001
```

- `UseContainerSupport` stays on (Java 21 default; still declare it).
- `MaxRAMPercentage` is **75**, not 100, not omitted in favor of `-Xmx` = limit.
- Do **not** set `-Xmx` equal to the container memory limit.
- Do **not** set `-Xmx512m` on a 512 MiB teaching limit (INCIDENT-806).
- A reviewed explicit `-Xmx384m` on a 512 MiB limit is an acceptable **trade-off answer**. Prefer percentage in the file.

## Why heap ≠ limit

Heap is one resident consumer. Metaspace, thread stacks, code cache, GC structures, direct buffers, and glibc sit on top. `MaxRAMPercentage=75` on a 512 MiB cgroup ≈ 384 MiB heap and ~128 MiB native headroom (LAB-704). `MaxRAMPercentage=100` is the same outage class as `-Xmx` = limit.

## Optional `jlink`

Not required. A high Trade-off answer names `jlink` as a smaller custom runtime when the team will own module lists and rebuilds; `21-jre` is the course default.

## Checklist

- [x] Poms before sources
- [x] Resolve before source compile (preferred)
- [x] Runtime JRE
- [x] `JAVA_TOOL_OPTIONS` with `UseContainerSupport` and `MaxRAMPercentage` < 100
- [x] No `-Xmx` equal to a memory limit
- [x] `USER 10001`, no secrets

## Scoring notes

`-Xmx` equal to the limit cannot score high on Technical accuracy, Production awareness, or Security / reliability. A JDK runtime “for jcmd” fails Production awareness. Skipping Docker is not an Efficiency penalty. `jlink` absence is not a deduction.
