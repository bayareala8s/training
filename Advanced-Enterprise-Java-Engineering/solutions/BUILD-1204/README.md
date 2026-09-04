# BUILD-1204 — Instructor solution

**Do not share these files with students before they submit a complete workflow.**

This folder is the answer key for the CI/CD pipeline. Students are not required to run GitHub Actions.

## Files

| File | Role |
|---|---|
| [.github/workflows/baypay.yml](.github/workflows/baypay.yml) | Test (Java 21, `./mvnw test`) then publish `${{ github.sha }}` |

A student workflow that has a test job, Temurin 21, Wrapper `test`, `needs: test`, and a SHA tag passes even if they named the job `unit` or omitted the `if: main` guard.

## What the starter got wrong

- **No test job.** Publish was the only job.
- Image tagged **`:latest` only**.
- No Java setup, no `./mvnw`.

The starter was valid-looking Actions YAML. It was not a release gate.

## Required contracts

```text
test:     setup-java temurin 21; ./mvnw -B -pl payment-service -am test
publish:  needs: test; docker build ...:${{ github.sha }}
secrets:  names only — no key material
latest:   not the deploy tag
validate: read the YAML; live Actions optional
```

## Diagram

AEJE-D-056: push → test (Java 21 / Maven Wrapper) → build → immutable SHA tag.

## Scoring notes

Full marks require the test job, Java 21, Wrapper `test`, `needs`, and SHA tag. A publish-only file fails Technical accuracy. `-DskipTests` in the “test” job fails Production awareness. Access keys in YAML fail Security. GitHub absence must not fail the lab.
