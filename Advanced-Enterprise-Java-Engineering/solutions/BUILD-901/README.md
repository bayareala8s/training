# BUILD-901 — Instructor solution

**Do not share these files with students before they submit a checklist-complete Dockerfile.**

This folder is the answer key for containerizing `payment-service` **on disk**. Students are not required to run Docker or Podman.

## Files

| File | Role |
|---|---|
| [Dockerfile](Dockerfile) | Multi-stage: Maven Wrapper on `21-jdk`, runtime `21-jre`, `EXPOSE 8080`, `USER 10001` |

A student file that matches contracts (two stages, Wrapper build, JRE runtime, port, UID, no secrets) passes even if `WORKDIR` paths or the JAR file name differ.

## What the starter got wrong

- Single `FROM eclipse-temurin:21-jdk` — the compiler image was also the runtime.
- No `USER` instruction — the JVM would start as root.
- `COPY . .` into that one stage left source in the runnable image.

The starter was valid-looking syntax. It was not the CLUSTER.md contract.

## Required contracts

```text
build:     eclipse-temurin:21-jdk + ./mvnw -pl payment-service -am -DskipTests package
runtime:   eclipse-temurin:21-jre
copy:      JAR only via COPY --from=build
port:      EXPOSE 8080
user:      USER 10001
secrets:   none in the file — BAYPAY_DB_* at process start
heap:      do not set -Xmx equal to a memory limit (do not set -Xmx here)
```

Build context, if anyone builds: `reference-apps/baypay`.

## Checklist (same as the student lab)

- [x] Two `FROM` stages
- [x] Runtime is `21-jre`
- [x] `WORKDIR` present
- [x] JAR copied from the build stage
- [x] `EXPOSE 8080`
- [x] `USER 10001`
- [x] No password `ENV`
- [x] Maven Wrapper used in the build stage

## Optional Docker

Not required. If a student builds locally, treat it as extra. Do not deduct Efficiency for skipping the engine. Do deduct Production awareness if they keep a JDK runtime “so we can jcmd.”

## Diagram

AEJE-D-039: JDK build stage packages the JAR; JRE runtime copies it, exposes 8080, runs as `10001`. Database credentials are runtime environment.

## Scoring notes

Full marks require the stage split, JRE runtime, `USER 10001`, Wrapper build, and no secrets. A single-stage JDK file fails Technical accuracy. A password `ENV` fails Security / reliability regardless of stages. Optional `docker build` neither raises nor lowers the score.
