# AEJE-D-015 — Spring to Jakarta mapping

- Type: concept
- Module: 4
- Maps to: ARCHITECT-401
- Complexity: 2

```mermaid
flowchart TB
  DI[Spring DI] --- CDI[CDI]
  Tx[@Transactional] --- JTA[JTA]
  JPA[Spring Data JPA] --- EM[EntityManager]
  Rest[RestController] --- JAX[JAX-RS]
```
