# Instructor Guide — Module 04: Target-State Architecture and Transformation Roadmaps

**Audience:** BayLearn instructors  
**Student materials:** `modules/module-04-target-state/`, `labs/lab-04-target-state-roadmap/`, assessments (non-key)  
**Classification:** Instructor-only when combined with reference solutions and answer keys

---

## 1. Module purpose

Enable students, as NorthStar’s Lead Enterprise Architect, to define a defensible target-state architecture, choose modernization dispositions with trade-offs, design transition architectures with exit criteria, and communicate a 24-month roadmap that executives can fund and challenge.

## 2. Learning objectives

1. Define target-state architecture aligned to capabilities, principles, and constraints (LO-4.1).  
2. Select and justify modernization strategies including retain/replace/consolidate/retire (LO-4.2).  
3. Design three transition architectures with coexistence and exit criteria (LO-4.3).  
4. Produce a sequenced 24-month roadmap with value, dependencies, and risks (LO-4.4).

## 3. Prerequisites

Modules 01–03 completed or catch-up brief issued. Students need TIME/current-state notes and draft principles. No AWS required.

## 4. Estimated timing (120 minutes)

| Segment | Minutes |
| ------- | ------: |
| Business scenario and framing | 10 |
| Lessons 4.1–4.2 (target + strategies) | 25 |
| Lessons 4.3–4.4 (transitions + roadmaps) | 20 |
| Instructor demonstration | 15 |
| Guided lab | 35 |
| Architecture review | 10 |
| Assignment briefing | 5 |

Adjust: if cohort is weak on Module 03, steal 5 minutes from lab for TIME refresh—not from exit-criteria teaching.

## 5. Opening business scenario

Maya Chen (CIO) presents a glossy “Target 2028” cloud+AI slide. Elena Vos asks about dual-run funding for acquired products. Raj Patel asks where audit evidence lives during migration. Your job is to replace vision theater with a target-state + transition + roadmap package.

Personas to keep consistent: Maya Chen (CIO), Raj Patel (CISO), Elena Vos (Retail BU), Marcus Webb (Platform), Priya Nair (Data).

## 6. Lesson flow

1. Define target state as patterns + principles + outcomes + non-goals (4.1).  
2. Teach seven strategies; force retain/consolidate/retire—not replace-only (4.2).  
3. Design three transitions with observable exit criteria (4.3).  
4. Sequence 24-month waves with value-vs-risk and dependencies (4.4) → lab.

## 7. Questions to ask

1. What is the difference between a vision slide and a target-state architecture?  
2. When is retain the brave decision?  
3. What makes an exit criterion observable?  
4. Which dependency kills Phase 2 if delayed?

## 8. Whiteboard sequence

See `whiteboard-plan.md`. Summary:

1. Strategy themes → capabilities → principles  
2. Disposition matrix for 6–8 apps  
3. Three transition boxes with exit gates  
4. 24-month wave swimlane + value tags  

## 9. Demonstration steps

1. Show sample target principles and one non-goal.  
2. Walk CRM consolidate vs replace trade-off aloud.  
3. Draft Transition A exit criteria live; sketch Phase 0–1 roadmap rows.

Use reference solution privately—do not project full solution.

## 10. Break points

- After strategies (~35–40 min): 2-minute stretch  
- Mid-lab (~75 min): progress check—“hardest disposition?”

## 11. Lab facilitation

See `lab-facilitation-guide.md`.

**Lab goal:** Complete draft target + three transitions + roadmap skeleton in-session; polish as homework.

**Timebox rule:** Protect last 20 minutes for review + assignment even if labs incomplete.

## 12. Common student issues

| Issue | Facilitation response |
| ----- | --------------------- |
| Replace-everything bias | Ask dual-run cost for StarCore + PayForge + CRM simultaneously |
| Transitions = project phases | Require systems of record + interface + exit metric |
| Roadmap as backlog | Force dependency column; block “all Month 1” |
| Vague value | Demand KPI direction per phase |
| Missing security | Prompt identity + audit during dual-write |

## 13. Debrief questions

1. What non-goal will be attacked first politically?  
2. Which exit criterion is weakest—and how do you harden it?  
3. What did you learn about sequencing value vs risk?

## 14. Assignment briefing

Assignment extends lab into a polished executive package. Rubric emphasis: feasibility/roadmap, trade-offs, business alignment. Capstone: target-state, transitions, roadmap artifacts.

## 15. Suggested homework

- Finish Lab 04 deliverables  
- Complete Module 04 quiz (formative)  
- Optional stretch: CRM survivor ADR  
- Skim Module 05 teaser (landing zone will consume Phase 0)

---

## Materials checklist

- [ ] Slides / slide-outline loaded  
- [ ] Speaking script reviewed  
- [ ] Lab files ready  
- [ ] Reference solution reviewed privately  
- [ ] Grading guide open for office hours  
- [ ] Fiction notice stated in opening  
