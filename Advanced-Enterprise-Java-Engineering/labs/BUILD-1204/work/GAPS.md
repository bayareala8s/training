# BUILD-1204 — starter gaps (before edit)

| AEJE-D-056 | Starter |
|---|---|
| Job **test** (Java 21, `./mvnw test`) | **Missing** — only `publish` |
| `needs: test` | Publish runs alone |
| Tag `${{ github.sha }}` | Only **`:latest`** |
| Working directory `reference-apps/baypay` | `docker build` context only |
| Secret **names** if push | No keys (keep) |

INCIDENT-1205 is the pager for a publish-only / `:latest` pipeline. Fixes in `work/` only.
