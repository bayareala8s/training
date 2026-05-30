# Capstone Presentation Guide

**Duration:** 15–20 minutes (+ 5 minutes Q&A)  
**Format:** Live demo preferred; recorded backup acceptable  
**Audience:** Instructor, peers, and industry reviewers (technical + managerial mix)

---

## Goals

By the end of your presentation, the audience should:

1. Understand the **business problem** you solved
2. Visualize your **architecture** and key design decisions
3. Trust that the platform **works** (demo or evidence)
4. See **governance, monitoring, and cost** awareness
5. Believe you can **own this system in production**

---

## Recommended Structure

### Slide Deck Outline (12–15 slides)

| # | Slide | Time | Content |
|---|-------|------|---------|
| 1 | Title | 0:30 | Project name, your name, scenario, date |
| 2 | Problem | 1:30 | Business context, pain points, stakeholders |
| 3 | Requirements | 1:00 | Top 5 functional + non-functional requirements |
| 4 | Architecture Overview | 2:00 | Single diagram—full platform |
| 5 | Data Zones | 1:30 | Raw / Cleaned / Curated / Quarantine paths |
| 6 | Ingestion & ETL | 2:00 | How data moves; key AWS services |
| 7 | Data Quality | 1:30 | Rules, quarantine, sample report |
| 8 | Security & Governance | 1:30 | IAM, encryption, PII (if applicable) |
| 9 | Monitoring & Ops | 1:30 | Dashboard, alarms, runbook highlight |
| 10 | Cost Analysis | 1:00 | Spend summary, top optimizations |
| 11 | Demo | 3:00 | Live or screenshots |
| 12 | Lessons Learned | 1:00 | What worked, what you'd change |
| 13 | Q&A | — | Backup slide with repo URL |

**Total:** ~17 minutes (adjust to fit 15–20 window)

---

## The First Two Minutes (Critical)

Open with a **story**, not technology:

> "RetailCo's finance team discovered $2M in reporting discrepancies because negative order amounts reached dashboards undetected. I built a cloud-native data platform on AWS that validates every record, quarantines failures, and alerts the team before bad data reaches analytics."

Then show the architecture diagram. Never start with "I used S3, Glue, and Lambda..."

---

## Demo Script (5 Minutes)

Practice this sequence until it takes under 5 minutes:

### Pre-Demo Checklist

- [ ] AWS Console logged in; region correct
- [ ] Sample data present in raw/
- [ ] Recent successful Glue run (or trigger during demo)
- [ ] Athena query saved
- [ ] CloudWatch dashboard bookmarked
- [ ] Screenshots folder open as backup

### Demo Flow

| Step | Action | What to Say |
|------|--------|-------------|
| 1 | S3 Console → bucket → show zones | "Here's our medallion layout—raw is immutable, curated is what analysts query." |
| 2 | Glue → Jobs → last run succeeded | "The ETL job processed yesterday's partition; job bookmarks prevent reprocessing." |
| 3 | Athena → run saved query | "Finance can self-serve: daily order totals by region from curated Parquet." |
| 4 | S3 quarantine/ or quality report | "When validation fails, records route here—847 bad orders never reached curated." |
| 5 | CloudWatch dashboard | "Operations sees job health and pass rate; this alarm pages on failure." |

### If Live Demo Fails

Calmly switch to screenshots:

> "Let me show you the verified state from this morning's run."

Never apologize excessively—reviewers expect demo risk.

---

## Speaking Tips

### Do

- **Pause** after the architecture slide for questions
- Use **pointer/highlight** on diagrams—not laser spam
- Explain **why** you chose services, not just what they are
- Connect features to **Module N** briefly ("Quality framework from Module 4")
- End with **one sentence** takeaway

### Don't

- Read bullet points verbatim
- Show code unless asked (have appendix slides ready)
- Exceed 20 minutes—respect the schedule
- Skip governance ("we'll add security later")
- Claim production-ready if it's a dev lab deployment—be honest

---

## Handling Q&A

### Common Questions & Strong Answers

**Q: Why Athena instead of Redshift?**  
A: "Serverless fit our dev scale and ad-hoc query pattern. At 10× volume we'd evaluate Redshift Serverless or Spectrum for known dashboards."

**Q: How do you handle schema changes?**  
A: "Glue crawlers detect new columns; ETL uses merge schema mode. Breaking changes trigger a steward review before curated publish."

**Q: What happens when the pipeline fails at 2 AM?**  
A: "CloudWatch alarm → SNS → on-call runbook. We halt curated publish if pass rate drops below SLO."

**Q: What's the monthly cost?**  
A: "Dev spend was $X; largest driver Glue DPUs. Lifecycle on raw/ and partition pruning cut Athena scan by Y%."

**Q: How is PII protected?**  
A: "Email hashed in curated; raw restricted to ETL role. Analysts query via Athena workgroup with column-level views."

### If You Don't Know

> "I haven't implemented that yet, but my approach would be [reasonable idea based on course content]."

Never fabricate.

---

## Visual Design Guidelines

- **One idea per slide**
- Diagrams > bullet lists
- Font size ≥ 24pt for body
- Use consistent colors matching architecture layers
- Include your name and scenario on every slide footer
- Export diagrams as PNG from Draw.io/Lucidchart for crisp display

---

## Recording a Backup Video (Optional)

If presenting asynchronously or as insurance:

1. Use OBS or Loom; 1080p screen recording
2. Record demo segment separately from slides (easier to re-cut)
3. Keep under 20 minutes
4. Upload unlisted to YouTube or include in repo `presentation/`
5. Test audio levels before full recording

---

## Presentation Day Checklist

### 24 Hours Before

- [ ] Rehearse full presentation with timer
- [ ] Run `terraform apply` and verify demo path
- [ ] Export latest dashboard screenshot
- [ ] Upload slides to `presentation/slides/`
- [ ] Share repo link in chat/LMS

### 1 Hour Before

- [ ] Close unrelated browser tabs
- [ ] Disable notifications
- [ ] Increase terminal font size
- [ ] Open demo tabs in order
- [ ] Water nearby

### After Presentation

- [ ] Note Q&A gaps for README FAQ
- [ ] Tag repo `capstone-presented`
- [ ] Run `terraform destroy` if course ends

---

## Rubric Alignment

This presentation primarily supports **Documentation & Presentation (15%)** but also demonstrates **Implementation**, **Monitoring**, and **Governance**. Ensure slides explicitly cover each rubric area—reviewers score holistically.

See [rubric.md](./rubric.md) for detailed criteria.

---

## Example Timeline (18 Minutes)

```text
0:00 – Hook and problem
2:00 – Requirements
3:00 – Architecture walkthrough
6:00 – Data flow and quality
8:30 – Security and governance
10:00 – Monitoring and cost
11:30 – Live demo
16:30 – Lessons learned
17:30 – Thank you / Q&A
```

Practice until consistent at 17–18 minutes.

---

## Resources

- [Week 10 Lecture](../modules/module-10-capstone/lectures/week-10-lecture.md)
- [Capstone Checklist](../modules/module-10-capstone/assignments/capstone-checklist.md)
- [Project Template README](./templates/project-structure/README.md)
