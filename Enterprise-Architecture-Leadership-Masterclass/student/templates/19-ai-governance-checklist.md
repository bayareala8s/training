# AI Governance Checklist

**Organization:** NorthStar Financial Services (fictional)  
**Use case / system:**  
**Owner:**  
**Date:**  

---

## Business and ownership

- [ ] Business sponsor named
- [ ] Success metrics defined
- [ ] Operating model roles clear (build, run, approve, audit)
- [ ] Exit / rollback criteria defined

## Data and privacy

- [ ] Data sources inventoried and classified
- [ ] Retention and minimization rules set
- [ ] PII/sensitive data handling documented
- [ ] Training/evaluation data rights reviewed

## Model and architecture

- [ ] Pattern selected (prompt / RAG / agent / workflow) with rationale
- [ ] Structured outputs validated where used
- [ ] Deterministic rules layered for high-risk decisions
- [ ] Model gateway / access control defined
- [ ] Prompt and version change control defined

## Safety and human oversight

- [ ] Harm / abuse cases identified
- [ ] Human-in-the-loop triggers defined
- [ ] Override and escalation path documented
- [ ] User-facing limitations disclosed where needed

## Evaluation and monitoring

- [ ] Evaluation dataset created
- [ ] Quality thresholds set
- [ ] Drift / regression monitoring planned
- [ ] Incident response for model failures defined

## Audit, cost, and compliance

- [ ] Input/output logging policy (safe redaction)
- [ ] Token/cost tracking enabled
- [ ] Access and change audit trail
- [ ] Regulatory/control mapping completed (as applicable)

## Go-live gate

- [ ] Security review complete
- [ ] Privacy review complete
- [ ] ARB / design authority decision recorded
- [ ] ADR(s) filed

**Decision:** Pilot / Production / Blocked  
**Conditions:**
