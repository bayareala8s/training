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
| Date | |
| Engine used (`docker` / `podman` / files only) | |
| Reference commit or branch | |

---

## 2. Image

Teaching registry and name from [CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md):

| Field | Your answer |
|---|---|
| Image name (`registry.../payment-service:<tag>`) | |
| Build-stage base | |
| Runtime-stage base (must not be a full JDK) | |
| How you pin the runtime (tag `21-jre` and/or digest) | |
| What the runtime `COPY`s (JAR only?) | |
| Port (`EXPOSE`) | |
| How you invoke the process (`ENTRYPOINT` / `CMD`) | |

In 4–6 sentences, explain why a multi-stage file is the BayPay default and what AEJE-D-039 is showing.

---

## 3. User

| Field | Your answer |
|---|---|
| UID in the Dockerfile | |
| Why not `root` | |
| What still has to be true in Module 10 `securityContext` | |

One paragraph: what changes about a container escape and about file ownership when the JVM is `10001`.

---

## 4. JVM flags

Do **not** recommend `-Xmx` equal to the container memory limit.

| Field | Your answer |
|---|---|
| `JAVA_TOOL_OPTIONS` you would ship | |
| `UseContainerSupport` on or off? Why? | |
| `MaxRAMPercentage` value and why it is not 100 | |
| Native consumers that sit **beside** the heap | |
| What INCIDENT-806 showed about heap = limit | |

Show arithmetic for one teaching limit (for example 512 MiB at 75%).

---

## 5. Secrets

| Field | Your answer |
|---|---|
| Which `BAYPAY_DB_*` keys exist | |
| Where they must **not** appear (Dockerfile `ENV`, git, image history) | |
| Where they **do** appear at runtime (Module 10 Secret name if you know it) | |
| What you grepped for before submit | |

In 4–6 sentences, explain why a correct kube Secret cannot save an image that already baked `BAYPAY_DB_PASSWORD`.

---

## 6. Hardening checklist (SECURITY-903)

- [ ] Non-root `USER 10001`
- [ ] No secrets in layers
- [ ] Runtime pin: digest or at least `21-jre` (not `:latest`)
- [ ] No extra packages on the JRE stage
- [ ] Read-only root filesystem note + writable `/tmp`
- [ ] Not privileged (`--privileged` / `privileged: true` refused)

Write the read-only root + `/tmp` note here:

---

## 7. Layer cache (PERFORMANCE-904)

What do you `COPY` first, and which `RUN` must happen before sources land, so a controller edit does not re-download plugins?

---

## 8. Interview snippet (Staff, 6–8 sentences)

Explain to Sam Okada, Priya Nair, and Riley Okonkwo, in one sitting, what the payment image is, who it runs as, how the heap is sized, and why Avery Chen’s POST must not depend on a password layer or a privileged container.
