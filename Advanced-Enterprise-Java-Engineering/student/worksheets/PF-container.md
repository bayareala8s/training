# Portfolio worksheet — Container architecture

**Artifact:** Module 9 / [BUILD-901](../../labs/BUILD-901/README.md) · [SECURITY-903](../../labs/SECURITY-903/README.md) · [PERFORMANCE-904](../../labs/PERFORMANCE-904/README.md)  
**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Diagrams:** AEJE-D-039 (image), AEJE-D-040 (trust boundary)

Use this sheet to export a reviewer-ready excerpt. Fill every section in your own words. Do not paste secrets; all BayPay data is synthetic. Docker or Podman is optional — say whether you used an engine.

---

## 1. Identity

| Field | Your answer |
|---|---|
| Your name | |
| Date | 2026-09-06 |
| Engine used (`docker` / `podman` / files only) | **files only** (checklist path; no required daemon) |
| Reference commit or branch | Downloads workspace; optimized image: `labs/PERFORMANCE-904/Dockerfile` (901/903 predecessors in their labs) |

---

## 2. Image

Teaching registry and name from [CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md):

| Field | Your answer |
|---|---|
| Image name (`registry.../payment-service:<tag>`) | `registry.baypay.example/baypay/payment-service:<tag>` — never `:latest` |
| Build-stage base | `eclipse-temurin:21-jdk` as stage `build` |
| Runtime-stage base (must not be a full JDK) | `eclipse-temurin:21-jre` (final `FROM`) |
| How you pin the runtime (tag `21-jre` and/or digest) | Tag `21-jre` (never `:latest`). Prod pins a digest; Jordan owns CVE rebuilds (SECURITY-903). |
| What the runtime `COPY`s (JAR only?) | `COPY --from=build …/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar` only |
| Port (`EXPOSE`) | `8080` |
| How you invoke the process (`ENTRYPOINT` / `CMD`) | `ENTRYPOINT ["java", "-jar", "/app/app.jar"]` (exec form) |

AEJE-D-039 is the **image contract**, not ND in Docker. A JDK stage runs `./mvnw -pl payment-service -am package` so the compiler and Wrapper stay off the merchant process. A JRE stage copies **one JAR**, exposes **8080**, and runs as **10001**. `BAYPAY_DB_*` is an arrow **into** the running container, not a layer. Multi-stage is the BayPay default because “we already had a JDK for Maven” is how you ship `javac`, headers, and root-shaped tools next to Avery’s POST. A single JRE image that `COPY`s a laptop-built JAR is honest **only** if CI already produced that JAR; it is not an excuse to run `21-jdk` as the final stage. `registry.baypay.example` is a teaching name — not a reason to open ECR this week.

---

## 3. User

| Field | Your answer |
|---|---|
| UID in the Dockerfile | **10001** (`USER 10001` after the last `COPY`, before `ENTRYPOINT`) |
| Why not `root` | Riley will not ship a root JVM. Escape + writeable image = host-shaped damage. |
| What still has to be true in Module 10 `securityContext` | `runAsNonRoot: true` and `runAsUser: 10001` (numeric). A named `/etc/passwd` user is optional; kube still needs the **UID**. |

`USER 10001` means the JVM is not uid 0: a container break starts as an unprivileged user, and files copied as root in the image are typically **not** writable by the process (good for `/app/app.jar`, which is why we do not volume-mount the fat JAR over the image). It is **not** a cluster policy by itself. Module 10 must still set `runAsNonRoot` / `runAsUser: 10001` or a privileged pod spec can put root back. Numeric 10001 matches `runAsNonRoot` without inventing a name.

---

## 4. JVM flags

Do **not** recommend `-Xmx` equal to the container memory limit.

| Field | Your answer |
|---|---|
| `JAVA_TOOL_OPTIONS` you would ship | In `labs/PERFORMANCE-904/Dockerfile`: `-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0`. **No** `-Xmx` in the file. |
| `UseContainerSupport` on or off? | **On** (Java 21 default). The VM must see the **cgroup**, not the node’s RAM. Do not `-XX:-UseContainerSupport`. |
| `MaxRAMPercentage` value and why it is not 100 | **75** — leftover ~25% is native headroom. 100% (or `-Xmx` = limit) is INC-JVM-806. |
| Native consumers that sit **beside** the heap | Metaspace, thread stacks, code cache, GC structures, NIO direct (LAB-701 / 806). |
| What INCIDENT-806 showed about heap = limit | Jordan set `-Xmx512m -Xms512m` on a **512Mi** canary. Heap used ~390 MB; RSS hit 512Mi; kubelet **OOMKilled / 137**. No Java heap OOME. |

512 MiB (1024-based) = 536,870,912 bytes. `× 0.75` = **402,653,184 bytes = 384 MiB** heap. Remaining **~128 MiB** is native headroom, not waste. Default 25% would be **128 MiB** heap — safer than heap=limit, too small for Boot after warmup. PERFORMANCE-904 puts the percentage flags in the **image contract**. INCIDENT-806: `-Xmx512m -Xms512m` on a 512Mi canary left no room for native; kubelet **OOMKilled / 137** with no Java heap OOME. `MaxRAMPercentage=100` is the same class of mistake.

---

## 5. Secrets

| Field | Your answer |
|---|---|
| Which `BAYPAY_DB_*` keys exist | `BAYPAY_DB_URL` / `HOST`+`PORT`+`NAME`, `BAYPAY_DB_USER`, `BAYPAY_DB_PASSWORD` (Boot `application-prod.yml` + Liberty `${env.BAYPAY_DB_*}`) |
| Where they must **not** appear (Dockerfile `ENV`, git, image history) | No `ENV BAYPAY_DB_PASSWORD`, no `ARG` password, no `changeme` in the file, not committed `.env` |
| Where they **do** appear at runtime (Module 10 Secret name if you know it) | Process env. Module 10 Secret **`baypay-db`** keys `BAYPAY_DB_USER`, `BAYPAY_DB_PASSWORD`. ConfigMap `payment-config` for non-secrets. |
| What you grepped for before submit | `PASSWORD`, `changeme`, `Xmx`, `:latest` in `labs/BUILD-901/work/Dockerfile` — none |

A kube Secret injects env into the **running** container. Image layers are already built. If `ENV BAYPAY_DB_PASSWORD=…` (or an `ARG` that became an `ENV`) is in the Dockerfile, that value is in **history** and in every pull of that tag. Rotating `baypay-db` does not rewrite old layers. Anyone with the image has the password Jordan thought he left in the Secret. FIX-902 is that incident; this file does not bake credentials.

---

---

## 6. Hardening checklist (SECURITY-903)

Hardened file: `labs/SECURITY-903/Dockerfile`.

- [x] Non-root `USER 10001`
- [x] No secrets in layers
- [x] Runtime pin: digest or at least `21-jre` (not `:latest`)
- [x] No extra packages on the JRE stage
- [x] Read-only root filesystem note + writable `/tmp`
- [x] Not privileged (`--privileged` / `privileged: true` refused)

Write the read-only root + `/tmp` note here:

The **platform** (Module 10 `securityContext`) sets `readOnlyRootFilesystem: true`. The Dockerfile cannot set that kube field. Java 21 and Spring write temp files (extracted natives, Tomcat work, JVM hsperf / attach) under **`/tmp`**. Give them an `emptyDir` (or volume) mounted at `/tmp`. Privileged is **not** how you get a writable temp dir. This image is **not** run with `--privileged` or `privileged: true`.

Digest rule: lab uses `eclipse-temurin:21-jre` (never `:latest`). Production `FROM eclipse-temurin:21-jre@sha256:…`. Example amd64 manifest from 2026-09-06 inspect is in the Dockerfile comment. **Jordan owns the CVE bump** when Temurin publishes a fix. A tag that is not `latest` is still weaker than a digest: the tag can move.

---

## 7. Layer cache (PERFORMANCE-904)

Optimized file: `labs/PERFORMANCE-904/Dockerfile`.

**COPY first:** `mvnw`, `.mvn/`, reactor `pom.xml`, then each module `pom.xml` only (`shared`, `payment-service`, `refund-service`, `notification-service`, `transaction-worker`).

**RUN before sources:** `./mvnw -pl payment-service -am dependency:go-offline -B`. That layer holds the plugin/dependency download. Then `COPY` module trees and `package`.

A controller edit changes `payment-service/src/...` only. Docker cache hits the pom + `go-offline` layers. Maven does not re-download the internet. If you `COPY` the whole tree first (BUILD-901 / SECURITY-903 shape), every comma invalidates the download layer and Sam waits ten minutes.

**Trade-offs**

- **75% vs explicit `-Xmx384m` on a reviewed 512 MiB limit:** a fixed `-Xmx384m` is clearer when the limit is a contract that will not change and you want the same heap on a laptop and in kube. `%` is clearer when the same image runs at 512 MiB and 1 GiB (canary vs west). Still refuse `-Xmx` = limit. Drop toward 50% if thread count or NIO direct grows (LAB-701 native).
- **Fat JAR vs `BOOT-INF/lib` as its own layer:** lib layer caches across app-class edits. Extra COPY choreography; this course ships one JAR.
- **`jlink` vs `21-jre`:** spend time on `jlink` when image size / CVE surface of unused modules is a measured cost (finance image budget, air-gap). Do not spend this lab building one. `21-jre` is enough to run the fat JAR.
- **CI `--mount=type=cache` for `~/.m2` vs pom-first:** they solve different machines. Pom-first reuses **image layers** on the same builder. A Maven cache mount reuses downloads across Dockerfiles and machines. BayPay wants both in real CI; this lab grades the COPY order.

Runtime stays `eclipse-temurin:21-jre`. A JDK runtime is larger and a compiler on the merchant process — not a startup optimization.

---

## 8. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, and Riley Okonkwo, in one sitting, what the payment image is, who it runs as, how the heap is sized, and why Avery Chen’s POST must not depend on a password layer or a privileged container.

The image is `registry.baypay.example/baypay/payment-service:<tag>` — one disposable `payment-service` process, not `BayPayCell` in Docker. JDK builds with `./mvnw`; JRE runs `/app/app.jar` on **8080** as **UID 10001**. Poms and `dependency:go-offline` land before sources so a controller edit does not re-download plugins. Runtime is `21-jre` (digest in prod; never `:latest`); no apt toolbox. Heap is `JAVA_TOOL_OPTIONS`: `UseContainerSupport` + **MaxRAMPercentage=75** (384 MiB of 512), never `-Xmx` = limit (INCIDENT-806 / 137). Avery’s POST gets `BAYPAY_DB_*` from Secret `baypay-db` at start — a kube Secret cannot save an image that already baked the password. The platform sets **read-only root** + writable `/tmp` and **never** `--privileged`. `EXPOSE 8080` is the process port, not the internet.
