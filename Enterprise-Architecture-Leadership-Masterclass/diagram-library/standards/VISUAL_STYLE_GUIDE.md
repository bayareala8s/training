# Visual Style Guide — BayLearn Architecture Diagrams

## Canvas

| Property | Value |
| -------- | ----- |
| Background | White `#FFFFFF` |
| Aspect | 16:9 preferred for slides; square OK for LinkedIn crops |
| Margins | ≥ 24px |
| Corner radius (containers) | 8px |
| Line weight | 1.5–2px |
| Arrowheads | Simple filled |

## Color domains (architecture)

| Domain | Fill | Border | Use |
| ------ | ---- | ------ | --- |
| Business | `#E8F1FA` | `#232F3E` | Capabilities, outcomes |
| Application | `#F0F7E6` | `#1D8102` | Apps, services |
| Data | `#FFF3E0` | `#ED7100` | Data stores, products |
| Integration | `#F3E8FF` | `#5A3E85` | APIs, events, messaging |
| Security | `#FCE8E6` | `#D13212` | Trust, controls, IAM |
| Cloud / AWS | `#E6F2FF` | `#146EB4` | AWS accounts, regions |
| AI | `#EDE7F6` | `#5C2D91` | Models, RAG, agents |
| Platform | `#E0F7F5` | `#0073BB` | IDP, golden paths |
| Executive accent | `#C2A14D` | `#232F3E` | Outcomes / asks only |

Navy primary text: `#232F3E`  
Muted secondary: `#545B64`  
Success / healthy: `#1D8102`  
Warning: `#ED7100`  
Critical: `#D13212`

## Typography

| Element | Guidance |
| ------- | -------- |
| Title | Sans-serif, bold, 18–22pt equivalent |
| Service labels | Sans-serif, 11–13pt, never below readable slide size |
| Annotations | 10–12pt, muted |
| Numbers (steps) | Bold circle badges 1…n |

Prefer Inter / Helvetica / Amazon Ember equivalents. Avoid decorative fonts.

## Layout rules

1. **Left → right** primary data/control flow (top → bottom only for org/hierarchy)  
2. **Group** related services in labeled containers (Account, VPC, Trust Zone)  
3. **Number** workflow steps when process-oriented  
4. **Legend** required if >3 icon types or color meanings  
5. **Minimize crossing lines**; prefer orthogonal routing  
6. **One job per diagram** — split rather than clutter  
7. Progressive reveal: keep major components as **separate groups** for PowerPoint animation  

## Avoid

Cartoon graphics · 3D · random colors · dense spaghetti · tiny unreadable text · generic DB/cloud icons when AWS icons exist

## Executive vs technical views

| View | Detail | Audience |
| ---- | ------ | -------- |
| Executive | 5–9 boxes, outcomes language, no service clutter | CIO / exec |
| Concept | Frameworks, layers, domains | Learners |
| Reference | AWS icons, named services | Architects |
| Lab / infra | Exact resources, tags, flows | Hands-on |

## Accessibility

- Do not rely on color alone (use labels + icons)  
- Contrast text on fills ≥ WCAG AA where practical  
- Fiction notice on NorthStar case diagrams: footer “NorthStar (fictional)”
