# Lesson 6.1 — Why Enterprises Still Use Files

**Module:** 06 — Enterprise File Transfer  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Argue for files as a valid enterprise style.
2. Separate edge protocol from internal processing.
3. List industries where files remain the contract.

---

## Enterprise scenario

Atlas’s largest supplier still drops a 4 GB CSV at 02:00. They have no API roadmap this decade. Refusing files is refusing to manufacture.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

Files persist because they match **batch economics**, **partner capability**, **regulatory extracts**, and **legacy systems**. A file is a bounded snapshot with a name, a checksum, and a business date. Many industries (banking settlements, healthcare claims, retail EDI) standardized on files before REST existed. Cloud does not erase counterparties.

---

## WHEN an Enterprise Architect uses it

- Partner cannot or will not call your API.
- Bulk is the natural grain.
- Legal evidence is a file artifact.
- Mainframe extract windows.

### When NOT to use it

- Low-latency single-record UX.
- Unknown many consumers of a tiny fact (events).
- Using files to avoid designing an API you actually need internally.

---

## HOW — the pattern (vendor-neutral)

Keep files as a first-class style in the decision framework. Wrap them with a platform (landing, validate, event FileReceived) rather than a unique script per partner. Internally you may translate files into events/commands; at the edge the file remains.

### Architecture diagram

```mermaid
flowchart LR
  P[Partner] -->|SFTP file| L[Landing zone]
  L --> V[Validate]
  V --> E[FileReceived event]
  E --> I[Internal APIs / queues]
```

---

## HOW — AWS implementation (after the pattern)

S3 as landing zone; Transfer Family for SFTP; EventBridge on object created. The AWS mapping does not make the partner modern—it makes you operable.

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Shame-driven architecture (“files are legacy so we will not design them”).

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| Files | Partner reach, bulk, evidence | Latency, hygiene, duplicates |
| Force API | Modern internal estate | Lost revenue if partners cannot comply |

---

## Architecture decision prompt

A board member asks “why not APIs for everyone?” Answer in business terms, not protocol nostalgia.

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** Does using S3 mean you no longer “use files”?

*Answer.* No. S3 objects are files. You modernized the store and automation, not necessarily the partner contract.

---

## Architect's note

Capstone 1 and 4 are unwinnable if you pretend files do not exist.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
