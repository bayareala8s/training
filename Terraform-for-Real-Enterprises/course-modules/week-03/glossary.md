# Week 3 — Glossary

| Term | Definition |
|------|------------|
| **Module** | Container for multiple resources used together, invoked via `module` block |
| **Root module** | Top-level configuration in a working directory (e.g. environment stack) |
| **Child module** | Module called by another module or root module |
| **Source** | Argument specifying where module code is loaded from (path, Git, registry) |
| **Input variable** | Module parameter exposed to callers |
| **Output value** | Module result exported to callers or other modules |
| **Composition** | Wiring multiple modules via outputs → inputs in a root module |
| **Implicit dependency** | Order determined by references between resources/modules |
| **Semantic versioning (SemVer)** | MAJOR.MINOR.PATCH versioning signaling compatibility |
| **Breaking change** | Change requiring consumer code updates (major bump) |
| **CHANGELOG** | File listing version history and migration notes |
| **Private registry** | Organization-hosted catalog for approved Terraform modules |
| **God module** | Overly broad module mixing unrelated infrastructure concerns |
| **for_each (modules)** | Creating multiple module instances from a map or set |
| **Validation block** | Variable constraint evaluated at plan time |
| **Consumer** | Team or stack that calls a published module |
| **Platform module** | Organization-standard building block maintained by platform engineering |
