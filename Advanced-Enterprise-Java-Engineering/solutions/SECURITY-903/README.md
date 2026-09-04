# SECURITY-903 — Instructor solution

**Do not share these files with students before they submit a hardened Dockerfile and worksheet notes.**

Students may start from their BUILD-901 output. Docker is not required.

## Files

| File | Role |
|---|---|
| [Dockerfile](Dockerfile) | Hardened multi-stage image: JRE tag (not `latest`), JAR only, `USER 10001`, no secrets, no apt |

## Controls (must be visible)

| Control | How the key shows it |
|---|---|
| Non-root | `USER 10001` after the JAR copy |
| No secrets in layers | No `ENV`/`ARG` password values |
| Pin base | Comment documents `21-jre@sha256:<digest>`; lab `FROM` is `eclipse-temurin:21-jre` |
| No extra packages | No `apt-get` on the runtime stage |
| Read-only root | Comment: platform `readOnlyRootFilesystem: true` + writable `/tmp` |
| Not privileged | Comment: no `--privileged` / `privileged: true` |

A digest in the actual `FROM` is excellent if the student looked one up. A honest comment plus tag `21-jre` meets the lab minimum. `:latest` does not.

## What BUILD-901 already had

Stage split, Wrapper, JRE, port, UID, no secrets. This lab adds the **review language**: pin rule, package ban, read-only root note, privileged ban. Do not deduct if the file looks like BUILD-901 plus those comments — that is a valid harden.

## Platform note (Module 10)

The Dockerfile cannot emit kube YAML. Accept a worksheet paragraph such as:

```text
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  privileged: false
# volumeMount emptyDir or ephemeral volume at /tmp
```

Do not require a live cluster to prove it.

## Checklist

- [x] `USER 10001`
- [x] No secret literals
- [x] Runtime `21-jre` (not `latest`)
- [x] No extra packages
- [x] Read-only root + `/tmp` documented
- [x] Not privileged documented
- [x] `FROM` / `WORKDIR` / `COPY` / `USER` present

## Diagram

AEJE-D-040: trust boundary is the pinned JRE, JAR, and UID. Secrets and `securityContext` stay outside. Privileged, `latest`, apt toolboxes, and password `ENV` are rejected.

## Scoring notes

A toolbox `apt-get install curl vim` on the runtime stage fails Security / reliability. `:latest` fails Technical accuracy. A password `ENV` fails Security / reliability regardless of UID. Skipping Docker is not an Efficiency penalty. Privileged “for debugging” in a student note caps Production awareness.
