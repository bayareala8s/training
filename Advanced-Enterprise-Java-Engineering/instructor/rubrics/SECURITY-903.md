# Rubric — SECURITY-903 Harden container

**Type:** SECURITY  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Score each dimension 0–100, then apply the weight. Docker or a paid scanner must not be required to pass.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | `USER 10001`; `21-jre` or digest (not `:latest`); JAR-only copy; no apt on runtime; parseable instructions | Tag is `21-jre` but still copies the whole tree | `:latest` or JDK runtime remains |
| Diagnostic method | 20% | Grepped secrets; listed pin / packages / privilege before editing | Hardened “by feel” | Opened `solutions/` first |
| Production awareness | 15% | AEJE-D-040 boundary; Module 10 Secret vs image; Avery identifiers in the POST body | Mentions hardening vaguely | Recommends `--privileged` for debug |
| Trade-off analysis | 15% | Digest vs tag rebuilds; distroless vs `21-jre`; shell for `exec` vs no shell | One honest trade-off | “Never update the base” or “install everything” |
| Security / reliability | 10% | No secrets; non-root; read-only root + `/tmp` note; not privileged; no toolbox packages | Non-root only | Password layer or privileged as default |
| Communication | 10% | PF-container secrets/user/hardening sections complete | Files only | Empty worksheet |
| Efficiency | 5% | Checklist only; no required scanner | Finished in session | Paid registry scan or AWS as if required |

**Pass guideline:** weighted score ≥ 70, non-root, no secret values, not `:latest`, no privileged recommendation. Runtime `apt-get install curl` caps Security / reliability at 20 or below.
