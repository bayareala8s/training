# Student Datasets

> **Fiction notice:** All datasets in this folder are invented for BayLearn instructional use.  
> **NorthStar Financial Services** is a fictional organization. Application names, costs, risks, owners, and dates are not associated with any real company.

---

## Contents

| File | Module | Description |
| ---- | ------ | ----------- |
| `northstar-application-inventory.csv` | 03 | Fictional application portfolio (40+ apps) for TIME / current-state assessment labs |

---

## How to use `northstar-application-inventory.csv`

1. Treat rows as **directional evidence**, not absolute truth—scores and dispositions are starting points for analysis.
2. Join mentally (or in a sheet) to your Module 02 capability map via the **Business capability** column.
3. Do **not** blindly accept **Recommended disposition**—defend or challenge it with TIME dimensions, dependencies, and business risk.
4. Annual cost is USD fictional OpEx/run-cost estimate for teaching prioritization.

## Columns

| Column | Meaning |
| ------ | ------- |
| Application ID | Stable fictional ID (`NS-APP-###`) |
| Name | Fictional application name |
| Business capability | Primary capability mapping (may be imperfect—students may challenge) |
| Business owner | Fictional role/name |
| Technology stack | High-level stack labels |
| Hosting model | On-premises, private cloud, public cloud, SaaS, hybrid |
| Annual cost | Fictional annual run cost (USD) |
| Criticality | Mission Critical / High / Medium / Low |
| Technical health | Poor / Fair / Good |
| Security risk | Low / Medium / High |
| Integration count | Approximate dependency fan-in/out |
| Data classification | Public / Internal / Confidential / Restricted |
| End-of-life date | Vendor or internal support end (fictional) |
| Recommended disposition | Seed TIME-oriented label (Tolerate / Invest / Migrate / Eliminate)—challenge in lab |

## Governance

- Do not present this CSV as real production data in external portfolios without the fiction notice.
- Instructor analysis guidance lives under `instructor/reference-solutions/module-03/`.
