# Common Mistakes — Module 01: The Enterprise Architect’s Role

**Audience:** Students and instructors (facilitation cues in italics)  
**Case study:** NorthStar Financial Services (fictional)

---

## 1. Treating EA as “senior designer of everything”

**Symptom:** Lab artifacts describe how the Lead EA will personally design payments, onboarding, and partner APIs.  
**Why it fails:** Does not scale; starves decision rights; recreates hero dependency.  
**Fix:** Reframe mission around decision quality, reuse, and risk visibility. Solution design stays with SA/domain roles.  
*Instructor cue: Ask “What stops working when you are on PTO?”*

## 2. Org chart without decision rights

**Symptom:** Pretty operating-model diagram; empty or contradictory RACI.  
**Why it fails:** Meetings happen; decisions still thrash.  
**Fix:** Start from decision classes; then draw structure that supports them.  
*Instructor cue: Point to any row with two A’s—force a single Accountable.*

## 3. “Best practice” centralized ARB in Week 1

**Symptom:** Every project must pass ARB; 15-step intake.  
**Why it fails:** NorthStar teams will bypass; BU presidents will escalate to CTO.  
**Fix:** Narrow ARB to material risk/cost/lock-in; invest in guardrails and golden paths.  
*Instructor cue: “What percent of decisions should never reach ARB?”*

## 4. Principles as technology shopping lists

**Symptom:** “Prefer Kubernetes,” “Use Kafka,” “Be cloud-native.”  
**Why it fails:** Ages fast; invites dogma; ignores coexistence.  
**Fix:** Rewrite as enduring constraints with implications and exceptions; put product choices in standards/ADRs.  
*Instructor cue: Apply the five-question principle quality test from Lesson 1.3.*

## 5. No exception path (or an unusable one)

**Symptom:** Principles say “always”; or exceptions need six signatures.  
**Why it fails:** Underground architecture; loss of risk visibility.  
**Fix:** Time-boxed exceptions with owner, risk note, and sunset.  
*Instructor cue: Role-play a Payments latency exception in 3 minutes.*

## 6. Ignoring federated BU architects

**Symptom:** Operating model written as if BU architects do not exist—or are obstacles.  
**Why it fails:** They hold local political capital; you need a coalition.  
**Fix:** Explicit federated roles; engagement model that makes them look successful.  
*Instructor cue: “Who co-authors principles with you in the first 30 days?”*

## 7. Mission statements full of jargon

**Symptom:** “Leverage synergistic paradigms to drive digital transformation.”  
**Why it fails:** Executives cannot fund what they cannot parse.  
**Fix:** One paragraph: outcomes, decision scope, what you will *not* own.  
*Instructor cue: Have a peer rewrite the mission in plain language in 90 seconds.*

## 8. RACI theater (everyone Consulted on everything)

**Symptom:** Dense C’s across the matrix; no prioritization.  
**Why it fails:** Slow; accountability blurs.  
**Fix:** Consult only roles that change the decision; Inform the rest asynchronously.  
*Instructor cue: Delete half the C’s and ask what risk that creates.*

## 9. Leadership plan that starts with control

**Symptom:** Day-1 “mandate compliance” without listening tour or credibility win.  
**Why it fails:** Title without trust at NorthStar.  
**Fix:** Credibility-before-control sequence from Lesson 1.4.  
*Instructor cue: Ask for the first visible win that helps a delivery team go faster safely.*

## 10. Empty risk register—or only technology risks

**Symptom:** Risks list “cloud outage” but not “EA bypassed” or “dual Accountables.”  
**Why it fails:** Module 01 is about the *architecture function*; operating-model risks are in scope.  
**Fix:** Include political, capacity, and adoption risks alongside technology.  
*Instructor cue: Require at least two risks about influence/adoption.*

## 11. Security and resilience omitted “because early module”

**Symptom:** Principles and RACI ignore CISO/Security Architecture.  
**Why it fails:** Financial-services context; late engagement is already a NorthStar problem.  
**Fix:** Proportionate inclusion—consulted on material decisions; principle for secure/resilient by design.  
*Instructor cue: Soft penalty on rubric Security criterion if entirely absent.*

## 12. Copying a framework and calling it done

**Symptom:** TOGAF/Zachman dump with no NorthStar decisions.  
**Why it fails:** Not executable; fails trade-off standard.  
**Fix:** Use frameworks as optional vocabulary; grade on NorthStar-fit artifacts.  
*Instructor cue: “Which decision changes on Monday because of this page?”*
