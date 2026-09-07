# BUILD-901 — starter defects (before edit)

Starter `labs/BUILD-901/starter/Dockerfile` left unchanged. Completed file: `work/Dockerfile`.

| Defect vs CLUSTER.md | Starter |
|---|---|
| Single `FROM eclipse-temurin:21-jdk` | JDK is the **runtime**. Compiler in production. |
| No named build stage | Cannot `COPY --from=build` a JAR only. |
| `COPY . .` then `java -jar` from target | Ships source + `target/` as the running tree. |
| No `USER` | Process is **root**. |
| No comment that `BAYPAY_DB_*` is runtime | Easy to “fix” with `ENV` password (FIX-902). |
| No `-Xmx` (good) | Keep it that way. |

Context if you ever build: `reference-apps/baypay` (where `mvnw` lives).
