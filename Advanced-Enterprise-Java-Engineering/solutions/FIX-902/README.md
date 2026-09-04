# FIX-902 — Instructor solution

**Do not walk the room to this list in the first 20 minutes.** Students should inventory symptoms first. The student guide hides this RCA (`hideAnswerUpfront`).

## Root causes in `labs/FIX-902/starter/Dockerfile`

The contractor file is parseable and wrong.

1. **`FROM ubuntu:latest`.** A general OS plus a floating tag. Every rebuild can change the userland. The image is not a JRE contract.
2. **`apt-get install openjdk-21-jdk`.** The runtime includes a full JDK and the Ubuntu package graph. That is why the image is huge.
3. **`USER root`.** Explicit root. CLUSTER.md requires numeric UID `10001`.
4. **`ENV BAYPAY_DB_PASSWORD=changeme-baypay`.** The secret is a layer. `docker history` and any registry copy keep it. Rotation cannot save a tag that already shipped.
5. **`COPY . .`.** The entire build context (source, `.git` if present, local env files) enters the image. Secrets and size both suffer.
6. **`:latest`.** Combined with Ubuntu, there is no reproducible base for a payments review.

There is no HEALTHCHECK requirement in this lab. Missing HEALTHCHECK is not a scored defect.

## Clean shape

See [Dockerfile](Dockerfile). Multi-stage Temurin JDK build with the Maven Wrapper, `eclipse-temurin:21-jre` runtime, JAR-only copy, `EXPOSE 8080`, `USER 10001`, no password `ENV`.

## Defect → repair

| Starter defect | Repair |
|---|---|
| `ubuntu:latest` | `eclipse-temurin:21-jre` as the final `FROM` (tag, not `latest`) |
| `apt-get install openjdk-21-jdk` | Compile in a `21-jdk` **build** stage; do not apt-install Java |
| `USER root` | `USER 10001` |
| `ENV BAYPAY_DB_PASSWORD=changeme-baypay` | Delete the assignment. Inject `BAYPAY_DB_*` at runtime |
| `COPY . .` on the runnable image | `COPY --from=build` the JAR only |
| `:latest` | Pin `21-jre` (SECURITY-903 may add a digest) |

## Facilitation

- If a student only adds `USER 10001` and leaves Ubuntu + apt + password, cap Technical accuracy and Security / reliability.
- If they remove the password but keep `USER root` and `:latest`, cap Diagnostic method.
- A lucky paste of `solutions/BUILD-901/Dockerfile` without a private defect inventory caps Diagnostic method.
- Full marks require a file that meets CLUSTER.md **and** a written inventory that names size, history, and root (the symptoms operations reported) with the matching lines.

## Optional Docker

Not required. `docker history` on a student-built starter tag is extra evidence, not the grade path.

## Scoring notes

`changeme-baypay` remaining in the submitted file caps Security / reliability. `USER root` remaining caps Security / reliability and Technical accuracy. Do not award high Diagnostic for “the Dockerfile is messy” without naming at least secret-in-layer, root, and oversized base.
