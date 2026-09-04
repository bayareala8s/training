# Portfolio — Spring-to-Jakarta mapping brief

**Course:** Advanced Enterprise Java Engineering  
**Module:** 04  
**Lab:** ARCHITECT-401  
**Case study:** BayPay Financial Services (fictional)

Export this page (or a copy) as your Module 4 portfolio artifact.

**Your name:**  
**Date:**  
**Reference app commit / tag (if known):**  

---

## Required mapping

| Spring (BayPay today) | Jakarta contract | Evidence (type or file) | Notes |
|---|---|---|---|
| IoC (`@Service`, injection) | CDI | | |
| `@Transactional` | JTA | | |
| `JpaRepository` | `EntityManager` | | |
| `@RestController` | JAX-RS | | |
| `application.yml` / env | JNDI | | |

## Extra rows (at least three)

| Spring / Boot | Jakarta / server | Evidence | Notes |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## Transaction walk

Does `PaymentPostingService.postAuthorized` start its own transaction in the **reference app**? What Jakarta attribute matches that?

## Greenfield vs source estate

What did operators bind in JNDI on the historical cell? What binds it in Boot today? One sentence: why you would **not** create a new traditional WAS ND cell for a new BayPay service.

## Interview snippet (Staff, 6–8 sentences)

Explain to a WAS operator and a Spring engineer, in one sitting, why BayPay’s payment API is already a Jakarta application and why that does not mean the next service should be an ear on PaymentCluster.
