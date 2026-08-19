# Diagram 12 — AI-agent integration (governed)

```mermaid
flowchart LR
  U[User] --> Ag[AI Agent]
  Ag --> Tools[Authorized tool layer]
  Tools --> Pol[Policy + HITL]
  Pol --> Plat[Integration platform]
  Plat --> Sys[Enterprise systems]
```

## Unacceptable

```mermaid
flowchart LR
  LLM[LLM] -->|forbidden| PDB[(Production database)]
```
