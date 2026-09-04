# Rubric — BUILD-303 Persistence

Score each dimension 0–100, then apply the weight. Copy-pasting entities without a ledger-count proof is not a high Diagnostic score.

| Dimension | Weight | 100 | 60 | 20 |
|---|---|---|---|---|
| Technical accuracy | 25% | Money embed, STRING enums, unique keys, `@Version`, finders; default tests green; replay still one ledger row | Mappings work; no ledger-count proof | Wrong table names or ordinal enums |
| Diagnostic method | 20% | Used schema/SQL and test failures to fix scan/mapping | Changed `ddl-auto` until boot succeeded | Random annotation spray |
| Production awareness | 15% | Written warning on prod `update`; profile table correct; OSIV false | Profiles named; no `validate` argument | Treats H2 as production |
| Trade-off analysis | 15% | H2 vs Testcontainers; shared DB limits; Flyway vs `update` | One preference | No trade-off |
| Security / reliability | 10% | Prod console off; no real secrets; atomic create left intact | Console off; OSIV ignored | OSIV on or secrets committed |
| Communication | 10% | Entity excerpt + prod-DDL paragraph | Incomplete | Empty |
| Efficiency | 5% | Worked in `shared` | Finished | Second persistence stack |

**Pass guideline:** weighted score ≥ 70 and `open-in-view` stays false. Skipping `PostgresCompatibilityIT` without Docker is allowed.
