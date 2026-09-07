# FIX-902 — private defect list (starter left unbroken)

Would fail a registry review of `labs/FIX-902/starter/Dockerfile`:

1. **`FROM ubuntu:latest`** — floating tag; general desktop OS, not `eclipse-temurin:21-jre`.
2. **`USER root` + `apt-get install openjdk-21-jdk`** — compiler via apt as the production story; image huge; process stays root.
3. **`ENV BAYPAY_DB_PASSWORD=changeme-baypay`** — password in every layer / `docker history`; rotation cannot rewrite the tag.
4. **`COPY . .` as the only copy** — whole build context (source, `.git`, tests) is the runtime filesystem.
5. **No `USER 10001`** — CLUSTER.md contract is a numeric non-root UID.
6. **No Maven Wrapper build stage** — assumes a JAR already sitting in `target/` inside that copied tree, or nothing to run.

Repair lives in `work/Dockerfile`. Starter is the foil.
