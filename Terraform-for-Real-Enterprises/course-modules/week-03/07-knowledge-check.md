# Week 3 — Knowledge Check

**Format:** 15 questions · **Time:** 20 minutes closed-book (or open-book for self-paced)

---

## Questions

1. What three elements form a Terraform module’s public “contract” with consumers?
2. What is the difference between a root module and a child module?
3. How does Terraform determine order of operations between `module.vpc` and `module.compute` when compute references vpc outputs?
4. Why should production module sources pin `ref=v1.2.3` instead of `ref=main`?
5. What semver bump is required when removing a required input variable?
6. What semver bump is required when adding an optional input with a safe default?
7. Name two appropriate uses of `validation` blocks on module variables.
8. What should a module README include at minimum for enterprise consumers?
9. What is a “god module” anti-pattern?
10. When is `depends_on` between modules justified?
11. What command validates Terraform configuration without contacting AWS?
12. What does `make validate` in this course accomplish?
13. Name two module source types enterprises use besides local path.
14. What file documents version history for module consumers?
15. What tag does this course require on all AWS resources for cost scripts?

---

## Answer key (instructors only)

| # | Answer |
|---|--------|
| 1 | Input variables, output values, documented behavior/README (accept interface/sources) |
| 2 | Root = environment stack that calls modules; child = reusable module under `modules/` |
| 3 | Implicit dependency graph from output references—vpc created before compute |
| 4 | Reproducibility; prevents unreviewed upstream changes breaking production |
| 5 | MAJOR |
| 6 | MINOR |
| 7 | Any two: allowed environment values, valid CIDR format, regex on naming, numeric ranges |
| 8 | Purpose, example usage, inputs/outputs tables, upgrade notes (any three) |
| 9 | Single module owning unrelated resources (VPC+DB+app) preventing independent lifecycle/versioning |
| 10 | Hidden dependency without attribute reference; ordering not expressible via references |
| 11 | `terraform validate` |
| 12 | Runs validate across dev/test/prod environment directories |
| 13 | Any two: Git URL, Terraform Registry/private registry, S3 module archive |
| 14 | CHANGELOG.md |
| 15 | `Course=terraform-enterprise` |

**Passing score:** 80% (12/15)
