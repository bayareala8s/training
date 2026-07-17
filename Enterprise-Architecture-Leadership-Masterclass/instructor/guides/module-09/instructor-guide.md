# Instructor Guide — Module 09: Architecture Governance and Executive Communication

**Audience:** BayLearn instructors  
**Student materials:** modules/, labs/, assessments/ (non-key)  
**Classification:** Instructor-only when combined with reference solutions

---

## 1. Module purpose

Train students to govern architecture decisions under political pressure and to communicate dispositions in executive language. The ARB simulation is the signature experience of Week 9.

## 2. Learning objectives

1. Design a balanced architecture governance model.  
2. Facilitate ARB conversations with role fidelity.  
3. Author high-quality ADRs.  
4. Write executive decision memos.

## 3. Prerequisites

Modules 01–08 complete or summary-reviewed. Proposal pack printed or shared digitally before class.

## 4. Estimated timing (120 minutes)

| Segment | Minutes |
| ------- | ------: |
| Business scenario and lesson | 15 |
| Governance + ARB concepts | 20 |
| Instructor demonstration (mini-ARB) | 15 |
| Guided ARB lab | 40 |
| Architecture review / debrief | 15 |
| Assignment briefing | 10 |
| Buffer / breaks | 5 |

## 5. Opening business scenario

Retail Payments arrives with funded licenses and a hard date. Ask: “Is governance blocking innovation—or preventing a permanent tax?” Collect two student votes publicly, then park them until after the simulation.

## 6. Lesson flow

1. Governance stack: principles → standards → guardrails → exceptions → forums  
2. ARB purpose, roles, disposition vocabulary  
3. ADR quality bar and anti-patterns  
4. Executive memo spine and language swaps  
5. Demo: 8-minute compressed ARB on one decision request  
6. Full lab simulation on all four requests

## 7. Questions to ask

1. Which of the four requests is most irreversible?  
2. What is the difference between sunk cost and stoppable spend?  
3. When is Approve-with-conditions dishonest?  
4. What guardrail would have prevented this proposal from reaching ARB?

## 8. Whiteboard sequence

See `whiteboard-plan.md`. Summary:

1. Governance stack  
2. Four decision requests as separate swimlanes  
3. Disposition matrix  
4. Memo spine

## 9. Demonstration steps

1. Model Lead EA framing (split four decisions).  
2. Ask one strong Security question on contractor access.  
3. Synthesize “Reject cloud + Reject proprietary SoR + Condition access alternative + Offer landing-zone fast path.”  
4. Show how that becomes memo bullets + ADR titles.

## 10. Break points

- After concept block (~35 min)  
- Mid-lab check (~75 min)

## 11. Lab facilitation

See `lab-facilitation-guide.md`.

**Lab goal:** Produce a defensible multi-decision disposition with memo + ADRs.

**Timebox rule:** Protect the last 25 minutes for review + assignment briefing even if labs are incomplete.

## 12. Common student issues

| Issue | Facilitation response |
| ----- | --------------------- |
| Rubber-stamp because licenses signed | Teach sunk vs. stoppable cost; separate commercial from architecture |
| Endless debate on CloudNova features | Redirect to operating-model duplication and audit trail |
| Single ADR for everything | Require split ADRs before submission |
| Hostile security veto | Demand an alternative that still enables hypercare |

## 13. Debrief questions

1. What changed your preliminary disposition?  
2. Did role pressure distort judgment?  
3. What will you automate next?

## 14. Assignment briefing

Polish the lab package to submission quality; extend governance model narrative for capstone artifact 17.

## 15. Suggested homework

- Complete memo + ADRs  
- Formative quiz  
- Begin assembling capstone completeness checklist

---

## Materials checklist

- [ ] Slides loaded  
- [ ] Speaking script reviewed  
- [ ] Proposal pack distributed 24h prior if possible  
- [ ] Role badges / breakout assignments ready  
- [ ] Reference solution reviewed privately  
- [ ] Grading guide open for office hours
