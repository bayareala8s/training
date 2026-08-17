# Instructor Guide — Module 01: The Enterprise Architect’s Role

**Audience:** BayLearn instructors  
**Student materials:** `modules/module-01-enterprise-architect-role/`, `labs/lab-01-architecture-operating-model/`, `assessments/` (non-key)  
**Classification:** Instructor-only when combined with reference solutions  
**Case study:** NorthStar Financial Services (fictional)

---

## 1. Module purpose

Establish students as NorthStar’s Lead Enterprise Architect by defining the architecture function—mission, operating model, principles, decision rights, engagement, and influence tactics—before they design technical target states in later modules.

Students leave Week 1 with portfolio-ready operating-model artifacts and a clear stance: **architecture leadership is decision quality and influence, not universal design ownership.**

---

## 2. Learning objectives

1. Distinguish enterprise architecture from solution, cloud, platform, and engineering leadership—and explain EA value in NorthStar outcome language.  
2. Design a federated-compatible architecture operating model (mission, structure option, decision rights, RACI, engagement).  
3. Draft 8–10 architecture principles with rationale, implications, exceptions, and signals tied to NorthStar strategy.  
4. Assess architecture leadership readiness and prescribe influence tactics that do not depend solely on hierarchical authority.

---

## 3. Prerequisites

- Students have read the NorthStar case study baseline  
- Templates 03 (principles) and 05 (RACI) skimmed  
- No AWS required  
- Instructors: review reference solution privately; do not project it

---

## 4. Estimated timing (120 minutes)

| Segment | Minutes |
| ------- | ------: |
| Welcome, fiction notice, business scenario | 15 |
| Lessons 1.1–1.3 concepts (EA role, operating model, principles) | 25 |
| Lesson 1.4 leadership + instructor demonstration | 15 |
| Guided lab | 40 |
| Architecture review / debrief | 15 |
| Assignment briefing | 5 |
| Buffer / breaks | 5 |

Protect the last ~25 minutes for review + assignment even if labs are incomplete.

---

## 5. Opening business scenario

Read (paraphrase allowed):

> NorthStar has architects in Retail, Payments, Partner Channels, and Wealth. Last quarter three overlapping customer-identity initiatives were funded. Partner onboarding still uses multiple file platforms. Security is engaged late. The CIO appointed you Lead EA and wants an architecture operating model before the next Executive Committee technology review—not another framework presentation.

**Cold-call:** “If architecture disappeared tomorrow, which outcome fails first?”

Keep the fiction notice visible on Slide 2.

---

## 6. Lesson flow

1. **What EA really is** — decision stack; role boundaries; anti-pattern “senior designer of everything.”  
2. **Operating model** — central / federated / hybrid trade-offs; engagement modes; decision classes. Prefer hybrid as *NorthStar Year-1 fit*, not universal law.  
3. **Principles** — anatomy; strategy→principle mapping; exception path; quality test.  
4. **Leadership assessment** — influence sources; readiness scores; 90-day sequence; transition to demo + lab.

---

## 7. Questions to ask

1. What is the difference between a guardrail and a gate—and which should NorthStar bias toward in Year 1?  
2. Who should be Accountable for enterprise principles—and why not the ARB?  
3. Which principle most threatens BU autonomy, and how do you socialize it?  
4. What is your first move when Wealth announces a CRM platform in a town hall without consulting EA?

---

## 8. Whiteboard sequence

See `whiteboard-plan.md`. Summary:

1. EA decision stack (strategy → capabilities → principles → platforms → solutions)  
2. Three operating-model options with +/- columns; star hybrid for NorthStar Year 1  
3. Decision-class table + consult/collaborate/govern funnel  
4. Principle anatomy + exception loop  
5. Influence sources radar (quick)

---

## 9. Demonstration steps

Demonstrate a **partial** operating-model pack (mission + 2 decision classes + 2 principles + one risk)—not the full reference solution.

1. Write a plain-language mission (30–40 seconds aloud).  
2. Place “second API gateway” into a decision class; assign a single Accountable.  
3. Draft one strong principle with exception and signal; contrast with a weak slogan.  
4. Add risk AF-01 “EA bypassed by BU presidents” with mitigation.

Narrate trade-offs out loud: what you are *not* choosing (broad ARB; full centralization).

---

## 10. Break points

- After concept block (~40 min): 3–5 minute stretch / bio break  
- Mid-lab check (~75–80 min): 2-minute progress prompt  
- Optional micro-break before debrief if energy is low

---

## 11. Lab facilitation

See `lab-facilitation-guide.md`.

**Lab goal:** Produce NorthStar’s first architecture operating-model pack.

**Timebox rule:** At T+35 lab minutes, tell students unfinished polish becomes homework; debrief starts on schedule.

---

## 12. Common student issues

| Issue | Facilitation response |
| ----- | --------------------- |
| Principles = product list | Apply quality test; move products to standards/ADR |
| Two Accountables in RACI | “Only one A—who escalates?” |
| Heavy ARB everything | Ask bypass likelihood; shrink triggers |
| Ignoring BU architects | Reframe as coalition; add them to RACI as R/C |
| Jargon mission | Peer rewrite in plain language |
| No security in artifacts | Soft rubric hit; add CISO consult on material class |

---

## 13. Debrief questions

1. What does architecture own—and not own—at NorthStar?  
2. What option did you reject and why?  
3. Stress-test the second API gateway through your model.  
4. Strongest vs. weakest principle?  
5. First move if bypassed?  

Full set: module `debrief-questions.md` and `discussion-questions.md`.

---

## 14. Assignment briefing

Students refine lab artifacts into a CIO-ready pack plus a one-page influence narrative (see assignment file). Emphasize rubric: **Business alignment, Trade-off analysis, Communication quality** this week; Security proportionate but not absent.

Capstone: mission, principles, RACI/decision rights, engagement, AF risk register.

---

## 15. Suggested homework

- Complete unfinished lab deliverables  
- Formative quiz (`assessments/quizzes/module-01-quiz.md`)  
- Read Module 02 preview: capability mapping teaser in slide close  
- Optional: start stakeholder matrix using template 04  
- Office hours: blockers on decision classes or principle wording

---

## Materials checklist

- [ ] Slides loaded (`slides/module-01/`)  
- [ ] Speaking script reviewed  
- [ ] Lab files ready  
- [ ] Reference solution reviewed privately  
- [ ] Grading guide open for office hours  
- [ ] Fiction notice on opening slides  
- [ ] Mermaid diagram render check (`diagrams/operating-model.mmd`)
